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
from dcs.triggers import (
    Event,
    TriggerOnce,
    TriggerStart,
    TriggerZone,
    TriggerZoneQuadPoint,
)
from dcs.unit import Unit, InvisibleFARP, BaseFARP, SingleHeliPad, FARP
from dcs.unitgroup import MovingGroup, ShipGroup, StaticGroup, VehicleGroup
from dcs.unittype import ShipType, VehicleType
from dcs.vehicles import vehicle_map, Unarmed

from game.missiongenerator.groundforcepainter import (
    NavalForcePainter,
    GroundForcePainter,
)
from game.missiongenerator.missiondata import CarrierInfo, MissionData
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
)
from game.theater.theatergroundobject import (
    CarrierGroundObject,
    GenericCarrierGroundObject,
    LhaGroundObject,
    MissileSiteGroundObject,
)
from game.theater.theatergroup import SceneryUnit, IadsGroundGroup
from game.unitmap import UnitMap
from game.utils import Heading, feet, knots, mps

if TYPE_CHECKING:
    from game import Game

FARP_FRONTLINE_DISTANCE = 10000
AA_CP_MIN_DISTANCE = 40000


def farp_truck_types_for_country(
    country_id: int,
) -> Tuple[Type[VehicleType], Type[VehicleType], Type[VehicleType]]:
    soviet_tankers: List[Type[VehicleType]] = [
        Unarmed.ATMZ_5,
        Unarmed.ATZ_10,
        Unarmed.ATZ_5,
        Unarmed.ATZ_60_Maz,
        Unarmed.TZ_22_KrAZ,
    ]
    soviet_trucks: List[Type[VehicleType]] = [
        Unarmed.S_75_ZIL,
        Unarmed.GAZ_3308,
        Unarmed.GAZ_66,
        Unarmed.KAMAZ_Truck,
        Unarmed.KrAZ6322,
        Unarmed.Ural_375,
        Unarmed.Ural_375_PBU,
        Unarmed.Ural_4320_31,
        Unarmed.Ural_4320T,
        Unarmed.ZIL_135,
    ]

    axis_trucks: List[Type[VehicleType]] = [Unarmed.Blitz_36_6700A]

    us_tankers: List[Type[VehicleType]] = [Unarmed.M978_HEMTT_Tanker]
    us_trucks: List[Type[VehicleType]] = [Unarmed.M_818]
    uk_trucks: List[Type[VehicleType]] = [Unarmed.Bedford_MWD]

    ground_power_trucks: List[Type[VehicleType]] = [
        Unarmed.Ural_4320_APA_5D,
        Unarmed.ZiL_131_APA_80,
    ]

    if country_id in [
        Abkhazia.id,
        Algeria.id,
        Bahrain.id,
        Belarus.id,
        Belgium.id,
        Bulgaria.id,
        China.id,
        Croatia.id,
        Cuba.id,
        Cyprus.id,
        CzechRepublic.id,
        Egypt.id,
        Ethiopia.id,
        Finland.id,
        GDR.id,
        Georgia.id,
        Ghana.id,
        Greece.id,
        Hungary.id,
        India.id,
        Insurgents.id,
        Iraq.id,
        Jordan.id,
        Kazakhstan.id,
        Lebanon.id,
        Libya.id,
        Morocco.id,
        Nigeria.id,
        NorthKorea.id,
        Poland.id,
        Romania.id,
        Russia.id,
        Serbia.id,
        Slovakia.id,
        Slovenia.id,
        SouthAfrica.id,
        SouthOssetia.id,
        Sudan.id,
        Syria.id,
        Tunisia.id,
        USSR.id,
        Ukraine.id,
        Venezuela.id,
        Vietnam.id,
        Yemen.id,
        Yugoslavia.id,
    ]:
        tanker_type = random.choice(soviet_tankers)
        ammo_truck_type = random.choice(soviet_trucks)
    elif country_id in [ItalianSocialRepublic.id, ThirdReich.id]:
        tanker_type = random.choice(soviet_tankers)
        ammo_truck_type = random.choice(axis_trucks)
    elif country_id in [
        Argentina.id,
        Australia.id,
        Austria.id,
        Bolivia.id,
        Brazil.id,
        Canada.id,
        Chile.id,
        Denmark.id,
        Ecuador.id,
        France.id,
        Germany.id,
        Honduras.id,
        Indonesia.id,
        Iran.id,
        Israel.id,
        Italy.id,
        Japan.id,
        Kuwait.id,
        Malaysia.id,
        Mexico.id,
        Norway.id,
        Oman.id,
        Pakistan.id,
        Peru.id,
        Philippines.id,
        Portugal.id,
        Qatar.id,
        SaudiArabia.id,
        SouthKorea.id,
        Spain.id,
        Sweden.id,
        Switzerland.id,
        Thailand.id,
        TheNetherlands.id,
        Turkey.id,
        USA.id,
        USAFAggressors.id,
        UnitedArabEmirates.id,
    ]:
        tanker_type = random.choice(us_tankers)
        ammo_truck_type = random.choice(us_trucks)
    elif country_id in [UK.id]:
        tanker_type = random.choice(us_tankers)
        ammo_truck_type = random.choice(uk_trucks)
    elif country_id in [CombinedJointTaskForcesBlue.id]:
        tanker_types = us_tankers
        truck_types = us_trucks + uk_trucks

        tanker_type = random.choice(tanker_types)
        ammo_truck_type = random.choice(truck_types)
    elif country_id in [CombinedJointTaskForcesRed.id]:
        tanker_types = us_tankers
        truck_types = us_trucks + uk_trucks

        tanker_type = random.choice(tanker_types)
        ammo_truck_type = random.choice(truck_types)
    elif country_id in [UnitedNationsPeacekeepers.id]:
        tanker_types = soviet_tankers + us_tankers
        truck_types = soviet_trucks + us_trucks + uk_trucks

        tanker_type = random.choice(tanker_types)
        ammo_truck_type = random.choice(truck_types)
    else:
        tanker_types = soviet_tankers + us_tankers
        truck_types = soviet_trucks + us_trucks + uk_trucks + axis_trucks

        tanker_type = random.choice(tanker_types)
        ammo_truck_type = random.choice(truck_types)

    power_truck_type = random.choice(ground_power_trucks)

    return tanker_type, ammo_truck_type, power_truck_type


class GroundObjectGenerator:
    """generates the DCS groups and units from the TheaterGroundObject"""

    def __init__(
        self,
        ground_object: TheaterGroundObject,
        country: Country,
        game: Game,
        mission: Mission,
        unit_map: UnitMap,
    ) -> None:
        self.ground_object = ground_object
        self.country = country
        self.game = game
        self.m = mission
        self.unit_map = unit_map

    @property
    def culled(self) -> bool:
        return self.game.iads_considerate_culling(self.ground_object)

    def generate(self) -> None:
        if self.culled:
            return
        for group in self.ground_object.groups:
            vehicle_units = []
            ship_units = []
            # Split the different unit types to be compliant to dcs limitation
            for unit in group.units:
                if unit.is_static:
                    if isinstance(unit, SceneryUnit):
                        # Special handling for scenery objects
                        self.add_trigger_zone_for_scenery(unit)
                        if (
                            self.game.settings.plugin_option("skynetiads")
                            and isinstance(group, IadsGroundGroup)
                            and group.iads_role.participate
                        ):
                            # Generate a unit which can be controlled by skynet
                            self.generate_iads_command_unit(unit)
                    else:
                        # Create a static group for each static unit
                        self.create_static_group(unit)
                elif unit.is_vehicle and unit.alive:
                    # All alive Vehicles
                    vehicle_units.append(unit)
                elif unit.is_ship and unit.alive:
                    # All alive Ships
                    ship_units.append(unit)
            if vehicle_units:
                vg = self.create_vehicle_group(group.group_name, vehicle_units)
                vg.hidden_on_mfd = self.ground_object.hide_on_mfd
            if ship_units:
                sg = self.create_ship_group(group.group_name, ship_units)
                sg.hidden_on_mfd = self.ground_object.hide_on_mfd

    def create_vehicle_group(
        self, group_name: str, units: list[TheaterUnit]
    ) -> VehicleGroup:
        vehicle_group: Optional[VehicleGroup] = None
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

    def create_ship_group(
        self,
        group_name: str,
        units: list[TheaterUnit],
        frequency: Optional[RadioFrequency] = None,
    ) -> ShipGroup:
        ship_group: Optional[ShipGroup] = None
        for unit in units:
            assert issubclass(unit.type, ShipType)
            faction = unit.ground_object.control_point.coalition.faction
            if ship_group is None:
                ship_group = self.m.ship_group(
                    self.country,
                    group_name,
                    unit.type,
                    position=unit.position,
                    heading=unit.position.heading.degrees,
                )
                if frequency:
                    ship_group.set_frequency(frequency.hertz)
                ship_group.units[0].name = unit.unit_name
                self.set_alarm_state(ship_group)
                NavalForcePainter(faction, ship_group.units[0]).apply_livery()
            else:
                ship_unit = self.m.ship(unit.unit_name, unit.type)
                if frequency:
                    ship_unit.set_frequency(frequency.hertz)
                ship_unit.position = unit.position
                ship_unit.heading = unit.position.heading.degrees
                NavalForcePainter(faction, ship_unit).apply_livery()
                ship_group.add_unit(ship_unit)
            self._register_theater_unit(unit, ship_group.units[-1])
        if ship_group is None:
            raise RuntimeError(f"Error creating ShipGroup for {group_name}")
        return ship_group

    def create_static_group(self, unit: TheaterUnit) -> None:
        static_group = self.m.static_group(
            country=self.country,
            name=unit.unit_name,
            _type=unit.type,
            position=unit.position,
            heading=unit.position.heading.degrees,
            dead=not unit.alive,
        )
        self._register_theater_unit(unit, static_group.units[0])

    @staticmethod
    def enable_eplrs(group: VehicleGroup, unit_type: Type[VehicleType]) -> None:
        if unit_type.eplrs:
            group.points[0].tasks.append(EPLRS(group.id))

    def set_alarm_state(self, group: MovingGroup[Any]) -> None:
        if self.game.settings.perf_red_alert_state:
            group.points[0].tasks.append(OptAlarmState(2))
        else:
            group.points[0].tasks.append(OptAlarmState(1))

    def _register_theater_unit(
        self,
        theater_unit: TheaterUnit,
        dcs_unit: Unit,
    ) -> None:
        self.unit_map.add_theater_unit_mapping(theater_unit, dcs_unit)

    def add_trigger_zone_for_scenery(self, scenery: SceneryUnit) -> None:
        # Align the trigger zones to the faction color on the DCS briefing/F10 map.
        color = (
            {1: 0.2, 2: 0.7, 3: 1, 4: 0.15}
            if scenery.ground_object.is_friendly(to_player=True)
            else {1: 1, 2: 0.2, 3: 0.2, 4: 0.15}
        )

        # Create the smallest valid size trigger zone (16 feet) so that risk of overlap
        # is minimized. As long as the triggerzone is over the scenery object, we're ok.
        smallest_valid_radius = feet(16).meters

        if isinstance(scenery.zone, TriggerZoneQuadPoint):
            trigger_zone: TriggerZone = self.m.triggers.add_triggerzone_quad(
                scenery.zone.position,
                scenery.zone.verticies,
                scenery.zone.hidden,
                scenery.zone.name,
                color,
                scenery.zone.properties,
            )
        else:
            trigger_zone = self.m.triggers.add_triggerzone(
                scenery.zone.position,
                smallest_valid_radius,
                scenery.zone.hidden,
                scenery.zone.name,
                color,
                scenery.zone.properties,
            )
        # DCS only visually shows a scenery object is dead when
        # this trigger rule is applied.  Otherwise you can kill a
        # structure twice.
        if not scenery.alive:
            self.generate_destruction_trigger_rule(trigger_zone)
        else:
            self.generate_on_dead_trigger_rule(trigger_zone)

        self.unit_map.add_scenery(scenery, trigger_zone)

    def generate_destruction_trigger_rule(self, trigger_zone: TriggerZone) -> None:
        # Add destruction zone trigger
        t = TriggerStart(comment="Destruction")
        t.actions.append(
            SceneryDestructionZone(destruction_level=100, zone=trigger_zone.id)
        )
        self.m.triggerrules.triggers.append(t)

    def generate_on_dead_trigger_rule(self, trigger_zone: TriggerZone) -> None:
        # Add a TriggerRule with the MapObjectIsDead condition to recognize killed
        # map objects and add them to the state.json with a DoScript
        t = TriggerOnce(Event.NoEvent, f"MapObjectIsDead Trigger {trigger_zone.id}")
        t.add_condition(MapObjectIsDead(trigger_zone.id))
        script_string = String(f'dead_events[#dead_events + 1] = "{trigger_zone.name}"')
        t.actions.append(DoScript(script_string))
        self.m.triggerrules.triggers.append(t)

    def generate_iads_command_unit(self, unit: SceneryUnit) -> None:
        # Creates a static Infantry Unit next to a scenery object. This is needed
        # because skynet can not use map objects as Comms, Power or Command and needs a
        # "real" unit to function correctly
        self.m.static_group(
            country=self.country,
            name=unit.unit_name,
            _type=dcs.vehicles.Infantry.Soldier_M4,
            position=unit.position,
            heading=unit.position.heading.degrees,
            dead=not unit.alive,  # Also spawn as dead!
        )


class MissileSiteGenerator(GroundObjectGenerator):
    @property
    def culled(self) -> bool:
        # Don't cull missile sites - their range is long enough to make them easily
        # culled despite being a threat.
        return False

    def generate(self) -> None:
        super(MissileSiteGenerator, self).generate()

        if not self.game.settings.generate_fire_tasks_for_missile_sites:
            return

        # Note : Only the SCUD missiles group can fire (V1 site cannot fire in game right now)
        # TODO : Should be pre-planned ?
        # TODO : Add delay to task to spread fire task over mission duration ?
        for group in self.ground_object.groups:
            vg = self.m.find_group(group.group_name)
            if vg is not None:
                targets = self.possible_missile_targets()
                if targets:
                    target = random.choice(targets)
                    real_target = target.point_from_heading(
                        Heading.random().degrees, random.randint(0, 2500)
                    )
                    vg.points[0].add_task(FireAtPoint(real_target))
                    logging.info("Set up fire task for missile group.")
                else:
                    logging.info(
                        "Couldn't setup missile site to fire, no valid target in range."
                    )
            else:
                logging.info(
                    "Couldn't setup missile site to fire, group was not generated."
                )

    def possible_missile_targets(self) -> List[Point]:
        """
        Find enemy control points in range
        :return: List of possible missile targets
        """
        targets: List[Point] = []
        for cp in self.game.theater.controlpoints:
            if cp.captured != self.ground_object.control_point.captured:
                distance = cp.position.distance_to_point(self.ground_object.position)
                if distance < self.missile_site_range:
                    targets.append(cp.position)
        return targets

    @property
    def missile_site_range(self) -> int:
        """
        Get the missile site range
        :return: Missile site range
        """
        site_range = 0
        for group in self.ground_object.groups:
            vg = self.m.find_group(group.group_name)
            if vg is not None:
                for u in vg.units:
                    if u.type in vehicle_map:
                        if vehicle_map[u.type].threat_range > site_range:
                            site_range = vehicle_map[u.type].threat_range
        return site_range


class GenericCarrierGenerator(GroundObjectGenerator):
    """Base type for carrier group generation.

    Used by both CV(N) groups and LHA groups.
    """

    def __init__(
        self,
        ground_object: GenericCarrierGroundObject,
        control_point: NavalControlPoint,
        country: Country,
        game: Game,
        mission: Mission,
        radio_registry: RadioRegistry,
        tacan_registry: TacanRegistry,
        icls_alloc: Iterator[int],
        runways: Dict[str, RunwayData],
        unit_map: UnitMap,
        mission_data: MissionData,
    ) -> None:
        super().__init__(ground_object, country, game, mission, unit_map)
        self.ground_object = ground_object
        self.control_point = control_point
        self.radio_registry = radio_registry
        self.tacan_registry = tacan_registry
        self.icls_alloc = icls_alloc
        self.runways = runways
        self.mission_data = mission_data

    def generate(self) -> None:
        if self.control_point.frequency is not None:
            atc = self.control_point.frequency
            if atc not in self.radio_registry.allocated_channels:
                self.radio_registry.reserve(atc)
        else:
            atc = self.radio_registry.alloc_uhf()

        for g_id, group in enumerate(self.ground_object.groups):
            if not group.units:
                logging.warning(f"Found empty carrier group in {self.control_point}")
                continue

            ship_units = []
            for unit in group.units:
                if unit.alive:
                    # All alive Ships
                    ship_units.append(unit)

            if not ship_units:
                # Empty array (no alive units), skip this group
                continue

            ship_group = self.create_ship_group(group.group_name, ship_units, atc)

            # Always steam into the wind, even if the carrier is being moved.
            # There are multiple unsimulated hours between turns, so we can
            # count those as the time the carrier uses to move and the mission
            # time as the recovery window.
            brc = self.steam_into_wind(ship_group)

            # Set Carrier Specific Options
            if g_id == 0 and self.control_point.runway_is_operational():
                # Get Correct unit type for the carrier.
                # This will upgrade to super carrier if option is enabled
                carrier_type = self.carrier_type
                if carrier_type is None:
                    raise RuntimeError(
                        f"Error generating carrier group for {self.control_point.name}"
                    )
                ship_group.units[0].type = carrier_type.id
                self.control_point.carrier_id = ship_group.units[0].id
                if self.control_point.tacan is None:
                    tacan = self.tacan_registry.alloc_for_band(
                        TacanBand.X, TacanUsage.TransmitReceive
                    )
                else:
                    tacan = self.control_point.tacan
                if self.control_point.tcn_name is None:
                    tacan_callsign = self.tacan_callsign()
                else:
                    tacan_callsign = self.control_point.tcn_name
                link4 = None
                link4carriers = [Stennis, CVN_71, CVN_72, CVN_73, CVN_75, Forrestal]
                if carrier_type in link4carriers:
                    if self.control_point.link4 is None:
                        link4 = self.radio_registry.alloc_uhf()
                    else:
                        link4 = self.control_point.link4
                icls = None
                icls_name = self.control_point.icls_name
                if carrier_type in link4carriers or carrier_type == LHA_Tarawa:
                    if self.control_point.icls_channel is None:
                        icls = next(self.icls_alloc)
                    else:
                        icls = self.control_point.icls_channel
                self.activate_beacons(
                    ship_group, tacan, tacan_callsign, icls, icls_name, link4
                )
                self.add_runway_data(
                    brc or Heading.from_degrees(0), atc, tacan, tacan_callsign, icls
                )
                self.mission_data.carriers.append(
                    CarrierInfo(
                        group_name=ship_group.name,
                        unit_name=ship_group.units[0].name,
                        callsign=tacan_callsign,
                        freq=atc,
                        tacan=tacan,
                        blue=self.control_point.captured,
                    )
                )

    @property
    def carrier_type(self) -> Optional[Type[ShipType]]:
        return self.control_point.get_carrier_group_type()

    def steam_into_wind(self, group: ShipGroup) -> Optional[Heading]:
        wind = self.game.conditions.weather.wind.at_0m
        brc = Heading.from_degrees(wind.direction).opposite
        # Aim for 25kts over the deck.
        carrier_speed = knots(25) - mps(wind.speed)
        for attempt in range(5):
            point = group.points[0].position.point_from_heading(
                brc.degrees, 100000 - attempt * 20000
            )
            if self.game.theater.is_in_sea(point):
                group.points[0].speed = carrier_speed.meters_per_second
                group.add_waypoint(point, carrier_speed.kph)
                # Rotate the whole ground object to the new course
                self.ground_object.rotate(brc)
                return brc
        return None

    def tacan_callsign(self) -> str:
        raise NotImplementedError

    @staticmethod
    def activate_beacons(
        group: ShipGroup,
        tacan: TacanChannel,
        callsign: str,
        icls: Optional[int] = None,
        icls_name: Optional[str] = None,
        link4: Optional[RadioFrequency] = None,
    ) -> None:
        group.points[0].tasks.append(
            ActivateBeaconCommand(
                channel=tacan.number,
                modechannel=tacan.band.value,
                callsign=callsign,
                unit_id=group.units[0].id,
                aa=False,
            )
        )
        if icls is not None:
            icls_name = "" if icls_name is None else icls_name
            group.points[0].tasks.append(
                ActivateICLSCommand(icls, group.units[0].id, icls_name)
            )
        if link4 is not None:
            group.points[0].tasks.append(
                ActivateLink4Command(link4.hertz, group.units[0].id)
            )
            group.points[0].tasks.append(ActivateACLSCommand(unit_id=group.units[0].id))

    def add_runway_data(
        self,
        brc: Heading,
        atc: RadioFrequency,
        tacan: TacanChannel,
        callsign: str,
        icls: Optional[int],
    ) -> None:
        # This relies on one control point mapping exactly
        # to one LHA, carrier, or other usable "runway".
        # This isn't wholly true, since the DD escorts of
        # the carrier group are valid for helicopters, but
        # they aren't exposed as such to the game. Should
        # clean this up so that's possible. We can't use the
        # unit name since it's an arbitrary ID.
        self.runways[self.control_point.full_name] = RunwayData(
            self.control_point.name,
            brc,
            f"{brc.degrees:03}",
            atc=atc,
            tacan=tacan,
            tacan_callsign=callsign,
            icls=icls,
        )


class CarrierGenerator(GenericCarrierGenerator):
    """Generator for CV(N) groups."""

    def tacan_callsign(self) -> str:
        # TODO: Assign these properly.
        return random.choice(
            [
                "STE",
                "CVN",
                "CVH",
                "CCV",
                "ACC",
                "ARC",
                "GER",
                "ABR",
                "LIN",
                "TRU",
            ]
        )


class LhaGenerator(GenericCarrierGenerator):
    """Generator for LHA groups."""

    def tacan_callsign(self) -> str:
        # TODO: Assign these properly.
        return random.choice(
            [
                "LHD",
                "LHA",
                "LHB",
                "LHC",
                "LHD",
                "LDS",
            ]
        )


class HelipadGenerator:
    """
    Generates helipads for given control point
    """

    def __init__(
        self,
        mission: Mission,
        cp: ControlPoint,
        game: Game,
        radio_registry: RadioRegistry,
        tacan_registry: TacanRegistry,
    ):
        self.m = mission
        self.cp = cp
        self.game = game
        self.radio_registry = radio_registry
        self.tacan_registry = tacan_registry
        self.helipads: list[StaticGroup] = []

    def create_helipad(
        self, i: int, helipad: PointWithHeading, helipad_type: str
    ) -> None:
        # Note: Helipad are generated as neutral object in order not to interfere with
        # capture triggers
        pad: BaseFARP
        neutral_country = self.m.country(self.game.neutral_country.name)
        country = self.m.country(
            self.game.coalition_for(self.cp.captured).faction.country.name
        )

        name = f"{self.cp.name} {helipad_type} {i}"
        logging.info("Generating helipad static : " + name)
        terrain = self.m.terrain
        if helipad_type == "SINGLE_HELIPAD":
            pad = SingleHeliPad(
                unit_id=self.m.next_unit_id(), name=name, terrain=terrain
            )
            number_of_pads = 1
        elif helipad_type == "FARP":
            pad = FARP(unit_id=self.m.next_unit_id(), name=name, terrain=terrain)
            number_of_pads = 4
        else:
            pad = InvisibleFARP(
                unit_id=self.m.next_unit_id(), name=name, terrain=terrain
            )
            number_of_pads = 1
        pad.position = Point(helipad.x, helipad.y, terrain=terrain)
        pad.heading = helipad.heading.degrees

        # Set FREQ
        if isinstance(self.cp, RadioFrequencyContainer) and self.cp.frequency:
            if isinstance(pad, BaseFARP):
                pad.heliport_frequency = self.cp.frequency.mhz

        sg = unitgroup.StaticGroup(self.m.next_group_id(), name)
        sg.add_unit(pad)
        sp = StaticPoint(pad.position)
        sg.add_point(sp)
        neutral_country.add_static_group(sg)

        if number_of_pads > 1:
            self.append_helipad(pad, name, helipad.heading.degrees, 60, 0, 0)
            self.append_helipad(pad, name, helipad.heading.degrees + 180, 20, 0, 0)
            self.append_helipad(
                pad, name, helipad.heading.degrees + 90, 60, helipad.heading.degrees, 20
            )
            self.append_helipad(
                pad,
                name,
                helipad.heading.degrees + 90,
                60,
                helipad.heading.degrees + 180,
                60,
            )
        else:
            self.helipads.append(sg)

        # Generate a FARP Ammo and Fuel stack for each pad
        self.m.static_group(
            country=country,
            name=(name + "_fuel"),
            _type=Fortification.FARP_Fuel_Depot,
            position=pad.position.point_from_heading(helipad.heading.degrees, 35),
            heading=pad.heading + 180,
        )
        self.m.static_group(
            country=country,
            name=(name + "_ammo"),
            _type=Fortification.FARP_Ammo_Dump_Coating,
            position=pad.position.point_from_heading(
                helipad.heading.degrees, 35
            ).point_from_heading(helipad.heading.degrees + 90, 10),
            heading=pad.heading + 90,
        )
        self.m.static_group(
            country=country,
            name=(name + "_ws"),
            _type=Fortification.Windsock,
            position=helipad.point_from_heading(helipad.heading.degrees + 45, 35),
            heading=pad.heading,
        )

    def append_helipad(
        self,
        pad: BaseFARP,
        name: str,
        heading_1: int,
        distance_1: int,
        heading_2: int,
        distance_2: int,
    ) -> None:
        new_pad = InvisibleFARP(pad._terrain)
        new_pad.position = pad.position.point_from_heading(heading_1, distance_1)
        new_pad.position = new_pad.position.point_from_heading(heading_2, distance_2)
        sg = unitgroup.StaticGroup(self.m.next_group_id(), name)
        sg.add_unit(new_pad)
        self.helipads.append(sg)

    def generate(self) -> None:
        for i, helipad in enumerate(self.cp.helipads):
            self.create_helipad(i, helipad, "SINGLE_HELIPAD")
        for i, helipad in enumerate(self.cp.helipads_quad):
            self.create_helipad(i, helipad, "FARP")
        for i, helipad in enumerate(self.cp.helipads_invisible):
            self.create_helipad(i, helipad, "Invisible FARP")


class GroundSpawnRoadbaseGenerator:
    """
    Generates Highway strip starting positions for given control point
    """

    def __init__(
        self,
        mission: Mission,
        cp: ControlPoint,
        game: Game,
        radio_registry: RadioRegistry,
        tacan_registry: TacanRegistry,
    ):
        self.m = mission
        self.cp = cp
        self.game = game
        self.radio_registry = radio_registry
        self.tacan_registry = tacan_registry
        self.ground_spawns_roadbase: list[Tuple[StaticGroup, Point]] = []

    def create_ground_spawn_roadbase(
        self, i: int, ground_spawn: Tuple[PointWithHeading, Point]
    ) -> None:
        # Note: FARPs are generated as neutral object in order not to interfere with
        # capture triggers
        neutral_country = self.m.country(self.game.neutral_country.name)
        country = self.m.country(
            self.game.coalition_for(self.cp.captured).faction.country.name
        )
        terrain = self.cp.coalition.game.theater.terrain

        name = f"{self.cp.name} roadbase spawn {i}"
        logging.info("Generating Roadbase Spawn static : " + name)

        pad = InvisibleFARP(unit_id=self.m.next_unit_id(), name=name, terrain=terrain)

        pad.position = Point(ground_spawn[0].x, ground_spawn[0].y, terrain=terrain)
        pad.heading = ground_spawn[0].heading.degrees
        sg = unitgroup.StaticGroup(self.m.next_group_id(), name)
        sg.add_unit(pad)
        sp = StaticPoint(pad.position)
        sg.add_point(sp)
        neutral_country.add_static_group(sg)

        self.ground_spawns_roadbase.append((sg, ground_spawn[1]))

        tanker_type, ammo_truck_type, power_truck_type = farp_truck_types_for_country(
            country.id
        )

        # Generate ammo truck/farp and fuel truck/stack for each pad
        if self.game.settings.ground_start_trucks_roadbase:
            self.m.vehicle_group(
                country=country,
                name=(name + "_fuel"),
                _type=tanker_type,
                position=pad.position.point_from_heading(
                    ground_spawn[0].heading.degrees + 90, 35
                ),
                group_size=1,
                heading=pad.heading + 315,
                move_formation=PointAction.OffRoad,
            )
            self.m.vehicle_group(
                country=country,
                name=(name + "_ammo"),
                _type=ammo_truck_type,
                position=pad.position.point_from_heading(
                    ground_spawn[0].heading.degrees + 90, 35
                ).point_from_heading(ground_spawn[0].heading.degrees + 180, 10),
                group_size=1,
                heading=pad.heading + 315,
                move_formation=PointAction.OffRoad,
            )
        else:
            self.m.static_group(
                country=country,
                name=(name + "_fuel"),
                _type=Fortification.FARP_Fuel_Depot,
                position=pad.position.point_from_heading(
                    ground_spawn[0].heading.degrees + 90, 35
                ),
                heading=pad.heading + 270,
            )
            self.m.static_group(
                country=country,
                name=(name + "_ammo"),
                _type=Fortification.FARP_Ammo_Dump_Coating,
                position=pad.position.point_from_heading(
                    ground_spawn[0].heading.degrees + 90, 35
                ).point_from_heading(ground_spawn[0].heading.degrees + 180, 10),
                heading=pad.heading + 180,
            )
        if self.game.settings.ground_start_ground_power_trucks_roadbase:
            self.m.vehicle_group(
                country=country,
                name=(name + "_power"),
                _type=power_truck_type,
                position=pad.position.point_from_heading(
                    ground_spawn[0].heading.degrees + 90, 35
                ).point_from_heading(ground_spawn[0].heading.degrees + 180, 20),
                group_size=1,
                heading=pad.heading + 315,
                move_formation=PointAction.OffRoad,
            )

    def generate(self) -> None:
        try:
            for i, ground_spawn in enumerate(self.cp.ground_spawns_roadbase):
                self.create_ground_spawn_roadbase(i, ground_spawn)
        except AttributeError:
            self.ground_spawns_roadbase = []


class GroundSpawnLargeGenerator:
    """
    Generates STOL aircraft starting positions for given control point
    """

    def __init__(
        self,
        mission: Mission,
        cp: ControlPoint,
        game: Game,
        radio_registry: RadioRegistry,
        tacan_registry: TacanRegistry,
    ):
        self.m = mission
        self.cp = cp
        self.game = game
        self.radio_registry = radio_registry
        self.tacan_registry = tacan_registry
        self.ground_spawns_large: list[Tuple[StaticGroup, Point]] = []

    def create_ground_spawn_large(
        self, i: int, vtol_pad: Tuple[PointWithHeading, Point]
    ) -> None:
        # Note: FARPs are generated as neutral object in order not to interfere with
        # capture triggers
        neutral_country = self.m.country(self.game.neutral_country.name)
        country = self.m.country(
            self.game.coalition_for(self.cp.captured).faction.country.name
        )
        terrain = self.cp.coalition.game.theater.terrain

        name = f"{self.cp.name} large ground spawn {i}"
        logging.info("Generating Large Ground Spawn static : " + name)

        pad = InvisibleFARP(unit_id=self.m.next_unit_id(), name=name, terrain=terrain)

        pad.position = Point(vtol_pad[0].x, vtol_pad[0].y, terrain=terrain)
        pad.heading = vtol_pad[0].heading.degrees
        sg = unitgroup.StaticGroup(self.m.next_group_id(), name)
        sg.add_unit(pad)
        sp = StaticPoint(pad.position)
        sg.add_point(sp)
        neutral_country.add_static_group(sg)

        self.ground_spawns_large.append((sg, vtol_pad[1]))

        # tanker_type: Type[VehicleType]
        # ammo_truck_type: Type[VehicleType]

        tanker_type, ammo_truck_type, power_truck_type = farp_truck_types_for_country(
            country.id
        )

        # Generate a FARP Ammo and Fuel stack for each pad
        if self.game.settings.ground_start_trucks:
            self.m.vehicle_group(
                country=country,
                name=(name + "_fuel"),
                _type=tanker_type,
                position=pad.position.point_from_heading(
                    vtol_pad[0].heading.degrees - 175, 45
                ),
                group_size=1,
                heading=pad.heading + 45,
                move_formation=PointAction.OffRoad,
            )
            self.m.vehicle_group(
                country=country,
                name=(name + "_ammo"),
                _type=ammo_truck_type,
                position=pad.position.point_from_heading(
                    vtol_pad[0].heading.degrees - 185, 45
                ),
                group_size=1,
                heading=pad.heading + 45,
                move_formation=PointAction.OffRoad,
            )
        else:
            self.m.static_group(
                country=country,
                name=(name + "_fuel"),
                _type=Fortification.FARP_Fuel_Depot,
                position=pad.position.point_from_heading(
                    vtol_pad[0].heading.degrees - 180, 55
                ),
                heading=pad.heading,
            )
            self.m.static_group(
                country=country,
                name=(name + "_ammo"),
                _type=Fortification.FARP_Ammo_Dump_Coating,
                position=pad.position.point_from_heading(
                    vtol_pad[0].heading.degrees - 180, 45
                ),
                heading=pad.heading + 270,
            )
        if self.game.settings.ground_start_ground_power_trucks:
            self.m.vehicle_group(
                country=country,
                name=(name + "_power"),
                _type=power_truck_type,
                position=pad.position.point_from_heading(
                    vtol_pad[0].heading.degrees - 185, 45
                ),
                group_size=1,
                heading=pad.heading + 45,
                move_formation=PointAction.OffRoad,
            )

    def generate(self) -> None:
        try:
            for i, vtol_pad in enumerate(self.cp.ground_spawns_large):
                self.create_ground_spawn_large(i, vtol_pad)
        except AttributeError:
            self.ground_spawns_large = []


class GroundSpawnGenerator:
    """
    Generates STOL aircraft starting positions for given control point
    """

    def __init__(
        self,
        mission: Mission,
        cp: ControlPoint,
        game: Game,
        radio_registry: RadioRegistry,
        tacan_registry: TacanRegistry,
    ):
        self.m = mission
        self.cp = cp
        self.game = game
        self.radio_registry = radio_registry
        self.tacan_registry = tacan_registry
        self.ground_spawns: list[Tuple[StaticGroup, Point]] = []

    def create_ground_spawn(
        self, i: int, vtol_pad: Tuple[PointWithHeading, Point]
    ) -> None:
        # Note: FARPs are generated as neutral object in order not to interfere with
        # capture triggers
        neutral_country = self.m.country(self.game.neutral_country.name)
        country = self.m.country(
            self.game.coalition_for(self.cp.captured).faction.country.name
        )
        terrain = self.cp.coalition.game.theater.terrain

        name = f"{self.cp.name} ground spawn {i}"
        logging.info("Generating Ground Spawn static : " + name)

        pad = InvisibleFARP(unit_id=self.m.next_unit_id(), name=name, terrain=terrain)

        pad.position = Point(vtol_pad[0].x, vtol_pad[0].y, terrain=terrain)
        pad.heading = vtol_pad[0].heading.degrees
        sg = unitgroup.StaticGroup(self.m.next_group_id(), name)
        sg.add_unit(pad)
        sp = StaticPoint(pad.position)
        sg.add_point(sp)
        neutral_country.add_static_group(sg)

        self.ground_spawns.append((sg, vtol_pad[1]))

        # tanker_type: Type[VehicleType]
        # ammo_truck_type: Type[VehicleType]

        tanker_type, ammo_truck_type, power_truck_type = farp_truck_types_for_country(
            country.id
        )

        # Generate a FARP Ammo and Fuel stack for each pad
        if self.game.settings.ground_start_trucks:
            self.m.vehicle_group(
                country=country,
                name=(name + "_fuel"),
                _type=tanker_type,
                position=pad.position.point_from_heading(
                    vtol_pad[0].heading.degrees - 175, 35
                ),
                group_size=1,
                heading=pad.heading + 45,
                move_formation=PointAction.OffRoad,
            )
            self.m.vehicle_group(
                country=country,
                name=(name + "_ammo"),
                _type=ammo_truck_type,
                position=pad.position.point_from_heading(
                    vtol_pad[0].heading.degrees - 185, 35
                ),
                group_size=1,
                heading=pad.heading + 45,
                move_formation=PointAction.OffRoad,
            )
        else:
            self.m.static_group(
                country=country,
                name=(name + "_fuel"),
                _type=Fortification.FARP_Fuel_Depot,
                position=pad.position.point_from_heading(
                    vtol_pad[0].heading.degrees - 180, 45
                ),
                heading=pad.heading,
            )
            self.m.static_group(
                country=country,
                name=(name + "_ammo"),
                _type=Fortification.FARP_Ammo_Dump_Coating,
                position=pad.position.point_from_heading(
                    vtol_pad[0].heading.degrees - 180, 35
                ),
                heading=pad.heading + 270,
            )
        if self.game.settings.ground_start_ground_power_trucks:
            self.m.vehicle_group(
                country=country,
                name=(name + "_power"),
                _type=power_truck_type,
                position=pad.position.point_from_heading(
                    vtol_pad[0].heading.degrees - 185, 35
                ),
                group_size=1,
                heading=pad.heading + 45,
                move_formation=PointAction.OffRoad,
            )

    def generate(self) -> None:
        try:
            for i, vtol_pad in enumerate(self.cp.ground_spawns):
                self.create_ground_spawn(i, vtol_pad)
        except AttributeError:
            self.ground_spawns = []


class TgoGenerator:
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
        self.ground_spawns_large: dict[
            ControlPoint, list[Tuple[StaticGroup, Point]]
        ] = defaultdict(list)
        self.ground_spawns: dict[
            ControlPoint, list[Tuple[StaticGroup, Point]]
        ] = defaultdict(list)
        self.mission_data = mission_data

    def generate(self) -> None:
        for cp in self.game.theater.controlpoints:
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

            # Generate Large Ground Spawn slots
            ground_large_spawn_gen = GroundSpawnLargeGenerator(
                self.m, cp, self.game, self.radio_registry, self.tacan_registry
            )
            ground_large_spawn_gen.generate()
            self.ground_spawns_large[cp] = ground_large_spawn_gen.ground_spawns_large
            random.shuffle(self.ground_spawns_large[cp])

            # Generate Ground Spawn slots
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
                    generator = GroundObjectGenerator(
                        ground_object, country, self.game, self.m, self.unit_map
                    )
                generator.generate()
        self.mission_data.runways = list(self.runways.values())
