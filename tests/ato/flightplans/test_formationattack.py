from __future__ import annotations

from types import SimpleNamespace
from typing import Any, cast

import pytest
from dcs import Point
from dcs.terrain import Caucasus, Terrain

from game.ato.flight import Flight
from game.ato.flightplans.bai import BaiFlightPlan
from game.ato.flightplans.formationattack import (
    FormationAttackFlightPlan,
    FormationAttackLayout,
)
from game.ato.flightplans.strike import StrikeFlightPlan
from game.ato.flighttype import FlightType
from game.data.groups import GroupTask
from game.theater.controlpoint import ControlPoint
from game.theater.presetlocation import PresetLocation
from game.theater.theatergroundobject import MotorpoolGroundObject
from game.utils import Heading
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


def test_empty_motorpool_strike_uses_target_area_waypoint(monkeypatch: Any) -> None:
    terrain = Caucasus()
    control_point = cast(ControlPoint, SimpleNamespace())
    target = MotorpoolGroundObject(
        "Motorpool",
        PresetLocation("Garage", Point(0, 0, terrain), Heading.from_degrees(0)),
        control_point,
        GroupTask.MOTORPOOL,
    )
    package = cast(
        Package,
        SimpleNamespace(
            target=target,
            waypoints=SimpleNamespace(
                join=FlightWaypoint(
                    "JOIN", FlightWaypointType.JOIN, Point(0, 0, terrain)
                ),
                ingress=FlightWaypoint(
                    "INGRESS", FlightWaypointType.INGRESS_STRIKE, Point(0, 0, terrain)
                ),
                split=Point(0, 0, terrain),
            ),
        ),
    )
    flight = cast(
        Flight,
        SimpleNamespace(
            package=package,
            flight_type=FlightType.STRIKE,
            is_helo=False,
            departure=SimpleNamespace(position=Point(0, 0, terrain)),
            arrival=SimpleNamespace(position=Point(0, 0, terrain)),
            divert=None,
        ),
    )
    builder = cast(Any, object.__new__(StrikeFlightPlan.builder_type()))
    builder.flight = flight
    builder._hold_point = lambda: Point(0, 0, terrain)
    builder._get_split = lambda: Point(0, 0, terrain)
    builder._build_refuel = lambda _builder: None

    class FakeWaypointBuilder:
        get_combat_altitude = cast(Any, None)

        def __init__(self, _flight: Flight, _targets: object) -> None:
            pass

        def __getattr__(self, _name: str) -> Any:
            return lambda *_args: FlightWaypoint(
                "TARGET AREA", FlightWaypointType.TARGET_GROUP_LOC, target.position
            )

    monkeypatch.setattr(
        "game.ato.flightplans.formationattack.WaypointBuilder", FakeWaypointBuilder
    )

    layout = builder.layout()
    plan = StrikeFlightPlan.__new__(StrikeFlightPlan)
    plan.flight = flight
    plan.layout = layout

    assert len(layout.targets) == 1
    assert plan.tot_waypoint is layout.targets[0]


def test_motorpool_bai_with_live_groups_uses_per_target_waypoints(
    monkeypatch: Any,
) -> None:
    terrain = Caucasus()
    control_point = cast(ControlPoint, SimpleNamespace())
    target = MotorpoolGroundObject(
        "Motorpool",
        PresetLocation("Garage", Point(0, 0, terrain), Heading.from_degrees(0)),
        control_point,
        GroupTask.MOTORPOOL,
    )
    group = cast(Any, SimpleNamespace(units=[object()], group_name="Armor"))
    target.groups = [group]
    package = cast(
        Package,
        SimpleNamespace(
            target=target,
            waypoints=SimpleNamespace(
                join=FlightWaypoint(
                    "JOIN", FlightWaypointType.JOIN, Point(0, 0, terrain)
                ),
                ingress=FlightWaypoint(
                    "INGRESS", FlightWaypointType.INGRESS_BAI, Point(0, 0, terrain)
                ),
                split=Point(0, 0, terrain),
            ),
        ),
    )
    flight = cast(
        Flight,
        SimpleNamespace(
            package=package,
            flight_type=FlightType.BAI,
            is_helo=False,
            departure=SimpleNamespace(position=Point(0, 0, terrain)),
            arrival=SimpleNamespace(position=Point(0, 0, terrain)),
            divert=None,
        ),
    )
    builder = cast(Any, object.__new__(BaiFlightPlan.builder_type()))
    builder.flight = flight
    builder._hold_point = lambda: Point(0, 0, terrain)
    builder._get_split = lambda: Point(0, 0, terrain)
    builder._build_refuel = lambda _builder: None

    class FakeWaypointBuilder:
        get_combat_altitude = cast(Any, None)

        def __init__(self, _flight: Flight, _targets: object) -> None:
            pass

        def bai_group(self, target: object) -> FlightWaypoint:
            return FlightWaypoint(
                "BAI GROUP", FlightWaypointType.TARGET_GROUP_LOC, Point(1, 1, terrain)
            )

        def strike_area(self, _target: object) -> FlightWaypoint:
            return FlightWaypoint(
                "STRIKE AREA", FlightWaypointType.TARGET_GROUP_LOC, Point(2, 2, terrain)
            )

        def __getattr__(self, _name: str) -> Any:
            return lambda *_args: FlightWaypoint(
                "OTHER", FlightWaypointType.TARGET_GROUP_LOC, target.position
            )

    monkeypatch.setattr(
        "game.ato.flightplans.formationattack.WaypointBuilder", FakeWaypointBuilder
    )

    layout = builder.layout()

    assert len(layout.targets) == 1
    assert layout.targets[0].name == "BAI GROUP"
