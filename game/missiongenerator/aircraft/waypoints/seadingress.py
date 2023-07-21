import logging

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
        self.register_special_waypoints(self.waypoint.targets)

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

            if self.flight.any_member_has_weapon_of_type(WeaponType.ARM):
                # Special handling for ARM Weapon types:
                # The SEAD flight will Search for the targeted group and then engage it
                # if it is found only. This will prevent AI from having huge problems
                # when skynet is enabled and the Radar is not emitting. They dive
                # into the SAM instead of waiting for it to come alive
                engage_task = EngageGroup(miz_group.id)
                engage_task.params["weaponType"] = DcsWeaponType.ARM.value
                waypoint.tasks.append(engage_task)

            # Use other Air-to-Surface Missiles at last
            attack_task = AttackGroup(
                miz_group.id,
                weapon_type=DcsWeaponType.ASM,
                altitude=waypoint.alt,  # flight loses alt with AB restriction
            )
            waypoint.tasks.append(attack_task)

        burn_free = OptRestrictAfterburner(False)
        waypoint.tasks.append(burn_free)
