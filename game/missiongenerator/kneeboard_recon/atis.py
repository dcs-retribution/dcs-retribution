# game/missiongenerator/kneeboard_recon/atis.py
"""ATIS-like text block builder for the airfield departure page.

QFE is computed from QNH and the OSM/DEM-derived airfield elevation
(``resources/airport_imagery/<terrain>.json``) using the ISA barometric
formula. When no elevation is available the field displays as ``"N/A"``.
"""

from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING

from PIL import ImageDraw

from dcs.weather import Weather as PydcsWeather, Wind

from game.utils import inches_hg, mps

from ._fonts import load_font

if TYPE_CHECKING:
    from game.weather.weather import Weather
    from game.weather.clouds import Clouds
    from game.weather.fog import Fog


# DCS thunderstorm cells (legacy clouds with precipitation=Thunderstorm or a
# storm cloud preset) drop the local pressure inside the CB by roughly 3 mb
# below the mission's nominal QNH. The kneeboard cannot predict whether the
# player will be inside a cell, so we surface the in-CB low as a secondary
# value next to the nominal QNH/QFE. ~3 mb is the value pilots empirically
# observe in DCS storm cells; it is not derived from the cloud-preset numbers
# because DCS does not expose its CB pressure model.
THUNDERSTORM_PRESSURE_DROP_INHG = 0.09


_FG = (15, 15, 15)
_FG_MUTED = (60, 60, 60)
_PANEL_BG = (238, 238, 232)


@dataclass(frozen=True)
class AtisBlock:
    local_time: str
    zulu_time: Optional[str]
    sunrise: Optional[str]
    sunset: Optional[str]
    runway_name: str
    runway_heading: int
    wind_surface: tuple[int, int]  # (heading_deg, speed_kts)
    wind_2000m: tuple[int, int]
    wind_8000m: tuple[int, int]
    qnh_inhg: float
    qnh_hpa: int
    qnh_display: str
    qfe_inhg: Optional[float]
    qfe_display: str
    temperature_c: int
    cloud_layer: str
    visibility: str
    atc_freq: str
    tacan: str
    # Plain-text caveat shown below the panel when the weather setup will
    # produce CB cells (e.g. precipitation=Thunderstorm). Empty otherwise.
    pressure_note: str


def format_cloud_layer(clouds: Optional["Clouds"]) -> str:
    if clouds is None:
        return "CLR"
    density_raw = getattr(clouds, "density", None)
    # DCS legacy clouds use integer octa-style density 0-10; older test fixtures
    # also pass a pre-formatted string (e.g. "bkn"). Map ints into the canonical
    # METAR-style abbreviation and pass strings through as-is.
    if isinstance(density_raw, int):
        if density_raw <= 0:
            density = "CLR"
        elif density_raw <= 2:
            density = "FEW"
        elif density_raw <= 4:
            density = "SCT"
        elif density_raw <= 7:
            density = "BKN"
        else:
            density = "OVC"
    elif isinstance(density_raw, str):
        density = density_raw.upper() or "CLD"
    else:
        density = "CLD"
    base_ft = getattr(clouds, "base_ft", None)
    if base_ft is None:
        return density
    return f"{density} {int(base_ft)} FT"


def format_visibility(fog: Optional["Fog"]) -> str:
    if fog is None:
        return "7+ SM"
    km = getattr(fog, "visibility_km", None)
    if km is None:
        return "fog"
    return f"{km:.1f} km (fog)"


def wind_from_deg(blows_to_deg: float) -> int:
    """Convert a DCS "blows-to" wind direction to the aviation "wind from".

    Retribution stores ``wind.direction`` using DCS's "blows-to" convention
    (verified empirically: a 271° value in the .miz reads as wind blowing
    toward 271° in-cockpit). Pilots expect "wind from" by aviation
    convention, so flip 180° at the display boundary. Shared by the recon
    ATIS panel and the standard kneeboard's wind line so the two surfaces
    never disagree on direction.
    """
    return (round(blows_to_deg) % 360 + 180) % 360


def _format_wind(wind: Wind) -> tuple[int, int]:
    # Speed is m/s in storage and knots in the ATIS.
    return (wind_from_deg(wind.direction), int(round(mps(wind.speed).knots)))


# ISA standard-atmosphere constants for the QFE/QNH barometric reduction.
# Derived from the hydrostatic equation under a linear temperature lapse:
#   P(h) = P0 * (1 - L*h/T0) ** (g*M/(R*L))
# with the standard troposphere values below. The exponent ~5.2561 is the
# canonical ICAO/ISA value used in altimeter conversions worldwide.
_ISA_LAPSE_K_PER_M = 0.0065
_ISA_TEMP_K = 288.15
_ISA_EXP = 5.25588


def compute_qfe_inhg(qnh_inhg: float, elevation_m: float) -> float:
    """Reduce sea-level QNH to airfield-level QFE via ISA barometric formula."""
    ratio = (1.0 - _ISA_LAPSE_K_PER_M * elevation_m / _ISA_TEMP_K) ** _ISA_EXP
    return qnh_inhg * ratio


_KELVIN_OFFSET = 273.15


def altimeter_setting_inhg(
    qnh_inhg: float, elevation_m: float, oat_msl_c: float
) -> float:
    """True sea-level QNH → the temperature-corrected **altimeter setting**.

    This is the value a standard (ISA-calibrated) altimeter must be set to so it
    reads field elevation on the ground — i.e. real-world QNH, and what the MOOSE
    ATIS broadcasts (``altimeterQNH=true``). Reduce QNH to the field using the
    *actual* OAT, then back to sea level using *ISA standard* temperature; the two
    reductions cancel at 0 m or when OAT == ISA (15 °C), so it's a no-op there.
    Feeding this into ``compute_qfe_inhg`` then yields the actual field pressure
    (the MOOSE QFE), so QNH and QFE both match ATIS.
    """
    if elevation_m == 0.0:
        return qnh_inhg
    t0 = oat_msl_c + _KELVIN_OFFSET
    actual = (1.0 - _ISA_LAPSE_K_PER_M * elevation_m / t0) ** _ISA_EXP
    isa = (1.0 - _ISA_LAPSE_K_PER_M * elevation_m / _ISA_TEMP_K) ** _ISA_EXP
    return qnh_inhg * actual / isa


def has_thunderstorm_cells(clouds: Optional["Clouds"]) -> bool:
    """True when DCS will spawn CB cells in this weather setup.

    Triggered by legacy thunderstorm precipitation. The shipped pydcs cloud
    presets (CLOUD_PRESETS) do not include any storm/CB-capable entries, so
    we rely solely on the precipitation enum. If DCS adds CB-capable presets
    later, extend this check then — guessing from substring matches on the
    preset name produced false positives on rain presets.
    """
    if clouds is None:
        return False
    return clouds.precipitation == PydcsWeather.Preceptions.Thunderstorm


def build_atis_block(
    weather: "Weather",
    *,
    start_time_local: datetime.datetime,
    start_time_zulu: Optional[datetime.datetime],
    sunrise: Optional[datetime.time],
    sunset: Optional[datetime.time],
    runway_name: str,
    runway_heading_deg: int,
    atc_freq_str: str,
    tacan_str: str,
    field_elevation_m: Optional[float] = None,
) -> AtisBlock:
    qnh = weather.atmospheric.qnh
    # Show the temperature-corrected altimeter setting at the departure field (what
    # ATIS broadcasts), not the raw sea-level QNH, so the kneeboard matches ATIS.
    # Without a field elevation we can't correct, so fall back to the raw QNH.
    if field_elevation_m is not None:
        qnh_inhg_eff = altimeter_setting_inhg(
            qnh.inches_hg, field_elevation_m, weather.atmospheric.temperature_celsius
        )
    else:
        qnh_inhg_eff = qnh.inches_hg
    qnh_inhg_rounded = round(qnh_inhg_eff, 2)
    qnh_hpa = int(round(inches_hg(qnh_inhg_eff).hecto_pascals))
    storm_cells = has_thunderstorm_cells(weather.clouds)
    qnh_storm_inhg = (
        round(qnh_inhg_eff - THUNDERSTORM_PRESSURE_DROP_INHG, 2)
        if storm_cells
        else None
    )
    # inHg only in the cell (no /hPa) so the panel width doesn't overflow into
    # the QFE / CLOUDS columns when the in-CB caveat is appended. hPa still
    # ships on AtisBlock as a separate field for callers that want it.
    qnh_display = f"{qnh_inhg_rounded:.2f} inHg"
    if qnh_storm_inhg is not None:
        qnh_display += f" (~{qnh_storm_inhg:.2f} CB)"
    if field_elevation_m is not None:
        # QFE from the temperature-corrected QNH = the actual field pressure, which
        # is what ATIS reports (and what zeros the altimeter on the ramp).
        qfe_inhg = round(compute_qfe_inhg(qnh_inhg_eff, field_elevation_m), 2)
        qfe_display = f"{qfe_inhg:.2f} inHg"
        if qnh_storm_inhg is not None:
            qfe_storm_inhg = round(
                compute_qfe_inhg(qnh_storm_inhg, field_elevation_m), 2
            )
            qfe_display += f" (~{qfe_storm_inhg:.2f} CB)"
    else:
        qfe_inhg = None
        qfe_display = "N/A"
    pressure_note = (
        "Thunderstorm cells in area — local QNH may drop ~3 mb (~0.09 inHg) "
        "inside CB cores; reset altimeter on approach"
        if storm_cells
        else ""
    )
    return AtisBlock(
        # ``L`` is a literal suffix ("local"), not a strftime directive —
        # parallel to the ``Z`` suffix used on zulu_time below.
        local_time=start_time_local.strftime("%H:%ML"),
        zulu_time=start_time_zulu.strftime("%H:%MZ") if start_time_zulu else None,
        sunrise=sunrise.strftime("%H:%M") if sunrise else None,
        sunset=sunset.strftime("%H:%M") if sunset else None,
        runway_name=runway_name,
        runway_heading=int(runway_heading_deg),
        wind_surface=_format_wind(weather.wind.at_0m),
        wind_2000m=_format_wind(weather.wind.at_2000m),
        wind_8000m=_format_wind(weather.wind.at_8000m),
        qnh_inhg=qnh_inhg_rounded,
        qnh_hpa=qnh_hpa,
        qnh_display=qnh_display,
        qfe_inhg=qfe_inhg,
        qfe_display=qfe_display,
        temperature_c=int(round(weather.atmospheric.temperature_celsius)),
        cloud_layer=format_cloud_layer(weather.clouds),
        visibility=format_visibility(weather.fog),
        atc_freq=atc_freq_str,
        tacan=tacan_str,
        pressure_note=pressure_note,
    )


def draw_atis_block(
    draw: ImageDraw.ImageDraw,
    block: AtisBlock,
    *,
    x: int,
    y: int,
    width: int,
    height: int,
) -> None:
    """Render ATIS block in 5-row x 3-column layout inside given rect."""
    draw.rectangle((x, y, x + width, y + height), fill=_PANEL_BG)
    draw.line((x, y + height, x + width, y + height), fill=_FG, width=2)

    rows: list[list[tuple[str, str]]] = [
        [
            (
                "TIME",
                (
                    f"{block.local_time} / {block.zulu_time}"
                    if block.zulu_time
                    else block.local_time
                ),
            ),
            ("SUNRISE", block.sunrise or "--"),
            ("SUNSET", block.sunset or "--"),
        ],
        [
            ("RWY IN USE", block.runway_name),
            ("HDG", f"{block.runway_heading}°"),
            ("WIND SFC", f"{block.wind_surface[0]:03d} / {block.wind_surface[1]} kt"),
        ],
        [
            ("WIND 2000 m", f"{block.wind_2000m[0]:03d} / {block.wind_2000m[1]} kt"),
            ("WIND 8000 m", f"{block.wind_8000m[0]:03d} / {block.wind_8000m[1]} kt"),
            ("TEMP", f"{block.temperature_c:+d} °C"),
        ],
        [
            ("QNH", block.qnh_display),
            ("QFE", block.qfe_display),
            ("CLOUDS", block.cloud_layer),
        ],
        [
            ("VIS", block.visibility),
            ("ATC", block.atc_freq or "--"),
            ("TACAN", block.tacan or "--"),
        ],
    ]

    label_font = load_font(11, bold=True)
    value_font = load_font(15, bold=True)
    note_font = load_font(10, bold=False)
    col_w = width // 3
    # Reserve a footer strip inside the panel for the pressure note when
    # present so it does not overlap the bottom row of cells.
    note_h = 18 if block.pressure_note else 0
    row_area_h = height - note_h
    row_h = row_area_h // len(rows)
    for ri, row in enumerate(rows):
        ry = y + 12 + ri * row_h
        for ci, (k, v) in enumerate(row):
            cx = x + ci * col_w + 18
            draw.text((cx, ry), k, fill=_FG_MUTED, font=label_font)
            draw.text((cx, ry + 14), v, fill=_FG, font=value_font)
    if block.pressure_note:
        draw.text(
            (x + 18, y + height - note_h + 2),
            block.pressure_note,
            fill=_FG_MUTED,
            font=note_font,
        )
