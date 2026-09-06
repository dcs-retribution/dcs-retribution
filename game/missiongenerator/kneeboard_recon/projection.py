# game/missiongenerator/kneeboard_recon/projection.py
"""Project DCS-world Points into page pixel coordinates for a given extent."""

from __future__ import annotations

from dataclasses import dataclass

from dcs.mapping import Point

from .extent import MapExtent


@dataclass(frozen=True)
class Projector:
    """Maps a `MapExtent` to a fixed-size pixel viewport.

    DCS world axes: x is north (positive = up on the map), y is east (positive
    = right). Page pixels: (0, 0) is top-left, x grows right, y grows down.
    """

    extent: MapExtent
    pixel_width: int
    pixel_height: int

    def project(self, point: Point) -> tuple[int, int]:
        """Return (page_x, page_y) for a DCS Point, both in image pixel space."""
        # Horizontal: DCS y (east) -> page x.
        frac_x = (point.y - self.extent.min_y) / max(self.extent.span_y_m, 1.0)
        # Vertical: DCS x (north) -> page y, inverted because image y
        # grows downward but DCS x grows northward.
        frac_y = (point.x - self.extent.min_x) / max(self.extent.span_x_m, 1.0)
        px = int(round(frac_x * (self.pixel_width - 1)))
        py = int(round((1.0 - frac_y) * (self.pixel_height - 1)))
        return px, py

    def meters_to_px(self, distance_m: float) -> int:
        """Convert a distance in meters to page pixels.

        Uses the smaller m/px of the two image axes so that rings drawn
        in pixel space stay circular under non-square extents. DCS-x
        span maps to the vertical page axis; DCS-y span to the
        horizontal.
        """
        m_per_px_vertical = self.extent.span_x_m / max(self.pixel_height, 1)
        m_per_px_horizontal = self.extent.span_y_m / max(self.pixel_width, 1)
        m_per_px = min(m_per_px_vertical, m_per_px_horizontal)
        return int(round(distance_m / max(m_per_px, 1.0)))
