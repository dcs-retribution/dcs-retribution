import logging

from dcs.point import MovingPoint
from dcs.task import AttackGroup, OptFormation, WeaponType

from game.theater import TheaterGroundObject
from game.transfers import MultiGroupTransport
from .pydcswaypointbuilder import PydcsWaypointBuilder


class BaiIngressBuilder(PydcsWaypointBuilder):
    def add_tasks(self, waypoint: MovingPoint) -> None:
        self.register_special_ingress_points()
        if not self.flight.is_helo:
            waypoint.tasks.append(OptFormation.trail_open())
        # Motorpool targets flow through the same path as any other TGO: one
        # AttackGroup task per group. The populator renders a motorpool as one
        # group per unit type ("{tgo.name} ({unit_type})"), so motorpool BAI
        # engages each armor group individually — the same shape as non-motorpool
        # BAI — rather than a single zone task (mission spec).
        target = self.package.target

        # TODO: Add common "UnitGroupTarget" base type.
        group_names = []
        if isinstance(target, TheaterGroundObject):
            for group in target.groups:
                group_names.append(group.group_name)
        elif isinstance(target, MultiGroupTransport):
            group_names.append(target.name)
        else:
            logging.error(
                "Unexpected target type for BAI mission: %s",
                target.__class__.__name__,
            )
            return

        for group_name in group_names:
            miz_group = self.mission.find_group(group_name)
            if miz_group is None:
                logging.error("Could not find group for BAI mission %s", group_name)
                continue

            task = AttackGroup(miz_group.id, weapon_type=WeaponType.Auto)
            waypoint.tasks.append(task)
