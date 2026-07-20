#!/usr/bin/env python
"""Build a standalone DCS test mission for land_relocate.lua.

Generates a self-contained Caucasus .miz that reproduces the "carrier hugs the
shore, escorts spawn on land" case the naval relocation handles, wired up exactly
like Retribution wires the base plugin: mist loads first, then land_relocate.lua,
then a small diagnostic script that logs every ship's surface type and position.

Run from the repo root:

    .venv/bin/python scripts/gen_land_relocate_test_mission.py

The .miz is written under docs/superpowers/land_relocate_validation/ (git-excluded).
Copy it to your DCS Missions folder, fly it, and grep dcs.log for "RELOCATE_TEST"
and "land_relocate".

The mission is self-diagnostic so you do not have to trust the coordinates below:
the diagnostic logs the actual surface under each ship at +0.5s and +6s. The
escorts spawn ~1 nm inland of the coast, so they are guaranteed to start on land
and exercise the relocation. If the diagnostic shows the carrier started on land
too, nudge CARRIER_POS until it reports WATER so it can act as the bias anchor.
"""

from __future__ import annotations

from pathlib import Path

from dcs import Mission
from dcs.action import DoScript, DoScriptFile
from dcs.mapping import Point
from dcs.ships import CVN_73, USS_Arleigh_Burke_IIa
from dcs.translation import String
from dcs.triggers import TriggerStart

# --- Geometry (Caucasus, metres; x = north, y = east) ------------------------
# Beached escorts ~1 nm inland of the Black Sea coast SW of Kobuleti. This is the
# Kobuleti airfield ramp (-317962, 635633) shifted 4 nm along bearing 255 deg
# (the direction of the water), which acceptance testing showed leaves them ~1 nm
# from the shoreline and within the relocation search radius.
ESCORT_ORIGIN = Point(-319879, 628477, None)  # type: ignore[arg-type]
ESCORT_SPACING = 250  # metres between the four beached escorts
# Carrier afloat, a further ~3 nm out along the same bearing (well past the
# shoreline). Adjust if the diagnostic reports the carrier started on land.
CARRIER_POS = Point(-321317, 623111, None)  # type: ignore[arg-type]

REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_DIR = REPO_ROOT / "resources" / "plugins" / "base"
OUT_DIR = REPO_ROOT / "docs" / "superpowers" / "land_relocate_validation"
OUT_MIZ = OUT_DIR / "land_relocate_test.miz"

# Diagnostic: log each ship group's surface type + position, before and after the
# relocate pass (which runs at +1s). Greppable with "RELOCATE_TEST".
DIAGNOSTIC_LUA = """
local SURFACE_NAMES = {
    [land.SurfaceType.LAND] = "LAND",
    [land.SurfaceType.SHALLOW_WATER] = "SHALLOW_WATER",
    [land.SurfaceType.WATER] = "WATER",
    [land.SurfaceType.ROAD] = "ROAD",
    [land.SurfaceType.RUNWAY] = "RUNWAY",
}

local function report(label)
    for _, side in ipairs({ coalition.side.RED, coalition.side.BLUE }) do
        for _, group in ipairs(coalition.getGroups(side, Group.Category.SHIP)) do
            for _, unit in ipairs(group:getUnits()) do
                local p = unit:getPoint()
                local surface = land.getSurfaceType({ x = p.x, y = p.z })
                env.info(string.format(
                    "RELOCATE_TEST [%s] %s: %s at x=%.0f z=%.0f",
                    label, unit:getName(), SURFACE_NAMES[surface] or "?", p.x, p.z))
            end
        end
    end
end

-- Before the relocate pass (it is scheduled at +1s) and well after it.
timer.scheduleFunction(function() report("BEFORE") end, {}, timer.getTime() + 0.5)
timer.scheduleFunction(function() report("AFTER") end, {}, timer.getTime() + 6)
"""


def _load_script_file(mission: Mission, filename: str, comment: str) -> None:
    path = (PLUGIN_DIR / filename).resolve()
    if not path.exists():
        raise FileNotFoundError(path)
    fileref = mission.map_resource.add_resource_file(str(path))
    trigger = TriggerStart(comment=comment)
    trigger.add_action(DoScriptFile(fileref))
    mission.triggerrules.triggers.append(trigger)


def main() -> None:
    mission = Mission()  # defaults to Caucasus
    usa = mission.country("USA")
    terrain = mission.terrain

    # Carrier afloat offshore — the deep-water bias anchor.
    mission.ship_group(
        usa,
        "Carrier",
        CVN_73,
        Point(CARRIER_POS.x, CARRIER_POS.y, terrain),
        heading=90,
    )

    # Four escorts ~1 nm inland — guaranteed to start on land.
    escorts = mission.ship_group(
        usa,
        "Escorts",
        USS_Arleigh_Burke_IIa,
        Point(ESCORT_ORIGIN.x, ESCORT_ORIGIN.y, terrain),
        heading=90,
        group_size=1,
    )
    for i in range(1, 4):
        unit = mission.ship(f"Escort-{i + 1}", USS_Arleigh_Burke_IIa)
        unit.position = Point(
            ESCORT_ORIGIN.x + i * ESCORT_SPACING, ESCORT_ORIGIN.y, terrain
        )
        unit.heading = 90
        escorts.add_unit(unit)

    # Wire up the plugin scripts in the same order the base plugin does.
    _load_script_file(mission, "mist_4_5_126.lua", "Load mist")
    _load_script_file(mission, "land_relocate.lua", "Load land_relocate")

    diagnostic = TriggerStart(comment="Load relocate diagnostic")
    diagnostic.add_action(DoScript(String(DIAGNOSTIC_LUA)))
    mission.triggerrules.triggers.append(diagnostic)

    mission.set_description_text(
        "land_relocate.lua validation: four Arleigh Burke escorts spawn ~1 nm "
        "inland SW of Kobuleti next to a CVN-73 offshore. At mission start they "
        "should relocate into deep water, biased toward the carrier. Check dcs.log "
        "for 'RELOCATE_TEST' and 'land_relocate' lines."
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    mission.save(str(OUT_MIZ))
    print(f"wrote {OUT_MIZ}")


if __name__ == "__main__":
    main()
