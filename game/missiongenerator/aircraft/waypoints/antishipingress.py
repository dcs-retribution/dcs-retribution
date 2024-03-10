import logging

from dcs.point import MovingPoint
from dcs.task import AttackGroup, OptFormation, WeaponType

from game.theater import NavalControlPoint, TheaterGroundObject
from .pydcswaypointbuilder import PydcsWaypointBuilder


class AntiShipIngressBuilder(PydcsWaypointBuilder):
    def add_tasks(self, waypoint: MovingPoint) -> None:
        self.register_special_ingress_points()
        group_names = []
        waypoint.tasks.append(OptFormation.finger_four_open())

        target = self.package.target
        if isinstance(target, NavalControlPoint):
            carrier_tgo = target.ground_objects[0]
            for g in carrier_tgo.groups:
                group_names.append(g.group_name)
        elif isinstance(target, TheaterGroundObject):
            for group in target.groups:
                group_names.append(group.group_name)
        else:
            logging.error(
                "Unexpected target type for Anti-Ship mission: %s",
                target.__class__.__name__,
            )
            return

        for group_name in group_names:
            miz_group = self.mission.find_group(group_name)
            if miz_group is None:
                logging.error(
                    "Could not find group for Anti-Ship mission %s", group_name
                )
                continue

            task = AttackGroup(
                miz_group.id, group_attack=True, weapon_type=WeaponType.Auto
            )
            waypoint.tasks.append(task)
