"""Tests for recon kneeboard page rendering helpers."""

from __future__ import annotations

from collections.abc import Generator, Sequence
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from dcs.vehicles import AirDefence
from game.data.radar_db import LAUNCHER_TRACKER_PAIRS, TRACK_RADARS
from game.missiongenerator.kneeboard_recon.label_layout import (
    LabelRequest,
    PlacedLabel,
    Rect,
)
from game.missiongenerator.kneeboard_recon.pages import (
    DetailReconPage,
    _dcs_airport_for_runway,
)


@pytest.fixture(autouse=True)
def _offline_basemap(
    monkeypatch: pytest.MonkeyPatch, tmp_path_factory: pytest.TempPathFactory
) -> Generator[None, None, None]:
    """Force the basemap into legacy-fallback mode and inject a tmp tile cache.

    Required because the recon page constructors now call
    ``tile_cache_dir()`` (which needs ``persistency.setup`` to have run) and
    because tests must not hit the live Esri tile service.
    """
    from game.missiongenerator.kneeboard_recon import basemap as _basemap
    from game.missiongenerator.kneeboard_recon import pages as _pages

    cache = tmp_path_factory.mktemp("tilecache")
    monkeypatch.setattr(_pages, "tile_cache_dir", lambda: cache)
    monkeypatch.setattr(_basemap, "render_tiles", lambda *a, **kw: None)
    yield


# ---------------------------------------------------------------------------
# RunwayData → pydcs Airport lookup helper
# ---------------------------------------------------------------------------


def test_dcs_airport_for_runway_matches_by_name() -> None:
    """Helper returns the pydcs Airport whose name matches runway.airfield_name."""
    runway = SimpleNamespace(airfield_name="Batumi")
    matching_ap = SimpleNamespace(name="Batumi")
    other_ap = SimpleNamespace(name="Senaki-Kolkhi")
    theater = SimpleNamespace(
        controlpoints=[
            SimpleNamespace(dcs_airport=other_ap),
            SimpleNamespace(dcs_airport=matching_ap),
            SimpleNamespace(dcs_airport=None),  # FOB / carrier
        ]
    )
    assert _dcs_airport_for_runway(runway, theater) is matching_ap


def test_dcs_airport_for_runway_returns_none_when_no_match() -> None:
    """FOB/carrier departures (no matching airport) return None instead of raising."""
    runway = SimpleNamespace(airfield_name="Some FOB")
    theater = SimpleNamespace(
        controlpoints=[
            SimpleNamespace(dcs_airport=None),
            SimpleNamespace(dcs_airport=SimpleNamespace(name="Batumi")),
        ]
    )
    assert _dcs_airport_for_runway(runway, theater) is None


# ---------------------------------------------------------------------------
# I1 — _describe_unit role labels for SAM components
# ---------------------------------------------------------------------------


def _make_unit(unit_type: object) -> MagicMock:
    """Build a minimal unit stub with .type = unit_type and .type.id."""
    u = MagicMock()
    u.type = unit_type
    u.name = "stub_unit"
    u.alive = True
    return u


def _make_page() -> DetailReconPage:
    flight = MagicMock()
    game = MagicMock()
    return DetailReconPage(flight=flight, game=game)


def test_describe_unit_track_radar_with_alic() -> None:
    """A TRACK_RADAR unit returns 'TR (<alic>)'."""
    # Kub STR is in TRACK_RADARS and has ALIC code 108.
    tr_type = AirDefence.Kub_1S91_str
    assert tr_type in TRACK_RADARS, "precondition: Kub_1S91_str must be in TRACK_RADARS"
    unit = _make_unit(tr_type)
    page = _make_page()
    desc = page._describe_unit(unit)
    assert desc == "TR (108)", f"Expected 'TR (108)', got {desc!r}"


def test_describe_unit_launcher_with_alic() -> None:
    """A LAUNCHER_TRACKER_PAIRS unit returns 'LN' (or 'LN (<alic>)' if a code exists)."""
    from game.data.alic import AlicCodes

    ln_type = AirDefence.Kub_2P25_ln
    assert ln_type in LAUNCHER_TRACKER_PAIRS, "precondition"
    unit = _make_unit(ln_type)
    page = _make_page()
    desc = page._describe_unit(unit)
    try:
        expected = f"LN ({AlicCodes.code_for(unit)})"
    except KeyError:
        expected = "LN"
    assert desc == expected, f"Expected {expected!r}, got {desc!r}"


def test_describe_unit_no_role_falls_back_to_name() -> None:
    """A plain vehicle unit that is not in any SAM set returns generic name."""
    page = _make_page()
    unit = MagicMock()
    unit.type = MagicMock()
    unit.type.name = "Generic Vehicle"
    unit.type.id = "some_id_not_in_radar_db"
    # Ensure it's not accidentally in any of the sets by using a fresh mock.
    desc = page._describe_unit(unit)
    assert desc == "Generic Vehicle", f"Expected generic name, got {desc!r}"


def test_describe_unit_track_radar_no_alic_returns_role_only() -> None:
    """A TRACK_RADAR unit with no ALIC code still returns the role label."""
    # Use Patriot_str which IS in TRACK_RADARS (code 202 exists, but test
    # the no-ALIC path by patching AlicCodes.code_for to raise KeyError).
    tr_type = AirDefence.Patriot_str
    assert tr_type in TRACK_RADARS, "precondition"
    unit = _make_unit(tr_type)
    page = _make_page()
    with patch(
        "game.missiongenerator.kneeboard_recon.pages.AlicCodes.code_for",
        side_effect=KeyError("no alic"),
    ):
        desc = page._describe_unit(unit)
    assert desc == "TR", f"Expected 'TR', got {desc!r}"


# ---------------------------------------------------------------------------
# I2 — OverviewReconPage calls place_labels
# ---------------------------------------------------------------------------


def test_overview_page_calls_place_labels(tmp_path: Path) -> None:
    """place_labels must be called during OverviewReconPage.write."""
    from PIL import Image as PILImage
    from game.missiongenerator.kneeboard_recon.pages import OverviewReconPage
    from game.missiongenerator.kneeboard_recon.extent import MapExtent
    import game.missiongenerator.kneeboard_recon.pages as pages_module

    flight = MagicMock()
    flight.callsign = "ENFIELD 1-1"
    flight.waypoints = []
    flight.friendly = True
    dep = MagicMock()
    dep.dcs_airport = None  # skip friendly CP drawing so no extra complexity
    flight.departure = dep

    target = MagicMock()
    target.position = MagicMock()
    target.position.x = 5000.0
    target.position.y = 5000.0
    target.position._terrain = MagicMock()
    target.obj_name = "TEST_TARGET"
    flight.package = MagicMock()
    flight.package.target = target

    game = MagicMock()
    game.theater.controlpoints = []
    coalition = MagicMock()
    bullseye_pos = MagicMock()
    bullseye_pos.x = 0.0
    bullseye_pos.y = 0.0
    bullseye_pos._terrain = MagicMock()
    coalition.bullseye.position = bullseye_pos
    game.coalition_for.return_value = coalition

    # A real tiny basemap so img.paste doesn't raise.
    fake_basemap = PILImage.new("RGB", (924, 900), (200, 200, 200))

    terrain_mock = MagicMock()
    fake_extent = MapExtent(
        min_x=0.0,
        max_x=10000.0,
        min_y=0.0,
        max_y=10000.0,
        terrain=terrain_mock,
    )

    page = OverviewReconPage(flight=flight, game=game)

    called = []
    original_place_labels = pages_module.place_labels

    def spy_place_labels(
        requests: Sequence[LabelRequest], *, occupied: Sequence[Rect], page_bbox: Rect
    ) -> list[PlacedLabel]:
        called.append(len(requests))
        return original_place_labels(requests, occupied=occupied, page_bbox=page_bbox)

    with patch.object(
        pages_module, "place_labels", side_effect=spy_place_labels
    ), patch.object(
        pages_module, "render_basemap", return_value=fake_basemap
    ), patch.object(
        pages_module, "corridor_extent", return_value=fake_extent
    ), patch.object(
        pages_module,
        "bullseye_bearing_range_nm",
        return_value=(MagicMock(degrees=270), 42.0),
    ):
        page.write(tmp_path / "overview.png")

    assert called, "place_labels was not called during OverviewReconPage.write"
