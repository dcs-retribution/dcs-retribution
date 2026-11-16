from collections.abc import Iterator

from game.ato.flighttype import FlightType
from game.commander.tasks.primitive.motorpool import PlanMotorpoolAttack
from game.commander.theaterstate import TheaterState
from game.htn import CompoundTask, Method


class AttackMotorpools(CompoundTask[TheaterState]):
    def each_valid_method(self, state: TheaterState) -> Iterator[Method[TheaterState]]:
        for motorpool in state.motorpool_targets:
            # BAI is preferred (parked ground forces); STRIKE is the fallback so a
            # package can still form when no BAI-capable aircraft are available.
            # Applying either effect removes the target from motorpool_targets, so at
            # most one package is planned against a given motorpool per turn.
            yield [PlanMotorpoolAttack(motorpool, FlightType.BAI)]
            yield [PlanMotorpoolAttack(motorpool, FlightType.STRIKE)]
