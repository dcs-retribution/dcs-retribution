"""Generators for creating the groups for ground objectives.

The classes in this file are responsible for creating the vehicle groups, ship
groups, statics, missile sites, and AA sites for the mission. Each of these
objectives is defined in the Theater by a TheaterGroundObject. These classes
create the pydcs groups and statics for those areas and add them to the mission.
"""
from __future__ import annotations

import logging
import random
from collections import defaultdict
from typing import Any, Dict, Iterator, List, Optional, TYPE_CHECKING, Type, Tuple

import dcs.vehicles
from dcs import Mission, Point, unitgroup
from dcs.action import DoScript, SceneryDestructionZone
from dcs.condition import MapObjectIsDead
from dcs.countries import *
from dcs.country import Country
from dcs.point import StaticPoint, PointAction
from dcs.ships import (
    CVN_71,
    CVN_72,
    CVN_73,
    CVN_75,
    Stennis,
    Forrestal,
    LHA_Tarawa,
)
from dcs.statics import Fortification
from dcs.task import (
    ActivateBeaconCommand,
    ActivateICLSCommand,
    ActivateLink4Command,
    ActivateACLSCommand,
    EPLRS,
    FireAtPoint,
    OptAlarmState,
)
from dcs.translation import String
from dcs.triggers import Event, TriggerOnce, TriggerStart, TriggerZone
from dcs.unit import Unit, InvisibleFARP, BaseFARP, SingleHeliPad, FARP
from dcs.unitgroup import MovingGroup, ShipGroup, StaticGroup, VehicleGroup
from dcs.unittype import ShipType, VehicleType
from dcs.vehicles import vehicle_map, Unarmed

from game.data.units import UnitClass
from game.dcs.groundunittype import GroundUnitType
from game.missiongenerator.groundforcepainter import (
    NavalForcePainter,
    GroundForcePainter,
)
from game.missiongenerator.missiondata import CarrierInfo, MissionData
from game.missiongenerator.tgogenerator import (
    TgoGenerator,
    HelipadGenerator,
    GroundSpawnRoadbaseGenerator,
    GroundSpawnGenerator,
    GroundObjectGenerator,
    CarrierGenerator,
    LhaGenerator,
    MissileSiteGenerator,
)
from game.point_with_heading import PointWithHeading
from game.radio.RadioFrequencyContainer import RadioFrequencyContainer
from game.radio.radios import RadioFrequency, RadioRegistry
from game.radio.tacan import TacanBand, TacanChannel, TacanRegistry, TacanUsage
from game.runways import RunwayData
from game.theater import (
    ControlPoint,
    TheaterGroundObject,
    TheaterUnit,
    NavalControlPoint,
    PresetLocation,
)
from game.theater.theatergroundobject import (
    CarrierGroundObject,
    GenericCarrierGroundObject,
    LhaGroundObject,
    MissileSiteGroundObject,
    BuildingGroundObject,
    VehicleGroupGroundObject,
)
from game.theater.theatergroup import SceneryUnit, IadsGroundGroup, TheaterGroup
from game.unitmap import UnitMap
from game.utils import Heading, feet, knots, mps

if TYPE_CHECKING:
    from game import Game

FARP_FRONTLINE_DISTANCE = 10000
AA_CP_MIN_DISTANCE = 40000
PRETENSE_GROUND_UNIT_GROUP_SIZE = 4


class PretenseGroundObjectGenerator(GroundObjectGenerator):
    """generates the DCS groups and units from the TheaterGroundObject"""

    def __init__(
        self,
        ground_object: TheaterGroundObject,
        country: Country,
        game: Game,
        mission: Mission,
        unit_map: UnitMap,
    ) -> None:
        super().__init__(
            ground_object,
            country,
            game,
            mission,
            unit_map,
        )

        self.ground_object = ground_object
        self.country = country
        self.game = game
        self.m = mission
        self.unit_map = unit_map

    @property
    def culled(self) -> bool:
        return self.game.iads_considerate_culling(self.ground_object)

    def ground_unit_of_class(self, unit_class: UnitClass) -> Optional[GroundUnitType]:
        faction_units = (
            set(self.ground_object.coalition.faction.frontline_units)
            | set(self.ground_object.coalition.faction.artillery_units)
            | set(self.ground_object.coalition.faction.logistics_units)
        )
        of_class = list({u for u in faction_units if u.unit_class is unit_class})

        if len(of_class) > 0:
            return random.choice(of_class)
        else:
            return None

    def generate_ground_unit_of_class(
        self,
        unit_class: UnitClass,
        group: TheaterGroup,
        vehicle_units: list[TheaterUnit],
        cp_name: str,
        group_role: str,
        max_num: int,
    ) -> None:
        if self.ground_object.coalition.faction.has_access_to_unit_class(unit_class):
            unit_type = self.ground_unit_of_class(unit_class)
            if unit_type is not None and len(vehicle_units) < max_num:
                unit_id = self.game.next_unit_id()
                unit_name = f"{cp_name}-{group_role}-{unit_id}"

                spread_out_heading = random.randrange(1, 360)
                spread_out_position = group.position.point_from_heading(
                    spread_out_heading, 30
                )
                ground_unit_pos = PointWithHeading.from_point(
                    spread_out_position, group.position.heading
                )

                theater_unit = TheaterUnit(
                    unit_id,
                    unit_name,
                    unit_type.dcs_unit_type,
                    ground_unit_pos,
                    group.ground_object,
                )
                vehicle_units.append(theater_unit)

    def generate(self) -> None:
        if self.culled:
            return
        cp_name_trimmed = "".join(
            [i for i in self.ground_object.control_point.name.lower() if i.isalnum()]
        )

        for group in self.ground_object.groups:
            vehicle_units: list[TheaterUnit] = []
            ship_units: list[TheaterUnit] = []
            # Split the different unit types to be compliant to dcs limitation
            for unit in group.units:
                if unit.is_static:
                    # Add supply convoy
                    group_role = "supply"
                    group_name = f"{cp_name_trimmed}-{group_role}-{group.id}"
                    group.name = group_name

                    self.generate_ground_unit_of_class(
                        UnitClass.LOGISTICS,
                        group,
                        vehicle_units,
                        cp_name_trimmed,
                        group_role,
                        PRETENSE_GROUND_UNIT_GROUP_SIZE,
                    )
                elif unit.is_vehicle and unit.alive:
                    # Add armor group
                    group_role = "assault"
                    group_name = f"{cp_name_trimmed}-{group_role}-{group.id}"
                    group.name = group_name

                    self.generate_ground_unit_of_class(
                        UnitClass.TANK,
                        group,
                        vehicle_units,
                        cp_name_trimmed,
                        group_role,
                        PRETENSE_GROUND_UNIT_GROUP_SIZE - 3,
                    )
                    self.generate_ground_unit_of_class(
                        UnitClass.ATGM,
                        group,
                        vehicle_units,
                        cp_name_trimmed,
                        group_role,
                        PRETENSE_GROUND_UNIT_GROUP_SIZE - 2,
                    )
                    self.generate_ground_unit_of_class(
                        UnitClass.APC,
                        group,
                        vehicle_units,
                        cp_name_trimmed,
                        group_role,
                        PRETENSE_GROUND_UNIT_GROUP_SIZE - 1,
                    )
                    self.generate_ground_unit_of_class(
                        UnitClass.IFV,
                        group,
                        vehicle_units,
                        cp_name_trimmed,
                        group_role,
                        PRETENSE_GROUND_UNIT_GROUP_SIZE,
                    )
                    self.generate_ground_unit_of_class(
                        UnitClass.ARTILLERY,
                        group,
                        vehicle_units,
                        cp_name_trimmed,
                        group_role,
                        PRETENSE_GROUND_UNIT_GROUP_SIZE,
                    )
                    self.generate_ground_unit_of_class(
                        UnitClass.RECON,
                        group,
                        vehicle_units,
                        cp_name_trimmed,
                        group_role,
                        PRETENSE_GROUND_UNIT_GROUP_SIZE,
                    )
                    if random.randrange(0, 100) > 75:
                        self.generate_ground_unit_of_class(
                            UnitClass.SHORAD,
                            group,
                            vehicle_units,
                            cp_name_trimmed,
                            group_role,
                            PRETENSE_GROUND_UNIT_GROUP_SIZE,
                        )
                elif unit.is_ship and unit.alive:
                    # All alive Ships
                    ship_units.append(unit)
            if vehicle_units:
                self.create_vehicle_group(group.group_name, vehicle_units)
            if ship_units:
                self.create_ship_group(group.group_name, ship_units)

    def create_vehicle_group(
        self, group_name: str, units: list[TheaterUnit]
    ) -> VehicleGroup:
        vehicle_group: Optional[VehicleGroup] = None

        cp_name_trimmed = "".join(
            [i for i in self.ground_object.control_point.name.lower() if i.isalnum()]
        )
        is_player = True
        side = (
            2
            if self.country == self.game.coalition_for(is_player).faction.country
            else 1
        )

        for unit in units:
            assert issubclass(unit.type, VehicleType)
            faction = unit.ground_object.control_point.coalition.faction
            if vehicle_group is None:
                vehicle_group = self.m.vehicle_group(
                    self.country,
                    group_name,
                    unit.type,
                    position=unit.position,
                    heading=unit.position.heading.degrees,
                )
                vehicle_group.units[0].player_can_drive = True
                self.enable_eplrs(vehicle_group, unit.type)
                vehicle_group.units[0].name = unit.unit_name
                self.set_alarm_state(vehicle_group)
                GroundForcePainter(faction, vehicle_group.units[0]).apply_livery()

                group_role = group_name.split("-")[1]
                if group_role == "supply":
                    self.game.pretense_ground_supply[side][cp_name_trimmed].append(
                        f"{vehicle_group.name}"
                    )
                elif group_role == "assault":
                    self.game.pretense_ground_assault[side][cp_name_trimmed].append(
                        f"{vehicle_group.name}"
                    )
            else:
                vehicle_unit = self.m.vehicle(unit.unit_name, unit.type)
                vehicle_unit.player_can_drive = True
                vehicle_unit.position = unit.position
                vehicle_unit.heading = unit.position.heading.degrees
                GroundForcePainter(faction, vehicle_unit).apply_livery()
                vehicle_group.add_unit(vehicle_unit)
            self._register_theater_unit(unit, vehicle_group.units[-1])
        if vehicle_group is None:
            raise RuntimeError(f"Error creating VehicleGroup for {group_name}")
        return vehicle_group


class PretenseTgoGenerator(TgoGenerator):
    """Creates DCS groups and statics for the theater during mission generation.

    Most of the work of group/static generation is delegated to the other
    generator classes. This class is responsible for finding each of the
    locations for spawning ground objects, determining their types, and creating
    the appropriate generators.
    """

    def __init__(
        self,
        mission: Mission,
        game: Game,
        radio_registry: RadioRegistry,
        tacan_registry: TacanRegistry,
        unit_map: UnitMap,
        mission_data: MissionData,
    ) -> None:
        super().__init__(
            mission,
            game,
            radio_registry,
            tacan_registry,
            unit_map,
            mission_data,
        )

        self.m = mission
        self.game = game
        self.radio_registry = radio_registry
        self.tacan_registry = tacan_registry
        self.unit_map = unit_map
        self.icls_alloc = iter(range(1, 21))
        self.runways: Dict[str, RunwayData] = {}
        self.helipads: dict[ControlPoint, list[StaticGroup]] = defaultdict(list)
        self.ground_spawns_roadbase: dict[
            ControlPoint, list[Tuple[StaticGroup, Point]]
        ] = defaultdict(list)
        self.ground_spawns: dict[
            ControlPoint, list[Tuple[StaticGroup, Point]]
        ] = defaultdict(list)
        self.mission_data = mission_data

    def generate(self) -> None:
        for cp in self.game.theater.controlpoints:
            cp_name_trimmed = "".join([i for i in cp.name.lower() if i.isalnum()])
            for side in range(1, 3):
                if cp_name_trimmed not in self.game.pretense_ground_supply[side]:
                    self.game.pretense_ground_supply[side][cp_name_trimmed] = list()
                if cp_name_trimmed not in self.game.pretense_ground_assault[side]:
                    self.game.pretense_ground_assault[side][cp_name_trimmed] = list()

            # First generate units for the coalition, which initially holds this CP
            country = self.m.country(cp.coalition.faction.country.name)

            # Generate helipads
            helipad_gen = HelipadGenerator(
                self.m, cp, self.game, self.radio_registry, self.tacan_registry
            )
            helipad_gen.generate()
            self.helipads[cp] = helipad_gen.helipads

            # Generate Highway Strip slots
            ground_spawn_roadbase_gen = GroundSpawnRoadbaseGenerator(
                self.m, cp, self.game, self.radio_registry, self.tacan_registry
            )
            ground_spawn_roadbase_gen.generate()
            self.ground_spawns_roadbase[
                cp
            ] = ground_spawn_roadbase_gen.ground_spawns_roadbase
            random.shuffle(self.ground_spawns_roadbase[cp])

            # Generate STOL pads
            ground_spawn_gen = GroundSpawnGenerator(
                self.m, cp, self.game, self.radio_registry, self.tacan_registry
            )
            ground_spawn_gen.generate()
            self.ground_spawns[cp] = ground_spawn_gen.ground_spawns
            random.shuffle(self.ground_spawns[cp])

            for ground_object in cp.ground_objects:
                generator: GroundObjectGenerator
                if isinstance(ground_object, CarrierGroundObject) and isinstance(
                    cp, NavalControlPoint
                ):
                    generator = CarrierGenerator(
                        ground_object,
                        cp,
                        country,
                        self.game,
                        self.m,
                        self.radio_registry,
                        self.tacan_registry,
                        self.icls_alloc,
                        self.runways,
                        self.unit_map,
                        self.mission_data,
                    )
                elif isinstance(ground_object, LhaGroundObject) and isinstance(
                    cp, NavalControlPoint
                ):
                    generator = LhaGenerator(
                        ground_object,
                        cp,
                        country,
                        self.game,
                        self.m,
                        self.radio_registry,
                        self.tacan_registry,
                        self.icls_alloc,
                        self.runways,
                        self.unit_map,
                        self.mission_data,
                    )
                elif isinstance(ground_object, MissileSiteGroundObject):
                    generator = MissileSiteGenerator(
                        ground_object, country, self.game, self.m, self.unit_map
                    )
                else:
                    generator = PretenseGroundObjectGenerator(
                        ground_object, country, self.game, self.m, self.unit_map
                    )
                generator.generate()
            # Then generate ground supply and assault groups for the other coalition
            other_coalition = cp.coalition
            for coalition in cp.coalition.game.coalitions:
                if coalition == cp.coalition:
                    continue
                else:
                    other_coalition = coalition
            country = self.m.country(other_coalition.faction.country.name)
            for ground_object in cp.ground_objects:
                generator: GroundObjectGenerator
                if isinstance(ground_object, BuildingGroundObject):
                    new_ground_object = BuildingGroundObject(
                        name=ground_object.name,
                        category=ground_object.category,
                        location=PresetLocation(
                            f"{ground_object.name} {ground_object.id}",
                            ground_object.position,
                            ground_object.heading,
                        ),
                        control_point=ground_object.control_point,
                        is_fob_structure=ground_object.is_fob_structure,
                        task=ground_object.task,
                    )
                    generator = PretenseGroundObjectGenerator(
                        new_ground_object, country, self.game, self.m, self.unit_map
                    )
                elif isinstance(ground_object, VehicleGroupGroundObject):
                    new_ground_object = VehicleGroupGroundObject(
                        name=ground_object.name,
                        location=PresetLocation(
                            f"{ground_object.name} {ground_object.id}",
                            ground_object.position,
                            ground_object.heading,
                        ),
                        control_point=ground_object.control_point,
                        task=ground_object.task,
                    )
                    generator = PretenseGroundObjectGenerator(
                        new_ground_object, country, self.game, self.m, self.unit_map
                    )
                else:
                    continue

                generator.generate()

        self.mission_data.runways = list(self.runways.values())
