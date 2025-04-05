from typing import Dict, List, Set, Any

from dcs import task
from dcs.planes import PlaneType
from dcs.unitpropertydescription import UnitPropertyDescription
from dcs.weapons_data import Weapons

from game.modsupport import planemod
from pydcs_extensions.weapon_injector import inject_weapons


class WeaponsFA18EFG:
    STA_01_WNGTP_LAU127_1x_AIM_9M_Sidewinder_IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_01_SW_1X_AIM-9}",
        "name": " [ STA 01	  | WNGTP | LAU127 ] - 1x AIM-9M Sidewinder IR AAM",
        "weight": 85.72,
    }
    STA_01_WNGTP_LAU127_1x_AIM_9X_Sidewinder_IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_01_SW_1X_AIM-9X}",
        "name": " [ STA 01	  | WNGTP | LAU127 ] - 1x AIM-9X Sidewinder IR AAM",
        "weight": 84.46,
    }
    STA_01_WNGTP_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod = {
        "clsid": "{SUPERHORNET_PYLON_01_PD_1X_ais-pod-t50}",
        "name": " [ STA 01	  | WNGTP | LAU127 ] - 1x AN/ASQ-T50(V)1 TCTS Pod",
        "weight": 62.6,
    }
    STA_01_WNGTP_LAU127_1x_Captive_AIM_9M_for_ACM = {
        "clsid": "{SUPERHORNET_PYLON_01_SW_1X_CATM-9M}",
        "name": " [ STA 01	  | WNGTP | LAU127 ] - 1x Captive AIM-9M for ACM",
        "weight": 85.73,
    }
    STA_02_SUU79_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_PD_1X_ais-pod-t50}",
        "name": " [ STA 02	  | SUU79 | LAU127 ] - 1x AN/ASQ-T50(V)1 TCTS Pod",
        "weight": 107.9,
    }
    STA_02_SUU79_LAU127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X = {
        "clsid": "{SUPERHORNET_PYLON_03_LAU127}",
        "name": " [ STA 02	  | SUU79 | LAU127 ] - 1x Marvin LAU-127 Rail Launcher for AIM-120B/C/D and AIM9L/M/X",
        "weight": 45.3,
    }
    STA_02_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MK_1X_BDU-45B}",
        "name": " [ STA 02	  | SUU80 | BRU32   ] - 1x BDU-45B - 500lb Practice Bomb",
        "weight": 266.47,
    }
    STA_02_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MK_1X_BDU-45}",
        "name": " [ STA 02	  | SUU80 | BRU32   ] - 1x BDU-45 - 500lb Practice Bomb",
        "weight": 266.47,
    }
    STA_02_SUU80_BRU32_1x_CBU_99___490lbs__247_x_HEAT_Bomblets = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MK_1X_CBU-99}",
        "name": " [ STA 02	  | SUU80 | BRU32   ] - 1x CBU-99 - 490lbs, 247 x HEAT Bomblets",
        "weight": 56.47,
    }
    STA_02_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MK_1X_GBU-12}",
        "name": " [ STA 02	  | SUU80 | BRU32   ] - 1x GBU-12 - 500lb Laser Guided Bomb",
        "weight": 311.47,
    }
    STA_02_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MK_1X_GBU-16}",
        "name": " [ STA 02	  | SUU80 | BRU32   ] - 1x GBU-16 - 1000lb Laser Guided Bomb",
        "weight": 547.47,
    }
    STA_02_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MK_1X_GBU-32}",
        "name": " [ STA 02	  | SUU80 | BRU32   ] - 1x GBU-32(V)2/B - JDAM, 1000lb GPS Guided Bomb",
        "weight": 501.47,
    }
    STA_02_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MK_1X_GBU-38}",
        "name": " [ STA 02	  | SUU80 | BRU32   ] - 1x GBU-38 - JDAM, 500lb GPS Guided Bomb",
        "weight": 275.47,
    }
    STA_02_SUU80_BRU32_1x_GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MK_1X_GBU_54V}",
        "name": " [ STA 02	  | SUU80 | BRU32   ] - 1x GBU-54(V)1/B - LJDAM, 500lb Laser & GPS Guided Bomb LD",
        "weight": 287.47,
    }
    STA_02_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MK_1X_ROCKEYE}",
        "name": " [ STA 02	  | SUU80 | BRU32   ] - 1x Mk-20 Rockeye - 490lbs CBU, 247 x HEAT Bomblets",
        "weight": 256.47,
    }
    STA_02_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MK_1X_MK-82Y}",
        "name": " [ STA 02	  | SUU80 | BRU32   ] - 1x Mk-82Y - 500lb GP Chute Retarded HD",
        "weight": 266.47,
    }
    STA_02_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MK_1X_MK-82_Snakeye}",
        "name": " [ STA 02	  | SUU80 | BRU32   ] - 1x Mk-82 Snakeye - 500lb GP Bomb HD",
        "weight": 283.97,
    }
    STA_02_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MK_1X_MK-82}",
        "name": " [ STA 02	  | SUU80 | BRU32   ] - 1x Mk-82 - 500lb GP Bomb LD",
        "weight": 262.47,
    }
    STA_02_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MK_1X_MK-83}",
        "name": " [ STA 02	  | SUU80 | BRU32   ] - 1x Mk-83 - 1000lb GP Bomb LD",
        "weight": 488.47,
    }
    STA_02_SUU80_EMPTY = {
        "clsid": "{SUPERHORNET_PYLON_02_EMPTY}",
        "name": " [ STA 02	  | SUU80 | EMPTY ]",
        "weight": 0,
    }
    STA_02_SUU80_LA115_1x_AIM_7F_Sparrow_Semi_Active_Radar = {
        "clsid": "{GROWLER_PYLON_02_SP_1X_AIM-7F}",
        "name": " [ STA 02	  | SUU80 | LA115 ] - 1x AIM-7F Sparrow Semi-Active Radar",
        "weight": 319.87,
    }
    STA_02_SUU80_LA115_1x_AIM_7MH_Sparrow_Semi_Active_Radar = {
        "clsid": "{GROWLER_PYLON_02_SP_1X_AIM-7H}",
        "name": " [ STA 02	  | SUU80 | LA115 ] - 1x AIM-7MH Sparrow Semi-Active Radar",
        "weight": 319.87,
    }
    STA_02_SUU80_LA115_1x_AIM_7M_Sparrow_Semi_Active_Radar = {
        "clsid": "{GROWLER_PYLON_02_SP_1X_AIM-7M}",
        "name": " [ STA 02	  | SUU80 | LA115 ] - 1x AIM-7M Sparrow Semi-Active Radar",
        "weight": 319.87,
    }
    STA_02_SUU80_LA115_1x_AIM_7P_Sparrow_Semi_Active_Radar = {
        "clsid": "{GROWLER_PYLON_02_SP_1X_AIM-7P}",
        "name": " [ STA 02	  | SUU80 | LA115 ] - 1x AIM-7P Sparrow Semi-Active Radar",
        "weight": 319.87,
    }
    STA_02_SUU80_LA118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = {
        "clsid": "{GROWLER_PYLON_02_OB_AR_1X_AGM-88}",
        "name": " [ STA 02	  | SUU80 | LA118 ] - 1x AGM-88C HARM - High Speed Anti-Radiation Missile",
        "weight": 440.87,
    }
    STA_02_SUU80_LA127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = {
        "clsid": "{GROWLER_PYLON_02_OB_AM_1X_AIM-120}",
        "name": " [ STA 02	  | SUU80 | LA127 ] - 1x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 337.32,
    }
    STA_02_SUU80_LA127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = {
        "clsid": "{GROWLER_PYLON_02_OB_AM_1X_AIM-120C}",
        "name": " [ STA 02	  | SUU80 | LA127 ] - 1x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 340.95,
    }
    STA_02_SUU80_LA127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = {
        "clsid": "{GROWLER_PYLON_02_OB_AM_1X_AIM-120D}",
        "name": " [ STA 02	  | SUU80 | LA127 ] - 1x AIM-120D AMRAAM - Active Radar AAM (AI Only)",
        "weight": 341.87,
    }
    STA_02_SUU80_LA127_1x_AIM_9M_Sidewinder_IR_AAM = {
        "clsid": "{GROWLER_PYLON_02_OB_SW_1X_AIM-9}",
        "name": " [ STA 02	  | SUU80 | LA127 ] - 1x AIM-9M Sidewinder IR AAM",
        "weight": 265.19,
    }
    STA_02_SUU80_LA127_1x_AIM_9M_Sidewinder_IR_AAM_ = {
        "clsid": "{GROWLER_PYLON_03_OB_SW_1X_AIM-9}",
        "name": " [ STA 02	  | SUU80 | LA127 ] - 1x AIM-9M Sidewinder IR AAM",
        "weight": 137.82,
    }
    STA_02_SUU80_LA127_1x_AIM_9X_Sidewinder_IR_AAM = {
        "clsid": "{GROWLER_PYLON_02_OB_SW_1X_AIM-9X}",
        "name": " [ STA 02	  | SUU80 | LA127 ] - 1x AIM-9X Sidewinder IR AAM",
        "weight": 263.93,
    }
    STA_02_SUU80_LA127_1x_AIM_9X_Sidewinder_IR_AAM_ = {
        "clsid": "{GROWLER_PYLON_03_OB_SW_1X_AIM-9X}",
        "name": " [ STA 02	  | SUU80 | LA127 ] - 1x AIM-9X Sidewinder IR AAM",
        "weight": 136.56,
    }
    STA_02_SUU80_LA127_1x_AN_ASQ_T50_V_1_TCTS_Pod = {
        "clsid": "{GROWLER_PYLON_02_PD_ais-pod-t50}",
        "name": " [ STA 02	  | SUU80 | LA127 ] - 1x AN/ASQ-T50(V)1 TCTS Pod",
        "weight": 114.7,
    }
    STA_02_SUU80_LA127_1x_Captive_AIM_9M_for_ACM = {
        "clsid": "{GROWLER_PYLON_02_OB_SW_1X_C}",
        "name": " [ STA 02	  | SUU80 | LA127 ] - 1x Captive AIM-9M for ACM",
        "weight": 265.2,
    }
    STA_02_SUU80_LA127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X = {
        "clsid": "{GROWLER_PYLON_02_LAU127}",
        "name": " [ STA 02	  | SUU80 | LA127 ] - 1x Marvin LAU-127 Rail Launcher for AIM-120B/C/D and AIM9L/M/X",
        "weight": 52.1,
    }
    STA_02_SUU80_LA127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X_ = {
        "clsid": "{GROWLER_PYLON_03_OB_LAU127}",
        "name": " [ STA 02	  | SUU80 | LA127 ] - 1x Marvin LAU-127 Rail Launcher for AIM-120B/C/D and AIM9L/M/X",
        "weight": 52.1,
    }
    STA_02_SUU80_LAU115_1x_AIM_7F_Sparrow_Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_02_SP_1X_AIM-7F}",
        "name": " [ STA 02	  | SUU80 | LAU115 ] - 1x AIM-7F Sparrow Semi-Active Radar",
        "weight": 319.9,
    }
    STA_02_SUU80_LAU115_1x_AIM_7MH_Sparrow_Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_02_SP_1X_AIM-7H}",
        "name": " [ STA 02	  | SUU80 | LAU115 ] - 1x AIM-7MH Sparrow Semi-Active Radar",
        "weight": 319.9,
    }
    STA_02_SUU80_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_02_SP_1X_AIM-7M}",
        "name": " [ STA 02	  | SUU80 | LAU115 ] - 1x AIM-7M Sparrow Semi-Active Radar",
        "weight": 319.9,
    }
    STA_02_SUU80_LAU115_1x_AIM_7P_Sparrow_Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_02_SP_1X_AIM-7P}",
        "name": " [ STA 02	  | SUU80 | LAU115 ] - 1x AIM-7P Sparrow Semi-Active Radar",
        "weight": 319.9,
    }
    STA_02_SUU80_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MV_1X_AGM-65E}",
        "name": " [ STA 02	  | SUU80 | LAU117 ] - 1x AGM-65E - Maverick E (Laser ASM - Lg Whd)",
        "weight": 379.47,
    }
    STA_02_SUU80_LAU117_1x_AGM_65F___Maverick_F__IIR_ = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MV_1X_AGM-65F}",
        "name": " [ STA 02	  | SUU80 | LAU117 ] - 1x AGM-65F - Maverick F (IIR)",
        "weight": 394.47,
    }
    STA_02_SUU80_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MV_1X_CATM-65K}",
        "name": " [ STA 02	  | SUU80 | LAU117 ] - 1x CATM-65K - Captive Trg Round for Mav K (CCD), AI Only",
        "weight": 390.47,
    }
    STA_02_SUU80_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_AR_1X_AGM-88}",
        "name": " [ STA 02	  | SUU80 | LAU118 ] - 1x AGM-88C HARM - High Speed Anti-Radiation Missile",
        "weight": 440.87,
    }
    STA_02_SUU80_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_02_AM_1X_AIM-120}",
        "name": " [ STA 02	  | SUU80 | LAU127 ] - 1x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 209.95,
    }
    STA_02_SUU80_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_02_AM_1X_AIM-120C}",
        "name": " [ STA 02	  | SUU80 | LAU127 ] - 1x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 213.58,
    }
    STA_02_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_02_AM_1X_AIM-120D}",
        "name": " [ STA 02	  | SUU80 | LAU127 ] - 1x AIM-120D AMRAAM - Active Radar AAM (AI Only)",
        "weight": 214.5,
    }
    STA_02_SUU80_LAU127_1x_AIM_9M_Sidewinder_IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_02_SW_1X_AIM-9}",
        "name": " [ STA 02	  | SUU80 | LAU127 ] - 1x AIM-9M Sidewinder IR AAM",
        "weight": 137.82,
    }
    STA_02_SUU80_LAU127_1x_AIM_9X_Sidewinder_IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_02_SW_1X_AIM-9X}",
        "name": " [ STA 02	  | SUU80 | LAU127 ] - 1x AIM-9X Sidewinder IR AAM",
        "weight": 136.56,
    }
    STA_02_SUU80_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod = {
        "clsid": "{SUPERHORNET_PYLON_02_PD_1X_ais-pod-t50}",
        "name": " [ STA 02	  | SUU80 | LAU127 ] - 1x AN/ASQ-T50(V)1 TCTS Pod",
        "weight": 114.7,
    }
    STA_02_SUU80_LAU127_1x_Captive_AIM_9M_for_ACM = {
        "clsid": "{SUPERHORNET_PYLON_02_SW_1X_CATM-9M}",
        "name": " [ STA 02	  | SUU80 | LAU127 ] - 1x Captive AIM-9M for ACM",
        "weight": 137.83,
    }
    STA_02_SUU80_LAU127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X = {
        "clsid": "{SUPERHORNET_PYLON_02_LAU127}",
        "name": " [ STA 02	  | SUU80 | LAU127 ] - 1x Marvin LAU-127 Rail Launcher for AIM-120B/C/D and AIM9L/M/X",
        "weight": 52.1,
    }
    STA_02_03_79_80_LAU127_1x_1x_AIM_120B_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_OB_AM_2X_AIM-120}",
        "name": " [ STA 02/03 | 79/80 | LAU127 ] - 1x/1x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 547.3,
    }
    STA_02_03_79_80_LAU127_1x_1x_AIM_120C_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_OB_AM_2X_AIM-120C}",
        "name": " [ STA 02/03 | 79/80 | LAU127 ] - 1x/1x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 554.56,
    }
    STA_02_03_79_80_LAU127_1x_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_OB_AM_2X_AIM-120D}",
        "name": " [ STA 02/03 | 79/80 | LAU127 ] - 1x/1x AIM-120D AMRAAM - Active Radar AAM (AI Only)",
        "weight": 556.4,
    }
    STA_02_03_79_80_LAU127_1x_1x_AIM_9M_Sidewinder_IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_OB_SW_2X_AIM-9}",
        "name": " [ STA 02/03 | 79/80 | LAU127 ] - 1x/1x AIM-9M Sidewinder IR AAM",
        "weight": 403.04,
    }
    STA_02_03_79_80_LAU127_1x_1x_AIM_9X_Sidewinder_IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_OB_SW_2X_AIM-9X}",
        "name": " [ STA 02/03 | 79/80 | LAU127 ] - 1x/1x AIM-9X Sidewinder IR AAM",
        "weight": 400.52,
    }
    STA_03_SUU79_BRU32_1x_AN_ALQ_249_Mid_Band_Next_Generation_Jamming_Pod = {
        "clsid": "{GROWLER_PYLON_03_MB_ALQ_249_MID_BAND}",
        "name": " [ STA 03	  | SUU79 | BRU32 ] - 1x AN/ALQ-249 Mid Band Next Generation Jamming Pod",
        "weight": 534.47,
    }
    STA_03_SUU79_BRU32_1x_AN_ALQ_99_ICAP_III_High_Band_Jamming_Pod = {
        "clsid": "{GROWLER_PYLON_03_MB_ALQ_99_HI_BAND}",
        "name": " [ STA 03	  | SUU79 | BRU32 ] - 1x AN/ALQ-99 ICAP III High Band Jamming Pod",
        "weight": 465.383,
    }
    STA_03_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank = {
        "clsid": "{GROWLER_PYLON_02_MB_FT_FPU-12_Fueltank}",
        "name": " [ STA 03	  | SUU79 | BRU32 ] - 1x FPU-12/A Fuel Tank",
        "weight": 1384.47,
    }
    STA_03_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis = {
        "clsid": "{GROWLER_PYLON_02_MB_FT_FPU-12_FueltankHighVis}",
        "name": " [ STA 03	  | SUU79 | BRU32 ] - 1x FPU-12/A Fuel Tank - High Vis",
        "weight": 1384.47,
    }
    STA_03_SUU79_BRU32_1x_AGM_154A___JSOW_CEB__CBU_type_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_JS_1X_AGM-154A}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x AGM-154A - JSOW CEB (CBU-type)",
        "weight": 519.47,
    }
    STA_03_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_JS_1X_AGM-154C}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x AGM-154C - JSOW Unitary BROACH",
        "weight": 518.47,
    }
    STA_03_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_JS_1X_AGM-154C}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x AGM-154C - JSOW Unitary BROACH",
        "weight": 518.47,
    }
    STA_03_SUU79_BRU32_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_SM_1X_AGM-84E}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x AGM-84E Harpoon/SLAM (Stand-Off Land-Attack Missile)",
        "weight": 662.47,
    }
    STA_03_SUU79_BRU32_1x_ALQ_167_Countermeasures_System = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_PD_1X_ALQ-167}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x ALQ-167 Countermeasures System",
        "weight": 84.47,
    }
    STA_03_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_PD_1X_AWW-13}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x AN/AWW-13 Advanced Datalink Pod",
        "weight": 234.47,
    }
    STA_03_SUU79_BRU32_1x_BDU_45B___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_1X_BDU-45B}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x BDU-45B - 500lb Practice Bomb",
        "weight": 266.47,
    }
    STA_03_SUU79_BRU32_1x_BDU_45___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_1X_BDU-45}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x BDU-45 - 500lb Practice Bomb",
        "weight": 266.47,
    }
    STA_03_SUU79_BRU32_1x_CBU_99___490lbs__247_x_HEAT_Bomblets = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_1X_CBU-99}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x CBU-99 - 490lbs, 247 x HEAT Bomblets",
        "weight": 56.47,
    }
    STA_03_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_FT_FPU-12_Fueltank}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x FPU-12/A Fuel Tank",
        "weight": 1384.47,
    }
    STA_03_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_FT_FPU-12_FueltankHighVis}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x FPU-12/A Fuel Tank - High Vis",
        "weight": 1384.47,
    }
    STA_03_SUU79_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_MK_1X_GBU-10}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x GBU-10 - 2000lb Laser Guided Bomb",
        "weight": 946.47,
    }
    STA_03_SUU79_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_1X_GBU-10}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x GBU-10 - 2000lb Laser Guided Bomb",
        "weight": 946.47,
    }
    STA_03_SUU79_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_MK_1X_GBU-12}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x GBU-12 - 500lb Laser Guided Bomb",
        "weight": 311.47,
    }
    STA_03_SUU79_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_1X_GBU-12}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x GBU-12 - 500lb Laser Guided Bomb",
        "weight": 311.47,
    }
    STA_03_SUU79_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_MK_1X_GBU-16}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x GBU-16 - 1000lb Laser Guided Bomb",
        "weight": 547.47,
    }
    STA_03_SUU79_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_1X_GBU-16}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x GBU-16 - 1000lb Laser Guided Bomb",
        "weight": 547.47,
    }
    STA_03_SUU79_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_MK_1X_GBU-24}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x GBU-24A/B Paveway III - 2000lb Laser Guided Bomb",
        "weight": 968.47,
    }
    STA_03_SUU79_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_1X_GBU-24}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x GBU-24A/B Paveway III - 2000lb Laser Guided Bomb",
        "weight": 968.47,
    }
    STA_03_SUU79_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_MK_1X_GBU-31}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x GBU-31(V)1/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 968.47,
    }
    STA_03_SUU79_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_1X_GBU-31}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x GBU-31(V)1/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 968.47,
    }
    STA_03_SUU79_BRU32_1x_GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_1X_GBU-31_V_2B}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x GBU-31(V)2/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 968.47,
    }
    STA_03_SUU79_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_MK_1X_GBU-31V}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x GBU-31(V)3/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 1015.47,
    }
    STA_03_SUU79_BRU32_1x_GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_1X_GBU-31_V_4B}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x GBU-31(V)4/B - JDAM, 2000lb GPS Guided Penetrator Bomb",
        "weight": 1004.47,
    }
    STA_03_SUU79_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_1X_GBU-32}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x GBU-32(V)2/B - JDAM, 1000lb GPS Guided Bomb",
        "weight": 501.47,
    }
    STA_03_SUU79_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_MK_1X_GBU-38}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x GBU-38 - JDAM, 500lb GPS Guided Bomb",
        "weight": 275.47,
    }
    STA_03_SUU79_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_1X_GBU-38}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x GBU-38 - JDAM, 500lb GPS Guided Bomb",
        "weight": 275.47,
    }
    STA_03_SUU79_BRU32_1x_GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_1X_GBU_54V}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x GBU-54(V)1/B - LJDAM, 500lb Laser & GPS Guided Bomb LD",
        "weight": 287.47,
    }
    STA_03_SUU79_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_MK_1X_ROCKEYE}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x Mk-20 Rockeye - 490lbs CBU, 247 x HEAT Bomblets",
        "weight": 256.47,
    }
    STA_03_SUU79_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_1X_ROCKEYE}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x Mk-20 Rockeye - 490lbs CBU, 247 x HEAT Bomblets",
        "weight": 256.47,
    }
    STA_03_SUU79_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_MK_1X_MK-82Y}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x Mk-82Y - 500lb GP Chute Retarded HD",
        "weight": 266.47,
    }
    STA_03_SUU79_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_1X_MK-82Y}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x Mk-82Y - 500lb GP Chute Retarded HD",
        "weight": 266.47,
    }
    STA_03_SUU79_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_MK_1X_MK-82_Snakeye}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x Mk-82 Snakeye - 500lb GP Bomb HD",
        "weight": 283.97,
    }
    STA_03_SUU79_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_1X_MK-82_Snakeye}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x Mk-82 Snakeye - 500lb GP Bomb HD",
        "weight": 283.97,
    }
    STA_03_SUU79_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_MK_1X_MK-82}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x Mk-82 - 500lb GP Bomb LD",
        "weight": 262.47,
    }
    STA_03_SUU79_BRU32_1x_Mk_82___500lb_GP_Bomb_LD_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_1X_MK-82}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x Mk-82 - 500lb GP Bomb LD",
        "weight": 262.47,
    }
    STA_03_SUU79_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_MK_1X_MK-83}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x Mk-83 - 1000lb GP Bomb LD",
        "weight": 488.47,
    }
    STA_03_SUU79_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_1X_MK-83}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x Mk-83 - 1000lb GP Bomb LD",
        "weight": 488.47,
    }
    STA_03_SUU79_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_MK_1X_MK-84}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x Mk-84 - 2000lb GP Bomb LD",
        "weight": 946.47,
    }
    STA_03_SUU79_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_1X_MK-84}",
        "name": " [ STA 03	  | SUU79 | BRU32   ] - 1x Mk-84 - 2000lb GP Bomb LD",
        "weight": 946.47,
    }
    STA_03_SUU79_BRU33_2x_BDU_45B___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_BR2_BDU-45B}",
        "name": " [ STA 03	  | SUU79 | BRU33   ] - 2x BDU-45B - 500lb Practice Bomb",
        "weight": 589.1885,
    }
    STA_03_SUU79_BRU33_2x_BDU_45___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_BR2_BDU-45}",
        "name": " [ STA 03	  | SUU79 | BRU33   ] - 2x BDU-45 - 500lb Practice Bomb",
        "weight": 589.1885,
    }
    STA_03_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_MK_BR2_GBU-12}",
        "name": " [ STA 03	  | SUU79 | BRU33   ] - 2x GBU-12 - 500lb Laser Guided Bomb",
        "weight": 679.1885,
    }
    STA_03_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_BR2_GBU-12}",
        "name": " [ STA 03	  | SUU79 | BRU33   ] - 2x GBU-12 - 500lb Laser Guided Bomb",
        "weight": 679.1885,
    }
    STA_03_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_BR2_MK-82Y}",
        "name": " [ STA 03	  | SUU79 | BRU33   ] - 2x Mk-82Y - 500lb GP Chute Retarded HD",
        "weight": 589.1885,
    }
    STA_03_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_MK_BR2_MK-82_Snakeye}",
        "name": " [ STA 03	  | SUU79 | BRU33   ] - 2x Mk-82 Snakeye - 500lb GP Bomb HD",
        "weight": 624.1885,
    }
    STA_03_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_BR2_MK-82_Snakeye}",
        "name": " [ STA 03	  | SUU79 | BRU33   ] - 2x Mk-82 Snakeye - 500lb GP Bomb HD",
        "weight": 624.1885,
    }
    STA_03_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_MK_BR2_MK-82}",
        "name": " [ STA 03	  | SUU79 | BRU33   ] - 2x Mk-82 - 500lb GP Bomb LD",
        "weight": 581.1885,
    }
    STA_03_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_BR2_MK-82}",
        "name": " [ STA 03	  | SUU79 | BRU33   ] - 2x Mk-82 - 500lb GP Bomb LD",
        "weight": 581.1885,
    }
    STA_03_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_MK_BR2_MK-83}",
        "name": " [ STA 03	  | SUU79 | BRU33   ] - 2x Mk-83 - 1000lb GP Bomb LD",
        "weight": 1033.1885,
    }
    STA_03_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_BR2_MK-83}",
        "name": " [ STA 03	  | SUU79 | BRU33   ] - 2x Mk-83 - 1000lb GP Bomb LD",
        "weight": 1033.1885,
    }
    STA_03_SUU79_BRU41_6x_BDU_33___25lb_Practice_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_BD_BRU41_6X_BDU-33}",
        "name": " [ STA 03	  | SUU79 | BRU41   ] - 6x BDU-33 - 25lb Practice Bomb LD",
        "weight": 195.713,
    }
    STA_03_SUU79_BRU42_1x_ADM_141A_TALD = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_TD_1X_BRU_ADM-141A}",
        "name": " [ STA 03	  | SUU79 | BRU42   ] - 1x ADM-141A TALD",
        "weight": 265.27,
    }
    STA_03_SUU79_BRU42_1x_ADM_141A_TALD_ = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_TD_1X_BRU_ADM-141A}",
        "name": " [ STA 03	  | SUU79 | BRU42   ] - 1x ADM-141A TALD",
        "weight": 265.27,
    }
    STA_03_SUU79_BRU42_1x_ADM_141A_TALD__ = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_TD_1X_BRU_ADM-141A}",
        "name": " [ STA 03	  | SUU79 | BRU42   ] - 1x ADM-141A TALD",
        "weight": 265.27,
    }
    STA_03_SUU79_BRU42_2x_ADM_141A_TALD = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_TD_2X_BRU_ADM-141A}",
        "name": " [ STA 03	  | SUU79 | BRU42   ] - 2x ADM-141A TALD",
        "weight": 445.27,
    }
    STA_03_SUU79_BRU42_2x_ADM_141A_TALD_ = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_TD_2X_BRU_ADM-141A}",
        "name": " [ STA 03	  | SUU79 | BRU42   ] - 2x ADM-141A TALD",
        "weight": 445.27,
    }
    STA_03_SUU79_BRU42_2x_ADM_141A_TALD__ = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_TD_2X_BRU_ADM-141A}",
        "name": " [ STA 03	  | SUU79 | BRU42   ] - 2x ADM-141A TALD",
        "weight": 445.27,
    }
    STA_03_SUU79_BRU42_3x_ADM_141A_TALD = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_TD_3X_BRU_ADM-141A}",
        "name": " [ STA 03	  | SUU79 | BRU42   ] - 3x ADM-141A TALD",
        "weight": 625.27,
    }
    STA_03_SUU79_BRU42_3x_ADM_141A_TALD_ = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_TD_3X_BRU_ADM-141A}",
        "name": " [ STA 03	  | SUU79 | BRU42   ] - 3x ADM-141A TALD",
        "weight": 625.27,
    }
    STA_03_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_JS_1X_BRU_AGM-154A}",
        "name": " [ STA 03	  | SUU79 | BRU55   ] - 1x AGM-154A - JSOW CEB (CBU-type)",
        "weight": 606.97,
    }
    STA_03_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_JS_1X_BRU_AGM-154C}",
        "name": " [ STA 03	  | SUU79 | BRU55   ] - 1x AGM-154C - JSOW Unitary BROACH",
        "weight": 605.97,
    }
    STA_03_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_JS_1X_BRU_AGM-154C}",
        "name": " [ STA 03	  | SUU79 | BRU55   ] - 1x AGM-154C - JSOW Unitary BROACH",
        "weight": 605.97,
    }
    STA_03_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_JS_2X_BRU_AGM-154A}",
        "name": " [ STA 03	  | SUU79 | BRU55   ] - 2x AGM-154A - JSOW CEB (CBU-type)",
        "weight": 1091.97,
    }
    STA_03_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_JS_2X_BRU_AGM-154C}",
        "name": " [ STA 03	  | SUU79 | BRU55   ] - 2x AGM-154C - JSOW Unitary BROACH",
        "weight": 1089.97,
    }
    STA_03_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_JS_2X_BRU_AGM-154C}",
        "name": " [ STA 03	  | SUU79 | BRU55   ] - 2x AGM-154C - JSOW Unitary BROACH",
        "weight": 1089.97,
    }
    STA_03_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_MK_BR55_2X_GBU-32}",
        "name": " [ STA 03	  | SUU79 | BRU55   ] - 2x GBU-32(V)2/B - JDAM, 1000lb GPS Guided Bomb",
        "weight": 1055.97,
    }
    STA_03_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_MK_BR55_2X_GBU-38}",
        "name": " [ STA 03	  | SUU79 | BRU55   ] - 2x GBU-38 - JDAM, 500lb GPS Guided Bomb",
        "weight": 603.97,
    }
    STA_03_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MK_BR55_2X_GBU-38}",
        "name": " [ STA 03	  | SUU79 | BRU55   ] - 2x GBU-38 - JDAM, 500lb GPS Guided Bomb",
        "weight": 603.97,
    }
    STA_03_SUU79_EMPTY = {
        "clsid": "{SUPERHORNET_PYLON_03_EMPTY}",
        "name": " [ STA 03	  | SUU79 | EMPTY ]",
        "weight": 0,
    }
    STA_03_SUU79_LA118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = {
        "clsid": "{GROWLER_PYLON_02_MB_AR_1X_AGM-88}",
        "name": " [ STA 03	  | SUU79 | LA118 ] - 1x AGM-88C HARM - High Speed Anti-Radiation Missile",
        "weight": 440.87,
    }
    STA_03_SUU79_LA127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = {
        "clsid": "{GROWLER_PYLON_02_MB_AM_1X_AIM-120}",
        "name": " [ STA 03	  | SUU79 | LA127 ] - 1x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 337.32,
    }
    STA_03_SUU79_LA127_1x_AIM_120B_AMRAAM___Active_Radar_AAM_ = {
        "clsid": "{GROWLER_PYLON_03_MB_AM_1X_AIM-120}",
        "name": " [ STA 03	  | SUU79 | LA127 ] - 1x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 337.32,
    }
    STA_03_SUU79_LA127_1x_AIM_120B_AMRAAM___Active_Radar_AAM__ = {
        "clsid": "{GROWLER_PYLON_03_MB_AM_1X_AIM-9}",
        "name": " [ STA 03	  | SUU79 | LA127 ] - 1x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 337.32,
    }
    STA_03_SUU79_LA127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = {
        "clsid": "{GROWLER_PYLON_02_MB_AM_1X_AIM-120C}",
        "name": " [ STA 03	  | SUU79 | LA127 ] - 1x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 340.95,
    }
    STA_03_SUU79_LA127_1x_AIM_120C_AMRAAM___Active_Radar_AAM_ = {
        "clsid": "{GROWLER_PYLON_03_MB_AM_1X_AIM-120C}",
        "name": " [ STA 03	  | SUU79 | LA127 ] - 1x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 340.95,
    }
    STA_03_SUU79_LA127_1x_AIM_120C_AMRAAM___Active_Radar_AAM__ = {
        "clsid": "{GROWLER_PYLON_03_MB_AM_1X_AIM-9X}",
        "name": " [ STA 03	  | SUU79 | LA127 ] - 1x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 340.95,
    }
    STA_03_SUU79_LA127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = {
        "clsid": "{GROWLER_PYLON_02_MB_AM_1X_AIM-120D}",
        "name": " [ STA 03	  | SUU79 | LA127 ] - 1x AIM-120D AMRAAM - Active Radar AAM (AI Only)",
        "weight": 341.87,
    }
    STA_03_SUU79_LA127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only__ = {
        "clsid": "{GROWLER_PYLON_03_MB_AM_1X_AIM-120D}",
        "name": " [ STA 03	  | SUU79 | LA127 ] - 1x AIM-120D AMRAAM - Active Radar AAM (AI Only)",
        "weight": 341.87,
    }
    STA_03_SUU79_LA127_1x_AIM_9M_Sidewinder_IR_AAM = {
        "clsid": "{GROWLER_PYLON_02_MB_SW_1X_AIM-9}",
        "name": " [ STA 03	  | SUU79 | LA127 ] - 1x AIM-9M Sidewinder IR AAM",
        "weight": 265.19,
    }
    STA_03_SUU79_LA127_1x_AIM_9X_Sidewinder_IR_AAM = {
        "clsid": "{GROWLER_PYLON_02_MB_SW_1X_AIM-9X}",
        "name": " [ STA 03	  | SUU79 | LA127 ] - 1x AIM-9X Sidewinder IR AAM",
        "weight": 263.93,
    }
    STA_03_SUU79_LA127_1x_Captive_AIM_9M_for_ACM = {
        "clsid": "{GROWLER_PYLON_02_MB_SW_1X_CATM-9M}",
        "name": " [ STA 03	  | SUU79 | LA127 ] - 1x Captive AIM-9M for ACM",
        "weight": 265.2,
    }
    STA_03_SUU79_LA127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X = {
        "clsid": "{GROWLER_PYLON_03_MB_LAU127}",
        "name": " [ STA 03	  | SUU79 | LA127 ] - 1x Marvin LAU-127 Rail Launcher for AIM-120B/C/D and AIM9L/M/X",
        "weight": 52.1,
    }
    STA_03_SUU79_LA127_2x_AIM_120B_AMRAAM___Active_Radar_AAM = {
        "clsid": "{GROWLER_PYLON_02_MB_AM_2X_AIM-120}",
        "name": " [ STA 03	  | SUU79 | LA127 ] - 2x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 495.17,
    }
    STA_03_SUU79_LA127_2x_AIM_120B_AMRAAM___Active_Radar_AAM_ = {
        "clsid": "{GROWLER_PYLON_03_MB_AM_2X_AIM-120}",
        "name": " [ STA 03	  | SUU79 | LA127 ] - 2x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 495.17,
    }
    STA_03_SUU79_LA127_2x_AIM_120B_AMRAAM___Active_Radar_AAM__ = {
        "clsid": "{GROWLER_PYLON_03_MB_AM_2X_AIM-9}",
        "name": " [ STA 03	  | SUU79 | LA127 ] - 2x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 495.17,
    }
    STA_03_SUU79_LA127_2x_AIM_120C_AMRAAM___Active_Radar_AAM = {
        "clsid": "{GROWLER_PYLON_02_MB_AM_2X_AIM-120C}",
        "name": " [ STA 03	  | SUU79 | LA127 ] - 2x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 502.43,
    }
    STA_03_SUU79_LA127_2x_AIM_120C_AMRAAM___Active_Radar_AAM_ = {
        "clsid": "{GROWLER_PYLON_03_MB_AM_2X_AIM-120C}",
        "name": " [ STA 03	  | SUU79 | LA127 ] - 2x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 502.43,
    }
    STA_03_SUU79_LA127_2x_AIM_120C_AMRAAM___Active_Radar_AAM__ = {
        "clsid": "{GROWLER_PYLON_03_MB_AM_2X_AIM-9X}",
        "name": " [ STA 03	  | SUU79 | LA127 ] - 2x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 502.43,
    }
    STA_03_SUU79_LA127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = {
        "clsid": "{GROWLER_PYLON_02_MB_AM_2X_AIM-120D}",
        "name": " [ STA 03	  | SUU79 | LA127 ] - 2x AIM-120D AMRAAM - Active Radar AAM (AI Only)",
        "weight": 504.27,
    }
    STA_03_SUU79_LA127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only__ = {
        "clsid": "{GROWLER_PYLON_03_MB_AM_2X_AIM-120D}",
        "name": " [ STA 03	  | SUU79 | LA127 ] - 2x AIM-120D AMRAAM - Active Radar AAM (AI Only)",
        "weight": 504.27,
    }
    STA_03_SUU79_LA127_2x_AIM_9M_Sidewinder_IR_AAM = {
        "clsid": "{GROWLER_PYLON_02_MB_SW_2X_AIM-9}",
        "name": " [ STA 03	  | SUU79 | LA127 ] - 2x AIM-9M Sidewinder IR AAM",
        "weight": 350.91,
    }
    STA_03_SUU79_LA127_2x_AIM_9X_Sidewinder_IR_AAM = {
        "clsid": "{GROWLER_PYLON_02_MB_SW_2X_AIM-9X}",
        "name": " [ STA 03	  | SUU79 | LA127 ] - 2x AIM-9X Sidewinder IR AAM",
        "weight": 348.39,
    }
    STA_03_SUU79_LA127_2x_Captive_AIM_9M_for_ACM = {
        "clsid": "{GROWLER_PYLON_02_MB_SW_2X_CATM-9M}",
        "name": " [ STA 03	  | SUU79 | LA127 ] - 2x Captive AIM-9M for ACM",
        "weight": 350.93,
    }
    STA_03_SUU79_LAU115_1x_AIM_7F_Sparrow_Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_SP_1X_AIM-7F}",
        "name": " [ STA 03	  | SUU79 | LAU115 ] - 1x AIM-7F Sparrow Semi-Active Radar",
        "weight": 319.9,
    }
    STA_03_SUU79_LAU115_1x_AIM_7F_Sparrow_Semi_Active_Radar_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_SP_1X_AIM-7F}",
        "name": " [ STA 03	  | SUU79 | LAU115 ] - 1x AIM-7F Sparrow Semi-Active Radar",
        "weight": 319.9,
    }
    STA_03_SUU79_LAU115_1x_AIM_7MH_Sparrow_Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_SP_1X_AIM-7H}",
        "name": " [ STA 03	  | SUU79 | LAU115 ] - 1x AIM-7MH Sparrow Semi-Active Radar",
        "weight": 319.9,
    }
    STA_03_SUU79_LAU115_1x_AIM_7MH_Sparrow_Semi_Active_Radar_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_SP_1X_AIM-7H}",
        "name": " [ STA 03	  | SUU79 | LAU115 ] - 1x AIM-7MH Sparrow Semi-Active Radar",
        "weight": 319.9,
    }
    STA_03_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_SP_1X_AIM-7M}",
        "name": " [ STA 03	  | SUU79 | LAU115 ] - 1x AIM-7M Sparrow Semi-Active Radar",
        "weight": 319.9,
    }
    STA_03_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_SP_1X_AIM-7M}",
        "name": " [ STA 03	  | SUU79 | LAU115 ] - 1x AIM-7M Sparrow Semi-Active Radar",
        "weight": 319.9,
    }
    STA_03_SUU79_LAU115_1x_AIM_7P_Sparrow_Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_SP_1X_AIM-7P}",
        "name": " [ STA 03	  | SUU79 | LAU115 ] - 1x AIM-7P Sparrow Semi-Active Radar",
        "weight": 319.9,
    }
    STA_03_SUU79_LAU115_1x_AIM_7P_Sparrow_Semi_Active_Radar_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_SP_1X_AIM-7P}",
        "name": " [ STA 03	  | SUU79 | LAU115 ] - 1x AIM-7P Sparrow Semi-Active Radar",
        "weight": 319.9,
    }
    STA_03_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_MV_1X_AGM-65E}",
        "name": " [ STA 03	  | SUU79 | LAU117 ] - 1x AGM-65E - Maverick E (Laser ASM - Lg Whd)",
        "weight": 379.47,
    }
    STA_03_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd__ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MV_1X_AGM-65E}",
        "name": " [ STA 03	  | SUU79 | LAU117 ] - 1x AGM-65E - Maverick E (Laser ASM - Lg Whd)",
        "weight": 379.47,
    }
    STA_03_SUU79_LAU117_1x_AGM_65F___Maverick_F__IIR_ = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_MV_1X_AGM-65F}",
        "name": " [ STA 03	  | SUU79 | LAU117 ] - 1x AGM-65F - Maverick F (IIR)",
        "weight": 394.47,
    }
    STA_03_SUU79_LAU117_1x_AGM_65F___Maverick_F__IIR__ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MV_1X_AGM-65F}",
        "name": " [ STA 03	  | SUU79 | LAU117 ] - 1x AGM-65F - Maverick F (IIR)",
        "weight": 394.47,
    }
    STA_03_SUU79_LAU117_1x_AGM_84D_Harpoon_Anti_Ship_Missile = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_SM_1X_AGM-84D}",
        "name": " [ STA 03	  | SUU79 | LAU117 ] - 1x AGM-84D Harpoon Anti-Ship Missile",
        "weight": 574.47,
    }
    STA_03_SUU79_LAU117_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_SM_1X_AGM-84E}",
        "name": " [ STA 03	  | SUU79 | LAU117 ] - 1x AGM-84E Harpoon/SLAM (Stand-Off Land-Attack Missile)",
        "weight": 662.47,
    }
    STA_03_SUU79_LAU117_1x_AGM_84H_SLAM_ER__Expanded_Response_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_SM_1X_AGM-84H}",
        "name": " [ STA 03	  | SUU79 | LAU117 ] - 1x AGM-84H SLAM-ER (Expanded Response)",
        "weight": 709.47,
    }
    STA_03_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_MV_1X_CATM-65K}",
        "name": " [ STA 03	  | SUU79 | LAU117 ] - 1x CATM-65K - Captive Trg Round for Mav K (CCD), AI Only",
        "weight": 390.47,
    }
    STA_03_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_MV_1X_CATM-65K}",
        "name": " [ STA 03	  | SUU79 | LAU117 ] - 1x CATM-65K - Captive Trg Round for Mav K (CCD), AI Only",
        "weight": 390.47,
    }
    STA_03_SUU79_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_AR_1X_AGM-88}",
        "name": " [ STA 03	  | SUU79 | LAU118 ] - 1x AGM-88C HARM - High Speed Anti-Radiation Missile",
        "weight": 440.87,
    }
    STA_03_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_AM_1X_AIM-120}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 1x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 337.35,
    }
    STA_03_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_AM_1X_AIM-120}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 1x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 337.35,
    }
    STA_03_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_AM_1X_AIM-120C}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 1x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 340.98,
    }
    STA_03_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_AM_1X_AIM-120C}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 1x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 340.98,
    }
    STA_03_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_AM_1X_AIM-120D}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 1x AIM-120D AMRAAM - Active Radar AAM (AI Only)",
        "weight": 341.9,
    }
    STA_03_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only__ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_AM_1X_AIM-120D}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 1x AIM-120D AMRAAM - Active Radar AAM (AI Only)",
        "weight": 341.9,
    }
    STA_03_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_SW_1X_AIM-9}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 1x AIM-9M Sidewinder IR AAM",
        "weight": 265.22,
    }
    STA_03_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_SW_1X_AIM-9}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 1x AIM-9M Sidewinder IR AAM",
        "weight": 265.22,
    }
    STA_03_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_SW_1X_AIM-9X}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 1x AIM-9X Sidewinder IR AAM",
        "weight": 263.96,
    }
    STA_03_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_SW_1X_AIM-9X}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 1x AIM-9X Sidewinder IR AAM",
        "weight": 263.96,
    }
    STA_03_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_SW_1X_CATM-9M}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 1x Captive AIM-9M for ACM",
        "weight": 265.23,
    }
    STA_03_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_SW_1X_CATM-9M}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 1x Captive AIM-9M for ACM",
        "weight": 265.23,
    }
    STA_03_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_AM_2X_AIM-120}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 2x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 495.2,
    }
    STA_03_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_AM_2X_AIM-120}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 2x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 495.2,
    }
    STA_03_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_AM_2X_AIM-120C}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 2x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 502.46,
    }
    STA_03_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_AM_2X_AIM-120C}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 2x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 502.46,
    }
    STA_03_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_AM_2X_AIM-120D}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 2x AIM-120D AMRAAM - Active Radar AAM (AI Only)",
        "weight": 504.3,
    }
    STA_03_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only__ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_AM_2X_AIM-120D}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 2x AIM-120D AMRAAM - Active Radar AAM (AI Only)",
        "weight": 504.3,
    }
    STA_03_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_SW_2X_AIM-9}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 2x AIM-9M Sidewinder IR AAM",
        "weight": 350.94,
    }
    STA_03_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_SW_2X_AIM-9}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 2x AIM-9M Sidewinder IR AAM",
        "weight": 350.94,
    }
    STA_03_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_SW_2X_AIM-9X}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 2x AIM-9X Sidewinder IR AAM",
        "weight": 348.42,
    }
    STA_03_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_SW_2X_AIM-9X}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 2x AIM-9X Sidewinder IR AAM",
        "weight": 348.42,
    }
    STA_03_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM = {
        "clsid": "{SUPERHORNET_PYLON_02_MB_SW_2X_CATM-9M}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 2x Captive AIM-9M for ACM",
        "weight": 350.96,
    }
    STA_03_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM_ = {
        "clsid": "{SUPERHORNET_PYLON_03_MB_SW_2X_CATM-9M}",
        "name": " [ STA 03	  | SUU79 | LAU127 ] - 2x Captive AIM-9M for ACM",
        "weight": 350.96,
    }
    STA_03_02_79_80_BRU32_2x_GBU_10___2000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MB_MK_2X_GBU-10}",
        "name": " [ STA 03/02 | 79/80 | BRU32   ] - 2x GBU-10 - 2000lb Laser Guided Bomb",
        "weight": 1892.94,
    }
    STA_03_02_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MB_MK_2X_GBU-12}",
        "name": " [ STA 03/02 | 79/80 | BRU32   ] - 2x GBU-12 - 500lb Laser Guided Bomb",
        "weight": 622.94,
    }
    STA_03_02_79_80_BRU32_2x_GBU_16___1000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MB_MK_2X_GBU-16}",
        "name": " [ STA 03/02 | 79/80 | BRU32   ] - 2x GBU-16 - 1000lb Laser Guided Bomb",
        "weight": 1094.94,
    }
    STA_03_02_79_80_BRU32_2x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MB_MK_2X_GBU-24}",
        "name": " [ STA 03/02 | 79/80 | BRU32   ] - 2x GBU-24A/B Paveway III - 2000lb Laser Guided Bomb",
        "weight": 1936.94,
    }
    STA_03_02_79_80_BRU32_2x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MB_MK_2X_GBU-31}",
        "name": " [ STA 03/02 | 79/80 | BRU32   ] - 2x GBU-31(V)1/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 1936.94,
    }
    STA_03_02_79_80_BRU32_2x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MB_MK_2X_GBU-31V}",
        "name": " [ STA 03/02 | 79/80 | BRU32   ] - 2x GBU-31(V)3/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 2030.94,
    }
    STA_03_02_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MB_MK_2X_GBU-38}",
        "name": " [ STA 03/02 | 79/80 | BRU32   ] - 2x GBU-38 - JDAM, 500lb GPS Guided Bomb",
        "weight": 550.94,
    }
    STA_03_02_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MB_MK_2X_ROCKEYE}",
        "name": " [ STA 03/02 | 79/80 | BRU32   ] - 2x Mk-20 Rockeye - 490lbs CBU, 247 x HEAT Bomblets",
        "weight": 512.94,
    }
    STA_03_02_79_80_BRU32_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MB_MK_2X_MK-82Y}",
        "name": " [ STA 03/02 | 79/80 | BRU32   ] - 2x Mk-82Y - 500lb GP Chute Retarded HD",
        "weight": 532.94,
    }
    STA_03_02_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MB_MK_2X_MK-82_Snakeye}",
        "name": " [ STA 03/02 | 79/80 | BRU32   ] - 2x Mk-82 Snakeye - 500lb GP Bomb HD",
        "weight": 567.94,
    }
    STA_03_02_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MB_MK_2X_MK-82}",
        "name": " [ STA 03/02 | 79/80 | BRU32   ] - 2x Mk-82 - 500lb GP Bomb LD",
        "weight": 524.94,
    }
    STA_03_02_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MB_MK_2X_MK-83}",
        "name": " [ STA 03/02 | 79/80 | BRU32   ] - 2x Mk-83 - 1000lb GP Bomb LD",
        "weight": 976.94,
    }
    STA_03_02_79_80_BRU32_2x_Mk_84___2000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_MB_MK_2X_MK-84}",
        "name": " [ STA 03/02 | 79/80 | BRU32   ] - 2x Mk-84 - 2000lb GP Bomb LD",
        "weight": 1892.94,
    }
    STA_04_SUU79_BRU32_1x_AGM_154A___JSOW_CEB__CBU_type_ = {
        "clsid": "{GROWLER_PYLON_04_IB_JS_1X_AGM-154A}",
        "name": " [ STA 04	  | SUU79 | BRU32 ] - 1x AGM-154A - JSOW CEB (CBU-type)",
        "weight": 519.47,
    }
    STA_04_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH = {
        "clsid": "{GROWLER_PYLON_04_IB_JS_1X_AGM-154C}",
        "name": " [ STA 04	  | SUU79 | BRU32 ] - 1x AGM-154C - JSOW Unitary BROACH",
        "weight": 518.47,
    }
    STA_04_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank = {
        "clsid": "{GROWLER_PYLON_04_IB_FT_FPU-12_Fueltank}",
        "name": " [ STA 04	  | SUU79 | BRU32 ] - 1x FPU-12/A Fuel Tank",
        "weight": 1384.47,
    }
    STA_04_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank_ = {
        "clsid": "{GROWLER_PYLON_08_IB_FT_FPU-12_Fueltank}",
        "name": " [ STA 04	  | SUU79 | BRU32 ] - 1x FPU-12/A Fuel Tank",
        "weight": 1384.47,
    }
    STA_04_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis = {
        "clsid": "{GROWLER_PYLON_04_IB_FT_FPU-12_FueltankHighVis}",
        "name": " [ STA 04	  | SUU79 | BRU32 ] - 1x FPU-12/A Fuel Tank - High Vis",
        "weight": 1384.47,
    }
    STA_04_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis_ = {
        "clsid": "{GROWLER_PYLON_08_IB_FT_FPU-12_FueltankHighVis}",
        "name": " [ STA 04	  | SUU79 | BRU32 ] - 1x FPU-12/A Fuel Tank - High Vis",
        "weight": 1384.47,
    }
    STA_04_SUU79_BRU32_Remove_SUU_79A_A_Pylon = {
        "clsid": "{SUPERHORNET_PYLON_04_REMOVE_SUU79}",
        "name": " [ STA 04	  | SUU79 | BRU32   ] Remove SUU-79A/A Pylon",
        "weight": 0,
    }
    STA_04_SUU79_BRU32_1x_AGM_154A___JSOW_CEB__CBU_type_ = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_JS_1X_AGM-154A}",
        "name": " [ STA 04	  | SUU79 | BRU32   ] - 1x AGM-154A - JSOW CEB (CBU-type)",
        "weight": 519.47,
    }
    STA_04_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_JS_1X_AGM-154C}",
        "name": " [ STA 04	  | SUU79 | BRU32   ] - 1x AGM-154C - JSOW Unitary BROACH",
        "weight": 518.47,
    }
    STA_04_SUU79_BRU32_1x_AGM_84D_Harpoon_Anti_Ship_Missile = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_SM_1X_AGM-84D}",
        "name": " [ STA 04	  | SUU79 | BRU32   ] - 1x AGM-84D Harpoon Anti-Ship Missile",
        "weight": 574.47,
    }
    STA_04_SUU79_BRU32_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_SM_1X_AGM-84E}",
        "name": " [ STA 04	  | SUU79 | BRU32   ] - 1x AGM-84E Harpoon/SLAM (Stand-Off Land-Attack Missile)",
        "weight": 662.47,
    }
    STA_04_SUU79_BRU32_1x_AGM_84H_SLAM_ER__Expanded_Response_ = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_SM_1X_AGM-84H}",
        "name": " [ STA 04	  | SUU79 | BRU32   ] - 1x AGM-84H SLAM-ER (Expanded Response)",
        "weight": 709.47,
    }
    STA_04_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_PD_1X_AWW-13}",
        "name": " [ STA 04	  | SUU79 | BRU32   ] - 1x AN/AWW-13 Advanced Datalink Pod",
        "weight": 234.47,
    }
    STA_04_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_FT_FPU-12_Fueltank}",
        "name": " [ STA 04	  | SUU79 | BRU32   ] - 1x FPU-12/A Fuel Tank",
        "weight": 1384.47,
    }
    STA_04_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank_ = {
        "clsid": "{SUPERHORNET_PYLON_04_IB_FT_FPU-12_Fueltank}",
        "name": " [ STA 04	  | SUU79 | BRU32   ] - 1x FPU-12/A Fuel Tank",
        "weight": 1384.47,
    }
    STA_04_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_FT_FPU-12_FueltankHighVis}",
        "name": " [ STA 04	  | SUU79 | BRU32   ] - 1x FPU-12/A Fuel Tank - High Vis",
        "weight": 1384.47,
    }
    STA_04_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis_ = {
        "clsid": "{SUPERHORNET_PYLON_04_IB_FT_FPU-12_FueltankHighVis}",
        "name": " [ STA 04	  | SUU79 | BRU32   ] - 1x FPU-12/A Fuel Tank - High Vis",
        "weight": 1384.47,
    }
    STA_04_SUU79_BRU33_2x_BDU_45B___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_BR2_BDU-45B}",
        "name": " [ STA 04	  | SUU79 | BRU33   ] - 2x BDU-45B - 500lb Practice Bomb",
        "weight": 589.1885,
    }
    STA_04_SUU79_BRU33_2x_BDU_45___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_BR2_BDU-45}",
        "name": " [ STA 04	  | SUU79 | BRU33   ] - 2x BDU-45 - 500lb Practice Bomb",
        "weight": 589.1885,
    }
    STA_04_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_BR2_GBU-12}",
        "name": " [ STA 04	  | SUU79 | BRU33   ] - 2x GBU-12 - 500lb Laser Guided Bomb",
        "weight": 679.1885,
    }
    STA_04_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_BR2_MK-82Y}",
        "name": " [ STA 04	  | SUU79 | BRU33   ] - 2x Mk-82Y - 500lb GP Chute Retarded HD",
        "weight": 589.1885,
    }
    STA_04_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_BR2_MK-82_Snakeye}",
        "name": " [ STA 04	  | SUU79 | BRU33   ] - 2x Mk-82 Snakeye - 500lb GP Bomb HD",
        "weight": 624.1885,
    }
    STA_04_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_BR2_MK-82}",
        "name": " [ STA 04	  | SUU79 | BRU33   ] - 2x Mk-82 - 500lb GP Bomb LD",
        "weight": 581.1885,
    }
    STA_04_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_BR2_MK-83}",
        "name": " [ STA 04	  | SUU79 | BRU33   ] - 2x Mk-83 - 1000lb GP Bomb LD",
        "weight": 1033.1885,
    }
    STA_04_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type_ = {
        "clsid": "{GROWLER_PYLON_04_IB_JS_1X_BRU_AGM-154A}",
        "name": " [ STA 04	  | SUU79 | BRU55 ] - 1x AGM-154A - JSOW CEB (CBU-type)",
        "weight": 606.97,
    }
    STA_04_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH = {
        "clsid": "{GROWLER_PYLON_04_IB_JS_1X_BRU_AGM-154C}",
        "name": " [ STA 04	  | SUU79 | BRU55 ] - 1x AGM-154C - JSOW Unitary BROACH",
        "weight": 605.97,
    }
    STA_04_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type_ = {
        "clsid": "{GROWLER_PYLON_04_IB_JS_2X_BRU_AGM-154A}",
        "name": " [ STA 04	  | SUU79 | BRU55 ] - 2x AGM-154A - JSOW CEB (CBU-type)",
        "weight": 1091.97,
    }
    STA_04_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH = {
        "clsid": "{GROWLER_PYLON_04_IB_JS_2X_BRU_AGM-154C}",
        "name": " [ STA 04	  | SUU79 | BRU55 ] - 2x AGM-154C - JSOW Unitary BROACH",
        "weight": 1089.97,
    }
    STA_04_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type_ = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_JS_1X_BRU_AGM-154A}",
        "name": " [ STA 04	  | SUU79 | BRU55   ] - 1x AGM-154A - JSOW CEB (CBU-type)",
        "weight": 606.97,
    }
    STA_04_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_JS_1X_BRU_AGM-154C}",
        "name": " [ STA 04	  | SUU79 | BRU55   ] - 1x AGM-154C - JSOW Unitary BROACH",
        "weight": 605.97,
    }
    STA_04_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type_ = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_JS_2X_BRU_AGM-154A}",
        "name": " [ STA 04	  | SUU79 | BRU55   ] - 2x AGM-154A - JSOW CEB (CBU-type)",
        "weight": 1091.97,
    }
    STA_04_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_JS_2X_BRU_AGM-154C}",
        "name": " [ STA 04	  | SUU79 | BRU55   ] - 2x AGM-154C - JSOW Unitary BROACH",
        "weight": 1089.97,
    }
    STA_04_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_BR55_2X_GBU-32}",
        "name": " [ STA 04	  | SUU79 | BRU55   ] - 2x GBU-32(V)2/B - JDAM, 1000lb GPS Guided Bomb",
        "weight": 1055.97,
    }
    STA_04_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_BR55_2X_GBU-38}",
        "name": " [ STA 04	  | SUU79 | BRU55   ] - 2x GBU-38 - JDAM, 500lb GPS Guided Bomb",
        "weight": 603.97,
    }
    STA_04_SUU79_EMPTY = {
        "clsid": "{SUPERHORNET_PYLON_04_EMPTY}",
        "name": " [ STA 04	  | SUU79 | EMPTY ]",
        "weight": 0,
    }
    STA_04_SUU79_LA127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = {
        "clsid": "{GROWLER_PYLON_04_IB_AM_1X_AIM-120}",
        "name": " [ STA 04	  | SUU79 | LA127 ] - 1x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 337.32,
    }
    STA_04_SUU79_LA127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = {
        "clsid": "{GROWLER_PYLON_04_IB_AM_1X_AIM-120C}",
        "name": " [ STA 04	  | SUU79 | LA127 ] - 1x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 340.95,
    }
    STA_04_SUU79_LA127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = {
        "clsid": "{GROWLER_PYLON_04_IB_AM_1X_AIM-120D}",
        "name": " [ STA 04	  | SUU79 | LA127 ] - 1x AIM-120D AMRAAM - Active Radar AAM (AI Only)",
        "weight": 341.87,
    }
    STA_04_SUU79_LA127_1x_AIM_9M_Sidewinder_IR_AAM = {
        "clsid": "{GROWLER_PYLON_04_IB_SW_1X_AIM-9}",
        "name": " [ STA 04	  | SUU79 | LA127 ] - 1x AIM-9M Sidewinder IR AAM",
        "weight": 265.19,
    }
    STA_04_SUU79_LA127_1x_AIM_9X_Sidewinder_IR_AAM = {
        "clsid": "{GROWLER_PYLON_04_IB_SW_1X_AIM-9X}",
        "name": " [ STA 04	  | SUU79 | LA127 ] - 1x AIM-9X Sidewinder IR AAM",
        "weight": 263.93,
    }
    STA_04_SUU79_LA127_1x_Captive_AIM_9M_for_ACM = {
        "clsid": "{GROWLER_PYLON_04_IB_SW_1X_CATM-9M}",
        "name": " [ STA 04	  | SUU79 | LA127 ] - 1x Captive AIM-9M for ACM",
        "weight": 265.2,
    }
    STA_04_SUU79_LA127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X = {
        "clsid": "{GROWLER_PYLON_04_IB_LAU127}",
        "name": " [ STA 04	  | SUU79 | LA127 ] - 1x Marvin LAU-127 Rail Launcher for AIM-120B/C/D and AIM9L/M/X",
        "weight": 52.1,
    }
    STA_04_SUU79_LA127_2x_AIM_120B_AMRAAM___Active_Radar_AAM = {
        "clsid": "{GROWLER_PYLON_04_IB_AM_2X_AIM-120}",
        "name": " [ STA 04	  | SUU79 | LA127 ] - 2x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 495.17,
    }
    STA_04_SUU79_LA127_2x_AIM_120C_AMRAAM___Active_Radar_AAM = {
        "clsid": "{GROWLER_PYLON_04_IB_AM_2X_AIM-120C}",
        "name": " [ STA 04	  | SUU79 | LA127 ] - 2x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 502.43,
    }
    STA_04_SUU79_LA127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = {
        "clsid": "{GROWLER_PYLON_04_IB_AM_2X_AIM-120D}",
        "name": " [ STA 04	  | SUU79 | LA127 ] - 2x AIM-120D AMRAAM - Active Radar AAM (AI Only)",
        "weight": 504.27,
    }
    STA_04_SUU79_LA127_2x_AIM_9M_Sidewinder_IR_AAM = {
        "clsid": "{GROWLER_PYLON_04_IB_SW_2X_AIM-9}",
        "name": " [ STA 04	  | SUU79 | LA127 ] - 2x AIM-9M Sidewinder IR AAM",
        "weight": 350.91,
    }
    STA_04_SUU79_LA127_2x_AIM_9X_Sidewinder_IR_AAM = {
        "clsid": "{GROWLER_PYLON_04_IB_SW_2X_AIM-9X}",
        "name": " [ STA 04	  | SUU79 | LA127 ] - 2x AIM-9X Sidewinder IR AAM",
        "weight": 348.39,
    }
    STA_04_SUU79_LA127_2x_Captive_AIM_9M_for_ACM = {
        "clsid": "{GROWLER_PYLON_04_IB_SW_2X_CATM-9M}",
        "name": " [ STA 04	  | SUU79 | LA127 ] - 2x Captive AIM-9M for ACM",
        "weight": 350.93,
    }
    STA_04_SUU79_LAU115_1x_AIM_7F_Sparrow_Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_SP_1X_AIM-7F}",
        "name": " [ STA 04	  | SUU79 | LAU115 ] - 1x AIM-7F Sparrow Semi-Active Radar",
        "weight": 319.9,
    }
    STA_04_SUU79_LAU115_1x_AIM_7MH_Sparrow_Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_SP_1X_AIM-7H}",
        "name": " [ STA 04	  | SUU79 | LAU115 ] - 1x AIM-7MH Sparrow Semi-Active Radar",
        "weight": 319.9,
    }
    STA_04_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_SP_1X_AIM-7M}",
        "name": " [ STA 04	  | SUU79 | LAU115 ] - 1x AIM-7M Sparrow Semi-Active Radar",
        "weight": 319.9,
    }
    STA_04_SUU79_LAU115_1x_AIM_7P_Sparrow_Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_SP_1X_AIM-7P}",
        "name": " [ STA 04	  | SUU79 | LAU115 ] - 1x AIM-7P Sparrow Semi-Active Radar",
        "weight": 319.9,
    }
    STA_04_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MV_1X_AGM-65E}",
        "name": " [ STA 04	  | SUU79 | LAU117 ] - 1x AGM-65E - Maverick E (Laser ASM - Lg Whd)",
        "weight": 379.47,
    }
    STA_04_SUU79_LAU117_1x_AGM_65F___Maverick_F__IIR_ = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MV_1X_AGM-65F}",
        "name": " [ STA 04	  | SUU79 | LAU117 ] - 1x AGM-65F - Maverick F (IIR)",
        "weight": 394.47,
    }
    STA_04_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MV_1X_CATM-65K}",
        "name": " [ STA 04	  | SUU79 | LAU117 ] - 1x CATM-65K - Captive Trg Round for Mav K (CCD), AI Only",
        "weight": 390.47,
    }
    STA_04_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_AM_1X_AIM-120}",
        "name": " [ STA 04	  | SUU79 | LAU127 ] - 1x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 337.35,
    }
    STA_04_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_AM_1X_AIM-120C}",
        "name": " [ STA 04	  | SUU79 | LAU127 ] - 1x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 340.98,
    }
    STA_04_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_AM_1X_AIM-120D}",
        "name": " [ STA 04	  | SUU79 | LAU127 ] - 1x AIM-120D AMRAAM - Active Radar AAM (AI Only)",
        "weight": 341.9,
    }
    STA_04_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_SW_1X_AIM-9}",
        "name": " [ STA 04	  | SUU79 | LAU127 ] - 1x AIM-9M Sidewinder IR AAM",
        "weight": 265.22,
    }
    STA_04_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_SW_1X_AIM-9X}",
        "name": " [ STA 04	  | SUU79 | LAU127 ] - 1x AIM-9X Sidewinder IR AAM",
        "weight": 263.96,
    }
    STA_04_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_SW_1X_CATM-9M}",
        "name": " [ STA 04	  | SUU79 | LAU127 ] - 1x Captive AIM-9M for ACM",
        "weight": 265.23,
    }
    STA_04_SUU79_LAU127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X = {
        "clsid": "{SUPERHORNET_PYLON_04_LAU127}",
        "name": " [ STA 04	  | SUU79 | LAU127 ] - 1x Marvin LAU-127 Rail Launcher for AIM-120B/C/D and AIM9L/M/X",
        "weight": 45.3,
    }
    STA_04_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_AM_2X_AIM-120}",
        "name": " [ STA 04	  | SUU79 | LAU127 ] - 2x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 495.2,
    }
    STA_04_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_AM_2X_AIM-120C}",
        "name": " [ STA 04	  | SUU79 | LAU127 ] - 2x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 502.46,
    }
    STA_04_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_AM_2X_AIM-120D}",
        "name": " [ STA 04	  | SUU79 | LAU127 ] - 2x AIM-120D AMRAAM - Active Radar AAM (AI Only)",
        "weight": 504.3,
    }
    STA_04_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_SW_2X_AIM-9}",
        "name": " [ STA 04	  | SUU79 | LAU127 ] - 2x AIM-9M Sidewinder IR AAM",
        "weight": 350.94,
    }
    STA_04_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_SW_2X_AIM-9X}",
        "name": " [ STA 04	  | SUU79 | LAU127 ] - 2x AIM-9X Sidewinder IR AAM",
        "weight": 348.42,
    }
    STA_04_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_SW_2X_CATM-9M}",
        "name": " [ STA 04	  | SUU79 | LAU127 ] - 2x Captive AIM-9M for ACM",
        "weight": 350.96,
    }
    STA_04_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_1X_BDU-45B}",
        "name": " [ STA 04	  | SUU80 | BRU32   ] - 1x BDU-45B - 500lb Practice Bomb",
        "weight": 266.47,
    }
    STA_04_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_1X_BDU-45}",
        "name": " [ STA 04	  | SUU80 | BRU32   ] - 1x BDU-45 - 500lb Practice Bomb",
        "weight": 266.47,
    }
    STA_04_SUU80_BRU32_1x_CBU_99___490lbs__247_x_HEAT_Bomblets = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_1X_CBU-99}",
        "name": " [ STA 04	  | SUU80 | BRU32   ] - 1x CBU-99 - 490lbs, 247 x HEAT Bomblets",
        "weight": 56.47,
    }
    STA_04_SUU80_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_1X_GBU-10}",
        "name": " [ STA 04	  | SUU80 | BRU32   ] - 1x GBU-10 - 2000lb Laser Guided Bomb",
        "weight": 946.47,
    }
    STA_04_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_1X_GBU-12}",
        "name": " [ STA 04	  | SUU80 | BRU32   ] - 1x GBU-12 - 500lb Laser Guided Bomb",
        "weight": 311.47,
    }
    STA_04_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_1X_GBU-16}",
        "name": " [ STA 04	  | SUU80 | BRU32   ] - 1x GBU-16 - 1000lb Laser Guided Bomb",
        "weight": 547.47,
    }
    STA_04_SUU80_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_1X_GBU-24}",
        "name": " [ STA 04	  | SUU80 | BRU32   ] - 1x GBU-24A/B Paveway III - 2000lb Laser Guided Bomb",
        "weight": 968.47,
    }
    STA_04_SUU80_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_1X_GBU-31}",
        "name": " [ STA 04	  | SUU80 | BRU32   ] - 1x GBU-31(V)1/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 968.47,
    }
    STA_04_SUU80_BRU32_1x_GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_1X_GBU-31_V_2B}",
        "name": " [ STA 04	  | SUU80 | BRU32   ] - 1x GBU-31(V)2/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 968.47,
    }
    STA_04_SUU80_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_1X_GBU-31V}",
        "name": " [ STA 04	  | SUU80 | BRU32   ] - 1x GBU-31(V)3/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 1015.47,
    }
    STA_04_SUU80_BRU32_1x_GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_1X_GBU-31_V_4B}",
        "name": " [ STA 04	  | SUU80 | BRU32   ] - 1x GBU-31(V)4/B - JDAM, 2000lb GPS Guided Penetrator Bomb",
        "weight": 1004.47,
    }
    STA_04_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_1X_GBU-38}",
        "name": " [ STA 04	  | SUU80 | BRU32   ] - 1x GBU-38 - JDAM, 500lb GPS Guided Bomb",
        "weight": 275.47,
    }
    STA_04_SUU80_BRU32_1x_GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_1X_GBU_54V}",
        "name": " [ STA 04	  | SUU80 | BRU32   ] - 1x GBU-54(V)1/B - LJDAM, 500lb Laser & GPS Guided Bomb LD",
        "weight": 287.47,
    }
    STA_04_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_1X_ROCKEYE}",
        "name": " [ STA 04	  | SUU80 | BRU32   ] - 1x Mk-20 Rockeye - 490lbs CBU, 247 x HEAT Bomblets",
        "weight": 256.47,
    }
    STA_04_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_1X_MK-82Y}",
        "name": " [ STA 04	  | SUU80 | BRU32   ] - 1x Mk-82Y - 500lb GP Chute Retarded HD",
        "weight": 266.47,
    }
    STA_04_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_1X_MK-82_Snakeye}",
        "name": " [ STA 04	  | SUU80 | BRU32   ] - 1x Mk-82 Snakeye - 500lb GP Bomb HD",
        "weight": 283.97,
    }
    STA_04_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_1X_MK-82}",
        "name": " [ STA 04	  | SUU80 | BRU32   ] - 1x Mk-82 - 500lb GP Bomb LD",
        "weight": 262.47,
    }
    STA_04_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_1X_MK-83}",
        "name": " [ STA 04	  | SUU80 | BRU32   ] - 1x Mk-83 - 1000lb GP Bomb LD",
        "weight": 488.47,
    }
    STA_04_SUU80_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MK_1X_MK-84}",
        "name": " [ STA 04	  | SUU80 | BRU32   ] - 1x Mk-84 - 2000lb GP Bomb LD",
        "weight": 946.47,
    }
    STA_04_SUU80_LA118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = {
        "clsid": "{GROWLER_PYLON_04_IB_AR_1X_AGM-88}",
        "name": " [ STA 04	  | SUU80 | LA118 ] - 1x AGM-88C HARM - High Speed Anti-Radiation Missile",
        "weight": 440.87,
    }
    STA_04_02_79_80_BRU32_2x_GBU_10___2000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_IB_MK_2X_GBU-10}",
        "name": " [ STA 04/02 | 79/80 | BRU32   ] - 2x GBU-10 - 2000lb Laser Guided Bomb",
        "weight": 1892.94,
    }
    STA_04_02_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_IB_MK_2X_GBU-12}",
        "name": " [ STA 04/02 | 79/80 | BRU32   ] - 2x GBU-12 - 500lb Laser Guided Bomb",
        "weight": 622.94,
    }
    STA_04_02_79_80_BRU32_2x_GBU_16___1000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_IB_MK_2X_GBU-16}",
        "name": " [ STA 04/02 | 79/80 | BRU32   ] - 2x GBU-16 - 1000lb Laser Guided Bomb",
        "weight": 1094.94,
    }
    STA_04_02_79_80_BRU32_2x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_IB_MK_2X_GBU-24}",
        "name": " [ STA 04/02 | 79/80 | BRU32   ] - 2x GBU-24A/B Paveway III - 2000lb Laser Guided Bomb",
        "weight": 1936.94,
    }
    STA_04_02_79_80_BRU32_2x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_IB_MK_2X_GBU-31}",
        "name": " [ STA 04/02 | 79/80 | BRU32   ] - 2x GBU-31(V)1/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 1936.94,
    }
    STA_04_02_79_80_BRU32_2x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_IB_MK_2X_GBU-31V}",
        "name": " [ STA 04/02 | 79/80 | BRU32   ] - 2x GBU-31(V)3/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 2030.94,
    }
    STA_04_02_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_IB_MK_2X_GBU-38}",
        "name": " [ STA 04/02 | 79/80 | BRU32   ] - 2x GBU-38 - JDAM, 500lb GPS Guided Bomb",
        "weight": 550.94,
    }
    STA_04_02_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_IB_MK_2X_ROCKEYE}",
        "name": " [ STA 04/02 | 79/80 | BRU32   ] - 2x Mk-20 Rockeye - 490lbs CBU, 247 x HEAT Bomblets",
        "weight": 512.94,
    }
    STA_04_02_79_80_BRU32_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_IB_MK_2X_MK-82Y}",
        "name": " [ STA 04/02 | 79/80 | BRU32   ] - 2x Mk-82Y - 500lb GP Chute Retarded HD",
        "weight": 532.94,
    }
    STA_04_02_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_IB_MK_2X_MK-82_Snakeye}",
        "name": " [ STA 04/02 | 79/80 | BRU32   ] - 2x Mk-82 Snakeye - 500lb GP Bomb HD",
        "weight": 567.94,
    }
    STA_04_02_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_IB_MK_2X_MK-82}",
        "name": " [ STA 04/02 | 79/80 | BRU32   ] - 2x Mk-82 - 500lb GP Bomb LD",
        "weight": 524.94,
    }
    STA_04_02_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_IB_MK_2X_MK-83}",
        "name": " [ STA 04/02 | 79/80 | BRU32   ] - 2x Mk-83 - 1000lb GP Bomb LD",
        "weight": 976.94,
    }
    STA_04_02_79_80_BRU32_2x_Mk_84___2000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_02_OB_IB_MK_2X_MK-84}",
        "name": " [ STA 04/02 | 79/80 | BRU32   ] - 2x Mk-84 - 2000lb GP Bomb LD",
        "weight": 1892.94,
    }
    STA_04_03_79_80_BRU32_1x_1x_AGM_154C___JSOW_Unitary_BROACH = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MB_JS_2X_BRU_AGM-154C}",
        "name": " [ STA 04/03 | 79/80 | BRU32   ] - 1x/1x AGM-154C - JSOW Unitary BROACH",
        "weight": 1036.94,
    }
    STA_04_03_SUU79_BRU32_1x_1x_BDU_45B___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MB_MK_BDU-45B}",
        "name": " [ STA 04/03 | SUU79 | BRU32   ] - 1x/1x BDU-45B - 500lb Practice Bomb",
        "weight": 532.94,
    }
    STA_04_03_SUU79_BRU32_1x_1x_BDU_45___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MB_MK_BDU-45}",
        "name": " [ STA 04/03 | SUU79 | BRU32   ] - 1x/1x BDU-45 - 500lb Practice Bomb",
        "weight": 532.94,
    }
    STA_04_03_SUU79_BRU32_1x_1x_CBU_99___490lbs__247_x_HEAT_Bomblets = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MB_MK_CBU-99}",
        "name": " [ STA 04/03 | SUU79 | BRU32   ] - 1x/1x CBU-99 - 490lbs, 247 x HEAT Bomblets",
        "weight": 112.94,
    }
    STA_04_03_SUU79_BRU32_1x_1x_GBU_10___2000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MB_MK_GBU-10}",
        "name": " [ STA 04/03 | SUU79 | BRU32   ] - 1x/1x GBU-10 - 2000lb Laser Guided Bomb",
        "weight": 1892.94,
    }
    STA_04_03_SUU79_BRU32_1x_1x_GBU_12___500lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MB_MK_GBU-12}",
        "name": " [ STA 04/03 | SUU79 | BRU32   ] - 1x/1x GBU-12 - 500lb Laser Guided Bomb",
        "weight": 622.94,
    }
    STA_04_03_SUU79_BRU32_1x_1x_GBU_16___1000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MB_MK_GBU-16}",
        "name": " [ STA 04/03 | SUU79 | BRU32   ] - 1x/1x GBU-16 - 1000lb Laser Guided Bomb",
        "weight": 1094.94,
    }
    STA_04_03_SUU79_BRU32_1x_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MB_MK_GBU-24}",
        "name": " [ STA 04/03 | SUU79 | BRU32   ] - 1x/1x GBU-24A/B Paveway III - 2000lb Laser Guided Bomb",
        "weight": 1936.94,
    }
    STA_04_03_SUU79_BRU32_1x_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MB_MK_GBU-31}",
        "name": " [ STA 04/03 | SUU79 | BRU32   ] - 1x/1x GBU-31(V)1/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 1936.94,
    }
    STA_04_03_SUU79_BRU32_1x_1x_GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MB_MK_GBU-31_V_2B}",
        "name": " [ STA 04/03 | SUU79 | BRU32   ] - 1x/1x GBU-31(V)2/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 1936.94,
    }
    STA_04_03_SUU79_BRU32_1x_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MB_MK_GBU-31V}",
        "name": " [ STA 04/03 | SUU79 | BRU32   ] - 1x/1x GBU-31(V)3/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 2030.94,
    }
    STA_04_03_SUU79_BRU32_1x_1x_GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MB_MK_GBU-31_V_4B}",
        "name": " [ STA 04/03 | SUU79 | BRU32   ] - 1x/1x GBU-31(V)4/B - JDAM, 2000lb GPS Guided Penetrator Bomb",
        "weight": 2008.94,
    }
    STA_04_03_SUU79_BRU32_1x_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MB_MK_GBU-38}",
        "name": " [ STA 04/03 | SUU79 | BRU32   ] - 1x/1x GBU-38 - JDAM, 500lb GPS Guided Bomb",
        "weight": 550.94,
    }
    STA_04_03_SUU79_BRU32_1x_1x_GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MB_MK_GBU_54V}",
        "name": " [ STA 04/03 | SUU79 | BRU32   ] - 1x/1x GBU-54(V)1/B - LJDAM, 500lb Laser & GPS Guided Bomb LD",
        "weight": 574.94,
    }
    STA_04_03_SUU79_BRU32_1x_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MB_MK_ROCKEYE}",
        "name": " [ STA 04/03 | SUU79 | BRU32   ] - 1x/1x Mk-20 Rockeye - 490lbs CBU, 247 x HEAT Bomblets",
        "weight": 512.94,
    }
    STA_04_03_SUU79_BRU32_1x_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MB_MK_MK-82Y}",
        "name": " [ STA 04/03 | SUU79 | BRU32   ] - 1x/1x Mk-82Y - 500lb GP Chute Retarded HD",
        "weight": 532.94,
    }
    STA_04_03_SUU79_BRU32_1x_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MB_MK_MK-82_Snakeye}",
        "name": " [ STA 04/03 | SUU79 | BRU32   ] - 1x/1x Mk-82 Snakeye - 500lb GP Bomb HD",
        "weight": 567.94,
    }
    STA_04_03_SUU79_BRU32_1x_1x_Mk_82___500lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MB_MK_MK-82}",
        "name": " [ STA 04/03 | SUU79 | BRU32   ] - 1x/1x Mk-82 - 500lb GP Bomb LD",
        "weight": 524.94,
    }
    STA_04_03_SUU79_BRU32_1x_1x_Mk_83___1000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MB_MK_MK-83}",
        "name": " [ STA 04/03 | SUU79 | BRU32   ] - 1x/1x Mk-83 - 1000lb GP Bomb LD",
        "weight": 976.94,
    }
    STA_04_03_SUU79_BRU32_1x_1x_Mk_84___2000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_03_IB_MB_MK_MK-84}",
        "name": " [ STA 04/03 | SUU79 | BRU32   ] - 1x/1x Mk-84 - 2000lb GP Bomb LD",
        "weight": 1892.94,
    }
    STA_05_CHEEK__LAU116_Empty_AIM_7_120_Ejectors = {
        "clsid": "{SUPERHORNET_PYLON_05_CN_EMPTY}",
        "name": " [ STA 05	  | CHEEK  | LAU116 ] Empty AIM-7/120 Ejectors",
        "weight": 0,
    }
    STA_05_CHEEK__LAU116_1x_AIM_120B_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_05_AM_1X_AIM-120}",
        "name": " [ STA 05	  | CHEEK  | LAU116 ] - 1x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 157.85,
    }
    STA_05_CHEEK__LAU116_1x_AIM_120C_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_05_AM_1X_AIM-120C}",
        "name": " [ STA 05	  | CHEEK  | LAU116 ] - 1x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 161.48,
    }
    STA_05_CHEEK__LAU116_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_05_AM_1X_AIM-120D}",
        "name": " [ STA 05	  | CHEEK  | LAU116 ] - 1x AIM-120D AMRAAM - Active Radar AAM (AI Only)",
        "weight": 162.4,
    }
    STA_05_CHEEK__LAU116_1x_AIM_7F_Sparrow_Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_05_SP_1X_AIM-7F}",
        "name": " [ STA 05	  | CHEEK  | LAU116 ] - 1x AIM-7F Sparrow Semi-Active Radar",
        "weight": 231,
    }
    STA_05_CHEEK__LAU116_1x_AIM_7MH_Sparrow_Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_05_SP_1X_AIM-7H}",
        "name": " [ STA 05	  | CHEEK  | LAU116 ] - 1x AIM-7MH Sparrow Semi-Active Radar",
        "weight": 231,
    }
    STA_05_CHEEK__LAU116_1x_AIM_7M_Sparrow_Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_05_SP_1X_AIM-7M}",
        "name": " [ STA 05	  | CHEEK  | LAU116 ] - 1x AIM-7M Sparrow Semi-Active Radar",
        "weight": 231,
    }
    STA_05_CHEEK__LAU116_1x_AIM_7P_Sparrow_Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_05_SP_1X_AIM-7P}",
        "name": " [ STA 05	  | CHEEK  | LAU116 ] - 1x AIM-7P Sparrow Semi-Active Radar",
        "weight": 231,
    }
    STA_05_CHEEK__TGPMNT_Empty_TGP_Mount = {
        "clsid": "{SUPERHORNET_PYLON_05_CN_TGP_MOUNT}",
        "name": " [ STA 05	  | CHEEK  | TGPMNT ] Empty TGP Mount",
        "weight": 215.5,
    }
    STA_05_CHEEK__TGPMNT_1x_AN_AAQ_28_LITENING___Targeting_Pod = {
        "clsid": "{SUPERHORNET_PYLON_05_TP_AAQ28}",
        "name": " [ STA 05	  | CHEEK  | TGPMNT ] - 1x AN/AAQ-28 LITENING - Targeting Pod",
        "weight": 233,
    }
    STA_05_CHEEK__TGPMNT_1x_AN_ASQ_228_ATFLIR___Targeting_Pod = {
        "clsid": "{SUPERHORNET_PYLON_05_TP_ASQ228}",
        "name": " [ STA 05	  | CHEEK  | TGPMNT ] - 1x AN/ASQ-228 ATFLIR - Targeting Pod",
        "weight": 190.5,
    }
    STA_05_LA116_LA116_Empty_AIM_7_120_Ejectors = {
        "clsid": "{GROWLER_PYLON_05_FL_EMPTY}",
        "name": " [ STA 05	  | LA116 | LA116 ] Empty AIM-7/120 Ejectors",
        "weight": 0,
    }
    STA_05_LA116_LA116_1x_AIM_120B_AMRAAM___Active_Radar_AAM = {
        "clsid": "{GROWLER_PYLON_05_AM_1X_AIM-120}",
        "name": " [ STA 05	  | LA116 | LA116 ] - 1x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 157.85,
    }
    STA_05_LA116_LA116_1x_AIM_120C_AMRAAM___Active_Radar_AAM = {
        "clsid": "{GROWLER_PYLON_05_AM_1X_AIM-120C}",
        "name": " [ STA 05	  | LA116 | LA116 ] - 1x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 161.48,
    }
    STA_05_LA116_LA116_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = {
        "clsid": "{GROWLER_PYLON_05_AM_1X_AIM-120D}",
        "name": " [ STA 05	  | LA116 | LA116 ] - 1x AIM-120D AMRAAM - Active Radar AAM (AI Only)",
        "weight": 162.4,
    }
    STA_05_LA116_LA116_1x_AIM_7F_Sparrow_Semi_Active_Radar = {
        "clsid": "{GROWLER_PYLON_05_SP_1X_AIM-7F}",
        "name": " [ STA 05	  | LA116 | LA116 ] - 1x AIM-7F Sparrow Semi-Active Radar",
        "weight": 231,
    }
    STA_05_LA116_LA116_1x_AIM_7MH_Sparrow_Semi_Active_Radar = {
        "clsid": "{GROWLER_PYLON_05_SP_1X_AIM-7H}",
        "name": " [ STA 05	  | LA116 | LA116 ] - 1x AIM-7MH Sparrow Semi-Active Radar",
        "weight": 231,
    }
    STA_05_LA116_LA116_1x_AIM_7M_Sparrow_Semi_Active_Radar = {
        "clsid": "{GROWLER_PYLON_05_SP_1X_AIM-7M}",
        "name": " [ STA 05	  | LA116 | LA116 ] - 1x AIM-7M Sparrow Semi-Active Radar",
        "weight": 231,
    }
    STA_05_LA116_LA116_1x_AIM_7P_Sparrow_Semi_Active_Radar = {
        "clsid": "{GROWLER_PYLON_05_SP_1X_AIM-7P}",
        "name": " [ STA 05	  | LA116 | LA116 ] - 1x AIM-7P Sparrow Semi-Active Radar",
        "weight": 231,
    }
    STA_05_LA116_TPMNT_Empty_TGP_Mount = {
        "clsid": "{GROWLER_PYLON_05_CN_TGP_MOUNT}",
        "name": " [ STA 05	  | LA116 | TPMNT ] Empty TGP Mount",
        "weight": 0,
    }
    STA_05_LA116_TPMNT_1x_AN_AAQ_28_LITENING___Targeting_Pod = {
        "clsid": "{GROWLER_PYLON_05_TP_AAQ28}",
        "name": " [ STA 05	  | LA116 | TPMNT ] - 1x AN/AAQ-28 LITENING - Targeting Pod",
        "weight": 208,
    }
    STA_05_LA116_TPMNT_1x_AN_ASQ_228_ATFLIR___Targeting_Pod = {
        "clsid": "{GROWLER_PYLON_05_TP_ASQ228}",
        "name": " [ STA 05	  | LA116 | TPMNT ] - 1x AN/ASQ-228 ATFLIR - Targeting Pod",
        "weight": 195,
    }
    STA_06_SUU78_BRU32_1x_AN_ALQ_99_ICAP_III_Low_Band_Jamming_Pod = {
        "clsid": "{GROWLER_PYLON_06_CN_ANALQ_99_LO_BAND}",
        "name": " [ STA 06	  | SUU78 | BRU32 ] - 1x AN/ALQ-99 ICAP III Low Band Jamming Pod",
        "weight": 465.383,
    }
    STA_06_SUU78_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod = {
        "clsid": "{GROWLER_PYLON_06_CN_PD_1X_AWW-13}",
        "name": " [ STA 06	  | SUU78 | BRU32 ] - 1x AN/AWW-13 Advanced Datalink Pod",
        "weight": 234.47,
    }
    STA_06_SUU78_BRU32_1x_FPU_12_A_Fuel_Tank = {
        "clsid": "{GROWLER_PYLON_06_CN_FT_FPU-12_Fueltank}",
        "name": " [ STA 06	  | SUU78 | BRU32 ] - 1x FPU-12/A Fuel Tank",
        "weight": 1384.47,
    }
    STA_06_SUU78_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis = {
        "clsid": "{GROWLER_PYLON_06_CN_FT_FPU-12_FueltankHighVis}",
        "name": " [ STA 06	  | SUU78 | BRU32 ] - 1x FPU-12/A Fuel Tank - High Vis",
        "weight": 1384.47,
    }
    STA_06_SUU78_BRU32_1x_AN_AAQ_28_LITENING___Targeting_Pod = {
        "clsid": "{SUPERHORNET_PYLON_06_CN_TP_AAQ28}",
        "name": " [ STA 06	  | SUU78 | BRU32   ] - 1x AN/AAQ-28 LITENING - Targeting Pod",
        "weight": 242.47,
    }
    STA_06_SUU78_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod = {
        "clsid": "{SUPERHORNET_PYLON_06_CN_PD_1X_AWW-13}",
        "name": " [ STA 06	  | SUU78 | BRU32   ] - 1x AN/AWW-13 Advanced Datalink Pod",
        "weight": 234.47,
    }
    STA_06_SUU78_BRU32_1x_A_A_42R_1_Aerial_Refueling_Buddy_Pod = {
        "clsid": "{SUPERHORNET_PYLON_06_CN_FT_AA42R}",
        "name": " [ STA 06	  | SUU78 | BRU32   ] - 1x A/A-42R-1 Aerial Refueling Buddy Pod",
        "weight": 1249.47,
    }
    STA_06_SUU78_BRU32_1x_FPU_12_A_Fuel_Tank = {
        "clsid": "{SUPERHORNET_PYLON_06_CN_FT_FPU-12_Fueltank}",
        "name": " [ STA 06	  | SUU78 | BRU32   ] - 1x FPU-12/A Fuel Tank",
        "weight": 1384.47,
    }
    STA_06_SUU78_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis = {
        "clsid": "{SUPERHORNET_PYLON_06_CN_FT_FPU-12_FueltankHighVis}",
        "name": " [ STA 06	  | SUU78 | BRU32   ] - 1x FPU-12/A Fuel Tank - High Vis",
        "weight": 1384.47,
    }
    STA_06_SUU78_EMPTY = {
        "clsid": "{SUPERHORNET_PYLON_06_CN_EMPTY}",
        "name": " [ STA 06	  | SUU78 | EMPTY ]",
        "weight": 0,
    }
    STA_06_SUU78_EMPTY_ = {
        "clsid": "{GROWLER_PYLON_06_CN_EMPTY}",
        "name": " [ STA 06	  | SUU78 | EMPTY ]",
        "weight": 0,
    }
    STA_07_CHEEK__LAU116_1x_AIM_120B_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_07_AM_1X_AIM-120}",
        "name": " [ STA 07	  | CHEEK  | LAU116 ] - 1x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 157.85,
    }
    STA_07_CHEEK__LAU116_1x_AIM_120C_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_07_AM_1X_AIM-120C}",
        "name": " [ STA 07	  | CHEEK  | LAU116 ] - 1x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 161.48,
    }
    STA_07_CHEEK__LAU116_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_07_AM_1X_AIM-120D}",
        "name": " [ STA 07	  | CHEEK  | LAU116 ] - 1x AIM-120D AMRAAM - Active Radar AAM (AI Only)",
        "weight": 162.4,
    }
    STA_07_CHEEK__LAU116_1x_AIM_7F_Sparrow_Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_07_SP_1X_AIM-7F}",
        "name": " [ STA 07	  | CHEEK  | LAU116 ] - 1x AIM-7F Sparrow Semi-Active Radar",
        "weight": 231,
    }
    STA_07_CHEEK__LAU116_1x_AIM_7MH_Sparrow_Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_07_SP_1X_AIM-7H}",
        "name": " [ STA 07	  | CHEEK  | LAU116 ] - 1x AIM-7MH Sparrow Semi-Active Radar",
        "weight": 231,
    }
    STA_07_CHEEK__LAU116_1x_AIM_7M_Sparrow_Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_07_SP_1X_AIM-7M}",
        "name": " [ STA 07	  | CHEEK  | LAU116 ] - 1x AIM-7M Sparrow Semi-Active Radar",
        "weight": 231,
    }
    STA_07_CHEEK__LAU116_1x_AIM_7P_Sparrow_Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_07_SP_1X_AIM-7P}",
        "name": " [ STA 07	  | CHEEK  | LAU116 ] - 1x AIM-7P Sparrow Semi-Active Radar",
        "weight": 231,
    }
    STA_07_LA116_LA116_Empty_AIM_7_120_Ejectors = {
        "clsid": "{GROWLER_PYLON_07_CN_EMPTY}",
        "name": " [ STA 07	  | LA116 | LA116 ] Empty AIM-7/120 Ejectors",
        "weight": 0,
    }
    STA_07_LA116_LA116_1x_AIM_120B_AMRAAM___Active_Radar_AAM = {
        "clsid": "{GROWLER_PYLON_07_AM_1X_AIM-120}",
        "name": " [ STA 07	  | LA116 | LA116 ] - 1x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 157.85,
    }
    STA_07_LA116_LA116_1x_AIM_120C_AMRAAM___Active_Radar_AAM = {
        "clsid": "{GROWLER_PYLON_07_AM_1X_AIM-120C}",
        "name": " [ STA 07	  | LA116 | LA116 ] - 1x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 161.48,
    }
    STA_07_LA116_LA116_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = {
        "clsid": "{GROWLER_PYLON_07_AM_1X_AIM-120D}",
        "name": " [ STA 07	  | LA116 | LA116 ] - 1x AIM-120D AMRAAM - Active Radar AAM (AI Only)",
        "weight": 162.4,
    }
    STA_07_LA116_LA116_1x_AIM_7F_Sparrow_Semi_Active_Radar = {
        "clsid": "{GROWLER_PYLON_07_SP_1X_AIM-7F}",
        "name": " [ STA 07	  | LA116 | LA116 ] - 1x AIM-7F Sparrow Semi-Active Radar",
        "weight": 231,
    }
    STA_07_LA116_LA116_1x_AIM_7MH_Sparrow_Semi_Active_Radar = {
        "clsid": "{GROWLER_PYLON_07_SP_1X_AIM-7H}",
        "name": " [ STA 07	  | LA116 | LA116 ] - 1x AIM-7MH Sparrow Semi-Active Radar",
        "weight": 231,
    }
    STA_07_LA116_LA116_1x_AIM_7M_Sparrow_Semi_Active_Radar = {
        "clsid": "{GROWLER_PYLON_07_SP_1X_AIM-7M}",
        "name": " [ STA 07	  | LA116 | LA116 ] - 1x AIM-7M Sparrow Semi-Active Radar",
        "weight": 231,
    }
    STA_07_LA116_LA116_1x_AIM_7P_Sparrow_Semi_Active_Radar = {
        "clsid": "{GROWLER_PYLON_07_SP_1X_AIM-7P}",
        "name": " [ STA 07	  | LA116 | LA116 ] - 1x AIM-7P Sparrow Semi-Active Radar",
        "weight": 231,
    }
    STA_07_SUU79_BRU32_Remove_SUU_79A_A_Pylon = {
        "clsid": "{SUPERHORNET_PYLON_08_REMOVE_SUU79}",
        "name": " [ STA 07	  | SUU79 | BRU32   ] Remove SUU-79A/A Pylon",
        "weight": 0,
    }
    STA_08_SUU79_BRU32_1x_AGM_154A___JSOW_CEB__CBU_type_ = {
        "clsid": "{GROWLER_PYLON_08_IB_JS_1X_AGM-154A}",
        "name": " [ STA 08	  | SUU79 | BRU32 ] - 1x AGM-154A - JSOW CEB (CBU-type)",
        "weight": 519.47,
    }
    STA_08_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH = {
        "clsid": "{GROWLER_PYLON_08_IB_JS_1X_AGM-154C}",
        "name": " [ STA 08	  | SUU79 | BRU32 ] - 1x AGM-154C - JSOW Unitary BROACH",
        "weight": 518.47,
    }
    STA_08_SUU79_BRU32_1x_AGM_154A___JSOW_CEB__CBU_type_ = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_JS_1X_AGM-154A}",
        "name": " [ STA 08	  | SUU79 | BRU32   ] - 1x AGM-154A - JSOW CEB (CBU-type)",
        "weight": 519.47,
    }
    STA_08_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_JS_1X_AGM-154C}",
        "name": " [ STA 08	  | SUU79 | BRU32   ] - 1x AGM-154C - JSOW Unitary BROACH",
        "weight": 518.47,
    }
    STA_08_SUU79_BRU32_1x_AGM_84D_Harpoon_Anti_Ship_Missile = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_SM_1X_AGM-84D}",
        "name": " [ STA 08	  | SUU79 | BRU32   ] - 1x AGM-84D Harpoon Anti-Ship Missile",
        "weight": 574.47,
    }
    STA_08_SUU79_BRU32_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_SM_1X_AGM-84E}",
        "name": " [ STA 08	  | SUU79 | BRU32   ] - 1x AGM-84E Harpoon/SLAM (Stand-Off Land-Attack Missile)",
        "weight": 662.47,
    }
    STA_08_SUU79_BRU32_1x_AGM_84H_SLAM_ER__Expanded_Response_ = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_SM_1X_AGM-84H}",
        "name": " [ STA 08	  | SUU79 | BRU32   ] - 1x AGM-84H SLAM-ER (Expanded Response)",
        "weight": 709.47,
    }
    STA_08_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod = {
        "clsid": "{SUPERHORNET_PYLON_08_IB_PD_1X_AWW-13}",
        "name": " [ STA 08	  | SUU79 | BRU32   ] - 1x AN/AWW-13 Advanced Datalink Pod",
        "weight": 234.47,
    }
    STA_08_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod_ = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_PD_1X_AWW-13}",
        "name": " [ STA 08	  | SUU79 | BRU32   ] - 1x AN/AWW-13 Advanced Datalink Pod",
        "weight": 234.47,
    }
    STA_08_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank = {
        "clsid": "{SUPERHORNET_PYLON_08_CN_FT_FPU-12_Fueltank}",
        "name": " [ STA 08	  | SUU79 | BRU32   ] - 1x FPU-12/A Fuel Tank",
        "weight": 1384.47,
    }
    STA_08_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank_ = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_FT_FPU-12_Fueltank}",
        "name": " [ STA 08	  | SUU79 | BRU32   ] - 1x FPU-12/A Fuel Tank",
        "weight": 1384.47,
    }
    STA_08_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis = {
        "clsid": "{SUPERHORNET_PYLON_08_CN_FT_FPU-12_FueltankHighVis}",
        "name": " [ STA 08	  | SUU79 | BRU32   ] - 1x FPU-12/A Fuel Tank - High Vis",
        "weight": 1384.47,
    }
    STA_08_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis_ = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_FT_FPU-12_FueltankHighVis}",
        "name": " [ STA 08	  | SUU79 | BRU32   ] - 1x FPU-12/A Fuel Tank - High Vis",
        "weight": 1384.47,
    }
    STA_08_SUU79_BRU33_2x_BDU_45B___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_BR2_BDU-45B}",
        "name": " [ STA 08	  | SUU79 | BRU33   ] - 2x BDU-45B - 500lb Practice Bomb",
        "weight": 589.1885,
    }
    STA_08_SUU79_BRU33_2x_BDU_45___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_BR2_BDU-45}",
        "name": " [ STA 08	  | SUU79 | BRU33   ] - 2x BDU-45 - 500lb Practice Bomb",
        "weight": 589.1885,
    }
    STA_08_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_BR2_GBU-12}",
        "name": " [ STA 08	  | SUU79 | BRU33   ] - 2x GBU-12 - 500lb Laser Guided Bomb",
        "weight": 679.1885,
    }
    STA_08_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_BR2_MK-82Y}",
        "name": " [ STA 08	  | SUU79 | BRU33   ] - 2x Mk-82Y - 500lb GP Chute Retarded HD",
        "weight": 589.1885,
    }
    STA_08_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_BR2_MK-82_Snakeye}",
        "name": " [ STA 08	  | SUU79 | BRU33   ] - 2x Mk-82 Snakeye - 500lb GP Bomb HD",
        "weight": 624.1885,
    }
    STA_08_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_BR2_MK-82}",
        "name": " [ STA 08	  | SUU79 | BRU33   ] - 2x Mk-82 - 500lb GP Bomb LD",
        "weight": 581.1885,
    }
    STA_08_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_BR2_MK-83}",
        "name": " [ STA 08	  | SUU79 | BRU33   ] - 2x Mk-83 - 1000lb GP Bomb LD",
        "weight": 1033.1885,
    }
    STA_08_SUU79_BRU42_1x_ADM_141A_TALD = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_TD_1X_BRU_ADM-141A}",
        "name": " [ STA 08	  | SUU79 | BRU42   ] - 1x ADM-141A TALD",
        "weight": 265.27,
    }
    STA_08_SUU79_BRU42_2x_ADM_141A_TALD = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_TD_2X_BRU_ADM-141A}",
        "name": " [ STA 08	  | SUU79 | BRU42   ] - 2x ADM-141A TALD",
        "weight": 445.27,
    }
    STA_08_SUU79_BRU42_3x_ADM_141A_TALD = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_TD_3X_BRU_ADM-141A}",
        "name": " [ STA 08	  | SUU79 | BRU42   ] - 3x ADM-141A TALD",
        "weight": 625.27,
    }
    STA_08_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type_ = {
        "clsid": "{GROWLER_PYLON_08_IB_JS_1X_BRU_AGM-154A}",
        "name": " [ STA 08	  | SUU79 | BRU55 ] - 1x AGM-154A - JSOW CEB (CBU-type)",
        "weight": 606.97,
    }
    STA_08_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH = {
        "clsid": "{GROWLER_PYLON_08_IB_JS_1X_BRU_AGM-154C}",
        "name": " [ STA 08	  | SUU79 | BRU55 ] - 1x AGM-154C - JSOW Unitary BROACH",
        "weight": 605.97,
    }
    STA_08_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type_ = {
        "clsid": "{GROWLER_PYLON_08_IB_JS_2X_BRU_AGM-154A}",
        "name": " [ STA 08	  | SUU79 | BRU55 ] - 2x AGM-154A - JSOW CEB (CBU-type)",
        "weight": 1091.97,
    }
    STA_08_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH = {
        "clsid": "{GROWLER_PYLON_08_IB_JS_2X_BRU_AGM-154C}",
        "name": " [ STA 08	  | SUU79 | BRU55 ] - 2x AGM-154C - JSOW Unitary BROACH",
        "weight": 1089.97,
    }
    STA_08_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type_ = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_JS_1X_BRU_AGM-154A}",
        "name": " [ STA 08	  | SUU79 | BRU55   ] - 1x AGM-154A - JSOW CEB (CBU-type)",
        "weight": 606.97,
    }
    STA_08_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_JS_1X_BRU_AGM-154C}",
        "name": " [ STA 08	  | SUU79 | BRU55   ] - 1x AGM-154C - JSOW Unitary BROACH",
        "weight": 605.97,
    }
    STA_08_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type_ = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_JS_2X_BRU_AGM-154A}",
        "name": " [ STA 08	  | SUU79 | BRU55   ] - 2x AGM-154A - JSOW CEB (CBU-type)",
        "weight": 1091.97,
    }
    STA_08_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_JS_2X_BRU_AGM-154C}",
        "name": " [ STA 08	  | SUU79 | BRU55   ] - 2x AGM-154C - JSOW Unitary BROACH",
        "weight": 1089.97,
    }
    STA_08_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_BR55_2X_GBU-32}",
        "name": " [ STA 08	  | SUU79 | BRU55   ] - 2x GBU-32(V)2/B - JDAM, 1000lb GPS Guided Bomb",
        "weight": 1055.97,
    }
    STA_08_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_BR55_2X_GBU-38}",
        "name": " [ STA 08	  | SUU79 | BRU55   ] - 2x GBU-38 - JDAM, 500lb GPS Guided Bomb",
        "weight": 603.97,
    }
    STA_08_SUU79_EMPTY = {
        "clsid": "{SUPERHORNET_PYLON_08_IB_EMPTY}",
        "name": " [ STA 08	  | SUU79 | EMPTY ]",
        "weight": 0,
    }
    STA_08_SUU79_LA127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = {
        "clsid": "{GROWLER_PYLON_08_IB_AM_1X_AIM-120}",
        "name": " [ STA 08	  | SUU79 | LA127 ] - 1x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 337.32,
    }
    STA_08_SUU79_LA127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = {
        "clsid": "{GROWLER_PYLON_08_IB_AM_1X_AIM-120C}",
        "name": " [ STA 08	  | SUU79 | LA127 ] - 1x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 340.95,
    }
    STA_08_SUU79_LA127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = {
        "clsid": "{GROWLER_PYLON_08_IB_AM_1X_AIM-120D}",
        "name": " [ STA 08	  | SUU79 | LA127 ] - 1x AIM-120D AMRAAM - Active Radar AAM (AI Only)",
        "weight": 341.87,
    }
    STA_08_SUU79_LA127_1x_AIM_9M_Sidewinder_IR_AAM = {
        "clsid": "{GROWLER_PYLON_08_IB_SW_1X_AIM-9}",
        "name": " [ STA 08	  | SUU79 | LA127 ] - 1x AIM-9M Sidewinder IR AAM",
        "weight": 265.19,
    }
    STA_08_SUU79_LA127_1x_AIM_9X_Sidewinder_IR_AAM = {
        "clsid": "{GROWLER_PYLON_08_IB_SW_1X_AIM-9X}",
        "name": " [ STA 08	  | SUU79 | LA127 ] - 1x AIM-9X Sidewinder IR AAM",
        "weight": 263.93,
    }
    STA_08_SUU79_LA127_1x_Captive_AIM_9M_for_ACM = {
        "clsid": "{GROWLER_PYLON_08_IB_SW_1X_CATM-9M}",
        "name": " [ STA 08	  | SUU79 | LA127 ] - 1x Captive AIM-9M for ACM",
        "weight": 265.2,
    }
    STA_08_SUU79_LA127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X = {
        "clsid": "{GROWLER_PYLON_08_IB_LAU127}",
        "name": " [ STA 08	  | SUU79 | LA127 ] - 1x Marvin LAU-127 Rail Launcher for AIM-120B/C/D and AIM9L/M/X",
        "weight": 52.1,
    }
    STA_08_SUU79_LA127_2x_AIM_120B_AMRAAM___Active_Radar_AAM = {
        "clsid": "{GROWLER_PYLON_08_IB_AM_2X_AIM-120}",
        "name": " [ STA 08	  | SUU79 | LA127 ] - 2x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 495.17,
    }
    STA_08_SUU79_LA127_2x_AIM_120C_AMRAAM___Active_Radar_AAM = {
        "clsid": "{GROWLER_PYLON_08_IB_AM_2X_AIM-120C}",
        "name": " [ STA 08	  | SUU79 | LA127 ] - 2x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 502.43,
    }
    STA_08_SUU79_LA127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = {
        "clsid": "{GROWLER_PYLON_08_IB_AM_2X_AIM-120D}",
        "name": " [ STA 08	  | SUU79 | LA127 ] - 2x AIM-120D AMRAAM - Active Radar AAM (AI Only)",
        "weight": 504.27,
    }
    STA_08_SUU79_LA127_2x_AIM_9M_Sidewinder_IR_AAM = {
        "clsid": "{GROWLER_PYLON_08_IB_SW_2X_AIM-9}",
        "name": " [ STA 08	  | SUU79 | LA127 ] - 2x AIM-9M Sidewinder IR AAM",
        "weight": 350.91,
    }
    STA_08_SUU79_LA127_2x_AIM_9X_Sidewinder_IR_AAM = {
        "clsid": "{GROWLER_PYLON_08_IB_SW_2X_AIM-9X}",
        "name": " [ STA 08	  | SUU79 | LA127 ] - 2x AIM-9X Sidewinder IR AAM",
        "weight": 348.39,
    }
    STA_08_SUU79_LA127_2x_Captive_AIM_9M_for_ACM = {
        "clsid": "{GROWLER_PYLON_08_IB_SW_2X_CATM-9M}",
        "name": " [ STA 08	  | SUU79 | LA127 ] - 2x Captive AIM-9M for ACM",
        "weight": 350.93,
    }
    STA_08_SUU79_LAU115_1x_AIM_7F_Sparrow_Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_SP_1X_AIM-7F}",
        "name": " [ STA 08	  | SUU79 | LAU115 ] - 1x AIM-7F Sparrow Semi-Active Radar",
        "weight": 319.9,
    }
    STA_08_SUU79_LAU115_1x_AIM_7MH_Sparrow_Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_SP_1X_AIM-7H}",
        "name": " [ STA 08	  | SUU79 | LAU115 ] - 1x AIM-7MH Sparrow Semi-Active Radar",
        "weight": 319.9,
    }
    STA_08_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_SP_1X_AIM-7M}",
        "name": " [ STA 08	  | SUU79 | LAU115 ] - 1x AIM-7M Sparrow Semi-Active Radar",
        "weight": 319.9,
    }
    STA_08_SUU79_LAU115_1x_AIM_7P_Sparrow_Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_SP_1X_AIM-7P}",
        "name": " [ STA 08	  | SUU79 | LAU115 ] - 1x AIM-7P Sparrow Semi-Active Radar",
        "weight": 319.9,
    }
    STA_08_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MV_1X_AGM-65E}",
        "name": " [ STA 08	  | SUU79 | LAU117 ] - 1x AGM-65E - Maverick E (Laser ASM - Lg Whd)",
        "weight": 379.47,
    }
    STA_08_SUU79_LAU117_1x_AGM_65F___Maverick_F__IIR_ = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MV_1X_AGM-65F}",
        "name": " [ STA 08	  | SUU79 | LAU117 ] - 1x AGM-65F - Maverick F (IIR)",
        "weight": 394.47,
    }
    STA_08_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MV_1X_CATM-65K}",
        "name": " [ STA 08	  | SUU79 | LAU117 ] - 1x CATM-65K - Captive Trg Round for Mav K (CCD), AI Only",
        "weight": 390.47,
    }
    STA_08_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_AM_1X_AIM-120}",
        "name": " [ STA 08	  | SUU79 | LAU127 ] - 1x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 337.35,
    }
    STA_08_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_AM_1X_AIM-120C}",
        "name": " [ STA 08	  | SUU79 | LAU127 ] - 1x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 340.98,
    }
    STA_08_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_AM_1X_AIM-120D}",
        "name": " [ STA 08	  | SUU79 | LAU127 ] - 1x AIM-120D AMRAAM - Active Radar AAM (AI Only)",
        "weight": 341.9,
    }
    STA_08_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_SW_1X_AIM-9}",
        "name": " [ STA 08	  | SUU79 | LAU127 ] - 1x AIM-9M Sidewinder IR AAM",
        "weight": 265.22,
    }
    STA_08_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_SW_1X_AIM-9X}",
        "name": " [ STA 08	  | SUU79 | LAU127 ] - 1x AIM-9X Sidewinder IR AAM",
        "weight": 263.96,
    }
    STA_08_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_SW_1X_CATM-9M}",
        "name": " [ STA 08	  | SUU79 | LAU127 ] - 1x Captive AIM-9M for ACM",
        "weight": 265.23,
    }
    STA_08_SUU79_LAU127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X = {
        "clsid": "{SUPERHORNET_PYLON_08_IB_LAU127}",
        "name": " [ STA 08	  | SUU79 | LAU127 ] - 1x Marvin LAU-127 Rail Launcher for AIM-120B/C/D and AIM9L/M/X",
        "weight": 45.3,
    }
    STA_08_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_AM_2X_AIM-120}",
        "name": " [ STA 08	  | SUU79 | LAU127 ] - 2x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 495.2,
    }
    STA_08_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_AM_2X_AIM-120C}",
        "name": " [ STA 08	  | SUU79 | LAU127 ] - 2x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 502.46,
    }
    STA_08_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_AM_2X_AIM-120D}",
        "name": " [ STA 08	  | SUU79 | LAU127 ] - 2x AIM-120D AMRAAM - Active Radar AAM (AI Only)",
        "weight": 504.3,
    }
    STA_08_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_SW_2X_AIM-9}",
        "name": " [ STA 08	  | SUU79 | LAU127 ] - 2x AIM-9M Sidewinder IR AAM",
        "weight": 350.94,
    }
    STA_08_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_SW_2X_AIM-9X}",
        "name": " [ STA 08	  | SUU79 | LAU127 ] - 2x AIM-9X Sidewinder IR AAM",
        "weight": 348.42,
    }
    STA_08_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_SW_2X_CATM-9M}",
        "name": " [ STA 08	  | SUU79 | LAU127 ] - 2x Captive AIM-9M for ACM",
        "weight": 350.96,
    }
    STA_08_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_1X_BDU-45B}",
        "name": " [ STA 08	  | SUU80 | BRU32   ] - 1x BDU-45B - 500lb Practice Bomb",
        "weight": 266.47,
    }
    STA_08_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_1X_BDU-45}",
        "name": " [ STA 08	  | SUU80 | BRU32   ] - 1x BDU-45 - 500lb Practice Bomb",
        "weight": 266.47,
    }
    STA_08_SUU80_BRU32_1x_CBU_99___490lbs__247_x_HEAT_Bomblets = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_1X_CBU-99}",
        "name": " [ STA 08	  | SUU80 | BRU32   ] - 1x CBU-99 - 490lbs, 247 x HEAT Bomblets",
        "weight": 56.47,
    }
    STA_08_SUU80_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_1X_GBU-10}",
        "name": " [ STA 08	  | SUU80 | BRU32   ] - 1x GBU-10 - 2000lb Laser Guided Bomb",
        "weight": 946.47,
    }
    STA_08_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_1X_GBU-12}",
        "name": " [ STA 08	  | SUU80 | BRU32   ] - 1x GBU-12 - 500lb Laser Guided Bomb",
        "weight": 311.47,
    }
    STA_08_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_1X_GBU-16}",
        "name": " [ STA 08	  | SUU80 | BRU32   ] - 1x GBU-16 - 1000lb Laser Guided Bomb",
        "weight": 547.47,
    }
    STA_08_SUU80_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_1X_GBU-24}",
        "name": " [ STA 08	  | SUU80 | BRU32   ] - 1x GBU-24A/B Paveway III - 2000lb Laser Guided Bomb",
        "weight": 968.47,
    }
    STA_08_SUU80_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_1X_GBU-31}",
        "name": " [ STA 08	  | SUU80 | BRU32   ] - 1x GBU-31(V)1/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 968.47,
    }
    STA_08_SUU80_BRU32_1x_GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_1X_GBU-31_V_2B}",
        "name": " [ STA 08	  | SUU80 | BRU32   ] - 1x GBU-31(V)2/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 968.47,
    }
    STA_08_SUU80_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_1X_GBU-31V}",
        "name": " [ STA 08	  | SUU80 | BRU32   ] - 1x GBU-31(V)3/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 1015.47,
    }
    STA_08_SUU80_BRU32_1x_GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_1X_GBU-31_V_4B}",
        "name": " [ STA 08	  | SUU80 | BRU32   ] - 1x GBU-31(V)4/B - JDAM, 2000lb GPS Guided Penetrator Bomb",
        "weight": 1004.47,
    }
    STA_08_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_1X_GBU-32}",
        "name": " [ STA 08	  | SUU80 | BRU32   ] - 1x GBU-32(V)2/B - JDAM, 1000lb GPS Guided Bomb",
        "weight": 501.47,
    }
    STA_08_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_1X_GBU-38}",
        "name": " [ STA 08	  | SUU80 | BRU32   ] - 1x GBU-38 - JDAM, 500lb GPS Guided Bomb",
        "weight": 275.47,
    }
    STA_08_SUU80_BRU32_1x_GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_1X_GBU_54V}",
        "name": " [ STA 08	  | SUU80 | BRU32   ] - 1x GBU-54(V)1/B - LJDAM, 500lb Laser & GPS Guided Bomb LD",
        "weight": 287.47,
    }
    STA_08_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_1X_ROCKEYE}",
        "name": " [ STA 08	  | SUU80 | BRU32   ] - 1x Mk-20 Rockeye - 490lbs CBU, 247 x HEAT Bomblets",
        "weight": 256.47,
    }
    STA_08_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_1X_MK-82Y}",
        "name": " [ STA 08	  | SUU80 | BRU32   ] - 1x Mk-82Y - 500lb GP Chute Retarded HD",
        "weight": 266.47,
    }
    STA_08_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_1X_MK-82_Snakeye}",
        "name": " [ STA 08	  | SUU80 | BRU32   ] - 1x Mk-82 Snakeye - 500lb GP Bomb HD",
        "weight": 283.97,
    }
    STA_08_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_1X_MK-82}",
        "name": " [ STA 08	  | SUU80 | BRU32   ] - 1x Mk-82 - 500lb GP Bomb LD",
        "weight": 262.47,
    }
    STA_08_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_1X_MK-83}",
        "name": " [ STA 08	  | SUU80 | BRU32   ] - 1x Mk-83 - 1000lb GP Bomb LD",
        "weight": 488.47,
    }
    STA_08_SUU80_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MK_1X_MK-84}",
        "name": " [ STA 08	  | SUU80 | BRU32   ] - 1x Mk-84 - 2000lb GP Bomb LD",
        "weight": 946.47,
    }
    STA_08_SUU80_LA118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = {
        "clsid": "{GROWLER_PYLON_08_IB_AR_1X_AGM-88}",
        "name": " [ STA 08	  | SUU80 | LA118 ] - 1x AGM-88C HARM - High Speed Anti-Radiation Missile",
        "weight": 440.87,
    }
    STA_08_09_SUU79_BRU32_1x_1x_AGM_154C___JSOW_Unitary_BROACH = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MB_JS_2X_BRU_AGM-154C}",
        "name": " [ STA 08/09 | SUU79 | BRU32   ] - 1x/1x AGM-154C - JSOW Unitary BROACH",
        "weight": 1036.94,
    }
    STA_09_SUU79_BRU32_1x_AN_ALQ_249_Mid_Band_Next_Generation_Jamming_Pod = {
        "clsid": "{GROWLER_PYLON_09_MB_ALQ_249_MID_BAND}",
        "name": " [ STA 09	  | SUU79 | BRU32 ] - 1x AN/ALQ-249 Mid Band Next Generation Jamming Pod",
        "weight": 465.383,
    }
    STA_09_SUU79_BRU32_1x_AN_ALQ_99_ICAP_III_High_Band_Jamming_Pod = {
        "clsid": "{GROWLER_PYLON_09_MB_ALQ_99_HI_BAND}",
        "name": " [ STA 09	  | SUU79 | BRU32 ] - 1x AN/ALQ-99 ICAP III High Band Jamming Pod",
        "weight": 465.383,
    }
    STA_09_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank = {
        "clsid": "{GROWLER_PYLON_10_MB_FT_FPU-12_Fueltank}",
        "name": " [ STA 09	  | SUU79 | BRU32 ] - 1x FPU-12/A Fuel Tank",
        "weight": 1384.47,
    }
    STA_09_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis = {
        "clsid": "{GROWLER_PYLON_10_MB_FT_FPU-12_FueltankHighVis}",
        "name": " [ STA 09	  | SUU79 | BRU32 ] - 1x FPU-12/A Fuel Tank - High Vis",
        "weight": 1384.47,
    }
    STA_09_SUU79_BRU32_1x_AGM_154A___JSOW_CEB__CBU_type_ = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_JS_1X_AGM-154A}",
        "name": " [ STA 09	  | SUU79 | BRU32   ] - 1x AGM-154A - JSOW CEB (CBU-type)",
        "weight": 519.47,
    }
    STA_09_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_JS_1X_AGM-154C}",
        "name": " [ STA 09	  | SUU79 | BRU32   ] - 1x AGM-154C - JSOW Unitary BROACH",
        "weight": 518.47,
    }
    STA_09_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_JS_1X_BRU32_AGM-154C}",
        "name": " [ STA 09	  | SUU79 | BRU32   ] - 1x AGM-154C - JSOW Unitary BROACH",
        "weight": 518.47,
    }
    STA_09_SUU79_BRU32_1x_ALQ_167_Countermeasures_System = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_PD_1X_ALQ-167}",
        "name": " [ STA 09	  | SUU79 | BRU32   ] - 1x ALQ-167 Countermeasures System",
        "weight": 84.47,
    }
    STA_09_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_PD_1X_AWW-13}",
        "name": " [ STA 09	  | SUU79 | BRU32   ] - 1x AN/AWW-13 Advanced Datalink Pod",
        "weight": 234.47,
    }
    STA_09_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_FT_FPU-12_Fueltank}",
        "name": " [ STA 09	  | SUU79 | BRU32   ] - 1x FPU-12/A Fuel Tank",
        "weight": 1384.47,
    }
    STA_09_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_FT_FPU-12_FueltankHighVis}",
        "name": " [ STA 09	  | SUU79 | BRU32   ] - 1x FPU-12/A Fuel Tank - High Vis",
        "weight": 1384.47,
    }
    STA_09_SUU79_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_MK_1X_GBU-10}",
        "name": " [ STA 09	  | SUU79 | BRU32   ] - 1x GBU-10 - 2000lb Laser Guided Bomb",
        "weight": 946.47,
    }
    STA_09_SUU79_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_MK_1X_GBU-12}",
        "name": " [ STA 09	  | SUU79 | BRU32   ] - 1x GBU-12 - 500lb Laser Guided Bomb",
        "weight": 311.47,
    }
    STA_09_SUU79_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_MK_1X_GBU-16}",
        "name": " [ STA 09	  | SUU79 | BRU32   ] - 1x GBU-16 - 1000lb Laser Guided Bomb",
        "weight": 547.47,
    }
    STA_09_SUU79_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_MK_1X_GBU-24}",
        "name": " [ STA 09	  | SUU79 | BRU32   ] - 1x GBU-24A/B Paveway III - 2000lb Laser Guided Bomb",
        "weight": 968.47,
    }
    STA_09_SUU79_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_MK_1X_GBU-31}",
        "name": " [ STA 09	  | SUU79 | BRU32   ] - 1x GBU-31(V)1/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 968.47,
    }
    STA_09_SUU79_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_MK_1X_GBU-31V}",
        "name": " [ STA 09	  | SUU79 | BRU32   ] - 1x GBU-31(V)3/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 1015.47,
    }
    STA_09_SUU79_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_MK_1X_GBU-38}",
        "name": " [ STA 09	  | SUU79 | BRU32   ] - 1x GBU-38 - JDAM, 500lb GPS Guided Bomb",
        "weight": 275.47,
    }
    STA_09_SUU79_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_MK_1X_ROCKEYE}",
        "name": " [ STA 09	  | SUU79 | BRU32   ] - 1x Mk-20 Rockeye - 490lbs CBU, 247 x HEAT Bomblets",
        "weight": 256.47,
    }
    STA_09_SUU79_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_MK_1X_MK-82Y}",
        "name": " [ STA 09	  | SUU79 | BRU32   ] - 1x Mk-82Y - 500lb GP Chute Retarded HD",
        "weight": 266.47,
    }
    STA_09_SUU79_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_MK_1X_MK-82_Snakeye}",
        "name": " [ STA 09	  | SUU79 | BRU32   ] - 1x Mk-82 Snakeye - 500lb GP Bomb HD",
        "weight": 283.97,
    }
    STA_09_SUU79_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_MK_1X_MK-82}",
        "name": " [ STA 09	  | SUU79 | BRU32   ] - 1x Mk-82 - 500lb GP Bomb LD",
        "weight": 262.47,
    }
    STA_09_SUU79_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_MK_1X_MK-83}",
        "name": " [ STA 09	  | SUU79 | BRU32   ] - 1x Mk-83 - 1000lb GP Bomb LD",
        "weight": 488.47,
    }
    STA_09_SUU79_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_MK_1X_MK-84}",
        "name": " [ STA 09	  | SUU79 | BRU32   ] - 1x Mk-84 - 2000lb GP Bomb LD",
        "weight": 946.47,
    }
    STA_09_SUU79_BRU33_2x_BDU_45B___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_BR2_BDU-45B}",
        "name": " [ STA 09	  | SUU79 | BRU33   ] - 2x BDU-45B - 500lb Practice Bomb",
        "weight": 589.1885,
    }
    STA_09_SUU79_BRU33_2x_BDU_45___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_BR2_BDU-45}",
        "name": " [ STA 09	  | SUU79 | BRU33   ] - 2x BDU-45 - 500lb Practice Bomb",
        "weight": 589.1885,
    }
    STA_09_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_BR2_GBU-12}",
        "name": " [ STA 09	  | SUU79 | BRU33   ] - 2x GBU-12 - 500lb Laser Guided Bomb",
        "weight": 679.1885,
    }
    STA_09_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_MK_BR2_GBU-12}",
        "name": " [ STA 09	  | SUU79 | BRU33   ] - 2x GBU-12 - 500lb Laser Guided Bomb",
        "weight": 679.1885,
    }
    STA_09_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_BR2_MK-82Y}",
        "name": " [ STA 09	  | SUU79 | BRU33   ] - 2x Mk-82Y - 500lb GP Chute Retarded HD",
        "weight": 589.1885,
    }
    STA_09_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_BR2_MK-82_Snakeye}",
        "name": " [ STA 09	  | SUU79 | BRU33   ] - 2x Mk-82 Snakeye - 500lb GP Bomb HD",
        "weight": 624.1885,
    }
    STA_09_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_MK_BR2_MK-82_Snakeye}",
        "name": " [ STA 09	  | SUU79 | BRU33   ] - 2x Mk-82 Snakeye - 500lb GP Bomb HD",
        "weight": 624.1885,
    }
    STA_09_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_BR2_MK-82}",
        "name": " [ STA 09	  | SUU79 | BRU33   ] - 2x Mk-82 - 500lb GP Bomb LD",
        "weight": 581.1885,
    }
    STA_09_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_MK_BR2_MK-82}",
        "name": " [ STA 09	  | SUU79 | BRU33   ] - 2x Mk-82 - 500lb GP Bomb LD",
        "weight": 581.1885,
    }
    STA_09_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_BR2_MK-83}",
        "name": " [ STA 09	  | SUU79 | BRU33   ] - 2x Mk-83 - 1000lb GP Bomb LD",
        "weight": 1033.1885,
    }
    STA_09_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_MK_BR2_MK-83}",
        "name": " [ STA 09	  | SUU79 | BRU33   ] - 2x Mk-83 - 1000lb GP Bomb LD",
        "weight": 1033.1885,
    }
    STA_09_SUU79_BRU41_6x_BDU_33___25lb_Practice_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_BD_BRU41_6X_BDU-33}",
        "name": " [ STA 09	  | SUU79 | BRU41   ] - 6x BDU-33 - 25lb Practice Bomb LD",
        "weight": 195.713,
    }
    STA_09_SUU79_BRU42_1x_ADM_141A_TALD = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_TD_1X_BRU_ADM-141A}",
        "name": " [ STA 09	  | SUU79 | BRU42   ] - 1x ADM-141A TALD",
        "weight": 265.27,
    }
    STA_09_SUU79_BRU42_1x_ADM_141A_TALD_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_TD_1X_BRU_ADM-141A}",
        "name": " [ STA 09	  | SUU79 | BRU42   ] - 1x ADM-141A TALD",
        "weight": 265.27,
    }
    STA_09_SUU79_BRU42_2x_ADM_141A_TALD = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_TD_2X_BRU_ADM-141A}",
        "name": " [ STA 09	  | SUU79 | BRU42   ] - 2x ADM-141A TALD",
        "weight": 445.27,
    }
    STA_09_SUU79_BRU42_2x_ADM_141A_TALD_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_TD_2X_BRU_ADM-141A}",
        "name": " [ STA 09	  | SUU79 | BRU42   ] - 2x ADM-141A TALD",
        "weight": 445.27,
    }
    STA_09_SUU79_BRU42_3x_ADM_141A_TALD = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_TD_3X_BRU_ADM-141A}",
        "name": " [ STA 09	  | SUU79 | BRU42   ] - 3x ADM-141A TALD",
        "weight": 625.27,
    }
    STA_09_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type_ = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_JS_1X_BRU_AGM-154A}",
        "name": " [ STA 09	  | SUU79 | BRU55   ] - 1x AGM-154A - JSOW CEB (CBU-type)",
        "weight": 606.97,
    }
    STA_09_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_JS_1X_BRU_AGM-154C}",
        "name": " [ STA 09	  | SUU79 | BRU55   ] - 1x AGM-154C - JSOW Unitary BROACH",
        "weight": 605.97,
    }
    STA_09_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_JS_1X_BRU55_AGM-154C}",
        "name": " [ STA 09	  | SUU79 | BRU55   ] - 1x AGM-154C - JSOW Unitary BROACH",
        "weight": 605.97,
    }
    STA_09_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type_ = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_JS_2X_BRU_AGM-154A}",
        "name": " [ STA 09	  | SUU79 | BRU55   ] - 2x AGM-154A - JSOW CEB (CBU-type)",
        "weight": 1091.97,
    }
    STA_09_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_JS_2X_BRU_AGM-154C}",
        "name": " [ STA 09	  | SUU79 | BRU55   ] - 2x AGM-154C - JSOW Unitary BROACH",
        "weight": 1089.97,
    }
    STA_09_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_JS_2X_BRU55_AGM-154C}",
        "name": " [ STA 09	  | SUU79 | BRU55   ] - 2x AGM-154C - JSOW Unitary BROACH",
        "weight": 1089.97,
    }
    STA_09_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_MK_BR55_2X_GBU-32}",
        "name": " [ STA 09	  | SUU79 | BRU55   ] - 2x GBU-32(V)2/B - JDAM, 1000lb GPS Guided Bomb",
        "weight": 1055.97,
    }
    STA_09_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_BR55_2X_GBU-38}",
        "name": " [ STA 09	  | SUU79 | BRU55   ] - 2x GBU-38 - JDAM, 500lb GPS Guided Bomb",
        "weight": 603.97,
    }
    STA_09_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_MK_BR55_2X_GBU-38}",
        "name": " [ STA 09	  | SUU79 | BRU55   ] - 2x GBU-38 - JDAM, 500lb GPS Guided Bomb",
        "weight": 603.97,
    }
    STA_09_SUU79_EMPTY = {
        "clsid": "{SUPERHORNET_PYLON_09_EMPTY}",
        "name": " [ STA 09	  | SUU79 | EMPTY ]",
        "weight": 0,
    }
    STA_09_SUU79_LA118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = {
        "clsid": "{GROWLER_PYLON_10_MB_AR_1X_AGM-88}",
        "name": " [ STA 09	  | SUU79 | LA118 ] - 1x AGM-88C HARM - High Speed Anti-Radiation Missile",
        "weight": 440.87,
    }
    STA_09_SUU79_LA127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = {
        "clsid": "{GROWLER_PYLON_10_MB_AM_1X_AIM-120}",
        "name": " [ STA 09	  | SUU79 | LA127 ] - 1x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 337.32,
    }
    STA_09_SUU79_LA127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = {
        "clsid": "{GROWLER_PYLON_10_MB_AM_1X_AIM-120C}",
        "name": " [ STA 09	  | SUU79 | LA127 ] - 1x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 340.95,
    }
    STA_09_SUU79_LA127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = {
        "clsid": "{GROWLER_PYLON_10_MB_AM_1X_AIM-120D}",
        "name": " [ STA 09	  | SUU79 | LA127 ] - 1x AIM-120D AMRAAM - Active Radar AAM (AI Only)",
        "weight": 341.87,
    }
    STA_09_SUU79_LA127_1x_AIM_9M_Sidewinder_IR_AAM = {
        "clsid": "{GROWLER_PYLON_10_MB_SW_1X_AIM-9}",
        "name": " [ STA 09	  | SUU79 | LA127 ] - 1x AIM-9M Sidewinder IR AAM",
        "weight": 265.19,
    }
    STA_09_SUU79_LA127_1x_AIM_9X_Sidewinder_IR_AAM = {
        "clsid": "{GROWLER_PYLON_10_MB_SW_1X_AIM-9X}",
        "name": " [ STA 09	  | SUU79 | LA127 ] - 1x AIM-9X Sidewinder IR AAM",
        "weight": 263.93,
    }
    STA_09_SUU79_LA127_1x_Captive_AIM_9M_for_ACM = {
        "clsid": "{GROWLER_PYLON_10_MB_SW_1X_CATM-9M}",
        "name": " [ STA 09	  | SUU79 | LA127 ] - 1x Captive AIM-9M for ACM",
        "weight": 265.2,
    }
    STA_09_SUU79_LA127_2x_AIM_120B_AMRAAM___Active_Radar_AAM = {
        "clsid": "{GROWLER_PYLON_10_MB_AM_2X_AIM-120}",
        "name": " [ STA 09	  | SUU79 | LA127 ] - 2x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 495.17,
    }
    STA_09_SUU79_LA127_2x_AIM_120C_AMRAAM___Active_Radar_AAM = {
        "clsid": "{GROWLER_PYLON_10_MB_AM_2X_AIM-120C}",
        "name": " [ STA 09	  | SUU79 | LA127 ] - 2x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 502.43,
    }
    STA_09_SUU79_LA127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = {
        "clsid": "{GROWLER_PYLON_10_MB_AM_2X_AIM-120D}",
        "name": " [ STA 09	  | SUU79 | LA127 ] - 2x AIM-120D AMRAAM - Active Radar AAM (AI Only)",
        "weight": 504.27,
    }
    STA_09_SUU79_LA127_2x_AIM_9M_Sidewinder_IR_AAM = {
        "clsid": "{GROWLER_PYLON_10_MB_SW_2X_AIM-9}",
        "name": " [ STA 09	  | SUU79 | LA127 ] - 2x AIM-9M Sidewinder IR AAM",
        "weight": 350.91,
    }
    STA_09_SUU79_LA127_2x_AIM_9X_Sidewinder_IR_AAM = {
        "clsid": "{GROWLER_PYLON_10_MB_SW_2X_AIM-9X}",
        "name": " [ STA 09	  | SUU79 | LA127 ] - 2x AIM-9X Sidewinder IR AAM",
        "weight": 348.39,
    }
    STA_09_SUU79_LA127_2x_Captive_AIM_9M_for_ACM = {
        "clsid": "{GROWLER_PYLON_10_MB_SW_2X_CATM-9M}",
        "name": " [ STA 09	  | SUU79 | LA127 ] - 2x Captive AIM-9M for ACM",
        "weight": 350.93,
    }
    STA_09_SUU79_LAU115_1x_AIM_7F_Sparrow_Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_SP_1X_AIM-7F}",
        "name": " [ STA 09	  | SUU79 | LAU115 ] - 1x AIM-7F Sparrow Semi-Active Radar",
        "weight": 319.9,
    }
    STA_09_SUU79_LAU115_1x_AIM_7F_Sparrow_Semi_Active_Radar_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_SP_1X_AIM-7F}",
        "name": " [ STA 09	  | SUU79 | LAU115 ] - 1x AIM-7F Sparrow Semi-Active Radar",
        "weight": 319.9,
    }
    STA_09_SUU79_LAU115_1x_AIM_7MH_Sparrow_Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_SP_1X_AIM-7H}",
        "name": " [ STA 09	  | SUU79 | LAU115 ] - 1x AIM-7MH Sparrow Semi-Active Radar",
        "weight": 319.9,
    }
    STA_09_SUU79_LAU115_1x_AIM_7MH_Sparrow_Semi_Active_Radar_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_SP_1X_AIM-7H}",
        "name": " [ STA 09	  | SUU79 | LAU115 ] - 1x AIM-7MH Sparrow Semi-Active Radar",
        "weight": 319.9,
    }
    STA_09_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_SP_1X_AIM-7M}",
        "name": " [ STA 09	  | SUU79 | LAU115 ] - 1x AIM-7M Sparrow Semi-Active Radar",
        "weight": 319.9,
    }
    STA_09_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_SP_1X_AIM-7M}",
        "name": " [ STA 09	  | SUU79 | LAU115 ] - 1x AIM-7M Sparrow Semi-Active Radar",
        "weight": 319.9,
    }
    STA_09_SUU79_LAU115_1x_AIM_7P_Sparrow_Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_SP_1X_AIM-7P}",
        "name": " [ STA 09	  | SUU79 | LAU115 ] - 1x AIM-7P Sparrow Semi-Active Radar",
        "weight": 319.9,
    }
    STA_09_SUU79_LAU115_1x_AIM_7P_Sparrow_Semi_Active_Radar_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_SP_1X_AIM-7P}",
        "name": " [ STA 09	  | SUU79 | LAU115 ] - 1x AIM-7P Sparrow Semi-Active Radar",
        "weight": 319.9,
    }
    STA_09_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MV_1X_AGM-65E}",
        "name": " [ STA 09	  | SUU79 | LAU117 ] - 1x AGM-65E - Maverick E (Laser ASM - Lg Whd)",
        "weight": 379.47,
    }
    STA_09_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd__ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_MV_1X_AGM-65E}",
        "name": " [ STA 09	  | SUU79 | LAU117 ] - 1x AGM-65E - Maverick E (Laser ASM - Lg Whd)",
        "weight": 379.47,
    }
    STA_09_SUU79_LAU117_1x_AGM_65F___Maverick_F__IIR_ = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MV_1X_AGM-65F}",
        "name": " [ STA 09	  | SUU79 | LAU117 ] - 1x AGM-65F - Maverick F (IIR)",
        "weight": 394.47,
    }
    STA_09_SUU79_LAU117_1x_AGM_84D_Harpoon_Anti_Ship_Missile = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_SM_1X_AGM-84D}",
        "name": " [ STA 09	  | SUU79 | LAU117 ] - 1x AGM-84D Harpoon Anti-Ship Missile",
        "weight": 574.47,
    }
    STA_09_SUU79_LAU117_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_SM_1X_AGM-84E}",
        "name": " [ STA 09	  | SUU79 | LAU117 ] - 1x AGM-84E Harpoon/SLAM (Stand-Off Land-Attack Missile)",
        "weight": 662.47,
    }
    STA_09_SUU79_LAU117_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile__ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_SM_1X_AGM-84E}",
        "name": " [ STA 09	  | SUU79 | LAU117 ] - 1x AGM-84E Harpoon/SLAM (Stand-Off Land-Attack Missile)",
        "weight": 662.47,
    }
    STA_09_SUU79_LAU117_1x_AGM_84H_SLAM_ER__Expanded_Response_ = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_SM_1X_AGM-84H}",
        "name": " [ STA 09	  | SUU79 | LAU117 ] - 1x AGM-84H SLAM-ER (Expanded Response)",
        "weight": 709.47,
    }
    STA_09_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MV_1X_CATM-65K}",
        "name": " [ STA 09	  | SUU79 | LAU117 ] - 1x CATM-65K - Captive Trg Round for Mav K (CCD), AI Only",
        "weight": 390.47,
    }
    STA_09_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_MV_1X_CATM-65K}",
        "name": " [ STA 09	  | SUU79 | LAU117 ] - 1x CATM-65K - Captive Trg Round for Mav K (CCD), AI Only",
        "weight": 390.47,
    }
    STA_09_SUU79_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_AR_1X_AGM-88}",
        "name": " [ STA 09	  | SUU79 | LAU118 ] - 1x AGM-88C HARM - High Speed Anti-Radiation Missile",
        "weight": 440.87,
    }
    STA_09_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_AM_1X_AIM-120}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 1x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 337.35,
    }
    STA_09_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_AM_1X_AIM-120}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 1x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 337.35,
    }
    STA_09_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_AM_1X_AIM-120C}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 1x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 340.98,
    }
    STA_09_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_AM_1X_AIM-120C}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 1x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 340.98,
    }
    STA_09_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_AM_1X_AIM-120D}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 1x AIM-120D AMRAAM - Active Radar AAM (AI Only)",
        "weight": 341.9,
    }
    STA_09_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only__ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_AM_1X_AIM-120D}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 1x AIM-120D AMRAAM - Active Radar AAM (AI Only)",
        "weight": 341.9,
    }
    STA_09_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_SW_1X_AIM-9}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 1x AIM-9M Sidewinder IR AAM",
        "weight": 265.22,
    }
    STA_09_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_SW_1X_AIM-9}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 1x AIM-9M Sidewinder IR AAM",
        "weight": 265.22,
    }
    STA_09_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_SW_1X_AIM-9X}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 1x AIM-9X Sidewinder IR AAM",
        "weight": 263.96,
    }
    STA_09_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_SW_1X_AIM-9X}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 1x AIM-9X Sidewinder IR AAM",
        "weight": 263.96,
    }
    STA_09_SUU79_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_PD_1X_ais-pod-t50}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 1x AN/ASQ-T50(V)1 TCTS Pod",
        "weight": 107.9,
    }
    STA_09_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_SW_1X_CATM-9M}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 1x Captive AIM-9M for ACM",
        "weight": 265.23,
    }
    STA_09_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_SW_1X_CATM-9M}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 1x Captive AIM-9M for ACM",
        "weight": 265.23,
    }
    STA_09_SUU79_LAU127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X = {
        "clsid": "{SUPERHORNET_PYLON_09_LAU127}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 1x Marvin LAU-127 Rail Launcher for AIM-120B/C/D and AIM9L/M/X",
        "weight": 0,
    }
    STA_09_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_AM_2X_AIM-120}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 2x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 495.2,
    }
    STA_09_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_AM_2X_AIM-120}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 2x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 495.2,
    }
    STA_09_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_AM_2X_AIM-120C}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 2x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 502.46,
    }
    STA_09_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_AM_2X_AIM-120C}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 2x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 502.46,
    }
    STA_09_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_AM_2X_AIM-120D}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 2x AIM-120D AMRAAM - Active Radar AAM (AI Only)",
        "weight": 504.3,
    }
    STA_09_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only__ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_AM_2X_AIM-120D}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 2x AIM-120D AMRAAM - Active Radar AAM (AI Only)",
        "weight": 504.3,
    }
    STA_09_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_SW_2X_AIM-9}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 2x AIM-9M Sidewinder IR AAM",
        "weight": 350.94,
    }
    STA_09_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_SW_2X_AIM-9}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 2x AIM-9M Sidewinder IR AAM",
        "weight": 350.94,
    }
    STA_09_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_SW_2X_AIM-9X}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 2x AIM-9X Sidewinder IR AAM",
        "weight": 348.42,
    }
    STA_09_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_SW_2X_AIM-9X}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 2x AIM-9X Sidewinder IR AAM",
        "weight": 348.42,
    }
    STA_09_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_SW_2X_CATM-9M}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 2x Captive AIM-9M for ACM",
        "weight": 350.96,
    }
    STA_09_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_SW_2X_CATM-9M}",
        "name": " [ STA 09	  | SUU79 | LAU127 ] - 2x Captive AIM-9M for ACM",
        "weight": 350.96,
    }
    STA_09_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_1X_BDU-45B}",
        "name": " [ STA 09	  | SUU80 | BRU32   ] - 1x BDU-45B - 500lb Practice Bomb",
        "weight": 266.47,
    }
    STA_09_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_1X_BDU-45}",
        "name": " [ STA 09	  | SUU80 | BRU32   ] - 1x BDU-45 - 500lb Practice Bomb",
        "weight": 266.47,
    }
    STA_09_SUU80_BRU32_1x_CBU_99___490lbs__247_x_HEAT_Bomblets = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_1X_CBU-99}",
        "name": " [ STA 09	  | SUU80 | BRU32   ] - 1x CBU-99 - 490lbs, 247 x HEAT Bomblets",
        "weight": 56.47,
    }
    STA_09_SUU80_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_1X_GBU-10}",
        "name": " [ STA 09	  | SUU80 | BRU32   ] - 1x GBU-10 - 2000lb Laser Guided Bomb",
        "weight": 946.47,
    }
    STA_09_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_1X_GBU-12}",
        "name": " [ STA 09	  | SUU80 | BRU32   ] - 1x GBU-12 - 500lb Laser Guided Bomb",
        "weight": 311.47,
    }
    STA_09_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_1X_GBU-16}",
        "name": " [ STA 09	  | SUU80 | BRU32   ] - 1x GBU-16 - 1000lb Laser Guided Bomb",
        "weight": 547.47,
    }
    STA_09_SUU80_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_1X_GBU-24}",
        "name": " [ STA 09	  | SUU80 | BRU32   ] - 1x GBU-24A/B Paveway III - 2000lb Laser Guided Bomb",
        "weight": 968.47,
    }
    STA_09_SUU80_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_1X_GBU-31}",
        "name": " [ STA 09	  | SUU80 | BRU32   ] - 1x GBU-31(V)1/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 968.47,
    }
    STA_09_SUU80_BRU32_1x_GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_1X_GBU-31_V_2B}",
        "name": " [ STA 09	  | SUU80 | BRU32   ] - 1x GBU-31(V)2/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 968.47,
    }
    STA_09_SUU80_BRU32_1x_GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_1X_GBU-31_V_4B}",
        "name": " [ STA 09	  | SUU80 | BRU32   ] - 1x GBU-31(V)4/B - JDAM, 2000lb GPS Guided Penetrator Bomb",
        "weight": 1004.47,
    }
    STA_09_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_1X_GBU-32}",
        "name": " [ STA 09	  | SUU80 | BRU32   ] - 1x GBU-32(V)2/B - JDAM, 1000lb GPS Guided Bomb",
        "weight": 501.47,
    }
    STA_09_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_1X_GBU-38}",
        "name": " [ STA 09	  | SUU80 | BRU32   ] - 1x GBU-38 - JDAM, 500lb GPS Guided Bomb",
        "weight": 275.47,
    }
    STA_09_SUU80_BRU32_1x_GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_1X_GBU_54V}",
        "name": " [ STA 09	  | SUU80 | BRU32   ] - 1x GBU-54(V)1/B - LJDAM, 500lb Laser & GPS Guided Bomb LD",
        "weight": 287.47,
    }
    STA_09_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_1X_ROCKEYE}",
        "name": " [ STA 09	  | SUU80 | BRU32   ] - 1x Mk-20 Rockeye - 490lbs CBU, 247 x HEAT Bomblets",
        "weight": 256.47,
    }
    STA_09_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_1X_MK-82Y}",
        "name": " [ STA 09	  | SUU80 | BRU32   ] - 1x Mk-82Y - 500lb GP Chute Retarded HD",
        "weight": 266.47,
    }
    STA_09_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_1X_MK-82_Snakeye}",
        "name": " [ STA 09	  | SUU80 | BRU32   ] - 1x Mk-82 Snakeye - 500lb GP Bomb HD",
        "weight": 283.97,
    }
    STA_09_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_1X_MK-82}",
        "name": " [ STA 09	  | SUU80 | BRU32   ] - 1x Mk-82 - 500lb GP Bomb LD",
        "weight": 262.47,
    }
    STA_09_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_1X_MK-83}",
        "name": " [ STA 09	  | SUU80 | BRU32   ] - 1x Mk-83 - 1000lb GP Bomb LD",
        "weight": 488.47,
    }
    STA_09_SUU80_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_09_MB_MK_1X_MK-84}",
        "name": " [ STA 09	  | SUU80 | BRU32   ] - 1x Mk-84 - 2000lb GP Bomb LD",
        "weight": 946.47,
    }
    STA_09_SUU80_LA127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X = {
        "clsid": "{GROWLER_PYLON_09_IB_LAU127}",
        "name": " [ STA 09	  | SUU80 | LA127 ] - 1x Marvin LAU-127 Rail Launcher for AIM-120B/C/D and AIM9L/M/X",
        "weight": 52.1,
    }
    STA_09_08_SUU79_BRU32_1x_1x_BDU_45B___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MB_MK_BDU-45B}",
        "name": " [ STA 09/08 | SUU79 | BRU32   ] - 1x/1x BDU-45B - 500lb Practice Bomb",
        "weight": 532.94,
    }
    STA_09_08_SUU79_BRU32_1x_1x_BDU_45___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MB_MK_BDU-45}",
        "name": " [ STA 09/08 | SUU79 | BRU32   ] - 1x/1x BDU-45 - 500lb Practice Bomb",
        "weight": 532.94,
    }
    STA_09_08_SUU79_BRU32_1x_1x_CBU_99___490lbs__247_x_HEAT_Bomblets = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MB_MK_CBU-99}",
        "name": " [ STA 09/08 | SUU79 | BRU32   ] - 1x/1x CBU-99 - 490lbs, 247 x HEAT Bomblets",
        "weight": 112.94,
    }
    STA_09_08_SUU79_BRU32_1x_1x_GBU_10___2000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MB_MK_GBU-10}",
        "name": " [ STA 09/08 | SUU79 | BRU32   ] - 1x/1x GBU-10 - 2000lb Laser Guided Bomb",
        "weight": 1892.94,
    }
    STA_09_08_SUU79_BRU32_1x_1x_GBU_12___500lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MB_MK_GBU-12}",
        "name": " [ STA 09/08 | SUU79 | BRU32   ] - 1x/1x GBU-12 - 500lb Laser Guided Bomb",
        "weight": 622.94,
    }
    STA_09_08_SUU79_BRU32_1x_1x_GBU_16___1000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MB_MK_GBU-16}",
        "name": " [ STA 09/08 | SUU79 | BRU32   ] - 1x/1x GBU-16 - 1000lb Laser Guided Bomb",
        "weight": 1094.94,
    }
    STA_09_08_SUU79_BRU32_1x_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MB_MK_GBU-24}",
        "name": " [ STA 09/08 | SUU79 | BRU32   ] - 1x/1x GBU-24A/B Paveway III - 2000lb Laser Guided Bomb",
        "weight": 1936.94,
    }
    STA_09_08_SUU79_BRU32_1x_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MB_MK_GBU-31}",
        "name": " [ STA 09/08 | SUU79 | BRU32   ] - 1x/1x GBU-31(V)1/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 1936.94,
    }
    STA_09_08_SUU79_BRU32_1x_1x_GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MB_MK_GBU-31_V_2B}",
        "name": " [ STA 09/08 | SUU79 | BRU32   ] - 1x/1x GBU-31(V)2/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 1936.94,
    }
    STA_09_08_SUU79_BRU32_1x_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MB_MK_GBU-31V}",
        "name": " [ STA 09/08 | SUU79 | BRU32   ] - 1x/1x GBU-31(V)3/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 2030.94,
    }
    STA_09_08_SUU79_BRU32_1x_1x_GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MB_MK_GBU-31_V_4B}",
        "name": " [ STA 09/08 | SUU79 | BRU32   ] - 1x/1x GBU-31(V)4/B - JDAM, 2000lb GPS Guided Penetrator Bomb",
        "weight": 2008.94,
    }
    STA_09_08_SUU79_BRU32_1x_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MB_MK_GBU-38}",
        "name": " [ STA 09/08 | SUU79 | BRU32   ] - 1x/1x GBU-38 - JDAM, 500lb GPS Guided Bomb",
        "weight": 550.94,
    }
    STA_09_08_SUU79_BRU32_1x_1x_GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MB_MK_GBU_54V}",
        "name": " [ STA 09/08 | SUU79 | BRU32   ] - 1x/1x GBU-54(V)1/B - LJDAM, 500lb Laser & GPS Guided Bomb LD",
        "weight": 574.94,
    }
    STA_09_08_SUU79_BRU32_1x_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MB_MK_ROCKEYE}",
        "name": " [ STA 09/08 | SUU79 | BRU32   ] - 1x/1x Mk-20 Rockeye - 490lbs CBU, 247 x HEAT Bomblets",
        "weight": 512.94,
    }
    STA_09_08_SUU79_BRU32_1x_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MB_MK_MK-82Y}",
        "name": " [ STA 09/08 | SUU79 | BRU32   ] - 1x/1x Mk-82Y - 500lb GP Chute Retarded HD",
        "weight": 532.94,
    }
    STA_09_08_SUU79_BRU32_1x_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MB_MK_MK-82_Snakeye}",
        "name": " [ STA 09/08 | SUU79 | BRU32   ] - 1x/1x Mk-82 Snakeye - 500lb GP Bomb HD",
        "weight": 567.94,
    }
    STA_09_08_SUU79_BRU32_1x_1x_Mk_82___500lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MB_MK_MK-82}",
        "name": " [ STA 09/08 | SUU79 | BRU32   ] - 1x/1x Mk-82 - 500lb GP Bomb LD",
        "weight": 524.94,
    }
    STA_09_08_SUU79_BRU32_1x_1x_Mk_83___1000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MB_MK_MK-83}",
        "name": " [ STA 09/08 | SUU79 | BRU32   ] - 1x/1x Mk-83 - 1000lb GP Bomb LD",
        "weight": 976.94,
    }
    STA_09_08_SUU79_BRU32_1x_1x_Mk_84___2000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_09_IB_MB_MK_MK-84}",
        "name": " [ STA 09/08 | SUU79 | BRU32   ] - 1x/1x Mk-84 - 2000lb GP Bomb LD",
        "weight": 1892.94,
    }
    STA_09_10_79_80_BRU32_2x_GBU_10___2000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MB_MK_2X_GBU-10}",
        "name": " [ STA 09/10 | 79/80 | BRU32   ] - 2x GBU-10 - 2000lb Laser Guided Bomb",
        "weight": 1892.94,
    }
    STA_09_10_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MB_MK_2X_GBU-12}",
        "name": " [ STA 09/10 | 79/80 | BRU32   ] - 2x GBU-12 - 500lb Laser Guided Bomb",
        "weight": 622.94,
    }
    STA_09_10_79_80_BRU32_2x_GBU_16___1000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MB_MK_2X_GBU-16}",
        "name": " [ STA 09/10 | 79/80 | BRU32   ] - 2x GBU-16 - 1000lb Laser Guided Bomb",
        "weight": 1094.94,
    }
    STA_09_10_79_80_BRU32_2x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MB_MK_2X_GBU-24}",
        "name": " [ STA 09/10 | 79/80 | BRU32   ] - 2x GBU-24A/B Paveway III - 2000lb Laser Guided Bomb",
        "weight": 1936.94,
    }
    STA_09_10_79_80_BRU32_2x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MB_MK_2X_GBU-31}",
        "name": " [ STA 09/10 | 79/80 | BRU32   ] - 2x GBU-31(V)1/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 1936.94,
    }
    STA_09_10_79_80_BRU32_2x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MB_MK_2X_GBU-31V}",
        "name": " [ STA 09/10 | 79/80 | BRU32   ] - 2x GBU-31(V)3/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 2030.94,
    }
    STA_09_10_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MB_MK_2X_GBU-38}",
        "name": " [ STA 09/10 | 79/80 | BRU32   ] - 2x GBU-38 - JDAM, 500lb GPS Guided Bomb",
        "weight": 550.94,
    }
    STA_09_10_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MB_MK_2X_ROCKEYE}",
        "name": " [ STA 09/10 | 79/80 | BRU32   ] - 2x Mk-20 Rockeye - 490lbs CBU, 247 x HEAT Bomblets",
        "weight": 512.94,
    }
    STA_09_10_79_80_BRU32_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MB_MK_2X_MK-82Y}",
        "name": " [ STA 09/10 | 79/80 | BRU32   ] - 2x Mk-82Y - 500lb GP Chute Retarded HD",
        "weight": 532.94,
    }
    STA_09_10_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MB_MK_2X_MK-82_Snakeye}",
        "name": " [ STA 09/10 | 79/80 | BRU32   ] - 2x Mk-82 Snakeye - 500lb GP Bomb HD",
        "weight": 567.94,
    }
    STA_09_10_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MB_MK_2X_MK-82}",
        "name": " [ STA 09/10 | 79/80 | BRU32   ] - 2x Mk-82 - 500lb GP Bomb LD",
        "weight": 524.94,
    }
    STA_09_10_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MB_MK_2X_MK-83}",
        "name": " [ STA 09/10 | 79/80 | BRU32   ] - 2x Mk-83 - 1000lb GP Bomb LD",
        "weight": 976.94,
    }
    STA_09_10_79_80_BRU32_2x_Mk_84___2000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MB_MK_2X_MK-84}",
        "name": " [ STA 09/10 | 79/80 | BRU32   ] - 2x Mk-84 - 2000lb GP Bomb LD",
        "weight": 1892.94,
    }
    STA_09_10_79_80_LAU127_1x_1x_AIM_120B_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_OB_AM_2X_AIM-120}",
        "name": " [ STA 09/10 | 79/80 | LAU127 ] - 1x/1x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 547.3,
    }
    STA_09_10_79_80_LAU127_1x_1x_AIM_120C_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_OB_AM_2X_AIM-120C}",
        "name": " [ STA 09/10 | 79/80 | LAU127 ] - 1x/1x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 554.56,
    }
    STA_09_10_79_80_LAU127_1x_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_OB_AM_2X_AIM-120D}",
        "name": " [ STA 09/10 | 79/80 | LAU127 ] - 1x/1x AIM-120D AMRAAM - Active Radar AAM (AI Only)",
        "weight": 556.4,
    }
    STA_09_10_79_80_LAU127_1x_1x_AIM_9M_Sidewinder_IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_OB_SW_2X_AIM-9}",
        "name": " [ STA 09/10 | 79/80 | LAU127 ] - 1x/1x AIM-9M Sidewinder IR AAM",
        "weight": 403.04,
    }
    STA_09_10_79_80_LAU127_1x_1x_AIM_9X_Sidewinder_IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_10_MB_OB_SW_2X_AIM-9X}",
        "name": " [ STA 09/10 | 79/80 | LAU127 ] - 1x/1x AIM-9X Sidewinder IR AAM",
        "weight": 400.52,
    }
    STA_10_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MK_1X_BDU-45B}",
        "name": " [ STA 10	  | SUU80 | BRU32   ] - 1x BDU-45B - 500lb Practice Bomb",
        "weight": 266.47,
    }
    STA_10_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MK_1X_BDU-45}",
        "name": " [ STA 10	  | SUU80 | BRU32   ] - 1x BDU-45 - 500lb Practice Bomb",
        "weight": 266.47,
    }
    STA_10_SUU80_BRU32_1x_CBU_99___490lbs__247_x_HEAT_Bomblets = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MK_1X_CBU-99}",
        "name": " [ STA 10	  | SUU80 | BRU32   ] - 1x CBU-99 - 490lbs, 247 x HEAT Bomblets",
        "weight": 56.47,
    }
    STA_10_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MK_1X_GBU-12}",
        "name": " [ STA 10	  | SUU80 | BRU32   ] - 1x GBU-12 - 500lb Laser Guided Bomb",
        "weight": 311.47,
    }
    STA_10_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MK_1X_GBU-16}",
        "name": " [ STA 10	  | SUU80 | BRU32   ] - 1x GBU-16 - 1000lb Laser Guided Bomb",
        "weight": 547.47,
    }
    STA_10_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MK_1X_GBU-32}",
        "name": " [ STA 10	  | SUU80 | BRU32   ] - 1x GBU-32(V)2/B - JDAM, 1000lb GPS Guided Bomb",
        "weight": 501.47,
    }
    STA_10_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MK_1X_GBU-38}",
        "name": " [ STA 10	  | SUU80 | BRU32   ] - 1x GBU-38 - JDAM, 500lb GPS Guided Bomb",
        "weight": 275.47,
    }
    STA_10_SUU80_BRU32_1x_GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MK_1X_GBU_54V}",
        "name": " [ STA 10	  | SUU80 | BRU32   ] - 1x GBU-54(V)1/B - LJDAM, 500lb Laser & GPS Guided Bomb LD",
        "weight": 287.47,
    }
    STA_10_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MK_1X_ROCKEYE}",
        "name": " [ STA 10	  | SUU80 | BRU32   ] - 1x Mk-20 Rockeye - 490lbs CBU, 247 x HEAT Bomblets",
        "weight": 256.47,
    }
    STA_10_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MK_1X_MK-82Y}",
        "name": " [ STA 10	  | SUU80 | BRU32   ] - 1x Mk-82Y - 500lb GP Chute Retarded HD",
        "weight": 266.47,
    }
    STA_10_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MK_1X_MK-82_Snakeye}",
        "name": " [ STA 10	  | SUU80 | BRU32   ] - 1x Mk-82 Snakeye - 500lb GP Bomb HD",
        "weight": 283.97,
    }
    STA_10_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MK_1X_MK-82}",
        "name": " [ STA 10	  | SUU80 | BRU32   ] - 1x Mk-82 - 500lb GP Bomb LD",
        "weight": 262.47,
    }
    STA_10_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MK_1X_MK-83}",
        "name": " [ STA 10	  | SUU80 | BRU32   ] - 1x Mk-83 - 1000lb GP Bomb LD",
        "weight": 488.47,
    }
    STA_10_SUU80_EMPTY = {
        "clsid": "{SUPERHORNET_PYLON_10_EMPTY}",
        "name": " [ STA 10	  | SUU80 | EMPTY ]",
        "weight": 0,
    }
    STA_10_SUU80_LA115_1x_AIM_7F_Sparrow_Semi_Active_Radar = {
        "clsid": "{GROWLER_PYLON_10_SP_1X_AIM-7F}",
        "name": " [ STA 10	  | SUU80 | LA115 ] - 1x AIM-7F Sparrow Semi-Active Radar",
        "weight": 319.87,
    }
    STA_10_SUU80_LA115_1x_AIM_7MH_Sparrow_Semi_Active_Radar = {
        "clsid": "{GROWLER_PYLON_10_SP_1X_AIM-7H}",
        "name": " [ STA 10	  | SUU80 | LA115 ] - 1x AIM-7MH Sparrow Semi-Active Radar",
        "weight": 319.87,
    }
    STA_10_SUU80_LA115_1x_AIM_7M_Sparrow_Semi_Active_Radar = {
        "clsid": "{GROWLER_PYLON_10_SP_1X_AIM-7M}",
        "name": " [ STA 10	  | SUU80 | LA115 ] - 1x AIM-7M Sparrow Semi-Active Radar",
        "weight": 319.87,
    }
    STA_10_SUU80_LA115_1x_AIM_7P_Sparrow_Semi_Active_Radar = {
        "clsid": "{GROWLER_PYLON_10_SP_1X_AIM-7P}",
        "name": " [ STA 10	  | SUU80 | LA115 ] - 1x AIM-7P Sparrow Semi-Active Radar",
        "weight": 319.87,
    }
    STA_10_SUU80_LA118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = {
        "clsid": "{GROWLER_PYLON_10_OB_AR_1X_AGM-88}",
        "name": " [ STA 10	  | SUU80 | LA118 ] - 1x AGM-88C HARM - High Speed Anti-Radiation Missile",
        "weight": 440.87,
    }
    STA_10_SUU80_LA127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = {
        "clsid": "{GROWLER_PYLON_10_OB_AM_1X_AIM-120}",
        "name": " [ STA 10	  | SUU80 | LA127 ] - 1x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 337.32,
    }
    STA_10_SUU80_LA127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = {
        "clsid": "{GROWLER_PYLON_10_OB_AM_1X_AIM-120C}",
        "name": " [ STA 10	  | SUU80 | LA127 ] - 1x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 340.95,
    }
    STA_10_SUU80_LA127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = {
        "clsid": "{GROWLER_PYLON_10_OB_AM_1X_AIM-120D}",
        "name": " [ STA 10	  | SUU80 | LA127 ] - 1x AIM-120D AMRAAM - Active Radar AAM (AI Only)",
        "weight": 341.87,
    }
    STA_10_SUU80_LA127_1x_AIM_9M_Sidewinder_IR_AAM = {
        "clsid": "{GROWLER_PYLON_09_OB_SW_1X_AIM-9}",
        "name": " [ STA 10	  | SUU80 | LA127 ] - 1x AIM-9M Sidewinder IR AAM",
        "weight": 137.82,
    }
    STA_10_SUU80_LA127_1x_AIM_9M_Sidewinder_IR_AAM_ = {
        "clsid": "{GROWLER_PYLON_10_OB_SW_1X_AIM-9}",
        "name": " [ STA 10	  | SUU80 | LA127 ] - 1x AIM-9M Sidewinder IR AAM",
        "weight": 265.19,
    }
    STA_10_SUU80_LA127_1x_AIM_9X_Sidewinder_IR_AAM = {
        "clsid": "{GROWLER_PYLON_09_OB_SW_1X_AIM-9X}",
        "name": " [ STA 10	  | SUU80 | LA127 ] - 1x AIM-9X Sidewinder IR AAM",
        "weight": 136.56,
    }
    STA_10_SUU80_LA127_1x_AIM_9X_Sidewinder_IR_AAM_ = {
        "clsid": "{GROWLER_PYLON_10_OB_SW_1X_AIM-9X}",
        "name": " [ STA 10	  | SUU80 | LA127 ] - 1x AIM-9X Sidewinder IR AAM",
        "weight": 263.93,
    }
    STA_10_SUU80_LA127_1x_AN_ASQ_T50_V_1_TCTS_Pod = {
        "clsid": "{GROWLER_PYLON_10_PD_ais-pod-t50}",
        "name": " [ STA 10	  | SUU80 | LA127 ] - 1x AN/ASQ-T50(V)1 TCTS Pod",
        "weight": 114.7,
    }
    STA_10_SUU80_LA127_1x_Captive_AIM_9M_for_ACM = {
        "clsid": "{GROWLER_PYLON_10_OB_SW_1X_C}",
        "name": " [ STA 10	  | SUU80 | LA127 ] - 1x Captive AIM-9M for ACM",
        "weight": 265.2,
    }
    STA_10_SUU80_LA127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X = {
        "clsid": "{GROWLER_PYLON_09_OB_LAU127}",
        "name": " [ STA 10	  | SUU80 | LA127 ] - 1x Marvin LAU-127 Rail Launcher for AIM-120B/C/D and AIM9L/M/X",
        "weight": 52.1,
    }
    STA_10_SUU80_LA127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X_ = {
        "clsid": "{GROWLER_PYLON_10_LAU127}",
        "name": " [ STA 10	  | SUU80 | LA127 ] - 1x Marvin LAU-127 Rail Launcher for AIM-120B/C/D and AIM9L/M/X",
        "weight": 52.1,
    }
    STA_10_SUU80_LAU115_1x_AIM_7F_Sparrow_Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_10_SP_1X_AIM-7F}",
        "name": " [ STA 10	  | SUU80 | LAU115 ] - 1x AIM-7F Sparrow Semi-Active Radar",
        "weight": 319.9,
    }
    STA_10_SUU80_LAU115_1x_AIM_7MH_Sparrow_Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_10_SP_1X_AIM-7H}",
        "name": " [ STA 10	  | SUU80 | LAU115 ] - 1x AIM-7MH Sparrow Semi-Active Radar",
        "weight": 319.9,
    }
    STA_10_SUU80_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_10_SP_1X_AIM-7M}",
        "name": " [ STA 10	  | SUU80 | LAU115 ] - 1x AIM-7M Sparrow Semi-Active Radar",
        "weight": 319.9,
    }
    STA_10_SUU80_LAU115_1x_AIM_7P_Sparrow_Semi_Active_Radar = {
        "clsid": "{SUPERHORNET_PYLON_10_SP_1X_AIM-7P}",
        "name": " [ STA 10	  | SUU80 | LAU115 ] - 1x AIM-7P Sparrow Semi-Active Radar",
        "weight": 319.9,
    }
    STA_10_SUU80_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MV_1X_AGM-65E}",
        "name": " [ STA 10	  | SUU80 | LAU117 ] - 1x AGM-65E - Maverick E (Laser ASM - Lg Whd)",
        "weight": 379.47,
    }
    STA_10_SUU80_LAU117_1x_AGM_65F___Maverick_F__IIR_ = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MV_1X_AGM-65F}",
        "name": " [ STA 10	  | SUU80 | LAU117 ] - 1x AGM-65F - Maverick F (IIR)",
        "weight": 394.47,
    }
    STA_10_SUU80_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_MV_1X_CATM-65K}",
        "name": " [ STA 10	  | SUU80 | LAU117 ] - 1x CATM-65K - Captive Trg Round for Mav K (CCD), AI Only",
        "weight": 390.47,
    }
    STA_10_SUU80_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_AR_1X_AGM-88}",
        "name": " [ STA 10	  | SUU80 | LAU118 ] - 1x AGM-88C HARM - High Speed Anti-Radiation Missile",
        "weight": 440.87,
    }
    STA_10_SUU80_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_10_AM_1X_AIM-120}",
        "name": " [ STA 10	  | SUU80 | LAU127 ] - 1x AIM-120B AMRAAM - Active Radar AAM",
        "weight": 209.95,
    }
    STA_10_SUU80_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = {
        "clsid": "{SUPERHORNET_PYLON_10_AM_1X_AIM-120C}",
        "name": " [ STA 10	  | SUU80 | LAU127 ] - 1x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 213.58,
    }
    STA_10_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = {
        "clsid": "{SUPERHORNET_PYLON_10_AM_1X_AIM-120D}",
        "name": " [ STA 10	  | SUU80 | LAU127 ] - 1x AIM-120D AMRAAM - Active Radar AAM (AI Only)",
        "weight": 214.5,
    }
    STA_10_SUU80_LAU127_1x_AIM_9M_Sidewinder_IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_10_SW_1X_AIM-9}",
        "name": " [ STA 10	  | SUU80 | LAU127 ] - 1x AIM-9M Sidewinder IR AAM",
        "weight": 137.82,
    }
    STA_10_SUU80_LAU127_1x_AIM_9X_Sidewinder_IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_10_SW_1X_AIM-9X}",
        "name": " [ STA 10	  | SUU80 | LAU127 ] - 1x AIM-9X Sidewinder IR AAM",
        "weight": 136.56,
    }
    STA_10_SUU80_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod = {
        "clsid": "{SUPERHORNET_PYLON_10_PD_1X_ais-pod-t50}",
        "name": " [ STA 10	  | SUU80 | LAU127 ] - 1x AN/ASQ-T50(V)1 TCTS Pod",
        "weight": 107.9,
    }
    STA_10_SUU80_LAU127_1x_Captive_AIM_9M_for_ACM = {
        "clsid": "{SUPERHORNET_PYLON_10_SW_1X_CATM-9M}",
        "name": " [ STA 10	  | SUU80 | LAU127 ] - 1x Captive AIM-9M for ACM",
        "weight": 137.83,
    }
    STA_10_SUU80_LAU127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X = {
        "clsid": "{SUPERHORNET_PYLON_10_LAU127}",
        "name": " [ STA 10	  | SUU80 | LAU127 ] - 1x Marvin LAU-127 Rail Launcher for AIM-120B/C/D and AIM9L/M/X",
        "weight": 52.1,
    }
    STA_10_08_79_80_BRU32_2x_GBU_10___2000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_IB_MK_2X_GBU-10}",
        "name": " [ STA 10/08 | 79/80 | BRU32   ] - 2x GBU-10 - 2000lb Laser Guided Bomb",
        "weight": 1892.94,
    }
    STA_10_08_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_IB_MK_2X_GBU-12}",
        "name": " [ STA 10/08 | 79/80 | BRU32   ] - 2x GBU-12 - 500lb Laser Guided Bomb",
        "weight": 622.94,
    }
    STA_10_08_79_80_BRU32_2x_GBU_16___1000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_IB_MK_2X_GBU-16}",
        "name": " [ STA 10/08 | 79/80 | BRU32   ] - 2x GBU-16 - 1000lb Laser Guided Bomb",
        "weight": 1094.94,
    }
    STA_10_08_79_80_BRU32_2x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_IB_MK_2X_GBU-24}",
        "name": " [ STA 10/08 | 79/80 | BRU32   ] - 2x GBU-24A/B Paveway III - 2000lb Laser Guided Bomb",
        "weight": 1936.94,
    }
    STA_10_08_79_80_BRU32_2x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_IB_MK_2X_GBU-31}",
        "name": " [ STA 10/08 | 79/80 | BRU32   ] - 2x GBU-31(V)1/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 1936.94,
    }
    STA_10_08_79_80_BRU32_2x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_IB_MK_2X_GBU-31V}",
        "name": " [ STA 10/08 | 79/80 | BRU32   ] - 2x GBU-31(V)3/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 2030.94,
    }
    STA_10_08_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_IB_MK_2X_GBU-38}",
        "name": " [ STA 10/08 | 79/80 | BRU32   ] - 2x GBU-38 - JDAM, 500lb GPS Guided Bomb",
        "weight": 550.94,
    }
    STA_10_08_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_IB_MK_2X_ROCKEYE}",
        "name": " [ STA 10/08 | 79/80 | BRU32   ] - 2x Mk-20 Rockeye - 490lbs CBU, 247 x HEAT Bomblets",
        "weight": 512.94,
    }
    STA_10_08_79_80_BRU32_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_IB_MK_2X_MK-82Y}",
        "name": " [ STA 10/08 | 79/80 | BRU32   ] - 2x Mk-82Y - 500lb GP Chute Retarded HD",
        "weight": 532.94,
    }
    STA_10_08_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_IB_MK_2X_MK-82_Snakeye}",
        "name": " [ STA 10/08 | 79/80 | BRU32   ] - 2x Mk-82 Snakeye - 500lb GP Bomb HD",
        "weight": 567.94,
    }
    STA_10_08_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_IB_MK_2X_MK-82}",
        "name": " [ STA 10/08 | 79/80 | BRU32   ] - 2x Mk-82 - 500lb GP Bomb LD",
        "weight": 524.94,
    }
    STA_10_08_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_IB_MK_2X_MK-83}",
        "name": " [ STA 10/08 | 79/80 | BRU32   ] - 2x Mk-83 - 1000lb GP Bomb LD",
        "weight": 976.94,
    }
    STA_10_08_79_80_BRU32_2x_Mk_84___2000lb_GP_Bomb_LD = {
        "clsid": "{SUPERHORNET_PYLON_10_OB_IB_MK_2X_MK-84}",
        "name": " [ STA 10/08 | 79/80 | BRU32   ] - 2x Mk-84 - 2000lb GP Bomb LD",
        "weight": 1892.94,
    }
    STA_11_WNGTP_LAU127_1x_AIM_9M_Sidewinder_IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_11_SW_1X_AIM-9}",
        "name": " [ STA 11	  | WNGTP | LAU127 ] - 1x AIM-9M Sidewinder IR AAM",
        "weight": 85.72,
    }
    STA_11_WNGTP_LAU127_1x_AIM_9X_Sidewinder_IR_AAM = {
        "clsid": "{SUPERHORNET_PYLON_11_SW_1X_AIM-9X}",
        "name": " [ STA 11	  | WNGTP | LAU127 ] - 1x AIM-9X Sidewinder IR AAM",
        "weight": 84.46,
    }
    STA_11_WNGTP_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod = {
        "clsid": "{SUPERHORNET_PYLON_11_PD_1X_ais-pod-t50}",
        "name": " [ STA 11	  | WNGTP | LAU127 ] - 1x AN/ASQ-T50(V)1 TCTS Pod",
        "weight": 62.6,
    }
    STA_11_WNGTP_LAU127_1x_Captive_AIM_9M_for_ACM = {
        "clsid": "{SUPERHORNET_PYLON_11_SW_1X_CATM-9M}",
        "name": " [ STA 11	  | WNGTP | LAU127 ] - 1x Captive AIM-9M for ACM",
        "weight": 85.73,
    }
    STA_AX_AUX_PILOT_1x_Hood_Displayed_Folded_Flag = {
        "clsid": "{SUPERHORNET_PYLON_06_CN_HOOD_FLAG}",
        "name": " [ STA AX	  | AUX	 | PILOT ] - 1x Hood Displayed Folded Flag",
        "weight": 0,
    }
    STA_AX_AUX_PILOT_1x_Hood_Displayed_Folded_Flag_ = {
        "clsid": "{GROWLER_PYLON_XX_CN_HOOD_FLAG}",
        "name": " [ STA AX	  | AUX	 | PILOT ] - 1x Hood Displayed Folded Flag",
        "weight": 0,
    }
    STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Blue = {
        "clsid": "{SUPERHORNET_PYLON_IN_PD_1X_SMOKE_BLUE}",
        "name": " [ STA AX	  | CKPIT | SMOKE ] - 1x Internal Smoke Generator - Blue",
        "weight": 15,
    }
    STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Green = {
        "clsid": "{SUPERHORNET_PYLON_IN_PD_1X_SMOKE_GREEN}",
        "name": " [ STA AX	  | CKPIT | SMOKE ] - 1x Internal Smoke Generator - Green",
        "weight": 15,
    }
    STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Orange = {
        "clsid": "{SUPERHORNET_PYLON_IN_PD_1X_SMOKE_ORANGE}",
        "name": " [ STA AX	  | CKPIT | SMOKE ] - 1x Internal Smoke Generator - Orange",
        "weight": 15,
    }
    STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Red = {
        "clsid": "{SUPERHORNET_PYLON_IN_PD_1X_SMOKE_RED}",
        "name": " [ STA AX	  | CKPIT | SMOKE ] - 1x Internal Smoke Generator - Red",
        "weight": 15,
    }
    STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___White = {
        "clsid": "{SUPERHORNET_PYLON_IN_PD_1X_SMOKE_WHITE}",
        "name": " [ STA AX	  | CKPIT | SMOKE ] - 1x Internal Smoke Generator - White",
        "weight": 15,
    }
    STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Yellow = {
        "clsid": "{SUPERHORNET_PYLON_IN_PD_1X_SMOKE_YELLOW}",
        "name": " [ STA AX	  | CKPIT | SMOKE ] - 1x Internal Smoke Generator - Yellow",
        "weight": 15,
    }
    STA_AX_FUEL_CELLS_1x_Internal_Auxillary_Fuel_Cells = {
        "clsid": "{SUPERHORNET_PYLON_IN_FT_AUX_CELLS}",
        "name": " [ STA AX	  | FUEL	 | CELLS ] - 1x Internal Auxillary Fuel Cells",
        "weight": 1670,
    }


inject_weapons(WeaponsFA18EFG)


@planemod
class FA_18E(PlaneType):
    id = "FA-18E"
    flyable = True
    height = 4.88
    width = 13.62456
    length = 18.31
    fuel_max = 4900
    max_speed = 2120.04
    chaff = 60
    flare = 60
    charge_total = 120
    chaff_charge_size = 1
    flare_charge_size = 1
    eplrs = True
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 305

    panel_radio = {
        1: {
            "channels": {
                1: 305,
                2: 264,
                4: 256,
                8: 257,
                16: 261,
                17: 267,
                9: 255,
                18: 251,
                5: 254,
                10: 262,
                20: 266,
                11: 259,
                3: 265,
                6: 250,
                12: 268,
                13: 269,
                7: 270,
                14: 260,
                19: 253,
                15: 263,
            },
        },
        2: {
            "channels": {
                1: 305,
                2: 264,
                4: 256,
                8: 257,
                16: 261,
                17: 267,
                9: 255,
                18: 251,
                5: 254,
                10: 262,
                20: 266,
                11: 259,
                3: 265,
                6: 250,
                12: 268,
                13: 269,
                7: 270,
                14: 260,
                19: 253,
                15: 263,
            },
        },
    }

    callnames: Dict[str, List[str]] = {
        "USA": [
            "Hornet",
            "Squid",
            "Ragin",
            "Roman",
            "Sting",
            "Jury",
            "Joker",
            "Ram",
            "Hawk",
            "Devil",
            "Check",
            "Snake",
        ]
    }

    property_defaults: Dict[str, Any] = {
        "AIRCRAFT_ID_SEQ": 0,
        "DemoEquipment": False,
        "USA_FLAG": False,
        "BlockIIIEquip": True,
        "HelmetMountedDevice": 1,
        "RemoveLOutboard": False,
        "RemoveLMidboard": False,
        "RemoveLInboard": False,
        "RemoveRInboard": False,
        "RemoveRMidboard": False,
        "RemoveROutboard": False,
        "OuterBoard": 0,
        "InnerBoard": 0,
        "DYNAMIC_BORTS_MODE": 0,
        "DYNAMIC_BUNOS": False,
        "DYNAMIC_BUNO_01": 10,
        "DYNAMIC_BUNO_02": 10,
        "DYNAMIC_BUNO_03": 10,
        "DYNAMIC_BUNO_04": 10,
        "DYNAMIC_BUNO_05": 10,
        "DYNAMIC_BUNO_06": 10,
    }

    class Properties:

        class AIRCRAFT_ID_SEQ:
            id = "AIRCRAFT_ID_SEQ"

            class Values:
                Norm = 0
                Pattern_0A = 1
                Pattern_1B = 2
                Pattern_2C = 3
                Pattern_3D = 4
                Pattern_4E = 5
                Pattern_5F = 6

        class DemoEquipment:
            id = "DemoEquipment"

        class USA_FLAG:
            id = "USA_FLAG"

        class BlockIIIEquip:
            id = "BlockIIIEquip"

        class HelmetMountedDevice:
            id = "HelmetMountedDevice"

            class Values:
                Not_installed = 0
                JHMCS = 1
                NVG = 2

        class RemoveLOutboard:
            id = "RemoveLOutboard"

        class RemoveLMidboard:
            id = "RemoveLMidboard"

        class RemoveLInboard:
            id = "RemoveLInboard"

        class RemoveRInboard:
            id = "RemoveRInboard"

        class RemoveRMidboard:
            id = "RemoveRMidboard"

        class RemoveROutboard:
            id = "RemoveROutboard"

        class OuterBoard:
            id = "OuterBoard"

            class Values:
                Single = 0
                Ripple = 1

        class InnerBoard:
            id = "InnerBoard"

            class Values:
                Single = 0
                Ripple = 1

        class DYNAMIC_BORTS_MODE:
            id = "DYNAMIC_BORTS_MODE"

            class Values:
                DISABLED___NONE = 0
                USN_STANDARD = 1
                RAAF_FIGHTER = 2
                RAAF_GROWLER = 3
                KAF_LEGACY = 4
                KAF_SUPER_HORNET = 5

        class DYNAMIC_BUNOS:
            id = "DYNAMIC_BUNOS"

        class DYNAMIC_BUNO_01:
            id = "DYNAMIC_BUNO_01"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_02:
            id = "DYNAMIC_BUNO_02"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_03:
            id = "DYNAMIC_BUNO_03"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_04:
            id = "DYNAMIC_BUNO_04"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_05:
            id = "DYNAMIC_BUNO_05"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_06:
            id = "DYNAMIC_BUNO_06"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

    properties = {
        "DemoEquipment": UnitPropertyDescription(
            identifier="DemoEquipment",
            control="comboList",
            label="Demonstration Team Equipment",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "False",
                1: "True",
            },
        ),
        "USA_FLAG": UnitPropertyDescription(
            identifier="USA_FLAG",
            control="comboList",
            label="Hood Displayed USA Flag",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "False",
                1: "True",
            },
        ),
        "BlockIIIEquip": UnitPropertyDescription(
            identifier="BlockIIIEquip",
            control="comboList",
            label="Block III Antennas (Cosmetic)",
            player_only=False,
            default=1,
            w_ctrl=150,
            values={
                0: "False",
                1: "True",
            },
        ),
        "HelmetMountedDevice": UnitPropertyDescription(
            identifier="HelmetMountedDevice",
            control="comboList",
            label="Helmet Mounted Device",
            player_only=True,
            default=1,
            w_ctrl=150,
            values={
                0: "Not installed",
                1: "JHMCS",
                2: "NVG",
            },
        ),
        "RemoveLOutboard": UnitPropertyDescription(
            identifier="RemoveLOutboard",
            control="comboList",
            label="Dismount STA 2 SUU-80A Pylon (Left Outboard)",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "False",
                1: "True",
            },
        ),
        "RemoveLMidboard": UnitPropertyDescription(
            identifier="RemoveLMidboard",
            control="comboList",
            label="Dismount STA 3 SUU-79A Pylon (Left Midboard)",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "False",
                1: "True",
            },
        ),
        "RemoveLInboard": UnitPropertyDescription(
            identifier="RemoveLMidboard",
            control="comboList",
            label="Dismount STA 4 SUU-79A Pylon (Left Inboard)",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "False",
                1: "True",
            },
        ),
        "RemoveRInboard": UnitPropertyDescription(
            identifier="RemoveRInboard",
            control="comboList",
            label="Dismount STA 8 SUU-79A Pylon (Right Inboard)",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "False",
                1: "True",
            },
        ),
        "RemoveRMidboard": UnitPropertyDescription(
            identifier="RemoveRInboard",
            control="comboList",
            label="Dismount STA 9 SUU-79A Pylon (Right Midboard)",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "False",
                1: "True",
            },
        ),
        "RemoveROutboard": UnitPropertyDescription(
            identifier="RemoveROutboard",
            control="comboList",
            label="Dismount STA 10 SUU-80A Pylon (Right Outboard)",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "False",
                1: "True",
            },
        ),
        "OuterBoard": UnitPropertyDescription(
            identifier="OuterBoard",
            control="comboList",
            label="Outerboard rockets mode",
            player_only=True,
            default=0,
            w_ctrl=150,
            values={
                0: "Single",
                1: "Ripple",
            },
        ),
        "InnerBoard": UnitPropertyDescription(
            identifier="InnerBoard",
            control="comboList",
            label="Innerboard rockets mode",
            player_only=True,
            default=0,
            w_ctrl=150,
            values={
                0: "Single",
                1: "Ripple",
            },
        ),
        "datalink_Label": UnitPropertyDescription(
            identifier="datalink_Label",
            control="label",
            label="DATALINK",
            player_only=False,
            x_lbl=150,
        ),
        "VoiceCallsignLabel": UnitPropertyDescription(
            identifier="VoiceCallsignLabel",
            control="editbox",
            label="Voice Callsign Label",
            player_only=False,
        ),
        "VoiceCallsignNumber": UnitPropertyDescription(
            identifier="VoiceCallsignNumber",
            control="editbox",
            label="Voice Callsign Number",
            player_only=False,
        ),
        "STN_L16": UnitPropertyDescription(
            identifier="STN_L16",
            control="editbox",
            label="STN",
            player_only=False,
        ),
    }

    livery_name = "FA-18E"  # from livery_entry

    class Pylon1:
        STA_01_WNGTP_LAU127_1x_AIM_9M_Sidewinder_IR_AAM = (
            1,
            WeaponsFA18EFG.STA_01_WNGTP_LAU127_1x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_01_WNGTP_LAU127_1x_AIM_9X_Sidewinder_IR_AAM = (
            1,
            WeaponsFA18EFG.STA_01_WNGTP_LAU127_1x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_01_WNGTP_LAU127_1x_Captive_AIM_9M_for_ACM = (
            1,
            WeaponsFA18EFG.STA_01_WNGTP_LAU127_1x_Captive_AIM_9M_for_ACM,
        )
        STA_01_WNGTP_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod = (
            1,
            WeaponsFA18EFG.STA_01_WNGTP_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod,
        )

    class Pylon2:
        STA_02_SUU80_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar,
        )
        STA_02_SUU80_LAU127_1x_AIM_9M_Sidewinder_IR_AAM = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_02_SUU80_LAU127_1x_AIM_9X_Sidewinder_IR_AAM = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_02_SUU80_LAU127_1x_Captive_AIM_9M_for_ACM = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_Captive_AIM_9M_for_ACM,
        )
        STA_02_SUU80_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod,
        )
        STA_02_SUU80_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_02_SUU80_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_02_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_02_SUU80_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        STA_02_SUU80_LAU117_1x_AGM_65F___Maverick_F__IIR_ = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU117_1x_AGM_65F___Maverick_F__IIR_,
        )
        STA_02_SUU80_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only,
        )
        STA_02_SUU80_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        STA_02_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_02_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_02_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        STA_02_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_02_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_02_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_02_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_02_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        STA_02_SUU80_BRU32_1x_GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        STA_02_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_02_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb,
        )
        STA_02_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb,
        )
        STA_02_SUU80_BRU32_1x_CBU_99___490lbs__247_x_HEAT_Bomblets = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        STA_03_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar,
        )
        STA_03_SUU79_LAU115_1x_AIM_7F_Sparrow_Semi_Active_Radar = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU115_1x_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        STA_03_SUU79_LAU115_1x_AIM_7MH_Sparrow_Semi_Active_Radar = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU115_1x_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        STA_03_SUU79_LAU115_1x_AIM_7P_Sparrow_Semi_Active_Radar = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU115_1x_AIM_7P_Sparrow_Semi_Active_Radar,
        )
        STA_03_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_03_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_03_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_03_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_03_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_03_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_03_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_03_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_03_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM,
        )
        STA_03_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_03_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_03_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM,
        )
        STA_03_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        STA_03_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only,
        )
        STA_03_SUU79_BRU32_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        STA_03_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_03_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_03_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_03_SUU79_BRU42_1x_ADM_141A_TALD_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU42_1x_ADM_141A_TALD_,
        )
        STA_03_SUU79_BRU42_2x_ADM_141A_TALD_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU42_2x_ADM_141A_TALD_,
        )
        STA_03_SUU79_BRU42_3x_ADM_141A_TALD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU42_3x_ADM_141A_TALD,
        )
        STA_03_SUU79_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_03_SUU79_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_03_SUU79_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_03_SUU79_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_03_SUU79_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        # ERRR {SUPERHORNET_PYLON_02_MB_MK_BR55_1X_GBU-38}
        STA_03_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_03_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        STA_03_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_03_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_03_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_03_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_02_03_79_80_LAU127_1x_1x_AIM_9M_Sidewinder_IR_AAM = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_1x_1x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_02_03_79_80_LAU127_1x_1x_AIM_9X_Sidewinder_IR_AAM = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_1x_1x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_02_03_79_80_LAU127_1x_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_1x_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_02_03_79_80_LAU127_1x_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_1x_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_02_03_79_80_LAU127_1x_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_1x_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_03_02_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_02_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_03_02_79_80_BRU32_2x_GBU_16___1000lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_02_79_80_BRU32_2x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_03_02_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_02_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_03_02_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_03_02_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_03_02_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            2,
            WeaponsFA18EFG.STA_03_02_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_03_02_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_03_02_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_03_02_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            2,
            WeaponsFA18EFG.STA_03_02_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_04_02_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_04_02_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_04_02_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_04_02_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        # ERRR {SUPERHORNET_PYLON_02_MB_MK_BR55_1X_GBU-32V}
        # ERRR {SUPERHORNET_PYLON_02_MB_MK_BR55_2X_GBU-32V}
        STA_04_02_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_04_02_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_04_02_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            2,
            WeaponsFA18EFG.STA_04_02_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_04_02_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_04_02_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_04_02_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            2,
            WeaponsFA18EFG.STA_04_02_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_02_SUU80_LAU127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X,
        )
        STA_02_SUU80_EMPTY = (2, WeaponsFA18EFG.STA_02_SUU80_EMPTY)
        # ERRR <CLEAN>
        # ERRR {CATM-120C}
        # ERRR {CATM-9M}
        # ERRR {CATM-9X}
        LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar = (
            2,
            Weapons.LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar = (
            2,
            Weapons.LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7P_Sparrow_Semi_Active_Radar = (
            2,
            Weapons.LAU_115C_with_AIM_7P_Sparrow_Semi_Active_Radar,
        )
        LAU_117_AGM_65F = (2, Weapons.LAU_117_AGM_65F)
        BRU_42_with_ADM_141A_TALD = (2, Weapons.BRU_42_with_ADM_141A_TALD)
        BRU_42_with_2_x_ADM_141A_TALD = (2, Weapons.BRU_42_with_2_x_ADM_141A_TALD)
        BRU_42_with_3_x_ADM_141A_TALD = (2, Weapons.BRU_42_with_3_x_ADM_141A_TALD)
        BDU_45___500lb_Practice_Bomb = (2, Weapons.BDU_45___500lb_Practice_Bomb)
        BDU_45B___500lb_Practice_Bomb = (2, Weapons.BDU_45B___500lb_Practice_Bomb)
        GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            2,
            Weapons.GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            2,
            Weapons.GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            2,
            Weapons.Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        CBU_99___490lbs__247_x_HEAT_Bomblets = (
            2,
            Weapons.CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            2,
            Weapons.BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )

    class Pylon3:
        STA_02_SUU79_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod = (
            3,
            WeaponsFA18EFG.STA_02_SUU79_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod,
        )
        STA_03_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar_,
        )
        STA_03_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM_,
        )
        STA_03_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM_,
        )
        STA_03_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only__,
        )
        STA_03_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM_,
        )
        STA_03_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM_,
        )
        STA_03_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only__,
        )
        STA_03_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM_,
        )
        STA_03_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM_,
        )
        STA_03_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM_,
        )
        STA_03_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM_,
        )
        STA_03_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM_,
        )
        STA_03_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM_,
        )
        STA_03_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank,
        )
        STA_03_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis,
        )
        STA_03_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod,
        )
        STA_03_SUU79_BRU32_1x_ALQ_167_Countermeasures_System = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_ALQ_167_Countermeasures_System,
        )
        STA_03_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd__,
        )
        STA_03_SUU79_LAU117_1x_AGM_65F___Maverick_F__IIR__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_AGM_65F___Maverick_F__IIR__,
        )
        STA_03_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only_,
        )
        STA_03_SUU79_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        STA_03_SUU79_LAU117_1x_AGM_84D_Harpoon_Anti_Ship_Missile = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_AGM_84D_Harpoon_Anti_Ship_Missile,
        )
        STA_03_SUU79_LAU117_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        STA_03_SUU79_LAU117_1x_AGM_84H_SLAM_ER__Expanded_Response_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_AGM_84H_SLAM_ER__Expanded_Response_,
        )
        STA_03_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH_,
        )
        STA_03_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH_,
        )
        STA_03_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH_,
        )
        STA_03_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        STA_03_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        STA_03_SUU79_BRU32_1x_Mk_82___500lb_GP_Bomb_LD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_82___500lb_GP_Bomb_LD_,
        )
        STA_03_SUU79_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD_,
        )
        STA_03_SUU79_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD_,
        )
        STA_03_SUU79_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD_,
        )
        STA_03_SUU79_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD_,
        )
        STA_03_SUU79_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb_,
        )
        STA_03_SUU79_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb_,
        )
        STA_03_SUU79_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb_,
        )
        STA_03_SUU79_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb_,
        )
        STA_03_SUU79_BRU32_1x_GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb_,
        )
        # ERRR {SUPERHORNET_PYLON_03_MB_MK_1X_GBU-32V}
        STA_03_SUU79_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets_,
        )
        STA_03_SUU79_BRU32_1x_BDU_45___500lb_Practice_Bomb = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_BDU_45___500lb_Practice_Bomb,
        )
        STA_03_SUU79_BRU32_1x_BDU_45B___500lb_Practice_Bomb = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_BDU_45B___500lb_Practice_Bomb,
        )
        STA_03_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb_,
        )
        STA_03_SUU79_BRU33_2x_BDU_45___500lb_Practice_Bomb = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_BDU_45___500lb_Practice_Bomb,
        )
        STA_03_SUU79_BRU33_2x_BDU_45B___500lb_Practice_Bomb = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_BDU_45B___500lb_Practice_Bomb,
        )
        STA_03_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD_,
        )
        STA_03_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        STA_03_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD_,
        )
        STA_03_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD_,
        )
        # ERRR {SUPERHORNET_PYLON_03_MB_MK_BR2_ROCKEYE}
        STA_03_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb_,
        )
        STA_03_SUU79_BRU41_6x_BDU_33___25lb_Practice_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU41_6x_BDU_33___25lb_Practice_Bomb_LD,
        )
        STA_04_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar,
        )
        STA_04_SUU79_LAU115_1x_AIM_7F_Sparrow_Semi_Active_Radar = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU115_1x_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        STA_04_SUU79_LAU115_1x_AIM_7MH_Sparrow_Semi_Active_Radar = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU115_1x_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        STA_04_SUU79_LAU115_1x_AIM_7P_Sparrow_Semi_Active_Radar = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU115_1x_AIM_7P_Sparrow_Semi_Active_Radar,
        )
        STA_04_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_04_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_04_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM,
        )
        STA_04_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_04_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_04_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM,
        )
        STA_04_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_04_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_04_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_04_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_04_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_04_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_04_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank,
        )
        STA_04_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis,
        )
        # ERRR {SUPERHORNET_PYLON_03_IB_PD_1X_ALQ-167}
        STA_04_SUU79_BRU32_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        STA_04_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        STA_03_SUU79_BRU42_1x_ADM_141A_TALD__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU42_1x_ADM_141A_TALD__,
        )
        STA_03_SUU79_BRU42_2x_ADM_141A_TALD__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU42_2x_ADM_141A_TALD__,
        )
        STA_03_SUU79_BRU42_3x_ADM_141A_TALD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU42_3x_ADM_141A_TALD_,
        )
        STA_04_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only,
        )
        STA_04_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_04_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_04_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_04_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_04_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_04_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_04_SUU80_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_04_SUU80_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        STA_04_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_04_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_04_SUU80_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        STA_04_SUU80_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_04_SUU80_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_04_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_04_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_04_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_04_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_04_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        STA_04_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_04_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        # ERRR {SUPERHORNET_PYLON_03_IB_MK_BR2_ROCKEYE}
        STA_04_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_04_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        STA_04_03_79_80_BRU32_1x_1x_AGM_154C___JSOW_Unitary_BROACH = (
            3,
            WeaponsFA18EFG.STA_04_03_79_80_BRU32_1x_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_04_03_SUU79_BRU32_1x_1x_GBU_10___2000lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        STA_04_03_SUU79_BRU32_1x_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_04_03_SUU79_BRU32_1x_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_04_03_SUU79_BRU32_1x_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        STA_04_03_SUU79_BRU32_1x_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_04_03_SUU79_BRU32_1x_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_04_03_SUU79_BRU32_1x_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_04_03_SUU79_BRU32_1x_1x_Mk_82___500lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_04_03_SUU79_BRU32_1x_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_04_03_SUU79_BRU32_1x_1x_Mk_83___1000lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_04_03_SUU79_BRU32_1x_1x_Mk_84___2000lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_04_03_SUU79_BRU32_1x_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_03_SUU79_EMPTY = (3, WeaponsFA18EFG.STA_03_SUU79_EMPTY)
        # ERRR <CLEAN>
        # ERRR LAU-115_2*LAU-127_CATM-120C
        # ERRR LAU_117_TGM_65E
        # ERRR LAU_117_TGM_65F
        LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar = (
            3,
            Weapons.LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar = (
            3,
            Weapons.LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7P_Sparrow_Semi_Active_Radar = (
            3,
            Weapons.LAU_115C_with_AIM_7P_Sparrow_Semi_Active_Radar,
        )
        LAU_117_AGM_65F = (3, Weapons.LAU_117_AGM_65F)
        AGM_84H_SLAM_ER__Expanded_Response_ = (
            3,
            Weapons.AGM_84H_SLAM_ER__Expanded_Response_,
        )
        AGM_84D_Harpoon_AShM = (3, Weapons.AGM_84D_Harpoon_AShM)
        BRU_42_with_ADM_141A_TALD = (3, Weapons.BRU_42_with_ADM_141A_TALD)
        BRU_42_with_2_x_ADM_141A_TALD = (3, Weapons.BRU_42_with_2_x_ADM_141A_TALD)
        BRU_42_with_3_x_ADM_141A_TALD = (3, Weapons.BRU_42_with_3_x_ADM_141A_TALD)
        AGM_154A___JSOW_CEB__CBU_type_ = (3, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_ = (
            3,
            Weapons.BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        BDU_45___500lb_Practice_Bomb = (3, Weapons.BDU_45___500lb_Practice_Bomb)
        BDU_45B___500lb_Practice_Bomb = (3, Weapons.BDU_45B___500lb_Practice_Bomb)
        GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            Weapons.GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            3,
            Weapons.GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            3,
            Weapons.GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            3,
            Weapons.GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            3,
            Weapons.Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            3,
            Weapons.BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        CBU_99___490lbs__247_x_HEAT_Bomblets = (
            3,
            Weapons.CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            3,
            Weapons.BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        AWW_13_DATALINK_POD = (3, Weapons.AWW_13_DATALINK_POD)

    class Pylon4:
        STA_05_CHEEK__LAU116_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_05_CHEEK__LAU116_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_05_CHEEK__LAU116_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_05_CHEEK__LAU116_1x_AIM_7M_Sparrow_Semi_Active_Radar = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_7M_Sparrow_Semi_Active_Radar,
        )
        STA_05_CHEEK__LAU116_1x_AIM_7F_Sparrow_Semi_Active_Radar = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        STA_05_CHEEK__LAU116_1x_AIM_7MH_Sparrow_Semi_Active_Radar = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        STA_05_CHEEK__LAU116_1x_AIM_7P_Sparrow_Semi_Active_Radar = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_7P_Sparrow_Semi_Active_Radar,
        )
        STA_05_CHEEK__TGPMNT_1x_AN_ASQ_228_ATFLIR___Targeting_Pod = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__TGPMNT_1x_AN_ASQ_228_ATFLIR___Targeting_Pod,
        )
        STA_04_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank_ = (
            4,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank_,
        )
        STA_04_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis_ = (
            4,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis_,
        )
        AWW_13_DATALINK_POD = (4, Weapons.AWW_13_DATALINK_POD)
        STA_04_SUU79_BRU32_Remove_SUU_79A_A_Pylon = (
            4,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_Remove_SUU_79A_A_Pylon,
        )
        STA_05_CHEEK__TGPMNT_Empty_TGP_Mount = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__TGPMNT_Empty_TGP_Mount,
        )
        STA_05_CHEEK__LAU116_Empty_AIM_7_120_Ejectors = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_Empty_AIM_7_120_Ejectors,
        )
        # ERRR <CLEAN>
        AIM_7F_Sparrow_Semi_Active_Radar = (4, Weapons.AIM_7F_Sparrow_Semi_Active_Radar)
        AIM_7MH_Sparrow_Semi_Active_Radar = (
            4,
            Weapons.AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        AIM_7P_Sparrow_Semi_Active_Radar = (4, Weapons.AIM_7P_Sparrow_Semi_Active_Radar)
        AN_ASQ_228_ATFLIR___Targeting_Pod = (
            4,
            Weapons.AN_ASQ_228_ATFLIR___Targeting_Pod,
        )

    class Pylon5:
        STA_06_SUU78_BRU32_1x_FPU_12_A_Fuel_Tank = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_FPU_12_A_Fuel_Tank,
        )
        STA_06_SUU78_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis,
        )
        STA_06_SUU78_BRU32_1x_A_A_42R_1_Aerial_Refueling_Buddy_Pod = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_A_A_42R_1_Aerial_Refueling_Buddy_Pod,
        )
        STA_06_SUU78_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod,
        )
        STA_06_SUU78_BRU32_1x_AN_AAQ_28_LITENING___Targeting_Pod = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_AN_AAQ_28_LITENING___Targeting_Pod,
        )
        STA_06_SUU78_EMPTY = (5, WeaponsFA18EFG.STA_06_SUU78_EMPTY)
        # ERRR <CLEAN>
        AWW_13_DATALINK_POD = (5, Weapons.AWW_13_DATALINK_POD)
        AN_AAQ_28_LITENING___Targeting_Pod_ = (
            5,
            Weapons.AN_AAQ_28_LITENING___Targeting_Pod_,
        )

    class Pylon6:
        STA_07_CHEEK__LAU116_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_07_CHEEK__LAU116_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_07_CHEEK__LAU116_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_07_CHEEK__LAU116_1x_AIM_7M_Sparrow_Semi_Active_Radar = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_7M_Sparrow_Semi_Active_Radar,
        )
        STA_07_CHEEK__LAU116_1x_AIM_7F_Sparrow_Semi_Active_Radar = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        STA_07_CHEEK__LAU116_1x_AIM_7MH_Sparrow_Semi_Active_Radar = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        STA_07_CHEEK__LAU116_1x_AIM_7P_Sparrow_Semi_Active_Radar = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_7P_Sparrow_Semi_Active_Radar,
        )
        STA_08_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank = (
            6,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank,
        )
        STA_08_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis = (
            6,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis,
        )
        STA_08_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod = (
            6,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod,
        )
        STA_07_SUU79_BRU32_Remove_SUU_79A_A_Pylon = (
            6,
            WeaponsFA18EFG.STA_07_SUU79_BRU32_Remove_SUU_79A_A_Pylon,
        )
        STA_08_SUU79_EMPTY = (6, WeaponsFA18EFG.STA_08_SUU79_EMPTY)
        STA_08_SUU79_LAU127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X = (
            6,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X,
        )
        # ERRR <CLEAN>
        AIM_7F_Sparrow_Semi_Active_Radar = (6, Weapons.AIM_7F_Sparrow_Semi_Active_Radar)
        AIM_7MH_Sparrow_Semi_Active_Radar = (
            6,
            Weapons.AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        AIM_7P_Sparrow_Semi_Active_Radar = (6, Weapons.AIM_7P_Sparrow_Semi_Active_Radar)
        AWW_13_DATALINK_POD = (6, Weapons.AWW_13_DATALINK_POD)

    class Pylon7:
        STA_09_SUU79_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod,
        )
        STA_09_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar,
        )
        STA_09_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_09_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_09_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_09_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_09_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_09_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_09_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_09_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_09_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM,
        )
        STA_09_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_09_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_09_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM,
        )
        STA_09_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank,
        )
        STA_09_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis,
        )
        STA_09_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod,
        )
        STA_09_SUU79_BRU32_1x_ALQ_167_Countermeasures_System = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_ALQ_167_Countermeasures_System,
        )
        STA_09_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        STA_09_SUU79_LAU117_1x_AGM_65F___Maverick_F__IIR_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_AGM_65F___Maverick_F__IIR_,
        )
        STA_09_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only,
        )
        STA_09_SUU79_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        STA_09_SUU79_LAU117_1x_AGM_84D_Harpoon_Anti_Ship_Missile = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_AGM_84D_Harpoon_Anti_Ship_Missile,
        )
        STA_09_SUU79_LAU117_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        STA_09_SUU79_LAU117_1x_AGM_84H_SLAM_ER__Expanded_Response_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_AGM_84H_SLAM_ER__Expanded_Response_,
        )
        STA_09_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_09_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_09_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_09_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        STA_09_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        STA_09_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_09_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_09_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        STA_09_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_09_SUU80_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_09_SUU80_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        STA_09_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_09_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_09_SUU80_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        STA_09_SUU80_BRU32_1x_GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_09_SUU80_BRU32_1x_GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        STA_09_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_09_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        STA_09_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_09_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb,
        )
        STA_09_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb,
        )
        STA_09_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_09_SUU79_BRU33_2x_BDU_45___500lb_Practice_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_BDU_45___500lb_Practice_Bomb,
        )
        STA_09_SUU79_BRU33_2x_BDU_45B___500lb_Practice_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_BDU_45B___500lb_Practice_Bomb,
        )
        STA_09_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_09_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        STA_09_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_09_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        # ERRR {SUPERHORNET_PYLON_09_MB_MK_BR2_ROCKEYE}
        STA_09_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_09_SUU79_BRU41_6x_BDU_33___25lb_Practice_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU41_6x_BDU_33___25lb_Practice_Bomb_LD,
        )
        STA_08_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar,
        )
        STA_08_SUU79_LAU115_1x_AIM_7F_Sparrow_Semi_Active_Radar = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU115_1x_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        STA_08_SUU79_LAU115_1x_AIM_7MH_Sparrow_Semi_Active_Radar = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU115_1x_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        STA_08_SUU79_LAU115_1x_AIM_7P_Sparrow_Semi_Active_Radar = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU115_1x_AIM_7P_Sparrow_Semi_Active_Radar,
        )
        STA_08_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_08_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_08_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM,
        )
        STA_08_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_08_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_08_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM,
        )
        STA_08_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_08_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_08_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_08_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_08_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_08_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_08_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank_,
        )
        STA_08_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis_,
        )
        # ERRR {SUPERHORNET_PYLON_09_IB_PD_1X_ALQ-167}
        # ERRR {SUPERHORNET_PYLON_09_IB_PD_1X_ALQ-167}
        STA_08_SUU79_BRU32_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        STA_08_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        STA_08_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only,
        )
        STA_08_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_08_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_08_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_08_SUU79_BRU42_1x_ADM_141A_TALD = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU42_1x_ADM_141A_TALD,
        )
        STA_08_SUU79_BRU42_2x_ADM_141A_TALD = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU42_2x_ADM_141A_TALD,
        )
        STA_08_SUU79_BRU42_3x_ADM_141A_TALD = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU42_3x_ADM_141A_TALD,
        )
        STA_08_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_08_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_08_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_08_SUU80_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_08_SUU80_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        STA_08_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_08_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_08_SUU80_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        STA_08_SUU80_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_08_SUU80_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_08_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_08_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_08_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_08_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_08_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        STA_08_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_08_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        # ERRR {SUPERHORNET_PYLON_09_IB_MK_BR2_ROCKEYE}
        STA_08_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_08_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        STA_08_09_SUU79_BRU32_1x_1x_AGM_154C___JSOW_Unitary_BROACH = (
            7,
            WeaponsFA18EFG.STA_08_09_SUU79_BRU32_1x_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_09_08_SUU79_BRU32_1x_1x_GBU_10___2000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        STA_09_08_SUU79_BRU32_1x_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_09_08_SUU79_BRU32_1x_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_09_08_SUU79_BRU32_1x_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        STA_09_08_SUU79_BRU32_1x_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_09_08_SUU79_BRU32_1x_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_09_08_SUU79_BRU32_1x_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_09_08_SUU79_BRU32_1x_1x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_09_08_SUU79_BRU32_1x_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_09_08_SUU79_BRU32_1x_1x_Mk_83___1000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_09_08_SUU79_BRU32_1x_1x_Mk_84___2000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_09_08_SUU79_BRU32_1x_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_09_SUU79_EMPTY = (7, WeaponsFA18EFG.STA_09_SUU79_EMPTY)
        # ERRR <CLEAN>
        # ERRR LAU-115_2*LAU-127_CATM-120C
        # ERRR LAU_117_TGM_65E
        # ERRR LAU_117_TGM_65F
        LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar = (
            7,
            Weapons.LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar = (
            7,
            Weapons.LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7P_Sparrow_Semi_Active_Radar = (
            7,
            Weapons.LAU_115C_with_AIM_7P_Sparrow_Semi_Active_Radar,
        )
        LAU_117_AGM_65F = (7, Weapons.LAU_117_AGM_65F)
        AGM_84H_SLAM_ER__Expanded_Response_ = (
            7,
            Weapons.AGM_84H_SLAM_ER__Expanded_Response_,
        )
        AGM_84D_Harpoon_AShM = (7, Weapons.AGM_84D_Harpoon_AShM)
        BRU_42_with_ADM_141A_TALD = (7, Weapons.BRU_42_with_ADM_141A_TALD)
        BRU_42_with_2_x_ADM_141A_TALD = (7, Weapons.BRU_42_with_2_x_ADM_141A_TALD)
        BRU_42_with_3_x_ADM_141A_TALD = (7, Weapons.BRU_42_with_3_x_ADM_141A_TALD)
        AGM_154A___JSOW_CEB__CBU_type_ = (7, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_ = (
            7,
            Weapons.BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        BDU_45___500lb_Practice_Bomb = (7, Weapons.BDU_45___500lb_Practice_Bomb)
        BDU_45B___500lb_Practice_Bomb = (7, Weapons.BDU_45B___500lb_Practice_Bomb)
        GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            Weapons.GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            7,
            Weapons.GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            7,
            Weapons.GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            7,
            Weapons.GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            7,
            Weapons.Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            7,
            Weapons.BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            7,
            Weapons.BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        AWW_13_DATALINK_POD = (7, Weapons.AWW_13_DATALINK_POD)

    class Pylon8:
        STA_10_SUU80_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar,
        )
        STA_10_SUU80_LAU127_1x_AIM_9M_Sidewinder_IR_AAM = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_10_SUU80_LAU127_1x_AIM_9X_Sidewinder_IR_AAM = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_10_SUU80_LAU127_1x_Captive_AIM_9M_for_ACM = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_Captive_AIM_9M_for_ACM,
        )
        STA_10_SUU80_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod,
        )
        STA_10_SUU80_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_10_SUU80_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_10_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_10_SUU80_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        STA_10_SUU80_LAU117_1x_AGM_65F___Maverick_F__IIR_ = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU117_1x_AGM_65F___Maverick_F__IIR_,
        )
        STA_10_SUU80_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only,
        )
        STA_10_SUU80_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        STA_10_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_10_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_10_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        STA_10_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_10_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_10_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_10_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_10_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        STA_10_SUU80_BRU32_1x_GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        STA_10_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_10_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb,
        )
        STA_10_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb,
        )
        STA_10_SUU80_BRU32_1x_CBU_99___490lbs__247_x_HEAT_Bomblets = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        STA_09_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar_,
        )
        STA_09_SUU79_LAU115_1x_AIM_7F_Sparrow_Semi_Active_Radar_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU115_1x_AIM_7F_Sparrow_Semi_Active_Radar_,
        )
        STA_09_SUU79_LAU115_1x_AIM_7MH_Sparrow_Semi_Active_Radar_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU115_1x_AIM_7MH_Sparrow_Semi_Active_Radar_,
        )
        STA_09_SUU79_LAU115_1x_AIM_7P_Sparrow_Semi_Active_Radar_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU115_1x_AIM_7P_Sparrow_Semi_Active_Radar_,
        )
        STA_09_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM_,
        )
        STA_09_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM_,
        )
        STA_09_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only__,
        )
        STA_09_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM_,
        )
        STA_09_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM_,
        )
        STA_09_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only__,
        )
        STA_09_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM_,
        )
        STA_09_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM_,
        )
        STA_09_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM_,
        )
        STA_09_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM_,
        )
        STA_09_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM_,
        )
        STA_09_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM_,
        )
        STA_09_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd__,
        )
        STA_09_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only_,
        )
        STA_09_SUU79_LAU117_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile__,
        )
        STA_09_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH_,
        )
        STA_09_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH_,
        )
        STA_09_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH_,
        )
        STA_09_SUU79_BRU42_1x_ADM_141A_TALD_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU42_1x_ADM_141A_TALD_,
        )
        STA_09_SUU79_BRU42_2x_ADM_141A_TALD_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU42_2x_ADM_141A_TALD_,
        )
        STA_09_SUU79_BRU42_3x_ADM_141A_TALD = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU42_3x_ADM_141A_TALD,
        )
        STA_09_SUU79_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_09_SUU79_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_09_SUU79_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_09_SUU79_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_09_SUU79_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        STA_09_SUU79_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_09_SUU79_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_09_SUU79_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        STA_09_SUU79_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_09_SUU79_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_09_SUU79_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_09_SUU79_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_09_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb_,
        )
        STA_09_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        STA_09_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD_,
        )
        STA_09_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD_,
        )
        STA_09_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD_,
        )
        STA_09_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb_,
        )
        STA_09_10_79_80_LAU127_1x_1x_AIM_9M_Sidewinder_IR_AAM = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_1x_1x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_09_10_79_80_LAU127_1x_1x_AIM_9X_Sidewinder_IR_AAM = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_1x_1x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_09_10_79_80_LAU127_1x_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_1x_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_09_10_79_80_LAU127_1x_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_1x_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_09_10_79_80_LAU127_1x_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_1x_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_09_10_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_09_10_79_80_BRU32_2x_GBU_16___1000lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_BRU32_2x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_09_10_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_09_10_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_09_10_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_09_10_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_09_10_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_10_08_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_08_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_10_08_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_08_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_10_08_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_10_08_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_10_08_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            8,
            WeaponsFA18EFG.STA_10_08_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_10_08_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_10_08_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_10_08_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            8,
            WeaponsFA18EFG.STA_10_08_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_10_SUU80_LAU127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X,
        )
        STA_10_SUU80_EMPTY = (8, WeaponsFA18EFG.STA_10_SUU80_EMPTY)
        # ERRR <CLEAN>
        # ERRR {CATM-120C}
        # ERRR {CATM-9M}
        # ERRR {CATM-9X}
        LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar = (
            8,
            Weapons.LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar = (
            8,
            Weapons.LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7P_Sparrow_Semi_Active_Radar = (
            8,
            Weapons.LAU_115C_with_AIM_7P_Sparrow_Semi_Active_Radar,
        )
        LAU_117_AGM_65F = (8, Weapons.LAU_117_AGM_65F)
        BRU_42_with_ADM_141A_TALD = (8, Weapons.BRU_42_with_ADM_141A_TALD)
        BRU_42_with_2_x_ADM_141A_TALD = (8, Weapons.BRU_42_with_2_x_ADM_141A_TALD)
        BRU_42_with_3_x_ADM_141A_TALD = (8, Weapons.BRU_42_with_3_x_ADM_141A_TALD)
        BDU_45___500lb_Practice_Bomb = (8, Weapons.BDU_45___500lb_Practice_Bomb)
        BDU_45B___500lb_Practice_Bomb = (8, Weapons.BDU_45B___500lb_Practice_Bomb)
        GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            8,
            Weapons.GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            8,
            Weapons.GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            8,
            Weapons.Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        CBU_99___490lbs__247_x_HEAT_Bomblets = (
            8,
            Weapons.CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            8,
            Weapons.BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )

    class Pylon9:
        STA_11_WNGTP_LAU127_1x_AIM_9M_Sidewinder_IR_AAM = (
            9,
            WeaponsFA18EFG.STA_11_WNGTP_LAU127_1x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_11_WNGTP_LAU127_1x_AIM_9X_Sidewinder_IR_AAM = (
            9,
            WeaponsFA18EFG.STA_11_WNGTP_LAU127_1x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_11_WNGTP_LAU127_1x_Captive_AIM_9M_for_ACM = (
            9,
            WeaponsFA18EFG.STA_11_WNGTP_LAU127_1x_Captive_AIM_9M_for_ACM,
        )
        STA_11_WNGTP_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod = (
            9,
            WeaponsFA18EFG.STA_11_WNGTP_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod,
        )

    class Pylon10:
        STA_AX_FUEL_CELLS_1x_Internal_Auxillary_Fuel_Cells = (
            10,
            WeaponsFA18EFG.STA_AX_FUEL_CELLS_1x_Internal_Auxillary_Fuel_Cells,
        )
        STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___White = (
            10,
            WeaponsFA18EFG.STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___White,
        )
        STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Red = (
            10,
            WeaponsFA18EFG.STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Red,
        )
        STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Green = (
            10,
            WeaponsFA18EFG.STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Green,
        )
        STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Blue = (
            10,
            WeaponsFA18EFG.STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Blue,
        )
        STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Yellow = (
            10,
            WeaponsFA18EFG.STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Yellow,
        )
        STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Orange = (
            10,
            WeaponsFA18EFG.STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Orange,
        )

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.PinpointStrike,
        task.CAS,
        task.GroundAttack,
        task.RunwayAttack,
        task.SEAD,
        task.AFAC,
        task.AntishipStrike,
        task.Reconnaissance,
    ]
    task_default = task.CAP


@planemod
class FA_18F(PlaneType):
    id = "FA-18F"
    flyable = True
    height = 4.88
    width = 13.62456
    length = 18.31
    fuel_max = 4482
    max_speed = 2120.04
    chaff = 60
    flare = 60
    charge_total = 120
    chaff_charge_size = 1
    flare_charge_size = 1
    eplrs = True
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 305

    panel_radio = {
        1: {
            "channels": {
                1: 305,
                2: 264,
                4: 256,
                8: 257,
                16: 261,
                17: 267,
                9: 255,
                18: 251,
                5: 254,
                10: 262,
                20: 266,
                11: 259,
                3: 265,
                6: 250,
                12: 268,
                13: 269,
                7: 270,
                14: 260,
                19: 253,
                15: 263,
            },
        },
        2: {
            "channels": {
                1: 305,
                2: 264,
                4: 256,
                8: 257,
                16: 261,
                17: 267,
                9: 255,
                18: 251,
                5: 254,
                10: 262,
                20: 266,
                11: 259,
                3: 265,
                6: 250,
                12: 268,
                13: 269,
                7: 270,
                14: 260,
                19: 253,
                15: 263,
            },
        },
    }

    callnames: Dict[str, List[str]] = {
        "USA": [
            "Hornet",
            "Squid",
            "Ragin",
            "Roman",
            "Sting",
            "Jury",
            "Joker",
            "Ram",
            "Hawk",
            "Devil",
            "Check",
            "Snake",
        ]
    }

    property_defaults: Dict[str, Any] = {
        "SoloFlight": False,
        "AIRCRAFT_ID_SEQ": 0,
        "DemoEquipment": False,
        "USA_FLAG": False,
        "BlockIIIEquip": True,
        "HelmetMountedDevice": 1,
        "HelmetMountedDeviceWSO": 1,
        "RemoveLOutboard": False,
        "RemoveLMidboard": False,
        "RemoveLInboard": False,
        "RemoveRInboard": False,
        "RemoveRMidboard": False,
        "RemoveROutboard": False,
        "OuterBoard": 0,
        "InnerBoard": 0,
        "DYNAMIC_BORTS_MODE": 0,
        "DYNAMIC_BUNOS": False,
        "DYNAMIC_BUNO_01": 10,
        "DYNAMIC_BUNO_02": 10,
        "DYNAMIC_BUNO_03": 10,
        "DYNAMIC_BUNO_04": 10,
        "DYNAMIC_BUNO_05": 10,
        "DYNAMIC_BUNO_06": 10,
    }

    class Properties:

        class SoloFlight:
            id = "SoloFlight"

        class AIRCRAFT_ID_SEQ:
            id = "AIRCRAFT_ID_SEQ"

            class Values:
                Norm = 0
                Pattern_0A = 1
                Pattern_1B = 2
                Pattern_2C = 3
                Pattern_3D = 4
                Pattern_4E = 5
                Pattern_5F = 6

        class DemoEquipment:
            id = "DemoEquipment"

        class USA_FLAG:
            id = "USA_FLAG"

        class BlockIIIEquip:
            id = "BlockIIIEquip"

        class HelmetMountedDevice:
            id = "HelmetMountedDevice"

            class Values:
                Not_installed = 0
                JHMCS = 1
                NVG = 2

        class HelmetMountedDeviceWSO:
            id = "HelmetMountedDeviceWSO"

            class Values:
                Not_installed = 0
                JHMCS = 1
                NVG = 2

        class RemoveLOutboard:
            id = "RemoveLOutboard"

        class RemoveLMidboard:
            id = "RemoveLMidboard"

        class RemoveLInboard:
            id = "RemoveLInboard"

        class RemoveRInboard:
            id = "RemoveRInboard"

        class RemoveRMidboard:
            id = "RemoveRMidboard"

        class RemoveROutboard:
            id = "RemoveROutboard"

        class OuterBoard:
            id = "OuterBoard"

            class Values:
                Single = 0
                Ripple = 1

        class InnerBoard:
            id = "InnerBoard"

            class Values:
                Single = 0
                Ripple = 1

        class DYNAMIC_BORTS_MODE:
            id = "DYNAMIC_BORTS_MODE"

            class Values:
                DISABLED___NONE = 0
                USN_STANDARD = 1
                RAAF_FIGHTER = 2
                RAAF_GROWLER = 3
                KAF_LEGACY = 4
                KAF_SUPER_HORNET = 5

        class DYNAMIC_BUNOS:
            id = "DYNAMIC_BUNOS"

        class DYNAMIC_BUNO_01:
            id = "DYNAMIC_BUNO_01"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_02:
            id = "DYNAMIC_BUNO_02"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_03:
            id = "DYNAMIC_BUNO_03"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_04:
            id = "DYNAMIC_BUNO_04"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_05:
            id = "DYNAMIC_BUNO_05"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_06:
            id = "DYNAMIC_BUNO_06"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

    properties = {
        "SoloFlight": UnitPropertyDescription(
            identifier="SoloFlight",
            control="comboList",
            label="Solo Flight (Remove WSO)",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "False",
                1: "True",
            },
        ),
        "DemoEquipment": UnitPropertyDescription(
            identifier="DemoEquipment",
            control="comboList",
            label="Demonstration Team Equipment",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "False",
                1: "True",
            },
        ),
        "USA_FLAG": UnitPropertyDescription(
            identifier="USA_FLAG",
            control="comboList",
            label="Hood Displayed USA Flag",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "False",
                1: "True",
            },
        ),
        "BlockIIIEquip": UnitPropertyDescription(
            identifier="BlockIIIEquip",
            control="comboList",
            label="Block III Antennas (Cosmetic)",
            player_only=False,
            default=1,
            w_ctrl=150,
            values={
                0: "False",
                1: "True",
            },
        ),
        "HelmetMountedDevice": UnitPropertyDescription(
            identifier="HelmetMountedDevice",
            control="comboList",
            label="Helmet Mounted Device",
            player_only=True,
            default=1,
            w_ctrl=150,
            values={
                0: "Not installed",
                1: "JHMCS",
                2: "NVG",
            },
        ),
        "HelmetMountedDeviceWSO": UnitPropertyDescription(
            identifier="HelmetMountedDeviceWSO",
            control="comboList",
            label="WSO Helmet Mounted Device",
            player_only=True,
            default=1,
            w_ctrl=150,
            values={
                0: "Not installed",
                1: "JHMCS",
                2: "NVG",
            },
        ),
        "RemoveLOutboard": UnitPropertyDescription(
            identifier="RemoveLOutboard",
            control="comboList",
            label="Dismount STA 2 SUU-80A Pylon (Left Outboard)",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "False",
                1: "True",
            },
        ),
        "RemoveLMidboard": UnitPropertyDescription(
            identifier="RemoveLMidboard",
            control="comboList",
            label="Dismount STA 3 SUU-79A Pylon (Left Midboard)",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "False",
                1: "True",
            },
        ),
        "RemoveLInboard": UnitPropertyDescription(
            identifier="RemoveLMidboard",
            control="comboList",
            label="Dismount STA 4 SUU-79A Pylon (Left Inboard)",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "False",
                1: "True",
            },
        ),
        "RemoveRInboard": UnitPropertyDescription(
            identifier="RemoveRInboard",
            control="comboList",
            label="Dismount STA 8 SUU-79A Pylon (Right Inboard)",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "False",
                1: "True",
            },
        ),
        "RemoveRMidboard": UnitPropertyDescription(
            identifier="RemoveRInboard",
            control="comboList",
            label="Dismount STA 9 SUU-79A Pylon (Right Midboard)",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "False",
                1: "True",
            },
        ),
        "RemoveROutboard": UnitPropertyDescription(
            identifier="RemoveROutboard",
            control="comboList",
            label="Dismount STA 10 SUU-80A Pylon (Right Outboard)",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "False",
                1: "True",
            },
        ),
        "OuterBoard": UnitPropertyDescription(
            identifier="OuterBoard",
            control="comboList",
            label="Outerboard rockets mode",
            player_only=True,
            default=0,
            w_ctrl=150,
            values={
                0: "Single",
                1: "Ripple",
            },
        ),
        "InnerBoard": UnitPropertyDescription(
            identifier="InnerBoard",
            control="comboList",
            label="Innerboard rockets mode",
            player_only=True,
            default=0,
            w_ctrl=150,
            values={
                0: "Single",
                1: "Ripple",
            },
        ),
        "datalink_Label": UnitPropertyDescription(
            identifier="datalink_Label",
            control="label",
            label="DATALINK",
            player_only=False,
            x_lbl=150,
        ),
        "VoiceCallsignLabel": UnitPropertyDescription(
            identifier="VoiceCallsignLabel",
            control="editbox",
            label="Voice Callsign Label",
            player_only=False,
        ),
        "VoiceCallsignNumber": UnitPropertyDescription(
            identifier="VoiceCallsignNumber",
            control="editbox",
            label="Voice Callsign Number",
            player_only=False,
        ),
        "STN_L16": UnitPropertyDescription(
            identifier="STN_L16",
            control="editbox",
            label="STN",
            player_only=False,
        ),
    }

    livery_name = "FA-18F"  # from livery_entry

    class Pylon1:
        STA_01_WNGTP_LAU127_1x_AIM_9M_Sidewinder_IR_AAM = (
            1,
            WeaponsFA18EFG.STA_01_WNGTP_LAU127_1x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_01_WNGTP_LAU127_1x_AIM_9X_Sidewinder_IR_AAM = (
            1,
            WeaponsFA18EFG.STA_01_WNGTP_LAU127_1x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_01_WNGTP_LAU127_1x_Captive_AIM_9M_for_ACM = (
            1,
            WeaponsFA18EFG.STA_01_WNGTP_LAU127_1x_Captive_AIM_9M_for_ACM,
        )
        STA_01_WNGTP_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod = (
            1,
            WeaponsFA18EFG.STA_01_WNGTP_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod,
        )

    class Pylon2:
        STA_02_SUU80_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar,
        )
        STA_02_SUU80_LAU127_1x_AIM_9M_Sidewinder_IR_AAM = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_02_SUU80_LAU127_1x_AIM_9X_Sidewinder_IR_AAM = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_02_SUU80_LAU127_1x_Captive_AIM_9M_for_ACM = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_Captive_AIM_9M_for_ACM,
        )
        STA_02_SUU80_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod,
        )
        STA_02_SUU80_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_02_SUU80_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_02_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_02_SUU80_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        STA_02_SUU80_LAU117_1x_AGM_65F___Maverick_F__IIR_ = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU117_1x_AGM_65F___Maverick_F__IIR_,
        )
        STA_02_SUU80_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only,
        )
        STA_02_SUU80_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        STA_02_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_02_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_02_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        STA_02_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_02_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_02_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_02_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_02_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        STA_02_SUU80_BRU32_1x_GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        STA_02_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_02_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb,
        )
        STA_02_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb,
        )
        STA_02_SUU80_BRU32_1x_CBU_99___490lbs__247_x_HEAT_Bomblets = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        STA_03_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar,
        )
        STA_03_SUU79_LAU115_1x_AIM_7F_Sparrow_Semi_Active_Radar = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU115_1x_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        STA_03_SUU79_LAU115_1x_AIM_7MH_Sparrow_Semi_Active_Radar = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU115_1x_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        STA_03_SUU79_LAU115_1x_AIM_7P_Sparrow_Semi_Active_Radar = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU115_1x_AIM_7P_Sparrow_Semi_Active_Radar,
        )
        STA_03_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_03_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_03_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_03_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_03_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_03_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_03_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_03_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_03_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM,
        )
        STA_03_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_03_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_03_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM,
        )
        STA_03_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        STA_03_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only,
        )
        STA_03_SUU79_BRU32_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        STA_03_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_03_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_03_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_03_SUU79_BRU42_1x_ADM_141A_TALD_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU42_1x_ADM_141A_TALD_,
        )
        STA_03_SUU79_BRU42_2x_ADM_141A_TALD_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU42_2x_ADM_141A_TALD_,
        )
        STA_03_SUU79_BRU42_3x_ADM_141A_TALD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU42_3x_ADM_141A_TALD,
        )
        STA_03_SUU79_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_03_SUU79_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_03_SUU79_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_03_SUU79_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_03_SUU79_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        # ERRR {SUPERHORNET_PYLON_02_MB_MK_BR55_1X_GBU-38}
        STA_03_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_03_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        STA_03_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_03_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_03_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_03_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_02_03_79_80_LAU127_1x_1x_AIM_9M_Sidewinder_IR_AAM = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_1x_1x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_02_03_79_80_LAU127_1x_1x_AIM_9X_Sidewinder_IR_AAM = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_1x_1x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_02_03_79_80_LAU127_1x_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_1x_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_02_03_79_80_LAU127_1x_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_1x_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_02_03_79_80_LAU127_1x_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_1x_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_03_02_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_02_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_03_02_79_80_BRU32_2x_GBU_16___1000lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_02_79_80_BRU32_2x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_03_02_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_02_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_03_02_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_03_02_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_03_02_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            2,
            WeaponsFA18EFG.STA_03_02_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_03_02_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_03_02_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_03_02_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            2,
            WeaponsFA18EFG.STA_03_02_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_04_02_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_04_02_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_04_02_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_04_02_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        # ERRR {SUPERHORNET_PYLON_02_MB_MK_BR55_1X_GBU-32V}
        # ERRR {SUPERHORNET_PYLON_02_MB_MK_BR55_2X_GBU-32V}
        STA_04_02_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_04_02_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_04_02_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            2,
            WeaponsFA18EFG.STA_04_02_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_04_02_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_04_02_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_04_02_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            2,
            WeaponsFA18EFG.STA_04_02_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_02_SUU80_LAU127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X,
        )
        STA_02_SUU80_EMPTY = (2, WeaponsFA18EFG.STA_02_SUU80_EMPTY)
        # ERRR <CLEAN>
        # ERRR {CATM-120C}
        # ERRR {CATM-9M}
        # ERRR {CATM-9X}
        LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar = (
            2,
            Weapons.LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar = (
            2,
            Weapons.LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7P_Sparrow_Semi_Active_Radar = (
            2,
            Weapons.LAU_115C_with_AIM_7P_Sparrow_Semi_Active_Radar,
        )
        LAU_117_AGM_65F = (2, Weapons.LAU_117_AGM_65F)
        BRU_42_with_ADM_141A_TALD = (2, Weapons.BRU_42_with_ADM_141A_TALD)
        BRU_42_with_2_x_ADM_141A_TALD = (2, Weapons.BRU_42_with_2_x_ADM_141A_TALD)
        BRU_42_with_3_x_ADM_141A_TALD = (2, Weapons.BRU_42_with_3_x_ADM_141A_TALD)
        BDU_45___500lb_Practice_Bomb = (2, Weapons.BDU_45___500lb_Practice_Bomb)
        BDU_45B___500lb_Practice_Bomb = (2, Weapons.BDU_45B___500lb_Practice_Bomb)
        GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            2,
            Weapons.GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            2,
            Weapons.GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            2,
            Weapons.Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        CBU_99___490lbs__247_x_HEAT_Bomblets = (
            2,
            Weapons.CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            2,
            Weapons.BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )

    class Pylon3:
        STA_02_SUU79_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod = (
            3,
            WeaponsFA18EFG.STA_02_SUU79_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod,
        )
        STA_03_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar_,
        )
        STA_03_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM_,
        )
        STA_03_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM_,
        )
        STA_03_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only__,
        )
        STA_03_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM_,
        )
        STA_03_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM_,
        )
        STA_03_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only__,
        )
        STA_03_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM_,
        )
        STA_03_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM_,
        )
        STA_03_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM_,
        )
        STA_03_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM_,
        )
        STA_03_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM_,
        )
        STA_03_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM_,
        )
        STA_03_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank,
        )
        STA_03_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis,
        )
        STA_03_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod,
        )
        STA_03_SUU79_BRU32_1x_ALQ_167_Countermeasures_System = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_ALQ_167_Countermeasures_System,
        )
        STA_03_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd__,
        )
        STA_03_SUU79_LAU117_1x_AGM_65F___Maverick_F__IIR__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_AGM_65F___Maverick_F__IIR__,
        )
        STA_03_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only_,
        )
        STA_03_SUU79_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        STA_03_SUU79_LAU117_1x_AGM_84D_Harpoon_Anti_Ship_Missile = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_AGM_84D_Harpoon_Anti_Ship_Missile,
        )
        STA_03_SUU79_LAU117_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        STA_03_SUU79_LAU117_1x_AGM_84H_SLAM_ER__Expanded_Response_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_AGM_84H_SLAM_ER__Expanded_Response_,
        )
        STA_03_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH_,
        )
        STA_03_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH_,
        )
        STA_03_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH_,
        )
        STA_03_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        STA_03_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        STA_03_SUU79_BRU32_1x_Mk_82___500lb_GP_Bomb_LD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_82___500lb_GP_Bomb_LD_,
        )
        STA_03_SUU79_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD_,
        )
        STA_03_SUU79_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD_,
        )
        STA_03_SUU79_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD_,
        )
        STA_03_SUU79_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD_,
        )
        STA_03_SUU79_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb_,
        )
        STA_03_SUU79_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb_,
        )
        STA_03_SUU79_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb_,
        )
        STA_03_SUU79_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb_,
        )
        STA_03_SUU79_BRU32_1x_GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb_,
        )
        # ERRR {SUPERHORNET_PYLON_03_MB_MK_1X_GBU-32V}
        STA_03_SUU79_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets_,
        )
        STA_03_SUU79_BRU32_1x_BDU_45___500lb_Practice_Bomb = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_BDU_45___500lb_Practice_Bomb,
        )
        STA_03_SUU79_BRU32_1x_BDU_45B___500lb_Practice_Bomb = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_BDU_45B___500lb_Practice_Bomb,
        )
        STA_03_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb_,
        )
        STA_03_SUU79_BRU33_2x_BDU_45___500lb_Practice_Bomb = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_BDU_45___500lb_Practice_Bomb,
        )
        STA_03_SUU79_BRU33_2x_BDU_45B___500lb_Practice_Bomb = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_BDU_45B___500lb_Practice_Bomb,
        )
        STA_03_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD_,
        )
        STA_03_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        STA_03_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD_,
        )
        STA_03_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD_,
        )
        # ERRR {SUPERHORNET_PYLON_03_MB_MK_BR2_ROCKEYE}
        STA_03_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb_,
        )
        STA_03_SUU79_BRU41_6x_BDU_33___25lb_Practice_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU41_6x_BDU_33___25lb_Practice_Bomb_LD,
        )
        STA_04_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar,
        )
        STA_04_SUU79_LAU115_1x_AIM_7F_Sparrow_Semi_Active_Radar = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU115_1x_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        STA_04_SUU79_LAU115_1x_AIM_7MH_Sparrow_Semi_Active_Radar = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU115_1x_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        STA_04_SUU79_LAU115_1x_AIM_7P_Sparrow_Semi_Active_Radar = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU115_1x_AIM_7P_Sparrow_Semi_Active_Radar,
        )
        STA_04_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_04_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_04_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM,
        )
        STA_04_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_04_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_04_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM,
        )
        STA_04_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_04_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_04_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_04_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_04_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_04_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_04_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank,
        )
        STA_04_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis,
        )
        # ERRR {SUPERHORNET_PYLON_03_IB_PD_1X_ALQ-167}
        STA_04_SUU79_BRU32_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        STA_04_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        STA_03_SUU79_BRU42_1x_ADM_141A_TALD__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU42_1x_ADM_141A_TALD__,
        )
        STA_03_SUU79_BRU42_2x_ADM_141A_TALD__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU42_2x_ADM_141A_TALD__,
        )
        STA_03_SUU79_BRU42_3x_ADM_141A_TALD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU42_3x_ADM_141A_TALD_,
        )
        STA_04_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only,
        )
        STA_04_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_04_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_04_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_04_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_04_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_04_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_04_SUU80_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_04_SUU80_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        STA_04_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_04_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_04_SUU80_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        STA_04_SUU80_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_04_SUU80_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_04_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_04_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_04_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_04_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_04_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        STA_04_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_04_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        # ERRR {SUPERHORNET_PYLON_03_IB_MK_BR2_ROCKEYE}
        STA_04_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_04_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        STA_04_03_79_80_BRU32_1x_1x_AGM_154C___JSOW_Unitary_BROACH = (
            3,
            WeaponsFA18EFG.STA_04_03_79_80_BRU32_1x_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_04_03_SUU79_BRU32_1x_1x_GBU_10___2000lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        STA_04_03_SUU79_BRU32_1x_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_04_03_SUU79_BRU32_1x_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_04_03_SUU79_BRU32_1x_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        STA_04_03_SUU79_BRU32_1x_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_04_03_SUU79_BRU32_1x_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_04_03_SUU79_BRU32_1x_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_04_03_SUU79_BRU32_1x_1x_Mk_82___500lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_04_03_SUU79_BRU32_1x_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_04_03_SUU79_BRU32_1x_1x_Mk_83___1000lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_04_03_SUU79_BRU32_1x_1x_Mk_84___2000lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_04_03_SUU79_BRU32_1x_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_03_SUU79_EMPTY = (3, WeaponsFA18EFG.STA_03_SUU79_EMPTY)
        # ERRR <CLEAN>
        # ERRR LAU-115_2*LAU-127_CATM-120C
        # ERRR LAU_117_TGM_65E
        # ERRR LAU_117_TGM_65F
        LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar = (
            3,
            Weapons.LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar = (
            3,
            Weapons.LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7P_Sparrow_Semi_Active_Radar = (
            3,
            Weapons.LAU_115C_with_AIM_7P_Sparrow_Semi_Active_Radar,
        )
        LAU_117_AGM_65F = (3, Weapons.LAU_117_AGM_65F)
        AGM_84H_SLAM_ER__Expanded_Response_ = (
            3,
            Weapons.AGM_84H_SLAM_ER__Expanded_Response_,
        )
        AGM_84D_Harpoon_AShM = (3, Weapons.AGM_84D_Harpoon_AShM)
        BRU_42_with_ADM_141A_TALD = (3, Weapons.BRU_42_with_ADM_141A_TALD)
        BRU_42_with_2_x_ADM_141A_TALD = (3, Weapons.BRU_42_with_2_x_ADM_141A_TALD)
        BRU_42_with_3_x_ADM_141A_TALD = (3, Weapons.BRU_42_with_3_x_ADM_141A_TALD)
        AGM_154A___JSOW_CEB__CBU_type_ = (3, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_ = (
            3,
            Weapons.BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        BDU_45___500lb_Practice_Bomb = (3, Weapons.BDU_45___500lb_Practice_Bomb)
        BDU_45B___500lb_Practice_Bomb = (3, Weapons.BDU_45B___500lb_Practice_Bomb)
        GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            Weapons.GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            3,
            Weapons.GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            3,
            Weapons.GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            3,
            Weapons.GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            3,
            Weapons.Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            3,
            Weapons.BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        CBU_99___490lbs__247_x_HEAT_Bomblets = (
            3,
            Weapons.CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            3,
            Weapons.BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        AWW_13_DATALINK_POD = (3, Weapons.AWW_13_DATALINK_POD)

    class Pylon4:
        STA_05_CHEEK__LAU116_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_05_CHEEK__LAU116_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_05_CHEEK__LAU116_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_05_CHEEK__LAU116_1x_AIM_7M_Sparrow_Semi_Active_Radar = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_7M_Sparrow_Semi_Active_Radar,
        )
        STA_05_CHEEK__LAU116_1x_AIM_7F_Sparrow_Semi_Active_Radar = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        STA_05_CHEEK__LAU116_1x_AIM_7MH_Sparrow_Semi_Active_Radar = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        STA_05_CHEEK__LAU116_1x_AIM_7P_Sparrow_Semi_Active_Radar = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_7P_Sparrow_Semi_Active_Radar,
        )
        STA_05_CHEEK__TGPMNT_1x_AN_ASQ_228_ATFLIR___Targeting_Pod = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__TGPMNT_1x_AN_ASQ_228_ATFLIR___Targeting_Pod,
        )
        STA_04_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank_ = (
            4,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank_,
        )
        STA_04_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis_ = (
            4,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis_,
        )
        AWW_13_DATALINK_POD = (4, Weapons.AWW_13_DATALINK_POD)
        STA_04_SUU79_BRU32_Remove_SUU_79A_A_Pylon = (
            4,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_Remove_SUU_79A_A_Pylon,
        )
        STA_05_CHEEK__TGPMNT_Empty_TGP_Mount = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__TGPMNT_Empty_TGP_Mount,
        )
        STA_05_CHEEK__LAU116_Empty_AIM_7_120_Ejectors = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_Empty_AIM_7_120_Ejectors,
        )
        # ERRR <CLEAN>
        AIM_7F_Sparrow_Semi_Active_Radar = (4, Weapons.AIM_7F_Sparrow_Semi_Active_Radar)
        AIM_7MH_Sparrow_Semi_Active_Radar = (
            4,
            Weapons.AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        AIM_7P_Sparrow_Semi_Active_Radar = (4, Weapons.AIM_7P_Sparrow_Semi_Active_Radar)
        AN_ASQ_228_ATFLIR___Targeting_Pod = (
            4,
            Weapons.AN_ASQ_228_ATFLIR___Targeting_Pod,
        )

    class Pylon5:
        STA_06_SUU78_BRU32_1x_FPU_12_A_Fuel_Tank = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_FPU_12_A_Fuel_Tank,
        )
        STA_06_SUU78_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis,
        )
        STA_06_SUU78_BRU32_1x_A_A_42R_1_Aerial_Refueling_Buddy_Pod = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_A_A_42R_1_Aerial_Refueling_Buddy_Pod,
        )
        STA_06_SUU78_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod,
        )
        STA_06_SUU78_BRU32_1x_AN_AAQ_28_LITENING___Targeting_Pod = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_AN_AAQ_28_LITENING___Targeting_Pod,
        )
        STA_06_SUU78_EMPTY = (5, WeaponsFA18EFG.STA_06_SUU78_EMPTY)
        # ERRR <CLEAN>
        AWW_13_DATALINK_POD = (5, Weapons.AWW_13_DATALINK_POD)
        AN_AAQ_28_LITENING___Targeting_Pod_ = (
            5,
            Weapons.AN_AAQ_28_LITENING___Targeting_Pod_,
        )

    class Pylon6:
        STA_07_CHEEK__LAU116_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_07_CHEEK__LAU116_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_07_CHEEK__LAU116_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_07_CHEEK__LAU116_1x_AIM_7M_Sparrow_Semi_Active_Radar = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_7M_Sparrow_Semi_Active_Radar,
        )
        STA_07_CHEEK__LAU116_1x_AIM_7F_Sparrow_Semi_Active_Radar = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        STA_07_CHEEK__LAU116_1x_AIM_7MH_Sparrow_Semi_Active_Radar = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        STA_07_CHEEK__LAU116_1x_AIM_7P_Sparrow_Semi_Active_Radar = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_7P_Sparrow_Semi_Active_Radar,
        )
        STA_08_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank = (
            6,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank,
        )
        STA_08_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis = (
            6,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis,
        )
        STA_08_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod = (
            6,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod,
        )
        STA_07_SUU79_BRU32_Remove_SUU_79A_A_Pylon = (
            6,
            WeaponsFA18EFG.STA_07_SUU79_BRU32_Remove_SUU_79A_A_Pylon,
        )
        STA_08_SUU79_EMPTY = (6, WeaponsFA18EFG.STA_08_SUU79_EMPTY)
        STA_08_SUU79_LAU127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X = (
            6,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X,
        )
        # ERRR <CLEAN>
        AIM_7F_Sparrow_Semi_Active_Radar = (6, Weapons.AIM_7F_Sparrow_Semi_Active_Radar)
        AIM_7MH_Sparrow_Semi_Active_Radar = (
            6,
            Weapons.AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        AIM_7P_Sparrow_Semi_Active_Radar = (6, Weapons.AIM_7P_Sparrow_Semi_Active_Radar)
        AWW_13_DATALINK_POD = (6, Weapons.AWW_13_DATALINK_POD)

    class Pylon7:
        STA_09_SUU79_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod,
        )
        STA_09_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar,
        )
        STA_09_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_09_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_09_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_09_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_09_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_09_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_09_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_09_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_09_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM,
        )
        STA_09_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_09_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_09_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM,
        )
        STA_09_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank,
        )
        STA_09_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis,
        )
        STA_09_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod,
        )
        STA_09_SUU79_BRU32_1x_ALQ_167_Countermeasures_System = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_ALQ_167_Countermeasures_System,
        )
        STA_09_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        STA_09_SUU79_LAU117_1x_AGM_65F___Maverick_F__IIR_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_AGM_65F___Maverick_F__IIR_,
        )
        STA_09_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only,
        )
        STA_09_SUU79_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        STA_09_SUU79_LAU117_1x_AGM_84D_Harpoon_Anti_Ship_Missile = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_AGM_84D_Harpoon_Anti_Ship_Missile,
        )
        STA_09_SUU79_LAU117_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        STA_09_SUU79_LAU117_1x_AGM_84H_SLAM_ER__Expanded_Response_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_AGM_84H_SLAM_ER__Expanded_Response_,
        )
        STA_09_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_09_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_09_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_09_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        STA_09_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        STA_09_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_09_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_09_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        STA_09_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_09_SUU80_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_09_SUU80_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        STA_09_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_09_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_09_SUU80_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        STA_09_SUU80_BRU32_1x_GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_09_SUU80_BRU32_1x_GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        STA_09_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_09_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        STA_09_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_09_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb,
        )
        STA_09_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb,
        )
        STA_09_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_09_SUU79_BRU33_2x_BDU_45___500lb_Practice_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_BDU_45___500lb_Practice_Bomb,
        )
        STA_09_SUU79_BRU33_2x_BDU_45B___500lb_Practice_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_BDU_45B___500lb_Practice_Bomb,
        )
        STA_09_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_09_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        STA_09_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_09_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        # ERRR {SUPERHORNET_PYLON_09_MB_MK_BR2_ROCKEYE}
        STA_09_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_09_SUU79_BRU41_6x_BDU_33___25lb_Practice_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU41_6x_BDU_33___25lb_Practice_Bomb_LD,
        )
        STA_08_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar,
        )
        STA_08_SUU79_LAU115_1x_AIM_7F_Sparrow_Semi_Active_Radar = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU115_1x_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        STA_08_SUU79_LAU115_1x_AIM_7MH_Sparrow_Semi_Active_Radar = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU115_1x_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        STA_08_SUU79_LAU115_1x_AIM_7P_Sparrow_Semi_Active_Radar = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU115_1x_AIM_7P_Sparrow_Semi_Active_Radar,
        )
        STA_08_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_08_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_08_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM,
        )
        STA_08_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_08_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_08_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM,
        )
        STA_08_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_08_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_08_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_08_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_08_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_08_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_08_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank_,
        )
        STA_08_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis_,
        )
        # ERRR {SUPERHORNET_PYLON_09_IB_PD_1X_ALQ-167}
        # ERRR {SUPERHORNET_PYLON_09_IB_PD_1X_ALQ-167}
        STA_08_SUU79_BRU32_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        STA_08_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        STA_08_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only,
        )
        STA_08_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_08_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_08_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_08_SUU79_BRU42_1x_ADM_141A_TALD = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU42_1x_ADM_141A_TALD,
        )
        STA_08_SUU79_BRU42_2x_ADM_141A_TALD = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU42_2x_ADM_141A_TALD,
        )
        STA_08_SUU79_BRU42_3x_ADM_141A_TALD = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU42_3x_ADM_141A_TALD,
        )
        STA_08_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_08_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_08_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_08_SUU80_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_08_SUU80_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        STA_08_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_08_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_08_SUU80_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        STA_08_SUU80_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_08_SUU80_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_08_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_08_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_08_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_08_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_08_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        STA_08_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_08_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        # ERRR {SUPERHORNET_PYLON_09_IB_MK_BR2_ROCKEYE}
        STA_08_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_08_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        STA_08_09_SUU79_BRU32_1x_1x_AGM_154C___JSOW_Unitary_BROACH = (
            7,
            WeaponsFA18EFG.STA_08_09_SUU79_BRU32_1x_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_09_08_SUU79_BRU32_1x_1x_GBU_10___2000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        STA_09_08_SUU79_BRU32_1x_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_09_08_SUU79_BRU32_1x_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_09_08_SUU79_BRU32_1x_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        STA_09_08_SUU79_BRU32_1x_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_09_08_SUU79_BRU32_1x_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_09_08_SUU79_BRU32_1x_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_09_08_SUU79_BRU32_1x_1x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_09_08_SUU79_BRU32_1x_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_09_08_SUU79_BRU32_1x_1x_Mk_83___1000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_09_08_SUU79_BRU32_1x_1x_Mk_84___2000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_09_08_SUU79_BRU32_1x_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_09_SUU79_EMPTY = (7, WeaponsFA18EFG.STA_09_SUU79_EMPTY)
        # ERRR <CLEAN>
        # ERRR LAU-115_2*LAU-127_CATM-120C
        # ERRR LAU_117_TGM_65E
        # ERRR LAU_117_TGM_65F
        LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar = (
            7,
            Weapons.LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar = (
            7,
            Weapons.LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7P_Sparrow_Semi_Active_Radar = (
            7,
            Weapons.LAU_115C_with_AIM_7P_Sparrow_Semi_Active_Radar,
        )
        LAU_117_AGM_65F = (7, Weapons.LAU_117_AGM_65F)
        AGM_84H_SLAM_ER__Expanded_Response_ = (
            7,
            Weapons.AGM_84H_SLAM_ER__Expanded_Response_,
        )
        AGM_84D_Harpoon_AShM = (7, Weapons.AGM_84D_Harpoon_AShM)
        BRU_42_with_ADM_141A_TALD = (7, Weapons.BRU_42_with_ADM_141A_TALD)
        BRU_42_with_2_x_ADM_141A_TALD = (7, Weapons.BRU_42_with_2_x_ADM_141A_TALD)
        BRU_42_with_3_x_ADM_141A_TALD = (7, Weapons.BRU_42_with_3_x_ADM_141A_TALD)
        AGM_154A___JSOW_CEB__CBU_type_ = (7, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_ = (
            7,
            Weapons.BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        BDU_45___500lb_Practice_Bomb = (7, Weapons.BDU_45___500lb_Practice_Bomb)
        BDU_45B___500lb_Practice_Bomb = (7, Weapons.BDU_45B___500lb_Practice_Bomb)
        GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            Weapons.GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            7,
            Weapons.GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            7,
            Weapons.GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            7,
            Weapons.GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            7,
            Weapons.Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            7,
            Weapons.BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            7,
            Weapons.BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        AWW_13_DATALINK_POD = (7, Weapons.AWW_13_DATALINK_POD)

    class Pylon8:
        STA_10_SUU80_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar,
        )
        STA_10_SUU80_LAU127_1x_AIM_9M_Sidewinder_IR_AAM = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_10_SUU80_LAU127_1x_AIM_9X_Sidewinder_IR_AAM = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_10_SUU80_LAU127_1x_Captive_AIM_9M_for_ACM = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_Captive_AIM_9M_for_ACM,
        )
        STA_10_SUU80_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod,
        )
        STA_10_SUU80_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_10_SUU80_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_10_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_10_SUU80_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        STA_10_SUU80_LAU117_1x_AGM_65F___Maverick_F__IIR_ = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU117_1x_AGM_65F___Maverick_F__IIR_,
        )
        STA_10_SUU80_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only,
        )
        STA_10_SUU80_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        STA_10_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_10_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_10_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        STA_10_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_10_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_10_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_10_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_10_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        STA_10_SUU80_BRU32_1x_GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        STA_10_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_10_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb,
        )
        STA_10_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb,
        )
        STA_10_SUU80_BRU32_1x_CBU_99___490lbs__247_x_HEAT_Bomblets = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        STA_09_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar_,
        )
        STA_09_SUU79_LAU115_1x_AIM_7F_Sparrow_Semi_Active_Radar_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU115_1x_AIM_7F_Sparrow_Semi_Active_Radar_,
        )
        STA_09_SUU79_LAU115_1x_AIM_7MH_Sparrow_Semi_Active_Radar_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU115_1x_AIM_7MH_Sparrow_Semi_Active_Radar_,
        )
        STA_09_SUU79_LAU115_1x_AIM_7P_Sparrow_Semi_Active_Radar_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU115_1x_AIM_7P_Sparrow_Semi_Active_Radar_,
        )
        STA_09_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM_,
        )
        STA_09_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM_,
        )
        STA_09_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only__,
        )
        STA_09_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM_,
        )
        STA_09_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM_,
        )
        STA_09_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only__,
        )
        STA_09_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM_,
        )
        STA_09_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM_,
        )
        STA_09_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM_,
        )
        STA_09_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM_,
        )
        STA_09_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM_,
        )
        STA_09_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM_,
        )
        STA_09_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd__,
        )
        STA_09_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only_,
        )
        STA_09_SUU79_LAU117_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile__,
        )
        STA_09_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH_,
        )
        STA_09_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH_,
        )
        STA_09_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH_,
        )
        STA_09_SUU79_BRU42_1x_ADM_141A_TALD_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU42_1x_ADM_141A_TALD_,
        )
        STA_09_SUU79_BRU42_2x_ADM_141A_TALD_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU42_2x_ADM_141A_TALD_,
        )
        STA_09_SUU79_BRU42_3x_ADM_141A_TALD = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU42_3x_ADM_141A_TALD,
        )
        STA_09_SUU79_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_09_SUU79_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_09_SUU79_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_09_SUU79_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_09_SUU79_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        STA_09_SUU79_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_09_SUU79_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_09_SUU79_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        STA_09_SUU79_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_09_SUU79_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_09_SUU79_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_09_SUU79_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_09_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb_,
        )
        STA_09_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        STA_09_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD_,
        )
        STA_09_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD_,
        )
        STA_09_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD_,
        )
        STA_09_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb_,
        )
        STA_09_10_79_80_LAU127_1x_1x_AIM_9M_Sidewinder_IR_AAM = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_1x_1x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_09_10_79_80_LAU127_1x_1x_AIM_9X_Sidewinder_IR_AAM = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_1x_1x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_09_10_79_80_LAU127_1x_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_1x_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_09_10_79_80_LAU127_1x_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_1x_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_09_10_79_80_LAU127_1x_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_1x_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_09_10_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_09_10_79_80_BRU32_2x_GBU_16___1000lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_BRU32_2x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_09_10_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_09_10_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_09_10_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_09_10_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_09_10_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_10_08_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_08_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_10_08_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_08_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_10_08_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_10_08_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_10_08_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            8,
            WeaponsFA18EFG.STA_10_08_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_10_08_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_10_08_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_10_08_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            8,
            WeaponsFA18EFG.STA_10_08_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_10_SUU80_LAU127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X,
        )
        STA_10_SUU80_EMPTY = (8, WeaponsFA18EFG.STA_10_SUU80_EMPTY)
        # ERRR <CLEAN>
        # ERRR {CATM-120C}
        # ERRR {CATM-9M}
        # ERRR {CATM-9X}
        LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar = (
            8,
            Weapons.LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar = (
            8,
            Weapons.LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7P_Sparrow_Semi_Active_Radar = (
            8,
            Weapons.LAU_115C_with_AIM_7P_Sparrow_Semi_Active_Radar,
        )
        LAU_117_AGM_65F = (8, Weapons.LAU_117_AGM_65F)
        BRU_42_with_ADM_141A_TALD = (8, Weapons.BRU_42_with_ADM_141A_TALD)
        BRU_42_with_2_x_ADM_141A_TALD = (8, Weapons.BRU_42_with_2_x_ADM_141A_TALD)
        BRU_42_with_3_x_ADM_141A_TALD = (8, Weapons.BRU_42_with_3_x_ADM_141A_TALD)
        BDU_45___500lb_Practice_Bomb = (8, Weapons.BDU_45___500lb_Practice_Bomb)
        BDU_45B___500lb_Practice_Bomb = (8, Weapons.BDU_45B___500lb_Practice_Bomb)
        GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            8,
            Weapons.GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            8,
            Weapons.GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            8,
            Weapons.Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        CBU_99___490lbs__247_x_HEAT_Bomblets = (
            8,
            Weapons.CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            8,
            Weapons.BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )

    class Pylon9:
        STA_11_WNGTP_LAU127_1x_AIM_9M_Sidewinder_IR_AAM = (
            9,
            WeaponsFA18EFG.STA_11_WNGTP_LAU127_1x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_11_WNGTP_LAU127_1x_AIM_9X_Sidewinder_IR_AAM = (
            9,
            WeaponsFA18EFG.STA_11_WNGTP_LAU127_1x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_11_WNGTP_LAU127_1x_Captive_AIM_9M_for_ACM = (
            9,
            WeaponsFA18EFG.STA_11_WNGTP_LAU127_1x_Captive_AIM_9M_for_ACM,
        )
        STA_11_WNGTP_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod = (
            9,
            WeaponsFA18EFG.STA_11_WNGTP_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod,
        )

    class Pylon10:
        STA_AX_FUEL_CELLS_1x_Internal_Auxillary_Fuel_Cells = (
            10,
            WeaponsFA18EFG.STA_AX_FUEL_CELLS_1x_Internal_Auxillary_Fuel_Cells,
        )
        STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___White = (
            10,
            WeaponsFA18EFG.STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___White,
        )
        STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Red = (
            10,
            WeaponsFA18EFG.STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Red,
        )
        STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Green = (
            10,
            WeaponsFA18EFG.STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Green,
        )
        STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Blue = (
            10,
            WeaponsFA18EFG.STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Blue,
        )
        STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Yellow = (
            10,
            WeaponsFA18EFG.STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Yellow,
        )
        STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Orange = (
            10,
            WeaponsFA18EFG.STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Orange,
        )

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.PinpointStrike,
        task.CAS,
        task.GroundAttack,
        task.RunwayAttack,
        task.SEAD,
        task.AFAC,
        task.AntishipStrike,
        task.Reconnaissance,
    ]
    task_default = task.CAP


@planemod
class EA_18G(PlaneType):
    id = "EA-18G"
    flyable = True
    height = 4.88
    width = 13.62456
    length = 18.31
    fuel_max = 4900
    max_speed = 2120.04
    chaff = 60
    flare = 60
    charge_total = 120
    chaff_charge_size = 1
    flare_charge_size = 1
    eplrs = True
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 305

    panel_radio = {
        1: {
            "channels": {
                1: 305,
                2: 264,
                4: 256,
                8: 257,
                16: 261,
                17: 267,
                9: 255,
                18: 251,
                5: 254,
                10: 262,
                20: 266,
                11: 259,
                3: 265,
                6: 250,
                12: 268,
                13: 269,
                7: 270,
                14: 260,
                19: 253,
                15: 263,
            },
        },
        2: {
            "channels": {
                1: 305,
                2: 264,
                4: 256,
                8: 257,
                16: 261,
                17: 267,
                9: 255,
                18: 251,
                5: 254,
                10: 262,
                20: 266,
                11: 259,
                3: 265,
                6: 250,
                12: 268,
                13: 269,
                7: 270,
                14: 260,
                19: 253,
                15: 263,
            },
        },
    }

    callnames: Dict[str, List[str]] = {
        "USA": [
            "Hornet",
            "Squid",
            "Ragin",
            "Roman",
            "Sting",
            "Jury",
            "Joker",
            "Ram",
            "Hawk",
            "Devil",
            "Check",
            "Snake",
        ]
    }

    property_defaults: Dict[str, Any] = {
        "SoloFlight": False,
        "AIRCRAFT_ID_SEQ": 0,
        "USA_FLAG": False,
        "BlockIIIEquip": True,
        "HelmetMountedDevice": 1,
        "HelmetMountedDeviceWSO": 1,
        "RemoveLOutboard": False,
        "RemoveLMidboard": False,
        "RemoveLInboard": False,
        "RemoveRInboard": False,
        "RemoveRMidboard": False,
        "RemoveROutboard": False,
        "OuterBoard": 0,
        "InnerBoard": 0,
        "DYNAMIC_BORTS_MODE": 0,
        "DYNAMIC_BUNOS": False,
        "DYNAMIC_BUNO_01": 10,
        "DYNAMIC_BUNO_02": 10,
        "DYNAMIC_BUNO_03": 10,
        "DYNAMIC_BUNO_04": 10,
        "DYNAMIC_BUNO_05": 10,
        "DYNAMIC_BUNO_06": 10,
    }

    class Properties:

        class SoloFlight:
            id = "SoloFlight"

        class AIRCRAFT_ID_SEQ:
            id = "AIRCRAFT_ID_SEQ"

            class Values:
                Norm = 0
                Pattern_0A = 1
                Pattern_1B = 2
                Pattern_2C = 3
                Pattern_3D = 4
                Pattern_4E = 5
                Pattern_5F = 6

        class USA_FLAG:
            id = "USA_FLAG"

        class BlockIIIEquip:
            id = "BlockIIIEquip"

        class HelmetMountedDevice:
            id = "HelmetMountedDevice"

            class Values:
                Not_installed = 0
                JHMCS = 1
                NVG = 2

        class HelmetMountedDeviceWSO:
            id = "HelmetMountedDeviceWSO"

            class Values:
                Not_installed = 0
                JHMCS = 1
                NVG = 2

        class RemoveLOutboard:
            id = "RemoveLOutboard"

        class RemoveLMidboard:
            id = "RemoveLMidboard"

        class RemoveLInboard:
            id = "RemoveLInboard"

        class RemoveRInboard:
            id = "RemoveRInboard"

        class RemoveRMidboard:
            id = "RemoveRMidboard"

        class RemoveROutboard:
            id = "RemoveROutboard"

        class OuterBoard:
            id = "OuterBoard"

            class Values:
                Single = 0
                Ripple = 1

        class InnerBoard:
            id = "InnerBoard"

            class Values:
                Single = 0
                Ripple = 1

        class DYNAMIC_BORTS_MODE:
            id = "DYNAMIC_BORTS_MODE"

            class Values:
                DISABLED___NONE = 0
                USN_STANDARD = 1
                RAAF_FIGHTER = 2
                RAAF_GROWLER = 3
                KAF_LEGACY = 4
                KAF_SUPER_HORNET = 5

        class DYNAMIC_BUNOS:
            id = "DYNAMIC_BUNOS"

        class DYNAMIC_BUNO_01:
            id = "DYNAMIC_BUNO_01"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_02:
            id = "DYNAMIC_BUNO_02"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_03:
            id = "DYNAMIC_BUNO_03"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_04:
            id = "DYNAMIC_BUNO_04"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_05:
            id = "DYNAMIC_BUNO_05"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_06:
            id = "DYNAMIC_BUNO_06"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

    properties = {
        "SoloFlight": UnitPropertyDescription(
            identifier="SoloFlight",
            control="comboList",
            label="Solo Flight (Remove WSO)",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "False",
                1: "True",
            },
        ),
        "USA_FLAG": UnitPropertyDescription(
            identifier="USA_FLAG",
            control="comboList",
            label="Hood Displayed USA Flag",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "False",
                1: "True",
            },
        ),
        "BlockIIIEquip": UnitPropertyDescription(
            identifier="BlockIIIEquip",
            control="comboList",
            label="Block III Antennas (Cosmetic)",
            player_only=False,
            default=1,
            w_ctrl=150,
            values={
                0: "False",
                1: "True",
            },
        ),
        "HelmetMountedDevice": UnitPropertyDescription(
            identifier="HelmetMountedDevice",
            control="comboList",
            label="Helmet Mounted Device",
            player_only=True,
            default=1,
            w_ctrl=150,
            values={
                0: "Not installed",
                1: "JHMCS",
                2: "NVG",
            },
        ),
        "HelmetMountedDeviceWSO": UnitPropertyDescription(
            identifier="HelmetMountedDeviceWSO",
            control="comboList",
            label="WSO Helmet Mounted Device",
            player_only=True,
            default=1,
            w_ctrl=150,
            values={
                0: "Not installed",
                1: "JHMCS",
                2: "NVG",
            },
        ),
        "RemoveLOutboard": UnitPropertyDescription(
            identifier="RemoveLOutboard",
            control="comboList",
            label="Dismount STA 2 SUU-80A Pylon (Left Outboard)",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "False",
                1: "True",
            },
        ),
        "RemoveLMidboard": UnitPropertyDescription(
            identifier="RemoveLMidboard",
            control="comboList",
            label="Dismount STA 3 SUU-79A Pylon (Left Midboard)",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "False",
                1: "True",
            },
        ),
        "RemoveLInboard": UnitPropertyDescription(
            identifier="RemoveLMidboard",
            control="comboList",
            label="Dismount STA 4 SUU-79A Pylon (Left Inboard)",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "False",
                1: "True",
            },
        ),
        "RemoveRInboard": UnitPropertyDescription(
            identifier="RemoveRInboard",
            control="comboList",
            label="Dismount STA 8 SUU-79A Pylon (Right Inboard)",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "False",
                1: "True",
            },
        ),
        "RemoveRMidboard": UnitPropertyDescription(
            identifier="RemoveRInboard",
            control="comboList",
            label="Dismount STA 9 SUU-79A Pylon (Right Midboard)",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "False",
                1: "True",
            },
        ),
        "RemoveROutboard": UnitPropertyDescription(
            identifier="RemoveROutboard",
            control="comboList",
            label="Dismount STA 10 SUU-80A Pylon (Right Outboard)",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "False",
                1: "True",
            },
        ),
        "OuterBoard": UnitPropertyDescription(
            identifier="OuterBoard",
            control="comboList",
            label="Outerboard rockets mode",
            player_only=True,
            default=0,
            w_ctrl=150,
            values={
                0: "Single",
                1: "Ripple",
            },
        ),
        "InnerBoard": UnitPropertyDescription(
            identifier="InnerBoard",
            control="comboList",
            label="Innerboard rockets mode",
            player_only=True,
            default=0,
            w_ctrl=150,
            values={
                0: "Single",
                1: "Ripple",
            },
        ),
        "datalink_Label": UnitPropertyDescription(
            identifier="datalink_Label",
            control="label",
            label="DATALINK",
            player_only=False,
            x_lbl=150,
        ),
        "VoiceCallsignLabel": UnitPropertyDescription(
            identifier="VoiceCallsignLabel",
            control="editbox",
            label="Voice Callsign Label",
            player_only=False,
        ),
        "VoiceCallsignNumber": UnitPropertyDescription(
            identifier="VoiceCallsignNumber",
            control="editbox",
            label="Voice Callsign Number",
            player_only=False,
        ),
        "STN_L16": UnitPropertyDescription(
            identifier="STN_L16",
            control="editbox",
            label="STN",
            player_only=False,
        ),
    }

    livery_name = "EA-18G"  # from livery_entry

    class Pylon1:
        STA_02_SUU80_LA127_1x_AIM_9M_Sidewinder_IR_AAM_ = (
            1,
            WeaponsFA18EFG.STA_02_SUU80_LA127_1x_AIM_9M_Sidewinder_IR_AAM_,
        )
        STA_02_SUU80_LA127_1x_AIM_9X_Sidewinder_IR_AAM_ = (
            1,
            WeaponsFA18EFG.STA_02_SUU80_LA127_1x_AIM_9X_Sidewinder_IR_AAM_,
        )
        STA_03_SUU79_BRU32_1x_AN_ALQ_99_ICAP_III_High_Band_Jamming_Pod = (
            1,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_AN_ALQ_99_ICAP_III_High_Band_Jamming_Pod,
        )
        STA_03_SUU79_BRU32_1x_AN_ALQ_249_Mid_Band_Next_Generation_Jamming_Pod = (
            1,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_AN_ALQ_249_Mid_Band_Next_Generation_Jamming_Pod,
        )
        STA_02_SUU80_LA127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X_ = (
            1,
            WeaponsFA18EFG.STA_02_SUU80_LA127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X_,
        )

    # ERRR <CLEAN>

    class Pylon2:
        STA_02_SUU80_LA118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LA118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        STA_02_SUU80_LA115_1x_AIM_7M_Sparrow_Semi_Active_Radar = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LA115_1x_AIM_7M_Sparrow_Semi_Active_Radar,
        )
        STA_02_SUU80_LA127_1x_AIM_9M_Sidewinder_IR_AAM = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LA127_1x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_02_SUU80_LA127_1x_AIM_9X_Sidewinder_IR_AAM = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LA127_1x_AIM_9X_Sidewinder_IR_AAM,
        )
        # ERRR {GROWLER_PYLON_02_OB_Sw_1X_CATM-9M}
        STA_02_SUU80_LA127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LA127_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_02_SUU80_LA127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LA127_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_02_SUU80_LA127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LA127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_02_SUU80_LA127_1x_AN_ASQ_T50_V_1_TCTS_Pod = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LA127_1x_AN_ASQ_T50_V_1_TCTS_Pod,
        )
        STA_03_SUU79_LA127_1x_AIM_9M_Sidewinder_IR_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LA127_1x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_03_SUU79_LA127_1x_AIM_9X_Sidewinder_IR_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LA127_1x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_03_SUU79_LA127_2x_AIM_9M_Sidewinder_IR_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LA127_2x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_03_SUU79_LA127_2x_AIM_9X_Sidewinder_IR_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LA127_2x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_03_SUU79_LA127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LA127_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_03_SUU79_LA127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LA127_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_03_SUU79_LA127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LA127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_03_SUU79_LA127_2x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LA127_2x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_03_SUU79_LA127_2x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LA127_2x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_03_SUU79_LA127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LA127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_03_SUU79_LA118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LA118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        STA_03_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank,
        )
        STA_02_SUU80_LA127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LA127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X,
        )

    # ERRR <CLEAN>

    class Pylon3:
        STA_04_SUU79_LA127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LA127_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_04_SUU79_LA127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LA127_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_04_SUU79_LA127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LA127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_04_SUU79_LA127_2x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LA127_2x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_04_SUU79_LA127_2x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LA127_2x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_04_SUU79_LA127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LA127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_04_SUU79_LA127_1x_AIM_9M_Sidewinder_IR_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LA127_1x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_04_SUU79_LA127_2x_AIM_9M_Sidewinder_IR_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LA127_2x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_04_SUU79_LA127_1x_AIM_9X_Sidewinder_IR_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LA127_1x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_04_SUU79_LA127_2x_AIM_9X_Sidewinder_IR_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LA127_2x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_04_SUU79_LA127_1x_Captive_AIM_9M_for_ACM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LA127_1x_Captive_AIM_9M_for_ACM,
        )
        STA_04_SUU79_LA127_2x_Captive_AIM_9M_for_ACM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LA127_2x_Captive_AIM_9M_for_ACM,
        )
        STA_04_SUU80_LA118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_LA118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        STA_04_SUU79_BRU32_1x_AGM_154A___JSOW_CEB__CBU_type_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_1x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        STA_04_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        STA_04_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        STA_04_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_04_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_04_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_04_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank,
        )
        STA_04_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis,
        )

    # ERRR <CLEAN>

    class Pylon4:
        STA_05_LA116_LA116_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            4,
            WeaponsFA18EFG.STA_05_LA116_LA116_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_05_LA116_LA116_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            4,
            WeaponsFA18EFG.STA_05_LA116_LA116_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_05_LA116_LA116_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            4,
            WeaponsFA18EFG.STA_05_LA116_LA116_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_05_LA116_LA116_1x_AIM_7M_Sparrow_Semi_Active_Radar = (
            4,
            WeaponsFA18EFG.STA_05_LA116_LA116_1x_AIM_7M_Sparrow_Semi_Active_Radar,
        )
        STA_05_LA116_LA116_1x_AIM_7F_Sparrow_Semi_Active_Radar = (
            4,
            WeaponsFA18EFG.STA_05_LA116_LA116_1x_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        STA_05_LA116_LA116_1x_AIM_7MH_Sparrow_Semi_Active_Radar = (
            4,
            WeaponsFA18EFG.STA_05_LA116_LA116_1x_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        STA_05_LA116_LA116_1x_AIM_7P_Sparrow_Semi_Active_Radar = (
            4,
            WeaponsFA18EFG.STA_05_LA116_LA116_1x_AIM_7P_Sparrow_Semi_Active_Radar,
        )
        STA_05_LA116_TPMNT_1x_AN_ASQ_228_ATFLIR___Targeting_Pod = (
            4,
            WeaponsFA18EFG.STA_05_LA116_TPMNT_1x_AN_ASQ_228_ATFLIR___Targeting_Pod,
        )
        STA_05_LA116_LA116_Empty_AIM_7_120_Ejectors = (
            4,
            WeaponsFA18EFG.STA_05_LA116_LA116_Empty_AIM_7_120_Ejectors,
        )
        # ERRR <CLEAN>
        AIM_7F_Sparrow_Semi_Active_Radar = (4, Weapons.AIM_7F_Sparrow_Semi_Active_Radar)
        AIM_7MH_Sparrow_Semi_Active_Radar = (
            4,
            Weapons.AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        AIM_7P_Sparrow_Semi_Active_Radar = (4, Weapons.AIM_7P_Sparrow_Semi_Active_Radar)

    class Pylon5:
        STA_06_SUU78_BRU32_1x_FPU_12_A_Fuel_Tank = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_FPU_12_A_Fuel_Tank,
        )
        STA_06_SUU78_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis,
        )
        STA_06_SUU78_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod,
        )
        STA_06_SUU78_BRU32_1x_AN_ALQ_99_ICAP_III_Low_Band_Jamming_Pod = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_AN_ALQ_99_ICAP_III_Low_Band_Jamming_Pod,
        )
        STA_06_SUU78_EMPTY_ = (5, WeaponsFA18EFG.STA_06_SUU78_EMPTY_)

    # ERRR <CLEAN>

    class Pylon6:
        STA_07_LA116_LA116_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            6,
            WeaponsFA18EFG.STA_07_LA116_LA116_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_07_LA116_LA116_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            6,
            WeaponsFA18EFG.STA_07_LA116_LA116_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_07_LA116_LA116_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            6,
            WeaponsFA18EFG.STA_07_LA116_LA116_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_07_LA116_LA116_1x_AIM_7M_Sparrow_Semi_Active_Radar = (
            6,
            WeaponsFA18EFG.STA_07_LA116_LA116_1x_AIM_7M_Sparrow_Semi_Active_Radar,
        )
        STA_07_LA116_LA116_1x_AIM_7F_Sparrow_Semi_Active_Radar = (
            6,
            WeaponsFA18EFG.STA_07_LA116_LA116_1x_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        STA_07_LA116_LA116_1x_AIM_7MH_Sparrow_Semi_Active_Radar = (
            6,
            WeaponsFA18EFG.STA_07_LA116_LA116_1x_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        STA_07_LA116_LA116_1x_AIM_7P_Sparrow_Semi_Active_Radar = (
            6,
            WeaponsFA18EFG.STA_07_LA116_LA116_1x_AIM_7P_Sparrow_Semi_Active_Radar,
        )
        AIM_7F_Sparrow_Semi_Active_Radar = (6, Weapons.AIM_7F_Sparrow_Semi_Active_Radar)
        AIM_7MH_Sparrow_Semi_Active_Radar = (
            6,
            Weapons.AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        AIM_7P_Sparrow_Semi_Active_Radar = (6, Weapons.AIM_7P_Sparrow_Semi_Active_Radar)
        STA_05_LA116_LA116_Empty_AIM_7_120_Ejectors = (
            6,
            WeaponsFA18EFG.STA_05_LA116_LA116_Empty_AIM_7_120_Ejectors,
        )

    # ERRR <CLEAN>

    class Pylon7:
        STA_08_SUU79_LA127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LA127_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_08_SUU79_LA127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LA127_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_08_SUU79_LA127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LA127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_08_SUU79_LA127_2x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LA127_2x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_08_SUU79_LA127_2x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LA127_2x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_08_SUU79_LA127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LA127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_08_SUU79_LA127_1x_AIM_9M_Sidewinder_IR_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LA127_1x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_08_SUU79_LA127_2x_AIM_9M_Sidewinder_IR_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LA127_2x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_08_SUU79_LA127_1x_AIM_9X_Sidewinder_IR_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LA127_1x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_08_SUU79_LA127_2x_AIM_9X_Sidewinder_IR_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LA127_2x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_08_SUU79_LA127_1x_Captive_AIM_9M_for_ACM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LA127_1x_Captive_AIM_9M_for_ACM,
        )
        STA_08_SUU79_LA127_2x_Captive_AIM_9M_for_ACM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LA127_2x_Captive_AIM_9M_for_ACM,
        )
        STA_08_SUU80_LA118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_LA118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        STA_08_SUU79_BRU32_1x_AGM_154A___JSOW_CEB__CBU_type_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        STA_08_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        STA_08_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        STA_08_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_08_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_08_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_04_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank_ = (
            7,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank_,
        )
        STA_04_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis_ = (
            7,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis_,
        )

    # ERRR <CLEAN>

    class Pylon8:
        STA_10_SUU80_LA118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LA118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        STA_10_SUU80_LA115_1x_AIM_7M_Sparrow_Semi_Active_Radar = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LA115_1x_AIM_7M_Sparrow_Semi_Active_Radar,
        )
        STA_10_SUU80_LA127_1x_AIM_9M_Sidewinder_IR_AAM_ = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LA127_1x_AIM_9M_Sidewinder_IR_AAM_,
        )
        STA_10_SUU80_LA127_1x_AIM_9X_Sidewinder_IR_AAM_ = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LA127_1x_AIM_9X_Sidewinder_IR_AAM_,
        )
        # ERRR {GROWLER_PYLON_10_OB_Sw_1X_CATM-9M}
        STA_10_SUU80_LA127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LA127_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_10_SUU80_LA127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LA127_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_10_SUU80_LA127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LA127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_10_SUU80_LA127_1x_AN_ASQ_T50_V_1_TCTS_Pod = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LA127_1x_AN_ASQ_T50_V_1_TCTS_Pod,
        )
        STA_09_SUU79_LA127_1x_AIM_9M_Sidewinder_IR_AAM = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LA127_1x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_09_SUU79_LA127_1x_AIM_9X_Sidewinder_IR_AAM = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LA127_1x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_09_SUU79_LA127_2x_AIM_9M_Sidewinder_IR_AAM = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LA127_2x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_09_SUU79_LA127_2x_AIM_9X_Sidewinder_IR_AAM = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LA127_2x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_09_SUU79_LA127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LA127_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_09_SUU79_LA127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LA127_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_09_SUU79_LA127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LA127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_09_SUU79_LA127_2x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LA127_2x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_09_SUU79_LA127_2x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LA127_2x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_09_SUU79_LA127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LA127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_09_SUU79_LA118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LA118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        STA_09_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank,
        )
        STA_10_SUU80_LA127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X_ = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LA127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X_,
        )

    # ERRR <CLEAN>

    class Pylon9:
        STA_10_SUU80_LA127_1x_AIM_9M_Sidewinder_IR_AAM = (
            9,
            WeaponsFA18EFG.STA_10_SUU80_LA127_1x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_10_SUU80_LA127_1x_AIM_9X_Sidewinder_IR_AAM = (
            9,
            WeaponsFA18EFG.STA_10_SUU80_LA127_1x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_09_SUU79_BRU32_1x_AN_ALQ_99_ICAP_III_High_Band_Jamming_Pod = (
            9,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_AN_ALQ_99_ICAP_III_High_Band_Jamming_Pod,
        )
        STA_09_SUU79_BRU32_1x_AN_ALQ_249_Mid_Band_Next_Generation_Jamming_Pod = (
            9,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_AN_ALQ_249_Mid_Band_Next_Generation_Jamming_Pod,
        )
        STA_10_SUU80_LA127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X = (
            9,
            WeaponsFA18EFG.STA_10_SUU80_LA127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X,
        )

    # ERRR <CLEAN>

    class Pylon10:
        STA_AX_FUEL_CELLS_1x_Internal_Auxillary_Fuel_Cells = (
            10,
            WeaponsFA18EFG.STA_AX_FUEL_CELLS_1x_Internal_Auxillary_Fuel_Cells,
        )

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.PinpointStrike,
        task.CAS,
        task.GroundAttack,
        task.RunwayAttack,
        task.SEAD,
        task.AFAC,
        task.AntishipStrike,
        task.Reconnaissance,
    ]
    task_default = task.CAP


@planemod
class FA_18ET(PlaneType):
    id = "FA-18ET"
    group_size_max = 1
    height = 4.88
    width = 13.62456
    length = 18.31
    fuel_max = 13154
    max_speed = 2120.04
    chaff = 60
    flare = 60
    charge_total = 120
    chaff_charge_size = 1
    flare_charge_size = 1
    tacan = True
    eplrs = True
    category = "Tankers"  # {8A302789-A55D-4897-B647-66493FA6826F}
    radio_frequency = 305

    panel_radio = {
        1: {
            "channels": {
                1: 305,
                2: 264,
                4: 256,
                8: 257,
                16: 261,
                17: 267,
                9: 255,
                18: 251,
                5: 254,
                10: 262,
                20: 266,
                11: 259,
                3: 265,
                6: 250,
                12: 268,
                13: 269,
                7: 270,
                14: 260,
                19: 253,
                15: 263,
            },
        },
        2: {
            "channels": {
                1: 305,
                2: 264,
                4: 256,
                8: 257,
                16: 261,
                17: 267,
                9: 255,
                18: 251,
                5: 254,
                10: 262,
                20: 266,
                11: 259,
                3: 265,
                6: 250,
                12: 268,
                13: 269,
                7: 270,
                14: 260,
                19: 253,
                15: 263,
            },
        },
    }

    callnames: Dict[str, List[str]] = {
        "USA": [
            "Hornet",
            "Squid",
            "Ragin",
            "Roman",
            "Sting",
            "Jury",
            "Joker",
            "Ram",
            "Hawk",
            "Devil",
            "Check",
            "Snake",
        ]
    }

    property_defaults: Dict[str, Any] = {
        "AIRCRAFT_ID_SEQ": 0,
        "USA_FLAG": False,
        "BlockIIIEquip": True,
        "HelmetMountedDevice": 1,
        "DYNAMIC_BORTS_MODE": 0,
        "DYNAMIC_BUNOS": False,
        "DYNAMIC_BUNO_01": 10,
        "DYNAMIC_BUNO_02": 10,
        "DYNAMIC_BUNO_03": 10,
        "DYNAMIC_BUNO_04": 10,
        "DYNAMIC_BUNO_05": 10,
        "DYNAMIC_BUNO_06": 10,
    }

    class Properties:

        class AIRCRAFT_ID_SEQ:
            id = "AIRCRAFT_ID_SEQ"

            class Values:
                Norm = 0
                Pattern_0A = 1
                Pattern_1B = 2
                Pattern_2C = 3
                Pattern_3D = 4
                Pattern_4E = 5
                Pattern_5F = 6

        class USA_FLAG:
            id = "USA_FLAG"

        class BlockIIIEquip:
            id = "BlockIIIEquip"

        class HelmetMountedDevice:
            id = "HelmetMountedDevice"

            class Values:
                Not_installed = 0
                JHMCS = 1
                NVG = 2

        class DYNAMIC_BORTS_MODE:
            id = "DYNAMIC_BORTS_MODE"

            class Values:
                DISABLED___NONE = 0
                USN_STANDARD = 1
                RAAF_FIGHTER = 2
                RAAF_GROWLER = 3
                KAF_LEGACY = 4
                KAF_SUPER_HORNET = 5

        class DYNAMIC_BUNOS:
            id = "DYNAMIC_BUNOS"

        class DYNAMIC_BUNO_01:
            id = "DYNAMIC_BUNO_01"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_02:
            id = "DYNAMIC_BUNO_02"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_03:
            id = "DYNAMIC_BUNO_03"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_04:
            id = "DYNAMIC_BUNO_04"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_05:
            id = "DYNAMIC_BUNO_05"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_06:
            id = "DYNAMIC_BUNO_06"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

    properties = {
        "USA_FLAG": UnitPropertyDescription(
            identifier="USA_FLAG",
            control="comboList",
            label="Hood Displayed USA Flag",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "False",
                1: "True",
            },
        ),
        "BlockIIIEquip": UnitPropertyDescription(
            identifier="BlockIIIEquip",
            control="comboList",
            label="Block III Antennas (Cosmetic)",
            player_only=False,
            default=1,
            w_ctrl=150,
            values={
                0: "False",
                1: "True",
            },
        ),
        "HelmetMountedDevice": UnitPropertyDescription(
            identifier="HelmetMountedDevice",
            control="comboList",
            label="Helmet Mounted Device",
            player_only=True,
            default=1,
            w_ctrl=150,
            values={
                0: "Not installed",
                1: "JHMCS",
                2: "NVG",
            },
        ),
        "datalink_Label": UnitPropertyDescription(
            identifier="datalink_Label",
            control="label",
            label="DATALINK",
            player_only=False,
            x_lbl=150,
        ),
        "VoiceCallsignLabel": UnitPropertyDescription(
            identifier="VoiceCallsignLabel",
            control="editbox",
            label="Voice Callsign Label",
            player_only=False,
        ),
        "VoiceCallsignNumber": UnitPropertyDescription(
            identifier="VoiceCallsignNumber",
            control="editbox",
            label="Voice Callsign Number",
            player_only=False,
        ),
        "STN_L16": UnitPropertyDescription(
            identifier="STN_L16",
            control="editbox",
            label="STN",
            player_only=False,
        ),
    }

    livery_name = "FA-18E"  # from livery_entry

    class Pylon1:
        STA_01_WNGTP_LAU127_1x_AIM_9M_Sidewinder_IR_AAM = (
            1,
            WeaponsFA18EFG.STA_01_WNGTP_LAU127_1x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_01_WNGTP_LAU127_1x_AIM_9X_Sidewinder_IR_AAM = (
            1,
            WeaponsFA18EFG.STA_01_WNGTP_LAU127_1x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_01_WNGTP_LAU127_1x_Captive_AIM_9M_for_ACM = (
            1,
            WeaponsFA18EFG.STA_01_WNGTP_LAU127_1x_Captive_AIM_9M_for_ACM,
        )
        STA_01_WNGTP_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod = (
            1,
            WeaponsFA18EFG.STA_01_WNGTP_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod,
        )

    class Pylon2:
        STA_02_SUU80_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar,
        )
        STA_02_SUU80_LAU127_1x_AIM_9M_Sidewinder_IR_AAM = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_02_SUU80_LAU127_1x_AIM_9X_Sidewinder_IR_AAM = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_02_SUU80_LAU127_1x_Captive_AIM_9M_for_ACM = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_Captive_AIM_9M_for_ACM,
        )
        STA_02_SUU80_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod,
        )
        STA_02_SUU80_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_02_SUU80_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_02_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_02_SUU80_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        STA_02_SUU80_LAU117_1x_AGM_65F___Maverick_F__IIR_ = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU117_1x_AGM_65F___Maverick_F__IIR_,
        )
        STA_02_SUU80_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only,
        )
        STA_02_SUU80_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        STA_02_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_02_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_02_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        STA_02_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_02_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_02_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_02_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_02_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        STA_02_SUU80_BRU32_1x_GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        STA_02_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_02_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb,
        )
        STA_02_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb,
        )
        STA_02_SUU80_BRU32_1x_CBU_99___490lbs__247_x_HEAT_Bomblets = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        STA_03_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar,
        )
        STA_03_SUU79_LAU115_1x_AIM_7F_Sparrow_Semi_Active_Radar = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU115_1x_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        STA_03_SUU79_LAU115_1x_AIM_7MH_Sparrow_Semi_Active_Radar = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU115_1x_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        STA_03_SUU79_LAU115_1x_AIM_7P_Sparrow_Semi_Active_Radar = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU115_1x_AIM_7P_Sparrow_Semi_Active_Radar,
        )
        STA_03_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_03_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_03_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_03_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_03_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_03_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_03_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_03_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_03_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM,
        )
        STA_03_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_03_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_03_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM,
        )
        STA_03_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        STA_03_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only,
        )
        STA_03_SUU79_BRU32_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        STA_03_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_03_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_03_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_03_SUU79_BRU42_1x_ADM_141A_TALD_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU42_1x_ADM_141A_TALD_,
        )
        STA_03_SUU79_BRU42_2x_ADM_141A_TALD_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU42_2x_ADM_141A_TALD_,
        )
        STA_03_SUU79_BRU42_3x_ADM_141A_TALD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU42_3x_ADM_141A_TALD,
        )
        STA_03_SUU79_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_03_SUU79_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_03_SUU79_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_03_SUU79_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_03_SUU79_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        # ERRR {SUPERHORNET_PYLON_02_MB_MK_BR55_1X_GBU-38}
        STA_03_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_03_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        STA_03_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_03_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_03_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_03_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_02_03_79_80_LAU127_1x_1x_AIM_9M_Sidewinder_IR_AAM = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_1x_1x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_02_03_79_80_LAU127_1x_1x_AIM_9X_Sidewinder_IR_AAM = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_1x_1x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_02_03_79_80_LAU127_1x_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_1x_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_02_03_79_80_LAU127_1x_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_1x_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_02_03_79_80_LAU127_1x_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_1x_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_03_02_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_02_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_03_02_79_80_BRU32_2x_GBU_16___1000lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_02_79_80_BRU32_2x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_03_02_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_02_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_03_02_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_03_02_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_03_02_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            2,
            WeaponsFA18EFG.STA_03_02_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_03_02_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_03_02_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_03_02_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            2,
            WeaponsFA18EFG.STA_03_02_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_04_02_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_04_02_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_04_02_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_04_02_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        # ERRR {SUPERHORNET_PYLON_02_MB_MK_BR55_1X_GBU-32V}
        # ERRR {SUPERHORNET_PYLON_02_MB_MK_BR55_2X_GBU-32V}
        STA_04_02_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_04_02_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_04_02_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            2,
            WeaponsFA18EFG.STA_04_02_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_04_02_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_04_02_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_04_02_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            2,
            WeaponsFA18EFG.STA_04_02_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_02_SUU80_LAU127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X,
        )
        STA_02_SUU80_EMPTY = (2, WeaponsFA18EFG.STA_02_SUU80_EMPTY)
        # ERRR <CLEAN>
        # ERRR {CATM-120C}
        # ERRR {CATM-9M}
        # ERRR {CATM-9X}
        LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar = (
            2,
            Weapons.LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar = (
            2,
            Weapons.LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7P_Sparrow_Semi_Active_Radar = (
            2,
            Weapons.LAU_115C_with_AIM_7P_Sparrow_Semi_Active_Radar,
        )
        LAU_117_AGM_65F = (2, Weapons.LAU_117_AGM_65F)
        BRU_42_with_ADM_141A_TALD = (2, Weapons.BRU_42_with_ADM_141A_TALD)
        BRU_42_with_2_x_ADM_141A_TALD = (2, Weapons.BRU_42_with_2_x_ADM_141A_TALD)
        BRU_42_with_3_x_ADM_141A_TALD = (2, Weapons.BRU_42_with_3_x_ADM_141A_TALD)
        BDU_45___500lb_Practice_Bomb = (2, Weapons.BDU_45___500lb_Practice_Bomb)
        BDU_45B___500lb_Practice_Bomb = (2, Weapons.BDU_45B___500lb_Practice_Bomb)
        GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            2,
            Weapons.GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            2,
            Weapons.GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            2,
            Weapons.Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        CBU_99___490lbs__247_x_HEAT_Bomblets = (
            2,
            Weapons.CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            2,
            Weapons.BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )

    class Pylon3:
        STA_02_SUU79_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod = (
            3,
            WeaponsFA18EFG.STA_02_SUU79_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod,
        )
        STA_03_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar_,
        )
        STA_03_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM_,
        )
        STA_03_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM_,
        )
        STA_03_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only__,
        )
        STA_03_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM_,
        )
        STA_03_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM_,
        )
        STA_03_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only__,
        )
        STA_03_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM_,
        )
        STA_03_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM_,
        )
        STA_03_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM_,
        )
        STA_03_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM_,
        )
        STA_03_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM_,
        )
        STA_03_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM_,
        )
        STA_03_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank,
        )
        STA_03_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis,
        )
        STA_03_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod,
        )
        STA_03_SUU79_BRU32_1x_ALQ_167_Countermeasures_System = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_ALQ_167_Countermeasures_System,
        )
        STA_03_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd__,
        )
        STA_03_SUU79_LAU117_1x_AGM_65F___Maverick_F__IIR__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_AGM_65F___Maverick_F__IIR__,
        )
        STA_03_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only_,
        )
        STA_03_SUU79_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        STA_03_SUU79_LAU117_1x_AGM_84D_Harpoon_Anti_Ship_Missile = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_AGM_84D_Harpoon_Anti_Ship_Missile,
        )
        STA_03_SUU79_LAU117_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        STA_03_SUU79_LAU117_1x_AGM_84H_SLAM_ER__Expanded_Response_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_AGM_84H_SLAM_ER__Expanded_Response_,
        )
        STA_03_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH_,
        )
        STA_03_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH_,
        )
        STA_03_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH_,
        )
        STA_03_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        STA_03_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        STA_03_SUU79_BRU32_1x_Mk_82___500lb_GP_Bomb_LD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_82___500lb_GP_Bomb_LD_,
        )
        STA_03_SUU79_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD_,
        )
        STA_03_SUU79_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD_,
        )
        STA_03_SUU79_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD_,
        )
        STA_03_SUU79_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD_,
        )
        STA_03_SUU79_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb_,
        )
        STA_03_SUU79_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb_,
        )
        STA_03_SUU79_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb_,
        )
        STA_03_SUU79_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb_,
        )
        STA_03_SUU79_BRU32_1x_GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb_,
        )
        # ERRR {SUPERHORNET_PYLON_03_MB_MK_1X_GBU-32V}
        STA_03_SUU79_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets_,
        )
        STA_03_SUU79_BRU32_1x_BDU_45___500lb_Practice_Bomb = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_BDU_45___500lb_Practice_Bomb,
        )
        STA_03_SUU79_BRU32_1x_BDU_45B___500lb_Practice_Bomb = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_BDU_45B___500lb_Practice_Bomb,
        )
        STA_03_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb_,
        )
        STA_03_SUU79_BRU33_2x_BDU_45___500lb_Practice_Bomb = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_BDU_45___500lb_Practice_Bomb,
        )
        STA_03_SUU79_BRU33_2x_BDU_45B___500lb_Practice_Bomb = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_BDU_45B___500lb_Practice_Bomb,
        )
        STA_03_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD_,
        )
        STA_03_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        STA_03_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD_,
        )
        STA_03_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD_,
        )
        # ERRR {SUPERHORNET_PYLON_03_MB_MK_BR2_ROCKEYE}
        STA_03_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb_,
        )
        STA_03_SUU79_BRU41_6x_BDU_33___25lb_Practice_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU41_6x_BDU_33___25lb_Practice_Bomb_LD,
        )
        STA_04_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar,
        )
        STA_04_SUU79_LAU115_1x_AIM_7F_Sparrow_Semi_Active_Radar = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU115_1x_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        STA_04_SUU79_LAU115_1x_AIM_7MH_Sparrow_Semi_Active_Radar = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU115_1x_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        STA_04_SUU79_LAU115_1x_AIM_7P_Sparrow_Semi_Active_Radar = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU115_1x_AIM_7P_Sparrow_Semi_Active_Radar,
        )
        STA_04_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_04_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_04_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM,
        )
        STA_04_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_04_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_04_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM,
        )
        STA_04_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_04_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_04_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_04_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_04_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_04_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_04_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank,
        )
        STA_04_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis,
        )
        # ERRR {SUPERHORNET_PYLON_03_IB_PD_1X_ALQ-167}
        STA_04_SUU79_BRU32_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        STA_04_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        STA_03_SUU79_BRU42_1x_ADM_141A_TALD__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU42_1x_ADM_141A_TALD__,
        )
        STA_03_SUU79_BRU42_2x_ADM_141A_TALD__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU42_2x_ADM_141A_TALD__,
        )
        STA_03_SUU79_BRU42_3x_ADM_141A_TALD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU42_3x_ADM_141A_TALD_,
        )
        STA_04_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only,
        )
        STA_04_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_04_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_04_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_04_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_04_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_04_SUU80_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_04_SUU80_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        STA_04_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_04_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_04_SUU80_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        STA_04_SUU80_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_04_SUU80_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_04_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_04_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_04_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_04_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_04_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        STA_04_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_04_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        # ERRR {SUPERHORNET_PYLON_03_IB_MK_BR2_ROCKEYE}
        STA_04_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_04_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        STA_04_03_79_80_BRU32_1x_1x_AGM_154C___JSOW_Unitary_BROACH = (
            3,
            WeaponsFA18EFG.STA_04_03_79_80_BRU32_1x_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_04_03_SUU79_BRU32_1x_1x_GBU_10___2000lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        STA_04_03_SUU79_BRU32_1x_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_04_03_SUU79_BRU32_1x_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_04_03_SUU79_BRU32_1x_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        STA_04_03_SUU79_BRU32_1x_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_04_03_SUU79_BRU32_1x_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_04_03_SUU79_BRU32_1x_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_04_03_SUU79_BRU32_1x_1x_Mk_82___500lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_04_03_SUU79_BRU32_1x_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_04_03_SUU79_BRU32_1x_1x_Mk_83___1000lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_04_03_SUU79_BRU32_1x_1x_Mk_84___2000lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_04_03_SUU79_BRU32_1x_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_03_SUU79_EMPTY = (3, WeaponsFA18EFG.STA_03_SUU79_EMPTY)
        # ERRR <CLEAN>
        # ERRR LAU-115_2*LAU-127_CATM-120C
        # ERRR LAU_117_TGM_65E
        # ERRR LAU_117_TGM_65F
        LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar = (
            3,
            Weapons.LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar = (
            3,
            Weapons.LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7P_Sparrow_Semi_Active_Radar = (
            3,
            Weapons.LAU_115C_with_AIM_7P_Sparrow_Semi_Active_Radar,
        )
        LAU_117_AGM_65F = (3, Weapons.LAU_117_AGM_65F)
        AGM_84H_SLAM_ER__Expanded_Response_ = (
            3,
            Weapons.AGM_84H_SLAM_ER__Expanded_Response_,
        )
        AGM_84D_Harpoon_AShM = (3, Weapons.AGM_84D_Harpoon_AShM)
        BRU_42_with_ADM_141A_TALD = (3, Weapons.BRU_42_with_ADM_141A_TALD)
        BRU_42_with_2_x_ADM_141A_TALD = (3, Weapons.BRU_42_with_2_x_ADM_141A_TALD)
        BRU_42_with_3_x_ADM_141A_TALD = (3, Weapons.BRU_42_with_3_x_ADM_141A_TALD)
        AGM_154A___JSOW_CEB__CBU_type_ = (3, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_ = (
            3,
            Weapons.BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        BDU_45___500lb_Practice_Bomb = (3, Weapons.BDU_45___500lb_Practice_Bomb)
        BDU_45B___500lb_Practice_Bomb = (3, Weapons.BDU_45B___500lb_Practice_Bomb)
        GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            Weapons.GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            3,
            Weapons.GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            3,
            Weapons.GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            3,
            Weapons.GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            3,
            Weapons.Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            3,
            Weapons.BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        CBU_99___490lbs__247_x_HEAT_Bomblets = (
            3,
            Weapons.CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            3,
            Weapons.BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        AWW_13_DATALINK_POD = (3, Weapons.AWW_13_DATALINK_POD)

    class Pylon4:
        STA_05_CHEEK__LAU116_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_05_CHEEK__LAU116_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_05_CHEEK__LAU116_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_05_CHEEK__LAU116_1x_AIM_7M_Sparrow_Semi_Active_Radar = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_7M_Sparrow_Semi_Active_Radar,
        )
        STA_05_CHEEK__LAU116_1x_AIM_7F_Sparrow_Semi_Active_Radar = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        STA_05_CHEEK__LAU116_1x_AIM_7MH_Sparrow_Semi_Active_Radar = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        STA_05_CHEEK__LAU116_1x_AIM_7P_Sparrow_Semi_Active_Radar = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_7P_Sparrow_Semi_Active_Radar,
        )
        STA_05_CHEEK__TGPMNT_1x_AN_ASQ_228_ATFLIR___Targeting_Pod = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__TGPMNT_1x_AN_ASQ_228_ATFLIR___Targeting_Pod,
        )
        STA_04_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank_ = (
            4,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank_,
        )
        STA_04_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis_ = (
            4,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis_,
        )
        AWW_13_DATALINK_POD = (4, Weapons.AWW_13_DATALINK_POD)
        STA_04_SUU79_BRU32_Remove_SUU_79A_A_Pylon = (
            4,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_Remove_SUU_79A_A_Pylon,
        )
        STA_05_CHEEK__TGPMNT_Empty_TGP_Mount = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__TGPMNT_Empty_TGP_Mount,
        )
        STA_05_CHEEK__LAU116_Empty_AIM_7_120_Ejectors = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_Empty_AIM_7_120_Ejectors,
        )
        # ERRR <CLEAN>
        AIM_7F_Sparrow_Semi_Active_Radar = (4, Weapons.AIM_7F_Sparrow_Semi_Active_Radar)
        AIM_7MH_Sparrow_Semi_Active_Radar = (
            4,
            Weapons.AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        AIM_7P_Sparrow_Semi_Active_Radar = (4, Weapons.AIM_7P_Sparrow_Semi_Active_Radar)
        AN_ASQ_228_ATFLIR___Targeting_Pod = (
            4,
            Weapons.AN_ASQ_228_ATFLIR___Targeting_Pod,
        )

    class Pylon5:
        STA_06_SUU78_BRU32_1x_FPU_12_A_Fuel_Tank = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_FPU_12_A_Fuel_Tank,
        )
        STA_06_SUU78_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis,
        )
        STA_06_SUU78_BRU32_1x_A_A_42R_1_Aerial_Refueling_Buddy_Pod = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_A_A_42R_1_Aerial_Refueling_Buddy_Pod,
        )
        STA_06_SUU78_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod,
        )
        STA_06_SUU78_BRU32_1x_AN_AAQ_28_LITENING___Targeting_Pod = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_AN_AAQ_28_LITENING___Targeting_Pod,
        )
        STA_06_SUU78_EMPTY = (5, WeaponsFA18EFG.STA_06_SUU78_EMPTY)
        # ERRR <CLEAN>
        AWW_13_DATALINK_POD = (5, Weapons.AWW_13_DATALINK_POD)
        AN_AAQ_28_LITENING___Targeting_Pod_ = (
            5,
            Weapons.AN_AAQ_28_LITENING___Targeting_Pod_,
        )

    class Pylon6:
        STA_07_CHEEK__LAU116_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_07_CHEEK__LAU116_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_07_CHEEK__LAU116_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_07_CHEEK__LAU116_1x_AIM_7M_Sparrow_Semi_Active_Radar = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_7M_Sparrow_Semi_Active_Radar,
        )
        STA_07_CHEEK__LAU116_1x_AIM_7F_Sparrow_Semi_Active_Radar = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        STA_07_CHEEK__LAU116_1x_AIM_7MH_Sparrow_Semi_Active_Radar = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        STA_07_CHEEK__LAU116_1x_AIM_7P_Sparrow_Semi_Active_Radar = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_7P_Sparrow_Semi_Active_Radar,
        )
        STA_08_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank = (
            6,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank,
        )
        STA_08_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis = (
            6,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis,
        )
        STA_08_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod = (
            6,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod,
        )
        STA_07_SUU79_BRU32_Remove_SUU_79A_A_Pylon = (
            6,
            WeaponsFA18EFG.STA_07_SUU79_BRU32_Remove_SUU_79A_A_Pylon,
        )
        STA_08_SUU79_EMPTY = (6, WeaponsFA18EFG.STA_08_SUU79_EMPTY)
        STA_08_SUU79_LAU127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X = (
            6,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X,
        )
        # ERRR <CLEAN>
        AIM_7F_Sparrow_Semi_Active_Radar = (6, Weapons.AIM_7F_Sparrow_Semi_Active_Radar)
        AIM_7MH_Sparrow_Semi_Active_Radar = (
            6,
            Weapons.AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        AIM_7P_Sparrow_Semi_Active_Radar = (6, Weapons.AIM_7P_Sparrow_Semi_Active_Radar)
        AWW_13_DATALINK_POD = (6, Weapons.AWW_13_DATALINK_POD)

    class Pylon7:
        STA_09_SUU79_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod,
        )
        STA_09_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar,
        )
        STA_09_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_09_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_09_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_09_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_09_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_09_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_09_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_09_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_09_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM,
        )
        STA_09_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_09_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_09_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM,
        )
        STA_09_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank,
        )
        STA_09_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis,
        )
        STA_09_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod,
        )
        STA_09_SUU79_BRU32_1x_ALQ_167_Countermeasures_System = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_ALQ_167_Countermeasures_System,
        )
        STA_09_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        STA_09_SUU79_LAU117_1x_AGM_65F___Maverick_F__IIR_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_AGM_65F___Maverick_F__IIR_,
        )
        STA_09_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only,
        )
        STA_09_SUU79_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        STA_09_SUU79_LAU117_1x_AGM_84D_Harpoon_Anti_Ship_Missile = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_AGM_84D_Harpoon_Anti_Ship_Missile,
        )
        STA_09_SUU79_LAU117_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        STA_09_SUU79_LAU117_1x_AGM_84H_SLAM_ER__Expanded_Response_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_AGM_84H_SLAM_ER__Expanded_Response_,
        )
        STA_09_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_09_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_09_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_09_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        STA_09_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        STA_09_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_09_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_09_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        STA_09_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_09_SUU80_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_09_SUU80_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        STA_09_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_09_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_09_SUU80_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        STA_09_SUU80_BRU32_1x_GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_09_SUU80_BRU32_1x_GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        STA_09_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_09_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        STA_09_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_09_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb,
        )
        STA_09_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb,
        )
        STA_09_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_09_SUU79_BRU33_2x_BDU_45___500lb_Practice_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_BDU_45___500lb_Practice_Bomb,
        )
        STA_09_SUU79_BRU33_2x_BDU_45B___500lb_Practice_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_BDU_45B___500lb_Practice_Bomb,
        )
        STA_09_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_09_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        STA_09_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_09_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        # ERRR {SUPERHORNET_PYLON_09_MB_MK_BR2_ROCKEYE}
        STA_09_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_09_SUU79_BRU41_6x_BDU_33___25lb_Practice_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU41_6x_BDU_33___25lb_Practice_Bomb_LD,
        )
        STA_08_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar,
        )
        STA_08_SUU79_LAU115_1x_AIM_7F_Sparrow_Semi_Active_Radar = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU115_1x_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        STA_08_SUU79_LAU115_1x_AIM_7MH_Sparrow_Semi_Active_Radar = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU115_1x_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        STA_08_SUU79_LAU115_1x_AIM_7P_Sparrow_Semi_Active_Radar = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU115_1x_AIM_7P_Sparrow_Semi_Active_Radar,
        )
        STA_08_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_08_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_08_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM,
        )
        STA_08_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_08_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_08_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM,
        )
        STA_08_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_08_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_08_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_08_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_08_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_08_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_08_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank_,
        )
        STA_08_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis_,
        )
        # ERRR {SUPERHORNET_PYLON_09_IB_PD_1X_ALQ-167}
        # ERRR {SUPERHORNET_PYLON_09_IB_PD_1X_ALQ-167}
        STA_08_SUU79_BRU32_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        STA_08_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        STA_08_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only,
        )
        STA_08_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_08_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_08_SUU79_BRU42_1x_ADM_141A_TALD = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU42_1x_ADM_141A_TALD,
        )
        STA_08_SUU79_BRU42_2x_ADM_141A_TALD = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU42_2x_ADM_141A_TALD,
        )
        STA_08_SUU79_BRU42_3x_ADM_141A_TALD = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU42_3x_ADM_141A_TALD,
        )
        STA_08_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_08_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_08_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_08_SUU80_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_08_SUU80_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        STA_08_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_08_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_08_SUU80_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        STA_08_SUU80_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_08_SUU80_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_08_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_08_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_08_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_08_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_08_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        STA_08_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_08_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        # ERRR {SUPERHORNET_PYLON_09_IB_MK_BR2_ROCKEYE}
        STA_08_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_08_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        STA_08_09_SUU79_BRU32_1x_1x_AGM_154C___JSOW_Unitary_BROACH = (
            7,
            WeaponsFA18EFG.STA_08_09_SUU79_BRU32_1x_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_09_08_SUU79_BRU32_1x_1x_GBU_10___2000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        STA_09_08_SUU79_BRU32_1x_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_09_08_SUU79_BRU32_1x_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_09_08_SUU79_BRU32_1x_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        STA_09_08_SUU79_BRU32_1x_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_09_08_SUU79_BRU32_1x_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_09_08_SUU79_BRU32_1x_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_09_08_SUU79_BRU32_1x_1x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_09_08_SUU79_BRU32_1x_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_09_08_SUU79_BRU32_1x_1x_Mk_83___1000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_09_08_SUU79_BRU32_1x_1x_Mk_84___2000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_09_08_SUU79_BRU32_1x_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_09_SUU79_EMPTY = (7, WeaponsFA18EFG.STA_09_SUU79_EMPTY)
        # ERRR <CLEAN>
        # ERRR LAU-115_2*LAU-127_CATM-120C
        # ERRR LAU_117_TGM_65E
        # ERRR LAU_117_TGM_65F
        LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar = (
            7,
            Weapons.LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar = (
            7,
            Weapons.LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7P_Sparrow_Semi_Active_Radar = (
            7,
            Weapons.LAU_115C_with_AIM_7P_Sparrow_Semi_Active_Radar,
        )
        LAU_117_AGM_65F = (7, Weapons.LAU_117_AGM_65F)
        AGM_84H_SLAM_ER__Expanded_Response_ = (
            7,
            Weapons.AGM_84H_SLAM_ER__Expanded_Response_,
        )
        AGM_84D_Harpoon_AShM = (7, Weapons.AGM_84D_Harpoon_AShM)
        BRU_42_with_ADM_141A_TALD = (7, Weapons.BRU_42_with_ADM_141A_TALD)
        BRU_42_with_2_x_ADM_141A_TALD = (7, Weapons.BRU_42_with_2_x_ADM_141A_TALD)
        BRU_42_with_3_x_ADM_141A_TALD = (7, Weapons.BRU_42_with_3_x_ADM_141A_TALD)
        AGM_154A___JSOW_CEB__CBU_type_ = (7, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_ = (
            7,
            Weapons.BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        BDU_45___500lb_Practice_Bomb = (7, Weapons.BDU_45___500lb_Practice_Bomb)
        BDU_45B___500lb_Practice_Bomb = (7, Weapons.BDU_45B___500lb_Practice_Bomb)
        GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            Weapons.GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            7,
            Weapons.GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            7,
            Weapons.GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            7,
            Weapons.GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            7,
            Weapons.Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            7,
            Weapons.BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            7,
            Weapons.BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        AWW_13_DATALINK_POD = (7, Weapons.AWW_13_DATALINK_POD)

    class Pylon8:
        STA_10_SUU80_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar,
        )
        STA_10_SUU80_LAU127_1x_AIM_9M_Sidewinder_IR_AAM = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_10_SUU80_LAU127_1x_AIM_9X_Sidewinder_IR_AAM = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_10_SUU80_LAU127_1x_Captive_AIM_9M_for_ACM = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_Captive_AIM_9M_for_ACM,
        )
        STA_10_SUU80_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod,
        )
        STA_10_SUU80_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_10_SUU80_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_10_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_10_SUU80_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        STA_10_SUU80_LAU117_1x_AGM_65F___Maverick_F__IIR_ = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU117_1x_AGM_65F___Maverick_F__IIR_,
        )
        STA_10_SUU80_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only,
        )
        STA_10_SUU80_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        STA_10_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_10_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_10_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        STA_10_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_10_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_10_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_10_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_10_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        STA_10_SUU80_BRU32_1x_GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        STA_10_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_10_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb,
        )
        STA_10_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb,
        )
        STA_10_SUU80_BRU32_1x_CBU_99___490lbs__247_x_HEAT_Bomblets = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        STA_09_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar_,
        )
        STA_09_SUU79_LAU115_1x_AIM_7F_Sparrow_Semi_Active_Radar_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU115_1x_AIM_7F_Sparrow_Semi_Active_Radar_,
        )
        STA_09_SUU79_LAU115_1x_AIM_7MH_Sparrow_Semi_Active_Radar_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU115_1x_AIM_7MH_Sparrow_Semi_Active_Radar_,
        )
        STA_09_SUU79_LAU115_1x_AIM_7P_Sparrow_Semi_Active_Radar_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU115_1x_AIM_7P_Sparrow_Semi_Active_Radar_,
        )
        STA_09_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM_,
        )
        STA_09_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM_,
        )
        STA_09_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only__,
        )
        STA_09_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM_,
        )
        STA_09_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM_,
        )
        STA_09_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only__,
        )
        STA_09_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM_,
        )
        STA_09_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM_,
        )
        STA_09_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM_,
        )
        STA_09_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM_,
        )
        STA_09_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM_,
        )
        STA_09_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM_,
        )
        STA_09_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd__,
        )
        STA_09_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only_,
        )
        STA_09_SUU79_LAU117_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile__,
        )
        STA_09_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH_,
        )
        STA_09_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH_,
        )
        STA_09_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH_,
        )
        STA_09_SUU79_BRU42_1x_ADM_141A_TALD_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU42_1x_ADM_141A_TALD_,
        )
        STA_09_SUU79_BRU42_2x_ADM_141A_TALD_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU42_2x_ADM_141A_TALD_,
        )
        STA_09_SUU79_BRU42_3x_ADM_141A_TALD = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU42_3x_ADM_141A_TALD,
        )
        STA_09_SUU79_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_09_SUU79_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_09_SUU79_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_09_SUU79_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_09_SUU79_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        STA_09_SUU79_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_09_SUU79_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_09_SUU79_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        STA_09_SUU79_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_09_SUU79_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_09_SUU79_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_09_SUU79_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_09_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb_,
        )
        STA_09_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        STA_09_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD_,
        )
        STA_09_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD_,
        )
        STA_09_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD_,
        )
        STA_09_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb_,
        )
        STA_09_10_79_80_LAU127_1x_1x_AIM_9M_Sidewinder_IR_AAM = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_1x_1x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_09_10_79_80_LAU127_1x_1x_AIM_9X_Sidewinder_IR_AAM = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_1x_1x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_09_10_79_80_LAU127_1x_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_1x_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_09_10_79_80_LAU127_1x_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_1x_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_09_10_79_80_LAU127_1x_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_1x_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_09_10_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_09_10_79_80_BRU32_2x_GBU_16___1000lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_BRU32_2x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_09_10_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_09_10_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_09_10_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_09_10_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_09_10_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_10_08_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_08_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_10_08_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_08_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_10_08_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_10_08_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_10_08_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            8,
            WeaponsFA18EFG.STA_10_08_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_10_08_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_10_08_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_10_08_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            8,
            WeaponsFA18EFG.STA_10_08_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_10_SUU80_LAU127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X,
        )
        STA_10_SUU80_EMPTY = (8, WeaponsFA18EFG.STA_10_SUU80_EMPTY)
        # ERRR <CLEAN>
        # ERRR {CATM-120C}
        # ERRR {CATM-9M}
        # ERRR {CATM-9X}
        LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar = (
            8,
            Weapons.LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar = (
            8,
            Weapons.LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7P_Sparrow_Semi_Active_Radar = (
            8,
            Weapons.LAU_115C_with_AIM_7P_Sparrow_Semi_Active_Radar,
        )
        LAU_117_AGM_65F = (8, Weapons.LAU_117_AGM_65F)
        BRU_42_with_ADM_141A_TALD = (8, Weapons.BRU_42_with_ADM_141A_TALD)
        BRU_42_with_2_x_ADM_141A_TALD = (8, Weapons.BRU_42_with_2_x_ADM_141A_TALD)
        BRU_42_with_3_x_ADM_141A_TALD = (8, Weapons.BRU_42_with_3_x_ADM_141A_TALD)
        BDU_45___500lb_Practice_Bomb = (8, Weapons.BDU_45___500lb_Practice_Bomb)
        BDU_45B___500lb_Practice_Bomb = (8, Weapons.BDU_45B___500lb_Practice_Bomb)
        GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            8,
            Weapons.GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            8,
            Weapons.GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            8,
            Weapons.Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        CBU_99___490lbs__247_x_HEAT_Bomblets = (
            8,
            Weapons.CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            8,
            Weapons.BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )

    class Pylon9:
        STA_11_WNGTP_LAU127_1x_AIM_9M_Sidewinder_IR_AAM = (
            9,
            WeaponsFA18EFG.STA_11_WNGTP_LAU127_1x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_11_WNGTP_LAU127_1x_AIM_9X_Sidewinder_IR_AAM = (
            9,
            WeaponsFA18EFG.STA_11_WNGTP_LAU127_1x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_11_WNGTP_LAU127_1x_Captive_AIM_9M_for_ACM = (
            9,
            WeaponsFA18EFG.STA_11_WNGTP_LAU127_1x_Captive_AIM_9M_for_ACM,
        )
        STA_11_WNGTP_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod = (
            9,
            WeaponsFA18EFG.STA_11_WNGTP_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod,
        )

    class Pylon10:
        STA_AX_FUEL_CELLS_1x_Internal_Auxillary_Fuel_Cells = (
            10,
            WeaponsFA18EFG.STA_AX_FUEL_CELLS_1x_Internal_Auxillary_Fuel_Cells,
        )
        STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___White = (
            10,
            WeaponsFA18EFG.STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___White,
        )
        STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Red = (
            10,
            WeaponsFA18EFG.STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Red,
        )
        STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Green = (
            10,
            WeaponsFA18EFG.STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Green,
        )
        STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Blue = (
            10,
            WeaponsFA18EFG.STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Blue,
        )
        STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Yellow = (
            10,
            WeaponsFA18EFG.STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Yellow,
        )
        STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Orange = (
            10,
            WeaponsFA18EFG.STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Orange,
        )

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

    tasks = [task.Refueling]
    task_default = task.Refueling


@planemod
class FA_18FT(PlaneType):
    id = "FA-18FT"
    group_size_max = 1
    height = 4.88
    width = 13.62456
    length = 18.31
    fuel_max = 13154
    max_speed = 2120.04
    chaff = 60
    flare = 60
    charge_total = 120
    chaff_charge_size = 1
    flare_charge_size = 1
    tacan = True
    eplrs = True
    category = "Tankers"  # {8A302789-A55D-4897-B647-66493FA6826F}
    radio_frequency = 305

    panel_radio = {
        1: {
            "channels": {
                1: 305,
                2: 264,
                4: 256,
                8: 257,
                16: 261,
                17: 267,
                9: 255,
                18: 251,
                5: 254,
                10: 262,
                20: 266,
                11: 259,
                3: 265,
                6: 250,
                12: 268,
                13: 269,
                7: 270,
                14: 260,
                19: 253,
                15: 263,
            },
        },
        2: {
            "channels": {
                1: 305,
                2: 264,
                4: 256,
                8: 257,
                16: 261,
                17: 267,
                9: 255,
                18: 251,
                5: 254,
                10: 262,
                20: 266,
                11: 259,
                3: 265,
                6: 250,
                12: 268,
                13: 269,
                7: 270,
                14: 260,
                19: 253,
                15: 263,
            },
        },
    }

    callnames: Dict[str, List[str]] = {
        "USA": [
            "Hornet",
            "Squid",
            "Ragin",
            "Roman",
            "Sting",
            "Jury",
            "Joker",
            "Ram",
            "Hawk",
            "Devil",
            "Check",
            "Snake",
        ]
    }

    property_defaults: Dict[str, Any] = {
        "AIRCRAFT_ID_SEQ": 0,
        "USA_FLAG": False,
        "BlockIIIEquip": True,
        "HelmetMountedDevice": 1,
        "DYNAMIC_BORTS_MODE": 0,
        "DYNAMIC_BUNOS": False,
        "DYNAMIC_BUNO_01": 10,
        "DYNAMIC_BUNO_02": 10,
        "DYNAMIC_BUNO_03": 10,
        "DYNAMIC_BUNO_04": 10,
        "DYNAMIC_BUNO_05": 10,
        "DYNAMIC_BUNO_06": 10,
    }

    class Properties:

        class AIRCRAFT_ID_SEQ:
            id = "AIRCRAFT_ID_SEQ"

            class Values:
                Norm = 0
                Pattern_0A = 1
                Pattern_1B = 2
                Pattern_2C = 3
                Pattern_3D = 4
                Pattern_4E = 5
                Pattern_5F = 6

        class USA_FLAG:
            id = "USA_FLAG"

        class BlockIIIEquip:
            id = "BlockIIIEquip"

        class HelmetMountedDevice:
            id = "HelmetMountedDevice"

            class Values:
                Not_installed = 0
                JHMCS = 1
                NVG = 2

        class DYNAMIC_BORTS_MODE:
            id = "DYNAMIC_BORTS_MODE"

            class Values:
                DISABLED___NONE = 0
                USN_STANDARD = 1
                RAAF_FIGHTER = 2
                RAAF_GROWLER = 3
                KAF_LEGACY = 4
                KAF_SUPER_HORNET = 5

        class DYNAMIC_BUNOS:
            id = "DYNAMIC_BUNOS"

        class DYNAMIC_BUNO_01:
            id = "DYNAMIC_BUNO_01"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_02:
            id = "DYNAMIC_BUNO_02"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_03:
            id = "DYNAMIC_BUNO_03"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_04:
            id = "DYNAMIC_BUNO_04"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_05:
            id = "DYNAMIC_BUNO_05"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

        class DYNAMIC_BUNO_06:
            id = "DYNAMIC_BUNO_06"

            class Values:
                x_1 = 0
                x_2 = 1
                x_3 = 2
                x_4 = 3
                x_5 = 4
                x_6 = 5
                x_7 = 6
                x_8 = 7
                x_9 = 8
                x_0 = 9
                Blank = 10

    properties = {
        "USA_FLAG": UnitPropertyDescription(
            identifier="USA_FLAG",
            control="comboList",
            label="Hood Displayed USA Flag",
            player_only=False,
            default=0,
            w_ctrl=150,
            values={
                0: "False",
                1: "True",
            },
        ),
        "BlockIIIEquip": UnitPropertyDescription(
            identifier="BlockIIIEquip",
            control="comboList",
            label="Block III Antennas (Cosmetic)",
            player_only=False,
            default=1,
            w_ctrl=150,
            values={
                0: "False",
                1: "True",
            },
        ),
        "HelmetMountedDevice": UnitPropertyDescription(
            identifier="HelmetMountedDevice",
            control="comboList",
            label="Helmet Mounted Device",
            player_only=True,
            default=1,
            w_ctrl=150,
            values={
                0: "Not installed",
                1: "JHMCS",
                2: "NVG",
            },
        ),
        "datalink_Label": UnitPropertyDescription(
            identifier="datalink_Label",
            control="label",
            label="DATALINK",
            player_only=False,
            x_lbl=150,
        ),
        "VoiceCallsignLabel": UnitPropertyDescription(
            identifier="VoiceCallsignLabel",
            control="editbox",
            label="Voice Callsign Label",
            player_only=False,
        ),
        "VoiceCallsignNumber": UnitPropertyDescription(
            identifier="VoiceCallsignNumber",
            control="editbox",
            label="Voice Callsign Number",
            player_only=False,
        ),
        "STN_L16": UnitPropertyDescription(
            identifier="STN_L16",
            control="editbox",
            label="STN",
            player_only=False,
        ),
    }

    livery_name = "FA-18F"  # from livery_entry

    class Pylon1:
        STA_01_WNGTP_LAU127_1x_AIM_9M_Sidewinder_IR_AAM = (
            1,
            WeaponsFA18EFG.STA_01_WNGTP_LAU127_1x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_01_WNGTP_LAU127_1x_AIM_9X_Sidewinder_IR_AAM = (
            1,
            WeaponsFA18EFG.STA_01_WNGTP_LAU127_1x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_01_WNGTP_LAU127_1x_Captive_AIM_9M_for_ACM = (
            1,
            WeaponsFA18EFG.STA_01_WNGTP_LAU127_1x_Captive_AIM_9M_for_ACM,
        )
        STA_01_WNGTP_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod = (
            1,
            WeaponsFA18EFG.STA_01_WNGTP_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod,
        )

    class Pylon2:
        STA_02_SUU80_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar,
        )
        STA_02_SUU80_LAU127_1x_AIM_9M_Sidewinder_IR_AAM = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_02_SUU80_LAU127_1x_AIM_9X_Sidewinder_IR_AAM = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_02_SUU80_LAU127_1x_Captive_AIM_9M_for_ACM = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_Captive_AIM_9M_for_ACM,
        )
        STA_02_SUU80_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod,
        )
        STA_02_SUU80_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_02_SUU80_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_02_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_02_SUU80_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        STA_02_SUU80_LAU117_1x_AGM_65F___Maverick_F__IIR_ = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU117_1x_AGM_65F___Maverick_F__IIR_,
        )
        STA_02_SUU80_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only,
        )
        STA_02_SUU80_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        STA_02_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_02_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_02_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        STA_02_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_02_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_02_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_02_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_02_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        STA_02_SUU80_BRU32_1x_GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        STA_02_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_02_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb,
        )
        STA_02_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb,
        )
        STA_02_SUU80_BRU32_1x_CBU_99___490lbs__247_x_HEAT_Bomblets = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_BRU32_1x_CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        STA_03_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar,
        )
        STA_03_SUU79_LAU115_1x_AIM_7F_Sparrow_Semi_Active_Radar = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU115_1x_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        STA_03_SUU79_LAU115_1x_AIM_7MH_Sparrow_Semi_Active_Radar = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU115_1x_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        STA_03_SUU79_LAU115_1x_AIM_7P_Sparrow_Semi_Active_Radar = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU115_1x_AIM_7P_Sparrow_Semi_Active_Radar,
        )
        STA_03_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_03_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_03_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_03_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_03_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_03_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_03_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_03_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_03_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM,
        )
        STA_03_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_03_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_03_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM,
        )
        STA_03_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        STA_03_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only,
        )
        STA_03_SUU79_BRU32_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        STA_03_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_03_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_03_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_03_SUU79_BRU42_1x_ADM_141A_TALD_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU42_1x_ADM_141A_TALD_,
        )
        STA_03_SUU79_BRU42_2x_ADM_141A_TALD_ = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU42_2x_ADM_141A_TALD_,
        )
        STA_03_SUU79_BRU42_3x_ADM_141A_TALD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU42_3x_ADM_141A_TALD,
        )
        STA_03_SUU79_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_03_SUU79_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_03_SUU79_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_03_SUU79_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_03_SUU79_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        # ERRR {SUPERHORNET_PYLON_02_MB_MK_BR55_1X_GBU-38}
        STA_03_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_03_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        STA_03_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_03_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_03_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_03_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_02_03_79_80_LAU127_1x_1x_AIM_9M_Sidewinder_IR_AAM = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_1x_1x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_02_03_79_80_LAU127_1x_1x_AIM_9X_Sidewinder_IR_AAM = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_1x_1x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_02_03_79_80_LAU127_1x_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_1x_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_02_03_79_80_LAU127_1x_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_1x_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_02_03_79_80_LAU127_1x_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            2,
            WeaponsFA18EFG.STA_02_03_79_80_LAU127_1x_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_03_02_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_02_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_03_02_79_80_BRU32_2x_GBU_16___1000lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_02_79_80_BRU32_2x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_03_02_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_03_02_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_03_02_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_03_02_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_03_02_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            2,
            WeaponsFA18EFG.STA_03_02_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_03_02_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_03_02_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_03_02_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            2,
            WeaponsFA18EFG.STA_03_02_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_04_02_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_04_02_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_04_02_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            2,
            WeaponsFA18EFG.STA_04_02_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        # ERRR {SUPERHORNET_PYLON_02_MB_MK_BR55_1X_GBU-32V}
        # ERRR {SUPERHORNET_PYLON_02_MB_MK_BR55_2X_GBU-32V}
        STA_04_02_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_04_02_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_04_02_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            2,
            WeaponsFA18EFG.STA_04_02_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_04_02_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD = (
            2,
            WeaponsFA18EFG.STA_04_02_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_04_02_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            2,
            WeaponsFA18EFG.STA_04_02_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_02_SUU80_LAU127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X = (
            2,
            WeaponsFA18EFG.STA_02_SUU80_LAU127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X,
        )
        STA_02_SUU80_EMPTY = (2, WeaponsFA18EFG.STA_02_SUU80_EMPTY)
        # ERRR <CLEAN>
        # ERRR {CATM-120C}
        # ERRR {CATM-9M}
        # ERRR {CATM-9X}
        LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar = (
            2,
            Weapons.LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar = (
            2,
            Weapons.LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7P_Sparrow_Semi_Active_Radar = (
            2,
            Weapons.LAU_115C_with_AIM_7P_Sparrow_Semi_Active_Radar,
        )
        LAU_117_AGM_65F = (2, Weapons.LAU_117_AGM_65F)
        BRU_42_with_ADM_141A_TALD = (2, Weapons.BRU_42_with_ADM_141A_TALD)
        BRU_42_with_2_x_ADM_141A_TALD = (2, Weapons.BRU_42_with_2_x_ADM_141A_TALD)
        BRU_42_with_3_x_ADM_141A_TALD = (2, Weapons.BRU_42_with_3_x_ADM_141A_TALD)
        BDU_45___500lb_Practice_Bomb = (2, Weapons.BDU_45___500lb_Practice_Bomb)
        BDU_45B___500lb_Practice_Bomb = (2, Weapons.BDU_45B___500lb_Practice_Bomb)
        GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            2,
            Weapons.GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            2,
            Weapons.GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            2,
            Weapons.Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        CBU_99___490lbs__247_x_HEAT_Bomblets = (
            2,
            Weapons.CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            2,
            Weapons.BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )

    class Pylon3:
        STA_02_SUU79_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod = (
            3,
            WeaponsFA18EFG.STA_02_SUU79_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod,
        )
        STA_03_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar_,
        )
        STA_03_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM_,
        )
        STA_03_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM_,
        )
        STA_03_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only__,
        )
        STA_03_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM_,
        )
        STA_03_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM_,
        )
        STA_03_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only__,
        )
        STA_03_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM_,
        )
        STA_03_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM_,
        )
        STA_03_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM_,
        )
        STA_03_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM_,
        )
        STA_03_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM_,
        )
        STA_03_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM_,
        )
        STA_03_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank,
        )
        STA_03_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis,
        )
        STA_03_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod,
        )
        STA_03_SUU79_BRU32_1x_ALQ_167_Countermeasures_System = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_ALQ_167_Countermeasures_System,
        )
        STA_03_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd__,
        )
        STA_03_SUU79_LAU117_1x_AGM_65F___Maverick_F__IIR__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_AGM_65F___Maverick_F__IIR__,
        )
        STA_03_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only_,
        )
        STA_03_SUU79_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        STA_03_SUU79_LAU117_1x_AGM_84D_Harpoon_Anti_Ship_Missile = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_AGM_84D_Harpoon_Anti_Ship_Missile,
        )
        STA_03_SUU79_LAU117_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        STA_03_SUU79_LAU117_1x_AGM_84H_SLAM_ER__Expanded_Response_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_LAU117_1x_AGM_84H_SLAM_ER__Expanded_Response_,
        )
        STA_03_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH_,
        )
        STA_03_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH_,
        )
        STA_03_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH_,
        )
        STA_03_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        STA_03_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        STA_03_SUU79_BRU32_1x_Mk_82___500lb_GP_Bomb_LD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_82___500lb_GP_Bomb_LD_,
        )
        STA_03_SUU79_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD_,
        )
        STA_03_SUU79_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD_,
        )
        STA_03_SUU79_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD_,
        )
        STA_03_SUU79_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD_,
        )
        STA_03_SUU79_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb_,
        )
        STA_03_SUU79_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb_,
        )
        STA_03_SUU79_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb_,
        )
        STA_03_SUU79_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb_,
        )
        STA_03_SUU79_BRU32_1x_GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        STA_03_SUU79_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb_,
        )
        # ERRR {SUPERHORNET_PYLON_03_MB_MK_1X_GBU-32V}
        STA_03_SUU79_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets_,
        )
        STA_03_SUU79_BRU32_1x_BDU_45___500lb_Practice_Bomb = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_BDU_45___500lb_Practice_Bomb,
        )
        STA_03_SUU79_BRU32_1x_BDU_45B___500lb_Practice_Bomb = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU32_1x_BDU_45B___500lb_Practice_Bomb,
        )
        STA_03_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb_,
        )
        STA_03_SUU79_BRU33_2x_BDU_45___500lb_Practice_Bomb = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_BDU_45___500lb_Practice_Bomb,
        )
        STA_03_SUU79_BRU33_2x_BDU_45B___500lb_Practice_Bomb = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_BDU_45B___500lb_Practice_Bomb,
        )
        STA_03_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD_,
        )
        STA_03_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        STA_03_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD_,
        )
        STA_03_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD_,
        )
        # ERRR {SUPERHORNET_PYLON_03_MB_MK_BR2_ROCKEYE}
        STA_03_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb_,
        )
        STA_03_SUU79_BRU41_6x_BDU_33___25lb_Practice_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU41_6x_BDU_33___25lb_Practice_Bomb_LD,
        )
        STA_04_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar,
        )
        STA_04_SUU79_LAU115_1x_AIM_7F_Sparrow_Semi_Active_Radar = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU115_1x_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        STA_04_SUU79_LAU115_1x_AIM_7MH_Sparrow_Semi_Active_Radar = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU115_1x_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        STA_04_SUU79_LAU115_1x_AIM_7P_Sparrow_Semi_Active_Radar = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU115_1x_AIM_7P_Sparrow_Semi_Active_Radar,
        )
        STA_04_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_04_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_04_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM,
        )
        STA_04_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_04_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_04_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM,
        )
        STA_04_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_04_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_04_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_04_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_04_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_04_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_04_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank,
        )
        STA_04_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis,
        )
        # ERRR {SUPERHORNET_PYLON_03_IB_PD_1X_ALQ-167}
        STA_04_SUU79_BRU32_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        STA_04_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        STA_03_SUU79_BRU42_1x_ADM_141A_TALD__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU42_1x_ADM_141A_TALD__,
        )
        STA_03_SUU79_BRU42_2x_ADM_141A_TALD__ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU42_2x_ADM_141A_TALD__,
        )
        STA_03_SUU79_BRU42_3x_ADM_141A_TALD_ = (
            3,
            WeaponsFA18EFG.STA_03_SUU79_BRU42_3x_ADM_141A_TALD_,
        )
        STA_04_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only,
        )
        STA_04_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_04_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_04_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_04_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_04_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_04_SUU80_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_04_SUU80_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        STA_04_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_04_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_04_SUU80_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        STA_04_SUU80_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_04_SUU80_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_04_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_04_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            3,
            WeaponsFA18EFG.STA_04_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_04_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_04_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_04_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        STA_04_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_04_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        # ERRR {SUPERHORNET_PYLON_03_IB_MK_BR2_ROCKEYE}
        STA_04_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_04_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        STA_04_03_79_80_BRU32_1x_1x_AGM_154C___JSOW_Unitary_BROACH = (
            3,
            WeaponsFA18EFG.STA_04_03_79_80_BRU32_1x_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_04_03_SUU79_BRU32_1x_1x_GBU_10___2000lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        STA_04_03_SUU79_BRU32_1x_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_04_03_SUU79_BRU32_1x_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_04_03_SUU79_BRU32_1x_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        STA_04_03_SUU79_BRU32_1x_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_04_03_SUU79_BRU32_1x_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_04_03_SUU79_BRU32_1x_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_04_03_SUU79_BRU32_1x_1x_Mk_82___500lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_04_03_SUU79_BRU32_1x_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_04_03_SUU79_BRU32_1x_1x_Mk_83___1000lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_04_03_SUU79_BRU32_1x_1x_Mk_84___2000lb_GP_Bomb_LD = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_04_03_SUU79_BRU32_1x_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            3,
            WeaponsFA18EFG.STA_04_03_SUU79_BRU32_1x_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_03_SUU79_EMPTY = (3, WeaponsFA18EFG.STA_03_SUU79_EMPTY)
        # ERRR <CLEAN>
        # ERRR LAU-115_2*LAU-127_CATM-120C
        # ERRR LAU_117_TGM_65E
        # ERRR LAU_117_TGM_65F
        LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar = (
            3,
            Weapons.LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar = (
            3,
            Weapons.LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7P_Sparrow_Semi_Active_Radar = (
            3,
            Weapons.LAU_115C_with_AIM_7P_Sparrow_Semi_Active_Radar,
        )
        LAU_117_AGM_65F = (3, Weapons.LAU_117_AGM_65F)
        AGM_84H_SLAM_ER__Expanded_Response_ = (
            3,
            Weapons.AGM_84H_SLAM_ER__Expanded_Response_,
        )
        AGM_84D_Harpoon_AShM = (3, Weapons.AGM_84D_Harpoon_AShM)
        BRU_42_with_ADM_141A_TALD = (3, Weapons.BRU_42_with_ADM_141A_TALD)
        BRU_42_with_2_x_ADM_141A_TALD = (3, Weapons.BRU_42_with_2_x_ADM_141A_TALD)
        BRU_42_with_3_x_ADM_141A_TALD = (3, Weapons.BRU_42_with_3_x_ADM_141A_TALD)
        AGM_154A___JSOW_CEB__CBU_type_ = (3, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_ = (
            3,
            Weapons.BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        BDU_45___500lb_Practice_Bomb = (3, Weapons.BDU_45___500lb_Practice_Bomb)
        BDU_45B___500lb_Practice_Bomb = (3, Weapons.BDU_45B___500lb_Practice_Bomb)
        GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            Weapons.GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            3,
            Weapons.GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            3,
            Weapons.GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            3,
            Weapons.GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            3,
            Weapons.Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            3,
            Weapons.BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        CBU_99___490lbs__247_x_HEAT_Bomblets = (
            3,
            Weapons.CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            3,
            Weapons.BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        AWW_13_DATALINK_POD = (3, Weapons.AWW_13_DATALINK_POD)

    class Pylon4:
        STA_05_CHEEK__LAU116_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_05_CHEEK__LAU116_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_05_CHEEK__LAU116_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_05_CHEEK__LAU116_1x_AIM_7M_Sparrow_Semi_Active_Radar = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_7M_Sparrow_Semi_Active_Radar,
        )
        STA_05_CHEEK__LAU116_1x_AIM_7F_Sparrow_Semi_Active_Radar = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        STA_05_CHEEK__LAU116_1x_AIM_7MH_Sparrow_Semi_Active_Radar = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        STA_05_CHEEK__LAU116_1x_AIM_7P_Sparrow_Semi_Active_Radar = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_1x_AIM_7P_Sparrow_Semi_Active_Radar,
        )
        STA_05_CHEEK__TGPMNT_1x_AN_ASQ_228_ATFLIR___Targeting_Pod = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__TGPMNT_1x_AN_ASQ_228_ATFLIR___Targeting_Pod,
        )
        STA_04_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank_ = (
            4,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank_,
        )
        STA_04_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis_ = (
            4,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis_,
        )
        AWW_13_DATALINK_POD = (4, Weapons.AWW_13_DATALINK_POD)
        STA_04_SUU79_BRU32_Remove_SUU_79A_A_Pylon = (
            4,
            WeaponsFA18EFG.STA_04_SUU79_BRU32_Remove_SUU_79A_A_Pylon,
        )
        STA_05_CHEEK__TGPMNT_Empty_TGP_Mount = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__TGPMNT_Empty_TGP_Mount,
        )
        STA_05_CHEEK__LAU116_Empty_AIM_7_120_Ejectors = (
            4,
            WeaponsFA18EFG.STA_05_CHEEK__LAU116_Empty_AIM_7_120_Ejectors,
        )
        # ERRR <CLEAN>
        AIM_7F_Sparrow_Semi_Active_Radar = (4, Weapons.AIM_7F_Sparrow_Semi_Active_Radar)
        AIM_7MH_Sparrow_Semi_Active_Radar = (
            4,
            Weapons.AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        AIM_7P_Sparrow_Semi_Active_Radar = (4, Weapons.AIM_7P_Sparrow_Semi_Active_Radar)
        AN_ASQ_228_ATFLIR___Targeting_Pod = (
            4,
            Weapons.AN_ASQ_228_ATFLIR___Targeting_Pod,
        )

    class Pylon5:
        STA_06_SUU78_BRU32_1x_FPU_12_A_Fuel_Tank = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_FPU_12_A_Fuel_Tank,
        )
        STA_06_SUU78_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis,
        )
        STA_06_SUU78_BRU32_1x_A_A_42R_1_Aerial_Refueling_Buddy_Pod = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_A_A_42R_1_Aerial_Refueling_Buddy_Pod,
        )
        STA_06_SUU78_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod,
        )
        STA_06_SUU78_BRU32_1x_AN_AAQ_28_LITENING___Targeting_Pod = (
            5,
            WeaponsFA18EFG.STA_06_SUU78_BRU32_1x_AN_AAQ_28_LITENING___Targeting_Pod,
        )
        STA_06_SUU78_EMPTY = (5, WeaponsFA18EFG.STA_06_SUU78_EMPTY)
        # ERRR <CLEAN>
        AWW_13_DATALINK_POD = (5, Weapons.AWW_13_DATALINK_POD)
        AN_AAQ_28_LITENING___Targeting_Pod_ = (
            5,
            Weapons.AN_AAQ_28_LITENING___Targeting_Pod_,
        )

    class Pylon6:
        STA_07_CHEEK__LAU116_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_07_CHEEK__LAU116_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_07_CHEEK__LAU116_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_07_CHEEK__LAU116_1x_AIM_7M_Sparrow_Semi_Active_Radar = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_7M_Sparrow_Semi_Active_Radar,
        )
        STA_07_CHEEK__LAU116_1x_AIM_7F_Sparrow_Semi_Active_Radar = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        STA_07_CHEEK__LAU116_1x_AIM_7MH_Sparrow_Semi_Active_Radar = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        STA_07_CHEEK__LAU116_1x_AIM_7P_Sparrow_Semi_Active_Radar = (
            6,
            WeaponsFA18EFG.STA_07_CHEEK__LAU116_1x_AIM_7P_Sparrow_Semi_Active_Radar,
        )
        STA_08_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank = (
            6,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank,
        )
        STA_08_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis = (
            6,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis,
        )
        STA_08_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod = (
            6,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod,
        )
        STA_07_SUU79_BRU32_Remove_SUU_79A_A_Pylon = (
            6,
            WeaponsFA18EFG.STA_07_SUU79_BRU32_Remove_SUU_79A_A_Pylon,
        )
        STA_08_SUU79_EMPTY = (6, WeaponsFA18EFG.STA_08_SUU79_EMPTY)
        STA_08_SUU79_LAU127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X = (
            6,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X,
        )
        # ERRR <CLEAN>
        AIM_7F_Sparrow_Semi_Active_Radar = (6, Weapons.AIM_7F_Sparrow_Semi_Active_Radar)
        AIM_7MH_Sparrow_Semi_Active_Radar = (
            6,
            Weapons.AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        AIM_7P_Sparrow_Semi_Active_Radar = (6, Weapons.AIM_7P_Sparrow_Semi_Active_Radar)
        AWW_13_DATALINK_POD = (6, Weapons.AWW_13_DATALINK_POD)

    class Pylon7:
        STA_09_SUU79_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod,
        )
        STA_09_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar,
        )
        STA_09_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_09_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_09_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_09_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_09_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_09_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_09_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_09_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_09_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM,
        )
        STA_09_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_09_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_09_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM,
        )
        STA_09_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank,
        )
        STA_09_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis,
        )
        STA_09_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_AN_AWW_13_Advanced_Datalink_Pod,
        )
        STA_09_SUU79_BRU32_1x_ALQ_167_Countermeasures_System = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_ALQ_167_Countermeasures_System,
        )
        STA_09_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        STA_09_SUU79_LAU117_1x_AGM_65F___Maverick_F__IIR_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_AGM_65F___Maverick_F__IIR_,
        )
        STA_09_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only,
        )
        STA_09_SUU79_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        STA_09_SUU79_LAU117_1x_AGM_84D_Harpoon_Anti_Ship_Missile = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_AGM_84D_Harpoon_Anti_Ship_Missile,
        )
        STA_09_SUU79_LAU117_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        STA_09_SUU79_LAU117_1x_AGM_84H_SLAM_ER__Expanded_Response_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_AGM_84H_SLAM_ER__Expanded_Response_,
        )
        STA_09_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_09_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_09_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_09_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_1x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        STA_09_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type_ = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_2x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        STA_09_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_09_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_09_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        STA_09_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_09_SUU80_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_09_SUU80_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        STA_09_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_09_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_09_SUU80_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        STA_09_SUU80_BRU32_1x_GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_09_SUU80_BRU32_1x_GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        STA_09_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_09_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        STA_09_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_09_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb,
        )
        STA_09_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb,
        )
        STA_09_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_09_SUU79_BRU33_2x_BDU_45___500lb_Practice_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_BDU_45___500lb_Practice_Bomb,
        )
        STA_09_SUU79_BRU33_2x_BDU_45B___500lb_Practice_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_BDU_45B___500lb_Practice_Bomb,
        )
        STA_09_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_09_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        STA_09_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_09_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        # ERRR {SUPERHORNET_PYLON_09_MB_MK_BR2_ROCKEYE}
        STA_09_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_09_SUU79_BRU41_6x_BDU_33___25lb_Practice_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_SUU79_BRU41_6x_BDU_33___25lb_Practice_Bomb_LD,
        )
        STA_08_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar,
        )
        STA_08_SUU79_LAU115_1x_AIM_7F_Sparrow_Semi_Active_Radar = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU115_1x_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        STA_08_SUU79_LAU115_1x_AIM_7MH_Sparrow_Semi_Active_Radar = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU115_1x_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        STA_08_SUU79_LAU115_1x_AIM_7P_Sparrow_Semi_Active_Radar = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU115_1x_AIM_7P_Sparrow_Semi_Active_Radar,
        )
        STA_08_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_08_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_08_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM,
        )
        STA_08_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_08_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_08_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM,
        )
        STA_08_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_08_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_08_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_08_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_08_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_08_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_08_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank_,
        )
        STA_08_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_FPU_12_A_Fuel_Tank___High_Vis_,
        )
        # ERRR {SUPERHORNET_PYLON_09_IB_PD_1X_ALQ-167}
        # ERRR {SUPERHORNET_PYLON_09_IB_PD_1X_ALQ-167}
        STA_08_SUU79_BRU32_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU32_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        STA_08_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        STA_08_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only,
        )
        STA_08_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_08_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH_ = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_08_SUU79_BRU42_1x_ADM_141A_TALD = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU42_1x_ADM_141A_TALD,
        )
        STA_08_SUU79_BRU42_2x_ADM_141A_TALD = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU42_2x_ADM_141A_TALD,
        )
        STA_08_SUU79_BRU42_3x_ADM_141A_TALD = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU42_3x_ADM_141A_TALD,
        )
        STA_08_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_08_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_08_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_08_SUU80_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_08_SUU80_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        STA_08_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_08_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_08_SUU80_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        STA_08_SUU80_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_08_SUU80_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_08_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_08_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            7,
            WeaponsFA18EFG.STA_08_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_08_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_08_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_08_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU33_2x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        STA_08_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_08_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        # ERRR {SUPERHORNET_PYLON_09_IB_MK_BR2_ROCKEYE}
        STA_08_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_08_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_08_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        STA_08_09_SUU79_BRU32_1x_1x_AGM_154C___JSOW_Unitary_BROACH = (
            7,
            WeaponsFA18EFG.STA_08_09_SUU79_BRU32_1x_1x_AGM_154C___JSOW_Unitary_BROACH,
        )
        STA_09_08_SUU79_BRU32_1x_1x_GBU_10___2000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        STA_09_08_SUU79_BRU32_1x_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_09_08_SUU79_BRU32_1x_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_09_08_SUU79_BRU32_1x_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        STA_09_08_SUU79_BRU32_1x_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_09_08_SUU79_BRU32_1x_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_09_08_SUU79_BRU32_1x_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_09_08_SUU79_BRU32_1x_1x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_09_08_SUU79_BRU32_1x_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_09_08_SUU79_BRU32_1x_1x_Mk_83___1000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_09_08_SUU79_BRU32_1x_1x_Mk_84___2000lb_GP_Bomb_LD = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_09_08_SUU79_BRU32_1x_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            7,
            WeaponsFA18EFG.STA_09_08_SUU79_BRU32_1x_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_09_SUU79_EMPTY = (7, WeaponsFA18EFG.STA_09_SUU79_EMPTY)
        # ERRR <CLEAN>
        # ERRR LAU-115_2*LAU-127_CATM-120C
        # ERRR LAU_117_TGM_65E
        # ERRR LAU_117_TGM_65F
        LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar = (
            7,
            Weapons.LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar = (
            7,
            Weapons.LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7P_Sparrow_Semi_Active_Radar = (
            7,
            Weapons.LAU_115C_with_AIM_7P_Sparrow_Semi_Active_Radar,
        )
        LAU_117_AGM_65F = (7, Weapons.LAU_117_AGM_65F)
        AGM_84H_SLAM_ER__Expanded_Response_ = (
            7,
            Weapons.AGM_84H_SLAM_ER__Expanded_Response_,
        )
        AGM_84D_Harpoon_AShM = (7, Weapons.AGM_84D_Harpoon_AShM)
        BRU_42_with_ADM_141A_TALD = (7, Weapons.BRU_42_with_ADM_141A_TALD)
        BRU_42_with_2_x_ADM_141A_TALD = (7, Weapons.BRU_42_with_2_x_ADM_141A_TALD)
        BRU_42_with_3_x_ADM_141A_TALD = (7, Weapons.BRU_42_with_3_x_ADM_141A_TALD)
        AGM_154A___JSOW_CEB__CBU_type_ = (7, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_ = (
            7,
            Weapons.BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        BDU_45___500lb_Practice_Bomb = (7, Weapons.BDU_45___500lb_Practice_Bomb)
        BDU_45B___500lb_Practice_Bomb = (7, Weapons.BDU_45B___500lb_Practice_Bomb)
        GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            Weapons.GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            7,
            Weapons.GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            7,
            Weapons.GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            7,
            Weapons.GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            7,
            Weapons.Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            7,
            Weapons.BRU_33_with_2_x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            7,
            Weapons.BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        AWW_13_DATALINK_POD = (7, Weapons.AWW_13_DATALINK_POD)

    class Pylon8:
        STA_10_SUU80_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar,
        )
        STA_10_SUU80_LAU127_1x_AIM_9M_Sidewinder_IR_AAM = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_10_SUU80_LAU127_1x_AIM_9X_Sidewinder_IR_AAM = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_10_SUU80_LAU127_1x_Captive_AIM_9M_for_ACM = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_Captive_AIM_9M_for_ACM,
        )
        STA_10_SUU80_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod,
        )
        STA_10_SUU80_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_10_SUU80_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_10_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_10_SUU80_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        STA_10_SUU80_LAU117_1x_AGM_65F___Maverick_F__IIR_ = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU117_1x_AGM_65F___Maverick_F__IIR_,
        )
        STA_10_SUU80_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only,
        )
        STA_10_SUU80_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU118_1x_AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        STA_10_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_10_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_10_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        STA_10_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_10_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_10_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_10_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_10_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        STA_10_SUU80_BRU32_1x_GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        STA_10_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_10_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_BDU_45___500lb_Practice_Bomb,
        )
        STA_10_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_BDU_45B___500lb_Practice_Bomb,
        )
        STA_10_SUU80_BRU32_1x_CBU_99___490lbs__247_x_HEAT_Bomblets = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_BRU32_1x_CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        STA_09_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU115_1x_AIM_7M_Sparrow_Semi_Active_Radar_,
        )
        STA_09_SUU79_LAU115_1x_AIM_7F_Sparrow_Semi_Active_Radar_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU115_1x_AIM_7F_Sparrow_Semi_Active_Radar_,
        )
        STA_09_SUU79_LAU115_1x_AIM_7MH_Sparrow_Semi_Active_Radar_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU115_1x_AIM_7MH_Sparrow_Semi_Active_Radar_,
        )
        STA_09_SUU79_LAU115_1x_AIM_7P_Sparrow_Semi_Active_Radar_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU115_1x_AIM_7P_Sparrow_Semi_Active_Radar_,
        )
        STA_09_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_120B_AMRAAM___Active_Radar_AAM_,
        )
        STA_09_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_120C_AMRAAM___Active_Radar_AAM_,
        )
        STA_09_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only__,
        )
        STA_09_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_120B_AMRAAM___Active_Radar_AAM_,
        )
        STA_09_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_120C_AMRAAM___Active_Radar_AAM_,
        )
        STA_09_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only__,
        )
        STA_09_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_9M_Sidewinder_IR_AAM_,
        )
        STA_09_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_AIM_9X_Sidewinder_IR_AAM_,
        )
        STA_09_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_1x_Captive_AIM_9M_for_ACM_,
        )
        STA_09_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_9M_Sidewinder_IR_AAM_,
        )
        STA_09_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_AIM_9X_Sidewinder_IR_AAM_,
        )
        STA_09_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU127_2x_Captive_AIM_9M_for_ACM_,
        )
        STA_09_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd__,
        )
        STA_09_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___AI_Only_,
        )
        STA_09_SUU79_LAU117_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile__ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_LAU117_1x_AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile__,
        )
        STA_09_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_AGM_154C___JSOW_Unitary_BROACH_,
        )
        STA_09_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_1x_AGM_154C___JSOW_Unitary_BROACH_,
        )
        STA_09_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_2x_AGM_154C___JSOW_Unitary_BROACH_,
        )
        STA_09_SUU79_BRU42_1x_ADM_141A_TALD_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU42_1x_ADM_141A_TALD_,
        )
        STA_09_SUU79_BRU42_2x_ADM_141A_TALD_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU42_2x_ADM_141A_TALD_,
        )
        STA_09_SUU79_BRU42_3x_ADM_141A_TALD = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU42_3x_ADM_141A_TALD,
        )
        STA_09_SUU79_BRU32_1x_Mk_82___500lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_09_SUU79_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_09_SUU79_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_09_SUU79_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_Mk_84___2000lb_GP_Bomb_LD,
        )
        STA_09_SUU79_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        STA_09_SUU79_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_09_SUU79_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_09_SUU79_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        STA_09_SUU79_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_09_SUU79_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        STA_09_SUU79_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_09_SUU79_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU32_1x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_09_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb_,
        )
        STA_09_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU55_2x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        STA_09_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_Mk_82___500lb_GP_Bomb_LD_,
        )
        STA_09_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD_,
        )
        STA_09_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_Mk_83___1000lb_GP_Bomb_LD_,
        )
        STA_09_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb_ = (
            8,
            WeaponsFA18EFG.STA_09_SUU79_BRU33_2x_GBU_12___500lb_Laser_Guided_Bomb_,
        )
        STA_09_10_79_80_LAU127_1x_1x_AIM_9M_Sidewinder_IR_AAM = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_1x_1x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_09_10_79_80_LAU127_1x_1x_AIM_9X_Sidewinder_IR_AAM = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_1x_1x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_09_10_79_80_LAU127_1x_1x_AIM_120B_AMRAAM___Active_Radar_AAM = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_1x_1x_AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        STA_09_10_79_80_LAU127_1x_1x_AIM_120C_AMRAAM___Active_Radar_AAM = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_1x_1x_AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        STA_09_10_79_80_LAU127_1x_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_ = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_LAU127_1x_1x_AIM_120D_AMRAAM___Active_Radar_AAM__AI_Only_,
        )
        STA_09_10_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_09_10_79_80_BRU32_2x_GBU_16___1000lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_BRU32_2x_GBU_16___1000lb_Laser_Guided_Bomb,
        )
        STA_09_10_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_09_10_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_09_10_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_09_10_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_09_10_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            8,
            WeaponsFA18EFG.STA_09_10_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_10_08_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_08_79_80_BRU32_2x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        STA_10_08_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            8,
            WeaponsFA18EFG.STA_10_08_79_80_BRU32_2x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        STA_10_08_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_10_08_79_80_BRU32_2x_Mk_82___500lb_GP_Bomb_LD,
        )
        STA_10_08_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            8,
            WeaponsFA18EFG.STA_10_08_79_80_BRU32_2x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        STA_10_08_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD = (
            8,
            WeaponsFA18EFG.STA_10_08_79_80_BRU32_2x_Mk_83___1000lb_GP_Bomb_LD,
        )
        STA_10_08_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            8,
            WeaponsFA18EFG.STA_10_08_79_80_BRU32_2x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        STA_10_SUU80_LAU127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X = (
            8,
            WeaponsFA18EFG.STA_10_SUU80_LAU127_1x_Marvin_LAU_127_Rail_Launcher_for_AIM_120B_C_D_and_AIM9L_M_X,
        )
        STA_10_SUU80_EMPTY = (8, WeaponsFA18EFG.STA_10_SUU80_EMPTY)
        # ERRR <CLEAN>
        # ERRR {CATM-120C}
        # ERRR {CATM-9M}
        # ERRR {CATM-9X}
        LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar = (
            8,
            Weapons.LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar = (
            8,
            Weapons.LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        LAU_115C_with_AIM_7P_Sparrow_Semi_Active_Radar = (
            8,
            Weapons.LAU_115C_with_AIM_7P_Sparrow_Semi_Active_Radar,
        )
        LAU_117_AGM_65F = (8, Weapons.LAU_117_AGM_65F)
        BRU_42_with_ADM_141A_TALD = (8, Weapons.BRU_42_with_ADM_141A_TALD)
        BRU_42_with_2_x_ADM_141A_TALD = (8, Weapons.BRU_42_with_2_x_ADM_141A_TALD)
        BRU_42_with_3_x_ADM_141A_TALD = (8, Weapons.BRU_42_with_3_x_ADM_141A_TALD)
        BDU_45___500lb_Practice_Bomb = (8, Weapons.BDU_45___500lb_Practice_Bomb)
        BDU_45B___500lb_Practice_Bomb = (8, Weapons.BDU_45B___500lb_Practice_Bomb)
        GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            8,
            Weapons.GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )
        GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD = (
            8,
            Weapons.GBU_54_V_1_B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD,
        )
        Mk_82Y___500lb_GP_Chute_Retarded_HD = (
            8,
            Weapons.Mk_82Y___500lb_GP_Chute_Retarded_HD,
        )
        CBU_99___490lbs__247_x_HEAT_Bomblets = (
            8,
            Weapons.CBU_99___490lbs__247_x_HEAT_Bomblets,
        )
        BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb = (
            8,
            Weapons.BRU_55_with_2_x_GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb,
        )

    class Pylon9:
        STA_11_WNGTP_LAU127_1x_AIM_9M_Sidewinder_IR_AAM = (
            9,
            WeaponsFA18EFG.STA_11_WNGTP_LAU127_1x_AIM_9M_Sidewinder_IR_AAM,
        )
        STA_11_WNGTP_LAU127_1x_AIM_9X_Sidewinder_IR_AAM = (
            9,
            WeaponsFA18EFG.STA_11_WNGTP_LAU127_1x_AIM_9X_Sidewinder_IR_AAM,
        )
        STA_11_WNGTP_LAU127_1x_Captive_AIM_9M_for_ACM = (
            9,
            WeaponsFA18EFG.STA_11_WNGTP_LAU127_1x_Captive_AIM_9M_for_ACM,
        )
        STA_11_WNGTP_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod = (
            9,
            WeaponsFA18EFG.STA_11_WNGTP_LAU127_1x_AN_ASQ_T50_V_1_TCTS_Pod,
        )

    class Pylon10:
        STA_AX_FUEL_CELLS_1x_Internal_Auxillary_Fuel_Cells = (
            10,
            WeaponsFA18EFG.STA_AX_FUEL_CELLS_1x_Internal_Auxillary_Fuel_Cells,
        )
        STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___White = (
            10,
            WeaponsFA18EFG.STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___White,
        )
        STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Red = (
            10,
            WeaponsFA18EFG.STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Red,
        )
        STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Green = (
            10,
            WeaponsFA18EFG.STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Green,
        )
        STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Blue = (
            10,
            WeaponsFA18EFG.STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Blue,
        )
        STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Yellow = (
            10,
            WeaponsFA18EFG.STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Yellow,
        )
        STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Orange = (
            10,
            WeaponsFA18EFG.STA_AX_CKPIT_SMOKE_1x_Internal_Smoke_Generator___Orange,
        )

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

    tasks = [task.Refueling]
    task_default = task.Refueling
