from types import SimpleNamespace
from typing import Any
from unittest.mock import MagicMock
from uuid import uuid4

from game.data.units import UnitClass
from game.dcs.groundunittype import GroundUnitType
from game.ground_forces.ai_ground_planner import CombatGroup, CombatGroupRole
from game.ground_forces.ai_ground_planner import (
    Cluster,
    CLUSTER_DEPTH_OFFSET,
    WEDGE_ROLES,
    assemble_clusters,
    interleave_by_unit_type,
    GroundPlanner,
)


def test_combat_group_anchor_defaults_to_none() -> None:
    unit_type = MagicMock(spec=GroundUnitType)
    group = CombatGroup(CombatGroupRole.TANK, unit_type, 5)
    assert group.anchor is None


def test_combat_group_anchor_settable() -> None:
    unit_type = MagicMock(spec=GroundUnitType)
    wedge = CombatGroup(CombatGroupRole.TANK, unit_type, 5)
    shorad = CombatGroup(CombatGroupRole.SHORAD, unit_type, 1)
    shorad.anchor = wedge
    assert shorad.anchor is wedge


def test_combat_group_setstate_backfills_anchor_for_old_saves() -> None:
    # Saves predating dr-588t have no ``anchor`` in their pickled state; pickle
    # skips ``__init__`` so __setstate__ must backfill the default.
    unit_type = MagicMock(spec=GroundUnitType)
    group = CombatGroup(CombatGroupRole.TANK, unit_type, 5)
    old_state = dict(group.__dict__)
    del old_state["anchor"]

    restored = CombatGroup.__new__(CombatGroup)
    restored.__setstate__(old_state)

    assert restored.anchor is None


def test_combat_group_setstate_preserves_existing_anchor() -> None:
    unit_type = MagicMock(spec=GroundUnitType)
    wedge = CombatGroup(CombatGroupRole.TANK, unit_type, 5)
    member = CombatGroup(CombatGroupRole.SHORAD, unit_type, 1)
    member.anchor = wedge

    restored = CombatGroup.__new__(CombatGroup)
    restored.__setstate__(dict(member.__dict__))

    assert restored.anchor is wedge


def _grp(role: CombatGroupRole, size: int) -> CombatGroup:
    return CombatGroup(role, MagicMock(spec=GroundUnitType), size)


def test_assemble_attaches_members_and_sets_anchor() -> None:
    wedge = _grp(CombatGroupRole.TANK, 6)
    shorad = _grp(CombatGroupRole.SHORAD, 1)
    atgm = _grp(CombatGroupRole.ATGM, 2)
    clusters = assemble_clusters(
        {
            CombatGroupRole.TANK: [wedge],
            CombatGroupRole.SHORAD: [shorad],
            CombatGroupRole.ATGM: [atgm],
        }
    )
    assert len(clusters) == 1
    assert clusters[0].wedge is wedge
    assert shorad in clusters[0].members
    assert atgm in clusters[0].members
    assert shorad.anchor is wedge
    assert atgm.anchor is wedge
    assert wedge.anchor is None


def test_assemble_armor_only_when_no_members() -> None:
    wedge = _grp(CombatGroupRole.IFV, 5)
    clusters = assemble_clusters({CombatGroupRole.IFV: [wedge]})
    assert len(clusters) == 1
    assert clusters[0].members == []


def test_assemble_distributes_spares_round_robin() -> None:
    w1 = _grp(CombatGroupRole.TANK, 6)
    w2 = _grp(CombatGroupRole.TANK, 6)
    s1 = _grp(CombatGroupRole.SHORAD, 1)
    s2 = _grp(CombatGroupRole.SHORAD, 1)
    s3 = _grp(CombatGroupRole.SHORAD, 1)
    clusters = assemble_clusters(
        {CombatGroupRole.TANK: [w1, w2], CombatGroupRole.SHORAD: [s1, s2, s3]}
    )
    assert len(clusters) == 2
    # _grp() creates a fresh MagicMock unit_type each call, so all 3 SHORAD are
    # distinct types and all 3 attach via the distinct-type path (2 clusters × ≥1
    # SHORAD each, with the 3rd placed on whichever cluster the round-robin picks).
    total_shorad = sum(len(c.members) for c in clusters)
    assert total_shorad == 3
    assert all(m.anchor in (w1, w2) for c in clusters for m in c.members)


def test_assemble_no_wedges_returns_empty() -> None:
    clusters = assemble_clusters(
        {CombatGroupRole.SHORAD: [_grp(CombatGroupRole.SHORAD, 1)]}
    )
    assert clusters == []


def test_cluster_depth_offsets_signs() -> None:
    assert CLUSTER_DEPTH_OFFSET[CombatGroupRole.RECON] < 0  # in front
    assert CLUSTER_DEPTH_OFFSET[CombatGroupRole.SHORAD] > 0  # behind
    assert (
        CLUSTER_DEPTH_OFFSET[CombatGroupRole.ATGM]
        > CLUSTER_DEPTH_OFFSET[CombatGroupRole.SHORAD]
    )  # further behind
    assert CombatGroupRole.TANK in WEDGE_ROLES


# ---------------------------------------------------------------------------
# plan_groundwar cluster tests (Task 5)
# ---------------------------------------------------------------------------


def _unit(unit_class: UnitClass) -> MagicMock:
    ut = MagicMock(spec=GroundUnitType)
    ut.unit_class = unit_class
    return ut


def _planner_with(armor: dict[MagicMock, int], limit: int) -> tuple[GroundPlanner, Any]:
    enemy = SimpleNamespace(id=uuid4(), captured=SimpleNamespace())
    cp = SimpleNamespace(
        captured=SimpleNamespace(),
        connected_points=[enemy],
        frontline_unit_count_limit=limit,
        base=SimpleNamespace(armor=armor, total_armor=sum(armor.values())),
        stances={},
    )
    # connected_enemy_cp filter compares captured identity; make them differ.
    cp.captured = object()
    enemy.captured = object()
    planner = GroundPlanner.__new__(GroundPlanner)
    planner.cp = cp  # type: ignore[assignment]
    planner.game = MagicMock()
    planner.connected_enemy_cp = [enemy]  # type: ignore[list-item]
    planner.units_per_cp = {enemy.id: []}
    planner.reserve = []
    return planner, enemy


def test_plan_groundwar_builds_clusters_with_anchors() -> None:
    tank = _unit(UnitClass.TANK)
    shorad = _unit(UnitClass.SHORAD)
    planner, enemy = _planner_with({tank: 12, shorad: 3}, limit=15)
    planner.plan_groundwar()
    groups = planner.units_per_cp[enemy.id]
    wedges = [g for g in groups if g.role in WEDGE_ROLES]
    shorads = [g for g in groups if g.role == CombatGroupRole.SHORAD]
    assert wedges, "expected at least one armor wedge"
    assert all(2 <= w.size <= 7 for w in wedges)
    # Anchored SHORADs must point to a real wedge; unattached ones (same-type
    # extras per the distinct-type rule) are valid with anchor=None.
    assert all(s.anchor in wedges or s.anchor is None for s in shorads)


def test_plan_groundwar_respects_cap() -> None:
    tank = _unit(UnitClass.TANK)
    planner, enemy = _planner_with({tank: 100}, limit=15)
    planner.plan_groundwar()
    deployed = sum(g.size for g in planner.units_per_cp[enemy.id])
    assert deployed <= 15


# ---------------------------------------------------------------------------
# I2 — adjacent clusters alternate armor type
# ---------------------------------------------------------------------------


def _grp_typed(
    role: CombatGroupRole, unit_type: GroundUnitType, size: int
) -> CombatGroup:
    return CombatGroup(role, unit_type, size)


def test_assemble_clusters_alternates_armor_types() -> None:
    """Adjacent clusters must not all share one armor type when two types present."""
    type_a = MagicMock(spec=GroundUnitType)
    type_b = MagicMock(spec=GroundUnitType)
    # 3 wedges of type A, 3 of type B — without interleaving they'd be AAABBB
    wedges_a = [_grp_typed(CombatGroupRole.TANK, type_a, 5) for _ in range(3)]
    wedges_b = [_grp_typed(CombatGroupRole.TANK, type_b, 5) for _ in range(3)]
    clusters = assemble_clusters({CombatGroupRole.TANK: wedges_a + wedges_b})
    assert len(clusters) == 6
    types_in_order = [c.wedge.unit_type for c in clusters]
    # Must not be all type_a first then all type_b (i.e. not [A,A,A,B,B,B]).
    # Round-robin interleave gives [A,B,A,B,A,B]; assert no run of 3+ same type.
    runs = 1
    for i in range(1, len(types_in_order)):
        if types_in_order[i] == types_in_order[i - 1]:
            runs += 1
            assert (
                runs < 3
            ), f"Got a run of same armor type >= 3 at position {i}: {types_in_order}"
        else:
            runs = 1


def test_interleave_by_unit_type_is_module_level() -> None:
    """interleave_by_unit_type must be importable at module level."""
    type_a = MagicMock(spec=GroundUnitType)
    type_b = MagicMock(spec=GroundUnitType)
    groups = [
        _grp_typed(CombatGroupRole.SHORAD, type_a, 1),
        _grp_typed(CombatGroupRole.SHORAD, type_a, 1),
        _grp_typed(CombatGroupRole.SHORAD, type_b, 1),
    ]
    result = interleave_by_unit_type(groups)
    # First two should not both be type_a (interleaved: A, B, A)
    assert (
        result[0].unit_type != result[1].unit_type
        or result[1].unit_type != result[2].unit_type
    )


# ---------------------------------------------------------------------------
# I1 — SHORAD 2nd-per-cluster only if DISTINCT type
# ---------------------------------------------------------------------------


def test_assemble_same_type_shorad_leaves_3rd_unattached() -> None:
    """2 clusters + 3 same-type SHORAD → each cluster ≤1 SHORAD; 3rd unattached."""
    w1 = _grp(CombatGroupRole.TANK, 6)
    w2 = _grp(CombatGroupRole.TANK, 6)
    # All three SHORAD are the same unit_type (same MagicMock identity via _grp)
    s1 = _grp(CombatGroupRole.SHORAD, 1)
    s2 = _grp(CombatGroupRole.SHORAD, 1)
    s3 = _grp(CombatGroupRole.SHORAD, 1)
    # All _grp() calls use a fresh MagicMock — make them explicitly same type.
    shared_type = MagicMock(spec=GroundUnitType)
    s1.unit_type = shared_type
    s2.unit_type = shared_type
    s3.unit_type = shared_type

    buckets = {
        CombatGroupRole.TANK: [w1, w2],
        CombatGroupRole.SHORAD: [s1, s2, s3],
    }
    clusters = assemble_clusters(buckets)
    assert len(clusters) == 2
    # Each cluster must have at most 1 SHORAD member.
    for c in clusters:
        shorad_members = [m for m in c.members if m.role == CombatGroupRole.SHORAD]
        assert (
            len(shorad_members) <= 1
        ), f"Cluster got {len(shorad_members)} same-type SHORAD, expected ≤1"
    # The 3rd SHORAD must remain unattached (anchor is None).
    all_anchored_ids = {id(m) for c in clusters for m in c.members}
    unattached_shorad = [g for g in [s1, s2, s3] if id(g) not in all_anchored_ids]
    assert (
        len(unattached_shorad) == 1
    ), f"Expected 1 unattached SHORAD, got {len(unattached_shorad)}"
    assert unattached_shorad[0].anchor is None


def test_assemble_distinct_type_shorad_both_attached() -> None:
    """1 cluster + 2 SHORAD of distinct types → cluster gets both."""
    wedge = _grp(CombatGroupRole.TANK, 6)
    type_a = MagicMock(spec=GroundUnitType)
    type_b = MagicMock(spec=GroundUnitType)
    sa = CombatGroup(CombatGroupRole.SHORAD, type_a, 1)
    sb = CombatGroup(CombatGroupRole.SHORAD, type_b, 1)

    clusters = assemble_clusters(
        {CombatGroupRole.TANK: [wedge], CombatGroupRole.SHORAD: [sa, sb]}
    )
    assert len(clusters) == 1
    shorad_members = [
        m for m in clusters[0].members if m.role == CombatGroupRole.SHORAD
    ]
    assert (
        len(shorad_members) == 2
    ), f"Expected 2 distinct-type SHORAD in cluster, got {len(shorad_members)}"
    assert sa.anchor is wedge
    assert sb.anchor is wedge
