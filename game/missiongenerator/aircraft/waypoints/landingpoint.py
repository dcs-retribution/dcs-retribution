from dcs.point import MovingPoint, PointAction

from game.theater import NavalControlPoint
from .pydcswaypointbuilder import PydcsWaypointBuilder


class LandingPointBuilder(PydcsWaypointBuilder):
    def build(self) -> MovingPoint:
        waypoint = super().build()
        waypoint.type = "Land"
        waypoint.action = PointAction.Landing
        if (control_point := self.waypoint.control_point) is not None:
            if isinstance(control_point, NavalControlPoint):
                waypoint.helipad_id = control_point.airdrome_id_for_landing
                waypoint.link_unit = control_point.airdrome_id_for_landing
            else:
                waypoint.airdrome_id = control_point.airdrome_id_for_landing
        return waypoint
