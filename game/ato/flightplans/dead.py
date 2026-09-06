from __future__ import annotations

import logging
from typing import Type

from game.theater.theatergroundobject import (
    EwrGroundObject,
    SamGroundObject,
)
from .formationattack import (
    FormationAttackBuilder,
    FormationAttackFlightPlan,
    FormationAttackLayout,
)
from .invalidobjectivelocation import InvalidObjectiveLocation
from .tacticaloverlay import TacticalOverlay, TacticalOverlayDisplay, attack_run_overlay
from ..flightwaypointtype import FlightWaypointType


class DeadFlightPlan(FormationAttackFlightPlan, TacticalOverlayDisplay):
    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder

    def tactical_overlay(self) -> TacticalOverlay:
        return attack_run_overlay(
            self.layout.ingress.position,
            self.package.target.position,
            self.layout.split.position,
        )


class Builder(FormationAttackBuilder[DeadFlightPlan, FormationAttackLayout]):
    def layout(self) -> FormationAttackLayout:
        location = self.package.target

        is_ewr = isinstance(location, EwrGroundObject)
        is_sam = isinstance(location, SamGroundObject)
        if not is_ewr and not is_sam:
            logging.exception(
                f"Invalid Objective Location for DEAD flight {self.flight=} at "
                f"{location=}"
            )
            raise InvalidObjectiveLocation(self.flight.flight_type, location)

        return self._build(FlightWaypointType.INGRESS_DEAD)

    def build(self, dump_debug_info: bool = False) -> DeadFlightPlan:
        return DeadFlightPlan(self.flight, self.layout())
