from __future__ import annotations

from pathlib import Path
from typing import List, TYPE_CHECKING

from game.plugins.luaplugin import LuaPlugin, LuaPluginDefinition

if TYPE_CHECKING:
    from game.missiongenerator.luagenerator import LuaGenerator

# Module-level so tests can monkeypatch the resource root.
PLUGIN_RESOURCE_ROOT = Path("resources/plugins")


class MooseAtisPlugin(LuaPlugin):
    """ATIS plugin with terrain-scoped airport-name soundfile injection.

    The common/NATO fragments are static (manifest ``otherResourceFiles``).
    Per-terrain airport-name files live under ``SoundFiles/<TerrainName>/`` and
    are injected only for the mission's current terrain -- so a ``.miz`` never
    carries every map's name audio. Missing name files degrade to no spoken
    field name (design §4); this method simply injects whatever is present.
    """

    def __init__(self, definition: LuaPluginDefinition) -> None:
        super().__init__(definition)
        # Expose as a direct instance attribute so inject_other_resource_files
        # can use self.other_resource_files uniformly (the test harness also sets
        # this attribute directly on __new__-constructed instances).
        self.other_resource_files: List[str] = list(definition.other_resource_files)

    def inject_other_resource_files(self, lua_generator: "LuaGenerator") -> None:
        # Inject the static common/NATO files declared in the plugin manifest.
        # We use self.identifier / self.other_resource_files directly so both
        # the production path (via __init__) and the test path (via __new__ with
        # direct attribute assignment) work identically.
        for resource_file in self.other_resource_files:
            lua_generator.inject_other_plugin_resources(self.identifier, resource_file)
        terrain_name = lua_generator.game.theater.terrain.name
        names_dir = PLUGIN_RESOURCE_ROOT / self.identifier / "SoundFiles" / terrain_name
        if not names_dir.is_dir():
            return
        for ogg in sorted(names_dir.glob("*.ogg")):
            lua_generator.inject_other_plugin_resources(
                self.identifier, f"SoundFiles/{terrain_name}/{ogg.name}"
            )
