from collections.abc import Iterator

from game.commander.tasks.primitive.armedrecon import PlanArmedRecon
from game.commander.tasks.primitive.bai import PlanBai
from game.commander.theaterstate import TheaterState
from game.htn import CompoundTask, Method


class AttackBattlePositions(CompoundTask[TheaterState]):
    def each_valid_method(self, state: TheaterState) -> Iterator[Method[TheaterState]]:
        for battle_positions in state.enemy_battle_positions.values():
            for battle_position in battle_positions.in_priority_order:
                yield [PlanBai(battle_position)]
        # Only plan against the 2 most important CPs
        for cp in state.control_point_priority_queue[:2]:
            yield [PlanArmedRecon(cp)]
