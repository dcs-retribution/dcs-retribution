from __future__ import annotations

from typing import TYPE_CHECKING, Any

from game.dcs.groundunittype import GroundUnitType
from game.ground_forces.ai_ground_planner import (
    DISTANCE_FROM_FRONTLINE,
    CombatGroupRole,
)
from game.plugins.luaplugin import LuaPlugin

if TYPE_CHECKING:
    from game.missiongenerator.luagenerator import LuaGenerator


def build_unit_class_table() -> dict[str, str]:
    """Map every known DCS ground type id to its Retribution UnitClass value.

    Keyed by ``dcs_unit_type.id`` (what ``unit:GetTypeName()`` returns in-sim).
    When several variants share one DCS type they share a class in practice;
    last-wins is acceptable.
    """
    table: dict[str, str] = {}
    for dcs_type in GroundUnitType.each_dcs_type():
        for ground_unit_type in GroundUnitType.for_dcs_type(dcs_type):
            table[dcs_type.id] = ground_unit_type.unit_class.value
    return table


def corridor_depths_m() -> tuple[int, int]:
    """Return (default_corridor_m, artillery_corridor_m), grounded in the
    ground-force deployment depths. Default = deepest non-artillery,
    non-logistics combat role; artillery = artillery's own depth."""
    artillery_m = DISTANCE_FROM_FRONTLINE[CombatGroupRole.ARTILLERY][1]
    default_m = max(
        upper
        for role, (_lower, upper) in DISTANCE_FROM_FRONTLINE.items()
        if role not in (CombatGroupRole.ARTILLERY, CombatGroupRole.LOGI)
    )
    return default_m, artillery_m


ORBIT_BASE_ALT_FT = 15000
ORBIT_ALT_STEP_FT = 2000
ORBIT_ALT_CEIL_FT = 28000


def _lua_str(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def _lua_jtacs(mission_data: Any) -> str:
    # Group by region only to stagger each drone's orbit altitude by its
    # per-front-line index, then emit ONE flat entry per drone — one AUTOLASE
    # instance per drone downstream. (Deconfliction is claim-based in Lua, keyed
    # by the `frontline` field, so no index is emitted.)
    by_region: dict[str, list[Any]] = {}
    for jtac in getattr(mission_data, "jtacs", []):
        by_region.setdefault(jtac.region, []).append(jtac)

    entries = []
    for region, drones in by_region.items():
        for index, jtac in enumerate(drones):
            orbit_alt = min(
                ORBIT_BASE_ALT_FT + index * ORBIT_ALT_STEP_FT, ORBIT_ALT_CEIL_FT
            )
            # fall back to UHF if a JTAC lacks a VHF freq, so mission-gen never crashes
            vhf_freq = jtac.freq_vhf if jtac.freq_vhf is not None else jtac.freq
            entries.append(
                "  { "
                f"frontline = {_lua_str(region)}, "
                f"callsign = {_lua_str(jtac.callsign)}, "
                f"groupName = {_lua_str(jtac.group_name)}, "
                f"laserCode = {int(jtac.code)}, "
                f"uhf = {jtac.freq.mhz}, "
                f"vhf = {vhf_freq.mhz}, "
                f"orbitAlt = {orbit_alt}, "
                "maxLasing = 1 "
                "},\n"
            )
    return "{\n" + "".join(entries) + "}"


def _lua_unit_class_table(table: dict[str, str]) -> str:
    rows = "".join(
        f"  [{_lua_str(k)}] = {_lua_str(v)},\n" for k, v in sorted(table.items())
    )
    return "{\n" + rows + "}"


def _lua_frontlines(mission_data: Any) -> str:
    rows = []
    seen: set[str] = set()
    for jtac in getattr(mission_data, "jtacs", []):
        seg = getattr(jtac, "frontline_segment", None)
        if seg is None:
            continue
        region = jtac.region
        if region in seen:
            continue
        seen.add(region)
        a, b = seg
        rows.append(
            f"  [{_lua_str(region)}] = "
            f"{{ a = {{ x = {a.x}, y = {a.y} }}, b = {{ x = {b.x}, y = {b.y} }} }},\n"
        )
    return "{\n" + "".join(rows) + "}"


class MooseAutolasePlugin(LuaPlugin):
    """LuaPlugin that also injects computed autolase config (unit-class table,
    per-JTAC frontline segment, corridor depths) before its config scripts run."""

    def inject_configuration(self, lua_generator: "LuaGenerator") -> None:
        self._inject_option_table(lua_generator)
        self._inject_computed_config(lua_generator)
        self._run_config_work_orders(lua_generator)

    def _inject_computed_config(self, lua_generator: "LuaGenerator") -> None:
        classes = build_unit_class_table()
        default_m, artillery_m = corridor_depths_m()
        unit_classes_lua = _lua_unit_class_table(classes)
        frontlines_lua = _lua_frontlines(lua_generator.mission_data)
        jtacs_lua = _lua_jtacs(lua_generator.mission_data)

        lua = (
            "-- MooseAutolase computed configuration (unit classes, frontlines, corridors).\n"
            "if dcsRetribution and dcsRetribution.plugins and dcsRetribution.plugins.MooseAutolase then\n"
            "    dcsRetribution.plugins.MooseAutolase.UnitClasses = "
            + unit_classes_lua
            + "\n"
            "    dcsRetribution.plugins.MooseAutolase.Frontlines = "
            + frontlines_lua
            + "\n"
            "    dcsRetribution.plugins.MooseAutolase.DefaultCorridorM = "
            + str(default_m)
            + "\n"
            "    dcsRetribution.plugins.MooseAutolase.ArtilleryCorridorM = "
            + str(artillery_m)
            + "\n"
            "    dcsRetribution.plugins.MooseAutolase.JTACs = " + jtacs_lua + "\n"
            "end\n"
        )

        # MooseAutolase drives JTAC lasing; when ctld's own JTAC autolase is off,
        # suppress ctld's stale "JTAC Status" F10 menu (it would report "no active
        # jtacs"). Runs after ctld's CTLD.lua init (ctld is injected first) and
        # before ctld's periodic addF10MenuOptions, so the menu is never added.
        # Guard dcsRetribution/.plugins before indexing .ctld: this block is a
        # sibling of the MooseAutolase config above, so it also runs when this is
        # not a full Retribution mission (dcsRetribution nil) — indexing .plugins
        # then would error.
        lua += (
            "if ctld and dcsRetribution and dcsRetribution.plugins "
            "and not (dcsRetribution.plugins.ctld "
            "and dcsRetribution.plugins.ctld.autolase) then\n"
            "    ctld.JTAC_jtacStatusF10 = false\n"
            "end\n"
        )

        lua_generator.inject_lua_trigger(lua, "MooseAutolase computed configuration")
