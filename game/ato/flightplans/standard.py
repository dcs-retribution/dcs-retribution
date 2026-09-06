from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, TypeVar, Optional

from game.ato.flightplans.flightplan import FlightPlan, Layout
from .waypointbuilder import WaypointBuilder
from ..flightwaypointtype import FlightWaypointType

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
        new_wpt = WaypointBuilder.nav_midpoint(wpt, next_wpt)
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
        elif waypoint in self.custom_waypoints:
            self.custom_waypoints.remove(waypoint)
            return True
        return False

    def move_waypoint(self, waypoint: FlightWaypoint, direction: int) -> bool:
        for sequence in (self.nav_to, self.nav_from, self.custom_waypoints):
            if waypoint in sequence:
                index = sequence.index(waypoint)
                target = index + direction
                if 0 <= target < len(sequence):
                    sequence[index], sequence[target] = (
                        sequence[target],
                        sequence[index],
                    )
                    return True
                # At the edge of its list: moving further would cross a structural
                # boundary, which this layout cannot do. The UI offers degrade-to-custom.
                return False
        return False


LayoutT = TypeVar("LayoutT", bound=StandardLayout)


class StandardFlightPlan(FlightPlan[LayoutT], ABC):
    """Base type for all non-custom flight plans.

    We can't reason about custom flight plans so they get special treatment, but all
    others are guaranteed to have certain properties like departure and arrival points,
    potentially a divert field, and a bullseye
    """

    @property
    def landing_time(self) -> datetime:
        return_time = self.total_time_between_waypoints(
            self.tot_waypoint, self.layout.arrival
        )
        return self.mission_departure_time + return_time
