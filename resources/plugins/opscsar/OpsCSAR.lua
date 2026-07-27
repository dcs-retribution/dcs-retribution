-- Ops.CSAR integration for DCS Retribution.
--
-- Spawns the downed pilots that Retribution recorded on previous turns (injected
-- via the dcsRetribution.CSAR table) using MOOSE Ops.CSAR, and reports confirmed
-- rescues back to Retribution by appending the pilot's UUID to the global
-- `csar_rescued` table that dcs_retribution.lua writes into state.json.
--
-- Assumes MOOSE (Moose.lua) and dcs_retribution.lua have already been loaded.

-- How far from the stored position we will search for a spot a helicopter can
-- actually set down. Kept tight so the pilot stays close to the pickup waypoint
-- the AI rescue flight was routed to.
local SEARCH_MAX_RADIUS = 150
local SEARCH_STEP = 25
-- Max terrain height variation (metres) across a small ring for a spot to count
-- as landable.
local FLATNESS_RING = 15
local FLATNESS_TOLERANCE = 3.0

-- AI pickup tuning. MOOSE only boards pilots onto *player* helicopters, so
-- AI-flown rescues are handled below.
local AI_APPROACH_DISTANCE = 250 -- helo on station this close -> pilot runs to it
local AI_BOARD_DISTANCE = 30 -- pilot this close -> boarded
local AI_PATIENCE_SECONDS = 120 -- board anyway if the run-in stalls
local AI_CHECK_INTERVAL = 10
-- A helo hovering at or below this AGL counts as on station even if it never
-- touches down. Terrain the AI refuses to land on is common, and a hoist pickup
-- is a realistic outcome, so this keeps rescues working on rough ground.
local AI_HOVER_AGL = 30

local function opscsar_log(msg)
    env.info("[OpsCSAR] " .. tostring(msg))
end

local function opscsar_warn(msg)
    env.warning("[OpsCSAR] " .. tostring(msg))
end

local function opscsar_main()
    if not dcsRetribution or type(dcsRetribution.CSAR) ~= "table" then
        opscsar_log("No CSAR data injected; nothing to do.")
        return
    end
    if CSAR == nil then
        opscsar_warn("MOOSE Ops.CSAR (CSAR class) not found; is Moose.lua loaded?")
        return
    end

    csar_rescued = csar_rescued or {}
    local cfg = dcsRetribution.CSAR

    opscsar_log("=== Ops.CSAR starting ===")

    -- Warn if the FlightControl AICSAR system is also active, since running both
    -- CSAR systems at once causes duplicate rescue helicopters and confusion.
    if AICSAR ~= nil then
        opscsar_warn(
            "AICSAR appears to be loaded as well. Running Ops.CSAR and AICSAR "
            .. "together is not recommended."
        )
        trigger.action.outText(
            "WARNING: Both Ops.CSAR and AICSAR are enabled. Disable one of them.",
            20
        )
    end

    -- Extend the MOOSE transport-capacity whitelist so types MOOSE doesn't ship a
    -- default for (e.g. the CH-47D) are accepted as rescue aircraft.
    if type(cfg.rescueTypes) == "table" then
        for _, t in pairs(cfg.rescueTypes) do
            if t.dcs_id then
                CSAR.AircraftType[t.dcs_id] = tonumber(t.capacity) or 4
            end
        end
    end

    -- Finds a spot near (x, z) where a helicopter can actually set down: land or
    -- road surface, and flat enough to put skids on. This is the authoritative
    -- terrain check -- Retribution has no elevation or building data, so its
    -- stored position is only a best guess.
    local function surface_ok(x, z)
        local surface = land.getSurfaceType({ x = x, y = z })
        return surface == land.SurfaceType.LAND or surface == land.SurfaceType.ROAD
    end

    local function flat_enough(x, z)
        local base = land.getHeight({ x = x, y = z })
        local lowest, highest = base, base
        for deg = 0, 315, 45 do
            local rad = math.rad(deg)
            local h = land.getHeight({
                x = x + FLATNESS_RING * math.cos(rad),
                y = z + FLATNESS_RING * math.sin(rad),
            })
            if h < lowest then lowest = h end
            if h > highest then highest = h end
        end
        return (highest - lowest) <= FLATNESS_TOLERANCE
    end

    local function landable_coord(x, z)
        -- Prefer a flat spot; fall back to any land/road surface so a pilot in
        -- rough terrain is still rescuable, just less comfortably.
        local fallback = nil
        for radius = 0, SEARCH_MAX_RADIUS, SEARCH_STEP do
            local angles = radius == 0 and { 0 } or { 0, 45, 90, 135, 180, 225, 270, 315 }
            for _, deg in ipairs(angles) do
                local rad = math.rad(deg)
                local px = x + radius * math.cos(rad)
                local pz = z + radius * math.sin(rad)
                if surface_ok(px, pz) then
                    if flat_enough(px, pz) then
                        return COORDINATE:NewFromVec3({ x = px, y = 0, z = pz }), true
                    end
                    fallback = fallback
                        or COORDINATE:NewFromVec3({ x = px, y = 0, z = pz })
                end
            end
        end
        return fallback, false
    end

    local blue_csar = nil
    local red_csar = nil
    -- Helicopter unit name -> list of pilot UUIDs currently onboard (player pickups).
    local onboard = {}

    local function make_csar(side_name, side_const, template)
        if template == nil or template == "" then
            opscsar_warn("No pilot template for " .. side_name .. "; skipping side.")
            return nil
        end
        if GROUP:FindByName(template) == nil then
            opscsar_warn(
                "Pilot template '" .. template .. "' not found for " .. side_name
            )
            return nil
        end
        local my = CSAR:New(side_const, template, "CSAR")
        my.enableForAI = cfg.rescueAI == "true"
        -- MOOSE defaults these to USA/Russia and applies them with InitCountry()
        -- when spawning a pilot. DCS derives coalition membership from country, so
        -- they must match the faction actually flying for this side.
        local country_override = tonumber(
            side_const == coalition.side.RED and cfg.redCountry or cfg.blueCountry
        )
        if country_override then
            if side_const == coalition.side.RED then
                my.countryred = country_override
            else
                my.countryblue = country_override
            end
        end
        my:__Start(1)

        -- Player pickups: record boarding and rescue so we can attribute the
        -- rescue to the exact pilot recovered.
        function my:OnAfterBoarded(From, Event, To, Heliname, Woundedgroupname)
            local uuid = nil
            for _, entry in pairs(self.downedPilots or {}) do
                if entry.name == Woundedgroupname then
                    uuid = entry.originalUnit
                    break
                end
            end
            if uuid and uuid ~= "" and Heliname then
                onboard[Heliname] = onboard[Heliname] or {}
                table.insert(onboard[Heliname], uuid)
                opscsar_log("Pilot " .. uuid .. " boarded " .. Heliname)
            end
        end

        function my:OnAfterRescued(From, Event, To, HeliUnit, HeliName, PilotsSaved)
            local saved = onboard[HeliName]
            if saved then
                for _, uuid in pairs(saved) do
                    table.insert(csar_rescued, uuid)
                    opscsar_log("Pilot " .. uuid .. " rescued by " .. tostring(HeliName))
                end
                onboard[HeliName] = nil
                dirty_state = true
            end
        end

        opscsar_log(side_name .. " Ops.CSAR started (template=" .. template .. ")")
        return my
    end

    if cfg.blueEnabled == "true" then
        blue_csar = make_csar("BLUE", coalition.side.BLUE, cfg.blueTemplate)
    end
    if cfg.redEnabled == "true" then
        red_csar = make_csar("RED", coalition.side.RED, cfg.redTemplate)
    end

    local spawned = 0
    if type(cfg.downedPilots) == "table" then
        for _, dp in pairs(cfg.downedPilots) do
            local instance = (dp.coalition == "red") and red_csar or blue_csar
            if instance ~= nil and dp.id then
                local x = tonumber(dp.x)
                local z = tonumber(dp.z)
                if x and z then
                    local coord, flat = landable_coord(x, z)
                    if coord == nil then
                        opscsar_warn(
                            "No landable spot for downed pilot " .. tostring(dp.id)
                        )
                    else
                        local side_const = (dp.coalition == "red")
                            and coalition.side.RED or coalition.side.BLUE
                        local country_id = (dp.coalition == "red")
                            and instance.countryred or instance.countryblue
                        -- _AddCsar rather than SpawnCASEVAC: the public CASEVAC
                        -- wrapper hardcodes frequency 0, which suppresses the ADF
                        -- beacon players home in on. Passing nil generates one.
                        -- The UUID goes in as the unit name so it comes back to us
                        -- on the downed-pilot record as `originalUnit`.
                        instance:_AddCsar(
                            side_const,
                            country_id,
                            coord,
                            dp.aircraft or "Pilot",
                            dp.id,
                            dp.description or "Downed pilot",
                            nil,
                            false,
                            dp.description or "Downed pilot",
                            false
                        )
                        spawned = spawned + 1
                        if not flat then
                            opscsar_log(
                                "Downed pilot " .. tostring(dp.id)
                                .. " placed on uneven ground; landing may be tricky."
                            )
                        end
                    end
                end
            end
        end
    end

    -- ------------------------------------------------------------------
    -- AI rescue pickups.
    --
    -- MOOSE Ops.CSAR only ever boards pilots onto *player* helicopters: the
    -- csarUnits list that drives _CheckWoundedGroupStatus is built in
    -- _AddMedevacMenuItem, which filters on _unit:IsPlayer(). Retribution's
    -- auto-planner also flies AI CSAR missions, so without this an AI helo lands
    -- next to the pilot, sits there, and leaves again. Handle those ourselves.
    -- ------------------------------------------------------------------
    local ai_state = {} -- pilot group name -> { approached = bool, since = time }

    local function complete_ai_rescue(instance, entry, heli_name)
        local uuid = entry.originalUnit
        if uuid and uuid ~= "" then
            table.insert(csar_rescued, uuid)
            dirty_state = true
            opscsar_log(
                "Pilot " .. uuid .. " recovered by AI rescue " .. tostring(heli_name)
            )
        end
        instance:_RemoveNameFromDownedPilots(entry.name, true)
        if entry.group and entry.group:IsAlive() then
            entry.group:Destroy(false)
        end
        ai_state[entry.name] = nil
    end

    local function nearest_ai_rescue_unit(instance, pilot_coord)
        local best_unit, best_distance = nil, nil
        local heli_set = instance.allheligroupset
        if not heli_set then
            return nil, nil
        end
        for _, group in pairs(heli_set:GetSetObjects() or {}) do
            if group and group:IsAlive() then
                for _, unit in pairs(group:GetUnits() or {}) do
                    -- Players are MOOSE's job; only handle AI here.
                    if unit and unit:IsAlive() and not unit:IsPlayer() then
                        -- On station = landed, or hovering low enough to hoist.
                        local agl = unit:GetAltitude(true) or 9999
                        if not unit:InAir() or agl <= AI_HOVER_AGL then
                            local distance =
                                pilot_coord:Get2DDistance(unit:GetCoordinate())
                            if best_distance == nil or distance < best_distance then
                                best_unit, best_distance = unit, distance
                            end
                        end
                    end
                end
            end
        end
        return best_unit, best_distance
    end

    local function check_ai_pickups(instance)
        if instance == nil then
            return
        end
        for _, entry in pairs(instance.downedPilots or {}) do
            local group = entry.alive and entry.group or nil
            if group and group:IsAlive() then
                local pilot_coord = group:GetCoordinate()
                if pilot_coord then
                    local unit, distance = nearest_ai_rescue_unit(instance, pilot_coord)
                    if unit and distance and distance <= AI_APPROACH_DISTANCE then
                        local state = ai_state[entry.name]
                        if state == nil then
                            -- Send the pilot running to the helicopter so the
                            -- pickup reads correctly to anyone watching.
                            state = { since = timer.getTime() }
                            ai_state[entry.name] = state
                            group:RouteGroundTo(unit:GetCoordinate(), 10, "Off Road", 0)
                            opscsar_log(
                                "AI rescue " .. unit:GetName() .. " on station near "
                                .. tostring(entry.desc) .. "; pilot moving to board."
                            )
                        end
                        local waited = timer.getTime() - state.since
                        if distance <= AI_BOARD_DISTANCE
                            or waited >= AI_PATIENCE_SECONDS then
                            complete_ai_rescue(instance, entry, unit:GetName())
                        end
                    end
                end
            end
        end
    end

    if blue_csar or red_csar then
        timer.scheduleFunction(function()
            local ok, err = pcall(function()
                check_ai_pickups(blue_csar)
                check_ai_pickups(red_csar)
            end)
            if not ok then
                opscsar_warn("AI pickup check failed: " .. tostring(err))
            end
            return timer.getTime() + AI_CHECK_INTERVAL
        end, nil, timer.getTime() + AI_CHECK_INTERVAL)
    end

    opscsar_log("=== Ops.CSAR setup complete (spawned " .. spawned .. " pilots) ===")
end

local ok, err = pcall(opscsar_main)
if not ok then
    env.error("[OpsCSAR] Fatal error: " .. tostring(err))
end
