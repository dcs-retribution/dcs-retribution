from __future__ import annotations

from typing import Type

from game.theater import TheaterGroundObject
from .formationattack import (
    FormationAttackBuilder,
    FormationAttackFlightPlan,
    FormationAttackLayout,
)
from .invalidobjectivelocation import InvalidObjectiveLocation
from .tacticaloverlay import TacticalOverlay, TacticalOverlayDisplay, attack_run_overlay
from .waypointbuilder import StrikeTarget
from ..flightwaypointtype import FlightWaypointType
from ...theater.theatergroup import SceneryUnit


class StrikeFlightPlan(FormationAttackFlightPlan, TacticalOverlayDisplay):
    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder

    def tactical_overlay(self) -> TacticalOverlay:
        return attack_run_overlay(
            self.layout.ingress.position,
            self.package.target.position,
            self.layout.split.position,
        )


class Builder(FormationAttackBuilder[StrikeFlightPlan, FormationAttackLayout]):
    def layout(self) -> FormationAttackLayout:
        location = self.package.target

        if not isinstance(location, TheaterGroundObject):
            raise InvalidObjectiveLocation(self.flight.flight_type, location)

        targets: list[StrikeTarget] = []
        for idx, unit in enumerate(location.strike_targets):
            name = unit.type.id
            if isinstance(unit, SceneryUnit):
                name = unit.name
            targets.append(StrikeTarget(f"{name} #{idx}", unit))

        return self._build(FlightWaypointType.INGRESS_STRIKE, targets)

    def build(self, dump_debug_info: bool = False) -> StrikeFlightPlan:
        return StrikeFlightPlan(self.flight, self.layout())
