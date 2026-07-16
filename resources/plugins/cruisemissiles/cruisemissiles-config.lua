---------------------------------------------------------------------------------------------------
-- Ship-launched cruise missile strikes runtime.
--
-- Reads dcsRetribution.cruiseMissiles (game/missiongenerator/cruisemissileluadata.py):
--   ships = { { group=, coalition=, remaining= }, ... }  -- live LACM ship groups + magazine
--   raids = { { group=, coalition=, target=, x=, y=, count= }, ... }  -- planned auto raids
--
-- Two fire paths share one budget:
--   * AUTO raids: after a launch delay, each planned raid ripples its salvo from its ship via a
--     FireAtPoint task with the cruise-missile weapon flag (the ME "fire Tomahawks at a point"
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
-- ordinary death events, enemy point defense engages them, and a sunk ship fires nothing -- the
-- plugin owns no kills and no spawns. Inert when the node is absent. pcall-guarded throughout;
-- definition order matters (Lua 5.1): helpers precede use.
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
local RAID_DELAY = 240 -- s after mission start before the auto raids launch
local PLAYER_SALVO = 4 -- missiles per F10 call-for-fire
local PLAYER_RANGE = 250 * NM_TO_M -- m, max ship-to-marker range for call-for-fire
local SALVO_RADIUS = 100 -- m, impact dispersion radius
local MENU = true -- F10 call-for-fire menu on

if dcsRetribution.plugins and dcsRetribution.plugins.cruisemissiles then
    local o = dcsRetribution.plugins.cruisemissiles
    RAID_DELAY = tonumber(o.raidDelayS) or RAID_DELAY
    PLAYER_SALVO = tonumber(o.playerSalvoSize) or PLAYER_SALVO
    PLAYER_RANGE = (tonumber(o.playerRangeNm) or 250) * NM_TO_M
    SALVO_RADIUS = tonumber(o.salvoRadiusM) or SALVO_RADIUS
    if o.menuEnabled ~= nil then
        MENU = o.menuEnabled
    end
end

-- Mirror-back channel: the base script serializes `cruise_missiles_state` into the debrief and
-- Python debits each ship group's persisted magazine by its reported `fired`. One entry per
-- group, updated in place (one shared table reference per group), with dirty_state flagged so
-- write_state actually flushes.
cruise_missiles_state = cruise_missiles_state or {}

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
    cmMsg(side, string.format(
        "CRUISE MISSILES AWAY -- %d missile(s) from %s inbound to %s.",
        salvo, groupName, tostring(targetLabel or "target")))
    -- The defender's cue is deliberately vague: a launch warning, not targeting intel.
    cmMsg(enemy, "LAUNCH WARNING -- enemy cruise missile launch detected.")
    env.info(string.format("CRUISEMISSILES|: %s fired %d at %s (%d left this mission)",
        groupName, salvo, tostring(targetLabel or "?"), remaining[groupName]))
    return salvo
end

-- AUTO raids: one scheduled launch pass after the delay (a dead ship / dry magazine simply
-- contributes nothing; there is no re-fire -- the raid was this turn's salvo).
local function fireRaids()
    for _, raid in ipairs(data.raids or {}) do
        local ok, err = pcall(function()
            fireCruise(raid.group, tonumber(raid.x) or 0, tonumber(raid.y) or 0,
                tonumber(raid.count) or 0, raid.target)
        end)
        if not ok then
            env.warning("cruisemissiles: raid launch error (continuing): " .. tostring(err))
        end
    end
    return nil
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
        timer.scheduleFunction(fireRaids, {}, timer.getTime() + RAID_DELAY)
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
