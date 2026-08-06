-- CSAR integration for DCS Retribution.
--
-- Retribution places each downed pilot in the mission as a real ground group
-- carrying DCS's native `EmbarkToTransport` task, and gives every CSAR flight's
-- pickup waypoint a matching `Embarking` task (see csargenerator.py and
-- csarpickup.py). That combination performs the AI rescue on its own: the
-- helicopter lands, the pilot walks over, DCS loads them and deletes the group.
-- MOOSE Ops.CSAR cannot do this at all for AI helicopters -- its boarding loop
-- (CSAR:_CheckWoundedGroupStatus, driven by the csarUnits list built in
-- CSAR:_AddMedevacMenuItem) only ever considers units where _unit:IsPlayer() is
-- true.
--
-- This script therefore does three things:
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
--  3. Under hover extraction there is no native mechanic at all -- DCS has no
--     hoist -- so the whole pickup is run from here. The rescue flight's pickup
--     waypoint carries a script call into OpsCSAR_BeginHover (see csarpickup.py);
--     that pushes a real hover onto the helicopter, and once it has held it long
--     enough the survivor is deleted, the rescue reported and the flight released
--     to fly home, exactly as if they had been winched aboard.
--
-- Assumes MOOSE (Moose.lua) and dcs_retribution.lua have already been loaded.

-- A helicopter within this range of where the pilot was counts as the one that
-- picked them up. Matches the embark zone radius used on the pilot's task.
local PICKUP_RADIUS = 600
-- A helo above this AGL is transiting, not picking anyone up.
local PICKUP_MAX_AGL = 150
local CHECK_INTERVAL = 5
-- How long after a rescue helicopter was last seen in the embark zone a vanishing
-- pilot still counts as having boarded it. Generous, because the only other way
-- for a tracked survivor to disappear is being killed, and the post-mission
-- fallback in Retribution re-checks the outcome anyway.
local RESCUE_ATTRIBUTION_WINDOW = 120
-- How long a rescue helicopter can be in the embark zone with the survivor still
-- reporting as present before that is worth complaining about. Comfortably longer
-- than the walk to the helicopter and the Embarking task's own hold.
local STILL_HERE_WARN_AFTER = 420

-- The AI embark, watched from the helicopter's side (landing mode only).
--
-- Once troops are loaded they stop being a unit anyone can query, so every test
-- that looks at the survivor is racing their removal. The helicopter, though,
-- announces both ends of the pickup: DCS fires S_EVENT_LAND when it sets down on
-- the unprepared LZ and S_EVENT_TAKEOFF when it lifts again, both with a nil
-- `place` (an airfield or FARP fills that in, which is how an RTB landing is told
-- apart). A rescue flight that put down inside a survivor's embark zone, stayed
-- long enough for them to walk over, and then left, has done the pickup.
--
-- Below this much time on the ground it cannot have loaded anybody -- the walk
-- from the survivor to the touchdown point is LANDING_ZONE_OFFSET on foot.
local EMBARK_MIN_GROUND_TIME = 20

-- Positive detection that the survivor has boarded.
--
-- DCS fires no embark event -- there is nothing in the event enum for troop
-- transport, and a full AI pickup (touchdown, load, RTB, shutdown) produces no
-- event attributable to the survivor at all. But it does keep reporting a
-- position for troops it has loaded, and that position is the transport's.
--
-- A survivor never goes anywhere under their own power except the run to a
-- helicopter that has landed for them, and that run stays inside the embark zone
-- by construction (LANDING_ZONE_OFFSET is half its radius). So a reported
-- position outside that zone is not the pilot moving -- it is the pilot being
-- flown away, which is the pickup. No altitude, no terrain, nothing to be fooled
-- by. The zone radius itself is the threshold; see embark_zone_radius.

-- Hover extraction (the csar_hover_extraction setting). DCS's embark tasks only
-- fire once the transport is on the ground with weight off wheels, so when the
-- player would rather not have the AI hunting for a landable patch of terrain we
-- fake the recovery instead: the flight is held in a hover over the survivor and
-- the pickup is simulated when the hold is done.
--
-- Defaults only; the real values are injected from csarpickup.py.
local HOVER_DURATION_SECONDS = 30
local HOVER_ALTITUDE = 30

-- Signal smoke for AI rescues. The survivor pops smoke in their own coalition's
-- colour once an AI rescue helicopter is inside their embark zone. Players get
-- Ops.CSAR's "Request Smoke" F10 menu item instead, so they choose when to expose
-- the survivor's position. DCS smoke burns for about five minutes, so re-pop on
-- that cadence while the helicopter is still around.
local SMOKE_MAX_AGL = 600
local SMOKE_REPOP_SECONDS = 300

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
    -- The mission-wide default. The pickup style is decided per pilot though (see
    -- entry.hover), because a survivor in the water has to be hoisted whatever
    -- this says.
    local hover_extraction = cfg.hoverExtraction == "true"
    local embark_zone_radius = tonumber(cfg.embarkZoneRadius) or PICKUP_RADIUS
    local hover_duration = tonumber(cfg.hoverDurationSeconds) or HOVER_DURATION_SECONDS
    local hover_altitude = tonumber(cfg.hoverAltitudeMeters) or HOVER_ALTITUDE

    opscsar_log(
        "=== CSAR starting (default AI pickup: "
        .. (hover_extraction and "scripted hover extraction" or "DCS embark on landing")
        .. ") ==="
    )

    -- Moose.lua always defines the AICSAR *class*, so testing for the global
    -- alone warns on every single mission. An instance assigned over the global
    -- fills in lid/alias, which the class table leaves empty.
    if AICSAR ~= nil and AICSAR.lid ~= nil and AICSAR.lid ~= "" then
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

    -- Declared up here so the Ops.CSAR callbacks below can resolve a survivor
    -- back to their Retribution id. Populated further down.
    local tracked = {}
    local tracked_by_id = {}

    local function tracked_by_group(group_name)
        for _, entry in pairs(tracked) do
            if entry.group_name == group_name then
                return entry
            end
        end
        return nil
    end

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
        -- Consider *every* friendly helicopter, not just ones named after MOOSE's
        -- demo templates. Ops.CSAR defaults to useprefix=true with
        -- csarPrefix={"helicargo","MEDEVAC"} and builds allheligroupset from that,
        -- which in turn is the only source of csarUnits -- the list that drives
        -- both the F10 menu and MOOSE's boarding. Retribution names its flights
        -- after the mission, so with the default no player helicopter is ever a
        -- rescue helicopter: no menu, no pickup, silently.
        my.useprefix = false
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
            -- Resolve against our own list rather than self.downedPilots, which
            -- is a race: _PickupUnit destroys the survivor's group and Boarded is
            -- raised 5s later, while onbeforeStatus -> _CheckDownedPilotTable
            -- drops any entry whose group is gone. Usually the id is still there
            -- when we get here; if a Status cycle lands in that 5s window it is
            -- not, and the rescue goes unrecorded. Our list has no such window.
            local entry = tracked_by_group(Woundedgroupname)
            if entry == nil or not Heliname then
                return
            end
            -- Theirs to report now. Ops.CSAR credits the rescue on delivery, not
            -- on pickup, which is the behaviour we want for a crewed rescue.
            entry.moose_boarded = true
            entry.done = true
            onboard[Heliname] = onboard[Heliname] or {}
            table.insert(onboard[Heliname], entry.id)
            opscsar_log(
                "Pilot " .. entry.id .. " boarded " .. Heliname
                .. "; rescue will be reported on delivery."
            )
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
    local function distance2d(ax, az, bx, bz)
        local dx, dz = ax - bx, az - bz
        return math.sqrt(dx * dx + dz * dz)
    end

    -- Whether anyone is flying this group. A Retribution flight is a single DCS
    -- group holding the client slots *and* their AI wingmen, so the question has
    -- to be asked of the group: testing units individually leaves the wingmen
    -- looking like an AI rescue flight, and they are close enough to the survivor
    -- to satisfy every proximity check we make.
    local function group_has_player(group)
        for _, unit in pairs(group:getUnits() or {}) do
            if unit:isExist() and unit:getPlayerName() ~= nil then
                return true
            end
        end
        return false
    end

    -- Nearest live helicopter of `side` within `radius` of the point and no higher
    -- than `max_agl`. `ai_only` skips player-crewed flights, which Ops.CSAR owns.
    local function helo_near(side_const, px, pz, radius, max_agl, ai_only)
        local groups = coalition.getGroups(side_const, Group.Category.HELICOPTER) or {}
        for _, group in pairs(groups) do
            if group:isExist() and not (ai_only and group_has_player(group)) then
                for _, unit in pairs(group:getUnits() or {}) do
                    if unit:isExist() and unit:getLife() > 0 then
                        local point = unit:getPoint()
                        local agl =
                            point.y - land.getHeight({ x = point.x, y = point.z })
                        if agl <= max_agl then
                            local d = distance2d(px, pz, point.x, point.z)
                            if d <= radius then
                                return unit
                            end
                        end
                    end
                end
            end
        end
        return nil
    end

    -- AI only, deliberately. Everything this drives -- the vanish attribution and
    -- carried_out_of_zone -- credits a rescue the moment the survivor leaves the
    -- map, which is the right moment for an AI pickup but the *wrong* one for a
    -- player: Ops.CSAR credits a crewed rescue on delivery to a MASH or airfield,
    -- and MOOSE destroys the survivor at pickup, so counting the vanish would
    -- report the rescue while the pilot is still in the back of the helicopter.
    local function rescue_helo_near(side_const, px, pz)
        return helo_near(side_const, px, pz, PICKUP_RADIUS, PICKUP_MAX_AGL, true)
    end

    -- The helicopter flying the survivor away, if their reported position has left
    -- the embark zone. Attribution is the rescue helicopter last seen in the zone:
    -- it is the one that landed for them, and nothing else could have moved them.
    local function carried_out_of_zone(entry, point)
        if entry.origin_x == nil or entry.helo_name == nil then
            return nil
        end
        local travelled =
            distance2d(point.x, point.z, entry.origin_x, entry.origin_z)
        if travelled <= embark_zone_radius then
            return nil
        end
        return entry.helo_name
    end

    -- Pops signal smoke at the survivor while an *AI* rescue helicopter is inside
    -- their embark zone. Blue coalition pilots throw blue smoke, red throw red.
    --
    -- AI only, deliberately: a human crew already has Ops.CSAR's "Request Smoke"
    -- F10 menu item and can call for it when they want it. Popping automatically
    -- for players would both pre-empt that choice and give away the survivor's
    -- position for the whole burn time whether they wanted it or not.
    local function maybe_pop_smoke(entry, px, pz)
        local helo = helo_near(
            entry.side, px, pz, embark_zone_radius, SMOKE_MAX_AGL, true
        )
        if helo == nil then
            return
        end
        local now = timer.getTime()
        if entry.smoke_until ~= nil and now < entry.smoke_until then
            return
        end
        entry.smoke_until = now + SMOKE_REPOP_SECONDS
        local colour = entry.side == coalition.side.RED
            and trigger.smokeColor.Red
            or trigger.smokeColor.Blue
        pcall(function()
            -- Offset slightly so the plume doesn't sit inside the pilot model.
            trigger.action.smoke({ x = px + 6, y = land.getHeight({ x = px + 6, y = pz }), z = pz }, colour)
        end)
        opscsar_log(
            "Pilot " .. entry.id .. " popped smoke for " .. tostring(helo:getName())
        )
    end

    -- Single place a rescue is reported back to Retribution.
    local function record_rescue(entry, by, how)
        if entry.done then
            return
        end
        entry.done = true
        table.insert(csar_rescued, entry.id)
        dirty_state = true
        opscsar_log(
            "Pilot " .. entry.id .. " " .. how .. " " .. tostring(by or "a helicopter")
        )
    end

    -- ------------------------------------------------------------------
    -- Scripted hoist pickup.
    --
    -- The flight tells us when it is on station rather than us guessing from
    -- proximity: its pickup waypoint runs OpsCSAR_BeginHover (csarpickup.py). We
    -- then hold it ourselves, because the hold cannot be built into the .miz --
    -- the DCS Orbit task takes an MSL altitude and Retribution has no terrain
    -- elevation when it generates the mission. land.getHeight does, here.
    --
    -- AI only: a player over the survivor is Ops.CSAR's to handle, and lifting the
    -- pilot out from under it would break MOOSE's own boarding. DCS doesn't run
    -- waypoint tasks for client aircraft, so that falls out for free.
    -- ------------------------------------------------------------------

    local function hover_controller(entry)
        if entry.hover_group == nil then
            return nil
        end
        local group = Group.getByName(entry.hover_group)
        if group == nil or not group:isExist() then
            return nil
        end
        return group:getController()
    end

    -- Gives the flight its route back, so it flies on to the arrival waypoint.
    -- popTask is what makes this safe: unlike setTask it leaves the underlying
    -- route mission in place, so the helicopter simply resumes it.
    local function release_hover(entry, why)
        if entry.hover_group == nil then
            return
        end
        local name = entry.hover_group
        local controller = hover_controller(entry)
        entry.hover_group = nil
        entry.hover_since = nil
        if controller == nil then
            return
        end
        local ok, err = pcall(function()
            controller:popTask()
        end)
        if ok then
            opscsar_log(name .. " released from the hover (" .. why .. ")")
        else
            opscsar_warn("Could not release " .. name .. ": " .. tostring(err))
        end
    end

    local function begin_hover(entry, helo_group_name)
        local group = Group.getByName(helo_group_name)
        if group == nil or not group:isExist() then
            opscsar_warn("Rescue flight '" .. helo_group_name .. "' not found.")
            return
        end
        local controller = group:getController()
        if controller == nil then
            return
        end
        local px, pz, py = entry.last_x, entry.last_z, entry.last_y
        if px == nil then
            local pilot = Group.getByName(entry.group_name)
            local unit = pilot and pilot:isExist() and pilot:getUnit(1) or nil
            local point = unit and unit:getPoint() or nil
            if point == nil then
                opscsar_warn(
                    "No position for pilot " .. tostring(entry.id)
                    .. "; cannot set up the hover."
                )
                return
            end
            px, pz, py = point.x, point.z, point.y
            entry.last_x, entry.last_z, entry.last_y = px, pz, py
        end

        -- Hold this far above whatever the survivor is lying on. Their own
        -- reported altitude is the reference rather than land.getHeight, which
        -- reads the sea *bottom* over water (the same DCS quirk the
        -- switch_baro_fix setting exists for) and would sink the hover.
        local surface = py or land.getHeight({ x = px, y = pz })

        local ok, err = pcall(function()
            controller:pushTask({
                id = "Orbit",
                params = {
                    pattern = "Circle",
                    point = { x = px, y = pz },
                    -- A circle flown at zero speed is a stationary hover.
                    speed = 0,
                    -- MSL, which is the only reason this has to happen at
                    -- runtime rather than in the .miz.
                    altitude = surface + hover_altitude,
                },
            })
        end)
        if not ok then
            opscsar_warn("Could not hold " .. helo_group_name .. ": " .. tostring(err))
            return
        end

        entry.hover_group = helo_group_name
        entry.hover_since = timer.getTime()
        opscsar_log(
            "AI rescue " .. helo_group_name .. " holding hover over "
            .. tostring(entry.id) .. "; hoist in " .. hover_duration .. "s."
        )
    end

    -- Called from the rescue flight's pickup waypoint. Global on purpose: this is
    -- the entry point csarpickup.py writes into the mission.
    function OpsCSAR_BeginHover(helo_group_name, uuid)
        local entry = tracked_by_id[uuid]
        if entry ~= nil and not entry.hover then
            -- The waypoint only carries this call in hover mode, so the two
            -- disagreeing means the .miz and the injected data are out of step.
            opscsar_warn(
                "Hover requested for " .. tostring(uuid)
                .. ", who is set up for a landing pickup; ignoring."
            )
            return
        end
        if entry == nil then
            opscsar_warn("Hover requested for unknown pilot " .. tostring(uuid))
            return
        end
        if entry.done or entry.hover_group ~= nil then
            return
        end
        local ok, err = pcall(begin_hover, entry, helo_group_name)
        if not ok then
            opscsar_warn("Hover setup failed: " .. tostring(err))
        end
    end

    -- Completes the hoist once the flight has held its hover long enough: the
    -- survivor is removed by hand (nothing in DCS loads them in this mode) and the
    -- flight is sent on its way.
    local function service_hover(entry)
        if entry.hover_since == nil then
            return
        end
        local held = timer.getTime() - entry.hover_since
        if hover_controller(entry) == nil then
            -- Flight shot down or despawned mid-hoist.
            entry.hover_group = nil
            entry.hover_since = nil
            return
        end
        if held < hover_duration then
            return
        end

        local by = entry.hover_group
        local group = Group.getByName(entry.group_name)
        if group and group:isExist() then
            group:destroy()
        end
        -- Stop Ops.CSAR beaconing and calling MAYDAY for a pilot who is aboard.
        if entry.instance then
            pcall(function()
                entry.instance:_RemoveNameFromDownedPilots(entry.group_name, true)
            end)
        end
        record_rescue(entry, by, "hoisted by")
        release_hover(entry, "hoist complete")
    end

    -- The survivor, if they are still standing in the world; nil once they are not.
    --
    -- This asks DCS's unit registry by name rather than walking the group. Neither
    -- the group nor the unit *handles* it hands back are a liveness test: DCS keeps
    -- both alive while the occupants are aboard a transport, ready to be
    -- disembarked, so a group-based check never sees the pickup even though the
    -- pilot has visibly gone from the map. Unit.getByName is resolved against the
    -- world every time it is called, and returns nil once the unit is gone.
    local function survivor_in_world(entry)
        if entry.unit_name and entry.unit_name ~= "" then
            local unit = Unit.getByName(entry.unit_name)
            if unit == nil or not unit:isExist() or unit:getLife() <= 0 then
                return nil
            end
            return unit
        end
        -- No unit name injected (older save); fall back to the group.
        local group = Group.getByName(entry.group_name)
        if group == nil or not group:isExist() then
            return nil
        end
        for _, unit in pairs(group:getUnits() or {}) do
            if unit ~= nil and unit:isExist() and unit:getLife() > 0 then
                return unit
            end
        end
        return nil
    end

    -- ------------------------------------------------------------------
    -- Embark detection from the helicopter's events (AI, landing mode).
    -- ------------------------------------------------------------------

    local function is_ai_helicopter(unit)
        local ok, result = pcall(function()
            if unit == nil or not unit:isExist() then
                return false
            end
            local group = unit:getGroup()
            if group == nil or group:getCategory() ~= Group.Category.HELICOPTER then
                return false
            end
            -- Crewed flights are Ops.CSAR's to handle; it reports their pickups
            -- itself, on delivery. Asked of the whole group so an AI wingman in a
            -- player's flight doesn't land us in the AI path.
            return not group_has_player(group)
        end)
        return ok and result == true
    end

    -- The survivor whose embark zone this point is inside, if any. Hover pickups
    -- are excluded: nothing lands for them, so a helicopter setting down nearby is
    -- somebody else's business.
    local function survivor_awaiting_pickup_at(point, side_const)
        for _, entry in pairs(tracked) do
            local px = entry.origin_x or entry.spawn_x
            local pz = entry.origin_z or entry.spawn_z
            if not entry.done and not entry.hover
                and entry.side == side_const and px ~= nil then
                if distance2d(point.x, point.z, px, pz) <= embark_zone_radius then
                    return entry
                end
            end
        end
        return nil
    end

    local function on_lz_landing(unit)
        local point = unit:getPoint()
        local entry = survivor_awaiting_pickup_at(point, unit:getCoalition())
        if entry == nil then
            return
        end
        entry.embark_helo = unit:getName()
        entry.embark_landed_at = timer.getTime()
        opscsar_log(
            entry.embark_helo .. " has landed to collect " .. tostring(entry.id)
        )
    end

    local function on_lz_takeoff(unit)
        local name = unit:getName()
        for _, entry in pairs(tracked) do
            if not entry.done and entry.embark_helo == name then
                local on_ground = timer.getTime() - (entry.embark_landed_at or 0)
                entry.embark_helo = nil
                if on_ground >= EMBARK_MIN_GROUND_TIME then
                    opscsar_log(
                        name .. " lifted from the pickup after "
                        .. math.floor(on_ground) .. "s on the ground."
                    )
                    record_rescue(entry, name, "embarked on")
                else
                    opscsar_log(
                        name .. " left the pickup for " .. tostring(entry.id)
                        .. " after only " .. math.floor(on_ground)
                        .. "s; too brief to have loaded anyone."
                    )
                end
                return
            end
        end
    end

    local embark_events = {}
    function embark_events:onEvent(event)
        -- Never let a handler error take the whole event system down.
        pcall(function()
            if event == nil or event.initiator == nil then
                return
            end
            -- A place means an airfield, FARP or ship: that is an RTB, not a
            -- pickup. The LZ is bare terrain, so DCS leaves it nil.
            if event.place ~= nil then
                return
            end
            if event.id == world.event.S_EVENT_LAND then
                if is_ai_helicopter(event.initiator) then
                    on_lz_landing(event.initiator)
                end
            elseif event.id == world.event.S_EVENT_TAKEOFF then
                if is_ai_helicopter(event.initiator) then
                    on_lz_takeoff(event.initiator)
                end
            end
        end)
    end

    local function check_pickups()
        for _, entry in pairs(tracked) do
            if entry.done then
                -- Whatever became of the pilot, a flight left in its hover would
                -- never come home. Always give the route back.
                release_hover(entry, "pilot no longer tracked")
            else
                local unit = survivor_in_world(entry)
                if unit ~= nil then
                    local ok, point = pcall(function()
                        return unit:getPoint()
                    end)
                    if ok and point then
                        entry.last_x, entry.last_z = point.x, point.z
                        -- Their own altitude, i.e. the surface they are on --
                        -- ground, or the sea. See begin_hover.
                        entry.last_y = point.y
                        -- Where they came down. They stay put until a helicopter
                        -- lands for them, so this is the reference for "moved".
                        if entry.origin_x == nil then
                            entry.origin_x, entry.origin_z = point.x, point.z
                        end
                        local carrier = carried_out_of_zone(entry, point)
                        if carrier then
                            -- Being flown out: the pickup already happened,
                            -- whatever the survivor's unit handle still claims.
                            record_rescue(entry, carrier, "embarked on")
                        else
                            -- Remember the last rescue helicopter seen in the
                            -- embark zone, with a timestamp. Attribution can't be
                            -- done at vanish time alone: DCS removes the survivor
                            -- the instant they board and the helicopter is already
                            -- climbing away by the next poll, so a "is one here
                            -- right now?" test races the takeoff and loses it.
                            local helo =
                                rescue_helo_near(entry.side, point.x, point.z)
                            if helo then
                                entry.helo_name = helo:getName()
                                entry.helo_seen = timer.getTime()
                                entry.helo_first_seen =
                                    entry.helo_first_seen or entry.helo_seen
                            end
                            maybe_pop_smoke(entry, point.x, point.z)
                        end
                    end
                    if not entry.done then
                        -- A survivor still reporting as present long after a
                        -- rescue helicopter turned up, without ever having left
                        -- the zone, means neither signal is working. Said once, so
                        -- a mission that reports no rescue says why rather than
                        -- just falling silent.
                        if entry.helo_first_seen ~= nil and not entry.stuck_logged
                            and (timer.getTime() - entry.helo_first_seen)
                                > STILL_HERE_WARN_AFTER
                        then
                            entry.stuck_logged = true
                            opscsar_warn(
                                "Pilot " .. entry.id .. " still reports as present "
                                .. STILL_HERE_WARN_AFTER .. "s after "
                                .. tostring(entry.helo_name) .. " reached the "
                                .. "embark zone, and has never moved out of it. "
                                .. "If they have gone from the map, the pickup "
                                .. "will not be reported."
                            )
                        end
                        -- Last, because completing the hoist destroys the survivor
                        -- and everything above wants them still in the world.
                        service_hover(entry)
                    end
                elseif entry.last_x then
                    -- Gone from the map. That is the moment a rescue registers, in
                    -- both modes: DCS deletes the survivor as it loads them and
                    -- fires no embark event, so this is the only signal there is.
                    -- Count it if a rescue helicopter was in the embark zone
                    -- recently enough to have loaded them.
                    local recent = entry.helo_seen ~= nil
                        and (timer.getTime() - entry.helo_seen)
                            <= RESCUE_ATTRIBUTION_WINDOW
                    if recent then
                        record_rescue(entry, entry.helo_name, "embarked on")
                    elseif entry.moose_boarded then
                        opscsar_log(
                            "Pilot " .. entry.id .. " is aboard a player's "
                            .. "helicopter; Ops.CSAR reports on delivery."
                        )
                    else
                        opscsar_log(
                            "Pilot " .. entry.id .. " is gone but no AI rescue "
                            .. "helicopter was in the embark zone within "
                            .. RESCUE_ATTRIBUTION_WINDOW .. "s; not counting a "
                            .. "rescue. (A player pickup is reported by Ops.CSAR "
                            .. "on delivery instead.)"
                        )
                    end
                    entry.done = true
                else
                    -- Never seen alive at all, so there is nothing to attribute.
                    -- Logged rather than dropped silently: it means the survivor
                    -- was missing on the very first poll, which points at the
                    -- placement rather than at the rescue.
                    opscsar_warn(
                        "Pilot " .. entry.id .. " (unit '"
                        .. tostring(entry.unit_name) .. "') was never in the world; "
                        .. "no longer tracking them."
                    )
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
                    local entry = {
                        id = dp.id,
                        group_name = group_name,
                        unit_name = dp.unitName,
                        side = side_const,
                        -- Per pilot: the setting, or forced because they are in
                        -- the water and nothing can land beside them.
                        hover = dp.hoverExtraction == "true",
                        -- Kept so a scripted hoist can tell Ops.CSAR to stop
                        -- tracking a pilot who is aboard a helicopter.
                        instance = instance,
                        done = false,
                        -- Where Retribution placed them, as a fallback reference
                        -- for the embark zone before the first poll has run.
                        spawn_x = tonumber(dp.x),
                        spawn_z = tonumber(dp.z),
                        last_x = nil,
                        last_z = nil,
                        last_y = nil,
                        origin_x = nil,
                        origin_z = nil,
                        embark_helo = nil,
                        embark_landed_at = nil,
                        helo_name = nil,
                        helo_seen = nil,
                        helo_first_seen = nil,
                        stuck_logged = false,
                        moose_boarded = false,
                        hover_group = nil,
                        hover_since = nil,
                        smoke_until = nil,
                    }
                    table.insert(tracked, entry)
                    tracked_by_id[dp.id] = entry
                    watched = watched + 1
                end
            end
        end
    end

    local landing_pickups = 0
    for _, entry in pairs(tracked) do
        if not entry.hover then
            landing_pickups = landing_pickups + 1
        end
    end
    if landing_pickups > 0 then
        -- Only needed for pilots being collected by a landing: for a hover pickup
        -- OpsCSAR_BeginHover already knows exactly when it happened.
        world.addEventHandler(embark_events)
        opscsar_log(
            "Watching for AI pickups on the LZ landing/takeoff events ("
            .. landing_pickups .. " of " .. #tracked .. " pilots)."
        )
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
