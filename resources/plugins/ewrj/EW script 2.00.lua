--EW Script 1.01
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
-- Now it takes into account, distances, angles between Jammer and SAMs and Aircraft targeted by SAMs (hereinafter “Target”), jammer altitude, Jammer and Target altitude differences, banking, pitching, and few other factors such as the “dice”.
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
function check(jammer, samunit)
-- trigger.action.outText(samunit.."Checking",1)
    local UnitObject = Unit.getByName(samunit)
        if UnitObject ~= nil then
        local status, target = UnitObject:getRadar()
        -- trigger.action.outText(Unitobject,20)
            -- if status == true then                         -- to see if the Radar is working
                if target ~= nil then                    -- to see if it is engaging
                local targetname = target:getName()    
                -- trigger.action.outText(samunit.." Detecting  "..targetname,2)                    
                -- trigger.action.outText(mist.utils.tableShow(jammerplanes),20)
                   
                    jammerobject = Unit.getByName(jammer)
                        if jammerobject ~= nil then
                            -- trigger.action.outText(jammer.."   "..samunit,20)
                            
                                if isLOS(samunit, jammer)==true then
                                 -- trigger.action.outText(jammer..'is LOS with '..samunit,20)
                                
                                    local distSamJammer = get3DDist(Unit.getPoint(Unit.getByName(samunit)), Unit.getPoint(Unit.getByName(jammer)))
                                    local distSamTarget = get3DDist(Unit.getPoint(Unit.getByName(samunit)), Unit.getPoint(Unit.getByName(targetname)))
                                    local dice = math.random(0,100)                                                                
                                    local conditiondist = 100 * distSamTarget  / distSamJammer
    -------------------------------------------- HEIGHT OF JAMMER

                        local Position_vec3 = Unit.getByName(jammer):getPoint()
                        local _elevation = land.getHeight({x = Position_vec3.x, y = Position_vec3.z})
                        local _height = Position_vec3.y - _elevation    
                        
                        
                        local tPosition_vec3 = Unit.getByName(targetname):getPoint()
                        local t_elevation = land.getHeight({x = tPosition_vec3.x, y = tPosition_vec3.z})
                        local t_height = tPosition_vec3.y - t_elevation    
                        local prob = dice + _height/1000  + (_height - t_height)/1000
                        -- trigger.action.outText("dice  "..dice.."prob  "..prob.."altjammer".._height.."alttarget"..t_height,20)

                        
    -------------------------------------------- LOBE parameter
                    local SamPos = mist.utils.makeVec2(Unit.getByName(samunit):getPosition().p)-- tenemos un vector x e y
-- trigger.action.outText(mist.utils.tableShow(SamPos),20)
                    local JammerPos = mist.utils.makeVec2(Unit.getByName(jammer):getPosition().p)        
-- trigger.action.outText(mist.utils.tableShow(JammerPos),20)                    
                    local TargetPos = mist.utils.makeVec2(Unit.getByName(targetname):getPosition().p)    
-- trigger.action.outText(mist.utils.tableShow(TargetPos),20)                    
                    local AngleSamJammer = mist.utils.toDegree(mist.utils.getDir(mist.vec.sub(mist.utils.makeVec3GL(JammerPos),mist.utils.makeVec3GL(SamPos))))
-- trigger.action.outText(AngleSamJammer,20)
                    local AngleSamTarget = mist.utils.toDegree(mist.utils.getDir(mist.vec.sub(mist.utils.makeVec3GL(TargetPos),mist.utils.makeVec3GL(SamPos))))    
-- trigger.action.outText(AngleSamTarget,20)                    
                    local offsetJamTar = smallestAngleDiff(AngleSamJammer, AngleSamTarget )
-- trigger.action.outText(offsetJamTar,20)
                    local offsetJamSam = smallestAngleDiff(AngleSamJammer, 180 )
-- trigger.action.outText("Jamm "..AngleSamJammer.."-Target ".. AngleSamTarget.."-Offjam ".. offsetJamSam.." -Offtar "..offsetJamTar,20)

                    local TargetandOffsetJamSam = smallestAngleDiff(AngleSamTarget, offsetJamSam )*2
                            if TargetandOffsetJamSam < 0 then
                                TargetandOffsetJamSam = -TargetandOffsetJamSam
                        
                            end
-- trigger.action.outText(conditiondist.." relacion ".. prob.." probabilidad",20)
                    local anglecondition = 2/3 * distSamJammer/1000 
                    -- trigger.action.outText(anglecondition.." target difference "..TargetandOffsetJamSam,20)
                    
    ---------------------------------------------------    PITCH and BANK

                    local bankr = mist.utils.toDegree(mist.getRoll(Unit.getByName(jammer)))
                        
                    if bankr < 0 then
                        bankr = -bankr
                    end
                        bank = bankr - 30
                        
                        -- trigger.action.outText("real"..bankr.."tocado"..bank,20)
                        
                    local pitchr = mist.utils.toDegree(mist.getPitch(Unit.getByName(jammer)))
                    if pitchr < 0 then
                        pitchr = -pitch
                    end
                        pitch = pitchr - 30
                        
                        -- trigger.action.outText("real"..bankr.."tocado"..bank,20)
                    
                    local sPosition_vec3 = Unit.getByName(samunit):getPoint()
                    -- trigger.action.outText(mist.utils.tableShow(sPosition_vec3),20)
                    local s_elevation = land.getHeight({x = sPosition_vec3.x, y = sPosition_vec3.z})
                    local s_height = sPosition_vec3.y - s_elevation    
                    
                    local cateto = _height - s_height
                    -- trigger.action.outText("altura sam "..cateto,20)
                    local samunitposition = Unit.getByName(samunit):getPosition().p
                    local jammerposition = Unit.getByName(jammer):getPosition().p
                    local _2DDistSamJammer = mist.utils.get2DDist(samunitposition, jammerposition)
                    local anglesamjam = mist.utils.toDegree(math.asin(cateto/_2DDistSamJammer))
                    -- trigger.action.outText("angulo is "..anglesamjam,20) 
    ------------------------------------------------------------------------
local probsector1 = ((5/2)*conditiondist)+10
local probsector2 = (conditiondist+30)
local probsector3 = ((conditiondist/3)+57)
                                            if      (conditiondist > 40.5)
                                                and (prob <= probsector3) 
                                                and (anglecondition < TargetandOffsetJamSam)
                                                and anglesamjam >= bank 
                                                and anglesamjam > pitch
                                                then
                                                
                                            -- trigger.action.outText(samunit.." "..conditiondist.." "..probsector3.." "..dice,20)
                                            mist.scheduleFunction(samOFF, {samunit}, timer.getTime())
                                            
                                            elseif    ((conditiondist < 40.5) and (conditiondist > 13.33)) 
                                                and (prob <= probsector2) 
                                                and (anglecondition < TargetandOffsetJamSam)
                                                and anglesamjam >= bank 
                                                and anglesamjam > pitch                                                 
                                                then
                                            -- trigger.action.outText(samunit.." "..conditiondist.." "..probsector2.." "..dice,20)
                                                    mist.scheduleFunction(samOFF, {samunit}, timer.getTime())
                                            elseif	 (conditiondist < 13.33) 
												and  (prob <= 	probsector1 )
												and (anglecondition < TargetandOffsetJamSam)
                                                and anglesamjam >= bank 
                                                and anglesamjam > pitch
												then
													mist.scheduleFunction(samOFF, {samunit}, timer.getTime())
													-- trigger.action.outText(samunit.." "..conditiondist.." "..probsector1.." "..dice,20) 
											else
                                                    mist.scheduleFunction(samON, {samunit}, timer.getTime()+ math.random(15,25))
                                            -- trigger.action.outText("fuera de cobertura",20)    
                                            end
                                else
                                -- trigger.action.outText(jammer..'NOT LOS with '..samunit,20)
                                mist.scheduleFunction(samON, {samunit}, timer.getTime()+ math.random(15,25))
                                end
                                
                        end
                               
                end
                else
                -- trigger.action.outText(samunit.." No detection",5)
                -- end
            end
			
offscriptfunc = mist.scheduleFunction(check, {jammer, samunit}, timer.getTime() + 5)
end
-- check('radar1')
-- check('radar2')
---------------------------- SAM ON OFF. IT CHANGES THE RULE OF ENGAGEMENT OR ALERT STATE.
function samON(groupsam)


_group = Unit.getByName(groupsam):getGroup()
_controller = _group:getController()
_controller:setOption(AI.Option.Ground.id.ROE,     AI.Option.Ground.val.ROE.OPEN_FIRE)
-- trigger.action.outText(groupsam.." SAM SWITCHING ON", 10)

local dice = math
end
function samOFF(groupsam)
	
_group = Unit.getByName(groupsam):getGroup()
_controller = _group:getController()
_controller:setOption(AI.Option.Ground.id.ROE, AI.Option.Ground.val.ROE.WEAPON_HOLD)
-- trigger.action.outText(groupsam.." SAM SWITCHING OFF", 10)
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
 
 
 
 function 	startEWjamm(jammer)
 trigger.action.outText("OFFENSIVE COUNTER MEASURES POD ON "..jammer,5)
 for k,v in pairs ( radarList)do
 if Unit.getByName(radarList[k]):getCoalition()~= Unit.getByName(jammer):getCoalition() then
 check(jammer, radarList[k]) 
 -- trigger.action.outText(radarList[k],5)
 end
 end
 end
 -- startEWjamm('Prowler1')
 function stopEWjamming(jammer)
mist.removeFunction(offscriptfunc)
 trigger.action.outText("OFFENSIVE COUNTER MEASURES POD OFF "..jammer,5)
end




switch = {}
function EWJscript(jammer)
-- createmenu(jammer)
EWJD(jammer)
end

--------------------- MENU CRATION FOR START/STOP JAMMING

function createmenu(jammer)
if Unit.getByName(jammer) ~= nil then
local _groupID =  Unit.getByName(jammer):getGroup():getID()


local _jammermenu = missionCommands.addSubMenuForGroup(_groupID,"Jammer menu", nil)
local _jammermenudef = missionCommands.addSubMenuForGroup(_groupID,"Defensive Jamming", _jammermenu)
local _jammermenuoff = missionCommands.addSubMenuForGroup(_groupID,"Offensive Jamming", _jammermenu)

missionCommands.addCommandForGroup(_groupID, "Start Defensive Jamming ",_jammermenudef, function () startDjamming(jammer)end, nil)
missionCommands.addCommandForGroup(_groupID, "Stop Defensive Jamming ",_jammermenudef, function () stopDjamming(jammer)end, nil)
missionCommands.addCommandForGroup(_groupID, "Start Offensive Jamming ",_jammermenuoff, function ()  startEWjamm(jammer)end, nil)
missionCommands.addCommandForGroup(_groupID, "Stop Offensive Jamming ",_jammermenuoff, function () stopEWjamming(jammer)end, nil)
end
end

-------------------- SWITCH TO ON AND OFF THE DEFENSIVE JAMMING
function startIAdefjamming(jammer)
startDjamming(jammer)
EWJD(jammer)
end
function startDjamming(jammer)
switch[#switch+1]=jammer
trigger.action.outText("DEFENSIVE COUNTER MEASURES POD ON"..jammer,5)
end

function stopDjamming(jammer)
for i, v in pairs (switch) do
if switch[i]==jammer then
switch[i] = nil
end
end
trigger.action.outText("DEFENSIVE COUNTER MEASURES POD OFF"..jammer,5)
end

-------------------------------------- FUNCTION THAT EVALUATES THE DISTANCE OF THE MISSILE TO THE TARGET... YOU CAN EVEN DEFEND CLOSER AIRCRAFTS. BASED ON TRAINING MISSILES FROM GRIMES
function EWJD(jammer)

trigger.action.outText("EWJD Script ON"..jammer,5)
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
	
        if Object.isExist(aiMissiles[id].missile) then -- if missile is still active and needs to be destroyed
            if Weapon.getTarget(aiMissiles[id].missile) == aiMissiles[id].origTarg and Unit.getPlayerName(aiMissiles[id].origTarg) then
                -- trigger.action.outText(Unit.getPlayerName(aiMissiles[id].origTarg) .. ' has been hit by a simulated missile. You should eject in shame.', 20)
            end
            if remove_missile_method == 0 then
                trigger.action.explosion(Object.getPosition(aiMissiles[id].missile).p, 5)
            else
                Object.destroy(aiMissiles[id].missile)
            end
        end
        aiMissiles[id] = nil
        numActive = numActive - 1
        
        return
    end
    local function checkMis(mis)
	
	
        local tot = 0
        
        if Object.isExist(mis.missile) == false then
            removeMis(mis.uid)
        else
            if Object.isExist(mis.origTarg) == true then
                local misVel = Object.getVelocity(mis.missile)
                local targVel = Object.getVelocity(mis.origTarg)
				for i, v in pairs (switch) do
				if switch[i]==jammer then
					
					if jammer ~= nil then
					local dist = get3DDist(Object.getPoint(mis.missile), Unit.getPoint(Unit.getByName(jammer)))
					-- trigger.action.outText(prob..jammer, 20)
							if dist < removalDist5 and prob < pkill_5 then -- if its close and still guiding
								removeMis(mis.uid)
								-- trigger.action.outText('5', 20)
							elseif	dist < removalDist4 and prob < pkill_4 then -- if its close and still guiding
								removeMis(mis.uid)
								-- trigger.action.outText('4', 20)
							elseif	dist < removalDist3 and prob < pkill_3 then -- if its close and still guiding
								removeMis(mis.uid)
								-- trigger.action.outText('3', 20)
							elseif	dist < removalDist2 and prob < pkill_2 then -- if its close and still guiding
								removeMis(mis.uid)
								-- trigger.action.outText('2', 20)
							elseif	dist < removalDist1 and prob < pkill_1 then -- if its close and still guiding
								removeMis(mis.uid)
								-- trigger.action.outText('1', 20)
							else
								tot = math.min(10, dist/getMag(mist.vec.sub(misVel, targVel)))
								timer.scheduleFunction(checkMis, mis, timer.getTime() + tot)
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

