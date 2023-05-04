local unitPayloads = {
	["name"] = "TIE",
	["payloads"] = {
		[1] = {
			["name"] = "CAP",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{TIEFUEL}",
					["num"] = 2,
				},
				[2] = {
					["CLSID"] = "{TIEFUEL}",
					["num"] = 10,
				},
				
			},
			["tasks"] = {				
				[1] = CAP,
				[2] = Escort,
				[3] = FighterSweep,
				[4] = Intercept,
				[5] = Reconnaissance,
			},
		},
		
		
	
},
["tasks"] = {
	},
["unitType"] = "TIE", 
}
return unitPayloads
