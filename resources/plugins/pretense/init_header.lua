

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

	TemplateDB.templates["blueShipGroup"] = {
		units = {
			"PERRY",
			"USS_Arleigh_Burke_IIa",
			"PERRY"
		},
		maxDist = 300,
		skill = "Excellent",
		dataCategory= TemplateDB.type.group
	}

	TemplateDB.templates["redShipGroup"] = {
		units = {
			"ALBATROS",
			"NEUSTRASH",
			"ALBATROS"
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
			}),
            shipTankerSeawisegiant = Preset:new({
                display = 'Tanker Seawise Giant',
                cost = 1500,
                type = 'upgrade',
                template = "ship-tanker-seawisegiant"
            }),
            shipLandingShipSamuelChase = Preset:new({
                display = 'LST USS Samuel Chase',
                cost = 1500,
                type = 'upgrade',
                template = "ship-landingship-samuelchase"
            }),
            shipLandingShipRopucha = Preset:new({
                display = 'LS Ropucha',
                cost = 1500,
                type = 'upgrade',
                template = "ship-landingship-ropucha"
            }),
            shipTankerElnya = Preset:new({
                display = 'Tanker Elnya',
                cost = 1500,
                type = 'upgrade',
                template = "ship-tanker-elnya"
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
			}),
            shipSupplyTilde = Preset:new({
                display = 'Ship_Tilde_Supply',
                cost = 1500,
                type = 'upgrade',
                template = "ship-supply-tilde"
            }),
            shipLandingShipLstMk2 = Preset:new({
                display = 'LST Mk.II',
                cost = 1500,
                type = 'upgrade',
                template = "ship-landingship-lstmk2"
            }),
            shipBulkerYakushev = Preset:new({
                display = 'Bulker Yakushev',
                cost = 1500,
                type = 'upgrade',
                template = "ship-bulker-yakushev"
            }),
            shipCargoIvanov = Preset:new({
                display = 'Cargo Ivanov',
                cost = 1500,
                type = 'upgrade',
                template = "ship-cargo-ivanov"
            })
		},
		airdef = {
			bunker = Preset:new({
				display = 'Bunker',
				cost = 1500,
				type = 'upgrade',
				template = "bunker-1"
			}),
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
			}),
			redShipGroup = Preset:new({
				display = 'SAM', 
				cost=3000, 
				type='defense', 
				template='redShipGroup',
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
			}),
			blueShipGroup = Preset:new({
				display = 'SAM',
				cost=3000,
				type='defense',
				template='blueShipGroup',
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

