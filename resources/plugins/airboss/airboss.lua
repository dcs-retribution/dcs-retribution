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
    ["despawnMinutesAfterLanding"] = 5, -- 0 = disabled, 1/2/3... = minutes after landing before despawn (unless unit shuts down)
}

-- Carrier data lookup table from Retribution
airboss_carrier_data = {}

if dcsRetribution then
    if dcsRetribution.plugins and dcsRetribution.plugins.airboss then
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
        airboss_options.despawnMinutesAfterLanding = dcsRetribution.plugins.airboss.despawnMinutesAfterLanding
    end

    -- Build carrier data lookup table
    if dcsRetribution.Carriers then
        for _, carrier in pairs(dcsRetribution.Carriers) do
            airboss_carrier_data[carrier.unit_name] = carrier
            env.info("AIRBOSS: Loaded carrier data from Retribution for " .. carrier.unit_name)
        end
    end
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

-- Track carriers that Airboss was created for (keyed by UNIT name)
AirbossCarriers = AirbossCarriers or {}

-- Per-unit despawn state
AirbossPendingDespawnUnit = AirbossPendingDespawnUnit or {} -- unitName -> true
AirbossShutdownSeenUnit   = AirbossShutdownSeenUnit   or {} -- unitName -> true

-- RESCUE HELO

function AddRescueHelo(nameOfCarrier)
    env.info("AIRBOSS: Loading Rescue Helo")

    local rescueHeloType = airboss_options.useUH60mod and "UH-60L" or "SH-60B"
    env.info("AIRBOSS: RescueHelo Type = " .. tostring(rescueHeloType))

    -- Ensure BlueNavalUnitSet is initialized
    if not BlueNavalUnitSet then
        BlueNavalUnitSet = SET_UNIT:New():FilterCoalitions("blue"):FilterCategories("ship"):FilterStart()
    end

    local navalUnit = BlueNavalUnitSet:GetFirst()
    local inferredCountryID = navalUnit and navalUnit:GetCountry() or country.id.USA

    -- Generate unique names
    local groupName = UTILS.UniqueName("RescueHeloGroup")
    local unitName = UTILS.UniqueName("RescueHeloUnit")

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
                ["psi"] = 0,
                ["onboard_num"] = "010",
                ["y"] = -206504.32547097,
                ["x"] = 123036.89246336,
                ["name"] = unitName,
                ["payload"] = {
                    ["pylons"] = {},
                    ["fuel"] = 1100,
                    ["flare"] = 30,
                    ["chaff"] = 30,
                    ["gun"] = 100
                },
                ["heading"] = 0,
                ["callsign"] = {
                    [1] = 1,
                    [2] = 1,
                    [3] = 1,
                    ["name"] = "Enfield11"
                }
            }
        },
        ["y"] = -206504.32547097,
        ["x"] = 123036.89246336,
        ["name"] = groupName,
        ["communication"] = true,
        ["start_time"] = 0,
        ["modulation"] = 0,
        ["frequency"] = 127.5
    }

    local SH60 = SPAWN:NewFromTemplate(heli, groupName)
    SH60:InitLateActivated()
    SH60:InitCountry(inferredCountryID)
    SH60:InitCategory(Group.Category.HELICOPTER)
    SH60:InitCoalition(coalition.side.BLUE)

    SH60:OnSpawnGroup(function(grp)
        MESSAGE:New("AIRBOSS: Group Spawned Late Activated: " .. grp:GetName(), 15, "SPAWN"):ToLog()

        local carrierUnit = UNIT:FindByName(nameOfCarrier)
        if not carrierUnit then
            env.info("AIRBOSS: Carrier unit not found: " .. nameOfCarrier)
            return
        end

        local carrierNameLower = string.lower(nameOfCarrier)
        local carrierUnitHeading = carrierUnit:GetHeading()

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

    SH60:Spawn(5)
end

-- S3 TANKER

function AddTrickOrTreat(nameOfCarrier)
    env.info("AIRBOSS: Loading S3 Tanker")

    -- Ensure BlueNavalUnitSet is initialized
    if not BlueNavalUnitSet then
        BlueNavalUnitSet = SET_UNIT:New():FilterCoalitions("blue"):FilterCategories("ship"):FilterStart()
    end

    local navalUnit = BlueNavalUnitSet:GetFirst()
    local inferredCountryID = navalUnit and navalUnit:GetCountry() or country.id.USA

    -- Generate unique names
    local groupName = UTILS.UniqueName("TankerS3Group")
    local unitName = UTILS.UniqueName("TankerS3Unit")

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
                                { ["enabled"] = true, ["auto"] = true, ["id"] = "Tanker", ["number"] = 1, ["params"] = {} },
                                { ["enabled"] = true, ["auto"] = true, ["id"] = "WrappedAction", ["number"] = 2, ["params"] = { ["action"] = { ["id"] = "ActivateBeacon", ["params"] = { ["type"] = 4, ["AA"] = false, ["callsign"] = "TKR", ["system"] = 4, ["channel"] = 1, ["modeChannel"] = "X", ["bearing"] = true, ["frequency"] = 962000000 } } } },
                                { ["enabled"] = true, ["auto"] = true, ["id"] = "WrappedAction", ["number"] = 3, ["params"] = { ["action"] = { ["id"] = "EPLRS", ["params"] = { ["value"] = true, ["groupId"] = 1 } } } },
                                { ["enabled"] = true, ["auto"] = true, ["id"] = "WrappedAction", ["number"] = 4, ["params"] = { ["action"] = { ["id"] = "Option", ["params"] = { ["value"] = true, ["name"] = 35 } } } }
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
        ["hidden"] = false,
        ["units"] = {
            [1] = {
                ["alt"] = 2000,
                ["alt_type"] = "BARO",
                ["skill"] = "High",
                ["speed"] = 82.222222222222,
                ["AddPropAircraft"] = { ["STN_L16"] = "00202", ["VoiceCallsignNumber"] = "11", ["VoiceCallsignLabel"] = "SD" },
                ["type"] = "S-3B Tanker",
                ["psi"] = 0,
                ["onboard_num"] = "011",
                ["y"] = -110857.14285714,
                ["x"] = -18142.857142857,
                ["name"] = unitName,
                ["payload"] = {
                    ["pylons"] = {},
                    ["fuel"] = 6887,
                    ["flare"] = 30,
                    ["chaff"] = 30,
                    ["gun"] = 100
                },
                ["heading"] = 0,
                ["callsign"] = {
                    [1] = 5,
                    [2] = 1,
                    [3] = 1,
                    [4] = "Arco11",
                    ["name"] = "Arco11"
                }
            }
        },
        ["y"] = -110857.14285714,
        ["x"] = -18142.857142857,
        ["name"] = groupName,
        ["communication"] = true,
        ["start_time"] = 0,
        ["modulation"] = 0,
        ["frequency"] = 251
    }

    local S3 = SPAWN:NewFromTemplate(TankerS3, groupName)
    S3:InitLateActivated()
    S3:InitCountry(inferredCountryID)
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

    -- Ensure BlueNavalUnitSet is initialized
    if not BlueNavalUnitSet then
        BlueNavalUnitSet = SET_UNIT:New():FilterCoalitions("blue"):FilterCategories("ship"):FilterStart()
    end

    local navalUnit = BlueNavalUnitSet:GetFirst()
    local inferredCountryID = navalUnit and navalUnit:GetCountry() or country.id.USA

    -- Generate unique names
    local groupName = UTILS.UniqueName("AWACSGroup")
    local unitName = UTILS.UniqueName("AWACSUnit")

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
                                { ["enabled"] = true, ["auto"] = true, ["id"] = "AWACS", ["number"] = 1, ["params"] = {} },
                                { ["enabled"] = true, ["auto"] = true, ["id"] = "WrappedAction", ["number"] = 2, ["params"] = { ["action"] = { ["id"] = "EPLRS", ["params"] = { ["value"] = true, ["groupId"] = 2 } } } },
                                { ["enabled"] = true, ["auto"] = true, ["id"] = "WrappedAction", ["number"] = 3, ["params"] = { ["action"] = { ["id"] = "Option", ["params"] = { ["value"] = true, ["name"] = 35 } } } }
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
        ["hidden"] = false,
        ["units"] = {
            [1] = {
                ["alt"] = 2000,
                ["alt_type"] = "BARO",
                ["livery_id"] = "E-2D Demo",
                ["skill"] = "High",
                ["speed"] = 133.61111111111,
                ["AddPropAircraft"] = {
                    ["STN_L16"] = "00203",
                    ["VoiceCallsignNumber"] = "11",
                    ["VoiceCallsignLabel"] = "OD"
                },
                ["type"] = "E-2C",
                ["psi"] = 0,
                ["onboard_num"] = "012",
                ["y"] = -87714.285714285,
                ["x"] = -36142.857142857,
                ["name"] = unitName,
                ["payload"] = {
                    ["pylons"] = {},
                    ["fuel"] = 5624,
                    ["flare"] = 60,
                    ["chaff"] = 120,
                    ["gun"] = 100
                },
                ["heading"] = 0,
                ["callsign"] = {
                    [1] = 1,
                    [2] = 1,
                    [3] = 1,
                    ["name"] = "Overlord11"
                }
            }
        },
        ["y"] = -87714.285714285,
        ["x"] = -36142.857142857,
        ["name"] = groupName,
        ["communication"] = true,
        ["start_time"] = 0,
        ["modulation"] = 0,
        ["frequency"] = 251
    }

    local E2D = SPAWN:NewFromTemplate(heli, groupName)
    E2D:InitLateActivated()
    E2D:InitCountry(inferredCountryID)
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

    AirbossCarriers[nameOfCarrier] = true
    -- Get carrier data from lookup table
    local carrierData = airboss_carrier_data[nameOfCarrier]

    AirbossRetribution = AIRBOSS:New(nameOfCarrier)
    AirbossRetribution:SetMenuRecovery(30, 20, true)
    AirbossRetribution:SetCarrierControlledArea(airboss_options.rescueHeloDistance)
    AirbossRetribution:SetSoundfilesFolder("l10n/DEFAULT/")
    AirbossRetribution:SetRefuelAI(10)

    -- TACAN/ICLS/Radio configuration based on carrier type
    if carrierType == "CVN" then
        -- Use dynamic values from Retribution if available, otherwise fall back to defaults
        local tacan_channel = 71
        local tacan_band = "X"
        local tacan_callsign = "RID"
        local icls_channel = 11
        local icls_callsign = "RID"
        local lso_radio = 126.5
        local marshal_radio = 127.5

        if carrierData then
            if carrierData.tacan_channel then
                tacan_channel = tonumber(carrierData.tacan_channel)
                env.info("AIRBOSS: Using dynamic TACAN channel: " .. tacan_channel)
            end
            if carrierData.tacan_band then
                tacan_band = carrierData.tacan_band
                env.info("AIRBOSS: Using dynamic TACAN band: " .. tacan_band)
            end
            if carrierData.icls then
                icls_channel = tonumber(carrierData.icls)
                env.info("AIRBOSS: Using dynamic ICLS channel: " .. icls_channel)
            end
            if carrierData.callsign then
                tacan_callsign = carrierData.callsign:sub(1, 3):upper()
                icls_callsign = tacan_callsign
                env.info("AIRBOSS: Using dynamic callsign: " .. tacan_callsign)
            end
        else
            env.info("AIRBOSS: No Retribution data found, using default CVN settings")
        end

        AirbossRetribution:SetTACAN(tacan_channel, tacan_band, tacan_callsign)
        AirbossRetribution:SetICLS(icls_channel, icls_callsign)
        AirbossRetribution:SetLSORadio(lso_radio)
        AirbossRetribution:SetMarshalRadio(marshal_radio)
        AirbossRetribution:Load(nil, "Retribution_CVN_Grades.csv")
        AirbossRetribution:SetAutoSave(nil, "Retribution_CVN_Grades.csv")
        AirbossRetribution:SetTrapSheet(nil, "Retribution_TrapSheet")
    elseif carrierType == "LHA" then
        -- Use dynamic values from Retribution if available, otherwise fall back to defaults
        local tacan_channel = 72
        local tacan_band = "X"
        local tacan_callsign = "LHA"
        local icls_channel = 15
        local icls_callsign = "LHA"
        local lso_radio = 126.6
        local marshal_radio = 127.6

        if carrierData then
            if carrierData.tacan_channel then
                tacan_channel = tonumber(carrierData.tacan_channel)
                env.info("AIRBOSS: Using dynamic TACAN channel: " .. tacan_channel)
            end
            if carrierData.tacan_band then
                tacan_band = carrierData.tacan_band
                env.info("AIRBOSS: Using dynamic TACAN band: " .. tacan_band)
            end
            if carrierData.icls then
                icls_channel = tonumber(carrierData.icls)
                env.info("AIRBOSS: Using dynamic ICLS channel: " .. icls_channel)
            end
            if carrierData.callsign then
                tacan_callsign = carrierData.callsign:sub(1, 3):upper()
                icls_callsign = tacan_callsign
                env.info("AIRBOSS: Using dynamic callsign: " .. tacan_callsign)
            end
        else
            env.info("AIRBOSS: No Retribution data found, using default LHA settings")
        end

        AirbossRetribution:SetTACAN(tacan_channel, tacan_band, tacan_callsign)
        AirbossRetribution:SetICLS(icls_channel, icls_callsign)
        AirbossRetribution:SetLSORadio(lso_radio)
        AirbossRetribution:SetMarshalRadio(marshal_radio)
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

    local cvnUnits = {}
    local lhaUnits = {}
    local escortCandidates = {}

    -- First pass: classify units
    BlueNavalUnitSet:ForEachUnit(function(unt)
        local unitName = unt:GetName()
        local typeUnitName = string.lower(unt:GetName())
        local typeNameLower = string.lower(unt:GetTypeName())
        local group = unt:GetGroup()
        local groupID = group:GetID()
        local groupName = group:GetName()

        BASE:I(string.format("AIRBOSS: %s is a %s (Group: %03d | %s)", unitName, unt:GetTypeName(), groupID, groupName))

        -- CVN detection
        if string.find(typeNameLower, "cvn", 1, true)
            or string.find(typeNameLower, "stennis", 1, true)
            or string.find(typeNameLower, "forrestal", 1, true)
        then
            table.insert(cvnUnits, {
                unit = unt,
                name = unitName,
                groupID = groupID,
                groupName = groupName,
                prefix = tonumber(string.match(unitName, "^(%d+)"))
            })

        -- LHA detection
        elseif string.find(typeNameLower, "lha", 1, true)
            or string.find(typeNameLower, "tarawa", 1, true)
            or string.find(typeNameLower, "hms_invincible", 1, true)
            or string.find(typeNameLower, "essex", 1, true)
        then
            table.insert(lhaUnits, {
                unit = unt,
                name = unitName,
                groupID = groupID,
                groupName = groupName
            })

        -- Escort detection
        elseif string.find(typeNameLower, "arleigh")
            or string.find(typeNameLower, "burke")
            or string.find(typeNameLower, "ticon")
            or string.find(typeNameLower, "bdk")
        then
            table.insert(escortCandidates, {
                unit = unt,
                name = unitName,
                groupID = groupID,
                groupName = groupName,
                prefix = tonumber(string.match(unitName, "^(%d+)"))
            })
        end
    end)

    -- Setup CVNs and match escorts
    for _, cvn in ipairs(cvnUnits) do
        MESSAGE:New("AIRBOSS: CARRIER (CVN) FOUND: " .. cvn.name, 15, "SPAWN"):ToLog()
        SetupAirboss(cvn.name, "CVN")

        if airboss_options.enableRescueHelo then AddRescueHelo(cvn.name) end
        if airboss_options.enableAWACS      then AddShipAWACS(cvn.name) end
        if airboss_options.enableTanker     then AddTrickOrTreat(cvn.name) end

        -- Match escort by prefix +1
        for _, escort in ipairs(escortCandidates) do
            if cvn.prefix and escort.prefix and escort.prefix == cvn.prefix + 1 then
                MESSAGE:New("AIRBOSS: MATCHED ESCORT FOR CVN: " .. escort.name, 10, "RETRIBUTION"):ToLog()
                if not rescueHomeBase then
                    rescueHomeBase = escort.name
                    env.info("AIRBOSS: Rescue Helo Home Base set to ESCORT: " .. rescueHomeBase)
                end
                break -- only use first valid match
            end
        end
    end

    -- Setup LHAs
    for _, lha in ipairs(lhaUnits) do
        if airboss_options.enableForLHA then
            MESSAGE:New("AIRBOSS: CARRIER (LHA) FOUND: " .. lha.name, 15, "SPAWN"):ToLog()
            SetupAirboss(lha.name, "LHA")
            if airboss_options.enableRescueHelo then AddRescueHelo(lha.name) end
        else
            MESSAGE:New("AIRBOSS: LHA FOUND BUT AIRBOSS DISABLED: " .. lha.name, 15, "SPAWN"):ToLog()
        end
    end
end

-- Engine shutdown handler (per-unit). If a unit shuts down before timer expires, we do NOT despawn it.
AirbossEngineStopHandler = AirbossEngineStopHandler or EVENTHANDLER:New()
AirbossEngineStopHandler:HandleEvent(EVENTS.EngineShutdown)
if EVENTS.EngineStop then
    AirbossEngineStopHandler:HandleEvent(EVENTS.EngineStop)
end

local function Airboss_MarkShutdownUnit(EventData)
    if not EventData or not EventData.IniUnit then return end
    local u = EventData.IniUnit

    -- Ignore players/clients
    if u:IsPlayer() then return end

    local unitName = u:GetName()

    -- Only mark shutdown for units that previously landed on a tracked carrier
    -- (i.e., the land handler scheduled them for despawn)
    if not AirbossPendingDespawnUnit[unitName] then
        return
    end

    AirbossShutdownSeenUnit[unitName] = true
    env.info("AIRBOSS: Shutdown detected for tracked unit (will NOT despawn): " .. unitName)
end

function AirbossEngineStopHandler:OnEventEngineShutdown(EventData) Airboss_MarkShutdownUnit(EventData) end
function AirbossEngineStopHandler:OnEventEngineStop(EventData)     Airboss_MarkShutdownUnit(EventData) end

-- Despawn AI aircraft N minutes after they land on a tracked carrier/LHA, unless they shut down.
AirbossLandDespawnHandler = AirbossLandDespawnHandler or EVENTHANDLER:New()
AirbossLandDespawnHandler:HandleEvent(EVENTS.Land)

function AirbossLandDespawnHandler:OnEventLand(EventData)
    if not EventData or not EventData.IniUnit then return end

    -- Option gate
    local minutes = tonumber(airboss_options.despawnMinutesAfterLanding) or 0
    if minutes <= 0 then return end
    local delaySeconds = math.floor(minutes * 60)

    local iniUnit = EventData.IniUnit

    -- Ignore players/clients
    if iniUnit:IsPlayer() then return end

    -- Identify what they landed on (carrier/LHA)
    local placeName = nil

    -- Depending on MOOSE version, land event may provide Place (AIRBASE/UNIT) and/or PlaceName
    if EventData.Place and EventData.Place.GetName then
        placeName = EventData.Place:GetName()
    elseif EventData.PlaceName then
        placeName = EventData.PlaceName
    end

    if not placeName then
        env.info("AIRBOSS: OnEventLand - placeName missing for " .. iniUnit:GetName())
        return
    end

    -- Only act if it's one of the ships we set up Airboss for
    if not AirbossCarriers[placeName] then
        return
    end

    local unitName = iniUnit:GetName()

    -- New landing cycle: clear shutdown protection for this unit
    AirbossShutdownSeenUnit[unitName] = nil

    -- Avoid scheduling twice for the same unit
    if AirbossPendingDespawnUnit[unitName] then return end
    AirbossPendingDespawnUnit[unitName] = true

    env.info(string.format(
        "AIRBOSS: %s landed on %s -> scheduling per-unit despawn in %d seconds",
        unitName, placeName, delaySeconds
    ))

    SCHEDULER:New(nil,
        function()
            AirbossPendingDespawnUnit[unitName] = nil

            local u = UNIT:FindByName(unitName)
            if not u or not u:IsAlive() then return end

            -- If shutdown happened before timer, keep it
            if AirbossShutdownSeenUnit[unitName] then
                env.info("AIRBOSS: " .. unitName .. " shut down before timer; skipping despawn.")
                return
            end

            -- Safety: if airborne again, skip
            local alt = u:GetAltitude()
            if alt and alt > 50 then
                env.info("AIRBOSS: " .. unitName .. " appears airborne again; skipping despawn.")
                return
            end

            env.info("AIRBOSS: Despawning landed AI unit: " .. unitName)

            -- Prefer unit-only destroy if available; otherwise fall back to destroying its group.
            if u.Destroy then
                u:Destroy()
            else
                local g = u:GetGroup()
                if g and g:IsAlive() then
                    env.info("AIRBOSS: UNIT:Destroy not available; destroying group: " .. g:GetName())
                    g:Destroy()
                end
            end
        end,
        {},
        delaySeconds
    )
end

AutoSetup()
