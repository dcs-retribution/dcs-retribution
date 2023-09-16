from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from datetime import timedelta
from typing import TYPE_CHECKING, Type

from game.utils import feet
from .ferry import FerryLayout
from .ibuilder import IBuilder
from .planningerror import PlanningError
from .standard import StandardFlightPlan, StandardLayout
from .waypointbuilder import WaypointBuilder

if TYPE_CHECKING:
    from ..flightwaypoint import FlightWaypoint


PRETENSE_CARGO_FLIGHT_DISTANCE = 50000


class PretenseCargoFlightPlan(StandardFlightPlan[FerryLayout]):
    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder

    @property
    def tot_waypoint(self) -> FlightWaypoint:
        return self.layout.arrival

    def tot_for_waypoint(self, waypoint: FlightWaypoint) -> timedelta | None:
        # TOT planning isn't really useful for ferries. They're behind the front
        # lines so no need to wait for escorts or for other missions to complete.
        return None

    def depart_time_for_waypoint(self, waypoint: FlightWaypoint) -> timedelta | None:
        return None

    @property
    def mission_departure_time(self) -> timedelta:
        return self.package.time_over_target


class Builder(IBuilder[PretenseCargoFlightPlan, FerryLayout]):
    def layout(self) -> FerryLayout:
        # Find the spawn location for off-map transport planes
        distance_to_flot = 0
        heading_from_flot = 0.0
        offmap_transport_cp_id = self.flight.departure.id
        for front_line_cp in self.coalition.game.theater.controlpoints:
            for front_line in self.coalition.game.theater.conflicts():
                if front_line_cp.captured == self.flight.coalition.player:
                    if (
                        front_line_cp.position.distance_to_point(front_line.position)
                        > distance_to_flot
                    ):
                        distance_to_flot = front_line_cp.position.distance_to_point(
                            front_line.position
                        )
                        heading_from_flot = front_line.position.heading_between_point(
                            front_line_cp.position
                        )
                        offmap_transport_cp_id = front_line_cp.id
        offmap_transport_cp = self.coalition.game.theater.find_control_point_by_id(
            offmap_transport_cp_id
        )
        offmap_transport_spawn = offmap_transport_cp.position.point_from_heading(
            heading_from_flot, PRETENSE_CARGO_FLIGHT_DISTANCE
        )

        altitude_is_agl = self.flight.unit_type.dcs_unit_type.helicopter
        altitude = (
            feet(1500)
            if altitude_is_agl
            else self.flight.unit_type.preferred_patrol_altitude
        )

        builder = WaypointBuilder(self.flight, self.coalition)
        ferry_layout = FerryLayout(
            departure=builder.join(offmap_transport_spawn),
            nav_to=builder.nav_path(
                offmap_transport_spawn,
                self.flight.arrival.position,
                altitude,
                altitude_is_agl,
            ),
            arrival=builder.land(self.flight.arrival),
            divert=builder.divert(self.flight.divert),
            bullseye=builder.bullseye(),
            nav_from=[],
        )
        ferry_layout.departure = builder.join(offmap_transport_spawn)
        ferry_layout.nav_to.append(builder.join(offmap_transport_spawn))
        ferry_layout.nav_from.append(builder.join(offmap_transport_spawn))
        print(ferry_layout)
        return ferry_layout

    def build(self) -> PretenseCargoFlightPlan:
        return PretenseCargoFlightPlan(self.flight, self.layout())
