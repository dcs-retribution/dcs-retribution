from datetime import datetime, timedelta
from types import SimpleNamespace

from dcs import Point
from dcs.terrain import Caucasus

from game.ato.flightplans.patrolling import PatrollingFlightPlan, PatrollingLayout
from game.ato.flightwaypoint import FlightWaypoint
from game.ato.flightwaypointtype import FlightWaypointType
from game.utils import Distance, Speed, kph, nautical_miles

T0 = datetime(2020, 1, 1, 12, 0, 0)


def _wp(name: str, kind: FlightWaypointType = FlightWaypointType.NAV) -> FlightWaypoint:
    return FlightWaypoint(name, kind, Point(0, 0, Caucasus()))


class _FixedPatrolPlan(PatrollingFlightPlan[PatrollingLayout]):
    """Patrol plan with constant 2-minute travel legs for deterministic tests."""

    @property
    def patrol_duration(self) -> timedelta:
        return timedelta(minutes=30)

    @property
    def patrol_speed(self) -> Speed:
        return kph(400)

    @property
    def engagement_distance(self) -> Distance:
        return nautical_miles(10)

    def travel_time_between_waypoints(
        self, a: FlightWaypoint, b: FlightWaypoint
    ) -> timedelta:
        return timedelta(minutes=2)


def _make_patrol_plan() -> _FixedPatrolPlan:
    layout = PatrollingLayout(
        departure=_wp("dep", FlightWaypointType.TAKEOFF),
        custom_waypoints=[],
        arrival=_wp("arr", FlightWaypointType.LANDING_POINT),
        divert=None,
        bullseye=_wp("bull", FlightWaypointType.BULLSEYE),
        nav_to=[],
        nav_from=[],
        patrol_start=_wp("ps", FlightWaypointType.PATROL_TRACK),
        patrol_end=_wp("pe", FlightWaypointType.PATROL),
    )
    flight = SimpleNamespace(package=SimpleNamespace(time_over_target=T0))
    return _FixedPatrolPlan(flight, layout)  # type: ignore[arg-type]


def test_patrol_leg_carries_on_station_time() -> None:
    plan = _make_patrol_plan()
    ps = plan.layout.patrol_start
    pe = plan.layout.patrol_end
    # The on-station leg is patrol_duration (30 min), not the 2-minute travel stub. This
    # is what makes patrol_end_time = patrol_start_time + patrol_duration hold when the
    # schedule is chained leg-by-leg (manual ToT cascade, kneeboard ETAs).
    assert plan.total_time_between_waypoints(ps, pe) == timedelta(minutes=30)


def test_non_patrol_legs_are_travel_only() -> None:
    plan = _make_patrol_plan()
    ps = plan.layout.patrol_start
    pe = plan.layout.patrol_end
    # Only the patrol_start -> patrol_end orbit carries the loiter; every other leg
    # (including the reverse direction) stays at travel time.
    assert plan.total_time_between_waypoints(plan.layout.departure, ps) == timedelta(
        minutes=2
    )
    assert plan.total_time_between_waypoints(pe, plan.layout.arrival) == timedelta(
        minutes=2
    )
    assert plan.total_time_between_waypoints(pe, ps) == timedelta(minutes=2)
