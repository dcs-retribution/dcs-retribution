local unitPayloads = {
	["name"] = "B-52H",
	["payloads"] = {
		[1] = {
			["displayName"] = "Retribution BAI",
			["name"] = "Retribution BAI",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{HSAB_8x_CBU105_R}",
					["num"] = 3,
					["settings"] = {
						["NFP_fuze_type_nose"] = "FZU39",
						["function_altitude_ctrl_FZU39_SUU65_SFW"] = 457.2,
						["function_delay_ctrl_FZU39_SUU65_SFW"] = 2.23,
					},
				},
				[2] = {
					["CLSID"] = "{HSAB_8x_CBU105_L}",
					["num"] = 1,
					["settings"] = {
						["NFP_PRESID"] = "MDRN_CC_A_SUU65Plus_SFW",
						["NFP_PRESVER"] = 1,
						["NFP_fuze_type_nose"] = "FZU39",
						["function_altitude_ctrl_FZU39_SUU65_SFW"] = 457.2,
						["function_delay_ctrl_FZU39_SUU65_SFW"] = 2.23,
					},
				},
				[3] = {
					["CLSID"] = "{A111396E-D3E8-4b9c-8AC9-2432489304D5}",
					["num"] = 4,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[2] = {
			["name"] = "Retribution DEAD",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{45447F82-01B5-4029-A572-9AAD28AF0275}",
					["num"] = 3,
				},
				[2] = {
					["CLSID"] = "{8DCAF3A3-7FCF-41B8-BB88-58DEDA878EDE}",
					["num"] = 2,
				},
				[3] = {
					["CLSID"] = "{45447F82-01B5-4029-A572-9AAD28AF0275}",
					["num"] = 1,
				},
				[4] = {
					["CLSID"] = "{A111396E-D3E8-4b9c-8AC9-2432489304D5}",
					["num"] = 4,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[3] = {
			["displayName"] = "Retribution Anti-ship",
			["name"] = "Retribution Anti-ship",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{HSAB_4x_AGM84D_R}",
					["num"] = 3,
				},
				[2] = {
					["CLSID"] = "{HSAB_4x_AGM84D_L}",
					["num"] = 1,
				},
				[3] = {
					["CLSID"] = "{A111396E-D3E8-4b9c-8AC9-2432489304D5}",
					["num"] = 4,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[4] = {
			["name"] = "Retribution OCA/Runway",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{HSAB_6x_GBU31V3_R}",
					["num"] = 3,
					["settings"] = {
						["01_prfx_arm_delay_ctrl_FMU143"] = 5.5,
						["01_prfx_function_delay_ctrl_FMU143"] = 0.03,
						["NFP_fuze_type_tail"] = "FMU143",
					},
				},
				[2] = {
					["CLSID"] = "{HSAB_6x_GBU31V3_L}",
					["num"] = 1,
					["settings"] = {
						["01_prfx_arm_delay_ctrl_FMU143"] = 5.5,
						["01_prfx_function_delay_ctrl_FMU143"] = 0.03,
						["NFP_PRESID"] = "MDRN_B_A_PGM_HTP",
						["NFP_PRESVER"] = 2,
						["NFP_fuze_type_tail"] = "FMU143",
					},
				},
				[3] = {
					["CLSID"] = "{CSRL_GBU31V3}",
					["num"] = 2,
					["settings"] = {
						["01_prfx_arm_delay_ctrl_FMU143"] = 5.5,
						["01_prfx_function_delay_ctrl_FMU143"] = 0.03,
						["NFP_PRESID"] = "MDRN_B_A_PGM_HTP",
						["NFP_PRESVER"] = 2,
						["NFP_fuze_type_tail"] = "FMU143",
					},
				},
				[4] = {
					["CLSID"] = "{A111396E-D3E8-4b9c-8AC9-2432489304D5}",
					["num"] = 4,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[5] = {
			["displayName"] = "Retribution Strike",
			["name"] = "Retribution Strike",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{HSAB_6x_GBU31V3_R}",
					["num"] = 3,
					["settings"] = {
						["01_prfx_arm_delay_ctrl_FMU143"] = 5.5,
						["01_prfx_function_delay_ctrl_FMU143"] = 0.03,
						["NFP_fuze_type_tail"] = "FMU143",
					},
				},
				[2] = {
					["CLSID"] = "{CSRL_GBU31V3}",
					["num"] = 2,
					["settings"] = {
						["01_prfx_arm_delay_ctrl_FMU143"] = 5.5,
						["01_prfx_function_delay_ctrl_FMU143"] = 0.03,
						["NFP_PRESID"] = "MDRN_B_A_PGM_HTP",
						["NFP_PRESVER"] = 2,
						["NFP_fuze_type_tail"] = "FMU143",
					},
				},
				[3] = {
					["CLSID"] = "{HSAB_6x_GBU31V3_L}",
					["num"] = 1,
					["settings"] = {
						["01_prfx_arm_delay_ctrl_FMU143"] = 5.5,
						["01_prfx_function_delay_ctrl_FMU143"] = 0.03,
						["NFP_PRESID"] = "MDRN_B_A_PGM_HTP",
						["NFP_PRESVER"] = 2,
						["NFP_fuze_type_tail"] = "FMU143",
					},
				},
				[4] = {
					["CLSID"] = "{A111396E-D3E8-4b9c-8AC9-2432489304D5}",
					["num"] = 4,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[6] = {
			["displayName"] = "Retribution OCA/Aircraft",
			["name"] = "Retribution OCA/Aircraft",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{HSAB_6x_GBU31V3_R}",
					["num"] = 3,
					["settings"] = {
						["01_prfx_arm_delay_ctrl_FMU143"] = 5.5,
						["01_prfx_function_delay_ctrl_FMU143"] = 0.03,
						["NFP_fuze_type_tail"] = "FMU143",
					},
				},
				[2] = {
					["CLSID"] = "{HSAB_6x_GBU31V3_L}",
					["num"] = 1,
					["settings"] = {
						["01_prfx_arm_delay_ctrl_FMU143"] = 5.5,
						["01_prfx_function_delay_ctrl_FMU143"] = 0.03,
						["NFP_PRESID"] = "MDRN_B_A_PGM_HTP",
						["NFP_PRESVER"] = 2,
						["NFP_fuze_type_tail"] = "FMU143",
					},
				},
				[3] = {
					["CLSID"] = "{CSRL_GBU31V3}",
					["num"] = 2,
					["settings"] = {
						["01_prfx_arm_delay_ctrl_FMU143"] = 5.5,
						["01_prfx_function_delay_ctrl_FMU143"] = 0.03,
						["NFP_PRESID"] = "MDRN_B_A_PGM_HTP",
						["NFP_PRESVER"] = 2,
						["NFP_fuze_type_tail"] = "FMU143",
					},
				},
				[4] = {
					["CLSID"] = "{A111396E-D3E8-4b9c-8AC9-2432489304D5}",
					["num"] = 4,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
	},
	["unitType"] = "B-52H",
}
return unitPayloads
