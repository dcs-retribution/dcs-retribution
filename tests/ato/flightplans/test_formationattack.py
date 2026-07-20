from __future__ import annotations

from typing import cast

import pytest
from dcs import Point
from dcs.terrain import Caucasus, Terrain

from game.ato.flight import Flight
from game.ato.flightplans.formationattack import FormationAttackFlightPlan
from game.ato.flightwaypoint import FlightWaypoint
from game.ato.flightwaypointtype import FlightWaypointType
from game.ato.package import Package
from game.utils import Speed, knots


class _StubPackage:
    def __init__(self, formation_speed: Speed | None) -> None:
        self._formation_speed = formation_speed

    def formation_speed(self, is_helo: bool) -> Speed | None:
        return self._formation_speed


class _StubFlight:
    def __init__(self, package: Package) -> None:
        self.package = package
        self.is_helo = False


class _FormationAttackUnderTest(FormationAttackFlightPlan):
    """Minimal concrete flight plan exercising ``speed_between_waypoints``.

    The real collaborators (package, flight, formation speed) are stubbed so the
    test focuses on how the target-area segment is priced.
    """

    def __init__(self, formation_speed: Speed | None, fallback_speed: Speed) -> None:
        package = cast(Package, _StubPackage(formation_speed))
        self.flight = cast(Flight, _StubFlight(package))
        self._fallback_speed = fallback_speed

    @property
    def best_flight_formation_speed(self) -> Speed:
        return self._fallback_speed


@pytest.fixture(name="target_waypoint")
def target_waypoint_fixture() -> FlightWaypoint:
    terrain: Terrain = Caucasus()
    return FlightWaypoint(
        "TARGET AREA",
        FlightWaypointType.TARGET_GROUP_LOC,
        Point(0, 0, terrain),
    )


def test_uses_package_formation_speed_at_target_when_available(
    target_waypoint: FlightWaypoint,
) -> None:
    formation_speed = knots(400)
    plan = _FormationAttackUnderTest(formation_speed, fallback_speed=knots(250))

    speed = plan.speed_between_waypoints(target_waypoint, target_waypoint)

    assert speed == formation_speed


def test_falls_back_to_flight_speed_when_package_has_no_formation_speed(
    target_waypoint: FlightWaypoint,
) -> None:
    fallback_speed = knots(250)
    plan = _FormationAttackUnderTest(
        formation_speed=None, fallback_speed=fallback_speed
    )

    speed = plan.speed_between_waypoints(target_waypoint, target_waypoint)

    assert speed == fallback_speed
