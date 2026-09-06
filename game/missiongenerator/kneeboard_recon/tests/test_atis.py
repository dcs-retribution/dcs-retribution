# game/missiongenerator/kneeboard_recon/tests/test_atis.py
"""Tests for ATIS block extraction from Retribution Weather."""

from __future__ import annotations

import datetime
from unittest.mock import MagicMock

import pytest
from dcs.weather import Wind

from game.missiongenerator.kneeboard_recon.atis import (
    AtisBlock,
    altimeter_setting_inhg,
    build_atis_block,
    compute_qfe_inhg,
    draw_atis_block,
    format_cloud_layer,
    format_visibility,
    wind_from_deg,
)
from game.missiongenerator.kneeboard_recon._fonts import load_font
from game.utils import inches_hg
from game.weather.atmosphericconditions import AtmosphericConditions
from game.weather.clouds import Clouds
from game.weather.fog import Fog
from game.weather.weather import Weather
from game.weather.wind import WindConditions


def _stub_weather(
    *,
    qnh_inhg: float = 29.92,
    temp_c: int = 14,
    wind_sfc: tuple[float, float] = (130, 12),
    wind_2000: tuple[float, float] = (145, 22),
    wind_8000: tuple[float, float] = (160, 45),
    clouds_base_ft: int | None = 4500,
    clouds_density: str = "bkn",
    fog_visibility_km: float | None = None,
) -> MagicMock:
    # spec= guards against typoed attribute names silently returning a fresh
    # MagicMock instead of raising AttributeError. Sub-objects whose real
    # shapes matter for the ATIS pipeline (atmospheric, wind, clouds, fog)
    # are also spec'd to their actual Retribution classes.
    m = MagicMock(spec=Weather)
    m.atmospheric = MagicMock(spec=AtmosphericConditions)
    m.atmospheric.qnh = inches_hg(qnh_inhg)
    m.atmospheric.temperature_celsius = temp_c
    m.wind = MagicMock(spec=WindConditions)
    m.wind.at_0m = Wind(*wind_sfc)
    m.wind.at_2000m = Wind(*wind_2000)
    m.wind.at_8000m = Wind(*wind_8000)
    if clouds_base_ft is None:
        m.clouds = None
    else:
        # ``MagicMock(spec=Clouds)`` blocks attributes that aren't
        # exposed on the class itself. Real ``Clouds`` instances always
        # carry ``precipitation`` (set in ``__init__``); mirror that
        # default here so the spec-guarded mock can be inspected by
        # production code without raising.
        m.clouds = MagicMock(spec=Clouds)
        m.clouds.base_ft = clouds_base_ft
        m.clouds.density = clouds_density
        from dcs.weather import Weather as _PydcsWeather

        m.clouds.precipitation = _PydcsWeather.Preceptions.None_
    if fog_visibility_km is None:
        m.fog = None
    else:
        m.fog = MagicMock(spec=Fog)
        m.fog.visibility_km = fog_visibility_km
    return m


@pytest.mark.parametrize(
    "blows_to, expected_from",
    [
        (0, 180),
        (90, 270),
        (271, 91),
        (360, 180),
        (359.6, 180),  # rounds to 360 -> 0 -> +180
    ],
)
def test_wind_from_deg_flips_blows_to_into_wind_from(
    blows_to: float, expected_from: int
) -> None:
    """DCS stores "blows-to"; pilots expect "wind from" (180° opposite)."""
    assert wind_from_deg(blows_to) == expected_from


@pytest.mark.parametrize(
    "elevation_m, expected_inhg",
    [
        (0.0, 29.92),  # sea level: QFE equals QNH
        (305.0, 28.854),  # ~1000 ft
        (1000.0, 26.539),
        (1609.0, 24.636),  # ~5280 ft, Denver-class field
    ],
)
def test_compute_qfe_inhg_matches_isa_reduction(
    elevation_m: float, expected_inhg: float
) -> None:
    """Tight tolerance so a wrong ISA exponent or lapse rate is caught."""
    assert compute_qfe_inhg(29.92, elevation_m) == pytest.approx(
        expected_inhg, abs=0.01
    )


def test_compute_qfe_inhg_below_sea_level_exceeds_qnh() -> None:
    """Below-sea-level fields (e.g. Dead Sea strips) read higher than QNH."""
    assert compute_qfe_inhg(29.92, -20.0) == pytest.approx(29.991, abs=0.01)


def test_build_atis_block_populates_winds() -> None:
    """Wind tuples carry (from_dir_deg, speed_kts). Input direction is "blows to"
    per DCS convention, so the ATIS surface "from" value is the 180° opposite.
    Input speed is in m/s and is converted to knots.
    """
    block = build_atis_block(
        weather=_stub_weather(
            wind_sfc=(130, 12), wind_2000=(145, 22), wind_8000=(160, 45)
        ),
        start_time_local=datetime.datetime(2026, 5, 21, 6, 42),
        start_time_zulu=datetime.datetime(2026, 5, 21, 3, 42),
        sunrise=datetime.time(5, 54),
        sunset=datetime.time(20, 14),
        runway_name="13",
        runway_heading_deg=132,
        atc_freq_str="UHF 251.000",
        tacan_str="16X UGK",
    )
    # 12 m/s ≈ 23 kt, 22 m/s ≈ 43 kt, 45 m/s ≈ 87 kt; directions flipped 180°.
    assert block.wind_surface == (310, 23)
    assert block.wind_2000m == (325, 43)
    assert block.wind_8000m == (340, 87)


def test_build_atis_block_qnh_in_inhg_and_hpa() -> None:
    block = build_atis_block(
        weather=_stub_weather(qnh_inhg=30.02),
        start_time_local=datetime.datetime(2026, 5, 21, 6, 42),
        start_time_zulu=datetime.datetime(2026, 5, 21, 3, 42),
        sunrise=None,
        sunset=None,
        runway_name="13",
        runway_heading_deg=132,
        atc_freq_str="",
        tacan_str="",
    )
    assert block.qnh_inhg == pytest.approx(30.02, abs=0.001)
    # 30.02 inHg * 33.86389 hPa/inHg ≈ 1016.6 hPa, rounded to nearest = 1017.
    assert block.qnh_hpa == 1017


def test_build_atis_block_qfe_is_not_implemented_marker() -> None:
    """No elevation given -> QFE field shows N/A and qfe_inhg is None."""
    block = build_atis_block(
        weather=_stub_weather(),
        start_time_local=datetime.datetime(2026, 5, 21, 6, 42),
        start_time_zulu=datetime.datetime(2026, 5, 21, 3, 42),
        sunrise=None,
        sunset=None,
        runway_name="13",
        runway_heading_deg=132,
        atc_freq_str="",
        tacan_str="",
    )
    assert block.qfe_inhg is None
    assert "N/A" in block.qfe_display


def test_build_atis_block_qfe_uses_isa_when_elevation_provided() -> None:
    """ISA reduction: at 305 m (1000 ft) and 29.92 QNH, QFE ≈ 28.85 inHg."""
    block = build_atis_block(
        weather=_stub_weather(qnh_inhg=29.92),
        start_time_local=datetime.datetime(2026, 5, 21, 6, 42),
        start_time_zulu=datetime.datetime(2026, 5, 21, 3, 42),
        sunrise=None,
        sunset=None,
        runway_name="13",
        runway_heading_deg=132,
        atc_freq_str="",
        tacan_str="",
        field_elevation_m=305.0,
    )
    assert block.qfe_inhg is not None
    assert block.qfe_inhg == pytest.approx(28.85, abs=0.01)
    assert "inHg" in block.qfe_display
    assert "N/A" not in block.qfe_display


def test_build_atis_block_qfe_zero_elevation_equals_qnh() -> None:
    """At sea level QFE must equal QNH exactly."""
    block = build_atis_block(
        weather=_stub_weather(qnh_inhg=30.05),
        start_time_local=datetime.datetime(2026, 5, 21, 6, 42),
        start_time_zulu=datetime.datetime(2026, 5, 21, 3, 42),
        sunrise=None,
        sunset=None,
        runway_name="13",
        runway_heading_deg=132,
        atc_freq_str="",
        tacan_str="",
        field_elevation_m=0.0,
    )
    assert block.qfe_inhg == pytest.approx(30.05, abs=0.01)


def test_atis_block_no_storm_note_when_clear() -> None:
    """Quiet weather: pressure_note must be empty and no CB caveat in display."""
    block = build_atis_block(
        weather=_stub_weather(),
        start_time_local=datetime.datetime(2026, 5, 21, 6, 42),
        start_time_zulu=None,
        sunrise=None,
        sunset=None,
        runway_name="13",
        runway_heading_deg=132,
        atc_freq_str="",
        tacan_str="",
        field_elevation_m=468.0,
    )
    assert block.pressure_note == ""
    assert "CB" not in block.qnh_display
    assert "CB" not in block.qfe_display


def test_atis_block_adds_storm_caveat_when_precipitation_is_thunderstorm() -> None:
    """Thunderstorm precipitation: surface ~3 mb in-CB low alongside nominal QNH/QFE."""
    from dcs.weather import Weather as PydcsWeather

    # ISA temp so the altimeter-setting correction is a no-op here — this test
    # exercises the storm-drop surfacing, not the temperature correction.
    weather = _stub_weather(qnh_inhg=29.98, temp_c=15)
    # has_thunderstorm_cells reads .precipitation off the Clouds spec.
    weather.clouds.precipitation = PydcsWeather.Preceptions.Thunderstorm
    weather.clouds.preset = None
    block = build_atis_block(
        weather=weather,
        start_time_local=datetime.datetime(2026, 5, 21, 6, 42),
        start_time_zulu=None,
        sunrise=None,
        sunset=None,
        runway_name="13",
        runway_heading_deg=132,
        atc_freq_str="",
        tacan_str="",
        field_elevation_m=468.0,
    )
    assert "CB" in block.qnh_display
    assert "CB" in block.qfe_display
    # Nominal QNH 29.98 - 0.09 storm drop = 29.89 surfaced in the caveat.
    assert "29.89" in block.qnh_display
    assert "Thunderstorm" in block.pressure_note
    assert "3 mb" in block.pressure_note


def test_format_cloud_layer_clear() -> None:
    assert format_cloud_layer(None) == "CLR"


def test_format_cloud_layer_bkn() -> None:
    clouds = MagicMock()
    clouds.density = "bkn"
    clouds.base_ft = 4500
    assert format_cloud_layer(clouds) == "BKN 4500 FT"


def test_format_visibility_no_fog_is_unrestricted() -> None:
    assert format_visibility(None) == "7+ SM"


def test_format_visibility_with_fog_emits_km() -> None:
    fog = MagicMock()
    fog.visibility_km = 3.5
    assert format_visibility(fog) == "3.5 km (fog)"


def test_build_atis_block_zulu_optional_when_no_conversion_available() -> None:
    """Passing start_time_zulu=None must yield AtisBlock.zulu_time = None.

    Previously the page silently fell back to start_time_zulu = start_local
    and the ATIS row printed `06:42L / 06:42Z` — claiming a Zulu suffix on
    a local-time value. Callers without a real timezone must pass None so the
    display can drop the second column instead of lying about it.
    """
    block = build_atis_block(
        weather=_stub_weather(),
        start_time_local=datetime.datetime(2026, 5, 21, 6, 42),
        start_time_zulu=None,
        sunrise=None,
        sunset=None,
        runway_name="13",
        runway_heading_deg=132,
        atc_freq_str="",
        tacan_str="",
    )
    assert block.zulu_time is None


def test_build_atis_block_converts_wind_mps_to_knots() -> None:
    # Retribution stores Wind.speed in m/s (see game/weather/windspeedgenerators.py).
    # 25 m/s ≈ 48.6 kt; output is labeled "kt" so the value must be converted.
    block = build_atis_block(
        weather=_stub_weather(
            wind_sfc=(180, 25.0), wind_2000=(180, 30.0), wind_8000=(180, 50.0)
        ),
        start_time_local=datetime.datetime(2026, 1, 1),
        start_time_zulu=datetime.datetime(2026, 1, 1),
        sunrise=None,
        sunset=None,
        runway_name="13",
        runway_heading_deg=132,
        atc_freq_str="",
        tacan_str="",
    )
    assert (
        47 <= block.wind_surface[1] <= 50
    ), f"expected ~48 kt, got {block.wind_surface[1]}"
    assert 57 <= block.wind_2000m[1] <= 60
    assert 96 <= block.wind_8000m[1] <= 98


def test_atis_pressure_note_fits_within_panel_width() -> None:
    """The thunderstorm CB caveat must fit inside the ATIS panel.

    Regression guard: the note is drawn at the bottom of the panel with an
    18 px left inset and no wrapping. A future font-size bump or longer
    translation would silently clip on the right edge — assert the rendered
    text width stays within the panel's interior so changes have to update
    this test deliberately.
    """
    from PIL import Image, ImageDraw
    from dcs.weather import Weather as PydcsWeather

    weather = _stub_weather()
    weather.clouds.precipitation = PydcsWeather.Preceptions.Thunderstorm
    weather.clouds.preset = None
    block = build_atis_block(
        weather=weather,
        start_time_local=datetime.datetime(2026, 5, 21, 6, 42),
        start_time_zulu=None,
        sunrise=None,
        sunset=None,
        runway_name="13",
        runway_heading_deg=132,
        atc_freq_str="",
        tacan_str="",
        field_elevation_m=468.0,
    )
    assert (
        block.pressure_note != ""
    ), "pressure_note must be set for thunderstorm weather"

    panel_w = 768  # matches kneeboard_recon.pages.PAGE_W
    panel_h = 220  # matches kneeboard_recon.pages.ATIS_H
    img = Image.new("RGB", (panel_w, panel_h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw_atis_block(draw, block, x=0, y=0, width=panel_w, height=panel_h)

    # Same font draw_atis_block uses for the note row (size 10, regular).
    note_font = load_font(10, bold=False)
    note_width = draw.textlength(block.pressure_note, font=note_font)
    # Panel uses 18 px inset on each side for the note (matches draw_atis_block).
    usable = panel_w - 18 - 18
    assert (
        note_width <= usable
    ), f"pressure_note width {note_width:.0f}px overflows {usable}px panel area"


def test_altimeter_setting_noop_at_sea_level_and_isa_temp() -> None:
    # No correction at 0 m, nor when OAT == ISA standard (15 C) at any elevation.
    assert altimeter_setting_inhg(29.92, 0.0, 35.0) == 29.92
    assert altimeter_setting_inhg(29.92, 500.0, 15.0) == pytest.approx(29.92, abs=1e-6)


def test_altimeter_setting_hot_raises_cold_lowers() -> None:
    raw = 29.92
    assert altimeter_setting_inhg(raw, 500.0, 35.0) > raw  # warm day
    assert altimeter_setting_inhg(raw, 500.0, -10.0) < raw  # cold day


def test_atis_block_qnh_is_temperature_corrected_and_qfe_follows() -> None:
    # Cold day + elevation -> ATIS QNH below the raw sea-level value, and QFE is
    # the actual field pressure derived from the corrected QNH.
    weather = _stub_weather(qnh_inhg=29.92, temp_c=-10)
    block = build_atis_block(
        weather=weather,
        start_time_local=datetime.datetime(2026, 5, 21, 6, 42),
        start_time_zulu=None,
        sunrise=None,
        sunset=None,
        runway_name="13",
        runway_heading_deg=132,
        atc_freq_str="",
        tacan_str="",
        field_elevation_m=1000.0,
    )
    corrected = altimeter_setting_inhg(29.92, 1000.0, -10.0)
    assert block.qnh_inhg == pytest.approx(round(corrected, 2), abs=0.001)
    assert block.qnh_inhg < 29.92
    assert block.qfe_inhg == pytest.approx(
        round(compute_qfe_inhg(corrected, 1000.0), 2), abs=0.001
    )


def test_atis_block_qnh_uncorrected_without_elevation() -> None:
    # No field elevation -> can't correct -> raw sea-level QNH is shown.
    weather = _stub_weather(qnh_inhg=29.92, temp_c=-10)
    block = build_atis_block(
        weather=weather,
        start_time_local=datetime.datetime(2026, 5, 21, 6, 42),
        start_time_zulu=None,
        sunrise=None,
        sunset=None,
        runway_name="13",
        runway_heading_deg=132,
        atc_freq_str="",
        tacan_str="",
        field_elevation_m=None,
    )
    assert block.qnh_inhg == pytest.approx(29.92, abs=0.001)
