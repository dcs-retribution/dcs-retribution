"""Regression coverage for air-assault return-leg fuel restoration.

Air assault flight plans emit a JOIN waypoint but never a SPLIT, so under the
phase-based AI fuel policy their AI flights consume real fuel from the
objective onward and never regain unlimited fuel for the return leg. The
restoration must sit on the executed objective-completion boundaries: the
helicopter drop-off landing and the Hercules assault area waypoint (the
helicopter assault area is player-only, so all-AI helicopter flights never
receive it).
"""

from types import SimpleNamespace
from typing import Any, cast
from unittest.mock import MagicMock, patch

import pytest
from dcs import Point
from dcs.point import MovingPoint
from dcs.terrain import Caucasus, Terrain
from dcs.task import Land, RunScript, SetUnlimitedFuelCommand

from game.ato import FlightType
from game.ato.flightplans.airassault import AirAssaultLayout
from game.ato.flightplans.waypointbuilder import WaypointBuilder
from game.ato.flightwaypoint import FlightWaypoint
from game.ato.flightwaypointtype import FlightWaypointType
from game.missiongenerator.aircraft.waypoints.landingzone import LandingZoneBuilder
from game.missiongenerator.aircraft.waypoints.pydcswaypointbuilder import (
    PydcsWaypointBuilder,
)
from game.missiongenerator.aircraft.waypoints.target import TargetBuilder
from game.theater import MissionTarget


def _flight(flight_type: FlightType, ai_unlimited_fuel: bool) -> SimpleNamespace:
    # is_player=True makes PydcsWaypointBuilder.ai_despawn a no-op so tests
    # observe exactly the tasks the builders under test append. The settings
    # object is shared: LandingZoneBuilder reads use_ai_combat_landing through
    # flight.coalition while the fuel gates read ai_unlimited_fuel through
    # flight.squadron.coalition.
    settings = SimpleNamespace(
        ai_unlimited_fuel=ai_unlimited_fuel,
        use_ai_combat_landing=False,
    )
    game = SimpleNamespace(settings=settings)
    return SimpleNamespace(
        flight_type=flight_type,
        roster=SimpleNamespace(members=[SimpleNamespace(is_player=True)]),
        coalition=SimpleNamespace(game=game),
        squadron=SimpleNamespace(coalition=SimpleNamespace(game=game)),
    )


def _landing_zone_builder(flight: SimpleNamespace) -> LandingZoneBuilder:
    builder = LandingZoneBuilder.__new__(LandingZoneBuilder)
    builder.flight = cast(Any, flight)
    return builder


def _target_builder(flight: SimpleNamespace) -> TargetBuilder:
    builder = TargetBuilder.__new__(TargetBuilder)
    builder.flight = cast(Any, flight)
    return builder


def _assert_restored_unlimited_fuel(waypoint: MagicMock) -> None:
    waypoint.tasks.append.assert_called_once()
    (task,) = waypoint.tasks.append.call_args[0]
    assert isinstance(task, SetUnlimitedFuelCommand)
    assert task.params["action"]["params"]["value"] is True


def test_drop_off_restores_unlimited_fuel_for_air_assault_when_enabled() -> None:
    builder = _landing_zone_builder(_flight(FlightType.AIR_ASSAULT, True))
    waypoint = MagicMock()

    builder._restore_unlimited_fuel_for_return_leg(waypoint)

    _assert_restored_unlimited_fuel(waypoint)


def test_drop_off_keeps_finite_fuel_when_option_disabled() -> None:
    builder = _landing_zone_builder(_flight(FlightType.AIR_ASSAULT, False))
    waypoint = MagicMock()

    builder._restore_unlimited_fuel_for_return_leg(waypoint)

    waypoint.tasks.append.assert_not_called()


def test_drop_off_leaves_transport_airlift_flights_alone() -> None:
    # Airlift shares the LandingZone builder and the DROPOFFZONE waypoint, but
    # only air assault plans omit SPLIT.
    builder = _landing_zone_builder(_flight(FlightType.TRANSPORT, True))
    waypoint = MagicMock()

    builder._restore_unlimited_fuel_for_return_leg(waypoint)

    waypoint.tasks.append.assert_not_called()


def test_drop_off_leaves_escort_flights_alone() -> None:
    # Escorts of air-assault packages release via the split user flag; their
    # return-leg fuel policy is not this fix's concern.
    builder = _landing_zone_builder(_flight(FlightType.ESCORT, True))
    waypoint = MagicMock()

    builder._restore_unlimited_fuel_for_return_leg(waypoint)

    waypoint.tasks.append.assert_not_called()


def _build_landing_zone_waypoint(
    flight_type: FlightType,
    ai_unlimited_fuel: bool,
    waypoint_name: str,
) -> tuple[MovingPoint, object]:
    """Runs the real LandingZoneBuilder.build against a real MovingPoint.

    Only the base waypoint construction is mocked (PydcsWaypointBuilder.build,
    which needs a full FlyingGroup to add the MovingPoint to); every task
    LandingZoneBuilder appends is produced and inspected for real, including
    its serialized params.
    """
    builder = _landing_zone_builder(_flight(flight_type, ai_unlimited_fuel))
    builder.package = cast(Any, object())
    builder.waypoint = _waypoint(
        waypoint_name,
        (
            FlightWaypointType.PICKUP_ZONE
            if waypoint_name == "PICKUPZONE"
            else FlightWaypointType.DROPOFF_ZONE
        ),
    )
    built = MovingPoint(Point(0, 0, Caucasus()))
    built.name = waypoint_name
    with patch.object(PydcsWaypointBuilder, "build", return_value=built):
        return builder.build(), builder.package


@pytest.mark.parametrize(
    ("flight_type", "ai_unlimited_fuel", "waypoint_name", "expects_fuel_command"),
    [
        (FlightType.AIR_ASSAULT, True, "DROPOFFZONE", True),
        (FlightType.AIR_ASSAULT, False, "DROPOFFZONE", False),
        (FlightType.TRANSPORT, True, "DROPOFFZONE", False),
        (FlightType.AIR_ASSAULT, True, "PICKUPZONE", False),
    ],
    ids=[
        "air-assault-enabled-restores-return-fuel",
        "air-assault-disabled-keeps-finite-fuel",
        "transport-airlift-excluded",
        "pickup-zone-is-not-a-return-boundary",
    ],
)
def test_landing_zone_build_task_list(
    flight_type: FlightType,
    ai_unlimited_fuel: bool,
    waypoint_name: str,
    expects_fuel_command: bool,
) -> None:
    built, package = _build_landing_zone_waypoint(
        flight_type,
        ai_unlimited_fuel,
        waypoint_name,
    )
    tasks = built.tasks

    # The landing point stays within the 30 m buffer around the LZ.
    landing = tasks[0]
    assert isinstance(landing, Land)
    assert landing.params["duration"] == 30
    assert landing.params["durationFlag"] is True
    assert landing.params["combatLandingFlag"] is False
    assert abs(landing.params["x"]) <= 30
    assert abs(landing.params["y"]) <= 30

    expected: list[type[Any]] = [Land]
    if waypoint_name == "DROPOFFZONE":
        expected.append(RunScript)
        if expects_fuel_command:
            expected.append(SetUnlimitedFuelCommand)
    assert [type(task) for task in tasks] == expected
    if waypoint_name != "DROPOFFZONE":
        # Pickup zones open the objective: no release signal, no fuel restore.
        return

    release = tasks[1]
    assert isinstance(release, RunScript)
    assert release.params["action"]["id"] == "Script"
    assert release.params["action"]["params"]["command"] == (
        f'trigger.action.setUserFlag("split-{id(package)}", true)'
    )

    if expects_fuel_command:
        # Fuel is restored last: after the landing task and the package
        # release, never while the objective is still active.
        fuel = tasks[2]
        assert isinstance(fuel, SetUnlimitedFuelCommand)
        assert fuel.params["action"]["id"] == "SetUnlimitedFuel"
        assert fuel.params["action"]["params"]["value"] is True


def test_assault_area_restores_unlimited_fuel_for_air_assault_when_enabled() -> None:
    builder = _target_builder(_flight(FlightType.AIR_ASSAULT, True))
    waypoint = MagicMock()

    builder.add_tasks(waypoint)

    _assert_restored_unlimited_fuel(waypoint)


def test_assault_area_keeps_finite_fuel_when_option_disabled() -> None:
    builder = _target_builder(_flight(FlightType.AIR_ASSAULT, False))
    waypoint = MagicMock()

    builder.add_tasks(waypoint)

    waypoint.tasks.append.assert_not_called()


def test_assault_area_leaves_other_flight_types_alone() -> None:
    builder = _target_builder(_flight(FlightType.STRIKE, True))
    waypoint = MagicMock()

    builder.add_tasks(waypoint)

    waypoint.tasks.append.assert_not_called()


def _waypoint(name: str, waypoint_type: FlightWaypointType) -> FlightWaypoint:
    terrain: Terrain = Caucasus()
    return FlightWaypoint(name, waypoint_type, Point(0, 0, terrain))


def _layout(is_helo: bool) -> AirAssaultLayout:
    return AirAssaultLayout(
        departure=_waypoint("TAKEOFF", FlightWaypointType.TAKEOFF),
        pickup=_waypoint("PICKUPZONE", FlightWaypointType.PICKUP_ZONE),
        nav_to=[],
        join=_waypoint("JOIN", FlightWaypointType.JOIN),
        ingress=_waypoint("INGRESS", FlightWaypointType.INGRESS_AIR_ASSAULT),
        drop_off=(
            _waypoint("DROPOFFZONE", FlightWaypointType.DROPOFF_ZONE)
            if is_helo
            else None
        ),
        targets=[_waypoint("ASSAULT", FlightWaypointType.TARGET_GROUP_LOC)],
        nav_from=[],
        arrival=_waypoint("LANDING", FlightWaypointType.LANDING_POINT),
        divert=None,
        bullseye=_waypoint("BULLSEYE", FlightWaypointType.BULLSEYE),
        hold=None,
        split=_waypoint("SPLIT", FlightWaypointType.SPLIT),
        refuel=None,
        custom_waypoints=[],
    )


def test_helicopter_route_ends_objective_at_drop_off_without_split() -> None:
    # The executed helicopter route is ... JOIN, INGRESS, DROPOFFZONE, nav_from,
    # LANDING. The constructed SPLIT (at arrival) is never emitted, which is why
    # the drop-off is the only executed post-objective boundary.
    route = list(_layout(is_helo=True).iter_waypoints())
    names = [wp.name for wp in route]

    assert names.index("INGRESS") < names.index("DROPOFFZONE") < names.index("LANDING")
    assert all(wp.waypoint_type != FlightWaypointType.SPLIT for wp in route)


def test_hercules_route_ends_objective_at_assault_area_without_split() -> None:
    # Hercules air assaults have no drop-off waypoint; the assault area is
    # their AI-executed objective-completion boundary. SPLIT is likewise never
    # emitted.
    route = list(_layout(is_helo=False).iter_waypoints())
    names = [wp.name for wp in route]

    assert "DROPOFFZONE" not in names
    assert names.index("INGRESS") < names.index("ASSAULT") < names.index("LANDING")
    assert all(wp.waypoint_type != FlightWaypointType.SPLIT for wp in route)


def test_assault_area_waypoint_is_player_only_by_default() -> None:
    # All-AI helicopter flights therefore never receive the assault area at
    # all; their executed post-objective boundary is the drop-off landing.
    builder = WaypointBuilder.__new__(WaypointBuilder)
    target = cast(
        MissionTarget,
        SimpleNamespace(name="Some FOB", position=Point(0, 0, Caucasus())),
    )

    area = builder.assault_area(target)

    assert area.only_for_player is True
    assert area.waypoint_type is FlightWaypointType.TARGET_GROUP_LOC
