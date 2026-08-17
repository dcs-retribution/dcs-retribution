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
    from game.theater import ControlPoint
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
        """Decides what becomes of the pilot of a lost aircraft.

        Returns the downed pilot if one was placed on the map, or None if their
        fate was settled here -- killed, captured, or walked home. Either way the
        pilot's own state is set before returning, so callers have nothing left to
        do.
        """
        squadron = flight.squadron
        player = squadron.player

        resolved = self._resolve_near_control_point(pilot, position, player, was_player)
        if resolved:
            return None

        valid = find_downed_pilot_position(self.game.theater, position)
        if valid is None:
            # Nowhere survivable to put them.
            pilot.kill()
            return None

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

    def _resolve_near_control_point(
        self, pilot: Pilot, position: Point, player: Player, was_player: bool
    ) -> bool:
        """Settles a pilot who came down on top of a control point, if they did.

        Close enough to a base and there is nothing for a rescue flight to do: on
        friendly ground they walk back and go into recovery, on enemy ground they
        are captured. Returns whether the pilot was dealt with here.
        """
        radius = nautical_miles(self.game.settings.csar_control_point_radius)
        if radius.meters <= 0:
            return False

        nearest = self.game.theater.closest_control_point(position)
        if nearest.position.distance_to_point(position) > radius.meters:
            return False

        # They did come down, whatever happens next. Also what lets go_mia()
        # accept them: it only transitions a pilot who is already Downed.
        pilot.go_down()
        if nearest.is_friendly(player):
            turns = (
                self.game.settings.csar_player_recovery_turns
                if was_player
                else self.game.settings.csar_ai_recovery_turns
            )
            pilot.begin_recovery(turns)
            self.game.message(
                "Pilot recovered",
                f"{pilot.name} came down inside friendly lines near {nearest.name}. "
                f"Recovered by Control Point. They return to duty in {turns} "
                f"turn(s).",
            )
        else:
            # Held by the base that took them, so retaking it brings them home.
            pilot.go_mia(held_at=nearest.id)
            self.game.message(
                "Pilot captured",
                f"{pilot.name} came down inside enemy lines near {nearest.name} "
                f"and is now held there.",
            )
        return True

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
        captor = self._nearest_enemy_control_point(downed)
        downed.pilot.go_mia(held_at=captor.id if captor is not None else None)
        self._remove(downed)
        if captor is not None:
            self.game.message(
                "Pilot captured",
                f"{downed.pilot.name} ({downed.aircraft_name}) was never rescued and "
                f"is now held at {captor.name}. Taking it would bring them home.",
            )
        else:
            self.game.message(
                "Pilot missing in action",
                f"{downed.pilot.name} ({downed.aircraft_name}) was never rescued and "
                f"is now missing in action.",
            )

    def _nearest_enemy_control_point(
        self, downed: DownedPilot
    ) -> Optional[ControlPoint]:
        """The enemy base that would have picked this pilot up."""
        enemy = [
            cp
            for cp in self.game.theater.controlpoints
            if not cp.is_friendly(downed.player)
        ]
        if not enemy:
            return None
        return min(enemy, key=lambda cp: cp.position.distance_to_point(downed.position))

    def liberate_prisoners_at(self, control_point: ControlPoint) -> None:
        """Frees any pilots held at a control point that has just changed hands.

        Called for every capture, so it also has to check the base actually
        belongs to the prisoner's coalition now -- losing a base does not free the
        prisoners in it, and a base can be taken by the side already holding them.
        """
        for coalition in (self.game.blue, self.game.red):
            turns = (
                self.game.settings.csar_player_recovery_turns
                if coalition.player.is_blue
                else self.game.settings.csar_ai_recovery_turns
            )
            if not control_point.is_friendly(coalition.player):
                continue
            for squadron in coalition.air_wing.iter_squadrons():
                for pilot in list(squadron.missing_pilots):
                    if pilot.held_at != control_point.id:
                        continue
                    pilot.release_from_captivity(turns)
                    self.game.message(
                        "Prisoner of war freed",
                        f"{pilot.name} was freed by the capture of "
                        f"{control_point.name} and returns to {squadron} in "
                        f"{turns} turn(s).",
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
