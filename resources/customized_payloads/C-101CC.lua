local unitPayloads = {
	["name"] = "C-101CC",
	["payloads"] = {
		[1] = {
			["name"] = "CAP",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{C-101-DEFA553}",
					["num"] = 4,
				},
				[2] = {
					["CLSID"] = "{FC23864E-3B80-48E3-9C03-4DA8B1D7497B}",
					["num"] = 1,
				},
				[3] = {
					["CLSID"] = "{FC23864E-3B80-48E3-9C03-4DA8B1D7497B}",
					["num"] = 7,
				},
			},
			["tasks"] = {
				[1] = 17,
			},
		},
		[2] = {
			["name"] = "CAS",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{C-101-DEFA553}",
					["num"] = 4,
				},
				[2] = {
					["CLSID"] = "{A021F29D-18AB-4d3e-985C-FC9C60E35E9E}",
					["num"] = 5,
				},
				[3] = {
					["CLSID"] = "{A021F29D-18AB-4d3e-985C-FC9C60E35E9E}",
					["num"] = 3,
				},
				[4] = {
					["CLSID"] = "{A021F29D-18AB-4d3e-985C-FC9C60E35E9E}",
					["num"] = 2,
				},
				[5] = {
					["CLSID"] = "{A021F29D-18AB-4d3e-985C-FC9C60E35E9E}",
					["num"] = 6,
				},
				[6] = {
					["CLSID"] = "{6CEB49FC-DED8-4DED-B053-E1F033FF72D3}",
					["num"] = 7,
				},
				[7] = {
					["CLSID"] = "{6CEB49FC-DED8-4DED-B053-E1F033FF72D3}",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 31,
			},
		},
		[3] = {
			["name"] = "ANTISHIP",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{1461CD18-429A-42A9-A21F-4C621ECD4573}",
					["num"] = 6,
				},
				[2] = {
					["CLSID"] = "{1461CD18-429A-42A9-A21F-4C621ECD4573}",
					["num"] = 2,
				},
			},
			["tasks"] = {
				[1] = 30,
			},
		},
		[4] = {
			["name"] = "STRIKE",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{C-101-DEFA553}",
					["num"] = 4,
				},
				[2] = {
					["CLSID"] = "{6CEB49FC-DED8-4DED-B053-E1F033FF72D3}",
					["num"] = 7,
				},
				[3] = {
					["CLSID"] = "{6CEB49FC-DED8-4DED-B053-E1F033FF72D3}",
					["num"] = 1,
				},
				[4] = {
					["CLSID"] = "{BCE4E030-38E9-423E-98ED-24BE3DA87C32}",
					["num"] = 3,
					["settings"] = {
						["GUI_fuze_type"] = 1,
						["arm_delay_ctrl_FMU139CB_LD"] = 1,
						["function_delay_ctrl_FMU139CB_LD"] = 0,
					},
				},
				[5] = {
					["CLSID"] = "{BCE4E030-38E9-423E-98ED-24BE3DA87C32}",
					["num"] = 5,
					["settings"] = {
						["GUI_fuze_type"] = 1,
						["arm_delay_ctrl_FMU139CB_LD"] = 1,
						["function_delay_ctrl_FMU139CB_LD"] = 0,
					},
				},
			},
			["tasks"] = {
				[1] = 31,
			},
		},
		[5] = {
			["name"] = "SEAD",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{C-101-DEFA553}",
					["num"] = 4,
				},
				[2] = {
					["CLSID"] = "{FD90A1DC-9147-49FA-BF56-CB83EF0BD32B}",
					["num"] = 2,
				},
				[3] = {
					["CLSID"] = "{FD90A1DC-9147-49FA-BF56-CB83EF0BD32B}",
					["num"] = 6,
				},
				[4] = {
					["CLSID"] = "{6CEB49FC-DED8-4DED-B053-E1F033FF72D3}",
					["num"] = 7,
				},
				[5] = {
					["CLSID"] = "{6CEB49FC-DED8-4DED-B053-E1F033FF72D3}",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 31,
			},
		},
	},
	["tasks"] = {
	},
	["unitType"] = "C-101CC",
}
return unitPayloads
