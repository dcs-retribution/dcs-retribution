"""InFlight.next_waypoint_state() must not crash when a flight advances past its
final waypoint.

Regression: a flight that reaches or exits combat at its last waypoint used to
build an InFlight subclass for an out-of-range index, which raised in
InFlight.__init__. Two shapes trigger it:

* a plan with no explicit LANDING_POINT (or whose landing waypoint was already
  consumed) advancing onto a terminal NAV waypoint, and
* a custom plan whose final waypoint is a PATROL_TRACK or LOITER -- these routed
  to RaceTrack / Loiter *before* the end-of-plan check, so the guard never ran
  and construction still crashed.

next_waypoint_state() now guards the end of the plan before the waypoint-type
dispatch, so every terminal waypoint type completes the flight instead.
"""

from __future__ import annotations

from datetime import timedelta
from types import SimpleNamespace
from typing import cast

import pytest

from game.ato.flightstate.completed import Completed
from game.ato.flightstate.inflight import InFlight
from game.ato.flightwaypointtype import FlightWaypointType


def _next_state(
    waypoint_index: int,
    waypoint_count: int,
    next_type: FlightWaypointType = FlightWaypointType.NAV,
) -> object:
    """Run InFlight.next_waypoint_state() against a minimal fake, bypassing
    __init__. ``next_type`` selects the routing branch under test."""
    waypoints = [SimpleNamespace(waypoint_type=FlightWaypointType.NAV)] * waypoint_count
    flight_plan = SimpleNamespace(
        waypoints=waypoints,
        travel_time_between_waypoints=lambda a, b: timedelta(),
    )
    fake = SimpleNamespace(
        waypoint_index=waypoint_index,
        next_waypoint=SimpleNamespace(waypoint_type=next_type),
        flight=SimpleNamespace(flight_plan=flight_plan),
        settings=SimpleNamespace(),
    )
    return InFlight.next_waypoint_state(cast(InFlight, fake))


def test_advancing_past_final_nav_waypoint_completes_flight() -> None:
    # waypoint_index 1 -> new_index 2 is the last index of a 3-waypoint plan, so
    # there is no waypoint after it: complete instead of raising.
    assert isinstance(_next_state(waypoint_index=1, waypoint_count=3), Completed)


@pytest.mark.parametrize(
    "terminal_type",
    [FlightWaypointType.PATROL_TRACK, FlightWaypointType.LOITER],
)
def test_terminal_patrol_or_loiter_completes_instead_of_crashing(
    terminal_type: FlightWaypointType,
) -> None:
    # A plan whose final waypoint is a PATROL_TRACK/LOITER must not try to build a
    # RaceTrack/Loiter for the last index (which would raise in InFlight.__init__).
    # The end-of-plan guard runs before the type dispatch and completes it.
    assert isinstance(
        _next_state(waypoint_index=1, waypoint_count=3, next_type=terminal_type),
        Completed,
    )


def test_advancing_with_remaining_waypoints_keeps_navigating() -> None:
    # new_index 1 still has a waypoint after it, so the flight keeps navigating
    # rather than completing early.
    assert not isinstance(_next_state(waypoint_index=0, waypoint_count=3), Completed)
