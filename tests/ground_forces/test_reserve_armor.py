from __future__ import annotations

from types import SimpleNamespace
from typing import TYPE_CHECKING, Any, cast
from unittest.mock import MagicMock

import pytest

from game.data.units import UnitClass
from game.dcs.groundunittype import GroundUnitType
from game.ground_forces.ai_ground_planner import (
    GroundPlanner,
    deployable_armor,
    reserve_armor_for,
)
from game.ground_forces.combat_stance import CombatStance
from game.theater.base import Base
from game.theater.player import Player

if TYPE_CHECKING:
    from game.theater import ControlPoint


def _unit(
    unit_class: UnitClass = UnitClass.TANK, variant_id: str = "Test unit"
) -> MagicMock:
    unit = MagicMock(spec=GroundUnitType)
    unit.unit_class = unit_class
    unit.variant_id = variant_id
    unit.price = 5
    return unit


def _cp(armor: dict[MagicMock, int], limit: int, has_enemy: bool) -> ControlPoint:
    # `captured` sentinels MUST be identity-distinct: SimpleNamespace() instances
    # compare EQUAL by content, which would make the `p.captured != cp.captured`
    # enemy gate vacuously false. Use object().
    own = object()
    enemy = SimpleNamespace(captured=object(), id=object(), name="Enemy")
    base = SimpleNamespace(armor=armor, total_armor=sum(armor.values()))
    return cast(
        "ControlPoint",
        SimpleNamespace(
            captured=own,
            connected_points=[enemy] if has_enemy else [],
            frontline_unit_count_limit=limit,
            base=base,
            name="Test CP",
            stances={enemy.id: CombatStance.DEFENSIVE},
        ),
    )


def test_rear_cp_reserves_full_pool() -> None:
    tank = _unit()
    cp = _cp({tank: 12}, limit=8, has_enemy=False)
    assert reserve_armor_for(cp) == {tank: 12}


def test_unknown_unit_class_stays_in_reserve() -> None:
    bogus = _unit()
    bogus.unit_class = object()
    cp = _cp({bogus: 7}, limit=10, has_enemy=True)
    assert deployable_armor(cp) == {}
    assert reserve_armor_for(cp) == {bogus: 7}


def test_reserve_matches_ground_planner_allocation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    alpha = _unit(variant_id="Alpha")
    bravo = _unit(variant_id="Bravo")
    charlie = _unit(variant_id="Charlie")
    armor = {charlie: 1, alpha: 4, bravo: 2}
    cp = _cp(armor, limit=4, has_enemy=True)
    planner = GroundPlanner(cp, cast(Any, SimpleNamespace()))
    monkeypatch.setattr(
        "game.ground_forces.ai_ground_planner.random.choice", lambda values: values[0]
    )

    planner.plan_groundwar()

    planned: dict[GroundUnitType, int] = {}
    for group in planner.tank_groups:
        planned[group.unit_type] = planned.get(group.unit_type, 0) + group.size
    reserve = reserve_armor_for(cp)
    assert planned == {
        unit_type: count - reserve.get(unit_type, 0)
        for unit_type, count in armor.items()
        if count - reserve.get(unit_type, 0) > 0
    }
