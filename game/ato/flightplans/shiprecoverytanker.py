from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from typing import Iterator, Type
from game.ato.flightplans.ibuilder import IBuilder
from .patrolling import PatrollingLayout
from .refuelingflightplan import RefuelingFlightPlan
from game.ato.flightplans.waypointbuilder import WaypointBuilder
from game.ato.flightwaypoint import FlightWaypoint


class RecoveryTankerFlightPlan(RefuelingFlightPlan):
    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder

    @property
    def patrol_duration(self) -> timedelta:
        return self.flight.coalition.game.settings.desired_tanker_on_station_time


class Builder(IBuilder[RecoveryTankerFlightPlan, PatrollingLayout]):
    def layout(self) -> PatrollingLayout:

        builder = WaypointBuilder(self.flight)
        # TODO: Propagate the ship position to the Tanker's TOT,
        # so that we minimize the tanker's need to catch up to the carrier.
        recovery_ship = self.package.target.position
        recovery_tanker = builder.recovery_tanker(recovery_ship)

        altitude = builder.get_patrol_altitude

        return PatrollingLayout(
            departure=builder.takeoff(self.flight.departure),
            nav_to=builder.nav_path(
                self.flight.departure.position, recovery_ship, altitude
            ),
            nav_from=builder.nav_path(
                recovery_ship, self.flight.arrival.position, altitude
            ),
            patrol_start=recovery_tanker,
            patrol_end=builder.land(self.flight.arrival),
            arrival=builder.land(self.flight.arrival),
            divert=builder.divert(self.flight.divert),
            bullseye=builder.bullseye(),
            custom_waypoints=list(),
        )

    def build(self, dump_debug_info: bool = False) -> RecoveryTankerFlightPlan:
        return RecoveryTankerFlightPlan(self.flight, self.layout())
