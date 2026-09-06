# game/missiongenerator/kneeboard_recon/extent.py
"""Rectangular DCS-world bounding boxes used to drive a single kneeboard page."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from dcs.mapping import Point
from dcs.terrain.terrain import Terrain


@dataclass(frozen=True)
class MapExtent:
    """A rectangular DCS-world bounding box (in meters) for a single page."""

    min_x: float
    max_x: float
    min_y: float
    max_y: float
    terrain: Terrain

    # DCS world axes: x = northing, y = easting. Properties name the
    # axis explicitly so callers don't have to remember that the page-x
    # (horizontal) direction is sourced from DCS-y. See projection.py
    # and tile_compositor.py for the page-axis swap.
    @property
    def span_x_m(self) -> float:
        """North-south span (DCS x axis), in metres."""
        return self.max_x - self.min_x

    @property
    def span_y_m(self) -> float:
        """East-west span (DCS y axis), in metres."""
        return self.max_y - self.min_y

    def expand(self, margin_m: float) -> "MapExtent":
        return MapExtent(
            min_x=self.min_x - margin_m,
            max_x=self.max_x + margin_m,
            min_y=self.min_y - margin_m,
            max_y=self.max_y + margin_m,
            terrain=self.terrain,
        )

    def contains(self, point: Point) -> bool:
        return (
            self.min_x <= point.x <= self.max_x and self.min_y <= point.y <= self.max_y
        )


def square_extent(
    center: Point,
    half_side_m: float,
    pixel_width: int,
    pixel_height: int,
    terrain: Terrain,
) -> MapExtent:
    """Build a centered extent whose world aspect matches the pixel aspect.

    Locks the smaller-pixel axis to ``2 * half_side_m`` world meters and
    grows the other axis proportionally so projected circles stay circular
    (no oval threat rings on a non-square map_box). Use this in place of a
    hand-built square ``MapExtent`` for any page whose ``map_box`` is not
    perfectly square.

    Page axis -> DCS axis mapping (see projection.py):
        pixel_width  -> span_y_m (DCS east)
        pixel_height -> span_x_m (DCS north)
    """
    pw = max(int(pixel_width), 1)
    ph = max(int(pixel_height), 1)
    if pw >= ph:
        span_x = 2.0 * half_side_m
        span_y = span_x * (pw / ph)
    else:
        span_y = 2.0 * half_side_m
        span_x = span_y * (ph / pw)
    return MapExtent(
        min_x=center.x - span_x / 2.0,
        max_x=center.x + span_x / 2.0,
        min_y=center.y - span_y / 2.0,
        max_y=center.y + span_y / 2.0,
        terrain=terrain,
    )


# A single-waypoint corridor falls back to a 5 km square so the page is non-empty.
_DEGENERATE_HALF_SIDE_M = 2_500.0
# 10 % margin around the bounding box of all waypoints + threats.
_DEFAULT_MARGIN_FRAC = 0.10
# Smallest extent we will ever emit (avoids divide-by-zero in the projector for
# tightly-spaced waypoints or near-overlapping threats).
_MIN_HALF_SIDE_M = 500.0


def aspect_correct(extent: MapExtent, pixel_width: int, pixel_height: int) -> MapExtent:
    """Pad ``extent`` symmetrically so its world aspect matches the pixel aspect.

    The tile compositor warps the extent corners onto the page rectangle
    via :func:`PIL.Image.transform` with mode ``QUAD``. When the world
    aspect ratio doesn't match the pixel aspect ratio that warp produces
    a non-uniform stretch, which on the overview page reads as a strong
    horizontal squish for typical wide-and-short strike corridors. This
    helper expands the smaller-axis half-side of ``extent`` so the warp
    becomes uniform scaling.

    The original extent's center is preserved.
    """
    pw = max(int(pixel_width), 1)
    ph = max(int(pixel_height), 1)
    span_x = max(extent.span_x_m, 1.0)  # vertical (DCS north)
    span_y = max(extent.span_y_m, 1.0)  # horizontal (DCS east)
    target_ratio = pw / ph
    current_ratio = span_y / span_x
    if current_ratio < target_ratio:
        # World is narrower than the pixel aspect — pad horizontally.
        pad = (span_x * target_ratio - span_y) / 2.0
        return MapExtent(
            min_x=extent.min_x,
            max_x=extent.max_x,
            min_y=extent.min_y - pad,
            max_y=extent.max_y + pad,
            terrain=extent.terrain,
        )
    if current_ratio > target_ratio:
        # World is wider than the pixel aspect — pad vertically.
        pad = (span_y / target_ratio - span_x) / 2.0
        return MapExtent(
            min_x=extent.min_x - pad,
            max_x=extent.max_x + pad,
            min_y=extent.min_y,
            max_y=extent.max_y,
            terrain=extent.terrain,
        )
    return extent


def corridor_extent(
    waypoints: Iterable[Point],
    threats: Iterable[Point],
    extra_radius_m: float,
    terrain: Terrain,
) -> MapExtent:
    """Compute an overview extent enclosing the package corridor + nearby threats.

    Args:
        waypoints: Package-corridor waypoints, typically IP, target, egress.
        threats: Enemy ground/sea positions to include if inside the bbox.
        extra_radius_m: Per-side margin (nm * 1852, converted upstream) added
            to the bounding box to widen the threat-search area.
        terrain: Terrain attached to the returned MapExtent.
    """
    wp_list = list(waypoints)
    threat_list = list(threats)
    if not wp_list:
        raise ValueError("corridor_extent requires at least one waypoint")

    # Bounding box of waypoints + threats.
    xs = [p.x for p in wp_list]
    ys = [p.y for p in wp_list]
    bbox_min_x, bbox_max_x = min(xs), max(xs)
    bbox_min_y, bbox_max_y = min(ys), max(ys)
    for t in threat_list:
        bbox_min_x = min(bbox_min_x, t.x)
        bbox_max_x = max(bbox_max_x, t.x)
        bbox_min_y = min(bbox_min_y, t.y)
        bbox_max_y = max(bbox_max_y, t.y)

    # Degenerate-span floor: when waypoints + threats collapse to a
    # point (single-waypoint corridor, or every input at the same
    # coord), pad symmetrically to a 5 km square so downstream
    # extent.span_x_m / span_y_m never round to zero. Applied
    # independently per axis so a collinear corridor still gets a real
    # span on the non-zero axis.
    center_x = (bbox_min_x + bbox_max_x) / 2
    center_y = (bbox_min_y + bbox_max_y) / 2
    if bbox_max_x - bbox_min_x < 2 * _DEGENERATE_HALF_SIDE_M:
        bbox_min_x = center_x - _DEGENERATE_HALF_SIDE_M
        bbox_max_x = center_x + _DEGENERATE_HALF_SIDE_M
    if bbox_max_y - bbox_min_y < 2 * _DEGENERATE_HALF_SIDE_M:
        bbox_min_y = center_y - _DEGENERATE_HALF_SIDE_M
        bbox_max_y = center_y + _DEGENERATE_HALF_SIDE_M

    extent = MapExtent(
        min_x=bbox_min_x,
        max_x=bbox_max_x,
        min_y=bbox_min_y,
        max_y=bbox_max_y,
        terrain=terrain,
    )

    # Extra threat search radius.
    if extra_radius_m > 0.0:
        extent = extent.expand(extra_radius_m)

    # Default 10 % margin, with a floor.
    span = max(extent.span_x_m, extent.span_y_m)
    margin = max(span * _DEFAULT_MARGIN_FRAC, _MIN_HALF_SIDE_M)
    return extent.expand(margin)
