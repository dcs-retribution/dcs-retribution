from dcs.point import MovingPoint
from dcs.task import RefuelingTaskAction, ControlledTask

from game.theater import OffMapSpawn
from .pydcswaypointbuilder import PydcsWaypointBuilder


class RefuelPointBuilder(PydcsWaypointBuilder):
    def add_tasks(self, waypoint: MovingPoint) -> None:
        offmap = isinstance(self.flight.arrival, OffMapSpawn)
        if self.flight.divert:
            offmap |= isinstance(self.flight.divert, OffMapSpawn)
        if not offmap:
            refuel = ControlledTask(RefuelingTaskAction())
            refuel.start_probability(10)
            waypoint.add_task(refuel)
        return super().add_tasks(waypoint)
