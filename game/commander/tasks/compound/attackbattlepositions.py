from collections.abc import Iterator
import logging

from game.commander.tasks.primitive.armedrecon import PlanArmedRecon
from game.commander.tasks.primitive.bai import PlanBai
from game.commander.theaterstate import TheaterState
from game.htn import CompoundTask, Method

# Maximum number of BAI packages to plan
MAX_BAI_PACKAGES = 4
# Maximum number of battle positions per enemy CP
MAX_POSITIONS_PER_CP = 2
# Maximum distance to consider enemy CP for BAI (in meters)
MAX_BAI_DISTANCE = 200000  # 200km


class AttackBattlePositions(CompoundTask[TheaterState]):
    def each_valid_method(self, state: TheaterState) -> Iterator[Method[TheaterState]]:
        """Plan BAI missions against nearest enemy control points.
        
        Prioritizes enemy CPs that are closest to friendly CPs.
        Limits total BAI packages to prevent spending all aircraft on ground attack.
        """
        # Get friendly control points for distance calculation
        friendly_cps = list(state.context.theater.control_points_for(
            state.context.coalition.player
        ))
        
        if not friendly_cps:
            return
        
        # Score and sort enemy CPs by distance to nearest friendly CP
        enemy_cp_scores = []
        for enemy_cp, battle_positions in state.enemy_battle_positions.items():
            # Skip if no battle positions
            if not list(battle_positions.in_priority_order):
                continue
            
            # Find distance to closest friendly CP
            min_distance = min(enemy_cp.distance_to(fcp) for fcp in friendly_cps)
            
            # Filter out CPs that are too far away
            if min_distance > MAX_BAI_DISTANCE:
                continue
            
            # Lower distance = higher priority (negate for sorting)
            enemy_cp_scores.append((min_distance, enemy_cp, battle_positions))
        
        # Sort by distance (closest first)
        enemy_cp_scores.sort(key=lambda x: x[0])
        
        # Yield BAI targets from closest CPs, limited to MAX_BAI_PACKAGES total
        packages_yielded = 0
        for distance, enemy_cp, battle_positions in enemy_cp_scores:
            if packages_yielded >= MAX_BAI_PACKAGES:
                break
            
            # Yield top battle positions from this CP
            positions_from_cp = 0
            for battle_position in battle_positions.in_priority_order:
                if positions_from_cp >= MAX_POSITIONS_PER_CP:
                    break
                
                yield [PlanBai(battle_position)]
                packages_yielded += 1
                positions_from_cp += 1
                
                if packages_yielded >= MAX_BAI_PACKAGES:
                    break
        
        # Plan armed recon against highest priority CPs
        for cp in state.control_point_priority_queue[:2]:
            if not cp.is_fleet:
                yield [PlanArmedRecon(cp)]
