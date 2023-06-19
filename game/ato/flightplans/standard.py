from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from typing import TYPE_CHECKING, TypeVar

from game.ato.flightplans.flightplan import FlightPlan, Layout

if TYPE_CHECKING:
    from ..flightwaypoint import FlightWaypoint


@dataclass
class StandardLayout(Layout, ABC):
    arrival: FlightWaypoint
    divert: FlightWaypoint | None
    bullseye: FlightWaypoint

    def delete_waypoint(self, waypoint: FlightWaypoint) -> bool:
        if waypoint is self.divert:
            self.divert = None
            return True
        return False


LayoutT = TypeVar("LayoutT", bound=StandardLayout)


class StandardFlightPlan(FlightPlan[LayoutT], ABC):
    """Base type for all non-custom flight plans.

    We can't reason about custom flight plans so they get special treatment, but all
    others are guaranteed to have certain properties like departure and arrival points,
    potentially a divert field, and a bullseye
    """
