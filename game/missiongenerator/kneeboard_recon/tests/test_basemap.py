# game/missiongenerator/kneeboard_recon/tests/test_basemap.py
"""Tests for the basemap façade: tile path, legacy fallback, OFFLINE banner."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest
from PIL import Image
from dcs.terrain.caucasus.caucasus import Caucasus

from game.missiongenerator.kneeboard_recon import basemap
from game.missiongenerator.kneeboard_recon.basemap import (
    DETAIL_THRESHOLD_M,
    render_basemap,
)
from game.missiongenerator.kneeboard_recon.extent import MapExtent


@pytest.fixture(scope="module")
def caucasus() -> Caucasus:
    return Caucasus()


def test_render_basemap_returns_tile_image_when_pipeline_succeeds(
    caucasus: Caucasus, tmp_path: Path
) -> None:
    """When render_tiles returns an image, render_basemap returns it unchanged."""
    extent = MapExtent(min_x=0.0, max_x=600.0, min_y=0.0, max_y=600.0, terrain=caucasus)
    sentinel = Image.new("RGB", (400, 400), (12, 34, 56))
    with patch.object(basemap, "render_tiles", return_value=sentinel):
        img = render_basemap(
            extent, page_width=400, page_height=400, cache_dir=tmp_path
        )
    assert img is sentinel


def test_render_basemap_falls_back_to_legacy_when_tiles_unavailable(
    caucasus: Caucasus, tmp_path: Path
) -> None:
    """Legacy renderer runs and OFFLINE banner is stamped on the top row."""
    extent = MapExtent(
        min_x=0.0, max_x=1_000.0, min_y=0.0, max_y=1_000.0, terrain=caucasus
    )
    with patch.object(basemap, "render_tiles", return_value=None):
        img = render_basemap(
            extent, page_width=400, page_height=400, cache_dir=tmp_path
        )
    assert img.size == (400, 400)
    # Banner is rendered across the top: sample a pixel in the middle of the
    # banner band. The banner background red dominates.
    r, g, b = img.getpixel((200, 6))
    assert (
        r > 120 and r > g + 40 and r > b + 40
    ), f"expected red OFFLINE banner at top, got pixel ({r}, {g}, {b})"


def test_render_basemap_legacy_fallback_below_threshold_uses_tan_landmap(
    caucasus: Caucasus, tmp_path: Path
) -> None:
    """Below DETAIL_THRESHOLD_M, fallback uses the tan landmap renderer.

    Sample a pixel below the OFFLINE banner band but above any overlay; it
    should be the tan land colour.
    """
    extent = MapExtent(
        min_x=0.0, max_x=1_000.0, min_y=0.0, max_y=1_000.0, terrain=caucasus
    )
    with patch.object(basemap, "render_tiles", return_value=None):
        img = render_basemap(
            extent, page_width=900, page_height=600, cache_dir=tmp_path
        )
    # The OFFLINE banner is 24 px tall; sample at y=50 which is past it.
    assert img.getpixel((0, 50)) == (224, 213, 191)


def test_render_basemap_legacy_fallback_above_threshold_uses_gif_crop(
    caucasus: Caucasus, tmp_path: Path
) -> None:
    """Above DETAIL_THRESHOLD_M the legacy path crops the theater gif.

    Patch ``_load_gif`` so the test does not depend on the GIF file being
    present in the CI environment, and explicitly assert it was invoked —
    a prior version only checked ``len(colors) > 5`` which also passes
    on the tan-landmap fallback when the GIF is absent, providing no
    real regression coverage for the GIF path.
    """
    extent = MapExtent(
        min_x=0.0, max_x=30_000.0, min_y=0.0, max_y=30_000.0, terrain=caucasus
    )
    synthetic_gif = Image.new("RGB", (200, 200), (50, 90, 130))
    # Drop any cached gif from a previous test so the spy actually runs.
    basemap._gif_cache.pop(caucasus.name, None)
    with patch.object(basemap, "render_tiles", return_value=None), patch.object(
        basemap, "_load_gif", return_value=synthetic_gif
    ) as gif_spy:
        img = render_basemap(
            extent, page_width=920, page_height=600, cache_dir=tmp_path
        )
    gif_spy.assert_called()
    colors = img.getcolors(maxcolors=100_000)
    assert colors is not None
    assert len(colors) > 5, "gif crop fallback should produce a multi-color image"


def test_render_basemap_legacy_fallback_wide_east_west_uses_gif_crop(
    caucasus: Caucasus, tmp_path: Path
) -> None:
    """A corridor short north-south but wide east-west is still a large area
    and must take the GIF crop, not the tan grid. Guards against keying the
    threshold off span_x_m alone."""
    extent = MapExtent(
        min_x=0.0, max_x=2_000.0, min_y=0.0, max_y=30_000.0, terrain=caucasus
    )
    synthetic_gif = Image.new("RGB", (200, 200), (50, 90, 130))
    basemap._gif_cache.pop(caucasus.name, None)
    with patch.object(basemap, "render_tiles", return_value=None), patch.object(
        basemap, "_load_gif", return_value=synthetic_gif
    ) as gif_spy:
        render_basemap(extent, page_width=920, page_height=600, cache_dir=tmp_path)
    gif_spy.assert_called()


def test_detail_threshold_is_5km() -> None:
    assert DETAIL_THRESHOLD_M == 5_000.0


def test_landmap_polygons_cached_after_first_load(caucasus: Caucasus) -> None:
    """Repeated calls for the same terrain must not re-read the pickle file."""
    basemap._landmap_cache.pop(caucasus.name, None)
    with patch.object(basemap, "pickle", wraps=basemap.pickle) as spy:
        basemap._landmap_polygons_for_terrain(caucasus)
        basemap._landmap_polygons_for_terrain(caucasus)
        assert spy.load.call_count == 1


def _has_text_pixels(img: Image.Image, text_substr: str) -> bool:
    """Quick proxy: scan the banner band for the expected text by rendering
    a synthetic comparison and asserting close-to-white pixels exist in the
    matching x-range. We don't OCR — pixel sampling is good enough."""
    # Lightweight: count near-white pixels in the banner row. The cap-text
    # banner ("...area too large...") is longer than the default banner,
    # so the count of bright pixels in the banner band differs.
    near_white = 0
    for x in range(img.width):
        r, g, b = img.getpixel((x, 11))
        if r > 220 and g > 220 and b > 220:
            near_white += 1
    return near_white > 0


def test_render_basemap_offline_banner_uses_tile_cap_text(
    caucasus: Caucasus, tmp_path: Path
) -> None:
    """Tile-cap fallback must stamp the tile-cap banner text, not the generic one."""
    from game.missiongenerator.kneeboard_recon import tile_compositor

    extent = MapExtent(
        min_x=0.0, max_x=1_000.0, min_y=0.0, max_y=1_000.0, terrain=caucasus
    )

    def _fail_with_cap(*args: object, **kwargs: object) -> None:
        tile_compositor._set_failure(tile_compositor.FAILURE_TILE_CAP)
        return None

    with patch.object(basemap, "render_tiles", side_effect=_fail_with_cap):
        cap_img = render_basemap(extent, 400, 400, cache_dir=tmp_path)

    def _fail_generic(*args: object, **kwargs: object) -> None:
        tile_compositor._set_failure(tile_compositor.FAILURE_TILE_FETCH)
        return None

    with patch.object(basemap, "render_tiles", side_effect=_fail_generic):
        generic_img = render_basemap(extent, 400, 400, cache_dir=tmp_path)

    # The cap banner text is materially longer than the default; the number
    # of white-text pixels in the banner row therefore differs. This is a
    # cheap proxy for "the two banner strings actually rendered differently"
    # without parsing pixels into glyphs.
    cap_white = sum(
        1
        for x in range(cap_img.width)
        if all(c > 220 for c in cap_img.getpixel((x, 11)))
    )
    generic_white = sum(
        1
        for x in range(generic_img.width)
        if all(c > 220 for c in generic_img.getpixel((x, 11)))
    )
    assert cap_white != generic_white, (
        f"cap-vs-generic banner pixel counts must differ; got cap={cap_white}, "
        f"generic={generic_white}"
    )


def test_banner_text_for_reason_returns_distinct_strings() -> None:
    """Unit guard on the reason → banner mapping (no PIL involvement)."""
    from game.missiongenerator.kneeboard_recon.basemap import (
        _OFFLINE_TEXT_DEFAULT,
        _OFFLINE_TEXT_TILE_CAP,
        _banner_text_for_reason,
    )
    from game.missiongenerator.kneeboard_recon import tile_compositor

    assert (
        _banner_text_for_reason(tile_compositor.FAILURE_TILE_CAP)
        == _OFFLINE_TEXT_TILE_CAP
    )
    assert (
        _banner_text_for_reason(tile_compositor.FAILURE_TILE_FETCH)
        == _OFFLINE_TEXT_DEFAULT
    )
    assert (
        _banner_text_for_reason(tile_compositor.FAILURE_PROJECTION)
        == _OFFLINE_TEXT_DEFAULT
    )
    assert _banner_text_for_reason("") == _OFFLINE_TEXT_DEFAULT
    assert _OFFLINE_TEXT_TILE_CAP != _OFFLINE_TEXT_DEFAULT
