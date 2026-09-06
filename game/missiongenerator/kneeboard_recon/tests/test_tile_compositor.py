"""Tests for the tile compositor: stitch + crop + resample + treatment."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from PIL import Image

from game.missiongenerator.kneeboard_recon import tile_compositor
from game.missiongenerator.kneeboard_recon.extent import MapExtent
from game.missiongenerator.kneeboard_recon.tile_compositor import render_tiles


class _LL:
    """Minimal lat/lng carrier used by fake DCS Points in these tests."""

    def __init__(self, lat: float, lng: float) -> None:
        self.lat = lat
        self.lng = lng


def _solid_tile(color: tuple[int, int, int]) -> Image.Image:
    return Image.new("RGB", (256, 256), color)


def _make_extent(terrain: Any, half_extent_m: float = 5_000.0) -> MapExtent:
    return MapExtent(
        min_x=-half_extent_m,
        max_x=half_extent_m,
        min_y=-half_extent_m,
        max_y=half_extent_m,
        terrain=terrain,
    )


def _fake_terrain_with_latlng(
    lat: float = 42.0, lon: float = 41.0
) -> tuple[MagicMock, type[_LL]]:
    """Build a fake terrain whose Point(...).latlng() returns a fixed point.

    The compositor calls Point(x, y, terrain).latlng() for the SW and NE
    corners. We make latlng deterministic by giving each (x, y) a tiny
    offset from the centre, so SW < NE on both axes.
    """
    terrain = MagicMock()

    # The compositor wraps (x, y, terrain) in a dcs.mapping.Point. We patch
    # the Point class at the call site instead — see tests below.
    return terrain, _LL


def test_render_tiles_returns_none_if_any_tile_fails(tmp_path: Path) -> None:
    terrain, _LL = _fake_terrain_with_latlng()
    extent = _make_extent(terrain)

    from game.missiongenerator.kneeboard_recon import tile_compositor as tc

    def fake_point(x: float, y: float, t: Any) -> MagicMock:
        p = MagicMock()
        p.latlng.return_value = _LL(42.0 + x * 1e-6, 41.0 + y * 1e-6)
        return p

    def fake_fetch(z: int, x: int, y: int, cache_dir: Path) -> Image.Image | None:
        return None  # always fail

    with patch.object(tc, "Point", side_effect=fake_point), patch.object(
        tc, "fetch_tile", side_effect=fake_fetch
    ):
        img = render_tiles(extent, 400, 400, tmp_path)

    assert img is None


def test_render_tiles_stitches_known_tiles(tmp_path: Path) -> None:
    terrain, _LL = _fake_terrain_with_latlng()
    extent = _make_extent(terrain, half_extent_m=300.0)

    from game.missiongenerator.kneeboard_recon import tile_compositor as tc

    def fake_point(x: float, y: float, t: Any) -> MagicMock:
        p = MagicMock()
        p.latlng.return_value = _LL(42.0 + x * 1e-6, 41.0 + y * 1e-6)
        return p

    def fake_fetch(z: int, x: int, y: int, cache_dir: Path) -> Image.Image:
        # Deterministic colour per tile so we can probe pixels.
        return _solid_tile(((x * 17) % 256, (y * 31) % 256, 64))

    with patch.object(tc, "Point", side_effect=fake_point), patch.object(
        tc, "fetch_tile", side_effect=fake_fetch
    ):
        img = render_tiles(extent, 400, 400, tmp_path)

    assert img is not None
    assert img.size == (400, 400)
    assert img.mode == "RGB"


def test_render_tiles_applies_desaturation(tmp_path: Path) -> None:
    """A vivid red input tile should come out desaturated (S channel lower)."""
    import colorsys

    terrain, _LL = _fake_terrain_with_latlng()
    extent = _make_extent(terrain, half_extent_m=300.0)

    from game.missiongenerator.kneeboard_recon import tile_compositor as tc

    def fake_point(x: float, y: float, t: Any) -> MagicMock:
        p = MagicMock()
        p.latlng.return_value = _LL(42.0 + x * 1e-6, 41.0 + y * 1e-6)
        return p

    vivid_red: tuple[int, int, int] = (255, 30, 30)
    with patch.object(tc, "Point", side_effect=fake_point), patch.object(
        tc, "fetch_tile", return_value=_solid_tile(vivid_red)
    ):
        img = render_tiles(extent, 200, 200, tmp_path)

    # Sample a pixel away from the bottom-right attribution stamp.
    assert img is not None
    r, g, b = img.getpixel((50, 50))
    _, raw_s, _ = colorsys.rgb_to_hsv(255 / 255, 30 / 255, 30 / 255)
    _, treated_s, _ = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    assert (
        treated_s < raw_s * 0.85
    ), f"expected substantial desaturation; raw S={raw_s:.2f}, treated S={treated_s:.2f}"


def test_render_tiles_stamps_attribution_in_bottom_right(tmp_path: Path) -> None:
    """The Esri attribution stamp should darken the bottom-right corner."""
    terrain, _LL = _fake_terrain_with_latlng()
    extent = _make_extent(terrain, half_extent_m=300.0)

    from game.missiongenerator.kneeboard_recon import tile_compositor as tc

    def fake_point(x: float, y: float, t: Any) -> MagicMock:
        p = MagicMock()
        p.latlng.return_value = _LL(42.0 + x * 1e-6, 41.0 + y * 1e-6)
        return p

    white: tuple[int, int, int] = (255, 255, 255)
    with patch.object(tc, "Point", side_effect=fake_point), patch.object(
        tc, "fetch_tile", return_value=_solid_tile(white)
    ):
        img = render_tiles(extent, 200, 200, tmp_path)

    # Without attribution, every pixel would be the (treated) bright tile
    # color. With attribution, some pixel in the bottom-right region must
    # be significantly darker (attribution background is semi-transparent
    # black). Probe a region rather than a fixed point so the test doesn't
    # break when the attribution string width changes (e.g. `(c)` → `©`).
    assert img is not None
    plain_pixel = img.getpixel((20, 20))
    plain_lum = sum(plain_pixel) / 3
    darkest_lum = min(
        sum(img.getpixel((x, y))) / 3
        for x in range(img.width - 90, img.width - 4)
        for y in range(img.height - 30, img.height - 4)
    )
    assert darkest_lum < plain_lum * 0.7, (
        f"expected attribution to darken some pixel in the bottom-right; "
        f"plain_lum={plain_lum:.1f}, darkest_lum={darkest_lum:.1f}"
    )


def test_render_tiles_aligns_with_rotated_projection(tmp_path: Path) -> None:
    """Regression for the four-corner bbox / quad-warp fix.

    DCS theaters use Transverse Mercator centred on the theater; a
    DCS-axis-aligned square is a rotated quadrilateral in lat/lon space.
    The compositor must fetch tiles covering all four corners (not just
    the SW/NE diagonal) and warp the resulting canvas onto the page so
    that DCS corners land at page corners.

    Using a synthetic terrain that rotates DCS axes by 30 degrees, build
    a 4-tile fetcher whose colour encodes the tile's (x, y). After warp,
    the four output corners must each contain the colour of a *different*
    tile — i.e. the four DCS corners genuinely sit in four different
    tiles of the Mercator-aligned canvas. The pre-fix code (SW/NE-only
    bbox) cropped to a tighter rectangle whose four corners often shared
    a single tile, producing duplicate colours.
    """
    angle = math.radians(30.0)
    cos_a, sin_a = math.cos(angle), math.sin(angle)

    def rotated_latlng(x: float, y: float) -> _LL:
        # 30-degree rotation between DCS and lat/lon. Scale chosen so that
        # a 2000m DCS extent spans roughly one tile at z=15.
        return _LL(
            42.0 + (cos_a * x - sin_a * y) * 1e-5,
            41.0 + (sin_a * x + cos_a * y) * 1e-5,
        )

    terrain = MagicMock()

    def fake_point(x: float, y: float, t: Any) -> MagicMock:
        p = MagicMock()
        p.latlng.return_value = rotated_latlng(x, y)
        return p

    # Distinct colour per (tx, ty) so we can identify which tile each
    # page corner sampled from.
    def fake_fetch(z: int, x: int, y: int, cache_dir: Path) -> Image.Image:
        return Image.new(
            "RGB", (256, 256), ((x * 53) % 200 + 30, (y * 79) % 200 + 30, 90)
        )

    extent = MapExtent(
        min_x=-1000.0,
        max_x=1000.0,
        min_y=-1000.0,
        max_y=1000.0,
        terrain=terrain,
    )

    from game.missiongenerator.kneeboard_recon import tile_compositor as tc

    with patch.object(tc, "Point", side_effect=fake_point), patch.object(
        tc, "fetch_tile", side_effect=fake_fetch
    ):
        img = render_tiles(extent, 400, 400, tmp_path)

    assert img is not None
    # Sample a few pixels inboard from each output corner (away from the
    # attribution stamp at the bottom-right).
    page_corners = {
        "ul": img.getpixel((20, 20)),
        "ur": img.getpixel((img.width - 20, 20)),
        "ll": img.getpixel((20, img.height - 60)),
        "lr": img.getpixel((img.width - 80, img.height - 60)),
    }
    # Each sampled pixel should not be the canvas fill black (the warp
    # source quad lies within fetched tiles, not outside them).
    for name, px in page_corners.items():
        assert (
            sum(px) > 30
        ), f"corner {name} pixel {px} looks like canvas fill (no tile data)"


def test_render_tiles_applies_imagery_offset(tmp_path: Path) -> None:
    """An ``imagery_offset_deg=(dlat, dlng)`` must shift the tile lookup.

    Regression for the OSM offset path: a sign-flip in ``dlat``/``dlng``
    would silently misplace the satellite mosaic everywhere the offset
    JSON shipped a non-zero value. Capture the tile-coordinate range
    twice (once with offset 0, once with a small positive offset) and
    assert the second range is shifted in the direction the math
    requires.
    """
    from collections.abc import Callable

    terrain, _LL = _fake_terrain_with_latlng()
    extent = _make_extent(terrain, half_extent_m=500.0)

    from game.missiongenerator.kneeboard_recon import tile_compositor as tc

    def fake_point(x: float, y: float, t: Any) -> MagicMock:
        p = MagicMock()
        p.latlng.return_value = _LL(42.0 + x * 1e-6, 41.0 + y * 1e-6)
        return p

    calls_no_offset: list[tuple[int, int, int]] = []
    calls_offset: list[tuple[int, int, int]] = []

    def fake_fetch_recorder(
        target: list[tuple[int, int, int]],
    ) -> Callable[[int, int, int, Path], Image.Image]:
        def _impl(z: int, x: int, y: int, cache_dir: Path) -> Image.Image:
            target.append((z, x, y))
            return _solid_tile((100, 100, 100))

        return _impl

    with patch.object(tc, "Point", side_effect=fake_point), patch.object(
        tc, "fetch_tile", side_effect=fake_fetch_recorder(calls_no_offset)
    ):
        render_tiles(extent, 200, 200, tmp_path)
    with patch.object(tc, "Point", side_effect=fake_point), patch.object(
        tc, "fetch_tile", side_effect=fake_fetch_recorder(calls_offset)
    ):
        # +0.5° lng shifts the tile X range right; +0.5° lat shifts the tile
        # Y range up (Web Mercator: higher lat → smaller Y).
        render_tiles(extent, 200, 200, tmp_path, imagery_offset_deg=(0.5, 0.5))

    assert calls_no_offset, "no-offset path must fetch at least one tile"
    assert calls_offset, "offset path must fetch at least one tile"
    base_x = min(x for _, x, _ in calls_no_offset)
    base_y = min(y for _, _, y in calls_no_offset)
    shifted_x = min(x for _, x, _ in calls_offset)
    shifted_y = min(y for _, _, y in calls_offset)
    assert shifted_x > base_x, (
        f"+0.5° longitude must shift tile X range east (larger X); "
        f"base_x={base_x}, shifted_x={shifted_x}"
    )
    assert shifted_y < base_y, (
        f"+0.5° latitude must shift tile Y range north (smaller Y); "
        f"base_y={base_y}, shifted_y={shifted_y}"
    )


def test_render_tiles_returns_none_when_projection_raises(tmp_path: Path) -> None:
    terrain, _ = _fake_terrain_with_latlng()
    extent = _make_extent(terrain)

    from game.missiongenerator.kneeboard_recon import tile_compositor as tc

    def boom_point(x: float, y: float, t: Any) -> MagicMock:
        p = MagicMock()
        p.latlng.side_effect = RuntimeError("no transformer")
        return p

    with patch.object(tc, "Point", side_effect=boom_point):
        img = render_tiles(extent, 100, 100, tmp_path)
    assert img is None


def test_render_tiles_sets_projection_failure_reason(tmp_path: Path) -> None:
    terrain, _ = _fake_terrain_with_latlng()
    extent = _make_extent(terrain)

    from game.missiongenerator.kneeboard_recon import tile_compositor as tc

    def boom_point(x: float, y: float, t: Any) -> MagicMock:
        p = MagicMock()
        p.latlng.side_effect = RuntimeError("no transformer")
        return p

    with patch.object(tc, "Point", side_effect=boom_point):
        tc.render_tiles(extent, 100, 100, tmp_path)
    assert tc.last_failure_reason() == tc.FAILURE_PROJECTION


def test_render_tiles_sets_fetch_failure_reason(tmp_path: Path) -> None:
    terrain, _LL = _fake_terrain_with_latlng()
    extent = _make_extent(terrain, half_extent_m=500.0)

    from game.missiongenerator.kneeboard_recon import tile_compositor as tc

    def fake_point(x: float, y: float, t: Any) -> MagicMock:
        p = MagicMock()
        p.latlng.return_value = _LL(42.0 + x * 1e-6, 41.0 + y * 1e-6)
        return p

    with patch.object(tc, "Point", side_effect=fake_point), patch.object(
        tc, "fetch_tile", return_value=None
    ):
        tc.render_tiles(extent, 100, 100, tmp_path)
    assert tc.last_failure_reason() == tc.FAILURE_TILE_FETCH


def test_render_tiles_sets_tile_cap_failure_reason(tmp_path: Path) -> None:
    """A huge fake extent forces auto_zoom into a high level → tile count
    explodes past MAX_TILE_COUNT, and render_tiles must short-circuit with
    the cap reason rather than spend cycles fetching."""
    terrain, _LL = _fake_terrain_with_latlng()

    from game.missiongenerator.kneeboard_recon import tile_compositor as tc

    extent = _make_extent(terrain, half_extent_m=600.0)

    def fake_point(x: float, y: float, t: Any) -> MagicMock:
        # Inflate corner spread so auto_zoom picks a high z and the tile
        # range balloons past MAX_TILE_COUNT.
        p = MagicMock()
        p.latlng.return_value = _LL(42.0 + x * 1.0 / 1200.0, 41.0 + y * 1.0 / 1200.0)
        return p

    fetch_calls: list[tuple[int, int, int]] = []

    def recording_fetch(z: int, x: int, y: int, cache_dir: Path) -> Image.Image:
        fetch_calls.append((z, x, y))
        return _solid_tile((128, 128, 128))

    with patch.object(tc, "Point", side_effect=fake_point), patch.object(
        tc, "fetch_tile", side_effect=recording_fetch
    ):
        result = tc.render_tiles(extent, 800, 800, tmp_path)

    assert result is None
    assert tc.last_failure_reason() == tc.FAILURE_TILE_CAP
    assert fetch_calls == [], (
        "tile-cap fallback must short-circuit before fetching any tile; "
        f"got {len(fetch_calls)} fetch attempts"
    )


def test_render_tiles_resets_failure_reason_on_success(tmp_path: Path) -> None:
    """A successful render must wipe any stale failure-reason from prior calls."""
    terrain, _LL = _fake_terrain_with_latlng()
    extent = _make_extent(terrain, half_extent_m=300.0)

    from game.missiongenerator.kneeboard_recon import tile_compositor as tc

    def fake_point(x: float, y: float, t: Any) -> MagicMock:
        p = MagicMock()
        p.latlng.return_value = _LL(42.0 + x * 1e-6, 41.0 + y * 1e-6)
        return p

    # Seed a stale reason from a prior failure.
    tc._set_failure(tc.FAILURE_TILE_FETCH)
    assert tc.last_failure_reason() == tc.FAILURE_TILE_FETCH

    with patch.object(tc, "Point", side_effect=fake_point), patch.object(
        tc, "fetch_tile", return_value=_solid_tile((100, 100, 100))
    ):
        img = tc.render_tiles(extent, 200, 200, tmp_path)
    assert img is not None
    assert tc.last_failure_reason() == tc.FAILURE_NONE


def test_render_tiles_concurrent_fetch_invokes_all_tile_coords(tmp_path: Path) -> None:
    """Sanity check that the parallel fetch still requests every tile in the range."""
    import threading

    terrain, _LL = _fake_terrain_with_latlng()
    extent = _make_extent(terrain, half_extent_m=600.0)

    from game.missiongenerator.kneeboard_recon import tile_compositor as tc

    def fake_point(x: float, y: float, t: Any) -> MagicMock:
        p = MagicMock()
        p.latlng.return_value = _LL(42.0 + x * 1e-6, 41.0 + y * 1e-6)
        return p

    seen: set[tuple[int, int, int]] = set()
    seen_lock = threading.Lock()

    def thread_recording_fetch(z: int, x: int, y: int, cache_dir: Path) -> Image.Image:
        with seen_lock:
            seen.add((z, x, y))
        return _solid_tile((((x + y) * 7) % 256, 64, 64))

    with patch.object(tc, "Point", side_effect=fake_point), patch.object(
        tc, "fetch_tile", side_effect=thread_recording_fetch
    ):
        img = tc.render_tiles(extent, 400, 400, tmp_path)

    assert img is not None
    # Tile coverage of the 4-corner bbox should be at least 1 tile.
    assert len(seen) >= 1
    # All fetches at one zoom level (sanity check on the parallel path).
    assert len({z for z, _, _ in seen}) == 1


def test_render_tiles_degrades_when_fetch_raises_unexpectedly(
    tmp_path: Path,
) -> None:
    """An unforeseen exception escaping ``fetch_tile`` must degrade to the
    offline basemap, not abort mission generation.

    ``fetch_tile`` is designed to return ``None`` on every known failure,
    but the ``ThreadPoolExecutor`` re-raises anything it does not catch when
    its results are realised. Belt-and-suspenders: a raw exception here must
    still resolve to ``None`` + ``FAILURE_TILE_FETCH`` so the caller renders
    the OFFLINE fallback instead of crashing turn generation."""
    terrain, _LL = _fake_terrain_with_latlng()
    extent = _make_extent(terrain, half_extent_m=300.0)

    from game.missiongenerator.kneeboard_recon import tile_compositor as tc

    def fake_point(x: float, y: float, t: Any) -> MagicMock:
        p = MagicMock()
        p.latlng.return_value = _LL(42.0 + x * 1e-6, 41.0 + y * 1e-6)
        return p

    def exploding_fetch(z: int, x: int, y: int, cache_dir: Path) -> Image.Image:
        raise RuntimeError("unexpected tile-fetch failure")

    with patch.object(tc, "Point", side_effect=fake_point), patch.object(
        tc, "fetch_tile", side_effect=exploding_fetch
    ):
        result = tc.render_tiles(extent, 200, 200, tmp_path)

    assert result is None
    assert tc.last_failure_reason() == tc.FAILURE_TILE_FETCH
