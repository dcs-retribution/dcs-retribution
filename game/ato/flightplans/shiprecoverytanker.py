from __future__ import annotations

from datetime import timedelta
from typing import Type

from game.ato.flightplans.ibuilder import IBuilder
from game.ato.flightplans.waypointbuilder import WaypointBuilder
from .patrolling import PatrollingLayout
from .refuelingflightplan import RefuelingFlightPlan
from .. import FlightWaypoint
from ...utils import knots


class RecoveryTankerFlightPlan(RefuelingFlightPlan):
    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder

    @property
    def patrol_duration(self) -> timedelta:
        return self.flight.coalition.game.settings.desired_tanker_on_station_time

    @property
    def tot_waypoint(self) -> FlightWaypoint:
        return self.layout.departure


class Builder(IBuilder[RecoveryTankerFlightPlan, PatrollingLayout]):
    def layout(self) -> PatrollingLayout:

        builder = WaypointBuilder(self.flight)
        altitude = builder.get_patrol_altitude

        station_time = self.coalition.game.settings.desired_tanker_on_station_time
        time_to_landing = station_time.total_seconds()
        hdg = (self.coalition.game.conditions.weather.wind.at_0m.direction + 180) % 360
        recovery_ship = self.package.target.position.point_from_heading(
            hdg, time_to_landing * knots(20).meters_per_second
        )
        recovery_tanker = builder.recovery_tanker(recovery_ship)
        patrol_end = builder.race_track_end(recovery_tanker.position, altitude)
        patrol_end.only_for_player = True  # avoid generating the waypoints

        return PatrollingLayout(
            departure=builder.takeoff(self.flight.departure),
            nav_to=builder.nav_path(
                self.flight.departure.position, recovery_ship, altitude
            ),
            nav_from=builder.nav_path(
                recovery_ship, self.flight.arrival.position, altitude
            ),
            patrol_start=recovery_tanker,
            patrol_end=patrol_end,
            arrival=builder.land(self.flight.arrival),
            divert=builder.divert(self.flight.divert),
            bullseye=builder.bullseye(),
            custom_waypoints=list(),
        )

    def build(self, dump_debug_info: bool = False) -> RecoveryTankerFlightPlan:
        return RecoveryTankerFlightPlan(self.flight, self.layout())
