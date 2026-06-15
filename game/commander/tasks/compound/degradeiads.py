from collections.abc import Iterator
from typing import Union

from game.ato.flighttype import FlightType
from game.commander.tasks.primitive.antiship import PlanAntiShip
from game.commander.tasks.primitive.dead import PlanDead
from game.commander.theaterstate import TheaterState
from game.data.groups import GroupTask
from game.htn import CompoundTask, Method
from game.theater.theatergroundobject import IadsGroundObject, NavalGroundObject


class DegradeIads(CompoundTask[TheaterState]):
    def _in_area_of_operations(
        self, state: TheaterState, target: IadsGroundObject | NavalGroundObject
    ) -> bool:
        if isinstance(target, IadsGroundObject):
            task = FlightType.DEAD
        else:
            task = FlightType.ANTISHIP
        if not state.context.settings.is_aoo_task_enabled(task):
            return True
        return state.context.coalition.is_in_area_of_operations(target.position)

    def each_valid_method(self, state: TheaterState) -> Iterator[Method[TheaterState]]:
        for air_defense in state.threatening_air_defenses:
            if not self._in_area_of_operations(state, air_defense):
                continue
            yield [self.plan_against(air_defense)]

        prioritized_air_defenses = sorted(
            [
                tgo
                for tgo in state.enemy_air_defenses
                if tgo.task in [GroupTask.LORAD, GroupTask.MERAD]
            ],
            key=lambda x: (state.priority_cp.distance_to(x) if state.priority_cp else 0)
            - x.max_threat_range().meters,
        )

        for air_defense in prioritized_air_defenses:
            if not self._in_area_of_operations(state, air_defense):
                continue
            yield [self.plan_against(air_defense)]
        for detector in state.detecting_air_defenses:
            if not self._in_area_of_operations(state, detector):
                continue
            yield [self.plan_against(detector)]

    @staticmethod
    def plan_against(
        target: Union[IadsGroundObject, NavalGroundObject],
    ) -> Union[PlanDead, PlanAntiShip]:
        if isinstance(target, IadsGroundObject):
            return PlanDead(target)
        return PlanAntiShip(target)
