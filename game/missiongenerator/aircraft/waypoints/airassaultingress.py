from dcs.point import MovingPoint
from dcs.task import Expend, WeaponType, CarpetBombing, OptROE

from game.ato.flightwaypointtype import FlightWaypointType
from game.utils import feet, knots
from pydcs_extensions.hercules.hercules import Hercules
from .pydcswaypointbuilder import PydcsWaypointBuilder


class AirAssaultIngressBuilder(PydcsWaypointBuilder):
    def add_tasks(self, waypoint: MovingPoint) -> None:
        self.register_special_ingress_points()
        air_drop = self.group.units[0].unit_type in [Hercules]
        if air_drop:
            waypoint.speed = knots(230).meters_per_second
            waypoint.speed_locked = True
            waypoint.ETA_locked = False
            tgt = self.flight.flight_plan.package.target.position
            for wpt in self.flight.flight_plan.waypoints:
                if wpt.waypoint_type == FlightWaypointType.TARGET_GROUP_LOC:
                    tgt = wpt.position
                    break
            bombing = CarpetBombing(
                tgt,
                weapon_type=WeaponType.Bombs,
                expend=Expend.All,
                carpet_length=feet(9000).meters,
            )
            waypoint.add_task(bombing)
