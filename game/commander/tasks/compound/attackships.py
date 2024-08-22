from collections.abc import Iterator

from game.commander.tasks.primitive.antiship import PlanAntiShip
from game.commander.theaterstate import TheaterState
from game.htn import CompoundTask, Method


class AttackShips(CompoundTask[TheaterState]):
    def each_valid_method(self, state: TheaterState) -> Iterator[Method[TheaterState]]:
        for ship in state.enemy_ships:
            # Ammo depots are targeted based on the needs of the front line by
            # ReduceEnemyFrontLineCapacity. No reason to target them before that front
            # line is active.
            if ship.has_live_radar_sam:
                yield [PlanAntiShip(ship)]
