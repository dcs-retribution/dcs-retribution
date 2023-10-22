from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

import dcs.lua
from dcs import Mission, Point
from dcs.coalition import Coalition
from dcs.countries import (
    country_dict,
    CombinedJointTaskForcesBlue,
    CombinedJointTaskForcesRed,
)

from game.lasercodes.lasercoderegistry import LaserCodeRegistry
from game.missiongenerator.convoygenerator import ConvoyGenerator
from game.missiongenerator.environmentgenerator import EnvironmentGenerator
from game.missiongenerator.flotgenerator import FlotGenerator
from game.missiongenerator.forcedoptionsgenerator import ForcedOptionsGenerator
from game.missiongenerator.frontlineconflictdescription import (
    FrontLineConflictDescription,
)
from game.missiongenerator.missiondata import MissionData
from game.missiongenerator.tgogenerator import TgoGenerator
from game.missiongenerator.visualsgenerator import VisualsGenerator
from game.naming import namegen
from game.pretense.pretenseaircraftgenerator import PretenseAircraftGenerator
from game.radio.radios import RadioRegistry
from game.radio.tacan import TacanRegistry
from game.theater.bullseye import Bullseye
from game.unitmap import UnitMap
from .pretenseluagenerator import PretenseLuaGenerator
from .pretensetgogenerator import PretenseTgoGenerator
from .pretensetriggergenerator import PretenseTriggerGenerator
from ..ato.airtaaskingorder import AirTaskingOrder
from ..missiongenerator import MissionGenerator

if TYPE_CHECKING:
    from game import Game


class PretenseMissionGenerator(MissionGenerator):
    def __init__(self, game: Game, time: datetime) -> None:
        super().__init__(game, time)
        self.game = game
        self.time = time
        self.mission = Mission(game.theater.terrain)
        self.unit_map = UnitMap()

        self.mission_data = MissionData()

        self.laser_code_registry = LaserCodeRegistry()
        self.radio_registry = RadioRegistry()
        self.tacan_registry = TacanRegistry()

        self.generation_started = False

        self.p_country = country_dict[self.game.blue.faction.country.id]()
        self.e_country = country_dict[self.game.red.faction.country.id]()

        with open("resources/default_options.lua", "r", encoding="utf-8") as f:
            options = dcs.lua.loads(f.read())["options"]
            ext_view = game.settings.external_views_allowed
            options["miscellaneous"]["f11_free_camera"] = ext_view
            options["difficulty"]["spectatorExternalViews"] = ext_view
            self.mission.options.load_from_dict(options)

    def generate_miz(self, output: Path) -> UnitMap:
        if self.generation_started:
            raise RuntimeError(
                "Mission has already begun generating. To reset, create a new "
                "MissionSimulation."
            )
        self.generation_started = True

        self.game.pretense_ground_supply = {1: {}, 2: {}}
        self.game.pretense_ground_assault = {1: {}, 2: {}}
        self.game.pretense_air = {1: {}, 2: {}}

        self.setup_mission_coalitions()
        self.add_airfields_to_unit_map()
        self.initialize_registries()

        EnvironmentGenerator(self.mission, self.game.conditions, self.time).generate()

        tgo_generator = PretenseTgoGenerator(
            self.mission,
            self.game,
            self.radio_registry,
            self.tacan_registry,
            self.unit_map,
            self.mission_data,
        )
        tgo_generator.generate()

        ConvoyGenerator(self.mission, self.game, self.unit_map).generate()

        # Generate ground conflicts first so the JTACs get the first laser code (1688)
        # rather than the first player flight with a TGP.
        self.generate_ground_conflicts()
        self.generate_air_units(tgo_generator)

        self.mission.triggerrules.triggers.clear()
        PretenseTriggerGenerator(self.mission, self.game).generate()
        ForcedOptionsGenerator(self.mission, self.game).generate()
        VisualsGenerator(self.mission, self.game).generate()
        PretenseLuaGenerator(self.game, self.mission, self.mission_data).generate()

        self.setup_combined_arms()

        self.notify_info_generators()

        # TODO: Shouldn't this be first?
        namegen.reset_numbers()
        self.mission.save(output)

        return self.unit_map

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

        # Add CJTF factions to the coalitions, if they're not being used in the campaign
        if CombinedJointTaskForcesBlue not in {self.p_country, self.e_country}:
            self.mission.coalition["blue"].add_country(CombinedJointTaskForcesBlue())
        if CombinedJointTaskForcesRed not in {self.p_country, self.e_country}:
            self.mission.coalition["red"].add_country(CombinedJointTaskForcesRed())

        belligerents = {self.p_country.id, self.e_country.id}
        for country_id in country_dict.keys():
            if country_id not in belligerents:
                c = country_dict[country_id]()
                self.mission.coalition["neutrals"].add_country(c)

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
        aircraft_generator = PretenseAircraftGenerator(
            self.mission,
            self.game.settings,
            self.game,
            self.time,
            self.radio_registry,
            self.tacan_registry,
            self.laser_code_registry,
            self.unit_map,
            mission_data=self.mission_data,
            helipads=tgo_generator.helipads,
            ground_spawns_roadbase=tgo_generator.ground_spawns_roadbase,
            ground_spawns=tgo_generator.ground_spawns,
        )

        # Clear parking slots and ATOs
        aircraft_generator.clear_parking_slots()
        self.game.blue.ato.clear()
        self.game.red.ato.clear()

        for cp in self.game.theater.controlpoints:
            for country in (self.p_country, self.e_country):
                ato = AirTaskingOrder()
                aircraft_generator.generate_flights(
                    country,
                    cp,
                    ato,
                )
                aircraft_generator.generate_packages(
                    country,
                    ato,
                    tgo_generator.runways,
                )

        self.mission_data.flights = aircraft_generator.flights

        for flight in aircraft_generator.flights:
            if not flight.client_units:
                continue
            flight.aircraft_type.assign_channels_for_flight(flight, self.mission_data)
