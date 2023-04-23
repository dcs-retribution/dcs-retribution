import logging
import math

from dcs.point import MovingPoint
from dcs.task import AttackGroup, OptECMUsing, WeaponType, Expend

from game.theater import TheaterGroundObject
from .pydcswaypointbuilder import PydcsWaypointBuilder


class DeadIngressBuilder(PydcsWaypointBuilder):
    def add_tasks(self, waypoint: MovingPoint) -> None:
        self.register_special_waypoints(self.waypoint.targets)

        target = self.package.target
        if not isinstance(target, TheaterGroundObject):
            logging.error(
                "Unexpected target type for DEAD mission: %s",
                target.__class__.__name__,
            )
            return

        # Preemptively use ECM to better avoid getting swatted.
        ecm_option = OptECMUsing(value=OptECMUsing.Values.UseIfDetectedLockByRadar)
        waypoint.tasks.append(ecm_option)

        for group in target.groups:
            miz_group = self.mission.find_group(group.group_name)
            if miz_group is None:
                logging.error(
                    f"Could not find group for DEAD mission {group.group_name}"
                )
                continue

            task = AttackGroup(
                miz_group.id,
                weapon_type=WeaponType.Guided,
                altitude=waypoint.alt,
            )
            waypoint.tasks.append(task)

            dir = target.position.heading_between_point(waypoint.position)

            task = AttackGroup(
                miz_group.id,
                weapon_type=WeaponType.Unguided,
                expend=Expend.All,
                direction=math.radians(dir),
                altitude=waypoint.alt,
            )
            task.params["altitudeEnabled"] = False
            waypoint.tasks.append(task)
