from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from typing import Iterator, TYPE_CHECKING, Type

from game.ato.flightplans.standard import StandardFlightPlan, StandardLayout
from game.theater.controlpoint import ControlPointType
from game.theater.missiontarget import MissionTarget
from game.utils import Distance, feet, meters
from ._common_ctld import generate_random_ctld_point
from .ibuilder import IBuilder
from .planningerror import PlanningError
from .uizonedisplay import UiZone, UiZoneDisplay
from .waypointbuilder import WaypointBuilder
from ..flightwaypoint import FlightWaypointType
from ...theater.interfaces.CTLD import CTLD

if TYPE_CHECKING:
    from dcs import Point
    from ..flightwaypoint import FlightWaypoint


@dataclass
class AirAssaultLayout(StandardLayout):
    # The pickup point is optional because we don't always need to load the cargo. When
    # departing from a carrier, LHA, or off-map spawn, the cargo is pre-loaded.
    pickup: FlightWaypoint | None
    nav_to_ingress: list[FlightWaypoint]
    ingress: FlightWaypoint
    drop_off: FlightWaypoint | None
    # This is an implementation detail used by CTLD. The aircraft will not go to this
    # waypoint. It is used by CTLD as the destination for unloaded troops.
    target: FlightWaypoint
    nav_to_home: list[FlightWaypoint]

    def iter_waypoints(self) -> Iterator[FlightWaypoint]:
        yield self.departure
        if self.pickup is not None:
            yield self.pickup
        yield from self.nav_to_ingress
        yield self.ingress
        if self.drop_off is not None:
            yield self.drop_off
        yield self.target
        yield from self.nav_to_home
        yield self.arrival
        if self.divert is not None:
            yield self.divert
        yield self.bullseye


class AirAssaultFlightPlan(StandardFlightPlan[AirAssaultLayout], UiZoneDisplay):
    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder

    @property
    def tot_waypoint(self) -> FlightWaypoint:
        if self.flight.is_helo and self.layout.drop_off is not None:
            return self.layout.drop_off
        return self.layout.target

    def tot_for_waypoint(self, waypoint: FlightWaypoint) -> timedelta | None:
        if waypoint == self.tot_waypoint:
            return self.tot
        return None

    def depart_time_for_waypoint(self, waypoint: FlightWaypoint) -> timedelta | None:
        return None

    @property
    def ctld_target_zone_radius(self) -> Distance:
        return meters(2500)

    @property
    def mission_departure_time(self) -> timedelta:
        return self.package.time_over_target

    def ui_zone(self) -> UiZone:
        return UiZone(
            [self.layout.target.position],
            self.ctld_target_zone_radius,
        )


class Builder(IBuilder[AirAssaultFlightPlan, AirAssaultLayout]):
    def layout(self) -> AirAssaultLayout:
        if not self.flight.is_helo and not self.flight.is_hercules:
            raise PlanningError(
                "Air assault is only usable by helicopters and Anubis' C-130 mod"
            )
        assert self.package.waypoints is not None

        altitude = feet(1500) if self.flight.is_helo else self.doctrine.ingress_altitude
        altitude_is_agl = self.flight.is_helo

        builder = WaypointBuilder(self.flight, self.coalition)

        if self.flight.is_hercules or self.flight.departure.cptype in [
            ControlPointType.AIRCRAFT_CARRIER_GROUP,
            ControlPointType.LHA_GROUP,
            ControlPointType.OFF_MAP,
        ]:
            # Off_Map spawns will be preloaded
            # Carrier operations load the logistics directly from the carrier
            pickup = None
            pickup_position = self.flight.departure.position
        else:
            pickup = builder.pickup_zone(
                MissionTarget(
                    "Pickup Zone",
                    self._generate_ctld_pickup(),
                )
            )
            pickup_position = pickup.position
        assault_area = builder.assault_area(self.package.target)
        heading = self.package.target.position.heading_between_point(pickup_position)
        if self.flight.is_hercules:
            assault_area.only_for_player = False
            assault_area.alt = feet(1000)

        # TODO: define CTLD dropoff zones in campaign miz?
        drop_off_zone = MissionTarget(
            "Dropoff zone",
            self.package.target.position.point_from_heading(heading, 1200),
        )
        dz = builder.dropoff_zone(drop_off_zone) if self.flight.is_helo else None

        return AirAssaultLayout(
            departure=builder.takeoff(self.flight.departure),
            pickup=pickup,
            nav_to_ingress=builder.nav_path(
                pickup_position,
                self.package.waypoints.ingress,
                altitude,
                altitude_is_agl,
            ),
            ingress=builder.ingress(
                FlightWaypointType.INGRESS_AIR_ASSAULT,
                self.package.waypoints.ingress,
                self.package.target,
            ),
            drop_off=dz,
            target=assault_area,
            nav_to_home=builder.nav_path(
                drop_off_zone.position,
                self.flight.arrival.position,
                altitude,
                altitude_is_agl,
            ),
            arrival=builder.land(self.flight.arrival),
            divert=builder.divert(self.flight.divert),
            bullseye=builder.bullseye(),
        )

    def build(self) -> AirAssaultFlightPlan:
        return AirAssaultFlightPlan(self.flight, self.layout())

    def _generate_ctld_pickup(self) -> Point:
        assert isinstance(self.flight.departure, CTLD)
        return generate_random_ctld_point(self.flight.departure)
