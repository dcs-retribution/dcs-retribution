from dcs.point import MovingPoint
from dcs.task import Expend, WeaponType, CarpetBombing

from game.ato.flightplans.airassault import AirAssaultLayout
from game.utils import feet, knots
from pydcs_extensions.hercules.hercules import Hercules
from .pydcswaypointbuilder import PydcsWaypointBuilder


class AirAssaultIngressBuilder(PydcsWaypointBuilder):
    def add_tasks(self, waypoint: MovingPoint) -> None:
        self.register_special_ingress_points()
        air_drop = self.group.units[0].unit_type in [Hercules]
        if air_drop:
            waypoint.speed = knots(200).meters_per_second
            waypoint.speed_locked = True
            waypoint.ETA_locked = False
            tgt = self.flight.package.target.position
            layout = self.flight.flight_plan.layout
            assert isinstance(layout, AirAssaultLayout)
            heading = layout.ingress.position.heading_between_point(tgt)
            tgt = tgt.point_from_heading(heading, feet(6000).meters)
            bombing = CarpetBombing(
                tgt,
                weapon_type=WeaponType.Bombs,
                expend=Expend.All,
                carpet_length=feet(9000).meters,
            )
            waypoint.add_task(bombing)
