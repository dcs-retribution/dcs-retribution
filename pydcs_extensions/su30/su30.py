from typing import Dict, Any, Set

from dcs import task
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

from game.modsupport import planemod
from pydcs_extensions.weapon_injector import inject_weapons


class WeaponsSu30:
    ASTRA_Mk_1___Active_Rdr_AAM = {
        "clsid": "{Su30_ASTRA}",
        "name": "ASTRA Mk.1 - Active Rdr AAM",
        "weight": 154,
    }

    APK_9_POD = {"clsid": "{SU30_APK-9}", "name": "APK-9 POD", "weight": 295}

    BRAHMOS_A_Ship = {"clsid": "{BRAHMOS_S}", "name": "BRAHMOS A-Ship", "weight": 2500}

    DAMOCLES___Targeting_Pod = {
        "clsid": "{DAMOCLES}",
        "name": "DAMOCLES - Targeting Pod",
        "weight": 208,
    }

    EL_M_2060 = {"clsid": "{SU30_ELM2060}", "name": "EL/M-2060", "weight": 295}

    FAB_500_M54___474kg = {
        "clsid": "{Su30_FAB500M54}",
        "name": "FAB-500 M54 - 474kg",
        "weight": 506,
    }

    FAB_500_M62___474kg = {
        "clsid": "{Su30_FAB500M62}",
        "name": "FAB-500 M62 - 474kg",
        "weight": 506,
    }

    FAB_250_M62___227kg = {
        "clsid": "{Su30_FAB250M62}",
        "name": "FAB-250 M62 - 227kg",
        "weight": 506,
    }

    FAB_500_M62_UMPK = {
        "clsid": "{Su30_UMPKFAB500M62}",
        "name": "FAB-500 M62 UMPK",
        "weight": 570,
    }

    FAB_500_M62_NV___500kg = {
        "clsid": "{Su30_FAB500M62NV}",
        "name": "FAB-500 M62 NV - 500kg",
        "weight": 277,
    }

    GBU_38___JDAM__500lb_GPS_Guided_Bomb = {
        "clsid": "{SU30_GBU_38}",
        "name": "GBU-38 - JDAM, 500lb GPS Guided Bomb",
        "weight": 321,
    }

    I_Derby_ER___Active_Rdr_AAM = {
        "clsid": "{Su30_DERBY_ER}",
        "name": "I-Derby ER - Active Rdr AAM",
        "weight": 118,
    }

    Kh_31P = {"clsid": "{SU30_KH31P}", "name": "Kh-31P", "weight": 690}

    KH_31PD__AA_ = {"clsid": "{SU30_KH31PDAA}", "name": "KH-31PD (AA)", "weight": 893}

    Kh_36_Grom_1 = {"clsid": "{SU30_KH36}", "name": "Kh-36 Grom-1", "weight": 690}

    KH_38MTE = {"clsid": "{SU30_KH38MTE}", "name": "KH-38MTE", "weight": 1240}

    KH_38MLE = {"clsid": "{SU30_KH38MLE}", "name": "KH-38MLE", "weight": 520}

    KH_38MAE = {"clsid": "{SU30_KH38MAE}", "name": "KH-38MAE", "weight": 520}

    KH_29L__AS_14_Kedge___Semi_Act_Laser = {
        "clsid": "{SU30_KH29L}",
        "name": "KH-29L (AS-14 Kedge), Semi-Act Laser",
        "weight": 657,
    }

    KH_29TE__AS_14_Kedge___TV_Guided = {
        "clsid": "{SU30_KH29TE}",
        "name": "KH-29TE (AS-14 Kedge), TV Guided",
        "weight": 1240,
    }

    Kh_59M = {"clsid": "{SU30_KH59M}", "name": "Kh-59M", "weight": 930}

    Kh_59MK = {"clsid": "{SU30_KH59MK}", "name": "Kh-59MK", "weight": 770}

    Kh_59MK2_ = {"clsid": "{SU30_KH59MK2}", "name": "Kh-59MK2", "weight": 770}

    Kh_31A = {"clsid": "{SU30_KH_31A}", "name": "Kh-31A", "weight": 690}

    Kh_31P_AA = {"clsid": "{SU30_KH31PAA}", "name": "Kh-31P AA", "weight": 786}

    KH_35A = {"clsid": "{SU30_KH_35}", "name": "KH-35A", "weight": 540}

    KH_35UE = {"clsid": "{SU30_KH_35UE}", "name": "KH-35UE", "weight": 540}

    KH_31AD = {"clsid": "{SU30_KH31AD}", "name": "KH-31AD", "weight": 690}

    KH_31PD = {"clsid": "{SU30_KH31PD}", "name": "KH-31PD", "weight": 690}

    KAB_500S___500kg = {
        "clsid": "{SU30_KAB_500S_LOADOUT}",
        "name": "KAB-500S - 500kg",
        "weight": 500,
    }

    KAB_1500Kr___1500kg = {
        "clsid": "{SU30_KAB_1500Kr_LOADOUT}",
        "name": "KAB-1500Kr - 1500kg",
        "weight": 1560,
    }

    KAB_1500LG_PR___1500kg = {
        "clsid": "{SU30_KAB_1500LG_LOADOUT}",
        "name": "KAB-1500LG PR - 1500kg",
        "weight": 1525,
    }

    LITENING___Targeting_Pod = {
        "clsid": "{LITENING_POD}",
        "name": "LITENING - Targeting Pod",
        "weight": 1.4789,
    }

    MBD3_U6_68_with_6_x_FAB_250___250kg = {
        "clsid": "{Su30_MBD3-U6-68-250}",
        "name": "MBD3-U6-68 with 6 x FAB-250 - 250kg",
        "weight": 1560,
    }

    MBD3_U6_68_with_6_x_FAB_100___100kg = {
        "clsid": "{Su30_MBD3-U6-68-100}",
        "name": "MBD3-U6-68 with 6 x FAB-100 - 100kg",
        "weight": 660,
    }

    R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = {
        "clsid": "{SU30_R27R}",
        "name": "R-27R1 (AA-10 Alamo A) - Semi-Act Rdr",
        "weight": 253,
    }

    R_27T1__AA_10_Alamo_B____Infra_Red = {
        "clsid": "{SU30_R27T}",
        "name": "R-27T1 (AA-10 Alamo B) - Infra Red",
        "weight": 245,
    }

    R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = {
        "clsid": "{SU30_R27ER}",
        "name": "R-27ER1 (AA-10 Alamo C) - Semi-Act Extended Range",
        "weight": 350,
    }

    R_27ET1__AA_10_Alamo_D____IR_Extended_Range = {
        "clsid": "{SU30_R27ET}",
        "name": "R-27ET1 (AA-10 Alamo D) - IR Extended Range",
        "weight": 343,
    }

    R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range = {
        "clsid": "{SU30_R27EA}",
        "name": "R-27EA (AA-10 Alamo) - Active Rdr Extended Range",
        "weight": 350,
    }

    R_27EP1__AA_10_Alamo_F____Passive_Rdr_Extended_Range = {
        "clsid": "{SU30_R27EP}",
        "name": "R-27EP1 (AA-10 Alamo F) - Passive Rdr Extended Range",
        "weight": 350,
    }

    R_27P1__AA_10_Alamo_E____Passive_Rdr = {
        "clsid": "{SU30_R27P}",
        "name": "R-27P1 (AA-10 Alamo E) - Passive Rdr",
        "weight": 253,
    }

    R_73L__AA_11_Archer_L____Infra_Red = {
        "clsid": "{Su30-R-73L-AA}",
        "name": "R-73L (AA-11 Archer L) - Infra Red",
        "weight": 106,
    }

    R_73M__AA_11_Archer_M____Infra_Red = {
        "clsid": "{Su30-R-73M-AA}",
        "name": "R-73M (AA-11 Archer M) - Infra Red",
        "weight": 110,
    }

    R_77__AA_12_Adder_Early____Active_Rdr = {
        "clsid": "{SU30_R77}",
        "name": "R-77 (AA-12 Adder Early) - Active Rdr",
        "weight": 175,
    }

    R_77_1__AA_12_Adder_B____Active_Rdr = {
        "clsid": "{SU30_R771}",
        "name": "R-77-1 (AA-12 Adder B) - Active Rdr",
        "weight": 190,
    }

    R_77M__AA_12_Adder_C____Active_Rdr = {
        "clsid": "{SU30_R77M}",
        "name": "R-77M (AA-12 Adder C) - Active Rdr",
        "weight": 190,
    }

    RVV_AE__AA_12_Adder____Active_Rdr = {
        "clsid": "{SU30_RVVAE}",
        "name": "RVV-AE (AA-12 Adder) - Active Rdr",
        "weight": 175,
    }

    RVV_SD__AA_12_Adder_B____Active_Rdr = {
        "clsid": "{SU30_RVVSD}",
        "name": "RVV-SD (AA-12 Adder B) - Active Rdr",
        "weight": 190,
    }

    RVV_MD2__AA_11_Archer_M2____Infra_Red = {
        "clsid": "{Su30-RVV-MD2-AA}",
        "name": "RVV-MD2 (AA-11 Archer M2) - Infra Red",
        "weight": 117,
    }

    Rudra_M1 = {"clsid": "{SU30_RudraM1}", "name": "Rudra-M1", "weight": 690}

    RN_244___260kg__nuclear_bomb = {
        "clsid": "{SU30_244N}",
        "name": "RN-244 - 260kg, nuclear bomb",
        "weight": 260,
    }

    SAP_518_ECM_Pod__Left_ = {
        "clsid": "{SU30_SAP_518_L}",
        "name": "SAP-518 ECM Pod (Left)",
        "weight": 150,
    }

    SAP_518_ECM_Pod__Right_ = {
        "clsid": "{SU30_SAP_518_R}",
        "name": "SAP-518 ECM Pod (Right)",
        "weight": 150,
    }

    SAAW_POD = {"clsid": "{SU30_SAAW}", "name": "SAAW POD", "weight": 570}


inject_weapons(WeaponsSu30)


@planemod
class Su_30MKI(PlaneType):
    id = "Su-30MKI"
    flyable = True
    height = 5.932
    width = 14.7
    length = 21.935
    fuel_max = 9400
    max_speed = 2499.984
    chaff = 96
    flare = 96
    charge_total = 192
    chaff_charge_size = 1
    flare_charge_size = 1
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 124

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

    property_defaults: Dict[str, Any] = {
        "SoloFlight": False,
        "NetCrewControlPriority": 1,
        "MOUNTSURA": False,
    }

    class Properties:
        class SoloFlight:
            id = "SoloFlight"

        class NetCrewControlPriority:
            id = "NetCrewControlPriority"

            class Values:
                Pilot = 0
                Co_Pilot = 1
                Ask_Always = -1
                Equally_Responsible = -2

        class MOUNTSURA:
            id = "MOUNTSURA"

    livery_name = "SU-30MKI"  # from type

    class Pylon1:
        R_73__AA_11_Archer____Infra_Red = (1, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            1,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            1,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            1,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        L005_Sorbtsiya_ECM_pod__left_ = (1, Weapons.L005_Sorbtsiya_ECM_pod__left_)
        SAP_518_ECM_Pod__Left_ = (1, WeaponsSu30.SAP_518_ECM_Pod__Left_)
        Smoke_Generator___red = (1, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (1, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (1, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (1, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (1, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (1, Weapons.Smoke_Generator___orange)

    class Pylon2:
        R_73__AA_11_Archer____Infra_Red = (2, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            2,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            2,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            2,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        ASTRA_Mk_1___Active_Rdr_AAM = (2, WeaponsSu30.ASTRA_Mk_1___Active_Rdr_AAM)
        I_Derby_ER___Active_Rdr_AAM = (2, WeaponsSu30.I_Derby_ER___Active_Rdr_AAM)
        RVV_AE__AA_12_Adder____Active_Rdr = (
            2,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            2,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Smoke_Generator___red = (2, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (2, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (2, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (2, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (2, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (2, Weapons.Smoke_Generator___orange)

    class Pylon3:
        R_73__AA_11_Archer____Infra_Red = (3, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            3,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            3,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            3,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            3,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27T1__AA_10_Alamo_B____Infra_Red = (
            3,
            WeaponsSu30.R_27T1__AA_10_Alamo_B____Infra_Red,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            3,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_27ET1__AA_10_Alamo_D____IR_Extended_Range = (
            3,
            WeaponsSu30.R_27ET1__AA_10_Alamo_D____IR_Extended_Range,
        )
        ASTRA_Mk_1___Active_Rdr_AAM = (3, WeaponsSu30.ASTRA_Mk_1___Active_Rdr_AAM)
        I_Derby_ER___Active_Rdr_AAM = (3, WeaponsSu30.I_Derby_ER___Active_Rdr_AAM)
        RVV_AE__AA_12_Adder____Active_Rdr = (
            3,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            3,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            3,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_ = (
            3,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            3,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_59M = (3, WeaponsSu30.Kh_59M)
        Kh_59MK = (3, WeaponsSu30.Kh_59MK)
        Kh_31A = (3, WeaponsSu30.Kh_31A)
        Kh_31P_AA = (3, WeaponsSu30.Kh_31P_AA)
        KH_35A = (3, WeaponsSu30.KH_35A)
        Rudra_M1 = (3, WeaponsSu30.Rudra_M1)
        SAAW_POD = (3, WeaponsSu30.SAAW_POD)
        KAB_500Kr___500kg_TV_Guided_Bomb = (3, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg = (3, WeaponsSu30.KAB_500S___500kg)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            3,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            3,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            3,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            3,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (3, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            3,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            3,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            3,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            3,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        FAB_500_M54___474kg = (3, WeaponsSu30.FAB_500_M54___474kg)
        FAB_500_M62___474kg = (3, WeaponsSu30.FAB_500_M62___474kg)
        FAB_250_M62___227kg = (3, WeaponsSu30.FAB_250_M62___227kg)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            3,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            3,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )
        _2_x_B_13L_pods___10_x_S_13_OF__122mm_UnGd_Rkts__Blast_Frag = (
            3,
            Weapons._2_x_B_13L_pods___10_x_S_13_OF__122mm_UnGd_Rkts__Blast_Frag,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            3,
            Weapons._2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange = (
            3,
            Weapons._2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8OFP2_MPP = (
            3,
            Weapons._2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8OFP2_MPP,
        )
        _2_x_S_25 = (3, Weapons._2_x_S_25)

    class Pylon4:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            4,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            4,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        I_Derby_ER___Active_Rdr_AAM = (4, WeaponsSu30.I_Derby_ER___Active_Rdr_AAM)
        RVV_AE__AA_12_Adder____Active_Rdr = (
            4,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            4,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            4,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_ = (
            4,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            4,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_59M = (4, WeaponsSu30.Kh_59M)
        Kh_59MK = (4, WeaponsSu30.Kh_59MK)
        Kh_31A = (4, WeaponsSu30.Kh_31A)
        Kh_31P_AA = (4, WeaponsSu30.Kh_31P_AA)
        KH_35A = (4, WeaponsSu30.KH_35A)
        Rudra_M1 = (4, WeaponsSu30.Rudra_M1)
        SAAW_POD = (4, WeaponsSu30.SAAW_POD)
        KAB_500Kr___500kg_TV_Guided_Bomb = (4, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg = (4, WeaponsSu30.KAB_500S___500kg)
        KAB_1500Kr___1500kg = (4, WeaponsSu30.KAB_1500Kr___1500kg)
        KAB_1500LG_PR___1500kg = (4, WeaponsSu30.KAB_1500LG_PR___1500kg)
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            4,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            4,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            4,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            4,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            4,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (4, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            4,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            4,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            4,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            4,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        FAB_500_M54___474kg = (4, WeaponsSu30.FAB_500_M54___474kg)
        FAB_500_M62___474kg = (4, WeaponsSu30.FAB_500_M62___474kg)
        FAB_250_M62___227kg = (4, WeaponsSu30.FAB_250_M62___227kg)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            4,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            4,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )

    class Pylon5:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            5,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            5,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        I_Derby_ER___Active_Rdr_AAM = (5, WeaponsSu30.I_Derby_ER___Active_Rdr_AAM)
        RVV_AE__AA_12_Adder____Active_Rdr = (
            5,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            5,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_ = (
            5,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            5,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            5,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        Kh_31A = (5, WeaponsSu30.Kh_31A)
        Kh_31P_AA = (5, WeaponsSu30.Kh_31P_AA)
        Rudra_M1 = (5, WeaponsSu30.Rudra_M1)
        KAB_500Kr___500kg_TV_Guided_Bomb = (5, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg = (5, WeaponsSu30.KAB_500S___500kg)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            5,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            5,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        P_50T___50kg_Practice_Bomb_LD = (5, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            5,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            5,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            5,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            5,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        FAB_500_M54___474kg = (5, WeaponsSu30.FAB_500_M54___474kg)
        FAB_500_M62___474kg = (5, WeaponsSu30.FAB_500_M62___474kg)
        FAB_250_M62___227kg = (5, WeaponsSu30.FAB_250_M62___227kg)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            5,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            5,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )
        APK_9_POD = (5, WeaponsSu30.APK_9_POD)

    class Pylon6:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            6,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            6,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            6,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            6,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        I_Derby_ER___Active_Rdr_AAM = (6, WeaponsSu30.I_Derby_ER___Active_Rdr_AAM)
        BRAHMOS_A_Ship = (6, WeaponsSu30.BRAHMOS_A_Ship)
        KAB_500Kr___500kg_TV_Guided_Bomb = (6, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg = (6, WeaponsSu30.KAB_500S___500kg)
        KAB_1500Kr___1500kg = (6, WeaponsSu30.KAB_1500Kr___1500kg)
        KAB_1500LG_PR___1500kg = (6, WeaponsSu30.KAB_1500LG_PR___1500kg)
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            6,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            6,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            6,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            6,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            6,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (6, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            6,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            6,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            6,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            6,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        FAB_500_M54___474kg = (6, WeaponsSu30.FAB_500_M54___474kg)
        FAB_500_M62___474kg = (6, WeaponsSu30.FAB_500_M62___474kg)
        FAB_250_M62___227kg = (6, WeaponsSu30.FAB_250_M62___227kg)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            6,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            6,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )
        RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag = (
            6,
            Weapons.RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag,
        )
        RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP = (
            6,
            Weapons.RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP,
        )
        EL_M_2060 = (6, WeaponsSu30.EL_M_2060)

    class Pylon7:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            7,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            7,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            7,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            7,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        I_Derby_ER___Active_Rdr_AAM = (7, WeaponsSu30.I_Derby_ER___Active_Rdr_AAM)
        KAB_500Kr___500kg_TV_Guided_Bomb = (7, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg = (7, WeaponsSu30.KAB_500S___500kg)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            7,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            7,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            7,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            7,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (7, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            7,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            7,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            7,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            7,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        FAB_500_M54___474kg = (7, WeaponsSu30.FAB_500_M54___474kg)
        FAB_500_M62___474kg = (7, WeaponsSu30.FAB_500_M62___474kg)
        FAB_250_M62___227kg = (7, WeaponsSu30.FAB_250_M62___227kg)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            7,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            7,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )
        Smoke_Generator___red = (7, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (7, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (7, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (7, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (7, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (7, Weapons.Smoke_Generator___orange)
        RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag = (
            7,
            Weapons.RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag,
        )
        RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP = (
            7,
            Weapons.RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP,
        )

    class Pylon8:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            8,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            8,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            8,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            8,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        I_Derby_ER___Active_Rdr_AAM = (8, WeaponsSu30.I_Derby_ER___Active_Rdr_AAM)
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            8,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_ = (
            8,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            8,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_31A = (8, WeaponsSu30.Kh_31A)
        Kh_31P_AA = (8, WeaponsSu30.Kh_31P_AA)
        Rudra_M1 = (8, WeaponsSu30.Rudra_M1)
        KAB_500Kr___500kg_TV_Guided_Bomb = (8, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg = (8, WeaponsSu30.KAB_500S___500kg)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            8,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            8,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        P_50T___50kg_Practice_Bomb_LD = (8, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            8,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            8,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            8,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            8,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        FAB_500_M54___474kg = (8, WeaponsSu30.FAB_500_M54___474kg)
        FAB_500_M62___474kg = (8, WeaponsSu30.FAB_500_M62___474kg)
        FAB_250_M62___227kg = (8, WeaponsSu30.FAB_250_M62___227kg)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            8,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            8,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )
        DAMOCLES___Targeting_Pod = (8, WeaponsSu30.DAMOCLES___Targeting_Pod)
        LITENING___Targeting_Pod = (8, WeaponsSu30.LITENING___Targeting_Pod)

    class Pylon9:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            9,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            9,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            9,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            9,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        I_Derby_ER___Active_Rdr_AAM = (9, WeaponsSu30.I_Derby_ER___Active_Rdr_AAM)
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            9,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_ = (
            9,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            9,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_59M = (9, WeaponsSu30.Kh_59M)
        Kh_59MK = (9, WeaponsSu30.Kh_59MK)
        Kh_31A = (9, WeaponsSu30.Kh_31A)
        Kh_31P_AA = (9, WeaponsSu30.Kh_31P_AA)
        KH_35A = (9, WeaponsSu30.KH_35A)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            9,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            9,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        Rudra_M1 = (9, WeaponsSu30.Rudra_M1)
        SAAW_POD = (9, WeaponsSu30.SAAW_POD)
        KAB_500Kr___500kg_TV_Guided_Bomb = (9, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg = (9, WeaponsSu30.KAB_500S___500kg)
        KAB_1500Kr___1500kg = (9, WeaponsSu30.KAB_1500Kr___1500kg)
        KAB_1500LG_PR___1500kg = (9, WeaponsSu30.KAB_1500LG_PR___1500kg)
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            9,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            9,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            9,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (9, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            9,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            9,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            9,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            9,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        FAB_500_M54___474kg = (9, WeaponsSu30.FAB_500_M54___474kg)
        FAB_500_M62___474kg = (9, WeaponsSu30.FAB_500_M62___474kg)
        FAB_250_M62___227kg = (9, WeaponsSu30.FAB_250_M62___227kg)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            9,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            9,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )

    class Pylon10:
        R_73__AA_11_Archer____Infra_Red = (10, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            10,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            10,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            10,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            10,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27T1__AA_10_Alamo_B____Infra_Red = (
            10,
            WeaponsSu30.R_27T1__AA_10_Alamo_B____Infra_Red,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            10,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_27ET1__AA_10_Alamo_D____IR_Extended_Range = (
            10,
            WeaponsSu30.R_27ET1__AA_10_Alamo_D____IR_Extended_Range,
        )
        ASTRA_Mk_1___Active_Rdr_AAM = (10, WeaponsSu30.ASTRA_Mk_1___Active_Rdr_AAM)
        I_Derby_ER___Active_Rdr_AAM = (10, WeaponsSu30.I_Derby_ER___Active_Rdr_AAM)
        RVV_AE__AA_12_Adder____Active_Rdr = (
            10,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            10,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            10,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_ = (
            10,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            10,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_59M = (10, WeaponsSu30.Kh_59M)
        Kh_59MK = (10, WeaponsSu30.Kh_59MK)
        Kh_31A = (10, WeaponsSu30.Kh_31A)
        Kh_31P_AA = (10, WeaponsSu30.Kh_31P_AA)
        KH_35A = (10, WeaponsSu30.KH_35A)
        Rudra_M1 = (10, WeaponsSu30.Rudra_M1)
        SAAW_POD = (10, WeaponsSu30.SAAW_POD)
        KAB_500Kr___500kg_TV_Guided_Bomb = (
            10,
            Weapons.KAB_500Kr___500kg_TV_Guided_Bomb,
        )
        KAB_500S___500kg = (10, WeaponsSu30.KAB_500S___500kg)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            10,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            10,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            10,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            10,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (10, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            10,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            10,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            10,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            10,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        FAB_500_M54___474kg = (10, WeaponsSu30.FAB_500_M54___474kg)
        FAB_500_M62___474kg = (10, WeaponsSu30.FAB_500_M62___474kg)
        FAB_250_M62___227kg = (10, WeaponsSu30.FAB_250_M62___227kg)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            10,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            10,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )
        _2_x_B_13L_pods___10_x_S_13_OF__122mm_UnGd_Rkts__Blast_Frag = (
            10,
            Weapons._2_x_B_13L_pods___10_x_S_13_OF__122mm_UnGd_Rkts__Blast_Frag,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            10,
            Weapons._2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange = (
            10,
            Weapons._2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8OFP2_MPP = (
            10,
            Weapons._2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8OFP2_MPP,
        )
        _2_x_S_25 = (10, Weapons._2_x_S_25)

    class Pylon11:
        R_73__AA_11_Archer____Infra_Red = (11, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            11,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            11,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            11,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        ASTRA_Mk_1___Active_Rdr_AAM = (11, WeaponsSu30.ASTRA_Mk_1___Active_Rdr_AAM)
        I_Derby_ER___Active_Rdr_AAM = (11, WeaponsSu30.I_Derby_ER___Active_Rdr_AAM)
        RVV_AE__AA_12_Adder____Active_Rdr = (
            11,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            11,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Smoke_Generator___red = (11, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (11, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (11, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (11, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (11, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (11, Weapons.Smoke_Generator___orange)

    class Pylon12:
        R_73__AA_11_Archer____Infra_Red = (12, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            12,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            12,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            12,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        L005_Sorbtsiya_ECM_pod__right_ = (12, Weapons.L005_Sorbtsiya_ECM_pod__right_)
        SAP_518_ECM_Pod__Right_ = (12, WeaponsSu30.SAP_518_ECM_Pod__Right_)
        Smoke_Generator___red = (12, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (12, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (12, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (12, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (12, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (12, Weapons.Smoke_Generator___orange)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.AFAC,
        task.SEAD,
        task.AntishipStrike,
        task.CAS,
        task.PinpointStrike,
        task.GroundAttack,
        task.RunwayAttack,
    ]
    task_default = task.CAP


@planemod
class Su_30MKA(PlaneType):
    id = "Su-30MKA"
    flyable = True
    height = 5.932
    width = 14.7
    length = 21.935
    fuel_max = 9500
    max_speed = 2499.984
    chaff = 96
    flare = 96
    charge_total = 192
    chaff_charge_size = 1
    flare_charge_size = 1
    eplrs = True
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 124

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

    property_defaults: Dict[str, Any] = {
        "SoloFlight": False,
        "NetCrewControlPriority": 1,
        "MOUNTSURA": False,
    }

    class Properties:
        class SoloFlight:
            id = "SoloFlight"

        class NetCrewControlPriority:
            id = "NetCrewControlPriority"

            class Values:
                Pilot = 0
                Co_Pilot = 1
                Ask_Always = -1
                Equally_Responsible = -2

        class MOUNTSURA:
            id = "MOUNTSURA"

    livery_name = "SU-30MKA"  # from type

    class Pylon1:
        R_73__AA_11_Archer____Infra_Red = (1, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            1,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            1,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            1,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        L005_Sorbtsiya_ECM_pod__left_ = (1, Weapons.L005_Sorbtsiya_ECM_pod__left_)
        SAP_518_ECM_Pod__Left_ = (1, WeaponsSu30.SAP_518_ECM_Pod__Left_)
        Smoke_Generator___red = (1, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (1, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (1, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (1, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (1, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (1, Weapons.Smoke_Generator___orange)

    class Pylon2:
        R_73__AA_11_Archer____Infra_Red = (2, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            2,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            2,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            2,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            2,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            2,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Smoke_Generator___red = (2, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (2, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (2, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (2, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (2, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (2, Weapons.Smoke_Generator___orange)

    class Pylon3:
        R_73__AA_11_Archer____Infra_Red = (3, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            3,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            3,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            3,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            3,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27T1__AA_10_Alamo_B____Infra_Red = (
            3,
            WeaponsSu30.R_27T1__AA_10_Alamo_B____Infra_Red,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            3,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_27ET1__AA_10_Alamo_D____IR_Extended_Range = (
            3,
            WeaponsSu30.R_27ET1__AA_10_Alamo_D____IR_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            3,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            3,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_ = (
            3,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_,
        )
        Kh_31P_AA = (3, WeaponsSu30.Kh_31P_AA)
        Kh_36_Grom_1 = (3, WeaponsSu30.Kh_36_Grom_1)
        KH_38MTE = (3, WeaponsSu30.KH_38MTE)
        KH_38MLE = (3, WeaponsSu30.KH_38MLE)
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            3,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            3,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_59M = (3, WeaponsSu30.Kh_59M)
        Kh_59MK = (3, WeaponsSu30.Kh_59MK)
        Kh_31A = (3, WeaponsSu30.Kh_31A)
        KH_35A = (3, WeaponsSu30.KH_35A)
        KH_35UE = (3, WeaponsSu30.KH_35UE)
        KH_31AD = (3, WeaponsSu30.KH_31AD)
        KH_31PD__AA_ = (3, WeaponsSu30.KH_31PD__AA_)
        KAB_500Kr___500kg_TV_Guided_Bomb = (3, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg = (3, WeaponsSu30.KAB_500S___500kg)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            3,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            3,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            3,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            3,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (3, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            3,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            3,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            3,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            3,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        FAB_500_M54___474kg = (3, WeaponsSu30.FAB_500_M54___474kg)
        FAB_500_M62___474kg = (3, WeaponsSu30.FAB_500_M62___474kg)
        FAB_250_M62___227kg = (3, WeaponsSu30.FAB_250_M62___227kg)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            3,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            3,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )
        _2_x_B_13L_pods___10_x_S_13_OF__122mm_UnGd_Rkts__Blast_Frag = (
            3,
            Weapons._2_x_B_13L_pods___10_x_S_13_OF__122mm_UnGd_Rkts__Blast_Frag,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            3,
            Weapons._2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange = (
            3,
            Weapons._2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8OFP2_MPP = (
            3,
            Weapons._2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8OFP2_MPP,
        )
        _2_x_S_25 = (3, Weapons._2_x_S_25)

    class Pylon4:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            4,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            4,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            4,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            4,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Kh_31P_AA = (4, WeaponsSu30.Kh_31P_AA)
        Kh_36_Grom_1 = (4, WeaponsSu30.Kh_36_Grom_1)
        KH_38MTE = (4, WeaponsSu30.KH_38MTE)
        KH_38MLE = (4, WeaponsSu30.KH_38MLE)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_ = (
            4,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            4,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            4,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_59M = (4, WeaponsSu30.Kh_59M)
        Kh_59MK = (4, WeaponsSu30.Kh_59MK)
        Kh_31A = (4, WeaponsSu30.Kh_31A)
        KH_35A = (4, WeaponsSu30.KH_35A)
        KH_35UE = (4, WeaponsSu30.KH_35UE)
        KH_31AD = (4, WeaponsSu30.KH_31AD)
        KH_31PD__AA_ = (4, WeaponsSu30.KH_31PD__AA_)
        KAB_500Kr___500kg_TV_Guided_Bomb = (4, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg = (4, WeaponsSu30.KAB_500S___500kg)
        KAB_1500Kr___1500kg = (4, WeaponsSu30.KAB_1500Kr___1500kg)
        KAB_1500LG_PR___1500kg = (4, WeaponsSu30.KAB_1500LG_PR___1500kg)
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            4,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            4,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            4,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            4,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            4,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (4, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            4,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            4,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            4,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            4,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        FAB_500_M54___474kg = (4, WeaponsSu30.FAB_500_M54___474kg)
        FAB_500_M62___474kg = (4, WeaponsSu30.FAB_500_M62___474kg)
        FAB_250_M62___227kg = (4, WeaponsSu30.FAB_250_M62___227kg)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            4,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            4,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )

    class Pylon5:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            5,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            5,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            5,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            5,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Kh_31P_AA = (5, WeaponsSu30.Kh_31P_AA)
        Kh_36_Grom_1 = (5, WeaponsSu30.Kh_36_Grom_1)
        KH_38MTE = (5, WeaponsSu30.KH_38MTE)
        KH_38MLE = (5, WeaponsSu30.KH_38MLE)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_ = (
            5,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            5,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            5,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_31A = (5, WeaponsSu30.Kh_31A)
        KH_31AD = (5, WeaponsSu30.KH_31AD)
        KH_31PD__AA_ = (5, WeaponsSu30.KH_31PD__AA_)
        KAB_500Kr___500kg_TV_Guided_Bomb = (5, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg = (5, WeaponsSu30.KAB_500S___500kg)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            5,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            5,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        P_50T___50kg_Practice_Bomb_LD = (5, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            5,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            5,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            5,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            5,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        FAB_500_M54___474kg = (5, WeaponsSu30.FAB_500_M54___474kg)
        FAB_500_M62___474kg = (5, WeaponsSu30.FAB_500_M62___474kg)
        FAB_250_M62___227kg = (5, WeaponsSu30.FAB_250_M62___227kg)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            5,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            5,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )
        APK_9_POD = (5, WeaponsSu30.APK_9_POD)

    class Pylon6:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            6,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            6,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            6,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            6,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (6, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg = (6, WeaponsSu30.KAB_500S___500kg)
        KAB_1500Kr___1500kg = (6, WeaponsSu30.KAB_1500Kr___1500kg)
        KAB_1500LG_PR___1500kg = (6, WeaponsSu30.KAB_1500LG_PR___1500kg)
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            6,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            6,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            6,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            6,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            6,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        P_50T___50kg_Practice_Bomb_LD = (6, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            6,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            6,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            6,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            6,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        FAB_500_M54___474kg = (6, WeaponsSu30.FAB_500_M54___474kg)
        FAB_500_M62___474kg = (6, WeaponsSu30.FAB_500_M62___474kg)
        FAB_250_M62___227kg = (6, WeaponsSu30.FAB_250_M62___227kg)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            6,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            6,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )
        RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag = (
            6,
            Weapons.RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag,
        )
        RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP = (
            6,
            Weapons.RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP,
        )

    class Pylon7:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            7,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            7,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            7,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            7,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (7, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg = (7, WeaponsSu30.KAB_500S___500kg)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            7,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            7,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            7,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            7,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (7, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            7,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            7,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            7,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            7,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        FAB_500_M54___474kg = (7, WeaponsSu30.FAB_500_M54___474kg)
        FAB_500_M62___474kg = (7, WeaponsSu30.FAB_500_M62___474kg)
        FAB_250_M62___227kg = (7, WeaponsSu30.FAB_250_M62___227kg)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            7,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            7,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )
        Smoke_Generator___red = (7, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (7, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (7, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (7, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (7, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (7, Weapons.Smoke_Generator___orange)
        RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag = (
            7,
            Weapons.RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag,
        )
        RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP = (
            7,
            Weapons.RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP,
        )

    class Pylon8:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            8,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            8,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            8,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            8,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Kh_31P_AA = (8, WeaponsSu30.Kh_31P_AA)
        Kh_36_Grom_1 = (8, WeaponsSu30.Kh_36_Grom_1)
        KH_38MTE = (8, WeaponsSu30.KH_38MTE)
        KH_38MLE = (8, WeaponsSu30.KH_38MLE)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_ = (
            8,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            8,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            8,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_31A = (8, WeaponsSu30.Kh_31A)
        KH_31AD = (8, WeaponsSu30.KH_31AD)
        KH_31PD__AA_ = (8, WeaponsSu30.KH_31PD__AA_)
        KAB_500Kr___500kg_TV_Guided_Bomb = (8, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg = (8, WeaponsSu30.KAB_500S___500kg)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            8,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            8,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        P_50T___50kg_Practice_Bomb_LD = (8, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            8,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            8,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            8,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            8,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        FAB_500_M54___474kg = (8, WeaponsSu30.FAB_500_M54___474kg)
        FAB_500_M62___474kg = (8, WeaponsSu30.FAB_500_M62___474kg)
        FAB_250_M62___227kg = (8, WeaponsSu30.FAB_250_M62___227kg)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            8,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            8,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )

    # ERRR {DAMOCLES}

    class Pylon9:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            9,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            9,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            9,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            9,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Kh_31P_AA = (9, WeaponsSu30.Kh_31P_AA)
        Kh_36_Grom_1 = (9, WeaponsSu30.Kh_36_Grom_1)
        KH_38MTE = (9, WeaponsSu30.KH_38MTE)
        KH_38MLE = (9, WeaponsSu30.KH_38MLE)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_ = (
            9,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            9,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            9,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_59M = (9, WeaponsSu30.Kh_59M)
        Kh_59MK = (9, WeaponsSu30.Kh_59MK)
        Kh_31A = (9, WeaponsSu30.Kh_31A)
        KH_35A = (9, WeaponsSu30.KH_35A)
        KH_35UE = (9, WeaponsSu30.KH_35UE)
        KH_31AD = (9, WeaponsSu30.KH_31AD)
        KH_31PD__AA_ = (9, WeaponsSu30.KH_31PD__AA_)
        KAB_500Kr___500kg_TV_Guided_Bomb = (9, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg = (9, WeaponsSu30.KAB_500S___500kg)
        KAB_1500Kr___1500kg = (9, WeaponsSu30.KAB_1500Kr___1500kg)
        KAB_1500LG_PR___1500kg = (9, WeaponsSu30.KAB_1500LG_PR___1500kg)
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            9,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            9,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            9,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            9,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            9,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (9, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            9,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            9,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            9,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            9,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        FAB_500_M54___474kg = (9, WeaponsSu30.FAB_500_M54___474kg)
        FAB_500_M62___474kg = (9, WeaponsSu30.FAB_500_M62___474kg)
        FAB_250_M62___227kg = (9, WeaponsSu30.FAB_250_M62___227kg)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            9,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            9,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )

    class Pylon10:
        R_73__AA_11_Archer____Infra_Red = (10, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            10,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            10,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            10,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            10,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27T1__AA_10_Alamo_B____Infra_Red = (
            10,
            WeaponsSu30.R_27T1__AA_10_Alamo_B____Infra_Red,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            10,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_27ET1__AA_10_Alamo_D____IR_Extended_Range = (
            10,
            WeaponsSu30.R_27ET1__AA_10_Alamo_D____IR_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            10,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            10,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Kh_31P_AA = (10, WeaponsSu30.Kh_31P_AA)
        Kh_36_Grom_1 = (10, WeaponsSu30.Kh_36_Grom_1)
        KH_38MTE = (10, WeaponsSu30.KH_38MTE)
        KH_38MLE = (10, WeaponsSu30.KH_38MLE)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_ = (
            10,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            10,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            10,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_59M = (10, WeaponsSu30.Kh_59M)
        Kh_59MK = (10, WeaponsSu30.Kh_59MK)
        Kh_31A = (10, WeaponsSu30.Kh_31A)
        KH_35A = (10, WeaponsSu30.KH_35A)
        KH_35UE = (10, WeaponsSu30.KH_35UE)
        KH_31AD = (10, WeaponsSu30.KH_31AD)
        KH_31PD__AA_ = (10, WeaponsSu30.KH_31PD__AA_)
        KAB_500Kr___500kg_TV_Guided_Bomb = (
            10,
            Weapons.KAB_500Kr___500kg_TV_Guided_Bomb,
        )
        KAB_500S___500kg = (10, WeaponsSu30.KAB_500S___500kg)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            10,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            10,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            10,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            10,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (10, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            10,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            10,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            10,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            10,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        FAB_500_M54___474kg = (10, WeaponsSu30.FAB_500_M54___474kg)
        FAB_500_M62___474kg = (10, WeaponsSu30.FAB_500_M62___474kg)
        FAB_250_M62___227kg = (10, WeaponsSu30.FAB_250_M62___227kg)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            10,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            10,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )
        _2_x_B_13L_pods___10_x_S_13_OF__122mm_UnGd_Rkts__Blast_Frag = (
            10,
            Weapons._2_x_B_13L_pods___10_x_S_13_OF__122mm_UnGd_Rkts__Blast_Frag,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            10,
            Weapons._2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange = (
            10,
            Weapons._2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8OFP2_MPP = (
            10,
            Weapons._2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8OFP2_MPP,
        )
        _2_x_S_25 = (10, Weapons._2_x_S_25)

    class Pylon11:
        R_73__AA_11_Archer____Infra_Red = (11, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            11,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            11,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            11,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            11,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            11,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Smoke_Generator___red = (11, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (11, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (11, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (11, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (11, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (11, Weapons.Smoke_Generator___orange)

    class Pylon12:
        R_73__AA_11_Archer____Infra_Red = (12, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            12,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            12,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            12,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        L005_Sorbtsiya_ECM_pod__right_ = (12, Weapons.L005_Sorbtsiya_ECM_pod__right_)
        SAP_518_ECM_Pod__Right_ = (12, WeaponsSu30.SAP_518_ECM_Pod__Right_)
        Smoke_Generator___red = (12, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (12, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (12, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (12, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (12, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (12, Weapons.Smoke_Generator___orange)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.AFAC,
        task.SEAD,
        task.AntishipStrike,
        task.CAS,
        task.PinpointStrike,
        task.GroundAttack,
        task.RunwayAttack,
    ]
    task_default = task.CAP


@planemod
class Su_30MKM(PlaneType):
    id = "Su-30MKM"
    flyable = True
    height = 5.932
    width = 14.7
    length = 21.935
    fuel_max = 9400
    max_speed = 2499.984
    chaff = 96
    flare = 96
    charge_total = 192
    chaff_charge_size = 1
    flare_charge_size = 1
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 124

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

    property_defaults: Dict[str, Any] = {
        "SoloFlight": False,
        "NetCrewControlPriority": 1,
    }

    class Properties:
        class SoloFlight:
            id = "SoloFlight"

        class NetCrewControlPriority:
            id = "NetCrewControlPriority"

            class Values:
                Pilot = 0
                Co_Pilot = 1
                Ask_Always = -1
                Equally_Responsible = -2

    livery_name = "SU-30MKM"  # from type

    class Pylon1:
        R_73__AA_11_Archer____Infra_Red = (1, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            1,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            1,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            1,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        L005_Sorbtsiya_ECM_pod__left_ = (1, Weapons.L005_Sorbtsiya_ECM_pod__left_)
        SAP_518_ECM_Pod__Left_ = (1, WeaponsSu30.SAP_518_ECM_Pod__Left_)
        Smoke_Generator___red = (1, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (1, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (1, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (1, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (1, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (1, Weapons.Smoke_Generator___orange)

    class Pylon2:
        R_73__AA_11_Archer____Infra_Red = (2, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            2,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            2,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            2,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            2,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            2,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Smoke_Generator___red = (2, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (2, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (2, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (2, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (2, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (2, Weapons.Smoke_Generator___orange)

    class Pylon3:
        R_73__AA_11_Archer____Infra_Red = (3, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            3,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            3,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            3,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            3,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27T1__AA_10_Alamo_B____Infra_Red = (
            3,
            WeaponsSu30.R_27T1__AA_10_Alamo_B____Infra_Red,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            3,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_27ET1__AA_10_Alamo_D____IR_Extended_Range = (
            3,
            WeaponsSu30.R_27ET1__AA_10_Alamo_D____IR_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            3,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            3,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Kh_31P_AA = (3, WeaponsSu30.Kh_31P_AA)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_ = (
            3,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            3,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            3,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_59M = (3, WeaponsSu30.Kh_59M)
        Kh_59MK = (3, WeaponsSu30.Kh_59MK)
        Kh_31A = (3, WeaponsSu30.Kh_31A)
        KH_35A = (3, WeaponsSu30.KH_35A)
        KAB_500Kr___500kg_TV_Guided_Bomb = (3, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg = (3, WeaponsSu30.KAB_500S___500kg)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            3,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            3,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            3,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            3,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (3, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            3,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            3,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        FAB_250___250kg_GP_Bomb_LD = (3, Weapons.FAB_250___250kg_GP_Bomb_LD)
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            3,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M_62___500kg_GP_Bomb_LD = (3, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            3,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            3,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD = (
            3,
            Weapons.MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD,
        )
        _2_x_B_13L_pods___10_x_S_13_OF__122mm_UnGd_Rkts__Blast_Frag = (
            3,
            Weapons._2_x_B_13L_pods___10_x_S_13_OF__122mm_UnGd_Rkts__Blast_Frag,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            3,
            Weapons._2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange = (
            3,
            Weapons._2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8OFP2_MPP = (
            3,
            Weapons._2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8OFP2_MPP,
        )
        _2_x_S_25 = (3, Weapons._2_x_S_25)
        Mk_82___500lb_GP_Bomb_LD = (3, Weapons.Mk_82___500lb_GP_Bomb_LD)
        GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            WeaponsSu30.GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (3, Weapons.GBU_12___500lb_Laser_Guided_Bomb)

    class Pylon4:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            4,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            4,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            4,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            4,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Kh_31P_AA = (4, WeaponsSu30.Kh_31P_AA)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_ = (
            4,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            4,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            4,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_59M = (4, WeaponsSu30.Kh_59M)
        Kh_59MK = (4, WeaponsSu30.Kh_59MK)
        Kh_31A = (4, WeaponsSu30.Kh_31A)
        KH_35A = (4, WeaponsSu30.KH_35A)
        KAB_500Kr___500kg_TV_Guided_Bomb = (4, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg = (4, WeaponsSu30.KAB_500S___500kg)
        KAB_1500Kr___1500kg = (4, WeaponsSu30.KAB_1500Kr___1500kg)
        KAB_1500LG_PR___1500kg = (4, WeaponsSu30.KAB_1500LG_PR___1500kg)
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            4,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            4,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            4,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            4,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            4,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (4, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            4,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            4,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        FAB_250___250kg_GP_Bomb_LD = (4, Weapons.FAB_250___250kg_GP_Bomb_LD)
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            4,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M_62___500kg_GP_Bomb_LD = (4, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            4,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            4,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD = (
            4,
            Weapons.MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD,
        )
        Mk_82___500lb_GP_Bomb_LD = (4, Weapons.Mk_82___500lb_GP_Bomb_LD)
        GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            4,
            WeaponsSu30.GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (4, Weapons.GBU_12___500lb_Laser_Guided_Bomb)

    class Pylon5:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            5,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            5,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            5,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            5,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Kh_31P_AA = (5, WeaponsSu30.Kh_31P_AA)
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            5,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_ = (
            5,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            5,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_31A = (5, WeaponsSu30.Kh_31A)
        KAB_500Kr___500kg_TV_Guided_Bomb = (5, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg = (5, WeaponsSu30.KAB_500S___500kg)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            5,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            5,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        P_50T___50kg_Practice_Bomb_LD = (5, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            5,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            5,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        FAB_250___250kg_GP_Bomb_LD = (5, Weapons.FAB_250___250kg_GP_Bomb_LD)
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            5,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M_62___500kg_GP_Bomb_LD = (5, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            5,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            5,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        APK_9_POD = (5, WeaponsSu30.APK_9_POD)

        Mk_82___500lb_GP_Bomb_LD = (5, Weapons.Mk_82___500lb_GP_Bomb_LD)
        GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            5,
            WeaponsSu30.GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (5, Weapons.GBU_12___500lb_Laser_Guided_Bomb)

    class Pylon6:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            6,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            6,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            6,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            6,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (6, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg = (6, WeaponsSu30.KAB_500S___500kg)
        KAB_1500Kr___1500kg = (6, WeaponsSu30.KAB_1500Kr___1500kg)
        KAB_1500LG_PR___1500kg = (6, WeaponsSu30.KAB_1500LG_PR___1500kg)
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            6,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            6,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            6,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            6,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            6,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (6, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            6,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            6,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        FAB_250___250kg_GP_Bomb_LD = (6, Weapons.FAB_250___250kg_GP_Bomb_LD)
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            6,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M_62___500kg_GP_Bomb_LD = (6, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            6,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            6,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag = (
            6,
            Weapons.RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag,
        )
        RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP = (
            6,
            Weapons.RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP,
        )

        Mk_82___500lb_GP_Bomb_LD = (6, Weapons.Mk_82___500lb_GP_Bomb_LD)
        GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            6,
            WeaponsSu30.GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (6, Weapons.GBU_12___500lb_Laser_Guided_Bomb)

    class Pylon7:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            7,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            7,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            7,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            7,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (7, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg = (7, WeaponsSu30.KAB_500S___500kg)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            7,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            7,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            7,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            7,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (7, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            7,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            7,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        FAB_250___250kg_GP_Bomb_LD = (7, Weapons.FAB_250___250kg_GP_Bomb_LD)
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            7,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M_62___500kg_GP_Bomb_LD = (7, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            7,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            7,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag = (
            7,
            Weapons.RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag,
        )
        RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP = (
            7,
            Weapons.RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP,
        )
        Smoke_Generator___red = (7, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (7, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (7, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (7, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (7, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (7, Weapons.Smoke_Generator___orange)
        Mk_82___500lb_GP_Bomb_LD = (7, Weapons.Mk_82___500lb_GP_Bomb_LD)
        GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsSu30.GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (7, Weapons.GBU_12___500lb_Laser_Guided_Bomb)

    class Pylon8:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            8,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            8,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            8,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            8,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Kh_31P_AA = (8, WeaponsSu30.Kh_31P_AA)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_ = (
            8,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            8,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            8,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_31A = (8, WeaponsSu30.Kh_31A)
        KAB_500Kr___500kg_TV_Guided_Bomb = (8, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg = (8, WeaponsSu30.KAB_500S___500kg)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            8,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            8,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        P_50T___50kg_Practice_Bomb_LD = (8, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            8,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            8,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        FAB_250___250kg_GP_Bomb_LD = (8, Weapons.FAB_250___250kg_GP_Bomb_LD)
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            8,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M_62___500kg_GP_Bomb_LD = (8, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            8,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            8,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        # ERRR {DAMOCLES}

        Mk_82___500lb_GP_Bomb_LD = (8, Weapons.Mk_82___500lb_GP_Bomb_LD)
        GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            8,
            WeaponsSu30.GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (8, Weapons.GBU_12___500lb_Laser_Guided_Bomb)

    class Pylon9:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            9,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            9,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            9,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            9,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Kh_31P_AA = (9, WeaponsSu30.Kh_31P_AA)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_ = (
            9,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            9,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            9,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_59M = (9, WeaponsSu30.Kh_59M)
        Kh_59MK = (9, WeaponsSu30.Kh_59MK)
        Kh_31A = (9, WeaponsSu30.Kh_31A)
        KH_35A = (9, WeaponsSu30.KH_35A)
        KAB_500Kr___500kg_TV_Guided_Bomb = (9, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg = (9, WeaponsSu30.KAB_500S___500kg)
        KAB_1500Kr___1500kg = (9, WeaponsSu30.KAB_1500Kr___1500kg)
        KAB_1500LG_PR___1500kg = (9, WeaponsSu30.KAB_1500LG_PR___1500kg)
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            9,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            9,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            9,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            9,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            9,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (9, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            9,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            9,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        FAB_250___250kg_GP_Bomb_LD = (9, Weapons.FAB_250___250kg_GP_Bomb_LD)
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            9,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M_62___500kg_GP_Bomb_LD = (9, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            9,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            9,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD = (
            9,
            Weapons.MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD,
        )

        Mk_82___500lb_GP_Bomb_LD = (9, Weapons.Mk_82___500lb_GP_Bomb_LD)
        GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            9,
            WeaponsSu30.GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (9, Weapons.GBU_12___500lb_Laser_Guided_Bomb)

    class Pylon10:
        R_73__AA_11_Archer____Infra_Red = (10, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            10,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            10,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            10,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            10,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27T1__AA_10_Alamo_B____Infra_Red = (
            10,
            WeaponsSu30.R_27T1__AA_10_Alamo_B____Infra_Red,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            10,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_27ET1__AA_10_Alamo_D____IR_Extended_Range = (
            10,
            WeaponsSu30.R_27ET1__AA_10_Alamo_D____IR_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            10,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            10,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Kh_31P_AA = (10, WeaponsSu30.Kh_31P_AA)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_ = (
            10,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            10,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            10,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_59M = (10, WeaponsSu30.Kh_59M)
        Kh_59MK = (10, WeaponsSu30.Kh_59MK)
        Kh_31A = (10, WeaponsSu30.Kh_31A)
        KH_35A = (10, WeaponsSu30.KH_35A)
        KAB_500Kr___500kg_TV_Guided_Bomb = (
            10,
            Weapons.KAB_500Kr___500kg_TV_Guided_Bomb,
        )
        KAB_500S___500kg = (10, WeaponsSu30.KAB_500S___500kg)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            10,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            10,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            10,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            10,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (10, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            10,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            10,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        FAB_250___250kg_GP_Bomb_LD = (10, Weapons.FAB_250___250kg_GP_Bomb_LD)
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            10,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M_62___500kg_GP_Bomb_LD = (10, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            10,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            10,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD = (
            10,
            Weapons.MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD,
        )
        _2_x_B_13L_pods___10_x_S_13_OF__122mm_UnGd_Rkts__Blast_Frag = (
            10,
            Weapons._2_x_B_13L_pods___10_x_S_13_OF__122mm_UnGd_Rkts__Blast_Frag,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            10,
            Weapons._2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange = (
            10,
            Weapons._2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8OFP2_MPP = (
            10,
            Weapons._2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8OFP2_MPP,
        )
        _2_x_S_25 = (10, Weapons._2_x_S_25)

        Mk_82___500lb_GP_Bomb_LD = (10, Weapons.Mk_82___500lb_GP_Bomb_LD)
        GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            10,
            WeaponsSu30.GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (
            10,
            Weapons.GBU_12___500lb_Laser_Guided_Bomb,
        )

    class Pylon11:
        R_73__AA_11_Archer____Infra_Red = (11, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            11,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            11,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            11,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            11,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            11,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Smoke_Generator___red = (11, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (11, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (11, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (11, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (11, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (11, Weapons.Smoke_Generator___orange)

    class Pylon12:
        R_73__AA_11_Archer____Infra_Red = (12, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            12,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            12,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            12,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        L005_Sorbtsiya_ECM_pod__right_ = (12, Weapons.L005_Sorbtsiya_ECM_pod__right_)
        SAP_518_ECM_Pod__Right_ = (12, WeaponsSu30.SAP_518_ECM_Pod__Right_)
        Smoke_Generator___red = (12, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (12, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (12, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (12, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (12, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (12, Weapons.Smoke_Generator___orange)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.AFAC,
        task.SEAD,
        task.AntishipStrike,
        task.CAS,
        task.PinpointStrike,
        task.GroundAttack,
        task.RunwayAttack,
    ]
    task_default = task.CAP


@planemod
class Su_30SM(PlaneType):
    id = "Su-30SM"
    flyable = True
    height = 5.932
    width = 14.7
    length = 21.935
    fuel_max = 9500
    max_speed = 2499.984
    chaff = 96
    flare = 96
    charge_total = 192
    chaff_charge_size = 1
    flare_charge_size = 1
    eplrs = True
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 124

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

    property_defaults: Dict[str, Any] = {
        "SoloFlight": False,
        "NetCrewControlPriority": 1,
        "MOUNTSURA": False,
    }

    class Properties:
        class SoloFlight:
            id = "SoloFlight"

        class NetCrewControlPriority:
            id = "NetCrewControlPriority"

            class Values:
                Pilot = 0
                Flight_officer = 1
                Ask_Always = -1
                Equally_Responsible = -2

        class MOUNTSURA:
            id = "MOUNTSURA"

    livery_name = "SU-30SM"  # from type

    class Pylon1:
        R_73__AA_11_Archer____Infra_Red = (1, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            1,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            1,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            1,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        L005_Sorbtsiya_ECM_pod__left_ = (1, Weapons.L005_Sorbtsiya_ECM_pod__left_)
        SAP_518_ECM_Pod__Left_ = (1, WeaponsSu30.SAP_518_ECM_Pod__Left_)
        Smoke_Generator___red = (1, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (1, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (1, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (1, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (1, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (1, Weapons.Smoke_Generator___orange)

    class Pylon2:
        R_73__AA_11_Archer____Infra_Red = (2, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            2,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            2,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            2,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        R_77__AA_12_Adder_Early____Active_Rdr = (
            2,
            WeaponsSu30.R_77__AA_12_Adder_Early____Active_Rdr,
        )
        R_77_1__AA_12_Adder_B____Active_Rdr = (
            2,
            WeaponsSu30.R_77_1__AA_12_Adder_B____Active_Rdr,
        )
        R_77M__AA_12_Adder_C____Active_Rdr = (
            2,
            WeaponsSu30.R_77M__AA_12_Adder_C____Active_Rdr,
        )
        Smoke_Generator___red = (2, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (2, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (2, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (2, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (2, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (2, Weapons.Smoke_Generator___orange)

    class Pylon3:
        R_73__AA_11_Archer____Infra_Red = (3, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            3,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            3,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            3,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            3,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27T1__AA_10_Alamo_B____Infra_Red = (
            3,
            WeaponsSu30.R_27T1__AA_10_Alamo_B____Infra_Red,
        )
        R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range = (
            3,
            WeaponsSu30.R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            3,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_27ET1__AA_10_Alamo_D____IR_Extended_Range = (
            3,
            WeaponsSu30.R_27ET1__AA_10_Alamo_D____IR_Extended_Range,
        )
        R_27EP1__AA_10_Alamo_F____Passive_Rdr_Extended_Range = (
            3,
            WeaponsSu30.R_27EP1__AA_10_Alamo_F____Passive_Rdr_Extended_Range,
        )
        R_27P1__AA_10_Alamo_E____Passive_Rdr = (
            3,
            WeaponsSu30.R_27P1__AA_10_Alamo_E____Passive_Rdr,
        )
        R_77__AA_12_Adder_Early____Active_Rdr = (
            3,
            WeaponsSu30.R_77__AA_12_Adder_Early____Active_Rdr,
        )
        R_77_1__AA_12_Adder_B____Active_Rdr = (
            3,
            WeaponsSu30.R_77_1__AA_12_Adder_B____Active_Rdr,
        )
        R_77M__AA_12_Adder_C____Active_Rdr = (
            3,
            WeaponsSu30.R_77M__AA_12_Adder_C____Active_Rdr,
        )
        Kh_31P_AA = (3, WeaponsSu30.Kh_31P_AA)
        Kh_36_Grom_1 = (3, WeaponsSu30.Kh_36_Grom_1)
        KH_38MTE = (3, WeaponsSu30.KH_38MTE)
        KH_38MLE = (3, WeaponsSu30.KH_38MLE)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_ = (
            3,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            3,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            3,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_59M = (3, WeaponsSu30.Kh_59M)
        Kh_59MK = (3, WeaponsSu30.Kh_59MK)
        Kh_31A = (3, WeaponsSu30.Kh_31A)
        KH_35A = (3, WeaponsSu30.KH_35A)
        KH_35UE = (3, WeaponsSu30.KH_35UE)
        KH_31AD = (3, WeaponsSu30.KH_31AD)
        KH_31PD__AA_ = (3, WeaponsSu30.KH_31PD__AA_)
        Kh_59MK2_ = (3, WeaponsSu30.Kh_59MK2_)
        KAB_500Kr___500kg_TV_Guided_Bomb = (3, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg = (3, WeaponsSu30.KAB_500S___500kg)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            3,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            3,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            3,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            3,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (3, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            3,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            3,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            3,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M54___474kg = (3, WeaponsSu30.FAB_500_M54___474kg)
        FAB_500_M62___474kg = (3, WeaponsSu30.FAB_500_M62___474kg)
        FAB_500_M62_UMPK = (3, WeaponsSu30.FAB_500_M62_UMPK)
        FAB_250_M62___227kg = (3, WeaponsSu30.FAB_250_M62___227kg)
        FAB_500_M62_NV___500kg = (3, WeaponsSu30.FAB_500_M62_NV___500kg)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            3,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            3,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            3,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        _2_x_B_13L_pods___10_x_S_13_OF__122mm_UnGd_Rkts__Blast_Frag = (
            3,
            Weapons._2_x_B_13L_pods___10_x_S_13_OF__122mm_UnGd_Rkts__Blast_Frag,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            3,
            Weapons._2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange = (
            3,
            Weapons._2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8OFP2_MPP = (
            3,
            Weapons._2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8OFP2_MPP,
        )
        _2_x_S_25 = (3, Weapons._2_x_S_25)

    class Pylon4:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            4,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range = (
            4,
            WeaponsSu30.R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            4,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_27EP1__AA_10_Alamo_F____Passive_Rdr_Extended_Range = (
            4,
            WeaponsSu30.R_27EP1__AA_10_Alamo_F____Passive_Rdr_Extended_Range,
        )
        R_27P1__AA_10_Alamo_E____Passive_Rdr = (
            4,
            WeaponsSu30.R_27P1__AA_10_Alamo_E____Passive_Rdr,
        )
        R_77__AA_12_Adder_Early____Active_Rdr = (
            4,
            WeaponsSu30.R_77__AA_12_Adder_Early____Active_Rdr,
        )
        R_77_1__AA_12_Adder_B____Active_Rdr = (
            4,
            WeaponsSu30.R_77_1__AA_12_Adder_B____Active_Rdr,
        )
        R_77M__AA_12_Adder_C____Active_Rdr = (
            4,
            WeaponsSu30.R_77M__AA_12_Adder_C____Active_Rdr,
        )
        Kh_31P_AA = (4, WeaponsSu30.Kh_31P_AA)
        Kh_36_Grom_1 = (4, WeaponsSu30.Kh_36_Grom_1)
        KH_38MTE = (4, WeaponsSu30.KH_38MTE)
        KH_38MLE = (4, WeaponsSu30.KH_38MLE)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_ = (
            4,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            4,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            4,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_59M = (4, WeaponsSu30.Kh_59M)
        Kh_59MK = (4, WeaponsSu30.Kh_59MK)
        Kh_31A = (4, WeaponsSu30.Kh_31A)
        KH_35A = (4, WeaponsSu30.KH_35A)
        KH_35UE = (4, WeaponsSu30.KH_35UE)
        KH_31AD = (4, WeaponsSu30.KH_31AD)
        KH_31PD__AA_ = (4, WeaponsSu30.KH_31PD__AA_)
        Kh_59MK2_ = (4, WeaponsSu30.Kh_59MK2_)
        KAB_500Kr___500kg_TV_Guided_Bomb = (4, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg = (4, WeaponsSu30.KAB_500S___500kg)
        KAB_1500Kr___1500kg = (4, WeaponsSu30.KAB_1500Kr___1500kg)
        KAB_1500LG_PR___1500kg = (4, WeaponsSu30.KAB_1500LG_PR___1500kg)
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            4,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            4,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            4,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            4,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            4,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (4, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            4,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            4,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            4,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M54___474kg = (4, WeaponsSu30.FAB_500_M54___474kg)
        FAB_500_M62___474kg = (4, WeaponsSu30.FAB_500_M62___474kg)
        FAB_500_M62_UMPK = (4, WeaponsSu30.FAB_500_M62_UMPK)
        FAB_250_M62___227kg = (4, WeaponsSu30.FAB_250_M62___227kg)
        FAB_500_M62_NV___500kg = (4, WeaponsSu30.FAB_500_M62_NV___500kg)
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            4,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            4,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            4,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD = (
            4,
            Weapons.MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            4,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )

    class Pylon5:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            5,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range = (
            5,
            WeaponsSu30.R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            5,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_27EP1__AA_10_Alamo_F____Passive_Rdr_Extended_Range = (
            5,
            WeaponsSu30.R_27EP1__AA_10_Alamo_F____Passive_Rdr_Extended_Range,
        )
        R_27P1__AA_10_Alamo_E____Passive_Rdr = (
            5,
            WeaponsSu30.R_27P1__AA_10_Alamo_E____Passive_Rdr,
        )
        R_77__AA_12_Adder_Early____Active_Rdr = (
            5,
            WeaponsSu30.R_77__AA_12_Adder_Early____Active_Rdr,
        )
        R_77_1__AA_12_Adder_B____Active_Rdr = (
            5,
            WeaponsSu30.R_77_1__AA_12_Adder_B____Active_Rdr,
        )
        R_77M__AA_12_Adder_C____Active_Rdr = (
            5,
            WeaponsSu30.R_77M__AA_12_Adder_C____Active_Rdr,
        )
        Kh_31P_AA = (5, WeaponsSu30.Kh_31P_AA)
        Kh_36_Grom_1 = (5, WeaponsSu30.Kh_36_Grom_1)
        KH_38MTE = (5, WeaponsSu30.KH_38MTE)
        KH_38MLE = (5, WeaponsSu30.KH_38MLE)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_ = (
            5,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            5,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            5,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_31A = (5, WeaponsSu30.Kh_31A)
        KH_31AD = (5, WeaponsSu30.KH_31AD)
        KH_31PD__AA_ = (5, WeaponsSu30.KH_31PD__AA_)
        KAB_500Kr___500kg_TV_Guided_Bomb = (5, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg = (5, WeaponsSu30.KAB_500S___500kg)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            5,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            5,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        P_50T___50kg_Practice_Bomb_LD = (5, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            5,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            5,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            5,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M54___474kg = (5, WeaponsSu30.FAB_500_M54___474kg)
        FAB_500_M62___474kg = (5, WeaponsSu30.FAB_500_M62___474kg)
        FAB_500_M62_UMPK = (5, WeaponsSu30.FAB_500_M62_UMPK)
        FAB_250_M62___227kg = (5, WeaponsSu30.FAB_250_M62___227kg)
        FAB_500_M62_NV___500kg = (5, WeaponsSu30.FAB_500_M62_NV___500kg)
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            5,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            5,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            5,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            5,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )
        APK_9_POD = (5, WeaponsSu30.APK_9_POD)

    class Pylon6:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            6,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range = (
            6,
            WeaponsSu30.R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            6,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_27EP1__AA_10_Alamo_F____Passive_Rdr_Extended_Range = (
            6,
            WeaponsSu30.R_27EP1__AA_10_Alamo_F____Passive_Rdr_Extended_Range,
        )
        R_27P1__AA_10_Alamo_E____Passive_Rdr = (
            6,
            WeaponsSu30.R_27P1__AA_10_Alamo_E____Passive_Rdr,
        )
        R_77__AA_12_Adder_Early____Active_Rdr = (
            6,
            WeaponsSu30.R_77__AA_12_Adder_Early____Active_Rdr,
        )
        R_77_1__AA_12_Adder_B____Active_Rdr = (
            6,
            WeaponsSu30.R_77_1__AA_12_Adder_B____Active_Rdr,
        )
        R_77M__AA_12_Adder_C____Active_Rdr = (
            6,
            WeaponsSu30.R_77M__AA_12_Adder_C____Active_Rdr,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (6, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg = (6, WeaponsSu30.KAB_500S___500kg)
        KAB_1500Kr___1500kg = (6, WeaponsSu30.KAB_1500Kr___1500kg)
        KAB_1500LG_PR___1500kg = (6, WeaponsSu30.KAB_1500LG_PR___1500kg)
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            6,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            6,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            6,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            6,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            6,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        P_50T___50kg_Practice_Bomb_LD = (6, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            6,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            6,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            6,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M54___474kg = (6, WeaponsSu30.FAB_500_M54___474kg)
        FAB_500_M62___474kg = (6, WeaponsSu30.FAB_500_M62___474kg)
        FAB_500_M62_UMPK = (6, WeaponsSu30.FAB_500_M62_UMPK)
        FAB_250_M62___227kg = (6, WeaponsSu30.FAB_250_M62___227kg)
        FAB_500_M62_NV___500kg = (6, WeaponsSu30.FAB_500_M62_NV___500kg)
        RN_244___260kg__nuclear_bomb = (6, WeaponsSu30.RN_244___260kg__nuclear_bomb)
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            6,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            6,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            6,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            6,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )
        RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag = (
            6,
            Weapons.RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag,
        )
        RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP = (
            6,
            Weapons.RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP,
        )

    class Pylon7:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            7,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range = (
            7,
            WeaponsSu30.R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            7,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_27EP1__AA_10_Alamo_F____Passive_Rdr_Extended_Range = (
            7,
            WeaponsSu30.R_27EP1__AA_10_Alamo_F____Passive_Rdr_Extended_Range,
        )
        R_27P1__AA_10_Alamo_E____Passive_Rdr = (
            7,
            WeaponsSu30.R_27P1__AA_10_Alamo_E____Passive_Rdr,
        )
        R_77__AA_12_Adder_Early____Active_Rdr = (
            7,
            WeaponsSu30.R_77__AA_12_Adder_Early____Active_Rdr,
        )
        R_77_1__AA_12_Adder_B____Active_Rdr = (
            7,
            WeaponsSu30.R_77_1__AA_12_Adder_B____Active_Rdr,
        )
        R_77M__AA_12_Adder_C____Active_Rdr = (
            7,
            WeaponsSu30.R_77M__AA_12_Adder_C____Active_Rdr,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (7, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg = (7, WeaponsSu30.KAB_500S___500kg)
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            7,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            7,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (7, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            7,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            7,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            7,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M54___474kg = (7, WeaponsSu30.FAB_500_M54___474kg)
        FAB_500_M62___474kg = (7, WeaponsSu30.FAB_500_M62___474kg)
        FAB_500_M62_UMPK = (7, WeaponsSu30.FAB_500_M62_UMPK)
        FAB_250_M62___227kg = (7, WeaponsSu30.FAB_250_M62___227kg)
        FAB_500_M62_NV___500kg = (7, WeaponsSu30.FAB_500_M62_NV___500kg)
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            7,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            7,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            7,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            7,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            7,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            7,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )
        Smoke_Generator___red = (7, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (7, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (7, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (7, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (7, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (7, Weapons.Smoke_Generator___orange)
        RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag = (
            7,
            Weapons.RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag,
        )
        RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP = (
            7,
            Weapons.RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP,
        )

    class Pylon8:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            8,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range = (
            8,
            WeaponsSu30.R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            8,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_27EP1__AA_10_Alamo_F____Passive_Rdr_Extended_Range = (
            8,
            WeaponsSu30.R_27EP1__AA_10_Alamo_F____Passive_Rdr_Extended_Range,
        )
        R_27P1__AA_10_Alamo_E____Passive_Rdr = (
            8,
            WeaponsSu30.R_27P1__AA_10_Alamo_E____Passive_Rdr,
        )
        R_77__AA_12_Adder_Early____Active_Rdr = (
            8,
            WeaponsSu30.R_77__AA_12_Adder_Early____Active_Rdr,
        )
        R_77_1__AA_12_Adder_B____Active_Rdr = (
            8,
            WeaponsSu30.R_77_1__AA_12_Adder_B____Active_Rdr,
        )
        R_77M__AA_12_Adder_C____Active_Rdr = (
            8,
            WeaponsSu30.R_77M__AA_12_Adder_C____Active_Rdr,
        )
        Kh_31P_AA = (8, WeaponsSu30.Kh_31P_AA)
        Kh_36_Grom_1 = (8, WeaponsSu30.Kh_36_Grom_1)
        KH_38MTE = (8, WeaponsSu30.KH_38MTE)
        KH_38MLE = (8, WeaponsSu30.KH_38MLE)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_ = (
            8,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            8,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            8,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_31A = (8, WeaponsSu30.Kh_31A)
        KH_31AD = (8, WeaponsSu30.KH_31AD)
        KH_31PD__AA_ = (8, WeaponsSu30.KH_31PD__AA_)
        KAB_500Kr___500kg_TV_Guided_Bomb = (8, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg = (8, WeaponsSu30.KAB_500S___500kg)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            8,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            8,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        P_50T___50kg_Practice_Bomb_LD = (8, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            8,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            8,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            8,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M54___474kg = (8, WeaponsSu30.FAB_500_M54___474kg)
        FAB_500_M62___474kg = (8, WeaponsSu30.FAB_500_M62___474kg)
        FAB_500_M62_UMPK = (8, WeaponsSu30.FAB_500_M62_UMPK)
        FAB_250_M62___227kg = (8, WeaponsSu30.FAB_250_M62___227kg)
        FAB_500_M62_NV___500kg = (8, WeaponsSu30.FAB_500_M62_NV___500kg)
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            8,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            8,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            8,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            8,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )

    class Pylon9:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            9,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range = (
            9,
            WeaponsSu30.R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            9,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_27EP1__AA_10_Alamo_F____Passive_Rdr_Extended_Range = (
            9,
            WeaponsSu30.R_27EP1__AA_10_Alamo_F____Passive_Rdr_Extended_Range,
        )
        R_27P1__AA_10_Alamo_E____Passive_Rdr = (
            9,
            WeaponsSu30.R_27P1__AA_10_Alamo_E____Passive_Rdr,
        )
        R_77__AA_12_Adder_Early____Active_Rdr = (
            9,
            WeaponsSu30.R_77__AA_12_Adder_Early____Active_Rdr,
        )
        R_77_1__AA_12_Adder_B____Active_Rdr = (
            9,
            WeaponsSu30.R_77_1__AA_12_Adder_B____Active_Rdr,
        )
        R_77M__AA_12_Adder_C____Active_Rdr = (
            9,
            WeaponsSu30.R_77M__AA_12_Adder_C____Active_Rdr,
        )
        Kh_31P_AA = (9, WeaponsSu30.Kh_31P_AA)
        Kh_36_Grom_1 = (9, WeaponsSu30.Kh_36_Grom_1)
        KH_38MTE = (9, WeaponsSu30.KH_38MTE)
        KH_38MLE = (9, WeaponsSu30.KH_38MLE)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_ = (
            9,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            9,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            9,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_59M = (9, WeaponsSu30.Kh_59M)
        Kh_59MK = (9, WeaponsSu30.Kh_59MK)
        Kh_31A = (9, WeaponsSu30.Kh_31A)
        KH_35A = (9, WeaponsSu30.KH_35A)
        KH_35UE = (9, WeaponsSu30.KH_35UE)
        KH_31AD = (9, WeaponsSu30.KH_31AD)
        KH_31PD__AA_ = (9, WeaponsSu30.KH_31PD__AA_)
        Kh_59MK2_ = (9, WeaponsSu30.Kh_59MK2_)
        KAB_500Kr___500kg_TV_Guided_Bomb = (9, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg = (9, WeaponsSu30.KAB_500S___500kg)
        KAB_1500Kr___1500kg = (9, WeaponsSu30.KAB_1500Kr___1500kg)
        KAB_1500LG_PR___1500kg = (9, WeaponsSu30.KAB_1500LG_PR___1500kg)
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            9,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            9,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            9,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            9,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            9,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (9, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            9,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            9,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            9,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M54___474kg = (9, WeaponsSu30.FAB_500_M54___474kg)
        FAB_500_M62___474kg = (9, WeaponsSu30.FAB_500_M62___474kg)
        FAB_500_M62_UMPK = (9, WeaponsSu30.FAB_500_M62_UMPK)
        # ERRR {DIS_UMPK_FAB_5002}
        FAB_250_M62___227kg = (9, WeaponsSu30.FAB_250_M62___227kg)
        FAB_500_M62_NV___500kg = (9, WeaponsSu30.FAB_500_M62_NV___500kg)
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            9,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            9,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            9,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD = (
            9,
            Weapons.MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            9,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )

    class Pylon10:
        R_73__AA_11_Archer____Infra_Red = (10, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            10,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            10,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            10,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            10,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27T1__AA_10_Alamo_B____Infra_Red = (
            10,
            WeaponsSu30.R_27T1__AA_10_Alamo_B____Infra_Red,
        )
        R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range = (
            10,
            WeaponsSu30.R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            10,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_27ET1__AA_10_Alamo_D____IR_Extended_Range = (
            10,
            WeaponsSu30.R_27ET1__AA_10_Alamo_D____IR_Extended_Range,
        )
        R_27EP1__AA_10_Alamo_F____Passive_Rdr_Extended_Range = (
            10,
            WeaponsSu30.R_27EP1__AA_10_Alamo_F____Passive_Rdr_Extended_Range,
        )
        R_27P1__AA_10_Alamo_E____Passive_Rdr = (
            10,
            WeaponsSu30.R_27P1__AA_10_Alamo_E____Passive_Rdr,
        )
        R_77__AA_12_Adder_Early____Active_Rdr = (
            10,
            WeaponsSu30.R_77__AA_12_Adder_Early____Active_Rdr,
        )
        R_77_1__AA_12_Adder_B____Active_Rdr = (
            10,
            WeaponsSu30.R_77_1__AA_12_Adder_B____Active_Rdr,
        )
        R_77M__AA_12_Adder_C____Active_Rdr = (
            10,
            WeaponsSu30.R_77M__AA_12_Adder_C____Active_Rdr,
        )
        Kh_31P_AA = (10, WeaponsSu30.Kh_31P_AA)
        Kh_36_Grom_1 = (10, WeaponsSu30.Kh_36_Grom_1)
        KH_38MTE = (10, WeaponsSu30.KH_38MTE)
        KH_38MLE = (10, WeaponsSu30.KH_38MLE)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_ = (
            10,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            10,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            10,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_59M = (10, WeaponsSu30.Kh_59M)
        Kh_59MK = (10, WeaponsSu30.Kh_59MK)
        Kh_31A = (10, WeaponsSu30.Kh_31A)
        KH_35A = (10, WeaponsSu30.KH_35A)
        KH_35UE = (10, WeaponsSu30.KH_35UE)
        KH_31AD = (10, WeaponsSu30.KH_31AD)
        KH_31PD__AA_ = (10, WeaponsSu30.KH_31PD__AA_)
        Kh_59MK2_ = (10, WeaponsSu30.Kh_59MK2_)
        KAB_500Kr___500kg_TV_Guided_Bomb = (
            10,
            Weapons.KAB_500Kr___500kg_TV_Guided_Bomb,
        )
        KAB_500S___500kg = (10, WeaponsSu30.KAB_500S___500kg)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            10,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            10,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            10,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            10,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (10, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            10,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            10,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            10,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M54___474kg = (10, WeaponsSu30.FAB_500_M54___474kg)
        FAB_500_M62___474kg = (10, WeaponsSu30.FAB_500_M62___474kg)
        FAB_500_M62_UMPK = (10, WeaponsSu30.FAB_500_M62_UMPK)
        FAB_250_M62___227kg = (10, WeaponsSu30.FAB_250_M62___227kg)
        FAB_500_M62_NV___500kg = (10, WeaponsSu30.FAB_500_M62_NV___500kg)
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            10,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            10,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            10,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD = (
            10,
            Weapons.MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            10,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )
        _2_x_B_13L_pods___10_x_S_13_OF__122mm_UnGd_Rkts__Blast_Frag = (
            10,
            Weapons._2_x_B_13L_pods___10_x_S_13_OF__122mm_UnGd_Rkts__Blast_Frag,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            10,
            Weapons._2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange = (
            10,
            Weapons._2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8OFP2_MPP = (
            10,
            Weapons._2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8OFP2_MPP,
        )
        _2_x_S_25 = (10, Weapons._2_x_S_25)

    class Pylon11:
        R_73__AA_11_Archer____Infra_Red = (11, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            11,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            11,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            11,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        R_77__AA_12_Adder_Early____Active_Rdr = (
            11,
            WeaponsSu30.R_77__AA_12_Adder_Early____Active_Rdr,
        )
        R_77_1__AA_12_Adder_B____Active_Rdr = (
            11,
            WeaponsSu30.R_77_1__AA_12_Adder_B____Active_Rdr,
        )
        R_77M__AA_12_Adder_C____Active_Rdr = (
            11,
            WeaponsSu30.R_77M__AA_12_Adder_C____Active_Rdr,
        )
        Smoke_Generator___red = (11, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (11, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (11, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (11, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (11, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (11, Weapons.Smoke_Generator___orange)

    class Pylon12:
        R_73__AA_11_Archer____Infra_Red = (12, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            12,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            12,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            12,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        L005_Sorbtsiya_ECM_pod__right_ = (12, Weapons.L005_Sorbtsiya_ECM_pod__right_)
        SAP_518_ECM_Pod__Right_ = (12, WeaponsSu30.SAP_518_ECM_Pod__Right_)
        Smoke_Generator___red = (12, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (12, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (12, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (12, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (12, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (12, Weapons.Smoke_Generator___orange)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.AFAC,
        task.SEAD,
        task.AntishipStrike,
        task.CAS,
        task.PinpointStrike,
        task.GroundAttack,
        task.RunwayAttack,
    ]
    task_default = task.CAP
