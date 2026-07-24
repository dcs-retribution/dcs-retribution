from __future__ import annotations

from dataclasses import dataclass

from game.ato.flighttype import FlightType
from game.commander.tasks.packageplanningtask import PackagePlanningTask
from game.commander.theaterstate import TheaterState
from game.squadrons.downedpilot import DownedPilot


@dataclass
class PlanCsar(PackagePlanningTask[DownedPilot]):
    def preconditions_met(self, state: TheaterState) -> bool:
        if self.target not in state.csar_targets:
            return False
        # Don't feed rescue helicopters into a live SAM ring; the planner will
        # schedule DEAD/SEAD first and revisit the pilot on a later pass.
        if not self.target_area_preconditions_met(state):
            return False
        return super().preconditions_met(state)

    def apply_effects(self, state: TheaterState) -> None:
        state.csar_targets.remove(self.target)
        super().apply_effects(state)

    def propose_flights(self) -> None:
        self.propose_flight(FlightType.CSAR, 2)
        self.propose_common_escorts()
