from collections.abc import Iterator
import logging

from game.commander.tasks.primitive.armedrecon import PlanArmedRecon
from game.commander.tasks.primitive.bai import PlanBai
from game.commander.theaterstate import TheaterState
from game.htn import CompoundTask, Method


class AttackBattlePositions(CompoundTask[TheaterState]):
    def each_valid_method(self, state: TheaterState) -> Iterator[Method[TheaterState]]:
        """Plan BAI missions against nearest enemy control points.

        Prioritizes enemy CPs that are closest to friendly CPs.
        Limits total BAI packages to prevent spending all aircraft on ground attack.
        """
        # Get friendly control points for distance calculation
        friendly_cps = list(
            state.context.theater.control_points_for(state.context.coalition.player)
        )

        if not friendly_cps:
            return

        settings = state.context.settings

        # Score and sort enemy CPs by distance to nearest friendly CP
        enemy_cp_scores = []
        for enemy_cp, battle_positions in state.enemy_battle_positions.items():
            # Skip if no battle positions
            if not list(battle_positions.in_priority_order):
                continue

            # Find distance to closest friendly CP
            min_distance = min(enemy_cp.distance_to(fcp) for fcp in friendly_cps)

            # Filter out CPs that are too far away
            if min_distance > settings.bai_max_distance_meters:
                continue

            # Lower distance = higher priority (negate for sorting)
            enemy_cp_scores.append((min_distance, enemy_cp, battle_positions))

        # Sort by distance (closest first)
        enemy_cp_scores.sort(key=lambda x: x[0])

        # Yield BAI targets from closest CPs, limited to configured total
        packages_yielded = 0
        for distance, enemy_cp, battle_positions in enemy_cp_scores:
            if packages_yielded >= settings.bai_max_packages:
                break

            # Yield top battle positions from this CP
            positions_from_cp = 0
            for battle_position in battle_positions.in_priority_order:
                if positions_from_cp >= settings.bai_max_positions_per_cp:
                    break

                yield [PlanBai(battle_position)]
                packages_yielded += 1
                positions_from_cp += 1

                if packages_yielded >= settings.bai_max_packages:
                    break

        # Plan armed recon against highest priority CPs
        for cp in state.control_point_priority_queue[
            : settings.bai_armed_recon_target_count
        ]:
            if not cp.is_fleet:
                yield [PlanArmedRecon(cp)]
