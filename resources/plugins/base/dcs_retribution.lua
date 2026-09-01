-- the state.json file will be updated according to this schedule and on mission end
local WRITESTATE_SCHEDULE_IN_SECONDS = 15

logger = mist.Logger:new("DCSRetribution", "info")
logger:info("Check that json.lua is loaded : json = "..tostring(json))

crash_events = {} -- killed aircraft will be added via S_EVENT_CRASH event
dead_events = {} -- killed units will be added via S_EVENT_DEAD event
unit_lost_events = {} -- killed units will be added via S_EVENT_UNIT_LOST
kill_events = {} -- killed units will be added via S_EVENT_KILL 
base_capture_events = {}
destroyed_objects_positions = {} -- will be added via S_EVENT_DEAD event
mission_ended = false
dirty_state = false -- Track if state has changed and needs writing

-- Scenery objectives: credit a map-object death to the building it belongs to.
--
-- DCS reports a scenery death with the object's numeric id rather than a name,
-- so the debriefing, which resolves scenery by trigger-zone name, discarded
-- every one. The MapObjectIsDead trigger meant to catch this cannot fire: it
-- needs EVERY map object in the zone dead, and those polygons hold scenery that
-- cannot be destroyed (WOODPILE_01 reports a life of 1e38).
--
-- Deaths are matched to the nearest objective instead. The radius is measured:
-- hits that destroyed the objective landed within 29 m of its zone, collateral
-- from 31 m out.
SCENERY_MATCH_RADIUS = 30

-- Some map objects have no damage model at all. DCS reports a life of 1e38 for
-- them and they never die, so an objective standing on one could never be
-- completed however much ordnance it absorbed. For those the direct hit is the
-- destruction, because nothing else is ever coming.
--
-- Measured on Kola: the four submarines of the CHIMAERA objective at Gadzhiyevo
-- took eight JDAM, every one matching within 2 m of its zone, without losing a
-- point of life. The piers 200 m away, which do have a damage model, lost life
-- to the same bombs.
SCENERY_INDESTRUCTIBLE_LIFE = 1e37

scenery_zone_reported = {} -- zone name -> true, so a building is only counted once
scenery_zones_primed = false

-- Objectives already destroyed on previous turns count as reported, so they are
-- never scored twice. They stay in the list all the same: the destruction zone
-- that replays their rubble at mission start kills their scenery, and those
-- deaths have to land on them rather than on a live neighbour.
local function prime_scenery_zones()
    if scenery_zones_primed or type(RETRIBUTION_SCENERY_ZONES) ~= "table" then
        return
    end
    scenery_zones_primed = true
    local dead = 0
    for _, zone in ipairs(RETRIBUTION_SCENERY_ZONES) do
        if zone.dead then
            scenery_zone_reported[zone.name] = true
            dead = dead + 1
        end
    end
    logger:info(string.format(
        "Scenery objectives: %d known, %d already destroyed, match radius %d m",
        #RETRIBUTION_SCENERY_ZONES, dead, SCENERY_MATCH_RADIUS))
end

-- Nearest objective zone to a dead scenery object. Reads
-- RETRIBUTION_SCENERY_ZONES lazily so it does not care whether the generator
-- seeded it before or after this script loaded.
function scenery_zone_for(obj)
    if type(RETRIBUTION_SCENERY_ZONES) ~= "table" then
        return nil, nil
    end
    prime_scenery_zones()
    local point
    if not pcall(function() point = obj:getPoint() end) or point == nil then
        return nil, nil
    end
    local best, best_distance = nil, nil
    for _, zone in ipairs(RETRIBUTION_SCENERY_ZONES) do
        local dx, dy = point.x - zone.x, point.z - zone.y
        local distance = math.sqrt(dx * dx + dy * dy)
        if best_distance == nil or distance < best_distance then
            best, best_distance = zone, distance
        end
    end
    return best, best_distance
end

-- Credit the objective standing where this scenery object is, at most once.
-- Only the credit is logged: a mission destroys hundreds of unrelated buildings
-- and logging the misses drowns the log.
local function credit_scenery_zone(obj, note)
    local zone, distance = scenery_zone_for(obj)
    if zone == nil or distance > SCENERY_MATCH_RADIUS
            or scenery_zone_reported[zone.name] then
        return false
    end
    scenery_zone_reported[zone.name] = true
    dead_events[#dead_events + 1] = zone.name
    logger:info(string.format("Objective destroyed: '%s' (%.0f m from the hit%s)",
        zone.name, distance, note or ""))
    return true
end

-- Scenery that can never die, so a hit on it has to be the destruction.
local function is_indestructible(obj)
    local life
    if not pcall(function() life = obj:getLife() end) then
        return false
    end
    return life ~= nil and life >= SCENERY_INDESTRUCTIBLE_LIFE
end

local function ends_with(str, ending)
   return ending == "" or str:sub(-#ending) == ending
end

local function messageAll(message)
    local msg = {}
    msg.text = message
    msg.displayTime = 25
    msg.msgFor = {coa = {'all'}}
    mist.message.add(msg)
end

function write_state()
    local _debriefing_file_location = debriefing_file_location
    if not debriefing_file_location or debriefing_file_location == "" then
        error("Unable to save DCS Retribution state: debriefing file path is unavailable")
    end

    if not json then
        error("Unable to save DCS Retribution state, JSON library is not loaded")
    end

    local fp, open_error = io.open(_debriefing_file_location, 'w')
    if not fp then
        error("Unable to open state file for writing: "..tostring(_debriefing_file_location).." ("..tostring(open_error)..")")
    end
    local game_state = {
        ["crash_events"] = crash_events,
        ["dead_events"] = dead_events,
        ["base_capture_events"] = base_capture_events,
		["unit_lost_events"] = unit_lost_events,
		["kill_events"] = kill_events,
        ["mission_ended"] = mission_ended,
        ["destroyed_objects_positions"] = destroyed_objects_positions,
    }
    local ok, write_error = pcall(function()
        fp:write(json:encode(game_state))
    end)
    fp:close()
    if not ok then
        error(write_error)
    end
end

local function canWrite(name)
    local f = io.open(name, "a")
    if f then
        f:close()
        return true
    end
    return false
end

local function testDebriefingFilePath(folderPath, folderName, useCurrentStamping)
    if folderPath then
        local filePath = nil
        if not ends_with(folderPath, "\\") then
            folderPath = folderPath .. "\\"
        end
        if useCurrentStamping then
            filePath = string.format("%sstate-%s.json",folderPath, tostring(os.time()))
        else 
            filePath = string.format("%sstate.json",folderPath)
        end
        local isOk = canWrite(filePath)
        if isOk then 
            logger:info(string.format("The state.json file will be created in %s : (%s)",folderName, filePath))
            return filePath
        end
    end
    return nil
end

local function discoverDebriefingFilePath()   
    -- establish a search pattern into the following modes
    -- 1. Environment variable RETRIBUTION_EXPORT_DIR, to support dedicated server hosting
    -- 2. Embedded DCS Retribution dcsRetribution.installPath (set by the app to its install path), to support locally hosted single player
    -- 3. System temporary folder, as set in the TEMP environment variable
    -- 4. Working directory.
    
    local useCurrentStamping = nil
    if os then  
        useCurrentStamping = os.getenv("RETRIBUTION_EXPORT_STAMPED_STATE")
    end

    local installPath = nil
    if dcsRetribution then
        installPath = dcsRetribution.installPath
    end
    
    if os then
        local result = nil
        -- try using the RETRIBUTION_EXPORT_DIR environment variable
        result = testDebriefingFilePath(os.getenv("RETRIBUTION_EXPORT_DIR"), "RETRIBUTION_EXPORT_DIR", useCurrentStamping)
        if result then
            return result
        end
        -- no joy ? maybe there is a valid path in the mission ?
        result = testDebriefingFilePath(installPath, "the DCS Retribution install folder", useCurrentStamping)
        if result then
            return result
        end
        -- there's always the possibility of using the system temporary folder
        result = testDebriefingFilePath(os.getenv("TEMP"), "TEMP", useCurrentStamping)
        if result then
            return result
        end
    end

    -- nothing worked, let's try the last resort folder : current directory.
    if lfs then
        return testDebriefingFilePath(lfs.writedir().."Missions\\", "the working directory", useCurrentStamping)
    end
    
    return nil
end

debriefing_file_location = discoverDebriefingFilePath()
local error_message_shown = false

write_state_error_handling = function()
    local _debriefing_file_location = debriefing_file_location
    if not debriefing_file_location then 
        _debriefing_file_location = "[nil]"
        logger:error("Unable to find where to write DCS Retribution state")
    end

    -- Only write if state has changed since last write
    if dirty_state then
        if pcall(write_state) then
            dirty_state = false -- Reset dirty flag after successful write
            error_message_shown = false
        else
            if not error_message_shown then
                messageAll("Unable to write DCS Retribution state to ".._debriefing_file_location..
                        "\nYou can abort the mission in DCS Retribution.\n"..
                        "\n\nPlease fix your setup in DCS Retribution, make sure you are pointing to the right installation directory from the File/Preferences menu. Then after fixing the path restart DCS Retribution, and then restart DCS."..
                        "\n\nYou can also try to fix the issue manually by replacing the file <dcs_installation_directory>/Scripts/MissionScripting.lua by the one provided there : <dcs_retribution_folder>/resources/scripts/MissionScripting.lua. And then restart DCS. (This will also have to be done again after each DCS update)"..
                        "\n\nIt's not worth playing, the state of the mission will not be recorded.")
                error_message_shown = true
            end
        end
    end

    -- Reschedule quickly if mission is over and we still have unsaved changes,
    -- otherwise use the normal cadence.
    local next_schedule_in_seconds = WRITESTATE_SCHEDULE_IN_SECONDS
    if mission_ended and dirty_state then
        next_schedule_in_seconds = 1
    end
    mist.scheduleFunction(write_state_error_handling, {}, timer.getTime() + next_schedule_in_seconds)
end

activeWeapons = {}
local function onEvent(event)
    if event.id == world.event.S_EVENT_CRASH and event.initiator then
        crash_events[#crash_events + 1] = event.initiator.getName(event.initiator)
        dirty_state = true
    end
   
    if event.id == world.event.S_EVENT_UNIT_LOST and event.initiator then
        unit_lost_events[#unit_lost_events + 1] = event.initiator.getName(event.initiator)
        dirty_state = true
    end
	
	if event.id == world.event.S_EVENT_KILL and event.target then
        kill_events[#kill_events + 1] = event.target.getName(event.target)
        dirty_state = true
    end

    if event.id == world.event.S_EVENT_HIT and event.target and event.target.getName then
        -- Only scenery gets this far, and only the kind that cannot be damaged:
        -- anything with a damage model is left to die on its own and be counted
        -- by S_EVENT_DEAD below. The numeric name is the cheapest of the three
        -- tests, so it goes first and keeps strafing runs off the zone search.
        local name = event.target.getName(event.target)
        if type(name) == "number" and is_indestructible(event.target) then
            if credit_scenery_zone(event.target, ", indestructible: credited on impact") then
                dirty_state = true
            end
        end
    end

    if event.id == world.event.S_EVENT_DEAD and event.initiator and event.initiator.getName then
        local name = event.initiator.getName(event.initiator)
        if type(name) == "number" then
            -- Scenery. The id is meaningless downstream, so credit the objective
            -- standing on that spot instead, or drop it.
            credit_scenery_zone(event.initiator)
        else
            dead_events[#dead_events + 1] = name
        end
        local position = event.initiator.getPosition(event.initiator)
        local destruction = {}
        destruction.x = position.p.x
        destruction.y = position.p.y
        destruction.z = position.p.z
        destruction.type = event.initiator:getTypeName()
        destruction.orientation = mist.getHeading(event.initiator) * 57.3
        -- Only track actual units/buildings, not debris/crash models
        if destruction.type ~= nil and 
           string.find(destruction.type, "GENERIC_CRASH_MODEL") == nil and
           string.find(destruction.type, "_CRASH") == nil then
            destroyed_objects_positions[#destroyed_objects_positions + 1] = destruction
        end
        dirty_state = true
    end

    if event.id == world.event.S_EVENT_MISSION_END then
        mission_ended = true
        dirty_state = true
        if pcall(write_state) then
            dirty_state = false
        end
    end

end

mist.addEventHandler(onEvent)

dirty_state = true
write_state_error_handling()

-- Escort leash
-- Escorts are kept within their engagement range relative to the escorted group.
-- This is driven by the mission-injected dcsRetribution.Escorts table.

local function escort_leash_get_group(id)
    local group_id = tonumber(id)
    if not group_id or group_id <= 0 then
        return nil
    end
    -- DCS has no Group.getByID; resolve the mission group id to a name via mist.
    local data = mist.DBs.groupsById and mist.DBs.groupsById[group_id]
    return data and Group.getByName(data.groupName) or nil
end

local function escort_leash_set_roe(group, roe)
    if not group then
        return
    end
    local controller = group:getController()
    if controller then
        controller:setOption(AI.Option.Air.id.ROE, roe)
    end
end

local function escort_leash_update()
    -- Keep running even if dcsRetribution data isn't available yet (trigger ordering)
    if not dcsRetribution or type(dcsRetribution.Escorts) ~= "table" then
        return timer.getTime() + 10
    end

    for _, pair in pairs(dcsRetribution.Escorts) do
        local escort_group = escort_leash_get_group(pair.escortGroupId)
        local escorted_group = escort_leash_get_group(pair.escortedGroupId)

        -- If the escorted group no longer exists (dead/despawned), ensure escort isn't stuck.
        if escort_group and not escorted_group then
            escort_leash_set_roe(escort_group, AI.Option.Air.val.ROE.OPEN_FIRE)
        elseif escort_group and escorted_group then
            local escort_unit = escort_group:getUnit(1)
            local escorted_unit = escorted_group:getUnit(1)
            if escort_unit and escorted_unit then
                local escort_pos = escort_unit:getPoint()
                local escorted_pos = escorted_unit:getPoint()
                local dx = escort_pos.x - escorted_pos.x
                local dz = escort_pos.z - escorted_pos.z
                local distance = math.sqrt(dx * dx + dz * dz)

                local max_dist = tonumber(pair.engagementRangeMeters) or 0
                if max_dist > 0 and distance > max_dist then
                    escort_leash_set_roe(escort_group, AI.Option.Air.val.ROE.RETURN_FIRE)
                else
                    escort_leash_set_roe(escort_group, AI.Option.Air.val.ROE.OPEN_FIRE)
                end
            end
        end
    end

    return timer.getTime() + 10
end

timer.scheduleFunction(escort_leash_update, nil, timer.getTime() + 1)
