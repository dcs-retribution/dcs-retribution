from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Union

from game.ato.flighttype import FlightType
from game.commander.missionproposals import EscortType
from game.commander.tasks.packageplanningtask import PackagePlanningTask
from game.commander.theaterstate import TheaterState
from game.squadrons.downedpilot import DownedPilot
from game.theater.theatergroundobject import IadsGroundObject, NavalGroundObject
from game.utils import Distance, meters, nautical_miles

#: How far out an air defense is held to threaten a rescue helicopter.
#:
#: The planner's usual rule is the system's full engagement range, which is written
#: for strike aircraft at altitude. A rescue helicopter flies at treetop height, and a
#: long-range SAM cannot see that low beyond the radar horizon however far its missiles
#: reach. Without this a single S-300 150 nm away made every pilot on its side of the
#: map "threatened" -- including ones sitting next to their own airfield -- so nobody
#: was ever sent for them.
LOW_LEVEL_THREAT_RANGE = nautical_miles(30)


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
            # Worked out only when somebody is reading the log: it is the one thing
            # that says why a pilot nobody is coming for was left where they are.
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug(
                    "Not planning CSAR for %s: %s",
                    self.target.pilot.name,
                    self._describe_threats(state),
                )
            return False
        return super().preconditions_met(state)

    def threat_range_for(
        self, iads_threat: Union[IadsGroundObject, NavalGroundObject]
    ) -> Distance:
        return min(iads_threat.max_threat_range(), LOW_LEVEL_THREAT_RANGE)

    def _describe_threats(self, state: TheaterState) -> str:
        blockers = [
            f"{threat.name} ({threat.distance_to(self.target) / 1852:.0f} nm away)"
            for threat in self.iter_iads_threats(state)
            if self._get_weighted_threat_range(threat, state) < meters(0)
        ]
        return "inside the threat range of " + ", ".join(blockers)

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
        # Escorts, planned only if the approach turns out to be threatened (see
        # CsarFlightPlan.escorted_waypoints). Not propose_common_escorts(): that adds a
        # SEAD sweep, whose flight plan needs package waypoints, which a friendly
        # target never has. The escort plan builds its own, as it does for transports.
        #
        # Optional: the helicopters only ever travel with an escort that can keep up
        # with them, and most factions have none. Unescorted is how rescues went
        # before there were escorts, and a pilot who is not collected before their
        # timer runs out is lost, so a missing escort must not cancel the rescue.
        self.propose_flight(FlightType.SEAD_ESCORT, 2, EscortType.Sead, optional=True)
        self.propose_flight(FlightType.ESCORT, 2, EscortType.AirToAir, optional=True)
