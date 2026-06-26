-- land_relocate_test.lua
--
-- Standalone unit test for resources/plugins/base/land_relocate.lua under a
-- mocked DCS/mist environment. Not run by CI (CI has no Lua); run locally with:
--
--   lua    tests/missiongenerator/land_relocate_test.lua
--   luajit tests/missiongenerator/land_relocate_test.lua
--
-- Mirrors the in-DCS acceptance scenarios for the naval relocation mirror of
-- water_relocate.lua: beached ships move to deep water, ships already afloat are
-- untouched, the shallow waterline is skipped in favour of deep water, ships
-- with no reachable deep water are left in place + warned, and group/unit names
-- survive the dynAdd round-trip.

local SCRIPT = "resources/plugins/base/land_relocate.lua"

-- Surface type constants (values are arbitrary; only identity matters).
local SURF = { LAND = 1, ROAD = 2, RUNWAY = 3, WATER = 4, SHALLOW_WATER = 5 }

-- Test state, reset by each scenario via setup().
local surface_fn   -- function(x, y) -> SURF.*
local groups       -- list of ship groups for coalition.side.BLUE
local dynadd_calls -- list of data tables passed to mist.dynAdd
local warnings     -- list of env.warning strings
local scheduled    -- the function handed to timer.scheduleFunction

-- Install the mocked DCS/mist globals the script closes over.
local function setup()
    surface_fn = function()
        return SURF.LAND
    end
    groups = {}
    dynadd_calls = {}
    warnings = {}
    scheduled = nil

    land = {
        SurfaceType = SURF,
        getSurfaceType = function(point)
            return surface_fn(point.x, point.y)
        end,
    }

    coalition = {
        side = { RED = "red", BLUE = "blue" },
        getGroups = function(side, _category)
            if side == "blue" then
                return groups
            end
            return {}
        end,
    }

    Group = { Category = { SHIP = "ship" } }

    mist = {
        getGroupData = function(name)
            for _, g in ipairs(groups) do
                if g.name == name then
                    return g.data
                end
            end
            return nil
        end,
        dynAdd = function(data)
            dynadd_calls[#dynadd_calls + 1] = data
        end,
    }

    env = {
        info = function() end,
        warning = function(msg)
            warnings[#warnings + 1] = msg
        end,
    }

    timer = {
        getTime = function()
            return 0
        end,
        scheduleFunction = function(fn)
            scheduled = fn
        end,
    }
end

-- Register a ship group. The entry doubles as the DCS group object (getName)
-- and the carrier of its mist group data.
local function add_group(name, data)
    groups[#groups + 1] = {
        name = name,
        data = data,
        getName = function(self)
            return self.name
        end,
    }
end

-- Register a single-unit ship group named `name` at (x, y).
local function add_ship(name, x, y)
    add_group(name, {
        name = name,
        units = { { unitName = name .. "-1", x = x, y = y } },
    })
end

-- Load and run the script once against the current mocks.
local function run_script()
    assert(loadfile(SCRIPT))()
    assert(scheduled, "script never scheduled its run function")
    scheduled(nil, 0)
end

local function ship(name)
    for _, g in ipairs(groups) do
        if g.name == name then
            return g.data.units[1]
        end
    end
    error("no ship named " .. name)
end

-- Assertions ------------------------------------------------------------------

local passed = 0
local function check(cond, label)
    if not cond then
        error("FAIL: " .. label, 2)
    end
    passed = passed + 1
end

-- Scenarios -------------------------------------------------------------------

-- A beached ship relocates to the nearest deep water and is re-added.
local function test_beached_ship_relocates()
    setup()
    -- Land for x < 500, deep water beyond.
    surface_fn = function(x)
        if x >= 500 then
            return SURF.WATER
        end
        return SURF.LAND
    end
    add_ship("escort", 0, 0)

    run_script()

    check(ship("escort").x >= 500, "beached ship moved into water")
    check(surface_fn(ship("escort").x) == SURF.WATER, "destination is deep water")
    check(#dynadd_calls == 1, "dynAdd called once for the moved group")
    check(dynadd_calls[1].name == "escort", "group name preserved on dynAdd")
    check(#warnings == 0, "no warning when deep water is reachable")
end

-- A ship already floating in deep water is left untouched.
local function test_floating_ship_untouched()
    setup()
    surface_fn = function()
        return SURF.WATER
    end
    add_ship("carrier", 1000, 0)

    run_script()

    check(ship("carrier").x == 1000, "floating ship not moved")
    check(#dynadd_calls == 0, "no dynAdd for an unchanged group")
end

-- The shallow waterline is skipped; the ship lands in deep water past it.
local function test_shallow_waterline_skipped()
    setup()
    -- Land < 500, a 60 m shallow band, deep water beyond 560.
    surface_fn = function(x)
        if x >= 560 then
            return SURF.WATER
        elseif x >= 500 then
            return SURF.SHALLOW_WATER
        end
        return SURF.LAND
    end
    add_ship("escort", 0, 0)

    run_script()

    check(surface_fn(ship("escort").x) == SURF.WATER, "skipped shallow, landed in deep water")
    check(ship("escort").x >= 560, "moved past the shallow band")
end

-- No deep water within range: leave in place and warn, no dynAdd.
local function test_no_water_warns_and_skips()
    setup()
    surface_fn = function()
        return SURF.LAND
    end
    add_ship("stranded", 0, 0)

    run_script()

    check(ship("stranded").x == 0, "ship left in place when no deep water found")
    check(#dynadd_calls == 0, "no dynAdd when nothing changed")
    check(#warnings == 1, "warned about unreachable deep water")
end

-- A dry spawn waypoint is moved onto deep water too.
local function test_spawn_waypoint_relocated()
    setup()
    surface_fn = function(x)
        if x >= 500 then
            return SURF.WATER
        end
        return SURF.LAND
    end
    add_group("escort", {
        name = "escort",
        -- Unit already afloat, but the spawn waypoint is on land.
        units = { { unitName = "escort-1", x = 1000, y = 0 } },
        route = { points = { { x = 0, y = 0 } } },
    })

    run_script()

    check(groups[1].data.route.points[1].x >= 500, "dry spawn waypoint moved to water")
    check(#dynadd_calls == 1, "dynAdd called for waypoint-only change")
end

-- With deep water on both sides, a beached escort is pulled toward the side an
-- afloat ship (the carrier) sits on, not the first ring candidate.
local function test_relocation_biased_toward_carrier()
    setup()
    -- Land in the middle; deep water both east (x >= 500) and west (x <= -500).
    surface_fn = function(x)
        if x >= 500 or x <= -500 then
            return SURF.WATER
        end
        return SURF.LAND
    end
    -- Carrier afloat to the west; escort beached at the origin.
    add_ship("carrier", -1000, 0)
    add_ship("escort", 0, 0)

    run_script()

    check(ship("escort").x < 0, "beached escort pulled west toward the carrier")
    check(surface_fn(ship("escort").x) == SURF.WATER, "destination is deep water")
    check(ship("carrier").x == -1000, "afloat carrier left untouched")
    check(#dynadd_calls == 1, "only the beached escort is re-added")
    check(dynadd_calls[1].name == "escort", "the re-added group is the escort")
end

-- A narrow river nearer than the open sea is rejected; the ship skips past it to
-- water with a full nautical mile of clearance instead of straddling the sliver.
local function test_narrow_river_rejected()
    setup()
    -- A 60 m wide river band at 500 <= y <= 560, and the open sea at y >= 3000;
    -- everything else is land.
    surface_fn = function(_x, y)
        if y >= 3000 then
            return SURF.WATER
        elseif y >= 500 and y <= 560 then
            return SURF.WATER
        end
        return SURF.LAND
    end
    add_ship("escort", 0, 0)

    run_script()

    check(ship("escort").y > 560, "ship did not settle in the narrow river")
    check(ship("escort").y >= 3000, "ship relocated to the open sea")
    check(#dynadd_calls == 1, "the beached escort was re-added once")
end

-- NARROW CHANNEL, ESCORT UP THE BANK (relaxed gated pass).
-- A 200 m vertical water strip (|x| <= 100) flanked by land; carrier afloat in
-- the strip; escort beached on the bank, well north of the carrier. Strict fails
-- (the strip is too narrow for is_open_water); the gated relaxed pass moves the
-- escort into the strip at a point >= 0.5 nm from the carrier.
local function test_narrow_channel_escort_up_bank()
    setup()
    surface_fn = function(x)
        if x >= -100 and x <= 100 then
            return SURF.WATER
        end
        return SURF.LAND
    end
    add_ship("carrier", 0, 0)
    add_ship("escort", 500, 2000)

    run_script()

    local e = ship("escort")
    check(math.abs(e.x) <= 100, "escort moved into the channel strip")
    local dx, dy = e.x - 0, e.y - 0
    check(math.sqrt(dx * dx + dy * dy) >= 0.5 * 1852, "destination >= 0.5 nm from carrier")
    check(ship("carrier").x == 0 and ship("carrier").y == 0, "carrier untouched")
    check(#warnings == 0, "no warning when fallback relocates the escort")
end

-- ESCORT ABEAM CARRIER (relaxed ungated pass; soft gate).
-- Same strip, but the escort is beached directly abeam the carrier, so every
-- reachable strip point is < 0.5 nm from the carrier. The gated pass therefore
-- finds nothing; the ungated pass still gets the escort afloat (afloat beats
-- beached) at the nearest strip point, even though it is within 0.5 nm.
local function test_escort_abeam_carrier_soft_gate()
    setup()
    surface_fn = function(x)
        if x >= -100 and x <= 100 then
            return SURF.WATER
        end
        return SURF.LAND
    end
    add_ship("carrier", 0, 0)
    add_ship("escort", 500, 0)

    run_script()

    local e = ship("escort")
    check(math.abs(e.x) <= 100, "escort relocated into the strip via ungated pass")
    local dx, dy = e.x - 0, e.y - 0
    check(math.sqrt(dx * dx + dy * dy) < 0.5 * 1852, "destination is the close water (gate bypassed)")
    check(#dynadd_calls == 1, "escort re-added")
    check(#warnings == 0, "escort got afloat, so no warning")
end

-- CLOSED POND NEARER THAN THE CHANNEL (documented limitation).
-- A small near pond (200 <= x <= 400) and a far channel (x >= 5000) with the
-- carrier afloat in it; both too narrow for is_open_water. The relaxed pass takes
-- the NEAREST water -- the near pond -- even though carrier bias points at the far
-- channel. Pins that relaxed has no sea-connectivity check.
local function test_closed_pond_nearer_wins()
    setup()
    surface_fn = function(x)
        if x >= 200 and x <= 400 then
            return SURF.WATER   -- near pond
        elseif x >= 5000 and x <= 5100 then
            return SURF.WATER   -- far channel
        end
        return SURF.LAND
    end
    add_ship("carrier", 5050, 0)
    add_ship("escort", 0, 0)

    run_script()

    local e = ship("escort")
    check(e.x >= 200 and e.x <= 400, "escort settled in the nearer pond, not the far channel")
    check(ship("carrier").x == 5050, "carrier untouched")
    check(#dynadd_calls == 1, "only the escort is re-added")
end

-- THE SPACING GATE ACTUALLY PUSHES AN ESCORT CLEAR OF THE CARRIER (gated != ungated).
-- The escort's NEAREST water is a small pond hugging the carrier (every point of it
-- < 0.5 nm away); a separate open-water strip sits farther east, >= 0.5 nm away.
-- Strict fails (both bodies are too narrow for is_open_water). The gated pass rejects
-- the near pond and lands the escort in the far strip; the ungated pass alone would
-- take the near pond. Asserting the far strip pins the gate: delete the gated pass,
-- or shrink MIN_ANCHOR_DIST below the pond's reach, and the escort lands in the pond.
local function test_gated_pass_pushes_clear_of_carrier()
    setup()
    surface_fn = function(x, y)
        if x >= -100 and x <= 100 and y >= -100 and y <= 100 then
            return SURF.WATER   -- pond hugging the carrier (all of it < 0.5 nm away)
        elseif x >= 2000 and x <= 2100 then
            return SURF.WATER   -- far strip, >= 0.5 nm from the carrier
        end
        return SURF.LAND
    end
    add_ship("carrier", 0, 0)
    add_ship("escort", 500, 0)

    run_script()

    local e = ship("escort")
    check(e.x >= 2000, "gate pushed escort to the far strip, past the near pond")
    local dx, dy = e.x - 0, e.y - 0
    check(math.sqrt(dx * dx + dy * dy) >= 0.5 * 1852, "destination >= 0.5 nm from carrier")
    check(ship("carrier").x == 0 and ship("carrier").y == 0, "carrier untouched")
    check(#dynadd_calls == 1, "only the escort is re-added")
end

-- Driver ----------------------------------------------------------------------

local tests = {
    test_beached_ship_relocates,
    test_floating_ship_untouched,
    test_shallow_waterline_skipped,
    test_no_water_warns_and_skips,
    test_spawn_waypoint_relocated,
    test_relocation_biased_toward_carrier,
    test_narrow_river_rejected,
    test_narrow_channel_escort_up_bank,
    test_escort_abeam_carrier_soft_gate,
    test_closed_pond_nearer_wins,
    test_gated_pass_pushes_clear_of_carrier,
}

for _, t in ipairs(tests) do
    t()
end

print(string.format("ok - %d assertions across %d scenarios", passed, #tests))
