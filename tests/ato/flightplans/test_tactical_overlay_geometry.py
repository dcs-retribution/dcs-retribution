import math

from dcs import Point
from dcs.terrain import Caucasus
from shapely.geometry import Point as ShapelyPoint

from game.ato.flightplans.tacticaloverlay import (
    asymmetric_capsule,
    orbit_loop,
    orbit_radius,
    reach_circle,
    reach_corridor,
)
from game.utils import knots, nautical_miles


def _p(x: float, y: float) -> Point:
    return Point(x, y, Caucasus())


def test_reach_circle_radius() -> None:
    poly = reach_circle(_p(0, 0), nautical_miles(10))
    minx, miny, maxx, maxy = poly.bounds
    assert maxx == nautical_miles(10).meters
    assert math.isclose(maxx, -minx, rel_tol=1e-9)


def test_asymmetric_capsule_is_fatter_at_b() -> None:
    cap = asymmetric_capsule(
        _p(0, 0), _p(10000, 0), nautical_miles(5), nautical_miles(15)
    )
    minx, miny, maxx, maxy = cap.bounds
    assert maxy == nautical_miles(15).meters
    assert cap.contains(ShapelyPoint(10000, 0))


def test_corridor_follows_the_line() -> None:
    poly = reach_corridor([_p(0, 0), _p(10000, 0)], nautical_miles(2))
    assert poly.contains(ShapelyPoint(5000, 0))
    assert not poly.contains(ShapelyPoint(5000, nautical_miles(3).meters))


def test_orbit_loop_is_closed_ring_on_center() -> None:
    loop = orbit_loop(_p(100, 200), nautical_miles(3), segments=24)
    assert len(loop) == 25
    assert math.isclose(loop[0].x, loop[-1].x) and math.isclose(loop[0].y, loop[-1].y)
    for p in loop:
        assert math.isclose(
            _p(100, 200).distance_to_point(p), nautical_miles(3).meters, rel_tol=1e-6
        )


def test_orbit_radius_grows_with_speed() -> None:
    assert orbit_radius(knots(500)).meters > orbit_radius(knots(300)).meters > 0
