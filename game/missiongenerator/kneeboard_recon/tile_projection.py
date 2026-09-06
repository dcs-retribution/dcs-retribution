"""Pure math for Web-Mercator tile coordinates and zoom selection.

No I/O. No DCS terrain instantiation. Stateless. The DCS-Point -> lat/lon
helper delegates to pydcs (which uses a pre-built pyproj transformer cached
on the terrain instance).
"""

from __future__ import annotations

import math
from typing import Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from dcs.mapping import Point

# Web Mercator constants. Earth equatorial circumference in metres.
_EARTH_CIRCUMFERENCE_M = 40_075_016.686
_TILE_PX = 256


def lat_lon_to_tile(lat_deg: float, lon_deg: float, z: int) -> Tuple[float, float]:
    """Convert WGS84 lat/lon (degrees) to fractional Web Mercator tile coords.

    Returns ``(x, y)`` in tile units (0..2^z). Caller floors to get integer
    tile indices, or keeps the fraction for sub-tile cropping.
    """
    n = 2.0**z
    x = (lon_deg + 180.0) / 360.0 * n
    lat_rad = math.radians(lat_deg)
    y = (1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n
    return x, y


def tile_to_lat_lon(x: float, y: float, z: int) -> Tuple[float, float]:
    """Inverse of :func:`lat_lon_to_tile`."""
    n = 2.0**z
    lon_deg = x / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1.0 - 2.0 * y / n)))
    lat_deg = math.degrees(lat_rad)
    return lat_deg, lon_deg


def dcs_to_lat_lon(point: "Point") -> Tuple[float, float]:
    """Convert a pydcs ``Point`` to WGS84 (lat, lon) in degrees.

    Thin wrapper over ``Point.latlng()`` so callers don't have to know about
    the ``LatLng`` named tuple. Accepts anything with ``.latlng()`` returning
    an object with ``.lat`` and ``.lng`` attributes (eases mocking).
    """
    latlng = point.latlng()
    return latlng.lat, latlng.lng


def auto_zoom(
    width_m: float,
    height_m: float,
    page_w: int,
    page_h: int,
    center_lat_deg: float,
    max_zoom: int = 19,
) -> int:
    """Pick the smallest zoom whose tile metres-per-pixel is no coarser than
    the page metres-per-pixel.

    Returns the minimum adequate zoom in ``[0, max_zoom]`` — the first
    level whose tile resolution is at least as fine as the page. Fetching
    one zoom finer would quadruple tile count for marginal visual gain
    since the warp downsamples to the page either way.

    Zero-area extents (collapsed corridor, degenerate single-point bbox)
    short-circuit to ``z=0`` instead of exhausting the loop and returning
    ``max_zoom`` — the caller's degenerate-quad guard rejects the result
    anyway, but at least we don't fetch a z=19 tile first.
    """
    page_mpp = max(width_m / max(page_w, 1), height_m / max(page_h, 1))
    if page_mpp == 0:
        return 0
    cos_lat = max(math.cos(math.radians(center_lat_deg)), 1e-6)
    for z in range(0, max_zoom + 1):
        tile_mpp = _EARTH_CIRCUMFERENCE_M * cos_lat / ((2**z) * _TILE_PX)
        if tile_mpp <= page_mpp:
            return z
    return max_zoom
