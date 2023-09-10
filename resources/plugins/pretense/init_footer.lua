supplyPointRegistry = {
	blue = {},
	red = {}
}

for i,v in ipairs(blueSupply) do
	local g = Group.getByName(v)
	if g then 
		supplyPointRegistry.blue[v] = g:getUnit(1):getPoint()
	end
end

for i,v in ipairs(redSupply) do
	local g = Group.getByName(v)
	if g then 
		supplyPointRegistry.red[v] = g:getUnit(1):getPoint()
	end
end

offmapSupplyRegistry = {}
timer.scheduleFunction(function(param, time)
	local availableBlue = {}
	for i,v in ipairs(param.blue) do
		if offmapSupplyRegistry[v] == nil then
			table.insert(availableBlue, v)
		end
	end

	local availableRed = {}
	for i,v in ipairs(param.red) do
		if offmapSupplyRegistry[v] == nil then
			table.insert(availableRed, v)
		end
	end
 
	local redtargets = {}
	local bluetargets = {}
	for _, zn in ipairs(param.offmapZones) do
		if zn:needsSupplies(3000) then
			local isOnRoute = false
			for _,data in pairs(offmapSupplyRegistry) do
				if data.zone.name == zn.name then
					isOnRoute = true
					break
				end
			end
			if not isOnRoute then
				if zn.side == 1 then
					table.insert(redtargets, zn)
				elseif zn.side == 2 then
					table.insert(bluetargets, zn)
				end
			end
		end
	end

	if #availableRed > 0 and #redtargets > 0 then
		local zn = redtargets[math.random(1,#redtargets)]

		local red = nil
		local minD = 999999999
		for i,v in ipairs(availableRed) do
			local d = mist.utils.get2DDist(zn.zone.point, supplyPointRegistry.red[v])
			if d < minD then
				red = v
				minD = d
			end
		end

		if not red then red = availableRed[math.random(1,#availableRed)] end

		local gr = red
		red = nil
		mist.respawnGroup(gr, true)
		offmapSupplyRegistry[gr] = {zone = zn, assigned = timer.getAbsTime()}
		env.info(gr..' was deployed')
		timer.scheduleFunction(function(param,time)
			local g = Group.getByName(param.group)
			TaskExtensions.landAtAirfield(g, param.target.zone.point)
			env.info(param.group..' going to '..param.target.name)
		end, {group=gr, target=zn}, timer.getTime()+2)
	end
	
	if #availableBlue > 0 and #bluetargets>0 then
		local zn = bluetargets[math.random(1,#bluetargets)]

		local blue = nil
		local minD = 999999999
		for i,v in ipairs(availableBlue) do
			local d = mist.utils.get2DDist(zn.zone.point, supplyPointRegistry.blue[v])
			if d < minD then
				blue = v
				minD = d
			end
		end

		if not blue then blue = availableBlue[math.random(1,#availableBlue)] end

		local gr = blue
		blue = nil
		mist.respawnGroup(gr, true)
		offmapSupplyRegistry[gr] = {zone = zn, assigned = timer.getAbsTime()}
		env.info(gr..' was deployed')
		timer.scheduleFunction(function(param,time)
			local g = Group.getByName(param.group)
			TaskExtensions.landAtAirfield(g, param.target.zone.point)
			env.info(param.group..' going to '..param.target.name)
		end, {group=gr, target=zn}, timer.getTime()+2)
	end

	return time+(60*5)
end, {blue = blueSupply, red = redSupply, offmapZones = offmapZones}, timer.getTime()+60)



timer.scheduleFunction(function(param, time)
	
	for groupname,data in pairs(offmapSupplyRegistry) do
		local gr = Group.getByName(groupname)
		if not gr then 
			offmapSupplyRegistry[groupname] = nil
			env.info(groupname..' was destroyed')
		end
	
		if gr and ((timer.getAbsTime() - data.assigned) > (60*60)) then
			gr:destroy()
			offmapSupplyRegistry[groupname] = nil
			env.info(groupname..' despawned due to being alive for too long')
		end
		
		if gr and Utils.allGroupIsLanded(gr) and Utils.someOfGroupInZone(gr, data.zone.name) then 
			data.zone:addResource(15000)
			gr:destroy()
			offmapSupplyRegistry[groupname] = nil
			env.info(groupname..' landed at '..data.zone.name..' and delivered 15000 resources')
		end
	end

	return time+180
end, {}, timer.getTime()+180)