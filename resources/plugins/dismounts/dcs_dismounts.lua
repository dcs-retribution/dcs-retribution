--TRANSPORT CAPACITIES
--BTR-80,BTR-81A,BMP-2,BMP-3: 7 Troops
--BMP-1: 8 Troops
--MTLB: 11 Troops
--M2A2 Bradley: 7 Troops
--Stryker: 9 Troops
--LAV-25: 6 Troops
--BMD-1 and BTR-RD: 6 Troops
--Marder with Milan: 6, without 7
--Warrior: 7
--M-113: 11
--AAV-7: 21 (hoooly schmallies!)
--Tpz Fuchs: 10
--Sdkfz 251
--M2 Halftrack
--Sdkfz 7

--Country IDs: 17 = Insurgents 81 = CJTF Red

--Questioned: Merkava? M6 Linebacker?

do

local missionTransports = {}
local weaponTransports = {}
local groupsWithRoutes = {}
local groupsWithRoutesUpdated = {}
local removeFromWeaponTransports = {}
dismountsInitiated = 0

transportCapacities = 
{
	["BMP-1"] = 8,
	["BMP-2"] = 7,
	["BMP-3"] = 7,
	["BTR-82A"] = 7,
	["BTR-80"] = 7,
	["BMD-1"] = 6,
	["BTR_D"] = 6,
	["GAZ-66"] = 7,
	["KAMAZ Truck"] = 7,
	["ZBD04A"] = 7,
	["M-2 Bradley"] = 7,
	["Marder"] = 7,
	["MCV-80"] = 7,
	["LAV-25"] = 6,
	["M 818"] = 7,
	["M-113"] = 11,
	["M1126 Stryker ICV"] = 9,
	["AAV7"] = 21,
	["TPZ"] = 10,
	["MTLB"] = 11,
	--["M 818"] = 7,
}


--START Squads
russianModernSquadBTR_BMP2_BMP3 =
{
	"Infantry AK",
	"Infantry AK",
	"Infantry AK ver2",
	"Infantry AK ver3",
	"Infantry AK ver2",
	"SA-18 Igla-S manpad",
	"Infantry AK ver3"	
}--end of russianModernSquadBTR_BMP2_BMP3

russianRifleSquadBTR_BMP2_BMP3 =
{
	"Infantry AK",
	"Infantry AK ver2",
	"Infantry AK",
	"Infantry AK ver3",
	"Infantry AK ver2",
	"Infantry AK ver3",
	"Infantry AK ver3"	
}--end of russianRifleSquadBTR_BMP2_BMP3

russianManpadsCmdSquadBTR_BMP2_BMP3 =
{
	"SA-18 Igla-S comm",
	"Infantry AK",
	"SA-18 Igla-S manpad",
	"Infantry AK ver2",
	"Infantry AK ver3",
	"SA-18 Igla-S manpad",
	"Infantry AK ver3"	
}--end of russianManpadsCmdSquadBTR_BMP2_BMP3

russianSquadBMP1 =
{
	"Infantry AK",
	"Infantry AK ver2",
	"Infantry AK",
	"Infantry AK ver3",
	"Infantry AK ver2",
	"Infantry AK ver3",
	"Infantry AK ver3",
	"Infantry AK ver2"
}--end of russianSquadBMP1

russianSquadManpadsBMP1 =
{
	"Infantry AK",
	"Infantry AK ver2",
	"SA-18 Igla-S manpad",
	"Infantry AK ver3",
	"Infantry AK ver2",
	"Infantry AK ver3",
	"Infantry AK ver3",
	"Infantry AK ver2"
}--end of russianSquadManpadsBMP1

russianSquadManpadsCmdBMP1 =
{
	"SA-18 Igla-S comm",
	"Infantry AK ver2",
	"SA-18 Igla-S manpad",
	"Infantry AK ver3",
	"Infantry AK ver2",
	"SA-18 Igla-S manpad",
	"Infantry AK ver3",
	"Infantry AK ver2"
}--end of russianSquadManpadsCmdBMP1

russianVDVBMD1 =
{
	"Paratrooper AKS-74",
	"Paratrooper RPG-16",
	"Paratrooper AKS-74",
	"Paratrooper AKS-74",
	"Paratrooper RPG-16",
	"Paratrooper AKS-74"
}--end of russianVDVBMD1

russianSquadMTLB =
{
	"Infantry AK",
	"Infantry AK",
	"Infantry AK ver3",
	"Infantry AK ver2",
	"Infantry AK ver3",
	"Infantry AK ver3",
	"Infantry AK ver2",
	"Infantry AK ver2",
	"Infantry AK",
	"Infantry AK ver2",
	"Infantry AK ver3"
}

russianSquadManpadsMTLB =
{
	"Infantry AK ver3",
	"Infantry AK",
	"Infantry AK ver2",
	"Infantry AK",
	"SA-18 Igla-S manpad",
	"Infantry AK ver3",
	"Infantry AK ver2",
	"Infantry AK ver2",
	"Infantry AK",
	"Infantry AK ver3",
	"Infantry AK"
}

russianSquadRPGMTLB =
{
	"Infantry AK",
	"Infantry AK",
	"Infantry AK ver3",
	"Paratrooper RPG-16",
	"Infantry AK ver3",
	"Infantry AK ver2",
	"Paratrooper RPG-16",
	"Infantry AK ver3",
	"Paratrooper RPG-16",
	"Infantry AK ver2",
	"Infantry AK ver3"
}

russianSquadRPGIglaMTLB =
{
	"Infantry AK",
	"Infantry AK",
	"Infantry AK ver3",
	"Paratrooper RPG-16",
	"SA-18 Igla-S manpad",
	"Infantry AK ver2",
	"Paratrooper RPG-16",
	"Infantry AK ver3",
	"Infantry AK ver2",
	"Infantry AK",
	"Infantry AK ver3"
}

russianSquadAntiAirMTLB =
{
	"Infantry AK ver3",
	"Infantry AK ver2",
	"Infantry AK",
	"SA-18 Igla-S manpad",
	"Infantry AK ver3",
	"Infantry AK ver2",
	"SA-18 Igla-S manpad",
	"Infantry AK ver3",
	"Infantry AK",
	"Infantry AK ver2",
	"SA-18 Igla-S manpad"
}

usaSquadLAV25 =
{
	"Soldier M4",
	"Soldier M4",
	"Soldier M249",
	"Soldier M4",
	"Soldier M4",
	"Soldier M249"
}

usaSquadManpadsLAV25 =
{
	"Soldier M4",
	"Soldier M4",
	"Soldier stinger",
	"Soldier M4",
	"Soldier M4",
	"Soldier M249"
}

usaSquadManpadsBradleyMarder =
{
	"Soldier M4",
	"Soldier M4",
	"Soldier M249",
	"Soldier M4",
	"Soldier M4",
	"Soldier stinger",
	"Soldier M4"
}

usaSquadBradleyMarderWarrior =
{
	"Soldier M4",
	"Soldier M4",
	"Soldier M249",
	"Soldier M4",
	"Soldier M4",
	"Soldier M249",
	"Soldier M4"
}

usaSquadStryker =
{
	"Soldier M4",
	"Soldier M4",
	"Soldier M249",
	"Soldier M4",
	"Soldier M4",
	"Soldier M249",
	"Soldier M4",
	"Soldier M4",
	"Soldier M4"
}

usaSquadManpadsStryker =
{
	"Soldier M4",
	"Soldier M4",
	"Soldier M249",
	"Soldier M4",
	"Soldier M4",
	"Soldier stinger",
	"Soldier M4",
	"Soldier M4",
	"Soldier M249"
}

usaFireteamStryker =
{
	"Soldier M4",
	"Soldier M249",
	"Soldier M249",
	"Soldier M249",
	"Soldier M4",
	"Soldier stinger",
	"Soldier M4",
	"Soldier stinger",
	"Soldier M249"
}

usaSquadManpadsM113 =
{
	"Soldier M4",
	"Soldier M4",
	"Soldier M4",
	"Soldier M4",
	"Soldier M4",
	"Soldier stinger",
	"Soldier M4",
	"Soldier M4",
	"Soldier M249",
	"Soldier M4",
	"Soldier M249"
}

usaSquadM113 =
{
	"Soldier M4",
	"Soldier M4",
	"Soldier M249",
	"Soldier M4",
	"Soldier M4",
	"Soldier M4",
	"Soldier M4",
	"Soldier M4",
	"Soldier M249",
	"Soldier M4",
	"Soldier M249"
}

usaSquadAAV7USMC =
{
	"Soldier M4",
	"Soldier M4",
	"Soldier M249",
	"Soldier M4",
	"Soldier M4",
	"Soldier M249",
	"Soldier M4",
	"Soldier M4",
	"Soldier M249",
	"Soldier M249",
	"Soldier M4",
	"Soldier M4",
	"Soldier M249",
	"Soldier M4",
	"Soldier M4",
	"Soldier M249",
	"Soldier M4",
	"Soldier M4",
	"Soldier M249",
	"Soldier M249",
	"Soldier M4"
}

usaSquadManpadsAAV7USMC =
{
	"Soldier M4",
	"Soldier M4",
	"Soldier M249",
	"Soldier M4",
	"Soldier M4",
	"Soldier M249",
	"Soldier M4",
	"Soldier stinger",
	"Soldier M249",
	"Soldier M249",
	"Soldier M4",
	"Soldier M4",
	"Soldier stinger",
	"Soldier M4",
	"Soldier M4",
	"Soldier M249",
	"Soldier M4",
	"Soldier stinger",
	"Soldier M249",
	"Soldier M249",
	"Soldier M4"
}

gerSquadTPz = 
{
	"Soldier M4",
	"Soldier M4",
	"Soldier M249",
	"Soldier M4",
	"Soldier M4",
	"Soldier M4",
	"Soldier M4",
	"Soldier M4",
	"Soldier M249",
	"Soldier M4"
}

gerSquadManpadsTPz = 
{
	"Soldier M4",
	"Soldier M4",
	"Soldier M249",
	"Soldier M4",
	"Soldier M4",
	"Soldier M4",
	"Soldier M4",
	"Soldier M4",
	"Soldier stinger",
	"Soldier M4"
}

insRifleSquadBTR_BMP2 =
{
	"Infantry AK Ins",
	"Infantry AK Ins",
	"Infantry AK Ins",
	"Infantry AK Ins",
	"Infantry AK Ins",
	"Infantry AK Ins",
	"Infantry AK Ins"
}

insSquadBTR_BMP2 =
{
	"Infantry AK Ins",
	"Soldier AK",
	"Soldier RPG",
	"Infantry AK Ins",
	"Soldier AK",
	"Infantry AK Ins",
	"Soldier AK"
}

insSquadManpadsBTR_BMP2 =
{
	"Infantry AK Ins",
	"Infantry AK Ins",
	"Igla manpad INS",
	"Infantry AK Ins",
	"Infantry AK Ins",
	"Infantry AK Ins",
	"Infantry AK Ins"
}

insSquadAntiAirBTR_BMP2 =
{
	"SA-18 Igla comm",
	"Soldier AK",
	"Igla manpad INS",
	"Infantry AK Ins",
	"Soldier AK",
	"Infantry AK Ins",
	"SA-18 Igla manpad"
}

insSquadRpgBTR_BMP2 =
{
	"Infantry AK Ins",
	"Soldier AK",
	"Soldier RPG",
	"Infantry AK Ins",
	"Soldier AK",
	"Soldier RPG",
	"Soldier RPG"
}

insRifleSquadBMP1 =
{
	"Infantry AK Ins",
	"Infantry AK Ins",
	"Infantry AK Ins",
	"Infantry AK Ins",
	"Infantry AK Ins",
	"Infantry AK Ins",
	"Infantry AK Ins",
	"Infantry AK Ins"
}

insSquadBMP1 =
{
	"Infantry AK Ins",
	"Soldier AK",
	"Soldier RPG",
	"Infantry AK Ins",
	"Soldier AK",
	"Infantry AK Ins",
	"Soldier AK",
	"Soldier AK",
}

insSquadManpadsBMP1 =
{
	"Infantry AK Ins",
	"Infantry AK Ins",
	"Igla manpad INS",
	"Infantry AK Ins",
	"Infantry AK Ins",
	"Infantry AK Ins",
	"Infantry AK Ins",
	"SA-18 Igla manpad"
}

insSquadAntiAirBMP1 =
{
	"SA-18 Igla comm",
	"Soldier AK",
	"Igla manpad INS",
	"Infantry AK Ins",
	"Soldier AK",
	"Infantry AK Ins",
	"SA-18 Igla manpad",
	"Igla manpad INS"
}

insSquadRpgBMP1 =
{
	"Infantry AK Ins",
	"Soldier AK",
	"Soldier RPG",
	"Infantry AK Ins",
	"Soldier AK",
	"Soldier RPG",
	"Soldier RPG",
	"Infantry AK Ins"
}

insSquadMTLB =
{
	"Infantry AK Ins",
	"Infantry AK Ins",
	"Soldier RPG",
	"Infantry AK Ins",
	"Soldier AK",
	"Infantry AK Ins",
	"Soldier RPG",
	"Soldier AK",
	"Soldier AK",
	"Infantry AK Ins",
	"Soldier AK"
}

insRifleSquadMTLB =
{
	"Infantry AK Ins",
	"Infantry AK Ins",
	"Infantry AK Ins",
	"Infantry AK Ins",
	"Infantry AK Ins",
	"Infantry AK Ins",
	"Infantry AK Ins",
	"Infantry AK Ins",
	"Infantry AK Ins",
	"Infantry AK Ins",
	"Infantry AK Ins"
}

insSquadManpadsMTLB =
{
	"Infantry AK Ins",
	"Infantry AK Ins",
	"SA-18 Igla manpad",
	"Infantry AK Ins",
	"Soldier AK",
	"Infantry AK Ins",
	"Soldier RPG",
	"Soldier AK",
	"Soldier AK",
	"Infantry AK Ins",
	"Soldier AK"
}

insSquadAntiAirMTLB =
{
	"Infantry AK Ins",
	"SA-18 Igla manpad",
	"Igla manpad INS",
	"Infantry AK Ins",
	"Soldier AK",
	"Infantry AK Ins",
	"SA-18 Igla comm",
	"Soldier AK",
	"Igla manpad INS",
	"Infantry AK Ins",
	"Soldier AK"
}

insSquadRpgMTLB =
{
	"Soldier AK",
	"Infantry AK Ins",
	"Soldier RPG",
	"Infantry AK Ins",
	"Soldier AK",
	"Infantry AK Ins",
	"Soldier RPG",
	"Soldier RPG",
	"Soldier AK",
	"Infantry AK Ins",
	"Soldier RPG"
}

insSquadMixedMTLB =
{
	"Infantry AK Ins",
	"Infantry AK Ins",
	"Soldier RPG",
	"Infantry AK Ins",
	"Soldier AK",
	"Infantry AK Ins",
	"Soldier RPG",
	"SA-18 Igla manpad",
	"Soldier AK",
	"Infantry AK Ins",
	"Soldier AK"
}

insSquadBMD1 =
{
	"Soldier RPG",
	"Infantry AK Ins",
	"Soldier AK",
	"SA-18 Igla manpad",
	"Soldier AK",
	"Infantry AK Ins"
}

westMortarTeam =
{
	"Soldier M4",
	"Soldier M4",
	"2B11 mortar",
	"Soldier M4",
	"Soldier M4",
	"2B11 mortar"
}

eastMortarTeam =
{
	"Infantry AK ver3",
	"Infantry AK",
	"2B11 mortar",
	"Infantry AK",
	"Infantry AK ver2",
	"2B11 mortar"
}

insMortarTeam =
{
	"Soldier AK",
	"Soldier AK",
	"2B11 mortar",
	"Soldier AK",
	"Soldier AK",
	"2B11 mortar"
}

ww2Wehrmacht =
{
	"soldier_mauser98",
	"soldier_mauser98",
	"soldier_mauser98",
	"soldier_mauser98",
	"soldier_mauser98",
	"soldier_mauser98",
	"soldier_mauser98"
}

ww2UKTroops =
{
	"soldier_wwii_br_01",
	"soldier_wwii_br_01",
	"soldier_wwii_br_01",
	"soldier_wwii_br_01",
	"soldier_wwii_br_01",
	"soldier_wwii_br_01",
	"soldier_wwii_br_01"
}

ww2USTroops =
{
	"soldier_wwii_us",
	"soldier_wwii_us",
	"soldier_wwii_us",
	"soldier_wwii_us",
	"soldier_wwii_us",
	"soldier_wwii_us",
	"soldier_wwii_us"
}
--END squads

--MOD squads
westMortarTeamFrenchPack =
{
	"Soldier M4",
	"Soldier M4",
	"Soldier M4",
	"Soldier M4",
	"M120",
	"M120"
}
--END MOD squads

--Transports for weapon positions
ukRapierSiteTransport =
{
	"",
}

--END Transports for weapon positions

--Weapon sites
weaponSiteTemplate =
{
	["SpawnedUnitType"] = "",				-- Unit Type string for the type of unit to spawn after setup time (SAM launcher or radar, AA gun, field gun etc)
	["SpawnerTransportTypes"] = {"",""},	-- Suitable vehicle types for the script to assign this cargo to
	["SetupTime"] = 0,						-- How many ticks does it take to deploy this system from the transport (ticks are 5 secs each)
	["WorkerCount"] = 0,					-- How many riflemen will spawn when the deployment sequence starts before the system is deployed
	["CarrierVehicleNamePrefix"] = "",		-- If a vehicle in the group has a name starting with this prefix, this cargo type will be added to it
	["Optional"] = false,					-- If true, the script will not populate any vehicle with this cargo type, unless vehicle name is assigned it through use of above prefix
}

weaponSiteTransportItemTemplate =
{
	["TransportingVehicleName"] = "",	
	["TransportedItem"] = "",	
	["WorkerCount"] = 0,
}

ruAAASiteTemplate =
{
	["RDR"] =
	{
		["SpawnedUnitType"] = "SON_9",
		["SpawnerTransportTypes"] = {"TRUCKRU"},
		["SetupTime"] = 60,
		["WorkerCount"] = 4,
		["CarrierVehicleNamePrefix"] = "RDR"
	},
	["KS19s"] =
	{
		["SpawnedUnitType"] = "KS-19",
		["SpawnerTransportTypes"] = {"TRUCKRU"},
		["SetupTime"] = 60,
		["WorkerCount"] = 4,
		["CarrierVehicleNamePrefix"] = "KS",
	},
	["S60s"] =
	{
		["SpawnedUnitType"] = "S-60_Type59_Artillery",
		["SpawnerTransportTypes"] = {"TRUCKRU"},
		["SetupTime"] = 60,
		["WorkerCount"] = 2,
		["CarrierVehicleNamePrefix"] = "S60"
	},
	["ZU23s"] =
	{
		["SpawnedUnitType"] = "ZU-23 Emplacement",
		["SpawnerTransportTypes"] = {"TRUCKRU"},
		["SetupTime"] = 60,
		["WorkerCount"] = 2,
		["CarrierVehicleNamePrefix"] = "ZU"
	},
	["STF"] =
	{
		["SpawnedUnitType"] = "SQ_russianModernSquadBTR_BMP2_BMP3",
		["SpawnerTransportTypes"] = {"TRUCKRU","BMP-1","BMP-2","BTR-80","UAZ"},
		["SetupTime"] = 0,
		["WorkerCount"] = 0,
		["CarrierVehicleNamePrefix"] = "STF"
	},
}

ukRapierSiteTemplate = 
{
	["RDR"] =
	{
		["SpawnedUnitType"] = "rapier_fsa_blindfire_radar",
		["SpawnerTransportTypes"] = {"Land_Rover_101_FC"},
		["SetupTime"] = 60,
		["WorkerCount"] = 2,
		["CarrierVehicleNamePrefix"] = "RDR"
	},
	["OPT"] =
	{
		["SpawnedUnitType"] = "rapier_fsa_optical_tracker_unit",
		["SpawnerTransportTypes"] = {"Land_Rover_101_FC"},
		["SetupTime"] = 60,
		["WorkerCount"] = 2,
		["CarrierVehicleNamePrefix"] = "OPT"
	},
	["MSL"] =
	{
		["SpawnedUnitType"] = "rapier_fsa_launcher",
		["SpawnerTransportTypes"] = {"Land_Rover_101_FC"},
		["SetupTime"] = 60,
		["WorkerCount"] = 2,
		["CarrierVehicleNamePrefix"] = "MSL"
	},
	["STF"] =
	{
		["SpawnedUnitType"] = "SQ_usaSquadManpadsLAV25",
		["SpawnerTransportTypes"] = {"Land_Rover_101_FC","Land_Rover_109_S3"},
		["SetupTime"] = 0,
		["WorkerCount"] = 0,
		["CarrierVehicleNamePrefix"] = "STF"
	},
}

ww2GerLeFHSiteTemplate =
{
	["GUN1"] =
	{
		["SpawnedUnitType"] = "LeFH_18-40-105",
		["SpawnerTransportTypes"] = {"Blitz_36-6700A","Sd_Kfz_7"},
		["SetupTime"] = 60,
		["WorkerCount"] = 4,
		["CarrierVehicleNamePrefix"] = "GUN"
	},
	["GUN2"] =
	{
		["SpawnedUnitType"] = "LeFH_18-40-105",
		["SpawnerTransportTypes"] = {"Blitz_36-6700A","Sd_Kfz_7"},
		["SetupTime"] = 60,
		["WorkerCount"] = 4,
		["CarrierVehicleNamePrefix"] = "GN2"
	},
	["GUN3"] =
	{
		["SpawnedUnitType"] = "LeFH_18-40-105",
		["SpawnerTransportTypes"] = {"Blitz_36-6700A","Sd_Kfz_7"},
		["SetupTime"] = 60,
		["WorkerCount"] = 4,
		["CarrierVehicleNamePrefix"] = "GN3"
	},
	["GUN4"] =
	{
		["SpawnedUnitType"] = "LeFH_18-40-105",
		["SpawnerTransportTypes"] = {"Blitz_36-6700A","Sd_Kfz_7"},
		["SetupTime"] = 60,
		["WorkerCount"] = 4,
		["CarrierVehicleNamePrefix"] = "GN4"
	},
	["STF"] =
	{
		["SpawnedUnitType"] = "SQ_ww2Wehrmacht",
		["SpawnerTransportTypes"] = {"Blitz_36-6700A","Sd_Kfz_251"},
		["SetupTime"] = 0,
		["WorkerCount"] = 0,
		["CarrierVehicleNamePrefix"] = "STF"
	},
}

ww2USAAATemplate =
{
	["M37"] =
	{
		["SpawnedUnitType"] = "M1_37mm",
		["SpawnerTransportTypes"] = {"CCKW_353"},
		["SetupTime"] = 60,
		["WorkerCount"] = 2,
		["CarrierVehicleNamePrefix"] = "M37"
	},
	["M372"] =
	{
		["SpawnedUnitType"] = "M1_37mm",
		["SpawnerTransportTypes"] = {"CCKW_353"},
		["SetupTime"] = 60,
		["WorkerCount"] = 2,
		["CarrierVehicleNamePrefix"] = "M372"
	},
	["M45"] =
	{
		["SpawnedUnitType"] = "M45_Quadmount",
		["SpawnerTransportTypes"] = {"CCKW_353"},
		["SetupTime"] = 60,
		["WorkerCount"] = 2,
		["CarrierVehicleNamePrefix"] = "M45"
	},
	["M373"] =
	{
		["SpawnedUnitType"] = "M1_37mm",
		["SpawnerTransportTypes"] = {"CCKW_353"},
		["SetupTime"] = 60,
		["WorkerCount"] = 2,
		["CarrierVehicleNamePrefix"] = "M373"
	},
	["M451"] =
	{
		["SpawnedUnitType"] = "M45_Quadmount",
		["SpawnerTransportTypes"] = {"CCKW_353"},
		["SetupTime"] = 60,
		["WorkerCount"] = 2,
		["CarrierVehicleNamePrefix"] = "M451"
	},
	["M452"] =
	{
		["SpawnedUnitType"] = "M45_Quadmount",
		["SpawnerTransportTypes"] = {"CCKW_353"},
		["SetupTime"] = 60,
		["WorkerCount"] = 2,
		["CarrierVehicleNamePrefix"] = "M452"
	},
	["STF"] =
	{
		["SpawnedUnitType"] = "SQ_ww2USTroops",
		["SpawnerTransportTypes"] = {"CCKW_353","M2A1_halftrack"},
		["SetupTime"] = 0,
		["WorkerCount"] = 0,
		["CarrierVehicleNamePrefix"] = "STF"
	},
}

missionWeaponSiteTransports = {}

--END Weapon sites


--Script options
dismountsOptions = 
{
	['LeaveDeployed'] = false,
	['WWIIAssets'] = false,
	['FrenchPack'] = false,
	['TroopsFollowSlowTransport'] = false,
	['GorgeousGeorgians'] = false,
	['VehiclesToIgnore'] = {},
	['RandomizeRussianTroops'] = false,
	['NoManpads'] = false,
	['WPNSitesAddMoreWPNToFreeVehicles'] = false,
}

function setOptions(optionsList)
	for key,value in pairs(dismountsOptions) do
		if optionsList[key] ~= nil then
			dismountsOptions[key] = optionsList[key]		
		end
	end
	trigger.action.outText(mist.utils.tableShow(dismountsOptions),25)
end

function georgify(origSquad)
	local newSquad = mist.utils.deepCopy(origSquad)

	for i=1,#newSquad do
		if newSquad[i] == 'Soldier M4' then
			newSquad[i] = 'Soldier M4 GRG'
		end
	end
	return newSquad
end

function randomizeRussianTroops(origSquad)
	-- TO BE IMPLEMENTED
end

function randomizeInsurgentManpads(origSquad)
	-- TO BE IMPLEMENTED
end

local function replaceManpadsWithRiflemen(squad)
	for i=1,#squad do
		local rifleSoldierType = ''
		if squad[i] == 'SA-18 Igla-S manpad' then
			local riflemanTypeSeed = mist.random(3)			
			if riflemanTypeSeed == 1 then
				rifleSoldierType = 'Infantry AK'
			elseif riflemanTypeSeed == 2 then
				rifleSoldierType = 'Infantry AK ver2'
			else
				rifleSoldierType = 'Infantry AK ver3'
			end			
			squad[i] = rifleSoldierType
		elseif squad[i] == 'Igla manpad INS' or squad[i] == 'SA-18 Igla manpad' then
			rifleSoldierType = 'Infantry AK Ins'
			squad[i] = rifleSoldierType
		elseif squad[i] == 'Soldier stinger' then
			rifleSoldierType = 'Soldier M4'
			if dismountsOptions['GorgeousGeorgians'] == true then
				rifleSoldierType = georgify({[1] = rifleSoldierType})[1]
			end
			squad[i] = rifleSoldierType
		end
	end
	return squad
end

function newCoordFromDistanceBearing(initPosVec2,bearing,dist)
	local bearingRad = math.rad(bearing)
	local dept = dist * math.sin(bearingRad)
	local lat = dist * math.cos(bearingRad)

	return { x= initPosVec2.x + dept, y = initPosVec2.y + lat }
end


local function checkForMarkers(hostVehicle)
	--local markersForUnit = mist.marker.get(hostVehicle)
	local markersForUnit = {}
	--trigger.action.outText('markers check for vehichle: ' .. hostVehicle, 2)

	local allMarkers = world.getMarkPanels()
	--trigger.action.outText('total markers: ' .. #markersForUnit, 2)

	if allMarkers ~= nil and #allMarkers > 0 then
		for i=1,#allMarkers do
			if allMarkers[i].text == hostVehicle then
				table.insert(markersForUnit,allMarkers[i])
			end
		end
	end

	if markersForUnit ~= nil and #markersForUnit > 0 then
		return markersForUnit
	else
		return 0
	end
end

local function getHeading(Pos3)
		if (Pos3.x.x > 0) and (Pos3.x.z == 0) then
			return 0
		elseif (Pos3.x.x > 0) and (Pos3.x.z > 0) then
			return math.atan(Pos3.x.z / Pos3.x.x)
		elseif (Pos3.x.x == 0) and (Pos3.x.z > 0) then
			return math.rad(90)
		elseif (Pos3.x.x < 0) and (Pos3.x.z > 0) then
			return math.rad(90) - math.atan(Pos3.x.x / Pos3.x.z)
		elseif (Pos3.x.x < 0) and (Pos3.x.z == 0) then
			return math.rad(180)
		elseif (Pos3.x.x < 0) and (Pos3.x.z < 0) then
			return math.rad(180) + math.atan(Pos3.x.z / Pos3.x.x)
		elseif (Pos3.x.x == 0) and (Pos3.x.z < 0) then
			return math.rad(270)
		elseif (Pos3.x.x > 0) and (Pos3.x.z < 0) then
			return math.rad(270) - math.atan(Pos3.x.x / Pos3.x.z)
		end
end

local function addWaypointToGroup(groupName,waypointsPos3)
	local squadPath = {}
	local groupDismounts = 'Dismounts_' .. groupName
	squadPath[1] = mist.ground.buildWP(mist.getLeadPos(groupDismounts))

	local wpToAdd = mist.ground.buildWP(waypointsPos3[1].pos)
	
	table.insert(squadPath,wpToAdd)
	mist.goRoute(groupDismounts,squadPath)
end

local function addWaypointToVehicles(groupName,waypointVec2)
	local squadPath = {}	
	squadPath[1] = mist.ground.buildWP(mist.getLeadPos(groupName))

	local wpToAdd = mist.ground.buildWP(waypointVec2)
	
	table.insert(squadPath,wpToAdd)
	mist.goRoute(groupName,squadPath)
end


local function createTargetPoint(groupName,waypointsPos3,radiusOfAttack)
	local radiusOfBoom = 5
	if radiusOfAttack ~= nil then
		radiusOfBoom = radiusOfAttack
	end	
	local groupDismounts = 'Dismounts_' .. groupName

	local tgt = { 
		id = 'FireAtPoint', 
		params = { 
			x = waypointsPos3[1].pos.x,
			y = waypointsPos3[1].pos.z,
			radius = radiusOfBoom,
			expendQty = 20,
			expendQtyEnabled = false,
			weaponType = 3221225470,
			altitude = 0,
			alt_type = 1,
		} 
	}

	Group.getByName(groupDismounts):getController():setTask(tgt)
end

--This is for when there is no country specific squad type definition for given vehicle is available, or when you want to populate a vehicle that isn't supported in the script by default. In that case, we will create a random squad based on countryID being east/insurgent/west, as well as the squad having a manpad or being rifle only
local function randomizedSquadForTransport(transportType, squadType, countryID, troopCount)
	local troopNumber = 7 --default to 7
	if troopCount ~= nil then --if a certain number for transports is provided in troopCount parameter, use that
		troopNumber = troopCount
	elseif transportCapacities[transportType] ~= nil then --if not, and if it is a vehicle we know the troop capacity of, then use that instead
		troopNumber = transportCapacities[transportType]
	end
	if squadType == nil then
		local squadTypeSeed = mist.random(3)
		if squadTypeSeed < 3 then
			squadType = 'rifle'
		else
			squadType = 'manpads'
		end
	end
	local squadComposition = {}
	local manpadsSoldierType = ''
	local rifleSoldierType = ''

	if countryID == 0 or countryID == 1 or countryID == 16 or countryID == 18 or countryID == 19 or countryID == 68 or countryID == 81 then --east/Ru
		manpadsSoldierType = 'SA-18 Igla-S manpad'
		local riflemanTypeSeed = mist.random(3)
		if riflemanTypeSeed == 1 then
			rifleSoldierType = 'Infantry AK'
		elseif riflemanTypeSeed == 2 then
			rifleSoldierType = 'Infantry AK ver2'
		else
			rifleSoldierType = 'Infantry AK ver3'
		end
	elseif  countryID == 17 then --Insurgent
		local insManpadsTypeSeed = mist.random(2)
		if insManpadsTypeSeed == 1 then
			manpadsSoldierType = 'Igla manpad INS'
		else
			manpadsSoldierType = 'SA-18 Igla manpad'
		end		
		rifleSoldierType = 'Infantry AK Ins'
	else --west
		manpadsSoldierType = 'Soldier stinger'
		rifleSoldierType = 'Soldier M4'
	end
	if squadType == 'manpads' then
		table.insert(squadComposition,manpadsSoldierType)
		troopNumber = troopNumber - 1
	end
	for i=1,troopNumber do
		table.insert(squadComposition,rifleSoldierType)
	end
	if dismountsOptions["NoManpads"] == true then
		squadComposition = replaceManpadsWithRiflemen(squadComposition)
	end

	return squadComposition
end


local function initializeTransport(unitName,cargoSquad)	
	unitId = Unit.getByName(unitName):getID()

	if dismountsOptions["GorgeousGeorgians"] == true then
		cargoSquad = georgify(cargoSquad)
	end

	missionTransports[unitName] = {			
			countryID = Unit.getByName(unitName):getCountry(),
			UnitID = Unit.getByName(unitName):getID(),
			cargo = cargoSquad,
			cargo_status = "mounted"
	}
end

local function checkTransportForWeaponSite(transportType, allowedTypes)	
	for i=1,#allowedTypes do
		if allowedTypes[i] == transportType then
			return true
		elseif allowedTypes[i] == "TRUCKRU" and (transportType == "GAZ-66" or transportType == "KAMAZ Truck") then
			return true
		end
	end
	return false
end


function assignWeaponTransports(hostGroup,cargoType)
	local transportGroup = Group.getByName(hostGroup)
	local numberOfUnitsInGroup = transportGroup:getSize()
	local unitsWithCargo = {}
	local setupTicksMax = 0

	local weaponTransportType = {}

	--local groupRadars = {}
	--local groupOpticsAndCommand = {}
	--local groupWeapons = {}
	--local groupStaffAndInfantry = {}
	local alreadyLoadedVehicles = {} --key = vehicle name, value = cargo
	local nonSensorCargoTypesInTemplate = {}

	local templateType = cargoType .. 'Template'
	if templateType == 'ww2GerLeFHSiteTemplate' and dismountsOptions['WWIIAssets'] == false then
		--trigger.action.outText('NON!!',15)
		return 0
	end

	--trigger.action.outText(templateType,15)
	weaponTransportType = mist.utils.deepCopy(_G[templateType])
	--trigger.action.outText(mist.utils.tableShow(weaponTransportType),15)

	for transportedItemType, transportedItemInfo in pairs(weaponTransportType) do
		if dismountsOptions["WPNSitesAddMoreWPNToFreeVehicles"] == true and (transportedItemType ~= "RDR" and transportedItemType ~= "OPT") then
			table.insert(nonSensorCargoTypesInTemplate,transportedItemInfo)
		end
		
		for i=1,numberOfUnitsInGroup do
			local unitToProcess = transportGroup:getUnit(i)
			local unitType = unitToProcess:getTypeName()
			local unitName = unitToProcess:getName()
			if transportedItemInfo["CarrierVehicleNamePrefix"] == string.sub(unitName,1,#transportedItemInfo["CarrierVehicleNamePrefix"]) or checkTransportForWeaponSite(unitType,transportedItemInfo["SpawnerTransportTypes"]) then
				if alreadyLoadedVehicles[unitName] == nil then					
					local itemToAdd = {
						['TransportingVehicleName'] = unitName,
						['TransportedItem'] = transportedItemInfo['SpawnedUnitType'],
						['WorkerCount'] = transportedItemInfo['WorkerCount'],
						['WorkerStatus'] = 0
					}
					table.insert(unitsWithCargo,itemToAdd)
					if transportedItemInfo['SetupTime'] > setupTicksMax then
						setupTicksMax = transportedItemInfo['SetupTime']
					end
					--Add the vehicle to "ignore to add squads into" list if any auto populate function is called after this one, then remove it from dismounts list if it was already populated with troops
					table.insert(dismountsOptions['VehiclesToIgnore'],unitName)
					if missionTransports[unitName] ~= nil then
						missionTransports[unitName] = nil
					end
					alreadyLoadedVehicles[unitName] = transportedItemInfo['SpawnedUnitType']
					break
				end
			end
		end
	end

	--loop through the group again to check remaining non-assigned vehicles
	for z=1,numberOfUnitsInGroup do
		local unitToProcess = transportGroup:getUnit(z)
		local unitType = unitToProcess:getTypeName()
		local unitName = unitToProcess:getName()

		if alreadyLoadedVehicles[unitName] == nil then
			for cargoType, cargoInfo in pairs(weaponTransportType) do
				local itemToAdd = {}
				if cargoInfo["CarrierVehicleNamePrefix"] == string.sub(unitName,1,#cargoInfo["CarrierVehicleNamePrefix"]) then
					if alreadyLoadedVehicles[unitName] == nil then					
						itemToAdd = {
							['TransportingVehicleName'] = unitName,
							['TransportedItem'] = cargoInfo['SpawnedUnitType'],
							['WorkerCount'] = cargoInfo['WorkerCount'],
							['WorkerStatus'] = 0
						}
						table.insert(unitsWithCargo,itemToAdd)
						if cargoInfo['SetupTime'] > setupTicksMax then
							setupTicksMax = cargoInfo['SetupTime']
						end
						--Add the vehicle to "ignore to add squads into" list if any auto populate function is called after this one, then remove it from dismounts list if it was already populated with troops
						table.insert(dismountsOptions['VehiclesToIgnore'],unitName)
						if missionTransports[unitName] ~= nil then
							missionTransports[unitName] = nil
						end
						alreadyLoadedVehicles[unitName] = cargoInfo['SpawnedUnitType']
						break
					end
				elseif dismountsOptions["WPNSitesAddMoreWPNToFreeVehicles"] == true and #nonSensorCargoTypesInTemplate > 0 then --and (cargoInfo["CarrierVehicleNamePrefix"] ~= "RDR" or cargoInfo["CarrierVehicleNamePrefix"] ~= "OPT") then
					if alreadyLoadedVehicles[unitName] == nil then
						--first, let's decide whether we'll give this particular vehicle any cargo or not
						local emptyOrFull = mist.random(1,10)
						if emptyOrFull < 8 then
							break
						end
						--now we can go about giving this particular vehicle some random goodies, consideration for future: make vehicle type suitability check for the cargo!!
						local seed = mist.random(1,#nonSensorCargoTypesInTemplate)
						itemToAdd = {
							['TransportingVehicleName'] = unitName,
							['TransportedItem'] = nonSensorCargoTypesInTemplate[seed]['SpawnedUnitType'],
							['WorkerCount'] = nonSensorCargoTypesInTemplate[seed]['WorkerCount'],
							['WorkerStatus'] = 0
						}
						table.insert(unitsWithCargo,itemToAdd)
						if nonSensorCargoTypesInTemplate[seed]['SetupTime'] > setupTicksMax then
							setupTicksMax = nonSensorCargoTypesInTemplate[seed]['SetupTime']
						end
						--Add the vehicle to "ignore to add squads into" list if any auto populate function is called after this one, then remove it from dismounts list if it was already populated with troops
						table.insert(dismountsOptions['VehiclesToIgnore'],unitName)
						if missionTransports[unitName] ~= nil then
							missionTransports[unitName] = nil
						end
						alreadyLoadedVehicles[unitName] = nonSensorCargoTypesInTemplate[seed]['SpawnedUnitType']
						break
					end
				end
			end
		end
	end

	local weaponTransportGroupToAdd = { ['groupName'] = hostGroup, ['SetupTicksLeft'] = setupTicksMax, ['groupCargo'] = unitsWithCargo}
	table.insert(weaponTransports,weaponTransportGroupToAdd)

	--if #weaponTransports > 1 then
		--trigger.action.outText(mist.utils.tableShow(weaponTransports),15)
	--end
end


function determineRandomSquad(hostVehicle)
	countryId = Unit.getByName(hostVehicle):getCountry()
	vehichleType = Unit.getByName(hostVehicle):getTypeName()

	if countryId == 0 or countryId == 1 or countryId == 16 or countryId == 18 or countryId == 19 or countryId == 68 or countryId == 81 or countryId == 17 then --East
		if vehichleType == 'BTR-80' or vehichleType == 'BMP-2' then
			--randomize a number, and determine squad type corresponding to nation and number for this vehicle type, in this case, 7 men squads
			squadTypeSeed = mist.random(7) --1 to 5 = rifle squad, 5 and 6 = rifle squad with 1 manpads, 7 = air defense squad with manpads cmd+2 manpads+4 riflemen			
			if countryId == 17 then --Insurgents
				if squadTypeSeed < 3 then
					initializeTransport(hostVehicle,insRifleSquadBTR_BMP2)
				elseif squadTypeSeed < 5 then
					initializeTransport(hostVehicle,insSquadManpadsBTR_BMP2)
				elseif squadTypeSeed < 6 then
					initializeTransport(hostVehicle,insSquadBTR_BMP2)
				elseif squadTypeSeed < 7 then
					initializeTransport(hostVehicle,insSquadRpgBTR_BMP2)
				else
					initializeTransport(hostVehicle,insSquadAntiAirBTR_BMP2)
				end
			elseif countryId == 81 then --CJTF Red, dismounts can either be of Russian troops type, or Insurgent type
				cjtfRedTroopTypeSeed = mist.random(2)
				if cjtfRedTroopTypeSeed == 1 then
					if squadTypeSeed < 3 then
						initializeTransport(hostVehicle,insRifleSquadBTR_BMP2)
					elseif squadTypeSeed < 5 then
						initializeTransport(hostVehicle,insSquadManpadsBTR_BMP2)
					elseif squadTypeSeed < 6 then
						initializeTransport(hostVehicle,insSquadBTR_BMP2)
					elseif squadTypeSeed < 7 then
						initializeTransport(hostVehicle,insSquadRpgBTR_BMP2)
					else
						initializeTransport(hostVehicle,insSquadAntiAirBTR_BMP2)
					end
				else
					if squadTypeSeed < 5 then
						initializeTransport(hostVehicle,russianRifleSquadBTR_BMP2_BMP3)
					elseif squadTypeSeed < 7 then
						initializeTransport(hostVehicle,russianModernSquadBTR_BMP2_BMP3)
					else
						initializeTransport(hostVehicle,russianManpadsCmdSquadBTR_BMP2_BMP3)
					end
				end
			else --Otherwise use just Russian troops
				if squadTypeSeed < 5 then
					initializeTransport(hostVehicle,russianRifleSquadBTR_BMP2_BMP3)
				elseif squadTypeSeed < 7 then
					initializeTransport(hostVehicle,russianModernSquadBTR_BMP2_BMP3)
				else
					initializeTransport(hostVehicle,russianManpadsCmdSquadBTR_BMP2_BMP3)
				end
			end
		elseif vehichleType == 'ZBD04A'  or vehichleType == 'BMP-3' or vehichleType == 'BTR-82A' then
			squadTypeSeed = mist.random(7)
			if squadTypeSeed < 5 then
				initializeTransport(hostVehicle,russianRifleSquadBTR_BMP2_BMP3)
			elseif squadTypeSeed < 7 then
				initializeTransport(hostVehicle,russianModernSquadBTR_BMP2_BMP3)
			else
				initializeTransport(hostVehicle,russianManpadsCmdSquadBTR_BMP2_BMP3)
			end
		elseif vehichleType == 'GAZ-66' or vehichleType == 'KAMAZ Truck' then
			--trucks may not get any dismounts, depending on randomizer
			squadTypeSeed = mist.random(7)
			if squadTypeSeed < 4 then
				return 0
			elseif squadTypeSeed < 7 then
				if countryId == 17 then
					initializeTransport(hostVehicle,insMortarTeam)
				elseif countryId == 81 then
					cjtfRedTroopTypeSeed = mist.random(2)
					if cjtfRedTroopTypeSeed == 1 then
						initializeTransport(hostVehicle,insMortarTeam)
					else
						initializeTransport(hostVehicle,eastMortarTeam)
					end
				else
					initializeTransport(hostVehicle,eastMortarTeam)
				end
			else
				if countryId == 17 then
					initializeTransport(hostVehicle,insRifleSquadMTLB)
				elseif countryId == 81 then
					cjtfRedTroopTypeSeed = mist.random(2)
					if cjtfRedTroopTypeSeed == 1 then
						initializeTransport(hostVehicle,insRifleSquadMTLB)
					else
						initializeTransport(hostVehicle,russianSquadMTLB)
					end
				else
					initializeTransport(hostVehicle,russianSquadMTLB)
				end
			end			
		elseif vehichleType == 'BMP-1' then
			squadTypeSeed = mist.random(7)
			--trigger.action.outText('seed:' .. squadTypeSeed, 20)
			if countryId == 17 then
				if squadTypeSeed < 3 then
					initializeTransport(hostVehicle,insRifleSquadBMP1)
				elseif squadTypeSeed < 5 then
					initializeTransport(hostVehicle,insSquadBMP1)
				elseif squadTypeSeed < 6 then
					initializeTransport(hostVehicle,insSquadManpadsBMP1)
				elseif squadTypeSeed < 7 then
					initializeTransport(hostVehicle,insSquadRpgBMP1)
				else
					initializeTransport(hostVehicle,insSquadAntiAirBMP1)
				end
			elseif countryId == 81 then
				cjtfRedTroopTypeSeed = mist.random(2)
				if cjtfRedTroopTypeSeed == 1 then
					if squadTypeSeed < 3 then
						initializeTransport(hostVehicle,insRifleSquadBMP1)
					elseif squadTypeSeed < 5 then
						initializeTransport(hostVehicle,insSquadBMP1)
					elseif squadTypeSeed < 6 then
						initializeTransport(hostVehicle,insSquadManpadsBMP1)
					elseif squadTypeSeed < 7 then
						initializeTransport(hostVehicle,insSquadRpgBMP1)
					else
						initializeTransport(hostVehicle,insSquadAntiAirBMP1)
					end
				else
					if squadTypeSeed < 5 then
						initializeTransport(hostVehicle,russianSquadBMP1)
					elseif squadTypeSeed < 7 then
						initializeTransport(hostVehicle,russianSquadManpadsBMP1)
					else
						initializeTransport(hostVehicle,russianSquadManpadsCmdBMP1)
					end
				end
			else
				if squadTypeSeed < 5 then
					initializeTransport(hostVehicle,russianSquadBMP1)
				elseif squadTypeSeed < 7 then
					initializeTransport(hostVehicle,russianSquadManpadsBMP1)
				else
					initializeTransport(hostVehicle,russianSquadManpadsCmdBMP1)
				end
			end			
		elseif vehichleType == 'BMD-1' or vehichleType == 'BTR_D' then
			if countryId == 17 then
				initializeTransport(hostVehicle,insSquadBMD1)
			elseif countryId == 81 then
				cjtfRedTroopTypeSeed = mist.random(2)
				if cjtfRedTroopTypeSeed == 1 then
					initializeTransport(hostVehicle,insSquadBMD1)
				else
					initializeTransport(hostVehicle,russianVDVBMD1)
				end			
			else
				initializeTransport(hostVehicle,russianVDVBMD1)
			end			
		elseif vehichleType == 'MTLB' then
			squadTypeSeed = mist.random(9)
			if countryId == 17 then
				if squadTypeSeed < 3 then
					initializeTransport(hostVehicle,insRifleSquadMTLB)
				elseif squadTypeSeed < 5 then
					initializeTransport(hostVehicle,insSquadMTLB)
				elseif squadTypeSeed < 7 then
					initializeTransport(hostVehicle,insSquadManpadsMTLB)
				elseif squadTypeSeed < 8 then
					initializeTransport(hostVehicle,insSquadRpgBMP1)
				elseif  squadTypeSeed < 9 then
					initializeTransport(hostVehicle,insSquadMixedMTLB)
				else
					initializeTransport(hostVehicle,insSquadAntiAirMTLB)
				end
			elseif countryId == 81 then
				cjtfRedTroopTypeSeed = mist.random(2)
				if cjtfRedTroopTypeSeed == 1 then
					if squadTypeSeed < 3 then
						initializeTransport(hostVehicle,insRifleSquadMTLB)
					elseif squadTypeSeed < 5 then
						initializeTransport(hostVehicle,insSquadMTLB)
					elseif squadTypeSeed < 7 then
						initializeTransport(hostVehicle,insSquadManpadsMTLB)
					elseif squadTypeSeed < 8 then
						initializeTransport(hostVehicle,insSquadRpgBMP1)
					elseif  squadTypeSeed < 9 then
						initializeTransport(hostVehicle,insSquadMixedMTLB)
					else
						initializeTransport(hostVehicle,insSquadAntiAirMTLB)
					end
				else
					if squadTypeSeed < 4 then
						initializeTransport(hostVehicle,russianSquadMTLB)
					elseif squadTypeSeed < 6 then
						initializeTransport(hostVehicle,russianSquadManpadsMTLB)
					elseif squadTypeSeed < 8 then
						initializeTransport(hostVehicle,russianSquadRPGMTLB)
					elseif squadTypeSeed < 9 then
						initializeTransport(hostVehicle,russianSquadRPGIglaMTLB)
					else
						initializeTransport(hostVehicle,russianSquadAntiAirMTLB)
					end	
				end
			else
				if squadTypeSeed < 4 then
					initializeTransport(hostVehicle,russianSquadMTLB)
				elseif squadTypeSeed < 6 then
					initializeTransport(hostVehicle,russianSquadManpadsMTLB)
				elseif squadTypeSeed < 8 then
					initializeTransport(hostVehicle,russianSquadRPGMTLB)
				elseif squadTypeSeed < 9 then
					initializeTransport(hostVehicle,russianSquadRPGIglaMTLB)
				else
					initializeTransport(hostVehicle,russianSquadAntiAirMTLB)
				end
			end			
		else
			initializeTransport(hostVehicle,randomizedSquadForTransport(vehichleType,nil,countryId))
		end --END vehichle type if for east	
	else --West
		if vehichleType == 'M-2 Bradley' or vehichleType == 'Marder' or vehichleType == 'MCV-80' then
			--randomize a number, and determine squad type corresponding to nation and number for this vehicle type, in this case, 7 men squads
			squadTypeSeed = mist.random(7) --1 to 4 = rifle squad, 5 and 6 = rifle squad with 1 manpads, 7 = air defense squad with manpads cmd+2 manpads+4 riflemen			
			if squadTypeSeed < 5 then
				initializeTransport(hostVehicle,usaSquadBradleyMarderWarrior)
			elseif squadTypeSeed < 7 then
				initializeTransport(hostVehicle,usaSquadManpadsBradleyMarder)
			else
				initializeTransport(hostVehicle,usaSquadManpadsBradleyMarder)
			end
		elseif vehichleType == 'M 818' then
			--trucks may not get any dismounts, depending on randomizer
			squadTypeSeed = mist.random(7)
			if squadTypeSeed < 4 then
				return 0
			elseif squadTypeSeed < 7 then
				initializeTransport(hostVehicle,westMortarTeam)
			else
				initializeTransport(hostVehicle,usaSquadM113)
			end
		elseif vehichleType == 'LAV-25' then
			squadTypeSeed = mist.random(7)			
			if squadTypeSeed < 4 then
				initializeTransport(hostVehicle,usaSquadLAV25)
			elseif squadTypeSeed < 6 then
				initializeTransport(hostVehicle,usaSquadManpadsLAV25)
			else
				initializeTransport(hostVehicle,westMortarTeam)
			end
		elseif vehichleType == 'M-113' then
			squadTypeSeed = mist.random(5)
			if squadTypeSeed < 4 then
				initializeTransport(hostVehicle,usaSquadM113)
			else
				initializeTransport(hostVehicle,usaSquadManpadsM113)
			end
		elseif vehichleType == 'M1126 Stryker ICV' then
			squadTypeSeed = mist.random(9)
			if squadTypeSeed < 5 then
				initializeTransport(hostVehicle,usaSquadStryker)
			elseif squadTypeSeed < 8 then
				initializeTransport(hostVehicle,usaSquadManpadsStryker)			
			else
				initializeTransport(hostVehicle,usaFireteamStryker)
			end
		elseif vehichleType == 'AAV7' then
			squadTypeSeed = mist.random(5)
			if squadTypeSeed < 4 then
				initializeTransport(hostVehicle,usaSquadAAV7USMC)				
			else
				initializeTransport(hostVehicle,usaSquadManpadsAAV7USMC)
			end
		elseif vehichleType == 'TPZ' then
			squadTypeSeed = mist.random(5)
			if squadTypeSeed < 4 then
				initializeTransport(hostVehicle,gerSquadTPz)				
			else
				initializeTransport(hostVehicle,gerSquadManpadsTPz)
			end		
		else
			initializeTransport(hostVehicle,randomizedSquadForTransport(vehichleType,nil,countryId))
		end --END vehichle type if for west
	end --END country type

	if dismountsOptions["WWIIAssets"] == true then
			if vehichleType == 'Blitz_36-6700A' or vehichleType == 'Sd_Kfz_251' or vehichleType == 'Sd_Kfz_7' then				
				initializeTransport(hostVehicle,ww2Wehrmacht)
			elseif vehichleType == 'Bedford_MWD' then
				initializeTransport(hostVehicle,ww2UKTroops)
			elseif vehichleType == 'CCKW_353' or vehichleType == 'M2A1_halftrack' then
				initializeTransport(hostVehicle,ww2USTroops)
			end
	end

	if dismountsOptions["FrenchPack"] == true then
			if vehichleType == 'VBCI' then --VBCI 8 troops capacity
				squadTypeSeed = mist.random(7)	
				local pseudoFrenchySquad = {}
				if squadTypeSeed < 5 then
					pseudoFrenchySquad = mist.utils.deepCopy(usaSquadBradleyMarderWarrior)
					table.insert(pseudoFrenchySquad,'Soldier M4')
				elseif squadTypeSeed < 8 then
					pseudoFrenchySquad = mist.utils.deepCopy(usaSquadManpadsBradleyMarder)
					table.insert(pseudoFrenchySquad,'Soldier M4')
				end
				initializeTransport(hostVehicle,pseudoFrenchySquad)
			elseif vehichleType == 'VAB_50' or vehichleType == 'VIB_VBR' or vehichleType == 'VAB_RADIO' then --VAB 10 troops capacity
				squadTypeSeed = mist.random(5)
				if squadTypeSeed < 4 then
					initializeTransport(hostVehicle,gerSquadTPz)				
				else
					initializeTransport(hostVehicle,gerSquadManpadsTPz)
				end
			elseif vehichleType == 'TRM2000' then
				squadTypeSeed = mist.random(7)
				if squadTypeSeed < 4 then
					return 0
				elseif squadTypeSeed < 7 then
					initializeTransport(hostVehicle,westMortarTeamFrenchPack)
				else
					initializeTransport(hostVehicle,usaSquadM113)
				end
			end
	end

	if dismountsOptions["NoManpads"] == true then
		missionTransports[hostVehicle].cargo = replaceManpadsWithRiflemen(missionTransports[hostVehicle].cargo)
	end
end

function assignSetSquadTypeToVehicle(hostVehicle, squadType)
	--squadType = mortarWest, mortarGrg, mortarRu, mortarIns, rifleWest, rifleGrg, rifleRu, rifleIns, manpadsWest, manpadsRu, manpadsIns, vdv, rpgIns, antiAir, special, specificGroupNameFromMEditor:	
	local vehicle = Unit.getByName(hostVehicle)
	local vehichleType = Unit.getByName(hostVehicle):getTypeName()	

	if vehicle ~= nil then
		--vehicles with 7 passenger capacity
		--if vehichleType == 'BTR-80' or vehichleType == 'BMP-2' or vehichleType == 'BMP-3' or vehichleType == 'BTR-82A' or vehichleType == 'M-2 Bradley' or vehichleType == 'Marder' or vehichleType == 'MCV-80' then
		--	if squadType == 'rifleWest' then
		--		initializeTransport(hostVehicle,usaSquadBradleyMarderWarrior)
		--	elseif squadType == 'rifleRu' then
		--		initializeTransport(hostVehicle,russianRifleSquadBTR_BMP2_BMP3)
		--	elseif squadType == 'rifleIns' then
		--		initializeTransport(hostVehicle,insRifleSquadBTR_BMP2)
		--	elseif squadType == 'manpadsWest' then
		--		initializeTransport(hostVehicle,usaSquadManpadsBradleyMarder)
		--	elseif squadType == 'manpadsRu' then
		--		initializeTransport(hostVehicle,russianModernSquadBTR_BMP2_BMP3)
		--	elseif squadType == 'manpadsIns' then
		--		initializeTransport(hostVehicle,insSquadManpadsBTR_BMP2)
		--	end
		--vehicles with 11 passenger capacity
		if vehichleType == 'M-113' or vehichleType == 'MTLB' then
			if squadType == 'rifleWest' then
				initializeTransport(hostVehicle,usaSquadM113)
			elseif squadType == 'rifleRu' then
				initializeTransport(hostVehicle,russianSquadMTLB)
			elseif squadType == 'rifleIns' then
				initializeTransport(hostVehicle,insRifleSquadMTLB)
			elseif squadType == 'manpadsWest' then
				initializeTransport(hostVehicle,usaSquadManpadsM113)
			elseif squadType == 'manpadsRu' then
				initializeTransport(hostVehicle,russianSquadManpadsMTLB)
			elseif squadType == 'manpadsIns' then
				initializeTransport(hostVehicle,insSquadManpadsMTLB)
			end
		else --else use 7 man squads for now
			if squadType == 'rifleWest' then
				initializeTransport(hostVehicle,usaSquadBradleyMarderWarrior)
			elseif squadType == 'rifleRu' then
				initializeTransport(hostVehicle,russianRifleSquadBTR_BMP2_BMP3)
			elseif squadType == 'rifleIns' then
				initializeTransport(hostVehicle,insRifleSquadBTR_BMP2)
			elseif squadType == 'manpadsWest' then
				initializeTransport(hostVehicle,usaSquadManpadsBradleyMarder)
			elseif squadType == 'manpadsRu' then
				initializeTransport(hostVehicle,russianModernSquadBTR_BMP2_BMP3)
			elseif squadType == 'manpadsIns' then
				initializeTransport(hostVehicle,insSquadManpadsBTR_BMP2)
			end
		end
	end
end

function mechanizeAll(optionsList)
	if optionsList ~= nil then
		setOptions(optionsList)
	end

	local units = mist.makeUnitTable({'[all][vehicle]'})
	local ignoreVehicleList = dismountsOptions['VehiclesToIgnore']

	for i=1,#units do
		local isVehicleInIgnoreList = false
		if #ignoreVehicleList > 0 then
			for ignoreItem = 1, #ignoreVehicleList do
				if ignoreVehicleList[ignoreItem] == units[i] then
					isVehicleInIgnoreList = true
				end
			end
		end

		if isVehicleInIgnoreList == false then
			local unit = Unit.getByName(units[i])					
			if unit ~= nil then
				local unitType = unit:getTypeName()
				if unitType == 'BTR-80' or unitType == 'BMP-2' or unitType == 'BMP-3' or unitType == 'BMP-1' or unitType == 'BTR-82A' or
					unitType == 'BMD-1' or unitType == 'BTR_D' or unitType == 'MTLB' or unitType == 'M-2 Bradley' or unitType == 'Marder' or 
					unitType == 'MCV-80' or unitType == 'LAV-25' or unitType == 'M-113' or unitType == 'M1126 Stryker ICV' or unitType == 'AAV7'
					or unitType == 'M 818' or unitType == 'KAMAZ Truck' or unitType == 'GAZ-66' or unitType == 'TPZ' or unitType == 'ZBD04A' or string.sub(units[i],1,11) == 'TRANSPORT##' then		
					determineRandomSquad(units[i])
				end
			
				if dismountsOptions["WWIIAssets"] == true then				
					if unitType == 'Blitz_36-6700A' or unitType == 'Sd_Kfz_251' or unitType == 'Sd_Kfz_7'
					or unitType == 'Bedford_MWD' or unitType == 'CCKW_353' or unitType == 'M2A1_halftrack'
					then					
						determineRandomSquad(units[i])
					end
				end

				if dismountsOptions["FrenchPack"] == true then				
					if unitType == 'VBCI' or unitType == 'VAB_50' or unitType == 'VIB_VBR'
					or unitType == 'VBAE' or unitType == 'VBAE_MMP' or unitType == 'VBL50'
					or unitType == 'VBLANF1' or unitType == 'TRM2000' or unitType == 'VAB_RADIO'
					or unitType == 'VBL-Radio'
					then					
						determineRandomSquad(units[i])
					end
				end
			end
		end
	end
end

function addTransportType(transportType, troopCapacity)
	local units = mist.makeUnitTable({'[all][vehicle]'})
	local ignoreVehicleList = dismountsOptions['VehiclesToIgnore']

	for i=1,#units do
		local isVehicleInIgnoreList = false
		if #ignoreVehicleList > 0 then
			for ignoreItem = 1, #ignoreVehicleList do
				if ignoreVehicleList[ignoreItem] == units[i] then
					isVehicleInIgnoreList = true
				end
			end
		end
		vehichleType = Unit.getByName(units[i]):getTypeName()

		if isVehicleInIgnoreList == false and vehichleType == transportType then					
			countryId = Unit.getByName(units[i]):getCountry()
			initializeTransport(units[i],randomizedSquadForTransport('',nil,countryId,troopCapacity))
		end
	end
end

function spawnWeaponSite(groupName)
	local groupDismounting = Group.getByName(groupName)		
	local countryId = 0

	--trigger.action.outText('spawning weapon site from group: ' .. groupName,15)	
	
	if groupDismounting ~= nil then
		countryId = groupDismounting:getUnit(1):getCountry()
	else
		return false
	end

	--trigger.action.outText(mist.utils.tableShow(groupDismounting),15)
	
	--find in weaponTransports
	local transportData = {}
	
	local carrierPos = groupDismounting:getUnit(1):getPosition()			
	local dmVec2 = {
		x = carrierPos.p.x + carrierPos.x.x * -5,
		y = carrierPos.p.z + carrierPos.x.z * -5,
	}
	local newGroup = {		
			["visible"] = false,
			["route"] = 
			{
				
			}, -- end of ["route"]
			["groupId"] = groupName .. 10000,
			["tasks"] = 
			{
			}, -- end of ["tasks"]
			["hidden"] = false,
			["units"] = 
			{
						
			}, -- end of ["units"]
			["y"] = dmVec2.y,
			["x"] = dmVec2.x,
			["name"] = "Site_" .. groupName,
			["start_time"] = 0,
			["task"] = "Ground Nothing",		
	}
	local unitsInNewGroup = {}

	local weaponTransportsId = 0
	for i=1,#weaponTransports do
		if weaponTransports[i]["groupName"] == groupName then
			transportData = weaponTransports[i]
			weaponTransportsId = i
			i = #weaponTransports
		end
	end

	--trigger.action.outText(mist.utils.tableShow(transportData["groupCargo"]),15)

	--go through still alive units
	for vhc=1,#transportData["groupCargo"] do
		local vehicleName = transportData["groupCargo"][vhc]["TransportingVehicleName"]
		local vehicleObj = Unit.getByName(vehicleName)

		if vehicleObj ~= nil then
			--(create a list of units to spawn first, with their coordinates being near their worker infantry, and then spawn this new group)
			local workers = Group.getByName('Dismounts_'..vehicleName)
			local workersPos = workers:getUnit(1):getPosition()
			local workersPosVec2 = {
				x = workersPos.p.x + workersPos.x.x * -5,
				y = workersPos.p.z + workersPos.x.z * -5,
			}

			local objTypeToSpawn = transportData["groupCargo"][vhc]["TransportedItem"]
			if string.sub(objTypeToSpawn,1,3) ~= 'SQ_' then
				local newObjectToAdd = {				
					["y"] = workersPosVec2.y + 0.05,
					["type"] = objTypeToSpawn,
					["name"] = "WeaponSite_" .. groupName .. "_" .. vhc,
					["unitId"] = "WeaponSite_" .. groupName .. '(' .. vhc .. ')',
					["heading"] = 0,
					["playerCanDrive"] = false,
					["skill"] = "Average",
					["x"] = workersPosVec2.x + 0.05,				
				}
				table.insert(unitsInNewGroup,newObjectToAdd)
			end
			--add spawnable object to unitsInNewGroup
		end
	end
	newGroup["units"] = unitsInNewGroup
	--trigger.action.outText('CountryID = ' .. countryId,15)
	--trigger.action.outText(mist.utils.tableShow(newGroup),15)
	
	
	--spawn their cargo at the location of worker infantry, but only if worker infantry is still alive
	coalition.addGroup(countryId, Group.Category.GROUND, newGroup)
	--table.remove(weaponTransports,weaponTransportsId)
	table.insert(removeFromWeaponTransports,groupName)
	--move the column forward a bit and away from deployed things
	local transportingGroupHdg = getHeading(Group.getByName(groupName):getUnit(1):getPosition())
	local transportingGroupPos = mist.utils.makeVec2(Group.getByName(groupName):getUnit(1):getPoint())
	local trasportingGroupNewPos3Wpt = newCoordFromDistanceBearing(transportingGroupPos,transportingGroupHdg,100)
	addWaypointToVehicles(groupName,trasportingGroupNewPos3Wpt)
end

local function spawnSquad(hostVehicle,alternateCargo,initialWPVec2)
	transportVehicle = missionTransports[hostVehicle]

	if alternateCargo ~= nil then
		local altCargoDataType = type(alternateCargo)
		if altCargoDataType == 'string' and string.sub(alternateCargo,1,3) == 'SQ_' then
			local classNameForCargo = string.sub(alternateCargo,4,-1)
			alternateCargo = _G[classNameForCargo]			
		end
		transportVehicle = 
		{
			countryID = Unit.getByName(hostVehicle):getCountry(),
			UnitID = Unit.getByName(hostVehicle):getID(),
			cargo = alternateCargo
		}

		--trigger.action.outText(mist.utils.tableShow(transportVehicle),15)
	end

	if transportVehicle ~= nil then
		local dismountingTransport = Unit.getByName(hostVehicle)
		local carrierPos = dismountingTransport:getPosition()
		local carrierUnitID = transportVehicle.UnitID		

		local heading = getHeading(carrierPos)

		local choices = {-1, 1}
		local side = choices[ math.random(#choices) ]
		local spawnHeading = heading + math.pi / 2 * side
		local dmVec2 = {
			x = carrierPos.p.x + math.cos(spawnHeading) * 10,
			y = carrierPos.p.z + math.sin(spawnHeading) * 10,
		}
		local dismountsWP2X = dmVec2.x + math.cos(spawnHeading) * 50
		local dismountsWP2Y = dmVec2.y + math.sin(spawnHeading) * 50

		local markDismountWP = checkForMarkers('infWP'..hostVehicle)
		local zoneDismountWP = trigger.misc.getZone('WP_'..hostVehicle)

		--if hostVehicle == 'Ground-1-7' then
		--	trigger.action.outText('So this is our vehicle with zone...',15)
		--
		--	if zoneDismountWP ~= nil then
		--		trigger.action.outText(mist.utils.tableShow(zoneDismountWP),15)
		--	else
		--		trigger.action.outText('AND YET ITS ZONE AINT FOUND... GGGRRRRRRRRRRRRRR',15)
		--	end
		--end


		if markDismountWP ~= 0 and #markDismountWP > 0 then
			--local dismountsWP2X = markDismountWP[1].pos.x
			--local dismountsWP2Y = markDismountWP[1].pos.z

			local routeToSchedule = { pos = markDismountWP[1].pos }
			
			groupsWithRoutes[hostVehicle] = routeToSchedule
		elseif zoneDismountWP ~= nil then
			--trigger.action.outText(mist.utils.tableShow(zoneDismountWP),15)
			--local dismountsWP2X = zoneDismountWP.point.x
			--local dismountsWP2Y = zoneDismountWP.point.z

			local routeToSchedule = { pos = zoneDismountWP.point }

			groupsWithRoutes[hostVehicle] = routeToSchedule

			--trigger.action.outText(mist.utils.tableShow(groupsWithRoutes),15)
		end

		local pointsForFirstWP = 
		{
			[1] = 
				{
					["alt"] = 0,
					["type"] = "Turning Point",
					["ETA"] = 0,
					["alt_type"] = "BARO",
					["formation_template"] = "",
					["y"] = dismountsWP2Y,--dmVec2.y,
					["x"] = dismountsWP2X,--dmVec2.x,
					["ETA_locked"] = true,
					["speed"] = 5.5555555555556,
					["action"] = "Off Road",
					["task"] = 
					{
						["id"] = "ComboTask",
						["params"] = 
						{
							["tasks"] = 
							{
							}, -- end of ["tasks"]
						}, -- end of ["params"]
					}, -- end of ["task"]
					["speed_locked"] = true,
				}, -- end of [1]
				[2] = 
				{
					["alt"] = 0,
					["type"] = "Turning Point",
					["ETA"] = 0,
					["alt_type"] = "BARO",
					["formation_template"] = "",
					["y"] = dismountsWP2Y,
					["x"] = dismountsWP2X,
					["ETA_locked"] = false,
					["speed"] = 5.5555555555556,
					["action"] = "Off Road",
					["task"] = 
					{
						["id"] = "ComboTask",
						["params"] = 
						{
							["tasks"] = 
							{
							}, -- end of ["tasks"]
						}, -- end of ["params"]
					}, -- end of ["task"]
					["speed_locked"] = true,
				}, -- end of [2]
		}

		if initialWPVec2 ~= nil then
			if initialWPVec2.x == 0.0 and initialWPVec2.y == 0.0 then
				pointsForFirstWP[2] = nil
			else
				pointsForFirstWP[2]["x"] = initialWPVec2.x
				pointsForFirstWP[2]["y"] = initialWPVec2.y
			end
		end

		if transportVehicle.cargo ~= nil then
			local groupData = {
					["visible"] = false,
					["route"] = 
					{
						["spans"] = 
						{
						}, -- end of ["spans"]
						["points"] = 
						{
							pointsForFirstWP
						}, -- end of ["points"]
					}, -- end of ["route"]
					["groupId"] = hostVehicle .. 10000,
					["tasks"] = 
					{
					}, -- end of ["tasks"]
					["hidden"] = false,
					["units"] = 
					{
						
					}, -- end of ["units"]
					["y"] = dmVec2.y,
					["x"] = dmVec2.x,
					["name"] = "Dismounts_" .. hostVehicle,
					["start_time"] = 0,
					["task"] = "Ground Nothing",
			}
			local vehiclesList = {}

			for i=1,#transportVehicle.cargo do
				vehiclesList[i] = {
						["y"] = dmVec2.y + math.sin(spawnHeading) * i,
						["type"] = transportVehicle.cargo[i],
						["name"] = "Dismounts_" .. hostVehicle .. "_" .. i,
						["unitId"] = "Dismounts_" .. hostVehicle .. '(' .. transportVehicle.cargo[i] .. ')',
						["heading"] = heading,
						["playerCanDrive"] = true,
						["skill"] = "Average",
						["x"] = dmVec2.x + math.cos(spawnHeading) * i,
				}
			end
			groupData["units"] = vehiclesList
			coalition.addGroup(transportVehicle.countryID, Group.Category.GROUND, groupData)
		end
	else
		return 0;
	end	
end

local function despawnSquad(hostVehicle)
	local g = Group.getByName("Dismounts_" .. hostVehicle)
	local initialSize = g:getInitialSize()
	local currentSize = g:getUnits()
	if initialSize > #currentSize then		
		local remainingInfantry = {}
		for i=1,#currentSize do			
			table.insert(remainingInfantry, currentSize[i]:getTypeName())
		end		
		missionTransports[hostVehicle].cargo = remainingInfantry
	end
end

local function checkMovement()	
	for unitName, transportData in pairs(missionTransports) do
		local dismountingTransport = Unit.getByName(unitName)		
		if dismountingTransport ~= nil then
				unitId = Unit.getByName(unitName):getID()

				local v = dismountingTransport:getVelocity()	--Velocity is a Vec3
				local spd = mist.vec.mag(v)

				if spd < 1 and dismountingTransport:isActive()==true then	--Check if speed is zero
					if transportData.cargo_status == "mounted" then
						spawnSquad(unitName)
						missionTransports[unitName].cargo_status = "dismounted"
					elseif transportData.cargo_status == "dismounted" then
						--local markers = checkForMarkers(unitName)
						--if markers ~= 0 then
						--	for i=1,#markers do
						--		addWaypointToGroup(unitName,markers)
						--	end
						--else
						--	trigger.action.outText('saddy mc sad face :( markers were 0 for vehichle:' .. unitName, 2)
						--end
					end
				else	--Else carrier is moving
					if transportData.cargo_status == "dismounted" then
						if spd > 2.3 then
							local g = Group.getByName("Dismounts_" .. unitName)
							if g ~= nil then	--Check if the group is still alive
								missionTransports[unitName].cargo_status = "mounted"
								despawnSquad(unitName)
								g:destroy()
							else
								missionTransports[unitName].cargo_status = "lost"	--If the dismounted group is destroyed, set status of the carrier to lost to prevent it from deploying a new group
							end
						end
					end
				end
		else
			--trigger.action.outText('wow sth wrong for vehichle:' .. unitName, 2)
			--TODO: remove this entry from missionTransports table
		end
	end

	--ASSIGN ROUTES/TASKS FROM F10 MARKERS
	--trigger.action.outText('grouops with routes are numbered as: '..#groupsWithRoutes,15)
	for key, value in pairs(groupsWithRoutes) do
		local dismountedGroupName = 'Dismounts_' .. key
		local dismountedGroup = Group.getByName(dismountedGroupName)
			
		if dismountedGroup ~= nil then
			--trigger.action.outText('so this should really work.. '..key,35)
			local newPath = {}
			newPath[1] = value
			--trigger.action.outText('WPT is: '..mist.utils.tableShow(newPath),35)
			addWaypointToGroup(key,newPath)
			if groupsWithRoutesUpdated[key] ~= nil then
				groupsWithRoutesUpdated[key] = groupsWithRoutesUpdated[key] + 1
			else
				groupsWithRoutesUpdated[key] = 1
			end
		end
	end

	local removeRoutesUpdated = {}
	for key, value in pairs(groupsWithRoutesUpdated) do
		local cont = true
		if groupsWithRoutes[key] == nil then
			table.insert(removeRoutesUpdated,key)
			cont = false
		end		
		if cont and value > 1 then
			groupsWithRoutes[key] = nil
		end		
	end

	for i=1,#removeRoutesUpdated do
		groupsWithRoutesUpdated[removeRoutesUpdated[i]] = nil
	end
	--END ASSIGN ROUTES/TASKS FROM F10 MARKERS

	--CHECK FOR WEAPON SITE TRANSPORTS
	if #weaponTransports > 0 then
		for i=1,#weaponTransports do
			if weaponTransports[i]["SetupTicksLeft"] > 0 then
				--TODO: first check if the first unit that is alive has stopped or not
				local groupTransportingWeaponSite = weaponTransports[i]["groupName"]
				local leaderVhc = Group.getByName(groupTransportingWeaponSite):getUnit(1)
				local vel = leaderVhc:getVelocity()
				local speed = mist.vec.mag(vel)
				local leaderPos = leaderVhc:getPoint()				
			
				if speed < 1 then --Check if lead vehicle from our weapon site tranport column is stopped
					--if so, let's see if it is near the group's final waypoint
					local groupPath = mist.getGroupPoints(groupTransportingWeaponSite)					

					local distanceToFinalWP = mist.utils.get2DDist(mist.utils.makeVec2(leaderPos),groupPath[#groupPath])
					if distanceToFinalWP < 101 then
						--spawn the "worker" infantry first TODO
						spawnTransportWorkers(groupTransportingWeaponSite)
						--then start the ticks countdown
						weaponTransports[i]["SetupTicksLeft"] = weaponTransports[i]["SetupTicksLeft"] - 1
					end
				end
			elseif weaponTransports[i]["SetupTicksLeft"] == 0 then
				--start spawning!
				weaponTransports[i]["SetupTicksLeft"] = -1 --started spawning, don't keep doing it over and over again shall we?
				spawnWeaponSite(weaponTransports[i]["groupName"])
			end
		end
	end
	if #removeFromWeaponTransports > 0 then
		for toRemoveTransportsIdx=1,#removeFromWeaponTransports do
			for wpnTransportIdx = #weaponTransports, 1, -1 do
				if weaponTransports[wpnTransportIdx]["groupName"] == removeFromWeaponTransports[toRemoveTransportsIdx] then
					table.remove(weaponTransports,wpnTransportIdx)
				end
			end
		end
		removeFromWeaponTransports = {}
	end
	--END CHECK FOR WEAPON SITE TRANSPORTS

	return timer.getTime() + 5
end

function spawnTransportWorkers(groupName)
	local countryId = Group.getByName(groupName):getUnit(1):getCountry()
	local soldierType = "Infantry AK" --default red, Russian soldier

	if countryId == 17 then --insurgents
		soldierType = "Infantry AK Ins"
	elseif (countryId > 1 and countryId < 16 and countryId ~= 7) then --blue
		soldierType = "Soldier M4"
	end

	for i=1,#weaponTransports do
		if weaponTransports[i]["groupName"] == groupName then
			for cargoIndex = 1,#weaponTransports[i]["groupCargo"] do
				local workerSquad = {}
				local transportName = weaponTransports[i]["groupCargo"][cargoIndex]["TransportingVehicleName"]
				local workersToSpawn = 0

				if Unit.getByName(transportName) ~= nil and weaponTransports[i]["groupCargo"][cargoIndex]["WorkerStatus"] == 0 then
					if string.sub(weaponTransports[i]["groupCargo"][cargoIndex]["TransportedItem"],1,3) == 'SQ_' then
						--trigger.action.outText('STF SQ_ stuff sent',15)
						spawnSquad(transportName,weaponTransports[i]["groupCargo"][cargoIndex]["TransportedItem"])
						weaponTransports[i]["groupCargo"][cargoIndex]["WorkerStatus"] = 1
					else
						workersToSpawn = weaponTransports[i]["groupCargo"][cargoIndex]["WorkerCount"]
						for idx = 1, workersToSpawn do
							table.insert(workerSquad,soldierType)
						end
						spawnSquad(transportName,workerSquad,{x=0.0,y=0.0})
						weaponTransports[i]["groupCargo"][cargoIndex]["WorkerStatus"] = 1
					end
				end
			end
		end
	end
end

local function sanitizeMarkers(markerText, markerId)
	--trigger.action.outText('Marker event hit, marker text:' .. markerText .. ' marker Id:' .. markerId, 5)

	local mkrPfx = string.sub(markerText,1,5)
	local markers = checkForMarkers(markerText)
	local markerIdForWP = {}

	

	if mkrPfx == 'infWP' or mkrPfx == 'infTG' then
		--First find the marker with provided ID, which sadly takes an additional loop
		local currentMarker = {}
		for i=1,#markers do
			if markers[i].idx == markerId then
				currentMarker = markers[i]
			end
		end
		local unitName = string.sub(markerText,6,#markerText)
		--Check if the marker is created by a player from same side as the unit
		local unitCoalition = Unit.getByName(unitName):getCoalition()
		if currentMarker.coalition ~= unitCoalition then
			mist.marker.remove(markerId)
			return 0
		end


		if #markers > 1 then
			for i=1,#markers do
				if markers[i].idx ~= markerId then
					mist.marker.remove(markers[i].idx)				
				else
					table.insert(markerIdForWP, markers[i])
				end
			end
		else
			table.insert(markerIdForWP, markers[1])
		end
		
		if mkrPfx == 'infWP' then
			addWaypointToGroup(unitName,markerIdForWP)
		else
			createTargetPoint(unitName,markerIdForWP)
		end
	end	
end

local e = {}
function e:onEvent(event)
	if event.id == world.event.S_EVENT_MARK_ADDED or event.id == world.event.S_EVENT_MARK_CHANGE then
		local mkrText = event.text
		local mkrPfx = string.sub(mkrText,1,5)
		if  mkrPfx == 'infWP' or mkrPfx == 'infTG' then
			sanitizeMarkers(mkrText, event.idx)
		end
	end
end
world.addEventHandler(e)


timer.scheduleFunction(checkMovement, nil, timer.getTime() + 1)

end