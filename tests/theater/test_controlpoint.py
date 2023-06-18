import pytest
from typing import Any

from dcs import Point
from dcs.planes import AJS37
from dcs.terrain.terrain import Airport
from game.ato.flighttype import FlightType
from game.dcs.aircrafttype import AircraftType
from game.dcs.countries import country_with_name
from game.point_with_heading import PointWithHeading
from game.squadrons import Squadron
from game.squadrons.operatingbases import OperatingBases
from game.theater.controlpoint import (
    Airfield,
    Carrier,
    Lha,
    OffMapSpawn,
    Fob,
    ParkingType,
)
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
    airfield = Airfield(airport, theater=None, starts_blue=True)  # type: ignore
    mission_types = list(airfield.mission_types(for_player=True))
    assert len(mission_types) == 3
    assert FlightType.AEWC in mission_types
    assert FlightType.REFUELING in mission_types
    assert FlightType.BARCAP in mission_types

    # Carrier
    mocker.patch("game.theater.controlpoint.Carrier.is_friendly", return_value=True)
    carrier = Carrier(name="test", at=None, theater=None, starts_blue=True)  # type: ignore
    mission_types = list(carrier.mission_types(for_player=True))
    assert len(mission_types) == 3
    assert FlightType.AEWC in mission_types
    assert FlightType.REFUELING in mission_types
    assert FlightType.BARCAP in mission_types

    # LHA
    mocker.patch("game.theater.controlpoint.Lha.is_friendly", return_value=True)
    lha = Lha(name="test", at=None, theater=None, starts_blue=True)  # type: ignore
    mission_types = list(lha.mission_types(for_player=True))
    assert len(mission_types) == 3
    assert FlightType.AEWC in mission_types
    assert FlightType.REFUELING in mission_types
    assert FlightType.BARCAP in mission_types

    # Fob
    mocker.patch("game.theater.controlpoint.Fob.is_friendly", return_value=True)
    fob = Fob(name="test", at=None, theater=None, starts_blue=True)  # type: ignore
    mission_types = list(fob.mission_types(for_player=True))
    assert len(mission_types) == 2
    assert FlightType.AEWC in mission_types
    assert FlightType.BARCAP in mission_types

    # Off map spawn
    mocker.patch("game.theater.controlpoint.OffMapSpawn.is_friendly", return_value=True)
    off_map_spawn = OffMapSpawn(name="test", position=None, theater=None, starts_blue=True)  # type: ignore
    mission_types = list(off_map_spawn.mission_types(for_player=True))
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
    airfield = Airfield(airport, theater=None, starts_blue=True)  # type: ignore
    mission_types = list(airfield.mission_types(for_player=True))
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
    carrier = Carrier(name="test", at=None, theater=None, starts_blue=True)  # type: ignore
    mission_types = list(carrier.mission_types(for_player=True))
    assert len(mission_types) == 5
    assert FlightType.ANTISHIP in mission_types
    assert FlightType.ESCORT in mission_types
    assert FlightType.TARCAP in mission_types
    assert FlightType.SEAD_ESCORT in mission_types
    assert FlightType.SWEEP in mission_types

    # LHA
    mocker.patch("game.theater.controlpoint.Lha.is_friendly", return_value=False)
    lha = Lha(name="test", at=None, theater=None, starts_blue=True)  # type: ignore
    mission_types = list(lha.mission_types(for_player=True))
    assert len(mission_types) == 5
    assert FlightType.ANTISHIP in mission_types
    assert FlightType.ESCORT in mission_types
    assert FlightType.TARCAP in mission_types
    assert FlightType.SEAD_ESCORT in mission_types
    assert FlightType.SWEEP in mission_types

    # Fob
    mocker.patch("game.theater.controlpoint.Fob.is_friendly", return_value=False)
    fob = Fob(name="test", at=None, theater=None, starts_blue=True)  # type: ignore
    mission_types = list(fob.mission_types(for_player=True))
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
    off_map_spawn = OffMapSpawn(name="test", position=None, theater=None, starts_blue=True)  # type: ignore
    mission_types = list(off_map_spawn.mission_types(for_player=True))
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
    control_point = Airfield(airport, theater=None, starts_blue=True)  # type: ignore
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
