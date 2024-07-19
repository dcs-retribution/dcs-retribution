from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, cast

import dcs.lua
from dcs import Mission, Point
from dcs.coalition import Coalition
from dcs.countries import country_dict
from dcs.task import OptReactOnThreat
from dcs.terrain import Airport
from dcs.unit import Static

from game.atcdata import AtcData
from game.dcs.beacons import Beacons
from game.dcs.helpers import unit_type_from_name
from game.missiongenerator.aircraft.aircraftgenerator import (
    AircraftGenerator,
)
from game.naming import namegen
from game.radio.radios import RadioFrequency, RadioRegistry, MHz
from game.radio.tacan import TacanRegistry
from game.theater import Airfield
from game.theater.bullseye import Bullseye
from game.unitmap import UnitMap
from .briefinggenerator import BriefingGenerator, MissionInfoGenerator
from .cargoshipgenerator import CargoShipGenerator
from .convoygenerator import ConvoyGenerator
from .drawingsgenerator import DrawingsGenerator
from .environmentgenerator import EnvironmentGenerator
from .flotgenerator import FlotGenerator
from .forcedoptionsgenerator import ForcedOptionsGenerator
from .frontlineconflictdescription import FrontLineConflictDescription
from .kneeboard import KneeboardGenerator
from .luagenerator import LuaGenerator
from .missiondata import MissionData
from .tgogenerator import TgoGenerator
from .triggergenerator import TriggerGenerator
from .visualsgenerator import VisualsGenerator
from ..radio.TacanContainer import TacanContainer

if TYPE_CHECKING:
    from game import Game


class MissionGenerator:
    def __init__(self, game: Game, time: datetime) -> None:
        self.game = game
        self.time = time
        self.mission = Mission(game.theater.terrain)
        self.unit_map = UnitMap()

        self.mission_data = MissionData()

        self.radio_registry = RadioRegistry()
        self.tacan_registry = TacanRegistry()

        self.generation_started = False

        self.p_country = country_dict[self.game.blue.faction.country.id]()
        self.e_country = country_dict[self.game.red.faction.country.id]()

        with open("resources/default_options.lua", "r", encoding="utf-8") as f:
            options = dcs.lua.loads(f.read())["options"]
            ext_view = game.settings.external_views_allowed
            options["miscellaneous"]["f11_free_camera"] = ext_view
            options["miscellaneous"]["f5_nearest_ac"] = ext_view
            options["difficulty"]["spectatorExternalViews"] = ext_view
            self.mission.options.load_from_dict(options)

    def generate_miz(self, output: Path) -> UnitMap:
        if self.generation_started:
            raise RuntimeError(
                "Mission has already begun generating. To reset, create a new "
                "MissionSimulation."
            )
        self.generation_started = True

        self.setup_mission_coalitions()
        self.add_airfields_to_unit_map()
        self.initialize_registries()

        EnvironmentGenerator(self.mission, self.game.conditions, self.time).generate()

        tgo_generator = TgoGenerator(
            self.mission,
            self.game,
            self.radio_registry,
            self.tacan_registry,
            self.unit_map,
            self.mission_data,
        )
        tgo_generator.generate()

        ConvoyGenerator(self.mission, self.game, self.unit_map).generate()
        CargoShipGenerator(self.mission, self.game, self.unit_map).generate()

        self.generate_destroyed_units()

        # Generate ground conflicts first so the JTACs get the first laser code (1688)
        # rather than the first player flight with a TGP.
        self.generate_ground_conflicts()
        self.generate_air_units(tgo_generator)

        TriggerGenerator(self.mission, self.game).generate()
        ForcedOptionsGenerator(self.mission, self.game).generate()
        VisualsGenerator(self.mission, self.game).generate()
        LuaGenerator(self.game, self.mission, self.mission_data).generate()
        DrawingsGenerator(self.mission, self.game).generate()

        self.setup_combined_arms()

        self.notify_info_generators()

        namegen.reset_numbers()
        self.generate_warehouses()
        self.mission.save(output)

        return self.unit_map

    @staticmethod
    def _configure_ewrj(gen: AircraftGenerator) -> None:
        for groups in gen.ewrj_package_dict.values():
            optrot = [
                task
                for task in groups[0].points[0].tasks
                if isinstance(task, OptReactOnThreat)
            ][0]
            assert isinstance(optrot, OptReactOnThreat)
            if (
                len(groups) == 1
                and optrot.value != OptReactOnThreat.Values.PassiveDefense
            ):
                # primary flight with no EWR-Jamming capability
                continue
            for group in groups:
                tasks = group.points[0].tasks
                for i in range(len(tasks)):
                    if isinstance(tasks[i], OptReactOnThreat):
                        tasks[i] = OptReactOnThreat(
                            OptReactOnThreat.Values.PassiveDefense
                        )
                        break

    def setup_mission_coalitions(self) -> None:
        self.mission.coalition["blue"] = Coalition(
            "blue", bullseye=self.game.blue.bullseye.to_pydcs()
        )
        self.mission.coalition["red"] = Coalition(
            "red", bullseye=self.game.red.bullseye.to_pydcs()
        )
        self.mission.coalition["neutrals"] = Coalition(
            "neutrals", bullseye=Bullseye(Point(0, 0, self.mission.terrain)).to_pydcs()
        )

        self.mission.coalition["blue"].add_country(self.p_country)
        self.mission.coalition["red"].add_country(self.e_country)

        belligerents = {self.p_country.id, self.e_country.id}
        for country_id in country_dict.keys():
            if country_id not in belligerents:
                c = country_dict[country_id]()
                self.mission.coalition["neutrals"].add_country(c)

    def add_airfields_to_unit_map(self) -> None:
        for control_point in self.game.theater.controlpoints:
            if isinstance(control_point, Airfield):
                self.unit_map.add_airfield(control_point)

    def initialize_registries(self) -> None:
        unique_map_frequencies: set[RadioFrequency] = set()
        self.initialize_tacan_registry(unique_map_frequencies)
        self.initialize_radio_registry(unique_map_frequencies)
        # Allocate UHF/VHF Guard Freq first!
        unique_map_frequencies.add(MHz(243))
        unique_map_frequencies.add(MHz(121, 500))
        for frequency in unique_map_frequencies:
            self.radio_registry.reserve(frequency)

    def initialize_tacan_registry(
        self, unique_map_frequencies: set[RadioFrequency]
    ) -> None:
        """
        Dedup beacon/radio frequencies, since some maps have some frequencies
        used multiple times.
        """
        for beacon in Beacons.iter_theater(self.game.theater):
            unique_map_frequencies.add(beacon.frequency)
            if beacon.is_tacan:
                if beacon.channel is None:
                    logging.warning(f"TACAN beacon has no channel: {beacon.callsign}")
                else:
                    self.tacan_registry.mark_unavailable(beacon.tacan_channel)
        for cp in self.game.theater.controlpoints:
            if isinstance(cp, TacanContainer) and cp.tacan is not None:
                self.tacan_registry.mark_unavailable(cp.tacan)

    def initialize_radio_registry(
        self, unique_map_frequencies: set[RadioFrequency]
    ) -> None:
        for airport in self.game.theater.terrain.airport_list():
            if (atc := AtcData.from_pydcs(airport)) is not None:
                unique_map_frequencies.add(atc.hf)
                unique_map_frequencies.add(atc.vhf_fm)
                unique_map_frequencies.add(atc.vhf_am)
                unique_map_frequencies.add(atc.uhf)
                # No need to reserve ILS or TACAN because those are in the
                # beacon list.

    def generate_ground_conflicts(self) -> None:
        """Generate FLOTs and JTACs for each active front line."""
        for front_line in self.game.theater.conflicts():
            player_cp = front_line.blue_cp
            enemy_cp = front_line.red_cp
            conflict = FrontLineConflictDescription.frontline_cas_conflict(
                front_line, self.game.theater
            )
            # Generate frontline ops
            player_gp = self.game.ground_planners[player_cp.id].units_per_cp[
                enemy_cp.id
            ]
            enemy_gp = self.game.ground_planners[enemy_cp.id].units_per_cp[player_cp.id]
            ground_conflict_gen = FlotGenerator(
                self.mission,
                conflict,
                self.game,
                player_gp,
                enemy_gp,
                player_cp.stances[enemy_cp.id],
                enemy_cp.stances[player_cp.id],
                self.unit_map,
                self.radio_registry,
                self.mission_data,
            )
            ground_conflict_gen.generate()

    def generate_air_units(self, tgo_generator: TgoGenerator) -> None:
        """Generate the air units for the Operation"""

        # Generate Aircraft Activity on the map
        aircraft_generator = AircraftGenerator(
            self.mission,
            self.game.settings,
            self.game,
            self.time,
            self.radio_registry,
            self.tacan_registry,
            self.unit_map,
            mission_data=self.mission_data,
            helipads=tgo_generator.helipads,
            ground_spawns_roadbase=tgo_generator.ground_spawns_roadbase,
            ground_spawns_large=tgo_generator.ground_spawns_large,
            ground_spawns=tgo_generator.ground_spawns,
        )

        aircraft_generator.clear_parking_slots()

        aircraft_generator.generate_flights(
            self.p_country,
            self.game.blue.ato,
            tgo_generator.runways,
        )
        aircraft_generator.generate_flights(
            self.e_country,
            self.game.red.ato,
            tgo_generator.runways,
        )
        aircraft_generator.spawn_unused_aircraft(
            self.p_country,
            self.e_country,
        )

        self.mission_data.flights = aircraft_generator.flights

        for flight in aircraft_generator.flights:
            if not flight.client_units:
                continue
            flight.aircraft_type.assign_channels_for_flight(flight, self.mission_data)

        if self.game.settings.plugins.get("ewrj"):
            self._configure_ewrj(aircraft_generator)

    def generate_destroyed_units(self) -> None:
        """Add destroyed units to the Mission"""
        if not self.game.settings.perf_destroyed_units:
            return

        for d in self.game.get_destroyed_units():
            try:
                type_name = d["type"]
                if not isinstance(type_name, str):
                    raise TypeError(
                        "Expected the type of the destroyed static to be a string"
                    )
                utype = unit_type_from_name(type_name)
            except KeyError:
                logging.warning(f"Destroyed unit has no type: {d}")
                continue

            pos = Point(cast(float, d["x"]), cast(float, d["z"]), self.mission.terrain)
            if utype is not None and not self.game.position_culled(pos):
                self.mission.static_group(
                    country=self.p_country,
                    name="",
                    _type=utype,
                    hidden=True,
                    position=pos,
                    heading=d["orientation"],
                    dead=True,
                )

    def notify_info_generators(
        self,
    ) -> None:
        """Generates subscribed MissionInfoGenerator objects."""
        mission_data = self.mission_data
        gens: list[MissionInfoGenerator] = [
            KneeboardGenerator(self.mission, self.game),
            BriefingGenerator(self.mission, self.game),
        ]
        for gen in gens:
            for dynamic_runway in mission_data.runways:
                gen.add_dynamic_runway(dynamic_runway)

            for tanker in mission_data.tankers:
                if tanker.blue:
                    gen.add_tanker(tanker)

            for aewc in mission_data.awacs:
                if aewc.blue:
                    gen.add_awacs(aewc)

            for jtac in mission_data.jtacs:
                if jtac.blue:
                    gen.add_jtac(jtac)

            for flight in mission_data.flights:
                gen.add_flight(flight)
            gen.generate()

    def setup_combined_arms(self) -> None:
        settings = self.game.settings
        commanders = settings.tactical_commander_count
        self.mission.groundControl.pilot_can_control_vehicles = commanders > 0

        self.mission.groundControl.blue_game_masters = settings.game_masters_count
        self.mission.groundControl.blue_tactical_commander = commanders
        self.mission.groundControl.blue_jtac = settings.jtac_count
        self.mission.groundControl.blue_observer = settings.observer_count

    def generate_warehouses(self) -> None:
        settings = self.game.settings
        for tmu in self.unit_map.theater_objects.values():
            if (
                tmu.theater_unit.is_ship
                or
                isinstance(tmu.dcs_unit, Static)
                and tmu.dcs_unit.category in ["Warehouses", "Heliports"]
            ):
                # We'll serialize more than is actually necessary
                # DCS will filter out warehouses as dynamic spawns so no need to worry there
                # thus, if we serialize a ship as a warehouse that's not supported, DCS will filter it out
                warehouse = Airport(
                    tmu.theater_unit.position,
                    self.mission.terrain,
                ).dict()
                warehouse["coalition"] = "blue" if tmu.theater_unit.ground_object.coalition.player else "red"
                warehouse["dynamicCargo"] = settings.dynamic_cargo
                if tmu.theater_unit.is_ship or tmu.dcs_unit.category == "Heliports":  # type: ignore
                    warehouse["dynamicSpawn"] = settings.dynamic_slots
                    warehouse["allowHotStart"] = settings.dynamic_slots_hot
                self.mission.warehouses.warehouses[tmu.dcs_unit.id] = warehouse

        # configure dynamic spawn, hot start of DS & dynamic cargo for airfields
        for ap in self.mission.terrain.airports.values():
            ap.dynamic_spawn = settings.dynamic_slots
            ap.allow_hot_start = settings.dynamic_slots_hot
            ap.dynamic_cargo = settings.dynamic_cargo
