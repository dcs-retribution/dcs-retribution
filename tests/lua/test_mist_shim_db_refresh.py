"""mist_moose_shim.lua: the DB refresh cadence (birth-driven + periodic fallback).

The DBs used to rebuild on a flat 5 s whole-mission ``coalition.getGroups`` scan --
the heaviest standing poll in the plugin stack on a dense mission. Now a late-spawned
group triggers its own debounced rebuild via S_EVENT_BIRTH (so consumers see it within
~2 s, faster than the old scan guaranteed), and the periodic pass -- slowed to 30 s --
only bounds staleness for removals. Pin all three behaviours plus the debounce
coalescing, so a cadence tweak can't silently break a consumer's freshness contract.
"""

from __future__ import annotations

from typing import Any

from .harness import DcsPluginHarness

SHIM = "resources/plugins/base/mist_moose_shim.lua"


def _group(name: str) -> dict[str, Any]:
    return {
        "name": name,
        "side": 2,  # BLUE
        "category": 0,  # AIRPLANE
        "units": [{"name": name + " 1-1", "type": "F-16C_50", "x": 0, "z": 0}],
    }


def _db_entry(h: DcsPluginHarness, name: str) -> Any:
    return h.to_python(h.lua.eval(f"mist.DBs.groupsByName[{name!r}]"))


def test_birth_triggers_a_debounced_refresh() -> None:
    h = DcsPluginHarness()
    h.load_plugin_script(SHIM)

    # Spawned after load: invisible to the DBs until something refreshes them.
    h.add_group(_group("Late Spawn"))
    assert _db_entry(h, "Late Spawn") is None

    # The birth schedules a rebuild; it lands after the debounce, well before the
    # 30 s fallback.
    h.fire_birth("Late Spawn")
    assert _db_entry(h, "Late Spawn") is None
    h.advance_to(3)
    assert _db_entry(h, "Late Spawn") is not None
    h.assert_no_lua_errors()


def test_burst_of_births_coalesces_into_one_rebuild() -> None:
    h = DcsPluginHarness()
    h.load_plugin_script(SHIM)
    # One pending scheduled function: the periodic fallback.
    baseline = h.pending_scheduled()

    h.add_group(_group("Burst A"))
    h.add_group(_group("Burst B"))
    for _ in range(5):
        h.fire_birth("Burst A")
        h.fire_birth("Burst B")
    # Ten births, ONE debounced rebuild scheduled.
    assert h.pending_scheduled() == baseline + 1

    h.advance_to(3)
    assert _db_entry(h, "Burst A") is not None
    assert _db_entry(h, "Burst B") is not None
    h.assert_no_lua_errors()


def test_periodic_fallback_catches_a_birthless_spawn() -> None:
    h = DcsPluginHarness()
    h.load_plugin_script(SHIM)

    # No birth event at all (nothing in DCS should do this, but the fallback is
    # exactly the safety net for it): the 30 s pass picks it up.
    h.add_group(_group("Silent Spawn"))
    h.advance_to(29)
    assert _db_entry(h, "Silent Spawn") is None
    h.advance_to(31)
    assert _db_entry(h, "Silent Spawn") is not None
    h.assert_no_lua_errors()


def test_periodic_fallback_drops_a_dead_group() -> None:
    h = DcsPluginHarness()
    h.add_group(_group("Doomed"))
    h.load_plugin_script(SHIM)
    assert _db_entry(h, "Doomed") is not None

    # Kill it: entry staleness is bounded by one periodic pass.
    h.lua.execute("DcsHarness.groupsByName['Doomed'].exists = false")
    h.advance_to(31)
    assert _db_entry(h, "Doomed") is None
    h.assert_no_lua_errors()
