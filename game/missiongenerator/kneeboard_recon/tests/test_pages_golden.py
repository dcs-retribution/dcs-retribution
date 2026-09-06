"""Golden-image regression tests for recon kneeboard pages.

Each page class is rendered against the deterministic Caucasus stubs from
``conftest.py`` and the resulting PNG is compared to a fixture checked in
under ``tests/fixtures/``.

Gated behind ``RUN_KNEEBOARD_VISUAL_TESTS=1`` so it stays out of normal
CI runs. Font hinting and shapely-coastline polygon rasterisation drift
across Pillow / OS releases, and we don't want to re-baseline the
fixtures every time CI lands on a different runner image.

Refresh after a deliberate visual change:

    UPDATE_KNEEBOARD_GOLDENS=1 .venv/bin/python -m pytest \\
        game/missiongenerator/kneeboard_recon/tests/test_pages_golden.py

This overwrites the fixtures with the current renders and skips the
assertion pass so the developer can git-diff the PNGs before committing.
"""

from __future__ import annotations

import os
from collections.abc import Generator
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from dcs.terrain.caucasus.caucasus import Caucasus
from PIL import Image, ImageChops, ImageDraw, ImageStat

from game.missiongenerator.kneeboard_recon.pages import (
    AirbaseReconPage,
    AirfieldDeparturePage,
    DetailReconPage,
    FrontLineDetailPage,
    OverviewReconPage,
)

FIXTURES_DIR = Path(__file__).parent / "fixtures"

# Mean per-channel difference across the whole page. Antialiased text drifts
# one or two AA levels across Pillow releases, so a tiny tolerance is
# realistic. A pixel-perfect match would break on the next Pillow upgrade
# without signalling a real regression. The basemap itself is deterministic
# here (synthetic tiles, see _satellite_tiles), so the residual drift is
# font/marker antialiasing only.
MAX_MEAN_DIFF = 2.0

_run = os.environ.get("RUN_KNEEBOARD_VISUAL_TESTS") == "1"
_update = os.environ.get("UPDATE_KNEEBOARD_GOLDENS") == "1"

pytestmark = pytest.mark.skipif(
    not (_run or _update),
    reason="set RUN_KNEEBOARD_VISUAL_TESTS=1 to run golden-image tests",
)


def _synthetic_tile(
    z: int, x: int, y: int, cache_dir: Path | None = None, timeout: float = 15.0
) -> Image.Image:
    """Deterministic stand-in for the Esri World Imagery tile fetch.

    A solid per-tile colour keyed on ``(z, x, y)`` plus a 1px border — only
    non-antialiased primitives, so the composited mosaic is byte-identical
    across Pillow / OS releases. Real satellite JPEGs are not (imagery
    refreshes, recompression), which is why the live tile path is excluded
    from golden regression; eyeball real imagery via gen_recon_kneeboards.py.
    """
    img = Image.new(
        "RGB",
        (256, 256),
        ((x * 37) % 256, (y * 59) % 256, (z * 23 + x + y) % 256),
    )
    ImageDraw.Draw(img).rectangle((0, 0, 255, 255), outline=(40, 40, 40), width=1)
    return img


@pytest.fixture(autouse=True)
def _satellite_tiles(
    monkeypatch: pytest.MonkeyPatch, _offline_basemap: None
) -> Generator[None, None, None]:
    """Route golden renders through the real tile compositor fed by
    deterministic synthetic tiles, instead of the conftest offline fallback.

    The conftest ``_offline_basemap`` fixture forces ``render_tiles`` to
    ``None`` so the smoke tests exercise the legacy fallback path. Golden
    images should instead validate the *satellite* compositing/projection
    path, so here we restore the real ``render_tiles`` and patch the per-tile
    fetch with ``_synthetic_tile``. Declaring ``_offline_basemap`` as a
    dependency guarantees this fixture runs after it, so these patches win.
    """
    from game.missiongenerator.kneeboard_recon import basemap as _basemap
    from game.missiongenerator.kneeboard_recon import tile_compositor as _tc

    monkeypatch.setattr(_basemap, "render_tiles", _tc.render_tiles)
    monkeypatch.setattr(_tc, "fetch_tile", _synthetic_tile)
    yield


def _compare(actual: Image.Image, name: str) -> None:
    fixture_path = FIXTURES_DIR / f"{name}.png"
    if _update:
        FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
        actual.save(fixture_path)
        pytest.skip(f"updated fixture: {fixture_path}")
    assert fixture_path.exists(), (
        f"missing golden fixture {fixture_path}. "
        "Run with UPDATE_KNEEBOARD_GOLDENS=1 to create it."
    )
    expected = Image.open(fixture_path).convert(actual.mode)
    assert (
        actual.size == expected.size
    ), f"size mismatch: actual={actual.size} expected={expected.size}"
    diff = ImageChops.difference(actual, expected)
    if diff.getbbox() is None:
        return  # pixel-identical
    mean_diff = sum(ImageStat.Stat(diff).mean) / len(diff.getbands())
    assert mean_diff <= MAX_MEAN_DIFF, (
        f"{name}: mean per-channel diff {mean_diff:.2f} exceeds "
        f"tolerance {MAX_MEAN_DIFF}. Inspect {fixture_path} vs current "
        f"render; re-baseline with UPDATE_KNEEBOARD_GOLDENS=1 if "
        f"intentional."
    )


def test_airfield_departure_golden(
    tmp_path: Path,
    stub_flight: MagicMock,
    stub_game: MagicMock,
    stub_weather: MagicMock,
) -> None:
    page = AirfieldDeparturePage(
        flight=stub_flight,
        game=stub_game,
        weather=stub_weather,
    )
    out = tmp_path / "departure.png"
    page.write(out)
    _compare(Image.open(out), "airfield_departure")


def test_overview_golden(
    tmp_path: Path,
    stub_strike_flight: MagicMock,
    stub_game: MagicMock,
) -> None:
    page = OverviewReconPage(flight=stub_strike_flight, game=stub_game)
    out = tmp_path / "overview.png"
    page.write(out)
    _compare(Image.open(out), "overview")


def test_detail_golden(
    tmp_path: Path,
    stub_strike_flight: MagicMock,
    stub_game: MagicMock,
) -> None:
    page = DetailReconPage(flight=stub_strike_flight, game=stub_game)
    out = tmp_path / "detail.png"
    page.write(out)
    _compare(Image.open(out), "detail")


def test_airbase_golden(
    tmp_path: Path,
    stub_oca_flight: MagicMock,
    stub_game: MagicMock,
) -> None:
    page = AirbaseReconPage(flight=stub_oca_flight, game=stub_game)
    out = tmp_path / "airbase.png"
    page.write(out)
    _compare(Image.open(out), "airbase")


def test_frontline_detail_golden(
    tmp_path: Path,
    stub_strike_flight: MagicMock,
    stub_game: MagicMock,
    caucasus: Caucasus,
) -> None:
    """Visual regression guard for CAS / front-line detail rendering.

    Mirrors ``test_dispatcher_emits_frontline_detail`` in ``test_pages.py``:
    builds a synthetic front-line target with three concrete points and
    renders the page. Re-baseline with ``UPDATE_KNEEBOARD_GOLDENS=1`` after
    deliberate visual changes to corridor/label/threat-marker layout.
    """
    from unittest.mock import MagicMock
    from dcs.mapping import Point
    from game.ato.flighttype import FlightType
    from game.theater.frontline import FrontLine

    airport = next(a for a in caucasus.airport_list() if "Kobuleti" in a.name)
    front = MagicMock(spec=FrontLine)
    front.position = Point(airport.position.x + 30_000, airport.position.y, caucasus)
    front.name = "Front line A/B"
    front.points = [
        Point(front.position.x - 5_000, front.position.y - 1_000, caucasus),
        Point(front.position.x, front.position.y, caucasus),
        Point(front.position.x + 5_000, front.position.y + 1_000, caucasus),
    ]
    stub_strike_flight.flight_type = FlightType.CAS
    stub_strike_flight.package.target = front
    page = FrontLineDetailPage(flight=stub_strike_flight, game=stub_game)
    out = tmp_path / "frontline_detail.png"
    page.write(out)
    _compare(Image.open(out), "frontline_detail")
