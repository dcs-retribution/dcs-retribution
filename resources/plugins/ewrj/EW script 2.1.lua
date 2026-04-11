-- EW Script 2.03
-- Original script by ESA_Matador
-- Adapted for Retribution with fixes by Drexyl
--
-- DEFENSIVE JAMMING
-- We all know that DCS lacks an Electronic War (EW) enviroment… The ECM, are available only for individual aircraft. But in modern conflicts, since Vietnam, the Jammers, with aircrafts like, F4 Phantom, A6 Intruder, F18 Hornet, or AWACS... have been used to avoid enemy SAMs to shot down aircrafts. 
-- What I did in this Script is to Emulate this EW (not simulate!!!). We need to use a little bit our imagination and to imagine, that some aircraft has Jamming Pods... with chaffs, ECMs or whatever. So i recommend that if you or any of your friends is flying as if he is carrying ECM pods... just put One or Two Mk82-84 to simulate that they are carrying this pod. And AVOID them to use them as weapons... (I would love if someone can model an AN/ANQ pod...

-- To start Jamming just go to F10 radio menú, and select Defensive Jamming On... Take into account that you can also jamm friendly missiles!!!

-- This Defensive Script, creates a bubble with 5 layers (easily increased upon request) surrounding an aircraft called in the function, for instance "EWJamming('Prowler1')". THis will work in the aircraft which pilot´s name is “Prowler1”. What the scripts makes is, to explode the missile if the missile gets close enough  the bubble. But the good point is that the missile will explode with certain probablility, depending on the distance to the Jammer, the closer the missile is to the Jammer, the more difficult, is for the missile to get its target. 
-- So, long story short... whatever missile guided by RADAR (AG or AA) is launched to an aircraft and the missile cross inside the bubble, the missile will be Jammed with a certain probability. It doesn’t matter if the missile is launched to the Jammer or to  another aircraft who is inside its coverage bubble. The closer, the better!!...
-- The layers of the bubble I put is something like this this.... (to modyfy it go to line 320)
-- Layer 1 = 500    probability of succesfull Jamming = 85%
-- Layer 2 = 1000     probability of succesfull Jamming = 65%
-- Layer 3 = 2000     probability of succesfull Jamming = 50%
-- Layer 4 = 4000     probability of succesfull Jamming = 30%
-- Layer 5 = 7000     probability of succesfull Jamming = 15%

-- It gives us plenty of new tactical opportunities and situations to work with. You can fly the Jammer  by,  escorting in a cruise, create a Shield between the SAMs and the aircrafts, or even to Blind enemy SAMs by overflying them really close. 
-- Each one has its adventages and inconvenient.

--You can also use an IA as a ECM carrier or Jammer by using the function, "startDjamming('jammer')"



-- OFFENSIVE 
--So there we go… THis is an awesome script... you  can be the Stand Off Jammer (EA6 or F18G style!!).

-- After the V1.0, which was based in a simple script where, it takes SAMs and switched them off depending on the distances and couple of other factors, i made this V2.0 which is much more advanced and have many other factors. 
--The script can be used with a player (A6 Prowler style) or with an Standoff Jamming with an AWACS or E2/E3 style... with the command "startEWjamm(jammer)"
-- Now it takes into account distances, angles between Jammer and SAMs and Aircraft targeted by SAMs (hereinafter “Target”), jammer altitude, Jammer and Target altitude differences, banking, pitching, and few other factors such as the “dice”.
-- In this script I manage probabilities, and go/no go parameters. For instance, if the bank of the aircraft is too high, it takes into account, if the angle between the SAM and the Jammer... if it is not in the proper position, then, the jammer does not work. Others, such as distances, an altitudes, makes the probability of successful jamming to rise the lower the better... but if differences between Jammer and Target altitudes, the higher the differences, the lowest capacity of Jamming. 
-- Now I ll explain all these factors so you can plan your successful mission taking into account what is best for your mission profile.
-- Another improvement is now, the radar does not Switch off. It just goes to Green Alarm state, it means, it does not fire, but is still working. Therefore, as in real life, you only know if the jamming is working if you are not being shot at!!!!!!.
-- The script start working, when a SAM is TRACKING (not Detecting) a Target... when it does so, the script start doing checks, and if it is succesfull, the radar goes to weapon hold for few seconds, then it goes to weapons free, and if it detects a Target, the checks starts again.
-- So... lets start, you have the instrucctions attached in a PDF document.

-- CONFIGURABLE JAMMING MULTIPLIERS
ewrj_options = {
    -- Offensive jamming vs SAM radars (in check())
    ["OFFENSIVE_POWER"] = 1.6,     -- 1.0 = stock, 1.4 = realistic-strong
    -- Defensive jamming vs incoming missiles (in EWJD)
    ["DEFENSIVE_POWER"] = 1.25,  -- 1.0 = stock, 1.25 = mild buff
    -- NEW: < 1.0 = missile targets get jammed LESS often
    ["MISSILE_JAM_SCALE"] = 0.2,
    -- Enable Debug
    ["DEBUG"] = false,
    -- Enable Offensive Debug
    ["DEBUG_OFFENSIVE"] = false,
    -- Enable Defensive Debug
    ["DEBUG_DEFENSIVE"] = false,
    -- Enable Advanced Debug (Radar Lists)
    ["DEBUG_ADVANCED"] = false
}
-- Offensive jamming vs SAM radars (in check())
--local OFFENSIVE_POWER = 1.6     -- 1.0 = stock, 1.4 = realistic-strong

-- Defensive jamming vs incoming missiles (in EWJD)
--local DEFENSIVE_MISSILE_POWER = 1.25  -- 1.0 = stock, 1.25 = mild buff


------------------------ SOME TRIGONOMETRIC FUNCTIONS AND STUFF
getMag = function(vec) -- from mist
    return (vec.x^2 + vec.y^2 + vec.z^2)^0.5
end
    
get3DDist = function(point1, point2)
    return getMag({x = point1.x - point2.x, y = point1.y - point2.y, z = point1.z - point2.z})
end
            
function smallestAngleDiff( target, source )
   local a = target - source
   
   if (a > 180) then
      a = a - 360
   elseif (a < -180) then
      a = a + 360
   end
   
   return a
end

----------------------------------------------------------
---- Helper: List units in the player’s group (names) ----
----------------------------------------------------------
local function getGroupUnitNames(group)
    local out = {}
    if not group or not group:isExist() then return out end
    local units = group:getUnits() or {}
    for _, u in ipairs(units) do
        if u and u:isExist() then
            table.insert(out, u:getName())
        end
    end
    return out
end

------------------------------------------------------
---- Helper: Pick wingmen from the player’s group ----
------------------------------------------------------
local function getAIWingmenNamesFromPlayerGroup(playerUnitName)
    local pu = Unit.getByName(playerUnitName)
    if not pu or not pu:isExist() then return {} end

    local g = pu:getGroup()
    if not g or not g:isExist() then return {} end

    local names = {}
    for _, u in ipairs(g:getUnits() or {}) do
        if u and u:isExist() then
            -- “player” unit is the one you called createmenu() for
            if u:getName() ~= playerUnitName then
                -- If it has a player name, it’s human; otherwise AI
                local pn = Unit.getPlayerName(u)
                if not pn or pn == "" then
                    table.insert(names, u:getName())
                end
            end
        end
    end

    return names
end

-------------------------------------------
---- Flight-level start/stop functions ----
-------------------------------------------
local function startDefensiveForWingmen(playerUnitName)
    for _, name in ipairs(getAIWingmenNamesFromPlayerGroup(playerUnitName)) do
        startIAdefjamming(name)   -- or startDjamming(name) if that’s what you want
    end
end

local function stopDefensiveForWingmen(playerUnitName)
    for _, name in ipairs(getAIWingmenNamesFromPlayerGroup(playerUnitName)) do
        stopIAdefjamming(name)
    end
end

local function startOffensiveForWingmen(playerUnitName)
    for _, name in ipairs(getAIWingmenNamesFromPlayerGroup(playerUnitName)) do
        startEWjamm(name)
    end
end

local function stopOffensiveForWingmen(playerUnitName)
    for _, name in ipairs(getAIWingmenNamesFromPlayerGroup(playerUnitName)) do
        stopEWjamm(name)
    end
end

------------------------
---- SAM Hesitation ----
------------------------
function samHesitateDelay(conditiondist, isMissileTarget)
    local base = math.random(12,22)
    local power = ewrj_options.OFFENSIVE_POWER or 1.0
    local missilePenalty = isMissileTarget and 2.2 or 1.0
    if not conditiondist then 
        conditiondist = 0
    end
    local rangeBonus = conditiondist > 40.5 and 1.2 or 1.0
    return math.min(base * power * missilePenalty * rangeBonus, 40)
end

-- NEW: SAM commitment delay before firing during a peek
function samCommitDelay(conditiondist, isMissileTarget)
    local base = 0.5          -- base seconds before firing allowed
    local distFactor = math.min(4, conditiondist / 18)
    local missileBonus = isMissileTarget and -1.2 or 0

    return math.max(1.2, base + distFactor + missileBonus)
end

---------------------------- LOOP TO SEE IF A SAM SHOULD BE SHUT OFF DEPENDING ON THE TARGET DETECTED, THE JAMMER AND THE SAM

-- ensure ActiveJammers table exists for multi-jammer support
ActiveJammers = ActiveJammers or {}
-- Track which jammer is actively suppressing each SAM
SamState = SamState or {}
-- Tracks whether a launcher group is currently jammed (used by Defensive EW)
JammedLaunchers = JammedLaunchers or {}  -- [groupName] = { untilT=number, by=string }

local function markLauncherJammedByUnit(unitObj, jammerName, seconds)
    if not unitObj or not unitObj:isExist() then return end
    local g = unitObj:getGroup()
    if not g then return end
    local groupName = g:getName()
    JammedLaunchers[groupName] = {
        untilT = timer.getTime() + (seconds or 10),
        by = jammerName
    }
end

function check(jammer, samunit)
    -- trigger.action.outText(samunit.."Checking",1)
    local now = timer.getTime()
    local state = SamState[samunit]
    if state then
        if state.state == "JAMMED" and now >= state.nextAction then
            samPEEK(samunit)

            local peekDuration = math.random(5,8) -- Original (2,4)

            SamState[samunit] = {
                state = "PEEKING",
                peekUntil = now + peekDuration,
                peekStart = now,
                commitAt = nil
            }
            if ewrj_options.DEBUG_OFFENSIVE then
                env.info("[EW DEBUG - OFFENSIVE] "..samunit.." PEEKING")
            end
            mist.scheduleFunction(check, {jammer, samunit}, timer.getTime() + 0.8)
            return
        end

        if state.state == "PEEKING" then
            if now >= state.peekUntil then
                -- Missed its firing opportunity
                SamState[samunit] = {
                    state = "JAMMED",
                    nextAction = now + math.random(12,20)
                }
                samOFF(samunit)
                if ewrj_options.DEBUG_OFFENSIVE then
                    env.info("[EW DEBUG - OFFENSIVE] "..samunit.." missed peek opportunity — rejammed")
                end
                mist.scheduleFunction(check, {jammer, samunit}, timer.getTime() + 3)
                return
            end
        end

    end
    --- New logic to replace unreliable getRadar() ---
    local UnitObject = Unit.getByName(samunit)
    if (not UnitObject) or (not UnitObject:isExist()) then
        if ewrj_options.DEBUG then
            env.info("[EW DEBUG] check(): SAM unit does not exist: "..tostring(samunit))
        end
        return
    end

    ------------------------------------
    --- Logic of diminishing returns ---
    ------------------------------------
    local activeJammerCount = 0
    for _, active in pairs(ActiveJammers or {}) do
        if active then
            activeJammerCount = activeJammerCount + 1
        end
    end

    -- Soft cap effectiveness
    local jammerScale = 1 / math.max(1, math.sqrt(activeJammerCount))


    local status, target = false, nil
    local controller = UnitObject:getController()
    local detectedTargets = controller and controller:getDetectedTargets() or {}

    for _, tgt in pairs(detectedTargets) do
        if tgt and tgt.object and tgt.object:isExist() then
            status = true
            target = tgt.object
            break
        end
    end
    -- Abort if this jammer is no longer active
    if not ActiveJammers[jammer] then
        return
    end

    --- Start of original script ---
    if target ~= nil then
        -- Use the detected object directly; it may be a Unit OR a Weapon (missile), etc.
        -- local targetobject = target

        local jammerobject = Unit.getByName(jammer)
        if (not jammerobject) or (not jammerobject:isExist()) then
            ActiveJammers[jammer] = nil
            if ewrj_options.DEBUG then
                env.info("[EW DEBUG] check(): jammer missing or destroyed: "..tostring(jammer).." for SAM "..tostring(samunit))
            end
            -- if jammer doesn't exist, only restore SAM if no other jammer active
            local anyActive = false
            for otherJammer, active in pairs(ActiveJammers or {}) do
                if active and otherJammer ~= jammer then
                    if ewrj_options.DEBUG then
                        env.info("[EW DEBUG] check(): other jammer still active ("..tostring(otherJammer)..") - keeping "..tostring(samunit).." suppressed")
                    end
                    anyActive = true
                    break
                end
            end
            if not anyActive then
                if ewrj_options.DEBUG then
                    env.info("[EW DEBUG] check(): no other jammers - restoring "..tostring(samunit))
                end
                mist.scheduleFunction(samON, {samunit}, timer.getTime() + math.random(25,40))
            end
            return
        end

        local targetobject = target

        if not targetobject or not targetobject:isExist() then
            if ewrj_options.DEBUG then
                env.info("[EW DEBUG] check(): target missing or destroyed for SAM "..tostring(samunit))
            end
            mist.scheduleFunction(check, {jammer, samunit}, timer.getTime() + 0.8)
            return
        end

        -- Optional: name only for logging (and may be nil/empty for some objects)
        local targetname = targetobject.getName and targetobject:getName() or "<noname>"
        if ewrj_options.DEBUG then
            env.info("[EW DEBUG] Target Name = ".. tostring(targetname) .." | Sam UNIT = ".. tostring(samunit) .." | Jammer Name = ".. tostring(jammer))
        end
        -- LOS check
        if not isLOS(samunit, jammer) then
            -- LOS broken: only restore if no other jammer
            local anyActive = false
            for otherJammer, active in pairs(ActiveJammers or {}) do
                if active and otherJammer ~= jammer then
                    if ewrj_options.DEBUG then
                        env.info("[EW DEBUG] check(): LOS lost for "..tostring(jammer).." but "..tostring(otherJammer).." still jamming "..tostring(samunit))
                    end
                    anyActive = true
                    break
                end
            end
            if not anyActive then
                if ewrj_options.DEBUG then
                    env.info("[EW DEBUG] check(): LOS lost and no other jammers - restoring "..tostring(samunit))
                end
                mist.scheduleFunction(samON, {samunit}, timer.getTime() + math.random(25,40))
            end
            return
        end

        local isMissileTarget = false
        if Object.getCategory(targetobject) == Object.Category.WEAPON then
            isMissileTarget = true
        end

        if isMissileTarget then
            -- Only allow a peek attempt ~30% of the time
            if math.random() > 0.3 then
                mist.scheduleFunction(check, {jammer, samunit}, timer.getTime() + 5)
                return
            end
        end

        ------------------------------------------------------------------------
        -- distance/angle/probability logic (now guarded against nils)
        ------------------------------------------------------------------------

        -- compute distances safely
        local distSamJammer = nil
        local distSamTarget = nil

        if UnitObject and jammerobject then
            local p1 = UnitObject:getPoint()
            local p2 = jammerobject:getPoint()
            if p1 and p2 then
                distSamJammer = get3DDist(p1, p2)
            end
        end

        if UnitObject and targetobject then
            local p1 = UnitObject:getPoint()
            local p3 = targetobject:getPoint()
            if p1 and p3 then
                distSamTarget = get3DDist(p1, p3)
            end
        end

        if not distSamJammer or not distSamTarget or distSamJammer == 0 then
            if ewrj_options.DEBUG then
                env.info("[EW DEBUG] check(): invalid distances for SAM "..tostring(samunit).." (distSamJammer="..tostring(distSamJammer)..", distSamTarget="..tostring(distSamTarget)..")")
            end
            mist.scheduleFunction(check, {jammer, samunit}, timer.getTime() + 5)
            return
        end

        local dice = math.random(0,100)
        -- reduced multiplier: stronger jamming at longer ranges
        -- local conditiondist = 50 * distSamTarget / distSamJammer
        local rawCondition = 50 * distSamJammer / distSamTarget
        local conditiondist = math.min(rawCondition, 60)

        -- Arm commit timer once geometry is known
        if SamState[samunit]
           and SamState[samunit].state == "PEEKING"
           and not SamState[samunit].commitAt
        then
            SamState[samunit].commitAt = now + samCommitDelay(conditiondist, isMissileTarget)
            if ewrj_options.DEBUG_OFFENSIVE then
                env.info(string.format(
                    "[EW DEBUG - OFFENSIVE] %s peeking — commit in %.1fs",
                    samunit,
                    SamState[samunit].commitAt - now
                ))
            end
        end

        if SamState[samunit]
           and SamState[samunit].state == "PEEKING"
           and SamState[samunit].commitAt
           and now >= SamState[samunit].commitAt
           and not SamState[samunit].committed
        then
            SamState[samunit].committed = true
            samON(samunit)
            if ewrj_options.DEBUG_OFFENSIVE then
                env.info("[EW DEBUG - OFFENSIVE] "..samunit.." committed — firing allowed")
            end
        end

        -- HEIGHT OF JAMMER
        local Position_vec3 = jammerobject:getPoint()
        local _elevation = land.getHeight({x = Position_vec3.x, y = Position_vec3.z})
        local _height = Position_vec3.y - _elevation    

        local tPosition_vec3 = targetobject:getPoint()
        local t_elevation = land.getHeight({x = tPosition_vec3.x, y = tPosition_vec3.z})
        local t_height = tPosition_vec3.y - t_elevation    
        local prob = dice + _height/5000 + (_height - t_height)/5000
        -- prob = prob * jammerScale

--        if isMissileTarget
--           and SamState[samunit]
--           and SamState[samunit].state == "PEEKING"
--        then end

        if isMissileTarget then
            local missilePenalty = math.max(0.5, conditiondist / 20)
            prob = prob * missilePenalty
        end

        -- BLOCK FIRING UNTIL COMMIT TIMER EXPIRES
        if SamState[samunit]
           and SamState[samunit].state == "PEEKING"
           and SamState[samunit].commitAt
           and now < SamState[samunit].commitAt
        then
            -- samOFF(samunit)
            if ewrj_options.DEBUG_OFFENSIVE then
                env.info("[EW DEBUG - OFFENSIVE] "..samunit.." peeking — not yet committed to fire")
            end
            mist.scheduleFunction(check, {jammer, samunit}, timer.getTime() + 0.8)
            return
        end

        -- FIX 5: missile-target peeking tuning + desperation fire
        if isMissileTarget
           and SamState[samunit]
           and SamState[samunit].state == "PEEKING"
        then
            -- Make jamming more effective vs missile peeks
            -- prob = prob + 25

            local missilePenalty = math.max(0.5, conditiondist / 20)
            prob = prob * missilePenalty

            -- Only 20% of peeks even attempt a shot
            if math.random() > 0.2 then
                SamState[samunit] = {
                    state = "JAMMED",
                    nextAction = now + samHesitateDelay(conditiondist, true)
                }

                samOFF(samunit)
                if ewrj_options.DEBUG_OFFENSIVE then
                    env.info("[EW DEBUG - OFFENSIVE] "..samunit.." panic-peek vs missile — no fire")
                end
                mist.scheduleFunction(check, {jammer, samunit}, timer.getTime() + 5)
                return
            end

            -- Of those, only 10% escalate to actual OPEN_FIRE
            if math.random() < 0.1 then
                if ewrj_options.DEBUG_OFFENSIVE then
                    env.info("[EW DEBUG - OFFENSIVE] "..samunit.." DESPERATION FIRE during peek")
                end
                samON(samunit)
            end
        end

        -------------------------
        ---- LOBE Parameters ----
        -------------------------
        local SamPos = mist.utils.makeVec2(UnitObject:getPosition().p) -- tenemos un vector x e y
        local JammerPos = mist.utils.makeVec2(jammerobject:getPosition().p)        
        local TargetPos = mist.utils.makeVec2(targetobject:getPosition().p)    
        local AngleSamJammer = mist.utils.toDegree(mist.utils.getDir(mist.vec.sub(mist.utils.makeVec3GL(JammerPos),mist.utils.makeVec3GL(SamPos))))
        local AngleSamTarget = mist.utils.toDegree(mist.utils.getDir(mist.vec.sub(mist.utils.makeVec3GL(TargetPos),mist.utils.makeVec3GL(SamPos))))    
        local offsetJamTar = smallestAngleDiff(AngleSamJammer, AngleSamTarget )
        local offsetJamSam = smallestAngleDiff(AngleSamJammer, 180 )
        local TargetandOffsetJamSam = smallestAngleDiff(AngleSamTarget, offsetJamSam )*2
        if TargetandOffsetJamSam < 0 then
            TargetandOffsetJamSam = -TargetandOffsetJamSam
        end

        local anglecondition = 0 -- Decouple Angle gating from distance.

        --    PITCH and BANK
        local bankr = mist.utils.toDegree(mist.getRoll(jammerobject))
        if bankr < 0 then
            bankr = -bankr
        end
        local bank = bankr - 15

        local pitchr = mist.utils.toDegree(mist.getPitch(jammerobject))
        if pitchr < 0 then
            pitchr = -pitchr
        end
        local pitch = pitchr - 15

        local sPosition_vec3 = UnitObject:getPoint()
        local s_elevation = land.getHeight({x = sPosition_vec3.x, y = sPosition_vec3.z})
        local s_height = sPosition_vec3.y - s_elevation    

        local cateto = _height - s_height
        local samunitposition = UnitObject:getPosition().p
        local jammerposition = jammerobject:getPosition().p
        local _2DDistSamJammer = mist.utils.get2DDist(samunitposition, jammerposition)

        local anglesamjam = 0
        if _2DDistSamJammer ~= 0 then
            local ratio = cateto/_2DDistSamJammer
            if ratio > 1 then ratio = 1 end
            if ratio < -1 then ratio = -1 end
            anglesamjam = mist.utils.toDegree(math.asin(ratio))
        end

        ------------------------------------------------------------------------
        -- scaled by OFFENSIVE_POWER for stronger offensive jamming
        ------------------------------------------------------------------------
        local offensivePower = ewrj_options.OFFENSIVE_POWER or 1.0
        -- Missile Specific Jamming Scale
        if isMissileTarget then
            offensivePower = offensivePower * (ewrj_options.MISSILE_JAM_SCALE or 0.6)
        end

        local probsector1 = offensivePower * (110 - (2.5 * conditiondist))
        local probsector2 = offensivePower * (95  - (1.5 * conditiondist))
        local probsector3 = offensivePower * (80  - (0.8 * conditiondist))

        -- Diminishing returns for multiple jammers
        local jammerScale = 1 / math.max(1, math.sqrt(activeJammerCount))

        probsector1 = probsector1 * jammerScale
        probsector2 = probsector2 * jammerScale
        probsector3 = probsector3 * jammerScale
        ------------------------------------------------------------------------
        -- Apply jamming decision
        ------------------------------------------------------------------------
        if (conditiondist > 40.5)
            and (prob <= probsector3) 
            and (anglecondition < TargetandOffsetJamSam)
            and anglesamjam >= bank 
            and anglesamjam > pitch
        then
            SamState[samunit] = nil -- <<< NEW: cancel PEEKING immediately
            samOFF(samunit)
            -- mark this SAM launcher as jammed for defensive logic
            markLauncherJammedByUnit(UnitObject, jammer, 10)
            SamState[samunit] = {
                state = "JAMMED",
                nextAction = now + math.random(15,30)
            }
            if ewrj_options.DEBUG_OFFENSIVE then
                env.info("[EW DEBUG - OFFENSIVE] "..samunit.." JAMMED by: "..jammer.." Target: "..targetname)
            end
            mist.scheduleFunction(check, {jammer, samunit}, timer.getTime() + 5)

        elseif ((conditiondist < 40.5) and (conditiondist > 13.33)) 
            and (prob <= probsector2) 
            and (anglecondition < TargetandOffsetJamSam)
            and anglesamjam >= bank 
            and anglesamjam > pitch                                                 
        then
            SamState[samunit] = nil -- <<< NEW: cancel PEEKING immediately
            samOFF(samunit)
            -- mark this SAM launcher as jammed for defensive logic
            markLauncherJammedByUnit(UnitObject, jammer, 10)
            SamState[samunit] = {
                state = "JAMMED",
                nextAction = now + samHesitateDelay(conditiondist, isMissileTarget)
            }
            if ewrj_options.DEBUG_OFFENSIVE then
                env.info("[EW DEBUG - OFFENSIVE] "..samunit.." JAMMED (mid)")
            end
            mist.scheduleFunction(check, {jammer, samunit}, timer.getTime() + 5)
        elseif (conditiondist < 13.33) 
            and (prob <= probsector1)
            and (anglecondition < TargetandOffsetJamSam)
            and anglesamjam >= bank 
            and anglesamjam > pitch
        then
            SamState[samunit] = nil -- <<< NEW: cancel PEEKING immediately
            samOFF(samunit)
            -- mark this SAM launcher as jammed for defensive logic
            markLauncherJammedByUnit(UnitObject, jammer, 10)
            SamState[samunit] = {
                state = "JAMMED",
                nextAction = now + samHesitateDelay(conditiondist, isMissileTarget)
            }
            if ewrj_options.DEBUG_OFFENSIVE then
                env.info("[EW DEBUG - OFFENSIVE] "..samunit.." JAMMED (close)")
            end
            mist.scheduleFunction(check, {jammer, samunit}, timer.getTime() + 5)
        else
            mist.scheduleFunction(check, {jammer, samunit}, timer.getTime() + 5)
        end

    else
        -- no target: keep polling so jamming can resume when target reappears
        mist.scheduleFunction(check, {jammer, samunit}, timer.getTime() + 5)
        return
    end
end

------------------------------------------------------------
---- SAM ON/OFF/PEEK. IT CHANGES THE RULE OF ENGAGEMENT ----
------------------------------------------------------------

function samON(groupsam)

    -- local samName = groupsam
    local unitObj = Unit.getByName(groupsam)
    if not unitObj or not Unit.isExist(unitObj) then
        -- Unit missing (dead or wrong name) — avoid nil indexing
        if ewrj_options.DEBUG_OFFENSIVE then
            env.info("[EW DEBUG - OFFENSIVE] samON() - Unit not found or destroyed: " .. tostring(groupsam))
        end
        return
    end

    local _group = unitObj:getGroup()
    if not _group then
        if ewrj_options.DEBUG_OFFENSIVE then
            env.info("[EW DEBUG - OFFENSIVE] samON() - Group not found for unit: " .. tostring(groupsam))
        end
        return
    end

    local _controller = _group:getController()
    if not _controller then
        if ewrj_options.DEBUG_OFFENSIVE then
            env.info("[EW DEBUG - OFFENSIVE] samON() - Controller missing for group of: " .. tostring(groupsam))
        end
        return
    end

    _controller:setOption(AI.Option.Ground.id.ROE,     AI.Option.Ground.val.ROE.OPEN_FIRE)
    if ewrj_options.DEBUG then
        trigger.action.outText(groupsam.." SAM SWITCHING ON", 5)
        env.info("[EW DEBUG] SAM has switched ON: " .. groupsam)
    end
end

function samOFF(groupsam)
    local unitObj = Unit.getByName(groupsam)
    if not unitObj or not Unit.isExist(unitObj) then
        if ewrj_options.DEBUG_OFFENSIVE then
            env.info("[EW DEBUG - OFFENSIVE] samOFF() - Unit not found or destroyed: " .. tostring(groupsam))
        end
        return
    end

    local _group = unitObj:getGroup()
    if not _group then
        if ewrj_options.DEBUG_OFFENSIVE then
            env.info("[EW DEBUG - OFFENSIVE] samOFF() - Group not found for unit: " .. tostring(groupsam))
        end
        return
    end

    local _controller = _group:getController()
    if not _controller then
        if ewrj_options.DEBUG_OFFENSIVE then
            env.info("[EW DEBUG - OFFENSIVE] samOFF() - Controller missing for group of: " .. tostring(groupsam))
        end
        return
    end

    _controller:setOption(AI.Option.Ground.id.ROE, AI.Option.Ground.val.ROE.WEAPON_HOLD)
    if ewrj_options.DEBUG then
        trigger.action.outText(groupsam.." SAM SWITCHING OFF", 5)
        env.info("[EW DEBUG] SAM has switched OFF: " .. groupsam)
    end
    -- mist.scheduleFunction(samON, {groupsam}, timer.getTime()+ math.random(25,40))
end

function samPEEK(groupsam)
    local unitObj = Unit.getByName(groupsam)
    if not unitObj or not Unit.isExist(unitObj) then return end

    local group = unitObj:getGroup()
    if not group then return end

    local controller = group:getController()
    if not controller then return end

    controller:setOption(
        AI.Option.Ground.id.ROE,
        AI.Option.Ground.val.ROE.RETURN_FIRE
    )
    if ewrj_options.DEBUG then
        trigger.action.outText(groupsam.." SAM is PEEKING (Return Fire)", 5)
        env.info("[EW DEBUG] "..groupsam.." radar PEEK (RETURN_FIRE)")
    end
end

--------------------------
---- LOS Calculations ----
--------------------------
function isLOS(sam,radar) --- check if sam is LOS with Jammer
        local samUnit = Unit.getByName(sam)
        local radarUnit = Unit.getByName(radar)

        if not samUnit or not radarUnit then
            return false
        end

        if not Unit.isExist(samUnit) or not Unit.isExist(radarUnit) then
            return false
        end

        local moverPos = samUnit:getPosition()
        local radarPos = radarUnit:getPosition()

        if not moverPos or not radarPos then
            return false
        end

        local mover = moverPos.p
        local target = radarPos.p

        if not mover or not target then
            return false
        end

        mover.y = mover.y + 3
        target.y = target.y + 1.8

        return land.isVisible(mover, target)
end 

------------------------------------------------------------
---- Get list of Radars available for Offensive Jamming ----
------------------------------------------------------------
radarList = {}

function getRadars()
    local redUnits = mist.makeUnitTable({'[red][vehicle]','[blue][vehicle]','[red][ship]','[blue][ship]'})
        if ewrj_options.DEBUG_ADVANCED then
            trigger.action.outText(mist.utils.tableShow(redUnits),15)
        end
        for i, unitName in pairs (redUnits) do
        if type(i) == "number" then  -- makeUnitTable also has a ["processed"] = time index which does not represent a unit
        local samUnit = Unit.getByName(unitName)

            if samUnit and Unit.isExist(samUnit) then
                if samUnit:hasSensors(Unit.SensorType.RADAR, Unit.RadarType.AS)
                    or samUnit:hasAttribute("SAM SR")
                    or samUnit:hasAttribute("EWR")
                    or samUnit:hasAttribute("SAM TR")
                    or samUnit:hasAttribute("Armed ships")
                then
                    table.insert(radarList, unitName)
                end
            end        -- end
        end
    end
end

getRadars()

---------------------------------
---- START OFFENSIVE JAMMING ----
--------------------------------- 
function startEWjamm(jammer)
    trigger.action.outText("OFFENSIVE COUNTER MEASURES POD ON "..jammer, 5)
    if ewrj_options.DEBUG then
        env.info("[EW DEBUG] Start Offensive Jamming: " .. jammer)
    end

    ActiveJammers[jammer] = true -- mark jammer active for multi-jammer logic

    -- Clean radar list and process live units only
    local validRadarList = {}
    for k, radarName in pairs(radarList) do
        local radarUnit = Unit.getByName(radarName)
        if radarUnit and Unit.isExist(radarUnit) then
            table.insert(validRadarList, radarName)
        else
            if ewrj_options.DEBUG then
                env.info("[DEBUG EW] Removing destroyed or missing radar: " .. tostring(radarName))
            end
        end
        if ewrj_options.DEBUG_ADVANCED then
            env.info("--- RADAR LIST ---")
            env.info(radarList[k])
        end
    end
    radarList = validRadarList  -- update the global list safely
    if ewrj_options.DEBUG_ADVANCED then
        trigger.action.outText(mist.utils.tableShow(radarList),20)
    end

    --------------------------------------
    ---- Remaining valid radar checks ----
    --------------------------------------
    for _, radarName in pairs(radarList) do
        local radarUnit = Unit.getByName(radarName)
        local jammerUnit = Unit.getByName(jammer)

        if radarUnit and jammerUnit and radarUnit:isExist() and jammerUnit:isExist() then
            if radarUnit:getCoalition() ~= jammerUnit:getCoalition() then
                check(jammer, radarName)
                if ewrj_options.DEBUG_OFFENSIVE then
                    env.info("[EW DEBUG - OFFENSIVE] Checking radar: " .. radarName)
                end
            end
        else
            if not radarUnit or not radarUnit:isExist() then
                if ewrj_options.DEBUG_OFFENSIVE then
                    env.info("[EW DEBUG - OFFENSIVE] Skipping destroyed radar: " .. tostring(radarName))
                end
            elseif not jammerUnit or not jammerUnit:isExist() then
                if ewrj_options.DEBUG_OFFENSIVE then
                    env.info("[EW DEBUG - OFFENSIVE] Jammer destroyed or missing: " .. tostring(jammer))
                end
                return  -- stop processing if jammer gone
            end
        end
    end
end -- startEWjamm('Prowler1')

--------------------------------
---- STOP OFFENSIVE JAMMING ----
--------------------------------
function stopEWjamm(jammer)
    ActiveJammers[jammer] = nil
    trigger.action.outText("OFFENSIVE COUNTER MEASURES POD OFF "..jammer,5)
    if ewrj_options.DEBUG then
        env.info("[EW DEBUG] Stop Offensive Jamming: " .. jammer)
    end

    -- Check if *any* other jammer is still active
    local anyActive = false
    for otherJammer, active in pairs(ActiveJammers) do
        if active and otherJammer ~= jammer then
            if ewrj_options.DEBUG_OFFENSIVE then
                env.info("[EW DEBUG - OFFENSIVE] stopEWjamm(): "..jammer.." stopped, but "..otherJammer.." still active")
            end
            anyActive = true
            break
        end
    end

    -- Only restore SAMs if no other jammer exists
    if not anyActive then
        if ewrj_options.DEBUG_OFFENSIVE then
            env.info("[EW DEBUG - OFFENSIVE] stopEWjamm(): No jammers left, restoring all SAMs")
        end
        for _, samName in pairs(radarList) do
            local samUnit = Unit.getByName(samName)
            if samUnit and samUnit:isExist() then
                mist.scheduleFunction(samON, {samName}, timer.getTime()+ math.random(5,15))
            end
        end
    else
        if ewrj_options.DEBUG_OFFENSIVE then
            env.info("[EW DEBUG - OFFENSIVE] stopEWjamm(): SAMs remain suppressed due to other active jammers")
        end
    end
end

switch = {}
function EWJscript(jammer)
EWJD(jammer)
end

-------------------------------------------------------
---- ORIGINAL MENU CREATION FOR START/STOP JAMMING ----
-------------------------------------------------------
--function createmenu(jammer)
--if Unit.getByName(jammer) ~= nil then
--local _groupID =  Unit.getByName(jammer):getGroup():getID()
--
--local _jammermenu = missionCommands.addSubMenuForGroup(_groupID,"Jammer menu", nil)
--local _jammermenudef = missionCommands.addSubMenuForGroup(_groupID,"Defensive Jamming", _jammermenu)
--local _jammermenuoff = missionCommands.addSubMenuForGroup(_groupID,"Offensive Jamming", _jammermenu)
--
--missionCommands.addCommandForGroup(_groupID, "Start Defensive Jamming ",_jammermenudef, function () startDjamming(jammer)end, nil)
--missionCommands.addCommandForGroup(_groupID, "Stop Defensive Jamming ",_jammermenudef, function () stopDjamming(jammer)end, nil)
--missionCommands.addCommandForGroup(_groupID, "Start Offensive Jamming ",_jammermenuoff, function ()  startEWjamm(jammer)end, nil)
--missionCommands.addCommandForGroup(_groupID, "Stop Offensive Jamming ",_jammermenuoff, function () stopEWjamm(jammer)end, nil)
--end
--end
-------------------------------------------------------

--------------------------------------------
---- Retribution Specific Menu Creation ----
--------------------------------------------

-- Track created menus per GROUP so we can delete/rebuild on reconnect
JammerMenus = JammerMenus or {}   -- [groupId] = rootMenuHandle

function createmenu(jammer)
     local u = Unit.getByName(jammer)
     if not u or not u:isExist() then return end
 
     local group = u:getGroup()
     if not group then return end
     local _groupID = group:getID()
 
     local ecmFlag = trigger.misc.getUserFlag("offensive_jamming_" .. jammer)
 
    -- If this group already has a jammer menu (e.g. reconnect), remove it first
    if JammerMenus[_groupID] then
        missionCommands.removeItemForGroup(_groupID, JammerMenus[_groupID])
        JammerMenus[_groupID] = nil
    end

    local _jammermenu = missionCommands.addSubMenuForGroup(_groupID, "Jammer menu", nil)
    JammerMenus[_groupID] = _jammermenu

    -- Defensive submenu
    local _jammermenudef = missionCommands.addSubMenuForGroup(_groupID, "Defensive Jamming", _jammermenu)

    -- Self
    missionCommands.addCommandForGroup(_groupID, "Start Defensive (Self)", _jammermenudef, function()
        startIAdefjamming(jammer)    -- or startDjamming(jammer)
    end)

    missionCommands.addCommandForGroup(_groupID, "Stop Defensive (Self)", _jammermenudef, function()
        stopIAdefjamming(jammer)
    end)

    -- Flight (AI wingmen)
    missionCommands.addCommandForGroup(_groupID, "Start Defensive (Flight)", _jammermenudef, function()
        startDefensiveForWingmen(jammer)
    end)

    missionCommands.addCommandForGroup(_groupID, "Stop Defensive (Flight)", _jammermenudef, function()
        stopDefensiveForWingmen(jammer)
    end)

    -- Offensive submenu (only if flag)
    if ecmFlag == 1 then
        local _jammermenuoff = missionCommands.addSubMenuForGroup(_groupID, "Offensive Jamming", _jammermenu)

        -- Self
        missionCommands.addCommandForGroup(_groupID, "Start Offensive (Self)", _jammermenuoff, function()
            startEWjamm(jammer)
        end)

        missionCommands.addCommandForGroup(_groupID, "Stop Offensive (Self)", _jammermenuoff, function()
            stopEWjamm(jammer)
        end)

        -- Flight (AI wingmen)
        missionCommands.addCommandForGroup(_groupID, "Start Offensive (Flight)", _jammermenuoff, function()
            startOffensiveForWingmen(jammer)
        end)

        missionCommands.addCommandForGroup(_groupID, "Stop Offensive (Flight)", _jammermenuoff, function()
            stopOffensiveForWingmen(jammer)
        end)
    end
end

---------------------------------
---- START DEFENSIVE JAMMING ----
---------------------------------
    function startIAdefjamming(jammer)
        startDjamming(jammer)
        EWJD(jammer)
    end
    function startDjamming(jammer)
        switch[#switch+1]=jammer
        trigger.action.outText("DEFENSIVE COUNTER MEASURES POD ON "..jammer,5)
        if ewrj_options.DEBUG then
            env.info("[EW DEBUG] Start Defensive Jamming: " ..jammer)
        end
    end

--------------------------------
---- STOP DEFENSIVE JAMMING ----
--------------------------------
    function stopIAdefjamming(jammer)
        for i, v in pairs (switch) do
        if switch[i]==jammer then
            switch[i] = nil
        end
    end
    trigger.action.outText("DEFENSIVE COUNTER MEASURES POD OFF "..jammer,5)
    if ewrj_options.DEBUG then
        env.info("[EW DEBUG] Stop Defensive Jamming: " ..jammer)    
    end
end

---------------------------------
---- Defensive Jamming Logic ----
---------------------------------
-- FUNCTION THAT EVALUATES THE DISTANCE OF THE MISSILE TO THE TARGET... YOU CAN EVEN DEFEND CLOSER AIRCRAFTS. BASED ON TRAINING MISSILES FROM GRIMES
function EWJD(jammer)

    local function guidanceName(g)
        if g == 3 then return "SARH"
        elseif g == 4 then return "ARH"
        else return tostring(g)
        end
    end
    -- DISTANCES AND PROBABILITIES OF JAMM THE MISSILE FOR DEFENSIVE JAMMING REMOVALDIST1 CORRESPOND TO PKILL1, REMOVALDIST2 CORRESPOND TO PKILL2, ETC...
    local removalDist1 = 500
    local removalDist2 = 1500
    local removalDist3 = 3000
    local removalDist4 = 5000
    local removalDist5 = 7000
    -- PROBAILITY OF SUCCESFULL JAMMING  REMOVALDIST1 CORRESPOND TO PKILL1, REMOVALDIST2 CORRESPOND TO PKILL2, ETC...
    local pkill_1 =95
    local pkill_2 =65
    local pkill_3 =50
    local pkill_4 =30
    local pkill_5 =15

    -- Scale Defensive missile pkill by DEFENSIVE_POWER (capped at 100)
    local function scale_pkill(base)
        local v = base * ewrj_options.DEFENSIVE_POWER
        if v > 100 then v = 100 end
        return v
    end

    pkill_1 = scale_pkill(pkill_1)
    pkill_2 = scale_pkill(pkill_2)
    pkill_3 = scale_pkill(pkill_3)
    pkill_4 = scale_pkill(pkill_4)
    pkill_5 = scale_pkill(pkill_5)

    local remove_missile_method = 0
    -- 0 will create an explosion
    -- 1 will use Object.destroy() which simply makes the missile disappear.
    
    local aiMissiles = {}
    local numActive = 0
    local uid = 1
    local idNum = 1
    local function simpleEvent(f) -- from mist
        local handler = {}
        idNum = idNum + 1
        handler.id = idNum
        handler.f = f
        handler.onEvent = function(self, event)
            self.f(event)
        end
        world.addEventHandler(handler)
    end
    
    ---------------------------------
    ---- Remove Missile Function ----
    ---------------------------------
    local function removeMis(id)
        local rec = aiMissiles[id]
        if not rec then return end

        local missile = rec.missile
        local origTarg = rec.origTarg

        -- missile might already be gone
        if missile and missile:isExist() then

            -- Only call Unit.getPlayerName if target is a UNIT and still exists
            local isPlayerTarget = false
            if origTarg
                and origTarg:isExist()
                and Object.getCategory(origTarg) == Object.Category.UNIT
            then
                local pn = Unit.getPlayerName(origTarg)   -- only safe for real Units
                if pn and pn ~= "" then
                    isPlayerTarget = true
                end
            end

            local mt = missile.getTarget and missile:getTarget() or nil
            if mt == origTarg
                and origTarg
                and origTarg:isExist()
                and Object.getCategory(origTarg) == Object.Category.UNIT
            then
                if ewrj_options.DEBUG_DEFENSIVE then
                    env.info("[EW DEBUG - DEFENSIVE] Missile NOT JAMMED and hit target: " .. tostring(jammer))
                end
            end

            if remove_missile_method == 0 then
                local pos = missile:getPosition()
                if pos and pos.p then
                    trigger.action.explosion(pos.p, 5)
                end
                if ewrj_options.DEBUG_DEFENSIVE then
                    env.info("[EW DEBUG - DEFENSIVE] Missile has been jammed: " .. tostring(jammer))
                end
            else
                missile:destroy()
            end
        end

        aiMissiles[id] = nil
        numActive = numActive - 1
    end

local function checkMis(mis)
    if not (mis and mis.missile and mis.missile:isExist()) then
        removeMis(mis and mis.uid)
        return
    end

    if not (mis.origTarg and mis.origTarg:isExist()) then
        removeMis(mis.uid)
        return
    end

    ---------------------------------------------------------------
    ---- DEBUG: launcher jam state (log once per missile)
    ---------------------------------------------------------------
    if not mis.debugLogged then
        local jamRec = mis.launcherGroupName and JammedLaunchers[mis.launcherGroupName]
        local jammed = jamRec and jamRec.untilT and timer.getTime() < jamRec.untilT

        if ewrj_options.DEBUG_DEFENSIVE then
            env.info(string.format(
                "[EW DEBUG - DEFENSIVE] [MIS] uid=%d guidance=%s launcherGrp=%s jammed=%s tLeft=%.1f",
                mis.uid,
                guidanceName(mis.guidance),
                tostring(mis.launcherGroupName),
                jammed and "YES" or "NO",
                jammed and (jamRec.untilT - timer.getTime()) or 0
            ))
        end
        mis.debugLogged = true
    end
    ---------------------------------------------------
    -- SARH "launcher jammed => missile dies" code ----
    ---------------------------------------------------
    if mis.launcherGroupName and (mis.guidance == 3) then
        local rec = JammedLaunchers and JammedLaunchers[mis.launcherGroupName]
        if rec and rec.untilT and timer.getTime() < rec.untilT then
            if ewrj_options.DEBUG_OFFENSIVE then
                env.info(string.format(
                    "[EW DEBUG - OFFENSIVE] KILL missile (guidance=%s): launcher group jammed (%s) by %s (%.1fs left)",
                    tostring(mis.guidance),
                    tostring(mis.launcherGroupName),
                    tostring(rec.by),
                    rec.untilT - timer.getTime()
                ))
            end
            removeMis(mis.uid)
            return
        end
    end

    local prob = math.random(0,100)

    local misVel  = mis.missile:getVelocity()
    local targVel = (mis.origTarg and mis.origTarg.isExist and mis.origTarg:isExist() and mis.origTarg.getVelocity)
        and mis.origTarg:getVelocity()
        or {x=0,y=0,z=0}

    -- Default next check time (fallback)
    local nextDelay = 2.0

    -- Only do jammer math if THIS jammer is armed (in switch)
    local jammerActive = false
    for _, name in pairs(switch) do
        if name == jammer then
            jammerActive = true
            break
        end
    end

    if jammerActive and jammer then
        local jammerUnit = Unit.getByName(jammer)
        if jammerUnit and jammerUnit:isExist() then
            local dist = get3DDist(mis.missile:getPoint(), jammerUnit:getPoint())

            -- optional "lost track" behavior
            if dist < 9000 and not mis.lostTrack then
                if math.random(0,100) < (20 * (ewrj_options.DEFENSIVE_POWER or 1.0)) then
                    mis.lostTrack = true
                end
            end

            if dist < removalDist5 and prob < pkill_5 then
                removeMis(mis.uid); return
            elseif dist < removalDist4 and prob < pkill_4 then
                removeMis(mis.uid); return
            elseif dist < removalDist3 and prob < pkill_3 then
                removeMis(mis.uid); return
            elseif dist < removalDist2 and prob < pkill_2 then
                removeMis(mis.uid); return
            elseif dist < removalDist1 and prob < pkill_1 then
                removeMis(mis.uid); return
            end

            -- schedule rate
            if mis.lostTrack then
                nextDelay = math.random(6,10)
            else
                local relSpeed = getMag(mist.vec.sub(misVel, targVel))
                if relSpeed < 50 then relSpeed = 50 end
                nextDelay = math.min(10, dist / relSpeed)
            end
        end
    end

    timer.scheduleFunction(checkMis, mis, timer.getTime() + nextDelay)
end

    local function aiShot(event)
        if event.id ~= world.event.S_EVENT_SHOT then return end
        if not event.weapon then return end

        local w = event.weapon
        if not w:isExist() then return end

        local d = w:getDesc()
        if not d then return end

        if ewrj_options.DEBUG_DEFENSIVE then
            env.info(string.format(
                "[EW DEBUG - DEFENSIVE] shot: cat=%s guidance=%s",
                tostring(d.missileCategory),
                tostring(d.guidance)
            ))
        end

        if event.initiator then
            -- Radar missiles Filters
            if (d.missileCategory == 2 or d.missileCategory == 1)
               and (d.guidance == 3 or d.guidance == 4)
            then
                local newMis = {}
                newMis.launchTime = timer.getTime()
                newMis.uid = uid
                newMis.missile = w
                newMis.origTarg = w:getTarget()
                newMis.launcher = event.initiator
                newMis.guidance = d.guidance
                local launcherGroupName = nil
                if event.initiator.isExist and event.initiator:isExist() then
                    local lg = event.initiator:getGroup()
                    if lg then launcherGroupName = lg:getName() end
                end
                newMis.launcherGroupName = launcherGroupName
                newMis.debugLogged = false
                newMis.lostTrack = false

                aiMissiles[uid] = newMis
                uid = uid + 1
                numActive = numActive + 1

                timer.scheduleFunction(checkMis, newMis, timer.getTime() + 4)
            end
        end
    end
    simpleEvent(aiShot)
end

--------------------------------
---- Player EW Script Start ----
--------------------------------
function EWJamming(jammer)

    local _unit = Unit.getByName(jammer)
    if _unit ~= nil and _unit:isExist() == true then
    createmenu(jammer)
    EWJscript(jammer)
    end
    EWHandler = {}
    function EWHandler:onEvent(event)
        if event.id == world.event.S_EVENT_BIRTH then
            local aircraft = event.initiator
            local aircraftname = aircraft:getName()          
                if aircraftname == jammer then    
                -- trigger.action.outText(jammer, 20)
                createmenu(jammer)
                EWJscript(jammer)
                EWHandler = {}
                end
        end
        
    end
    world.addEventHandler(EWHandler)
end