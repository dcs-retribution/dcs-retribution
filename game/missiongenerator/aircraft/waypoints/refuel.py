from dcs.point import MovingPoint
from dcs.task import RefuelingTaskAction, ControlledTask

from .pydcswaypointbuilder import PydcsWaypointBuilder


class RefuelPointBuilder(PydcsWaypointBuilder):
    def add_tasks(self, waypoint: MovingPoint) -> None:
        if not self.ai_despawn(waypoint, True):
            refuel = ControlledTask(RefuelingTaskAction())
            refuel.start_probability(10)
            waypoint.add_task(refuel)
        return super().add_tasks(waypoint)
