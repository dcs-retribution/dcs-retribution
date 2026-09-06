from dcs import Point
from dcs.terrain import Caucasus
from shapely.geometry import Point as ShapelyPoint

from game.ato.flightplans.tacticaloverlay import (
    ReachShape,
    TacticalOverlay,
    TacticalTarget,
)


def test_overlay_defaults_are_empty() -> None:
    overlay = TacticalOverlay()
    assert overlay.reach == []
    assert overlay.actual_path is None
    assert overlay.targets == []


def test_reach_shape_carries_fill_flag() -> None:
    shape = ReachShape(geometry=ShapelyPoint(0, 0).buffer(1.0), filled=True)
    assert shape.filled is True
    assert not shape.geometry.is_empty


def test_target_carries_position() -> None:
    position = Point(1000.0, 2000.0, Caucasus())
    target = TacticalTarget(position=position)
    assert target.position == position
