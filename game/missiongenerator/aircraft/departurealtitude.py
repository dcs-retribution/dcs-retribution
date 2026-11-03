"""Mission-local altitude slots for fixed-wing departure air starts."""

from __future__ import annotations

from typing import MutableMapping, Optional
from uuid import UUID

from game.utils import Distance


def reserve_departure_altitude(
    stack: MutableMapping[UUID, Distance],
    control_point_id: UUID,
    requested_altitude: Optional[Distance],
    minimum_altitude: Distance,
    separation: Distance,
) -> Distance:
    """Reserve a RADIO departure slot, honoring any higher requested altitude."""
    altitude = max(
        stack.get(control_point_id, minimum_altitude),
        requested_altitude if requested_altitude is not None else minimum_altitude,
        minimum_altitude,
    )
    stack[control_point_id] = altitude + separation
    return altitude
