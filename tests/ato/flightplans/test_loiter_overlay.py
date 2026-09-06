import math

from dcs import Point
from dcs.terrain import Caucasus

from game.ato.flightplans.sead import SeadFlightPlan
from game.ato.flightplans.seadsweep import SeadSweepFlightPlan
from game.ato.flightplans.tacticaloverlay import TacticalOverlayDisplay, loiter_overlay
from game.ato.flightplans.uizonedisplay import UiZoneDisplay
from game.utils import nautical_miles


def _p(x: float, y: float) -> Point:
    return Point(x, y, Caucasus())


def test_loiter_overlay_bubble_on_engagement_center() -> None:
    target = _p(50000, 0)
    overlay = loiter_overlay(
        orbit_center=_p(0, 0),
        loiter_radius=nautical_miles(3),
        engagement_center=target,
        engagement_range=nautical_miles(30),
        target_position=target,
    )
    assert len(overlay.reach) == 1 and overlay.reach[0].filled
    minx, _, maxx, _ = overlay.reach[0].geometry.bounds
    assert (minx + maxx) / 2 == 50000  # bubble centered on engagement_center
    assert overlay.targets[0].position == target


def test_loiter_overlay_orbit_ring_on_anchor() -> None:
    anchor = _p(10000, 20000)
    overlay = loiter_overlay(
        orbit_center=anchor,
        loiter_radius=nautical_miles(3),
        engagement_center=anchor,
        engagement_range=nautical_miles(30),
        target_position=_p(50000, 0),
    )
    ring = overlay.actual_path
    assert ring is not None
    # Closed ring of loiter_radius centered on the orbit anchor.
    assert math.isclose(ring[0].x, ring[-1].x) and math.isclose(ring[0].y, ring[-1].y)
    for p in ring:
        assert math.isclose(
            anchor.distance_to_point(p), nautical_miles(3).meters, rel_tol=1e-6
        )


def test_sead_family_are_overlay_and_uizone_displays() -> None:
    for cls in (SeadFlightPlan, SeadSweepFlightPlan):
        assert issubclass(cls, TacticalOverlayDisplay)
        assert issubclass(cls, UiZoneDisplay)
