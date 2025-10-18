-- Original script supplied by Taco
-- Modified/plagiarised/updated for Retribution by Drexyl

-- Retribution Options

airboss_options = {
    ["enableRescueHelo"] = true,
    ["rescueHeloDistance"] = 50,
    ["enableAWACS"] = false,
    ["enableTanker"] = false,
    ["enableForLHA"] = true,
    ["useUH60mod"] = false,
    ["rescueDuration"] = 3,
    ["rescueZoneRadius"] = 50,
    ["windowStartOption"] = 30,
    ["windowLengthOption"] = 30,
}

    if dcsRetribution and dcsRetribution.plugins and dcsRetribution.plugins.airboss then
        airboss_options.enableRescueHelo = dcsRetribution.plugins.airboss.enableRescueHelo
        airboss_options.rescueHeloDistance = dcsRetribution.plugins.airboss.rescueHeloDistance
        airboss_options.enableAWACS = dcsRetribution.plugins.airboss.enableAWACS
        airboss_options.enableTanker = dcsRetribution.plugins.airboss.enableTanker
        airboss_options.enableForLHA = dcsRetribution.plugins.airboss.enableForLHA
        airboss_options.useUH60mod = dcsRetribution.plugins.airboss.useUH60mod
        airboss_options.rescueDuration = dcsRetribution.plugins.airboss.rescueDuration
        airboss_options.rescueZoneRadius = dcsRetribution.plugins.airboss.rescueZoneRadius
        airboss_options.windowStartOption = dcsRetribution.plugins.airboss.windowStartOption
        airboss_options.windowLengthOption = dcsRetribution.plugins.airboss.windowLengthOption
    end

--    env.info("AIRBOSS Rescue Helo Enabled: " .. tostring(airboss_options.enableRescueHelo))
--    env.info("AIRBOSS AWACS Enabled: " .. tostring(airboss_options.enableAWACS))
--    env.info("AIRBOSS Tanker Enabled: " .. tostring(airboss_options.enableTanker))
--    env.info("AIRBOSS LHA Airboss Enabled: " .. tostring(airboss_options.enableForLHA))    
--    env.info("AIRBOSS Rescue Helo Max Distance: " .. tostring(airboss_options.rescueHeloDistance))
--    env.info("AIRBOSS Use UH60 Mod: " .. tostring(airboss_options.useUH60mod))
--    env.info("AIRNOSS Rescue Duration: " .. airboss_options.rescueDuration)
--    env.info("AIRBOSS Rescue Zone Radius: " .. airboss_options.rescueZoneRadius)
--    env.info("AIRBOSS Window Start: " .. airboss_options.windowStartOption)
--    env.info("AIRBOSS Window Length: " .. airboss_options.windowLengthOption)

-- RESCUE HELO

function AddRescueHelo(nameOfCarrier)
    env.info("AIRBOSS: Loading Rescue Helo")

    local rescueHeloType = airboss_options.useUH60mod and "UH-60L" or "SH-60B"
    env.info("AIRBOSS: RescueHelo Type = " .. tostring(rescueHeloType))

    local heli = {
        ["dynSpawnTemplate"] = false,
        ["lateActivation"] = true,
        ["tasks"] = {},
        ["radioSet"] = false,
        ["task"] = "Transport",
        ["uncontrolled"] = false,
        ["route"] = {
            ["routeRelativeTOT"] = true,
            ["points"] = {
                [1] = {
                    ["alt"] = 500,
                    ["action"] = "Turning Point",
                    ["alt_type"] = "BARO",
                    ["speed"] = 46.25,
                    ["task"] = {
                        ["id"] = "ComboTask",
                        ["params"] = { ["tasks"] = {} }
                    },
                    ["type"] = "Turning Point",
                    ["ETA"] = 0,
                    ["ETA_locked"] = true,
                    ["y"] = -206504.32547097,
                    ["x"] = 123036.89246336,
                    ["speed_locked"] = true,
                    ["formation_template"] = ""
                }
            }
        },
        ["groupId"] = 2,
        ["hidden"] = false,
        ["units"] = {
            [1] = {
                ["alt"] = 500,
                ["alt_type"] = "BARO",
                ["livery_id"] = "standard",
                ["skill"] = "High",
                ["ropeLength"] = 15,
                ["speed"] = 46.25,
                ["type"] = rescueHeloType,
                ["unitId"] = 2,
                ["psi"] = 0,
                ["onboard_num"] = "010",
                ["y"] = -206504.32547097,
                ["x"] = 123036.89246336,
                ["name"] = "Rescue Helo Group",
                ["payload"] = {
                    ["pylons"] = {},
                    ["fuel"] = "1100",
                    ["flare"] = 30,
                    ["chaff"] = 30,
                    ["gun"] = 100
                },
                ["heading"] = 0,
                ["callsign"] = {
                    [1] = 1,
                    [2] = 1,
                    ["name"] = "Enfield11",
                    [3] = 1
                }
            }
        },
        ["y"] = -206504.32547097,
        ["x"] = 123036.89246336,
        ["name"] = "Rescue Helo Group",
        ["communication"] = true,
        ["start_time"] = 0,
        ["modulation"] = 0,
        ["frequency"] = 127.5
    }

    local SH60 = SPAWN:NewFromTemplate(heli, UTILS.UniqueName("SH60B"))
    SH60:InitLateActivated()
    SH60:InitCountry(country.id.CJTF_BLUE)
    SH60:InitCategory(Group.Category.HELICOPTER)
    SH60:InitCoalition(coalition.side.BLUE)

    SH60:OnSpawnGroup(function(grp)
        MESSAGE:New("AIRBOSS: Group Spawned Late Activated: " .. grp:GetName(), 15, "SPAWN"):ToLog()

        local carrierUnit = UNIT:FindByName(nameOfCarrier)
        local carrierNameLower = string.lower(nameOfCarrier)
        carrierUnitHeading = carrierUnit:GetHeading()

        rescueheloTED = RESCUEHELO:New(nameOfCarrier, grp:GetName())
        rescueheloTED:SetRescueOn()
        rescueheloTED:SetRescueZone(airboss_options.rescueZoneRadius)
        rescueheloTED:SetRescueDuration(airboss_options.rescueDuration)
        rescueheloTED:SetTakeoffHot()

        if string.find(carrierNameLower, "cvn") and rescueHomeBase then
            rescueheloTED:SetHomeBase(rescueHomeBase)
            env.info("AIRBOSS: Rescue Helo Home Base set to CVN Escort: " .. rescueHomeBase)
        elseif string.find(carrierNameLower, "lha") then
            rescueheloTED:SetHomeBase(nameOfCarrier)
            env.info("AIRBOSS: Rescue Helo Home Base set to LHA: " .. nameOfCarrier)
        end

        -- Assign relay units to this Rescue Helo
        function rescueheloTED:OnAfterStart(From, Event, To)
            local unitName = self:GetUnitName()
            if AirbossRetribution then
                env.info("AIRBOSS: Setting relay units to Rescue Helo: " .. unitName)
                AirbossRetribution:SetRadioRelayMarshal(unitName)
                AirbossRetribution:SetRadioRelayLSO(unitName)
            else
                env.info("AIRBOSS: Rescue Helo not found, relay units not set")
            end
        end

        rescueheloTED:Start()
    end)

    SH60:Spawn()
end

-- S3 TANKER

function AddTrickOrTreat(nameOfCarrier)
    env.info("AIRBOSS: Loading S3 Tanker")
    local TankerS3 = {
        ["dynSpawnTemplate"] = false,
        ["lateActivation"] = true,
        ["tasks"] = {},
        ["task"] = "Refueling",
        ["uncontrolled"] = false,
        ["taskSelected"] = true,
        ["route"] = {
            ["routeRelativeTOT"] = true,
            ["points"] = {
                [1] = {
                    ["alt"] = 2000,
                    ["action"] = "Turning Point",
                    ["alt_type"] = "BARO",
                    ["speed"] = 82.222222222222,
                    ["task"] = {
                        ["id"] = "ComboTask",
                        ["params"] = {
                            ["tasks"] = {
                                [1] = { ["enabled"] = true, ["auto"] = true, ["id"] = "Tanker", ["number"] = 1, ["params"] = {} },
                                [2] = { ["enabled"] = true, ["auto"] = true, ["id"] = "WrappedAction", ["number"] = 2, ["params"] = { ["action"] = { ["id"] = "ActivateBeacon", ["params"] = { ["type"] = 4, ["AA"] = false, ["callsign"] = "TKR", ["system"] = 4, ["channel"] = 1, ["modeChannel"] = "X", ["bearing"] = true, ["frequency"] = 962000000 } } } },
                                [3] = { ["enabled"] = true, ["auto"] = true, ["id"] = "WrappedAction", ["number"] = 3, ["params"] = { ["action"] = { ["id"] = "EPLRS", ["params"] = { ["value"] = true, ["groupId"] = 1 } } } },
                                [4] = { ["enabled"] = true, ["auto"] = true, ["id"] = "WrappedAction", ["number"] = 4, ["params"] = { ["action"] = { ["id"] = "Option", ["params"] = { ["value"] = true, ["name"] = 35 } } } }
                            }
                        }
                    },
                    ["type"] = "Turning Point",
                    ["ETA"] = 0,
                    ["ETA_locked"] = true,
                    ["y"] = -110857.14285714,
                    ["x"] = -18142.857142857,
                    ["speed_locked"] = true,
                    ["formation_template"] = ""
                }
            }
        },
        ["groupId"] = 2,
        ["hidden"] = false,
        ["units"] = {
            [1] = {
                ["alt"] = 2000,
                ["alt_type"] = "BARO",
                ["skill"] = "High",
                ["speed"] = 82.222222222222,
                ["AddPropAircraft"] = { ["STN_L16"] = "00202", ["VoiceCallsignNumber"] = "11", ["VoiceCallsignLabel"] = "SD" },
                ["type"] = "S-3B Tanker",
                ["unitId"] = 2,
                ["psi"] = 0,
                ["onboard_num"] = "011",
                ["y"] = -110857.14285714,
                ["x"] = -18142.857142857,
                ["name"] = "TankerS3",
                ["payload"] = { ["pylons"] = {}, ["fuel"] = 6887, ["flare"] = 30, ["chaff"] = 30, ["gun"] = 100 },
                ["heading"] = 0,
                ["callsign"] = { [1] = 5, [2] = 1, [3] = 1, [4] = "Arco11", ["name"] = "Arco11" }
            }
        },
        ["y"] = -110857.14285714,
        ["x"] = -18142.857142857,
        ["name"] = "TankerS3",
        ["communication"] = true,
        ["start_time"] = 0,
        ["modulation"] = 0,
        ["frequency"] = 251
    }

    local S3 = SPAWN:NewFromTemplate(TankerS3, UTILS.UniqueName("S3"))
    S3:InitLateActivated()
    S3:InitCountry(country.id.CJTF_BLUE)
    S3:InitCategory(Group.Category.AIRPLANE)
    S3:InitCoalition(coalition.side.BLUE)

    S3:OnSpawnGroup(function(grp)
        MESSAGE:New("AIRBOSS: Group Spawned Late Activated: " .. grp:GetName(), 15, "SPAWN"):ToLog()

        local S3TED = RECOVERYTANKER:New(UNIT:FindByName(nameOfCarrier), grp:GetName())
        S3TED:SetTACAN(57, "MLR", "Y")
        S3TED:SetRadio(257, "AM")
        S3TED:SetTakeoffHot()
        S3TED:SetAltitude(8000)
        S3TED:SetSpeed(275)
        S3TED:SetRacetrackDistances(15, 15)
        S3TED:SetHomeBase(nameOfCarrier)
        S3TED:SetUnlimitedFuel(false)
        S3TED:SetCallsign(CALLSIGN.Tanker.Mauler)
        S3TED:__Start(1)

        function S3TED:OnAfterStart(From, Event, To)
            if AirbossRetribution then
                env.info("AIRBOSS: DETECTED FOR TANKER")
                AirbossRetribution:SetRecoveryTanker(S3TED)
            else
                env.info("AIRBOSS: NOT DETECTED FOR TANKER")
            end
        end
    end)
    S3:Spawn()
end

-- SHIP AWACS

function AddShipAWACS(nameOfCarrier)
    env.info("AIRBOSS: Loading E2D for AWACS")

    local heli = {
        ["dynSpawnTemplate"] = false,
        ["lateActivation"] = true,
        ["tasks"] = {},
        ["task"] = "AWACS",
        ["uncontrolled"] = false,
        ["route"] = {
            ["routeRelativeTOT"] = true,
            ["points"] = {
                [1] = {
                    ["alt"] = 2000,
                    ["action"] = "Turning Point",
                    ["alt_type"] = "BARO",
                    ["speed"] = 133.61111111111,
                    ["task"] = {
                        ["id"] = "ComboTask",
                        ["params"] = {
                            ["tasks"] = {
                                [1] = { ["enabled"] = true, ["auto"] = true, ["id"] = "AWACS", ["number"] = 1, ["params"] = {} },
                                [2] = { ["enabled"] = true, ["auto"] = true, ["id"] = "WrappedAction", ["number"] = 2, ["params"] = { ["action"] = { ["id"] = "EPLRS", ["params"] = { ["value"] = true, ["groupId"] = 2 } } } },
                                [3] = { ["enabled"] = true, ["auto"] = true, ["id"] = "WrappedAction", ["number"] = 3, ["params"] = { ["action"] = { ["id"] = "Option", ["params"] = { ["value"] = true, ["name"] = 35 } } } }
                            }
                        }
                    },
                    ["type"] = "Turning Point",
                    ["ETA"] = 0,
                    ["ETA_locked"] = true,
                    ["y"] = -87714.285714285,
                    ["x"] = -36142.857142857,
                    ["speed_locked"] = true,
                    ["formation_template"] = ""
                }
            }
        },
        ["groupId"] = 3,
        ["hidden"] = false,
        ["units"] = {
            [1] = {
                ["alt"] = 2000,
                ["alt_type"] = "BARO",
                ["livery_id"] = "E-2D Demo",
                ["skill"] = "High",
                ["speed"] = 133.61111111111,
                ["AddPropAircraft"] = { ["STN_L16"] = "00203", ["VoiceCallsignNumber"] = "11", ["VoiceCallsignLabel"] = "OD" },
                ["type"] = "E-2C",
                ["unitId"] = 3,
                ["psi"] = 0,
                ["onboard_num"] = "012",
                ["y"] = -87714.285714285,
                ["x"] = -36142.857142857,
                ["name"] = "E-2D",
                ["payload"] = { ["pylons"] = {}, ["fuel"] = "5624", ["flare"] = 60, ["chaff"] = 120, ["gun"] = 100 },
                ["heading"] = 0,
                ["callsign"] = { [1] = 1, [2] = 1, ["name"] = "Overlord11", [3] = 1 }
            }
        },
        ["y"] = -87714.285714285,
        ["x"] = -36142.857142857,
        ["name"] = "E-2D",
        ["communication"] = true,
        ["start_time"] = 0,
        ["modulation"] = 0,
        ["frequency"] = 251
    }

    local E2D = SPAWN:NewFromTemplate(heli, UTILS.UniqueName("E2D"))
    E2D:InitLateActivated()
    E2D:InitCountry(country.id.CJTF_BLUE)
    E2D:InitCategory(Group.Category.AIRPLANE)
    E2D:InitCoalition(coalition.side.BLUE)
    E2D:OnSpawnGroup(function(grp)
        MESSAGE:New("AIRBOSS: Group Spawned Late Activated: " .. grp:GetName(), 15, "SPAWN"):ToLog()

        awacsTED = RECOVERYTANKER:New(UNIT:FindByName(nameOfCarrier), grp:GetName())
        awacsTED:SetAWACS()
        awacsTED:SetCallsign(CALLSIGN.AWACS.Wizard)
        awacsTED:SetTakeoffAir()
        awacsTED:SetAltitude(25000)
        awacsTED:SetSpeed(275)
        awacsTED:SetRadio(254)
        awacsTED:SetTACAN(55, "WIZ")
        awacsTED:SetRacetrackDistances(20, 20)
        awacsTED:SetHomeBase(nameOfCarrier)
        awacsTED:SetUnlimitedFuel(true)
        awacsTED:__Start(1)

        function awacsTED:OnAfterStart(From, Event, To)
            if AirbossRetribution then
                env.info("AIRBOSS: DETECTED FOR AWACS")
                AirbossRetribution:SetAWACS(awacsTED)
            else
                env.info("AIRBOSS: NOT DETECTED FOR AWACS")
            end
        end
    end)
    E2D:Spawn()
end

-- AIRBOSS

function SetupAirboss(nameOfCarrier, carrierType)
    function ReportDayNightStatusAtBullseye()
        local bullseyeCoord = COORDINATE.GetBullseyeCoordinate(coalition.side.BLUE)
        local isDay = bullseyeCoord:IsDay()

        local function FormatTime(seconds)
            local hours = math.floor(seconds / 3600)
            local minutes = math.floor((seconds % 3600) / 60)
            return string.format("%02d:%02d", hours, minutes)
        end

        local currentTime = timer.getAbsTime()
        local status = isDay and "DAYTIME" or "NIGHTTIME"
        local missionTimeStr = FormatTime(currentTime)
        env.info(string.format("AIRBOSS: [Bullseye Time Report] It is currently %s at the bullseye. Mission Time: %s", status, missionTimeStr))

        local recoveryStartTime = currentTime + (60 * airboss_options.windowStartOption)
        local recoveryEndTime = recoveryStartTime + (60 * airboss_options.windowLengthOption)
        local recoveryStartClock = UTILS.SecondsToClock(recoveryStartTime, true)
        local recoveryEndClock = UTILS.SecondsToClock(recoveryEndTime, true)

        env.info("AIRBOSS: [Recovery Window] Start Time: " .. recoveryStartClock)
        env.info("AIRBOSS: [Recovery Window] End Time: " .. recoveryEndClock)

        if isDay then
            env.info("AIRBOSS: [Bullseye Logic] Executing daytime behavior")
            AirbossRetribution:AddRecoveryWindow(recoveryStartClock, recoveryEndClock, 1, nil, true, 20, true)
        else
            env.info("AIRBOSS: [Bullseye Logic] Executing nighttime behavior")
            AirbossRetribution:AddRecoveryWindow(recoveryStartClock, recoveryEndClock, 3, nil, true, 20, true)
        end

        return isDay
    end

    AirbossRetribution = AIRBOSS:New(nameOfCarrier)
    AirbossRetribution:SetMenuRecovery(30, 20, true)
    AirbossRetribution:SetCarrierControlledArea(airboss_options.rescueHeloDistance)
    AirbossRetribution:SetSoundfilesFolder("l10n/DEFAULT/")
    AirbossRetribution:SetRefuelAI(10)

    -- TACAN/ICLS/Radio configuration based on carrier type
    if carrierType == "CVN" then
        AirbossRetribution:SetTACAN(71, "X", "RID")
        AirbossRetribution:SetICLS(11, "RID")
        AirbossRetribution:SetLSORadio(126.5)
        AirbossRetribution:SetMarshalRadio(127.5)
        AirbossRetribution:Load(nil, "Retribution_CVN_Grades.csv")
        AirbossRetribution:SetAutoSave(nil, "Retribution_CVN_Grades.csv")
        AirbossRetribution:SetTrapSheet(nil, "Retribution_TrapSheet")
    elseif carrierType == "LHA" then
        AirbossRetribution:SetTACAN(72, "X", "LHA")
        AirbossRetribution:SetICLS(15, "LHA")
        AirbossRetribution:SetLSORadio(126.6)
        AirbossRetribution:SetMarshalRadio(127.6)
        AirbossRetribution:Load(nil, "Retribution_LHA_Grades.csv")
        AirbossRetribution:SetAutoSave(nil, "Retribution_LHA_Grades.csv")
    end

    AirbossRetribution:SetBeaconRefresh(600)
    AirbossRetribution:SetHandleAION()
    AirbossRetribution:SetRadioUnitName(nameOfCarrier)
    AirbossRetribution:SetDespawnOnEngineShutdown()
    AirbossRetribution:SetCollisionDistance(15)
    AirbossRetribution:SetCarrierIllumination(-1)
    AirbossRetribution:SetExtraVoiceOvers(true)
    ReportDayNightStatusAtBullseye()

    if MSRS_Config then
        env.info("AIRBOSS: MSRS configuration file was loaded, Setting SRS to Active.")
        AirbossRetribution:EnableSRS()
    else
        env.info("AIRBOSS: MSRS Configuration File not loaded, falling back to Soundfiles")
    end

    AirbossRetribution:Start()

    function AirbossRetribution:OnAfterRecoveryStart(From, Event, To, Case, Offset)
        env.info("AIRBOSS: CARRIER BEGINNING CASE " .. Case .. " RECOVERY")
    end
end

local BlueNavalUnitSet = SET_UNIT:New():FilterAlive():FilterCoalitions("blue"):FilterCategories("ship"):FilterOnce()
rescueHomeBase = nil

local function AutoSetup()
    MESSAGE:New("AIRBOSS: SETTING UP CARRIER ASSETS", 5, "RETRIBUTION", false):ToAll():ToLog()

    local cvnGroupID = nil
    local cvnTaskName = nil

    BlueNavalUnitSet:ForEachUnit(function(unt)
        local unitName = unt:GetName()
        local typeName = unt:GetTypeName()
        local typeNameLower = string.lower(typeName)
        local group = unt:GetGroup()
        local groupID = group:GetID()
        local groupName = group:GetName()

        BASE:I(string.format("AIRBOSS: %s is a %s (Group: %03d | %s)", unitName, typeName, groupID, groupName))

        -- CVN detection
        if string.find(typeNameLower, "cvn_71", 1, true) then
            MESSAGE:New("AIRBOSS: CARRIER (CVN) FOUND: " .. unitName, 15, "SPAWN"):ToLog()
            SetupAirboss(unitName, "CVN")

            cvnGroupID = groupID
            cvnTaskName = string.match(groupName, "^(%S+)")

            if airboss_options.enableRescueHelo then AddRescueHelo(unitName) end
            if airboss_options.enableAWACS      then AddShipAWACS(unitName) end
            if airboss_options.enableTanker     then AddTrickOrTreat(unitName) end

        -- LHA detection
        elseif (string.find(typeNameLower, "lha") or string.find(typeNameLower, "tarawa")) and airboss_options.enableForLHA then
            MESSAGE:New("AIRBOSS: CARRIER (LHA) FOUND: " .. unitName, 15, "SPAWN"):ToLog()
            SetupAirboss(unitName, "LHA")
            if airboss_options.enableRescueHelo then AddRescueHelo(unitName) end

        elseif string.find(typeNameLower, "lha") or string.find(typeNameLower, "tarawa") then
            MESSAGE:New("AIRBOSS: LHA FOUND BUT AIRBOSS DISABLED: " .. unitName, 15, "SPAWN"):ToLog()

        -- DDG/CG detection with task match or groupID offset
        elseif string.find(typeNameLower, "arleigh") or string.find(typeNameLower, "burke") or string.find(typeNameLower, "ticon") then
            local escortTaskName = string.match(groupName, "^(%S+)")
            if (cvnGroupID and groupID == cvnGroupID + 1) or (cvnTaskName and escortTaskName == cvnTaskName) then
                MESSAGE:New("AIRBOSS: MATCHED ESCORT FOR CVN: " .. unitName, 10, "RETRIBUTION"):ToLog()
                -- Set rescueHomeBase to first matched escort
                if not rescueHomeBase then
                    rescueHomeBase = unitName
                    env.info("AIRBOSS: Rescue Helo Home Base set to ESCORT: " .. rescueHomeBase)
                end
            else
                MESSAGE:New("AIRBOSS: UNMATCHED ESCORT: " .. unitName, 10, "RETRIBUTION"):ToLog()
            end
        end
    end)
end

AutoSetup()
