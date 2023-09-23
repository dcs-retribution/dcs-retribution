from __future__ import annotations

from dataclasses import dataclass

from game.ato.flighttype import FlightType
from game.commander.missionproposals import EscortType
from game.commander.tasks.packageplanningtask import PackagePlanningTask
from game.commander.theaterstate import TheaterState
from game.transfers import CargoShip


@dataclass
class PlanAntiShipping(PackagePlanningTask[CargoShip]):
    def preconditions_met(self, state: TheaterState) -> bool:
        if self.target not in state.enemy_shipping:
            return False
        if not self.target_area_preconditions_met(state):
            return False
        return super().preconditions_met(state)

    def apply_effects(self, state: TheaterState) -> None:
        state.enemy_shipping.remove(self.target)

    def propose_flights(self) -> None:
        size = self.get_flight_size()
        self.propose_flight(FlightType.ANTISHIP, size)
        self.propose_flight(FlightType.ESCORT, 2, EscortType.AirToAir)
