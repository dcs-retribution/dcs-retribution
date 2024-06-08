local unitPayloads = {
	["name"] = "OH58D",
	["payloads"] = {
		[1] = {
			["name"] = "Retribution CAS",
			["pylons"] = {
				[1] = {
					["CLSID"] = "OH58D_AGM_114_R",
					["num"] = 5,
				},
				[2] = {
					["CLSID"] = "OH58D_M3P_L500",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 16,
			},
		},
		[2] = {
			["displayName"] = "Retribution DEAD",
			["name"] = "Retribution DEAD",
			["pylons"] = {
				[1] = {
					["CLSID"] = "OH58D_AGM_114_R",
					["num"] = 5,
				},
				[2] = {
					["CLSID"] = "OH58D_AGM_114_L",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 16,
			},
		},
		[3] = {
			["displayName"] = "Retribution BAI",
			["name"] = "Retribution BAI",
			["pylons"] = {
				[1] = {
					["CLSID"] = "OH58D_AGM_114_R",
					["num"] = 5,
				},
				[2] = {
					["CLSID"] = "{M260_APKWS_M151}",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 16,
			},
		},
		[4] = {
			["displayName"] = "Retribution OCA/Aircraft",
			["name"] = "Retribution OCA/Aircraft",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{M260_APKWS_M151}",
					["num"] = 5,
				},
				[2] = {
					["CLSID"] = "{M260_APKWS_M151}",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 16,
			},
		},
		[5] = {
			["displayName"] = "Retribution Escort",
			["name"] = "Retribution Escort",
			["pylons"] = {
				[1] = {
					["CLSID"] = "OH58D_AGM_114_R",
					["num"] = 5,
				},
				[2] = {
					["CLSID"] = "OH58D_FIM_92_L",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 16,
			},
		},
	},
	["tasks"] = {
		[1] = 11,
		[2] = 31,
		[3] = 32,
		[4] = 16,
		[5] = 18,
		[6] = 35,
		[7] = 30,
		[8] = 17,
	},
	["unitType"] = "OH58D",
}
return unitPayloads
