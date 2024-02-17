from __future__ import annotations

import random
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from typing import TYPE_CHECKING, Type

from game.theater.missiontarget import MissionTarget
from game.utils import feet, Distance
from ._common_ctld import generate_random_ctld_point
from .ibuilder import IBuilder
from .planningerror import PlanningError
from .standard import StandardFlightPlan, StandardLayout
from .waypointbuilder import WaypointBuilder
from ..flightwaypointtype import FlightWaypointType
from ...theater.interfaces.CTLD import CTLD

if TYPE_CHECKING:
    from ..flightwaypoint import FlightWaypoint
    from dcs import Point


@dataclass
class AirliftLayout(StandardLayout):
    pickup_ascent: FlightWaypoint | None
    pickup_descent: FlightWaypoint | None
    # There will not be a pickup waypoint when the pickup airfield is the departure
    # airfield for cargo planes, as the cargo is pre-loaded. Helicopters will still pick
    # up the cargo near the airfield.
    pickup: FlightWaypoint | None
    # pickup_zone will be used for player flights to create the CTLD stuff
    ctld_pickup_zone: FlightWaypoint | None
    drop_off_ascent: FlightWaypoint | None
    nav_to_drop_off: list[FlightWaypoint]
    drop_off_descent: FlightWaypoint | None
    # There will not be a drop-off waypoint when the drop-off airfield and the arrival
    # airfield is the same for a cargo plane, as planes will land to unload and we don't
    # want a double landing. Helicopters will still drop their cargo near the airfield
    # before landing.
    drop_off: FlightWaypoint | None
    # drop_off_zone will be used for player flights to create the CTLD stuff
    ctld_drop_off_zone: FlightWaypoint | None
    return_ascent: FlightWaypoint | None
    return_descent: FlightWaypoint | None

    def add_waypoint(
        self, wpt: FlightWaypoint, next_wpt: Optional[FlightWaypoint]
    ) -> bool:
        new_wpt = self.get_midpoint(wpt, next_wpt)
        if wpt.waypoint_type in [
            FlightWaypointType.PICKUP_ZONE,
            FlightWaypointType.CARGO_STOP,
        ]:
            self.nav_to_drop_off.insert(0, new_wpt)
            return True
        return super().add_waypoint(wpt, next_wpt)

    def delete_waypoint(self, waypoint: FlightWaypoint) -> bool:
        if waypoint in self.nav_to_drop_off:
            self.nav_to_drop_off.remove(waypoint)
            return True
        elif super().delete_waypoint(waypoint):
            return True
        return False

    def iter_waypoints(self) -> Iterator[FlightWaypoint]:
        yield self.departure
        if self.pickup_ascent is not None:
            yield self.pickup_ascent
        yield from self.nav_to
        if self.pickup_descent is not None:
            yield self.pickup_descent
        if self.pickup is not None:
            yield self.pickup
        if self.ctld_pickup_zone is not None:
            yield self.ctld_pickup_zone
        if self.drop_off_ascent is not None:
            yield self.drop_off_ascent
        yield from self.nav_to_drop_off
        if self.drop_off_descent is not None:
            yield self.drop_off_descent
        if self.drop_off is not None:
            yield self.drop_off
        if self.return_ascent is not None:
            yield self.return_ascent
        if self.ctld_drop_off_zone is not None:
            yield self.ctld_drop_off_zone
        yield from self.nav_from
        if self.return_descent is not None:
            yield self.return_descent
        yield self.arrival
        if self.divert is not None:
            yield self.divert
        yield self.bullseye


class AirliftFlightPlan(StandardFlightPlan[AirliftLayout]):
    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder

    @property
    def tot_waypoint(self) -> FlightWaypoint:
        # The TOT is the time that the cargo will be dropped off. If the drop-off
        # location is the arrival airfield and this is not a helicopter flight, there
        # will not be a separate drop-off waypoint; the arrival landing waypoint is the
        # drop-off waypoint.
        return self.layout.drop_off or self.layout.arrival

    def tot_for_waypoint(self, waypoint: FlightWaypoint) -> datetime | None:
        # TOT planning isn't really useful for transports. They're behind the front
        # lines so no need to wait for escorts or for other missions to complete.
        return None

    def depart_time_for_waypoint(self, waypoint: FlightWaypoint) -> datetime | None:
        return None

    @property
    def mission_begin_on_station_time(self) -> datetime | None:
        return None

    @property
    def mission_departure_time(self) -> datetime:
        return self.package.time_over_target


class Builder(IBuilder[AirliftFlightPlan, AirliftLayout]):
    def layout(self) -> AirliftLayout:
        cargo = self.flight.cargo
        if cargo is None:
            raise PlanningError(
                "Cannot plan transport mission for flight with no cargo."
            )

        heli_alt = feet(self.coalition.game.settings.heli_cruise_alt_agl)
        altitude = heli_alt if self.flight.is_helo else self.doctrine.ingress_altitude
        altitude_is_agl = self.flight.is_helo

        builder = WaypointBuilder(self.flight)

        pickup_ascent = None
        pickup_descent = None
        pickup = None
        drop_off_ascent = None
        drop_off_descent = None
        drop_off = None
        pickup_zone = None
        drop_off_zone = None

        if cargo.origin != self.flight.departure:
            pickup = builder.cargo_stop(cargo.origin)
            pickup_ascent = self._create_ascent_or_descent(
                builder,
                self.flight.departure.position,
                cargo.origin.position,
                altitude,
                altitude_is_agl,
            )
            pickup_descent = self._create_ascent_or_descent(
                builder,
                cargo.origin.position,
                self.flight.departure.position,
                altitude,
                altitude_is_agl,
            )
        if cargo.next_stop != self.flight.arrival:
            drop_off = builder.cargo_stop(cargo.next_stop)
            drop_off_ascent = self._create_ascent_or_descent(
                builder,
                cargo.origin.position,
                cargo.next_stop.position,
                altitude,
                altitude_is_agl,
            )
            drop_off_descent = self._create_ascent_or_descent(
                builder,
                cargo.next_stop.position,
                cargo.origin.position,
                altitude,
                altitude_is_agl,
            )

        if self.flight.is_helo:
            # Create CTLD Zones for Helo flights
            pickup_zone = builder.pickup_zone(
                MissionTarget("Pickup Zone", self._generate_ctld_pickup())
            )
            drop_off_zone = builder.dropoff_zone(
                MissionTarget("Dropoff zone", self._generate_ctld_dropoff())
            )
            # Show the zone waypoints only to the player
            pickup_zone.only_for_player = True
            drop_off_zone.only_for_player = True

        nav_to_pickup = builder.nav_path(
            self.flight.departure.position,
            cargo.origin.position,
            altitude,
            altitude_is_agl,
        )

        return_ascent = self._create_ascent_or_descent(
            builder,
            cargo.next_stop.position
            if cargo.next_stop != self.flight.arrival
            else cargo.origin.position,
            self.flight.arrival.position,
            altitude,
            altitude_is_agl,
        )
        return_descent = self._create_ascent_or_descent(
            builder,
            self.flight.arrival.position,
            cargo.next_stop.position
            if cargo.next_stop != self.flight.arrival
            else cargo.origin.position,
            altitude,
            altitude_is_agl,
        )

        return AirliftLayout(
            departure=builder.takeoff(self.flight.departure),
            pickup_ascent=pickup_ascent,
            nav_to=nav_to_pickup,
            pickup_descent=pickup_descent,
            pickup=pickup,
            ctld_pickup_zone=pickup_zone,
            drop_off_ascent=drop_off_ascent,
            nav_to_drop_off=builder.nav_path(
                cargo.origin.position,
                cargo.next_stop.position,
                altitude,
                altitude_is_agl,
            ),
            drop_off_descent=drop_off_descent,
            drop_off=drop_off,
            ctld_drop_off_zone=drop_off_zone,
            return_ascent=return_ascent,
            nav_from=builder.nav_path(
                cargo.origin.position,
                self.flight.arrival.position,
                altitude,
                altitude_is_agl,
            ),
            return_descent=return_descent,
            arrival=builder.land(self.flight.arrival),
            divert=builder.divert(self.flight.divert),
            bullseye=builder.bullseye(),
        )

    def build(self, dump_debug_info: bool = False) -> AirliftFlightPlan:
        return AirliftFlightPlan(self.flight, self.layout())

    def _generate_ctld_pickup(self) -> Point:
        cargo = self.flight.cargo
        if cargo and cargo.origin and isinstance(cargo.origin, CTLD):
            return generate_random_ctld_point(cargo.origin)
        raise RuntimeError("Could not generate CTLD pickup")

    def _generate_ctld_dropoff(self) -> Point:
        cargo = self.flight.cargo
        if cargo and cargo.transport and isinstance(cargo.transport.destination, CTLD):
            return generate_random_ctld_point(cargo.transport.destination)
        raise RuntimeError("Could not generate CTLD dropoff")

    @staticmethod
    def _create_ascent_or_descent(
        builder: WaypointBuilder,
        start: Point,
        end: Point,
        alt: Distance,
        agl: bool,
    ) -> FlightWaypoint:
        distance = start.distance_to_point(end)
        rdistance = 1000 if agl else min(distance / 10, 20000)
        heading = round(start.heading_between_point(end))
        rheading = random.randint(heading - 30, heading + 30) % 360
        pos = start.point_from_heading(float(rheading), rdistance)
        return builder.nav(pos, alt, agl)
