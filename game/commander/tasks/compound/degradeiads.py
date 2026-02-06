import logging
from collections.abc import Iterator
from typing import Union

from game.commander.tasks.primitive.antiship import PlanAntiShip
from game.commander.tasks.primitive.dead import PlanDead
from game.commander.theaterstate import TheaterState
from game.data.groups import GroupTask
from game.htn import CompoundTask, Method
from game.theater.theatergroundobject import IadsGroundObject, NavalGroundObject
from game.utils import meters


class DegradeIads(CompoundTask[TheaterState]):
    # Yield multiple DEAD targets as alternatives for HTN planner to try
    # If first target fails planning, HTN will automatically try next alternative

    def each_valid_method(self, state: TheaterState) -> Iterator[Method[TheaterState]]:
        # Get all candidate targets in priority order
        candidates = []

        # Priority 1: Strategic threats (based on threat circle proximity)
        strategically_threatening_sams = self._assess_strategic_threats(
            state.enemy_air_defenses, state
        )
        for sam in strategically_threatening_sams:
            candidates.append(("strategic", sam))

        # Priority 2: Systems actively threatening planned missions
        prioritized_threats = self._prioritize_threatening_systems(state.threatening_air_defenses)
        for sam in prioritized_threats:
            # Only add if not already in candidates
            if not any(c[1] == sam for c in candidates):
                candidates.append(("threatening", sam))

        # Priority 3: High-value detection systems (EWRs)
        high_value_detectors = [
            d for d in state.detecting_air_defenses
            if d.task == GroupTask.EARLY_WARNING_RADAR
        ]
        for ewr in high_value_detectors[:2]:  # Top 2 EWRs
            if not any(c[1] == ewr for c in candidates):
                candidates.append(("detector", ewr))

        # Yield each candidate as a separate method
        # HTN planner will try them in order until one succeeds
        for priority_type, target in candidates:
            yield [self.plan_against(target)]

    def _prioritize_threatening_systems(
            self,
            threatening: list[IadsGroundObject]
    ) -> list[IadsGroundObject]:
        """Prioritize threatening systems to avoid targeting every AAA/SHORAD.
        
        Focus on high-value threats: LORAD > MERAD > SHORAD.
        AAA is only targeted if it's one of the very few threats.
        """
        if not threatening:
            return []

        # Categorize by threat tier
        lorad_threats = [t for t in threatening if t.task == GroupTask.LORAD]
        merad_threats = [t for t in threatening if t.task == GroupTask.MERAD]
        shorad_threats = [t for t in threatening if t.task == GroupTask.SHORAD]

        # Prioritize: top LORAD, top MERAD only (very selective)
        prioritized = []
        prioritized.extend(lorad_threats[:1])  # Top 1 long-range SAM only
        if len(lorad_threats) == 0:
            # Only if no LORAD, take top 1 MERAD
            prioritized.extend(merad_threats[:1])

        return prioritized

    def _assess_strategic_threats(
            self,
            air_defenses: list[IadsGroundObject],
            state: TheaterState
    ) -> list[Union[IadsGroundObject, NavalGroundObject]]:
        """Assess and prioritize air defenses by strategic threat level.
        
        Prioritizes based on:
        1. Capability tier (LORAD > MERAD, SHORAD/AAA generally ignored)
        2. Range and coverage of friendly bases
        3. Position relative to operations
        
        Includes both land-based SAMs and naval SAM systems.
        
        Returns sorted list with highest threats first (limited to top 2).
        """
        threats = []

        # Get all friendly control points for threat assessment
        friendly_cps = list(state.context.theater.control_points_for(
            state.context.coalition.player
        ))

        # Assess land-based SAMs
        for air_defense in air_defenses:
            # Only consider SAM systems that are meaningful threats
            if air_defense.task not in [GroupTask.LORAD, GroupTask.MERAD]:
                continue

            threat_range = air_defense.max_threat_range()

            # Calculate threat value based on multiple factors
            threat_score = self._calculate_threat_score(
                air_defense,
                threat_range,
                friendly_cps,
                state
            )

            # Only consider systems that pose actual strategic threat
            if threat_score > 0:
                threats.append((threat_score, air_defense))

        # Assess naval SAM threats (ships with air defense capabilities)
        for ship in state.enemy_ships:
            threat_range = ship.max_threat_range()

            # Ships with significant SAM range are strategic threats
            if threat_range.meters > 20000:  # 20km+ range worth considering
                threat_score = self._calculate_naval_threat_score(
                    ship,
                    threat_range,
                    friendly_cps
                )

                if threat_score > 0:
                    threats.append((threat_score, ship))

        # Sort by threat score (highest first) and return top 2 only
        threats.sort(key=lambda x: x[0], reverse=True)
        return [ad for _, ad in threats[:2]]

    def _calculate_naval_threat_score(
            self,
            ship: NavalGroundObject,
            threat_range: meters,
            friendly_cps: list
    ) -> float:
        """Calculate threat score for naval SAM systems.
        
        Prioritizes ships whose threat circle is closest to any friendly CP.
        Lower distance = higher threat.
        """
        if threat_range.meters < 20000:
            # Very short range, not worth targeting
            return 0.0

        # Find the closest approach distance (distance - range)
        # This tells us how close the threat circle edge gets to a friendly base
        closest_threat_penetration = float('inf')

        for cp in friendly_cps:
            distance = ship.distance_to(cp)
            # How far is the threat circle edge from this CP?
            penetration_distance = distance - threat_range.meters
            closest_threat_penetration = min(closest_threat_penetration, penetration_distance)

        # If threat circle can't reach ANY base, lower priority
        # Increased threshold to 150km to capture more strategic naval SAMs
        if closest_threat_penetration > 150000:  # 150km+ away from all bases
            return 0.0

        # Invert the score: closer threat circle = higher priority
        # Normalize to reasonable scale (closer = bigger score)
        # Using negative values for systems that can already reach bases
        threat_score = 200000.0 - closest_threat_penetration

        return max(0.0, threat_score)

    def _calculate_threat_score(
            self,
            air_defense: IadsGroundObject,
            threat_range: meters,
            friendly_cps: list,
            state: TheaterState
    ) -> float:
        """Calculate threat score for air defense system.
        
        Prioritizes SAMs whose threat circle is closest to any friendly CP.
        Simple approach: distance_to_closest_cp - threat_range
        Lower result = closer threat circle = higher priority.
        """
        # Only consider meaningful SAM systems
        if air_defense.task not in [GroupTask.LORAD, GroupTask.MERAD]:
            return 0.0

        # Find the closest approach distance (distance - range)
        # This tells us how close the threat circle edge gets to a friendly base
        closest_threat_penetration = float('inf')

        for cp in friendly_cps:
            distance = air_defense.distance_to(cp)
            # How far is the threat circle edge from this CP?
            penetration_distance = distance - threat_range.meters
            if penetration_distance < closest_threat_penetration:
                closest_threat_penetration = penetration_distance

        # If threat circle is very far away, deprioritize
        # Increased threshold to 100km to capture more strategic SAMs
        if closest_threat_penetration > 100000:  # 100km+ away from all bases
            return 0.0

        # Invert the score: closer threat circle = higher priority
        # Normalize to reasonable scale (closer = bigger score)
        # Using 200km as baseline - systems further than that get very low scores
        threat_score = 200000.0 - closest_threat_penetration

        return max(0.0, threat_score)

    @staticmethod
    def plan_against(
            target: Union[IadsGroundObject, NavalGroundObject],
    ) -> Union[PlanDead, PlanAntiShip]:
        if isinstance(target, IadsGroundObject):
            return PlanDead(target)
        return PlanAntiShip(target)
