-- land_relocate.lua
--
-- Relocates ship units that spawn on land (LAND / ROAD / RUNWAY) to the nearest
-- deep water at mission start, across all theaters. This is the naval mirror of
-- water_relocate.lua: when a carrier sits close to shore its formation escorts
-- can land on the coastline and end up stranded. Preserves each group's route,
-- tasks, skill and -- critically -- its group and unit names, so DCS
-- Retribution's kill/loss tracking and state.json parsing stay correct.
--
-- Part of the mandatory "base" plugin. Requires mist, which the plugin loads
-- first (this script is registered after moose.lua in plugin.json).
--
-- Mechanism: a live unit cannot be cheaply teleported, so we read the original
-- group definition with mist.getGroupData(), edit the x/y of beached units (and
-- the spawn waypoint if it is dry), and re-add the group under the same name
-- with mist.dynAdd(). coalition.addGroup with an existing name silently swaps
-- the units (fires S_EVENT_BIRTH only), so none of the four loss/kill events
-- Retribution tracks are emitted.
--
-- Destination is deep WATER only (not SHALLOW_WATER): the nearest wet point to a
-- beached ship is the waterline, which is often too shallow to float a hull, so
-- skipping the shallow band lands ships in water deep enough to clear the coast.
--
-- Open-water clearance: the nearest deep-water point to a beached ship is often a
-- sliver -- a river or a tidal inlet -- that leaves the hull straddling land. A
-- candidate is only accepted if deep water extends a full nautical mile out along
-- eight spokes, sampled every 0.2 nm, so the destination is genuinely open sea.
-- The check is heading-agnostic on purpose: a ship's spawn heading can point
-- inland, and keying the clearance off it could reject every valid destination.
--
-- Direction bias: the nearest open-water point can still be on the wrong side of
-- the ship. There is no runtime link from an escort to its carrier, but ships
-- placed correctly sit in deep water, so we treat every already-afloat ship unit
-- as an anchor and, among the equidistant candidates on a search ring, pick the
-- one nearest the closest anchor. That pulls beached escorts toward the carrier /
-- open sea (and keeps a partially-beached group together) instead of toward a
-- lake behind them. With no afloat ship anywhere we fall back to plain nearest.

-- Tunable constants -----------------------------------------------------------
local NM = 1852  -- metres per nautical mile

local RELOCATE_DELAY  = 1        -- seconds after start, so mist's group DB is ready
local SEARCH_STEP     = 60       -- metres between expanding search rings
local SEARCH_MAX      = 7 * NM   -- give up beyond ~7 nm. A carrier's outer escort
                                 -- ring sits up to ~5.8 nm out (Carrier_Strike_
                                 -- Group_8), so a landward escort can be that far
                                 -- inland when the carrier hugs the shore; 7 nm
                                 -- covers it plus the ~1 nm clearance margin
local SEARCH_HEADINGS = 8        -- sample points per ring (every 45 degrees)

local CLEAR_RADIUS = 1 * NM      -- destination must be open water this far out...
local CLEAR_STEP   = 0.2 * NM    -- ...sampled every 0.2 nm along each spoke

-- Relaxed fallback: when the strict open-water search finds nothing (e.g. a
-- carrier's escorts in a narrow canal), a beached ship is moved to the nearest
-- deep water. The gated relaxed pass keeps that destination at least
-- MIN_ANCHOR_DIST from the nearest afloat ship so escorts don't stack on the
-- carrier when a farther channel point exists; a final ungated pass ignores it so
-- a ship whose only water is the sliver beside the carrier still gets afloat.
local MIN_ANCHOR_DIST = 0.5 * NM

local DRY_SURFACES = {
    [land.SurfaceType.LAND] = true,
    [land.SurfaceType.ROAD] = true,
    [land.SurfaceType.RUNWAY] = true,
}

local DEEP_WATER_SURFACES = {
    [land.SurfaceType.WATER] = true,
}

-- Helpers ---------------------------------------------------------------------

-- DCS ground plane: getSurfaceType takes a 2D point { x = north, y = east }.
-- Group/unit data and route points store these as .x and .y, so pass them
-- straight through.
local function surface_at(x, y)
    return land.getSurfaceType({ x = x, y = y })
end

local function distance_sq(ax, ay, bx, by)
    local dx, dy = ax - bx, ay - by
    return dx * dx + dy * dy
end

-- Nearest afloat ship unit to (x, y), used as the bias target. Returns
-- { x = ..., y = ... } or nil when no ship is currently in deep water.
local function nearest_anchor(x, y, anchors)
    local best, best_d
    for _, a in ipairs(anchors) do
        local d = distance_sq(x, y, a.x, a.y)
        if not best_d or d < best_d then
            best, best_d = a, d
        end
    end
    return best
end

-- True only if deep water extends CLEAR_RADIUS out from (x, y) along every spoke,
-- sampled every CLEAR_STEP. A spoke crossing a river bank or pond shore hits land
-- and fails, so narrow slivers of water are rejected and a hull is never left
-- straddling one.
local function is_open_water(x, y)
    for i = 0, SEARCH_HEADINGS - 1 do
        local a = i * (2 * math.pi / SEARCH_HEADINGS)
        local dx, dy = math.cos(a), math.sin(a)
        -- +1 keeps the CLEAR_RADIUS endpoint in despite float drift.
        for d = CLEAR_STEP, CLEAR_RADIUS + 1, CLEAR_STEP do
            if not DEEP_WATER_SURFACES[surface_at(x + d * dx, y + d * dy)] then
                return false
            end
        end
    end
    return true
end

-- Expanding-ring spiral search for the nearest water point matching `opts`.
--   opts.require_open    -- gate candidates on is_open_water (strict clearance)
--   opts.min_anchor_dist -- reject candidates nearer than this (metres) to `bias`;
--                           0, nil, or a nil bias disables the gate.
-- With a bias target, a ring's qualifying candidates resolve in favour of the one
-- nearest it (the carrier / open sea); exact ties fall to heading-iteration order.
-- Returns { x = ..., y = ... } or nil if nothing within SEARCH_MAX.
local function find_water(x, y, bias, opts)
    -- Gate distance is compared squared, to match distance_sq and skip a sqrt.
    -- A nil min_anchor_dist is treated as 0 (gate off) so a preset may omit it.
    local min_anchor_dist = opts.min_anchor_dist or 0
    local min_d2 = 0
    if bias and min_anchor_dist > 0 then
        min_d2 = min_anchor_dist * min_anchor_dist
    end
    for r = SEARCH_STEP, SEARCH_MAX, SEARCH_STEP do
        local best, best_d
        for i = 0, SEARCH_HEADINGS - 1 do
            local a = i * (2 * math.pi / SEARCH_HEADINGS)
            local cx = x + r * math.cos(a)
            local cy = y + r * math.sin(a)
            if DEEP_WATER_SURFACES[surface_at(cx, cy)]
                and (not opts.require_open or is_open_water(cx, cy))
            then
                -- With no anchor to bias toward, take the first qualifying
                -- candidate. Otherwise a positive min_anchor_dist keeps the
                -- destination clear of the anchor (so escorts don't pile onto the
                -- carrier), and among the rest the one nearest the anchor wins.
                if not bias then
                    return { x = cx, y = cy }
                end
                local d = distance_sq(cx, cy, bias.x, bias.y)
                if d >= min_d2 then
                    if not best_d or d < best_d then
                        best, best_d = { x = cx, y = cy }, d
                    end
                end
            end
        end
        if best then
            return best
        end
    end
    return nil
end

-- Pass presets for find_destination, loosest-last.
local STRICT          = { require_open = true,  min_anchor_dist = 0 }
local RELAXED_GATED   = { require_open = false, min_anchor_dist = MIN_ANCHOR_DIST }
local RELAXED_UNGATED = { require_open = false, min_anchor_dist = 0 }

-- Find a water destination for a dry point. Tries the strict open-water search
-- first (unchanged behaviour for open coasts), then a relaxed search that accepts
-- any deep water but keeps MIN_ANCHOR_DIST off the nearest afloat ship, then a
-- final relaxed search with no spacing gate so an abeam escort still gets afloat
-- instead of stranded on land.
-- Returns (point, fallback): fallback is nil for the strict pass, or the
-- "gated" / "ungated" name of the relaxed pass that found the point. Returns
-- (nil, nil) when no pass found water within SEARCH_MAX.
local function find_destination(x, y, bias)
    local p = find_water(x, y, bias, STRICT)
    if p then
        return p, nil
    end
    p = find_water(x, y, bias, RELAXED_GATED)
    if p then
        return p, "gated"
    end
    p = find_water(x, y, bias, RELAXED_UNGATED)
    if p then
        return p, "ungated"
    end
    return nil, nil
end

-- Move a dry point (a unit or a route waypoint -- anything with x/y) onto water
-- in place, biased toward the nearest afloat anchor. Returns (moved, fallback):
-- moved is false when no pass found water; fallback is nil for the strict pass or
-- the "gated" / "ungated" name of the relaxed pass that produced the destination.
local function relocate_point(p, anchors)
    local bias = nearest_anchor(p.x, p.y, anchors)
    local dest, fallback = find_destination(p.x, p.y, bias)
    if dest then
        p.x, p.y = dest.x, dest.y
    end
    return dest ~= nil, fallback
end

-- Entry point -----------------------------------------------------------------

-- timer.scheduleFunction calls this with (argument, time); both are ignored.
-- Returning nil (no number) means it runs exactly once.
local function run()
    -- Pass 1: gather every ship group's data and record the positions of units
    -- already in deep water as bias anchors (the carrier and well-placed ships).
    local ships = {}
    local anchors = {}
    for _, side in ipairs({ coalition.side.RED, coalition.side.BLUE }) do
        for _, group in ipairs(coalition.getGroups(side, Group.Category.SHIP)) do
            local name = group:getName()
            local data = mist.getGroupData(name)
            if data and data.units and #data.units > 0 then
                ships[#ships + 1] = { name = name, data = data }
                for _, unit in ipairs(data.units) do
                    if DEEP_WATER_SURFACES[surface_at(unit.x, unit.y)] then
                        anchors[#anchors + 1] = { x = unit.x, y = unit.y }
                    end
                end
            end
        end
    end

    -- Pass 2: relocate beached units toward the nearest anchor.
    for _, ship in ipairs(ships) do
        local name, data = ship.name, ship.data
        local changed = false

        for _, unit in ipairs(data.units) do
            if DRY_SURFACES[surface_at(unit.x, unit.y)] then
                local moved, fallback = relocate_point(unit, anchors)
                if moved then
                    changed = true
                    if fallback then
                        env.info(
                            "land_relocate: "
                                .. name
                                .. " placed in nearest deep water via "
                                .. fallback
                                .. " fallback (no open-water site within "
                                .. SEARCH_MAX
                                .. "m)"
                        )
                    end
                else
                    env.warning(
                        "land_relocate: no deep water within "
                            .. SEARCH_MAX
                            .. "m for "
                            .. name
                    )
                end
            end
        end

        -- Keep the spawn waypoint (route point 1) on water too.
        if data.route and data.route.points and data.route.points[1] then
            local pt = data.route.points[1]
            if DRY_SURFACES[surface_at(pt.x, pt.y)] then
                local moved, fallback = relocate_point(pt, anchors)
                if moved then
                    changed = true
                    if fallback then
                        env.info(
                            "land_relocate: "
                                .. name
                                .. " spawn waypoint placed via "
                                .. fallback
                                .. " fallback"
                        )
                    end
                end
            end
        end

        if changed then
            env.info("land_relocate: relocating " .. name)
            mist.dynAdd(data)
        end
    end
end

timer.scheduleFunction(run, {}, timer.getTime() + RELOCATE_DELAY)
