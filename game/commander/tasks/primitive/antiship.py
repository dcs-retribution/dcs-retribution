from __future__ import annotations

from dataclasses import dataclass

from game.ato.flighttype import FlightType
from game.commander.missionproposals import EscortType
from game.commander.tasks.packageplanningtask import PackagePlanningTask
from game.commander.theaterstate import TheaterState
from game.theater.theatergroundobject import NavalGroundObject
from game.utils import meters


@dataclass
class PlanAntiShip(PackagePlanningTask[NavalGroundObject]):
    def preconditions_met(self, state: TheaterState) -> bool:
        if (
            self.target not in state.threatening_air_defenses
            and not self.target.is_naval_control_point
        ):
            return False
        if not self.target_area_preconditions_met(state, ignore_iads=True):
            return False
        return super().preconditions_met(state)

    def apply_effects(self, state: TheaterState) -> None:
        state.eliminate_ship(self.target)
        super().apply_effects(state)

    def propose_flights(self) -> None:
        size = self.get_flight_size()
        if self.target.max_detection_range() > meters(0):
            size = 4  # attempt to saturate ship's air-defences
            self.propose_flight(FlightType.ANTISHIP, size)
            self.propose_flight(FlightType.ESCORT, 2, EscortType.AirToAir)
        self.propose_flight(FlightType.ANTISHIP, size)
        self.propose_flight(FlightType.ESCORT, 2, EscortType.AirToAir)
        if self.target.max_detection_range() > meters(0):
            self.propose_flight(FlightType.SEAD, 2, EscortType.Sead)
