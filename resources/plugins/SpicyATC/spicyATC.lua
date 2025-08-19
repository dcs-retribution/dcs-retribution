-- spicyATC_custom.lua - Improved BMS‑style ATC for DCS Missions (auto-assign base and runway takeoff gating)
-- Author: Spicy
-- Version: Alpha 0.2
---------------------------
-- Logging 
---------------------------
local function log(msg)
  env.info("SpicyATC: " .. tostring(msg))
end

local function logf(fmt, ...)
  local ok, s = pcall(string.format, fmt, ...)
  if ok then log(s) else log("format error: " .. tostring(fmt)) end
end

---------------------------
-- State & Structures
---------------------------
-- Each player record now also tracks hasTakenOff (true when the player has left the runway).
local players          = {}   -- unitName -> { coalitionID, unitID, airbaseName, state, engineStarted, hasTakenOff }
local unitCoalitions   = {}   -- unitName -> coalitionID
local takeoffQueues    = {}   -- airbaseName -> { unitName1, ... }
local landingQueues    = {}   -- airbaseName -> { unitName1, ... }
local menuPaths        = {}   -- coalitionID -> { root, ground, tower, approach, selectAB }
local telemetry        = {}   -- unitName -> { time=number, point=vec3, speed_mps=number, alt_m=number }

---------------------------
-- Helicopter Support
---------------------------
-- Determine if a unit is a helicopter based upon its description category.
local function isHelicopter(unit)
  if not unit or not unit.getDesc then return false end
  local ok, desc = pcall(unit.getDesc, unit)
  if ok and desc and desc.category then
    -- In DCS scripting, Unit.getDesc().category == 1 indicates a helicopter.
    return desc.category == 1
  end
  return false
end

---------------------------
-- Utility / Context
---------------------------
local function now() return timer.getTime() end
local function metersToNM(m) return m / 1852.0 end

local function planarDistanceMeters(a, b)
  local dx = (a.x or 0) - (b.x or 0)
  local dz = (a.z or 0) - (b.z or 0)
  return math.sqrt(dx * dx + dz * dz)
end

-- Wrapper to get point
local function pointOf(obj, label)
  if not obj then return nil end
  local p = nil
  if obj.getPoint then
    p = obj:getPoint()
  else
    -- Static Airbase API form
    local ok, got = pcall(Airbase.getPoint, obj)
    if ok then p = got end
  end
  if p and label then
    logf("pointOf(%s): x=%.2f z=%.2f y=%.2f", label, p.x or 0, p.z or 0, p.y or 0)
  end
  return p
end

-- Fixed coalition IDs per spec
local function getActiveCoalitionIDs()
  return { coalition.side.BLUE, coalition.side.RED, coalition.side.NEUTRAL }
end

local function getAirbaseName(ab)
  if not ab then return "Airbase ?" end
  if ab.getName then
    local ok, n = pcall(ab.getName, ab)
    if ok and n then return n end
  end
  if Airbase.getName then
    local ok, n = pcall(Airbase.getName, ab)
    if ok and n then return n end
  end
  if Airbase.getCallsign then
    local ok, n = pcall(Airbase.getCallsign, ab)
    if ok and n then return n end
  end
  local ok, id = pcall(Airbase.getID, ab)
  return ok and ("Airbase " .. tostring(id)) or "Airbase ?"
end

local function getPlayerContext()
  local unit = world.getPlayer()
  if not unit or not unit.isExist or not unit:isExist() then return nil end
  local ctx = {
    unit        = unit,
    unitName    = unit.getName and unit:getName() or nil,
    coalitionID = unit.getCoalition and unit:getCoalition() or nil,
    unitID      = unit.getID and unit:getID() or nil,
    group       = unit.getGroup and unit:getGroup() or nil,
    playerName  = unit.getPlayerName and unit:getPlayerName() or nil,
  }
  ctx.groupID = ctx.group and ctx.group.getID and ctx.group:getID() or nil
  -- Log snapshot
  local p = pointOf(unit, "player")
  local v = unit.getVelocity and unit:getVelocity() or {x=0,y=0,z=0}
  local spd = math.sqrt((v.x or 0)^2 + (v.y or 0)^2 + (v.z or 0)^2)
  logf("getPlayerContext(): unit=%s id=%s coalition=%s groupID=%s speed=%.1f mps",
       tostring(ctx.unitName), tostring(ctx.unitID), tostring(ctx.coalitionID),
       tostring(ctx.groupID), spd)
  return ctx
end

-- Capture telemetry for range checks
local function captureTelemetry(unit)
  if not unit or not unit.isExist or not unit:isExist() then return end
  local name = unit:getName()
  local pt   = pointOf(unit)
  local vel  = unit.getVelocity and unit:getVelocity() or {x=0,y=0,z=0}
  local spd  = math.sqrt((vel.x or 0)^2 + (vel.y or 0)^2 + (vel.z or 0)^2)
  telemetry[name] = { time = now(), point = pt, speed_mps = spd, alt_m = (pt and pt.y) or 0 }
  logf("telemetry[%s]: time=%.1f alt=%.1f speed=%.1f", name, telemetry[name].time, telemetry[name].alt_m, telemetry[name].speed_mps)
end

local function listCoalitionAirbases(coalitionID)
  local list = coalition.getAirbases(coalitionID) or {}
  logf("listCoalitionAirbases(%s): count=%d", tostring(coalitionID), #list)
  return list
end

local function nearestOwnedAirbase(unit, coalitionID)
  local list = listCoalitionAirbases(coalitionID)
  if not unit or not unit.isExist or not unit:isExist() or #list == 0 then return nil end
  local up = pointOf(unit)
  local best, bestD = nil, 1e12
  for i = 1, #list do
    local ab = list[i]
    if ab and ab.isExist and ab:isExist() then
      local p = pointOf(ab)
      local d = planarDistanceMeters(up, p)
      if d < bestD then
        best, bestD = ab, d
      end
    end
  end
  logf("nearestOwnedAirbase: winner=%s d=%.1f m (%.2f NM)", getAirbaseName(best), bestD, metersToNM(bestD))
  return best
end

---------------------------
-- Forward Declarations
---------------------------
local ensureMenusForCoalition
local rebuildAirbaseList
local selectAirbase
local requestStartup
local requestTaxi
local requestTakeoff
local requestHandoff
local requestSlasherCheckIn
local setAirborne
local requestInbound
local requestApproach
local requestLanding
local requestTaxiToParking
local requestShutdown
local onEvent
local retryAddMenus
local periodicApproachTick

---------------------------
-- Menu Building
---------------------------
ensureMenusForCoalition = function(coalitionID)
  if not coalitionID then return end
  menuPaths[coalitionID] = menuPaths[coalitionID] or {}
  local paths = menuPaths[coalitionID]
  if not paths.root then
    -- Root
    paths.root = missionCommands.addSubMenuForCoalition(coalitionID, "SpicyATC")
    -- Submenus
    paths.ground   = missionCommands.addSubMenuForCoalition(coalitionID, "Ground",   paths.root)
    paths.tower    = missionCommands.addSubMenuForCoalition(coalitionID, "Tower",    paths.root)
    -- Rename the Approach menu to Slasher to match radio calls
    paths.approach = missionCommands.addSubMenuForCoalition(coalitionID, "Slasher", paths.root)
    -- Ground commands
    -- The home airbase is assigned automatically on spawn, so we no longer
    -- present a "Select Home Airbase" menu here.
    missionCommands.addCommandForCoalition(coalitionID, "Request Startup",     paths.ground,   requestStartup)
    missionCommands.addCommandForCoalition(coalitionID, "Request Taxi",        paths.ground,   requestTaxi)
    missionCommands.addCommandForCoalition(coalitionID, "Taxi to Parking",     paths.ground,   requestTaxiToParking)
    missionCommands.addCommandForCoalition(coalitionID, "Shutdown",            paths.ground,   requestShutdown)
    missionCommands.addCommandForCoalition(coalitionID, "Refresh Airbase List",paths.ground,   function() rebuildAirbaseList(coalitionID) end)
    -- Tower commands
    missionCommands.addCommandForCoalition(coalitionID, "Request Takeoff",     paths.tower,    requestTakeoff)
    missionCommands.addCommandForCoalition(coalitionID, "Request Handoff",     paths.tower,    requestHandoff)
    missionCommands.addCommandForCoalition(coalitionID, "Request Landing",     paths.tower,    requestLanding)
    -- Approach commands
    missionCommands.addCommandForCoalition(coalitionID, "Request Inbound",     paths.approach, requestInbound)
    missionCommands.addCommandForCoalition(coalitionID, "Request Approach",    paths.approach, requestApproach)
    -- Free check‑in option for Slasher
    missionCommands.addCommandForCoalition(coalitionID, "Check In",        paths.approach, requestSlasherCheckIn)
    logf("ensureMenusForCoalition(%s): built", tostring(coalitionID))
  end
end

rebuildAirbaseList = function(coalitionID)
  if not coalitionID then return end
  local paths = menuPaths[coalitionID]
  if not paths or not paths.ground then return end
  -- Remove old select list
  if paths.selectAB then
    missionCommands.removeItemForCoalition(coalitionID, paths.selectAB)
    paths.selectAB = nil
  end
  paths.selectAB = missionCommands.addSubMenuForCoalition(coalitionID, "Select Home Airbase", paths.ground)
  -- Recommended (nearest owned)
  missionCommands.addCommandForCoalition(coalitionID, "Recommended (Nearest Owned)", paths.selectAB, function()
    local ctx = getPlayerContext(); if not ctx then return end
    local ab = nearestOwnedAirbase(ctx.unit, ctx.coalitionID)
    if ab then
      selectAirbase({ airbaseName = getAirbaseName(ab) })
    else
      trigger.action.outTextForCoalition(ctx.coalitionID, "ATC: No owned airbases found.", 10, false)
    end
  end)
  -- Owned list only
  local list = listCoalitionAirbases(coalitionID)
  if #list == 0 then
    missionCommands.addCommandForCoalition(coalitionID, "(No owned airbases)", paths.selectAB, function() end)
  else
    table.sort(list, function(a,b) return getAirbaseName(a) < getAirbaseName(b) end)
    for _, ab in ipairs(list) do
      local abName = getAirbaseName(ab)
      missionCommands.addCommandForCoalition(coalitionID, abName, paths.selectAB, selectAirbase, { airbaseName = abName })
    end
  end
  logf("rebuildAirbaseList(%s): done", tostring(coalitionID))
end

---------------------------
-- Player Flow / State
---------------------------
selectAirbase = function(args)
  local abName = args and args.airbaseName or nil
  local ctx = getPlayerContext(); if not ctx or not abName then return end
  local p = players[ctx.unitName] or { coalitionID = ctx.coalitionID, unitID = ctx.unitID, airbaseName = nil, state = "not_started", engineStarted = false, hasTakenOff = false }
  players[ctx.unitName] = p
  p.coalitionID = ctx.coalitionID
  p.unitID      = ctx.unitID
  p.airbaseName = abName
  if not p.state or p.state == "airborne" then p.state = "not_started" end
  logf("selectAirbase: unit=%s set=%s", tostring(ctx.unitName), tostring(abName))
  trigger.action.outTextForCoalition(ctx.coalitionID, "ATC: Home airbase set to " .. abName .. ".", 10, false)
end

-- Automatically assign the nearest owned airbase to the player if none is set.
local function autoAssignHomeBase(ctx)
  if not ctx then return end
  local p = players[ctx.unitName]
  if p and not p.airbaseName then
    local ab = nearestOwnedAirbase(ctx.unit, ctx.coalitionID)
    if ab then
      p.airbaseName = getAirbaseName(ab)
      trigger.action.outTextForCoalition(ctx.coalitionID, "ATC: Home airbase set to " .. p.airbaseName .. ".", 10, false)
      logf("autoAssignHomeBase: unit=%s assigned=%s", tostring(ctx.unitName), tostring(p.airbaseName))
    else
      trigger.action.outTextForCoalition(ctx.coalitionID, "ATC: No owned airbases found.", 10, false)
    end
  end
end

requestStartup = function()
  local ctx = getPlayerContext(); if not ctx then return end
  local p = players[ctx.unitName]
  if not p then
    -- If no player record exists (e.g. birth event not processed yet), create one
    p = { coalitionID = ctx.coalitionID, unitID = ctx.unitID, airbaseName = nil, state = "not_started", engineStarted = false, hasTakenOff = false }
    players[ctx.unitName] = p
  end
  -- Auto assign home base if needed
  autoAssignHomeBase(ctx)
  -- If no home base is set yet, try to assign one but do not block startup
  if not p.airbaseName then
    autoAssignHomeBase(ctx)
  end
  if p.state ~= "not_started" then
    trigger.action.outTextForCoalition(ctx.coalitionID, "ATC: Not in correct state for startup.", 10, false)
    return
  end
  p.state = "started"
  local group = ctx.group
  local numUnits = group and group.getUnits and #group:getUnits() or 1
  local msg = nil
  if numUnits > 1 then
    msg = "Flight cleared for startup (" .. numUnits .. " aircraft). Contact ground for taxi."
  else
    msg = "Cleared for startup. Contact ground for taxi."
  end
  logf("requestStartup: unit=%s state=started", tostring(ctx.unitName))
  trigger.action.outTextForCoalition(ctx.coalitionID, "ATC Ground: " .. msg, 10, false)
end

requestTaxi = function()
  local ctx = getPlayerContext(); if not ctx then return end
  local p = players[ctx.unitName]
  if not p then
    p = { coalitionID = ctx.coalitionID, unitID = ctx.unitID, airbaseName = nil, state = "not_started", engineStarted = false, hasTakenOff = false }
    players[ctx.unitName] = p
  end
  autoAssignHomeBase(ctx)
  -- If no home base is set yet, try to assign one but do not block taxi
  if not p.airbaseName then
    autoAssignHomeBase(ctx)
  end
  -- If already taxiing, repeat the taxi clearance
  if p.state == "on_taxi" then
    trigger.action.outTextForCoalition(ctx.coalitionID, "ATC Ground: Taxi to the runway and hold short. Contact tower for takeoff clearance.", 10, false)
    return
  end
  if p.state ~= "started" then
    trigger.action.outTextForCoalition(ctx.coalitionID, "ATC: Not cleared for taxi yet.", 10, false)
    return
  end
  p.state = "on_taxi"
  logf("requestTaxi: unit=%s state=on_taxi", tostring(ctx.unitName))
  -- Simplified taxi instructions
  trigger.action.outTextForCoalition(ctx.coalitionID, "ATC Ground: Taxi to the runway and hold short. Contact tower for takeoff clearance.", 10, false)

  -- Record the starting point of the taxi for movement check
  captureTelemetry(ctx.unit)
  local t = telemetry[ctx.unitName]
  if t then
    p.taxiStartPoint = t.point
    logf("requestTaxi: stored taxiStartPoint for %s at (x=%.1f,z=%.1f)", ctx.unitName, t.point.x or 0, t.point.z or 0)
  end
end

requestTakeoff = function()
  local ctx = getPlayerContext(); if not ctx then return end
  local p = players[ctx.unitName]
  if not p then
    p = { coalitionID = ctx.coalitionID, unitID = ctx.unitID, airbaseName = nil, state = "not_started", engineStarted = false, hasTakenOff = false }
    players[ctx.unitName] = p
  end
  autoAssignHomeBase(ctx)
  -- If no home base is set yet, try to assign one but do not block takeoff
  if not p.airbaseName then
    autoAssignHomeBase(ctx)
  end
  -- Ensure the aircraft has moved away from the taxi starting point before takeoff
  captureTelemetry(ctx.unit)
  local tCurr = telemetry[ctx.unitName]
  if p.taxiStartPoint and tCurr and tCurr.point then
    local distMoved = planarDistanceMeters(p.taxiStartPoint, tCurr.point)
    if distMoved < 50 then
      trigger.action.outTextForCoalition(ctx.coalitionID, "ATC: Taxi to the runway before requesting takeoff.", 10, false)
      return
    end
  end
  if p.state ~= "on_taxi" then
    trigger.action.outTextForCoalition(ctx.coalitionID, "ATC: Not cleared for takeoff yet.", 10, false)
    return
  end
  local abName = p.airbaseName
  takeoffQueues[abName] = takeoffQueues[abName] or {}
  local q = takeoffQueues[abName]
  table.insert(q, ctx.unitName)
  local pos = #q
  logf("requestTakeoff: unit=%s queuedPos=%d at=%s", tostring(ctx.unitName), pos, tostring(abName))
  if pos == 1 then
    p.state = "take_off"
    trigger.action.outTextForCoalition(ctx.coalitionID, "ATC Tower: Cleared for takeoff. Fly runway heading. Contact tower for handoff.", 10, false)
  else
    trigger.action.outTextForCoalition(ctx.coalitionID, "ATC Tower: Hold short, you are number " .. pos .. " for takeoff.", 10, false)
  end
end

requestHandoff = function()
  local ctx = getPlayerContext(); if not ctx then return end
  local p = players[ctx.unitName]; if not p then return end
  if p.state ~= "take_off" then
    trigger.action.outTextForCoalition(ctx.coalitionID, "ATC: Not in takeoff state.", 10, false)
    return
  end
  -- Require the player to have left the runway before handoff (runway takeoff event).
  if not p.hasTakenOff then
    trigger.action.outTextForCoalition(ctx.coalitionID, "ATC: You have not taken off yet.", 10, false)
    return
  end
  logf("requestHandoff: unit=%s -> airborne", tostring(ctx.unitName))
  setAirborne(ctx.unitName)
end

-- Slasher check‑in command: free trigger after handoff
requestSlasherCheckIn = function()
  local ctx = getPlayerContext(); if not ctx then return end
  -- Slasher acknowledges check‑in and instructs player to fly their mission
  trigger.action.outTextForCoalition(ctx.coalitionID, "ATC Slasher: Check‑in acknowledged. Fly your planned mission.", 10, false)
end

setAirborne = function(unitName)
  local p = players[unitName]; if not p then return end
  local abName = p.airbaseName
  p.state = "airborne"
  p.airbaseName = nil
  p.hasTakenOff = false -- reset flag for next cycle
  p.taxiStartPoint = nil -- clear taxi start for next cycle
  logf("setAirborne: unit=%s departed=%s", tostring(unitName), tostring(abName))
  trigger.action.outTextForCoalition(p.coalitionID, "ATC Tower: Handoff acknowledged. Contact Slasher to check in.", 10, false)
  local q = takeoffQueues[abName]
  if q then
    for i, u in ipairs(q) do if u == unitName then table.remove(q, i) break end end
    if #q > 0 then
      local nextUnit = q[1]
      local nextP = players[nextUnit]
      if nextP then
        nextP.state = "take_off"
        trigger.action.outTextForCoalition(nextP.coalitionID, "ATC Tower: You are now cleared for takeoff.", 10, false)
        logf("setAirborne: next cleared=%s", tostring(nextUnit))
      end
    end
  end
end

requestInbound = function()
  local ctx = getPlayerContext(); if not ctx then return end
  local p = players[ctx.unitName] or { coalitionID = ctx.coalitionID, unitID = ctx.unitID, state = "airborne", engineStarted = true, hasTakenOff = true }
  players[ctx.unitName] = p
  if not p.airbaseName then
    local ab = nearestOwnedAirbase(ctx.unit, ctx.coalitionID)
    if ab then
      p.airbaseName = getAirbaseName(ab)
      trigger.action.outTextForCoalition(ctx.coalitionID, "ATC: Destination set to nearest owned: " .. p.airbaseName .. ".", 10, false)
    else
      trigger.action.outTextForCoalition(ctx.coalitionID, "ATC: No owned airbases to inbound to.", 10, false)
      return
    end
  end
  if p.state ~= "airborne" or not ctx.unit:inAir() then
    trigger.action.outTextForCoalition(ctx.coalitionID, "ATC: Not airborne or incorrect state.", 10, false)
    return
  end
  p.state = "in_bound"
  landingQueues[p.airbaseName] = landingQueues[p.airbaseName] or {}
  table.insert(landingQueues[p.airbaseName], ctx.unitName)
  logf("requestInbound: unit=%s dest=%s", tostring(ctx.unitName), tostring(p.airbaseName))
  -- Simplified inbound call
  trigger.action.outTextForCoalition(ctx.coalitionID, "ATC Slasher: Inbound acknowledged. Continue to base. Contact Slasher for approach clearance.", 10, false)
end

requestApproach = function()
  local ctx = getPlayerContext(); if not ctx then return end
  local p = players[ctx.unitName]; if not p or not p.airbaseName then return end
  if p.state ~= "in_bound" then
    trigger.action.outTextForCoalition(ctx.coalitionID, "ATC: Not in inbound state.", 10, false)
    return
  end
  local ab = Airbase.getByName(p.airbaseName)
  local d  = planarDistanceMeters(pointOf(ctx.unit), pointOf(ab))
  if d > 10 * 1852 then
    trigger.action.outTextForCoalition(ctx.coalitionID, "ATC: Too far for approach (current " .. string.format("%.1f", metersToNM(d)) .. " NM).", 10, false)
    return
  end
  p.state = "approach"
  logf("requestApproach: unit=%s -> approach (%s)", tostring(ctx.unitName), tostring(p.airbaseName))
  trigger.action.outTextForCoalition(ctx.coalitionID, "ATC Slasher: Approach cleared. Contact tower for landing clearance.", 10, false)
end

requestLanding = function()
  local ctx = getPlayerContext(); if not ctx then return end
  local p = players[ctx.unitName]; if not p or not p.airbaseName then return end
  if p.state ~= "approach" then
    trigger.action.outTextForCoalition(ctx.coalitionID, "ATC: Not in approach state.", 10, false)
    return
  end
  local q = landingQueues[p.airbaseName] or {}
  local pos = 0
  for i, u in ipairs(q) do if u == ctx.unitName then pos = i break end end
  logf("requestLanding: unit=%s queuePos=%d dest=%s", tostring(ctx.unitName), pos, tostring(p.airbaseName))
  if pos == 1 then
    trigger.action.outTextForCoalition(ctx.coalitionID, "ATC Tower: Cleared to land.", 10, false)
  else
    trigger.action.outTextForCoalition(ctx.coalitionID, "ATC Tower: Number " .. pos .. " for landing. Maintain pattern.", 10, false)
  end
end

requestTaxiToParking = function()
  local ctx = getPlayerContext(); if not ctx then return end
  local p = players[ctx.unitName]
  if not p then
    p = { coalitionID = ctx.coalitionID, unitID = ctx.unitID, airbaseName = nil, state = "landed", engineStarted = false, hasTakenOff = false }
    players[ctx.unitName] = p
  end
  -- Allow taxi to parking without state requirement
  p.state = "parked"
  logf("requestTaxiToParking: unit=%s -> parked", tostring(ctx.unitName))
  -- Simplified parking instructions
  trigger.action.outTextForCoalition(ctx.coalitionID, "ATC Ground: Taxi to parking. Contact ground when ready to shutdown.", 10, false)
end

requestShutdown = function()
  local ctx = getPlayerContext(); if not ctx then return end
  local p = players[ctx.unitName]
  if not p then
    p = { coalitionID = ctx.coalitionID, unitID = ctx.unitID, airbaseName = nil, state = "parked", engineStarted = false, hasTakenOff = false }
    players[ctx.unitName] = p
  end
  -- Allow shutdown at any time without state requirement
  logf("requestShutdown: unit=%s shutdown complete", tostring(ctx.unitName))
  trigger.action.outTextForCoalition(ctx.coalitionID, "ATC Ground: Cleared for shutdown. Good day.", 10, false)
end

---------------------------
-- Events & Timers
---------------------------
onEvent = function(event)
  local id = event.id
  local initiator = event.initiator
  local place = event.place
  local iname = initiator and (initiator.getName and initiator:getName()) or "<nil>"
  local pname = place and getAirbaseName(place) or "<nil>"
  logf("onEvent: id=%s initiator=%s place=%s", tostring(id), tostring(iname), tostring(pname))
  if id == world.event.S_EVENT_BIRTH then
    local unit = event.initiator
    if unit and unit.isExist and unit:isExist() and unit.getPlayerName and unit:getPlayerName() then
      local name = unit:getName()
      local coa  = unit:getCoalition()
      unitCoalitions[name] = coa
      ensureMenusForCoalition(coa)
      captureTelemetry(unit)
      players[name] = players[name] or { coalitionID = coa, unitID = unit:getID(), airbaseName = nil, state = "not_started", engineStarted = false, hasTakenOff = false }
      logf("BIRTH: player=%s coalition=%s", tostring(name), tostring(coa))
      -- Automatically assign nearest owned airbase using the spawning unit
      local p = players[name]
      local ab = nearestOwnedAirbase(unit, coa)
      if ab and p then
        p.airbaseName = getAirbaseName(ab)
        trigger.action.outTextForCoalition(coa, "ATC: Home airbase set to " .. p.airbaseName .. ".", 10, false)
        logf("autoAssignHomeBase: unit=%s assigned=%s", tostring(name), tostring(p.airbaseName))
      end
    end
  elseif id == world.event.S_EVENT_ENGINE_STARTUP then
    local unit = event.initiator
    if unit and unit.isExist and unit:isExist() and unit.getPlayerName and unit:getPlayerName() then
      local name = unit:getName()
      local p = players[name]
      if p then
        p.engineStarted = true
        logf("ENGINE_STARTUP: %s", tostring(name))
      end
    end
  elseif id == world.event.S_EVENT_RUNWAY_TAKEOFF then
    local unit = event.initiator
    if unit and unit.isExist and unit:isExist() and unit.getPlayerName and unit:getPlayerName() then
      local name = unit:getName()
      captureTelemetry(unit)
      local p = players[name]
      if p then
        p.hasTakenOff = true
        logf("RUNWAY_TAKEOFF: player=%s marked as taken off", tostring(name))
      end
      local placeName = place and getAirbaseName(place) or "unknown"
      logf("RUNWAY_TAKEOFF: %s from %s", tostring(name), tostring(placeName))
    end
  elseif id == world.event.S_EVENT_TAKEOFF then
    local unit = event.initiator
    if unit and unit.isExist and unit:isExist() and unit.getPlayerName and unit:getPlayerName() then
      captureTelemetry(unit)
      logf("TAKEOFF: %s", tostring(unit:getName()))
    end
  elseif id == world.event.S_EVENT_LAND then
    local unit = event.initiator
    if unit and unit.isExist and unit:isExist() and unit.getPlayerName and unit:getPlayerName() then
      local name = unit:getName()
      captureTelemetry(unit)
      local p = players[name]
      local placeName = place and getAirbaseName(place) or "unknown"
      if p and p.state == "approach" and place and p.airbaseName and placeName == p.airbaseName then
        p.state = "landed"
        trigger.action.outTextForCoalition(p.coalitionID, "ATC Tower: Landing noted. Contact ground for taxi to parking.", 10, false)
        local q = landingQueues[p.airbaseName]
        if q then
          for i, u in ipairs(q) do if u == name then table.remove(q, i) break end end
          if #q > 0 then
            local nextUnit = q[1]
            local nextP = players[nextUnit]
            if nextP then
              trigger.action.outTextForCoalition(nextP.coalitionID, "ATC Tower: You are now cleared to land.", 10, false)
              logf("LAND: cleared next=%s", tostring(nextUnit))
            end
          end
        end
      end
      logf("LAND: %s at %s", tostring(name), tostring(placeName))
    end
  end
end

periodicApproachTick = function()
  local ctx = getPlayerContext()
  if ctx then
    captureTelemetry(ctx.unit)
    local p = players[ctx.unitName]
    if p and p.state == "in_bound" and p.airbaseName then
      local ab = Airbase.getByName(p.airbaseName)
      local d  = planarDistanceMeters(pointOf(ctx.unit), pointOf(ab))
      if d <= 10 * 1852 then
        p.state = "approach"
        logf("tick: state -> approach for %s", tostring(ctx.unitName))
        trigger.action.outTextForCoalition(p.coalitionID, "ATC: Entering approach phase.", 10, false)
      end
    end

    -- Detect takeoff based on speed if the runway takeoff event is not fired
    for unitName, playerData in pairs(players) do
      if playerData.state == "take_off" and not playerData.hasTakenOff then
        local t = telemetry[unitName]
        if t and t.speed_mps then
          local threshold = 90
          local okUnit, unitObj = pcall(Unit.getByName, unitName)
          if okUnit and unitObj and isHelicopter(unitObj) then
            threshold = 25 -- ~50 knots
          end
          if t.speed_mps > threshold then
            playerData.hasTakenOff = true
            logf("speed check: %s speed=%.1f m/s marked as taken off", unitName, t.speed_mps)
          end
        end
      end
    end
  end
  return timer.getTime() + 30
end

retryAddMenus = function()
  -- Ensure BLUE/RED/NEUTRAL have menus
  local ids = getActiveCoalitionIDs()
  for i = 1, #ids do
    local coa = ids[i]
    if not (menuPaths[coa] and menuPaths[coa].root) then
      ensureMenusForCoalition(coa)
    end
  end
  return timer.getTime() + 10
end

---------------------------
-- Init
---------------------------
logf("Script loaded at %.1f", now())

-- Build menus early for BLUE/RED/NEUTRAL
local ids = getActiveCoalitionIDs()
for i = 1, #ids do
  ensureMenusForCoalition(ids[i])
end

world.addEventHandler({ onEvent = onEvent })
timer.scheduleFunction(periodicApproachTick, {}, timer.getTime() + 30)
timer.scheduleFunction(retryAddMenus,        {}, timer.getTime() + 5)
