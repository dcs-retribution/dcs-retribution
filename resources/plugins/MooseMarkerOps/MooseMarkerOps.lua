SoundFilePath = ""
BlueDebug = false
-------------------------------------------------------------------------------------------------
-- MARKEROPS BOOM
-------------------------------------------------------------------------------------------------
function Boom()
    local MarkerOpsBoom = MARKEROPS_BASE:New("Boom", nil, false)
    if BlueDebug then
        BASE:I("--------BOOM LOADING-----")
    end
    if BlueDebug then
        local m = MESSAGE:New("Explosion on Coordinate Mode Enabled", 30, "Player"):ToBlue()
    end

    -- Handler function
    local function Handler(Text, Coord)
        local n = tonumber(Text:match("(%d+)$"))
        BASE:I(n)
        Coord:Explosion(n)
    end

    -- Event functions
    function MarkerOpsBoom:OnAfterMarkAdded(From, Event, To, Text, Keywords, Coord)
        if BlueDebug then
            local ms = MESSAGE:New("Sending Boom", 30, "Player"):ToBlue()
        end
        Handler(Text, Coord)
    end

    function MarkerOpsBoom:OnAfterMarkChanged(From, Event, To, Text, Keywords, Coord)
        if BlueDebug then
            local m = MESSAGE:New(string.format("%s coordinates recieved", self.Tag), 10, "Info", true):ToAll()
        end
        Handler(Text, Coord)
    end

    function MarkerOpsBoom:OnAfterMarkDeleted(From, Event, To)
        if BlueDebug then
            local m = MESSAGE:New(string.format("%s Mark Deleted.", self.Tag), 10, "Info", true):ToAll()
        end
    end

    if BlueDebug then
        BASE:I("-------BOOM LOADED------")
    end
end

Boom()

-------------------------------------------------------------------------------------------------
-- MARKEROPS ILLUMINATION
-------------------------------------------------------------------------------------------------

function Illumination()
    if BlueDebug then
        BASE:I("----ILLUMINATION LOADING---------")
    end
    local MarkerOpsIlluminationBomb = MARKEROPS_BASE:New("Light", { "Zone", "zone" }, false)
    if BlueDebug then
        local m = MESSAGE:New("IlluminationBomb on Coordinate Mode Enabled", 30, "Player"):ToBlue()
    end

    -- Handler function
    local function LightHandler(Coord, Keywords, Text)
        env.info("----Simple Light-----")
        Coord:SetAltitude(350)
        Coord:IlluminationBomb(nil, 3)

        for _index, _word in pairs(Keywords) do
            if string.lower(_word) == "zone" then -- User says "Light zone" or "Light Zone 5", not just "Light"
                env.info("----Light 'zone' found-----")

                local coord = Coord
                -- See if a Radius is Defined
                local n = tonumber(Text:match("(%d+)$")) or 5
                BASE:I(n)
                -- Make X Mile Zone Around Coord
                local ZoneAroundCoord = ZONE_RADIUS:New("Zone " .. math.random(100000), coord:GetVec2(), n * 1609)
                -- Draw the Zone
                ZoneAroundCoord:DrawZone(-1, { 1, 0, 0 }, 1, { 1, 0, 0 })
                ZoneAroundCoord:UndrawZone(10)
                -- Make a set of all Groups in Zone
                local GroupsInZoneSet = SET_GROUP:New():FilterZones({ ZoneAroundCoord }, true):FilterOnce()

                -- If Groups In Zone, Drop an Illumination Bomb on Each
                if GroupsInZoneSet:Count() > 0 then
                    GroupsInZoneSet:ForEachGroup(function(grp)
                        env.info(grp:GetName() .. " Is In Zone-----")
                        grpFirstCoord = grp:GetCoordinate()
                        grpFirstCoord:SetAltitude(350)
                        grpFirstCoord:IlluminationBomb(nil, 3)
                        env.info("-----Illuminating " .. grp:GetName() .. " In Zone-----")
                        if BlueDebug then
                            trigger.action.outText("---Illuminating " .. grp:GetName() .. " In Zone-----", 5)
                        end
                    end)
                end
            end
        end
    end

    -- Event functions
    function MarkerOpsIlluminationBomb:OnAfterMarkAdded(From, Event, To, Text, Keywords, Coord)
        if BlueDebug then
            local ms = MESSAGE:New("Sending Illumination", 30, "Player"):ToBlue()
        end
        LightHandler(Coord, Keywords, Text)
    end

    function MarkerOpsIlluminationBomb:OnAfterMarkChanged(From, Event, To, Text, Keywords, Coord)
        if BlueDebug then
            local m = MESSAGE:New(string.format("%s coordinates recieved", self.Tag), 10, "Info", true):ToAll()
        end
        LightHandler(Coord, Keywords, Text)
    end

    function MarkerOpsIlluminationBomb:OnAfterMarkDeleted(From, Event, To)
        if BlueDebug then
            local m = MESSAGE:New(string.format("%s Mark Deleted.", self.Tag), 10, "Info", true):ToAll()
        end
    end

    if BlueDebug then
        BASE:I("----ILLUMINATION LOADED---------")
    end
end

Illumination()

-------------------------------------------------------------------------------------------------
-- MARKEROPS SMOKE POINT
-------------------------------------------------------------------------------------------------

function Smoke()
    if BlueDebug then
        BASE:I("------SMOKE LOADING------")
    end
    local MarkerOpsSmoke = MARKEROPS_BASE:New("Smoke", { "Red", "Blue", "Green", "Orange", "White" }, false)

    if BlueDebug then
        local m = MESSAGE:New("Smoke Mode Enabled (Lasts 5 min)", 30, "Player"):ToBlue()
    end

    -- Handler function
    function SmokeHandler(Keywords, Coord)
        for _, _word in pairs(Keywords) do
            if string.lower(_word) == "red" then
                Coord:SmokeRed()
                env.info("------Red Smoke on Coord-------")
            elseif string.lower(_word) == "blue" then
                Coord:SmokeBlue()
                env.info("------Blue Smoke on Coord-------")
            elseif string.lower(_word) == "green" then
                Coord:SmokeGreen()
                env.info("------Green Smoke on Coord-------")
            elseif string.lower(_word) == "orange" then
                Coord:SmokeOrange()
                env.info("------Orange Smoke on Coord-------")
            elseif string.lower(_word) == "white" then
                Coord:SmokeWhite()
                env.info("------White Smoke on Coord-------")
            end
        end
    end

    -- Event functions
    function MarkerOpsSmoke:OnAfterMarkAdded(From, Event, To, Text, Keywords, Coord)
        if BlueDebug then
            local ms = MESSAGE:New("Marking Smoke", 30, "Player"):ToBlue()
        end
        SmokeHandler(Keywords, Coord)
    end

    function MarkerOpsSmoke:OnAfterMarkChanged(From, Event, To, Text, Keywords, Coord)
        if BlueDebug then
            local m = MESSAGE:New(string.format("%s coordinates recieved", self.Tag), 10, "Info", true):ToAll()
        end
        SmokeHandler(Keywords, Coord)
    end

    function MarkerOpsSmoke:OnAfterMarkDeleted(From, Event, To)
        if BlueDebug then
            local m = MESSAGE:New(string.format("%s Mark Deleted.", self.Tag), 10, "Info", true):ToAll()
        end
    end

    if BlueDebug then
        BASE:I("-----SMOKE LOADED------")
    end
end

Smoke()

-------------------------------------------------------------------------------------------------
-- MARKEROPS SMOKE ZONE
-------------------------------------------------------------------------------------------------
function SmokeZone()
    if BlueDebug then
        BASE:I("------SMOKE ZONE LOADING------")
    end
    local MarkerOpsSmokeZone = MARKEROPS_BASE:New("SmokeZone", nil, false)

    if BlueDebug then
        local m = MESSAGE:New("Smoke Zone Mode Enabled (Lasts 5 min)", 30, "Player"):ToBlue()
    end

    -- Handler function
    function SmokeZoneHandler(Text, Coord)
        local coord = Coord
        local n = 5

        if Text then
            local n = tonumber(Text:match("(%d+)$"))
        end
        BASE:I(n)

        -- Make X Mile Zone Around Coord
        local ZoneAroundCoord = ZONE_RADIUS:New("Zone " .. math.random(100000), coord:GetVec2(), n * 1609)
        -- Draw the Zone
        ZoneAroundCoord:DrawZone(-1, { 1, 0, 0 }, 1, { 1, 0, 0 })
        ZoneAroundCoord:UndrawZone(10)

        -- Make a set of all Groups in Zone
        local GroupsInZoneSet = SET_GROUP:New():FilterZones({ ZoneAroundCoord }, true):FilterOnce()

        -- If Groups In Zone, Attack
        if GroupsInZoneSet:Count() > 0 then
            GroupsInZoneSet:ForEachGroup(function(grp)
                local grpCoalition = grp:GetCoalition()
                local grpCoordinate = grp:GetCoordinate()
                if grpCoalition == coalition.side.RED then
                    grpCoordinate:SmokeRed()
                    env.info("----SMOKING " .. grp:GetName() .. " RED----")
                end

                if grpCoalition == coalition.side.BLUE then
                    grpCoordinate:SmokeBlue()
                    env.info("----SMOKING " .. grp:GetName() .. " BLUE----")
                end

                if grpCoalition == coalition.side.NEUTRAL then
                    grpCoordinate:SmokeWhite()
                    env.info("----SMOKING " .. grp:GetName() .. " WHITE----")
                end
            end)
        else
            env.info("-----NO GROUPS IN ZONE------")
        end
    end

    -- Event functions
    function MarkerOpsSmokeZone:OnAfterMarkAdded(From, Event, To, Text, Keywords, Coord)
        if BlueDebug then
            local ms = MESSAGE:New("Marking SmokeZone", 30, "Player"):ToBlue()
        end
        SmokeZoneHandler(Text, Coord)
    end

    function MarkerOpsSmokeZone:OnAfterMarkChanged(From, Event, To, Text, Keywords, Coord)
        if BlueDebug then
            local m = MESSAGE:New(string.format("%s coordinates recieved", self.Tag), 10, "Info", true):ToAll()
        end
        SmokeZoneHandler(Text, Coord)
    end

    function MarkerOpsSmokeZone:OnAfterMarkDeleted(From, Event, To)
        if BlueDebug then
            local m = MESSAGE:New(string.format("%s Mark Deleted.", self.Tag), 10, "Info", true):ToAll()
        end
    end

    if BlueDebug then
        BASE:I("-----SMOKE ZONE LOADED------")
    end
end

SmokeZone()

-------------------------------------------------------------------------------------------------
-- MARKEROPS DESTROY
-------------------------------------------------------------------------------------------------

function DestroyThem()
    if BlueDebug then
        BASE:I("------DESTROY LOADING------")
    end
    local MarkerOpsDestroy = MARKEROPS_BASE:New("Destroy", nil, false)

    if BlueDebug then
        local m = MESSAGE:New("Destroy Mode Enabled", 30, "Player"):ToBlue()
    end

    -- Handler function
    local function DestroyHandler(Text, Coord)
        local n = tonumber(Text:match("(%d+)$")) or 5
        BASE:I(n)

        local coord = Coord
        -- Make X Mile Zone Around Coord
        local ZoneAroundCoord = ZONE_RADIUS:New("Zone " .. math.random(100000), coord:GetVec2(), n * 1609)
        -- Draw the Zone
        ZoneAroundCoord:DrawZone(-1, { 1, 0, 0 }, 1, { 1, 0, 0 })
        ZoneAroundCoord:UndrawZone(10)

        -- Make a set of all Groups in Zone
        local GroupsInZoneSet = SET_GROUP:New():FilterZones({ ZoneAroundCoord }, true):FilterOnce()

        -- If Groups In Zone, Attack
        if GroupsInZoneSet:Count() > 0 then
            GroupsInZoneSet:ForEachGroup(function(grp)
                grp:Destroy(true)
                env.info("-----Destroying " .. grp:GetName() .. " In Zone")
                if BlueDebug then
                    trigger.action.outText("---Destroying " .. grp:GetName() .. " In Zone-----", 5)
                end
            end)
        else
            env.info("-----NO GROUPS IN ZONE------")
        end
    end

    -- Event functions
    function MarkerOpsDestroy:OnAfterMarkAdded(From, Event, To, Text, Keywords, Coord)
        if BlueDebug then
            local ms = MESSAGE:New("Destroying All Groups In Radius", 30, "Player"):ToBlue()
        end
        DestroyHandler(Text, Coord)
    end

    function MarkerOpsDestroy:OnAfterMarkChanged(From, Event, To, Text, Keywords, Coord)
        if BlueDebug then
            local m = MESSAGE:New(string.format("%s coordinates recieved", self.Tag), 10, "Info", true):ToAll()
        end
        DestroyHandler(Text, Coord)
    end

    function MarkerOpsDestroy:OnAfterMarkDeleted(From, Event, To)
        if BlueDebug then
            local m = MESSAGE:New(string.format("%s Mark Deleted.", self.Tag), 10, "Info", true):ToAll()
        end
    end

    if BlueDebug then
        BASE:I("------DESTROY LOADED-----------")
    end
end

DestroyThem()

-------------------------------------------------------------------------------------------------
-- RTB ZONE
-------------------------------------------------------------------------------------------------
function RTBZone()
    if BlueDebug then
        BASE:I("------RTB ZONE LOADING------")
    end
    local MarkerOpsRTBZone = MARKEROPS_BASE:New("RTB", nil, false)

    if BlueDebug then
        local m = MESSAGE:New("RTB Zone Mode Enabled", 30, "Player"):ToBlue()
    end

    -- Handler function
    function RTBZoneHandler(Text, Coord)
        local coord = Coord
        local n = 5

        if Text then
            local n = tonumber(Text:match("(%d+)$"))
        end
        BASE:I(n)

        -- Make X Mile Zone Around Coord
        local ZoneAroundCoord = ZONE_RADIUS:New("Zone " .. math.random(100000), coord:GetVec2(), n * 1609)
        -- Draw the Zone
        ZoneAroundCoord:DrawZone(-1, { 1, 0, 0 }, 1, { 1, 0, 0 })
        ZoneAroundCoord:UndrawZone(10)

        -- Make a set of all Groups in Zone
        local GroupsInZoneSet = SET_GROUP:New():FilterZones({ ZoneAroundCoord }, true):FilterOnce()

        -- If Groups In Zone, Attack
        if GroupsInZoneSet:Count() > 0 then
            env.info("----THERE ARE " .. GroupsInZoneSet:Count() .. " GROUPS IN ZONE-----")

            GroupsInZoneSet:ForEachGroup(function(grp)
                local opsGroup = _DATABASE:FindOpsGroup(grp:GetName())

                if opsGroup then
                    if opsGroup:IsFlightgroup() then
                        env.info("-----Flightgroup RTB-----")
                        opsGroup:CancelAllMissions()
                    end
                end
            end)
        else
            env.info("-----NO GROUPS IN ZONE------")
        end
    end

    -- Event functions
    function MarkerOpsRTBZone:OnAfterMarkAdded(From, Event, To, Text, Keywords, Coord)
        if BlueDebug then
            local ms = MESSAGE:New("RTB for all groups in Zone", 30, "Player"):ToBlue()
        end
        RTBZoneHandler(Text, Coord)
    end

    function MarkerOpsRTBZone:OnAfterMarkChanged(From, Event, To, Text, Keywords, Coord)
        if BlueDebug then
            local m = MESSAGE:New(string.format("%s coordinates recieved", self.Tag), 10, "Info", true):ToAll()
        end
        RTBZoneHandler(Text, Coord)
    end

    function MarkerOpsRTBZone:OnAfterMarkDeleted(From, Event, To)
        if BlueDebug then
            local m = MESSAGE:New(string.format("%s Mark Deleted.", self.Tag), 10, "Info", true):ToAll()
        end
    end

    if BlueDebug then
        BASE:I("-----RTB ZONE LOADED------")
    end
end

RTBZone()

-------------------------------------------------------------------------------------------------
-- IMMORTAL ON ZONE
-------------------------------------------------------------------------------------------------
function ImmortalZone()
    if BlueDebug then
        BASE:I("------Immortal ZONE LOADING------")
    end
    local MarkerOpsImmortalZone = MARKEROPS_BASE:New("Immortal", nil, false)

    if BlueDebug then
        local m = MESSAGE:New("Immortal Zone Mode Enabled", 30, "Player"):ToBlue()
    end

    -- Handler function
    function ImmortalZoneHandler(Text, Coord)
        local coord = Coord
        local n = 5

        if Text then
            local n = tonumber(Text:match("(%d+)$"))
        end
        BASE:I(n)

        -- Make X Mile Zone Around Coord
        local ZoneAroundCoord = ZONE_RADIUS:New("Zone " .. math.random(100000), coord:GetVec2(), n * 1609)
        -- Draw the Zone
        ZoneAroundCoord:DrawZone(-1, { 1, 0, 0 }, 1, { 1, 0, 0 })
        ZoneAroundCoord:UndrawZone(10)

        -- Make a set of all Groups in Zone
        local GroupsInZoneSet = SET_GROUP:New():FilterZones({ ZoneAroundCoord }, true):FilterOnce()

        -- If Groups In Zone, Attack
        if GroupsInZoneSet:Count() > 0 then
            env.info("----THERE ARE " .. GroupsInZoneSet:Count() .. " GROUPS IN ZONE-----")

            GroupsInZoneSet:ForEachGroup(function(grp)
                env.info(grp:GetName() .. " IS NOW IMMORTAL-----")
                grp:CommandSetImmortal(true)
            end)
        else
            env.info("-----NO GROUPS IN ZONE------")
        end
    end

    -- Event functions
    function MarkerOpsImmortalZone:OnAfterMarkAdded(From, Event, To, Text, Keywords, Coord)
        if BlueDebug then
            local ms = MESSAGE:New("GROUPS IN ZONE NOW IMMORTAL", 30, "Player"):ToBlue()
        end
        ImmortalZoneHandler(Text, Coord)
    end

    function MarkerOpsImmortalZone:OnAfterMarkChanged(From, Event, To, Text, Keywords, Coord)
        if BlueDebug then
            local m = MESSAGE:New(string.format("%s coordinates recieved", self.Tag), 10, "Info", true):ToAll()
        end
        ImmortalZoneHandler(Text, Coord)
    end

    function MarkerOpsImmortalZone:OnAfterMarkDeleted(From, Event, To)
        if BlueDebug then
            local m = MESSAGE:New(string.format("%s Mark Deleted.", self.Tag), 10, "Info", true):ToAll()
        end
    end

    if BlueDebug then
        BASE:I("-----IMMORTAL ZONE LOADED------")
    end
end

ImmortalZone()

-------------------------------------------------------------------------------------------------
-- MORTAL ON ZONE
-------------------------------------------------------------------------------------------------
function MortalZone()
    if BlueDebug then
        BASE:I("------MORTAL ZONE LOADING------")
    end
    local MarkerOpsMortalZone = MARKEROPS_BASE:New("Mortal", nil, false)

    if BlueDebug then
        local m = MESSAGE:New("Mortal Zone Mode Enabled", 30, "Player"):ToBlue()
    end

    -- Handler function
    function MortalZoneHandler(Text, Coord)
        local coord = Coord
        local n = 5

        if Text then
            local n = tonumber(Text:match("(%d+)$"))
        end
        BASE:I(n)

        -- Make X Mile Zone Around Coord
        local ZoneAroundCoord = ZONE_RADIUS:New("Zone " .. math.random(100000), coord:GetVec2(), n * 1609)
        -- Draw the Zone
        ZoneAroundCoord:DrawZone(-1, { 1, 0, 0 }, 1, { 1, 0, 0 })
        ZoneAroundCoord:UndrawZone(10)

        -- Make a set of all Groups in Zone
        local GroupsInZoneSet = SET_GROUP:New():FilterZones({ ZoneAroundCoord }, true):FilterOnce()

        -- If Groups In Zone, Attack
        if GroupsInZoneSet:Count() > 0 then
            env.info("----THERE ARE " .. GroupsInZoneSet:Count() .. " GROUPS IN ZONE-----")

            GroupsInZoneSet:ForEachGroup(function(grp)
                env.info(grp:GetName() .. " IS NOW MORTAL-----")
                grp:CommandSetImmortal(false)
            end)
        else
            env.info("-----NO GROUPS IN ZONE------")
        end
    end

    -- Event functions
    function MarkerOpsMortalZone:OnAfterMarkAdded(From, Event, To, Text, Keywords, Coord)
        if BlueDebug then
            local ms = MESSAGE:New("GROUPS IN ZONE NOW MORTAL", 30, "Player"):ToBlue()
        end
        MortalZoneHandler(Text, Coord)
    end

    function MarkerOpsMortalZone:OnAfterMarkChanged(From, Event, To, Text, Keywords, Coord)
        if BlueDebug then
            local m = MESSAGE:New(string.format("%s coordinates recieved", self.Tag), 10, "Info", true):ToAll()
        end
        MortalZoneHandler(Text, Coord)
    end

    function MarkerOpsMortalZone:OnAfterMarkDeleted(From, Event, To)
        if BlueDebug then
            local m = MESSAGE:New(string.format("%s Mark Deleted.", self.Tag), 10, "Info", true):ToAll()
        end
    end

    if BlueDebug then
        BASE:I("-----MORTAL ZONE LOADED------")
    end
end

MortalZone()

-------------------------------------------------------------------------------------------------
-- REFUEL ZONE
-------------------------------------------------------------------------------------------------
function RefuelZone()
    if BlueDebug then
        BASE:I("------REFUEL ZONE LOADING------")
    end
    local MarkerOpsRefuelZone = MARKEROPS_BASE:New("Refuel", nil, false)

    if BlueDebug then
        local m = MESSAGE:New("Refuel Zone Mode Enabled", 30, "Player"):ToBlue()
    end

    -- Handler function
    function RefuelZoneHandler(Text, Coord)
        local coord = Coord
        local n = 5

        if Text then
            local n = tonumber(Text:match("(%d+)$"))
        end
        BASE:I(n)

        -- Make X Mile Zone Around Coord
        local ZoneAroundCoord = ZONE_RADIUS:New("Zone " .. math.random(100000), coord:GetVec2(), n * 1609)
        -- Draw the Zone
        ZoneAroundCoord:DrawZone(-1, { 1, 0, 0 }, 1, { 1, 0, 0 })
        ZoneAroundCoord:UndrawZone(10)

        -- Make a set of all Groups in Zone
        local GroupsInZoneSet = SET_GROUP:New():FilterZones({ ZoneAroundCoord }, true)
            :FilterFunction( -- The function needs to take a GROUP object as first - and in this case, only - argument.
                function(grp)
                    local isinclude = true
                    if grp:GetAttribute() == GROUP.Attribute.AIR_TANKER then
                        isinclude = false
                    end
                    return isinclude
                end):FilterOnce()

        -- If Groups In Zone, Attack
        if GroupsInZoneSet:Count() > 0 then
            env.info("----THERE ARE " .. GroupsInZoneSet:Count() .. " GROUPS IN ZONE-----")

            GroupsInZoneSet:ForEachGroup(function(grp)
                if opsGroup and opsGroup:IsFlightgroup() then
                    opsGroup:Refuel()
                    env.info(grp:GetName() .. "Sent to Refuel-----")
                end
            end)
        else
            env.info("-----NO GROUPS IN ZONE------")
        end
    end

    -- Event functions
    function MarkerOpsRefuelZone:OnAfterMarkAdded(From, Event, To, Text, Keywords, Coord)
        if BlueDebug then
            local ms = MESSAGE:New("Refuel for all groups in Zone", 30, "Player"):ToBlue()
        end
        RefuelZoneHandler(Text, Coord)
    end

    function MarkerOpsRefuelZone:OnAfterMarkChanged(From, Event, To, Text, Keywords, Coord)
        if BlueDebug then
            local m = MESSAGE:New(string.format("%s coordinates recieved", self.Tag), 10, "Info", true):ToAll()
        end
        RefuelZoneHandler(Text, Coord)
    end

    function MarkerOpsRefuelZone:OnAfterMarkDeleted(From, Event, To)
        if BlueDebug then
            local m = MESSAGE:New(string.format("%s Mark Deleted.", self.Tag), 10, "Info", true):ToAll()
        end
    end

    if BlueDebug then
        BASE:I("-----Refuel ZONE LOADED------")
    end
end

RefuelZone()


MESSAGE:New("*MARKEROPS LOADED*", 5, "MISSION", false):ToAll():ToLog()
