from __future__ import annotations

from datetime import timedelta
from typing import Type

from .formationattack import (
    FormationAttackBuilder,
    FormationAttackFlightPlan,
    FormationAttackLayout,
)
from ..flightwaypointtype import FlightWaypointType


class SeadSweepFlightPlan(FormationAttackFlightPlan):
    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder

    def default_tot_offset(self) -> timedelta:
        return -timedelta(minutes=2)


class Builder(FormationAttackBuilder[SeadSweepFlightPlan, FormationAttackLayout]):
    def layout(self) -> FormationAttackLayout:
        return self._build(FlightWaypointType.INGRESS_SEAD_SWEEP)

    def build(self, dump_debug_info: bool = False) -> SeadSweepFlightPlan:
        return SeadSweepFlightPlan(self.flight, self.layout())
