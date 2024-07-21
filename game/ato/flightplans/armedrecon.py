from __future__ import annotations

from typing import Type

from .formationattack import (
    FormationAttackBuilder,
    FormationAttackFlightPlan,
    FormationAttackLayout,
)
from .uizonedisplay import UiZone, UiZoneDisplay
from ..flightwaypointtype import FlightWaypointType
from ...utils import nautical_miles


class ArmedReconFlightPlan(FormationAttackFlightPlan, UiZoneDisplay):
    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder

    def ui_zone(self) -> UiZone:
        return UiZone(
            [self.tot_waypoint.position],
            nautical_miles(
                self.flight.coalition.game.settings.armed_recon_engagement_range_distance
            ),
        )


class Builder(FormationAttackBuilder[ArmedReconFlightPlan, FormationAttackLayout]):
    def layout(self) -> FormationAttackLayout:
        return self._build(FlightWaypointType.INGRESS_ARMED_RECON)

    def build(self, dump_debug_info: bool = False) -> ArmedReconFlightPlan:
        return ArmedReconFlightPlan(self.flight, self.layout())
