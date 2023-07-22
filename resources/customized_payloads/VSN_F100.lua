local unitPayloads = {
	["name"] = "VSN_F100",
	["payloads"] = {
		[1] = {
			["name"] = "Retribution BARCAP",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{9BFD8C90-F7AE-4e90-833B-BFD0CED0E536}",
					["num"] = 3,
				},
				[2] = {
					["CLSID"] = "{9BFD8C90-F7AE-4e90-833B-BFD0CED0E536}",
					["num"] = 4,
				},
				[3] = {
					["CLSID"] = "{VSN_F100500_ptb}",
					["num"] = 5,
				},
				[4] = {
					["CLSID"] = "{VSN_F100500_ptb}",
					["num"] = 7,
				},
				[5] = {
					["CLSID"] = "{9BFD8C90-F7AE-4e90-833B-BFD0CED0E536}",
					["num"] = 8,
				},
				[6] = {
					["CLSID"] = "{9BFD8C90-F7AE-4e90-833B-BFD0CED0E536}",
					["num"] = 9,
				},
			},
			["tasks"] = {
			},
		},
		[2] = {
			["name"] = "Retribution CAS",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{D5D51E24-348C-4702-96AF-97A714E72697}",
					["num"] = 3,
				},
				[2] = {
					["CLSID"] = "{D5D51E24-348C-4702-96AF-97A714E72697}",
					["num"] = 4,
				},
				[3] = {
					["CLSID"] = "{7A44FF09-527C-4B7E-B42B-3F111CFE50FB}",
					["num"] = 5,
					["settings"] = {
						["GUI_fuze_type"] = 1,
						["arm_delay_ctrl_FMU139CB_LD"] = 1,
						["function_delay_ctrl_FMU139CB_LD"] = 0,
					},
				},
				[4] = {
					["CLSID"] = "{7A44FF09-527C-4B7E-B42B-3F111CFE50FB}",
					["num"] = 7,
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
				[6] = {
					["CLSID"] = "{D5D51E24-348C-4702-96AF-97A714E72697}",
					["num"] = 9,
				},
			},
			["tasks"] = {
			},
		},
		[3] = {
			["name"] = "Retribution Strike",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{9BFD8C90-F7AE-4e90-833B-BFD0CED0E536}",
					["num"] = 9,
				},
				[2] = {
					["CLSID"] = "{9BFD8C90-F7AE-4e90-833B-BFD0CED0E536}",
					["num"] = 3,
				},
				[3] = {
					["CLSID"] = "<CLEAN>",
					["num"] = 4,
				},
				[4] = {
					["CLSID"] = "<CLEAN>",
					["num"] = 8,
				},
				[5] = {
					["CLSID"] = "{BRU-42_3*Mk-83}",
					["num"] = 7,
				},
				[6] = {
					["CLSID"] = "{BRU-42_3*Mk-83}",
					["num"] = 5,
				},
			},
			["tasks"] = {
			},
		},
		[4] = {
			["name"] = "Retribution SEAD",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{0519A264-0AB6-11d6-9193-00A0249B6F00}",
					["num"] = 2,
				},
				[2] = {
					["CLSID"] = "{AGM_45A}",
					["num"] = 3,
				},
				[3] = {
					["CLSID"] = "{AGM_45A}",
					["num"] = 4,
				},
				[4] = {
					["CLSID"] = "{VSN_F100500_ptb}",
					["num"] = 5,
				},
				[5] = {
					["CLSID"] = "{VSN_F100500_ptb}",
					["num"] = 7,
				},
				[6] = {
					["CLSID"] = "{AGM_45A}",
					["num"] = 8,
				},
				[7] = {
					["CLSID"] = "{AGM_45A}",
					["num"] = 9,
				},
			},
			["tasks"] = {
			},
		},
		[5] = {
			["name"] = "Retribution SEAD Escort",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{0519A264-0AB6-11d6-9193-00A0249B6F00}",
					["num"] = 2,
				},
				[2] = {
					["CLSID"] = "{9BFD8C90-F7AE-4e90-833B-BFD0CED0E536}",
					["num"] = 3,
				},
				[3] = {
					["CLSID"] = "{AGM_45A}",
					["num"] = 4,
				},
				[4] = {
					["CLSID"] = "{AGM_45A}",
					["num"] = 8,
				},
				[5] = {
					["CLSID"] = "{9BFD8C90-F7AE-4e90-833B-BFD0CED0E536}",
					["num"] = 9,
				},
				[6] = {
					["CLSID"] = "{VSN_F100500_ptb}",
					["num"] = 7,
				},
				[7] = {
					["CLSID"] = "{VSN_F100500_ptb}",
					["num"] = 5,
				},
			},
			["tasks"] = {
			},
		},
		[6] = {
			["name"] = "Retribution DEAD",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{SB_F105_BRU_41A_M117_6}",
					["num"] = 7,
				},
				[2] = {
					["CLSID"] = "{SB_F105_BRU_41A_M117_6}",
					["num"] = 5,
				},
				[3] = {
					["CLSID"] = "{9BFD8C90-F7AE-4e90-833B-BFD0CED0E536}",
					["num"] = 9,
				},
				[4] = {
					["CLSID"] = "{9BFD8C90-F7AE-4e90-833B-BFD0CED0E536}",
					["num"] = 3,
				},
				[5] = {
					["CLSID"] = "<CLEAN>",
					["num"] = 4,
				},
				[6] = {
					["CLSID"] = "<CLEAN>",
					["num"] = 8,
				},
			},
			["tasks"] = {
			},
		},
		[7] = {
			["name"] = "Retribution Anti-ship",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{AGM_45A}",
					["num"] = 3,
				},
				[2] = {
					["CLSID"] = "{AGM_45A}",
					["num"] = 4,
				},
				[3] = {
					["CLSID"] = "{AGM_45A}",
					["num"] = 8,
				},
				[4] = {
					["CLSID"] = "{AGM_45A}",
					["num"] = 9,
				},
				[5] = {
					["CLSID"] = "{VSN_F100500_ptb}",
					["num"] = 7,
				},
				[6] = {
					["CLSID"] = "{VSN_F100500_ptb}",
					["num"] = 5,
				},
				[7] = {
					["CLSID"] = "{0519A264-0AB6-11d6-9193-00A0249B6F00}",
					["num"] = 2,
				},
			},
			["tasks"] = {
			},
		},
		[8] = {
			["name"] = "Retribution Escort",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{VSN_F1001000_ptb}",
					["num"] = 4,
				},
				[2] = {
					["CLSID"] = "{VSN_F1001000_ptb}",
					["num"] = 8,
				},
				[3] = {
					["CLSID"] = "<CLEAN>",
					["num"] = 7,
				},
				[4] = {
					["CLSID"] = "<CLEAN>",
					["num"] = 5,
				},
				[5] = {
					["CLSID"] = "{9BFD8C90-F7AE-4e90-833B-BFD0CED0E536}",
					["num"] = 9,
				},
				[6] = {
					["CLSID"] = "{9BFD8C90-F7AE-4e90-833B-BFD0CED0E536}",
					["num"] = 3,
				},
			},
			["tasks"] = {
			},
		},
		[9] = {
			["name"] = "Retribution OCA/Runway",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{AB8B8299-F1CC-4359-89B5-2172E0CF4A5A}",
					["num"] = 3,
					["settings"] = {
						["GUI_fuze_type"] = 1,
						["arm_delay_ctrl_FMU139CB_LD"] = 1,
						["function_delay_ctrl_FMU139CB_LD"] = 0,
					},
				},
				[2] = {
					["CLSID"] = "{7A44FF09-527C-4B7E-B42B-3F111CFE50FB}",
					["num"] = 8,
					["settings"] = {
						["GUI_fuze_type"] = 1,
						["arm_delay_ctrl_FMU139CB_LD"] = 1,
						["function_delay_ctrl_FMU139CB_LD"] = 0,
					},
				},
				[3] = {
					["CLSID"] = "{VSN_F100500_ptb}",
					["num"] = 7,
				},
				[4] = {
					["CLSID"] = "{VSN_F100500_ptb}",
					["num"] = 5,
				},
				[5] = {
					["CLSID"] = "{7A44FF09-527C-4B7E-B42B-3F111CFE50FB}",
					["num"] = 4,
					["settings"] = {
						["GUI_fuze_type"] = 1,
						["arm_delay_ctrl_FMU139CB_LD"] = 1,
						["function_delay_ctrl_FMU139CB_LD"] = 0,
					},
				},
				[6] = {
					["CLSID"] = "{AB8B8299-F1CC-4359-89B5-2172E0CF4A5A}",
					["num"] = 9,
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
			["name"] = "Retribution OCA/Aircraft",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{LAU3_FFAR_MK1HE}",
					["num"] = 9,
				},
				[2] = {
					["CLSID"] = "{VSN_F1001000_ptb}",
					["num"] = 8,
				},
				[3] = {
					["CLSID"] = "{LAU3_FFAR_MK1HE}",
					["num"] = 7,
				},
				[4] = {
					["CLSID"] = "{LAU3_FFAR_MK1HE}",
					["num"] = 5,
				},
				[5] = {
					["CLSID"] = "{VSN_F1001000_ptb}",
					["num"] = 4,
				},
				[6] = {
					["CLSID"] = "{LAU3_FFAR_MK1HE}",
					["num"] = 3,
				},
			},
			["tasks"] = {
			},
		},
		[11] = {
			["name"] = "Retribution Fighter sweep",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{9BFD8C90-F7AE-4e90-833B-BFD0CED0E536}",
					["num"] = 9,
				},
				[2] = {
					["CLSID"] = "{9BFD8C90-F7AE-4e90-833B-BFD0CED0E536}",
					["num"] = 8,
				},
				[3] = {
					["CLSID"] = "<CLEAN>",
					["num"] = 7,
				},
				[4] = {
					["CLSID"] = "<CLEAN>",
					["num"] = 5,
				},
				[5] = {
					["CLSID"] = "{9BFD8C90-F7AE-4e90-833B-BFD0CED0E536}",
					["num"] = 4,
				},
				[6] = {
					["CLSID"] = "{9BFD8C90-F7AE-4e90-833B-BFD0CED0E536}",
					["num"] = 3,
				},
			},
			["tasks"] = {
			},
		},
		[12] = {
			["name"] = "Retribution Intercept",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{9BFD8C90-F7AE-4e90-833B-BFD0CED0E536}",
					["num"] = 3,
				},
				[2] = {
					["CLSID"] = "{9BFD8C90-F7AE-4e90-833B-BFD0CED0E536}",
					["num"] = 9,
				},
				[3] = {
					["CLSID"] = "{VSN_F1001000_ptb}",
					["num"] = 4,
				},
				[4] = {
					["CLSID"] = "<CLEAN>",
					["num"] = 5,
				},
				[5] = {
					["CLSID"] = "{VSN_F1001000_ptb}",
					["num"] = 8,
				},
				[6] = {
					["CLSID"] = "<CLEAN>",
					["num"] = 7,
				},
			},
			["tasks"] = {
			},
		},
	},
	["tasks"] = {
	},
	["unitType"] = "VSN_F100",
}
return unitPayloads
