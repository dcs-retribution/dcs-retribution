-- CSAR integration for DCS Retribution.
--
-- Retribution places each downed pilot in the mission as a real ground group
-- carrying DCS's native `EmbarkToTransport` task, and gives every CSAR flight's
-- pickup waypoint a matching `Embarking` task (see csargenerator.py and
-- csarpickup.py). That combination is what performs an AI rescue: stock DCS
-- transport logic walks the pilot to the hovering helicopter and loads them.
-- MOOSE Ops.CSAR cannot do this at all for AI helicopters -- its boarding loop
-- (CSAR:_CheckWoundedGroupStatus, driven by the csarUnits list built in
-- CSAR:_AddMedevacMenuItem) only ever considers units where _unit:IsPlayer() is
-- true.
--
-- This script therefore does two things:
--
--  1. Hands those same pre-placed groups to Ops.CSAR, so a player flying any
--     CSAR-capable helicopter can rescue any downed pilot -- including ones the
--     auto-planner assigned to an AI flight -- with beacons, the F10 menu and
--     MOOSE's own boarding.
--
--  2. Watches for a pilot group disappearing next to a rescue helicopter, which
--     is how a completed native embark presents itself, and reports the rescue
--     back to Retribution via the global `csar_rescued` table that
--     dcs_retribution.lua writes into state.json.
--
-- Assumes MOOSE (Moose.lua) and dcs_retribution.lua have already been loaded.

-- A helicopter within this range of where the pilot was counts as the one that
-- picked them up. Matches the embark zone radius used on the pilot's task.
local PICKUP_RADIUS = 600
-- A helo above this AGL is transiting, not picking anyone up.
local PICKUP_MAX_AGL = 100
local CHECK_INTERVAL = 5

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
    -- Ops.CSAR, for player-flown rescues.
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

    -- Registers an already-placed pilot group with Ops.CSAR. This is the tail of
    -- CSAR:_AddCsar with the spawn removed, so the player experience (ADF beacon,
    -- MAYDAY call, F10 menu, boarding) is identical to a MOOSE-spawned pilot.
    local function register_with_ops_csar(instance, group, uuid, description, typename)
        if instance == nil or group == nil then
            return false
        end
        local ok, err = pcall(function()
            local freq = instance:_GenerateADFFrequency() or 333000
            local beacon_name = uuid .. "-" .. math.random(1, 10000)
            if freq ~= 0 then
                instance:_AddBeaconToGroup(group, freq, beacon_name)
            end
            instance:_AddSpecialOptions(group)
            instance:_CreateDownedPilotTrack(
                group,
                group:GetName(),
                instance.coalition,
                uuid, -- becomes DownedPilot.originalUnit, our id back again
                description,
                typename,
                freq,
                nil,
                false,
                beacon_name
            )
            instance:_InitSARForPilot(group, group:GetName(), freq, false, nil)
        end)
        if not ok then
            opscsar_warn("Could not register pilot with Ops.CSAR: " .. tostring(err))
            return false
        end
        return true
    end

    -- ------------------------------------------------------------------
    -- Rescue detection for the native (AI) embark.
    --
    -- DCS gives no event when troops board a transport; the pilot's group simply
    -- ceases to exist. So remember where each pilot was and whether a rescue
    -- helicopter was on top of them, and treat "group gone while a helo was
    -- right there" as a pickup. Anything else (killed, or still waiting) is left
    -- alone -- Retribution's own post-mission fallback still handles those.
    -- ------------------------------------------------------------------
    local tracked = {}

    local function distance2d(ax, az, bx, bz)
        local dx, dz = ax - bx, az - bz
        return math.sqrt(dx * dx + dz * dz)
    end

    local function rescue_helo_near(side_const, px, pz)
        local groups = coalition.getGroups(side_const, Group.Category.HELICOPTER) or {}
        for _, group in pairs(groups) do
            if group:isExist() then
                for _, unit in pairs(group:getUnits() or {}) do
                    if unit:isExist() and unit:getLife() > 0 then
                        local point = unit:getPoint()
                        local agl =
                            point.y - land.getHeight({ x = point.x, y = point.z })
                        if agl <= PICKUP_MAX_AGL then
                            local d = distance2d(px, pz, point.x, point.z)
                            if d <= PICKUP_RADIUS then
                                return unit
                            end
                        end
                    end
                end
            end
        end
        return nil
    end

    local function check_pickups()
        for _, entry in pairs(tracked) do
            if not entry.done then
                local group = Group.getByName(entry.group_name)
                local alive = group ~= nil and group:isExist()
                    and #(group:getUnits() or {}) > 0
                if alive then
                    local unit = group:getUnit(1)
                    local point = unit and unit:getPoint() or nil
                    if point then
                        entry.last_x, entry.last_z = point.x, point.z
                        local helo =
                            rescue_helo_near(entry.side, point.x, point.z)
                        entry.helo_name = helo and helo:getName() or nil
                    end
                elseif entry.last_x then
                    -- Gone. If a rescue helicopter was on station where the pilot
                    -- was, they embarked.
                    local helo =
                        rescue_helo_near(entry.side, entry.last_x, entry.last_z)
                    local by = helo and helo:getName() or entry.helo_name
                    if by then
                        table.insert(csar_rescued, entry.id)
                        dirty_state = true
                        opscsar_log(
                            "Pilot " .. entry.id .. " embarked on " .. tostring(by)
                        )
                    else
                        opscsar_log(
                            "Pilot " .. entry.id .. " is gone with no rescue "
                            .. "helicopter nearby; not counting a rescue."
                        )
                    end
                    entry.done = true
                else
                    entry.done = true
                end
            end
        end
    end

    -- ------------------------------------------------------------------
    -- Wire up every downed pilot Retribution placed in the mission.
    -- ------------------------------------------------------------------
    local registered, watched = 0, 0
    if type(cfg.downedPilots) == "table" then
        for _, dp in pairs(cfg.downedPilots) do
            local group_name = dp.groupName
            if dp.id and group_name and group_name ~= "" then
                local is_red = dp.coalition == "red"
                local side_const = is_red and coalition.side.RED or coalition.side.BLUE
                local instance = is_red and red_csar or blue_csar

                local moose_group = GROUP:FindByName(group_name)
                if moose_group == nil then
                    opscsar_warn(
                        "Downed pilot group '" .. group_name .. "' not found."
                    )
                else
                    if register_with_ops_csar(
                        instance,
                        moose_group,
                        dp.id,
                        dp.description or "Downed pilot",
                        dp.aircraft or "Pilot"
                    ) then
                        registered = registered + 1
                    end
                    table.insert(tracked, {
                        id = dp.id,
                        group_name = group_name,
                        side = side_const,
                        done = false,
                        last_x = nil,
                        last_z = nil,
                        helo_name = nil,
                    })
                    watched = watched + 1
                end
            end
        end
    end

    if #tracked > 0 then
        timer.scheduleFunction(function()
            local ok, err = pcall(check_pickups)
            if not ok then
                opscsar_warn("CSAR pickup check failed: " .. tostring(err))
            end
            return timer.getTime() + CHECK_INTERVAL
        end, nil, timer.getTime() + CHECK_INTERVAL)
    end

    opscsar_log(
        "=== CSAR setup complete (" .. watched .. " downed pilots, "
        .. registered .. " registered with Ops.CSAR) ==="
    )
end

local ok, err = pcall(opscsar_main)
if not ok then
    env.error("[OpsCSAR] Fatal error: " .. tostring(err))
end
