"""Tests for the active front line as a navmesh routing hazard.

``ThreatZones`` now buffers a capsule along the active front (perpendicular to
the blue->red axis) and folds it into ``all`` -- the geometry the navmesh and
generic ``threatened()`` checks use -- so AI flights route around / quickly
across the ground battle instead of loitering over it. The SAM-specific
(``air_defenses``) and CAP-specific (``airbases``) views deliberately stay clean.
"""

from __future__ import annotations

from dataclasses import dataclass

from dcs.mapping import Point
from shapely.geometry import Point as ShapelyPoint, Polygon, box

from game.threatzones import FRONT_LINE_THREAT_BUFFER, ThreatZones
from game.utils import Heading, nautical_miles


def _pt(x: float, y: float) -> Point:
    # Terrain is irrelevant to the planar math exercised here.
    return Point(x, y, None)  # type: ignore[arg-type]


@dataclass
class _FakeFrontLine:
    position: Point
    blue_forward_heading: Heading


def _front_line_north() -> _FakeFrontLine:
    # Combat centre at the origin, blue advancing north (toward red). The lateral
    # front therefore runs east-west (DCS convention: +x north, +y east).
    return _FakeFrontLine(_pt(0.0, 0.0), Heading.from_degrees(0))


def _capsule() -> Polygon:
    return ThreatZones._front_line_threat_zone(_front_line_north(), 80)  # type: ignore[arg-type]


def test_capsule_covers_the_front_and_lateral_extent() -> None:
    zone = _capsule()
    half_width_m = 80 * 1000 / 2
    # Centre of the battle and a point well within the lateral extent are covered.
    assert zone.contains(ShapelyPoint(0, 0))
    assert zone.contains(ShapelyPoint(0, half_width_m - 5000))


def test_capsule_buffers_only_modestly_in_depth() -> None:
    zone = _capsule()
    # A few NM back from the FLOT is inside the buffer...
    near = nautical_miles(5).meters
    assert zone.contains(ShapelyPoint(near, 0))
    # ...but well beyond FRONT_LINE_THREAT_BUFFER it is clear airspace again.
    far = FRONT_LINE_THREAT_BUFFER.meters + nautical_miles(5).meters
    assert not zone.contains(ShapelyPoint(far, 0))


def test_capsule_ends_past_the_front_flanks() -> None:
    zone = _capsule()
    half_width_m = 80 * 1000 / 2
    beyond_flank = half_width_m + FRONT_LINE_THREAT_BUFFER.meters + 5000
    assert not zone.contains(ShapelyPoint(0, beyond_flank))


def _zone_with_front(front: Polygon | None) -> ThreatZones:
    empty = Polygon()
    kwargs = {} if front is None else {"front_lines": front}
    return ThreatZones(
        theater=None,  # type: ignore[arg-type]
        airbases=empty,
        air_defenses=empty,
        radar_sam_threats=empty,
        **kwargs,
    )


def test_front_line_marks_all_but_not_the_sam_view() -> None:
    front = box(-1000, -1000, 1000, 1000)
    tz = _zone_with_front(front)
    here = _pt(0.0, 0.0)
    # The navmesh / generic threat view sees the front...
    assert tz.threatened(here) is True
    # ...but the SAM-specific view does not (air-defense planning stays clean).
    assert tz.threatened_by_air_defense(here) is False


def test_default_threat_zone_has_no_front_line() -> None:
    tz = _zone_with_front(None)
    assert tz.threatened(_pt(0.0, 0.0)) is False
