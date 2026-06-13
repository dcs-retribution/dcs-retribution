from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dcs import Point

    from game.coalition import Coalition
    from game.utils import Distance, Heading
    from ..flight import Flight
    from ..flighttype import FlightType


def deconflicted_racetrack_center(
    base_center: Point,
    orbit_heading: Heading,
    spacing: Distance,
    flight: Flight,
    coalition: Coalition,
    flight_type: FlightType,
) -> Point:
    """Offset a patrol's racetrack center laterally so multiple same-type patrols
    (AWACS, tankers) spread out along the front instead of stacking on one orbit.

    All flights of ``flight_type`` planned for ``coalition`` are ordered
    deterministically and assigned evenly spaced offsets centered on
    ``base_center``. With a single such flight the offset is zero, preserving the
    original placement.
    """
    same_type = sorted(
        (
            f
            for package in coalition.ato.packages
            for f in package.flights
            if f.flight_type is flight_type
        ),
        key=lambda f: str(f.id),
    )
    count = len(same_type)
    try:
        index = next(i for i, f in enumerate(same_type) if f is flight)
    except StopIteration:
        index = 0

    lateral = (index - (count - 1) / 2) * spacing.meters
    if lateral >= 0:
        return base_center.point_from_heading(orbit_heading.right.degrees, lateral)
    return base_center.point_from_heading(orbit_heading.left.degrees, -lateral)
