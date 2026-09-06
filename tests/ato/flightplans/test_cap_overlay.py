from datetime import datetime, timedelta
from types import SimpleNamespace

from dcs import Point
from dcs.terrain import Caucasus

from game.ato.flightplans.patrolling import PatrollingFlightPlan, PatrollingLayout
from game.ato.flightplans.tacticaloverlay import cap_overlay
from game.ato.flightwaypoint import FlightWaypoint
from game.ato.flightwaypointtype import FlightWaypointType
from game.utils import Distance, Speed, kph, nautical_miles


def _wp(name: str, x: float, y: float, kind: FlightWaypointType) -> FlightWaypoint:
    return FlightWaypoint(name, kind, Point(x, y, Caucasus()))


class _Cap(PatrollingFlightPlan[PatrollingLayout]):
    @property
    def patrol_duration(self) -> timedelta:
        return timedelta(minutes=30)

    @property
    def patrol_speed(self) -> Speed:
        return kph(700)

    @property
    def engagement_distance(self) -> Distance:
        return nautical_miles(35)


def _plan() -> _Cap:
    layout = PatrollingLayout(
        departure=_wp("dep", 0, 0, FlightWaypointType.TAKEOFF),
        custom_waypoints=[],
        arrival=_wp("arr", 0, 0, FlightWaypointType.LANDING_POINT),
        divert=None,
        bullseye=_wp("bull", 0, 0, FlightWaypointType.BULLSEYE),
        nav_to=[],
        nav_from=[],
        patrol_start=_wp("ps", 0, 0, FlightWaypointType.PATROL_TRACK),
        patrol_end=_wp("pe", 100000, 0, FlightWaypointType.PATROL),
    )
    flight = SimpleNamespace(
        package=SimpleNamespace(time_over_target=datetime(2020, 1, 1))
    )
    return _Cap(flight, layout)  # type: ignore[arg-type]


def test_cap_overlay_shapes() -> None:
    overlay = cap_overlay(_plan())
    filled = [r for r in overlay.reach if r.filled]
    outline = [r for r in overlay.reach if not r.filled]
    assert len(filled) == 1 and len(outline) == 1
    fminx, _, fmaxx, _ = filled[0].geometry.bounds
    assert (fminx + fmaxx) / 2 > 90000
    assert overlay.actual_path is not None
    assert overlay.actual_path[0].x == overlay.actual_path[-1].x
    assert overlay.targets == []
