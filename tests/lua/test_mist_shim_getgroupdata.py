"""mist_moose_shim.lua: the getGroupData mission-table read.

The land_relocate/water_relocate scripts call mist.getGroupData(name) and
feed the result back to mist.dynAdd. Under the full MIST build that always
worked; the shim replaces MIST, so the symbol must exist and return a
dynAdd-shaped group definition or the relocate pass dies at runtime. Pin that
contract here.
"""

from __future__ import annotations

from .harness import DcsPluginHarness

SHIM = "resources/plugins/base/mist_moose_shim.lua"


def _harness_with_mission() -> DcsPluginHarness:
    harness = DcsPluginHarness()
    # A minimal env.mission with one blue ship group, shaped like a pydcs miz.
    harness.lua.globals().env.mission = harness.to_lua(
        {
            "coalition": {
                "blue": {
                    "country": [
                        {
                            "id": 2,
                            "ship": {
                                "group": [
                                    {
                                        "name": "Carrier Escorts",
                                        "route": {"points": [{"x": 10.0, "y": 20.0}]},
                                        "units": [
                                            {
                                                "name": "Escort 1-1",
                                                "x": 100.0,
                                                "y": 200.0,
                                                "type": "PERRY",
                                                "skill": "Average",
                                            }
                                        ],
                                    }
                                ]
                            },
                        }
                    ]
                }
            }
        }
    )
    harness.load_plugin_script(SHIM)
    return harness


def test_get_group_data_returns_dynadd_shaped_entry() -> None:
    harness = _harness_with_mission()
    data = harness.to_python(harness.lua.eval('mist.getGroupData("Carrier Escorts")'))
    assert data is not None
    # The relocate scripts read data.units[i].x/.y and data.route.points[1];
    # mist.dynAdd reads country/countryId + category + name.
    assert data["units"][0]["x"] == 100.0
    assert data["units"][0]["y"] == 200.0
    assert data["units"][0]["name"] == "Escort 1-1"
    assert data["route"]["points"][0]["x"] == 10.0
    assert data["country"] == 2
    assert data["category"] == "ship"
    assert data["name"] == "Carrier Escorts"


def test_get_group_data_returns_fresh_copies() -> None:
    # Callers mutate the returned table (the relocate scripts edit unit x/y
    # in place before dynAdd); a second read must not see those edits.
    harness = _harness_with_mission()
    harness.lua.execute(
        'local d = mist.getGroupData("Carrier Escorts"); d.units[1].x = -1'
    )
    data = harness.to_python(harness.lua.eval('mist.getGroupData("Carrier Escorts")'))
    assert data["units"][0]["x"] == 100.0


def test_get_group_data_unknown_group_is_nil() -> None:
    harness = _harness_with_mission()
    assert harness.lua.eval('mist.getGroupData("No Such Group")') is None
