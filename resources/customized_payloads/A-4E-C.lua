local unitPayloads = {
	["name"] = "A-4E-C",
	["payloads"] = {
		[1] = {
			["displayName"] = "Retribution Anti-ship",
			["name"] = "Retribution Anti-ship",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{AGM_45A}",
					["num"] = 1,
				},
				[2] = {
					["CLSID"] = "{AGM_45A}",
					["num"] = 2,
				},
				[3] = {
					["CLSID"] = "{AGM_45A}",
					["num"] = 4,
				},
				[4] = {
					["CLSID"] = "{AGM_45A}",
					["num"] = 5,
				},
				[5] = {
					["CLSID"] = "{DFT-400gal}",
					["num"] = 3,
				},
			},
			["tasks"] = {
				[1] = 31,
			},
		},
		[2] = {
			["name"] = "Retribution SEAD",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{AGM_45A}",
					["num"] = 5,
				},
				[2] = {
					["CLSID"] = "{AGM_45A}",
					["num"] = 4,
				},
				[3] = {
					["CLSID"] = "{AGM_45A}",
					["num"] = 2,
				},
				[4] = {
					["CLSID"] = "{AGM_45A}",
					["num"] = 1,
				},
				[5] = {
					["CLSID"] = "{DFT-300gal}",
					["num"] = 3,
				},
			},
			["tasks"] = {
				[1] = 31,
			},
		},
		[3] = {
			["name"] = "Retribution OCA/Runway",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{BCE4E030-38E9-423E-98ED-24BE3DA87C32}",
					["num"] = 1,
					["settings"] = {
						["GUI_fuze_type"] = 1,
						["arm_delay_ctrl_FMU139CB_LD"] = 1,
						["function_delay_ctrl_FMU139CB_LD"] = 0,
					},
				},
				[2] = {
					["CLSID"] = "{BCE4E030-38E9-423E-98ED-24BE3DA87C32}",
					["num"] = 5,
					["settings"] = {
						["GUI_fuze_type"] = 1,
						["arm_delay_ctrl_FMU139CB_LD"] = 1,
						["function_delay_ctrl_FMU139CB_LD"] = 0,
					},
				},
				[3] = {
					["CLSID"] = "{DFT-300gal_LR}",
					["num"] = 2,
				},
				[4] = {
					["CLSID"] = "{DFT-300gal_LR}",
					["num"] = 4,
				},
				[5] = {
					["CLSID"] = "{Mk-83_TER_3_C}",
					["num"] = 3,
				},
			},
			["tasks"] = {
				[1] = 31,
			},
		},
		[4] = {
			["name"] = "Retribution CAP",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{AIM-9P5-ON-ADAPTER}",
					["num"] = 5,
				},
				[2] = {
					["CLSID"] = "{AIM-9P5-ON-ADAPTER}",
					["num"] = 1,
				},
				[3] = {
					["CLSID"] = "{AIM-9P5-ON-ADAPTER}",
					["num"] = 2,
				},
				[4] = {
					["CLSID"] = "{AIM-9P5-ON-ADAPTER}",
					["num"] = 4,
				},
				[5] = {
					["CLSID"] = "{DFT-400gal}",
					["num"] = 3,
				},
			},
			["tasks"] = {
				[1] = 31,
			},
		},
		[5] = {
			["name"] = "Retribution CAS",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{AIM-9P5-ON-ADAPTER}",
					["num"] = 1,
				},
				[2] = {
					["CLSID"] = "{AIM-9P5-ON-ADAPTER}",
					["num"] = 5,
				},
				[3] = {
					["CLSID"] = "{Mk-81SE_MER_5_R}",
					["num"] = 4,
				},
				[4] = {
					["CLSID"] = "{Mk-81SE_MER_5_L}",
					["num"] = 2,
				},
				[5] = {
					["CLSID"] = "{Mk-82 Snakeye_MER_6_C}",
					["num"] = 3,
				},
			},
			["tasks"] = {
				[1] = 31,
			},
		},
		[6] = {
			["displayName"] = "Retribution Strike",
			["name"] = "Retribution Strike",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{DFT-400gal}",
					["num"] = 3,
				},
				[2] = {
					["CLSID"] = "{AB8B8299-F1CC-4359-89B5-2172E0CF4A5A}",
					["num"] = 2,
					["settings"] = {
						["GUI_fuze_type"] = 1,
						["arm_delay_ctrl_FMU139CB_LD"] = 4,
						["function_delay_ctrl_FMU139CB_LD"] = 0.06,
					},
				},
				[3] = {
					["CLSID"] = "{AB8B8299-F1CC-4359-89B5-2172E0CF4A5A}",
					["num"] = 4,
					["settings"] = {
						["GUI_fuze_type"] = 1,
						["arm_delay_ctrl_FMU139CB_LD"] = 4,
						["function_delay_ctrl_FMU139CB_LD"] = 0.06,
					},
				},
				[4] = {
					["CLSID"] = "{AIM-9P5-ON-ADAPTER}",
					["num"] = 1,
				},
				[5] = {
					["CLSID"] = "{AIM-9P5-ON-ADAPTER}",
					["num"] = 5,
				},
			},
			["tasks"] = {
				[1] = 31,
			},
		},
		[7] = {
			["name"] = "Retribution OCA/Aircraft",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{LAU3_FFAR_MK1HE}",
					["num"] = 1,
				},
				[2] = {
					["CLSID"] = "{LAU3_FFAR_MK1HE}",
					["num"] = 5,
				},
				[3] = {
					["CLSID"] = "{CBU-2B/A_TER_2_L}",
					["num"] = 2,
				},
				[4] = {
					["CLSID"] = "{CBU-2B/A_TER_2_R}",
					["num"] = 4,
				},
				[5] = {
					["CLSID"] = "{Mk4 HIPEG}",
					["num"] = 3,
				},
			},
			["tasks"] = {
			},
		},
		[8] = {
			["name"] = "Retribution BAI",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{mk77mod1}",
					["num"] = 1,
				},
				[2] = {
					["CLSID"] = "{mk77mod1}",
					["num"] = 5,
				},
				[3] = {
					["CLSID"] = "{Mk-20_TER_2_L}",
					["num"] = 2,
				},
				[4] = {
					["CLSID"] = "{Mk-20_TER_2_R}",
					["num"] = 4,
				},
				[5] = {
					["CLSID"] = "{LAU-10 ZUNI_TER_3_C}",
					["num"] = 3,
				},
			},
			["tasks"] = {
			},
		},
		[9] = {
			["name"] = "Retribution DEAD",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{BCE4E030-38E9-423E-98ED-24BE3DA87C32}",
					["num"] = 1,
					["settings"] = {
						["GUI_fuze_type"] = 1,
						["arm_delay_ctrl_FMU139CB_LD"] = 1,
						["function_delay_ctrl_FMU139CB_LD"] = 0,
					},
				},
				[2] = {
					["CLSID"] = "{Mk-82_TER_2_L}",
					["num"] = 2,
				},
				[3] = {
					["CLSID"] = "{Mk-83_TER_3_C}",
					["num"] = 3,
				},
				[4] = {
					["CLSID"] = "{Mk-82_TER_2_R}",
					["num"] = 4,
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
			},
		},
		[10] = {
			["name"] = "Retribution SEAD Escort",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{AIM-9P5-ON-ADAPTER}",
					["num"] = 1,
				},
				[2] = {
					["CLSID"] = "{AIM-9P5-ON-ADAPTER}",
					["num"] = 5,
				},
				[3] = {
					["CLSID"] = "{AGM_45A}",
					["num"] = 2,
				},
				[4] = {
					["CLSID"] = "{AGM_45A}",
					["num"] = 4,
				},
				[5] = {
					["CLSID"] = "{DFT-300gal}",
					["num"] = 3,
				},
			},
			["tasks"] = {
			},
		},
		[11] = {
			["name"] = "Retribution SEAD Sweep",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{AGM_45A}",
					["num"] = 1,
				},
				[2] = {
					["CLSID"] = "{AGM_45A}",
					["num"] = 2,
				},
				[3] = {
					["CLSID"] = "{AGM_45A}",
					["num"] = 4,
				},
				[4] = {
					["CLSID"] = "{AGM_45A}",
					["num"] = 5,
				},
				[5] = {
					["CLSID"] = "{DFT-300gal}",
					["num"] = 3,
				},
			},
			["tasks"] = {
			},
		},
	},
	["tasks"] = {
	},
	["unitType"] = "A-4E-C",
}
return unitPayloads
