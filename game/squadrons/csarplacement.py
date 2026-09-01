from __future__ import annotations

import logging
from typing import Optional, TYPE_CHECKING

from dcs.mapping import Point

if TYPE_CHECKING:
    from game.theater import ConflictTheater

#: Keep downed pilots at least this far from any mapped structure/control point so
#: they don't land on top of a building where a helicopter cannot set down.
_MIN_CLEARANCE_METERS = 300.0

#: If snapping to land moves a position further than this, treat the snap as
#: implausible (island maps can teleport hundreds of NM) and give up on the point.
#:
#: Only reachable for points that are neither land nor sea -- an exclusion zone --
#: since an open-water ditching is left where it is.
_MAX_SNAP_METERS = 8000.0


def find_downed_pilot_position(
    theater: ConflictTheater, near: Point
) -> Optional[Point]:
    """Finds a valid position for a downed pilot near ``near``.

    A pilot who came down at sea stays where they ditched: the rescue is a hoist,
    so there is nothing to be gained by putting them ashore, and a helicopter can
    reach anywhere on the map so no distance makes them unreachable. Everyone else
    gets a point on land (not an exclusion zone) and clear of mapped structures,
    or ``None`` if no suitable spot could be found nearby (in which case the caller
    should treat the pilot as killed).

    Retribution has no building/foliage data, so the definitive "can a helicopter
    actually land here" check is done in Lua at spawn time. This only rules out the
    obviously-unlandable cases we *can* see: water and known structures.
    """
    if theater.is_in_sea(near):
        # See DownedPilot.in_water: this is what forces a hover extraction for
        # them later, whatever the csar_hover_extraction setting says.
        return near

    candidate = _snap_to_land(theater, near)
    if candidate is None:
        return None

    if _is_landable(theater, candidate):
        return candidate

    # Spiral outward looking for a clear spot.
    for radius in (150.0, 300.0, 500.0, 800.0, 1200.0):
        for step in range(8):
            heading = step * 45.0
            probe = candidate.point_from_heading(heading, radius)
            snapped = _snap_to_land(theater, probe)
            if snapped is not None and _is_landable(theater, snapped):
                return snapped

    logging.info(
        "Could not find a landable CSAR position near %s; pilot will be killed.",
        near,
    )
    return None


def _snap_to_land(theater: ConflictTheater, point: Point) -> Optional[Point]:
    if not theater.landmap:
        return point
    if theater.is_on_land(point):
        return point
    snapped = theater.nearest_land_pos(point)
    if snapped.distance_to_point(point) > _MAX_SNAP_METERS:
        return None
    return snapped


def _is_landable(theater: ConflictTheater, point: Point) -> bool:
    if theater.landmap and not theater.is_on_land(point):
        return False
    for cp in theater.controlpoints:
        if cp.position.distance_to_point(point) < _MIN_CLEARANCE_METERS:
            return False
    for tgo in theater.ground_objects:
        if tgo.position.distance_to_point(point) < _MIN_CLEARANCE_METERS:
            return False
    return True
