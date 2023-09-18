from __future__ import annotations

import logging
import random
from datetime import datetime
from functools import cached_property
from typing import Any, Dict, List, TYPE_CHECKING, Tuple, Optional

from dcs import Point
from dcs.country import Country
from dcs.mission import Mission
from dcs.terrain import NoParkingSlotError
from dcs.unitgroup import FlyingGroup, StaticGroup

from game.ato.airtaaskingorder import AirTaskingOrder
from game.ato.flight import Flight
from game.ato.flightstate import WaitingForStart, Navigating
from game.ato.flighttype import FlightType
from game.ato.package import Package
from game.ato.starttype import StartType
from game.coalition import Coalition
from game.data.weapons import WeaponType
from game.dcs.aircrafttype import AircraftType
from game.missiongenerator.aircraft.flightdata import FlightData
from game.missiongenerator.aircraft.flightgroupconfigurator import (
    FlightGroupConfigurator,
)
from game.missiongenerator.lasercoderegistry import LaserCodeRegistry
from game.missiongenerator.missiondata import MissionData
from game.radio.radios import RadioRegistry
from game.radio.tacan import TacanRegistry
from game.runways import RunwayData
from game.settings import Settings
from game.squadrons import AirWing
from game.theater.controlpoint import (
    ControlPoint,
    OffMapSpawn,
    ParkingType,
    Airfield,
)
from game.theater.theatergroundobject import EwrGroundObject, SamGroundObject
from game.unitmap import UnitMap
from game.squadrons import Squadron

if TYPE_CHECKING:
    from game import Game


PRETENSE_SQUADRON_DEF_RETRIES = 100
PRETENSE_SEAD_FLIGHTS_PER_CP = 1
PRETENSE_CAS_FLIGHTS_PER_CP = 1
PRETENSE_STRIKE_FLIGHTS_PER_CP = 1
PRETENSE_BARCAP_FLIGHTS_PER_CP = 1
PRETENSE_AI_AIRCRAFT_PER_FLIGHT = 2
PRETENSE_AI_AWACS_PER_FLIGHT = 1
PRETENSE_AI_TANKERS_PER_FLIGHT = 1
PRETENSE_PLAYER_AIRCRAFT_PER_FLIGHT = 2


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

    def find_pretense_cargo_plane_cp(self, cp: ControlPoint) -> ControlPoint:
        """
        Finds the location (ControlPoint) for Pretense off-map transport planes.
        """
        distance_to_flot = 0.0
        offmap_transport_cp_id = cp.id
        parking_type = ParkingType(
            fixed_wing=True, fixed_wing_stol=True, rotary_wing=False
        )
        for front_line_cp in self.game.theater.controlpoints:
            if isinstance(front_line_cp, OffMapSpawn):
                continue
            for front_line in self.game.theater.conflicts():
                if front_line_cp.captured == cp.captured:
                    if (
                        front_line_cp.total_aircraft_parking(parking_type) > 0
                        and front_line_cp.position.distance_to_point(
                            front_line.position
                        )
                        > distance_to_flot
                    ):
                        distance_to_flot = front_line_cp.position.distance_to_point(
                            front_line.position
                        )
                        offmap_transport_cp_id = front_line_cp.id
        return self.game.theater.find_control_point_by_id(offmap_transport_cp_id)

    def should_generate_pretense_transports(
        self, air_wing: AirWing
    ) -> tuple[bool, bool]:
        """
        Returns a tuple of booleans, telling whether transport helicopter and aircraft
        squadrons should be generated from the faction squadron definitions.

        This helps to ensure that the faction has at least one transport helicopter and one cargo plane squadron.

        (autogenerate_transport_helicopter_squadron, autogenerate_cargo_plane_squadron)
        """
        autogenerate_transport_helicopter_squadron = True
        autogenerate_cargo_plane_squadron = True
        for aircraft_type in air_wing.squadrons:
            for squadron in air_wing.squadrons[aircraft_type]:
                if squadron.aircraft.helicopter and (
                    squadron.aircraft.capable_of(FlightType.TRANSPORT)
                    or squadron.aircraft.capable_of(FlightType.AIR_ASSAULT)
                ):
                    autogenerate_transport_helicopter_squadron = False
                elif not squadron.aircraft.helicopter and (
                    squadron.aircraft.capable_of(FlightType.TRANSPORT)
                    or squadron.aircraft.capable_of(FlightType.AIR_ASSAULT)
                ):
                    autogenerate_cargo_plane_squadron = False
        return (
            autogenerate_transport_helicopter_squadron,
            autogenerate_cargo_plane_squadron,
        )

    def generate_pretense_squadron(
        self,
        cp: ControlPoint,
        coalition: Coalition,
        flight_type: FlightType,
        fixed_wing: bool,
        num_retries: int,
    ) -> Optional[Squadron]:
        """
        Generates a Pretense squadron from the faction squadron definitions. Use FlightType AIR_ASSAULT
        for Pretense supply helicopters and TRANSPORT for off-map cargo plane squadrons.

        Retribution does not differentiate between fixed wing and rotary wing transport squadron definitions, which
        is why there is a retry mechanism in case the wrong type is returned. Use fixed_wing False
        for Pretense supply helicopters and fixed_wing True for off-map cargo plane squadrons.

        TODO: Find out if Pretense can handle rotary wing "cargo planes".
        """

        squadron_def = coalition.air_wing.squadron_def_generator.generate_for_task(
            flight_type, cp
        )
        print(
            f"Generating a squadron definition for fixed-wing {fixed_wing} squadron at {cp}"
        )
        for retries in range(num_retries):
            if squadron_def is None or fixed_wing == squadron_def.aircraft.helicopter:
                squadron_def = (
                    coalition.air_wing.squadron_def_generator.generate_for_task(
                        flight_type, cp
                    )
                )

        # Failed, stop here
        if squadron_def is None:
            return None

        squadron = Squadron.create_from(
            squadron_def,
            flight_type,
            2,
            cp,
            coalition,
            self.game,
        )
        if squadron.aircraft not in coalition.air_wing.squadrons:
            coalition.air_wing.squadrons[squadron.aircraft] = list()
        coalition.air_wing.add_squadron(squadron)
        return squadron

    def generate_pretense_squadron_for(
        self,
        aircraft_type: AircraftType,
        cp: ControlPoint,
        coalition: Coalition,
    ) -> Optional[Squadron]:
        """
        Generates a Pretense squadron from the faction squadron definitions for the designated
        AircraftType. Use FlightType AIR_ASSAULT
        for Pretense supply helicopters and TRANSPORT for off-map cargo plane squadrons.
        """

        squadron_def = coalition.air_wing.squadron_def_generator.generate_for_aircraft(
            aircraft_type
        )
        flight_type = random.choice(list(squadron_def.auto_assignable_mission_types))
        if flight_type == FlightType.ESCORT and aircraft_type.helicopter:
            flight_type = FlightType.CAS
        if flight_type in (
            FlightType.INTERCEPTION,
            FlightType.ESCORT,
            FlightType.SWEEP,
        ):
            flight_type = FlightType.BARCAP
        if flight_type in (FlightType.SEAD_ESCORT, FlightType.SEAD_SWEEP):
            flight_type = FlightType.SEAD
        if flight_type == FlightType.ANTISHIP:
            flight_type = FlightType.STRIKE
        if flight_type == FlightType.TRANSPORT:
            flight_type = FlightType.AIR_ASSAULT
        squadron = Squadron.create_from(
            squadron_def,
            flight_type,
            2,
            cp,
            coalition,
            self.game,
        )
        if squadron.aircraft not in coalition.air_wing.squadrons:
            coalition.air_wing.squadrons[squadron.aircraft] = list()
        coalition.air_wing.add_squadron(squadron)
        return squadron

    def generate_pretense_aircraft(
        self, cp: ControlPoint, ato: AirTaskingOrder
    ) -> None:
        """
        Plans and generates AI aircraft groups/packages for Pretense.

        Aircraft generation is done by walking the control points which will be made into
        Pretense "zones" and spawning flights for different missions.
        After the flight is generated the package is added to the ATO so the flights
        can be configured.

        Args:
            cp: Control point to generate aircraft for.
            ato: The ATO to generate aircraft for.
        """
        num_of_sead = 0
        num_of_cas = 0
        num_of_strike = 0
        num_of_cap = 0

        for squadron in cp.squadrons:
            # Intentionally don't spawn anything at OffMapSpawns in Pretense
            if isinstance(squadron.location, OffMapSpawn):
                continue
            if cp.coalition != squadron.coalition:
                continue

            squadron.owned_aircraft += PRETENSE_AI_AIRCRAFT_PER_FLIGHT
            squadron.untasked_aircraft += PRETENSE_AI_AIRCRAFT_PER_FLIGHT
            package = Package(cp, squadron.flight_db, auto_asap=False)
            mission_types = squadron.auto_assignable_mission_types
            aircraft_per_flight = 1
            if squadron.aircraft.helicopter and (
                FlightType.TRANSPORT in mission_types
                or FlightType.AIR_ASSAULT in mission_types
            ):
                flight_type = FlightType.AIR_ASSAULT
            elif not squadron.aircraft.helicopter and (
                FlightType.TRANSPORT in mission_types
                or FlightType.AIR_ASSAULT in mission_types
            ):
                flight_type = FlightType.TRANSPORT
            elif (
                FlightType.SEAD in mission_types
                or FlightType.SEAD_SWEEP in mission_types
                or FlightType.SEAD_ESCORT in mission_types
            ) and num_of_sead < PRETENSE_SEAD_FLIGHTS_PER_CP:
                flight_type = FlightType.SEAD
                num_of_sead += 1
                aircraft_per_flight = PRETENSE_AI_AIRCRAFT_PER_FLIGHT
            elif (
                FlightType.DEAD in mission_types
                and num_of_sead < PRETENSE_SEAD_FLIGHTS_PER_CP
            ):
                flight_type = FlightType.DEAD
                num_of_sead += 1
                aircraft_per_flight = PRETENSE_AI_AIRCRAFT_PER_FLIGHT
            elif (
                FlightType.CAS in mission_types or FlightType.BAI in mission_types
            ) and num_of_cas < PRETENSE_CAS_FLIGHTS_PER_CP:
                flight_type = FlightType.CAS
                num_of_cas += 1
                aircraft_per_flight = PRETENSE_AI_AIRCRAFT_PER_FLIGHT
            elif (
                FlightType.STRIKE in mission_types
                or FlightType.OCA_RUNWAY in mission_types
                or FlightType.OCA_AIRCRAFT in mission_types
            ) and num_of_strike < PRETENSE_STRIKE_FLIGHTS_PER_CP:
                flight_type = FlightType.STRIKE
                num_of_strike += 1
                aircraft_per_flight = PRETENSE_AI_AIRCRAFT_PER_FLIGHT
            elif (
                FlightType.BARCAP in mission_types
                or FlightType.TARCAP in mission_types
                or FlightType.ESCORT in mission_types
                or FlightType.INTERCEPTION in mission_types
            ) and num_of_cap < PRETENSE_BARCAP_FLIGHTS_PER_CP:
                flight_type = FlightType.BARCAP
                num_of_cap += 1
                aircraft_per_flight = PRETENSE_AI_AIRCRAFT_PER_FLIGHT
            elif FlightType.AEWC in mission_types:
                flight_type = FlightType.AEWC
                aircraft_per_flight = PRETENSE_AI_AWACS_PER_FLIGHT
            elif FlightType.REFUELING in mission_types:
                flight_type = FlightType.REFUELING
                aircraft_per_flight = PRETENSE_AI_TANKERS_PER_FLIGHT
            else:
                continue

            if flight_type == FlightType.TRANSPORT:
                flight = Flight(
                    package,
                    squadron,
                    aircraft_per_flight,
                    FlightType.PRETENSE_CARGO,
                    StartType.IN_FLIGHT,
                    divert=cp,
                )
                package.add_flight(flight)
                flight.state = Navigating(flight, self.game.settings, waypoint_index=1)
            else:
                flight = Flight(
                    package,
                    squadron,
                    aircraft_per_flight,
                    flight_type,
                    StartType.COLD,
                    divert=cp,
                )
                package.add_flight(flight)
                flight.state = WaitingForStart(
                    flight, self.game.settings, self.game.conditions.start_time
                )

            ato.add_package(package)
        return

    def generate_pretense_aircraft_for_other_side(
        self, cp: ControlPoint, coalition: Coalition, ato: AirTaskingOrder
    ) -> None:
        """
        Plans and generates AI aircraft groups/packages for Pretense
        for the other side, which doesn't initially hold this control point.

        Aircraft generation is done by walking the control points which will be made into
        Pretense "zones" and spawning flights for different missions.
        After the flight is generated the package is added to the ATO so the flights
        can be configured.

        Args:
            cp: Control point to generate aircraft for.
            coalition: Coalition to generate aircraft for.
            ato: The ATO to generate aircraft for.
        """

        aircraft_per_flight = 1
        if cp.has_helipads and not cp.is_fleet:
            flight_type = FlightType.AIR_ASSAULT
            squadron = self.generate_pretense_squadron(
                cp,
                coalition,
                flight_type,
                False,
                PRETENSE_SQUADRON_DEF_RETRIES,
            )
            if squadron is not None:
                squadron.owned_aircraft += PRETENSE_AI_AIRCRAFT_PER_FLIGHT
                squadron.untasked_aircraft += PRETENSE_AI_AIRCRAFT_PER_FLIGHT
                package = Package(cp, squadron.flight_db, auto_asap=False)
                flight = Flight(
                    package,
                    squadron,
                    aircraft_per_flight,
                    flight_type,
                    StartType.COLD,
                    divert=cp,
                )
                print(
                    f"Generated flight for {flight_type} flying {squadron.aircraft.name} at {squadron.location.name}"
                )

                package.add_flight(flight)
                flight.state = WaitingForStart(
                    flight, self.game.settings, self.game.conditions.start_time
                )
                ato.add_package(package)
        if isinstance(cp, Airfield):
            # Generate SEAD flight
            flight_type = FlightType.SEAD
            aircraft_per_flight = PRETENSE_AI_AIRCRAFT_PER_FLIGHT
            squadron = self.generate_pretense_squadron(
                cp,
                coalition,
                flight_type,
                True,
                PRETENSE_SQUADRON_DEF_RETRIES,
            )
            if squadron is None:
                squadron = self.generate_pretense_squadron(
                    cp,
                    coalition,
                    FlightType.DEAD,
                    True,
                    PRETENSE_SQUADRON_DEF_RETRIES,
                )
            if squadron is not None:
                squadron.owned_aircraft += PRETENSE_AI_AIRCRAFT_PER_FLIGHT
                squadron.untasked_aircraft += PRETENSE_AI_AIRCRAFT_PER_FLIGHT
                package = Package(cp, squadron.flight_db, auto_asap=False)
                flight = Flight(
                    package,
                    squadron,
                    aircraft_per_flight,
                    flight_type,
                    StartType.COLD,
                    divert=cp,
                )
                print(
                    f"Generated flight for {flight_type} flying {squadron.aircraft.name} at {squadron.location.name}"
                )

                package.add_flight(flight)
                flight.state = WaitingForStart(
                    flight, self.game.settings, self.game.conditions.start_time
                )
                ato.add_package(package)

            # Generate CAS flight
            flight_type = FlightType.CAS
            aircraft_per_flight = PRETENSE_AI_AIRCRAFT_PER_FLIGHT
            squadron = self.generate_pretense_squadron(
                cp,
                coalition,
                flight_type,
                True,
                PRETENSE_SQUADRON_DEF_RETRIES,
            )
            if squadron is None:
                squadron = self.generate_pretense_squadron(
                    cp,
                    coalition,
                    FlightType.BAI,
                    True,
                    PRETENSE_SQUADRON_DEF_RETRIES,
                )
            if squadron is not None:
                squadron.owned_aircraft += PRETENSE_AI_AIRCRAFT_PER_FLIGHT
                squadron.untasked_aircraft += PRETENSE_AI_AIRCRAFT_PER_FLIGHT
                package = Package(cp, squadron.flight_db, auto_asap=False)
                flight = Flight(
                    package,
                    squadron,
                    aircraft_per_flight,
                    flight_type,
                    StartType.COLD,
                    divert=cp,
                )
                print(
                    f"Generated flight for {flight_type} flying {squadron.aircraft.name} at {squadron.location.name}"
                )

                package.add_flight(flight)
                flight.state = WaitingForStart(
                    flight, self.game.settings, self.game.conditions.start_time
                )
                ato.add_package(package)
        return

    def generate_pretense_aircraft_for_players(
        self, cp: ControlPoint, coalition: Coalition, ato: AirTaskingOrder
    ) -> None:
        """
        Plans and generates player piloted aircraft groups/packages for Pretense.

        Aircraft generation is done by walking the control points which will be made into
        Pretense "zones" and spawning flights for different missions.
        After the flight is generated the package is added to the ATO so the flights
        can be configured.

        Args:
            cp: Control point to generate aircraft for.
            coalition: Coalition to generate aircraft for.
            ato: The ATO to generate aircraft for.
        """

        aircraft_per_flight = PRETENSE_PLAYER_AIRCRAFT_PER_FLIGHT
        random_aircraft_list = list(coalition.faction.aircraft)
        random.shuffle(random_aircraft_list)
        for aircraft_type in random_aircraft_list:
            # Don't generate any player flights for non-flyable types (obviously)
            if not aircraft_type.flyable:
                continue
            if not cp.can_operate(aircraft_type):
                continue

            squadron = self.generate_pretense_squadron_for(
                aircraft_type,
                cp,
                coalition,
            )
            if squadron is not None:
                squadron.owned_aircraft += PRETENSE_PLAYER_AIRCRAFT_PER_FLIGHT
                squadron.untasked_aircraft += PRETENSE_PLAYER_AIRCRAFT_PER_FLIGHT
                squadron.populate_for_turn_0(False)
                for pilot in squadron.pilot_pool:
                    pilot.player = True
                package = Package(cp, squadron.flight_db, auto_asap=False)
                flight = Flight(
                    package,
                    squadron,
                    aircraft_per_flight,
                    squadron.primary_task,
                    StartType.COLD,
                    divert=cp,
                )
                for pilot in flight.roster.pilots:
                    if pilot is not None:
                        pilot.player = True
                print(
                    f"Generated flight for {squadron.primary_task} flying {squadron.aircraft.name} at {squadron.location.name}. Pilot client count: {flight.client_count}"
                )

                package.add_flight(flight)
                flight.state = WaitingForStart(
                    flight, self.game.settings, self.game.conditions.start_time
                )
                ato.add_package(package)

        return

    def initialize_pretense_data_structures(self, cp: ControlPoint) -> None:
        """
        Ensures that the data structures used to pass flight group information
        to the Pretense init script lua are initialized for use in
        PretenseFlightGroupSpawner and PretenseLuaGenerator.

        Args:
            cp: Control point to generate aircraft for.
            flight: The current flight being generated.
        """
        cp_name_trimmed = "".join([i for i in cp.name.lower() if i.isalnum()])

        for side in range(1, 3):
            if cp_name_trimmed not in cp.coalition.game.pretense_air[side]:
                cp.coalition.game.pretense_air[side][cp_name_trimmed] = {}
                print(
                    f"Populated flight.coalition.game.pretense_air[{side}][{cp_name_trimmed}]"
                )
        return

    def initialize_pretense_data_structures_for_flight(
        self, cp: ControlPoint, flight: Flight
    ) -> None:
        """
        Ensures that the data structures used to pass flight group information
        to the Pretense init script lua are initialized for use in
        PretenseFlightGroupSpawner and PretenseLuaGenerator.

        Args:
            cp: Control point to generate aircraft for.
            flight: The current flight being generated.
        """
        flight_type = flight.flight_type.name
        cp_name_trimmed = "".join([i for i in cp.name.lower() if i.isalnum()])

        for side in range(1, 3):
            if cp_name_trimmed not in flight.coalition.game.pretense_air[side]:
                flight.coalition.game.pretense_air[side][cp_name_trimmed] = {}
                print(
                    f"Populated flight.coalition.game.pretense_air[{side}][{cp_name_trimmed}]"
                )
            if (
                flight_type
                not in flight.coalition.game.pretense_air[side][cp_name_trimmed]
            ):
                flight.coalition.game.pretense_air[side][cp_name_trimmed][
                    flight_type
                ] = list()
                print(
                    f"Populated flight.coalition.game.pretense_air[{side}][{cp_name_trimmed}][{flight_type}]"
                )
        return

    def generate_flights(
        self,
        country: Country,
        cp: ControlPoint,
        ato: AirTaskingOrder,
    ) -> None:
        """Adds aircraft to the mission for every flight in the ATO.

        Args:
            country: The country from the mission to use for this ATO.
            cp: Control point to generate aircraft for.
            ato: The ATO to generate aircraft for.
            dynamic_runways: Runway data for carriers and FARPs.
        """
        self.initialize_pretense_data_structures(cp)

        is_player = True
        if country == cp.coalition.faction.country:
            offmap_transport_cp = self.find_pretense_cargo_plane_cp(cp)

            (
                autogenerate_transport_helicopter_squadron,
                autogenerate_cargo_plane_squadron,
            ) = self.should_generate_pretense_transports(cp.coalition.air_wing)

            if autogenerate_transport_helicopter_squadron:
                self.generate_pretense_squadron(
                    offmap_transport_cp,
                    offmap_transport_cp.coalition,
                    FlightType.AIR_ASSAULT,
                    False,
                    PRETENSE_SQUADRON_DEF_RETRIES,
                )
            if autogenerate_cargo_plane_squadron:
                self.generate_pretense_squadron(
                    offmap_transport_cp,
                    offmap_transport_cp.coalition,
                    FlightType.TRANSPORT,
                    True,
                    PRETENSE_SQUADRON_DEF_RETRIES,
                )

            self.generate_pretense_aircraft(cp, ato)
        else:
            coalition = (
                self.game.coalition_for(is_player)
                if country == self.game.coalition_for(is_player).faction.country
                else self.game.coalition_for(False)
            )
            self.generate_pretense_aircraft_for_other_side(cp, coalition, ato)

        if country == self.game.coalition_for(is_player).faction.country:
            if not isinstance(cp, OffMapSpawn):
                coalition = self.game.coalition_for(is_player)
                self.generate_pretense_aircraft_for_players(cp, coalition, ato)

        self._reserve_frequencies_and_tacan(ato)

    def generate_packages(
        self,
        country: Country,
        ato: AirTaskingOrder,
        dynamic_runways: Dict[str, RunwayData],
    ) -> None:
        for package in reversed(sorted(ato.packages, key=lambda x: x.time_over_target)):
            logging.info(f"Generating package for target: {package.target.name}")
            if not package.flights:
                continue
            for flight in package.flights:
                self.initialize_pretense_data_structures_for_flight(
                    flight.departure, flight
                )

                if flight.alive:
                    if not flight.squadron.location.runway_is_operational():
                        logging.warning(
                            f"Runway not operational, skipping flight: {flight.flight_type}"
                        )
                        flight.return_pilots_and_aircraft()
                        continue
                    logging.info(
                        f"Generating flight: {flight.unit_type} for {flight.flight_type.name}"
                    )
                    try:
                        group = self.create_and_configure_flight(
                            flight, country, dynamic_runways
                        )
                    except NoParkingSlotError:
                        return
                    self.unit_map.add_aircraft(group, flight)

    def create_and_configure_flight(
        self, flight: Flight, country: Country, dynamic_runways: Dict[str, RunwayData]
    ) -> FlyingGroup[Any]:
        from game.pretense.pretenseflightgroupspawner import PretenseFlightGroupSpawner

        """Creates and configures the flight group in the mission."""
        if not country.unused_onboard_numbers:
            country.reset_onboard_numbers()
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
        else:
            if flight.client_count > 0:
                if flight.flight_type == FlightType.CAS:
                    for conflict in self.game.theater.conflicts():
                        flight.package.target = conflict
                        break
                elif (
                    flight.flight_type == FlightType.STRIKE
                    or flight.flight_type == FlightType.BAI
                ):
                    for cp in self.game.theater.closest_opposing_control_points():
                        if cp.coalition == flight.coalition:
                            continue
                        for mission_target in cp.ground_objects:
                            flight.package.target = mission_target
                elif (
                    flight.flight_type == FlightType.OCA_RUNWAY
                    or flight.flight_type == FlightType.OCA_AIRCRAFT
                ):
                    for cp in self.game.theater.controlpoints:
                        if cp.coalition == flight.coalition or not isinstance(
                            cp, Airfield
                        ):
                            continue
                        flight.package.target = cp
                elif flight.flight_type == FlightType.DEAD:
                    for cp in self.game.theater.controlpoints:
                        if cp.coalition == flight.coalition:
                            continue
                        for ground_object in cp.ground_objects:
                            is_ewr = isinstance(ground_object, EwrGroundObject)
                            is_sam = isinstance(ground_object, SamGroundObject)

                            if is_ewr or is_sam:
                                flight.package.target = ground_object
                elif flight.flight_type == FlightType.AIR_ASSAULT:
                    for cp in self.game.theater.closest_opposing_control_points():
                        if cp.coalition == flight.coalition:
                            continue
                        if flight.is_hercules:
                            if cp.coalition == flight.coalition or not isinstance(
                                cp, Airfield
                            ):
                                continue
                        flight.package.target = cp

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
                # for unit in group.units:
                #     unit.set_client()

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
