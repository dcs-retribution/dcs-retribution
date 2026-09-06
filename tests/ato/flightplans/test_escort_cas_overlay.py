from dcs import Point
from dcs.terrain import Caucasus
from shapely.geometry import Point as ShapelyPoint

from game.ato.flightplans.tacticaloverlay import cas_overlay, escort_overlay
from game.utils import nautical_miles


def _p(x: float, y: float) -> Point:
    return Point(x, y, Caucasus())


def test_escort_corridor_follows_route() -> None:
    overlay = escort_overlay(
        route=[_p(0, 0), _p(50000, 10000), _p(100000, 0)],
        engagement_range=nautical_miles(20),
    )
    assert len(overlay.reach) == 1 and overlay.reach[0].filled
    assert overlay.reach[0].geometry.contains(ShapelyPoint(50000, 10000))
    assert overlay.targets == []


def test_cas_corridor_spans_the_flot() -> None:
    overlay = cas_overlay(
        patrol_start=_p(0, 0),
        patrol_end=_p(40000, 0),
        engagement_range=nautical_miles(10),
    )
    assert len(overlay.reach) == 1 and overlay.reach[0].filled
    geom = overlay.reach[0].geometry
    # Corridor down the whole FLOT, not just a circle at the midpoint.
    assert geom.contains(ShapelyPoint(0, 0))
    assert geom.contains(ShapelyPoint(20000, 0))
    assert geom.contains(ShapelyPoint(40000, 0))
    assert overlay.actual_path is None
