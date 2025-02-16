----- Call Artillery Script -----
--v02.10.2022
--By Marc "MBot" Marbot
----------------------------------------------------------------

--Script control functions:
--AddFS(GroupName, SalvoSize)									--define group that can provide fire support; SalvoSize = numer of rounds per fire mission or table with selectable amounts of rounds per fire mission
--AddFO(UnitName)												--define unit that can call fire support

----------------------------------------------------------------

local SoundFilename = "l10n/DEFAULT/beep.wav"					--name of sound file to be played whenever a radio text message is displayed 
env.info("DCSRetribution|Mbot's Call Artillery Script plugin - Imported")
--Fire support groups
FS = {}															--Fire Support
function AddFS(GroupName, SalvoSize)							--add new fire support group
	if Group.getByName(GroupName) then
		FS[GroupName] = {
			callsign = Group.getByName(GroupName):getUnit(1):getCallsign(),
			SalvoSize = SalvoSize or {10, 20, 30, 40},
		}
		if FS[GroupName].callsign == "" then
			FS[GroupName].callsign = GroupName
		else
			local a,b = string.find(FS[GroupName].callsign, "%d%d")
			FS[GroupName].callsign = string.sub(FS[GroupName].callsign, 1, a - 1) .. " " .. string.sub(FS[GroupName].callsign, a, a) .. "-" .. string.sub(FS[GroupName].callsign, b, b)		--put callsign "Enfield11" into format "Enfield 1-1"
		end
	end
end

--Forward observer units
FO = {}															--Forward Obeserver that can request fire support
function AddFO(UnitName)										--add new forward observer
	FO[UnitName] = {}
end

local Mission = {}												--table to store fire missions

--collect added user marks
local UserMark = {												--table to store added user marks										
	[1] = {},													--red coalition
	[2] = {},													--blue coalition
}
MarkEventHandler = {}
function MarkEventHandler:onEvent(event)
	if event.id == world.event.S_EVENT_MARK_ADDED then
		if event.coalition == 1 or event.coalition == 2 then	--mark is coalition specific
			table.insert(UserMark[event.coalition], event)		--add to coalition
		else													--mark is not coalition specific
			table.insert(UserMark[1], event)					--add to both coalitions
			table.insert(UserMark[2], event)					--add to both coalitions
		end
	elseif event.id == 27 then									--mark remove
		if event.coalition == 1 or event.coalition == 2 then	--mark is coalition specific
			for i = 1, #UserMark[event.coalition] do
				if UserMark[event.coalition][i].idx == event.idx then
					table.remove(UserMark[event.coalition], i)
					break
				end
			end
		else													--mark is not coalition specific
			for c = 1, 2 do
				for i = 1, #UserMark[c] do
					if UserMark[c][i].idx == event.idx then
						table.remove(UserMark[c], i)
						break
					end
				end
			end
		end
	end
end
world.addEventHandler(MarkEventHandler)

--return amount of artillery ammo rounds in a group
local function ReturnArtilleryAmmo(GroupName)
	local group = Group.getByName(GroupName)
	if group then
		local units = group:getUnits()
		
		--find the primary artillery ammo type of group leader
		local ammoType = "n/a"										--variable to store the primary artillery ammo type
		local ammoCat												--variable to store ammo category (shell or rocket)
		local ammo = units[1]:getAmmo()								--get all ammo of group leader
		if ammo then												--ammo is not nil
			for a = 1, #ammo do										--iterate through different ammo types
				if ammo[a].desc and ammo[a].desc.category and ammo[a].desc.category == 0 then		--ammo is a shell
					if ammo[a].desc.warhead and ammo[a].desc.warhead.caliber and  ammo[a].desc.warhead.caliber > 70 then	--caliber needs to be bigger than 70 mm to be considered as artillery ammo
						ammoType = ammo[a].desc.displayName			--store ammo type name
						ammoCat = ammo[a].desc.category				--store ammo category (shell or rocket)
						break
					end
				elseif ammo[a].desc and ammo[a].desc.category and ammo[a].desc.category == 2 then		--ammo is a rocket
					ammoType = ammo[a].desc.displayName				--store ammo type name
					ammoCat = ammo[a].desc.category					--store ammo category (shell or rocket)
					break
				end
			end
		end
		--trigger.action.outText(ammoType, 99)
		
		--collect the amount of primary artillery ammo in group
		local ammoNumber = 0
		for u = 1, #units do										--iterate throug all units in group
			if units[u]:getTypeName() ~= "MLRS FDDM" then			--MLRS FDDM includes 1 M26 round as ammo (seems to be a bug). Exclude this unit type from ammo count to correctly count ammo of MLRS batteries
				ammo = units[u]:getAmmo()							--get unit ammo
				if ammo then										--ammo is not nil
					for a = 1, #ammo do								--iterate through different ammo types
						if ammo[a].desc and ammo[a].desc.displayName and ammo[a].desc.displayName == ammoType then		--ammo type is the groups primary artillery ammo type
							ammoNumber = ammoNumber + ammo[a].count		--add up the number of rounds of this type in group
						end
					end
				end
			end
		end
		--trigger.action.outText(ammoNumber, 99)
		
		local minRange = 0
		local maxRange = 20000
		local warhead = "HE"
		
		if ammoType == 'leFH18_105HE' then
			maxRange = 10500
		elseif ammoType == 'HE M1 Shell' then
			maxRange = 11500
		elseif ammoType == 'Pz.Gr. 39 (75mm APCBC-HE-T)' then
			maxRange = 3000
		elseif ammoType == '9M55K (300mm CM-AP)' then
			minRange = 20000
			maxRange = 70000
			warhead = "ICM"
		elseif ammoType == '9M55F (300mm HE)' then
			minRange = 20000
			maxRange = 70000
		elseif ammoType == '9M27F (220mm HE)' then
			minRange = 11500
			maxRange = 35500
		elseif ammoType == '9M22U (122mm HE)' then
			minRange = 5000
			maxRange = 19000
		elseif ammoType == 'S-8OFP2' then
			maxRange = 5000
		elseif ammoType == 'M26 (270mm DPICM)' then
			minRange = 10000
			maxRange = 32000
			warhead = "ICM"
		elseif ammoType == '3OF49 (120mm HE)' then
			maxRange = 7000
		elseif ammoType == '155mm HE' then
			maxRange = 23500
		elseif ammoType == '3OF56 (122mm HE)' then
			maxRange = 15000
		elseif ammoType == '3OF45 (152mm HE)' then
			maxRange = 23500
		elseif ammoType == '53OF540 (152mm HE)' then
			maxRange = 17000
		elseif ammoType == '152-EOF (152mm HE)' then
			maxRange = 18500
		elseif ammoType == 'M795 (155mm HE)' then
			maxRange = 22000
		elseif ammoType == 'M101 (155mm HE)' then
			maxRange = 18300
		elseif ammoType == 'K307 (155mm HE)' then
			maxRange = 41000
		elseif ammoType == '130mm HE' then
			maxRange = 23000
		elseif ammoType == '127mm HE' then
			maxRange = 23700
		elseif ammoType == '100mm HE' then
			maxRange = 20000
		elseif ammoType == '76mm HE' then
			maxRange = 18350
		elseif ammoType == 'Mk 12 HE' then
			maxRange = 16000
		end
		
		return ammoNumber, ammoCat, minRange, maxRange, warhead, ammoType
	end
end


----- End Active Fire Mission -----
local function FO_EndFireMission(N)
	if FS[Mission[N].FS_name].status == "request" then
		trigger.action.outTextForCoalition(Mission[N].coalition, Mission[N].FO_callsign .. ": Cancel mission, over.", 10)
		trigger.action.outSoundForCoalition(Mission[N].coalition, SoundFilename)
		
		local function AcknowlegdeReply()
			trigger.action.outTextForCoalition(Mission[N].coalition, Mission[N].FS_callsign .. ": Cancel mission, out.", 10)
			trigger.action.outSoundForCoalition(Mission[N].coalition, SoundFilename)
			PopulateFreshRadioMenu(Mission[N].FO_name)
			FS[Mission[N].FS_name].status = nil
			Mission[N].idle = nil
		end
		timer.scheduleFunction(AcknowlegdeReply, nil, timer.getTime() + 3)
		
	elseif FS[Mission[N].FS_name].status == "prepare fire" then
		trigger.action.outTextForCoalition(Mission[N].coalition, Mission[N].FO_callsign .. ": Check fire, end mission, over.", 10)
		trigger.action.outSoundForCoalition(Mission[N].coalition, SoundFilename)
		
		local function AcknowlegdeReply()
			trigger.action.outTextForCoalition(Mission[N].coalition, Mission[N].FS_callsign .. ": Check fire, end mission, out.", 10)
			trigger.action.outSoundForCoalition(Mission[N].coalition, SoundFilename)
			PopulateFreshRadioMenu(Mission[N].FO_name)
			FS[Mission[N].FS_name].status = nil
			FS[Mission[N].FS_name].mission = nil
			Mission[N].idle = nil
			if Group.getByName(Mission[N].FS_name) then
				Group.getByName(Mission[N].FS_name):getController():resetTask()	--reset task
			end
			
		end
		timer.scheduleFunction(AcknowlegdeReply, nil, timer.getTime() + 3)
	
	elseif FS[Mission[N].FS_name].status == "firing" then
		trigger.action.outTextForCoalition(Mission[N].coalition, Mission[N].FO_callsign .. ": Check fire, over.", 10)
		trigger.action.outSoundForCoalition(Mission[N].coalition, SoundFilename)
		FS[Mission[N].FS_name].status = "cease fire"
		
		local function AcknowlegdeReply()
			trigger.action.outTextForCoalition(Mission[N].coalition, Mission[N].FS_callsign .. ": Check fire, out.", 10)
			trigger.action.outSoundForCoalition(Mission[N].coalition, SoundFilename)
			if Group.getByName(Mission[N].FS_name) then
				Group.getByName(Mission[N].FS_name):getController():resetTask()	--reset task
			end
		end
		timer.scheduleFunction(AcknowlegdeReply, nil, timer.getTime() + 3)
		
	elseif FS[Mission[N].FS_name].status == "splash" then
		trigger.action.outTextForCoalition(Mission[N].coalition, Mission[N].FO_callsign .. ": End of mission, over.", 10)
		trigger.action.outSoundForCoalition(Mission[N].coalition, SoundFilename)
		
		local function AcknowlegdeReply()
			trigger.action.outTextForCoalition(Mission[N].coalition, Mission[N].FS_callsign .. ": End of mission, out.", 10)
			trigger.action.outSoundForCoalition(Mission[N].coalition, SoundFilename)
			PopulateFreshRadioMenu(Mission[N].FO_name)
			FS[Mission[N].FS_name].status = nil
			Mission[N].idle = nil
			if Group.getByName(Mission[N].FS_name) then
				Group.getByName(Mission[N].FS_name):getController():resetTask()	--reset task
			end
		end
		timer.scheduleFunction(AcknowlegdeReply, nil, timer.getTime() + 3)
	end
	
	missionCommands.removeItemForGroup(Mission[N].FO_id, "Fire Support")
	missionCommands.addSubMenuForGroup(Mission[N].FO_id, "Fire Support")
end


----- Artillery Perform Fire Mission -----
local function FireMission(N, expendQty)
	if FS[Mission[N].FS_name].status then
		if Group.getByName(Mission[N].FS_name) then		
			local FSammoQty, ammoCat, minRange, maxRange, warheadType, ammoType = ReturnArtilleryAmmo(Mission[N].FS_name)
			local FSpoint = Group.getByName(Mission[N].FS_name):getUnit(1):getPoint()
			local DistToTarget = math.sqrt(math.pow(FSpoint.x - Mission[N].x, 2) + math.pow(FSpoint.z - Mission[N].z, 2))
			if FSammoQty == 0 then
				trigger.action.outTextForCoalition(Mission[N].coalition, Mission[N].FS_callsign .. ": Cannot comply, out of ammo, end of mission, out.", 15)
				trigger.action.outSoundForCoalition(Mission[N].coalition, SoundFilename)
				PopulateFreshRadioMenu(Mission[N].FO_name)
				FS[Mission[N].FS_name].status = nil
				Mission[N].idle = nil
			elseif DistToTarget < minRange then
				trigger.action.outTextForCoalition(Mission[N].coalition, Mission[N].FS_callsign .. ": Cannot comply, target within minimum range, end of mission, out.", 15)
				trigger.action.outSoundForCoalition(Mission[N].coalition, SoundFilename)
				PopulateFreshRadioMenu(Mission[N].FO_name)
				FS[Mission[N].FS_name].status = nil
				Mission[N].idle = nil
			elseif DistToTarget > maxRange then
				trigger.action.outTextForCoalition(Mission[N].coalition, Mission[N].FS_callsign .. ": Cannot comply, target out of range, end of mission, out.", 15)
				trigger.action.outSoundForCoalition(Mission[N].coalition, SoundFilename)
				PopulateFreshRadioMenu(Mission[N].FO_name)
				FS[Mission[N].FS_name].status = nil
				Mission[N].idle = nil
			else
				FS[Mission[N].FS_name].status = "prepare fire"
				missionCommands.removeItemForGroup(Mission[N].FO_id, "Fire Support")
				missionCommands.addSubMenuForGroup(Mission[N].FO_id, "Fire Support")
				missionCommands.addCommandForGroup(Mission[N].FO_id, "Check Fire", {"Fire Support"}, FO_EndFireMission, N)
			
				if FSammoQty < expendQty then
					trigger.action.outTextForCoalition(Mission[N].coalition, Mission[N].FS_callsign .. ": Cannot comply with " .. expendQty .. " rounds, " .. FSammoQty .. " rounds in effect, out.", 15)
					trigger.action.outSoundForCoalition(Mission[N].coalition, SoundFilename)
					expendQty = FSammoQty
				end
				
				local weaponType
				if ammoCat == 0 then												--ammo category is shell
					weaponType = 536870912											--fire with cannon
				elseif ammoCat == 2 then											--ammo category is rocket
					weaponType = 30720												--fire with rocket
				end
				
				local radius = 1
				if expendQty > 1 then
					radius = 100
				end
				
				local function CheckFireMissionOngoing()								--after 4 minutes of issuing the task, check if FS has shot first round (might be unable to and is stuck for unknown reason)
					Mission[N].funcID = nil
					if FS[Mission[N].FS_name].mission == N then							--FS has not fired first shot yet, reset everything
						trigger.action.outTextForCoalition(Mission[N].coalition, Mission[N].FS_callsign .. ": Unable to fire, end of mission, out.", 15)
						trigger.action.outSoundForCoalition(Mission[N].coalition, SoundFilename)
						PopulateFreshRadioMenu(Mission[N].FO_name)
						FS[Mission[N].FS_name].status = nil
						FS[Mission[N].FS_name].mission = nil
						Mission[N].idle = nil
						if Group.getByName(Mission[N].FS_name) then
							Group.getByName(Mission[N].FS_name):getController():resetTask()	--reset task
						end
					end
				end
				if Mission[N].funcID then
					timer.removeFunction(Mission[N].funcID)
				end
				Mission[N].funcID = timer.scheduleFunction(CheckFireMissionOngoing, nil, timer.getTime() + 240)
				
				local FireMissionTask = {
					id = "ComboTask",
					params = {
						tasks = {
							[1] = {													--fire at target task
								id = 'ControlledTask', 
								params = { 
									task = {
										id = 'FireAtPoint',
										params = {
											x = Mission[N].x,
											y = Mission[N].z,
											zoneRadius = radius,
											expendQty = expendQty,
											expendQtyEnabled = true,
											weaponType = weaponType,
										}
									},
									stopCondition = {
										duration = 600,								--stop the task if it cannot be completed in 10 minutes
									},
								},
							},
						},
					},
				}
				Group.getByName(Mission[N].FS_name):getController():setTask(FireMissionTask)
				Mission[N].lastRoundN = expendQty
				FS[Mission[N].FS_name].mission = N
				Mission[N].ammoType = ammoType
			end
		else
			trigger.action.outTextForCoalition(Mission[N].coalition, Mission[N].FS_callsign .. ": Cannot comply, unit out of action, end of mission, out.", 15)
			trigger.action.outSoundForCoalition(Mission[N].coalition, SoundFilename)
			PopulateFreshRadioMenu(Mission[N].FO_name)
			Mission[N].idle = nil
		end
	end
end


----- FO Actions After Salvo Impact -----
--repeat the last salvo
local function FO_RepeatFireMission(N)
	Mission[N].idle = timer.getTime() + 300
	missionCommands.removeItemForGroup(Mission[N].FO_id, "Fire Support")
	missionCommands.addSubMenuForGroup(Mission[N].FO_id, "Fire Support")
	
	trigger.action.outTextForCoalition(Mission[N].coalition, Mission[N].FO_callsign .. ": Repeat, over.", 10)
	trigger.action.outSoundForCoalition(Mission[N].coalition, SoundFilename)
	local function AcknowlegdeReply()
		trigger.action.outTextForCoalition(Mission[N].coalition, Mission[N].FS_callsign .. ": Repeat, out.", 10)
		trigger.action.outSoundForCoalition(Mission[N].coalition, SoundFilename)
		local function delay()
			FireMission(N, Mission[N].lastRoundN)
		end
		timer.scheduleFunction(delay, nil, timer.getTime() + 10)
	end
	timer.scheduleFunction(AcknowlegdeReply, nil, timer.getTime() + 3)
end

--adjust the next salvo
local function FO_AdjustFire(arg)
	Mission[arg[1]].idle = timer.getTime() + 300
	missionCommands.removeItemForGroup(Mission[arg[1]].FO_id, "Fire Support")
	missionCommands.addSubMenuForGroup(Mission[arg[1]].FO_id, "Fire Support")
	
	if arg[2] == "NORTH" then
		Mission[arg[1]].x = Mission[arg[1]].x + arg[3]
	elseif arg[2] == "SOUTH" then
		Mission[arg[1]].x = Mission[arg[1]].x - arg[3]
	end
	
	if arg[4] == "WEST" then
		Mission[arg[1]].z = Mission[arg[1]].z - arg[5]
	elseif arg[4] == "EAST" then
		Mission[arg[1]].z = Mission[arg[1]].z + arg[5]
	end
	
	local adjust_text = ""
	if arg[3] > 0 then
		adjust_text = adjust_text .. arg[2] .. " " .. arg[3] .. ", "
	end
	if arg[5] > 0 then
		adjust_text = adjust_text .. arg[4] .. " " .. arg[5] .. ", "
	end
	
	trigger.action.outTextForCoalition(Mission[arg[1]].coalition, Mission[arg[1]].FO_callsign .. ": " .. adjust_text .. arg[6] .. ", over.", 10)
	trigger.action.outSoundForCoalition(Mission[arg[1]].coalition, SoundFilename)
	local function AcknowlegdeReply()
		trigger.action.outTextForCoalition(Mission[arg[1]].coalition, Mission[arg[1]].FS_callsign .. ": " .. adjust_text .. arg[6] .. ", out.", 10)
		trigger.action.outSoundForCoalition(Mission[arg[1]].coalition, SoundFilename)
		
		local function delay()
			if arg[6] == "adjust fire" then
				FireMission(arg[1], 1)
			elseif arg[6] == "fire for effect" then
				FireMission(arg[1], Mission[arg[1]].rounds)
			end
		end
		timer.scheduleFunction(delay, nil, timer.getTime() + 10)
	end
	timer.scheduleFunction(AcknowlegdeReply, nil, timer.getTime() + 5)
end

--radio menu after salvo impact listing options: adjust impact point, repeat mission, end mission
local function FO_AdjustFireRadioMenu(N)
	missionCommands.removeItemForGroup(Mission[N].FO_id, "Fire Support")
	missionCommands.addSubMenuForGroup(Mission[N].FO_id, "Fire Support")
	if Mission[N].MissionType == "adjust fire" and Mission[N].lastRoundN == 1 then
		missionCommands.addCommandForGroup(Mission[N].FO_id, "Fire for effect", {"Fire Support"}, FO_AdjustFire, {N, "NORTH", 0, "WEST", 0, "fire for effect"})
	end
	missionCommands.addSubMenuForGroup(Mission[N].FO_id, "Adjust Impact Point", {"Fire Support"})
	
	for Lat = 1, 2 do
		if Lat == 1 then
			Lat = "NORTH"
		elseif Lat == 2 then
			Lat = "SOUTH"
		end
		missionCommands.addSubMenuForGroup(Mission[N].FO_id, Lat, {"Fire Support", "Adjust Impact Point"})
		
		for LatDist = 1, 10 do
			if LatDist == 1 then
				LatDist = 0
			elseif LatDist == 2 then
				LatDist = 50
			elseif LatDist == 3 then
				LatDist = 100
			elseif LatDist == 4 then
				LatDist = 200
			elseif LatDist == 5 then
				LatDist = 300
			elseif LatDist == 6 then
				LatDist = 400
			elseif LatDist == 7 then
				LatDist = 500
			elseif LatDist == 8 then
				LatDist = 600
			elseif LatDist == 9 then
				LatDist = 800
			elseif LatDist == 10 then
				LatDist = 1000
			end
			missionCommands.addSubMenuForGroup(Mission[N].FO_id, LatDist .. " M", {"Fire Support", "Adjust Impact Point", Lat})
			
			for Lon = 1, 2 do
				if Lon == 1 then
					Lon = "WEST"
				elseif Lon == 2 then
					Lon = "EAST"
				end
				missionCommands.addSubMenuForGroup(Mission[N].FO_id, Lon, {"Fire Support", "Adjust Impact Point", Lat, LatDist .. " M"})
				
				for LonDist = 1, 10 do
					if LonDist == 1 then
						LonDist = 0
					elseif LonDist == 2 then
						LonDist = 50
					elseif LonDist == 3 then
						LonDist = 100
					elseif LonDist == 4 then
						LonDist = 200
					elseif LonDist == 5 then
						LonDist = 300
					elseif LonDist == 6 then
						LonDist = 400
					elseif LonDist == 7 then
						LonDist = 500
					elseif LonDist == 8 then
						LonDist = 600
					elseif LonDist == 9 then
						LonDist = 800
					elseif LonDist == 10 then
						LonDist = 1000
					end
					missionCommands.addSubMenuForGroup(Mission[N].FO_id, LonDist .. " M", {"Fire Support", "Adjust Impact Point", Lat, LatDist .. " M", Lon})
					
					missionCommands.addCommandForGroup(Mission[N].FO_id, "Adjust Fire", {"Fire Support", "Adjust Impact Point", Lat, LatDist .. " M", Lon, LonDist .. " M"}, FO_AdjustFire, {N, Lat, LatDist, Lon, LonDist, "adjust fire"})
					missionCommands.addCommandForGroup(Mission[N].FO_id, "Fire For Effect", {"Fire Support", "Adjust Impact Point", Lat, LatDist .. " M", Lon, LonDist .. " M"}, FO_AdjustFire, {N, Lat, LatDist, Lon, LonDist, "fire for effect"})
				end
			end
		end
	end
	
	missionCommands.addCommandForGroup(Mission[N].FO_id, "Repeat Mission", {"Fire Support"}, FO_RepeatFireMission, N)
	missionCommands.addCommandForGroup(Mission[N].FO_id, "End Mission", {"Fire Support"}, FO_EndFireMission, N)
end


----- First Round Impact Call -----
--weapon tracking to make splash call 5 seconds from impact of first round
local function TrackWeapon(N)
	if Mission[N].weapon and Mission[N].weapon:isExist() then
		local WeaponPoint = Mission[N].weapon:getPoint()		--position of the weapon
		local WeaponVV = Mission[N].weapon:getVelocity()		--velocity vector of the weapon
		local WeaponSpeed = math.sqrt(math.pow(WeaponVV.x, 2) + math.pow(WeaponVV.y, 2) + math.pow(WeaponVV.z, 2))						--airspeed of weapon
		local FreeFallSpeed = 9.81 * math.sqrt((WeaponPoint.y - Mission[N].y) / (0.5 * 9.81))											--the potential speed weapon could pick up when free falling down on target due to gravity (this ignores weapon drag)
		--trigger.action.outText("Current speed: " .. WeaponSpeed, 2)
		WeaponSpeed = WeaponSpeed + FreeFallSpeed																						--add potential free fall speed to current weapon speed. This is important for high angle trajectories where weapon speed gets very low on top and then picks up again.
		--trigger.action.outText("Alt above target: " .. WeaponPoint.y - Mission[N].y, 2)
		--trigger.action.outText("Free fall speed: " .. FreeFallSpeed, 2)
		local DistanceToTarget = math.sqrt(math.pow(Mission[N].x - WeaponPoint.x, 2) + math.pow(Mission[N].y - WeaponPoint.y, 2) + math.pow(Mission[N].z - WeaponPoint.z, 2))		--distance from weapon to target
		local TimeToImpact = DistanceToTarget / WeaponSpeed																				--time until weapon reaches target
		
		--trigger.action.outText("Speed: " .. WeaponSpeed, 2)
		--trigger.action.outText("Distance: " .. DistanceToTarget, 2)
		--trigger.action.outText("TTI: " .. TimeToImpact, 2)
		
		if TimeToImpact > 5 then								--time to impact is bigger than 5 seconds
			return timer.getTime() + TimeToImpact - 4			--track weapon again 4 seconds from impact
		else													--time to impact is 5 seconds or less
			trigger.action.outTextForCoalition(Mission[N].coalition, Mission[N].FS_callsign .. ": Splash, over.", 10)
			trigger.action.outSoundForCoalition(Mission[N].coalition, SoundFilename)
			local function AcknowlegdeReply()
				trigger.action.outTextForCoalition(Mission[N].coalition, Mission[N].FO_callsign .. ": Splash, out.", 10)
				trigger.action.outSoundForCoalition(Mission[N].coalition, SoundFilename)
				FS[Mission[N].FS_name].status = "splash"
				FO_AdjustFireRadioMenu(N)
				Mission[N].idle = timer.getTime() + 180
			end
			timer.scheduleFunction(AcknowlegdeReply, nil, timer.getTime() + 4)
		end
	else
		FS[Mission[N].FS_name].status = "splash"
		FO_AdjustFireRadioMenu(N)
		Mission[N].idle = timer.getTime() + 180
	end
end

--capture the first shot of the firing group
ShotEventHandler = {}
function ShotEventHandler:onEvent(event)
	if event.id == world.event.S_EVENT_SHOT then
		local InitGroupName = event.initiator:getGroup():getName()
		if FS[InitGroupName] and FS[InitGroupName].mission then			--group is Fire Support and has not yet fired first round
			local N = FS[InitGroupName].mission
			if event.weapon and event.weapon:getDesc() and event.weapon:getDesc().displayName and event.weapon:getDesc().displayName == Mission[N].ammoType then	--weapon is the expected ammo type for fire mission
				FS[Mission[N].FS_name].status = "firing"
				trigger.action.outTextForCoalition(Mission[N].coalition, Mission[N].FS_callsign .. ": Shot, over.", 10)
				trigger.action.outSoundForCoalition(Mission[N].coalition, SoundFilename)
				local function ShotReply()
					if FS[Mission[N].FS_name].status ~= "cease fire" then
						trigger.action.outTextForCoalition(Mission[N].coalition, Mission[N].FO_callsign .. ": Shot, out.", 10)
						trigger.action.outSoundForCoalition(Mission[N].coalition, SoundFilename)
					end
				end
				timer.scheduleFunction(ShotReply, nil, timer.getTime() + 4)
			
				Mission[N].weapon = event.weapon								--store the first weapon fired in this fire mission for later tracking
				timer.scheduleFunction(TrackWeapon, N, timer.getTime() + 4)		--track flight of shell to get its time to impact
				FS[InitGroupName].mission = nil							--mark as nil to stop tracking of subsequent shells in fire mission
				Mission[N].idle = timer.getTime() + 180
			end
		end
	end
end
world.addEventHandler(ShotEventHandler)


----- Call for Fire Part 3 (description of target, method of engagement, and method of fire and control) -----
local function FS_AcknowledgeMethod(N)
	if Group.getByName(Mission[N].FS_name) then
		Mission[N].idle = timer.getTime() + 300
		local text
		if Mission[N].MissionType == "adjust fire" then
			text = ": " .. Mission[N].warheadType .. " in effect, " .. Mission[N].rounds
		elseif Mission[N].MissionType == "fire for effect" then
			text = ": " .. Mission[N].warheadType .. ", " .. Mission[N].rounds
		end
		if Mission[N].rounds == 1 then
			text = text .. " round, out."
		else
			text = text .. " rounds, out."
		end
		trigger.action.outTextForCoalition(Mission[N].coalition, Mission[N].FS_callsign .. text, 15)
		trigger.action.outSoundForCoalition(Mission[N].coalition, SoundFilename)
		
		FS[Mission[N].FS_name].status = "prepare fire"
		missionCommands.addCommandForGroup(Mission[N].FO_id, "Check Fire", {"Fire Support"}, FO_EndFireMission, N)
		
		local function delay()
			if Mission[N].MissionType == "adjust fire" then
				FireMission(N, 1)
			elseif Mission[N].MissionType == "fire for effect" then
				FireMission(N, Mission[N].rounds)
			end
		end
		timer.scheduleFunction(delay, nil, timer.getTime() + 10)
		
	else
		Mission[N].idle = nil
		PopulateFreshRadioMenu(Mission[N].FO_name)
		trigger.action.outTextForCoalition(Mission[N].coalition, Mission[N].FS_callsign .. ": Cannot comply, unit out of action, out.", 15)
		trigger.action.outSoundForCoalition(Mission[N].coalition, SoundFilename)
	end
end

local function FO_TransmitMethod(arg)
	local N = arg[1]
	Mission[N].idle = timer.getTime() + 180
	Mission[N].rounds = arg[2]
	local _, _, _, _, warheadType = ReturnArtilleryAmmo(Mission[N].FS_name)
	Mission[N].warheadType = warheadType
	local text
	if Mission[N].MissionType == "adjust fire" then
		text = ": " .. Mission[N].warheadType .. " in effect, " .. Mission[N].rounds
	elseif Mission[N].MissionType == "fire for effect" then
		text = ": " .. Mission[N].warheadType .. ", " .. Mission[N].rounds
	end
	if Mission[N].rounds == 1 then
		text = text .. " round, over."
	else
		text = text .. " rounds, over."
	end
	trigger.action.outTextForCoalition(Mission[N].coalition, Mission[N].FO_callsign .. text, 15)
	trigger.action.outSoundForCoalition(Mission[N].coalition, SoundFilename)
	timer.scheduleFunction(FS_AcknowledgeMethod, N, timer.getTime() + 5)
	missionCommands.removeItemForGroup(Mission[N].FO_id, "Fire Support")
	missionCommands.addSubMenuForGroup(Mission[N].FO_id, "Fire Support")
end

local function InsertSalvoSize(N)
	local roundsN = FS[Mission[N].FS_name].SalvoSize
	if type(roundsN) == "table" then
		for n = 1, #roundsN do
			missionCommands.addCommandForGroup(Mission[N].FO_id, roundsN[n] .. " rounds", {"Fire Support"}, FO_TransmitMethod, {N, roundsN[n]})
			if n == 9 then
				break
			end
		end
		missionCommands.addCommandForGroup(Mission[N].FO_id, "Cancel Call For Fire", {"Fire Support"}, FO_EndFireMission, N)
	else
		missionCommands.addCommandForGroup(Mission[N].FO_id, roundsN .. " rounds", {"Fire Support"}, FO_TransmitMethod, {N, roundsN})
	end
end


----- Call for Fire Part 2 (target location) -----
local function FS_AcknowledgeTargetLocation(N)
	if Group.getByName(Mission[N].FS_name) then
		trigger.action.outTextForCoalition(Mission[N].coalition, Mission[N].FS_callsign .. ": Grid " .. Mission[N].grid .. ", out.", 15)
		trigger.action.outSoundForCoalition(Mission[N].coalition, SoundFilename)
		InsertSalvoSize(N)
	else
		trigger.action.outTextForCoalition(Mission[N].coalition, Mission[N].FS_callsign .. ": Cannot comply, unit out of action, out.", 15)
		trigger.action.outSoundForCoalition(Mission[N].coalition, SoundFilename)
		PopulateFreshRadioMenu(Mission[N].FO_name)
		Mission[N].idle = nil
	end
end

local function FO_TransmitTargetLocation(arg)
	Mission[arg[1]].idle = timer.getTime() + 180
	local N = arg[1]
	Mission[N].x = arg[2].x
	Mission[N].y = land.getHeight({x = arg[2].x, y = arg[2].z})				--target elevation
	Mission[N].z = arg[2].z
	Mission[N].grid = arg[3]
	
	trigger.action.outTextForCoalition(Mission[N].coalition, Mission[N].FO_callsign .. ": Grid " .. Mission[N].grid .. ", over.", 15)
	trigger.action.outSoundForCoalition(Mission[N].coalition, SoundFilename)
	timer.scheduleFunction(FS_AcknowledgeTargetLocation, N, timer.getTime() + 5)
	missionCommands.removeItemForGroup(Mission[N].FO_id, "Fire Support")
	missionCommands.addSubMenuForGroup(Mission[N].FO_id, "Fire Support")
end

local function FO_DetermineTargetLoction(N)
	
	----- Target coordinates from map marker -----
	local function StartMarkEntry()
		Mission[N].idle = timer.getTime() + 180
		missionCommands.removeItemForGroup(Mission[N].FO_id, {"Fire Support", "Transmit Target Location", "From Map Marker"})
		missionCommands.addSubMenuForGroup(Mission[N].FO_id, "From Map Marker", {"Fire Support", "Transmit Target Location"})
		local c = Unit.getByName(Mission[N].FO_name):getCoalition()						--FO coalition
		for n = #UserMark[c], #UserMark[c] - 8, -1 do									--get the last 9 added map markers
			if n == 0 then
				break
			end
			local point = UserMark[c][n].pos
			local lat, lon = coord.LOtoLL(point)										--target coordinates
			local MGRS = coord.LLtoMGRS(lat, lon)										--target MGRS grid
			local MGRS6 = MGRS.MGRSDigraph .. " " .. math.floor(MGRS.Easting / 100) .. " " .. math.floor(MGRS.Northing / 100)	--simplified MGRS grid to 100m precision
			missionCommands.addCommandForGroup(Mission[N].FO_id, MGRS6, {"Fire Support", "Transmit Target Location", "From Map Marker"}, FO_TransmitTargetLocation, {N, point, MGRS6})
		end
		missionCommands.addCommandForGroup(Mission[N].FO_id, "Refresh List", {"Fire Support", "Transmit Target Location", "From Map Marker"}, StartMarkEntry, nil)
	end
	
	
	----- Manual grid entry -----	
	local function InsertMGRS_Northing(MGRS)											--populate the radio menu to enter the MGRS Northing coordinates
		Mission[N].idle = timer.getTime() + 180
		trigger.action.outTextForUnit(Unit.getByName(Mission[N].FO_name):getID(), "Manual Grid Entry: " .. MGRS.MGRSDigraph .. " " .. MGRS.e1 .. MGRS.e2 .. MGRS.e3 .. " ...", 3)
		missionCommands.removeItemForGroup(Mission[N].FO_id, {"Fire Support"})
		missionCommands.addSubMenuForGroup(Mission[N].FO_id, "Fire Support")
		missionCommands.addSubMenuForGroup(Mission[N].FO_id, "Enter MGRS Northing (3 digit)", {"Fire Support"})
		missionCommands.addCommandForGroup(Mission[N].FO_id, "Cancel Grid Entry", {"Fire Support"}, TargetLocationMenu, nil)
		missionCommands.addCommandForGroup(Mission[N].FO_id, "Cancel Call For Fire", {"Fire Support"}, FO_EndFireMission, N)
		
		for n1 = 1, 10 do
			if n1 == 10 then
				n1 = 0
			end
			missionCommands.addSubMenuForGroup(Mission[N].FO_id, n1, {"Fire Support", "Enter MGRS Northing (3 digit)"})
			
			for n2 = 1, 10 do
				if n2 == 10 then
					n2 = 0
				end
				missionCommands.addSubMenuForGroup(Mission[N].FO_id, n2, {"Fire Support", "Enter MGRS Northing (3 digit)", n1})
				
				for n3 = 1, 10 do
					if n3 == 10 then
						n3 = 0
					end
					
					MGRS.Easting = tonumber(MGRS.e1 .. MGRS.e2 .. MGRS.e3 .. 0 .. 0)
					MGRS.Northing = tonumber(n1 .. n2 .. n3 .. 0 .. 0)
					local lat, lon = coord.MGRStoLL(MGRS)										--target coordinates in lat-lon
					local point = coord.LLtoLO(lat, lon)										--target position as vec3
					local MGRS6 = MGRS.MGRSDigraph .. " " .. MGRS.e1 .. MGRS.e2 .. MGRS.e3 .. " " .. n1 .. n2 .. n3		--simplified MGRS grid to 100m precision
					missionCommands.addCommandForGroup(Mission[N].FO_id, n3, {"Fire Support", "Enter MGRS Northing (3 digit)", n1, n2}, FO_TransmitTargetLocation, {N, point, MGRS6})
				end
			end
		end
	end
	
	local function InsertMGRS_Easting(MGRS)												--popuate the radio menu to enter the MGRS Easting Coordinates
		Mission[N].idle = timer.getTime() + 180
		trigger.action.outTextForUnit(Unit.getByName(Mission[N].FO_name):getID(), "Manual Grid Entry: " .. MGRS.MGRSDigraph .. " ...", 3)
		missionCommands.removeItemForGroup(Mission[N].FO_id, {"Fire Support"})
		missionCommands.addSubMenuForGroup(Mission[N].FO_id, "Fire Support")
		missionCommands.addSubMenuForGroup(Mission[N].FO_id, "Enter MGRS Easting (3 digit)", {"Fire Support"})
		missionCommands.addCommandForGroup(Mission[N].FO_id, "Cancel Grid Entry", {"Fire Support"}, TargetLocationMenu, nil)
		missionCommands.addCommandForGroup(Mission[N].FO_id, "Cancel Call For Fire", {"Fire Support"}, FO_EndFireMission, N)
		
		for e1 = 1, 10 do
			if e1 == 10 then
				e1 = 0
			end
			missionCommands.addSubMenuForGroup(Mission[N].FO_id, e1, {"Fire Support", "Enter MGRS Easting (3 digit)"})
			
			for e2 = 1, 10 do
				if e2 == 10 then
					e2 = 0
				end
				missionCommands.addSubMenuForGroup(Mission[N].FO_id, e2, {"Fire Support", "Enter MGRS Easting (3 digit)", e1})
				
				for e3 = 1, 10 do
					if e3 == 10 then
						e3 = 0
					end
					local MGRS_copy = {
						UTMZone = MGRS.UTMZone, 
						MGRSDigraph = MGRS.MGRSDigraph,
						e1 = e1,
						e2 = e2,
						e3 = e3,
					}
					missionCommands.addCommandForGroup(Mission[N].FO_id, e3, {"Fire Support", "Enter MGRS Easting (3 digit)", e1, e2}, InsertMGRS_Northing, MGRS_copy)
				end
			end
		end
	end
	
	local function StartGridEntry()													--populate the radio menu to enter the MGRSDigraph (100km grid) of the target
		Mission[N].idle = timer.getTime() + 180
		missionCommands.addSubMenuForGroup(Mission[N].FO_id, "Manual Grid Entry", {"Fire Support", "Transmit Target Location"})
		--find the nine 100km grids around the FO
		local GridTable = {}														--table to store the details of the nine 100km grids around the FO			
		local point = Unit.getByName(Mission[N].FO_name):getPoint()					--current position of FO						
		local lat, lon = coord.LOtoLL(point)										--convert position to lat-lon coordinates
		local MGRS = coord.LLtoMGRS(lat, lon)										--convert position to MGRS grid
		
		for n1 = -1, 1 do															--get the 100 km grids to the south, center and north of FO
			local northing_mod = MGRS.Northing + n1 * 100000						--modify MGRS Northing with -100 km, 0 and +100 km
			for n2 = -1, 1 do														--get the 100 km grids to the weast, center and east of FO
				local grid															--to store the 100 km grid name ("AB" etc.). 9 iterations total
				for dist = 100000, 0, -10000 do										--distance to modify the MGRS Easting. Due to earth curviture, some 100 km grids are skipped on the longitudinal axis. Distance between the grids is therefore lowered until we have found the next adjecent grid.
					local MGRS_mod = {												--to store the full MGRS coordinates of the next grid
						UTMZone = MGRS.UTMZone,
						MGRSDigraph = MGRS.MGRSDigraph,
						Easting = MGRS.Easting + n2 * dist,							--modify MGRS Easting with distance variable to the west (-), center (0) and east (+)
						Northing = northing_mod,									--take the modified northing which we have already done above
					}
					local lat_mod, lon_mod = coord.MGRStoLL(MGRS_mod)				--convert modified MGRS to lat-lon
					MGRS_mod = coord.LLtoMGRS(lat_mod, lon_mod)						--convert the modified MGRS back to MGRS (this will update the UTMZone and MGRSDigrap to the actual values)
									
					if MGRS_mod.UTMZone == MGRS.UTMZone then						--if the UTMZone of the modified MGRS is the same as the original MGRS
						if dist == 100000 then										--this is the first try with the full 100 km distance
							grid = {												--this is the new 100 km grid we seek
								UTMZone = MGRS_mod.UTMZone, 
								MGRSDigraph = MGRS_mod.MGRSDigraph,
							}
						end
						break														--do not check lower distances
					end
					grid = {														--if the UTMZone is different, store the 100 km grid and continue to check with lower distances. If then a lower distances raches the same UTMZone, then the previous 100 km grid will be used.
						UTMZone = MGRS_mod.UTMZone, 
						MGRSDigraph = MGRS_mod.MGRSDigraph,
					}		
				end
				
				if #GridTable == 0 or GridTable[#GridTable].MGRSDigraph ~= grid.MGRSDigraph then				--100 km grid is not the same as the last one (can happen when operating extremely close to UTMZone boundaries)
					table.insert(GridTable, grid)									--insert 100 km grid
				end
			end
		end
		
		for g = 1, #GridTable do
			missionCommands.addCommandForGroup(Mission[N].FO_id, GridTable[g].MGRSDigraph, {"Fire Support", "Transmit Target Location", "Manual Grid Entry"}, InsertMGRS_Easting, GridTable[g])
		end
	end

	----- Main Menu -----
	function TargetLocationMenu()
		missionCommands.removeItemForGroup(Mission[N].FO_id, "Fire Support")
		missionCommands.addSubMenuForGroup(Mission[N].FO_id, "Fire Support")
		missionCommands.addSubMenuForGroup(Mission[N].FO_id, "Transmit Target Location", {"Fire Support"})
		missionCommands.addCommandForGroup(Mission[N].FO_id, "Cancel Call For Fire", {"Fire Support"}, FO_EndFireMission, N)
		StartMarkEntry()
		StartGridEntry()
	end
	TargetLocationMenu()
	
	----- FOR DEBUG -----
	--local point = trigger.misc.getZone('TestZone').point
	--local lat, lon = coord.LOtoLL(point)										--target coordinates
	--local MGRS = coord.LLtoMGRS(lat, lon)										--target MGRS grid
	--local MGRS6 = MGRS.MGRSDigraph .. " " .. math.floor(MGRS.Easting / 100) .. " " .. math.floor(MGRS.Northing / 100)	--simplified MGRS grid to 100m precision
	--missionCommands.addCommandForGroup(Mission[N].FO_id, "DEBUG: " .. MGRS6, {"Fire Support", "Transmit Target Location"}, FO_TransmitTargetLocation, {N, point, MGRS6})
end

----- Call for Fire Part 1 (observer identification and warning order) -----
local function FS_AcknowledgeFireMission(arg)
	local FO_name = arg[1]
	local FO_callsign = Unit.getByName(arg[1]):getCallsign()
	local a,b = string.find(FO_callsign, "%d%d")
	FO_callsign = string.sub(FO_callsign, 1, a - 1) .. " " .. string.sub(FO_callsign, a, a) .. "-" .. string.sub(FO_callsign, b, b)		--put callsign "Enfield11" into format "Enfield 1-1"
	local FS_name = arg[2]
	local FS_callsign = FS[arg[2]].callsign
	local coalition = Unit.getByName(arg[1]):getCoalition()
	local MissionType = arg[3]
	
	if Group.getByName(FS_name) and Group.getByName(FS_name):getUnit(1):isActive() then
		if FS[FS_name].status then
			trigger.action.outTextForCoalition(coalition, FS_callsign .. ": " .. FO_callsign .. " this is " .. FS_callsign .. ", negative, mission in progress, out.", 15)
			trigger.action.outSoundForCoalition(coalition, SoundFilename)
		elseif ReturnArtilleryAmmo(FS_name) == 0 then
			trigger.action.outTextForCoalition(coalition, FS_callsign .. ": " .. FO_callsign .. " this is " .. FS_callsign .. ", negative, out of ammo, out.", 15)
			trigger.action.outSoundForCoalition(coalition, SoundFilename)
		else
			local N = #Mission + 1
			Mission[N] = {
				idle = timer.getTime() + 180,
				FO_name = FO_name,
				FO_callsign = FO_callsign,
				FO_id = Unit.getByName(FO_name):getGroup():getID(),
				FS_name = FS_name,
				FS_callsign = FS_callsign,
				MissionType = MissionType,
				coalition = coalition,
			}
			FS[FS_name].status = "request"
			FO_DetermineTargetLoction(N)
			trigger.action.outTextForCoalition(coalition, FS_callsign .. ": " .. FO_callsign .. " this is " .. FS_callsign .. ", " .. MissionType .. ", out.", 15)
			trigger.action.outSoundForCoalition(coalition, SoundFilename)
		end
	else
		trigger.action.outTextForCoalition(coalition, FS_callsign .. ": " .. FO_callsign .. " this is " .. FS_callsign .. ", negative, unit out of action, out.", 15)
		trigger.action.outSoundForCoalition(coalition, SoundFilename)
	end
end

local function FO_CallFireMission(arg)
	local FO_callsign = Unit.getByName(arg[1]):getCallsign()
	local a,b = string.find(FO_callsign, "%d%d")
	FO_callsign = string.sub(FO_callsign, 1, a - 1) .. " " .. string.sub(FO_callsign, a, a) .. "-" .. string.sub(FO_callsign, b, b)		--put callsign "Enfield11" into format "Enfield 1-1"
	local FS_callsign = FS[arg[2]].callsign
	local coalition = Unit.getByName(arg[1]):getCoalition()
	local MissionType = arg[3]
	
	trigger.action.outTextForCoalition(coalition, FO_callsign .. ": " .. FS_callsign .. " this is " .. FO_callsign .. ", " .. MissionType .. ", over.", 15)
	trigger.action.outSoundForCoalition(coalition, SoundFilename)
	timer.scheduleFunction(FS_AcknowledgeFireMission, arg, timer.getTime() + 5)
end


----- Initialize Radiomenu -----
function PopulateFreshRadioMenu(FO_name)
	if Unit.getByName(FO_name) then
		missionCommands.removeItemForGroup(FO[FO_name].id, "Fire Support")
		missionCommands.addSubMenuForGroup(FO[FO_name].id, "Fire Support")
		
		for FS_name,v in pairs(FS) do
			if Group.getByName(FS_name) and Group.getByName(FS_name):getCoalition() == Unit.getByName(FO_name):getCoalition() then
				missionCommands.addSubMenuForGroup(FO[FO_name].id, v.callsign, {"Fire Support"})
				missionCommands.addCommandForGroup(FO[FO_name].id, "Call for Adjust Fire Mission", {"Fire Support", v.callsign}, FO_CallFireMission, {FO_name, FS_name, "adjust fire"})
				missionCommands.addCommandForGroup(FO[FO_name].id, "Call for Fire For Effect Mission", {"Fire Support", v.callsign}, FO_CallFireMission, {FO_name, FS_name, "fire for effect"})
			end
		end
	end
end

local function FO_CheckActive()
	for FO_name,v in pairs(FO) do
		if Unit.getByName(FO_name) and v.active == nil then
			v.active = true
			v.id = Unit.getByName(FO_name):getGroup():getID()
			PopulateFreshRadioMenu(FO_name)
		elseif Unit.getByName(FO_name) == nil then
			v.active = nil
		end
	end
	return timer.getTime() + 1
end
timer.scheduleFunction(FO_CheckActive, nil, timer.getTime() + 2)


----- Loop to check if a fire mission is idle for too long -----
local function CheckIdleLoop()
	for N = 1, #Mission do
		if Mission[N].idle and timer.getTime() > Mission[N].idle then
			Mission[N].idle = nil
			PopulateFreshRadioMenu(Mission[N].FO_name)
			FS[Mission[N].FS_name].status = nil
			FS[Mission[N].FS_name].mission = nil
			if Group.getByName(Mission[N].FS_name) then
				Group.getByName(Mission[N].FS_name):getController():resetTask()	--reset task
			end
			trigger.action.outTextForCoalition(Mission[N].coalition, Mission[N].FS_callsign .. ": End mission, out.", 10)
			trigger.action.outSoundForCoalition(Mission[N].coalition, SoundFilename)
		end
	end
	return timer.getTime() + 60
end
timer.scheduleFunction(CheckIdleLoop, nil, timer.getTime() + 30)