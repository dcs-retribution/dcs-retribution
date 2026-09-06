from __future__ import annotations

from datetime import datetime, timedelta
from typing import Type

from .formationattack import (
    FormationAttackBuilder,
    FormationAttackFlightPlan,
    FormationAttackLayout,
)
from .uizonedisplay import UiZone, UiZoneDisplay
from ..flighttype import FlightType
from ..flightwaypointtype import FlightWaypointType
from ...utils import nautical_miles

# Plain SEAD reactively fires HARMs from its loiter anchor. The planner overlay shows a
# fixed HARM-reach bubble rather than the user-tunable SEAD-sweep engagement range, so
# the orbit is always drawn against a realistic engagement envelope.
SEAD_ENGAGEMENT_RANGE = nautical_miles(20)


def _loiter_end_time(
    tot: datetime, mate_departures: list[datetime], fallback_window: int
) -> datetime:
    """Absolute mission time a SEAD loiter should break off.

    `mate_departures` is the `mission_departure_time` of every non-SEAD package-mate
    (the time it leaves the target area). The loiter holds until the last of them is
    gone. With no gating mates we fall back to `tot + fallback_window`. Floored at `tot`
    so a package whose mates all depart before the SEAD arrives never yields a stop time
    before arrival. No upper cap: the package schedule, native winchester, and native
    bingo-fuel RTB are the natural bounds.
    """
    if not mate_departures:
        return tot + timedelta(seconds=fallback_window)
    return max(tot, *mate_departures)


class SeadFlightPlan(FormationAttackFlightPlan, UiZoneDisplay):
    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder

    def default_tot_offset(self) -> timedelta:
        return -timedelta(minutes=1)

    @property
    def loiter_end_time(self) -> datetime:
        """When the SEAD loiter breaks off: the latest a non-SEAD package-mate leaves
        the target area. SEAD mates are excluded so a loiter never gates on itself or a
        sibling SEAD loiter."""
        mate_departures = [
            flight.flight_plan.mission_departure_time
            for flight in self.package.flights
            if flight.flight_type is not FlightType.SEAD
        ]
        fallback = self.flight.coalition.game.settings.sead_loiter_max_window_seconds
        return _loiter_end_time(self.tot, mate_departures, fallback)

    def ui_zone(self) -> UiZone:
        # Centre the HARM-reach bubble on the loiter anchor (where the flight orbits and
        # engages), falling back to the target if no anchor was planned.
        anchor = self.layout.initial or self.tot_waypoint
        return UiZone([anchor.position], SEAD_ENGAGEMENT_RANGE)


class Builder(FormationAttackBuilder[SeadFlightPlan, FormationAttackLayout]):
    def layout(self) -> FormationAttackLayout:
        return self._build(FlightWaypointType.INGRESS_SEAD)

    def build(self, dump_debug_info: bool = False) -> SeadFlightPlan:
        return SeadFlightPlan(self.flight, self.layout())
