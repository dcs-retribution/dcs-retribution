from __future__ import annotations

from dataclasses import dataclass

from game.ato.flighttype import FlightType
from game.commander.missionproposals import EscortType
from game.commander.tasks.packageplanningtask import PackagePlanningTask
from game.commander.theaterstate import TheaterState
from game.theater.theatergroundobject import TheaterGroundObject


@dataclass
class PlanStrike(PackagePlanningTask[TheaterGroundObject]):
    def preconditions_met(self, state: TheaterState) -> bool:
        if self.target not in state.strike_targets:
            return False
        if not self.target_area_preconditions_met(state):
            return False
        return super().preconditions_met(state)

    def apply_effects(self, state: TheaterState) -> None:
        state.strike_targets.remove(self.target)

    def propose_flights(self) -> None:
        tgt_count = self.target.alive_unit_count
        self.propose_flight(FlightType.STRIKE, min(4, (tgt_count // 2) + tgt_count % 2))
        self.propose_common_escorts()
        if self.target.coalition.game.settings.autoplan_tankers_for_strike:
            self.propose_flight(FlightType.REFUELING, 1, EscortType.Refuel)
