
-- Creates a single pilot unit at a given position, used to facilitate CSAR type mission
-- Function is rewritten to support the new Spawner.getData which takes side as an argument
function Spawner.createPilot(name, pos)

    -- Request spawn data for a "pilot-replacement" template.
    -- side = 2 (Blue), minDist = nil, maxDist = 5
    -- Allowed surfaces: land, road, runway
    local groupData = Spawner.getData("pilot-replacement", name, pos, 2, nil, 5, {
        [land.SurfaceType.LAND] = true,
        [land.SurfaceType.ROAD] = true,
        [land.SurfaceType.RUNWAY] = true,
    })

    -- Spawn the pilot as a BLUE ground unit group
    return coalition.addGroup(country.id.CJTF_BLUE, Group.Category.GROUND, groupData)
end

-- Creates either a static object or a ground group depending on template type
-- Function is rewritten to support the new Spawner.getData which takes side as an argument
function Spawner.createObject(name, objType, pos, side, minDist, maxDist, surfaceTypes, zone)
    -- If a zone name was provided, convert it into a CustomZone object
    -- by looking up with the zone name
    if zone then
        zone = CustomZone:getByName(zone)
    end

    -- Retrieve spawn data for the requested object type, also considering the side for which the data should
    -- be retrieved. The side impacts which livery overrides should be applied, if any have been defined.
    local data = Spawner.getData(objType, name, pos, side, minDist, maxDist, surfaceTypes, zone)

    -- If no data returned, abort spawning
    if not data then return end

    -- Here, side also determines whether to create the object for Combined Joint Task Force Blue or Red
    local cnt = country.id.CJTF_BLUE
    if side == 1 then
        cnt = country.id.CJTF_RED
    end

    -- TemplateDB determines whether to spawn static objects or ground unit groups
    if data.dataCategory == TemplateDB.type.static then
        return coalition.addStaticObject(cnt, data)
    elseif data.dataCategory == TemplateDB.type.group then
        return coalition.addGroup(cnt, Group.Category.GROUND, data)
    end
end

-- Core function that builds spawn data for static objects or groups
-- Function is rewritten to support the new Spawner.getData which takes side as an argument
function Spawner.getData(objtype, name, pos, side, minDist, maxDist, surfaceTypes, zone)
    -- Default max distance of 150 meters if none provided as argument
    if not maxDist then maxDist = 150 end

    -- Default allowed surface type = land only
    if not surfaceTypes then surfaceTypes = { [land.SurfaceType.LAND]=true } end

    -- Retrieve template data from TemplateDB
    local data = TemplateDB.getData(objtype)
    if not data then
        env.info("Spawner - ERROR: cant find group data "..tostring(objtype).." for group name "..name)
        return
    end

    local spawnData = {}

    --------------------------------------------------------------------------
    -- STATIC OBJECT SPAWNING
    --------------------------------------------------------------------------
    if data.dataCategory == TemplateDB.type.static then
        -- If the initial position is not on an allowed surface, search for a valid one
        -- Repeat 500 times before giving up, trying out a different position within maxDist.
        -- Print an error message if a good spot was not found. However, will resume spawning
        -- even if a good location was not found.
        if not surfaceTypes[land.getSurfaceType(pos)] then
            for i=1,500,1 do
                pos = mist.getRandPointInCircle(pos, maxDist)

                -- If spawning inside a zone, ensure the point is inside it
                if zone then
                    if zone:isInside(pos) and surfaceTypes[land.getSurfaceType(pos)] then
                        break
                    end
                else
                    -- No zone: only check surface type
                    if surfaceTypes[land.getSurfaceType(pos)] then
                        break
                    end
                end

                if i==500 then env.info('Spawner - ERROR: failed to find good location') end
            end
        end

        spawnData = {
            ["type"] = data.type,
            ["name"] = name,
            ["shape_name"] = data.shape,
            ["category"] = data.category,
            ["x"] = pos.x,
            ["y"] = pos.y,
            ['heading'] = math.random()*math.pi*2
        }
    elseif data.dataCategory== TemplateDB.type.group then
        spawnData = {
            ["units"] = {},
            ["name"] = name,
            ["task"] = "Ground Nothing",
            ["route"] = {
                ["points"]={
                    {
                        ["x"] = pos.x,
                        ["y"] = pos.y,
                        ["action"] = "Off Road",
                        ["speed"] = 0,
                        ["type"] = "Turning Point",
                        ["ETA"] = 0,
                        ["formation_template"] = "",
                        ["task"] = Spawner.getDefaultTask(data.invisible)
                    }
                }
            }
        }

        -- Override min/max distance if template defines them
        if data.minDist then
            minDist = data.minDist
        end

        if data.maxDist then
            maxDist = data.maxDist
        end

        -- Build each unit in the group
        for i,v in ipairs(data.units) do
            -- Generate unit spawn data
            unitData = Spawner.getUnit(v, name.."-"..i, pos, data.skill, minDist, maxDist, surfaceTypes, zone)

            ------------------------------------------------------------------
            -- APPLY LIVERY OVERRIDES
            ------------------------------------------------------------------
            local liverytable_side = LiveryDB.livery_overrides[tostring(side)]
            if liverytable_side ~= nil then
                env.info("Spawner - Found livery overrides for side "..tostring(side))
                env.info("Spawner - Object type key is: "..tostring(v))

                -- Look up livery list for this specific unit type
                local liverytable_object = liverytable_side[tostring(v)]
                if liverytable_object ~= nil then
                    env.info("Spawner - Found livery override for object "..tostring(v))

                    -- Pick a random livery from the list
                    local livery_override = liverytable_object[math.random(#liverytable_object)]
                    if livery_override ~= nil then
                        env.info("Spawner - Applying livery override "..tostring(livery_override))
                        unitData["livery_id"] = livery_override
                    end
                else
                    env.info("Spawner - WARNING: Could not find livery overrides for object "..tostring(v))
                end
            else
                env.info("Spawner - WARNING: Could not find livery overrides for side "..tostring(side))
            end

            -- Add the completed unit to the group
            table.insert(spawnData.units, unitData)
        end
    end

    -- Store the category so the caller knows how to spawn it
    spawnData.dataCategory = data.dataCategory

    return spawnData
end


