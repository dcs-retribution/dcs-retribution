-- EW Script 2.02
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


---------------------------- LOOP TO SEE IF A SAM SHOULD BE SHUT OFF DEPENDING ON THE TARGET DETECTED, THE JAMMER AND THE SAM

-- ensure ActiveJammers table exists for multi-jammer support
ActiveJammers = ActiveJammers or {}

function check(jammer, samunit)
    -- trigger.action.outText(samunit.."Checking",1)

    --- New logic to replace unreliable getRadar() ---
    local UnitObject = Unit.getByName(samunit)
    if UnitObject == nil or not Unit.isExist(UnitObject) then
        -- env.info("[DEBUG] check(): SAM unit does not exist: "..tostring(samunit))
        return
    end

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

    --- Start of original script ---
    if target ~= nil then
        local targetname = target:getName()

        local jammerobject = Unit.getByName(jammer)
        if jammerobject == nil or not Unit.isExist(jammerobject) then
            -- env.info("[DEBUG] check(): jammer missing or destroyed: "..tostring(jammer).." for SAM "..tostring(samunit))
            -- if jammer doesn't exist, only restore SAM if no other jammer active
            local anyActive = false
            for otherJammer, active in pairs(ActiveJammers or {}) do
                if active and otherJammer ~= jammer then
                    -- env.info("[DEBUG] check(): other jammer still active ("..tostring(otherJammer)..") - keeping "..tostring(samunit).." suppressed")
                    anyActive = true
                    break
                end
            end
            if not anyActive then
                -- env.info("[DEBUG] check(): no other jammers - restoring "..tostring(samunit))
                mist.scheduleFunction(samON, {samunit}, timer.getTime()+ math.random(15,25))
            end
            return
        end

        -- ensure target object still valid
        local targetobject = Unit.getByName(targetname)
        if targetobject == nil or not Unit.isExist(targetobject) then
            -- env.info("[DEBUG] check(): target missing or destroyed: "..tostring(targetname).." for SAM "..tostring(samunit))
            return
        end

        -- env.info("[DEBUG] Target Name = ".. tostring(targetname) .." | Sam UNIT = ".. tostring(samunit) .." | Jammer Name = ".. tostring(jammer))

        -- LOS check
        if not isLOS(samunit, jammer) then
            -- LOS broken: only restore if no other jammer
            local anyActive = false
            for otherJammer, active in pairs(ActiveJammers or {}) do
                if active and otherJammer ~= jammer then
                    -- env.info("[DEBUG] check(): LOS lost for "..tostring(jammer).." but "..tostring(otherJammer).." still jamming "..tostring(samunit))
                    anyActive = true
                    break
                end
            end
            if not anyActive then
                -- env.info("[DEBUG] check(): LOS lost and no other jammers - restoring "..tostring(samunit))
                mist.scheduleFunction(samON, {samunit}, timer.getTime()+ math.random(15,25))
            end
            return
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
            -- env.info("[DEBUG] check(): invalid distances for SAM "..tostring(samunit).." (distSamJammer="..tostring(distSamJammer)..", distSamTarget="..tostring(distSamTarget)..")")
            return
        end

        local dice = math.random(0,100)
        local conditiondist = 100 * distSamTarget / distSamJammer

        -- HEIGHT OF JAMMER
        local Position_vec3 = jammerobject:getPoint()
        local _elevation = land.getHeight({x = Position_vec3.x, y = Position_vec3.z})
        local _height = Position_vec3.y - _elevation    

        local tPosition_vec3 = targetobject:getPoint()
        local t_elevation = land.getHeight({x = tPosition_vec3.x, y = tPosition_vec3.z})
        local t_height = tPosition_vec3.y - t_elevation    
        local prob = dice + _height/1000  + (_height - t_height)/1000
        -- trigger.action.outText("dice  "..dice.."prob  "..prob.."altjammer".._height.."alttarget"..t_height,20)

        -- LOBE parameter
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
        -- trigger.action.outText(conditiondist.." relacion ".. prob.." probabilidad",20)
        local anglecondition = 2/3 * distSamJammer/1000 
        -- trigger.action.outText(anglecondition.." target difference "..TargetandOffsetJamSam,20)

        --    PITCH and BANK
        local bankr = mist.utils.toDegree(mist.getRoll(jammerobject))
        if bankr < 0 then
            bankr = -bankr
        end
        local bank = bankr - 30

        -- trigger.action.outText("real"..bankr.."tocado"..bank,20)

        local pitchr = mist.utils.toDegree(mist.getPitch(jammerobject))
        if pitchr < 0 then
            pitchr = -pitchr
        end
        local pitch = pitchr - 30

        -- trigger.action.outText("real"..pitchr.."tocado"..pitch,20)

        local sPosition_vec3 = UnitObject:getPoint()
        -- trigger.action.outText(mist.utils.tableShow(sPosition_vec3),20)
        local s_elevation = land.getHeight({x = sPosition_vec3.x, y = sPosition_vec3.z})
        local s_height = sPosition_vec3.y - s_elevation    

        local cateto = _height - s_height
        -- trigger.action.outText("altura sam "..cateto,20)
        local samunitposition = UnitObject:getPosition().p
        local jammerposition = jammerobject:getPosition().p
        local _2DDistSamJammer = mist.utils.get2DDist(samunitposition, jammerposition)
        local anglesamjam = mist.utils.toDegree(math.asin(cateto/_2DDistSamJammer))
        -- trigger.action.outText("angulo is "..anglesamjam,20) 
        ------------------------------------------------------------------------
        local probsector1 = ((5/2)*conditiondist)+10
        local probsector2 = (conditiondist+30)
        local probsector3 = ((conditiondist/3)+57)
        if (conditiondist > 40.5)
            and (prob <= probsector3) 
            and (anglecondition < TargetandOffsetJamSam)
            and anglesamjam >= bank 
            and anglesamjam > pitch
        then
            mist.scheduleFunction(samOFF, {samunit}, timer.getTime())
        elseif ((conditiondist < 40.5) and (conditiondist > 13.33)) 
            and (prob <= probsector2) 
            and (anglecondition < TargetandOffsetJamSam)
            and anglesamjam >= bank 
            and anglesamjam > pitch                                                 
        then
            mist.scheduleFunction(samOFF, {samunit}, timer.getTime())
        elseif (conditiondist < 13.33) 
            and  (prob <=  probsector1 )
            and (anglecondition < TargetandOffsetJamSam)
            and anglesamjam >= bank 
            and anglesamjam > pitch
        then
            mist.scheduleFunction(samOFF, {samunit}, timer.getTime())
        else
            -- Only restore SAM if no other jammer is still active
            local anyActive = false
            local blockingJammer = nil
            for otherJammer, active in pairs(ActiveJammers or {}) do
                if active and otherJammer ~= jammer then
                    anyActive = true
                    blockingJammer = otherJammer
                    break
                end
            end

            if not anyActive then
                -- env.info("[DEBUG] check(): SAM "..tostring(samunit).." restored (no other jammers)")
                mist.scheduleFunction(samON, {samunit}, timer.getTime()+ math.random(15,25))
            else
                -- env.info("[DEBUG] check(): SAM "..tostring(samunit).." still jammed by "..tostring(blockingJammer))
            end
        end

    else
        -- no target
        -- trigger.action.outText(samunit.." No detection",5)
        return
    end

    offscriptfunc = mist.scheduleFunction(check, {jammer, samunit}, timer.getTime() + 5)
end

-- check('radar1')
-- check('radar2')
---------------------------- SAM ON OFF. IT CHANGES THE RULE OF ENGAGEMENT OR ALERT STATE.
function samON(groupsam)

    -- local samName = groupsam
    local unitObj = Unit.getByName(groupsam)
    if not unitObj or not Unit.isExist(unitObj) then
        -- Unit missing (dead or wrong name) — avoid nil indexing
        -- env.info("[DEBUG] samON() - Unit not found or destroyed: " .. tostring(groupsam))
        return
    end

    local _group = unitObj:getGroup()
    if not _group then
        -- env.info("[DEBUG] samON() - Group not found for unit: " .. tostring(groupsam))
        return
    end

    local _controller = _group:getController()
    if not _controller then
        -- env.info("[DEBUG] samON() - Controller missing for group of: " .. tostring(groupsam))
        return
    end

    _controller:setOption(AI.Option.Ground.id.ROE,     AI.Option.Ground.val.ROE.OPEN_FIRE)
    -- trigger.action.outText(groupsam.." SAM SWITCHING ON", 10)
    -- env.info("[DEBUG - OFFENSIVE] SAM has switched ON: " .. groupsam)
end

function samOFF(groupsam)
    local unitObj = Unit.getByName(groupsam)
    if not unitObj or not Unit.isExist(unitObj) then
        -- env.info("[DEBUG] samOFF() - Unit not found or destroyed: " .. tostring(groupsam))
        return
    end

    local _group = unitObj:getGroup()
    if not _group then
        -- env.info("[DEBUG] samOFF() - Group not found for unit: " .. tostring(groupsam))
        return
    end

    local _controller = _group:getController()
    if not _controller then
        -- env.info("[DEBUG] samOFF() - Controller missing for group of: " .. tostring(groupsam))
        return
    end

    _controller:setOption(AI.Option.Ground.id.ROE, AI.Option.Ground.val.ROE.WEAPON_HOLD)
    -- trigger.action.outText(groupsam.." SAM SWITCHING OFF", 10)
    -- local samName = groupsam    
    -- env.info("[DEBUG - OFFENSIVE] SAM has switched OFF: " .. groupsam)
    mist.scheduleFunction(samON, {groupsam}, timer.getTime()+ math.random(15,25))
end

function isLOS(sam,radar) --- check if sam is LOS with Jammer
        local mover = Unit.getByName(sam):getPosition().p
        mover.y = mover.y + 3
        -- trigger.action.outText(mist.utils.tableShow(mover),20)
        local target = Unit.getByName(radar):getPosition().p
        target.y = target.y + 1.8
        -- trigger.action.outText(mist.utils.tableShow(target),20)
            if land.isVisible(mover, target)then
            -- trigger.action.outText('Is Visible: ', 2)
            return true
            else
            return false
            end

 end
 
-------------------------------- GET A LIST OF POSSIBLE SAMS TO BE JAMMED (OFFENSIVELY)
 radarList = {}

function getRadars()
  local redUnits = mist.makeUnitTable({'[red][vehicle]','[blue][vehicle]','[red][ship]','[blue][ship]'})
  -- trigger.action.outText(mist.utils.tableShow(redUnits),15)
  for i, unitName in pairs (redUnits) do
    if type(i) == "number" then  -- makeUnitTable also has a ["processed"] = time index which does not represent a unit
        local samUnit = Unit.getByName(unitName)
        local samSensors = samUnit:getSensors()
        -- if samSensors then 
            -- trigger.action.outText("unit '"..unitName.."' has sensors",5)
            if samUnit:hasSensors(Unit.SensorType.RADAR, Unit.RadarType.AS) or samUnit:hasAttribute("SAM SR") or samUnit:hasAttribute("EWR") or samUnit:hasAttribute("SAM TR") or samUnit:hasAttribute("Armed ships") then
                -- env.info(" - also has Radar")
                -- trigger.action.outText("unit '"..unitName.."' has sensors",5)
                table.insert(radarList, unitName)
            end
        -- end
    end
  end
end
getRadars()
-- trigger.action.outText(mist.utils.tableShow(radarList),20)
 
 
 
function startEWjamm(jammer)
--    local jammerName = jammer
    trigger.action.outText("OFFENSIVE COUNTER MEASURES POD ON "..jammer,5)
    env.info("[DEBUG] Start Offensive Jamming: " ..jammer)

    -- mark jammer active for multi-jammer logic
    ActiveJammers[jammer] = true

    for k,v in pairs ( radarList)do
        if Unit.getByName(radarList[k]):getCoalition()~= Unit.getByName(jammer):getCoalition() then
            check(jammer, radarList[k]) 
            -- trigger.action.outText(radarList[k],5)
        end
    end
end
 -- startEWjamm('Prowler1')
 
function stopEWjamm(jammer)
    ActiveJammers[jammer] = nil
    trigger.action.outText("OFFENSIVE COUNTER MEASURES OFF "..jammer,5)
    env.info("[DEBUG] Stop Offensive Jamming: " .. jammer)

    -- Check if *any* other jammer is still active
    local anyActive = false
    for otherJammer, active in pairs(ActiveJammers) do
        if active and otherJammer ~= jammer then
            -- env.info("[DEBUG] stopEWjamm(): "..jammer.." stopped, but "..otherJammer.." still active")
            anyActive = true
            break
        end
    end

    -- Only restore SAMs if no other jammer exists
    if not anyActive then
        -- env.info("[DEBUG] stopEWjamm(): No jammers left, restoring all SAMs")
        for _, samName in pairs(radarList) do
            local samUnit = Unit.getByName(samName)
            if samUnit and samUnit:isExist() then
                mist.scheduleFunction(samON, {samName}, timer.getTime()+ math.random(5,15))
            end
        end
    else
        -- env.info("[DEBUG] stopEWjamm(): SAMs remain suppressed due to other active jammers")
    end
end

switch = {}
function EWJscript(jammer)
-- createmenu(jammer)
EWJD(jammer)
end

--------------------- MENU CRATION FOR START/STOP JAMMING

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

-------------------- Retribution Specific Menu Creation

function createmenu(jammer)
    if Unit.getByName(jammer) ~= nil then
        local _groupID = Unit.getByName(jammer):getGroup():getID()

        local ecmFlag = trigger.misc.getUserFlag("offensive_jamming_" .. jammer)

        local _jammermenu = missionCommands.addSubMenuForGroup(_groupID, "Jammer menu", nil)
        local _jammermenudef = missionCommands.addSubMenuForGroup(_groupID, "Defensive Jamming", _jammermenu)

        missionCommands.addCommandForGroup(_groupID, "Start Defensive Jamming", _jammermenudef, function ()
            startDjamming(jammer)
        end, nil)

        missionCommands.addCommandForGroup(_groupID, "Stop Defensive Jamming", _jammermenudef, function ()
            stopIAdefjamming(jammer)
        end, nil)

        -- Only create Offensive Jamming menu if ECM flag is set
        if ecmFlag == 1 then
            local _jammermenuoff = missionCommands.addSubMenuForGroup(_groupID, "Offensive Jamming", _jammermenu)

            missionCommands.addCommandForGroup(_groupID, "Start Offensive Jamming", _jammermenuoff, function ()
                startEWjamm(jammer)
            end, nil)

            missionCommands.addCommandForGroup(_groupID, "Stop Offensive Jamming", _jammermenuoff, function ()
                stopEWjamm(jammer)
            end, nil)
        end
    end
end

-------------------- SWITCH TO ON AND OFF THE DEFENSIVE JAMMING
    function startIAdefjamming(jammer)
        startDjamming(jammer)
        EWJD(jammer)
    end
    function startDjamming(jammer)
--        local jammerName = jammer
        switch[#switch+1]=jammer
        trigger.action.outText("DEFENSIVE COUNTER MEASURES POD ON "..jammer,5)
        env.info("[DEBUG] Start Defensive Jamming: " ..jammer)
    end

    function stopIAdefjamming(jammer)
--        local jammerName = jammer
        for i, v in pairs (switch) do
        if switch[i]==jammer then
            switch[i] = nil
        end
    end
    trigger.action.outText("DEFENSIVE COUNTER MEASURES POD OFF "..jammer,5)
    env.info("[DEBUG] Stop Defensive Jamming: " ..jammer)    
end

-------------------------------------- FUNCTION THAT EVALUATES THE DISTANCE OF THE MISSILE TO THE TARGET... YOU CAN EVEN DEFEND CLOSER AIRCRAFTS. BASED ON TRAINING MISSILES FROM GRIMES
function EWJD(jammer)

-- trigger.action.outText("EWJD Script ON "..jammer,5)
------------------------------------------------------------ DISTANCES AND PROBABILITIES OF JAMM THE MISSILE FOR DEFENSIVE JAMMING REMOVALDIST1 CORRESPOND TO PKILL1, REMOVALDIST2 CORRESPOND TO PKILL2, ETC...
local removalDist1 = 500
local removalDist2 = 1500
local removalDist3 = 3000
local removalDist4 = 5000
local removalDist5 = 7000

local pkill_1 =95 -------- PROBAILITY OF SUCCESFULL JAMMING  REMOVALDIST1 CORRESPOND TO PKILL1, REMOVALDIST2 CORRESPOND TO PKILL2, ETC...
local pkill_2 =65
local pkill_3 =50
local pkill_4 =30
local pkill_5 =15

-- DEBUG VALUES
-- local pkill_1 =100 -------- PROBAILITY OF SUCCESFULL JAMMING  REMOVALDIST1 CORRESPOND TO PKILL1, REMOVALDIST2 CORRESPOND TO PKILL2, ETC...
-- local pkill_2 =100
-- local pkill_3 =100
-- local pkill_4 =100
-- local pkill_5 =100

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
    
    getMag = function(vec) -- from mist
        return (vec.x^2 + vec.y^2 + vec.z^2)^0.5
    end
    
    get3DDist = function(point1, point2)
        return getMag({x = point1.x - point2.x, y = point1.y - point2.y, z = point1.z - point2.z})
    end
    
    local function removeMis(id)
    --    local jammerName = jammer
        if Object.isExist(aiMissiles[id].missile) then -- if missile is still active and needs to be destroyed
            if Weapon.getTarget(aiMissiles[id].missile) == aiMissiles[id].origTarg and Unit.getPlayerName(aiMissiles[id].origTarg) then
                -- trigger.action.outText(Unit.getPlayerName(aiMissiles[id].origTarg) .. ' has been hit by a simulated missile. You should eject in shame.', 20)
                -- env.info("[DEBUG - JAMMED] Missile NOT JAMMED and hit target: " ..jammer)
            end
            if remove_missile_method == 0 then
                trigger.action.explosion(Object.getPosition(aiMissiles[id].missile).p, 5)
                -- trigger.action.outText("MISSILE GO BOOM!!! "..jammer,10)
                -- trigger.action.outText("Missile has been successfully jammed"..jammer,5)
                -- env.info("[DEBUG - JAMMED] Missile has been jammed: " ..jammer)
            else
                Object.destroy(aiMissiles[id].missile)
            end
        end
        aiMissiles[id] = nil
        numActive = numActive - 1
        
        return
    end

local function checkMis(mis)
--  local jammerName = jammer
    
    local tot = 0
    
    if Object.isExist(mis.missile) == false then
        removeMis(mis.uid)
    else
        if Object.isExist(mis.origTarg) == true then
            local misVel = Object.getVelocity(mis.missile)
            local targVel = Object.getVelocity(mis.origTarg)
            
            for i, v in pairs(switch) do
                if switch[i] == jammer then
                    if jammer ~= nil then
                        local jammerUnit = Unit.getByName(jammer)
                        if jammerUnit and Unit.isExist(jammerUnit) then
                            local dist = get3DDist(mis.missile:getPoint(), jammerUnit:getPoint())
                            -- env.info("[DEBUG] Checking jammer: " .. jammer .. " | Distance: " .. dist .. " | Missile prob: " .. prob)
--                          trigger.action.outText(prob..jammer, 20)
                            
                            if dist < removalDist5 and prob < pkill_5 then -- if its close and still guiding
                                removeMis(mis.uid)
                                -- env.info("[DEBUG - JAMMED] Missile UID " .. mis.uid .. " removed by jammer " .. jammer .. " within removalDist5 and prob < pkill_5" .. prob)
                            elseif dist < removalDist4 and prob < pkill_4 then -- if its close and still guiding
                                removeMis(mis.uid)
                                -- env.info("[DEBUG - JAMMED] Missile UID " .. mis.uid .. " removed by jammer " .. jammer .. " within removalDist4 and prob < pkill_4" .. prob)
                            elseif dist < removalDist3 and prob < pkill_3 then -- if its close and still guiding
                                removeMis(mis.uid)
                                -- env.info("[DEBUG - JAMMED] Missile UID " .. mis.uid .. " removed by jammer " .. jammer .. " within removalDist3 and prob < pkill_3" .. prob)
                            elseif dist < removalDist2 and prob < pkill_2 then -- if its close and still guiding
                                removeMis(mis.uid)
                                -- env.info("[DEBUG - JAMMED] Missile UID " .. mis.uid .. " removed by jammer " .. jammer .. " within removalDist2 and prob < pkill_2" .. prob)
                            elseif dist < removalDist1 and prob < pkill_1 then -- if its close and still guiding
                                removeMis(mis.uid)
                                -- env.info("[DEBUG - JAMMED] Missile UID " .. mis.uid .. " removed by jammer " .. jammer .. " within removalDist1 and prob < pkill_1" .. prob)
                            else
                                tot = math.min(10, dist / getMag(mist.vec.sub(misVel, targVel)))
                                timer.scheduleFunction(checkMis, mis, timer.getTime() + tot)
                            end
                        else
                            -- env.info("[DEBUG] Jammer " .. tostring(jammer) .. " does not exist or is destroyed")
                        end
                    end        
                end
            end
        end
    end
end

    local function aiShot(event)
        prob = math.random(0,100)
        if event.id == world.event.S_EVENT_SHOT and event.initiator then --{{and not Unit.getPlayerName(event.initiator)}}-- then -- if AI
            if (event.weapon) and 
                                    (
                                    ((Weapon.getDesc(event.weapon).missileCategory == 2) or (Weapon.getDesc(event.weapon).missileCategory == 1)) and     
                                    ((Weapon.getDesc(event.weapon).guidance == 3 or Weapon.getDesc(event.weapon).guidance == 4))
                                    )  then
        
                local newMis = {}
                newMis.launchTime = timer.getTime()
                newMis.uid = uid
                newMis.missile = event.weapon
                newMis.origTarg = Weapon.getTarget(event.weapon)
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
  
 -- EWJamming("Prowler1")
 -- EWJamming("Prowler2")
