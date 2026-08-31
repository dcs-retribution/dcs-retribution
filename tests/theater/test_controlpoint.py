import logging

import pytest
from typing import Any, cast
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from dcs import Point
from dcs.planes import AJS37
from dcs.terrain import Terrain
from dcs.terrain.terrain import Airport
from game.ato.flighttype import FlightType
from game.dcs.aircrafttype import AircraftType
from game.dcs.countries import country_with_name
from game.data.groups import GroupTask
from game.point_with_heading import PointWithHeading
from game.squadrons import Squadron
from game.squadrons.operatingbases import OperatingBases
from game.sim.gameupdateevents import GameUpdateEvents
from game.theater.controlpoint import (
    Airfield,
    Carrier,
    ControlPoint,
    ControlPointType,
    Lha,
    OffMapSpawn,
    Fob,
    ParkingType,
    Player,
    motorpools_inside_capture_zone,
    warn_if_motorpool_inside_capture_zone,
)
from game.theater.presetlocation import PresetLocation
from game.theater.theatergroundobject import MotorpoolGroundObject
from game.utils import Heading


@pytest.fixture
def test_mission_types_friendly(mocker: Any) -> None:
    """
    Test the mission types that can be planned against friendly control points
    """
    # Airfield
    mocker.patch("game.theater.controlpoint.Airfield.is_friendly", return_value=True)
    airport = Airport(None, None)  # type: ignore
    airport.name = "test"  # required for Airfield.__init__
    airfield = Airfield(airport, theater=None, starts_blue=Player.BLUE)  # type: ignore
    mission_types = list(airfield.mission_types(for_player=Player.BLUE))
    assert len(mission_types) == 3
    assert FlightType.AEWC in mission_types
    assert FlightType.REFUELING in mission_types
    assert FlightType.BARCAP in mission_types

    # Carrier
    mocker.patch("game.theater.controlpoint.Carrier.is_friendly", return_value=True)
    carrier = Carrier(name="test", at=None, theater=None, starts_blue=Player.BLUE)  # type: ignore
    mission_types = list(carrier.mission_types(for_player=Player.BLUE))
    assert len(mission_types) == 3
    assert FlightType.AEWC in mission_types
    assert FlightType.REFUELING in mission_types
    assert FlightType.BARCAP in mission_types

    # LHA
    mocker.patch("game.theater.controlpoint.Lha.is_friendly", return_value=True)
    lha = Lha(name="test", at=None, theater=None, starts_blue=Player.BLUE)  # type: ignore
    mission_types = list(lha.mission_types(for_player=Player.BLUE))
    assert len(mission_types) == 3
    assert FlightType.AEWC in mission_types
    assert FlightType.REFUELING in mission_types
    assert FlightType.BARCAP in mission_types

    # Fob
    mocker.patch("game.theater.controlpoint.Fob.is_friendly", return_value=True)
    fob = Fob(name="test", at=None, theater=None, starts_blue=Player.BLUE)  # type: ignore
    mission_types = list(fob.mission_types(for_player=Player.BLUE))
    assert len(mission_types) == 2
    assert FlightType.AEWC in mission_types
    assert FlightType.BARCAP in mission_types

    # Off map spawn
    mocker.patch("game.theater.controlpoint.OffMapSpawn.is_friendly", return_value=True)
    off_map_spawn = OffMapSpawn(name="test", position=None, theater=None, starts_blue=Player.BLUE)  # type: ignore
    mission_types = list(off_map_spawn.mission_types(for_player=Player.BLUE))
    assert len(mission_types) == 0


@pytest.fixture
def test_mission_types_enemy(mocker: Any) -> None:
    """
    Test the mission types that can be planned against enemy control points
    """
    # Airfield
    mocker.patch("game.theater.controlpoint.Airfield.is_friendly", return_value=False)
    airport = Airport(None, None)  # type: ignore
    airport.name = "test"  # required for Airfield.__init__
    airfield = Airfield(airport, theater=None, starts_blue=Player.BLUE)  # type: ignore
    mission_types = list(airfield.mission_types(for_player=Player.BLUE))
    assert len(mission_types) == 8
    assert FlightType.OCA_AIRCRAFT in mission_types
    assert FlightType.OCA_RUNWAY in mission_types
    assert FlightType.AIR_ASSAULT in mission_types
    assert FlightType.ESCORT in mission_types
    assert FlightType.TARCAP in mission_types
    assert FlightType.SEAD_ESCORT in mission_types
    assert FlightType.SWEEP in mission_types
    assert FlightType.REFUELING in mission_types

    # Carrier
    mocker.patch("game.theater.controlpoint.Carrier.is_friendly", return_value=False)
    carrier = Carrier(name="test", at=None, theater=None, starts_blue=Player.BLUE)  # type: ignore
    mission_types = list(carrier.mission_types(for_player=Player.BLUE))
    assert len(mission_types) == 5
    assert FlightType.ANTISHIP in mission_types
    assert FlightType.ESCORT in mission_types
    assert FlightType.TARCAP in mission_types
    assert FlightType.SEAD_ESCORT in mission_types
    assert FlightType.SWEEP in mission_types

    # LHA
    mocker.patch("game.theater.controlpoint.Lha.is_friendly", return_value=False)
    lha = Lha(name="test", at=None, theater=None, starts_blue=Player.BLUE)  # type: ignore
    mission_types = list(lha.mission_types(for_player=Player.BLUE))
    assert len(mission_types) == 5
    assert FlightType.ANTISHIP in mission_types
    assert FlightType.ESCORT in mission_types
    assert FlightType.TARCAP in mission_types
    assert FlightType.SEAD_ESCORT in mission_types
    assert FlightType.SWEEP in mission_types

    # Fob
    mocker.patch("game.theater.controlpoint.Fob.is_friendly", return_value=False)
    fob = Fob(name="test", at=None, theater=None, starts_blue=Player.BLUE)  # type: ignore
    mission_types = list(fob.mission_types(for_player=Player.BLUE))
    assert len(mission_types) == 6
    assert FlightType.AIR_ASSAULT in mission_types
    assert FlightType.ESCORT in mission_types
    assert FlightType.TARCAP in mission_types
    assert FlightType.SEAD_ESCORT in mission_types
    assert FlightType.SWEEP in mission_types
    assert FlightType.STRIKE in mission_types

    # Off map spawn
    mocker.patch(
        "game.theater.controlpoint.OffMapSpawn.is_friendly", return_value=False
    )
    off_map_spawn = OffMapSpawn(name="test", position=None, theater=None, starts_blue=Player.BLUE)  # type: ignore
    mission_types = list(off_map_spawn.mission_types(for_player=Player.BLUE))
    assert len(mission_types) == 0


@pytest.fixture
def test_control_point_parking(mocker: Any) -> None:
    """
    Test correct number of parking slots are returned for control point
    """
    # Airfield
    mocker.patch("game.theater.controlpoint.unclaimed_parking", return_value=10)
    airport = Airport(None, None)  # type: ignore
    airport.name = "test"  # required for Airfield.__init__
    point = Point(0, 0, None)  # type: ignore
    control_point = Airfield(airport, theater=None, starts_blue=Player.BLUE)  # type: ignore
    parking_type_ground_start = ParkingType(
        fixed_wing=False, fixed_wing_stol=True, rotary_wing=False
    )
    parking_type_rotary = ParkingType(
        fixed_wing=False, fixed_wing_stol=False, rotary_wing=True
    )
    for x in range(10):
        control_point.ground_spawns.append(
            (
                PointWithHeading.from_point(
                    point,
                    Heading.from_degrees(0),
                ),
                point,
            )
        )
    for x in range(20):
        control_point.helipads.append(
            PointWithHeading.from_point(
                point,
                Heading.from_degrees(0),
            )
        )

    assert control_point.unclaimed_parking(parking_type_ground_start) == 10
    assert control_point.unclaimed_parking(parking_type_rotary) == 20


@pytest.fixture
def test_parking_type_from_squadron(mocker: Any) -> None:
    """
    Test correct ParkingType object returned for a squadron of Viggens
    """
    mocker.patch(
        "game.theater.controlpoint.parking_type.include_fixed_wing_stol",
        return_value=True,
    )
    aircraft = next(AircraftType.for_dcs_type(AJS37))
    squadron = Squadron(
        name="test",
        nickname=None,
        country=country_with_name("Sweden"),
        role="test",
        aircraft=aircraft,
        max_size=16,
        livery=None,
        primary_task=FlightType.STRIKE,
        auto_assignable_mission_types=set(aircraft.iter_task_capabilities()),
        operating_bases=OperatingBases.default_for_aircraft(aircraft),
        female_pilot_percentage=0,
    )  # type: ignore
    parking_type = ParkingType().from_squadron(squadron)

    assert parking_type.include_rotary_wing == False
    assert parking_type.include_fixed_wing == True
    assert parking_type.include_fixed_wing_stol == True


@pytest.fixture
def test_parking_type_from_aircraft(mocker: Any) -> None:
    """
    Test correct ParkingType object returned for Viggen aircraft type
    """
    mocker.patch(
        "game.theater.controlpoint.parking_type.include_fixed_wing_stol",
        return_value=True,
    )
    aircraft = next(AircraftType.for_dcs_type(AJS37))
    parking_type = ParkingType().from_aircraft(aircraft, False)

    assert parking_type.include_rotary_wing == False
    assert parking_type.include_fixed_wing == True
    assert parking_type.include_fixed_wing_stol == True


def _capture_zone_cp(position: Point, name: str = "Test CP") -> Any:
    """A stand-in ControlPoint carrying only what the capture-zone check reads."""
    cp = MagicMock(spec=ControlPoint)
    cp.name = name
    cp.position = position
    return cp


def test_motorpool_inside_capture_zone_logs_error(caplog: Any) -> None:
    terrain = MagicMock(spec=Terrain)
    cp = _capture_zone_cp(Point(0.0, 0.0, terrain))
    # 2.5 km east of the CP: inside the 3 km capture radius.
    location = Point(2500.0, 0.0, terrain)

    with caplog.at_level(logging.ERROR):
        warn_if_motorpool_inside_capture_zone("JAGUAR", location, cp)

    assert any(
        "JAGUAR" in record.message
        and "capture zone" in record.message
        and "approximately 2 nm" in record.message
        for record in caplog.records
    )


def test_motorpool_outside_capture_zone_is_silent(caplog: Any) -> None:
    terrain = MagicMock(spec=Terrain)
    cp = _capture_zone_cp(Point(0.0, 0.0, terrain))
    # 3.5 km east of the CP: outside the 3 km capture radius.
    location = Point(3500.0, 0.0, terrain)

    with caplog.at_level(logging.ERROR):
        warn_if_motorpool_inside_capture_zone("JAGUAR", location, cp)

    assert not any("capture zone" in record.message for record in caplog.records)


def _preset(name: str, position: Point) -> PresetLocation:
    return PresetLocation(name, position, Heading.from_degrees(0))


def _cp_with_motorpool_tgos(
    cp_position: Point,
    tgo_positions: list[tuple[str, Point]],
    name: str = "Test CP",
) -> Any:
    cp = MagicMock(spec=ControlPoint)
    cp.name = name
    cp.position = cp_position
    cp.captured = MagicMock()
    cp.captured.is_blue = True
    cp.ground_objects = [
        MotorpoolGroundObject(tgo_name, _preset(tgo_name, pos), cp, None)
        for tgo_name, pos in tgo_positions
    ]
    return cp


def test_capture_rehomes_motorpools_immediately() -> None:
    from game.missiongenerator.motorpoolpopulator import MotorpoolPopulator

    cp = cast(Any, ControlPoint.__new__(Airfield))
    old_coalition = MagicMock()
    new_coalition = MagicMock()
    cp._coalition = old_coalition
    cp.connected_objectives = []
    cp.front_lines = {}
    cp.ground_unit_orders = MagicMock()
    cp.base = MagicMock()
    cp.retreat_ground_units = MagicMock()
    cp.retreat_air_units = MagicMock()
    cp.release_parking_slots = MagicMock()
    cp.depopulate_uncapturable_tgos = MagicMock()
    cp._clear_front_lines = MagicMock()
    cp._create_missing_front_lines = MagicMock()
    tgo = MotorpoolGroundObject(
        "JAGUAR",
        _preset("Garage A", Point(4000.0, 0.0, MagicMock(spec=Terrain))),
        cp,
        GroupTask.MOTORPOOL,
    )
    cp.connected_objectives.append(tgo)
    game = MagicMock()
    game.coalition_for.return_value = new_coalition
    game.theater.controlpoints = [cp]
    events = MagicMock()

    with patch.object(MotorpoolPopulator, "_rehome_motorpools") as rehome:
        cp.capture(game, events, Player.BLUE)

    assert cp._coalition is new_coalition
    rehome.assert_called_once_with(events)


def test_capture_publishes_rehomed_motorpool_tgo_update() -> None:
    terrain = MagicMock(spec=Terrain)
    captured_cp = cast(Any, ControlPoint.__new__(Airfield))
    captured_cp._coalition = MagicMock()
    captured_cp.connected_objectives = []
    captured_cp.front_lines = {}
    captured_cp.ground_unit_orders = MagicMock()
    captured_cp.base = MagicMock()
    captured_cp.retreat_ground_units = MagicMock()
    captured_cp.retreat_air_units = MagicMock()
    captured_cp.release_parking_slots = MagicMock()
    captured_cp.depopulate_uncapturable_tgos = MagicMock()
    captured_cp._clear_front_lines = MagicMock()
    captured_cp._create_missing_front_lines = MagicMock()
    captured_cp.cptype = ControlPointType.AIRBASE
    captured_cp.position = Point(5000.0, 0.0, terrain)
    motorpool_location = _preset("Garage A", Point(0.0, 0.0, terrain))
    captured_cp.preset_locations = SimpleNamespace(motorpools=[motorpool_location])

    destination_cp = SimpleNamespace(
        cptype=ControlPointType.FARP,
        position=Point(0.0, 0.0, terrain),
        connected_objectives=[],
        preset_locations=SimpleNamespace(motorpools=[]),
    )
    tgo = MotorpoolGroundObject(
        "JAGUAR",
        motorpool_location,
        captured_cp,
        GroupTask.MOTORPOOL,
    )
    captured_cp.connected_objectives.append(tgo)
    game = MagicMock()
    game.coalition_for.return_value = MagicMock()
    game.theater.controlpoints = [captured_cp, destination_cp]
    events = GameUpdateEvents()

    captured_cp.capture(game, events, Player.BLUE)

    assert tgo.control_point is destination_cp
    assert events.updated_tgos == {tgo}


def test_motorpools_inside_capture_zone_reports_only_inside() -> None:
    terrain = MagicMock(spec=Terrain)
    cp = _cp_with_motorpool_tgos(
        Point(0.0, 0.0, terrain),
        [
            ("Near", Point(2500.0, 0.0, terrain)),
            ("Far", Point(4000.0, 0.0, terrain)),
        ],
    )
    violations = motorpools_inside_capture_zone([cp])
    assert len(violations) == 1
    assert violations[0].motorpool == "Near"
    assert violations[0].control_point == "Test CP"


def test_motorpools_inside_capture_zone_empty_when_all_outside() -> None:
    terrain = MagicMock(spec=Terrain)
    cp = _cp_with_motorpool_tgos(
        Point(0.0, 0.0, terrain), [("Far", Point(4000.0, 0.0, terrain))]
    )
    assert motorpools_inside_capture_zone([cp]) == []
