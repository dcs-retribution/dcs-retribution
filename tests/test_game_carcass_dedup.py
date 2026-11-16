from typing import Union
from unittest.mock import MagicMock

from game.game import Game
from game.spatialindex import LiveUnitIndex


def _carcass(type_name: str, x: float, z: float) -> dict[str, Union[float, str]]:
    return {"x": x, "y": 0.0, "z": z, "type": type_name, "orientation": 0.0}


def _bare_game(on_land: bool = True) -> Game:
    # Game.__new__ skips heavy __init__; we only exercise the carcass paths.
    game = Game.__new__(Game)
    game._Game__destroyed_units = []  # type: ignore[attr-defined]
    theater = MagicMock()
    theater.is_on_land.return_value = on_land
    game.theater = theater
    return game


def test_carcass_key_same_type_and_position_are_equal() -> None:
    a = Game._carcass_key(_carcass("Garage_A", 100.0, 200.0))
    b = Game._carcass_key(_carcass("Garage_A", 100.0, 200.0))
    assert a == b


def test_carcass_key_distinct_position_differs() -> None:
    a = Game._carcass_key(_carcass("Garage_A", 100.0, 200.0))
    b = Game._carcass_key(_carcass("Garage_A", 100.0, 260.0))
    assert a != b


def test_carcass_key_distinct_type_differs() -> None:
    # FARP fuel vs ammo can sit within metres of each other — must not merge.
    a = Game._carcass_key(_carcass("FARP_Fuel_Depot", 100.0, 200.0))
    b = Game._carcass_key(_carcass("FARP_Ammo_Dump_Coating", 100.0, 200.0))
    assert a != b


def test_carcass_key_quantizes_submetre_jitter() -> None:
    a = Game._carcass_key(_carcass("Garage_A", 100.0, 200.0))
    b = Game._carcass_key(_carcass("Garage_A", 100.4, 199.6))
    assert a == b


def test_add_destroyed_units_dedups_same_type_position() -> None:
    game = _bare_game()
    game.add_destroyed_units(_carcass("Garage_A", 100.0, 200.0))
    game.add_destroyed_units(_carcass("Garage_A", 100.0, 200.0))
    assert len(game.get_destroyed_units()) == 1


def test_add_destroyed_units_keeps_distinct_positions() -> None:
    game = _bare_game()
    game.add_destroyed_units(_carcass("Garage_A", 100.0, 200.0))
    game.add_destroyed_units(_carcass("Garage_A", 100.0, 260.0))
    assert len(game.get_destroyed_units()) == 2


def test_add_destroyed_units_skips_offland() -> None:
    game = _bare_game(on_land=False)
    game.add_destroyed_units(_carcass("Garage_A", 100.0, 200.0))
    assert len(game.get_destroyed_units()) == 0


def test_dedup_destroyed_units_collapses_and_keeps_first() -> None:
    game = _bare_game()
    first = _carcass("Garage_A", 100.0, 200.0)
    dup = _carcass("Garage_A", 100.3, 200.2)  # same 1 m cell
    other = _carcass("FARP_Fuel_Depot", 500.0, 600.0)
    game._Game__destroyed_units = [first, dup, other]  # type: ignore[attr-defined]
    game._dedup_destroyed_units()
    result = game.get_destroyed_units()
    assert result == [first, other]  # first occurrence kept, order preserved


def test_dedup_destroyed_units_keeps_unkeyable_entries() -> None:
    game = _bare_game()
    bad: dict[str, Union[float, str]] = {"y": 0.0, "type": "Garage_A"}  # no x/z
    game._Game__destroyed_units = [bad]  # type: ignore[attr-defined]
    game._dedup_destroyed_units()
    assert game.get_destroyed_units() == [bad]


def test_add_destroyed_units_survives_unkeyable_entry_in_list() -> None:
    # An unkeyable legacy entry (no x/z) that _dedup preserves must not make the
    # next insert's dedup scan raise KeyError.
    game = _bare_game()
    bad: dict[str, Union[float, str]] = {"y": 0.0, "type": "Garage_A"}  # no x/z
    game._Game__destroyed_units = [bad]  # type: ignore[attr-defined]
    game.add_destroyed_units(_carcass("Garage_A", 100.0, 200.0))
    assert len(game.get_destroyed_units()) == 2  # bad kept, new one appended


def test_safe_carcass_key_none_on_inf_coord() -> None:
    # round(inf) raises OverflowError (not ValueError): must be caught -> None.
    assert Game._safe_carcass_key(_carcass("Garage_A", float("inf"), 0.0)) is None


def test_dedup_destroyed_units_survives_inf_coord() -> None:
    game = _bare_game()
    inf_entry = _carcass("Garage_A", float("inf"), 0.0)
    game._Game__destroyed_units = [inf_entry]  # type: ignore[attr-defined]
    game._dedup_destroyed_units()  # must not raise OverflowError
    assert game.get_destroyed_units() == [inf_entry]  # kept as unkeyable


def test_add_destroyed_units_survives_inf_coord_incoming() -> None:
    game = _bare_game()
    game.add_destroyed_units(_carcass("Garage_A", float("inf"), 0.0))  # no crash
    assert len(game.get_destroyed_units()) == 1


def test_prune_removes_carcass_under_live_unit() -> None:
    game = _bare_game()
    on = _carcass("Garage_A", 100.0, 200.0)
    off = _carcass("Garage_A", 100.0, 400.0)
    game._Game__destroyed_units = [on, off]  # type: ignore[attr-defined]
    game.prune_destroyed_units(LiveUnitIndex([(101.0, 201.0)], 5.0))
    assert game.get_destroyed_units() == [off]  # 'on' pruned, 'off' kept


def test_prune_empty_index_keeps_all() -> None:
    game = _bare_game()
    items = [_carcass("Garage_A", 100.0, 200.0)]
    game._Game__destroyed_units = list(items)  # type: ignore[attr-defined]
    game.prune_destroyed_units(LiveUnitIndex([], 5.0))
    assert game.get_destroyed_units() == items


def test_prune_keeps_garbled_coord_carcass() -> None:
    game = _bare_game()
    bad: dict[str, Union[float, str]] = {"y": 0.0, "type": "Garage_A"}  # no x/z
    game._Game__destroyed_units = [bad]  # type: ignore[attr-defined]
    game.prune_destroyed_units(LiveUnitIndex([(0.0, 0.0)], 5.0))
    assert game.get_destroyed_units() == [bad]  # unmatchable -> kept


def test_prune_survives_inf_coord_carcass() -> None:
    # math.floor(inf / radius) raises OverflowError (not ValueError): must be
    # caught so an inf-coord carcass is kept, not crashing mission generation.
    game = _bare_game()
    inf_entry = _carcass("Garage_A", float("inf"), 0.0)
    game._Game__destroyed_units = [inf_entry]  # type: ignore[attr-defined]
    game.prune_destroyed_units(LiveUnitIndex([(0.0, 0.0)], 5.0))  # must not raise
    assert game.get_destroyed_units() == [inf_entry]  # unmatchable -> kept
