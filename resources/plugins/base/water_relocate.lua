-- water_relocate.lua
--
-- Relocates ground units that spawn on water (WATER / SHALLOW_WATER) to the
-- nearest land at mission start, across all theaters. Preserves each group's
-- route, tasks, skill and -- critically -- its group and unit names, so DCS
-- Retribution's kill/loss tracking and state.json parsing stay correct.
--
-- Part of the mandatory "base" plugin. Requires mist, which the plugin loads
-- first (this script is registered after moose.lua in plugin.json).
--
-- Mechanism: a live unit cannot be cheaply teleported, so we read the original
-- group definition with mist.getGroupData(), edit the x/y of wet units (and the
-- spawn waypoint if it is wet), and re-add the group under the same name with
-- mist.dynAdd(). coalition.addGroup with an existing name silently swaps the
-- units (fires S_EVENT_BIRTH only), so none of the four loss/kill events
-- Retribution tracks are emitted.

-- Tunable constants -----------------------------------------------------------
local RELOCATE_DELAY  = 1     -- seconds after start, so mist's group DB is ready
local SEARCH_STEP     = 60    -- metres between expanding search rings
local SEARCH_MAX      = 2000  -- metres; give up beyond this radius
local SEARCH_HEADINGS = 8     -- sample points per ring (every 45 degrees)

local WET_SURFACES = {
    [land.SurfaceType.WATER] = true,
    [land.SurfaceType.SHALLOW_WATER] = true,
}

local LAND_SURFACES = {
    [land.SurfaceType.LAND] = true,
    [land.SurfaceType.ROAD] = true,
    [land.SurfaceType.RUNWAY] = true,
}

-- Helpers ---------------------------------------------------------------------

-- DCS ground plane: getSurfaceType takes a 2D point { x = north, y = east }.
-- Group/unit data and route points store these as .x and .y, so pass them
-- straight through.
local function surface_at(x, y)
    return land.getSurfaceType({ x = x, y = y })
end

-- Expanding-ring spiral search for the nearest land point.
-- Returns { x = ..., y = ... } or nil if no land within SEARCH_MAX.
local function nearest_land(x, y)
    for r = SEARCH_STEP, SEARCH_MAX, SEARCH_STEP do
        for i = 0, SEARCH_HEADINGS - 1 do
            local a = i * (2 * math.pi / SEARCH_HEADINGS)
            local cx = x + r * math.cos(a)
            local cy = y + r * math.sin(a)
            if LAND_SURFACES[surface_at(cx, cy)] then
                return { x = cx, y = cy }
            end
        end
    end
    return nil
end

-- Entry point -----------------------------------------------------------------

-- timer.scheduleFunction calls this with (argument, time); both are ignored.
-- Returning nil (no number) means it runs exactly once.
local function run()
    for _, side in ipairs({ coalition.side.RED, coalition.side.BLUE }) do
        for _, group in ipairs(coalition.getGroups(side, Group.Category.GROUND)) do
            local name = group:getName()
            local data = mist.getGroupData(name)
            if data and data.units and #data.units > 0 then
                local changed = false

                for _, unit in ipairs(data.units) do
                    if WET_SURFACES[surface_at(unit.x, unit.y)] then
                        local p = nearest_land(unit.x, unit.y)
                        if p then
                            unit.x, unit.y = p.x, p.y
                            changed = true
                        else
                            env.warning(
                                "water_relocate: no land within "
                                    .. SEARCH_MAX
                                    .. "m for "
                                    .. name
                            )
                        end
                    end
                end

                -- Keep the spawn waypoint (route point 1) on land too.
                if data.route and data.route.points and data.route.points[1] then
                    local pt = data.route.points[1]
                    if WET_SURFACES[surface_at(pt.x, pt.y)] then
                        local p = nearest_land(pt.x, pt.y)
                        if p then
                            pt.x, pt.y = p.x, p.y
                            changed = true
                        end
                    end
                end

                if changed then
                    env.info("water_relocate: relocating " .. name)
                    mist.dynAdd(data)
                end
            end
        end
    end
end

timer.scheduleFunction(run, {}, timer.getTime() + RELOCATE_DELAY)
