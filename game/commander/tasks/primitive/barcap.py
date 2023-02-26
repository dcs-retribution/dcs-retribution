from __future__ import annotations

import random
from dataclasses import dataclass
from random import randint

from game.ato.flighttype import FlightType
from game.commander.tasks.packageplanningtask import PackagePlanningTask
from game.commander.theaterstate import TheaterState
from game.theater import ControlPoint


@dataclass
class PlanBarcap(PackagePlanningTask[ControlPoint]):
    max_orders: int

    def preconditions_met(self, state: TheaterState) -> bool:
        if not state.barcaps_needed[self.target]:
            return False
        return super().preconditions_met(state)

    def apply_effects(self, state: TheaterState) -> None:
        state.barcaps_needed[self.target] -= 1

    def propose_flights(self) -> None:
        size = self.get_flight_size()
        self.propose_flight(FlightType.BARCAP, size)

    @property
    def purchase_multiplier(self) -> int:
        return self.max_orders
