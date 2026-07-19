"""mist_moose_shim.lua: the consumer symbol contract + the new-symbol behavior.

The shim's whole promise is "every mist.* symbol a shipped plugin calls exists
and behaves". The symbol list below is the audited union across the consumers
(base glue, CTLD, EWRS, the EW jammer script, dismounts, Pretense, Skynet-IADS)
-- a missing symbol dies at runtime in the mission, not at parse time, which is
exactly the failure class this file exists to catch. When a plugin grows a new
mist.* call, add it here; the contract test failing is the signal the shim
needs the symbol.
"""

from __future__ import annotations

import math
from typing import Any

from .harness import DcsPluginHarness

SHIM = "resources/plugins/base/mist_moose_shim.lua"

# The audited union of mist.* symbols called by resources/plugins consumers.
CONSUMED_SYMBOLS = [
    "mist.DBs.groupsById",
    "mist.DBs.groupsByName",
    "mist.DBs.unitsById",
    "mist.DBs.unitsByName",
    "mist.DBs.zonesByName",
    "mist.Logger",
    "mist.addEventHandler",
    "mist.dynAdd",
    "mist.dynAddStatic",
    "mist.getGroupData",
    "mist.getGroupPoints",
    "mist.getHeading",
    "mist.getLeadPos",
    "mist.getPitch",
    "mist.getRandPointInCircle",
    "mist.getRandomPointInZone",
    "mist.getRoll",
    "mist.goRoute",
    "mist.ground.buildWP",
    "mist.groupToRandomZone",
    "mist.makeUnitTable",
    "mist.marker.remove",
    "mist.message.add",
    "mist.pointInPolygon",
    "mist.random",
    "mist.removeFunction",
    "mist.respawnGroup",
    "mist.scheduleFunction",
    "mist.teleportToPoint",
    "mist.terrainHeightDiff",
    "mist.tostringLL",
    "mist.tostringMGRS",
    "mist.utils.deepCopy",
    "mist.utils.get2DDist",
    "mist.utils.get3DDist",
    "mist.utils.getDir",
    "mist.utils.getHeadingPoints",
    "mist.utils.makeVec2",
    "mist.utils.makeVec3",
    "mist.utils.makeVec3GL",
    "mist.utils.metersToFeet",
    "mist.utils.metersToNM",
    "mist.utils.mpsToKmph",
    "mist.utils.mpsToKnots",
    "mist.utils.round",
    "mist.utils.tableShow",
    "mist.utils.toDegree",
    "mist.utils.zoneToVec3",
    "mist.vec.dp",
    "mist.vec.mag",
    "mist.vec.sub",
]


def loaded_harness(mission: dict[str, Any] | None = None) -> DcsPluginHarness:
    harness = DcsPluginHarness()
    if mission is not None:
        harness.lua.globals().env.mission = harness.to_lua(mission)
    harness.load_plugin_script(SHIM)
    return harness


def mission_with_zone_and_group() -> dict[str, Any]:
    return {
        "triggers": {
            "zones": [
                {"name": "Circle Zone", "x": 1000.0, "y": 2000.0, "radius": 500.0},
                {
                    "name": "Quad Zone",
                    "x": 0.0,
                    "y": 0.0,
                    "radius": 0.0,
                    "type": 2,
                    "verticies": [
                        {"x": 0.0, "y": 0.0},
                        {"x": 1000.0, "y": 0.0},
                        {"x": 1000.0, "y": 1000.0},
                        {"x": 0.0, "y": 1000.0},
                    ],
                },
            ]
        },
        "coalition": {
            "blue": {
                "country": [
                    {
                        "id": 2,
                        "vehicle": {
                            "group": [
                                {
                                    "name": "Supply Column",
                                    "groupId": 77,
                                    "route": {
                                        "points": [
                                            {"x": 10.0, "y": 20.0},
                                            {"x": 500.0, "y": 600.0},
                                        ]
                                    },
                                    "units": [
                                        {
                                            "name": "Supply Column 1",
                                            "x": 10.0,
                                            "y": 20.0,
                                            "type": "Ural-375",
                                            "skill": "Average",
                                            "heading": 0,
                                        }
                                    ],
                                }
                            ]
                        },
                    }
                ]
            }
        },
    }


def test_every_consumed_symbol_resolves() -> None:
    harness = loaded_harness()
    missing = [
        symbol for symbol in CONSUMED_SYMBOLS if harness.lua.eval(symbol) is None
    ]
    assert not missing, f"shim is missing consumer symbols: {missing}"


def test_speed_conversions() -> None:
    harness = loaded_harness()
    assert harness.lua.eval("mist.utils.mpsToKmph(10)") == 36.0
    assert math.isclose(
        harness.lua.eval("mist.utils.mpsToKnots(51.444)"), 100.0, rel_tol=1e-3
    )


def test_make_vec3_gl_uses_terrain_height() -> None:
    harness = loaded_harness()
    harness.harness.terrainHeight = 123.0
    vec = harness.to_python(harness.lua.eval("mist.utils.makeVec3GL({x = 5, y = 7})"))
    assert vec == {"x": 5, "y": 123.0, "z": 7}


def test_pitch_and_roll_from_unit_orientation() -> None:
    harness = loaded_harness()
    # 30 degrees nose-up: the forward vector's vertical component is sin(30).
    harness.add_group(
        {
            "name": "Jammer",
            "side": 2,
            "category": 0,
            "units": [
                {
                    "name": "Jammer 1-1",
                    "type": "EA-6B",
                    "x": 0.0,
                    "z": 0.0,
                    "alt": 3000.0,
                    "orient": {
                        "x": {"x": math.cos(math.pi / 6), "y": 0.5, "z": 0.0},
                        "y": {"x": -0.5, "y": math.cos(math.pi / 6), "z": 0.0},
                        "z": {"x": 0.0, "y": 0.0, "z": 1.0},
                    },
                }
            ],
        }
    )
    pitch = harness.lua.eval('mist.getPitch(Unit.getByName("Jammer 1-1"))')
    assert math.isclose(pitch, math.pi / 6, rel_tol=1e-6)
    # Wings level: zero roll.
    roll = harness.lua.eval('mist.getRoll(Unit.getByName("Jammer 1-1"))')
    assert math.isclose(roll, 0.0, abs_tol=1e-6)


def test_point_in_polygon() -> None:
    harness = loaded_harness()
    poly = "{ {x = 0, y = 0}, {x = 100, y = 0}, {x = 100, y = 100}, {x = 0, y = 100} }"
    assert harness.lua.eval(f"mist.pointInPolygon({{x = 50, y = 50}}, {poly})") is True
    assert (
        harness.lua.eval(f"mist.pointInPolygon({{x = 150, y = 50}}, {poly})") is False
    )


def test_random_point_in_circular_zone_stays_inside() -> None:
    harness = loaded_harness(mission_with_zone_and_group())
    for _ in range(10):
        point = harness.to_python(
            harness.lua.eval('mist.getRandomPointInZone("Circle Zone")')
        )
        distance = math.hypot(point["x"] - 1000.0, point["y"] - 2000.0)
        assert distance <= 500.0 + 1e-6


def test_random_point_in_quad_zone_lands_in_the_polygon() -> None:
    harness = loaded_harness(mission_with_zone_and_group())
    for _ in range(10):
        point = harness.to_python(
            harness.lua.eval('mist.getRandomPointInZone("Quad Zone")')
        )
        assert -1e-6 <= point["x"] <= 1000.0 + 1e-6
        assert -1e-6 <= point["y"] <= 1000.0 + 1e-6


def test_marker_remove_reaches_the_dcs_panel() -> None:
    harness = loaded_harness()
    assert harness.lua.eval("mist.marker.remove(41)") is True
    assert harness.records("removedMarks") == [41]


def test_group_points_reads_the_me_route() -> None:
    harness = loaded_harness(mission_with_zone_and_group())
    points = harness.to_python(harness.lua.eval('mist.getGroupPoints("Supply Column")'))
    assert points == [{"x": 10.0, "y": 20.0}, {"x": 500.0, "y": 600.0}]
    by_id = harness.to_python(harness.lua.eval("mist.getGroupPoints(77)"))
    assert by_id == points


def test_respawn_group_reregisters_the_me_group() -> None:
    harness = loaded_harness(mission_with_zone_and_group())
    # The dismounts/Pretense respawn path: the ME group died; respawn re-adds it
    # from the mission-table definition with its route re-applied.
    result = harness.to_python(
        harness.lua.eval('mist.respawnGroup("Supply Column", true)')
    )
    assert result is not None
    assert result["name"] == "Supply Column"
    assert result["units"][0]["x"] == 10.0
    # The spawn went through coalition.addGroup: the group is findable again.
    assert harness.lua.eval('Group.getByName("Supply Column") ~= nil') is True
    harness.assert_no_lua_errors()


def test_teleport_to_point_moves_a_live_group() -> None:
    harness = loaded_harness(mission_with_zone_and_group())
    harness.add_group(
        {
            "name": "Patrol",
            "side": 1,
            "category": 2,  # GROUND -> category "vehicle" in the snapshot
            "units": [
                {"name": "Patrol 1", "type": "BTR-80", "x": 0.0, "z": 0.0, "id": 9}
            ],
        }
    )
    # The Pretense supply-run shape: relocate the live group near a point.
    harness.lua.execute(
        "mist.teleportToPoint({groupName = 'Patrol', action = 'teleport', "
        "initTasks = false, point = {x = 4000, y = 0, z = 6000}, radius = 50})"
    )
    harness.assert_no_lua_errors()
    moved = harness.to_python(
        harness.lua.eval('Group.getByName("Patrol"):getUnit(1):getPoint()')
    )
    distance = math.hypot(moved["x"] - 4000.0, moved["z"] - 6000.0)
    assert distance <= 50.0 + 1e-6
