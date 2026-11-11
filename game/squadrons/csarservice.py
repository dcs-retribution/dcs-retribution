from __future__ import annotations

import logging
import random
from dataclasses import dataclass
from enum import Enum, auto
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
    from game.squadrons.squadron import Squadron
    from game.theater import ControlPoint
    from game.theater.player import Player

#: A downed pilot this close to a front line is treated as being in contested
#: territory and gets the shorter survival window.
_FRONT_LINE_DANGER = nautical_miles(30)

#: Fallback scatter radius (metres) when a loss has no DCS-reported position.
_FALLBACK_SCATTER_METERS = 5000.0


class _Fate(Enum):
    """What a control point within reach does with a pilot on the ground."""

    #: A friendly base or ship: they are picked up and go into recovery.
    RECOVER = auto()
    #: An enemy land base: taken prisoner, and held there until it is retaken.
    CAPTURE = auto()
    #: An enemy ship: lost to us, but nobody is holding them anywhere that could
    #: ever be captured to bring them home.
    MISSING = auto()


@dataclass(frozen=True)
class CapturedPilot:
    """A pilot taken prisoner this turn, for the debriefing report.

    Recorded rather than derived, because by the time the debrief is drawn the
    only trace on the pilot is a ``held_at`` id -- which says where they are, not
    that it happened this turn.
    """

    name: str
    aircraft: str
    squadron: str
    player: Player
    control_point: str


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

        resolved = self._resolve_near_control_point(
            pilot, position, player, was_player, squadron
        )
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

    def _record_capture(
        self,
        name: str,
        aircraft: str,
        squadron: str,
        player: Player,
        control_point: str,
    ) -> None:
        self.game.pilots_captured_this_turn.append(
            CapturedPilot(
                name=name,
                aircraft=aircraft,
                squadron=squadron,
                player=player,
                control_point=control_point,
            )
        )

    def _nearest_base(self, position: Point) -> Optional[ControlPoint]:
        """The nearest control point that has a side, ships included.

        Every CSAR question about "whose ground is this" goes through here.
        Carriers and LHAs count, or a pilot in the water beside their own boat is
        measured against some airfield over the horizon instead. Neutral bases do
        not: they belong to neither side, so they neither bring anyone home nor
        take prisoners until somebody captures them.
        """
        nearest = self.game.theater.closest_control_point(
            position, allow_naval=True, include_neutral=False
        )
        if nearest.captured.is_neutral:
            # Only possible if every control point is neutral.
            return None
        return nearest

    def _fate_within_radius(
        self, position: Point, player: Player
    ) -> Optional[tuple[_Fate, ControlPoint]]:
        """What happens to a pilot at ``position`` without any rescue flight.

        None unless they are inside csar_control_point_radius of the nearest
        base, in which case that base settles it.
        """
        radius = nautical_miles(self.game.settings.csar_control_point_radius)
        if radius.meters <= 0:
            return None

        nearest = self._nearest_base(position)
        if nearest is None:
            return None
        if nearest.position.distance_to_point(position) > radius.meters:
            return None

        if nearest.is_friendly(player):
            return _Fate.RECOVER, nearest
        if nearest.is_fleet:
            # A ship cannot be captured, so a prisoner aboard one could never be
            # freed. They are missing, not held.
            return _Fate.MISSING, nearest
        return _Fate.CAPTURE, nearest

    def _recovery_turns(self, was_player: bool) -> int:
        settings = self.game.settings
        if was_player:
            return settings.csar_player_recovery_turns
        return settings.csar_ai_recovery_turns

    def _apply_fate(
        self,
        fate: _Fate,
        control_point: ControlPoint,
        pilot: Pilot,
        was_player: bool,
        player: Player,
        aircraft: str,
        squadron: str,
    ) -> None:
        """Carries out a fate from ``_fate_within_radius`` on an already-Downed
        pilot. Shared by the landing check and the turn-end re-check."""
        if fate is _Fate.RECOVER:
            turns = self._recovery_turns(was_player)
            pilot.begin_recovery(turns)
            if control_point.is_fleet:
                where = f"was picked up near {control_point.name}"
            else:
                where = f"is inside friendly lines near {control_point.name}"
            self.game.message(
                "Pilot recovered",
                f"{pilot.name} {where}. Recovered by Control Point. They return "
                f"to duty in {turns} turn(s).",
            )
        elif fate is _Fate.CAPTURE:
            # Held by the base that took them, so retaking it brings them home.
            pilot.go_mia(held_at=control_point.id)
            self._record_capture(
                pilot.name, aircraft, squadron, player, control_point.name
            )
            self.game.message(
                "Pilot captured",
                f"{pilot.name} is inside enemy lines near {control_point.name} "
                f"and is now held there.",
            )
        else:
            pilot.go_mia()
            self.game.message(
                "Pilot missing in action",
                f"{pilot.name} was lost near the enemy ships of "
                f"{control_point.name} and is now missing in action.",
            )

    def _resolve_near_control_point(
        self,
        pilot: Pilot,
        position: Point,
        player: Player,
        was_player: bool,
        squadron: Squadron,
    ) -> bool:
        """Settles a pilot who came down on top of a control point, if they did.

        Close enough to a base and there is nothing for a rescue flight to do: by
        a friendly base or ship they are brought in and go into recovery, by an
        enemy base they are captured, by enemy ships they are simply lost. Returns
        whether the pilot was dealt with here.
        """
        resolved = self._fate_within_radius(position, player)
        if resolved is None:
            return False
        fate, control_point = resolved

        # They did come down, whatever happens next. Also what lets go_mia()
        # accept them: it only transitions a pilot who is already Downed.
        pilot.go_down()
        self._apply_fate(
            fate,
            control_point,
            pilot,
            was_player,
            player,
            squadron.aircraft.display_name,
            str(squadron),
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

        # Neutral ground is nobody's, so it does not make territory hostile.
        nearest_cp = self._nearest_base(position)
        in_hostile_territory = nearest_cp is not None and not nearest_cp.is_friendly(
            player
        )

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
        turns = self._recovery_turns(downed.was_player)
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
            self._record_capture(
                downed.pilot.name,
                downed.aircraft_name,
                str(downed.squadron),
                downed.player,
                captor.name,
            )
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
        """The enemy base that took this pilot prisoner, if any did.

        Two conditions, both required: they have to be in enemy-held territory
        (the nearest base is hostile) *and* within csar_capture_radius of it.
        Without the distance test an unrescued pilot was recorded as captured by
        whatever enemy base happened to be nearest, even one on the far side of
        the map.

        Its own setting rather than the landing radius that resolves a pilot when
        they first come down: anyone still on the map is by definition outside
        that one, so reusing it here would mean nobody is ever captured.

        Neutral bases take nobody, and nor do enemy ships -- there would be no
        way to ever get the prisoner back.

        Anyone else is simply missing: nobody reached them either way.
        """
        radius = nautical_miles(self.game.settings.csar_capture_radius)
        if radius.meters <= 0:
            return None

        nearest = self._nearest_base(downed.position)
        if nearest is None or nearest.is_friendly(downed.player):
            return None
        if nearest.is_fleet:
            return None
        if nearest.position.distance_to_point(downed.position) > radius.meters:
            return None
        return nearest

    def liberate_prisoners_at(self, control_point: ControlPoint) -> None:
        """Frees any pilots held at a control point that has just changed hands.

        Called for every capture, so it also has to check the base actually
        belongs to the prisoner's coalition now -- losing a base does not free the
        prisoners in it, and a base can be taken by the side already holding them.
        """
        for coalition in (self.game.blue, self.game.red):
            if not control_point.is_friendly(coalition.player):
                continue
            for squadron in coalition.air_wing.iter_squadrons():
                for pilot in list(squadron.missing_pilots):
                    if pilot.held_at != control_point.id:
                        continue
                    # Per pilot, not per coalition: whether a human flew them is
                    # what the two recovery settings distinguish, exactly as for a
                    # CSAR rescue. Keying off the coalition gave every blue pilot
                    # the (shorter) player figure.
                    turns = self._recovery_turns(pilot.player)
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
        """Ages a coalition's downed pilots, expiring to MIA.

        Before the countdown, anyone a base can now reach is settled without a
        rescue flight, exactly as if they had just come down there. The map moves
        under a waiting pilot: a carrier sails closer, a base changes hands, a
        neutral base is taken by one side or the other.

        Called at coalition turn end, after the turn's captures are committed.
        Iterates a copy since resolving a pilot mutates the underlying list.
        """
        for downed in list(coalition.downed_pilots):
            resolved = self._fate_within_radius(downed.position, downed.player)
            if resolved is not None:
                fate, control_point = resolved
                self._apply_fate(
                    fate,
                    control_point,
                    downed.pilot,
                    downed.was_player,
                    downed.player,
                    downed.aircraft_name,
                    str(downed.squadron),
                )
                self._remove(downed)
                continue

            downed.turns_remaining -= 1
            if downed.turns_remaining <= 0:
                self.go_mia(downed)
