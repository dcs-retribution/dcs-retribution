from __future__ import annotations

import logging
import random
from datetime import datetime
from functools import cached_property
from typing import Any, Dict, List, TYPE_CHECKING, Tuple

from dcs import Point
from dcs.action import AITaskPush
from dcs.condition import FlagIsTrue, GroupDead, Or, FlagIsFalse
from dcs.country import Country
from dcs.mission import Mission
from dcs.terrain.terrain import NoParkingSlotError
from dcs.triggers import TriggerOnce, Event
from dcs.unit import Skill
from dcs.unitgroup import FlyingGroup, StaticGroup

from game.ato.airtaaskingorder import AirTaskingOrder
from game.ato.flight import Flight
from game.ato.flightstate import Completed, WaitingForStart
from game.ato.flighttype import FlightType
from game.ato.package import Package
from game.ato.starttype import StartType
from game.missiongenerator.lasercoderegistry import LaserCodeRegistry
from game.missiongenerator.missiondata import MissionData
from game.radio.radios import RadioRegistry
from game.radio.tacan import TacanRegistry
from game.runways import RunwayData
from game.settings import Settings
from game.theater.controlpoint import (
    Airfield,
    ControlPoint,
    Fob,
    OffMapSpawn,
)
from game.unitmap import UnitMap
from game.missiongenerator.aircraft.aircraftpainter import AircraftPainter
from game.missiongenerator.aircraft.flightdata import FlightData
from game.data.weapons import WeaponType

if TYPE_CHECKING:
    from game import Game
    from game.squadrons import Squadron


class PretenseAircraftGenerator:
    def __init__(
        self,
        mission: Mission,
        settings: Settings,
        game: Game,
        time: datetime,
        radio_registry: RadioRegistry,
        tacan_registry: TacanRegistry,
        laser_code_registry: LaserCodeRegistry,
        unit_map: UnitMap,
        mission_data: MissionData,
        helipads: dict[ControlPoint, list[StaticGroup]],
        ground_spawns_roadbase: dict[ControlPoint, list[Tuple[StaticGroup, Point]]],
        ground_spawns: dict[ControlPoint, list[Tuple[StaticGroup, Point]]],
    ) -> None:
        self.mission = mission
        self.settings = settings
        self.game = game
        self.time = time
        self.radio_registry = radio_registry
        self.tacan_registy = tacan_registry
        self.laser_code_registry = laser_code_registry
        self.unit_map = unit_map
        self.flights: List[FlightData] = []
        self.mission_data = mission_data
        self.helipads = helipads
        self.ground_spawns_roadbase = ground_spawns_roadbase
        self.ground_spawns = ground_spawns

        self.ewrj_package_dict: Dict[int, List[FlyingGroup[Any]]] = {}
        self.ewrj = settings.plugins.get("ewrj")
        self.need_ecm = settings.plugin_option("ewrj.ecm_required")

    @cached_property
    def use_client(self) -> bool:
        """True if Client should be used instead of Player."""
        blue_clients = self.client_slots_in_ato(self.game.blue.ato)
        red_clients = self.client_slots_in_ato(self.game.red.ato)
        return blue_clients + red_clients > 1

    @staticmethod
    def client_slots_in_ato(ato: AirTaskingOrder) -> int:
        total = 0
        for package in ato.packages:
            for flight in package.flights:
                total += flight.client_count
        return total

    def clear_parking_slots(self) -> None:
        for cp in self.game.theater.controlpoints:
            for parking_slot in cp.parking_slots:
                parking_slot.unit_id = None

    def generate_flights(
        self,
        country: Country,
        cp: ControlPoint,
        ato: AirTaskingOrder,
        dynamic_runways: Dict[str, RunwayData],
    ) -> None:
        """Adds aircraft to the mission for every flight in the ATO.

        Aircraft generation is done by walking the ATO and spawning each flight in turn.
        After the flight is generated the group is added to the UnitMap so aircraft
        deaths can be tracked.

        Args:
            country: The country from the mission to use for this ATO.
            ato: The ATO to spawn aircraft for.
            dynamic_runways: Runway data for carriers and FARPs.
        """

        num_of_sead = 0
        num_of_cas = 0
        num_of_strike = 0
        num_of_cap = 0

        for squadron in cp.squadrons:
            # Intentionally don't spawn anything at OffMapSpawns in Pretense
            if isinstance(squadron.location, OffMapSpawn):
                continue

            squadron.owned_aircraft += 1
            squadron.untasked_aircraft += 1
            package = Package(cp, squadron.flight_db, auto_asap=False)
            mission_types = squadron.auto_assignable_mission_types
            if (
                FlightType.TRANSPORT in mission_types
                or FlightType.AIR_ASSAULT in mission_types
            ):
                flight_type = FlightType.AIR_ASSAULT
            elif (
                FlightType.SEAD in mission_types
                or FlightType.SEAD_SWEEP in mission_types
                or FlightType.SEAD_ESCORT in mission_types
            ) and num_of_sead < 2:
                flight_type = FlightType.SEAD
                num_of_sead += 1
            elif FlightType.DEAD in mission_types and num_of_sead < 2:
                flight_type = FlightType.DEAD
                num_of_sead += 1
            elif (
                FlightType.CAS in mission_types or FlightType.BAI in mission_types
            ) and num_of_cas < 2:
                flight_type = FlightType.CAS
                num_of_cas += 1
            elif (
                FlightType.STRIKE in mission_types
                or FlightType.OCA_RUNWAY in mission_types
                or FlightType.OCA_AIRCRAFT in mission_types
            ) and num_of_strike < 2:
                flight_type = FlightType.STRIKE
                num_of_strike += 1
            elif (
                FlightType.BARCAP in mission_types
                or FlightType.TARCAP in mission_types
                or FlightType.ESCORT in mission_types
            ) and num_of_cap < 2:
                flight_type = FlightType.BARCAP
                num_of_cap += 1
            else:
                flight_type = random.choice(list(mission_types))
            flight = Flight(
                package, squadron, 1, flight_type, StartType.COLD, divert=cp
            )
            flight.state = WaitingForStart(
                flight, self.game.settings, self.game.conditions.start_time
            )
            package.add_flight(flight)
            ato.add_package(package)

        self._reserve_frequencies_and_tacan(ato)

        for package in reversed(sorted(ato.packages, key=lambda x: x.time_over_target)):
            logging.info(f"Generating package for target: {package.target.name}")
            if not package.flights:
                continue
            for flight in package.flights:
                if flight.alive:
                    if not flight.squadron.location.runway_is_operational():
                        logging.warning(
                            f"Runway not operational, skipping flight: {flight.flight_type}"
                        )
                        flight.return_pilots_and_aircraft()
                        continue
                    logging.info(f"Generating flight: {flight.unit_type}")
                    group = self.create_and_configure_flight(
                        flight, country, dynamic_runways
                    )
                    self.unit_map.add_aircraft(group, flight)

    def create_and_configure_flight(
        self, flight: Flight, country: Country, dynamic_runways: Dict[str, RunwayData]
    ) -> FlyingGroup[Any]:
        from game.pretense.pretenseflightgroupspawner import PretenseFlightGroupSpawner

        """Creates and configures the flight group in the mission."""
        group = PretenseFlightGroupSpawner(
            flight,
            country,
            self.mission,
            self.helipads,
            self.ground_spawns_roadbase,
            self.ground_spawns,
            self.mission_data,
        ).create_flight_group()
        if flight.flight_type in [
            FlightType.REFUELING,
            FlightType.AEWC,
        ]:
            self.flights.append(
                FlightGroupConfigurator(
                    flight,
                    group,
                    self.game,
                    self.mission,
                    self.time,
                    self.radio_registry,
                    self.tacan_registy,
                    self.laser_code_registry,
                    self.mission_data,
                    dynamic_runways,
                    self.use_client,
                ).configure()
            )

        if self.ewrj:
            self._track_ewrj_flight(flight, group)

        return group

    def _track_ewrj_flight(self, flight: Flight, group: FlyingGroup[Any]) -> None:
        if not self.ewrj_package_dict.get(id(flight.package)):
            self.ewrj_package_dict[id(flight.package)] = []
        if (
            flight.package.primary_flight
            and flight is flight.package.primary_flight
            or flight.client_count
            and (
                not self.need_ecm
                or flight.loadout.has_weapon_of_type(WeaponType.JAMMER)
            )
        ):
            self.ewrj_package_dict[id(flight.package)].append(group)

    def _reserve_frequencies_and_tacan(self, ato: AirTaskingOrder) -> None:
        for package in ato.packages:
            if package.frequency is None:
                continue
            if package.frequency not in self.radio_registry.allocated_channels:
                self.radio_registry.reserve(package.frequency)
            for f in package.flights:
                if (
                    f.frequency
                    and f.frequency not in self.radio_registry.allocated_channels
                ):
                    self.radio_registry.reserve(f.frequency)
                if f.tacan and f.tacan not in self.tacan_registy.allocated_channels:
                    self.tacan_registy.mark_unavailable(f.tacan)
