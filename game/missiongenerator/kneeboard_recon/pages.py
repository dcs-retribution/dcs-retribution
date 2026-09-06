# game/missiongenerator/kneeboard_recon/pages.py
"""Recon kneeboard page classes."""

from __future__ import annotations

import datetime
import logging
import math
from dataclasses import dataclass
from pathlib import Path
from typing import (
    Any,
    Dict,
    Optional,
    Sequence,
    TYPE_CHECKING,
    List,
    Tuple,
    Union,
    cast,
)

from PIL import Image, ImageDraw, ImageFont
from dcs.mapping import LatLng, Point as DcsPoint
from dcs.terrain.terrain import Airport, Terrain
from suntime import Sun, SunTimeException  # type: ignore

from game.missiongenerator.kneeboard_page import KneeboardPage

from ._fonts import load_font, PilFont
from .airfield_diagram import (
    draw_active_threshold_marker,
    draw_spawn_marker,
    draw_wind_arrow_badge,
)
from .label_layout import LabelRequest, PlacedLabel, Rect, place_labels
from .atis import build_atis_block, draw_atis_block
from .basemap import render_basemap
from . import airport_imagery as _airport_imagery
from game.persistency import tile_cache_dir
from .coords import bullseye_bearing_range_nm, point_to_mgrs
from .extent import MapExtent, aspect_correct, corridor_extent, square_extent
from .markers import (
    Aimpoint,
    FRIENDLY_FILL,
    FRIENDLY_OUTLINE,
    cluster_items,
    draw_aimpoint_badge,
    draw_building_footprint,
    draw_sidc_enemy,
)
from .projection import Projector
from .threat_rings import draw_threat_rings
from .tile_source import reset_failure_log_state as _reset_tile_log_state

from game.ato.flighttype import FlightType
from game.ato.flightwaypointtype import FlightWaypointType
from game.data.alic import AlicCodes
from game.data.radar_db import (
    LAUNCHER_TRACKER_PAIRS,
    TELARS,
    TRACK_RADARS,
    UNITS_WITH_RADAR,
)
from game.ato.starttype import StartType
from game.data.units import UnitClass
from game.theater.controlpoint import ControlPoint
from game.theater.frontline import FrontLine
from game.theater.theatergroundobject import (
    BuildingGroundObject,
    EwrGroundObject,
    TheaterGroundObject,
)

if TYPE_CHECKING:
    from game import Game
    from game.missiongenerator.aircraft.flightdata import FlightData
    from game.weather.weather import Weather


logger = logging.getLogger(__name__)


PAGE_W = 768
PAGE_H = 1024
TITLE_H = 56
ATIS_H = 220
FOOTER_H = 36


def _dcs_airport_for_runway(runway: Any, theater: Any) -> Optional[Airport]:
    # RunwayData only carries airfield_name; the pydcs Airport lives on the
    # originating ControlPoint. Returns None for FOB/carrier departures.
    name = runway.airfield_name
    for cp in theater.controlpoints:
        ap = cp.dcs_airport
        if ap is not None and ap.name == name:
            return ap
    return None


@dataclass(frozen=True)
class _Palette:
    """Recon-page chrome colors. Marker semantics (red threat, blue friendly,
    destroyed brown) are not themed — only text, lines, and panel backgrounds.
    """

    page_bg: tuple[int, int, int]
    fg: tuple[int, int, int]
    muted: tuple[int, int, int]
    title_bg: tuple[int, int, int]
    title_fg: tuple[int, int, int]
    panel_bg: tuple[int, int, int]
    panel_outline: tuple[int, int, int]
    destroyed: tuple[int, int, int]


_LIGHT_PALETTE = _Palette(
    page_bg=(250, 248, 244),
    fg=(15, 15, 15),
    muted=(60, 60, 60),
    title_bg=(15, 15, 15),
    title_fg=(250, 248, 244),
    panel_bg=(255, 255, 255),
    panel_outline=(0, 0, 0),
    destroyed=(130, 60, 60),
)


_DARK_PALETTE = _Palette(
    page_bg=(12, 8, 8),
    fg=(220, 200, 200),
    muted=(150, 140, 140),
    title_bg=(220, 200, 200),
    title_fg=(12, 8, 8),
    panel_bg=(40, 30, 30),
    panel_outline=(220, 200, 200),
    destroyed=(220, 110, 110),
)


def _palette(dark: bool) -> _Palette:
    return _DARK_PALETTE if dark else _LIGHT_PALETTE


def _title_bar(
    image: Image.Image,
    draw: ImageDraw.ImageDraw,
    text: str,
    palette: _Palette,
) -> int:
    draw.rectangle((0, 0, image.width, TITLE_H), fill=palette.title_bg)
    font = load_font(26, bold=True)
    draw.text((24, 12), text, fill=palette.title_fg, font=font)
    return TITLE_H + 8


# Used when no OSM record ships for an airport: place the threshold
# marker this far from airport center, opposite the landing heading
# (i.e. at the touchdown end). 900 m is a coarse approximation of a
# typical runway half-length across the shipped DCS terrains.
_FALLBACK_RUNWAY_HALF_LENGTH_M = 900.0


def _fallback_threshold_dcs_point(
    airport: Airport, heading_deg: float, terrain: Terrain
) -> DcsPoint:
    """Project a fallback threshold marker along the runway heading.

    The named threshold for RWY N is the END where aircraft landing on
    RWY N first touch down — i.e. the end OPPOSITE the landing direction.
    DCS axes: x = north, y = east.
    """
    rad = math.radians(heading_deg)
    dx = -math.cos(rad) * _FALLBACK_RUNWAY_HALF_LENGTH_M
    dy = -math.sin(rad) * _FALLBACK_RUNWAY_HALF_LENGTH_M
    return DcsPoint(
        airport.position.x + dx,
        airport.position.y + dy,
        terrain,
    )


def _target_display_name(target: Any) -> str:
    """Best-effort human name for a package target.

    Recon pages show this in the page title, so it must always be
    non-empty. Walks ``obj_name`` then ``name`` and falls back to a
    placeholder for targets that expose neither.
    """
    return (
        getattr(target, "obj_name", None) or getattr(target, "name", None) or "TARGET"
    )


def _centroid(members: List[Any], terrain: Terrain) -> DcsPoint:
    n = len(members)
    sx = sum(m.position.x for m in members) / n
    sy = sum(m.position.y for m in members) / n
    return DcsPoint(sx, sy, terrain)


# Default front-line width in km when game.settings is unavailable (e.g.
# stubs in unit tests, or a malformed campaign save). Matches the shipped
# Settings default so the kneeboard render lines up with the planner UI.
_DEFAULT_MAX_FRONTLINE_WIDTH_KM = 80.0


def _frontline_bounds_points(
    front: Any, game: Any, terrain: Terrain
) -> Tuple[Any, Any]:
    """Return (left_position, right_position) of the perpendicular front-line
    bounds matching the planner map, or (None, None) if not computable.

    Defers to ``FrontLineConflictDescription.frontline_bounds`` so the
    kneeboard line matches the planner's orange polyline exactly,
    INCLUDING the inclusion-zone clamping that shortens the line when
    the perpendicular runs into water or terrain exclusion. Without that
    clamping the line spans the whole nominal ``max_frontline_width``
    even when the actual contested area is much narrower.

    Falls back to inline perpendicular math when frontline_bounds raises
    (e.g. unit-test mocks that don't wire ``front.coalition.game.settings``
    or a theater landmap). The fallback uses the unclamped width — fine
    for tests, which don't assert on bounds length.
    """
    try:
        from game.missiongenerator.frontlineconflictdescription import (
            FrontLineConflictDescription,
        )

        bounds = FrontLineConflictDescription.frontline_bounds(front, game.theater)
        return bounds.left_position, bounds.right_position
    except Exception as exc:
        logger.debug("frontline_bounds fallback: %s", exc, exc_info=True)

    # Fallback path: derive heading from the active segment endpoints
    # (real ``dcs.mapping.Point`` methods work on the test mocks) and
    # extend symmetrically without clamping. Production should never
    # reach this branch — frontline_bounds works on a real campaign.
    seg = getattr(front, "active_segment", None)
    if seg is None:
        return None, None
    point_a = getattr(seg, "point_a", None)
    point_b = getattr(seg, "point_b", None)
    if point_a is None or point_b is None:
        return None, None
    try:
        attack_heading_deg = float(point_a.heading_between_point(point_b))
    except (TypeError, ValueError):
        return None, None
    width_km = getattr(getattr(game, "settings", None), "max_frontline_width", None)
    try:
        width_km_f = (
            float(width_km) if width_km is not None else _DEFAULT_MAX_FRONTLINE_WIDTH_KM
        )
    except (TypeError, ValueError):
        width_km_f = _DEFAULT_MAX_FRONTLINE_WIDTH_KM
    half_m = width_km_f * 1000.0 / 2.0
    left_deg = (attack_heading_deg - 90.0) % 360.0
    right_deg = (attack_heading_deg + 90.0) % 360.0
    center = front.position
    try:
        left_pos = center.point_from_heading(left_deg, half_m)
        right_pos = center.point_from_heading(right_deg, half_m)
    except (TypeError, ValueError):
        return None, None
    return left_pos, right_pos


def _osm_threshold_in_dcs(
    airport: Airport, approach_heading_deg: float, terrain: Terrain
) -> Optional[DcsPoint]:
    """Return the DCS Point of the OSM-derived threshold for this approach.

    Looks up the airport's OSM record, picks the runway whose heading
    matches ``approach_heading_deg``, computes the threshold lat/lng for
    that approach end, then converts back to DCS coords. Returns ``None``
    if no OSM data is shipped for this airport or no runway matches the
    heading.

    The DCS Point lies on the OSM runway centerline regardless of the
    DCS-vs-real airport offset; combined with the imagery offset applied
    in the basemap renderer, the resulting marker pixel overlays the real
    runway end in the satellite imagery.
    """
    record = _airport_imagery.load(terrain.name)
    if record is None:
        return None
    entry = record.for_airport(airport)
    if entry is None:
        return None
    runway = entry.runway_for_heading(approach_heading_deg)
    if runway is None:
        return None
    t_lat, t_lng = runway.threshold_for_approach(approach_heading_deg)
    # Translate to the DCS-coord position whose imagery (after offset
    # correction in the basemap) overlays this real-world threshold.
    target_lat = t_lat - entry.imagery_offset_lat
    target_lng = t_lng - entry.imagery_offset_lng
    return DcsPoint.from_latlng(LatLng(target_lat, target_lng), terrain)


def _field_elevation_m(airport: Airport, terrain: Terrain) -> Optional[float]:
    """Return the OSM/DEM-derived field elevation in metres AMSL, or None."""
    return _airport_imagery.field_elevation_for_airport(terrain, airport)


# Distances offered to the scale-bar picker. Imperial-only to match
# cockpit unit conventions: short distances in feet, longer in nautical
# miles. The picker walks this list and chooses the one whose pixel
# length is closest to `target_bar_px` (subject to a min/max so the bar
# is never tiny or wider than the box).
_SCALE_BAR_NICE_DISTANCES: list[tuple[float, str]] = [
    (30.48, "100'"),  # 100 ft
    (152.4, "500'"),
    (304.8, "1000'"),
    (762.0, "2500'"),
    (1852.0, "1 NM"),
    (3704.0, "2 NM"),
    (9260.0, "5 NM"),
    (18520.0, "10 NM"),
    (46300.0, "25 NM"),
    (92600.0, "50 NM"),
    (185200.0, "100 NM"),
]


def _draw_scale_bar(
    draw: ImageDraw.ImageDraw,
    projector: Projector,
    *,
    map_right: int,
    map_bottom: int,
    palette: _Palette,
    target_bar_px: int = 120,
) -> None:
    """Render a graphical map-scale bar in the lower-right of the map area.

    Picks the entry from `_SCALE_BAR_NICE_DISTANCES` whose ground length
    (via projector.meters_to_px) lands closest to `target_bar_px` while
    staying within reasonable pixel bounds — so a tight detail page draws
    e.g. ``500'`` and an overview spanning 75 km draws ``5 NM``, both
    occupying a similar visual width.
    """
    best: Optional[tuple[float, str, int]] = None
    best_diff = float("inf")
    min_px, max_px = 30, 240
    for meters, label in _SCALE_BAR_NICE_DISTANCES:
        px = projector.meters_to_px(meters)
        if px < min_px or px > max_px:
            continue
        diff = abs(px - target_bar_px)
        if diff < best_diff:
            best_diff = diff
            best = (meters, label, px)
    if best is None:
        # Pathological extent: pick the closest match regardless of bounds.
        for meters, label in _SCALE_BAR_NICE_DISTANCES:
            px = projector.meters_to_px(meters)
            diff = abs(px - target_bar_px)
            if diff < best_diff:
                best_diff = diff
                best = (meters, label, px)
    if best is None:
        # The unbounded fallback loop above iterates a non-empty list, so
        # `best` is always set on its first pass. Raising explicitly (rather
        # than asserting) keeps the invariant load-bearing under
        # PYTHONOPTIMIZE=1, where ``assert`` is stripped and the subsequent
        # tuple unpack would fail with a confusing NoneType error.
        raise RuntimeError("scale-bar selection produced no candidate")
    _, label, bar_px = best

    font = load_font(11, bold=True)
    label_w = int(draw.textlength(label, font=font))
    pad_x, pad_y = 8, 6
    inner_w = max(bar_px, label_w)
    box_w = inner_w + pad_x * 2
    box_h = 32
    margin = 8
    box_x1 = map_right - margin
    box_y1 = map_bottom - margin
    box_x0 = box_x1 - box_w
    box_y0 = box_y1 - box_h
    draw.rectangle(
        (box_x0, box_y0, box_x1, box_y1),
        fill=palette.panel_bg,
        outline=palette.panel_outline,
        width=1,
    )
    # Bar: foreground line with tick marks at both ends.
    bar_y = box_y0 + 10
    bar_x0 = box_x0 + (box_w - bar_px) // 2
    bar_x1 = bar_x0 + bar_px
    draw.line((bar_x0, bar_y, bar_x1, bar_y), fill=palette.fg, width=2)
    draw.line((bar_x0, bar_y - 4, bar_x0, bar_y + 4), fill=palette.fg, width=2)
    draw.line((bar_x1, bar_y - 4, bar_x1, bar_y + 4), fill=palette.fg, width=2)
    # Label centered below bar.
    draw.text(
        (box_x0 + (box_w - label_w) // 2, bar_y + 6),
        label,
        fill=palette.fg,
        font=font,
    )


_LABEL_HALO_LIGHT = (255, 255, 255)
_LABEL_HALO_DARK = (0, 0, 0)


def _draw_placed_label(
    draw: ImageDraw.ImageDraw,
    placed: PlacedLabel,
    text: str,
    font: PilFont,
    palette: _Palette,
) -> None:
    """Render a label produced by `place_labels`: foreground text on a
    panel-filled, outlined box, with a leader line back to the marker
    anchor when the placement required one.

    Leader lines and the box outline are stroked twice — a wider
    contrasting halo first, then a thinner core in the opposite shade — so
    the pointer reads against both light terrain (sand, snow) and dark
    terrain (forest, water) without depending on which side of the basemap
    happens to be under the line.
    """
    r = placed.rect
    # Halo is the OPPOSITE shade of the core so one of the two stays
    # visible whichever way the basemap pixels lean. Light theme keeps
    # the historical black core (best contrast on a desaturated tile)
    # and adds a white halo so dark forest/water tiles don't swallow
    # the line; dark theme inverts.
    if palette is _DARK_PALETTE:
        halo = _LABEL_HALO_DARK
        core = _LABEL_HALO_LIGHT
    else:
        halo = _LABEL_HALO_LIGHT
        core = _LABEL_HALO_DARK
    if placed.leader is not None:
        draw.line(
            [placed.leader.src, placed.leader.dest],
            fill=halo,
            width=4,
        )
        draw.line(
            [placed.leader.src, placed.leader.dest],
            fill=core,
            width=2,
        )
    draw.rectangle(
        (r.x0 - 1, r.y0 - 1, r.x1 + 1, r.y1 + 1),
        fill=None,
        outline=halo,
        width=2,
    )
    draw.rectangle(
        (r.x0, r.y0, r.x1, r.y1),
        fill=palette.panel_bg,
        outline=core,
        width=1,
    )
    draw.text((r.x0 + 2, r.y0), text, fill=palette.fg, font=font)


class _RecordingPage(KneeboardPage):
    """Base class that records emitted text strings during ``write()``.

    The ``last_text_log`` buffer is intentional production behavior, not a
    test-only side channel: it costs at most a few dozen short strings per
    page (transient, freed when the page is dropped) and gives tests a
    stable assertion surface without inspecting rendered pixels. The same
    buffer is useful for debugging — dumping ``last_text_log`` after a
    page render shows exactly which strings were emitted and in what order.
    """

    last_text_log: List[str]

    def __init__(self) -> None:
        self.last_text_log = []

    def _record(self, *parts: str) -> None:
        self.last_text_log.extend(parts)


class AirfieldDeparturePage(_RecordingPage):
    """Departure page: spawn parking, active runway, ATIS-like weather."""

    def __init__(
        self,
        *,
        flight: "FlightData",
        game: "Game",
        weather: "Weather",
        dark: bool = False,
    ) -> None:
        super().__init__()
        self.flight = flight
        self.game = game
        self.weather = weather
        self.dark = dark
        self._p = _palette(dark)

    def write(self, path: Path) -> None:
        # Re-arm the per-render text log so a page reused across multiple
        # write() calls (regen after a settings change, repeated test runs
        # against a single instance) emits a clean buffer rather than
        # accumulating entries from every prior render.
        self.last_text_log = []
        p = self._p
        img = Image.new("RGB", (PAGE_W, PAGE_H), p.page_bg)
        draw = ImageDraw.Draw(img)

        airport = _dcs_airport_for_runway(self.flight.departure, self.game.theater)
        # generate_recon_pages only constructs this page when
        # _should_emit_departure has already confirmed the departure resolves
        # to a real pydcs Airport, so airport is never None here. Assert the
        # invariant so a direct (mis)construction fails loudly instead of
        # raising an opaque AttributeError on airport.position below.
        assert airport is not None, (
            "AirfieldDeparturePage requires a runway-backed departure airport; "
            "construct it via generate_recon_pages, which gates on "
            "_should_emit_departure"
        )
        title = (
            f"{self.flight.callsign} -- DEPARTURE -- "
            f"{self.flight.departure.airfield_name}"
        )
        self._record(title)
        y = _title_bar(img, draw, title, p)

        # ATIS block. By convention, ATIS broadcasts always announce zulu
        # alongside local time regardless of the airframe's kneeboard format
        # preference, so always derive zulu from theater.timezone when one is
        # known. None signals "no conversion available" and drops the Z column.
        start_local = self.game.conditions.start_time
        theater_tz = getattr(self.game.theater, "timezone", None)
        if theater_tz is not None:
            start_zulu = start_local.replace(tzinfo=theater_tz).astimezone(
                datetime.timezone.utc
            )
        else:
            start_zulu = None
        sunrise, sunset = self._sun_times(airport.position.latlng())
        block = build_atis_block(
            weather=self.weather,
            start_time_local=start_local,
            start_time_zulu=start_zulu,
            sunrise=sunrise,
            sunset=sunset,
            runway_name=self.flight.departure.runway_name,
            runway_heading_deg=int(self.flight.departure.runway_heading.degrees),
            atc_freq_str=self._format_freq(self.flight.departure.atc),
            tacan_str=self._format_tacan(),
            field_elevation_m=_field_elevation_m(airport, self.game.theater.terrain),
        )
        self._record(f"QNH {block.qnh_inhg:.2f}")
        self._record(f"QFE {block.qfe_display}")
        self._record(f"SUNRISE {block.sunrise or '--'}")
        self._record(f"SUNSET {block.sunset or '--'}")
        draw_atis_block(draw, block, x=0, y=y, width=PAGE_W, height=ATIS_H)
        y += ATIS_H

        # Airfield map area (tile basemap; airfield diagram is the focus)
        map_box = (18, y + 18, PAGE_W - 18, PAGE_H - FOOTER_H - 24)
        x0, y0, x1, y1 = map_box
        map_w = x1 - x0
        map_h = y1 - y0
        # Aspect-correct so projected circles (threshold ring, threat rings)
        # stay circular on a non-square map_box. 2_500 m short-axis half-side
        # gives the ~5 km square minimum scope the airfield diagram was built
        # around; the longer axis grows proportionally.
        extent = square_extent(
            center=airport.position,
            half_side_m=2_500.0,
            pixel_width=map_w,
            pixel_height=map_h,
            terrain=self.game.theater.terrain,
        )
        basemap = render_basemap(
            extent,
            map_w,
            map_h,
            cache_dir=tile_cache_dir(),
            imagery_anchor=airport,
        )
        img.paste(basemap, (x0, y0))
        projector = Projector(extent=extent, pixel_width=map_w, pixel_height=map_h)

        # Pass 1: draw the marker boxes / threshold ring / wind badge and
        # record the pixel rects they occupy. Spawn labels are deferred to a
        # second pass so place_labels can spread them when units cluster.
        spawn_label_font = load_font(11, bold=True)
        spawn_marker_half = 9  # matches draw_spawn_marker default size
        occupied_rects: List[Rect] = []
        spawn_label_requests: List[tuple[LabelRequest, str]] = []
        # FlightData.callsign follows DCS convention "<NAME> N-M" where the
        # final dash separates flight number from element index (e.g.
        # "ENFIELD 1-1"). Strip the element suffix once so per-unit labels
        # re-derive it. If the callsign carries no dash (custom callsign,
        # single-unit ferry, etc.) fall back to the whole string; resulting
        # labels read "<NAME>-1", "<NAME>-2", which is acceptable.
        callsign_base = self.flight.callsign
        last_dash = callsign_base.rfind("-")
        base_callsign = callsign_base[:last_dash] if last_dash != -1 else callsign_base
        for i, unit in enumerate(self.flight.units, start=1):
            px, py = projector.project(unit.position)
            cx, cy = x0 + px, y0 + py
            draw_spawn_marker(draw, (cx, cy))
            occupied_rects.append(
                Rect(
                    cx - spawn_marker_half,
                    cy - spawn_marker_half,
                    cx + spawn_marker_half,
                    cy + spawn_marker_half,
                )
            )
            label = f"{base_callsign}-{i}"
            lw = int(draw.textlength(label, font=spawn_label_font)) + 4
            spawn_label_requests.append(
                (
                    LabelRequest(anchor=(cx, cy), width=lw, height=14),
                    label,
                )
            )

        # Active threshold marker (ring radius 26 — block its area for labels)
        thr = self._compute_threshold_pixel(projector, airport, x0, y0)
        if thr is not None:
            draw_active_threshold_marker(draw, thr)
            tcx, tcy = thr
            occupied_rects.append(Rect(tcx - 26, tcy - 26, tcx + 26, tcy + 26))

        # Wind arrow badge (110x110)
        wind_x = x1 - 70
        wind_y = y0 + 70
        draw_wind_arrow_badge(
            draw,
            (wind_x, wind_y),
            from_dir_deg=block.wind_surface[0],
            speed_kts=block.wind_surface[1],
        )
        occupied_rects.append(Rect(wind_x - 55, wind_y - 55, wind_x + 55, wind_y + 55))

        # Map scale bar — lower-right of the map area.
        _draw_scale_bar(draw, projector, map_right=x1, map_bottom=y1, palette=p)

        # Pass 2: collision-avoiding spawn labels.
        placed = place_labels(
            [lr for lr, _ in spawn_label_requests],
            occupied=occupied_rects,
            page_bbox=Rect(x0, y0, x1, y1),
        )
        for pl, (_, text) in zip(placed, spawn_label_requests):
            _draw_placed_label(draw, pl, text, spawn_label_font, p)

        # Footer
        draw.line(
            (0, PAGE_H - FOOTER_H, PAGE_W, PAGE_H - FOOTER_H),
            fill=p.fg,
            width=1,
        )
        # Prefer the squadron nickname (e.g. "Battling Wyvern") over the raw
        # numeric designation (e.g. "009") which is meaningless to pilots.
        # Fall back to the designation if no nickname is set.
        sq = getattr(self.flight, "squadron", None)
        nickname = getattr(sq, "nickname", None)
        squadron_label = nickname or getattr(sq, "name", "") or ""
        draw.text(
            (18, PAGE_H - FOOTER_H + 8),
            f"Spawn type: {self.flight.start_type.value.upper()}"
            + (f"   |   Squadron: {squadron_label}" if squadron_label else ""),
            fill=p.muted,
            font=load_font(13),
        )

        img.save(path)

    def _format_freq(self, freq: Any) -> str:
        if freq is None:
            return ""
        if not hasattr(freq, "mhz"):
            return str(freq)
        # ITU radio-band conventions: VHF 30-300 MHz, UHF 300-3000 MHz.
        # Covers civil aviation (118-137 MHz), US/NATO military airband
        # (225-400 MHz), East-bloc tactical VHF (30-88 MHz) used by some
        # Russian airframes for ground/ATC comms, and the 156-174 MHz
        # range used by older eastern-bloc air-ground sets.
        mhz = freq.mhz
        if 30.0 <= mhz < 300.0:
            band = "VHF"
        elif 300.0 <= mhz <= 3000.0:
            band = "UHF"
        else:
            band = ""
        return f"{band} {mhz:.3f}".strip()

    def _format_tacan(self) -> str:
        ch = self.flight.departure.tacan
        if ch is None:
            return ""
        callsign = self.flight.departure.tacan_callsign or ""
        return f"{ch} {callsign}".strip()

    def _sun_times(
        self, latlng: Any
    ) -> Tuple[Optional[datetime.time], Optional[datetime.time]]:
        sun = Sun(latlng.lat, latlng.lng)
        # suntime requires datetime; passing date raises TypeError inside utcoffset().
        start = self.game.conditions.start_time
        tz = getattr(self.game.theater, "timezone", None)
        try:
            if tz is not None:
                # suntime returns the UTC moment of sunrise/set on the input
                # date's UTC day. For east-of-Greenwich locations the LOCAL
                # sunrise falls on the PRIOR UTC day (Marianas +10 May 21
                # local sunrise = May 20 ~20:00 UTC); for west-of-Greenwich
                # locations the LOCAL sunset can fall on the NEXT UTC day.
                # Compute the right UTC date independently for each event by
                # converting a representative local hour to UTC.
                sr_local = datetime.datetime(
                    start.year, start.month, start.day, 6, 0, tzinfo=tz
                )
                ss_local = datetime.datetime(
                    start.year, start.month, start.day, 18, 0, tzinfo=tz
                )
                sr_utc_date = sr_local.astimezone(datetime.timezone.utc).date()
                ss_utc_date = ss_local.astimezone(datetime.timezone.utc).date()
                rise_utc = sun.get_sunrise_time(
                    datetime.datetime(
                        sr_utc_date.year, sr_utc_date.month, sr_utc_date.day
                    )
                )
                set_utc = sun.get_sunset_time(
                    datetime.datetime(
                        ss_utc_date.year, ss_utc_date.month, ss_utc_date.day
                    )
                )
            else:
                dt = datetime.datetime(start.year, start.month, start.day)
                rise_utc = sun.get_sunrise_time(dt)
                set_utc = sun.get_sunset_time(dt)
        except SunTimeException:
            return None, None
        # suntime returns tz-aware UTC datetimes. Convert to theater-local
        # time via astimezone — never add utcoffset by hand (would leave the
        # value tagged UTC while really showing local).
        if tz is not None:
            return rise_utc.astimezone(tz).time(), set_utc.astimezone(tz).time()
        return rise_utc.time(), set_utc.time()

    def _compute_threshold_pixel(
        self, projector: Projector, airport: Airport, x0: int, y0: int
    ) -> Optional[Tuple[int, int]]:
        if not airport.runways:
            return None
        # RunwayData.runway_heading is already the approach heading for the
        # active end (RunwayAssigner picks it based on wind). No need to walk
        # the pydcs Runway pair.
        heading_deg = self.flight.departure.runway_heading.degrees
        terrain = self.game.theater.terrain
        threshold_world = _osm_threshold_in_dcs(
            airport,
            heading_deg,
            terrain,
        )
        if threshold_world is None:
            threshold_world = _fallback_threshold_dcs_point(
                airport, heading_deg, terrain
            )
        px, py = projector.project(threshold_world)
        return (x0 + px, y0 + py)


def _footer_panel(
    draw: ImageDraw.ImageDraw,
    *,
    cells: list[tuple[str, str]],
    y_top: int,
    page_width: int,
    palette: _Palette,
) -> None:
    """Draw a multi-column footer bar with label + value pairs."""
    draw.line((0, y_top, page_width, y_top), fill=palette.fg, width=2)
    col_w = page_width // max(len(cells), 1)
    label_font = load_font(13, bold=True)
    value_font = load_font(18, bold=True)
    for i, (k, v) in enumerate(cells):
        cx = i * col_w + 20
        draw.text((cx, y_top + 8), k, fill=palette.muted, font=label_font)
        draw.text((cx, y_top + 26), v, fill=palette.fg, font=value_font)


class OverviewReconPage(_RecordingPage):
    """Overview page: package corridor + target + nearby threats.

    The user's ``extra_threat_search_m`` slider drives ONE knob:
    ``_nearby_threats`` filters TGOs by
    ``corridor.expand(extra_threat_search_m + DEFAULT_THREAT_MARGIN_M)``
    — picking WHICH threats appear on the page. The 20 km default keeps
    relevant threats visible even when the slider is at 0.

    The rendered bbox (``corridor_extent``) is built from waypoints +
    already-filtered threats with only a 10 % cosmetic margin; the slider
    is intentionally NOT plumbed through a second time. Threats forced
    into the bbox via the ``threats=`` arg keep them visible without
    extra whitespace padding.
    """

    FOOTER_H = 72
    # Always include threats within this margin of the corridor bbox even when
    # the user-tunable extra search radius is 0.
    DEFAULT_THREAT_MARGIN_M = 20_000.0  # ~11 nm

    def __init__(
        self,
        *,
        flight: "FlightData",
        game: "Game",
        extra_threat_search_m: float = 0.0,
        dark: bool = False,
    ) -> None:
        super().__init__()
        self.flight = flight
        self.game = game
        self.extra_threat_search_m = extra_threat_search_m
        self.dark = dark
        self._p = _palette(dark)

    def write(self, path: Path) -> None:
        # Re-arm the per-render text log so a page reused across multiple
        # write() calls (regen after a settings change, repeated test runs
        # against a single instance) emits a clean buffer rather than
        # accumulating entries from every prior render.
        self.last_text_log = []
        p = self._p
        img = Image.new("RGB", (PAGE_W, PAGE_H), p.page_bg)
        draw = ImageDraw.Draw(img)

        target = self.flight.package.target
        target_name = _target_display_name(target)
        title = f"{self.flight.callsign} -- RECON OVERVIEW -- {target_name}"
        self._record(title)
        y = _title_bar(img, draw, title, p)

        # Gather waypoint positions. ``FlightWaypoint.waypoint_type`` is
        # non-Optional in production, but defensively skipping any unset
        # entries keeps the page from crashing on a malformed test stub.
        waypoints = [wp.position for wp in self.flight.waypoints]
        if not waypoints:
            waypoints = [target.position]

        # Gather nearby threats as (position, max_range_m, det_range_m, label)
        threats = self._nearby_threats(target, waypoints, self.extra_threat_search_m)

        # Compute map extent from corridor + threat positions. Threats are
        # already passed in via ``threats=`` (which forces the bbox to
        # include their positions), so ``extra_radius_m=0`` here — the
        # slider's effect on bbox size is already baked into which threats
        # show up.
        extent = corridor_extent(
            waypoints=waypoints,
            threats=[t[0] for t in threats],
            extra_radius_m=0.0,
            terrain=self.game.theater.terrain,
        )

        # Basemap area. Markers and threat rings are drawn onto the basemap
        # SUB-IMAGE so PIL's natural clipping prevents them from leaking onto
        # the page background outside the map_box when a feature sits near
        # the extent edge. The basemap is then pasted in one shot. Labels are
        # still drawn on the page-level Draw after paste so they can sit just
        # inside the map_box via place_labels' page_bbox check.
        map_box = (18, y + 14, PAGE_W - 18, PAGE_H - self.FOOTER_H - 8)
        x0, y0, x1, y1 = map_box
        map_w, map_h = x1 - x0, y1 - y0
        # Pad the corridor bbox so its world aspect matches the pixel
        # aspect — without this the tile-warp stretches a typical
        # wide-and-short strike corridor non-uniformly and the basemap
        # reads as horizontally squished.
        extent = aspect_correct(extent, map_w, map_h)
        basemap = render_basemap(extent, map_w, map_h, cache_dir=tile_cache_dir())
        map_draw = ImageDraw.Draw(basemap)
        projector = Projector(extent=extent, pixel_width=map_w, pixel_height=map_h)

        # Track occupied pixel rects (page-pixel coords) for label placement.
        occupied_rects: list[Rect] = []
        # Deferred label requests: (LabelRequest, text, font). Labels are
        # rendered uniformly by _draw_placed_label (black-on-white box);
        # marker color is conveyed by the marker itself, not the label.
        label_requests: List[Tuple[LabelRequest, str, PilFont]] = []

        _label_font = load_font(13, bold=True)

        def _marker_rect(cx: int, cy: int, half: int) -> Rect:
            return Rect(cx - half, cy - half, cx + half, cy + half)

        # Friendly departure CP marker (box drawn now; name deferred for placement)
        dep_airport = _dcs_airport_for_runway(self.flight.departure, self.game.theater)
        if dep_airport is not None and extent.contains(dep_airport.position):
            dx, dy = projector.project(dep_airport.position)
            cp_size = 11
            # Box only — name is added below via the label-collision pass.
            map_draw.rectangle(
                (dx - cp_size, dy - cp_size, dx + cp_size, dy + cp_size),
                fill=FRIENDLY_FILL,
                outline=FRIENDLY_OUTLINE,
                width=2,
            )
            cp_cx, cp_cy = x0 + dx, y0 + dy
            occupied_rects.append(_marker_rect(cp_cx, cp_cy, cp_size))
            cp_label = self.flight.departure.airfield_name
            lw = int(draw.textlength(cp_label, font=_label_font)) + 4
            lh = 18
            label_requests.append(
                (
                    LabelRequest(anchor=(cp_cx, cp_cy), width=lw, height=lh),
                    cp_label,
                    _label_font,
                )
            )

        # Enemy threats with rings
        for threat_pos, max_r_m, det_r_m, threat_label in threats:
            tx, ty = projector.project(threat_pos)
            draw_threat_rings(
                map_draw,
                (tx, ty),
                max_range_px=projector.meters_to_px(max_r_m),
                detection_range_px=projector.meters_to_px(det_r_m),
            )
            draw_sidc_enemy(map_draw, (tx, ty), "A")
            sidc_half = 13  # half the default SIDC diamond size (26)
            occupied_rects.append(_marker_rect(x0 + tx, y0 + ty, sidc_half))
            # Defer threat name label through place_labels for collision avoidance.
            lw = int(draw.textlength(threat_label, font=_label_font)) + 4
            lh = 18
            label_requests.append(
                (
                    LabelRequest(anchor=(x0 + tx, y0 + ty), width=lw, height=lh),
                    threat_label,
                    _label_font,
                )
            )

        # Target cluster marker
        tgt_px, tgt_py = projector.project(target.position)
        draw_aimpoint_badge(map_draw, (tgt_px, tgt_py), "T")
        occupied_rects.append(_marker_rect(x0 + tgt_px, y0 + tgt_py, 18))

        # Paste the fully-drawn basemap (with markers/rings clipped to its
        # bounds) onto the page.
        img.paste(basemap, (x0, y0))

        # --- Collision-avoiding label placement ---
        page_bbox = Rect(x0, y0, x1, y1)
        only_requests = [lr for lr, *_ in label_requests]
        placed = place_labels(
            only_requests, occupied=occupied_rects, page_bbox=page_bbox
        )
        for pl, (_, text, font) in zip(placed, label_requests):
            _draw_placed_label(draw, pl, text, font, p)
            self._record(text)

        # Map scale bar — lower-right of the map area. Replaces the prior
        # "1:N" SCALE cell that lived in the footer panel.
        _draw_scale_bar(draw, projector, map_right=x1, map_bottom=y1, palette=p)
        # Threat-ring legend in the bottom-left so pilots can decode the
        # solid vs dashed rings without guessing.
        _draw_threat_ring_legend(
            draw,
            bottom_right=(x0 + 186, y1 - 6),
            palette=p,
        )

        # Footer: just bullseye bearing/range now.
        bullseye_pos = self.game.coalition_for(self.flight.friendly).bullseye.position
        bearing, range_nm = bullseye_bearing_range_nm(bullseye_pos, target.position)
        # Spec example uses no spaces: TARGET BE: 087°/22 NM.
        be_str = f"{int(bearing.degrees):03d}°/{range_nm:.0f} NM"
        self._record(f"TARGET BE: {be_str}")
        _footer_panel(
            draw,
            cells=[("TARGET BE", be_str)],
            y_top=PAGE_H - self.FOOTER_H,
            page_width=PAGE_W,
            palette=p,
        )
        img.save(path)

    def _nearby_threats(
        self,
        target: Any,
        waypoints: List[Any],
        search_radius_m: float,
    ) -> List[Tuple[Any, ...]]:
        """Return enemy threats inside the corridor bbox grown by ``search_radius_m``.

        Without this filter, a theater-wide enemy IADS would balloon the
        overview extent to span the entire map.
        """
        corridor = MapExtent(
            min_x=min(p.x for p in waypoints),
            max_x=max(p.x for p in waypoints),
            min_y=min(p.y for p in waypoints),
            max_y=max(p.y for p in waypoints),
            terrain=self.game.theater.terrain,
        ).expand(search_radius_m + self.DEFAULT_THREAT_MARGIN_M)
        threats: List[Tuple[Any, ...]] = []
        for cp in self.game.theater.controlpoints:
            for tgo in cp.ground_objects:
                if tgo is target:
                    continue
                # Cheap position check first — skips the threat-range
                # method calls (which walk every unit) for the vast
                # majority of TGOs that fall outside the corridor.
                if not corridor.contains(tgo.position):
                    continue
                if tgo.is_friendly(self.flight.friendly):
                    continue
                max_r = tgo.max_threat_range().meters
                det_r = tgo.max_detection_range().meters
                if max_r == 0 and det_r == 0:
                    continue
                threats.append((tgo.position, max_r, det_r, tgo.obj_name))
        return threats


class DetailReconPage(_RecordingPage):
    """Detail page: tight zoom + per-aimpoint table + attack axis."""

    TABLE_H = 240
    FOOTER_H = 32

    def __init__(
        self,
        *,
        flight: "FlightData",
        game: "Game",
        dark: bool = False,
    ) -> None:
        super().__init__()
        self.flight = flight
        self.game = game
        self.dark = dark
        self._p = _palette(dark)

    def write(self, path: Path) -> None:
        # Re-arm the per-render text log so a page reused across multiple
        # write() calls (regen after a settings change, repeated test runs
        # against a single instance) emits a clean buffer rather than
        # accumulating entries from every prior render.
        self.last_text_log = []
        p = self._p
        img = Image.new("RGB", (PAGE_W, PAGE_H), p.page_bg)
        draw = ImageDraw.Draw(img)

        target = self.flight.package.target
        target_name = _target_display_name(target)
        title = f"{self.flight.callsign} -- RECON DETAIL -- {target_name}"
        self._record(title)
        y = _title_bar(img, draw, title, p)

        aimpoints = self._build_aimpoints(target)

        map_h = PAGE_H - y - self.TABLE_H - self.FOOTER_H - 16
        map_box = (18, y + 14, PAGE_W - 18, y + 14 + map_h)
        x0, y0, x1, y1 = map_box
        map_w = x1 - x0

        # Tight extent around all aimpoints with a 300 m margin.
        xs = [a.position.x for a in aimpoints] + [target.position.x]
        ys = [a.position.y for a in aimpoints] + [target.position.y]
        extent = MapExtent(
            min_x=min(xs) - 300.0,
            max_x=max(xs) + 300.0,
            min_y=min(ys) - 300.0,
            max_y=max(ys) + 300.0,
            terrain=self.game.theater.terrain,
        )
        # Detail extents are tight; the tile compositor picks a high zoom so
        # the satellite background stays sharp. Markers + attack axis arrow
        # are drawn onto the basemap sub-image so PIL clips them to map_box
        # bounds (the IP for a small detail extent often projects far
        # outside the visible area — without clipping, the arrow line bled
        # across the page footer/table).
        basemap = render_basemap(extent, map_w, map_h, cache_dir=tile_cache_dir())
        map_draw = ImageDraw.Draw(basemap)
        projector = Projector(extent=extent, pixel_width=map_w, pixel_height=map_h)

        # Attack axis arrow (drawn on basemap so it clips at the map edge).
        ip_pos = self._inbound_ip_position()
        if ip_pos is not None:
            self._draw_attack_axis(
                map_draw,
                projector,
                ip_pos,
                target.position,
                map_w,
                map_h,
                p,
            )

        # Aimpoints — building footprints first, then badges.
        for a in aimpoints:
            px, py = projector.project(a.position)
            if a.footprint is not None:
                corners = [projector.project(p) for p in a.footprint.points]
                draw_building_footprint(map_draw, corners)
            draw_aimpoint_badge(map_draw, (px, py), a.label, dead=a.is_dead)

        # Paste the fully-drawn basemap (arrow + footprints + badges all
        # clipped to map_box bounds).
        img.paste(basemap, (x0, y0))

        # Map scale bar — lower-right of the map area.
        _draw_scale_bar(draw, projector, map_right=x1, map_bottom=y1, palette=p)

        # Aimpoint table.
        table_y = y + 14 + map_h + 12
        self._draw_aimpoint_table(draw, aimpoints, table_y, p)

        # Footer.
        bullseye = self.game.coalition_for(self.flight.friendly).bullseye.position
        bearing, range_nm = bullseye_bearing_range_nm(bullseye, target.position)
        # Spec example uses no spaces around `/`.
        be_str = f"{int(bearing.degrees):03d}°/{range_nm:.0f} NM"
        # Record the bullseye string for test/debug parity with OverviewReconPage.
        self._record(f"TARGET BE: {be_str}")
        draw.line(
            (0, PAGE_H - self.FOOTER_H, PAGE_W, PAGE_H - self.FOOTER_H),
            fill=p.fg,
            width=1,
        )
        draw.text(
            (20, PAGE_H - self.FOOTER_H + 6),
            f"TARGET BE {be_str}   |   BRG = bearing from TGT waypoint to aimpoint",
            fill=p.muted,
            font=load_font(13),
        )
        img.save(path)

    CLUSTER_THRESHOLD_M = 75.0
    CLUSTER_CAP = 12

    def _build_aimpoints(self, target: Any) -> List[Aimpoint]:
        units = list(getattr(target, "strike_targets", None) or [])
        # Fallback to all live units if strike_targets is empty (CAS / armed recon).
        if not units:
            raw_units = getattr(target, "units", [])
            # units may be a callable (method) or a property/list
            if callable(raw_units):
                raw_units = raw_units()
            units = [u for u in (raw_units or []) if getattr(u, "alive", True)]

        groups = cluster_items(
            units,
            position_of=lambda u: u.position,
            threshold_m=self.CLUSTER_THRESHOLD_M,
            cap=self.CLUSTER_CAP,
        )
        return [
            self._aimpoint_from_group(idx, members, trailing, target)
            for idx, (members, trailing) in enumerate(groups, start=1)
        ]

    def _aimpoint_from_group(
        self,
        number: int,
        members: List[Any],
        trailing: bool,
        target: Any,
    ) -> Aimpoint:
        from game.utils import Heading

        terrain = self.game.theater.terrain
        if len(members) == 1 and not trailing:
            u = members[0]
            position = u.position
            description = self._describe_unit(u)
            footprint = self._unit_footprint(u, terrain)
            is_dead = not getattr(u, "alive", True)
        else:
            position = _centroid(members, terrain)
            description = self._describe_cluster(members, trailing)
            footprint = None
            is_dead = all(not getattr(m, "alive", True) for m in members)
        heading = Heading.from_degrees(
            round(target.position.heading_between_point(position)) % 360
        )
        return Aimpoint(
            number=number,
            description=description,
            position=position,
            heading_from_center=heading,
            footprint=footprint,
            is_dead=is_dead,
            cluster_size=len(members),
            is_trailing=trailing,
        )

    @staticmethod
    def _unit_footprint(u: Any, terrain: Terrain) -> Any:
        from dcs.mapping import Polygon

        unit_type = getattr(u, "type", None)
        length = getattr(unit_type, "length", None)
        width = getattr(unit_type, "width", None)
        if not (length and width):
            return None
        hx, hy = length / 2, width / 2
        pts = [
            DcsPoint(u.position.x - hx, u.position.y - hy, terrain),
            DcsPoint(u.position.x + hx, u.position.y - hy, terrain),
            DcsPoint(u.position.x + hx, u.position.y + hy, terrain),
            DcsPoint(u.position.x - hx, u.position.y + hy, terrain),
        ]
        return Polygon(terrain, points=pts)

    def _describe_cluster(self, members: List[Any], trailing: bool) -> str:
        if trailing:
            return f"{len(members)} units (... remaining)"
        sample = self._describe_unit(members[0])
        return f"{sample} ({len(members)}×)"

    def _describe_unit(self, unit: Any) -> str:
        """Return a description for an aimpoint unit.

        For air-defence units, the description uses the SAM-component role
        label (SR, TR, TEL, LN) followed by the ALIC code in parentheses when
        available.  This matches the SEAD/DEAD aimpoint-description spec
        regardless of flight type — if the unit IS a TR or LN, label it as
        such for any striking flight.

        Fallback: generic unit-type name (original behaviour).
        """
        unit_type = getattr(unit, "type", None)
        role: Optional[str] = None
        if unit_type is not None:
            # Order matters: TELARs are launchers WITH a track radar, so
            # they appear in both TELARS and LAUNCHER_TRACKER_PAIRS. The
            # more-specific label ("TEL") must win over the general
            # launcher label ("LN"). Likewise TRACK_RADARS is checked
            # first because a track radar that is itself a launcher
            # (some Patriot variants) reads as "TR" to a SEAD striker
            # rather than "LN".
            if unit_type in TRACK_RADARS:
                role = "TR"
            elif unit_type in TELARS:
                role = "TEL"
            elif unit_type in LAUNCHER_TRACKER_PAIRS:
                role = "LN"
            elif unit_type in UNITS_WITH_RADAR:
                # EWR / acquisition / search radars: labelled "SR".
                role = "SR"
        if role is not None:
            try:
                alic = str(AlicCodes.code_for(unit))
                return f"{role} ({alic})"
            except KeyError:
                return role
        # str() the fallback so MagicMock-typed test stubs don't leak a non-
        # string into the last_text_log (which would break any consumer
        # calling .startswith() on the recorded descriptions).
        fallback = (
            getattr(unit_type, "name", None) or getattr(unit, "name", None) or "TARGET"
        )
        return str(fallback)

    def _draw_attack_axis(
        self,
        draw: ImageDraw.ImageDraw,
        projector: Projector,
        ip_pos: Any,
        target_pos: Any,
        map_w: int,
        map_h: int,
        palette: _Palette,
    ) -> None:
        """Draw the IP→TGT arrow onto the basemap-local Draw.

        Coordinates are map-local (0..map_w, 0..map_h); PIL clips line
        primitives to that canvas automatically, so an IP far outside the
        detail extent won't bleed across the page below.
        """
        sx, sy = projector.project(ip_pos)
        ex, ey = projector.project(target_pos)
        dx, dy = ex - sx, ey - sy
        L = max(math.hypot(dx, dy), 1.0)
        ex2 = ex + int(dx / L * 60)
        ey2 = ey + int(dy / L * 60)
        draw.line((sx, sy, ex2, ey2), fill=palette.fg, width=3)
        ang = math.atan2(ey2 - sy, ex2 - sx)
        ah = math.radians(22)
        for sign in (-1, +1):
            a = ang + math.pi - sign * ah
            draw.line(
                (ex2, ey2, ex2 + int(18 * math.cos(a)), ey2 + int(18 * math.sin(a))),
                fill=palette.fg,
                width=3,
            )
        # Compass heading must come from world coordinates: pixel-space atan2 is
        # rotated 90° (pixel +x = east, pixel -y = north) so deriving it from
        # `ang` mislabels every axis (e.g. due-north target → 270° instead of 0°).
        hdg_deg = int(round(ip_pos.heading_between_point(target_pos))) % 360
        text = f"Attack Axis {hdg_deg:03d}°"
        self._record(text)
        # Label midpoint computed from IP CLAMPED to the visible map bounds,
        # so when the IP projects off-canvas the label still sits along the
        # arrow's visible portion instead of off-screen.
        sx_c = max(0, min(map_w - 1, sx))
        sy_c = max(0, min(map_h - 1, sy))
        mx, my = (sx_c + ex2) // 2, (sy_c + ey2) // 2
        # Size the box to the actual text (was previously a fixed 140x28
        # with lots of dead whitespace on either side of the text).
        font = load_font(13, bold=True)
        tw = int(draw.textlength(text, font=font))
        th = 16
        pad_x, pad_y = 6, 3
        box_hw = tw // 2 + pad_x
        box_hh = th // 2 + pad_y
        mx = max(box_hw + 2, min(map_w - box_hw - 2, mx))
        my = max(box_hh + 2, min(map_h - box_hh - 2, my))
        draw.rectangle(
            (mx - box_hw, my - box_hh, mx + box_hw, my + box_hh),
            fill=palette.page_bg,
            outline=palette.fg,
            width=1,
        )
        draw.text(
            (mx - tw // 2, my - th // 2 - 1),
            text,
            fill=palette.fg,
            font=font,
        )

    def _draw_aimpoint_table(
        self,
        draw: ImageDraw.ImageDraw,
        aimpoints: list[Aimpoint],
        y_top: int,
        palette: _Palette,
    ) -> None:
        draw.line((0, y_top - 4, PAGE_W, y_top - 4), fill=palette.fg, width=2)
        # BRG = bearing from the package target waypoint (center of the TGO)
        # to this aimpoint. The footer line below the table calls this out.
        cols = [
            (18, "#"),
            (62, "DESCRIPTION"),
            (300, "MGRS"),
            (540, "DMS"),
            (820, "BRG"),
        ]
        hdr_font = load_font(14, bold=True)
        row_font = load_font(13)
        for x, h in cols:
            draw.text((x, y_top), h, fill=palette.muted, font=hdr_font)
        row_y = y_top + 22
        for a in aimpoints:
            mgrs_str = point_to_mgrs(a.position)
            dms_str = a.position.latlng().format_dms(include_decimal_seconds=True)
            color = palette.destroyed if a.is_dead else palette.fg
            desc = a.description + (" (DESTROYED)" if a.is_dead else "")
            self._record(a.label)
            # Record the description exactly as drawn so debug/test
            # consumers see the same text the pilot sees, including the
            # "(DESTROYED)" suffix on dead aimpoints.
            self._record(desc)
            self._record(mgrs_str)
            values = [
                a.label,
                desc,
                mgrs_str,
                dms_str,
                f"{round(a.heading_from_center.degrees):03d}°",
            ]
            for (x, _), v in zip(cols, values):
                draw.text((x, row_y), v, fill=color, font=row_font)
                if a.is_dead and v:
                    # Per-cell strikethrough: ask PIL for the actual rendered
                    # bounding box (left, top, right, bottom) so the line
                    # spans exactly the text in each column, not a fixed
                    # 380px slab that misses the right-hand cells.
                    bbox = draw.textbbox((x, row_y), v, font=row_font)
                    mid_y = (bbox[1] + bbox[3]) // 2
                    draw.line(
                        (bbox[0], mid_y, bbox[2], mid_y),
                        fill=color,
                        width=1,
                    )
            row_y += 22

    # Waypoint types treated as the inbound IP for the attack-axis arrow.
    # Listed explicitly (rather than derived by substring match on
    # FlightWaypointType.name) so adding a new enum member can't silently
    # change classification — every new ingress/target type needs an
    # intentional edit here.
    _INGRESS_TYPES = frozenset(
        {
            FlightWaypointType.INGRESS_AIR_ASSAULT,
            FlightWaypointType.INGRESS_ANTI_SHIP,
            FlightWaypointType.INGRESS_ARMED_RECON,
            FlightWaypointType.INGRESS_BAI,
            FlightWaypointType.INGRESS_CAS,
            FlightWaypointType.INGRESS_DEAD,
            FlightWaypointType.INGRESS_ESCORT,
            FlightWaypointType.INGRESS_OCA_AIRCRAFT,
            FlightWaypointType.INGRESS_OCA_RUNWAY,
            FlightWaypointType.INGRESS_SEAD,
            FlightWaypointType.INGRESS_SEAD_SWEEP,
            FlightWaypointType.INGRESS_STRIKE,
            FlightWaypointType.INGRESS_SWEEP,
        }
    )
    _TARGET_TYPES = frozenset(
        {
            FlightWaypointType.TARGET_POINT,
            FlightWaypointType.TARGET_GROUP_LOC,
            FlightWaypointType.TARGET_SHIP,
        }
    )

    def _inbound_ip_position(self) -> Optional[Any]:
        for wp in self.flight.waypoints:
            if wp.waypoint_type in self._INGRESS_TYPES:
                return wp.position
        # No explicit ingress: fall back to the last non-target waypoint before
        # the first target waypoint, which is the closest thing to an IP we have.
        last_pre_target = None
        for wp in self.flight.waypoints:
            if wp.waypoint_type in self._TARGET_TYPES:
                break
            last_pre_target = wp
        return last_pre_target.position if last_pre_target is not None else None


# Priority for picking the "greatest threat" label/ring on a live TGO.
# Lower = higher priority. Matches the user-supplied ranking:
# track radar > unguided/self-guided missile launcher > AAA > tank > other.
_THREAT_PRIORITY: dict[UnitClass, int] = {
    UnitClass.TRACK_RADAR: 1,
    UnitClass.SEARCH_TRACK_RADAR: 1,
    UnitClass.SEARCH_RADAR: 1,
    UnitClass.SPECIALIZED_RADAR: 1,
    UnitClass.LAUNCHER: 2,
    UnitClass.TELAR: 2,
    UnitClass.MANPAD: 2,
    UnitClass.SHORAD: 2,
    UnitClass.AAA: 3,
    UnitClass.TANK: 4,
    UnitClass.IFV: 5,
    UnitClass.APC: 5,
    UnitClass.ARTILLERY: 5,
    UnitClass.ATGM: 5,
}
_THREAT_PRIORITY_DEFAULT = 9


def _threat_priority_for(unit_type: Any) -> int:
    cls = getattr(unit_type, "unit_class", None)
    if cls is None:
        return _THREAT_PRIORITY_DEFAULT
    return _THREAT_PRIORITY.get(cls, _THREAT_PRIORITY_DEFAULT)


def _greatest_alive_threat(tgo: Any) -> Optional[Tuple[str, int]]:
    """Return (display_name, alive_count) for the highest-priority live unit type.

    Returns None only when the TGO has no live units at all. A TGO with live
    units that all lack a classified ``unit_type`` (pydcs data gap, exotic
    static prop) still reports as alive — the dispatcher must not confuse
    "unclassified" with "destroyed", since drawing a destroyed marker over a
    live enemy presence is a tactical lie.
    """
    classified_counts: Dict[Any, int] = {}
    alive_count = 0
    for group in getattr(tgo, "groups", []):
        for unit in getattr(group, "units", []):
            if not getattr(unit, "alive", False):
                continue
            alive_count += 1
            ut = getattr(unit, "unit_type", None)
            if ut is None:
                continue
            classified_counts[ut] = classified_counts.get(ut, 0) + 1
    if alive_count == 0:
        return None
    if not classified_counts:
        return ("Unknown", alive_count)
    chosen_ut = min(
        classified_counts.items(),
        key=lambda kv: (_threat_priority_for(kv[0]), -kv[1]),
    )[0]
    display_name: str = getattr(chosen_ut, "display_name", None) or str(chosen_ut)
    return (display_name, classified_counts[chosen_ut])


def _draw_dead_marker(draw: ImageDraw.ImageDraw, center: tuple[int, int]) -> None:
    """Render a 'completely destroyed' icon — black filled disc with white X."""
    cx, cy = center
    r = 9
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(0, 0, 0), outline=(0, 0, 0))
    draw.line((cx - 5, cy - 5, cx + 5, cy + 5), fill=(255, 255, 255), width=2)
    draw.line((cx - 5, cy + 5, cx + 5, cy - 5), fill=(255, 255, 255), width=2)


def _draw_threat_ring_legend(
    draw: ImageDraw.ImageDraw,
    *,
    bottom_right: tuple[int, int],
    palette: "_Palette",
) -> None:
    """Swatch legend explaining the two threat-ring styles.

    Solid red circle = max weapon engagement range; dashed red = detection
    range. Anchored by its bottom-right corner so callers can pin it to any
    map_box edge.
    """
    font = load_font(10, bold=True)
    w, h = 168, 50
    bx, by = bottom_right
    x0, y0, x1, y1 = bx - w, by - h, bx, by
    draw.rectangle((x0, y0, x1, y1), fill=palette.panel_bg, outline=palette.fg, width=1)
    cx, cy = x0 + 14, y0 + 14
    draw.ellipse((cx - 7, cy - 7, cx + 7, cy + 7), outline=(180, 20, 20), width=2)
    draw.text((x0 + 30, y0 + 7), "Max threat range", fill=palette.fg, font=font)
    cx, cy = x0 + 14, y0 + 34
    for i in range(20):
        a0 = i * 360 / 20
        a1 = a0 + 360 / 40
        if i % 2 == 0:
            draw.arc(
                (cx - 7, cy - 7, cx + 7, cy + 7),
                start=a0,
                end=a1,
                fill=(180, 20, 20),
                width=2,
            )
    draw.text((x0 + 30, y0 + 27), "Detection range", fill=palette.fg, font=font)


class FrontLineDetailPage(_RecordingPage):
    """Detail page for CAS-style targets whose ``package.target`` is a FrontLine.

    Aspect-correct square scope centered on the active conflict point (~20 nm
    short-axis half-side). Draws the active frontline segment as a single bold
    line so the line-of-contact reads unambiguously, plus the in-scope TGOs:

    * BuildingGroundObject + EwrGroundObject are filtered out — neither
      contributes to the CAS engagement picture.
    * TGOs with no living units render as a black destroyed-marker (no rings,
      no label) so the pilot can confirm prior hits without re-engaging.
    * Live TGOs render labelled with their greatest-threat unit type + count
      (e.g. "SA-6", "Marder x3"); enemy threat rings come from the worst
      live anti-air range and shrink as units die in earlier turns.

    Footer carries the bullseye bearing/range to the frontline center.
    """

    FOOTER_H = 72
    # 20 nm short-axis half-side (~37 km). square_extent grows the longer pixel
    # axis proportionally so threat rings stay circular on non-square map_box.
    HALF_SIDE_M = 20.0 * 1852.0 / 2.0

    def __init__(
        self,
        *,
        flight: "FlightData",
        game: "Game",
        dark: bool = False,
    ) -> None:
        super().__init__()
        self.flight = flight
        self.game = game
        self.dark = dark
        self._p = _palette(dark)

    def write(self, path: Path) -> None:
        self.last_text_log = []
        p = self._p
        img = Image.new("RGB", (PAGE_W, PAGE_H), p.page_bg)
        draw = ImageDraw.Draw(img)

        front = cast(FrontLine, self.flight.package.target)
        title = f"{self.flight.callsign} -- FRONTLINE -- {front.name}"
        self._record(title)
        y = _title_bar(img, draw, title, p)

        map_box = (18, y + 14, PAGE_W - 18, PAGE_H - self.FOOTER_H - 8)
        x0, y0, x1, y1 = map_box
        map_w, map_h = x1 - x0, y1 - y0
        center = front.position
        extent = square_extent(
            center=center,
            half_side_m=self.HALF_SIDE_M,
            pixel_width=map_w,
            pixel_height=map_h,
            terrain=self.game.theater.terrain,
        )
        basemap = render_basemap(extent, map_w, map_h, cache_dir=tile_cache_dir())
        map_draw = ImageDraw.Draw(basemap)
        projector = Projector(extent=extent, pixel_width=map_w, pixel_height=map_h)

        occupied_rects: list[Rect] = []
        label_requests: List[Tuple[LabelRequest, str, PilFont]] = []
        _label_font = load_font(13, bold=True)

        def _marker_rect(cx_p: int, cy_p: int, half: int) -> Rect:
            return Rect(cx_p - half, cy_p - half, cx_p + half, cy_p + half)

        # Front line of contact: draw the perpendicular bounds line that
        # matches the orange polyline on the main planner map (see
        # FrontLineConflictDescription.frontline_bounds and
        # client/src/components/frontline/FrontLine.tsx). The bounds extend
        # `max_frontline_width / 2` km perpendicular to the active route
        # tangent on each side of the conflict center; PIL clips the line
        # to the basemap canvas when the bounds reach beyond the visible
        # extent. Earlier the page drew the convoy route segment itself,
        # which read as an arbitrary red diagonal unrelated to the line of
        # contact on the planner map.
        left_pos, right_pos = _frontline_bounds_points(
            front,
            self.game,
            terrain=self.game.theater.terrain,
        )
        if left_pos is not None and right_pos is not None:
            left_px = projector.project(left_pos)
            right_px = projector.project(right_pos)
            map_draw.line(
                [left_px, right_px],
                fill=(254, 125, 10),
                width=10,
            )

        # Center marker (active conflict): orange diamond drawn over the
        # bounds line so the engagement point is obvious without
        # overloading the friendly/enemy color contract.
        cx, cy = projector.project(center)
        diamond = [(cx, cy - 9), (cx + 9, cy), (cx, cy + 9), (cx - 9, cy)]
        map_draw.polygon(diamond, fill=(255, 165, 0), outline=(80, 40, 0))
        occupied_rects.append(_marker_rect(x0 + cx, y0 + cy, 12))

        # TGOs in scope, filtered + classified per the CAS-page contract.
        for cp in self.game.theater.controlpoints:
            for tgo in cp.ground_objects:
                if not extent.contains(tgo.position):
                    continue
                if isinstance(tgo, (BuildingGroundObject, EwrGroundObject)):
                    continue
                tx, ty = projector.project(tgo.position)
                threat = _greatest_alive_threat(tgo)
                friendly = tgo.is_friendly(self.flight.friendly)
                if threat is None:
                    if friendly:
                        # Dead friendly TGO: skip — black-skull markers mean
                        # "destroyed enemy" and painting one over a fallen
                        # friendly asset would lie to the pilot. Leave the
                        # square gap so they notice it's gone.
                        continue
                    # All enemy units destroyed — black skull-style marker,
                    # no rings, no label so the pilot can confirm prior
                    # hits at a glance.
                    _draw_dead_marker(map_draw, (tx, ty))
                    occupied_rects.append(_marker_rect(x0 + tx, y0 + ty, 11))
                    continue
                if friendly:
                    map_draw.rectangle(
                        (tx - 7, ty - 7, tx + 7, ty + 7),
                        fill=FRIENDLY_FILL,
                        outline=FRIENDLY_OUTLINE,
                        width=2,
                    )
                    occupied_rects.append(_marker_rect(x0 + tx, y0 + ty, 9))
                else:
                    # max_threat_range / max_detection_range already exclude
                    # dead units (TheaterUnit.threat_range returns 0 when dead),
                    # so the ring shrinks to the worst LIVE weapon range.
                    max_r = tgo.max_threat_range().meters
                    det_r = tgo.max_detection_range().meters
                    if max_r > 0 or det_r > 0:
                        draw_threat_rings(
                            map_draw,
                            (tx, ty),
                            max_range_px=projector.meters_to_px(max_r),
                            detection_range_px=projector.meters_to_px(det_r),
                        )
                    draw_sidc_enemy(map_draw, (tx, ty), "G")
                    occupied_rects.append(_marker_rect(x0 + tx, y0 + ty, 13))
                # Label = greatest-threat unit type + count (e.g. "Marder x3").
                name, n = threat
                label_text = name if n <= 1 else f"{name} x{n}"
                lw = int(draw.textlength(label_text, font=_label_font)) + 4
                label_requests.append(
                    (
                        LabelRequest(anchor=(x0 + tx, y0 + ty), width=lw, height=18),
                        label_text,
                        _label_font,
                    )
                )

        img.paste(basemap, (x0, y0))

        page_bbox = Rect(x0, y0, x1, y1)
        only_requests = [lr for lr, *_ in label_requests]
        placed = place_labels(
            only_requests, occupied=occupied_rects, page_bbox=page_bbox
        )
        for pl, (_, text, font) in zip(placed, label_requests):
            _draw_placed_label(draw, pl, text, font, p)
            self._record(text)

        _draw_scale_bar(draw, projector, map_right=x1, map_bottom=y1, palette=p)
        # Threat-ring legend in the bottom-left so it does not collide with the
        # scale bar (which sits in the bottom-right of the map area).
        _draw_threat_ring_legend(
            draw,
            bottom_right=(x0 + 186, y1 - 6),
            palette=p,
        )

        bullseye_pos = self.game.coalition_for(self.flight.friendly).bullseye.position
        bearing, range_nm = bullseye_bearing_range_nm(bullseye_pos, center)
        be_str = f"{int(bearing.degrees):03d}°/{range_nm:.0f} NM"
        self._record(f"FRONT BE: {be_str}")
        _footer_panel(
            draw,
            cells=[("FRONT BE", be_str)],
            y_top=PAGE_H - self.FOOTER_H,
            page_width=PAGE_W,
            palette=p,
        )
        img.save(path)


class AirbaseReconPage(_RecordingPage):
    """Airbase-as-target variant of the recon detail page.

    Used for OCA Aircraft and OCA Runway packages whose target is an
    Airfield ControlPoint (i.e. ``cp.dcs_airport`` is not None).
    """

    # Visual cap on parking-slot markers drawn on the airfield diagram.
    # The diagram is busy enough at 8; more slots make it unreadable.
    PARKING_MARKER_LIMIT = 8

    FOOTER_H = 32

    # Table sits between the map (bottom at PAGE_H-280) and the footer
    # band. Available rows: floor((280 - 20 header gap - 32 footer) / 22)
    # = 10. A multi-runway airfield can produce more thresholds than will
    # fit (5 runways = 10 rows, 6 = 12); cap to keep the table off the
    # footer.
    _THRESHOLD_ROW_CAP = 10

    def __init__(
        self,
        *,
        flight: "FlightData",
        game: "Game",
        dark: bool = False,
    ) -> None:
        super().__init__()
        self.flight = flight
        self.game = game
        self.dark = dark
        self._p = _palette(dark)

    def write(self, path: Path) -> None:
        # Re-arm the per-render text log so a page reused across multiple
        # write() calls (regen after a settings change, repeated test runs
        # against a single instance) emits a clean buffer rather than
        # accumulating entries from every prior render.
        self.last_text_log = []
        p = self._p
        img = Image.new("RGB", (PAGE_W, PAGE_H), p.page_bg)
        draw = ImageDraw.Draw(img)

        cp = cast(ControlPoint, self.flight.package.target)
        airport = cp.dcs_airport
        title = f"{self.flight.callsign} -- AIRFIELD LAYOUT -- {cp.name}"
        self._record(title)
        y = _title_bar(img, draw, title, p)

        if airport is None:
            # Dispatcher gates this page on dcs_airport being non-None, but
            # a stale target ref or future refactor would otherwise crash
            # mid-render. Emit the title-only page and bail.
            img.save(path)
            return

        # Map area: tight box around airport (3 km radius).
        map_box = (18, y + 14, PAGE_W - 18, PAGE_H - 280)
        x0, y0, x1, y1 = map_box
        map_w, map_h = x1 - x0, y1 - y0
        extent = MapExtent(
            min_x=airport.position.x - 1_500.0,
            max_x=airport.position.x + 1_500.0,
            min_y=airport.position.y - 1_500.0,
            max_y=airport.position.y + 1_500.0,
            terrain=self.game.theater.terrain,
        )
        basemap = render_basemap(
            extent,
            map_w,
            map_h,
            cache_dir=tile_cache_dir(),
            imagery_anchor=airport,
        )
        map_draw = ImageDraw.Draw(basemap)
        projector = Projector(extent=extent, pixel_width=map_w, pixel_height=map_h)

        # Runway threshold markers (drawn on basemap sub-image so they clip
        # cleanly if a threshold projects near the edge). We don't know the
        # defender's active runway (DCS picks at mission start based on local
        # wind), so no row is marked "in use" — pilots must read both
        # threshold MGRSs.
        thresholds = self._compute_thresholds(airport)
        if len(thresholds) > self._THRESHOLD_ROW_CAP:
            logger.debug(
                "Airfield %s has %d runway thresholds; truncating to %d to "
                "keep table inside the page footer.",
                cp.name,
                len(thresholds),
                self._THRESHOLD_ROW_CAP,
            )
            thresholds = thresholds[: self._THRESHOLD_ROW_CAP]
        aimpoint_rows: list[tuple[str, str, str]] = []
        for idx, (thr_pos, thr_name, mgrs) in enumerate(thresholds, start=1):
            px, py = projector.project(thr_pos)
            draw_aimpoint_badge(map_draw, (px, py), f"T{idx}")
            self._record(mgrs)
            aimpoint_rows.append((f"T{idx}", f"RWY {thr_name} threshold", mgrs))

        # Parking slot markers — nearest the apron, filtered to extent.
        # Labels go inline next to each box; clusters are tight enough that
        # the small offset reads as a single "ramp area" annotation and the
        # numeric labels stay tied visually to their boxes.
        slot_label_font = load_font(11, bold=True)
        for idx, slot in enumerate(
            self._select_parking_slots(airport.parking_slots, airport.position),
            start=1,
        ):
            if not extent.contains(slot.position):
                continue
            px, py = projector.project(slot.position)
            # Parking-slot markers stay red regardless of theme — pilots
            # need them to read as "enemy parking" against any basemap.
            map_draw.rectangle(
                (px - 8, py - 6, px + 8, py + 6),
                fill=(180, 20, 20),
                outline=p.fg,
                width=1,
            )
            map_draw.text(
                (px + 10, py - 8),
                f"P{idx}",
                fill=p.fg,
                font=slot_label_font,
            )

        # Paste the fully-drawn basemap (with badges/boxes/labels clipped to bounds).
        img.paste(basemap, (x0, y0))

        # Map scale bar — lower-right of the map area.
        _draw_scale_bar(draw, projector, map_right=x1, map_bottom=y1, palette=p)

        # Aimpoint table.
        table_y = y1 + 20
        draw.line((0, table_y - 4, PAGE_W, table_y - 4), fill=p.fg, width=2)
        cols = [(18, "#"), (62, "DESCRIPTION"), (320, "MGRS")]
        hdr_font = load_font(14, bold=True)
        row_font = load_font(13)
        for x, h in cols:
            draw.text((x, table_y), h, fill=p.muted, font=hdr_font)
        row_y = table_y + 22
        for r in aimpoint_rows:
            for (xc, _), v in zip(cols, r):
                draw.text((xc, row_y), v, fill=p.fg, font=row_font)
            row_y += 22

        # Footer.
        bullseye = self.game.coalition_for(self.flight.friendly).bullseye.position
        bearing, range_nm = bullseye_bearing_range_nm(bullseye, cp.position)
        # Spec example uses no spaces around `/`.
        be_str = f"{int(bearing.degrees):03d}°/{range_nm:.0f} NM"
        self._record(f"TARGET BE: {be_str}")
        draw.line(
            (0, PAGE_H - self.FOOTER_H, PAGE_W, PAGE_H - self.FOOTER_H),
            fill=p.fg,
            width=1,
        )
        draw.text(
            (20, PAGE_H - self.FOOTER_H + 6),
            f"TARGET BE {be_str}   |   {self.flight.flight_type.value}",
            fill=p.muted,
            font=load_font(13),
        )
        img.save(path)

    def _select_parking_slots(self, slots: Any, airport_pos: Any) -> List[Any]:
        """Pick the PARKING_MARKER_LIMIT slots nearest the airport center.

        Pydcs iteration order is roughly insertion order — meaningless for
        prioritising what to draw. Distance-from-center is a coarse proxy for
        "near the apron" that doesn't depend on per-airport metadata.
        """
        return sorted(slots, key=lambda s: s.position.distance_to_point(airport_pos))[
            : self.PARKING_MARKER_LIMIT
        ]

    def _compute_thresholds(self, airport: Airport) -> List[Tuple[Any, ...]]:
        """Return [(position, threshold_name, mgrs), ...] for each runway end.

        Uses OSM-derived runway endpoints when available
        (``resources/airport_imagery/<terrain>.json``); falls back to a
        fixed 900 m offset along the runway heading when no OSM data is
        shipped for the airport.
        """
        terrain = self.game.theater.terrain
        results: List[Tuple[Any, ...]] = []
        for runway in airport.runways:
            for approach in (runway.main, runway.opposite):
                heading_deg = approach.heading
                thr_pos = _osm_threshold_in_dcs(airport, heading_deg, terrain)
                if thr_pos is None:
                    thr_pos = _fallback_threshold_dcs_point(
                        airport, heading_deg, terrain
                    )
                mgrs = point_to_mgrs(thr_pos)
                results.append((thr_pos, approach.name, mgrs))
        return results


# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------

_FLIGHT_TYPES_WITH_RECON = frozenset(
    {
        FlightType.STRIKE,
        FlightType.BAI,
        FlightType.CAS,
        FlightType.SEAD,
        FlightType.DEAD,
        FlightType.OCA_AIRCRAFT,
        FlightType.OCA_RUNWAY,
        FlightType.ANTISHIP,
        FlightType.ARMED_RECON,
    }
)


def generate_recon_pages(
    *,
    flight: "FlightData",
    game: "Game",
    weather: "Weather",
    extra_threat_search_m: float,
    dark: bool = False,
) -> List[KneeboardPage]:
    # Re-arm the once-per-pass WARNING log for tile-fetch failures so a new
    # generation pass surfaces the first failure even if the previous pass
    # already tripped the suppression flag.
    _reset_tile_log_state()

    pages: List[KneeboardPage] = []

    if _should_emit_departure(flight, game):
        pages.append(
            AirfieldDeparturePage(
                flight=flight,
                game=game,
                weather=weather,
                dark=dark,
            )
        )

    if flight.flight_type not in _FLIGHT_TYPES_WITH_RECON:
        return pages
    target = getattr(flight.package, "target", None)
    if target is None:
        return pages

    pages.append(
        OverviewReconPage(
            flight=flight,
            game=game,
            extra_threat_search_m=extra_threat_search_m,
            dark=dark,
        )
    )

    if isinstance(target, ControlPoint):
        if getattr(target, "dcs_airport", None) is not None:
            pages.append(AirbaseReconPage(flight=flight, game=game, dark=dark))
    elif isinstance(target, FrontLine):
        pages.append(FrontLineDetailPage(flight=flight, game=game, dark=dark))
    elif isinstance(target, TheaterGroundObject):
        pages.append(DetailReconPage(flight=flight, game=game, dark=dark))
    # NavalGroundObject inherits from TheaterGroundObject and is handled by
    # the same branch — naval ring rendering is driven off the threat-range
    # values, not by class.

    return pages


def _should_emit_departure(flight: "FlightData", game: "Game") -> bool:
    # Spec: ground-start flights (COLD, WARM, RUNWAY) get a departure page.
    # IN_FLIGHT spawns are airborne and never see the airfield, so skip them.
    if flight.start_type == StartType.IN_FLIGHT:
        return False
    # FlightData.departure is RunwayData (no dcs_airport); resolve the pydcs
    # Airport via theater so carrier/FOB pseudo-runways correctly return None
    # and suppress the page.
    dep = getattr(flight, "departure", None)
    if dep is None:
        return False
    return _dcs_airport_for_runway(dep, game.theater) is not None
