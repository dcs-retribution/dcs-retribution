--[[
Pretense Dynamic Mission Engine
## Description:

Pretense Dynamic Mission Engine (PDME) is a the heart and soul of the Pretense missions.
You are allowed to use and modify this script for personal or private use.
Please do not share modified versions of this script.
Please do not reupload missions that use this script.
Please do not charge money for access to missions using this script.

## Links:

ED Forums Post: <https://forum.dcs.world/topic/327483-pretense-dynamic-campaign>

Pretense Manual: <https://github.com/Dzsek/pretense>

If you'd like to buy me a beer: <https://www.buymeacoffee.com/dzsek>

Makes use of Mission scripting tools (Mist): <https://github.com/mrSkortch/MissionScriptingTools>

@script PDME
@author Dzsekeb

]]--

-----------------[[ Config.lua ]]-----------------

Config = Config or {}
Config.lossCompensation = Config.lossCompensation or 1.1 -- gives advantage to the side with less zones. Set to 0 to disable
Config.randomBoost = Config.randomBoost or 0.0004 -- adds a random factor to build speeds that changes every 30 minutes, set to 0 to disable
Config.buildSpeed = Config.buildSpeed or 10 -- structure and defense build speed
Config.supplyBuildSpeed = Config.supplyBuildSpeed or 85 -- supply helicopters and convoys build speed
Config.missionBuildSpeedReduction = Config.missionBuildSpeedReduction or 0.12 -- reduction of build speed in case of ai missions
Config.maxDistFromFront = Config.maxDistFromFront or 129640 -- max distance in meters from front after which zone is forced into low activity state (export mode)

Config.missions = Config.missions or {}

-----------------[[ END OF Config.lua ]]-----------------



-----------------[[ Utils.lua ]]-----------------

Utils = {}
do
	local JSON = (loadfile('Scripts/JSON.lua'))()

	function Utils.getPointOnSurface(point)
		return {x = point.x, y = land.getHeight({x = point.x, y = point.z}), z= point.z}
	end
	
	function Utils.getTableSize(tbl)
		local cnt = 0
		for i,v in pairs(tbl) do cnt=cnt+1 end
		return cnt
	end

	Utils.cache = {}
	Utils.cache.groups = {}
	function Utils.getOriginalGroup(groupName)
		if Utils.cache.groups[groupName] then
			return Utils.cache.groups[groupName]
		end

		for _,coalition in pairs(env.mission.coalition) do
			for _,country in pairs(coalition.country) do
				local tocheck = {}
				table.insert(tocheck, country.plane)
				table.insert(tocheck, country.helicopter)
				table.insert(tocheck, country.ship)
				table.insert(tocheck, country.vehicle)
				table.insert(tocheck, country.static)

				for _, checkGroup in ipairs(tocheck) do
					for _,item in pairs(checkGroup.group) do
						Utils.cache.groups[item.name] = item
						if item.name == groupName then
							return item
						end
					end
				end
			end
		end
	end
	
	function Utils.getBearing(fromvec, tovec)
		local fx = fromvec.x
		local fy = fromvec.z
		
		local tx = tovec.x
		local ty = tovec.z
		
		local brg = math.atan2(ty - fy, tx - fx)
		
		
		if brg < 0 then
			 brg = brg + 2 * math.pi
		end
		
		brg = brg * 180 / math.pi
		

		return brg
	end

	function Utils.getHeadingDiff(heading1, heading2) -- heading1 + result == heading2
		local diff = heading1 - heading2
		local absDiff = math.abs(diff)
		local complementaryAngle = 360 - absDiff
	
		if absDiff <= 180 then 
			return -diff
		elseif heading1 > heading2 then
			return complementaryAngle
		else
			return -complementaryAngle
		end
	end
	
	function Utils.getAGL(object)
		local pt = object:getPoint()
		return pt.y - land.getHeight({ x = pt.x, y = pt.z })
	end

	function Utils.round(number)
		return math.floor(number+0.5)
	end
	
	function Utils.isLanded(unit, ignorespeed)
		--return (Utils.getAGL(unit)<5 and mist.vec.mag(unit:getVelocity())<0.10)
		
		if ignorespeed then
			return not unit:inAir()
		else
			return (not unit:inAir() and mist.vec.mag(unit:getVelocity())<1)
		end
	end
	
	function Utils.isGroupActive(group)
		if group and group:getSize()>0 and group:getController():hasTask() then 
			return not Utils.allGroupIsLanded(group, true)
		else
			return false
		end
	end
	
	function Utils.isInAir(unit)
		--return Utils.getAGL(unit)>5
		return unit:inAir()
	end
	
	function Utils.isInZone(unit, zonename)
		local zn = CustomZone:getByName(zonename)
		if zn then
			return zn:isInside(unit:getPosition().p)
		end
		
		return false
	end
	
	function Utils.isCrateSettledInZone(crate, zonename)
		local zn = CustomZone:getByName(zonename)
		if zn and crate then
			return (zn:isInside(crate:getPosition().p) and Utils.getAGL(crate)<1)
		end
		
		return false
	end
	
	function Utils.someOfGroupInZone(group, zonename)
		for i,v in pairs(group:getUnits()) do
			if Utils.isInZone(v, zonename) then
				return true
			end
		end
		
		return false
	end
	
	function Utils.allGroupIsLanded(group, ignorespeed)
		for i,v in pairs(group:getUnits()) do
			if not Utils.isLanded(v, ignorespeed) then
				return false
			end
		end
		
		return true
	end
	
	function Utils.someOfGroupInAir(group)
		for i,v in pairs(group:getUnits()) do
			if Utils.isInAir(v) then
				return true
			end
		end
		
		return false
	end
	
	Utils.canAccessFS = true
	function Utils.saveTable(filename, data)
		if not Utils.canAccessFS then 
			return
		end
		
		if not io then
			Utils.canAccessFS = false
			trigger.action.outText('Persistance disabled', 30)
			return
		end
	
		local str = JSON:encode(data)
		-- local str = 'return (function() local tbl = {}'
		-- for i,v in pairs(data) do
		-- 	str = str..'\ntbl[\''..i..'\'] = '..Utils.serializeValue(v)
		-- end
		
		-- str = str..'\nreturn tbl end)()'
	
		local File = io.open(filename, "w")
		File:write(str)
		File:close()
	end
	
	function Utils.serializeValue(value)
		local res = ''
		if type(value)=='number' or type(value)=='boolean' then
			res = res..tostring(value)
		elseif type(value)=='string' then
			res = res..'\''..value..'\''
		elseif type(value)=='table' then
			res = res..'{ '
			for i,v in pairs(value) do
				if type(i)=='number' then
					res = res..'['..i..']='..Utils.serializeValue(v)..','
				else
					res = res..'[\''..i..'\']='..Utils.serializeValue(v)..','
				end
			end
			res = res:sub(1,-2)
			res = res..' }'
		end
		return res
	end
	
	function Utils.loadTable(filename)
		if not Utils.canAccessFS then 
			return
		end
		
		if not lfs then
			Utils.canAccessFS = false
			trigger.action.outText('Persistance disabled', 30)
			return
		end
		
		if lfs.attributes(filename) then
			local File = io.open(filename, "r")
			local str = File:read('*all')
			File:close()

			return JSON:decode(str)
		end
	end
	
	function Utils.merge(table1, table2)
		local result = {}
		for i,v in pairs(table1) do
			result[i] = v
		end
		
		for i,v in pairs(table2) do
			result[i] = v
		end
		
		return result
	end

	function Utils.log(func)
		return function(p1,p2,p3,p4,p5,p6,p7,p8,p9,p10)
			local err, msg = pcall(func,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10)
			if not err then
				env.info("ERROR - callFunc\n"..msg)
				env.info('Traceback\n'..debug.traceback())
			end
		end
	end
end



-----------------[[ END OF Utils.lua ]]-----------------



-----------------[[ MenuRegistry.lua ]]-----------------

MenuRegistry = {}

do
    MenuRegistry.menus = {}
    function MenuRegistry:register(order, registerfunction, context)
        for i=1,order,1 do
            if not MenuRegistry.menus[i] then MenuRegistry.menus[i] = {func = function() end, context = {}} end
        end

        MenuRegistry.menus[order] = {func = registerfunction, context = context}
    end

    local ev = {}
    function ev:onEvent(event)
        if event.id == world.event.S_EVENT_BIRTH and event.initiator and event.initiator.getPlayerName then
            local player = event.initiator:getPlayerName()
            if player then
                env.info('MenuRegistry - creating menus for player: '..player)
                for i,v in ipairs(MenuRegistry.menus) do
                    local err, msg = pcall(v.func, event, v.context)
                    if not err then
                        env.info("MenuRegistry - ERROR :\n"..msg)
                        env.info('Traceback\n'..debug.traceback())
                    end
                end
            end
        end
    end
    
    world.addEventHandler(ev)


    function MenuRegistry.showTargetZoneMenu(groupid, name, action, targetside, minDistToFront)
        local executeAction = function(act, params)
			local err = act(params)
			if not err then
				missionCommands.removeItemForGroup(params.groupid, params.menu)
			end
		end
	
		local menu = missionCommands.addSubMenuForGroup(groupid, name)
		local sub1 = nil
		local zones = ZoneCommand.getAllZones()

        local zns = {}
        for i,v in pairs(zones) do
            if not targetside or v.side == targetside then 
                if not minDistToFront or v.distToFront <= minDistToFront then
                    table.insert(zns, v)
                end
            end
        end

        table.sort(zns, function(a,b) return a.name < b.name end)

		local count = 0
		for i,v in ipairs(zns) do
            count = count + 1
            if count<10 then
                missionCommands.addCommandForGroup(groupid, v.name, menu, executeAction, action, {zone = v, menu=menu, groupid=groupid})
            elseif count==10 then
                sub1 = missionCommands.addSubMenuForGroup(groupid, "More", menu)
                missionCommands.addCommandForGroup(groupid, v.name, sub1, executeAction, action, {zone = v, menu=menu, groupid=groupid})
            elseif count%9==1 then
                sub1 = missionCommands.addSubMenuForGroup(groupid, "More", sub1)
                missionCommands.addCommandForGroup(groupid, v.name, sub1, executeAction, action, {zone = v, menu=menu, groupid=groupid})
            else
                missionCommands.addCommandForGroup(groupid, v.name, sub1, executeAction, action, {zone = v, menu=menu, groupid=groupid})
            end
		end
		
		return menu
    end
end

-----------------[[ END OF MenuRegistry.lua ]]-----------------



-----------------[[ CustomZone.lua ]]-----------------


CustomZone = {}
do
	function CustomZone:getByName(name)
		local obj = {}
		obj.name = name
		
		local zd = nil
		for _,v in ipairs(env.mission.triggers.zones) do
			if v.name == name then
				zd = v
				break
			end
		end
		
		if not zd then
			return nil
		end
		
		obj.type = zd.type -- 2 == quad, 0 == circle
		if obj.type == 2 then
			obj.vertices = {}
			for _,v in ipairs(zd.verticies) do
				local vertex = {
					x = v.x,
					y = 0,
					z = v.y
				}
				table.insert(obj.vertices, vertex)
			end
		end
		
		obj.radius = zd.radius
		obj.point = {
			x = zd.x,
			y = 0,
			z = zd.y
		}
		
		setmetatable(obj, self)
		self.__index = self
		return obj
	end
	
	function CustomZone:isQuad()
		return self.type==2
	end
	
	function CustomZone:isCircle()
		return self.type==0
	end
	
	function CustomZone:isInside(point)
		if self:isCircle() then
			local dist = mist.utils.get2DDist(point, self.point)
			return dist<self.radius
		elseif self:isQuad() then
			return mist.pointInPolygon(point, self.vertices)
		end
	end
	
	function CustomZone:draw(id, border, background)
		if self:isCircle() then
			trigger.action.circleToAll(-1,id,self.point, self.radius,border,background,1)
		elseif self:isQuad() then
			trigger.action.quadToAll(-1,id,self.vertices[4], self.vertices[3], self.vertices[2], self.vertices[1],border,background,1)
		end
	end
	
	function CustomZone:getRandomSpawnZone()
		local spawnZones = {}
		for i=1,100,1 do
			local zname = self.name..'-'..i
			if trigger.misc.getZone(zname) then
				table.insert(spawnZones, zname)
			else
				break
			end
		end
		
		if #spawnZones == 0 then return nil end
		
		local choice = math.random(1, #spawnZones)
		return spawnZones[choice]
	end
	
	function CustomZone:spawnGroup(product)
		local spname = self.name
		local spawnzone = nil
		
		if not spawnzone then
			spawnzone = self:getRandomSpawnZone()
		end
		
		if spawnzone then
			spname = spawnzone
		end
		
		local pnt = mist.getRandomPointInZone(spname)
		for i=1,500,1 do
			if land.getSurfaceType(pnt) == land.SurfaceType.LAND then
				break
			end

			pnt = mist.getRandomPointInZone(spname)
		end

		local newgr = Spawner.createObject(product.name, product.template, pnt, product.side, nil, nil, nil, spname)

		return newgr
	end
end






-----------------[[ END OF CustomZone.lua ]]-----------------



-----------------[[ GroupMonitor.lua ]]-----------------

GroupMonitor = {}
do
	GroupMonitor.blockedDespawnTime = 10*60 --used to despawn aircraft that are stuck taxiing for some reason
	GroupMonitor.landedDespawnTime = 10
	GroupMonitor.atDestinationDespawnTime = 2*60
	GroupMonitor.recoveryReduction = 0.8 -- reduce recovered resource from landed missions by this amount to account for maintenance

	GroupMonitor.siegeExplosiveTime = 5*60 -- how long until random upgrade is detonated in zone
	GroupMonitor.siegeExplosiveStrength = 1000 -- detonation strength

	function GroupMonitor:new(connectionManager)
		local obj = {}
		obj.groups = {}
		obj.connectionManager = connectionManager
		setmetatable(obj, self)
		self.__index = self
		
		obj:start()
		return obj
	end

	function GroupMonitor.isAirAttack(misType)
		if misType == ZoneCommand.missionTypes.cas then return true end
		if misType == ZoneCommand.missionTypes.cas_helo then return true end
		if misType == ZoneCommand.missionTypes.strike then return true end
		if misType == ZoneCommand.missionTypes.patrol then return true end
		if misType == ZoneCommand.missionTypes.sead then return true end
		if misType == ZoneCommand.missionTypes.bai then return true end
	end

	function GroupMonitor.hasWeapons(group)
		for _,un in ipairs(group:getUnits()) do
			local wps = un:getAmmo()
			if wps then
				for _,w in ipairs(wps) do
					if w.desc.category ~= 0 and w.count > 0 then
						return true
					end
				end
			end
		end
	end

	function GroupMonitor:sendHome(trackedGroup)
		if trackedGroup.home == nil then 
			env.info("GroupMonitor - sendHome "..trackedGroup.name..' does not have home set')
			return
		end

		if trackedGroup.returning then return end


		local gr = Group.getByName(trackedGroup.name)
		if gr then
			if trackedGroup.product.missionType == ZoneCommand.missionTypes.cas_helo then
				local hsp = trigger.misc.getZone(trackedGroup.home.name..'-hsp')
				if not hsp then
					hsp = trigger.misc.getZone(trackedGroup.home.name)
				end

				local alt = self.connectionManager:getHeliAlt(trackedGroup.target.name, trackedGroup.home.name)
				TaskExtensions.landAtPointFromAir(gr, {x=hsp.point.x, y=hsp.point.z}, alt)
			else
				local homeZn = trigger.misc.getZone(trackedGroup.home.name)
				TaskExtensions.landAtAirfield(gr, {x=homeZn.point.x, y=homeZn.point.z})
			end
			
			local cnt = gr:getController()
			cnt:setOption(0,4) -- force ai hold fire
			cnt:setOption(1, 4) -- force reaction on threat to allow abort
			
			trackedGroup.returning = true
			env.info('GroupMonitor - sendHome ['..trackedGroup.name..'] returning home')
		end
	end
	
	function GroupMonitor:registerGroup(product, target, home, savedData)
		self.groups[product.name] = {name = product.name, lastStateTime = timer.getAbsTime(), product = product, target = target, home = home}

		if savedData and savedData.state ~= 'uninitialized' then
			env.info('GroupMonitor - registerGroup ['..product.name..'] restored state '..savedData.state..' dur:'..savedData.lastStateDuration)
			self.groups[product.name].state = savedData.state
			self.groups[product.name].lastStateTime = timer.getAbsTime() - savedData.lastStateDuration
		end
	end
	
	function GroupMonitor:start()
		timer.scheduleFunction(function(param, time)
			local self = param.context
			
			for i,v in pairs(self.groups) do
				local isDead = false
				if v.product.missionType == 'supply_convoy' or v.product.missionType == 'assault' then
					isDead = self:processSurface(v)
					if isDead then 
						MissionTargetRegistry.removeBaiTarget(v) --safety measure in case group is dead
					end
				else
					isDead = self:processAir(v)
				end
				
				if isDead then
					self.groups[i] = nil
				end
			end
			
			return time+10
		end, {context = self}, timer.getTime()+1)
	end

	function GroupMonitor:getGroup(name)
		return self.groups[name]
	end
	
	function GroupMonitor:processSurface(group) -- states: [started, enroute, atdestination, siege]
		local gr = Group.getByName(group.name)
		if not gr then return true end
		if gr:getSize()==0 then 
			gr:destroy()
			return true
		end
		
		if not group.state then 
			group.state = 'started'
			lastStateTime = timer.getAbsTime()
			env.info('GroupMonitor: processSurface ['..group.name..'] starting')
		end
		
		if group.state =='started' then
			if gr then
				local firstUnit = gr:getUnit(1):getName()
				local z = ZoneCommand.getZoneOfUnit(firstUnit)
				
				if not z then
					env.info('GroupMonitor: processSurface ['..group.name..'] is enroute')
					group.state = 'enroute'
					group.lastStateTime = timer.getAbsTime()
					MissionTargetRegistry.addBaiTarget(group)
				elseif timer.getAbsTime() - group.lastStateTime > GroupMonitor.blockedDespawnTime then
					env.info('GroupMonitor: processSurface ['..group.name..'] despawned due to blockage')
					gr:destroy()
					local todeliver = math.floor(group.product.cost)
					z:addResource(todeliver)
					return true
				end
			end
		elseif group.state =='enroute' then
			if gr then
				local firstUnit = gr:getUnit(1):getName()
				local z = ZoneCommand.getZoneOfUnit(firstUnit)
				
				if z and (z.name==group.target.name or z.name==group.home.name) then
					MissionTargetRegistry.removeBaiTarget(group)
					
					if group.product.missionType == 'supply_convoy' then
						env.info('GroupMonitor: processSurface ['..group.name..'] has arrived at destination')
						group.state = 'atdestination'
						group.lastStateTime = timer.getAbsTime()
						z:capture(gr:getCoalition())
						local percentSurvived = gr:getSize()/gr:getInitialSize()
						local todeliver = math.floor(group.product.cost * percentSurvived)
						z:addResource(todeliver)
						env.info('GroupMonitor: processSurface ['..group.name..'] has supplied ['..z.name..'] with ['..todeliver..']')
					elseif group.product.missionType == 'assault' then
						if z.side == gr:getCoalition() then
							env.info('GroupMonitor: processSurface ['..group.name..'] has arrived at destination')
							group.state = 'atdestination'
							group.lastStateTime = timer.getAbsTime()
							local percentSurvived = gr:getSize()/gr:getInitialSize()
							local torecover = math.floor(group.product.cost * percentSurvived * GroupMonitor.recoveryReduction)
							z:addResource(torecover)
							env.info('GroupMonitor: processSurface ['..z.name..'] has recovered ['..torecover..'] from ['..group.name..']')
						elseif z.side == 0 then
							env.info('GroupMonitor: processSurface ['..group.name..'] has arrived at destination')
							group.state = 'atdestination'
							group.lastStateTime = timer.getAbsTime()
							z:capture(gr:getCoalition())
							env.info('GroupMonitor: processSurface ['..group.name..'] has captured ['..z.name..']')
						elseif z.side ~= gr:getCoalition() and z.side ~= 0  then
							env.info('GroupMonitor: processSurface ['..group.name..'] starting siege')
							group.state = 'siege'
							group.lastStateTime = timer.getAbsTime()
						end
					end
				else
					if group.product.missionType == 'supply_convoy' then
						if not group.returning and group.target and group.target.side ~= group.product.side and group.target.side ~= 0 then
							local supplyPoint = trigger.misc.getZone(group.home.name..'-sp')
							if not supplyPoint then
								supplyPoint = trigger.misc.getZone(group.home.name)
							end
	
							if supplyPoint then 
								group.returning = true
								env.info('GroupMonitor: processSurface ['..group.name..'] returning home')
								TaskExtensions.moveOnRoadToPoint(gr,  {x=supplyPoint.point.x, y=supplyPoint.point.z})
							end
						end
					elseif  group.product.missionType == 'assault' then
						local frUnit = gr:getUnit(1)
						if frUnit then
							local controller = frUnit:getController()
							local targets = controller:getDetectedTargets()

							local shouldstop = false
							if #targets > 0 then
								for _,tgt in ipairs(targets) do
									if tgt.visible and tgt.object then
										if tgt.object.getCoalition and tgt.object:getCoalition()~=frUnit:getCoalition() and 
											tgt.object.getCategory and tgt.object:getCategory() == 1 then
											local dist = mist.utils.get3DDist(frUnit:getPoint(), tgt.object:getPoint())
											if dist < 1000 then
												if not group.isstopped then
													env.info('GroupMonitor: processSurface ['..group.name..'] stopping to engage targets')
													--gr:getController():setCommand({id = 'StopRoute', params = { value = true}})
													TaskExtensions.stopAndDisperse(gr)
													group.isstopped = true
												end
												shouldstop = true
												break
											end
										end
									end
								end
							end

							if not shouldstop and group.isstopped then
								env.info('GroupMonitor: processSurface ['..group.name..'] resuming mission')
								--gr:getController():setCommand({id = 'StopRoute', params = { value = false}})
								local tp = {
									x = group.target.zone.point.x,
									y = group.target.zone.point.z
								}

								TaskExtensions.moveOnRoadToPointAndAssault(gr, tp, group.target.built)
								group.isstopped = false
							end
						end
					end
				end
			end
		elseif group.state == 'atdestination' then
			if timer.getAbsTime() - group.lastStateTime > GroupMonitor.atDestinationDespawnTime then
				
				if gr then
					local firstUnit = gr:getUnit(1):getName()
					local z = ZoneCommand.getZoneOfUnit(firstUnit)
					if z and z.side == 0 then
						env.info('GroupMonitor: processSurface ['..group.name..'] is at neutral zone')
						z:capture(gr:getCoalition())
						env.info('GroupMonitor: processSurface ['..group.name..'] has captured ['..z.name..']')
					else
						env.info('GroupMonitor: processSurface ['..group.name..'] starting siege')
						group.state = 'siege'
						group.lastStateTime = timer.getAbsTime()
					end

					env.info('GroupMonitor: processSurface ['..group.name..'] despawned after arriving at destination')
					gr:destroy()
					return true
				end
			end
		elseif group.state == 'siege' then
			if group.product.missionType ~= 'assault' then 
				group.state = 'atdestination'
				group.lastStateTime = timer.getAbsTime()
			else
				if timer.getAbsTime() - group.lastStateTime > GroupMonitor.siegeExplosiveTime then
					if gr then
						local firstUnit = gr:getUnit(1):getName()
						local z = ZoneCommand.getZoneOfUnit(firstUnit)
						local success = false
						
						if z then
							for i,v in pairs(z.built) do
								if v.type == 'upgrade' and v.side ~= gr:getCoalition() then
									local st = StaticObject.getByName(v.name)
									if not st then st = Group.getByName(v.name) end
									local pos = st:getPoint()
									trigger.action.explosion(pos, GroupMonitor.siegeExplosiveStrength)
									group.lastStateTime = timer.getAbsTime()
									success = true
									env.info('GroupMonitor: processSurface ['..group.name..'] detonating structure at '..z.name)
									break
								end
							end
						end

						if not success then
							env.info('GroupMonitor: processSurface ['..group.name..'] no targets to detonate, switching to atdestination')
							group.state = 'atdestination'
							group.lastStateTime = timer.getAbsTime()
						end
					end
				end
			end
		end
	end
	
	function GroupMonitor:processAir(group)-- states: [takeoff, inair, landed]
		local gr = Group.getByName(group.name)
		if not gr then return true end
		if gr:getSize()==0 then 
			gr:destroy()
			return true
		end
		--[[
		if group.product.missionType == 'cas' or group.product.missionType == 'cas_helo' or group.product.missionType == 'strike' or group.product.missionType == 'sead' then
			if MissionTargetRegistry.isZoneTargeted(group.target) and group.product.side == 2 and not group.returning then 
				env.info('GroupMonitor - mission ['..group.name..'] to ['..group.target..'] canceled due to player mission')

				GroupMonitor.sendHome(group)
			end
		end
		]]--
		
		if not group.state then 
			group.state = 'takeoff' 
			env.info('GroupMonitor: processAir ['..group.name..'] taking off')
		end
		
		if group.state =='takeoff' then
			if timer.getAbsTime() - group.lastStateTime > GroupMonitor.blockedDespawnTime then
				if gr and Utils.allGroupIsLanded(gr) then
					env.info('GroupMonitor: processAir ['..group.name..'] is blocked, despawning')
					local frUnit = gr:getUnit(1)
					if frUnit then
						local firstUnit = frUnit:getName()
						local z = ZoneCommand.getZoneOfUnit(firstUnit)
						if z then
							z:addResource(group.product.cost)
							env.info('GroupMonitor: processAir ['..z.name..'] has recovered ['..group.product.cost..'] from ['..group.name..']')
						end
					end

					gr:destroy()
					return true
				end
			elseif gr and Utils.someOfGroupInAir(gr) then
				env.info('GroupMonitor: processAir ['..group.name..'] is in the air')
				group.state = 'inair'
				group.lastStateTime = timer.getAbsTime()
			end
		elseif group.state =='inair' then
			if gr and Utils.allGroupIsLanded(gr) then
				env.info('GroupMonitor: processAir ['..group.name..'] has landed')
				group.state = 'landed'
				group.lastStateTime = timer.getAbsTime()

				local unit = gr:getUnit(1)
				if unit then
					local firstUnit = unit:getName()
					local z = ZoneCommand.getZoneOfUnit(firstUnit)
					
					if group.product.missionType == 'supply_air' then
						if z then
							z:capture(gr:getCoalition())
							z:addResource(group.product.cost)
							env.info('GroupMonitor: processAir ['..group.name..'] has supplied ['..z.name..'] with ['..group.product.cost..']')
						end
					else
						if z and z.side == gr:getCoalition() then
							local percentSurvived = gr:getSize()/gr:getInitialSize()
							local torecover = math.floor(group.product.cost * percentSurvived * GroupMonitor.recoveryReduction)
							z:addResource(torecover)
							env.info('GroupMonitor: processAir ['..z.name..'] has recovered ['..torecover..'] from ['..group.name..']')
						end
					end
				else
					env.info('GroupMonitor: processAir ['..group.name..'] size ['..gr:getSize()..'] has no unit 1')
				end
			elseif gr then
				if GroupMonitor.isAirAttack(group.product.missionType) and not group.returning then
					if not GroupMonitor.hasWeapons(gr) then
						env.info('GroupMonitor: processAir ['..group.name..'] size ['..gr:getSize()..'] has no weapons outside of shells')
						self:sendHome(group)
					elseif group.product.missionType == ZoneCommand.missionTypes.cas_helo then 
						local frUnit = gr:getUnit(1)
						local controller = frUnit:getController()
						local targets = controller:getDetectedTargets()

						local tgtToEngage = {}
						if #targets > 0 then
							for _,tgt in ipairs(targets) do
								if tgt.visible and tgt.object and tgt.object.isExist and tgt.object:isExist() then
									if tgt.object.getCategory and tgt.object:getCategory() == Object.Category.UNIT and 
										tgt.object.getCoalition and tgt.object:getCoalition()~=frUnit:getCoalition() and 
										tgt.object:getDesc().category == Unit.Category.GROUND_UNIT then

										local dist = mist.utils.get3DDist(frUnit:getPoint(), tgt.object:getPoint())
										if dist < 2000 then
											table.insert(tgtToEngage, tgt.object)
										end
									end
								end
							end
						end

						if not group.isengaging and #tgtToEngage > 0 then
							env.info('GroupMonitor: processAir ['..group.name..'] engaging targets')
							TaskExtensions.heloEngageTargets(gr, tgtToEngage, group.product.expend)
							group.isengaging = true
							group.startedEngaging = timer.getAbsTime()
						elseif group.isengaging and #tgtToEngage == 0 and group.startedEngaging and (timer.getAbsTime() - group.startedEngaging) > 60*5 then
							env.info('GroupMonitor: processAir ['..group.name..'] resuming mission')
							if group.returning then
								group.returning = nil
								self:sendHome(group)
							else
								local homePos = group.home.zone.point
								TaskExtensions.executeHeloCasMission(gr, group.target.built, group.product.expend, group.product.altitude, {homePos = homePos})
							end
							group.isengaging = false
						end
					end
				elseif group.product.missionType == 'supply_air' then
					if not group.returning and group.target and group.target.side ~= group.product.side and group.target.side ~= 0 then
						local supplyPoint = trigger.misc.getZone(group.home.name..'-hsp')
						if not supplyPoint then
							supplyPoint = trigger.misc.getZone(group.home.name)
						end

						if supplyPoint then 
							group.returning = true
							local alt = self.connectionManager:getHeliAlt(group.target.name, group.home.name)
							TaskExtensions.landAtPointFromAir(gr,  {x=supplyPoint.point.x, y=supplyPoint.point.z}, alt)
							env.info('GroupMonitor: processAir ['..group.name..'] returning home')
						end
					end
				end
			end
		elseif group.state =='landed' then
			if timer.getAbsTime() - group.lastStateTime > GroupMonitor.landedDespawnTime then
				if gr then
					env.info('GroupMonitor: processAir ['..group.name..'] despawned after landing')
					gr:destroy()
					return true
				end
			end
		end
	end
end

-----------------[[ END OF GroupMonitor.lua ]]-----------------



-----------------[[ ConnectionManager.lua ]]-----------------

ConnectionManager = {}
do
	ConnectionManager.currentLineIndex = 5000
	function ConnectionManager:new()
		local obj = {}
		obj.connections = {}
		obj.zoneConnections = {}
		obj.heliAlts = {}
		obj.blockedRoads = {}
		setmetatable(obj, self)
		self.__index = self
		
		return obj
	end

	function ConnectionManager:addConnection(f, t, blockedRoad, heliAlt)
		local i = ConnectionManager.currentLineIndex
		ConnectionManager.currentLineIndex = ConnectionManager.currentLineIndex + 1
		
		table.insert(self.connections, {from=f, to=t, index=i})
		self.zoneConnections[f] = self.zoneConnections[f] or {}
		self.zoneConnections[t] = self.zoneConnections[t] or {}
		self.zoneConnections[f][t] = true
		self.zoneConnections[t][f] = true
		
		if heliAlt then
			self.heliAlts[f] = self.heliAlts[f] or {}
			self.heliAlts[t] = self.heliAlts[t] or {}
			self.heliAlts[f][t] = heliAlt
			self.heliAlts[t][f] = heliAlt
		end

		if blockedRoad then
			self.blockedRoads[f] = self.blockedRoads[f] or {}
			self.blockedRoads[t] = self.blockedRoads[t] or {}
			self.blockedRoads[f][t] = true
			self.blockedRoads[t][f] = true
		end

		local from = CustomZone:getByName(f)
		local to = CustomZone:getByName(t)

		if not from then env.info("ConnectionManager - addConnection: missing zone "..f) end
		if not to then env.info("ConnectionManager - addConnection: missing zone "..t) end
		
		if blockedRoad then
			trigger.action.lineToAll(-1, i, from.point, to.point, {1,1,1,0.5}, 3)
		else
			trigger.action.lineToAll(-1, i, from.point, to.point, {1,1,1,0.5}, 2)
		end
	end
	
	function ConnectionManager:getConnectionsOfZone(zonename)
		if not self.zoneConnections[zonename] then return {} end
		
		local connections = {}
		for i,v in pairs(self.zoneConnections[zonename]) do
			table.insert(connections, i)
		end
		
		return connections
	end

	function ConnectionManager:isRoadBlocked(f,t)
		if self.blockedRoads[f] then 
			return self.blockedRoads[f][t]
		end

		if self.blockedRoads[t] then 
			return self.blockedRoads[t][f]
		end
	end

	function ConnectionManager:getHeliAltSimple(f,t)
		if self.heliAlts[f] then 
			if self.heliAlts[f][t] then
				return self.heliAlts[f][t]
			end
		end

		if self.heliAlts[t] then 
			if self.heliAlts[t][f] then
				return self.heliAlts[t][f]
			end
		end
	end

	function ConnectionManager:getHeliAlt(f,t)
		local alt = self:getHeliAltSimple(f,t)
		if alt then return alt end

		if self.heliAlts[f] then 
			local max = -1
			for zn,_ in pairs(self.heliAlts[f]) do
				local alt = self:getHeliAltSimple(f, zn)
				if alt then
					if alt > max then
						max = alt
					end
				end

				alt = self:getHeliAltSimple(zn, t)
				if alt then
					if alt > max then
						max = alt
					end
				end
			end
			
			if max > 0 then return max end
		end

		if self.heliAlts[t] then 
			local max = -1
			for zn,_ in pairs(self.heliAlts[t]) do
				local alt = self:getHeliAltSimple(t, zn)
				if alt then
					if alt > max then
						max = alt
					end
				end

				alt = self:getHeliAltSimple(zn, f)
				if alt then
					if alt > max then
						max = alt
					end
				end
			end

			if max > 0 then return max end
		end
	end
end

-----------------[[ END OF ConnectionManager.lua ]]-----------------



-----------------[[ TaskExtensions.lua ]]-----------------

TaskExtensions = {}
do
	function TaskExtensions.getAttackTask(targetName, expend, altitude)
		local tgt = Group.getByName(targetName)
		if tgt then
			return { 
				id = 'AttackGroup', 
				params = { 
					groupId = tgt:getID(),
					expend = expend,
					weaponType = Weapon.flag.AnyWeapon,
					groupAttack = true,
					altitudeEnabled = (altitude ~= nil),
					altitude = altitude
				} 
			}
		else
			tgt = StaticObject.getByName(targetName)
			if not tgt then tgt = Unit.getByName(targetName) end
			if tgt then
				return { 
					id = 'AttackUnit', 
					params = { 
						unitId = tgt:getID(),
						expend = expend,
						weaponType = Weapon.flag.AnyWeapon,
						groupAttack = true,
						altitudeEnabled = (altitude ~= nil),
						altitude = altitude
					} 
				}
			end
		end
	end

	function TaskExtensions.getDefaultWaypoints(startPos, task, tgpos, reactivated)
		local defwp = {
			id='Mission',
			params = {
				route = {
					airborne = true,
					points = {}
				}  
			}
		}

		if reactivated then
			table.insert(defwp.params.route.points, {
				type= AI.Task.WaypointType.TURNING_POINT,
				x = reactivated.currentPos.x,
				y = reactivated.currentPos.z,
				speed = 257,
				action = AI.Task.TurnMethod.FLY_OVER_POINT,
				alt = 4572,
				alt_type = AI.Task.AltitudeType.BARO, 
				task = task
			})
		else
			table.insert(defwp.params.route.points, {
				type= AI.Task.WaypointType.TAKEOFF,
				x = startPos.x,
				y = startPos.z,
				speed = 0,
				action = AI.Task.TurnMethod.FIN_POINT,
				alt = 0,
				alt_type = AI.Task.AltitudeType.RADIO
			})

			table.insert(defwp.params.route.points, {
				type= AI.Task.WaypointType.TURNING_POINT,
				x = startPos.x,
				y = startPos.z,
				speed = 257,
				action = AI.Task.TurnMethod.FLY_OVER_POINT,
				alt = 4572,
				alt_type = AI.Task.AltitudeType.BARO, 
				task = task
			})
		end

		if tgpos then
			table.insert(defwp.params.route.points, {
				type= AI.Task.WaypointType.TURNING_POINT,
				x = tgpos.x,
				y = tgpos.z,
				speed = 257,
				action = AI.Task.TurnMethod.FLY_OVER_POINT,
				alt = 4572,
				alt_type = AI.Task.AltitudeType.BARO,
				task = task
			})
		end

		table.insert(defwp.params.route.points, {
			type= AI.Task.WaypointType.LAND,
			x = startPos.x,
			y = startPos.z,
			speed = 257,
			action = AI.Task.TurnMethod.FIN_POINT,
			alt = 0,
			alt_type = AI.Task.AltitudeType.RADIO
		})

		return defwp
	end

	function TaskExtensions.executeSeadMission(group,targets, expend, altitude, reactivated)
		if not group then return end
		if not group:isExist() or group:getSize()==0 then return end
		local startPos = group:getUnit(1):getPoint()

		if reactivated then
			reactivated.currentPos = startPos
			startPos = reactivated.homePos
		end

		local expCount = AI.Task.WeaponExpend.ALL
		if expend then
			expCount = expend
		end
		
		local alt = 4572
		if altitude then
			alt = altitude/3.281
		end

		local viable = {}
		for i,v in pairs(targets) do
			if v.type == 'defense' and v.side ~= group:getCoalition() then
				local gr = Group.getByName(v.name)
				for _,unit in ipairs(gr:getUnits()) do
					if unit:hasAttribute('SAM SR') or unit:hasAttribute('SAM TR') or unit:hasAttribute('AAA') or unit:hasAttribute('IR Guided SAM') or unit:hasAttribute('SAM LL') then
						table.insert(viable, unit:getName())
					end
				end
			end
		end

		local attack = {
			id = 'ComboTask',
			params = {
				tasks = {
					{ 
						id = 'EngageTargets', 
						params = {  
						  targetTypes = {'SAM SR', 'SAM TR', 'AAA', 'IR Guided SAM', 'SAM LL'}
						} 
					}
				}
			}
		}

		for i,v in ipairs(viable) do
			local task = TaskExtensions.getAttackTask(v, expCount, alt)
			table.insert(attack.params.tasks, task)
		end

		local firstunitpos = nil
		local tgt = viable[1]
		if tgt then 
			firstunitpos = Unit.getByName(tgt):getPoint()
		end
		
		local mis = TaskExtensions.getDefaultWaypoints(startPos, attack, firstunitpos, reactivated)

		group:getController():setTask(mis)
		TaskExtensions.setDefaultAG(group)
	end

	function TaskExtensions.executeStrikeMission(group,targets, expend, altitude, reactivated)
		if not group then return end
		if not group:isExist() or group:getSize()==0 then return end
		local startPos = group:getUnit(1):getPoint()

		if reactivated then
			reactivated.currentPos = startPos
			startPos = reactivated.homePos
		end

		local expCount = AI.Task.WeaponExpend.ALL
		if expend then
			expCount = expend
		end
		
		local alt = 4572
		if altitude then
			alt = altitude/3.281
		end

		local attack = {
			id = 'ComboTask',
			params = {
				tasks = {
				}
			}
		}

		for i,v in pairs(targets) do
			if v.type == 'upgrade' and v.side ~= group:getCoalition() then
				local task = TaskExtensions.getAttackTask(v.name, expCount, alt)
				table.insert(attack.params.tasks, task)
			end
		end

		local mis = TaskExtensions.getDefaultWaypoints(startPos, attack, nil, reactivated)

		group:getController():setTask(mis)
		TaskExtensions.setDefaultAG(group)
	end

	function TaskExtensions.executeCasMission(group, targets, expend, altitude, reactivated)
		if not group then return end
		if not group:isExist() or group:getSize()==0 then return end
		local startPos = group:getUnit(1):getPoint()

		if reactivated then
			reactivated.currentPos = startPos
			startPos = reactivated.homePos
		end

		local attack = {
			id = 'ComboTask',
			params = {
				tasks = {
				}
			}
		}

		local expCount = AI.Task.WeaponExpend.ONE
		if expend then
			expCount = expend
		end
		
		local alt = 4572
		if altitude then
			alt = altitude/3.281
		end

		for i,v in pairs(targets) do
			if v.type == 'defense' then
				local g = Group.getByName(i)
				if g and g:getCoalition()~=group:getCoalition() then
					local task = TaskExtensions.getAttackTask(i, expCount, alt)
					table.insert(attack.params.tasks, task)
				end
			end
		end

		local mis = TaskExtensions.getDefaultWaypoints(startPos, attack, nil, reactivated)

		group:getController():setTask(mis)
		TaskExtensions.setDefaultAG(group)
	end

	function TaskExtensions.executeBaiMission(group, targets, expend, altitude, reactivated)
		if not group then return end
		if not group:isExist() or group:getSize()==0 then return end
		local startPos = group:getUnit(1):getPoint()

		if reactivated then
			reactivated.currentPos = startPos
			startPos = reactivated.homePos
		end

		local attack = {
			id = 'ComboTask',
			params = {
				tasks = {
					{ 
						id = 'EngageTargets', 
						params = {  
						  targetTypes = {'Vehicles'}
						} 
					}
				}
			}
		}

		local expCount = AI.Task.WeaponExpend.ONE
		if expend then
			expCount = expend
		end
		
		local alt = 4572
		if altitude then
			alt = altitude/3.281
		end

		for i,v in pairs(targets) do
			if v.type == 'mission' and (v.missionType == 'assault' or v.missionType == 'supply_convoy') then
				local g = Group.getByName(i)
				if g and g:getSize()>0 and g:getCoalition()~=group:getCoalition() then
					local task = TaskExtensions.getAttackTask(i, expCount, alt)
					table.insert(attack.params.tasks, task)
				end
			end
		end

		local mis = TaskExtensions.getDefaultWaypoints(startPos, attack, nil, reactivated)

		group:getController():setTask(mis)
		TaskExtensions.setDefaultAG(group)
	end

	function TaskExtensions.heloEngageTargets(group, targets, expend)
		if not group then return end
		if not group:isExist() or group:getSize()==0 then return end
		local startPos = group:getUnit(1):getPoint()

		local attack = {
			id = 'ComboTask',
			params = {
				tasks = {
				}
			}
		}

		local expCount = AI.Task.WeaponExpend.ONE
		if expend then
			expCount = expend
		end
		
		for i,v in pairs(targets) do
			local task = { 
				id = 'AttackUnit', 
				params = { 
					unitId = v:getID(),
					expend = expend,
					weaponType = Weapon.flag.AnyWeapon,
					groupAttack = true
				} 
			}

			table.insert(attack.params.tasks, task)
		end

		group:getController():pushTask(attack)
	end

	function TaskExtensions.executeHeloCasMission(group, targets, expend, altitude, reactivated)
		if not group then return end
		if not group:isExist() or group:getSize()==0 then return end
		local startPos = group:getUnit(1):getPoint()

		if reactivated then
			reactivated.currentPos = startPos
			startPos = reactivated.homePos
		end

		local attack = {
			id = 'ComboTask',
			params = {
				tasks = {
				}
			}
		}

		local expCount = AI.Task.WeaponExpend.ONE
		if expend then
			expCount = expend
		end
		
		local alt = 61
		if altitude then
			alt = altitude/3.281
		end

		for i,v in pairs(targets) do
			if v.type == 'defense' then
				local g = Group.getByName(i)
				if g and g:getCoalition()~=group:getCoalition() then
					local task = TaskExtensions.getAttackTask(i, expCount, alt)
					table.insert(attack.params.tasks, task)
				end
			end
		end

		local land = {
			id='Land',
			params = {
				point = {x = startPos.x, y=startPos.z}
			}
		}

		local mis = {
			id='Mission',
			params = {
				route = {
					airborne = true,
					points = {}
				}  
			}
		}

		if reactivated then
			table.insert(mis.params.route.points, {
				type= AI.Task.WaypointType.TURNING_POINT,
				x = reactivated.currentPos.x+1000,
				y = reactivated.currentPos.z+1000,
				speed = 257,
				action = AI.Task.TurnMethod.FLY_OVER_POINT,
				alt = alt,
				alt_type = AI.Task.AltitudeType.RADIO, 
				task = attack
			})
		else
			table.insert(mis.params.route.points, {
				type= AI.Task.WaypointType.TAKEOFF,
				x = startPos.x,
				y = startPos.z,
				speed = 0,
				action = AI.Task.TurnMethod.FIN_POINT,
				alt = 0,
				alt_type = AI.Task.AltitudeType.RADIO,
			})

			table.insert(mis.params.route.points, {
				type= AI.Task.WaypointType.TURNING_POINT,
				x = startPos.x+1000,
				y = startPos.z+1000,
				speed = 257,
				action = AI.Task.TurnMethod.FLY_OVER_POINT,
				alt = alt,
				alt_type = AI.Task.AltitudeType.RADIO, 
				task = attack
			})
		end

		table.insert(mis.params.route.points, {
			type= AI.Task.WaypointType.TURNING_POINT,
			x = startPos.x,
			y = startPos.z,
			speed = 257,
			action = AI.Task.TurnMethod.FIN_POINT,
			alt = alt,
			alt_type = AI.Task.AltitudeType.RADIO, 
			task = land
		})
		
		group:getController():setTask(mis)
		TaskExtensions.setDefaultAG(group)
	end

	function TaskExtensions.executeTankerMission(group, point, altitude, frequency, tacan, reactivated)
		if not group then return end
		if not group:isExist() or group:getSize()==0 then return end
		local startPos = group:getUnit(1):getPoint()
		if reactivated then
			reactivated.currentPos = startPos
			startPos = reactivated.homePos
		end
		
		local alt = 4572
		if altitude then
			alt = altitude/3.281
		end

		local freq = 259500000
		if frequency then
			freq = math.floor(frequency*1000000)
		end

		local setfreq = {
			id = 'SetFrequency', 
			params = { 
				frequency = freq,
				modulation = 0
			} 
		}

		local setbeacon = {
			id = 'ActivateBeacon', 
			params = { 
				type = 4, -- TACAN type
				system = 4, -- Tanker TACAN
				name = 'tacan task', 
				callsign = group:getUnit(1):getCallsign():sub(1,3), 
				frequency = tacan
			} 
		}

		local distFromPoint = 20000
		local theta = math.random() * 2 * math.pi
  
		local dx = distFromPoint * math.cos(theta)
		local dy = distFromPoint * math.sin(theta)

		local pos1 = {
			x = point.x + dx,
			y = point.z + dy
		}

		local pos2 = {
			x = point.x - dx,
			y = point.z - dy
		}

		local orbit = { 
			id = 'Orbit', 
			params = { 
				pattern = AI.Task.OrbitPattern.RACE_TRACK,
				point = pos1,
   				point2 = pos2,
				speed = 195,
				altitude = alt
			}
		}

		local script = {
			id = "WrappedAction",
			params = {
				action = {
					id = "Script",
					params = 
					{
						command = "trigger.action.outTextForCoalition("..group:getCoalition()..", 'Tanker on station. "..(freq/1000000).." AM', 15)",
					}
				}
			}
		}

		local tanker = {
			id = 'Tanker', 
			params = { 
			}
		}

		local task = {
			id='Mission',
			params = {
				route = {
					airborne = true,
					points = {}
				}
			}
		}

		if reactivated then
			table.insert(task.params.route.points, {
				type= AI.Task.WaypointType.TURNING_POINT,
				x = pos1.x,
				y = pos1.y,
				speed = 450,
				action = AI.Task.TurnMethod.FLY_OVER_POINT,
				alt = alt,
				alt_type = AI.Task.AltitudeType.BARO,
				task = tanker
			})
		else
			table.insert(task.params.route.points, {
				type= AI.Task.WaypointType.TAKEOFF,
				x = startPos.x,
				y = startPos.z,
				speed = 0,
				action = AI.Task.TurnMethod.FIN_POINT,
				alt = 0,
				alt_type = AI.Task.AltitudeType.RADIO,
				task = tanker
			})
		end

		table.insert(task.params.route.points, {
			type= AI.Task.WaypointType.TURNING_POINT,
			x = pos1.x,
			y = pos1.y,
			speed = 195,
			action = AI.Task.TurnMethod.FLY_OVER_POINT,
			alt = alt,
			alt_type = AI.Task.AltitudeType.BARO,
			task = {
				id = 'ComboTask',
				params = {
					tasks = {
						script
					}
				}
			}
		})

		table.insert(task.params.route.points, {
			type= AI.Task.WaypointType.TURNING_POINT,
			x = pos2.x,
			y = pos2.y,
			speed = 195,
			action = AI.Task.TurnMethod.FLY_OVER_POINT,
			alt = alt,
			alt_type = AI.Task.AltitudeType.BARO,
			task = {
				id = 'ComboTask',
				params = {
					tasks = {
						orbit
					}
				}
			}
		})

		table.insert(task.params.route.points, {
			type= AI.Task.WaypointType.LAND,
			x = startPos.x,
			y = startPos.z,
			speed = 450,
			action = AI.Task.TurnMethod.FIN_POINT,
			alt = 0,
			alt_type = AI.Task.AltitudeType.RADIO
		})
		
		group:getController():setTask(task)
		group:getController():setOption(AI.Option.Air.id.REACTION_ON_THREAT, AI.Option.Air.val.REACTION_ON_THREAT.PASSIVE_DEFENCE)
		group:getController():setCommand(setfreq)
		group:getController():setCommand(setbeacon)
	end

	function TaskExtensions.executeAwacsMission(group, point, altitude, frequency, reactivated)
		if not group then return end
		if not group:isExist() or group:getSize()==0 then return end
		local startPos = group:getUnit(1):getPoint()
		if reactivated then
			reactivated.currentPos = startPos
			startPos = reactivated.homePos
		end
		
		local alt = 4572
		if altitude then
			alt = altitude/3.281
		end

		local freq = 259500000
		if frequency then
			freq = math.floor(frequency*1000000)
		end

		local setfreq = {
			id = 'SetFrequency', 
			params = { 
				frequency = freq,
				modulation = 0
			} 
		}

		local distFromPoint = 10000
		local theta = math.random() * 2 * math.pi
  
		local dx = distFromPoint * math.cos(theta)
		local dy = distFromPoint * math.sin(theta)

		local pos1 = {
			x = point.x + dx,
			y = point.z + dy
		}

		local pos2 = {
			x = point.x - dx,
			y = point.z - dy
		}

		local orbit = { 
			id = 'Orbit', 
			params = { 
				pattern = AI.Task.OrbitPattern.RACE_TRACK,
				point = pos1,
   				point2 = pos2,
				altitude = alt
			}
		}

		local script = {
			id = "WrappedAction",
			params = {
				action = {
					id = "Script",
					params = 
					{
						command = "trigger.action.outTextForCoalition("..group:getCoalition()..", 'AWACS on station. "..(freq/1000000).." AM', 15)",
					}
				}
			}
		}

		local awacs = {
			id = 'AWACS', 
			params = { 
			}
		}

		local task = {
			id='Mission',
			params = {
				route = {
					airborne = true,
					points = {}
				}  
			}
		}

		if reactivated then
			table.insert(task.params.route.points, {
				type= AI.Task.WaypointType.TURNING_POINT,
				x = pos1.x,
				y = pos1.y,
				speed = 257,
				action = AI.Task.TurnMethod.FLY_OVER_POINT,
				alt = alt,
				alt_type = AI.Task.AltitudeType.BARO,
				task = awacs
			})
		else
			table.insert(task.params.route.points, {
				type= AI.Task.WaypointType.TAKEOFF,
				x = startPos.x,
				y = startPos.z,
				speed = 0,
				action = AI.Task.TurnMethod.FIN_POINT,
				alt = 0,
				alt_type = AI.Task.AltitudeType.RADIO,
				task = awacs
			})
		end
			
		table.insert(task.params.route.points, {
			type= AI.Task.WaypointType.TURNING_POINT,
			x = pos1.x,
			y = pos1.y,
			speed = 257,
			action = AI.Task.TurnMethod.FLY_OVER_POINT,
			alt = alt,
			alt_type = AI.Task.AltitudeType.BARO,
			task = {
				id = 'ComboTask',
				params = {
					tasks = {
						script
					}
				}
			}
		})

		table.insert(task.params.route.points, {
			type= AI.Task.WaypointType.TURNING_POINT,
			x = pos2.x,
			y = pos2.y,
			speed = 257,
			action = AI.Task.TurnMethod.FLY_OVER_POINT,
			alt = alt,
			alt_type = AI.Task.AltitudeType.BARO,
			task = {
				id = 'ComboTask',
				params = {
					tasks = {
						orbit
					}
				}
			}
		})

		table.insert(task.params.route.points, {
			type= AI.Task.WaypointType.LAND,
			x = startPos.x,
			y = startPos.z,
			speed = 257,
			action = AI.Task.TurnMethod.FIN_POINT,
			alt = 0,
			alt_type = AI.Task.AltitudeType.RADIO
		})
		
		group:getController():setTask(task)
		group:getController():setOption(AI.Option.Air.id.REACTION_ON_THREAT, AI.Option.Air.val.REACTION_ON_THREAT.PASSIVE_DEFENCE)
		group:getController():setCommand(setfreq)
	end
	
	function TaskExtensions.executePatrolMission(group, point, altitude, range, reactivated)
		if not group then return end
		if not group:isExist() or group:getSize()==0 then return end
		local startPos = group:getUnit(1):getPoint()

		if reactivated then
			reactivated.currentPos = startPos
			startPos = reactivated.homePos
		end

		local rng = 25 * 1852
		if range then
			rng = range * 1852
		end
		
		local alt = 4572
		if altitude then
			alt = altitude/3.281
		end

		local search = { 
			id = 'EngageTargets',
			params = {
				maxDist = rng,
				targetTypes = { 'Planes', 'Helicopters' }
			} 
		}

		local distFromPoint = 10000
		local theta = math.random() * 2 * math.pi
  
		local dx = distFromPoint * math.cos(theta)
		local dy = distFromPoint * math.sin(theta)

		local p1 = {
			x = point.x + dx,
			y = point.z + dy
		}

		local p2 = {
			x = point.x - dx,
			y = point.z - dy
		}

		local orbit = {
			id = 'Orbit',
			params = {
				pattern = AI.Task.OrbitPattern.RACE_TRACK,
				point = p1,
				point2 = p2,
				speed = 154,
				altitude = alt
			}
		}

		local task = {
			id='Mission',
			params = {
				route = {
					airborne = true,
					points = {}
				}  
			}
		}

		if not reactivated then
			table.insert(task.params.route.points, {
				type= AI.Task.WaypointType.TAKEOFF,
				x = startPos.x,
				y = startPos.z,
				speed = 0,
				action = AI.Task.TurnMethod.FIN_POINT,
				alt = 0,
				alt_type = AI.Task.AltitudeType.RADIO,
				task = search
			})
		else
			table.insert(task.params.route.points, {
				type= AI.Task.WaypointType.TURNING_POINT,
				x = reactivated.currentPos.x,
				y = reactivated.currentPos.z,
				speed = 257,
				action = AI.Task.TurnMethod.FIN_POINT,
				alt = alt,
				alt_type = AI.Task.AltitudeType.BARO,
				task = search
			})
		end

		table.insert(task.params.route.points, {
			type= AI.Task.WaypointType.TURNING_POINT,
			x = p1.x,
			y = p1.y,
			speed = 257,
			action = AI.Task.TurnMethod.FLY_OVER_POINT,
			alt = alt,
			alt_type = AI.Task.AltitudeType.BARO
		})

		table.insert(task.params.route.points, {
			type= AI.Task.WaypointType.TURNING_POINT,
			x = p2.x,
			y = p2.y,
			speed = 257,
			action = AI.Task.TurnMethod.FLY_OVER_POINT,
			alt = alt,
			alt_type = AI.Task.AltitudeType.BARO,
			task = orbit
		})

		table.insert(task.params.route.points, {
			type= AI.Task.WaypointType.LAND,
			x = startPos.x,
			y = startPos.z,
			speed = 257,
			action = AI.Task.TurnMethod.FIN_POINT,
			alt = 0,
			alt_type = AI.Task.AltitudeType.RADIO
		})
		
		group:getController():setTask(task)
		TaskExtensions.setDefaultAA(group)
	end

	function TaskExtensions.setDefaultAA(group)
		group:getController():setOption(AI.Option.Air.id.PROHIBIT_AG, true)
		group:getController():setOption(AI.Option.Air.id.JETT_TANKS_IF_EMPTY, true)
		group:getController():setOption(AI.Option.Air.id.PROHIBIT_JETT, true)
		group:getController():setOption(AI.Option.Air.id.REACTION_ON_THREAT, AI.Option.Air.val.REACTION_ON_THREAT.EVADE_FIRE)
		group:getController():setOption(AI.Option.Air.id.MISSILE_ATTACK, AI.Option.Air.val.MISSILE_ATTACK.MAX_RANGE)

		local weapons = 268402688  -- AnyMissile
		group:getController():setOption(AI.Option.Air.id.RTB_ON_OUT_OF_AMMO, weapons)
	end

	function TaskExtensions.setDefaultAG(group)
		--group:getController():setOption(AI.Option.Air.id.PROHIBIT_AA, true)
		group:getController():setOption(AI.Option.Air.id.JETT_TANKS_IF_EMPTY, true)
		group:getController():setOption(AI.Option.Air.id.PROHIBIT_JETT, true)
		group:getController():setOption(AI.Option.Air.id.REACTION_ON_THREAT, AI.Option.Air.val.REACTION_ON_THREAT.EVADE_FIRE)

		local weapons = 2147485694 + 30720 + 4161536 -- AnyBomb + AnyRocket + AnyASM
		group:getController():setOption(AI.Option.Air.id.RTB_ON_OUT_OF_AMMO, weapons)
	end

	function TaskExtensions.stopAndDisperse(group)
		if not group then return end
		if not group:isExist() or group:getSize()==0 then return end
		local pos = group:getUnit(1):getPoint()
		group:getController():setTask({
			id='Mission',
			params = {
				route = {
					points = {
						[1] = {
							type= AI.Task.WaypointType.TURNING_POINT,
							x = pos.x,
							y = pos.z,
							speed = 1000,
							action = AI.Task.VehicleFormation.OFF_ROAD
						},
						[2] = {
							type= AI.Task.WaypointType.TURNING_POINT,
							x = pos.x+math.random(25),
							y = pos.z+math.random(25),
							speed = 1000,
							action = AI.Task.VehicleFormation.DIAMOND
						},
					}
				}  
			}
        })
	end

	function TaskExtensions.moveOnRoadToPointAndAssault(group, point, targets)
		if not group or not point then return end
		if not group:isExist() or group:getSize()==0 then return end
		local startPos = group:getUnit(1):getPoint()

		local srx, sry = land.getClosestPointOnRoads('roads', startPos.x, startPos.z)
		local erx, ery = land.getClosestPointOnRoads('roads', point.x, point.y)

		local mis = {
			id='Mission',
			params = {
				route = {
					points = {
						[1] = {
							type= AI.Task.WaypointType.TURNING_POINT,
							x = srx,
							y = sry,
							speed = 1000,
							action = AI.Task.VehicleFormation.ON_ROAD
						},
						[2] = {
							type= AI.Task.WaypointType.TURNING_POINT,
							x = erx,
							y = ery,
							speed = 1000,
							action = AI.Task.VehicleFormation.ON_ROAD
						},
						[3] = {
							type= AI.Task.WaypointType.TURNING_POINT,
							x = point.x,
							y = point.y,
							speed = 1000,
							action = AI.Task.VehicleFormation.DIAMOND
						}
					}
				}  
			}
		}

		for i,v in pairs(targets) do
			if v.type == 'defense' then
				local group = Group.getByName(v.name)
				if group then
					for i,v in ipairs(group:getUnits()) do
						local unpos = v:getPoint()
						local pnt = {x=unpos.x, y = unpos.z}
	
						table.insert(mis.params.route.points, {
							type= AI.Task.WaypointType.TURNING_POINT,
							x = pnt.x,
							y = pnt.y,
							speed = 10,
							action = AI.Task.VehicleFormation.DIAMOND
						})
					end
				end
			end
		end
		group:getController():setTask(mis)
	end
	
	function TaskExtensions.moveOnRoadToPoint(group, point) -- point = {x,y}
		if not group or not point then return end
		if not group:isExist() or group:getSize()==0 then return end
		local startPos = group:getUnit(1):getPoint()
		
		local srx, sry = land.getClosestPointOnRoads('roads', startPos.x, startPos.z)
		local erx, ery = land.getClosestPointOnRoads('roads', point.x, point.y)

		local mis = {
			id='Mission',
			params = {
				route = {
					points = {
						[1] = {
							type= AI.Task.WaypointType.TURNING_POINT,
							x = srx,
							y = sry,
							speed = 1000,
							action = AI.Task.VehicleFormation.ON_ROAD
						},
						[2] = {
							type= AI.Task.WaypointType.TURNING_POINT,
							x = erx,
							y = ery,
							speed = 1000,
							action = AI.Task.VehicleFormation.ON_ROAD
						},
						[3] = {
							type= AI.Task.WaypointType.TURNING_POINT,
							x = point.x,
							y = point.y,
							speed = 1000,
							action = AI.Task.VehicleFormation.OFF_ROAD
						}
					}
				}  
			}
		}
		group:getController():setTask(mis)
	end
	
	function TaskExtensions.landAtPointFromAir(group, point, alt)
		if not group or not point then return end
		if not group:isExist() or group:getSize()==0 then return end
		local startPos = group:getUnit(1):getPoint()

		local atype = AI.Task.AltitudeType.RADIO
		if alt then
			atype = AI.Task.AltitudeType.BARO
		else
			alt = 500
		end

		local land = {
			id='Land',
			params = {
				point = point
			}
		}
		
		local mis = {
			id='Mission',
			params = {
				route = {
					airborne = true,
					points = {
						[1] = {
							type= AI.Task.WaypointType.TURNING_POINT,
							x = startPos.x,
							y = startPos.z,
							speed = 500,
							action = AI.Task.TurnMethod.FIN_POINT,
							alt = alt,
							alt_type = atype
						},
						[2] = {
							type= AI.Task.WaypointType.TURNING_POINT,
							x = point.x,
							y = point.y,
							speed = 257,
							action = AI.Task.TurnMethod.FIN_POINT,
							alt = alt,
							alt_type = atype, 
							task = land
						}
					}
				}  
			}
		}
		
		group:getController():setTask(mis)
	end

	function TaskExtensions.landAtPoint(group, point, alt) -- point = {x,y}
		if not group or not point then return end
		if not group:isExist() or group:getSize()==0 then return end
		local startPos = group:getUnit(1):getPoint()

		local atype = AI.Task.AltitudeType.RADIO
		if alt then
			atype = AI.Task.AltitudeType.BARO
		else
			alt = 500
		end
		
		local land = {
			id='Land',
			params = {
				point = point
			}
		}

		local mis = {
			id='Mission',
			params = {
				route = {
					airborne = true,
					points = {
						[1] = {
							type = AI.Task.WaypointType.TAKEOFF,
							x = startPos.x,
							y = startPos.z,
							speed = 0,
							action = AI.Task.TurnMethod.FIN_POINT,
							alt = alt,
							alt_type = atype
						},
						[2] = {
							type = AI.Task.WaypointType.TURNING_POINT,
							x = point.x,
							y = point.y,
							speed = 257,
							action = AI.Task.TurnMethod.FIN_POINT,
							alt = alt,
							alt_type = atype, 
							task = land
						}
					}
				}  
			}
		}
		
		group:getController():setTask(mis)
	end

	function TaskExtensions.landAtAirfield(group, point) -- point = {x,y}
		if not group or not point then return end
		if not group:isExist() or group:getSize()==0 then return end
		
		local mis = {
			id='Mission',
			params = {
				route = {
					airborne = true,
					points = {
						[1] = {
							type= AI.Task.WaypointType.TURNING_POINT,
							x = point.x,
							y = point.z,
							speed = 257,
							action = AI.Task.TurnMethod.FIN_POINT,
							alt = 4572,
							alt_type = AI.Task.AltitudeType.BARO
						},
						[2] = {
							type= AI.Task.WaypointType.LAND,
							x = point.x,
							y = point.z,
							speed = 257,
							action = AI.Task.TurnMethod.FIN_POINT,
							alt = 0,
							alt_type = AI.Task.AltitudeType.RADIO
						}
					}
				}  
			}
		}
		
		group:getController():setTask(mis)
	end
end

-----------------[[ END OF TaskExtensions.lua ]]-----------------



-----------------[[ PlayerLogistics.lua ]]-----------------

PlayerLogistics = {}
do
	PlayerLogistics.allowedTypes = {}
	PlayerLogistics.allowedTypes['Mi-24P'] = { supplies = true, personCapacity = 8 }
	PlayerLogistics.allowedTypes['Mi-8MT'] = { supplies = true, personCapacity = 24 }
	PlayerLogistics.allowedTypes['UH-1H'] = { supplies = true, personCapacity = 12}
	PlayerLogistics.allowedTypes['Hercules'] = { supplies = true, personCapacity = 92 }
	PlayerLogistics.allowedTypes['UH-60L'] = { supplies = true, personCapacity = 12 }
	PlayerLogistics.allowedTypes['Ka-50'] = { supplies = false }
	PlayerLogistics.allowedTypes['Ka-50_3'] = { supplies = false }
	PlayerLogistics.allowedTypes['SA342L'] = { supplies = false, personCapacity = 2}
	PlayerLogistics.allowedTypes['SA342M'] = { supplies = false, personCapacity = 2}
	PlayerLogistics.allowedTypes['SA342Minigun'] = { supplies = false, personCapacity = 2}
	PlayerLogistics.allowedTypes['AH-64D_BLK_II'] = { supplies = false }

	PlayerLogistics.infantryTypes = {
		capture = 'capture',
		sabotage = 'sabotage',
		ambush = 'ambush',
		engineer = 'engineer',
		manpads = 'manpads',
		spy = 'spy',
		rapier = 'rapier',
		extractable = 'extractable'
	}

	function PlayerLogistics.getInfantryName(infType)
		if infType==PlayerLogistics.infantryTypes.capture then
			return "Capture Squad"
		elseif infType==PlayerLogistics.infantryTypes.sabotage then
			return "Sabotage Squad"
		elseif infType==PlayerLogistics.infantryTypes.ambush then
			return "Ambush Squad"
		elseif infType==PlayerLogistics.infantryTypes.engineer then
			return "Engineer"
		elseif infType==PlayerLogistics.infantryTypes.manpads then
			return "MANPADS"
		elseif infType==PlayerLogistics.infantryTypes.spy then
			return "Spy"
		elseif infType==PlayerLogistics.infantryTypes.rapier then
			return "Rapier SAM"
		elseif infType==PlayerLogistics.infantryTypes.extractable then
			return "Extracted infantry"
		end

		return "INVALID SQUAD"
	end
	
	function PlayerLogistics:new(misTracker, plyTracker, squadTracker, csarTracker)
		local obj = {}
		obj.groupMenus = {} -- groupid = path
		obj.carriedCargo = {} -- groupid = source
		obj.carriedInfantry = {} -- groupid = source
		obj.carriedPilots = {} --groupid = source
		obj.registeredSquadGroups = {}
		obj.lastLoaded = {} -- groupid = zonename
		obj.missionTracker = misTracker
		obj.playerTracker = plyTracker
		obj.squadTracker = squadTracker
		obj.csarTracker = csarTracker

		obj.hercTracker = {
			cargos = {},
			cargoCheckFunctions = {}
		}

		obj.hercPreparedDrops = {}
		
		setmetatable(obj, self)
		self.__index = self
		
		obj:start()
		
		return obj
	end

	function PlayerLogistics:registerSquadGroup(squadType, groupname, weight, cost, jobtime, extracttime, squadSize)
		self.registeredSquadGroups[squadType] = { name=groupname, type=squadType, weight=weight, cost=cost, jobtime=jobtime, extracttime=extracttime, size = squadSize}
	end
	
	function PlayerLogistics:start()
		if not ZoneCommand then return end
	
        MenuRegistry:register(3, function(event, context)
			if event.id == world.event.S_EVENT_BIRTH and event.initiator and event.initiator.getPlayerName then
				local player = event.initiator:getPlayerName()
				if player then
					local unitType = event.initiator:getDesc()['typeName']
					local groupid = event.initiator:getGroup():getID()
					local groupname = event.initiator:getGroup():getName()
					
					local logistics = context.allowedTypes[unitType]
					if logistics and (logistics.supplies or logistics.personCapacity)then

						if context.groupMenus[groupid] then
							missionCommands.removeItemForGroup(groupid, context.groupMenus[groupid])
							context.groupMenus[groupid] = nil
						end

						if not context.groupMenus[groupid] then
							local size = event.initiator:getGroup():getSize()
							if size > 1 then
								trigger.action.outText('WARNING: group '..groupname..' has '..size..' units. Logistics will only function for group leader', 10)
							end
							
							local cargomenu = missionCommands.addSubMenuForGroup(groupid, 'Logistics')
							if logistics.supplies then
								local supplyMenu = missionCommands.addSubMenuForGroup(groupid, 'Supplies', cargomenu)
								local loadMenu = missionCommands.addSubMenuForGroup(groupid, 'Load', supplyMenu)
								missionCommands.addCommandForGroup(groupid, 'Load 100 supplies', loadMenu, Utils.log(context.loadSupplies), context, {group=groupname, amount=100})
								missionCommands.addCommandForGroup(groupid, 'Load 500 supplies', loadMenu, Utils.log(context.loadSupplies), context, {group=groupname, amount=500})
								missionCommands.addCommandForGroup(groupid, 'Load 1000 supplies', loadMenu, Utils.log(context.loadSupplies), context, {group=groupname, amount=1000})
								missionCommands.addCommandForGroup(groupid, 'Load 2000 supplies', loadMenu, Utils.log(context.loadSupplies), context, {group=groupname, amount=2000})
								missionCommands.addCommandForGroup(groupid, 'Load 5000 supplies', loadMenu, Utils.log(context.loadSupplies), context, {group=groupname, amount=5000})

								local unloadMenu = missionCommands.addSubMenuForGroup(groupid, 'Unload', supplyMenu)
								missionCommands.addCommandForGroup(groupid, 'Unload 100 supplies', unloadMenu, Utils.log(context.unloadSupplies), context, {group=groupname, amount=100})
								missionCommands.addCommandForGroup(groupid, 'Unload 500 supplies', unloadMenu, Utils.log(context.unloadSupplies), context, {group=groupname, amount=500})
								missionCommands.addCommandForGroup(groupid, 'Unload 1000 supplies', unloadMenu, Utils.log(context.unloadSupplies), context, {group=groupname, amount=1000})
								missionCommands.addCommandForGroup(groupid, 'Unload 2000 supplies', unloadMenu, Utils.log(context.unloadSupplies), context, {group=groupname, amount=2000})
								missionCommands.addCommandForGroup(groupid, 'Unload 5000 supplies', unloadMenu, Utils.log(context.unloadSupplies), context, {group=groupname, amount=5000})
								missionCommands.addCommandForGroup(groupid, 'Unload all supplies', unloadMenu, Utils.log(context.unloadSupplies), context, {group=groupname, amount=9999999})
							end

							local sqs = {}
							for sqType,_ in pairs(context.registeredSquadGroups) do
								table.insert(sqs,sqType)
							end
							table.sort(sqs)

							if logistics.personCapacity then
								local infMenu = missionCommands.addSubMenuForGroup(groupid, 'Infantry', cargomenu)
								
								local loadInfMenu = missionCommands.addSubMenuForGroup(groupid, 'Load', infMenu)
								for _,sqType in ipairs(sqs) do
									local menuName =  'Load '..PlayerLogistics.getInfantryName(sqType)
									missionCommands.addCommandForGroup(groupid, menuName, loadInfMenu, Utils.log(context.loadInfantry), context, {group=groupname, type=sqType})
								end

								local unloadInfMenu = missionCommands.addSubMenuForGroup(groupid, 'Unload', infMenu)
								for _,sqType in ipairs(sqs) do
									local menuName =  'Unload '..PlayerLogistics.getInfantryName(sqType)
									missionCommands.addCommandForGroup(groupid, menuName, unloadInfMenu, Utils.log(context.unloadInfantry), context, {group=groupname, type=sqType})
								end
								missionCommands.addCommandForGroup(groupid, 'Unload Extracted squad', unloadInfMenu, Utils.log(context.unloadInfantry), context, {group=groupname, type=PlayerLogistics.infantryTypes.extractable})

								missionCommands.addCommandForGroup(groupid, 'Extract squad', infMenu, Utils.log(context.extractSquad), context, groupname)
								missionCommands.addCommandForGroup(groupid, 'Unload all', infMenu, Utils.log(context.unloadInfantry), context, {group=groupname})

								local csarMenu = missionCommands.addSubMenuForGroup(groupid, 'CSAR', cargomenu)
								missionCommands.addCommandForGroup(groupid, 'Show info (closest)', csarMenu, Utils.log(context.showPilot), context, groupname)
								missionCommands.addCommandForGroup(groupid, 'Smoke marker (closest)', csarMenu, Utils.log(context.smokePilot), context, groupname)
								missionCommands.addCommandForGroup(groupid, 'Flare (closest)', csarMenu, Utils.log(context.flarePilot), context, groupname)
								missionCommands.addCommandForGroup(groupid, 'Extract pilot', csarMenu, Utils.log(context.extractPilot), context, groupname)
								missionCommands.addCommandForGroup(groupid, 'Unload pilots', csarMenu, Utils.log(context.unloadPilots), context, groupname)
							end

							missionCommands.addCommandForGroup(groupid, 'Cargo status', cargomenu, Utils.log(context.cargoStatus), context, groupname)
							missionCommands.addCommandForGroup(groupid, 'Unload Everything', cargomenu, Utils.log(context.unloadAll), context, groupname)
							
							if unitType == 'Hercules' then
								local loadmasterMenu = missionCommands.addSubMenuForGroup(groupid, 'Loadmaster', cargomenu)

								for _,sqType in ipairs(sqs) do
									local menuName =  'Prepare '..PlayerLogistics.getInfantryName(sqType)
									missionCommands.addCommandForGroup(groupid, menuName, loadmasterMenu, Utils.log(context.hercPrepareDrop), context, {group=groupname, type=sqType})
								end

								missionCommands.addCommandForGroup(groupid, 'Prepare Supplies', loadmasterMenu, Utils.log(context.hercPrepareDrop), context, {group=groupname, type='supplies'})
							end
							
							
							context.groupMenus[groupid] = cargomenu
						end
						
						if context.carriedCargo[groupid] then
							context.carriedCargo[groupid] = 0
						end

						if context.carriedInfantry[groupid] then
							context.carriedInfantry[groupid] = {}
						end

						if context.carriedPilots[groupid] then
							context.carriedPilots[groupid] = {}
						end

						if context.lastLoaded[groupid] then
							context.lastLoaded[groupid] = nil
						end

						if context.hercPreparedDrops[groupid] then
							context.hercPreparedDrops[groupid] = nil
						end
					end
				end
			elseif (event.id == world.event.S_EVENT_PLAYER_LEAVE_UNIT or event.id == world.event.S_EVENT_DEAD) and event.initiator and event.initiator.getPlayerName then
                local player = event.initiator:getPlayerName()
				if player then
					local groupid = event.initiator:getGroup():getID()
					
					if context.groupMenus[groupid] then
						missionCommands.removeItemForGroup(groupid, context.groupMenus[groupid])
						context.groupMenus[groupid] = nil
					end
				end
            end
		end, self)

		local ev = {}
		ev.context = self
		function ev:onEvent(event)
			if event.id == world.event.S_EVENT_SHOT and event.initiator and event.initiator:isExist() then
				local unitName = event.initiator:getName()
				local groupId = event.initiator:getGroup():getID()
				local name = event.weapon:getDesc().typeName
				if name == 'weapons.bombs.Generic Crate [20000lb]' then
					local prepared = self.context.hercPreparedDrops[groupId]

					if not prepared then
						prepared = 'supplies'
								
						if self.context.carriedInfantry[groupId] then
							for _,v in ipairs(self.context.carriedInfantry[groupId]) do
								if v.type ~= PlayerLogistics.infantryTypes.extractable then
									prepared = v.type
									break
								end
							end
						end

						env.info('PlayerLogistics - Hercules - auto preparing '..prepared)
					end

					if prepared then
						if prepared == 'supplies' then
							env.info('PlayerLogistics - Hercules - supplies getting dropped')
							local carried = self.context.carriedCargo[groupId]
							local amount = 0
							if carried and carried > 0 then
								amount = 9000
								if carried < amount then
									amount = carried
								end
							end
							
							if amount > 0 then
								self.context.carriedCargo[groupId] = math.max(0,self.context.carriedCargo[groupId] - amount)
								if not self.context.hercTracker.cargos[unitName] then
									self.context.hercTracker.cargos[unitName] = {}
								end
								
								table.insert(self.context.hercTracker.cargos[unitName],{
									object = event.weapon,
									supply = amount,
									lastLoaded = self.context.lastLoaded[groupId],
									unit = event.initiator
								})
								
								env.info('PlayerLogistics - Hercules - '..unitName..'deployed crate with '..amount..' supplies')
								self.context:processHercCargos(unitName)
								self.context.hercPreparedDrops[groupId] = nil
								trigger.action.outTextForUnit(event.initiator:getID(), 'Crate with '..amount..' supplies deployed', 10)
							else
								trigger.action.outTextForUnit(event.initiator:getID(), 'Empty crate deployed', 10)
							end
						else
							env.info('PlayerLogistics - Hercules - searching for prepared infantry')
							local toDrop = nil
							local remaining = {}
							if self.context.carriedInfantry[groupId] then
								for _,v in ipairs(self.context.carriedInfantry[groupId]) do
									if v.type == prepared and toDrop == nil then
										toDrop = v
									else
										table.insert(remaining, v)
									end
								end
							end
							
							
							if toDrop then
								env.info('PlayerLogistics - Hercules - dropping '..toDrop.type)
								if not self.context.hercTracker.cargos[unitName] then
									self.context.hercTracker.cargos[unitName] = {}
								end
								
								table.insert(self.context.hercTracker.cargos[unitName],{
									object = event.weapon,
									squad = toDrop,
									lastLoaded = self.context.lastLoaded[groupId],
									unit = event.initiator
								})
								
								env.info('PlayerLogistics - Hercules - '..unitName..'deployed crate with '..toDrop.type)
								self.context:processHercCargos(unitName)
								self.context.hercPreparedDrops[groupId] = nil
								
								local squadName = PlayerLogistics.getInfantryName(prepared)
								trigger.action.outTextForUnit(event.initiator:getID(), squadName..' crate deployed.', 10)
								self.context.carriedInfantry[groupId] = remaining
								local weight = self.context:getCarriedPersonWeight(event.initiator:getGroup():getName())
								trigger.action.setUnitInternalCargo(event.initiator:getName(), weight)
							else
								trigger.action.outTextForUnit(event.initiator:getID(), 'Empty crate deployed', 10)
							end
						end
					else
						trigger.action.outTextForUnit(event.initiator:getID(), 'Empty crate deployed', 10)
					end
				end
			end
		end
		
		world.addEventHandler(ev)
	end

	function PlayerLogistics:processHercCargos(unitName)
		if not self.hercTracker.cargoCheckFunctions[unitName] then
			env.info('PlayerLogistics - Hercules - start tracking cargos of '..unitName)
			self.hercTracker.cargoCheckFunctions[unitName] = timer.scheduleFunction(function(params, time)
				local reschedule = params.context:checkHercCargo(params.unitName, time)
				if not reschedule then
					params.context.hercTracker.cargoCheckFunctions[params.unitName] = nil
				end
				
				return reschedule
			end, {unitName=unitName, context = self}, timer.getTime() + 0.1)
		end
	end

	function PlayerLogistics:checkHercCargo(unitName, time)
		local cargos = self.hercTracker.cargos[unitName]
		if cargos and #cargos > 0 then
			local remaining = {}
			for _,cargo in ipairs(cargos) do
				if cargo.object and cargo.object:isExist() then
					local alt = Utils.getAGL(cargo.object)
					if alt < 5 then
						self:deliverHercCargo(cargo)
					else
						table.insert(remaining, cargo)
					end
				else
					env.info('PlayerLogistics - Hercules - cargo crashed')
					if cargo.unit and cargo.unit:isExist() then
						trigger.action.outTextForUnit(cargo.unit:getID(), 'Cargo drop of '..cargo.unit:getPlayerName()..' crashed', 10)
					end
				end
			end

			if #remaining > 0 then
				self.hercTracker.cargos[unitName] = remaining
				return time + 0.1
			end
		end
	end

	function PlayerLogistics:deliverHercCargo(cargo)
		if cargo.object and cargo.object:isExist() then
			if cargo.supply then
				local zone = ZoneCommand.getZoneOfWeapon(cargo.object)
				if zone then
					zone:addResource(cargo.supply)
					cargo.object:destroy()
					env.info('PlayerLogistics - Hercules - '..cargo.supply..' delivered to '..zone.name)

					self:awardSupplyXP(cargo.lastLoaded, zone, cargo.unit, cargo.supply)
				end
			elseif cargo.squad then
				local pos = Utils.getPointOnSurface(cargo.object:getPoint())
				local surface = land.getSurfaceType(pos)
				if surface == land.SurfaceType.LAND or surface == land.SurfaceType.ROAD or surface == land.SurfaceType.RUNWAY then
					local zn = ZoneCommand.getZoneOfPoint(pos)
					
					local lastLoad = cargo.squad.loadedAt
					if lastLoad and zn and zn.side == cargo.object:getCoalition() and zn.name==lastLoad.name then
						if self.registeredSquadGroups[cargo.squad.type] then
							local cost = self.registeredSquadGroups[cargo.squad.type].cost
							zn:addResource(cost)
							zn:refreshText()
							if cargo.unit and cargo.unit:isExist() then
								local squadName = PlayerLogistics.getInfantryName(cargo.squad.type)
								trigger.action.outTextForUnit(cargo.unit:getID(), squadName..' unloaded', 10)
							end
						end
					else
						local error = self.squadTracker:spawnInfantry(self.registeredSquadGroups[cargo.squad.type], pos)
						if not error then
							cargo.object:destroy()
							env.info('PlayerLogistics - Hercules - '..cargo.squad.type..' deployed')
							
							local squadName = PlayerLogistics.getInfantryName(cargo.squad.type)
							trigger.action.outTextForUnit(cargo.unit:getID(), squadName..' deployed', 10)
							
							if cargo.unit and cargo.unit:isExist() and cargo.unit.getPlayerName then
								local player = cargo.unit:getPlayerName()
								local xp = RewardDefinitions.actions.squadDeploy
								
								self.playerTracker:addStat(player, math.floor(xp), PlayerTracker.statTypes.xp)
								
								if zn then
									self.missionTracker:tallyUnloadSquad(player, zn.name, cargo.squad.type)
								else
									self.missionTracker:tallyUnloadSquad(player, '', cargo.squad.type)
								end
								trigger.action.outTextForUnit(cargo.unit:getID(), '+'..math.floor(xp)..' XP', 10)
							end
						end
					end
				end
			end
		end
	end

	function PlayerLogistics:hercPrepareDrop(params)
		local groupname = params.group
		local type = params.type
		local gr = Group.getByName(groupname)
		if gr then
			local un = gr:getUnit(1)

			if type == 'supplies' then
				local cargo = self.carriedCargo[gr:getID()]
				if cargo and cargo > 0 then
					self.hercPreparedDrops[gr:getID()] = type
					trigger.action.outTextForUnit(un:getID(), 'Supply drop prepared', 10)
				else
					trigger.action.outTextForUnit(un:getID(), 'No supplies onboard the aircraft', 10)
				end
			else
				local exists = false
				if self.carriedInfantry[gr:getID()] then
					for i,v in ipairs(self.carriedInfantry[gr:getID()]) do
						if v.type == type then
							exists = true
							break
						end
					end
				end
			
				if exists then
					self.hercPreparedDrops[gr:getID()] = type
					local squadName = PlayerLogistics.getInfantryName(type)
					trigger.action.outTextForUnit(un:getID(), squadName..' drop prepared', 10)
				else
					local squadName = PlayerLogistics.getInfantryName(type)
					trigger.action.outTextForUnit(un:getID(), 'No '..squadName..' onboard the aircraft', 10)
				end
			end
		end
	end

	function PlayerLogistics:awardSupplyXP(lastLoad, zone, unit, amount)
		if lastLoad and zone.name~=lastLoad.name then
			if unit and unit.isExist and unit:isExist() and unit.getPlayerName then
				local player = unit:getPlayerName()
				local xp = amount*RewardDefinitions.actions.supplyRatio

				local totalboost = 0
				local dist = mist.utils.get2DDist(lastLoad.zone.point, zone.zone.point)
				if dist > 15000 then
					local extradist = math.max(dist - 15000, 85000)
					local kmboost = extradist/85000
					local actualboost = xp * kmboost * 1
					totalboost = totalboost + actualboost
				end

				local both = true
				if zone:criticalOnSupplies() then
					local actualboost = xp * RewardDefinitions.actions.supplyBoost
					totalboost = totalboost + actualboost
				else 
					both = false
				end

				if zone.distToFront == 0 then
					local actualboost = xp * RewardDefinitions.actions.supplyBoost
					totalboost = totalboost + actualboost
				else 
					both = false
				end

				if both then
					local actualboost = xp * 1
					totalboost = totalboost + actualboost
				end

				xp = xp + totalboost

				if lastLoad.distToFront >= zone.distToFront then
					xp = xp * 0.25
				end

				self.playerTracker:addStat(player, math.floor(xp), PlayerTracker.statTypes.xp)
				self.missionTracker:tallySupplies(player, amount, zone.name)
				trigger.action.outTextForUnit(unit:getID(), '+'..math.floor(xp)..' XP', 10)
			end
		end
	end
	
	function PlayerLogistics.markWithSmoke(zonename)
		local zone = CustomZone:getByName(zonename)
		local p = Utils.getPointOnSurface(zone.point)
		trigger.action.smoke(p, 0)
	end
	
	function PlayerLogistics.getWeight(supplies)
		return math.floor(supplies)
	end

	function PlayerLogistics:getCarriedPersonWeight(groupname)
		local gr = Group.getByName(groupname)
		local un = gr:getUnit(1)
		if un then
			if not PlayerLogistics.allowedTypes[un:getDesc().typeName] then return 0 end
			
			local max = PlayerLogistics.allowedTypes[un:getDesc().typeName].personCapacity

			local pilotWeight = 0
			local squadWeight = 0
			if not self.carriedPilots[gr:getID()] then self.carriedPilots[gr:getID()] = {} end
			local pilots = self.carriedPilots[gr:getID()]
			if pilots then 
				pilotWeight = 100 * #pilots
			end

			if not self.carriedInfantry[gr:getID()] then self.carriedInfantry[gr:getID()] = {} end
			local squads = self.carriedInfantry[gr:getID()]
			if squads then
				for _,squad in ipairs(squads) do 
					squadWeight = squadWeight + squad.weight
				end
			end

			return pilotWeight + squadWeight
		end
	end

	function PlayerLogistics:getOccupiedPersonCapacity(groupname)
		local gr = Group.getByName(groupname)
		local un = gr:getUnit(1)
		if un then
			if not PlayerLogistics.allowedTypes[un:getDesc().typeName] then return 0 end
			if self.carriedCargo[gr:getID()] and self.carriedCargo[gr:getID()] > 0 then return 0 end
			
			local max = PlayerLogistics.allowedTypes[un:getDesc().typeName].personCapacity

			local pilotCount = 0
			local squadCount = 0
			if not self.carriedPilots[gr:getID()] then self.carriedPilots[gr:getID()] = {} end
			local pilots = self.carriedPilots[gr:getID()]
			if pilots then 
				pilotCount = #pilots
			end

			if not self.carriedInfantry[gr:getID()] then self.carriedInfantry[gr:getID()] = {} end
			local squads = self.carriedInfantry[gr:getID()]
			if squads then
				for _,squad in ipairs(squads) do 
					squadCount = squadCount + squad.size
				end
			end

			local total = pilotCount + squadCount

			return total
		end
	end

	function PlayerLogistics:getRemainingPersonCapacity(groupname)
		local gr = Group.getByName(groupname)
		local un = gr:getUnit(1)
		if un then
			if not PlayerLogistics.allowedTypes[un:getDesc().typeName] then return 0 end
			if self.carriedCargo[gr:getID()] and self.carriedCargo[gr:getID()] > 0 then return 0 end
			
			local max = PlayerLogistics.allowedTypes[un:getDesc().typeName].personCapacity

			local total = self:getOccupiedPersonCapacity(groupname)

			return max - total
		end
	end

	function PlayerLogistics:canFitCargo(groupname)
		local gr = Group.getByName(groupname)
		local un = gr:getUnit(1)
		if un then
			if not PlayerLogistics.allowedTypes[un:getDesc().typeName] then return false end
			return self:getOccupiedPersonCapacity(groupname) == 0
		end
	end

	function PlayerLogistics:canFitPersonnel(groupname, toFit)
		local gr = Group.getByName(groupname)
		local un = gr:getUnit(1)
		if un then
			if not PlayerLogistics.allowedTypes[un:getDesc().typeName] then return false end

			return self:getRemainingPersonCapacity(groupname) >= toFit
		end
	end

	function PlayerLogistics:showPilot(groupname)
		local gr = Group.getByName(groupname)
		if gr then
			local un = gr:getUnit(1)
			if un then
				local data = self.csarTracker:getClosestPilot(un:getPoint())
				
				if not data then 
					trigger.action.outTextForUnit(un:getID(), 'No pilots in need of extraction', 10)
					return
				end

				local pos = data.pilot:getUnit(1):getPoint()
				local brg = math.floor(Utils.getBearing(un:getPoint(), data.pilot:getUnit(1):getPoint()))
				local dist = data.dist
				local dstft = math.floor(dist/0.3048)

				local msg = data.name..' requesting extraction'
				msg = msg..'\n\n Distance: '
				if dist>1000 then
					local dstkm = string.format('%.2f',dist/1000)
					local dstnm = string.format('%.2f',dist/1852)
					
					msg = msg..dstkm..'km | '..dstnm..'nm'
				else
					local dstft = math.floor(dist/0.3048)
					msg = msg..math.floor(dist)..'m | '..dstft..'ft'
				end
				
				msg = msg..'\n Bearing: '..brg
				
				trigger.action.outTextForUnit(un:getID(), msg, 10)
			end
		end
	end
	
	function PlayerLogistics:smokePilot(groupname)
		local gr = Group.getByName(groupname)
		if gr then
			local un = gr:getUnit(1)
			if un then
				local data = self.csarTracker:getClosestPilot(un:getPoint())
				
				if not data or data.dist >= 5000 then 
					trigger.action.outTextForUnit(un:getID(), 'No pilots nearby', 10)
					return
				end

				self.csarTracker:markPilot(data)
				trigger.action.outTextForUnit(un:getID(), 'Location of '..data.name..' marked with green smoke.', 10)
			end
		end
	end
	
	function PlayerLogistics:flarePilot(groupname)
		local gr = Group.getByName(groupname)
		if gr then
			local un = gr:getUnit(1)
			if un then
				local data = self.csarTracker:getClosestPilot(un:getPoint())
				
				if not data or data.dist >= 5000 then 
					trigger.action.outTextForUnit(un:getID(), 'No pilots nearby', 10)
					return
				end

				self.csarTracker:flarePilot(data)
				trigger.action.outTextForUnit(un:getID(), data.name..' has deployed a green flare', 10)
			end
		end
	end
	
	function PlayerLogistics:unloadPilots(groupname)
		local gr = Group.getByName(groupname)
		if gr then
			local un = gr:getUnit(1)
			if un then
				local pilots = self.carriedPilots[gr:getID()]
				if not pilots or #pilots==0 then
					trigger.action.outTextForUnit(un:getID(), 'No pilots onboard', 10)
					return
				end

				if Utils.isInAir(un) then
					trigger.action.outTextForUnit(un:getID(), 'Can not unload pilot while in air', 10)
					return
				end
				
				if not self:isCargoDoorOpen(un) then
					trigger.action.outTextForUnit(un:getID(), 'Can not unload pilot while cargo door closed', 10)
					return
				end

				local zn = ZoneCommand.getZoneOfUnit(un:getName())
				if not zn then
					trigger.action.outTextForUnit(un:getID(), 'Can only unload extracted pilots while within a friendly zone', 10)
					return
				end
				
				if zn.side ~= 0 and zn.side ~= un:getCoalition()then
					trigger.action.outTextForUnit(un:getID(), 'Can only unload extracted pilots while within a friendly zone', 10)
					return
				end

				zn:addResource(200*#pilots)
				zn:refreshText()

				if un.getPlayerName then
					local player = un:getPlayerName()

					local xp = #pilots*RewardDefinitions.actions.pilotExtract

					self.playerTracker:addStat(player, math.floor(xp), PlayerTracker.statTypes.xp)
					self.missionTracker:tallyUnloadPilot(player, zn.name)
					trigger.action.outTextForUnit(un:getID(), '+'..math.floor(xp)..' XP', 10)
				end

				self.carriedPilots[gr:getID()] = {}
				trigger.action.setUnitInternalCargo(un:getName(), 0)
				trigger.action.outTextForUnit(un:getID(), 'Pilots unloaded', 10)
			end
		end
	end
	
	function PlayerLogistics:extractPilot(groupname)
		local gr = Group.getByName(groupname)
		if gr then
			local un = gr:getUnit(1)
			if un then
				if not self:canFitPersonnel(groupname, 1) then
					trigger.action.outTextForUnit(un:getID(), 'Not enough free space onboard. (Need 1)', 10)
					return
				end

				timer.scheduleFunction(function(param,time) 
					local self = param.context
					local un = param.unit
					if not un then return end
					if not un:isExist() then return end
					local gr = un:getGroup()

					local data = self.csarTracker:getClosestPilot(un:getPoint())

					if not data or data.dist > 500 then
						trigger.action.outTextForUnit(un:getID(), 'There is no pilot nearby that needs extraction', 10)
						return
					else
						if not self:isCargoDoorOpen(un) then
							trigger.action.outTextForUnit(un:getID(), 'Cargo door closed', 1)
						elseif Utils.getAGL(un) > 70 then
							trigger.action.outTextForUnit(un:getID(), 'Altitude too high (< 70 m). Current: '..string.format('%.2f',Utils.getAGL(un))..' m', 1)
						elseif mist.vec.mag(un:getVelocity())>5 then
							trigger.action.outTextForUnit(un:getID(), 'Moving too fast (< 5 m/s). Current: '..string.format('%.2f',mist.vec.mag(un:getVelocity()))..' m/s', 1)
						else
							if data.dist > 100 then
								trigger.action.outTextForUnit(un:getID(), 'Too far (< 100m). Current: '..string.format('%.2f',data.dist)..' m', 1)
							else
								if not self.carriedPilots[gr:getID()] then self.carriedPilots[gr:getID()] = {} end
								table.insert(self.carriedPilots[gr:getID()], data.name)
								local player = un:getPlayerName()
								self.missionTracker:tallyLoadPilot(player, data)
								self.csarTracker:removePilot(data.name)
								local weight = self:getCarriedPersonWeight(gr:getName())
								trigger.action.setUnitInternalCargo(un:getName(), weight)
								trigger.action.outTextForUnit(un:getID(), data.name..' onboard. ('..weight..' kg)', 10)
								return
							end
						end
					end

					param.trys = param.trys - 1
					if param.trys > 0 then
						return time+1
					end
				end, {context = self, unit = un, trys = 60}, timer.getTime()+0.1)
			end
		end
	end
	
	function PlayerLogistics:extractSquad(groupname)
		local gr = Group.getByName(groupname)
		if gr then
			local un = gr:getUnit(1)
			if un then

				if Utils.isInAir(un) then
					trigger.action.outTextForUnit(un:getID(), 'Can not load infantry while in air', 10)
					return
				end
				
				if not self:isCargoDoorOpen(un) then
					trigger.action.outTextForUnit(un:getID(), 'Can not load infantry while cargo door closed', 10)
					return
				end

				local squad, distance = self.squadTracker:getClosestExtractableSquad(un:getPoint())
				if squad and distance < 50 then
					local squadgr = Group.getByName(squad.name)
					if squadgr and squadgr:isExist() then
						local sqsize = squadgr:getSize()
						if not self:canFitPersonnel(groupname, sqsize) then
							trigger.action.outTextForUnit(un:getID(), 'Not enough free space onboard. (Need '..sqsize..')', 10)
							return
						end

						if not self.carriedInfantry[gr:getID()] then self.carriedInfantry[gr:getID()] = {} end
						table.insert(self.carriedInfantry[gr:getID()],{type = PlayerLogistics.infantryTypes.extractable, size = sqsize, weight = sqsize * 100})
						
						local weight = self:getCarriedPersonWeight(gr:getName())

						trigger.action.setUnitInternalCargo(un:getName(), weight)
						
						local loadedInfName = PlayerLogistics.getInfantryName(PlayerLogistics.infantryTypes.extractable)
						trigger.action.outTextForUnit(un:getID(), loadedInfName..' onboard. ('..weight..' kg)', 10)
						
						local player = un:getPlayerName()
						self.missionTracker:tallyLoadSquad(player, squad)
						self.squadTracker:removeSquad(squad.name)
						
						squadgr:destroy()
					end
				else
					trigger.action.outTextForUnit(un:getID(), 'There is no infantry nearby that is ready to be extracted.', 10)
				end
			end
		end
	end

	function PlayerLogistics:loadInfantry(params)
		if not ZoneCommand then return end
		
		local gr = Group.getByName(params.group)
		local squadType = params.type
		local squadName = PlayerLogistics.getInfantryName(squadType)
		
		local squadCost = 0
		local squadSize = 999999
		local squadWeight = 0
		if self.registeredSquadGroups[squadType] then
			squadCost = self.registeredSquadGroups[squadType].cost
			squadSize = self.registeredSquadGroups[squadType].size
			squadWeight = self.registeredSquadGroups[squadType].weight
		end
		
		if gr then
			local un = gr:getUnit(1)
			if un then
				if Utils.isInAir(un) then
					trigger.action.outTextForUnit(un:getID(), 'Can not load infantry while in air', 10)
					return
				end
				
				local zn = ZoneCommand.getZoneOfUnit(un:getName())
				if not zn then
					trigger.action.outTextForUnit(un:getID(), 'Can only load infantry while within a friendly zone', 10)
					return
				end
				
				if zn.side ~= un:getCoalition() then
					trigger.action.outTextForUnit(un:getID(), 'Can only load infantry while within a friendly zone', 10)
					return
				end

				if not self:isCargoDoorOpen(un) then
					trigger.action.outTextForUnit(un:getID(), 'Can not load infantry while cargo door closed', 10)
					return
				end

				if zn:criticalOnSupplies() then
					trigger.action.outTextForUnit(un:getID(), 'Can not load infantry, zone is low on resources', 10)
					return
				end

				if zn.resource < zn.spendTreshold + squadCost then
					trigger.action.outTextForUnit(un:getID(), 'Can not afford to load '..squadName..' (Cost: '..squadCost..'). Resources would fall to a critical level.', 10)
					return
				end

				if not self:canFitPersonnel(params.group, squadSize) then
					trigger.action.outTextForUnit(un:getID(), 'Not enough free space on board. (Need '..squadSize..')', 10)
					return
				end
				
				zn:removeResource(squadCost)
				zn:refreshText()
				if not self.carriedInfantry[gr:getID()] then self.carriedInfantry[gr:getID()] = {} end
				table.insert(self.carriedInfantry[gr:getID()],{ type = squadType, size = squadSize, weight = squadWeight, loadedAt = zn })
				self.lastLoaded[gr:getID()] = zn
				
				local weight = self:getCarriedPersonWeight(gr:getName())
				trigger.action.setUnitInternalCargo(un:getName(), weight)
				
				local loadedInfName = PlayerLogistics.getInfantryName(squadType)
				trigger.action.outTextForUnit(un:getID(), loadedInfName..' onboard. ('..weight..' kg)', 10)
			end
		end
	end

	function PlayerLogistics:unloadInfantry(params)
		if not ZoneCommand then return end
		local groupname = params.group
		local sqtype = params.type
		
		local gr = Group.getByName(groupname)
		if gr then
			local un = gr:getUnit(1)
			if un then
				if Utils.isInAir(un) then
					trigger.action.outTextForUnit(un:getID(), 'Can not unload infantry while in air', 10)
					return
				end

				if not self:isCargoDoorOpen(un) then
					trigger.action.outTextForUnit(un:getID(), 'Can not unload infantry while cargo door closed', 10)
					return
				end

				local carriedSquads = self.carriedInfantry[gr:getID()]
				if not carriedSquads or #carriedSquads == 0 then
					trigger.action.outTextForUnit(un:getID(), 'No infantry onboard', 10)
					return
				end
				
				local toUnload = carriedSquads
				local remaining = {}
				if sqtype then
					toUnload = {}
					local sqToUnload = nil
					for _,sq in ipairs(carriedSquads) do
						if sq.type == sqtype and not sqToUnload then
							sqToUnload = sq
						else
							table.insert(remaining, sq)
						end
					end

					if sqToUnload then toUnload = { sqToUnload } end
				end

				if #toUnload == 0 then
					if sqtype then
						local squadName = PlayerLogistics.getInfantryName(sqtype)
						trigger.action.outTextForUnit(un:getID(), 'No '..squadName..' onboard.', 10)
					else
						trigger.action.outTextForUnit(un:getID(), 'No infantry onboard.', 10)
					end

					return
				end
				
				local zn = ZoneCommand.getZoneOfUnit(un:getName())

				for _, sq in ipairs(toUnload) do
					local squadName = PlayerLogistics.getInfantryName(sq.type)
					local lastLoad = sq.loadedAt
					if lastLoad and zn and zn.side == un:getCoalition() and zn.name==lastLoad.name then
						if self.registeredSquadGroups[sq.type] then
							local cost = self.registeredSquadGroups[sq.type].cost
							zn:addResource(cost)
							zn:refreshText()
							trigger.action.outTextForUnit(un:getID(), squadName..' unloaded', 10)
						end
					else
						if sq.type == PlayerLogistics.infantryTypes.extractable then
							if not zn then
								trigger.action.outTextForUnit(un:getID(), 'Can only unload extracted infantry while within a friendly zone', 10)
								table.insert(remaining, sq)
							elseif zn.side ~= un:getCoalition() then
								trigger.action.outTextForUnit(un:getID(), 'Can only unload extracted infantry while within a friendly zone', 10)
								table.insert(remaining, sq)
							else
								trigger.action.outTextForUnit(un:getID(), 'Infantry recovered', 10)
								zn:addResource(200)
								zn:refreshText()
								
								if un.getPlayerName then
									local player = un:getPlayerName()
									local xp = RewardDefinitions.actions.squadExtract
			
									self.playerTracker:addStat(player, math.floor(xp), PlayerTracker.statTypes.xp)
									self.missionTracker:tallyUnloadSquad(player, zn.name, sq.type)
									trigger.action.outTextForUnit(un:getID(), '+'..math.floor(xp)..' XP', 10)
								end
							end
						elseif self.registeredSquadGroups[sq.type] then
							local pos = Utils.getPointOnSurface(un:getPoint())
		
							local error = self.squadTracker:spawnInfantry(self.registeredSquadGroups[sq.type], pos)
							
							if not error then
								trigger.action.outTextForUnit(un:getID(), squadName..' deployed', 10)
		
								if un.getPlayerName then
									local player = un:getPlayerName()
									local xp = RewardDefinitions.actions.squadDeploy
				
									self.playerTracker:addStat(player, math.floor(xp), PlayerTracker.statTypes.xp)

									if zn then
										self.missionTracker:tallyUnloadSquad(player, zn.name, sq.type)
									else
										self.missionTracker:tallyUnloadSquad(player, '', sq.type)
									end
									trigger.action.outTextForUnit(un:getID(), '+'..math.floor(xp)..' XP', 10)
								end
							else
								trigger.action.outTextForUnit(un:getID(), 'Failed to deploy squad, no suitable location nearby', 10)
								table.insert(remaining, sq)
							end
						else
							trigger.action.outText("ERROR: SQUAD TYPE NOT REGISTERED", 60)
						end
					end
				end
				
				self.carriedInfantry[gr:getID()] = remaining
				local weight = self:getCarriedPersonWeight(groupname)
				trigger.action.setUnitInternalCargo(un:getName(), weight)
			end
		end
	end

	function PlayerLogistics:unloadAll(groupname)
		local gr = Group.getByName(groupname)
		if gr then 
			local un = gr:getUnit(1)
			if un then
				local cargo = self.carriedCargo[gr:getID()]
				local squad = self.carriedInfantry[gr:getID()]
				local pilot = self.carriedPilots[gr:getID()]

				if cargo and cargo>0 then
					self:unloadSupplies({group=groupname, amount=9999999})
				end

				if squad and #squad>0 then
					self:unloadInfantry({group=groupname})
				end

				if pilot and #pilot>0 then
					self:unloadPilots(groupname)
				end
			end
		end
	end
	
	function PlayerLogistics:cargoStatus(groupName)
		local gr = Group.getByName(groupName)
		if gr then
			local un = gr:getUnit(1)
			if un then
				local onboard = self.carriedCargo[gr:getID()]
				if onboard and onboard > 0 then
					local weight = self.getWeight(onboard)
					trigger.action.outTextForUnit(un:getID(), onboard..' supplies onboard. ('..weight..' kg)', 10)
				else
					local msg = ''
					local squads = self.carriedInfantry[gr:getID()]
					if squads and #squads>0 then
						msg = msg..'Squads:\n'

						for _,squad in ipairs(squads) do
							local infName = PlayerLogistics.getInfantryName(squad.type)
							msg = msg..'  \n'..infName..' (Size: '..squad.size..')'
						end
					end

					local pilots = self.carriedPilots[gr:getID()]
					if pilots and #pilots>0 then
						msg = msg.."\n\nPilots:\n"
						for i,v in ipairs(pilots) do
							msg = msg..'\n '..v
						end

					end
					
					local max = PlayerLogistics.allowedTypes[un:getDesc().typeName].personCapacity
					local occupied = self:getOccupiedPersonCapacity(groupName)

					msg = msg..'\n\nCapacity: '..occupied..'/'..max
					
					msg = msg..'\n('..self:getCarriedPersonWeight(groupName)..' kg)'

					if un:getDesc().typeName == 'Hercules' then
						local preped = self.hercPreparedDrops[gr:getID()]
						if preped then
							if preped == 'supplies' then
								msg = msg..'\nSupplies prepared for next drop.'
							else
								local squadName = PlayerLogistics.getInfantryName(preped)
								msg = msg..'\n'..squadName..' prepared for next drop.'
							end
						end
					end

					trigger.action.outTextForUnit(un:getID(), msg, 10)
				end
			end
		end
	end

	function PlayerLogistics:isCargoDoorOpen(unit)
		if unit then
			local tp = unit:getDesc().typeName
			if tp == "Mi-8MT" then
				if unit:getDrawArgumentValue(86) == 1 then return true end
				if unit:getDrawArgumentValue(38) > 0.85 then return true end
			elseif tp == "UH-1H" then
				if unit:getDrawArgumentValue(43) == 1 then return true end
				if unit:getDrawArgumentValue(44) == 1 then return true end
			elseif tp == "Mi-24P" then
				if unit:getDrawArgumentValue(38) == 1 then return true end
				if unit:getDrawArgumentValue(86) == 1 then return true end
			elseif tp == "Hercules" then
				if unit:getDrawArgumentValue(1215) == 1 and unit:getDrawArgumentValue(1216) == 1 then return true end
			elseif tp == "UH-60L" then
				if unit:getDrawArgumentValue(401) == 1 then return true end
				if unit:getDrawArgumentValue(402) == 1 then return true end
			elseif tp == "SA342Mistral" then
				if unit:getDrawArgumentValue(34) == 1 then return true end
				if unit:getDrawArgumentValue(38) == 1 then return true end
			elseif tp == "SA342L" then
				if unit:getDrawArgumentValue(34) == 1 then return true end
				if unit:getDrawArgumentValue(38) == 1 then return true end
			elseif tp == "SA342M" then
				if unit:getDrawArgumentValue(34) == 1 then return true end
				if unit:getDrawArgumentValue(38) == 1 then return true end
			elseif tp == "SA342Minigun" then
				if unit:getDrawArgumentValue(34) == 1 then return true end
				if unit:getDrawArgumentValue(38) == 1 then return true end
			else
				return true
			end
		end
	end
	
	function PlayerLogistics:loadSupplies(params)
		if not ZoneCommand then return end
		
		local groupName = params.group
		local amount = params.amount
		
		local gr = Group.getByName(groupName)
		if gr then
			local un = gr:getUnit(1)
			if un then
				if not self:canFitCargo(groupName) then
					trigger.action.outTextForUnit(un:getID(), 'Can not load cargo. Personnel onboard.', 10)
					return
				end

				if Utils.isInAir(un) then
					trigger.action.outTextForUnit(un:getID(), 'Can not load supplies while in air', 10)
					return
				end
				
				local zn = ZoneCommand.getZoneOfUnit(un:getName())
				if not zn then
					trigger.action.outTextForUnit(un:getID(), 'Can only load supplies while within a friendly zone', 10)
					return
				end
				
				if zn.side ~= un:getCoalition() then
					trigger.action.outTextForUnit(un:getID(), 'Can only load supplies while within a friendly zone', 10)
					return
				end

				if not self:isCargoDoorOpen(un) then
					trigger.action.outTextForUnit(un:getID(), 'Can not load supplies while cargo door closed', 10)
					return
				end

				if zn:criticalOnSupplies() then
					trigger.action.outTextForUnit(un:getID(), 'Can not load supplies, zone is low on resources', 10)
					return
				end

				if zn.resource < zn.spendTreshold + amount then
					trigger.action.outTextForUnit(un:getID(), 'Can not load supplies if resources would fall to a critical level.', 10)
					return
				end

				local carried = self.carriedCargo[gr:getID()] or 0
				if amount > zn.resource then
					amount = zn.resource
				end
				
				zn:removeResource(amount)
				zn:refreshText()
				self.carriedCargo[gr:getID()] = carried + amount
				self.lastLoaded[gr:getID()] = zn
				local onboard = self.carriedCargo[gr:getID()]
				local weight = self.getWeight(onboard)

				if un:getDesc().typeName == "Hercules" then
					local loadedInCrates = 0
					local ammo = un:getAmmo()
					for _,load in ipairs(ammo) do
						if load.desc.typeName == 'weapons.bombs.Generic Crate [20000lb]' then
							loadedInCrates = 9000 * load.count
						end
					end

					local internal = 0
					if weight > loadedInCrates then
						internal = weight - loadedInCrates
					end

					trigger.action.setUnitInternalCargo(un:getName(), internal)
				else
					trigger.action.setUnitInternalCargo(un:getName(), weight)
				end

				trigger.action.outTextForUnit(un:getID(), amount..' supplies loaded', 10)
				trigger.action.outTextForUnit(un:getID(), onboard..' supplies onboard. ('..weight..' kg)', 10)
			end
		end
	end
	
	function PlayerLogistics:unloadSupplies(params)
		if not ZoneCommand then return end
		
		local groupName = params.group
		local amount = params.amount
		
		local gr = Group.getByName(groupName)
		if gr then
			local un = gr:getUnit(1)
			if un then
				if Utils.isInAir(un) then
					trigger.action.outTextForUnit(un:getID(), 'Can not unload supplies while in air', 10)
					return
				end
				
				local zn = ZoneCommand.getZoneOfUnit(un:getName())
				if not zn then
					trigger.action.outTextForUnit(un:getID(), 'Can only unload supplies while within a friendly zone', 10)
					return
				end
				
				if zn.side ~= 0 and zn.side ~= un:getCoalition()then
					trigger.action.outTextForUnit(un:getID(), 'Can only unload supplies while within a friendly zone', 10)
					return
				end

				if not self:isCargoDoorOpen(un) then
					trigger.action.outTextForUnit(un:getID(), 'Can not unload supplies while cargo door closed', 10)
					return
				end

				if not self.carriedCargo[gr:getID()] or self.carriedCargo[gr:getID()] == 0 then
					trigger.action.outTextForUnit(un:getID(), 'No supplies loaded', 10)
					return
				end
				
				local carried = self.carriedCargo[gr:getID()]
				if amount > carried then
					amount = carried
				end
				
				self.carriedCargo[gr:getID()] = carried-amount
				zn:addResource(amount)

				local lastLoad = self.lastLoaded[gr:getID()]
				self:awardSupplyXP(lastLoad, zn, un, amount)

				zn:refreshText()
				local onboard = self.carriedCargo[gr:getID()]
				local weight = self.getWeight(onboard)
			
				if un:getDesc().typeName == "Hercules" then
					local loadedInCrates = 0
					local ammo = un:getAmmo()
					for _,load in ipairs(ammo) do
						if load.desc.typeName == 'weapons.bombs.Generic Crate [20000lb]' then
							loadedInCrates = 9000 * load.count
						end
					end

					local internal = 0
					if weight > loadedInCrates then
						internal = weight - loadedInCrates
					end
					
					trigger.action.setUnitInternalCargo(un:getName(), internal)
				else
					trigger.action.setUnitInternalCargo(un:getName(), weight)
				end

				trigger.action.outTextForUnit(un:getID(), amount..' supplies unloaded', 10)
				trigger.action.outTextForUnit(un:getID(), onboard..' supplies remaining onboard. ('..weight..' kg)', 10)
			end
		end
	end
end

-----------------[[ END OF PlayerLogistics.lua ]]-----------------



-----------------[[ MarkerCommands.lua ]]-----------------

MarkerCommands = {}
do
	function MarkerCommands:new()
		local obj = {}
		obj.commands = {} --{command=string, action=function}
		
		setmetatable(obj, self)
		self.__index = self
		
		obj:start()
		
		return obj
	end
	
	function MarkerCommands:addCommand(command, action, hasParam, state)
		table.insert(self.commands, {command = command, action = action, hasParam = hasParam, state = state})
	end
	
	function MarkerCommands:start()
		local markEditedEvent = {}
		markEditedEvent.context = self
		function markEditedEvent:onEvent(event)
			if event.id == 26 and event.text and (event.coalition == 1 or event.coalition == 2) then -- mark changed
				local success = false
				env.info('MarkerCommands - input: '..event.text)
				
				for i,v in ipairs(self.context.commands) do
					if (not v.hasParam) and event.text == v.command then
						success = v.action(event, nil, v.state)
						break
					elseif v.hasParam and event.text:find('^'..v.command..':') then
						local param = event.text:gsub('^'..v.command..':', '')
						success = v.action(event, param, v.state)
						break
					end
				end
				
				if success then
					trigger.action.removeMark(event.idx)
				end
			end
		end
		
		world.addEventHandler(markEditedEvent)
	end
end


-----------------[[ END OF MarkerCommands.lua ]]-----------------



-----------------[[ ZoneCommand.lua ]]-----------------

ZoneCommand = {}
do
	ZoneCommand.currentZoneIndex = 1000
	ZoneCommand.allZones = {}
	ZoneCommand.buildSpeed = Config.buildSpeed
	ZoneCommand.supplyBuildSpeed = Config.supplyBuildSpeed
	ZoneCommand.missionValidChance = 0.9
	ZoneCommand.missionBuildSpeedReduction = Config.missionBuildSpeedReduction
	ZoneCommand.revealTime = 0
	ZoneCommand.staticRegistry = {}

	ZoneCommand.modes = {
		normal = 'normal',
		supply = 'supply',
		export = 'export'
	}
	
	ZoneCommand.productTypes = {
		upgrade = 'upgrade',
		mission = 'mission',
		defense = 'defense'
	}
	
	ZoneCommand.missionTypes = {
		supply_air = 'supply_air',
		supply_convoy = 'supply_convoy',
		cas = 'cas',
		cas_helo = 'cas_helo',
		strike = 'strike',
		patrol = 'patrol',
		sead = 'sead',
		assault = 'assault',
		bai = 'bai',
		supply_transfer = 'supply_transfer',
		awacs = 'awacs',
		tanker = 'tanker'
	}
	
	function ZoneCommand:new(zonename)
		local obj = {}
		obj.name = zonename
		obj.side = 0
		obj.resource = 0
		obj.resourceChange = 0
		obj.maxResource = 20000
		obj.spendTreshold = 5000
		obj.keepActive = false
		obj.boostScale = 1.0
		obj.extraBuildResources = 0
		obj.reservedMissions = {}
		obj.isHeloSpawn = false
		obj.isPlaneSpawn = false

		obj.connectionManager = nil
		
		obj.zone = CustomZone:getByName(zonename)
		obj.products = {}
		obj.mode = 'normal' 
		--[[
			normal: buys whatever it can
			supply: buys only supply missions
			export: supply mode, but also sells all defense groups from the zone
		]]--
		obj.index = ZoneCommand.currentZoneIndex
		ZoneCommand.currentZoneIndex = ZoneCommand.currentZoneIndex + 1
		
		obj.built = {}
		obj.income = 0
		
		--group restrictions
		obj.spawns = {}
		for i,v in pairs(mist.DBs.groupsByName) do
			if v.units[1].skill == 'Client' then
				local zn = obj.zone
				local pos3d = {
					x = v.units[1].point.x,
					y = 0,
					z = v.units[1].point.y
				}
				
				if zn and zn:isInside(pos3d) then
					local coa = 0
					if v.coalition=='blue' then
						coa = 2
					elseif v.coalition=='red' then
						coa = 1
					end
					
					table.insert(obj.spawns, {name=i, side=coa})
				end
			end
		end
		
		--draw graphics
		local color = {0.7,0.7,0.7,0.3}
		if obj.side == 1 then
			color = {1,0,0,0.3}
		elseif obj.side == 2 then
			color = {0,0,1,0.3}
		end
		
		obj.zone:draw(obj.index, color, color)
		
		local point = obj.zone.point

		if obj.zone:isCircle() then
			point = {
				x = obj.zone.point.x,
				y = obj.zone.point.y,
				z = obj.zone.point.z + obj.zone.radius
			}
		elseif obj.zone:isQuad() then
			local largestZ = obj.zone.vertices[1].z
			local largestX = obj.zone.vertices[1].x
			for i=2,4,1 do
				if obj.zone.vertices[i].z > largestZ then
					largestZ = obj.zone.vertices[i].z
					largestX = obj.zone.vertices[i].x
				end
			end
			
			point = {
				x = largestX,
				y = obj.zone.point.y,
				z = largestZ
			}
		end
		
		--trigger.action.textToAll(1,1000+obj.index,point, {0,0,0,0.8}, {1,1,1,0.5}, 15, true, '')
		--trigger.action.textToAll(2,2000+obj.index,point, {0,0,0,0.8}, {1,1,1,0.5}, 15, true, '')
		trigger.action.textToAll(-1,2000+obj.index,point, {0,0,0,0.8}, {1,1,1,0.5}, 15, true, '') --show blue to all
		setmetatable(obj, self)
		self.__index = self
		
		obj:refreshText()
		obj:start()
		obj:refreshSpawnBlocking()
		ZoneCommand.allZones[obj.name] = obj
		return obj
	end
	
	function ZoneCommand:refreshSpawnBlocking()
		for _,v in ipairs(self.spawns) do
			trigger.action.setUserFlag(v.name, v.side ~= self.side)
		end
	end
	
	function ZoneCommand.setNeighbours(conManager)
		for name,zone in pairs(ZoneCommand.allZones) do
			zone.connectionManager = conManager
			local neighbours = conManager:getConnectionsOfZone(name)
			zone.neighbours = {}
			for _,zname in ipairs(neighbours) do
				zone.neighbours[zname] = ZoneCommand.getZoneByName(zname)
			end
		end
	end
	
	function ZoneCommand.getZoneByName(name)
		if not name then return nil end
		return ZoneCommand.allZones[name]
	end
	
	function ZoneCommand.getAllZones()
		return ZoneCommand.allZones
	end
	
	function ZoneCommand.getZoneOfUnit(unitname)
		local un = Unit.getByName(unitname)
		
		if not un then 
			return nil
		end
		
		for i,v in pairs(ZoneCommand.allZones) do
			if Utils.isInZone(un, i) then
				return v
			end
		end
		
		return nil
	end
	
	function ZoneCommand.getZoneOfWeapon(weapon)
		if not weapon then 
			return nil
		end
		
		for i,v in pairs(ZoneCommand.allZones) do
			if Utils.isInZone(weapon, i) then
				return v
			end
		end
		
		return nil
	end

	function ZoneCommand.getClosestZoneToPoint(point)
		local minDist = 9999999
		local closest = nil
		for i,v in pairs(ZoneCommand.allZones) do
			local d = mist.utils.get2DDist(v.zone.point, point)
			if d < minDist then
				minDist = d
				closest = v
			end
		end
		
		return closest, minDist
	end
	
	function ZoneCommand.getZoneOfPoint(point)
		for i,v in pairs(ZoneCommand.allZones) do
			local z = CustomZone:getByName(i)
			if z and z:isInside(point) then
				return v
			end
		end
		
		return nil
	end

	function ZoneCommand:boostProduction(amount)
		self.extraBuildResources = self.extraBuildResources + amount
		env.info('ZoneCommand:boostProduction - '..self.name..' production boosted by '..amount..' to a total of '..self.extraBuildResources)
	end

	function ZoneCommand:sabotage(explosionSize, sourcePoint)
		local minDist = 99999999
		local closest = nil
		for i,v in pairs(self.built) do
			if v.type == 'upgrade' then
				local st = StaticObject.getByName(v.name)
				if not st then st = Group.getByName(v.name) end
				local pos = st:getPoint()

				local d = mist.utils.get2DDist(pos, sourcePoint)
				if d < minDist then
					minDist = d;
					closest = pos
				end
			end
		end

		if closest then
			trigger.action.explosion(closest, explosionSize)
			env.info('ZoneCommand:sabotage - Structure has been sabotaged at '..self.name)
		end

		local damagedResources = math.random(2000,5000)
		self:removeResource(damagedResources)
		self:refreshText()
	end
	
	function ZoneCommand:refreshText()
		local build = ''
		if self.currentBuild then
			local job = ''
			local display = self.currentBuild.product.display
			if self.currentBuild.product.type == 'upgrade' then
				job = display
			elseif self.currentBuild.product.type == 'defense' then
				if self.currentBuild.isRepair then
					job = display..' (repair)'
				else
					job = display
				end
			elseif self.currentBuild.product.type == 'mission' then
				job = display
			end
			
			build = '\n['..job..' '..math.min(math.floor((self.currentBuild.progress/self.currentBuild.product.cost)*100),100)..'%]'
		end

		local mBuild = ''
		if self.currentMissionBuild then
			local job = ''
			local display = self.currentMissionBuild.product.display
			job = display
			
			mBuild = '\n['..job..' '..math.min(math.floor((self.currentMissionBuild.progress/self.currentMissionBuild.product.cost)*100),100)..'%]'
		end
		
		local status=''
		if self.side ~= 0 and self:criticalOnSupplies() then
			status = '(!)'
		end

		local color = {0.3,0.3,0.3,1}
		if self.side == 1 then
			color = {0.7,0,0,1}
		elseif self.side == 2 then
			color = {0,0,0.7,1}
		end

		--trigger.action.setMarkupColor(1000+self.index, color)
		trigger.action.setMarkupColor(2000+self.index, color)

		local label = '['..self.resource..'/'..self.maxResource..']'..status..build..mBuild

		if self.side == 1 then
			--trigger.action.setMarkupText(1000+self.index, self.name..label)

			if self.revealTime > 0 then
				trigger.action.setMarkupText(2000+self.index, self.name..label)
			else
				trigger.action.setMarkupText(2000+self.index, self.name)
			end
		elseif self.side == 2 then
			--if self.revealTime > 0 then
			--	trigger.action.setMarkupText(1000+self.index, self.name..label)
			--else
			--	trigger.action.setMarkupText(1000+self.index, self.name)
			--end
			trigger.action.setMarkupText(2000+self.index, self.name..label)
		elseif self.side == 0 then
			--trigger.action.setMarkupText(1000+self.index, ' '..self.name..' ')
			trigger.action.setMarkupText(2000+self.index, ' '..self.name..' ')
		end
	end
	
	function ZoneCommand:setSide(side)
		self.side = side
		self:refreshSpawnBlocking()

		if side == 0 then
			self.revealTime = 0
		end

		local color = {0.7,0.7,0.7,0.3}
		if self.side==1 then
			color = {1,0,0,0.3}
		elseif self.side==2 then
			color = {0,0,1,0.3}
		end
		
		trigger.action.setMarkupColorFill(self.index, color)
		trigger.action.setMarkupColor(self.index, color)
		trigger.action.setMarkupTypeLine(self.index, 1)

		if self.side == 2 and (self.isHeloSpawn or self.isPlaneSpawn) then
			trigger.action.setMarkupTypeLine(self.index, 2)
			trigger.action.setMarkupColor(self.index, {0,1,0,1})
		end

		self:refreshText()
	end
	
	function ZoneCommand:addResource(amount)
		self.resource = self.resource+amount
		self.resource = math.floor(math.min(self.resource, self.maxResource))
	end
	
	function ZoneCommand:removeResource(amount)
		self.resource = self.resource-amount
		self.resource = math.floor(math.max(self.resource, 0))
	end

	function ZoneCommand:reveal()
		self.revealTime = 60*30
		self:refreshText()
	end
	
	function ZoneCommand:needsSupplies(sendamount)
		return self.resource + sendamount<self.maxResource
	end
	
	function ZoneCommand:criticalOnSupplies()
		return self.resource<=self.spendTreshold
	end
	
	function ZoneCommand:capture(side, isSetup)
		if self.side == 0 then
			if not isSetup then
				local sidetxt = "Neutral"
				if side == 1 then
					sidetxt = "Red"
				elseif side == 2 then
					sidetxt = "Blue"
				end

				trigger.action.outText(self.name.." has been captured by "..sidetxt, 15)
			end
			self:setSide(side)
			local p = self.upgrades[side][1]
			self:instantBuild(p)
			if not isSetup then
				for i,v in pairs(p.products) do
					if v.cost < 0 then
						self:instantBuild(v)
					end
				end
			end
		end
	end
	
	function ZoneCommand:instantBuild(product)
		if product.type == 'defense' or product.type == 'upgrade' then
			env.info('ZoneCommand: instantBuild ['..product.name..']')
			if self.built[product.name] == nil then
				self.zone:spawnGroup(product)
				self.built[product.name] = product
			end
		elseif product.type == 'mission' then
			self:reserveMission(product)
			timer.scheduleFunction(function (param, tme)
				param.context:unReserveMission(param.product)
				if param.context:isMissionValid(param.product) then
					param.context:activateMission(param.product)
				end
			end, {context = self, product = product}, timer.getTime()+math.random(3,10))
		end
	end
	
	function ZoneCommand:fullUpgrade(resourcePercentage)
		if not resourcePercentage then resourcePercentage = 0.25 end
		self.resource = math.floor(self.maxResource*resourcePercentage)
		self:fullBuild()
	end

	function ZoneCommand:fullBuild(useCost)
		if self.side ~= 1 and self.side ~= 2 then return end

		for i,v in ipairs(self.upgrades[self.side]) do
			if useCost then
				local cost = v.cost * useCost
				if self.resource >= cost then
					self:removeResource(cost)
				else
					break
				end
			end

			self:instantBuild(v)

			for i2,v2 in ipairs(v.products) do
				if (v2.type == 'defense' or v2.type=='upgrade') and v2.cost > 0 then
					if useCost then
						local cost = v2.cost * useCost
						if self.resource >= cost then
							self:removeResource(cost)
						else
							break
						end
					end

					self:instantBuild(v2)
				end
			end
		end
	end
	
	function ZoneCommand:start()
		timer.scheduleFunction(function(param, time)
			local self = param.context
			local initialRes = self.resource
			
			--generate income
			if self.side ~= 0 then
				self:addResource(self.income)
			end
			
			--untrack destroyed zone upgrades
			for i,v in pairs(self.built) do
				local u = Group.getByName(i)
				if u and u:getSize() == 0 then
					u:destroy()
					self.built[i] = nil
				end
				
				if not u then
					u = StaticObject.getByName(i)
					if u and u:getLife()<1 then
						u:destroy()
						self.built[i] = nil
					end
				end
				
				if not u then 
					self.built[i] = nil
				end
			end
			
			--upkeep costs for defenses
			for i,v in pairs(self.built) do
				if v.type == 'defense' and v.upkeep then
					v.strikes = v.strikes or 0
					if self.resource >= v.upkeep then
						self:removeResource(v.upkeep)
						v.strikes = 0
					else
						if v.strikes < 6 then
							v.strikes = v.strikes+1
						else
							local u = Group.getByName(i)
							if u then 
								v.strikes = nil
								u:destroy()
								self.built[i] = nil
							end
						end
					end
				elseif v.type == 'upgrade' and v.income then
					self:addResource(v.income)
				end
			end
			
			--check if zone should be reverted to neutral
			local hasUpgrade = false
			for i,v in pairs(self.built) do
				if v.type=='upgrade' then
					hasUpgrade = true
					break
				end
			end
			
			if not hasUpgrade and self.side ~= 0 then
				local sidetxt = "Neutral"
				if self.side == 1 then
					sidetxt = "Red"
				elseif self.side == 2 then
					sidetxt = "Blue"
				end

				trigger.action.outText(sidetxt.." has lost control of "..self.name, 15)

				self:setSide(0)
				self.mode = 'normal'
				self.currentBuild = nil
				self.currentMissionBuild = nil
			end
			
			--sell defenses if export mode
			if self.side ~= 0 and self.mode == 'export' then
				for i,v in pairs(self.built) do
					if v.type=='defense' then
						local g = Group.getByName(i)
						if g then g:destroy() end
						self:addResource(math.floor(v.cost/2))
						self.built[i] = nil
					end
				end
			end
			
			self:verifyBuildValid()
			self:chooseBuild()
			self:progressBuild()
			
			self.resourceChange = self.resource - initialRes
			self:refreshText()
			
			--use revealTime resource
			if self.revealTime > 0 then
				self.revealTime = math.max(0,self.revealTime-10)
			end

			return time+10
		end, {context = self}, timer.getTime()+1)
	end
	
	function ZoneCommand:verifyBuildValid()
		if self.currentBuild then
			if self.side == 0 then
				self.currentBuild = nil 
				env.info('ZoneCommand:verifyBuildValid - stopping build, zone is neutral')
			end

			if self.mode == 'export' or self.mode == 'supply' then 
				if not (self.currentBuild.product.type == ZoneCommand.productTypes.upgrade or 
					self.currentBuild.product.missionType == ZoneCommand.missionTypes.supply_air or 
					self.currentBuild.product.missionType == ZoneCommand.missionTypes.supply_convoy or
					self.currentBuild.product.missionType == ZoneCommand.missionTypes.supply_transfer) then 
					env.info('ZoneCommand:verifyBuildValid - stopping build, mode is '..self.mode..' but mission is not supply')
					self.currentBuild = nil 
				end
			end
			
			if self.currentBuild and (self.currentBuild.product.type == 'defense' or self.currentBuild.product.type == 'mission') then
				for i,v in ipairs(self.upgrades[self.currentBuild.side]) do
					for i2,v2 in ipairs(v.products) do
						if v2.name == self.currentBuild.product.name then
							local g = Group.getByName(v.name)
							if not g then g = StaticObject.getByName(v.name) end
							
							if not g then 
								env.info('ZoneCommand:verifyBuildValid - stopping build, required upgrade no longer exists')
								self.currentBuild = nil 
								break
							end
						end
					end
					
					if not self.currentBuild then
						break
					end
				end
			end
		end

		if self.currentMissionBuild then
			if self.side == 0 then
				self.currentMissionBuild = nil 
				env.info('ZoneCommand:verifyBuildValid - stopping mission build, zone is neutral')
			end

			if (self.mode == 'export' and not self.keepActive) or self.mode == 'supply' then 
				env.info('ZoneCommand:verifyBuildValid - stopping mission build, mode is '..self.mode..'')
				self.currentMissionBuild = nil
			end
			
			if self.currentMissionBuild and self.currentMissionBuild.product.type == 'mission' then
				for i,v in ipairs(self.upgrades[self.currentMissionBuild.side]) do
					for i2,v2 in ipairs(v.products) do
						if v2.name == self.currentMissionBuild.product.name then
							local g = Group.getByName(v.name)
							if not g then g = StaticObject.getByName(v.name) end
							
							if not g then 
								env.info('ZoneCommand:verifyBuildValid - stopping mission build, required upgrade no longer exists')
								self.currentMissionBuild = nil 
								break
							end
						end
					end
					
					if not self.currentMissionBuild then
						break
					end
				end
			end
		end
	end
	
	function ZoneCommand:chooseBuild()
		local treshhold = self.spendTreshold
		--local treshhold = 0
		if self.side ~= 0 and self.currentBuild == nil then
			local canAfford = {}
			for _,v in ipairs(self.upgrades[self.side]) do
				local u = Group.getByName(v.name)
				if not u then u = StaticObject.getByName(v.name) end
				
				if not u then
						table.insert(canAfford, {product = v, reason='upgrade'})
				elseif u ~= nil then
					for _,v2 in ipairs(v.products) do
						if v2.type == 'mission'  then 
							if self.resource > treshhold and
								(v2.missionType == ZoneCommand.missionTypes.supply_air or 
								v2.missionType == ZoneCommand.missionTypes.supply_convoy or 
								v2.missionType == ZoneCommand.missionTypes.supply_transfer) then
								if self:isMissionValid(v2) and math.random() < ZoneCommand.missionValidChance then
									table.insert(canAfford, {product = v2, reason='mission'})
									if v2.bias then
										for _=1,v2.bias,1 do
											table.insert(canAfford, {product = v2, reason='mission'})
										end
									end
								end
							end
						elseif v2.type=='defense' and self.mode ~='export' and self.mode ~='supply' and v2.cost > 0 then
							local g = Group.getByName(v2.name)
							if not g then
								table.insert(canAfford, {product = v2, reason='defense'})
							elseif g:getSize() < (g:getInitialSize()*math.random(40,100)/100) then
								table.insert(canAfford, {product = v2, reason='repair'})
							end
						end
					end
				end
			end
			
			if #canAfford > 0 then
				local choice = math.random(1, #canAfford)
				
				if canAfford[choice] then
					local p = canAfford[choice]
					if p.reason == 'repair' then
						self:queueBuild(p.product, self.side, true)
					else
						self:queueBuild(p.product, self.side)
					end
				end
			end
		end

		if self.side ~= 0 and self.currentMissionBuild == nil then
			local canMission = {}
			for _,v in ipairs(self.upgrades[self.side]) do
				local u = Group.getByName(v.name)
				if not u then u = StaticObject.getByName(v.name) end
				if u ~= nil then
					for _,v2 in ipairs(v.products) do
						if v2.type == 'mission' then 
							if v2.missionType ~= ZoneCommand.missionTypes.supply_air and 
								v2.missionType ~= ZoneCommand.missionTypes.supply_convoy and 
								v2.missionType ~= ZoneCommand.missionTypes.supply_transfer then
								if self:isMissionValid(v2) and math.random() < ZoneCommand.missionValidChance then
									table.insert(canMission, {product = v2, reason='mission'})
									if v2.bias then
										for _=1,v2.bias,1 do
											table.insert(canMission, {product = v2, reason='mission'})
										end
									end
								end
							end
						end
					end
				end
			end

			if #canMission > 0 then
				local choice = math.random(1, #canMission)
				
				if canMission[choice] then
					local p = canMission[choice]
					self:queueBuild(p.product, self.side)
				end
			end
		end
	end
	
	function ZoneCommand:progressBuild()
		if self.currentBuild and self.currentBuild.side ~= self.side then
			env.info('ZoneCommand:progressBuild '..self.name..' - stopping build, zone changed owner')
			self.currentBuild = nil
		end

		if self.currentMissionBuild and self.currentMissionBuild.side ~= self.side then
			env.info('ZoneCommand:progressBuild '..self.name..' - stopping mission build, zone changed owner')
			self.currentMissionBuild = nil
		end
		
		if self.currentBuild then
			if self.currentBuild.product.type == 'mission' and not self:isMissionValid(self.currentBuild.product) then
				env.info('ZoneCommand:progressBuild '..self.name..' - stopping build, mission no longer valid')
				self.currentBuild = nil
			else
				local cost = self.currentBuild.product.cost
				if self.currentBuild.isRepair then
					cost = math.floor(self.currentBuild.product.cost/2)
				end
				
				if self.currentBuild.progress < cost then
					if self.currentBuild.isRepair and not Group.getByName(self.currentBuild.product.name) then
						env.info('ZoneCommand:progressBuild '..self.name..' - stopping build, group to repair no longer exists')
						self.currentBuild = nil
					else
						if self.currentBuild.isRepair then
							local gr = Group.getByName(self.currentBuild.product.name)
							if gr and self.currentBuild.unitcount and gr:getSize() < self.currentBuild.unitcount then
								env.info('ZoneCommand:progressBuild '..self.name..' - restarting build, group to repair has casualties')
								self.currentBuild.unitcount = gr:getSize()
								self:addResource(self.currentBuild.progress)
								self.currentBuild.progress = 0
							end
						end

						local step = math.floor(ZoneCommand.buildSpeed * self.boostScale)
						if self.currentBuild.product.type == ZoneCommand.productTypes.mission then
							if self.currentBuild.product.missionType == ZoneCommand.missionTypes.supply_air or
								self.currentBuild.product.missionType == ZoneCommand.missionTypes.supply_convoy or
								self.currentBuild.product.missionType == ZoneCommand.missionTypes.supply_transfer then
								step = math.floor(ZoneCommand.supplyBuildSpeed * self.boostScale)

								if self.currentBuild.product.missionType == ZoneCommand.missionTypes.supply_transfer then
									step = math.floor(step*2)
								end
							end
						end
						
						if step > self.resource then step = 1 end
						if step <= self.resource then
							self:removeResource(step)
							self.currentBuild.progress = self.currentBuild.progress + step

							if self.extraBuildResources > 0 then
								local extrastep = step
								if self.extraBuildResources < extrastep then
									extrastep = self.extraBuildResources
								end

								self.extraBuildResources = math.max(self.extraBuildResources - extrastep, 0)
								self.currentBuild.progress = self.currentBuild.progress + extrastep
								
								env.info('ZoneCommand:progressBuild - '..self.name..' consumed '..extrastep..' extra resources, remaining '..self.extraBuildResources)
							end
						end
					end
				else
					if self.currentBuild.product.type == 'mission' then
						if self:isMissionValid(self.currentBuild.product) then
							self:activateMission(self.currentBuild.product)
						else
							self:addResource(self.currentBuild.product.cost)
						end
					elseif self.currentBuild.product.type == 'defense' or self.currentBuild.product.type=='upgrade' then
						if self.currentBuild.isRepair then
							if Group.getByName(self.currentBuild.product.name) then
								self.zone:spawnGroup(self.currentBuild.product)
							end
						else
							self.zone:spawnGroup(self.currentBuild.product)
						end
						
						self.built[self.currentBuild.product.name] = self.currentBuild.product
					end
					
					self.currentBuild = nil
				end
			end
		end

		if self.currentMissionBuild then
			if self.currentMissionBuild.product.type == 'mission' and not self:isMissionValid(self.currentMissionBuild.product) then
				env.info('ZoneCommand:progressBuild '..self.name..' - stopping build, mission no longer valid')
				self.currentMissionBuild = nil
			else
				local cost = self.currentMissionBuild.product.cost
				
				if self.currentMissionBuild.progress < cost then
					local step = math.floor(ZoneCommand.buildSpeed * self.boostScale)

					if step > self.resource then step = 1 end

					local progress = step*self.missionBuildSpeedReduction
					local reducedCost = math.max(1, math.floor(progress))
					if reducedCost <= self.resource then
						self:removeResource(reducedCost)
						self.currentMissionBuild.progress = self.currentMissionBuild.progress + progress
					end
				else
					if self:isMissionValid(self.currentMissionBuild.product) then
						self:activateMission(self.currentMissionBuild.product)
					else
						self:addResource(self.currentMissionBuild.product.cost)
					end
					
					self.currentMissionBuild = nil
				end
			end
		end
	end
	
	function ZoneCommand:queueBuild(product, side, isRepair, progress)
		if product.type ~= ZoneCommand.productTypes.mission or 
			(product.missionType == ZoneCommand.missionTypes.supply_air or
			product.missionType == ZoneCommand.missionTypes.supply_convoy or
			product.missionType == ZoneCommand.missionTypes.supply_transfer) then
				
			local unitcount = nil
			if isRepair then
				local g = Group.getByName(product.name)
				if g then
					unitcount = g:getSize()
					env.info('ZoneCommand:queueBuild - '..self.name..' '..product.name..' has '..unitcount..' units')
				end
			end
			
			self.currentBuild = { product = product, progress = (progress or 0), side = side, isRepair = isRepair, unitcount = unitcount}
			env.info('ZoneCommand:queueBuild - '..self.name..' chose '..product.name..'('..product.display..') as its build')
		else
			self.currentMissionBuild = { product = product, progress = (progress or 0), side = side}
			env.info('ZoneCommand:queueBuild - '..self.name..' chose '..product.name..'('..product.display..') as its mission build')
		end
	end

	function ZoneCommand:reserveMission(product)
		self.reservedMissions[product.name] = product
	end

	function ZoneCommand:unReserveMission(product)
		self.reservedMissions[product.name] = nil
	end

	function ZoneCommand:isMissionValid(product)
		if Group.getByName(product.name) then return false end

		if self.reservedMissions[product.name] then
			return false
		end

		if product.missionType == ZoneCommand.missionTypes.supply_convoy then
			if self.distToFront == nil then return false end

			for _,tgt in pairs(self.neighbours) do
				if self:isSupplyMissionValid(product, tgt) then 
					return true 
				end
			end
		elseif product.missionType == ZoneCommand.missionTypes.supply_transfer then
			if self.distToFront == nil then return false end 
			for _,tgt in pairs(self.neighbours) do
				if self:isSupplyTransferMissionValid(product, tgt) then 
					return true 
				end
			end
		elseif product.missionType == ZoneCommand.missionTypes.supply_air then
			if self.distToFront == nil then return false end

			for _,tgt in pairs(self.neighbours) do
				if self:isSupplyMissionValid(product, tgt) then 
					return true 
				else
					for _,subtgt in pairs(tgt.neighbours) do
						if subtgt.name ~= self.name and self:isSupplyMissionValid(product, subtgt) then
							local dist = mist.utils.get2DDist(self.zone.point, subtgt.zone.point)
							if dist < 50000 then
								return true
							end
						end
					end
				end
			end
		elseif product.missionType == ZoneCommand.missionTypes.assault then
			if self.mode ~= ZoneCommand.modes.normal then return false end
			for _,tgt in pairs(self.neighbours) do
				if self:isAssaultMissionValid(product, tgt) then 
					return true 
				end
			end
		elseif product.missionType == ZoneCommand.missionTypes.cas then
			if self.mode ~= ZoneCommand.modes.normal and not self.keepActive then return false end

			for _,tgt in pairs(ZoneCommand.getAllZones()) do
				if self:isCasMissionValid(product, tgt) then 
					return true 
				end
			end
		elseif product.missionType == ZoneCommand.missionTypes.cas_helo then
			if self.mode ~= ZoneCommand.modes.normal and not self.keepActive then return false end

			for _,tgt in pairs(self.neighbours) do
				if self:isCasMissionValid(product, tgt) then 
					return true 
				end
			end
		elseif product.missionType == ZoneCommand.missionTypes.strike then
			if self.mode ~= ZoneCommand.modes.normal and not self.keepActive then return false end

			for _,tgt in pairs(ZoneCommand.getAllZones()) do
				if self:isStrikeMissionValid(product, tgt) then 
					return true 
				end
			end
		elseif product.missionType == ZoneCommand.missionTypes.sead then
			if self.mode ~= ZoneCommand.modes.normal and not self.keepActive then return false end

			for _,tgt in pairs(ZoneCommand.getAllZones()) do
				if self:isSeadMissionValid(product, tgt) then 
					return true 
				end
			end
		elseif product.missionType == ZoneCommand.missionTypes.patrol then
			if self.mode ~= ZoneCommand.modes.normal and not self.keepActive then return false end

			for _,tgt in pairs(ZoneCommand.getAllZones()) do
				if self:isPatrolMissionValid(product, tgt) then 
					return true 
				end
			end
		elseif product.missionType == ZoneCommand.missionTypes.bai then
			if not ZoneCommand.groupMonitor then return false end
			if self.mode ~= ZoneCommand.modes.normal and not self.keepActive then return false end

			for _,tgt in pairs(ZoneCommand.groupMonitor.groups) do
				if self:isBaiMissionValid(product, tgt) then 
					return true
				end	
			end
		elseif product.missionType == ZoneCommand.missionTypes.awacs then
			if not ZoneCommand.groupMonitor then return false end
			if self.mode ~= ZoneCommand.modes.normal and not self.keepActive then return false end
			for _,tgt in pairs(ZoneCommand.getAllZones()) do
				if self:isAwacsMissionValid(product, tgt) then 
					return true
				end	
			end
		elseif product.missionType == ZoneCommand.missionTypes.tanker then
			if not ZoneCommand.groupMonitor then return false end
			if self.mode ~= ZoneCommand.modes.normal and not self.keepActive then return false end
			if not self.distToFront or self.distToFront == 0 then return false end
			for _,tgt in pairs(ZoneCommand.getAllZones()) do
				if self:isTankerMissionValid(product, tgt) then 
					return true
				end	
			end
		end
	end

	function ZoneCommand:activateMission(product)
		if product.missionType == ZoneCommand.missionTypes.supply_convoy then
			self:activateSupplyConvoyMission(product)
		elseif product.missionType == ZoneCommand.missionTypes.assault then
			self:activateAssaultMission(product)
		elseif product.missionType == ZoneCommand.missionTypes.supply_air then
			self:activateAirSupplyMission(product)
		elseif product.missionType == ZoneCommand.missionTypes.supply_transfer then
			self:activateSupplyTransferMission(product)
		elseif product.missionType == ZoneCommand.missionTypes.cas then
			self:activateCasMission(product)
		elseif product.missionType == ZoneCommand.missionTypes.cas_helo then
			self:activateCasMission(product, true)
		elseif product.missionType == ZoneCommand.missionTypes.strike then
			self:activateStrikeMission(product)
		elseif product.missionType == ZoneCommand.missionTypes.sead then
			self:activateSeadMission(product)
		elseif product.missionType == ZoneCommand.missionTypes.patrol then
			self:activatePatrolMission(product)
		elseif product.missionType == ZoneCommand.missionTypes.bai then
			self:activateBaiMission(product)
		elseif product.missionType == ZoneCommand.missionTypes.awacs then
			self:activateAwacsMission(product)
		elseif product.missionType == ZoneCommand.missionTypes.tanker then
			self:activateTankerMission(product)
		end

		env.info('ZoneCommand:activateMission - '..self.name..' activating mission '..product.name..'('..product.display..')')
	end

	function ZoneCommand:reActivateMission(savedData)
		local product = self:getProductByName(savedData.productName)

		if product.missionType == ZoneCommand.missionTypes.supply_convoy then
			self:reActivateSupplyConvoyMission(product, savedData)
		elseif product.missionType == ZoneCommand.missionTypes.assault then
			self:reActivateAssaultMission(product, savedData)
		elseif product.missionType == ZoneCommand.missionTypes.supply_air then
			self:reActivateAirSupplyMission(product, savedData)
		elseif product.missionType == ZoneCommand.missionTypes.supply_transfer then
			self:reActivateSupplyTransferMission(product, savedData)
		elseif product.missionType == ZoneCommand.missionTypes.cas then
			self:reActivateCasMission(product, nil, savedData)
		elseif product.missionType == ZoneCommand.missionTypes.cas_helo then
			self:reActivateCasMission(product, true, savedData)
		elseif product.missionType == ZoneCommand.missionTypes.strike then
			self:reActivateStrikeMission(product, savedData)
		elseif product.missionType == ZoneCommand.missionTypes.sead then
			self:reActivateSeadMission(product, savedData)
		elseif product.missionType == ZoneCommand.missionTypes.patrol then
			self:reActivatePatrolMission(product, savedData)
		elseif product.missionType == ZoneCommand.missionTypes.bai then
			self:reActivateBaiMission(product, savedData)
		elseif product.missionType == ZoneCommand.missionTypes.awacs then
			self:reActivateAwacsMission(product, savedData)
		elseif product.missionType == ZoneCommand.missionTypes.tanker then
			self:reActivateTankerMission(product, savedData)
		end

		env.info('ZoneCommand:reActivateMission - '..self.name..' reactivating mission '..product.name..'('..product.display..')')
	end

	local function getDefaultPos(savedData, isAir)
		local action = 'Off Road'
		local speed = 0
		if isAir then
			action = 'Turning Point'
			speed = 250
		end

		local vars = {
			groupName = savedData.productName,
			point = savedData.position,
			action = 'respawn',
			heading = savedData.heading,
			initTasks = false,
			route = { 
				[1] = {
					alt = savedData.position.y,
					type = 'Turning Point',
					action = action,
					alt_type = 'BARO',
					x = savedData.position.x,
					y = savedData.position.z,
					speed = speed
				}
			}
		}

		return vars
	end

	local function teleportToPos(groupName, pos)
		if pos.y == nil then
			pos.y = land.getHeight({ x = pos.x, y = pos.z })
		end

		local vars = {
			groupName = groupName,
			point = pos,
			action = 'respawn',
			initTasks = false
		}

		mist.teleportToPoint(vars)
	end

	function ZoneCommand:reActivateSupplyConvoyMission(product, savedData)
		local zone = ZoneCommand.getZoneByName(savedData.lastMission.zoneName)

		local supplyPoint = trigger.misc.getZone(zone.name..'-sp')
		if not supplyPoint then
			supplyPoint = trigger.misc.getZone(zone.name)
		end
		if supplyPoint then 
			mist.teleportToPoint(getDefaultPos(savedData, false))
			if ZoneCommand.groupMonitor then
				ZoneCommand.groupMonitor:registerGroup(product, zone, self, savedData)
			end

			product.lastMission = {zoneName = zone.name}
			timer.scheduleFunction(function(param)
				local gr = Group.getByName(param.name)
				TaskExtensions.moveOnRoadToPoint(gr, param.point)
			end, {name=product.name, point={ x=supplyPoint.point.x, y = supplyPoint.point.z}}, timer.getTime()+1)
		end
	end
	
	function ZoneCommand:reActivateAssaultMission(product, savedData)
		local zone = ZoneCommand.getZoneByName(savedData.lastMission.zoneName)

		local supplyPoint = trigger.misc.getZone(zone.name..'-sp')
		if not supplyPoint then
			supplyPoint = trigger.misc.getZone(zone.name)
		end
		if supplyPoint then 
			mist.teleportToPoint(getDefaultPos(savedData, false))
			if ZoneCommand.groupMonitor then
				ZoneCommand.groupMonitor:registerGroup(product, zone, self, savedData)
			end

			local tgtPoint = trigger.misc.getZone(zone.name)

			if tgtPoint then 
				product.lastMission = {zoneName = zone.name}
				timer.scheduleFunction(function(param)
					local gr = Group.getByName(param.name)
					TaskExtensions.moveOnRoadToPointAndAssault(gr, param.point, param.targets)
				end, {name=product.name, point={ x=tgtPoint.point.x, y = tgtPoint.point.z}, targets=zone.built}, timer.getTime()+1)
			end
		end
	end
	
	function ZoneCommand:reActivateAirSupplyMission(product, savedData)
		local zone = ZoneCommand.getZoneByName(savedData.lastMission.zoneName)

		mist.teleportToPoint(getDefaultPos(savedData, true))
		if ZoneCommand.groupMonitor then
			ZoneCommand.groupMonitor:registerGroup(product, zone, self, savedData)
		end

		local supplyPoint = trigger.misc.getZone(zone.name..'-hsp')
		if not supplyPoint then
			supplyPoint = trigger.misc.getZone(zone.name)
		end

		if supplyPoint then 
			product.lastMission = {zoneName = zone.name}
			local alt = self.connectionManager:getHeliAlt(self.name, zone.name)
			timer.scheduleFunction(function(param)
				local gr = Group.getByName(param.name)
				TaskExtensions.landAtPoint(gr, param.point, param.alt)
			end, {name=product.name, point={ x=supplyPoint.point.x, y = supplyPoint.point.z}, alt = alt}, timer.getTime()+1)
		end
	end
	
	function ZoneCommand:reActivateSupplyTransferMission(product, savedData)
		-- not needed
	end
	
	function ZoneCommand:reActivateCasMission(product, isHelo, savedData)
		local zone = ZoneCommand.getZoneByName(savedData.lastMission.zoneName)

		mist.teleportToPoint(getDefaultPos(savedData, true))
		if ZoneCommand.groupMonitor then
			ZoneCommand.groupMonitor:registerGroup(product, zone, self, savedData)
		end

		local homePos = trigger.misc.getZone(savedData.homeName).point

		if zone then 
			product.lastMission = {zoneName = zone.name}
			timer.scheduleFunction(function(param)
				local gr = Group.getByName(param.prod.name)
				if param.helo then
					TaskExtensions.executeHeloCasMission(gr, param.targets, param.prod.expend, param.prod.altitude, {homePos = homePos})
				else
					TaskExtensions.executeCasMission(gr, param.targets, param.prod.expend, param.prod.altitude, {homePos = homePos})
				end
			end, {prod=product, targets=zone.built, helo = isHelo, homePos = homePos}, timer.getTime()+1)
		end
	end
	
	function ZoneCommand:reActivateStrikeMission(product, savedData)
		local zone = ZoneCommand.getZoneByName(savedData.lastMission.zoneName)

		mist.teleportToPoint(getDefaultPos(savedData, true))

		if ZoneCommand.groupMonitor then
			ZoneCommand.groupMonitor:registerGroup(product, zone, self, savedData)
		end

		local homePos = trigger.misc.getZone(savedData.homeName).point

		if zone then 
			product.lastMission = {zoneName = zone.name}
			timer.scheduleFunction(function(param)
				local gr = Group.getByName(param.prod.name)
				TaskExtensions.executeStrikeMission(gr, param.targets, param.prod.expend, param.prod.altitude, {homePos = homePos})
			end, {prod=product, targets=zone.built, homePos = homePos}, timer.getTime()+1)
		end
	end
	
	function ZoneCommand:reActivateSeadMission(product, savedData)
		local zone = ZoneCommand.getZoneByName(savedData.lastMission.zoneName)

		mist.teleportToPoint(getDefaultPos(savedData, true))
		if ZoneCommand.groupMonitor then
			ZoneCommand.groupMonitor:registerGroup(product, zone, self, savedData)
		end

		local homePos = trigger.misc.getZone(savedData.homeName).point

		if zone then 
			product.lastMission = {zoneName = zone.name}
			timer.scheduleFunction(function(param)
				local gr = Group.getByName(param.prod.name)
				TaskExtensions.executeSeadMission(gr, param.targets, param.prod.expend, param.prod.altitude, {homePos = homePos})
			end, {prod=product, targets=zone.built, homePos = homePos}, timer.getTime()+1)
		end
	end
	
	function ZoneCommand:reActivatePatrolMission(product, savedData)

		local zn1 = ZoneCommand.getZoneByName(savedData.lastMission.zone1name)

		mist.teleportToPoint(getDefaultPos(savedData, true))
		if ZoneCommand.groupMonitor then
			ZoneCommand.groupMonitor:registerGroup(product, zn1, self, savedData)
		end

		local homePos = trigger.misc.getZone(savedData.homeName).point

		if zn1 then 
			product.lastMission = {zone1name = zn1.name}
			timer.scheduleFunction(function(param)
				local gr = Group.getByName(param.prod.name)

				local point = trigger.misc.getZone(param.zone1.name).point

				TaskExtensions.executePatrolMission(gr, point, param.prod.altitude, param.prod.range, {homePos = param.homePos})
			end, {prod=product, zone1 = zn1, homePos = homePos}, timer.getTime()+1)
		end
	end
	
	function ZoneCommand:reActivateBaiMission(product, savedData)
		local targets = {}
		local hasTarget = false
		for _,tgt in pairs(ZoneCommand.groupMonitor.groups) do
			if self:isBaiMissionValid(product, tgt) then 
				targets[tgt.product.name] = tgt.product
				hasTarget = true
			end	
		end
		
		local homePos = trigger.misc.getZone(savedData.homeName).point

		if hasTarget then 
			mist.teleportToPoint(getDefaultPos(savedData, true))
			if ZoneCommand.groupMonitor then
				ZoneCommand.groupMonitor:registerGroup(product, nil, self, savedData)
			end

			product.lastMission = { active = true }
			timer.scheduleFunction(function(param)
				local gr = Group.getByName(param.prod.name)
				TaskExtensions.executeBaiMission(gr, param.targets, param.prod.expend, param.prod.altitude, {homePos = param.homePos})
			end, {prod=product, targets=targets, homePos = homePos}, timer.getTime()+1)
		end
	end
	
	function ZoneCommand:reActivateAwacsMission(product, savedData)
		
		local zone = ZoneCommand.getZoneByName(savedData.lastMission.zoneName)
		local homePos = trigger.misc.getZone(savedData.homeName).point

		mist.teleportToPoint(getDefaultPos(savedData, true))
		if ZoneCommand.groupMonitor then
			ZoneCommand.groupMonitor:registerGroup(product, nil, self, savedData)
		end
		timer.scheduleFunction(function(param)
			local gr = Group.getByName(param.prod.name)
			if gr then
				local un = gr:getUnit(1)
				if un then 
					local callsign = un:getCallsign()
					RadioFrequencyTracker.registerRadio(param.prod.name, '[AWACS] '..callsign, param.prod.freq..' AM')
				end

				local point = trigger.misc.getZone(param.target.name).point
				product.lastMission = { zoneName = param.target.name }
				TaskExtensions.executeAwacsMission(gr, point, param.prod.altitude, param.prod.freq, {homePos = param.homePos})
			end
		end, {prod=product, target=zone, homePos = homePos}, timer.getTime()+1)
	end
	
	function ZoneCommand:reActivateTankerMission(product, savedData)

		local zone = ZoneCommand.getZoneByName(savedData.lastMission.zoneName)

		local homePos = trigger.misc.getZone(savedData.homeName).point
		mist.teleportToPoint(getDefaultPos(savedData, true))
		if ZoneCommand.groupMonitor then
			ZoneCommand.groupMonitor:registerGroup(product, zone, self, savedData)
		end
		
		timer.scheduleFunction(function(param)
			local gr = Group.getByName(param.prod.name)
			if gr then
				local un = gr:getUnit(1)
				if un then 
					local callsign = un:getCallsign()
					RadioFrequencyTracker.registerRadio(param.prod.name, '[Tanker('..param.prod.variant..')] '..callsign, param.prod.freq..' AM | TCN '..param.prod.tacan..'X')
				end

				local point = trigger.misc.getZone(param.target.name).point
				product.lastMission = { zoneName = param.target.name }
				TaskExtensions.executeTankerMission(gr, point, param.prod.altitude, param.prod.freq, param.prod.tacan, {homePos = param.homePos})
			end
		end, {prod=product, target=zone, homePos = homePos}, timer.getTime()+1)
	end

	function ZoneCommand:isBaiMissionValid(product, tgtgroup)
		if product.side == tgtgroup.product.side then return false end
		if tgtgroup.product.type ~= ZoneCommand.productTypes.mission then return false end
		if tgtgroup.product.missionType == ZoneCommand.missionTypes.assault then return true end
		if tgtgroup.product.missionType == ZoneCommand.missionTypes.supply_convoy then return true end
	end

	function ZoneCommand:activateBaiMission(product)
		--{name = product.name, lastStateTime = timer.getAbsTime(), product = product, target = target}
		local targets = {}
		local hasTarget = false
		for _,tgt in pairs(ZoneCommand.groupMonitor.groups) do
			if self:isBaiMissionValid(product, tgt) then 
				targets[tgt.product.name] = tgt.product
				hasTarget = true
			end	
		end

		if hasTarget then 
			local og = Utils.getOriginalGroup(product.name)
			if og then
				teleportToPos(product.name, {x=og.x, z=og.y})
				env.info("ZoneCommand - activateBaiMission teleporting to OG pos")
			else
				mist.respawnGroup(product.name, true)
				env.info("ZoneCommand - activateBaiMission fallback to respawnGroup")
			end

			if ZoneCommand.groupMonitor then
				ZoneCommand.groupMonitor:registerGroup(product, nil, self)
			end

			product.lastMission = { active = true }
			timer.scheduleFunction(function(param)
				local gr = Group.getByName(param.prod.name)
				TaskExtensions.executeBaiMission(gr, param.targets, param.prod.expend, param.prod.altitude)
			end, {prod=product, targets=targets}, timer.getTime()+1)

			env.info("ZoneCommand - "..product.name.." targeting convoys")
		end
	end

	local function prioritizeSupplyTargets(a,b)
		--if a:criticalOnSupplies() and not b:criticalOnSupplies() then return true end
		--if b:criticalOnSupplies() and not a:criticalOnSupplies() then return false end

		if a.distToFront~=nil and b.distToFront == nil then
			return true
		elseif a.distToFront == nil and b.distToFront ~= nil then
			return false
		elseif a.distToFront == b.distToFront then
			return a.resource < b.resource
		else
			return a.distToFront<b.distToFront
		end
	end

	function ZoneCommand:activateSupplyTransferMission(product)
		local tgtzones = {}
		for _,v in pairs(self.neighbours) do
			if (v.side == 0 or v.side==product.side) then
				table.insert(tgtzones, v)
			end
		end
		
		if #tgtzones == 0 then 
			env.info('ZoneCommand:activateSupplyTransferMission - '..self.name..' no valid tgtzones')
			return 
		end

		table.sort(tgtzones, prioritizeSupplyTargets)

		for i,v in ipairs(tgtzones) do
			if self:isSupplyTransferMissionValid(product, v) then
				-- virtual resourse transfer to save some performance
				v:addResource(product.cost)
				env.info('ZoneCommand:activateSupplyTransferMission - '..self.name..' transfered '..product.cost..' to '..v.name)
				break
			end
		end
	end

	function ZoneCommand:activateAirSupplyMission(product) 
		local tgtzones = {}
		for _,v in pairs(self.neighbours) do
			if (v.side == 0 or v.side==product.side) then
				table.insert(tgtzones, v)

				for _,v2 in pairs(v.neighbours) do
					if v2.name~=self.name and (v2.side == 0 or v2.side==product.side) then
						local dist = mist.utils.get2DDist(self.zone.point, v2.zone.point)
						if dist < 50000 then
							table.insert(tgtzones, v2)
						end
					end
				end
			end
		end
		
		if #tgtzones == 0 then 
			env.info('ZoneCommand:activateAirSupplyMission - '..self.name..' no valid tgtzones')
			return 
		end

		table.sort(tgtzones, prioritizeSupplyTargets)
		local viablezones = {}
		for _,v in ipairs(tgtzones) do
			viablezones[v.name] = v
		end

		if BattlefieldManager and BattlefieldManager.priorityZones[self.side] then
			local prioZone = BattlefieldManager.priorityZones[self.side]
			if prioZone.side == 0 and viablezones[prioZone.name] and self:isSupplyMissionValid(product, prioZone) then
				tgtzones = { prioZone }
			end
		end

		for i,v in ipairs(tgtzones) do
			if self:isSupplyMissionValid(product, v) then

				local og = Utils.getOriginalGroup(product.name)
				if og then
					teleportToPos(product.name, {x=og.x, z=og.y})
					env.info("ZoneCommand - activateAirSupplyMission teleporting to OG pos")
				else
					mist.respawnGroup(product.name, true)
					env.info("ZoneCommand - activateAirSupplyMission fallback to respawnGroup")
				end

				if ZoneCommand.groupMonitor then
					ZoneCommand.groupMonitor:registerGroup(product, v, self)
				end

				local supplyPoint = trigger.misc.getZone(v.name..'-hsp')
				if not supplyPoint then
					supplyPoint = trigger.misc.getZone(v.name)
				end

				if supplyPoint then 
					product.lastMission = {zoneName = v.name}

					local alt = self.connectionManager:getHeliAlt(self.name, v.name)
					timer.scheduleFunction(function(param)
						local gr = Group.getByName(param.name)
						TaskExtensions.landAtPoint(gr, param.point, param.alt )
					end, {name=product.name, point={ x=supplyPoint.point.x, y = supplyPoint.point.z}, alt = alt}, timer.getTime()+1)

					env.info("ZoneCommand - "..product.name.." targeting "..v.name)
				end

				break
			end
		end
	end

	function ZoneCommand:isSupplyTransferMissionValid(product, target)
		if target.side == 0 then
			return false
		end

		if target.side == self.side then 
			if self.distToFront <= 1 or target.distToFront <= 1 then return false end -- skip transfer missions if close to front

			if not target.distToFront or not self.distToFront then
				return false
			end
			
			if target:needsSupplies(product.cost) and target.distToFront < self.distToFront then
				return true
			end
			
			if target:criticalOnSupplies() and self.distToFront<=target.distToFront then
				return true
			end

			if target:criticalOnSupplies() and target.mode == 'normal' then 
				return true
			end
		end
	end

	function ZoneCommand:isSupplyMissionValid(product, target)
		if not self.connectionManager then
			env.info("ZoneCommand - ERROR missing connection manager")
		end
		
		if product.missionType == ZoneCommand.missionTypes.supply_convoy then
			if self.connectionManager:isRoadBlocked(self.name, target.name) then
				return false
			end
		end
		
		if not self.distToFront then return false end
		if not target.distToFront then return false end
		
		if target.side == 0 then
			return true
		end

		if target.side == self.side then 
			if self.distToFront > 1 and target.distToFront > 1 then return false end -- skip regular missions if not close to front

			if self.mode == 'normal' and self.distToFront == 0  and target.distToFront == 0 then
				return target:needsSupplies(product.cost*0.5)
			end
			
			if target:needsSupplies(product.cost*0.5) and target.distToFront < self.distToFront then
				return true
			elseif target:criticalOnSupplies() and self.distToFront>=target.distToFront then
				return true
			end

			if target.mode == 'normal' and target:needsSupplies(product.cost*0.5) then 
				return true
			end
		end
	end

	function ZoneCommand:activateSupplyConvoyMission(product)
		local tgtzones = {}
		for _,v in pairs(self.neighbours) do
			if (v.side == 0 or v.side==product.side) then
				table.insert(tgtzones, v)
			end
		end
		
		if #tgtzones == 0 then 
			env.info('ZoneCommand:activateSupplyConvoyMission - '..self.name..' no valid tgtzones')
			return 
		end

		table.sort(tgtzones, prioritizeSupplyTargets)

		if BattlefieldManager and BattlefieldManager.priorityZones[self.side] then
			local prioZone = BattlefieldManager.priorityZones[self.side]
			if prioZone.side == 0 and self.neighbours[prioZone.name] and self:isSupplyMissionValid(product, prioZone) then
				tgtzones = { prioZone }
			end
		end

		for i,v in ipairs(tgtzones) do
			if self:isSupplyMissionValid(product, v) then

				local supplyPoint = trigger.misc.getZone(v.name..'-sp')
				if not supplyPoint then
					supplyPoint = trigger.misc.getZone(v.name)
				end
				
				if supplyPoint then 

					local og = Utils.getOriginalGroup(product.name)
					if og then
						teleportToPos(product.name, {x=og.x, z=og.y})
						env.info("ZoneCommand - activateSupplyConvoyMission teleporting to OG pos")
					else
						mist.respawnGroup(product.name, true)
						env.info("ZoneCommand - activateSupplyConvoyMission fallback to respawnGroup")
					end

					if ZoneCommand.groupMonitor then
						ZoneCommand.groupMonitor:registerGroup(product, v, self)
					end

					product.lastMission = {zoneName = v.name}
					timer.scheduleFunction(function(param)
						local gr = Group.getByName(param.name)
						TaskExtensions.moveOnRoadToPoint(gr, param.point)
					end, {name=product.name, point={ x=supplyPoint.point.x, y = supplyPoint.point.z}}, timer.getTime()+1)
					
					env.info("ZoneCommand - "..product.name.." targeting "..v.name)
				end

				break
			end
		end
	end

	function ZoneCommand:isAssaultMissionValid(product, target)
		if not self.connectionManager then
			env.info("ZoneCommand - ERROR missing connection manager")
		end

		if product.missionType == ZoneCommand.missionTypes.assault then
			if self.connectionManager:isRoadBlocked(self.name, target.name) then
				return false
			end
		end

		if target.side ~= product.side and target.side ~= 0 then
			return true
		end
	end

	function ZoneCommand:activateAssaultMission(product)
		local tgtzones = {}
		for _,v in pairs(self.neighbours) do
			table.insert(tgtzones, {zone = v, rank = math.random()})
		end

		table.sort(tgtzones, function(a,b) return a.rank < b.rank end)

		local sorted = {}
		for i,v in ipairs(tgtzones) do
			table.insert(sorted, v.zone)
		end
		tgtzones = sorted

		if BattlefieldManager and BattlefieldManager.priorityZones[self.side] then
			local prioZone = BattlefieldManager.priorityZones[self.side]
			if self.neighbours[prioZone.name] and self:isAssaultMissionValid(product, prioZone) then
				tgtzones = { prioZone }
			end
		end

		for i,v in ipairs(tgtzones) do
			if self:isAssaultMissionValid(product, v) then

				local og = Utils.getOriginalGroup(product.name)
				if og then
					teleportToPos(product.name, {x=og.x, z=og.y})
					env.info("ZoneCommand - activateAssaultMission teleporting to OG pos")
				else
					mist.respawnGroup(product.name, true)
					env.info("ZoneCommand - activateAssaultMission fallback to respawnGroup")
				end

				if ZoneCommand.groupMonitor then
					ZoneCommand.groupMonitor:registerGroup(product, v, self)
				end

				local tgtPoint = trigger.misc.getZone(v.name)

				if tgtPoint then 
					product.lastMission = {zoneName = v.name}
					timer.scheduleFunction(function(param)
						local gr = Group.getByName(param.name)
						TaskExtensions.moveOnRoadToPointAndAssault(gr, param.point, param.targets)
					end, {name=product.name, point={ x=tgtPoint.point.x, y = tgtPoint.point.z}, targets=v.built}, timer.getTime()+1)

					env.info("ZoneCommand - "..product.name.." targeting "..v.name)
				end

				break
			end
		end
	end
	
	function ZoneCommand:isAwacsMissionValid(product, target)
		if target.side ~= product.side then return false end
		if target.name == self.name then return false end
		if not target.distToFront or target.distToFront ~= 4 then return false end
		
		return true
	end

	function ZoneCommand:activateAwacsMission(product)
		local tgtzones = {}
		for _,v in pairs(ZoneCommand.getAllZones()) do
			if self:isAwacsMissionValid(product, v) then
				table.insert(tgtzones, v)
			end
		end

		local choice1 = math.random(1,#tgtzones)
		local zn = tgtzones[choice1]

		local og = Utils.getOriginalGroup(product.name)
		if og then
			teleportToPos(product.name, {x=og.x, z=og.y})
			env.info("ZoneCommand - activateAwacsMission teleporting to OG pos")
		else
			mist.respawnGroup(product.name, true)
			env.info("ZoneCommand - activateAwacsMission fallback to respawnGroup")
		end

		if ZoneCommand.groupMonitor then
			ZoneCommand.groupMonitor:registerGroup(product, zn, self)
		end
		timer.scheduleFunction(function(param)
			local gr = Group.getByName(param.prod.name)
			if gr then
				local un = gr:getUnit(1)
				if un then 
					local callsign = un:getCallsign()
					RadioFrequencyTracker.registerRadio(param.prod.name, '[AWACS] '..callsign, param.prod.freq..' AM')
				end

				local point = trigger.misc.getZone(param.target.name).point
				product.lastMission = { zoneName = param.target.name }
				TaskExtensions.executeAwacsMission(gr, point, param.prod.altitude, param.prod.freq)
				
			end
		end, {prod=product, target=zn}, timer.getTime()+1)

		env.info("ZoneCommand - "..product.name.." targeting "..zn.name)
	end

	function ZoneCommand:isTankerMissionValid(product, target)
		if target.side ~= product.side then return false end
		if target.name == self.name then return false end
		if not target.distToFront or target.distToFront ~= 4 then return false end
		
		return true
	end

	function ZoneCommand:activateTankerMission(product)

		local tgtzones = {}
		for _,v in pairs(ZoneCommand.getAllZones()) do
			if self:isTankerMissionValid(product, v) then
				table.insert(tgtzones, v)
			end
		end

		local choice1 = math.random(1,#tgtzones)
		local zn = tgtzones[choice1]
		table.remove(tgtzones, choice1)

		local og = Utils.getOriginalGroup(product.name)
		if og then
			teleportToPos(product.name, {x=og.x, z=og.y})
			env.info("ZoneCommand - activateTankerMission teleporting to OG pos")
		else
			mist.respawnGroup(product.name, true)
			env.info("ZoneCommand - activateTankerMission fallback to respawnGroup")
		end

		if ZoneCommand.groupMonitor then
			ZoneCommand.groupMonitor:registerGroup(product, zn, self)
		end

		timer.scheduleFunction(function(param)
			local gr = Group.getByName(param.prod.name)
			if gr then
				local un = gr:getUnit(1)
				if un then 
					local callsign = un:getCallsign()
					RadioFrequencyTracker.registerRadio(param.prod.name, '[Tanker('..param.prod.variant..')] '..callsign, param.prod.freq..' AM | TCN '..param.prod.tacan..'X')
				end

				local point = trigger.misc.getZone(param.target.name).point
				product.lastMission = { zoneName = param.target.name }
				TaskExtensions.executeTankerMission(gr, point, param.prod.altitude, param.prod.freq, param.prod.tacan)
			end
		end, {prod=product, target=zn}, timer.getTime()+1)
		
		env.info("ZoneCommand - "..product.name.." targeting "..zn.name)
	end

	function ZoneCommand:isPatrolMissionValid(product, target)
		--if target.side ~= product.side then return false end
		if target.name == self.name then return false end
		if not target.distToFront or target.distToFront > 1 then return false end
		if target.side ~= product.side and target.side ~= 0 then return false end
		local dist = mist.utils.get2DDist(self.zone.point, target.zone.point)
		if dist > 150000 then return false end
		
		return true
	end

	function ZoneCommand:activatePatrolMission(product)
		local tgtzones = {}
		for _,v in pairs(ZoneCommand.getAllZones()) do
			if self:isPatrolMissionValid(product, v) then
				table.insert(tgtzones, v)
			end
		end

		local choice1 = math.random(1,#tgtzones)
		local zn1 = tgtzones[choice1]

		if BattlefieldManager and BattlefieldManager.priorityZones[self.side] then
			local prioZone = BattlefieldManager.priorityZones[self.side]
			if self:isPatrolMissionValid(product, prioZone) then
				zn1 = prioZone
			end
		end

		local og = Utils.getOriginalGroup(product.name)
		if og then
			teleportToPos(product.name, {x=og.x, z=og.y})
			env.info("ZoneCommand - activatePatrolMission teleporting to OG pos")
		else
			mist.respawnGroup(product.name, true)
			env.info("ZoneCommand - activatePatrolMission fallback to respawnGroup")
		end

		if ZoneCommand.groupMonitor then
			ZoneCommand.groupMonitor:registerGroup(product, zn1, self)
		end

		if zn1 then 
			product.lastMission = {zone1name = zn1.name}
			timer.scheduleFunction(function(param)
				local gr = Group.getByName(param.prod.name)

				local point = trigger.misc.getZone(param.zone1.name).point

				TaskExtensions.executePatrolMission(gr, point, param.prod.altitude, param.prod.range)
			end, {prod=product, zone1 = zn1}, timer.getTime()+1)

			env.info("ZoneCommand - "..product.name.." targeting "..zn1.name)
		end
	end

	function ZoneCommand:isSeadMissionValid(product, target)
		if target.side == 0 then return false end
		if not target.distToFront or target.distToFront > 1 then return false end
		
		--if MissionTargetRegistry.isZoneTargeted(target.name) then return false end

		return target:hasEnemySAMRadar(product)
	end

	function ZoneCommand:hasEnemySAMRadar(product)
		if product.side == 1 then
			return self:hasSAMRadarOnSide(2)
		elseif product.side == 2 then
			return self:hasSAMRadarOnSide(1)
		end
	end

	function ZoneCommand:hasSAMRadarOnSide(side)
		for i,v in pairs(self.built) do
			if v.type == ZoneCommand.productTypes.defense and v.side == side then 
				local gr = Group.getByName(v.name)
				if gr then
					for _,unit in ipairs(gr:getUnits()) do
						if unit:hasAttribute('SAM SR') or unit:hasAttribute('SAM TR') then
							return true
						end
					end
				end
			end
		end
	end

	function ZoneCommand:hasRunway()
		local zones = self:getRunwayZones()
		return #zones > 0
	end

	function ZoneCommand:getRunwayZones()
		local runways = {}
		for i=1,10,1 do
			local name = self.name..'-runway-'..i
			local zone = trigger.misc.getZone(name)
			if zone then 
				runways[i] = {name = name, zone = zone}
			else
				break
			end
		end

		return runways
	end

	function ZoneCommand:getRandomUnitWithAttributeOnSide(attributes, side)
		local available = {}
		for i,v in pairs(self.built) do
			if v.type == ZoneCommand.productTypes.upgrade and v.side == side then
				local st = StaticObject.getByName(v.name)
				if st then
					for _,a in ipairs(attributes) do
						if a == "Buildings" and ZoneCommand.staticRegistry[v.name] then -- dcs does not consider all statics buildings so we compensate
							table.insert(available, v)
						end
					end
				end
			elseif v.type == ZoneCommand.productTypes.defense and v.side == side then 
				local gr = Group.getByName(v.name)
				if gr then
					for _,unit in ipairs(gr:getUnits()) do
						for _,a in ipairs(attributes) do
							if unit:hasAttribute(a) then
								table.insert(available, v)
							end
						end
					end
				end
			end
		end

		if #available > 0 then
			return available[math.random(1, #available)]
		end
	end

	function ZoneCommand:hasUnitWithAttributeOnSide(attributes, side, amount)
		local count = 0

		for i,v in pairs(self.built) do
			if v.type == ZoneCommand.productTypes.upgrade and v.side == side then
				local st = StaticObject.getByName(v.name)
				if st then
					for _,a in ipairs(attributes) do
						if a == "Buildings" and ZoneCommand.staticRegistry[v.name] then -- dcs does not consider all statics buildings so we compensate
							if amount==nil then
								return true
							else
								count = count + 1
								if count >= amount then return true end
							end
						end
					end
				end
			elseif v.type == ZoneCommand.productTypes.defense and v.side == side then 
				local gr = Group.getByName(v.name)
				if gr then
					for _,unit in ipairs(gr:getUnits()) do
						for _,a in ipairs(attributes) do
							if unit:hasAttribute(a) then
								if amount==nil then
									return true
								else
									count = count + 1
									if count >= amount then return true end
								end
							end
						end
					end
				end
			end
		end
	end

	function ZoneCommand:getUnitCountWithAttributeOnSide(attributes, side)
		local count = 0

		for i,v in pairs(self.built) do
			if v.type == ZoneCommand.productTypes.upgrade and v.side == side then
				local st = StaticObject.getByName(v.name)
				if st then
					for _,a in ipairs(attributes) do
						if a == "Buildings" and ZoneCommand.staticRegistry[v.name] then
							count = count + 1
							break
						end
					end
				end
			elseif v.type == ZoneCommand.productTypes.defense and v.side == side then 
				local gr = Group.getByName(v.name)
				if gr then
					for _,unit in ipairs(gr:getUnits()) do
						for _,a in ipairs(attributes) do
							if unit:hasAttribute(a) then
								count = count + 1
								break
							end
						end
					end
				end
			end
		end

		return count
	end

	function ZoneCommand:activateSeadMission(product)
		local tgtzones = {}
		for _,v in pairs(ZoneCommand.getAllZones()) do
			if self:isSeadMissionValid(product, v) then
				table.insert(tgtzones, v)
			end
		end
		
		local choice = math.random(1,#tgtzones)
		local target = tgtzones[choice]

		if BattlefieldManager and BattlefieldManager.priorityZones[self.side] then
			local prioZone = BattlefieldManager.priorityZones[self.side]
			if self:isSeadMissionValid(product, prioZone) then
				target = prioZone
			end
		end

		local og = Utils.getOriginalGroup(product.name)
		if og then
			teleportToPos(product.name, {x=og.x, z=og.y})
			env.info("ZoneCommand - activateSeadMission teleporting to OG pos")
		else
			mist.respawnGroup(product.name, true)
			env.info("ZoneCommand - activateSeadMission fallback to respawnGroup")
		end

		if ZoneCommand.groupMonitor then
			ZoneCommand.groupMonitor:registerGroup(product, target, self)
		end

		if target then 
			product.lastMission = {zoneName = target.name}
			timer.scheduleFunction(function(param)
				local gr = Group.getByName(param.prod.name)
				TaskExtensions.executeSeadMission(gr, param.targets, param.prod.expend, param.prod.altitude)
			end, {prod=product, targets=target.built}, timer.getTime()+1)
			
			env.info("ZoneCommand - "..product.name.." targeting "..target.name)
		end
	end

	function ZoneCommand:isStrikeMissionValid(product, target)
		if target.side == 0 then return false end
		if target.side == product.side then return false end
		if not target.distToFront or target.distToFront > 0 then return false end

		if target:hasEnemySAMRadar(product) then return false end

		--if MissionTargetRegistry.isZoneTargeted(target.name) then return false end

		for i,v in pairs(target.built) do
			if v.type == ZoneCommand.productTypes.upgrade and v.side ~= product.side then 
				return true
			end
		end
	end

	function ZoneCommand:activateStrikeMission(product)
		local tgtzones = {}
		for _,v in pairs(ZoneCommand.getAllZones()) do
			if self:isStrikeMissionValid(product, v) then
				table.insert(tgtzones, v)
			end
		end
		
		local choice = math.random(1,#tgtzones)
		local target = tgtzones[choice]

		if BattlefieldManager and BattlefieldManager.priorityZones[self.side] then
			local prioZone = BattlefieldManager.priorityZones[self.side]
			if self:isStrikeMissionValid(product, prioZone) then
				target = prioZone
			end
		end

		local og = Utils.getOriginalGroup(product.name)
		if og then
			teleportToPos(product.name, {x=og.x, z=og.y})
			env.info("ZoneCommand - activateStrikeMission teleporting to OG pos")
		else
			mist.respawnGroup(product.name, true)
			env.info("ZoneCommand - activateStrikeMission fallback to respawnGroup")
		end

		if ZoneCommand.groupMonitor then
			ZoneCommand.groupMonitor:registerGroup(product, target, self)
		end

		if target then 
			product.lastMission = {zoneName = target.name}
			timer.scheduleFunction(function(param)
				local gr = Group.getByName(param.prod.name)
				TaskExtensions.executeStrikeMission(gr, param.targets, param.prod.expend, param.prod.altitude)
			end, {prod=product, targets=target.built}, timer.getTime()+1)
			
			env.info("ZoneCommand - "..product.name.." targeting "..target.name)
		end
	end

	function ZoneCommand:isCasMissionValid(product, target)
		if target.side == product.side then return false end
		if not target.distToFront or target.distToFront > 0 then return false end

		if target:hasEnemySAMRadar(product) then return false end

		--if MissionTargetRegistry.isZoneTargeted(target.name) then return false end
		
		for i,v in pairs(target.built) do
			if v.type == ZoneCommand.productTypes.defense and v.side ~= product.side then 
				return true
			end
		end
	end

	function ZoneCommand:activateCasMission(product, ishelo)
		local viablezones = {}
		if ishelo then
			viablezones = self.neighbours
		else
			viablezones = ZoneCommand.getAllZones()
		end

		local tgtzones = {}
		for _,v in pairs(viablezones) do
			if self:isCasMissionValid(product, v) then
				table.insert(tgtzones, v)
			end
		end
		
		local choice = math.random(1,#tgtzones)
		local target = tgtzones[choice]

		if BattlefieldManager and BattlefieldManager.priorityZones[self.side] then
			local prioZone = BattlefieldManager.priorityZones[self.side]
			if viablezones[prioZone.name] and self:isCasMissionValid(product, prioZone) then
				target = prioZone
			end
		end

		local og = Utils.getOriginalGroup(product.name)
		if og then
			teleportToPos(product.name, {x=og.x, z=og.y})
			env.info("ZoneCommand - activateCasMission teleporting to OG pos")
		else
			mist.respawnGroup(product.name, true)
			env.info("ZoneCommand - activateCasMission fallback to respawnGroup")
		end

		if ZoneCommand.groupMonitor then
			ZoneCommand.groupMonitor:registerGroup(product, target, self)
		end

		if target then 
			product.lastMission = {zoneName = target.name}
			timer.scheduleFunction(function(param)
				local gr = Group.getByName(param.prod.name)
				if param.helo then
					TaskExtensions.executeHeloCasMission(gr, param.targets, param.prod.expend, param.prod.altitude)
				else
					TaskExtensions.executeCasMission(gr, param.targets, param.prod.expend, param.prod.altitude)
				end
			end, {prod=product, targets=target.built, helo = ishelo}, timer.getTime()+1)

			env.info("ZoneCommand - "..product.name.." targeting "..target.name)
		end
	end
	
	function ZoneCommand:defineUpgrades(upgrades)
		self.upgrades = upgrades
		
		for side,sd in ipairs(self.upgrades) do
			for _,v in ipairs(sd) do
				v.side = side
				
				local cat = TemplateDB.getData(v.template)
				if cat.dataCategory == TemplateDB.type.static then
					ZoneCommand.staticRegistry[v.name] = true
				end
				
				for _,v2 in ipairs(v.products) do
					v2.side = side

					if v2.type == "mission" then
						local gr = Group.getByName(v2.name)
						
						if not gr then
							if v2.missionType ~= ZoneCommand.missionTypes.supply_transfer then
								env.info("ZoneCommand - ERROR declared group does not exist in mission: ".. v2.name)
							end
						else
							gr:destroy() 
						end
					end
				end
			end
		end
	end
	
	function ZoneCommand:getProductByName(name)
		for i,v in ipairs(self.upgrades) do
			for i2,v2 in ipairs(v) do
				if v2.name == name then
					return v2
				else
					for i3,v3 in ipairs(v2.products) do
						if v3.name == name then 
							return v3
						end
					end
				end
			end
		end

		return nil
	end

	function ZoneCommand:cleanup()
		local zn = trigger.misc.getZone(self.name)
		local pos =  {
			x = zn.point.x, 
			y = land.getHeight({x = zn.point.x, y = zn.point.z}), 
			z= zn.point.z
		}
		local radius = zn.radius*2
		world.removeJunk({id = world.VolumeType.SPHERE,params = {point = pos, radius = radius}})
	end
end




-----------------[[ END OF ZoneCommand.lua ]]-----------------



-----------------[[ BattlefieldManager.lua ]]-----------------

BattlefieldManager = {}
do
	BattlefieldManager.closeOverride = 27780 -- 15nm
	BattlefieldManager.farOverride = Config.maxDistFromFront -- default 100nm
	BattlefieldManager.boostScale = {[0] = 1.0, [1]=1.0, [2]=1.0}
	BattlefieldManager.noRedZones = false
	BattlefieldManager.noBlueZones = false

	BattlefieldManager.priorityZones = {
		[1] = nil,
		[2] = nil
	}

	BattlefieldManager.overridePriorityZones = {
		[1] = nil,
		[2] = nil
	}
	
	function BattlefieldManager:new()
		local obj = {}
		
		setmetatable(obj, self)
		self.__index = self
		obj:start()
		return obj
	end
	
	function BattlefieldManager:start()
		timer.scheduleFunction(function(param, time)
			local self = param.context
			
			local zones = ZoneCommand.getAllZones()
			local torank = {}
			
			--reset ranks and define frontline
			for name,zone in pairs(zones) do
				zone.distToFront = nil
				zone.closestEnemyDist = nil
				
				if zone.neighbours then
					for nName, nZone in pairs(zone.neighbours) do
						if zone.side ~= nZone.side then
							zone.distToFront = 0
						end
					end
				end
				
				--set dist to closest enemy
				for name2,zone2 in pairs(zones) do
					if zone.side ~= zone2.side then
						local dist = mist.utils.get2DDist(zone.zone.point, zone2.zone.point)
						if not zone.closestEnemyDist or dist < zone.closestEnemyDist then
							zone.closestEnemyDist = dist
						end
					end
				end
			end
			
			for name,zone in pairs(zones) do
				if zone.distToFront == 0 then
					for nName, nZone in pairs(zone.neighbours) do
						if nZone.distToFrount == nil then
							table.insert(torank, nZone)
						end
					end
				end
			end

			-- build ranks of every other zone
			while #torank > 0 do
				local nexttorank = {}
				for _,zone in ipairs(torank) do
					if not zone.distToFront then
						local minrank = 999
						for nName,nZone in pairs(zone.neighbours) do
							if nZone.distToFront then
								if nZone.distToFront<minrank then
									minrank = nZone.distToFront
								end
							else
								table.insert(nexttorank, nZone)
							end
						end
						zone.distToFront = minrank + 1
					end
				end
				torank = nexttorank
			end
			
			for name, zone in pairs(zones) do
				if zone.keepActive then
					if zone.closestEnemyDist and zone.closestEnemyDist > BattlefieldManager.farOverride and zone.distToFront > 3 then
						zone.mode = ZoneCommand.modes.export
					else
						if zone.mode ~= ZoneCommand.modes.normal then
							zone:fullBuild(1.0)
						end
						zone.mode = ZoneCommand.modes.normal
					end
				else
					if not zone.distToFront or zone.distToFront == 0 or (zone.closestEnemyDist and zone.closestEnemyDist < BattlefieldManager.closeOverride) then
						if zone.mode ~= ZoneCommand.modes.normal then
							zone:fullBuild(1.0)
						end
						zone.mode = ZoneCommand.modes.normal
					elseif zone.distToFront == 1 then
						zone.mode = ZoneCommand.modes.supply
					elseif zone.distToFront > 1 then
						zone.mode = ZoneCommand.modes.export
					end
				end

				zone.boostScale = self.boostScale[zone.side]
			end
			
			return time+60
		end, {context = self}, timer.getTime()+1)

		timer.scheduleFunction(function(param, time)
			local self = param.context
			
			local zones = ZoneCommand.getAllZones()
			
			local noRed = true
			local noBlue = true
			for name, zone in pairs(zones) do
				if zone.side == 1 then
					noRed = false
				elseif zone.side == 2 then
					noBlue = false
				end

				if not noRed and not noBlue then
					break
				end
			end

			if noRed then
				BattlefieldManager.noRedZones = true
			end

			if noBlue then
				BattlefieldManager.noBlueZones = true
			end
			
			return time+10
		end, {context = self}, timer.getTime()+1)

		timer.scheduleFunction(function(param, time)
			local self = param.context
			
			local zones = ZoneCommand.getAllZones()
			
			local frontLineRed = {}
			local frontLineBlue = {}
			for name, zone in pairs(zones) do
				if zone.distToFront == 0 then
					if zone.side == 1 then
						table.insert(frontLineRed, zone)
					elseif zone.side == 2 then
						table.insert(frontLineBlue, zone)
					else
						table.insert(frontLineRed, zone)
						table.insert(frontLineBlue, zone)
					end
				end
			end

			if BattlefieldManager.overridePriorityZones[1] and BattlefieldManager.overridePriorityZones[1].ticks > 0 then
				BattlefieldManager.priorityZones[1] = BattlefieldManager.overridePriorityZones[1].zone
				BattlefieldManager.overridePriorityZones[1].ticks = BattlefieldManager.overridePriorityZones[1].ticks - 1
			else
				local redChangeChance = 1
				if BattlefieldManager.priorityZones[1] and BattlefieldManager.priorityZones[1].side ~= 1 then
					redChangeChance = 0.1
				end

				if #frontLineBlue > 0 then
					if math.random() <= redChangeChance then
						BattlefieldManager.priorityZones[1] = frontLineBlue[math.random(1,#frontLineBlue)]
					end
				else
					BattlefieldManager.priorityZones[1] = nil
				end
			end
			
			if BattlefieldManager.overridePriorityZones[2] and BattlefieldManager.overridePriorityZones[2].ticks > 0 then
				BattlefieldManager.priorityZones[2] = BattlefieldManager.overridePriorityZones[2].zone
				BattlefieldManager.overridePriorityZones[2].ticks = BattlefieldManager.overridePriorityZones[2].ticks - 1
			else
				local blueChangeChance = 1
				if BattlefieldManager.priorityZones[2] and BattlefieldManager.priorityZones[2].side ~= 2 then
					blueChangeChance = 0.1
				end
				
				if #frontLineRed > 0 then
					if math.random() <= blueChangeChance then
						BattlefieldManager.priorityZones[2] = frontLineRed[math.random(1,#frontLineRed)]
					end
				else
					BattlefieldManager.priorityZones[2] = nil
				end
			end

			if BattlefieldManager.priorityZones[1] then
				env.info('BattlefieldManager - red priority: '..BattlefieldManager.priorityZones[1].name)
			else
				env.info('BattlefieldManager - red no priority')
			end

			if BattlefieldManager.priorityZones[2] then
				env.info('BattlefieldManager - blue priority: '..BattlefieldManager.priorityZones[2].name)
			else
				env.info('BattlefieldManager - blue no priority')
			end

			if BattlefieldManager.overridePriorityZones[1] and BattlefieldManager.overridePriorityZones[1].ticks == 0 then
				BattlefieldManager.overridePriorityZones[1] = nil
			end

			if BattlefieldManager.overridePriorityZones[2] and BattlefieldManager.overridePriorityZones[2].ticks == 0 then
				BattlefieldManager.overridePriorityZones[2] = nil
			end
			
			return time+(60*30)
		end, {context = self}, timer.getTime()+10)

		timer.scheduleFunction(function(param, time)
			local x = math.random(-50,50) -- the lower limit benefits blue, higher limit benefits red, adjust to increase limit of random boost variance, default (-50,50)
			local boostIntensity = Config.randomBoost -- adjusts the intensity of the random boost variance, default value = 0.0004
			local factor = (x*x*x*boostIntensity)/100  -- the farther x is the higher the factor, negative beneifts blue, pozitive benefits red
			param.context.boostScale[1] = 1.0+factor
			param.context.boostScale[2] = 1.0-factor

			local red = 0
			local blue = 0
			for i,v in pairs(ZoneCommand.getAllZones()) do
				if v.side == 1 then
					red = red + 1
				elseif v.side == 2 then
					blue = blue + 1
				end

				--v:cleanup()
			end

			-- push factor towards coalition with less zones (up to 0.5)
			local multiplier = Config.lossCompensation -- adjust this to boost losing side production(higher means losing side gains more advantage) (default 1.25)
			local total = red + blue
			local redp = (0.5-(red/total))*multiplier
			local bluep = (0.5-(blue/total))*multiplier

			-- cap factor to avoid increasing difficulty until the end
			redp = math.min(redp, 0.15)
			bluep = math.max(bluep, -0.15)

			param.context.boostScale[1] = param.context.boostScale[1] + redp
			param.context.boostScale[2] = param.context.boostScale[2] + bluep

			--limit to numbers above 0
			param.context.boostScale[1] = math.max(0.01,param.context.boostScale[1])
			param.context.boostScale[2] = math.max(0.01,param.context.boostScale[2])

			env.info('BattlefieldManager - power red = '..param.context.boostScale[1])
			env.info('BattlefieldManager - power blue = '..param.context.boostScale[2])

			return time+(60*30)
		end, {context = self}, timer.getTime()+1)
	end
	
	function BattlefieldManager.overridePriority(side, zone, ticks)
		BattlefieldManager.overridePriorityZones[side] = { zone = zone, ticks = ticks }
		BattlefieldManager.priorityZones[side] = zone
		
		env.info('BattlefieldManager.overridePriority - '..side..' focusing on '..zone.name)
	end
end

-----------------[[ END OF BattlefieldManager.lua ]]-----------------



-----------------[[ Preset.lua ]]-----------------

Preset = {}
do
    function Preset:new(obj)
		setmetatable(obj, self)
		self.__index = self
		return obj
    end

	function Preset:extend(new)
		return Preset:new(Utils.merge(self, new))
	end
end

-----------------[[ END OF Preset.lua ]]-----------------



-----------------[[ PlayerTracker.lua ]]-----------------

PlayerTracker = {}
do
    PlayerTracker.savefile = 'player_stats.json'
    PlayerTracker.statTypes = {
        xp = 'XP',
        cmd = "CMD"
    }

    PlayerTracker.cmdShopTypes = {
        smoke = 'smoke',
        prio = 'prio',
        jtac = 'jtac',
        bribe1 = 'bribe1',
        bribe2 = 'bribe2',
    }

    PlayerTracker.cmdShopPrices = {
        [PlayerTracker.cmdShopTypes.smoke] = 1,
        [PlayerTracker.cmdShopTypes.prio] = 2,
        [PlayerTracker.cmdShopTypes.jtac] = 3,
        [PlayerTracker.cmdShopTypes.bribe1] = 1,
        [PlayerTracker.cmdShopTypes.bribe2] = 3,
    }

	function PlayerTracker:new(markerCommands)
		local obj = {}
        obj.markerCommands = markerCommands
        obj.stats = {}
        obj.tempStats = {}
        obj.groupMenus = {}
        obj.groupShopMenus = {}
        obj.groupTgtMenus = {}
        obj.playerAircraft = {}
        obj.playerWeaponStock = {}

        if lfs then 
            local dir = lfs.writedir()..'Missions/Saves/'
            lfs.mkdir(dir)
            PlayerTracker.savefile = dir..PlayerTracker.savefile
            env.info('Pretense - Player stats file path: '..PlayerTracker.savefile)
        end

        local save = Utils.loadTable(PlayerTracker.savefile)
        if save then 
            obj.stats = save.stats or {}
            obj.playerWeaponStock = save.playerWeaponStock or {}
        end

		setmetatable(obj, self)
		self.__index = self
		
        obj:init()

		return obj
	end

    function PlayerTracker:init()
        local ev = {}
        ev.context = self
        function ev:onEvent(event)
            if not event.initiator then return end
            if not event.initiator.getPlayerName then return end
            if not event.initiator.getCoalition then return end

            local player = event.initiator:getPlayerName()
            if not player then return end
            
            if event.id==world.event.S_EVENT_PLAYER_ENTER_UNIT then
                if event.initiator and event.initiator:getCategory() == Object.Category.UNIT and 
                    (event.initiator:getDesc().category == Unit.Category.AIRPLANE or event.initiator:getDesc().category == Unit.Category.HELICOPTER)  then
                    
                        local pname = event.initiator:getPlayerName()
                        if pname then
                            local gr = event.initiator:getGroup()
                            if trigger.misc.getUserFlag(gr:getName())==1 then
                                trigger.action.outTextForGroup(gr:getID(), 'Can not spawn as '..gr:getName()..' in enemy/neutral zone',5)
                                event.initiator:destroy()
                            end
                        end
                end
            end

            if event.id == world.event.S_EVENT_BIRTH then
                -- init stats for player if not exist
                if not self.context.stats[player] then
                    self.context.stats[player] = {}
                end

                -- reset temp track for player
                self.context.tempStats[player] = nil
                -- reset playeraircraft
                self.context.playerAircraft[player] = nil
            end

            if event.id == world.event.S_EVENT_KILL then
                local target = event.target
                
                if not target then return end
                if not target.getCoalition then return end
                
                if target:getCoalition() == event.initiator:getCoalition() then return end
                
                local xpkey = PlayerTracker.statTypes.xp
                local award = PlayerTracker.getXP(target)

                local instantxp = math.floor(award*0.25)
                local tempxp = award - instantxp

                self.context:addStat(player, instantxp, PlayerTracker.statTypes.xp)
                local msg = '[XP] '..self.context.stats[player][xpkey]..' (+'..instantxp..')'
                env.info("PlayerTracker.kill - "..player..' awarded '..tostring(instantxp)..' xp')
                
                self.context:addTempStat(player, tempxp, PlayerTracker.statTypes.xp)
                msg = msg..'\n+'..tempxp..' XP (unclaimed)'
                env.info("PlayerTracker.kill - "..player..' awarded '..tostring(tempxp)..' xp (unclaimed)')

                trigger.action.outTextForUnit(event.initiator:getID(), msg, 5)
            end

            if event.id==world.event.S_EVENT_EJECTION then
				self.context.stats[player] = self.context.stats[player] or {}
                local ts = self.context.tempStats[player]
                if ts then
                    local un = event.initiator
                    local key = PlayerTracker.statTypes.xp
                    local xp = self.context.tempStats[player][key]
                    if xp then
                        local isFree = event.initiator:getGroup():getName():find("(FREE)")
                        trigger.action.outTextForUnit(un:getID(), 'Ejection. 30\% XP claimed', 5)
                        self.context:addStat(player, math.floor(xp*0.3), PlayerTracker.statTypes.xp)
                        trigger.action.outTextForUnit(un:getID(), '[XP] '..self.context.stats[player][key]..' (+'..math.floor(xp*0.3)..')', 5)
                    end
                    
                    self.context.tempStats[player] = nil
                end
			end

            if event.id==world.event.S_EVENT_TAKEOFF then
                local un = event.initiator
                local zn = ZoneCommand.getZoneOfUnit(event.initiator:getName())
                env.info('PlayerTracker - '..player..' took off in '..tostring(un:getID())..' '..un:getName())
                if un and zn and zn.side == un:getCoalition() then
                    timer.scheduleFunction(function(param, time)
                        local un = param.unit
                        if not un or not un:isExist() then return end
                        local player = param.player
                        local inAir = Utils.isInAir(un)
                        env.info('PlayerTracker - '..player..' checking if in air: '..tostring(inAir))
                        if inAir and param.context.playerAircraft[player] == nil then
                            if param.context.playerAircraft[player] == nil then
                                param.context.playerAircraft[player] = { unitID = un:getID() }
                            end
                        end
                    end, {player = player, unit = event.initiator, context = self.context}, timer.getTime()+10)
                end
			end

            if event.id==world.event.S_EVENT_LAND then
                local un = event.initiator
                local zn = ZoneCommand.getZoneOfUnit(event.initiator:getName())
                local aircraft = self.context.playerAircraft[player]
                env.info('PlayerTracker - '..player..' landed in '..tostring(un:getID())..' '..un:getName())
                if aircraft and un and zn and zn.side == un:getCoalition() then
                    trigger.action.outTextForUnit(event.initiator:getID(), "Wait 10 seconds to validate landing...", 10)
                    timer.scheduleFunction(function(param, time)
                        local un = param.unit
                        if not un or not un:isExist() then return end
                        
                        local player = param.player
                        local isLanded = Utils.isLanded(un, true)
                        local zn = ZoneCommand.getZoneOfUnit(un:getName())

                        env.info('PlayerTracker - '..player..' checking if landed: '..tostring(isLanded))

                        if isLanded then
                            if self.context.tempStats[player] then 
                                if zn and zn.side == un:getCoalition() then
                                    self.context.stats[player] = self.context.stats[player] or {}
                                    
                                    trigger.action.outTextForUnit(un:getID(), 'Rewards claimed', 5)
                                    for _,key in pairs(PlayerTracker.statTypes) do
                                        local value = self.context.tempStats[player][key]
                                        env.info("PlayerTracker.landing - "..player..' redeeming '..tostring(value)..' '..key)
                                        if value then 
                                            self.context:commitTempStat(player, key)
                                            trigger.action.outTextForUnit(un:getID(), key..' +'..value..'', 5)
                                        end
                                    end
                                end
                            end

                            local aircraft = param.context.playerAircraft[player]
                            if aircraft and aircraft.unitID == un:getID() then
                                param.context.playerAircraft[player] = nil
                            end
                        end
                    end, {player = player, unit = event.initiator, context = self.context}, timer.getTime()+10)
                end
                
			end
        end

		world.addEventHandler(ev)
        self:periodicSave()
        self:menuSetup()
    end

    function PlayerTracker:addTempStat(player, amount, stattype)
        self.tempStats[player] = self.tempStats[player] or {}
        self.tempStats[player][stattype] = self.tempStats[player][stattype] or 0
        self.tempStats[player][stattype] = self.tempStats[player][stattype] + amount
    end

    function PlayerTracker:addStat(player, amount, stattype)
        self.stats[player] = self.stats[player] or {}
        self.stats[player][stattype] = self.stats[player][stattype] or 0

        if stattype == PlayerTracker.statTypes.xp then
            local cur = self:getRank(self.stats[player][stattype])
            if cur then 
                local nxt = self:getRank(self.stats[player][stattype] + amount)
                if nxt and cur.rank < nxt.rank then
                    trigger.action.outText(player..' has leveled up to rank: '..nxt.name, 10)
                    if nxt.cmdAward and nxt.cmdAward > 0 then
                        self:addStat(player, nxt.cmdAward, PlayerTracker.statTypes.cmd)
                        trigger.action.outText(player.." awarded "..nxt.cmdAward.." CMD tokens", 10)
                        env.info("PlayerTracker.addStat - Awarded "..player.." "..nxt.cmdAward.." CMD tokens for rank up to "..nxt.name)
                    end
                end
            end
        end

        self.stats[player][stattype] = self.stats[player][stattype] + amount
    end

    function PlayerTracker:commitTempStat(player, statkey)
        local value = self.tempStats[player][statkey]
        if value then 
            self:addStat(player, value, statkey)

            self.tempStats[player][statkey] = nil
        end
    end

    function PlayerTracker:addRankRewards(player, unit, isTemp)
        local rank = self:getPlayerRank(player)
        if not rank then return end

        local cmdChance = rank.cmdChance
        if cmdChance > 0 then 
            local die = math.random()
            if die <= cmdChance then
                if isTemp then
                    self:addTempStat(player, 1, PlayerTracker.statTypes.cmd)
                else
                    self:addStat(player, 1, PlayerTracker.statTypes.cmd)
                end

                local msg = ""
                if isTemp then
                    msg = '+1 CMD (unclaimed)'
                else
                    msg = '[CMD] '..self.stats[player][PlayerTracker.statTypes.cmd]..' (+1)'
                end

                trigger.action.outTextForUnit(unit:getID(), msg, 5)
                env.info("PlayerTracker.addRankRewards - Awarded "..player.." a CMD token with chance "..cmdChance.." die roll "..die)
            end
        end
    end

    function PlayerTracker.getXP(unit)
        local xp = 30

        if unit:hasAttribute('Planes') then xp = xp + 20 end
        if unit:hasAttribute('Helicopters') then xp = xp + 20 end
        if unit:hasAttribute('Infantry') then xp = xp + 10 end
        if unit:hasAttribute('SAM SR') then xp = xp + 15 end
        if unit:hasAttribute('SAM TR') then xp = xp + 15 end
        if unit:hasAttribute('IR Guided SAM') then xp = xp + 10 end
        if unit:hasAttribute('Ships') then xp = xp + 20 end
        if unit:hasAttribute('Buildings') then xp = xp + 30 end
        if unit:hasAttribute('Tanks') then xp = xp + 10 end

        return xp
    end

    function PlayerTracker:menuSetup()
        
        MenuRegistry:register(1, function(event, context)
			if event.id == world.event.S_EVENT_BIRTH and event.initiator and event.initiator.getPlayerName then
				local player = event.initiator:getPlayerName()
				if player then
					local groupid = event.initiator:getGroup():getID()
                    local groupname = event.initiator:getGroup():getName()
					
                    if context.groupMenus[groupid] then
                        missionCommands.removeItemForGroup(groupid, context.groupMenus[groupid])
                        context.groupMenus[groupid] = nil
                    end

                    if not context.groupMenus[groupid] then
                        
                        local menu = missionCommands.addSubMenuForGroup(groupid, 'Information')
                        missionCommands.addCommandForGroup(groupid, 'Player', menu, Utils.log(context.showGroupStats), context, groupname)
                        missionCommands.addCommandForGroup(groupid, 'Frequencies', menu, Utils.log(context.showFrequencies), context, groupname)
                        
                        context.groupMenus[groupid] = menu
                    end
				end
			elseif (event.id == world.event.S_EVENT_PLAYER_LEAVE_UNIT or event.id == world.event.S_EVENT_DEAD) and event.initiator and event.initiator.getPlayerName then
                local player = event.initiator:getPlayerName()
				if player then
					local groupid = event.initiator:getGroup():getID()
					
                    if context.groupMenus[groupid] then
                        missionCommands.removeItemForGroup(groupid, context.groupMenus[groupid])
                        context.groupMenus[groupid] = nil
                    end
				end
            end
		end, self)

        MenuRegistry:register(4, function(event, context)
			if event.id == world.event.S_EVENT_BIRTH and event.initiator and event.initiator.getPlayerName then
				local player = event.initiator:getPlayerName()
				if player then
                    local rank = context:getPlayerRank(player)
                    if not rank then return end

                    if rank.cmdChance > 0 then
                        local groupid = event.initiator:getGroup():getID()
                        local groupname = event.initiator:getGroup():getName()
                        
                        if context.groupShopMenus[groupid] then
                            missionCommands.removeItemForGroup(groupid, context.groupShopMenus[groupid])
                            context.groupShopMenus[groupid] = nil
                        end
                        
                        if context.groupTgtMenus[groupid] then
                            missionCommands.removeItemForGroup(groupid, context.groupTgtMenus[groupid])
                            context.groupTgtMenus[groupid] = nil
                        end

                        if not context.groupShopMenus[groupid] then
                            
                            local menu = missionCommands.addSubMenuForGroup(groupid, 'Command & Control')
                            missionCommands.addCommandForGroup(groupid, 'Deploy Smoke ['..PlayerTracker.cmdShopPrices[PlayerTracker.cmdShopTypes.smoke]..' CMD]', menu, Utils.log(context.buyCommand), context, groupname, PlayerTracker.cmdShopTypes.smoke)
                            missionCommands.addCommandForGroup(groupid, 'Hack enemy comms ['..PlayerTracker.cmdShopPrices[PlayerTracker.cmdShopTypes.bribe1]..' CMD]', menu, Utils.log(context.buyCommand), context, groupname, PlayerTracker.cmdShopTypes.bribe1)
                            missionCommands.addCommandForGroup(groupid, 'Prioritize zone ['..PlayerTracker.cmdShopPrices[PlayerTracker.cmdShopTypes.prio]..' CMD]', menu, Utils.log(context.buyCommand), context, groupname, PlayerTracker.cmdShopTypes.prio)
                            missionCommands.addCommandForGroup(groupid, 'Bribe enemy officer ['..PlayerTracker.cmdShopPrices[PlayerTracker.cmdShopTypes.bribe2]..' CMD]', menu, Utils.log(context.buyCommand), context, groupname, PlayerTracker.cmdShopTypes.bribe2)
                           
                            if CommandFunctions.jtac then
                                missionCommands.addCommandForGroup(groupid, 'Deploy JTAC ['..PlayerTracker.cmdShopPrices[PlayerTracker.cmdShopTypes.jtac]..' CMD]', menu, Utils.log(context.buyCommand), context, groupname, PlayerTracker.cmdShopTypes.jtac)
                            end

                            context.groupShopMenus[groupid] = menu
                        end
                    end
				end
			elseif (event.id == world.event.S_EVENT_PLAYER_LEAVE_UNIT or event.id == world.event.S_EVENT_DEAD) and event.initiator and event.initiator.getPlayerName then
                local player = event.initiator:getPlayerName()
				if player then
					local groupid = event.initiator:getGroup():getID()
					
                    if context.groupShopMenus[groupid] then
                        missionCommands.removeItemForGroup(groupid, context.groupShopMenus[groupid])
                        context.groupShopMenus[groupid] = nil
                    end

                    if context.groupTgtMenus[groupid] then
                        missionCommands.removeItemForGroup(groupid, context.groupTgtMenus[groupid])
                        context.groupTgtMenus[groupid] = nil
                    end
				end
            end
		end, self)
		
        self.markerCommands:addCommand('stats',function(event, _, state) 
            local unit = nil
            if event.initiator then 
                unit = event.initiator
            elseif world.getPlayer() then
                unit = world.getPlayer()
            end

            if not unit then return false end

            state:showGroupStats(unit:getGroup():getName())
            return true
        end, false, self)

        self.markerCommands:addCommand('freqs',function(event, _, state) 
            local unit = nil
            if event.initiator then 
                unit = event.initiator
            elseif world.getPlayer() then
                unit = world.getPlayer()
            end

            if not unit then return false end

            state:showFrequencies(unit:getGroup():getName())
            return true
        end, false, self)
    end

    function PlayerTracker:buyCommand(groupname, itemType)
        local gr = Group.getByName(groupname)
        if gr and gr:getSize()>0 then 
            local un = gr:getUnit(1)
            if un then
                local player = un:getPlayerName()
                local cost = PlayerTracker.cmdShopPrices[itemType]
                local cmdTokens = self.stats[player][PlayerTracker.statTypes.cmd]

                if cmdTokens and cost <= cmdTokens then
                    if self.groupTgtMenus[gr:getID()] then
                        missionCommands.removeItemForGroup(gr:getID(), self.groupTgtMenus[gr:getID()])
                        self.groupTgtMenus[gr:getID()] = nil
                    end

                    if itemType == PlayerTracker.cmdShopTypes.smoke then

                        self.groupTgtMenus[gr:getID()] = MenuRegistry.showTargetZoneMenu(gr:getID(), "Smoke Marker target", function(params) 
                            CommandFunctions.smokeTargets(params.zone, 5)
                            trigger.action.outTextForGroup(params.groupid, "Targets marked at "..params.zone.name.." with red smoke", 5)
                        end, 1, 1)
                        trigger.action.outTextForGroup(gr:getID(), "Select target from radio menu",10)

                    elseif itemType == PlayerTracker.cmdShopTypes.jtac then

                        self.groupTgtMenus[gr:getID()] = MenuRegistry.showTargetZoneMenu(gr:getID(), "JTAC target", function(params) 

                            CommandFunctions.spawnJtac(params.zone)
                            trigger.action.outTextForGroup(params.groupid, "Reaper orbiting "..params.zone.name,5)

                        end, 1, 1)
                        trigger.action.outTextForGroup(gr:getID(), "Select target from radio menu",10)

                    elseif itemType== PlayerTracker.cmdShopTypes.prio then

                        self.groupTgtMenus[gr:getID()] = MenuRegistry.showTargetZoneMenu(gr:getID(), "Priority zone", function(params) 
                            BattlefieldManager.overridePriority(2, params.zone, 2)
                            trigger.action.outTextForGroup(params.groupid, "Blue is concentrating efforts on "..params.zone.name.." for the next hour", 5)
                        end, nil, 1)
                        trigger.action.outTextForGroup(gr:getID(), "Select target from radio menu",10)

                    elseif itemType== PlayerTracker.cmdShopTypes.bribe1 then

                        timer.scheduleFunction(function(params, time)
                            local count = 0
                            for i,v in pairs(ZoneCommand.getAllZones()) do
                                if v.side == 1 and v.distToFront <= 1 then
                                    if math.random()<0.5 then
                                        v:reveal()
                                        count = count + 1
                                    end
                                end
                            end
                            if count > 0 then
                                trigger.action.outTextForGroup(params.groupid, "Intercepted enemy communications have revealed information on "..count.." enemy zones",20)
                            else
                                trigger.action.outTextForGroup(params.groupid, "No useful information has been intercepted",20)
                            end
                        end, {groupid=gr:getID()}, timer.getTime()+60)

                        trigger.action.outTextForGroup(gr:getID(), "Attempting to intercept enemy comms...",60)

                    elseif itemType == PlayerTracker.cmdShopTypes.bribe2 then
                        timer.scheduleFunction(function(params, time)
                            local count = 0
                            for i,v in pairs(ZoneCommand.getAllZones()) do
                                if v.side == 1 then
                                    if math.random()<0.5 then
                                        v:reveal()
                                        count = count + 1
                                    end
                                end
                            end

                            if count > 0 then
                                trigger.action.outTextForGroup(params.groupid, "Bribed officer has shared intel on "..count.." enemy zones",20)
                            else
                                trigger.action.outTextForGroup(params.groupid, "Bribed officer has stopped responding to attempted communications.",20)
                            end
                        end, {groupid=gr:getID()}, timer.getTime()+(60*5))
                        
                        trigger.action.outTextForGroup(gr:getID(), "Bribe has been transfered to enemy officer. Waiting for contact...",20)
                    end
                    
                    self.stats[player][PlayerTracker.statTypes.cmd] = self.stats[player][PlayerTracker.statTypes.cmd] - cost
                else
                    trigger.action.outTextForUnit(un:getID(), "Insufficient CMD to buy selected item", 5)
                end
            end
        end
    end

    function PlayerTracker:showFrequencies(groupname)
        local gr = Group.getByName(groupname)
        if gr then 
            for i,v in pairs(gr:getUnits()) do
                if v.getPlayerName and v:getPlayerName() then
                    local message = RadioFrequencyTracker.getRadioFrequencyMessage(gr:getCoalition())
                    trigger.action.outTextForUnit(v:getID(), message, 20)
                end
            end
        end
    end

    function PlayerTracker:showGroupStats(groupname)
        local gr = Group.getByName(groupname)
        if gr then 
            for i,v in pairs(gr:getUnits()) do
                if v.getPlayerName and v:getPlayerName() then
                    local player = v:getPlayerName()
                    local message = '['..player..']\n'
                    
                    local stats = self.stats[player]
                    if stats then
                        local xp = stats[PlayerTracker.statTypes.xp]
                        if xp then
                            local rank, nextRank = self:getRank(xp)
                            
                            message = message ..'\nXP: '..xp

                            if rank then
                                message = message..'\nRank: '..rank.name
                            end

                            if nextRank then
                                message = message..'\nXP needed for promotion: '..(nextRank.requiredXP-xp)
                            end
                        end

                        local cmd = stats[PlayerTracker.statTypes.cmd]
                        if cmd then
                            message = message ..'\n\nCMD: '..cmd
                        end
                    end

                    local tstats = self.tempStats[player]
                    if tstats then
                        message = message..'\n'
                        local tempxp =  tstats[PlayerTracker.statTypes.xp]
                        if tempxp and tempxp > 0 then
                            message = message .. '\nUnclaimed XP: '..tempxp
                        end
                    end

                    trigger.action.outTextForUnit(v:getID(), message, 10)
                end
            end
        end
    end

    function PlayerTracker:periodicSave()
        timer.scheduleFunction(function(param, time)
            local tosave = {}
            tosave.stats = param.stats
            tosave.playerWeaponStock = param.playerWeaponStock
            
            --temp mission stat tracking
            tosave.zones = {}
            tosave.zones.red = {}
            tosave.zones.blue = {}
            tosave.zones.neutral = {}
            for i,v in pairs(ZoneCommand.getAllZones()) do
                if v.side == 1 then
                    table.insert(tosave.zones.red,v.name)
                elseif v.side == 2 then
                    table.insert(tosave.zones.blue,v.name)
                elseif v.side == 0 then
                    table.insert(tosave.zones.neutral,v.name)
                end
            end

            tosave.players = {}
            for i,v in ipairs(coalition.getPlayers(2)) do
                if v and v:isExist() and v.getPlayerName then
                    table.insert(tosave.players, {name=v:getPlayerName(), unit=v:getDesc().typeName})
                end
            end

            --end mission stat tracking

            Utils.saveTable(PlayerTracker.savefile, tosave)
            env.info("PlayerTracker - state saved")
            return time+60
        end, self, timer.getTime()+60)
    end

    PlayerTracker.ranks = {}
    PlayerTracker.ranks[1] =  { rank=1,  name='E-1 Airman basic',           requiredXP = 0,        cmdChance = 0,       cmdAward=0}
    PlayerTracker.ranks[2] =  { rank=2,  name='E-2 Airman',                 requiredXP = 2000,     cmdChance = 0,       cmdAward=0}
    PlayerTracker.ranks[3] =  { rank=3,  name='E-3 Airman first class',     requiredXP = 4500,     cmdChance = 0,       cmdAward=0}
    PlayerTracker.ranks[4] =  { rank=4,  name='E-4 Senior airman',          requiredXP = 7700,     cmdChance = 0,       cmdAward=0}
    PlayerTracker.ranks[5] =  { rank=5,  name='E-5 Staff sergeant',         requiredXP = 11800,    cmdChance = 0,       cmdAward=0}
    PlayerTracker.ranks[6] =  { rank=6,  name='E-6 Technical sergeant',     requiredXP = 17000,    cmdChance = 0.01,    cmdAward=1}
    PlayerTracker.ranks[7] =  { rank=7,  name='E-7 Master sergeant',        requiredXP = 23500,    cmdChance = 0.02,    cmdAward=1}
    PlayerTracker.ranks[8] =  { rank=8,  name='E-8 Senior master sergeant', requiredXP = 31500,    cmdChance = 0.03,    cmdAward=1}
    PlayerTracker.ranks[9] =  { rank=9,  name='E-9 Chief master sergeant',  requiredXP = 42000,    cmdChance = 0.05,    cmdAward=1}
    PlayerTracker.ranks[10] = { rank=10, name='O-1 Second lieutenant',      requiredXP = 52800,    cmdChance = 0.08,    cmdAward=2}
    PlayerTracker.ranks[11] = { rank=11, name='O-2 First lieutenant',       requiredXP = 66500,    cmdChance = 0.10,    cmdAward=2}
    PlayerTracker.ranks[12] = { rank=12, name='O-3 Captain',                requiredXP = 82500,    cmdChance = 0.14,    cmdAward=2}
    PlayerTracker.ranks[13] = { rank=13, name='O-4 Major',                  requiredXP = 101000,   cmdChance = 0.17,    cmdAward=2}
    PlayerTracker.ranks[14] = { rank=14, name='O-5 Lieutenant colonel',     requiredXP = 122200,   cmdChance = 0.22,    cmdAward=3}
    PlayerTracker.ranks[15] = { rank=15, name='O-6 Colonel',                requiredXP = 146300,   cmdChance = 0.26,    cmdAward=3}
    PlayerTracker.ranks[16] = { rank=16, name='O-7 Brigadier general',      requiredXP = 173500,   cmdChance = 0.32,    cmdAward=3}
    PlayerTracker.ranks[17] = { rank=17, name='O-8 Major general',          requiredXP = 204000,   cmdChance = 0.37,    cmdAward=4}
    PlayerTracker.ranks[18] = { rank=18, name='O-9 Lieutenant general',     requiredXP = 238000,   cmdChance = 0.43,    cmdAward=4}
    PlayerTracker.ranks[19] = { rank=19, name='O-10 General',               requiredXP = 275700,   cmdChance = 0.50,    cmdAward=5}

    function PlayerTracker:getPlayerRank(playername)
        if self.stats[playername] then
            local xp = self.stats[playername][PlayerTracker.statTypes.xp]
            if xp then
                return self:getRank(xp)
            end
        end
    end

    function PlayerTracker:getRank(xp)
        local rank = nil
        local nextRank = nil
        for _, rnk in ipairs(PlayerTracker.ranks) do
            if rnk.requiredXP <= xp then
                rank = rnk
            else
                nextRank = rnk
                break
            end
        end

        return rank, nextRank
    end
end

-----------------[[ END OF PlayerTracker.lua ]]-----------------



-----------------[[ MissionTargetRegistry.lua ]]-----------------

MissionTargetRegistry = {}
do
    MissionTargetRegistry.playerTargetZones = {}

    function MissionTargetRegistry.addZone(zone)
        MissionTargetRegistry.playerTargetZones[zone] = true
    end

    function MissionTargetRegistry.removeZone(zone)
        MissionTargetRegistry.playerTargetZones[zone] = nil
    end

    function MissionTargetRegistry.isZoneTargeted(zone)
        return MissionTargetRegistry.playerTargetZones[zone] ~= nil
    end

    MissionTargetRegistry.baiTargets = {}

    function MissionTargetRegistry.addBaiTarget(target)
        MissionTargetRegistry.baiTargets[target.name] = target
        env.info('MissionTargetRegistry - bai target added '..target.name)
    end

    function MissionTargetRegistry.baiTargetsAvailable(coalition)
        local targets = {}
        for i,v in pairs(MissionTargetRegistry.baiTargets) do
            if v.product.side == coalition then
                local tgt = Group.getByName(v.name)

                if not tgt or not tgt:isExist() or tgt:getSize()==0 then
                    MissionTargetRegistry.removeBaiTarget(v)
                elseif not v.state or v.state ~= 'enroute' then
                    MissionTargetRegistry.removeBaiTarget(v)
                else
                    table.insert(targets, v)
                end
            end
        end

        return #targets > 0
    end

    function MissionTargetRegistry.getRandomBaiTarget(coalition)
        local targets = {}
        for i,v in pairs(MissionTargetRegistry.baiTargets) do
            if v.product.side == coalition then
                local tgt = Group.getByName(v.name)

                if not tgt or not tgt:isExist() or tgt:getSize()==0 then
                    MissionTargetRegistry.removeBaiTarget(v)
                elseif not v.state or v.state ~= 'enroute' then
                    MissionTargetRegistry.removeBaiTarget(v)
                else
                    table.insert(targets, v)
                end
            end
        end

        if #targets == 0 then return end

        local dice = math.random(1,#targets)
        
        return targets[dice]
    end

    function MissionTargetRegistry.removeBaiTarget(target)
        MissionTargetRegistry.baiTargets[target.name] = nil
        env.info('MissionTargetRegistry - bai target removed '..target.name)
    end

    MissionTargetRegistry.strikeTargetExpireTime = 30*60
    MissionTargetRegistry.strikeTargets = {}

    function MissionTargetRegistry.addStrikeTarget(target, zone, isDeep)
        MissionTargetRegistry.strikeTargets[target.name] = {data=target, zone=zone, addedTime = timer.getAbsTime(), isDeep = isDeep}
        env.info('MissionTargetRegistry - strike target added '..target.name)
    end

    function MissionTargetRegistry.strikeTargetsAvailable(coalition, isDeep)
        for i,v in pairs(MissionTargetRegistry.strikeTargets) do
            if v.data.side == coalition then
                local tgt = StaticObject.getByName(v.data.name)
                if not tgt then tgt = Group.getByName(v.data.name) end

                if not tgt or not tgt:isExist() then
                    MissionTargetRegistry.removeStrikeTarget(v)
                elseif timer.getAbsTime() - v.addedTime > MissionTargetRegistry.strikeTargetExpireTime then
                    MissionTargetRegistry.removeStrikeTarget(v)
                elseif v.isDeep == isDeep then
                    return true
                end
            end
        end

        return false
    end

    function MissionTargetRegistry.getRandomStrikeTarget(coalition, isDeep)
        local targets = {}
        for i,v in pairs(MissionTargetRegistry.strikeTargets) do
            if v.data.side == coalition then
                local tgt = StaticObject.getByName(v.data.name)
                if not tgt then tgt = Group.getByName(v.data.name) end

                if not tgt or not tgt:isExist() then
                    MissionTargetRegistry.removeStrikeTarget(v)
                elseif timer.getAbsTime() - v.addedTime > MissionTargetRegistry.strikeTargetExpireTime then
                    MissionTargetRegistry.removeStrikeTarget(v)
                elseif v.isDeep == isDeep then
                    table.insert(targets, v)
                end
            end
        end

        if #targets == 0 then return end

        local dice = math.random(1,#targets)

        return targets[dice]
    end

    function MissionTargetRegistry.removeStrikeTarget(target)
        MissionTargetRegistry.strikeTargets[target.data.name] = nil
        env.info('MissionTargetRegistry - strike target removed '..target.data.name)
    end

    MissionTargetRegistry.extractableSquads = {}

    function MissionTargetRegistry.addSquad(squad)
        MissionTargetRegistry.extractableSquads[squad.name] = squad
        env.info('MissionTargetRegistry - squad added '..squad.name)
    end

    function MissionTargetRegistry.squadsReadyToExtract()
        for i,v in pairs(MissionTargetRegistry.extractableSquads) do
            local gr = Group.getByName(i)
            if gr and gr:isExist() and gr:getSize() > 0 then
                return true
            end
        end

        return false
    end

    function MissionTargetRegistry.getRandomSquad()
        local targets = {}
        for i,v in pairs(MissionTargetRegistry.extractableSquads) do
            local gr = Group.getByName(i)
            if gr and gr:isExist() and gr:getSize() > 0 then
                table.insert(targets, v)
            end
        end

        if #targets == 0 then return end

        local dice = math.random(1,#targets)

        return targets[dice]
    end

    function MissionTargetRegistry.removeSquad(squad)
        MissionTargetRegistry.extractableSquads[squad.name] = nil
        env.info('MissionTargetRegistry - squad removed '..squad.name)
    end

    MissionTargetRegistry.extractablePilots = {}

    function MissionTargetRegistry.addPilot(pilot)
        MissionTargetRegistry.extractablePilots[pilot.name] = pilot
        env.info('MissionTargetRegistry - pilot added '..pilot.name)
    end

    function MissionTargetRegistry.pilotsAvailableToExtract()
        for i,v in pairs(MissionTargetRegistry.extractablePilots) do
            if v.pilot:isExist() and v.pilot:getSize() > 0 and v.remainingTime > 30*60 then
                return true
            end
        end

        return false
    end

    function MissionTargetRegistry.getRandomPilot()
        local targets = {}
        for i,v in pairs(MissionTargetRegistry.extractablePilots) do
            if v.pilot:isExist() and v.pilot:getSize() > 0 and v.remainingTime > 30*60 then
                table.insert(targets, v)
            end
        end

        if #targets == 0 then return end

        local dice = math.random(1,#targets)

        return targets[dice]
    end

    function MissionTargetRegistry.removePilot(pilot)
        MissionTargetRegistry.extractablePilots[pilot.name] = nil
        env.info('MissionTargetRegistry - pilot removed '..pilot.name)
    end
end

-----------------[[ END OF MissionTargetRegistry.lua ]]-----------------



-----------------[[ RadioFrequencyTracker.lua ]]-----------------

RadioFrequencyTracker = {}

do
    RadioFrequencyTracker.radios = {}

    function RadioFrequencyTracker.registerRadio(groupname, name, frequency)
        RadioFrequencyTracker.radios[groupname] = {name = name, frequency = frequency}    
    end

    function RadioFrequencyTracker.getRadioFrequencyMessage(side)
        local radios ={}
        for i,v in pairs(RadioFrequencyTracker.radios) do
            local gr = Group.getByName(i) 
            if gr and gr:getCoalition()==side then
                table.insert(radios, v)
            else
                RadioFrequencyTracker.radios[i] = nil
            end
        end

        table.sort(radios, function (a,b) return a.name < b.name end)

        local msg = 'Active frequencies:'
        for i,v in ipairs(radios) do
            msg = msg..'\n  '..v.name..' ['..v.frequency..']'
        end

        return msg
    end
end


-----------------[[ END OF RadioFrequencyTracker.lua ]]-----------------



-----------------[[ PersistenceManager.lua ]]-----------------

PersistenceManager = {}

do

    function PersistenceManager:new(path, groupManager, squadTracker, csarTracker, playerLogistics)
        local obj = {
            path = path,
            groupManager = groupManager,
            squadTracker = squadTracker,
            csarTracker = csarTracker,
            playerLogistics = playerLogistics,
            data = nil
        }

        setmetatable(obj, self)
		self.__index = self
        return obj
    end

    function PersistenceManager:restoreZones()
        local save = self.data
        for i,v in pairs(save.zones) do
            local z = ZoneCommand.getZoneByName(i)
            if z then
                z:setSide(v.side)
                z.resource = v.resource
                z.revealTime = v.revealTime
                z.extraBuildResources = v.extraBuildResources
                z.mode = v.mode
                z.distToFront = v.distToFront
                z.closestEnemyDist = v.closestEnemyDist
                for name,data in pairs(v.built) do
                    local pr = z:getProductByName(name)
                    z:instantBuild(pr)
    
                    if pr.type == 'defense' and type(data) == "table" then
                        local unitTypes = {}
                        for _,typeName in ipairs(data) do
                            if not unitTypes[typeName] then 
                                unitTypes[typeName] = 0
                            end
                            unitTypes[typeName] = unitTypes[typeName] + 1
                        end
    
                        timer.scheduleFunction(function(param, time)
                            local gr = Group.getByName(param.name)
                            if gr then
                                local types = param.data
                                local toKill = {}
                                for _,un in ipairs(gr:getUnits()) do
                                    local tp = un:getDesc().typeName
                                    if types[tp] and types[tp] > 0 then
                                        types[tp] = types[tp] - 1
                                    else
                                        table.insert(toKill, un)
                                    end
                                end
    
                                for _,un in ipairs(toKill) do
                                    un:destroy()
                                end
                            end
                        end, {data=unitTypes, name=name}, timer.getTime()+2)
                    end
                end
                
                if v.currentBuild then
                    local pr = z:getProductByName(v.currentBuild.name)
                    z:queueBuild(pr, v.currentBuild.side, v.currentBuild.isRepair, v.currentBuild.progress)
                end
    
                if v.currentMissionBuild then
                    local pr = z:getProductByName(v.currentMissionBuild.name)
                    z:queueBuild(pr, v.currentMissionBuild.side, false, v.currentMissionBuild.progress)
                end
                
                z:refreshText()
            end
        end

    end

    function PersistenceManager:restoreAIMissions()
        local save = self.data
        local instantBuildStates = {
            ['uninitialized'] = true,
            ['takeoff'] = true,
        }
    
        local reActivateStates = {
            ['inair'] = true,
            ['enroute'] = true,
            ['atdestination'] = true,
            ['siege'] = true
        }
    
        for i,v in pairs(save.activeGroups) do
            if v.homeName then
                if instantBuildStates[v.state] then
                    local z = ZoneCommand.getZoneByName(v.homeName)
                    if z then
                        local pr = z:getProductByName(v.productName)
                        if z.side == pr.side then
                            z:instantBuild(pr)
                        end
                    end
                elseif v.lastMission and reActivateStates[v.state] then
                    timer.scheduleFunction(function(param, time)
                        local z = ZoneCommand.getZoneByName(param.homeName)
                        if z then
                            z:reActivateMission(param)
                        end
                    end, v, timer.getTime()+3)
                end
            end
        end
    end

    function PersistenceManager:restoreBattlefield()
        local save = self.data
        if save.battlefieldManager then
            if save.battlefieldManager.priorityZones then
                if save.battlefieldManager.priorityZones['1'] then
                    BattlefieldManager.priorityZones[1] = ZoneCommand.getZoneByName(save.battlefieldManager.priorityZones[1])
                end


                if save.battlefieldManager.priorityZones['2'] then
                    BattlefieldManager.priorityZones[2] = ZoneCommand.getZoneByName(save.battlefieldManager.priorityZones[2])
                end
            end

            if save.battlefieldManager.overridePriorityZones then
                if save.battlefieldManager.overridePriorityZones['1'] then
                    BattlefieldManager.overridePriorityZones[1] = {
                        zone = ZoneCommand.getZoneByName(save.battlefieldManager.overridePriorityZones['1'].zone),
                        ticks = save.battlefieldManager.overridePriorityZones['1'].ticks
                    }
                end

                if save.battlefieldManager.overridePriorityZones['2'] then
                    BattlefieldManager.overridePriorityZones[2] = {
                        zone = ZoneCommand.getZoneByName(save.battlefieldManager.overridePriorityZones['2'].zone),
                        ticks = save.battlefieldManager.overridePriorityZones['2'].ticks
                    }
                end
            end
        end 
    end

    function PersistenceManager:restoreCsar()
        local save = self.data
        if save.csarTracker then
            for i,v in pairs(save.csarTracker) do
                self.csarTracker:restorePilot(v)
            end
        end
    end

    function PersistenceManager:restoreSquads()
        local save = self.data
        if save.squadTracker then
            for i,v in pairs(save.squadTracker) do
                local sdata = self.playerLogistics.registeredSquadGroups[v.type]
                if sdata then
                    v.data = sdata
                    self.squadTracker:restoreInfantry(v)
                end
            end
        end
    end

    function PersistenceManager:canRestore()
        return self.data ~= nil
    end

    function PersistenceManager:load()
        self.data = Utils.loadTable(self.path)
    end

    function PersistenceManager:save()
        local tosave = {}
        
        tosave.zones = {}
        for i,v in pairs(ZoneCommand.getAllZones()) do
        
            tosave.zones[i] = {
                name = v.name,
                side = v.side,
                resource = v.resource,
                mode = v.mode,
                distToFront = v.distToFront,
                closestEnemyDist = v.closestEnemyDist,
                extraBuildResources = v.extraBuildResources,
                revealTime = v.revealTime,
                built = {}
            }
            
            for n,b in pairs(v.built) do
                if b.type == 'defense' then
                    local typeList = {}
                    local gr = Group.getByName(b.name)
                    for _,unit in ipairs(gr:getUnits()) do
                        table.insert(typeList, unit:getDesc().typeName)
                    end

                    tosave.zones[i].built[n] = typeList
                else
                    tosave.zones[i].built[n] = true
                end
                
            end
            
            if v.currentBuild then
                tosave.zones[i].currentBuild = {
                    name = v.currentBuild.product.name, 
                    progress = v.currentBuild.progress,
                    side = v.currentBuild.side,
                    isRepair = v.currentBuild.isRepair
                }
            end

            if v.currentMissionBuild then
                tosave.zones[i].currentMissionBuild = {
                    name = v.currentMissionBuild.product.name, 
                    progress = v.currentMissionBuild.progress,
                    side = v.currentMissionBuild.side
                }
            end
        end

        tosave.activeGroups = {}
        for i,v in pairs(self.groupManager.groups) do
            tosave.activeGroups[i] = {
                productName = v.product.name,
                type = v.product.missionType
            }

            local gr = Group.getByName(v.product.name)
            if gr and gr:getSize()>0 then
                local un = gr:getUnit(1)
                if un then 
                    tosave.activeGroups[i].position = un:getPoint()
                    tosave.activeGroups[i].lastMission = v.product.lastMission
                    tosave.activeGroups[i].heading = math.atan2(un:getPosition().x.z, un:getPosition().x.x)
                end
            end

            if v.target then
                tosave.activeGroups[i].targetName = v.target.name
            end

            if v.home then
                tosave.activeGroups[i].homeName = v.home.name
            end

            if v.state then
                tosave.activeGroups[i].state = v.state
                tosave.activeGroups[i].lastStateDuration = timer.getAbsTime() - v.lastStateTime
            else
                tosave.activeGroups[i].state = 'uninitialized'
                tosave.activeGroups[i].lastStateDuration = 0
            end
        end

        tosave.battlefieldManager = {
            priorityZones = {},
            overridePriorityZones = {}
        }

        if BattlefieldManager.priorityZones[1] then
            tosave.battlefieldManager.priorityZones['1'] = BattlefieldManager.priorityZones[1].name
        end
        
        if BattlefieldManager.priorityZones[2] then
            tosave.battlefieldManager.priorityZones['2'] = BattlefieldManager.priorityZones[2].name
        end
        
        if BattlefieldManager.overridePriorityZones[1] then
            tosave.battlefieldManager.overridePriorityZones['1'] = { 
                zone = BattlefieldManager.overridePriorityZones[1].zone.name, 
                ticks = BattlefieldManager.overridePriorityZones[1].ticks
            }
        end

        if BattlefieldManager.overridePriorityZones[2] then
            tosave.battlefieldManager.overridePriorityZones['2'] = { 
                zone = BattlefieldManager.overridePriorityZones[2].zone.name, 
                ticks = BattlefieldManager.overridePriorityZones[2].ticks
            }
        end


        tosave.csarTracker = {}

        for i,v in pairs(self.csarTracker.activePilots) do
            if v.pilot:isExist() and v.pilot:getSize()>0 and v.remainingTime>60 then
                tosave.csarTracker[i] = {
                    name = v.name,
                    remainingTime = v.remainingTime,
                    pos = v.pilot:getUnit(1):getPoint()
                }
            end
        end

        tosave.squadTracker = {}

        for i,v in pairs(self.squadTracker.activeInfantrySquads) do
            tosave.squadTracker[i] = {
                state = v.state,
                remainingStateTime = v.remainingStateTime,
                position = v.position,
                name = v.name,
                type = v.data.type
            }
        end

        Utils.saveTable(self.path, tosave)
    end
end

-----------------[[ END OF PersistenceManager.lua ]]-----------------



-----------------[[ TemplateDB.lua ]]-----------------

TemplateDB = {}

do
    TemplateDB.type = {
        group = 'group',
        static = 'static',
    }

    TemplateDB.templates = {}
    function TemplateDB.getData(objtype)
        return TemplateDB.templates[objtype]
    end

    TemplateDB.templates["pilot-replacement"] = {
        units = { "Soldier M4 GRG" },
        skill = "Good",
        dataCategory= TemplateDB.type.group
    }

    TemplateDB.templates["capture-squad"] = {
        units = {
            "Soldier M4 GRG",
            "Soldier M4 GRG",
            "Soldier M249",
            "Soldier M4 GRG"
        },
        skill = "Good",
        dataCategory= TemplateDB.type.group
    }

    TemplateDB.templates["sabotage-squad"] = {
        units = {
            "Soldier M4 GRG",
            "Soldier M249",
            "Soldier M249",
            "Soldier M4 GRG"
        },
        skill = "Good",
        dataCategory= TemplateDB.type.group
    }

    TemplateDB.templates["ambush-squad"] = {
        units = {
            "Soldier RPG",
            "Soldier RPG",
            "Soldier M249",
            "Soldier M4 GRG",
            "Soldier M4 GRG"
        },
        skill = "Good",
        invisible = true,
        dataCategory= TemplateDB.type.group
    }

    TemplateDB.templates["manpads-squad"] = {
        units = {
            "Soldier M4 GRG",
            "Soldier M249",
            "Soldier stinger",
            "Soldier stinger",
            "Soldier M4 GRG"
        },
        skill = "Good",
        dataCategory= TemplateDB.type.group
    }

    TemplateDB.templates["engineer-squad"] = {
        units = {
            "Soldier M4 GRG",
            "Soldier M4 GRG"
        },
        skill = "Good",
        dataCategory= TemplateDB.type.group
    }
    
    TemplateDB.templates["spy-squad"] = {
        units = {
            "Infantry AK"
        },
        skill = "Good",
        invisible = true,
        dataCategory= TemplateDB.type.group
    }

    TemplateDB.templates["rapier-squad"] = {
        units = {
            "rapier_fsa_blindfire_radar",
            "rapier_fsa_optical_tracker_unit",
            "rapier_fsa_launcher",
            "rapier_fsa_launcher",
            "Soldier M4 GRG",
            "Soldier M4 GRG"
        },
        skill = "Excellent",
        dataCategory= TemplateDB.type.group
    }

    TemplateDB.templates["tent"] = { type="FARP Tent", category="Fortifications", shape="PalatkaB", dataCategory=TemplateDB.type.static }

    TemplateDB.templates["barracks"] = { type="house1arm", category="Fortifications", shape=nil, dataCategory=TemplateDB.type.static }

    TemplateDB.templates["outpost"] = { type="outpost", category="Fortifications", shape=nil, dataCategory=TemplateDB.type.static }

    TemplateDB.templates["ammo-cache"] = { type="FARP Ammo Dump Coating", category="Fortifications", shape="SetkaKP", dataCategory=TemplateDB.type.static }

    TemplateDB.templates["ammo-depot"] = { type=".Ammunition depot", category="Warehouses", shape="SkladC", dataCategory=TemplateDB.type.static }

    TemplateDB.templates["fuel-cache"] = { type="FARP Fuel Depot", category="Fortifications", shape="GSM Rus", dataCategory=TemplateDB.type.static }

    TemplateDB.templates["fuel-tank-small"] = { type="Fuel tank", category="Fortifications", shape="toplivo-bak", dataCategory=TemplateDB.type.static }

    TemplateDB.templates["fuel-tank-big"] = { type="Tank", category="Warehouses", shape="bak", dataCategory=TemplateDB.type.static }

    TemplateDB.templates["chem-tank"] = { type="Chemical tank A", category="Fortifications", shape="him_bak_a", dataCategory=TemplateDB.type.static }

    TemplateDB.templates["factory-1"] = { type="Tech combine", category="Fortifications", shape="kombinat", dataCategory=TemplateDB.type.static }

    TemplateDB.templates["factory-2"] = { type="Workshop A", category="Fortifications", shape="tec_a", dataCategory=TemplateDB.type.static }

    TemplateDB.templates["oil-pump"] = { type="Pump station", category="Fortifications", shape="nasos", dataCategory=TemplateDB.type.static }

    TemplateDB.templates["hangar"] = { type="Hangar A", category="Fortifications", shape="angar_a", dataCategory=TemplateDB.type.static }

    TemplateDB.templates["excavator"] = { type="345 Excavator", category="Fortifications", shape="cat_3451", dataCategory=TemplateDB.type.static }

    TemplateDB.templates["farm-house-1"] = { type="Farm A", category="Fortifications", shape="ferma_a", dataCategory=TemplateDB.type.static }

    TemplateDB.templates["farm-house-2"] = { type="Farm B", category="Fortifications", shape="ferma_b", dataCategory=TemplateDB.type.static }

    TemplateDB.templates["antenna"] = { type="Comms tower M", category="Fortifications", shape="tele_bash_m", dataCategory=TemplateDB.type.static }

    TemplateDB.templates["tv-tower"] = { type="TV tower", category="Fortifications", shape="tele_bash", dataCategory=TemplateDB.type.static }

    TemplateDB.templates["bunker-1"] = { type="Sandbox", category="Fortifications", dataCategory=TemplateDB.type.static }

    TemplateDB.templates["command-center"] = { type=".Command Center", category="Fortifications", shape="ComCenter", dataCategory=TemplateDB.type.static }
    
    TemplateDB.templates["military-staff"] = { type="Military staff", category="Fortifications", shape="aviashtab", dataCategory=TemplateDB.type.static }

    TemplateDB.templates["ship-tanker-seawisegiant"] = { type="Seawise_Giant", category="Ships", dataCategory=TemplateDB.type.static }

    TemplateDB.templates["ship-supply-tilde"] = { type="Ship_Tilde_Supply", category="Ships", dataCategory=TemplateDB.type.static }

    TemplateDB.templates["ship-landingship-samuelchase"] = { type="USS_Samuel_Chase", category="Ships", dataCategory=TemplateDB.type.static }

    TemplateDB.templates["ship-landingship-ropucha"] = { type="BDK-775", category="Ships", dataCategory=TemplateDB.type.static }

    TemplateDB.templates["ship-tanker-elnya"] = { type="ELNYA", category="Ships", dataCategory=TemplateDB.type.static }

    TemplateDB.templates["ship-landingship-lstmk2"] = { type="LST_Mk2", category="Ships", dataCategory=TemplateDB.type.static }

    TemplateDB.templates["ship-bulker-yakushev"] = { type="Dry-cargo ship-1", category="Ships", dataCategory=TemplateDB.type.static }

    TemplateDB.templates["ship-cargo-ivanov"] = { type="Dry-cargo ship-2", category="Ships", dataCategory=TemplateDB.type.static }


end

-----------------[[ END OF TemplateDB.lua ]]-----------------



-----------------[[ Spawner.lua ]]-----------------

Spawner = {}

do
    function Spawner.createPilot(name, pos)
        local groupData = Spawner.getData("pilot-replacement", name, pos, nil, 5, {
            [land.SurfaceType.LAND] = true, 
            [land.SurfaceType.ROAD] = true,
            [land.SurfaceType.RUNWAY] = true,
        })

        return coalition.addGroup(country.id.CJTF_BLUE, Group.Category.GROUND, groupData)
    end

    function Spawner.createObject(name, objType, pos, side, minDist, maxDist, surfaceTypes, zone)
        if zone then
            zone = CustomZone:getByName(zone) -- expand zone name to CustomZone object
        end

        local data = Spawner.getData(objType, name, pos, minDist, maxDist, surfaceTypes, zone)

        if not data then return end

        local cnt = country.id.CJTF_BLUE
        if side == 1 then
            cnt = country.id.CJTF_RED
        end

        if data.dataCategory == TemplateDB.type.static then
            return coalition.addStaticObject(cnt, data)
        elseif data.dataCategory == TemplateDB.type.group then
            return coalition.addGroup(cnt, Group.Category.GROUND, data)
        end
    end

    function Spawner.getUnit(unitType, name, pos, skill, minDist, maxDist, surfaceTypes, zone)
        local nudgedPos = nil
		for i=1,500,1 do
            nudgedPos = mist.getRandPointInCircle(pos, maxDist, minDist)
           
            if zone then
                if zone:isInside(nudgedPos) and surfaceTypes[land.getSurfaceType(nudgedPos)] then
                    break
                end
            else
                if surfaceTypes[land.getSurfaceType(nudgedPos)] then
                    break
                end
            end

            if i==500 then env.info('Spawner - ERROR: failed to find good location') end
		end

        return {
            ["type"] = unitType,
            ["skill"] = skill,
            ["coldAtStart"] = false,
            ["x"] = nudgedPos.x,
            ["y"] = nudgedPos.y,
            ["name"] = name,
            ['heading'] = math.random()*math.pi*2,
            ["playerCanDrive"] = false
        }
    end

    function Spawner.getData(objtype, name, pos, minDist, maxDist, surfaceTypes, zone)
        if not maxDist then maxDist = 150 end
        if not surfaceTypes then surfaceTypes = { [land.SurfaceType.LAND]=true } end

        local data = TemplateDB.getData(objtype)
        if not data then 
            env.info("Spawner - ERROR: cant find group data "..tostring(objtype).." for group name "..name)
            return
        end

        local spawnData = {}

        if data.dataCategory == TemplateDB.type.static then
            if not surfaceTypes[land.getSurfaceType(pos)] then
                for i=1,500,1 do
                    pos = mist.getRandPointInCircle(pos, maxDist)

                    if zone then
                        if zone:isInside(pos) and surfaceTypes[land.getSurfaceType(pos)] then
                            break
                        end
                    else
                        if surfaceTypes[land.getSurfaceType(pos)] then
                            break
                        end
                    end
                    
                    if i==500 then env.info('Spawner - ERROR: failed to find good location') end
                end
            end

            spawnData = {
                ["type"] = data.type,
                ["name"] = name,
                ["shape_name"] = data.shape,
                ["category"] = data.category,
                ["x"] = pos.x,
                ["y"] = pos.y,
                ['heading'] = math.random()*math.pi*2
            }
        elseif data.dataCategory== TemplateDB.type.group then
            spawnData = {
                ["units"] = {},
                ["name"] = name,
                ["task"] = "Ground Nothing",
                ["route"] = {
                    ["points"]={
                        {
                            ["x"] = pos.x,
                            ["y"] = pos.y,
                            ["action"] = "Off Road",
                            ["speed"] = 0,
                            ["type"] = "Turning Point",
                            ["ETA"] = 0,
                            ["formation_template"] = "",
                            ["task"] = Spawner.getDefaultTask(data.invisible)
                        }
                    }
                }
            }

            if data.minDist then
                minDist = data.minDist
            end

            if data.maxDist then
                maxDist = data.maxDist
            end
            
            for i,v in ipairs(data.units) do
                table.insert(spawnData.units, Spawner.getUnit(v, name.."-"..i, pos, data.skill, minDist, maxDist, surfaceTypes, zone))
            end
        end

        spawnData.dataCategory = data.dataCategory
            
        return spawnData
    end

    function Spawner.getDefaultTask(invisible)
        local defTask =  {
            ["id"] = "ComboTask",
            ["params"] = 
            {
                ["tasks"] = 
                {
                    [1] = 
                    {
                        ["enabled"] = true,
                        ["auto"] = false,
                        ["id"] = "WrappedAction",
                        ["number"] = 1,
                        ["params"] = 
                        {
                            ["action"] = 
                            {
                                ["id"] = "Option",
                                ["params"] = 
                                {
                                    ["name"] = 9,
                                    ["value"] = 2,
                                },
                            },
                        },
                    }, 
                    [2] = 
                    {
                        ["enabled"] = true,
                        ["auto"] = false,
                        ["id"] = "WrappedAction",
                        ["number"] = 2,
                        ["params"] = 
                        {
                            ["action"] = 
                            {
                                ["id"] = "Option",
                                ["params"] = 
                                {
                                    ["name"] = 0,
                                    ["value"] = 0,
                                }
                            }
                        }
                    }
                }
            }
        }

        if invisible then 
            table.insert(defTask.params.tasks, {
                ["number"] = 3,
                ["auto"] = false,
                ["id"] = "WrappedAction",
                ["enabled"] = true,
                ["params"] = 
                {
                    ["action"] = 
                    {
                        ["id"] = "SetInvisible",
                        ["params"] = 
                        {
                            ["value"] = true,
                        }
                    }
                }
            })
        end
        
        return defTask
    end
end

-----------------[[ END OF Spawner.lua ]]-----------------



-----------------[[ CommandFunctions.lua ]]-----------------

CommandFunctions = {}

do
    CommandFunctions.jtac = nil

    function CommandFunctions.spawnJtac(zone)
        if CommandFunctions.jtac then
            CommandFunctions.jtac:deployAtZone(zone)
            CommandFunctions.jtac:showMenu()
            CommandFunctions.jtac:setLifeTime(60)
        end
    end

    function CommandFunctions.smokeTargets(zone, count)
        local units = {}
        for i,v in pairs(zone.built) do
            local g = Group.getByName(v.name)
            if g then
                for i2,v2 in ipairs(g:getUnits()) do
                    table.insert(units, v2)
                end
            else
                local s = StaticObject.getByName(v.name)
                if s then
                    table.insert(units, s)
                end
            end
        end
        
        local tgts = {}
        for i=1,count,1 do
            if #units > 0 then
                local selected = math.random(1,#units)
                table.insert(tgts, units[selected])
                table.remove(units, selected)
            end
        end
        
        for i,v in ipairs(tgts) do
            local pos = v:getPoint()
            trigger.action.smoke(pos, 1)
        end
    end
end

-----------------[[ END OF CommandFunctions.lua ]]-----------------



-----------------[[ JTAC.lua ]]-----------------

JTAC = {}
do
	JTAC.categories = {}
	JTAC.categories['SAM'] = {'SAM SR', 'SAM TR', 'IR Guided SAM','SAM LL','SAM CC'}
	JTAC.categories['Infantry'] = {'Infantry'}
	JTAC.categories['Armor'] = {'Tanks','IFV','APC'}
	JTAC.categories['Support'] = {'Unarmed vehicles','Artillery'}
	JTAC.categories['Structures'] = {'StaticObjects'}
	
	--{name = 'groupname'}
	function JTAC:new(obj)
		obj = obj or {}
		obj.lasers = {tgt=nil, ir=nil}
		obj.target = nil
		obj.timerReference = nil
        obj.remainingLife = nil
		obj.tgtzone = nil
		obj.priority = nil
		obj.jtacMenu = nil
		obj.laserCode = 1688
		obj.side = Group.getByName(obj.name):getCoalition()
		setmetatable(obj, self)
		self.__index = self
		obj:initCodeListener()
		return obj
	end
	
	function JTAC:initCodeListener()
		local ev = {}
		ev.context = self
		function ev:onEvent(event)
			if event.id == 26 then
				if event.text:find('^jtac%-code:') then
					local s = event.text:gsub('^jtac%-code:', '')
					local code = tonumber(s)
					self.context:setCode(code)
                    trigger.action.removeMark(event.idx)
				end
			end
		end
		
		world.addEventHandler(ev)
	end

    function JTAC:setCode(code)
        if code>=1111 and code <= 1788 then
            self.laserCode = code
            trigger.action.outTextForCoalition(self.side, 'JTAC code set to '..code, 10)
        else
            trigger.action.outTextForCoalition(self.side, 'Invalid laser code. Must be between 1111 and 1788 ', 10)
        end
    end
	
	function JTAC:showMenu()
		local gr = Group.getByName(self.name)
		if not gr then
			return
		end
		
		if not self.jtacMenu then
			self.jtacMenu = missionCommands.addSubMenuForCoalition(self.side, 'JTAC')
			
			missionCommands.addCommandForCoalition(self.side, 'Target report', self.jtacMenu, function(dr)
				if Group.getByName(dr.name) then
					dr:printTarget(true)
				else
					missionCommands.removeItemForCoalition(dr.side, dr.jtacMenu)
					dr.jtacMenu = nil
				end
			end, self)
			
			missionCommands.addCommandForCoalition(self.side, 'Next Target', self.jtacMenu, function(dr)
				if Group.getByName(dr.name) then
					dr:searchTarget()
				else
					missionCommands.removeItemForCoalition(dr.side, dr.jtacMenu)
					dr.jtacMenu = nil
				end
			end, self)
			
			missionCommands.addCommandForCoalition(self.side, 'Deploy Smoke', self.jtacMenu, function(dr)
				if Group.getByName(dr.name) then
					local tgtunit = Unit.getByName(dr.target)
                    if not tgtunit then
                        tgtunit = StaticObject.getByName(dr.target)
                    end

					if tgtunit then
						trigger.action.smoke(tgtunit:getPoint(), 3)
						trigger.action.outTextForCoalition(dr.side, 'JTAC target marked with ORANGE smoke', 10)
					end
				else
					missionCommands.removeItemForCoalition(dr.side, dr.jtacMenu)
					dr.jtacMenu = nil
				end
			end, self)
			
			local priomenu = missionCommands.addSubMenuForCoalition(self.side, 'Set Priority', self.jtacMenu)
			for i,v in pairs(JTAC.categories) do
				missionCommands.addCommandForCoalition(self.side, i, priomenu, function(dr, cat)
					if Group.getByName(dr.name) then
						dr:setPriority(cat)
						dr:searchTarget()
					else
						missionCommands.removeItemForCoalition(dr.side, dr.jtacMenu)
						dr.jtacMenu = nil
					end
				end, self, i)
			end

            local dial = missionCommands.addSubMenuForCoalition(self.side, 'Set Laser Code', self.jtacMenu)
            for i2=1,7,1 do
                local digit2 = missionCommands.addSubMenuForCoalition(self.side, '1'..i2..'__', dial)
                for i3=1,9,1 do
                    local digit3 = missionCommands.addSubMenuForCoalition(self.side, '1'..i2..i3..'_', digit2)
                    for i4=1,9,1 do
                        local digit4 = missionCommands.addSubMenuForCoalition(self.side, '1'..i2..i3..i4, digit3)
                        local code = tonumber('1'..i2..i3..i4)
                        missionCommands.addCommandForCoalition(self.side, 'Accept', digit4, Utils.log(self.setCode), self, code)
                    end
                end
            end
			
			missionCommands.addCommandForCoalition(self.side, "Clear", priomenu, function(dr)
				if Group.getByName(dr.name) then
					dr:clearPriority()
					dr:searchTarget()
				else
					missionCommands.removeItemForCoalition(dr.side, dr.jtacMenu)
					dr.jtacMenu = nil
				end
			end, self)
		end
	end
	
	function JTAC:setPriority(prio)
		self.priority = JTAC.categories[prio]
		self.prioname = prio
	end
	
	function JTAC:clearPriority()
		self.priority = nil
	end
	
	function JTAC:setTarget(unit)
		
		if self.lasers.tgt then
			self.lasers.tgt:destroy()
			self.lasers.tgt = nil
		end
		
		if self.lasers.ir then
			self.lasers.ir:destroy()
			self.lasers.ir = nil
		end
		
		local me = Group.getByName(self.name)
		if not me then return end
		
		local pnt = unit:getPoint()
		self.lasers.tgt = Spot.createLaser(me:getUnit(1), { x = 0, y = 2.0, z = 0 }, pnt, self.laserCode)
		self.lasers.ir = Spot.createInfraRed(me:getUnit(1), { x = 0, y = 2.0, z = 0 }, pnt)
		
		self.target = unit:getName()
	end

    function JTAC:setLifeTime(minutes)
        self.remainingLife = minutes
        
        timer.scheduleFunction(function(param, time)
            if param.remainingLife == nil then return end

            local gr = Group.getByName(self.name)
		    if not gr then
                param.remainingLife = nil
                return 
            end

            param.remainingLife = param.remainingLife - 1
            if param.remainingLife < 0 then
                param:clearTarget()
                return
            end

            return time+60
        end, self, timer.getTime()+60)
    end
	
	function JTAC:printTarget(makeitlast)
		local toprint = ''
		if self.target and self.tgtzone then
			local tgtunit = Unit.getByName(self.target)
            local isStructure = false
            if not tgtunit then 
                tgtunit = StaticObject.getByName(self.target)
                isStructure = true
            end

			if tgtunit then
				local pnt = tgtunit:getPoint()
                local tgttype = "Unidentified"
                if isStructure then
                    tgttype = "Structure"
                else
                    tgttype = tgtunit:getTypeName()
                end
				
				if self.priority then
					toprint = 'Priority targets: '..self.prioname..'\n'
				end
				
				toprint = toprint..'Lasing '..tgttype..' at '..self.tgtzone.name..'\nCode: '..self.laserCode..'\n'
				local lat,lon,alt = coord.LOtoLL(pnt)
				local mgrs = coord.LLtoMGRS(coord.LOtoLL(pnt))
				toprint = toprint..'\nDDM:  '.. mist.tostringLL(lat,lon,3)
				toprint = toprint..'\nDMS:  '.. mist.tostringLL(lat,lon,2,true)
				toprint = toprint..'\nMGRS: '.. mist.tostringMGRS(mgrs, 5)
				toprint = toprint..'\n\nAlt: '..math.floor(alt)..'m'..' | '..math.floor(alt*3.280839895)..'ft'
			else
				makeitlast = false
				toprint = 'No Target'
			end
		else
			makeitlast = false
			toprint = 'No target'
		end
		
		local gr = Group.getByName(self.name)
		if makeitlast then
			trigger.action.outTextForCoalition(gr:getCoalition(), toprint, 60)
		else
			trigger.action.outTextForCoalition(gr:getCoalition(), toprint, 10)
		end
	end
	
	function JTAC:clearTarget()
		self.target = nil
	
		if self.lasers.tgt then
			self.lasers.tgt:destroy()
			self.lasers.tgt = nil
		end
		
		if self.lasers.ir then
			self.lasers.ir:destroy()
			self.lasers.ir = nil
		end
		
		if self.timerReference then
			mist.removeFunction(self.timerReference)
			self.timerReference = nil
		end
		
		local gr = Group.getByName(self.name)
		if gr then
			gr:destroy()
			missionCommands.removeItemForCoalition(self.side, self.jtacMenu)
			self.jtacMenu = nil
		end
	end
	
	function JTAC:searchTarget()
		local gr = Group.getByName(self.name)
		if gr then
			if self.tgtzone and self.tgtzone.side~=0 and self.tgtzone.side~=gr:getCoalition() then
				local viabletgts = {}
				for i,v in pairs(self.tgtzone.built) do
					local tgtgr = Group.getByName(v.name)
					if tgtgr and tgtgr:getSize()>0 then
						for i2,v2 in ipairs(tgtgr:getUnits()) do
							if v2:getLife()>=1 then
								table.insert(viabletgts, v2)
							end
						end
                    else
                        tgtgr = StaticObject.getByName(v.name)
                        if tgtgr then
                            table.insert(viabletgts, tgtgr)
                        end
                    end
				end
				
				if self.priority then
					local priorityTargets = {}
					for i,v in ipairs(viabletgts) do
						for i2,v2 in ipairs(self.priority) do
                            if v2 == "StaticObjects" and ZoneCommand.staticRegistry[v:getName()] then
                                table.insert(priorityTargets, v)
                                break
                            elseif v:hasAttribute(v2) and v:getLife()>=1 then
								table.insert(priorityTargets, v)
								break
							end
						end
					end
					
					if #priorityTargets>0 then
						viabletgts = priorityTargets
					else
						self:clearPriority()
						trigger.action.outTextForCoalition(gr:getCoalition(), 'JTAC: No priority targets found', 10)
					end
				end
				
				if #viabletgts>0 then
					local chosentgt = math.random(1, #viabletgts)
					self:setTarget(viabletgts[chosentgt])
					self:printTarget()
				else
					self:clearTarget()
				end
			else
				self:clearTarget()
			end
		end
	end
	
	function JTAC:searchIfNoTarget()
		if Group.getByName(self.name) then
			if not self.target or (not Unit.getByName(self.target) and not StaticObject.getByName(self.target)) then
				self:searchTarget()
			elseif self.target then
				local un = Unit.getByName(self.target)
				if un then
					if un:getLife()>=1 then
						self:setTarget(un)
					else
						self:searchTarget()
					end
				else
                    local st = StaticObject.getByName(self.target)
                    if st then
                        self:setTarget(st)
                    end
                end
			end
		else
			self:clearTarget()
		end
	end
	
	function JTAC:deployAtZone(zoneCom)
        self.remainingLife = nil
		self.tgtzone = zoneCom
		local p = CustomZone:getByName(self.tgtzone.name).point
		local vars = {}
		vars.gpName = self.name
		vars.action = 'respawn' 
		vars.point = {x=p.x, y=5000, z = p.z}
		mist.teleportToPoint(vars)
		
		mist.scheduleFunction(self.setOrbit, {self, self.tgtzone.zone, p}, timer.getTime()+1)
		
		if not self.timerReference then
			self.timerReference = mist.scheduleFunction(self.searchIfNoTarget, {self}, timer.getTime()+5, 5)
		end
	end
	
	function JTAC:setOrbit(zonename, point)
		local gr = Group.getByName(self.name)
		if not gr then 
			return
		end
		
		local cnt = gr:getController()
		cnt:setCommand({ 
			id = 'SetInvisible', 
			params = { 
				value = true 
			} 
		})
  
		cnt:setTask({ 
			id = 'Orbit', 
			params = { 
				pattern = 'Circle',
				point = {x = point.x, y=point.z},
				altitude = 5000
			} 
		})
		
		self:searchTarget()
	end
end

-----------------[[ END OF JTAC.lua ]]-----------------



-----------------[[ Objectives/Objective.lua ]]-----------------

Objective = {}

do
    Objective.types = {
        fly_to_zone_seq = 'fly_to_zone_seq',            -- any of playerlist inside [zone] in sequence
        recon_zone = 'recon_zone',                           -- within X km, facing Y angle +-, % of enemy units in LOS progress faster
        destroy_attr = 'destroy_attr',                  -- any of playerlist kill event on target with any of [attribute]
        destroy_attr_at_zone = 'destroy_attr_at_zone',  -- any of playerlist kill event on target at [zone] with any of [attribute]
        clear_attr_at_zone = 'clear_attr_at_zone',      -- [zone] does not have any units with [attribute]
        destroy_structure = 'destroy_structure',        -- [structure] is killed by any player (getDesc().displayName or getDesc().typeName:gsub('%.','') must match)
        destroy_group = 'destroy_group',                -- [group] is missing from mission AND any player killed unit from group at least once
        supply = 'supply',                              -- any of playerlist unload [amount] supply at [zone]
        extract_pilot = 'extract_pilot',                  -- players extracted specific ejected pilots
        extract_squad = 'extract_squad',                  -- players extracted specific squad
        unloaded_pilot_or_squad = 'unloaded_pilot_or_squad', -- unloaded pilot or squad
        deploy_squad = 'deploy_squad',                  --deploy squad at zone
        escort = 'escort',                              -- escort convoy
        protect = 'protect',                            -- protect other mission
        air_kill_bonus = 'air_kill_bonus',               -- award bonus for air kills
        bomb_in_zone = 'bomb_in_zone',                     -- bombs tallied inside zone
        player_close_to_zone = 'player_close_to_zone' -- player is close to point
    }

    function Objective:new(type)

		local obj = {
            type = type,
            mission = nil,
            param = {},
            isComplete = false,
            isFailed = false
        }

		setmetatable(obj, self)
		self.__index = self

		return obj
    end

    function Objective:initialize(mission, param)
        self.mission = mission
        self:validateParameters(param)
        self.param = param
    end

    function Objective:getType()
        return self.type
    end

    function Objective:validateParameters(param)
        for i,v in pairs(self.requiredParams) do
            if v and param[i] == nil then
                env.error("Objective - missing parameter: "..i..' in '..self:getType(), true)
            end
        end
    end

    -- virtual
    Objective.requiredParams = {}

    function Objective:getText()
        env.error("Objective - getText not implemented")
        return "NOT IMPLEMENTED"
    end

    function Objective:update()
        env.error("Objective - update not implemented")
    end

    function Objective:checkFail()
        env.error("Objective - checkFail not implemented")
    end
    --end virtual
end

-----------------[[ END OF Objectives/Objective.lua ]]-----------------



-----------------[[ Objectives/ObjAirKillBonus.lua ]]-----------------

ObjAirKillBonus = Objective:new(Objective.types.air_kill_bonus)
do
    ObjAirKillBonus.requiredParams = {
        ['attr'] = true,
        ['bonus'] = true,
        ['count'] = true,
        ['linkedObjectives'] = true
    }

    function ObjAirKillBonus:getText()
        local msg = 'Destroy: '
        for _,v in ipairs(self.param.attr) do
            msg = msg..v..', '
        end
        msg = msg:sub(1,#msg-2)
        msg = msg..'\n Kills increase mission reward (Ends when other objectives are completed)'
        msg = msg..'\n   Kills: '..self.param.count
        return msg
    end

    function ObjAirKillBonus:update()
        if not self.isComplete and not self.isFailed then
            local allcomplete = true
            for _,obj in pairs(self.param.linkedObjectives) do
                if obj.isFailed then self.isFailed = true end
                if not obj.isComplete then allcomplete = false end
            end

            self.isComplete = allcomplete
        end
    end

    function ObjAirKillBonus:checkFail()
        if not self.isComplete and not self.isFailed then
            local allcomplete = true
            for _,obj in pairs(self.param.linkedObjectives) do
                if obj.isFailed then self.isFailed = true end
                if not obj.isComplete then allcomplete = false end
            end

            self.isComplete = allcomplete
        end
    end
end

-----------------[[ END OF Objectives/ObjAirKillBonus.lua ]]-----------------



-----------------[[ Objectives/ObjBombInsideZone.lua ]]-----------------

ObjBombInsideZone = Objective:new(Objective.types.bomb_in_zone)
do
    ObjBombInsideZone.requiredParams = {
        ['targetZone'] = true,
        ['max'] = true,
        ['required'] = true,
        ['dropped'] = true,
        ['isFinishStarted'] = true,
        ['bonus'] = true
    }

    function ObjBombInsideZone:getText()
        local msg = 'Bomb runways at '..self.param.targetZone.name..'\n'

        local ratio = self.param.dropped/self.param.required
        local percent = string.format('%.1f',ratio*100)

        msg = msg..'\n  Runway bombed: '..percent..'%\n'

        msg = msg..'\n  Cluster bombs do not deal enough damage to complete this mission'

        return msg
    end

    function ObjBombInsideZone:update()
        if not self.isComplete and not self.isFailed then
            if self.param.targetZone.side ~= 1 then
                self.isFailed = true
                self.mission.failureReason = self.param.targetZone.name..' is no longer controlled by the enemy.'
            end

            if not self.param.isFinishStarted then
                if self.param.dropped >= self.param.required then
                    self.param.isFinishStarted = true
                    timer.scheduleFunction(function(o)
                        o.isComplete = true
                    end, self, timer.getTime()+5)
                end
            end
        end
    end

    function ObjBombInsideZone:checkFail()
        if not self.isComplete and not self.isFailed then
            if self.param.targetZone.side ~= 1 then
                self.isFailed = true
            end
        end
    end
end

-----------------[[ END OF Objectives/ObjBombInsideZone.lua ]]-----------------



-----------------[[ Objectives/ObjClearZoneOfUnitsWithAttribute.lua ]]-----------------

ObjClearZoneOfUnitsWithAttribute = Objective:new(Objective.types.clear_attr_at_zone)
do
    ObjClearZoneOfUnitsWithAttribute.requiredParams = {
        ['attr'] = true,
        ['tgtzone'] = true
    }

    function ObjClearZoneOfUnitsWithAttribute:getText()
        local msg = 'Clear '..self.param.tgtzone.name..' of: '
        for _,v in ipairs(self.param.attr) do
            msg = msg..v..', '
        end
        msg = msg:sub(1,#msg-2)
        msg = msg..'\n Progress: '..self.param.tgtzone:getUnitCountWithAttributeOnSide(self.param.attr, 1)..' left'
        return msg
    end

    function ObjClearZoneOfUnitsWithAttribute:update()
        if not self.isComplete and not self.isFailed then
            local zn = self.param.tgtzone
            if zn.side ~= 1 or not zn:hasUnitWithAttributeOnSide(self.param.attr, 1) then 
                self.isComplete = true
                return true
            end
        end
    end

    function ObjClearZoneOfUnitsWithAttribute:checkFail()
        -- can not fail
    end
end

-----------------[[ END OF Objectives/ObjClearZoneOfUnitsWithAttribute.lua ]]-----------------



-----------------[[ Objectives/ObjDestroyGroup.lua ]]-----------------

ObjDestroyGroup = Objective:new(Objective.types.destroy_group)
do
    ObjDestroyGroup.requiredParams = {
        ['target'] = true,
        ['targetUnitNames'] = true,
        ['lastUpdate'] = true
    }

    function ObjDestroyGroup:getText()
        local msg = 'Destroy '..self.param.target.product.display..' before it reaches its destination.\n'

        local gr = Group.getByName(self.param.target.name)
        if gr and gr:getSize()>0 then
            local killcount = 0
            for i,v in pairs(self.param.targetUnitNames) do
                if v == true then
                    killcount = killcount + 1
                end
            end

            msg = msg..'\n     '..gr:getSize()..' units remaining. (killed '..killcount..')\n'
            for name, unit in pairs(self.mission.players) do
                if unit and unit:isExist() then
                    local tgtUnit = gr:getUnit(1)
                    local dist = mist.utils.get2DDist(unit:getPoint(), tgtUnit:getPoint())
                    
                    local m = '\n     '..name..': Distance: '
                    m = m..string.format('%.2f',dist/1000)..'km'
                    m = m..' Bearing: '..math.floor(Utils.getBearing(unit:getPoint(), tgtUnit:getPoint()))
                    msg = msg..m
                end
            end
        end

        return msg
    end

    function ObjDestroyGroup:update()
        if not self.isComplete and not self.isFailed then
            local target = self.param.target
            local exists = false
            local gr = Group.getByName(target.name)

            if gr and gr:getSize() > 0 then
                local updateFrequency = 5 -- seconds
                local shouldUpdateMsg = (timer.getAbsTime() - self.param.lastUpdate) > updateFrequency

                if shouldUpdateMsg then
                    for _, unit in pairs(self.mission.players) do
                        if unit and unit:isExist() then
                            local tgtUnit = gr:getUnit(1)
                            local dist = mist.utils.get2DDist(unit:getPoint(), tgtUnit:getPoint())
                            local dstkm = string.format('%.2f',dist/1000)
                            local dstnm = string.format('%.2f',dist/1852)

                            local m = 'Distance: '
                            m = m..dstkm..'km | '..dstnm..'nm'

                            m = m..'\nBearing: '..math.floor(Utils.getBearing(unit:getPoint(), tgtUnit:getPoint()))
                            trigger.action.outTextForUnit(unit:getID(), m, updateFrequency)
                        end
                    end
                    
                    self.param.lastUpdate = timer.getAbsTime()
                end
            elseif target.state == 'enroute' then
                for i,v in pairs(self.param.targetUnitNames) do
                    if v == true then
                        self.isComplete = true
                        return true
                    end
                end

                self.isFailed = true
                self.mission.failureReason = 'Convoy was killed by someone else.'
                return true
            else
                self.isFailed = true
                self.mission.failureReason = 'Convoy has reached its destination.'
                return true
            end
        end
    end

    function ObjDestroyGroup:checkFail()
        if not self.isComplete and not self.isFailed then
            local target = self.param.target
            local gr = Group.getByName(target.name)

            if target.state ~= 'enroute' or not gr or gr:getSize() == 0 then
                self.isFailed = true
            end
        end
    end
end

-----------------[[ END OF Objectives/ObjDestroyGroup.lua ]]-----------------



-----------------[[ Objectives/ObjDestroyStructure.lua ]]-----------------

ObjDestroyStructure = Objective:new(Objective.types.destroy_structure)
do
    ObjDestroyStructure.requiredParams = {
        ['target']=true,
        ['tgtzone']=true,
        ['killed']=true
    }

    function ObjDestroyStructure:getText()
        local msg = 'Destroy '..self.param.target.display..' at '..self.param.tgtzone.name..'\n'
            
        local point = nil
        local st = StaticObject.getByName(self.param.target.name)
        if st then
            point = st:getPoint()
        else
            st = Group.getByName(self.param.target.name)
            if st and st:getSize()>0 then
                point = st:getUnit(1):getPoint()
            end
        end
        
        if point then
            local lat,lon,alt = coord.LOtoLL(point)
            local mgrs = coord.LLtoMGRS(coord.LOtoLL(point))
            msg = msg..'\n DDM:  '.. mist.tostringLL(lat,lon,3)
            msg = msg..'\n DMS:  '.. mist.tostringLL(lat,lon,2,true)
            msg = msg..'\n MGRS: '.. mist.tostringMGRS(mgrs, 5)
            msg = msg..'\n Altitude: '..math.floor(alt)..'m'..' | '..math.floor(alt*3.280839895)..'ft'
        end

        return msg
    end

    function ObjDestroyStructure:update()
        if not self.isComplete and not self.isFailed then
            if self.param.killed then
                self.isComplete = true
                return true
            end

            local target = self.param.target
            local exists = false
            local st = StaticObject.getByName(target.name)
            if st then
                exists = true
            else
                st = Group.getByName(target.name)
                if st and st:getSize()>0 then
                    exists = true
                end
            end

            if not exists then
                if not self.firstFailure then
                    self.firstFailure = timer.getAbsTime()
                end
            end

            if self.firstFailure and (timer.getAbsTime() - self.firstFailure > 1*60) then
                self.isFailed = true
                self.mission.failureReason = 'Structure was destoyed by someone else.'
                return true
            end
        end
    end

    function ObjDestroyStructure:checkFail()
        if not self.isComplete and not self.isFailed then
            local target = self.param.target
            local exists = false
            local st = StaticObject.getByName(target.name)
            if st then
                exists = true
            else
                st = Group.getByName(target.name)
                if st and st:getSize()>0 then
                    exists = true
                end
            end

            if not exists then 
                self.isFailed = true
            end
        end
    end
end

-----------------[[ END OF Objectives/ObjDestroyStructure.lua ]]-----------------



-----------------[[ Objectives/ObjDestroyUnitsWithAttribute.lua ]]-----------------

ObjDestroyUnitsWithAttribute = Objective:new(Objective.types.destroy_attr)
do
    ObjDestroyUnitsWithAttribute.requiredParams = {
        ['attr'] = true,
        ['amount'] = true,
        ['killed'] = true
    }

    function ObjDestroyUnitsWithAttribute:getText()
        local msg = 'Destroy: '
        for _,v in ipairs(self.param.attr) do
            msg = msg..v..', '
        end
        msg = msg:sub(1,#msg-2)
        msg = msg..'\n Progress: '..self.param.killed..'/'..self.param.amount
        return msg
    end

    function ObjDestroyUnitsWithAttribute:update()
        if not self.isComplete and not self.isFailed then
            if self.param.killed >= self.param.amount then
                self.isComplete = true
                return true
            end
        end
    end

    function ObjDestroyUnitsWithAttribute:checkFail()
        -- can not fail
    end
end

-----------------[[ END OF Objectives/ObjDestroyUnitsWithAttribute.lua ]]-----------------



-----------------[[ Objectives/ObjDestroyUnitsWithAttributeAtZone.lua ]]-----------------

ObjDestroyUnitsWithAttributeAtZone = Objective:new(Objective.types.destroy_attr_at_zone)
do
    ObjDestroyUnitsWithAttributeAtZone.requiredParams = {
        ['attr']=true,
        ['amount'] = true,
        ['killed'] = true,
        ['tgtzone'] = true
    }

    function ObjDestroyUnitsWithAttributeAtZone:getText()
        local msg = 'Destroy at '..self.param.tgtzone.name..': '
        for _,v in ipairs(self.param.attr) do
            msg = msg..v..', '
        end
        msg = msg:sub(1,#msg-2)
        msg = msg..'\n Progress: '..self.param.killed..'/'..self.param.amount
        return msg
    end

    function ObjDestroyUnitsWithAttributeAtZone:update()
        if not self.isComplete and not self.isFailed then
            if self.param.killed >= self.param.amount then
                self.isComplete = true
                return true
            end

            local zn = self.param.tgtzone
            if zn.side ~= 1 or not zn:hasUnitWithAttributeOnSide(self.param.attr, 1) then 
                if self.firstFailure == nil then
                    self.firstFailure = timer.getAbsTime()
                else
                    if timer.getAbsTime() - self.firstFailure > 5*60 then
                        self.isFailed = true
                        self.mission.failureReason = zn.name..' no longer has targets matching the description.'
                        return true
                    end
                end
            else
                if self.firstFailure ~= nil then
                    self.firstFailure = nil
                end
            end
        end
    end

    function ObjDestroyUnitsWithAttributeAtZone:checkFail()
        if not self.isComplete and not self.isFailed then
            local zn = self.param.tgtzone
            if zn.side ~= 1 or not zn:hasUnitWithAttributeOnSide(self.param.attr, 1) then 
                self.isFailed = true
            end
        end
    end
end

-----------------[[ END OF Objectives/ObjDestroyUnitsWithAttributeAtZone.lua ]]-----------------



-----------------[[ Objectives/ObjEscortGroup.lua ]]-----------------

ObjEscortGroup = Objective:new(Objective.types.escort)
do
    ObjEscortGroup.requiredParams = {
        ['maxAmount']=true,
        ['amount'] = true,
        ['proxDist']= true,
        ['target'] = true,
        ['lastUpdate']= true
    }

    function ObjEscortGroup:getText()
        local msg = 'Stay in close proximity of the convoy'

        local gr = Group.getByName(self.param.target.name)
        if gr and gr:getSize()>0 then
            local grunit = gr:getUnit(1)
            local lat,lon,alt = coord.LOtoLL(grunit:getPoint())
            local mgrs = coord.LLtoMGRS(coord.LOtoLL(grunit:getPoint()))
            msg = msg..'\n DDM:  '.. mist.tostringLL(lat,lon,3)
            msg = msg..'\n DMS:  '.. mist.tostringLL(lat,lon,2,true)
            msg = msg..'\n MGRS: '.. mist.tostringMGRS(mgrs, 5)
        end
        
        local prg = math.floor(((self.param.maxAmount - self.param.amount)/self.param.maxAmount)*100)
        msg = msg.. '\n Progress: '..prg..'%'
        return msg
    end

    function ObjEscortGroup:update()
        if not self.isComplete and not self.isFailed then
            local gr = Group.getByName(self.param.target.name)
            if not gr or gr:getSize()==0 then
                self.isFailed = true
                self.mission.failureReason = 'Group has been destroyed.'
                return true
            end
            local grunit = gr:getUnit(1)

            if self.param.target.state == 'atdestination' or self.param.target.state == 'siege' then
                for name, unit in pairs(self.mission.players) do
                    if unit and unit:isExist() then
                        local dist = mist.utils.get3DDist(unit:getPoint(), grunit:getPoint())
                        if dist < self.param.proxDist then
                            self.isComplete = true
                            break
                        end
                    end
                end

                if not self.isComplete then 
                    self.isFailed = true 
                    self.mission.failureReason = 'Group has reached its destination without an escort.'
                end
            end

            if not self.isComplete and not self.isFailed then
                local plycount = Utils.getTableSize(self.mission.players)
                if plycount == 0 then plycount = 1 end
                local updateFrequency = 5 -- seconds
                local shouldUpdateMsg = (timer.getAbsTime() - self.param.lastUpdate) > updateFrequency
                for name, unit in pairs(self.mission.players) do
                    if unit and unit:isExist() then
                        local dist = mist.utils.get3DDist(unit:getPoint(), grunit:getPoint())
                        if dist < self.param.proxDist then
                            self.param.amount = self.param.amount - (1/plycount)

                            if shouldUpdateMsg then
                                local prg = string.format('%.1f',((self.param.maxAmount - self.param.amount)/self.param.maxAmount)*100)
                                trigger.action.outTextForUnit(unit:getID(), 'Progress: '..prg..'%', updateFrequency)
                            end
                        else
                            if shouldUpdateMsg then
                                local m = 'Distance: '
                                if dist>1000 then
                                    local dstkm = string.format('%.2f',dist/1000)
                                    local dstnm = string.format('%.2f',dist/1852)

                                    m = m..dstkm..'km | '..dstnm..'nm'
                                else
                                    local dstft = math.floor(dist/0.3048)
                                    m = m..math.floor(dist)..'m | '..dstft..'ft'
                                end

                                m = m..'\nBearing: '..math.floor(Utils.getBearing(unit:getPoint(), grunit:getPoint()))
                                trigger.action.outTextForUnit(unit:getID(), m, updateFrequency)
                            end
                        end
                    end
                end

                if shouldUpdateMsg then
                    self.param.lastUpdate = timer.getAbsTime()
                end
            end

            if self.param.amount <= 0 then
                self.isComplete = true
                return true
            end
        end
    end

    function ObjEscortGroup:checkFail()
        if not self.isComplete and not self.isFailed then
            local tg = self.param.target
            local gr = Group.getByName(tg.name)
            if not gr or gr:getSize() == 0 then
                self.isFailed = true
            end

            if self.mission.state == Mission.states.new then
                if tg.state == 'enroute' and (timer.getAbsTime() - tg.lastStateTime) >= 7*60 then
                    self.isFailed = true
                end
            end
        end
    end
end

-----------------[[ END OF Objectives/ObjEscortGroup.lua ]]-----------------



-----------------[[ Objectives/ObjFlyToZoneSequence.lua ]]-----------------

ObjFlyToZoneSequence = Objective:new(Objective.types.fly_to_zone_seq)
do
    ObjFlyToZoneSequence.requiredParams = {
        ['waypoints'] = true,
        ['failZones'] = true
    }

    function ObjFlyToZoneSequence:getText()
        local msg = 'Fly route: '
            
        for i,v in ipairs(self.param.waypoints) do
            if v.complete then
                msg = msg..'\n [✓] '..i..'. '..v.zone.name
            else
                msg = msg..'\n --> '..i..'. '..v.zone.name
            end
        end
        return msg
    end

    function ObjFlyToZoneSequence:update()
        if not self.isComplete and not self.isFailed then
            if self.param.failZones[1] then
                for _,zn in ipairs(self.param.failZones[1]) do
                    if zn.side ~= 1 then 
                        self.isFailed = true
                        self.mission.failureReason = zn.name..' is no longer controlled by the enemy.'
                        break
                    end
                end
            end

            if self.param.failZones[2] then
                for _,zn in ipairs(self.param.failZones[2]) do
                    if zn.side ~= 2 then 
                        self.isFailed = true
                        self.mission.failureReason = zn.name..' was lost.'
                        break
                    end
                end
            end

            if not self.isFailed then
                local firstWP = nil
                local nextWP = nil
                for i,leg in ipairs(self.param.waypoints) do
                    if not leg.complete then
                        firstWP = leg
                        nextWP = self.param.waypoints[i+1]
                        break
                    end
                end

                if firstWP then
                    local point = firstWP.zone.zone.point
                    local range = 3000 --meters
                    local allInside = true
                    for p,u in pairs(self.mission.players) do
                        if u and u:isExist() then
                            if Utils.isLanded(u,true) then
                                allInside = false
                                break
                            end
                            
                            local pos = u:getPoint()
                            local dist = mist.utils.get2DDist(point, pos)
                            if dist > range then
                                allInside = false
                                break
                            end
                        end
                    end

                    if allInside then
                        firstWP.complete = true
                        self.mission:pushMessageToPlayers(firstWP.zone.name..' reached')
                        if nextWP then
                            self.mission:pushMessageToPlayers('Next point: '..nextWP.zone.name)
                        end
                    end
                else
                    self.isComplete = true
                    return true
                end
            end
        end
    end

    function ObjFlyToZoneSequence:checkFail()
        if not self.isComplete and not self.isFailed then
            if self.param.failZones[1] then
                for _,zn in ipairs(self.param.failZones[1]) do
                    if zn.side ~= 1 then 
                        self.isFailed = true
                        break
                    end
                end
            end

            if self.param.failZones[2] then
                for _,zn in ipairs(self.param.failZones[2]) do
                    if zn.side ~= 2 then 
                        self.isFailed = true
                        break
                    end
                end
            end
        end
    end
end

-----------------[[ END OF Objectives/ObjFlyToZoneSequence.lua ]]-----------------



-----------------[[ Objectives/ObjProtectMission.lua ]]-----------------

ObjProtectMission = Objective:new(Objective.types.protect)
do
    ObjProtectMission.requiredParams = {
        ['mis'] = true
    }

    function ObjProtectMission:getText()
        local msg = 'Prevent enemy aircraft from interfering with '..self.param.mis:getMissionName()..' mission.'

        if self.param.mis.info and self.param.mis.info.targetzone then
            msg = msg..'\n Target zone: '..self.param.mis.info.targetzone.name
        end

        msg = msg..'\n Protect players: '
        for i,v in pairs(self.param.mis.players) do
            msg = msg..'\n  '..i
        end
        
        msg = msg..'\n Mission success depends on '..self.param.mis:getMissionName()..' mission success.'
        return msg
    end

    function ObjProtectMission:update()
        if not self.isComplete and not self.isFailed then
            if self.param.mis.state == Mission.states.failed then 
                self.isFailed = true
                self.mission.failureReason = "Failed to protect players of "..self.param.mis.name.." mission."
            end

            if self.param.mis.state == Mission.states.completed then 
                self.isComplete = true
            end
        end
    end

    function ObjProtectMission:checkFail()
        if not self.isComplete and not self.isFailed then
            if self.param.mis.state == Mission.states.failed then 
                self.isFailed = true
            end

            if self.param.mis.state == Mission.states.completed then 
                if self.state == Mission.states.new or 
                    self.state == Mission.states.preping or 
                    self.state == Mission.states.comencing then
                        
                    self.isFailed = true
                end
            end
        end
    end
end

-----------------[[ END OF Objectives/ObjProtectMission.lua ]]-----------------



-----------------[[ Objectives/ObjReconZone.lua ]]-----------------

ObjReconZone = Objective:new(Objective.types.recon_zone)
do
    ObjReconZone.requiredParams = { 
        ['target'] = true,
        ['maxAmount'] = true,
        ['amount'] = true,
        ['allowedDeviation'] = true,
        ['proxDist'] = true,
        ['lastUpdate'] = true,
        ['failZones'] = true
    }

    function ObjReconZone:getText()
        local msg = 'Stay within range of '..self.param.target.name..' and observe the enemy.'

        local prg = math.floor(((self.param.maxAmount - self.param.amount)/self.param.maxAmount)*100)
        msg = msg.. '\n Progress: '..prg..'%'
        return msg
    end

    function ObjReconZone:update()
        if not self.isComplete and not self.isFailed then
            if self.param.failZones[1] then
                for _,zn in ipairs(self.param.failZones[1]) do
                    if zn.side ~= 1 then 
                        self.isFailed = true
                        self.mission.failureReason = zn.name..' is no longer controlled by the enemy.'
                        break
                    end
                end
            end

            if self.param.failZones[2] then
                for _,zn in ipairs(self.param.failZones[2]) do
                    if zn.side ~= 2 then 
                        self.isFailed = true
                        self.mission.failureReason = zn.name..' was lost.'
                        break
                    end
                end
            end

            if not self.isFailed then
                local plycount = Utils.getTableSize(self.mission.players)
                if plycount == 0 then plycount = 1 end
                local updateFrequency = 5 -- seconds
                local shouldUpdateMsg = (timer.getAbsTime() - self.param.lastUpdate) > updateFrequency

                for name, unit in pairs(self.mission.players) do
                    if unit and unit:isExist() then
                        local dist = mist.utils.get2DDist(unit:getPoint(), self.param.target.zone.point)
                        if dist < self.param.proxDist then
                            local unitPos = unit:getPosition()
                            local unitheading = math.deg(math.atan2(unitPos.x.z, unitPos.x.x))
                            local bearing = Utils.getBearing(unit:getPoint(), self.param.target.zone.point)

                            local diff = Utils.getHeadingDiff(unitheading, bearing)

                            if math.abs(diff) <= self.param.allowedDeviation then
                                local unitsCount = 0
                                local visibleCount = 0
                                for _,product in pairs(self.param.target.built) do
                                    if product.side ~= unit:getCoalition() then
                                        local gr = Group.getByName(product.name)
                                        if gr then
                                            for _,enemyUnit in ipairs(gr:getUnits()) do
                                                unitsCount = unitsCount+1
                                                local from = unit:getPoint()
                                                from.y = from.y+1.5
                                                local to = enemyUnit:getPoint()
                                                to.y = to.y+1.5
                                                if land.isVisible(from, to) then
                                                    visibleCount = visibleCount+1
                                                end
                                            end 
                                        else
                                            local st = StaticObject.getByName(product.name)
                                            if st then
                                                unitsCount = unitsCount+1
                                                local from = unit:getPoint()
                                                from.y = from.y+1.5
                                                local to = st:getPoint()
                                                to.y = to.y+1.5
                                                if land.isVisible(from, to) then
                                                    visibleCount = visibleCount+1
                                                end
                                            end
                                        end
                                    end
                                end
                                
                                local percentVisible = 0
                                if unitsCount > 0 and visibleCount > 0 then
                                    percentVisible = visibleCount/unitsCount
                                    if percentVisible > 0.5 then
                                        self.param.amount = self.param.amount - percentVisible
                                    else

                                    end
                                    env.info('Scout_Helo - player can see '..string.format('%.2f',percentVisible)..'%')
                                end
                                
                                
                                if shouldUpdateMsg then
                                    if visibleCount == 0 then
                                        local prg = string.format('%.1f',((self.param.maxAmount - self.param.amount)/self.param.maxAmount)*100)
                                        trigger.action.outTextForUnit(unit:getID(), 'No enemy visible.\nProgress: '..prg..'%', updateFrequency)
                                    else
                                        local percent = string.format('%.1f',percentVisible*100)

                                        local prg = string.format('%.1f',((self.param.maxAmount - self.param.amount)/self.param.maxAmount)*100)
                                        trigger.action.outTextForUnit(unit:getID(), percent..'% of enemies visible.\nProgress: '..prg..'%', updateFrequency)
                                    end
                                end
                            else
                                if shouldUpdateMsg then
                                    local m = 'Within range\nTurn heading: '..math.floor(Utils.getBearing(unit:getPoint(), self.param.target.zone.point))
                                    trigger.action.outTextForUnit(unit:getID(), m, updateFrequency)
                                end
                            end
                        else
                            if shouldUpdateMsg then
                                local dstkm = string.format('%.2f',dist/1000)
                                local dstnm = string.format('%.2f',dist/1852)

                                local m = 'Distance: '
                                m = m..dstkm..'km | '..dstnm..'nm'

                                m = m..'\nBearing: '..math.floor(Utils.getBearing(unit:getPoint(), self.param.target.zone.point))
                                trigger.action.outTextForUnit(unit:getID(), m, updateFrequency)
                            end
                        end
                    end
                end

                if shouldUpdateMsg then
                    self.param.lastUpdate = timer.getAbsTime()
                end

                if self.param.amount <= 0 then
                    self.isComplete = true
                    return true
                end
            end
        end
    end

    function ObjReconZone:checkFail()
        if not self.isComplete and not self.isFailed then
            if self.param.failZones[1] then
                for _,zn in ipairs(self.param.failZones[1]) do
                    if zn.side ~= 1 then 
                        self.isFailed = true
                        break
                    end
                end
            end

            if self.param.failZones[2] then
                for _,zn in ipairs(self.param.failZones[2]) do
                    if zn.side ~= 2 then 
                        self.isFailed = true
                        break
                    end
                end
            end
        end
    end
end

-----------------[[ END OF Objectives/ObjReconZone.lua ]]-----------------



-----------------[[ Objectives/ObjSupplyZone.lua ]]-----------------

ObjSupplyZone = Objective:new(Objective.types.supply)
do
    ObjSupplyZone.requiredParams = {
        ['amount']=true,
        ['delivered']=true,
        ['tgtzone']=true
    }

    function ObjSupplyZone:getText()
        local msg = 'Deliver '..self.param.amount..' to '..self.param.tgtzone.name..': '
        msg = msg..'\n Progress: '..self.param.delivered..'/'..self.param.amount
        return msg
    end

    function ObjSupplyZone:update()
        if not self.isComplete and not self.isFailed then
            if self.param.delivered >= self.param.amount then
                self.isComplete = true
                return true
            end

            local zn = self.param.tgtzone
            if zn.side ~= 2 then 
                self.isFailed = true
                self.mission.failureReason = zn.name..' was lost.'
                return true
            end
        end
    end

    function ObjSupplyZone:checkFail()
        if not self.isComplete and not self.isFailed then
            local zn = self.param.tgtzone
            if zn.side ~= 2 then 
                self.isFailed = true
                return true
            end
        end
    end
end

-----------------[[ END OF Objectives/ObjSupplyZone.lua ]]-----------------



-----------------[[ Objectives/ObjExtractSquad.lua ]]-----------------

ObjExtractSquad = Objective:new(Objective.types.extract_squad)
do
    ObjExtractSquad.requiredParams = {
        ['target']=true,
        ['loadedBy']=false,
        ['lastUpdate']= true
    }

    function ObjExtractSquad:getText()
        local infName = PlayerLogistics.getInfantryName(self.param.target.data.type)
        local msg = 'Extract '..infName..' '..self.param.target.name..'\n'
        
        if not self.param.loadedBy then
            local gr = Group.getByName(self.param.target.name)
            if gr and gr:getSize()>0 then
                local point = gr:getUnit(1):getPoint()

                local lat,lon,alt = coord.LOtoLL(point)
                local mgrs = coord.LLtoMGRS(coord.LOtoLL(point))
                msg = msg..'\n DDM:  '.. mist.tostringLL(lat,lon,3)
                msg = msg..'\n DMS:  '.. mist.tostringLL(lat,lon,2,true)
                msg = msg..'\n MGRS: '.. mist.tostringMGRS(mgrs, 5)
                msg = msg..'\n Altitude: '..math.floor(alt)..'m'..' | '..math.floor(alt*3.280839895)..'ft'
            end
        end

        return msg
    end

    function ObjExtractSquad:update()
        if not self.isComplete and not self.isFailed then

            if self.param.loadedBy then
                self.isComplete = true
                return true
            else
                local target = self.param.target
                
                local gr = Group.getByName(target.name)
                if not gr or gr:getSize()==0 then
                    self.isFailed = true
                    self.mission.failureReason = 'Squad was not rescued in time, and went MIA.'
                    return true
                end
            end

            local updateFrequency = 5 -- seconds
            local shouldUpdateMsg = (timer.getAbsTime() - self.param.lastUpdate) > updateFrequency
            if shouldUpdateMsg then
                for name, unit in pairs(self.mission.players) do
                    if unit and unit:isExist() then
                        local gr = Group.getByName(self.param.target.name)
                        local un = gr:getUnit(1)
                        local dist = mist.utils.get3DDist(unit:getPoint(), un:getPoint())
                        local m = 'Distance: '
                        if dist>1000 then
                            local dstkm = string.format('%.2f',dist/1000)
                            local dstnm = string.format('%.2f',dist/1852)

                            m = m..dstkm..'km | '..dstnm..'nm'
                        else
                            local dstft = math.floor(dist/0.3048)
                            m = m..math.floor(dist)..'m | '..dstft..'ft'
                        end

                        m = m..'\nBearing: '..math.floor(Utils.getBearing(unit:getPoint(), un:getPoint()))           
                        trigger.action.outTextForUnit(unit:getID(), m, updateFrequency)
                    end
                end

                self.param.lastUpdate = timer.getAbsTime()
            end
        end
    end

    function ObjExtractSquad:checkFail()
        if not self.isComplete and not self.isFailed then
            local target = self.param.target
                
            local gr = Group.getByName(target.name)
            if not gr or not gr:isExist() or gr:getSize()==0 then
                self.isFailed = true
                return true
            end
        end
    end
end

-----------------[[ END OF Objectives/ObjExtractSquad.lua ]]-----------------



-----------------[[ Objectives/ObjExtractPilot.lua ]]-----------------

ObjExtractPilot = Objective:new(Objective.types.extract_pilot)
do
    ObjExtractPilot.requiredParams = {
        ['target']=true,
        ['loadedBy']=false,
        ['lastUpdate']= true
    }

    function ObjExtractPilot:getText()
        local msg = 'Rescue '..self.param.target.name..'\n'
        
        if not self.param.loadedBy then
            
            if self.param.target.pilot:isExist() then
                local point = self.param.target.pilot:getUnit(1):getPoint()

                local lat,lon,alt = coord.LOtoLL(point)
                local mgrs = coord.LLtoMGRS(coord.LOtoLL(point))
                msg = msg..'\n DDM:  '.. mist.tostringLL(lat,lon,3)
                msg = msg..'\n DMS:  '.. mist.tostringLL(lat,lon,2,true)
                msg = msg..'\n MGRS: '.. mist.tostringMGRS(mgrs, 5)
                msg = msg..'\n Altitude: '..math.floor(alt)..'m'..' | '..math.floor(alt*3.280839895)..'ft'
            end
        end

        return msg
    end

    function ObjExtractPilot:update()
        if not self.isComplete and not self.isFailed then

            if self.param.loadedBy then
                self.isComplete = true
                return true
            else
                if not self.param.target.pilot:isExist() or self.param.target.remainingTime <= 0 then
                    self.isFailed = true
                    self.mission.failureReason = 'Pilot was not rescued in time, and went MIA.'
                    return true
                end
            end

            local updateFrequency = 5 -- seconds
            local shouldUpdateMsg = (timer.getAbsTime() - self.param.lastUpdate) > updateFrequency
            if shouldUpdateMsg then
                for name, unit in pairs(self.mission.players) do
                    if unit and unit:isExist() then
                        local gr = Group.getByName(self.param.target.name)
                        if gr and gr:getSize() > 0 then
                            local un = gr:getUnit(1)
                            if un then
                                local dist = mist.utils.get3DDist(unit:getPoint(), un:getPoint())
                                local m = 'Distance: '
                                if dist>1000 then
                                    local dstkm = string.format('%.2f',dist/1000)
                                    local dstnm = string.format('%.2f',dist/1852)

                                    m = m..dstkm..'km | '..dstnm..'nm'
                                else
                                    local dstft = math.floor(dist/0.3048)
                                    m = m..math.floor(dist)..'m | '..dstft..'ft'
                                end

                                m = m..'\nBearing: '..math.floor(Utils.getBearing(unit:getPoint(), un:getPoint()))
                                trigger.action.outTextForUnit(unit:getID(), m, updateFrequency)
                            end
                        end
                    end
                end

                self.param.lastUpdate = timer.getAbsTime()
            end
        end
    end

    function ObjExtractPilot:checkFail()
        if not self.isComplete and not self.isFailed then
            if not self.param.target.pilot:isExist() or self.param.target.remainingTime <= 0 then
                self.isFailed = true
                return true
            end
        end
    end
end

-----------------[[ END OF Objectives/ObjExtractPilot.lua ]]-----------------



-----------------[[ Objectives/ObjUnloadExtractedPilotOrSquad.lua ]]-----------------

ObjUnloadExtractedPilotOrSquad = Objective:new(Objective.types.unloaded_pilot_or_squad)
do
    ObjUnloadExtractedPilotOrSquad.requiredParams = {
        ['targetZone']=false,
        ['extractObjective']=true,
        ['unloadedAt']=false
    }

    function ObjUnloadExtractedPilotOrSquad:getText()
        local msg = 'Drop off personnel '
        if self.param.targetZone then
            msg = msg..'at '..self.param.targetZone.name..'\n'
        else
            msg = msg..'at a friendly zone\n'
        end

        return msg
    end

    function ObjUnloadExtractedPilotOrSquad:update()
        if not self.isComplete and not self.isFailed then

            if self.param.extractObjective.isComplete and self.param.unloadedAt then
                if self.param.targetZone then
                    if self.param.unloadedAt == self.param.targetZone.name then
                        self.isComplete = true
                        return true
                    else
                        self.isFailed = true
                        self.mission.failureReason = 'Personnel dropped off at wrong zone.'
                        return true
                    end
                else
                    self.isComplete = true
                    return true
                end
            end

            if self.param.extractObjective.isFailed then
                self.isFailed = true
                return true
            end

            if self.param.targetZone and self.param.targetZone.side ~= 2 then
                self.isFailed = true
                self.mission.failureReason = self.param.targetZone.name..' was lost.'
                return true
            end
        end
    end

    function ObjUnloadExtractedPilotOrSquad:checkFail()
        if not self.isComplete and not self.isFailed then

            if self.param.extractObjective.isFailed then
                self.isFailed = true
                return true
            end

            if self.param.targetZone and self.param.targetZone.side ~= 2 then
                self.isFailed = true
                return true
            end
        end
    end
end

-----------------[[ END OF Objectives/ObjUnloadExtractedPilotOrSquad.lua ]]-----------------



-----------------[[ Objectives/ObjPlayerCloseToZone.lua ]]-----------------

ObjPlayerCloseToZone = Objective:new(Objective.types.player_close_to_zone)
do
    ObjPlayerCloseToZone.requiredParams = {
        ['target']=true,
        ['range'] = true,
        ['amount']= true,
        ['maxAmount'] = true,
        ['lastUpdate']= true
    }

    function ObjPlayerCloseToZone:getText()
        local msg = 'Patrol area around '..self.param.target.name

        local prg = math.floor(((self.param.maxAmount - self.param.amount)/self.param.maxAmount)*100)
        msg = msg.. '\n Progress: '..prg..'%'
        return msg
    end

    function ObjPlayerCloseToZone:update()
        if not self.isComplete and not self.isFailed then

            if self.param.target.side ~= 2 then
                self.isFailed = true
                self.mission.failureReason = self.param.target.name..' was lost.'
                return true
            end

            local plycount = Utils.getTableSize(self.mission.players)
            if plycount == 0 then plycount = 1 end
            local updateFrequency = 5 -- seconds
            local shouldUpdateMsg = (timer.getAbsTime() - self.param.lastUpdate) > updateFrequency
            for name, unit in pairs(self.mission.players) do
                if unit and unit:isExist() and Utils.isInAir(unit) then
                    local dist = mist.utils.get2DDist(unit:getPoint(), self.param.target.zone.point)
                    if dist < self.param.range then
                        self.param.amount = self.param.amount - (1/plycount)

                        if shouldUpdateMsg then
                            local prg = string.format('%.1f',((self.param.maxAmount - self.param.amount)/self.param.maxAmount)*100)
                            trigger.action.outTextForUnit(unit:getID(), '['..self.param.target.name..'] Progress: '..prg..'%', updateFrequency)
                        end
                    end
                end
            end

            if shouldUpdateMsg then
                self.param.lastUpdate = timer.getAbsTime()
            end

            if self.param.amount <= 0 then
                self.isComplete = true
                for name, unit in pairs(self.mission.players) do
                    if unit and unit:isExist() and Utils.isInAir(unit) then
                        trigger.action.outTextForUnit(unit:getID(), '['..self.param.target.name..'] Complete', updateFrequency)
                    end
                end
                return true
            end
        end
    end

    function ObjPlayerCloseToZone:checkFail()
        if not self.isComplete and not self.isFailed then
            if self.param.target.side ~= 2 then
                self.isFailed = true
            end
        end
    end
end

-----------------[[ END OF Objectives/ObjPlayerCloseToZone.lua ]]-----------------



-----------------[[ Objectives/ObjDeploySquad.lua ]]-----------------

ObjDeploySquad = Objective:new(Objective.types.deploy_squad)
do
    ObjDeploySquad.requiredParams = {
        ['squadType']=true,
        ['targetZone']=true,
        ['requiredZoneSide']=true,
        ['unloadedType']=false,
        ['unloadedAt']=false
    }

    function ObjDeploySquad:getText()
        local infName = PlayerLogistics.getInfantryName(self.param.squadType)
        local msg = 'Deploy '..infName..' at '..self.param.targetZone.name
        return msg
    end

    function ObjDeploySquad:update()
        if not self.isComplete and not self.isFailed then

            if self.param.unloadedType and self.param.unloadedAt then
                if self.param.targetZone.name == self.param.unloadedAt then
                    if self.param.squadType == self.param.unloadedType then
                        self.isComplete = true
                        return true
                    end
                end
            end

            if self.param.targetZone.side ~= self.param.requiredZoneSide then
                self.isFailed = true

                local side = ''
                if self.param.requiredZoneSide == 0 then side = 'neutral' 
                elseif self.param.requiredZoneSide == 1 then side = 'controlled by Red'
                elseif self.param.requiredZoneSide == 2 then side = 'controlled by Blue'
                end

                self.mission.failureReason = self.param.targetZone.name..' is no longer '..side
                return true
            end
        end
    end

    function ObjDeploySquad:checkFail()
        if not self.isComplete and not self.isFailed then
            if self.param.targetZone.side ~= self.param.requiredZoneSide then
                self.isFailed = true
                return true
            end
        end
    end
end

-----------------[[ END OF Objectives/ObjDeploySquad.lua ]]-----------------



-----------------[[ Missions/Mission.lua ]]-----------------

Mission = {}
do
    Mission.states = {
        new = 'new',                -- mission was just generated and is listed publicly
        preping = 'preping',        -- mission was accepted by a player, was delisted, and player recieved a join code that can be shared
        comencing = 'comencing',    -- a player that is subscribed to the mission has taken off, join code is invalidated
        active = 'active',          -- all players subscribed to the mission have taken off, objective can now be accomplished
        completed = 'completed',    -- mission objective was completed, players need to land to claim rewards
        failed = 'failed'           -- mission lost all players OR mission objective no longer possible to accomplish
    }

    --[[
        new -> preping -> comencing -> active -> completed
         |      |         |           |-> failed
         |      |         |->failed
         |      |->failed
         |->failed
    --]]

    Mission.types = {
        cap_easy = 'cap_easy',          -- fly over zn A-B-A-B-A-B OR destroy few enemy aircraft 
        cap_medium = 'cap_medium',      -- fly over zn A-B-A-B-A-B AND destroy few enemy aircraft -- push list of aircraft within range of target zones
        tarcap = 'tarcap',              -- protect other mission, air kills increase reward
        --tarcap = 'tarcap',            -- update target mission list after all other missions are in

        cas_easy = 'cas_easy',          -- destroy small amount of ground units
        cas_medium = 'cas_medium',      -- destroy large amount of ground units
        cas_hard = 'cas_hard',          -- destroy all defenses at zone A
        bai = 'bai',                    -- destroy any enemy convoy - show "last" location of convoi (BRA or LatLon) update every 30 seconds
        
        sead = 'sead',                  -- destroy any SAM TR or SAM SR at zone A
        dead = 'dead',                  -- destroy all SAM TR or SAM SR, or IR Guided SAM at zone A
        
        strike_veryeasy = 'strike_veryeasy',   -- destroy 1 building
        strike_easy = 'strike_easy',    -- destroy any structure at zone A
        strike_medium = 'strike_medium',-- destroy specific structure at zone A - show LatLon and Alt in mission description
        strike_hard = 'strike_hard',    -- destroy all structures at zone A and turn it neutral
        deep_strike = 'deep_strike',   -- destroy specific structure taken from strike queue - show LatLon and Alt in mission description

        recon_plane ='recon_plane',   -- overly target zone and survive
        recon_plane_deep = 'recon_plane_deep', -- overfly zone where distance from front == 2, add target to a strike queue, stays there until building exists, or 1hr passes
        anti_runway = 'anti_runway',  -- drop at least X anti runway bombs on runway zone (if player unit launches correct weapon, track, if agl>10m check if in zone, tally), define list of runway zones somewhere
        
        supply_easy = 'supply_easy',   -- transfer resources to zone A(low supply)
        supply_hard = 'supply_hard',   -- transfer resources to zone A(low supply), high resource number
        escort = 'escort',              -- follow and protect friendly convoy until they get to target OR 10 minutes pass
        csar = 'csar',              -- extract specific pilot to friendly zone, track friendly pilots ejected
        scout_helo = 'scout_helo',       -- within X km, facing Y angle +-, % of enemy units in LOS progress faster
        extraction = 'extraction',  -- extract a deployed squad to friendly zone, generate mission if squad has extractionReady state
        deploy_squad = 'deploy_squad',  -- deploy squad to zone
    }

    Mission.completion_type = {
        any = 'any',
        all = 'all'
    }

    function Mission:new(id, type)
        local expire = math.random(60*15, 60*30)

		local obj = {
            missionID = id,
            type = type,
            name = '',
            description = '',
            failureReason = nil,
            state = Mission.states.new,
            expireTime = expire,
            lastStateTime = timer.getAbsTime(),
            objectives = {},
            completionType = Mission.completion_type.any,
            rewards = {},
            players = {},
            info = {}
        }

		setmetatable(obj, self)
		self.__index = self
		
        if obj.getExpireTime then obj.expireTime = obj:getExpireTime() end
        if obj.getMissionName then obj.name = obj:getMissionName() end
        if obj.generateObjectives then obj:generateObjectives() end
        if obj.generateRewards then obj:generateRewards() end

		return obj
	end

    function Mission:updateState(newstate)
        env.info('Mission - code'..self.missionID..' updateState state changed from '..self.state..' to '..newstate)
        self.state = newstate
        self.lastStateTime = timer.getAbsTime()
        if self.state == self.states.preping then
            if self.info.targetzone then
                MissionTargetRegistry.addZone(self.info.targetzone.name)
            end
        elseif self.state == self.states.completed or self.state == self.states.failed then
            if self.info.targetzone then
                MissionTargetRegistry.removeZone(self.info.targetzone.name)
            end
        end
    end

    function Mission:pushMessageToPlayers(msg, duration)
        if not duration then
            duration = 10
        end

        for _,un in pairs(self.players) do
            if un and un:isExist() then
                trigger.action.outTextForUnit(un:getID(), msg, duration)
            end
        end
    end

    function Mission:pushSoundToPlayers(sound)
        for _,un in pairs(self.players) do
            if un and un:isExist() then
                --trigger.action.outSoundForUnit(un:getID(), sound) -- does not work correctly in multiplayer
                trigger.action.outSoundForGroup(un:getGroup():getID(), sound)
            end
        end
    end

    function Mission:removePlayer(player)
        for pl,un in pairs(self.players) do
            if pl == player then
                self.players[pl] = nil
                break
            end
        end
    end

    function Mission:isInstantReward()
        return false
    end

    function Mission:hasPlayers()
        return Utils.getTableSize(self.players) > 0
    end

    function Mission:getPlayerUnit(player)
        return self.players[player]
    end

    function Mission:addPlayer(player, unit)
        self.players[player] = unit
    end

    function Mission:checkFailConditions()
        if self.state == Mission.states.active then return end

        for _,obj in ipairs(self.objectives) do
            local shouldBreak = obj:checkFail()
            
            if shouldBreak then break end
        end
    end

    function Mission:updateObjectives()
        if self.state ~= self.states.active then return end

        for _,obj in ipairs(self.objectives) do
            local shouldBreak = obj:update()

            if obj.isFailed and self.objectiveFailedCallback then self:objectiveFailedCallback(obj) end
            if not obj.isFailed and obj.isComplete and self.objectiveCompletedCallback then self:objectiveCompletedCallback(obj) end

            if shouldBreak then break end
        end
    end

    function Mission:updateIsFailed()
        self:checkFailConditions()

        local allFailed = true
        for _,obj in ipairs(self.objectives) do
            if self.state == Mission.states.new then
                if obj.isFailed then
                    self:updateState(Mission.states.failed)
                    env.info("Mission code"..self.missionID.." objective cancelled:\n"..obj:getText())
                    break
                end
            end

            if self.completionType == Mission.completion_type.all then
                if obj.isFailed then
                    self:updateState(Mission.states.failed)
                    env.info("Mission code"..self.missionID.." (all) objective failed:\n"..obj:getText())
                    break
                end
            end

            if not obj.isFailed then
                allFailed = false
            end
        end

        if self.completionType == Mission.completion_type.any and allFailed then
            self:updateState(Mission.states.failed)
            env.info("Mission code"..self.missionID.." all objectives failed")
        end
    end

    function Mission:updateIsCompleted()
        if self.completionType == self.completion_type.any then
            for _,obj in ipairs(self.objectives) do
                if obj.isComplete then 
                    self:updateState(self.states.completed)
                    env.info("Mission code"..self.missionID.." (any) objective completed:\n"..obj:getText())
                    break
                end
            end
        elseif self.completionType == self.completion_type.all then
            local allComplete = true
            for _,obj in ipairs(self.objectives) do
                if not obj.isComplete then
                    allComplete = false
                    break
                end
            end

            if allComplete then
                self:updateState(self.states.completed)
                env.info("Mission code"..self.missionID.." all objectives complete")
            end
        end
    end

    function Mission:tallyWeapon(weapon)
        for _,obj in ipairs(self.objectives) do
            if not obj.isComplete and not obj.isFailed then
                if obj.type == ObjBombInsideZone:getType() then
                    for i,v in ipairs(obj.param.targetZone:getRunwayZones()) do
                        if Utils.isInZone(weapon, v.name) then
                            if obj.param.dropped < obj.param.max then
                                obj.param.dropped = obj.param.dropped + 1
                                if obj.param.dropped > obj.param.required then
                                    for _,rew in ipairs(self.rewards) do
                                        if obj.param.bonus[rew.type] then
                                            rew.amount = rew.amount +  obj.param.bonus[rew.type]

                                            if rew.type == PlayerTracker.statTypes.xp then
                                                self:pushMessageToPlayers("Bonus: + "..obj.param.bonus[rew.type]..' XP')
                                            end
                                        end
                                    end
                                end
                            end
                            break
                        end
                    end
                end
            end
        end
    end

    function Mission:tallyKill(kill)
        for _,obj in ipairs(self.objectives) do
            if not obj.isComplete and not obj.isFailed then
                if obj.type == ObjDestroyUnitsWithAttribute:getType() then
                    for _,a in ipairs(obj.param.attr) do
                        if kill:hasAttribute(a) then
                            obj.param.killed = obj.param.killed + 1
                            break
                        elseif a == 'Buildings' and ZoneCommand and ZoneCommand.staticRegistry[kill:getName()] then
                            obj.param.killed = obj.param.killed + 1
                            break
                        end
                    end
                elseif obj.type == ObjDestroyStructure:getType() then
                    if obj.param.target.name == kill:getName() then
                        obj.param.killed = true
                    end
                elseif obj.type == ObjDestroyGroup:getType() then
                    if kill.getName then
                        if obj.param.targetUnitNames[kill:getName()] ~= nil then
                            obj.param.targetUnitNames[kill:getName()] = true
                        end
                    end
                elseif obj.type == ObjAirKillBonus:getType() then
                    for _,a in ipairs(obj.param.attr) do
                        if kill:hasAttribute(a) then
                            for _,rew in ipairs(self.rewards) do
                                if obj.param.bonus[rew.type] then
                                    rew.amount = rew.amount +  obj.param.bonus[rew.type]
                                    obj.param.count = obj.param.count + 1
                                    if rew.type == PlayerTracker.statTypes.xp then
                                        self:pushMessageToPlayers("Reward increased: + "..obj.param.bonus[rew.type]..' XP')
                                    end
                                end
                            end
                            break
                        elseif a == 'Buildings' and ZoneCommand and ZoneCommand.staticRegistry[kill:getName()] then
                            for _,rew in ipairs(self.rewards) do
                                if obj.param.bonus[rew.type] then
                                    rew.amount = rew.amount +  obj.param.bonus[rew.type]
                                    obj.param.count = obj.param.count + 1
                                    
                                    if rew.type == PlayerTracker.statTypes.xp then
                                        self:pushMessageToPlayers("Reward increased: + "..obj.param.bonus[rew.type]..' XP')
                                    end
                                end
                            end
                            break
                        end
                    end
                elseif obj.type == ObjDestroyUnitsWithAttributeAtZone:getType() then
                    local zn = obj.param.tgtzone
                    if zn then
                        local validzone = false
                        if Utils.isInZone(kill, zn.name) then
                            validzone = true
                        else
                            for nm,_ in pairs(zn.built) do
                                local gr = Group.getByName(nm)
                                if gr then
                                    for _,un in ipairs(gr:getUnits()) do
                                        if un:getID() == kill:getID() then
                                            validzone = true
                                            break
                                        end
                                    end
                                end

                                if validzone then break end
                            end
                        end
                        
                        if validzone then
                            for _,a in ipairs(obj.param.attr) do
                                if kill:hasAttribute(a) then
                                    obj.param.killed = obj.param.killed + 1
                                    break
                                elseif a == 'Buildings' and ZoneCommand and ZoneCommand.staticRegistry[kill:getName()] then
                                    obj.param.killed = obj.param.killed + 1
                                    break
                                end
                            end
                        end
                    end
                end
            end
        end
    end

    function Mission:isUnitTypeAllowed(unit)
        return true
    end

    function Mission:tallySupplies(amount, zonename)
        for _,obj in ipairs(self.objectives) do
            if not obj.isComplete and not obj.isFailed then
                if obj.type == ObjSupplyZone:getType() then
                    if obj.param.tgtzone.name == zonename then
                        obj.param.delivered = obj.param.delivered + amount
                    end
                end
            end
        end
    end

    function Mission:tallyLoadPilot(player, pilot)
        for _,obj in ipairs(self.objectives) do
            if not obj.isComplete and not obj.isFailed then
                if obj.type == ObjExtractPilot:getType() then
                    if obj.param.target.name == pilot.name then
                        obj.param.loadedBy = player
                    end
                end
            end
        end
    end

    function Mission:tallyUnloadPilot(player, zonename)
        for _,obj in ipairs(self.objectives) do
            if not obj.isComplete and not obj.isFailed then
                if obj.type == ObjUnloadExtractedPilotOrSquad:getType() then
                    if obj.param.extractObjective.param.loadedBy == player then
                        obj.param.unloadedAt = zonename
                    end
                end
            end
        end
    end

    function Mission:tallyLoadSquad(player, squad)
        for _,obj in ipairs(self.objectives) do
            if not obj.isComplete and not obj.isFailed then
                if obj.type == ObjExtractSquad:getType() then
                    if obj.param.target.name == squad.name then
                        obj.param.loadedBy = player
                    end
                end
            end
        end
    end

    function Mission:tallyUnloadSquad(player, zonename, unloadedType)
        for _,obj in ipairs(self.objectives) do
            if not obj.isComplete and not obj.isFailed then
                if obj.type == ObjUnloadExtractedPilotOrSquad:getType() then
                    if obj.param.extractObjective.param.loadedBy == player and unloadedType == PlayerLogistics.infantryTypes.extractable then
                        obj.param.unloadedAt = zonename
                    end
                elseif obj.type == ObjDeploySquad:getType() then
                    obj.param.unloadedType = unloadedType
                    obj.param.unloadedAt = zonename
                end
            end
        end
    end

    function Mission:getBriefDescription()
        local msg = '~~~~~'..self.name..' ['..self.missionID..']~~~~~\n'..self.description..'\n'

        msg = msg..' Reward:'

        for _,r in ipairs(self.rewards) do
            msg = msg..' ['..r.type..': '..r.amount..']'
        end

        return msg
    end

    function Mission:generateRewards()
        if not self.type then return end
        
        local rewardDef = RewardDefinitions.missions[self.type]
        
        self.rewards = {}
        table.insert(self.rewards, {
            type = PlayerTracker.statTypes.xp,
            amount = math.random(rewardDef.xp.low,rewardDef.xp.high)*50
        })
    end

    function Mission:getDetailedDescription()
        local msg = '['..self.name..']'

        if self.state == Mission.states.comencing or self.state == Mission.states.preping then
            msg = msg..'\nJoin code ['..self.missionID..']'
        end

        msg = msg..'\nReward:'

        for _,r in ipairs(self.rewards) do
            msg = msg..' ['..r.type..': '..r.amount..']'
        end
        msg = msg..'\n'

        if #self.objectives>1 then
            msg = msg..'\nObjectives: '
            if self.completionType == Mission.completion_type.all then
                msg = msg..'(Complete ALL)\n'
            elseif self.completionType == Mission.completion_type.any then
                msg = msg..'(Complete ONE)\n'
            end
        elseif #self.objectives==1 then
            msg = msg..'\nObjective: \n'
        end

        for i,v in ipairs(self.objectives) do
            local obj = v:getText()
            if v.isComplete then 
                obj = '[✓]'..obj
            elseif v.isFailed then
                obj = '[X]'..obj
            else
                obj = '[ ]'..obj 
            end

            msg = msg..'\n'..obj..'\n'
        end

        msg = msg..'\nPlayers:'
        for i,_ in pairs(self.players) do
            msg = msg..'\n  '..i
        end

        return msg
    end
end

-----------------[[ END OF Missions/Mission.lua ]]-----------------



-----------------[[ Missions/CAP_Easy.lua ]]-----------------

CAP_Easy = Mission:new()
do
    function CAP_Easy.canCreate()
        local zoneNum = 0
        for _,zone in pairs(ZoneCommand.getAllZones()) do
            if zone.side == 2 and zone.distToFront == 0 then 
                zoneNum = zoneNum + 1
            end

            if zoneNum >= 2 then return true end
        end
    end

    function CAP_Easy:getMissionName()
        return 'CAP'
    end

    function CAP_Easy:isUnitTypeAllowed(unit)
        return unit:hasAttribute('Planes')
    end

    function CAP_Easy:generateObjectives()
        self.completionType = Mission.completion_type.any
        local description = ''
        local viableZones = {}
        for _,zone in pairs(ZoneCommand.getAllZones()) do
            if zone.side == 2 and zone.distToFront == 0 then
                table.insert(viableZones, zone)
            end
        end
        
        if #viableZones >= 2 then
            local choice1 = math.random(1,#viableZones)
            local zn1 = viableZones[choice1]

            local patrol1 = ObjPlayerCloseToZone:new()
            patrol1:initialize(self, {
                target = zn1,
                range = 20000,
                amount = 15*60,
                maxAmount = 15*60,
                lastUpdate = 0
            })

            table.insert(self.objectives, patrol1)
            description = description..'   Patrol airspace near '..zn1.name..'\n   OR\n'
        end

        local kills = ObjDestroyUnitsWithAttribute:new()
        kills:initialize(self, {
            attr = {'Planes', 'Helicopters'},
            amount = math.random(2,4),
            killed = 0 
        })

        table.insert(self.objectives, kills)
        description = description..'   Kill '..kills.param.amount..' aircraft'
        self.description = self.description..description
    end
end

-----------------[[ END OF Missions/CAP_Easy.lua ]]-----------------



-----------------[[ Missions/CAP_Medium.lua ]]-----------------

CAP_Medium = Mission:new()
do
    function CAP_Medium.canCreate()
        local zoneNum = 0
        for _,zone in pairs(ZoneCommand.getAllZones()) do
            if zone.side == 2 and zone.distToFront == 0 then 
                zoneNum = zoneNum + 1
            end

            if zoneNum >= 2 then return true end
        end
    end

    function CAP_Medium:getMissionName()
        return 'CAP'
    end

    function CAP_Medium:isUnitTypeAllowed(unit)
        return unit:hasAttribute('Planes')
    end

    function CAP_Medium:generateObjectives()
        self.completionType = Mission.completion_type.all
        local description = ''
        local viableZones = {}
        for _,zone in pairs(ZoneCommand.getAllZones()) do
            if zone.side == 2 and zone.distToFront == 0 then
                table.insert(viableZones, zone)
            end
        end
        
        if #viableZones >= 2 then
            local choice1 = math.random(1,#viableZones)
            local zn1 = viableZones[choice1]
            table.remove(viableZones,choice1)
            local choice2 = math.random(1,#viableZones)
            local zn2 = viableZones[choice2]

            local patrol1 = ObjPlayerCloseToZone:new()
            patrol1:initialize(self, {
                target = zn1,
                range = 20000,
                amount = 10*60,
                maxAmount = 10*60,
                lastUpdate = 0
            })

            table.insert(self.objectives, patrol1)

            local patrol2 = ObjPlayerCloseToZone:new()
            patrol2:initialize(self, {
                target = zn2,
                range = 20000,
                amount = 10*60,
                maxAmount = 10*60,
                lastUpdate = 0
            })

            table.insert(self.objectives, patrol2)
            description = description..'   Patrol airspace near '..zn1.name..' and '..zn2.name..'\n'

            local rewardDef = RewardDefinitions.missions[self.type]

            local kills = ObjAirKillBonus:new()
            kills:initialize(self, {
                attr = {'Planes', 'Helicopters'},
                bonus = {
                    [PlayerTracker.statTypes.xp] = rewardDef.xp.boost
                },
                count = 0,
                linkedObjectives = {patrol1, patrol2}
            })

            table.insert(self.objectives, kills)
            description = description..'   Aircraft kills increase reward'
        end

        self.description = self.description..description
    end
end

-----------------[[ END OF Missions/CAP_Medium.lua ]]-----------------



-----------------[[ Missions/CAS_Easy.lua ]]-----------------

CAS_Easy = Mission:new()
do
    function CAS_Easy.canCreate()
        return true
    end

    function CAS_Easy:getMissionName()
        return 'CAS'
    end

    function CAS_Easy:generateObjectives()
        self.completionType = Mission.completion_type.all
        local description = ''
        
        local kills = ObjDestroyUnitsWithAttribute:new()
        kills:initialize(self, {
            attr = {'Ground Units'},
            amount = math.random(3,6),
            killed = 0 
        })

        table.insert(self.objectives, kills)
        description = description..'   Destroy '..kills.param.amount..' Ground Units'
        self.description = self.description..description
    end
end

-----------------[[ END OF Missions/CAS_Easy.lua ]]-----------------



-----------------[[ Missions/CAS_Medium.lua ]]-----------------

CAS_Medium = Mission:new()
do
    function CAS_Medium.canCreate()
        return true
    end

    function CAS_Medium:getMissionName()
        return 'CAS'
    end

    function CAS_Medium:generateObjectives()
        self.completionType = Mission.completion_type.all
        local description = ''
        
        local kills = ObjDestroyUnitsWithAttribute:new()
        kills:initialize(self, {
            attr = {'Ground Units'},
            amount = math.random(8,12),
            killed = 0
        })

        table.insert(self.objectives, kills)
        description = description..'   Destroy '..kills.param.amount..' Ground Units'
        self.description = self.description..description
    end
end

-----------------[[ END OF Missions/CAS_Medium.lua ]]-----------------



-----------------[[ Missions/CAS_Hard.lua ]]-----------------

CAS_Hard = Mission:new()
do
    function CAS_Hard.canCreate()
        for _,zone in pairs(ZoneCommand.getAllZones()) do
            if zone.side == 1 and zone.distToFront and zone.distToFront <=1 and zone:hasUnitWithAttributeOnSide({"Ground Units"}, 1, 6) then
                if not MissionTargetRegistry.isZoneTargeted(zone.name) then
                    return true
                end
            end
        end
    end

    function CAS_Hard:getMissionName()
        return 'CAS'
    end

    function CAS_Hard:generateObjectives()
        self.completionType = Mission.completion_type.all
        local description = ''
        local viableZones = {}
        for _,zone in pairs(ZoneCommand.getAllZones()) do
            if zone.side == 1 and zone.distToFront == 0 and zone:hasUnitWithAttributeOnSide({"Ground Units"}, 1, 6) then
                if not MissionTargetRegistry.isZoneTargeted(zone.name) then
                    table.insert(viableZones, zone)
                end
            end
        end

        if #viableZones == 0 then
            for _,zone in pairs(ZoneCommand.getAllZones()) do
                if zone.side == 1 and zone.distToFront == 1 and zone:hasUnitWithAttributeOnSide({"Ground Units"}, 1, 6) then
                    if not MissionTargetRegistry.isZoneTargeted(zone.name) then
                        table.insert(viableZones, zone)
                    end
                end
            end
        end
        
        if #viableZones > 0 then
            local choice = math.random(1,#viableZones)
            local zn = viableZones[choice]
            
            local kill = ObjDestroyUnitsWithAttributeAtZone:new()
            kill:initialize(self, {
                attr = {"Ground Units"},
                amount = 1,
                killed = 0,
                tgtzone = zn
            })
            table.insert(self.objectives, kill)

            local clear = ObjClearZoneOfUnitsWithAttribute:new()
            clear:initialize(self, {
                attr = {"Ground Units"},
                tgtzone = zn
            })
            table.insert(self.objectives, clear)

            description = description..'   Clear '..zn.name..' of ground units'
            self.info = {
                targetzone = zn
            }
        end
        self.description = self.description..description
    end
end

-----------------[[ END OF Missions/CAS_Hard.lua ]]-----------------



-----------------[[ Missions/SEAD.lua ]]-----------------

SEAD = Mission:new()
do
    function SEAD.canCreate()
        for _,zone in pairs(ZoneCommand.getAllZones()) do
            if zone.side == 1 and zone.distToFront and zone.distToFront <=1 and zone:hasSAMRadarOnSide(1) then
                if not MissionTargetRegistry.isZoneTargeted(zone.name) then
                    return true
                end
            end
        end
    end

    function SEAD:getMissionName()
        return 'SEAD'
    end

    function SEAD:generateObjectives()
        self.completionType = Mission.completion_type.all
        local description = ''
        local viableZones = {}
        for _,zone in pairs(ZoneCommand.getAllZones()) do
            if zone.side == 1 and zone.distToFront == 0 and zone:hasSAMRadarOnSide(1) then
                if not MissionTargetRegistry.isZoneTargeted(zone.name) then
                    table.insert(viableZones, zone)
                end
            end
        end

        if #viableZones == 0 then
            for _,zone in pairs(ZoneCommand.getAllZones()) do
                if zone.side == 1 and zone.distToFront == 1 and zone:hasSAMRadarOnSide(1) then
                    if not MissionTargetRegistry.isZoneTargeted(zone.name) then
                        table.insert(viableZones, zone)
                    end
                end
            end
        end
        
        if #viableZones > 0 then
            local choice = math.random(1,#viableZones)
            local zn = viableZones[choice]
            
            local kill = ObjDestroyUnitsWithAttributeAtZone:new()
            kill:initialize(self, {
                attr = {'SAM SR','SAM TR'},
                amount = 1,
                killed = 0,
                tgtzone = zn
            })

            table.insert(self.objectives, kill)
            description = description..'   Destroy '..kill.param.amount..' Search Radar or Track Radar at '..zn.name
            self.info = {
                targetzone = zn
            }
        end
        self.description = self.description..description
    end
end

-----------------[[ END OF Missions/SEAD.lua ]]-----------------



-----------------[[ Missions/DEAD.lua ]]-----------------

DEAD = Mission:new()
do
    function DEAD.canCreate()
        for _,zone in pairs(ZoneCommand.getAllZones()) do
            if zone.side == 1 and zone.distToFront and zone.distToFront <=1 and zone:hasUnitWithAttributeOnSide({"Air Defence"}, 1, 4) then
                if not MissionTargetRegistry.isZoneTargeted(zone.name) then
                    return true
                end
            end
        end
    end

    function DEAD:getMissionName()
        return 'DEAD'
    end

    function DEAD:generateObjectives()
        self.completionType = Mission.completion_type.all
        local description = ''
        local viableZones = {}
        for _,zone in pairs(ZoneCommand.getAllZones()) do
            if zone.side == 1 and zone.distToFront <=1 and zone:hasUnitWithAttributeOnSide({"Air Defence"}, 1, 4) then
                if not MissionTargetRegistry.isZoneTargeted(zone.name) then
                    table.insert(viableZones, zone)
                end
            end
        end
        
        if #viableZones > 0 then
            local choice = math.random(1,#viableZones)
            local zn = viableZones[choice]
            
            local kill = ObjDestroyUnitsWithAttributeAtZone:new()
            kill:initialize(self, {
                attr = {"Air Defence"},
                amount = 1,
                killed = 0,
                tgtzone = zn
            })
            table.insert(self.objectives, kill)

            local clear = ObjClearZoneOfUnitsWithAttribute:new()
            clear:initialize(self, {
                attr = {"Air Defence"},
                tgtzone = zn
            })
            table.insert(self.objectives, clear)

            description = description..'   Clear '..zn.name..' of any Air Defenses'
            self.info = {
                targetzone = zn
            }
        end
        self.description = self.description..description
    end
end

-----------------[[ END OF Missions/DEAD.lua ]]-----------------



-----------------[[ Missions/Supply_Easy.lua ]]-----------------

Supply_Easy = Mission:new()
do
    function Supply_Easy.canCreate()
        for _,zone in pairs(ZoneCommand.getAllZones()) do
            if zone.side == 2 and zone.distToFront and zone.distToFront <=1 and zone:criticalOnSupplies() then
                return true
            end
        end
    end

    function Supply_Easy:getMissionName()
        return "Supply delivery"
    end

    function Supply_Easy:isInstantReward()
        return true
    end

    function Supply_Easy:isUnitTypeAllowed(unit)
        if PlayerLogistics then
            local unitType = unit:getDesc()['typeName']
            return PlayerLogistics.allowedTypes[unitType] and PlayerLogistics.allowedTypes[unitType].supplies
        end
    end

    function Supply_Easy:generateObjectives()
        self.completionType = Mission.completion_type.all
        local description = ''

        local viableZones = {}
        for _,zone in pairs(ZoneCommand.getAllZones()) do
            if zone.side == 2 and zone.distToFront <=1 and zone:criticalOnSupplies() then
                table.insert(viableZones, zone)
            end
        end
        
        if #viableZones > 0 then
            local choice = math.random(1,#viableZones)
            local zn = viableZones[choice]
            
            local deliver = ObjSupplyZone:new()
            deliver:initialize(self, {
                amount = math.random(2,6)*250,
                delivered = 0,
                tgtzone = zn
            })
            
            table.insert(self.objectives, deliver)
            description = description..'   Deliver '..deliver.param.amount..' of supplies to '..zn.name
            self.info = {
                targetzone = zn
            }
        end

        self.description = self.description..description
    end
end

-----------------[[ END OF Missions/Supply_Easy.lua ]]-----------------



-----------------[[ Missions/Supply_Hard.lua ]]-----------------

Supply_Hard = Mission:new()
do
    function Supply_Hard.canCreate()
        for _,zone in pairs(ZoneCommand.getAllZones()) do
            if zone.side == 2 and zone.distToFront and zone.distToFront <=1 and zone:criticalOnSupplies() then
                return true
            end
        end
    end

    function Supply_Hard:getMissionName()
        return "Supply delivery"
    end

    function Supply_Hard:isInstantReward()
        return true
    end

    function Supply_Hard:isUnitTypeAllowed(unit)
        if PlayerLogistics then
            local unitType = unit:getDesc()['typeName']
            return PlayerLogistics.allowedTypes[unitType] and PlayerLogistics.allowedTypes[unitType].supplies
        end
    end

    function Supply_Hard:generateObjectives()
        self.completionType = Mission.completion_type.all
        local description = ''

        local viableZones = {}
        for _,zone in pairs(ZoneCommand.getAllZones()) do
            if zone.side == 2 and zone.distToFront == 0 and zone:criticalOnSupplies() then
                table.insert(viableZones, zone)
            end
        end

        if #viableZones == 0 then
            for _,zone in pairs(ZoneCommand.getAllZones()) do
                if zone.side == 2 and zone.distToFront == 1 and zone:criticalOnSupplies() then
                    table.insert(viableZones, zone)
                end
            end
        end
        
        if #viableZones > 0 then
            local choice = math.random(1,#viableZones)
            local zn = viableZones[choice]
            
            local deliver = ObjSupplyZone:new()
            deliver:initialize(self, {
                amount = math.random(18,24)*250,
                delivered = 0,
                tgtzone = zn
            })
            
            table.insert(self.objectives, deliver)
            description = description..'   Deliver '..deliver.param.amount..' of supplies to '..zn.name
            self.info = {
                targetzone = zn
            }
        end

        self.description = self.description..description
    end
end

-----------------[[ END OF Missions/Supply_Hard.lua ]]-----------------



-----------------[[ Missions/Strike_VeryEasy.lua ]]-----------------

Strike_VeryEasy = Mission:new()
do
    function Strike_VeryEasy.canCreate()
        return true
    end

    function Strike_VeryEasy:getMissionName()
        return 'Strike'
    end

    function Strike_VeryEasy:generateObjectives()
        self.completionType = Mission.completion_type.all
        local description = ''
        
        local kills = ObjDestroyUnitsWithAttribute:new()
        kills:initialize(self, {
            attr = {'Buildings'},
            amount = 1,
            killed = 0 
        })

        table.insert(self.objectives, kills)
        description = description..'   Destroy '..kills.param.amount..' building'
        self.description = self.description..description
    end
end

-----------------[[ END OF Missions/Strike_VeryEasy.lua ]]-----------------



-----------------[[ Missions/Strike_Easy.lua ]]-----------------

Strike_Easy = Mission:new()
do
    function Strike_Easy.canCreate()
        for _,zone in pairs(ZoneCommand.getAllZones()) do
            if zone.side == 1 and zone.distToFront and zone.distToFront <=1 and zone:hasUnitWithAttributeOnSide({'Buildings'}, 1) then
                if not MissionTargetRegistry.isZoneTargeted(zone.name) then
                    return true
                end
            end
        end
    end

    function Strike_Easy:getMissionName()
        return 'Strike'
    end

    function Strike_Easy:generateObjectives()
        self.completionType = Mission.completion_type.all
        local description = ''
        local viableZones = {}
        for _,zone in pairs(ZoneCommand.getAllZones()) do
            if zone.side == 1 and zone.distToFront == 0 and zone:hasUnitWithAttributeOnSide({'Buildings'}, 1) then
                if not MissionTargetRegistry.isZoneTargeted(zone.name) then
                    table.insert(viableZones, zone)
                end
            end
        end

        if #viableZones == 0 then
            for _,zone in pairs(ZoneCommand.getAllZones()) do
                if zone.side == 1 and zone.distToFront == 1 and zone:hasUnitWithAttributeOnSide({'Buildings'}, 1) then
                    if not MissionTargetRegistry.isZoneTargeted(zone.name) then
                        table.insert(viableZones, zone)
                    end
                end
            end
        end
        
        if #viableZones > 0 then
            local choice = math.random(1,#viableZones)
            local zn = viableZones[choice]
            
            local kill = ObjDestroyUnitsWithAttributeAtZone:new()
            kill:initialize(self, {
                attr = {'Buildings'},
                amount = 1,
                killed = 0,
                tgtzone = zn
            })

            table.insert(self.objectives, kill)
            description = description..'   Destroy '..kill.param.amount..' Building at '..zn.name
            self.info = {
                targetzone = zn
            }
        end
        self.description = self.description..description
    end
end

-----------------[[ END OF Missions/Strike_Easy.lua ]]-----------------



-----------------[[ Missions/Strike_Medium.lua ]]-----------------

Strike_Medium = Mission:new()
do
    function Strike_Medium.canCreate()
        return MissionTargetRegistry.strikeTargetsAvailable(1, false)
    end

    function Strike_Medium:getMissionName()
        return 'Strike'
    end

    function Strike_Medium:generateObjectives()
        self.completionType = Mission.completion_type.all
        local description = ''
        local viableZones = {}
       
        local tgt = MissionTargetRegistry.getRandomStrikeTarget(1, false)
        
        if tgt then
            local chozenTarget = tgt.data
            local zn = tgt.zone

            local kill = ObjDestroyStructure:new()
            kill:initialize(self, {
                target = chozenTarget,
                tgtzone = zn,
                killed = false
            })

            table.insert(self.objectives, kill)
            description = description..'   Destroy '..chozenTarget.display..' at '..zn.name
            self.info = {
                targetzone = zn
            }

            MissionTargetRegistry.removeStrikeTarget(tgt)
        end
        self.description = self.description..description
    end
end

-----------------[[ END OF Missions/Strike_Medium.lua ]]-----------------



-----------------[[ Missions/Strike_Hard.lua ]]-----------------

Strike_Hard = Mission:new()
do
    function Strike_Hard.canCreate()
        for _,zone in pairs(ZoneCommand.getAllZones()) do
            if zone.side == 1 and zone.distToFront and zone.distToFront <=1 and zone:hasUnitWithAttributeOnSide({"Buildings"}, 1, 3) then
                if not MissionTargetRegistry.isZoneTargeted(zone.name) then
                    return true
                end
            end
        end
    end

    function Strike_Hard:getMissionName()
        return 'Strike'
    end

    function Strike_Hard:generateObjectives()
        self.completionType = Mission.completion_type.all
        local description = ''
        local viableZones = {}
        for _,zone in pairs(ZoneCommand.getAllZones()) do
            if zone.side == 1 and zone.distToFront == 0 and zone:hasUnitWithAttributeOnSide({"Buildings"}, 1, 3) then
                if not MissionTargetRegistry.isZoneTargeted(zone.name) then
                    table.insert(viableZones, zone)
                end
            end
        end

        if #viableZones == 0 then
            for _,zone in pairs(ZoneCommand.getAllZones()) do
                if zone.side == 1 and zone.distToFront == 1 and zone:hasUnitWithAttributeOnSide({"Buildings"}, 1, 3) then
                    if not MissionTargetRegistry.isZoneTargeted(zone.name) then
                        table.insert(viableZones, zone)
                    end
                end
            end
        end
        
        if #viableZones > 0 then
            local choice = math.random(1,#viableZones)
            local zn = viableZones[choice]
            
            local kill = ObjDestroyUnitsWithAttributeAtZone:new()
            kill:initialize(self, { 
                attr = {"Buildings"},
                amount = 1,
                killed = 0,
                tgtzone = zn
            })

            table.insert(self.objectives, kill)

            local clear = ObjClearZoneOfUnitsWithAttribute:new()
            clear:initialize(self, {
                attr = {"Buildings"},
                tgtzone = zn
            })
            table.insert(self.objectives, clear)

            description = description..'   Destroy every structure at '..zn.name
            self.info = {
                targetzone = zn
            }
        end
        self.description = self.description..description
    end
end

-----------------[[ END OF Missions/Strike_Hard.lua ]]-----------------



-----------------[[ Missions/Deep_Strike.lua ]]-----------------

Deep_Strike = Mission:new()
do
    function Deep_Strike.canCreate()
        return MissionTargetRegistry.strikeTargetsAvailable(1, true)
    end

    function Deep_Strike:getMissionName()
        return 'Deep Strike'
    end

    function Deep_Strike:generateObjectives()
        self.completionType = Mission.completion_type.all
        local description = ''
        local viableZones = {}
       
        local tgt = MissionTargetRegistry.getRandomStrikeTarget(1, true)
        
        if tgt then
            local chozenTarget = tgt.data
            local zn = tgt.zone

            local kill = ObjDestroyStructure:new()
            kill:initialize(self, {
                target = chozenTarget,
                tgtzone = zn,
                killed = false
            })

            table.insert(self.objectives, kill)
            description = description..'   Destroy '..chozenTarget.display..' at '..zn.name
            self.info = {
                targetzone = zn
            }

            MissionTargetRegistry.removeStrikeTarget(tgt)
        end
        self.description = self.description..description
    end
end

-----------------[[ END OF Missions/Deep_Strike.lua ]]-----------------



-----------------[[ Missions/Escort.lua ]]-----------------

Escort = Mission:new()
do    
    function Escort.canCreate()
        local currentTime = timer.getAbsTime()
        for _,gr in pairs(ZoneCommand.groupMonitor.groups) do
            if gr.product.side == 2 and gr.product.type == 'mission' and (gr.product.missionType == 'supply_convoy' or gr.product.missionType == 'assault')  then
                local z = gr.target
                if z.distToFront == 0 and z.side~= 2 then
                    if gr.state == nil or gr.state == 'started' or (gr.state == 'enroute' and (currentTime - gr.lastStateTime < 7*60)) then
                        return true
                    end
                end
            end
        end
    end

    function Escort:getMissionName()
        return "Escort convoy"
    end

    function Escort:isUnitTypeAllowed(unit)
        return unit:hasAttribute('Helicopters')
    end

    function Escort:generateObjectives()
        self.completionType = Mission.completion_type.all
        local description = ''

        local currentTime = timer.getAbsTime()
        local viableConvoys = {}
        for _,gr in pairs(ZoneCommand.groupMonitor.groups) do
            if gr.product.side == 2 and gr.product.type == 'mission' and (gr.product.missionType == 'supply_convoy' or gr.product.missionType == 'assault')  then
                local z = gr.target
                if z.distToFront == 0 and z.side ~= 2 then
                    if gr.state == nil or gr.state == 'started' or (gr.state == 'enroute' and (currentTime - gr.lastStateTime < 7*60)) then
                        table.insert(viableConvoys, gr)
                    end
                end
            end
        end
        
        if #viableConvoys > 0 then
            local choice = math.random(1,#viableConvoys)
            local convoy = viableConvoys[choice]
            
            local escort = ObjEscortGroup:new()
            escort:initialize(self, {
                maxAmount = 60*7,
                amount = 60*7,
                proxDist = 400,
                target = convoy,
                lastUpdate = timer.getAbsTime()
            })
            
            table.insert(self.objectives, escort)

            local nearzone = ""
            local gr = Group.getByName(convoy.name)
            if gr and gr:getSize()>0 then
                local un = gr:getUnit(1)
                local closest = ZoneCommand.getClosestZoneToPoint(un:getPoint())
                if closest then
                    nearzone = ' near '..closest.name..''
                end
            end

            description = description..'   Escort convoy'..nearzone..' on route to their destination'
            --description = description..'\n   Target will be assigned after accepting mission'

        end

        self.description = self.description..description
    end
end

-----------------[[ END OF Missions/Escort.lua ]]-----------------



-----------------[[ Missions/TARCAP.lua ]]-----------------

TARCAP = Mission:new()
do
    TARCAP.relevantMissions = {
        Mission.types.cas_hard,
        Mission.types.dead,
        Mission.types.sead,
        Mission.types.strike_easy,
        Mission.types.strike_hard
    }

    function TARCAP:new(id, type, activeMissions)
        self = Mission.new(self, id, type)
        self:generateObjectivesOverload(activeMissions)
		return self
	end

    function TARCAP.canCreate(activeMissions)
        for _,mis in pairs(activeMissions) do
            for _,tp in ipairs(TARCAP.relevantMissions) do
                if mis.type == tp then return true end
            end
        end
    end

    function TARCAP:getMissionName()
        return 'TARCAP'
    end

    function TARCAP:isUnitTypeAllowed(unit)
        return unit:hasAttribute('Planes')
    end

    function TARCAP:generateObjectivesOverload(activeMissions)
        self.completionType = Mission.completion_type.any
        local description = ''
        local viableMissions = {}
        for _,mis in pairs(activeMissions) do
            for _,tp in ipairs(TARCAP.relevantMissions) do
                if mis.type == tp then
                    table.insert(viableMissions, mis)
                    break
                end
            end
        end
        
        if #viableMissions >= 1 then
            local choice = math.random(1,#viableMissions)
            local mis = viableMissions[choice]

            local protect = ObjProtectMission:new()
            protect:initialize(self, {
                mis = mis
            })

            table.insert(self.objectives, protect)
            description = description..'   Prevent enemy aircraft from interfering with friendly '..mis:getMissionName()..' mission'
            if mis.info and mis.info.targetzone then
                description = description..' at '..mis.info.targetzone.name
            end

            local rewardDef = RewardDefinitions.missions[self.type]

            local kills = ObjAirKillBonus:new()
            kills:initialize(self, {
                attr = {'Planes'},
                bonus = {
                    [PlayerTracker.statTypes.xp] = rewardDef.xp.boost
                },
                count = 0,
                linkedObjectives = {protect}
            })
    
            table.insert(self.objectives, kills)
            
            description = description..'\n   Aircraft kills increase reward'
        end

        self.description = self.description..description
    end
end

-----------------[[ END OF Missions/TARCAP.lua ]]-----------------



-----------------[[ Missions/Recon_Plane.lua ]]-----------------

Recon_Plane = Mission:new()
do
    function Recon_Plane.canCreate()
        local zoneNum = 0
        for _,zone in pairs(ZoneCommand.getAllZones()) do
            if zone.side == 1 and zone.distToFront == 0 then 
                return true
            end
        end
    end

    function Recon_Plane:getMissionName()
        return 'Recon'
    end

    function Recon_Plane:isUnitTypeAllowed(unit)
        return unit:hasAttribute('Planes')
    end

    function Recon_Plane:generateObjectives()
        self.completionType = Mission.completion_type.any
        local description = ''
        local viableZones = {}
        local secondaryViableZones = {}
        for _,zone in pairs(ZoneCommand.getAllZones()) do
            if zone.side == 1 and zone.distToFront == 0 then
                if zone.revealTime <= 60*5 then
                    table.insert(viableZones, zone)
                else
                    table.insert(secondaryViableZones, zone)
                end
            end
        end

        if #viableZones == 0 then
            viableZones = secondaryViableZones
        end
        
        
        if #viableZones > 0 then
            local choice1 = math.random(1,#viableZones)
            local zn1 = viableZones[choice1]

            local recon = ObjFlyToZoneSequence:new()
            recon:initialize(self,{
                waypoints = { 
                    [1] = {zone = zn1, complete = false}
                },
                failZones = {
                    [1] = {zn1}
                }
            })

            table.insert(self.objectives, recon)
            description = description..'   Overfly '..zn1.name..'\n'
        end

        self.description = self.description..description
    end

    function Recon_Plane:objectiveCompletedCallback(objective)
        if objective.type == ObjFlyToZoneSequence:getType() then
            local firstWP = objective.param.waypoints[1]

            if firstWP and firstWP.zone:hasUnitWithAttributeOnSide({'Buildings'}, 1) then
                local tgt = firstWP.zone:getRandomUnitWithAttributeOnSide({'Buildings'}, 1)
                if tgt then
                    MissionTargetRegistry.addStrikeTarget(tgt, firstWP.zone, true)
                    self:pushMessageToPlayers(tgt.display..' discovered at '..firstWP.zone.name)
                    firstWP.zone:reveal()
                end
            end
        end
    end
end

-----------------[[ END OF Missions/Recon_Plane.lua ]]-----------------



-----------------[[ Missions/Deep_Recon_Plane.lua ]]-----------------

Deep_Recon_Plane = Mission:new()
do
    function Deep_Recon_Plane.canCreate()
        local zoneNum = 0
        for _,zone in pairs(ZoneCommand.getAllZones()) do
            if zone.side == 1 and zone.distToFront == 2 then 
                return true
            end
        end
    end
    
    function Deep_Recon_Plane:getMissionName()
        return 'Deep Recon'
    end

    function Deep_Recon_Plane:isUnitTypeAllowed(unit)
        return unit:hasAttribute('Planes')
    end

    function Deep_Recon_Plane:generateObjectives()
        self.completionType = Mission.completion_type.any
        local description = ''
        local viableZones = {}
        local secondaryViableZones = {}
        for _,zone in pairs(ZoneCommand.getAllZones()) do
            if zone.side == 1 and zone.distToFront == 2 then
                if zone.revealTime <= 60*5 then
                    table.insert(viableZones, zone)
                else
                    table.insert(secondaryViableZones, zone)
                end
            end
        end

        if #viableZones == 0 then
            viableZones = secondaryViableZones
        end
        
        if #viableZones > 0 then
            local choice1 = math.random(1,#viableZones)
            local zn1 = viableZones[choice1]

            local recon = ObjFlyToZoneSequence:new()
            recon:initialize(self, {
                waypoints = { 
                    [1] = {zone = zn1, complete = false}
                },
                failZones = {
                    [1] = {zn1}
                }
            })

            table.insert(self.objectives, recon)
            description = description..'   Overfly '..zn1.name..'\n'
        end

        self.description = self.description..description
    end

    function Deep_Recon_Plane:objectiveCompletedCallback(objective)
        if objective.type == ObjFlyToZoneSequence:getType() then
            local firstWP = objective.param.waypoints[1]

            if firstWP and firstWP.zone:hasUnitWithAttributeOnSide({'Buildings'}, 1) then
                local tgt = firstWP.zone:getRandomUnitWithAttributeOnSide({'Buildings'}, 1)
                if tgt then
                    MissionTargetRegistry.addStrikeTarget(tgt, firstWP.zone, true)
                    self:pushMessageToPlayers(tgt.display..' discovered at '..firstWP.zone.name)
                    firstWP.zone:reveal()
                end
            end
        end
    end
end

-----------------[[ END OF Missions/Deep_Recon_Plane.lua ]]-----------------



-----------------[[ Missions/Scout_Helo.lua ]]-----------------

Scout_Helo = Mission:new()
do
    function Scout_Helo.canCreate()
        local zoneNum = 0
        for _,zone in pairs(ZoneCommand.getAllZones()) do
            if zone.side == 1 and zone.distToFront == 0 then 
                return true
            end
        end
    end

    function Scout_Helo:getMissionName()
        return 'Recon'
    end

    function Scout_Helo:isUnitTypeAllowed(unit)
        return unit:hasAttribute('Helicopters')
    end

    function Scout_Helo:generateObjectives()
        self.completionType = Mission.completion_type.any
        local description = ''
        local viableZones = {}
        local secondaryViableZones = {}
        for _,zone in pairs(ZoneCommand.getAllZones()) do
            if zone.side == 1 and zone.distToFront == 0 then
                if zone.revealTime <= 60*5 then
                    table.insert(viableZones, zone)
                else
                    table.insert(secondaryViableZones, zone)
                end
            end
        end

        if #viableZones == 0 then
            viableZones = secondaryViableZones
        end
        
        if #viableZones > 0 then
            local choice1 = math.random(1,#viableZones)
            local zn1 = viableZones[choice1]

            local recon = ObjReconZone:new()
            recon:initialize(self, {
                target = zn1,
                maxAmount = 60*1.5,
                amount = 60*1.5,
                allowedDeviation = 20,
                proxDist = 10000,
                lastUpdate = timer.getAbsTime(),
                failZones = {
                    [1] = {zn1}
                }
            })

            table.insert(self.objectives, recon)
            description = description..'   Observe enemies at '..zn1.name..'\n'
        end

        self.description = self.description..description
    end

    function Scout_Helo:objectiveCompletedCallback(objective)
        if objective.type == ObjReconZone:getType() then
            if objective.param.target:hasUnitWithAttributeOnSide({'Buildings'}, 1) then
                local tgt = objective.param.target:getRandomUnitWithAttributeOnSide({'Buildings'}, 1)
                if tgt then
                    MissionTargetRegistry.addStrikeTarget(tgt, objective.param.target, false)
                    self:pushMessageToPlayers(tgt.display..' discovered at '..objective.param.target.name)
                    objective.param.target:reveal()
                end
            end
        end
    end
end

-----------------[[ END OF Missions/Scout_Helo.lua ]]-----------------



-----------------[[ Missions/BAI.lua ]]-----------------

BAI = Mission:new()
do
    function BAI.canCreate()
        return MissionTargetRegistry.baiTargetsAvailable(1)
    end

    function BAI:getMissionName()
        return 'BAI'
    end

    function BAI:generateObjectives()
        self.completionType = Mission.completion_type.all
        local description = ''
        local viableZones = {}
       
        local tgt = MissionTargetRegistry.getRandomBaiTarget(1)
        
        if tgt then

            local gr = Group.getByName(tgt.name)
            if gr and gr:getSize()>0 then
                local units = {}
                for i,v in ipairs(gr:getUnits()) do
                    units[v:getName()] = false
                end

                local kill = ObjDestroyGroup:new() 
                kill:initialize(self, {
                    target = tgt,
                    targetUnitNames = units,
                    lastUpdate = timer.getAbsTime()
                })

                table.insert(self.objectives, kill)

                local nearzone = ""
                local un = gr:getUnit(1)
                local closest = ZoneCommand.getClosestZoneToPoint(un:getPoint())
                if closest then
                    nearzone = ' near '..closest.name..''
                end

                description = description..'   Destroy '..tgt.product.display..nearzone..' before it reaches its destination.'
            end

            MissionTargetRegistry.removeBaiTarget(tgt)
        end
        self.description = self.description..description
    end
end

-----------------[[ END OF Missions/BAI.lua ]]-----------------



-----------------[[ Missions/Anti_Runway.lua ]]-----------------

Anti_Runway = Mission:new()
do
    function Anti_Runway.canCreate()
        for _,zone in pairs(ZoneCommand.getAllZones()) do
            if zone.side == 1 and zone.distToFront <=2 and zone:hasRunway() then
                    return true
            end
        end
    end

    function Anti_Runway:getMissionName()
        return 'Runway Attack'
    end

    function Anti_Runway:generateObjectives()
        self.completionType = Mission.completion_type.all
        local description = ''
        local viableZones = {}
       
        local tgts = {}
        for _,zone in pairs(ZoneCommand.getAllZones()) do
            if zone.side == 1 and zone.distToFront <=2 and zone:hasRunway() then
                if not MissionTargetRegistry.isZoneTargeted(zone.name) then
                    table.insert(tgts, zone)
                end
            end
        end
        
        if #tgts > 0 then
            local tgt = tgts[math.random(1,#tgts)]

            local rewardDef = RewardDefinitions.missions[self.type]

            local bomb = ObjBombInsideZone:new()
            bomb:initialize(self,{
                targetZone = tgt,
                max = 20,
                required = 5,
                dropped = 0,
                isFinishStarted = false,
                bonus = {
                    [PlayerTracker.statTypes.xp] = rewardDef.xp.boost
                }
            })

            table.insert(self.objectives, bomb)
            description = description..'   Bomb runway at '..bomb.param.targetZone.name
        end
        self.description = self.description..description
    end
end

-----------------[[ END OF Missions/Anti_Runway.lua ]]-----------------



-----------------[[ Missions/CSAR.lua ]]-----------------

CSAR = Mission:new()
do
    function CSAR.canCreate()
        return MissionTargetRegistry.pilotsAvailableToExtract()
    end

    function CSAR:getMissionName()
        return 'CSAR'
    end

    function CSAR:isInstantReward()
        return true
    end

    function CSAR:isUnitTypeAllowed(unit)
        if PlayerLogistics then
            local unitType = unit:getDesc()['typeName']
            return PlayerLogistics.allowedTypes[unitType] and PlayerLogistics.allowedTypes[unitType].personCapacity and PlayerLogistics.allowedTypes[unitType].personCapacity > 0
        end
    end

    function CSAR:generateObjectives()
        self.completionType = Mission.completion_type.all
        local description = ''
        
        if MissionTargetRegistry.pilotsAvailableToExtract() then
            local tgt = MissionTargetRegistry.getRandomPilot()
            
            local extract = ObjExtractPilot:new()
            extract:initialize(self, {
                target = tgt,
                loadedBy = nil,
                lastUpdate = timer.getAbsTime()
            })
            table.insert(self.objectives, extract)

            local unload = ObjUnloadExtractedPilotOrSquad:new()
            unload:initialize(self, {
                extractObjective = extract
            })
            table.insert(self.objectives, unload)

            local nearzone = ''
            local closest = ZoneCommand.getClosestZoneToPoint(tgt.pilot:getUnit(1):getPoint())
            if closest then
                nearzone = ' near '..closest.name..''
            end

            description = description..'   Rescue '..tgt.name..nearzone..' and deliver them to a friendly zone'
            --local mgrs = coord.LLtoMGRS(coord.LOtoLL(tgt.pilot:getUnit(1):getPoint()))
            --local grid = mist.tostringMGRS(mgrs, 2):gsub(' ','')
            --description = description..' ['..grid..']'
        end
        self.description = self.description..description
    end
end

-----------------[[ END OF Missions/CSAR.lua ]]-----------------



-----------------[[ Missions/Extraction.lua ]]-----------------

Extraction = Mission:new()
do
    function Extraction.canCreate()
        return MissionTargetRegistry.squadsReadyToExtract()
    end

    function Extraction:getMissionName()
        return 'Extraction'
    end

    function Extraction:isInstantReward()
        return true
    end
    
    function Extraction:isUnitTypeAllowed(unit)
        if PlayerLogistics then
            local unitType = unit:getDesc()['typeName']
            return PlayerLogistics.allowedTypes[unitType] and PlayerLogistics.allowedTypes[unitType].personCapacity
        end
    end

    function Extraction:generateObjectives()
        self.completionType = Mission.completion_type.all
        local description = ''
        
        if MissionTargetRegistry.squadsReadyToExtract() then
            local tgt = MissionTargetRegistry.getRandomSquad()
            if tgt then
                local extract = ObjExtractSquad:new()
                extract:initialize(self, {
                    target = tgt,
                    loadedBy = nil,
                    lastUpdate = timer.getAbsTime()
                })
                table.insert(self.objectives, extract)

                local unload = ObjUnloadExtractedPilotOrSquad:new()
                unload:initialize(self, {
                    extractObjective = extract
                })
                table.insert(self.objectives, unload)

                local infName = PlayerLogistics.getInfantryName(tgt.data.type)

                
                local nearzone = ''
                local gr = Group.getByName(tgt.name)
                if gr and gr:isExist() and gr:getSize()>0 then
                    local un = gr:getUnit(1)
                    local closest = ZoneCommand.getClosestZoneToPoint(un:getPoint())
                    if closest then
                        nearzone = ' near '..closest.name..''
                    end
                    --local mgrs = coord.LLtoMGRS(coord.LOtoLL(un:getPoint()))
                    --local grid = mist.tostringMGRS(mgrs, 2):gsub(' ','')
                    --description = description..' ['..grid..']'
                end

                description = description..'   Extract '..infName..nearzone..' to a friendly zone'
            end
        end
        self.description = self.description..description
    end
end

-----------------[[ END OF Missions/Extraction.lua ]]-----------------



-----------------[[ Missions/DeploySquad.lua ]]-----------------

DeploySquad = Mission:new()
do
    function DeploySquad.canCreate()
        for _,zone in pairs(ZoneCommand.getAllZones()) do
            if zone.distToFront and zone.distToFront == 0 then
                if not MissionTargetRegistry.isZoneTargeted(zone.name) then
                    return true
                end
            end
        end
    end

    function DeploySquad:getMissionName()
        return 'Deploy infantry'
    end

    function DeploySquad:isInstantReward()
        local friendlyDeployments = {
            [PlayerLogistics.infantryTypes.engineer] = true,
        }

        if self.objectives and self.objectives[1] then
            local sqType = self.objectives[1].param.squadType
            if friendlyDeployments[sqType] then
                return true
            end
        end

        return false
    end
    
    function DeploySquad:isUnitTypeAllowed(unit)
        if PlayerLogistics then
            local unitType = unit:getDesc()['typeName']
            return PlayerLogistics.allowedTypes[unitType] and PlayerLogistics.allowedTypes[unitType].personCapacity
        end
    end

    function DeploySquad:generateObjectives()
        self.completionType = Mission.completion_type.all
        local description = ''

        local viableZones = {}
        for _,zone in pairs(ZoneCommand.getAllZones()) do
            if zone.distToFront and zone.distToFront == 0 then
                if not MissionTargetRegistry.isZoneTargeted(zone.name) then
                    table.insert(viableZones, zone)
                end
            end
        end

        if #viableZones > 0 then
            local tgt = viableZones[math.random(1,#viableZones)]
            if tgt then
                local squadType = nil

                if tgt.side == 0 then
                    squadType = PlayerLogistics.infantryTypes.capture
                elseif tgt.side == 1 then
                    if math.random()>0.5 then
                        squadType = PlayerLogistics.infantryTypes.sabotage
                    else
                        squadType = PlayerLogistics.infantryTypes.spy
                    end
                elseif tgt.side == 2 then
                    squadType = PlayerLogistics.infantryTypes.engineer
                end

                local deploy = ObjDeploySquad:new()
                deploy:initialize(self, {
                    squadType = squadType,
                    targetZone = tgt,
                    requiredZoneSide = tgt.side,
                    unloadedType = nil,
                    unloadedAt = nil
                })
                table.insert(self.objectives, deploy)

                local infName = PlayerLogistics.getInfantryName(squadType)

                description = description..'   Deploy '..infName..' to '..tgt.name
                
                self.info = {
                    targetzone = tgt
                }
            end
        end
        self.description = self.description..description
    end
end

-----------------[[ END OF Missions/DeploySquad.lua ]]-----------------



-----------------[[ RewardDefinitions.lua ]]-----------------

RewardDefinitions = {}

do
    RewardDefinitions.missions = {
      [Mission.types.cap_easy]        = { xp = { low = 10, high = 20, boost = 0   } },
      [Mission.types.cap_medium]      = { xp = { low = 10, high = 20, boost = 100 } },
      [Mission.types.tarcap]          = { xp = { low = 10, high = 10, boost = 150 } },
      [Mission.types.cas_easy]        = { xp = { low = 10, high = 20, boost = 0   } },
      [Mission.types.cas_medium]      = { xp = { low = 20, high = 30, boost = 0   } },
      [Mission.types.cas_hard]        = { xp = { low = 30, high = 40, boost = 0   } },
      [Mission.types.bai]             = { xp = { low = 20, high = 30, boost = 0   } },
      [Mission.types.sead]            = { xp = { low = 10, high = 20, boost = 0   } },
      [Mission.types.dead]            = { xp = { low = 30, high = 40, boost = 0   } },
      [Mission.types.strike_veryeasy] = { xp = { low = 5,  high = 10, boost = 0   } },
      [Mission.types.strike_easy]     = { xp = { low = 10, high = 20, boost = 0   } },
      [Mission.types.strike_medium]   = { xp = { low = 20, high = 30, boost = 0   } },
      [Mission.types.strike_hard]     = { xp = { low = 30, high = 40, boost = 0   } },
      [Mission.types.deep_strike]     = { xp = { low = 30, high = 40, boost = 0   } },
      [Mission.types.recon_plane]     = { xp = { low = 20, high = 30, boost = 0   } },
      [Mission.types.recon_plane_deep]= { xp = { low = 30, high = 40, boost = 0   } },
      [Mission.types.anti_runway]     = { xp = { low = 20, high = 30, boost = 25  } },
      [Mission.types.supply_easy]     = { xp = { low = 10, high = 20, boost = 0   } },
      [Mission.types.supply_hard]     = { xp = { low = 20, high = 30, boost = 0   } },
      [Mission.types.escort]          = { xp = { low = 20, high = 30, boost = 0   } },
      [Mission.types.scout_helo]      = { xp = { low = 20, high = 30, boost = 0   } },
      [Mission.types.csar]            = { xp = { low = 20, high = 30, boost = 0   } },
      [Mission.types.extraction]      = { xp = { low = 20, high = 30, boost = 0   } },
      [Mission.types.deploy_squad]    = { xp = { low = 20, high = 30, boost = 0   } }
    }

    RewardDefinitions.actions = {
      pilotExtract = 100,
      squadDeploy = 150,
      squadExtract = 150,
      supplyRatio = 0.06,
      supplyBoost = 0.5
    }
end

-----------------[[ END OF RewardDefinitions.lua ]]-----------------



-----------------[[ MissionTracker.lua ]]-----------------

MissionTracker = {}
do
    MissionTracker.maxMissionCount = {
        [Mission.types.cap_easy] = 1,
        [Mission.types.cap_medium] = 1,
        [Mission.types.cas_easy] = 1,
        [Mission.types.cas_medium] = 1,
        [Mission.types.cas_hard] = 1,
        [Mission.types.sead] = 1,
        [Mission.types.supply_easy] = 1,
        [Mission.types.supply_hard] = 1,
        [Mission.types.strike_veryeasy] = 1,
        [Mission.types.strike_easy] = 1,
        [Mission.types.strike_medium] = 3,
        [Mission.types.strike_hard] = 1,
        [Mission.types.dead] = 1,
        [Mission.types.escort] = 1,
        [Mission.types.tarcap] = 1,
        [Mission.types.recon_plane] = 1,
        [Mission.types.recon_plane_deep] = 1,
        [Mission.types.deep_strike] = 3,
        [Mission.types.scout_helo] = 1,
        [Mission.types.bai] = 1,
        [Mission.types.anti_runway] = 1,
        [Mission.types.csar] = 1,
        [Mission.types.extraction] = 1,
        [Mission.types.deploy_squad] = 1,
    }

    if Config.missions then
        for i,v in pairs(Config.missions) do
            if MissionTracker.maxMissionCount[i] then
                MissionTracker.maxMissionCount[i] = v
            end
        end
    end

    MissionTracker.missionBoardSize = 10

	function MissionTracker:new(playerTracker, markerCommands)
		local obj = {}
        obj.playerTracker = playerTracker
        obj.markerCommands = markerCommands
        obj.groupMenus = {}
        obj.missionIDPool = {}
        obj.missionBoard = {}
        obj.activeMissions = {}
		
		setmetatable(obj, self)
		self.__index = self

        obj.markerCommands:addCommand('list', function(event, _, state) 
            if event.initiator then
                state:printMissionBoard(event.initiator:getID(), nil, event.initiator:getGroup():getName())
            elseif world.getPlayer() then
                local unit = world.getPlayer()
                state:printMissionBoard(unit:getID(), nil, event.initiator:getGroup():getName())
            end
            return true
        end, nil, obj)

        obj.markerCommands:addCommand('help', function(event, _, state) 
            if event.initiator then
                state:printHelp(event.initiator:getID())
            elseif world.getPlayer() then
                local unit = world.getPlayer()
                state:printHelp(unit:getID())
            end
            return true
        end, nil, obj)

        obj.markerCommands:addCommand('active', function(event, _, state) 
            if event.initiator then
                state:printActiveMission(event.initiator:getID(), nil, event.initiator:getPlayerName())
            elseif world.getPlayer() then
                state:printActiveMission(nil, nil, world.getPlayer():getPlayerName())
            end
            return true
        end, nil, obj)

        obj.markerCommands:addCommand('accept',function(event, code, state) 
            local numcode = tonumber(code)
            if not numcode or numcode<1000 or numcode > 9999 then return false end

            local player = ''
            local unit = nil
            if event.initiator then 
                player = event.initiator:getPlayerName()
                unit = event.initiator
            elseif world.getPlayer() then
                player = world.getPlayer():getPlayerName()
                unit = world.getPlayer()
            end

            return state:activateMission(numcode, player, unit)
        end, true, obj)

        obj.markerCommands:addCommand('join',function(event, code, state) 
            local numcode = tonumber(code)
            if not numcode or numcode<1000 or numcode > 9999 then return false end

            local player = ''
            local unit = nil
            if event.initiator then 
                player = event.initiator:getPlayerName()
                unit = event.initiator
            elseif world.getPlayer() then
                player = world.getPlayer():getPlayerName()
                unit = world.getPlayer()
            end

            return state:joinMission(numcode, player, unit)
        end, true, obj)

        obj.markerCommands:addCommand('leave',function(event, _, state) 
            local player = ''
            if event.initiator then 
                player = event.initiator:getPlayerName()
            elseif world.getPlayer() then
                player = world.getPlayer():getPlayerName()
            end

            return state:leaveMission(player)
        end, nil, obj)

        obj:menuSetup()
		obj:start()
		return obj
	end

    function MissionTracker:menuSetup()
        MenuRegistry:register(2, function(event, context)
            if event.id == world.event.S_EVENT_BIRTH and event.initiator and event.initiator.getPlayerName then
				local player = event.initiator:getPlayerName()
				if player then
					local groupid = event.initiator:getGroup():getID()
                    local groupname = event.initiator:getGroup():getName()

                    if context.groupMenus[groupid] then
                        missionCommands.removeItemForGroup(groupid, context.groupMenus[groupid])
                        context.groupMenus[groupid] = nil
                    end

                    if not context.groupMenus[groupid] then
                        local menu = missionCommands.addSubMenuForGroup(groupid, 'Missions')
                        missionCommands.addCommandForGroup(groupid, 'List Missions', menu, Utils.log(context.printMissionBoard), context, nil, groupid, groupname)
                        missionCommands.addCommandForGroup(groupid, 'Active Mission', menu, Utils.log(context.printActiveMission), context, nil, groupid, nil, groupname)
                        
                        local dial = missionCommands.addSubMenuForGroup(groupid, 'Dial Code', menu)
                        for i1=1,5,1 do
                            local digit1 = missionCommands.addSubMenuForGroup(groupid, i1..'___', dial)
                            for i2=1,5,1 do
                                local digit2 = missionCommands.addSubMenuForGroup(groupid, i1..i2..'__', digit1)
                                for i3=1,5,1 do
                                    local digit3 = missionCommands.addSubMenuForGroup(groupid, i1..i2..i3..'_', digit2)
                                    for i4=1,5,1 do
                                        local code = tonumber(i1..i2..i3..i4)
                                        local digit4 = missionCommands.addCommandForGroup(groupid, i1..i2..i3..i4, digit3, Utils.log(context.activateOrJoinMissionForGroup), context, code, groupname)
                                    end
                                end
                            end
                        end
                        
                        local leavemenu = missionCommands.addSubMenuForGroup(groupid, 'Leave Mission', menu)
                        missionCommands.addCommandForGroup(groupid, 'Confirm to leave mission', leavemenu, Utils.log(context.leaveMission), context, player)
                        missionCommands.addCommandForGroup(groupid, 'Cancel', leavemenu, function() end)

                        missionCommands.addCommandForGroup(groupid, 'Help', menu, Utils.log(context.printHelp), context, nil, groupid)
                        
                        context.groupMenus[groupid] = menu
                    end
				end
			elseif (event.id == world.event.S_EVENT_PLAYER_LEAVE_UNIT or event.id == world.event.S_EVENT_DEAD) and event.initiator and event.initiator.getPlayerName then
                local player = event.initiator:getPlayerName()
				if player then
					local groupid = event.initiator:getGroup():getID()
					
					if context.groupMenus[groupid] then
                        missionCommands.removeItemForGroup(groupid, context.groupMenus[groupid])
                        context.groupMenus[groupid] = nil
                    end
				end
            end
        end, self)
    end

    function MissionTracker:printHelp(unitid, groupid)
        local msg = 'Missions can only be accepted or joined while landed at a friendly zone.\n'
        msg = msg.. 'Rewards from mission completion need to be claimed by landing at a friendly zone.\n\n'
        msg = msg.. 'Accept mission:\n'
        msg = msg.. ' Each mission has a 4 digit code listed next to its name.\n To accept a mission, either dial its code from the mission radio menu,\n or create a marker on the map and set its text to:\n'
        msg = msg.. '   accept:code\n'
        msg = msg.. ' (ex. accept:4126)\n\n'
        msg = msg.. 'Join mission:\n'
        msg = msg.. ' You can team up with other players, by joining a mission they already accepted.\n'
        msg = msg.. ' Missions can only be joined if all players who are already part of that mission\n have not taken off yet.\n'
        msg = msg.. ' When a mission is completed each player has to land to claim their reward individually.\n'
        msg = msg.. ' To join a mission, ask for the join code from a player who is already part of the mission,\n dial it in from the mission radio menu,\n or create a marker on the map and set its text to:\n'
        msg = msg.. '   join:code\n'
        msg = msg.. ' (ex. join:4126)\n\n'
        msg = msg.. 'Map marker commands:\n'
        msg = msg.. ' list - displays mission board\n'
        msg = msg.. ' accept:code - accepts mission with corresponding code\n'
        msg = msg.. ' join:code - joins other players mission with corresponding code\n'
        msg = msg.. ' active - displays active mission\n'
        msg = msg.. ' leave - leaves active mission\n'
        msg = msg.. ' help - displays this message'

        if unitid then
            trigger.action.outTextForUnit(unitid, msg, 30)
        elseif groupid then
            trigger.action.outTextForGroup(groupid, msg, 30)
        else
            --trigger.action.outText(msg, 30)
        end
    end

    function MissionTracker:printActiveMission(unitid, groupid, playername, groupname)
        if not playername and groupname then
            env.info('MissionTracker - printActiveMission: '..tostring(groupname)..' requested group print.')
            local gr = Group.getByName(groupname)
            for i,v in ipairs(gr:getUnits()) do
                if v.getPlayerName and v:getPlayerName() then 
                    self:printActiveMission(v:getID(), gr:getID(), v:getPlayerName())
                end
            end
            return
        end

        local mis = nil
        for i,v in pairs(self.activeMissions) do
            for pl,un in pairs(v.players) do
                if pl == playername then
                    mis = v
                    break
                end
            end

            if mis then break end
        end

        local msg = ''
        if mis then
            msg = mis:getDetailedDescription()
        else
            msg = 'No active mission'
        end

        if unitid then
            trigger.action.outTextForUnit(unitid, msg, 30)
        elseif groupid then
            trigger.action.outTextForGroup(groupid, msg, 30)
        else
            --trigger.action.outText(msg, 30)
        end
    end

    function MissionTracker:printMissionBoard(unitid, groupid, groupname)
        local gr = Group.getByName(groupname)
        local un = gr:getUnit(1)

        local msg = 'Mission Board\n'
        local empty = true
        local invalidCount = 0
        for i,v in pairs(self.missionBoard) do
            if v:isUnitTypeAllowed(un) then
                empty = false
                msg = msg..'\n'..v:getBriefDescription()..'\n'
            else
                invalidCount = invalidCount + 1
            end
        end

        if empty then 
            msg = msg..'\n No missions available'
        end

        if invalidCount > 0 then
            msg = msg..'\n'..invalidCount..' additional missions are not compatible with current aircraft\n'
        end

        if unitid then
            trigger.action.outTextForUnit(unitid, msg, 30)
        elseif groupid then
            trigger.action.outTextForGroup(groupid, msg, 30)
        else
            --trigger.action.outText(msg, 30)
        end
    end

    function MissionTracker:getNewMissionID()
        if #self.missionIDPool == 0 then
            for i=1111,5555,1 do 
                if not tostring(i):find('[06789]') then
                    if not self.missionBoard[i] and not self.activeMissions[i] then
                        table.insert(self.missionIDPool, i)
                    end
                end
            end
        end
        
        local choice = math.random(1,#self.missionIDPool)
        local newId = self.missionIDPool[choice]
        table.remove(self.missionIDPool,choice)
        return newId
    end
	
	function MissionTracker:start()
        timer.scheduleFunction(function(param, time)
            for code,mis in pairs(param.missionBoard) do
                if timer.getAbsTime() - mis.lastStateTime > mis.expireTime then
                    param.missionBoard[code].state = Mission.states.failed
                    param.missionBoard[code] = nil
                    env.info('Mission code'..code..' expired.')
                else
                    mis:updateIsFailed()
                    if mis.state == Mission.states.failed then
                        param.missionBoard[code]=nil
                        env.info('Mission code'..code..' canceled due to objectives failed')
                        trigger.action.outTextForCoalition(2,'Mission ['..mis.missionID..'] '..mis.name..' was cancelled',5)
                    end
                end
            end

            local misCount = Utils.getTableSize(param.missionBoard)
            local toGen = MissionTracker.missionBoardSize-misCount
            if toGen > 0 then
                local validMissions = {}
                for _,v in pairs(Mission.types) do
                    if self:canCreateMission(v) then
                        table.insert(validMissions,v)
                    end
                end

                if #validMissions > 0  then
                    for i=1,toGen,1 do
                        if #validMissions > 0 then
                            local choice = math.random(1,#validMissions)
                            local misType = validMissions[choice]
                            table.remove(validMissions, choice)
                            param:generateMission(misType)
                        else
                            break
                        end
                    end
                end
            end

            return time+1
        end, self, timer.getTime()+1)

        timer.scheduleFunction(function(param, time)
            for code,mis in pairs(param.activeMissions) do
                -- check if players exist and in same unit as when joined
                -- remove from mission if false
                for pl,un in pairs(mis.players) do
                    if not un or
                        not un:isExist() then

                        mis:removePlayer(pl)
                        env.info('Mission code'..code..' removing player '..pl..', unit no longer exists')
                    end
                end
                
                -- check if mission has 0 players, delete mission if true
                if not mis:hasPlayers() then
                    param.activeMissions[code]:updateState(Mission.states.failed)
                    param.activeMissions[code] = nil
                    env.info('Mission code'..code..' canceled due to no players')
                else
                    --check if mission objectives can still be completed, cancel mission if not
                    mis:updateIsFailed()
                    mis:updateIsCompleted()

                    if mis.state == Mission.states.preping then
                        --check if any player in air and move to comencing if true
                        for pl,un in pairs(mis.players) do
                            if Utils.isInAir(un) then
                                mis:updateState(Mission.states.comencing)
                                mis:pushMessageToPlayers(mis.name..' mission is starting')
                                break
                            end
                        end
                    elseif mis.state == Mission.states.comencing then
                        --check if all players in air and move to active if true
                        --if all players landed, move to preping
                        local allInAir = true
                        local allLanded = true
                        for pl,un in pairs(mis.players) do
                            if Utils.isInAir(un) then
                                allLanded = false
                            else
                                allInAir = false
                            end
                        end

                        if allLanded then
                            mis:updateState(Mission.states.preping)
                            mis:pushMessageToPlayers(mis.name..' mission is in the prep phase')
                        end

                        if allInAir then
                            mis:updateState(Mission.states.active)
                            mis:pushMessageToPlayers(mis.name..' mission has started')
                            local missionstatus = mis:getDetailedDescription()
                            mis:pushMessageToPlayers(missionstatus)
                        end
                    elseif mis.state == Mission.states.active then
                        mis:updateObjectives()
                    elseif mis.state == Mission.states.completed then
                        local isInstant = mis:isInstantReward()
                        if isInstant then
                            mis:pushMessageToPlayers(mis.name..' mission complete.', 60)
                        else
                            mis:pushMessageToPlayers(mis.name..' mission complete. Land to claim rewards.', 60)
                        end 

                        for _,reward in ipairs(mis.rewards) do
                            for p,_ in pairs(mis.players) do
                                if isInstant then
                                    param.playerTracker:addStat(p, reward.amount, reward.type)
                                else
                                    param.playerTracker:addTempStat(p, reward.amount, reward.type)
                                end
                            end

                            if isInstant then
                                mis:pushMessageToPlayers('+'..reward.amount..' '..reward.type)
                            end
                        end

                        for p,u in pairs(mis.players) do
                            param.playerTracker:addRankRewards(p,u, not isInstant)
                        end

                        mis:pushSoundToPlayers("success.ogg")
                        param.activeMissions[code] = nil
                        env.info('Mission code'..code..' removed due to completion')
                    elseif mis.state == Mission.states.failed then
                        local msg = mis.name..' mission failed.'
                        if mis.failureReason then
                            msg = msg..'\n'..mis.failureReason
                        end

                        mis:pushMessageToPlayers(msg, 60)

                        mis:pushSoundToPlayers("fail.ogg")
                        param.activeMissions[code] = nil
                        env.info('Mission code'..code..' removed due to failure')
                    end
                end
            end

            return time+1
        end, self, timer.getTime()+1)

        local ev = {}
		ev.context = self
		function ev:onEvent(event)
			if event.id == world.event.S_EVENT_KILL and event.initiator and event.target and event.initiator.getPlayerName then
				local player = event.initiator:getPlayerName()
				if player and 
                    event.initiator:isExist() and
                    event.initiator.getCoalition and 
                    event.target.getCoalition and 
                    event.initiator:getCoalition() ~= event.target:getCoalition() then
					    self.context:tallyKill(player, event.target)
				end
			end

            if event.id == world.event.S_EVENT_SHOT and event.initiator and event.weapon and event.initiator.getPlayerName then
                local player = event.initiator:getPlayerName()
				if player and event.initiator:isExist() and event.weapon:isExist() then
                    self.context:tallyWeapon(player, event.weapon)
                end
            end
		end
		
		world.addEventHandler(ev)
	end

    function MissionTracker:generateMission(misType)
        local misid = self:getNewMissionID()
        env.info('MissionTracker - generating mission type ['..misType..'] id code['..misid..']')
        
        local newmis = nil
        if misType == Mission.types.cap_easy then
            newmis = CAP_Easy:new(misid, misType)
        elseif misType == Mission.types.cap_medium then
            newmis = CAP_Medium:new(misid, misType)
        elseif misType == Mission.types.cas_easy then
            newmis = CAS_Easy:new(misid, misType)
        elseif misType == Mission.types.cas_medium then
            newmis = CAS_Medium:new(misid, misType)
        elseif misType == Mission.types.cas_hard then
            newmis = CAS_Hard:new(misid, misType)
        elseif misType == Mission.types.sead then
            newmis = SEAD:new(misid, misType)
        elseif misType == Mission.types.supply_easy then
            newmis = Supply_Easy:new(misid, misType)
        elseif misType == Mission.types.supply_hard then
            newmis = Supply_Hard:new(misid, misType)
        elseif misType == Mission.types.strike_veryeasy then
            newmis = Strike_VeryEasy:new(misid, misType)
        elseif misType == Mission.types.strike_easy then
            newmis = Strike_Easy:new(misid, misType)
        elseif misType == Mission.types.strike_medium then
            newmis = Strike_Medium:new(misid, misType)
        elseif misType == Mission.types.strike_hard then
            newmis = Strike_Hard:new(misid, misType)
        elseif misType == Mission.types.deep_strike then
            newmis = Deep_Strike:new(misid, misType)
        elseif misType == Mission.types.dead then
            newmis = DEAD:new(misid, misType)
        elseif misType == Mission.types.escort then
            newmis = Escort:new(misid, misType)
        elseif misType == Mission.types.tarcap then
            newmis = TARCAP:new(misid, misType, self.activeMissions)
        elseif misType == Mission.types.recon_plane then
            newmis = Recon_Plane:new(misid, misType)
        elseif misType == Mission.types.recon_plane_deep then
            newmis = Deep_Recon_Plane:new(misid, misType)
        elseif misType == Mission.types.scout_helo then
            newmis = Scout_Helo:new(misid, misType)
        elseif misType == Mission.types.bai then
            newmis = BAI:new(misid, misType)
        elseif misType == Mission.types.anti_runway then
            newmis = Anti_Runway:new(misid, misType)
        elseif misType == Mission.types.csar then
            newmis = CSAR:new(misid, misType)
        elseif misType == Mission.types.extraction then
            newmis = Extraction:new(misid, misType)
        elseif misType == Mission.types.deploy_squad then
            newmis = DeploySquad:new(misid, misType)
        end

        if not newmis then return end

        if #newmis.objectives == 0 then return end

        self.missionBoard[misid] = newmis
        env.info('MissionTracker - generated mission id code'..misid..' \n'..newmis.description)
        trigger.action.outTextForCoalition(2,'New mission available: '..newmis.name,5)
    end

    function MissionTracker:tallyWeapon(player, weapon)
        for _,m in pairs(self.activeMissions) do
            if m.players[player] then
                if m.state == Mission.states.active then
                    if weapon:getDesc().category == Weapon.Category.BOMB then
                        timer.scheduleFunction(function (params, time)
                            if not params.weapon:isExist() then
                                return nil -- weapon despawned
                            end

                            local alt = Utils.getAGL(params.weapon)
                            if alt < 5 then 
                                params.mission:tallyWeapon(params.weapon)
                                return nil
                            end

                            if alt < 20 then
                                return time+0.01
                            end

                            return time+0.1
                        end, {player = player, weapon = weapon, mission = m}, timer.getTime()+0.1)
                    end
                end
            end
        end
    end

    function MissionTracker:tallyKill(player,kill)
        env.info("MissionTracker - tallyKill: "..player.." killed "..kill:getName())
        for _,m in pairs(self.activeMissions) do
            if m.players[player] then
                if m.state == Mission.states.active then
                    m:tallyKill(kill)
                end
            end
        end
    end

    function MissionTracker:tallySupplies(player, amount, zonename)
        env.info("MissionTracker - tallySupplies: "..player.." delivered "..amount.." of supplies to "..zonename)
        for _,m in pairs(self.activeMissions) do
            if m.players[player] then
                if m.state == Mission.states.active then
                    m:tallySupplies(amount, zonename)
                end
            end
        end
    end

    function MissionTracker:tallyLoadPilot(player, pilot)
        env.info("MissionTracker - tallyLoadPilot: "..player.." loaded pilot "..pilot.name)
        for _,m in pairs(self.activeMissions) do
            if m.players[player] then
                if m.state == Mission.states.active then
                    m:tallyLoadPilot(player, pilot)
                end
            end
        end
    end

    function MissionTracker:tallyUnloadPilot(player, zonename)
        env.info("MissionTracker - tallyUnloadPilot: "..player.." unloaded pilots at "..zonename)
        for _,m in pairs(self.activeMissions) do
            if m.players[player] then
                if m.state == Mission.states.active then
                    m:tallyUnloadPilot(player, zonename)
                end
            end
        end
    end

    function MissionTracker:tallyLoadSquad(player, squad)
        env.info("MissionTracker - tallyLoadSquad: "..player.." loaded squad "..squad.name)
        for _,m in pairs(self.activeMissions) do
            if m.players[player] then
                if m.state == Mission.states.active then
                    m:tallyLoadSquad(player, squad)
                end
            end
        end
    end

    function MissionTracker:tallyUnloadSquad(player, zonename, squadType)
        env.info("MissionTracker - tallyUnloadSquad: "..player.." unloaded "..squadType.." squad at "..zonename)
        for _,m in pairs(self.activeMissions) do
            if m.players[player] then
                if m.state == Mission.states.active then
                    m:tallyUnloadSquad(player, zonename, squadType)
                end
            end
        end
    end

    function MissionTracker:activateOrJoinMissionForGroup(code, groupname)
        if groupname then
            env.info('MissionTracker - activateOrJoinMissionForGroup: '..tostring(groupname)..' requested activate or join '..code)
            local gr = Group.getByName(groupname)
            for i,v in ipairs(gr:getUnits()) do
                if v.getPlayerName and v:getPlayerName() then 
                    local mis = self.activeMissions[code]
                    if mis then 
                        self:joinMission(code, v:getPlayerName(), v)
                    else
                        self:activateMission(code, v:getPlayerName(), v)
                    end
                    return
                end
            end
        end
    end

    function MissionTracker:activateMission(code, player, unit)
        if not unit or not unit:isExist() or not Utils.isLanded(unit, true) then 
            if unit and unit:isExist() then trigger.action.outTextForUnit(unit:getID(), 'Can only accept mission while landed', 5) end
            return false 
        end

        local zn = ZoneCommand.getZoneOfUnit(unit:getName())
        if not zn or zn.side ~= unit:getCoalition() then 
            trigger.action.outTextForUnit(unit:getID(), 'Can only accept mission while inside friendly zone', 5)
            return false 
        end

        for c,m in pairs(self.activeMissions) do
            if m:getPlayerUnit(player) then 
                trigger.action.outTextForUnit(unit:getID(), 'A mission is already active.', 5)
                return false 
            end
        end

        local mis = self.missionBoard[code]
        if not mis then 
            trigger.action.outTextForUnit(unit:getID(), 'Invalid mission code', 5)
            return false 
        end

        if mis.state ~= Mission.states.new then
            trigger.action.outTextForUnit(unit:getID(), 'Invalid mission.', 5)
            return false 
        end

        if not mis:isUnitTypeAllowed(unit) then
            trigger.action.outTextForUnit(unit:getID(), 'Current aircraft type is not compatible with this mission.', 5)
            return false
        end

        self.missionBoard[code] = nil
        
        trigger.action.outTextForCoalition(2,'Mission ['..mis.missionID..'] '..mis.name..' was accepted by '..player,5)
        mis:updateState(Mission.states.preping)
        mis.missionID = self:getNewMissionID()
        mis:addPlayer(player, unit)

        mis:pushMessageToPlayers(mis.name..' accepted.\nJoin code: ['..mis.missionID..']')

        env.info('Mission code'..code..' changed to code'..mis.missionID)
        env.info('Mission code'..mis.missionID..' accepted by '..player)
        self.activeMissions[mis.missionID] = mis
        return true
    end

    function MissionTracker:joinMission(code, player, unit)
        if not unit or not unit:isExist() or not Utils.isLanded(unit, true) then 
            if unit and unit:isExist() then trigger.action.outTextForUnit(unit:getID(), 'Can only join mission while landed', 5) end
            return false
        end

        local zn = ZoneCommand.getZoneOfUnit(unit:getName())
        if not zn or zn.side ~= unit:getCoalition() then 
            trigger.action.outTextForUnit(unit:getID(), 'Can only join mission while inside friendly zone', 5)
            return false
        end
       
        for c,m in pairs(self.activeMissions) do
            if m:getPlayerUnit(player) then 
                trigger.action.outTextForUnit(unit:getID(), 'A mission is already active.', 5)
                return false 
            end
        end

        local mis = self.activeMissions[code]
        if not mis then 
            trigger.action.outTextForUnit(unit:getID(), 'Invalid mission code', 5)
            return false 
        end

        if mis.state ~= Mission.states.preping then
            trigger.action.outTextForUnit(unit:getID(), 'Mission can only be joined if its members have not taken off yet.', 5)
            return false 
        end

        if not mis:isUnitTypeAllowed(unit) then
            trigger.action.outTextForUnit(unit:getID(), 'Current aircraft type is not compatible with this mission.', 5)
            return false
        end
        
        mis:addPlayer(player, unit)
        mis:pushMessageToPlayers(player..' has joined mission '..mis.name)
        env.info('Mission code'..code..' joined by '..player)
        return true
    end

    function MissionTracker:leaveMission(player)
        for _,mis in pairs(self.activeMissions) do
            if mis:getPlayerUnit(player) then
                mis:pushMessageToPlayers(player..' has left mission '..mis.name)
                mis:removePlayer(player)
                env.info('Mission code'..mis.missionID..' left by '..player)
                if not mis:hasPlayers() then
                    self.activeMissions[mis.missionID]:updateState(Mission.states.failed)
                    self.activeMissions[mis.missionID] = nil
                    env.info('Mission code'..mis.missionID..' canceled due to all players leaving')
                end

                break
            end
        end
        
        return true
    end

    function MissionTracker:canCreateMission(misType)
        if not MissionTracker.maxMissionCount[misType] then return false end
        
        local missionCount = 0
        for i,v in pairs(self.missionBoard) do
            if v.type == misType then missionCount = missionCount + 1 end
        end

        for i,v in pairs(self.activeMissions) do
            if v.type == misType then missionCount = missionCount + 1 end
        end

        if missionCount >= MissionTracker.maxMissionCount[misType] then return false end

        if misType == Mission.types.cap_easy then
            return CAP_Easy.canCreate()
        elseif misType == Mission.types.cap_medium then
            return CAP_Medium.canCreate()
        elseif misType == Mission.types.cas_easy then
            return CAS_Easy.canCreate()
        elseif misType == Mission.types.cas_medium then
            return CAS_Medium.canCreate()
        elseif misType == Mission.types.sead then
            return SEAD.canCreate()
        elseif misType == Mission.types.dead then
            return DEAD.canCreate()
        elseif misType == Mission.types.cas_hard then
            return CAS_Hard.canCreate()
        elseif misType == Mission.types.supply_easy then
            return Supply_Easy.canCreate()
        elseif misType == Mission.types.supply_hard then
            return Supply_Hard.canCreate()
        elseif misType == Mission.types.strike_veryeasy then
            return Strike_VeryEasy.canCreate()
        elseif misType == Mission.types.strike_easy then
            return Strike_Easy.canCreate()
        elseif misType == Mission.types.strike_medium then
            return Strike_Medium.canCreate()
        elseif misType == Mission.types.strike_hard then
            return Strike_Hard.canCreate()
        elseif misType == Mission.types.deep_strike then
            return Deep_Strike.canCreate()
        elseif misType == Mission.types.escort then
            return Escort.canCreate()
        elseif misType == Mission.types.tarcap then
            return TARCAP.canCreate(self.activeMissions)
        elseif misType == Mission.types.recon_plane then
            return Recon_Plane.canCreate()
        elseif misType == Mission.types.recon_plane_deep then
            return Deep_Recon_Plane.canCreate()
        elseif misType == Mission.types.scout_helo then
            return Scout_Helo.canCreate()
        elseif misType == Mission.types.bai then
            return BAI.canCreate()
        elseif misType == Mission.types.anti_runway then
            return Anti_Runway.canCreate()
        elseif misType == Mission.types.csar then
            return CSAR.canCreate()
        elseif misType == Mission.types.extraction then
            return Extraction.canCreate()
        elseif misType == Mission.types.deploy_squad then
            return DeploySquad.canCreate()
        end

        return false
    end

end


-----------------[[ END OF MissionTracker.lua ]]-----------------



-----------------[[ SquadTracker.lua ]]-----------------

SquadTracker = {}
do
	function SquadTracker:new()
		local obj = {}
		obj.activeInfantrySquads = {}
		setmetatable(obj, self)
		self.__index = self
		
		obj:start()
		return obj
	end

    SquadTracker.infantryCallsigns = {
        adjectives = {"Sapphire", "Emerald", "Whisper", "Vortex", "Blaze", "Nova", "Silent", "Zephyr", "Radiant", "Shadow", "Lively", "Dynamo", "Dusk", "Rapid", "Stellar", "Tundra", "Obsidian", "Cascade", "Zenith", "Solar"},
        nouns = {"Journey", "Quasar", "Galaxy", "Moonbeam", "Comet", "Starling", "Serenade", "Raven", "Breeze", "Echo", "Avalanche", "Harmony", "Stardust", "Horizon", "Firefly", "Solstice", "Labyrinth", "Whisper", "Cosmos", "Mystique"}
    }

    function SquadTracker:generateCallsign()
        local adjective = self.infantryCallsigns.adjectives[math.random(1,#self.infantryCallsigns.adjectives)]
        local noun = self.infantryCallsigns.nouns[math.random(1,#self.infantryCallsigns.nouns)]

        local callsign = adjective..noun

        if self.activeInfantrySquads[callsign] then
            for i=1,1000,1 do
                local try = callsign..'-'..i
                if not self.activeInfantrySquads[try] then
                    callsign = try
                    break
                end
            end
        end

        if not self.activeInfantrySquads[callsign] then
            return callsign
        end
    end

    function SquadTracker:restoreInfantry(save)

        Spawner.createObject(save.name, save.data.name, save.position, 2, 10, 20,{
            [land.SurfaceType.LAND] = true, 
            [land.SurfaceType.ROAD] = true,
            [land.SurfaceType.RUNWAY] = true,
        })

        self.activeInfantrySquads[save.name] = {
            name = save.name, 
            position = save.position, 
            state = save.state, 
            remainingStateTime=save.remainingStateTime, 
            data = save.data
        }

        if save.state == "extractReady" then
            MissionTargetRegistry.addSquad(self.activeInfantrySquads[save.name])
        end
        
        env.info('SquadTracker - '..save.name..'('..save.data.type..') restored')
    end

    function SquadTracker:spawnInfantry(infantryData, position)
        local callsign = self:generateCallsign()
        if callsign then
            Spawner.createObject(callsign, infantryData.name, position, 2, 10, 20,{
                [land.SurfaceType.LAND] = true, 
                [land.SurfaceType.ROAD] = true,
                [land.SurfaceType.RUNWAY] = true,
            })

            self:registerInfantry(infantryData, callsign, position)
        end
    end

    function SquadTracker:registerInfantry(infantryData, groupname, position)
        self.activeInfantrySquads[groupname] = {name = groupname, position = position, state = "deployed", remainingStateTime=0, data = infantryData}
        
        env.info('SquadTracker - '..groupname..'('..infantryData.type..') deployed')
    end
	
    function SquadTracker:start()
		if not ZoneCommand then return end

        timer.scheduleFunction(function(param, time)
			local self = param.context
			
			for i,v in pairs(self.activeInfantrySquads) do
                local remove = self:processInfantrySquad(v)
                if remove then
                    MissionTargetRegistry.removeSquad(v)
                    self.activeInfantrySquads[v.name] = nil
                end
			end
			
			return time+10
		end, {context = self}, timer.getTime()+1)
    end

    function SquadTracker:removeSquad(squadname)
        local squad = self.activeInfantrySquads[squadname]
        if squad then
            MissionTargetRegistry.removeSquad(squad)
            squad.state = 'extracted'
            squad.remainingStateTime = 0
            self.activeInfantrySquads[squadname] = nil
        end
    end

    function SquadTracker:getClosestExtractableSquad(sourcePoint)
        local minDist = 99999999
        local squad = nil

        for i,v in pairs(self.activeInfantrySquads) do
            if v.state == 'extractReady' then
                local gr = Group.getByName(v.name)
                if gr and gr:getSize()>0 then
                    local dist = mist.utils.get2DDist(sourcePoint, gr:getUnit(1):getPoint())
                    if dist<minDist then
                        minDist = dist
                        squad = v
                    end
                end
            end
        end

        if squad then
            return squad, minDist
        end
    end

    --[[
        infantry states:
            deployed - just spawned not processed yet
            working - started main activity, last until jobtime elapses
            extractReady - job completed waiting for extract, lasts until extracttime elapses
            mia - missing in action, extracttime elapsed without extraction, group is forever lost
            complete - mission complete no extraction necessary
            extracted - squad was loaded into a player helicopter
    ]] 
    function SquadTracker:processInfantrySquad(squad)
        local gr = Group.getByName(squad.name)
        if not gr then return true end
		if gr:getSize()==0 then 
			gr:destroy()
			return true
		end

        squad.remainingStateTime = squad.remainingStateTime - 10

        if squad.state == 'deployed' then
            env.info('SquadTracker - '..squad.name..'('..squad.data.type..') started working for '..squad.data.jobtime..' seconds')
            squad.state = 'working'
            squad.remainingStateTime = squad.data.jobtime
        elseif squad.state == 'working' then
            if squad.remainingStateTime <=0 then
                env.info('SquadTracker - '..squad.name..'('..squad.data.type..') job complete, waiting '..squad.data.extracttime..' seconds for extract')
                
                if squad.data.type == PlayerLogistics.infantryTypes.capture then
                    local zn = ZoneCommand.getZoneOfPoint(squad.position)
                    if zn and zn.side == 0 then
                        squad.state = "complete"
                        squad.remainingStateTime = 0
                        zn:capture(gr:getCoalition())
                        gr:destroy()
                        env.info('SquadTracker - '..squad.name..'('..squad.data.type..') no extraction required, deleting')
                        return true
                    else
                        env.info('SquadTracker - '..squad.name..'('..squad.data.type..') not in zone, cant capture')
                    end
                elseif squad.data.type == PlayerLogistics.infantryTypes.engineer then
                    local zn = ZoneCommand.getZoneOfPoint(squad.position)
                    if zn and zn.side == gr:getCoalition() then
                        zn:boostProduction(3000)
                        squad.state = "complete"
                        squad.remainingStateTime = 0
                        gr:destroy()
                        env.info('SquadTracker - '..squad.name..'('..squad.data.type..') no extraction required, deleting')
                        return true
                    else
                        env.info('SquadTracker - '..squad.name..'('..squad.data.type..') not in zone, cant boost')
                    end
                elseif squad.data.type == PlayerLogistics.infantryTypes.sabotage then
                    local zn = ZoneCommand.getZoneOfPoint(squad.position)
                    if zn and zn.side ~= gr:getCoalition() and zn.side ~= 0 then
                        zn:sabotage(1000, squad.position)
                        env.info('SquadTracker - '..squad.name..'('..squad.data.type..') sabotaged '..zn.name)
                    else
                        env.info('SquadTracker - '..squad.name..'('..squad.data.type..') not in zone, cant sabotage')
                    end
                elseif squad.data.type == PlayerLogistics.infantryTypes.spy then
                    local zn = ZoneCommand.getZoneOfPoint(squad.position)
                    if zn and zn.side ~= gr:getCoalition() and zn.side ~= 0 then
                        zn:reveal()

                        if zn.neighbours then
                            for _,v in pairs(zn.neighbours) do
                                if v.side ~= gr:getCoalition() and v.side ~= 0 then
                                    v:reveal()
                                end
                            end
                        end

                        env.info('SquadTracker - '..squad.name..'('..squad.data.type..') infiltrated into '..zn.name)
                    else
                        env.info('SquadTracker - '..squad.name..'('..squad.data.type..') not in zone, cant infiltrate')
                    end
                end

                squad.state = 'extractReady'
                squad.remainingStateTime = squad.data.extracttime
                MissionTargetRegistry.addSquad(squad)
			end
        elseif squad.state == 'extractReady' then
            if squad.remainingStateTime <= 0 then
                env.info('SquadTracker - '..squad.name..'('..squad.data.type..') extract time elapsed, group MIA')
                squad.state = 'mia'
                squad.remainingStateTime = 0
			    gr:destroy()
                MissionTargetRegistry.removeSquad(squad)
                return true
            end

            if not squad.lastMarkerDeployedTime then
                squad.lastMarkerDeployedTime = timer.getAbsTime() - (10*60)
            end

            if timer.getAbsTime() - squad.lastMarkerDeployedTime > (5*60) then
                if gr:getSize()>0 then
                    local unPos = gr:getUnit(1):getPoint()
                    local p = Utils.getPointOnSurface(unPos)
                    p.x = p.x + math.random(-5,5)
                    p.z = p.z + math.random(-5,5)
		            trigger.action.smoke(p, trigger.smokeColor.Green)
                    squad.lastMarkerDeployedTime = timer.getAbsTime()
                end
            end
        end
    end
end

-----------------[[ END OF SquadTracker.lua ]]-----------------



-----------------[[ CSARTracker.lua ]]-----------------

CSARTracker = {}
do
	function CSARTracker:new()
		local obj = {}
		obj.activePilots = {}
		setmetatable(obj, self)
		self.__index = self
		
		obj:start()
		return obj
	end

    function CSARTracker:start()
		if not ZoneCommand then return end

        local ev = {}
		ev.context = self
		function ev:onEvent(event)
			if event.id == world.event.S_EVENT_LANDING_AFTER_EJECTION then
                if event.initiator and event.initiator:isExist() then
                    if event.initiator:getCoalition() == 2 then
                        local z = ZoneCommand.getZoneOfPoint(event.initiator:getPoint())
                        if not z then
                            local name = self.context:generateCallsign()
                            if name then
                                local pos = {
                                    x = event.initiator:getPoint().x,
                                    y = event.initiator:getPoint().z
                                }

                                if pos.x ~= 0 and pos.y ~= 0 then
                                    local srfType = land.getSurfaceType(pos)
                                    if srfType ~= land.SurfaceType.WATER and srfType ~= land.SurfaceType.SHALLOW_WATER then
                                        local gr = Spawner.createPilot(name, pos)
                                        self.context:addPilot(name, gr)
                                    end
                                end
                            end
                        end
                    end

                    event.initiator:destroy()
                end
			end
		end
		
		world.addEventHandler(ev)

        timer.scheduleFunction(function(param, time)
            for i,v in pairs(param.context.activePilots) do
                v.remainingTime = v.remainingTime - 10
                if not v.pilot:isExist() or v.remainingTime <=0 then
                    param.context:removePilot(i)
                end
            end
			
			return time+10
		end, {context = self}, timer.getTime()+1)
    end

    function CSARTracker:markPilot(data)
        local pilot = data.pilot
        if pilot:isExist() then
            local pos = pilot:getUnit(1):getPoint()
            local p = Utils.getPointOnSurface(pos)
            p.x = p.x + math.random(-5,5)
            p.z = p.z + math.random(-5,5)
            trigger.action.smoke(p, trigger.smokeColor.Green)
        end
    end

    function CSARTracker:flarePilot(data)
        local pilot = data.pilot
        if pilot:isExist() then
            local pos = pilot:getUnit(1):getPoint()
            local p = Utils.getPointOnSurface(pos)
            trigger.action.signalFlare(p, trigger.flareColor.Green, math.random(1,360))
        end
    end

    function CSARTracker:removePilot(name)
        local data = self.activePilots[name]
        if data.pilot and data.pilot:isExist() then data.pilot:destroy() end

        MissionTargetRegistry.removePilot(data)
        self.activePilots[name] = nil
    end

    function CSARTracker:addPilot(name, pilot)
        self.activePilots[name] = {pilot = pilot, name = name, remainingTime = 45*60}
        MissionTargetRegistry.addPilot(self.activePilots[name])
    end

    function CSARTracker:restorePilot(save)         
        local gr = Spawner.createPilot(save.name, save.pos)
        
        self.activePilots[save.name] = {
            pilot = gr, 
            name = save.name, 
            remainingTime = save.remainingTime
        }
        
        MissionTargetRegistry.addPilot(self.activePilots[save.name])       
    end

    function CSARTracker:getClosestPilot(toPosition)
        local minDist = 99999999
        local data = nil
        local name = nil

        for i,v in pairs(self.activePilots) do
            if v.pilot:isExist() and v.remainingTime > 0 then
                local dist = mist.utils.get2DDist(toPosition, v.pilot:getUnit(1):getPoint())
                if dist<minDist then
                    minDist = dist
                    data = v
                end
            else
                self:removePilot(i)
            end
        end

        if data then
            return {name=data.name, pilot=data.pilot, remainingTime = data.remainingTime, dist=minDist}
        end
    end

    CSARTracker.pilotCallsigns = {
        adjectives = {"Agile", "Voyager", "Sleek", "Fierce", "Nimble", "Daring", "Swift", "Fearless", "Dynamic", "Rapid", "Brave", "Stealthy", "Eagle", "Thunder", "Roaring", "Jade", "Lion", "Crimson", "Mighty", "Phoenix"},
        nouns = {"Pancake", "Noodle", "Potato", "Banana", "Wombat", "Penguin", "Llama", "Cabbage", "Kangaroo", "Giraffe", "Walrus", "Pickle", "Donut", "Hamburger", "Toaster", "Teapot", "Unicorn", "Rainbow", "Dragon", "Sasquatch"}
    }

    function CSARTracker:generateCallsign()
        local adjective = self.pilotCallsigns.adjectives[math.random(1,#self.pilotCallsigns.adjectives)]
        local noun = self.pilotCallsigns.nouns[math.random(1,#self.pilotCallsigns.nouns)]

        local callsign = adjective..noun

        if self.activePilots[callsign] then
            for i=1,1000,1 do
                local try = callsign..'-'..i
                if not self.activePilots[try] then
                    callsign = try
                    break
                end
            end
        end

        if not self.activePilots[callsign] then
            return callsign
        end
    end
end

-----------------[[ END OF CSARTracker.lua ]]-----------------



-----------------[[ GCI.lua ]]-----------------

GCI = {}

do
    function GCI:new(side)
        local o = {}
        o.side = side
        o.tgtSide = 0
        if side == 1 then
            o.tgtSide = 2
        elseif side == 2 then
            o.tgtSide = 1
        end

        o.radars = {}
        o.players = {}
        o.radarTypes = {
            'SAM SR',
            'EWR',
            'AWACS'
        }

        o.groupMenus = {}

        setmetatable(o, self)
		self.__index = self

        o:start()

		return o
    end

    function GCI:registerPlayer(name, unit, warningRadius, metric)
        if warningRadius > 0 then
            local msg = "Warning radius set to "..warningRadius
            if metric then
                msg=msg.."km" 
            else
                msg=msg.."nm"
            end
            
            if metric then
                warningRadius = warningRadius * 1000
            else
                warningRadius = warningRadius * 1852
            end
            
            self.players[name] = {
                unit = unit, 
                warningRadius = warningRadius,
                metric = metric
            }
            
            trigger.action.outTextForUnit(unit:getID(), msg, 10)
        else
            self.players[name] = nil
            trigger.action.outTextForUnit(unit:getID(), "GCI Reports disabled", 10)
        end
    end

    function GCI:start()
        MenuRegistry:register(5, function(event, context)
			if event.id == world.event.S_EVENT_BIRTH and event.initiator and event.initiator.getPlayerName then
				local player = event.initiator:getPlayerName()
				if player then
					local groupid = event.initiator:getGroup():getID()
                    local groupname = event.initiator:getGroup():getName()
                    local unit = event.initiator
					
                    if context.groupMenus[groupid] then
                        missionCommands.removeItemForGroup(groupid, context.groupMenus[groupid])
                        context.groupMenus[groupid] = nil
                    end

                    if not context.groupMenus[groupid] then
                        
                        local menu = missionCommands.addSubMenuForGroup(groupid, 'GCI')
                        local setWR = missionCommands.addSubMenuForGroup(groupid, 'Set Warning Radius', menu)
                        local kmMenu = missionCommands.addSubMenuForGroup(groupid, 'KM', setWR)
                        local nmMenu = missionCommands.addSubMenuForGroup(groupid, 'NM', setWR)

                        missionCommands.addCommandForGroup(groupid, '10 KM',  kmMenu, Utils.log(context.registerPlayer), context, player, unit, 10, true)
                        missionCommands.addCommandForGroup(groupid, '25 KM',  kmMenu, Utils.log(context.registerPlayer), context, player, unit, 25, true)
                        missionCommands.addCommandForGroup(groupid, '50 KM',  kmMenu, Utils.log(context.registerPlayer), context, player, unit, 50, true)
                        missionCommands.addCommandForGroup(groupid, '100 KM', kmMenu, Utils.log(context.registerPlayer), context, player, unit, 100, true)
                        missionCommands.addCommandForGroup(groupid, '150 KM', kmMenu, Utils.log(context.registerPlayer), context, player, unit, 150, true)

                        missionCommands.addCommandForGroup(groupid, '5 NM',  nmMenu, Utils.log(context.registerPlayer), context, player, unit, 5, false)
                        missionCommands.addCommandForGroup(groupid, '10 NM', nmMenu, Utils.log(context.registerPlayer), context, player, unit, 10, false)
                        missionCommands.addCommandForGroup(groupid, '25 NM', nmMenu, Utils.log(context.registerPlayer), context, player, unit, 25, false)
                        missionCommands.addCommandForGroup(groupid, '50 NM', nmMenu, Utils.log(context.registerPlayer), context, player, unit, 50, false)
                        missionCommands.addCommandForGroup(groupid, '80 NM', nmMenu, Utils.log(context.registerPlayer), context, player, unit, 80, false)
                        missionCommands.addCommandForGroup(groupid, 'Disable', menu, Utils.log(context.registerPlayer), context, player, unit, 0, false)

                        context.groupMenus[groupid] = menu
                    end
				end
            elseif (event.id == world.event.S_EVENT_PLAYER_LEAVE_UNIT or event.id == world.event.S_EVENT_DEAD) and event.initiator and event.initiator.getPlayerName then
                local player = event.initiator:getPlayerName()
				if player then
					local groupid = event.initiator:getGroup():getID()
					
                    if context.groupMenus[groupid] then
                        missionCommands.removeItemForGroup(groupid, context.groupMenus[groupid])
                        context.groupMenus[groupid] = nil
                    end
				end
            end
		end, self)

        timer.scheduleFunction(function(param, time)
            local self = param.context
            local allunits = coalition.getGroups(self.side)
  
            local radars = {}
            for _,g in ipairs(allunits) do
                for _,u in ipairs(g:getUnits()) do
                    for _,a in ipairs(self.radarTypes) do
                        if u:hasAttribute(a) then
                            table.insert(radars, u)
                            break
                        end
                    end
                end
            end

            self.radars = radars
            env.info("GCI - tracking "..#radars.." radar enabled units")

            return time+10
        end, {context = self}, timer.getTime()+1)

        timer.scheduleFunction(function(param, time)
            local self = param.context

            local plyCount = 0
            for i,v in pairs(self.players) do
                if not v.unit or not v.unit:isExist() then
                    self.players[i] = nil
                else
                    plyCount = plyCount + 1
                end
            end

            env.info("GCI - reporting to "..plyCount.." players")
            if plyCount >0 then
                local dect = {}
                local dcount = 0
                for _,u in ipairs(self.radars) do
                    if u:isExist() then
                        local detected = u:getController():getDetectedTargets(Controller.Detection.RADAR)
                        for _,d in ipairs(detected) do
                            if d and d.object and d.object.isExist and d.object:isExist() and 
                                d.object:getCategory() == Object.Category.UNIT and
                                d.object.getCoalition and
                                d.object:getCoalition() == self.tgtSide then
                                    
                                if not dect[d.object:getName()] then
                                    dect[d.object:getName()] = d.object
                                    dcount = dcount + 1
                                end
                            end
                        end
                    end
                end
                
                env.info("GCI - aware of "..dcount.." enemy units")

                for name, data in pairs(self.players) do
                    if data.unit and data.unit:isExist() then
                        local closeUnits = {}

                        local wr = data.warningRadius
                        if wr > 0 then
                            for _,dt in pairs(dect) do
                                if dt:isExist() then
                                    local tgtPnt = dt:getPoint()
                                    local dist = mist.utils.get2DDist(data.unit:getPoint(), tgtPnt)
                                    if dist <= wr then
                                        local brg = math.floor(Utils.getBearing(data.unit:getPoint(), tgtPnt))

                                        local myPos = data.unit:getPosition()
                                        local tgtPos = dt:getPosition()
                                        local tgtHeading = math.deg(math.atan2(tgtPos.x.z, tgtPos.x.x))
                                        local tgtBearing = Utils.getBearing(tgtPos.p, myPos.p)
            
                                        local diff = math.abs(Utils.getHeadingDiff(tgtBearing, tgtHeading))
                                        local aspect = ''
                                        local priority = 1
                                        if diff <= 30 then
                                            aspect = "Hot"
                                            priority = 1
                                        elseif diff <= 60 then
                                            aspect = "Flanking"
                                            priority = 1
                                        elseif diff <= 120 then
                                            aspect = "Beaming"
                                            priority = 2
                                        else
                                            aspect = "Cold"
                                            priority = 3
                                        end

                                        table.insert(closeUnits, {
                                            type = dt:getDesc().typeName,
                                            bearing = brg,
                                            range = dist,
                                            altitude = tgtPnt.y,
                                            score = dist*priority,
                                            aspect = aspect
                                        })
                                    end
                                end
                            end
                        end

                        env.info("GCI - "..#closeUnits.." enemy units within "..wr.."m of "..name)
                        if #closeUnits > 0 then
                            table.sort(closeUnits, function(a, b) return a.range < b.range end)

                            local msg = "GCI Report:\n"
                            local count = 0
                            for _,tgt in ipairs(closeUnits) do
                                if data.metric then
                                    local km = tgt.range/1000
                                    if km < 1 then
                                        msg = msg..'\n'..tgt.type..'  MERGED'
                                    else
                                        msg = msg..'\n'..tgt.type..'  BRA: '..tgt.bearing..' for '
                                        msg = msg..Utils.round(km)..'km at '
                                        msg = msg..(Utils.round(tgt.altitude/250)*250)..'m, '
                                        msg = msg..tostring(tgt.aspect)
                                    end
                                else
                                    local nm = tgt.range/1852
                                    if nm < 1 then
                                        msg = msg..'\n'..tgt.type..'  MERGED'
                                    else
                                        msg = msg..'\n'..tgt.type..'  BRA: '..tgt.bearing..' for '
                                        msg = msg..Utils.round(nm)..'nm at '
                                        msg = msg..(Utils.round((tgt.altitude/0.3048)/1000)*1000)..'ft, '
                                        msg = msg..tostring(tgt.aspect)
                                    end
                                end
                                
                                count = count + 1
                                if count >= 10 then break end
                            end

                            trigger.action.outTextForUnit(data.unit:getID(), msg, 19)
                        end
                    else
                        self.players[name] = nil
                    end
                end
            end

            return time+20
        end, {context = self}, timer.getTime()+6)
    end
end

-----------------[[ END OF GCI.lua ]]-----------------



-----------------[[ Starter.lua ]]-----------------

Starter = {}
do
    Starter.neutralChance = 0.1

    function Starter.start(zones)
        if Starter.shouldRandomize() then
            Starter.randomize(zones)
        else
            Starter.normalStart(zones)
        end
    end

    function Starter.randomize(zones)
        local startZones = {}
        for _,z in pairs(zones) do
            if z.isHeloSpawn and z.isPlaneSpawn then
                table.insert(startZones, z)
            end
        end

        if #startZones > 0 then
            local sz = startZones[math.random(1,#startZones)]

            sz:capture(2, true)
            Starter.captureNeighbours(sz, math.random(1,3))
        end

        for _,z in pairs(zones) do
            if z.side == 0 then 
                if math.random() > Starter.neutralChance then
                    z:capture(1,true)
                end
            end

            if z.side ~= 0 then
                z:fullUpgrade(math.random(1,30)/100)
            end
        end
    end

    function Starter.captureNeighbours(zone, stepsLeft)
        if stepsLeft > 0 then
            for _,v in pairs(zone.neighbours) do
                if v.side == 0 then
                    if math.random() > Starter.neutralChance then
                        v:capture(2,true)
                    end
                    Starter.captureNeighbours(v, stepsLeft-1)
                end
            end
        end
    end

    function Starter.shouldRandomize()
        if lfs then
            local filename = lfs.writedir()..'Missions/Saves/randomize.lua'
            if lfs.attributes(filename) then
                return true
            end
		end
    end

    function Starter.normalStart(zones)
        for _,z in pairs(zones) do
            local i = z.initialState
            if i then
                if i.side and i.side ~= 0 then
                    z:capture(i.side, true)
                    z:fullUpgrade()
                    z:boostProduction(math.random(1,200))
                end
            end
        end
    end
end

-----------------[[ END OF Starter.lua ]]-----------------

