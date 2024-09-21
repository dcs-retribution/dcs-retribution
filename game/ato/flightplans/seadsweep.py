from __future__ import annotations

from datetime import timedelta
from typing import Type

from .formationattack import (
    FormationAttackBuilder,
    FormationAttackFlightPlan,
    FormationAttackLayout,
)
from .uizonedisplay import UiZoneDisplay, UiZone
from ..flightwaypointtype import FlightWaypointType
from ...utils import nautical_miles


class SeadSweepFlightPlan(FormationAttackFlightPlan, UiZoneDisplay):
    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder

    def default_tot_offset(self) -> timedelta:
        return -timedelta(minutes=2)

    def ui_zone(self) -> UiZone:
        return UiZone(
            [self.tot_waypoint.position],
            nautical_miles(
                self.flight.coalition.game.settings.sead_sweep_engagement_range_distance
            ),
        )


class Builder(FormationAttackBuilder[SeadSweepFlightPlan, FormationAttackLayout]):
    def layout(self) -> FormationAttackLayout:
        return self._build(FlightWaypointType.INGRESS_SEAD_SWEEP)

    def build(self, dump_debug_info: bool = False) -> SeadSweepFlightPlan:
        return SeadSweepFlightPlan(self.flight, self.layout())
