local unitPayloads = {
	["name"] = "A-6E",
	["payloads"] = {
		[1] = {
			["displayName"] = "Retribution Strike",
			["name"] = "Retribution Strike",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{0D33DDAE-524F-4A4E-B5B8-621754FE3ADE}",
					["num"] = 5,
					["settings"] = {
						["01_prfx_arm_delay_ctrl_FMU139CB_LD"] = 4,
						["01_prfx_function_delay_ctrl_FMU139CB_LD"] = 0,
						["NFP_PRESID"] = "MDRN_B_A",
						["NFP_PRESVER"] = 2,
						["NFP_VIS_DrawArgNo_57"] = 0,
						["NFP_fuze_type_tail"] = "FMU139CB_LD",
						["laser_code"] = 1688,
					},
				},
				[2] = {
					["CLSID"] = "{0D33DDAE-524F-4A4E-B5B8-621754FE3ADE}",
					["num"] = 4,
					["settings"] = {
						["01_prfx_arm_delay_ctrl_FMU139CB_LD"] = 4,
						["01_prfx_function_delay_ctrl_FMU139CB_LD"] = 0,
						["NFP_PRESID"] = "MDRN_B_A",
						["NFP_PRESVER"] = 2,
						["NFP_VIS_DrawArgNo_57"] = 0,
						["NFP_fuze_type_tail"] = "FMU139CB_LD",
						["laser_code"] = 1688,
					},
				},
				[3] = {
					["CLSID"] = "{HB_A6E_AERO1D}",
					["num"] = 3,
				},
				[4] = {
					["CLSID"] = "{0D33DDAE-524F-4A4E-B5B8-621754FE3ADE}",
					["num"] = 2,
					["settings"] = {
						["01_prfx_arm_delay_ctrl_FMU139CB_LD"] = 4,
						["01_prfx_function_delay_ctrl_FMU139CB_LD"] = 0,
						["NFP_PRESID"] = "MDRN_B_A",
						["NFP_PRESVER"] = 2,
						["NFP_VIS_DrawArgNo_57"] = 0,
						["NFP_fuze_type_tail"] = "FMU139CB_LD",
						["laser_code"] = 1688,
					},
				},
				[5] = {
					["CLSID"] = "{0D33DDAE-524F-4A4E-B5B8-621754FE3ADE}",
					["num"] = 1,
					["settings"] = {
						["01_prfx_arm_delay_ctrl_FMU139CB_LD"] = 4,
						["01_prfx_function_delay_ctrl_FMU139CB_LD"] = 0,
						["NFP_PRESID"] = "MDRN_B_A",
						["NFP_PRESVER"] = 2,
						["NFP_VIS_DrawArgNo_57"] = 0,
						["NFP_fuze_type_tail"] = "FMU139CB_LD",
						["laser_code"] = 1688,
					},
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[2] = {
			["displayName"] = "Retribution SEAD",
			["name"] = "Retribution SEAD",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{B06DD79A-F21E-4EB9-BD9D-AB3844618C93}",
					["num"] = 5,
				},
				[2] = {
					["CLSID"] = "{B06DD79A-F21E-4EB9-BD9D-AB3844618C93}",
					["num"] = 4,
				},
				[3] = {
					["CLSID"] = "{HB_A6E_AERO1D}",
					["num"] = 3,
				},
				[4] = {
					["CLSID"] = "{B06DD79A-F21E-4EB9-BD9D-AB3844618C93}",
					["num"] = 2,
				},
				[5] = {
					["CLSID"] = "{B06DD79A-F21E-4EB9-BD9D-AB3844618C93}",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[3] = {
			["displayName"] = "Retribution SEAD Sweep",
			["name"] = "Retribution SEAD Sweep",
			["pylons"] = {
				[1] = {
					["CLSID"] = "LAU_117_AGM_65F",
					["num"] = 5,
				},
				[2] = {
					["CLSID"] = "{B06DD79A-F21E-4EB9-BD9D-AB3844618C93}",
					["num"] = 4,
				},
				[3] = {
					["CLSID"] = "{HB_A6E_AERO1D}",
					["num"] = 3,
				},
				[4] = {
					["CLSID"] = "{AGM_84E}",
					["num"] = 2,
				},
				[5] = {
					["CLSID"] = "LAU_117_AGM_65F",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[4] = {
			["displayName"] = "Retribution DEAD",
			["name"] = "Retribution DEAD",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{B06DD79A-F21E-4EB9-BD9D-AB3844618C93}",
					["num"] = 5,
				},
				[2] = {
					["CLSID"] = "{AGM_84E}",
					["num"] = 4,
				},
				[3] = {
					["CLSID"] = "{HB_A6E_AERO1D}",
					["num"] = 3,
				},
				[4] = {
					["CLSID"] = "{AGM_84E}",
					["num"] = 2,
				},
				[5] = {
					["CLSID"] = "{B06DD79A-F21E-4EB9-BD9D-AB3844618C93}",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[5] = {
			["displayName"] = "Retribution CEAD",
			["name"] = "Retribution CEAD",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{HB_A6E_TALD_MER_4x}",
					["num"] = 5,
				},
				[2] = {
					["CLSID"] = "{HB_A6E_TALD_MER_2x}",
					["num"] = 4,
				},
				[3] = {
					["CLSID"] = "{HB_A6E_AERO1D}",
					["num"] = 3,
				},
				[4] = {
					["CLSID"] = "{HB_A6E_TALD_MER_2x}",
					["num"] = 2,
				},
				[5] = {
					["CLSID"] = "{HB_A6E_TALD_MER_4x}",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[6] = {
			["displayName"] = "Retribution BAI",
			["name"] = "Retribution BAI",
			["pylons"] = {
				[1] = {
					["CLSID"] = "LAU_117_AGM_65F",
					["num"] = 5,
				},
				[2] = {
					["CLSID"] = "LAU_117_AGM_65F",
					["num"] = 4,
				},
				[3] = {
					["CLSID"] = "{HB_A6E_AERO1D}",
					["num"] = 3,
				},
				[4] = {
					["CLSID"] = "LAU_117_AGM_65F",
					["num"] = 2,
				},
				[5] = {
					["CLSID"] = "LAU_117_AGM_65F",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[7] = {
			["displayName"] = "Retribution CAS",
			["name"] = "Retribution CAS",
			["pylons"] = {
				[1] = {
					["CLSID"] = "LAU_117_AGM_65F",
					["num"] = 5,
				},
				[2] = {
					["CLSID"] = "LAU_117_AGM_65F",
					["num"] = 4,
				},
				[3] = {
					["CLSID"] = "{HB_A6E_AERO1D}",
					["num"] = 3,
				},
				[4] = {
					["CLSID"] = "LAU_117_AGM_65F",
					["num"] = 2,
				},
				[5] = {
					["CLSID"] = "LAU_117_AGM_65F",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[8] = {
			["displayName"] = "Retribution Anti-ship",
			["name"] = "Retribution Anti-ship",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{AGM_84D}",
					["num"] = 5,
				},
				[2] = {
					["CLSID"] = "{AGM_84D}",
					["num"] = 4,
				},
				[3] = {
					["CLSID"] = "{HB_A6E_AERO1D}",
					["num"] = 3,
				},
				[4] = {
					["CLSID"] = "{AGM_84D}",
					["num"] = 2,
				},
				[5] = {
					["CLSID"] = "{AGM_84D}",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[9] = {
			["displayName"] = "Retribution SEAD Escort",
			["name"] = "Retribution SEAD Escort",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{B06DD79A-F21E-4EB9-BD9D-AB3844618C93}",
					["num"] = 5,
				},
				[2] = {
					["CLSID"] = "{AGM_84E}",
					["num"] = 4,
				},
				[3] = {
					["CLSID"] = "{HB_A6E_AERO1D}",
					["num"] = 3,
				},
				[4] = {
					["CLSID"] = "{AGM_84E}",
					["num"] = 2,
				},
				[5] = {
					["CLSID"] = "{B06DD79A-F21E-4EB9-BD9D-AB3844618C93}",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[10] = {
			["displayName"] = "Retribution Refueling",
			["name"] = "Retribution Refueling",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{HB_A6E_AERO1D}",
					["num"] = 5,
				},
				[2] = {
					["CLSID"] = "{HB_A6E_AERO1D}",
					["num"] = 4,
				},
				[3] = {
					["CLSID"] = "{HB_A6E_D704}",
					["num"] = 3,
				},
				[4] = {
					["CLSID"] = "{HB_A6E_AERO1D}",
					["num"] = 2,
				},
				[5] = {
					["CLSID"] = "{HB_A6E_AERO1D}",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[11] = {
			["displayName"] = "Retribution OCA/Runway",
			["name"] = "Retribution OCA/Runway",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{51F9AAE5-964F-4D21-83FB-502E3BFE5F8A}",
					["num"] = 5,
					["settings"] = {
						["01_prfx_arm_delay_ctrl_FMU139CB_LD"] = 4,
						["01_prfx_function_delay_ctrl_FMU139CB_LD"] = 0,
						["NFP_PRESID"] = "MDRN_B_A",
						["NFP_PRESVER"] = 2,
						["NFP_VIS_DrawArgNo_57"] = 0,
						["NFP_fuze_type_tail"] = "FMU139CB_LD",
						["laser_code"] = 1688,
					},
				},
				[2] = {
					["CLSID"] = "{51F9AAE5-964F-4D21-83FB-502E3BFE5F8A}",
					["num"] = 4,
					["settings"] = {
						["01_prfx_arm_delay_ctrl_FMU139CB_LD"] = 4,
						["01_prfx_function_delay_ctrl_FMU139CB_LD"] = 0,
						["NFP_PRESID"] = "MDRN_B_A",
						["NFP_PRESVER"] = 2,
						["NFP_VIS_DrawArgNo_57"] = 0,
						["NFP_fuze_type_tail"] = "FMU139CB_LD",
						["laser_code"] = 1688,
					},
				},
				[3] = {
					["CLSID"] = "{HB_A6E_AERO1D}",
					["num"] = 3,
				},
				[4] = {
					["CLSID"] = "{51F9AAE5-964F-4D21-83FB-502E3BFE5F8A}",
					["num"] = 2,
					["settings"] = {
						["01_prfx_arm_delay_ctrl_FMU139CB_LD"] = 4,
						["01_prfx_function_delay_ctrl_FMU139CB_LD"] = 0,
						["NFP_PRESID"] = "MDRN_B_A",
						["NFP_PRESVER"] = 2,
						["NFP_VIS_DrawArgNo_57"] = 0,
						["NFP_fuze_type_tail"] = "FMU139CB_LD",
						["laser_code"] = 1688,
					},
				},
				[5] = {
					["CLSID"] = "{51F9AAE5-964F-4D21-83FB-502E3BFE5F8A}",
					["num"] = 1,
					["settings"] = {
						["01_prfx_arm_delay_ctrl_FMU139CB_LD"] = 4,
						["01_prfx_function_delay_ctrl_FMU139CB_LD"] = 0,
						["NFP_PRESID"] = "MDRN_B_A",
						["NFP_PRESVER"] = 2,
						["NFP_VIS_DrawArgNo_57"] = 0,
						["NFP_fuze_type_tail"] = "FMU139CB_LD",
						["laser_code"] = 1688,
					},
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[12] = {
			["displayName"] = "Retribution OCA/Aircraft",
			["name"] = "Retribution OCA/Aircraft",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{HB_A6E_GBU12_MER_2x_RIGHT}",
					["num"] = 5,
					["settings"] = {
						["01_prfx_arm_delay_ctrl_FMU139CB_LD"] = 4,
						["01_prfx_function_delay_ctrl_FMU139CB_LD"] = 0,
						["NFP_PRESID"] = "MDRN_B_A",
						["NFP_PRESVER"] = 2,
						["NFP_VIS_DrawArgNo_57"] = 0,
						["NFP_fuze_type_tail"] = "FMU139CB_LD",
						["laser_code"] = 1688,
					},
				},
				[2] = {
					["CLSID"] = "{HB_A6E_GBU12_MER_2x_RIGHT}",
					["num"] = 4,
					["settings"] = {
						["01_prfx_arm_delay_ctrl_FMU139CB_LD"] = 4,
						["01_prfx_function_delay_ctrl_FMU139CB_LD"] = 0,
						["NFP_PRESID"] = "MDRN_B_A",
						["NFP_PRESVER"] = 2,
						["NFP_VIS_DrawArgNo_57"] = 0,
						["NFP_fuze_type_tail"] = "FMU139CB_LD",
						["laser_code"] = 1688,
					},
				},
				[3] = {
					["CLSID"] = "{HB_A6E_AERO1D}",
					["num"] = 3,
				},
				[4] = {
					["CLSID"] = "{HB_A6E_GBU12_MER_2x_LEFT}",
					["num"] = 2,
					["settings"] = {
						["01_prfx_arm_delay_ctrl_FMU139CB_LD"] = 4,
						["01_prfx_function_delay_ctrl_FMU139CB_LD"] = 0,
						["NFP_PRESID"] = "MDRN_B_A",
						["NFP_PRESVER"] = 2,
						["NFP_VIS_DrawArgNo_57"] = 0,
						["NFP_fuze_type_tail"] = "FMU139CB_LD",
						["laser_code"] = 1688,
					},
				},
				[5] = {
					["CLSID"] = "{HB_A6E_GBU12_MER_2x_LEFT}",
					["num"] = 1,
					["settings"] = {
						["01_prfx_arm_delay_ctrl_FMU139CB_LD"] = 4,
						["01_prfx_function_delay_ctrl_FMU139CB_LD"] = 0,
						["NFP_PRESID"] = "MDRN_B_A",
						["NFP_PRESVER"] = 2,
						["NFP_VIS_DrawArgNo_57"] = 0,
						["NFP_fuze_type_tail"] = "FMU139CB_LD",
						["laser_code"] = 1688,
					},
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[13] = {
			["displayName"] = "Retribution Armed Recon",
			["name"] = "Retribution Armed Recon",
			["pylons"] = {
				[1] = {
					["CLSID"] = "LAU_117_AGM_65F",
					["num"] = 5,
				},
				[2] = {
					["CLSID"] = "{AGM_84E}",
					["num"] = 4,
				},
				[3] = {
					["CLSID"] = "{HB_A6E_AERO1D}",
					["num"] = 3,
				},
				[4] = {
					["CLSID"] = "{AGM_84E}",
					["num"] = 2,
				},
				[5] = {
					["CLSID"] = "LAU_117_AGM_65F",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
	},
	["unitType"] = "A6E",
}
return unitPayloads
