from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterator, TYPE_CHECKING, Type

from game.utils import Distance, feet, meters
from .formationattack import (
    FormationAttackBuilder,
    FormationAttackFlightPlan,
    FormationAttackLayout,
)
from .planningerror import PlanningError
from .uizonedisplay import UiZone, UiZoneDisplay
from .waypointbuilder import WaypointBuilder
from ..flightwaypointtype import FlightWaypointType

if TYPE_CHECKING:
    from ..flightwaypoint import FlightWaypoint


@dataclass
class CsarLayout(FormationAttackLayout):
    pickup: FlightWaypoint | None = None

    def iter_waypoints(self) -> Iterator[FlightWaypoint]:
        yield self.departure
        yield from self.nav_to
        yield self.join
        yield self.ingress
        if self.pickup is not None:
            yield self.pickup
        yield self.targets[0]
        yield from self.nav_from
        yield self.arrival
        if self.divert is not None:
            yield self.divert
        yield self.bullseye
        yield from self.custom_waypoints


class CsarFlightPlan(FormationAttackFlightPlan, UiZoneDisplay):
    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder

    @property
    def tot_waypoint(self) -> FlightWaypoint:
        if self.layout.pickup is not None:
            return self.layout.pickup
        return self.layout.targets[0]

    @property
    def ingress_time(self) -> datetime:
        tot = self.tot
        travel_time = self.travel_time_between_waypoints(
            self.layout.ingress, self.tot_waypoint
        )
        return tot - travel_time

    def depart_time_for_waypoint(self, waypoint: FlightWaypoint) -> datetime | None:
        return None

    @property
    def csar_target_zone_radius(self) -> Distance:
        return meters(500)

    @property
    def mission_departure_time(self) -> datetime:
        return self.package.time_over_target

    def ui_zone(self) -> UiZone:
        return UiZone(
            [self.layout.targets[0].position],
            self.csar_target_zone_radius,
        )


class Builder(FormationAttackBuilder[CsarFlightPlan, CsarLayout]):
    def layout(self) -> CsarLayout:
        if not self.flight.is_helo and not self.flight.is_hercules:
            raise PlanningError(
                "CSAR is only usable by helicopters and Anubis' C-130 mod"
            )
        assert self.package.waypoints is not None

        builder = WaypointBuilder(self.flight)

        altitude = builder.get_cruise_altitude
        altitude_is_agl = self.flight.is_helo

        target = self.package.target

        ingress = builder.ingress(
            FlightWaypointType.INGRESS_CSAR,
            (
                self.package.waypoints.ingress
                if not self.flight.is_hercules
                else self.package.waypoints.initial
            ),
            target,
        )

        # Marker/target waypoint at the pilot's location (shown to players, drives
        # the CTLD-style landing zone radius on the map).
        pickup_area = builder.assault_area(target)
        if self.flight.is_hercules:
            pickup_area.only_for_player = False
            pickup_area.alt = feet(1000)

        # Helicopters get a landing task at the pilot; fixed wing only overflies.
        pickup = builder.csar_pickup(target) if self.flight.is_helo else None
        pickup_position = pickup.position if pickup is not None else target.position

        return CsarLayout(
            departure=builder.takeoff(self.flight.departure),
            nav_to=builder.nav_path(
                self.flight.departure.position,
                ingress.position,
                altitude,
                altitude_is_agl,
            ),
            ingress=ingress,
            pickup=pickup,
            targets=[pickup_area],
            nav_from=builder.nav_path(
                pickup_position,
                self.flight.arrival.position,
                altitude,
                altitude_is_agl,
            ),
            arrival=builder.land(self.flight.arrival),
            divert=builder.divert(self.flight.divert),
            bullseye=builder.bullseye(),
            hold=None,
            join=builder.join(self.package.waypoints.ingress),
            split=builder.split(self.flight.arrival.position),
            refuel=None,
            custom_waypoints=list(),
        )

    def build(self, dump_debug_info: bool = False) -> CsarFlightPlan:
        return CsarFlightPlan(self.flight, self.layout())
