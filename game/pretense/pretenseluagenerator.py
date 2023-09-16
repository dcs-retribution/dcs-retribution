from __future__ import annotations

import logging
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING, Optional

from dcs import Mission
from dcs.action import DoScript, DoScriptFile
from dcs.translation import String
from dcs.triggers import TriggerStart

from game.ato import FlightType
from game.dcs.aircrafttype import AircraftType
from game.missiongenerator.luagenerator import LuaGenerator
from game.plugins import LuaPluginManager
from game.theater import TheaterGroundObject, Airfield, OffMapSpawn
from game.theater.iadsnetwork.iadsrole import IadsRole
from game.utils import escape_string_for_lua
from game.missiongenerator.missiondata import MissionData

if TYPE_CHECKING:
    from game import Game


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
        self.generate_plugin_data()
        self.inject_plugins()
        for t in ewrj_triggers:
            self.mission.triggerrules.triggers.remove(t)
            self.mission.triggerrules.triggers.append(t)

    def generate_plugin_data(self) -> None:
        self.mission.triggerrules.triggers.clear()

        self.inject_plugin_script("base", "mist_4_5_107.lua", "mist_4_5_107")
        self.inject_plugin_script(
            "pretense", "pretense_compiled.lua", "pretense_compiled"
        )

        trigger = TriggerStart(comment="Pretense init")

        init_header_file = open("./resources/plugins/pretense/init_header.lua", "r")
        init_header = init_header_file.read()

        lua_string_zones = ""

        for cp in self.game.theater.controlpoints:
            if isinstance(cp, OffMapSpawn):
                continue

            cp_name_trimmed = "".join([i for i in cp.name.lower() if i.isalnum()])
            cp_side = 2 if cp.captured else 1
            for side in range(1, 3):
                if cp_name_trimmed not in self.game.pretense_air[cp_side]:
                    self.game.pretense_air[side][cp_name_trimmed] = {}
                if cp_name_trimmed not in self.game.pretense_ground_supply[cp_side]:
                    self.game.pretense_ground_supply[side][cp_name_trimmed] = list()
                if cp_name_trimmed not in self.game.pretense_ground_assault[cp_side]:
                    self.game.pretense_ground_assault[side][cp_name_trimmed] = list()
            lua_string_zones += (
                f"zones.{cp_name_trimmed} = ZoneCommand:new('{cp.name}')\n"
            )
            lua_string_zones += (
                f"zones.{cp_name_trimmed}.initialState = "
                + "{ side="
                + str(cp_side)
                + " }\n"
            )
            lua_string_zones += f"zones.{cp_name_trimmed}.keepActive = true\n"
            max_resource = 20000
            if cp.has_helipads:
                lua_string_zones += f"zones.{cp_name_trimmed}.isHeloSpawn = true\n"
                max_resource = 30000
            if isinstance(cp, Airfield) or cp.has_ground_spawns:
                lua_string_zones += f"zones.{cp_name_trimmed}.isPlaneSpawn = true\n"
            if cp.has_ground_spawns or cp.is_lha:
                max_resource = 40000
            if isinstance(cp, Airfield) or cp.is_carrier:
                max_resource = 50000
            lua_string_zones += (
                f"zones.{cp_name_trimmed}.maxResource = {max_resource}\n"
            )
            lua_string_zones += f"zones.{cp_name_trimmed}:defineUpgrades(" + "{\n"
            lua_string_zones += "    [1] = { --red side\n"
            lua_string_zones += "        presets.upgrades.basic.tent:extend({\n"
            lua_string_zones += f"            name='{cp_name_trimmed}-tent-red',\n"
            lua_string_zones += "            products = {\n"
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
            lua_string_zones += (
                "                presets.defenses.red.infantry:extend({ name='"
                + cp_name_trimmed
                + "-garrison-red' })\n"
            )
            lua_string_zones += "            }\n"
            lua_string_zones += "        }),\n"
            lua_string_zones += "    },\n"
            lua_string_zones += "    [2] = --blue side\n"
            lua_string_zones += "    {\n"
            lua_string_zones += "        presets.upgrades.basic.tent:extend({\n"
            lua_string_zones += f"            name='{cp_name_trimmed}-tent-blue',\n"
            lua_string_zones += "            products = {\n"
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
            lua_string_zones += (
                "                presets.defenses.blue.infantry:extend({ name='"
                + cp_name_trimmed
                + "-garrison-blue' })\n"
            )
            lua_string_zones += "            }\n"
            lua_string_zones += "        }),\n"
            lua_string_zones += "        presets.upgrades.supply.fuelTank:extend({\n"
            lua_string_zones += (
                "            name = '" + cp_name_trimmed + "-fueltank-blue',\n"
            )
            lua_string_zones += "            products = {\n"
            for ground_group in self.game.pretense_ground_supply[cp_side][
                cp_name_trimmed
            ]:
                lua_string_zones += (
                    "                presets.missions.supply.convoy:extend({ name='"
                    + ground_group
                    + "'}),\n"
                )
            for ground_group in self.game.pretense_ground_assault[cp_side][
                cp_name_trimmed
            ]:
                lua_string_zones += (
                    "                presets.missions.attack.surface:extend({ name='"
                    + ground_group
                    + "'}),\n"
                )
            for mission_type in self.game.pretense_air[cp_side][cp_name_trimmed]:
                if mission_type == FlightType.AIR_ASSAULT.name:
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
            lua_string_zones += "        presets.upgrades.airdef.comCenter:extend({\n"
            lua_string_zones += (
                f"            name = '{cp_name_trimmed}-mission-command-blue',\n"
            )
            lua_string_zones += "            products = {\n"
            lua_string_zones += (
                "                presets.defenses.blue.shorad:extend({ name='"
                + cp_name_trimmed
                + "-sam-blue' }),\n"
            )
            for mission_type in self.game.pretense_air[cp_side][cp_name_trimmed]:
                if mission_type == FlightType.SEAD.name:
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
                elif mission_type == FlightType.CAS.name:
                    mission_name = "attack.cas"
                    for air_group in self.game.pretense_air[cp_side][cp_name_trimmed][
                        mission_type
                    ]:
                        lua_string_zones += (
                            f"                presets.missions.{mission_name}:extend"
                            + "({name='"
                            + air_group
                            + "', altitude=15000, expend=AI.Task.WeaponExpend.ONE}),\n"
                        )
                elif mission_type == FlightType.BAI.name:
                    mission_name = "attack.bai"
                    for air_group in self.game.pretense_air[cp_side][cp_name_trimmed][
                        mission_type
                    ]:
                        lua_string_zones += (
                            f"                presets.missions.{mission_name}:extend"
                            + "({name='"
                            + air_group
                            + "', altitude=10000, expend=AI.Task.WeaponExpend.ONE}),\n"
                        )
                elif mission_type == FlightType.STRIKE.name:
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
                elif mission_type == FlightType.BARCAP.name:
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
                elif mission_type == FlightType.REFUELING.name:
                    mission_name = "support.tanker"
                    for air_group in self.game.pretense_air[cp_side][cp_name_trimmed][
                        mission_type
                    ]:
                        tanker_freq = 257.0
                        tanker_tacan = 37.0
                        for tanker in self.mission_data.tankers:
                            if tanker.group_name == air_group:
                                tanker_freq = tanker.freq.hertz / 1000000
                                tanker_tacan = tanker.tacan.number
                                if tanker.variant == "KC-135 Stratotanker":
                                    tanker_variant = "Boom"
                                else:
                                    tanker_variant = "Drogue"
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
                elif mission_type == FlightType.AEWC.name:
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
            lua_string_zones += "    }\n"
            lua_string_zones += "})\n"

        lua_string_connman = "	cm = ConnectionManager:new()\n"

        # Generate ConnectionManager connections
        for cp in self.game.theater.controlpoints:
            for other_cp in cp.connected_points:
                lua_string_connman += (
                    f"    cm: addConnection('{cp.name}', '{other_cp.name}')\n"
                )
            for sea_connection in cp.shipping_lanes:
                if sea_connection.is_friendly_to(cp):
                    lua_string_connman += (
                        f"    cm: addConnection('{cp.name}', '{sea_connection.name}')\n"
                    )
            if len(cp.connected_points) == 0 and len(cp.shipping_lanes) == 0:
                # Also connect carrier and LHA control points to adjacent friendly points
                if cp.is_fleet:
                    for (
                        other_cp
                    ) in self.game.theater.closest_friendly_control_points_to(cp):
                        lua_string_connman += (
                            f"    cm: addConnection('{cp.name}', '{other_cp.name}')\n"
                        )
            else:
                # Finally, connect remaining non-connected points
                (
                    closest_cp,
                    second_closest_cp,
                ) = self.game.theater.closest_friendly_control_points_to(cp)
                lua_string_connman += (
                    f"    cm: addConnection('{cp.name}', '{closest_cp.name}')\n"
                )
                lua_string_connman += (
                    f"    cm: addConnection('{cp.name}', '{second_closest_cp.name}')\n"
                )

        init_body_1_file = open("./resources/plugins/pretense/init_body_1.lua", "r")
        init_body_1 = init_body_1_file.read()

        lua_string_jtac = ""
        for jtac in self.mission_data.jtacs:
            lua_string_jtac = f"Group.getByName('{jtac.group_name}'): destroy()"
            lua_string_jtac += (
                "CommandFunctions.jtac = JTAC:new({name = '" + jtac.group_name + "'})"
            )

        init_body_2_file = open("./resources/plugins/pretense/init_body_2.lua", "r")
        init_body_2 = init_body_2_file.read()

        init_footer_file = open("./resources/plugins/pretense/init_footer.lua", "r")
        init_footer = init_footer_file.read()

        lua_string = (
            init_header
            + lua_string_zones
            + lua_string_connman
            + init_body_1
            + lua_string_jtac
            + init_body_2
            + init_footer
        )

        trigger.add_action(DoScript(String(lua_string)))
        self.mission.triggerrules.triggers.append(trigger)

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
            if plugin.enabled and plugin.identifier not in ("base"):
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
