from __future__ import annotations

from types import SimpleNamespace
from typing import Any, cast
from uuid import UUID
from unittest.mock import patch

import pytest
from dcs import Mission
from dcs.terrain import NoParkingSlotError
from game.pretense.pretenseflightgroupspawner import PretenseFlightGroupSpawner
from dcs.mapping import Point
from dcs.planes import F_16C_50
from dcs.helicopters import UH_1H
from dcs.terrain import Caucasus

from game.ato.flight import Flight
from game.ato.flightstate.inflight import InFlight
from game.ato.starttype import StartType
from game.missiongenerator.aircraft.flightgroupspawner import FlightGroupSpawner
from game.missiongenerator.missiondata import MissionData
from game.theater import Airfield, OffMapSpawn
from game.utils import feet, knots

CP_ID = UUID("00000000-0000-0000-0000-000000000001")


class FlightStub:
    state: Any

    def __init__(
        self, aircraft: Any, origin: Any, alt: Any, alt_type: str = "RADIO"
    ) -> None:
        self.unit_type = SimpleNamespace(
            dcs_unit_type=aircraft,
            variant_id=aircraft.id,
            helicopter=aircraft == UH_1H,
            max_speed=knots(aircraft.max_speed),
        )
        self.is_helo = aircraft == UH_1H
        self.flight_plan = SimpleNamespace(
            waypoints=[SimpleNamespace(alt=alt, alt_type=alt_type)]
        )
        self.departure = origin
        self.coalition = SimpleNamespace(
            game=SimpleNamespace(
                settings=SimpleNamespace(
                    nevatim_parking_fix=False,
                    ground_start_ai_planes=False,
                )
            )
        )
        self.squadron = SimpleNamespace(
            location=origin,
            aircraft=SimpleNamespace(
                helicopter=aircraft == UH_1H, lha_capable=False, dcs_unit_type=aircraft
            ),
        )
        self.count = 2
        self.callsign = None
        self.custom_name = None
        self.package = SimpleNamespace(target=SimpleNamespace(name="Test target"))
        self.flight_type = "Test flight"
        self.state: Any = SimpleNamespace(
            is_waiting_for_start=True, spawn_type=StartType.COLD
        )
        self.group_id = 0


class EstimateState(InFlight):
    def __init__(self, position: Point) -> None:
        self.position = position

    def estimate_position(self) -> Point:
        return self.position

    def estimate_altitude(self) -> tuple[Any, str]:
        return feet(100), "RADIO"

    def estimate_speed(self) -> Any:
        return knots(300)


def make_spawner(
    aircraft: Any = F_16C_50,
    offmap: bool = False,
    alt: Any = feet(1000),
    alt_type: str = "RADIO",
) -> tuple[FlightGroupSpawner, FlightStub, Mission]:
    mission = Mission(Caucasus())
    position = Point(0, 0, mission.terrain)
    origin: Any
    if offmap:
        origin = object.__new__(OffMapSpawn)
        origin.id = CP_ID
        origin.position = position
    else:
        origin = object.__new__(Airfield)
        origin.id = CP_ID
        origin.position = position
        origin.airport = next(iter(mission.terrain.airports.values()))
        origin.helipads = []
        origin.helipads_quad = []
        origin.helipads_invisible = []
        origin.ground_spawns_roadbase = []
        origin.ground_spawns_large = []
        origin.ground_spawns = []
    origin.name = "Test departure"
    flight = FlightStub(aircraft, origin, alt, alt_type)
    spawner = FlightGroupSpawner(
        cast(Flight, flight),
        mission.country("USA"),
        mission,
        {},
        {},
        {},
        {},
        MissionData(),
    )
    return spawner, flight, mission


def test_fixed_wing_departures_use_real_mission_groups_and_keep_legacy_stack() -> None:
    spawner, _, _ = make_spawner()

    first = spawner._generate_over_departure("first", spawner.flight.departure)
    second = spawner._generate_over_departure("second", spawner.flight.departure)

    assert [
        point.alt for point in (first.points[0], second.points[0])
    ] == pytest.approx([feet(2000).meters, feet(2500).meters])
    assert [group.points[0].alt_type for group in (first, second)] == ["RADIO", "RADIO"]
    assert len(first.units) == len(second.units) == 2
    assert spawner.mission_data.cp_stack[CP_ID].meters == pytest.approx(
        feet(900).meters
    )
    assert spawner.mission_data.fixed_wing_departure_stack[
        CP_ID
    ].meters == pytest.approx(feet(3000).meters)


def test_offmap_radio_request_and_baro_reference_are_preserved() -> None:
    radio_spawner, _, _ = make_spawner(offmap=True, alt=feet(5000))
    radio = radio_spawner._generate_over_departure(
        "radio", radio_spawner.flight.departure
    )
    baro_spawner, _, _ = make_spawner(offmap=True, alt=feet(12000), alt_type="BARO")
    baro = baro_spawner._generate_over_departure("baro", baro_spawner.flight.departure)

    assert radio.points[0].alt_type == "RADIO"
    assert radio.points[0].alt == pytest.approx(feet(5000).meters)
    assert radio_spawner.mission_data.fixed_wing_departure_stack[
        CP_ID
    ].meters == pytest.approx(feet(5500).meters)
    assert baro.points[0].alt_type == "BARO"
    assert baro.points[0].alt == pytest.approx(feet(12000).meters)
    assert baro_spawner.mission_data.fixed_wing_departure_stack == {}


def test_helicopter_departure_does_not_reserve_fixed_wing_slot() -> None:
    spawner, _, _ = make_spawner(aircraft=UH_1H)

    group = spawner._generate_over_departure("helo", spawner.flight.departure)

    assert group.points[0].alt_type == "RADIO"
    assert group.points[0].alt == pytest.approx(500)
    assert spawner.mission_data.fixed_wing_departure_stack == {}


@pytest.mark.parametrize("pretense", [False, True])
def test_mid_mission_radio_floor_stays_separate_when_interleaved_with_departures(
    pretense: bool,
) -> None:
    spawner, flight, _ = make_spawner()
    if pretense:
        spawner.__class__ = PretenseFlightGroupSpawner
    flight.state = EstimateState(Point(100, 200, spawner.mission.terrain))

    departure = spawner._generate_over_departure("departure", flight.departure)
    if pretense:
        with patch.object(PretenseFlightGroupSpawner, "insert_into_pretense"):
            midroute = spawner.generate_mid_mission()
    else:
        midroute = spawner.generate_mid_mission()

    assert departure.points[0].alt == pytest.approx(feet(2000).meters)
    assert midroute.points[0].alt == pytest.approx(feet(700).meters)
    assert midroute.points[0].alt_type == "RADIO"
    assert spawner.mission_data.cp_stack[CP_ID].meters == pytest.approx(
        feet(900).meters
    )
    assert spawner.mission_data.fixed_wing_departure_stack[
        CP_ID
    ].meters == pytest.approx(feet(2500).meters)


def test_each_mission_data_starts_a_fresh_departure_stack() -> None:
    first, _, _ = make_spawner()
    second, _, _ = make_spawner()

    first._generate_over_departure("first", first.flight.departure)
    group = second._generate_over_departure("second", second.flight.departure)

    assert group.points[0].alt == pytest.approx(feet(2000).meters)
    assert second.mission_data.fixed_wing_departure_stack[
        CP_ID
    ].meters == pytest.approx(feet(2500).meters)


@pytest.mark.parametrize("start_type", [StartType.COLD, StartType.RUNWAY])
def test_create_flight_group_parking_or_runway_overflow_uses_departure_stack(
    start_type: StartType,
) -> None:
    spawner, flight, _ = make_spawner()
    flight.state.spawn_type = start_type
    with patch.object(
        spawner,
        "_generate_at_airfield",
        side_effect=NoParkingSlotError,
    ):
        group = spawner.create_flight_group()

    assert flight.group_id == group.id
    assert group.points[0].alt_type == "RADIO"
    assert group.points[0].alt == pytest.approx(feet(2000).meters)
