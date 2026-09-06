from __future__ import annotations

import logging
from typing import Type

from game.theater import Airfield, Fob
from .formationattack import (
    FormationAttackBuilder,
    FormationAttackFlightPlan,
    FormationAttackLayout,
)
from .invalidobjectivelocation import InvalidObjectiveLocation
from .tacticaloverlay import TacticalOverlay, TacticalOverlayDisplay, attack_run_overlay
from ..flightwaypointtype import FlightWaypointType


class OcaAircraftFlightPlan(FormationAttackFlightPlan, TacticalOverlayDisplay):
    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder

    def tactical_overlay(self) -> TacticalOverlay:
        return attack_run_overlay(
            self.layout.ingress.position,
            self.package.target.position,
            self.layout.split.position,
        )


class Builder(FormationAttackBuilder[OcaAircraftFlightPlan, FormationAttackLayout]):
    def layout(self) -> FormationAttackLayout:
        location = self.package.target

        if not isinstance(location, Airfield) and not isinstance(location, Fob):
            logging.exception(
                f"Invalid Objective Location for OCA/Aircraft flight "
                f"{self.flight=} at {location=}."
            )
            raise InvalidObjectiveLocation(self.flight.flight_type, location)

        return self._build(FlightWaypointType.INGRESS_OCA_AIRCRAFT)

    def build(self, dump_debug_info: bool = False) -> OcaAircraftFlightPlan:
        return OcaAircraftFlightPlan(self.flight, self.layout())
