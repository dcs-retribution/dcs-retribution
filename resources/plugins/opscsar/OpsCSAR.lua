-- Ops.CSAR integration for DCS Retribution.
--
-- Spawns the downed pilots that Retribution recorded on previous turns (injected
-- via the dcsRetribution.CSAR table) using MOOSE Ops.CSAR, and reports confirmed
-- rescues back to Retribution by appending the pilot's UUID to the global
-- `csar_rescued` table that dcs_retribution.lua writes into state.json.
--
-- Assumes MOOSE (Moose.lua) and dcs_retribution.lua have already been loaded.

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
    -- default for (e.g. the Hercules) are accepted as rescue aircraft.
    if type(cfg.rescueTypes) == "table" then
        for _, t in pairs(cfg.rescueTypes) do
            if t.dcs_id then
                CSAR.AircraftType[t.dcs_id] = tonumber(t.capacity) or 4
            end
        end
    end

    -- Group name -> downed-pilot UUID, so a rescue can be attributed to the exact
    -- pilot it recovered.
    local uuid_for_group = {}
    -- Helicopter unit name -> list of pilot UUIDs currently onboard.
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
        my:__Start(1)

        -- Record boarding and rescue so we can report the specific pilot rescued.
        function my:OnAfterBoarded(From, Event, To, Heliname, Woundedgroupname)
            local uuid = uuid_for_group[Woundedgroupname]
            if uuid and Heliname then
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

    local blue_csar = nil
    local red_csar = nil
    if cfg.blueEnabled == "true" then
        blue_csar = make_csar("BLUE", coalition.side.BLUE, cfg.blueTemplate)
    end
    if cfg.redEnabled == "true" then
        red_csar = make_csar("RED", coalition.side.RED, cfg.redTemplate)
    end

    -- Finds a spot near (x, z) where a helicopter can actually set down: the first
    -- land/road surface on an outward spiral. This is the authoritative "not on a
    -- building / not in water" check that Retribution cannot make (it has no
    -- terrain/building data).
    local function landable_coord(x, z)
        local steps = { 0, 25, 50, 75, 100, 150, 200, 250 }
        local angles = { 0, 45, 90, 135, 180, 225, 270, 315 }
        for _, radius in ipairs(steps) do
            local tries = radius == 0 and { 0 } or angles
            for _, deg in ipairs(tries) do
                local rad = math.rad(deg)
                local px = x + radius * math.cos(rad)
                local pz = z + radius * math.sin(rad)
                local surface = land.getSurfaceType({ x = px, y = pz })
                if surface == land.SurfaceType.LAND
                    or surface == land.SurfaceType.ROAD then
                    return COORDINATE:NewFromVec3({ x = px, y = 0, z = pz })
                end
            end
        end
        return nil
    end

    local spawned = 0
    if type(cfg.downedPilots) == "table" then
        for _, dp in pairs(cfg.downedPilots) do
            local instance = (dp.coalition == "red") and red_csar or blue_csar
            if instance ~= nil and dp.id then
                local x = tonumber(dp.x)
                local z = tonumber(dp.z)
                if x and z then
                    local coord = landable_coord(x, z)
                    if coord == nil then
                        opscsar_warn(
                            "No landable spot for downed pilot " .. tostring(dp.id)
                        )
                    else
                        local side_const = (dp.coalition == "red")
                            and coalition.side.RED or coalition.side.BLUE
                        -- Unitname is set to the UUID so the spawned downed-pilot
                        -- group name carries our id; we also map it explicitly.
                        instance:SpawnCASEVAC(
                            coord,
                            side_const,
                            dp.description or "Downed pilot",
                            false,        -- no radio message spam
                            dp.id,        -- Unitname
                            dp.aircraft   -- Typename (shown in the mayday call)
                        )
                        -- MOOSE derives the spawned group name from the unit name;
                        -- track both the raw id and common decorations.
                        uuid_for_group[dp.id] = dp.id
                        spawned = spawned + 1
                    end
                end
            end
        end
    end

    -- Late binding: MOOSE names the spawned wounded group from the CASEVAC unit
    -- name plus a suffix, so also index by any downed pilot group whose name
    -- contains one of our UUIDs. Refresh the mapping when boarding is evaluated.
    local function refresh_group_map()
        for _, instance in pairs({ blue_csar, red_csar }) do
            if instance and instance.downedPilots then
                for _, entry in pairs(instance.downedPilots) do
                    local gname = entry.name
                    if gname then
                        for uuid, _ in pairs(uuid_for_group) do
                            if string.find(gname, uuid, 1, true) then
                                uuid_for_group[gname] = uuid
                            end
                        end
                    end
                end
            end
        end
    end
    timer.scheduleFunction(function()
        refresh_group_map()
        return timer.getTime() + 10
    end, nil, timer.getTime() + 5)

    opscsar_log("=== Ops.CSAR setup complete (spawned " .. spawned .. " pilots) ===")
end

local ok, err = pcall(opscsar_main)
if not ok then
    env.error("[OpsCSAR] Fatal error: " .. tostring(err))
end
