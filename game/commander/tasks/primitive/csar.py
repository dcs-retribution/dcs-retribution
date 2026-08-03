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
        # Only so much of the ATO is worth spending on rescues in one turn. Pilots
        # are offered closest-to-base first, so the ones dropped here are the least
        # reachable; they wait for a later turn if they survive that long.
        if state.csar_flights_planned >= state.context.settings.max_csar_flights:
            return False
        # Don't feed rescue helicopters into a live SAM ring; the planner will
        # schedule DEAD/SEAD first and revisit the pilot on a later pass.
        if not self.target_area_preconditions_met(state):
            return False
        return super().preconditions_met(state)

    def apply_effects(self, state: TheaterState) -> None:
        state.csar_targets.remove(self.target)
        state.csar_flights_planned += 1
        super().apply_effects(state)

    def propose_flights(self) -> None:
        self.propose_flight(FlightType.CSAR, 2)
        self.propose_common_escorts()
