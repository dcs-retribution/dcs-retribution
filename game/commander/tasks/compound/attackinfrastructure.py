from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass

from game.commander.tasks.primitive.strike import PlanStrike
from game.commander.theaterstate import TheaterState
from game.config import REWARDS
from game.htn import CompoundTask, Method
from game.theater.theatergroundobject import BuildingGroundObject


# High-value infrastructure categories worth targeting
HIGH_VALUE_CATEGORIES = ["oil", "derrick", "factory", "fuel"]


@dataclass(frozen=True)
class AttackInfrastructure(CompoundTask[TheaterState]):
    """Plans attacks on high-value enemy infrastructure.
    
    Targets valuable buildings like fuel depots, oil facilities, and factories
    that generate significant income for the enemy. Prioritizes targets that are:
    1. High value (based on income generation)
    2. Accessible (outside of threat zones)
    3. Close to friendly bases
    """

    def _calculate_target_value(self, target: BuildingGroundObject) -> float:
        """Calculate the total income value of a target."""
        category = target.category
        if category not in REWARDS:
            return 0.0
        
        income_per_building = REWARDS[category]
        alive_count = sum(1 for unit in target.statics if unit.alive)
        return income_per_building * alive_count

    def _get_closest_friendly_distance(
        self, target: BuildingGroundObject, state: TheaterState
    ) -> float:
        """Get distance from target to closest friendly control point."""
        min_distance = float("inf")
        for cp in state.context.theater.control_points_for(state.context.coalition.player):
            distance = cp.position.distance_to_point(target.position)
            if distance < min_distance:
                min_distance = distance
        return min_distance

    def each_valid_method(self, state: TheaterState) -> Iterator[Method[TheaterState]]:
        """Yields strike missions for high-value infrastructure targets.
        
        Filters for buildings in high-value categories, calculates their worth,
        and prioritizes by value-to-distance ratio to target the most valuable
        and accessible infrastructure first.
        """
        # Collect and evaluate high-value targets
        valuable_targets = []
        
        for target in state.strike_targets:
            # Only consider building ground objects
            if not isinstance(target, BuildingGroundObject):
                continue
            
            # Skip if not a high-value category
            if target.category not in HIGH_VALUE_CATEGORIES:
                continue
            
            # Skip ammo depots (handled by other tasks)
            if target.is_ammo_depot:
                continue
            
            # Calculate value and distance
            value = self._calculate_target_value(target)
            if value <= 0:
                continue
            
            distance = self._get_closest_friendly_distance(target, state)
            if distance == float("inf"):
                continue
            
            # Calculate priority (higher value / shorter distance = higher priority)
            priority = value / (distance / 1000.0)  # Normalize distance to km
            
            valuable_targets.append((priority, value, distance, target))
        
        # Sort by priority (highest first)
        valuable_targets.sort(key=lambda x: x[0], reverse=True)
        
        # Yield strike plans for targets in priority order
        for priority, value, distance, target in valuable_targets:
            yield [PlanStrike(target)]
