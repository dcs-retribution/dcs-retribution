from __future__ import annotations

import logging
import os
import random
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Optional, List, Type

from dcs import Mission
from dcs.action import DoScript, DoScriptFile
from dcs.ships import Stennis, CVN_71, CVN_72, CVN_73, CVN_75, Forrestal
from dcs.translation import String
from dcs.triggers import TriggerStart
from dcs.unittype import VehicleType, ShipType
from dcs.vehicles import AirDefence, Unarmed

from game.ato import FlightType
from game.coalition import Coalition
from game.data.units import UnitClass
from game.dcs.aircrafttype import AircraftType
from game.missiongenerator.luagenerator import LuaGenerator
from game.missiongenerator.missiondata import MissionData
from game.plugins import LuaPluginManager
from game.pretense.pretensetgogenerator import PretenseGroundObjectGenerator
from game.theater import Airfield, OffMapSpawn, TheaterGroundObject
from game.theater.iadsnetwork.iadsrole import IadsRole
from game.utils import escape_string_for_lua
from pydcs_extensions import IRON_DOME_LN, DAVID_SLING_LN

if TYPE_CHECKING:
    from game import Game

PRETENSE_RED_SIDE = 1
PRETENSE_BLUE_SIDE = 2
PRETENSE_NUMBER_OF_ZONES_TO_CONNECT_CARRIERS_TO = 2


@dataclass
class PretenseSam:
    name: str
    enabled: bool

    def __init__(
        self,
        name: str,
    ) -> None:
        self.name = name
        self.enabled = False


class PretenseLuaGenerator(LuaGenerator):
    def __init__(
        self,
        game: Game,
        mission: Mission,
        mission_data: MissionData,
    ) -> None:
        super().__init__(
            game,
            mission,
            mission_data,
        )

        self.game = game
        self.mission = mission
        self.mission_data = mission_data
        self.plugin_scripts: list[str] = []

    def generate(self) -> None:
        ewrj_triggers = [
            x for x in self.mission.triggerrules.triggers if isinstance(x, TriggerStart)
        ]
        self.generate_pretense_plugin_data()
        self.generate_plugin_data()
        self.inject_plugins()
        for t in ewrj_triggers:
            self.mission.triggerrules.triggers.remove(t)
            self.mission.triggerrules.triggers.append(t)

    def generate_plugin_data(self) -> None:
        lua_data = LuaData("dcsRetribution")

        install_path = lua_data.add_item("installPath")
        install_path.set_value(os.path.abspath("."))

        lua_data.add_item("Airbases")
        carriers_object = lua_data.add_item("Carriers")

        for carrier in self.mission_data.carriers:
            carrier_item = carriers_object.add_item()
            carrier_item.add_key_value("dcsGroupName", carrier.group_name)
            carrier_item.add_key_value("unit_name", carrier.unit_name)
            carrier_item.add_key_value("callsign", carrier.callsign)
            carrier_item.add_key_value("radio", str(carrier.freq.mhz))
            carrier_item.add_key_value(
                "tacan", str(carrier.tacan.number) + carrier.tacan.band.name
            )

        tankers_object = lua_data.add_item("Tankers")
        for tanker in self.mission_data.tankers:
            tanker_item = tankers_object.add_item()
            tanker_item.add_key_value("dcsGroupName", tanker.group_name)
            tanker_item.add_key_value("callsign", tanker.callsign)
            tanker_item.add_key_value("variant", tanker.variant)
            tanker_item.add_key_value("radio", str(tanker.freq.mhz))
            if tanker.tacan is not None:
                tanker_item.add_key_value(
                    "tacan", str(tanker.tacan.number) + tanker.tacan.band.name
                )

        awacs_object = lua_data.add_item("AWACs")
        for awacs in self.mission_data.awacs:
            awacs_item = awacs_object.add_item()
            awacs_item.add_key_value("dcsGroupName", awacs.group_name)
            awacs_item.add_key_value("callsign", awacs.callsign)
            awacs_item.add_key_value("radio", str(awacs.freq.mhz))

        jtacs_object = lua_data.add_item("JTACs")
        for jtac in self.mission_data.jtacs:
            jtac_item = jtacs_object.add_item()
            jtac_item.add_key_value("dcsGroupName", jtac.group_name)
            jtac_item.add_key_value("callsign", jtac.callsign)
            jtac_item.add_key_value("zone", jtac.region)
            jtac_item.add_key_value("dcsUnit", jtac.unit_name)
            jtac_item.add_key_value("laserCode", jtac.code)
            jtac_item.add_key_value("radio", str(jtac.freq.mhz))
            jtac_item.add_key_value("modulation", jtac.freq.modulation.name)

        logistics_object = lua_data.add_item("Logistics")
        logistics_flights = logistics_object.add_item("flights")
        crates_object = logistics_object.add_item("crates")
        spawnable_crates: dict[str, str] = {}
        transports: list[AircraftType] = []
        for logistic_info in self.mission_data.logistics:
            if logistic_info.transport not in transports:
                transports.append(logistic_info.transport)
            coalition_color = "blue" if logistic_info.blue else "red"
            logistics_item = logistics_flights.add_item()
            logistics_item.add_data_array("pilot_names", logistic_info.pilot_names)
            logistics_item.add_key_value("pickup_zone", logistic_info.pickup_zone)
            logistics_item.add_key_value("drop_off_zone", logistic_info.drop_off_zone)
            logistics_item.add_key_value("target_zone", logistic_info.target_zone)
            logistics_item.add_key_value("side", str(2 if logistic_info.blue else 1))
            logistics_item.add_key_value("logistic_unit", logistic_info.logistic_unit)
            logistics_item.add_key_value(
                "aircraft_type", logistic_info.transport.dcs_id
            )
            logistics_item.add_key_value(
                "preload", "true" if logistic_info.preload else "false"
            )
            for cargo in logistic_info.cargo:
                if cargo.unit_type not in spawnable_crates:
                    spawnable_crates[cargo.unit_type] = str(200 + len(spawnable_crates))
                crate_weight = spawnable_crates[cargo.unit_type]
                for i in range(cargo.amount):
                    cargo_item = crates_object.add_item()
                    cargo_item.add_key_value("weight", crate_weight)
                    cargo_item.add_key_value("coalition", coalition_color)
                    cargo_item.add_key_value("zone", cargo.spawn_zone)
        transport_object = logistics_object.add_item("transports")
        for transport in transports:
            transport_item = transport_object.add_item()
            transport_item.add_key_value("aircraft_type", transport.dcs_id)
            transport_item.add_key_value("cabin_size", str(transport.cabin_size))
            transport_item.add_key_value(
                "troops", "true" if transport.cabin_size > 0 else "false"
            )
            transport_item.add_key_value(
                "crates", "true" if transport.can_carry_crates else "false"
            )
        spawnable_crates_object = logistics_object.add_item("spawnable_crates")
        for unit, weight in spawnable_crates.items():
            crate_item = spawnable_crates_object.add_item()
            crate_item.add_key_value("unit", unit)
            crate_item.add_key_value("weight", weight)

        target_points = lua_data.add_item("TargetPoints")
        for flight in self.mission_data.flights:
            if flight.friendly and flight.flight_type in [
                FlightType.ANTISHIP,
                FlightType.DEAD,
                FlightType.SEAD,
                FlightType.STRIKE,
            ]:
                flight_type = str(flight.flight_type)
                flight_target = flight.package.target
                if flight_target:
                    flight_target_name = None
                    flight_target_type = None
                    if isinstance(flight_target, TheaterGroundObject):
                        flight_target_name = flight_target.obj_name
                        flight_target_type = (
                            flight_type + f" TGT ({flight_target.category})"
                        )
                    elif hasattr(flight_target, "name"):
                        flight_target_name = flight_target.name
                        flight_target_type = flight_type + " TGT (Airbase)"
                    target_item = target_points.add_item()
                    if flight_target_name:
                        target_item.add_key_value("name", flight_target_name)
                    if flight_target_type:
                        target_item.add_key_value("type", flight_target_type)
                    target_item.add_key_value(
                        "positionX", str(flight_target.position.x)
                    )
                    target_item.add_key_value(
                        "positionY", str(flight_target.position.y)
                    )

        for cp in self.game.theater.controlpoints:
            coalition_object = (
                lua_data.get_or_create_item("BlueAA")
                if cp.captured
                else lua_data.get_or_create_item("RedAA")
            )
            for ground_object in cp.ground_objects:
                for g in ground_object.groups:
                    threat_range = g.max_threat_range()

                    if not threat_range:
                        continue

                    aa_item = coalition_object.add_item()
                    aa_item.add_key_value("name", ground_object.name)
                    aa_item.add_key_value("range", str(threat_range.meters))
                    aa_item.add_key_value("positionX", str(ground_object.position.x))
                    aa_item.add_key_value("positionY", str(ground_object.position.y))

        # Generate IADS Lua Item
        iads_object = lua_data.add_item("IADS")
        for node in self.game.theater.iads_network.skynet_nodes(self.game):
            coalition = iads_object.get_or_create_item("BLUE" if node.player else "RED")
            iads_type = coalition.get_or_create_item(node.iads_role.value)
            iads_element = iads_type.add_item()
            iads_element.add_key_value("dcsGroupName", node.dcs_name)
            if node.iads_role in [IadsRole.SAM, IadsRole.SAM_AS_EWR]:
                # add additional SkynetProperties to SAM Sites
                for property, value in node.properties.items():
                    iads_element.add_key_value(property, value)
            for role, connections in node.connections.items():
                iads_element.add_data_array(role, connections)

        trigger = TriggerStart(comment="Set DCS Retribution data")
        trigger.add_action(DoScript(String(lua_data.create_operations_lua())))
        self.mission.triggerrules.triggers.append(trigger)

    @staticmethod
    def generate_sam_from_preset(
        preset: str, cp_side_str: str, cp_name_trimmed: str
    ) -> str:
        lua_string_zones = (
            "                presets.defenses."
            + cp_side_str
            + "."
            + preset
            + ":extend({ name='"
            + cp_name_trimmed
            + f"-{preset}-"
            + cp_side_str
            + "' }),\n"
        )
        return lua_string_zones

    def generate_pretense_land_upgrade_supply(self, cp_name: str, cp_side: int) -> str:
        lua_string_zones = ""
        cp_name_trimmed = "".join([i for i in cp_name.lower() if i.isalpha()])
        cp_side_str = "blue" if cp_side == PRETENSE_BLUE_SIDE else "red"
        cp = self.game.theater.controlpoints[0]
        for loop_cp in self.game.theater.controlpoints:
            if loop_cp.name == cp_name:
                cp = loop_cp
        sam_presets: dict[str, PretenseSam] = {}
        for sam_name in [
            "sa2",
            "sa3",
            "sa5",
            "sa6",
            "sa10",
            "sa11",
            "hawk",
            "patriot",
            "nasamsb",
            "nasamsc",
            "rapier",
            "roland",
            "hq7",
            "irondome",
            "davidsling",
        ]:
            sam_presets[sam_name] = PretenseSam(sam_name)

        lua_string_zones += "        presets.upgrades.supply.fuelTank:extend({\n"
        lua_string_zones += (
            "            name = '"
            + cp_name_trimmed
            + "-fueltank-"
            + cp_side_str
            + "',\n"
        )
        lua_string_zones += "            products = {\n"
        for ground_group in self.game.pretense_ground_supply[cp_side][cp_name_trimmed]:
            lua_string_zones += (
                "                presets.missions.supply.convoy:extend({ name='"
                + ground_group
                + "'}),\n"
            )
        for ground_group in self.game.pretense_ground_assault[cp_side][cp_name_trimmed]:
            lua_string_zones += (
                "                presets.missions.attack.surface:extend({ name='"
                + ground_group
                + "'}),\n"
            )
        for mission_type in self.game.pretense_air[cp_side][cp_name_trimmed]:
            if mission_type == FlightType.AIR_ASSAULT:
                mission_name = "supply.helo"
                for air_group in self.game.pretense_air[cp_side][cp_name_trimmed][
                    mission_type
                ]:
                    lua_string_zones += (
                        f"                presets.missions.{mission_name}:extend"
                        + "({name='"
                        + air_group
                        + "'}),\n"
                    )
        lua_string_zones += "            }\n"
        lua_string_zones += "        }),\n"
        lua_string_zones += "        presets.upgrades.airdef.bunker:extend({\n"
        lua_string_zones += (
            f"            name = '{cp_name_trimmed}-shorad-command-"
            + cp_side_str
            + "',\n"
        )
        lua_string_zones += "            products = {\n"
        lua_string_zones += (
            "                presets.defenses."
            + cp_side_str
            + ".shorad:extend({ name='"
            + cp_name_trimmed
            + "-shorad-"
            + cp_side_str
            + "' }),\n"
        )
        lua_string_zones += "            }\n"
        lua_string_zones += "        }),\n"

        for ground_object in cp.ground_objects:
            for ground_unit in ground_object.units:
                if ground_unit.unit_type is not None:
                    if ground_unit.unit_type.dcs_unit_type == AirDefence.S_75M_Volhov:
                        sam_presets["sa2"].enabled = True
                    if (
                        ground_unit.unit_type.dcs_unit_type
                        == AirDefence.X_5p73_s_125_ln
                    ):
                        sam_presets["sa3"].enabled = True
                    if ground_unit.unit_type.dcs_unit_type == AirDefence.S_200_Launcher:
                        sam_presets["sa5"].enabled = True
                    if ground_unit.unit_type.dcs_unit_type == AirDefence.Kub_2P25_ln:
                        sam_presets["sa6"].enabled = True
                    if (
                        ground_unit.unit_type.dcs_unit_type
                        == AirDefence.S_300PS_5P85C_ln
                        or ground_unit.unit_type.dcs_unit_type
                        == AirDefence.S_300PS_5P85D_ln
                    ):
                        sam_presets["sa10"].enabled = True
                    if (
                        ground_unit.unit_type.dcs_unit_type
                        == AirDefence.SA_11_Buk_LN_9A310M1
                    ):
                        sam_presets["sa11"].enabled = True
                    if ground_unit.unit_type.dcs_unit_type == AirDefence.Hawk_ln:
                        sam_presets["hawk"].enabled = True
                    if ground_unit.unit_type.dcs_unit_type == AirDefence.Patriot_ln:
                        sam_presets["patriot"].enabled = True
                    if ground_unit.unit_type.dcs_unit_type == AirDefence.NASAMS_LN_B:
                        sam_presets["nasamsb"].enabled = True
                    if ground_unit.unit_type.dcs_unit_type == AirDefence.NASAMS_LN_C:
                        sam_presets["nasamsc"].enabled = True
                    if (
                        ground_unit.unit_type.dcs_unit_type
                        == AirDefence.Rapier_fsa_launcher
                    ):
                        sam_presets["rapier"].enabled = True
                    if ground_unit.unit_type.dcs_unit_type == AirDefence.Roland_ADS:
                        sam_presets["roland"].enabled = True
                    if ground_unit.unit_type.dcs_unit_type == AirDefence.HQ_7_STR_SP:
                        sam_presets["hq7"].enabled = True
                    if ground_unit.unit_type.dcs_unit_type == IRON_DOME_LN:
                        sam_presets["irondome"].enabled = True
                    if ground_unit.unit_type.dcs_unit_type == DAVID_SLING_LN:
                        sam_presets["davidsling"].enabled = True

        cp_has_sams = False
        for sam_name in sam_presets:
            if sam_presets[sam_name].enabled:
                cp_has_sams = True
                break
        if cp_has_sams:
            lua_string_zones += "        presets.upgrades.airdef.comCenter:extend({\n"
            lua_string_zones += (
                f"            name = '{cp_name_trimmed}-sam-command-"
                + cp_side_str
                + "',\n"
            )
            lua_string_zones += "            products = {\n"
            for sam_name in sam_presets:
                if sam_presets[sam_name].enabled:
                    lua_string_zones += self.generate_sam_from_preset(
                        sam_name, cp_side_str, cp_name_trimmed
                    )
            lua_string_zones += "            }\n"
            lua_string_zones += "        }),\n"

        lua_string_zones += "        presets.upgrades.supply.hangar:extend({\n"
        lua_string_zones += (
            f"            name = '{cp_name_trimmed}-aircraft-command-"
            + cp_side_str
            + "',\n"
        )
        lua_string_zones += "            products = {\n"
        for mission_type in self.game.pretense_air[cp_side][cp_name_trimmed]:
            if mission_type in (FlightType.SEAD, FlightType.DEAD):
                mission_name = "attack.sead"
                for air_group in self.game.pretense_air[cp_side][cp_name_trimmed][
                    mission_type
                ]:
                    lua_string_zones += (
                        f"                presets.missions.{mission_name}:extend"
                        + "({name='"
                        + air_group
                        + "', altitude=25000, expend=AI.Task.WeaponExpend.ALL}),\n"
                    )
            elif mission_type == FlightType.CAS:
                mission_name = "attack.cas"
                for air_group in self.game.pretense_air[cp_side][cp_name_trimmed][
                    mission_type
                ]:
                    flight = self.game.pretense_air_groups[air_group]
                    if flight.is_helo:
                        mission_name = "attack.helo"
                    lua_string_zones += (
                        f"                presets.missions.{mission_name}:extend"
                        + "({name='"
                        + air_group
                        + "', altitude=15000, expend=AI.Task.WeaponExpend.QUARTER}),\n"
                    )
            elif mission_type == FlightType.BAI:
                mission_name = "attack.bai"
                for air_group in self.game.pretense_air[cp_side][cp_name_trimmed][
                    mission_type
                ]:
                    lua_string_zones += (
                        f"                presets.missions.{mission_name}:extend"
                        + "({name='"
                        + air_group
                        + "', altitude=10000, expend=AI.Task.WeaponExpend.QUARTER}),\n"
                    )
            elif mission_type == FlightType.STRIKE:
                mission_name = "attack.strike"
                for air_group in self.game.pretense_air[cp_side][cp_name_trimmed][
                    mission_type
                ]:
                    lua_string_zones += (
                        f"                presets.missions.{mission_name}:extend"
                        + "({name='"
                        + air_group
                        + "', altitude=20000, expend=AI.Task.WeaponExpend.ALL}),\n"
                    )
            elif mission_type == FlightType.BARCAP:
                mission_name = "patrol.aircraft"
                for air_group in self.game.pretense_air[cp_side][cp_name_trimmed][
                    mission_type
                ]:
                    lua_string_zones += (
                        f"                presets.missions.{mission_name}:extend"
                        + "({name='"
                        + air_group
                        + "', altitude=25000, range=25}),\n"
                    )
            elif mission_type == FlightType.REFUELING:
                mission_name = "support.tanker"
                for air_group in self.game.pretense_air[cp_side][cp_name_trimmed][
                    mission_type
                ]:
                    tanker_freq = 257.0
                    tanker_tacan = 37.0
                    tanker_variant = "Drogue"
                    for tanker in self.mission_data.tankers:
                        if tanker.group_name == air_group:
                            tanker_freq = tanker.freq.hertz / 1000000
                            tanker_tacan = tanker.tacan.number if tanker.tacan else 0.0
                            if tanker.variant == "KC-135 Stratotanker":
                                tanker_variant = "Boom"
                    lua_string_zones += (
                        f"                presets.missions.{mission_name}:extend"
                        + "({name='"
                        + air_group
                        + "', freq='"
                        + str(tanker_freq)
                        + "', tacan='"
                        + str(tanker_tacan)
                        + "', variant='"
                        + tanker_variant
                        + "'}),\n"
                    )
            elif mission_type == FlightType.AEWC:
                mission_name = "support.awacs"
                for air_group in self.game.pretense_air[cp_side][cp_name_trimmed][
                    mission_type
                ]:
                    awacs_freq = 257.5
                    for awacs in self.mission_data.awacs:
                        if awacs.group_name == air_group:
                            awacs_freq = awacs.freq.hertz / 1000000
                    lua_string_zones += (
                        f"                presets.missions.{mission_name}:extend"
                        + "({name='"
                        + air_group
                        + "', freq="
                        + str(awacs_freq)
                        + "}),\n"
                    )
        lua_string_zones += "            }\n"
        lua_string_zones += "        })\n"

        return lua_string_zones

    def generate_pretense_sea_upgrade_supply(self, cp_name: str, cp_side: int) -> str:
        lua_string_zones = ""
        cp_name_trimmed = "".join([i for i in cp_name.lower() if i.isalpha()])
        cp_side_str = "blue" if cp_side == PRETENSE_BLUE_SIDE else "red"

        supply_ship = "oilPump"
        tanker_ship = "chemTank"
        command_ship = "comCenter"

        lua_string_zones += (
            "        presets.upgrades.supply." + supply_ship + ":extend({\n"
        )
        lua_string_zones += (
            "            name = '"
            + cp_name_trimmed
            + f"-{supply_ship}-"
            + cp_side_str
            + "',\n"
        )
        lua_string_zones += "            products = {\n"
        for ground_group in self.game.pretense_ground_supply[cp_side][cp_name_trimmed]:
            lua_string_zones += (
                "                presets.missions.supply.convoy:extend({ name='"
                + ground_group
                + "'}),\n"
            )
        for ground_group in self.game.pretense_ground_assault[cp_side][cp_name_trimmed]:
            lua_string_zones += (
                "                presets.missions.attack.surface:extend({ name='"
                + ground_group
                + "'}),\n"
            )
        for mission_type in self.game.pretense_air[cp_side][cp_name_trimmed]:
            if mission_type == FlightType.AIR_ASSAULT:
                mission_name = "supply.helo"
                for air_group in self.game.pretense_air[cp_side][cp_name_trimmed][
                    mission_type
                ]:
                    lua_string_zones += (
                        f"                presets.missions.{mission_name}:extend"
                        + "({name='"
                        + air_group
                        + "'}),\n"
                    )
        lua_string_zones += "            }\n"
        lua_string_zones += "        }),\n"
        lua_string_zones += (
            "        presets.upgrades.airdef." + command_ship + ":extend({\n"
        )
        lua_string_zones += (
            f"            name = '{cp_name_trimmed}-mission-command-"
            + cp_side_str
            + "',\n"
        )
        lua_string_zones += "            products = {\n"
        lua_string_zones += (
            "                presets.defenses."
            + cp_side_str
            + ".shorad:extend({ name='"
            + cp_name_trimmed
            + "-shorad-"
            + cp_side_str
            + "' }),\n"
        )
        lua_string_zones += "            }\n"
        lua_string_zones += "        }),\n"
        lua_string_zones += (
            "        presets.upgrades.attack." + tanker_ship + ":extend({\n"
        )
        lua_string_zones += (
            f"            name = '{cp_name_trimmed}-aircraft-command-"
            + cp_side_str
            + "',\n"
        )
        lua_string_zones += "            products = {\n"
        for mission_type in self.game.pretense_air[cp_side][cp_name_trimmed]:
            if mission_type == FlightType.SEAD:
                mission_name = "attack.sead"
                for air_group in self.game.pretense_air[cp_side][cp_name_trimmed][
                    mission_type
                ]:
                    lua_string_zones += (
                        f"                presets.missions.{mission_name}:extend"
                        + "({name='"
                        + air_group
                        + "', altitude=25000, expend=AI.Task.WeaponExpend.ALL}),\n"
                    )
            elif mission_type == FlightType.CAS:
                mission_name = "attack.cas"
                for air_group in self.game.pretense_air[cp_side][cp_name_trimmed][
                    mission_type
                ]:
                    flight = self.game.pretense_air_groups[air_group]
                    if flight.is_helo:
                        mission_name = "attack.helo"
                    lua_string_zones += (
                        f"                presets.missions.{mission_name}:extend"
                        + "({name='"
                        + air_group
                        + "', altitude=15000, expend=AI.Task.WeaponExpend.QUARTER}),\n"
                    )
            elif mission_type == FlightType.BAI:
                mission_name = "attack.bai"
                for air_group in self.game.pretense_air[cp_side][cp_name_trimmed][
                    mission_type
                ]:
                    lua_string_zones += (
                        f"                presets.missions.{mission_name}:extend"
                        + "({name='"
                        + air_group
                        + "', altitude=10000, expend=AI.Task.WeaponExpend.QUARTER}),\n"
                    )
            elif mission_type == FlightType.STRIKE:
                mission_name = "attack.strike"
                for air_group in self.game.pretense_air[cp_side][cp_name_trimmed][
                    mission_type
                ]:
                    lua_string_zones += (
                        f"                presets.missions.{mission_name}:extend"
                        + "({name='"
                        + air_group
                        + "', altitude=20000, expend=AI.Task.WeaponExpend.ALL}),\n"
                    )
            elif mission_type == FlightType.BARCAP:
                mission_name = "patrol.aircraft"
                for air_group in self.game.pretense_air[cp_side][cp_name_trimmed][
                    mission_type
                ]:
                    lua_string_zones += (
                        f"                presets.missions.{mission_name}:extend"
                        + "({name='"
                        + air_group
                        + "', altitude=25000, range=25}),\n"
                    )
            elif mission_type == FlightType.REFUELING:
                mission_name = "support.tanker"
                for air_group in self.game.pretense_air[cp_side][cp_name_trimmed][
                    mission_type
                ]:
                    tanker_freq = 257.0
                    tanker_tacan = 37.0
                    tanker_variant = "Drogue"
                    for tanker in self.mission_data.tankers:
                        if tanker.group_name == air_group:
                            tanker_freq = tanker.freq.hertz / 1000000
                            tanker_tacan = tanker.tacan.number if tanker.tacan else 0.0
                            if tanker.variant == "KC-135 Stratotanker":
                                tanker_variant = "Boom"
                    lua_string_zones += (
                        f"                presets.missions.{mission_name}:extend"
                        + "({name='"
                        + air_group
                        + "', freq='"
                        + str(tanker_freq)
                        + "', tacan='"
                        + str(tanker_tacan)
                        + "', variant='"
                        + tanker_variant
                        + "'}),\n"
                    )
            elif mission_type == FlightType.AEWC:
                mission_name = "support.awacs"
                for air_group in self.game.pretense_air[cp_side][cp_name_trimmed][
                    mission_type
                ]:
                    awacs_freq = 257.5
                    for awacs in self.mission_data.awacs:
                        if awacs.group_name == air_group:
                            awacs_freq = awacs.freq.hertz / 1000000
                    lua_string_zones += (
                        f"                presets.missions.{mission_name}:extend"
                        + "({name='"
                        + air_group
                        + "', freq="
                        + str(awacs_freq)
                        + "}),\n"
                    )
        lua_string_zones += "            }\n"
        lua_string_zones += "        })\n"

        return lua_string_zones

    def generate_pretense_zone_land(self, cp_name: str) -> str:
        is_artillery_zone = random.choice([True, False])

        lua_string_zones = ""
        cp_name_trimmed = "".join([i for i in cp_name.lower() if i.isalpha()])

        lua_string_zones += f"zones.{cp_name_trimmed}:defineUpgrades(" + "{\n"
        lua_string_zones += "    [1] = { --red side\n"
        lua_string_zones += "        presets.upgrades.basic.tent:extend({\n"
        lua_string_zones += f"            name='{cp_name_trimmed}-tent-red',\n"
        lua_string_zones += "            products = {\n"
        if not is_artillery_zone:
            lua_string_zones += (
                "                presets.special.red.infantry:extend({ name='"
                + cp_name_trimmed
                + "-defense-red'})\n"
            )
        lua_string_zones += "            }\n"
        lua_string_zones += "        }),\n"
        lua_string_zones += "        presets.upgrades.basic.comPost:extend({\n"
        lua_string_zones += f"            name = '{cp_name_trimmed}-com-red',\n"
        lua_string_zones += "            products = {\n"
        lua_string_zones += (
            "                presets.special.red.infantry:extend({ name='"
            + cp_name_trimmed
            + "-defense-red'}),\n"
        )
        if not is_artillery_zone:
            lua_string_zones += (
                "                presets.defenses.red.infantry:extend({ name='"
                + cp_name_trimmed
                + "-garrison-red' })\n"
            )
        lua_string_zones += "            }\n"
        lua_string_zones += "        }),\n"
        if is_artillery_zone:
            lua_string_zones += "        presets.upgrades.basic.artyBunker:extend({\n"
            lua_string_zones += f"            name='{cp_name_trimmed}-arty-red',\n"
            lua_string_zones += "            products = {\n"
            lua_string_zones += (
                "                presets.defenses.red.artillery:extend({ name='"
                + cp_name_trimmed
                + "-artillery-red'})\n"
            )
            lua_string_zones += "            }\n"
            lua_string_zones += "        }),\n"

        lua_string_zones += self.generate_pretense_land_upgrade_supply(
            cp_name, PRETENSE_RED_SIDE
        )

        lua_string_zones += "    },\n"
        lua_string_zones += "    [2] = --blue side\n"
        lua_string_zones += "    {\n"
        lua_string_zones += "        presets.upgrades.basic.tent:extend({\n"
        lua_string_zones += f"            name='{cp_name_trimmed}-tent-blue',\n"
        lua_string_zones += "            products = {\n"
        if not is_artillery_zone:
            lua_string_zones += (
                "                presets.special.blue.infantry:extend({ name='"
                + cp_name_trimmed
                + "-defense-blue'})\n"
            )
        lua_string_zones += "            }\n"
        lua_string_zones += "        }),\n"
        lua_string_zones += "        presets.upgrades.basic.comPost:extend({\n"
        lua_string_zones += f"            name = '{cp_name_trimmed}-com-blue',\n"
        lua_string_zones += "            products = {\n"
        lua_string_zones += (
            "                presets.special.blue.infantry:extend({ name='"
            + cp_name_trimmed
            + "-defense-blue'}),\n"
        )
        if not is_artillery_zone:
            lua_string_zones += (
                "                presets.defenses.blue.infantry:extend({ name='"
                + cp_name_trimmed
                + "-garrison-blue' })\n"
            )
        lua_string_zones += "            }\n"
        lua_string_zones += "        }),\n"
        if is_artillery_zone:
            lua_string_zones += "        presets.upgrades.basic.artyBunker:extend({\n"
            lua_string_zones += f"            name='{cp_name_trimmed}-arty-blue',\n"
            lua_string_zones += "            products = {\n"
            lua_string_zones += (
                "                presets.defenses.blue.artillery:extend({ name='"
                + cp_name_trimmed
                + "-artillery-blue'})\n"
            )
            lua_string_zones += "            }\n"
            lua_string_zones += "        }),\n"

        lua_string_zones += self.generate_pretense_land_upgrade_supply(
            cp_name, PRETENSE_BLUE_SIDE
        )

        lua_string_zones += "    }\n"
        lua_string_zones += "})\n"

        return lua_string_zones

    def generate_pretense_zone_sea(self, cp_name: str) -> str:
        lua_string_zones = ""
        cp_name_trimmed = "".join([i for i in cp_name.lower() if i.isalpha()])

        lua_string_zones += f"zones.{cp_name_trimmed}:defineUpgrades(" + "{\n"
        lua_string_zones += "    [1] = { --red side\n"

        lua_string_zones += self.generate_pretense_sea_upgrade_supply(
            cp_name, PRETENSE_RED_SIDE
        )

        lua_string_zones += "    },\n"
        lua_string_zones += "    [2] = --blue side\n"
        lua_string_zones += "    {\n"

        lua_string_zones += self.generate_pretense_sea_upgrade_supply(
            cp_name, PRETENSE_BLUE_SIDE
        )

        lua_string_zones += "    }\n"
        lua_string_zones += "})\n"

        return lua_string_zones

    def generate_pretense_carrier_zones(self) -> str:
        lua_string_carrier_zones = "cmap1 = CarrierMap:new({"
        for zone_name in self.game.pretense_carrier_zones:
            lua_string_carrier_zones += f'"{zone_name}",'
        lua_string_carrier_zones += "})\n"

        return lua_string_carrier_zones

    def generate_pretense_carriers(
        self,
        cp_name: str,
        cp_side: int,
        cp_carrier_group_type: Type[ShipType] | None,
        cp_carrier_group_name: str | None,
    ) -> str:
        lua_string_carrier = "\n"
        cp_name_trimmed = "".join([i for i in cp_name.lower() if i.isalpha()])

        link4carriers = [Stennis, CVN_71, CVN_72, CVN_73, CVN_75, Forrestal]
        is_link4carrier = False
        carrier_unit_name = ""
        icls_channel = 10
        link4_freq = 339000000
        tacan_channel = 44
        tacan_callsign = ""
        radio = 137500000
        if cp_carrier_group_type is not None:
            if cp_carrier_group_type in link4carriers:
                is_link4carrier = True
        else:
            return lua_string_carrier
        if cp_carrier_group_name is None:
            return lua_string_carrier

        for carrier in self.mission_data.carriers:
            if cp_carrier_group_name == carrier.group_name:
                carrier_unit_name = carrier.unit_name
                tacan_channel = carrier.tacan.number
                tacan_callsign = carrier.callsign
                radio = carrier.freq.hertz
                if carrier.link4_freq is not None:
                    link4_freq = carrier.link4_freq.hertz
                if carrier.icls_channel is not None:
                    icls_channel = carrier.icls_channel
                break

        lua_string_carrier += (
            f'{cp_name_trimmed} = CarrierCommand:new("'
            + carrier_unit_name
            + '", 3000, cmap1:getNavMap(), '
            + "{\n"
        )
        if is_link4carrier:
            lua_string_carrier += "	icls = " + str(icls_channel) + ",\n"
            lua_string_carrier += "	acls = true,\n"
            lua_string_carrier += "	link4 = " + str(link4_freq) + ",\n"
        lua_string_carrier += (
            "	tacan = {channel = "
            + str(tacan_channel)
            + ', callsign="'
            + tacan_callsign
            + '"},\n'
        )
        lua_string_carrier += "	radio = " + str(radio) + "\n"
        lua_string_carrier += "}, 30000)\n"

        for mission_type in self.game.pretense_air[cp_side][cp_name_trimmed]:
            if mission_type == FlightType.SEAD:
                mission_name = "supportTypes.strike"
                for air_group in self.game.pretense_air[cp_side][cp_name_trimmed][
                    mission_type
                ]:
                    lua_string_carrier += (
                        f'{cp_name_trimmed}:addSupportFlight("{air_group}", 1000, CarrierCommand.{mission_name}, '
                        + "{altitude = 25000, expend=AI.Task.WeaponExpend.ALL})\n"
                    )
            elif mission_type == FlightType.CAS:
                mission_name = "supportTypes.strike"
                for air_group in self.game.pretense_air[cp_side][cp_name_trimmed][
                    mission_type
                ]:
                    lua_string_carrier += (
                        f'{cp_name_trimmed}:addSupportFlight("{air_group}", 1000, CarrierCommand.{mission_name}, '
                        + "{altitude = 15000, expend=AI.Task.WeaponExpend.QUARTER})\n"
                    )
            elif mission_type == FlightType.BAI:
                mission_name = "supportTypes.strike"
                for air_group in self.game.pretense_air[cp_side][cp_name_trimmed][
                    mission_type
                ]:
                    lua_string_carrier += (
                        f'{cp_name_trimmed}:addSupportFlight("{air_group}", 1000, CarrierCommand.{mission_name}, '
                        + "{altitude = 10000, expend=AI.Task.WeaponExpend.QUARTER})\n"
                    )
            elif mission_type == FlightType.STRIKE:
                mission_name = "supportTypes.strike"
                for air_group in self.game.pretense_air[cp_side][cp_name_trimmed][
                    mission_type
                ]:
                    lua_string_carrier += (
                        f'{cp_name_trimmed}:addSupportFlight("{air_group}", 2000, CarrierCommand.{mission_name}, '
                        + "{altitude = 20000})\n"
                    )
            elif mission_type == FlightType.BARCAP:
                mission_name = "supportTypes.cap"
                for air_group in self.game.pretense_air[cp_side][cp_name_trimmed][
                    mission_type
                ]:
                    lua_string_carrier += (
                        f'{cp_name_trimmed}:addSupportFlight("{air_group}", 1000, CarrierCommand.{mission_name}, '
                        + "{altitude = 25000, range=25})\n"
                    )
            elif mission_type == FlightType.REFUELING:
                mission_name = "supportTypes.tanker"
                for air_group in self.game.pretense_air[cp_side][cp_name_trimmed][
                    mission_type
                ]:
                    tanker_freq = 257.0
                    tanker_tacan = 37.0
                    tanker_variant = "Drogue"
                    for tanker in self.mission_data.tankers:
                        if tanker.group_name == air_group:
                            tanker_freq = tanker.freq.hertz / 1000000
                            tanker_tacan = tanker.tacan.number if tanker.tacan else 0.0
                            if tanker.variant == "KC-135 Stratotanker":
                                tanker_variant = "Boom"
                    lua_string_carrier += (
                        f'{cp_name_trimmed}:addSupportFlight("{air_group}", 3000, CarrierCommand.{mission_name}, '
                        + "{altitude = 19000, freq="
                        + str(tanker_freq)
                        + ", tacan="
                        + str(tanker_tacan)
                        + "})\n"
                    )
            elif mission_type == FlightType.AEWC:
                mission_name = "supportTypes.awacs"
                for air_group in self.game.pretense_air[cp_side][cp_name_trimmed][
                    mission_type
                ]:
                    awacs_freq = 257.5
                    for awacs in self.mission_data.awacs:
                        if awacs.group_name == air_group:
                            awacs_freq = awacs.freq.hertz / 1000000
                    lua_string_carrier += (
                        f'{cp_name_trimmed}:addSupportFlight("{air_group}", 5000, CarrierCommand.{mission_name}, '
                        + "{altitude = 30000, freq="
                        + str(awacs_freq)
                        + "})\n"
                    )

        # lua_string_carrier += f'{cp_name_trimmed}:addExtraSupport("BGM-109B", 10000, CarrierCommand.supportTypes.mslstrike, ' + '{salvo = 10, wpType = \'weapons.missiles.BGM_109B\'})\n'

        return lua_string_carrier

    def get_ground_unit(
        self, coalition: Coalition, side: int, desired_unit_classes: list[UnitClass]
    ) -> str:
        ammo_trucks: List[Type[VehicleType]] = [
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
            Unarmed.Blitz_36_6700A,
            Unarmed.M_818,
            Unarmed.Bedford_MWD,
        ]

        for unit_class in desired_unit_classes:
            if coalition.faction.has_access_to_unit_class(unit_class):
                dcs_unit_type = PretenseGroundObjectGenerator.ground_unit_of_class(
                    coalition=coalition, unit_class=unit_class
                )
                if (
                    dcs_unit_type is not None
                    and unit_class == UnitClass.LOGISTICS
                    and dcs_unit_type.dcs_unit_type.__class__ not in ammo_trucks
                ):
                    # ground_unit_of_class returned a logistics unit not capable of ammo resupply
                    # Retry up to 10 times
                    for truck_retry in range(10):
                        dcs_unit_type = (
                            PretenseGroundObjectGenerator.ground_unit_of_class(
                                coalition=coalition, unit_class=unit_class
                            )
                        )
                        if (
                            dcs_unit_type is not None
                            and dcs_unit_type.dcs_unit_type in ammo_trucks
                        ):
                            break
                        else:
                            dcs_unit_type = None
                if dcs_unit_type is not None:
                    return dcs_unit_type.dcs_id

        # Faction did not contain any of the desired unit classes.
        # Fall back to defaults.
        if desired_unit_classes[0] == UnitClass.TANK:
            if side == PRETENSE_BLUE_SIDE:
                return "M-1 Abrams"
            else:
                return "T-90"
        elif desired_unit_classes[0] == UnitClass.ATGM:
            if side == PRETENSE_BLUE_SIDE:
                return "M1134 Stryker ATGM"
            else:
                return "BTR_D"
        elif desired_unit_classes[0] == UnitClass.IFV:
            if side == PRETENSE_BLUE_SIDE:
                return "M1128 Stryker MGS"
            else:
                return "BMP-3"
        elif desired_unit_classes[0] == UnitClass.APC:
            if side == PRETENSE_BLUE_SIDE:
                return "LAV-25"
            else:
                return "BTR-80"
        elif desired_unit_classes[0] == UnitClass.ARTILLERY:
            if side == PRETENSE_BLUE_SIDE:
                return "M-109"
            else:
                return "SAU Gvozdika"
        elif desired_unit_classes[0] == UnitClass.RECON:
            if side == PRETENSE_BLUE_SIDE:
                return "M1043 HMMWV Armament"
            else:
                return "BRDM-2"
        elif desired_unit_classes[0] == UnitClass.SHORAD:
            if side == PRETENSE_BLUE_SIDE:
                return "Roland ADS"
            else:
                return "2S6 Tunguska"
        elif desired_unit_classes[0] == UnitClass.AAA:
            if side == PRETENSE_BLUE_SIDE:
                return "bofors40"
            else:
                return "KS-19"
        elif desired_unit_classes[0] == UnitClass.MANPAD:
            if coalition.game.date.year >= 1990:
                if side == PRETENSE_BLUE_SIDE:
                    return "Soldier stinger"
                else:
                    return "SA-18 Igla manpad"
            else:
                if side == PRETENSE_BLUE_SIDE:
                    return "Soldier M4"
                else:
                    return "Infantry AK"
        elif desired_unit_classes[0] == UnitClass.LOGISTICS:
            if side == PRETENSE_BLUE_SIDE:
                return "M 818"
            else:
                return "Ural-4320T"
        else:
            if side == PRETENSE_BLUE_SIDE:
                return "Soldier M4"
            else:
                return "Infantry AK"

    def generate_pretense_ground_groups(self, side: int) -> str:
        if side == PRETENSE_BLUE_SIDE:
            side_str = "blue"
            skill_str = self.game.settings.player_skill
            coalition = self.game.blue
        else:
            side_str = "red"
            skill_str = self.game.settings.enemy_vehicle_skill
            coalition = self.game.red

        lua_string_ground_groups = ""

        lua_string_ground_groups += (
            'TemplateDB.templates["infantry-' + side_str + '"] = {\n'
        )
        lua_string_ground_groups += "    units = {\n"
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.IFV, UnitClass.APC, UnitClass.RECON])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.TANK, UnitClass.ATGM, UnitClass.IFV, UnitClass.APC, UnitClass.RECON])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.TANK, UnitClass.ATGM, UnitClass.IFV, UnitClass.APC, UnitClass.RECON])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.INFANTRY])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.INFANTRY])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.INFANTRY])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.INFANTRY])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.INFANTRY])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.MANPAD, UnitClass.INFANTRY])}"\n'
        lua_string_ground_groups += "            },\n"
        lua_string_ground_groups += f'            skill = "{skill_str}",\n'
        lua_string_ground_groups += "            dataCategory = TemplateDB.type.group\n"
        lua_string_ground_groups += "}\n"

        lua_string_ground_groups += (
            'TemplateDB.templates["artillery-' + side_str + '"] = {\n'
        )
        lua_string_ground_groups += "    units = {\n"
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.ARTILLERY])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.ARTILLERY])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.ARTILLERY])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.ARTILLERY])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.INFANTRY])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.INFANTRY])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.INFANTRY])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.INFANTRY])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.MANPAD, UnitClass.INFANTRY])}"\n'
        lua_string_ground_groups += "            },\n"
        lua_string_ground_groups += f'            skill = "{skill_str}",\n'
        lua_string_ground_groups += "            dataCategory = TemplateDB.type.group\n"
        lua_string_ground_groups += "}\n"

        lua_string_ground_groups += (
            'TemplateDB.templates["defense-' + side_str + '"] = {\n'
        )
        lua_string_ground_groups += "    units = {\n"
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.INFANTRY])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.INFANTRY])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.INFANTRY])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.INFANTRY])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.MANPAD, UnitClass.INFANTRY])}"\n'
        lua_string_ground_groups += "            },\n"
        lua_string_ground_groups += f'            skill = "{skill_str}",\n'
        lua_string_ground_groups += "            dataCategory = TemplateDB.type.group\n"
        lua_string_ground_groups += "}\n"

        lua_string_ground_groups += (
            'TemplateDB.templates["shorad-' + side_str + '"] = {\n'
        )
        lua_string_ground_groups += "    units = {\n"
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.SHORAD, UnitClass.AAA, UnitClass.MANPAD])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.SHORAD, UnitClass.AAA, UnitClass.MANPAD])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.AAA, UnitClass.SHORAD, UnitClass.MANPAD])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.AAA, UnitClass.SHORAD, UnitClass.MANPAD])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}"\n'
        lua_string_ground_groups += "            },\n"
        lua_string_ground_groups += "            maxDist = 300,\n"
        lua_string_ground_groups += f'            skill = "{skill_str}",\n'
        lua_string_ground_groups += "            dataCategory = TemplateDB.type.group\n"
        lua_string_ground_groups += "}\n"

        lua_string_ground_groups += 'TemplateDB.templates["sa2-' + side_str + '"] = {\n'
        lua_string_ground_groups += "    units = {\n"
        lua_string_ground_groups += '                "p-19 s-125 sr",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += '                "S_75M_Volhov",\n'
        lua_string_ground_groups += '                "S_75M_Volhov",\n'
        lua_string_ground_groups += '                "S_75M_Volhov",\n'
        lua_string_ground_groups += '                "S_75M_Volhov",\n'
        lua_string_ground_groups += '                "S_75M_Volhov",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.SHORAD, UnitClass.AAA, UnitClass.MANPAD])}",\n'
        lua_string_ground_groups += '                "RD_75",\n'
        lua_string_ground_groups += '                "SNR_75V"\n'
        lua_string_ground_groups += "            },\n"
        lua_string_ground_groups += "            maxDist = 300,\n"
        lua_string_ground_groups += f'            skill = "{skill_str}",\n'
        lua_string_ground_groups += "            dataCategory = TemplateDB.type.group\n"
        lua_string_ground_groups += "}\n"

        lua_string_ground_groups += (
            'TemplateDB.templates["hawk-' + side_str + '"] = {\n'
        )
        lua_string_ground_groups += "    units = {\n"
        lua_string_ground_groups += '                "Hawk pcp",\n'
        lua_string_ground_groups += '                "Hawk cwar",\n'
        lua_string_ground_groups += '                "Hawk ln",\n'
        lua_string_ground_groups += '                "Hawk ln",\n'
        lua_string_ground_groups += '                "Hawk ln",\n'
        lua_string_ground_groups += '                "Hawk ln",\n'
        lua_string_ground_groups += '                "Hawk ln",\n'
        lua_string_ground_groups += '                "Hawk tr",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += '                "Hawk sr"\n'
        lua_string_ground_groups += "            },\n"
        lua_string_ground_groups += "            maxDist = 300,\n"
        lua_string_ground_groups += f'            skill = "{skill_str}",\n'
        lua_string_ground_groups += "            dataCategory = TemplateDB.type.group\n"
        lua_string_ground_groups += "}\n"

        lua_string_ground_groups += (
            'TemplateDB.templates["patriot-' + side_str + '"] = {\n'
        )
        lua_string_ground_groups += "    units = {\n"
        lua_string_ground_groups += '                "Patriot cp",\n'
        lua_string_ground_groups += '                "Patriot str",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += '                "Patriot ln",\n'
        lua_string_ground_groups += '                "Patriot ln",\n'
        lua_string_ground_groups += '                "Patriot ln",\n'
        lua_string_ground_groups += '                "Patriot ln",\n'
        lua_string_ground_groups += '                "Patriot str",\n'
        lua_string_ground_groups += '                "Patriot str",\n'
        lua_string_ground_groups += '                "Patriot str",\n'
        lua_string_ground_groups += '                "Patriot EPP",\n'
        lua_string_ground_groups += '                "Patriot ECS",\n'
        lua_string_ground_groups += '                "Patriot AMG"\n'
        lua_string_ground_groups += "            },\n"
        lua_string_ground_groups += "            maxDist = 300,\n"
        lua_string_ground_groups += f'            skill = "{skill_str}",\n'
        lua_string_ground_groups += "            dataCategory = TemplateDB.type.group\n"
        lua_string_ground_groups += "}\n"

        lua_string_ground_groups += 'TemplateDB.templates["sa3-' + side_str + '"] = {\n'
        lua_string_ground_groups += "    units = {\n"
        lua_string_ground_groups += '                "p-19 s-125 sr",\n'
        lua_string_ground_groups += '                "snr s-125 tr",\n'
        lua_string_ground_groups += '                "5p73 s-125 ln",\n'
        lua_string_ground_groups += '                "5p73 s-125 ln",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += '                "5p73 s-125 ln",\n'
        lua_string_ground_groups += '                "5p73 s-125 ln"\n'
        lua_string_ground_groups += "            },\n"
        lua_string_ground_groups += "            maxDist = 300,\n"
        lua_string_ground_groups += f'            skill = "{skill_str}",\n'
        lua_string_ground_groups += "            dataCategory = TemplateDB.type.group\n"
        lua_string_ground_groups += "}\n"

        lua_string_ground_groups += 'TemplateDB.templates["sa6-' + side_str + '"] = {\n'
        lua_string_ground_groups += "    units = {\n"
        lua_string_ground_groups += '                "Kub 1S91 str",\n'
        lua_string_ground_groups += '                "Kub 2P25 ln",\n'
        lua_string_ground_groups += '                "Kub 2P25 ln",\n'
        lua_string_ground_groups += '                "Kub 2P25 ln",\n'
        lua_string_ground_groups += '                "Kub 2P25 ln",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.SHORAD, UnitClass.AAA, UnitClass.MANPAD])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.SHORAD, UnitClass.AAA, UnitClass.MANPAD])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += '                "Kub 2P25 ln"\n'
        lua_string_ground_groups += "            },\n"
        lua_string_ground_groups += "            maxDist = 300,\n"
        lua_string_ground_groups += f'            skill = "{skill_str}",\n'
        lua_string_ground_groups += "            dataCategory = TemplateDB.type.group\n"
        lua_string_ground_groups += "}"

        lua_string_ground_groups += (
            'TemplateDB.templates["sa10-' + side_str + '"] = {\n'
        )
        lua_string_ground_groups += "    units = {\n"
        lua_string_ground_groups += '                "S-300PS 54K6 cp",\n'
        lua_string_ground_groups += '                "S-300PS 5P85C ln",\n'
        lua_string_ground_groups += '                "S-300PS 5P85C ln",\n'
        lua_string_ground_groups += '                "S-300PS 5P85C ln",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += '                "S-300PS 5P85C ln",\n'
        lua_string_ground_groups += '                "S-300PS 5P85C ln",\n'
        lua_string_ground_groups += '                "S-300PS 5P85C ln",\n'
        lua_string_ground_groups += '                "S-300PS 40B6MD sr",\n'
        lua_string_ground_groups += '                "S-300PS 40B6M tr",\n'
        lua_string_ground_groups += '                "S-300PS 64H6E sr"\n'
        lua_string_ground_groups += "            },\n"
        lua_string_ground_groups += "            maxDist = 300,\n"
        lua_string_ground_groups += f'            skill = "{skill_str}",\n'
        lua_string_ground_groups += "            dataCategory = TemplateDB.type.group\n"
        lua_string_ground_groups += "}\n"

        lua_string_ground_groups += 'TemplateDB.templates["sa5-' + side_str + '"] = {\n'
        lua_string_ground_groups += "    units = {\n"
        lua_string_ground_groups += '                "RLS_19J6",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += '                "RPC_5N62V",\n'
        lua_string_ground_groups += '                "S-200_Launcher",\n'
        lua_string_ground_groups += '                "S-200_Launcher",\n'
        lua_string_ground_groups += '                "S-200_Launcher",\n'
        lua_string_ground_groups += '                "S-200_Launcher",\n'
        lua_string_ground_groups += '                "S-200_Launcher",\n'
        lua_string_ground_groups += '                "S-200_Launcher"\n'
        lua_string_ground_groups += "            },\n"
        lua_string_ground_groups += "            maxDist = 300,\n"
        lua_string_ground_groups += f'            skill = "{skill_str}",\n'
        lua_string_ground_groups += "            dataCategory = TemplateDB.type.group\n"
        lua_string_ground_groups += "}\n"

        lua_string_ground_groups += (
            'TemplateDB.templates["sa11-' + side_str + '"] = {\n'
        )
        lua_string_ground_groups += "    units = {\n"
        lua_string_ground_groups += '                "SA-11 Buk SR 9S18M1",\n'
        lua_string_ground_groups += '                "SA-11 Buk LN 9A310M1",\n'
        lua_string_ground_groups += '                "SA-11 Buk LN 9A310M1",\n'
        lua_string_ground_groups += '                "SA-11 Buk LN 9A310M1",\n'
        lua_string_ground_groups += '                "SA-11 Buk LN 9A310M1",\n'
        lua_string_ground_groups += '                "SA-11 Buk LN 9A310M1",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.SHORAD, UnitClass.AAA, UnitClass.MANPAD])}",\n'
        lua_string_ground_groups += '                "SA-11 Buk SR 9S18M1",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += '                "SA-11 Buk CC 9S470M1"\n'
        lua_string_ground_groups += "            },\n"
        lua_string_ground_groups += "            maxDist = 300,\n"
        lua_string_ground_groups += f'            skill = "{skill_str}",\n'
        lua_string_ground_groups += "            dataCategory = TemplateDB.type.group\n"
        lua_string_ground_groups += "}\n"

        lua_string_ground_groups += (
            'TemplateDB.templates["nasamsb-' + side_str + '"] = {\n'
        )
        lua_string_ground_groups += "    units = {\n"
        lua_string_ground_groups += '                "NASAMS_Command_Post",\n'
        lua_string_ground_groups += '                "NASAMS_Radar_MPQ64F1",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.AAA, UnitClass.SHORAD, UnitClass.MANPAD])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.SHORAD, UnitClass.AAA, UnitClass.MANPAD])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.SHORAD, UnitClass.AAA, UnitClass.MANPAD])}",\n'
        lua_string_ground_groups += '                "NASAMS_LN_B",\n'
        lua_string_ground_groups += '                "NASAMS_LN_B",\n'
        lua_string_ground_groups += '                "NASAMS_LN_B",\n'
        lua_string_ground_groups += '                "NASAMS_LN_B",\n'
        lua_string_ground_groups += '                "NASAMS_Radar_MPQ64F1",\n'
        lua_string_ground_groups += '                "NASAMS_Radar_MPQ64F1",\n'
        lua_string_ground_groups += '                "NASAMS_Radar_MPQ64F1"\n'
        lua_string_ground_groups += "            },\n"
        lua_string_ground_groups += "            maxDist = 300,\n"
        lua_string_ground_groups += f'            skill = "{skill_str}",\n'
        lua_string_ground_groups += "            dataCategory = TemplateDB.type.group\n"
        lua_string_ground_groups += "}\n"

        lua_string_ground_groups += (
            'TemplateDB.templates["nasamsc-' + side_str + '"] = {\n'
        )
        lua_string_ground_groups += "    units = {\n"
        lua_string_ground_groups += '                "NASAMS_Command_Post",\n'
        lua_string_ground_groups += '                "NASAMS_Radar_MPQ64F1",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.AAA, UnitClass.SHORAD, UnitClass.MANPAD])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.SHORAD, UnitClass.AAA, UnitClass.MANPAD])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.SHORAD, UnitClass.AAA, UnitClass.MANPAD])}",\n'
        lua_string_ground_groups += '                "NASAMS_LN_C",\n'
        lua_string_ground_groups += '                "NASAMS_LN_C",\n'
        lua_string_ground_groups += '                "NASAMS_LN_C",\n'
        lua_string_ground_groups += '                "NASAMS_LN_C",\n'
        lua_string_ground_groups += '                "NASAMS_Radar_MPQ64F1",\n'
        lua_string_ground_groups += '                "NASAMS_Radar_MPQ64F1",\n'
        lua_string_ground_groups += '                "NASAMS_Radar_MPQ64F1"\n'
        lua_string_ground_groups += "            },\n"
        lua_string_ground_groups += "            maxDist = 300,\n"
        lua_string_ground_groups += f'            skill = "{skill_str}",\n'
        lua_string_ground_groups += "            dataCategory = TemplateDB.type.group\n"
        lua_string_ground_groups += "}\n"

        lua_string_ground_groups += (
            'TemplateDB.templates["rapier-' + side_str + '"] = {\n'
        )
        lua_string_ground_groups += "    units = {\n"
        lua_string_ground_groups += '                "rapier_fsa_blindfire_radar",\n'
        lua_string_ground_groups += '                "rapier_fsa_blindfire_radar",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.AAA, UnitClass.SHORAD, UnitClass.MANPAD])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.SHORAD, UnitClass.AAA, UnitClass.MANPAD])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.SHORAD, UnitClass.AAA, UnitClass.MANPAD])}",\n'
        lua_string_ground_groups += '                "rapier_fsa_launcher",\n'
        lua_string_ground_groups += '                "rapier_fsa_launcher",\n'
        lua_string_ground_groups += '                "rapier_fsa_launcher",\n'
        lua_string_ground_groups += '                "rapier_fsa_launcher",\n'
        lua_string_ground_groups += (
            '                "rapier_fsa_optical_tracker_unit",\n'
        )
        lua_string_ground_groups += (
            '                "rapier_fsa_optical_tracker_unit",\n'
        )
        lua_string_ground_groups += (
            '                "rapier_fsa_optical_tracker_unit"\n'
        )
        lua_string_ground_groups += "            },\n"
        lua_string_ground_groups += "            maxDist = 300,\n"
        lua_string_ground_groups += f'            skill = "{skill_str}",\n'
        lua_string_ground_groups += "            dataCategory = TemplateDB.type.group\n"
        lua_string_ground_groups += "}\n"

        lua_string_ground_groups += (
            'TemplateDB.templates["roland-' + side_str + '"] = {\n'
        )
        lua_string_ground_groups += "    units = {\n"
        lua_string_ground_groups += '                "Roland ADS",\n'
        lua_string_ground_groups += '                "Roland ADS",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.AAA, UnitClass.SHORAD, UnitClass.MANPAD])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.SHORAD, UnitClass.AAA, UnitClass.MANPAD])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.SHORAD, UnitClass.AAA, UnitClass.MANPAD])}",\n'
        lua_string_ground_groups += '                "Roland ADS",\n'
        lua_string_ground_groups += '                "Roland ADS",\n'
        lua_string_ground_groups += '                "Roland ADS",\n'
        lua_string_ground_groups += '                "Roland ADS",\n'
        lua_string_ground_groups += '                "Roland Radar",\n'
        lua_string_ground_groups += '                "Roland Radar",\n'
        lua_string_ground_groups += '                "Roland Radar"\n'
        lua_string_ground_groups += "            },\n"
        lua_string_ground_groups += "            maxDist = 300,\n"
        lua_string_ground_groups += f'            skill = "{skill_str}",\n'
        lua_string_ground_groups += "            dataCategory = TemplateDB.type.group\n"
        lua_string_ground_groups += "}\n"

        lua_string_ground_groups += 'TemplateDB.templates["hq7-' + side_str + '"] = {\n'
        lua_string_ground_groups += "    units = {\n"
        lua_string_ground_groups += '                "HQ-7_LN_EO",\n'
        lua_string_ground_groups += '                "HQ-7_LN_EO",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.AAA, UnitClass.SHORAD, UnitClass.MANPAD])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.LOGISTICS])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.SHORAD, UnitClass.AAA, UnitClass.MANPAD])}",\n'
        lua_string_ground_groups += f'                "{self.get_ground_unit(coalition, side, [UnitClass.SHORAD, UnitClass.AAA, UnitClass.MANPAD])}",\n'
        lua_string_ground_groups += '                "HQ-7_LN_SP",\n'
        lua_string_ground_groups += '                "HQ-7_LN_SP",\n'
        lua_string_ground_groups += '                "HQ-7_LN_SP",\n'
        lua_string_ground_groups += '                "HQ-7_LN_SP",\n'
        lua_string_ground_groups += '                "HQ-7_STR_SP",\n'
        lua_string_ground_groups += '                "HQ-7_STR_SP",\n'
        lua_string_ground_groups += '                "HQ-7_STR_SP"\n'
        lua_string_ground_groups += "            },\n"
        lua_string_ground_groups += "            maxDist = 300,\n"
        lua_string_ground_groups += f'            skill = "{skill_str}",\n'
        lua_string_ground_groups += "            dataCategory = TemplateDB.type.group\n"
        lua_string_ground_groups += "}\n"

        return lua_string_ground_groups

    @staticmethod
    def generate_pretense_zone_connection(
        connected_points: dict[str, list[str]],
        cp_name: str,
        other_cp_name: str,
    ) -> str:
        lua_string_connman = ""
        try:
            connected_points[cp_name]
        except KeyError:
            connected_points[cp_name] = list()
        try:
            connected_points[other_cp_name]
        except KeyError:
            connected_points[other_cp_name] = list()

        if (
            other_cp_name not in connected_points[cp_name]
            and cp_name not in connected_points[other_cp_name]
        ):
            cp_name_conn = "".join(
                [i for i in cp_name if i.isalnum() or i.isspace() or i == "-"]
            )
            cp_name_conn_other = "".join(
                [i for i in other_cp_name if i.isalnum() or i.isspace() or i == "-"]
            )
            lua_string_connman = (
                f"    cm: addConnection('{cp_name_conn}', '{cp_name_conn_other}')\n"
            )
            connected_points[cp_name].append(other_cp_name)
            connected_points[other_cp_name].append(cp_name)

        return lua_string_connman

    def generate_pretense_plugin_data(self) -> None:
        self.inject_plugin_script("base", "mist_4_5_122.lua", "mist_4_5_122")

        lua_string_config = "Config = Config or {}\n"

        lua_string_config += (
            f"Config.maxDistFromFront = "
            + str(self.game.settings.pretense_maxdistfromfront_distance * 1000)
            + "\n"
        )
        trigger = TriggerStart(comment="Pretense config")
        trigger.add_action(DoScript(String(lua_string_config)))
        self.mission.triggerrules.triggers.append(trigger)

        self.inject_plugin_script(
            "pretense", "pretense_compiled.lua", "pretense_compiled"
        )

        trigger = TriggerStart(comment="Pretense init")

        now = datetime.now()
        date_time = now.strftime("%Y-%m-%dT%H_%M_%S")
        lua_string_savefile = (
            f"local savefile = 'pretense_retribution_{date_time}.json'"
        )

        init_header_file = open("./resources/plugins/pretense/init_header.lua", "r")
        init_header = init_header_file.read()

        lua_string_ground_groups_blue = self.generate_pretense_ground_groups(
            PRETENSE_BLUE_SIDE
        )
        lua_string_ground_groups_red = self.generate_pretense_ground_groups(
            PRETENSE_RED_SIDE
        )

        lua_string_zones = ""
        lua_string_carriers = ""
        if self.game.settings.pretense_controllable_carrier:
            lua_string_carriers += self.generate_pretense_carrier_zones()

        for cp in self.game.theater.controlpoints:
            cp_name_trimmed = "".join([i for i in cp.name.lower() if i.isalpha()])
            cp_name = "".join(
                [i for i in cp.name if i.isalnum() or i.isspace() or i == "-"]
            )
            cp_side = 2 if cp.captured else 1

            if isinstance(cp, OffMapSpawn):
                continue
            elif (
                cp.is_fleet
                and cp.captured
                and self.game.settings.pretense_controllable_carrier
            ):
                # Friendly carrier, generate carrier parameters
                cp_carrier_group_type = cp.get_carrier_group_type()
                cp_carrier_group_name = cp.get_carrier_group_name()
                lua_string_carriers += self.generate_pretense_carriers(
                    cp_name, cp_side, cp_carrier_group_type, cp_carrier_group_name
                )
                continue

            for side in range(1, 3):
                if cp_name_trimmed not in self.game.pretense_air[cp_side]:
                    self.game.pretense_air[side][cp_name_trimmed] = {}
                if cp_name_trimmed not in self.game.pretense_ground_supply[cp_side]:
                    self.game.pretense_ground_supply[side][cp_name_trimmed] = list()
                if cp_name_trimmed not in self.game.pretense_ground_assault[cp_side]:
                    self.game.pretense_ground_assault[side][cp_name_trimmed] = list()
            lua_string_zones += (
                f"zones.{cp_name_trimmed} = ZoneCommand:new('{cp_name}')\n"
            )
            lua_string_zones += (
                f"zones.{cp_name_trimmed}.initialState = "
                + "{ side="
                + str(cp_side)
                + " }\n"
            )
            max_resource = 20000
            is_helo_spawn = "false"
            is_plane_spawn = "false"
            is_keep_active = "false"
            if cp.has_helipads:
                is_helo_spawn = "true"
                max_resource = 30000
            if isinstance(cp, Airfield) or cp.has_ground_spawns:
                is_helo_spawn = "true"
                is_plane_spawn = "true"
            if cp.has_ground_spawns or cp.is_lha:
                is_helo_spawn = "true"
                is_plane_spawn = "true"
                max_resource = 40000
            if cp.is_lha:
                is_keep_active = "true"
            if isinstance(cp, Airfield) or cp.is_carrier:
                is_helo_spawn = "true"
                is_plane_spawn = "true"
                is_keep_active = "true"
                max_resource = 50000
            lua_string_zones += (
                f"zones.{cp_name_trimmed}.maxResource = {max_resource}\n"
            )
            lua_string_zones += (
                f"zones.{cp_name_trimmed}.isHeloSpawn = " + is_helo_spawn + "\n"
            )
            lua_string_zones += (
                f"zones.{cp_name_trimmed}.isPlaneSpawn = " + is_plane_spawn + "\n"
            )
            lua_string_zones += (
                f"zones.{cp_name_trimmed}.keepActive = " + is_keep_active + "\n"
            )
            if cp.is_fleet:
                lua_string_zones += self.generate_pretense_zone_sea(cp_name)
            else:
                lua_string_zones += self.generate_pretense_zone_land(cp_name)

        lua_string_connman = "	cm = ConnectionManager:new()\n"

        # Generate ConnectionManager connections
        connected_points: dict[str, list[str]] = {}
        for cp in self.game.theater.controlpoints:
            for other_cp in cp.connected_points:
                lua_string_connman += self.generate_pretense_zone_connection(
                    connected_points, cp.name, other_cp.name
                )
            for sea_connection in cp.shipping_lanes:
                lua_string_connman += self.generate_pretense_zone_connection(
                    connected_points,
                    cp.name,
                    sea_connection.name,
                )
            if len(cp.connected_points) == 0 and len(cp.shipping_lanes) == 0:
                # Also connect carrier and LHA control points to adjacent friendly points
                if cp.is_fleet and (
                    not self.game.settings.pretense_controllable_carrier
                    or not cp.captured
                ):
                    num_of_carrier_connections = 0
                    for (
                        other_cp
                    ) in self.game.theater.closest_friendly_control_points_to(cp):
                        num_of_carrier_connections += 1
                        if (
                            num_of_carrier_connections
                            > PRETENSE_NUMBER_OF_ZONES_TO_CONNECT_CARRIERS_TO
                        ):
                            break

                        lua_string_connman += self.generate_pretense_zone_connection(
                            connected_points, cp.name, other_cp.name
                        )
            else:
                # Finally, connect remaining non-connected points
                closest_cps = self.game.theater.closest_friendly_control_points_to(cp)
                for extra_connection in range(
                    self.game.settings.pretense_extra_zone_connections
                ):
                    if (
                        cp.is_fleet
                        and cp.captured
                        and self.game.settings.pretense_controllable_carrier
                    ):
                        break
                    elif (
                        closest_cps[extra_connection].is_fleet
                        and closest_cps[extra_connection].captured
                        and self.game.settings.pretense_controllable_carrier
                    ):
                        break
                    elif len(closest_cps) > extra_connection:
                        lua_string_connman += self.generate_pretense_zone_connection(
                            connected_points,
                            cp.name,
                            closest_cps[extra_connection].name,
                        )
                    else:
                        break

        lua_string_supply = "local redSupply = {\n"
        # Generate supply
        for cp_side in range(1, 3):
            for cp in self.game.theater.controlpoints:
                if isinstance(cp, OffMapSpawn):
                    continue
                cp_side_captured = cp_side == 2
                if cp_side_captured != cp.captured:
                    continue
                cp_name_trimmed = "".join([i for i in cp.name.lower() if i.isalpha()])
                for mission_type in self.game.pretense_air[cp_side][cp_name_trimmed]:
                    if mission_type == FlightType.PRETENSE_CARGO:
                        for air_group in self.game.pretense_air[cp_side][
                            cp_name_trimmed
                        ][mission_type]:
                            lua_string_supply += f"'{air_group}',"
            lua_string_supply += "}\n"
            if cp_side < 2:
                lua_string_supply += "local blueSupply = {\n"
        lua_string_supply += "local offmapZones = {\n"
        for cp in self.game.theater.controlpoints:
            if isinstance(cp, Airfield):
                cp_name_trimmed = "".join([i for i in cp.name.lower() if i.isalpha()])
                lua_string_supply += f"   zones.{cp_name_trimmed},\n"
        lua_string_supply += "}\n"

        init_body_1_file = open("./resources/plugins/pretense/init_body_1.lua", "r")
        init_body_1 = init_body_1_file.read()

        lua_string_jtac = ""
        for jtac in self.mission_data.jtacs:
            lua_string_jtac = f"Group.getByName('{jtac.group_name}'): destroy()\n"
            lua_string_jtac += (
                "CommandFunctions.jtac = JTAC:new({name = '" + jtac.group_name + "'})\n"
            )

        init_body_2_file = open("./resources/plugins/pretense/init_body_2.lua", "r")
        init_body_2 = init_body_2_file.read()

        init_body_3_file = open("./resources/plugins/pretense/init_body_3.lua", "r")
        init_body_3 = init_body_3_file.read()

        init_footer_file = open("./resources/plugins/pretense/init_footer.lua", "r")
        init_footer = init_footer_file.read()

        lua_string = (
            lua_string_savefile
            + init_header
            + lua_string_ground_groups_blue
            + lua_string_ground_groups_red
            + init_body_1
            + lua_string_zones
            + lua_string_connman
            + init_body_2
            + lua_string_jtac
            + lua_string_carriers
            + init_body_3
            + lua_string_supply
            + init_footer
        )

        trigger.add_action(DoScript(String(lua_string)))
        self.mission.triggerrules.triggers.append(trigger)

        file1 = open(Path("./resources/plugins/pretense", "pretense_output.lua"), "w")
        file1.write(lua_string)
        file1.close()

    def inject_lua_trigger(self, contents: str, comment: str) -> None:
        trigger = TriggerStart(comment=comment)
        trigger.add_action(DoScript(String(contents)))
        self.mission.triggerrules.triggers.append(trigger)

    def bypass_plugin_script(self, mnemonic: str) -> None:
        self.plugin_scripts.append(mnemonic)

    def inject_plugin_script(
        self, plugin_mnemonic: str, script: str, script_mnemonic: str
    ) -> None:
        if script_mnemonic in self.plugin_scripts:
            logging.debug(f"Skipping already loaded {script} for {plugin_mnemonic}")
            return

        self.plugin_scripts.append(script_mnemonic)

        plugin_path = Path("./resources/plugins", plugin_mnemonic)

        script_path = Path(plugin_path, script)
        if not script_path.exists():
            logging.error(f"Cannot find {script_path} for plugin {plugin_mnemonic}")
            return

        trigger = TriggerStart(comment=f"Load {script_mnemonic}")
        filename = script_path.resolve()
        fileref = self.mission.map_resource.add_resource_file(filename)
        trigger.add_action(DoScriptFile(fileref))
        self.mission.triggerrules.triggers.append(trigger)

    def inject_plugins(self) -> None:
        for plugin in LuaPluginManager.plugins():
            if plugin.enabled:
                plugin.inject_scripts(self)
                plugin.inject_configuration(self)


class LuaValue:
    key: Optional[str]
    value: str | list[str]

    def __init__(self, key: Optional[str], value: str | list[str]):
        self.key = key
        self.value = value

    def serialize(self) -> str:
        serialized_value = self.key + " = " if self.key else ""
        if isinstance(self.value, str):
            serialized_value += f'"{escape_string_for_lua(self.value)}"'
        else:
            escaped_values = [f'"{escape_string_for_lua(v)}"' for v in self.value]
            serialized_value += "{" + ", ".join(escaped_values) + "}"
        return serialized_value


class LuaItem(ABC):
    value: LuaValue | list[LuaValue]
    name: Optional[str]

    def __init__(self, name: Optional[str]):
        self.value = []
        self.name = name

    def set_value(self, value: str) -> None:
        self.value = LuaValue(None, value)

    def set_data_array(self, values: list[str]) -> None:
        self.value = LuaValue(None, values)

    def add_data_array(self, key: str, values: list[str]) -> None:
        self._add_value(LuaValue(key, values))

    def add_key_value(self, key: str, value: str) -> None:
        self._add_value(LuaValue(key, value))

    def _add_value(self, value: LuaValue) -> None:
        if isinstance(self.value, list):
            self.value.append(value)
        else:
            self.value = value

    @abstractmethod
    def add_item(self, item_name: Optional[str] = None) -> LuaItem:
        """adds a new item to the LuaArray without checking the existence"""
        raise NotImplementedError

    @abstractmethod
    def get_item(self, item_name: str) -> Optional[LuaItem]:
        """gets item from LuaArray. Returns None if it does not exist"""
        raise NotImplementedError

    @abstractmethod
    def get_or_create_item(self, item_name: Optional[str] = None) -> LuaItem:
        """gets item from the LuaArray or creates one if it does not exist already"""
        raise NotImplementedError

    @abstractmethod
    def serialize(self) -> str:
        if isinstance(self.value, LuaValue):
            return self.value.serialize()
        else:
            serialized_data = [d.serialize() for d in self.value]
            return "{" + ", ".join(serialized_data) + "}"


class LuaData(LuaItem):
    objects: list[LuaData]
    base_name: Optional[str]

    def __init__(self, name: Optional[str], is_base_name: bool = True):
        self.objects = []
        self.base_name = name if is_base_name else None
        super().__init__(name)

    def add_item(self, item_name: Optional[str] = None) -> LuaItem:
        item = LuaData(item_name, False)
        self.objects.append(item)
        return item

    def get_item(self, item_name: str) -> Optional[LuaItem]:
        for lua_object in self.objects:
            if lua_object.name == item_name:
                return lua_object
        return None

    def get_or_create_item(self, item_name: Optional[str] = None) -> LuaItem:
        if item_name:
            item = self.get_item(item_name)
            if item:
                return item
        return self.add_item(item_name)

    def serialize(self, level: int = 0) -> str:
        """serialize the LuaData to a string"""
        serialized_data: list[str] = []
        serialized_name = ""
        linebreak = "\n"
        tab = "\t"
        tab_end = ""
        for _ in range(level):
            tab += "\t"
            tab_end += "\t"
        if self.base_name:
            # Only used for initialization of the object in lua
            serialized_name += self.base_name + " = "
        if self.objects:
            # nested objects
            serialized_objects = [o.serialize(level + 1) for o in self.objects]
            if self.name:
                if self.name is not self.base_name:
                    serialized_name += self.name + " = "
            serialized_data.append(
                serialized_name
                + "{"
                + linebreak
                + tab
                + ("," + linebreak + tab).join(serialized_objects)
                + linebreak
                + tab_end
                + "}"
            )
        else:
            # key with value
            if self.name:
                serialized_data.append(self.name + " = " + super().serialize())
            # only value
            else:
                serialized_data.append(super().serialize())

        return "\n".join(serialized_data)

    def create_operations_lua(self) -> str:
        """crates the liberation lua script for the dcs mission"""
        lua_prefix = """
-- setting configuration table
env.info("DCSRetribution|: setting configuration table")
"""

        return lua_prefix + self.serialize()
