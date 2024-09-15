from __future__ import annotations

from dataclasses import dataclass

from game.ato.flighttype import FlightType
from game.commander.tasks.packageplanningtask import PackagePlanningTask
from game.commander.theaterstate import TheaterState
from game.theater import ControlPoint


@dataclass
class PlanAirAssault(PackagePlanningTask[ControlPoint]):
    def preconditions_met(self, state: TheaterState) -> bool:
        if self.target not in state.vulnerable_control_points:
            return False
        if not self.target_area_preconditions_met(state):
            return False
        return super().preconditions_met(state)

    def apply_effects(self, state: TheaterState) -> None:
        state.vulnerable_control_points.remove(self.target)

    def propose_flights(self) -> None:
        self.propose_flight(FlightType.AIR_ASSAULT, self.get_flight_size())
        self.propose_common_escorts()
