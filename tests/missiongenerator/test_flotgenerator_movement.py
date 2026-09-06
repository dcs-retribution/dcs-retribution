from dcs.point import PointAction

from game.ground_forces.ai_ground_planner import CombatGroupRole
from game.ground_forces.combat_stance import CombatStance
from game.missiongenerator.flotgenerator import (
    AGGRESIVE_MOVE_DISTANCE,
    BREAKTHROUGH_OFFENSIVE_DISTANCE,
    follower_advance_distance,
    move_formation_for_role,
)


def test_aggressive_and_elimination_advance_the_wedge_distance() -> None:
    # Anchored members keep up with an attacking/advancing wedge.
    assert follower_advance_distance(CombatStance.AGGRESSIVE) == AGGRESIVE_MOVE_DISTANCE
    assert (
        follower_advance_distance(CombatStance.ELIMINATION) == AGGRESIVE_MOVE_DISTANCE
    )


def test_breakthrough_advances_the_full_breakthrough_distance() -> None:
    # Must match the wedge's 35 km push or the cluster splits apart.
    assert (
        follower_advance_distance(CombatStance.BREAKTHROUGH)
        == BREAKTHROUGH_OFFENSIVE_DISTANCE
    )


def test_hold_and_static_stances_produce_no_advance() -> None:
    # DEFENSIVE/AMBUSH hold in place; RETREAT is handled by the universal
    # fallback block in plan_action_for_groups, not here.
    assert follower_advance_distance(CombatStance.DEFENSIVE) is None
    assert follower_advance_distance(CombatStance.AMBUSH) is None
    assert follower_advance_distance(CombatStance.RETREAT) is None


def test_armor_wedge_roles_get_vee() -> None:
    for role in (CombatGroupRole.TANK, CombatGroupRole.IFV, CombatGroupRole.APC):
        assert move_formation_for_role(role) == PointAction.Vee


def test_atgm_gets_line_abreast() -> None:
    # pydcs LineAbreast serialises to the DCS "Rank" formation.
    assert move_formation_for_role(CombatGroupRole.ATGM) == PointAction.LineAbreast


def test_other_roles_keep_the_default() -> None:
    # None => caller leaves the vehicle_group OffRoad default (recon scatter,
    # single-unit SHORAD, artillery, logi).
    for role in (
        CombatGroupRole.RECON,
        CombatGroupRole.SHORAD,
        CombatGroupRole.ARTILLERY,
        CombatGroupRole.LOGI,
    ):
        assert move_formation_for_role(role) is None
