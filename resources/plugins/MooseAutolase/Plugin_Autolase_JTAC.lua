env.info("-----DCSRetribution|MOOSE Autolase plugin - configuration start ------")

-- Defaults (overridden by dcsRetribution.plugins.MooseAutolase when present)
DangerCloseNM            = 1
AutolaseSmokeDurationSec = 180
MooseAutolaseDebug       = false
UseConvoyChaosSFX        = true -- NEW: set false if ConvoyChaos.ogg not in mission

-- Pull from UI if available
if dcsRetribution and dcsRetribution.plugins and dcsRetribution.plugins.MooseAutolase then
    local p                  = dcsRetribution.plugins.MooseAutolase
    DangerCloseNM            = p.DangerCloseNM
    AutolaseSmokeDurationSec = p.AutolaseSmokeDurationSec
    MooseAutolaseDebug       = p.MooseAutolaseDebug
    if p.UseConvoyChaosSFX ~= nil then UseConvoyChaosSFX = p.UseConvoyChaosSFX end
else
    env.info("-----dcsRetribution.plugins.MooseAutolase NOT FOUND")
end

-- Debug output to DCS log
env.info("--------- DangerCloseNM=" .. tostring(DangerCloseNM) ..
    " | UseConvoyChaosSFX=" .. tostring(UseConvoyChaosSFX) ..
    " | MooseAutolaseDebug=" .. tostring(MooseAutolaseDebug) ..
    " | AutolaseSmokeDurationSec=" .. tostring(AutolaseSmokeDurationSec)
)

-----------------------------------------------------------------
-- COORDINATE:Smoke duration override (uses AutolaseSmokeDurationSec when duration omitted)
-----------------------------------------------------------------
if not _G.__CoordSmokePatched and COORDINATE and COORDINATE.Smoke then
    _G.__CoordSmokePatched = true
    COORDINATE._Smoke_original = COORDINATE._Smoke_original or COORDINATE.Smoke
    function COORDINATE:Smoke(color, duration, delay, name, offset, direction, distance)
        local useDuration = (duration ~= nil) and duration or AutolaseSmokeDurationSec
        if MooseAutolaseDebug and duration == nil then
            env.info(string.format("[AutolaseSmokePatch] default duration %ds (color=%s)", useDuration, tostring(color)))
        end
        return COORDINATE._Smoke_original(self, color, useDuration, delay, name, offset, direction, distance)
    end
end

-- Safe AM constant
local AM = (radio and radio.modulation and radio.modulation.AM) or 0

-----------------------------------------------------------------
-- JTAC target-prioritization config (Part 1)
-- File-scope so the monkeypatch closure below can capture these.
-----------------------------------------------------------------
local _p = (dcsRetribution and dcsRetribution.plugins and dcsRetribution.plugins.MooseAutolase) or nil
local TierSamThreats     = (_p and _p.TierSamThreats)     or 1
local TierGuidedAaa      = (_p and _p.TierGuidedAaa)      or 2
local TierArtillery      = (_p and _p.TierArtillery)      or 3
local TierUnguidedAaa    = (_p and _p.TierUnguidedAaa)    or 3
local TierArmorLaunchers = (_p and _p.TierArmorLaunchers) or 4
local TierOther          = (_p and _p.TierOther)          or 5

MooseAutolaseUnitClasses        = (_p and _p.UnitClasses)        or {}
MooseAutolaseFrontlines         = (_p and _p.Frontlines)         or {}
MooseAutolaseDefaultCorridorM   = (_p and _p.DefaultCorridorM)   or 8000
MooseAutolaseArtilleryCorridorM = (_p and _p.ArtilleryCorridorM) or 18000

-- New injected-config reads (Task 5a/6): per-frontline list + shared defaults
local MooseAutolaseJTACs   = (_p and _p.JTACs) or {}
local JtacSmoke            = (_p and _p.JtacSmoke)
if JtacSmoke == nil then JtacSmoke = true end
-- JtacsPerFrontline is expressed by the COUNT of flat entries in
-- MooseAutolaseJTACs (one AUTOLASE instance per drone); each entry's
-- def.maxLasing is always 1. There is no file-scope use of the raw option.
local JtacRadiusNM         = (_p and _p.JtacRadiusNM)   or 50

-- B+ deconfliction: per-front-line set of unit names currently lased by any
-- drone on that front. Each cycle a drone REBUILDS its own claims from its live
-- CurrentLasing and skips targets another drone claims; when every candidate is
-- claimed (live targets < drones) drones double up on the highest-priority
-- target. Reset fresh each script load.
-- LIMITATION: a claim is freed when the lase ends (the next monitor cycle's
-- rebuild drops it) or proactively by the target-lost/destroyed handlers. If a
-- drone's GROUP is despawned externally (no further cycles, no target events),
-- its last claims leak for the session and those unit names stay excluded from
-- *unclaimed* selection on that front. The double-up fallback still lets
-- surviving drones lase them, so this only degrades deconfliction — it never
-- blocks lasing. Front-line JTACs spawn immortal/invisible, so despawn-on-death
-- does not occur in practice.
-- Persist across script re-execution (DCS reload / a Lua test harness loading the
-- file twice): match the _G.__...Patched guards above so the already-patched
-- onafterMonitor closure and a freshly-loaded setupJtac share ONE claim table.
_G.__MooseAutolaseClaims = _G.__MooseAutolaseClaims or {}
local MooseAutolaseClaims = _G.__MooseAutolaseClaims

-- Fixed UnitClass -> category map (categories carry the configurable tier).
local CategoryByClass = {
    TrackRadar = "SamThreats", SearchTrackRadar = "SamThreats",
    TELAR = "SamThreats", SpecializedRadar = "SamThreats",
    OpticalTracker = "SamThreats", Manpad = "SamThreats", SHORAD = "SamThreats",
    Artillery = "Artillery",
    Tank = "ArmorLaunchers", APC = "ArmorLaunchers", IFV = "ArmorLaunchers",
    ATGM = "ArmorLaunchers", Launcher = "ArmorLaunchers",
    -- AAA is split at runtime (see jtacCategoryFor); everything else -> Other.
}

local TierByCategory = {
    SamThreats = TierSamThreats, GuidedAaa = TierGuidedAaa,
    Artillery = TierArtillery, UnguidedAaa = TierUnguidedAaa,
    ArmorLaunchers = TierArmorLaunchers, Other = TierOther,
}

local function jtacCategoryFor(unit)
    local cls = MooseAutolaseUnitClasses[unit:GetTypeName()]
    if cls == "AAA" then
        if unit:HasAttribute("RADAR_BAND1_FOR_ARM")
            or unit:HasAttribute("RADAR_BAND2_FOR_ARM")
            or unit:HasAttribute("Optical Tracker") then
            return "GuidedAaa"
        end
        return "UnguidedAaa"
    end
    return CategoryByClass[cls or ""] or "Other"
end

local function jtacTierFor(category)
    return TierByCategory[category] or TierOther
end

-- Perpendicular distance (m) from point P to segment AB, all DCS vec2 {x,y}.
local function pointSegmentDistance(px, py, ax, ay, bx, by)
    local dx, dy = bx - ax, by - ay
    local len2 = dx * dx + dy * dy
    local t = 0
    if len2 > 0 then
        t = ((px - ax) * dx + (py - ay) * dy) / len2
        if t < 0 then t = 0 elseif t > 1 then t = 1 end
    end
    local cx, cy = ax + t * dx, ay + t * dy
    local ex, ey = px - cx, py - cy
    return math.sqrt(ex * ex + ey * ey)
end

-----------------------------------------------------------------
-- Part 2: monkeypatch AUTOLASE:onafterMonitor with tier + frontline-box
-- selection. Guarded exactly like the COORDINATE:Smoke patch above.
-----------------------------------------------------------------
if not _G.__AutolaseTierPatched and AUTOLASE then
    _G.__AutolaseTierPatched = true
    AUTOLASE._onafterMonitor_tierOriginal = AUTOLASE.onafterMonitor

    function AUTOLASE:onafterMonitor(From, Event, To)
        self:T({From, Event, To})
        -- Fall back to stock behaviour when this instance has no frontline
        -- segment or the class table is missing (e.g. >2 JTACs, no front).
        if not self._frontlineSegment or not next(MooseAutolaseUnitClasses) then
            return AUTOLASE._onafterMonitor_tierOriginal(self, From, Event, To)
        end

        self:CleanCurrentLasing()
        self:SetPilotMenu()

        local seg = self._frontlineSegment
        local boxed, unboxed = {}, {}

        -- Stock onafterMonitor maintains GroupsByThreat/UnitsByThreat/RecceNames/
        -- RecceUnitNames, but those are single-cycle scratch read only within stock
        -- onafterMonitor (which this patch fully replaces). The pilot Status menu and
        -- CheckIsLased/CleanCurrentLasing run off self.CurrentLasing, which we still
        -- populate in the lasing loop below, so we don't rebuild the unused tables.
        for _, contact in pairs(self.Contacts or {}) do
            local grp = contact.group
            if grp and grp:IsGround() then
                local units = grp:GetUnits() or {}
                for _, unit in pairs(units) do
                    if unit and unit:IsAlive() then
                        local category = jtacCategoryFor(unit)
                        local tier = jtacTierFor(category)
                        if tier > 0 then  -- 0 = Don't lase
                            local vec = unit:GetVec2()
                            local corridor = (category == "Artillery")
                                and MooseAutolaseArtilleryCorridorM
                                or MooseAutolaseDefaultCorridorM
                            local dist = pointSegmentDistance(
                                vec.x, vec.y, seg.a.x, seg.a.y, seg.b.x, seg.b.y)
                            local entry = {
                                unit = unit, tier = tier,
                                threat = unit:GetThreatLevel() or 0,
                            }
                            table.insert(unboxed, entry)
                            if dist <= corridor then
                                table.insert(boxed, entry)
                            end
                        end
                    end
                end
            end
        end

        -- Box-empty fallback: open up to everything in lase range.
        local chosen = (#boxed > 0) and boxed or unboxed

        -- Highest priority first: lowest tier number, then highest threat.
        table.sort(chosen, function(a, b)
            if a.tier ~= b.tier then return a.tier < b.tier end
            return a.threat > b.threat
        end)

        -- B+ deconfliction via a shared per-front-line claim set
        -- (MooseAutolaseClaims[region] = set of unit names currently lased by any
        -- drone on that front). We REBUILD this instance's claims from its own live
        -- CurrentLasing every cycle (CleanCurrentLasing above already dropped dead/
        -- expired spots), so a claim lives exactly as long as the lase does and
        -- self-heals without depending on the pick path running each cycle.
        local region = self._frontlineRegion
        local claims = MooseAutolaseClaims[region]
        if not claims then claims = {}; MooseAutolaseClaims[region] = claims end
        local mine = {}
        if self._claimedUnits then
            for u in pairs(self._claimedUnits) do claims[u] = nil end
        end
        for _, ls in pairs(self.CurrentLasing or {}) do
            local n = ls and ls.unitname
            if n then mine[n] = true; claims[n] = true end
        end
        self._claimedUnits = mine

        for _, detectingunit in pairs(self.RecceUnits) do
            local reccename = detectingunit.name
            local recce = detectingunit.unit
            local reccecount = self.targetsperrecce[reccename] or 0
            if reccecount < self.maxlasing then
                local pick, fallback = nil, nil
                for _, entry in pairs(chosen) do
                    local unit = entry.unit
                    local uname = unit:GetName()
                    -- IsAlive + coordinate guard: GetCoordinate is nil for a unit
                    -- that died this frame; skip it so we never deref nil below.
                    if unit:IsAlive() and unit:GetCoordinate()
                        and not self:CheckIsLased(uname)
                        and self:CanLase(recce, unit) then
                        -- fallback = highest-priority laseable unit, claimed or not.
                        if not fallback then fallback = unit end
                        -- pick = first laseable unit no OTHER drone on this front has
                        -- claimed (mine[] are our own current lases, free to retake).
                        if not claims[uname] or mine[uname] then pick = unit; break end
                    end
                end
                -- Double up on the top-priority target only when every laseable
                -- candidate is already claimed by another drone (live targets < drones).
                local unit = pick or fallback
                -- One GetCoordinate reused throughout the lase block. Guard it
                -- defensively: the pick guard already required a coordinate and a
                -- single Lua callback cannot yield, so c is non-nil on the normal
                -- path — the guard just avoids any nil deref if that ever changes.
                local c = unit and unit:GetCoordinate()
                if unit and c then
                    local uname = unit:GetName()
                    local code = self:GetLaserCode(reccename)
                    local spot = SPOT:New(recce)
                    spot:LaseOn(unit, code, self.LaseDuration)
                    local locationstring = c:ToStringLLDDM()
                    if _SETTINGS:IsA2G_MGRS() then
                        local precision = _SETTINGS:GetMGRS_Accuracy()
                        local settings = {}
                        settings.MGRS_Accuracy = precision
                        locationstring = c:ToStringMGRS(settings)
                    elseif _SETTINGS:IsA2G_LL_DMS() then
                        locationstring = c:ToStringLLDMS(_SETTINGS)
                    elseif _SETTINGS:IsA2G_BR() then
                        locationstring = c:ToStringBULLS(self.coalition, _SETTINGS)
                    end
                    local laserspot = {
                        laserspot = spot, lasedunit = unit, lasingunit = recce,
                        lasercode = code, location = locationstring,
                        timestamp = timer.getAbsTime(),
                        unitname = uname, reccename = reccename,
                        unittype = unit:GetTypeName(),
                        coordinate = c,
                    }
                    if self.smoketargets then
                        -- Translate with Overwrite=false returns a NEW coordinate so
                        -- we never mutate c (which is also laserspot.coordinate).
                        local coord = c
                        if self.smokeoffset then
                            coord = c:Translate(self.smokeoffset.Distance, self.smokeoffset.Angle, true, false)
                        end
                        local color = self:GetSmokeColor(reccename)
                        coord:Smoke(color)
                    end
                    self.lasingindex = self.lasingindex + 1
                    self.CurrentLasing[self.lasingindex] = laserspot
                    self:__Lasing(2, laserspot)
                    -- Claim immediately so a peer firing later this cycle skips it;
                    -- next cycle's rebuild re-publishes it from CurrentLasing anyway.
                    claims[uname] = true
                    mine[uname] = true
                end
            end
        end

        local nextloop = -self.MonitorFrequency or -30
        self:__Monitor(nextloop)
        return self
    end
end

-----------------------------------------------------------------
-- Part 3: monkeypatch AUTOLASE:SetPilotMenu to use a per-callsign MenuTitle
-- ("JTAC - <callsign>") and a per-recce "Change laser code" submenu.
-----------------------------------------------------------------
if not _G.__AutolaseMenuPatched and AUTOLASE then
    _G.__AutolaseMenuPatched = true
    function AUTOLASE:SetPilotMenu()
        if self.usepilotset then
            local pilottable=self.pilotset:GetSetObjects()or{}
            local grouptable={}
            for _,_unit in pairs(pilottable)do
                local Unit=_unit
                if Unit and Unit:IsAlive()then
                    local Group=Unit:GetGroup()
                    local GroupName=Group:GetName()or"none"
                    local unitname=Unit:GetName()
                    if not grouptable[GroupName]==true then
                        if self.playermenus[unitname]then self.playermenus[unitname]:Remove()end
                        local lasetopm=MENU_GROUP:New(Group,self.MenuTitle or "Autolase",nil)
                        self.playermenus[unitname]=lasetopm
                        local lasemenu=MENU_GROUP_COMMAND:New(Group,"Status",lasetopm,self.ShowStatus,self,Group,Unit)
                        if self.smokemenu then
                            local smoke=(self.smoketargets==true)and"off"or"on"
                            local smoketext=string.format("Switch smoke targets to %s",smoke)
                            local smokemenu=MENU_GROUP_COMMAND:New(Group,smoketext,lasetopm,self.SetSmokeTargets,self,(not self.smoketargets))
                        end
                        if self.threatmenu then
                            local threatmenutop=MENU_GROUP:New(Group,"Set min lasing threat",lasetopm)
                            for i=0,10,2 do
                                local text="Threatlevel "..tostring(i)
                                local threatmenu=MENU_GROUP_COMMAND:New(Group,text,threatmenutop,self.SetMinThreatLevel,self,i)
                            end
                        end
                        for _,_grp in pairs(self.RecceSet.Set)do
                            local grp=_grp
                            local unit=grp:GetUnit(1)
                            if unit and unit:IsAlive()then
                                local name=unit:GetName()
                                local mname=string.gsub(name,".%d+.%d+$","")
                                local code=self:GetLaserCode(name)
                                local unittop=MENU_GROUP:New(Group,"Change laser code for "..mname,lasetopm)
                                for _,_code in pairs(self.LaserCodes)do
                                    local text=tostring(_code)
                                    if _code==code then text=text.."(*)"end
                                    local changemenu=MENU_GROUP_COMMAND:New(Group,text,unittop,self.SetRecceLaserCode,self,name,_code,true)
                                end
                            end
                        end
                        grouptable[GroupName]=true
                    end
                end
            end
        else
            if not self.NoMenus then
                self.Menu=MENU_COALITION_COMMAND:New(self.coalition,self.MenuTitle or "Autolase",nil,self.ShowStatus,self)
            end
        end
        return self
    end
end

-- Utility: format integer values with thousands separators (e.g., 12,345)
local function FormatWithCommas(n)
    local s = tostring(math.floor(n or 0))
    local left, num, right = s:match('^([^%d]*%d)(%d*)(.-)$')
    return left .. (num:reverse():gsub('(%d%d%d)', '%1,'):reverse()) .. right
end

-- Per-file durations (seconds). Adjust as needed.
local SFX_DURATION_DEFAULT = 5.0
local SFX_DURATIONS = {
    ["ConvoyChaos.ogg"] = 6.0,
    ["LaserOff.ogg"]    = 1.0,
    ["LaserOn.ogg"]     = 1.0,
    ["TargetLost.ogg"]  = 1.0,
    ["TargetSmoke.ogg"] = 5.0, -- assumed from your note
}
local function GetSfxDuration(sfx)
    return SFX_DURATIONS[sfx] or SFX_DURATION_DEFAULT
end

-- Unified transmitter (uses the JTAC’s own unit(1))
local function TransmitRadio(forGroup, freqMHz, sfx, text, dbgTag)
    local unit = forGroup and forGroup:GetUnit(1)
    if not unit then
        if MooseAutolaseDebug then env.info(string.format("[%s] No unit to transmit on", dbgTag or "TX")) end
        return
    end
    local Radio = unit:GetRadio()
    if not Radio then
        if MooseAutolaseDebug then env.info(string.format("[%s] No Radio on %s", dbgTag or "TX", unit:GetName())) end
        return
    end
    Radio:SetFrequency(freqMHz)
    Radio:SetModulation(AM)
    Radio:SetPower(100)
    Radio:SetFileName(sfx)
    Radio:SetSubtitle(text, 60)
    Radio:Broadcast()
    if MooseAutolaseDebug then
        env.info(string.format("[%s] tx @ %.3f MHz AM via %s (sfx=%s)", dbgTag or "TX", freqMHz, unit:GetName(), sfx))
    end
end

-----------------------------------------------------------------
-- Shared helper: ScanDangerClose
-- Scans for friendly ground units within DangerCloseNM of tgtCoord.
-- jtacGroup is used to determine the coalition side for friendly filter.
-- Returns: dangerNote (string), dangerClose (bool).
-- Free variables: DangerCloseNM, AutolaseSmokeDurationSec, FormatWithCommas,
--                 SET_GROUP, SMOKECOLOR (all file-scope or DCS/Moose globals).
-----------------------------------------------------------------
local function ScanDangerClose(tgtCoord, jtacGroup)
    local DC_RADIUS_M       = DangerCloseNM * 1852
    local jtacSide          = jtacGroup:GetCoalition()
    local sideStr           = (jtacSide == coalition.side.RED and "red")
        or (jtacSide == coalition.side.BLUE and "blue")
        or "neutral"
    local nearestCoord, nearestDist

    local FriendlyGroundSet = SET_GROUP:New()
        :FilterCoalitions(sideStr)
        :FilterActive()
        :FilterStart()

    FriendlyGroundSet:ForEachGroup(function(g)
        if g:IsGround() then
            local c = g:GetCoordinate()
            local d = c and tgtCoord and c:Get2DDistance(tgtCoord) or nil
            if d and d <= DC_RADIUS_M and (not nearestDist or d < nearestDist) then
                nearestDist, nearestCoord = d, c
            end
        end
    end)

    if nearestCoord and nearestDist then
        nearestCoord:Smoke(SMOKECOLOR.Green, AutolaseSmokeDurationSec)

        local brtxt    = tgtCoord:ToStringBR(nearestCoord) or ""
        local bearing  = tonumber(brtxt:match("(%d+)")) or 0
        local dirs     = { "north", "northeast", "east", "southeast", "south", "southwest", "west",
            "northwest" }
        local idx      = (math.floor((bearing + 22.5) / 45) % 8) + 1
        local cardinal = dirs[idx]

        local feet     = math.floor(nearestDist * 3.28084 + 0.5)
        local feetStr  = (feet >= 1000) and FormatWithCommas(feet) or tostring(feet)

        local dangerNote = string.format(
            "\nFriendlies are DANGER CLOSE, %s feet %s of target, marking with green smoke.",
            feetStr, cardinal)
        return dangerNote, true
    end

    return "", false
end

-----------------------------------------------------------------
-- Shared helper: PickSFX
-- Selects the appropriate SFX filename for a lasing event.
-- Free variables: UseConvoyChaosSFX (file-scope global).
-----------------------------------------------------------------
local function PickSFX(dangerClose, smokeOn)
    if dangerClose and UseConvoyChaosSFX then return "ConvoyChaos.ogg" end
    return (smokeOn and "TargetSmoke.ogg") or "LaserOn.ogg"
end

-----------------------------------------------------------------
-- setupJtac: configure ONE AUTOLASE instance for a single drone.
-- def fields (flat per-drone shape from Python):
--   frontline, callsign, groupName, laserCode, uhf, vhf, orbitAlt, maxLasing(=1)
-- Shared globals consumed: JtacSmoke, JtacRadiusNM, MooseAutolaseFrontlines,
--   AutolaseSmokeDurationSec, MooseAutolaseDebug, ScanDangerClose, PickSFX,
--   GetSfxDuration, TransmitRadio, FormatWithCommas, AM (all file-scope).
-----------------------------------------------------------------
local function setupJtac(def)
    local g = GROUP:FindByName(def.groupName)
    if not g then
        if MooseAutolaseDebug then
            env.info("------JTAC drone " .. tostring(def.groupName) .. " NOT Located (frontline="
                .. tostring(def.frontline) .. ")-------")
        end
        return
    end
    if MooseAutolaseDebug then
        env.info("------JTAC drone " .. tostring(def.groupName) .. " Located (frontline="
            .. tostring(def.frontline) .. ")-------")
    end

    -- Step 1: orbit for this one drone.
    local coord     = g:GetCoordinate()
    if not coord then
        -- Group exists but has no live unit yet (e.g. late activation); without a
        -- coord the orbit AUFTRAG would error and abort setup for this drone.
        if MooseAutolaseDebug then
            env.info("------JTAC drone " .. tostring(def.groupName)
                .. " has no coordinate (no live unit), skipping-------")
        end
        return
    end
    local fg        = FLIGHTGROUP:New(g)
    local racetrack = AUFTRAG:NewORBIT_CIRCLE(coord, def.orbitAlt, 120)
    fg:SetDefaultInvisible(true)
    fg:SetDefaultImmortal(true)
    fg:AddMission(racetrack)

    if MooseAutolaseDebug then
        MESSAGE:New("SETTING UP JTAC " .. tostring(def.callsign) .. " FOR AUTOLASE (MOOSE)",
            5, "RETRIBUTION", false):ToAll():ToLog()
    end

    local jtacName = def.callsign

    -- Step 2: recce SET_GROUP over this single drone group.
    local set = SET_GROUP:New():FilterPrefixes({ def.groupName }):FilterCoalitions("blue"):FilterOnce()
    set:AddGroup(g)

    -- Pilot menu zone anchored on this drone.
    local droneZone = ZONE_GROUP:New(def.callsign .. " Zone", g, 1852 * JtacRadiusNM)
    local pilotSet  = SET_CLIENT:New():FilterCoalitions("blue"):FilterZones({ droneZone }):FilterActive():FilterStart()

    -- Step 3: one AUTOLASE instance for this drone.
    local inst = AUTOLASE:New(set, coalition.side.BLUE, def.callsign .. " Autolase", pilotSet)
        :SetMaxLasingTargets(1)
        :SetLasingParameters(15000, AutolaseSmokeDurationSec)
        :SetNotifyPilots(false)
        :DisableThreatLevelMenu()
        :SetSmokeTargets(JtacSmoke, SMOKECOLOR.Red)
        :EnableSmokeMenu({ Angle = 30, Distance = 40 })

    -- Dual assignment is intentional: SetLaserCodes constrains the instance's
    -- code pool to this drone's code (kills the shared-default "same code" bug);
    -- SetRecceLaserCode (Step 4) binds that code to this recce unit.
    inst:SetLaserCodes({ def.laserCode })

    inst._currentOrbitAuftrag = racetrack
    inst._homeCoord           = coord
    inst._altHomeFt           = def.orbitAlt
    inst._altTgtFt            = def.orbitAlt + 1000
    inst._orbitSpeedKts       = 120
    inst._lastLaserInfo       = {}
    inst._frontlineSegment    = MooseAutolaseFrontlines[def.frontline]
    -- B+ deconfliction: region keys the shared MooseAutolaseClaims set;
    -- _claimedUnits is the set of unit names this instance currently lases
    -- (rebuilt from CurrentLasing each monitor cycle). One-time region init here
    -- so the monitor loop never has to nil-check the per-region table.
    inst._frontlineRegion     = def.frontline
    inst._claimedUnits        = {}
    MooseAutolaseClaims[def.frontline] = MooseAutolaseClaims[def.frontline] or {}
    inst.MenuTitle            = "JTAC - " .. def.callsign

    -- Mission-queue debug helper (closes over fg / jtacName).
    local function _DumpMissionQueue(tag)
        local lines = {}
        local queue = fg and fg.missionqueue or nil

        local function safe(call, default)
            local ok, val = pcall(call); return ok and val or default
        end
        local function _describeAuftrag(idx, auf)
            local name   = safe(function() return auf:GetName() end,
                safe(function() return auf.Name end, safe(function() return auf.name end, "AUFTRAG")))
            local prio   = safe(function() return auf:GetPriority() end,
                safe(function() return auf.Priority end, safe(function() return auf.prio end, "?")))
            local urgent = safe(function() return tostring(auf:GetUrgent()) end,
                safe(function() return tostring(auf.Urgent) end, safe(function() return tostring(auf.urgent) end, "?")))
            return string.format("%02d) %s  [prio=%s, urgent=%s]", idx, tostring(name), tostring(prio), tostring(urgent))
        end

        if type(queue) == "table" then
            local idx = 0
            for i, auf in ipairs(queue) do
                idx = i; table.insert(lines, _describeAuftrag(i, auf))
            end
            for k, auf in pairs(queue) do
                if type(k) ~= "number" or k < 1 or k > idx then
                    table.insert(lines, _describeAuftrag(#lines + 1, auf))
                end
            end
        else
            table.insert(lines, "(missionqueue not available on this FLIGHTGROUP)")
        end

        local text = string.format("JTAC %s MissionQueue — %s\n%s", jtacName, tag or "update",
            table.concat(lines, "\n"))
        if MooseAutolaseDebug then MESSAGE:New(text, 15, def.callsign .. " Queue"):ToAll() end
    end

    -- Retask this drone's orbit toward the lased target.
    function inst:_ReplaceOrbitAt(coord2, altFt, reasonTag)
        if not coord2 then return end
        if self._currentOrbitAuftrag then
            pcall(function() self._currentOrbitAuftrag:Cancel() end); self._currentOrbitAuftrag = nil
        end
        local newOrbit = AUFTRAG:NewORBIT_CIRCLE(coord2, altFt or self._altTgtFt, self._orbitSpeedKts)
        newOrbit:SetPriority(1, true, 1)
        fg:AddMission(newOrbit)
        self._currentOrbitAuftrag = newOrbit
        if MooseAutolaseDebug then
            env.info(string.format("JTAC %s orbit RECENTERED at %s (alt %d ft) [%s]",
                jtacName, coord2:ToStringMGRS(), altFt or self._altTgtFt, tostring(reasonTag or "update")))
        end
        _DumpMissionQueue(reasonTag or "orbit retask")
    end

    function inst:OnAfterLasing(From, Event, To, LaserSpot)
        if MooseAutolaseDebug then env.info(def.callsign .. " ------ Laser On!") end

        self._lastLaserInfo = {
            code      = LaserSpot and LaserSpot.lasercode or 0,
            mgrs      = (LaserSpot and LaserSpot.coordinate) and LaserSpot.coordinate:ToStringMGRS() or "N/A",
            unittype  = LaserSpot and LaserSpot.unittype or "Unknown",
            reccename = LaserSpot and LaserSpot.reccename or "Unknown"
        }

        if LaserSpot and LaserSpot.coordinate then
            self:_ReplaceOrbitAt(LaserSpot.coordinate, self._altTgtFt, "new lase")
        else
            self:_ReplaceOrbitAt(self._homeCoord, self._altHomeFt, "no coord")
        end

        pilotSet:ForEachClient(function(client)
            if client and client:IsAlive() then
                local laserspot = LaserSpot
                if laserspot and laserspot.coordinate then
                    local clientCoord = client:GetCoordinate()
                    local BRInfo      = laserspot.coordinate:ToStringBR(clientCoord)
                    local BRInfoClean = (BRInfo or "N/A"):gsub("^%s*:%s*", "")

                    local dangerNote, dangerClose = ScanDangerClose(laserspot.coordinate, g)

                    local text = string.format(
                        "%s is lasing %s code %d\nat %s\n%s%s",
                        laserspot.reccename or "Unknown",
                        laserspot.unittype or "Unknown",
                        laserspot.lasercode or 0,
                        laserspot.coordinate:ToStringMGRS(),
                        BRInfoClean,
                        dangerNote
                    )

                    local sfx      = PickSFX(dangerClose, inst.smoketargets)
                    local firstDur = GetSfxDuration(sfx)

                    TransmitRadio(g, def.uhf, sfx, text, def.callsign .. " UHF")

                    TIMER:New(function()
                        TransmitRadio(g, def.vhf, sfx, text, def.callsign .. " VHF")
                    end):Start(firstDur + 0.15)

                    MESSAGE:New(text, 60, def.callsign):ToLog()
                end
            end
        end)
    end

    function inst:OnAfterTargetDestroyed(From, Event, To, UnitName, RecceName)
        env.info("----JTAC " .. def.callsign .. "'s target destroyed, returning to home orbit-----")
        -- Free the claim on the unit that was destroyed (by its name, not our
        -- current claim) so a peer can take its slot before our next rebuild.
        local claims = MooseAutolaseClaims[self._frontlineRegion]
        if claims and UnitName then claims[UnitName] = nil end
        if self._claimedUnits and UnitName then self._claimedUnits[UnitName] = nil end
        self:_ReplaceOrbitAt(self._homeCoord, self._altHomeFt, "target destroyed")
    end

    function inst:OnAfterTargetLost(From, Event, To, UnitName, RecceName)
        if MooseAutolaseDebug then env.info(def.callsign .. " ------ Target Lost!") end

        pilotSet:ForEachClient(function(client)
            if client and client:IsAlive() then
                local info = self._lastLaserInfo or {}
                local text = string.format("%s LOST TARGET\n%s (code %d) at %s", info.reccename or RecceName,
                    info.unittype or "Unknown", info.code or 0, info.mgrs or "Unknown")

                local sfx      = (inst.smoketargets and "TargetLost.ogg") or "LaserOff.ogg"
                local firstDur = GetSfxDuration(sfx)

                TransmitRadio(g, def.uhf, sfx, text, def.callsign .. " UHF LOST")

                TIMER:New(function()
                    TransmitRadio(g, def.vhf, sfx, text, def.callsign .. " VHF LOST")
                end):Start(firstDur + 0.15)

                MESSAGE:New(text, 60, def.callsign):ToLog()
            end
        end)

        local claims = MooseAutolaseClaims[self._frontlineRegion]
        if claims and UnitName then claims[UnitName] = nil end
        if self._claimedUnits and UnitName then self._claimedUnits[UnitName] = nil end
        self:_ReplaceOrbitAt(self._homeCoord, self._altHomeFt, "target lost")
    end

    -- Step 4: assign this drone its distinct laser code + smoke color.
    local u = g:GetUnit(1)
    if u then
        inst:SetRecceLaserCode(u:GetName(), def.laserCode)
        inst:SetRecceSmokeColor(u:GetName(), SMOKECOLOR.Red)
        if MooseAutolaseDebug then
            env.info(string.format("%s assigned laser code %d (frontline=%s)",
                u:GetName(), def.laserCode, tostring(def.frontline)))
        end
    end

    _DumpMissionQueue("initial")
end

for _, def in ipairs(MooseAutolaseJTACs) do
    setupJtac(def)
end

env.info("-----DCSRetribution|MOOSE Autolase plugin - configuration end ------")
