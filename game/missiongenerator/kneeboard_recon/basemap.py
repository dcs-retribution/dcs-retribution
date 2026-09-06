# game/missiongenerator/kneeboard_recon/basemap.py
"""Basemap façade for recon kneeboard pages.

Primary path: Esri World Imagery tile compositor (``tile_compositor.render_tiles``)
matching the layer the planner UI already uses.

Fallback path (network unreachable, ToS-blocked, or terrain without a
pyproj projection): the legacy GIF-crop / tan-landmap renderer is invoked
and an OFFLINE banner is stamped across the top of the result so the user
notices the degraded quality before printing.
"""

from __future__ import annotations

import logging
import pickle
import threading
from collections import OrderedDict
from pathlib import Path
from typing import Any, Iterable, Optional, TypeVar

_VT = TypeVar("_VT")

from PIL import Image, ImageDraw, ImageFont
from dcs.terrain.terrain import Terrain

from . import airport_imagery
from ._fonts import PilFont
from .extent import MapExtent
from .tile_compositor import (
    FAILURE_TILE_CAP,
    last_failure_reason,
    render_tiles,
)

logger = logging.getLogger(__name__)

# Public, used by the legacy fallback path. The tile compositor handles
# resolution natively and does not consult this constant.
DETAIL_THRESHOLD_M: float = 5_000.0

# Legacy renderer palette (kept from the original implementation).
_LAND_TAN = (224, 213, 191)
_LAND_TAN_DARK = (188, 173, 142)
_GRID_LINE = (200, 190, 170)

# OFFLINE banner styling.
_OFFLINE_BAND_H = 24
_OFFLINE_BAND_RGB = (180, 25, 25)
_OFFLINE_TEXT_DEFAULT = "OFFLINE — basemap unavailable"
# Shown when the tile compositor refused due to MAX_TILE_COUNT — the cause
# is "area too large for the chosen zoom", which the user can actually
# address (shrink the corridor or extra-threat-search radius). The generic
# "basemap unavailable" message would imply a network problem instead.
_OFFLINE_TEXT_TILE_CAP = "OFFLINE — area too large for satellite tiles"

_RESOURCES_DIR = Path(__file__).resolve().parents[3] / "resources"
_THEATERS_DIR = _RESOURCES_DIR / "theaters"

# Bound the per-process caches so a long-running multi-theater process
# (campaign server, gen_recon_kneeboards.py looping over terrains) does
# not retain every theater GIF and landmap pickle ever loaded. Practical
# usage touches at most a handful of theaters in a single Retribution
# session, so a small bound is plenty.
_MAX_CACHED_THEATERS = 4

_gif_cache: "OrderedDict[str, Image.Image]" = OrderedDict()
_gif_cache_lock = threading.Lock()

_landmap_cache: "OrderedDict[str, tuple[Any, ...]]" = OrderedDict()
_landmap_cache_lock = threading.Lock()


def _cache_set(cache: "OrderedDict[str, _VT]", key: str, value: "_VT") -> None:
    """LRU-insert ``value`` under ``key``, evicting the oldest entry when
    the cache would exceed :data:`_MAX_CACHED_THEATERS`.

    Callers must already hold the matching cache lock.
    """
    cache[key] = value
    cache.move_to_end(key)
    while len(cache) > _MAX_CACHED_THEATERS:
        cache.popitem(last=False)


def render_basemap(
    extent: MapExtent,
    page_width: int,
    page_height: int,
    *,
    cache_dir: Path,
    imagery_anchor: Optional[Any] = None,
) -> Image.Image:
    """Render the basemap layer for a recon kneeboard page.

    Tries the Esri tile pipeline first. On failure (network unavailable,
    HTTP refusal, terrain projection error, degenerate extent), falls back
    to the legacy GIF/landmap renderer and stamps an OFFLINE banner across
    the top of the returned image.

    ``imagery_anchor`` is an optional pydcs ``Airport``. When provided and
    we have OSM-derived data for it (see
    ``resources/airport_imagery/<terrain>.json``), the satellite tile
    mosaic is shifted by the per-airport offset so it overlays where DCS
    draws its markers. Pages that center their extent on a target instead
    of an airport should leave this ``None``.

    Always returns an :class:`~PIL.Image.Image` of size
    ``(page_width, page_height)``.
    """
    offset_deg = _imagery_offset_for(extent.terrain, imagery_anchor)
    tiled = render_tiles(
        extent,
        page_width,
        page_height,
        cache_dir,
        imagery_offset_deg=offset_deg,
    )
    if tiled is not None:
        return tiled

    reason = last_failure_reason()
    logger.warning(
        "kneeboard_recon: tile basemap unavailable (reason=%r); rendering legacy fallback",
        reason,
    )
    fallback = _render_legacy_fallback(extent, page_width, page_height)
    _stamp_offline_banner(fallback, _banner_text_for_reason(reason))
    return fallback


def _banner_text_for_reason(reason: str) -> str:
    """Pick the OFFLINE banner string for a ``render_tiles`` failure reason.

    The tile-cap path is broken out because it is the only failure mode the
    user can act on — they can shrink the corridor or
    ``target_recon_extra_threat_search_nmi``. Network/projection failures
    share the generic banner; the log line carries the underlying cause.
    """
    if reason == FAILURE_TILE_CAP:
        return _OFFLINE_TEXT_TILE_CAP
    return _OFFLINE_TEXT_DEFAULT


def _imagery_offset_for(
    terrain: Terrain, airport: Optional[Any]
) -> Optional[tuple[float, float]]:
    """Look up the OSM-derived `(dlat, dlng)` offset for an airport, or None.

    Returns None when no airport was supplied, no JSON file is shipped for
    this terrain, or no entry exists for the airport's ID. The renderer
    silently proceeds without offset correction in those cases.
    """
    if airport is None:
        return None
    record = airport_imagery.load(terrain.name)
    if record is None:
        return None
    entry = record.for_airport(airport)
    if entry is None:
        return None
    return (entry.imagery_offset_lat, entry.imagery_offset_lng)


def _stamp_offline_banner(img: Image.Image, text: str = _OFFLINE_TEXT_DEFAULT) -> None:
    """Draw a red OFFLINE warning band across the top of ``img``."""
    overlay = Image.new(
        "RGBA",
        (img.width, _OFFLINE_BAND_H),
        _OFFLINE_BAND_RGB + (200,),
    )
    img.paste(overlay, (0, 0), overlay)

    font: PilFont
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 14)
    except OSError:
        font = ImageFont.load_default()
    draw = ImageDraw.Draw(img)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = (img.width - tw) // 2 - bbox[0]
    ty = (_OFFLINE_BAND_H - th) // 2 - bbox[1]
    draw.text((tx, ty), text, fill=(255, 255, 255), font=font)


# ---------------------------------------------------------------------------
# Legacy fallback renderer (preserved from the original basemap.py).
# Public ``render_basemap`` invokes this only when ``render_tiles`` returns
# ``None``. Kept in this module so the failure path requires no additional
# imports.
# ---------------------------------------------------------------------------


def _render_legacy_fallback(
    extent: MapExtent, page_width: int, page_height: int
) -> Image.Image:
    """GIF-crop for wide extents; tan+landmap+grid for tight extents."""
    # Use the larger of the two world spans: a corridor that is wide
    # east-west but short north-south (or vice versa) is still a large area
    # the GIF crop handles better than the tan grid.
    if max(extent.span_x_m, extent.span_y_m) > DETAIL_THRESHOLD_M:
        gif_render = _crop_from_gif(extent, page_width, page_height)
        if gif_render is not None:
            return gif_render
    polygons = _landmap_polygons_for_terrain(extent.terrain)
    return _draw_landmap_only(extent, page_width, page_height, polygons)


def _theater_gif_path(terrain: Terrain) -> Optional[Path]:
    """Locate the shipped gif for the given terrain.

    Existing assets are named ``resources/<terrain>.gif`` (caumap.gif,
    syria.gif, persiangulf.gif, ...) with no consistent mapping to the pydcs
    terrain name. We try a small set of name normalisations before giving up.
    """
    name = terrain.name.lower()
    candidates = [
        name,
        "caumap" if name == "caucasus" else None,
        name.replace(" ", ""),
        name.replace("the", "").strip(),
    ]
    for cand in candidates:
        if not cand:
            continue
        path = _RESOURCES_DIR / f"{cand}.gif"
        if path.exists():
            return path
    return None


def _load_gif(terrain: Terrain) -> Optional[Image.Image]:
    with _gif_cache_lock:
        cached = _gif_cache.get(terrain.name)
        if cached is not None:
            _gif_cache.move_to_end(terrain.name)
            return cached
        path = _theater_gif_path(terrain)
        if path is None:
            return None
        img = Image.open(path).convert("RGB")
        _cache_set(_gif_cache, terrain.name, img)
        return img


def _crop_from_gif(
    extent: MapExtent, page_width: int, page_height: int
) -> Optional[Image.Image]:
    gif = _load_gif(extent.terrain)
    if gif is None:
        return None
    bounds = extent.terrain.bounds
    gif_w, gif_h = gif.size
    px_per_m_x = gif_w / (bounds.right - bounds.left)
    px_per_m_y = gif_h / (bounds.top - bounds.bottom)
    gx0 = int(round((extent.min_y - bounds.left) * px_per_m_x))
    gx1 = int(round((extent.max_y - bounds.left) * px_per_m_x))
    gy0 = int(round((bounds.top - extent.max_x) * px_per_m_y))
    gy1 = int(round((bounds.top - extent.min_x) * px_per_m_y))
    gx0 = max(0, min(gif_w - 1, gx0))
    gx1 = max(gx0 + 1, min(gif_w, gx1))
    gy0 = max(0, min(gif_h - 1, gy0))
    gy1 = max(gy0 + 1, min(gif_h, gy1))
    crop = gif.crop((gx0, gy0, gx1, gy1))
    return crop.resize((page_width, page_height), Image.LANCZOS)


def _draw_landmap_only(
    extent: MapExtent,
    page_width: int,
    page_height: int,
    landmap_polygons: Iterable[Any],
) -> Image.Image:
    # Local import keeps this module's import graph minimal — Projector
    # is only needed by the legacy fallback path, which the tile
    # pipeline bypasses entirely on the happy path.
    from dcs.mapping import Point as DcsPoint
    from .projection import Projector

    img = Image.new("RGB", (page_width, page_height), _LAND_TAN)
    draw = ImageDraw.Draw(img)
    projector = Projector(
        extent=extent,
        pixel_width=page_width,
        pixel_height=page_height,
    )
    for poly in landmap_polygons:
        pts = [
            projector.project(DcsPoint(x, y, extent.terrain))
            for x, y in poly.exterior.coords
        ]
        if len(pts) >= 2:
            draw.line(pts + [pts[0]], fill=_LAND_TAN_DARK, width=2)
    for i in range(1, 8):
        gx = i * page_width // 8
        draw.line((gx, 0, gx, page_height), fill=_GRID_LINE, width=1)
        gy = i * page_height // 8
        draw.line((0, gy, page_width, gy), fill=_GRID_LINE, width=1)
    return img


def _landmap_path_for_terrain(terrain: Terrain) -> Optional[Path]:
    terrain_name_lower = terrain.name.lower()
    if not _THEATERS_DIR.exists():
        return None
    # Resolve once so a symlinked _THEATERS_DIR (test fixtures, dev
    # overlays) is still validated via real-path equality.
    theaters_root = _THEATERS_DIR.resolve()
    for theater_dir in _THEATERS_DIR.iterdir():
        if not theater_dir.is_dir():
            continue
        # Refuse to traverse into anything whose resolved path escapes
        # the theaters root — symlinked theater_dir entries pointing
        # outside resources/theaters would otherwise let pickle.load
        # deserialize an attacker-controlled file.
        try:
            theater_dir.resolve().relative_to(theaters_root)
        except ValueError:
            logger.warning(
                "kneeboard_recon: skipping theater entry %s — resolved "
                "path escapes %s",
                theater_dir,
                theaters_root,
            )
            continue
        dir_name = theater_dir.name.lower().replace(" ", "").replace("_", "")
        candidate_name = terrain_name_lower.replace(" ", "").replace("_", "")
        if dir_name == candidate_name:
            landmap_p = theater_dir / "landmap.p"
            if not landmap_p.exists():
                return None
            # Re-validate the file itself, not just its parent dir — a
            # `landmap.p` symlink pointing outside the theaters root would
            # otherwise feed an attacker-controlled file to pickle.load.
            try:
                landmap_p.resolve().relative_to(theaters_root)
            except ValueError:
                logger.warning(
                    "kneeboard_recon: skipping landmap %s — resolved "
                    "path escapes %s",
                    landmap_p,
                    theaters_root,
                )
                return None
            return landmap_p
    return None


def _landmap_polygons_for_terrain(terrain: Terrain) -> Iterable[Any]:
    with _landmap_cache_lock:
        cached = _landmap_cache.get(terrain.name)
        if cached is not None:
            _landmap_cache.move_to_end(terrain.name)
            return cached
        polygons = _load_landmap_polygons(terrain)
        _cache_set(_landmap_cache, terrain.name, polygons)
        return polygons


def _load_landmap_polygons(terrain: Terrain) -> tuple[Any, ...]:
    path = _landmap_path_for_terrain(terrain)
    if path is None:
        return ()
    try:
        with path.open("rb") as f:
            data = pickle.load(f)
    except Exception as exc:
        logger.warning(
            "kneeboard_recon: failed to load landmap %s (%s); "
            "falling back to grid-only basemap",
            path,
            exc,
        )
        return ()
    try:
        return tuple(data.inclusion_zones.geoms)
    except AttributeError:
        logger.warning(
            "kneeboard_recon: landmap at %s has no inclusion_zones.geoms; "
            "falling back to grid-only basemap",
            path,
        )
        return ()
