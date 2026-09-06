# game/missiongenerator/kneeboard_recon/tests/test_projection.py
"""Tests for DCS Point to page pixel projection."""

from __future__ import annotations

import pytest
from dcs.mapping import Point
from dcs.terrain.caucasus.caucasus import Caucasus

from game.missiongenerator.kneeboard_recon.extent import MapExtent
from game.missiongenerator.kneeboard_recon.projection import Projector


@pytest.fixture(scope="module")
def caucasus() -> Caucasus:
    return Caucasus()


@pytest.fixture
def projector(caucasus: Caucasus) -> Projector:
    return Projector(
        extent=MapExtent(
            min_x=0.0,
            max_x=10_000.0,
            min_y=0.0,
            max_y=10_000.0,
            terrain=caucasus,
        ),
        pixel_width=1000,
        pixel_height=1000,
    )


def test_project_origin_is_bottom_left(
    projector: Projector, caucasus: Caucasus
) -> None:
    px, py = projector.project(Point(0.0, 0.0, caucasus))
    # Image coordinates: (0, 0) is top-left; min_x/min_y maps to bottom row of pixels.
    # DCS x is north (up on the map), so min_x = bottom. min_y is left.
    assert (px, py) == (0, 999)


def test_project_max_corner(projector: Projector, caucasus: Caucasus) -> None:
    px, py = projector.project(Point(10_000.0, 10_000.0, caucasus))
    assert (px, py) == (999, 0)


def test_project_center(projector: Projector, caucasus: Caucasus) -> None:
    px, py = projector.project(Point(5_000.0, 5_000.0, caucasus))
    # Python rounds half-to-even: round(499.5) == 500, so center maps to (500, 500).
    assert (px, py) == (500, 500)


def test_meters_to_px_scales_linearly(projector: Projector) -> None:
    # 1000 m at a 10 km / 1000 px extent = 100 px.
    assert projector.meters_to_px(1_000.0) == 100
    assert projector.meters_to_px(2_500.0) == 250


def test_meters_to_px_uses_smaller_axis(caucasus: Caucasus) -> None:
    # 20 km wide x 10 km tall extent, 2000 x 1000 page. Both axes give 100 m/px.
    p = Projector(
        extent=MapExtent(
            min_x=0.0,
            max_x=10_000.0,
            min_y=0.0,
            max_y=20_000.0,
            terrain=caucasus,
        ),
        pixel_width=2000,
        pixel_height=1000,
    )
    assert p.meters_to_px(1_000.0) == 100
