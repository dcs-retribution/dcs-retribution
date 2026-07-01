from dcs import unittype

from game.modsupport import vehiclemod

# Unit data targets the High Digit SAMs "Ultimate Compilation"
# (https://github.com/dcs-sams/HighDigitSAMs-Ultimate-Compilation, v1.4.3+),
# the maintained successor of the original HighDigitSAMs v1.4.0. Detection and
# threat ranges are read from the mod's own Database lua files (launcher threat
# = missile distanceMax; tracker detection = the vehicle-file tracking range),
# with search-radar detection sanity-banded to match the values the original
# extension used for the same radar families.
#
# RETIRED UNITS: classes below marked "retired" no longer exist in the Ultimate
# Compilation (DCS core gained vanilla KS-19 / SON-9 / Igla-S; some S-300PS
# radars were renamed). They are kept registered ONLY so pre-migration saves
# unpickle; do not reference them in factions, presets, or layouts.


@vehiclemod
class AAA_SON_9_Fire_Can(unittype.VehicleType):
    # Retired in Ultimate Compilation (vanilla SON-9 replaces it).
    id = "Fire Can radar"
    name = "AAA SON-9 Fire Can"
    detection_range = 35000
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class AAA_100mm_KS_19(unittype.VehicleType):
    # Retired in Ultimate Compilation (vanilla KS-19 replaces it).
    id = "KS19"
    name = "AAA 100mm KS-19"
    detection_range = 0
    threat_range = 15000
    air_weapon_dist = 15000


@vehiclemod
class SAM_SA_10B_S_300PS_54K6_CP(unittype.VehicleType):
    id = "S-300PS SA-10B 54K6 cp"
    name = "SAM SA-10B S-300PS 54K6 CP"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class SAM_SA_10B_S_300PS_5P85SE_LN(unittype.VehicleType):
    id = "S-300PS 5P85SE_mod ln"
    name = "SAM SA-10B S-300PS 5P85SE LN "
    detection_range = 0
    threat_range = 75000
    air_weapon_dist = 75000


@vehiclemod
class SAM_SA_10B_S_300PS_5P85SU_LN(unittype.VehicleType):
    id = "S-300PS 5P85SU_mod ln"
    name = "SAM SA-10B S-300PS 5P85SU LN "
    detection_range = 0
    threat_range = 75000
    air_weapon_dist = 75000


@vehiclemod
class SAM_SA_10__5V55RUD__S_300PS_LN_5P85CE(unittype.VehicleType):
    # Retired in Ultimate Compilation (the S-300PT 5P85-1 LN replaces it).
    id = "S-300PS 5P85CE ln"
    name = "SAM SA-10 (5V55RUD) S-300PS LN 5P85CE"
    detection_range = 0
    threat_range = 90000
    air_weapon_dist = 90000


@vehiclemod
class SAM_SA_10__5V55RUD__S_300PS_LN_5P85DE(unittype.VehicleType):
    id = "S-300PS 5P85DE ln"
    name = "SAM SA-10 (5V55RUD) S-300PS LN 5P85DE"
    detection_range = 0
    threat_range = 90000
    air_weapon_dist = 90000


@vehiclemod
class SAM_SA_10B_S_300PS_30N6_TR(unittype.VehicleType):
    id = "S-300PS 30N6 TRAILER tr"
    name = "SAM SA-10B S-300PS 30N6 TR"
    detection_range = 160000
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class SAM_SA_10B_S_300PS_40B6M_TR(unittype.VehicleType):
    # Retired in Ultimate Compilation (renamed: 30N6 MAST tr replaces it).
    id = "S-300PS SA-10B 40B6M MAST tr"
    name = "SAM SA-10B S-300PS 40B6M TR"
    detection_range = 160000
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class SAM_SA_10B_S_300PS_40B6MD_SR(unittype.VehicleType):
    # Retired in Ultimate Compilation (renamed: 76N6E sr replaces it).
    id = "S-300PS SA-10B 40B6MD MAST sr"
    name = "SAM SA-10B S-300PS 40B6MD SR"
    detection_range = 60000
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class SAM_SA_10B_S_300PS_64H6E_SR(unittype.VehicleType):
    # Retired in Ultimate Compilation (renamed: 64H6E MOD sr replaces it).
    id = "S-300PS 64H6E TRAILER sr"
    name = "SAM SA-10B S-300PS 64H6E SR"
    detection_range = 160000
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class SAM_SA_20_S_300PMU1_CP_54K6(unittype.VehicleType):
    id = "S-300PMU1 54K6 cp"
    name = "SAM SA-20 S-300PMU1 CP 54K6"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class SAM_SA_20_S_300PMU1_TR_30N6E(unittype.VehicleType):
    id = "S-300PMU1 40B6M tr"
    name = "SAM SA-20 S-300PMU1 TR 30N6E"
    detection_range = 160000
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class SAM_SA_20_S_300PMU1_TR_30N6E_truck(unittype.VehicleType):
    id = "S-300PMU1 30N6E tr"
    name = "SAM SA-20 S-300PMU1 TR 30N6E(truck)"
    detection_range = 160000
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class SAM_SA_20_S_300PMU1_SR_5N66E(unittype.VehicleType):
    id = "S-300PMU1 40B6MD sr"
    name = "SAM SA-20 S-300PMU1 SR 5N66E"
    detection_range = 120000
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class SAM_SA_20_S_300PMU1_SR_64N6E(unittype.VehicleType):
    id = "S-300PMU1 64N6E sr"
    name = "SAM SA-20 S-300PMU1 SR 64N6E"
    detection_range = 300000
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class SAM_SA_20_S_300PMU1_LN_5P85CE(unittype.VehicleType):
    id = "S-300PMU1 5P85CE ln"
    name = "SAM SA-20 S-300PMU1 LN 5P85CE"
    detection_range = 0
    threat_range = 150000
    air_weapon_dist = 150000


@vehiclemod
class SAM_SA_20_S_300PMU1_LN_5P85DE(unittype.VehicleType):
    id = "S-300PMU1 5P85DE ln"
    name = "SAM SA-20 S-300PMU1 LN 5P85DE"
    detection_range = 0
    threat_range = 150000
    air_weapon_dist = 150000


@vehiclemod
class SAM_SA_20B_S_300PMU2_CP_54K6E2(unittype.VehicleType):
    id = "S-300PMU2 54K6E2 cp"
    name = "SAM SA-20B S-300PMU2 CP 54K6E2"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class SAM_SA_20B_S_300PMU2_TR_92H6E_truck(unittype.VehicleType):
    id = "S-300PMU2 92H6E tr"
    name = "SAM SA-20B S-300PMU2 TR 92H6E(truck)"
    detection_range = 270000
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class SAM_SA_20B_S_300PMU2_SR_64N6E2(unittype.VehicleType):
    id = "S-300PMU2 64H6E2 sr"
    name = "SAM SA-20B S-300PMU2 SR 64N6E2"
    detection_range = 330000
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class SAM_SA_20B_S_300PMU2_LN_5P85SE2(unittype.VehicleType):
    id = "S-300PMU2 5P85SE2 ln"
    name = "SAM SA-20B S-300PMU2 LN 5P85SE2"
    detection_range = 0
    threat_range = 200000
    air_weapon_dist = 200000


@vehiclemod
class SAM_SA_12_S_300V_9S457_CP(unittype.VehicleType):
    id = "S-300V 9S457 cp"
    name = "SAM SA-12 S-300V 9S457 CP"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class SAM_SA_12_S_300V_9A82_LN(unittype.VehicleType):
    id = "S-300V 9A82 ln"
    name = "SAM SA-12 S-300V 9A82 LN"
    detection_range = 0
    threat_range = 100000
    air_weapon_dist = 100000


@vehiclemod
class SAM_SA_12_S_300V_9A83_LN(unittype.VehicleType):
    id = "S-300V 9A83 ln"
    name = "SAM SA-12 S-300V 9A83 LN"
    detection_range = 0
    threat_range = 75000
    air_weapon_dist = 75000


@vehiclemod
class SAM_SA_12_S_300V_9S15_SR(unittype.VehicleType):
    id = "S-300V 9S15 sr"
    name = "SAM SA-12 S-300V 9S15 SR"
    detection_range = 240000
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class SAM_SA_12_S_300V_9S19_SR(unittype.VehicleType):
    id = "S-300V 9S19 sr"
    name = "SAM SA-12 S-300V 9S19 SR"
    detection_range = 175000
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class SAM_SA_12_S_300V_9S32_TR(unittype.VehicleType):
    id = "S-300V 9S32 tr"
    name = "SAM SA-12 S-300V 9S32 TR"
    detection_range = 150000
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class SAM_SA_23_S_300VM_9S457ME_CP(unittype.VehicleType):
    id = "S-300VM 9S457ME cp"
    name = "SAM SA-23 S-300VM 9S457ME CP"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class SAM_SA_23_S_300VM_9S15M2_SR(unittype.VehicleType):
    id = "S-300VM 9S15M2 sr"
    name = "SAM SA-23 S-300VM 9S15M2 SR"
    detection_range = 320000
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class SAM_SA_23_S_300VM_9S19M2_SR(unittype.VehicleType):
    id = "S-300VM 9S19M2 sr"
    name = "SAM SA-23 S-300VM 9S19M2 SR"
    detection_range = 310000
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class SAM_SA_23_S_300VM_9S32ME_TR(unittype.VehicleType):
    id = "S-300VM 9S32ME tr"
    name = "SAM SA-23 S-300VM 9S32ME TR"
    detection_range = 230000
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class SAM_SA_23_S_300VM_9A83ME_LN(unittype.VehicleType):
    id = "S-300VM 9A83ME ln"
    name = "SAM SA-23 S-300VM 9A83ME LN"
    detection_range = 0
    threat_range = 90000
    air_weapon_dist = 90000


@vehiclemod
class SAM_SA_23_S_300VM_9A82ME_LN(unittype.VehicleType):
    id = "S-300VM 9A82ME ln"
    name = "SAM SA-23 S-300VM 9A82ME LN"
    detection_range = 0
    threat_range = 200000
    air_weapon_dist = 200000


@vehiclemod
class SAM_SA_17_Buk_M1_2_LN_9A310M1_2(unittype.VehicleType):
    id = "SA-17 Buk M1-2 LN 9A310M1-2"
    name = "SAM SA-17 Buk M1-2 LN 9A310M1-2"
    detection_range = 120000
    threat_range = 50000
    air_weapon_dist = 50000


@vehiclemod
class SAM_SA_2__V759__LN_SM_90(unittype.VehicleType):
    id = "S_75M_Volhov_V759"
    name = "SAM SA-2 (V759) LN SM-90"
    detection_range = 0
    threat_range = 50000
    air_weapon_dist = 50000


@vehiclemod
class SAM_HQ_2_LN_SM_90(unittype.VehicleType):
    id = "HQ_2_Guideline_LN"
    name = "SAM HQ-2 LN SM-90"
    detection_range = 0
    threat_range = 50000
    air_weapon_dist = 50000


@vehiclemod
class SAM_SA_3__V_601P__LN_5P73(unittype.VehicleType):
    id = "5p73 V-601P ln"
    name = "SAM SA-3 (V-601P) LN 5P73"
    detection_range = 0
    threat_range = 18000
    air_weapon_dist = 18000


@vehiclemod
class SAM_SA_24_Igla_S_manpad(unittype.VehicleType):
    # Retired in Ultimate Compilation (vanilla SA-18 Igla-S replaces it).
    id = "SA-24 Igla-S manpad"
    name = "SAM SA-24 Igla-S manpad"
    detection_range = 5000
    threat_range = 6000
    air_weapon_dist = 6000


@vehiclemod
class SAM_SA_14_Strela_3_manpad(unittype.VehicleType):
    id = "SA-14 Strela-3 manpad"
    name = "SAM SA-14 Strela-3 manpad"
    detection_range = 5000
    threat_range = 4500
    air_weapon_dist = 4500


@vehiclemod
class Polyana_D4M1_C2_node(unittype.VehicleType):
    id = "polyana-d4m1 cp"
    name = "Polyana-D4M1 C2 node"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class _34Ya6E_Gazetchik_E_decoy(unittype.VehicleType):
    id = "34Ya6E Gazetchik E decoy"
    name = "34Ya6E Gazetchik E decoy"
    detection_range = 20000
    threat_range = 0
    air_weapon_dist = 0


# --- Ultimate Compilation additions (v1.4.3+) ------------------------------
# S-300PS/PT renamed + new pieces.


@vehiclemod
class SAM_SA_10B_S_300PS_30N6_MAST_TR(unittype.VehicleType):
    id = "S-300PS SA-10B 30N6 MAST tr"
    name = "SAM SA-10B S-300PS 30N6 TR (mast)"
    detection_range = 160000
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class SAM_SA_10B_S_300PS_76N6E_SR(unittype.VehicleType):
    id = "S-300PS SA-10B 76N6E sr"
    name = "SAM SA-10B S-300PS 76N6E SR"
    detection_range = 120000
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class SAM_SA_10B_S_300PS_64H6E_MOD_SR(unittype.VehicleType):
    id = "S-300PS 64H6E MOD sr"
    name = "SAM SA-10B S-300PS 64H6E SR (truck)"
    detection_range = 200000
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class SAM_SA_10A_S_300PT_LN_5P85_1(unittype.VehicleType):
    id = "S-300PS 5P85_1_mod ln"
    name = "SAM SA-10A S-300PT LN 5P85-1"
    detection_range = 0
    threat_range = 47000
    air_weapon_dist = 47000


@vehiclemod
class SAM_SA_20B_S_300PMU2_TR_92H6E_mast(unittype.VehicleType):
    id = "S-300PMU2 40B6M tr"
    name = "SAM SA-20B S-300PMU2 TR 92H6E(mast)"
    detection_range = 270000
    threat_range = 0
    air_weapon_dist = 0


# S-400 / SA-21 Growler.


@vehiclemod
class SAM_SA_21_S_400_CP_55K6(unittype.VehicleType):
    id = "S-400 55K6 cp"
    name = "SAM SA-21 S-400 CP 55K6"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class SAM_SA_21_S_400_SR_91N6E(unittype.VehicleType):
    id = "S-400 91N6E sr"
    name = "SAM SA-21 S-400 SR 91N6E"
    detection_range = 340000
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class SAM_SA_21_S_400_SR_96L6E(unittype.VehicleType):
    id = "S-400 96L6E sr"
    name = "SAM SA-21 S-400 SR 96L6E (truck)"
    detection_range = 300000
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class SAM_SA_21_S_400_SR_96L6E_mast(unittype.VehicleType):
    id = "S-400 96L6E mast sr"
    name = "SAM SA-21 S-400 SR 96L6E (mast)"
    detection_range = 300000
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class SAM_SA_21_S_400_TR_92N6E(unittype.VehicleType):
    id = "S-400 92N6E tr"
    name = "SAM SA-21 S-400 TR 92N6E (truck)"
    detection_range = 410000
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class SAM_SA_21_S_400_TR_92N6E_mast(unittype.VehicleType):
    id = "S-400 92N6E mast tr"
    name = "SAM SA-21 S-400 TR 92N6E (mast)"
    detection_range = 410000
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class SAM_SA_21_S_400_LN_51P6A(unittype.VehicleType):
    id = "S-400 51P6A ln"
    name = "SAM SA-21 S-400 LN 51P6A (48N6DM)"
    detection_range = 0
    threat_range = 250000
    air_weapon_dist = 250000


@vehiclemod
class SAM_SA_21_S_400_LN_51P6A_9M96E2(unittype.VehicleType):
    id = "S-400 51P6A (9M96E2) ln"
    name = "SAM SA-21 S-400 LN 51P6A (9M96E2)"
    detection_range = 0
    threat_range = 120000
    air_weapon_dist = 120000


@vehiclemod
class SAM_SA_21_S_400_LN_51P6A_40N6E(unittype.VehicleType):
    id = "S-400 51P6A (40N6E) ln"
    name = "SAM SA-21 S-400 LN 51P6A (40N6E)"
    detection_range = 0
    threat_range = 400000
    air_weapon_dist = 400000


# S-300V4 (the modernised SA-23 / "Antey-4000" family).


@vehiclemod
class SAM_SA_23_S_300V4_9S457_2E_CP(unittype.VehicleType):
    id = "S-300V4 9S457-2E cp"
    name = "SAM SA-23 S-300V4 9S457-2E CP"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class SAM_SA_23_S_300V4_9S15MDE_SR(unittype.VehicleType):
    id = "S-300V4 9S15MDE sr"
    name = "SAM SA-23 S-300V4 9S15MDE SR"
    detection_range = 330000
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class SAM_SA_23_S_300V4_9S19M_1E_SR(unittype.VehicleType):
    id = "S-300V4 9S19M-1E sr"
    name = "SAM SA-23 S-300V4 9S19M-1E SR"
    detection_range = 310000
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class SAM_SA_23_S_300V4_9S32M_1E_TR(unittype.VehicleType):
    id = "S-300V4 9S32M-1E tr"
    name = "SAM SA-23 S-300V4 9S32M-1E TR"
    detection_range = 400000
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class SAM_SA_23_S_300V4_9A82M_2E_LN(unittype.VehicleType):
    id = "S-300V4 9A82M-2E ln"
    name = "SAM SA-23 S-300V4 9A82M-2E LN"
    detection_range = 0
    threat_range = 380000
    air_weapon_dist = 380000


@vehiclemod
class SAM_SA_23_S_300V4_9A84M_2E_LN(unittype.VehicleType):
    id = "S-300V4 9A84M-2E ln"
    name = "SAM SA-23 S-300V4 9A84M-2E LN"
    detection_range = 0
    threat_range = 380000
    air_weapon_dist = 380000


@vehiclemod
class SAM_SA_23_S_300V4_9A83M_2E_LN(unittype.VehicleType):
    id = "S-300V4 9A83M-2E ln"
    name = "SAM SA-23 S-300V4 9A83M-2E LN"
    detection_range = 0
    threat_range = 150000
    air_weapon_dist = 150000


# SA-22 Pantsir-SM (self-contained gun/missile SHORAD).


@vehiclemod
class SAM_SA_22_Pantsir_SM(unittype.VehicleType):
    id = "Pantsir_SM"
    name = "SAM SA-22 Pantsir-SM"
    detection_range = 75000
    threat_range = 30000
    air_weapon_dist = 30000


# SAMP/T (Aster 30) battery.


@vehiclemod
class SAMPT_C2_MC(unittype.VehicleType):
    id = "SAMPT_MC"
    name = "SAMP/T C2"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class SAMPT_ECS_ME(unittype.VehicleType):
    id = "SAMPT_ME"
    name = "SAMP/T ECS (ME)"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class SAMPT_EPP_MGE(unittype.VehicleType):
    id = "SAMPT_MGE"
    name = "SAMP/T EPP"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class SAMPT_ARABEL_STR(unittype.VehicleType):
    id = "SAMPT_MRI_ARABEL"
    name = "SAMP/T ARABEL STR"
    detection_range = 120000
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class SAMPT_GF300_STR(unittype.VehicleType):
    id = "SAMPT_MRI_GF300"
    name = "SAMP/T Ground Fire 300 STR"
    detection_range = 400000
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class SAMPT_TEL_Block_1(unittype.VehicleType):
    id = "SAMPT_MLT_Blk1"
    name = "SAMP/T TEL Block 1"
    detection_range = 0
    threat_range = 120000
    air_weapon_dist = 120000


@vehiclemod
class SAMPT_TEL_Block_1NT(unittype.VehicleType):
    id = "SAMPT_MLT_Blk1NT"
    name = "SAMP/T TEL Block 1NT"
    detection_range = 0
    threat_range = 150000
    air_weapon_dist = 150000


# Early-generation MANPADS.


@vehiclemod
class SAM_SA_7_Strela_2_manpad(unittype.VehicleType):
    id = "SA-7 Strela-2 manpad"
    name = "SAM SA-7 Strela-2 manpad"
    detection_range = 5000
    threat_range = 6000
    air_weapon_dist = 6000


@vehiclemod
class SAM_SA_7B_Strela_2M_manpad(unittype.VehicleType):
    id = "SA-7b Strela-2M manpad"
    name = "SAM SA-7B Strela-2M manpad"
    detection_range = 5000
    threat_range = 8500
    air_weapon_dist = 8500


# Early-warning radars.


@vehiclemod
class EWR_P_37_Bar_Lock(unittype.VehicleType):
    id = "EWR P-37 BAR LOCK"
    name = "EWR P-37 Bar Lock"
    detection_range = 350000
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class EWR_55G6U_Nebo_U(unittype.VehicleType):
    id = "EWR 55G6U NEBO-U"
    name = "EWR 55G6U Nebo-U"
    detection_range = 500000
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class EWR_1L119_Nebo_SVU(unittype.VehicleType):
    id = "EWR 1L119 Nebo-SVU"
    name = "EWR 1L119 Nebo-SVU"
    detection_range = 400000
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class EWR_Generic_radar_tower(unittype.VehicleType):
    id = "EWR Generic radar tower"
    name = "EWR Generic radar tower"
    detection_range = 350000
    threat_range = 0
    air_weapon_dist = 0


# ERO pack vehicles (site props + insurgent technicals).


@vehiclemod
class ERO_SA2_SNR75(unittype.VehicleType):
    id = "ERO_SA2_SNR75"
    name = "ERO SA-2 SNR-75 Fan Song"
    detection_range = 100000
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class ERO_SA2_Trailer(unittype.VehicleType):
    id = "ERO_SA2_Trailer"
    name = "ERO SA-2 missile trailer"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class ERO_5S99_Trailer(unittype.VehicleType):
    id = "ERO_5S99_Trailer"
    name = "ERO 5S99 missile trailer"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class ERO_Toyota_Camo(unittype.VehicleType):
    id = "ERO_Toyota_Camo"
    name = "ERO Toyota Camo"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class AAA_ZU_23_Toyota_technical(unittype.VehicleType):
    id = "ERO_ZU23_Toyota"
    name = "AAA ZU-23 Toyota technical"
    detection_range = 0
    threat_range = 2500
    air_weapon_dist = 2500


@vehiclemod
class AAA_ZU_23_Toyota_armored_technical(unittype.VehicleType):
    id = "ERO_ZU23_Toyota_armored"
    name = "AAA ZU-23 Toyota armored technical"
    detection_range = 0
    threat_range = 2500
    air_weapon_dist = 2500


@vehiclemod
class AAA_ZU_23_Insurgent_ERO(unittype.VehicleType):
    id = "ERO_ZU23_Insurgent"
    name = "AAA ZU-23 Insurgent (ERO)"
    detection_range = 0
    threat_range = 2500
    air_weapon_dist = 2500
