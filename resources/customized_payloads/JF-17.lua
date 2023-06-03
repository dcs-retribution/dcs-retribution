local unitPayloads = {
	["name"] = "JF-17",
	["payloads"] = {
		[1] = {
			["name"] = "ANTISHIP",
			["pylons"] = {
				[1] = {
					["CLSID"] = "DIS_WMD7",
					["num"] = 4,
				},
				[2] = {
					["CLSID"] = "DIS_PL-5EII",
					["num"] = 1,
				},
				[3] = {
					["CLSID"] = "DIS_PL-5EII",
					["num"] = 7,
				},
				[4] = {
					["CLSID"] = "DIS_SD-10_DUAL_R",
					["num"] = 6,
				},
				[5] = {
					["CLSID"] = "DIS_SD-10_DUAL_L",
					["num"] = 2,
				},
				[6] = {
					["CLSID"] = "DIS_C-802AK",
					["num"] = 3,
				},
				[7] = {
					["CLSID"] = "DIS_C-802AK",
					["num"] = 5,
				},
			},
			["tasks"] = {
				[1] = 10,
				[2] = 11,
				[3] = 19,
			},
		},
		[2] = {
			["name"] = "STRIKE",
			["pylons"] = {
				[1] = {
					["CLSID"] = "DIS_LS_6_500",
					["num"] = 6,
				},
				[2] = {
					["CLSID"] = "DIS_LS_6_500",
					["num"] = 5,
				},
				[3] = {
					["CLSID"] = "DIS_LS_6_500",
					["num"] = 3,
				},
				[4] = {
					["CLSID"] = "DIS_LS_6_500",
					["num"] = 2,
				},
				[5] = {
					["CLSID"] = "DIS_PL-5EII",
					["num"] = 1,
				},
				[6] = {
					["CLSID"] = "DIS_PL-5EII",
					["num"] = 7,
				},
			},
			["tasks"] = {
				[1] = 10,
				[2] = 11,
				[3] = 19,
			},
		},
		[3] = {
			["name"] = "CAP",
			["pylons"] = {
				[1] = {
					["CLSID"] = "DIS_TANK800",
					["num"] = 5,
				},
				[2] = {
					["CLSID"] = "DIS_TANK800",
					["num"] = 3,
				},
				[3] = {
					["CLSID"] = "DIS_SPJ_POD",
					["num"] = 4,
				},
				[4] = {
					["CLSID"] = "DIS_PL-5EII",
					["num"] = 1,
				},
				[5] = {
					["CLSID"] = "DIS_PL-5EII",
					["num"] = 7,
				},
				[6] = {
					["CLSID"] = "DIS_SD-10_DUAL_R",
					["num"] = 6,
				},
				[7] = {
					["CLSID"] = "DIS_SD-10_DUAL_L",
					["num"] = 2,
				},
			},
			["tasks"] = {
				[1] = 10,
				[2] = 11,
				[3] = 19,
			},
		},
		[4] = {
			["name"] = "RUNWAY_ATTACK",
			["pylons"] = {
				[1] = {
					["CLSID"] = "DIS_TYPE200_DUAL_R",
					["num"] = 6,
				},
				[2] = {
					["CLSID"] = "DIS_TANK800",
					["num"] = 5,
				},
				[3] = {
					["CLSID"] = "DIS_TANK800",
					["num"] = 3,
				},
				[4] = {
					["CLSID"] = "DIS_TYPE200_DUAL_L",
					["num"] = 2,
				},
				[5] = {
					["CLSID"] = "DIS_PL-5EII",
					["num"] = 1,
				},
				[6] = {
					["CLSID"] = "DIS_PL-5EII",
					["num"] = 7,
				},
				[7] = {
					["CLSID"] = "DIS_WMD7",
					["num"] = 4,
				},
			},
			["tasks"] = {
				[1] = 10,
				[2] = 11,
				[3] = 19,
			},
		},
		[5] = {
			["name"] = "CAS",
			["pylons"] = {
				[1] = {
					["CLSID"] = "DIS_WMD7",
					["num"] = 4,
				},
				[2] = {
					["CLSID"] = "DIS_PL-5EII",
					["num"] = 1,
				},
				[3] = {
					["CLSID"] = "DIS_PL-5EII",
					["num"] = 7,
				},
				[4] = {
					["CLSID"] = "DIS_BRM1_90",
					["num"] = 6,
				},
				[5] = {
					["CLSID"] = "DIS_BRM1_90",
					["num"] = 2,
				},
			},
			["tasks"] = {
				[1] = 10,
				[2] = 11,
				[3] = 19,
			},
		},
		[6] = {
			["name"] = "SEAD",
			["pylons"] = {
				[1] = {
					["CLSID"] = "DIS_SPJ_POD",
					["num"] = 4,
				},
				[2] = {
					["CLSID"] = "DIS_PL-5EII",
					["num"] = 1,
				},
				[3] = {
					["CLSID"] = "DIS_PL-5EII",
					["num"] = 7,
				},
				[4] = {
					["CLSID"] = "DIS_LD-10_DUAL_R",
					["num"] = 6,
				},
				[5] = {
					["CLSID"] = "DIS_LD-10_DUAL_L",
					["num"] = 2,
				},
				[6] = {
					["CLSID"] = "DIS_TANK800",
					["num"] = 3,
				},
				[7] = {
					["CLSID"] = "DIS_TANK800",
					["num"] = 5,
				},
			},
			["tasks"] = {
				[1] = 10,
				[2] = 11,
				[3] = 19,
			},
		},
		[7] = {
			["displayName"] = "Retribution OCA/Runway",
			["name"] = "Retribution OCA/Runway",
			["pylons"] = {
				[1] = {
					["CLSID"] = "DIS_PL-5EII",
					["num"] = 7,
				},
				[2] = {
					["CLSID"] = "DIS_PL-5EII",
					["num"] = 1,
				},
				[3] = {
					["CLSID"] = "DIS_TYPE200_DUAL_L",
					["num"] = 2,
				},
				[4] = {
					["CLSID"] = "DIS_TYPE200_DUAL_R",
					["num"] = 6,
				},
				[5] = {
					["CLSID"] = "DIS_TANK800",
					["num"] = 4,
				},
				[6] = {
					["CLSID"] = "DIS_TYPE200",
					["num"] = 5,
				},
				[7] = {
					["CLSID"] = "DIS_TYPE200",
					["num"] = 3,
				},
			},
			["tasks"] = {
				[1] = 34,
			},
		},
	},
	["unitType"] = "JF-17",
}
return unitPayloads
