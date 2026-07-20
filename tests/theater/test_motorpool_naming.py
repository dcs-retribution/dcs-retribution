from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from dcs.mapping import Point
from dcs.terrain import Terrain

from game.migrator import Migrator
from game.naming import namegen
from game.theater.presetlocation import PresetLocation
from game.theater.start_generator import AirbaseGroundObjectGenerator
from game.theater.theatergroundobject import MotorpoolGroundObject
from game.utils import Heading


def _loc() -> PresetLocation:
    return PresetLocation(
        "G", Point(0.0, 0.0, MagicMock(spec=Terrain)), Heading.from_degrees(0)
    )


def _cp() -> MagicMock:
    cp = MagicMock()
    cp.name = "CP"
    cp.preset_locations = SimpleNamespace(motorpools=[_loc()])
    cp.connected_objectives = []
    cp.ground_objects = []
    return cp


def test_start_generator_names_motorpool_with_codename(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # A motorpool should get a codename like every other TGO, not "<CP> Motorpool i".
    monkeypatch.setattr(namegen, "random_objective_name", lambda: "JAGUAR")
    cp = _cp()
    gen = AirbaseGroundObjectGenerator.__new__(AirbaseGroundObjectGenerator)
    gen.game = SimpleNamespace(  # type: ignore[assignment]
        settings=SimpleNamespace(motorpool_enabled=True)
    )
    gen.control_point = cp
    gen.generate_motorpools()
    pools = [o for o in cp.connected_objectives if isinstance(o, MotorpoolGroundObject)]
    assert pools[0].name == "JAGUAR"


def test_migrator_backfills_motorpool_with_codename(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(namegen, "random_objective_name", lambda: "JAGUAR")
    cp = _cp()
    game = SimpleNamespace(
        theater=SimpleNamespace(controlpoints=[cp]),
        settings=SimpleNamespace(motorpool_enabled=True),
    )
    m = Migrator.__new__(Migrator)
    m.game = game  # type: ignore[assignment]
    m._ensure_motorpool_tgos()
    pools = [o for o in cp.connected_objectives if isinstance(o, MotorpoolGroundObject)]
    assert pools[0].name == "JAGUAR"
