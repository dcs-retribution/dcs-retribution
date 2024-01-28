from dcs.point import MovingPoint, PointAction

from game.theater import NavalControlPoint
from .pydcswaypointbuilder import PydcsWaypointBuilder


class LandingPointBuilder(PydcsWaypointBuilder):
    def build(self) -> MovingPoint:
        waypoint = super().build()
        if self.ai_despawn(waypoint):
            waypoint.alt = round(
                self.flight.coalition.doctrine.max_patrol_altitude.meters
            )
            waypoint.alt_type = "BARO"
        else:
            waypoint.type = "Land"
            waypoint.action = PointAction.Landing
            if (control_point := self.waypoint.control_point) is not None:
                if isinstance(control_point, NavalControlPoint):
                    waypoint.helipad_id = control_point.airdrome_id_for_landing  # type: ignore
                    waypoint.link_unit = control_point.airdrome_id_for_landing  # type: ignore
                else:
                    waypoint.airdrome_id = control_point.airdrome_id_for_landing
        return waypoint
