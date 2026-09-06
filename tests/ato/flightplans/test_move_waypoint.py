from collections.abc import Iterator

from dcs import Point
from dcs.terrain import Caucasus

from game.ato.flightwaypoint import FlightWaypoint
from game.ato.flightwaypointtype import FlightWaypointType
from game.ato.flightplans.standard import StandardLayout


def _wp(name: str, kind: FlightWaypointType = FlightWaypointType.NAV) -> FlightWaypoint:
    return FlightWaypoint(name, kind, Point(0, 0, Caucasus()))


def _standard_layout(
    nav_to: list[FlightWaypoint],
    nav_from: list[FlightWaypoint],
    custom: list[FlightWaypoint],
) -> StandardLayout:
    # StandardLayout is abstract (no iter_waypoints); build a minimal concrete subclass.
    class _L(StandardLayout):
        def iter_waypoints(self) -> Iterator[FlightWaypoint]:
            yield self.departure
            yield from self.nav_to
            yield from self.nav_from
            yield from self.custom_waypoints

    return _L(
        departure=_wp("dep", FlightWaypointType.TAKEOFF),
        custom_waypoints=custom,
        arrival=_wp("arr", FlightWaypointType.LANDING_POINT),
        divert=None,
        bullseye=_wp("bull", FlightWaypointType.BULLSEYE),
        nav_to=nav_to,
        nav_from=nav_from,
    )


def test_move_down_within_nav_to_swaps() -> None:
    a, b = _wp("a"), _wp("b")
    layout = _standard_layout([a, b], [], [])
    assert layout.move_waypoint(a, 1) is True
    assert layout.nav_to == [b, a]


def test_move_up_within_custom_swaps() -> None:
    a, b = _wp("a"), _wp("b")
    layout = _standard_layout([], [], [a, b])
    assert layout.move_waypoint(b, -1) is True
    assert layout.custom_waypoints == [b, a]


def test_move_off_end_of_list_returns_false() -> None:
    a = _wp("a")
    layout = _standard_layout([a], [], [])
    assert layout.move_waypoint(a, 1) is False  # would cross into nav_from / structural
    assert layout.nav_to == [a]


def test_move_unknown_waypoint_returns_false() -> None:
    layout = _standard_layout([_wp("a")], [], [])
    assert layout.move_waypoint(_wp("ghost"), 1) is False


def test_custom_layout_reorders_custom_waypoints() -> None:
    from game.ato.flightplans.custom import CustomLayout

    a, b, c = _wp("a"), _wp("b"), _wp("c")
    layout = CustomLayout(_wp("dep", FlightWaypointType.TAKEOFF), [a, b, c])
    assert layout.move_waypoint(c, -1) is True
    assert layout.custom_waypoints == [a, c, b]
    assert layout.move_waypoint(a, -1) is False  # already first
