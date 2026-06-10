--[[
C-130J-30 Mission Systems Script for DCS World.
Combines EC-130H Compass Call electronic warfare and RC-130H Rivet Joint ISR capabilities.

EW:  Area and directional jamming, spot SAM suppression, missile spoofing,
     overheat energy management, pod loadout selection, radar-type jam difficulty.
ISR: Altitude-gated radar detection, up to 3 simultaneous ELINT tracks with progressive
     location refinement, displacement alerting, high-priority threat alerts,
     F10 map marks, Bullseye reporting, ELINT Lock coalition alert.
COORD: EW/ISR handoff brief deliverable to any selected friendly group.

Original EW script by Timberwolf, C-130 conversion by claude and Flash.
ISR conversion and merge by bradyccox.
--]]

-- ===========================================================================
-- CONFIGURATION
-- Adjust these values to tune difficulty and behaviour.
-- No other part of the script needs to be touched.
-- ===========================================================================

-- ── EW — energy ────────────────────────────────────────────────────────────
local CFG_regenPerSec      = 5      -- capacity regen per second when idle
local CFG_drainAreaPerSec  = 3      -- capacity drain per second: area jamming
local CFG_drainDirPerSec   = 1      -- capacity drain per second: directional jamming
local CFG_spotDrainPerSec  = 5      -- capacity drain per second: spot jamming
local CFG_overheatResetCap = 450    -- minimum capacity required to clear an overheat
local CFG_jamMaxRange      = 370400 -- maximum offensive jam range in metres (~200nm, theater-wide)
local CFG_lowCapWarnPct    = 0.20   -- warn crew when capacity falls below this fraction of max (0.20 = 20%)

-- ── EW — missile spoofing ──────────────────────────────────────────────────
-- One roll per second. Only the tightest matching zone fires (no stacking).
-- pk = percent chance (0-100) of spoofing the missile that tick.
-- Missile spoofing probability by range. Probability is per-tick (1/sec); the missile must
-- enter a zone and survive a random roll to be defeated. Zones are checked tightest-first so
-- only the innermost matching zone applies. The curve is intentionally steep at close range —
-- missiles should almost always fly in close before guidance breaks (dramatic, realistic feel).
local CFG_spoofZones = {
    { dist = 37000, pk = 3  },  -- ~20nm: barely working at range
    { dist = 27800, pk = 8  },  -- ~15nm: guidance starting to degrade
    { dist = 18500, pk = 18 },  -- ~10nm: working but unreliable
    { dist = 11100, pk = 48 },  -- ~6nm:  sweet spot — most missiles caught ~4-5nm
    { dist = 5556,  pk = 82 },  -- ~3nm:  backstop for anything that slips through
    { dist = 2778,  pk = 95 },  -- ~1.5nm: final backstop
}
-- A missile is never spoofed until it has flown at least this far from its launch
-- vehicle, so destroying it can't damage the launcher (no "explodes on launch").
local CFG_spoofMinTravel = 5556  -- metres (~3nm)

-- ── EW — offensive jamming ─────────────────────────────────────────────────
-- BURN-THROUGH MODEL: a standoff jammer is most effective at long range. Up close the
-- radar's skin return overpowers the noise ("burns through"), so jamming is weak.
-- Effectiveness therefore RISES with distance to the emitter.
-- Final jam probability = base (by distance) × system difficulty × cross-band penalty × mode power.
-- Bands are checked nearest-first; the first match wins.
local CFG_jamProbBands = {
    { dist = 18500,  prob = 0.40 },  -- <= 10nm: radar burns through, jamming barely works
    { dist = 46300,  prob = 0.62 },  -- <= 25nm
    { dist = 92600,  prob = 0.82 },  -- <= 50nm
    { dist = 185200, prob = 0.93 },  -- <= 100nm
    { dist = 370400, prob = 0.98 },  -- <= 200nm: full standoff effectiveness
}
local CFG_crossBandPenalty = 0.60    -- multiplier when pods don't cover a system's frequency band

-- Jam reach scales with altitude (like ISR detection). On the deck you reach only
-- CFG_jamFloorRange; climbing extends it up to CFG_jamMaxRange.
local CFG_jamFloorRange    = 46300   -- jam range at sea level in metres (~25nm)

-- Mode hierarchy — broad coverage trades power; focused modes hit harder.
local CFG_areaSpreadFactor   = 0.65  -- area (omnidirectional) effectiveness vs focused directional/spot
local CFG_spotPunchThrough   = 0.50  -- spot jamming recovers this fraction of a system's ECCM resistance
local CFG_drainPerSuppressed = 0.5   -- extra capacity/sec per emitter held down by area/directional jamming

-- Spot jamming is the focused single-target tool: a flat, altitude-INDEPENDENT reach
-- (unlike area/directional, which scale with altitude and burn-through).
local CFG_spotMaxRange = 185200      -- spot jam reach in metres (~100nm)
local CFG_spotFullEff  = 129600      -- within this radius spot is full power (~70nm); tapers beyond

-- ── ISR ────────────────────────────────────────────────────────────────────
local CFG_sweepInterval         = 5    -- seconds between radar sweeps
local CFG_markRefreshInterval   = 15   -- seconds between F10 map mark updates
local CFG_trackMinTime          = 60   -- fastest ELINT lock time in seconds (close range)
local CFG_trackMaxTime          = 360  -- slowest ELINT lock time in seconds (max range)
local CFG_refinementMult        = 4    -- phase-2 (85→100%) lasts this many × the phase-1 duration
local CFG_errorInitialNm        = 50   -- position error (nm) at 0% confidence
local CFG_errorPhase1Nm         = 10   -- position error (nm) at Phase 1 lock (85%)
local CFG_errorInitialBrg       = 30   -- bearing error (degrees) at 0% confidence
local CFG_errorPhase1Brg        = 5    -- bearing error (degrees) at Phase 1 lock (85%)
local CFG_displacementThreshold = 500  -- metres an emitter must move to trigger displacement alert
local CFG_maxTracks             = 3    -- maximum simultaneous ELINT tracks

-- ── Messages ───────────────────────────────────────────────────────────────
local CFG_msgGap            = 10   -- seconds between message queue flushes
local CFG_msgDur            = 15   -- seconds a flushed message stays on screen
local CFG_ewStatusInterval  = 30   -- minimum seconds between EW status line updates
local CFG_isrStatusInterval = 30   -- minimum seconds between ISR status line updates

-- ── Retribution plugin config override ────────────────────────────────────
-- dcsRetribution.plugins.c130j is written by Retribution AFTER this script
-- loads, so we apply overrides at T+0 (next tick) when all triggers have fired.
timer.scheduleFunction(function()
    if not (dcsRetribution and dcsRetribution.plugins and dcsRetribution.plugins.c130j) then return end
    local c = dcsRetribution.plugins.c130j
    if c.regenPerSec      ~= nil then CFG_regenPerSec      = c.regenPerSec      end
    if c.drainAreaPerSec  ~= nil then CFG_drainAreaPerSec  = c.drainAreaPerSec  end
    if c.spotDrainPerSec  ~= nil then CFG_spotDrainPerSec  = c.spotDrainPerSec  end
    if c.jamMaxRange      ~= nil then CFG_jamMaxRange       = c.jamMaxRange  * 1852 end  -- NM → metres
    if c.spotMaxRange     ~= nil then CFG_spotMaxRange      = c.spotMaxRange * 1852 end  -- NM → metres
    if c.maxTracks        ~= nil then CFG_maxTracks         = c.maxTracks        end
    if c.msgDur           ~= nil then CFG_msgDur            = c.msgDur           end
end, nil, timer.getTime() + 0)

-- ===========================================================================

-- ---------------------------------------------------------------------------
-- Shared utility
-- ---------------------------------------------------------------------------

local function getHeading(unit)
    if not unit or not unit.isExist or not unit:isExist() then return 0 end
    local pos = unit:getPosition()
    if not pos or not pos.x then return 0 end
    local hdg = math.atan2(pos.x.z, pos.x.x)
    if hdg < 0 then hdg = hdg + 2 * math.pi end
    return hdg
end

local function get3DDist(p1, p2)
    local dx = (p1.x or 0) - (p2.x or 0)
    local dy = (p1.y or 0) - (p2.y or 0)
    local dz = (p1.z or 0) - (p2.z or 0)
    return math.sqrt(dx*dx + dy*dy + dz*dz)
end

-- Line-of-sight check between a radar and an observer. The radar point is lifted 30m
-- because many DCS 3D models sit dug into the terrain, which falsely fails raw LOS tests.
local function hasLOS(radarPt, obsPt)
    local lifted = { x = radarPt.x, y = (radarPt.y or 0) + 30, z = radarPt.z }
    return land.isVisible(lifted, obsPt)
end

local function getBearing(from, to)
    local dx = to.x - from.x
    local dz = to.z - from.z
    local b  = math.deg(math.atan2(dz, dx))
    if b < 0 then b = b + 360 end
    return math.floor(b + 0.5)
end

local function getClockBearing(fromUnit, targetPos)
    if not fromUnit or not fromUnit:isExist() then return "?" end
    local jp  = fromUnit:getPosition().p
    local hdg = getHeading(fromUnit)
    local dx  = targetPos.x - jp.x
    local dz  = targetPos.z - jp.z
    local ang = math.atan2(dz, dx)
    local rel = ang - hdg
    if rel < 0 then rel = rel + 2 * math.pi end
    local hours = math.floor((rel / (2 * math.pi)) * 12 + 0.5)
    if hours == 0 then hours = 12 end
    return tostring(hours) .. " o'clock"
end

local function isRadarUnit(u)
    if not u or not u:isExist() then return false end
    -- An air-defense emitter is anything with an actual radar sensor or a SAM radar
    -- attribute. This deliberately includes radar-directed AAA (ZSU-23 Shilka,
    -- Gepard, M163 Vulcan). Optical AAA (ZU-23, ZPU, ZSU-57) carry no radar sensor
    -- and are excluded naturally, as are launchers and non-emitter ground units.
    local d = u:getDesc()
    if d and d.sensor and d.sensor.radar then return true end
    return u:hasAttribute("SAM TR") or u:hasAttribute("SAM SR") or u:hasAttribute("SAM STR")
end

-- A radar emitter worth tracking/jamming as a SAM/EWR site — excludes radar-directed
-- AAA / CIWS (ZSU-23 Shilka, Gepard, M163 Vulcan, Phalanx, SA-19 Tunguska: all carry the
-- AAA attribute). Used for ISR detection, SIGINT, tracking, and the spot list.
local function isImportantRadar(u)
    return isRadarUnit(u) and not u:hasAttribute("AAA")
end

local function getNatoName(unit)
    local t = unit:getTypeName()
    local m = {
        ["S-300PS 40B6M tr"]    = "SA-10", ["S-300PS 40B6MD sr"]    = "SA-10",
        ["S-300PS 64H6E sr"]    = "SA-10", ["S-300PS 5P85C ln"]     = "SA-10",
        ["S-300PS 5P85D ln"]    = "SA-10", ["S-300PS 54K6 cp"]      = "SA-10",
        ["SA-11 Buk SR 9S18M1"] = "SA-11", ["SA-11 Buk LN 9A310M1"] = "SA-11",
        ["SA-15 Tor 9A331"]     = "SA-15",
        ["SA-8 Osa 9A33 ln"]   = "SA-8",  ["Kub 1S91 str"]         = "SA-6",
        ["SNR_75V"]             = "SA-2",  ["p-19 s-125 sr"]        = "SA-3",
        ["snr s-125 tr"]        = "SA-3",  ["RPC_5N62V"]            = "SA-5",
        ["Dog Ear radar"]       = "Dog Ear",
        ["1L13 EWR"]            = "EWR",   ["55G6 EWR"]             = "EWR",
        ["Hawk tr"]             = "Hawk TR", ["Hawk sr"]             = "Hawk SR",
        ["Hawk cwar"]           = "Hawk CWAR",
        ["HQ-7_STR_SP"]         = "HQ-7",  ["HQ-7_SR"]             = "HQ-7 SR",
        ["Roland ADS"]          = "Roland", ["Roland Radar"]        = "Roland",
        ["ZSU-23-4 Shilka"]     = "ZSU-23",
    }
    if m[t] then return m[t] end

    -- Substring fallback (case-insensitive, plain match) for systems whose exact
    -- DCS type names vary or aren't enumerated above (e.g. Tunguska, S-300 variants).
    -- Order matters: more specific keywords first.
    local lt  = t:lower()
    local sub = {
        { "s-300",     "SA-10" },
        { "5n62",      "SA-5" },    { "square pair", "SA-5" },  { "s-200",  "SA-5" },
        { "tunguska",  "SA-19" },   { "2s6",         "SA-19" },
        { "roland",    "Roland" },  { "shilka",      "ZSU-23" },
        -- search / early-warning radars → EWR class
        { "bar lock",  "EWR" },     { "p-37",        "EWR" },
        { "side net",  "EWR" },     { "prw-11",      "EWR" },
        { "tin shield","EWR" },     { "st-68",       "EWR" },   { "19j6", "EWR" },
        { "tall king", "EWR" },     { "p-14",        "EWR" },
    }
    for _, pair in ipairs(sub) do
        if lt:find(pair[1], 1, true) then return pair[2] end
    end

    return t:gsub("^CHAP_", "")
end

local function bullseyeStr(pos)
    local be = coalition.getMainRefPoint(coalition.side.BLUE)
    if not be then return "no BE" end
    local brg  = getBearing(be, pos)
    local dist = math.floor(get3DDist(be, pos) / 1852 + 0.5)
    return string.format("BE %03d/%d", brg, dist)
end

-- ---------------------------------------------------------------------------
-- Eligible aircraft
-- ---------------------------------------------------------------------------

local eligibleTypeNames = { ["C-130J-30"] = true }

-- ---------------------------------------------------------------------------
-- Shared unit registry
-- ---------------------------------------------------------------------------

local unitNames    = {}   -- list of registered unit names
local groupIDs     = {}   -- name -> groupID
local rootMenus    = {}   -- name -> root menu handle
local ewMenus      = {}   -- name -> EW submenu handle
local isrMenus     = {}   -- name -> ISR submenu handle
local coordMenus   = {}   -- name -> Crew Coordination submenu handle
local _staticSlots = {}   -- set of unit names that existed at mission start

-- ---------------------------------------------------------------------------
-- EW state
-- ---------------------------------------------------------------------------

local ewSettings         = {}
local spotTargetMenus    = {}
local spotTargetCmds     = {}
local emitterCapacity    = {}
local maxEmitterCapacity = {}
local overheated         = {}
local loadoutConfigured   = {}
local selectedLoadoutName = {}   -- name -> active preset label (e.g. "Full Spectrum")
local loadoutBands        = {}   -- name -> { hi = bool, lo = bool }
local podEnabled          = {}
local trackedMissiles    = {}
local missileUID         = 1
local suppressedSAMs     = {}
local _preciseFixLog     = {}   -- ordered list of { nato, be, missionTime } — written to file on each fix
local writeISRPreciseFixLog    -- forward declaration; defined before the event handler
local _spotState         = {}   -- name -> { target, nato, suppressed } for coalition spot-jam broadcasts
local _lastJamAttempt    = {}   -- gname -> { time, cooldown }
local _lowCapWarned      = {}   -- name -> bool, true once low-cap alert has fired this drain cycle
local autoTriangulate    = {}   -- name -> bool, auto-fill slots closest-first + instant high-priority (default ON)

-- (EW scalars defined in CONFIG block above)

-- Jam difficulty multiplier by NATO name.
-- This is a large, dedicated theater jammer — base effectiveness is very high.
-- These multipliers model only the RELATIVE ECCM resistance between systems; even
-- the toughest are jammed reliably. 1.0 = no penalty, lower = harder to jam.
-- Final jam probability = base_prob_by_distance * jamDifficulty[nato] * cross-band penalty.
-- Systems not listed default to 1.0 (full probability).
local jamDifficulty = {

    -- ── Tier 1: Modern long-range / phased-array (very high ECCM) ──────────
    -- SA-10 / S-300PS: frequency agile, advanced ECCM, designed to defeat
    --   standoff jamming.  The hardest target in the set, short jam window (30s) —
    --   its ECCM actively burns through the jamming signal.
    ["SA-10"]    = 0.80,

    -- ── Tier 2: Modern medium-range (capable ECCM) ─────────────────────────
    -- SA-11 / Buk M1: semi-active radar, some frequency agility, reasonable ECCM.
    --   Jammable but re-acquires in 40s.
    ["SA-11"]    = 0.85,

    -- SA-15 / Tor M1: autonomous short-range, frequency agile, good ECCM.
    --   Smaller footprint makes it harder to spot and jam simultaneously; 45s window.
    ["SA-15"]    = 0.86,

    -- ── Tier 3: Semi-modern medium-range (partial ECCM) ───────────────────
    -- Hawk TR (tracking radar): narrowband CW, moderate ECCM.
    ["Hawk TR"]  = 0.84,

    -- Hawk CWAR (continuous-wave acquisition radar): older design, lower ECCM.
    ["Hawk CWAR"] = 0.86,

    -- Hawk SR (search radar): lower frequency, moderate jam resistance.
    ["Hawk SR"]  = 0.88,

    -- ── Tier 4: Cold-War era mobile systems (limited ECCM) ─────────────────
    -- SA-19 / 2S6 Tunguska: gun+missile combo, radar-guided guns,
    --   limited ECCM but fast engagement radar. Harder to break than SA-6.
    ["SA-19"]    = 0.86,

    -- SA-6 / Kub: continuous-wave illuminator, older ECCM, well-studied.
    ["SA-6"]     = 0.89,

    -- SA-8 / Osa: self-contained, J-band, aging ECCM.
    ["SA-8"]     = 0.92,

    -- Roland: French/German short-range, K-band, moderate ECCM for its era.
    ["Roland"]   = 0.92,

    -- HQ-7: Chinese Crotale derivative, similar ECM resistance to Roland.
    ["HQ-7"]     = 0.91,

    -- ── Tier 5: Legacy / early Cold-War (poor ECCM) ────────────────────────
    -- SA-3 / S-125: low-frequency E-band, old design.
    ["SA-3"]     = 0.93,

    -- SA-5 / S-200: enormous range but a 1960s Square Pair radar with weak ECCM —
    --   a priority threat because of its reach.
    ["SA-5"]     = 0.86,

    -- SA-2 / S-75: very old G/H-band, minimal ECCM, easily defeated.
    ["SA-2"]     = 0.96,

    -- ZSU-23 / Shilka: gun radar, simple J-band fire-control, minimal ECCM.
    ["ZSU-23"]   = 0.96,

    -- ── Tier 6: Radars / EWR (minimal jam resistance) ──────────────────────
    -- Dog Ear (P-19): simple VHF acquisition radar, no meaningful ECCM.
    ["Dog Ear"]  = 0.98,

    -- Generic early-warning radars: designed to detect, not to survive jamming.
    ["EWR"]      = 0.99,
}

-- How long (seconds) a successful jam holds before the next dice roll.
-- Modern systems with active ECCM burn through jamming faster.
-- Systems not listed use the default of 60s.
local jamDuration = {
    ["SA-10"]   = 30,   -- actively frequency-hops to break jamming
    ["SA-11"]   = 40,   -- semi-modern ECCM
    ["SA-15"]   = 45,   -- fast autonomous re-acquisition
}

-- Frequency band classification.
-- Lo-band (L/S/C-band) pods target long-range acquisition and search radars.
-- Hi-band (X/K-band) pods target tracking radars and terminal guidance systems.
-- Systems not listed here are treated as hi-band (tracking/short-range).
local loBandSystems = {
    ["SA-10"]    = true,   -- S-band acquisition / Flap Lid
    ["SA-2"]     = true,   -- G/H-band early Cold-War
    ["SA-3"]     = true,   -- E-band low-alt
    ["SA-5"]     = true,   -- long-range strategic, treated as lo-band like SA-10
    ["SA-6"]     = true,   -- C-band CW illuminator
    ["Hawk SR"]  = true,   -- L-band search radar
    ["Hawk CWAR"]= true,   -- S-band CWAR
    ["Dog Ear"]  = true,   -- VHF/UHF acquisition
    ["EWR"]      = true,   -- early-warning / long-range surveillance
}

-- ---------------------------------------------------------------------------
-- ISR state
-- ---------------------------------------------------------------------------

local trackMenus         = {}   -- name -> Track Emitter submenu
local trackCmds          = {}   -- name -> list of track commands
local stopTrackMenus     = {}   -- name -> Stop Track submenu
local stopTrackCmds      = {}   -- name -> list of stop-track commands
local coordCmds          = {}   -- name -> list of coord brief commands
local knownEmitters      = {}   -- name -> { gname = { pos, seenAt, unit, nato } }
local markedTarget       = {}   -- name -> { gname = track }  (active tracks only)
local elintParked        = {}   -- name -> { gname = "locked" | "precise" }  (Phase-1 done / fully done)
local lockedMarkIDs      = {}   -- name -> list of permanently kept markIDs
local _lastSweep         = {}

-- (ISR scalars defined in CONFIG block above)

-- High-priority NATO names that trigger an immediate crew-only threat alert
-- on first detection (bypasses the message queue).
local highPriorityThreats = {
    ["SA-10"]   = true,   -- S-300: long-range, aircraft-killing threat
    ["SA-5"]    = true,   -- S-200: very long-range aircraft killer
    ["SA-11"]   = true,   -- Buk M1: medium-range, high-speed engagement
    ["SA-15"]   = true,   -- Tor M1: point-defense, very fast reaction
}

local markIDCounter = 3000
local function nextMarkID()
    markIDCounter = markIDCounter + 1
    return markIDCounter
end

local function countTracks(name)
    local n = 0
    for _ in pairs(markedTarget[name] or {}) do n = n + 1 end
    return n
end

-- ---------------------------------------------------------------------------
-- Message queue
-- ---------------------------------------------------------------------------

-- (message queue scalars defined in CONFIG block above)

local _msgQueue          = {}
local _flushTimer        = {}
local _evtSeenInSlot     = {}
local _lastEWStatusTime  = {}
local _lastISRStatusTime = {}

local function _nextAligned(now, gap)
    return (math.floor(now / gap) + 1) * gap
end

local function _ensureQueue(name)
    local q = _msgQueue[name]
    if not q then
        q = { ewStatus = nil, isrStatus = nil, events = {},
              target = _nextAligned(timer.getTime(), CFG_msgGap) }
        _msgQueue[name] = q
    elseif not q.target then
        q.target = _nextAligned(timer.getTime(), CFG_msgGap)
    end
    return q
end

local function _scheduleFlush(name)
    if _flushTimer[name] then return end
    local q = _msgQueue[name]; if not q then return end
    _flushTimer[name] = timer.scheduleFunction(function()
        local cur = _msgQueue[name]; _flushTimer[name] = nil
        if cur then
            local lines = {}
            if cur.ewStatus  and #cur.ewStatus  > 0 then lines[#lines+1] = cur.ewStatus  end
            if cur.isrStatus and #cur.isrStatus > 0 then lines[#lines+1] = cur.isrStatus end
            if cur.events    and #cur.events    > 0 then lines[#lines+1] = table.concat(cur.events, " | ") end
            if #lines > 0 then
                local gid = groupIDs[name]
                if gid then trigger.action.outTextForGroup(gid, table.concat(lines, "\n"), CFG_msgDur) end
            end
        end
        _msgQueue[name]      = nil
        _evtSeenInSlot[name] = nil
        return nil
    end, {}, q.target)
end

local function emitEWStatus(name, msg)
    if not groupIDs[name] then return end
    local q = _ensureQueue(name); q.ewStatus = msg; _scheduleFlush(name)
end

local function emitISRStatus(name, msg)
    if not groupIDs[name] then return end
    local q = _ensureQueue(name); q.isrStatus = msg; _scheduleFlush(name)
end

local function emitEvent(name, msg)
    if not groupIDs[name] then return end
    local q    = _ensureQueue(name)
    local slot = q.target or 0
    local seen = _evtSeenInSlot[name]
    if not seen or seen.slot ~= slot then
        seen = { slot = slot, set = {} }; _evtSeenInSlot[name] = seen
    end
    if not seen.set[msg] then
        seen.set[msg] = true; table.insert(q.events, msg)
    end
    _scheduleFlush(name)
end

-- Immediate display bypassing the queue (for threat alerts)
local function emitImmediate(name, msg)
    local gid = groupIDs[name]; if not gid then return end
    trigger.action.outTextForGroup(gid, msg, CFG_msgDur)
end

-- True if any jamming mode is currently engaged.
local function ewActive(name)
    local s = ewSettings[name] or {}
    return (s.defensive or s.offensive or s.defDir or s.offDir or s.spotTarget) and true or false
end

-- Routine ISR chatter — suppressed while the crew is actively jamming, to cut spam.
-- (Threat alerts and coalition ELINT broadcasts are NOT routed through this.)
local function emitISR(name, msg)
    if ewActive(name) then return end
    emitEvent(name, msg)
end

-- ---------------------------------------------------------------------------
-- EW helpers
-- ---------------------------------------------------------------------------

local function formatPodsText(name)
    return selectedLoadoutName[name] or "None"
end

local function closeAllEW(name, silent)
    ewSettings[name] = ewSettings[name] or {}
    ewSettings[name].defensive  = false
    ewSettings[name].offensive  = false
    ewSettings[name].defDir     = nil
    ewSettings[name].offDir     = nil
    ewSettings[name].spotTarget = nil
    if not silent then emitEvent(name, "EW disabled: all modes off") end
end

local function inSector(jammerUnit, targetPos, sector)
    if not jammerUnit or not jammerUnit:isExist() then return false end
    local jp  = jammerUnit:getPosition().p
    local hdg = math.deg(getHeading(jammerUnit))
    local ang = math.deg(math.atan2(targetPos.z - jp.z, targetPos.x - jp.x))
    local rel = (ang - hdg) % 360
    if sector == "front" then return rel >= 315 or rel <= 45
    elseif sector == "right" then return rel > 45  and rel <= 135
    elseif sector == "rear"  then return rel > 135 and rel <= 225
    elseif sector == "left"  then return rel > 225 and rel <  315 end
    return false
end

local function computeJamAttemptCooldown(distMeters)
    local frac = math.min(distMeters / CFG_jamMaxRange, 1.0)
    return 1 + frac * 29
end

-- Altitude-scaled offensive/spot jam range. Low altitude = short reach, climbing
-- extends it to the theater maximum. Mirrors the ISR detection model.
local function getJamRange(unit)
    if not unit or not unit:isExist() then return CFG_jamFloorRange end
    local alt = math.max(0, unit:getPoint().y)
    return math.min(CFG_jamFloorRange + alt * 20, CFG_jamMaxRange)
end

-- How many emitters are currently held down by area/directional (non-spot) jamming.
-- Used to scale capacity drain so suppressing a whole IADS costs more than one site.
local function countAreaSuppressions()
    local n   = 0
    local now = timer.getTime()
    for _, info in pairs(suppressedSAMs) do
        if not info.spot and (now - (info.lastSuppressed or 0) <= (info.duration or 60)) then
            n = n + 1
        end
    end
    return n
end

local function computeModeAndDrainPerSec(name)
    local s = ewSettings[name] or {}
    local drain, modeOn = 0, {}
    if s.defensive  then drain = drain + CFG_drainAreaPerSec; modeOn[#modeOn+1] = "Area Defense"               end
    if s.offensive  then drain = drain + CFG_drainAreaPerSec; modeOn[#modeOn+1] = "Area Offense"               end
    if s.defDir     then drain = drain + CFG_drainDirPerSec;  modeOn[#modeOn+1] = "Dir Defense:" .. s.defDir   end
    if s.offDir     then drain = drain + CFG_drainDirPerSec;  modeOn[#modeOn+1] = "Dir Offense:" .. s.offDir   end
    if s.spotTarget then drain = drain + CFG_spotDrainPerSec; modeOn[#modeOn+1] = "Spot"                       end
    -- Per-target cost: every emitter held down by area/directional jamming adds drain.
    if s.offensive or s.offDir then
        drain = drain + CFG_drainPerSuppressed * countAreaSuppressions()
    end
    return (#modeOn > 0) and table.concat(modeOn, ", ") or "Off", drain
end

-- ---------------------------------------------------------------------------
-- EW status line
-- ---------------------------------------------------------------------------

local function ewStatusBrief(name)
    if not loadoutConfigured[name]
    or not emitterCapacity[name]
    or (maxEmitterCapacity[name] or 0) <= 0
    or podEnabled[name] == false then return end

    local now = timer.getTime()
    if _lastEWStatusTime[name] and (now - _lastEWStatusTime[name]) < CFG_ewStatusInterval then return end
    _lastEWStatusTime[name] = now

    local u = Unit.getByName(name); if not u or not u:isExist() then return end

    local cap    = emitterCapacity[name] or 0
    local capMax = maxEmitterCapacity[name] or 0
    local capPct = (capMax > 0) and math.floor(cap / capMax * 100 + 0.5) or 0
    local modeText, drainPerSec = computeModeAndDrainPerSec(name)

    if overheated[name] and cap < CFG_overheatResetCap then
        local needPct = (capMax > 0) and math.floor(CFG_overheatResetCap / capMax * 100 + 0.5) or 0
        emitEWStatus(name, string.format(
            "EW | Pods: %s | Power: %d%% | OVERHEAT (need %d%%)",
            formatPodsText(name), capPct, needPct))
        return
    end

    local state = drainPerSec > 0 and "draining"
        or (capMax > 0 and cap >= capMax) and "full" or "recharging"

    emitEWStatus(name, string.format(
        "EW | Pods: %s | Power: %d%% | Mode: %s | %s",
        formatPodsText(name), capPct, modeText, state))
end

-- ---------------------------------------------------------------------------
-- EW tactics
-- ---------------------------------------------------------------------------

-- Drop tracked missiles that have impacted or been destroyed.
-- Runs every ewTick regardless of loadout/mode so the table never grows unbounded.
local function purgeDeadMissiles()
    for id, entry in pairs(trackedMissiles) do
        local m = entry.missile
        if not (m and Object.isExist(m)) then
            trackedMissiles[id] = nil
        end
    end
end

local function defensiveLoop(name)
    -- Missile spoofing requires hi-band pods (X/K-band guidance jamming)
    local bands = loadoutBands[name]
    if bands and not bands.hi then return end
    local s    = ewSettings[name] or {}
    local unit = Unit.getByName(name); if not unit or not unit:isExist() then return end
    local pos  = unit:getPoint()
    local spoof = CFG_spoofZones  -- zones defined in CONFIG block at top of file
    for id, entry in pairs(trackedMissiles) do
        local m = entry.missile
        if m and Object.isExist(m) then
            local mp      = m:getPoint()
            local dist    = get3DDist(pos, mp)
            local allowed = s.defensive or (s.defDir and inSector(unit, mp, s.defDir))
            -- Don't spoof until the missile has cleared its launch vehicle.
            if allowed and entry.launchPos and get3DDist(mp, entry.launchPos) < CFG_spoofMinTravel then
                allowed = false
            end
            if allowed then
                -- Find the tightest applicable zone and roll once
                local pk = nil
                for _, z in ipairs(spoof) do
                    if dist < z.dist then pk = z.pk end
                end
                if pk and math.random(100) <= pk then
                    emitEvent(name, "Spoofed missile, ~" .. math.floor(dist/1852) .. "nm (" .. getClockBearing(unit, mp) .. ")")
                    Object.destroy(m)
                    trackedMissiles[id] = nil
                end
            end
        end
    end
end

local function offensiveLoop(name)
    local s    = ewSettings[name] or {}
    local unit = Unit.getByName(name); if not unit or not unit:isExist() then return end
    local jp       = unit:getPoint()
    local jamRange = getJamRange(unit)
    local cats     = { Group.Category.GROUND, Group.Category.SHIP }
    -- Track per-tick outcomes for aggregated failure reporting (see end of function).
    local failCount  = 0
    local anySuccess = false
    for _, cat in ipairs(cats) do
        local groups = coalition.getGroups(coalition.side.RED, cat) or {}
        for _, g in ipairs(groups) do
            if g and g.isExist and g:isExist() then
                for _, u in ipairs(g:getUnits() or {}) do
                    if u and u.isExist and u:isExist() and isRadarUnit(u) then
                        local up    = u:getPoint()
                        local dist  = get3DDist(jp, up)
                        local gname = g:getName()
                        local now   = timer.getTime()
                        local inDir   = s.offDir and inSector(unit, up, s.offDir)
                        local allowed = s.offensive or inDir

                        local existing = suppressedSAMs[gname]
                        local alreadySuppressed = existing and not existing.spot
                            and (now - (existing.lastSuppressed or 0) <= (existing.duration or 60))

                        local attempt    = _lastJamAttempt[gname]
                        local onCooldown = attempt and (now - attempt.time) < attempt.cooldown

                        if allowed and not alreadySuppressed and not onCooldown
                        and dist < jamRange and hasLOS(up, jp) then
                            -- Base probability by distance (theater jammer — high and long-ranged)
                            local prob = CFG_jamProbBands[#CFG_jamProbBands].prob
                            for _, band in ipairs(CFG_jamProbBands) do
                                if dist <= band.dist then prob = band.prob; break end
                            end
                            -- Apply radar-type jam difficulty
                            local nato = getNatoName(u)
                            prob = prob * (jamDifficulty[nato] or 1.0)
                            -- Apply cross-band penalty if pods don't cover this system's frequency
                            local bands = loadoutBands[name]
                            if bands then
                                local isLo = loBandSystems[nato]
                                if (isLo and not bands.lo) or (not isLo and not bands.hi) then
                                    prob = prob * CFG_crossBandPenalty
                                end
                            end
                            -- Mode power: focused directional hits at full strength;
                            -- broad omnidirectional area jamming spreads power thinner.
                            prob = prob * (inDir and 1.0 or CFG_areaSpreadFactor)

                            if math.random() < prob then
                                local ctrl = g:getController()
                                if ctrl and ctrl.setOption then ctrl:setOption(AI.Option.Ground.id.ROE, AI.Option.Ground.val.ROE.WEAPON_HOLD) end
                                local dur = jamDuration[nato] or 60
                                suppressedSAMs[gname] = { sam = u, lastSuppressed = now, spot = false, duration = dur, nato = nato }
                                _lastJamAttempt[gname] = nil
                                local gid = groupIDs[name]
                                if gid then trigger.action.outTextForGroup(gid, "Suppressed: " .. nato .. " — clear to engage", dur) end
                                anySuccess = true
                            else
                                _lastJamAttempt[gname] = { time = now, cooldown = computeJamAttemptCooldown(dist) }
                                failCount = failCount + 1
                            end
                        end
                        break
                    end
                end
            end
        end
    end
    -- Emit a single aggregated failure note only when nothing locked this tick.
    -- If any suppression succeeded the crew already has persistent banners; silence is cleaner.
    if failCount > 0 and not anySuccess then
        emitEvent(name, "Jam: no lock (" .. failCount .. " site(s))")
    end
end

local function restoreSAMs()
    for gname, info in pairs(suppressedSAMs) do
        local sam  = info.sam
        local keep = false
        if info.spot then
            for _, jammer in ipairs(unitNames) do
                local s = ewSettings[jammer]
                if s and s.spotTarget == gname then
                    local ju = Unit.getByName(jammer)
                    if ju and ju:isExist() and sam and sam:isExist() then
                        if get3DDist(ju:getPoint(), sam:getPoint()) <= CFG_spotMaxRange
                        and hasLOS(sam:getPoint(), ju:getPoint())
                        and (emitterCapacity[jammer] or 0) > 15 then
                            keep = true; break
                        end
                    end
                end
            end
        else
            keep = (timer.getTime() - (info.lastSuppressed or 0) <= (info.duration or 60))
        end
        if not keep then
            if sam and sam.isExist and sam:isExist() then
                -- Jam window expired normally — restore ROE
                local ctrl = sam:getGroup():getController()
                if ctrl and ctrl.setOption then ctrl:setOption(AI.Option.Ground.id.ROE, AI.Option.Ground.val.ROE.OPEN_FIRE) end
            else
                -- Radar unit no longer exists — site was destroyed while suppressed
                local label = info.nato or gname
                for _, jname in ipairs(unitNames) do
                    emitImmediate(jname, "THREAT NEUTRALIZED: " .. label)
                end
            end
            suppressedSAMs[gname] = nil
        end
    end
end

-- Coalition-wide spot-jam broadcasts. Announces only on state change so other BLUE
-- flights know when a site is being worked and whether it is currently silenced.
local function endSpotBroadcast(name)
    local st = _spotState[name]; if not st then return end
    _spotState[name] = nil
    trigger.action.outTextForCoalition(coalition.side.BLUE,
        string.format("SPOT JAM ENDED: %s — may re-engage", st.nato or "target"), st.duration or 60)
end

local function spotJammingTick(name)
    local s        = ewSettings[name] or {}
    local tgtGroup = s.spotTarget
    if not tgtGroup then return end

    if (emitterCapacity[name] or 0) <= CFG_spotDrainPerSec then
        ewSettings[name].spotTarget = nil
        endSpotBroadcast(name)
        emitImmediate(name, "Spot jamming stopped: insufficient capacity"); return
    end

    local ju = Unit.getByName(name); if not ju or not ju:isExist() then return end
    local g  = Group.getByName(tgtGroup)
    if not g or not g:isExist() then
        ewSettings[name].spotTarget = nil
        endSpotBroadcast(name)
        emitImmediate(name, "Spot jamming cancelled: target lost"); return
    end

    local tu = nil
    for _, u in ipairs(g:getUnits() or {}) do if u and u.isExist and u:isExist() then tu = u; break end end
    if not tu then
        ewSettings[name].spotTarget = nil
        endSpotBroadcast(name)
        emitImmediate(name, "Spot jamming cancelled: target destroyed"); return
    end

    local jp       = ju:getPoint()
    local tp       = tu:getPoint()
    local dist     = get3DDist(jp, tp)
    local maxRange = CFG_spotMaxRange                                  -- focused mode: flat, altitude-independent
    local fullEff  = CFG_spotFullEff
    local altBoost = math.min((jp.y or 0) / 10000, 0.2)

    if dist <= maxRange and hasLOS(tp, jp) then
        local prob
        if dist <= fullEff then prob = 1.0 else prob = 0.2 + ((fullEff / dist) * 0.8) end
        -- Apply radar-type difficulty, softened — spot jamming punches through ECCM
        local nato = getNatoName(tu)
        prob = prob + altBoost
        local diff = jamDifficulty[nato] or 1.0
        diff = diff + (1.0 - diff) * CFG_spotPunchThrough
        prob = prob * diff
        -- Apply cross-band penalty if pods don't cover this system's frequency
        local bands = loadoutBands[name]
        if bands then
            local isLo = loBandSystems[nato]
            if (isLo and not bands.lo) or (not isLo and not bands.hi) then
                prob = prob * CFG_crossBandPenalty
            end
        end
        prob = math.min(prob, 1.0)
        if math.random() < prob then
            local ctrl = g:getController()
            if ctrl and ctrl.setOption then ctrl:setOption(AI.Option.Ground.id.ROE, AI.Option.Ground.val.ROE.WEAPON_HOLD) end
            local dur = jamDuration[nato] or 60
            suppressedSAMs[tgtGroup] = { sam = tu, lastSuppressed = timer.getTime(), spot = true, duration = dur, nato = nato }
        end
        emitterCapacity[name] = math.max(0, (emitterCapacity[name] or 0) - CFG_spotDrainPerSec)

        -- Coalition broadcast on state change (new target, or suppressed <-> not).
        local nowSupp = suppressedSAMs[tgtGroup] ~= nil
        local st = _spotState[name]
        if st and st.target ~= tgtGroup then
            endSpotBroadcast(name)   -- announce the previous target ended first
            st = nil
        end
        if not st then
            -- Start in the "not suppressed" state so the opening attempt is silent —
            -- the first broadcast a striker gets is the actionable SUPPRESSED call.
            st = { target = tgtGroup, nato = nato, suppressed = false,
                   duration = jamDuration[nato] or 60 }
            _spotState[name] = st
        end
        st.nato = nato
        if nowSupp ~= st.suppressed then
            st.suppressed = nowSupp
            if nowSupp then
                trigger.action.outTextForCoalition(coalition.side.BLUE,
                    string.format("SPOT JAM: %s SUPPRESSED (%s) — clear to engage", nato, bullseyeStr(tp)),
                    (suppressedSAMs[tgtGroup] or {}).duration or 60)
            else
                -- Only reached if a previously suppressed site drops back to active.
                trigger.action.outTextForCoalition(coalition.side.BLUE,
                    string.format("SPOT JAM: %s LIVE again (%s)", nato, bullseyeStr(tp)), st.duration or 60)
            end
        end
    else
        ewSettings[name].spotTarget = nil
        endSpotBroadcast(name)
        emitImmediate(name, "Spot jamming cancelled: out of range/LOS")
    end
end

-- ---------------------------------------------------------------------------
-- ISR helpers
-- ---------------------------------------------------------------------------

local function getDetectionRange(unit)
    if not unit or not unit:isExist() then return 92600 end
    local alt = math.max(0, unit:getPoint().y)
    return math.min(92600 + alt * 20, 370400)
end

local function computeTrackTime(distMeters)
    local frac = math.min(distMeters / 370400, 1.0)
    return CFG_trackMinTime + frac * (CFG_trackMaxTime - CFG_trackMinTime)
end

-- Two-phase confidence.
--   Phase 1 (0 → 85%): linear over timeToFull seconds.
--   Phase 2 (85 → 100%): linear over (timeToFull × CFG_refinementMult) seconds,
--     starting from when phase 1 completed.  Requires track.phase2Start to be set.
local function getConfidence(track)
    local now     = timer.getTime()
    local elapsed = now - track.trackStart
    if elapsed < track.timeToFull then
        return (elapsed / track.timeToFull) * 0.85
    end
    -- Phase 2
    if not track.phase2Start then return 0.85 end
    local p2elapsed = now - track.phase2Start
    local p2total   = track.timeToFull * CFG_refinementMult
    return math.min(0.85 + 0.15 * (p2elapsed / p2total), 1.0)
end

local function confidenceLabel(c)
    if c < 0.25 then return "Initial Contact"
    elseif c < 0.50 then return "Tracking"
    elseif c < 0.85 then return "Refined"
    elseif c < 1.00 then return "ELINT Lock"
    else return "Precise Fix"
    end
end

-- Stop one track by group name.
-- If ELINT Lock was reached the map mark is preserved, otherwise removed.
local function stopTrack(name, gname, msg)
    local tracks = markedTarget[name]; if not tracks then return end
    local track  = tracks[gname];     if not track  then return end
    if track.markID then
        if track.sentLockMsg then
            lockedMarkIDs[name] = lockedMarkIDs[name] or {}
            table.insert(lockedMarkIDs[name], track.markID)
        else
            trigger.action.removeMark(track.markID)
        end
    end
    tracks[gname] = nil
    if msg then emitEvent(name, msg) end
end

local function stopAllTracks(name)
    for gname in pairs(markedTarget[name] or {}) do
        stopTrack(name, gname, nil)
    end
end

-- Scan all known contacts and fill open track slots with the closest untracked emitters.
-- Called each trackingTick when autoTriangulate is ON.
-- Stop the least-important active AUTO track to free a slot for a higher priority
-- target. Prefers bumping a Phase-2 (refining) track, then the farthest non-priority
-- Phase-1 track. Never bumps manual tracks or priority Phase-1 tracks. A bumped
-- Phase-2 target keeps its Phase-1 lock (restored to "locked").
local function bumpAutoTrack(name, jp)
    local best, bestScore = nil, nil
    for gn, tr in pairs(markedTarget[name] or {}) do
        if tr.auto then
            local trPrio = highPriorityThreats[tr.nato] and 1 or 0
            if not (tr.work == "p1" and trPrio == 1) then
                local d = (jp and tr.unit and tr.unit:isExist()) and get3DDist(jp, tr.unit:getPoint()) or math.huge
                local score = (tr.work == "p2" and 1e9 or 0) + d
                if bestScore == nil or score > bestScore then bestScore = score; best = gn end
            end
        end
    end
    if not best then return false end
    local bt = markedTarget[name][best]
    if bt and bt.work == "p2" then
        elintParked[name] = elintParked[name] or {}
        elintParked[name][best] = { stage = "locked", markID = bt.markID }   -- preserve Phase-1 lock + mark
        bt.markID = nil
    end
    stopTrack(name, best, nil)
    return true
end

-- Auto-triangulate strategy:
--   1) Get a Phase-1 lock (~10nm geolocation) on EVERY emitter in range first.
--   2) Only once no Phase-1 work remains, refine parked locks to a precise fix (Phase 2).
--   3) A high-priority SAM (SA-10 etc.) coming online preempts a lower track so it
--      gets worked first.
local function autoTriangulateFill(name)
    local unit = Unit.getByName(name); if not unit or not unit:isExist() then return end
    local jp    = unit:getPoint()
    local range = getDetectionRange(unit)
    local nowT  = timer.getTime()
    local tracked = markedTarget[name] or {}
    elintParked[name] = elintParked[name] or {}
    local parked  = elintParked[name]

    -- Build Phase-1 / Phase-2 work lists from currently known emitters
    local p1, p2, seen = {}, {}, {}
    for gname, info in pairs(knownEmitters[name] or {}) do
        local u = info.unit
        if u and u.isExist and u:isExist() then
            local dist = get3DDist(jp, u:getPoint())
            if dist <= range then
                seen[gname] = true
                if not tracked[gname] then
                    local nato  = info.nato or getNatoName(u)
                    local entry = { gname = gname, unit = u, dist = dist, nato = nato,
                                    prio = highPriorityThreats[nato] and 1 or 0 }
                    local rec   = parked[gname]
                    local stage = rec and rec.stage
                    if     stage == nil      then p1[#p1+1] = entry
                    elseif stage == "locked" then p2[#p2+1] = entry end
                end
            end
        end
    end

    -- Prune parked records for groups that no longer exist
    for gname in pairs(parked) do
        if not seen[gname] then
            local g = Group.getByName(gname)
            if not g or not g:isExist() then parked[gname] = nil end
        end
    end

    local function bySort(a, b)
        if a.prio ~= b.prio then return a.prio > b.prio end
        return a.dist < b.dist
    end
    table.sort(p1, bySort)
    table.sort(p2, bySort)

    local function createTrack(c, work)
        local angle = math.random() * 2 * math.pi
        local tt    = computeTrackTime(c.dist)
        local rec = {
            groupName      = c.gname,
            unit           = c.unit,
            nato           = c.nato,
            timeToFull     = tt,
            offsetX        = math.cos(angle) * (CFG_errorInitialNm * 1852),
            offsetZ        = math.sin(angle) * (CFG_errorInitialNm * 1852),
            markID         = nil,
            lastMarkUpdate = nil,
            auto           = true,
            work           = work,
        }
        if work == "p2" then
            -- resume already at the Phase-1 lock so confidence climbs 85% -> 100%
            local prev = parked[c.gname]
            rec.markID      = prev and prev.markID or nil   -- reuse the Phase-1 mark
            rec.trackStart  = nowT - tt
            rec.phase2Start = nowT
            rec.sentLockMsg = true
        else
            rec.trackStart  = nowT
            rec.sentLockMsg = false
        end
        markedTarget[name] = markedTarget[name] or {}
        markedTarget[name][c.gname] = rec
        parked[c.gname] = nil
    end

    -- Phase 1 first: work every emitter. Priority targets preempt a lower track if full.
    local unplacedP1 = 0
    for _, c in ipairs(p1) do
        if countTracks(name) < CFG_maxTracks then
            createTrack(c, "p1")
            emitISR(name, string.format("AUTO: %s | %s", c.nato, bullseyeStr(c.unit:getPoint())))
        elseif c.prio == 1 and bumpAutoTrack(name, jp) then
            createTrack(c, "p1")
            emitISR(name, string.format("AUTO*: %s | %s", c.nato, bullseyeStr(c.unit:getPoint())))
        else
            unplacedP1 = unplacedP1 + 1
        end
    end

    -- Phase 2 refinement: only with leftover slots once all in-range emitters are Phase-1 locked.
    if unplacedP1 == 0 then
        for _, c in ipairs(p2) do
            if countTracks(name) >= CFG_maxTracks then break end
            createTrack(c, "p2")
            emitISR(name, string.format("REFINE: %s | %s", c.nato, bullseyeStr(c.unit:getPoint())))
        end
    end
end

-- Returns a 0→1 multiplier applied to the initial offset vector stored on the track.
--   Phase 1 (0→85%): error shrinks linearly from CFG_errorInitialNm to CFG_errorPhase1Nm.
--   Phase 2 (85→100%): error shrinks linearly from CFG_errorPhase1Nm to 0.
local function trackDisplayScale(c)
    local p1Ratio = CFG_errorPhase1Nm / CFG_errorInitialNm   -- e.g. 10/50 = 0.20
    if c < 0.85 then
        return 1.0 - (c / 0.85) * (1.0 - p1Ratio)
    else
        return p1Ratio * (1.0 - c) / 0.15
    end
end

local function buildMarkText(natoName, bearing, rangeNm, confidence, displayPos)
    local rErr, bErr
    if confidence < 0.85 then
        local t = confidence / 0.85
        rErr = math.floor(CFG_errorInitialNm  + (CFG_errorPhase1Nm  - CFG_errorInitialNm)  * t)
        bErr = math.floor(CFG_errorInitialBrg + (CFG_errorPhase1Brg - CFG_errorInitialBrg) * t)
    else
        local t = (confidence - 0.85) / 0.15
        rErr = math.floor(CFG_errorPhase1Nm  * (1 - t))
        bErr = math.floor(CFG_errorPhase1Brg * (1 - t))
    end
    local lines = {
        confidenceLabel(confidence) .. ": " .. natoName,
        string.format("Bearing: %d (+/-%d)", bearing, bErr),
        string.format("Range:   ~%dnm (+/-%dnm)", rangeNm, rErr),
        string.format("Confidence: %d%%", math.floor(confidence * 100)),
    }
    if confidence >= 0.85 then lines[#lines+1] = bullseyeStr(displayPos) end
    return table.concat(lines, "\n")
end

local function updateMapMark(name, gname, track)
    if not groupIDs[name] then return end
    local u = track.unit; if not u or not u:isExist() then return end

    local actualPos  = u:getPoint()
    local now        = timer.getTime()

    -- Record phase-2 start the first time elapsed time exceeds timeToFull (85% threshold crossed)
    if not track.phase2Start and (now - track.trackStart) >= track.timeToFull then
        track.phase2Start = now
    end

    local confidence = getConfidence(track)
    local scale      = trackDisplayScale(confidence)
    local displayPos = {
        x = actualPos.x + track.offsetX * scale,
        y = actualPos.y,
        z = actualPos.z + track.offsetZ * scale,
    }

    local unit = Unit.getByName(name); if not unit or not unit:isExist() then return end
    local jp   = unit:getPoint()
    local brg  = getBearing(jp, displayPos)
    local rnm  = math.floor(get3DDist(jp, displayPos) / 1852 + 0.5)
    local nato = getNatoName(u)
    local text = buildMarkText(nato, brg, rnm, confidence, displayPos)

    if track.markID then trigger.action.removeMark(track.markID) end
    local mid = nextMarkID()
    track.markID         = mid
    track.lastMarkUpdate = now
    trigger.action.markToCoalition(mid, text, displayPos, coalition.side.BLUE, true, "")

    -- Phase 1 complete (85%): broadcast ELINT Lock. Track stays alive — players choose
    -- whether to keep refining or stop it manually to free the slot.
    if confidence >= 0.85 and not track.sentLockMsg then
        track.sentLockMsg = true
        trigger.action.outTextForCoalition(coalition.side.BLUE,
            string.format("RIVET ELINT LOCK: %s (~10nm)\n", nato) .. text, 25)
    end

    -- Phase 2 complete (100%): precise fix achieved, auto-release slot.
    if confidence >= 1.0 and not track.sentPreciseFix then
        track.sentPreciseFix = true
        track.locked         = true   -- trackingTick will free this slot
        _preciseFixLog[#_preciseFixLog + 1] = {
            nato        = nato,
            be          = bullseyeStr(displayPos),
            missionTime = timer.getTime(),
        }
        writeISRPreciseFixLog()   -- write immediately; file stays current if server is left
        trigger.action.outTextForCoalition(coalition.side.BLUE,
            string.format("RIVET PRECISE FIX: %s\n", nato) .. text, 25)
    end
end

local function sweepEmitters(name)
    local unit = Unit.getByName(name); if not unit or not unit:isExist() then return end
    local jp    = unit:getPoint()
    local range = getDetectionRange(unit)
    local prev  = knownEmitters[name] or {}
    local now   = {}
    local nowT  = timer.getTime()

    local cats = { Group.Category.GROUND, Group.Category.SHIP }
    for _, cat in ipairs(cats) do
        local groups = coalition.getGroups(coalition.side.RED, cat) or {}
        for _, g in ipairs(groups) do
            if g and g.isExist and g:isExist() then
                for _, u in ipairs(g:getUnits() or {}) do
                    if u and u.isExist and u:isExist() and isImportantRadar(u) then
                        local tp    = u:getPoint()
                        local dist  = get3DDist(jp, tp)
                        if dist <= range then
                            local gname = g:getName()
                            local nato  = getNatoName(u)
                            now[gname]  = { pos = tp, seenAt = nowT, unit = u, nato = nato }

                            if not prev[gname] then
                                -- New contact (routine ISR — muted while jamming)
                                emitISR(name, string.format("CONTACT: %s | %s", nato, bullseyeStr(tp)))
                                -- Threat alert always fires (safety), even while jamming.
                                if highPriorityThreats[nato] then
                                    emitImmediate(name, string.format(
                                        "THREAT: %s | %s", nato, bullseyeStr(tp)))
                                end
                            else
                                -- Existing contact — check for displacement
                                local moveDist = get3DDist(prev[gname].pos, tp)
                                if moveDist > CFG_displacementThreshold then
                                    emitISR(name, string.format("MOVED: %s %.1fnm", nato, moveDist/1852))
                                end
                            end
                        end
                        break
                    end
                end
            end
        end
    end

    for gname, info in pairs(prev) do
        if not now[gname] then
            -- Contact gone — stop any active track on this group (use NATO name, not group name)
            local label = info.nato or gname
            if (markedTarget[name] or {})[gname] then
                stopTrack(name, gname, nil)
                emitISR(name, "TRACK LOST: " .. label)
            else
                emitISR(name, "LOST: " .. label)
            end
        end
    end

    knownEmitters[name] = now
end

local function trackingTick(name)
    local tracks = markedTarget[name]; if not tracks then return end
    local unit   = Unit.getByName(name)
    local now    = timer.getTime()

    -- First pass: update tracks; mark which to release (and how they should be parked)
    local toRelease = {}
    elintParked[name] = elintParked[name] or {}
    for gname, track in pairs(tracks) do
        local u = track.unit
        if not u or not u:isExist() then
            -- destroyed: remove its mark and drop any parked record
            if track.markID then trigger.action.removeMark(track.markID); track.markID = nil end
            elintParked[name][gname] = nil
            toRelease[#toRelease+1] = { gname = gname, msg = "TRACK LOST: " .. (track.nato or "target") .. " destroyed" }
        elseif unit and unit:isExist() and
               get3DDist(unit:getPoint(), u:getPoint()) > getDetectionRange(unit) then
            -- out of range: a refining track keeps its Phase-1 lock (and its mark) for later
            if track.work == "p2" then
                elintParked[name][gname] = { stage = "locked", markID = track.markID }
                track.markID = nil   -- hand the mark to the parked record
            end
            toRelease[#toRelease+1] = { gname = gname, msg = "TRACK LOST: " .. (track.nato or "contact") .. " out of range" }
        else
            if not track.lastMarkUpdate or (now - track.lastMarkUpdate) >= CFG_markRefreshInterval then
                updateMapMark(name, gname, track)
            end
            if track.locked then
                -- Precise fix (100%) — stopTrack preserves the permanent mark; free slot
                elintParked[name][gname] = { stage = "precise" }
                toRelease[#toRelease+1] = { gname = gname, msg = nil }
            elseif track.auto and track.work == "p1" and track.sentLockMsg then
                -- Auto Phase-1 lock reached — park (keep the mark), free slot for next emitter
                elintParked[name][gname] = { stage = "locked", markID = track.markID }
                track.markID = nil   -- hand the mark to the parked record
                toRelease[#toRelease+1] = { gname = gname, msg = nil }
            end
        end
    end

    -- Second pass: release slots (outside the iteration to avoid modifying during pairs()).
    -- Track-lost notices are routine ISR — muted while jamming.
    for _, r in ipairs(toRelease) do
        stopTrack(name, r.gname, nil)
        if r.msg then emitISR(name, r.msg) end
    end

    -- Auto-triangulate: Phase-1-first / Phase-2-later strategy with priority preemption
    if autoTriangulate[name] then
        autoTriangulateFill(name)
    end
end

local function isrStatusBrief(name)
    -- Suppress the ISR status line while jamming; the EW status line is what matters then.
    if ewActive(name) then return end
    local now = timer.getTime()
    if _lastISRStatusTime[name] and (now - _lastISRStatusTime[name]) < CFG_isrStatusInterval then return end
    _lastISRStatusTime[name] = now

    local unit = Unit.getByName(name); if not unit or not unit:isExist() then return end
    local range    = getDetectionRange(unit)
    local contacts = 0
    for _ in pairs(knownEmitters[name] or {}) do contacts = contacts + 1 end
    local nTracks  = countTracks(name)

    -- Build per-track status summary
    local trackParts = {}
    for _, track in pairs(markedTarget[name] or {}) do
        if track.unit and track.unit:isExist() then
            local c    = getConfidence(track)
            local nato = getNatoName(track.unit)
            if c >= 1.0 then
                trackParts[#trackParts+1] = nato .. " PRECISE FIX"
            elseif c >= 0.85 then
                -- Phase 2: show refinement time remaining
                local p2total   = track.timeToFull * CFG_refinementMult
                local p2elapsed = track.phase2Start and (now - track.phase2Start) or 0
                local remaining = math.max(0, p2total - p2elapsed)
                local mins      = math.ceil(remaining / 60)
                trackParts[#trackParts+1] = string.format("%s LOCKED ~%dmin refine", nato, mins)
            else
                -- Phase 1: show time to initial lock
                local remaining = math.max(0, track.timeToFull - (now - track.trackStart))
                local mins      = math.ceil(remaining / 60)
                trackParts[#trackParts+1] = string.format("%s ~%dmin", nato, mins)
            end
        end
    end

    -- Parked-progress counts (Phase-1 locked awaiting refinement, and precise fixes)
    local nLocked, nPrecise = 0, 0
    for _, rec in pairs(elintParked[name] or {}) do
        if rec.stage == "locked" then nLocked = nLocked + 1
        elseif rec.stage == "precise" then nPrecise = nPrecise + 1 end
    end

    local trackSuffix = (#trackParts > 0) and (" [" .. table.concat(trackParts, " | ") .. "]") or ""
    emitISRStatus(name, string.format(
        "ISR | Range: %dnm | Contacts: %d | Working: %d/%d | Locked: %d | Precise: %d%s",
        math.floor(range/1852+0.5), contacts, nTracks, CFG_maxTracks, nLocked, nPrecise, trackSuffix))
end

local function sigintReport(name)
    local unit = Unit.getByName(name)
    local gid  = groupIDs[name]
    if not unit or not unit:isExist() or not gid then return end

    local jp    = unit:getPoint()
    local range = getDetectionRange(unit)
    local lines = { string.format("=== SIGINT REPORT | Det. range: %dnm ===", math.floor(range/1852+0.5)) }

    -- Collect, then sort by threat level (high-priority first), then distance.
    local contacts = {}
    local cats = { Group.Category.GROUND, Group.Category.SHIP }
    for _, cat in ipairs(cats) do
        local groups = coalition.getGroups(coalition.side.RED, cat) or {}
        for _, g in ipairs(groups) do
            local radar = nil
            for _, u in ipairs(g:getUnits() or {}) do
                if u and u.isExist and u:isExist() and isImportantRadar(u) then radar = u; break end
            end
            if radar then
                local tp   = radar:getPoint()
                local dist = get3DDist(jp, tp)
                if dist <= range then
                    local nato = getNatoName(radar)
                    contacts[#contacts+1] = { nato = nato, tp = tp, dist = dist,
                        prio = highPriorityThreats[nato] and 1 or 0 }
                end
            end
        end
    end

    table.sort(contacts, function(a, b)
        if a.prio ~= b.prio then return a.prio > b.prio end
        return a.dist < b.dist
    end)

    for _, c in ipairs(contacts) do
        local flag = (c.prio == 1) and "* " or "  "
        lines[#lines+1] = string.format("%s%-10s %s | %dnm",
            flag, c.nato, bullseyeStr(c.tp), math.floor(c.dist/1852+0.5))
    end

    if #contacts == 0 then lines[#lines+1] = "  No emitters detected in range" end
    lines[#lines+1] = "(* = priority threat)"
    trigger.action.outTextForCoalition(coalition.side.BLUE, table.concat(lines, "\n"), 20)
end

-- ---------------------------------------------------------------------------
-- Crew coordination — EW/ISR handoff brief
-- ---------------------------------------------------------------------------

local function sendHandoffBrief(fromName, toGID)
    local unit = Unit.getByName(fromName)
    if not unit or not unit:isExist() then return end

    local jp    = unit:getPoint()
    local range = getDetectionRange(unit)
    local lines = { "=== C-130J-30 MISSION SYSTEMS HANDOFF BRIEF ===" }

    -- EW status
    if loadoutConfigured[fromName] then
        local modeText, _ = computeModeAndDrainPerSec(fromName)
        local cap    = emitterCapacity[fromName] or 0
        local capMax = maxEmitterCapacity[fromName] or 0
        local capPct = (capMax > 0) and math.floor(cap / capMax * 100 + 0.5) or 0
        lines[#lines+1] = string.format("EW: Pods: %s | Power: %d%% | Mode: %s",
            formatPodsText(fromName), capPct, modeText)
    else
        lines[#lines+1] = "EW: No loadout configured"
    end

    -- SIGINT contacts
    local contacts = {}
    local cats = { Group.Category.GROUND, Group.Category.SHIP }
    for _, cat in ipairs(cats) do
        for _, g in ipairs(coalition.getGroups(coalition.side.RED, cat) or {}) do
            local radar = nil
            for _, u in ipairs(g:getUnits() or {}) do
                if u and u.isExist and u:isExist() and isImportantRadar(u) then radar = u; break end
            end
            if radar and get3DDist(jp, radar:getPoint()) <= range then
                local nato = getNatoName(radar)
                local tp   = radar:getPoint()
                contacts[#contacts+1] = string.format("  %-10s %s | %d | %dnm",
                    nato, bullseyeStr(tp),
                    getBearing(jp, tp), math.floor(get3DDist(jp, tp)/1852+0.5))
            end
        end
    end
    lines[#lines+1] = string.format("SIGINT: %d contact(s)", #contacts)
    for _, c in ipairs(contacts) do lines[#lines+1] = c end

    -- Active tracks
    local nTracks = countTracks(fromName)
    lines[#lines+1] = string.format("Tracks: %d active", nTracks)
    for gname, track in pairs(markedTarget[fromName] or {}) do
        if track.unit and track.unit:isExist() then
            local c  = getConfidence(track)
            local ap = track.unit:getPoint()
            local dp = { x = ap.x + track.offsetX*trackDisplayScale(c), y = ap.y, z = ap.z + track.offsetZ*trackDisplayScale(c) }
            lines[#lines+1] = string.format("  %s [%s %d%%] %s",
                getNatoName(track.unit), confidenceLabel(c),
                math.floor(c*100), bullseyeStr(dp))
        end
    end

    trigger.action.outTextForGroup(toGID, table.concat(lines, "\n"), 30)
    emitEvent(fromName, "Handoff brief sent")
end

-- True only if at least one unit in the group is occupied by a human player.
local function groupHasPlayer(g)
    for _, u in ipairs(g:getUnits() or {}) do
        if u and u.isExist and u:isExist() and u.getPlayerName and u:getPlayerName() then
            return true
        end
    end
    return false
end

local function refreshCoordTargets(name, gid, cmenu)
    if coordCmds[name] then
        for _, cmd in ipairs(coordCmds[name]) do
            if cmd then missionCommands.removeItemForGroup(gid, cmd) end
        end
    end
    coordCmds[name] = {}
    local myGID = groupIDs[name]
    local cats  = { Group.Category.AIRPLANE, Group.Category.HELICOPTER }
    for _, cat in ipairs(cats) do
        for _, g in ipairs(coalition.getGroups(coalition.side.BLUE, cat) or {}) do
            -- Only offer handoff to other PLAYER groups, never AI flights.
            if g and g.isExist and g:isExist() and g:getID() ~= myGID and groupHasPlayer(g) then
                local toGID = g:getID()
                local label = g:getName()
                local cmd = missionCommands.addCommandForGroup(gid, label, cmenu, function()
                    sendHandoffBrief(name, toGID)
                end)
                table.insert(coordCmds[name], cmd)
            end
        end
    end
end

-- ---------------------------------------------------------------------------
-- ISR track emitter menu
-- ---------------------------------------------------------------------------

local function refreshTrackTargets(name, gid, tsMenu)
    if trackCmds[name] then
        for _, cmd in ipairs(trackCmds[name]) do
            if cmd then missionCommands.removeItemForGroup(gid, cmd) end
        end
    end
    trackCmds[name] = {}

    local unit = Unit.getByName(name); if not unit or not unit:isExist() then return end
    local jp    = unit:getPoint()
    local range = getDetectionRange(unit)
    -- Always list untracked in-range emitters. A manual pick at capacity bumps the
    -- farthest auto-track (see click handler) rather than hiding the whole list.

    local cats = { Group.Category.GROUND, Group.Category.SHIP }
    for _, cat in ipairs(cats) do
        local groups = coalition.getGroups(coalition.side.RED, cat) or {}
        for _, g in ipairs(groups) do
            local radar = nil
            for _, u in ipairs(g:getUnits() or {}) do
                if u and u.isExist and u:isExist() and isImportantRadar(u) then radar = u; break end
            end
            if radar then
                local tp    = radar:getPoint()
                local dist  = get3DDist(jp, tp)
                local gname = g:getName()
                if dist <= range and not (markedTarget[name] or {})[gname] then
                    local brg    = getBearing(jp, tp)
                    local distNm = math.floor(dist/1852+0.5)
                    local label  = getNatoName(radar) .. " | " .. brg .. " | " .. distNm .. "nm"
                    local cmd = missionCommands.addCommandForGroup(gid, label, tsMenu, function()
                        if countTracks(name) >= CFG_maxTracks then
                            -- At capacity: bump the least-important auto-track to make room.
                            local u2  = Unit.getByName(name)
                            local jp2 = (u2 and u2:isExist()) and u2:getPoint() or nil
                            if not bumpAutoTrack(name, jp2) then
                                emitImmediate(name, "Track slots full — stop one first"); return
                            end
                        end
                        -- Manual selection overrides any parked auto record for this group
                        if elintParked[name] and elintParked[name][gname] then
                            local pr = elintParked[name][gname]
                            if pr.markID then trigger.action.removeMark(pr.markID) end
                            elintParked[name][gname] = nil
                        end
                        local angle = math.random() * 2 * math.pi
                        local rU = nil
                        for _, u in ipairs(g:getUnits() or {}) do
                            if u and u.isExist and u:isExist() then rU = u; break end
                        end
                        markedTarget[name] = markedTarget[name] or {}
                        markedTarget[name][gname] = {
                            groupName      = gname,
                            unit           = rU,
                            nato           = getNatoName(rU or radar),
                            trackStart     = timer.getTime(),
                            timeToFull     = computeTrackTime(dist),
                            offsetX        = math.cos(angle) * (CFG_errorInitialNm * 1852),
                            offsetZ        = math.sin(angle) * (CFG_errorInitialNm * 1852),
                            markID         = nil,
                            lastMarkUpdate = nil,
                            sentLockMsg    = false,
                            auto           = false,
                            work           = "manual",
                        }
                        local ttf = math.floor(computeTrackTime(dist) / 60 + 0.5)
                        emitImmediate(name, string.format("TRACK: %s ~%dmin", getNatoName(rU or radar), ttf))
                    end)
                    table.insert(trackCmds[name], cmd)
                end
            end
        end
    end
end

local function refreshStopTrackMenu(name, gid, stMenu)
    if stopTrackCmds[name] then
        for _, cmd in ipairs(stopTrackCmds[name]) do
            if cmd then missionCommands.removeItemForGroup(gid, cmd) end
        end
    end
    stopTrackCmds[name] = {}

    for gname, track in pairs(markedTarget[name] or {}) do
        local c    = getConfidence(track)
        local nato = track.nato
            or ((track.unit and track.unit:isExist()) and getNatoName(track.unit))
            or "Unknown"
        local be   = (track.unit and track.unit:isExist()) and bullseyeStr(track.unit:getPoint()) or "?"
        local label = string.format("%s %s [%d%%]", nato, be, math.floor(c*100))
        local g     = gname   -- capture for closure
        local msg   = "Stopped tracking: " .. nato .. " " .. be
        local cmd = missionCommands.addCommandForGroup(gid, label, stMenu, function()
            stopTrack(name, g, msg)
        end)
        table.insert(stopTrackCmds[name], cmd)
    end
end

-- ---------------------------------------------------------------------------
-- EW spot jam target menu
-- ---------------------------------------------------------------------------

local function refreshSpotTargetList(name, gid, tsMenu)
    if spotTargetCmds[name] then
        for _, cmd in ipairs(spotTargetCmds[name]) do
            if cmd then missionCommands.removeItemForGroup(gid, cmd) end
        end
    end
    spotTargetCmds[name] = {}

    local unit = Unit.getByName(name); if not unit or not unit:isExist() then return end
    local jp   = unit:getPoint()

    local cats = { Group.Category.GROUND, Group.Category.SHIP }
    for _, cat in ipairs(cats) do
        local groups = coalition.getGroups(coalition.side.RED, cat) or {}
        for _, g in ipairs(groups) do
            local radar = nil
            for _, u in ipairs(g:getUnits() or {}) do
                if u and u.isExist and u:isExist() and isImportantRadar(u) then radar = u; break end
            end
            if radar then
                local tp   = radar:getPoint()
                local dist = get3DDist(jp, tp)
                if dist <= CFG_spotMaxRange then
                    local brg    = getBearing(jp, tp)
                    local distNm = math.floor(dist/1852+0.5)
                    local label  = getNatoName(radar) .. " | " .. brg .. " | " .. distNm .. "nm"
                    local gname  = g:getName()
                    local cmd = missionCommands.addCommandForGroup(gid, label, tsMenu, function()
                        if overheated[name] and (emitterCapacity[name] or 0) < CFG_overheatResetCap then
                            emitImmediate(name, "Overheat (need >=" .. CFG_overheatResetCap .. ")"); return
                        end
                        ewSettings[name] = ewSettings[name] or {}
                        ewSettings[name].spotTarget = gname
                        emitImmediate(name, "Spot jamming: " .. label)
                    end)
                    table.insert(spotTargetCmds[name], cmd)
                end
            end
        end
    end
end

-- ---------------------------------------------------------------------------
-- Menu building
-- ---------------------------------------------------------------------------

local buildMenusFor  -- forward declaration

local function buildEWPostLoadoutMenus(name, ewRoot, gid)
    local dmenu = missionCommands.addSubMenuForGroup(gid, "Area Defense Jamming", ewRoot)
    missionCommands.addCommandForGroup(gid, "Enable", dmenu, function()
        if overheated[name] and (emitterCapacity[name] or 0) < CFG_overheatResetCap then
            emitImmediate(name, "Overheat (need " .. CFG_overheatResetCap .. ")"); return
        end
        ewSettings[name] = ewSettings[name] or {}; ewSettings[name].defensive = true
        emitImmediate(name, "Area Defense: ON")
    end)
    missionCommands.addCommandForGroup(gid, "Disable", dmenu, function()
        ewSettings[name] = ewSettings[name] or {}; ewSettings[name].defensive = false
        emitImmediate(name, "Area Defense: OFF")
    end)

    local amenu = missionCommands.addSubMenuForGroup(gid, "Area Offense Jamming", ewRoot)
    missionCommands.addCommandForGroup(gid, "Enable", amenu, function()
        if overheated[name] and (emitterCapacity[name] or 0) < CFG_overheatResetCap then
            emitImmediate(name, "Overheat (need " .. CFG_overheatResetCap .. ")"); return
        end
        ewSettings[name] = ewSettings[name] or {}; ewSettings[name].offensive = true
        emitImmediate(name, "Area Offense: ON")
    end)
    missionCommands.addCommandForGroup(gid, "Disable", amenu, function()
        ewSettings[name] = ewSettings[name] or {}; ewSettings[name].offensive = false
        emitImmediate(name, "Area Offense: OFF")
    end)

    for _, mode in ipairs({ "Offense", "Defense" }) do
        local key     = (mode == "Offense") and "offDir" or "defDir"
        local submenu = missionCommands.addSubMenuForGroup(gid, "Directional " .. mode .. " Jamming", ewRoot)
        for _, dir in ipairs({ "front", "left", "right", "rear" }) do
            missionCommands.addCommandForGroup(gid, "Enable " .. dir, submenu, function()
                if overheated[name] and (emitterCapacity[name] or 0) < CFG_overheatResetCap then
                    emitImmediate(name, "Overheat (need " .. CFG_overheatResetCap .. ")"); return
                end
                ewSettings[name] = ewSettings[name] or {}; ewSettings[name][key] = dir
                emitImmediate(name, "Dir " .. mode .. ": " .. dir)
            end)
        end
        missionCommands.addCommandForGroup(gid, "Disable", submenu, function()
            ewSettings[name] = ewSettings[name] or {}; ewSettings[name][key] = nil
            emitImmediate(name, "Dir " .. mode .. ": OFF")
        end)
    end

    local sjMenu = missionCommands.addSubMenuForGroup(gid, "Spot Jamming", ewRoot)
    missionCommands.addCommandForGroup(gid, "Disable", sjMenu, function()
        ewSettings[name] = ewSettings[name] or {}; ewSettings[name].spotTarget = nil
        emitImmediate(name, "Spot: OFF")
    end)
    local tsMenu = missionCommands.addSubMenuForGroup(gid, "Select Target", sjMenu)
    spotTargetMenus[name] = tsMenu

    missionCommands.addCommandForGroup(gid, "Disable All EW Modes", ewRoot, function()
        closeAllEW(name, true); emitImmediate(name, "All EW: OFF")
    end)

    missionCommands.addCommandForGroup(gid, "Power OFF Jammer Pods", ewRoot, function()
        closeAllEW(name, true)
        podEnabled[name] = false
        if ewMenus[name] then missionCommands.removeItemForGroup(gid, ewMenus[name]); ewMenus[name] = nil end
        local stub = missionCommands.addSubMenuForGroup(gid, "EW - Electronic Warfare [OFF]", rootMenus[name])
        ewMenus[name] = stub
        missionCommands.addCommandForGroup(gid, "Power ON Jammer Pods", stub, function()
            if ewMenus[name] then missionCommands.removeItemForGroup(gid, ewMenus[name]); ewMenus[name] = nil end
            podEnabled[name] = true
            local newEW = missionCommands.addSubMenuForGroup(gid, "EW - Electronic Warfare", rootMenus[name])
            ewMenus[name] = newEW
            buildEWPostLoadoutMenus(name, newEW, gid)
            ewStatusBrief(name)
            emitImmediate(name, "Jammer pods: ON")
        end)
    end)
end

local function buildEWLoadoutMenu(name, ewRoot, gid)
    local loadout = missionCommands.addSubMenuForGroup(gid, "Equipment Setup", ewRoot)
    local presets = {
        { label = "Defensive",     cap = 2500, hi = true,  lo = false,
          pods = "3x hi-band",              coverage = "Hi-band (tracking radars, missile spoofing)" },
        { label = "Offensive",     cap = 4500, hi = false, lo = true,
          pods = "2x lo-band",              coverage = "Lo-band (acquisition / search radars)" },
        { label = "Full Spectrum", cap = 5500, hi = true,  lo = true,
          pods = "2x lo-band + 1x hi-band", coverage = "Low-band + Hi-band" },
    }
    for _, p in ipairs(presets) do
        missionCommands.addCommandForGroup(gid, p.label, loadout, function()
            local cap                 = p.cap
            maxEmitterCapacity[name]  = cap
            emitterCapacity[name]     = cap
            overheated[name]          = false
            loadoutConfigured[name]   = true
            selectedLoadoutName[name] = p.label
            loadoutBands[name]        = { hi = p.hi, lo = p.lo }
            podEnabled[name]          = true
            if ewMenus[name] then missionCommands.removeItemForGroup(gid, ewMenus[name]); ewMenus[name] = nil end
            local newEW = missionCommands.addSubMenuForGroup(gid, "EW - Electronic Warfare", rootMenus[name])
            ewMenus[name] = newEW
            buildEWPostLoadoutMenus(name, newEW, gid)
            emitImmediate(name, string.format(
                "EW PODS ONLINE\nLoadout : %s  [%s]\nPower   : 100%%\nCoverage: %s\nStatus  : All modes available",
                p.label, p.pods, p.coverage))
        end)
    end
end

local function buildEWSubMenu(name, root, gid)
    local ewRoot = missionCommands.addSubMenuForGroup(gid, "EW - Electronic Warfare", root)
    ewMenus[name] = ewRoot
    if not loadoutConfigured[name] then
        buildEWLoadoutMenu(name, ewRoot, gid)
    else
        buildEWPostLoadoutMenus(name, ewRoot, gid)
    end
end

local function buildISRSubMenu(name, root, gid)
    local isrRoot = missionCommands.addSubMenuForGroup(gid, "ISR - Intelligence Surveillance Recon", root)
    isrMenus[name] = isrRoot

    missionCommands.addCommandForGroup(gid, "SIGINT Report", isrRoot, function()
        sigintReport(name)
    end)

    local tkMenu = missionCommands.addSubMenuForGroup(gid, "Track Emitter", isrRoot)
    trackMenus[name] = tkMenu

    local stMenu = missionCommands.addSubMenuForGroup(gid, "Stop Track", isrRoot)
    stopTrackMenus[name] = stMenu

    missionCommands.addCommandForGroup(gid, "Stop All Tracks", isrRoot, function()
        stopAllTracks(name)
        emitEvent(name, "All tracks stopped")
    end)

    missionCommands.addCommandForGroup(gid, "Toggle Auto-Triangulate", isrRoot, function()
        autoTriangulate[name] = not autoTriangulate[name]
        local state = autoTriangulate[name] and "ON" or "OFF"
        emitImmediate(name, "Auto-Triangulate: " .. state ..
            (autoTriangulate[name]
                and "\nTracking all contacts closest-first.\nHigh-priority threats tracked instantly.\nSlots freed on ELINT Lock — next target begins automatically."
                or "\nManual track selection only."))
    end)

    missionCommands.addCommandForGroup(gid, "Clear Map Marks", isrRoot, function()
        for _, track in pairs(markedTarget[name] or {}) do
            if track.markID then trigger.action.removeMark(track.markID) end
        end
        for _, rec in pairs(elintParked[name] or {}) do
            if rec.markID then trigger.action.removeMark(rec.markID) end
        end
        for _, mid in ipairs(lockedMarkIDs[name] or {}) do trigger.action.removeMark(mid) end
        lockedMarkIDs[name] = {}
        elintParked[name]   = {}   -- reset ELINT cycle; auto-triangulate will re-work contacts
        emitEvent(name, "Map marks cleared")
    end)
end

local function buildCoordSubMenu(name, root, gid)
    local cRoot = missionCommands.addSubMenuForGroup(gid, "Crew Coordination", root)
    coordMenus[name] = cRoot
    local briefMenu = missionCommands.addSubMenuForGroup(gid, "Send Handoff Brief To", cRoot)
    -- coordCmds populated by refreshCoordTargets each tick
    coordCmds[name] = {}
    -- store briefMenu handle so refresh knows where to add commands
    coordMenus[name .. "_brief"] = briefMenu
end

buildMenusFor = function(name)
    local unit = Unit.getByName(name); if not unit or not unit:isExist() then return end
    local gid  = unit:getGroup():getID()
    local root = missionCommands.addSubMenuForGroup(gid, "C-130J-30 | Mission Systems")
    rootMenus[name] = root
    buildEWSubMenu(name, root, gid)
    buildISRSubMenu(name, root, gid)
    buildCoordSubMenu(name, root, gid)
end

-- ---------------------------------------------------------------------------
-- Registration
-- ---------------------------------------------------------------------------

local function pushUnique(t, v) for i = 1, #t do if t[i] == v then return end end t[#t+1] = v end

local function isEligible(unit)
    if not unit or not unit.isExist or not unit:isExist() then return false end
    if eligibleTypeNames[unit:getTypeName() or ""] then return true end
    local nm = unit:getName() or ""
    return string.find(nm, "Compass Call") or string.find(nm, "Rivet")
end

local function registerUnit(unit)
    if not unit or not unit:isExist() then return end
    local name = unit:getName()
    if not _staticSlots[name] then return end
    local gid  = unit:getGroup():getID()
    if rootMenus[name] and groupIDs[name] == gid then return end
    if rootMenus[name] then
        missionCommands.removeItemForGroup(groupIDs[name], rootMenus[name])
        rootMenus[name] = nil
    end
    pushUnique(unitNames, name)
    groupIDs[name]           = gid
    ewSettings[name]         = {}
    emitterCapacity[name]    = nil
    maxEmitterCapacity[name] = 0
    loadoutConfigured[name]  = false
    overheated[name]         = false
    podEnabled[name]         = true
    knownEmitters[name]      = {}
    markedTarget[name]       = {}
    elintParked[name]        = {}
    lockedMarkIDs[name]      = {}
    autoTriangulate[name]    = true
    buildMenusFor(name)
end

local function unregisterByName(name)
    if not name then return end
    local gid = groupIDs[name]
    if gid and rootMenus[name] then missionCommands.removeItemForGroup(gid, rootMenus[name]) end
    stopAllTracks(name)
    for _, mid in ipairs(lockedMarkIDs[name] or {}) do trigger.action.removeMark(mid) end
    rootMenus[name]                  = nil
    ewMenus[name]                    = nil
    isrMenus[name]                   = nil
    coordMenus[name]                 = nil
    coordMenus[name .. "_brief"]     = nil
    groupIDs[name]                   = nil
    ewSettings[name]                 = nil
    emitterCapacity[name]            = nil
    maxEmitterCapacity[name]         = nil
    loadoutConfigured[name]          = nil
    selectedLoadoutName[name]        = nil
    overheated[name]                 = nil
    podEnabled[name]                 = nil
    spotTargetMenus[name]            = nil
    spotTargetCmds[name]             = nil
    knownEmitters[name]              = nil
    markedTarget[name]               = nil
    elintParked[name]                = nil
    lockedMarkIDs[name]              = nil
    trackMenus[name]                 = nil
    trackCmds[name]                  = nil
    stopTrackMenus[name]             = nil
    stopTrackCmds[name]              = nil
    coordCmds[name]                  = nil
    _lastSweep[name]                 = nil
    _lastEWStatusTime[name]          = nil
    _lastISRStatusTime[name]         = nil
    _lowCapWarned[name]              = nil
    autoTriangulate[name]            = nil
    endSpotBroadcast(name)   -- announce spot-jam end if the crew left mid-engagement
    for i = #unitNames, 1, -1 do if unitNames[i] == name then table.remove(unitNames, i) end end
end

-- ---------------------------------------------------------------------------
-- Main ticks
-- ---------------------------------------------------------------------------

local function ewTick()
    for _, name in ipairs(unitNames) do
        local proceed = loadoutConfigured[name]
            and emitterCapacity[name] ~= nil
            and (maxEmitterCapacity[name] or 0) > 0
            and podEnabled[name] ~= false

        if proceed then
            local cap    = emitterCapacity[name]
            local capMax = maxEmitterCapacity[name] or 0
            local _, drainPerSec = computeModeAndDrainPerSec(name)

            if overheated[name] and cap >= CFG_overheatResetCap then
                overheated[name] = false
                emitEvent(name, "Overheat cleared, EW available")
            end

            local wasCap = cap
            if drainPerSec > 0 and not overheated[name] then
                cap = math.max(0, cap - drainPerSec)
            else
                cap = math.min(capMax, cap + CFG_regenPerSec)
            end

            if wasCap > 0 and drainPerSec > 0 and cap == 0 and not overheated[name] then
                overheated[name] = true
                closeAllEW(name, true)
                emitEvent(name, "OVERHEAT - need >=" .. CFG_overheatResetCap .. " to enable")
            end

            emitterCapacity[name] = cap

            -- Low capacity warning
            local warnThresh = capMax * CFG_lowCapWarnPct
            if cap <= warnThresh and cap > 0 and not overheated[name] then
                if not _lowCapWarned[name] then
                    _lowCapWarned[name] = true
                    emitImmediate(name, string.format(
                        "EW | LOW POWER: %.0f%% — consider reducing modes",
                        (cap / capMax) * 100))
                end
            elseif cap > warnThresh then
                _lowCapWarned[name] = false  -- reset so it fires again next drain cycle
            end

            local s = ewSettings[name] or {}
            if s.spotTarget then spotJammingTick(name) end
            if s.defensive or s.defDir then defensiveLoop(name) end
            if s.offensive or s.offDir then offensiveLoop(name) end
        end
        -- Spot-jam end reconciliation: catches menu Disable, Power OFF, and overheat
        -- (paths that clear spotTarget outside spotJammingTick).
        if _spotState[name] and (ewSettings[name] or {}).spotTarget ~= _spotState[name].target then
            endSpotBroadcast(name)
        end
    end
    purgeDeadMissiles()
    restoreSAMs()
    return timer.getTime() + 1
end

local function isrTick()
    local now = timer.getTime()
    for _, name in ipairs(unitNames) do
        local u = Unit.getByName(name)
        if u and u:isExist() then
            if not _lastSweep[name] or (now - _lastSweep[name]) >= CFG_sweepInterval then
                sweepEmitters(name)
                _lastSweep[name] = now
            end
            trackingTick(name)
        end
    end
    return now + 1
end

local function statusDisplayTick()
    for _, name in ipairs(unitNames) do
        ewStatusBrief(name)
        isrStatusBrief(name)
    end
    return timer.getTime() + 1
end

local function refreshMenusTick()
    for _, name in ipairs(unitNames) do
        local gid = groupIDs[name]
        if gid then
            if spotTargetMenus[name] then
                refreshSpotTargetList(name, gid, spotTargetMenus[name])
            end
            if trackMenus[name] then
                refreshTrackTargets(name, gid, trackMenus[name])
            end
            if stopTrackMenus[name] then
                refreshStopTrackMenu(name, gid, stopTrackMenus[name])
            end
            local briefMenu = coordMenus[name .. "_brief"]
            if briefMenu then
                refreshCoordTargets(name, gid, briefMenu)
            end
        end
    end
    return timer.getTime() + 10
end

timer.scheduleFunction(ewTick,            {}, timer.getTime() + 1)
timer.scheduleFunction(isrTick,           {}, timer.getTime() + 1)
timer.scheduleFunction(statusDisplayTick, {}, timer.getTime() + 1)
timer.scheduleFunction(refreshMenusTick,  {}, timer.getTime() + 10)

-- ---------------------------------------------------------------------------
-- ISR precise-fix export (written to Logs\ on mission end)
-- ---------------------------------------------------------------------------

-- Note: declared local above (forward declaration) so updateMapMark can call it.
writeISRPreciseFixLog = function()
    local count = #_preciseFixLog
    if count == 0 then return end   -- nothing to write yet
    local lines = {
        "C-130J Mission Systems — ISR Precise Fix Log",
        string.rep("=", 48),
        "",
    }
    for i, entry in ipairs(_preciseFixLog) do
        local mins = math.floor(entry.missionTime / 60)
        local secs = math.floor(entry.missionTime % 60)
        lines[#lines + 1] = string.format(
            "%2d.  %-20s  %s  T+%02d:%02d",
            i, entry.nato, entry.be, mins, secs)
    end
    lines[#lines + 1] = ""
    lines[#lines + 1] = string.format("Total precise fixes: %d", count)
    local report = table.concat(lines, "\n")

    -- net.dostring_in runs in the GUI Lua state, which has io + lfs access.
    -- _C130_ISR_log_num is a GUI-side global set once per mission (reset at startup below).
    -- On first call it scans for the next unused _NNN suffix and stores it; all subsequent
    -- calls for this mission reuse that number, overwriting the same file with the latest log.
    -- %%03d in the long-string becomes %03d in the emitted GUI Lua code.
    if net and net.dostring_in then
        net.dostring_in('gui', string.format([[
pcall(function()
    if not _C130_ISR_log_num then
        local base = lfs.writedir().."Logs/C130_ISR_Report"
        local n, f = 1, nil
        repeat
            f = io.open(base.."_"..string.format("%%03d",n)..".txt","r")
            if f then f:close(); n = n+1 end
        until not f
        _C130_ISR_log_num = n
    end
    local f = io.open(lfs.writedir().."Logs/C130_ISR_Report_"..string.format("%%03d",_C130_ISR_log_num)..".txt","w")
    if f then f:write(%q); f:close() end
end)]], report))
    end
end

-- ---------------------------------------------------------------------------
-- Event handler
-- ---------------------------------------------------------------------------

local EventHandler = {}
function EventHandler:onEvent(event)
    if not event then return end

    if event.id == world.event.S_EVENT_SHOT and event.weapon then
        local shooter = event.initiator
        if shooter and shooter.getCoalition and shooter:getCoalition() == coalition.side.RED then
            local desc = event.weapon:getDesc()
            if desc and (desc.guidance == 3 or desc.guidance == 4) then
                local tgt = (Weapon and Weapon.getTarget and Weapon.getTarget(event.weapon))
                         or (event.weapon.getTarget and event.weapon:getTarget()) or nil
                if tgt and tgt.isExist and tgt:isExist() then
                    -- Record the launch vehicle's position so we never spoof (destroy) the
                    -- missile while it is still next to its launcher.
                    local launchPos = (shooter.getPoint and shooter:getPoint()) or event.weapon:getPoint()
                    trackedMissiles[missileUID] = { missile = event.weapon, target = tgt, uid = missileUID, launchPos = launchPos }
                    missileUID = missileUID + 1
                end
            end
        end
        return
    end

    if event.id == world.event.S_EVENT_BIRTH or event.id == world.event.S_EVENT_PLAYER_ENTER_UNIT then
        local u = event.initiator
        if u and u.getPlayerName and u:getPlayerName() and isEligible(u) then
            timer.scheduleFunction(function()
                if u and u:isExist() then registerUnit(u) end
            end, nil, timer.getTime() + 0.1)
        end
        return
    end

    if event.id == world.event.S_EVENT_CRASH    or event.id == world.event.S_EVENT_DEAD
    or event.id == world.event.S_EVENT_EJECTION or event.id == world.event.S_EVENT_PILOT_DEAD
    or event.id == world.event.S_EVENT_PLAYER_LEAVE_UNIT then
        local u = event.initiator
        if u then
            local ok, name = pcall(function() return u:getName() end)
            if ok and name then unregisterByName(name) end
        end
        return
    end

    if event.id == world.event.S_EVENT_MISSION_END then
        writeISRPreciseFixLog()
        return
    end
end

if not _G.C130_Systems_EventHandler_Registered then
    world.addEventHandler(EventHandler)
    _G.C130_Systems_EventHandler_Registered = true
end

-- ---------------------------------------------------------------------------
-- Auto-register & startup
-- ---------------------------------------------------------------------------

local _staticSlots_ready = false
local function recordStaticSlots()
    for _, g in ipairs(coalition.getGroups(coalition.side.BLUE) or {}) do
        if g and g.isExist and g:isExist() then
            for _, u in ipairs(g:getUnits() or {}) do
                if u and u.isExist and u:isExist() and isEligible(u) then
                    _staticSlots[u:getName()] = true
                end
            end
        end
    end
    _staticSlots_ready = true
end
timer.scheduleFunction(function() recordStaticSlots() end, {}, timer.getTime() + 0.1)

-- Reset the GUI-side ISR log file number so this mission gets a fresh _NNN file.
-- (The GUI Lua state can persist across mission loads within the same DCS session.)
if net and net.dostring_in then
    net.dostring_in('gui', '_C130_ISR_log_num = nil')
end

local function autoRegisterAtStart()
    for _, g in ipairs(coalition.getGroups(coalition.side.BLUE) or {}) do
        if g and g.isExist and g:isExist() then
            for _, u in ipairs(g:getUnits() or {}) do
                if u and u.isExist and u:isExist()
                and u.getPlayerName and u:getPlayerName()
                and isEligible(u) then
                    registerUnit(u)
                end
            end
        end
    end
end
timer.scheduleFunction(function() autoRegisterAtStart() end, {}, timer.getTime() + 1)

local function ensureMenus()
    for _, name in ipairs(unitNames) do
        if not rootMenus[name] then
            local u = Unit.getByName(name)
            if u and u:isExist() then buildMenusFor(name) end
        end
    end
    return timer.getTime() + 2
end
timer.scheduleFunction(ensureMenus, {}, timer.getTime() + 2)
