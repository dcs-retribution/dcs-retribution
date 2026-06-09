from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from dcs import Point

from game.ato.flightstate import Completed
from game.ato.flightstate.flightstate import FlightState
from game.ato.flightwaypoint import FlightWaypoint
from game.ato.flightwaypointtype import FlightWaypointType
from game.ato.starttype import StartType
from game.utils import Distance, LBS_TO_KG, Speed, pairwise

if TYPE_CHECKING:
    from game.ato.flight import Flight
    from game.settings import Settings
    from game.sim.gameupdateevents import GameUpdateEvents


class InFlight(FlightState, ABC):
    def __init__(
        self,
        flight: Flight,
        settings: Settings,
        waypoint_index: int,
        has_aborted: bool = False,
        elapsed_time: timedelta = timedelta(),
    ) -> None:
        super().__init__(flight, settings)
        waypoints = self.flight.flight_plan.waypoints
        self.waypoint_index = waypoint_index
        self.has_aborted = has_aborted
        self.current_waypoint = waypoints[self.waypoint_index]
        # Guard against flight plans that have no landing waypoint or whose
        # waypoint list ends earlier than expected (e.g. SCRAMBLE BarCap plans
        # that exit combat at the last waypoint).  next_waypoint_state() now
        # catches this before creating InFlight subclasses, but keep the check
        # here too so any future call sites get a clear error rather than a
        # confusing IndexError.
        if self.waypoint_index + 1 >= len(waypoints):
            raise ValueError(
                f"Flight {self.flight.flight_plan} has no waypoint after index "
                f"{self.waypoint_index} (plan has {len(waypoints)} waypoints). "
                "The flight plan is missing a terminal landing waypoint."
            )
        self.next_waypoint = waypoints[self.waypoint_index + 1]
        self.total_time_to_next_waypoint = self.travel_time_between_waypoints()
        self.elapsed_time = elapsed_time
        self.current_waypoint_elapsed = False

    @property
    def cancelable(self) -> bool:
        return False

    @property
    def in_flight(self) -> bool:
        return True

    def has_passed_waypoint(self, waypoint: FlightWaypoint) -> bool:
        index = self.flight.flight_plan.waypoints.index(waypoint)
        return index <= self.waypoint_index

    def travel_time_between_waypoints(self) -> timedelta:
        return self.flight.flight_plan.travel_time_between_waypoints(
            self.current_waypoint, self.next_waypoint
        )

    @abstractmethod
    def estimate_position(self) -> Point: ...

    @abstractmethod
    def estimate_altitude(self) -> tuple[Distance, str]: ...

    @abstractmethod
    def estimate_speed(self) -> Speed: ...

    def estimate_fuel_at_current_waypoint(self) -> float:
        initial_fuel = super().estimate_fuel()
        if self.flight.unit_type.fuel_consumption is None:
            return initial_fuel
        initial_fuel -= self.flight.unit_type.fuel_consumption.taxi * LBS_TO_KG
        waypoints = self.flight.flight_plan.waypoints[: self.waypoint_index + 1]
        for a, b in pairwise(waypoints[:-1]):
            consumption = self.flight.flight_plan.fuel_consumption_between_points(a, b)
            assert consumption is not None
            initial_fuel -= consumption * LBS_TO_KG
        return initial_fuel

    def next_waypoint_state(self) -> FlightState:
        from .loiter import Loiter
        from .racetrack import RaceTrack
        from .navigating import Navigating

        new_index = self.waypoint_index + 1
        if self.next_waypoint.waypoint_type is FlightWaypointType.LANDING_POINT:
            return Completed(self.flight, self.settings)
        if self.next_waypoint.waypoint_type is FlightWaypointType.PATROL_TRACK:
            return RaceTrack(self.flight, self.settings, new_index)
        if self.next_waypoint.waypoint_type is FlightWaypointType.LOITER:
            return Loiter(self.flight, self.settings, new_index)
        # Guard: if new_index is the last waypoint there is no [new_index + 1]
        # and Navigating.__init__ will crash.  This happens when a flight exits
        # combat at or past its final waypoint (e.g. a SCRAMBLE BarCap orbit
        # whose plan has no explicit LANDING_POINT, or whose landing waypoint
        # was already consumed before the combat state was entered).
        # Complete the flight rather than crashing.
        if new_index + 1 >= len(self.flight.flight_plan.waypoints):
            return Completed(self.flight, self.settings)
        return Navigating(self.flight, self.settings, new_index)

    def advance_to_next_waypoint(self) -> FlightState:
        new_state = self.next_waypoint_state()
        self.flight.set_state(new_state)
        self.current_waypoint_elapsed = True
        return new_state

    def on_game_tick(
        self, events: GameUpdateEvents, time: datetime, duration: timedelta
    ) -> None:
        self.elapsed_time += duration
        if self.elapsed_time > self.total_time_to_next_waypoint:
            new_state = self.advance_to_next_waypoint()

            # Roll over any extra time to the next state. We don't need to loop here
            # even if we've passed more than one waypoint because the new state will do
            # the same. There is a small gap here where we only do that for other *in
            # flight* states. We don't need to tick combat states (combat is ticked
            # separately) or completed states at all, so the only states that might be
            # under-ticked are the pre-takeoff states, where it's not really that
            # critical if we under-simulate them by the tick period or less. The tick
            # period at time of writing is one second. Not enough to throw off ground
            # ops, but at 600 knots we'd be getting the position wrong by up to 1000
            # feet.
            rollover = self.elapsed_time - self.total_time_to_next_waypoint
            new_state.on_game_tick(events, time, rollover)

    @property
    def is_at_ip(self) -> bool:
        contact_types = {
            FlightWaypointType.INGRESS_BAI,
            FlightWaypointType.INGRESS_CAS,
            FlightWaypointType.INGRESS_DEAD,
            FlightWaypointType.INGRESS_OCA_AIRCRAFT,
            FlightWaypointType.INGRESS_OCA_RUNWAY,
            FlightWaypointType.INGRESS_SEAD,
            FlightWaypointType.INGRESS_STRIKE,
            FlightWaypointType.INGRESS_AIR_ASSAULT,
        }
        return self.current_waypoint.waypoint_type in contact_types

    @property
    def vulnerable_to_intercept(self) -> bool:
        return True

    @property
    def vulnerable_to_sam(self) -> bool:
        return True

    @property
    def will_join_air_combat(self) -> bool:
        return self.flight.flight_type.is_air_to_air

    @property
    def is_waiting_for_start(self) -> bool:
        return False

    @property
    def spawn_type(self) -> StartType:
        return StartType.IN_FLIGHT

    @property
    def description(self) -> str:
        if self.has_aborted:
            abort = "(Aborted) "
        else:
            abort = ""
        return f"{abort}Flying to {self.next_waypoint.name}"
