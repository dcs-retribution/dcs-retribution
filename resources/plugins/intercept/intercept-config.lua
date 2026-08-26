-- Intercept (QRA) — drives AI_A2A_DISPATCHER per coalition from
-- dcsRetribution.Intercept. Aircraft are placed as late-activated template
-- groups by the mission generator; ParkDefender spawns parked instances and
-- recycles them on RTB, consuming a resource permanently on a kill.
--
-- Detection (dr-ktw0): the dispatcher's DETECTION_AREAS is fed from the real
-- EWR/SAM-as-EWR group names published in dcsRetribution.IADS for the
-- coalition (the same source Skynet uses). The previous FilterPrefixes("EWR")
-- matched almost nothing, because DCS EWR group names are suffix-form
-- ("1L13 EWR", "55G6 EWR").
--
-- Detection source: the IADS EWR/SAM-as-EWR network published in
-- dcsRetribution.IADS (the same source Skynet uses). A base only scrambles QRA
-- against raids its radar network actually sees; if a coalition's EWR/SAM-as-EWR
-- network is wiped out, its QRA loses GCI detection (by design — we no longer
-- spawn a per-base backstop EWR, which DCS placed on runways/taxiways at the
-- airbase reference point and broke AI taxi routing).
--
-- GciRadius (groundControlledInterceptionMaxRadius, default 100 NM) caps how
-- far from a base a detected raid can trigger a scramble. The dispatcher only
-- scrambles GCI once AirbaseDistance <= GciRadius. The IADS network provides
-- the real detection range; GciRadius just prevents scrambling against very
-- distant threats heading elsewhere.
--
-- Build timing: the detection SET_GROUP and dispatcher are assembled BUILD_DELAY
-- seconds in to give the mission's groups a frame to register before
-- SET_GROUP:FilterStart() scans them.
--
-- AI_A2A_DISPATCHER:New() calls self:__Start(5) internally — no explicit
-- dispatcher:Start() call is needed or valid (no such method exists).
--
-- Spawn path: NON-VISIBLE / fresh-spawn-on-scramble. We deliberately do NOT
-- call SetSquadronVisible. That keeps Moose's AI_A2A_DISPATCHER:ResourceActivate
-- in its else branch, which spawns a fresh group at scramble time honoring the
-- configured takeoff method (SetDefaultTakeoffInAir below).
--
-- Takeoff method history (all validated in-DCS):
--   1. Visible/ParkDefender pre-park: ParkDefender hardcodes SPAWN.Takeoff.Cold
--      (ignores SetDefaultTakeoff*), so F-16s sat cold and never completed the
--      cold-start→taxi sequence. SetSquadronVisible also clamps ResourceCount to
--      free parking spots and forces Grouping=1. Abandoned.
--   2. Non-visible ParkingHot (warm): F-16s DID scramble warm but still never
--      taxied out of congested ramps (e.g. Tiyas, packed with OCA + ~30 rotary
--      BARCAP — confirmed in-DCS), while
--      the identical code launched fine from uncluttered bases like H3. Ground
--      movement, not takeoff method, was the blocker.
--   3. Runway: SetDefaultTakeoffFromRunway spawned fine at uncluttered H3 (jets on
--      the runway, immediate takeoff) but at saturated Tiyas Moose could not place
--      them on the runway and dumped them into hangars, where they sat. Every
--      ground spawn (cold/hot/runway) fails on a fully-packed ramp.
--   4. In-air (current): the only method that escapes the congested ground. It was
--      blocked by a Moose bug (air-spawn's BASE:CreateEventTakeoff is mis-scheduled
--      → self is a plain table → self:F() crash → defenders never activate). The
--      BASE.CreateEventTakeoff monkeypatch above repairs that without touching the
--      vendored Moose.lua, so in-air now works. Upstream fix filed as MOOSE PR
--      #2595 (Core/Spawn.lua: pass the args as varargs, not a single table);
--      drop the monkeypatch once that lands in the vendored Moose.lua.
--
-- The non-visible path keeps full reserve and real 2-ship grouping (the visible
-- path lost both).
--
-- SetSquadronGci speed args are in km/h (WaypointAir divides by 3.6 to get m/s).
-- 900/1200 km/h ≈ 485/648 kt — reasonable for jet interceptors.

env.info("DCSRetribution|Intercept: configuring QRA dispatchers")

intercept_survivors = intercept_survivors or {}

-- Registry: maps squadronId -> { dispatcher, squadronName }. Populated by the
-- deferred dispatcher build (BUILD_DELAY seconds in), then read by the refresh
-- loop.
local intercept_registry = {}

-- QRA tuning (comms, GCI radius, engagement range) is sourced from the Campaign
-- Doctrine settings and carried on each Intercept record by the mission generator
-- (gciMaxRadiusNm/engagementRangeNm/commsEnabled). The values are global, so each
-- record in a coalition carries the same trio; build_dispatcher reads them from
-- records[1]. add_key_value serializes everything as a string, hence tonumber()
-- for the numerics and a string compare ("false") for the boolean.
local NM = 1852  -- metres per nautical mile
local DETECTION_GROUPING_M = 30000  -- contact-clustering radius for DETECTION_AREAS
local BUILD_DELAY = 5  -- seconds; let mission groups register before SET_GROUP scan

-- ---------------------------------------------------------------------------
-- MOOSE BUG WORKAROUND — air-spawn takeoff event
-- Upstream fix filed as MOOSE PR #2595
-- (https://github.com/FlightControl-Master/MOOSE/pull/2595). REMOVE THIS WHOLE
-- `do … end` BLOCK once that PR is released and pulled into Retribution's
-- vendored resources/plugins/base/Moose.lua — check the SpawnAtAirbase call site
-- there passes the args as varargs (no surrounding braces) before deleting.
-- Core/Spawn.lua SpawnAtAirbase schedules the synthetic takeoff event as:
--   self:ScheduleOnce(5, BASE.CreateEventTakeoff, {GroupSpawned, time, dcsObject})
-- ScheduleOnce forwards its trailing args as VARARGS, so that single table becomes
-- argument #1 — i.e. CreateEventTakeoff runs with the {group,time,dcs} table as
-- `self`. A plain table has no :F(), so the first line (self:F(...)) errors, the
-- takeoff event never fires, and air-spawned AI_A2A_DISPATCHER defenders never
-- activate (observed: zero QRA flew on either side with takeoff=Air). A sibling
-- call site uses SCHEDULER:New(nil, fn, {args}, 5) — which DOES treat the table as
-- the arg list — and is correct; the SpawnAtAirbase one is the regression.
--
-- We don't touch the vendored Moose.lua: override BASE.CreateEventTakeoff to
-- detect the mis-packed call (self is the args table, has no :F) and fire a proper
-- takeoff event; all well-formed calls delegate to the original untouched. Remove
-- once the upstream fix is vendored. Upstream fix = drop the braces at that line so
-- the args pass as varargs.
-- ---------------------------------------------------------------------------
do
    local _orig_create_event_takeoff = BASE.CreateEventTakeoff
    function BASE:CreateEventTakeoff(EventTime, Initiator)
        if type(self) == "table" and type(self.F) ~= "function" then
            -- self is the mis-packed {GroupSpawned, time, dcsObject} table.
            world.onEvent({
                id = world.event.S_EVENT_TAKEOFF,
                time = self[2],
                initiator = self[3],
            })
            return
        end
        return _orig_create_event_takeoff(self, EventTime, Initiator)
    end
end

-- ---------------------------------------------------------------------------
-- Task-type reaction filter (dr-99hm)
-- QRA only scrambles against air-to-ground raids. The enemy flight's Retribution
-- task type is embedded in its DCS group name by namegen.next_aircraft_name as
-- "{target} {flight_type}|{country}|{n}|{variant}|" (game/naming.py). We react
-- only when a detected cluster contains a group whose type is in QRA_REACT_TASKS;
-- CAP/sweep/escort/intercept/SEAD/CAS/DEAD/Air Assault/support are ignored.
-- Non-ATO enemy air
-- (not named by namegen) has no matching suffix and is never reacted to.
-- ---------------------------------------------------------------------------
local QRA_REACT_TASKS = {
    ["Strike"] = true,
    ["BAI"] = true,
    ["OCA/Runway"] = true,
    ["OCA/Aircraft"] = true,
    ["Anti-ship"] = true,
    ["Armed Recon"] = true,
}

local function ends_with(str, suffix)
    return str:sub(-#suffix) == suffix
end

-- Escape Lua pattern magic characters so a literal string can be used where
-- Moose treats it as a pattern (SET_GROUP:FilterPrefixes matches via string.find
-- with pattern semantics). We escape everything EXCEPT "-": Moose's FilterPrefixes
-- already gsubs "-" -> "%-" itself, so escaping it here would double-escape.
local function lua_pattern_escape(s)
    return (s:gsub("[%(%)%.%%%+%*%?%[%]%^%$]", "%%%1"))
end

-- True if the group name's task-type suffix is a react-type. We require the
-- namegen "{target} {flight_type}|..." format and match the first "|"-field:
-- a name with no "|" is not a Retribution ATO flight, so we cannot classify it
-- and never react (this enforces the documented non-ATO limitation and stops a
-- mission-editor/Combined-Arms group coincidentally named e.g. "Eagle Strike"
-- from false-matching). Within the field we suffix-match " " .. task so
-- multi-word target names (e.g. "Al Dhafra Strike") and any multi-word react
-- type both work; the leading space keeps a target name that merely ends in the
-- task word (no separator) from matching.
local function qra_group_reacts(group_name)
    if type(group_name) ~= "string" then return false end
    local field = group_name:match("^([^|]+)|")  -- "{target} {flight_type}" up to the first "|"
    if not field then return false end
    for task, _ in pairs(QRA_REACT_TASKS) do
        if ends_with(field, " " .. task) then
            return true
        end
    end
    return false
end

-- True if any unit in the detected cluster belongs to a react-type group. A
-- cluster reacts as soon as one react-type group is present (escorted strikes
-- still trigger).
local function qra_cluster_has_react(detected_item)
    local set = detected_item and detected_item.Set
    if not set then return false end
    local found = false
    set:ForEachUnit(function(unit)
        if found then return end  -- short-circuit; ForEachUnit has no early break
        local group = unit:GetGroup()
        if group and qra_group_reacts(group:GetName()) then
            found = true
        end
    end)
    return found
end

-- Collect the EWR / SAM-as-EWR group names the IADS generator published for a
-- coalition. SamAsEwr entries already carry the DCS GROUP name, but standalone
-- Ewr entries carry the UNIT name (Skynet convention: dcs_name_for_group
-- returns unit_name for EWR/CC roles). SET_GROUP filters by group name, so we
-- resolve unit names to their parent group via UNIT:FindByName → GetGroup.
local function ewr_group_names(coalition_name)
    local names = {}
    local seen = {}
    local iads = dcsRetribution.IADS and dcsRetribution.IADS[coalition_name]
    if iads then
        for _, role in ipairs({ "Ewr", "SamAsEwr" }) do
            local list = iads[role]
            if list then
                for _, node in pairs(list) do
                    if node.dcsGroupName then
                        local group_name = node.dcsGroupName
                        local grp = GROUP:FindByName(group_name)
                        if not grp then
                            local unit = UNIT:FindByName(group_name)
                            if unit then
                                local parent = unit:GetGroup()
                                if parent then
                                    group_name = parent:GetName()
                                end
                            end
                        end
                        if not seen[group_name] then
                            seen[group_name] = true
                            names[#names + 1] = group_name
                        end
                    end
                end
            end
        end
    end
    return names
end

local function build_dispatcher(coalition_name, records)
    if #records == 0 then return end

    -- Global QRA tuning, identical across this coalition's records (see header).
    local comms_enabled = records[1].commsEnabled ~= "false"
    local scramble_radius_nm = tonumber(records[1].gciMaxRadiusNm) or 100
    local engagement_range_nm = tonumber(records[1].engagementRangeNm) or 60

    -- Assemble the dispatcher once the mission's groups have registered.
    mist.scheduleFunction(function()
        local detection_prefixes = ewr_group_names(coalition_name)

        if #detection_prefixes == 0 then
            env.info("DCSRetribution|Intercept: no detection sources for "
                     ..coalition_name.."; QRA will not scramble.")
            return
        end

        -- Moose SET_GROUP:FilterPrefixes matches names with Lua-pattern semantics
        -- (string.find, only "-" pre-escaped). Retribution IADS group names contain
        -- "(" / ")" (e.g. "0041 | LION (EWR)", "0114 | LORIKEET (S-300)"), which
        -- would be read as pattern captures and never match, leaving the detection
        -- set empty (no QRA scramble ever). Escape the magic chars so each prefix
        -- matches its literal group name.
        local detection_patterns = {}
        for i, name in ipairs(detection_prefixes) do
            detection_patterns[i] = lua_pattern_escape(name)
        end

        local det_set = SET_GROUP:New()
            :FilterCoalitions(string.lower(coalition_name))
            :FilterPrefixes(detection_patterns)
            :FilterStart()

        local detection = DETECTION_AREAS:New(det_set, DETECTION_GROUPING_M)

        local dispatcher = AI_A2A_DISPATCHER:New(detection)
        -- dr-99hm: only scramble against air-to-ground raids. Wrap this
        -- instance's per-cluster evaluation so a detected cluster with no
        -- react-type group is skipped; otherwise delegate to Moose's original.
        -- Per-instance (not class-level) so it applies to this coalition's
        -- dispatcher only. EvaluateGCI returns (DefendersMissing, Friendlies);
        -- nil,nil means "no scramble". EvaluateENGAGE returns Friendlies or nil.
        local orig_evaluate_gci = dispatcher.EvaluateGCI
        function dispatcher:EvaluateGCI(detected_item)
            if not qra_cluster_has_react(detected_item) then
                return nil, nil
            end
            return orig_evaluate_gci(self, detected_item)
        end
        local orig_evaluate_engage = dispatcher.EvaluateENGAGE
        function dispatcher:EvaluateENGAGE(detected_item)
            if not qra_cluster_has_react(detected_item) then
                return nil
            end
            return orig_evaluate_engage(self, detected_item)
        end
        -- Spawn interceptors already airborne near the base. See header for the
        -- full method history: every ground spawn (cold/hot/runway) leaves F-16s
        -- stuck on congested ramps like Tiyas; only in-air escapes it. In-air is
        -- viable here because the BASE.CreateEventTakeoff monkeypatch above fixes
        -- the Moose air-spawn crash that previously killed it. Altitude is metres.
        dispatcher:SetDefaultTakeoffInAir()
        dispatcher:SetDefaultTakeoffInAirAltitude(2000)  -- ~6,500 ft
        dispatcher:SetDefaultLandingAtEngineShutdown()
        dispatcher:SetIntercept(0)
        dispatcher:SetEngageRadius(engagement_range_nm * NM)
        dispatcher:SetTacticalDisplay(false)  -- debug F10 overview; off in normal play
        dispatcher:SetGciRadius(scramble_radius_nm * NM)
        -- Moose's default DisengageRadius is 300 km (~162 NM): once a defender's
        -- DistanceFromHomeBase exceeds it, Moose aborts the intercept mid-transit.
        -- Our GCI radius is configurable up to 400 NM, so leaving the default would
        -- launch a far-edge defender only to have it turn straight around. Size the
        -- disengage radius to the furthest reachable point (scramble trigger + engage
        -- chase) plus a maneuver margin so a valid intercept never self-aborts.
        dispatcher:SetDisengageRadius((scramble_radius_nm + engagement_range_nm + 20) * NM)
        if comms_enabled then
            dispatcher:SetSendMessages(true)
        end

        for _, rec in ipairs(records) do
            -- Moose keys squadrons by name; the squadron display name is not
            -- unique across bases (dr-wz6p), so append a short slice of the
            -- unique squadron id to avoid one base's QRA overwriting another's.
            local sq = rec.squadronName .. " #" .. string.sub(tostring(rec.squadronId), 1, 8)
            dispatcher:SetSquadron(sq, rec.airbaseName, { rec.templatePrefix }, tonumber(rec.resourceCount))
            dispatcher:SetSquadronGci(sq, 900, 1200)
            -- Terrain-relative in-air spawn altitude (~2,500 ft AGL over this
            -- squadron's field). The global SetDefaultTakeoffInAirAltitude above
            -- is absolute MSL, so high-elevation fields spawn low and low fields
            -- spawn high with free energy; per-squadron we offset by the field's
            -- land height. Falls back to the global 2000 m when the lookup misses.
            local base = AIRBASE:FindByName(rec.airbaseName)
            if base then
                local ok_e, elev = pcall(function() return base:GetCoordinate():GetLandHeight() end)
                if ok_e and elev then
                    dispatcher:SetSquadronTakeoffInAirAltitude(sq, elev + 760)
                end
            end
            -- 75% single / 25% pair per scramble. QRA alert launches are mostly
            -- singles; a fixed group of 2 means a reserve of 4 answers only 2 raids,
            -- while mostly-singles lets the same reserve answer ~4. Rolled once per
            -- squadron (record) so each base's launches are independent.
            local grouping = (math.random() < 0.75) and 1 or 2
            dispatcher:SetSquadronGrouping(sq, grouping)
            -- NOTE: deliberately NOT SetSquadronVisible — see header. Visible mode
            -- forces a cold pre-park (F-16 never taxis), clamps reserve to parking
            -- spots, and forces Grouping=1. Non-visible = in-air fresh-spawn on scramble.
            if comms_enabled then
                dispatcher:SetSquadronLanguage(sq, "EN")
            end
            intercept_survivors[rec.squadronId] = tonumber(rec.resourceCount)

            intercept_registry[rec.squadronId] = {
                dispatcher    = dispatcher,
                squadronName  = sq,
            }
        end
    end, {}, timer.getTime() + BUILD_DELAY)
end

-- ---------------------------------------------------------------------------
-- Survivor refresh
-- Formula: survivors(squadron) = parked ResourceCount
--                              + sum of GetSize() for each airborne Defender
--                                whose SquadronName matches.
--
-- GetSquadron throws on unknown name — we pcall it.
-- GetSize() returns nil when the GROUP has no DCS object; treat nil as 0.
-- DefenderTasks is keyed by Defender GROUP object; we iterate pairs() and
-- call GetDefenderTaskSquadronName(Defender) to match the squadron.
-- ---------------------------------------------------------------------------
local REFRESH_INTERVAL = 30  -- seconds between polls

local function refresh_survivors()
    for squadron_id, entry in pairs(intercept_registry) do
        local ok, err = pcall(function()
            local disp = entry.dispatcher
            local sq_name = entry.squadronName

            -- Parked count
            local parked = 0
            local sq_ok, sq_obj = pcall(function()
                return disp:GetSquadron(sq_name)
            end)
            if sq_ok and sq_obj and sq_obj.ResourceCount then
                parked = sq_obj.ResourceCount
            else
                -- GetSquadron threw or ResourceCount nil: keep last known value
                return
            end

            -- Airborne count: sum GetSize() for alive Defender groups in this squadron
            local airborne = 0
            local tasks = disp:GetDefenderTasks()
            for defender, _ in pairs(tasks) do
                local task_sq_name = disp:GetDefenderTaskSquadronName(defender)
                if task_sq_name == sq_name then
                    local sz = defender:GetSize()
                    if sz then
                        airborne = airborne + sz
                    end
                end
            end

            local survivors = math.max(0, parked + airborne)
            intercept_survivors[squadron_id] = survivors
        end)
        if not ok then
            env.info("DCSRetribution|Intercept: survivor refresh error for squadron "
                     ..tostring(squadron_id)..": "..tostring(err))
            -- keep last known value; do not write nil
        end
    end

    -- Self-reschedule (one-shot mist pattern, same as write_state_error_handling)
    mist.scheduleFunction(refresh_survivors, {}, timer.getTime() + REFRESH_INTERVAL)
end

if dcsRetribution.Intercept then
    local blue = dcsRetribution.Intercept.BLUE or {}
    local red = dcsRetribution.Intercept.RED or {}
    build_dispatcher("BLUE", blue)
    build_dispatcher("RED", red)

    -- The registry is populated by the deferred build (BUILD_DELAY in); start the
    -- survivor poll well after that and after the dispatcher FSM auto-start.
    if #blue > 0 or #red > 0 then
        mist.scheduleFunction(refresh_survivors, {}, timer.getTime() + 15)
    end
end

-- Test hook: expose the pure filter helpers for tests/missiongenerator/
-- qra_filter_test.lua. The DCS plugin loader executes this chunk and discards
-- its return value, so this is inert in-mission.
return {
    group_reacts = qra_group_reacts,
    cluster_has_react = qra_cluster_has_react,
    pattern_escape = lua_pattern_escape,
}
