from __future__ import annotations

from datetime import timedelta
from typing import Type

from .formationattack import (
    FormationAttackBuilder,
    FormationAttackFlightPlan,
    FormationAttackLayout,
)
from .tacticaloverlay import (
    TacticalOverlay,
    TacticalOverlayDisplay,
    loiter_overlay,
    orbit_radius,
)
from .uizonedisplay import UiZone, UiZoneDisplay
from ..flightwaypoint import FlightWaypoint
from ..flightwaypointtype import FlightWaypointType
from ...utils import Distance, nautical_miles


class SeadFlightPlan(FormationAttackFlightPlan, UiZoneDisplay, TacticalOverlayDisplay):
    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder

    def default_tot_offset(self) -> timedelta:
        return -timedelta(minutes=1)

    @property
    def _loiter_anchor(self) -> FlightWaypoint:
        # Standoff loiter point (the "SEAD Search" anchor); fall back to the
        # target if the layout has no standoff anchor.
        return self.layout.initial or self.tot_waypoint

    @property
    def _engagement_range(self) -> Distance:
        return nautical_miles(
            self.flight.coalition.game.settings.sead_sweep_engagement_range_distance
        )

    def tactical_overlay(self) -> TacticalOverlay:
        # SEAD loiters at standoff and reacts to radars near its own position, so
        # both the orbit and the engagement bubble sit on the loiter anchor.
        anchor = self._loiter_anchor
        return loiter_overlay(
            orbit_center=anchor.position,
            loiter_radius=orbit_radius(
                self.flight.unit_type.preferred_patrol_speed(anchor.alt)
            ),
            engagement_center=anchor.position,
            engagement_range=self._engagement_range,
            target_position=self.tot_waypoint.position,
        )

    def ui_zone(self) -> UiZone:
        return UiZone([self._loiter_anchor.position], self._engagement_range)


class Builder(FormationAttackBuilder[SeadFlightPlan, FormationAttackLayout]):
    def layout(self) -> FormationAttackLayout:
        return self._build(FlightWaypointType.INGRESS_SEAD)

    def build(self, dump_debug_info: bool = False) -> SeadFlightPlan:
        return SeadFlightPlan(self.flight, self.layout())
