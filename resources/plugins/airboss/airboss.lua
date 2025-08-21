-- assert(loadfile("C:\\Users\\Taco\\Documents\\Github\\DCS\\#Utilities\\AutoSetup.lua"))()
-- RESCUE HELO
function AddRescueHeloMod(nameOfCarrier)
    env.info("----Loading SH60B Helo-----")
    local heli = {

        ["dynSpawnTemplate"] = false,
        ["lateActivation"] = true,
        ["tasks"] = {},
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
                        ["params"] = {
                            ["tasks"] = {}
                        } -- end of ["params"]
                    },    -- end of ["task"]
                    ["type"] = "Turning Point",
                    ["ETA"] = 0,
                    ["ETA_locked"] = true,
                    ["y"] = -135428.57142857,
                    ["x"] = -13285.714285714,
                    ["speed_locked"] = true,
                    ["formation_template"] = ""
                } -- end of [1]
            }     -- end of ["points"]
        },        -- end of ["route"]
        ["groupId"] = 1,
        ["hidden"] = false,
        ["units"] = {
            [1] = {
                ["alt"] = 500,
                ["alt_type"] = "BARO",
                ["livery_id"] = "default",
                ["skill"] = "High",
                ["ropeLength"] = 15,
                ["speed"] = 46.25,
                ["AddPropAircraft"] = {
                    ["SoloFlight"] = false,
                    ["PSGSEAT"] = false,
                    ["SOISEAT"] = false,
                    ["NoASW"] = false
                }, -- end of ["AddPropAircraft"]
                ["type"] = "SH60B",
                ["unitId"] = 1,
                ["psi"] = 0,
                ["onboard_num"] = "010",
                ["y"] = -135428.57142857,
                ["x"] = -13285.714285714,
                ["name"] = "SH60B",
                ["payload"] = {
                    ["pylons"] = {
                        [1] = {
                            ["CLSID"] = "{SH60B_FUEL_TANK_120}"
                        }, -- end of [1]
                        [2] = {
                            ["CLSID"] = "{SH60B_FUEL_TANK_120}"
                        }, -- end of [2]
                        [3] = {
                            ["CLSID"] = "{M299_2xAGM_114K}"
                        }, -- end of [3]
                        [4] = {
                            ["CLSID"] = "{SH60B_FLIRTURRET}"
                        }, -- end of [4]
                        [5] = {
                            ["CLSID"] = "{SH60B_M60}"
                        }, -- end of [5]
                        [6] = {
                            ["CLSID"] = "{SH60B_FUEL_TANK_120_DUMMY}"
                        }, -- end of [6]
                        [7] = {
                            ["CLSID"] = "{SH60B_FUEL_TANK_120_DUMMY}"
                        } -- end of [7]
                    },    -- end of ["pylons"]
                    ["fuel"] = 1362,
                    ["flare"] = 60,
                    ["chaff"] = 30,
                    ["gun"] = 100
                }, -- end of ["payload"]
                ["heading"] = 0,
                ["callsign"] = {
                    [1] = 1,
                    [2] = 1,
                    ["name"] = "Enfield11",
                    [3] = 1
                } -- end of ["callsign"]
            }     -- end of [1]
        },        -- end of ["units"]
        ["y"] = -135428.57142857,
        ["x"] = -13285.714285714,
        ["name"] = "SH60B",
        ["communication"] = true,
        ["start_time"] = 0,
        ["modulation"] = 0,
        ["frequency"] = 124
    } -- end of [1]

    local SH60 = SPAWN:NewFromTemplate(heli, UTILS.UniqueName("SH60B"))
    SH60:InitLateActivated()
    SH60:InitCountry(country.id.CJTF_BLUE)
    SH60:InitCategory(Group.Category.HELICOPTER)
    SH60:InitCoalition(coalition.side.BLUE)
    SH60:OnSpawnGroup(function(grp)
        MESSAGE:New("------Group Spawned Late Activated: " .. grp:GetName(), 15, "SPAWN"):ToLog()
        -- Set as Rescue Helo
        local carrierUnit = UNIT:FindByName(nameOfCarrier)
        carrierUnitHeading = carrierUnit:GetHeading()
        rescueheloTED = RESCUEHELO:New(nameOfCarrier, grp:GetName())
        rescueheloTED:SetRescueOn() -- Helo will rescue downed pilot
        rescueheloTED:SetTakeoffAir()
        rescueheloTED:Start()
    end)
    SH60:Spawn()
end

function AddRescueHeloNoMod(nameOfCarrier)
    env.info("----Loading SH60B Helo-----")

    -- Attempt to find a transport-role helicopter from the mission
    local heloSet = SET_UNIT:New():FilterCoalitions("blue"):FilterCategories("helicopter"):FilterOnce()
    local rescueHeloType = "SH-60B"  -- Default fallback

    heloSet:ForEachUnit(function(unit)
      if unit:IsAlive() then
        local rawUnit = Unit.getByName(unit:GetName())
        if rawUnit then
          local desc = rawUnit:getDesc()
          if desc then
            rescueHeloType = unit:GetTypeName()
            env.info("Using rescue helo type: " .. rescueHeloType)
            env.info("Descriptor description: " .. (desc.description or "N/A"))
            env.info("Descriptor category: " .. tostring(desc.category))
            env.info("Descriptor attributes:")
            for attr, val in pairs(desc.attributes or {}) do
              env.info("  " .. tostring(attr) .. " = " .. tostring(val))
            end
            return
          end
        end
      end
    end)
    

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
                        ["params"] = {
                            ["tasks"] = {}
                        } -- end of ["params"]
                    },    -- end of ["task"]
                    ["type"] = "Turning Point",
                    ["ETA"] = 0,
                    ["ETA_locked"] = true,
                    ["y"] = -206504.32547097,
                    ["x"] = 123036.89246336,
                    ["speed_locked"] = true,
                    ["formation_template"] = ""
                } -- end of [1]
            }     -- end of ["points"]
        },        -- end of ["route"]
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
                }, -- end of ["payload"]
                ["heading"] = 0,
                ["callsign"] = {
                    [1] = 1,
                    [2] = 1,
                    ["name"] = "Enfield11",
                    [3] = 1
                } -- end of ["callsign"]
            }     -- end of [1]
        },        -- end of ["units"]
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
        MESSAGE:New("------Group Spawned Late Activated: " .. grp:GetName(), 15, "SPAWN"):ToLog()
        -- Set as Rescue Helo
        local carrierUnit = UNIT:FindByName(nameOfCarrier)
        carrierUnitHeading = carrierUnit:GetHeading()
        rescueheloTED = RESCUEHELO:New(nameOfCarrier, grp:GetName())
        rescueheloTED:SetRescueOn() -- Helo will rescue downed pilot
        rescueheloTED:SetTakeoffCold()
        rescueheloTED:Start()

        --- Function called when rescue helo is started.
        function rescueheloTED:OnAfterStart(From, Event, To)
            -- Use rescue helo as radio relay for Marshal.

            AirbossRetribution:SetRadioRelayMarshal(self:GetUnitName())
        end
    end)
    SH60:Spawn()
end
  
-------------------------------------------------------------------
---S3 TANKER
-------------------------------------------------------------------

function AddTrickOrTreat(nameOfCarrier)
    env.info("----Loading S3 Tanker-----")
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
                                [1] = {
                                    ["enabled"] = true,
                                    ["auto"] = true,
                                    ["id"] = "Tanker",
                                    ["number"] = 1,
                                    ["params"] = {}
                                }, -- end of [1]
                                [2] = {
                                    ["enabled"] = true,
                                    ["auto"] = true,
                                    ["id"] = "WrappedAction",
                                    ["number"] = 2,
                                    ["params"] = {
                                        ["action"] = {
                                            ["id"] = "ActivateBeacon",
                                            ["params"] = {
                                                ["type"] = 4,
                                                ["AA"] = false,
                                                ["callsign"] = "TKR",
                                                ["system"] = 4,
                                                ["channel"] = 1,
                                                ["modeChannel"] = "X",
                                                ["bearing"] = true,
                                                ["frequency"] = 962000000
                                            } -- end of ["params"]
                                        }     -- end of ["action"]
                                    }         -- end of ["params"]
                                },            -- end of [2]
                                [3] = {
                                    ["enabled"] = true,
                                    ["auto"] = true,
                                    ["id"] = "WrappedAction",
                                    ["number"] = 3,
                                    ["params"] = {
                                        ["action"] = {
                                            ["id"] = "EPLRS",
                                            ["params"] = {
                                                ["value"] = true,
                                                ["groupId"] = 1
                                            } -- end of ["params"]
                                        }     -- end of ["action"]
                                    }         -- end of ["params"]
                                },            -- end of [3]
                                [4] = {
                                    ["enabled"] = true,
                                    ["auto"] = true,
                                    ["id"] = "WrappedAction",
                                    ["number"] = 4,
                                    ["params"] = {
                                        ["action"] = {
                                            ["id"] = "Option",
                                            ["params"] = {
                                                ["value"] = true,
                                                ["name"] = 35
                                            } -- end of ["params"]
                                        }     -- end of ["action"]
                                    }         -- end of ["params"]
                                }             -- end of [4]
                            }                 -- end of ["tasks"]
                        }                     -- end of ["params"]
                    },                        -- end of ["task"]
                    ["type"] = "Turning Point",
                    ["ETA"] = 0,
                    ["ETA_locked"] = true,
                    ["y"] = -110857.14285714,
                    ["x"] = -18142.857142857,
                    ["speed_locked"] = true,
                    ["formation_template"] = ""
                } -- end of [1]
            }     -- end of ["points"]
        },        -- end of ["route"]
        ["groupId"] = 2,
        ["hidden"] = false,
        ["units"] = {
            [1] = {
                ["alt"] = 2000,
                ["alt_type"] = "BARO",
                ["skill"] = "High",
                ["speed"] = 82.222222222222,
                ["AddPropAircraft"] = {
                    ["STN_L16"] = "00202",
                    ["VoiceCallsignNumber"] = "11",
                    ["VoiceCallsignLabel"] = "SD"
                }, -- end of ["AddPropAircraft"]
                ["type"] = "S-3B Tanker",
                ["unitId"] = 2,
                ["psi"] = 0,
                ["onboard_num"] = "011",
                ["y"] = -110857.14285714,
                ["x"] = -18142.857142857,
                ["name"] = "TankerS3",
                ["payload"] = {
                    ["pylons"] = {},
                    ["fuel"] = 6887,
                    ["flare"] = 30,
                    ["chaff"] = 30,
                    ["gun"] = 100
                }, -- end of ["payload"]
                ["heading"] = 0,
                ["callsign"] = {
                    [1] = 5,
                    [2] = 1,
                    [3] = 1,
                    [4] = "Arco11",
                    ["name"] = "Arco11"
                } -- end of ["callsign"]
            }     -- end of [1]
        },        -- end of ["units"]
        ["y"] = -110857.14285714,
        ["x"] = -18142.857142857,
        ["name"] = "TankerS3",
        ["communication"] = true,
        ["start_time"] = 0,
        ["modulation"] = 0,
        ["frequency"] = 251
    } -- end of [1]

    local S3 = SPAWN:NewFromTemplate(TankerS3, UTILS.UniqueName("S3"))
    S3:InitLateActivated()
    S3:InitCountry(country.id.CJTF_BLUE)
    S3:InitCategory(Group.Category.AIRPLANE)
    S3:InitCoalition(coalition.side.BLUE)

    S3:OnSpawnGroup(function(grp)
        MESSAGE:New("------Group Spawned Late Activated: " .. grp:GetName(), 15, "SPAWN"):ToLog()

        -- S3 RECOVERY TANKER SCRIPT
        local S3TED = RECOVERYTANKER:New(UNIT:FindByName(nameOfCarrier), grp:GetName())

        S3TED:SetTACAN(57, "MLR", "Y") -- sets TACAN to 57Y with morse MLR
        S3TED:SetRadio(257, "AM")      -- sets radio to 257 MHz AM

        -- S3TED:SetTakeoffAir()
        S3TED:SetAltitude(8000)
        S3TED:SetSpeed(275)
        S3TED:SetRacetrackDistances(15, 15)
        S3TED:SetHomeBase(nameOfCarrier)
        S3TED:SetUnlimitedFuel(true)
        S3TED:SetCallsign(CALLSIGN.Tanker.Mauler)
        S3TED:__Start(1)

        --- Function called when recovery tanker is started.
        function S3TED:OnAfterStart(From, Event, To)
            -- Set recovery tanker.
            if AirbossRetribution then
                env.info("-------AIRBOSS DETECTED FOR TANKER-----")
                AirbossRetribution:SetRecoveryTanker(S3TED)
                -- Use tanker as radio relay unit for LSO transmissions.
                AirbossRetribution:SetRadioRelayLSO(self:GetUnitName())
            else
                env.info("-------AIRBOSS NOT DETECTED FOR TANKER-----")
            end
        end

        -- Mark display on map updated every 15 minutes
        local S3MarkID = nil

        local function S3Info()
            local CarrierUnit = UNIT:FindByName(nameOfCarrier)
            if CarrierUnit then
                local CarrierCoord = CarrierUnit:GetCoordinate()

                if S3MarkID then
                    CarrierCoord:RemoveMark(S3MarkID)
                end

                -- Use RECOVERYTANKER properties directly
                local tacanString = string.format("%s / %d / %d%s", S3TED.TACANmorse, S3TED.RadioFreq,
                    S3TED.TACANchannel, S3TED.TACANmode)

                S3MarkID = CarrierCoord:TextToAll(tacanString, -1, { 0, 0, 0 }, 1, { 1, 1, 1 }, 0, 25, true)
            else
                env.info("S3Info: Carrier unit not found.")
            end
        end

--        local S3TextTimer = TIMER:New(S3Info)
--        S3TextTimer:Start(30, 900)
    end)
    S3:Spawn()
end

-------------------------------------------------------------------

-------------------------------------------------------------------
-- SHIP AWACS
function AddShipAWACS(nameOfCarrier)
    env.info("----Loading E2D-----")

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
                                [1] = {
                                    ["enabled"] = true,
                                    ["auto"] = true,
                                    ["id"] = "AWACS",
                                    ["number"] = 1,
                                    ["params"] = {}
                                }, -- end of [1]
                                [2] = {
                                    ["enabled"] = true,
                                    ["auto"] = true,
                                    ["id"] = "WrappedAction",
                                    ["number"] = 2,
                                    ["params"] = {
                                        ["action"] = {
                                            ["id"] = "EPLRS",
                                            ["params"] = {
                                                ["value"] = true,
                                                ["groupId"] = 2
                                            } -- end of ["params"]
                                        }     -- end of ["action"]
                                    }         -- end of ["params"]
                                },            -- end of [2]
                                [3] = {
                                    ["enabled"] = true,
                                    ["auto"] = true,
                                    ["id"] = "WrappedAction",
                                    ["number"] = 3,
                                    ["params"] = {
                                        ["action"] = {
                                            ["id"] = "Option",
                                            ["params"] = {
                                                ["value"] = true,
                                                ["name"] = 35
                                            } -- end of ["params"]
                                        }     -- end of ["action"]
                                    }         -- end of ["params"]
                                }             -- end of [3]
                            }                 -- end of ["tasks"]
                        }                     -- end of ["params"]
                    },                        -- end of ["task"]
                    ["type"] = "Turning Point",
                    ["ETA"] = 0,
                    ["ETA_locked"] = true,
                    ["y"] = -87714.285714285,
                    ["x"] = -36142.857142857,
                    ["speed_locked"] = true,
                    ["formation_template"] = ""
                } -- end of [1]
            }     -- end of ["points"]
        },        -- end of ["route"]
        ["groupId"] = 3,
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
                }, -- end of ["AddPropAircraft"]
                ["type"] = "E-2C",
                ["unitId"] = 3,
                ["psi"] = 0,
                ["onboard_num"] = "012",
                ["y"] = -87714.285714285,
                ["x"] = -36142.857142857,
                ["name"] = "E-2D",
                ["payload"] = {
                    ["pylons"] = {},
                    ["fuel"] = "5624",
                    ["flare"] = 60,
                    ["chaff"] = 120,
                    ["gun"] = 100
                }, -- end of ["payload"]
                ["heading"] = 0,
                ["callsign"] = {
                    [1] = 1,
                    [2] = 1,
                    ["name"] = "Overlord11",
                    [3] = 1
                } -- end of ["callsign"]
            }     -- end of [1]
        },        -- end of ["units"]
        ["y"] = -87714.285714285,
        ["x"] = -36142.857142857,
        ["name"] = "E-2D",
        ["communication"] = true,
        ["start_time"] = 0,
        ["modulation"] = 0,
        ["frequency"] = 251
    } -- end of [2]

    local E2D = SPAWN:NewFromTemplate(heli, UTILS.UniqueName("E2D"))
    E2D:InitLateActivated()
    E2D:InitCountry(country.id.CJTF_BLUE)
    E2D:InitCategory(Group.Category.AIRPLANE)
    E2D:InitCoalition(coalition.side.BLUE)
    E2D:OnSpawnGroup(function(grp)
        MESSAGE:New("------Group Spawned Late Activated: " .. grp:GetName(), 15, "SPAWN"):ToLog()
        -- E-2D @ USS Theodore Roosevelt CVN-71 spawning in air.
        awacsTED = RECOVERYTANKER:New(UNIT:FindByName(nameOfCarrier), grp:GetName())
        -- Custom settings:
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
        --- Function called when AWACS is started.
        function awacsTED:OnAfterStart(From, Event, To)
            -- Set AWACS.
            if AirbossRetribution then
                env.info("------AirbossRetribution DETECTED FOR AWACS-----")
                AirbossRetribution:SetAWACS(awacsTED)
            else
                env.info("------AirbossRetribution NOT DETECTED FOR AWACS-----")
            end
        end
    end)
    E2D:Spawn()
end

------------------------------------------------------------------------------------------------------
---AIRBOSS
---------------------------------------------------------------------------------------------------------
function SetupAirboss(nameOfCarrier)
    function ReportDayNightStatusAtBullseye()
        local bullseyeCoord = COORDINATE.GetBullseyeCoordinate(coalition.side.BLUE)
        local isDay = bullseyeCoord:IsDay()

        local function FormatTime(seconds)
            local hours = math.floor(seconds / 3600)
            local minutes = math.floor((seconds % 3600) / 60)
            return string.format("%02d:%02d", hours, minutes)
        end

        -- Get mission time
        local currentTime = timer.getAbsTime()

        local status = isDay and "DAYTIME" or "NIGHTTIME"
        local missionTimeStr = FormatTime(currentTime)

        -- Log to DCS log
        env.info(string.format("[Bullseye Time Report] It is currently %s at the bullseye. Mission Time: %s", status,
            missionTimeStr))

        -- Calculate start and end times
        local recoveryStartTime = currentTime + 1200       -- 20 minute after now
        local recoveryEndTime = currentTime + (5 * 3600) -- 5 hours after now

        local recoveryStartClock = UTILS.SecondsToClock(recoveryStartTime, true)
        local recoveryEndClock = UTILS.SecondsToClock(recoveryEndTime, true)

        -- Log recovery times
        env.info("-----[Recovery Window] Start Time: " .. recoveryStartClock)
        env.info("-----[Recovery Window] End Time: " .. recoveryEndClock)

        if isDay then
            env.info("[Bullseye Logic] Executing daytime behavior------")
            AirbossRetribution:AddRecoveryWindow(recoveryStartClock, recoveryEndClock, 1, nil, true, 25, nil)
        else
            env.info("[Bullseye Logic] Executing nighttime behavior-------")
            AirbossRetribution:AddRecoveryWindow(recoveryStartClock, recoveryEndClock, 3, nil, true, 25, nil)
        end

        return isDay
    end

    AIRBOSS_OPTIONS = {
        ["enableRescueHelo"] = true
    }

    enableRescueHelo = AIRBOSS_OPTIONS.enableRescueHelo

    retribution_enableRescueHelo = enableRescueHelo
    ---
    _SETTINGS:SetPlayerMenuOff(false)
    AirbossRetribution = AIRBOSS:New(nameOfCarrier)
    AirbossRetribution:SetMenuRecovery(30, 20, false)
--    AirbossRetribution:SetMenuSingleCarrier(true)
    AirbossRetribution:SetCarrierControlledArea(80)
    AirbossRetribution:SetSoundfilesFolder("l10n/DEFAULT/")
    AirbossRetribution:SetRefuelAI(10)
    AirbossRetribution:SetTACAN(71, "X", "RID")
    AirbossRetribution:SetICLS(11, "RID")
    AirbossRetribution:SetBeaconRefresh(600)
    AirbossRetribution:SetRecoveryTanker(S3TED)
--    AirbossRetribution:SetAWACS(awacsTED)
    AirbossRetribution:SetLSORadio(126.5)
    AirbossRetribution:SetMarshalRadio(127.5)
--    AirbossRetribution:SetPatrolAdInfinitum(true)
    AirbossRetribution:SetHandleAION()
    AirbossRetribution:SetRadioUnitName(nameOfCarrier)
    AirbossRetribution:SetDespawnOnEngineShutdown()
    AirbossRetribution:Load()
    AirbossRetribution:SetAutoSave()
    ReportDayNightStatusAtBullseye()
    if AIRBOSS_OPTIONS then
        env.info(string.format("MGC Rescue Helo Enabled: AIRBOSS_OPTIONS %s", tostring(AIRBOSS_OPTIONS.enableRescueHelo)))
        env.info(string.format("MGC Rescue Helo Enabled: %s", tostring(enableRescueHelo)))
        env.info(string.format("MGC Rescue Helo Enabled: Retribution %s", tostring(retribution_enableRescueHelo)))
    end
    AirbossRetribution:Start()
--    AirbossRetribution.carrier:CommandActivateLink4()
--    AirbossRetribution.carrier:CommandActivateACLS()

    function AirbossRetribution:OnAfterRecoveryStart(From, Event, To, Case, Offset)
        local case = Case
        env.info("-----CARRIER BEGINNING CASE " .. case .. " RECOVERY------")
    end
end

-- FIND THE CARRIER
local BlueNavalUnitSet = SET_UNIT:New():FilterAlive():FilterCoalitions("blue"):FilterCategories("ship"):FilterOnce()
local function AutoSetup()
    MESSAGE:New("SETTING UP CARRIER ASSETS", 5, "VCAW-1", false):ToAll():ToLog()

    BlueNavalUnitSet:ForEachUnit(function(unt)
        BASE:I(unt:GetName() .. "is a " .. unt:GetTypeName())
        if string.find(string.lower(unt:GetTypeName()), "cvn_71", 1, true) then
            local UID = unt:GetID()
            MESSAGE:New("------CARRIER (CVN 71) FOUND WITH ID:" .. UID .. " " .. unt:GetName(), 15, "SPAWN"):ToLog()
            shipID = UID
--            Flex9SpawnCat1342Parking()
--            FindTransportHeloTemplate()
            SetupAirboss(unt:GetName())
--            AddRescueHeloMod(unt:GetName()) -- Use if you have the SH60B mod
            AddRescueHeloNoMod(unt:GetName())
--            AddShipAWACS(unt:GetName())
            AddTrickOrTreat(unt:GetName())
            return
        end
    end)

    -- MENU
--    TankersAtBulls = MENU_MISSION:New("Tankers at Bulls")                                 -- #MENU
--    TexacoAtBullsMenu = MENU_MISSION_COMMAND:New("Texaco", TankersAtBulls, TexacoAtBulls) -- #MENU
--    ShellAtBullsMenu = MENU_MISSION_COMMAND:New("Shell", TankersAtBulls, ShellAtBulls)    -- #MENU
end

AutoSetup()
