from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock

from dcs.mapping import Point
from dcs.terrain import Terrain

from game.theater.controlpoint import ControlPoint, PresetLocations
from game.theater.presetlocation import PresetLocation
from game.theater.start_generator import AirbaseGroundObjectGenerator
from game.theater.theatergroundobject import MotorpoolGroundObject
from game.utils import Heading


def _generator(
    motorpool_locations: list[PresetLocation], enabled: bool
) -> tuple[AirbaseGroundObjectGenerator, ControlPoint]:
    cp = MagicMock(spec=ControlPoint)
    cp.name = "Test CP"
    cp.connected_objectives = []
    cp.preset_locations = PresetLocations(motorpools=motorpool_locations)
    game = SimpleNamespace(settings=SimpleNamespace(motorpool_enabled=enabled))
    gen = AirbaseGroundObjectGenerator.__new__(AirbaseGroundObjectGenerator)
    gen.control_point = cp
    gen.game = game  # type: ignore[assignment]
    return gen, cp


def _loc() -> PresetLocation:
    return PresetLocation(
        "Garage", Point(0.0, 0.0, MagicMock(spec=Terrain)), Heading.from_degrees(0)
    )


def test_generate_motorpools_creates_empty_tgo() -> None:
    gen, cp = _generator([_loc()], enabled=True)
    gen.generate_motorpools()
    pools = [o for o in cp.connected_objectives if isinstance(o, MotorpoolGroundObject)]
    assert len(pools) == 1
    assert pools[0].groups == []


def test_generate_motorpools_skipped_when_disabled() -> None:
    gen, cp = _generator([_loc()], enabled=False)
    gen.generate_motorpools()
    assert cp.connected_objectives == []


def test_generate_motorpools_noop_without_authored_locations() -> None:
    gen, cp = _generator([], enabled=True)
    gen.generate_motorpools()
    assert cp.connected_objectives == []
