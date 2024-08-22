from __future__ import annotations

import logging
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
from game.missiongenerator.missiondata import MissionData
from game.radio.radios import RadioRegistry
from game.radio.tacan import TacanRegistry
from game.runways import RunwayData
from game.settings import Settings
from game.theater.controlpoint import (
    Airfield,
    ControlPoint,
    Fob,
)
from game.unitmap import UnitMap
from .aircraftpainter import AircraftPainter
from .flightdata import FlightData
from .flightgroupconfigurator import FlightGroupConfigurator
from .flightgroupspawner import FlightGroupSpawner
from ...data.weapons import WeaponType

if TYPE_CHECKING:
    from game import Game
    from game.squadrons import Squadron


class AircraftGenerator:
    def __init__(
        self,
        mission: Mission,
        settings: Settings,
        game: Game,
        time: datetime,
        radio_registry: RadioRegistry,
        tacan_registry: TacanRegistry,
        unit_map: UnitMap,
        mission_data: MissionData,
        helipads: dict[ControlPoint, list[StaticGroup]],
        ground_spawns_roadbase: dict[ControlPoint, list[Tuple[StaticGroup, Point]]],
        ground_spawns_large: dict[ControlPoint, list[Tuple[StaticGroup, Point]]],
        ground_spawns: dict[ControlPoint, list[Tuple[StaticGroup, Point]]],
    ) -> None:
        self.mission = mission
        self.settings = settings
        self.game = game
        self.time = time
        self.radio_registry = radio_registry
        self.tacan_registy = tacan_registry
        self.unit_map = unit_map
        self.flights: List[FlightData] = []
        self.mission_data = mission_data
        self.helipads = helipads
        self.ground_spawns_roadbase = ground_spawns_roadbase
        self.ground_spawns_large = ground_spawns_large
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
        self._reserve_frequencies_and_tacan(ato)

        for package in reversed(sorted(ato.packages, key=lambda x: x.time_over_target)):
            logging.info(f"Generating package for target: {package.target.name}")
            if not package.flights:
                continue
            for flight in package.flights:
                if flight.alive and not isinstance(flight.state, Completed):
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
            if (
                package.primary_flight is not None
                and package.primary_flight.flight_plan.is_formation(
                    package.primary_flight.flight_plan
                )
            ):
                splittrigger = TriggerOnce(Event.NoEvent, f"Split-{id(package)}")
                splittrigger.add_condition(FlagIsTrue(flag=f"split-{id(package)}"))
                splittrigger.add_condition(Or())
                splittrigger.add_condition(FlagIsFalse(flag=f"split-{id(package)}"))
                splittrigger.add_condition(GroupDead(package.primary_flight.group_id))
                for flight in package.flights:
                    if flight.flight_type in [
                        FlightType.ESCORT,
                        FlightType.SEAD_ESCORT,
                    ]:
                        splittrigger.add_action(AITaskPush(flight.group_id, 1))
                if len(splittrigger.actions) > 0:
                    self.mission.triggerrules.triggers.append(splittrigger)

    def spawn_unused_aircraft(
        self, player_country: Country, enemy_country: Country
    ) -> None:
        for control_point in self.game.theater.controlpoints:
            if not (
                isinstance(control_point, Airfield) or isinstance(control_point, Fob)
            ):
                continue

            if control_point.captured:
                country = player_country
            else:
                country = enemy_country

            for squadron in control_point.squadrons:
                try:
                    self._spawn_unused_for(squadron, country)
                except NoParkingSlotError:
                    # If we run out of parking, stop spawning aircraft at this base.
                    break

    def _spawn_unused_for(self, squadron: Squadron, country: Country) -> None:
        assert isinstance(squadron.location, Airfield) or isinstance(
            squadron.location, Fob
        )
        if (
            squadron.coalition.player
            and self.game.settings.perf_disable_untasked_blufor_aircraft
        ):
            return
        elif (
            not squadron.coalition.player
            and self.game.settings.perf_disable_untasked_opfor_aircraft
        ):
            return

        for _ in range(squadron.untasked_aircraft):
            # Creating a flight even those this isn't a fragged mission lets us
            # reuse the existing debriefing code.
            # TODO: Special flight type?
            flight = Flight(
                Package(squadron.location, self.game.db.flights),
                squadron,
                1,
                FlightType.BARCAP,
                StartType.COLD,
                divert=None,
                claim_inv=False,
            )
            flight.state = Completed(flight, self.game.settings)

            group = FlightGroupSpawner(
                flight,
                country,
                self.mission,
                self.helipads,
                self.ground_spawns_roadbase,
                self.ground_spawns_large,
                self.ground_spawns,
                self.mission_data,
            ).create_idle_aircraft()
            if group:
                if (
                    not squadron.coalition.player
                    and squadron.aircraft.flyable
                    and (
                        self.game.settings.enable_squadron_pilot_limits
                        or squadron.number_of_available_pilots > 0
                    )
                    and self.game.settings.untasked_opfor_client_slots
                ):
                    flight.state = WaitingForStart(
                        flight, self.game.settings, self.game.conditions.start_time
                    )
                    group.uncontrolled = False
                    group.units[0].skill = Skill.Client
                AircraftPainter(flight, group).apply_livery()
                self.unit_map.add_aircraft(group, flight)

    def create_and_configure_flight(
        self, flight: Flight, country: Country, dynamic_runways: Dict[str, RunwayData]
    ) -> FlyingGroup[Any]:
        """Creates and configures the flight group in the mission."""
        group = FlightGroupSpawner(
            flight,
            country,
            self.mission,
            self.helipads,
            self.ground_spawns_roadbase,
            self.ground_spawns_large,
            self.ground_spawns,
            self.mission_data,
        ).create_flight_group()
        self.flights.append(
            FlightGroupConfigurator(
                flight,
                group,
                self.game,
                self.mission,
                self.time,
                self.radio_registry,
                self.tacan_registy,
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
                or flight.any_member_has_weapon_of_type(WeaponType.JAMMER)
            )
        ):
            self.ewrj_package_dict[id(flight.package)].append(group)

    def _reserve_frequencies_and_tacan(self, ato: AirTaskingOrder) -> None:
        for package in ato.packages:
            pfreq = package.frequency
            if pfreq and pfreq not in self.radio_registry.allocated_channels:
                self.radio_registry.reserve(pfreq)
            for f in package.flights:
                if (
                    f.frequency
                    and f.frequency not in self.radio_registry.allocated_channels
                ):
                    self.radio_registry.reserve(f.frequency)
                if f.tacan and f.tacan not in self.tacan_registy.allocated_channels:
                    self.tacan_registy.mark_unavailable(f.tacan)
