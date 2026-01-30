from __future__ import annotations

import logging
import random
from enum import Enum
from typing import List, TYPE_CHECKING
from uuid import UUID

from game.data.units import UnitClass
from game.dcs.groundunittype import GroundUnitType
from .combat_stance import CombatStance

if TYPE_CHECKING:
    from game import Game
    from game.theater import ControlPoint
    from game.groundunitorders import TemplateOrder

MAX_COMBAT_GROUP_PER_CP = 10


class CombatGroupRole(Enum):
    TANK = 1
    APC = 2
    IFV = 3
    ARTILLERY = 4
    SHORAD = 5
    LOGI = 6
    INFANTRY = 7
    ATGM = 8
    RECON = 9


DISTANCE_FROM_FRONTLINE = {
    CombatGroupRole.TANK: (2200, 3200),
    CombatGroupRole.APC: (2700, 3700),
    CombatGroupRole.IFV: (2700, 3700),
    CombatGroupRole.ARTILLERY: (16000, 18000),
    CombatGroupRole.SHORAD: (5000, 8000),
    CombatGroupRole.LOGI: (18000, 20000),
    CombatGroupRole.INFANTRY: (2800, 3300),
    CombatGroupRole.ATGM: (5200, 6200),
    CombatGroupRole.RECON: (2000, 3000),
}

GROUP_SIZES_BY_COMBAT_STANCE = {
    CombatStance.DEFENSIVE: [2, 4, 6],
    CombatStance.AGGRESSIVE: [2, 4, 6],
    CombatStance.RETREAT: [2, 4, 6, 8],
    CombatStance.BREAKTHROUGH: [4, 6, 6, 8],
    CombatStance.ELIMINATION: [2, 4, 4, 4, 6],
    CombatStance.AMBUSH: [1, 1, 2, 2, 2, 2, 4],
}


class CombatGroup:
    def __init__(
        self, role: CombatGroupRole, unit_type: GroundUnitType, size: int
    ) -> None:
        self.unit_type = unit_type
        self.size = size
        self.role = role
        self.start_position = None

    def __str__(self) -> str:
        s = f"ROLE : {self.role}\n"
        if self.size:
            s += f"UNITS {self.unit_type} * {self.size}"
        return s


class GroundPlanner:
    def __init__(self, cp: ControlPoint, game: Game) -> None:
        self.cp = cp
        self.game = game
        self.connected_enemy_cp = [
            cp for cp in self.cp.connected_points if cp.captured != self.cp.captured
        ]
        self.tank_groups: List[CombatGroup] = []
        self.apc_group: List[CombatGroup] = []
        self.ifv_group: List[CombatGroup] = []
        self.art_group: List[CombatGroup] = []
        self.atgm_group: List[CombatGroup] = []
        self.logi_groups: List[CombatGroup] = []
        self.shorad_groups: List[CombatGroup] = []
        self.recon_groups: List[CombatGroup] = []

        self.units_per_cp: dict[UUID, List[CombatGroup]] = {}
        for cp in self.connected_enemy_cp:
            self.units_per_cp[cp.id] = []
        self.reserve: List[CombatGroup] = []

    def plan_groundwar(self) -> None:
        ground_unit_limit = self.cp.frontline_unit_count_limit

        remaining_available_frontline_units = ground_unit_limit
        # Now applies the ratio between ground unit limit and the total number of ground units to each unit type
        # when planning the ground war. This will help with monocultures of certain unit types when the control
        # point has more units than can be spawned in one mission. In short, this will make more unit types to spawn.
        if self.cp.base.total_armor > 0:
            ratio_of_frontline_units_to_reserves = min(
                ground_unit_limit / self.cp.base.total_armor, 1
            )
        else:
            ratio_of_frontline_units_to_reserves = 1

        # ===== PHASE 1: Process Template Orders =====
        # Try to form groups from complete template orders first
        template_orders_to_remove: list[TemplateOrder] = []

        for template_order in self.cp.ground_unit_orders.template_orders:
            if not self.has_units_available(template_order.units):
                continue

            total_units = sum(template_order.units.values())
            if total_units > remaining_available_frontline_units:
                continue

            self.create_template_based_groups(template_order)
            self.consume_units(template_order.units)
            template_orders_to_remove.append(template_order)
            remaining_available_frontline_units -= total_units

        for template_order in template_orders_to_remove:
            self.cp.ground_unit_orders.consume_template_order(template_order)

        # ===== PHASE 2: Process Remaining Units (Existing Logic) =====
        # Create combat groups and assign them randomly to each enemy CP
        for unit_type in list(self.cp.base.armor.keys()):
            unit_class = unit_type.unit_class
            if unit_class is UnitClass.TANK:
                collection = self.tank_groups
                role = CombatGroupRole.TANK
            elif unit_class is UnitClass.APC:
                collection = self.apc_group
                role = CombatGroupRole.APC
            elif unit_class is UnitClass.ARTILLERY:
                collection = self.art_group
                role = CombatGroupRole.ARTILLERY
            elif unit_class is UnitClass.IFV:
                collection = self.ifv_group
                role = CombatGroupRole.IFV
            elif unit_class is UnitClass.LOGISTICS:
                collection = self.logi_groups
                role = CombatGroupRole.LOGI
            elif unit_class is UnitClass.ATGM:
                collection = self.atgm_group
                role = CombatGroupRole.ATGM
            elif unit_class in [UnitClass.SHORAD, UnitClass.AAA]:
                collection = self.shorad_groups
                role = CombatGroupRole.SHORAD
            elif unit_class is UnitClass.RECON:
                collection = self.recon_groups
                role = CombatGroupRole.RECON
            else:
                logging.warning(
                    f"Unused front line vehicle at base {unit_type}: unknown unit class"
                )
                continue

            available = (
                self.cp.base.armor[unit_type] * ratio_of_frontline_units_to_reserves
            )
            if 0 < available < 1:
                available = 1

            # Round the number of units to an integer
            if available > remaining_available_frontline_units:
                available = remaining_available_frontline_units
            available = round(available)

            remaining_available_frontline_units -= available

            while available > 0:
                if len(self.connected_enemy_cp) > 0:
                    enemy_cp: ControlPoint = random.choice(self.connected_enemy_cp)
                    frontline_stance = self.cp.stances.get(enemy_cp.id)
                    if not frontline_stance:
                        logging.warning(
                            f"{self.cp.name} lost its frontline stance for {enemy_cp.name}"
                        )
                        frontline_stance = CombatStance.DEFENSIVE
                    group_size_choice = GROUP_SIZES_BY_COMBAT_STANCE[frontline_stance]
                    if role == CombatGroupRole.SHORAD:
                        count = 1
                    else:
                        choices = [s for s in group_size_choice if s <= available]
                        if not choices:
                            choices.append(1)
                        count = random.choice(choices)

                    available -= count
                    group = CombatGroup(role, unit_type, count)
                    self.units_per_cp[enemy_cp.id].append(group)
                else:
                    group = CombatGroup(role, unit_type, available)
                    self.reserve.append(group)
                    available = 0  # All units allocated to reserves
                collection.append(group)

            if remaining_available_frontline_units == 0:
                break

    def has_units_available(self, required_units: dict[GroundUnitType, int]) -> bool:
        """Check if all required units are available in base armor."""
        for unit_type, count in required_units.items():
            available = self.cp.base.armor.get(unit_type, 0)
            if available < count:
                return False
        return True

    def consume_units(self, units: dict[GroundUnitType, int]) -> None:
        """Remove units from base armor inventory."""
        for unit_type, count in units.items():
            available = self.cp.base.armor.get(unit_type, 0)
            if available < count:
                logging.warning(
                    f"Attempting to consume {count} {unit_type} but only "
                    f"{available} available at {self.cp.name}"
                )
            self.cp.base.armor[unit_type] -= count
            if self.cp.base.armor[unit_type] <= 0:
                del self.cp.base.armor[unit_type]

    def unit_class_to_role(self, unit_class: UnitClass) -> CombatGroupRole:
        """Map unit class to combat group role."""
        mapping = {
            UnitClass.TANK: CombatGroupRole.TANK,
            UnitClass.APC: CombatGroupRole.APC,
            UnitClass.IFV: CombatGroupRole.IFV,
            UnitClass.ARTILLERY: CombatGroupRole.ARTILLERY,
            UnitClass.ATGM: CombatGroupRole.ATGM,
            UnitClass.LOGISTICS: CombatGroupRole.LOGI,
            UnitClass.SHORAD: CombatGroupRole.SHORAD,
            UnitClass.AAA: CombatGroupRole.SHORAD,
            UnitClass.RECON: CombatGroupRole.RECON,
        }
        return mapping.get(unit_class, CombatGroupRole.TANK)

    def add_group_to_collection(
        self, group: CombatGroup, role: CombatGroupRole
    ) -> None:
        collections = {
            CombatGroupRole.TANK: self.tank_groups,
            CombatGroupRole.APC: self.apc_group,
            CombatGroupRole.IFV: self.ifv_group,
            CombatGroupRole.ARTILLERY: self.art_group,
            CombatGroupRole.ATGM: self.atgm_group,
            CombatGroupRole.LOGI: self.logi_groups,
            CombatGroupRole.SHORAD: self.shorad_groups,
            CombatGroupRole.RECON: self.recon_groups,
        }
        collection = collections.get(role, self.tank_groups)
        collection.append(group)

    def create_template_based_groups(self, template_order) -> None:
        from game.ground_forces.frontline_group_loader import FrontlineGroupLoader

        loader = FrontlineGroupLoader()
        loader.initialize()

        try:
            template = loader.by_name(template_order.template_name)
        except KeyError:
            logging.warning(
                f"Template '{template_order.template_name}' not found, "
                f"falling back to random grouping"
            )
            return

        if self.connected_enemy_cp:
            enemy_cp = random.choice(self.connected_enemy_cp)
        else:
            # No connected enemies, add to reserves
            for unit_type, count in template_order.units.items():
                if count <= 0:
                    continue
                role = self.unit_class_to_role(unit_type.unit_class)
                group = CombatGroup(role, unit_type, count)
                self.reserve.append(group)
            return

        for unit_type, count in template_order.units.items():
            if count <= 0:
                continue

            role = self.unit_class_to_role(unit_type.unit_class)
            group = CombatGroup(role, unit_type, count)

            self.add_group_to_collection(group, role)
            self.units_per_cp[enemy_cp.id].append(group)

        logging.info(
            f"Formed template group '{template_order.template_name}' at {self.cp.name}"
        )
