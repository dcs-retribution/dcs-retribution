local unitPayloads = {
	["name"] = "Su-35S",
	["payloads"] = {
		[1] = {
			["displayName"] = "Retribution CAP",
			["name"] = "CAP",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{0519A264-0AB6-11d6-9193-00A0249B6F00}", -- Fantasmagoria
					["num"] = 12,
				},
				[2] = {
					["CLSID"] = "{SU35_L265_R}", -- L265 ECM
					["num"] = 1,
				},
				[3] = {
					["CLSID"] = "{Su30-R-74M2-AA}",
					["num"] = 2,
				},
				[4] = {
					["CLSID"] = "{Su30-R-74M2-AA}",
					["num"] = 11,
				},
				[5] = {
					["CLSID"] = "{SU30_R27ET}",
					["num"] = 10,
				},
				[6] = {
					["CLSID"] = "{SU30_R27ET}",
					["num"] = 3,
				},
				[7] = {
					["CLSID"] = "{SU30_R77M}",
					["num"] = 4,
				},
				[8] = {
					["CLSID"] = "{SU30-R37M-AA}",
					["num"] = 5,
				},
				[9] = {
					["CLSID"] = "{DUAL_77M}",
					["num"] = 6,
				},
				[10] = {
					["CLSID"] = "{DUAL_77M}",
					["num"] = 7,
				},
				[11] = {
					["CLSID"] = "{SU30-R37M-AA}",
					["num"] = 8,
				},
				[12] = {
					["CLSID"] = "{SU30_R77M}",
					["num"] = 9,
				},
			},
			["tasks"] = {
				[1] = 18, -- escort
				[2] = 19, -- sweep
				[3] = 11, -- CAP
			},
		},
		[2] = {
			["displayName"] = "Retribution Intercept",
			["name"] = "Retribution Intercept",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{0519A264-0AB6-11d6-9193-00A0249B6F00}", -- Fantasmagoria
					["num"] = 12,
				},
				[2] = {
					["CLSID"] = "{SU35_L265_R}", -- L265 ECM
					["num"] = 1,
				},
				[3] = {
					["CLSID"] = "{Su30-R-74M2-AA}",
					["num"] = 2,
				},
				[4] = {
					["CLSID"] = "{Su30-R-74M2-AA}",
					["num"] = 11,
				},
				[5] = {
					["CLSID"] = "{SU30-R37M-AA}",
					["num"] = 10,
				},
				[6] = {
					["CLSID"] = "{SU30-R37M-AA}",
					["num"] = 9,
				},
				[7] = {
					["CLSID"] = "{SU30-R37M-AA}",
					["num"] = 3,
				},
				[8] = {
					["CLSID"] = "{SU30-R37M-AA}",
					["num"] = 4,
				},
				[9] = {
					["CLSID"] = "{SU30_R77M}",
					["num"] = 5,
				},
				[10] = {
					["CLSID"] = "{DUAL_77M}",
					["num"] = 6,
				},
				[11] = {
					["CLSID"] = "{DUAL_77M}",
					["num"] = 7,
				},
				[12] = {
					["CLSID"] = "{SU30_R77M}",
					["num"] = 8,
				},
			},
			["tasks"] = {
				[1] = 10, -- intercept
			},
		},
		[3] = {
			["displayName"] = "Retribution SEAD",
			["name"] = "Retribution SEAD",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{0519A264-0AB6-11d6-9193-00A0249B6F00}", -- Fantasmagoria
					["num"] = 12,
				},
				[2] = {
					["CLSID"] = "{SU35_L265_R}", -- L265 ECM
					["num"] = 1,
				},
				[3] = {
					["CLSID"] = "{Su30-R-74M2-AA}",
					["num"] = 2,
				},
				[4] = {
					["CLSID"] = "{Su30-R-74M2-AA}",
					["num"] = 11,
				},
				[5] = {
					["CLSID"] = "{DUAL_77M}",
					["num"] = 7,
				},
				[6] = {
					["CLSID"] = "{DUAL_77M}",
					["num"] = 6,
				},
				[7] = {
					["CLSID"] = "{SU30_KH31PD}",
					["num"] = 8,
				},
				[8] = {
					["CLSID"] = "{SU30_KH31PD}",
					["num"] = 5,
				},
				[9] = {
					["CLSID"] = "{SU30_KH59MK2}",
					["num"] = 4,
				},
				[10] = {
					["CLSID"] = "{SU30_KH59MK2}",
					["num"] = 3,
				},
				[11] = {
					["CLSID"] = "{SU30_KH59MK2}",
					["num"] = 9,
				},
				[12] = {
					["CLSID"] = "{SU30_KH59MK2}",
					["num"] = 10,
				},
			},
			["tasks"] = {
				[1] = 29,
			},
		},
	},
	["tasks"] = {
	},
	["unitType"] = "Su-35S",
}
return unitPayloads
