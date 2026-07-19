-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- MIST compatibility shim for DCS Retribution
--
-- Goal: retire the ~9,500-line mist_4_5_126.lua by providing the *exact* subset of
-- the `mist` API that the shipped plugins actually call (51 distinct symbols across
-- the base glue (dcs_retribution.lua, land_relocate/water_relocate), CTLD, EWRS,
-- the EW jammer script, dismounts, Pretense, and Skynet-IADS), so every consumer
-- stays byte-for-byte unchanged.
--
-- IMPLEMENTATION: entirely vanilla DCS (coalition, Group, Unit, land, trigger, world, timer, env,
-- coord, math, string) with MIST behavior replicated verbatim. It has NO MOOSE dependency, so it
-- occupies mist's existing (first) work-order slot in base/plugin.json with NO reordering.
--
-- Lua 5.1 only. Define before first use. Behavior is replicated from the MIST
-- source (semantics matter -- a subtly-wrong vector/distance silently breaks a
-- consumer at runtime, not parse time). Contract pinned by tests/lua/test_mist_shim_*.py:
-- every symbol a shipped plugin calls must resolve and behave; a future plugin
-- calling a mist.* symbol the shim lacks fails the symbol-contract test instead
-- of dying silently in the mission.
-------------------------------------------------------------------------------------------------------------------------------------------------------------

mist = mist or {}
mist.utils = mist.utils or {}
mist.vec = mist.vec or {}
mist.ground = mist.ground or {}
mist.DBs = mist.DBs or {}
mist.message = mist.message or {}
mist.marker = mist.marker or {}

---------------------------------------------------------------------------------------------------
-- Tier 1a -- vectors (replicated verbatim from mist_4_5_126.lua; DCS Vec3 = {x, y, z}, y = altitude)
---------------------------------------------------------------------------------------------------

function mist.vec.sub(vec1, vec2)
    return { x = vec1.x - vec2.x, y = vec1.y - vec2.y, z = vec1.z - vec2.z }
end

function mist.vec.dp(vec1, vec2)
    return vec1.x * vec2.x + vec1.y * vec2.y + vec1.z * vec2.z
end

function mist.vec.mag(vec)
    return (vec.x ^ 2 + vec.y ^ 2 + vec.z ^ 2) ^ 0.5
end

function mist.vec.cp(vec1, vec2)
    return {
        x = vec1.y * vec2.z - vec1.z * vec2.y,
        y = vec1.z * vec2.x - vec1.x * vec2.z,
        z = vec1.x * vec2.y - vec1.y * vec2.x,
    }
end

---------------------------------------------------------------------------------------------------
-- Tier 1a -- scalar / unit conversions
---------------------------------------------------------------------------------------------------

function mist.utils.round(num, idp)
    local mult = 10 ^ (idp or 0)
    return math.floor(num * mult + 0.5) / mult
end

function mist.utils.toDegree(angle)
    return angle * 180 / math.pi
end

function mist.utils.metersToNM(meters)
    return meters / 1852
end

function mist.utils.metersToFeet(meters)
    return meters / 0.3048
end

function mist.utils.mpsToKmph(mps)
    return mps * 3.6
end

function mist.utils.mpsToKnots(mps)
    return mps * 3600 / 1852
end

---------------------------------------------------------------------------------------------------
-- Tier 1a -- vector constructors (note MIST's axis remap: Vec2.y carries Vec3.z)
---------------------------------------------------------------------------------------------------

function mist.utils.makeVec2(vec)
    if vec.z then
        return { x = vec.x, y = vec.z }
    else
        return { x = vec.x, y = vec.y } -- was already a Vec2
    end
end

function mist.utils.makeVec3(vec, y)
    if not vec.z then
        if vec.alt and not y then
            y = vec.alt
        elseif not y then
            y = 0
        end
        return { x = vec.x, y = y, z = vec.y }
    else
        return { x = vec.x, y = vec.y, z = vec.z } -- was already a Vec3
    end
end

function mist.utils.makeVec3GL(vec, offset)
    local adj = offset or 0
    if not vec.z then
        return { x = vec.x, y = land.getHeight(vec) + adj, z = vec.y }
    else
        return { x = vec.x, y = land.getHeight({ x = vec.x, y = vec.z }) + adj, z = vec.z }
    end
end

---------------------------------------------------------------------------------------------------
-- Tier 1a -- distances (defined after makeVec3 / vec.mag, which they use)
---------------------------------------------------------------------------------------------------

function mist.utils.get2DDist(point1, point2)
    point1 = mist.utils.makeVec3(point1)
    point2 = mist.utils.makeVec3(point2)
    return mist.vec.mag({ x = point1.x - point2.x, y = 0, z = point1.z - point2.z })
end

function mist.utils.get3DDist(point1, point2)
    return mist.vec.mag({
        x = point1.x - point2.x,
        y = point1.y - point2.y,
        z = point1.z - point2.z,
    })
end

---------------------------------------------------------------------------------------------------
-- Tier 1a -- deep copy (recursive table copy, preserves metatable, like MIST's deepCopy)
---------------------------------------------------------------------------------------------------

function mist.utils.deepCopy(object)
    local lookup_table = {}
    local function _copy(obj)
        if type(obj) ~= "table" then
            return obj
        elseif lookup_table[obj] then
            return lookup_table[obj]
        end
        local new_table = {}
        lookup_table[obj] = new_table
        for index, value in pairs(obj) do
            new_table[_copy(index)] = _copy(value)
        end
        return setmetatable(new_table, getmetatable(obj))
    end
    return _copy(object)
end

---------------------------------------------------------------------------------------------------
-- Tier 1b -- geo / coordinate helpers (replicated from mist_4_5_126.lua unless noted)
-- Defined before first use: getNorthCorrection -> getHeading/getDir -> getHeadingPoints.
---------------------------------------------------------------------------------------------------

-- True-north correction at a point (internal helper used by getHeading / getDir).
function mist.getNorthCorrection(gPoint)
    local point = mist.utils.deepCopy(gPoint)
    if not point.z then -- Vec2 -> Vec3
        point.z = point.y
        point.y = 0
    end
    local lat, lon = coord.LOtoLL(point)
    local north_posit = coord.LLtoLO(lat + 1, lon)
    return math.atan2(north_posit.z - point.z, north_posit.x - point.x)
end

function mist.getHeading(unit, rawHeading)
    local unitpos = unit:getPosition()
    if unitpos then
        local heading = math.atan2(unitpos.x.z, unitpos.x.x)
        if not rawHeading then
            heading = heading + mist.getNorthCorrection(unitpos.p)
        end
        if heading < 0 then
            heading = heading + 2 * math.pi
        end
        return heading
    end
end

function mist.getPitch(unit)
    local unitpos = unit:getPosition()
    if unitpos then
        return math.asin(unitpos.x.y)
    end
end

function mist.getRoll(unit)
    local unitpos = unit:getPosition()
    if unitpos then
        -- perpendicular to world-up and the nose vector, dotted against the
        -- right-wing vector; sign convention: right roll positive.
        local cp = mist.vec.cp(unitpos.x, { x = 0, y = 1, z = 0 })
        local dp = mist.vec.dp(cp, unitpos.z)
        local roll = math.acos(dp / (mist.vec.mag(cp) * mist.vec.mag(unitpos.z)))
        if unitpos.z.y > 0 then -- left roll, flip the sign
            roll = -roll
        end
        return roll
    end
end

function mist.utils.getDir(vec, point)
    local dir = math.atan2(vec.z, vec.x)
    if point then
        dir = dir + mist.getNorthCorrection(point)
    end
    if dir < 0 then
        dir = dir + 2 * math.pi
    end
    return dir
end

function mist.utils.getHeadingPoints(point1, point2, north)
    if north then
        -- MIST's original passes makeVec3(point1) here; get3DDist takes two
        -- points and would index nil (a latent runtime death for the first
        -- upstream Lua merge that passes the north flag).
        local p1 = mist.utils.makeVec3(point1)
        return mist.utils.getDir(mist.vec.sub(mist.utils.makeVec3(point2), p1), p1)
    else
        return mist.utils.getDir(mist.vec.sub(mist.utils.makeVec3(point2), mist.utils.makeVec3(point1)))
    end
end

function mist.getAvgPos(unitNames)
    local avgX, avgY, avgZ, totNum = 0, 0, 0, 0
    for i = 1, #unitNames do
        local unit
        if Unit.getByName(unitNames[i]) then
            unit = Unit.getByName(unitNames[i])
        elseif StaticObject.getByName(unitNames[i]) then
            unit = StaticObject.getByName(unitNames[i])
        end
        if unit and unit:isExist() == true then
            local pos = unit:getPosition().p
            if pos then
                avgX = avgX + pos.x
                avgY = avgY + pos.y
                avgZ = avgZ + pos.z
                totNum = totNum + 1
            end
        end
    end
    if totNum ~= 0 then
        return { x = avgX / totNum, y = avgY / totNum, z = avgZ / totNum }
    end
end

function mist.getLeadPos(group)
    local gObj
    if type(group) == "string" then
        gObj = Group.getByName(group)
    elseif type(group) == "table" then
        gObj = group
    end
    if gObj then
        local units = gObj:getUnits()
        local leader = units[1]
        if leader then
            if Unit.isExist(leader) then
                return leader:getPoint()
            elseif #units > 1 then
                for i = 2, #units do
                    if Unit.isExist(units[i]) then
                        return units[i]:getPoint()
                    end
                end
            end
        end
    end
end

function mist.utils.zoneToVec3(zone, gl)
    local new = {}
    if type(zone) == "table" then
        if zone.point then
            new.x = zone.point.x
            new.y = zone.point.y
            new.z = zone.point.z
        elseif zone.x and zone.y and zone.z then
            new = mist.utils.deepCopy(zone)
        end
        return new
    elseif type(zone) == "string" then
        zone = trigger.misc.getZone(zone)
        if zone then
            new.x = zone.point.x
            new.y = zone.point.y
            new.z = zone.point.z
        end
    end
    if new.x and gl then
        new.y = land.getHeight({ x = new.x, y = new.z })
    end
    return new
end

function mist.terrainHeightDiff(coordArg, searchSize)
    local searchRadius = searchSize or 5
    if type(coordArg) == "string" then
        coordArg = mist.utils.zoneToVec3(coordArg)
    end
    coordArg = mist.utils.makeVec2(coordArg)
    local samples = {}
    samples[#samples + 1] = land.getHeight(coordArg)
    for i = 0, 360, 30 do
        samples[#samples + 1] = land.getHeight({
            x = coordArg.x + (math.sin(math.rad(i)) * searchRadius),
            y = coordArg.y + (math.cos(math.rad(i)) * searchRadius),
        })
        if searchRadius >= 20 then
            samples[#samples + 1] = land.getHeight({
                x = coordArg.x + (math.sin(math.rad(i)) * (searchRadius / 2)),
                y = coordArg.y + (math.cos(math.rad(i)) * (searchRadius / 2)),
            })
        end
    end
    local tMax, tMin = samples[1], samples[1]
    for _, height in pairs(samples) do
        if height > tMax then tMax = height end
        if height < tMin then tMin = height end
    end
    return mist.utils.round(tMax - tMin, 2)
end

-- Anti-clustering random over an integer range (MIST semantics).
function mist.random(firstNum, secondNum)
    local lowNum, highNum
    if not secondNum then
        highNum = firstNum
        lowNum = 1
    else
        lowNum = firstNum
        highNum = secondNum
    end
    local total = 1
    if math.abs(highNum - lowNum + 1) < 50 then
        total = math.modf(50 / math.abs(highNum - lowNum + 1))
    end
    local choices = {}
    for _ = 1, total do
        for x = lowNum, highNum do
            choices[#choices + 1] = x
        end
    end
    local rtnVal = math.random(#choices)
    for _ = 1, 10 do
        rtnVal = math.random(#choices)
    end
    return choices[rtnVal]
end

function mist.getRandPointInCircle(p, r, innerRadius, maxA, minA)
    local point = mist.utils.makeVec3(p)
    local theta = 2 * math.pi * math.random()
    local radius = r or 1000
    local minR = innerRadius or 0
    if maxA and not minA then
        theta = math.rad(math.random(0, maxA - math.random()))
    elseif maxA and minA then
        if minA < maxA then
            theta = math.rad(math.random(minA, maxA) - math.random())
        else
            theta = math.rad(math.random(maxA, minA) - math.random())
        end
    end
    local rad = math.random() + math.random()
    if rad > 1 then
        rad = 2 - rad
    end
    local radMult
    if minR and minR <= radius then
        radMult = radius * math.sqrt((minR ^ 2 + (radius ^ 2 - minR ^ 2) * math.random()) / radius ^ 2)
    else
        radMult = radius * rad
    end
    local rndCoord
    if radius > 0 then
        rndCoord = { x = math.cos(theta) * radMult + point.x, y = math.sin(theta) * radMult + point.z }
    else
        rndCoord = { x = point.x, y = point.z }
    end
    return rndCoord
end

-- Ray-casting point-in-polygon (replicated verbatim; poly = array of Vec2/Vec3).
function mist.pointInPolygon(point, poly, maxalt)
    point = mist.utils.makeVec3(point)
    local px = point.x
    local pz = point.z
    local cn = 0
    local newpoly = mist.utils.deepCopy(poly)
    if not maxalt or (point.y <= maxalt) then
        local polysize = #newpoly
        newpoly[#newpoly + 1] = newpoly[1]
        newpoly[1] = mist.utils.makeVec3(newpoly[1])
        for k = 1, polysize do
            newpoly[k + 1] = mist.utils.makeVec3(newpoly[k + 1])
            if ((newpoly[k].z <= pz) and (newpoly[k + 1].z > pz))
                or ((newpoly[k].z > pz) and (newpoly[k + 1].z <= pz)) then
                local vt = (pz - newpoly[k].z) / (newpoly[k + 1].z - newpoly[k].z)
                if px < newpoly[k].x + vt * (newpoly[k + 1].x - newpoly[k].x) then
                    cn = cn + 1
                end
            end
        end
        return cn % 2 == 1
    else
        return false
    end
end

function mist.getAvgPoint(points)
    local avgX, avgY, avgZ, tot = 0, 0, 0, 0
    for i = 1, #points do
        local p = mist.utils.makeVec3(points[i])
        avgX = avgX + p.x
        avgY = avgY + p.y
        avgZ = avgZ + p.z
        tot = tot + 1
    end
    if tot > 0 then
        return { x = avgX / tot, y = avgY / tot, z = avgZ / tot }
    end
end

-- Random point inside a quad/freeform zone: rejection-sample the bounding
-- circle (MIST's own 100-try approach, warning on fallback).
function mist.getRandomPointInPoly(zone)
    local avg = mist.getAvgPoint(zone)
    local radius = 0
    local newCoord = {}
    for i = 1, #zone do
        local d = mist.utils.get2DDist(avg, zone[i])
        if d > radius then
            radius = d
        end
    end
    for j = 1, 100 do
        newCoord = mist.getRandPointInCircle(avg, radius)
        if mist.pointInPolygon(newCoord, zone) then
            break
        end
        if j == 100 then
            newCoord = mist.getRandPointInCircle(avg, radius)
            env.warning("mist shim: getRandomPointInPoly gave up; random point from poly center")
        end
    end
    return newCoord
end

-- Random point in a named ME trigger zone; quad zones (type 2) sample the
-- polygon, circular zones the radius (MIST semantics).
function mist.getRandomPointInZone(zoneName, innerRadius, maxA, minA)
    if type(zoneName) == "string" then
        local zone = mist.DBs.zonesByName[zoneName]
        if not zone then
            return false
        end
        if zone.type and zone.type == 2 and zone.verticies then
            return mist.getRandomPointInPoly(zone.verticies)
        end
        return mist.getRandPointInCircle(zone.point, zone.radius, innerRadius, maxA, minA)
    end
    return false
end

-- Consumers pass raw DCS mark panel ids (world.getMarkPanels entries / the
-- MARK_* event id); full MIST resolves its own marker ledger first, but a
-- panel id ends at the same trigger.action.removeMark either way.
function mist.marker.remove(id)
    if id == nil then
        return false
    end
    trigger.action.removeMark(id)
    return true
end

---------------------------------------------------------------------------------------------------
-- Tier 1b -- coordinate string formatting
---------------------------------------------------------------------------------------------------

-- MGRS table (from coord.LLtoMGRS) -> string. Replicated verbatim from MIST.
function mist.tostringMGRS(MGRS, acc)
    if acc == 0 then
        return MGRS.UTMZone .. " " .. MGRS.MGRSDigraph
    else
        return MGRS.UTMZone .. " " .. MGRS.MGRSDigraph
            .. " " .. string.format("%0" .. acc .. "d", mist.utils.round(MGRS.Easting / (10 ^ (5 - acc)), 0))
            .. " " .. string.format("%0" .. acc .. "d", mist.utils.round(MGRS.Northing / (10 ^ (5 - acc)), 0))
    end
end

-- LL formatting, replicated verbatim from MIST. (Originally delegated to MOOSE UTILS.tostringLL,
-- but inlining it keeps the shim free of ANY MOOSE dependency -> it can load in mist's existing
-- slot with no plugin.json reordering.)
function mist.tostringLL(lat, lon, acc, DMS)
    local latHemi, lonHemi
    if lat > 0 then latHemi = "N" else latHemi = "S" end
    if lon > 0 then lonHemi = "E" else lonHemi = "W" end
    lat = math.abs(lat)
    lon = math.abs(lon)
    local latDeg = math.floor(lat)
    local latMin = (lat - latDeg) * 60
    local lonDeg = math.floor(lon)
    local lonMin = (lon - lonDeg) * 60
    if DMS then
        local oldLatMin = latMin
        latMin = math.floor(latMin)
        local latSec = mist.utils.round((oldLatMin - latMin) * 60, acc)
        local oldLonMin = lonMin
        lonMin = math.floor(lonMin)
        local lonSec = mist.utils.round((oldLonMin - lonMin) * 60, acc)
        if latSec == 60 then latSec = 0 latMin = latMin + 1 end
        if lonSec == 60 then lonSec = 0 lonMin = lonMin + 1 end
        local secFrmtStr
        if acc <= 0 then
            secFrmtStr = "%02d"
        else
            secFrmtStr = "%0" .. (3 + acc) .. "." .. acc .. "f"
        end
        return string.format("%02d", latDeg) .. " " .. string.format("%02d", latMin) .. "' "
            .. string.format(secFrmtStr, latSec) .. "\"" .. latHemi .. "\t "
            .. string.format("%02d", lonDeg) .. " " .. string.format("%02d", lonMin) .. "' "
            .. string.format(secFrmtStr, lonSec) .. "\"" .. lonHemi
    else
        latMin = mist.utils.round(latMin, acc)
        lonMin = mist.utils.round(lonMin, acc)
        if latMin == 60 then latMin = 0 latDeg = latDeg + 1 end
        if lonMin == 60 then lonMin = 0 lonDeg = lonDeg + 1 end
        local minFrmtStr
        if acc <= 0 then
            minFrmtStr = "%02d"
        else
            minFrmtStr = "%0" .. (3 + acc) .. "." .. acc .. "f"
        end
        return string.format("%02d", latDeg) .. " " .. string.format(minFrmtStr, latMin) .. "'" .. latHemi .. "\t "
            .. string.format("%02d", lonDeg) .. " " .. string.format(minFrmtStr, lonMin) .. "'" .. lonHemi
    end
end

---------------------------------------------------------------------------------------------------
-- Tier 1b -- line-of-sight (only reached by CTLD JTAC autolase, which is DISABLED in Retribution;
-- compact best-effort impl over land.isVisible so the symbol is never nil).
---------------------------------------------------------------------------------------------------

function mist.getUnitsLOS(unitset1, altoffset1, unitset2, altoffset2, radius)
    radius = radius or math.huge
    altoffset1 = altoffset1 or 0
    altoffset2 = altoffset2 or 0
    local function collect(names)
        local out = {}
        for i = 1, #names do
            local u = Unit.getByName(names[i])
            if u and u:isExist() == true then
                out[#out + 1] = { unit = u, pos = u:getPosition().p }
            end
        end
        return out
    end
    local info1, info2 = collect(unitset1), collect(unitset2)
    local los = {}
    for _, a in ipairs(info1) do
        for _, b in ipairs(info2) do
            local pa = { x = a.pos.x, y = a.pos.y + altoffset1, z = a.pos.z }
            local pb = { x = b.pos.x, y = b.pos.y + altoffset2, z = b.pos.z }
            if mist.utils.get3DDist(pa, pb) <= radius and land.isVisible(pa, pb) then
                los[#los + 1] = { from = a.unit, to = b.unit }
            end
        end
    end
    return los
end

---------------------------------------------------------------------------------------------------
-- Tier 1b -- debug table serializer (mist.utils.tableShow). Debug-only; format need not match MIST.
---------------------------------------------------------------------------------------------------

function mist.utils.tableShow(tbl, loc, indent, tableshow_tbls)
    tableshow_tbls = tableshow_tbls or {}
    indent = indent or ""
    if type(tbl) ~= "table" then
        return tostring(tbl)
    end
    if tableshow_tbls[tbl] then
        return tostring(tbl) .. " (recursion)"
    end
    tableshow_tbls[tbl] = true
    local out = "{\n"
    for k, v in pairs(tbl) do
        local key
        if type(k) == "number" then
            key = "[" .. k .. "]"
        else
            key = "[\"" .. tostring(k) .. "\"]"
        end
        out = out .. indent .. "  " .. key .. " = "
        if type(v) == "table" then
            out = out .. mist.utils.tableShow(v, loc, indent .. "  ", tableshow_tbls)
        elseif type(v) == "string" then
            out = out .. "\"" .. v .. "\""
        else
            out = out .. tostring(v)
        end
        out = out .. ",\n"
    end
    out = out .. indent .. "}"
    return out
end

---------------------------------------------------------------------------------------------------
-- Tier 2 -- object database (mist.DBs.*)
--
-- Verified against consumer source: the entries are barely read --
--   * pairs(unitsByName) / pairs(groupsByName): only the KEY is used (value re-fetched via
--     Unit.getByName / Group.getByName), so entry values can be minimal.
--   * unitsById[id]: only .groupId.   * zonesByName[name]: only .point (Vec3).
--   * humansByName[name]: existence + a mutable .losMarkIds (CTLD JTAC autolase, disabled).
-- DCS Lua 5.1 has no __pairs, so these must be REAL tables. We rebuild them on a periodic scan of
-- coalition.getGroups (cheap; mirrors MIST's own DB cadence). Zones are static -> built once.
---------------------------------------------------------------------------------------------------

mist.DBs.unitsByName = mist.DBs.unitsByName or {}
mist.DBs.unitsById = mist.DBs.unitsById or {}
mist.DBs.groupsByName = mist.DBs.groupsByName or {}
-- groupsById[id]: only .groupName is read (the escort leash's id->name fallback,
-- upstream #850 -- merged 2026-07-10; the U1 "grep upstream Lua for mist." rule).
mist.DBs.groupsById = mist.DBs.groupsById or {}
mist.DBs.humansByName = mist.DBs.humansByName or {}
mist.DBs.zonesByName = mist.DBs.zonesByName or {}

-- Refresh cadence. The DBs used to rebuild on a flat 5 s whole-mission scan -- the single
-- heaviest standing poll in the plugin stack on a dense mission (every group of every side and
-- category, every 5 s, all mission long). New groups now trigger their own rebuild via
-- S_EVENT_BIRTH (debounced, below), so the periodic pass only bounds staleness for *removals*
-- (dead/despawned entries linger up to one period) -- and every consumer re-fetches by name via
-- Group.getByName/Unit.getByName anyway (see the shim notes: only the key set matters), so a
-- stale entry is skipped, never acted on.
local _MIST_DB_REFRESH = 30 -- seconds between fallback unit/group DB refreshes
local _MIST_DB_BIRTH_DEBOUNCE = 2 -- seconds to coalesce a burst of births into one rebuild

local function _mistBuildZones()
    local zones = {}
    if env and env.mission and env.mission.triggers and env.mission.triggers.zones then
        for _, z in pairs(env.mission.triggers.zones) do
            local gl = 0
            pcall(function() gl = land.getHeight({ x = z.x, y = z.y }) end)
            zones[z.name] = {
                name = z.name,
                point = { x = z.x, y = gl, z = z.y },
                radius = z.radius,
                type = z.type,
                verticies = z.verticies,
            }
        end
    end
    mist.DBs.zonesByName = zones
end

local function _mistRefreshDBs()
    local unitsByName, unitsById, groupsByName, humansByName = {}, {}, {}, {}
    local groupsById = {}
    local sides = { coalition.side.NEUTRAL, coalition.side.RED, coalition.side.BLUE }
    local cats = {
        Group.Category.AIRPLANE,
        Group.Category.HELICOPTER,
        Group.Category.GROUND,
        Group.Category.SHIP,
    }
    for _, side in pairs(sides) do
        for _, cat in pairs(cats) do
            local ok, groups = pcall(coalition.getGroups, side, cat)
            if ok and groups then
                for _, grp in pairs(groups) do
                    if grp and grp:isExist() then
                        local gname = grp:getName()
                        local gid = grp:getID()
                        groupsByName[gname] = { groupName = gname, groupId = gid }
                        local ngid = tonumber(gid)
                        if ngid then
                            groupsById[ngid] = groupsByName[gname]
                        end
                        for _, u in pairs(grp:getUnits()) do
                            if u and u:isExist() then
                                local uname = u:getName()
                                local entry = { unitName = uname, groupName = gname, groupId = gid }
                                unitsByName[uname] = entry
                                local okid, uid = pcall(function() return u:getID() end)
                                if okid and uid then
                                    unitsById[tonumber(uid)] = entry
                                end
                                local pname
                                pcall(function() pname = u:getPlayerName() end)
                                if pname then
                                    local prev = mist.DBs.humansByName[uname]
                                    humansByName[uname] = {
                                        unitName = uname,
                                        groupName = gname,
                                        groupId = gid,
                                        playerName = pname,
                                        losMarkIds = prev and prev.losMarkIds or nil,
                                    }
                                end
                            end
                        end
                    end
                end
            end
        end
    end
    mist.DBs.unitsByName = unitsByName
    mist.DBs.unitsById = unitsById
    mist.DBs.groupsByName = groupsByName
    mist.DBs.groupsById = groupsById
    mist.DBs.humansByName = humansByName
end

local function _mistDBLoop()
    _mistRefreshDBs()
    return timer.getTime() + _MIST_DB_REFRESH
end

-- Birth-driven refresh: a late-spawned group (QRA intercept clones, Combat SAR, CTLD, Super
-- Gaggle, a player slotting in) fires S_EVENT_BIRTH per unit; one debounced rebuild picks the
-- whole burst up within _MIST_DB_BIRTH_DEBOUNCE seconds -- faster than the old flat 5 s scan
-- ever guaranteed, at a fraction of the standing cost.
local _mistDBRefreshPending = false

local _mistBirthHandler = {}
function _mistBirthHandler:onEvent(event)
    if not event or event.id ~= world.event.S_EVENT_BIRTH then
        return
    end
    if _mistDBRefreshPending then
        return
    end
    _mistDBRefreshPending = true
    timer.scheduleFunction(function()
        _mistDBRefreshPending = false
        local ok, err = pcall(_mistRefreshDBs)
        if not ok then
            env.warning("mist shim: birth-triggered DB refresh error: " .. tostring(err))
        end
        return nil
    end, nil, timer.getTime() + _MIST_DB_BIRTH_DEBOUNCE)
end

-- Initial population + birth-driven refresh + periodic fallback. Safe at load:
-- coalition.getGroups, world.addEventHandler, env.mission and timer.* are all available at
-- mission start; the shim loads before any consumer reads mist.DBs.
_mistBuildZones()
_mistRefreshDBs()
world.addEventHandler(_mistBirthHandler)
timer.scheduleFunction(_mistDBLoop, nil, timer.getTime() + _MIST_DB_REFRESH)

-- Mission-editor group DB for mist.getGroupData (land_relocate/water_relocate). Unlike the live
-- DBs above, this reads the *mission table* (env.mission) so the returned entry carries the full
-- spawnable definition (units with type/x/y/heading/skill/name, route, country, category) that
-- mist.dynAdd can re-add under the same names. Built lazily on first call: env.mission is static,
-- so one build serves the whole mission. Names go through env.getValueDictByKey, which returns
-- plain strings unchanged and resolves DictKey_* entries from hand-built .miz files.
local _mistMEGroups = nil

local function _mistResolveName(s)
    if type(s) == "string" and env.getValueDictByKey then
        local ok, v = pcall(env.getValueDictByKey, s)
        if ok and v ~= nil then
            return v
        end
    end
    return s
end

local function _mistBuildMEGroups()
    _mistMEGroups = {}
    if not (env and env.mission and env.mission.coalition) then
        return
    end
    for _, coa in pairs(env.mission.coalition) do
        if type(coa) == "table" and type(coa.country) == "table" then
            for _, cntry in pairs(coa.country) do
                for _, catName in pairs({ "vehicle", "ship", "plane", "helicopter" }) do
                    local cat = cntry[catName]
                    if type(cat) == "table" and type(cat.group) == "table" then
                        for _, grp in pairs(cat.group) do
                            local name = _mistResolveName(grp.name)
                            if name then
                                local entry = mist.utils.deepCopy(grp)
                                entry.name = name
                                entry.groupName = name
                                entry.country = cntry.id
                                entry.countryId = cntry.id
                                entry.category = catName
                                if type(entry.units) == "table" then
                                    for _, u in pairs(entry.units) do
                                        u.name = _mistResolveName(u.name)
                                    end
                                end
                                _mistMEGroups[name] = entry
                            end
                        end
                    end
                end
            end
        end
    end
end

-- MIST-shaped group definition by group name, or nil for a name the mission table doesn't
-- know (e.g. a group spawned at runtime). Returns a fresh deep copy so callers may mutate it.
function mist.getGroupData(gpName)
    if _mistMEGroups == nil then
        _mistBuildMEGroups()
    end
    local entry = _mistMEGroups[gpName]
    if not entry then
        return nil
    end
    return mist.utils.deepCopy(entry)
end

-- Route points of a mission-editor group, by name or groupId (MIST shape:
-- each entry {x, y} unless the ME moved to point = Vec2 notation).
function mist.getGroupPoints(groupIdent)
    if _mistMEGroups == nil then
        _mistBuildMEGroups()
    end
    local entry
    if type(groupIdent) == "string" and not tonumber(groupIdent) then
        entry = _mistMEGroups[groupIdent]
    else
        local wanted = tonumber(groupIdent)
        for _, e in pairs(_mistMEGroups) do
            if tonumber(e.groupId) == wanted then
                entry = e
                break
            end
        end
    end
    if not (entry and entry.route and entry.route.points and #entry.route.points > 0) then
        return
    end
    local points = {}
    for num, point in pairs(entry.route.points) do
        if not point.point then
            points[num] = { x = point.x, y = point.y }
        else
            points[num] = point.point
        end
    end
    return points
end

---------------------------------------------------------------------------------------------------
-- Tier 3 (sched/events/wp) + Tier 4 (msg/log). The complex live spawn/route functions
-- (dynAdd, dynAddStatic, goRoute, getGroupRoute, groupToRandomZone, makeUnitTable) are done in a
-- dedicated pass -- they need per-function fidelity (CTLD crate spawning, SCAR/skynet movement).
---------------------------------------------------------------------------------------------------

-- internal helper used by ground.buildWP (not consumer-facing)
function mist.utils.kmphToMps(kmph)
    return kmph * 1000 / 3600
end

local _mistTasks = {} -- mist taskId -> DCS scheduler id
local _mistNextTaskId = 0

-- Run f(unpack(vars)) at time t; if rep, repeat every rep s; if st, stop after st.
-- Returns an id usable with mist.removeFunction. Backed by vanilla timer.scheduleFunction.
function mist.scheduleFunction(f, vars, t, rep, st)
    vars = vars or {}
    _mistNextTaskId = _mistNextTaskId + 1
    local myId = _mistNextTaskId
    local function run(_, now)
        if st and now >= st then
            _mistTasks[myId] = nil
            return nil
        end
        local ok, err = pcall(f, unpack(vars))
        if not ok then
            -- Real MIST surfaces scheduled-function errors in dcs.log; a silent
            -- swallow here is the "feature never starts, zero log signal" class.
            env.warning("mist shim: scheduled function error: " .. tostring(err))
        end
        if rep then
            return now + rep
        end
        _mistTasks[myId] = nil
        return nil
    end
    _mistTasks[myId] = timer.scheduleFunction(run, nil, t)
    return myId
end

function mist.removeFunction(id)
    local dcsId = _mistTasks[id]
    if dcsId then
        pcall(timer.removeFunction, dcsId)
        _mistTasks[id] = nil
        return true
    end
    return false
end

local _mistNextEventId = 0
function mist.addEventHandler(f)
    _mistNextEventId = _mistNextEventId + 1
    local handler = { id = _mistNextEventId, f = f }
    function handler:onEvent(event)
        self.f(event)
    end
    world.addEventHandler(handler)
    return handler.id
end

-- msg = { text, displayTime, msgFor = { coa = {...} } }. Retribution only broadcasts to all.
function mist.message.add(msg)
    if not msg or not msg.text then
        return
    end
    trigger.action.outText(tostring(msg.text), msg.displayTime or 20)
end

-- mist.Logger:new(name, level) -> logger with :info/:warn/:error/:alert. Retribution passes
-- pre-formatted strings (no $1 substitution), so these are thin env.* wrappers.
mist.Logger = mist.Logger or {}
mist.Logger.__index = mist.Logger
function mist.Logger:new(name, level)
    return setmetatable({ name = name or "", level = level }, mist.Logger)
end
function mist.Logger:info(msg)
    env.info((self.name or "") .. "|" .. tostring(msg))
end
function mist.Logger:warn(msg)
    env.warning((self.name or "") .. "|" .. tostring(msg))
end
function mist.Logger:error(msg)
    env.error((self.name or "") .. "|" .. tostring(msg))
end
function mist.Logger:alert(msg)
    env.error((self.name or "") .. "|" .. tostring(msg))
end

function mist.ground.buildWP(point, overRideForm, overRideSpeed)
    local wp = {}
    wp.x = point.x
    if point.z then
        wp.y = point.z
    else
        wp.y = point.y
    end
    local form
    if point.speed and not overRideSpeed then
        wp.speed = point.speed
    elseif type(overRideSpeed) == "number" then
        wp.speed = overRideSpeed
    else
        wp.speed = mist.utils.kmphToMps(20)
    end
    if point.form and not overRideForm then
        form = point.form
    else
        form = overRideForm
    end
    if not form then
        wp.action = "Cone"
    else
        form = string.lower(form)
        if form == "off_road" or form == "off road" then
            wp.action = "Off Road"
        elseif form == "on_road" or form == "on road" then
            wp.action = "On Road"
        elseif form == "rank" or form == "line_abrest" or form == "line abrest" or form == "lineabrest" then
            wp.action = "Rank"
        elseif form == "cone" then
            wp.action = "Cone"
        elseif form == "diamond" then
            wp.action = "Diamond"
        elseif form == "vee" then
            wp.action = "Vee"
        elseif form == "echelon_left" or form == "echelon left" or form == "echelonl" then
            wp.action = "EchelonL"
        elseif form == "echelon_right" or form == "echelon right" or form == "echelonr" then
            wp.action = "EchelonR"
        else
            wp.action = "Cone"
        end
    end
    wp.type = "Turning Point"
    return wp
end

---------------------------------------------------------------------------------------------------
-- Tier 3 (spawn/route) -- the live CTLD spawn + SCAR/skynet route family.
---------------------------------------------------------------------------------------------------

-- Expand a list of references to an array of unit names. Retribution's live path passes plain unit
-- names (getAvgPos); the bracket-notation group/coalition forms feed CTLD JTAC autolase (disabled),
-- so they are skipped here.
function mist.makeUnitTable(tbl, exclude)
    local out, seen = {}, {}
    for i = 1, #tbl do
        local entry = tbl[i]
        if type(entry) == "string" and entry:sub(1, 1) ~= "[" and not seen[entry] then
            seen[entry] = true
            out[#out + 1] = entry
        end
    end
    return out
end

-- Resolve a group category that callers may pass as a number (CTLD: Group.Category.GROUND) OR a
-- MIST-style string (intercept: "vehicle"). coalition.addGroup needs the numeric Group.Category.
local function _resolve_group_category(cat)
    if type(cat) == "string" then
        local c = string.lower(cat)
        if c == "vehicle" or c == "ground" or c == "ground_unit" then
            return Group.Category.GROUND
        elseif c == "plane" or c == "airplane" then
            return Group.Category.AIRPLANE
        elseif c == "helicopter" then
            return Group.Category.HELICOPTER
        elseif c == "ship" then
            return Group.Category.SHIP
        elseif c == "train" then
            return Group.Category.TRAIN
        end
    end
    return cat
end

-- Spawn a group. Callers pass a country (number) + category (numeric Group.Category from CTLD, or a
-- string like "vehicle" from the intercept glue) and read back .name. We resolve the category,
-- synthesize the route coalition.addGroup requires, and default unit name/skill.
function mist.dynAdd(ng)
    local newGroup = mist.utils.deepCopy(ng)
    local cntry = newGroup.country or newGroup.countryId
    local category = _resolve_group_category(newGroup.category)
    if newGroup.groupName then
        newGroup.name = newGroup.groupName
    end
    if not newGroup.name then
        newGroup.name = "dyn group " .. tostring(timer.getTime()) .. "_" .. math.random(1, 1000000)
    end
    for i, u in pairs(newGroup.units) do
        if u.unitName then
            u.name = u.unitName
        end
        if not u.name then
            u.name = newGroup.name .. " unit" .. i
        end
        if not u.skill then
            u.skill = "Random"
        end
        if category == Group.Category.GROUND and u.playerCanDrive == nil then
            u.playerCanDrive = true
        end
        u.unitName = nil
    end
    if newGroup.route and not newGroup.route.points then
        if newGroup.route[1] then
            newGroup.route = { points = newGroup.route }
        else
            newGroup.route = { points = { [1] = {} } }
        end
    elseif not newGroup.route then
        newGroup.route = { points = { [1] = {} } }
    end
    newGroup.groupName = nil
    newGroup.clone = nil
    newGroup.category = nil
    newGroup.country = nil
    newGroup.countryId = nil
    newGroup.tasks = {}
    coalition.addGroup(cntry, category, newGroup)
    return newGroup
end

-- Spawn a static object. CTLD provides type/shape_name/x/y/heading/category itself; we only default
-- name/heading/dead and honor the mass->Cargos / shapeName aliases, then coalition.addStaticObject.
function mist.dynAddStatic(n)
    local newObj = mist.utils.deepCopy(n)
    if newObj.units and newObj.units[1] then -- mist format: flatten unit[1] onto the object
        for entry, val in pairs(newObj.units[1]) do
            if newObj[entry] == nil then
                newObj[entry] = val
            end
        end
    end
    local cntry = newObj.country or newObj.countryId
    newObj.name = newObj.name or newObj.unitName
    if not newObj.name then
        newObj.name = "dyn static " .. tostring(timer.getTime()) .. "_" .. math.random(1, 1000000)
    end
    if newObj.dead == nil then
        newObj.dead = false
    end
    if not newObj.heading then
        newObj.heading = math.rad(math.random(360))
    end
    if newObj.categoryStatic then
        newObj.category = newObj.categoryStatic
    end
    if newObj.mass then
        newObj.category = "Cargos"
    end
    if newObj.shapeName then
        newObj.shape_name = newObj.shapeName
    end
    newObj.country = nil
    newObj.countryId = nil
    newObj.clone = nil
    newObj.unitName = nil
    if newObj.x and newObj.y and newObj.type
        and type(newObj.x) == "number" and type(newObj.y) == "number" and type(newObj.type) == "string" then
        coalition.addStaticObject(cntry, newObj)
        return newObj
    end
    return false
end

-- Push a route onto a group as a Mission task (verbatim from MIST).
function mist.goRoute(group, path)
    local misTask = {
        id = "Mission",
        params = { route = { points = mist.utils.deepCopy(path) } },
    }
    if type(group) == "string" then
        group = Group.getByName(group)
    end
    if group then
        local groupCon = group:getController()
        if groupCon then
            groupCon:setTask(misTask)
            return true
        end
    end
    return false
end

-- Read a group's mission-editor route from env.mission. Only called by CTLD JTAC autolase
-- (disabled in Retribution); kept faithful without needing mist.DBs.MEgroupsByName.
function mist.getGroupRoute(groupIdent, task)
    if not (env and env.mission and env.mission.coalition) then
        return {}
    end
    for _, coa_data in pairs(env.mission.coalition) do
        if type(coa_data) == "table" and coa_data.country then
            for _, cntry_data in pairs(coa_data.country) do
                for obj_cat, obj_cat_data in pairs(cntry_data) do
                    if (obj_cat == "helicopter" or obj_cat == "ship" or obj_cat == "plane" or obj_cat == "vehicle")
                        and type(obj_cat_data) == "table" and obj_cat_data.group then
                        for _, grp in pairs(obj_cat_data.group) do
                            if type(grp) == "table" and grp.name == groupIdent then
                                return (grp.route and grp.route.points) or {}
                            end
                        end
                    end
                end
            end
        end
    end
    return {}
end

-- Move a group to a random point within a zone (skynet shoot-and-scoot). Builds a two-waypoint
-- ground route via goRoute; zones come from the Tier-2 zonesByName.
function mist.groupToRandomZone(gpData, zone, form, heading, speed, disableRoads)
    if type(gpData) == "string" then
        gpData = Group.getByName(gpData)
    end
    if type(zone) == "string" then
        zone = mist.DBs.zonesByName[zone]
    elseif type(zone) == "table" and not zone.radius then
        zone = mist.DBs.zonesByName[zone[math.random(1, #zone)]]
    end
    if not (gpData and zone) then
        return false
    end
    local lead = mist.getLeadPos(gpData)
    if not lead then
        return false
    end
    local action = disableRoads and "off road" or "on road"
    local mps = speed and mist.utils.kmphToMps(speed) or nil
    local dest = mist.getRandPointInCircle(zone.point, zone.radius or 0)
    local startWP = mist.ground.buildWP({ x = lead.x, y = lead.z }, action, mps)
    local endWP = mist.ground.buildWP({ x = dest.x, y = dest.y }, action, mps)
    return mist.goRoute(gpData, { startWP, endWP })
end

---------------------------------------------------------------------------------------------------
-- Tier 3 (spawn/route, continued) -- the Pretense teleport/respawn family.
---------------------------------------------------------------------------------------------------

-- land.getSurfaceType check against a list of surface-type names/values (MIST shape).
function mist.isTerrainValid(coordinate, terrainTypes)
    local coordArg = coordinate
    if coordArg.z then
        coordArg = mist.utils.makeVec2(coordArg)
    end
    if type(terrainTypes) == "string" then
        terrainTypes = { terrainTypes }
    end
    local surface = land.getSurfaceType(coordArg)
    for _, value in pairs(terrainTypes) do
        if type(value) == "string" and land.SurfaceType[string.upper(value)] == surface then
            return true
        elseif type(value) == "number" and value == surface then
            return true
        end
    end
    return false
end

-- Live snapshot of an existing group as a dynAdd-shaped definition: mission-table
-- fields (payload/skill) where the ME knows the group, live position/type/heading
-- always. Returns nil when the group does not exist (MIST semantics).
function mist.getCurrentGroupData(gpName)
    local liveGroup = Group.getByName(gpName)
    if not (liveGroup and liveGroup:isExist() == true) then
        return nil
    end
    local dbData = mist.getGroupData(gpName) or {}
    local newData = mist.utils.deepCopy(dbData)
    newData.name = gpName
    newData.groupName = gpName
    newData.groupId = tonumber(liveGroup:getID())
    local cat = liveGroup:getCategory()
    if cat == Group.Category.GROUND then
        newData.category = "vehicle"
    elseif cat == Group.Category.SHIP then
        newData.category = "ship"
    elseif newData.category == nil then
        newData.category = cat
    end
    local meUnits = {}
    if type(dbData.units) == "table" then
        for _, u in pairs(dbData.units) do
            if u.name then
                meUnits[u.name] = u
            end
        end
    end
    newData.units = {}
    for unitNum, unitData in pairs(liveGroup:getUnits()) do
        local uName = unitData:getName()
        local entry = meUnits[uName] and mist.utils.deepCopy(meUnits[uName]) or {}
        entry.name = uName
        entry.type = unitData:getTypeName()
        entry.skill = entry.skill or "Random"
        local okId, uid = pcall(function()
            return unitData:getID()
        end)
        if okId and uid then
            entry.unitId = tonumber(uid)
        end
        local pos = unitData:getPosition()
        entry.x = pos.p.x
        entry.y = pos.p.z -- mission-format y carries the east (z) axis
        entry.alt = pos.p.y
        entry.heading = mist.getHeading(unitData, true) or entry.heading or 0
        newData.units[unitNum] = entry
        if not newData.country then
            local okC, cid = pcall(function()
                return unitData:getCountry()
            end)
            if okC and cid then
                newData.country = cid
            end
        end
    end
    return newData
end

-- The MIST teleport/respawn/clone core (Pretense calls it directly and via
-- respawnGroup). Replicates mist.teleportToPoint's used surface: action
-- selection, randomized destination with terrain validation, per-unit offset
-- or dispersion, air altitude handling, ME-route re-application with the
-- offsetRoute/offsetWP1/initTasks handling, then dynAdd/dynAddStatic.
function mist.teleportToPoint(vars)
    local point = vars.point
    local gpName = vars.gpName or vars.groupName
    if not gpName and not vars.groupData then
        env.warning("mist shim: teleportToPoint: missing gpName/groupName")
        return false
    end
    local action = vars.action or "tele"
    local disperse = vars.disperse or false
    local maxDisp = vars.maxDisp or 200
    local radius = vars.radius or 0
    local innerRadius = vars.innerRadius
    local dbData = false
    local newGroupData
    if gpName and not vars.groupData then
        local act = string.lower(action)
        if act == "teleport" or act == "tele" then
            newGroupData = mist.getCurrentGroupData(gpName)
        elseif act == "respawn" then
            newGroupData = mist.getGroupData(gpName)
            dbData = true
        elseif act == "clone" then
            newGroupData = mist.getGroupData(gpName)
            if newGroupData then
                newGroupData.clone = "order66"
            end
            dbData = true
        else
            newGroupData = mist.getCurrentGroupData(gpName)
        end
    else
        newGroupData = vars.groupData
    end
    if not newGroupData then
        env.warning("mist shim: teleportToPoint: no group data for " .. tostring(gpName))
        return false
    end
    if vars.newGroupName then
        newGroupData.groupName = vars.newGroupName
    end
    if not newGroupData.units or #newGroupData.units == 0 then
        env.warning("mist shim: teleportToPoint: " .. tostring(gpName) .. " has no units")
        return
    end
    local validTerrain = { "LAND", "ROAD", "SHALLOW_WATER", "WATER", "RUNWAY" }
    if vars.anyTerrain then
        -- keep the permissive default
    elseif vars.validTerrain then
        validTerrain = vars.validTerrain
    elseif type(newGroupData.category) == "string" then
        local cat = string.lower(newGroupData.category)
        if cat == "ship" then
            validTerrain = { "SHALLOW_WATER", "WATER" }
        elseif cat == "vehicle" then
            validTerrain = { "LAND", "ROAD" }
        end
    end
    local diff = { x = 0, y = 0 }
    local newCoord, origCoord
    if point and radius >= 0 then
        local valid = false
        for _ = 1, 100 do
            newCoord = mist.getRandPointInCircle(point, radius, innerRadius)
            if vars.anyTerrain or mist.isTerrainValid(newCoord, validTerrain) then
                origCoord = mist.utils.deepCopy(newCoord)
                diff = {
                    x = newCoord.x - newGroupData.units[1].x,
                    y = newCoord.y - newGroupData.units[1].y,
                }
                valid = true
                break
            end
        end
        if not valid then
            env.warning("mist shim: teleportToPoint: no valid terrain at the destination")
            return false
        end
    end
    for unitNum, unitData in pairs(newGroupData.units) do
        if disperse then
            local unitCoord
            if maxDisp and type(maxDisp) == "number" and unitNum ~= 1 then
                for _ = 1, 100 do
                    unitCoord = mist.getRandPointInCircle(origCoord, maxDisp)
                    if mist.isTerrainValid(unitCoord, validTerrain) then
                        break
                    end
                end
            else
                unitCoord = mist.utils.deepCopy(newCoord)
            end
            if unitCoord then
                newGroupData.units[unitNum].x = unitCoord.x
                newGroupData.units[unitNum].y = unitCoord.y
            end
        else
            newGroupData.units[unitNum].x = unitData.x + diff.x
            newGroupData.units[unitNum].y = unitData.y + diff.y
        end
        if point and (newGroupData.category == "plane" or newGroupData.category == "helicopter") then
            local gl = land.getHeight({
                x = newGroupData.units[unitNum].x,
                y = newGroupData.units[unitNum].y,
            })
            if point.z and point.y and point.y > 0 and point.y > gl + 10 then
                newGroupData.units[unitNum].alt = point.y
            elseif newGroupData.category == "plane" then
                newGroupData.units[unitNum].alt = gl + math.random(300, 9000)
            else
                newGroupData.units[unitNum].alt = gl + math.random(200, 3000)
            end
        end
    end
    if newGroupData.start_time then
        newGroupData.startTime = newGroupData.start_time
    end
    if newGroupData.startTime and newGroupData.startTime ~= 0 and dbData == true then
        local timeDif = 0
        if timer.getAbsTime and timer.getTime0 then
            timeDif = timer.getAbsTime() - timer.getTime0()
        end
        if timeDif > newGroupData.startTime then
            newGroupData.startTime = 0
        else
            newGroupData.startTime = newGroupData.startTime - timeDif
        end
    end
    local tempRoute
    if _mistMEGroups == nil then
        _mistBuildMEGroups()
    end
    if _mistMEGroups[gpName] and not vars.route then
        tempRoute = mist.getGroupRoute(gpName, true)
    elseif vars.route then
        tempRoute = mist.utils.deepCopy(vars.route)
    end
    if tempRoute then
        if vars.offsetRoute or vars.offsetWP1 or vars.initTasks then
            for i = 1, #tempRoute do
                if vars.offsetRoute or (i == 1 and (vars.offsetWP1 or vars.initTasks)) then
                    tempRoute[i].x = tempRoute[i].x + diff.x
                    tempRoute[i].y = tempRoute[i].y + diff.y
                elseif vars.initTasks and i > 1 then
                    tempRoute[i] = nil
                end
            end
        end
        newGroupData.route = tempRoute
    end
    if type(newGroupData.category) == "string" and string.lower(newGroupData.category) == "static" then
        return mist.dynAddStatic(newGroupData)
    end
    return mist.dynAdd(newGroupData)
end

-- Respawn a mission-editor group in place, optionally re-pushing its ME route
-- (task == true) or scheduling the route push after a delay (task == number).
function mist.respawnGroup(gpName, task)
    local vars = {}
    vars.gpName = gpName
    vars.action = "respawn"
    if task and type(task) ~= "number" then
        vars.route = mist.getGroupRoute(gpName, "task")
    end
    local newGroup = mist.teleportToPoint(vars)
    if task and type(task) == "number" then
        local newRoute = mist.getGroupRoute(gpName, "task")
        mist.scheduleFunction(mist.goRoute, { newGroup, newRoute }, timer.getTime() + task)
    end
    return newGroup
end

-- ==> All 51 mist.* symbols the shipped plugins call are implemented. Rollback =
-- restore mist_4_5_126.lua from git history and re-point base/plugin.json's
-- "mist" work-order back at it (one line).

