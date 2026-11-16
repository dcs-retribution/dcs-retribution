"""Tests that motorpool losses are tracked separately from front-line losses.

Decision: motorpool kills must decrement base.armor 1:1 but must NOT count
as front-line losses, so depot strikes do not shift the front-line via
casualty_count / commit_front_line_battle_impact.
"""

from __future__ import annotations

from unittest.mock import MagicMock

from dcs.vehicles import Armor

from game.dcs.groundunittype import GroundUnitType
from game.debriefing import GroundLosses
from game.unitmap import FrontLineUnit, UnitMap


def _gut() -> GroundUnitType:
    return next(GroundUnitType.for_dcs_type(Armor.M_1_Abrams))


def test_motorpool_losses_appear_in_motorpool_list_not_front_line() -> None:
    """GroundLosses with a motorpool entry: motorpool_losses yields it,
    player_front_line and enemy_front_line remain empty."""
    gut = _gut()
    cp = MagicMock()

    flu = FrontLineUnit(gut, cp)
    gl = GroundLosses(player_motorpool=[flu])

    assert list(gl.player_motorpool) == [flu]
    assert list(gl.enemy_motorpool) == []
    assert list(gl.player_front_line) == []
    assert list(gl.enemy_front_line) == []


def test_unitmap_motorpool_and_front_line_are_distinct_registries() -> None:
    """A unit registered via add_motorpool_units is not visible as a
    front_line_unit, and vice-versa — the two registries are independent."""
    gut = _gut()
    cp = MagicMock()

    from types import SimpleNamespace

    unit_map = UnitMap()
    mp_group = SimpleNamespace(units=[SimpleNamespace(name="mp-001")])
    fl_group = SimpleNamespace(units=[SimpleNamespace(name="fl-001")])

    unit_map.add_motorpool_units(mp_group, cp, gut)  # type: ignore[arg-type]
    unit_map.add_front_line_units(fl_group, cp, gut)  # type: ignore[arg-type]

    # motorpool unit visible only in motorpool_unit
    assert unit_map.motorpool_unit("mp-001") is not None
    assert unit_map.front_line_unit("mp-001") is None

    # front-line unit visible only in front_line_unit
    assert unit_map.front_line_unit("fl-001") is not None
    assert unit_map.motorpool_unit("fl-001") is None
