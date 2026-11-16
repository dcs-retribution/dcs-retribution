from __future__ import annotations

from types import SimpleNamespace
from typing import TYPE_CHECKING, cast
from unittest.mock import MagicMock

from game.data.units import UnitClass
from game.dcs.groundunittype import GroundUnitType
from game.ground_forces.ai_ground_planner import deployable_armor, reserve_armor_for

if TYPE_CHECKING:
    from game.theater import ControlPoint


def _unit(unit_class: UnitClass = UnitClass.TANK) -> MagicMock:
    u = MagicMock(spec=GroundUnitType)
    u.unit_class = unit_class
    return u


def _cp(armor: dict[MagicMock, int], limit: int, has_enemy: bool) -> ControlPoint:
    # `captured` sentinels MUST be identity-distinct: SimpleNamespace() instances
    # compare EQUAL by content, which would make the `p.captured != cp.captured`
    # enemy gate vacuously false. Use object().
    own = object()
    enemy = SimpleNamespace(captured=object())
    base = SimpleNamespace(armor=armor, total_armor=sum(armor.values()))
    return cast(
        "ControlPoint",
        SimpleNamespace(
            captured=own,
            connected_points=[enemy] if has_enemy else [],
            frontline_unit_count_limit=limit,
            base=base,
        ),
    )


def test_rear_cp_reserves_full_pool() -> None:
    tank = _unit()
    cp = _cp({tank: 12}, limit=8, has_enemy=False)
    assert reserve_armor_for(cp) == {tank: 12}
    assert deployable_armor(cp) == {tank: 8}  # helper itself has no enemy gate


def test_front_cp_single_type_clamped_to_limit() -> None:
    tank = _unit()
    cp = _cp({tank: 12}, limit=8, has_enemy=True)
    # ratio = 8/12; available = 12 * 8/12 = 8.0 -> round -> 8; deployed 8, reserve 4.
    assert deployable_armor(cp) == {tank: 8}
    assert reserve_armor_for(cp) == {tank: 4}


def test_deploy_all_leaves_no_reserve() -> None:
    tank = _unit()
    cp = _cp({tank: 5}, limit=100, has_enemy=True)  # ratio capped at 1 -> deploy all 5
    assert deployable_armor(cp) == {tank: 5}
    assert reserve_armor_for(cp) == {}


def test_unknown_unit_class_is_never_deployed() -> None:
    # A class not in the deployable set is skipped by plan_groundwar -> 0 deployed,
    # fully reserve, and does NOT consume the limit.
    # Build an explicit unknown class: pick a UnitClass NOT handled by the chain.
    # The chain handles TANK, APC, ARTILLERY, IFV, LOGISTICS, ATGM, SHORAD, AAA, RECON.
    # If no other UnitClass member exists, assert via a MagicMock unit_class sentinel
    # that is not in _DEPLOYABLE_UNIT_CLASSES.
    from game.ground_forces.ai_ground_planner import _DEPLOYABLE_UNIT_CLASSES

    bogus = MagicMock(spec=GroundUnitType)
    bogus.unit_class = object()  # definitely not in the deployable set
    assert bogus.unit_class not in _DEPLOYABLE_UNIT_CLASSES
    cp = _cp({bogus: 7}, limit=10, has_enemy=True)
    assert deployable_armor(cp) == {}
    assert reserve_armor_for(cp) == {bogus: 7}


def test_sequential_decrement_and_break_order_dependent() -> None:
    # Two TANK types, limit 6. dict order is insertion order. ratio = 6/10 = 0.6.
    # type a: 6*0.6=3.6 -> round -> 4 (banker's: round(3.6)=4); remaining 6-4=2.
    # type b: 4*0.6=2.4 -> round -> 2; clamp not needed (2<=2); remaining 0; deployed.
    a, b = _unit(), _unit()
    cp = _cp({a: 6, b: 4}, limit=6, has_enemy=True)
    deployed = deployable_armor(cp)
    assert deployed == {a: 4, b: 2}
    assert sum(deployed.values()) == 6
    assert reserve_armor_for(cp) == {a: 2, b: 2}
