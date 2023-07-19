local unitPayloads = {
	["name"] = "VSN_F104C",
	["payloads"] = {
		[1] = {
			["displayName"] = "Retribution BARCAP",
			["name"] = "Retribution BARCAP",
			["pylons"] = {
				[1] = {
					["CLSID"] = "VSN_F104G_L_PTB",
					["num"] = 2,
				},
				[2] = {
					["CLSID"] = "{AIM-9P5}",
					["num"] = 4,
				},
				[3] = {
					["CLSID"] = "LAU-105_2*AIM-9P5",
					["num"] = 6,
				},
				[4] = {
					["CLSID"] = "{AIM-9P5}",
					["num"] = 8,
				},
				[5] = {
					["CLSID"] = "VSN_F104G_R_PTB",
					["num"] = 10,
				},
			},
			["tasks"] = {
				[1] = 11,
			},
		},
		[2] = {
			["displayName"] = "Retribution Strike",
			["name"] = "Retribution Strike",
			["pylons"] = {
				[1] = {
					["CLSID"] = "VSN_F104G_L_PTB",
					["num"] = 2,
				},
				[2] = {
					["CLSID"] = "VSN_F104G_R_PTB",
					["num"] = 10,
				},
				[3] = {
					["CLSID"] = "{D5D51E24-348C-4702-96AF-97A714E72697}",
					["num"] = 4,
				},
				[4] = {
					["CLSID"] = "{BCE4E030-38E9-423E-98ED-24BE3DA87C32}",
					["num"] = 6,
					["settings"] = {
						["GUI_fuze_type"] = 1,
						["arm_delay_ctrl_FMU139CB_LD"] = 1,
						["function_delay_ctrl_FMU139CB_LD"] = 0,
					},
				},
				[5] = {
					["CLSID"] = "{D5D51E24-348C-4702-96AF-97A714E72697}",
					["num"] = 8,
				},
			},
			["tasks"] = {
				[1] = 11,
			},
		},
		[3] = {
			["name"] = "Retribution CAS",
			["pylons"] = {
				[1] = {
					["CLSID"] = "VSN_F104G_R_PTB",
					["num"] = 10,
				},
				[2] = {
					["CLSID"] = "VSN_F104G_L_PTB",
					["num"] = 2,
				},
				[3] = {
					["CLSID"] = "{7B34E0BB-E427-4C2A-A61A-8407CE18B54D}",
					["num"] = 8,
				},
				[4] = {
					["CLSID"] = "{BCE4E030-38E9-423E-98ED-24BE3DA87C32}",
					["num"] = 6,
					["settings"] = {
						["GUI_fuze_type"] = 1,
						["arm_delay_ctrl_FMU139CB_LD"] = 1,
						["function_delay_ctrl_FMU139CB_LD"] = 0,
					},
				},
				[5] = {
					["CLSID"] = "{7B34E0BB-E427-4C2A-A61A-8407CE18B54D}",
					["num"] = 4,
				},
			},
			["tasks"] = {
			},
		},
		[4] = {
			["name"] = "Retribution DEAD",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{BRU33_2X_ROCKEYE}",
					["num"] = 4,
				},
				[2] = {
					["CLSID"] = "{BRU33_2X_ROCKEYE}",
					["num"] = 8,
				},
				[3] = {
					["CLSID"] = "LAU-105_2*AIM-9P5",
					["num"] = 6,
				},
				[4] = {
					["CLSID"] = "VSN_F104G_L_PTB",
					["num"] = 2,
				},
				[5] = {
					["CLSID"] = "VSN_F104G_R_PTB",
					["num"] = 10,
				},
			},
			["tasks"] = {
			},
		},
	},
	["tasks"] = {
	},
	["unitType"] = "VSN_F104C",
}
return unitPayloads
