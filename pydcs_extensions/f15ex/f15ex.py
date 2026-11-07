"""The F-15EX V3 mod: F-15EX, F-15EX (CFTs) and F-15IA.

Station and store ids match the mod's own pylon tables. Stores that also
belong to the F-22A pack reuse its entries. The mod's own files are not
redistributable and are not copied here.
"""

from typing import Set

from dcs import task
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

from game.modsupport import planemod
from pydcs_extensions.f22a.f22a import F22AWeapons
from pydcs_extensions.weapon_injector import inject_weapons


class WeaponsF15EX:
    AIM200_4XRACK = {
        "clsid": "{AIM200-4XRACK}",
        "name": "BRU-61C - 4 x AIM-200A - Active Radar AAM",
        "weight": 681.4,
    }
    AMBER_2xAIM120C5 = {
        "clsid": "{AMBER_2xAIM120C5}",
        "name": "AMBER 2x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 372.96,
    }
    AMBER_2xAIM120C7 = {
        "clsid": "{AMBER_2xAIM120C7}",
        "name": "AMBER 2x AIM-120C-7 AMRAAM - Active Radar AAM",
        "weight": 372.96,
    }
    AMBER_2xAIM120C8 = {
        "clsid": "{AMBER_2xAIM120C8}",
        "name": "AMBER 2x AIM-120C-8 AMRAAM - Active Radar AAM",
        "weight": 383.4482,
    }
    AMBER_2xAIM120D_P3I = {
        "clsid": "{AMBER_2xAIM120D_P3I}",
        "name": "AMBER 2x AIM-120D P3I AMRAAM - Active Radar AAM",
        "weight": 372.96,
    }
    AMBER_2xAIM120D = {
        "clsid": "{AMBER_2xAIM120D}",
        "name": "AMBER 2x AIM-120D-3 AMRAAM - Active Radar AAM",
        "weight": 383.4482,
    }
    AMBER_2xAIM260A = {
        "clsid": "{AMBER_2xAIM260A}",
        "name": "AMBER 2x AIM-260A - Active Radar AAM",
        "weight": 405.6,
    }
    APKWS_II_IR_x21 = {
        "clsid": "{APKWS_II_IR_x21}",
        "name": "BRU-42: 3 x LAU-131 - 7 x IR AGR-20F APKWS II M282",
        "weight": 465.0,
    }
    APKWS_II_IRx21 = {
        "clsid": "{APKWS_II_IRx21}",
        "name": "BRU-42: 3 x LAU-131 - 7 x IR AGR-20F APKWS II M151",
        "weight": 465.0,
    }
    ASG_34_LegionPod = {
        "clsid": "{ASG-34_LegionPod}",
        "name": "AN/ASG-34 Legion IRST pod",
        "weight": 208.0,
    }
    F_15EX_AIM_9X_O = {
        "clsid": "{F-15EX_AIM-9X_O}",
        "name": "2x AIM-9X Sidewinder IR AAM",
        "weight": 321.0,
    }
    F15EX_2xAIM_120C_5 = {
        "clsid": "{F15EX_2xAIM-120C-5}",
        "name": "2x AIM-120C AMRAAM - Active Radar AAM",
        "weight": 372.96,
    }
    F15EX_2xAIM_120C_7 = {
        "clsid": "{F15EX_2xAIM-120C-7}",
        "name": "2x AIM-120C-7 AMRAAM - Active Radar AAM",
        "weight": 372.96,
    }
    F15EX_2xAIM_120C_8 = {
        "clsid": "{F15EX_2xAIM-120C-8}",
        "name": "2x AIM-120C-8 AMRAAM - Active Radar AAM",
        "weight": 383.4482,
    }
    F15EX_2xAIM_120D_3 = {
        "clsid": "{F15EX_2xAIM-120D-3}",
        "name": "2x AIM-120D-3 AMRAAM - Active Radar AAM",
        "weight": 383.4482,
    }
    F15EX_2xAIM_120D = {
        "clsid": "{F15EX_2xAIM-120D}",
        "name": "2x AIM-120D P3I AMRAAM - Active Radar AAM",
        "weight": 372.96,
    }
    F15EX_2xAIM_260A = {
        "clsid": "{F15EX_2xAIM-260A}",
        "name": "2x AIM-260A - Active Radar AAM",
        "weight": 405.6,
    }
    F15EX_AIM_120C_5_CFT_A = {
        "clsid": "{F15EX_AIM-120C-5_CFT_A}",
        "name": "AIM-120C AMRAAM - Active Radar AAM (conformal aft)",
        "weight": 161.48,
    }
    F15EX_AIM_120C_5_CFT_F = {
        "clsid": "{F15EX_AIM-120C-5_CFT_F}",
        "name": "AIM-120C AMRAAM - Active Radar AAM (conformal front)",
        "weight": 161.48,
    }
    F15EX_AIM_120C_5_CFT_RA = {
        "clsid": "{F15EX_AIM-120C-5_CFT_RA}",
        "name": "AIM-120C AMRAAM - Active Radar AAM (conformal right aft)",
        "weight": 161.48,
    }
    F15EX_AIM_120C_5_FUS_LA = {
        "clsid": "{F15EX_AIM-120C-5_FUS_LA}",
        "name": "AIM-120C AMRAAM - Active Radar AAM (FUS LA)",
        "weight": 161.48,
    }
    F15EX_AIM_120C_5_FUS_LF = {
        "clsid": "{F15EX_AIM-120C-5_FUS_LF}",
        "name": "AIM-120C AMRAAM - Active Radar AAM (FUS LF)",
        "weight": 161.48,
    }
    F15EX_AIM_120C_5_FUS_RA = {
        "clsid": "{F15EX_AIM-120C-5_FUS_RA}",
        "name": "AIM-120C AMRAAM - Active Radar AAM (FUS RA)",
        "weight": 161.48,
    }
    F15EX_AIM_120C_5_FUS_RF = {
        "clsid": "{F15EX_AIM-120C-5_FUS_RF}",
        "name": "AIM-120C AMRAAM - Active Radar AAM (FUS RF)",
        "weight": 161.48,
    }
    F15EX_AIM_120C_5_STA11A = {
        "clsid": "{F15EX_AIM-120C-5_STA11A}",
        "name": "AIM-120C AMRAAM - Active Radar AAM (STA11A)",
        "weight": 161.48,
    }
    F15EX_AIM_120C_5_STA11B = {
        "clsid": "{F15EX_AIM-120C-5_STA11B}",
        "name": "AIM-120C AMRAAM - Active Radar AAM (STA11B)",
        "weight": 161.48,
    }
    F15EX_AIM_120C_5_STA2A = {
        "clsid": "{F15EX_AIM-120C-5_STA2A}",
        "name": "AIM-120C AMRAAM - Active Radar AAM (STA2A)",
        "weight": 161.48,
    }
    F15EX_AIM_120C_5_STA2B = {
        "clsid": "{F15EX_AIM-120C-5_STA2B}",
        "name": "AIM-120C AMRAAM - Active Radar AAM (STA2B)",
        "weight": 161.48,
    }
    F15EX_AIM_120C_7_CFT_A = {
        "clsid": "{F15EX_AIM-120C-7_CFT_A}",
        "name": "AIM-120C-7 AMRAAM - Active Radar AAM (conformal aft)",
        "weight": 161.48,
    }
    F15EX_AIM_120C_7_CFT_F = {
        "clsid": "{F15EX_AIM-120C-7_CFT_F}",
        "name": "AIM-120C-7 AMRAAM - Active Radar AAM (conformal front)",
        "weight": 161.48,
    }
    F15EX_AIM_120C_7_CFT_RA = {
        "clsid": "{F15EX_AIM-120C-7_CFT_RA}",
        "name": "AIM-120C-7 AMRAAM - Active Radar AAM (conformal right aft)",
        "weight": 161.48,
    }
    F15EX_AIM_120C_7_FUS_LA = {
        "clsid": "{F15EX_AIM-120C-7_FUS_LA}",
        "name": "AIM-120C-7 AMRAAM - Active Radar AAM (FUS LA)",
        "weight": 161.48,
    }
    F15EX_AIM_120C_7_FUS_LF = {
        "clsid": "{F15EX_AIM-120C-7_FUS_LF}",
        "name": "AIM-120C-7 AMRAAM - Active Radar AAM (FUS LF)",
        "weight": 161.48,
    }
    F15EX_AIM_120C_7_FUS_RA = {
        "clsid": "{F15EX_AIM-120C-7_FUS_RA}",
        "name": "AIM-120C-7 AMRAAM - Active Radar AAM (FUS RA)",
        "weight": 161.48,
    }
    F15EX_AIM_120C_7_FUS_RF = {
        "clsid": "{F15EX_AIM-120C-7_FUS_RF}",
        "name": "AIM-120C-7 AMRAAM - Active Radar AAM (FUS RF)",
        "weight": 161.48,
    }
    F15EX_AIM_120C_7_STA11A = {
        "clsid": "{F15EX_AIM-120C-7_STA11A}",
        "name": "AIM-120C-7 AMRAAM - Active Radar AAM (STA11A)",
        "weight": 161.48,
    }
    F15EX_AIM_120C_7_STA11B = {
        "clsid": "{F15EX_AIM-120C-7_STA11B}",
        "name": "AIM-120C-7 AMRAAM - Active Radar AAM (STA11B)",
        "weight": 161.48,
    }
    F15EX_AIM_120C_7_STA2A = {
        "clsid": "{F15EX_AIM-120C-7_STA2A}",
        "name": "AIM-120C-7 AMRAAM - Active Radar AAM (STA2A)",
        "weight": 161.48,
    }
    F15EX_AIM_120C_7_STA2B = {
        "clsid": "{F15EX_AIM-120C-7_STA2B}",
        "name": "AIM-120C-7 AMRAAM - Active Radar AAM (STA2B)",
        "weight": 161.48,
    }
    F15EX_AIM_120C_8_CFT_A = {
        "clsid": "{F15EX_AIM-120C-8_CFT_A}",
        "name": "AIM-120C-8 AMRAAM - Active Radar AAM (conformal aft)",
        "weight": 166.7241,
    }
    F15EX_AIM_120C_8_CFT_F = {
        "clsid": "{F15EX_AIM-120C-8_CFT_F}",
        "name": "AIM-120C-8 AMRAAM - Active Radar AAM (conformal front)",
        "weight": 166.7241,
    }
    F15EX_AIM_120C_8_CFT_RA = {
        "clsid": "{F15EX_AIM-120C-8_CFT_RA}",
        "name": "AIM-120C-8 AMRAAM - Active Radar AAM (conformal right aft)",
        "weight": 166.7241,
    }
    F15EX_AIM_120C_8_FUS_LA = {
        "clsid": "{F15EX_AIM-120C-8_FUS_LA}",
        "name": "AIM-120C-8 AMRAAM - Active Radar AAM (FUS LA)",
        "weight": 166.7241,
    }
    F15EX_AIM_120C_8_FUS_LF = {
        "clsid": "{F15EX_AIM-120C-8_FUS_LF}",
        "name": "AIM-120C-8 AMRAAM - Active Radar AAM (FUS LF)",
        "weight": 166.7241,
    }
    F15EX_AIM_120C_8_FUS_RA = {
        "clsid": "{F15EX_AIM-120C-8_FUS_RA}",
        "name": "AIM-120C-8 AMRAAM - Active Radar AAM (FUS RA)",
        "weight": 166.7241,
    }
    F15EX_AIM_120C_8_FUS_RF = {
        "clsid": "{F15EX_AIM-120C-8_FUS_RF}",
        "name": "AIM-120C-8 AMRAAM - Active Radar AAM (FUS RF)",
        "weight": 166.7241,
    }
    F15EX_AIM_120C_8_STA11A = {
        "clsid": "{F15EX_AIM-120C-8_STA11A}",
        "name": "AIM-120C-8 AMRAAM - Active Radar AAM (STA11A)",
        "weight": 166.7241,
    }
    F15EX_AIM_120C_8_STA11B = {
        "clsid": "{F15EX_AIM-120C-8_STA11B}",
        "name": "AIM-120C-8 AMRAAM - Active Radar AAM (STA11B)",
        "weight": 166.7241,
    }
    F15EX_AIM_120C_8_STA2A = {
        "clsid": "{F15EX_AIM-120C-8_STA2A}",
        "name": "AIM-120C-8 AMRAAM - Active Radar AAM (STA2A)",
        "weight": 166.7241,
    }
    F15EX_AIM_120C_8_STA2B = {
        "clsid": "{F15EX_AIM-120C-8_STA2B}",
        "name": "AIM-120C-8 AMRAAM - Active Radar AAM (STA2B)",
        "weight": 166.7241,
    }
    F15EX_AIM_120D_3_CFT_A = {
        "clsid": "{F15EX_AIM-120D-3_CFT_A}",
        "name": "AIM-120D-3 AMRAAM - Active Radar AAM (conformal aft)",
        "weight": 165.0,
    }
    F15EX_AIM_120D_3_CFT_F = {
        "clsid": "{F15EX_AIM-120D-3_CFT_F}",
        "name": "AIM-120D-3 AMRAAM - Active Radar AAM (conformal front)",
        "weight": 165.0,
    }
    F15EX_AIM_120D_3_CFT_RA = {
        "clsid": "{F15EX_AIM-120D-3_CFT_RA}",
        "name": "AIM-120D-3 AMRAAM - Active Radar AAM (conformal right aft)",
        "weight": 165.0,
    }
    F15EX_AIM_120D_3_FUS_LA = {
        "clsid": "{F15EX_AIM-120D-3_FUS_LA}",
        "name": "AIM-120D-3 AMRAAM - Active Radar AAM (FUS LA)",
        "weight": 165.0,
    }
    F15EX_AIM_120D_3_FUS_LF = {
        "clsid": "{F15EX_AIM-120D-3_FUS_LF}",
        "name": "AIM-120D-3 AMRAAM - Active Radar AAM (FUS LF)",
        "weight": 165.0,
    }
    F15EX_AIM_120D_3_FUS_RA = {
        "clsid": "{F15EX_AIM-120D-3_FUS_RA}",
        "name": "AIM-120D-3 AMRAAM - Active Radar AAM (FUS RA)",
        "weight": 165.0,
    }
    F15EX_AIM_120D_3_FUS_RF = {
        "clsid": "{F15EX_AIM-120D-3_FUS_RF}",
        "name": "AIM-120D-3 AMRAAM - Active Radar AAM (FUS RF)",
        "weight": 165.0,
    }
    F15EX_AIM_120D_3_STA11A = {
        "clsid": "{F15EX_AIM-120D-3_STA11A}",
        "name": "AIM-120D-3 AMRAAM - Active Radar AAM (STA11A)",
        "weight": 165.0,
    }
    F15EX_AIM_120D_3_STA11B = {
        "clsid": "{F15EX_AIM-120D-3_STA11B}",
        "name": "AIM-120D-3 AMRAAM - Active Radar AAM (STA11B)",
        "weight": 165.0,
    }
    F15EX_AIM_120D_3_STA2A = {
        "clsid": "{F15EX_AIM-120D-3_STA2A}",
        "name": "AIM-120D-3 AMRAAM - Active Radar AAM (STA2A)",
        "weight": 165.0,
    }
    F15EX_AIM_120D_3_STA2B = {
        "clsid": "{F15EX_AIM-120D-3_STA2B}",
        "name": "AIM-120D-3 AMRAAM - Active Radar AAM (STA2B)",
        "weight": 165.0,
    }
    F15EX_AIM_120D_CFT_A = {
        "clsid": "{F15EX_AIM-120D_CFT_A}",
        "name": "AIM-120D P3I AMRAAM - Active Radar AAM (conformal aft)",
        "weight": 161.48,
    }
    F15EX_AIM_120D_CFT_F = {
        "clsid": "{F15EX_AIM-120D_CFT_F}",
        "name": "AIM-120D P3I AMRAAM - Active Radar AAM (conformal front)",
        "weight": 161.48,
    }
    F15EX_AIM_120D_CFT_RA = {
        "clsid": "{F15EX_AIM-120D_CFT_RA}",
        "name": "AIM-120D P3I AMRAAM - Active Radar AAM (conformal right aft)",
        "weight": 161.48,
    }
    F15EX_AIM_120D_FUS_LA = {
        "clsid": "{F15EX_AIM-120D_FUS_LA}",
        "name": "AIM-120D P3I AMRAAM - Active Radar AAM (FUS LA)",
        "weight": 161.48,
    }
    F15EX_AIM_120D_FUS_LF = {
        "clsid": "{F15EX_AIM-120D_FUS_LF}",
        "name": "AIM-120D P3I AMRAAM - Active Radar AAM (FUS LF)",
        "weight": 161.48,
    }
    F15EX_AIM_120D_FUS_RA = {
        "clsid": "{F15EX_AIM-120D_FUS_RA}",
        "name": "AIM-120D P3I AMRAAM - Active Radar AAM (FUS RA)",
        "weight": 161.48,
    }
    F15EX_AIM_120D_FUS_RF = {
        "clsid": "{F15EX_AIM-120D_FUS_RF}",
        "name": "AIM-120D P3I AMRAAM - Active Radar AAM (FUS RF)",
        "weight": 161.48,
    }
    F15EX_AIM_120D_STA11A = {
        "clsid": "{F15EX_AIM-120D_STA11A}",
        "name": "AIM-120D P3I AMRAAM - Active Radar AAM (STA11A)",
        "weight": 161.48,
    }
    F15EX_AIM_120D_STA11B = {
        "clsid": "{F15EX_AIM-120D_STA11B}",
        "name": "AIM-120D P3I AMRAAM - Active Radar AAM (STA11B)",
        "weight": 161.48,
    }
    F15EX_AIM_120D_STA2A = {
        "clsid": "{F15EX_AIM-120D_STA2A}",
        "name": "AIM-120D P3I AMRAAM - Active Radar AAM (STA2A)",
        "weight": 161.48,
    }
    F15EX_AIM_120D_STA2B = {
        "clsid": "{F15EX_AIM-120D_STA2B}",
        "name": "AIM-120D P3I AMRAAM - Active Radar AAM (STA2B)",
        "weight": 161.48,
    }
    F15EX_AIM_174B_CFT = {
        "clsid": "{F15EX_AIM-174B_CFT}",
        "name": "AIM-174B Gunslinger - Active Radar ULRAAM (conformal)",
        "weight": 860.0,
    }
    F15EX_AIM_174B = {
        "clsid": "{F15EX_AIM-174B}",
        "name": "AIM-174B Gunslinger - Active Radar ULRAAM",
        "weight": 910.0,
    }
    F15EX_AIM_200A_CFT_A = {
        "clsid": "{F15EX_AIM-200A_CFT_A}",
        "name": "AIM-200A - Active Radar AAM (conformal aft)",
        "weight": 157.85,
    }
    F15EX_AIM_200A_CFT_F = {
        "clsid": "{F15EX_AIM-200A_CFT_F}",
        "name": "AIM-200A - Active Radar AAM (conformal front)",
        "weight": 157.85,
    }
    F15EX_AIM_200A_CFT_RA = {
        "clsid": "{F15EX_AIM-200A_CFT_RA}",
        "name": "AIM-200A - Active Radar AAM (conformal right aft)",
        "weight": 157.85,
    }
    F15EX_AIM_200A_FUS_LA = {
        "clsid": "{F15EX_AIM-200A_FUS_LA}",
        "name": "AIM-200A - Active Radar AAM (FUS LA)",
        "weight": 157.85,
    }
    F15EX_AIM_200A_FUS_LF = {
        "clsid": "{F15EX_AIM-200A_FUS_LF}",
        "name": "AIM-200A - Active Radar AAM (FUS LF)",
        "weight": 157.85,
    }
    F15EX_AIM_200A_FUS_RA = {
        "clsid": "{F15EX_AIM-200A_FUS_RA}",
        "name": "AIM-200A - Active Radar AAM (FUS RA)",
        "weight": 157.85,
    }
    F15EX_AIM_200A_FUS_RF = {
        "clsid": "{F15EX_AIM-200A_FUS_RF}",
        "name": "AIM-200A - Active Radar AAM (FUS RF)",
        "weight": 157.85,
    }
    F15EX_AIM_260A_CFT_A = {
        "clsid": "{F15EX_AIM-260A_CFT_A}",
        "name": "AIM-260A - Active Radar AAM (conformal aft)",
        "weight": 160.0,
    }
    F15EX_AIM_260A_CFT_F = {
        "clsid": "{F15EX_AIM-260A_CFT_F}",
        "name": "AIM-260A - Active Radar AAM (conformal front)",
        "weight": 160.0,
    }
    F15EX_AIM_260A_CFT_RA = {
        "clsid": "{F15EX_AIM-260A_CFT_RA}",
        "name": "AIM-260A - Active Radar AAM (conformal right aft)",
        "weight": 160.0,
    }
    F15EX_AIM_260A_FUS_LA = {
        "clsid": "{F15EX_AIM-260A_FUS_LA}",
        "name": "AIM-260A - Active Radar AAM (FUS LA)",
        "weight": 160.0,
    }
    F15EX_AIM_260A_FUS_LF = {
        "clsid": "{F15EX_AIM-260A_FUS_LF}",
        "name": "AIM-260A - Active Radar AAM (FUS LF)",
        "weight": 160.0,
    }
    F15EX_AIM_260A_FUS_RA = {
        "clsid": "{F15EX_AIM-260A_FUS_RA}",
        "name": "AIM-260A - Active Radar AAM (FUS RA)",
        "weight": 160.0,
    }
    F15EX_AIM_260A_FUS_RF = {
        "clsid": "{F15EX_AIM-260A_FUS_RF}",
        "name": "AIM-260A - Active Radar AAM (FUS RF)",
        "weight": 160.0,
    }
    F15EX_AIM_260A_STA11A = {
        "clsid": "{F15EX_AIM-260A_STA11A}",
        "name": "AIM-260A - Active Radar AAM (STA11A)",
        "weight": 160.0,
    }
    F15EX_AIM_260A_STA11B = {
        "clsid": "{F15EX_AIM-260A_STA11B}",
        "name": "AIM-260A - Active Radar AAM (STA11B)",
        "weight": 160.0,
    }
    F15EX_AIM_260A_STA2A = {
        "clsid": "{F15EX_AIM-260A_STA2A}",
        "name": "AIM-260A - Active Radar AAM (STA2A)",
        "weight": 160.0,
    }
    F15EX_AIM_260A_STA2B = {
        "clsid": "{F15EX_AIM-260A_STA2B}",
        "name": "AIM-260A - Active Radar AAM (STA2B)",
        "weight": 160.0,
    }
    F15EX_AIM_9X_ED_STA11A = {
        "clsid": "{F15EX_AIM-9X-ED_STA11A}",
        "name": "AIM-9X Sidewinder IR AAM (ED) (STA11A)",
        "weight": 85.5,
    }
    F15EX_AIM_9X_ED_STA11B = {
        "clsid": "{F15EX_AIM-9X-ED_STA11B}",
        "name": "AIM-9X Sidewinder IR AAM (ED) (STA11B)",
        "weight": 85.5,
    }
    F15EX_AIM_9X_ED_STA2A = {
        "clsid": "{F15EX_AIM-9X-ED_STA2A}",
        "name": "AIM-9X Sidewinder IR AAM (ED) (STA2A)",
        "weight": 85.5,
    }
    F15EX_AIM_9X_ED_STA2B = {
        "clsid": "{F15EX_AIM-9X-ED_STA2B}",
        "name": "AIM-9X Sidewinder IR AAM (ED) (STA2B)",
        "weight": 85.5,
    }
    F15EX_AIM_9X_STA11A = {
        "clsid": "{F15EX_AIM-9X_STA11A}",
        "name": "AIM-9X Sidewinder IR AAM (STA11A)",
        "weight": 85.5,
    }
    F15EX_AIM_9X_STA11B = {
        "clsid": "{F15EX_AIM-9X_STA11B}",
        "name": "AIM-9X Sidewinder IR AAM (STA11B)",
        "weight": 85.5,
    }
    F15EX_AIM_9X_STA2A = {
        "clsid": "{F15EX_AIM-9X_STA2A}",
        "name": "AIM-9X Sidewinder IR AAM (STA2A)",
        "weight": 85.5,
    }
    F15EX_AIM_9X_STA2B = {
        "clsid": "{F15EX_AIM-9X_STA2B}",
        "name": "AIM-9X Sidewinder IR AAM (STA2B)",
        "weight": 85.5,
    }
    F15EX_LAU_115_2xAIM_120C_5 = {
        "clsid": "{F15EX_LAU_115_2xAIM-120C-5}",
        "name": "LAU-115 with 2 x LAU-127 AIM-120C AMRAAM - Active Radar AAM",
        "weight": 372.96,
    }
    F15EX_LAU_115_2xAIM_120C_8 = {
        "clsid": "{F15EX_LAU_115_2xAIM-120C-8}",
        "name": "LAU-115 with 2 x LAU-127 AIM-120C-8 AMRAAM - Active Radar AAM",
        "weight": 383.4482,
    }
    F15EX_LAU_115_2xAIM_120D = {
        "clsid": "{F15EX_LAU_115_2xAIM-120D}",
        "name": "LAU-115 with 2 x LAU-127 AIM-120D P3I AMRAAM - Active Radar AAM",
        "weight": 372.96,
    }
    F15EX_PYTHON_5_STA11A = {
        "clsid": "{F15EX_PYTHON-5_STA11A}",
        "name": "Python-5 IR AAM (STA11A)",
        "weight": 105.0,
    }
    F15EX_PYTHON_5_STA11B = {
        "clsid": "{F15EX_PYTHON-5_STA11B}",
        "name": "Python-5 IR AAM (STA11B)",
        "weight": 105.0,
    }
    F15EX_PYTHON_5_STA2A = {
        "clsid": "{F15EX_PYTHON-5_STA2A}",
        "name": "Python-5 IR AAM (STA2A)",
        "weight": 105.0,
    }
    F15EX_PYTHON_5_STA2B = {
        "clsid": "{F15EX_PYTHON-5_STA2B}",
        "name": "Python-5 IR AAM (STA2B)",
        "weight": 105.0,
    }
    F15IA_PYTHON_5 = {
        "clsid": "{F15IA_PYTHON-5}",
        "name": "2 x Python-5 IR AAM",
        "weight": 315.0,
    }


inject_weapons(WeaponsF15EX)


@planemod
class F_15EX(PlaneType):
    id = "F15EX"
    flyable = True
    height = 5.63
    width = 13.05
    length = 19.43
    fuel_max = 6146
    max_speed = 2664
    chaff = 120
    flare = 120
    charge_total = 360
    chaff_charge_size = 1
    flare_charge_size = 2
    eplrs = True
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    livery_name = "F-15EX"  # from livery_entry

    class Pylon1:
        F15EX_2xAIM_260A = (1, WeaponsF15EX.F15EX_2xAIM_260A)
        F15EX_2xAIM_120D_3 = (1, WeaponsF15EX.F15EX_2xAIM_120D_3)
        F15EX_2xAIM_120D = (1, WeaponsF15EX.F15EX_2xAIM_120D)
        F15EX_2xAIM_120C_8 = (1, WeaponsF15EX.F15EX_2xAIM_120C_8)
        F15EX_2xAIM_120C_7 = (1, WeaponsF15EX.F15EX_2xAIM_120C_7)
        F15EX_2xAIM_120C_5 = (1, WeaponsF15EX.F15EX_2xAIM_120C_5)
        F_15EX_AIM_9X_O = (1, WeaponsF15EX.F_15EX_AIM_9X_O)

    class Pylon2:
        F15E_EXTTANK = (2, Weapons.Fuel_tank_610_gal_)
        F15E_EXTTANK_EMPTY = (2, Weapons.Fuel_tank_610_gal__Empty_)
        LAU_115_2xAIM_260A = (2, F22AWeapons._2x_AIM_260A___Active_Radar_AAM)
        LAU_115_2xAIM_120C_7 = (2, F22AWeapons._2x_AIM_120C7___Active_Radar_AAM)
        F15EX_LAU_115_2xAIM_120C_8 = (2, WeaponsF15EX.F15EX_LAU_115_2xAIM_120C_8)
        LAU_115_2xAIM_120D_3 = (2, F22AWeapons._2x_AIM_120D3___Active_Radar_AAM)
        F15EX_LAU_115_2xAIM_120D = (2, WeaponsF15EX.F15EX_LAU_115_2xAIM_120D)
        F15EX_LAU_115_2xAIM_120C_5 = (2, WeaponsF15EX.F15EX_LAU_115_2xAIM_120C_5)
        F15EX_AIM_174B = (2, WeaponsF15EX.F15EX_AIM_174B)
        APKWS_II_IRx21 = (2, WeaponsF15EX.APKWS_II_IRx21)
        APKWS_II_IR_x21 = (2, WeaponsF15EX.APKWS_II_IR_x21)

    class Pylon3:
        F15EX_AIM_120C_8_STA2A = (3, WeaponsF15EX.F15EX_AIM_120C_8_STA2A)
        F15EX_AIM_120C_7_STA2A = (3, WeaponsF15EX.F15EX_AIM_120C_7_STA2A)
        F15EX_AIM_120C_5_STA2A = (3, WeaponsF15EX.F15EX_AIM_120C_5_STA2A)
        F15EX_AIM_120D_3_STA2A = (3, WeaponsF15EX.F15EX_AIM_120D_3_STA2A)
        F15EX_AIM_120D_STA2A = (3, WeaponsF15EX.F15EX_AIM_120D_STA2A)
        F15EX_AIM_260A_STA2A = (3, WeaponsF15EX.F15EX_AIM_260A_STA2A)
        F15EX_AIM_9X_STA2A = (3, WeaponsF15EX.F15EX_AIM_9X_STA2A)
        F15EX_AIM_9X_ED_STA2A = (3, WeaponsF15EX.F15EX_AIM_9X_ED_STA2A)

    class Pylon4:
        F15EX_AIM_120C_8_STA2B = (4, WeaponsF15EX.F15EX_AIM_120C_8_STA2B)
        F15EX_AIM_120C_7_STA2B = (4, WeaponsF15EX.F15EX_AIM_120C_7_STA2B)
        F15EX_AIM_120C_5_STA2B = (4, WeaponsF15EX.F15EX_AIM_120C_5_STA2B)
        F15EX_AIM_120D_3_STA2B = (4, WeaponsF15EX.F15EX_AIM_120D_3_STA2B)
        F15EX_AIM_120D_STA2B = (4, WeaponsF15EX.F15EX_AIM_120D_STA2B)
        F15EX_AIM_260A_STA2B = (4, WeaponsF15EX.F15EX_AIM_260A_STA2B)
        F15EX_AIM_9X_STA2B = (4, WeaponsF15EX.F15EX_AIM_9X_STA2B)
        F15EX_AIM_9X_ED_STA2B = (4, WeaponsF15EX.F15EX_AIM_9X_ED_STA2B)

    class Pylon5:
        F15EX_AIM_120C_8_FUS_LF = (5, WeaponsF15EX.F15EX_AIM_120C_8_FUS_LF)
        F15EX_AIM_120C_7_FUS_LF = (5, WeaponsF15EX.F15EX_AIM_120C_7_FUS_LF)
        F15EX_AIM_120C_5_FUS_LF = (5, WeaponsF15EX.F15EX_AIM_120C_5_FUS_LF)
        F15EX_AIM_120D_3_FUS_LF = (5, WeaponsF15EX.F15EX_AIM_120D_3_FUS_LF)
        F15EX_AIM_120D_FUS_LF = (5, WeaponsF15EX.F15EX_AIM_120D_FUS_LF)
        F15EX_AIM_260A_FUS_LF = (5, WeaponsF15EX.F15EX_AIM_260A_FUS_LF)
        F15EX_AIM_200A_FUS_LF = (5, WeaponsF15EX.F15EX_AIM_200A_FUS_LF)

    class Pylon6:
        F15EX_AIM_120C_8_FUS_LA = (6, WeaponsF15EX.F15EX_AIM_120C_8_FUS_LA)
        F15EX_AIM_120C_7_FUS_LA = (6, WeaponsF15EX.F15EX_AIM_120C_7_FUS_LA)
        F15EX_AIM_120C_5_FUS_LA = (6, WeaponsF15EX.F15EX_AIM_120C_5_FUS_LA)
        F15EX_AIM_120D_3_FUS_LA = (6, WeaponsF15EX.F15EX_AIM_120D_3_FUS_LA)
        F15EX_AIM_120D_FUS_LA = (6, WeaponsF15EX.F15EX_AIM_120D_FUS_LA)
        F15EX_AIM_260A_FUS_LA = (6, WeaponsF15EX.F15EX_AIM_260A_FUS_LA)
        F15EX_AIM_200A_FUS_LA = (6, WeaponsF15EX.F15EX_AIM_200A_FUS_LA)

    class Pylon7:
        A111396E_D3E8_4b9c_8AC9_2432489304D5 = (
            7,
            Weapons.AN_AAQ_28_LITENING___Targeting_Pod_,
        )
        AN_AAQ_33 = (7, Weapons.AN_AAQ_33___Advanced_Targeting_Pod)
        F_15E_AAQ_14_LANTIRN = (7, Weapons.AN_AAQ_14_LANTIRN_TGT_Pod)

    class Pylon8:
        F15E_EXTTANK = (8, Weapons.Fuel_tank_610_gal_)
        F15E_EXTTANK_EMPTY = (8, Weapons.Fuel_tank_610_gal__Empty_)
        ASG_34_LegionPod = (8, WeaponsF15EX.ASG_34_LegionPod)
        AN_AAQ_33 = (8, Weapons.AN_AAQ_33___Advanced_Targeting_Pod)

    class Pylon9:
        F_15E_AAQ_13_LANTIRN = (9, Weapons.AN_AAQ_13_LANTIRN_NAV_POD)

    class Pylon10:
        F15EX_AIM_120C_8_FUS_RA = (10, WeaponsF15EX.F15EX_AIM_120C_8_FUS_RA)
        F15EX_AIM_120C_7_FUS_RA = (10, WeaponsF15EX.F15EX_AIM_120C_7_FUS_RA)
        F15EX_AIM_120C_5_FUS_RA = (10, WeaponsF15EX.F15EX_AIM_120C_5_FUS_RA)
        F15EX_AIM_120D_3_FUS_RA = (10, WeaponsF15EX.F15EX_AIM_120D_3_FUS_RA)
        F15EX_AIM_120D_FUS_RA = (10, WeaponsF15EX.F15EX_AIM_120D_FUS_RA)
        F15EX_AIM_260A_FUS_RA = (10, WeaponsF15EX.F15EX_AIM_260A_FUS_RA)
        F15EX_AIM_200A_FUS_RA = (10, WeaponsF15EX.F15EX_AIM_200A_FUS_RA)

    class Pylon11:
        F15EX_AIM_120C_8_FUS_RF = (11, WeaponsF15EX.F15EX_AIM_120C_8_FUS_RF)
        F15EX_AIM_120C_7_FUS_RF = (11, WeaponsF15EX.F15EX_AIM_120C_7_FUS_RF)
        F15EX_AIM_120C_5_FUS_RF = (11, WeaponsF15EX.F15EX_AIM_120C_5_FUS_RF)
        F15EX_AIM_120D_3_FUS_RF = (11, WeaponsF15EX.F15EX_AIM_120D_3_FUS_RF)
        F15EX_AIM_120D_FUS_RF = (11, WeaponsF15EX.F15EX_AIM_120D_FUS_RF)
        F15EX_AIM_260A_FUS_RF = (11, WeaponsF15EX.F15EX_AIM_260A_FUS_RF)
        F15EX_AIM_200A_FUS_RF = (11, WeaponsF15EX.F15EX_AIM_200A_FUS_RF)

    class Pylon12:
        F15EX_AIM_120C_8_STA11B = (12, WeaponsF15EX.F15EX_AIM_120C_8_STA11B)
        F15EX_AIM_120C_7_STA11B = (12, WeaponsF15EX.F15EX_AIM_120C_7_STA11B)
        F15EX_AIM_120C_5_STA11B = (12, WeaponsF15EX.F15EX_AIM_120C_5_STA11B)
        F15EX_AIM_120D_3_STA11B = (12, WeaponsF15EX.F15EX_AIM_120D_3_STA11B)
        F15EX_AIM_120D_STA11B = (12, WeaponsF15EX.F15EX_AIM_120D_STA11B)
        F15EX_AIM_260A_STA11B = (12, WeaponsF15EX.F15EX_AIM_260A_STA11B)
        F15EX_AIM_9X_STA11B = (12, WeaponsF15EX.F15EX_AIM_9X_STA11B)
        F15EX_AIM_9X_ED_STA11B = (12, WeaponsF15EX.F15EX_AIM_9X_ED_STA11B)

    class Pylon13:
        F15EX_AIM_120C_8_STA11A = (13, WeaponsF15EX.F15EX_AIM_120C_8_STA11A)
        F15EX_AIM_120C_7_STA11A = (13, WeaponsF15EX.F15EX_AIM_120C_7_STA11A)
        F15EX_AIM_120C_5_STA11A = (13, WeaponsF15EX.F15EX_AIM_120C_5_STA11A)
        F15EX_AIM_120D_3_STA11A = (13, WeaponsF15EX.F15EX_AIM_120D_3_STA11A)
        F15EX_AIM_120D_STA11A = (13, WeaponsF15EX.F15EX_AIM_120D_STA11A)
        F15EX_AIM_260A_STA11A = (13, WeaponsF15EX.F15EX_AIM_260A_STA11A)
        F15EX_AIM_9X_STA11A = (13, WeaponsF15EX.F15EX_AIM_9X_STA11A)
        F15EX_AIM_9X_ED_STA11A = (13, WeaponsF15EX.F15EX_AIM_9X_ED_STA11A)

    class Pylon14:
        F15E_EXTTANK = (14, Weapons.Fuel_tank_610_gal_)
        F15E_EXTTANK_EMPTY = (14, Weapons.Fuel_tank_610_gal__Empty_)
        LAU_115_2xAIM_260A = (14, F22AWeapons._2x_AIM_260A___Active_Radar_AAM)
        LAU_115_2xAIM_120C_7 = (14, F22AWeapons._2x_AIM_120C7___Active_Radar_AAM)
        F15EX_LAU_115_2xAIM_120C_8 = (14, WeaponsF15EX.F15EX_LAU_115_2xAIM_120C_8)
        LAU_115_2xAIM_120D_3 = (14, F22AWeapons._2x_AIM_120D3___Active_Radar_AAM)
        F15EX_LAU_115_2xAIM_120D = (14, WeaponsF15EX.F15EX_LAU_115_2xAIM_120D)
        F15EX_LAU_115_2xAIM_120C_5 = (14, WeaponsF15EX.F15EX_LAU_115_2xAIM_120C_5)
        F15EX_AIM_174B = (14, WeaponsF15EX.F15EX_AIM_174B)
        APKWS_II_IRx21 = (14, WeaponsF15EX.APKWS_II_IRx21)
        APKWS_II_IR_x21 = (14, WeaponsF15EX.APKWS_II_IR_x21)

    class Pylon15:
        F_15EX_AIM_9X_O = (15, WeaponsF15EX.F_15EX_AIM_9X_O)
        F15EX_2xAIM_260A = (15, WeaponsF15EX.F15EX_2xAIM_260A)
        F15EX_2xAIM_120D_3 = (15, WeaponsF15EX.F15EX_2xAIM_120D_3)
        F15EX_2xAIM_120D = (15, WeaponsF15EX.F15EX_2xAIM_120D)
        F15EX_2xAIM_120C_8 = (15, WeaponsF15EX.F15EX_2xAIM_120C_8)
        F15EX_2xAIM_120C_7 = (15, WeaponsF15EX.F15EX_2xAIM_120C_7)
        F15EX_2xAIM_120C_5 = (15, WeaponsF15EX.F15EX_2xAIM_120C_5)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.Reconnaissance,
    ]
    task_default = task.CAP


@planemod
class F_15EX_CFT(PlaneType):
    id = "F15EX_CFT"
    flyable = True
    height = 5.63
    width = 13.05
    length = 19.43
    fuel_max = 10571
    max_speed = 2664
    chaff = 120
    flare = 120
    charge_total = 360
    chaff_charge_size = 1
    flare_charge_size = 2
    eplrs = True
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    livery_name = "F-15EX_CFT"  # from livery_entry

    class Pylon1:
        F15EX_2xAIM_260A = (1, WeaponsF15EX.F15EX_2xAIM_260A)
        F15EX_2xAIM_120D_3 = (1, WeaponsF15EX.F15EX_2xAIM_120D_3)
        F15EX_2xAIM_120D = (1, WeaponsF15EX.F15EX_2xAIM_120D)
        F15EX_2xAIM_120C_8 = (1, WeaponsF15EX.F15EX_2xAIM_120C_8)
        F15EX_2xAIM_120C_7 = (1, WeaponsF15EX.F15EX_2xAIM_120C_7)
        F15EX_2xAIM_120C_5 = (1, WeaponsF15EX.F15EX_2xAIM_120C_5)
        F_15EX_AIM_9X_O = (1, WeaponsF15EX.F_15EX_AIM_9X_O)

    class Pylon2:
        F15E_EXTTANK = (2, Weapons.Fuel_tank_610_gal_)
        F15E_EXTTANK_EMPTY = (2, Weapons.Fuel_tank_610_gal__Empty_)
        LAU_115_2xAIM_260A = (2, F22AWeapons._2x_AIM_260A___Active_Radar_AAM)
        LAU_115_2xAIM_120C_7 = (2, F22AWeapons._2x_AIM_120C7___Active_Radar_AAM)
        F15EX_LAU_115_2xAIM_120C_8 = (2, WeaponsF15EX.F15EX_LAU_115_2xAIM_120C_8)
        LAU_115_2xAIM_120D_3 = (2, F22AWeapons._2x_AIM_120D3___Active_Radar_AAM)
        F15EX_LAU_115_2xAIM_120D = (2, WeaponsF15EX.F15EX_LAU_115_2xAIM_120D)
        F15EX_LAU_115_2xAIM_120C_5 = (2, WeaponsF15EX.F15EX_LAU_115_2xAIM_120C_5)
        AIM200_4XRACK = (2, WeaponsF15EX.AIM200_4XRACK)
        F15EX_AIM_174B = (2, WeaponsF15EX.F15EX_AIM_174B)
        APKWS_II_IRx21 = (2, WeaponsF15EX.APKWS_II_IRx21)
        APKWS_II_IR_x21 = (2, WeaponsF15EX.APKWS_II_IR_x21)

    class Pylon3:
        F15EX_AIM_120C_8_STA2A = (3, WeaponsF15EX.F15EX_AIM_120C_8_STA2A)
        F15EX_AIM_120C_7_STA2A = (3, WeaponsF15EX.F15EX_AIM_120C_7_STA2A)
        F15EX_AIM_120C_5_STA2A = (3, WeaponsF15EX.F15EX_AIM_120C_5_STA2A)
        F15EX_AIM_120D_3_STA2A = (3, WeaponsF15EX.F15EX_AIM_120D_3_STA2A)
        F15EX_AIM_120D_STA2A = (3, WeaponsF15EX.F15EX_AIM_120D_STA2A)
        F15EX_AIM_260A_STA2A = (3, WeaponsF15EX.F15EX_AIM_260A_STA2A)
        F15EX_AIM_9X_STA2A = (3, WeaponsF15EX.F15EX_AIM_9X_STA2A)
        F15EX_AIM_9X_ED_STA2A = (3, WeaponsF15EX.F15EX_AIM_9X_ED_STA2A)

    class Pylon4:
        F15EX_AIM_120C_8_STA2B = (4, WeaponsF15EX.F15EX_AIM_120C_8_STA2B)
        F15EX_AIM_120C_7_STA2B = (4, WeaponsF15EX.F15EX_AIM_120C_7_STA2B)
        F15EX_AIM_120C_5_STA2B = (4, WeaponsF15EX.F15EX_AIM_120C_5_STA2B)
        F15EX_AIM_120D_3_STA2B = (4, WeaponsF15EX.F15EX_AIM_120D_3_STA2B)
        F15EX_AIM_120D_STA2B = (4, WeaponsF15EX.F15EX_AIM_120D_STA2B)
        F15EX_AIM_260A_STA2B = (4, WeaponsF15EX.F15EX_AIM_260A_STA2B)
        F15EX_AIM_9X_STA2B = (4, WeaponsF15EX.F15EX_AIM_9X_STA2B)
        F15EX_AIM_9X_ED_STA2B = (4, WeaponsF15EX.F15EX_AIM_9X_ED_STA2B)

    class Pylon5:
        AMBER_2xAIM120C8 = (5, WeaponsF15EX.AMBER_2xAIM120C8)
        AMBER_2xAIM120C7 = (5, WeaponsF15EX.AMBER_2xAIM120C7)
        AMBER_2xAIM120C5 = (5, WeaponsF15EX.AMBER_2xAIM120C5)
        AMBER_2xAIM120D = (5, WeaponsF15EX.AMBER_2xAIM120D)
        AMBER_2xAIM120D_P3I = (5, WeaponsF15EX.AMBER_2xAIM120D_P3I)
        AMBER_2xAIM260A = (5, WeaponsF15EX.AMBER_2xAIM260A)
        F15EX_AIM_120C_8_CFT_F = (5, WeaponsF15EX.F15EX_AIM_120C_8_CFT_F)
        F15EX_AIM_120C_7_CFT_F = (5, WeaponsF15EX.F15EX_AIM_120C_7_CFT_F)
        F15EX_AIM_120C_5_CFT_F = (5, WeaponsF15EX.F15EX_AIM_120C_5_CFT_F)
        F15EX_AIM_120D_3_CFT_F = (5, WeaponsF15EX.F15EX_AIM_120D_3_CFT_F)
        F15EX_AIM_120D_CFT_F = (5, WeaponsF15EX.F15EX_AIM_120D_CFT_F)
        F15EX_AIM_260A_CFT_F = (5, WeaponsF15EX.F15EX_AIM_260A_CFT_F)
        F15EX_AIM_200A_CFT_F = (5, WeaponsF15EX.F15EX_AIM_200A_CFT_F)
        AIM200_4XRACK = (5, WeaponsF15EX.AIM200_4XRACK)
        F15EX_AIM_174B_CFT = (5, WeaponsF15EX.F15EX_AIM_174B_CFT)

    class Pylon6:
        AMBER_2xAIM120C8 = (6, WeaponsF15EX.AMBER_2xAIM120C8)
        AMBER_2xAIM120C7 = (6, WeaponsF15EX.AMBER_2xAIM120C7)
        AMBER_2xAIM120C5 = (6, WeaponsF15EX.AMBER_2xAIM120C5)
        AMBER_2xAIM120D = (6, WeaponsF15EX.AMBER_2xAIM120D)
        AMBER_2xAIM120D_P3I = (6, WeaponsF15EX.AMBER_2xAIM120D_P3I)
        AMBER_2xAIM260A = (6, WeaponsF15EX.AMBER_2xAIM260A)
        AIM200_4XRACK = (6, WeaponsF15EX.AIM200_4XRACK)
        F15EX_AIM_120C_8_CFT_A = (6, WeaponsF15EX.F15EX_AIM_120C_8_CFT_A)
        F15EX_AIM_120C_7_CFT_A = (6, WeaponsF15EX.F15EX_AIM_120C_7_CFT_A)
        F15EX_AIM_120C_5_CFT_A = (6, WeaponsF15EX.F15EX_AIM_120C_5_CFT_A)
        F15EX_AIM_120D_3_CFT_A = (6, WeaponsF15EX.F15EX_AIM_120D_3_CFT_A)
        F15EX_AIM_120D_CFT_A = (6, WeaponsF15EX.F15EX_AIM_120D_CFT_A)
        F15EX_AIM_260A_CFT_A = (6, WeaponsF15EX.F15EX_AIM_260A_CFT_A)
        F15EX_AIM_200A_CFT_A = (6, WeaponsF15EX.F15EX_AIM_200A_CFT_A)

    class Pylon7:
        A111396E_D3E8_4b9c_8AC9_2432489304D5 = (
            7,
            Weapons.AN_AAQ_28_LITENING___Targeting_Pod_,
        )
        AN_AAQ_33 = (7, Weapons.AN_AAQ_33___Advanced_Targeting_Pod)
        F_15E_AAQ_14_LANTIRN = (7, Weapons.AN_AAQ_14_LANTIRN_TGT_Pod)

    class Pylon8:
        AMBER_2xAIM120C8 = (8, WeaponsF15EX.AMBER_2xAIM120C8)
        AMBER_2xAIM120C7 = (8, WeaponsF15EX.AMBER_2xAIM120C7)
        AMBER_2xAIM120C5 = (8, WeaponsF15EX.AMBER_2xAIM120C5)
        AMBER_2xAIM120D = (8, WeaponsF15EX.AMBER_2xAIM120D)
        AMBER_2xAIM120D_P3I = (8, WeaponsF15EX.AMBER_2xAIM120D_P3I)
        AMBER_2xAIM260A = (8, WeaponsF15EX.AMBER_2xAIM260A)
        AIM200_4XRACK = (8, WeaponsF15EX.AIM200_4XRACK)
        F15E_EXTTANK = (8, Weapons.Fuel_tank_610_gal_)
        F15E_EXTTANK_EMPTY = (8, Weapons.Fuel_tank_610_gal__Empty_)
        ASG_34_LegionPod = (8, WeaponsF15EX.ASG_34_LegionPod)

    class Pylon9:
        F_15E_AAQ_13_LANTIRN = (9, Weapons.AN_AAQ_13_LANTIRN_NAV_POD)

    class Pylon10:
        AMBER_2xAIM120C8 = (10, WeaponsF15EX.AMBER_2xAIM120C8)
        AMBER_2xAIM120C7 = (10, WeaponsF15EX.AMBER_2xAIM120C7)
        AMBER_2xAIM120C5 = (10, WeaponsF15EX.AMBER_2xAIM120C5)
        AMBER_2xAIM120D = (10, WeaponsF15EX.AMBER_2xAIM120D)
        AMBER_2xAIM120D_P3I = (10, WeaponsF15EX.AMBER_2xAIM120D_P3I)
        AMBER_2xAIM260A = (10, WeaponsF15EX.AMBER_2xAIM260A)
        AIM200_4XRACK = (10, WeaponsF15EX.AIM200_4XRACK)
        F15EX_AIM_120C_8_CFT_RA = (10, WeaponsF15EX.F15EX_AIM_120C_8_CFT_RA)
        F15EX_AIM_120C_7_CFT_RA = (10, WeaponsF15EX.F15EX_AIM_120C_7_CFT_RA)
        F15EX_AIM_120C_5_CFT_RA = (10, WeaponsF15EX.F15EX_AIM_120C_5_CFT_RA)
        F15EX_AIM_120D_3_CFT_RA = (10, WeaponsF15EX.F15EX_AIM_120D_3_CFT_RA)
        F15EX_AIM_120D_CFT_RA = (10, WeaponsF15EX.F15EX_AIM_120D_CFT_RA)
        F15EX_AIM_260A_CFT_RA = (10, WeaponsF15EX.F15EX_AIM_260A_CFT_RA)
        F15EX_AIM_200A_CFT_RA = (10, WeaponsF15EX.F15EX_AIM_200A_CFT_RA)

    class Pylon11:
        AMBER_2xAIM120C8 = (11, WeaponsF15EX.AMBER_2xAIM120C8)
        AMBER_2xAIM120C7 = (11, WeaponsF15EX.AMBER_2xAIM120C7)
        AMBER_2xAIM120C5 = (11, WeaponsF15EX.AMBER_2xAIM120C5)
        AMBER_2xAIM120D = (11, WeaponsF15EX.AMBER_2xAIM120D)
        AMBER_2xAIM120D_P3I = (11, WeaponsF15EX.AMBER_2xAIM120D_P3I)
        AMBER_2xAIM260A = (11, WeaponsF15EX.AMBER_2xAIM260A)
        F15EX_AIM_120C_8_CFT_F = (11, WeaponsF15EX.F15EX_AIM_120C_8_CFT_F)
        F15EX_AIM_120C_7_CFT_F = (11, WeaponsF15EX.F15EX_AIM_120C_7_CFT_F)
        F15EX_AIM_120C_5_CFT_F = (11, WeaponsF15EX.F15EX_AIM_120C_5_CFT_F)
        F15EX_AIM_120D_3_CFT_F = (11, WeaponsF15EX.F15EX_AIM_120D_3_CFT_F)
        F15EX_AIM_120D_CFT_F = (11, WeaponsF15EX.F15EX_AIM_120D_CFT_F)
        F15EX_AIM_260A_CFT_F = (11, WeaponsF15EX.F15EX_AIM_260A_CFT_F)
        F15EX_AIM_200A_CFT_F = (11, WeaponsF15EX.F15EX_AIM_200A_CFT_F)
        AIM200_4XRACK = (11, WeaponsF15EX.AIM200_4XRACK)
        F15EX_AIM_174B_CFT = (11, WeaponsF15EX.F15EX_AIM_174B_CFT)

    class Pylon12:
        F15EX_AIM_120C_8_STA11B = (12, WeaponsF15EX.F15EX_AIM_120C_8_STA11B)
        F15EX_AIM_120C_7_STA11B = (12, WeaponsF15EX.F15EX_AIM_120C_7_STA11B)
        F15EX_AIM_120C_5_STA11B = (12, WeaponsF15EX.F15EX_AIM_120C_5_STA11B)
        F15EX_AIM_120D_3_STA11B = (12, WeaponsF15EX.F15EX_AIM_120D_3_STA11B)
        F15EX_AIM_120D_STA11B = (12, WeaponsF15EX.F15EX_AIM_120D_STA11B)
        F15EX_AIM_260A_STA11B = (12, WeaponsF15EX.F15EX_AIM_260A_STA11B)
        F15EX_AIM_9X_STA11B = (12, WeaponsF15EX.F15EX_AIM_9X_STA11B)
        F15EX_AIM_9X_ED_STA11B = (12, WeaponsF15EX.F15EX_AIM_9X_ED_STA11B)

    class Pylon13:
        F15EX_AIM_120C_8_STA11A = (13, WeaponsF15EX.F15EX_AIM_120C_8_STA11A)
        F15EX_AIM_120C_7_STA11A = (13, WeaponsF15EX.F15EX_AIM_120C_7_STA11A)
        F15EX_AIM_120C_5_STA11A = (13, WeaponsF15EX.F15EX_AIM_120C_5_STA11A)
        F15EX_AIM_120D_3_STA11A = (13, WeaponsF15EX.F15EX_AIM_120D_3_STA11A)
        F15EX_AIM_120D_STA11A = (13, WeaponsF15EX.F15EX_AIM_120D_STA11A)
        F15EX_AIM_260A_STA11A = (13, WeaponsF15EX.F15EX_AIM_260A_STA11A)
        F15EX_AIM_9X_STA11A = (13, WeaponsF15EX.F15EX_AIM_9X_STA11A)
        F15EX_AIM_9X_ED_STA11A = (13, WeaponsF15EX.F15EX_AIM_9X_ED_STA11A)

    class Pylon14:
        F15E_EXTTANK = (14, Weapons.Fuel_tank_610_gal_)
        F15E_EXTTANK_EMPTY = (14, Weapons.Fuel_tank_610_gal__Empty_)
        LAU_115_2xAIM_260A = (14, F22AWeapons._2x_AIM_260A___Active_Radar_AAM)
        LAU_115_2xAIM_120C_7 = (14, F22AWeapons._2x_AIM_120C7___Active_Radar_AAM)
        F15EX_LAU_115_2xAIM_120C_8 = (14, WeaponsF15EX.F15EX_LAU_115_2xAIM_120C_8)
        LAU_115_2xAIM_120D_3 = (14, F22AWeapons._2x_AIM_120D3___Active_Radar_AAM)
        F15EX_LAU_115_2xAIM_120D = (14, WeaponsF15EX.F15EX_LAU_115_2xAIM_120D)
        F15EX_LAU_115_2xAIM_120C_5 = (14, WeaponsF15EX.F15EX_LAU_115_2xAIM_120C_5)
        AIM200_4XRACK = (14, WeaponsF15EX.AIM200_4XRACK)
        F15EX_AIM_174B = (14, WeaponsF15EX.F15EX_AIM_174B)
        APKWS_II_IRx21 = (14, WeaponsF15EX.APKWS_II_IRx21)
        APKWS_II_IR_x21 = (14, WeaponsF15EX.APKWS_II_IR_x21)

    class Pylon15:
        F_15EX_AIM_9X_O = (15, WeaponsF15EX.F_15EX_AIM_9X_O)
        F15EX_2xAIM_260A = (15, WeaponsF15EX.F15EX_2xAIM_260A)
        F15EX_2xAIM_120D_3 = (15, WeaponsF15EX.F15EX_2xAIM_120D_3)
        F15EX_2xAIM_120D = (15, WeaponsF15EX.F15EX_2xAIM_120D)
        F15EX_2xAIM_120C_8 = (15, WeaponsF15EX.F15EX_2xAIM_120C_8)
        F15EX_2xAIM_120C_7 = (15, WeaponsF15EX.F15EX_2xAIM_120C_7)
        F15EX_2xAIM_120C_5 = (15, WeaponsF15EX.F15EX_2xAIM_120C_5)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.Reconnaissance,
    ]
    task_default = task.CAP


@planemod
class F_15IA(PlaneType):
    id = "F15IA"
    flyable = True
    height = 5.63
    width = 13.05
    length = 19.43
    fuel_max = 10571
    max_speed = 2664
    chaff = 120
    flare = 120
    charge_total = 360
    chaff_charge_size = 1
    flare_charge_size = 2
    eplrs = True
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    livery_name = "F-15IA"  # from livery_entry

    class Pylon1:
        F15EX_2xAIM_120D_3 = (1, WeaponsF15EX.F15EX_2xAIM_120D_3)
        F15EX_2xAIM_120D = (1, WeaponsF15EX.F15EX_2xAIM_120D)
        F15EX_2xAIM_120C_8 = (1, WeaponsF15EX.F15EX_2xAIM_120C_8)
        F15EX_2xAIM_120C_7 = (1, WeaponsF15EX.F15EX_2xAIM_120C_7)
        F15EX_2xAIM_120C_5 = (1, WeaponsF15EX.F15EX_2xAIM_120C_5)
        F15IA_PYTHON_5 = (1, WeaponsF15EX.F15IA_PYTHON_5)

    class Pylon2:
        F15E_EXTTANK = (2, Weapons.Fuel_tank_610_gal_)
        F15E_EXTTANK_EMPTY = (2, Weapons.Fuel_tank_610_gal__Empty_)
        LAU_115_2xAIM_120C_7 = (2, F22AWeapons._2x_AIM_120C7___Active_Radar_AAM)
        F15EX_LAU_115_2xAIM_120C_8 = (2, WeaponsF15EX.F15EX_LAU_115_2xAIM_120C_8)
        LAU_115_2xAIM_120D_3 = (2, F22AWeapons._2x_AIM_120D3___Active_Radar_AAM)
        F15EX_LAU_115_2xAIM_120D = (2, WeaponsF15EX.F15EX_LAU_115_2xAIM_120D)
        F15EX_LAU_115_2xAIM_120C_5 = (2, WeaponsF15EX.F15EX_LAU_115_2xAIM_120C_5)
        AIM200_4XRACK = (2, WeaponsF15EX.AIM200_4XRACK)
        F15EX_AIM_174B = (2, WeaponsF15EX.F15EX_AIM_174B)
        APKWS_II_IRx21 = (2, WeaponsF15EX.APKWS_II_IRx21)
        APKWS_II_IR_x21 = (2, WeaponsF15EX.APKWS_II_IR_x21)

    class Pylon3:
        F15EX_AIM_120C_8_STA2A = (3, WeaponsF15EX.F15EX_AIM_120C_8_STA2A)
        F15EX_AIM_120C_7_STA2A = (3, WeaponsF15EX.F15EX_AIM_120C_7_STA2A)
        F15EX_AIM_120C_5_STA2A = (3, WeaponsF15EX.F15EX_AIM_120C_5_STA2A)
        F15EX_AIM_120D_3_STA2A = (3, WeaponsF15EX.F15EX_AIM_120D_3_STA2A)
        F15EX_AIM_120D_STA2A = (3, WeaponsF15EX.F15EX_AIM_120D_STA2A)
        F15EX_PYTHON_5_STA2A = (3, WeaponsF15EX.F15EX_PYTHON_5_STA2A)
        F15EX_AIM_9X_ED_STA2A = (3, WeaponsF15EX.F15EX_AIM_9X_ED_STA2A)

    class Pylon4:
        F15EX_AIM_120C_8_STA2B = (4, WeaponsF15EX.F15EX_AIM_120C_8_STA2B)
        F15EX_AIM_120C_7_STA2B = (4, WeaponsF15EX.F15EX_AIM_120C_7_STA2B)
        F15EX_AIM_120C_5_STA2B = (4, WeaponsF15EX.F15EX_AIM_120C_5_STA2B)
        F15EX_AIM_120D_3_STA2B = (4, WeaponsF15EX.F15EX_AIM_120D_3_STA2B)
        F15EX_AIM_120D_STA2B = (4, WeaponsF15EX.F15EX_AIM_120D_STA2B)
        F15EX_PYTHON_5_STA2B = (4, WeaponsF15EX.F15EX_PYTHON_5_STA2B)
        F15EX_AIM_9X_ED_STA2B = (4, WeaponsF15EX.F15EX_AIM_9X_ED_STA2B)

    class Pylon5:
        AMBER_2xAIM120C8 = (5, WeaponsF15EX.AMBER_2xAIM120C8)
        AMBER_2xAIM120C7 = (5, WeaponsF15EX.AMBER_2xAIM120C7)
        AMBER_2xAIM120C5 = (5, WeaponsF15EX.AMBER_2xAIM120C5)
        AMBER_2xAIM120D = (5, WeaponsF15EX.AMBER_2xAIM120D)
        AMBER_2xAIM120D_P3I = (5, WeaponsF15EX.AMBER_2xAIM120D_P3I)
        AMBER_2xAIM260A = (5, WeaponsF15EX.AMBER_2xAIM260A)
        F15EX_AIM_120C_8_CFT_F = (5, WeaponsF15EX.F15EX_AIM_120C_8_CFT_F)
        F15EX_AIM_120C_7_CFT_F = (5, WeaponsF15EX.F15EX_AIM_120C_7_CFT_F)
        F15EX_AIM_120C_5_CFT_F = (5, WeaponsF15EX.F15EX_AIM_120C_5_CFT_F)
        F15EX_AIM_120D_3_CFT_F = (5, WeaponsF15EX.F15EX_AIM_120D_3_CFT_F)
        F15EX_AIM_120D_CFT_F = (5, WeaponsF15EX.F15EX_AIM_120D_CFT_F)
        F15EX_AIM_200A_CFT_F = (5, WeaponsF15EX.F15EX_AIM_200A_CFT_F)
        AIM200_4XRACK = (5, WeaponsF15EX.AIM200_4XRACK)
        F15EX_AIM_174B_CFT = (5, WeaponsF15EX.F15EX_AIM_174B_CFT)

    class Pylon6:
        AMBER_2xAIM120C8 = (6, WeaponsF15EX.AMBER_2xAIM120C8)
        AMBER_2xAIM120C7 = (6, WeaponsF15EX.AMBER_2xAIM120C7)
        AMBER_2xAIM120C5 = (6, WeaponsF15EX.AMBER_2xAIM120C5)
        AMBER_2xAIM120D = (6, WeaponsF15EX.AMBER_2xAIM120D)
        AMBER_2xAIM120D_P3I = (6, WeaponsF15EX.AMBER_2xAIM120D_P3I)
        AMBER_2xAIM260A = (6, WeaponsF15EX.AMBER_2xAIM260A)
        AIM200_4XRACK = (6, WeaponsF15EX.AIM200_4XRACK)
        F15EX_AIM_120C_8_CFT_A = (6, WeaponsF15EX.F15EX_AIM_120C_8_CFT_A)
        F15EX_AIM_120C_7_CFT_A = (6, WeaponsF15EX.F15EX_AIM_120C_7_CFT_A)
        F15EX_AIM_120C_5_CFT_A = (6, WeaponsF15EX.F15EX_AIM_120C_5_CFT_A)
        F15EX_AIM_120D_3_CFT_A = (6, WeaponsF15EX.F15EX_AIM_120D_3_CFT_A)
        F15EX_AIM_120D_CFT_A = (6, WeaponsF15EX.F15EX_AIM_120D_CFT_A)
        F15EX_AIM_200A_CFT_A = (6, WeaponsF15EX.F15EX_AIM_200A_CFT_A)

    class Pylon7:
        A111396E_D3E8_4b9c_8AC9_2432489304D5 = (
            7,
            Weapons.AN_AAQ_28_LITENING___Targeting_Pod_,
        )
        F_15E_AAQ_14_LANTIRN = (7, Weapons.AN_AAQ_14_LANTIRN_TGT_Pod)

    class Pylon8:
        AMBER_2xAIM120C8 = (8, WeaponsF15EX.AMBER_2xAIM120C8)
        AMBER_2xAIM120C7 = (8, WeaponsF15EX.AMBER_2xAIM120C7)
        AMBER_2xAIM120C5 = (8, WeaponsF15EX.AMBER_2xAIM120C5)
        AMBER_2xAIM120D = (8, WeaponsF15EX.AMBER_2xAIM120D)
        AMBER_2xAIM120D_P3I = (8, WeaponsF15EX.AMBER_2xAIM120D_P3I)
        AMBER_2xAIM260A = (8, WeaponsF15EX.AMBER_2xAIM260A)
        AIM200_4XRACK = (8, WeaponsF15EX.AIM200_4XRACK)
        F15E_EXTTANK = (8, Weapons.Fuel_tank_610_gal_)
        F15E_EXTTANK_EMPTY = (8, Weapons.Fuel_tank_610_gal__Empty_)
        ASG_34_LegionPod = (8, WeaponsF15EX.ASG_34_LegionPod)

    class Pylon9:
        F_15E_AAQ_13_LANTIRN = (9, Weapons.AN_AAQ_13_LANTIRN_NAV_POD)

    class Pylon10:
        AMBER_2xAIM120C8 = (10, WeaponsF15EX.AMBER_2xAIM120C8)
        AMBER_2xAIM120C7 = (10, WeaponsF15EX.AMBER_2xAIM120C7)
        AMBER_2xAIM120C5 = (10, WeaponsF15EX.AMBER_2xAIM120C5)
        AMBER_2xAIM120D = (10, WeaponsF15EX.AMBER_2xAIM120D)
        AMBER_2xAIM120D_P3I = (10, WeaponsF15EX.AMBER_2xAIM120D_P3I)
        AMBER_2xAIM260A = (10, WeaponsF15EX.AMBER_2xAIM260A)
        AIM200_4XRACK = (10, WeaponsF15EX.AIM200_4XRACK)
        F15EX_AIM_120C_8_CFT_RA = (10, WeaponsF15EX.F15EX_AIM_120C_8_CFT_RA)
        F15EX_AIM_120C_7_CFT_RA = (10, WeaponsF15EX.F15EX_AIM_120C_7_CFT_RA)
        F15EX_AIM_120C_5_CFT_RA = (10, WeaponsF15EX.F15EX_AIM_120C_5_CFT_RA)
        F15EX_AIM_120D_3_CFT_RA = (10, WeaponsF15EX.F15EX_AIM_120D_3_CFT_RA)
        F15EX_AIM_120D_CFT_RA = (10, WeaponsF15EX.F15EX_AIM_120D_CFT_RA)
        F15EX_AIM_200A_CFT_RA = (10, WeaponsF15EX.F15EX_AIM_200A_CFT_RA)

    class Pylon11:
        AMBER_2xAIM120C8 = (11, WeaponsF15EX.AMBER_2xAIM120C8)
        AMBER_2xAIM120C7 = (11, WeaponsF15EX.AMBER_2xAIM120C7)
        AMBER_2xAIM120C5 = (11, WeaponsF15EX.AMBER_2xAIM120C5)
        AMBER_2xAIM120D = (11, WeaponsF15EX.AMBER_2xAIM120D)
        AMBER_2xAIM120D_P3I = (11, WeaponsF15EX.AMBER_2xAIM120D_P3I)
        AMBER_2xAIM260A = (11, WeaponsF15EX.AMBER_2xAIM260A)
        F15EX_AIM_120C_8_CFT_F = (11, WeaponsF15EX.F15EX_AIM_120C_8_CFT_F)
        F15EX_AIM_120C_7_CFT_F = (11, WeaponsF15EX.F15EX_AIM_120C_7_CFT_F)
        F15EX_AIM_120C_5_CFT_F = (11, WeaponsF15EX.F15EX_AIM_120C_5_CFT_F)
        F15EX_AIM_120D_3_CFT_F = (11, WeaponsF15EX.F15EX_AIM_120D_3_CFT_F)
        F15EX_AIM_120D_CFT_F = (11, WeaponsF15EX.F15EX_AIM_120D_CFT_F)
        F15EX_AIM_200A_CFT_F = (11, WeaponsF15EX.F15EX_AIM_200A_CFT_F)
        AIM200_4XRACK = (11, WeaponsF15EX.AIM200_4XRACK)
        F15EX_AIM_174B_CFT = (11, WeaponsF15EX.F15EX_AIM_174B_CFT)

    class Pylon12:
        F15EX_AIM_120C_8_STA11B = (12, WeaponsF15EX.F15EX_AIM_120C_8_STA11B)
        F15EX_AIM_120C_7_STA11B = (12, WeaponsF15EX.F15EX_AIM_120C_7_STA11B)
        F15EX_AIM_120C_5_STA11B = (12, WeaponsF15EX.F15EX_AIM_120C_5_STA11B)
        F15EX_AIM_120D_3_STA11B = (12, WeaponsF15EX.F15EX_AIM_120D_3_STA11B)
        F15EX_AIM_120D_STA11B = (12, WeaponsF15EX.F15EX_AIM_120D_STA11B)
        F15EX_PYTHON_5_STA11B = (12, WeaponsF15EX.F15EX_PYTHON_5_STA11B)
        F15EX_AIM_9X_ED_STA11B = (12, WeaponsF15EX.F15EX_AIM_9X_ED_STA11B)

    class Pylon13:
        F15EX_AIM_120C_8_STA11A = (13, WeaponsF15EX.F15EX_AIM_120C_8_STA11A)
        F15EX_AIM_120C_7_STA11A = (13, WeaponsF15EX.F15EX_AIM_120C_7_STA11A)
        F15EX_AIM_120C_5_STA11A = (13, WeaponsF15EX.F15EX_AIM_120C_5_STA11A)
        F15EX_AIM_120D_3_STA11A = (13, WeaponsF15EX.F15EX_AIM_120D_3_STA11A)
        F15EX_AIM_120D_STA11A = (13, WeaponsF15EX.F15EX_AIM_120D_STA11A)
        F15EX_PYTHON_5_STA11A = (13, WeaponsF15EX.F15EX_PYTHON_5_STA11A)
        F15EX_AIM_9X_ED_STA11A = (13, WeaponsF15EX.F15EX_AIM_9X_ED_STA11A)

    class Pylon14:
        F15E_EXTTANK = (14, Weapons.Fuel_tank_610_gal_)
        F15E_EXTTANK_EMPTY = (14, Weapons.Fuel_tank_610_gal__Empty_)
        LAU_115_2xAIM_120C_7 = (14, F22AWeapons._2x_AIM_120C7___Active_Radar_AAM)
        F15EX_LAU_115_2xAIM_120C_8 = (14, WeaponsF15EX.F15EX_LAU_115_2xAIM_120C_8)
        LAU_115_2xAIM_120D_3 = (14, F22AWeapons._2x_AIM_120D3___Active_Radar_AAM)
        F15EX_LAU_115_2xAIM_120D = (14, WeaponsF15EX.F15EX_LAU_115_2xAIM_120D)
        F15EX_LAU_115_2xAIM_120C_5 = (14, WeaponsF15EX.F15EX_LAU_115_2xAIM_120C_5)
        AIM200_4XRACK = (14, WeaponsF15EX.AIM200_4XRACK)
        F15EX_AIM_174B = (14, WeaponsF15EX.F15EX_AIM_174B)
        APKWS_II_IRx21 = (14, WeaponsF15EX.APKWS_II_IRx21)
        APKWS_II_IR_x21 = (14, WeaponsF15EX.APKWS_II_IR_x21)

    class Pylon15:
        F15IA_PYTHON_5 = (15, WeaponsF15EX.F15IA_PYTHON_5)
        F15EX_2xAIM_120D_3 = (15, WeaponsF15EX.F15EX_2xAIM_120D_3)
        F15EX_2xAIM_120D = (15, WeaponsF15EX.F15EX_2xAIM_120D)
        F15EX_2xAIM_120C_8 = (15, WeaponsF15EX.F15EX_2xAIM_120C_8)
        F15EX_2xAIM_120C_7 = (15, WeaponsF15EX.F15EX_2xAIM_120C_7)
        F15EX_2xAIM_120C_5 = (15, WeaponsF15EX.F15EX_2xAIM_120C_5)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.Reconnaissance,
    ]
    task_default = task.CAP
