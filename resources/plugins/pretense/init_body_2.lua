
end

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
