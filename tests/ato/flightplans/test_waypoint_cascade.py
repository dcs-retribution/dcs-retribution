import pickle
from datetime import datetime, timedelta
from types import SimpleNamespace

from dcs import Point
from dcs.terrain import Caucasus

from game.ato.flightplans.custom import CustomFlightPlan, CustomLayout
from game.ato.flightplans.flightplan import cascade_waypoint_times
from game.ato.flightwaypoint import FlightWaypoint
from game.ato.flightwaypointtype import FlightWaypointType
from game.ato.traveltime import TotEstimator

T0 = datetime(2020, 1, 1, 12, 0, 0)


def _legs(*minutes: int) -> list[timedelta]:
    return [timedelta(minutes=m) for m in minutes]


def test_no_offsets_is_takeoff_plus_prefix_legs() -> None:
    times = cascade_waypoint_times(
        T0, _legs(10, 5), [timedelta(), timedelta(), timedelta()]
    )
    assert times == [T0, T0 + timedelta(minutes=10), T0 + timedelta(minutes=15)]


def test_offset_shifts_that_waypoint_and_all_after() -> None:
    offsets = [timedelta(), timedelta(minutes=3), timedelta()]
    times = cascade_waypoint_times(T0, _legs(10, 5), offsets)
    assert times[0] == T0
    assert times[1] == T0 + timedelta(minutes=13)
    assert times[2] == T0 + timedelta(minutes=18)


def test_negative_offset_pulls_earlier() -> None:
    offsets = [timedelta(), timedelta(), timedelta(minutes=-2)]
    times = cascade_waypoint_times(T0, _legs(10, 5), offsets)
    assert times[2] == T0 + timedelta(minutes=13)


def test_stacked_offsets_accumulate() -> None:
    offsets = [timedelta(), timedelta(minutes=3), timedelta(minutes=2)]
    times = cascade_waypoint_times(T0, _legs(10, 5), offsets)
    assert times[1] == T0 + timedelta(minutes=13)
    assert times[2] == T0 + timedelta(minutes=20)


def test_manual_tot_offset_defaults_to_zero() -> None:
    wp = FlightWaypoint("", FlightWaypointType.NAV, Point(0, 0, Caucasus()))
    assert wp.manual_tot_offset == timedelta()


def test_manual_tot_offset_survives_pickle() -> None:
    wp = FlightWaypoint("", FlightWaypointType.NAV, Point(0, 0, Caucasus()))
    wp.manual_tot_offset = timedelta(minutes=4)
    restored = pickle.loads(pickle.dumps(wp))
    assert restored.manual_tot_offset == timedelta(minutes=4)


def test_old_save_without_field_loads_zero() -> None:
    wp = FlightWaypoint("", FlightWaypointType.NAV, Point(0, 0, Caucasus()))
    state = wp.__dict__.copy()
    del state["manual_tot_offset"]
    restored = FlightWaypoint.__new__(FlightWaypoint)
    restored.__setstate__(state)
    assert restored.manual_tot_offset == timedelta()


class _FixedTimePlan(CustomFlightPlan):
    """CustomFlightPlan with constant 10-minute legs for deterministic tests."""

    def total_time_between_waypoints(
        self, a: FlightWaypoint, b: FlightWaypoint
    ) -> timedelta:
        return timedelta(minutes=10)


def _make_plan(n: int) -> _FixedTimePlan:
    terrain = Caucasus()
    departure = FlightWaypoint("dep", FlightWaypointType.TAKEOFF, Point(0, 0, terrain))
    customs = [
        FlightWaypoint(f"w{i}", FlightWaypointType.NAV, Point(0, i, terrain))
        for i in range(1, n)
    ]
    layout = CustomLayout(departure, customs)
    flight = SimpleNamespace(
        manually_timed=True,
        manual_takeoff_time=T0,
        package=SimpleNamespace(time_over_target=T0),
    )
    plan = _FixedTimePlan(flight, layout)  # type: ignore[arg-type]
    return plan


def test_manual_waypoint_times_chain() -> None:
    plan = _make_plan(3)
    times = plan.manual_waypoint_times()
    assert times == [T0, T0 + timedelta(minutes=10), T0 + timedelta(minutes=20)]


def test_set_waypoint_tot_cascades_forward() -> None:
    plan = _make_plan(3)
    wps = plan.waypoints
    plan.set_waypoint_tot(wps[1], T0 + timedelta(minutes=15))  # +5 on wp1
    times = plan.manual_waypoint_times()
    assert times[0] == T0
    assert times[1] == T0 + timedelta(minutes=15)
    assert times[2] == T0 + timedelta(minutes=25)


def test_effective_tot_indexes_correct_waypoint() -> None:
    plan = _make_plan(3)
    wps = plan.waypoints
    plan.set_waypoint_tot(wps[2], T0 + timedelta(minutes=30))
    assert plan.effective_tot_for_waypoint(wps[2]) == T0 + timedelta(minutes=30)
    assert plan.effective_tot_for_waypoint(wps[1]) == T0 + timedelta(minutes=10)


def test_clear_manual_timing_resets() -> None:
    plan = _make_plan(3)
    wps = plan.waypoints
    plan.set_waypoint_tot(wps[1], T0 + timedelta(minutes=15))
    plan.clear_manual_timing()
    assert plan.flight.manually_timed is False
    assert plan.flight.manual_takeoff_time is None
    assert all(wp.manual_tot_offset == timedelta() for wp in plan.waypoints)


class _FractionalLegPlan(CustomFlightPlan):
    """CustomFlightPlan whose legs carry sub-second remainders."""

    def total_time_between_waypoints(
        self, a: FlightWaypoint, b: FlightWaypoint
    ) -> timedelta:
        return timedelta(seconds=125, microseconds=900000)


def test_manual_waypoint_times_floored_to_whole_seconds() -> None:
    terrain = Caucasus()
    departure = FlightWaypoint("dep", FlightWaypointType.TAKEOFF, Point(0, 0, terrain))
    customs = [
        FlightWaypoint(f"w{i}", FlightWaypointType.NAV, Point(0, i, terrain))
        for i in range(1, 3)
    ]
    flight = SimpleNamespace(
        manually_timed=True,
        manual_takeoff_time=T0,
        package=SimpleNamespace(time_over_target=T0),
    )
    plan = _FractionalLegPlan(flight, CustomLayout(departure, customs))  # type: ignore[arg-type]
    times = plan.manual_waypoint_times()
    assert all(t.microsecond == 0 for t in times)
    # Each leg floors 125.9s -> 125s before chaining.
    assert times == [T0, T0 + timedelta(seconds=125), T0 + timedelta(seconds=250)]


def test_move_waypoint_resets_manual_timing() -> None:
    plan = _make_plan(3)
    wps = plan.waypoints
    plan.set_waypoint_tot(wps[1], T0 + timedelta(minutes=15))
    was_manual = plan.flight.manually_timed
    moved = plan.move_waypoint(wps[2], -1)
    assert was_manual
    assert moved is True
    assert not plan.flight.manually_timed
    assert plan.flight.manual_takeoff_time is None
    assert all(wp.manual_tot_offset == timedelta() for wp in plan.waypoints)


def test_move_waypoint_failure_keeps_manual_timing() -> None:
    plan = _make_plan(3)
    wps = plan.waypoints
    plan.set_waypoint_tot(wps[1], T0 + timedelta(minutes=15))
    # The departure waypoint is not reorderable; a failed move must not reset timing.
    assert plan.move_waypoint(wps[0], -1) is False
    assert plan.flight.manually_timed


def test_custom_tot_waypoint_finds_target() -> None:
    terrain = Caucasus()
    departure = FlightWaypoint("dep", FlightWaypointType.TAKEOFF, Point(0, 0, terrain))
    nav = FlightWaypoint("nav", FlightWaypointType.NAV, Point(0, 1, terrain))
    target = FlightWaypoint(
        "tgt", FlightWaypointType.TARGET_POINT, Point(0, 2, terrain)
    )
    flight = SimpleNamespace(
        manually_timed=False,
        manual_takeoff_time=None,
        package=SimpleNamespace(time_over_target=T0),
    )
    plan = _FixedTimePlan(flight, CustomLayout(departure, [nav, target]))  # type: ignore[arg-type]
    assert plan.tot_waypoint is target


def test_custom_tot_waypoint_finds_cas_flot() -> None:
    # A CAS flight degraded to a custom plan anchors its ToT on the FLOT (CAS-type)
    # waypoint. Without CAS in the recognized types the anchor fell back to the
    # departure, collapsing the takeoff time onto the package TOT.
    terrain = Caucasus()
    departure = FlightWaypoint("dep", FlightWaypointType.TAKEOFF, Point(0, 0, terrain))
    nav = FlightWaypoint("nav", FlightWaypointType.NAV, Point(0, 1, terrain))
    flot = FlightWaypoint("FLOT START", FlightWaypointType.CAS, Point(0, 2, terrain))
    flight = SimpleNamespace(
        manually_timed=False,
        manual_takeoff_time=None,
        package=SimpleNamespace(time_over_target=T0),
    )
    plan = _FixedTimePlan(flight, CustomLayout(departure, [nav, flot]))  # type: ignore[arg-type]
    assert plan.tot_waypoint is flot


def test_earliest_tot_skips_manually_timed_flights() -> None:
    auto = SimpleNamespace(manually_timed=False)
    manual = SimpleNamespace(manually_timed=True)
    package = SimpleNamespace(flights=[auto, manual])
    estimator = TotEstimator(package)  # type: ignore[arg-type]

    seen = []

    def fake_for_flight(flight: object, now: datetime) -> datetime:
        seen.append(flight)
        return now

    estimator.earliest_tot_for_flight = fake_for_flight  # type: ignore[method-assign]
    estimator.earliest_tot(T0)
    assert manual not in seen
    assert auto in seen


def _make_auto_plan(n: int) -> _FixedTimePlan:
    terrain = Caucasus()
    departure = FlightWaypoint("dep", FlightWaypointType.TAKEOFF, Point(0, 0, terrain))
    customs = [
        FlightWaypoint(f"w{i}", FlightWaypointType.NAV, Point(0, i, terrain))
        for i in range(1, n)
    ]
    flight = SimpleNamespace(
        manually_timed=False,
        manual_takeoff_time=None,
        package=SimpleNamespace(time_over_target=T0),
    )
    return _FixedTimePlan(flight, CustomLayout(departure, customs))  # type: ignore[arg-type]


def test_chained_tot_auto_chains_from_takeoff() -> None:
    plan = _make_auto_plan(3)
    wps = plan.waypoints
    assert plan.chained_tot_for_waypoint(wps[0]) == plan.takeoff_time()
    assert plan.chained_tot_for_waypoint(wps[2]) == plan.takeoff_time() + timedelta(
        minutes=20
    )


def test_chained_tot_manual_matches_cascade() -> None:
    plan = _make_plan(3)
    wps = plan.waypoints
    plan.set_waypoint_tot(wps[1], T0 + timedelta(minutes=15))
    assert plan.chained_tot_for_waypoint(wps[2]) == plan.manual_waypoint_times()[2]


def test_would_invert_order_rejects_at_or_before_previous() -> None:
    plan = _make_auto_plan(3)
    wps = plan.waypoints
    prev = plan.chained_tot_for_waypoint(wps[1])
    assert prev is not None
    assert plan.would_invert_order(wps[2], prev - timedelta(minutes=1)) is True
    assert plan.would_invert_order(wps[2], prev) is True
    assert plan.would_invert_order(wps[2], prev + timedelta(minutes=1)) is False


def test_would_invert_order_first_waypoint_never_inverts() -> None:
    plan = _make_auto_plan(3)
    wps = plan.waypoints
    assert plan.would_invert_order(wps[0], T0 - timedelta(hours=1)) is False
