local unitPayloads = {
	["name"] = "Tu-16",
	["payloads"] = {
		[1] = {
			["name"] = "STRIKE",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{TU_16_KSR5}",
					["num"] = 1,
				},
				[2] = {
					["CLSID"] = "{BDAD04AA-4D4A-4E51-B958-180A89F963CF}",
					["num"] = 3,
				},
				[3] = {
					["CLSID"] = "{TU_16_KSR5}",
					["num"] = 4,
				},
			},
			["tasks"] = {
				[1] = 33,
			},
		},
		[2] = {
			["name"] = "ANTISHIP",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{TU_16_KSR5}",
					["num"] = 1,
				},
				[2] = {
					["CLSID"] = "{TU_16_KSR5}",
					["num"] = 4,
				},
			},
			["tasks"] = {
				[1] = 15,
			},
		},
		[3] = {
			["displayName"] = "SEAD",
			["name"] = "SEAD",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{TU_16_KSR5ARM}",
					["num"] = 1,
				},
				[2] = {
					["CLSID"] = "{TU_16_KSR5ARM}",
					["num"] = 4,
				},
			},
			["tasks"] = {
				[1] = 15,
			},
		},
		[4] = {
			["name"] = "CAS",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{TU_16_KSR5}",
					["num"] = 1,
				},
				[2] = {
					["CLSID"] = "{BDAD04AA-4D4A-4E51-B958-180A89F963CF}",
					["num"] = 3,
				},
				[3] = {
					["CLSID"] = "{TU_16_KSR5}",
					["num"] = 4,
				},
			},
			["tasks"] = {
				[1] = 33,
			},
		},
	},
	["tasks"] = {
	},
	["unitType"] = "Tu-16",
}
return unitPayloads
