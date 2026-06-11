-- ============================================================================
-- REACTIVE SCRAMBLE v2.3  (Retribution GCI Scramble Plugin)
-- Bundled automatically into every Retribution-generated .miz that has a
-- non-empty RED untasked-aircraft scramble pool.
-- ============================================================================
--
-- Retribution spawns each RED squadron's leftover ("untasked") aircraft cold on
-- the ramp as UNCONTROLLED groups — parked, engines off, no route. The mission
-- generator records the air-to-air-capable ones in dcsRetribution.scramble_pool.
--
-- This script holds those groups dormant until a Blue aircraft penetrates RED
-- airspace (the dcsRetribution.scramble_border polygon), then wakes the nearest
-- available one (StartUncontrolled) and tasks it to intercept with a MOOSE-built
-- route plus attack tasking.
-- When no border polygon is supplied it falls back to the legacy behaviour:
-- a Blue aircraft detected by the RED radar network within CFG_engageRadius.
--
-- Cold-ramp behaviour is intentional: an idle group does a full cold start,
-- taxis, takes off, and hunts. Nothing flies until a threat appears.
--
-- ── API NOTES ───────────────────────────────────────────────────────────────
--  GROUP:StartUncontrolled() — issues the {id='Start'} command to a parked
--                              uncontrolled group (cold start + taxi + takeoff)
--  GROUP:Route()             — applies a MOOSE-built waypoint route to the group
--  TaskAttackUnit            — MOOSE attack task applied at the intercept point
-- ============================================================================

local CFG_scanInterval   = 15     -- seconds between threat scans
local CFG_engageRadius   = 95000  -- metres (~51 nm); radar-range detection fallback
local CFG_interceptRange = 185000 -- metres (~100 nm); how far a scrambled QRA pursues
local CFG_responseRadius = 138900 -- metres (~75 nm); max distance from threat to launch
local CFG_interceptAlt   = 7000   -- metres (~23000 ft) intercept routing altitude
local CFG_interceptSpeed = 900    -- km/h transit speed for MOOSE route building
local CFG_reengageDelay  = 180    -- seconds before a busy group re-qualifies
local CFG_spawnDelay     = 5.0    -- seconds after Start before tasking the intercept
local CFG_vectorRefresh  = 45     -- seconds between re-vectors for an active intercept
local CFG_debug          = true   -- periodic status line in dcs.log (radars/border)

-- ── Retribution plugin config override ────────────────────────────────────
-- If a dcsRetribution.plugins.scramble block exists, apply it on the next tick
-- after mission-start data triggers have fired.
-- CFG_scanInterval is intentionally excluded — the SCHEDULER interval is
-- captured at creation time and cannot be changed after the fact.
timer.scheduleFunction(function()
    if not (dcsRetribution and dcsRetribution.plugins and dcsRetribution.plugins.scramble) then return end
    local c = dcsRetribution.plugins.scramble
    if c.engageRadius   ~= nil then CFG_engageRadius   = c.engageRadius * 1852 end  -- NM → metres
    if c.interceptRange ~= nil then CFG_interceptRange = c.interceptRange * 1852 end -- NM → metres
    if c.responseRadius ~= nil then
        CFG_responseRadius = c.responseRadius * 1852
    elseif c.interceptRange ~= nil then
        CFG_responseRadius = CFG_interceptRange
    end
    if c.reengageDelay  ~= nil then CFG_reengageDelay  = c.reengageDelay end
end, nil, timer.getTime() + 0)

local _groups = {}            -- name -> record
local _border = nil           -- list of { x=, z= } points (RED airspace polygon) or nil
local _borderZone = nil       -- MOOSE polygon zone built from _border
local _supportGroups = {}     -- blue support groups that should not trigger QRA
local _targetAssignments = {} -- threat group name -> interceptor group name

-- ── UTILITIES ────────────────────────────────────────────────────────────────

local function log(msg) BASE:E("=== SCRAMBLE: " .. tostring(msg)) end

local function dist3D(p1, p2)
    local dx, dy, dz = p1.x-p2.x, (p1.y or 0)-(p2.y or 0), p1.z-p2.z
    return math.sqrt(dx*dx + dy*dy + dz*dz)
end

local function addSupportGroup(name)
    if name and name ~= "" then
        _supportGroups[name] = true
    end
end

local function indexSupportGroups()
    if not dcsRetribution then return end

    for _, jtac in ipairs(dcsRetribution.JTACs or {}) do
        addSupportGroup(jtac.dcsGroupName)
    end
    for _, awacs in ipairs(dcsRetribution.AWACs or {}) do
        addSupportGroup(awacs.dcsGroupName)
    end
    for _, tanker in ipairs(dcsRetribution.Tankers or {}) do
        addSupportGroup(tanker.dcsGroupName)
    end
end

local function clearAssignment(rec, reason)
    if not rec then return end
    if reason and rec.targetName then
        log(reason .. ": " .. rec.name .. " from " .. rec.targetName)
    end
    if rec.targetName then
        _targetAssignments[rec.targetName] = nil
        rec.targetName = nil
    end
    rec.busy = false
end

-- A Blue contact is a threat once it crosses into RED airspace. Border crossing
-- is the primary trigger; raw radar range is the fallback when no border exists.
local function threatActive(pos, radarPts)
    if _borderZone then
        return _borderZone:IsVec3InZone(pos)
    end
    for _, rp in ipairs(radarPts) do
        if dist3D(pos, rp) <= CFG_engageRadius then return true end
    end
    return false
end

-- ── TASK APPLICATION ─────────────────────────────────────────────────────────

local function taskIntercept(rec)
    local mg = GROUP:FindByName(rec.name)
    if not mg or not mg:IsAlive() then return end
    rec.group = mg
    rec.lastVectorTime = timer.getTime()
    mg:OptionROEWeaponFree()
    mg:OptionROTEvadeFire()
    mg:OptionKeepWeaponsOnThreat()

    local targetGroup = rec.targetName and Group.getByName(rec.targetName) or nil
    local targetUnits = targetGroup and targetGroup:getUnits() or nil
    local targetUnit = targetUnits and targetUnits[1] or nil
    if not targetUnit or not targetUnit:isExist() then
        log("ERROR: no live target unit for " .. rec.name)
        return
    end

    local defenderCoord = mg:GetCoordinate()
    defenderCoord:SetAltitude(CFG_interceptAlt)
    local targetCoord = COORDINATE:NewFromVec3(targetUnit:getPoint())
    targetCoord:SetAltitude(CFG_interceptAlt)

    local attackTasks = {}
    for _, dcsUnit in ipairs(targetUnits or {}) do
        if dcsUnit and dcsUnit:isExist() then
            local mooseUnit = UNIT:FindByName(dcsUnit:getName())
            if mooseUnit and mooseUnit:IsAlive() and mooseUnit:IsAir() then
                attackTasks[#attackTasks + 1] = mg:TaskAttackUnit(mooseUnit)
            end
        end
    end
    if #attackTasks == 0 then
        log("ERROR: no valid attack tasks for " .. rec.name .. " -> " .. rec.targetName)
        return
    end

    local targetDistance = defenderCoord:Get2DDistance(targetCoord)
    local angle = defenderCoord:GetAngleDegrees(defenderCoord:GetDirectionVec3(targetCoord))
    local climbDistance = math.min(25000, math.max(8000, targetDistance * 0.15))
    local commitDistance = math.min(CFG_interceptRange, math.max(25000, targetDistance * 0.7))
    if commitDistance >= targetDistance then
        commitDistance = math.max(10000, targetDistance * 0.8)
    end

    local climbCoord = defenderCoord:Translate(climbDistance, angle, true)
    climbCoord:SetAltitude(CFG_interceptAlt)
    local commitCoord = defenderCoord:Translate(commitDistance, angle, true)
    commitCoord:SetAltitude(CFG_interceptAlt)

    local route = {
        defenderCoord:WaypointAirTurningPoint("BARO", CFG_interceptSpeed, {}, "Current"),
        climbCoord:WaypointAirTurningPoint("BARO", CFG_interceptSpeed, {}, "Climb"),
        commitCoord:WaypointAirTurningPoint("BARO", CFG_interceptSpeed, { mg:TaskCombo(attackTasks) }, "Commit"),
    }
    mg:Route(route, 0.1)
end

-- Wake a dormant uncontrolled group and send it to intercept.
--
-- The pool groups are generated with a single TakeOffParking point and no onward
-- route, so StartUncontrolled() alone only spins up engines — it will NOT take
-- off. The follow-on intercept route/task is what makes the cold-started AI
-- taxi, take off and hunt. So: Start first, then (after a short delay so the
-- Start command is processed) push the intercept task, which drives the takeoff.
local function spawnAndIntercept(rec)
    local mg = GROUP:FindByName(rec.name)
    if not mg then
        log("ERROR: cannot find pool group: " .. rec.name)
        return
    end
    rec.group   = mg
    rec.spawned = true
    mg:StartUncontrolled()
    log("Waking dormant group (cold start): " .. rec.name)
    timer.scheduleFunction(function()
        taskIntercept(rec)
        log("Tasked intercept (takeoff + hunt): " .. rec.name)
    end, nil, timer.getTime() + CFG_spawnDelay)
end

-- ── REGISTRATION: read dcsRetribution.scramble_pool ──────────────────────────
-- The pool table is written by a TriggerStart DoScript that runs at mission
-- start; we read it on the next tick so it is guaranteed populated.

timer.scheduleFunction(function()
    local border = dcsRetribution and dcsRetribution.scramble_border
    if border and #border >= 3 then
        _border = border
        if ZONE_POLYGON and ZONE_POLYGON.NewFromPointsArray then
            local points = {}
            for _, pt in ipairs(border) do
                points[#points + 1] = { x = pt.x, y = pt.z }
            end
            if #points >= 4 then
                local first, last = points[1], points[#points]
                if first.x == last.x and first.y == last.y then
                    table.remove(points, #points)
                end
            end
            if #points >= 3 then
                _borderZone = ZONE_POLYGON:NewFromPointsArray("Retribution Scramble Border", points)
            end
        end
        log(string.format("RED airspace border loaded (%d vertices)", #border))
    else
        log("No scramble border supplied — falling back to radar-range detection")
    end

    indexSupportGroups()

    local pool = dcsRetribution and dcsRetribution.scramble_pool
    if not pool then
        log("WARNING: dcsRetribution.scramble_pool not available — no interceptors registered")
        return
    end
    for _, name in ipairs(pool) do
        if not _groups[name] then
            local mg = GROUP:FindByName(name)
            _groups[name] = {
                name       = name,
                group      = mg,      -- uncontrolled groups exist at T=0
                busy       = false,
                lastTasked = 0,
                spawned    = false,
            }
            log("Registered dormant interceptor: " .. name)
        end
    end
end, nil, timer.getTime() + 0.1)

-- ── THREAT SCAN ──────────────────────────────────────────────────────────────

local function getRedRadarPositions()
    local pts = {}
    for _, cat in ipairs({ Group.Category.GROUND, Group.Category.SHIP }) do
        for _, g in ipairs(coalition.getGroups(coalition.side.RED, cat) or {}) do
            if g and g:isExist() then
                for _, u in ipairs(g:getUnits() or {}) do
                    if u and u:isExist() then
                        local d = u:getDesc()
                        if d and d.sensor and d.sensor.radar then
                            pts[#pts + 1] = u:getPoint()
                            break
                        end
                    end
                end
            end
        end
    end
    return pts
end

local function detectBlueThreats(radarPts)
    local threats, seen = {}, {}
    local function considerGroup(g)
        if not g or not g:isExist() then return end
        local name = g:getName()
        if seen[name] or _supportGroups[name] then return end

        local units = g:getUnits()
        local u = units and units[1]
        if not u or not u:isExist() or not u:inAir() then return end

        local pos = u:getPoint()
        if threatActive(pos, radarPts) then
            threats[#threats + 1] = { name = name, group = g, pos = pos }
            seen[name] = true
        end
    end

    if _borderZone then
        local blueSet = SET_GROUP:New()
        blueSet:FilterCoalitions("blue")
        blueSet:FilterCategoryAirplane()
        blueSet:FilterActive(true)
        blueSet:FilterZones({ _borderZone })
        blueSet:FilterOnce()
        blueSet:ForEachGroup(function(mooseGroup)
            local dcsGroup = Group.getByName(mooseGroup:GetName())
            considerGroup(dcsGroup)
        end)
    else
        for _, g in ipairs(coalition.getGroups(coalition.side.BLUE, Group.Category.AIRPLANE) or {}) do
            if g and g:isExist() then
                considerGroup(g)
            end
        end
    end
    return threats
end

-- Nearest available pool group to the threat, constrained by
-- CFG_responseRadius. Dormant groups report their parked position fine, so
-- distance ranking works before they spawn.
local function selectGroup(threatPos)
    local now = timer.getTime()
    local best, bestDist = nil, math.huge
    for _, rec in pairs(_groups) do
        local available = not rec.busy or (now - rec.lastTasked) > CFG_reengageDelay
        local mg = rec.group or GROUP:FindByName(rec.name)
        if available and mg and mg:IsAlive() then
            rec.group = mg
            local u1 = mg:GetUnit(1)
            if u1 and u1:IsAlive() then
                local d = dist3D(u1:GetVec3(), threatPos)
                if d <= CFG_responseRadius and d < bestDist then
                    best, bestDist = rec, d
                end
            end
        end
    end
    return best
end

SCHEDULER:New(nil, function()
    local radars = getRedRadarPositions()
    -- With a border polygon we trigger on penetration and don't need radars;
    -- without one we rely on radar detection, so nothing to do with no radars.
    if #radars == 0 and not _borderZone then return end

    local threats = detectBlueThreats(radars)
    local activeThreats = {}
    for _, threat in ipairs(threats) do
        activeThreats[threat.name] = true
    end

    for _, rec in pairs(_groups) do
        if rec.targetName and not activeThreats[rec.targetName] then
            clearAssignment(rec, "Released")
        end
    end

    if #threats == 0 then
        return
    end

    for _, threat in ipairs(threats) do
        local now = timer.getTime()
        local assignedName = _targetAssignments[threat.name]
        local assignedRec = assignedName and _groups[assignedName] or nil
        if assignedRec then
            local mg = assignedRec.group or GROUP:FindByName(assignedRec.name)
            if not mg or not mg:IsAlive() then
                clearAssignment(assignedRec, "Releasing dead interceptor")
                assignedRec = nil
            elseif assignedRec.spawned and (now - (assignedRec.lastVectorTime or 0)) >= CFG_vectorRefresh then
                taskIntercept(assignedRec)
            end
        end

        if not assignedRec then
            local rec = selectGroup(threat.pos)
            if rec then
                if not rec.busy or (now - rec.lastTasked) > CFG_reengageDelay then
                    rec.busy       = true
                    rec.lastTasked = now
                    rec.targetName = threat.name
                    _targetAssignments[threat.name] = rec.name
                    if rec.spawned then
                        taskIntercept(rec)
                    else
                        spawnAndIntercept(rec)
                    end
                    log("Scramble: " .. rec.name .. " -> " .. threat.group:getName())
                    MESSAGE:New("SCRAMBLE: interceptors launching!", 12):ToAll()
                end
            end
        end
    end
end, {}, 10, CFG_scanInterval)

-- ── STARTUP REPORT ───────────────────────────────────────────────────────────

timer.scheduleFunction(function()
    local n = 0
    for _ in pairs(_groups) do n = n + 1 end
    log(string.format("ONLINE — %d dormant interceptor group(s)", n))
    MESSAGE:New(string.format(
        "REACTIVE SCRAMBLE ONLINE: %d dormant interceptor group(s)", n), 12):ToAll()
end, nil, timer.getTime() + 2)

-- ── DEBUG STATUS ─────────────────────────────────────────────────────────────
-- Periodic one-liner so a test run can confirm from dcs.log that detection is
-- wired up (radar count, whether a border loaded, live threats). Set
-- CFG_debug = false to silence.
if CFG_debug then
    timer.scheduleFunction(function()
        local radars = getRedRadarPositions()
        local n = 0
        for _ in pairs(_groups) do n = n + 1 end
        local threats = detectBlueThreats(radars)
        log(string.format(
            "status: groups=%d radars=%d border=%s threats=%d",
            n, #radars, _borderZone and "yes" or "no", #threats))
        return timer.getTime() + 60
    end, nil, timer.getTime() + 25)
end
