local unitPayloads = {
	["name"] = "B-21",
	["payloads"] = {
		[1] = {
			["displayName"] = "Retribution Anti-ship",
			["name"] = "Retribution Anti-ship",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{B21_AGM-158C*4}",
					["num"] = 2,
				},
				[2] = {
					["CLSID"] = "{B21_AGM-158C*4}",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[2] = {
			["displayName"] = "Retribution BAI",
			["name"] = "Retribution BAI",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{AABA1A14-78A1-4E85-94DD-463CF75BD9E4}",
					["num"] = 2,
				},
				[2] = {
					["CLSID"] = "{AABA1A14-78A1-4E85-94DD-463CF75BD9E4}",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[3] = {
			["displayName"] = "Retribution DEAD",
			["name"] = "Retribution DEAD",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{B21_AGM-158B*4}",
					["num"] = 2,
				},
				[2] = {
					["CLSID"] = "{B21_AGM-158B*4}",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[4] = {
			["displayName"] = "Retribution OCA/Runway",
			["name"] = "Retribution OCA/Runway",
			["pylons"] = {
				[1] = {
					["CLSID"] = "GBU-31V3B*8",
					["num"] = 1,
				},
				[2] = {
					["CLSID"] = "<CLEAN>",
					["num"] = 2,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[5] = {
			["displayName"] = "Retribution CAS",
			["name"] = "Retribution CAS",
			["pylons"] = {
				[1] = {
					["CLSID"] = "GBU-31*8",
					["num"] = 2,
					["settings"] = {
						["NFP_PRESID"] = "MDRN_B_A_PGM_TWINWELL",
						["NFP_PRESVER"] = 1,
						["NFP_VIS_DrawArgNo_56"] = 0.5,
						["NFP_fuze_type_nose"] = "EMPTY_NOSE",
						["NFP_fuze_type_tail"] = "FMU139CB_LD",
						["arm_delay_ctrl_FMU139CB_LD"] = 4,
						["function_delay_ctrl_FMU139CB_LD"] = 0,
					},
				},
				[2] = {
					["CLSID"] = "GBU-31*8",
					["num"] = 1,
					["settings"] = {
						["NFP_PRESID"] = "MDRN_B_A_PGM_TWINWELL",
						["NFP_PRESVER"] = 1,
						["NFP_VIS_DrawArgNo_56"] = 0.5,
						["NFP_fuze_type_nose"] = "EMPTY_NOSE",
						["NFP_fuze_type_tail"] = "FMU139CB_LD",
						["arm_delay_ctrl_FMU139CB_LD"] = 4,
						["function_delay_ctrl_FMU139CB_LD"] = 0,
					},
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[6] = {
			["displayName"] = "Retribution SEAD Sweep",
			["name"] = "Retribution SEAD Sweep",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{B21_AGM-88G*4}",
					["num"] = 2,
				},
				[2] = {
					["CLSID"] = "{B21_AGM-158B*4}",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[7] = {
			["displayName"] = "Retribution OCA/Aircraft",
			["name"] = "Retribution OCA/Aircraft",
			["pylons"] = {
				[1] = {
					["CLSID"] = "GBU-31V3B*8",
					["num"] = 2,
				},
				[2] = {
					["CLSID"] = "GBU-31V3B*8",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[8] = {
			["displayName"] = "Retribution Armed Recon",
			["name"] = "Retribution Armed Recon",
			["pylons"] = {
				[1] = {
					["CLSID"] = "GBU-31*8",
					["num"] = 2,
					["settings"] = {
						["NFP_PRESID"] = "MDRN_B_A_PGM_TWINWELL",
						["NFP_PRESVER"] = 1,
						["NFP_VIS_DrawArgNo_56"] = 0.5,
						["NFP_fuze_type_nose"] = "EMPTY_NOSE",
						["NFP_fuze_type_tail"] = "FMU139CB_LD",
						["arm_delay_ctrl_FMU139CB_LD"] = 4,
						["function_delay_ctrl_FMU139CB_LD"] = 0,
					},
				},
				[2] = {
					["CLSID"] = "GBU-31*8",
					["num"] = 1,
					["settings"] = {
						["NFP_PRESID"] = "MDRN_B_A_PGM_TWINWELL",
						["NFP_PRESVER"] = 1,
						["NFP_VIS_DrawArgNo_56"] = 0.5,
						["NFP_fuze_type_nose"] = "EMPTY_NOSE",
						["NFP_fuze_type_tail"] = "FMU139CB_LD",
						["arm_delay_ctrl_FMU139CB_LD"] = 4,
						["function_delay_ctrl_FMU139CB_LD"] = 0,
					},
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[9] = {
			["displayName"] = "Retribution SEAD",
			["name"] = "Retribution SEAD",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{B21_AGM-88G*4}",
					["num"] = 2,
				},
				[2] = {
					["CLSID"] = "{B21_AGM-88G*4}",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[10] = {
			["displayName"] = "Retribution Strike",
			["name"] = "Retribution Strike",
			["pylons"] = {
				[1] = {
					["CLSID"] = "<CLEAN>",
					["num"] = 2,
				},
				[2] = {
					["CLSID"] = "{B21_GBU-57}",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
	},
	["tasks"] = {
	},
	["unitType"] = "B-21",
}
return unitPayloads
