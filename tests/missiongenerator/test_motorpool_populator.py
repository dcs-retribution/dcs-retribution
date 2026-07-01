from __future__ import annotations

from types import SimpleNamespace
from typing import TYPE_CHECKING, cast
from unittest.mock import MagicMock

from dcs.mapping import Point
from dcs.terrain import Terrain
from dcs.vehicles import Armor

from game.dcs.groundunittype import GroundUnitType
from game.missiongenerator.motorpoolpopulator import MotorpoolPopulator
from game.theater.controlpoint import ControlPoint
from game.theater.presetlocation import PresetLocation
from game.theater.theatergroundobject import MotorpoolGroundObject
from game.utils import Heading

if TYPE_CHECKING:
    from game.game import Game


def _gut() -> GroundUnitType:
    return next(GroundUnitType.for_dcs_type(Armor.M_1_Abrams))


def _motorpool(
    reserve: dict[GroundUnitType, int],
) -> tuple[MotorpoolGroundObject, ControlPoint]:
    cp = MagicMock(spec=ControlPoint)
    cp.captured = object()
    cp.base = SimpleNamespace(armor=dict(reserve), total_armor=sum(reserve.values()))
    cp.connected_points = []  # rear CP -> reserve == full pool
    cp.name = "CP"
    loc = PresetLocation(
        "G", Point(0.0, 0.0, MagicMock(spec=Terrain)), Heading.from_degrees(0)
    )
    from game.data.groups import GroupTask

    tgo = MotorpoolGroundObject("CP Motorpool 0", loc, cp, GroupTask.MOTORPOOL)
    cp.ground_objects = [tgo]
    return tgo, cp


def _game(cps: list[ControlPoint], cap: int, enabled: bool = True) -> object:
    counter = {"u": 0, "g": 0}

    def next_unit_id() -> int:
        counter["u"] += 1
        return counter["u"]

    def next_group_id() -> int:
        counter["g"] += 1
        return counter["g"]

    return SimpleNamespace(
        theater=SimpleNamespace(controlpoints=cps),
        settings=SimpleNamespace(motorpool_enabled=enabled, motorpool_spawn_cap=cap),
        next_unit_id=next_unit_id,
        next_group_id=next_group_id,
    )


def test_populate_renders_all_when_under_cap() -> None:
    gut = _gut()
    tgo, cp = _motorpool({gut: 4})
    MotorpoolPopulator(cast("Game", _game([cp], cap=10))).populate()
    rendered = sum(len(g.units) for g in tgo.groups)
    assert rendered == 4
    assert tgo.motorpool_unit_types[tgo.groups[0].id] is gut


def test_populate_caps_total() -> None:
    gut = _gut()
    tgo, cp = _motorpool({gut: 25})
    MotorpoolPopulator(cast("Game", _game([cp], cap=10))).populate()
    assert sum(len(g.units) for g in tgo.groups) == 10


def test_populate_empty_when_no_reserve() -> None:
    gut = _gut()
    tgo, cp = _motorpool({gut: 0})
    MotorpoolPopulator(cast("Game", _game([cp], cap=10))).populate()
    assert tgo.groups == []


def test_populate_disabled_renders_nothing() -> None:
    gut = _gut()
    tgo, cp = _motorpool({gut: 5})
    MotorpoolPopulator(cast("Game", _game([cp], cap=10, enabled=False))).populate()
    assert tgo.groups == []


def test_populate_is_idempotent_across_runs() -> None:
    gut = _gut()
    tgo, cp = _motorpool({gut: 3})
    pop = MotorpoolPopulator(cast("Game", _game([cp], cap=10)))
    pop.populate()
    pop.populate()
    assert sum(len(g.units) for g in tgo.groups) == 3  # reset each run, not 6


def test_multiple_motorpools_on_one_cp_share_one_reserve_pool() -> None:
    # Two motorpool TGOs on the same CP must split the single reserve pool, not
    # each render it in full — otherwise a strike decrements base.armor twice per
    # reserve unit. Regression guard for the multi-motorpool double-count bug.
    from game.data.groups import GroupTask

    gut = _gut()
    cp = MagicMock(spec=ControlPoint)
    cp.captured = object()
    cp.base = SimpleNamespace(armor={gut: 6}, total_armor=6)
    cp.connected_points = []
    cp.name = "CP"

    def _loc() -> PresetLocation:
        return PresetLocation(
            "G", Point(0.0, 0.0, MagicMock(spec=Terrain)), Heading.from_degrees(0)
        )

    t1 = MotorpoolGroundObject("CP Motorpool 0", _loc(), cp, GroupTask.MOTORPOOL)
    t2 = MotorpoolGroundObject("CP Motorpool 1", _loc(), cp, GroupTask.MOTORPOOL)
    cp.ground_objects = [t1, t2]

    MotorpoolPopulator(cast("Game", _game([cp], cap=10))).populate()

    total = sum(len(g.units) for tgo in (t1, t2) for g in tgo.groups)
    assert total == 6  # the shared pool, dealt across both — NOT 12
    assert sum(len(g.units) for g in t1.groups) == 3  # round-robin split
    assert sum(len(g.units) for g in t2.groups) == 3
