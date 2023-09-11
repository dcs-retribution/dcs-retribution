
ZoneCommand.setNeighbours(cm)

bm = BattlefieldManager:new()

mc = MarkerCommands:new()

pt = PlayerTracker:new(mc)

mt = MissionTracker:new(pt, mc)

st = SquadTracker:new()

ct = CSARTracker:new()

pl = PlayerLogistics:new(mt, pt, st, ct)

gci = GCI:new(2)

gm = GroupMonitor:new(cm)
ZoneCommand.groupMonitor = gm

-- PlayerLogistics:registerSquadGroup(squadType,              groupname,      weight,cost,jobtime,extracttime, squadSize)
pl:registerSquadGroup(PlayerLogistics.infantryTypes.capture,  'capture-squad',  700, 200, 60,    60*30, 4)
pl:registerSquadGroup(PlayerLogistics.infantryTypes.sabotage, 'sabotage-squad', 800, 500, 60*5,  60*30, 4)
pl:registerSquadGroup(PlayerLogistics.infantryTypes.ambush,   'ambush-squad',   900, 300, 60*20, 60*30, 5)
pl:registerSquadGroup(PlayerLogistics.infantryTypes.engineer, 'engineer-squad', 200, 1000,60,    60*30, 2)
pl:registerSquadGroup(PlayerLogistics.infantryTypes.manpads,  'manpads-squad',  900, 500, 60*20, 60*30, 5)
pl:registerSquadGroup(PlayerLogistics.infantryTypes.spy,      'spy-squad',      100, 300, 60*10, 60*30, 1)
pl:registerSquadGroup(PlayerLogistics.infantryTypes.rapier,   'rapier-squad',   1200,2000,60*60, 60*30, 8)

Group.getByName('jtacDrone'):destroy()
CommandFunctions.jtac = JTAC:new({name = 'jtacDrone'})

pm = PersistenceManager:new(savefile, gm, st, ct, pl)
pm:load()

if pm:canRestore() then
	pm:restoreZones()
	pm:restoreAIMissions()
	pm:restoreBattlefield()
	pm:restoreCsar()
	pm:restoreSquads()
else
	--initial states
	Starter.start(zones)
end

timer.scheduleFunction(function(param, time)
	pm:save()
	env.info("Mission state saved")
	return time+60
end, zones, timer.getTime()+60)


--make sure support units are present where needed
ensureSpawn = {
	['golf-farp-suport'] = zones.golf,
	['november-farp-suport'] = zones.november,
	['tango-farp-suport'] = zones.tango,
	['sierra-farp-suport'] = zones.sierra,
	['cherkessk-farp-suport'] = zones.cherkessk,
	['unal-farp-suport'] = zones.unal,
	['tyrnyauz-farp-suport'] = zones.tyrnyauz
}

for grname, zn in pairs(ensureSpawn) do
	local g = Group.getByName(grname)
	if g then g:destroy() end
end

timer.scheduleFunction(function(param, time)
	
	for grname, zn in pairs(ensureSpawn) do
		local g = Group.getByName(grname)
		if zn.side == 2 then
			if not g then
				local err, msg = pcall(mist.respawnGroup,grname,true)
				if not err then
					env.info("ERROR spawning "..grname)
					env.info(msg)
				end
			end
		else
			if g then g:destroy() end
		end
	end

	return time+30
end, {}, timer.getTime()+30)


--supply injection
local blueSupply = {'offmap-supply-blue-1','offmap-supply-blue-2','offmap-supply-blue-3','offmap-supply-blue-4','offmap-supply-blue-5'}
local redSupply = {'offmap-supply-red-1','offmap-supply-red-2','offmap-supply-red-3','offmap-supply-red-4','offmap-supply-red-5'}
local offmapZones = {
	zones.batumi, 
	zones.sochi,
	zones.nalchik, 
	zones.beslan,
	zones.mozdok,
	zones.mineralnye,
--  zones.senaki,
--	zones.sukhumi,
--	zones.gudauta,
--	zones.kobuleti,
}

