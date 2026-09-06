"""Tests for Web-Mercator tile math and zoom auto-selection."""

from __future__ import annotations

import math
from unittest.mock import MagicMock

import pytest

from game.missiongenerator.kneeboard_recon.tile_projection import (
    auto_zoom,
    dcs_to_lat_lon,
    lat_lon_to_tile,
    tile_to_lat_lon,
)


def test_lat_lon_to_tile_origin_zoom_zero() -> None:
    # (lat=0, lon=0) at z=0 is the centre of the single world tile.
    x, y = lat_lon_to_tile(0.0, 0.0, 0)
    assert x == pytest.approx(0.5, abs=1e-9)
    assert y == pytest.approx(0.5, abs=1e-9)


def test_lat_lon_to_tile_origin_zoom_two() -> None:
    # At z=2 the world is 4x4 tiles; (0, 0) lies at (2.0, 2.0).
    x, y = lat_lon_to_tile(0.0, 0.0, 2)
    assert x == pytest.approx(2.0, abs=1e-9)
    assert y == pytest.approx(2.0, abs=1e-9)


def test_lat_lon_to_tile_prime_meridian_north_pole_approx() -> None:
    # Web Mercator y -> 0 as lat -> +85.05; lat=80 at z=4 should land near
    # the top of the map (y small but > 0).
    _, y = lat_lon_to_tile(80.0, 0.0, 4)
    assert 0.0 < y < 2.5, f"expected y near top of map at lat=80 z=4, got {y}"


def test_tile_lat_lon_round_trip() -> None:
    for lat in (-60.0, -10.5, 0.0, 12.34, 45.0, 60.0):
        for lon in (-170.0, -90.0, 0.0, 30.0, 175.0):
            for z in (3, 7, 12, 17):
                x, y = lat_lon_to_tile(lat, lon, z)
                lat2, lon2 = tile_to_lat_lon(x, y, z)
                assert lat2 == pytest.approx(lat, abs=1e-6), (lat, lon, z)
                assert lon2 == pytest.approx(lon, abs=1e-6), (lat, lon, z)


def test_auto_zoom_tight_extent_picks_high_zoom() -> None:
    # A 600 m square on an 800x800 page wants ~0.75 m/px on the page.
    # World Imagery m/px at z=17 (lat 42) ~= 1.17; at z=18 ~= 0.58. The
    # function should pick z=18 (smallest z whose px is <= page px).
    z = auto_zoom(
        width_m=600.0,
        height_m=600.0,
        page_w=800,
        page_h=800,
        center_lat_deg=42.0,
    )
    assert z == 18, f"expected z=18 for 600 m / 800 px at lat 42, got {z}"


def test_auto_zoom_wide_extent_picks_low_zoom() -> None:
    # 100 km on an 800 px page = 125 m/px. At lat 42:
    #   z=10 -> ~113 m/px (too coarse: 113 > 125 is FALSE so qualifies),
    #   z=11 -> ~57 m/px.
    # We expect the smallest z whose meters-per-pixel is <= page m/px, so z=10.
    z = auto_zoom(
        width_m=100_000.0,
        height_m=100_000.0,
        page_w=800,
        page_h=800,
        center_lat_deg=42.0,
    )
    assert z == 10, f"expected z=10 for 100km / 800 px at lat 42, got {z}"


def test_auto_zoom_clamps_to_max() -> None:
    # Tiny extent that wants z>19 must be clamped at 19.
    z = auto_zoom(
        width_m=10.0,
        height_m=10.0,
        page_w=2000,
        page_h=2000,
        center_lat_deg=42.0,
        max_zoom=19,
    )
    assert z == 19


def test_auto_zoom_clamps_to_zero() -> None:
    z = auto_zoom(
        width_m=40_000_000.0,
        height_m=40_000_000.0,
        page_w=10,
        page_h=10,
        center_lat_deg=0.0,
    )
    assert z == 0


def test_dcs_to_lat_lon_uses_point_latlng() -> None:
    fake_latlng = MagicMock()
    fake_latlng.lat = 42.5
    fake_latlng.lng = 41.0
    point = MagicMock()
    point.latlng.return_value = fake_latlng
    lat, lon = dcs_to_lat_lon(point)
    point.latlng.assert_called_once_with()
    assert (lat, lon) == (42.5, 41.0)
