from __future__ import annotations

from dataclasses import dataclass

from game.ato.flighttype import FlightType
from game.commander.tasks.packageplanningtask import PackagePlanningTask
from game.commander.theaterstate import TheaterState
from game.theater import MissionTarget


@dataclass
class PlanRefueling(PackagePlanningTask[MissionTarget]):
    def preconditions_met(self, state: TheaterState) -> bool:
        if (
            state.context.coalition.player
            and not state.context.settings.auto_ato_behavior_tankers
        ):
            return False
        if not super().preconditions_met(state):
            return False
        return self.target in state.refueling_targets

    def apply_effects(self, state: TheaterState) -> None:
        state.refueling_targets.remove(self.target)

    def propose_flights(self) -> None:
        self.propose_flight(FlightType.REFUELING, 1)
