from __future__ import annotations

from datetime import datetime
from typing import Any, Optional, TYPE_CHECKING

from dcs import Mission, Point
from dcs.flyingunit import FlyingUnit
from dcs.unitgroup import FlyingGroup

from game.ato import Flight, FlightType
from game.ato.flightmember import FlightMember
from game.data.weapons import Pylon
from game.lasercodes.lasercoderegistry import LaserCodeRegistry
from game.missiongenerator.aircraft.aircraftbehavior import AircraftBehavior
from game.missiongenerator.aircraft.aircraftpainter import AircraftPainter
from game.missiongenerator.aircraft.bingoestimator import BingoEstimator
from game.missiongenerator.aircraft.flightdata import FlightData
from game.missiongenerator.aircraft.flightgroupconfigurator import (
    FlightGroupConfigurator,
)
from game.missiongenerator.aircraft.waypoints import WaypointGenerator
from game.missiongenerator.missiondata import MissionData
from game.radio.radios import RadioRegistry
from game.radio.tacan import (
    TacanRegistry,
)
from game.runways import RunwayData

if TYPE_CHECKING:
    from game import Game


class PretenseFlightGroupConfigurator(FlightGroupConfigurator):
    def __init__(
        self,
        flight: Flight,
        group: FlyingGroup[Any],
        game: Game,
        mission: Mission,
        time: datetime,
        radio_registry: RadioRegistry,
        tacan_registry: TacanRegistry,
        mission_data: MissionData,
        dynamic_runways: dict[str, RunwayData],
        use_client: bool,
    ) -> None:
        super().__init__(
            flight,
            group,
            game,
            mission,
            time,
            radio_registry,
            tacan_registry,
            mission_data,
            dynamic_runways,
            use_client,
        )

        self.flight = flight
        self.group = group
        self.game = game
        self.mission = mission
        self.time = time
        self.radio_registry = radio_registry
        self.tacan_registry = tacan_registry
        self.mission_data = mission_data
        self.dynamic_runways = dynamic_runways
        self.use_client = use_client

    def configure(self) -> FlightData:
        AircraftBehavior(self.flight.flight_type).apply_to(self.flight, self.group)
        AircraftPainter(self.flight, self.group).apply_livery()
        self.setup_props()
        self.setup_payloads()
        self.setup_fuel()
        flight_channel = self.setup_radios()

        laser_codes: list[Optional[int]] = []
        for unit, pilot in zip(self.group.units, self.flight.roster.members):
            self.configure_flight_member(unit, pilot, laser_codes)

        divert = None
        if self.flight.divert is not None:
            divert = self.flight.divert.active_runway(
                self.game.theater, self.game.conditions, self.dynamic_runways
            )

        mission_start_time, waypoints = WaypointGenerator(
            self.flight,
            self.group,
            self.mission,
            self.time,
            self.game.settings,
            self.mission_data,
        ).create_waypoints()

        divert_position: Point | None = None
        if self.flight.divert is not None:
            divert_position = self.flight.divert.position
        bingo_estimator = BingoEstimator(
            self.flight.unit_type.fuel_consumption,
            self.flight.arrival.position,
            divert_position,
            self.flight.flight_plan.waypoints,
        )

        self.group.uncontrolled = False

        return FlightData(
            package=self.flight.package,
            aircraft_type=self.flight.unit_type,
            squadron=self.flight.squadron,
            flight_type=self.flight.flight_type,
            units=self.group.units,
            size=len(self.group.units),
            friendly=self.flight.departure.captured,
            departure_delay=mission_start_time,
            departure=self.flight.departure.active_runway(
                self.game.theater, self.game.conditions, self.dynamic_runways
            ),
            arrival=self.flight.arrival.active_runway(
                self.game.theater, self.game.conditions, self.dynamic_runways
            ),
            divert=divert,
            waypoints=waypoints,
            intra_flight_channel=flight_channel,
            bingo_fuel=bingo_estimator.estimate_bingo(),
            joker_fuel=bingo_estimator.estimate_joker(),
            custom_name=self.flight.custom_name,
            laser_codes=laser_codes,
        )

    def setup_payloads(self) -> None:
        for unit, member in zip(self.group.units, self.flight.iter_members()):
            self.setup_payload(unit, member)

    def setup_payload(self, unit: FlyingUnit, member: FlightMember) -> None:
        unit.pylons.clear()

        loadout = member.loadout

        if self.flight.flight_type == FlightType.SEAD:
            loadout = member.loadout.default_for_task_and_aircraft(
                FlightType.SEAD_SWEEP, self.flight.unit_type.dcs_unit_type
            )

        if self.game.settings.restrict_weapons_by_date:
            loadout = loadout.degrade_for_date(self.flight.unit_type, self.game.date)

        for pylon_number, weapon in loadout.pylons.items():
            if weapon is None:
                continue
            pylon = Pylon.for_aircraft(self.flight.unit_type, pylon_number)
            pylon.equip(unit, weapon)
