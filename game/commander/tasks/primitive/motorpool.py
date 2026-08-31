from __future__ import annotations

from dataclasses import dataclass

from game.ato.flighttype import FlightType
from game.commander.tasks.packageplanningtask import PackagePlanningTask
from game.commander.theaterstate import TheaterState
from game.theater.theatergroundobject import MotorpoolGroundObject


@dataclass
class PlanMotorpoolAttack(PackagePlanningTask[MotorpoolGroundObject]):
    """Plans an armed recon package against an enemy motorpool depot."""

    def preconditions_met(self, state: TheaterState) -> bool:
        if self.target not in state.motorpool_targets:
            return False
        if not self._rendered_unit_count():
            return False
        if not self.target_area_preconditions_met(state):
            return False
        return super().preconditions_met(state)

    def apply_effects(self, state: TheaterState) -> None:
        state.motorpool_targets.remove(self.target)
        super().apply_effects(state)

    def propose_flights(self) -> None:
        self.propose_flight(FlightType.ARMED_RECON, self.get_flight_size())
        self.propose_common_escorts()

    def _rendered_unit_count(self) -> int:
        from game.theater.theatergroundobject import motorpool_rendered_unit_count

        settings = self.target.coalition.game.settings
        return motorpool_rendered_unit_count(
            self.target,
            settings.motorpool_enabled,
            settings.motorpool_spawn_cap,
        )
