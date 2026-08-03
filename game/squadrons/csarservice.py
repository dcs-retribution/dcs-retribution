from __future__ import annotations

import logging
import random
from typing import Optional, TYPE_CHECKING

from dcs.mapping import Point

from game.squadrons.csarplacement import find_downed_pilot_position
from game.squadrons.downedpilot import DownedPilot
from game.utils import nautical_miles

if TYPE_CHECKING:
    from game.ato.flight import Flight
    from game.coalition import Coalition
    from game.game import Game
    from game.squadrons.pilot import Pilot
    from game.theater.player import Player

#: A downed pilot this close to a front line is treated as being in contested
#: territory and gets the shorter survival window.
_FRONT_LINE_DANGER = nautical_miles(30)

#: Fallback scatter radius (metres) when a loss has no DCS-reported position.
_FALLBACK_SCATTER_METERS = 5000.0


class CsarService:
    """Creates and resolves downed pilots for a game."""

    def __init__(self, game: Game) -> None:
        self.game = game

    def csar_enabled_for(self, player: Player) -> bool:
        settings = self.game.settings
        return settings.csar_enabled if player.is_blue else settings.csar_enabled_red

    def down_pilot(
        self,
        flight: Flight,
        pilot: Pilot,
        was_player: bool,
        position: Point,
    ) -> Optional[DownedPilot]:
        """Creates a downed pilot for a lost aircraft, or returns None.

        Returns None when no landable position could be found near ``position``
        (the caller should then kill the pilot instead).
        """
        valid = find_downed_pilot_position(self.game.theater, position)
        if valid is None:
            return None

        squadron = flight.squadron
        player = squadron.player
        downed = DownedPilot(
            pilot=pilot,
            squadron=squadron,
            _position=valid,
            player=player,
            turn_downed=self.game.turn,
            turns_remaining=self._survival_turns(valid, player),
            was_player=was_player,
            aircraft_name=squadron.aircraft.display_name,
            in_water=self.game.theater.is_in_sea(valid),
        )
        pilot.go_down()
        squadron.coalition.downed_pilots.append(downed)
        self.game.db.downed_pilots.add(downed.id, downed)
        logging.info(
            "%s from %s is down near %s; awaiting CSAR (%d turns).",
            pilot.name,
            squadron,
            valid,
            downed.turns_remaining,
        )
        return downed

    def fallback_position_for(self, flight: Flight) -> Point:
        """A scattered position near the flight's target for losses with no
        DCS-reported position (AI kills, skipped/simulated turns)."""
        target = flight.package.target
        return target.position.random_point_within(_FALLBACK_SCATTER_METERS)

    def _survival_turns(self, position: Point, player: Player) -> int:
        settings = self.game.settings
        theater = self.game.theater

        nearest_cp = theater.closest_control_point(position)
        in_hostile_territory = not nearest_cp.is_friendly(player)

        near_front = False
        for front_line in theater.conflicts():
            if (
                front_line.position.distance_to_point(position)
                < _FRONT_LINE_DANGER.meters
            ):
                near_front = True
                break

        if in_hostile_territory or near_front:
            return settings.csar_survival_turns_hostile
        return settings.csar_survival_turns

    # Rescue resolution ------------------------------------------------------

    def rescue(self, downed: DownedPilot) -> None:
        """Removes a downed pilot from the map and puts them into recovery."""
        settings = self.game.settings
        turns = (
            settings.csar_player_recovery_turns
            if downed.was_player
            else settings.csar_ai_recovery_turns
        )
        downed.pilot.begin_recovery(turns)
        self._remove(downed)
        self.game.message(
            "Pilot rescued",
            f"{downed.pilot.name} ({downed.aircraft_name}) was recovered by CSAR "
            f"and will return to {downed.squadron} in {turns} turn(s).",
        )

    def go_mia(self, downed: DownedPilot) -> None:
        downed.pilot.go_mia()
        self._remove(downed)
        self.game.message(
            "Pilot missing in action",
            f"{downed.pilot.name} ({downed.aircraft_name}) was never rescued and is "
            f"now missing in action.",
        )

    def _remove(self, downed: DownedPilot) -> None:
        coalition = downed.squadron.coalition
        if downed in coalition.downed_pilots:
            coalition.downed_pilots.remove(downed)
        try:
            self.game.db.downed_pilots.remove(downed.id)
        except KeyError:
            pass

    def advance_turn_for(self, coalition: Coalition) -> None:
        """Decrements a coalition's downed pilots' countdowns, expiring to MIA.

        Called at coalition turn end. Iterates a copy since ``go_mia`` mutates the
        underlying list.
        """
        for downed in list(coalition.downed_pilots):
            downed.turns_remaining -= 1
            if downed.turns_remaining <= 0:
                self.go_mia(downed)
