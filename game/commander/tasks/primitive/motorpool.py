from __future__ import annotations

from dataclasses import dataclass

from game.ato.flighttype import FlightType
from game.commander.missionproposals import EscortType
from game.commander.tasks.packageplanningtask import PackagePlanningTask
from game.commander.theaterstate import TheaterState
from game.ground_forces.ai_ground_planner import reserve_armor_for
from game.theater.theatergroundobject import MotorpoolGroundObject


@dataclass
class PlanMotorpoolAttack(PackagePlanningTask[MotorpoolGroundObject]):
    """Plans a strike or BAI package (with escorts) against an enemy motorpool
    depot, destroying parked reserve armor so the owner must repurchase it.

    The motorpool's groups are populated ephemerally at mission generation *after*
    planning (see MotorpoolPopulator), so flight sizing is derived from the live
    reserve pool (``reserve_armor_for``) rather than the stale ``alive_unit_count``.
    """

    #: BAI is the doctrinal primary (parked ground forces, not in contact); STRIKE
    #: is the fallback so the package can still form when no BAI-capable aircraft
    #: are available. Both match what the manual planner offers for a motorpool.
    task: FlightType

    def preconditions_met(self, state: TheaterState) -> bool:
        if self.target not in state.motorpool_targets:
            return False
        if not self.target_area_preconditions_met(state):
            return False
        return super().preconditions_met(state)

    def apply_effects(self, state: TheaterState) -> None:
        state.motorpool_targets.remove(self.target)
        super().apply_effects(state)

    def propose_flights(self) -> None:
        target_count = self._rendered_unit_count()
        if self.task is FlightType.BAI:
            self.propose_flight(FlightType.BAI, min(4, (target_count // 4) + 1))
        else:
            self.propose_flight(
                FlightType.STRIKE,
                min(4, (target_count // 2) + target_count % 2),
            )
            if (
                self.target.control_point.coalition.game.settings.autoplan_tankers_for_strike
            ):
                self.propose_flight(FlightType.REFUELING, 1, EscortType.Refuel)
        self.propose_common_escorts()

    def _rendered_unit_count(self) -> int:
        """How many vehicles this motorpool will render this turn (0 when nothing
        will spawn, so the planner proposes no attack flight)."""
        settings = self.target.control_point.coalition.game.settings
        cap = settings.motorpool_spawn_cap
        if cap <= 0 or not settings.motorpool_enabled:
            return 0
        reserve = reserve_armor_for(self.target.control_point)
        return min(cap, sum(reserve.values()))
