-- CSAR integration for DCS Retribution.
--
-- Spawns the downed pilots that Retribution recorded on previous turns (injected
-- via the dcsRetribution.CSAR table) and reports confirmed rescues back to
-- Retribution by appending the pilot's UUID to the global `csar_rescued` table
-- that dcs_retribution.lua writes into state.json.
--
-- Two separate paths, chosen per pilot by the `aiRescue` flag Retribution sets:
--
--  * Player rescues (aiRescue == "false") use MOOSE Ops.CSAR, which gives the
--    player ADF beacons, the F10 radio menu, smoke and its own boarding logic.
--
--  * AI rescues (aiRescue == "true") are handled entirely here with the stock
--    DCS scripting API. Ops.CSAR cannot do these: CSAR:_AddMedevacMenuItem builds
--    the `csarUnits` list that drives its boarding loop by filtering on
--    _unit:IsPlayer(), so an AI helicopter is never considered and the pilot just
--    stands there while the helo lands, waits and leaves.
--
-- Assumes MOOSE (Moose.lua) and dcs_retribution.lua have already been loaded.

-- Terrain search for a spot a helicopter can actually set down. Kept tight so the
-- pilot stays near the pickup waypoint the rescue flight was routed to.
local SEARCH_MAX_RADIUS = 150
local SEARCH_STEP = 25
local FLATNESS_RING = 15
local FLATNESS_TOLERANCE = 3.0

-- AI pickup tuning.
local AI_ZONE_RADIUS = 300 -- helo inside this of the pilot -> pickup begins
local AI_BOARD_DISTANCE = 30 -- pilot this close to the helo -> boarded
local AI_PATIENCE_SECONDS = 90 -- board anyway if the pilot's run-in stalls
local AI_CHECK_INTERVAL = 5
-- A helo hovering at or below this AGL counts as on station even if it never
-- touches down; the AI often refuses to land on rough ground, and a hoist pickup
-- is a realistic outcome.
local AI_HOVER_AGL = 30
local PILOT_RUN_SPEED = 10 -- m/s

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

    csar_rescued = csar_rescued or {}
    local cfg = dcsRetribution.CSAR

    opscsar_log("=== CSAR starting ===")

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

    -- ------------------------------------------------------------------
    -- Terrain: find somewhere a helicopter can put its skids down.
    -- ------------------------------------------------------------------
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

    -- Returns x, z, flat. Prefers a flat spot, falls back to any land/road so a
    -- pilot down in rough terrain is still rescuable.
    local function landable_spot(x, z)
        local fx, fz = nil, nil
        for radius = 0, SEARCH_MAX_RADIUS, SEARCH_STEP do
            local angles = radius == 0 and { 0 } or { 0, 45, 90, 135, 180, 225, 270, 315 }
            for _, deg in ipairs(angles) do
                local rad = math.rad(deg)
                local px = x + radius * math.cos(rad)
                local pz = z + radius * math.sin(rad)
                if surface_ok(px, pz) then
                    if flat_enough(px, pz) then
                        return px, pz, true
                    end
                    if fx == nil then
                        fx, fz = px, pz
                    end
                end
            end
        end
        return fx, fz, false
    end

    -- ------------------------------------------------------------------
    -- Player path: MOOSE Ops.CSAR.
    -- ------------------------------------------------------------------
    local blue_csar, red_csar = nil, nil
    local onboard = {} -- helo unit name -> list of pilot UUIDs aboard

    local function make_csar(side_name, side_const, template)
        if CSAR == nil then
            opscsar_warn("MOOSE Ops.CSAR not found; player CSAR unavailable.")
            return nil
        end
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

    -- ------------------------------------------------------------------
    -- AI path: our own spawn, zone and pickup watcher (stock DCS API only).
    -- ------------------------------------------------------------------
    local ai_pilots = {} -- list of tracked AI-rescue pilots

    local function spawn_ai_pilot(dp, x, z, side_const, country_id, template)
        -- Clone the late-activated pilot template Retribution put in the mission.
        local template_group = Group.getByName(template)
        if template_group == nil then
            opscsar_warn("Pilot template '" .. tostring(template) .. "' missing.")
            return nil
        end
        local template_unit = template_group:getUnit(1)
        if template_unit == nil then
            opscsar_warn("Pilot template '" .. tostring(template) .. "' has no unit.")
            return nil
        end

        local group_name = "CSAR_AI_PILOT_" .. tostring(dp.id)
        local group_data = {
            visible = true,
            taskSelected = true,
            route = {},
            groupId = nil,
            tasks = {},
            hidden = false,
            units = {
                [1] = {
                    type = template_unit:getTypeName(),
                    transportable = { randomTransportable = false },
                    unitId = nil,
                    skill = "Average",
                    y = z,
                    x = x,
                    name = group_name .. " Pilot",
                    heading = 0,
                    playerCanDrive = false,
                },
            },
            y = z,
            x = x,
            name = group_name,
            start_time = 0,
            task = "Ground Nothing",
        }

        local ok, err = pcall(function()
            coalition.addGroup(country_id, Group.Category.GROUND, group_data)
        end)
        if not ok then
            opscsar_warn("Could not spawn AI-rescue pilot: " .. tostring(err))
            return nil
        end

        -- Keep the pilot alive and passive while they wait, the same way MOOSE
        -- Ops.CSAR treats its own downed pilots. A stray round killing the
        -- survivor before the helicopter arrives is not interesting gameplay.
        pcall(function()
            local group = Group.getByName(group_name)
            local controller = group and group:getController() or nil
            if controller then
                controller:setCommand({ id = "SetImmortal", params = { value = true } })
                controller:setOption(
                    AI.Option.Ground.id.ROE, AI.Option.Ground.val.ROE.WEAPON_HOLD
                )
                controller:setOption(
                    AI.Option.Ground.id.ALARM_STATE,
                    AI.Option.Ground.val.ALARM_STATE.GREEN
                )
            end
        end)
        return group_name
    end

    local next_mark_id = 92000
    local function mark_pickup_zone(x, z, side_const)
        -- Draw the pickup zone on the F10 map so the rescue is visible.
        local mark_id = next_mark_id
        next_mark_id = next_mark_id + 1
        local colour = side_const == coalition.side.RED
            and { 1, 0, 0, 0.6 } or { 0, 0.6, 1, 0.6 }
        local fill = side_const == coalition.side.RED
            and { 1, 0, 0, 0.15 } or { 0, 0.6, 1, 0.15 }
        pcall(function()
            trigger.action.circleToAll(
                side_const == coalition.side.RED and 1 or 2,
                mark_id,
                { x = x, y = 0, z = z },
                AI_ZONE_RADIUS,
                colour,
                fill,
                1,
                true
            )
        end)
        return mark_id
    end

    -- Order the pilot to run to the helicopter. Cosmetic: the rescue completes on
    -- proximity/patience regardless, so a failed route never blocks a pickup.
    local function route_pilot_to(group_name, x, z)
        local group = Group.getByName(group_name)
        if group == nil then
            return
        end
        local controller = group:getController()
        if controller == nil then
            return
        end
        local unit = group:getUnit(1)
        if unit == nil then
            return
        end
        local from = unit:getPoint()
        pcall(function()
            controller:setTask({
                id = "Mission",
                params = {
                    route = {
                        points = {
                            [1] = {
                                type = "Turning Point",
                                action = "Off Road",
                                x = from.x,
                                y = from.z,
                                speed = PILOT_RUN_SPEED,
                                ETA = 0,
                                ETA_locked = false,
                                name = "start",
                                task = { id = "ComboTask", params = { tasks = {} } },
                            },
                            [2] = {
                                type = "Turning Point",
                                action = "Off Road",
                                x = x,
                                y = z,
                                speed = PILOT_RUN_SPEED,
                                ETA = 0,
                                ETA_locked = false,
                                name = "board",
                                task = { id = "ComboTask", params = { tasks = {} } },
                            },
                        },
                    },
                },
            })
        end)
    end

    local function distance2d(ax, az, bx, bz)
        local dx, dz = ax - bx, az - bz
        return math.sqrt(dx * dx + dz * dz)
    end

    -- Nearest AI helicopter of `side` that is on station (landed, or hovering low
    -- enough to hoist) near the pilot.
    local function nearest_ai_rescue_unit(side_const, px, pz)
        local best_unit, best_distance = nil, nil
        local groups = coalition.getGroups(side_const, Group.Category.HELICOPTER) or {}
        for _, group in pairs(groups) do
            if group:isExist() then
                for _, unit in pairs(group:getUnits() or {}) do
                    -- Players are Ops.CSAR's job; only handle AI here.
                    if unit:isExist() and unit:getLife() > 0
                        and unit:getPlayerName() == nil then
                        local point = unit:getPoint()
                        local agl = point.y - land.getHeight({ x = point.x, y = point.z })
                        if not unit:inAir() or agl <= AI_HOVER_AGL then
                            local d = distance2d(px, pz, point.x, point.z)
                            if best_distance == nil or d < best_distance then
                                best_unit, best_distance = unit, d
                            end
                        end
                    end
                end
            end
        end
        return best_unit, best_distance
    end

    local function complete_ai_rescue(tracked, heli_name)
        table.insert(csar_rescued, tracked.id)
        dirty_state = true
        opscsar_log(
            "Pilot " .. tracked.id .. " recovered by AI rescue " .. tostring(heli_name)
        )
        local group = Group.getByName(tracked.group_name)
        if group and group:isExist() then
            group:destroy()
        end
        if tracked.mark_id then
            pcall(function()
                trigger.action.removeMark(tracked.mark_id)
            end)
        end
        tracked.done = true
    end

    local function check_ai_pickups()
        for _, tracked in pairs(ai_pilots) do
            if not tracked.done then
                local group = Group.getByName(tracked.group_name)
                if group == nil or not group:isExist() then
                    tracked.done = true
                else
                    local unit = group:getUnit(1)
                    local point = unit and unit:getPoint() or nil
                    if point then
                        local heli, distance =
                            nearest_ai_rescue_unit(tracked.side, point.x, point.z)
                        if heli and distance and distance <= AI_ZONE_RADIUS then
                            if tracked.since == nil then
                                tracked.since = timer.getTime()
                                local hp = heli:getPoint()
                                route_pilot_to(tracked.group_name, hp.x, hp.z)
                                opscsar_log(
                                    "AI rescue " .. heli:getName()
                                    .. " on station for " .. tostring(tracked.desc)
                                    .. "; pilot moving to board."
                                )
                            end
                            local waited = timer.getTime() - tracked.since
                            if distance <= AI_BOARD_DISTANCE
                                or waited >= AI_PATIENCE_SECONDS then
                                complete_ai_rescue(tracked, heli:getName())
                            end
                        end
                    end
                end
            end
        end
    end

    -- ------------------------------------------------------------------
    -- Spawn every downed pilot down the appropriate path.
    -- ------------------------------------------------------------------
    local spawned_player, spawned_ai = 0, 0
    if type(cfg.downedPilots) == "table" then
        for _, dp in pairs(cfg.downedPilots) do
            local is_red = dp.coalition == "red"
            local side_const = is_red and coalition.side.RED or coalition.side.BLUE
            local x, z = tonumber(dp.x), tonumber(dp.z)
            if dp.id and x and z then
                local sx, sz, flat = landable_spot(x, z)
                if sx == nil then
                    opscsar_warn(
                        "No landable spot for downed pilot " .. tostring(dp.id)
                    )
                elseif dp.aiRescue == "true" then
                    local country_id = tonumber(
                        is_red and cfg.redCountry or cfg.blueCountry
                    )
                    local template = is_red and cfg.redTemplate or cfg.blueTemplate
                    local group_name =
                        spawn_ai_pilot(dp, sx, sz, side_const, country_id, template)
                    if group_name then
                        table.insert(ai_pilots, {
                            id = dp.id,
                            group_name = group_name,
                            side = side_const,
                            desc = dp.description or "Downed pilot",
                            mark_id = mark_pickup_zone(sx, sz, side_const),
                            since = nil,
                            done = false,
                        })
                        spawned_ai = spawned_ai + 1
                    end
                else
                    local instance = is_red and red_csar or blue_csar
                    if instance ~= nil then
                        local country_id = is_red and instance.countryred
                            or instance.countryblue
                        -- _AddCsar rather than SpawnCASEVAC: the public CASEVAC
                        -- wrapper hardcodes frequency 0, which suppresses the ADF
                        -- beacon players home in on. Passing nil generates one. The
                        -- UUID goes in as the unit name so it comes back on the
                        -- downed-pilot record as `originalUnit`.
                        instance:_AddCsar(
                            side_const,
                            country_id,
                            COORDINATE:NewFromVec3({ x = sx, y = 0, z = sz }),
                            dp.aircraft or "Pilot",
                            dp.id,
                            dp.description or "Downed pilot",
                            nil,
                            false,
                            dp.description or "Downed pilot",
                            false
                        )
                        spawned_player = spawned_player + 1
                    end
                end
                if not flat then
                    opscsar_log(
                        "Downed pilot " .. tostring(dp.id)
                        .. " placed on uneven ground; landing may be tricky."
                    )
                end
            end
        end
    end

    if #ai_pilots > 0 then
        timer.scheduleFunction(function()
            local ok, err = pcall(check_ai_pickups)
            if not ok then
                opscsar_warn("AI pickup check failed: " .. tostring(err))
            end
            return timer.getTime() + AI_CHECK_INTERVAL
        end, nil, timer.getTime() + AI_CHECK_INTERVAL)
    end

    opscsar_log(
        "=== CSAR setup complete (" .. spawned_player .. " player-rescue, "
        .. spawned_ai .. " AI-rescue pilots) ==="
    )
end

local ok, err = pcall(opscsar_main)
if not ok then
    env.error("[OpsCSAR] Fatal error: " .. tostring(err))
end
