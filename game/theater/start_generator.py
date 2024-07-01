from __future__ import annotations

import logging
import random
from dataclasses import dataclass
from datetime import datetime, time
from typing import List, Optional

import dcs.statics
from dcs.countries import country_dict

from game import Game
from game.factions.faction import Faction
from game.naming import namegen
from game.scenery_group import SceneryGroup
from game.theater import PointWithHeading, PresetLocation, NavalControlPoint
from game.theater.theatergroundobject import (
    BuildingGroundObject,
    IadsBuildingGroundObject,
)
from game.utils import Heading, escape_string_for_lua
from game.version import VERSION
from . import (
    ConflictTheater,
    ControlPoint,
    ControlPointType,
    Fob,
    OffMapSpawn,
)
from .theatergroup import (
    IadsGroundGroup,
    IadsRole,
    SceneryUnit,
    TheaterGroup,
    TheaterUnit,
)
from ..armedforces.armedforces import ArmedForces
from ..armedforces.forcegroup import ForceGroup
from ..campaignloader.campaignairwingconfig import CampaignAirWingConfig
from ..campaignloader.campaigncarrierconfig import CampaignCarrierConfig
from ..campaignloader.campaigngroundconfig import TgoConfig
from ..data.groups import GroupTask
from ..data.units import UnitClass
from ..dcs.shipunittype import ShipUnitType
from ..profiling import logged_duration
from ..settings import Settings


@dataclass(frozen=True)
class GeneratorSettings:
    start_date: datetime
    start_time: time | None
    player_budget: int
    enemy_budget: int
    inverted: bool
    advanced_iads: bool
    no_carrier: bool
    no_lha: bool
    no_player_navy: bool
    no_enemy_navy: bool
    tgo_config: TgoConfig
    carrier_config: CampaignCarrierConfig
    squadrons_start_full: bool


@dataclass
class ModSettings:
    a4_skyhawk: bool = False
    a6a_intruder: bool = False
    a7e_corsair2: bool = False
    ea6b_prowler: bool = False
    f4bc_phantom: bool = False
    f9f_panther: bool = False
    f15d_baz: bool = False
    f_15_idf: bool = False
    f_16_idf: bool = False
    fa_18efg: bool = False
    fa18ef_tanker: bool = False
    f22_raptor: bool = False
    f84g_thunderjet: bool = False
    f100_supersabre: bool = False
    f104_starfighter: bool = False
    f105_thunderchief: bool = False
    f106_deltadart: bool = False
    hercules: bool = False
    irondome: bool = False
    uh_60l: bool = False
    jas39_gripen: bool = False
    mirage_3: bool = False
    super_etendard: bool = False
    su15_flagon: bool = False
    su30_flanker_h: bool = False
    su57_felon: bool = False
    frenchpack: bool = False
    high_digit_sams: bool = False
    ov10a_bronco: bool = False
    spanishnavypack: bool = False
    swedishmilitaryassetspack: bool = False
    SWPack: bool = False


class GameGenerator:
    def __init__(
        self,
        player: Faction,
        enemy: Faction,
        theater: ConflictTheater,
        air_wing_config: CampaignAirWingConfig,
        settings: Settings,
        generator_settings: GeneratorSettings,
        mod_settings: ModSettings,
    ) -> None:
        self.player = player
        self.enemy = enemy
        self.theater = theater
        self.air_wing_config = air_wing_config
        self.settings = settings
        self.generator_settings = generator_settings
        self.player.apply_mod_settings(mod_settings)
        self.enemy.apply_mod_settings(mod_settings)

    def generate(self) -> Game:
        with logged_duration("TGO population"):
            # Reset name generator
            namegen.reset()
            self.prepare_theater()
            game = Game(
                player_faction=self.player,
                enemy_faction=self.enemy,
                theater=self.theater,
                air_wing_config=self.air_wing_config,
                start_date=self.generator_settings.start_date,
                start_time=self.generator_settings.start_time,
                settings=self.settings,
                player_budget=self.generator_settings.player_budget,
                enemy_budget=self.generator_settings.enemy_budget,
            )

            GroundObjectGenerator(game, self.generator_settings).generate()
        game.settings.version = VERSION
        return game

    def should_remove_carrier(self, player: bool) -> bool:
        faction = self.player if player else self.enemy
        return self.generator_settings.no_carrier or not faction.carriers

    def should_remove_lha(self, player: bool) -> bool:
        faction = self.player if player else self.enemy
        return self.generator_settings.no_lha or not [
            x for x in faction.carriers if x.unit_class == UnitClass.HELICOPTER_CARRIER
        ]

    def prepare_theater(self) -> None:
        to_remove: List[ControlPoint] = []

        # Remove carrier and lha, invert situation if needed
        for cp in self.theater.controlpoints:
            if self.generator_settings.inverted:
                cp.starts_blue = cp.captured_invert

            if cp.is_carrier and self.should_remove_carrier(cp.starts_blue):
                to_remove.append(cp)
            elif cp.is_lha and self.should_remove_lha(cp.starts_blue):
                to_remove.append(cp)

        # do remove
        for cp in to_remove:
            self.theater.controlpoints.remove(cp)


class ControlPointGroundObjectGenerator:
    def __init__(
        self,
        game: Game,
        generator_settings: GeneratorSettings,
        control_point: ControlPoint,
    ) -> None:
        self.game = game
        self.generator_settings = generator_settings
        self.control_point = control_point

    @property
    def faction_name(self) -> str:
        return self.faction.name

    @property
    def faction(self) -> Faction:
        return self.game.coalition_for(self.control_point.captured).faction

    @property
    def armed_forces(self) -> ArmedForces:
        return self.game.coalition_for(self.control_point.captured).armed_forces

    def generate(self) -> bool:
        self.control_point.connected_objectives = []
        self.generate_navy()
        return True

    def generate_ground_object_from_group(
        self,
        unit_group: ForceGroup,
        location: PresetLocation,
        task: Optional[GroupTask] = None,
    ) -> None:
        ground_object = unit_group.generate(
            namegen.random_objective_name(),
            location,
            self.control_point,
            self.game,
            task,
        )
        self.control_point.connected_objectives.append(ground_object)

    def generate_navy(self) -> None:
        skip_player_navy = self.generator_settings.no_player_navy
        if self.control_point.captured and skip_player_navy:
            return
        skip_enemy_navy = self.generator_settings.no_enemy_navy
        if not self.control_point.captured and skip_enemy_navy:
            return
        for position in self.control_point.preset_locations.ships:
            unit_group = self.armed_forces.random_group_for_task(GroupTask.NAVY)
            if not unit_group:
                logging.warning(f"{self.faction_name} has no ForceGroup for Navy")
                return
            self.generate_ground_object_from_group(unit_group, position, GroupTask.NAVY)


class NoOpGroundObjectGenerator(ControlPointGroundObjectGenerator):
    def generate(self) -> bool:
        return True


class GenericCarrierGroundObjectGenerator(ControlPointGroundObjectGenerator):
    def update_carrier_name(self, carrier_name: str) -> None:
        # Set Control Point name
        self.control_point.name = carrier_name

        # Set UnitName. First unit of the TGO is always the carrier
        carrier = next(self.control_point.ground_objects[-1].units)
        carrier.name = carrier_name

    def apply_carrier_config(self) -> None:
        assert isinstance(self.control_point, NavalControlPoint)
        # If the campaign designer has specified a preferred name, use that
        # Note that the preferred name needs to exist in the faction, so we
        # don't end up with Kuznetsov carriers called CV-59 Forrestal
        preferred_name = None
        preferred_type = None
        carrier_map = self.generator_settings.carrier_config.by_original_name
        if ccfg := carrier_map.get(self.control_point.name):
            preferred_name = ccfg.preferred_name
            preferred_type = ccfg.preferred_type
        carrier_unit = self.get_carrier_unit()
        if preferred_type and preferred_type.dcs_unit_type in [
            v
            for k, v in country_dict[self.faction.country.id].Ship.__dict__.items()  # type: ignore
            if "__" not in k
        ]:
            carrier_unit.type = preferred_type.dcs_unit_type
        if preferred_name:
            self.control_point.name = preferred_name
        else:
            carrier_type = preferred_type if preferred_type else carrier_unit.unit_type
            assert isinstance(carrier_type, ShipUnitType)
            # Otherwise pick randomly from the names specified for that particular carrier type
            carrier_names = self.faction.carriers.get(carrier_type)
            if carrier_names:
                self.control_point.name = random.choice(list(carrier_names))
            else:
                self.control_point.name = carrier_type.display_name
        carrier_unit.name = self.control_point.name
        # Prevents duplicate carrier or LHA names in campaigns with more that one of either.
        for carrier_type_key in self.faction.carriers:
            for carrier_name in self.faction.carriers[carrier_type_key]:
                if carrier_name == self.control_point.name:
                    self.faction.carriers[carrier_type_key].remove(
                        self.control_point.name
                    )

    def get_carrier_unit(self) -> TheaterUnit:
        carrier_go = [
            go
            for go in self.control_point.ground_objects
            if go.category in ["CARRIER", "LHA"]
        ][0]
        groups = [
            g for g in carrier_go.groups if "Carrier" in g.name or "LHA" in g.name
        ]
        return groups[0].units[0]


class CarrierGroundObjectGenerator(GenericCarrierGroundObjectGenerator):
    def generate(self) -> bool:
        if not super().generate():
            return False

        carriers = self.faction.carriers
        if not carriers:
            logging.info(
                f"Skipping generation of {self.control_point.name} because "
                f"{self.faction_name} has no carriers"
            )
            return False

        unit_group = self.armed_forces.random_group_for_task(GroupTask.AIRCRAFT_CARRIER)
        if not unit_group:
            logging.error(f"{self.faction_name} has no access to AircraftCarrier")
            return False

        self.generate_ground_object_from_group(
            unit_group,
            PresetLocation(
                self.control_point.name,
                self.control_point.position,
                self.control_point.heading,
            ),
            GroupTask.AIRCRAFT_CARRIER,
        )
        self.apply_carrier_config()
        return True


class LhaGroundObjectGenerator(GenericCarrierGroundObjectGenerator):
    def generate(self) -> bool:
        if not super().generate():
            return False

        lhas = self.faction.carriers
        if not lhas:
            logging.info(
                f"Skipping generation of {self.control_point.name} because "
                f"{self.faction_name} has no LHAs"
            )
            return False

        unit_group = self.armed_forces.random_group_for_task(
            GroupTask.HELICOPTER_CARRIER
        )
        if not unit_group:
            logging.error(f"{self.faction_name} has no access to HelicopterCarrier")
            return False
        self.generate_ground_object_from_group(
            unit_group,
            PresetLocation(
                self.control_point.name,
                self.control_point.position,
                self.control_point.heading,
            ),
            GroupTask.HELICOPTER_CARRIER,
        )
        self.apply_carrier_config()
        return True


class AirbaseGroundObjectGenerator(ControlPointGroundObjectGenerator):
    def __init__(
        self,
        game: Game,
        generator_settings: GeneratorSettings,
        control_point: ControlPoint,
    ) -> None:
        super().__init__(game, generator_settings, control_point)

    def generate(self) -> bool:
        if not super().generate():
            return False

        self.generate_ground_points()
        return True

    def generate_ground_points(self) -> None:
        """Generate ground objects and AA sites for the control point."""
        self.generate_armor_groups()
        self.generate_iads()
        self.generate_scenery_sites()
        self.generate_strike_targets()
        self.generate_offshore_strike_targets()
        self.generate_factories()
        self.generate_ammunition_depots()
        self.generate_missile_sites()
        self.generate_coastal_sites()

    def get_unit_group_for_task(
        self, position: PresetLocation, task: GroupTask
    ) -> Optional[ForceGroup]:
        tgo_config = self.generator_settings.tgo_config
        fg = tgo_config[position.original_name]
        valid_fg = (
            fg
            and task in fg.tasks
            and all([u in self.faction.accessible_units for u in fg.units])
        )
        if valid_fg:
            assert fg
            for layout in fg.layouts:
                for lg in layout.groups:
                    for ug in lg.unit_groups:
                        if not fg.has_unit_for_layout_group(ug) and ug.fill:
                            for g in self.faction.ground_units:
                                if g.unit_class in ug.unit_classes:
                                    fg.units.append(g)
            unit_group: Optional[ForceGroup] = fg
        else:
            if fg:
                logging.warning(
                    f"Override in ground_forces failed for {fg} at {position.original_name}"
                )
            unit_group = self.armed_forces.random_group_for_task(task)
        return unit_group

    def generate_armor_groups(self) -> None:
        for position in self.control_point.preset_locations.armor_groups:
            unit_group = self.get_unit_group_for_task(position, GroupTask.BASE_DEFENSE)
            if not unit_group:
                logging.error(f"{self.faction_name} has no ForceGroup for Armor")
                return
            self.generate_ground_object_from_group(
                unit_group, position, GroupTask.BASE_DEFENSE
            )

    def generate_aa(self) -> None:
        presets = self.control_point.preset_locations
        aa_tasking = [GroupTask.AAA]
        for position in presets.aaa:
            self.generate_aa_at(position, aa_tasking)
        aa_tasking.insert(0, GroupTask.SHORAD)
        for position in presets.short_range_sams:
            self.generate_aa_at(position, aa_tasking)
        aa_tasking.insert(0, GroupTask.MERAD)
        for position in presets.medium_range_sams:
            self.generate_aa_at(position, aa_tasking)
        aa_tasking.insert(0, GroupTask.LORAD)
        for position in presets.long_range_sams:
            self.generate_aa_at(position, aa_tasking)

    def generate_ewrs(self) -> None:
        for position in self.control_point.preset_locations.ewrs:
            unit_group = self.armed_forces.random_group_for_task(
                GroupTask.EARLY_WARNING_RADAR
            )
            if not unit_group:
                logging.error(f"{self.faction_name} has no ForceGroup for EWR")
                return
            self.generate_ground_object_from_group(
                unit_group, position, GroupTask.EARLY_WARNING_RADAR
            )

    def generate_building_at(
        self,
        group_task: GroupTask,
        location: PresetLocation,
    ) -> None:
        # GroupTask is the type of the building to be generated
        unit_group = self.armed_forces.random_group_for_task(group_task)
        if not unit_group:
            raise RuntimeError(
                f"{self.faction_name} has no access to Building {group_task.description}"
            )
        self.generate_ground_object_from_group(unit_group, location, group_task)

    def generate_ammunition_depots(self) -> None:
        for position in self.control_point.preset_locations.ammunition_depots:
            self.generate_building_at(GroupTask.AMMO, position)

    def generate_factories(self) -> None:
        for position in self.control_point.preset_locations.factories:
            self.generate_building_at(GroupTask.FACTORY, position)

    def generate_aa_at(self, location: PresetLocation, tasks: list[GroupTask]) -> None:
        for task in tasks:
            unit_group = self.get_unit_group_for_task(location, task)
            if unit_group:
                # Only take next (smaller) aa_range when no template available for the
                # most requested range. Otherwise break the loop and continue
                self.generate_ground_object_from_group(unit_group, location, task)
                return

        logging.error(
            f"{self.faction_name} has no access to SAM {', '.join([task.description for task in tasks])}"
        )

    def generate_iads(self) -> None:
        # AntiAir
        self.generate_aa()
        # EWR
        self.generate_ewrs()
        # IADS Buildings
        for iads_element in self.control_point.preset_locations.iads_command_center:
            self.generate_building_at(GroupTask.COMMAND_CENTER, iads_element)
        for iads_element in self.control_point.preset_locations.iads_connection_node:
            self.generate_building_at(GroupTask.COMMS, iads_element)
        for iads_element in self.control_point.preset_locations.iads_power_source:
            self.generate_building_at(GroupTask.POWER, iads_element)

    def generate_scenery_sites(self) -> None:
        presets = self.control_point.preset_locations
        for scenery_group in presets.scenery:
            self.generate_tgo_for_scenery(scenery_group)

    def generate_tgo_for_scenery(self, scenery: SceneryGroup) -> None:
        # Special Handling for scenery Objects based on trigger zones
        iads_role = IadsRole.for_category(scenery.category)
        tgo_type = (
            IadsBuildingGroundObject if iads_role.participate else BuildingGroundObject
        )
        g = tgo_type(
            namegen.random_objective_name(),
            scenery.category,
            PresetLocation(scenery.zone_def.name, scenery.position),
            self.control_point,
            SceneryGroup.group_task_for_scenery_group_category(scenery.category),
        )
        ground_group = TheaterGroup(
            self.game.next_group_id(),
            scenery.zone_def.name,
            PointWithHeading.from_point(scenery.position, Heading.from_degrees(0)),
            [],
            g,
        )
        if iads_role.participate:
            ground_group = IadsGroundGroup.from_group(ground_group)
            ground_group.iads_role = iads_role

        g.groups.append(ground_group)
        # Each nested trigger zone is a target/building/unit for an objective.
        for zone in scenery.zones:
            zone.name = escape_string_for_lua(zone.name)
            scenery_unit = SceneryUnit(
                zone.id,
                zone.name,
                dcs.statics.Fortification.White_Flag,
                PointWithHeading.from_point(zone.position, Heading.from_degrees(0)),
                g,
            )
            scenery_unit.zone = zone
            ground_group.units.append(scenery_unit)

        self.control_point.connected_objectives.append(g)

    def generate_missile_sites(self) -> None:
        for position in self.control_point.preset_locations.missile_sites:
            unit_group = self.armed_forces.random_group_for_task(GroupTask.MISSILE)
            if not unit_group:
                logging.warning(f"{self.faction_name} has no ForceGroup for Missile")
                return
            self.generate_ground_object_from_group(
                unit_group, position, GroupTask.MISSILE
            )

    def generate_coastal_sites(self) -> None:
        for position in self.control_point.preset_locations.coastal_defenses:
            unit_group = self.armed_forces.random_group_for_task(GroupTask.COASTAL)
            if not unit_group:
                logging.warning(f"{self.faction_name} has no ForceGroup for Coastal")
                return
            self.generate_ground_object_from_group(
                unit_group, position, GroupTask.COASTAL
            )

    def generate_strike_targets(self) -> None:
        for position in self.control_point.preset_locations.strike_locations:
            self.generate_building_at(GroupTask.STRIKE_TARGET, position)

    def generate_offshore_strike_targets(self) -> None:
        for position in self.control_point.preset_locations.offshore_strike_locations:
            self.generate_building_at(GroupTask.OIL, position)


class FobGroundObjectGenerator(AirbaseGroundObjectGenerator):
    def generate(self) -> bool:
        if super(FobGroundObjectGenerator, self).generate():
            self.generate_fob()
            return True
        return False

    def generate_fob(self) -> None:
        self.generate_building_at(
            GroupTask.FOB,
            PresetLocation(
                self.control_point.name,
                self.control_point.position,
                self.control_point.heading,
            ),
        )


class GroundObjectGenerator:
    def __init__(self, game: Game, generator_settings: GeneratorSettings) -> None:
        self.game = game
        self.generator_settings = generator_settings

    def generate(self) -> None:
        # Copied so we can remove items from the original list without breaking
        # the iterator.
        control_points = list(self.game.theater.controlpoints)
        for control_point in control_points:
            if not self.generate_for_control_point(control_point):
                self.game.theater.controlpoints.remove(control_point)

    def generate_for_control_point(self, control_point: ControlPoint) -> bool:
        generator: ControlPointGroundObjectGenerator
        if control_point.cptype == ControlPointType.AIRCRAFT_CARRIER_GROUP:
            generator = CarrierGroundObjectGenerator(
                self.game, self.generator_settings, control_point
            )
        elif control_point.cptype == ControlPointType.LHA_GROUP:
            generator = LhaGroundObjectGenerator(
                self.game, self.generator_settings, control_point
            )
        elif isinstance(control_point, OffMapSpawn):
            generator = NoOpGroundObjectGenerator(
                self.game, self.generator_settings, control_point
            )
        elif isinstance(control_point, Fob):
            generator = FobGroundObjectGenerator(
                self.game, self.generator_settings, control_point
            )
        else:
            generator = AirbaseGroundObjectGenerator(
                self.game, self.generator_settings, control_point
            )
        return generator.generate()
