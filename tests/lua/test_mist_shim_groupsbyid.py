"""mist_moose_shim.lua: the groupsById DB tier.

The escort-leash fix (#850) resolves a mission group id to a name via
``mist.DBs.groupsById[id].groupName``. Under the full MIST build that DB
always exists; the shim replaces MIST, so the table must be populated or the
leash's id fallback silently resolves nothing. Pin the contract.
"""

from __future__ import annotations

from .harness import DcsPluginHarness

SHIM = "resources/plugins/base/mist_moose_shim.lua"


def _harness_with_group() -> DcsPluginHarness:
    harness = DcsPluginHarness()
    # Register the group BEFORE the shim loads: the shim's initial DB refresh
    # runs at load, exactly as in the mission.
    harness.add_group(
        {
            "name": "Strike Escorts",
            "id": 42,
            "side": 2,  # BLUE
            "category": 0,  # AIRPLANE
            "units": [{"name": "Escort 1-1", "type": "F-16C_50", "x": 0, "z": 0}],
        }
    )
    harness.load_plugin_script(SHIM)
    return harness


def test_groups_by_id_maps_id_to_group_name() -> None:
    # The escort leash reads exactly .groupName off the entry.
    harness = _harness_with_group()
    entry = harness.to_python(harness.lua.eval("mist.DBs.groupsById[42]"))
    assert entry is not None
    assert entry["groupName"] == "Strike Escorts"


def test_groups_by_id_unknown_id_is_nil() -> None:
    harness = _harness_with_group()
    assert harness.lua.eval("mist.DBs.groupsById[999]") is None
