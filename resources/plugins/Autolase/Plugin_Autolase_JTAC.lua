-- Map for passing settings from Retribution
Moose_Autolase_options = {
    ["JtacAlphaSmoke"] = true,
    ["JtacAlphaUHF"] = 250,
    ["JtacAlphaVHF"] = 123,
    ["JtacAlphaRadiusNM"] = 40,
    ["JtacBravoSmoke"] = true,
    ["JtacBravoUHF"] = 251,
    ["JtacBravoVHF"] = 124,
    ["JtacBravoRadiusNM"] = 40
}

-- User configurable variables

local JtacAlphaSmoke = Moose_Autolase_options.JtacAlphaSmoke
local JtacAlphaUHF = Moose_Autolase_options.JtacAlphaUHF
local JtacAlphaVHF = Moose_Autolase_options.JtacAlphaVHF
local JtacAlphaRadiusNM = Moose_Autolase_options.JtacAlphaRadiusNM
local JtacBravoSmoke = Moose_Autolase_options.JtacBravoSmoke
local JtacBravoUHF = Moose_Autolase_options.JtacBravoUHF
local JtacBravoVHF = Moose_Autolase_options.JtacBravoVHF
local JtacBravoRadiusNM = Moose_Autolase_options.JtacBravoRadiusNM

-- Debug output to DCS log
env.info("--------- JtacAlphaSmoke=" .. tostring(JtacAlphaSmoke) ..
    " | JtacAlphaUHF=" .. tostring(JtacAlphaUHF) ..
    " | JtacAlphaVHF=" .. tostring(JtacAlphaVHF) ..
    " | JtacAlphaRadiusNM=" .. tostring(JtacAlphaRadiusNM) ..
    " | JtacBravoSmoke=" .. tostring(JtacBravoSmoke) ..
    " | JtacBravoUHF=" .. tostring(JtacBravoUHF) ..
    " | JtacBravoVHF=" .. tostring(JtacBravoVHF) ..
    " | JtacBravoRadiusNM=" .. tostring(JtacBravoRadiusNM))

BlueDebug = false

--ALPHA
if GROUP:FindByName("JTAC Alpha") then
    env.info("------JTAC Alpha Located-------")
    local JtacAlpha = GROUP:FindByName("JTAC Alpha")
    local JtacAlphaCoord = JtacAlpha:GetCoordinate()
    local AlphaDroneUnit = JtacAlpha:GetUnit(1)
    local JtacAlphaFlightgroup = FLIGHTGROUP:New(JtacAlpha)
    local JtacAlphaName = JtacAlpha:GetName()

    MESSAGE:New("SETTING UP JTAC ALPHA FOR AUTOLASE (MOOSE)", 5, "RETRIBUTION", false):ToAll():ToLog()

    --Short Racetrack
    local AlphaRacetrack = AUFTRAG:NewORBIT_CIRCLE(JtacAlphaCoord, 15000, 120)
    JtacAlphaFlightgroup:SetDefaultInvisible(true)
    JtacAlphaFlightgroup:SetDefaultImmortal(true)
    JtacAlphaFlightgroup:AddMission(AlphaRacetrack)

    local Alpha_AutolaseSet = SET_GROUP:New()
        :FilterPrefixes("Alpha")
        :FilterCoalitions("blue")
        :FilterOnce()

    Alpha_AutolaseSet:AddGroup(JtacAlpha)

    function Alpha_AutolaseSet:OnAfterAdded(From, Event, To, ObjectName, Object)
        env.info("----- " .. ObjectName .. " ADDED TO " .. JtacAlphaName .. " RecceSet -----")
    end

    -- ZONE AROUND DRONE
    local Alpha_DroneZone = ZONE_GROUP:New("Alpha_DroneZone", JtacAlpha, 1852 * JtacAlphaRadiusNM)
    local Alpha_PilotSet = SET_CLIENT:New()
        :FilterCoalitions("blue")
        :FilterZones({ Alpha_DroneZone })
        :FilterActive()
        :FilterStart()

    function Alpha_PilotSet:OnAfterAdded(From, Event, To, ObjectName, Object)
        env.info("----- " .. ObjectName .. " ADDED TO " .. JtacAlphaName .. " PilotSet -----")
    end

    local Alpha_RetributionAutolase = AUTOLASE:New(Alpha_AutolaseSet, coalition.side.BLUE, JtacAlphaName .. " Autolase",
            Alpha_PilotSet)
        :SetMaxLasingTargets(1)
        :SetLasingParameters(10000, 60 * 5)
        :SetNotifyPilots(false)
        :SetSmokeTargets(JtacAlphaSmoke, SMOKECOLOR.Red)
        :EnableSmokeMenu({ Angle = 30, Distance = 40 })

    -- <<<< STORE LATEST LASER DATA HERE
    Alpha_RetributionAutolase._lastLaserInfo = {}

    function Alpha_RetributionAutolase:OnAfterLasing(From, Event, To, LaserSpot)
        if BlueDebug then env.info(JtacAlphaName .. " ------ Laser On!") end

        -- Cache laser info for later use
        self._lastLaserInfo = {
            code = LaserSpot.lasercode or 0,
            mgrs = LaserSpot.coordinate and LaserSpot.coordinate:ToStringMGRS() or "N/A",
            unittype = LaserSpot.unittype or "Unknown",
            reccename = LaserSpot.reccename or "Unknown"
        }

        --Adjust Orbit over LaserSpot
        if LaserSpot.coordinate == nil then
            local TgtCoord = JtacAlphaCoord
            env.info("------JTAC ALPHA: ORBITING IN PLACE-------")
            local NewOrbitInPlace = AUFTRAG:NewORBIT_CIRCLE(TgtCoord, 16000, 120)
            NewOrbitInPlace:SetPriority(1, true, 1)
            JtacAlphaFlightgroup:AddMission(NewOrbitInPlace)
        else
            local TgtCoord = LaserSpot.coordinate
            env.info("------JTAC ALPHA: ORBITING OVER TARGET-------")
            local NewOrbitOverTarget = AUFTRAG:NewORBIT_CIRCLE(TgtCoord, 16000, 120)
            NewOrbitOverTarget:SetPriority(1, true, 1)
            JtacAlphaFlightgroup:AddMission(NewOrbitOverTarget)
        end

        function Alpha_RetributionAutolase:OnAfterTargetDestroyed(From, Event, To, UnitName, RecceName)
            env.info("----JTAC Alpha's target destroyed, repositioning....-----")
            JtacAlphaFlightgroup:PauseMission()
        end

        Alpha_PilotSet:ForEachClient(function(client)
            if client and client:IsAlive() then
                local clientCoord = client:GetCoordinate()
                local laserspot = LaserSpot

                if laserspot and laserspot.coordinate then
                    local BRInfo = laserspot.coordinate:ToStringBR(clientCoord)
                    local text = string.format(
                        "JTAC %s is lasing %s code %d\nat %s\n: %s",
                        laserspot.reccename or "Unknown", laserspot.unittype or "Unknown",
                        laserspot.lasercode or 0, laserspot.coordinate:ToStringMGRS(),
                        BRInfo or "N/A"
                    )

                    -- UHF RADIO
                    local AlphaDroneUnit = JtacAlpha:GetUnit(1)
                    local JtacAlphaRadio = AlphaDroneUnit:GetRadio()
                    JtacAlphaRadio:SetFrequency(JtacAlphaUHF)
                    JtacAlphaRadio:SetModulation(radio.modulation.AM)
                    JtacAlphaRadio:SetPower(100)
                    if Alpha_RetributionAutolase.smoketargets then
                        env.info("-----(UHF) Alpha Smoke is ON-----")
                        JtacAlphaRadio:SetFileName("TargetSmoke.ogg")
                    else
                        env.info("-----(UHF) Alpha Smoke is OFF-----")
                        JtacAlphaRadio:SetFileName("LaserOn.ogg")
                    end
                    JtacAlphaRadio:SetSubtitle(text, 60)
                    JtacAlphaRadio:Broadcast()
                    MESSAGE:New(text, 60, "Alpha"):ToLog()

                    -- VHF RADIO
                    local AlphaDroneUnit = JtacAlpha:GetUnit(1)
                    local JtacAlphaRadio = AlphaDroneUnit:GetRadio()
                    JtacAlphaRadio:SetFrequency(JtacAlphaVHF)
                    JtacAlphaRadio:SetModulation(radio.modulation.AM)
                    JtacAlphaRadio:SetPower(100)
                    if Alpha_RetributionAutolase.smoketargets then
                        env.info("-----(VHF) Alpha Smoke is ON-----")
                        JtacAlphaRadio:SetFileName("TargetSmoke.ogg")
                    else
                        env.info("-----(VHF) Alpha Smoke is OFF-----")
                        JtacAlphaRadio:SetFileName("LaserOn.ogg")
                    end
                    JtacAlphaRadio:SetSubtitle(text, 60)
                    JtacAlphaRadio:Broadcast()
                    MESSAGE:New(text, 60, "Alpha"):ToLog()
                end
            end
        end)
    end

    function Alpha_RetributionAutolase:OnAfterTargetLost(From, Event, To, UnitName, RecceName)
        if BlueDebug then env.info(JtacAlphaName .. " ------ Target Lost!") end
        Alpha_PilotSet:ForEachClient(function(client)
            if client and client:IsAlive() then
                local info = self._lastLaserInfo or {}
                local text = string.format(
                    "%s LOST TARGET\n%s (code %d) at %s",
                    info.reccename or RecceName,
                    info.unittype or "Unknown",
                    info.code or 0,
                    info.mgrs or "Unknown"
                )

                --UHF RADIO
                local AlphaDroneUnit = JtacAlpha:GetUnit(1)
                local JtacAlphaRadio = AlphaDroneUnit:GetRadio()
                JtacAlphaRadio:SetFrequency(JtacAlphaUHF)
                JtacAlphaRadio:SetModulation(radio.modulation.AM)
                JtacAlphaRadio:SetPower(100)
                if Alpha_RetributionAutolase.smoketargets then
                    env.info("-----(UHF) Alpha Smoke is ON-----")
                    JtacAlphaRadio:SetFileName("TargetLost.ogg")
                else
                    env.info("-----(UHF) Alpha Smoke is OFF-----")
                    JtacAlphaRadio:SetFileName("LaserOff.ogg")
                end
                JtacAlphaRadio:SetSubtitle(text, 60)
                JtacAlphaRadio:Broadcast()
                MESSAGE:New(text, 60, "Alpha"):ToLog()

                --VHF RADIO
                local AlphaDroneUnit = JtacAlpha:GetUnit(1)
                local JtacAlphaRadio = AlphaDroneUnit:GetRadio()
                JtacAlphaRadio:SetFrequency(JtacAlphaVHF)
                JtacAlphaRadio:SetModulation(radio.modulation.AM)
                JtacAlphaRadio:SetPower(100)
                if Alpha_RetributionAutolase.smoketargets then
                    env.info("-----(VHF) Alpha Smoke is ON-----")
                    JtacAlphaRadio:SetFileName("TargetLost.ogg")
                else
                    env.info("-----(VHF) Alpha Smoke is OFF-----")
                    JtacAlphaRadio:SetFileName("LaserOff.ogg")
                end
                JtacAlphaRadio:SetSubtitle(text, 60)
                JtacAlphaRadio:Broadcast()
                MESSAGE:New(text, 60, "Alpha"):ToLog()
            end
        end)
    end

    if AlphaDroneUnit then
        local unitName = AlphaDroneUnit:GetName()
        local laserCode = 1688
        Alpha_RetributionAutolase:SetRecceLaserCode(unitName, laserCode)
        Alpha_RetributionAutolase:SetRecceSmokeColor(unitName, SMOKECOLOR.Red)
        env.info(string.format("%s assigned laser code %d", unitName, laserCode))
    end
else
    env.info("------JTAC Alpha NOT Located-------")
end

--BRAVO
if GROUP:FindByName("JTAC Bravo") then
    env.info("------JTAC Bravo Located-------")
    local JtacBravo = GROUP:FindByName("JTAC Bravo")
    local BravoDroneUnit = JtacBravo:GetUnit(1)
    local JtacBravoName = JtacBravo:GetName()
    local JtacBravoCoord = JtacBravo:GetCoordinate()
    local JtacBravoFlightgroup = FLIGHTGROUP:New(JtacBravo)


    MESSAGE:New("SETTING UP JTAC BRAVO FOR AUTOLASE (MOOSE)", 5, "RETRIBUTION", false):ToAll():ToLog()
    --Short Racetrack
    local BravoRacetrack = AUFTRAG:NewORBIT_CIRCLE(JtacBravoCoord, 15000, 120)
    JtacBravoFlightgroup:SetDefaultInvisible(true)
    JtacBravoFlightgroup:SetDefaultImmortal(true)
    JtacBravoFlightgroup:AddMission(BravoRacetrack)

    local Bravo_AutolaseSet = SET_GROUP:New()
        :FilterPrefixes("Bravo")
        :FilterCoalitions("blue")
        :FilterOnce()

    Bravo_AutolaseSet:AddGroup(JtacBravo)

    function Bravo_AutolaseSet:OnAfterAdded(From, Event, To, ObjectName, Object)
        env.info("----- " .. ObjectName .. " ADDED TO " .. JtacBravoName .. " RecceSet -----")
    end

    -- ZONE AROUND DRONE
    local Bravo_DroneZone = ZONE_GROUP:New("Bravo_DroneZone", JtacBravo, 1852 * JtacBravoRadiusNM)
    local Bravo_PilotSet = SET_CLIENT:New()
        :FilterCoalitions("blue")
        :FilterZones({ Bravo_DroneZone })
        :FilterActive()
        :FilterStart()

    function Bravo_PilotSet:OnAfterAdded(From, Event, To, ObjectName, Object)
        env.info("----- " .. ObjectName .. " ADDED TO " .. JtacBravoName .. " PilotSet -----")
    end

    local Bravo_RetributionAutolase = AUTOLASE:New(Bravo_AutolaseSet, coalition.side.BLUE, JtacBravoName .. " Autolase",
            Bravo_PilotSet)
        :SetMaxLasingTargets(1)
        :SetLasingParameters(10000, 60 * 5)
        :SetNotifyPilots(false)
        :SetSmokeTargets(JtacBravoSmoke, SMOKECOLOR.Red)
        :EnableSmokeMenu({ Angle = 30, Distance = 40 })

    -- <<<< STORE LATEST LASER DATA HERE
    Bravo_RetributionAutolase._lastLaserInfo = {}

    function Bravo_RetributionAutolase:OnAfterLasing(From, Event, To, LaserSpot)
        if BlueDebug then env.info(JtacBravoName .. " ------ Laser On!") end

        -- Cache laser info for later use
        self._lastLaserInfo = {
            code = LaserSpot.lasercode or 0,
            mgrs = LaserSpot.coordinate and LaserSpot.coordinate:ToStringMGRS() or "N/A",
            unittype = LaserSpot.unittype or "Unknown",
            reccename = LaserSpot.reccename or "Unknown"
        }
        --Adjust Orbit over LaserSpot
        if LaserSpot.coordinate == nil then
            local TgtCoord = JtacBravoCoord
            env.info("------JTAC BRAVO: ORBITING IN PLACE-------")
            local NewOrbitInPlace = AUFTRAG:NewORBIT_CIRCLE(TgtCoord, 16000, 120)
            NewOrbitInPlace:SetPriority(1, true, 1)
            JtacBravoFlightgroup:AddMission(NewOrbitInPlace)
        else
            local TgtCoord = LaserSpot.coordinate
            env.info("------JTAC BRAVO: ORBITING OVER TARGET-------")
            local NewOrbitOverTarget = AUFTRAG:NewORBIT_CIRCLE(TgtCoord, 16000, 120)
            NewOrbitOverTarget:SetPriority(1, true, 1)
            JtacBravoFlightgroup:AddMission(NewOrbitOverTarget)
        end

        function Bravo_RetributionAutolase:OnAfterTargetDestroyed(From, Event, To, UnitName, RecceName)
            env.info("----JTAC Bravo's target destroyed, repositioning....-----")
            JtacBravoFlightgroup:PauseMission()
        end

        Bravo_PilotSet:ForEachClient(function(client)
            if client and client:IsAlive() then
                local clientCoord = client:GetCoordinate()
                local laserspot = LaserSpot

                if laserspot and laserspot.coordinate then
                    local BRInfo = laserspot.coordinate:ToStringBR(clientCoord)
                    local text = string.format(
                        "JTAC %s is lasing %s code %d\nat %s\n %s",
                        laserspot.reccename or "Unknown", laserspot.unittype or "Unknown",
                        laserspot.lasercode or 0, laserspot.coordinate:ToStringMGRS(),
                        BRInfo or "N/A"
                    )

                    --UHF RADIO
                    local BravoDroneUnit = JtacBravo:GetUnit(1)
                    local JtacBravoRadio = BravoDroneUnit:GetRadio()
                    JtacBravoRadio:SetFrequency(JtacBravoUHF)
                    JtacBravoRadio:SetModulation(radio.modulation.AM)
                    JtacBravoRadio:SetPower(100)
                    if Bravo_RetributionAutolase.smoketargets then
                        env.info("-----(UHF) Bravo Smoke is ON-----")
                        JtacBravoRadio:SetFileName("TargetSmoke.ogg")
                    else
                        env.info("-----(UHF) Bravo Smoke is OFF-----")
                        JtacBravoRadio:SetFileName("LaserOn.ogg")
                    end
                    JtacBravoRadio:SetSubtitle(text, 60)
                    JtacBravoRadio:Broadcast()
                    MESSAGE:New(text, 60, "Bravo"):ToLog()

                    --VHF RADIO
                    local BravoDroneUnit = JtacBravo:GetUnit(1)
                    local JtacBravoRadio = BravoDroneUnit:GetRadio()
                    JtacBravoRadio:SetFrequency(JtacBravoVHF)
                    JtacBravoRadio:SetModulation(radio.modulation.AM)
                    JtacBravoRadio:SetPower(100)
                    if Bravo_RetributionAutolase.smoketargets then
                        env.info("-----(VHF) Bravo Smoke is ON-----")
                        JtacBravoRadio:SetFileName("TargetSmoke.ogg")
                    else
                        env.info("-----(VHF) Bravo Smoke is OFF-----")
                        JtacBravoRadio:SetFileName("LaserOn.ogg")
                    end
                    JtacBravoRadio:SetSubtitle(text, 60)
                    JtacBravoRadio:Broadcast()
                    MESSAGE:New(text, 60, "Bravo"):ToLog()
                end
            end
        end)
    end

    function Bravo_RetributionAutolase:OnAfterTargetLost(From, Event, To, UnitName, RecceName)
        if BlueDebug then env.info(JtacBravoName .. " ------ Target Lost!") end
        Bravo_PilotSet:ForEachClient(function(client)
            if client and client:IsAlive() then
                local info = self._lastLaserInfo or {}
                local message = string.format(
                    "%s LOST TARGET\n%s (code %d) at %s",
                    info.reccename or RecceName,
                    info.unittype or "Unknown",
                    info.code or 0,
                    info.mgrs or "Unknown"
                )

                --UHF RADIO
                local BravoDroneUnit = JtacBravo:GetUnit(1)
                local JtacBravoRadio = BravoDroneUnit:GetRadio()
                JtacBravoRadio:SetFrequency(JtacBravoUHF)
                JtacBravoRadio:SetModulation(radio.modulation.AM)
                JtacBravoRadio:SetPower(100)
                if Bravo_RetributionAutolase.smoketargets then
                    env.info("-----(UHF) Bravo Smoke is ON-----")
                    JtacBravoRadio:SetFileName("TargetLost.ogg")
                else
                    env.info("-----(UHF) Bravo Smoke is OFF-----")
                    JtacBravoRadio:SetFileName("LaserOff.ogg")
                end
                JtacBravoRadio:SetSubtitle(text, 60)
                JtacBravoRadio:Broadcast()
                MESSAGE:New(text, 60, "Bravo"):ToLog()

                --VHF RADIO
                local BravoDroneUnit = JtacBravo:GetUnit(1)
                local JtacBravoRadio = BravoDroneUnit:GetRadio()
                JtacBravoRadio:SetFrequency(JtacBravoVHF)
                JtacBravoRadio:SetModulation(radio.modulation.AM)
                JtacBravoRadio:SetPower(100)
                if Bravo_RetributionAutolase.smoketargets then
                    env.info("-----(VHF) Bravo Smoke is ON-----")
                    JtacBravoRadio:SetFileName("TargetLost.ogg")
                else
                    env.info("-----(VHF) Bravo Smoke is OFF-----")
                    JtacBravoRadio:SetFileName("LaserOff.ogg")
                end
                JtacBravoRadio:SetSubtitle(text, 60)
                JtacBravoRadio:Broadcast()
                MESSAGE:New(text, 60, "Bravo"):ToLog()
            end
        end)
    end

    if BravoDroneUnit then
        local unitName = BravoDroneUnit:GetName()
        local laserCode = 1688
        Bravo_RetributionAutolase:SetRecceLaserCode(unitName, laserCode)
        Bravo_RetributionAutolase:SetRecceSmokeColor(unitName, SMOKECOLOR.Red)
        env.info(string.format("%s assigned laser code %d", unitName, laserCode))
    end
else
    env.info("------JTAC Bravo NOT Located-------")
end
