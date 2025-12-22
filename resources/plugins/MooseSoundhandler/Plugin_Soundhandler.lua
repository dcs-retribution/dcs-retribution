env.info("-----DCSRetribution|MOOSE Soundhandler plugin - configuration start -----")
-- assert(loadfile("C:\\Users\\Taco\\Documents\\Github\\DCS\\Custom_Retribution\\Plugins\\MooseSoundhandler\\Plugin_Soundhandler.lua"))()
-----------------------------------------------------------------------------------------------------------------------------------
-- CONFIG
-----------------------------------------------------------------------------------------------------------------------------------
-- Defaults (overridden by dcsRetribution.plugins.MooseSoundhandler.* if present)
SoundToGroupOnly      = true
ShipSamSounds         = true
PlayOwnShootingGuns   = true
PlayOpForShootingGuns = true
SoundDebug            = true
SoundHandler          = true -- Not a UI setting, but an On/Off switch mid-mission.

if dcsRetribution and dcsRetribution.plugins and dcsRetribution.plugins.MooseSoundhandler then
    -- Use externally provided settings, preserving original field names
    if dcsRetribution.plugins.MooseSoundhandler.SoundToGroupOnly ~= nil then
        SoundToGroupOnly = dcsRetribution.plugins.MooseSoundhandler.SoundToGroupOnly
    end
    if dcsRetribution.plugins.MooseSoundhandler.ShipSamSounds ~= nil then
        ShipSamSounds = dcsRetribution.plugins.MooseSoundhandler.ShipSamSounds
    end
    if dcsRetribution.plugins.MooseSoundhandler.PlayOwnShootingGuns ~= nil then
        PlayOwnShootingGuns = dcsRetribution.plugins.MooseSoundhandler.PlayOwnShootingGuns
    end
    if dcsRetribution.plugins.MooseSoundhandler.PlayOpForShootingGuns ~= nil then
        PlayOpForShootingGuns = dcsRetribution.plugins.MooseSoundhandler.PlayOpForShootingGuns
    end
    if dcsRetribution.plugins.MooseSoundhandler.SoundDebug ~= nil then
        SoundDebug = dcsRetribution.plugins.MooseSoundhandler.SoundDebug
    end
else
    env.info("-----dcsRetribution.plugins.MooseSoundhandler NOT FOUND")
end

env.info("--------- SoundToGroupOnly=" .. tostring(SoundToGroupOnly) ..
    " | ShipSamSounds=" .. tostring(ShipSamSounds) ..
    " | PlayOwnShootingGuns=" .. tostring(PlayOwnShootingGuns) ..
    " | PlayOpForShootingGuns=" .. tostring(PlayOpForShootingGuns) ..
    " | Debug=" .. tostring(SoundDebug))

if SoundDebug then
    trigger.action.outText("---SOUND DEBUG IS ON!---", 10)
    trigger.action.outText("Soundhandler " .. (SoundHandler and "ON" or "OFF"), 10)
    trigger.action.outText("Sounds will play to " .. (SoundToGroupOnly and "GROUP only" or "ALL clients in coalition"),
        10)
    trigger.action.outText("Ships firing SAMs will " .. (ShipSamSounds and "" or "NOT ") .. "play sounds", 10)
    trigger.action.outText("Own Airplane Gun Bursts will " .. (PlayOwnShootingGuns and "" or "NOT ") .. "play sounds", 10)
    trigger.action.outText(
        "OpFor Airplane Gun Bursts will " .. (PlayOpForShootingGuns and "" or "NOT ") .. "play sounds", 10)
end

-----------------------------------------------------------------------------------------------------------------------------------
-- SOUND DATA
-----------------------------------------------------------------------------------------------------------------------------------
SoundFilePath = SoundFilePath or ""
if SoundFilePath ~= "" then
    local last = SoundFilePath:sub(-1)
    if last ~= "/" and last ~= "\\" then
        SoundFilePath = SoundFilePath .. "/"
    end
end

Sounds                         = {}
Sounds.Air_Unit_Sound_Table    = { "AAGoodKill", "AAKill4", "AAKillGoodhiton1", "AAKillSplash", "AAKillSplashone",
    "AASplashOne", "AASplashOne_2" }
Sounds.Incoming_Missile_Table  = { "Misil1", "Misil2", "Misil3", "Misil4", "Misil5", "Misil6" }
Sounds.Ground_Unit_Sound_Table = { "AGKillBOOM1", "AGKillCOMEONBABY", "AGKillGoodBOOM", "AGKillSeeTheSmoke",
    "AGKill_TARGET_DESTROYED", "AGKillBeautiful_beautiful", "AGKillMotherFucker" }
Sounds.SamSoundTable           = { "SAM1", "SAM2", "SAM3", "SAM4", "SAM5", "SAM6", "SAM7", "Defending" }
Sounds.Ballistic               = { "SCUD_Long", "Fireball" }
Sounds.PigsAway_Sound_Table    = { "PigsAway", "PigsAway2" }
Sounds.Paveway_Sound_Table     = { "Paveway" }
Sounds.Bruiser_Sound_Table     = { "Bruiser", "Bruiser2", "Bruiser3" }
Sounds.Fox2_Sound_Table        = { "Fox2A", "Fox2B", "Fox2C", "Fox2D", "Fox2E" }
Sounds.Fox3_Sound_Table        = { "Fox3A", "Fox3B", "Fox3C", "Fox3D", "Fox3E", "Fox3F" }
Sounds.Fox1_Sound_Table        = { "Fox1A", "Fox1B" }
Sounds.Magnum_Sound_Table      = { "Magnum", "Magnum2" }
Sounds.Rifle_Sound_Table       = { "RifleA", "RifleB", "RifleC", "RifleD", "RifleE" }
Sounds.Pickle_Sound_Table      = { "Pickle1", "Pickle2", "Pickle3", "Pickle4", "Pickle5", "Pickle6", "Pickle7" }
Sounds.FriendlyLosses          = { "OhJesus", "HitEjecting1", "HitEjecting2", "HitEjecting3", "StartFindingMeBoys" }
Sounds.Guns_OwnFire            = { "BlueGuns1", "BlueGuns2", "BlueGuns3" }
Sounds.Guns_Incoming           = { "Guns_Break_Right", "Guns_Break_Left" }
Sounds.Decoy_Table             = { "A2G_Duck1" }
Sounds.CruiseMissile_Table     = { "A2G_Greyhound1" }
Sounds.Vampires_Table          = { "A2G_Vampires1" } -- anti-ship call
Sounds.Tomahawk_Table          = { "S2G_Tomahawk1" }
Sounds.Friendly_Fire_Table     = { "FriendlyFire1", "FriendlyFire2" }
Sounds.Friendly_SAM_Table      = { "BirdsAway" }

if SoundDebug then
    for _, tbl in pairs(Sounds) do
        local txt = UTILS.OneLineSerialize(tbl)
        env.info("Sounds Loaded: " .. txt)
        trigger.action.outText("Sounds Loaded: " .. txt, 10)
    end
end

-----------------------------------------------------------------------------------------------------------------------------------
-- HELPERS
-----------------------------------------------------------------------------------------------------------------------------------
local BLUE, RED = coalition.side.BLUE, coalition.side.RED

local function Opposing(side)
    if side == BLUE then return RED end
    if side == RED then return BLUE end
    return side
end

local function ChooseRandom(t) return t[math.random(1, #t)] end

-- === DROP-IN: NewSound (no filesystem check; works with mission-embedded sounds) ===
local function NewSound(nameNoExt)
    local full = SoundFilePath .. nameNoExt .. ".ogg"
    if SoundDebug then env.info("[SND] NewSound: " .. tostring(full)) end
    return USERSOUND:New(full)
end

-- === DROP-IN: PlayToGroupOrCoalition (robust group canonization; no mirror re-load) ===
-- Signature: PlayToGroupOrCoalition(soundObj, groupObj, coalitionSide)
local function PlayToGroupOrCoalition(soundObj, groupObj, coalitionSide)
    if not soundObj then
        if SoundDebug then env.info("[SND] Play aborted: soundObj is nil") end
        return
    end

    -- Re-resolve the group by name to avoid stale wrapper instances.
    local canonGroup = nil
    if groupObj and groupObj.GetName then
        local gname = groupObj:GetName()
        if gname then canonGroup = GROUP:FindByName(gname) end
    end

    -- Preferred path: play to group when toggled and group exists
    if SoundToGroupOnly and canonGroup then
        if SoundDebug then
            local dcs = canonGroup.GetDCSObject and canonGroup:GetDCSObject() or nil
            local gid = dcs and dcs:getID() or "?"
            env.info(string.format("[SND] ToGroup '%s' (id=%s)", tostring(canonGroup:GetName()), tostring(gid)))
        end
        soundObj:ToGroup(canonGroup)
        return
    end

    -- Coalition fallback
    if coalitionSide then
        if SoundDebug then
            env.info(string.format("[SND] ToCoalition side=%s (group-only=%s, group=%s)",
                tostring(coalitionSide), tostring(SoundToGroupOnly),
                tostring(canonGroup and canonGroup:GetName() or "nil")))
        end
        soundObj:ToCoalition(coalitionSide)
        return
    end

    if SoundDebug then env.info("[SND] Play aborted: no valid group and no coalitionSide") end
end

-----------------------------------------------------------------------------------------------------------------------------------
-- EVENT HANDLERS
-----------------------------------------------------------------------------------------------------------------------------------
EventHandler = EVENTHANDLER:New()
EventHandler:HandleEvent(EVENTS.Shot)
EventHandler:HandleEvent(EVENTS.Kill)
EventHandler:HandleEvent(EVENTS.Dead)

-----------------------------------------------------------------------------------------------------------------------------------
-- KILL EVENTS (FULLY MIRRORED, nil-safe)
-----------------------------------------------------------------------------------------------------------------------------------
function EventHandler:OnEventKill(EventData)
    if not SoundHandler then return end
    if SoundDebug then
        BASE:I("---------KILL DETECTED----------"); BASE:I(EventData)
    end
    if SoundDebug then LogKillEvent(EventData) end

    local iniSide      = EventData.IniCoalition
    local tgtSide      = EventData.TgtCoalition
    local iniGroup     = EventData.IniGroup
    local iniGroupName = EventData.IniGroupName

    -- 1) A2A kill by an airplane → killer hears A2A “good kill”
    local gA2A         = iniGroupName and GROUP:FindByName(iniGroupName) or nil
    if (EventData.TgtCategory == 0 or EventData.TgtCategory == 1)
        and EventData.TgtObjectCategory == 1
        and gA2A and gA2A.IsAirPlane and gA2A:IsAirPlane() then
        local s = ChooseRandom(Sounds.Air_Unit_Sound_Table)
        PlayToGroupOrCoalition(NewSound(s), iniGroup, iniSide)
    end

    -- 2) A2G kill (ground unit killed by airplane) → killer hears ground kill
    local gA2G = iniGroupName and GROUP:FindByName(iniGroupName) or nil
    if gA2G and gA2G.IsAirPlane and gA2G:IsAirPlane()
        and EventData.TgtCategory == 2 and EventData.TgtObjectCategory == 1
        and iniSide ~= tgtSide then
        local s = ChooseRandom(Sounds.Ground_Unit_Sound_Table)
        PlayToGroupOrCoalition(NewSound(s), iniGroup, iniSide)
    end

    -- 3) Ship killed by airplane → killer hears ground/ship kill
    local gShip = iniGroupName and GROUP:FindByName(iniGroupName) or nil
    if gShip and gShip.IsAirPlane and gShip:IsAirPlane()
        and EventData.TgtCategory == 3 and EventData.TgtObjectCategory == 1 then
        local s = ChooseRandom(Sounds.Ground_Unit_Sound_Table)
        PlayToGroupOrCoalition(NewSound(s), iniGroup, iniSide)
    end

    -- 4) Friendly aircraft loss: only if a CLIENT aircraft is killed
    if EventData.TgtCategory == 0 and EventData.TgtUnitName then
        local tgtClient = CLIENT:FindByName(EventData.TgtUnitName)
        if tgtClient then
            local s = ChooseRandom(Sounds.FriendlyLosses)
            NewSound(s):ToCoalition(tgtSide)
        end
    end

    -- 5) Friendly-fire (air vs air): notify the offending side only if target is a CLIENT aircraft
    if iniSide == tgtSide and EventData.TgtCategory == 0 and EventData.TgtUnitName then
        local tgtClient = CLIENT:FindByName(EventData.TgtUnitName)
        if tgtClient then
            local s = ChooseRandom(Sounds.Friendly_Fire_Table)
            PlayToGroupOrCoalition(NewSound(s), iniGroup, iniSide)
        end
    end
end

-----------------------------------------------------------------------------------------------------------------------------------
-- DEAD EVENTS (MIRRORED)
-----------------------------------------------------------------------------------------------------------------------------------
function EventHandler:OnEventDead(EventData)
    if not SoundHandler then return end
    if SoundDebug then
        BASE:I("---------DEAD DETECTED----------"); BASE:I(EventData)
    end
    if SoundDebug then LogDeadUnit(EventData) end

    -- STATIC DEAD: play to the OPPOSING coalition (keeps the “good hit” vibe)
    if EventData.IniObjectCategory == 3 then
        local s = ChooseRandom(Sounds.Ground_Unit_Sound_Table)
        NewSound(s):ToCoalition(Opposing(EventData.IniCoalition))
    end
end

-----------------------------------------------------------------------------------------------------------------------------------
-- SHOT EVENTS (mirrored + clarified intent)
--  - Shooter feedback (own weapon) → Fox/Pickle/Rifle/etc to SHOOTER side (group/coalition)
--  - Incoming cues:
--      * Missile fired at a target group → Incoming_Missile_Table to TARGET group
--      * SAM launch:
--          - Friendly SAM → Friendly_SAM_Table to shooter side
--          - Hostile SAM at target → SamSoundTable to TARGET group
--  - Special cases: Tomahawk to shooter side, SCUD to opposing coalition
-----------------------------------------------------------------------------------------------------------------------------------
function EventHandler:OnEventShot(EventData)
    if SoundDebug then
        BASE:I("---------SHOT DETECTED----------"); BASE:I(EventData)
    end
    if not SoundHandler then return end
    if SoundDebug then LogFiringUnit(EventData) end
    if not EventData.Weapon then return end

    local WeaponDesc = EventData.Weapon:getDesc()
    if not WeaponDesc then return end

    local iniSide      = EventData.IniCoalition
    local tgtGroup     = EventData.TgtGroup
    local iniGroup     = EventData.IniGroup
    local iniGroupName = EventData.IniGroupName or ""
    local _weapon      = EventData.Weapon:getTypeName()
    local category     = WeaponDesc.category -- 0 shell, 1 missile, 2 rocket, 3 bomb
    local guidance     = WeaponDesc.guidance -- 1 unguided bomb, 2 IR, 3 ARH, 4 SARH, 5 anti-radar, 7 TV/EO
    local missileCat   = WeaponDesc.missileCategory

    local brevity      = "none"
    local function pick(tbl) brevity = ChooseRandom(tbl) end

    local shooterGroup = iniGroupName ~= "" and GROUP:FindByName(iniGroupName) or nil

    -- Shooter feedback (own-fire), nil-safe airplane check
    if shooterGroup and shooterGroup.IsAirPlane and shooterGroup:IsAirPlane() then
        if _weapon == "AGM_154" or _weapon == "AGM_154A" then
            pick(Sounds.PigsAway_Sound_Table)
        elseif string.find(_weapon, "ADM", 1, true) then
            pick(Sounds.Decoy_Table)
        elseif category == 3 and guidance == 7 then
            pick(Sounds.Paveway_Sound_Table)
        elseif _weapon == "AGM_84D" then
            pick(Sounds.Bruiser_Sound_Table)
        elseif _weapon == "AGM_84H" or string.find(_weapon, "84E", 1, true) then
            pick(Sounds.CruiseMissile_Table)
        elseif category == 1 and guidance == 3 then
            pick(Sounds.Fox3_Sound_Table)
        elseif category == 1 and guidance == 2 then
            pick(Sounds.Fox2_Sound_Table)
        elseif category == 1 and guidance == 4 then
            pick(Sounds.Fox1_Sound_Table)
        elseif category == 1 and guidance == 5 and missileCat == 6 then
            pick(Sounds.Magnum_Sound_Table)
        elseif category == 1 and guidance == 7 or string.find(_weapon, "65", 1, true) then
            pick(Sounds.Rifle_Sound_Table)
        elseif category == 0 then
            pick(Sounds.Rifle_Sound_Table)
        elseif category == 1 then
            pick(Sounds.Rifle_Sound_Table)
        elseif category == 2 then
            pick(Sounds.Rifle_Sound_Table)
        elseif category == 3 then
            if guidance == 1 or _weapon == "GBU_32_V_2B" or string.find(_weapon, "MK", 1, true) or string.find(_weapon, "ROCKEYE", 1, true) then
                pick(Sounds.Pickle_Sound_Table)
            else
                pick(Sounds.Pickle_Sound_Table)
            end
        end
    end

    -- Friendly SAM cue
    if shooterGroup and shooterGroup.IsSAM and shooterGroup:IsSAM() then
        pick(Sounds.Friendly_SAM_Table)
    end

    -- Ship-launched Tomahawk cue
    if shooterGroup and shooterGroup.IsShip and shooterGroup:IsShip() then
        if string.find(_weapon, "BGM_109B", 1, true) then
            pick(Sounds.Tomahawk_Table)
        end
    end

    -- Incoming missile cue to target group
    if tgtGroup and category == 1 then
        local inc = ChooseRandom(Sounds.Incoming_Missile_Table)
        local incsnd = NewSound(inc)
        local function DelayedIncoming() if tgtGroup then incsnd:ToGroup(tgtGroup) end end
        TIMER:New(DelayedIncoming):Start(math.random(3, 7)) --TODO make UI Variables
    end

    -- Hostile SAM at target → SAM call to TARGET group
    if tgtGroup and shooterGroup and ((shooterGroup.IsSAM and shooterGroup:IsSAM()) or (ShipSamSounds and shooterGroup.IsShip and shooterGroup:IsShip())) and category == 1 then
        if not string.find(_weapon, "SA48N6", 1, true) and not string.find(_weapon, "SCUD_RAKETA", 1, true) then
            local sams = ChooseRandom(Sounds.SamSoundTable)
            local samsnd = NewSound(sams)
            local function DelayedSAMS() if tgtGroup then samsnd:ToGroup(tgtGroup) end end
            TIMER:New(DelayedSAMS):Start(math.random(3, 7))
        end
    end

    -- Ballistic missile (SCUD) → opposing coalition
    if string.find(_weapon, "SCUD_RAKETA", 1, true) then
        local b = ChooseRandom(Sounds.Ballistic)
        NewSound(b):ToCoalition(Opposing(iniSide))
    end

    -- Deliver shooter feedback if selected
    if brevity ~= "none" then
        PlayToGroupOrCoalition(NewSound(brevity), iniGroup, iniSide)
    end
end

if SoundDebug then BASE:I("-----MISSILE/BOMB SOUNDS SET------") end

-----------------------------------------------------------------------------------------------------------------------------------
-- SHOOTING (RAPID FIRE) – mirrored & renamed tables
--  - If a CLIENT fires guns → Guns_OwnFire to their group/coalition
--  - If guns are being fired at a target group (client) → Guns_Incoming to target group
-----------------------------------------------------------------------------------------------------------------------------------
local SHOOT_SFX_COOLDOWN = 30 -- seconds
local _lastShootSfxAt    = -1

local function ShootingSfxGate(tag)
    local now = timer.getTime() -- mission time
    if _lastShootSfxAt and _lastShootSfxAt > 0 then
        local dt = now - _lastShootSfxAt
        if dt < SHOOT_SFX_COOLDOWN then
            if SoundDebug then
                env.info(string.format("[SFX-GATE] BLOCK %s: %.1fs remaining", tag,
                    SHOOT_SFX_COOLDOWN - dt))
            end
            return false
        end
    end
    _lastShootSfxAt = now
    if SoundDebug then env.info(string.format("[SFX-GATE] ALLOW %s at t=%.1f", tag, now)) end
    return true
end

ShootingEventHandler = EVENTHANDLER:New()
ShootingEventHandler:HandleEvent(EVENTS.ShootingStart)

if SoundDebug then env.info("----- GUN SHOOTING HANDLER INIT (listening for EVENTS.ShootingStart) -----") end

local function DBG(...)
    if SoundDebug then
        local msg = table.concat({ ... }, " "); BASE:I(msg); env.info(msg)
    end
end
local function BOOLSTR(b) return b and "true" or "false" end

local function FindGroupWithLog(name, tag)
    if not name then
        DBG(tag, " : no name provided"); return nil
    end
    local g = GROUP:FindByName(name)
    DBG(tag, " : GROUP:FindByName(", name, ") -> ", tostring(g))
    if g then
        local okExist = g.IsExist and g:IsExist()
        DBG(tag, " :   IsExist=", tostring(okExist), " IsAirPlane=", tostring(g.IsAirPlane and g:IsAirPlane() or "n/a"))
    end
    return g
end

local function FindUnitWithLog(dcsUnit, tag)
    if not dcsUnit then
        DBG(tag, " : no DCS unit handle"); return nil
    end
    local u = UNIT:Find(dcsUnit)
    DBG(tag, " : UNIT:Find(DCSUnit) -> ", tostring(u))
    if u then
        DBG(tag, " :   IsExist=", BOOLSTR(u.IsExist and u:IsExist()), " IsClient=",
            BOOLSTR(u.IsClient and u:IsClient()))
    end
    return u
end

function ShootingEventHandler:OnEventShootingStart(EventData)
    env.info(string.format("[GUN] ShootingStart fired t=%.2f ini=%s tgt=%s",
        tonumber(EventData.time or -1),
        tostring(EventData.IniUnitName or EventData.IniDCSUnitName or "?"),
        tostring(EventData.TgtUnitName or EventData.TgtDCSUnitName or "?")
    ))

    if SoundDebug then
        DBG("-----RAPID GUNS SHOOTING START-----")
        DBG("EventData fields present:",
            " IniGroupName=", tostring(EventData.IniGroupName),
            " IniUnitName=", tostring(EventData.IniUnitName),
            " IniCoalition=", tostring(EventData.IniCoalition),
            " TgtGroup=", tostring(EventData.TgtGroup),
            " TgtGroupName=", tostring(EventData.TgtGroupName),
            " TgtDCSUnit=", tostring(EventData.TgtDCSUnit),
            " TgtCoalition=", tostring(EventData.TgtCoalition))
        DBG("OneLineSerialize: ", UTILS.OneLineSerialize(EventData))
    end

    -- Shooter resolution + validation
    local ShooterGroup = FindGroupWithLog(EventData.IniGroupName, "SHOOTER group")
    local ShooterUnit  = nil
    if EventData.IniUnitName then
        ShooterUnit = UNIT:FindByName(EventData.IniUnitName)
        DBG("SHOOTER unit : UNIT:FindByName(", EventData.IniUnitName, ") -> ", tostring(ShooterUnit))
        if ShooterUnit then
            DBG("SHOOTER unit : IsExist=", BOOLSTR(ShooterUnit.IsExist and ShooterUnit:IsExist()),
                " IsClient=", BOOLSTR(ShooterUnit.IsClient and ShooterUnit:IsClient()))
        end
    else
        DBG("SHOOTER unit : IniUnitName missing")
    end

    if not ShooterGroup or not ShooterUnit then
        DBG("ABORT: missing ShooterGroup (", tostring(ShooterGroup), ") or ShooterUnit (", tostring(ShooterUnit), ")")
        return
    end

    local isPlane = ShooterGroup.IsAirPlane and ShooterGroup:IsAirPlane() or false
    DBG("SHOOTER group type: IsAirPlane=", BOOLSTR(isPlane))
    if not isPlane then
        DBG("ABORT: ShooterGroup is not airplane")
        return
    end

    -- Own-fire branch (client shooter)
    local shooterIsClient = ShooterUnit.IsClient and ShooterUnit:IsClient() or false
    DBG("SHOOTER IsClient=", BOOLSTR(shooterIsClient), " | PlayOwnShootingGuns=", BOOLSTR(PlayOwnShootingGuns))
    if shooterIsClient and PlayOwnShootingGuns then
        if not ShootingSfxGate("OWNFIRE") then return end
        local s = ChooseRandom(Sounds.Guns_OwnFire)
        DBG("OWNFIRE: choosing sound=", tostring(s))
        local snd = NewSound(s)
        if snd then
            DBG("OWNFIRE: playing to shooter group/coalition (SoundToGroupOnly=", BOOLSTR(SoundToGroupOnly), ")")
            PlayToGroupOrCoalition(snd, EventData.IniGroup, EventData.IniCoalition)
        else
            DBG("OWNFIRE: NewSound failed (nil)")
        end
        return
    elseif shooterIsClient and not PlayOwnShootingGuns then
        DBG("OWNFIRE: suppressed by PlayOwnShootingGuns=false")
    end

    -- Incoming branch – resolve target group in 3 passes
    local tgtGroup = nil
    if EventData.TgtGroup then
        tgtGroup = EventData.TgtGroup
        DBG("TARGET pass1: EventData.TgtGroup provided -> ", tostring(tgtGroup))
    end
    if not tgtGroup and EventData.TgtGroupName then
        DBG("TARGET pass2: Try TgtGroupName=", tostring(EventData.TgtGroupName))
        tgtGroup = FindGroupWithLog(EventData.TgtGroupName, "TARGET pass2")
    end
    if not tgtGroup and EventData.TgtDCSUnit then
        DBG("TARGET pass3: Try TgtDCSUnit wrapper")
        local u = FindUnitWithLog(EventData.TgtDCSUnit, "TARGET pass3")
        if u and u.IsExist and u:IsExist() then
            tgtGroup = u:GetGroup()
            DBG("TARGET pass3: u:GetGroup() -> ", tostring(tgtGroup))
            if tgtGroup and tgtGroup.IsExist then DBG("TARGET pass3: tgtGroup:IsExist()=", BOOLSTR(tgtGroup:IsExist())) end
        end
    end

    if not tgtGroup then
        DBG("INCOMING: abort — could not resolve a target group from any field.")
        return
    end

    -- Strict: confirm target is a client
    local pc = tgtGroup.GetPlayerCount and tgtGroup:GetPlayerCount() or nil
    DBG("CLIENT-CHECK: GetPlayerCount=", tostring(pc))
    local targetIsClient = false
    if pc ~= nil then
        targetIsClient = (pc or 0) > 0
        DBG("CLIENT-CHECK: via GetPlayerCount -> ", BOOLSTR(targetIsClient))
    end
    if pc == nil and tgtGroup.GetPlayerUnits then
        local pus = tgtGroup:GetPlayerUnits()
        local len = (type(pus) == "table") and #pus or 0
        targetIsClient = len > 0
        DBG("CLIENT-CHECK: via GetPlayerUnits (#=", tostring(len), ") -> ", BOOLSTR(targetIsClient))
    end
    if not targetIsClient and EventData.TgtDCSUnit then
        local u = FindUnitWithLog(EventData.TgtDCSUnit, "CLIENT-CHECK fallback")
        targetIsClient = (u and u.IsExist and u:IsExist() and u.IsClient and u:IsClient()) or false
        DBG("CLIENT-CHECK: via UNIT:IsClient fallback -> ", BOOLSTR(targetIsClient))
    end

    if not targetIsClient then
        DBG("INCOMING: target is NOT a client → no sound (strict mode).")
        return
    end

    -- Optional: suppress OpFor incoming if disabled
    if EventData.IniCoalition == RED and not PlayOpForShootingGuns then
        DBG("INCOMING: suppressed by PlayOpForShootingGuns=false (OpFor shooter)")
        return
    end

    -- Cooldown gate for INCOMING
    if not ShootingSfxGate("INCOMING") then return end

    -- Play incoming to victim client group
    local s = ChooseRandom(Sounds.Guns_Incoming)
    DBG("INCOMING: choosing sound=", tostring(s))
    local snd = NewSound(s)
    if not snd then
        DBG("INCOMING: NewSound failed (nil) for ", tostring(s))
        return
    end

    -- Canonize tgtGroup before playback
    local gname = tgtGroup.GetName and tgtGroup:GetName() or "?"
    local tgtGroupCanon = GROUP:FindByName(gname) or tgtGroup
    DBG(string.format("INCOMING: resolved tgtGroup name=%s obj=%s", tostring(gname), tostring(tgtGroupCanon)))

    if tgtGroupCanon and tgtGroupCanon.GetDCSObject then
        local dcs = tgtGroupCanon:GetDCSObject()
        local gid = dcs and dcs:getID() or "?"
        DBG("INCOMING: sending to GroupID=" .. tostring(gid))
        trigger.action.outTextForGroup(gid, "DEBUG: incoming sound " .. tostring(s), 2)
    end

    PlayToGroupOrCoalition(snd, tgtGroupCanon, nil)
end

if SoundDebug then BASE:I("-----GUN SHOOTING SOUNDS SET (with debug)-----") end

-----------------------------------------------------------------
-- MOOSE CLIENT MENU INTEGRATION (Soundhandler under "Moose Functions")
-----------------------------------------------------------------
MooseClientMenus = MooseClientMenus or { bySide = {} }

local function _sideNameFromNum(sideNum)
    if sideNum == coalition.side.BLUE then return "blue" end
    if sideNum == coalition.side.RED then return "red" end
    if sideNum == coalition.side.NEUTRAL then return "neutral" end
    return "neutral"
end

-- Ensure a SINGLE visible root "Moose Functions" exists for the coalition.
local function EnsureClientRootMenu(sideNum)
    local sideName = _sideNameFromNum(sideNum)
    local reg      = MooseClientMenus.bySide[sideName]
    if reg and reg.manager and reg.root and reg.root.IsDestroyed ~= true then
        return reg
    end

    local clientSet                   = SET_CLIENT:New():FilterCoalitions(sideName):FilterStart()
    local mgr                         = CLIENTMENUMANAGER:New(clientSet, "Moose Functions")
    local root                        = mgr:NewEntry("Moose Functions")

    reg                               = { manager = mgr, root = root, folders = {}, built = {} }
    MooseClientMenus.bySide[sideName] = reg

    TIMER:New(function()
        if SoundDebug then BASE:I(("[Soundhandler/ClientMenus] Init for side=%s"):format(sideName)) end
        mgr:Propagate()
        mgr:InitAutoPropagation()
    end):Start(1)

    return reg
end

-- Make/return a child folder under the visible "Moose Functions" root.
local function EnsureClientFolder(sideNum, folderName)
    local reg    = EnsureClientRootMenu(sideNum)
    local folder = reg.folders[folderName]
    if (not folder) or folder.IsDestroyed == true then
        folder = reg.manager:NewEntry(folderName, reg.root) -- parent = Moose Functions root
        reg.folders[folderName] = folder
        if SoundDebug then BASE:I(("[Soundhandler/ClientMenus] Created folder '%s'"):format(folderName)) end
    end
    return folder, reg.manager, reg
end

-----------------------------------------------------------------
-- SOUNDHANDLER MENUS under Moose Functions
-----------------------------------------------------------------
local function SoundhandlerOnOff(boolean, _Group, _Client)
    SoundHandler = boolean
    env.info("-----SoundHandler On = " .. tostring(boolean) .. "-----")
    trigger.action.outText(boolean and "**Soundhandler ON**" or "--Soundhandler OFF--", 5)
end

local function SwitchDebug(boolean, _Group, _Client)
    SoundDebug = boolean
    env.info("-----SoundDebug Now = " .. tostring(boolean) .. "-----")
end

local function SwitchSoundsToGroup(boolean, _Group, _Client)
    SoundToGroupOnly = boolean
    env.info("-----SoundToGroupOnly Now = " .. tostring(boolean) .. "-----")
    if not boolean then trigger.action.outText("--Sounds Play To All--", 5) end
end

local function BuildSoundhandlerMenus(sideNum)
    local root, mgr, reg = EnsureClientFolder(sideNum, "Soundhandler")
    if reg.built["Soundhandler"] then
        if SoundDebug then BASE:I("[Soundhandler/ClientMenus] Already built for this side, skipping") end
        return mgr
    end

    local onOffFolder = mgr:NewEntry("On or Off", root)
    local debugFolder = mgr:NewEntry("Sound Debug", root)
    local scopeFolder = mgr:NewEntry("Sounds To Group or All", root)

    mgr:NewEntry("On", onOffFolder, SoundhandlerOnOff, true, "nil")
    mgr:NewEntry("Off", onOffFolder, SoundhandlerOnOff, false, "nil")

    mgr:NewEntry("On", debugFolder, SwitchDebug, true, "nil")
    mgr:NewEntry("Off", debugFolder, SwitchDebug, false, "nil")

    mgr:NewEntry("Play Sounds to Group Only", scopeFolder, SwitchSoundsToGroup, true, "nil")
    mgr:NewEntry("Play Sounds to All", scopeFolder, SwitchSoundsToGroup, false, "nil")

    reg.built["Soundhandler"] = true
    if SoundDebug then BASE:I("[Soundhandler/ClientMenus] Added entries under Moose Functions > Soundhandler") end
    return mgr
end

BuildSoundhandlerMenus(coalition.side.BLUE)
BuildSoundhandlerMenus(coalition.side.RED)
-- BuildSoundhandlerMenus(coalition.side.NEUTRAL) -- if ever needed

-----------------------------------------------------------------------------------------------------------------------------------
-- LOGGING UTILITIES
-----------------------------------------------------------------------------------------------------------------------------------
function LogFiringUnit(EventData)
    local coalitionStr = "UNKNOWN"
    if EventData.IniCoalition == 1 then
        coalitionStr = "RED"
    elseif EventData.IniCoalition == 2 then
        coalitionStr = "BLUE"
    elseif EventData.IniCoalition == 0 then
        coalitionStr = "NEUTRAL"
    end

    local groupType = "UNIT"
    if EventData.IniGroupName then
        local group = GROUP:FindByName(EventData.IniGroupName)
        if group then
            if group:IsAirPlane() then
                groupType = "AIRPLANE"
            elseif group:IsHelicopter() then
                groupType = "HELICOPTER"
            elseif group:IsGround() then
                groupType = "GROUND UNIT"
            elseif group:IsShip() then
                groupType = "SHIP"
            end
        end
    end

    local groupName = EventData.IniGroupName or "UNKNOWN GROUP"
    BASE:I(string.format("------[SHOT] %s %s (%s)", coalitionStr, groupType, groupName))
end

function LogDeadUnit(EventData)
    local coalitionStr = "UNKNOWN"
    if EventData.IniCoalition == 1 then
        coalitionStr = "RED"
    elseif EventData.IniCoalition == 2 then
        coalitionStr = "BLUE"
    elseif EventData.IniCoalition == 0 then
        coalitionStr = "NEUTRAL"
    end

    local groupType = "UNIT"
    if EventData.IniGroupName then
        local group = GROUP:FindByName(EventData.IniGroupName)
        if group then
            if group:IsAirPlane() then
                groupType = "AIRPLANE"
            elseif group:IsHelicopter() then
                groupType = "HELICOPTER"
            elseif group:IsGround() then
                groupType = "GROUND UNIT"
            elseif group:IsShip() then
                groupType = "SHIP"
            end
        end
    end

    local groupName = EventData.IniGroupName or "UNKNOWN GROUP"
    BASE:I(string.format("------[DEAD] %s %s (%s)", coalitionStr, groupType, groupName))
end

function LogKillEvent(EventData)
    local iniUnitName     = EventData.IniUnitName or "Unknown Shooter"
    local iniGroupName    = EventData.IniGroupName or "Unknown Group"
    local tgtUnitName     = EventData.TgtUnitName or "Unknown Target"
    local tgtGroupName    = EventData.TgtGroupName or "Unknown Target Group"

    local iniCoalitionStr = "UNKNOWN"
    if EventData.IniCoalition == 1 then
        iniCoalitionStr = "RED"
    elseif EventData.IniCoalition == 2 then
        iniCoalitionStr = "BLUE"
    elseif EventData.IniCoalition == 0 then
        iniCoalitionStr = "NEUTRAL"
    end

    local tgtCoalitionStr = "UNKNOWN"
    if EventData.TgtCoalition == 1 then
        tgtCoalitionStr = "RED"
    elseif EventData.TgtCoalition == 2 then
        tgtCoalitionStr = "BLUE"
    elseif EventData.TgtCoalition == 0 then
        tgtCoalitionStr = "NEUTRAL"
    end

    local iniGroupType = "UNIT"
    local shooterGroup = GROUP:FindByName(iniGroupName)
    if shooterGroup then
        if shooterGroup:IsAirPlane() then
            iniGroupType = "AIRPLANE"
        elseif shooterGroup:IsHelicopter() then
            iniGroupType = "HELICOPTER"
        elseif shooterGroup:IsGround() then
            iniGroupType = "GROUND UNIT"
        elseif shooterGroup:IsShip() then
            iniGroupType = "SHIP"
        end
    end

    local tgtGroupType = "UNIT"
    local targetGroup = GROUP:FindByName(tgtGroupName)
    if targetGroup then
        if targetGroup:IsAirPlane() then
            tgtGroupType = "AIRPLANE"
        elseif targetGroup:IsHelicopter() then
            tgtGroupType = "HELICOPTER"
        elseif targetGroup:IsGround() then
            tgtGroupType = "GROUND UNIT"
        elseif targetGroup:IsShip() then
            tgtGroupType = "SHIP"
        end
    end

    BASE:I(string.format(
        "-----[UNIT KILL] %s %s (%s: %s) killed %s %s (%s: %s)",
        iniCoalitionStr, iniGroupType, iniGroupName, iniUnitName,
        tgtCoalitionStr, tgtGroupType, tgtGroupName, tgtUnitName
    ))
end

env.info("-----DCSRetribution|MOOSE Soundhandler plugin - configuration end -----")
