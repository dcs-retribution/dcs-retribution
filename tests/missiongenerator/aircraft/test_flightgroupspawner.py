"""Regression tests for altitude reference propagation in FlightGroupSpawner.

The spawner sets the altitude reference (BARO/MSL vs RADIO/AGL) on the group's
first waypoint, but DCS uses the *unit* altitude type for spawn placement.
Mismatched references crash aircraft on spawn, so every generated airborne
unit must carry the same altitude reference as the first waypoint. Ground
starts are not touched and keep the pydcs default.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Optional

import pytest
from dcs import Mission, Point
from dcs.helicopters import UH_1H
from dcs.planes import AJS37
from dcs.terrain import Caucasus
from dcs.unitgroup import FlyingGroup

from game import persistency

from game.ato.flightstate import InFlight
from game.ato.flightstate.flightstate import FlightState
from game.ato.flighttype import FlightType
from game.ato.starttype import StartType
from game.dcs.aircrafttype import AircraftType
from game.dcs.countries import country_with_name
from game.missiongenerator.aircraft.flightgroupspawner import FlightGroupSpawner
from game.missiongenerator.missiondata import MissionData
from game.sim.gameupdateevents import GameUpdateEvents
from game.theater.controlpoint import Airfield, ControlPoint, OffMapSpawn, Player
from game.utils import Distance, Speed, feet, kph

RADIO = "RADIO"
BARO = "BARO"

_TERRAIN = Caucasus()


@pytest.fixture(scope="session", autouse=True)
def _persistency_setup(tmp_path_factory: pytest.TempPathFactory) -> None:
    # Loading the aircraft database reads the user weapon injection directory,
    # which requires persistency to be initialized. Use a throwaway folder so
    # the tests never touch the real saved games directory.
    persistency.setup(str(tmp_path_factory.mktemp("flightgroupspawner")), False, 0)


def _point(x: float, y: float) -> Point:
    return Point(x, y, _TERRAIN)


class _StubTarget:
    def __init__(self, name: str) -> None:
        self.name = name


class _StubPackage:
    def __init__(self, target_name: str) -> None:
        self.target = _StubTarget(target_name)


class _StubSquadron:
    def __init__(self, location: ControlPoint) -> None:
        self.location = location


class _StubWaypoint:
    def __init__(self, alt: Distance, alt_type: str) -> None:
        self.alt = alt
        self.alt_type = alt_type


class _StubFlightPlan:
    def __init__(self, waypoints: list[_StubWaypoint]) -> None:
        self.waypoints = waypoints


class _StubInFlight(InFlight):
    """In-flight state with fixed estimates for mid-mission spawns.

    Bypasses FlightState.__init__ because the spawner only reads the estimate
    methods and isinstance(state, InFlight).
    """

    def __init__(
        self, altitude: Distance, alt_type: str, speed: Speed, position: Point
    ) -> None:
        self.fixed_altitude = altitude
        self.fixed_alt_type = alt_type
        self.fixed_speed = speed
        self.fixed_position = position

    def estimate_altitude(self) -> tuple[Distance, str]:
        return self.fixed_altitude, self.fixed_alt_type

    def estimate_position(self) -> Point:
        return self.fixed_position

    def estimate_speed(self) -> Speed:
        return self.fixed_speed


class _StubWarmAtAirfield(FlightState):
    """Ground state driving a warm start from an airfield."""

    def __init__(self) -> None:
        pass

    @property
    def cancelable(self) -> bool:
        return False

    def on_game_tick(
        self, events: GameUpdateEvents, time: datetime, duration: timedelta
    ) -> None:
        pass

    @property
    def is_waiting_for_start(self) -> bool:
        return False

    def estimate_position(self) -> Point:
        raise NotImplementedError

    @property
    def spawn_type(self) -> StartType:
        return StartType.WARM

    @property
    def description(self) -> str:
        return "warm at airfield"


class _StubFlight:
    """Minimal stub matching the attributes the air-start spawner reads."""

    def __init__(
        self,
        unit_type: AircraftType,
        state: FlightState,
        location: ControlPoint,
        count: int,
        flight_plan: Optional[_StubFlightPlan] = None,
    ) -> None:
        self.custom_name: Optional[str] = None
        self.package = _StubPackage("Test Target")
        self.flight_type = FlightType.BARCAP
        self.unit_type = unit_type
        self.state = state
        self.squadron = _StubSquadron(location)
        self.count = count
        self.callsign = None
        self.is_helo = unit_type.helicopter
        self.flight_plan: _StubFlightPlan = (
            flight_plan if flight_plan is not None else _StubFlightPlan([])
        )


def _fixed_wing_type() -> AircraftType:
    return next(AircraftType.for_dcs_type(AJS37))


def _helicopter_type() -> AircraftType:
    return next(AircraftType.for_dcs_type(UH_1H))


def _off_map_spawn() -> OffMapSpawn:
    return OffMapSpawn(
        name="Off Map Spawn",
        position=_point(280000, 210000),
        theater=None,  # type: ignore[arg-type]
        starts_blue=Player.BLUE,
    )


def _airfield() -> Airfield:
    airport = Caucasus().airports["Batumi"]
    return Airfield(
        airport,
        theater=None,  # type: ignore[arg-type]
        starting_coalition=Player.BLUE,
    )


def _make_spawner(
    flight: _StubFlight, mission: Mission, mission_data: MissionData
) -> FlightGroupSpawner:
    return FlightGroupSpawner(
        flight=flight,  # type: ignore[arg-type]
        country=country_with_name("USA"),
        mission=mission,
        helipads={},
        ground_spawns_roadbase={},
        ground_spawns_large={},
        ground_spawns={},
        mission_data=mission_data,
    )


def _mid_mission_group(
    unit_type: AircraftType, count: int, alt: Distance, alt_type: str
) -> FlyingGroup[Any]:
    origin = _off_map_spawn()
    state = _StubInFlight(
        altitude=alt,
        alt_type=alt_type,
        speed=kph(800),
        position=_point(300000, 250000),
    )
    flight = _StubFlight(
        unit_type=unit_type,
        state=state,
        location=origin,
        count=count,
    )
    spawner = _make_spawner(flight, Mission(), MissionData())
    return spawner.generate_mid_mission()


def test_mid_mission_propagates_radio_to_all_fixed_wing_units() -> None:
    group = _mid_mission_group(
        _fixed_wing_type(), count=2, alt=feet(1000), alt_type=RADIO
    )
    assert len(group.units) == 2
    assert group.points[0].alt_type == RADIO
    for unit in group.units:
        assert unit.alt_type == RADIO
    assert group.points[0].alt == group.units[0].alt


def test_mid_mission_propagates_baro_to_all_fixed_wing_units() -> None:
    group = _mid_mission_group(
        _fixed_wing_type(), count=2, alt=feet(8000), alt_type=BARO
    )
    assert len(group.units) == 2
    assert group.points[0].alt_type == BARO
    for unit in group.units:
        assert unit.alt_type == BARO
    assert group.points[0].alt == group.units[0].alt


def test_mid_mission_propagates_radio_to_all_helicopter_units() -> None:
    group = _mid_mission_group(
        _helicopter_type(), count=4, alt=feet(1500), alt_type=RADIO
    )
    assert len(group.units) == 4
    assert group.points[0].alt_type == RADIO
    for unit in group.units:
        assert unit.alt_type == RADIO


def test_mid_mission_serialization_carries_unit_alt_types() -> None:
    group = _mid_mission_group(
        _fixed_wing_type(), count=2, alt=feet(1000), alt_type=RADIO
    )
    data = group.dict()
    assert data["route"]["points"][1]["alt_type"] == RADIO
    for unit_data in data["units"].values():
        assert unit_data["alt_type"] == RADIO


def test_mid_mission_serialization_carries_baro_unit_alt_types() -> None:
    group = _mid_mission_group(
        _fixed_wing_type(), count=2, alt=feet(8000), alt_type=BARO
    )
    data = group.dict()
    assert data["route"]["points"][1]["alt_type"] == BARO
    for unit_data in data["units"].values():
        assert unit_data["alt_type"] == BARO


def _over_departure_group(
    unit_type: AircraftType,
    origin: ControlPoint,
    count: int,
    flight_plan: Optional[_StubFlightPlan] = None,
) -> FlyingGroup[Any]:
    state = _StubInFlight(
        altitude=feet(500),
        alt_type=RADIO,
        speed=kph(800),
        position=_point(300000, 250000),
    )
    flight = _StubFlight(
        unit_type=unit_type,
        state=state,
        location=origin,
        count=count,
        flight_plan=flight_plan,
    )
    spawner = _make_spawner(flight, Mission(), MissionData())
    return spawner._generate_over_departure("Test Flight", origin)


def test_over_departure_offmap_propagates_radio_to_all_units() -> None:
    origin = _off_map_spawn()
    flight_plan = _StubFlightPlan([_StubWaypoint(feet(20000), RADIO)])
    group = _over_departure_group(
        _fixed_wing_type(), origin, count=2, flight_plan=flight_plan
    )
    assert len(group.units) == 2
    assert group.points[0].alt_type == RADIO
    for unit in group.units:
        assert unit.alt_type == RADIO


def test_over_departure_offmap_propagates_baro_to_all_units() -> None:
    origin = _off_map_spawn()
    flight_plan = _StubFlightPlan([_StubWaypoint(feet(20000), BARO)])
    group = _over_departure_group(
        _fixed_wing_type(), origin, count=2, flight_plan=flight_plan
    )
    assert len(group.units) == 2
    assert group.points[0].alt_type == BARO
    for unit in group.units:
        assert unit.alt_type == BARO


def test_over_departure_land_cp_propagates_radio_to_fixed_wing_units() -> None:
    group = _over_departure_group(_fixed_wing_type(), _airfield(), count=2)
    assert len(group.units) == 2
    assert group.points[0].alt_type == RADIO
    for unit in group.units:
        assert unit.alt_type == RADIO


def test_over_departure_land_cp_propagates_radio_to_helicopter_units() -> None:
    group = _over_departure_group(_helicopter_type(), _airfield(), count=2)
    assert len(group.units) == 2
    assert group.points[0].alt_type == RADIO
    for unit in group.units:
        assert unit.alt_type == RADIO


def test_airfield_ground_start_leaves_unit_alt_types_untouched() -> None:
    origin = _airfield()
    flight = _StubFlight(
        unit_type=_fixed_wing_type(),
        state=_StubWarmAtAirfield(),
        location=origin,
        count=2,
    )
    spawner = _make_spawner(flight, Mission(), MissionData())
    group = spawner._generate_at_airfield("Test Flight", origin)
    assert len(group.units) == 2
    # Ground starts are not air starts; units keep the pydcs default and must
    # not be switched to the first waypoint's RADIO reference.
    for unit in group.units:
        assert unit.alt_type == BARO
