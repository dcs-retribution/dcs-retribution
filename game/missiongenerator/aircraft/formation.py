"""Heading-relative spacing for preplaced airborne aircraft groups."""

from __future__ import annotations

import math
from typing import Any

from dcs.unitgroup import FlyingGroup

MINIMUM_AIRCRAFT_SPACING_METERS = 50.0


def is_airborne_start(group: FlyingGroup[Any]) -> bool:
    """Return whether the group's initial point is an airborne start."""
    return bool(group.points) and not group.points[0].type.startswith("TakeOff")


def space_airborne_group(group: FlyingGroup[Any]) -> None:
    """Space aircraft laterally from their leader without changing the route.

    The first distinct route leg defines the common heading. A stable northbound
    heading is used when the route has no usable direction. Pydcs derives unit
    headings from the route while serializing, so mark the group for manual
    heading serialization and set every unit explicitly.
    """
    if len(group.units) < 2:
        return

    leader = group.units[0]
    heading = _initial_heading(group)
    lateral_heading = heading + 90.0
    for index, unit in enumerate(group.units[1:], start=1):
        unit.position = leader.position.point_from_heading(
            lateral_heading, index * MINIMUM_AIRCRAFT_SPACING_METERS
        )
    for unit in group.units:
        unit.heading = heading
    # Group.dict() honors this serializer attribute for aircraft headings.
    setattr(group, "manualHeading", True)


def _initial_heading(group: FlyingGroup[Any]) -> float:
    if not group.points:
        return 0.0
    origin = group.points[0].position
    for point in group.points[1:]:
        destination = point.position
        if origin.distance_to_point(destination) > 0:
            return origin.heading_between_point(destination)
    return 0.0
