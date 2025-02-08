local unitPayloads = {
	["name"]="vwv_mig17f",
	["payloads"]=
	{
		[1]=
		{
			["displayName"]="Retribution BARCAP",
			["name"]="Retribution BARCAP",
			["pylons"]=
			{
				[1]=
				{
					["CLSID"]="PTB400_MIG15",
					["num"]=3
				},
				[2]=
				{
					["CLSID"]="PTB400_MIG15",
					["num"]=4
				}
			},
			["tasks"]=
			{
				[1]=11,
				[2]=10
			}
		},
		[2]=
		{
			["displayName"]="Retribution Strike",
			["name"]="Retribution Strike",
			["pylons"]=
			{
				[1]=
				{
					["CLSID"]="{3C612111-C7AD-476E-8A8E-2485812F4E5C}",
					["num"]=1
				},
				[2]=
				{
					["CLSID"]="{3C612111-C7AD-476E-8A8E-2485812F4E5C}",
					["num"]=2
				}
			},
			["tasks"]=
			{
				[1]=32,
				[2]=33
			}
		},
		[3]=
		{
			["displayName"]="Retribution CAS",
			["name"]="Retribution CAS",
			["pylons"]=
			{
				[1]=
				{
					["CLSID"]="B-8M1 - 20 S-8OFP2",
					["num"]=1
				},
				[2]=
				{
					["CLSID"]="B-8M1 - 20 S-8OFP2",
					["num"]=2
				}
			},
			["tasks"]=
			{
				[1]=31
			}
		},
		[4]=
		{
			["displayName"]="Retribution BAI",
			["name"]="Retribution BAI",
			["pylons"]=
			{
				[1]=
				{
					["CLSID"]="B-8M1 - 20 S-8OFP2",
					["num"]=1
				},
				[2]=
				{
					["CLSID"]="B-8M1 - 20 S-8OFP2",
					["num"]=2
				}
			},
			["tasks"]=
			{
				[1]=32,
				[2]=33
			}
		},
		[5]=
		{
			["displayName"]="Retribution TARCAP",
			["name"]="Retribution TARCAP",
			["pylons"]=
			{
				[1]=
				{
					["CLSID"]="PTB400_MIG15",
					["num"]=3
				},
				[2]=
				{
					["CLSID"]="PTB400_MIG15",
					["num"]=4
				}
			},
			["tasks"]=
			{
				[1]=11
			}
		},
		[6]=
		{
			["displayName"]="Retribution Escort",
			["name"]="Retribution Escort",
			["pylons"]=
			{
				[1]=
				{
					["CLSID"]="PTB400_MIG15",
					["num"]=3
				},
				[2]=
				{
					["CLSID"]="PTB400_MIG15",
					["num"]=4
				}
			},
			["tasks"]=
			{
				[1]=18
			}
		},
		[7]=
		{
			["displayName"]="Retribution Fighter sweep",
			["name"]="Retribution Fighter sweep",
			["pylons"]=
			{
				[1]=
				{
					["CLSID"]="PTB400_MIG15",
					["num"]=3
				},
				[2]=
				{
					["CLSID"]="PTB400_MIG15",
					["num"]=4
				}
			},
			["tasks"]=
			{
				[1]=19
			}
		},
		[8]=
		{
			["displayName"]="Retribution Armed Recon",
			["name"]="Retribution Armed Recon",
			["pylons"]=
			{
				[1]=
				{
					["CLSID"]="PTB400_MIG15",
					["num"]=3
				},
				[2]=
				{
					["CLSID"]="PTB400_MIG15",
					["num"]=4
				}
			},
			["tasks"]=
			{
				[1]=11,
				[2]=10
			}
		}
	},
	["unitType"]="vwv_mig17f"
}
return unitPayloads
--
-- from task.py --
-- SEAD: id = 29
-- CAS: id = 31
-- GroundAttack: id = 32
-- PinpointStrike: id = 33
-- RunwayAttack: id = 34
-- AntishipStrike: id = 30
-- CAP: id = 11
-- Intercept: id = 10
-- FighterSweep: id = 19
-- Escort: id = 18
-- Reconnaissance: id = 17
-- AFAC: id = 16
-- AWACS: id = 14
-- Transport: id = 35
-- Refueling: id = 13
-- Nothing: id = 15