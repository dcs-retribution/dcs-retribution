from __future__ import annotations

from abc import ABC
from copy import deepcopy
from dataclasses import dataclass
from typing import TYPE_CHECKING, TypeVar, Optional

from game.ato.flightplans.flightplan import FlightPlan, Layout
from .waypointbuilder import WaypointBuilder
from ..flightwaypointtype import FlightWaypointType
from ...utils import feet

if TYPE_CHECKING:
    from ..flightwaypoint import FlightWaypoint


@dataclass
class StandardLayout(Layout, ABC):
    arrival: FlightWaypoint
    divert: FlightWaypoint | None
    bullseye: FlightWaypoint
    nav_to: list[FlightWaypoint]
    nav_from: list[FlightWaypoint]

    def add_waypoint(
        self, wpt: FlightWaypoint, next_wpt: Optional[FlightWaypoint]
    ) -> bool:
        new_wpt = self.get_midpoint(wpt, next_wpt)
        if wpt.waypoint_type in [FlightWaypointType.TAKEOFF, FlightWaypointType.LOITER]:
            self.nav_to.insert(0, new_wpt)
            return True
        elif wpt.waypoint_type in [
            FlightWaypointType.SPLIT,
            FlightWaypointType.REFUEL,
            FlightWaypointType.PATROL,
            FlightWaypointType.EGRESS,
        ]:
            self.nav_from.insert(0, new_wpt)
            return True
        elif wpt.waypoint_type is FlightWaypointType.NAV:
            if wpt in self.nav_to:
                index = self.nav_to.index(wpt) + 1
                self.nav_to.insert(index, new_wpt)
                return True
            elif wpt in self.nav_from:
                index = self.nav_from.index(wpt) + 1
                self.nav_from.insert(index, new_wpt)
                return True
        return False

    @staticmethod
    def get_midpoint(
        wpt: FlightWaypoint, next_wpt: Optional[FlightWaypoint]
    ) -> FlightWaypoint:
        new_pos = deepcopy(wpt.position)
        next_alt = feet(20000)
        if next_wpt:
            new_pos = wpt.position.lerp(next_wpt.position, 0.5)
            next_alt = next_wpt.alt
        new_wpt = WaypointBuilder.nav(new_pos, max(wpt.alt, next_alt))
        return new_wpt

    def delete_waypoint(self, waypoint: FlightWaypoint) -> bool:
        if waypoint is self.divert:
            self.divert = None
            return True
        elif waypoint in self.nav_to:
            self.nav_to.remove(waypoint)
            return True
        elif waypoint in self.nav_from:
            self.nav_from.remove(waypoint)
            return True
        return False


LayoutT = TypeVar("LayoutT", bound=StandardLayout)


class StandardFlightPlan(FlightPlan[LayoutT], ABC):
    """Base type for all non-custom flight plans.

    We can't reason about custom flight plans so they get special treatment, but all
    others are guaranteed to have certain properties like departure and arrival points,
    potentially a divert field, and a bullseye
    """
