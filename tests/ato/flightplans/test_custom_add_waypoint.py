from dcs import Point
from dcs.terrain import Caucasus

from game.ato.flightplans.custom import CustomLayout
from game.ato.flightwaypoint import FlightWaypoint
from game.ato.flightwaypointtype import FlightWaypointType


def _wp(name: str, kind: FlightWaypointType = FlightWaypointType.NAV) -> FlightWaypoint:
    return FlightWaypoint(name, kind, Point(0, 0, Caucasus()))


def test_add_waypoint_after_custom_inserts_after_selection() -> None:
    a, b = _wp("a"), _wp("b")
    layout = CustomLayout(_wp("dep", FlightWaypointType.TAKEOFF), [a, b])
    assert layout.add_waypoint(a, b) is True
    assert len(layout.custom_waypoints) == 3
    assert layout.custom_waypoints[0] is a
    assert layout.custom_waypoints[1].waypoint_type is FlightWaypointType.NAV
    assert layout.custom_waypoints[2] is b


def test_add_waypoint_after_departure_inserts_front() -> None:
    a = _wp("a")
    dep = _wp("dep", FlightWaypointType.TAKEOFF)
    layout = CustomLayout(dep, [a])
    assert layout.add_waypoint(dep, a) is True
    assert layout.custom_waypoints[0].waypoint_type is FlightWaypointType.NAV
    assert layout.custom_waypoints[1] is a


def test_add_waypoint_after_last_custom_appends() -> None:
    a = _wp("a")
    layout = CustomLayout(_wp("dep", FlightWaypointType.TAKEOFF), [a])
    assert layout.add_waypoint(a, None) is True
    assert len(layout.custom_waypoints) == 2
    assert layout.custom_waypoints[1].waypoint_type is FlightWaypointType.NAV


def test_add_waypoint_unknown_selection_returns_false() -> None:
    layout = CustomLayout(_wp("dep", FlightWaypointType.TAKEOFF), [_wp("a")])
    assert layout.add_waypoint(_wp("ghost"), None) is False
