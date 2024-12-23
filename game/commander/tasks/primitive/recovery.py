from __future__ import annotations

from dataclasses import dataclass

from game.ato.flighttype import FlightType
from game.commander.tasks.packageplanningtask import PackagePlanningTask
from game.commander.theaterstate import TheaterState
from game.theater import ControlPoint


@dataclass
class PlanRecovery(PackagePlanningTask[ControlPoint]):
    def preconditions_met(self, state: TheaterState) -> bool:
        if (
            state.context.coalition.player
            and not state.context.settings.auto_ato_behavior_tankers
        ):
            return False
        ac_per_tanker = state.context.settings.aircraft_per_recovery_tanker
        if not (
            self.target in state.recovery_targets
            and state.recovery_targets[self.target] >= ac_per_tanker
        ):
            return False
        return super().preconditions_met(state)

    def apply_effects(self, state: TheaterState) -> None:
        ac_per_tanker = state.context.settings.aircraft_per_recovery_tanker
        state.recovery_targets[self.target] -= ac_per_tanker

    def propose_flights(self) -> None:
        self.propose_flight(FlightType.RECOVERY, 1)
