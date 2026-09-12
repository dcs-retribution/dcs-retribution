from __future__ import annotations

import logging
import math
import random
from dataclasses import dataclass
from typing import Iterator, List, Optional, TYPE_CHECKING, Tuple

from game.config import RUNWAY_REPAIR_COST
from game.data.units import UnitClass
from game.dcs.groundunittype import GroundUnitType
from game.ground_forces.ai_ground_planner import CombatGroupRole
from game.ground_forces.frontline_group_loader import FrontlineGroupLoader
from game.theater import ControlPoint, MissionTarget, ParkingType, Player

if TYPE_CHECKING:
    from game import Game
    from game.ato import FlightType
    from game.factions.faction import Faction
    from game.squadrons import Squadron
    from game.ground_forces.frontline_group_loader import (
        FrontlineGroupTemplate,
    )


@dataclass(frozen=True)
class AircraftProcurementRequest:
    near: MissionTarget
    task_capability: FlightType
    number: int
    heli: bool = False

    def __str__(self) -> str:
        task = self.task_capability.value
        target = self.near.name
        return f"{self.number} ship {task} near {target} (heli={self.heli})"


class ProcurementAi:
    def __init__(
        self,
        game: Game,
        owner: Player,
        faction: Faction,
        manage_runways: bool,
        manage_front_line: bool,
        manage_aircraft: bool,
    ) -> None:
        self.game = game
        self.is_player = owner
        self.air_wing = game.air_wing_for(owner)
        self.faction = faction
        self.manage_runways = manage_runways
        self.manage_front_line = manage_front_line
        self.manage_aircraft = manage_aircraft
        self.threat_zones = self.game.threat_zone_for(self.is_player.opponent)

    def calculate_ground_unit_budget_share(self) -> float:
        armor_investment = 0
        aircraft_investment = 0

        # faction has no ground units
        if (
            len(self.faction.artillery_units) == 0
            and len(self.faction.frontline_units) == 0
        ):
            return 0

        # faction has no planes or no squadrons
        if len(self.faction.all_aircrafts) == 0 or len(self.air_wing.squadrons) == 0:
            return 1

        parking_type = ParkingType(
            fixed_wing=True, fixed_wing_stol=True, rotary_wing=True
        )

        for cp in self.owned_points:
            cp_ground_units = cp.allocated_ground_units(
                self.game.coalition_for(self.is_player).transfers
            )
            armor_investment += cp_ground_units.total_value
            cp_aircraft = cp.allocated_aircraft(parking_type)
            aircraft_investment += cp_aircraft.total_value

        balance = (
            self.game.settings.auto_procurement_balance
            if self.is_player.is_blue
            else self.game.settings.auto_procurement_balance_red
        )
        air = balance / 100.0
        ground = 1 - air
        weighted_investment = aircraft_investment * air + armor_investment * ground
        if weighted_investment == 0:
            # Turn 0 or all units were destroyed.
            return balance / 100.0

        # the more planes we have, the more ground units we want and vice versa
        ground_unit_share = aircraft_investment * air / weighted_investment
        if ground_unit_share > 1.0:
            raise ValueError

        return ground_unit_share

    def spend_budget(self, budget: float) -> float:
        if self.manage_runways:
            budget = self.repair_runways(budget)
        if self.manage_front_line:
            armor_budget = budget * self.calculate_ground_unit_budget_share()
            budget -= armor_budget
            budget += self.reinforce_front_line(armor_budget)

        if self.manage_aircraft:
            budget = self.purchase_aircraft(budget)
        return budget

    def repair_runways(self, budget: float) -> float:
        for control_point in self.owned_points:
            if budget < RUNWAY_REPAIR_COST:
                break
            if control_point.runway_can_be_repaired:
                control_point.begin_runway_repair()
                budget -= RUNWAY_REPAIR_COST
                if self.is_player.is_blue:
                    self.game.message(
                        "We have begun repairing the runway at " f"{control_point}"
                    )
                else:
                    self.game.message(
                        "OPFOR has begun repairing the runway at " f"{control_point}"
                    )
        return budget

    def affordable_ground_unit_of_class(
        self, budget: float, unit_class: UnitClass
    ) -> Optional[GroundUnitType]:
        faction_units = set(self.faction.frontline_units) | set(
            self.faction.artillery_units
        )
        of_class = {u for u in faction_units if u.unit_class is unit_class}

        # faction has no access to needed unit type, take a random unit
        if not of_class:
            of_class = faction_units

        affordable_units = [u for u in of_class if u.price <= budget]
        if not affordable_units:
            return None
        return random.choice(affordable_units)

    def can_fulfill_template(self, template: FrontlineGroupTemplate) -> bool:
        faction_units = set(self.faction.frontline_units) | set(
            self.faction.artillery_units
        )

        for unit_req_list in template.units.values():
            for req in unit_req_list:
                # Check if faction has any unit matching required classes
                has_match = any(u.unit_class in req.unit_classes for u in faction_units)
                if not has_match:
                    return False
        return True

    def plan_template_purchase(
        self, template: FrontlineGroupTemplate, budget: float
    ) -> Optional[tuple[dict[GroundUnitType, int], float]]:
        """
        Plan purchases for a template. Returns (units_dict, total_cost) or None.
        Uses random selection to avoid always buying the same units.

        For each unit requirement in the template:
        - Select a random count within min/max range
        - Randomly select units from faction that match required unit classes
        - Track total cost and ensure it stays within budget
        """
        units_to_buy: dict[GroundUnitType, int] = {}
        total_cost = 0.0

        # Get available faction units
        faction_units = set(self.faction.frontline_units) | set(
            self.faction.artillery_units
        )

        # Process each unit requirement in the template
        for unit_req_list in template.units.values():
            for req in unit_req_list:
                # Random count within template's specified range
                count = random.randint(req.min_count, req.max_count)

                # Find faction units matching required classes
                matching_units = [
                    u for u in faction_units if u.unit_class in req.unit_classes
                ]

                if not matching_units:
                    # Faction doesn't have units for this requirement
                    return None

                # Randomly select units to fill requirement
                for _ in range(count):
                    # Filter to affordable units
                    affordable = [
                        u for u in matching_units if u.price <= (budget - total_cost)
                    ]

                    if not affordable:
                        # Can't afford to complete this template
                        return None

                    # Random selection from affordable options
                    unit = random.choice(affordable)
                    units_to_buy[unit] = units_to_buy.get(unit, 0) + 1
                    total_cost += unit.price

        return units_to_buy, total_cost

    def role_to_unit_class(self, role: CombatGroupRole) -> UnitClass:
        mapping = {
            CombatGroupRole.TANK: UnitClass.TANK,
            CombatGroupRole.APC: UnitClass.APC,
            CombatGroupRole.IFV: UnitClass.IFV,
            CombatGroupRole.ARTILLERY: UnitClass.ARTILLERY,
            CombatGroupRole.ATGM: UnitClass.ATGM,
            CombatGroupRole.SHORAD: UnitClass.SHORAD,
            CombatGroupRole.RECON: UnitClass.RECON,
            CombatGroupRole.LOGI: UnitClass.LOGISTICS,
            CombatGroupRole.INFANTRY: UnitClass.INFANTRY,
        }
        return mapping.get(role, UnitClass.TANK)

    def select_template_for_purchase(
        self, cp: ControlPoint
    ) -> Optional[FrontlineGroupTemplate]:
        compatible_templates = [
            t
            for t in FrontlineGroupLoader().all_templates()
            if self.can_fulfill_template(t)
        ]

        if not compatible_templates:
            return None

        # Calculate deficit weight for each template based on its primary role
        template_weights: list[tuple[FrontlineGroupTemplate, float]] = []

        for template in compatible_templates:
            # Get the primary unit class from the template's role
            primary_class = self.role_to_unit_class(template.role)

            # Calculate how underrepresented this class is
            current_ratio = self.cost_ratio_of_ground_unit(cp, primary_class)
            desired_ratio = (
                self.faction.doctrine.ground_unit_procurement_ratios.for_unit_class(
                    primary_class
                )
            )

            if desired_ratio and desired_ratio > 0:
                weight = max(0, desired_ratio - current_ratio)
            else:
                weight = random.uniform(0, 0.1)

            template_weights.append((template, weight))

        if not any(weight for _, weight in template_weights):
            return random.choice(compatible_templates)

        total_weight = sum(weight for _, weight in template_weights)
        r = random.uniform(0, total_weight)
        cumulative = 0
        for template, weight in template_weights:
            cumulative += weight
            if r <= cumulative:
                return template

        return compatible_templates[-1]

    def try_purchase_template_group(
        self, cp: ControlPoint, budget: float
    ) -> tuple[float, bool]:
        template = self.select_template_for_purchase(cp)

        if template is None:
            return budget, False

        result = self.plan_template_purchase(template, budget)
        if result is None:
            return budget, False

        units_to_buy, cost = result
        cp.ground_unit_orders.order_template(template.name, units_to_buy)
        logging.info(
            f"Purchased template '{template.name}' for {cost:.0f} at {cp.name}"
        )
        return budget - cost, True

    def reinforce_front_line(self, budget: float) -> float:
        if not self.faction.frontline_units and not self.faction.artillery_units:
            return budget

        # TODO: Attempt to transfer from reserves.

        while budget > 0:
            cp = self.ground_reinforcement_candidate()
            if cp is None:
                break
            budget, success = self.try_purchase_template_group(cp, budget)
            if success:
                continue
            # Fall back to individual unit purchase
            most_needed_type = self.most_needed_unit_class(cp)
            unit = self.affordable_ground_unit_of_class(budget, most_needed_type)
            if unit is None:
                # Can't afford any more units.
                break

            budget -= unit.price
            cp.ground_unit_orders.order({unit: 1})

        return budget

    def most_needed_unit_class(self, cp: ControlPoint) -> UnitClass:
        worst_balanced: Optional[UnitClass] = None
        worst_fulfillment = math.inf
        for unit_class in UnitClass:
            if not self.faction.has_access_to_unit_class(unit_class):
                continue

            current_ratio = self.cost_ratio_of_ground_unit(cp, unit_class)
            desired_ratio = (
                self.faction.doctrine.ground_unit_procurement_ratios.for_unit_class(
                    unit_class
                )
            )
            if not desired_ratio:
                continue
            if current_ratio >= desired_ratio:
                continue
            fulfillment = current_ratio / desired_ratio
            if fulfillment < worst_fulfillment:
                worst_fulfillment = fulfillment
                worst_balanced = unit_class
        if worst_balanced is None:
            return UnitClass.TANK
        return worst_balanced

    @staticmethod
    def fulfill_aircraft_request(
        squadrons: list[Squadron], quantity: int, budget: float
    ) -> Tuple[float, bool]:
        for squadron in squadrons:
            price = squadron.aircraft.price * quantity
            # Final check to make sure the number of aircraft won't exceed the number of available pilots
            # after fulfilling this aircraft request.
            if (
                squadron.pilot_limits_enabled
                and squadron.expected_size_next_turn + quantity
                > squadron.expected_pilots_next_turn
            ):
                continue
            if price > budget:
                continue

            squadron.pending_deliveries += quantity
            budget -= price
            return budget, True
        return budget, False

    def purchase_aircraft(self, budget: float) -> float:
        for request in self.game.coalition_for(self.is_player).procurement_requests:
            squadrons = list(self.best_squadrons_for(request))
            if not squadrons:
                # No airbases in range of this request. Skip it.
                continue
            budget, fulfilled = self.fulfill_aircraft_request(
                squadrons, request.number, budget
            )
        return budget

    @property
    def owned_points(self) -> List[ControlPoint]:
        if self.is_player.is_blue:
            return self.game.theater.player_points()
        else:
            return self.game.theater.enemy_points()

    def best_squadrons_for(
        self, request: AircraftProcurementRequest
    ) -> Iterator[Squadron]:
        threatened = []
        for squadron in self.air_wing.best_squadrons_for(
            request.near,
            request.task_capability,
            request.number,
            request.heli,
            this_turn=False,
        ):
            parking_type = ParkingType().from_squadron(squadron)

            if not squadron.can_provide_pilots(request.number):
                continue
            if squadron.location.unclaimed_parking(parking_type) < request.number:
                continue
            if not squadron.has_aircraft_capacity_for(request.number):
                continue
            if self.threat_zones.threatened(squadron.location.position):
                threatened.append(squadron)
                continue
            yield squadron
        yield from threatened

    def ground_reinforcement_candidate(self) -> Optional[ControlPoint]:
        worst_supply = math.inf
        understaffed: Optional[ControlPoint] = None

        # Prefer to buy front line units at active front lines that are not
        # already overloaded.
        for cp in self.owned_points:
            if not cp.has_active_frontline:
                continue

            if not cp.has_ground_unit_source(self.game):
                # No source of ground units, so can't buy anything.
                continue

            reserves_factor = (
                self.game.settings.frontline_reserves_factor
                if self.is_player.is_blue
                else self.game.settings.frontline_reserves_factor_red
            )
            fr_factor = reserves_factor / 100.0
            purchase_target = cp.frontline_unit_count_limit * fr_factor
            allocated = cp.allocated_ground_units(
                self.game.coalition_for(self.is_player).transfers
            )
            if allocated.total >= purchase_target:
                # Control point is already sufficiently defended.
                continue
            if allocated.total < worst_supply:
                worst_supply = allocated.total
                understaffed = cp

        if understaffed is not None:
            return understaffed

        # Otherwise buy reserves, but don't exceed the amount defined in the settings.
        # These units do not exist in the world until the CP becomes
        # connected to an active front line, at which point all these units
        # will suddenly appear at the gates of the newly captured CP.
        #
        # To avoid sudden overwhelming numbers of units we avoid buying
        # many.
        #
        # Also, do not bother buying units at bases that will never connect
        # to a front line.
        for cp in self.owned_points:
            if cp.is_global:
                continue
            if not cp.can_recruit_ground_units(self.game):
                continue

            allocated = cp.allocated_ground_units(
                self.game.coalition_for(self.is_player).transfers
            )
            target = (
                self.game.settings.reserves_procurement_target
                if self.is_player.is_blue
                else self.game.settings.reserves_procurement_target_red
            )
            if allocated.total >= target:
                continue

            if allocated.total < worst_supply:
                worst_supply = allocated.total
                understaffed = cp

        return understaffed

    def cost_ratio_of_ground_unit(
        self, control_point: ControlPoint, unit_class: UnitClass
    ) -> float:
        allocations = control_point.allocated_ground_units(
            self.game.coalition_for(self.is_player).transfers
        )
        class_cost = 0
        total_cost = 0
        for unit_type, count in allocations.all.items():
            cost = unit_type.price * count
            total_cost += cost
            if unit_type.unit_class is unit_class:
                class_cost += cost
        if not total_cost:
            return 0
        return class_cost / total_cost
