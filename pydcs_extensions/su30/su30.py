from typing import Dict, Any, Set

from dcs import task
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

from game.modsupport import planemod
from pydcs_extensions.weapon_injector import inject_weapons


class WeaponsSu30:
    APK_9_POD = {"clsid": "{SU30_APK-9}", "name": "APK-9 POD", "weight": 295}
    ASTRA_Mk_1___Active_Rdr_AAM = {
        "clsid": "{Su30_ASTRA}",
        "name": "ASTRA Mk.1 - Active Rdr AAM",
        "weight": 154,
    }
    BRAHMOS_A_Ship = {"clsid": "{BRAHMOS_S}", "name": "BRAHMOS A-Ship", "weight": 2500}
    DAMOCLES___Targeting_Pod = {
        "clsid": "{DAMOCLES}",
        "name": "DAMOCLES - Targeting Pod",
        "weight": 208,
    }

    I_Derby_ER___Active_Rdr_AAM = {
        "clsid": "{Su30_DERBY_ER}",
        "name": "I-Derby ER - Active Rdr AAM",
        "weight": 118,
    }
    KAB_1500LG_Pr = {
        "clsid": "{SU30_KAB_1500LG_LOADOUT}",
        "name": "KAB-1500LG-Pr",
        "weight": 1525,
    }
    KAB_1500t = {
        "clsid": "{SU30_KAB_1500Kr_LOADOUT}",
        "name": "KAB-1500t",
        "weight": 1525,
    }
    KAB_500S = {"clsid": "{SU30_KAB_500S_LOADOUT}", "name": "KAB-500S", "weight": 500}
    KH_29L__AS_14_Kedge___Semi_Act_Laser = {
        "clsid": "{SU30_KH29L}",
        "name": "KH-29L (AS-14 Kedge), Semi-Act Laser",
        "weight": 657,
    }
    KH_29TE__AS_14_Kedge___TV_Guided = {
        "clsid": "{SU30_KH29TE}",
        "name": "KH-29TE (AS-14 Kedge), TV Guided",
        "weight": 780,
    }
    KH_29T__AS_14_Kedge___TV_Guided = {
        "clsid": "{SU30_KH29T}",
        "name": "KH-29T (AS-14 Kedge), TV Guided",
        "weight": 670,
    }
    KH_31AD = {"clsid": "{SU30_KH31AD}", "name": "KH-31AD", "weight": 690}
    KH_31PD = {"clsid": "{SU30_KH31PD}", "name": "KH-31PD", "weight": 690}
    KH_35A = {"clsid": "{SU30_KH_35}", "name": "KH-35A", "weight": 540}
    KH_35UE = {"clsid": "{SU30_KH_35UE}", "name": "KH-35UE", "weight": 540}
    KH_38MAE = {"clsid": "{SU30_KH38MAE}", "name": "KH-38MAE", "weight": 520}
    KH_38MLE = {"clsid": "{SU30_KH38MLE}", "name": "KH-38MLE", "weight": 520}
    KH_38MTE = {"clsid": "{SU30_KH38MTE}", "name": "KH-38MTE", "weight": 1240}
    Kh_31A = {"clsid": "{SU30_KH_31A}", "name": "Kh-31A", "weight": 690}
    Kh_31P = {"clsid": "{SU30_KH31P}", "name": "Kh-31P", "weight": 690}
    Kh_36_Grom_1 = {"clsid": "{SU30_KH36}", "name": "Kh-36 Grom-1", "weight": 690}
    Kh_59M = {"clsid": "{SU30_KH59M}", "name": "Kh-59M", "weight": 930}
    Kh_59MK = {"clsid": "{SU30_KH59MK}", "name": "Kh-59MK", "weight": 770}
    Kh_59MK2 = {"clsid": "{KH_59MK2}", "name": "Kh-59MK2", "weight": None}
    Kh_59MK2_ = {"clsid": "{SU30_KH59MK2}", "name": "Kh-59MK2", "weight": 770}
    LITENING___Targeting_Pod = {
        "clsid": "{LITENING_POD}",
        "name": "LITENING - Targeting Pod",
        "weight": 1.4789,
    }
    Rudra_M1 = {"clsid": "{SU30_RudraM1}", "name": "Rudra-M1", "weight": 690}
    R_27EA__Active_Rdr_AAM = {
        "clsid": "{SU30_R27EA}",
        "name": "R-27EA, Active Rdr AAM",
        "weight": 350,
    }
    R_27EP__Passive_Rdr_AAM = {
        "clsid": "{SU30_R27EP}",
        "name": "R-27EP, Passive Rdr AAM",
        "weight": 346,
    }
    R_27ER__Semi_Active_Rdr_AAM = {
        "clsid": "{SU30_R27ER}",
        "name": "R-27ER, Semi-Active Rdr AAM",
        "weight": 350,
    }
    R_27ET__IR_AAM = {"clsid": "{SU30_R27ET}", "name": "R-27ET, IR AAM", "weight": 343}
    R_27R__Semi_Active_Rdr_AAM = {
        "clsid": "{SU30_R27R}",
        "name": "R-27R, Semi-Active Rdr AAM",
        "weight": 253,
    }
    R_27T__IR_AAM = {"clsid": "{SU30_R27T}", "name": "R-27T, IR AAM", "weight": 245}
    R_77M__Active_Rdr_AAM = {
        "clsid": "{SU30_R77M}",
        "name": "R-77M, Active Rdr AAM",
        "weight": 210,
    }
    R_77_1__Active_Rdr_AAM = {
        "clsid": "{SU30_R771}",
        "name": "R-77-1, Active Rdr AAM",
        "weight": 190,
    }
    R_77__Active_Rdr_AAM = {
        "clsid": "{SU30_R77}",
        "name": "R-77, Active Rdr AAM",
        "weight": 175,
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
        L005_Sorbtsiya_ECM_pod__left_ = (1, Weapons.L005_Sorbtsiya_ECM_pod__left_)
        Smoke_Generator___red = (1, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (1, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (1, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (1, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (1, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (1, Weapons.Smoke_Generator___orange)

    class Pylon2:
        R_73__AA_11_Archer____Infra_Red = (2, Weapons.R_73__AA_11_Archer____Infra_Red)
        ASTRA_Mk_1___Active_Rdr_AAM = (2, WeaponsSu30.ASTRA_Mk_1___Active_Rdr_AAM)
        I_Derby_ER___Active_Rdr_AAM = (2, WeaponsSu30.I_Derby_ER___Active_Rdr_AAM)
        Smoke_Generator___red = (2, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (2, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (2, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (2, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (2, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (2, Weapons.Smoke_Generator___orange)

    class Pylon3:
        R_73__AA_11_Archer____Infra_Red = (3, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_27R__Semi_Active_Rdr_AAM = (3, WeaponsSu30.R_27R__Semi_Active_Rdr_AAM)
        R_27T__IR_AAM = (3, WeaponsSu30.R_27T__IR_AAM)
        R_27ER__Semi_Active_Rdr_AAM = (3, WeaponsSu30.R_27ER__Semi_Active_Rdr_AAM)
        R_27ET__IR_AAM = (3, WeaponsSu30.R_27ET__IR_AAM)
        ASTRA_Mk_1___Active_Rdr_AAM = (3, WeaponsSu30.ASTRA_Mk_1___Active_Rdr_AAM)
        I_Derby_ER___Active_Rdr_AAM = (3, WeaponsSu30.I_Derby_ER___Active_Rdr_AAM)
        R_77__Active_Rdr_AAM = (3, WeaponsSu30.R_77__Active_Rdr_AAM)
        R_77_1__Active_Rdr_AAM = (3, WeaponsSu30.R_77_1__Active_Rdr_AAM)
        R_27EA__Active_Rdr_AAM = (3, WeaponsSu30.R_27EA__Active_Rdr_AAM)
        R_27EP__Passive_Rdr_AAM = (3, WeaponsSu30.R_27EP__Passive_Rdr_AAM)
        Kh_31P__AS_17_Krypton____600kg__ARM__IN__Pas_Rdr = (
            3,
            Weapons.Kh_31P__AS_17_Krypton____600kg__ARM__IN__Pas_Rdr,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            3,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_ = (
            3,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_,
        )
        Kh_59M = (3, WeaponsSu30.Kh_59M)
        Kh_59MK = (3, WeaponsSu30.Kh_59MK)
        Kh_31A = (3, WeaponsSu30.Kh_31A)
        Kh_31P = (3, WeaponsSu30.Kh_31P)
        KH_35A = (3, WeaponsSu30.KH_35A)
        Rudra_M1 = (3, WeaponsSu30.Rudra_M1)
        SAAW_POD = (3, WeaponsSu30.SAAW_POD)
        KAB_500Kr___500kg_TV_Guided_Bomb = (3, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S = (3, WeaponsSu30.KAB_500S)
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
        _2_x_B_13L___5_S_13_OF = (3, Weapons._2_x_B_13L___5_S_13_OF)
        _2_x_B_8M1___20_S_8KOM = (3, Weapons._2_x_B_8M1___20_S_8KOM)
        _2_x_S_25 = (3, Weapons._2_x_S_25)

    class Pylon4:
        R_73__AA_11_Archer____Infra_Red = (4, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_27ER__Semi_Active_Rdr_AAM = (4, WeaponsSu30.R_27ER__Semi_Active_Rdr_AAM)
        R_27ET__IR_AAM = (4, WeaponsSu30.R_27ET__IR_AAM)
        I_Derby_ER___Active_Rdr_AAM = (4, WeaponsSu30.I_Derby_ER___Active_Rdr_AAM)
        R_77__Active_Rdr_AAM = (4, WeaponsSu30.R_77__Active_Rdr_AAM)
        R_77_1__Active_Rdr_AAM = (4, WeaponsSu30.R_77_1__Active_Rdr_AAM)
        R_27EA__Active_Rdr_AAM = (4, WeaponsSu30.R_27EA__Active_Rdr_AAM)
        R_27EP__Passive_Rdr_AAM = (4, WeaponsSu30.R_27EP__Passive_Rdr_AAM)
        Kh_31P__AS_17_Krypton____600kg__ARM__IN__Pas_Rdr = (
            4,
            Weapons.Kh_31P__AS_17_Krypton____600kg__ARM__IN__Pas_Rdr,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            4,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_ = (
            4,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_,
        )
        Kh_59M = (4, WeaponsSu30.Kh_59M)
        Kh_59MK = (4, WeaponsSu30.Kh_59MK)
        Kh_31A = (4, WeaponsSu30.Kh_31A)
        Kh_31P = (4, WeaponsSu30.Kh_31P)
        KH_35A = (4, WeaponsSu30.KH_35A)
        Rudra_M1 = (4, WeaponsSu30.Rudra_M1)
        SAAW_POD = (4, WeaponsSu30.SAAW_POD)
        KAB_500Kr___500kg_TV_Guided_Bomb = (4, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S = (4, WeaponsSu30.KAB_500S)
        KAB_1500t = (4, WeaponsSu30.KAB_1500t)
        KAB_1500LG_Pr = (4, WeaponsSu30.KAB_1500LG_Pr)
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            4,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
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

    class Pylon5:
        R_27ER__Semi_Active_Rdr_AAM = (5, WeaponsSu30.R_27ER__Semi_Active_Rdr_AAM)
        I_Derby_ER___Active_Rdr_AAM = (5, WeaponsSu30.I_Derby_ER___Active_Rdr_AAM)
        R_77__Active_Rdr_AAM = (5, WeaponsSu30.R_77__Active_Rdr_AAM)
        R_77_1__Active_Rdr_AAM = (5, WeaponsSu30.R_77_1__Active_Rdr_AAM)
        R_27EA__Active_Rdr_AAM = (5, WeaponsSu30.R_27EA__Active_Rdr_AAM)
        R_27EP__Passive_Rdr_AAM = (5, WeaponsSu30.R_27EP__Passive_Rdr_AAM)
        Kh_31P__AS_17_Krypton____600kg__ARM__IN__Pas_Rdr = (
            5,
            Weapons.Kh_31P__AS_17_Krypton____600kg__ARM__IN__Pas_Rdr,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            5,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_ = (
            5,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_,
        )
        Kh_31A = (5, WeaponsSu30.Kh_31A)
        Kh_31P = (5, WeaponsSu30.Kh_31P)
        Rudra_M1 = (5, WeaponsSu30.Rudra_M1)
        APK_9_POD = (5, WeaponsSu30.APK_9_POD)
        KAB_500Kr___500kg_TV_Guided_Bomb = (5, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S = (5, WeaponsSu30.KAB_500S)
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
        L_081_Fantasmagoria_ELINT_pod = (5, Weapons.L_081_Fantasmagoria_ELINT_pod)

    class Pylon6:
        R_77__Active_Rdr_AAM = (6, WeaponsSu30.R_77__Active_Rdr_AAM)
        R_77_1__Active_Rdr_AAM = (6, WeaponsSu30.R_77_1__Active_Rdr_AAM)
        R_27EA__Active_Rdr_AAM = (6, WeaponsSu30.R_27EA__Active_Rdr_AAM)
        R_27EP__Passive_Rdr_AAM = (6, WeaponsSu30.R_27EP__Passive_Rdr_AAM)
        I_Derby_ER___Active_Rdr_AAM = (6, WeaponsSu30.I_Derby_ER___Active_Rdr_AAM)
        # ERRR {BRAHMOS}
        BRAHMOS_A_Ship = (6, WeaponsSu30.BRAHMOS_A_Ship)
        KAB_500Kr___500kg_TV_Guided_Bomb = (6, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S = (6, WeaponsSu30.KAB_500S)
        KAB_1500t = (6, WeaponsSu30.KAB_1500t)
        KAB_1500LG_Pr = (6, WeaponsSu30.KAB_1500LG_Pr)
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

    class Pylon7:
        R_77__Active_Rdr_AAM = (7, WeaponsSu30.R_77__Active_Rdr_AAM)
        I_Derby_ER___Active_Rdr_AAM = (7, WeaponsSu30.I_Derby_ER___Active_Rdr_AAM)
        R_77_1__Active_Rdr_AAM = (7, WeaponsSu30.R_77_1__Active_Rdr_AAM)
        R_27EA__Active_Rdr_AAM = (7, WeaponsSu30.R_27EA__Active_Rdr_AAM)
        R_27EP__Passive_Rdr_AAM = (7, WeaponsSu30.R_27EP__Passive_Rdr_AAM)
        KAB_500Kr___500kg_TV_Guided_Bomb = (7, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S = (7, WeaponsSu30.KAB_500S)
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
        # ERRR <CLEAN>
        RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag = (
            7,
            Weapons.RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag,
        )
        RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP = (
            7,
            Weapons.RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP,
        )

    class Pylon8:
        R_27ET__IR_AAM = (8, WeaponsSu30.R_27ET__IR_AAM)
        R_27ER__Semi_Active_Rdr_AAM = (8, WeaponsSu30.R_27ER__Semi_Active_Rdr_AAM)
        R_77_1__Active_Rdr_AAM = (8, WeaponsSu30.R_77_1__Active_Rdr_AAM)
        R_27EA__Active_Rdr_AAM = (8, WeaponsSu30.R_27EA__Active_Rdr_AAM)
        R_27EP__Passive_Rdr_AAM = (8, WeaponsSu30.R_27EP__Passive_Rdr_AAM)
        I_Derby_ER___Active_Rdr_AAM = (8, WeaponsSu30.I_Derby_ER___Active_Rdr_AAM)
        R_77__Active_Rdr_AAM = (8, WeaponsSu30.R_77__Active_Rdr_AAM)
        Kh_31P__AS_17_Krypton____600kg__ARM__IN__Pas_Rdr = (
            8,
            Weapons.Kh_31P__AS_17_Krypton____600kg__ARM__IN__Pas_Rdr,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            8,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_ = (
            8,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_,
        )
        Kh_59M = (8, WeaponsSu30.Kh_59M)
        Kh_59MK = (8, WeaponsSu30.Kh_59MK)
        Kh_31A = (8, WeaponsSu30.Kh_31A)
        Kh_31P = (8, WeaponsSu30.Kh_31P)
        Rudra_M1 = (8, WeaponsSu30.Rudra_M1)
        KAB_500Kr___500kg_TV_Guided_Bomb = (8, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S = (8, WeaponsSu30.KAB_500S)
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
        LITENING___Targeting_Pod = (8, WeaponsSu30.LITENING___Targeting_Pod)

    class Pylon9:
        R_73__AA_11_Archer____Infra_Red = (9, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_27ER__Semi_Active_Rdr_AAM = (9, WeaponsSu30.R_27ER__Semi_Active_Rdr_AAM)
        R_27ET__IR_AAM = (9, WeaponsSu30.R_27ET__IR_AAM)
        R_77_1__Active_Rdr_AAM = (9, WeaponsSu30.R_77_1__Active_Rdr_AAM)
        R_27EA__Active_Rdr_AAM = (9, WeaponsSu30.R_27EA__Active_Rdr_AAM)
        R_27EP__Passive_Rdr_AAM = (9, WeaponsSu30.R_27EP__Passive_Rdr_AAM)
        I_Derby_ER___Active_Rdr_AAM = (9, WeaponsSu30.I_Derby_ER___Active_Rdr_AAM)
        R_77__Active_Rdr_AAM = (9, WeaponsSu30.R_77__Active_Rdr_AAM)
        Kh_31P__AS_17_Krypton____600kg__ARM__IN__Pas_Rdr = (
            9,
            Weapons.Kh_31P__AS_17_Krypton____600kg__ARM__IN__Pas_Rdr,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            9,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_ = (
            9,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_,
        )
        Kh_59M = (9, WeaponsSu30.Kh_59M)
        Kh_59MK = (9, WeaponsSu30.Kh_59MK)
        Kh_31A = (9, WeaponsSu30.Kh_31A)
        Kh_31P = (9, WeaponsSu30.Kh_31P)
        KH_35A = (9, WeaponsSu30.KH_35A)
        Rudra_M1 = (9, WeaponsSu30.Rudra_M1)
        SAAW_POD = (9, WeaponsSu30.SAAW_POD)
        KAB_500Kr___500kg_TV_Guided_Bomb = (9, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S = (9, WeaponsSu30.KAB_500S)
        KAB_1500t = (9, WeaponsSu30.KAB_1500t)
        KAB_1500LG_Pr = (9, WeaponsSu30.KAB_1500LG_Pr)
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

    class Pylon10:
        R_73__AA_11_Archer____Infra_Red = (10, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_27R__Semi_Active_Rdr_AAM = (10, WeaponsSu30.R_27R__Semi_Active_Rdr_AAM)
        R_27T__IR_AAM = (10, WeaponsSu30.R_27T__IR_AAM)
        R_27ER__Semi_Active_Rdr_AAM = (10, WeaponsSu30.R_27ER__Semi_Active_Rdr_AAM)
        R_27ET__IR_AAM = (10, WeaponsSu30.R_27ET__IR_AAM)
        ASTRA_Mk_1___Active_Rdr_AAM = (10, WeaponsSu30.ASTRA_Mk_1___Active_Rdr_AAM)
        I_Derby_ER___Active_Rdr_AAM = (10, WeaponsSu30.I_Derby_ER___Active_Rdr_AAM)
        R_77_1__Active_Rdr_AAM = (10, WeaponsSu30.R_77_1__Active_Rdr_AAM)
        R_27EA__Active_Rdr_AAM = (10, WeaponsSu30.R_27EA__Active_Rdr_AAM)
        R_27EP__Passive_Rdr_AAM = (10, WeaponsSu30.R_27EP__Passive_Rdr_AAM)
        R_77__Active_Rdr_AAM = (10, WeaponsSu30.R_77__Active_Rdr_AAM)
        Kh_31P__AS_17_Krypton____600kg__ARM__IN__Pas_Rdr = (
            10,
            Weapons.Kh_31P__AS_17_Krypton____600kg__ARM__IN__Pas_Rdr,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            10,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_ = (
            10,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_,
        )
        Kh_59M = (10, WeaponsSu30.Kh_59M)
        Kh_59MK = (10, WeaponsSu30.Kh_59MK)
        Kh_31A = (10, WeaponsSu30.Kh_31A)
        Kh_31P = (10, WeaponsSu30.Kh_31P)
        KH_35A = (10, WeaponsSu30.KH_35A)
        Rudra_M1 = (10, WeaponsSu30.Rudra_M1)
        SAAW_POD = (10, WeaponsSu30.SAAW_POD)
        KAB_500Kr___500kg_TV_Guided_Bomb = (
            10,
            Weapons.KAB_500Kr___500kg_TV_Guided_Bomb,
        )
        KAB_500S = (10, WeaponsSu30.KAB_500S)
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
        _2_x_B_13L___5_S_13_OF = (10, Weapons._2_x_B_13L___5_S_13_OF)
        _2_x_B_8M1___20_S_8KOM = (10, Weapons._2_x_B_8M1___20_S_8KOM)
        _2_x_S_25 = (10, Weapons._2_x_S_25)

    class Pylon11:
        R_73__AA_11_Archer____Infra_Red = (11, Weapons.R_73__AA_11_Archer____Infra_Red)
        ASTRA_Mk_1___Active_Rdr_AAM = (11, WeaponsSu30.ASTRA_Mk_1___Active_Rdr_AAM)
        I_Derby_ER___Active_Rdr_AAM = (11, WeaponsSu30.I_Derby_ER___Active_Rdr_AAM)
        Smoke_Generator___red = (11, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (11, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (11, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (11, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (11, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (11, Weapons.Smoke_Generator___orange)

    class Pylon12:
        R_73__AA_11_Archer____Infra_Red = (12, Weapons.R_73__AA_11_Archer____Infra_Red)
        L005_Sorbtsiya_ECM_pod__right_ = (12, Weapons.L005_Sorbtsiya_ECM_pod__right_)
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
        L005_Sorbtsiya_ECM_pod__left_ = (1, Weapons.L005_Sorbtsiya_ECM_pod__left_)
        Smoke_Generator___red = (1, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (1, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (1, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (1, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (1, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (1, Weapons.Smoke_Generator___orange)

    class Pylon2:
        R_73__AA_11_Archer____Infra_Red = (2, Weapons.R_73__AA_11_Archer____Infra_Red)
        Smoke_Generator___red = (2, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (2, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (2, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (2, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (2, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (2, Weapons.Smoke_Generator___orange)

    class Pylon3:
        R_73__AA_11_Archer____Infra_Red = (3, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_27R__Semi_Active_Rdr_AAM = (3, WeaponsSu30.R_27R__Semi_Active_Rdr_AAM)
        R_27T__IR_AAM = (3, WeaponsSu30.R_27T__IR_AAM)
        R_27ER__Semi_Active_Rdr_AAM = (3, WeaponsSu30.R_27ER__Semi_Active_Rdr_AAM)
        R_27ET__IR_AAM = (3, WeaponsSu30.R_27ET__IR_AAM)
        R_77__Active_Rdr_AAM = (3, WeaponsSu30.R_77__Active_Rdr_AAM)
        Kh_31P = (3, WeaponsSu30.Kh_31P)
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
        KAB_500S = (3, WeaponsSu30.KAB_500S)
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
        _2_x_B_13L___5_S_13_OF = (3, Weapons._2_x_B_13L___5_S_13_OF)
        _2_x_B_8M1___20_S_8KOM = (3, Weapons._2_x_B_8M1___20_S_8KOM)
        _2_x_S_25 = (3, Weapons._2_x_S_25)

    class Pylon4:
        R_73__AA_11_Archer____Infra_Red = (4, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_27R__Semi_Active_Rdr_AAM = (4, WeaponsSu30.R_27R__Semi_Active_Rdr_AAM)
        R_27T__IR_AAM = (4, WeaponsSu30.R_27T__IR_AAM)
        R_27ER__Semi_Active_Rdr_AAM = (4, WeaponsSu30.R_27ER__Semi_Active_Rdr_AAM)
        R_27ET__IR_AAM = (4, WeaponsSu30.R_27ET__IR_AAM)
        R_77__Active_Rdr_AAM = (4, WeaponsSu30.R_77__Active_Rdr_AAM)
        Kh_31P = (4, WeaponsSu30.Kh_31P)
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
        KAB_500S = (4, WeaponsSu30.KAB_500S)
        KAB_1500t = (4, WeaponsSu30.KAB_1500t)
        KAB_1500LG_Pr = (4, WeaponsSu30.KAB_1500LG_Pr)
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            4,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
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

    class Pylon5:
        R_27R__Semi_Active_Rdr_AAM = (5, WeaponsSu30.R_27R__Semi_Active_Rdr_AAM)
        R_27ER__Semi_Active_Rdr_AAM = (5, WeaponsSu30.R_27ER__Semi_Active_Rdr_AAM)
        R_77__Active_Rdr_AAM = (5, WeaponsSu30.R_77__Active_Rdr_AAM)
        Kh_31P = (5, WeaponsSu30.Kh_31P)
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
        KAB_500S = (5, WeaponsSu30.KAB_500S)
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

    class Pylon6:
        R_27R__Semi_Active_Rdr_AAM = (6, WeaponsSu30.R_27R__Semi_Active_Rdr_AAM)
        R_27ER__Semi_Active_Rdr_AAM = (6, WeaponsSu30.R_27ER__Semi_Active_Rdr_AAM)
        R_77__Active_Rdr_AAM = (6, WeaponsSu30.R_77__Active_Rdr_AAM)
        KAB_500Kr___500kg_TV_Guided_Bomb = (6, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S = (6, WeaponsSu30.KAB_500S)
        KAB_1500t = (6, WeaponsSu30.KAB_1500t)
        KAB_1500LG_Pr = (6, WeaponsSu30.KAB_1500LG_Pr)
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

    class Pylon7:
        R_27R__Semi_Active_Rdr_AAM = (7, WeaponsSu30.R_27R__Semi_Active_Rdr_AAM)
        R_27ER__Semi_Active_Rdr_AAM = (7, WeaponsSu30.R_27ER__Semi_Active_Rdr_AAM)
        R_77__Active_Rdr_AAM = (7, WeaponsSu30.R_77__Active_Rdr_AAM)
        KAB_500Kr___500kg_TV_Guided_Bomb = (7, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S = (7, WeaponsSu30.KAB_500S)
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

    class Pylon8:
        R_27R__Semi_Active_Rdr_AAM = (8, WeaponsSu30.R_27R__Semi_Active_Rdr_AAM)
        R_27ER__Semi_Active_Rdr_AAM = (8, WeaponsSu30.R_27ER__Semi_Active_Rdr_AAM)
        R_77__Active_Rdr_AAM = (8, WeaponsSu30.R_77__Active_Rdr_AAM)
        Kh_31P = (8, WeaponsSu30.Kh_31P)
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
        KAB_500S = (8, WeaponsSu30.KAB_500S)
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
        DAMOCLES___Targeting_Pod = (8, WeaponsSu30.DAMOCLES___Targeting_Pod)

    class Pylon9:
        R_73__AA_11_Archer____Infra_Red = (9, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_27R__Semi_Active_Rdr_AAM = (9, WeaponsSu30.R_27R__Semi_Active_Rdr_AAM)
        R_27T__IR_AAM = (9, WeaponsSu30.R_27T__IR_AAM)
        R_27ER__Semi_Active_Rdr_AAM = (9, WeaponsSu30.R_27ER__Semi_Active_Rdr_AAM)
        R_27ET__IR_AAM = (9, WeaponsSu30.R_27ET__IR_AAM)
        R_77__Active_Rdr_AAM = (9, WeaponsSu30.R_77__Active_Rdr_AAM)
        Kh_31P = (9, WeaponsSu30.Kh_31P)
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
        KAB_500S = (9, WeaponsSu30.KAB_500S)
        KAB_1500t = (9, WeaponsSu30.KAB_1500t)
        KAB_1500LG_Pr = (9, WeaponsSu30.KAB_1500LG_Pr)
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

    class Pylon10:
        R_73__AA_11_Archer____Infra_Red = (10, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_27R__Semi_Active_Rdr_AAM = (10, WeaponsSu30.R_27R__Semi_Active_Rdr_AAM)
        R_27T__IR_AAM = (10, WeaponsSu30.R_27T__IR_AAM)
        R_27ER__Semi_Active_Rdr_AAM = (10, WeaponsSu30.R_27ER__Semi_Active_Rdr_AAM)
        R_27ET__IR_AAM = (10, WeaponsSu30.R_27ET__IR_AAM)
        R_77__Active_Rdr_AAM = (10, WeaponsSu30.R_77__Active_Rdr_AAM)
        Kh_31P = (10, WeaponsSu30.Kh_31P)
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
        KAB_500S = (10, WeaponsSu30.KAB_500S)
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
        _2_x_B_13L___5_S_13_OF = (10, Weapons._2_x_B_13L___5_S_13_OF)
        _2_x_B_8M1___20_S_8KOM = (10, Weapons._2_x_B_8M1___20_S_8KOM)
        _2_x_S_25 = (10, Weapons._2_x_S_25)

    class Pylon11:
        R_73__AA_11_Archer____Infra_Red = (11, Weapons.R_73__AA_11_Archer____Infra_Red)
        Smoke_Generator___red = (11, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (11, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (11, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (11, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (11, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (11, Weapons.Smoke_Generator___orange)

    class Pylon12:
        R_73__AA_11_Archer____Infra_Red = (12, Weapons.R_73__AA_11_Archer____Infra_Red)
        L005_Sorbtsiya_ECM_pod__right_ = (12, Weapons.L005_Sorbtsiya_ECM_pod__right_)
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
        L005_Sorbtsiya_ECM_pod__left_ = (1, Weapons.L005_Sorbtsiya_ECM_pod__left_)
        Smoke_Generator___red = (1, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (1, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (1, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (1, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (1, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (1, Weapons.Smoke_Generator___orange)

    class Pylon2:
        R_73__AA_11_Archer____Infra_Red = (2, Weapons.R_73__AA_11_Archer____Infra_Red)
        Smoke_Generator___red = (2, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (2, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (2, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (2, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (2, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (2, Weapons.Smoke_Generator___orange)

    class Pylon3:
        R_73__AA_11_Archer____Infra_Red = (3, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_27R__Semi_Active_Rdr_AAM = (3, WeaponsSu30.R_27R__Semi_Active_Rdr_AAM)
        R_27T__IR_AAM = (3, WeaponsSu30.R_27T__IR_AAM)
        R_27ER__Semi_Active_Rdr_AAM = (3, WeaponsSu30.R_27ER__Semi_Active_Rdr_AAM)
        R_27ET__IR_AAM = (3, WeaponsSu30.R_27ET__IR_AAM)
        R_77__Active_Rdr_AAM = (3, WeaponsSu30.R_77__Active_Rdr_AAM)
        Kh_31P = (3, WeaponsSu30.Kh_31P)
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
        KAB_500S = (3, WeaponsSu30.KAB_500S)
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
        _2_x_B_13L___5_S_13_OF = (3, Weapons._2_x_B_13L___5_S_13_OF)
        _2_x_B_8M1___20_S_8KOM = (3, Weapons._2_x_B_8M1___20_S_8KOM)
        _2_x_S_25 = (3, Weapons._2_x_S_25)

    class Pylon4:
        R_73__AA_11_Archer____Infra_Red = (4, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_27R__Semi_Active_Rdr_AAM = (4, WeaponsSu30.R_27R__Semi_Active_Rdr_AAM)
        R_27T__IR_AAM = (4, WeaponsSu30.R_27T__IR_AAM)
        R_27ER__Semi_Active_Rdr_AAM = (4, WeaponsSu30.R_27ER__Semi_Active_Rdr_AAM)
        R_27ET__IR_AAM = (4, WeaponsSu30.R_27ET__IR_AAM)
        R_77__Active_Rdr_AAM = (4, WeaponsSu30.R_77__Active_Rdr_AAM)
        Kh_31P = (4, WeaponsSu30.Kh_31P)
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
        KAB_500S = (4, WeaponsSu30.KAB_500S)
        KAB_1500t = (4, WeaponsSu30.KAB_1500t)
        KAB_1500LG_Pr = (4, WeaponsSu30.KAB_1500LG_Pr)
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            4,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
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

    class Pylon5:
        R_27R__Semi_Active_Rdr_AAM = (5, WeaponsSu30.R_27R__Semi_Active_Rdr_AAM)
        R_27ER__Semi_Active_Rdr_AAM = (5, WeaponsSu30.R_27ER__Semi_Active_Rdr_AAM)
        R_77__Active_Rdr_AAM = (5, WeaponsSu30.R_77__Active_Rdr_AAM)
        Kh_31P = (5, WeaponsSu30.Kh_31P)
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
        KAB_500S = (5, WeaponsSu30.KAB_500S)
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

    class Pylon6:
        R_27R__Semi_Active_Rdr_AAM = (6, WeaponsSu30.R_27R__Semi_Active_Rdr_AAM)
        R_27ER__Semi_Active_Rdr_AAM = (6, WeaponsSu30.R_27ER__Semi_Active_Rdr_AAM)
        R_77__Active_Rdr_AAM = (6, WeaponsSu30.R_77__Active_Rdr_AAM)
        KAB_500Kr___500kg_TV_Guided_Bomb = (6, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S = (6, WeaponsSu30.KAB_500S)
        KAB_1500t = (6, WeaponsSu30.KAB_1500t)
        KAB_1500LG_Pr = (6, WeaponsSu30.KAB_1500LG_Pr)
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

    class Pylon7:
        R_27R__Semi_Active_Rdr_AAM = (7, WeaponsSu30.R_27R__Semi_Active_Rdr_AAM)
        R_27ER__Semi_Active_Rdr_AAM = (7, WeaponsSu30.R_27ER__Semi_Active_Rdr_AAM)
        R_77__Active_Rdr_AAM = (7, WeaponsSu30.R_77__Active_Rdr_AAM)
        KAB_500Kr___500kg_TV_Guided_Bomb = (7, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S = (7, WeaponsSu30.KAB_500S)
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

    class Pylon8:
        R_27R__Semi_Active_Rdr_AAM = (8, WeaponsSu30.R_27R__Semi_Active_Rdr_AAM)
        R_27ER__Semi_Active_Rdr_AAM = (8, WeaponsSu30.R_27ER__Semi_Active_Rdr_AAM)
        R_77__Active_Rdr_AAM = (8, WeaponsSu30.R_77__Active_Rdr_AAM)
        Kh_31P = (8, WeaponsSu30.Kh_31P)
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
        KAB_500S = (8, WeaponsSu30.KAB_500S)
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
        DAMOCLES___Targeting_Pod = (8, WeaponsSu30.DAMOCLES___Targeting_Pod)

    class Pylon9:
        R_73__AA_11_Archer____Infra_Red = (9, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_27R__Semi_Active_Rdr_AAM = (9, WeaponsSu30.R_27R__Semi_Active_Rdr_AAM)
        R_27T__IR_AAM = (9, WeaponsSu30.R_27T__IR_AAM)
        R_27ER__Semi_Active_Rdr_AAM = (9, WeaponsSu30.R_27ER__Semi_Active_Rdr_AAM)
        R_27ET__IR_AAM = (9, WeaponsSu30.R_27ET__IR_AAM)
        R_77__Active_Rdr_AAM = (9, WeaponsSu30.R_77__Active_Rdr_AAM)
        Kh_31P = (9, WeaponsSu30.Kh_31P)
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
        KAB_500S = (9, WeaponsSu30.KAB_500S)
        KAB_1500t = (9, WeaponsSu30.KAB_1500t)
        KAB_1500LG_Pr = (9, WeaponsSu30.KAB_1500LG_Pr)
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

    class Pylon10:
        R_73__AA_11_Archer____Infra_Red = (10, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_27R__Semi_Active_Rdr_AAM = (10, WeaponsSu30.R_27R__Semi_Active_Rdr_AAM)
        R_27T__IR_AAM = (10, WeaponsSu30.R_27T__IR_AAM)
        R_27ER__Semi_Active_Rdr_AAM = (10, WeaponsSu30.R_27ER__Semi_Active_Rdr_AAM)
        R_27ET__IR_AAM = (10, WeaponsSu30.R_27ET__IR_AAM)
        R_77__Active_Rdr_AAM = (10, WeaponsSu30.R_77__Active_Rdr_AAM)
        Kh_31P = (10, WeaponsSu30.Kh_31P)
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
        KAB_500S = (10, WeaponsSu30.KAB_500S)
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
        _2_x_B_13L___5_S_13_OF = (10, Weapons._2_x_B_13L___5_S_13_OF)
        _2_x_B_8M1___20_S_8KOM = (10, Weapons._2_x_B_8M1___20_S_8KOM)
        _2_x_S_25 = (10, Weapons._2_x_S_25)

    class Pylon11:
        R_73__AA_11_Archer____Infra_Red = (11, Weapons.R_73__AA_11_Archer____Infra_Red)
        Smoke_Generator___red = (11, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (11, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (11, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (11, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (11, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (11, Weapons.Smoke_Generator___orange)

    class Pylon12:
        R_73__AA_11_Archer____Infra_Red = (12, Weapons.R_73__AA_11_Archer____Infra_Red)
        L005_Sorbtsiya_ECM_pod__right_ = (12, Weapons.L005_Sorbtsiya_ECM_pod__right_)
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
        L005_Sorbtsiya_ECM_pod__left_ = (1, Weapons.L005_Sorbtsiya_ECM_pod__left_)
        Smoke_Generator___red = (1, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (1, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (1, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (1, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (1, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (1, Weapons.Smoke_Generator___orange)

    class Pylon2:
        R_73__AA_11_Archer____Infra_Red = (2, Weapons.R_73__AA_11_Archer____Infra_Red)
        Smoke_Generator___red = (2, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (2, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (2, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (2, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (2, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (2, Weapons.Smoke_Generator___orange)

    class Pylon3:
        R_73__AA_11_Archer____Infra_Red = (3, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_27R__Semi_Active_Rdr_AAM = (3, WeaponsSu30.R_27R__Semi_Active_Rdr_AAM)
        R_27T__IR_AAM = (3, WeaponsSu30.R_27T__IR_AAM)
        R_27EA__Active_Rdr_AAM = (3, WeaponsSu30.R_27EA__Active_Rdr_AAM)
        R_27ER__Semi_Active_Rdr_AAM = (3, WeaponsSu30.R_27ER__Semi_Active_Rdr_AAM)
        R_27ET__IR_AAM = (3, WeaponsSu30.R_27ET__IR_AAM)
        R_27EP__Passive_Rdr_AAM = (3, WeaponsSu30.R_27EP__Passive_Rdr_AAM)
        R_77__Active_Rdr_AAM = (3, WeaponsSu30.R_77__Active_Rdr_AAM)
        R_77_1__Active_Rdr_AAM = (3, WeaponsSu30.R_77_1__Active_Rdr_AAM)
        R_77M__Active_Rdr_AAM = (3, WeaponsSu30.R_77M__Active_Rdr_AAM)
        Kh_31P = (3, WeaponsSu30.Kh_31P)
        Kh_36_Grom_1 = (3, WeaponsSu30.Kh_36_Grom_1)
        KH_38MTE = (3, WeaponsSu30.KH_38MTE)
        KH_38MLE = (3, WeaponsSu30.KH_38MLE)
        KH_38MAE = (3, WeaponsSu30.KH_38MAE)
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
        KH_31PD = (3, WeaponsSu30.KH_31PD)
        Kh_59MK2_ = (3, WeaponsSu30.Kh_59MK2_)
        KAB_500Kr___500kg_TV_Guided_Bomb = (3, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S = (3, WeaponsSu30.KAB_500S)
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
        _2_x_B_13L___5_S_13_OF = (3, Weapons._2_x_B_13L___5_S_13_OF)
        _2_x_B_8M1___20_S_8KOM = (3, Weapons._2_x_B_8M1___20_S_8KOM)
        _2_x_S_25 = (3, Weapons._2_x_S_25)

    class Pylon4:
        R_73__AA_11_Archer____Infra_Red = (4, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_27R__Semi_Active_Rdr_AAM = (4, WeaponsSu30.R_27R__Semi_Active_Rdr_AAM)
        R_27T__IR_AAM = (4, WeaponsSu30.R_27T__IR_AAM)
        R_27EA__Active_Rdr_AAM = (4, WeaponsSu30.R_27EA__Active_Rdr_AAM)
        R_27ER__Semi_Active_Rdr_AAM = (4, WeaponsSu30.R_27ER__Semi_Active_Rdr_AAM)
        R_27ET__IR_AAM = (4, WeaponsSu30.R_27ET__IR_AAM)
        R_27EP__Passive_Rdr_AAM = (4, WeaponsSu30.R_27EP__Passive_Rdr_AAM)
        R_77__Active_Rdr_AAM = (4, WeaponsSu30.R_77__Active_Rdr_AAM)
        R_77_1__Active_Rdr_AAM = (4, WeaponsSu30.R_77_1__Active_Rdr_AAM)
        R_77M__Active_Rdr_AAM = (4, WeaponsSu30.R_77M__Active_Rdr_AAM)
        Kh_31P = (4, WeaponsSu30.Kh_31P)
        Kh_36_Grom_1 = (4, WeaponsSu30.Kh_36_Grom_1)
        KH_38MTE = (4, WeaponsSu30.KH_38MTE)
        KH_38MLE = (4, WeaponsSu30.KH_38MLE)
        KH_38MAE = (4, WeaponsSu30.KH_38MAE)
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
        KH_31PD = (4, WeaponsSu30.KH_31PD)
        Kh_59MK2_ = (4, WeaponsSu30.Kh_59MK2_)
        KAB_500Kr___500kg_TV_Guided_Bomb = (4, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S = (4, WeaponsSu30.KAB_500S)
        KAB_1500t = (4, WeaponsSu30.KAB_1500t)
        KAB_1500LG_Pr = (4, WeaponsSu30.KAB_1500LG_Pr)
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            4,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
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

    class Pylon5:
        R_27R__Semi_Active_Rdr_AAM = (5, WeaponsSu30.R_27R__Semi_Active_Rdr_AAM)
        R_27EA__Active_Rdr_AAM = (5, WeaponsSu30.R_27EA__Active_Rdr_AAM)
        R_27ER__Semi_Active_Rdr_AAM = (5, WeaponsSu30.R_27ER__Semi_Active_Rdr_AAM)
        R_27EP__Passive_Rdr_AAM = (5, WeaponsSu30.R_27EP__Passive_Rdr_AAM)
        R_77__Active_Rdr_AAM = (5, WeaponsSu30.R_77__Active_Rdr_AAM)
        R_77_1__Active_Rdr_AAM = (5, WeaponsSu30.R_77_1__Active_Rdr_AAM)
        R_77M__Active_Rdr_AAM = (5, WeaponsSu30.R_77M__Active_Rdr_AAM)
        Kh_31P = (5, WeaponsSu30.Kh_31P)
        Kh_36_Grom_1 = (5, WeaponsSu30.Kh_36_Grom_1)
        KH_38MTE = (5, WeaponsSu30.KH_38MTE)
        KH_38MLE = (5, WeaponsSu30.KH_38MLE)
        KH_38MAE = (5, WeaponsSu30.KH_38MAE)
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
        KH_31PD = (5, WeaponsSu30.KH_31PD)
        KAB_500Kr___500kg_TV_Guided_Bomb = (5, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S = (5, WeaponsSu30.KAB_500S)
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

    class Pylon6:
        R_27R__Semi_Active_Rdr_AAM = (6, WeaponsSu30.R_27R__Semi_Active_Rdr_AAM)
        R_27EA__Active_Rdr_AAM = (6, WeaponsSu30.R_27EA__Active_Rdr_AAM)
        R_27ER__Semi_Active_Rdr_AAM = (6, WeaponsSu30.R_27ER__Semi_Active_Rdr_AAM)
        R_77__Active_Rdr_AAM = (6, WeaponsSu30.R_77__Active_Rdr_AAM)
        R_77_1__Active_Rdr_AAM = (6, WeaponsSu30.R_77_1__Active_Rdr_AAM)
        R_77M__Active_Rdr_AAM = (6, WeaponsSu30.R_77M__Active_Rdr_AAM)
        KAB_500Kr___500kg_TV_Guided_Bomb = (6, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S = (6, WeaponsSu30.KAB_500S)
        KAB_1500t = (6, WeaponsSu30.KAB_1500t)
        KAB_1500LG_Pr = (6, WeaponsSu30.KAB_1500LG_Pr)
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

    class Pylon7:
        R_27R__Semi_Active_Rdr_AAM = (7, WeaponsSu30.R_27R__Semi_Active_Rdr_AAM)
        R_27EA__Active_Rdr_AAM = (7, WeaponsSu30.R_27EA__Active_Rdr_AAM)
        R_27ER__Semi_Active_Rdr_AAM = (7, WeaponsSu30.R_27ER__Semi_Active_Rdr_AAM)
        R_77__Active_Rdr_AAM = (7, WeaponsSu30.R_77__Active_Rdr_AAM)
        R_77_1__Active_Rdr_AAM = (7, WeaponsSu30.R_77_1__Active_Rdr_AAM)
        R_77M__Active_Rdr_AAM = (7, WeaponsSu30.R_77M__Active_Rdr_AAM)
        KAB_500Kr___500kg_TV_Guided_Bomb = (7, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S = (7, WeaponsSu30.KAB_500S)
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

    class Pylon8:
        R_27R__Semi_Active_Rdr_AAM = (8, WeaponsSu30.R_27R__Semi_Active_Rdr_AAM)
        R_27EA__Active_Rdr_AAM = (8, WeaponsSu30.R_27EA__Active_Rdr_AAM)
        R_27ER__Semi_Active_Rdr_AAM = (8, WeaponsSu30.R_27ER__Semi_Active_Rdr_AAM)
        R_27EP__Passive_Rdr_AAM = (8, WeaponsSu30.R_27EP__Passive_Rdr_AAM)
        R_77__Active_Rdr_AAM = (8, WeaponsSu30.R_77__Active_Rdr_AAM)
        R_77_1__Active_Rdr_AAM = (8, WeaponsSu30.R_77_1__Active_Rdr_AAM)
        R_77M__Active_Rdr_AAM = (8, WeaponsSu30.R_77M__Active_Rdr_AAM)
        Kh_31P = (8, WeaponsSu30.Kh_31P)
        Kh_36_Grom_1 = (8, WeaponsSu30.Kh_36_Grom_1)
        KH_38MTE = (8, WeaponsSu30.KH_38MTE)
        KH_38MLE = (8, WeaponsSu30.KH_38MLE)
        KH_38MAE = (8, WeaponsSu30.KH_38MAE)
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
        KH_31PD = (8, WeaponsSu30.KH_31PD)
        KAB_500Kr___500kg_TV_Guided_Bomb = (8, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S = (8, WeaponsSu30.KAB_500S)
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
        DAMOCLES___Targeting_Pod = (8, WeaponsSu30.DAMOCLES___Targeting_Pod)

    class Pylon9:
        R_73__AA_11_Archer____Infra_Red = (9, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_27R__Semi_Active_Rdr_AAM = (9, WeaponsSu30.R_27R__Semi_Active_Rdr_AAM)
        R_27T__IR_AAM = (9, WeaponsSu30.R_27T__IR_AAM)
        R_27EA__Active_Rdr_AAM = (9, WeaponsSu30.R_27EA__Active_Rdr_AAM)
        R_27ER__Semi_Active_Rdr_AAM = (9, WeaponsSu30.R_27ER__Semi_Active_Rdr_AAM)
        R_27ET__IR_AAM = (9, WeaponsSu30.R_27ET__IR_AAM)
        R_27EP__Passive_Rdr_AAM = (9, WeaponsSu30.R_27EP__Passive_Rdr_AAM)
        R_77__Active_Rdr_AAM = (9, WeaponsSu30.R_77__Active_Rdr_AAM)
        R_77_1__Active_Rdr_AAM = (9, WeaponsSu30.R_77_1__Active_Rdr_AAM)
        R_77M__Active_Rdr_AAM = (9, WeaponsSu30.R_77M__Active_Rdr_AAM)
        Kh_31P = (9, WeaponsSu30.Kh_31P)
        Kh_36_Grom_1 = (9, WeaponsSu30.Kh_36_Grom_1)
        KH_38MTE = (9, WeaponsSu30.KH_38MTE)
        KH_38MLE = (9, WeaponsSu30.KH_38MLE)
        KH_38MAE = (9, WeaponsSu30.KH_38MAE)
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
        KH_31PD = (9, WeaponsSu30.KH_31PD)
        Kh_59MK2_ = (9, WeaponsSu30.Kh_59MK2_)
        KAB_500Kr___500kg_TV_Guided_Bomb = (9, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S = (9, WeaponsSu30.KAB_500S)
        KAB_1500t = (9, WeaponsSu30.KAB_1500t)
        KAB_1500LG_Pr = (9, WeaponsSu30.KAB_1500LG_Pr)
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

    class Pylon10:
        R_73__AA_11_Archer____Infra_Red = (10, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_27R__Semi_Active_Rdr_AAM = (10, WeaponsSu30.R_27R__Semi_Active_Rdr_AAM)
        R_27T__IR_AAM = (10, WeaponsSu30.R_27T__IR_AAM)
        R_27EA__Active_Rdr_AAM = (10, WeaponsSu30.R_27EA__Active_Rdr_AAM)
        R_27ER__Semi_Active_Rdr_AAM = (10, WeaponsSu30.R_27ER__Semi_Active_Rdr_AAM)
        R_27ET__IR_AAM = (10, WeaponsSu30.R_27ET__IR_AAM)
        R_27EP__Passive_Rdr_AAM = (10, WeaponsSu30.R_27EP__Passive_Rdr_AAM)
        R_77__Active_Rdr_AAM = (10, WeaponsSu30.R_77__Active_Rdr_AAM)
        R_77_1__Active_Rdr_AAM = (10, WeaponsSu30.R_77_1__Active_Rdr_AAM)
        R_77M__Active_Rdr_AAM = (10, WeaponsSu30.R_77M__Active_Rdr_AAM)
        Kh_31P = (10, WeaponsSu30.Kh_31P)
        Kh_36_Grom_1 = (10, WeaponsSu30.Kh_36_Grom_1)
        KH_38MTE = (10, WeaponsSu30.KH_38MTE)
        KH_38MLE = (10, WeaponsSu30.KH_38MLE)
        KH_38MAE = (10, WeaponsSu30.KH_38MAE)
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
        KH_31PD = (10, WeaponsSu30.KH_31PD)
        Kh_59MK2_ = (10, WeaponsSu30.Kh_59MK2_)
        KAB_500Kr___500kg_TV_Guided_Bomb = (
            10,
            Weapons.KAB_500Kr___500kg_TV_Guided_Bomb,
        )
        KAB_500S = (10, WeaponsSu30.KAB_500S)
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
        _2_x_B_13L___5_S_13_OF = (10, Weapons._2_x_B_13L___5_S_13_OF)
        _2_x_B_8M1___20_S_8KOM = (10, Weapons._2_x_B_8M1___20_S_8KOM)
        _2_x_S_25 = (10, Weapons._2_x_S_25)

    class Pylon11:
        R_73__AA_11_Archer____Infra_Red = (11, Weapons.R_73__AA_11_Archer____Infra_Red)
        Smoke_Generator___red = (11, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (11, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (11, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (11, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (11, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (11, Weapons.Smoke_Generator___orange)

    class Pylon12:
        R_73__AA_11_Archer____Infra_Red = (12, Weapons.R_73__AA_11_Archer____Infra_Red)
        L005_Sorbtsiya_ECM_pod__right_ = (12, Weapons.L005_Sorbtsiya_ECM_pod__right_)
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
