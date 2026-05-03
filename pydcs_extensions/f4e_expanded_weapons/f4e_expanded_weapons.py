from dcs.planes import F_4E_45MC
from dcs.weapons_data import Weapons

from pydcs_extensions.pylon_injector import inject_pylon, eject_pylon
from pydcs_extensions.weapon_injector import inject_weapons


class WeaponsF4EExpanded:
    AGM_45B_Shrike_ARM__LAU_34_ = {
        "clsid": "{LAU_34_AGM_45B}",
        "name": "AGM-45B Shrike ARM (LAU-34)",
        "weight": 224,
        "settings": Weapons.AGM_45A_Shrike_ARM["settings"],
    }
    AGM_65E2_L___Maverick_E2_L__Laser_ASM___Lg_Whd___LAU_117_ = {
        "clsid": "{HB_F4E_AGM-65L_LAU117}",
        "name": "AGM-65E2/L - Maverick E2/L (Laser ASM - Lg Whd) (LAU-117)",
        "weight": 351,
    }
    AGM_65F___Maverick_F__IIR_ASM___Lg_Whd___LAU_117_ = {
        "clsid": "{HB_F4E_AGM-65K_LAU117}",
        "name": "AGM-65F - Maverick F (IIR ASM - Lg Whd) (LAU-117)",
        "weight": 360,
    }
    AGM_65H___Maverick_H__CCD_Imp_ASM___LAU_117_ = {
        "clsid": "{HB_F4E_AGM-65H_LAU117}",
        "name": "AGM-65H - Maverick H (CCD Imp ASM) (LAU-117)",
        "weight": 267,
    }
    AGM_78A_Standard_ARM_ = {
        "clsid": "{LAU_77_AGM_78A}",
        "name": "AGM-78A Standard ARM",
        "weight": 654,
        "settings": Weapons.AGM_45A_Shrike_ARM["settings"],
    }
    AGM_78B_Standard_ARM_ = {
        "clsid": "{LAU_77_AGM_78B}",
        "name": "AGM-78B Standard ARM",
        "weight": 659,
        "settings": Weapons.AGM_78B_Standard_ARM["settings"],
    }
    AIM_4D_Falcon = {
        "clsid": "{AIM-4D}",
        "name": "AIM-4D Falcon",
        "weight": 60.770975056689,
    }
    AIM_9D_Sidewinder_IR_AAM = {
        "clsid": "{AIM-9D}",
        "name": "AIM-9D Sidewinder IR AAM",
        "weight": 88.45,
    }
    AIM_9G_Sidewinder_IR_AAM = {
        "clsid": "{AIM-9G}",
        "name": "AIM-9G Sidewinder IR AAM",
        "weight": 88.45,
    }
    AIM_9H_Sidewinder_IR_AAM = {
        "clsid": "{AIM-9H}",
        "name": "AIM-9H Sidewinder IR AAM",
        "weight": 88.45,
    }
    ALQ_184_Long___ECM_Pod_Rack = {
        "clsid": "{HB_ALQ-184_ON_ADAPTER_IN_AERO7}",
        "name": "ALQ-184 Long - ECM Pod Rack",
        "weight": 240.9,
    }
    AN_AAQ_28_Litening___Targeting_Pod_Rack = {
        "clsid": "{HB_LITENING_ON_ADAPTER_IN_AERO7}",
        "name": "AN/AAQ-28 Litening - Targeting Pod Rack",
        "weight": 217.9,
    }
    CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___LAU_117_ = {
        "clsid": "{HB_F4E_CATM-65K_LAU117}",
        "name": "CATM-65K - Captive Trg Round for Mav K (CCD) (LAU-117)",
        "weight": 356,
    }
    GPU_5 = {
        "clsid": "{GPU_5_POD}",
        "name": "GPU-5",
        "weight": 845.9498,
    }
    TGM_65D___Trg_Round_for_Mav_D__IIR___LAU_117_ = {
        "clsid": "{HB_F4E_TGM-65D_LAU117}",
        "name": "TGM-65D - Trg Round for Mav D (IIR) (LAU-117)",
        "weight": 277,
    }
    TGM_65G___Trg_Round_for_Mav_G__IIR___LAU_117_ = {
        "clsid": "{HB_F4E_TGM-65G_LAU117}",
        "name": "TGM-65G - Trg Round for Mav G (IIR) (LAU-117)",
        "weight": 360,
    }
    TGM_65H___Trg_Round_for_Mav_H__CCD___LAU_117_ = {
        "clsid": "{HB_F4E_TGM-65H_LAU117}",
        "name": "TGM-65H - Trg Round for Mav H (CCD) (LAU-117)",
        "weight": 267,
    }
    _1x_AGM_65A___Maverick_A__TV_Guided___LAU_88_ = {
        "clsid": "{HB_F4EAGM-65A_LAU88_1x}",
        "name": "1x AGM-65A - Maverick A (TV Guided) (LAU-88)",
        "weight": 421.5,
    }
    _1x_AGM_65B___Maverick_B__TV_Guided___LAU_88_ = {
        "clsid": "{HB_F4EAGM-65B_LAU88_1x}",
        "name": "1x AGM-65B - Maverick B (TV Guided) (LAU-88)",
        "weight": 421.5,
    }
    _1x_AGM_65D___Maverick_D__IIR_ASM___LAU_88_ = {
        "clsid": "{HB_F4EAGM-65D_LAU88_1x}",
        "name": "1x AGM-65D - Maverick D (IIR ASM) (LAU-88)",
        "weight": 421.5,
    }
    _1x_AGM_65H___Maverick_H__CCD_Imp_ASM___LAU_88_ = {
        "clsid": "{HB_F4EAGM-65H_LAU88_1x}",
        "name": "1x AGM-65H - Maverick H (CCD Imp ASM) (LAU-88)",
        "weight": 419,
    }
    _1x_TGM_65D___Trg_Round_for_Mav_D__IIR___LAU_88_ = {
        "clsid": "{HB_F4ETGM-65D_LAU88_1x}",
        "name": "1x TGM-65D - Trg Round for Mav D (IIR) (LAU-88)",
        "weight": 429,
    }
    _1x_TGM_65H___Trg_Round_for_Mav_H__CCD___LAU_88_ = {
        "clsid": "{HB_F4ETGM-65H_LAU88_1x}",
        "name": "1x TGM-65H - Trg Round for Mav H (CCD) (LAU-88)",
        "weight": 419,
    }
    _2x_AGM_65H___Maverick_H__CCD_Imp_ASM___LAU_88_ = {
        "clsid": "{HB_F4EAGM-65H_LAU88_2x_Right}",
        "name": "2x AGM-65H - Maverick H (CCD Imp ASM) (LAU-88)",
        "weight": 627,
    }
    _2x_AGM_65H___Maverick_H__CCD_Imp_ASM___LAU_88__ = {
        "clsid": "{HB_F4EAGM-65H_LAU88_2x_Left}",
        "name": "2x AGM-65H - Maverick H (CCD Imp ASM) (LAU-88)",
        "weight": 627,
    }
    _2x_TGM_65D___Trg_Round_for_Mav_D__IIR___LAU_88_ = {
        "clsid": "{HB_F4ETGM-65D_LAU88_2x_Right}",
        "name": "2x TGM-65D - Trg Round for Mav D (IIR) (LAU-88)",
        "weight": 647,
    }
    _2x_TGM_65D___Trg_Round_for_Mav_D__IIR___LAU_88__ = {
        "clsid": "{HB_F4ETGM-65D_LAU88_2x_Left}",
        "name": "2x TGM-65D - Trg Round for Mav D (IIR) (LAU-88)",
        "weight": 647,
    }
    _2x_TGM_65H___Trg_Round_for_Mav_H__CCD___LAU_88_ = {
        "clsid": "{HB_F4ETGM-65H_LAU88_2x_Right}",
        "name": "2x TGM-65H - Trg Round for Mav H (CCD) (LAU-88)",
        "weight": 627,
    }
    _2x_TGM_65H___Trg_Round_for_Mav_H__CCD___LAU_88__ = {
        "clsid": "{HB_F4ETGM-65H_LAU88_2x_Left}",
        "name": "2x TGM-65H - Trg Round for Mav H (CCD) (LAU-88)",
        "weight": 627,
    }
    _3x_AGM_65H___Maverick_H__CCD_Imp_ASM___LAU_88_ = {
        "clsid": "{HB_F4EAGM-65H_LAU88_3x_Right}",
        "name": "3x AGM-65H - Maverick H (CCD Imp ASM) (LAU-88)",
        "weight": 835,
    }
    _3x_AGM_65H___Maverick_H__CCD_Imp_ASM___LAU_88__ = {
        "clsid": "{HB_F4EAGM-65H_LAU88_3x_Left}",
        "name": "3x AGM-65H - Maverick H (CCD Imp ASM) (LAU-88)",
        "weight": 835,
    }
    _3x_TGM_65D___Trg_Round_for_Mav_D__IIR___LAU_88_ = {
        "clsid": "{HB_F4ETGM-65D_LAU88_3x_Right}",
        "name": "3x TGM-65D - Trg Round for Mav D (IIR) (LAU-88)",
        "weight": 865,
    }
    _3x_TGM_65D___Trg_Round_for_Mav_D__IIR___LAU_88__ = {
        "clsid": "{HB_F4ETGM-65D_LAU88_3x_Left}",
        "name": "3x TGM-65D - Trg Round for Mav D (IIR) (LAU-88)",
        "weight": 865,
    }
    _3x_TGM_65H___Trg_Round_for_Mav_H__CCD___LAU_88_ = {
        "clsid": "{HB_F4ETGM-65H_LAU88_3x_Right}",
        "name": "3x TGM-65H - Trg Round for Mav H (CCD) (LAU-88)",
        "weight": 835,
    }
    _3x_TGM_65H___Trg_Round_for_Mav_H__CCD___LAU_88__ = {
        "clsid": "{HB_F4ETGM-65H_LAU88_3x_Left}",
        "name": "3x TGM-65H - Trg Round for Mav H (CCD) (LAU-88)",
        "weight": 835,
    }
    _Special_Weapons_Adapter__AGM_45B_Shrike_ARM__LAU_34_ = {
        "clsid": "{LAU_34_AGM_45B_SWA}",
        "name": "(Special Weapons Adapter) AGM-45B Shrike ARM (LAU-34)",
        "weight": 224,
        "settings": Weapons.AGM_45A_Shrike_ARM["settings"],
    }
    _Special_Weapons_Adapter__AGM_65H___Maverick_H__CCD_Imp_ASM___LAU_117__Special_Weapons_Adapter__ = {
        "clsid": "{HB_F4E_AGM-65H_LAU117_SWA}",
        "name": "(Special Weapons Adapter) AGM-65H - Maverick H (CCD Imp ASM) (LAU-117)(Special Weapons Adapter) ",
        "weight": 267,
    }
    _Special_Weapons_Adapter__TGM_65D___Trg_Round_for_Mav_D__IIR___LAU_117__Special_Weapons_Adapter__ = {
        "clsid": "{HB_F4E_TGM-65D_LAU117_SWA}",
        "name": "(Special Weapons Adapter) TGM-65D - Trg Round for Mav D (IIR) (LAU-117)(Special Weapons Adapter) ",
        "weight": 277,
    }
    _Special_Weapons_Adapter__TGM_65H___Trg_Round_for_Mav_H__CCD___LAU_117__Special_Weapons_Adapter__ = {
        "clsid": "{HB_F4E_TGM-65H_LAU117_SWA}",
        "name": "(Special Weapons Adapter) TGM-65H - Trg Round for Mav H (CCD) (LAU-117)(Special Weapons Adapter) ",
        "weight": 267,
    }


inject_weapons(WeaponsF4EExpanded)


class F4EExpandedPylon1:
    AGM_45B_Shrike_ARM__LAU_34_ = (1, Weapons.AGM_45B_Shrike_ARM__LAU_34_)
    AGM_78A_Standard_ARM_ = (1, Weapons.AGM_78A_Standard_ARM_)
    AGM_78B_Standard_ARM_ = (1, Weapons.AGM_78B_Standard_ARM_)
    AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
        1,
        Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
    )


class F4EExpandedPylon2:
    AIM_4D_Falcon = (2, Weapons.AIM_4D_Falcon)
    AIM_9D_Sidewinder_IR_AAM = (2, Weapons.AIM_9D_Sidewinder_IR_AAM)
    AIM_9G_Sidewinder_IR_AAM = (2, Weapons.AIM_9G_Sidewinder_IR_AAM)
    AIM_9H_Sidewinder_IR_AAM = (2, Weapons.AIM_9H_Sidewinder_IR_AAM)


class F4EExpandedPylon3:
    AGM_45B_Shrike_ARM__LAU_34_ = (3, Weapons.AGM_45B_Shrike_ARM__LAU_34_)
    AGM_65E2_L___Maverick_E2_L__Laser_ASM___Lg_Whd___LAU_117_ = (
        3,
        Weapons.AGM_65E2_L___Maverick_E2_L__Laser_ASM___Lg_Whd___LAU_117_,
    )
    AGM_65F___Maverick_F__IIR_ASM___Lg_Whd___LAU_117_ = (
        3,
        Weapons.AGM_65F___Maverick_F__IIR_ASM___Lg_Whd___LAU_117_,
    )
    AGM_65H___Maverick_H__CCD_Imp_ASM___LAU_117_ = (
        3,
        Weapons.AGM_65H___Maverick_H__CCD_Imp_ASM___LAU_117_,
    )
    AGM_78A_Standard_ARM_ = (3, Weapons.AGM_78A_Standard_ARM_)
    AGM_78B_Standard_ARM_ = (3, Weapons.AGM_78B_Standard_ARM_)
    AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
        3,
        Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
    )
    CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___LAU_117_ = (
        3,
        Weapons.CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___LAU_117_,
    )
    GBU_15_V1___2000_lb_TV_Guided_Bomb = (3, Weapons.GBU_15_V1___2000_lb_TV_Guided_Bomb)
    GPU_5 = (3, Weapons.GPU_5)
    SUU_23 = (3, Weapons.SUU_23)
    TGM_65D___Trg_Round_for_Mav_D__IIR___LAU_117_ = (
        3,
        Weapons.TGM_65D___Trg_Round_for_Mav_D__IIR___LAU_117_,
    )
    TGM_65G___Trg_Round_for_Mav_G__IIR___LAU_117_ = (
        3,
        Weapons.TGM_65G___Trg_Round_for_Mav_G__IIR___LAU_117_,
    )
    TGM_65H___Trg_Round_for_Mav_H__CCD___LAU_117_ = (
        3,
        Weapons.TGM_65H___Trg_Round_for_Mav_H__CCD___LAU_117_,
    )
    _1x_AGM_65A___Maverick_A__TV_Guided___LAU_88_ = (
        3,
        Weapons._1x_AGM_65A___Maverick_A__TV_Guided___LAU_88_,
    )
    _1x_AGM_65B___Maverick_B__TV_Guided___LAU_88_ = (
        3,
        Weapons._1x_AGM_65B___Maverick_B__TV_Guided___LAU_88_,
    )
    _1x_AGM_65D___Maverick_D__IIR_ASM___LAU_88_ = (
        3,
        Weapons._1x_AGM_65D___Maverick_D__IIR_ASM___LAU_88_,
    )
    _1x_AGM_65H___Maverick_H__CCD_Imp_ASM___LAU_88_ = (
        3,
        Weapons._1x_AGM_65H___Maverick_H__CCD_Imp_ASM___LAU_88_,
    )
    _1x_TGM_65D___Trg_Round_for_Mav_D__IIR___LAU_88_ = (
        3,
        Weapons._1x_TGM_65D___Trg_Round_for_Mav_D__IIR___LAU_88_,
    )
    _1x_TGM_65H___Trg_Round_for_Mav_H__CCD___LAU_88_ = (
        3,
        Weapons._1x_TGM_65H___Trg_Round_for_Mav_H__CCD___LAU_88_,
    )
    _2x_AGM_65H___Maverick_H__CCD_Imp_ASM___LAU_88_ = (
        3,
        Weapons._2x_AGM_65H___Maverick_H__CCD_Imp_ASM___LAU_88_,
    )
    _2x_TGM_65D___Trg_Round_for_Mav_D__IIR___LAU_88_ = (
        3,
        Weapons._2x_TGM_65D___Trg_Round_for_Mav_D__IIR___LAU_88_,
    )
    _2x_TGM_65H___Trg_Round_for_Mav_H__CCD___LAU_88_ = (
        3,
        Weapons._2x_TGM_65H___Trg_Round_for_Mav_H__CCD___LAU_88_,
    )
    _3x_AGM_65H___Maverick_H__CCD_Imp_ASM___LAU_88_ = (
        3,
        Weapons._3x_AGM_65H___Maverick_H__CCD_Imp_ASM___LAU_88_,
    )
    _3x_TGM_65D___Trg_Round_for_Mav_D__IIR___LAU_88_ = (
        3,
        Weapons._3x_TGM_65D___Trg_Round_for_Mav_D__IIR___LAU_88_,
    )
    _3x_TGM_65H___Trg_Round_for_Mav_H__CCD___LAU_88_ = (
        3,
        Weapons._3x_TGM_65H___Trg_Round_for_Mav_H__CCD___LAU_88_,
    )
    _Special_Weapons_Adapter__AGM_45B_Shrike_ARM__LAU_34_ = (
        3,
        Weapons._Special_Weapons_Adapter__AGM_45B_Shrike_ARM__LAU_34_,
    )
    _Special_Weapons_Adapter__AGM_65H___Maverick_H__CCD_Imp_ASM___LAU_117__Special_Weapons_Adapter__ = (
        3,
        Weapons._Special_Weapons_Adapter__AGM_65H___Maverick_H__CCD_Imp_ASM___LAU_117__Special_Weapons_Adapter__,
    )
    _Special_Weapons_Adapter__TGM_65D___Trg_Round_for_Mav_D__IIR___LAU_117__Special_Weapons_Adapter__ = (
        3,
        Weapons._Special_Weapons_Adapter__TGM_65D___Trg_Round_for_Mav_D__IIR___LAU_117__Special_Weapons_Adapter__,
    )
    _Special_Weapons_Adapter__TGM_65H___Trg_Round_for_Mav_H__CCD___LAU_117__Special_Weapons_Adapter__ = (
        3,
        Weapons._Special_Weapons_Adapter__TGM_65H___Trg_Round_for_Mav_H__CCD___LAU_117__Special_Weapons_Adapter__,
    )


class F4EExpandedPylon4:
    AIM_4D_Falcon = (4, Weapons.AIM_4D_Falcon)
    AIM_9D_Sidewinder_IR_AAM = (4, Weapons.AIM_9D_Sidewinder_IR_AAM)
    AIM_9G_Sidewinder_IR_AAM = (4, Weapons.AIM_9G_Sidewinder_IR_AAM)
    AIM_9H_Sidewinder_IR_AAM = (4, Weapons.AIM_9H_Sidewinder_IR_AAM)


class F4EExpandedPylon5:
    AIM_120B_AMRAAM___Active_Radar_AAM = (5, Weapons.AIM_120B_AMRAAM___Active_Radar_AAM)
    AIM_120C_AMRAAM___Active_Radar_AAM = (5, Weapons.AIM_120C_AMRAAM___Active_Radar_AAM)
    AIM_7MH = (5, Weapons.AIM_7MH)
    AIM_7P = (5, Weapons.AIM_7P)


class F4EExpandedPylon6:
    AIM_120B_AMRAAM___Active_Radar_AAM = (6, Weapons.AIM_120B_AMRAAM___Active_Radar_AAM)
    AIM_120C_AMRAAM___Active_Radar_AAM = (6, Weapons.AIM_120C_AMRAAM___Active_Radar_AAM)
    AIM_7MH = (6, Weapons.AIM_7MH)
    AIM_7P = (6, Weapons.AIM_7P)
    ALQ_184_Long___ECM_Pod_Rack = (6, Weapons.ALQ_184_Long___ECM_Pod_Rack)
    AN_AAQ_28_Litening___Targeting_Pod_Rack = (
        6,
        Weapons.AN_AAQ_28_Litening___Targeting_Pod_Rack,
    )


class F4EExpandedPylon7:
    AN_AXQ_14_Data_Link_Pod = (7, Weapons.AN_AXQ_14_Data_Link_Pod)
    GPU_5 = (7, Weapons.GPU_5)


class F4EExpandedPylon8:
    AIM_120B_AMRAAM___Active_Radar_AAM = (8, Weapons.AIM_120B_AMRAAM___Active_Radar_AAM)
    AIM_120C_AMRAAM___Active_Radar_AAM = (8, Weapons.AIM_120C_AMRAAM___Active_Radar_AAM)
    AIM_7MH = (8, Weapons.AIM_7MH)
    AIM_7P = (8, Weapons.AIM_7P)


class F4EExpandedPylon9:
    AIM_120B_AMRAAM___Active_Radar_AAM = (9, Weapons.AIM_120B_AMRAAM___Active_Radar_AAM)
    AIM_120C_AMRAAM___Active_Radar_AAM = (9, Weapons.AIM_120C_AMRAAM___Active_Radar_AAM)
    AIM_7MH = (9, Weapons.AIM_7MH)
    AIM_7P = (9, Weapons.AIM_7P)


class F4EExpandedPylon10:
    AIM_4D_Falcon = (10, Weapons.AIM_4D_Falcon)
    AIM_9D_Sidewinder_IR_AAM = (10, Weapons.AIM_9D_Sidewinder_IR_AAM)
    AIM_9G_Sidewinder_IR_AAM = (10, Weapons.AIM_9G_Sidewinder_IR_AAM)
    AIM_9H_Sidewinder_IR_AAM = (10, Weapons.AIM_9H_Sidewinder_IR_AAM)


class F4EExpandedPylon11:
    AGM_45B_Shrike_ARM__LAU_34_ = (11, Weapons.AGM_45B_Shrike_ARM__LAU_34_)
    AGM_65E2_L___Maverick_E2_L__Laser_ASM___Lg_Whd___LAU_117_ = (
        11,
        Weapons.AGM_65E2_L___Maverick_E2_L__Laser_ASM___Lg_Whd___LAU_117_,
    )
    AGM_65F___Maverick_F__IIR_ASM___Lg_Whd___LAU_117_ = (
        11,
        Weapons.AGM_65F___Maverick_F__IIR_ASM___Lg_Whd___LAU_117_,
    )
    AGM_65H___Maverick_H__CCD_Imp_ASM___LAU_117_ = (
        11,
        Weapons.AGM_65H___Maverick_H__CCD_Imp_ASM___LAU_117_,
    )
    AGM_78A_Standard_ARM_ = (11, Weapons.AGM_78A_Standard_ARM_)
    AGM_78B_Standard_ARM_ = (11, Weapons.AGM_78B_Standard_ARM_)
    AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
        11,
        Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
    )
    CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___LAU_117_ = (
        11,
        Weapons.CATM_65K___Captive_Trg_Round_for_Mav_K__CCD___LAU_117_,
    )
    GBU_15_V1___2000_lb_TV_Guided_Bomb = (
        11,
        Weapons.GBU_15_V1___2000_lb_TV_Guided_Bomb,
    )
    GPU_5 = (11, Weapons.GPU_5)
    SUU_23 = (11, Weapons.SUU_23)
    TGM_65D___Trg_Round_for_Mav_D__IIR___LAU_117_ = (
        11,
        Weapons.TGM_65D___Trg_Round_for_Mav_D__IIR___LAU_117_,
    )
    TGM_65G___Trg_Round_for_Mav_G__IIR___LAU_117_ = (
        11,
        Weapons.TGM_65G___Trg_Round_for_Mav_G__IIR___LAU_117_,
    )
    TGM_65H___Trg_Round_for_Mav_H__CCD___LAU_117_ = (
        11,
        Weapons.TGM_65H___Trg_Round_for_Mav_H__CCD___LAU_117_,
    )
    _1x_AGM_65A___Maverick_A__TV_Guided___LAU_88_ = (
        11,
        Weapons._1x_AGM_65A___Maverick_A__TV_Guided___LAU_88_,
    )
    _1x_AGM_65B___Maverick_B__TV_Guided___LAU_88_ = (
        11,
        Weapons._1x_AGM_65B___Maverick_B__TV_Guided___LAU_88_,
    )
    _1x_AGM_65D___Maverick_D__IIR_ASM___LAU_88_ = (
        11,
        Weapons._1x_AGM_65D___Maverick_D__IIR_ASM___LAU_88_,
    )
    _1x_AGM_65H___Maverick_H__CCD_Imp_ASM___LAU_88_ = (
        11,
        Weapons._1x_AGM_65H___Maverick_H__CCD_Imp_ASM___LAU_88_,
    )
    _1x_TGM_65D___Trg_Round_for_Mav_D__IIR___LAU_88_ = (
        11,
        Weapons._1x_TGM_65D___Trg_Round_for_Mav_D__IIR___LAU_88_,
    )
    _1x_TGM_65H___Trg_Round_for_Mav_H__CCD___LAU_88_ = (
        11,
        Weapons._1x_TGM_65H___Trg_Round_for_Mav_H__CCD___LAU_88_,
    )
    _2x_AGM_65H___Maverick_H__CCD_Imp_ASM___LAU_88_ = (
        11,
        Weapons._2x_AGM_65H___Maverick_H__CCD_Imp_ASM___LAU_88_,
    )
    _2x_TGM_65D___Trg_Round_for_Mav_D__IIR___LAU_88_ = (
        11,
        Weapons._2x_TGM_65D___Trg_Round_for_Mav_D__IIR___LAU_88_,
    )
    _2x_TGM_65H___Trg_Round_for_Mav_H__CCD___LAU_88_ = (
        11,
        Weapons._2x_TGM_65H___Trg_Round_for_Mav_H__CCD___LAU_88_,
    )
    _3x_AGM_65H___Maverick_H__CCD_Imp_ASM___LAU_88_ = (
        11,
        Weapons._3x_AGM_65H___Maverick_H__CCD_Imp_ASM___LAU_88_,
    )
    _3x_TGM_65D___Trg_Round_for_Mav_D__IIR___LAU_88_ = (
        11,
        Weapons._3x_TGM_65D___Trg_Round_for_Mav_D__IIR___LAU_88_,
    )
    _3x_TGM_65H___Trg_Round_for_Mav_H__CCD___LAU_88_ = (
        11,
        Weapons._3x_TGM_65H___Trg_Round_for_Mav_H__CCD___LAU_88_,
    )
    _Special_Weapons_Adapter__AGM_45B_Shrike_ARM__LAU_34_ = (
        11,
        Weapons._Special_Weapons_Adapter__AGM_45B_Shrike_ARM__LAU_34_,
    )
    _Special_Weapons_Adapter__AGM_65H___Maverick_H__CCD_Imp_ASM___LAU_117__Special_Weapons_Adapter__ = (
        11,
        Weapons._Special_Weapons_Adapter__AGM_65H___Maverick_H__CCD_Imp_ASM___LAU_117__Special_Weapons_Adapter__,
    )
    _Special_Weapons_Adapter__TGM_65D___Trg_Round_for_Mav_D__IIR___LAU_117__Special_Weapons_Adapter__ = (
        11,
        Weapons._Special_Weapons_Adapter__TGM_65D___Trg_Round_for_Mav_D__IIR___LAU_117__Special_Weapons_Adapter__,
    )
    _Special_Weapons_Adapter__TGM_65H___Trg_Round_for_Mav_H__CCD___LAU_117__Special_Weapons_Adapter__ = (
        11,
        Weapons._Special_Weapons_Adapter__TGM_65H___Trg_Round_for_Mav_H__CCD___LAU_117__Special_Weapons_Adapter__,
    )


class F4EExpandedPylon12:
    AIM_4D_Falcon = (12, Weapons.AIM_4D_Falcon)
    AIM_9D_Sidewinder_IR_AAM = (12, Weapons.AIM_9D_Sidewinder_IR_AAM)
    AIM_9G_Sidewinder_IR_AAM = (12, Weapons.AIM_9G_Sidewinder_IR_AAM)
    AIM_9H_Sidewinder_IR_AAM = (12, Weapons.AIM_9H_Sidewinder_IR_AAM)


class F4EExpandedPylon13:
    AGM_45B_Shrike_ARM__LAU_34_ = (13, Weapons.AGM_45B_Shrike_ARM__LAU_34_)
    AGM_78A_Standard_ARM_ = (13, Weapons.AGM_78A_Standard_ARM_)
    AGM_78B_Standard_ARM_ = (13, Weapons.AGM_78B_Standard_ARM_)
    AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
        13,
        Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
    )


def inject_F4E() -> None:
    inject_pylon(F_4E_45MC.Pylon1, F4EExpandedPylon1)
    inject_pylon(F_4E_45MC.Pylon2, F4EExpandedPylon2)
    inject_pylon(F_4E_45MC.Pylon3, F4EExpandedPylon3)
    inject_pylon(F_4E_45MC.Pylon4, F4EExpandedPylon4)
    inject_pylon(F_4E_45MC.Pylon5, F4EExpandedPylon5)
    inject_pylon(F_4E_45MC.Pylon6, F4EExpandedPylon6)
    inject_pylon(F_4E_45MC.Pylon7, F4EExpandedPylon7)
    inject_pylon(F_4E_45MC.Pylon8, F4EExpandedPylon8)
    inject_pylon(F_4E_45MC.Pylon9, F4EExpandedPylon9)
    inject_pylon(F_4E_45MC.Pylon10, F4EExpandedPylon10)
    inject_pylon(F_4E_45MC.Pylon11, F4EExpandedPylon11)
    inject_pylon(F_4E_45MC.Pylon12, F4EExpandedPylon12)
    inject_pylon(F_4E_45MC.Pylon13, F4EExpandedPylon13)


def eject_F4E() -> None:
    eject_pylon(F_4E_45MC.Pylon1, F4EExpandedPylon1)
    eject_pylon(F_4E_45MC.Pylon2, F4EExpandedPylon2)
    eject_pylon(F_4E_45MC.Pylon3, F4EExpandedPylon3)
    eject_pylon(F_4E_45MC.Pylon4, F4EExpandedPylon4)
    eject_pylon(F_4E_45MC.Pylon5, F4EExpandedPylon5)
    eject_pylon(F_4E_45MC.Pylon6, F4EExpandedPylon6)
    eject_pylon(F_4E_45MC.Pylon7, F4EExpandedPylon7)
    eject_pylon(F_4E_45MC.Pylon8, F4EExpandedPylon8)
    eject_pylon(F_4E_45MC.Pylon9, F4EExpandedPylon9)
    eject_pylon(F_4E_45MC.Pylon10, F4EExpandedPylon10)
    eject_pylon(F_4E_45MC.Pylon11, F4EExpandedPylon11)
    eject_pylon(F_4E_45MC.Pylon12, F4EExpandedPylon12)
    eject_pylon(F_4E_45MC.Pylon13, F4EExpandedPylon13)
