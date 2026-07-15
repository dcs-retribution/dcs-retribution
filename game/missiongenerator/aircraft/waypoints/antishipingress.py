import logging
from typing import List

from dcs.point import MovingPoint
from dcs.task import AttackGroup, Expend, OptFormation, WeaponType

from game.theater import NavalControlPoint, TheaterGroundObject
from .pydcswaypointbuilder import PydcsWaypointBuilder


class AntiShipIngressBuilder(PydcsWaypointBuilder):
    def add_tasks(self, waypoint: MovingPoint) -> None:
        self.register_special_ingress_points()
        group_names = []
        waypoint.tasks.append(OptFormation.finger_four_open())

        target = self.package.target
        if isinstance(target, NavalControlPoint):
            # Use find_main_tgo() like the flight plan does: ground_objects[0]
            # isn't necessarily the carrier (it may be a sunk, never-spawned
            # group), which would leave the flight with no AttackGroup target.
            carrier_tgo = target.find_main_tgo()
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

        added = 0
        for ordnance in (
            WeaponType.Antiship,
            WeaponType.Guided,
            WeaponType.Unguided,
        ):
            added += self.add_attack_group_tasks_for_ordnance(
                waypoint, group_names, ordnance
            )

        if not added:
            # No AttackGroup task could be attached, so the AI would fly to the
            # ingress point and turn back without engaging. Make this loud: it
            # almost always means the target group(s) were never spawned (e.g.
            # already destroyed) or the resolved name does not match a mission
            # group.
            logging.warning(
                "Anti-Ship flight %s has no attackable target group "
                "(resolved %s); it will not engage anything.",
                self.flight,
                group_names or "no groups",
            )

    def add_attack_group_tasks_for_ordnance(
        self,
        waypoint: MovingPoint,
        group_names: List[str],
        ordnance: WeaponType,
    ) -> int:
        added = 0
        for group_name in group_names:
            miz_group = self.mission.find_group(group_name)
            if miz_group is None:
                logging.error(
                    "Could not find group for Anti-Ship mission %s", group_name
                )
                continue

            # expend=All so the AI empties its anti-ship load on the target instead of
            # DCS's default Auto salvo (which fires ~2 and RTBs with the rest). Matches
            # what DEAD does. weapon_type scopes it to the anti-ship ordnance only.
            task = AttackGroup(
                miz_group.id,
                group_attack=True,
                weapon_type=ordnance,
                expend=Expend.All,
            )
            waypoint.tasks.append(task)
            added += 1
        return added
