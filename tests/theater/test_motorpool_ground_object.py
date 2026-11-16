from __future__ import annotations

from unittest.mock import MagicMock

from dcs.mapping import Point
from dcs.terrain import Terrain

from game.dcs.aircrafttype import AircraftType  # noqa: F401  (ensures registries load)
from game.sidc import SymbolSet
from game.theater.controlpoint import ControlPoint
from game.theater.presetlocation import PresetLocation
from game.theater.theatergroundobject import (
    NAME_BY_CATEGORY,
    MotorpoolGroundObject,
)
from game.utils import Heading


def _location() -> PresetLocation:
    terrain = MagicMock(spec=Terrain)
    point = Point(0.0, 0.0, terrain)
    return PresetLocation("Test Garage", point, Heading.from_degrees(0))


def _motorpool(captured_is_blue: bool = True) -> MotorpoolGroundObject:
    cp = MagicMock(spec=ControlPoint)
    cp.captured = MagicMock()
    cp.captured.is_blue = captured_is_blue
    from game.data.groups import GroupTask

    return MotorpoolGroundObject("Test Motorpool", _location(), cp, GroupTask.MOTORPOOL)


def test_motorpool_category_registered() -> None:
    assert NAME_BY_CATEGORY["motorpool"] == "Motorpool"


def test_motorpool_str_does_not_keyerror() -> None:
    assert str(_motorpool()) == "Motorpool"


def test_motorpool_is_not_purchasable() -> None:
    assert _motorpool().purchasable is False


def test_motorpool_is_not_capturable() -> None:
    assert _motorpool().capturable is False


def test_motorpool_does_not_head_to_conflict() -> None:
    assert _motorpool().should_head_to_conflict is False


def test_motorpool_symbol_is_maintenance_installation() -> None:
    symbol_set, _entity = _motorpool().symbol_set_and_entity
    assert symbol_set == SymbolSet.LAND_INSTALLATIONS


def test_motorpool_unit_types_starts_empty() -> None:
    assert _motorpool().motorpool_unit_types == {}
