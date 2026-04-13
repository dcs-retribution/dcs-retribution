env.info("-----DCSRetribution|MOOSE FlightControl plugin - configuration start ------")

local flightcontrol_options = {
    enableBlue = true,
    enableRed = false,
    useDcsAirbaseAtcFrequencies = true,
    blueFrequency = 251,
    redFrequency = 124,
    useFM = false,
    limitLanding = 2,
    limitLandingTakeoff = 0,
    landingIntervalSeconds = 180,
    limitTaxi = 2,
    taxiIncludeInbound = false,
    limitTaxiLanding = 0,
    taxiSpeedLimitKnots = 25,
    runwayRepairSeconds = 3600,
    markHoldingPatterns = true,
    radioOnlyIfPlayers = true,
    subtitles = true,
    disableSrsRadio = false,
    disableDcsAtc = true,
    enableParkingGuards = true,
    verbosity = 0,
}

if dcsRetribution and dcsRetribution.plugins and dcsRetribution.plugins.flightcontrol then
    local p = dcsRetribution.plugins.flightcontrol

    local function _fc_apply_option(key)
        if p[key] ~= nil then
            flightcontrol_options[key] = p[key]
        end
    end

    _fc_apply_option("enableBlue")
    _fc_apply_option("enableRed")
    _fc_apply_option("useDcsAirbaseAtcFrequencies")
    _fc_apply_option("blueFrequency")
    _fc_apply_option("redFrequency")
    _fc_apply_option("useFM")
    _fc_apply_option("limitLanding")
    _fc_apply_option("limitLandingTakeoff")
    _fc_apply_option("landingIntervalSeconds")
    _fc_apply_option("limitTaxi")
    _fc_apply_option("taxiIncludeInbound")
    _fc_apply_option("limitTaxiLanding")
    _fc_apply_option("taxiSpeedLimitKnots")
    _fc_apply_option("runwayRepairSeconds")
    _fc_apply_option("markHoldingPatterns")
    _fc_apply_option("radioOnlyIfPlayers")
    _fc_apply_option("subtitles")
    _fc_apply_option("disableSrsRadio")
    _fc_apply_option("disableDcsAtc")
    _fc_apply_option("enableParkingGuards")
    _fc_apply_option("verbosity")
else
    env.info("DCSRetribution|FlightControl plugin - settings block not found, using defaults")
end

local function _fc_country_for_airbase(fc, side)
    if fc and fc.GetCountry then
        local country_id = fc:GetCountry()
        if country_id then
            return country_id
        end
    end

    if side == "red" then
        return country.id.RUSSIA
    end
    return country.id.USA
end

local function _fc_coalition_for_airbase(fc, side)
    if fc and fc.GetCoalition then
        local coalition_id = fc:GetCoalition()
        if coalition_id then
            return coalition_id
        end
    end

    if side == "red" then
        return coalition.side.RED
    end
    return coalition.side.BLUE
end

local function _fc_parking_guard_unit_type(side)
    if side == "red" then
        return "Soldier AK"
    end
    return "Soldier M4"
end

local function _fc_parking_guard_template(group_name, side)
    local unit_type = _fc_parking_guard_unit_type(side)

    return {
        visible = false,
        lateActivation = true,
        tasks = {},
        task = "Ground Nothing",
        uncontrolled = false,
        route = {
            points = {
                {
                    x = 0,
                    y = 0,
                    speed = 0,
                    action = "Off Road",
                    task = {
                        id = "ComboTask",
                        params = { tasks = {} },
                    },
                },
            },
        },
        units = {
            {
                x = 0,
                y = 0,
                heading = 0,
                skill = "Excellent",
                type = unit_type,
                playerCanDrive = false,
                name = group_name .. " Unit",
            },
        },
        y = 0,
        x = 0,
        name = group_name,
    }
end

local function _fc_configure_parking_guards(fc, side)
    if not flightcontrol_options.enableParkingGuards then
        return
    end

    local guard_alias = string.format("Parking Guard %s", fc.airbasename)
    local guard_country = _fc_country_for_airbase(fc, side)
    local guard_coalition = _fc_coalition_for_airbase(fc, side)
    local guard_template = _fc_parking_guard_template(guard_alias, side)

    fc.parkingGuard = SPAWN:NewFromTemplate(guard_template, guard_alias)
    fc.parkingGuard:InitCountry(guard_country)
    fc.parkingGuard:InitCategory(Group.Category.GROUND)
    fc.parkingGuard:InitCoalition(guard_coalition)
end

local function _fc_coalition_enabled(side)
    if side == "blue" then
        return flightcontrol_options.enableBlue
    end
    if side == "red" then
        return flightcontrol_options.enableRed
    end
    return false
end

local function _fc_frequency_for_side(side)
    if side == "red" then
        return flightcontrol_options.redFrequency
    end
    return flightcontrol_options.blueFrequency
end

local function _fc_hz_to_mhz(hz)
    local f = tonumber(hz)
    if not f then
        return nil
    end
    return f / 1000000
end

local function _fc_modulation()
    if flightcontrol_options.useFM then
        return radio.modulation.FM
    end
    return radio.modulation.AM
end

local function _fc_pick_airbase_radio(airbase, side)
    if not flightcontrol_options.useDcsAirbaseAtcFrequencies then
        return _fc_frequency_for_side(side), _fc_modulation(), "fallback"
    end

    local mapping_rule = {
        { key = "atc_uhf_hz", label = "UHF" },
        { key = "atc_vhf_high_hz", label = "VHF-HIGH" },
        { key = "atc_vhf_low_hz", label = "VHF-LOW" },
        { key = "atc_hf_hz", label = "HF" },
    }

    for _, candidate in ipairs(mapping_rule) do
        local mhz = _fc_hz_to_mhz(airbase[candidate.key])
        if mhz then
            return mhz, radio.modulation.AM, candidate.label
        end
    end

    return _fc_frequency_for_side(side), _fc_modulation(), "fallback"
end

local function _fc_apply_common_options(fc)
    fc:SetLimitLanding(flightcontrol_options.limitLanding, flightcontrol_options.limitLandingTakeoff)
    fc:SetLandingInterval(flightcontrol_options.landingIntervalSeconds)
    fc:SetLimitTaxi(
        flightcontrol_options.limitTaxi,
        flightcontrol_options.taxiIncludeInbound,
        flightcontrol_options.limitTaxiLanding
    )
    fc:SetRunwayRepairtime(flightcontrol_options.runwayRepairSeconds)
    fc:SetMarkHoldingPattern(flightcontrol_options.markHoldingPatterns)
    fc:SetRadioOnlyIfPlayers(flightcontrol_options.radioOnlyIfPlayers)

    if flightcontrol_options.subtitles then
        fc:SwitchSubtitlesOn()
    else
        fc:SwitchSubtitlesOff()
    end

    if flightcontrol_options.taxiSpeedLimitKnots and flightcontrol_options.taxiSpeedLimitKnots > 0 then
        fc:SetSpeedLimitTaxi(flightcontrol_options.taxiSpeedLimitKnots)
    else
        fc:SetSpeedLimitTaxi(nil)
    end

    fc:SetVerbosity(flightcontrol_options.verbosity)
end

local function _fc_disable_srs_radio(fc)
    if not flightcontrol_options.disableSrsRadio then
        return
    end

    if fc._retributionSrsDisabled then
        return
    end

    function fc:TransmissionTower(Text, Flight, Delay)
        self.Tlastmessage = timer.getAbsTime() + (Delay or 0)
        self:T(self.lid .. string.format("Radio Tower skipped (SRS disabled): %s", tostring(Text)))
    end

    function fc:TransmissionPilot(Text, Flight, Delay)
        self.Tlastmessage = timer.getAbsTime() + (Delay or 0)
        self:T(self.lid .. string.format("Radio Pilot skipped (SRS disabled): %s", tostring(Text)))
    end

    fc._retributionSrsDisabled = true
end

local function _fc_mark_ai_group_ready_for_takeoff(group_name, expected_airbase_name)
    if not group_name then
        return
    end

    if not _DATABASE or not _DATABASE.GetOpsGroup then
        return
    end

    local flight = _DATABASE:GetOpsGroup(group_name)
    if not flight or not flight.isAI or not flight.SetReadyForTakeoff then
        return
    end

    if expected_airbase_name and flight.GetFlightControl then
        local owner_fc = flight:GetFlightControl()
        if owner_fc and owner_fc.airbasename and owner_fc.airbasename ~= expected_airbase_name then
            return
        end
    end

    flight:SetReadyForTakeoff(true)
end

local function _fc_enable_ai_takeoff_readiness_hooks(fc)
    if not flightcontrol_options.enableParkingGuards then
        return
    end

    if fc._retributionAiReadyHooksInstalled then
        return
    end

    local base_birth = fc.OnEventBirth
    local base_engine_startup = fc.OnEventEngineStartup

    function fc:OnEventBirth(EventData)
        if base_birth then
            base_birth(self, EventData)
        end

        if EventData and EventData.IniGroupName then
            self:ScheduleOnce(2, _fc_mark_ai_group_ready_for_takeoff, EventData.IniGroupName, self.airbasename)
        end
    end

    function fc:OnEventEngineStartup(EventData)
        if base_engine_startup then
            base_engine_startup(self, EventData)
        end

        if EventData and EventData.IniGroupName then
            self:ScheduleOnce(0.5, _fc_mark_ai_group_ready_for_takeoff, EventData.IniGroupName, self.airbasename)
        end
    end

    fc._retributionAiReadyHooksInstalled = true
end

local function _fc_is_controlled_by_airbase(flight, airbase_name)
    if not flight or not flight.GetFlightControl then
        return false
    end

    local owner_fc = flight:GetFlightControl()
    return owner_fc and owner_fc.airbasename == airbase_name
end

local function _fc_bind_occupied_parking_flights(fc)
    if not fc or not fc.parking then
        return 0
    end

    local bound = 0

    for _, spot in pairs(fc.parking) do
        if spot and spot.OccupiedBy then
            local unit = UNIT:FindByName(spot.OccupiedBy)
            if unit and unit:IsAlive() then
                local group = unit:GetGroup()
                if group and _DATABASE and _DATABASE.GetOpsGroup then
                    local group_name = group:GetName()
                    local flight = _DATABASE:GetOpsGroup(group_name)

                    if not flight and FLIGHTGROUP and FLIGHTGROUP.New then
                        flight = FLIGHTGROUP:New(group_name)
                    end

                    if flight then
                        local owner_fc = flight.GetFlightControl and flight:GetFlightControl() or nil
                        if owner_fc == nil or owner_fc.airbasename == fc.airbasename then
                            if flight.SetFlightControl and not _fc_is_controlled_by_airbase(flight, fc.airbasename) then
                                flight:SetFlightControl(fc)
                            end

                            if fc.GetFlightStatus and fc.SetFlightStatus then
                                local status = fc:GetFlightStatus(flight)
                                if status == FLIGHTCONTROL.FlightStatus.UNKNOWN then
                                    fc:SetFlightStatus(flight, FLIGHTCONTROL.FlightStatus.PARKING)
                                end
                            end

                            if flight.isAI and flight.SetReadyForTakeoff then
                                flight:SetReadyForTakeoff(true)
                            end

                            bound = bound + 1
                        end
                    end
                end
            end
        end
    end

    return bound
end

local function _fc_cleanup_orphan_parking_guards(fc)
    if not fc or not fc.parking then
        return 0
    end

    local removed = 0

    for _, spot in pairs(fc.parking) do
        if spot and spot.ParkingGuard then
            local keep_guard = false

            if spot.OccupiedBy then
                local unit = UNIT:FindByName(spot.OccupiedBy)
                if unit and unit:IsAlive() then
                    local group = unit:GetGroup()
                    if group and _DATABASE and _DATABASE.GetOpsGroup then
                        local flight = _DATABASE:GetOpsGroup(group:GetName())
                        keep_guard = _fc_is_controlled_by_airbase(flight, fc.airbasename)
                    end
                end
            end

            if not keep_guard then
                fc:RemoveParkingGuard(spot)
                removed = removed + 1
            end
        end
    end

    return removed
end

local function _fc_reconcile_startup_parking(fc, pass, max_passes)
    if not fc then
        return
    end

    local bound = _fc_bind_occupied_parking_flights(fc)
    local removed = _fc_cleanup_orphan_parking_guards(fc)

    if (bound > 0 or removed > 0) and env and env.info then
        env.info(
            string.format(
                "DCSRetribution|FlightControl plugin - startup reconcile at %s: bound=%d, removed_orphan_guards=%d",
                tostring(fc.airbasename),
                bound,
                removed
            )
        )
    end

    local current_pass = tonumber(pass) or 1
    local total_passes = tonumber(max_passes) or 1
    if current_pass < total_passes then
        fc:ScheduleOnce(10, _fc_reconcile_startup_parking, fc, current_pass + 1, total_passes)
    end
end

-- Hook for advanced mission-side customization.
-- If defined elsewhere, this receives every created FLIGHTCONTROL instance and
-- can use the full FLIGHTCONTROL API (holding patterns, parking guards, SRS voices, etc.).
--
-- function FlightControlRetributionConfigure(fc, airbaseName, side)
--     fc:AddHoldingPattern("Batumi Hold Alpha", 320, 15, 6, 12, 10)
-- end

FlightControlRetributionControllers = FlightControlRetributionControllers or {}

local function _fc_configure_airbase(airbase)
    local airbaseName = airbase.name
    local side = airbase.side
    local frequency, modulation, source = _fc_pick_airbase_radio(airbase, side)

    local fc = FLIGHTCONTROL:New(airbaseName, frequency, modulation)
    if not fc then
        env.info("DCSRetribution|FlightControl plugin - failed to create FLIGHTCONTROL for " .. tostring(airbaseName))
        return nil
    end

    _fc_apply_common_options(fc)
    _fc_disable_srs_radio(fc)
    _fc_configure_parking_guards(fc, side)
    _fc_enable_ai_takeoff_readiness_hooks(fc)

    if flightcontrol_options.disableDcsAtc and fc.airbase and fc.airbase.SetRadioSilentMode then
        fc.airbase:SetRadioSilentMode(true)
    end

    if FlightControlRetributionConfigure then
        local ok, err = pcall(FlightControlRetributionConfigure, fc, airbaseName, side)
        if not ok then
            env.info(
                "DCSRetribution|FlightControl plugin - FlightControlRetributionConfigure error for "
                    .. tostring(airbaseName)
                    .. ": "
                    .. tostring(err)
            )
        end
    end

    fc:Start()
    FlightControlRetributionControllers[airbaseName] = fc

    if flightcontrol_options.enableParkingGuards then
        fc:ScheduleOnce(2, _fc_reconcile_startup_parking, fc, 1, 12)
    end

    env.info(
        string.format(
            "DCSRetribution|FlightControl plugin - started at %s (side=%s, %.3f MHz %s, source=%s)",
            tostring(airbaseName),
            tostring(side),
            tonumber(frequency) or 0,
            modulation == radio.modulation.FM and "FM" or "AM",
            tostring(source)
        )
    )

    return fc
end

local function _fc_setup_from_retribution_data()
    local configured = 0

    if not dcsRetribution or not dcsRetribution.Airbases then
        env.info("DCSRetribution|FlightControl plugin - dcsRetribution.Airbases missing")
        return 0
    end

    for _, airbase in pairs(dcsRetribution.Airbases) do
        local name = airbase.name
        local side = airbase.side

        if name and side and _fc_coalition_enabled(side) then
            if not FlightControlRetributionControllers[name] then
                local fc = _fc_configure_airbase(airbase)
                if fc then
                    configured = configured + 1
                end
            end
        end
    end

    return configured
end

local configuredCount = _fc_setup_from_retribution_data()
env.info("DCSRetribution|FlightControl plugin - configured airbases: " .. tostring(configuredCount))

env.info("-----DCSRetribution|MOOSE FlightControl plugin - configuration complete ------")
