from __future__ import annotations

from typing import Type

from .formationattack import (
    FormationAttackBuilder,
    FormationAttackFlightPlan,
    FormationAttackLayout,
)
from .tacticaloverlay import TacticalOverlay, TacticalOverlayDisplay, attack_run_overlay
from .uizonedisplay import UiZone, UiZoneDisplay
from ..flightwaypointtype import FlightWaypointType
from ...utils import nautical_miles


class ArmedReconFlightPlan(
    FormationAttackFlightPlan, UiZoneDisplay, TacticalOverlayDisplay
):
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

    def tactical_overlay(self) -> TacticalOverlay:
        return attack_run_overlay(
            self.layout.ingress.position,
            self.package.target.position,
            self.layout.split.position,
        )


class Builder(FormationAttackBuilder[ArmedReconFlightPlan, FormationAttackLayout]):
    def layout(self) -> FormationAttackLayout:
        return self._build(FlightWaypointType.INGRESS_ARMED_RECON)

    def build(self, dump_debug_info: bool = False) -> ArmedReconFlightPlan:
        return ArmedReconFlightPlan(self.flight, self.layout())
