"""Compose Esri tiles into a basemap image at a given DCS-world extent.

Pipeline:

1. Project all four DCS-axis-aligned corners of the extent to WGS84 lat/lon
   via the terrain's pre-built pyproj transformer (pydcs ``Point.latlng()``).
   DCS theaters use Transverse Mercator centered on the theater; a
   DCS-axis-aligned square is a *rotated quadrilateral* in lat/lon space,
   so all four corners must be considered — using only the SW/NE diagonal
   undersizes the bbox and offsets the basemap from the markers.
2. Auto-select a zoom level whose tile metres-per-pixel is no coarser than
   the page metres-per-pixel.
3. Enumerate the integer (x, y) tile range covering the *four-corner*
   lat/lon bounding box, fetch each tile (cache-hit or network).
4. Composite tiles into a single canvas at native tile resolution
   (Mercator-axis-aligned).
5. Warp the canvas onto a ``(page_width, page_height)`` rectangle using
   ``Image.transform(QUAD, ...)`` with the four DCS corners' canvas-pixel
   positions as the source quadrilateral. This produces a DCS-axis-aligned
   output that exactly matches the marker ``Projector`` used elsewhere in
   the recon module.
6. Desaturate (0.6) and dim (0.85) so map overlays drawn on top stay
   visually dominant on a printed kneeboard.
7. Stamp the required Esri attribution in the bottom-right corner.

Any failure (lat/lon projection raises, a required tile fetch returns
``None``) returns ``None`` so the caller can fall back to a different
basemap.
"""

from __future__ import annotations

import logging
import math
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Optional, Union

from PIL import Image, ImageDraw, ImageEnhance
from dcs.mapping import LatLng, Point

from ._fonts import load_font
from .extent import MapExtent
from .tile_projection import auto_zoom, lat_lon_to_tile
from .tile_source import fetch_tile

logger = logging.getLogger(__name__)


# Failure-reason codes published via ``last_failure_reason`` so the basemap
# façade can pick a banner appropriate to the actual cause without forcing
# ``render_tiles`` to return a discriminated union. ``""`` = success.
FAILURE_NONE = ""
FAILURE_PROJECTION = "projection"
FAILURE_TILE_CAP = "tile_cap"
FAILURE_TILE_FETCH = "tile_fetch"
FAILURE_DEGENERATE = "degenerate"

# Thread-local so concurrent recon-page renders in different threads don't
# clobber each other's reason.
_state = threading.local()


def last_failure_reason() -> str:
    """Reason for the most recent ``render_tiles`` fallback, or ``""``.

    Reset at the start of every ``render_tiles`` call. Read by
    ``basemap.render_basemap`` so the OFFLINE banner can call out the
    specific failure mode (e.g. ``tile_cap`` lets the banner say "area too
    large for tiles" instead of the generic "basemap unavailable").
    """
    return getattr(_state, "reason", FAILURE_NONE)


def _set_failure(reason: str) -> None:
    _state.reason = reason


TILE_SIZE = 256
SATURATION_FACTOR = 0.6
BRIGHTNESS_FACTOR = 0.85
# Esri free-tier (World_Imagery) attribution. Their TOS requires naming
# the source providers; the short "© Esri" was insufficient.
ATTRIBUTION_TEXT = (
    "Imagery © Esri, Maxar, Earthstar Geographics, " "and the GIS User Community"
)

# Pathological extents (e.g. an overview corridor plus a wide
# `target_recon_extra_threat_search_nmi`) can balloon the tile range. A
# canvas of ~16-megapixel tiles is roughly the headroom Pillow handles
# comfortably; beyond that we'd rather degrade to the legacy basemap than
# allocate gigabytes for a single page.
MAX_TILE_COUNT = 400


class _ShiftedLatLng:
    """Lightweight lat/lng holder used when an imagery offset is applied.

    Defined at module scope (not nested inside ``render_tiles``) so each call
    doesn't redefine the class — the previous nested form re-created a fresh
    class object per render, defeating CPython attribute-access caching.
    """

    __slots__ = ("lat", "lng")

    def __init__(self, lat: float, lng: float) -> None:
        self.lat = lat
        self.lng = lng


def render_tiles(
    extent: MapExtent,
    page_width: int,
    page_height: int,
    cache_dir: Path,
    imagery_offset_deg: Optional[tuple[float, float]] = None,
) -> Optional[Image.Image]:
    """Render Esri World Imagery tiles into a page-sized basemap image.

    ``imagery_offset_deg`` is an optional ``(dlat, dlng)`` translation
    applied to each DCS corner's lat/lng *before* tile lookup. DCS terrain
    placements often differ from real-world placements by hundreds of
    metres; passing the OSM-derived offset shifts the satellite imagery so
    that pixel positions of DCS-projected markers overlay the real-world
    runway/apron features.

    Returns ``None`` on any failure; caller falls back. Inspect
    :func:`last_failure_reason` for the cause when ``None`` is returned.
    """
    _set_failure(FAILURE_NONE)

    # All four DCS-axis-aligned corners. DCS convention: x = north,
    # y = east. So:
    #   NW = (max_x, min_y)  — top-left of page (north + west)
    #   NE = (max_x, max_y)  — top-right of page (north + east)
    #   SW = (min_x, min_y)  — bottom-left of page (south + west)
    #   SE = (min_x, max_y)  — bottom-right of page (south + east)
    nw_ll: Union[LatLng, _ShiftedLatLng]
    ne_ll: Union[LatLng, _ShiftedLatLng]
    sw_ll: Union[LatLng, _ShiftedLatLng]
    se_ll: Union[LatLng, _ShiftedLatLng]
    try:
        nw_ll = Point(extent.max_x, extent.min_y, extent.terrain).latlng()
        ne_ll = Point(extent.max_x, extent.max_y, extent.terrain).latlng()
        sw_ll = Point(extent.min_x, extent.min_y, extent.terrain).latlng()
        se_ll = Point(extent.min_x, extent.max_y, extent.terrain).latlng()
    except Exception as exc:
        logger.warning(
            "kneeboard_recon: lat/lon projection failed for extent (%s); falling back",
            exc,
        )
        _set_failure(FAILURE_PROJECTION)
        return None

    if imagery_offset_deg is not None:
        dlat, dlng = imagery_offset_deg
        nw_ll = _ShiftedLatLng(nw_ll.lat + dlat, nw_ll.lng + dlng)
        ne_ll = _ShiftedLatLng(ne_ll.lat + dlat, ne_ll.lng + dlng)
        sw_ll = _ShiftedLatLng(sw_ll.lat + dlat, sw_ll.lng + dlng)
        se_ll = _ShiftedLatLng(se_ll.lat + dlat, se_ll.lng + dlng)

    all_lats = (nw_ll.lat, ne_ll.lat, sw_ll.lat, se_ll.lat)
    all_lngs = (nw_ll.lng, ne_ll.lng, sw_ll.lng, se_ll.lng)
    lat_min, lat_max = min(all_lats), max(all_lats)
    lng_min, lng_max = min(all_lngs), max(all_lngs)
    center_lat = (lat_min + lat_max) / 2

    # auto_zoom takes page-axis-aligned spans; MapExtent stores them in
    # DCS-axis terms. DCS-y (east-west) maps to page horizontal; DCS-x
    # (north-south) to page vertical.
    z = auto_zoom(
        width_m=extent.span_y_m,
        height_m=extent.span_x_m,
        page_w=page_width,
        page_h=page_height,
        center_lat_deg=center_lat,
    )

    # Tile range covering the four-corner lat/lon bbox. Web Mercator y
    # decreases as latitude increases (north = small y).
    fx_at_min_lng, fy_at_max_lat = lat_lon_to_tile(lat_max, lng_min, z)
    fx_at_max_lng, fy_at_min_lat = lat_lon_to_tile(lat_min, lng_max, z)
    fx0, fx1 = sorted([fx_at_min_lng, fx_at_max_lng])
    fy0, fy1 = sorted([fy_at_max_lat, fy_at_min_lat])

    tx0, tx1 = math.floor(fx0), math.floor(fx1)
    ty0, ty1 = math.floor(fy0), math.floor(fy1)

    tile_count = (tx1 - tx0 + 1) * (ty1 - ty0 + 1)
    if tile_count > MAX_TILE_COUNT:
        logger.warning(
            "kneeboard_recon: tile-count %d exceeds cap %d at z=%d "
            "for extent %.0f x %.0f m; falling back to legacy basemap",
            tile_count,
            MAX_TILE_COUNT,
            z,
            extent.span_x_m,
            extent.span_y_m,
        )
        _set_failure(FAILURE_TILE_CAP)
        return None

    canvas_w = (tx1 - tx0 + 1) * TILE_SIZE
    canvas_h = (ty1 - ty0 + 1) * TILE_SIZE
    canvas = Image.new("RGB", (canvas_w, canvas_h), (0, 0, 0))

    # Concurrent tile fetch. stdlib ``urlopen`` opens one TCP connection per
    # tile with no keep-alive, so a serial fetch of 20-30 tiles costs seconds
    # of round-trip time on a fresh cache. ``ThreadPoolExecutor`` parallelises
    # the I/O while keeping the surrounding compositor logic sequential.
    # ``fetch_tile`` is thread-safe by design: log-suppression state is
    # thread-local and the on-disk cache write uses a per-fetch unique
    # tempfile + ``os.replace`` so concurrent fetches of the same tile do
    # not clobber each other. The worker cap stays low to be a polite
    # citizen toward the Esri free service.
    tile_coords = [(tx, ty) for tx in range(tx0, tx1 + 1) for ty in range(ty0, ty1 + 1)]
    workers = max(1, min(6, len(tile_coords)))
    # ``fetch_tile`` is contracted to return ``None`` on every known failure,
    # but ``ThreadPoolExecutor`` re-raises anything it does not catch when the
    # results are realised by ``list(...)``. Belt-and-suspenders: any
    # unforeseen escapee (e.g. a network/protocol error not yet handled in
    # ``tile_source``) must degrade to the offline basemap rather than abort
    # mission generation at Take Off.
    try:
        with ThreadPoolExecutor(max_workers=workers) as exe:
            results = list(
                exe.map(
                    lambda c: (c, fetch_tile(z, c[0], c[1], cache_dir)),
                    tile_coords,
                )
            )
    except Exception as exc:
        logger.warning(
            "kneeboard_recon: tile fetch failed unexpectedly (%s); "
            "falling back to offline basemap",
            exc,
        )
        _set_failure(FAILURE_TILE_FETCH)
        return None

    for (tx, ty), tile in results:
        if tile is None:
            _set_failure(FAILURE_TILE_FETCH)
            return None
        canvas.paste(tile, ((tx - tx0) * TILE_SIZE, (ty - ty0) * TILE_SIZE))

    # Canvas-pixel positions of each DCS corner. The Image.QUAD warp will
    # map this quadrilateral onto the (page_w, page_h) rectangle.
    def _canvas_xy(latlng: Union[LatLng, _ShiftedLatLng]) -> tuple[float, float]:
        fx, fy = lat_lon_to_tile(latlng.lat, latlng.lng, z)
        return ((fx - tx0) * TILE_SIZE, (fy - ty0) * TILE_SIZE)

    ul = _canvas_xy(nw_ll)  # source upper-left  -> page (0, 0)
    ll = _canvas_xy(sw_ll)  # source lower-left  -> page (0, page_h)
    lr = _canvas_xy(se_ll)  # source lower-right -> page (page_w, page_h)
    ur = _canvas_xy(ne_ll)  # source upper-right -> page (page_w, 0)
    source_quad = (ul[0], ul[1], ll[0], ll[1], lr[0], lr[1], ur[0], ur[1])

    # Guard against degenerate extents collapsing the quad.
    if not _quad_has_area(source_quad):
        _set_failure(FAILURE_DEGENERATE)
        return None

    warped = canvas.transform(
        (page_width, page_height),
        Image.QUAD,
        source_quad,
        Image.BICUBIC,
    )

    warped = ImageEnhance.Color(warped).enhance(SATURATION_FACTOR)
    warped = ImageEnhance.Brightness(warped).enhance(BRIGHTNESS_FACTOR)

    return _stamp_attribution(warped)


def _quad_has_area(quad: tuple[float, ...]) -> bool:
    """True if the source quadrilateral has nonzero area."""
    xs = quad[0::2]
    ys = quad[1::2]
    return (max(xs) - min(xs)) > 0.5 and (max(ys) - min(ys)) > 0.5


def _stamp_attribution(img: Image.Image) -> Image.Image:
    """Draw the Esri attribution pill in the bottom-right corner.

    Mutates ``img`` in place AND returns it, so callers can chain
    ``warped = _stamp_attribution(warped)`` without losing track of
    whether the pill has already been baked in.

    Font size 12 (via the shared ``_fonts.load_font`` so the
    cross-platform fallback chain still applies). On a 768×1024 page
    printed at typical kneeboard size this renders as ~5pt — small but
    legible, which Esri ToS requires. The previous 10px ``DejaVuSans``
    direct load fell to PIL's 8px bitmap default on Windows systems
    that don't ship DejaVuSans, producing illegible (~4pt) attribution
    and a quiet ToS-compliance gap.
    """
    font = load_font(12, bold=True)

    draw = ImageDraw.Draw(img, "RGBA")
    bbox = draw.textbbox((0, 0), ATTRIBUTION_TEXT, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    pad = 5
    margin = 4
    box_w = tw + pad * 2
    box_h = th + pad * 2
    x = img.width - box_w - margin
    y = img.height - box_h - margin
    draw.rectangle((x, y, x + box_w, y + box_h), fill=(0, 0, 0, 160))
    draw.text(
        (x + pad - bbox[0], y + pad - bbox[1]),
        ATTRIBUTION_TEXT,
        fill=(255, 255, 255, 255),
        font=font,
    )
    return img
