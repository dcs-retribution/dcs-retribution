

local savefile = 'pretense_1.1.json'
if lfs then 
	local dir = lfs.writedir()..'Missions/Saves/'
	lfs.mkdir(dir)
	savefile = dir..savefile
	env.info('Pretense - Save file path: '..savefile)
end


do
	TemplateDB.templates["infantry-red"] = {
		units = {
			"BTR_D",
			"T-90",
			"T-90",
			"Infantry AK ver2",
			"Infantry AK",
			"Infantry AK",
			"Paratrooper RPG-16",
			"Infantry AK ver3",
			"SA-18 Igla manpad"
		},
		skill = "Excellent",
		dataCategory= TemplateDB.type.group
	}

	TemplateDB.templates["infantry-blue"] = {
		units = { 
			"M1045 HMMWV TOW",
			"Soldier stinger",
			"Soldier M4 GRG",
			"Soldier M4 GRG",
			"Soldier M4 GRG",
			"Soldier M4 GRG",
			"Soldier M4 GRG",
			"M1043 HMMWV Armament"
		},
		skill = "Excellent",
		dataCategory= TemplateDB.type.group
	}

	TemplateDB.templates["defense-red"] = {
		units = {
			"Infantry AK ver2",
			"Infantry AK",
			"Infantry AK ver3",
			"Paratrooper RPG-16",
			"SA-18 Igla manpad"
		},
		skill = "Excellent",
		dataCategory= TemplateDB.type.group
	}

	TemplateDB.templates["defense-blue"] = {
		units = { 
			"Soldier M4 GRG",
			"Soldier M4 GRG",
			"Soldier M4 GRG",
			"Soldier RPG",
			"Soldier stinger",
		},
		skill = "Excellent",
		dataCategory= TemplateDB.type.group
	}

	TemplateDB.templates["shorad-red"] = {
		units = {
			"Strela-10M3",
			"Strela-10M3",
			"Ural-4320T",
			"2S6 Tunguska"
		},
		maxDist = 300,
		skill = "Excellent",
		dataCategory= TemplateDB.type.group
	}

	TemplateDB.templates["shorad-blue"] = {
		units = {
			"Roland ADS",
			"M48 Chaparral",
			"M 818",
			"Gepard",
			"Gepard"
		},
		maxDist = 300,
		skill = "Excellent",
		dataCategory= TemplateDB.type.group
	}

	TemplateDB.templates["sam-red"] = {
		units = {
			"p-19 s-125 sr",
			"Ural-4320T",
			"Ural-4320T",
			"S_75M_Volhov",
			"S_75M_Volhov",
			"S_75M_Volhov",
			"S_75M_Volhov",
			"S_75M_Volhov",
			"Tor 9A331",
			"SNR_75V"
		},
		maxDist = 300,
		skill = "Excellent",
		dataCategory= TemplateDB.type.group
	}

	TemplateDB.templates["sam-blue"] = {
		units = {
			"Hawk pcp",
			"Hawk cwar",
			"Hawk ln",
			"Hawk ln",
			"Hawk ln",
			"Hawk ln",
			"Hawk ln",
			"Hawk tr",
			"M 818",
			"Hawk sr"
		},
		maxDist = 300,
		skill = "Good",
		dataCategory= TemplateDB.type.group
	}

	TemplateDB.templates["patriot"] = {
		units = {
			"Patriot cp",
			"Patriot str",
			"M 818",
			"M 818",
			"Patriot ln",
			"Patriot ln",
			"Patriot ln",
			"Patriot ln",
			"Patriot str",
			"Patriot str",
			"Patriot str",
			"Patriot EPP",
			"Patriot ECS",
			"Patriot AMG"
		},
		maxDist = 300,
		skill = "Good",
		dataCategory= TemplateDB.type.group
	}

	TemplateDB.templates["sa3"] = {
		units = {
			"p-19 s-125 sr",
			"snr s-125 tr",
			"5p73 s-125 ln",
			"5p73 s-125 ln",
			"Ural-4320T",
			"5p73 s-125 ln",
			"5p73 s-125 ln"
		},
		maxDist = 300,
		skill = "Excellent",
		dataCategory= TemplateDB.type.group
	}

	TemplateDB.templates["sa6"] = {
		units = {
			"Kub 1S91 str",
			"Kub 2P25 ln",
			"Kub 2P25 ln",
			"Kub 2P25 ln",
			"Kub 2P25 ln",
			"2S6 Tunguska",
			"Ural-4320T",
			"2S6 Tunguska",
			"Kub 2P25 ln"
		},
		maxDist = 300,
		skill = "Excellent",
		dataCategory= TemplateDB.type.group
	}

	TemplateDB.templates["sa10"] = {
		units = {
			"S-300PS 54K6 cp",
			"S-300PS 5P85C ln",
			"S-300PS 5P85C ln",
			"S-300PS 5P85C ln",
			"GAZ-66",
			"GAZ-66",
			"GAZ-66",
			"S-300PS 5P85C ln",
			"S-300PS 5P85C ln",
			"S-300PS 5P85C ln",
			"S-300PS 40B6MD sr",
			"S-300PS 40B6M tr",
			"S-300PS 64H6E sr"
		},
		maxDist = 300,
		skill = "Excellent",
		dataCategory= TemplateDB.type.group
	}

	TemplateDB.templates["sa5"] = {
		units = {
			"RLS_19J6",
			"Ural-4320T",
			"Ural-4320T",
			"RPC_5N62V",
			"S-200_Launcher",
			"S-200_Launcher",
			"S-200_Launcher",
			"S-200_Launcher",
			"S-200_Launcher",
			"S-200_Launcher"
		},
		maxDist = 300,
		skill = "Excellent",
		dataCategory= TemplateDB.type.group
	}

	TemplateDB.templates["sa11"] = {
		units = {
			"SA-11 Buk SR 9S18M1",
			"SA-11 Buk LN 9A310M1",
			"SA-11 Buk LN 9A310M1",
			"SA-11 Buk LN 9A310M1",
			"SA-11 Buk LN 9A310M1",
			"SA-11 Buk LN 9A310M1",
			"2S6 Tunguska",
			"SA-11 Buk SR 9S18M1",
			"GAZ-66",
			"GAZ-66",
			"SA-11 Buk CC 9S470M1"
		},
		maxDist = 300,
		skill = "Excellent",
		dataCategory= TemplateDB.type.group
	}

	TemplateDB.templates["nasams"] = {
		units = {
			"NASAMS_Command_Post",
			"NASAMS_Radar_MPQ64F1",
			"Vulcan",
			"M 818",
			"M 818",
			"Roland ADS",
			"Roland ADS",
			"NASAMS_LN_C",
			"NASAMS_LN_C",
			"NASAMS_LN_C",
			"NASAMS_LN_C",
			"NASAMS_Radar_MPQ64F1",
			"NASAMS_Radar_MPQ64F1",
			"NASAMS_Radar_MPQ64F1"
		},
		maxDist = 300,
		skill = "Excellent",
		dataCategory= TemplateDB.type.group
	}
end

presets = {
	upgrades = {
		basic = {
			tent = Preset:new({
				display = 'Tent',
				cost = 1500,
				type = 'upgrade',
				template = "tent"
			}),
			comPost = Preset:new({
				display = 'Barracks',
				cost = 1500,
				type = 'upgrade',
				template = "barracks"
			}),
			outpost = Preset:new({
				display = 'Outpost',
				cost = 1500,
				type = 'upgrade',
				template = "outpost"
			})
		},
		attack = {
			ammoCache = Preset:new({
				display = 'Ammo Cache',
				cost = 1500,
				type = 'upgrade',
				template = "ammo-cache"
			}),
			ammoDepot = Preset:new({
				display = 'Ammo Depot',
				cost = 2000,
				type = 'upgrade',
				template = "ammo-depot"
			})
		},
		supply = {
			fuelCache = Preset:new({
				display = 'Fuel Cache',
				cost = 1500,
				type = 'upgrade',
				template = "fuel-cache"
			}),
			fuelTank = Preset:new({
				display = 'Fuel Tank',
				cost = 1500,
				type = 'upgrade',
				template = "fuel-tank-big"
			}),
			fuelTankFarp = Preset:new({
				display = 'Fuel Tank',
				cost = 1500,
				type = 'upgrade',
				template = "fuel-tank-small"
			}),
			factory1 = Preset:new({
				display='Factory',
				cost = 2000,
				type ='upgrade',
				income = 20,
				template = "factory-1"
			}),
			factory2 = Preset:new({
				display='Factory',
				cost = 2000,
				type ='upgrade',
				income = 20,
				template = "factory-2"
			}),
			factoryTank = Preset:new({
				display='Storage Tank',
				cost = 1500,
				type ='upgrade',
				income = 10,
				template = "chem-tank"
			}),
			ammoDepot = Preset:new({
				display = 'Ammo Depot',
				cost = 2000,
				type = 'upgrade',
				income = 40,
				template = "ammo-depot"
			}),
			oilPump = Preset:new({
				display = 'Oil Pump',
				cost = 1500,
				type = 'upgrade',
				income = 20,
				template = "oil-pump"
			}),
			hangar = Preset:new({
				display = 'Hangar',
				cost = 2000,
				type = 'upgrade',
				income = 30,
				template = "hangar"
			}),
			excavator = Preset:new({
				display = 'Excavator',
				cost = 2000,
				type = 'upgrade',
				income = 20,
				template = "excavator"
			}),
			farm1 = Preset:new({
				display = 'Farm House',
				cost = 2000,
				type = 'upgrade',
				income = 40,
				template = "farm-house-1"
			}),
			farm2 = Preset:new({
				display = 'Farm House',
				cost = 2000,
				type = 'upgrade',
				income = 40,
				template = "farm-house-2"
			}),
			refinery1 = Preset:new({
				display='Refinery',
				cost = 2000,
				type ='upgrade',
				income = 100,
				template = "factory-1"
			}),
			powerplant1 = Preset:new({
				display='Power Plant',
				cost = 1500,
				type ='upgrade',
				income = 25,
				template = "factory-1"
			}),
			powerplant2 = Preset:new({
				display='Power Plant',
				cost = 1500,
				type ='upgrade',
				income = 25,
				template = "factory-2"
			}),
			antenna = Preset:new({
				display='Antenna',
				cost = 1000,
				type ='upgrade',
				income = 10,
				template = "antenna"
			}),
			hq = Preset:new({
				display='HQ Building',
				cost = 2000,
				type ='upgrade',
				income = 50,
				template = "tv-tower"
			})
		},
		airdef = {
			comCenter = Preset:new({
				display = 'Command Center',
				cost = 2500,
				type = 'upgrade',
				template = "command-center"
			})
		}
	},
	defenses = {
		red = {
			infantry = Preset:new({
				display = 'Infantry', 
				cost=2000, 
				type='defense', 
				template='infantry-red',
			}),
			shorad = Preset:new({
				display = 'SAM', 
				cost=2500, 
				type='defense', 
				template='shorad-red',
			}),
			sam = Preset:new({
				display = 'SAM', 
				cost=3000, 
				type='defense', 
				template='sam-red',
			}),
			sa10 = Preset:new({
				display = 'SAM', 
				cost=3000, 
				type='defense', 
				template='sa10',
			}),
			sa5 = Preset:new({
				display = 'SAM', 
				cost=3000, 
				type='defense', 
				template='sa5',
			}),
			sa3 = Preset:new({
				display = 'SAM', 
				cost=3000, 
				type='defense', 
				template='sa3',
			}),
			sa6 = Preset:new({
				display = 'SAM', 
				cost=3000, 
				type='defense', 
				template='sa6',
			}),
			sa11 = Preset:new({
				display = 'SAM', 
				cost=3000, 
				type='defense', 
				template='sa11',
			})
		},
		blue = {
			infantry = Preset:new({
				display = 'Infantry', 
				cost=2000, 
				type='defense', 
				template='infantry-blue',
			}),
			shorad = Preset:new({
				display = 'SAM', 
				cost=2500, 
				type='defense', 
				template='shorad-blue',
			}),
			sam = Preset:new({
				display = 'SAM', 
				cost=3000, 
				type='defense', 
				template='sam-blue',
			}),
			patriot = Preset:new({
				display = 'SAM', 
				cost=3000, 
				type='defense', 
				template='patriot',
			}),
			nasams = Preset:new({
				display = 'SAM', 
				cost=3000, 
				type='defense', 
				template='nasams',
			})
		}
	},
	missions = {
		supply = {
			convoy = Preset:new({
				display = 'Supply convoy',
				cost = 4000,
				type = 'mission',
				missionType = ZoneCommand.missionTypes.supply_convoy
			}),
			convoy_escorted = Preset:new({
				display = 'Supply convoy',
				cost = 3000,
				type = 'mission',
				missionType = ZoneCommand.missionTypes.supply_convoy
			}),
			helo = Preset:new({
				display = 'Supply helicopter',
				cost = 2500,
				type='mission',
				missionType = ZoneCommand.missionTypes.supply_air
			}),
			transfer = Preset:new({
				display = 'Supply transfer',
				cost = 1000,
				type='mission',
				missionType = ZoneCommand.missionTypes.supply_transfer
			})
		},
		attack = {
			surface = Preset:new({
				display = 'Ground assault',
				cost = 100,
				type = 'mission',
				missionType = ZoneCommand.missionTypes.assault,
			}),
			cas = Preset:new({
				display = 'CAS',
				cost = 200,
				type='mission',
				missionType = ZoneCommand.missionTypes.cas
			}),
			bai = Preset:new({
				display = 'BAI',
				cost = 200,
				type='mission',
				missionType = ZoneCommand.missionTypes.bai
			}),
			strike = Preset:new({
				display = 'Strike',
				cost = 300,
				type='mission',
				missionType = ZoneCommand.missionTypes.strike
			}),
			sead = Preset:new({
				display = 'SEAD',
				cost = 200,
				type='mission',
				missionType = ZoneCommand.missionTypes.sead
			}),
			helo = Preset:new({
				display = 'CAS',
				cost = 100,
				type='mission',
				missionType = ZoneCommand.missionTypes.cas_helo
			})
		},
		patrol={
			aircraft = Preset:new({
				display= "Patrol",
				cost = 100,
				type='mission',
				missionType = ZoneCommand.missionTypes.patrol
			})
		},
		support ={
			awacs = Preset:new({
				display= "AWACS",
				cost = 300,
				type='mission',
				bias='5',
				missionType = ZoneCommand.missionTypes.awacs
			}),
			tanker = Preset:new({
				display= "Tanker",
				cost = 200,
				type='mission',
				bias='2',
				missionType = ZoneCommand.missionTypes.tanker
			})
		}
	},
	special = {
		red = {
			infantry = Preset:new({
				display = 'Infantry', 
				cost=-1, 
				type='defense', 
				template='defense-red',
			}),
		},
		blue = {
			infantry = Preset:new({
				display = 'Infantry', 
				cost=-1, 
				type='defense', 
				template='defense-blue',
			})
		}
	}
}

zones = {}
do
	
	

-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Batumi.lua ]]-----------------

zones.batumi = ZoneCommand:new('Batumi')
zones.batumi.initialState = { side=2 }
zones.batumi.keepActive = true
zones.batumi.isHeloSpawn = true
zones.batumi.isPlaneSpawn = true
zones.batumi.maxResource = 50000
zones.batumi:defineUpgrades({
    [1] = { --red side
        presets.upgrades.basic.comPost:extend({ 
            name = 'batumi-com-red',
            products = {
                presets.special.red.infantry:extend({ name='batumi-defense-red'}),
                presets.defenses.red.infantry:extend({ name='batumi-garrison-red' })
            }
        }),
    }, 
    [2] = --blue side
    {	
        presets.upgrades.basic.comPost:extend({ 
            name = 'batumi-com-blue',
            products = {
                presets.special.blue.infantry:extend({ name='batumi-defense-blue'}),
                presets.defenses.blue.infantry:extend({ name='batumi-garrison-blue' })
            }
        }),
        presets.upgrades.supply.fuelTank:extend({ 
            name = 'batumi-fueltank-blue',
            products = {
                presets.missions.supply.convoy_escorted:extend({ name='batumi-supply-convoy-1'}),
                presets.missions.supply.helo:extend({ name='batumi-supply-blue-1' }),
                presets.missions.supply.transfer:extend({name='batumi-transfer-blue'})
            }
        }),
        presets.upgrades.airdef.comCenter:extend({ 
            name = 'batumi-mission-command-blue',
            products = {
                presets.defenses.blue.shorad:extend({ name='batumi-sam-blue' }),
                presets.missions.attack.sead:extend({name='batumi-sead-blue-1', altitude=25000, expend=AI.Task.WeaponExpend.ALL}),
                presets.missions.attack.cas:extend({name='batumi-cas-blue-1', altitude=15000, expend=AI.Task.WeaponExpend.ONE}),
                presets.missions.attack.bai:extend({name='batumi-cas-blue-1', altitude=10000, expend=AI.Task.WeaponExpend.ONE}),
                presets.missions.attack.strike:extend({name='batumi-strike-blue-1', altitude=20000, expend=AI.Task.WeaponExpend.ALL}),
                presets.missions.patrol.aircraft:extend({name='batumi-patrol-blue-1', altitude=25000, range=25}),
                presets.missions.support.awacs:extend({name='batumi-awacs-blue', altitude=30000, freq=257.5}),
                presets.missions.support.tanker:extend({name='batumi-tanker-blue', altitude=25000, freq=257, tacan='37', variant="Drogue"})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Batumi.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Mike.lua ]]-----------------

zones.mike = ZoneCommand:new("Mike")
zones.mike.initialState = { side=1 }
zones.mike.keepActive = true
zones.mike:defineUpgrades({
    [1] =  
    {
        presets.upgrades.basic.tent:extend({
            name='mike-tent-red',
            products = {
                presets.special.red.infantry:extend({ name='mike-defense-red'})
            }
        }),
        presets.upgrades.airdef.comCenter:extend({
            name='mike-comcenter-red',
            products = {
                presets.defenses.red.sam:extend({ name='mike-sam-red'})
            }
        })
    },
    [2] = 
    {
        presets.upgrades.basic.tent:extend({
            name='mike-tent-blue',
            products = {
                presets.special.blue.infantry:extend({ name='mike-defense-blue'})
            }
        }),
        presets.upgrades.airdef.comCenter:extend({
            name='mike-comcenter-blue',
            products = {
                presets.defenses.blue.sam:extend({ name='mike-sam-blue'})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Mike.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Tyrnyauz.lua ]]-----------------

zones.tyrnyauz = ZoneCommand:new("Tyrnyauz")
zones.tyrnyauz.initialState = { side=1 }
zones.tyrnyauz.isHeloSpawn = true
zones.tyrnyauz:defineUpgrades({
    [1] = {
        presets.upgrades.basic.tent:extend({
            name='tyrnyauz-tent-red',
            products = {
                presets.special.red.infantry:extend({ name='tyrnyauz-defense-red'}),
				presets.defenses.red.infantry:extend({ name='tyrnyauz-garrison-red'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='tyrnyauz-fuel-red',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='tyrnyauz-supply-red'}),
                presets.missions.supply.helo:extend({name='tyrnyauz-supply-red-2'}),
                presets.missions.supply.transfer:extend({name='tyrnyauz-transfer-red'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='tyrnyauz-ammo-red',
            products = {
                presets.missions.attack.surface:extend({name='tyrnyauz-assault-red'})
            }
        })
    },
    [2] = {
        presets.upgrades.basic.tent:extend({
            name='tyrnyauz-tent-blue',
            products = {
                presets.special.blue.infantry:extend({ name='tyrnyauz-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='tyrnyauz-garrison-blue'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='tyrnyauz-fuel-blue',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='tyrnyauz-supply-blue'}),
                presets.missions.supply.helo:extend({name='tyrnyauz-supply-blue-2'}),
                presets.missions.supply.transfer:extend({name='tyrnyauz-transfer-blue'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='tyrnyauz-ammo-blue',
            products = {
                presets.missions.attack.surface:extend({name='tyrnyauz-assault-blue'})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Tyrnyauz.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/India.lua ]]-----------------

zones.india = ZoneCommand:new("India")
zones.india.initialState = nil
zones.india:defineUpgrades({
    [1] = {
        presets.upgrades.basic.tent:extend({
            name='india-tent-red',
            products = {
                presets.special.red.infantry:extend({ name='india-defense-red'}),
				presets.defenses.red.infantry:extend({ name='india-garrison-red'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='india-fuel-red',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='india-supply-red'}),
                presets.missions.supply.transfer:extend({name='india-transfer-red'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='india-ammo-red',
            products = {
                presets.missions.attack.surface:extend({name='india-assault-red'})
            }
        })
    },
    [2] = {
        presets.upgrades.basic.tent:extend({
            name='india-tent-blue',
            products = {
                presets.special.blue.infantry:extend({ name='india-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='india-garrison-blue'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='india-fuel-blue',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='india-supply-blue'}),
                presets.missions.supply.transfer:extend({name='india-transfer-blue'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='india-ammo-blue',
            products = {
                presets.missions.attack.surface:extend({name='india-assault-blue'})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/India.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/IntelCenter.lua ]]-----------------

zones.intelcenter = ZoneCommand:new("Intel Center")
zones.intelcenter.initialState = { side=1 }
zones.intelcenter:defineUpgrades({
    [1] = 
    {
        presets.upgrades.basic.tent:extend({
            name='intelcenter-tent-red',
            products = {
                presets.special.red.infantry:extend({ name='intelcenter-defense-red'}),
				presets.defenses.red.infantry:extend({ name='intelcenter-garrison-red'})
            }
        }),
        presets.upgrades.supply.hq:extend({
            name='intelcenter-hq-red',
            products = {
                presets.missions.supply.convoy:extend({ name='intelcenter-supply-red'}),
                presets.missions.supply.convoy:extend({ name='intelcenter-supply-red-1'}),
                presets.missions.supply.transfer:extend({name='intelcenter-transfer-red'})
            }
        }),
        presets.upgrades.supply.antenna:extend({
            name='intelcenter-antenna-red',
            products = {
            }
        }),
        presets.upgrades.supply.antenna:extend({
            name='intelcenter-antenna-red-1',
            products = {
            }
        }),
        presets.upgrades.supply.antenna:extend({
            name='intelcenter-antenna-red-2',
            products = {
            }
        })
    },
    [2] = 
    {
        presets.upgrades.basic.tent:extend({
            name='intelcenter-tent-blue',
            products = {
                presets.special.blue.infantry:extend({ name='intelcenter-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='intelcenter-garrison-blue'})
            }
        }),
        presets.upgrades.supply.hq:extend({
            name='intelcenter-hq-blue',
            products = {
                presets.missions.supply.convoy:extend({ name='intelcenter-supply-blue'}),
                presets.missions.supply.convoy:extend({ name='intelcenter-supply-blue-1'}),
                presets.missions.supply.transfer:extend({name='intelcenter-transfer-blue'})
            }
        }),
        presets.upgrades.supply.antenna:extend({
            name='intelcenter-antenna-blue',
            products = {
            }
        }),
        presets.upgrades.supply.antenna:extend({
            name='intelcenter-antenna-blue-1',
            products = {
            }
        }),
        presets.upgrades.supply.antenna:extend({
            name='intelcenter-antenna-blue-2',
            products = {
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/IntelCenter.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Mineralnye.lua ]]-----------------

zones.mineralnye = ZoneCommand:new("Mineralnye")
zones.mineralnye.initialState = { side=1 }
zones.mineralnye.keepActive = true
zones.mineralnye.isHeloSpawn = true
zones.mineralnye.isPlaneSpawn = true
zones.mineralnye:defineUpgrades({
    [1] = 
    {
        presets.upgrades.basic.comPost:extend({
            name='mineralnye-compost-red',
            products = {
                presets.special.red.infantry:extend({ name='mineralnye-defense-red'}),
				presets.defenses.red.infantry:extend({ name='mineralnye-garrison-red'})
            }
        }),
        presets.upgrades.supply.fuelTank:extend({
            name='mineralnye-fuel-red',
            products = {
                presets.missions.supply.helo:extend({name='mineralnye-supply-red'}),
                presets.missions.supply.helo:extend({name='mineralnye-supply-red-1'}),
                presets.missions.supply.transfer:extend({name='mineralnye-transfer-red'})
            }
        }),
        presets.upgrades.airdef.comCenter:extend({
            name='mineralnye-comcenter-red',
            products = {
                presets.defenses.red.sa11:extend({ name='mineralnye-airdef-red'}),
                presets.missions.attack.cas:extend({name='mineralnye-cas-red', altitude=15000, expend=AI.Task.WeaponExpend.ONE}),
                presets.missions.attack.bai:extend({name='mineralnye-cas-red', altitude=10000, expend=AI.Task.WeaponExpend.ONE}),
                presets.missions.attack.strike:extend({name='mineralnye-strike-red', altitude=30000, expend=AI.Task.WeaponExpend.ALL}),
                presets.missions.attack.strike:extend({name='mineralnye-strike-red-1', altitude=30000, expend=AI.Task.WeaponExpend.ALL}),
                presets.missions.patrol.aircraft:extend({name='mineralnye-patrol-red', altitude=25000, range=25})
            }
        })
    },
    [2] = 
    {
        presets.upgrades.basic.comPost:extend({
            name='mineralnye-compost-blue',
            products = {
                presets.special.blue.infantry:extend({ name='mineralnye-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='mineralnye-garrison-blue'})
            }
        }),
        presets.upgrades.supply.fuelTank:extend({
            name='mineralnye-fuel-blue',
            products = {
                presets.missions.supply.helo:extend({name='mineralnye-supply-blue'}),
                presets.missions.supply.helo:extend({name='mineralnye-supply-blue-1'}),
                presets.missions.supply.transfer:extend({name='mineralnye-transfer-blue'})
            }
        }),
        presets.upgrades.airdef.comCenter:extend({
            name='mineralnye-comcenter-blue',
            products = {
                presets.defenses.blue.nasams:extend({ name='mineralnye-airdef-blue'}),
                presets.missions.attack.cas:extend({name='mineralnye-cas-blue', altitude=15000, expend=AI.Task.WeaponExpend.ONE}),
                presets.missions.attack.bai:extend({name='mineralnye-cas-blue', altitude=10000, expend=AI.Task.WeaponExpend.ONE}),
                presets.missions.attack.strike:extend({name='mineralnye-strike-blue', altitude=30000, expend=AI.Task.WeaponExpend.ALL}),
                presets.missions.attack.strike:extend({name='mineralnye-strike-blue-1', altitude=30000, expend=AI.Task.WeaponExpend.ALL}),
                presets.missions.patrol.aircraft:extend({name='mineralnye-patrol-blue', altitude=25000, range=25})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Mineralnye.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/PowerPlant.lua ]]-----------------

zones.powerplant = ZoneCommand:new("Power Plant")
zones.powerplant.initialState = { side=1 }
zones.powerplant:defineUpgrades({
    [1] = 
    {
        presets.upgrades.basic.tent:extend({
            name='powerplant-tent-red',
            products = {
                presets.special.red.infantry:extend({ name='powerplant-defense-red'}),
				presets.defenses.red.infantry:extend({ name='powerplant-garrison-red'})
            }
        }),
        presets.upgrades.supply.powerplant1:extend({
            name='powerplant-building-red-1',
            products = {
                presets.missions.supply.convoy:extend({ name='powerplant-supply-red'}),
                presets.missions.supply.transfer:extend({name='powerplant-transfer-red'})
            }
        }),
        presets.upgrades.supply.powerplant2:extend({
            name='powerplant-building-red-2',
            products = {
                presets.missions.supply.convoy:extend({ name='powerplant-supply-red-1'}),
                presets.missions.supply.transfer:extend({name='powerplant-transfer-red'})
            }
        })
    },
    [2] = 
    {
        presets.upgrades.basic.tent:extend({
            name='powerplant-tent-blue',
            products = {
                presets.special.blue.infantry:extend({ name='powerplant-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='powerplant-garrison-blue'})
            }
        }),
        presets.upgrades.supply.powerplant1:extend({
            name='powerplant-building-blue-1',
            products = {
                presets.missions.supply.convoy:extend({ name='powerplant-supply-blue'}),
                presets.missions.supply.transfer:extend({name='powerplant-transfer-blue'})
            }
        }),
        presets.upgrades.supply.powerplant2:extend({
            name='powerplant-building-blue-2',
            products = {
                presets.missions.supply.convoy:extend({ name='powerplant-supply-blue-1'}),
                presets.missions.supply.transfer:extend({name='powerplant-transfer-blue'})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/PowerPlant.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Zugdidi.lua ]]-----------------

zones.zugdidi = ZoneCommand:new("Zugdidi")
zones.zugdidi.initialState = { side=1 }
zones.zugdidi:defineUpgrades({
    [1] =  
    {
        presets.upgrades.basic.comPost:extend({
            name='zugdidi-compost-red',
            products = {
                presets.missions.supply.transfer:extend({name='zugdidi-transfer-red'}),
                presets.special.red.infantry:extend({ name='zugdidi-defense-red'}),
				presets.defenses.red.infantry:extend({ name='zugdidi-garrison-red'}),
                presets.missions.attack.surface:extend({name='zugdidi-attack-red'}),
                presets.missions.supply.convoy:extend({name='zugdidi-supply-red'})
            }
        }),
        presets.upgrades.supply.hangar:extend({
            name='zugdidi-hangar-red-1',
            products = {
                presets.missions.supply.helo:extend({name='zugdidi-supply-red-1'})
            }
        }),
        presets.upgrades.supply.hangar:extend({
            name='zugdidi-hangar-red-2',
            products = {
                presets.missions.supply.helo:extend({name='zugdidi-supply-red-2'})
            }
        }),
        presets.upgrades.supply.hangar:extend({
            name='zugdidi-hangar-red-3',
            products = {
                presets.missions.supply.helo:extend({name='zugdidi-supply-red-3'})
            }
        }),
        presets.upgrades.airdef.comCenter:extend({
            name='zugdidi-comcenter-red',
            products = {
                presets.defenses.red.sa6:extend({ name='zugdidi-sam-red'})
            }
        })
    },
    [2] = 
    {
        presets.upgrades.basic.tent:extend({
            name='zugdidi-compost-blue',
            products = {
                presets.missions.supply.transfer:extend({name='zugdidi-transfer-blue'}),
                presets.special.blue.infantry:extend({ name='zugdidi-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='zugdidi-garrison-blue'}),
                presets.missions.attack.surface:extend({name='zugdidi-attack-blue'}),
                presets.missions.supply.convoy:extend({name='zugdidi-supply-blue'})
            }
        }),
        presets.upgrades.supply.hangar:extend({
            name='zugdidi-hangar-blue-1',
            products = {
                presets.missions.supply.helo:extend({name='zugdidi-supply-blue-1'})
            }
        }),
        presets.upgrades.supply.hangar:extend({
            name='zugdidi-hangar-blue-2',
            products = {
                presets.missions.supply.helo:extend({name='zugdidi-supply-blue-2'})
            }
        }),
        presets.upgrades.supply.hangar:extend({
            name='zugdidi-hangar-blue-3',
            products = {
                presets.missions.supply.helo:extend({name='zugdidi-supply-blue-3'})
            }
        }),
        presets.upgrades.airdef.comCenter:extend({
            name='zugdidi-comcenter-blue',
            products = {
                presets.defenses.blue.shorad:extend({ name='zugdidi-sam-blue'})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Zugdidi.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Babugent.lua ]]-----------------

zones.babugent = ZoneCommand:new("Babugent")
zones.babugent.initialState = { side=1 }
zones.babugent:defineUpgrades({
    [1] = {
        presets.upgrades.basic.tent:extend({
            name='babugent-tent-red',
            products = {
                presets.special.red.infantry:extend({ name='babugent-defense-red'}),
				presets.defenses.red.infantry:extend({ name='babugent-garrison-red'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='babugent-fuel-red',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='babugent-supply-red'}),
                presets.missions.supply.helo:extend({name='babugent-supply-red-2'}),
                presets.missions.supply.transfer:extend({name='babugent-transfer-red'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='babugent-ammo-red',
            products = {
                presets.missions.attack.surface:extend({name='babugent-assault-red'})
            }
        })
    },
    [2] = {
        presets.upgrades.basic.tent:extend({
            name='babugent-tent-blue',
            products = {
                presets.special.blue.infantry:extend({ name='babugent-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='babugent-garrison-blue'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='babugent-fuel-blue',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='babugent-supply-blue'}),
                presets.missions.supply.helo:extend({name='babugent-supply-blue-2'}),
                presets.missions.supply.transfer:extend({name='babugent-transfer-blue'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='babugent-ammo-blue',
            products = {
                presets.missions.attack.surface:extend({name='babugent-assault-blue'})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Babugent.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Kislovodsk.lua ]]-----------------

zones.kislovodsk = ZoneCommand:new("Kislovodsk")
zones.kislovodsk.initialState = { side=1 }
zones.kislovodsk:defineUpgrades({
    [1] = {
        presets.upgrades.basic.tent:extend({
            name='kislovodsk-tent-red',
            products = {
                presets.special.red.infantry:extend({ name='kislovodsk-defense-red'}),
				presets.defenses.red.infantry:extend({ name='kislovodsk-garrison-red'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='kislovodsk-fuel-red',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='kislovodsk-supply-red'}),
                presets.missions.supply.transfer:extend({name='kislovodsk-transfer-red'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='kislovodsk-ammo-red',
            products = {
                presets.missions.attack.surface:extend({name='kislovodsk-assault-red'})
            }
        })
    },
    [2] = {
        presets.upgrades.basic.tent:extend({
            name='kislovodsk-tent-blue',
            products = {
                presets.special.blue.infantry:extend({ name='kislovodsk-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='kislovodsk-garrison-blue'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='kislovodsk-fuel-blue',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='kislovodsk-supply-blue'}),
                presets.missions.supply.transfer:extend({name='kislovodsk-transfer-blue'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='kislovodsk-ammo-blue',
            products = {
                presets.missions.attack.surface:extend({name='kislovodsk-assault-blue'})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Kislovodsk.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Gudauta.lua ]]-----------------

zones.gudauta = ZoneCommand:new("Gudauta")
zones.gudauta.initialState = { side=1 }
zones.gudauta.keepActive = true
zones.gudauta.maxResource = 50000
zones.gudauta:defineUpgrades({
    [1] = 
    {
        presets.upgrades.basic.comPost:extend({
            name='gudauta-compost-red',
            products = {
                presets.special.red.infantry:extend({ name='gudauta-defense-red'}),
				presets.defenses.red.infantry:extend({ name='gudauta-garrison-red'})
            }
        }),
        presets.upgrades.supply.fuelTank:extend({
            name='gudauta-fuel-red',
            products = {
                presets.missions.supply.helo:extend({name='gudauta-supply-red'}),
                presets.missions.supply.helo:extend({name='gudauta-supply-red-1'}),
                presets.missions.supply.transfer:extend({name='gudauta-transfer-red'})
            }
        }),
        presets.upgrades.airdef.comCenter:extend({
            name='gudauta-comcenter-red',
            products = {
                presets.defenses.red.sam:extend({ name='gudauta-airdef-red'}),
                presets.missions.attack.sead:extend({name='gudauta-sead-red', altitude=25000, expend=AI.Task.WeaponExpend.ALL}),
                presets.missions.attack.sead:extend({name='gudauta-sead-red-1', altitude=25000, expend=AI.Task.WeaponExpend.ALL}),
                presets.missions.attack.cas:extend({name='gudauta-cas-red', altitude=15000, expend=AI.Task.WeaponExpend.ONE}),
                presets.missions.attack.bai:extend({name='gudauta-cas-red', altitude=10000, expend=AI.Task.WeaponExpend.ONE}),
                presets.missions.patrol.aircraft:extend({name='gudauta-patrol-red', altitude=25000, range=25})
            }
        })
    },
    [2] = 
    {
        presets.upgrades.basic.comPost:extend({
            name='gudauta-compost-blue',
            products = {
                presets.special.blue.infantry:extend({ name='gudauta-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='gudauta-garrison-blue'})
            }
        }),
        presets.upgrades.supply.fuelTank:extend({
            name='gudauta-fuel-blue',
            products = {
                presets.missions.supply.helo:extend({name='gudauta-supply-blue'}),
                presets.missions.supply.helo:extend({name='gudauta-supply-blue-1'}),
                presets.missions.supply.transfer:extend({name='gudauta-transfer-blue'})
            }
        }),
        presets.upgrades.airdef.comCenter:extend({
            name='gudauta-comcenter-blue',
            products = {
                presets.defenses.blue.sam:extend({ name='gudauta-airdef-blue'}),
                presets.missions.attack.sead:extend({name='gudauta-sead-blue', altitude=25000, expend=AI.Task.WeaponExpend.ALL}),
                presets.missions.attack.sead:extend({name='gudauta-sead-blue-1', altitude=25000, expend=AI.Task.WeaponExpend.ALL}),
                presets.missions.attack.cas:extend({name='gudauta-cas-blue', altitude=15000, expend=AI.Task.WeaponExpend.ONE}),
                presets.missions.attack.bai:extend({name='gudauta-cas-blue', altitude=10000, expend=AI.Task.WeaponExpend.ONE}),
                presets.missions.patrol.aircraft:extend({name='gudauta-patrol-blue', altitude=25000, range=25})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Gudauta.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Distillery.lua ]]-----------------

zones.distillery = ZoneCommand:new("Distillery")
zones.distillery.initialState = { side=1 }
zones.distillery:defineUpgrades({
    [1] = 
    {
        presets.upgrades.basic.tent:extend({
            name='distillery-tent-red',
            products = {
                presets.special.red.infantry:extend({ name='distillery-defense-red'}),
				presets.defenses.red.infantry:extend({ name='distillery-garrison-red'})
            }
        }),
        presets.upgrades.supply.factory1:extend({
            name='distillery-prod-red-1',
            products = {
                presets.missions.supply.convoy:extend({ name='distillery-supply-red-1'}),
                presets.missions.supply.transfer:extend({name='distillery-transfer-red'})
            }
        }),
        presets.upgrades.supply.factory2:extend({
            name='distillery-prod-red-2',
            products = {
                presets.missions.supply.convoy:extend({ name='distillery-supply-red-2', cost=2000}),
                presets.missions.supply.transfer:extend({name='distillery-transfer-red2'})
            }
        }),
        presets.upgrades.supply.factoryTank:extend({
            name='distillery-tank-red-1',
            products = {
            }
        }),
        presets.upgrades.supply.factoryTank:extend({
            name='distillery-tank-red-2',
            products = {
            }
        }),
        presets.upgrades.supply.factoryTank:extend({
            name='distillery-tank-red-3',
            products = {
            }
        })
    },
    [2] = 
    {
        presets.upgrades.basic.tent:extend({
            name='distillery-tent-blue',
            products = {
                presets.special.blue.infantry:extend({ name='distillery-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='distillery-garrison-blue'})
            }
        }),
        presets.upgrades.supply.factory1:extend({
            name='distillery-prod-blue-1',
            products = {
                presets.missions.supply.convoy:extend({ name='distillery-supply-blue-1'}),
                presets.missions.supply.transfer:extend({name='distillery-transfer-blue'})
            }
        }),
        presets.upgrades.supply.factory2:extend({
            name='distillery-prod-blue-2',
            products = {
                presets.missions.supply.convoy:extend({ name='distillery-supply-blue-2', cost=2000}),
                presets.missions.supply.transfer:extend({name='distillery-transfer-blue2'})
            }
        }),
        presets.upgrades.supply.factoryTank:extend({
            name='distillery-tank-blue-1',
            products = {
            }
        }),
        presets.upgrades.supply.factoryTank:extend({
            name='distillery-tank-blue-2',
            products = {
            }
        }),
        presets.upgrades.supply.factoryTank:extend({
            name='distillery-tank-blue-3',
            products = {
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Distillery.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Sochi.lua ]]-----------------

zones.sochi = ZoneCommand:new("Sochi")
zones.sochi.initialState = { side=1 }
zones.sochi.keepActive = true
zones.sochi.maxResource = 50000
zones.sochi:defineUpgrades({
    [1] = 
    {
        presets.upgrades.basic.comPost:extend({
            name='sochi-compost-red',
            products = {
                presets.special.red.infantry:extend({ name='sochi-defense-red'}),
				presets.defenses.red.infantry:extend({ name='sochi-garrison-red'})
            }
        }),
        presets.upgrades.supply.fuelTank:extend({
            name='sochi-fuel-red',
            products = {
                presets.missions.supply.helo:extend({name='sochi-supply-red-1'}),
                presets.missions.supply.helo:extend({name='sochi-supply-red-2'}),
                presets.missions.supply.convoy_escorted:extend({name='sochi-supply-red-3'}),
                presets.missions.supply.transfer:extend({name='sochi-transfer-red'})
            }
        }),
        presets.upgrades.airdef.comCenter:extend({
            name='sochi-comcenter-red',
            products = {
                presets.defenses.red.sa10:extend({ name='sochi-airdef-red'}),
                presets.missions.attack.sead:extend({name='sochi-sead-red', altitude=25000, expend=AI.Task.WeaponExpend.ALL}),
                presets.missions.attack.strike:extend({name='sochi-strike-red', altitude=30000, expend=AI.Task.WeaponExpend.ALL}),
                presets.missions.patrol.aircraft:extend({name='sochi-patrol-red', altitude=25000, range=25}),
                presets.missions.patrol.aircraft:extend({name='sochi-patrol-red-1', altitude=25000, range=25}),
                presets.missions.attack.cas:extend({name='sochi-cas-red', altitude=15000, expend=AI.Task.WeaponExpend.ONE}),
                presets.missions.attack.bai:extend({name='sochi-cas-red', altitude=10000, expend=AI.Task.WeaponExpend.ONE})
            }
        })
    },
    [2] = 
    {
        presets.upgrades.basic.comPost:extend({
            name='sochi-compost-blue',
            products = {
                presets.special.blue.infantry:extend({ name='sochi-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='sochi-garrison-blue'})
            }
        }),
        presets.upgrades.supply.fuelTank:extend({
            name='sochi-fuel-blue',
            products = {
                presets.missions.supply.helo:extend({name='sochi-supply-blue-1'}),
                presets.missions.supply.helo:extend({name='sochi-supply-blue-2'}),
                presets.missions.supply.convoy_escorted:extend({name='sochi-supply-blue-3'}),
                presets.missions.supply.transfer:extend({name='sochi-transfer-blue'})
            }
        }),
        presets.upgrades.airdef.comCenter:extend({
            name='sochi-comcenter-blue',
            products = {
                presets.defenses.blue.patriot:extend({ name='sochi-airdef-blue'}),
                presets.missions.attack.sead:extend({name='sochi-sead-blue', altitude=25000, expend=AI.Task.WeaponExpend.ALL}),
                presets.missions.attack.strike:extend({name='sochi-strike-blue', altitude=30000, expend=AI.Task.WeaponExpend.ALL}),
                presets.missions.patrol.aircraft:extend({name='sochi-patrol-blue', altitude=25000, range=25}),
                presets.missions.attack.cas:extend({name='sochi-cas-blue', altitude=15000, expend=AI.Task.WeaponExpend.ONE}),
                presets.missions.attack.bai:extend({name='sochi-cas-blue', altitude=10000, expend=AI.Task.WeaponExpend.ONE})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Sochi.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Golf.lua ]]-----------------

zones.golf = ZoneCommand:new("Golf")
zones.golf.initialState = nil
zones.golf.isHeloSpawn = true
zones.golf:defineUpgrades({
    [1] = {
        presets.upgrades.basic.tent:extend({
            name='golf-tent-red',
            products = {
                presets.special.red.infantry:extend({ name='golf-defense-red'}),
				presets.defenses.red.infantry:extend({ name='golf-garrison-red'})
            }
        }),
        presets.upgrades.supply.fuelTank:extend({
            name='golf-fuel-red',
            products = {
                presets.missions.supply.helo:extend({name='golf-supply-red'}),
                presets.missions.supply.helo:extend({name='golf-supply-red-1'}),
                presets.missions.supply.transfer:extend({name='golf-transfer-red'})
            }
        }),
        presets.upgrades.airdef.comCenter:extend({
            name='golf-comcenter-red',
            products = {
                presets.defenses.red.shorad:extend({name='golf-sam-red'}),
                presets.missions.attack.helo:extend({name='golf-cas-red', altitude=200, expend=AI.Task.WeaponExpend.HALF })
            }
        })
    },
    [2] = {
        presets.upgrades.basic.tent:extend({
            name='golf-tent-blue',
            products = {
                presets.special.blue.infantry:extend({ name='golf-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='golf-garrison-blue'})
            }
        }),
        presets.upgrades.supply.fuelTankFarp:extend({
            name='golf-fuel-blue',
            products = {
                presets.missions.supply.helo:extend({name='golf-supply-blue'}),
                presets.missions.supply.helo:extend({name='golf-supply-blue-1'}),
                presets.missions.supply.transfer:extend({name='golf-transfer-blue'})
            }
        }),
        presets.upgrades.airdef.comCenter:extend({
            name='golf-comcenter-blue',
            products = {
                presets.defenses.blue.shorad:extend({name='golf-sam-blue'}),
                presets.missions.attack.helo:extend({name='golf-cas-blue', altitude=200, expend=AI.Task.WeaponExpend.HALF })
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Golf.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Charlie.lua ]]-----------------

zones.charlie = ZoneCommand:new("Charlie")
zones.charlie.initialState = { side=2 }
zones.charlie.keepActive = true
zones.charlie:defineUpgrades({
    [1] =  
    {
        presets.upgrades.basic.tent:extend({
            name='charlie-tent-red',
            products = {
                presets.special.red.infantry:extend({ name='charlie-defense-red'}),
				presets.defenses.red.infantry:extend({ name='charlie-garrison-red'})
            }
        }),
        presets.upgrades.airdef.comCenter:extend({
            name='charlie-comcenter-red',
            products = {
                presets.defenses.red.sam:extend({ name='charlie-sam-red'})
            }
        })
    },
    [2] = 
    {
        presets.upgrades.basic.tent:extend({
            name='charlie-tent-blue',
            products = {
                presets.special.blue.infantry:extend({ name='charlie-defense-red'}),
            }
        }),
        presets.upgrades.airdef.comCenter:extend({
            name='charlie-comcenter-blue',
            products = {
                presets.defenses.blue.sam:extend({ name='charlie-sam-blue'})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Charlie.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Lentehi.lua ]]-----------------

zones.lentehi = ZoneCommand:new("Lentehi")
zones.lentehi.initialState = { side=1 }
zones.lentehi:defineUpgrades({
    [1] = {
        presets.upgrades.basic.tent:extend({
            name='lentehi-tent-red',
            products = {
                presets.special.red.infantry:extend({ name='lentehi-defense-red'}),
				presets.defenses.red.infantry:extend({ name='lentehi-garrison-red'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='lentehi-fuel-red',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='lentehi-supply-red'}),
                presets.missions.supply.helo:extend({name='lentehi-supply-red-2'}),
                presets.missions.supply.transfer:extend({name='lentehi-transfer-red'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='lentehi-ammo-red',
            products = {
                presets.missions.attack.surface:extend({name='lentehi-assault-red'})
            }
        })
    },
    [2] = {
        presets.upgrades.basic.tent:extend({
            name='lentehi-tent-blue',
            products = {
                presets.special.blue.infantry:extend({ name='lentehi-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='lentehi-garrison-blue'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='lentehi-fuel-blue',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='lentehi-supply-blue'}),
                presets.missions.supply.helo:extend({name='lentehi-supply-blue-2'}),
                presets.missions.supply.transfer:extend({name='lentehi-transfer-blue'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='lentehi-ammo-blue',
            products = {
                presets.missions.attack.surface:extend({name='lentehi-assault-blue'})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Lentehi.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Refinery.lua ]]-----------------

zones.refinery = ZoneCommand:new("Refinery")
zones.refinery.initialState = { side=1 }
zones.refinery:defineUpgrades({
    [1] = 
    {
        presets.upgrades.basic.tent:extend({
            name='refinery-tent-red',
            products = {
                presets.special.red.infantry:extend({ name='refinery-defense-red'}),
				presets.defenses.red.infantry:extend({ name='refinery-garrison-red'})
            }
        }),
        presets.upgrades.supply.refinery1:extend({
            name='refinery-building-red',
            products = {
                presets.missions.supply.convoy:extend({ name='refinery-supply-red'}),
                presets.missions.supply.convoy:extend({ name='refinery-supply-red-1'}),
                presets.missions.supply.helo:extend({ name='refinery-supply-red-2'}),
                presets.missions.supply.transfer:extend({name='refinery-transfer-red'})
            }
        })
    },
    [2] = 
    {
        presets.upgrades.basic.tent:extend({
            name='refinery-tent-blue',
            products = {
                presets.special.blue.infantry:extend({ name='refinery-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='refinery-garrison-blue'})
            }
        }),
        presets.upgrades.supply.refinery1:extend({
            name='refinery-building-blue',
            products = {
                presets.missions.supply.convoy:extend({ name='refinery-supply-blue'}),
                presets.missions.supply.convoy:extend({ name='refinery-supply-blue-1'}),
                presets.missions.supply.helo:extend({ name='refinery-supply-blue-2'}),
                presets.missions.supply.transfer:extend({name='refinery-transfer-blue'})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Refinery.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Mozdok.lua ]]-----------------

zones.mozdok = ZoneCommand:new("Mozdok")
zones.mozdok.initialState = { side=1 }
zones.mozdok.keepActive = true
zones.mozdok.maxResource = 50000
zones.mozdok:defineUpgrades({
    [1] = 
    {
        presets.upgrades.basic.comPost:extend({
            name='mozdok-compost-red',
            products = {
                presets.special.red.infantry:extend({ name='mozdok-defense-red'}),
				presets.defenses.red.infantry:extend({ name='mozdok-garrison-red'})
            }
        }),
        presets.upgrades.supply.fuelTank:extend({
            name='mozdok-fuel-red',
            products = {
                presets.missions.supply.helo:extend({name='mozdok-supply-red-1'}),
                presets.missions.supply.helo:extend({name='mozdok-supply-red-2'}),
                presets.missions.supply.convoy_escorted:extend({name='mozdok-supply-red-3'}),
                presets.missions.supply.transfer:extend({name='mozdok-transfer-red'})
            }
        }),
        presets.upgrades.airdef.comCenter:extend({
            name='mozdok-comcenter-red',
            products = {
                presets.defenses.red.sa10:extend({ name='mozdok-airdef-red'}),
                presets.missions.patrol.aircraft:extend({name='mozdok-patrol-red', altitude=25000, range=25}),
                presets.missions.attack.cas:extend({name='mozdok-cas-red', altitude=15000, expend=AI.Task.WeaponExpend.ONE}),
                presets.missions.attack.bai:extend({name='mozdok-cas-red', altitude=10000, expend=AI.Task.WeaponExpend.ONE})
            }
        })
    },
    [2] = 
    {
        presets.upgrades.basic.comPost:extend({
            name='mozdok-compost-blue',
            products = {
                presets.special.blue.infantry:extend({ name='mozdok-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='mozdok-garrison-blue'})
            }
        }),
        presets.upgrades.supply.fuelTank:extend({
            name='mozdok-fuel-blue',
            products = {
                presets.missions.supply.helo:extend({name='mozdok-supply-blue-1'}),
                presets.missions.supply.helo:extend({name='mozdok-supply-blue-2'}),
                presets.missions.supply.convoy_escorted:extend({name='mozdok-supply-blue-3'}),
                presets.missions.supply.transfer:extend({name='mozdok-transfer-blue'})
            }
        }),
        presets.upgrades.airdef.comCenter:extend({
            name='mozdok-comcenter-blue',
            products = {
                presets.defenses.blue.shorad:extend({ name='mozdok-airdef-blue'}),
                presets.missions.patrol.aircraft:extend({name='mozdok-patrol-blue', altitude=25000, range=25}),
                presets.missions.attack.cas:extend({name='mozdok-cas-blue', altitude=15000, cost=50, expend=AI.Task.WeaponExpend.ONE}),
                presets.missions.attack.cas:extend({name='mozdok-cas-blue-1', altitude=15000, cost=50, expend=AI.Task.WeaponExpend.ONE}),
                presets.missions.attack.bai:extend({name='mozdok-cas-blue', altitude=15000, cost=50, expend=AI.Task.WeaponExpend.ONE}),
                presets.missions.attack.bai:extend({name='mozdok-cas-blue-1', altitude=15000, cost=50, expend=AI.Task.WeaponExpend.ONE})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Mozdok.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Lima.lua ]]-----------------

zones.lima = ZoneCommand:new("Lima")
zones.lima.initialState = { side=1 }
zones.lima:defineUpgrades({
    [1] = {
        presets.upgrades.basic.tent:extend({
            name='lima-tent-red',
            products = {
                presets.special.red.infantry:extend({ name='lima-defense-red'}),
				presets.defenses.red.infantry:extend({ name='lima-garrison-red'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='lima-fuel-red',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='lima-supply-red'}),
                presets.missions.supply.helo:extend({name='lima-supply-red-1'}),
                presets.missions.supply.transfer:extend({name='lima-transfer-red'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='lima-ammo-red',
            products = {
                presets.missions.attack.surface:extend({name='lima-assault-red'})
            }
        })
    },
    [2] = {
        presets.upgrades.basic.tent:extend({
            name='lima-tent-blue',
            products = {
                presets.special.blue.infantry:extend({ name='lima-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='lima-garrison-blue'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='lima-fuel-blue',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='lima-supply-blue'}),
                presets.missions.supply.helo:extend({name='lima-supply-blue-1'}),
                presets.missions.supply.transfer:extend({name='lima-transfer-blue'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='lima-ammo-blue',
            products = {
                presets.missions.attack.surface:extend({name='lima-assault-blue'})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Lima.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Oscar.lua ]]-----------------

zones.oscar = ZoneCommand:new("Oscar")
zones.oscar.initialState = { side=1 }
zones.oscar:defineUpgrades({
    [1] = {
        presets.upgrades.basic.tent:extend({
            name='oscar-tent-red',
            products = {
                presets.special.red.infantry:extend({ name='oscar-defense-red'}),
				presets.defenses.red.infantry:extend({ name='oscar-garrison-red'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='oscar-fuel-red',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='oscar-supply-red'}),
                presets.missions.supply.transfer:extend({name='oscar-transfer-red'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='oscar-ammo-red',
            products = {
                presets.missions.attack.surface:extend({name='oscar-assault-red'})
            }
        })
    },
    [2] = {
        presets.upgrades.basic.tent:extend({
            name='oscar-tent-blue',
            products = {
                presets.special.blue.infantry:extend({ name='oscar-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='oscar-garrison-blue'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='oscar-fuel-blue',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='oscar-supply-blue'}),
                presets.missions.supply.transfer:extend({name='oscar-transfer-blue'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='oscar-ammo-blue',
            products = {
                presets.missions.attack.surface:extend({name='oscar-assault-blue'})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Oscar.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Nalchik.lua ]]-----------------

zones.nalchik = ZoneCommand:new("Nalchik")
zones.nalchik.initialState = { side=1 }
zones.nalchik.keepActive = true
zones.nalchik.isHeloSpawn = true
zones.nalchik.isPlaneSpawn = true
zones.nalchik:defineUpgrades({
    [1] = 
    {
        presets.upgrades.basic.comPost:extend({
            name='nalchik-compost-red',
            products = {
                presets.special.red.infantry:extend({ name='nalchik-defense-red'}),
				presets.defenses.red.infantry:extend({ name='nalchik-garrison-red'})
            }
        }),
        presets.upgrades.supply.fuelTank:extend({
            name='nalchik-fuel-red',
            products = {
                presets.missions.supply.helo:extend({name='nalchik-supply-red-1'}),
                presets.missions.supply.helo:extend({name='nalchik-supply-red-2'}),
                presets.missions.supply.transfer:extend({name='nalchik-transfer-red'})
            }
        }),
        presets.upgrades.airdef.comCenter:extend({
            name='nalchik-comcenter-red',
            products = {
                presets.defenses.red.sa3:extend({ name='nalchik-airdef-red'}),
                presets.missions.attack.sead:extend({name='nalchik-sead-red', altitude=25000, expend=AI.Task.WeaponExpend.ALL}),
                presets.missions.attack.cas:extend({name='nalchik-cas-red', altitude=15000, expend=AI.Task.WeaponExpend.ONE}),
                presets.missions.attack.bai:extend({name='nalchik-cas-red', altitude=10000, expend=AI.Task.WeaponExpend.ONE}),
                presets.missions.attack.strike:extend({name='nalchik-strike-red', altitude=30000, expend=AI.Task.WeaponExpend.ALL}),
                presets.missions.patrol.aircraft:extend({name='nalchik-patrol-red', altitude=25000, range=25}),
                presets.missions.patrol.aircraft:extend({name='nalchik-patrol-red-2', altitude=25000, range=25}),
                presets.missions.support.awacs:extend({name='nalchik-awacs-red', altitude=30000, freq=251.2}),
                presets.missions.support.tanker:extend({name='nalchik-tanker-red', altitude=30000, freq=252.2, tacan='40', variant='Drogue'})
            }
        })
    },
    [2] = 
    {
        presets.upgrades.basic.comPost:extend({
            name='nalchik-compost-blue',
            products = {
                presets.special.blue.infantry:extend({ name='nalchik-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='nalchik-garrison-blue'})
            }
        }),
        presets.upgrades.supply.fuelTank:extend({
            name='nalchik-fuel-blue',
            products = {
                presets.missions.supply.helo:extend({name='nalchik-supply-blue-1'}),
                presets.missions.supply.helo:extend({name='nalchik-supply-blue-2'}),
                presets.missions.supply.transfer:extend({name='nalchik-transfer-blue'})
            }
        }),
        presets.upgrades.airdef.comCenter:extend({
            name='nalchik-comcenter-blue',
            products = {
                presets.defenses.blue.nasams:extend({ name='nalchik-airdef-blue'}),
                presets.missions.support.awacs:extend({name='nalchik-awacs-blue', altitude=30000, freq=259.5}),
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Nalchik.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Digora.lua ]]-----------------

zones.digora = ZoneCommand:new("Digora")
zones.digora.initialState = { side=1 }
zones.digora:defineUpgrades({
    [1] = {
        presets.upgrades.basic.tent:extend({
            name='digora-tent-red',
            products = {
                presets.special.red.infantry:extend({ name='digora-defense-red'}),
				presets.defenses.red.infantry:extend({ name='digora-garrison-red'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='digora-fuel-red',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='digora-supply-red'}),
                presets.missions.supply.transfer:extend({name='digora-transfer-red'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='digora-ammo-red',
            products = {
                presets.missions.attack.surface:extend({name='digora-assault-red'})
            }
        })
    },
    [2] = {
        presets.upgrades.basic.tent:extend({
            name='digora-tent-blue',
            products = {
                presets.special.blue.infantry:extend({ name='digora-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='digora-garrison-blue'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='digora-fuel-blue',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='digora-supply-blue'}),
                presets.missions.supply.transfer:extend({name='digora-transfer-blue'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='digora-ammo-blue',
            products = {
                presets.missions.attack.surface:extend({name='digora-assault-blue'})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Digora.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Uniform.lua ]]-----------------

zones.uniform = ZoneCommand:new("Uniform")
zones.uniform.initialState = { side=1 }
zones.uniform:defineUpgrades({
    [1] = {
        presets.upgrades.basic.tent:extend({
            name='uniform-tent-red',
            products = {
                presets.special.red.infantry:extend({ name='uniform-defense-red'}),
				presets.defenses.red.infantry:extend({ name='uniform-garrison-red'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='uniform-fuel-red',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='uniform-supply-red'}),
                presets.missions.supply.transfer:extend({name='uniform-transfer-red'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='uniform-ammo-red',
            products = {
                presets.missions.attack.surface:extend({name='uniform-assault-red'})
            }
        })
    },
    [2] = {
        presets.upgrades.basic.tent:extend({
            name='uniform-tent-blue',
            products = {
                presets.special.blue.infantry:extend({ name='uniform-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='uniform-garrison-blue'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='uniform-fuel-blue',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='uniform-supply-blue'}),
                presets.missions.supply.transfer:extend({name='uniform-transfer-blue'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='uniform-ammo-blue',
            products = {
                presets.missions.attack.surface:extend({name='uniform-assault-blue'})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Uniform.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Factory.lua ]]-----------------

zones.factory = ZoneCommand:new("Factory")
zones.factory.initialState = { side=2 }
zones.factory:defineUpgrades({
    [1] = 
    {
        presets.upgrades.basic.tent:extend({
            name='factory-tent-red',
            products = {
                presets.special.red.infantry:extend({ name='factory-defense-red'}),
				presets.defenses.red.infantry:extend({ name='factory-garrison-red'})
            }
        }),
        presets.upgrades.supply.factory1:extend({
            name='factory-prod-red-1',
            products = {
                presets.missions.supply.convoy:extend({ name='factory-supply-red-1'}),
                presets.missions.supply.transfer:extend({name='factory-transfer-red'})
            }
        }),
        presets.upgrades.supply.factory2:extend({
            name='factory-prod-red-2',
            products = {
                presets.missions.supply.convoy:extend({ name='factory-supply-red-2', cost=2000}),
                presets.missions.supply.transfer:extend({name='factory-transfer-red2'})
            }
        }),
        presets.upgrades.supply.factoryTank:extend({
            name='factory-tank-red-1',
            products = {
            }
        }),
        presets.upgrades.supply.factoryTank:extend({
            name='factory-tank-red-2',
            products = {
            }
        }),
        presets.upgrades.supply.factoryTank:extend({
            name='factory-tank-red-3',
            products = {
            }
        })
    },
    [2] = 
    {
        presets.upgrades.basic.tent:extend({
            name='factory-tent-blue',
            products = {
                presets.special.blue.infantry:extend({ name='factory-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='factory-garrison-blue'})
            }
        }),
        presets.upgrades.supply.factory1:extend({
            name='factory-prod-blue-1',
            products = {
                presets.missions.supply.convoy:extend({ name='factory-supply-blue-1'}),
                presets.missions.supply.transfer:extend({name='factory-transfer-blue'})
            }
        }),
        presets.upgrades.supply.factory2:extend({
            name='factory-prod-blue-2',
            products = {
                presets.missions.supply.convoy:extend({ name='factory-supply-blue-2', cost=2000}),
                presets.missions.supply.transfer:extend({name='factory-transfer-blue2'})
            }
        }),
        presets.upgrades.supply.factoryTank:extend({
            name='factory-tank-blue-1',
            products = {
            }
        }),
        presets.upgrades.supply.factoryTank:extend({
            name='factory-tank-blue-2',
            products = {
            }
        }),
        presets.upgrades.supply.factoryTank:extend({
            name='factory-tank-blue-3',
            products = {
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Factory.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Senaki.lua ]]-----------------

zones.senaki = ZoneCommand:new("Senaki")
zones.senaki.initialState = { side=1 }
zones.senaki.keepActive = true
zones.senaki.isHeloSpawn = true
zones.senaki.isPlaneSpawn = true
zones.senaki.maxResource = 50000
zones.senaki:defineUpgrades({
    [1] = 
    {
        presets.upgrades.basic.comPost:extend({
            name='senaki-compost-red',
            products = {
                presets.special.red.infantry:extend({ name='senaki-defense-red'}),
				presets.defenses.red.infantry:extend({ name='senaki-garrison-red'})
            }
        }),
        presets.upgrades.supply.fuelTank:extend({
            name='senaki-fuel-red',
            products = {
                presets.missions.supply.helo:extend({name='senaki-supply-red-1'}),
                presets.missions.supply.helo:extend({name='senaki-supply-red-2'}),
                presets.missions.supply.transfer:extend({name='senaki-transfer-red'})
            }
        }),
        presets.upgrades.airdef.comCenter:extend({
            name='senaki-comcenter-red',
            products = {
                presets.defenses.red.sa3:extend({ name='senaki-airdef-red'}),
                presets.missions.attack.sead:extend({name='senaki-sead-red', altitude=25000, expend=AI.Task.WeaponExpend.ALL}),
                presets.missions.attack.cas:extend({name='senaki-cas-red', altitude=15000, expend=AI.Task.WeaponExpend.ONE}),
                presets.missions.attack.bai:extend({name='senaki-cas-red', altitude=10000, expend=AI.Task.WeaponExpend.ONE}),
                presets.missions.attack.strike:extend({name='senaki-strike-red', altitude=20000, expend=AI.Task.WeaponExpend.ALL}),
                presets.missions.patrol.aircraft:extend({name='senaki-patrol-red', altitude=25000, range=25}),
                presets.missions.patrol.aircraft:extend({name='senaki-patrol-red-2', altitude=20000, range=25})
            }
        })
    },
    [2] = 
    {
        presets.upgrades.basic.comPost:extend({
            name='senaki-compost-blue',
            products = {
                presets.special.blue.infantry:extend({ name='senaki-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='senaki-garrison-blue'})
            }
        }),
        presets.upgrades.supply.fuelTank:extend({
            name='senaki-fuel-blue',
            products = {
                presets.missions.supply.helo:extend({name='senaki-supply-blue-1'}),
                presets.missions.supply.helo:extend({name='senaki-supply-blue-2'}),
                presets.missions.supply.transfer:extend({name='senaki-transfer-blue'})
            }
        }),
        presets.upgrades.airdef.comCenter:extend({
            name='senaki-comcenter-blue',
            products = {
                presets.defenses.blue.shorad:extend({ name='senaki-airdef-blue'}),
                presets.missions.attack.sead:extend({name='senaki-sead-blue', altitude=25000, expend=AI.Task.WeaponExpend.ALL}),
                presets.missions.attack.cas:extend({name='senaki-cas-blue', altitude=15000, expend=AI.Task.WeaponExpend.ONE}),
                presets.missions.attack.bai:extend({name='senaki-cas-blue', altitude=10000, expend=AI.Task.WeaponExpend.ONE}),
                presets.missions.attack.strike:extend({name='senaki-strike-blue', altitude=20000, expend=AI.Task.WeaponExpend.TWO}),
                presets.missions.patrol.aircraft:extend({name='senaki-patrol-blue', altitude=25000, range=25})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Senaki.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Kutaisi.lua ]]-----------------

zones.kutaisi = ZoneCommand:new("Kutaisi")
zones.kutaisi.initialState = { side=1 }
zones.kutaisi.keepActive = true
zones.kutaisi.maxResource = 50000
zones.kutaisi:defineUpgrades({
    [1] = 
    {
        presets.upgrades.basic.comPost:extend({
            name='kutaisi-compost-red',
            products = {
                presets.special.red.infantry:extend({ name='kutaisi-defense-red'}),
				presets.defenses.red.infantry:extend({ name='kutaisi-garrison-red'})
            }
        }),
        presets.upgrades.supply.fuelTank:extend({
            name='kutaisi-fuel-red',
            products = {
                presets.missions.supply.helo:extend({name='kutaisi-supply-red-1'}),
                presets.missions.supply.helo:extend({name='kutaisi-supply-red-2'}),
                presets.missions.supply.transfer:extend({name='kutaisi-transfer-red'})
            }
        }),
        presets.upgrades.airdef.comCenter:extend({
            name='kutaisi-comcenter-red',
            products = {
                presets.defenses.red.shorad:extend({ name='kutaisi-airdef-red'}),
                presets.missions.attack.sead:extend({name='kutaisi-sead-red', altitude=25000, expend=AI.Task.WeaponExpend.ALL}),
                presets.missions.attack.cas:extend({name='kutaisi-cas-red', altitude=15000, expend=AI.Task.WeaponExpend.ONE}),
                presets.missions.attack.bai:extend({name='kutaisi-cas-red', altitude=10000, expend=AI.Task.WeaponExpend.ONE}),
                presets.missions.attack.strike:extend({name='kutaisi-strike-red', altitude=20000, expend=AI.Task.WeaponExpend.HALF}),
                presets.missions.patrol.aircraft:extend({name='kutaisi-patrol-red', altitude=25000, range=25}),
                presets.missions.patrol.aircraft:extend({name='kutaisi-patrol-red-2', altitude=25000, range=25})
            }
        })
    },
    [2] = 
    {
        presets.upgrades.basic.comPost:extend({
            name='kutaisi-compost-blue',
            products = {
                presets.special.blue.infantry:extend({ name='kutaisi-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='kutaisi-garrison-blue'})
            }
        }),
        presets.upgrades.supply.fuelTank:extend({
            name='kutaisi-fuel-blue',
            products = {
                presets.missions.supply.helo:extend({name='kutaisi-supply-blue-1'}),
                presets.missions.supply.helo:extend({name='kutaisi-supply-blue-2'}),
                presets.missions.supply.transfer:extend({name='kutaisi-transfer-blue'})
            }
        }),
        presets.upgrades.airdef.comCenter:extend({
            name='kutaisi-comcenter-blue',
            products = {
                presets.defenses.blue.shorad:extend({ name='kutaisi-airdef-blue'}),
                presets.missions.attack.sead:extend({name='kutaisi-sead-blue', altitude=25000, expend=AI.Task.WeaponExpend.ALL}),
                presets.missions.attack.cas:extend({name='kutaisi-cas-blue', altitude=15000, expend=AI.Task.WeaponExpend.ONE}),
                presets.missions.attack.bai:extend({name='kutaisi-cas-blue', altitude=10000, expend=AI.Task.WeaponExpend.ONE}),
                presets.missions.attack.strike:extend({name='kutaisi-strike-blue', altitude=20000, expend=AI.Task.WeaponExpend.TWO}),
                presets.missions.patrol.aircraft:extend({name='kutaisi-patrol-blue', altitude=25000, range=25})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Kutaisi.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Prohladniy.lua ]]-----------------

zones.prohladniy = ZoneCommand:new("Prohladniy")
zones.prohladniy.initialState = { side=1 }
zones.prohladniy:defineUpgrades({
    [1] = {
        presets.upgrades.basic.tent:extend({
            name='prohladniy-tent-red',
            products = {
                presets.special.red.infantry:extend({ name='prohladniy-defense-red'}),
				presets.defenses.red.infantry:extend({ name='prohladniy-garrison-red'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='prohladniy-fuel-red',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='prohladniy-supply-red'}),
                presets.missions.supply.transfer:extend({name='prohladniy-transfer-red'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='prohladniy-ammo-red',
            products = {
                presets.missions.attack.surface:extend({name='prohladniy-assault-red'})
            }
        })
    },
    [2] = {
        presets.upgrades.basic.tent:extend({
            name='prohladniy-tent-blue',
            products = {
                presets.special.blue.infantry:extend({ name='prohladniy-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='prohladniy-garrison-blue'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='prohladniy-fuel-blue',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='prohladniy-supply-blue'}),
                presets.missions.supply.transfer:extend({name='prohladniy-transfer-blue'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='prohladniy-ammo-blue',
            products = {
                presets.missions.attack.surface:extend({name='prohladniy-assault-blue'})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Prohladniy.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Tallyk.lua ]]-----------------

zones.tallyk = ZoneCommand:new("Tallyk")
zones.tallyk.initialState = { side=1 }
zones.tallyk.keepActive = true
zones.tallyk:defineUpgrades({
    [1] =  
    {
        presets.upgrades.basic.tent:extend({
            name='tallyk-tent-red',
            products = {
                presets.special.red.infantry:extend({ name='tallyk-defense-red'}),
				presets.defenses.red.infantry:extend({ name='tallyk-garrison-red'}),
                presets.missions.attack.surface:extend({name='tallyk-assault-red'})
            }
        }),
        presets.upgrades.airdef.comCenter:extend({
            name='tallyk-comcenter-red',
            products = {
                presets.defenses.red.sam:extend({ name='tallyk-sam-red'})
            }
        })
    },
    [2] = 
    {
        presets.upgrades.basic.tent:extend({
            name='tallyk-tent-blue',
            products = {
                presets.special.blue.infantry:extend({ name='tallyk-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='tallyk-garrison-blue'}),
                presets.missions.attack.surface:extend({name='tallyk-assault-blue'})
            }
        }),
        presets.upgrades.airdef.comCenter:extend({
            name='tallyk-comcenter-blue',
            products = {
                presets.defenses.blue.sam:extend({ name='tallyk-sam-blue'})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Tallyk.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Terek.lua ]]-----------------

zones.terek = ZoneCommand:new("Terek")
zones.terek.initialState = { side=1 }
zones.terek:defineUpgrades({
    [1] = {
        presets.upgrades.basic.tent:extend({
            name='terek-tent-red',
            products = {
                presets.special.red.infantry:extend({ name='terek-defense-red'}),
				presets.defenses.red.infantry:extend({ name='terek-garrison-red'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='terek-fuel-red',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='terek-supply-red'}),
                presets.missions.supply.transfer:extend({name='terek-transfer-red'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='terek-ammo-red',
            products = {
                presets.missions.attack.surface:extend({name='terek-assault-red'})
            }
        })
    },
    [2] = {
        presets.upgrades.basic.tent:extend({
            name='terek-tent-blue',
            products = {
                presets.special.blue.infantry:extend({ name='terek-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='terek-garrison-blue'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='terek-fuel-blue',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='terek-supply-blue'}),
                presets.missions.supply.transfer:extend({name='terek-transfer-blue'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='terek-ammo-blue',
            products = {
                presets.missions.attack.surface:extend({name='terek-assault-blue'})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Terek.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Humara.lua ]]-----------------

zones.humara = ZoneCommand:new("Humara")
zones.humara.initialState = { side=1 }
zones.humara:defineUpgrades({
    [1] = {
        presets.upgrades.basic.tent:extend({
            name='humara-tent-red',
            products = {
                presets.special.red.infantry:extend({ name='humara-defense-red'}),
				presets.defenses.red.infantry:extend({ name='humara-garrison-red'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='humara-fuel-red',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='humara-supply-red'}),
                presets.missions.supply.transfer:extend({name='humara-transfer-red'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='humara-ammo-red',
            products = {
                presets.missions.attack.surface:extend({name='humara-assault-red'})
            }
        })
    },
    [2] = {
        presets.upgrades.basic.tent:extend({
            name='humara-tent-blue',
            products = {
                presets.special.blue.infantry:extend({ name='humara-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='humara-garrison-blue'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='humara-fuel-blue',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='humara-supply-blue'}),
                presets.missions.supply.transfer:extend({name='humara-transfer-blue'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='humara-ammo-blue',
            products = {
                presets.missions.attack.surface:extend({name='humara-assault-blue'})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Humara.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Ochamchira.lua ]]-----------------

zones.ochamchira = ZoneCommand:new("Ochamchira")
zones.ochamchira.initialState = { side=1 }
zones.ochamchira:defineUpgrades({
    [1] = {
        presets.upgrades.basic.tent:extend({
            name='ochamchira-tent-red',
            products = {
                presets.special.red.infantry:extend({ name='ochamchira-defense-red'}),
				presets.defenses.red.infantry:extend({ name='ochamchira-garrison-red'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='ochamchira-fuel-red',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='ochamchira-supply-red'}),
                presets.missions.supply.transfer:extend({name='ochamchira-transfer-red'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='ochamchira-ammo-red',
            products = {
                presets.missions.attack.surface:extend({name='ochamchira-assault-red'})
            }
        })
    },
    [2] = {
        presets.upgrades.basic.tent:extend({
            name='ochamchira-tent-blue',
            products = {
                presets.special.blue.infantry:extend({ name='ochamchira-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='ochamchira-garrison-blue'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='ochamchira-fuel-blue',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='ochamchira-supply-blue'}),
                presets.missions.supply.transfer:extend({name='ochamchira-transfer-blue'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='ochamchira-ammo-blue',
            products = {
                presets.missions.attack.surface:extend({name='ochamchira-assault-blue'})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Ochamchira.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/November.lua ]]-----------------

zones.november = ZoneCommand:new("November")
zones.november.initialState = { side=1 }
zones.november.isHeloSpawn = true
zones.november:defineUpgrades({
    [1] = {
        presets.upgrades.basic.tent:extend({
            name='november-tent-red',
            products = {
                presets.special.red.infantry:extend({ name='november-defense-red'}),
				presets.defenses.red.infantry:extend({ name='november-garrison-red'})
            }
        }),
        presets.upgrades.supply.fuelTankFarp:extend({
            name='november-fuel-red',
            products = {
                presets.missions.supply.helo:extend({name='november-supply-red'}),
                presets.missions.supply.helo:extend({name='november-supply-red-1'}),
                presets.missions.supply.transfer:extend({name='november-transfer-red'})
            }
        }),
        presets.upgrades.airdef.comCenter:extend({
            name='november-comcenter-red',
            products = {
                presets.defenses.red.shorad:extend({name='november-sam-red'}),
                presets.missions.attack.helo:extend({name='november-cas-red', altitude=200, expend=AI.Task.WeaponExpend.HALF })
            }
        })
    },
    [2] = {
        presets.upgrades.basic.tent:extend({
            name='november-tent-blue',
            products = {
                presets.special.blue.infantry:extend({ name='november-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='november-garrison-blue'})
            }
        }),
        presets.upgrades.supply.fuelTankFarp:extend({
            name='november-fuel-blue',
            products = {
                presets.missions.supply.helo:extend({name='november-supply-blue'}),
                presets.missions.supply.helo:extend({name='november-supply-blue-1'}),
                presets.missions.supply.transfer:extend({name='november-transfer-blue'})
            }
        }),
        presets.upgrades.airdef.comCenter:extend({
            name='november-comcenter-blue',
            products = {
                presets.defenses.blue.shorad:extend({name='november-sam-blue'}),
                presets.missions.attack.helo:extend({name='november-cas-blue', altitude=200, expend=AI.Task.WeaponExpend.HALF })
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/November.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/XRay.lua ]]-----------------

zones.xray = ZoneCommand:new("XRay")
zones.xray.initialState = { side=1 }
zones.xray:defineUpgrades({
    [1] = {
        presets.upgrades.basic.tent:extend({
            name='xray-tent-red',
            products = {
                presets.special.red.infantry:extend({ name='xray-defense-red'}),
				presets.defenses.red.infantry:extend({ name='xray-garrison-red'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='xray-fuel-red',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='xray-supply-red'}),
                presets.missions.supply.helo:extend({name='xray-supply-red-2'}),
                presets.missions.supply.transfer:extend({name='xray-transfer-red'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='xray-ammo-red',
            products = {
                presets.missions.attack.surface:extend({name='xray-assault-red'})
            }
        })
    },
    [2] = {
        presets.upgrades.basic.tent:extend({
            name='xray-tent-blue',
            products = {
                presets.special.blue.infantry:extend({ name='xray-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='xray-garrison-blue'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='xray-fuel-blue',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='xray-supply-blue'}),
                presets.missions.supply.helo:extend({name='xray-supply-blue-2'}),
                presets.missions.supply.transfer:extend({name='xray-transfer-blue'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='xray-ammo-blue',
            products = {
                presets.missions.attack.surface:extend({name='xray-assault-blue'})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/XRay.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Whiskey.lua ]]-----------------

zones.whiskey = ZoneCommand:new("Whiskey")
zones.whiskey.initialState = { side=1 }
zones.whiskey:defineUpgrades({
    [1] = {
        presets.upgrades.basic.tent:extend({
            name='whiskey-tent-red',
            products = {
                presets.special.red.infantry:extend({ name='whiskey-defense-red'}),
				presets.defenses.red.infantry:extend({ name='whiskey-garrison-red'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='whiskey-fuel-red',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='whiskey-supply-red'}),
                presets.missions.supply.transfer:extend({name='whiskey-transfer-red'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='whiskey-ammo-red',
            products = {
                presets.missions.attack.surface:extend({name='whiskey-assault-red'})
            }
        })
    },
    [2] = {
        presets.upgrades.basic.tent:extend({
            name='whiskey-tent-blue',
            products = {
                presets.special.blue.infantry:extend({ name='whiskey-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='whiskey-garrison-blue'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='whiskey-fuel-blue',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='whiskey-supply-blue'}),
                presets.missions.supply.transfer:extend({name='whiskey-transfer-blue'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='whiskey-ammo-blue',
            products = {
                presets.missions.attack.surface:extend({name='whiskey-assault-blue'})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Whiskey.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Mine.lua ]]-----------------

zones.mine = ZoneCommand:new("Mine")
zones.mine.initialState = { side=1 }
zones.mine:defineUpgrades({
    [1] = 
    {
        presets.upgrades.basic.tent:extend({
            name='mine-tent-red',
            products = {
                presets.special.red.infantry:extend({ name='mine-defense-red'}),
				presets.defenses.red.infantry:extend({ name='mine-garrison-red'})
            }
        }),
        presets.upgrades.supply.excavator:extend({
            name='mine-excavator-red-1',
            products = {
                presets.missions.supply.convoy:extend({ name='mine-supply-red'}),
                presets.missions.supply.transfer:extend({name='mine-transfer-red'})
            }
        }),
        presets.upgrades.supply.excavator:extend({
            name='mine-excavator-red-2',
            products = {
                presets.missions.supply.convoy:extend({ name='mine-supply-red'}),
                presets.missions.supply.transfer:extend({name='mine-transfer-red'})
            }
        }),
        presets.upgrades.supply.excavator:extend({
            name='mine-excavator-red-3',
            products = {
                presets.missions.supply.convoy:extend({ name='mine-supply-red'}),
                presets.missions.supply.transfer:extend({name='mine-transfer-red'})
            }
        })
    },
    [2] = 
    {
        presets.upgrades.basic.tent:extend({
            name='mine-tent-blue',
            products = {
                presets.special.blue.infantry:extend({ name='mine-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='mine-garrison-blue'})
            }
        }),
        presets.upgrades.supply.excavator:extend({
            name='mine-excavator-blue-1',
            products = {
                presets.missions.supply.convoy:extend({ name='mine-supply-blue'}),
                presets.missions.supply.transfer:extend({name='mine-transfer-blue'})
            }
        }),
        presets.upgrades.supply.excavator:extend({
            name='mine-excavator-blue-2',
            products = {
                presets.missions.supply.convoy:extend({ name='mine-supply-blue'}),
                presets.missions.supply.transfer:extend({name='mine-transfer-blue'})
            }
        }),
        presets.upgrades.supply.excavator:extend({
            name='mine-excavator-blue-3',
            products = {
                presets.missions.supply.convoy:extend({ name='mine-supply-blue'}),
                presets.missions.supply.transfer:extend({name='mine-transfer-blue'})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Mine.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Papa.lua ]]-----------------

zones.papa = ZoneCommand:new("Papa")
zones.papa.initialState = { side=1 }
zones.papa.keepActive = true
zones.papa:defineUpgrades({
    [1] =  
    {
        presets.upgrades.basic.tent:extend({
            name='papa-tent-red',
            products = {
                presets.special.red.infantry:extend({ name='papa-defense-red'})
            }
        }),
        presets.upgrades.airdef.comCenter:extend({
            name='papa-comcenter-red',
            products = {
                presets.defenses.red.sam:extend({ name='papa-sam-red'})
            }
        })
    },
    [2] = 
    {
        presets.upgrades.basic.tent:extend({
            name='papa-tent-blue',
            products = {
                presets.special.blue.infantry:extend({ name='papa-defense-blue'})
            }
        }),
        presets.upgrades.airdef.comCenter:extend({
            name='papa-comcenter-blue',
            products = {
                presets.defenses.blue.sam:extend({ name='papa-sam-blue'})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Papa.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Sukhumi.lua ]]-----------------

zones.sukhumi = ZoneCommand:new("Sukhumi")
zones.sukhumi.initialState = { side=1 }
zones.sukhumi.keepActive = true
zones.sukhumi.maxResource = 50000
zones.sukhumi:defineUpgrades({
    [1] = 
    {
        presets.upgrades.basic.comPost:extend({
            name='sukhumi-compost-red',
            products = {
                presets.special.red.infantry:extend({ name='sukhumi-defense-red'}),
				presets.defenses.red.infantry:extend({ name='sukhumi-garrison-red'})
            }
        }),
        presets.upgrades.supply.fuelTank:extend({
            name='sukhumi-fuel-red',
            products = {
                presets.missions.supply.helo:extend({name='sukhumi-supply-red-1'}),
                presets.missions.supply.helo:extend({name='sukhumi-supply-red-2'}),
                presets.missions.supply.transfer:extend({name='sukhumi-transfer-red'})
            }
        }),
        presets.upgrades.airdef.comCenter:extend({
            name='sukhumi-comcenter-red',
            products = {
                presets.defenses.red.sa11:extend({ name='sukhumi-airdef-red'}),
                presets.missions.attack.sead:extend({name='sukhumi-sead-red', altitude=25000, expend=AI.Task.WeaponExpend.ALL}),
                presets.missions.attack.cas:extend({name='sukhumi-cas-red', altitude=15000, expend=AI.Task.WeaponExpend.ONE}),
                presets.missions.attack.bai:extend({name='sukhumi-cas-red', altitude=10000, expend=AI.Task.WeaponExpend.ONE}),
                presets.missions.attack.strike:extend({name='sukhumi-strike-red', altitude=20000, expend=AI.Task.WeaponExpend.ALL}),
                presets.missions.patrol.aircraft:extend({name='sukhumi-patrol-red', altitude=25000, range=25}),
                presets.missions.patrol.aircraft:extend({name='sukhumi-patrol-red-2', altitude=25000, range=25})
            }
        })
    },
    [2] = 
    {
        presets.upgrades.basic.comPost:extend({
            name='sukhumi-compost-blue',
            products = {
                presets.special.blue.infantry:extend({ name='sukhumi-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='sukhumi-garrison-blue'})
            }
        }),
        presets.upgrades.supply.fuelTank:extend({
            name='sukhumi-fuel-blue',
            products = {
                presets.missions.supply.helo:extend({name='sukhumi-supply-blue-1'}),
                presets.missions.supply.helo:extend({name='sukhumi-supply-blue-2'}),
                presets.missions.supply.transfer:extend({name='sukhumi-transfer-blue'})
            }
        }),
        presets.upgrades.airdef.comCenter:extend({
            name='sukhumi-comcenter-blue',
            products = {
                presets.defenses.blue.nasams:extend({ name='sukhumi-airdef-blue'}),
                presets.missions.attack.sead:extend({name='sukhumi-sead-blue', altitude=25000, expend=AI.Task.WeaponExpend.ALL}),
                presets.missions.attack.cas:extend({name='sukhumi-cas-blue', altitude=15000, expend=AI.Task.WeaponExpend.ONE}),
                presets.missions.attack.bai:extend({name='sukhumi-cas-blue', altitude=10000, expend=AI.Task.WeaponExpend.ONE}),
                presets.missions.attack.strike:extend({name='sukhumi-strike-blue', altitude=20000, expend=AI.Task.WeaponExpend.ALL}),
                presets.missions.patrol.aircraft:extend({name='sukhumi-patrol-blue', altitude=25000, range=25})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Sukhumi.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Farm.lua ]]-----------------

zones.farm = ZoneCommand:new("Farm")
zones.farm.initialState = { side=1 }
zones.farm:defineUpgrades({
    [1] = 
    {
        presets.upgrades.basic.tent:extend({
            name='farm-tent-red',
            products = {
                presets.special.red.infantry:extend({ name='farm-defense-red'}),
				presets.defenses.red.infantry:extend({ name='farm-garrison-red'})
            }
        }),
        presets.upgrades.supply.farm1:extend({
            name='farm-prod-red-1',
            products = {
                presets.missions.supply.convoy:extend({ name='farm-supply-red'}),
                presets.missions.supply.transfer:extend({name='farm-transfer-red'})
            }
        }),
        presets.upgrades.supply.farm2:extend({
            name='farm-prod-red-2',
            products = {
                presets.missions.supply.convoy:extend({ name='farm-supply-red'}),
                presets.missions.supply.transfer:extend({name='farm-transfer-red'})
            }
        })
    },
    [2] = 
    {
        presets.upgrades.basic.tent:extend({
            name='farm-tent-blue',
            products = {
                presets.special.blue.infantry:extend({ name='farm-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='farm-garrison-blue'})
            }
        }),
        presets.upgrades.supply.farm1:extend({
            name='farm-prod-blue-1',
            products = {
                presets.missions.supply.convoy:extend({ name='farm-supply-blue'}),
                presets.missions.supply.transfer:extend({name='farm-transfer-blue'})
            }
        }),
        presets.upgrades.supply.farm2:extend({
            name='farm-prod-blue-2',
            products = {
                presets.missions.supply.convoy:extend({ name='farm-supply-blue'}),
                presets.missions.supply.transfer:extend({name='farm-transfer-blue'})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Farm.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Romeo.lua ]]-----------------

zones.romeo = ZoneCommand:new("Romeo")
zones.romeo.initialState = { side=1 }
zones.romeo:defineUpgrades({
    [1] = {
        presets.upgrades.basic.tent:extend({
            name='romeo-tent-red',
            products = {
                presets.special.red.infantry:extend({ name='romeo-defense-red'}),
				presets.defenses.red.infantry:extend({ name='romeo-garrison-red'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='romeo-fuel-red',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='romeo-supply-red'}),
                presets.missions.supply.transfer:extend({name='romeo-transfer-red'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='romeo-ammo-red',
            products = {
                presets.missions.attack.surface:extend({name='romeo-assault-red'})
            }
        })
    },
    [2] = {
        presets.upgrades.basic.tent:extend({
            name='romeo-tent-blue',
            products = {
                presets.special.blue.infantry:extend({ name='romeo-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='romeo-garrison-blue'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='romeo-fuel-blue',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='romeo-supply-blue'}),
                presets.missions.supply.transfer:extend({name='romeo-transfer-blue'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='romeo-ammo-blue',
            products = {
                presets.missions.attack.surface:extend({name='romeo-assault-blue'})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Romeo.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Zulu.lua ]]-----------------

zones.zulu = ZoneCommand:new("Zulu")
zones.zulu.initialState = { side=1 }
zones.zulu:defineUpgrades({
    [1] = {
        presets.upgrades.basic.tent:extend({
            name='zulu-tent-red',
            products = {
                presets.special.red.infantry:extend({ name='zulu-defense-red'}),
				presets.defenses.red.infantry:extend({ name='zulu-garrison-red'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='zulu-fuel-red',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='zulu-supply-red'}),
                presets.missions.supply.transfer:extend({name='zulu-transfer-red'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='zulu-ammo-red',
            products = {
                presets.missions.attack.surface:extend({name='zulu-assault-red'})
            }
        })
    },
    [2] = {
        presets.upgrades.basic.tent:extend({
            name='zulu-tent-blue',
            products = {
                presets.special.blue.infantry:extend({ name='zulu-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='zulu-garrison-blue'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='zulu-fuel-blue',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='zulu-supply-blue'}),
                presets.missions.supply.transfer:extend({name='zulu-transfer-blue'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='zulu-ammo-blue',
            products = {
                presets.missions.attack.surface:extend({name='zulu-assault-blue'})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Zulu.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Yankee.lua ]]-----------------

zones.yankee = ZoneCommand:new("Yankee")
zones.yankee.initialState = { side=1 }
zones.yankee:defineUpgrades({
    [1] = {
        presets.upgrades.basic.tent:extend({
            name='yankee-tent-red',
            products = {
                presets.special.red.infantry:extend({ name='yankee-defense-red'}),
				presets.defenses.red.infantry:extend({ name='yankee-garrison-red'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='yankee-fuel-red',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='yankee-supply-red'}),
                presets.missions.supply.transfer:extend({name='yankee-transfer-red'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='yankee-ammo-red',
            products = {
                presets.missions.attack.surface:extend({name='yankee-assault-red'})
            }
        })
    },
    [2] = {
        presets.upgrades.basic.tent:extend({
            name='yankee-tent-blue',
            products = {
                presets.special.blue.infantry:extend({ name='yankee-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='yankee-garrison-blue'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='yankee-fuel-blue',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='yankee-supply-blue'}),
                presets.missions.supply.transfer:extend({name='yankee-transfer-blue'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='yankee-ammo-blue',
            products = {
                presets.missions.attack.surface:extend({name='yankee-assault-blue'})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Yankee.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Malgobek.lua ]]-----------------

zones.malgobek = ZoneCommand:new("Malgobek")
zones.malgobek.initialState = { side=1 }
zones.malgobek:defineUpgrades({
    [1] = {
        presets.upgrades.basic.tent:extend({
            name='malgobek-tent-red',
            products = {
                presets.special.red.infantry:extend({ name='malgobek-defense-red'}),
				presets.defenses.red.infantry:extend({ name='malgobek-garrison-red'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='malgobek-fuel-red',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='malgobek-supply-red'}),
                presets.missions.supply.transfer:extend({name='malgobek-transfer-red'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='malgobek-ammo-red',
            products = {
                presets.missions.attack.surface:extend({name='malgobek-assault-red'})
            }
        })
    },
    [2] = {
        presets.upgrades.basic.tent:extend({
            name='malgobek-tent-blue',
            products = {
                presets.special.blue.infantry:extend({ name='malgobek-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='malgobek-garrison-blue'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='malgobek-fuel-blue',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='malgobek-supply-blue'}),
                presets.missions.supply.transfer:extend({name='malgobek-transfer-blue'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='malgobek-ammo-blue',
            products = {
                presets.missions.attack.surface:extend({name='malgobek-assault-blue'})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Malgobek.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Kilo.lua ]]-----------------

zones.kilo = ZoneCommand:new("Kilo")
zones.kilo.initialState = { side=1 }
zones.kilo:defineUpgrades({
    [1] = {
        presets.upgrades.basic.tent:extend({
            name='kilo-tent-red',
            products = {
                presets.special.red.infantry:extend({ name='kilo-defense-red'}),
				presets.defenses.red.infantry:extend({ name='kilo-garrison-red'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='kilo-fuel-red',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='kilo-supply-red'}),
                presets.missions.supply.transfer:extend({name='kilo-transfer-red'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='kilo-ammo-red',
            products = {
                presets.missions.attack.surface:extend({name='kilo-assault-red'})
            }
        })
    },
    [2] = {
        presets.upgrades.basic.tent:extend({
            name='kilo-tent-blue',
            products = {
                presets.special.blue.infantry:extend({ name='kilo-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='kilo-garrison-blue'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='kilo-fuel-blue',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='kilo-supply-blue'}),
                presets.missions.supply.transfer:extend({name='kilo-transfer-blue'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='kilo-ammo-blue',
            products = {
                presets.missions.attack.surface:extend({name='kilo-assault-blue'})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Kilo.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Quebec.lua ]]-----------------

zones.quebec = ZoneCommand:new("Quebec")
zones.quebec.initialState = { side=1 }
zones.quebec.keepActive = true
zones.quebec:defineUpgrades({
    [1] =  
    {
        presets.upgrades.basic.tent:extend({
            name='quebec-tent-red',
            products = {
                presets.special.red.infantry:extend({ name='quebec-defense-red'})
            }
        }),
        presets.upgrades.airdef.comCenter:extend({
            name='quebec-comcenter-red',
            products = {
                presets.defenses.red.sam:extend({ name='quebec-sam-red'})
            }
        })
    },
    [2] = 
    {
        presets.upgrades.basic.tent:extend({
            name='quebec-tent-blue',
            products = {
                presets.special.blue.infantry:extend({ name='quebec-defense-blue'})
            }
        }),
        presets.upgrades.airdef.comCenter:extend({
            name='quebec-comcenter-blue',
            products = {
                presets.defenses.blue.sam:extend({ name='quebec-sam-blue'})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Quebec.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/OilFields.lua ]]-----------------

zones.oilfields = ZoneCommand:new("Oil Fields")
zones.oilfields.initialState = { side=1 }
zones.oilfields:defineUpgrades({
    [1] = {
        presets.upgrades.basic.outpost:extend({
            name='oilfields-outpost-red',
            products = {
                presets.special.red.infantry:extend({ name='oilfields-defense-red'}),
				presets.defenses.red.infantry:extend({ name='oilfields-garrison-red'})
            }
        }),
        presets.upgrades.supply.oilPump:extend({
            name='oilfields-pump-red-1',
            products = {
                presets.missions.supply.transfer:extend({name='oilfields-transfer-red1'})
            }
        }),
        presets.upgrades.supply.oilPump:extend({
            name='oilfields-pump-red-2',
            products = {
                presets.missions.supply.convoy:extend({name='oilfields-supply-red-1'})
            }
        }),
        presets.upgrades.supply.oilPump:extend({
            name='oilfields-pump-red-3',
            products = {
                presets.missions.supply.transfer:extend({name='oilfields-transfer-red2'})
            }
        }),
        presets.upgrades.supply.oilPump:extend({
            name='oilfields-pump-red-4',
            products = {
                presets.missions.supply.convoy:extend({name='oilfields-supply-red-2'})
            }
        })
    },
    [2] = {
        presets.upgrades.basic.outpost:extend({
            name='oilfields-outpost-blue',
            products = {
                presets.special.blue.infantry:extend({ name='oilfields-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='oilfields-garrison-blue'})
            }
        }),
        presets.upgrades.supply.oilPump:extend({
            name='oilfields-pump-blue-1',
            products = {
                presets.missions.supply.transfer:extend({name='oilfields-transfer-blue1'})
            }
        }),
        presets.upgrades.supply.oilPump:extend({
            name='oilfields-pump-blue-2',
            products = {
                presets.missions.supply.convoy:extend({name='oilfields-supply-blue-1'})
            }
        }),
        presets.upgrades.supply.oilPump:extend({
            name='oilfields-pump-blue-3',
            products = {
                presets.missions.supply.transfer:extend({name='oilfields-transfer-blue2'})
            }
        }),
        presets.upgrades.supply.oilPump:extend({
            name='oilfields-pump-blue-4',
            products = {
                presets.missions.supply.convoy:extend({name='oilfields-supply-blue-2'})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/OilFields.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Echo.lua ]]-----------------

zones.echo = ZoneCommand:new("Echo")
zones.echo.initialState = { side=2 }
zones.echo:defineUpgrades({
    [1] = {
        presets.upgrades.basic.tent:extend({
            name='echo-tent-red',
            products = {
                presets.special.red.infantry:extend({ name='echo-defense-red'}),
				presets.defenses.red.infantry:extend({ name='echo-garrison-red'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='echo-fuel-red',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='echo-supply-red'}),
                presets.missions.supply.transfer:extend({name='echo-transfer-red'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='echo-ammo-red',
            products = {
                presets.missions.attack.surface:extend({name='echo-assault-red'})
            }
        })
    },
    [2] = {
        presets.upgrades.basic.tent:extend({
            name='echo-tent-blue',
            products = {
                presets.special.blue.infantry:extend({ name='echo-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='echo-garrison-blue'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='echo-fuel-blue',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='echo-supply-blue'}),
                presets.missions.supply.transfer:extend({name='echo-transfer-blue'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='echo-ammo-blue',
            products = {
                presets.missions.attack.surface:extend({name='echo-assault-blue'})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Echo.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Kobuleti.lua ]]-----------------

zones.kobuleti = ZoneCommand:new("Kobuleti")
zones.kobuleti.initialState = { side=2 }
zones.kobuleti.keepActive = true
zones.kobuleti.isHeloSpawn = true
zones.kobuleti.isPlaneSpawn = true
zones.kobuleti.maxResource = 50000
zones.kobuleti:defineUpgrades({
    [1] = 
    {
        presets.upgrades.basic.comPost:extend({
            name='kobuleti-compost-red',
            products = {
                presets.special.red.infantry:extend({ name='kobuleti-defense-red'}),
				presets.defenses.red.infantry:extend({ name='kobuleti-garrison-red'}),
                presets.missions.attack.surface:extend({ name='kobuleti-assault-red'})
            }
        }),
        presets.upgrades.supply.fuelTank:extend({
            name='kobuleti-fuel-red',
            products = {
                presets.missions.supply.helo:extend({name='kobuleti-supply-red-1'}),
                presets.missions.supply.helo:extend({name='kobuleti-supply-red-2'}),
                presets.missions.supply.transfer:extend({name='kobuleti-transfer-red'})
            }
        }),
        presets.upgrades.airdef.comCenter:extend({
            name='kobuleti-comcenter-red',
            products = {
                presets.defenses.red.shorad:extend({ name='kobuleti-airdef-red'}),
                presets.missions.attack.sead:extend({name='kobuleti-sead-red', altitude=25000, expend=AI.Task.WeaponExpend.ALL}),
                presets.missions.attack.cas:extend({name='kobuleti-cas-red', altitude=15000, expend=AI.Task.WeaponExpend.ONE}),
                presets.missions.attack.bai:extend({name='kobuleti-cas-red', altitude=10000, expend=AI.Task.WeaponExpend.ONE}),
                presets.missions.attack.strike:extend({name='kobuleti-strike-red', altitude=20000, expend=AI.Task.WeaponExpend.ALL}),
                presets.missions.patrol.aircraft:extend({name='kobuleti-patrol-red', altitude=25000, range=25})
            }
        })
    },
    [2] = 
    {
        presets.upgrades.basic.comPost:extend({
            name='kobuleti-compost-blue',
            products = {
                presets.special.blue.infantry:extend({ name='kobuleti-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='kobuleti-garrison-blue'}),
                presets.missions.attack.surface:extend({ name='kobuleti-assault-blue'})
            }
        }),
        presets.upgrades.supply.fuelTank:extend({
            name='kobuleti-fuel-blue',
            products = {
                presets.missions.supply.helo:extend({name='kobuleti-supply-blue-1'}),
                presets.missions.supply.helo:extend({name='kobuleti-supply-blue-2'}),
                presets.missions.supply.transfer:extend({name='kobuleti-transfer-blue'})
            }
        }),
        presets.upgrades.airdef.comCenter:extend({
            name='kobuleti-comcenter-blue',
            products = {
                presets.defenses.blue.shorad:extend({ name='kobuleti-airdef-blue'}),
                presets.missions.attack.sead:extend({name='kobuleti-sead-blue', altitude=25000, expend=AI.Task.WeaponExpend.ALL}),
                presets.missions.attack.cas:extend({name='kobuleti-cas-blue', altitude=15000, expend=AI.Task.WeaponExpend.ONE}),
                presets.missions.attack.bai:extend({name='kobuleti-cas-blue', altitude=10000, expend=AI.Task.WeaponExpend.ONE}),
                presets.missions.attack.strike:extend({name='kobuleti-strike-blue', altitude=20000, expend=AI.Task.WeaponExpend.TWO}),
                presets.missions.patrol.aircraft:extend({name='kobuleti-patrol-blue', altitude=25000, range=25}),
                presets.missions.support.awacs:extend({name='kobuleti-awacs-blue', altitude=30000, freq=258.5}),
                presets.missions.support.tanker:extend({name='kobuleti-tanker-blue', altitude=23000, freq=258, tacan='38', variant='Boom'})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Kobuleti.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Alpha.lua ]]-----------------

zones.alpha = ZoneCommand:new('Alpha')
zones.alpha.initialState = { side=2 }
zones.alpha:defineUpgrades({
    [1] = --red side
    {
        presets.upgrades.basic.tent:extend({ 
            name = 'alpha-tent-red',
            products = {
                presets.special.red.infantry:extend({ name='alpha-defense-red'}),
				presets.defenses.red.infantry:extend({ name='alpha-garrison-red'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({ 
            name = 'alpha-fuel-red',
            products = {
                presets.missions.supply.convoy_escorted:extend({ name='alpha-supply-red'}),
                presets.missions.supply.transfer:extend({name='alpha-transfer-red'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({ 
            name = 'alpha-ammo-red',
            products = {
                presets.missions.attack.surface:extend({ name='alpha-assault-red'})
            }
        })
    },
    [2] = --blue side
    {	
        presets.upgrades.basic.tent:extend({ 
            name = 'alpha-tent-blue',
            products = {
                presets.special.blue.infantry:extend({ name='alpha-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='alpha-garrison-blue'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({ 
            name = 'alpha-fuel-blue',
            products = {
                presets.missions.supply.convoy_escorted:extend({ name='alpha-supply-blue'}),
                presets.missions.supply.transfer:extend({name='alpha-transfer-blue'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({ 
            name = 'alpha-ammo-blue',
            products = {
                presets.missions.attack.surface:extend({ name='alpha-assault-blue'})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Alpha.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Foxtrot.lua ]]-----------------

zones.foxtrot = ZoneCommand:new("Foxtrot")
zones.foxtrot.initialState = { side=2 }
zones.foxtrot:defineUpgrades({
    [1] = {
        presets.upgrades.basic.tent:extend({
            name='foxtrot-tent-red',
            products = {
                presets.special.red.infantry:extend({ name='foxtrot-defense-red'}),
				presets.defenses.red.infantry:extend({ name='foxtrot-garrison-red'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='foxtrot-fuel-red',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='foxtrot-supply-red'}),
                presets.missions.supply.transfer:extend({name='foxtrot-transfer-red'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='foxtrot-ammo-red',
            products = {
                presets.missions.attack.surface:extend({name='foxtrot-assault-red'})
            }
        })
    },
    [2] = {
        presets.upgrades.basic.tent:extend({
            name='foxtrot-tent-blue',
            products = {
                presets.special.blue.infantry:extend({ name='foxtrot-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='foxtrot-garrison-blue'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='foxtrot-fuel-blue',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='foxtrot-supply-blue'}),
                presets.missions.supply.transfer:extend({name='foxtrot-transfer-blue'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='foxtrot-ammo-blue',
            products = {
                presets.missions.attack.surface:extend({name='foxtrot-assault-blue'})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Foxtrot.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Sierra.lua ]]-----------------

zones.sierra = ZoneCommand:new("Sierra")
zones.sierra.initialState = { side=1 }
zones.sierra.isHeloSpawn = true
zones.sierra:defineUpgrades({
    [1] = {
        presets.upgrades.basic.tent:extend({
            name='sierra-tent-red',
            products = {
                presets.special.red.infantry:extend({ name='sierra-defense-red'}),
				presets.defenses.red.infantry:extend({ name='sierra-garrison-red'})
            }
        }),
        presets.upgrades.supply.fuelTankFarp:extend({
            name='sierra-fuel-red',
            products = {
                presets.missions.supply.helo:extend({name='sierra-supply-red'}),
                presets.missions.supply.helo:extend({name='sierra-supply-red-1'}),
                presets.missions.supply.transfer:extend({name='sierra-transfer-red'})
            }
        }),
        presets.upgrades.airdef.comCenter:extend({
            name='sierra-comcenter-red',
            products = {
                presets.defenses.red.shorad:extend({name='sierra-sam-red'}),
                presets.missions.attack.helo:extend({name='sierra-cas-red', altitude=200, expend=AI.Task.WeaponExpend.HALF })
            }
        })
    },
    [2] = {
        presets.upgrades.basic.tent:extend({
            name='sierra-tent-blue',
            products = {
                presets.special.blue.infantry:extend({ name='sierra-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='sierra-garrison-blue'})
            }
        }),
        presets.upgrades.supply.fuelTankFarp:extend({
            name='sierra-fuel-blue',
            products = {
                presets.missions.supply.helo:extend({name='sierra-supply-blue'}),
                presets.missions.supply.helo:extend({name='sierra-supply-blue-1'}),
                presets.missions.supply.transfer:extend({name='sierra-transfer-blue'})
            }
        }),
        presets.upgrades.airdef.comCenter:extend({
            name='sierra-comcenter-blue',
            products = {
                presets.defenses.blue.shorad:extend({name='sierra-sam-blue'}),
                presets.missions.attack.helo:extend({name='sierra-cas-blue', altitude=200, expend=AI.Task.WeaponExpend.HALF })
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Sierra.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Oni.lua ]]-----------------

zones.oni = ZoneCommand:new("Oni")
zones.oni.initialState = { side=1 }
zones.oni:defineUpgrades({
    [1] = {
        presets.upgrades.basic.tent:extend({
            name='oni-tent-red',
            products = {
                presets.special.red.infantry:extend({ name='oni-defense-red'}),
				presets.defenses.red.infantry:extend({ name='oni-garrison-red'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='oni-fuel-red',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='oni-supply-red'}),
                presets.missions.supply.helo:extend({name='oni-supply-red-2'}),
                presets.missions.supply.transfer:extend({name='oni-transfer-red'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='oni-ammo-red',
            products = {
                presets.missions.attack.surface:extend({name='oni-assault-red'})
            }
        })
    },
    [2] = {
        presets.upgrades.basic.tent:extend({
            name='oni-tent-blue',
            products = {
                presets.special.blue.infantry:extend({ name='oni-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='oni-garrison-blue'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='oni-fuel-blue',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='oni-supply-blue'}),
                presets.missions.supply.helo:extend({name='oni-supply-blue-2'}),
                presets.missions.supply.transfer:extend({name='oni-transfer-blue'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='oni-ammo-blue',
            products = {
                presets.missions.attack.surface:extend({name='oni-assault-blue'})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Oni.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Hotel.lua ]]-----------------

zones.hotel = ZoneCommand:new("Hotel")
zones.hotel.initialState = nil
zones.hotel:defineUpgrades({
    [1] = {
        presets.upgrades.basic.tent:extend({
            name='hotel-tent-red',
            products = {
                presets.special.red.infantry:extend({ name='hotel-defense-red'}),
				presets.defenses.red.infantry:extend({ name='hotel-garrison-red'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='hotel-fuel-red',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='hotel-supply-red'}),
                presets.missions.supply.transfer:extend({name='hotel-transfer-red'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='hotel-ammo-red',
            products = {
                presets.missions.attack.surface:extend({name='hotel-assault-red'})
            }
        })
    },
    [2] = {
        presets.upgrades.basic.tent:extend({
            name='hotel-tent-blue',
            products = {
                presets.special.blue.infantry:extend({ name='hotel-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='hotel-garrison-blue'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='hotel-fuel-blue',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='hotel-supply-blue'}),
                presets.missions.supply.transfer:extend({name='hotel-transfer-blue'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='hotel-ammo-blue',
            products = {
                presets.missions.attack.surface:extend({name='hotel-assault-blue'})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Hotel.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Victor.lua ]]-----------------

zones.victor = ZoneCommand:new("Victor")
zones.victor.initialState = { side=1 }
zones.victor:defineUpgrades({
    [1] = {
        presets.upgrades.basic.tent:extend({
            name='victor-tent-red',
            products = {
                presets.special.red.infantry:extend({ name='victor-defense-red'}),
				presets.defenses.red.infantry:extend({ name='victor-garrison-red'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='victor-fuel-red',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='victor-supply-red'}),
                presets.missions.supply.helo:extend({name='victor-supply-red-2'}),
                presets.missions.supply.transfer:extend({name='victor-transfer-red'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='victor-ammo-red',
            products = {
                presets.missions.attack.surface:extend({name='victor-assault-red'})
            }
        })
    },
    [2] = {
        presets.upgrades.basic.tent:extend({
            name='victor-tent-blue',
            products = {
                presets.special.blue.infantry:extend({ name='victor-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='victor-garrison-blue'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='victor-fuel-blue',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='victor-supply-blue'}),
                presets.missions.supply.helo:extend({name='victor-supply-blue-2'}),
                presets.missions.supply.transfer:extend({name='victor-transfer-blue'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='victor-ammo-blue',
            products = {
                presets.missions.attack.surface:extend({name='victor-assault-blue'})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Victor.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Tango.lua ]]-----------------

zones.tango = ZoneCommand:new("Tango")
zones.tango.initialState = { side=1 }
zones.tango.isHeloSpawn = true
zones.tango:defineUpgrades({
    [1] = {
        presets.upgrades.basic.tent:extend({
            name='tango-tent-red',
            products = {
                presets.special.red.infantry:extend({ name='tango-defense-red'}),
				presets.defenses.red.infantry:extend({ name='tango-garrison-red'})
            }
        }),
        presets.upgrades.supply.fuelTankFarp:extend({
            name='tango-fuel-red',
            products = {
                presets.missions.supply.helo:extend({name='tango-supply-red'}),
                presets.missions.supply.helo:extend({name='tango-supply-red-1'}),
                presets.missions.supply.transfer:extend({name='tango-transfer-red'})
            }
        }),
        presets.upgrades.airdef.comCenter:extend({
            name='tango-comcenter-red',
            products = {
                presets.defenses.red.shorad:extend({name='tango-sam-red'}),
                presets.missions.attack.helo:extend({name='tango-cas-red', altitude=200, expend=AI.Task.WeaponExpend.HALF })
            }
        })
    },
    [2] = {
        presets.upgrades.basic.tent:extend({
            name='tango-tent-blue',
            products = {
                presets.special.blue.infantry:extend({ name='tango-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='tango-garrison-blue'})
            }
        }),
        presets.upgrades.supply.fuelTankFarp:extend({
            name='tango-fuel-blue',
            products = {
                presets.missions.supply.helo:extend({name='tango-supply-blue'}),
                presets.missions.supply.helo:extend({name='tango-supply-blue-1'}),
                presets.missions.supply.transfer:extend({name='tango-transfer-blue'})
            }
        }),
        presets.upgrades.airdef.comCenter:extend({
            name='tango-comcenter-blue',
            products = {
                presets.defenses.blue.shorad:extend({name='tango-sam-blue'}),
                presets.missions.attack.helo:extend({name='tango-cas-blue', altitude=200, expend=AI.Task.WeaponExpend.HALF })
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Tango.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Unal.lua ]]-----------------

zones.unal = ZoneCommand:new("Unal")
zones.unal.initialState = { side=1 }
zones.unal.isHeloSpawn = true
zones.unal:defineUpgrades({
    [1] = {
        presets.upgrades.basic.tent:extend({
            name='unal-tent-red',
            products = {
                presets.special.red.infantry:extend({ name='unal-defense-red'}),
				presets.defenses.red.infantry:extend({ name='unal-garrison-red'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='unal-fuel-red',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='unal-supply-red'}),
                presets.missions.supply.helo:extend({name='unal-supply-red-2'}),
                presets.missions.supply.transfer:extend({name='unal-transfer-red'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='unal-ammo-red',
            products = {
                presets.missions.attack.surface:extend({name='unal-assault-red'})
            }
        })
    },
    [2] = {
        presets.upgrades.basic.tent:extend({
            name='unal-tent-blue',
            products = {
                presets.special.blue.infantry:extend({ name='unal-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='unal-garrison-blue'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='unal-fuel-blue',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='unal-supply-blue'}),
                presets.missions.supply.helo:extend({name='unal-supply-blue-2'}),
                presets.missions.supply.transfer:extend({name='unal-transfer-blue'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='unal-ammo-blue',
            products = {
                presets.missions.attack.surface:extend({name='unal-assault-blue'})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Unal.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Beslan.lua ]]-----------------

zones.beslan = ZoneCommand:new("Beslan")
zones.beslan.initialState = { side=1 }
zones.beslan.keepActive = true
zones.beslan.maxResource = 50000
zones.beslan:defineUpgrades({
    [1] = 
    {
        presets.upgrades.basic.comPost:extend({
            name='beslan-compost-red',
            products = {
                presets.special.red.infantry:extend({ name='beslan-defense-red'}),
				presets.defenses.red.infantry:extend({ name='beslan-garrison-red'})
            }
        }),
        presets.upgrades.supply.fuelTank:extend({
            name='beslan-fuel-red',
            products = {
                presets.missions.supply.helo:extend({name='beslan-supply-red-1'}),
                presets.missions.supply.helo:extend({name='beslan-supply-red-2'}),
                presets.missions.supply.convoy_escorted:extend({name='beslan-supply-red-3'}),
                presets.missions.supply.transfer:extend({name='beslan-transfer-red'})
            }
        }),
        presets.upgrades.airdef.comCenter:extend({
            name='beslan-comcenter-red',
            products = {
                presets.defenses.red.sa5:extend({ name='beslan-airdef-red'}),
                presets.missions.attack.sead:extend({name='beslan-sead-red', altitude=25000, expend=AI.Task.WeaponExpend.ALL}),
                presets.missions.attack.strike:extend({name='beslan-strike-red', altitude=30000, expend=AI.Task.WeaponExpend.ALL}),
                presets.missions.attack.strike:extend({name='beslan-strike-red-1', altitude=30000, expend=AI.Task.WeaponExpend.ALL}),
                presets.missions.patrol.aircraft:extend({name='beslan-patrol-red', altitude=25000, range=25})
            }
        })
    },
    [2] = 
    {
        presets.upgrades.basic.comPost:extend({
            name='beslan-compost-blue',
            products = {
                presets.special.blue.infantry:extend({ name='beslan-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='beslan-garrison-blue'})
            }
        }),
        presets.upgrades.supply.fuelTank:extend({
            name='beslan-fuel-blue',
            products = {
                presets.missions.supply.helo:extend({name='beslan-supply-blue-1'}),
                presets.missions.supply.helo:extend({name='beslan-supply-blue-2'}),
                presets.missions.supply.convoy_escorted:extend({name='beslan-supply-blue-3'}),
                presets.missions.supply.transfer:extend({name='beslan-transfer-blue'})
            }
        }),
        presets.upgrades.airdef.comCenter:extend({
            name='beslan-comcenter-blue',
            products = {
                presets.defenses.blue.patriot:extend({ name='beslan-airdef-blue'}),
                presets.missions.attack.sead:extend({name='beslan-sead-blue', altitude=25000, expend=AI.Task.WeaponExpend.ALL}),
                presets.missions.attack.strike:extend({name='beslan-strike-blue', altitude=30000, expend=AI.Task.WeaponExpend.ALL}),
                presets.missions.attack.strike:extend({name='beslan-strike-blue-1', altitude=30000, expend=AI.Task.WeaponExpend.ALL}),
                presets.missions.patrol.aircraft:extend({name='beslan-patrol-blue', altitude=25000, range=25})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Beslan.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Bravo.lua ]]-----------------

zones.bravo = ZoneCommand:new("Bravo")
zones.bravo.initialState = { side=2 }
zones.bravo:defineUpgrades({
    [1] = 
    {
        presets.upgrades.basic.comPost:extend({
            name='bravo-compost-red',
            products = {
                presets.special.red.infantry:extend({ name='bravo-defense-red'}),
				presets.defenses.red.infantry:extend({ name='bravo-garrison-red'})
            }
        }),
        presets.upgrades.supply.fuelTankFarp:extend({
            name='bravo-fuel-red',
            products = {
                presets.missions.supply.convoy_escorted:extend({ name='bravo-supply-red'}),
                presets.missions.supply.transfer:extend({name='bravo-transfer-red'})
            }
        }),
        presets.upgrades.airdef.comCenter:extend({
            name='bravo-comcenter-red',
            products = {
                presets.defenses.red.shorad:extend({ name='bravo-airdef-red'}),
                presets.missions.attack.helo:extend({name='bravo-attack-red', altitude=200, expend=AI.Task.WeaponExpend.HALF})
            }
        })
    },
    [2] = 
    {
        presets.upgrades.basic.comPost:extend({
            name='bravo-compost-blue',
            products = {
                presets.special.blue.infantry:extend({ name='bravo-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='bravo-garrison-blue'})
            }
        }),
        presets.upgrades.supply.fuelTankFarp:extend({
            name='bravo-fuel-blue',
            products = {
                presets.missions.supply.convoy_escorted:extend({ name='bravo-supply-blue'}),
                presets.missions.supply.transfer:extend({name='bravo-transfer-blue'})
            }
        }),
        presets.upgrades.airdef.comCenter:extend({
            name='bravo-comcenter-blue',
            products = {
                presets.defenses.blue.shorad:extend({ name='bravo-airdef-blue'}),
                presets.missions.attack.helo:extend({name='bravo-attack-blue', altitude=200, expend=AI.Task.WeaponExpend.HALF })
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Bravo.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/WeaponDepot.lua ]]-----------------

zones.weapondepot = ZoneCommand:new("Weapon Depot")
zones.weapondepot.initialState = { side=1 }
zones.weapondepot:defineUpgrades({
    [1] = {
        presets.upgrades.basic.tent:extend({
            name='weapons-tent-red',
            products = {
                presets.special.red.infantry:extend({ name='weapons-defense-red'}),
				presets.defenses.red.infantry:extend({ name='weapons-garrison-red'})
            }
        }),
        presets.upgrades.supply.ammoDepot:extend({
            name='weapons-ammo-red-1',
            products = {
                presets.missions.supply.convoy:extend({name='weapons-supply-red-1'}),
                presets.missions.supply.transfer:extend({name='weapons-transfer-red-1'})
            }
        }),
        presets.upgrades.supply.ammoDepot:extend({
            name='weapons-ammo-red-2',
            products = {
                presets.missions.supply.convoy:extend({name='weapons-supply-red-2'}),
                presets.missions.supply.transfer:extend({name='weapons-transfer-red-2'})
            }
        })
    },
    [2] = {
        presets.upgrades.basic.tent:extend({
            name='weapons-tent-blue',
            products = {
                presets.special.blue.infantry:extend({ name='weapons-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='weapons-garrison-blue'})
            }
        }),
        presets.upgrades.supply.ammoDepot:extend({
            name='weapons-ammo-blue-1',
            products = {
                presets.missions.supply.convoy:extend({name='weapons-supply-blue-1'}),
                presets.missions.supply.transfer:extend({name='weapons-transfer-blue-1'})
            }
        }),
        presets.upgrades.supply.ammoDepot:extend({
            name='weapons-ammo-blue-2',
            products = {
                presets.missions.supply.convoy:extend({name='weapons-supply-blue-2'}),
                presets.missions.supply.transfer:extend({name='weapons-transfer-blue-2'})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/WeaponDepot.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Delta.lua ]]-----------------

zones.delta = ZoneCommand:new("Delta")
zones.delta.initialState = { side=2 }
zones.delta:defineUpgrades({
    [1] = {
        presets.upgrades.basic.tent:extend({
            name='delta-tent-red',
            products = {
                presets.special.red.infantry:extend({ name='delta-defense-red'}),
				presets.defenses.red.infantry:extend({ name='delta-garrison-red'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='delta-fuel-red',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='delta-supply-red'}),
                presets.missions.supply.transfer:extend({name='delta-transfer-red'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='delta-ammo-red',
            products = {
                presets.missions.attack.surface:extend({name='delta-assault-red'})
            }
        })
    },
    [2] = {
        presets.upgrades.basic.tent:extend({
            name='delta-tent-blue',
            products = {
                presets.special.blue.infantry:extend({ name='delta-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='delta-garrison-blue'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='delta-fuel-blue',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='delta-supply-blue'}),
                presets.missions.supply.transfer:extend({name='delta-transfer-blue'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='delta-ammo-blue',
            products = {
                presets.missions.attack.surface:extend({name='delta-assault-blue'})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Delta.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Cherkessk.lua ]]-----------------

zones.cherkessk = ZoneCommand:new("Cherkessk")
zones.cherkessk.initialState = { side=1 }
zones.cherkessk.isHeloSpawn = true
zones.cherkessk:defineUpgrades({
    [1] = {
        presets.upgrades.basic.tent:extend({
            name='cherkessk-tent-red',
            products = {
                presets.special.red.infantry:extend({ name='cherkessk-defense-red'}),
				presets.defenses.red.infantry:extend({ name='cherkessk-garrison-red'})
            }
        }),
        presets.upgrades.supply.fuelTankFarp:extend({
            name='cherkessk-fuel-red',
            products = {
                presets.missions.supply.helo:extend({name='cherkessk-supply-red'}),
                presets.missions.supply.helo:extend({name='cherkessk-supply-red-1'}),
                presets.missions.supply.transfer:extend({name='cherkessk-transfer-red'})
            }
        }),
        presets.upgrades.airdef.comCenter:extend({
            name='cherkessk-comcenter-red',
            products = {
                presets.defenses.red.shorad:extend({name='cherkessk-sam-red'}),
                presets.missions.attack.helo:extend({name='cherkessk-cas-red', altitude=200, expend=AI.Task.WeaponExpend.HALF }),
                presets.missions.attack.helo:extend({name='cherkessk-cas-red-1', altitude=200, expend=AI.Task.WeaponExpend.HALF }),
                presets.missions.attack.surface:extend({name='cherkessk-assault-red'})
            }
        })
    },
    [2] = {
        presets.upgrades.basic.tent:extend({
            name='cherkessk-tent-blue',
            products = {
                presets.special.blue.infantry:extend({ name='cherkessk-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='cherkessk-garrison-blue'})
            }
        }),
        presets.upgrades.supply.fuelTankFarp:extend({
            name='cherkessk-fuel-blue',
            products = {
                presets.missions.supply.helo:extend({name='cherkessk-supply-blue'}),
                presets.missions.supply.helo:extend({name='cherkessk-supply-blue-1'}),
                presets.missions.supply.transfer:extend({name='cherkessk-transfer-blue'}),
                presets.missions.attack.surface:extend({name='cherkessk-assault-blue'})
            }
        }),
        presets.upgrades.airdef.comCenter:extend({
            name='cherkessk-comcenter-blue',
            products = {
                presets.defenses.blue.shorad:extend({name='cherkessk-sam-blue'}),
                presets.missions.attack.helo:extend({name='cherkessk-cas-blue', altitude=200, expend=AI.Task.WeaponExpend.HALF }),
                presets.missions.attack.helo:extend({name='cherkessk-cas-blue-1', altitude=200, expend=AI.Task.WeaponExpend.HALF })
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Cherkessk.lua ]]-----------------



-----------------[[ MissionSpecific/PretenseCaucasus/ZoneDefinitions/Juliett.lua ]]-----------------

zones.juliett = ZoneCommand:new("Juliett")
zones.initialState = nil
zones.juliett:defineUpgrades({
    [1] = {
        presets.upgrades.basic.tent:extend({
            name='juliett-tent-red',
            products = {
                presets.special.red.infantry:extend({ name='juliett-defense-red'}),
				presets.defenses.red.infantry:extend({ name='juliett-garrison-red'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='juliett-fuel-red',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='juliett-supply-red'}),
                presets.missions.supply.transfer:extend({name='juliett-transfer-red'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='juliett-ammo-red',
            products = {
                presets.missions.attack.surface:extend({name='juliett-assault-red'})
            }
        })
    },
    [2] = {
        presets.upgrades.basic.tent:extend({
            name='juliett-tent-blue',
            products = {
                presets.special.blue.infantry:extend({ name='juliett-defense-blue'}),
				presets.defenses.blue.infantry:extend({ name='juliett-garrison-blue'})
            }
        }),
        presets.upgrades.supply.fuelCache:extend({
            name='juliett-fuel-blue',
            products = {
                presets.missions.supply.convoy_escorted:extend({name='juliett-supply-blue'}),
                presets.missions.supply.transfer:extend({name='juliett-transfer-blue'})
            }
        }),
        presets.upgrades.attack.ammoCache:extend({
            name='juliett-ammo-blue',
            products = {
                presets.missions.attack.surface:extend({name='juliett-assault-blue'})
            }
        })
    }
})

-----------------[[ END OF MissionSpecific/PretenseCaucasus/ZoneDefinitions/Juliett.lua ]]-----------------



	cm = ConnectionManager:new()
	cm:addConnection('Batumi', 'Alpha')
	cm:addConnection('Alpha', 'Bravo')
	cm:addConnection('Bravo', 'Kobuleti')
	cm:addConnection('Bravo', 'Factory')
	cm:addConnection('Kobuleti', 'Factory')
	cm:addConnection('Kobuleti', 'Charlie')
	cm:addConnection('Foxtrot', 'Charlie')
	cm:addConnection('Foxtrot', 'Kobuleti')
	cm:addConnection('Delta','Foxtrot')
	cm:addConnection('Delta','Kobuleti')
	cm:addConnection('Delta','Factory')
	cm:addConnection('Echo','Charlie')
	cm:addConnection('Golf','Echo')
	cm:addConnection('Golf','Foxtrot')
	cm:addConnection('India','Delta')
	cm:addConnection('Hotel','Golf')
	cm:addConnection('Hotel','Foxtrot')
	cm:addConnection('Hotel','Delta')
	cm:addConnection('Hotel','India')
	cm:addConnection('Juliett','Echo')
	cm:addConnection('Juliett','Golf')
	cm:addConnection('Senaki','Juliett')
	cm:addConnection('Senaki','Golf')
	cm:addConnection('Senaki','Hotel')
	cm:addConnection('Kutaisi','Hotel')
	cm:addConnection('Kutaisi','India')
	cm:addConnection('Kilo','Juliett')
	cm:addConnection('Mike','Kutaisi')
	cm:addConnection('Mike','Senaki')
	cm:addConnection('Romeo','Mike')
	cm:addConnection('Romeo','Kutaisi')
	cm:addConnection('Weapon Depot','Juliett')
	cm:addConnection('Weapon Depot','Senaki')
	cm:addConnection('Weapon Depot','Kilo')
	cm:addConnection('November','Weapon Depot')
	cm:addConnection('November','Senaki')
	cm:addConnection('November','Mike')
	cm:addConnection('Oil Fields','Romeo')
	cm:addConnection('Quebec','Kilo')
	cm:addConnection('Zugdidi','Weapon Depot')
	cm:addConnection('Zugdidi','Quebec')
	cm:addConnection('Zugdidi','November')
	cm:addConnection('Zugdidi','Kilo')
	cm:addConnection('Distillery','November')
	cm:addConnection('Distillery','Mike')
	cm:addConnection('Zugdidi','Papa')
	cm:addConnection('November','Papa')
	cm:addConnection('Sierra','Papa')
	cm:addConnection('Sierra','Zugdidi')
	cm:addConnection('Sierra','Uniform')
	cm:addConnection('Mine','Uniform')
	cm:addConnection('Tango','Quebec')
	cm:addConnection('Tango','Zugdidi')
	cm:addConnection('Sierra','Tango')
	cm:addConnection('Whiskey','Tango')
	cm:addConnection('Ochamchira','Tango')
	cm:addConnection('Ochamchira','Whiskey')
	cm:addConnection('Ochamchira','Farm')
	cm:addConnection('Ochamchira','Zulu')
	cm:addConnection('Farm','Zulu')
	cm:addConnection('Sukhumi','Zulu')
	cm:addConnection('Lentehi','Distillery', true, 3000)
	cm:addConnection('Lentehi','Babugent', true, 5000)
	cm:addConnection('Nalchik','Babugent')
	cm:addConnection('Victor','Distillery', true, 2000)
	cm:addConnection('Victor','Romeo')
	cm:addConnection('Victor','Lentehi')
	cm:addConnection('Victor','Oil Fields', true, 2000)
	cm:addConnection('Victor','Oni')
	cm:addConnection('Unal','Oni', true, 4500)
	cm:addConnection('Beslan','Unal')
	cm:addConnection('Digora','Beslan')
	cm:addConnection('Digora','Unal')
	cm:addConnection('Digora','Babugent')
	cm:addConnection('Terek','Digora')
	cm:addConnection('Terek','Nalchik')
	cm:addConnection('Terek','Beslan')
	cm:addConnection('Prohladniy','Terek')
	cm:addConnection('Prohladniy','Nalchik')
	cm:addConnection('Malgobek','Terek')
	cm:addConnection('Malgobek','Beslan')
	cm:addConnection('Lima','Mine')
	cm:addConnection('Lima','Lentehi', true, 4000)
	cm:addConnection('Tyrnyauz','Lima', true, 4000)
	cm:addConnection('Tyrnyauz','Nalchik')
	cm:addConnection('XRay','Sukhumi')
	cm:addConnection('Oscar','Sukhumi')
	cm:addConnection('Oscar','XRay')
	cm:addConnection('Mozdok','Malgobek')
	cm:addConnection('Mozdok','Prohladniy')
	cm:addConnection('Gudauta','Oscar')
	cm:addConnection('Yankee','Gudauta')
	cm:addConnection('Sochi','Yankee')
	cm:addConnection('Refinery','XRay', true, 4000)
	cm:addConnection('Refinery','Humara')
	cm:addConnection('Intel Center','Tyrnyauz')
	cm:addConnection('Intel Center','Nalchik')
	cm:addConnection('Intel Center','Prohladniy')
	cm:addConnection('Intel Center','Kislovodsk')
	cm:addConnection('Mineralnye','Intel Center')
	cm:addConnection('Kislovodsk','Mineralnye')
	cm:addConnection('Tallyk','Mineralnye')
	cm:addConnection('Tallyk','Kislovodsk')
	cm:addConnection('Power Plant','Mineralnye')
	cm:addConnection('Power Plant','Tallyk')
	cm:addConnection('Cherkessk','Tallyk')
	cm:addConnection('Cherkessk','Power Plant')
	cm:addConnection('Cherkessk','Humara')
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