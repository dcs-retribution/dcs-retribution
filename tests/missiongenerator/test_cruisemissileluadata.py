"""Cruise-missile emitter (dcsRetribution.cruiseMissiles).

Locks the shape the ``cruisemissiles`` plugin consumes: every live LACM ship group
with missiles left emits ``group``/``coalition``/``remaining`` (the mission's hard
expenditure cap), the planned auto raids ride under ``raids``, and the node is
absent entirely when the master setting is off or no launching group exists.
"""

from __future__ import annotations

import math
from types import SimpleNamespace
from typing import Any

from game.cruisemissiles import LACM_MAGAZINE_BY_TYPE
from game.missiongenerator.cruisemissileluadata import populate_cruise_missiles_lua
from game.missiongenerator.luagenerator import LuaData, LuaValue
from game.theater import Player

BURKE = "USS_Arleigh_Burke_IIa"
KARAKURT = "CH_Karakurt_LACM"


def _kv(item: Any) -> dict[str, Any]:
    vals = item.value
    if isinstance(vals, LuaValue):
        vals = [vals]
    return {v.key: v.value for v in vals}


class _Pos:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def distance_to_point(self, other: "_Pos") -> float:
        return math.hypot(self.x - other.x, self.y - other.y)


def _ship_tgo(owner_cp: Any, group_name: str, type_id: str, pos: _Pos) -> Any:
    units = [SimpleNamespace(alive=True, type=SimpleNamespace(id=type_id))]
    return SimpleNamespace(
        category="ship",
        name=group_name,
        position=pos,
        control_point=owner_cp,
        groups=[SimpleNamespace(group_name=group_name, units=units)],
        units=units,
        is_control_point=False,
    )


def _target_tgo(name: str, category: str, pos: _Pos) -> Any:
    units = [SimpleNamespace(alive=True, type=SimpleNamespace(id="Generator"))]
    return SimpleNamespace(
        category=category,
        name=name,
        position=pos,
        groups=[SimpleNamespace(group_name=name, units=units)],
        units=units,
        is_control_point=False,
    )


def _game(*, master: bool = True, auto: bool = False, with_target: bool = False) -> Any:
    blue_cp = SimpleNamespace(captured=Player.BLUE, ground_objects=[])
    blue_cp.ground_objects.append(
        _ship_tgo(blue_cp, "CVBG | Burke", BURKE, _Pos(0.0, 0.0))
    )
    red_cp = SimpleNamespace(captured=Player.RED, ground_objects=[])
    red_cp.ground_objects.append(
        _ship_tgo(red_cp, "Red Corvette", KARAKURT, _Pos(100_000.0, 0.0))
    )
    if with_target:
        red_cp.ground_objects.append(
            _target_tgo("Division HQ", "commandcenter", _Pos(60_000.0, 0.0))
        )
    return SimpleNamespace(
        theater=SimpleNamespace(controlpoints=[blue_cp, red_cp]),
        settings=SimpleNamespace(
            cruise_missile_strikes=master,
            cruise_missile_auto_raids=auto,
        ),
    )


def _node(game: Any) -> Any:
    root = LuaData("dcsRetribution")
    populate_cruise_missiles_lua(root, game, mission_data=None)  # type: ignore[arg-type]
    return root.get_item("cruiseMissiles")


def _records(node: Any, key: str) -> list[dict[str, Any]]:
    item = node.get_item(key)
    if item is None:
        return []
    assert isinstance(item, LuaData)
    return [_kv(rec) for rec in item.objects]


def test_emits_each_live_lacm_group_with_its_magazine() -> None:
    node = _node(_game())
    assert node is not None
    ships = _records(node, "ships")
    assert {s["group"]: (s["coalition"], s["remaining"]) for s in ships} == {
        "CVBG | Burke": ("blue", str(LACM_MAGAZINE_BY_TYPE[BURKE])),
        "Red Corvette": ("red", str(LACM_MAGAZINE_BY_TYPE[KARAKURT])),
    }
    # No auto-raid toggle -> no raids list at all.
    assert _records(node, "raids") == []


def test_emits_the_planned_auto_raid() -> None:
    node = _node(_game(auto=True, with_target=True))
    assert node is not None
    raids = _records(node, "raids")
    # One target in reach (red's corvette has no blue ground target: ships are
    # excluded), so exactly the blue raid emits.
    assert len(raids) == 1
    raid = raids[0]
    assert raid["group"] == "CVBG | Burke"
    assert raid["coalition"] == "blue"
    assert raid["target"] == "Division HQ"
    assert raid["x"] == "60000.0" and raid["y"] == "0.0"
    assert raid["count"] == "6"


def test_no_node_when_the_setting_is_off() -> None:
    assert _node(_game(master=False)) is None


def test_no_node_without_a_live_launching_group() -> None:
    game = _game()
    for cp in game.theater.controlpoints:
        for tgo in cp.ground_objects:
            for unit in tgo.units:
                unit.alive = False
    assert _node(game) is None
