"""InFlight.next_waypoint_state() must not crash when a flight advances past its
final waypoint.

Regression: a flight that exits combat at or after its last waypoint (e.g. a plan
with no explicit LANDING_POINT, or whose landing waypoint was already consumed)
used to build a Navigating state for an out-of-range index, which raised IndexError
in InFlight.__init__. The state machine now completes the flight instead.
"""

from __future__ import annotations

from datetime import timedelta
from types import SimpleNamespace
from typing import cast

from game.ato.flightstate.completed import Completed
from game.ato.flightstate.inflight import InFlight
from game.ato.flightwaypointtype import FlightWaypointType


def _next_state(waypoint_index: int, waypoint_count: int) -> object:
    """Run InFlight.next_waypoint_state() against a minimal fake, bypassing
    __init__. next_waypoint is a plain NAV waypoint so the routing falls through
    to the Navigating / end-of-plan branch."""
    waypoints = [SimpleNamespace(waypoint_type=FlightWaypointType.NAV)] * waypoint_count
    flight_plan = SimpleNamespace(
        waypoints=waypoints,
        travel_time_between_waypoints=lambda a, b: timedelta(),
    )
    fake = SimpleNamespace(
        waypoint_index=waypoint_index,
        next_waypoint=SimpleNamespace(waypoint_type=FlightWaypointType.NAV),
        flight=SimpleNamespace(flight_plan=flight_plan),
        settings=SimpleNamespace(),
    )
    return InFlight.next_waypoint_state(cast(InFlight, fake))


def test_advancing_past_final_waypoint_completes_flight() -> None:
    # waypoint_index 1 -> new_index 2 is the last index of a 3-waypoint plan, so
    # there is no waypoint after it: complete instead of raising.
    assert isinstance(_next_state(waypoint_index=1, waypoint_count=3), Completed)


def test_advancing_with_remaining_waypoints_keeps_navigating() -> None:
    # new_index 1 still has a waypoint after it, so the flight keeps navigating
    # rather than completing early.
    assert not isinstance(_next_state(waypoint_index=0, waypoint_count=3), Completed)
