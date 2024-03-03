from __future__ import annotations

from datetime import timedelta
from typing import Type

from game.utils import Heading, meters, nautical_miles
from .ibuilder import IBuilder
from .patrolling import PatrollingLayout
from .refuelingflightplan import RefuelingFlightPlan
from .waypointbuilder import WaypointBuilder


class TheaterRefuelingFlightPlan(RefuelingFlightPlan):
    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder

    @property
    def patrol_duration(self) -> timedelta:
        return self.flight.coalition.game.settings.desired_tanker_on_station_time


class Builder(IBuilder[TheaterRefuelingFlightPlan, PatrollingLayout]):
    def layout(self) -> PatrollingLayout:
        racetrack_half_distance = nautical_miles(20).meters

        location = self.package.target

        closest_boundary = self.threat_zones.closest_boundary(location.position)
        heading_to_threat_boundary = Heading.from_degrees(
            location.position.heading_between_point(closest_boundary)
        )
        distance_to_threat = meters(
            location.position.distance_to_point(closest_boundary)
        )
        orbit_heading = heading_to_threat_boundary

        # Station 70nm outside the threat zone.
        threat_buffer = nautical_miles(
            self.coalition.game.settings.tanker_threat_buffer_min_distance
        )
        if self.threat_zones.threatened(location.position):
            orbit_distance = distance_to_threat + threat_buffer
        else:
            orbit_distance = distance_to_threat - threat_buffer

        racetrack_center = location.position.point_from_heading(
            orbit_heading.degrees, orbit_distance.meters
        )

        racetrack_start = racetrack_center.point_from_heading(
            orbit_heading.right.degrees, racetrack_half_distance
        )

        racetrack_end = racetrack_center.point_from_heading(
            orbit_heading.left.degrees, racetrack_half_distance
        )

        builder = WaypointBuilder(self.flight)

        altitude = builder.get_patrol_altitude

        racetrack = builder.race_track(racetrack_start, racetrack_end, altitude)

        return PatrollingLayout(
            departure=builder.takeoff(self.flight.departure),
            nav_to=builder.nav_path(
                self.flight.departure.position, racetrack_start, altitude
            ),
            nav_from=builder.nav_path(
                racetrack_end, self.flight.arrival.position, altitude
            ),
            patrol_start=racetrack[0],
            patrol_end=racetrack[1],
            arrival=builder.land(self.flight.arrival),
            divert=builder.divert(self.flight.divert),
            bullseye=builder.bullseye(),
            custom_waypoints=list(),
        )

    def build(self, dump_debug_info: bool = False) -> TheaterRefuelingFlightPlan:
        return TheaterRefuelingFlightPlan(self.flight, self.layout())
