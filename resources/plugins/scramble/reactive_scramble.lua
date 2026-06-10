-- ============================================================================
-- REACTIVE SCRAMBLE v2.0 (Retribution GCI Scramble Plugin)
-- Bundled automatically into every Retribution-generated .miz that has a
-- non-empty RED untasked-aircraft scramble pool.
-- ============================================================================
--
-- Retribution spawns each RED squadron's leftover untasked aircraft cold on the
-- ramp as uncontrolled groups. The mission generator records the air-to-air
-- capable groups in dcsRetribution.scramble_pool.
--
-- This script holds those groups dormant until a Blue aircraft is detected by
-- the RED radar network within CFG_engageRadius, then wakes the nearest
-- available one with StartUncontrolled and tasks it to intercept.
--
-- Cold-ramp behavior is intentional: an idle group starts cold, taxis, takes
-- off, and hunts. Nothing flies until a threat appears.
-- ============================================================================

local CFG_scanInterval  = 15      -- seconds between threat scans
local CFG_engageRadius  = 95000   -- metres, about 51 nm
local CFG_reengageDelay = 180     -- seconds before a busy group re-qualifies
local CFG_spawnDelay    = 1.0     -- seconds between Start command and setTask

-- Retribution plugin config override. The config table is written by the
-- mission-start data trigger, so read it on the next tick.
timer.scheduleFunction(function()
    if not (dcsRetribution and dcsRetribution.plugins and dcsRetribution.plugins.scramble) then return end
    local c = dcsRetribution.plugins.scramble
    if c.engageRadius ~= nil then CFG_engageRadius = c.engageRadius * 1852 end
    if c.reengageDelay ~= nil then CFG_reengageDelay = c.reengageDelay end
end, nil, timer.getTime() + 0)

local _groups = {} -- name -> record

local function log(msg)
    BASE:E("=== SCRAMBLE: " .. tostring(msg))
end

local function dist3D(p1, p2)
    local dx = p1.x - p2.x
    local dy = (p1.y or 0) - (p2.y or 0)
    local dz = p1.z - p2.z
    return math.sqrt(dx * dx + dy * dy + dz * dz)
end

local function taskIntercept(rec)
    local mg = GROUP:FindByName(rec.name)
    if not mg or not mg:IsAlive() then return end

    rec.group = mg
    mg:OptionROEWeaponFree()
    mg:OptionROTEvadeFire()

    local ctrl = mg:GetController()
    if ctrl then
        ctrl:setTask({
            id = "EngageTargets",
            params = {
                targetTypes = { "Air" },
                maxDist = CFG_engageRadius,
                priority = 0,
            },
        })
    end
end

-- Wake a dormant uncontrolled group, then task it after a short delay so DCS
-- finishes processing the Start command before setTask fires.
local function spawnAndIntercept(rec)
    local mg = GROUP:FindByName(rec.name)
    if not mg then
        log("ERROR: cannot find pool group: " .. rec.name)
        return
    end

    rec.group = mg
    rec.spawned = true
    mg:StartUncontrolled()
    log("Waking dormant group: " .. rec.name)

    timer.scheduleFunction(function()
        taskIntercept(rec)
    end, nil, timer.getTime() + CFG_spawnDelay)
end

-- The pool table is written by a TriggerStart DoScript. Read it on the next
-- tick so it is populated before registration.
timer.scheduleFunction(function()
    local pool = dcsRetribution and dcsRetribution.scramble_pool
    if not pool then
        log("WARNING: dcsRetribution.scramble_pool not available - no interceptors registered")
        return
    end

    for _, name in ipairs(pool) do
        if not _groups[name] then
            local mg = GROUP:FindByName(name)
            _groups[name] = {
                name = name,
                group = mg,
                busy = false,
                lastTasked = 0,
                spawned = false,
            }
            log("Registered dormant interceptor: " .. name)
        end
    end
end, nil, timer.getTime() + 0.1)

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
    local threats = {}
    local seen = {}

    for _, g in ipairs(coalition.getGroups(coalition.side.BLUE, Group.Category.AIRPLANE) or {}) do
        if g and g:isExist() and not seen[g:getName()] then
            local units = g:getUnits()
            local u = units and units[1]
            if u and u:isExist() then
                local pos = u:getPoint()
                for _, rp in ipairs(radarPts) do
                    if dist3D(pos, rp) <= CFG_engageRadius then
                        threats[#threats + 1] = { group = g, pos = pos }
                        seen[g:getName()] = true
                        break
                    end
                end
            end
        end
    end

    return threats
end

-- Pick the nearest available pool group to the threat. Dormant groups report
-- their parked position, so distance ranking works before they wake.
local function selectGroup(threatPos)
    local now = timer.getTime()
    local best = nil
    local bestDist = math.huge

    for _, rec in pairs(_groups) do
        local available = not rec.busy or (now - rec.lastTasked) > CFG_reengageDelay
        local mg = rec.group or GROUP:FindByName(rec.name)
        if available and mg and mg:IsAlive() then
            rec.group = mg
            local u1 = mg:GetUnit(1)
            if u1 and u1:IsAlive() then
                local d = dist3D(u1:GetVec3(), threatPos)
                if d < bestDist then
                    best = rec
                    bestDist = d
                end
            end
        end
    end

    return best
end

SCHEDULER:New(nil, function()
    local radars = getRedRadarPositions()
    if #radars == 0 then return end

    local threats = detectBlueThreats(radars)

    if #threats == 0 then
        local now = timer.getTime()
        for _, rec in pairs(_groups) do
            if rec.busy and (now - rec.lastTasked) > CFG_reengageDelay then
                rec.busy = false
                log("Released: " .. rec.name)
            end
        end
        return
    end

    for _, threat in ipairs(threats) do
        local rec = selectGroup(threat.pos)
        if rec then
            local now = timer.getTime()
            if not rec.busy or (now - rec.lastTasked) > CFG_reengageDelay then
                rec.busy = true
                rec.lastTasked = now

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
end, {}, 10, CFG_scanInterval)

timer.scheduleFunction(function()
    local n = 0
    for _ in pairs(_groups) do n = n + 1 end
    log(string.format("ONLINE - %d dormant interceptor group(s)", n))
    MESSAGE:New(string.format(
        "REACTIVE SCRAMBLE ONLINE: %d dormant interceptor group(s)", n), 12):ToAll()
end, nil, timer.getTime() + 2)
