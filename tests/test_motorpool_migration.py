from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock

from dcs.mapping import Point
from dcs.terrain import Terrain

from game.migrator import Migrator
from game.theater.presetlocation import PresetLocation
from game.theater.theatergroundobject import MotorpoolGroundObject
from game.utils import Heading


def _loc() -> PresetLocation:
    return PresetLocation(
        "G", Point(0.0, 0.0, MagicMock(spec=Terrain)), Heading.from_degrees(0)
    )


def _migrator_with(cp: object, enabled: bool = True) -> Migrator:
    game = SimpleNamespace(
        theater=SimpleNamespace(controlpoints=[cp]),
        settings=SimpleNamespace(motorpool_enabled=enabled),
    )
    m = Migrator.__new__(Migrator)
    m.game = game  # type: ignore[assignment]
    return m


def test_injects_tgo_for_authored_cp_without_one() -> None:
    cp = MagicMock()
    cp.name = "CP"
    cp.preset_locations = SimpleNamespace(motorpools=[_loc()])
    cp.connected_objectives = []
    cp.ground_objects = []
    m = _migrator_with(cp)
    m._ensure_motorpool_tgos()
    assert any(isinstance(o, MotorpoolGroundObject) for o in cp.connected_objectives)


def test_no_injection_without_authored_locations() -> None:
    cp = MagicMock()
    cp.preset_locations = SimpleNamespace(motorpools=[])
    cp.connected_objectives = []
    cp.ground_objects = []
    m = _migrator_with(cp)
    m._ensure_motorpool_tgos()
    assert cp.connected_objectives == []


def test_no_double_injection_when_tgo_exists() -> None:
    cp = MagicMock()
    cp.name = "CP"
    cp.preset_locations = SimpleNamespace(motorpools=[_loc()])
    existing = MotorpoolGroundObject("CP Motorpool 0", _loc(), cp, None)
    cp.connected_objectives = [existing]
    cp.ground_objects = [existing]
    m = _migrator_with(cp)
    m._ensure_motorpool_tgos()
    pools = [o for o in cp.connected_objectives if isinstance(o, MotorpoolGroundObject)]
    assert len(pools) == 1
