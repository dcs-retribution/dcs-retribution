from enum import Enum
from typing import Dict, Any

from dcs import task
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

from game.modsupport import planemod
from pydcs_extensions.weapon_injector import inject_weapons


class WeaponsF4B:
    F4B_SUU_23_Gun_Pod = {
        "clsid": "{VSN_F4B_Gunpod}",
        "name": "F4B SUU-23 Gun Pod",
        "weight": 112.35,
    }
    VSN_F4EC_PTB = {
        "clsid": "VSN_F4EC_PTB",
        "name": "Fuel tank 600 Gal",
        "weight": 1980,
    }
    VSN_F4EL_PTB = {
        "clsid": "VSN_F4EL_PTB",
        "name": "Fuel tank 370 Gal",
        "weight": 1240,
    }
    VSN_F4ER_PTB = {
        "clsid": "VSN_F4ER_PTB",
        "name": "Fuel tank 370 Gal",
        "weight": 1240,
    }


inject_weapons(WeaponsF4B)


@planemod
class VSN_F4B(PlaneType):
    id = "VSN_F4B"
    flyable = True
    height = 5.02
    width = 11.71
    length = 19.2
    fuel_max = 6416
    max_speed = 2545.2
    chaff = 48
    flare = 48
    charge_total = 96
    chaff_charge_size = 1
    flare_charge_size = 1
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    class Liveries:
        class USSR(Enum):
            VF_121_118 = "VF-121-118"

        class Georgia(Enum):
            VF_121_118 = "VF-121-118"

        class Venezuela(Enum):
            VF_121_118 = "VF-121-118"

        class Australia(Enum):
            VF_121_118 = "VF-121-118"

        class Israel(Enum):
            VF_121_118 = "VF-121-118"

        class Combined_Joint_Task_Forces_Blue(Enum):
            VF_121_118 = "VF-121-118"

        class Sudan(Enum):
            VF_121_118 = "VF-121-118"

        class Norway(Enum):
            VF_121_118 = "VF-121-118"

        class Romania(Enum):
            VF_121_118 = "VF-121-118"

        class Iran(Enum):
            VF_121_118 = "VF-121-118"

        class Ukraine(Enum):
            VF_121_118 = "VF-121-118"

        class Libya(Enum):
            VF_121_118 = "VF-121-118"

        class Belgium(Enum):
            VF_121_118 = "VF-121-118"

        class Slovakia(Enum):
            VF_121_118 = "VF-121-118"

        class Greece(Enum):
            VF_121_118 = "VF-121-118"

        class UK(Enum):
            VF_121_118 = "VF-121-118"

        class Third_Reich(Enum):
            VF_121_118 = "VF-121-118"

        class Hungary(Enum):
            VF_121_118 = "VF-121-118"

        class Abkhazia(Enum):
            VF_121_118 = "VF-121-118"

        class Morocco(Enum):
            VF_121_118 = "VF-121-118"

        class United_Nations_Peacekeepers(Enum):
            VF_121_118 = "VF-121-118"

        class Switzerland(Enum):
            VF_121_118 = "VF-121-118"

        class SouthOssetia(Enum):
            VF_121_118 = "VF-121-118"

        class Vietnam(Enum):
            VF_121_118 = "VF-121-118"

        class China(Enum):
            VF_121_118 = "VF-121-118"

        class Yemen(Enum):
            VF_121_118 = "VF-121-118"

        class Kuwait(Enum):
            VF_121_118 = "VF-121-118"

        class Serbia(Enum):
            VF_121_118 = "VF-121-118"

        class Oman(Enum):
            VF_121_118 = "VF-121-118"

        class India(Enum):
            VF_121_118 = "VF-121-118"

        class Egypt(Enum):
            VF_121_118 = "VF-121-118"

        class TheNetherlands(Enum):
            VF_121_118 = "VF-121-118"

        class Poland(Enum):
            VF_121_118 = "VF-121-118"

        class Syria(Enum):
            VF_121_118 = "VF-121-118"

        class Finland(Enum):
            VF_121_118 = "VF-121-118"

        class Kazakhstan(Enum):
            VF_121_118 = "VF-121-118"

        class Denmark(Enum):
            VF_121_118 = "VF-121-118"

        class Sweden(Enum):
            VF_121_118 = "VF-121-118"

        class Croatia(Enum):
            VF_121_118 = "VF-121-118"

        class CzechRepublic(Enum):
            VF_121_118 = "VF-121-118"

        class GDR(Enum):
            VF_121_118 = "VF-121-118"

        class Yugoslavia(Enum):
            VF_121_118 = "VF-121-118"

        class Bulgaria(Enum):
            VF_121_118 = "VF-121-118"

        class SouthKorea(Enum):
            VF_121_118 = "VF-121-118"

        class Tunisia(Enum):
            VF_121_118 = "VF-121-118"

        class Combined_Joint_Task_Forces_Red(Enum):
            VF_121_118 = "VF-121-118"

        class Lebanon(Enum):
            VF_121_118 = "VF-121-118"

        class Portugal(Enum):
            VF_121_118 = "VF-121-118"

        class Cuba(Enum):
            VF_121_118 = "VF-121-118"

        class Insurgents(Enum):
            VF_121_118 = "VF-121-118"

        class SaudiArabia(Enum):
            VF_121_118 = "VF-121-118"

        class France(Enum):
            VF_121_118 = "VF-121-118"

        class USA(Enum):
            VF_121_118 = "VF-121-118"

        class Honduras(Enum):
            VF_121_118 = "VF-121-118"

        class Qatar(Enum):
            VF_121_118 = "VF-121-118"

        class Russia(Enum):
            VF_121_118 = "VF-121-118"

        class United_Arab_Emirates(Enum):
            VF_121_118 = "VF-121-118"

        class Italian_Social_Republi(Enum):
            VF_121_118 = "VF-121-118"

        class Austria(Enum):
            VF_121_118 = "VF-121-118"

        class Bahrain(Enum):
            VF_121_118 = "VF-121-118"

        class Italy(Enum):
            VF_121_118 = "VF-121-118"

        class Chile(Enum):
            VF_121_118 = "VF-121-118"

        class Turkey(Enum):
            VF_121_118 = "VF-121-118"

        class Philippines(Enum):
            VF_121_118 = "VF-121-118"

        class Algeria(Enum):
            VF_121_118 = "VF-121-118"

        class Pakistan(Enum):
            VF_121_118 = "VF-121-118"

        class Malaysia(Enum):
            VF_121_118 = "VF-121-118"

        class Indonesia(Enum):
            VF_121_118 = "VF-121-118"

        class Iraq(Enum):
            VF_121_118 = "VF-121-118"

        class Germany(Enum):
            VF_121_118 = "VF-121-118"

        class South_Africa(Enum):
            VF_121_118 = "VF-121-118"

        class Jordan(Enum):
            VF_121_118 = "VF-121-118"

        class Mexico(Enum):
            VF_121_118 = "VF-121-118"

        class USAFAggressors(Enum):
            VF_121_118 = "VF-121-118"

        class Brazil(Enum):
            VF_121_118 = "VF-121-118"

        class Spain(Enum):
            VF_121_118 = "VF-121-118"

        class Belarus(Enum):
            VF_121_118 = "VF-121-118"

        class Canada(Enum):
            VF_121_118 = "VF-121-118"

        class NorthKorea(Enum):
            VF_121_118 = "VF-121-118"

        class Ethiopia(Enum):
            VF_121_118 = "VF-121-118"

        class Japan(Enum):
            VF_121_118 = "VF-121-118"

        class Thailand(Enum):
            VF_121_118 = "VF-121-118"

    class Pylon1:
        Smoke_Generator___red_ = (1, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (1, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (1, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (1, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (1, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (1, Weapons.Smoke_Generator___orange_)

    class Pylon2:
        GBU_10___2000lb_Laser_Guided_Bomb = (
            2,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (2, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        BRU_42_with_3_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets = (
            2,
            Weapons.BRU_42_with_3_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets,
        )
        Mk_84___2000lb_GP_Bomb_LD = (2, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            2,
            Weapons.LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            2,
            Weapons.LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        _3_x_LAU_61_pods___57_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            2,
            Weapons._3_x_LAU_61_pods___57_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos = (
            2,
            Weapons.LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos,
        )
        LAU_118a_with_AGM_45B_Shrike_ARM__Imp_ = (
            2,
            Weapons.LAU_118a_with_AGM_45B_Shrike_ARM__Imp_,
        )
        Smokewinder___red = (2, Weapons.Smokewinder___red)
        Smokewinder___green = (2, Weapons.Smokewinder___green)
        Smokewinder___blue = (2, Weapons.Smokewinder___blue)
        Smokewinder___white = (2, Weapons.Smokewinder___white)
        Smokewinder___yellow = (2, Weapons.Smokewinder___yellow)
        BRU_33_with_2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            2,
            Weapons.BRU_33_with_2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            2,
            Weapons.BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_41A_with_6_x_Mk_82___500lb_GP_Bomb_LD = (
            2,
            Weapons.BRU_41A_with_6_x_Mk_82___500lb_GP_Bomb_LD,
        )
        BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb = (
            2,
            Weapons.BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        VSN_F4EL_PTB = (2, WeaponsF4B.VSN_F4EL_PTB)

    class Pylon3:
        GBU_10___2000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (3, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        BRU_42_with_3_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets = (
            3,
            Weapons.BRU_42_with_3_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets,
        )
        BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD = (
            3,
            Weapons.BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (3, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        LAU_88_with_2_x_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            3,
            Weapons.LAU_88_with_2_x_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM_ = (
            3,
            Weapons.LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_118a_with_AGM_45B_Shrike_ARM__Imp_ = (
            3,
            Weapons.LAU_118a_with_AGM_45B_Shrike_ARM__Imp_,
        )
        LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            3,
            Weapons.LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        _3_x_LAU_61_pods___57_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            3,
            Weapons._3_x_LAU_61_pods___57_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_33_with_2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            3,
            Weapons.BRU_33_with_2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            3,
            Weapons.BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM_ = (
            3,
            Weapons.LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_ = (
            3,
            Weapons.LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_105_with_2_x_AIM_9M_Sidewinder_IR_AAM = (
            3,
            Weapons.LAU_105_with_2_x_AIM_9M_Sidewinder_IR_AAM,
        )
        LAU_105_2_AIM_9L = (3, Weapons.LAU_105_2_AIM_9L)
        LAU_105_2_AIM_9P5 = (3, Weapons.LAU_105_2_AIM_9P5)
        AIM_120B_AMRAAM___Active_Rdr_AAM = (3, Weapons.AIM_120B_AMRAAM___Active_Rdr_AAM)
        AIM_7F_Sparrow_Semi_Active_Radar = (3, Weapons.AIM_7F_Sparrow_Semi_Active_Radar)
        AIM_7E_Sparrow_Semi_Active_Radar = (3, Weapons.AIM_7E_Sparrow_Semi_Active_Radar)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            3,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        Mk_82___500lb_GP_Bomb_LD = (3, Weapons.Mk_82___500lb_GP_Bomb_LD)
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            3,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        BRU_33_with_2_x_Mk_83___1000lb_GP_Bomb_LD = (
            3,
            Weapons.BRU_33_with_2_x_Mk_83___1000lb_GP_Bomb_LD,
        )

    class Pylon4:
        AIM_7M_Sparrow_Semi_Active_Radar = (4, Weapons.AIM_7M_Sparrow_Semi_Active_Radar)
        AIM_7F_Sparrow_Semi_Active_Radar = (4, Weapons.AIM_7F_Sparrow_Semi_Active_Radar)
        AIM_7E_Sparrow_Semi_Active_Radar = (4, Weapons.AIM_7E_Sparrow_Semi_Active_Radar)
        AIM_120B_AMRAAM___Active_Rdr_AAM = (4, Weapons.AIM_120B_AMRAAM___Active_Rdr_AAM)

    class Pylon5:
        AIM_7M_Sparrow_Semi_Active_Radar = (5, Weapons.AIM_7M_Sparrow_Semi_Active_Radar)
        AIM_7F_Sparrow_Semi_Active_Radar = (5, Weapons.AIM_7F_Sparrow_Semi_Active_Radar)
        AIM_7E_Sparrow_Semi_Active_Radar = (5, Weapons.AIM_7E_Sparrow_Semi_Active_Radar)
        AIM_120B_AMRAAM___Active_Rdr_AAM = (5, Weapons.AIM_120B_AMRAAM___Active_Rdr_AAM)

    class Pylon6:
        Smokewinder___red = (6, Weapons.Smokewinder___red)
        Smokewinder___green = (6, Weapons.Smokewinder___green)
        Smokewinder___blue = (6, Weapons.Smokewinder___blue)
        Smokewinder___white = (6, Weapons.Smokewinder___white)
        Smokewinder___yellow = (6, Weapons.Smokewinder___yellow)
        BRU_41A_with_6_x_Mk_82___500lb_GP_Bomb_LD = (
            6,
            Weapons.BRU_41A_with_6_x_Mk_82___500lb_GP_Bomb_LD,
        )
        _3_x_LAU_61_pods___57_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            6,
            Weapons._3_x_LAU_61_pods___57_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD = (
            6,
            Weapons.BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD,
        )
        ALQ_131___ECM_Pod = (6, Weapons.ALQ_131___ECM_Pod)
        F4B_SUU_23_Gun_Pod = (6, WeaponsF4B.F4B_SUU_23_Gun_Pod)
        VSN_F4EC_PTB = (6, WeaponsF4B.VSN_F4EC_PTB)

    class Pylon7:
        AIM_7M_Sparrow_Semi_Active_Radar = (7, Weapons.AIM_7M_Sparrow_Semi_Active_Radar)
        AIM_7F_Sparrow_Semi_Active_Radar = (7, Weapons.AIM_7F_Sparrow_Semi_Active_Radar)
        AIM_7E_Sparrow_Semi_Active_Radar = (7, Weapons.AIM_7E_Sparrow_Semi_Active_Radar)
        AIM_120B_AMRAAM___Active_Rdr_AAM = (7, Weapons.AIM_120B_AMRAAM___Active_Rdr_AAM)

    class Pylon8:
        AIM_7M_Sparrow_Semi_Active_Radar = (8, Weapons.AIM_7M_Sparrow_Semi_Active_Radar)
        AIM_7F_Sparrow_Semi_Active_Radar = (8, Weapons.AIM_7F_Sparrow_Semi_Active_Radar)
        AIM_7E_Sparrow_Semi_Active_Radar = (8, Weapons.AIM_7E_Sparrow_Semi_Active_Radar)
        AIM_120B_AMRAAM___Active_Rdr_AAM = (8, Weapons.AIM_120B_AMRAAM___Active_Rdr_AAM)

    class Pylon9:
        GBU_10___2000lb_Laser_Guided_Bomb = (
            9,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (9, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        BRU_42_with_3_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets = (
            9,
            Weapons.BRU_42_with_3_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets,
        )
        BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD = (
            9,
            Weapons.BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (9, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        LAU_88_with_2_x_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            9,
            Weapons.LAU_88_with_2_x_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM_ = (
            9,
            Weapons.LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_118a_with_AGM_45B_Shrike_ARM__Imp_ = (
            9,
            Weapons.LAU_118a_with_AGM_45B_Shrike_ARM__Imp_,
        )
        LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            9,
            Weapons.LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        _3_x_LAU_61_pods___57_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            9,
            Weapons._3_x_LAU_61_pods___57_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_33_with_2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            9,
            Weapons.BRU_33_with_2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            9,
            Weapons.BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM_ = (
            9,
            Weapons.LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_ = (
            9,
            Weapons.LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_105_with_2_x_AIM_9M_Sidewinder_IR_AAM = (
            9,
            Weapons.LAU_105_with_2_x_AIM_9M_Sidewinder_IR_AAM,
        )
        LAU_105_2_AIM_9L = (9, Weapons.LAU_105_2_AIM_9L)
        LAU_105_2_AIM_9P5 = (9, Weapons.LAU_105_2_AIM_9P5)
        AIM_120B_AMRAAM___Active_Rdr_AAM = (9, Weapons.AIM_120B_AMRAAM___Active_Rdr_AAM)
        AIM_7F_Sparrow_Semi_Active_Radar = (9, Weapons.AIM_7F_Sparrow_Semi_Active_Radar)
        AIM_7E_Sparrow_Semi_Active_Radar = (9, Weapons.AIM_7E_Sparrow_Semi_Active_Radar)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            9,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        Mk_82___500lb_GP_Bomb_LD = (9, Weapons.Mk_82___500lb_GP_Bomb_LD)
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            9,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        BRU_33_with_2_x_Mk_83___1000lb_GP_Bomb_LD = (
            9,
            Weapons.BRU_33_with_2_x_Mk_83___1000lb_GP_Bomb_LD,
        )

    class Pylon10:
        GBU_10___2000lb_Laser_Guided_Bomb = (
            10,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (
            10,
            Weapons.GBU_12___500lb_Laser_Guided_Bomb,
        )
        BRU_42_with_3_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets = (
            10,
            Weapons.BRU_42_with_3_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets,
        )
        Mk_84___2000lb_GP_Bomb_LD = (10, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            10,
            Weapons.LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            10,
            Weapons.LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        _3_x_LAU_61_pods___57_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            10,
            Weapons._3_x_LAU_61_pods___57_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos = (
            10,
            Weapons.LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos,
        )
        LAU_118a_with_AGM_45B_Shrike_ARM__Imp_ = (
            10,
            Weapons.LAU_118a_with_AGM_45B_Shrike_ARM__Imp_,
        )
        Smokewinder___red = (10, Weapons.Smokewinder___red)
        Smokewinder___green = (10, Weapons.Smokewinder___green)
        Smokewinder___blue = (10, Weapons.Smokewinder___blue)
        Smokewinder___white = (10, Weapons.Smokewinder___white)
        Smokewinder___yellow = (10, Weapons.Smokewinder___yellow)
        BRU_33_with_2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            10,
            Weapons.BRU_33_with_2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            10,
            Weapons.BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_41A_with_6_x_Mk_82___500lb_GP_Bomb_LD = (
            10,
            Weapons.BRU_41A_with_6_x_Mk_82___500lb_GP_Bomb_LD,
        )
        BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb = (
            10,
            Weapons.BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        VSN_F4ER_PTB = (10, WeaponsF4B.VSN_F4ER_PTB)

    class Pylon11:
        L005_Sorbtsiya_ECM_pod__left_ = (11, Weapons.L005_Sorbtsiya_ECM_pod__left_)
        L_081_Fantasmagoria_ELINT_pod = (11, Weapons.L_081_Fantasmagoria_ELINT_pod)

    pylons = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.Reconnaissance,
        task.GroundAttack,
        task.CAS,
        task.AFAC,
        task.RunwayAttack,
    ]
    task_default = task.CAP
