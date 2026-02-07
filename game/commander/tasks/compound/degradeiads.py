import logging
from collections.abc import Iterator, Sequence
from typing import Union

from game.commander.tasks.primitive.antiship import PlanAntiShip
from game.commander.tasks.primitive.dead import PlanDead
from game.commander.theaterstate import TheaterState
from game.data.groups import GroupTask
from game.htn import CompoundTask, Method
from game.theater.missiontarget import MissionTarget
from game.theater.theatergroundobject import IadsGroundObject, NavalGroundObject
from game.utils import Distance


class DegradeIads(CompoundTask[TheaterState]):
    # Yield multiple DEAD targets as alternatives for HTN planner to try
    # If first target fails planning, HTN will automatically try next alternative

    def each_valid_method(self, state: TheaterState) -> Iterator[Method[TheaterState]]:
        # Get all candidate targets in priority order
        candidates = []
        settings = state.context.settings

        # Priority 1: Strategic threats (based on threat circle proximity)
        strategically_threatening_sams = self._assess_strategic_threats(
            state.enemy_air_defenses, state
        )
        for sam in strategically_threatening_sams:
            candidates.append(("strategic", sam))

        # Priority 2: Systems actively threatening planned missions
        prioritized_threats = self._prioritize_threatening_systems(
            [
                defense
                for defense in state.threatening_air_defenses
                if isinstance(defense, IadsGroundObject)
            ]
        )
        for sam in prioritized_threats:
            # Only add if not already in candidates
            if not any(c[1] == sam for c in candidates):
                candidates.append(("threatening", sam))

        # Priority 3: High-value detection systems (EWRs)
        high_value_detectors = [
            d
            for d in state.detecting_air_defenses
            if d.task == GroupTask.EARLY_WARNING_RADAR
        ]
        for ewr in high_value_detectors[:1]:
            if not any(c[1] == ewr for c in candidates):
                candidates.append(("detector", ewr))

        # Yield each candidate as a separate method
        # HTN planner will try them in order until one succeeds
        for priority_type, target in candidates:
            yield [self.plan_against(target)]

    def _prioritize_threatening_systems(
        self, threatening: list[IadsGroundObject]
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
        prioritized.extend(lorad_threats[:1])
        if len(lorad_threats) == 0:
            # Only if no LORAD, take top MERAD targets
            prioritized.extend(merad_threats[:1])

        return prioritized

    def _assess_strategic_threats(
        self, air_defenses: list[IadsGroundObject], state: TheaterState
    ) -> list[Union[IadsGroundObject, NavalGroundObject]]:
        """Assess and prioritize air defenses by strategic threat level.

        Prioritizes based on:
        1. Capability tier (LORAD > MERAD, SHORAD/AAA generally ignored)
        2. Range and coverage of friendly bases
        3. Position relative to operations

        Includes both land-based SAMs and naval SAM systems.

        Returns sorted list with highest threats first (limited to top 2).
        """
        threats: list[tuple[float, Union[IadsGroundObject, NavalGroundObject]]] = []

        # Get all friendly control points for threat assessment
        friendly_cps = list(
            state.context.theater.control_points_for(state.context.coalition.player)
        )

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
                state,
                state.context.settings.degrade_iads_max_land_threat_penetration_meters,
                state.context.settings.degrade_iads_threat_range_effectiveness_percent,
                state.context.settings.degrade_iads_threat_score_baseline_meters,
            )

            # Only consider systems that pose actual strategic threat
            if threat_score > 0:
                threats.append((threat_score, air_defense))

        # Assess naval SAM threats (ships with air defense capabilities)
        for ship in state.enemy_ships:
            threat_range = ship.max_threat_range()

            threat_score = self._calculate_naval_threat_score(
                ship,
                threat_range,
                friendly_cps,
                state.context.settings.degrade_iads_min_naval_threat_range_meters,
                state.context.settings.degrade_iads_max_naval_threat_penetration_meters,
                state.context.settings.degrade_iads_threat_range_effectiveness_percent,
                state.context.settings.degrade_iads_threat_score_baseline_meters,
            )

            if threat_score > 0:
                threats.append((threat_score, ship))

        # Sort by threat score (highest first) and return top strategic targets only
        threats.sort(key=lambda x: x[0], reverse=True)
        return [
            ad
            for _, ad in threats[
                : state.context.settings.degrade_iads_max_strategic_targets
            ]
        ]

    def _calculate_naval_threat_score(
        self,
        ship: NavalGroundObject,
        threat_range: Distance,
        friendly_cps: Sequence[MissionTarget],
        min_threat_range_meters: int,
        max_threat_penetration_meters: int,
        threat_range_effectiveness_percent: int,
        threat_score_baseline_meters: int,
    ) -> float:
        """Calculate threat score for naval SAM systems.

        Prioritizes ships whose threat circle is closest to any friendly CP.
        Lower distance = higher threat.
        """
        effective_range = threat_range.meters * (
            float(threat_range_effectiveness_percent) / 100.0
        )

        if effective_range < min_threat_range_meters:
            # Very short range, not worth targeting
            return 0.0

        # Find the closest approach distance (distance - range)
        # This tells us how close the threat circle edge gets to a friendly base
        closest_threat_penetration = float("inf")

        for cp in friendly_cps:
            distance = ship.distance_to(cp)
            # How far is the threat circle edge from this CP?
            penetration_distance = distance - effective_range
            closest_threat_penetration = min(
                closest_threat_penetration, penetration_distance
            )

        # If threat circle can't reach ANY base, lower priority
        # Increased threshold to N meters to capture more strategic naval SAMs
        if closest_threat_penetration > max_threat_penetration_meters:
            return 0.0

        # Invert the score: closer threat circle = higher priority
        # Normalize to reasonable scale (closer = bigger score)
        # Using negative values for systems that can already reach bases
        threat_score = float(threat_score_baseline_meters) - closest_threat_penetration

        return max(0.0, threat_score)

    def _calculate_threat_score(
        self,
        air_defense: IadsGroundObject,
        threat_range: Distance,
        friendly_cps: Sequence[MissionTarget],
        state: TheaterState,
        max_threat_penetration_meters: int,
        threat_range_effectiveness_percent: int,
        threat_score_baseline_meters: int,
    ) -> float:
        """Calculate threat score for air defense system.

        Prioritizes SAMs whose threat circle is closest to any friendly CP.
        Simple approach: distance_to_closest_cp - threat_range
        Lower result = closer threat circle = higher priority.
        """
        # Only consider meaningful SAM systems
        if air_defense.task not in [GroupTask.LORAD, GroupTask.MERAD]:
            return 0.0

        effective_range = threat_range.meters * (
            float(threat_range_effectiveness_percent) / 100.0
        )

        # Find the closest approach distance (distance - range)
        # This tells us how close the threat circle edge gets to a friendly base
        closest_threat_penetration = float("inf")

        for cp in friendly_cps:
            distance = air_defense.distance_to(cp)
            # How far is the threat circle edge from this CP?
            penetration_distance = distance - effective_range
            if penetration_distance < closest_threat_penetration:
                closest_threat_penetration = penetration_distance

        # If threat circle is very far away, deprioritize
        # Increased threshold to N meters to capture more strategic SAMs
        if closest_threat_penetration > max_threat_penetration_meters:
            return 0.0

        # Invert the score: closer threat circle = higher priority
        # Normalize to reasonable scale (closer = bigger score)
        # Using N meters as baseline - systems further than that get very low scores
        threat_score = float(threat_score_baseline_meters) - closest_threat_penetration

        return max(0.0, threat_score)

    @staticmethod
    def plan_against(
        target: Union[IadsGroundObject, NavalGroundObject],
    ) -> Union[PlanDead, PlanAntiShip]:
        if isinstance(target, IadsGroundObject):
            return PlanDead(target)
        return PlanAntiShip(target)
