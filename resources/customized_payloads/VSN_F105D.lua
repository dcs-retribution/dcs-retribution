local unitPayloads = {
	["name"] = "VSN_F105D",
	["payloads"] = {
		[1] = {
			["name"] = "Retribution TARCAP",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{VSN_F105_LAU105_AIM9P}",
					["num"] = 4,
				},
				[2] = {
					["CLSID"] = "<CLEAN>",
					["num"] = 5,
				},
				[3] = {
					["CLSID"] = "{VSN_F105G_Center_PTB}",
					["num"] = 6,
				},
				[4] = {
					["CLSID"] = "<CLEAN>",
					["num"] = 7,
				},
				[5] = {
					["CLSID"] = "{VSN_F105_LAU105_AIM9P}",
					["num"] = 8,
				},
			},
			["tasks"] = {
				[1] = 11,
			},
		},
		[2] = {
			["name"] = "Retribution CAS",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{D5D51E24-348C-4702-96AF-97A714E72697}",
					["num"] = 4,
				},
				[2] = {
					["CLSID"] = "{D5D51E24-348C-4702-96AF-97A714E72697}",
					["num"] = 8,
				},
				[3] = {
					["CLSID"] = "{VSN_F105_MK82_6}",
					["num"] = 5,
				},
				[4] = {
					["CLSID"] = "{VSN_F105_MK82_6}",
					["num"] = 7,
				},
				[5] = {
					["CLSID"] = "{VSN_F105G_Center_PTB}",
					["num"] = 6,
				},
			},
			["tasks"] = {
				[1] = 11,
			},
		},
		[3] = {
			["name"] = "Retribution Strike",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{7A44FF09-527C-4B7E-B42B-3F111CFE50FB}",
					["num"] = 4,
					["settings"] = {
						["GUI_fuze_type"] = 1,
						["arm_delay_ctrl_FMU139CB_LD"] = 4,
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
					["CLSID"] = "{VSN_F105G_Center_PTB}",
					["num"] = 6,
				},
				[4] = {
					["CLSID"] = "{7A44FF09-527C-4B7E-B42B-3F111CFE50FB}",
					["num"] = 5,
					["settings"] = {
						["GUI_fuze_type"] = 1,
						["arm_delay_ctrl_FMU139CB_LD"] = 1,
						["function_delay_ctrl_FMU139CB_LD"] = 0,
					},
				},
				[5] = {
					["CLSID"] = "{7A44FF09-527C-4B7E-B42B-3F111CFE50FB}",
					["num"] = 7,
					["settings"] = {
						["GUI_fuze_type"] = 1,
						["arm_delay_ctrl_FMU139CB_LD"] = 1,
						["function_delay_ctrl_FMU139CB_LD"] = 0,
					},
				},
			},
			["tasks"] = {
				[1] = 11,
			},
		},
		[4] = {
			["name"] = "Retribution SEAD",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{AGM_45A}",
					["num"] = 4,
				},
				[2] = {
					["CLSID"] = "<CLEAN>",
					["num"] = 5,
				},
				[3] = {
					["CLSID"] = "{VSN_F105G_Center_PTB}",
					["num"] = 6,
				},
				[4] = {
					["CLSID"] = "<CLEAN>",
					["num"] = 7,
				},
				[5] = {
					["CLSID"] = "{AGM_45A}",
					["num"] = 8,
				},
			},
			["tasks"] = {
				[1] = 11,
			},
		},
		[5] = {
			["name"] = "Retribution Intercept",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{VSN_F105_LAU105_AIM9P}",
					["num"] = 8,
				},
				[2] = {
					["CLSID"] = "{VSN_F105_LAU105_AIM9P}",
					["num"] = 4,
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
					["CLSID"] = "<CLEAN>",
					["num"] = 6,
				},
			},
			["tasks"] = {
			},
		},
		[6] = {
			["name"] = "Retribution DEAD",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{AB8B8299-F1CC-4359-89B5-2172E0CF4A5A}",
					["num"] = 8,
					["settings"] = {
						["GUI_fuze_type"] = 1,
						["arm_delay_ctrl_FMU139CB_LD"] = 1,
						["function_delay_ctrl_FMU139CB_LD"] = 0,
					},
				},
				[2] = {
					["CLSID"] = "{AB8B8299-F1CC-4359-89B5-2172E0CF4A5A}",
					["num"] = 4,
					["settings"] = {
						["GUI_fuze_type"] = 1,
						["arm_delay_ctrl_FMU139CB_LD"] = 1,
						["function_delay_ctrl_FMU139CB_LD"] = 0,
					},
				},
				[3] = {
					["CLSID"] = "{AB8B8299-F1CC-4359-89B5-2172E0CF4A5A}",
					["num"] = 5,
					["settings"] = {
						["GUI_fuze_type"] = 1,
						["arm_delay_ctrl_FMU139CB_LD"] = 1,
						["function_delay_ctrl_FMU139CB_LD"] = 0,
					},
				},
				[4] = {
					["CLSID"] = "{AB8B8299-F1CC-4359-89B5-2172E0CF4A5A}",
					["num"] = 7,
					["settings"] = {
						["GUI_fuze_type"] = 1,
						["arm_delay_ctrl_FMU139CB_LD"] = 1,
						["function_delay_ctrl_FMU139CB_LD"] = 0,
					},
				},
				[5] = {
					["CLSID"] = "{AB8B8299-F1CC-4359-89B5-2172E0CF4A5A}",
					["num"] = 6,
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
		[7] = {
			["name"] = "Retribution Escort",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{9BFD8C90-F7AE-4e90-833B-BFD0CED0E536}",
					["num"] = 4,
				},
				[2] = {
					["CLSID"] = "{9BFD8C90-F7AE-4e90-833B-BFD0CED0E536}",
					["num"] = 8,
				},
				[3] = {
					["CLSID"] = "{VSN_F105G_Center_PTB}",
					["num"] = 6,
				},
				[4] = {
					["CLSID"] = "<CLEAN>",
					["num"] = 5,
				},
				[5] = {
					["CLSID"] = "<CLEAN>",
					["num"] = 7,
				},
			},
			["tasks"] = {
			},
		},
		[8] = {
			["name"] = "Retribution OCA/Runway",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{D5D51E24-348C-4702-96AF-97A714E72697}",
					["num"] = 4,
				},
				[2] = {
					["CLSID"] = "{VSN_F105_MK82_6}",
					["num"] = 5,
				},
				[3] = {
					["CLSID"] = "{VSN_F105_MK82_6}",
					["num"] = 6,
				},
				[4] = {
					["CLSID"] = "{VSN_F105_MK82_6}",
					["num"] = 7,
				},
				[5] = {
					["CLSID"] = "{D5D51E24-348C-4702-96AF-97A714E72697}",
					["num"] = 8,
				},
			},
			["tasks"] = {
			},
		},
		[9] = {
			["name"] = "Retribution OCA/Aircraft",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{LAU3_FFAR_MK1HE}",
					["num"] = 4,
				},
				[2] = {
					["CLSID"] = "{LAU3_FFAR_MK1HE}",
					["num"] = 5,
				},
				[3] = {
					["CLSID"] = "{VSN_F105G_Center_PTB}",
					["num"] = 6,
				},
				[4] = {
					["CLSID"] = "{LAU3_FFAR_MK1HE}",
					["num"] = 7,
				},
				[5] = {
					["CLSID"] = "{LAU3_FFAR_MK1HE}",
					["num"] = 8,
				},
			},
			["tasks"] = {
			},
		},
		[10] = {
			["name"] = "Retribution SEAD Sweep",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{AGM_45A}",
					["num"] = 4,
				},
				[2] = {
					["CLSID"] = "{VSN_F105G_PTB}",
					["num"] = 5,
				},
				[3] = {
					["CLSID"] = "{VSN_F105G_PTB}",
					["num"] = 7,
				},
				[4] = {
					["CLSID"] = "{AGM_45A}",
					["num"] = 8,
				},
				[5] = {
					["CLSID"] = "<CLEAN>",
					["num"] = 6,
				},
			},
			["tasks"] = {
			},
		},
		[11] = {
			["name"] = "Retribution BAI",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{LAU3_FFAR_MK5HEAT}",
					["num"] = 4,
				},
				[2] = {
					["CLSID"] = "{LAU3_FFAR_MK5HEAT}",
					["num"] = 8,
				},
				[3] = {
					["CLSID"] = "{VSN_F105_MK82_6}",
					["num"] = 5,
				},
				[4] = {
					["CLSID"] = "{VSN_F105_MK82_6}",
					["num"] = 7,
				},
				[5] = {
					["CLSID"] = "{VSN_F105G_Center_PTB}",
					["num"] = 6,
				},
			},
			["tasks"] = {
			},
		},
		[12] = {
			["name"] = "Retribution Anti-ship",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{AGM_45A}",
					["num"] = 4,
				},
				[2] = {
					["CLSID"] = "{AGM_45A}",
					["num"] = 8,
				},
				[3] = {
					["CLSID"] = "{VSN_F105G_PTB}",
					["num"] = 7,
				},
				[4] = {
					["CLSID"] = "{VSN_F105G_PTB}",
					["num"] = 5,
				},
				[5] = {
					["CLSID"] = "<CLEAN>",
					["num"] = 6,
				},
			},
			["tasks"] = {
			},
		},
	},
	["tasks"] = {
	},
	["unitType"] = "VSN_F105D",
}
return unitPayloads
