# game/missiongenerator/kneeboard_recon/tests/test_extent.py
"""Tests for MapExtent and corridor-extent computation."""

from __future__ import annotations

import pytest
from dcs.mapping import Point
from dcs.terrain.caucasus.caucasus import Caucasus

from game.missiongenerator.kneeboard_recon.extent import (
    MapExtent,
    aspect_correct,
    corridor_extent,
)


@pytest.fixture(scope="module")
def caucasus() -> Caucasus:
    return Caucasus()


def _p(x: float, y: float, caucasus: Caucasus) -> Point:
    return Point(x, y, caucasus)


def test_map_extent_span_x_and_span_y_in_meters(caucasus: Caucasus) -> None:
    e = MapExtent(
        min_x=0.0,
        max_x=10_000.0,
        min_y=-5_000.0,
        max_y=5_000.0,
        terrain=caucasus,
    )
    assert e.span_x_m == 10_000.0
    assert e.span_y_m == 10_000.0


def test_map_extent_contains(caucasus: Caucasus) -> None:
    e = MapExtent(
        min_x=0.0, max_x=10_000.0, min_y=0.0, max_y=10_000.0, terrain=caucasus
    )
    assert e.contains(_p(5_000.0, 5_000.0, caucasus)) is True
    assert e.contains(_p(15_000.0, 5_000.0, caucasus)) is False


def test_map_extent_expand(caucasus: Caucasus) -> None:
    e = MapExtent(
        min_x=0.0, max_x=10_000.0, min_y=0.0, max_y=10_000.0, terrain=caucasus
    )
    bigger = e.expand(1_000.0)
    assert bigger.min_x == -1_000.0
    assert bigger.max_x == 11_000.0
    assert bigger.min_y == -1_000.0
    assert bigger.max_y == 11_000.0


def test_corridor_extent_just_waypoints(caucasus: Caucasus) -> None:
    wp = [_p(0.0, 0.0, caucasus), _p(20_000.0, 10_000.0, caucasus)]
    e = corridor_extent(waypoints=wp, threats=[], extra_radius_m=0.0, terrain=caucasus)
    # A small margin is always added (10 % of corridor span).
    assert e.min_x < 0.0
    assert e.max_x > 20_000.0
    assert e.min_y < 0.0
    assert e.max_y > 10_000.0


def test_corridor_extent_includes_threats_in_bbox(caucasus: Caucasus) -> None:
    wp = [_p(0.0, 0.0, caucasus), _p(20_000.0, 0.0, caucasus)]
    threat = _p(10_000.0, 30_000.0, caucasus)  # 30 km north of corridor line
    e = corridor_extent(
        waypoints=wp, threats=[threat], extra_radius_m=0.0, terrain=caucasus
    )
    assert e.contains(threat)


def test_corridor_extent_extra_radius_expands_bbox(caucasus: Caucasus) -> None:
    wp = [_p(0.0, 0.0, caucasus), _p(20_000.0, 0.0, caucasus)]
    e = corridor_extent(
        waypoints=wp, threats=[], extra_radius_m=5_000.0, terrain=caucasus
    )
    assert e.min_y <= -5_000.0
    assert e.max_y >= 5_000.0


def test_corridor_extent_degenerate_single_waypoint(caucasus: Caucasus) -> None:
    wp = [_p(0.0, 0.0, caucasus)]
    e = corridor_extent(waypoints=wp, threats=[], extra_radius_m=0.0, terrain=caucasus)
    # Must still be a non-empty extent (we fall back to a 5 km square around the point).
    assert e.span_x_m > 0.0
    assert e.span_y_m > 0.0


def test_aspect_correct_pads_wide_world_vertically(caucasus: Caucasus) -> None:
    # World: 40 km east-west (span_y) by 10 km north-south (span_x)
    # Pixels: 800x800 (square). World is wider than pixel aspect -> pad span_x.
    e = MapExtent(
        min_x=0.0,
        max_x=10_000.0,
        min_y=0.0,
        max_y=40_000.0,
        terrain=caucasus,
    )
    out = aspect_correct(e, pixel_width=800, pixel_height=800)
    # span_y should be unchanged; span_x padded to match.
    assert out.span_y_m == pytest.approx(40_000.0)
    assert out.span_x_m == pytest.approx(40_000.0)
    # Center is preserved on both axes.
    assert (out.min_x + out.max_x) / 2 == pytest.approx(5_000.0)
    assert (out.min_y + out.max_y) / 2 == pytest.approx(20_000.0)


def test_aspect_correct_pads_tall_world_horizontally(caucasus: Caucasus) -> None:
    # World: 10 km east-west by 40 km north-south
    # Pixels: 800x800 -> world is taller than pixel aspect -> pad span_y.
    e = MapExtent(
        min_x=0.0,
        max_x=40_000.0,
        min_y=0.0,
        max_y=10_000.0,
        terrain=caucasus,
    )
    out = aspect_correct(e, pixel_width=800, pixel_height=800)
    assert out.span_x_m == pytest.approx(40_000.0)
    assert out.span_y_m == pytest.approx(40_000.0)


def test_aspect_correct_matches_nonsquare_pixel_aspect(caucasus: Caucasus) -> None:
    # 800px wide x 1000px tall -> target world ratio span_y:span_x = 0.8.
    e = MapExtent(
        min_x=0.0,
        max_x=10_000.0,
        min_y=0.0,
        max_y=10_000.0,
        terrain=caucasus,
    )
    out = aspect_correct(e, pixel_width=800, pixel_height=1000)
    # span_x grows because pixel is taller than wide; span_y stays.
    assert out.span_y_m == pytest.approx(10_000.0)
    assert out.span_x_m / out.span_y_m == pytest.approx(1000.0 / 800.0)


def test_aspect_correct_noop_when_already_matched(caucasus: Caucasus) -> None:
    e = MapExtent(
        min_x=0.0,
        max_x=10_000.0,
        min_y=0.0,
        max_y=10_000.0,
        terrain=caucasus,
    )
    out = aspect_correct(e, pixel_width=800, pixel_height=800)
    assert out.min_x == e.min_x and out.max_x == e.max_x
    assert out.min_y == e.min_y and out.max_y == e.max_y
