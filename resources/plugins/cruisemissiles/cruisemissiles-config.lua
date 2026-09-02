---------------------------------------------------------------------------------------------------
-- Ship-launched cruise missile strikes runtime.
--
-- Reads dcsRetribution.cruiseMissiles (game/missiongenerator/cruisemissileluadata.py):
--   ships = { { group=, coalition=, remaining= }, ... }  -- live LACM ship groups + magazine
--   raids = { { group=, coalition=, target=, x=, y=, count= }, ... }  -- planned auto raids
--
-- Two fire paths share one budget:
--   * AUTO raids: each planned raid launches at its own random moment inside the launch window
--     (staggered so several naval groups don't ripple simultaneously and stack the missile count
--     against the framerate -- the same stagger the SCUD fire tasks use), rippling its salvo via
--     a FireAtPoint task with the cruise-missile weapon flag (the ME "fire Tomahawks at a point"
--     mechanism, pushed by script).
--   * PLAYER call-for-fire: an F10 "Cruise Missile Strike" menu fires a salvo from the nearest
--     capable friendly ship onto the coalition's last F10 map marker.
--     The marker's own text sizes the salvo: just a number ("6" or "#6") fires exactly that
--     many (magazine-capped); any other text fires the default.
--
-- The emitted `remaining` is this mission's HARD expenditure cap per ship group (the campaign
-- magazine -- DCS would happily reload every mission, Python would not). Everything actually
-- fired is mirrored into the cruise_missiles_state debrief channel so the turn boundary debits
-- the persisted magazine; a mission that never fires debits nothing.
--
-- The missiles are real DCS weapons from real, tracked ships: kills record natively through the
-- ordinary death events, and a sunk ship fires nothing -- the plugin owns no kills and no
-- spawns. Because nothing in DCS wakes a defender for a weapon object on its own (flight
-- testing 2026-07-16: alive point-defense SAMs 250 m from the aimpoint sat idle through a
-- salvo -- ALARM AUTO only trips on aircraft), every launch also brings the opposing side's
-- air defenses near the aimpoint to alarm-RED readiness for the missile flight window (alarm
-- state only, never emission toggling), so the point defense actually gets its intercept
-- shot. Inert when the node is absent. pcall-guarded throughout; definition order matters
-- (Lua 5.1): helpers precede use.
---------------------------------------------------------------------------------------------------

if not (dcsRetribution and dcsRetribution.cruiseMissiles and GROUP) then
    return
end

local data = dcsRetribution.cruiseMissiles

local NM_TO_M = 1852
-- DCS weapon flag for cruise missiles (ENUMS.WeaponFlag.CruiseMissile) -- the FireAtPoint
-- weaponType that makes a Tomahawk/Kalibr ship actually ripple missiles instead of guns.
local CRUISE_MISSILE_FLAG = 2097152

-- Defaults. Overridable via the plugin options (dcsRetribution.plugins.cruisemissiles).
local RAID_DELAY_MIN = 240 -- s after mission start: the auto-raid launch window opens
local RAID_DELAY_MAX = 900 -- s after mission start: the auto-raid launch window closes
local PLAYER_SALVO = 4 -- missiles per F10 call-for-fire
local PLAYER_RANGE = 250 * NM_TO_M -- m, max ship-to-marker range for call-for-fire
local SALVO_RADIUS = 100 -- m, impact dispersion radius
local MENU = true -- F10 call-for-fire menu on
local DEFENDER_WAKE = true -- a launch brings opposing AD near the aimpoint to readiness
local WAKE_RADIUS = 8 * NM_TO_M -- m around the impact point swept for defenders
local WAKE_EXTRA = 300 -- s held at readiness past the estimated missile arrival
local WAKE_MISSILE_SPEED = 200 -- m/s assumed cruise speed (low estimate -> generous hold)

if dcsRetribution.plugins and dcsRetribution.plugins.cruisemissiles then
    local o = dcsRetribution.plugins.cruisemissiles
    -- raidDelayS is the pre-window legacy option name; honor it as the window open.
    RAID_DELAY_MIN = tonumber(o.raidDelayMinS) or tonumber(o.raidDelayS) or RAID_DELAY_MIN
    RAID_DELAY_MAX = tonumber(o.raidDelayMaxS) or RAID_DELAY_MAX
    if RAID_DELAY_MAX < RAID_DELAY_MIN then
        RAID_DELAY_MAX = RAID_DELAY_MIN
    end
    PLAYER_SALVO = tonumber(o.playerSalvoSize) or PLAYER_SALVO
    PLAYER_RANGE = (tonumber(o.playerRangeNm) or 250) * NM_TO_M
    SALVO_RADIUS = tonumber(o.salvoRadiusM) or SALVO_RADIUS
    if o.menuEnabled ~= nil then
        MENU = o.menuEnabled
    end
    if o.defenderWake ~= nil then
        DEFENDER_WAKE = o.defenderWake
    end
    WAKE_RADIUS = (tonumber(o.defenderWakeRadiusNm) or 8) * NM_TO_M
    WAKE_EXTRA = tonumber(o.defenderWakeExtraS) or WAKE_EXTRA
end

-- Mirror-back channel: the base script serializes `cruise_missiles_state` into the debrief and
-- Python debits each ship group's persisted magazine by its reported `fired`. One entry per
-- group, updated in place (one shared table reference per group), with dirty_state flagged so
-- write_state actually flushes.
cruise_missiles_state = cruise_missiles_state or {}

-- Defender launch wake: nothing in DCS ever wakes a defender for a cruise missile on its
-- own -- ALARM AUTO only trips on aircraft, and IADS scripts scan units, never weapon
-- objects -- so without this, raids fly in unopposed past alive SAMs. On every launch
-- (raid or call-for-fire), the opposing side's ground air-defense groups near the
-- AIMPOINT are set alarm state RED (radars up: the LAUNCH WARNING doing its job) and
-- stood back down to AUTO once the salvo has long arrived. Alarm state ONLY -- emission
-- toggling stays untouched, and a Skynet-managed site keeps its own emission-control
-- loop (Skynet may re-dark it; that is the IADS engine's call to make).
local wakeUntil = {} -- AD group name -> sim time to hold RED until

local function standDownDefender(name, t)
    local holdUntil = wakeUntil[name]
    if not holdUntil then
        return nil
    end
    if t and t < holdUntil then
        -- A later launch extended the hold; come back when it lapses.
        return holdUntil + 1
    end
    wakeUntil[name] = nil
    pcall(function()
        local grp = Group.getByName(name)
        if grp and grp:isExist() then
            grp:getController():setOption(
                AI.Option.Ground.id.ALARM_STATE, AI.Option.Ground.val.ALARM_STATE.AUTO)
        end
    end)
    return nil
end

local function firstAirDefenseUnit(grp)
    for _, u in ipairs(grp:getUnits() or {}) do
        if u:isExist() and u:hasAttribute("Air Defence") then
            return u
        end
    end
    return nil
end

local function wakeDefenders(shooterSide, x, y, flightDist)
    if not DEFENDER_WAKE then
        return
    end
    local enemy = (shooterSide == coalition.side.RED) and coalition.side.BLUE
        or coalition.side.RED
    local holdUntil = timer.getTime()
        + (tonumber(flightDist) or 0) / WAKE_MISSILE_SPEED
        + WAKE_EXTRA
    local woken = 0
    for _, grp in ipairs(coalition.getGroups(enemy, Group.Category.GROUND) or {}) do
        pcall(function()
            if grp:isExist() then
                local unit = firstAirDefenseUnit(grp)
                if unit then
                    local p = unit:getPoint()
                    local d = math.sqrt((p.x - x) ^ 2 + (p.z - y) ^ 2)
                    if d <= WAKE_RADIUS then
                        local name = grp:getName()
                        grp:getController():setOption(
                            AI.Option.Ground.id.ALARM_STATE,
                            AI.Option.Ground.val.ALARM_STATE.RED)
                        wakeUntil[name] = math.max(wakeUntil[name] or 0, holdUntil)
                        timer.scheduleFunction(standDownDefender, name, holdUntil + 1)
                        woken = woken + 1
                    end
                end
            end
        end)
    end
    if woken > 0 then
        env.info(string.format(
            "CRUISEMISSILES|: defender wake -- %d AD group(s) near the aimpoint held RED",
            woken))
    end
end

local remaining = {} -- group name -> missiles left this mission (the emitted magazine)
local shipSide = {} -- group name -> coalition.side
local shipsBySide = { [coalition.side.RED] = {}, [coalition.side.BLUE] = {} }
local fired = {} -- group name -> its cruise_missiles_state entry

local function sideOf(name)
    if name == "red" then
        return coalition.side.RED
    end
    return coalition.side.BLUE
end

for _, s in ipairs(data.ships or {}) do
    if s.group then
        local side = sideOf(s.coalition)
        remaining[s.group] = tonumber(s.remaining) or 0
        shipSide[s.group] = side
        table.insert(shipsBySide[side], s.group)
    end
end

local function recordFired(groupName, count)
    local entry = fired[groupName]
    if not entry then
        entry = { group = groupName, fired = 0 }
        fired[groupName] = entry
        cruise_missiles_state[#cruise_missiles_state + 1] = entry
    end
    entry.fired = entry.fired + count
    dirty_state = true
end

local function cmMsg(side, text)
    pcall(trigger.action.outTextForCoalition, side, text, 12)
end

-- Fire `count` cruise missiles from `groupName` at (x = north, y = east), capped by the group's
-- remaining budget. Returns the salvo actually committed (0 = ship dead / magazine dry).
local function fireCruise(groupName, x, y, count, targetLabel)
    local budget = remaining[groupName] or 0
    count = tonumber(count) or 0
    if budget <= 0 or count <= 0 then
        return 0
    end
    local grp = GROUP:FindByName(groupName)
    if not (grp and grp:IsAlive()) then
        return 0
    end
    local salvo = math.min(count, budget)
    local task = grp:TaskFireAtPoint({ x = x, y = y }, SALVO_RADIUS, salvo, CRUISE_MISSILE_FLAG)
    grp:PushTask(task, 1)
    remaining[groupName] = budget - salvo
    recordFired(groupName, salvo)
    local side = shipSide[groupName] or coalition.side.BLUE
    local enemy = (side == coalition.side.RED) and coalition.side.BLUE or coalition.side.RED
    -- The launch is observable, so the defense near the aimpoint comes to readiness.
    local flightDist = 0
    pcall(function()
        local sv = grp:GetCoordinate():GetVec2()
        flightDist = math.sqrt((sv.x - x) ^ 2 + (sv.y - y) ^ 2)
    end)
    wakeDefenders(side, x, y, flightDist)
    cmMsg(side, string.format(
        "CRUISE MISSILES AWAY -- %d missile(s) from %s inbound to %s.",
        salvo, groupName, tostring(targetLabel or "target")))
    -- The defender's cue is deliberately vague: a launch warning, not targeting intel.
    cmMsg(enemy, "LAUNCH WARNING -- enemy cruise missile launch detected.")
    env.info(string.format("CRUISEMISSILES|: %s fired %d at %s (%d left this mission)",
        groupName, salvo, tostring(targetLabel or "?"), remaining[groupName]))
    return salvo
end

-- AUTO raids: each raid fires once at its own scheduled moment (a dead ship / dry magazine at
-- fire time simply contributes nothing; there is no re-fire -- the raid was this turn's salvo).
local function fireOneRaid(raid)
    local ok, err = pcall(function()
        fireCruise(raid.group, tonumber(raid.x) or 0, tonumber(raid.y) or 0,
            tonumber(raid.count) or 0, raid.target)
    end)
    if not ok then
        env.warning("cruisemissiles: raid launch error (continuing): " .. tostring(err))
    end
    return nil
end

-- Pick each raid's launch moment inside [RAID_DELAY_MIN, RAID_DELAY_MAX], so several naval
-- groups (or both sides) never ripple their salvos simultaneously and stack the in-flight
-- missile count against the framerate.
local function raidDelay()
    if RAID_DELAY_MAX <= RAID_DELAY_MIN then
        return RAID_DELAY_MIN
    end
    return math.random(RAID_DELAY_MIN, RAID_DELAY_MAX)
end

-- PLAYER call-for-fire: nearest capable friendly ship within range of the target point.
local function nearestCapableShip(side, target)
    local bestName, bestD
    for _, name in ipairs(shipsBySide[side] or {}) do
        if (remaining[name] or 0) > 0 then
            local grp = GROUP:FindByName(name)
            if grp and grp:IsAlive() then
                local sv = grp:GetCoordinate():GetVec2()
                local d = math.sqrt((sv.x - target.x) ^ 2 + (sv.y - target.y) ^ 2)
                if d <= PLAYER_RANGE and (not bestD or d < bestD) then
                    bestName, bestD = name, d
                end
            end
        end
    end
    return bestName
end

-- Salvo size for a call-for-fire: the marker itself can order the count. A marker
-- whose text is just a number -- "6", or "#6" ("a # and nothing else") -- fires
-- exactly that many; any other text (or none) fires the default salvo. The
-- magazine still caps whatever is asked, so a big number just empties the tubes.
local function salvoFromMarkText(text)
    if type(text) ~= "string" then
        return PLAYER_SALVO
    end
    local n = tonumber(text:match("^%s*#?%s*(%d+)%s*$"))
    if n and n >= 1 then
        return n
    end
    return PLAYER_SALVO
end

-- Fire on the coalition's most recent F10 map marker.
local function fireOnLastMark(side)
    local ok, err = pcall(function()
        local panels = world.getMarkPanels() or {}
        local best
        for _, m in pairs(panels) do
            if m.pos and (m.coalition == side or m.coalition == -1) then
                if not best or (m.idx or 0) > (best.idx or 0) then
                    best = m
                end
            end
        end
        if not best then
            cmMsg(side, "Cruise missile strike: place an F10 map marker on the target "
                .. "first (marker text '#N' sets the salvo size).")
            return
        end
        -- mark pos is a DCS vec3 { x = north, y = alt, z = east }.
        local tgt = { x = best.pos.x, y = best.pos.z }
        local ship = nearestCapableShip(side, tgt)
        if not ship then
            cmMsg(side, "Cruise missile strike: no ship with missiles in range of that marker.")
            return
        end
        local salvo = salvoFromMarkText(best.text)
        if fireCruise(ship, tgt.x, tgt.y, salvo, "your F10 marker") == 0 then
            cmMsg(side, "Cruise missile strike: launch failed -- magazine dry.")
        end
    end)
    if not ok then
        env.warning("cruisemissiles: fire-on-mark error (continuing): " .. tostring(err))
    end
end

-- Magazine readout so the coalition knows what stock is left before calling fire.
local function magazineStatus(side)
    local ok, err = pcall(function()
        local lines = { "Cruise missile magazines:" }
        for _, name in ipairs(shipsBySide[side] or {}) do
            local grp = GROUP:FindByName(name)
            local state
            if grp and grp:IsAlive() then
                state = string.format("%d missile(s)", remaining[name] or 0)
            else
                state = "SUNK"
            end
            lines[#lines + 1] = string.format("  %s: %s", name, state)
        end
        cmMsg(side, table.concat(lines, "\n"))
    end)
    if not ok then
        env.warning("cruisemissiles: magazine status error (continuing): " .. tostring(err))
    end
end

local ok, err = pcall(function()
    if data.raids and #data.raids > 0 then
        for _, raid in ipairs(data.raids) do
            timer.scheduleFunction(fireOneRaid, raid, timer.getTime() + raidDelay())
        end
    end
    if MENU then
        for _, side in pairs({ coalition.side.RED, coalition.side.BLUE }) do
            if #shipsBySide[side] > 0 then
                local root = missionCommands.addSubMenuForCoalition(side, "Cruise Missile Strike")
                missionCommands.addCommandForCoalition(
                    side,
                    string.format(
                        "Fire at last F10 map marker (%d, or marker text #N)",
                        PLAYER_SALVO
                    ),
                    root, fireOnLastMark, side
                )
                missionCommands.addCommandForCoalition(
                    side, "Magazine status", root, magazineStatus, side
                )
            end
        end
    end
    env.info(string.format(
        "CRUISEMISSILES|: armed -- %d/%d ship group(s) blue/red, %d raid(s), menu %s",
        #shipsBySide[coalition.side.BLUE], #shipsBySide[coalition.side.RED],
        (data.raids and #data.raids or 0), tostring(MENU)))
end)
if not ok then
    env.error("CRUISEMISSILES|: setup error: " .. tostring(err))
end
