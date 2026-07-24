from collections.abc import Iterator

from game.commander.tasks.primitive.csar import PlanCsar
from game.commander.theaterstate import TheaterState
from game.htn import CompoundTask, Method


class RescueDownedPilots(CompoundTask[TheaterState]):
    def each_valid_method(self, state: TheaterState) -> Iterator[Method[TheaterState]]:
        yield [PlanRescueDownedPilots()]


class PlanRescueDownedPilots(CompoundTask[TheaterState]):
    def each_valid_method(self, state: TheaterState) -> Iterator[Method[TheaterState]]:
        for target in state.csar_targets:
            yield [PlanCsar(target)]
