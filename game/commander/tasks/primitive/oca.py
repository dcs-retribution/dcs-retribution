from __future__ import annotations

from dataclasses import dataclass

from game.ato.flighttype import FlightType
from game.commander.missionproposals import EscortType
from game.commander.tasks.packageplanningtask import PackagePlanningTask
from game.commander.theaterstate import TheaterState
from game.theater import ControlPoint


@dataclass
class PlanOcaStrike(PackagePlanningTask[ControlPoint]):
    aircraft_cold_start: bool

    def preconditions_met(self, state: TheaterState) -> bool:
        if self.target not in state.oca_targets:
            return False
        if not self.target_area_preconditions_met(state):
            return False
        return super().preconditions_met(state)

    def apply_effects(self, state: TheaterState) -> None:
        state.oca_targets.remove(self.target)

    def propose_flights(self) -> None:
        size = self.get_flight_size()
        if self.target.cptype == self.target.cptype.AIRBASE:
            self.propose_flight(FlightType.OCA_RUNWAY, size)  # type:ignore[unreachable]
        if self.aircraft_cold_start:
            self.propose_flight(FlightType.OCA_AIRCRAFT, 2)
        self.propose_common_escorts()
        if self.target.coalition.game.settings.autoplan_tankers_for_oca:
            self.propose_flight(FlightType.REFUELING, 1, EscortType.Refuel)
