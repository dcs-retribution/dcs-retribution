from __future__ import annotations

from dataclasses import dataclass

from game.ato.flighttype import FlightType
from game.commander.tasks.packageplanningtask import PackagePlanningTask
from game.commander.theaterstate import TheaterState
from game.squadrons.downedpilot import DownedPilot
from game.utils import meters


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
        # One flight collects the whole cluster, so take its other members off the
        # board too rather than planning a package each. The mission generator
        # rebuilds the same cluster from the target's position, so it knows who
        # else to expect at the pickup.
        radius = meters(state.context.settings.csar_cluster_radius)
        for pilot in self.target.cluster(radius):
            if pilot in state.csar_targets:
                state.csar_targets.remove(pilot)
        state.csar_flights_planned += 1
        super().apply_effects(state)

    def propose_flights(self) -> None:
        # Deliberately not get_flight_size(): the 2/3/4-ship weights are about
        # putting enough ordnance on a target, which has nothing to do with how
        # many helicopters it takes to collect one pilot. A pair by default, so
        # the lead has cover on the ground, or a singleton if configured.
        settings = self.target.coalition.game.settings
        self.propose_flight(FlightType.CSAR, 1 if settings.csar_single_flight else 2)
        self.propose_common_escorts()
