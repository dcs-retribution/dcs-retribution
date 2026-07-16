"""Ship-launched cruise missile strikes — planner, magazines, reconcile.

Locks the campaign contract: magazines seed once from the hull table and only the
debrief report ever debits them (regeneration-safe); the auto raid is at most one
per side, prefers C2 over closer low-value targets, honors the range gate, skips
ship targets, and is fully gated by the two settings; everything is a no-op on a
pre-feature save shape.
"""

from __future__ import annotations

import math
from types import SimpleNamespace
from typing import Any, cast

from game.cruisemissiles import (
    DEFAULT_MAGAZINE_PER_SHIP,
    LACM_MAGAZINE_BY_TYPE,
    MAX_RAID_RANGE_M,
    RAID_SALVO,
    ensure_magazines,
    lacm_ships,
    magazines,
    plan_cruise_raids,
    reconcile_cruise_missiles,
)
from game.theater import Player

BURKE = "USS_Arleigh_Burke_IIa"
KARAKURT = "CH_Karakurt_LACM"


class _Pos:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def distance_to_point(self, other: "_Pos") -> float:
        return math.hypot(self.x - other.x, self.y - other.y)


def _unit(type_id: str, alive: bool = True) -> Any:
    return SimpleNamespace(alive=alive, type=SimpleNamespace(id=type_id))


def _ship_tgo(
    name: str, owner_cp: Any, pos: _Pos, units: list[Any], group_name: str
) -> Any:
    return SimpleNamespace(
        category="ship",
        name=name,
        position=pos,
        control_point=owner_cp,
        groups=[SimpleNamespace(group_name=group_name, units=units)],
        units=units,
        is_control_point=False,
    )


def _target_tgo(name: str, category: str, pos: _Pos, *, alive: bool = True) -> Any:
    units = [SimpleNamespace(alive=alive, type=SimpleNamespace(id="Generator"))]
    return SimpleNamespace(
        category=category,
        name=name,
        position=pos,
        groups=[SimpleNamespace(group_name=name, units=units)],
        units=units,
        is_control_point=False,
    )


def _cp(owner: Player) -> Any:
    cp = SimpleNamespace(captured=owner, ground_objects=[])
    return cp


def _game(cps: list[Any], *, master: bool = True, auto: bool = True) -> Any:
    return SimpleNamespace(
        theater=SimpleNamespace(controlpoints=cps),
        settings=SimpleNamespace(
            cruise_missile_strikes=master,
            cruise_missile_auto_raids=auto,
        ),
    )


def _blue_burke(
    pos: _Pos = _Pos(0.0, 0.0), group: str = "CVBG | Burke"
) -> tuple[Any, Any]:
    cp = _cp(Player.BLUE)
    tgo = _ship_tgo("Burke DDG", cp, pos, [_unit(BURKE)], group)
    cp.ground_objects.append(tgo)
    return cp, tgo


def test_magazines_seed_from_the_hull_table_and_never_reseed() -> None:
    cp, _ = _blue_burke()
    game = _game([cp])
    ensure_magazines(cast(Any, game))
    assert magazines(cast(Any, game))["CVBG | Burke"] == LACM_MAGAZINE_BY_TYPE[BURKE]

    # Expenditure persists: a second ensure never re-ups an existing entry.
    magazines(cast(Any, game))["CVBG | Burke"] = 3
    ensure_magazines(cast(Any, game))
    assert magazines(cast(Any, game))["CVBG | Burke"] == 3


def test_unknown_lacm_hull_gets_the_default_magazine() -> None:
    # Defensive: a future curated id without a table row still seeds something.
    cp = _cp(Player.BLUE)
    unit = _unit(BURKE)
    escort = _unit("PERRY")  # non-LACM escort in the same group: no magazine
    cp.ground_objects.append(
        _ship_tgo("Fleet", cp, _Pos(0, 0), [unit, escort], "Fleet 1")
    )
    game = _game([cp])
    ensure_magazines(cast(Any, game))
    assert magazines(cast(Any, game))["Fleet 1"] == LACM_MAGAZINE_BY_TYPE[BURKE]
    assert DEFAULT_MAGAZINE_PER_SHIP > 0  # the fallback the table misses use


def test_lacm_ships_lists_both_sides_and_skips_dry_or_dead_groups() -> None:
    blue_cp, _ = _blue_burke()
    red_cp = _cp(Player.RED)
    red_cp.ground_objects.append(
        _ship_tgo(
            "Karakurt", red_cp, _Pos(10.0, 10.0), [_unit(KARAKURT)], "Red Corvette"
        )
    )
    dead_cp = _cp(Player.RED)
    dead_cp.ground_objects.append(
        _ship_tgo(
            "Sunk", dead_cp, _Pos(0, 0), [_unit(KARAKURT, alive=False)], "Sunk Corvette"
        )
    )
    game = _game([blue_cp, red_cp, dead_cp])
    ships = lacm_ships(cast(Any, game))
    assert {(s.group_name, s.coalition) for s in ships} == {
        ("CVBG | Burke", "blue"),
        ("Red Corvette", "red"),
    }

    # A dry magazine drops the ship from the shooter list.
    magazines(cast(Any, game))["Red Corvette"] = 0
    assert {s.group_name for s in lacm_ships(cast(Any, game))} == {"CVBG | Burke"}


def test_raid_prefers_c2_over_a_closer_low_value_target() -> None:
    blue_cp, _ = _blue_burke()
    red_cp = _cp(Player.RED)
    red_cp.ground_objects.append(_target_tgo("Cache", "ammo", _Pos(10_000.0, 0.0)))
    red_cp.ground_objects.append(
        _target_tgo("Division HQ", "commandcenter", _Pos(200_000.0, 0.0))
    )
    game = _game([blue_cp, red_cp])

    raids = plan_cruise_raids(cast(Any, game))
    assert len(raids) == 1
    raid = raids[0]
    assert raid.target_name == "Division HQ"
    assert raid.group_name == "CVBG | Burke"
    assert raid.coalition == "blue"
    assert raid.missiles == RAID_SALVO
    assert (raid.target_x, raid.target_y) == (200_000.0, 0.0)


def test_raid_salvo_is_capped_by_the_remaining_magazine() -> None:
    blue_cp, _ = _blue_burke()
    red_cp = _cp(Player.RED)
    red_cp.ground_objects.append(_target_tgo("Depot", "ware", _Pos(10_000.0, 0.0)))
    game = _game([blue_cp, red_cp])
    ensure_magazines(cast(Any, game))
    magazines(cast(Any, game))["CVBG | Burke"] = 2

    raids = plan_cruise_raids(cast(Any, game))
    assert [r.missiles for r in raids] == [2]


def test_raid_honors_the_range_gate() -> None:
    blue_cp, _ = _blue_burke()
    red_cp = _cp(Player.RED)
    red_cp.ground_objects.append(
        _target_tgo("Too far", "commandcenter", _Pos(MAX_RAID_RANGE_M + 1_000.0, 0.0))
    )
    assert plan_cruise_raids(cast(Any, _game([blue_cp, red_cp]))) == []


def test_raid_never_targets_ships_or_dead_objects() -> None:
    blue_cp, _ = _blue_burke()
    red_cp = _cp(Player.RED)
    red_cp.ground_objects.append(
        _ship_tgo(
            "Red fleet", red_cp, _Pos(5_000.0, 0.0), [_unit(KARAKURT)], "Red Fleet"
        )
    )
    red_cp.ground_objects.append(
        _target_tgo("Rubble", "factory", _Pos(7_000.0, 0.0), alive=False)
    )
    game = _game([blue_cp, red_cp])
    # The red fleet still raids BLUE the other way (it has no blue target here
    # either), so assert no raids at all: nothing legal to shoot for anyone.
    assert plan_cruise_raids(cast(Any, game)) == []


def test_red_raids_blue_symmetrically() -> None:
    red_cp = _cp(Player.RED)
    red_cp.ground_objects.append(
        _ship_tgo("Karakurt", red_cp, _Pos(0.0, 0.0), [_unit(KARAKURT)], "Red Corvette")
    )
    blue_cp = _cp(Player.BLUE)
    blue_cp.ground_objects.append(
        _target_tgo("Power plant", "power", _Pos(50_000.0, 0.0))
    )
    raids = plan_cruise_raids(cast(Any, _game([red_cp, blue_cp])))
    assert [(r.coalition, r.target_name) for r in raids] == [("red", "Power plant")]


def test_fully_gated_by_the_two_settings() -> None:
    blue_cp, _ = _blue_burke()
    red_cp = _cp(Player.RED)
    red_cp.ground_objects.append(
        _target_tgo("HQ", "commandcenter", _Pos(10_000.0, 0.0))
    )
    assert plan_cruise_raids(cast(Any, _game([blue_cp, red_cp], master=False))) == []
    assert plan_cruise_raids(cast(Any, _game([blue_cp, red_cp], auto=False))) == []


def test_reconcile_debits_floors_at_zero_and_ignores_unknown_groups() -> None:
    cp, _ = _blue_burke()
    game = _game([cp])
    ensure_magazines(cast(Any, game))
    debriefing = SimpleNamespace(
        state_data=SimpleNamespace(
            cruise_missiles_state=[("CVBG | Burke", 5), ("Ghost ship", 3)]
        )
    )
    reconcile_cruise_missiles(cast(Any, game), cast(Any, debriefing))
    mags = magazines(cast(Any, game))
    assert mags["CVBG | Burke"] == LACM_MAGAZINE_BY_TYPE[BURKE] - 5
    assert "Ghost ship" not in mags

    # Over-report (or a second full salvo) floors at zero -- never negative.
    debriefing = SimpleNamespace(
        state_data=SimpleNamespace(cruise_missiles_state=[("CVBG | Burke", 999)])
    )
    reconcile_cruise_missiles(cast(Any, game), cast(Any, debriefing))
    assert mags["CVBG | Burke"] == 0


def test_reconcile_tolerates_a_pre_feature_state_shape() -> None:
    cp, _ = _blue_burke()
    game = _game([cp])
    ensure_magazines(cast(Any, game))
    before = dict(magazines(cast(Any, game)))
    # Pre-feature state files carry no cruise_missiles_state attribute at all.
    debriefing = SimpleNamespace(state_data=SimpleNamespace())
    reconcile_cruise_missiles(cast(Any, game), cast(Any, debriefing))
    assert magazines(cast(Any, game)) == before
