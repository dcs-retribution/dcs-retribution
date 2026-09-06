from __future__ import annotations

import collections
import itertools
import logging
import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, List, Optional, TYPE_CHECKING
from uuid import UUID

from game.data.units import UnitClass
from game.dcs.groundunittype import GroundUnitType
from .frontline_clustering import allocate_largest_remainder

if TYPE_CHECKING:
    from game import Game
    from game.theater import ControlPoint


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


class CombatGroup:
    def __init__(
        self, role: CombatGroupRole, unit_type: GroundUnitType, size: int
    ) -> None:
        self.unit_type = unit_type
        self.size = size
        self.role = role
        self.start_position = None
        # Set for clustered members to their cluster's armor wedge; None for the
        # wedge itself and for unclustered groups (artillery/logi). Spec B reads
        # this to make the cluster maneuver as a unit.
        self.anchor: Optional[CombatGroup] = None

    def __setstate__(self, state: dict[str, Any]) -> None:
        # Saves made before the cluster work (dr-588t) have no ``anchor``; pickle
        # skips ``__init__`` so backfill the default for those old CombatGroups.
        self.__dict__.update(state)
        if not hasattr(self, "anchor"):
            self.anchor = None

    def __str__(self) -> str:
        s = f"ROLE : {self.role}\n"
        if self.size:
            s += f"UNITS {self.unit_type} * {self.size}"
        return s


# Unit classes plan_groundwar maps to a front-line role; any other class is
# skipped (never deployed). Mirrors the if/elif chain in plan_groundwar.
_DEPLOYABLE_UNIT_CLASSES = frozenset(
    {
        UnitClass.TANK,
        UnitClass.APC,
        UnitClass.ARTILLERY,
        UnitClass.IFV,
        UnitClass.LOGISTICS,
        UnitClass.ATGM,
        UnitClass.SHORAD,
        UnitClass.AAA,
        UnitClass.RECON,
    }
)


def deployable_armor(cp: ControlPoint) -> dict[GroundUnitType, int]:
    """Per-type counts GroundPlanner.plan_groundwar deploys toward the front.

    Replicates plan_groundwar's allocation EXACTLY: proportional ratio, a <1
    share rounded up to 1, clamp to the remaining limit, round(), sequential
    decrement, stop at 0, and skip unit classes the planner does not deploy.
    No connected-enemy gate (reserve_armor_for applies it).

    KEEP IN SYNC with GroundPlanner.plan_groundwar — this duplicates its math on
    purpose. plan_groundwar has no tests on this base, so it is intentionally
    left untouched rather than refactored to share this helper.
    """
    limit = cp.frontline_unit_count_limit
    total = cp.base.total_armor
    remaining = limit
    ratio = min(limit / total, 1) if total > 0 else 1
    deployed: dict[GroundUnitType, int] = {}
    for unit_type in cp.base.armor:
        if unit_type.unit_class not in _DEPLOYABLE_UNIT_CLASSES:
            continue  # plan_groundwar skips these before consuming the limit
        available: float = cp.base.armor[unit_type] * ratio
        if 0 < available < 1:
            available = 1
        if available > remaining:
            available = remaining
        available = round(available)
        remaining -= available
        if available > 0:
            deployed[unit_type] = available
        if remaining == 0:
            break
    return deployed


def reserve_armor_for(cp: ControlPoint) -> dict[GroundUnitType, int]:
    """The not-deployed remainder of a CP's armor, by type.

    Deployed is empty for a CP with no connected enemy CP (nothing reaches the
    front, so all armor is reserve), matching plan_groundwar, which only sends
    units to a front where there is a connected enemy CP.
    """
    has_enemy = any(p.captured != cp.captured for p in cp.connected_points)
    deployed = deployable_armor(cp) if has_enemy else {}
    reserve: dict[GroundUnitType, int] = {}
    for unit_type, count in cp.base.armor.items():
        remainder = count - deployed.get(unit_type, 0)
        if remainder > 0:
            reserve[unit_type] = remainder
    return reserve


WEDGE_ROLES: frozenset[CombatGroupRole] = frozenset(
    {CombatGroupRole.TANK, CombatGroupRole.IFV, CombatGroupRole.APC}
)

# Deterministic iteration order for collecting wedges in assemble_clusters.
_WEDGE_ROLE_ORDER: tuple[CombatGroupRole, ...] = (
    CombatGroupRole.TANK,
    CombatGroupRole.IFV,
    CombatGroupRole.APC,
)

WEDGE_SIZE_MIN = 5
WEDGE_SIZE_MAX = 7

# Depth of a cluster member relative to its armor wedge, in metres. Negative is
# toward the enemy (in front of the wedge); positive is behind it. Applied on top
# of the wedge's own distance-from-frontline at placement time (Task 6).
CLUSTER_DEPTH_OFFSET: dict[CombatGroupRole, int] = {
    CombatGroupRole.RECON: -800,
    CombatGroupRole.SHORAD: 800,
    CombatGroupRole.ATGM: 2000,
}

_ROLE_BY_UNIT_CLASS: dict[UnitClass, CombatGroupRole] = {
    UnitClass.TANK: CombatGroupRole.TANK,
    UnitClass.APC: CombatGroupRole.APC,
    UnitClass.IFV: CombatGroupRole.IFV,
    UnitClass.ARTILLERY: CombatGroupRole.ARTILLERY,
    UnitClass.LOGISTICS: CombatGroupRole.LOGI,
    UnitClass.ATGM: CombatGroupRole.ATGM,
    UnitClass.SHORAD: CombatGroupRole.SHORAD,
    UnitClass.AAA: CombatGroupRole.SHORAD,
    UnitClass.RECON: CombatGroupRole.RECON,
}

# Fixed group sizes per role (replaces stance-based sizing for Spec A).
_FIXED_GROUP_SIZE_BY_ROLE: dict[CombatGroupRole, int] = {
    CombatGroupRole.SHORAD: 1,
    CombatGroupRole.ATGM: 2,
    CombatGroupRole.RECON: 2,
}


@dataclass
class Cluster:
    wedge: CombatGroup
    members: list[CombatGroup] = field(default_factory=list)


def interleave_by_unit_type(groups: list[CombatGroup]) -> list[CombatGroup]:
    """Reorder so consecutive groups prefer distinct unit types (round-robin)."""
    by_type: dict[GroundUnitType, collections.deque[CombatGroup]] = {}
    for g in groups:
        by_type.setdefault(g.unit_type, collections.deque()).append(g)
    ordered: list[CombatGroup] = []
    queues = list(by_type.values())
    while any(queues):
        for q in queues:
            if q:
                ordered.append(q.popleft())
    return ordered


def assemble_clusters(
    buckets: dict[CombatGroupRole, list[CombatGroup]],
) -> list[Cluster]:
    """Group pre-sized single-type CombatGroups into combat clusters.

    Each WEDGE_ROLES group becomes a cluster anchor. Wedges are interleaved by
    unit_type so adjacent clusters alternate armor types. RECON and ATGM groups
    are attached round-robin (one per cluster first, then spares). SHORAD groups
    are attached with a distinct-type rule: each cluster gets at most 1 SHORAD of
    any given type (a 2nd SHORAD is only attached if it is a different unit_type
    than the cluster's existing SHORAD). Unattached SHORAD keep ``anchor = None``
    so that ``plan_groundwar``'s unclustered path places them independently.

    Roles missing from ``buckets`` are skipped, so a cluster degrades to
    armor-only when no members are available.
    """
    wedges: list[CombatGroup] = []
    for role in _WEDGE_ROLE_ORDER:
        wedges.extend(buckets.get(role, []))
    if not wedges:
        return []

    # I2: interleave wedges by type so adjacent clusters alternate armor type.
    wedges = interleave_by_unit_type(wedges)
    clusters = [Cluster(wedge=w, members=[]) for w in wedges]

    # RECON and ATGM: simple round-robin, one per cluster first then spares.
    for role in (CombatGroupRole.RECON, CombatGroupRole.ATGM):
        members = list(buckets.get(role, []))
        for member, cluster in zip(members, itertools.cycle(clusters)):
            member.anchor = cluster.wedge
            cluster.members.append(member)

    # I1: SHORAD — 1 per cluster; 2nd only if a distinct unit_type from the
    # cluster's existing SHORAD. Same-type extras are left unattached (anchor
    # stays None) so plan_groundwar's unclustered path picks them up.
    shorad_groups = list(buckets.get(CombatGroupRole.SHORAD, []))
    if shorad_groups:
        # First pass: one SHORAD per cluster (round-robin).
        cluster_shorad_types: list[set[GroundUnitType]] = [set() for _ in clusters]
        remaining_shorad: list[CombatGroup] = []
        for shorad, cluster_idx in zip(
            shorad_groups,
            itertools.islice(itertools.cycle(range(len(clusters))), len(shorad_groups)),
        ):
            c = clusters[cluster_idx]
            seen = cluster_shorad_types[cluster_idx]
            if not seen:
                # First SHORAD on this cluster — always attach.
                shorad.anchor = c.wedge
                c.members.append(shorad)
                seen.add(shorad.unit_type)
            else:
                remaining_shorad.append(shorad)

        # Second pass: attach remaining SHORAD only if distinct type.
        unattached_idx = 0
        for shorad in remaining_shorad:
            # Try each cluster (starting from unattached_idx to distribute evenly).
            for offset in range(len(clusters)):
                idx = (unattached_idx + offset) % len(clusters)
                seen = cluster_shorad_types[idx]
                if shorad.unit_type not in seen:
                    c = clusters[idx]
                    shorad.anchor = c.wedge
                    c.members.append(shorad)
                    seen.add(shorad.unit_type)
                    unattached_idx = (idx + 1) % len(clusters)
                    break
            # If not placed, shorad.anchor remains None → unclustered.

    return clusters


def _fixed_size_groups(
    role: CombatGroupRole, unit_type: GroundUnitType, n: int, size: int
) -> list[CombatGroup]:
    """Return groups of ``size`` units; the last group may be smaller."""
    groups: list[CombatGroup] = []
    remaining = n
    while remaining > 0:
        group_size = min(remaining, size)
        groups.append(CombatGroup(role, unit_type, group_size))
        remaining -= group_size
    return groups


class GroundPlanner:
    def __init__(self, cp: ControlPoint, game: Game) -> None:
        self.cp = cp
        self.game = game
        self.connected_enemy_cp = [
            cp for cp in self.cp.connected_points if cp.captured != self.cp.captured
        ]

        self.units_per_cp: dict[UUID, List[CombatGroup]] = {}
        for cp in self.connected_enemy_cp:
            self.units_per_cp[cp.id] = []
        self.reserve: List[CombatGroup] = []

    def plan_groundwar(self) -> None:
        limit = self.cp.frontline_unit_count_limit
        total = self.cp.base.total_armor
        if total <= 0 or limit <= 0:
            return
        ratio = min(limit / total, 1)

        # 1. Proportional deployable count per unit type, capped at the limit.
        weights: dict[GroundUnitType, float] = {}
        for unit_type, count in self.cp.base.armor.items():
            if unit_type.unit_class not in _ROLE_BY_UNIT_CLASS:
                logging.warning(
                    f"Unused front line vehicle at base {unit_type}: unknown unit class"
                )
                continue
            weights[unit_type] = count * ratio
        deploy = allocate_largest_remainder(weights, limit)

        # 2. Split each type's allocation into correctly-sized single-type groups,
        #    bucketed by role. Wedges get 5-7 (small leftover absorbed); SHORAD/
        #    ATGM/RECON get their fixed sizes.
        buckets: dict[CombatGroupRole, list[CombatGroup]] = {}
        for unit_type, n in deploy.items():
            if n <= 0:
                continue
            role = _ROLE_BY_UNIT_CLASS[unit_type.unit_class]
            for group in self._split_into_groups(role, unit_type, n):
                buckets.setdefault(role, []).append(group)

        # Order SHORAD so distinct types lead: the distinct-type attach pass in
        # assemble_clusters handles the 2nd-per-cluster rule correctly when types
        # are interleaved first.
        if CombatGroupRole.SHORAD in buckets:
            buckets[CombatGroupRole.SHORAD] = interleave_by_unit_type(
                buckets[CombatGroupRole.SHORAD]
            )

        # 3. Assemble clusters (sets anchors on members).
        clusters = assemble_clusters(buckets)

        # 4. Unclustered groups: artillery + logi (+ any role with no wedge).
        clustered = {id(c.wedge) for c in clusters}
        clustered |= {id(m) for c in clusters for m in c.members}
        unclustered = [
            g for gs in buckets.values() for g in gs if id(g) not in clustered
        ]

        # 5. Distribute clusters + unclustered groups across enemy CPs.
        if not self.connected_enemy_cp:
            for c in clusters:
                self.reserve.extend([c.wedge, *c.members])
            self.reserve.extend(unclustered)
            return

        for i, cluster in enumerate(clusters):
            enemy_cp = self.connected_enemy_cp[i % len(self.connected_enemy_cp)]
            self.units_per_cp[enemy_cp.id].extend([cluster.wedge, *cluster.members])
        for i, group in enumerate(unclustered):
            enemy_cp = self.connected_enemy_cp[i % len(self.connected_enemy_cp)]
            self.units_per_cp[enemy_cp.id].append(group)

    def _split_into_groups(
        self, role: CombatGroupRole, unit_type: GroundUnitType, n: int
    ) -> list[CombatGroup]:
        groups: list[CombatGroup] = []
        if role in WEDGE_ROLES:
            remaining = n
            while remaining > 0:
                size = min(remaining, random.randint(WEDGE_SIZE_MIN, WEDGE_SIZE_MAX))
                # Absorb a tiny trailing leftover (1) into this wedge rather than
                # spawning a lone vehicle.
                if 0 < remaining - size < 2:
                    size = remaining
                groups.append(CombatGroup(role, unit_type, size))
                remaining -= size
        elif role in _FIXED_GROUP_SIZE_BY_ROLE:
            groups = _fixed_size_groups(
                role, unit_type, n, _FIXED_GROUP_SIZE_BY_ROLE[role]
            )
        else:  # ARTILLERY, LOGI: one group per type (current behaviour).
            groups = [CombatGroup(role, unit_type, n)]
        return groups
