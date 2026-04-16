import logging
import math

from dcs.point import MovingPoint
from dcs.task import (
    AttackGroup,
    EngageGroup,
    Expend,
    OptECMUsing,
    WeaponType as DcsWeaponType,
    OptRestrictAfterburner,
)

from game.data.weapons import WeaponType
from game.theater import TheaterGroundObject
from .pydcswaypointbuilder import PydcsWaypointBuilder


class SeadIngressBuilder(PydcsWaypointBuilder):
    def add_tasks(self, waypoint: MovingPoint) -> None:
        self.register_special_strike_points(self.waypoint.targets)
        self.register_special_ingress_points()

        target = self.package.target
        if not isinstance(target, TheaterGroundObject):
            logging.error(
                "Unexpected target type for SEAD mission: %s",
                target.__class__.__name__,
            )
            return

        # Preemptively use ECM to better avoid getting swatted.
        ecm_option = OptECMUsing(value=OptECMUsing.Values.UseIfDetectedLockByRadar)
        waypoint.tasks.append(ecm_option)

        # Avoid having AI burn all of its fuel while loitering until next weapon release
        burn_restrict = OptRestrictAfterburner(True)
        waypoint.tasks.append(burn_restrict)

        for group in target.groups:
            miz_group = self.mission.find_group(group.group_name)
            if miz_group is None:
                logging.error(
                    f"Could not find group for SEAD mission {group.group_name}"
                )
                continue

            # Use decoys first
            attack_task = AttackGroup(
                miz_group.id,
                weapon_type=DcsWeaponType.Decoy,
                group_attack=True,
                expend=Expend.All,
                altitude=round(waypoint.alt * 1.5),  # 50% increase to force a climb
            )
            waypoint.tasks.append(attack_task)

            attack_task = AttackGroup(
                miz_group.id,
                weapon_type=DcsWeaponType.ARM,
                expend=Expend.All,
                altitude=waypoint.alt,
                group_attack=True,
            )
            waypoint.tasks.append(attack_task)

            attack_task = AttackGroup(
                miz_group.id,
                weapon_type=DcsWeaponType.ASM,
                expend=Expend.All,
                altitude=waypoint.alt,
                group_attack=True,
            )
            waypoint.tasks.append(attack_task)

            attack_task = AttackGroup(
                miz_group.id,
                weapon_type=DcsWeaponType.GuidedBombs,
                expend=Expend.All,
                altitude=waypoint.alt,
                group_attack=True,
            )
            waypoint.tasks.append(attack_task)

            dir = target.position.heading_between_point(waypoint.position)

            attack_task = AttackGroup(
                miz_group.id,
                weapon_type=DcsWeaponType.Unguided,
                attack_limit=1,
                expend=Expend.All,
                direction=math.radians(dir),
                altitude=waypoint.alt,
            )
            waypoint.tasks.append(attack_task)

        burn_free = OptRestrictAfterburner(False)
        waypoint.tasks.append(burn_free)
