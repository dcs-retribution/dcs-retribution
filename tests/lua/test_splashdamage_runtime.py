"""Splash Damage 3 plugin: headless runtime smoke tests.

The first consumer of the Lua harness: loads the real
``resources/plugins/splashdamage3`` scripts (main script + the sd3-config
configuration work order) against a generated-mission-shaped
``dcsRetribution`` table and drives the weapon-tracking loop on the virtual
clock. What this pins is the class of bug the ``luac -p`` syntax gate cannot
see: the script erroring at file scope or in a scheduled tick and the whole
plugin silently never running.

Deliberately NOT pinned: explosion power numbers (tuning values under active
discussion upstream) and anything requiring DCS physics or AI.
"""

from __future__ import annotations

from typing import Any

from .harness import DcsPluginHarness

MAIN_SCRIPT = (
    "resources/plugins/splashdamage3/Splash_Damage_3.4.2_Standard_Retribution.lua"
)
CONFIG_SCRIPT = "resources/plugins/splashdamage3/sd3-config.lua"


def plugin_defaults() -> dict[str, Any]:
    """The specificOptions defaults from splashdamage3/plugin.json, as the
    mission generator would emit them into dcsRetribution.plugins."""
    return {
        "game_messages": False,
        "debug": False,
        "weapon_missing_message": False,
        "enable_radio_menu": False,
        "wave_explosions": True,
        "larger_explosions": True,
        "use_dynamic_blast_radius": True,
        "dynamic_blast_radius_modifier": 200,
        "damage_model": True,
        "static_damage_boost": 2000,
        "overall_scaling": 3,
        "unit_disabled_health": 30,
        "unit_cant_fire_health": 40,
        "infantry_cant_fire_health": 60,
        "cluster_enabled": False,
        "cluster_bomblet_reduction_modifier": True,
        "cluster_bomblet_damage_modifier": 1,
        "rocket_multiplier": 130,
        "shipRadarDamageEnable": False,
        "oca_aircraft_damage_boost": 3000,
        "ordnance_protection": True,
        "ordnance_protection_radius": 800,
        "detect_ordnance_destruction": True,
        "snap_to_ground_if_destroyed_by_large_explosion": False,
        "max_snapped_height": 80,
        "recent_large_explosion_snap": True,
        "recent_large_explosion_range": 100,
        "recent_large_explosion_time": 4,
        "groundunitordnance_damage_modifier": 1,
        "groundunitordnance_blastwave_modifier": 4,
    }


def loaded_harness() -> DcsPluginHarness:
    harness = DcsPluginHarness()
    harness.set_retribution_config(plugin_options={"splashdamage3": plugin_defaults()})
    harness.load_plugin_script(MAIN_SCRIPT)
    harness.load_plugin_script(CONFIG_SCRIPT)
    return harness


def add_shooter(harness: DcsPluginHarness) -> None:
    harness.add_group(
        {
            "name": "Hog",
            "side": 2,
            "category": 0,
            "units": [
                {
                    "name": "Hog-1",
                    "type": "A-10C_2",
                    "x": 0.0,
                    "z": 0.0,
                    "alt": 2000.0,
                    "airborne": True,
                }
            ],
        }
    )


def test_scripts_load_and_start_the_tracking_loop() -> None:
    harness = loaded_harness()
    harness.assert_no_lua_errors()
    # The main script announces itself and schedules its weapon-tracking tick;
    # the config work order confirms it consumed the Retribution options.
    infos = harness.records("infos")
    assert any("SPLASH DAMAGE" in line for line in infos)
    assert any("Splash Damage 3.4.2 plugin - Setting Up" in line for line in infos)
    assert harness.pending_scheduled() >= 1


def test_config_percent_options_are_normalized() -> None:
    # sd3-config's contract: the generator emits UI percentages and the config
    # work order divides them down to the fractions the script multiplies by.
    harness = loaded_harness()
    options = harness.to_python(harness.lua.eval("splash_damage_options"))
    assert options["overall_scaling"] == plugin_defaults()["overall_scaling"] / 100
    assert (
        options["dynamic_blast_radius_modifier"]
        == plugin_defaults()["dynamic_blast_radius_modifier"] / 100
    )
    assert options["game_messages"] is False


def test_tracked_bomb_detonates_at_its_impact_point() -> None:
    harness = loaded_harness()
    add_shooter(harness)
    harness.advance_to(1.0)
    # A released Mk-84 (a known explTable entry) that the sim removes at t=6:
    # the tracker must resolve the disappearance as an impact and place the
    # scripted explosion at the weapon's last known position.
    harness.fire_shot(
        {
            "weapon": {
                "typeName": "Mk_84",
                "x": 500.0,
                "z": 300.0,
                "alt": 800.0,
                "velocity": {"x": 50.0, "y": -120.0, "z": 0.0},
                "vanishAt": 6.0,
            },
            "initiator": "Hog",
        }
    )
    harness.advance_to(30.0)
    harness.assert_no_lua_errors()
    explosions = harness.records("explosions")
    assert len(explosions) == 1
    assert explosions[0]["x"] == 500.0
    assert explosions[0]["z"] == 300.0
    assert explosions[0]["power"] > 0


def test_unknown_weapon_is_ignored_without_errors() -> None:
    harness = loaded_harness()
    add_shooter(harness)
    harness.advance_to(1.0)
    harness.fire_shot(
        {
            "weapon": {
                "typeName": "NOT_A_REAL_WEAPON",
                "x": 100.0,
                "z": 100.0,
                "alt": 500.0,
                "vanishAt": 4.0,
            },
            "initiator": "Hog",
        }
    )
    harness.advance_to(30.0)
    harness.assert_no_lua_errors()
    assert harness.records("explosions") == []
    # The script's own breadcrumb for an un-cataloged weapon.
    assert any("missing from script" in line for line in harness.records("infos"))
