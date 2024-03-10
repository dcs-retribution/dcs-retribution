import copy
from typing import Union

from dcs import Point
from dcs.planes import B_17G, B_52H, Tu_22M3, B_1B, F_15ESE
from dcs.point import MovingPoint
from dcs.task import Bombing, Expend, OptFormation, WeaponType, CarpetBombing

from game.utils import mach, meters
from .pydcswaypointbuilder import PydcsWaypointBuilder


class StrikeIngressBuilder(PydcsWaypointBuilder):
    _special_wpts_injected: bool = False

    def add_tasks(self, waypoint: MovingPoint) -> None:
        bomber = self.group.units[0].unit_type in [B_17G, Tu_22M3]
        bomber_guided = self.group.units[0].unit_type in [B_1B, B_52H]
        if bomber_guided or not bomber:
            waypoint.tasks.append(OptFormation.finger_four_open())
            self.add_strike_tasks(waypoint, WeaponType.ASM)
            waypoint.tasks.append(OptFormation.trail_open())
            self.add_strike_tasks(waypoint, WeaponType.GuidedBombs)

        waypoint.tasks.append(OptFormation.ww2_bomber_element_close())
        self.add_bombing_tasks(waypoint)
        waypoint.tasks.append(OptFormation.finger_four_open())
        self.register_special_ingress_points()

    def add_bombing_tasks(self, waypoint: MovingPoint) -> None:
        targets = self.waypoint.targets
        if not targets:
            return

        center: Point = copy.copy(targets[0].position)
        for target in targets[1:]:
            center += target.position
        center /= len(targets)
        avg_spacing = 0.0
        for t in targets:
            avg_spacing += center.distance_to_point(t.position)
        avg_spacing /= len(targets)
        bombing: Union[CarpetBombing, Bombing]
        if self.group.task == "Ground Attack":
            bombing = CarpetBombing(
                center,
                weapon_type=WeaponType.Bombs,
                expend=Expend.All,
                carpet_length=avg_spacing,
                altitude=waypoint.alt,
            )
        else:
            bombing = Bombing(
                center,
                weapon_type=WeaponType.Bombs,
                expend=Expend.All,
                group_attack=True,
                altitude=waypoint.alt,
            )
        waypoint.tasks.append(bombing)

    def add_strike_tasks(
        self, waypoint: MovingPoint, weapon_type: WeaponType = WeaponType.Auto
    ) -> None:
        for target in self.waypoint.targets:
            bombing = Bombing(target.position, weapon_type=weapon_type)
            # If there is only one target, drop all ordnance in one pass.
            if len(self.waypoint.targets) == 1:
                bombing.params["expend"] = Expend.All.value
            elif target.is_static:
                bombing.params["expend"] = Expend.Half.value
            waypoint.tasks.append(bombing)

            waypoint.speed = mach(0.85, meters(waypoint.alt)).meters_per_second

        # Register special waypoints
        if not self._special_wpts_injected:
            self.register_special_strike_points(self.waypoint.targets)
            if self.flight.unit_type.dcs_unit_type == F_15ESE:
                self.register_special_strike_points(self.flight.custom_targets, 2)
            self._special_wpts_injected = True
