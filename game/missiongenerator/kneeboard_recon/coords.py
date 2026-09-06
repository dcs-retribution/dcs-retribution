"""Coordinate formatting helpers for recon kneeboard pages.

All formatters take a pydcs `Point` and return human-readable strings used in
kneeboard footers and map labels. MGRS is the primary coordinate format for
aimpoints; DMS is kept as a secondary column for crews used to it.
"""

from __future__ import annotations

import logging

import mgrs as mgrs_lib
from dcs.mapping import Point

from game.utils import Heading, meters

logger = logging.getLogger(__name__)

_MGRS = mgrs_lib.MGRS()
_MGRS_PRECISION = 5


def point_to_mgrs(point: Point) -> str:
    """Convert a DCS Point to a human-readable MGRS string.

    Output format: `<GZD> <100km square> <easting/northing>` with 5-digit
    precision (1 m resolution), e.g. `38T MM 9622813049`.

    Polar / near-polar inputs (or any mgrs-library output that doesn't
    match the expected length) return the raw unformatted string and log
    a warning rather than raising — a kneeboard with an oddly-formatted
    cell is more useful than no kneeboard at all.
    """
    ll = point.latlng()
    lat, lon = ll.lat, ll.lng
    raw = _MGRS.toMGRS(lat, lon, MGRSPrecision=_MGRS_PRECISION)
    # mgrs returns "38TMM9622813049"; insert a space after the GZD and 100km-square letters.
    expected_digits = 2 * _MGRS_PRECISION
    gzd = raw[:3]
    square = raw[3:5]
    digits = raw[5:]
    if len(digits) != expected_digits:
        logger.warning(
            "point_to_mgrs: unexpected mgrs digit length %d (expected %d) "
            "in %r at lat=%.4f lon=%.4f; returning raw value",
            len(digits),
            expected_digits,
            raw,
            lat,
            lon,
        )
        return raw
    easting = digits[:_MGRS_PRECISION]
    northing = digits[_MGRS_PRECISION:]
    return f"{gzd} {square} {easting}{northing}"


def point_to_dms(point: Point) -> str:
    """Format a DCS Point as DMS coordinates with decimal seconds.

    Matches the existing kneeboard convention (e.g. `BriefingPage`).
    """
    return point.latlng().format_dms(include_decimal_seconds=True)


def bullseye_bearing_range_nm(bullseye: Point, target: Point) -> tuple[Heading, float]:
    """Bearing (from bullseye) and slant range (nm) from bullseye to target.

    DCS world axes: x is north, y is east. Bearing is reported as a true
    heading (0-360 deg, 0 = north, 90 = east).
    """
    heading_deg = bullseye.heading_between_point(target)
    distance_m = bullseye.distance_to_point(target)
    return (
        Heading.from_degrees(int(round(heading_deg)) % 360),
        meters(distance_m).nautical_miles,
    )
