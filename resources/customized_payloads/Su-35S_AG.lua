local unitPayloads = {
	["name"] = "Su-35S-AG",
	["payloads"] = {
		[1] = {
			["displayName"] = "Retribution Strike",
			["name"] = "Retribution Strike",
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
					["num"] = 11,
				},
				[4] = {
					["CLSID"] = "{Su30-R-74M2-AA}",
					["num"] = 2,
				},
				[5] = {
					["CLSID"] = "{DUAL_77M}", -- middle pylons
					["num"] = 6,
				},
				[6] = {
					["CLSID"] = "{DUAL_77M}",
					["num"] = 7,
				},
				[7] = {
					["CLSID"] = "{E2C426E3-8B10-4E09-B733-9CDC26520F48}", -- KAB-500 TV guided
					["num"] = 10,
				},
				[8] = {
					["CLSID"] = "{E2C426E3-8B10-4E09-B733-9CDC26520F48}",
					["num"] = 9,
				},
				[9] = {
					["CLSID"] = "{E2C426E3-8B10-4E09-B733-9CDC26520F48}",
					["num"] = 8,
				},
				[10] = {
					["CLSID"] = "{E2C426E3-8B10-4E09-B733-9CDC26520F48}",
					["num"] = 5,
				},
				[11] = {
					["CLSID"] = "{E2C426E3-8B10-4E09-B733-9CDC26520F48}",
					["num"] = 4,
				},
				[12] = {
					["CLSID"] = "{E2C426E3-8B10-4E09-B733-9CDC26520F48}",
					["num"] = 3,
				},
			},
			["tasks"] = {
				[1] = 33, -- strike
				[2] = 32, -- ground attack
				[3] = 31, -- CAS
			},
		},
		[2] = {
			["displayName"] = "Retribution BAI",
			["name"] = "Retribution BAI",
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
					["num"] = 11,
				},
				[4] = {
					["CLSID"] = "{Su30-R-74M2-AA}",
					["num"] = 2,
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
					["CLSID"] = "{601C99F7-9AF3-4ed7-A565-F8B8EC0D7AAC}", -- KH-29 TV guided
					["num"] = 10,
				},
				[8] = {
					["CLSID"] = "{601C99F7-9AF3-4ed7-A565-F8B8EC0D7AAC}",
					["num"] = 9,
				},
				[9] = {
					["CLSID"] = "{601C99F7-9AF3-4ed7-A565-F8B8EC0D7AAC}",
					["num"] = 8,
				},
				[10] = {
					["CLSID"] = "{601C99F7-9AF3-4ed7-A565-F8B8EC0D7AAC}",
					["num"] = 5,
				},
				[11] = {
					["CLSID"] = "{601C99F7-9AF3-4ed7-A565-F8B8EC0D7AAC}",
					["num"] = 4,
				},
				[12] = {
					["CLSID"] = "{601C99F7-9AF3-4ed7-A565-F8B8EC0D7AAC}",
					["num"] = 3,
				},
			},
			["tasks"] = {
				[1] = 31, -- CAS
				[2] = 32, -- ground attack
			},
		},
		[3] = {
			["displayName"] = "Retribution Antiship",
			["name"] = "Retribution Antiship",
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
					["CLSID"] = "{SU30_KH31AD}",
					["num"] = 10,
				},
				[6] = {
					["CLSID"] = "{SU30_KH31AD}",
					["num"] = 3,
				},
				[7] = {
					["CLSID"] = "{SU30_KH31AD}",
					["num"] = 4,
				},
				[8] = {
					["CLSID"] = "{SU30_KH31AD}",
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
					["CLSID"] = "{SU30_KH31AD}",
					["num"] = 8,
				},
				[12] = {
					["CLSID"] = "{SU30_KH31AD}",
					["num"] = 9,
				},
			},
			["tasks"] = {
				[1] = 30, -- antiship
			},
		},
		[4] = {
			["name"] = "Retribution CAS",
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
					["num"] = 11,
				},
				[4] = {
					["CLSID"] = "{Su30-R-74M2-AA}",
					["num"] = 2,
				},
				[5] = {
					["CLSID"] = "{TWIN_B_8M1_S_8KOM}", -- twin ung HEAT rocket
					["num"] = 3,
				},
				[6] = {
					["CLSID"] = "{TWIN_B_8M1_S_8KOM}",
					["num"] = 10,
				},
				[7] = {
					["CLSID"] = "{601C99F7-9AF3-4ed7-A565-F8B8EC0D7AAC}", -- KH-29 TV guided
					["num"] = 9,
				},
				[8] = {
					["CLSID"] = "{E2C426E3-8B10-4E09-B733-9CDC26520F48}", -- KAB-500Kr
					["num"] = 8,
				},
				[9] = {
					["CLSID"] = "{DUAL_77M}",
					["num"] = 7,
				},
				[10] = {
					["CLSID"] = "{DUAL_77M}",
					["num"] = 6,
				},
				[11] = {
					["CLSID"] = "{E2C426E3-8B10-4E09-B733-9CDC26520F48}", -- KAB-500Kr
					["num"] = 5,
				},
				[12] = {
					["CLSID"] = "{601C99F7-9AF3-4ed7-A565-F8B8EC0D7AAC}", -- KH-29 TV guided
					["num"] = 4,
				},
			},
			["tasks"] = {
				[1] = 31, -- CAS
				[2] = 32, -- ground attack
			},
		},
		[5] = {
			["displayName"] = "Retribution OCA/Aircraft",
			["name"] = "Retribution OCA/Aircraft",
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
					["num"] = 11,
				},
				[4] = {
					["CLSID"] = "{Su30-R-74M2-AA}",
					["num"] = 2,
				},
				[5] = {
					["CLSID"] = "{DUAL_77M}",
					["num"] = 6,
				},
				[6] = {
					["CLSID"] = "{DUAL_77M}",
					["num"] = 7,
				},
				[7] = {
					["CLSID"] = "{96A7F676-F956-404A-AD04-F33FB2C74884}", -- KMGU-2 HE/Frag dispenser
					["num"] = 10,
				},
				[8] = {
					["CLSID"] = "{96A7F676-F956-404A-AD04-F33FB2C74884}",
					["num"] = 3,
				},
				[9] = {
					["CLSID"] = "{96A7F676-F956-404A-AD04-F33FB2C74881}", -- KMGU-2 HEAT/AP
					["num"] = 9,
				},
				[10] = {
					["CLSID"] = "{96A7F676-F956-404A-AD04-F33FB2C74881}",
					["num"] = 4,
				},
				[11] = {
					["CLSID"] = "{53BE25A4-C86C-4571-9BC0-47D668349595}", -- 250kg OFAB x6
					["num"] = 8,
				},
				[12] = {
					["CLSID"] = "{53BE25A4-C86C-4571-9BC0-47D668349595}",
					["num"] = 5,
				},
			},
			["tasks"] = {
				[1] = 32,
				[2] = 31,
			},
		},
		[6] = {
			["displayName"] = "Retribution OCA/Runway",
			["name"] = "Retribution OCA/Runway",
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
					["num"] = 11,
				},
				[4] = {
					["CLSID"] = "{Su30-R-74M2-AA}",
					["num"] = 2,
				},
				[5] = {
					["CLSID"] = "{DUAL_77M}",
					["num"] = 6,
				},
				[6] = {
					["CLSID"] = "{DUAL_77M}",
					["num"] = 7,
				},
				[7] = {
					["CLSID"] = "{BD289E34-DF84-4C5E-9220-4B14C346E79D}", -- concrete piercing bombs
					["num"] = 10,
				},
				[8] = {
					["CLSID"] = "{BD289E34-DF84-4C5E-9220-4B14C346E79D}",
					["num"] = 9,
				},
				[9] = {
					["CLSID"] = "{BD289E34-DF84-4C5E-9220-4B14C346E79D}",
					["num"] = 8,
				},
				[10] = {
					["CLSID"] = "{BD289E34-DF84-4C5E-9220-4B14C346E79D}",
					["num"] = 5,
				},
				[11] = {
					["CLSID"] = "{BD289E34-DF84-4C5E-9220-4B14C346E79D}",
					["num"] = 4,
				},
				[12] = {
					["CLSID"] = "{BD289E34-DF84-4C5E-9220-4B14C346E79D}",
					["num"] = 3,
				},
			},
			["tasks"] = {
				[1] = 34,
			},
		},
		[7] = {
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
		[8] = {
			["displayName"] = "Retribution DEAD",
			["name"] = "Retribution DEAD",
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
					["CLSID"] = "{601C99F7-9AF3-4ed7-A565-F8B8EC0D7AAC}", -- Kh-29T
					["num"] = 8,
				},
				[8] = {
					["CLSID"] = "{601C99F7-9AF3-4ed7-A565-F8B8EC0D7AAC}",
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
				[2] = 32,
			},
		},
	},
	["tasks"] = {
	},
	["unitType"] = "Su-35S-AG",
}
return unitPayloads
