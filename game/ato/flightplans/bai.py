from __future__ import annotations

from typing import Type

from game.theater.theatergroundobject import TheaterGroundObject
from .formationattack import (
    FormationAttackBuilder,
    FormationAttackFlightPlan,
    FormationAttackLayout,
)
from .invalidobjectivelocation import InvalidObjectiveLocation
from .tacticaloverlay import TacticalOverlay, TacticalOverlayDisplay, attack_run_overlay
from .waypointbuilder import StrikeTarget
from ..flightwaypointtype import FlightWaypointType


class BaiFlightPlan(FormationAttackFlightPlan, TacticalOverlayDisplay):
    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder

    def tactical_overlay(self) -> TacticalOverlay:
        return attack_run_overlay(
            self.layout.ingress.position,
            self.package.target.position,
            self.layout.split.position,
        )


class Builder(FormationAttackBuilder[BaiFlightPlan, FormationAttackLayout]):
    def layout(self) -> FormationAttackLayout:
        location = self.package.target

        from game.transfers import Convoy

        targets: list[StrikeTarget] = []
        if isinstance(location, TheaterGroundObject):
            for group in location.groups:
                if group.units:
                    targets.append(
                        StrikeTarget(f"{group.group_name} at {location.name}", group)
                    )
        elif isinstance(location, Convoy):
            targets.append(StrikeTarget(location.name, location))
        else:
            raise InvalidObjectiveLocation(self.flight.flight_type, location)

        return self._build(FlightWaypointType.INGRESS_BAI, targets)

    def build(self, dump_debug_info: bool = False) -> BaiFlightPlan:
        return BaiFlightPlan(self.flight, self.layout())
