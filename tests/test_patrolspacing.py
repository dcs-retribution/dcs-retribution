"""deconflicted_racetrack_center spreads same-type patrols laterally.

Multiple AWACS (or tankers) used to be placed on the exact same racetrack center,
stacking their orbits. The helper offsets each one along the front so a single
flight is unchanged (offset 0) and multiple flights fan out symmetrically.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any, cast

from game.ato.flightplans.patrolspacing import deconflicted_racetrack_center
from game.ato.flighttype import FlightType


class _Point:
    """Records the (heading_degrees, distance_m) it was offset by."""

    def point_from_heading(
        self, heading: float, distance: float
    ) -> tuple[float, float]:
        return (heading, distance)


def _heading() -> Any:
    return SimpleNamespace(
        right=SimpleNamespace(degrees=90.0),
        left=SimpleNamespace(degrees=270.0),
    )


def _coalition(*flights: Any) -> Any:
    return SimpleNamespace(
        ato=SimpleNamespace(packages=[SimpleNamespace(flights=list(flights))])
    )


def _flight(flight_id: str, flight_type: FlightType = FlightType.AEWC) -> Any:
    return SimpleNamespace(id=flight_id, flight_type=flight_type)


def _spacing(meters: float) -> Any:
    return SimpleNamespace(meters=meters)


def _center(base: Any, heading: Any, spacing: Any, flight: Any, coalition: Any) -> Any:
    return deconflicted_racetrack_center(
        cast(Any, base),
        cast(Any, heading),
        cast(Any, spacing),
        cast(Any, flight),
        cast(Any, coalition),
        FlightType.AEWC,
    )


def test_single_flight_is_not_offset() -> None:
    flight = _flight("a")
    result = _center(_Point(), _heading(), _spacing(1000.0), flight, _coalition(flight))
    # right.degrees with zero distance == no lateral shift.
    assert result == (90.0, 0.0)


def test_two_flights_fan_out_symmetrically() -> None:
    a, b = _flight("a"), _flight("b")
    coalition = _coalition(a, b)
    first = _center(_Point(), _heading(), _spacing(1000.0), a, coalition)
    second = _center(_Point(), _heading(), _spacing(1000.0), b, coalition)
    # Half a spacing each, in opposite directions (left for the first, right second).
    assert first == (270.0, 500.0)
    assert second == (90.0, 500.0)


def test_other_flight_types_are_ignored() -> None:
    awacs = _flight("a")
    tanker = _flight("b", FlightType.REFUELING)
    coalition = _coalition(awacs, tanker)
    # Only the single AWACS counts, so it is not offset by the tanker's presence.
    result = _center(_Point(), _heading(), _spacing(1000.0), awacs, coalition)
    assert result == (90.0, 0.0)
