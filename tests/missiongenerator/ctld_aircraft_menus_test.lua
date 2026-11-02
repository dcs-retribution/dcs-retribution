-- ctld_aircraft_menus_test.lua
--
-- Standalone regression test for resources/plugins/ctld/CTLD.lua covering the
-- per-aircraft F10 transport menus: one shared "CTLD" root per flight group
-- with a distinct callsign-labelled submenu per active, eligible aircraft, and
-- every aircraft-dependent command bound to that aircraft's exact unit name.
--
-- The harness stubs only the DCS mission scripting environment (Unit, Group,
-- missionCommands, mist, trigger, ...). Menu builders AND the captured F10
-- callbacks are the production functions: scenarios click recorded callbacks
-- against real ctld.* state (troops, crates, beacons, menus) and assert on the
-- side effects visible in the stubbed DCS API. No production function is
-- replaced by a recording spy.
--
-- Covers tk dr-e9td acceptance scenarios:
--   1. two helicopters in one flight get distinct callsign menus, the full
--      nested per-aircraft command tree with exact unit-name payloads
--      (including the scalar nearby-crate payload), and no top-level beacon,
--   2. capability/coalition/feature flags still shape each tree,
--   3. missing callsigns fall back to the unit name; duplicate callsigns are
--      disambiguated deterministically; earlier labels stay stable as aircraft
--      activate later,
--   4. repeated scans are idempotent; death (nil-target scans prune the dead
--      tree and empty group roots), same-name replacement detection via the
--      changed unit id (label reused, tree rebuilt), group identity changes
--      (the old group keeps only its surviving aircraft), and returning unit
--      names; dead targets never fall back to a sibling,
--   5. transport registration is independent of the beacon-only top-level
--      "List Radio Beacons" command and the JTAC menu (both directions), and
--      replaces the owned beacon-only command of a beacon-first group once its
--      transport aircraft arrives,
--   6. real troop load/unload/status callbacks mutate only the targeted
--      helicopter's state, including a CTLD scripting callback event,
--   7. real crate spawn/load callbacks load exactly the nearby crate into
--      exactly the targeted helicopter.
--
-- Not run by CI (CI has no Lua); run locally with:
--
--   lua    tests/missiongenerator/ctld_aircraft_menus_test.lua
--   luajit tests/missiongenerator/ctld_aircraft_menus_test.lua
--
-- Both runtimes must exit 0 and print the assertion/scenario summary.

local SCRIPT = "resources/plugins/ctld/CTLD.lua"

-- Runtime portability: Lua 5.4+ removed math.atan2 (the DCS Lua environment is
-- 5.1-compatible and the plugin uses it). Provide it on modern interpreters so
-- the same test file runs under luaJIT and system lua alike.
if math.atan2 == nil then
    math.atan2 = function(y, x) return math.atan(y, x) end
end

-- Assertions -------------------------------------------------------------------

local passed = 0

local function check(condition, label)
    if not condition then
        error("FAIL: " .. tostring(label), 2)
    end
    passed = passed + 1
end

local function check_equal(actual, expected, label)
    if actual ~= expected then
        error(string.format(
            "FAIL: %s (expected %s, got %s)",
            tostring(label),
            tostring(expected),
            tostring(actual)
        ), 2)
    end
    passed = passed + 1
end

-- Test state, reset by each scenario --------------------------------------------

local time_now           -- returned by the timer.getTime stub
local scheduled          -- functions handed to timer.scheduleFunction
local menus              -- records of missionCommands.add*ForGroup calls
local removed_paths      -- missionCommands.removeItemForGroup captures
local next_menu_path     -- menu path token counter
local out_text_group     -- trigger.action.outTextForGroup captures
local out_text_coalition -- trigger.action.outTextForCoalition captures
local set_unit_cargo     -- trigger.action.setUnitInternalCargo captures
local smoke_actions      -- trigger.action.smoke captures
local user_flag_actions  -- trigger.action.setUserFlag captures
local removed_flag_group -- trigger.action.setGroupAIOff captures
local player_units       -- side -> list of player units for coalition.getPlayers
local units_by_name      -- DCS unit name -> unit stub (simulates live objects)
local mist_units_by_id   -- unit id -> mist DB entry { groupId = ... }
local mist_groups_by_id  -- unused bookkeeping kept for clarity of shape
local destroyed_units    -- names of stubs whose :destroy() was called
local trigger_zones      -- name -> { point = { x, y, z }, radius = n }
local env_error_calls    -- env.error messages (production error reports)
local fail_next_command_name -- one-shot missionCommands fault injection for registration failures

-- Unit stubs. Stand in for mission units (transports, logistics, crates). -------

local function make_unit(opts)
    local unit = {
        id = opts.id,
        name = opts.name,
        callsign = opts.callsign,
        number = opts.number,
        type = opts.type or "UH-1H",
        groupId = opts.group,
        alive = opts.alive ~= false,
        spawned = opts.active ~= false,
        in_air = opts.in_air == true,
        speed_vector = opts.speed_vector or { x = 0, y = 0, z = 0 },
        point = opts.point or { x = 0, y = 0, z = 0 },
        coalition_side = opts.side or 2,
        country = opts.country or 2,
        player = opts.player,
    }

    function unit:getName() return self.name end
    function unit:getID() return self.id end
    function unit:getNumber() return self.number end
    function unit:getTypeName() return self.type end
    function unit:getCoalition() return self.coalition_side end
    function unit:getCountry() return self.country end
    function unit:getPoint() return self.point end
    function unit:getVelocity() return self.speed_vector end
    function unit:getLife() return self.alive and 1 or 0 end
    function unit:isActive() return self.alive and self.spawned end
    function unit:inAir() return self.in_air end
    function unit:getPlayerName() return self.player end
    function unit:getPosition()
        return { x = { x = self.point.x, z = self.point.z }, p = self.point }
    end

    if opts.no_callsign then
        -- a transport whose callsign capability is entirely absent
        function unit:getCallsign() error("getCallsign unavailable", 2) end
    else
        function unit:getCallsign() return self.callsign end
    end

    function unit:destroy()
        self.alive = false
        self.spawned = false
        destroyed_units[#destroyed_units + 1] = self.name
    end

    return unit
end

-- Registers a unit stub as the current world object with its DCS name and its
-- mist group id so Unit.getByName / ctld.getGroupId resolve it.

local function register_unit(unit)
    local previous = units_by_name[unit.name]
    units_by_name[unit.name] = unit
    if unit.id ~= nil then
        mist_units_by_id[unit.id] = { groupId = unit.groupId, name = unit.name }
    end
    return unit, previous
end -- registered unit returns (unit, previous) for replacement scenarios

-- Stub environment installation (globals the production script closes over) ----

local function spawn_units_from_group_description(group)
    -- Simulates mist.dynAdd: materialize a group by name and every unit
    -- description it carries as world objects mirroring spawn points.
    local live = {
        name = group.name,
        id = group.name,
        units = {},
    }
    function live:getName() return self.name end
    function live:getID() return self.id end
    function live:getCoalition() return self.coalition or 2 end
    function live:getUnits() return self.units end
    function live:getUnit(index) return self.units[index] end

    for index, description in ipairs(group.units) do
        local object = make_unit({
            id = description.unitId,
            name = description.name,
            type = description.type,
            point = { x = description.x or 0, y = 0, z = description.y or 0 },
        })
        object.spawned = true
        register_unit(object)
        live.units[index] = object
    end

    mist_groups_by_id[group.name] = live
    return live
end

local function remove_menu_records(groupId, path)
    -- Mirrors DCS: removes the item at the path and every descendant record.
    local targets = {}

    local function collect_descendants(record_path)
        for _, menu in ipairs(menus) do
            if menu.parent == record_path and menu.path ~= nil
                    and not targets[menu.path] then
                targets[menu.path] = true
                collect_descendants(menu.path)
            end
        end
    end

    if type(path) == "table" then
        -- nested path of submenu names; the last segment is the item removed
        local parent = nil
        for _, name in ipairs(path) do
            local match = nil
            for _, menu in ipairs(menus) do
                if menu.kind == "submenu" and menu.name == name
                        and menu.groupId == groupId and menu.parent == parent then
                    match = menu
                    break
                end
            end
            if match == nil then
                parent = nil
                break
            end
            parent = match.path
        end
        if parent ~= nil then
            targets[parent] = true
            collect_descendants(parent)
        end
    elseif path ~= nil then
        for _, menu in ipairs(menus) do
            if menu.path == path and (groupId == nil or menu.groupId == groupId) then
                targets[path] = true
                break
            end
        end
        if targets[path] then
            collect_descendants(path)
        end
    end

    local kept = {}
    for _, menu in ipairs(menus) do
        if menu.path == nil or not targets[menu.path] then
            kept[#kept + 1] = menu
        end
    end
    if #kept < #menus then
        removed_paths[#removed_paths + 1] = { groupId = groupId, path = path }
    end
    menus = kept
    return true
end

local function install_globals()

    time_now = 100
    scheduled = {}
    menus = {}
    removed_paths = {}
    env_error_calls = {}
    fail_next_command_name = nil
    player_units = {}
    units_by_name = {}
    mist_units_by_id = {}
    mist_groups_by_id = {}
    destroyed_units = {}
    smoke_actions = {}
    user_flag_actions = {}
    out_text_group = {}
    out_text_coalition = {}
    set_unit_cargo = {}
    trigger_zones = {}

    Unit = {
        getByName = function(name)
            local unit = units_by_name[name]
            if unit ~= nil and unit.alive then
                return unit
            end
            return nil
        end,
    }

    Group = {
        Category = { GROUND = 1, AIRPLANE = 2, HELICOPTER = 3 },
        getByName = function(name) return mist_groups_by_id[name] end,
    }

    StaticObject = {
        getByName = function(name)
            local unit = units_by_name[name]
            if unit ~= nil and unit.alive then
                return unit
            end
            return nil
        end,
    }

    env = {
        info = function() end,
        warning = function() end,
        error = function(msg, _) env_error_calls[#env_error_calls + 1] = tostring(msg) end,
        setErrorMessageBoxEnabled = function() end,
    }

    timer = {
        getTime = function() return time_now end,
        scheduleFunction = function(fn, args, when)
            scheduled[#scheduled + 1] = { fn = fn, args = args, when = when }
            return #scheduled
        end,
    }

    next_menu_path = 1000
    missionCommands = {}

    function missionCommands.addSubMenuForGroup(groupId, name, parentPath)
        next_menu_path = next_menu_path + 1
        menus[#menus + 1] = {
            kind = "submenu",
            groupId = groupId,
            name = name,
            parent = parentPath,
            path = next_menu_path,
        }
        return next_menu_path
    end

    function missionCommands.addCommandForGroup(groupId, name, parentPath, callback, payload)
        if fail_next_command_name == name then
            fail_next_command_name = nil
            error("injected command registration failure: " .. name)
        end
        next_menu_path = next_menu_path + 1
        menus[#menus + 1] = {
            kind = "command",
            groupId = groupId,
            name = name,
            parent = parentPath,
            callback = callback,
            payload = payload,
            path = next_menu_path,
        }
        -- mirrors the DCS scripting API contract the production code relies on:
        -- removeItemForGroup must be able to resolve this returned path value
        return next_menu_path
    end

    function missionCommands.removeItemForGroup(groupId, path)
        return remove_menu_records(groupId, path)
    end

    coalition = {
        getPlayers = function(side) return player_units[side] end,
    }

    trigger = {
        smokeColor = { Red = 1, Blue = 2, Orange = 3, Green = 4 },
        misc = {
            getZone = function(name) return trigger_zones[name] end,
        },
        action = {
            outTextForGroup = function(groupId, text, _hundredths, _clear)
                out_text_group[#out_text_group + 1] = { groupId = groupId, text = text }
            end,
            outTextForCoalition = function(coalitionId, text, _hundredths)
                out_text_coalition[#out_text_coalition + 1] = { coalition = coalitionId, text = text }
            end,
            setUnitInternalCargo = function(unitName, weight)
                set_unit_cargo[#set_unit_cargo + 1] = { unitName = unitName, weight = weight }
            end,
            smoke = function(position, color)
                smoke_actions[#smoke_actions + 1] = { position = position, color = color }
            end,
            setUserFlag = function(flag, number)
                user_flag_actions[#user_flag_actions + 1] = { flag = flag, number = number }
            end,
            setGroupAIOff = function(_) end,
        },
    }

    land = {
        getHeight = function() return 0 end,
    }

    mist = {
        DBs = { unitsById = mist_units_by_id },
        dynAdd = function(group)
            return spawn_units_from_group_description(group)
        end,
        dynAddStatic = function(staticDescription)
            local object = make_unit({
                id = staticDescription.name,
                name = staticDescription.name,
                type = staticDescription.type or "Container red 1",
                point = { x = staticDescription.x or 0, y = 0, z = staticDescription.y or 0 },
            })
            register_unit(object)
            return { name = staticDescription.name }
        end,
        vec = {
            mag = function(v) return math.sqrt((v.x or 0) ^ 2 + (v.y or 0) ^ 2 + (v.z or 0) ^ 2) end,
        },
        utils = {
            deepCopy = function(value)
                if type(value) ~= "table" then
                    return value
                end
                local copy = {}
                for key, item in pairs(value) do
                    copy[key] = mist.utils.deepCopy(item)
                end
                return copy
            end,
            round = function(n) return math.floor(n + 0.5) end,
        },
        ground = {
            buildWP = function(point, _kind, _speed)
                return { x = point.x, z = point.z }
            end,
        },
    }

    World = {}
end

-- Reset the production module's own bookkeeping to the shape ctld.initialize()
-- gives it, plus per-test configuration. Every ctld.* table the executed code
-- paths read or write is listed here so scenarios are state-isolated. ----------

local function reset_ctld_state()

    env_error_calls = {}

    ctld.addedTo = {}
    ctld.transportMenus = {}
    ctld.transportPilotNames = {}
    ctld.beaconMenuPaths = {}
    ctld.callbacks = {}

    ctld.inTransitTroops = {}
    ctld.inTransitFOBCrates = {}
    ctld.inTransitSlingLoadCrates = {}

    ctld.spawnedCratesRED = {}
    ctld.spawnedCratesBLUE = {}
    ctld.droppedTroopsRED = {}
    ctld.droppedTroopsBLUE = {}
    ctld.droppedVehiclesRED = {}
    ctld.droppedVehiclesBLUE = {}
    ctld.droppedFOBCratesRED = {}
    ctld.droppedFOBCratesBLUE = {}

    ctld.pickupZones = {}
    ctld.dropOffZones = {}
    ctld.extractZones = {}
    ctld.logisticUnits = {}

    ctld.deployedRadioBeacons = {}
    ctld.beaconCount = 0

    ctld.jtacRadioAdded = {}
    ctld.jtacGroupSubMenuPath = {}
    ctld.jtacTargetsList = {}
    ctld.jtacUnits = {}
    ctld.jtacCurrentTargets = {}
    ctld.newJtac = { [1] = true, [2] = true }
    ctld.jtacLastRadioRefresh = 0
    ctld.jtacRadioRefreshDelay = 300
    ctld.jtacMenuName = "JTAC"
    ctld.jtacLaserPoints = {}

    ctld.loadableGroups = {}
    ctld.spawnableCrates = {}
    ctld.unitActions = {}
    ctld.unitLoadLimits = {}
    ctld.vehicleTransportEnabled = {}
    ctld.jtacUnitTypes = {}
    ctld.crateLookupTable = {}
    ctld.crateMove = {}
    ctld.crateWait = {}

    -- feature flags: off unless a scenario turns them on
    ctld.enableCrates = false
    ctld.enabledFOBBuilding = false
    ctld.enableSmokeDrop = false
    ctld.enabledRadioBeaconDrop = false
    ctld.hoverPickup = false
    ctld.slingLoad = false
    ctld.staticBugWorkaround = true
    ctld.JTAC_dropEnabled = false
    ctld.JTAC_jtacStatusF10 = false
    ctld.allowRandomAiTeamPickups = false
    ctld.numberOfTroops = 8

    ctld.watch = {}
end

local function run_menu_scan()
    scheduled = {}
    ctld.addF10MenuOptions()
end

-- Two standard transport helicopters in one flight. ------------------------------

local function setup_two_helis(group_id)
    ctld.transportPilotNames = { "helicargo1", "helicargo2" }
    register_unit(make_unit({
        id = 1, name = "helicargo1", group = group_id, callsign = "Uzi 11", number = 1, type = "UH-1H",
    }))
    register_unit(make_unit({
        id = 2, name = "helicargo2", group = group_id, callsign = "Uzi 12", number = 2, type = "UH-1H",
        point = { x = 10, y = 0, z = 10 },
    }))
    ctld.unitLoadLimits = { ["UH-1H"] = 8 }
    -- matches the shipped plugin config: UH-1H is NOT in vehicleTransportEnabled,
    -- so UH-1H carriers get crate spawning instead of the vehicle/FOB submenu
    ctld.vehicleTransportEnabled = {}
end

-- Menu record helpers. These walk the missionCommands call records, which is
-- what the DCS F10 menu derives its tree from; no production accounting table
-- is consulted for structure assertions. ----------------------------------------

local function children_of(menu_path, group_id)
    local found = {}
    for _, menu in ipairs(menus) do
        if menu.parent == menu_path and (group_id == nil or menu.groupId == group_id) then
            found[#found + 1] = menu
        end
    end
    return found
end

local function commands_under(parent_path, group_id)
    local found = {}
    for _, menu in ipairs(children_of(parent_path, group_id)) do
        if menu.kind == "command" then
            found[#found + 1] = menu
        end
    end
    return found
end

-- Name-keyed map of EVERY child record (submenus and commands) under one menu.
-- The production tree nests real submenus (Troop Transport, CTLD Commands,
-- Smoke Markers, Radio Beacons, ...), so tree assertions must consider both
-- kinds, exactly like the actual F10 menu.
local function children_by_name(parent_path, group_id)
    local found = {}
    for _, menu in ipairs(children_of(parent_path, group_id)) do
        found[menu.name] = menu
    end
    return found
end

-- Number of menu records in the subtree rooted at one submenu path, including
-- the root record itself; 0 once the subtree was removed by removeItemForGroup.
local function subtree_size(root_path)
    local count = 0
    local function walk(parent)
        for _, menu in ipairs(menus) do
            if menu.parent == parent then
                count = count + 1
                if menu.kind == "submenu" then
                    walk(menu.path)
                end
            end
        end
    end
    for _, menu in ipairs(menus) do
        if menu.path == root_path then
            count = count + 1
            walk(root_path)
        end
    end
    return count
end

local function find_roots_named(name, group_id)
    local found = {}
    for _, menu in ipairs(menus) do
        if menu.kind == "submenu" and menu.name == name and menu.parent == nil
                and (group_id == nil or menu.groupId == group_id) then
            found[#found + 1] = menu
        end
    end
    return found
end

local function submenus_under(parent_path, name, group_id)
    local found = {}
    for _, menu in ipairs(children_of(parent_path, group_id)) do
        if menu.kind == "submenu" and menu.name == name then
            found[#found + 1] = menu
        end
    end
    return found
end

local function command_above(parent_path, name)
    local found = {}
    for _, menu in ipairs(commands_under(parent_path)) do
        if menu.name == name then
            found[#found + 1] = menu
        end
    end
    check(#found <= 1, "at most one '" .. name .. "' command under a parent")
    return found[1]
end

local function all_commands_named(name)
    local found = {}
    for _, menu in ipairs(menus) do
        if menu.kind == "command" and menu.name == name then
            found[#found + 1] = menu
        end
    end
    return found
end

local function commands_in_group_named(name, group_id)
    local found = {}
    for _, menu in ipairs(menus) do
        if menu.kind == "command" and menu.name == name and menu.groupId == group_id then
            found[#found + 1] = menu
        end
    end
    return found
end

local function click(record)
    check(record ~= nil and type(record.callback) == "function",
        "menu record holds a production callback to click")
    return record.callback(record.payload)
end

-- Message helper: did a group receive a text containing the fragment?

local function group_said(fragment)
    for _, record in ipairs(out_text_group) do
        if string.find(record.text, fragment, 1, true) ~= nil then
            return true
        end
    end
    return false
end

-- Last cargo weight the production code set for one unit name.

local function last_cargo_weight_for(unit_name)
    local weight = nil
    for _, record in ipairs(set_unit_cargo) do
        if record.unitName == unit_name then
            weight = record.weight
        end
    end
    return weight
end

-- A pickup zone covering the map origin so both helis stand inside it. ----------

local function setup_pickup_zone(limit)
    trigger_zones = { pickup = { point = { x = 0, y = 0, z = 0 }, radius = 200 } }
    -- ctld.pickupZones entry shape: { name, smoke, limit, active, coalition }
    ctld.pickupZones = { { "pickup", 0, limit or 5, 1, 2 } }
end

-- Friendly logistics unit so production crate spawning permits the request. -----

local function setup_logistics_depot()
    ctld.logisticUnits = { "ammo depot" }
    register_unit(make_unit({
        id = "ammo depot", name = "ammo depot", type = "ammo depot",
    }))
end

-- Spawn a crate through the production callback used by the spawn menu
-- (same shape as the F10 payload { unitName, weight }). Returns the world
-- crate's name. -----------------------------------------------------------------

local function spawn_production_crate(heli_name, weight, desc)
    local existed = {}
    for name in pairs(ctld.spawnedCratesBLUE) do existed[name] = true end
    ctld.crateLookupTable[tostring(weight)] = {
        unit = desc.unit, desc = desc.desc, weight = weight,
    }
    ctld.spawnCrate({ heli_name, weight })
    for name, details in pairs(ctld.spawnedCratesBLUE) do
        if not existed[name] then
            return name, details
        end
    end
    return nil
end

-- Scenario 1 ---------------------------------------------------------------------
-- Two eligible helicopters in one flight: shared CTLD root, distinct callsign
-- submenus, the full nested command tree, exact unit-name payloads (including
-- the scalar nearby-crate payload), no top-level beacon, and smoke commands
-- that smoke at the selected helicopter's location.

local function test_two_aircraft_distinct_menus_with_unit_bound_payloads()
    reset_ctld_state()
    install_globals()
    setup_two_helis(100)

    ctld.loadableGroups = { { name = "Infantry Squad", inf = 4, total = 4 } }
    ctld.enableCrates = true
    ctld.enabledFOBBuilding = true
    ctld.enableSmokeDrop = true
    ctld.enabledRadioBeaconDrop = true
    ctld.spawnableCrates = {
        ["Test Crates"] = { { weight = 500, desc = "Fuel Barrel", unit = "fuel_barrel", side = nil } },
    }

    run_menu_scan()

    -- root: exactly one shared CTLD subtree at the flight group's top level
    local roots = find_roots_named("CTLD", 100)
    check_equal(#roots, 1, "one shared CTLD root for the flight group")
    local root = roots[1]
    local top_level_for_group = children_of(nil, 100)
    check_equal(#top_level_for_group, 1, "CTLD root is the flight group's only top-level entry")

    -- two aircraft submenus labelled by their DCS radio callsigns
    local heli1_menu = submenus_under(root.path, "Uzi 11", 100)
    check_equal(#heli1_menu, 1, "aircraft 1 submenu labelled Uzi 11")
    heli1_menu = heli1_menu[1]
    local heli2_menu = submenus_under(root.path, "Uzi 12", 100)
    check_equal(#heli2_menu, 1, "aircraft 2 submenu labelled Uzi 12")
    heli2_menu = heli2_menu[1]
    check(heli1_menu.path ~= heli2_menu.path, "the two aircraft submenus are distinct menu paths")

    -- each case clicks its own aircraft's orange smoke exactly once; the two
    -- actions then verify per-aircraft positioning below
    local smoke_clicks = 0
    for _, case in ipairs({
        { menu = heli1_menu, unit = "helicargo1", point_x = 0 },
        { menu = heli2_menu, unit = "helicargo2", point_x = 10 },
    }) do

        local direct_commands = children_by_name(case.menu.path, 100)

        -- level 1: exactly the expected entries, submenus and commands alike
        local expected_at_root = {
            ["Check Cargo"] = true,
            ["Troop Transport"] = true,
            ["Test Crates"] = true,       -- non-vehicle carriers spawn crates here
            ["CTLD Commands"] = true,
            ["Smoke Markers"] = true,
            ["Radio Beacons"] = true,
        }
        for name in pairs(direct_commands) do
            check(expected_at_root[name] ~= nil,
                "aircraft root entry '" .. name .. "' is expected for " .. case.unit)
        end
        check(direct_commands["Check Cargo"] ~= nil, "aircraft command 'Check Cargo' at aircraft root")
        check_equal(direct_commands["Check Cargo"].payload[1], case.unit, "'Check Cargo' targets " .. case.unit)
        check_equal(direct_commands["Check Cargo"].groupId, 100, "aircraft commands registered for the flight group")
        check(direct_commands["Vehicle / FOB Transport"] == nil,
            "non-vehicle carrier has no Vehicle / FOB Transport submenu (config-driven)")

        -- level 2: troop transport commands
        local troop_menu = direct_commands["Troop Transport"]
        check(troop_menu ~= nil, "Troop Transport submenu under " .. case.unit)
        check(troop_menu.kind == "submenu", "Troop Transport is a submenu under " .. case.unit)
        local unload_troops = command_above(troop_menu.path, "Unload / Extract Troops")
        check(unload_troops ~= nil, "troop unload inside Troop Transport")
        check_equal(troop_menu.groupId, 100, "troop submenu belongs to the flight group")
        local load_troops = command_above(troop_menu.path, "Load Infantry Squad")
        check(load_troops ~= nil, "loadable group command inside Troop Transport")
        check_equal(load_troops.payload[1], case.unit, "load command targets " .. case.unit)
        check_equal(load_troops.payload[3].name, "Infantry Squad", "load command carries its group template")
        check_equal(load_troops.payload[4], false, "load command keeps its allowExtract payload")

        -- level 2: spawnable crates offered to carriers without internal transport
        local crate_menu = direct_commands["Test Crates"]
        check(crate_menu ~= nil, "Test Crates submenu under " .. case.unit)
        local fuel = command_above(crate_menu.path, "Fuel Barrel")
        check(fuel ~= nil, "spawnable crate command inside Test Crates")
        check_equal(fuel.payload[1], case.unit, "crate spawn command targets " .. case.unit)
        check_equal(fuel.payload[2], 500, "crate spawn command carries its weight payload")

        -- level 2: CTLD commands incl. the scalar nearby-crate payload
        local ctld_commands_menu = direct_commands["CTLD Commands"]
        check(ctld_commands_menu ~= nil, "CTLD Commands submenu under " .. case.unit)
        local load_nearby = command_above(ctld_commands_menu.path, "Load Nearby Crate")
        check(load_nearby ~= nil, "Load Nearby Crate inside CTLD Commands")
        check_equal(type(load_nearby.payload), "string", "Load Nearby Crate payload is the scalar unit name (not wrapped)")
        check_equal(load_nearby.payload, case.unit, "Load Nearby Crate targets " .. case.unit)
        for _, name in ipairs({
            "Unpack Any Crate", "Drop Crate", "List Nearby Crates", "List FOBs",
        }) do
            local command = command_above(ctld_commands_menu.path, name)
            check(command ~= nil, "'" .. name .. "' present inside CTLD Commands")
            check_equal(command.payload[1], case.unit, "'" .. name .. "' targets " .. case.unit)
        end

        -- level 2: smoke colors all present and smoke at this aircraft's point
        local smoke_menu = direct_commands["Smoke Markers"]
        check(smoke_menu ~= nil, "Smoke Markers submenu under " .. case.unit)
        local orange = command_above(smoke_menu.path, "Drop Orange Smoke")
        check(orange ~= nil, "Drop Orange Smoke inside Smoke Markers")
        check_equal(orange.payload[2], trigger.smokeColor.Orange, "smoke color payload preserved")
        click(orange)
        smoke_clicks = smoke_clicks + 1
        check_equal(#smoke_actions, smoke_clicks, "one smoke action per click so far")
        check_equal(smoke_actions[#smoke_actions].color, trigger.smokeColor.Orange, "orange color reaches trigger.action.smoke")

        -- level 2: radio beacons
        local beacons_menu = direct_commands["Radio Beacons"]
        check(beacons_menu ~= nil, "Radio Beacons submenu under " .. case.unit)
        for _, name in ipairs({ "List Beacons", "Drop Beacon", "Remove Closet Beacon" }) do
            local command = command_above(beacons_menu.path, name)
            check(command ~= nil, "'" .. name .. "' inside Radio Beacons")
            check_equal(command.payload[1], case.unit, "'" .. name .. "' targets " .. case.unit)
        end
    end

    -- the second smoke click must have come from the OTHER helicopter
    check_equal(smoke_actions[1].position.x, 0, "helicargo1 sulphur smoke spawns at helicargo1 x")
    local smoke2 = nil
    check_equal(#smoke_actions, 2, "both smoke clicks reached trigger.action.smoke")
    smoke2 = smoke_actions[2]
    check_equal(math.floor(smoke2.position.x), 10, "helicargo2 smoke spawns at helicargo2 x")

    -- independent scans stay idempotent; nothing is re-registered
    local menus_before = #menus
    run_menu_scan()
    check_equal(#menus, menus_before, "second scan registers nothing twice")
    check_equal(#env_error_calls, 0, "scans report no production errors")
end

-- Scenario 2 ---------------------------------------------------------------------
-- Capability, coalition, and feature flags still shape each aircraft's tree.

local function test_capability_flags_coalition_and_jtac_filtering()
    reset_ctld_state()
    install_globals()

    ctld.transportPilotNames = { "helicargo1", "gazelle1" }
    register_unit(make_unit({
        id = 1, name = "helicargo1", group = 100, callsign = "Uz 11", number = 1, type = "Hercules",
    }))
    register_unit(make_unit({
        id = 2, name = "gazelle1", group = 100, callsign = "Gz 11", number = 2, type = "SA342L",
        point = { x = 4, y = 0, z = 4 },
    }))
    ctld.unitLoadLimits = { ["Hercules"] = 8 }
    -- shipped-config reality: only big aircraft listed in vehicleTransportEnabled
    -- get the Vehicle / FOB Transport submenu
    ctld.vehicleTransportEnabled = { "76MD", "Hercules", "C-130J-30" }
    ctld.unitActions = {
        ["Hercules"] = { crates = true, troops = true },
        ["SA342L"] = { crates = true, troops = false },
    }
    ctld.enabledFOBBuilding = true
    ctld.staticBugWorkaround = false -- exposes Load / Unload FOB Crate

    ctld.spawnableCrates = {
        ["Test Crates"] = {
            { weight = 500, desc = "Fuel Barrel", unit = "fuel_barrel", side = nil },   -- neutral
            { weight = 400, desc = "Ammo Box", unit = "ammo_box", side = 1 },          -- red only
            { weight = 300, desc = "Hunter Crate", unit = "hunter", side = nil },      -- JTAC unit type
        },
    }
    ctld.jtacUnitTypes = { "hunter" }
    ctld.enableCrates = true

    run_menu_scan()

    local roots = find_roots_named("CTLD", 100)
    check_equal(#roots, 1, "one CTLD root for the mixed-capability flight")
    local root = roots[1]

    local heli_menu = submenus_under(root.path, "Uz 11", 100)[1]
    local gaz_menu = submenus_under(root.path, "Gz 11", 100)[1]
    check(heli_menu ~= nil and gaz_menu ~= nil, "both aircraft have labeled submenus")

    local heli_root_children = children_by_name(heli_menu.path, 100)
    local gaz_root_children = children_by_name(gaz_menu.path, 100)

    -- troop capability difference
    check(heli_root_children["Troop Transport"] ~= nil, "troop-capable heli has Troop Transport")
    check(gaz_root_children["Troop Transport"] == nil, "non-troop aircraft has no Troop Transport")

    -- vehicle capability difference follows the shipped vehicleTransportEnabled
    check(heli_root_children["Vehicle / FOB Transport"] ~= nil, "vehicle-capable carrier has Vehicle / FOB Transport")
    local vehicle_menu = heli_root_children["Vehicle / FOB Transport"]
    check(vehicle_menu ~= nil and vehicle_menu.kind == "submenu", "vehicle-capable carrier has Vehicle / FOB Transport")
    local vehicle_items = children_by_name(vehicle_menu.path, 100)
    check(vehicle_items["Unload Vehicles"] ~= nil, "vehicle unload present for vehicle carrier")
    check_equal(vehicle_items["Unload Vehicles"].payload[1], "helicargo1", "vehicle unload binds carrier unit name")
    check_equal(vehicle_items["Unload Vehicles"].payload[2], false, "vehicle unload keeps troops=false payload")
    check(vehicle_items["Load / Extract Vehicles"] ~= nil, "vehicle load/extract present for vehicle carrier")
    check_equal(vehicle_items["Load / Extract Vehicles"].payload[1], "helicargo1", "vehicle load binds carrier unit name")
    check(vehicle_items["Load / Unload FOB Crate"] ~= nil, "FOB crate command when not using the static workaround")
    check_equal(vehicle_items["Load / Unload FOB Crate"].payload[1], "helicargo1", "FOB crate command binds carrier unit name")
    check(vehicle_items["Check Cargo"] ~= nil, "vehicle cargo check present for vehicle carrier")
    check(gaz_root_children["Vehicle / FOB Transport"] == nil, "non-vehicle aircraft has no Vehicle / FOB Transport")

    -- spawnable crates only offered to carriers that cannot internally transport
    check(heli_root_children["Test Crates"] == nil, "vehicle-capable carrier has no spawnable-crate submenu")
    local gaz_crate_menu = gaz_root_children["Test Crates"]
    check(gaz_crate_menu ~= nil, "non-vehicle transport gets its spawnable-crate submenu")
    local crates = children_by_name(gaz_crate_menu.path, 100)
    check(crates["Fuel Barrel"] ~= nil, "neutral-side crate offered")
    check(crates["Ammo Box"] == nil, "opposing-side crate not offered to a blue aircraft")
    check(crates["Hunter Crate"] == nil, "JTAC-type crate not offered while JTAC_dropEnabled is false")
    check_equal(crates["Fuel Barrel"].payload[1], "gazelle1", "crate spawn command binds gazelle unit name")
    check_equal(crates["Fuel Barrel"].payload[2], 500, "crate spawn keeps its weight payload")

    -- with JTAC drop enabled (a fresh group identity rebuilds the tree),
    -- the JTAC-type crate is offered
    local gazelle2 = register_unit(make_unit({
        id = 3, name = "gazelle2", group = 101, callsign = "Gz 21", number = 1, type = "SA342L",
    }))
    ctld.transportPilotNames = { "helicargo1", "gazelle1", "gazelle2" }
    ctld.JTAC_dropEnabled = true
    run_menu_scan()
    local roots101 = find_roots_named("CTLD", 101)
    check_equal(#roots101, 1, "new group identity gets its own CTLD root")
    local gaz2_menu = submenus_under(roots101[1].path, "Gz 21", 101)[1]
    check(gaz2_menu ~= nil, "second gazelle submenu registered under new group")
    local gaz2_children = children_by_name(gaz2_menu.path, 101)
    local gaz2_crate_menu = gaz2_children["Test Crates"]
    check(gaz2_crate_menu ~= nil, "second gazelle has its spawnable-crate submenu under new group")
    local gaz2_crates = children_by_name(gaz2_crate_menu.path, 101)
    check(gaz2_crates["Hunter Crate"] ~= nil, "JTAC-type crate offered once JTAC_dropEnabled is true")

    -- loadable group side filtering: a red-unit limit group is hidden from blue
    ctld.loadableGroups = { { name = "Red Squad", inf = 2, total = 2, side = 1 } }
    run_menu_scan()
    local red_offers = 0
    local blue_offers = 0
    -- scan rebuild registered heli with a fresh tree only for new aircraft;
    -- heli keeps its old tree, which had no Red Squad offer
    for _, menu in ipairs(children_of(find_roots_named("CTLD", 100)[1].path, 100)) do
        if menu.kind == "submenu" and menu.name == "Uz 11" then
            local troops = submenus_under(menu.path, "Troop Transport", 100)
            check_equal(#troops, 1, "heli still has exactly one Troop Transport submenu")
            for _, command in ipairs(commands_under(troops[1].path, 100)) do
                if string.find(command.name, "Red Squad", 1, true) ~= nil then
                    red_offers = red_offers + 1
                end
                if string.find(command.name, "Blue Squad", 1, true) ~= nil then
                    blue_offers = blue_offers + 1
                end
            end
        end
    end
    check_equal(red_offers, 0, "opposing-side load group never offered to this aircraft")
    check_equal(blue_offers, 0, "no phantom blue-side offer while only red was configured")

    -- but the blue-side group scared earlier build off: the built tree of an
    -- already-registered aircraft is not rewritten by later flag flips
    ctld.loadableGroups = { { name = "Blue Squad", inf = 2, total = 2, side = 2 } }
    run_menu_scan()
    for _, menu in ipairs(menus) do
        if menu.kind == "command" and menu.groupId == 100
                and string.find(menu.name, "Blue Squad", 1, true) ~= nil then
            check(nil, "flag flips do not regenerate already-built aircraft trees")
        end
    end

    -- a same-coalition load group IS offered through a NEW registration: fresh
    -- group identity (late joiner), payload binds its own unit name
    local fresh = register_unit(make_unit({
        id = 4, name = "heli2", group = 102, callsign = "Hq 21", number = 1, type = "UH-1H",
    }))
    ctld.transportPilotNames = { "helicargo1", "gazelle1", "gazelle2", "heli2" }
    run_menu_scan()
    local blue = 0
    for _, menu in ipairs(menus) do
        if menu.kind == "command" and menu.name == "Load Blue Squad" and menu.groupId == 102 then
            blue = blue + 1
            check_equal(menu.payload[1], "heli2", "same-coalition load command binds its own aircraft")
            check_equal(menu.payload[3].name, "Blue Squad", "blue-side group template is carried")
        end
    end
    check_equal(blue, 1, "same-coalition load group offered exactly once for the fresh aircraft")
    check_equal(#find_roots_named("CTLD", 102), 1, "fresh aircraft group got its own CTLD root")

    -- the late-registered aircraft is tracked in the registry under its group
    local entry102 = ctld.transportMenus["102"]
    check(entry102 ~= nil and entry102.aircrafts.heli2 ~= nil, "fresh aircraft registered in the group registry")
    check_equal(#env_error_calls, 0, "capability scenarios report no production errors")
    check_equal(#set_unit_cargo, 0, "no cargo actions taken in a menu-only scenario")
end

-- Scenario 3 ---------------------------------------------------------------------
-- Naming: missing callsigns fall back to the unit name; duplicate callsigns in
-- one group are disambiguated deterministically; earlier labels are stable as
-- later aircraft activate.

local function test_naming_fallbacks_collisions_and_late_activation()
    reset_ctld_state()
    install_globals()

    -- missing callsign capability entirely -> label is the unique unit name
    ctld.transportPilotNames = { "helicargoenosign" }
    register_unit(make_unit({
        id = 11, name = "helicargoenosign", group = 100, callsign = nil, no_callsign = true,
        number = 1, type = "UH-1H",
    }))
    run_menu_scan()
    local roots = find_roots_named("CTLD", 100)
    check_equal(#submenus_under(roots[1].path, "helicargoenosign", 100), 1,
        "missing callsign falls back to the unit name")

    -- blank callsign also falls back
    reset_ctld_state()
    install_globals()
    ctld.transportPilotNames = { "helicargoempty" }
    register_unit(make_unit({
        id = 12, name = "helicargoempty", group = 100, callsign = "   ", number = 1, type = "UH-1H",
    }))
    run_menu_scan()
    roots = find_roots_named("CTLD", 100)
    check_equal(#submenus_under(roots[1].path, "helicargoempty", 100), 1,
        "blank callsign falls back to the unit name")

    -- duplicate callsigns -> aircraft number disambiguates deterministically
    reset_ctld_state()
    install_globals()
    ctld.transportPilotNames = { "helicargo3", "helicargo4" }
    register_unit(make_unit({
        id = 13, name = "helicargo3", group = 100, callsign = "Uzi 1-1", number = 1, type = "UH-1H",
    }))
    register_unit(make_unit({
        id = 14, name = "helicargo4", group = 100, callsign = "Uzi 1-1", number = 2, type = "UH-1H",
    }))
    run_menu_scan()
    roots = find_roots_named("CTLD", 100)
    check_equal(#submenus_under(roots[1].path, "Uzi 1-1", 100), 1,
        "collision: first aircraft keeps the plain callsign label")
    check_equal(#submenus_under(roots[1].path, "Uzi 1-1 (#2)", 100), 1,
        "collision: second aircraft disambiguated via DCS aircraft number")

    -- duplicate callsigns with no usable number -> unit name disambiguates
    reset_ctld_state()
    install_globals()
    ctld.transportPilotNames = { "helicargo5", "helicargo6" }
    register_unit(make_unit({
        id = 15, name = "helicargo5", group = 100, callsign = "Uzi 1-1", number = nil, type = "UH-1H",
    }))
    register_unit(make_unit({
        id = 16, name = "helicargo6", group = 100, callsign = "Uzi 1-1", number = nil, type = "UH-1H",
    }))
    run_menu_scan()
    roots = find_roots_named("CTLD", 100)
    check_equal(#submenus_under(roots[1].path, "Uzi 1-1", 100), 1,
        "unknown number: first aircraft keeps the plain callsign label")
    check_equal(#submenus_under(roots[1].path, "Uzi 1-1 (helicargo6)", 100), 1,
        "unknown number: second aircraft disambiguated by its unique unit name")

    -- late activation: only the active aircraft gets menus, the other joins later
    reset_ctld_state()
    install_globals()
    ctld.transportPilotNames = { "helicargo7", "helicargo8" }
    register_unit(make_unit({
        id = 17, name = "helicargo7", group = 100, callsign = "Uzi 1-1", number = 1, type = "UH-1H",
    }))
    local late2 = register_unit(make_unit({
        id = 18, name = "helicargo8", group = 100, callsign = "Uzi 1-1", number = 2, type = "UH-1H",
    }))
    late2.spawned = false -- client slot exists, aircraft not yet active in the mission

    run_menu_scan()
    roots = find_roots_named("CTLD", 100)
    check_equal(#roots, 1, "root created on the first scan")
    check_equal(#submenus_under(roots[1].path, "Uzi 1-1", 100), 1, "late activation: active aircraft labeled plainly")
    check_equal(#submenus_under(roots[1].path, "Uzi 1-1 (#2)", 100), 0,
        "late activation: inactive aircraft has no submenu yet")

    local first_menus_snapshot = #menus
    local first_path = submenus_under(roots[1].path, "Uzi 1-1", 100)[1].path
    local first_tree_size = subtree_size(first_path)
    local first_records = {}
    for _, record in ipairs(menus) do
        first_records[record.path] = record
    end
    late2.spawned = true
    run_menu_scan()
    roots = find_roots_named("CTLD", 100)
    check_equal(#submenus_under(roots[1].path, "Uzi 1-1", 100), 1,
        "late activation: earlier aircraft label is not rewritten")
    check_equal(#submenus_under(roots[1].path, "Uzi 1-1 (#2)", 100), 1,
        "late activation: newly active aircraft gets its own distinct deterministic label")
    local late_path = submenus_under(roots[1].path, "Uzi 1-1 (#2)", 100)[1].path
    check_equal(submenus_under(roots[1].path, "Uzi 1-1", 100)[1].path, first_path,
        "late activation preserves the earlier aircraft's menu path")
    check_equal(subtree_size(first_path), first_tree_size,
        "late activation preserves the earlier aircraft's full subtree")
    local retained_records = 0
    for _, record in ipairs(menus) do
        if first_records[record.path] ~= nil then
            check_equal(record, first_records[record.path],
                "late activation leaves existing menu records untouched")
            retained_records = retained_records + 1
        end
    end
    check_equal(retained_records, first_menus_snapshot,
        "late activation retains every existing menu record")
    check_equal(#menus - first_menus_snapshot, subtree_size(late_path),
        "late activation adds only the new aircraft's command subtree")
    check_equal(#env_error_calls, 0, "late activation scans raise no production errors")

    -- a repeat scan after activation registers nothing further
    local stable_after_second = #menus
    run_menu_scan()
    check_equal(#menus, stable_after_second, "repeated scans after activation stay idempotent")
end

-- Scenario 4 ---------------------------------------------------------------------
-- Object/group identity replacement and death:
--   * a same-name replacement reappearing under the same transport name gets a
--     DISTINCT unit object (new unit id): the registry detects the replacement,
--     the stale tree is removed and rebuilt with the same owned label, and
--     dispatch resolves to the CURRENT live object,
--   * a scan over a still-live object with its unchanged unit id rebuilds
--     nothing (idempotence),
--   * the same-name replacement taking on a CHANGED group id gets a fresh root
--     and tree under the new group; the old group keeps ONLY its surviving
--     aircraft, and a fully emptied group root is removed,
--   * a brand-new group id (new group identity) gets its own tree,
--   * a nil-target scan (dead aircraft) removes the dead tree and, when no
--     live aircraft remain, the empty group root and registry entry,
--   * a dead target never dispatches to the live sibling,
--   * a returned unit name re-registers cleanly with its own label and unit id.

local function test_lifecycle_death_replacement_and_group_change()
    reset_ctld_state()
    install_globals()
    setup_two_helis(100)
    ctld.enableSmokeDrop = true

    run_menu_scan()
    local menus_after_first = #menus
    local root = find_roots_named("CTLD", 100)[1]
    check_equal(#children_of(root.path, 100), 2, "two aircraft submenus built initially")
    local entry = ctld.transportMenus["100"]
    local first_label = entry.aircrafts.helicargo1.label
    local first_path = entry.aircrafts.helicargo1.path
    check_equal(entry.aircrafts.helicargo1.unitId, 1, "registry records the live unit id of helicargo1")
    check_equal(entry.aircrafts.helicargo2.unitId, 2, "registry records the live unit id of helicargo2")
    local heli1_tree_size = subtree_size(first_path)
    check(heli1_tree_size > 3, "the registered tree actually occupied menu records")

    -- a scan over the SAME live unit objects (unchanged unit ids) rebuilds
    -- nothing and keeps the owned paths (idempotence)
    run_menu_scan()
    check_equal(#menus, menus_after_first, "scan over same live objects rebuilds nothing")
    check_equal(ctld.transportMenus["100"].aircrafts.helicargo1.path, first_path,
        "same-object scan keeps the owned menu path")
    check_equal(ctld.transportMenus["100"].aircrafts.helicargo1.unitId, 1,
        "same-object scan keeps the owned unit id")

    -- dead target dispatch must not fall back to the live sibling: killing the
    -- unit WITHOUT a registry update leaves the owned menus in place, and
    -- clicking them dispatches to a dead unit -> no message, no cargo sync
    units_by_name.helicargo1.alive = false
    out_text_group = {}
    set_unit_cargo = {}
    local dead_check = nil
    for _, menu in ipairs(menus) do
        if menu.kind == "command" and menu.name == "Check Cargo" and menu.payload[1] == "helicargo1" then
            dead_check = menu
            break
        end
    end
    click(dead_check)
    check_equal(#out_text_group, 0, "dead aircraft gets no cargo status message (no sibling fallback)")
    check_equal(#set_unit_cargo, 0, "dead aircraft gets no cargo weight syncs (no sibling fallback)")

    -- a nil-target scan over the dead aircraft prunes exactly its tree and its
    -- registry record, while the surviving sibling keeps everything
    run_menu_scan()
    check_equal(subtree_size(first_path), 0, "nil-target scan removed the dead aircraft's whole tree")
    check_equal(entry.aircrafts.helicargo1, nil, "nil-target scan dropped the dead aircraft's registry record")
    check(entry.aircrafts.helicargo2 ~= nil, "the surviving aircraft keeps its registry record")
    check_equal(#menus, menus_after_first - heli1_tree_size,
        "nil-target scan removed exactly the dead aircraft's own menu records")
    check(find_roots_named("CTLD", 100)[1] ~= nil, "the group root survives while a live aircraft remains")
    check_equal(#env_error_calls, 0, "nil-target scans report no production errors")

    -- a same-name replacement reappears with a DISTINCT unit object (and thus
    -- unit id) under the same group id: the rebuild reuses the label, swaps the
    -- tree for a fresh menu path, and re-records the new unit id
    local old_object = units_by_name.helicargo1
    local replacement_object = make_unit({
        id = 30, name = "helicargo1", group = 100, callsign = first_label, number = 1, type = "UH-1H",
        point = { x = 77, y = 2, z = 77 },
    })
    local _, previous_object = register_unit(replacement_object)
    check(replacement_object ~= previous_object, "the replacement is a distinct unit object")
    check_equal(previous_object, old_object, "the replaced object is still the previous world object")
    check_equal(old_object.id, 1, "the previous unit object kept its own unit id")
    check_equal(replacement_object.id, 30, "the replacement unit object has a different unit id")
    run_menu_scan()
    local entry_after_replacement = ctld.transportMenus["100"]
    check_equal(#menus, menus_after_first, "replacement swaps its tree without net menu growth")
    check_equal(#env_error_calls, 0, "same-name replacement raises no production errors")
    check_equal(entry_after_replacement.aircrafts.helicargo1.label, first_label,
        "same-name replacement reclaims the owned label")
    local rebuilt_path = entry_after_replacement.aircrafts.helicargo1.path
    check(rebuilt_path ~= first_path, "replacement detected via unit id builds a FRESH menu path")
    check_equal(subtree_size(first_path), 0, "the replaced aircraft's stale tree was removed")
    check_equal(entry_after_replacement.aircrafts.helicargo1.unitId, 30,
        "registry re-records the replacement unit id")
    check_equal(subtree_size(rebuilt_path), heli1_tree_size,
        "the rebuilt tree carries the same full record set")

    -- dispatch through the REBUILT tree resolves the CURRENT live object
    -- (the replacement with its own position), not the replaced object
    smoke_actions = {}
    local smoke_menu = submenus_under(rebuilt_path, "Smoke Markers", 100)[1]
    check(smoke_menu ~= nil, "the rebuilt tree carries its smoke commands after replacement")
    local drop_orange = command_above(smoke_menu.path, "Drop Orange Smoke")
    click(drop_orange)
    check_equal(#smoke_actions, 1, "one smoke action from the replacement's dispatch")
    check_equal(math.floor(smoke_actions[1].position.x), 77,
        "smoke dispatch resolved the replacement object at its own position")
    check_equal(math.floor(smoke_actions[1].position.z), 77,
        "smoke dispatch resolved the replacement object by unit name, not by stale object identity")

    -- the same-name replacement taking on a CHANGED group identity: fresh root
    -- + fresh tree under the new group, and the old group keeps ONLY its
    -- surviving aircraft
    replacement_object.groupId = 101
    mist_units_by_id[replacement_object.id] = { groupId = 101, name = replacement_object.name }
    run_menu_scan()
    local roots101 = find_roots_named("CTLD", 101)
    check_equal(#roots101, 1, "changed group identity gets its own CTLD root")
    check_equal(#children_of(roots101[1].path, 101), 1, "the new group root holds exactly the relocated aircraft")
    local entry101 = ctld.transportMenus["101"]
    check(entry101 ~= nil and entry101.aircrafts.helicargo1 ~= nil,
        "registry tracks the relocated aircraft under the new group")
    check_equal(entry101.aircrafts.helicargo1.path,
        submenus_under(roots101[1].path, entry101.aircrafts.helicargo1.label, 101)[1].path,
        "registry label matches the actual menu record in the new group")
    check_equal(entry101.aircrafts.helicargo1.unitId, 30, "the moved record keeps its unit id")
    check_equal(subtree_size(rebuilt_path), 0, "the moved aircraft's old-group tree was removed")
    local old_root = find_roots_named("CTLD", 100)[1]
    check(old_root ~= nil, "the old group root survives on its live aircraft")
    check_equal(#children_of(old_root.path, 100), 1, "old group root keeps only the surviving aircraft")
    check_equal(ctld.transportMenus["100"].aircrafts.helicargo1, nil,
        "the old group registry no longer claims the moved unit name")

    -- a fully emptied group root is removed together with its registry entry:
    -- both remaining live aircraft die and their nil-target scans clean up
    units_by_name.helicargo1.alive = false
    local group100_before_final_death = #menus
    units_by_name.helicargo2.alive = false
    run_menu_scan()
    check_equal(#find_roots_named("CTLD", 100), 0, "the emptied group 100 CTLD root was removed")
    check_equal(#find_roots_named("CTLD", 101), 0, "the fully dead moved aircraft's group root was removed")
    check_equal(ctld.transportMenus["100"], nil, "the emptied group's registry entry was removed")
    check_equal(ctld.transportMenus["101"], nil, "the fully dead name's registry entry was removed")
    check_equal(#env_error_calls, 0, "empty-root removal raises no production errors")
    check(group100_before_final_death > 0, "there were still owned menus before the final death scan")

    -- brand-new group identity (a NEW group id): fresh tree, fresh registry
    local third_heli = register_unit(make_unit({
        id = 40, name = "helicargo20", group = 102, callsign = "Uzi 41", number = 1, type = "UH-1H",
    }))
    table.insert(ctld.transportPilotNames, "helicargo20")
    run_menu_scan()
    local roots102 = find_roots_named("CTLD", 102)
    check_equal(#roots102, 1, "brand-new group identity got its own CTLD root")
    check_equal(#children_of(roots102[1].path, 102), 1, "brand-new group identity holds one aircraft submenu")
    check(ctld.transportMenus["102"] ~= nil and ctld.transportMenus["102"].aircrafts.helicargo20 ~= nil,
        "brand-new group identity registered independently of other groups")
    check_equal(#find_roots_named("CTLD", 100), 0,
        "the emptied group stays empty while an unrelated group registers")

    -- the same-name unit returns on an existing slot: its label is claimed
    -- fresh under its group and its unit id is re-recorded
    local replacement2 = make_unit({
        id = 31, name = "helicargo1", group = 101, callsign = first_label, number = 1, type = "UH-1H",
    })
    register_unit(replacement2)
    run_menu_scan()
    check(find_roots_named("CTLD", 101)[1] ~= nil, "the returned unit name recreated its group root")
    check_equal(ctld.transportMenus["101"].aircrafts.helicargo1.unitId, 31,
        "the returning record re-registered with its new unit id")
    check_equal(ctld.transportMenus["101"].aircrafts.helicargo1.label, first_label,
        "the returning aircraft reclaims its label after group recreation")
    check_equal(#children_of(find_roots_named("CTLD", 101)[1].path, 101), 1,
        "the recreated group root holds exactly the returned aircraft")

    -- helicargo2 returns to its ORIGINAL group: group root and tree rebuilt
    units_by_name.helicargo2.alive = true
    run_menu_scan()
    local root100_again = find_roots_named("CTLD", 100)[1]
    check(root100_again ~= nil, "a returning aircraft recreated its original group root")
    check_equal(#children_of(root100_again.path, 100), 1, "the recreated original group root holds one aircraft")
    check_equal(ctld.transportMenus["100"].aircrafts.helicargo2.unitId, 2,
        "the returning original aircraft re-registered under its unit id")

    -- repeated scans over every live registered aircraft register nothing and
    -- never disturb the other groups' trees
    local menus_stable = #menus
    run_menu_scan()
    run_menu_scan()
    check_equal(#menus, menus_stable, "scans across all live registered aircraft stay idempotent")
    check_equal(#children_of(root100_again.path, 100), 1,
        "repeated scans keep the recreated original group root intact")
    check_equal(ctld.transportMenus["102"].aircrafts.helicargo20.label, "Uzi 41",
        "brand-new group aircraft keeps its label")
    check_equal(#env_error_calls, 0, "identity replacement lifecycle raises no production errors")
    check(third_heli ~= nil, "third heli in the new group is present in the world")
end

-- Scenario 5 ---------------------------------------------------------------------
-- Idempotence, and independence of beacon-only and JTAC registration.

local function test_idempotence_registration_separation_beacon_jtac()
    reset_ctld_state()
    install_globals()
    setup_two_helis(100) -- transport flight group 100

    run_menu_scan()
    local total_after_first = #menus
    run_menu_scan()
    run_menu_scan()
    check_equal(#menus, total_after_first, "repeated scans add no duplicate menus")
    check_equal(#env_error_calls, 0, "repeated scans report no production errors")

    -- beacon-only group (no transport aircraft): top-level beacon list command
    local observer = register_unit(make_unit({
        id = 21, name = "observer1", group = 200, callsign = "Ring 1", number = 1, type = "F/A-18C",
    }))
    player_units[2] = { observer }
    ctld.enabledRadioBeaconDrop = true
    run_menu_scan()
    check_equal(#all_commands_named("List Radio Beacons"), 1,
        "beacon-only group receives one top-level beacon list command")
    check_equal(all_commands_named("List Radio Beacons")[1].groupId, 200,
        "the beacon list command belongs to the observer's group")
    run_menu_scan()
    check_equal(#all_commands_named("List Radio Beacons"), 1,
        "beacon-only group does not accumulate duplicate top-level beacons")
    check(ctld.transportMenus["200"] == nil, "beacon-only registration does not create transport bookkeeping")

    -- beacon-first group: a transport aircraft arriving at a group that ALREADY
    -- owns a top-level beacon command must REPLACE the owned beacon-only
    -- command: no redundant top-level beacon next to the CTLD root
    local observer3 = register_unit(make_unit({
        id = 24, name = "observer3", group = 250, callsign = "Chin 1", number = 1, type = "F/A-18C",
    }))
    player_units[2] = { observer3 }
    run_menu_scan()
    check_equal(#commands_in_group_named("List Radio Beacons", 250), 1,
        "beacon-first group receives its own top-level beacon list command")
    check(ctld.beaconMenuPaths["250"] ~= nil,
        "the beacon-only command path is owned for later transport replacement")
    -- then the same group gains a transport aircraft
    register_unit(make_unit({
        id = 25, name = "helicargo15", group = 250, callsign = "Uzi 51", number = 1, type = "UH-1H",
    }))
    table.insert(ctld.transportPilotNames, "helicargo15")
    run_menu_scan()
    check_equal(#commands_in_group_named("List Radio Beacons", 250), 0,
        "transport registration replaced the owned beacon-only command (no redundancy)")
    local toplevel250 = children_of(nil, 250)
    check_equal(#toplevel250, 1, "the beacon-first transport group has only its CTLD root at top level")
    check(toplevel250[1] ~= nil and toplevel250[1].name == "CTLD",
        "the replaced beacon command did not linger as a second top-level entry")
    check(ctld.transportMenus["250"] ~= nil, "the beacon-first group gains full transport bookkeeping")
    check(ctld.transportMenus["250"].aircrafts.helicargo15 ~= nil,
        "the beacon-first group registered the arriving transport aircraft")
    check(ctld.beaconMenuPaths["250"] == nil, "the owned beacon path was cleared after the transport arrival")
    check_equal(#env_error_calls, 0, "beacon-first transport arrival raises no production errors")

    -- transport group: no top-level beacon even when the transport pilot
    -- appears in the coalition player list
    player_units[2] = { units_by_name.helicargo1, observer }
    run_menu_scan()
    check_equal(#children_of(nil, 100), 1, "transport group keeps only its CTLD root at the top level")
    local beacons_for_transport_group = 0
    for _, menu in ipairs(menus) do
        if menu.kind == "command" and menu.name == "List Radio Beacons" and menu.groupId == 100 then
            beacons_for_transport_group = beacons_for_transport_group + 1
        end
    end
    check_equal(beacons_for_transport_group, 0, "transport group never gains the top-level beacon command")
    check_equal(#all_commands_named("List Radio Beacons"), 1, "non-transport beacon command stays unique")

    -- JTAC menu registration stays separate from transport registration
    ctld.JTAC_jtacStatusF10 = true
    run_menu_scan()
    local jtac_submenus = {}
    for _, menu in ipairs(menus) do
        if menu.kind == "submenu" and menu.name == "JTAC" then
            jtac_submenus[menu.groupId] = (jtac_submenus[menu.groupId] or 0) + 1
        end
    end
    check_equal(jtac_submenus[100], 1, "one JTAC submenu for the transport group")
    check_equal(jtac_submenus[200], 1, "one JTAC submenu for the observer group too")
    local jtac_status = nil
    for _, menu in ipairs(menus) do
        if menu.kind == "command" and menu.name == "JTAC Status" and menu.groupId == 100 then
            jtac_status = menu
        end
    end
    check_equal(jtac_status.payload[1], "helicargo1", "JTAC status command binds the invoking pilot's own unit name")
    run_menu_scan()
    local jtac_count = 0
    for _, menu in ipairs(menus) do
        if menu.kind == "submenu" and menu.name == "JTAC" then jtac_count = jtac_count + 1 end
    end
    check_equal(jtac_count, 2, "repeated scans keep exactly one JTAC submenu per group")
    check_equal(#env_error_calls, 0, "JTAC registration raises no production errors")

    -- beacon-first group: a transport arriving at a group that (later) also
    -- has transport aircraft never yields a top-level beacon, and vice versa
    register_unit(make_unit({
        id = 22, name = "helicargo10", group = 300, callsign = "Uzi 31", number = 1, type = "UH-1H",
    }))
    ctld.transportPilotNames = { "helicargo1", "helicargo10" }
    run_menu_scan()
    check(ctld.transportMenus["300"] ~= nil, "fresh transport group receives transport menus")
    local toplevel300 = children_of(nil, 300)
    check_equal(#toplevel300, 1, "beacon-capable transport group still has only its CTLD root at top level")
    check_equal(toplevel300[1].name, "CTLD", "the single top-level entry of the transport group is the CTLD root")

    -- and a second non-transport group keeps its top-level beacon, with no
    -- transport bookkeeping
    local observer2 = register_unit(make_unit({
        id = 23, name = "observer2", group = 400, callsign = "Buzzer 1", number = 1, type = "F-16C",
    }))
    player_units[2] = { observer2 }
    run_menu_scan()
    check_equal(ctld.addedTo["400"], true, "non-transport group keeps its beacon list registration")
    check(ctld.transportMenus["400"] == nil, "non-transport group has no transport bookkeeping")
end

-- Failed aircraft menu registration must not leave an empty group root that
-- suppresses beacon-only registration, and must not remove a registered sibling.
local function test_failed_transport_registration_cleanup_and_retry()
    reset_ctld_state()
    install_globals()
    setup_two_helis(100)
    ctld.transportPilotNames = { "helicargo1" }

    fail_next_command_name = "Check Cargo"
    run_menu_scan()
    check_equal(ctld.transportMenus["100"], nil,
        "failed first aircraft build removes its empty transport registry entry")
    check_equal(#find_roots_named("CTLD", 100), 0,
        "failed first aircraft build removes the empty shared root")
    check_equal(#env_error_calls, 1,
        "failed aircraft build reports its injected command error")
    check_equal(submenus_under(nil, "Uzi 11", 100)[1], nil,
        "failed aircraft build removes its partial aircraft subtree")

    -- A deactivated or dead failed aircraft has no record for ordinary pruning
    -- to discover; the failed-build cleanup must already have removed its root.
    units_by_name.helicargo1.spawned = false
    run_menu_scan()
    check_equal(ctld.transportMenus["100"], nil,
        "deactivation scan after failed registration leaves no stale group entry")
    units_by_name.helicargo1.alive = false
    run_menu_scan()
    check_equal(ctld.transportMenus["100"], nil,
        "death scan after failed registration leaves no stale group entry")

    -- Without the leaked transport entry, a different player in the same group
    -- can register the beacon-only command as usual.
    local observer = register_unit(make_unit({
        id = 3, name = "observer-after-failure", group = 100,
        callsign = "Observer 1", number = 1, type = "F/A-18C",
    }))
    player_units[2] = { observer }
    ctld.enabledRadioBeaconDrop = true
    run_menu_scan()
    check_equal(#commands_in_group_named("List Radio Beacons", 100), 1,
        "beacon-only registration recovers after a failed transport build")

    -- A later successful transport registration replaces that owned beacon
    -- command. A subsequent failure for another aircraft must preserve it.
    local retry = register_unit(make_unit({
        id = 4, name = "helicargo1", group = 100,
        callsign = "Uzi 11", number = 1, type = "UH-1H",
    }))
    check(retry ~= nil, "retry aircraft exists")
    ctld.transportPilotNames = { "helicargo1" }
    run_menu_scan()
    local entry = ctld.transportMenus["100"]
    check(entry ~= nil and entry.aircrafts.helicargo1 ~= nil,
        "successful retry registers the aircraft after initial failure")
    check_equal(#commands_in_group_named("List Radio Beacons", 100), 0,
        "successful retry replaces the recovered beacon-only command")

    local sibling = register_unit(make_unit({
        id = 5, name = "helicargo2", group = 100,
        callsign = "Uzi 12", number = 2, type = "UH-1H",
    }))
    check(sibling ~= nil, "sibling aircraft exists")
    ctld.transportPilotNames = { "helicargo1", "helicargo2" }
    fail_next_command_name = "Check Cargo"
    run_menu_scan()
    check(ctld.transportMenus["100"] == entry,
        "failed sibling build keeps the existing shared registry entry")
    check(entry.aircrafts.helicargo1 ~= nil,
        "failed sibling build keeps the successful aircraft record")
    check_equal(#find_roots_named("CTLD", 100), 1,
        "failed sibling build preserves the shared root")
    check_equal(#children_of(entry.root, 100), 1,
        "failed sibling build removes only its own partial subtree")
    check_equal(#env_error_calls, 2,
        "each injected build failure is reported once")
end

-- Scenario 6 ---------------------------------------------------------------------
-- Real state-changing troop callbacks: load, check, unload mutate only the
-- targeted helicopter's cargo state, weight sync and pickup zone counter, and
-- emit the CTLD scripting callback with the acting unit.

local function test_state_changing_troop_callbacks_are_independent()
    reset_ctld_state()
    install_globals()
    setup_two_helis(100)

    units_by_name.helicargo1.player = "Player A"
    units_by_name.helicargo2.player = "Player B"

    -- a production-level scripting callback registers the load/unload events
    local event_log = {}
    table.insert(ctld.callbacks, function(args)
        event_log[#event_log + 1] = args
    end)

    ctld.loadableGroups = { { name = "Infantry Squad", inf = 4, total = 4 } }
    setup_pickup_zone(5)
    run_menu_scan()

    -- F10 payload shape from the built menus
    local root = find_roots_named("CTLD", 100)[1]
    local heli1_label = "Uzi 11"
    local heli2_label = "Uzi 12"
    local heli1_menu = submenus_under(root.path, heli1_label, 100)[1]
    local heli2_menu = submenus_under(root.path, heli2_label, 100)[1]
    local troop1 = submenus_under(heli1_menu.path, "Troop Transport", 100)[1]
    local troop2 = submenus_under(heli2_menu.path, "Troop Transport", 100)[1]
    local load1 = command_above(troop1.path, "Load Infantry Squad")
    local load2 = command_above(troop2.path, "Load Infantry Squad")
    check(load1 ~= nil and load2 ~= nil, "both aircraft own their load command")
    check_equal(load1.payload[1], "helicargo1", "heli1 load command payload")
    check_equal(load2.payload[1], "helicargo2", "heli2 load command payload")

    -- heli1 airborne: loading does nothing for heli1 and nothing for heli2
    units_by_name.helicargo1.in_air = true
    units_by_name.helicargo1.speed_vector = { x = 5, y = 0, z = 0 }
    check_equal(click(load1), false, "airborne heli load reports failure")
    check_equal(ctld.inTransitTroops["helicargo1"], nil, "airborne heli loads no state")
    check_equal(ctld.inTransitTroops["helicargo2"], nil, "airborne heli load leaves sibling untouched")
    check_equal(ctld.pickupZones[1][3], 5, "airborne load does not consume a zone slot")
    units_by_name.helicargo1.speed_vector = { x = 0, y = 0, z = 0 }
    units_by_name.helicargo1.in_air = false

    -- landed heli1 loads
    check_equal(click(load1), true, "landed heli load reports success")
    check(ctld.inTransitTroops["helicargo1"] ~= nil, "heli1 carries cargo state after load")
    check_equal(#ctld.inTransitTroops["helicargo1"].troops.units, 4, "heli1 carries the 4-soldier squad")
    check_equal(ctld.inTransitTroops["helicargo2"], nil, "heli1's load does not touch heli2")
    check_equal(ctld.pickupZones[1][3], 4, "pickup zone counter decremented once for heli1")
    check(last_cargo_weight_for("helicargo1") ~= nil and last_cargo_weight_for("helicargo1") > 0,
        "heli1 internal cargo weight re-synced after load")
    check(last_cargo_weight_for("helicargo2") == nil, "no cargo weight sync for heli2 during heli1's load")
    check_equal(#event_log, 1, "heli1's load emitted one CTLD callback event")
    check_equal(event_log[1].action, "load_troops", "heli1's load event is a load_troops event")
    check_equal(event_log[1].unit, units_by_name.helicargo1, "heli1's load event carries the acting unit object")

    -- heli2 loads independently afterwards
    check_equal(click(load2), true, "heli2 load success after heli1")
    check_equal(#ctld.inTransitTroops["helicargo2"].troops.units, 4, "heli2 carries its own squad")
    check_equal(#ctld.inTransitTroops["helicargo1"].troops.units, 4, "heli1's cargo state untouched by heli2's load")
    check_equal(ctld.pickupZones[1][3], 3, "pickup zone counter decremented twice total")
    check_equal(#event_log, 2, "heli2's load emitted its own callback event")
    check_equal(event_log[2].unit, units_by_name.helicargo2, "heli2's load event carries heli2")

    -- check cargo status resolves per unit name
    out_text_group = {}
    click(command_above(heli1_menu.path, "Check Cargo"))
    check_equal(#out_text_group, 1, "heli1 cargo check reports once")
    check(group_said("4 troops onboard"), "heli1 cargo check reports its own squad")
    out_text_group = {}
    click(command_above(heli2_menu.path, "Check Cargo"))
    check_equal(#out_text_group, 1, "heli2 cargo check reports once")
    check(group_said("4 troops onboard"), "heli2 cargo check reports its own squad")

    -- unload heli1 only
    local unload1 = command_above(troop1.path, "Unload / Extract Troops")
    check_equal(click(unload1), true, "heli1 unload reports success")
    check_equal(ctld.inTransitTroops["helicargo1"].troops, nil, "heli1's troops cleared after unload")
    check(ctld.inTransitTroops["helicargo2"] ~= nil
        and #ctld.inTransitTroops["helicargo2"].troops.units == 4,
        "heli2 retains its troops after heli1 unloads")
    check_equal(ctld.pickupZones[1][3], 4, "drop in pickup zone returns the slot for heli1")
    local last_cargo = last_cargo_weight_for("helicargo1")
    check(last_cargo ~= nil and last_cargo == 0, "heli1 cargo weight re-synced to 0 after unload")

    -- reverse order: heli2 unloads into an empty world area (no extraction target)
    local unload2 = command_above(troop2.path, "Unload / Extract Troops")
    check_equal(click(unload2), true, "heli2 unload reports success")
    check_equal(ctld.inTransitTroops["helicargo2"].troops, nil, "heli2's troops cleared after unload")
    check_equal(#event_log, 4, "each load/unload pair emitted its own CTLD callback event")
    check_equal(#env_error_calls, 0, "troop callbacks raise no production errors")
end

-- Scenario 7 ---------------------------------------------------------------------
-- Real state-changing crate callbacks: production spawn creates a world crate
-- bound to the acting helicopter, Load Nearby Crate loads exactly one crate
-- into exactly that helicopter, and sibling state is untouched.

local function test_state_changing_crate_callbacks_are_independent()
    reset_ctld_state()
    install_globals()
    setup_two_helis(100)

    ctld.enableCrates = true
    units_by_name.helicargo1.player = "Player A"
    units_by_name.helicargo2.player = "Player B"
    setup_logistics_depot()
    run_menu_scan()

    local root = find_roots_named("CTLD", 100)[1]
    local heli1_menu = submenus_under(root.path, "Uzi 11", 100)[1]
    local heli2_menu = submenus_under(root.path, "Uzi 12", 100)[1]
    local ctld_commands1 = submenus_under(heli1_menu.path, "CTLD Commands", 100)[1]
    local ctld_commands2 = submenus_under(heli2_menu.path, "CTLD Commands", 100)[1]
    local load_crate1 = command_above(ctld_commands1.path, "Load Nearby Crate")
    local load_crate2 = command_above(ctld_commands2.path, "Load Nearby Crate")
    check(load_crate1 ~= nil and load_crate2 ~= nil, "per-aircraft Load Nearby Crate commands present")
    check_equal(type(load_crate1.payload), "string", "scalar payload for heli1 nearby crate load")
    check_equal(load_crate1.payload, "helicargo1", "scalar payload targets heli1")
    check_equal(load_crate2.payload, "helicargo2", "scalar payload targets heli2")

    -- loading with no crates at all is a safe failure, per dist listener
    click(load_crate1)
    check(group_said("No Crates within 50m to load!"), "empty world: heli1 told there are no crates nearby")
    check_equal(ctld.inTransitSlingLoadCrates["helicargo1"], nil, "no state created without a nearby crate")

    -- production spawn: heli1 (landed, in the logistics zone) brings a 500kg crate
    local crate1_name, crate1_details = spawn_production_crate("helicargo1", 500, { unit = "fuel_barrel", desc = "Fuel Barrel" })
    check(crate1_name ~= nil, "production crate spawn registered a world crate")
    check_equal(crate1_details.weight, 500, "crate manifest carries its weight")
    check(units_by_name[crate1_name] ~= nil, "world crate object exists in the (stubbed) DCS world")
    check(ctld.crateMove[crate1_name] ~= nil, "crate tracked for its spawn")
    check_equal(ctld.inTransitSlingLoadCrates["helicargo1"], nil, "spawning does not load anything")

    -- heli1 airborne: must not load
    units_by_name.helicargo1.in_air = true
    units_by_name.helicargo1.speed_vector = { x = 5, y = 0, z = 0 }
    click(load_crate1)
    check(group_said("You must land before you can load a crate!"), "airborne heli told to land first")
    check_equal(ctld.inTransitSlingLoadCrates["helicargo1"], nil, "airborne heli loads nothing")
    check_equal(#destroyed_units, 0, "airborne attempt destroyed nothing")
    units_by_name.helicargo1.in_air = false
    units_by_name.helicargo1.speed_vector = { x = 0, y = 0, z = 0 }

    -- landed heli1 loads its nearby crate exactly
    set_unit_cargo = {}
    click(load_crate1)
    check(ctld.inTransitSlingLoadCrates["helicargo1"] ~= nil, "heli1 loaded the nearby crate")
    check_equal(ctld.inTransitSlingLoadCrates["helicargo1"].desc, "Fuel Barrel", "loaded crate carries its details")
    check_equal(ctld.inTransitSlingLoadCrates["helicargo1"].weight, 500, "loaded crate carries its weight")
    check_equal(ctld.spawnedCratesBLUE[crate1_name], nil, "loaded crate deregistered from the manifest")
    check_equal(#destroyed_units, 1, "loading destroys the world crate object")
    check_equal(destroyed_units[1], crate1_name, "the destroyed object is the loaded crate")
    check(last_cargo_weight_for("helicargo1") == 500, "heli1 internal cargo set from crate weight")
    check_equal(ctld.inTransitSlingLoadCrates["helicargo2"], nil, "heli2 had no crate to load")

    -- second load attempt is rejected
    out_text_group = {}
    click(load_crate1)
    check(group_said("You already have a Fuel Barrel crate onboard!"), "second attempt reports the onboard crate")
    check_equal(ctld.inTransitSlingLoadCrates["helicargo1"].weight, 500, "repeated click keeps one crate")

    -- heli2: spawn its own crate, then try loading while far away
    local crate2_name = spawn_production_crate("helicargo2", 600, { unit = "ammo_box", desc = "Ammo Box" })
    check(crate2_name ~= nil, "heli2 crate spawn registered")
    units_by_name.helicargo2.point = { x = 2000, y = 0, z = 2000 }
    out_text_group = {}
    click(load_crate2)
    check(group_said("No Crates within 50m to load!"), "heli2 told its crate is too far away")
    check_equal(ctld.inTransitSlingLoadCrates["helicargo2"], nil, "heli2 still carries nothing")
    check_equal(ctld.inTransitSlingLoadCrates["helicargo1"].desc, "Fuel Barrel",
        "heli1 keeps its loaded crate throughout heli2's failed attempts")

    -- move heli2 next to its own crate: exactly heli2 loads its own crate
    units_by_name.helicargo2.point = { x = 30, y = 0, z = 0 }
    set_unit_cargo = {}
    out_text_group = {}
    click(load_crate2)
    check(ctld.inTransitSlingLoadCrates["helicargo2"] ~= nil, "heli2 loads its own crate by location")
    check_equal(ctld.inTransitSlingLoadCrates["helicargo2"].weight, 600, "heli2's crate carries heli2's weight")
    check_equal(ctld.inTransitSlingLoadCrates["helicargo1"].weight, 500,
        "heli1's crate state untouched by heli2's load")
    check(last_cargo_weight_for("helicargo2") == 600, "heli2 cargo re-synced from its own crate")
    check_equal(#env_error_calls, 0, "crate callbacks raise no production errors")
    check_equal(#removed_paths, 0, "no transport menu removals during crate operations")
end

-- Driver ---------------------------------------------------------------------------

install_globals()

assert(loadfile(SCRIPT))()

local TESTS = {
    { name = "two-aircraft distinct menus with unit-bound payloads", fn = test_two_aircraft_distinct_menus_with_unit_bound_payloads },
    { name = "capability flags, coalition and JTAC filtering", fn = test_capability_flags_coalition_and_jtac_filtering },
    { name = "naming fallbacks, collisions and late activation", fn = test_naming_fallbacks_collisions_and_late_activation },
    { name = "lifecycle: death, replacement and group change", fn = test_lifecycle_death_replacement_and_group_change },
    { name = "idempotence, registration separation, beacon/JTAC", fn = test_idempotence_registration_separation_beacon_jtac },
    { name = "failed registration cleanup and retry", fn = test_failed_transport_registration_cleanup_and_retry },
    { name = "independent troop callbacks", fn = test_state_changing_troop_callbacks_are_independent },
    { name = "independent crate callbacks", fn = test_state_changing_crate_callbacks_are_independent },
}

local scenario_failures = 0
local failed_names = {}
for _, scenario in ipairs(TESTS) do
    local ok, err = pcall(scenario.fn)
    if not ok then
        scenario_failures = scenario_failures + 1
        failed_names[#failed_names + 1] = scenario.name
        io.stderr:write(string.format("scenario '%s' failed: %s\n", scenario.name, tostring(err)))
    end
end

if scenario_failures > 0 then
    print(string.format("FAILED - %d/%d scenarios failed (%d passing assertions): %s",
        scenario_failures, #TESTS, passed, table.concat(failed_names, ", ")))
    os.exit(1)
end

print(string.format("ok - %d assertions across %d scenarios", passed, #TESTS))
