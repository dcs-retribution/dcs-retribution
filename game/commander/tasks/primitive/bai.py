from __future__ import annotations

from dataclasses import dataclass

from game.ato.flighttype import FlightType
from game.commander.tasks.packageplanningtask import PackagePlanningTask
from game.commander.theaterstate import TheaterState
from game.theater.theatergroundobject import VehicleGroupGroundObject


@dataclass
class PlanBai(PackagePlanningTask[VehicleGroupGroundObject]):
    def preconditions_met(self, state: TheaterState) -> bool:
        if not state.has_battle_position(self.target):
            return False
        if not self.target_area_preconditions_met(state):
            return False
        return super().preconditions_met(state)

    def apply_effects(self, state: TheaterState) -> None:
        state.eliminate_battle_position(self.target)
        super().apply_effects(state)

    def propose_flights(self) -> None:
        tgt_count = self.target.alive_unit_count
        self.propose_flight(FlightType.BAI, min(4, (tgt_count // 4) + 1))
        self.propose_common_escorts()
