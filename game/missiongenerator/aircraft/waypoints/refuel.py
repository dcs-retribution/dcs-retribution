from dcs.point import MovingPoint
from dcs.task import RefuelingTaskAction, ControlledTask

from .pydcswaypointbuilder import PydcsWaypointBuilder


class RefuelPointBuilder(PydcsWaypointBuilder):
    def add_tasks(self, waypoint: MovingPoint) -> None:
        if not self.ai_despawn(waypoint, True):
            refuel = ControlledTask(RefuelingTaskAction())
            refuel.start_if_lua_predicate(self._get_lua_predicate(0.2))
            refuel.stop_if_lua_predicate(self._get_lua_predicate(0.5))
            waypoint.add_task(refuel)
        return super().add_tasks(waypoint)

    def _get_lua_predicate(self, fuel_level: float) -> str:
        return f"""
            local okfuel = true
            for i, unitObject in pairs(Group.getByName('{self.group.name}'):getUnits()) do
                --trigger.action.outText(tostring(Unit.getFuel(unitObject)), 15)
                if Unit.getFuel(unitObject) < {fuel_level} then okfuel = false; break end
            end
            return lowfuel
            """
