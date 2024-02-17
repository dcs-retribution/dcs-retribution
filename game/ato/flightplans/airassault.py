from __future__ import annotations

import random
from dataclasses import dataclass
from datetime import datetime
from typing import Iterator, TYPE_CHECKING, Type

from game.theater.controlpoint import ControlPointType
from game.theater.missiontarget import MissionTarget
from game.utils import Distance, feet, meters
from ._common_ctld import generate_random_ctld_point
from .formationattack import (
    FormationAttackLayout,
    FormationAttackBuilder,
    FormationAttackFlightPlan,
)
from .planningerror import PlanningError
from .uizonedisplay import UiZone, UiZoneDisplay
from .waypointbuilder import WaypointBuilder
from ..flightwaypoint import FlightWaypointType
from ...theater.interfaces.CTLD import CTLD

if TYPE_CHECKING:
    from dcs import Point
    from ..flightwaypoint import FlightWaypoint


@dataclass
class AirAssaultLayout(FormationAttackLayout):
    # The pickup point is optional because we don't always need to load the cargo. When
    # departing from a carrier, LHA, or off-map spawn, the cargo is pre-loaded.
    pickup: FlightWaypoint | None = None
    drop_off: FlightWaypoint | None = None
    # This is an implementation detail used by CTLD. The aircraft will not go to this
    # waypoint. It is used by CTLD as the destination for unloaded troops.

    def iter_waypoints(self) -> Iterator[FlightWaypoint]:
        yield self.departure
        if self.pickup is not None:
            yield self.pickup
        yield from self.nav_to
        yield self.ingress
        if self.drop_off is not None:
            yield self.drop_off
        yield self.targets[0]
        yield from self.nav_from
        yield self.arrival
        if self.divert is not None:
            yield self.divert
        yield self.bullseye


class AirAssaultFlightPlan(FormationAttackFlightPlan, UiZoneDisplay):
    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder

    @property
    def is_airassault(self) -> bool:
        return True

    @property
    def tot_waypoint(self) -> FlightWaypoint:
        if self.flight.is_helo and self.layout.drop_off is not None:
            return self.layout.drop_off
        return self.layout.targets[0]

    @property
    def ingress_time(self) -> datetime:
        tot = self.tot
        travel_time = self.travel_time_between_waypoints(
            self.layout.ingress, self.tot_waypoint
        )
        return tot - travel_time

    def tot_for_waypoint(self, waypoint: FlightWaypoint) -> datetime | None:
        if waypoint is self.tot_waypoint:
            return self.tot
        elif waypoint is self.layout.ingress:
            return self.ingress_time
        return None

    def depart_time_for_waypoint(self, waypoint: FlightWaypoint) -> datetime | None:
        return None

    @property
    def ctld_target_zone_radius(self) -> Distance:
        return meters(2500)

    @property
    def mission_begin_on_station_time(self) -> datetime | None:
        return None

    @property
    def mission_departure_time(self) -> datetime:
        return self.package.time_over_target

    def ui_zone(self) -> UiZone:
        return UiZone(
            [self.layout.targets[0].position],
            self.ctld_target_zone_radius,
        )


class Builder(FormationAttackBuilder[AirAssaultFlightPlan, AirAssaultLayout]):
    def layout(self) -> AirAssaultLayout:
        if not self.flight.is_helo and not self.flight.is_hercules:
            raise PlanningError(
                "Air assault is only usable by helicopters and Anubis' C-130 mod"
            )
        assert self.package.waypoints is not None

        heli_alt = feet(self.coalition.game.settings.heli_cruise_alt_agl)
        altitude = heli_alt if self.flight.is_helo else self.doctrine.ingress_altitude
        altitude_is_agl = self.flight.is_helo

        builder = WaypointBuilder(self.flight)

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
            pickup.alt = heli_alt
            pickup_position = pickup.position

        ingress = builder.ingress(
            FlightWaypointType.INGRESS_AIR_ASSAULT,
            self.package.waypoints.ingress,
            self.package.target,
        )

        assault_area = builder.assault_area(self.package.target)
        if self.flight.is_hercules:
            assault_area.only_for_player = False
            assault_area.alt = feet(1000)

        tgt = self.package.target
        if isinstance(tgt, CTLD) and tgt.ctld_zones:
            top3 = sorted(
                tgt.ctld_zones, key=lambda x: ingress.position.distance_to_point(x[0])
            )[:3]
            closest = random.choice(top3)
            drop_pos = closest[0].random_point_within(closest[1])
        else:
            heading = tgt.position.heading_between_point(ingress.position)
            drop_pos = tgt.position.point_from_heading(heading, 1200)
        drop_off_zone = MissionTarget("Dropoff zone", drop_pos)
        dz = builder.dropoff_zone(drop_off_zone) if self.flight.is_helo else None
        if dz:
            dz.alt = heli_alt

        return AirAssaultLayout(
            departure=builder.takeoff(self.flight.departure),
            pickup=pickup,
            nav_to=builder.nav_path(
                pickup_position,
                self.package.waypoints.ingress,
                altitude,
                altitude_is_agl,
            ),
            ingress=ingress,
            drop_off=dz,
            targets=[assault_area],
            nav_from=builder.nav_path(
                drop_off_zone.position,
                self.flight.arrival.position,
                altitude,
                altitude_is_agl,
            ),
            arrival=builder.land(self.flight.arrival),
            divert=builder.divert(self.flight.divert),
            bullseye=builder.bullseye(),
            hold=None,
            join=builder.join(pickup_position),
            split=builder.split(self.package.waypoints.split),
            refuel=None,
        )

    def build(self, dump_debug_info: bool = False) -> AirAssaultFlightPlan:
        return AirAssaultFlightPlan(self.flight, self.layout())

    def _generate_ctld_pickup(self) -> Point:
        assert isinstance(self.flight.departure, CTLD)
        return generate_random_ctld_point(self.flight.departure)
