from collections.abc import Iterator

from game.commander.tasks.primitive.recovery import PlanRecovery
from game.commander.theaterstate import TheaterState
from game.htn import CompoundTask, Method


class RecoverySupport(CompoundTask[TheaterState]):
    def each_valid_method(self, state: TheaterState) -> Iterator[Method[TheaterState]]:
        yield [PlanRecoverySupport()]


class PlanRecoverySupport(CompoundTask[TheaterState]):
    def each_valid_method(self, state: TheaterState) -> Iterator[Method[TheaterState]]:
        for target in state.recovery_targets:
            yield [PlanRecovery(target)]
