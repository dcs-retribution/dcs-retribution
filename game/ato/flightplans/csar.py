from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterator, TYPE_CHECKING, Type

from game.theater.missiontarget import MissionTarget
from game.utils import Distance, meters
from .ibuilder import IBuilder
from .planningerror import PlanningError
from .standard import StandardFlightPlan, StandardLayout
from .uizonedisplay import UiZone, UiZoneDisplay
from .waypointbuilder import WaypointBuilder
from ..flightwaypointtype import FlightWaypointType

if TYPE_CHECKING:
    from dcs.mapping import Point
    from ..flightwaypoint import FlightWaypoint

#: How far the rescue helicopter's touchdown point sits from the survivor. Far
#: enough that landing on the waypoint doesn't crush them, close enough to stay
#: inside the embark zone (see EMBARK_ZONE_RADIUS in csargenerator.py) so DCS
#: still walks them out to the helicopter.
LANDING_ZONE_OFFSET = meters(150)


@dataclass
class CsarLayout(StandardLayout):
    # Ingress toward the downed pilot. Kept so players get a sensible run-in and so
    # the AI descends before the pickup.
    ingress: FlightWaypoint
    # The pickup itself. Helicopters get a landing task here (LandingZoneBuilder);
    # fixed-wing aircraft only overfly it, since the DCS AI Land task is
    # helicopter-only.
    pickup: FlightWaypoint

    def iter_waypoints(self) -> Iterator[FlightWaypoint]:
        yield self.departure
        yield from self.nav_to
        yield self.ingress
        yield self.pickup
        yield from self.nav_from
        yield self.arrival
        if self.divert is not None:
            yield self.divert
        yield self.bullseye
        yield from self.custom_waypoints


class CsarFlightPlan(StandardFlightPlan[CsarLayout], UiZoneDisplay):
    """Flight plan for recovering a downed pilot.

    Modelled on the airlift plan rather than the formation-attack plans: a CSAR
    target is a *friendly* downed pilot, and ``IBuilder`` deliberately skips
    package-waypoint generation for friendly targets, so anything deriving from
    FormationAttackFlightPlan would have no package waypoints to build from.
    """

    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder

    @property
    def tot_waypoint(self) -> FlightWaypoint:
        return self.layout.pickup

    def tot_for_waypoint(self, waypoint: FlightWaypoint) -> datetime | None:
        # Like transports, CSAR flights operate on their own schedule; there is no
        # package to synchronize a time-on-target with.
        return None

    def depart_time_for_waypoint(self, waypoint: FlightWaypoint) -> datetime | None:
        return None

    @property
    def mission_begin_on_station_time(self) -> datetime | None:
        return None

    @property
    def mission_departure_time(self) -> datetime:
        return self.package.time_over_target

    @property
    def csar_target_zone_radius(self) -> Distance:
        return meters(500)

    def ui_zone(self) -> UiZone:
        return UiZone([self.layout.pickup.position], self.csar_target_zone_radius)


class Builder(IBuilder[CsarFlightPlan, CsarLayout]):
    def layout(self) -> CsarLayout:
        # Helicopters only: the pickup is an unprepared site and the DCS AI Land
        # task is helicopter-only, so a fixed-wing CSAR flight would just orbit.
        if not self.flight.is_helo:
            raise PlanningError("CSAR is only usable by helicopters")

        builder = WaypointBuilder(self.flight)

        altitude = builder.get_cruise_altitude
        altitude_is_agl = True

        target = self.package.target

        # Run in from the departure side of the pilot so the approach doesn't
        # overfly the pickup. Package waypoints don't exist for friendly targets,
        # so the ingress is derived from the departure->target line.
        heading = target.position.heading_between_point(self.flight.departure.position)
        ingress_position = target.position.point_from_heading(
            heading, self._ingress_distance.meters
        )
        ingress = builder.ingress(
            FlightWaypointType.INGRESS_CSAR, ingress_position, target
        )

        # The landing zone is deliberately offset from the survivor. The AI puts
        # the helicopter down exactly on its waypoint, and a pilot standing there
        # gets crushed. The offset stays well inside the pilot's embark zone so
        # they still walk over to board.
        pickup = builder.csar_pickup(
            MissionTarget(target.name, self._landing_zone_for(target))
        )

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
            nav_from=builder.nav_path(
                pickup.position,
                self.flight.arrival.position,
                altitude,
                altitude_is_agl,
            ),
            arrival=builder.land(self.flight.arrival),
            divert=builder.divert(self.flight.divert),
            bullseye=builder.bullseye(),
            custom_waypoints=list(),
        )

    def _landing_zone_for(self, target: MissionTarget) -> Point:
        """A touchdown point clear of the survivor but inside their embark zone.

        Prefers the approach side (between the pilot and the departure airfield)
        and falls back through other bearings if that lands in water or an
        exclusion zone.
        """
        theater = self.theater
        toward_home = target.position.heading_between_point(
            self.flight.departure.position
        )
        for offset in (0, 45, -45, 90, -90, 135, -135, 180):
            candidate = target.position.point_from_heading(
                (toward_home + offset) % 360, LANDING_ZONE_OFFSET.meters
            )
            if theater.is_on_land(candidate):
                return candidate
        # Nowhere better; the pilot's own position was already land-validated, so
        # accept the approach-side point and let the AI sort out the touchdown.
        return target.position.point_from_heading(
            toward_home, LANDING_ZONE_OFFSET.meters
        )

    @property
    def _ingress_distance(self) -> Distance:
        from game.utils import nautical_miles

        return nautical_miles(5)

    def build(self, dump_debug_info: bool = False) -> CsarFlightPlan:
        return CsarFlightPlan(self.flight, self.layout())
