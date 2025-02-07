# Requires Cold War assets mod (ex Tu-16) v1.2 by tripod3:
# https://forum.dcs.world/topic/350021-cold-war-assets-mod-ex-tu-16-v-10/
#
from typing import Any, Dict, Set

from dcs import task
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

from game.modsupport import planemod
from pydcs_extensions.weapon_injector import inject_weapons


class WeaponsColdWarAssets:
    B29_AN_M57_10 = {
        "clsid": "B29_AN_M57_10",
        "name": "10 x AN-M57 - 250lb GP Bombs LD",
        "weight": 1185.462692,
    }
    B29_AN_M57_20 = {
        "clsid": "B29_AN_M57_20",
        "name": "20 x AN-M57 - 250lb GP Bombs LD",
        "weight": 2370.925384,
    }
    B29_AN_M64_4 = {
        "clsid": "B29_AN_M64_4",
        "name": "4 x AN-M64 - 500lb GP Bombs LD",
        "weight": 995.52557792,
    }
    B29_AN_M64_5 = {
        "clsid": "B29_AN_M64_5",
        "name": "5 x AN-M64 - 500lb GP Bombs LD",
        "weight": 1244.4069724,
    }
    B29_AN_M64_6 = {
        "clsid": "B29_AN_M64_6",
        "name": "6 x AN-M64 - 500lb GP Bombs LD",
        "weight": 1493.28836688,
    }
    B29_AN_M64_8 = {
        "clsid": "B29_AN_M64_8",
        "name": "8 x AN-M64 - 500lb GP Bombs LD",
        "weight": 1991.05115584,
    }
    B29_AN_M65_2 = {
        "clsid": "B29_AN_M65_2",
        "name": "2 x AN-M65 - 1000lb GP Bombs LD",
        "weight": 965.243776,
    }
    B29_AN_M65_3 = {
        "clsid": "B29_AN_M65_3",
        "name": "3 x AN-M65 - 1000lb GP Bombs LD",
        "weight": 1447.865664,
    }
    B29_AN_M65_4 = {
        "clsid": "B29_AN_M65_4",
        "name": "4 x AN-M65 - 1000lb GP Bombs LD",
        "weight": 1930.487552,
    }
    B29_AN_M65_6 = {
        "clsid": "B29_AN_M65_6",
        "name": "6 x AN-M65 - 1000lb GP Bombs LD",
        "weight": 2895.731328,
    }
    B29_AN_M66_1 = {
        "clsid": "B29_AN_M66_1",
        "name": "1 x AN-M66 - 2000lb GP Bombs LD",
        "weight": 958.5306144,
    }
    B29_AN_M66_2 = {
        "clsid": "B29_AN_M66_2",
        "name": "2 x AN-M66 - 2000lb GP Bombs LD",
        "weight": 1917.0612288,
    }
    B29_M19_10 = {
        "clsid": "B29_M19_10",
        "name": "10 x M19 - 38 x AN-M69, 500lb CBU with incendiary submunitions",
        "weight": 1973.1252,
    }
    B29_M19_6 = {
        "clsid": "B29_M19_6",
        "name": "6 x M19 - 38 x AN-M69, 500lb CBU with incendiary submunitions",
        "weight": 1183.87512,
    }
    B_43 = {"clsid": "{B_43_B_58}", "name": "B-43", "weight": 9400}
    Mk_53 = {"clsid": "{Mk_53_1}", "name": "Mk.53", "weight": 5000}
    W_53_H_Bomb_with_fuel_tank = {
        "clsid": "{W_53_B_58}",
        "name": "W-53 H-Bomb with fuel tank",
        "weight": 4000,
    }
    Fuel_10940_kg = {"clsid": "{LeBaque_B_58}", "name": "Fuel 10940 kg", "weight": 37}
    FAB_3000_M54 = {"clsid": "{FAB_3000_tu_22}", "name": "FAB-3000 M54", "weight": 9400}
    FAB_9000_M54 = {"clsid": "{FAB_9000_tu_22}", "name": "FAB-9000 M54", "weight": 9400}
    GAM_63_RASCAL = {
        "clsid": "{B_29_RASCALARM}",
        "name": "GAM-63 RASCAL",
        "weight": 2400,
    }
    Kh_20 = {"clsid": "{Kh_20_Tu_95K}", "name": "Kh-20", "weight": 2400}
    Kh_22MA = {"clsid": "{Tu_22_Kh22PSI}", "name": "Kh-22MA", "weight": 2400}
    Kh_22P__Passive_seeker_ = {
        "clsid": "{TU_22_KH22P}",
        "name": "Kh-22P (Passive seeker)",
        "weight": 1450,
    }
    KSR5P__Passive_seeker_ = {
        "clsid": "{TU_16_KSR5ARM}",
        "name": "KSR5P (Passive seeker)",
        "weight": 1450,
    }
    KSR_2 = {"clsid": "{TU_16_KSR2}", "name": "KSR-2", "weight": 1160}
    KSR_2D_decoy_missile = {
        "clsid": "{TU_16_KSR2d}",
        "name": "KSR-2D decoy missile",
        "weight": 1160,
    }
    KSR_2_086__Passive_seeker_ = {
        "clsid": "{TU_16_KSR2ARM}",
        "name": "KSR-2.086 (Passive seeker)",
        "weight": 1450,
    }
    KSR_5 = {"clsid": "{TU_16_KSR5}", "name": "KSR-5", "weight": 1450}
    KS_1 = {"clsid": "{Tu4_KS_1}", "name": "KS-1", "weight": 1160}
    KS_1_late = {"clsid": "{Tu16_KS_1}", "name": "KS-1 late", "weight": 1160}
    RDS_37 = {"clsid": "{RDS37_1}", "name": "RDS-37", "weight": 5500}
    R_4RM = {"clsid": "{R-8M1R}", "name": "R-4RM", "weight": 385}
    R_4TM = {"clsid": "{R-8M1T}", "name": "R-4TM", "weight": 265}
    R_8M1R_Yak_28 = {"clsid": "{R-8M1R_Yak_28}", "name": "R-8M1R", "weight": 285}
    R_8M1T_Yak_28 = {"clsid": "{R-8M1T_Yak_28}", "name": "R-8M1T", "weight": 265}
    R_98MR_Yak_28 = {"clsid": "{R-98MR_Yak_28}", "name": "R-98MR", "weight": 292}
    R_98MT_Yak_28 = {"clsid": "{R-98MT_Yak_28}", "name": "R-98MT", "weight": 272}


inject_weapons(WeaponsColdWarAssets)


@planemod
class B_47(PlaneType):
    id = "B_47"
    height = 10.36
    width = 33
    length = 34.8
    fuel_max = 25000
    max_speed = 1044
    chaff = 120
    flare = 120
    charge_total = 240
    chaff_charge_size = 1
    flare_charge_size = 1
    eplrs = True

    property_defaults: Dict[str, Any] = {}

    livery_name = "B_47"  # from type

    class Pylon1:
        GAM_63_RASCAL = (1, WeaponsColdWarAssets.GAM_63_RASCAL)

    class Pylon2:
        Mk_53 = (2, WeaponsColdWarAssets.Mk_53)
        # ERRR {72CAC282-AE18-490B-BD4D-35E7EE969E73}
        # ERRR {B84DFE16-6AC7-4854-8F6D-34137892E166}
        Mk_84_28 = (2, Weapons.Mk_84_28)
        # ERRR {F092B80C-BB54-477E-9408-66DEEF740008}
        # ERRR {574EDEDF-20DE-4942-B2A2-B2EDFD621562}

    pylons: Set[int] = {1, 2}

    tasks = [
        task.AntishipStrike,
        task.GroundAttack,
        task.PinpointStrike,
        task.RunwayAttack,
        task.SEAD,
        task.CAS,
        task.Reconnaissance,
    ]

    task_default = task.AntishipStrike


@planemod
class B_58(PlaneType):
    id = "B_58"
    height = 10.13
    width = 23.17
    length = 41.6
    fuel_max = 22500
    max_speed = 2121.84
    chaff = 45
    flare = -0
    charge_total = 45
    chaff_charge_size = 1
    flare_charge_size = 1

    livery_name = "B_58"  # from type

    class Pylon1:
        B_43 = (1, WeaponsColdWarAssets.B_43)
        Mk_84___2000lb_GP_Bomb_LD = (1, Weapons.Mk_84___2000lb_GP_Bomb_LD)

    class Pylon2:
        B_43 = (2, WeaponsColdWarAssets.B_43)
        Mk_84___2000lb_GP_Bomb_LD = (2, Weapons.Mk_84___2000lb_GP_Bomb_LD)

    class Pylon3:
        B_43 = (3, WeaponsColdWarAssets.B_43)
        Mk_84___2000lb_GP_Bomb_LD = (3, Weapons.Mk_84___2000lb_GP_Bomb_LD)

    class Pylon4:
        B_43 = (4, WeaponsColdWarAssets.B_43)
        Mk_84___2000lb_GP_Bomb_LD = (4, Weapons.Mk_84___2000lb_GP_Bomb_LD)

    class Pylon5:
        W_53_H_Bomb_with_fuel_tank = (
            5,
            WeaponsColdWarAssets.W_53_H_Bomb_with_fuel_tank,
        )

    pylons: Set[int] = {1, 2, 3, 4, 5}

    tasks = [
        task.Reconnaissance,
        task.GroundAttack,
        task.CAS,
        task.RunwayAttack,
        task.AntishipStrike,
        task.PinpointStrike,
    ]
    task_default = task.GroundAttack


@planemod
class Tu_4K(PlaneType):
    id = "Tu-4K"
    height = 8.46
    width = 43.1
    length = 30.18
    fuel_max = 22371
    max_speed = 558
    radio_frequency = 127.5

    property_defaults: Dict[str, Any] = {
        "Belly_Bay_Door": False,
    }

    class Properties:
        class Belly_Bay_Door:
            id = "Belly Bay Door"

    livery_name = "TU-4K"  # from type

    class Pylon1:
        KS_1 = (1, WeaponsColdWarAssets.KS_1)

    class Pylon2:
        KS_1 = (2, WeaponsColdWarAssets.KS_1)

    pylons: Set[int] = {1, 2}

    tasks = [task.GroundAttack, task.RunwayAttack, task.AntishipStrike]
    task_default = task.RunwayAttack


@planemod
class Tu_16(PlaneType):
    id = "Tu-16"
    height = 10.36
    width = 33
    length = 34.8
    fuel_max = 25000
    max_speed = 1044
    chaff = 120
    flare = 120
    charge_total = 240
    chaff_charge_size = 1
    flare_charge_size = 1
    eplrs = True

    property_defaults: Dict[str, Any] = {}

    livery_name = "TU-16"  # from type

    class Pylon1:
        KS_1_late = (1, WeaponsColdWarAssets.KS_1_late)
        KSR_2 = (1, WeaponsColdWarAssets.KSR_2)
        KSR_2_086__Passive_seeker_ = (
            1,
            WeaponsColdWarAssets.KSR_2_086__Passive_seeker_,
        )
        KSR_2D_decoy_missile = (1, WeaponsColdWarAssets.KSR_2D_decoy_missile)
        KSR5P__Passive_seeker_ = (1, WeaponsColdWarAssets.KSR5P__Passive_seeker_)
        KSR_5 = (1, WeaponsColdWarAssets.KSR_5)

    class Pylon2:
        FAB_3000_M54 = (2, WeaponsColdWarAssets.FAB_3000_M54)
        FAB_9000_M54 = (2, WeaponsColdWarAssets.FAB_9000_M54)
        RDS_37 = (2, WeaponsColdWarAssets.RDS_37)

    # ERRR <CLEAN>

    class Pylon3:
        _33_x_FAB_250___250kg_GP_Bombs_LD = (
            3,
            Weapons._33_x_FAB_250___250kg_GP_Bombs_LD,
        )

    # ERRR <CLEAN>

    class Pylon4:
        KS_1_late = (4, WeaponsColdWarAssets.KS_1_late)
        KSR_2 = (4, WeaponsColdWarAssets.KSR_2)
        KSR_2_086__Passive_seeker_ = (
            4,
            WeaponsColdWarAssets.KSR_2_086__Passive_seeker_,
        )
        KSR_2D_decoy_missile = (4, WeaponsColdWarAssets.KSR_2D_decoy_missile)
        KSR5P__Passive_seeker_ = (4, WeaponsColdWarAssets.KSR5P__Passive_seeker_)
        KSR_5 = (4, WeaponsColdWarAssets.KSR_5)

    pylons: Set[int] = {1, 2, 3, 4}

    tasks = [
        task.AntishipStrike,
        task.GroundAttack,
        task.PinpointStrike,
        task.RunwayAttack,
        task.SEAD,
        task.CAS,
    ]
    task_default = task.AntishipStrike


@planemod
class Tu_95K(PlaneType):
    id = "Tu_95K"
    large_parking_slot = True
    height = 13.3
    width = 50.04
    length = 49.13
    fuel_max = 87000
    max_speed = 919.8
    chaff = 48
    flare = 48
    charge_total = 96
    chaff_charge_size = 1
    flare_charge_size = 1
    eplrs = True

    property_defaults: Dict[str, Any] = {}

    livery_name = "TU_95K"  # from type

    class Pylon1:
        Kh_20 = (1, WeaponsColdWarAssets.Kh_20)

    pylons: Set[int] = {1}

    tasks = [
        task.Reconnaissance,
        task.GroundAttack,
        task.CAS,
        task.AFAC,
        task.RunwayAttack,
        task.AntishipStrike,
        task.PinpointStrike,
        task.SEAD,
    ]
    task_default = task.GroundAttack


@planemod
class tu_22D(PlaneType):
    id = "tu_22D"
    height = 10.13
    width = 23.17
    length = 41.6
    fuel_max = 42500
    max_speed = 1509.84
    chaff = 45
    flare = -0
    charge_total = 45
    chaff_charge_size = 1
    flare_charge_size = 1

    livery_name = "TU_22D"  # from type

    class Pylon1:
        FAB_3000_M54 = (1, WeaponsColdWarAssets.FAB_3000_M54)
        FAB_9000_M54 = (1, WeaponsColdWarAssets.FAB_9000_M54)
        _6_x_FAB_1500_M_54___1500kg_GP_Bombs_LD = (
            1,
            Weapons._6_x_FAB_1500_M_54___1500kg_GP_Bombs_LD,
        )
        MBD3_U2T_with_2_x_FAB_1500_M_54___1500kg_GP_Bombs_LD = (
            1,
            Weapons.MBD3_U2T_with_2_x_FAB_1500_M_54___1500kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_6_x_FAB_500_M_62___500kg_GP_Bombs_LD = (
            1,
            Weapons.MBD3_U6_68_with_6_x_FAB_500_M_62___500kg_GP_Bombs_LD,
        )
        RN_24___470kg__nuclear_bomb__free_fall = (
            1,
            Weapons.RN_24___470kg__nuclear_bomb__free_fall,
        )
        RN_28___260_kg__nuclear_bomb__free_fall = (
            1,
            Weapons.RN_28___260_kg__nuclear_bomb__free_fall,
        )
        RDS_37 = (1, WeaponsColdWarAssets.RDS_37)

    # ERRR <CLEAN>

    class Pylon2:
        _33_x_FAB_250___250kg_GP_Bombs_LD = (
            2,
            Weapons._33_x_FAB_250___250kg_GP_Bombs_LD,
        )

    # ERRR <CLEAN>

    pylons: Set[int] = {1, 2}

    tasks = [
        task.Reconnaissance,
        task.GroundAttack,
        task.CAS,
        task.RunwayAttack,
        task.AntishipStrike,
        task.PinpointStrike,
    ]
    task_default = task.GroundAttack


@planemod
class tu_22KD(PlaneType):
    id = "tu_22KD"
    height = 10.13
    width = 23.17
    length = 41.6
    fuel_max = 42500
    max_speed = 1509.84
    chaff = 45
    flare = -0
    charge_total = 45
    chaff_charge_size = 1
    flare_charge_size = 1

    livery_name = "TU_22KD"  # from type

    class Pylon1:
        Kh_22__AS_4_Kitchen____1000kg__AShM__IN__Act_Pas_Rdr = (
            1,
            Weapons.Kh_22__AS_4_Kitchen____1000kg__AShM__IN__Act_Pas_Rdr,
        )
        Kh_22MA = (1, WeaponsColdWarAssets.Kh_22MA)
        Kh_22P__Passive_seeker_ = (1, WeaponsColdWarAssets.Kh_22P__Passive_seeker_)

    class Pylon2:
        FAB_3000_M54 = (2, WeaponsColdWarAssets.FAB_3000_M54)
        FAB_9000_M54 = (2, WeaponsColdWarAssets.FAB_9000_M54)
        _6_x_FAB_1500_M_54___1500kg_GP_Bombs_LD = (
            2,
            Weapons._6_x_FAB_1500_M_54___1500kg_GP_Bombs_LD,
        )
        MBD3_U2T_with_2_x_FAB_1500_M_54___1500kg_GP_Bombs_LD = (
            2,
            Weapons.MBD3_U2T_with_2_x_FAB_1500_M_54___1500kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_6_x_FAB_500_M_62___500kg_GP_Bombs_LD = (
            2,
            Weapons.MBD3_U6_68_with_6_x_FAB_500_M_62___500kg_GP_Bombs_LD,
        )
        RDS_37 = (1, WeaponsColdWarAssets.RDS_37)

    # ERRR <CLEAN>

    class Pylon3:
        _33_x_FAB_250___250kg_GP_Bombs_LD = (
            3,
            Weapons._33_x_FAB_250___250kg_GP_Bombs_LD,
        )

    # ERRR <CLEAN>

    pylons: Set[int] = {1, 2, 3}

    tasks = [
        task.Reconnaissance,
        task.GroundAttack,
        task.CAS,
        task.RunwayAttack,
        task.AntishipStrike,
        task.PinpointStrike,
        task.SEAD,
    ]
    task_default = task.GroundAttack


@planemod
class Yak_28(PlaneType):
    id = "Yak_28"
    height = 5
    width = 9.34
    length = 18
    fuel_max = 5600
    max_speed = 2229.984
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    livery_name = "YAK_28"  # from type

    class Pylon1:
        APU_13U_2_with_R_3S__AA_2_Atoll_B____IR_AAM = (
            1,
            Weapons.APU_13U_2_with_R_3S__AA_2_Atoll_B____IR_AAM,
        )
        R_8M1R = (1, WeaponsColdWarAssets.R_8M1R_Yak_28)
        R_8M1T = (1, WeaponsColdWarAssets.R_8M1T_Yak_28)
        R_98MT = (1, WeaponsColdWarAssets.R_98MT_Yak_28)
        R_98MR = (1, WeaponsColdWarAssets.R_98MR_Yak_28)

    class Pylon2:
        APU_13U_2_with_R_3S__AA_2_Atoll_B____IR_AAM = (
            2,
            Weapons.APU_13U_2_with_R_3S__AA_2_Atoll_B____IR_AAM,
        )
        R_8M1R = (2, WeaponsColdWarAssets.R_8M1R_Yak_28)
        R_8M1T = (2, WeaponsColdWarAssets.R_8M1T_Yak_28)
        R_98MT = (2, WeaponsColdWarAssets.R_98MT_Yak_28)
        R_98MR = (2, WeaponsColdWarAssets.R_98MR_Yak_28)
        ORO_57K___S_5M_x_8 = (2, Weapons.ORO_57K___S_5M_x_8)

    class Pylon3:
        RN_24___470kg__nuclear_bomb__free_fall = (
            3,
            Weapons.RN_24___470kg__nuclear_bomb__free_fall,
        )
        RN_28___260_kg__nuclear_bomb__free_fall = (
            3,
            Weapons.RN_28___260_kg__nuclear_bomb__free_fall,
        )
        FAB_1500_M_54___1500kg_GP_Bomb_LD = (
            3,
            Weapons.FAB_1500_M_54___1500kg_GP_Bomb_LD,
        )
        MBD3_U4T_with_4_x_FAB_250___250kg_GP_Bombs_LD = (
            3,
            Weapons.MBD3_U4T_with_4_x_FAB_250___250kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_3_x_FAB_250___250kg_GP_Bombs_LD = (
            3,
            Weapons.MBD3_U6_68_with_3_x_FAB_250___250kg_GP_Bombs_LD,
        )
        FAB_500_M54_TU___480_kg__bomb__parachute = (
            3,
            Weapons.FAB_500_M54_TU___480_kg__bomb__parachute,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            3,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD = (
            3,
            Weapons.MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD,
        )

    class Pylon4:
        APU_13U_2_with_R_3S__AA_2_Atoll_B____IR_AAM = (
            4,
            Weapons.APU_13U_2_with_R_3S__AA_2_Atoll_B____IR_AAM,
        )
        R_8M1R = (4, WeaponsColdWarAssets.R_8M1R_Yak_28)
        R_8M1T = (4, WeaponsColdWarAssets.R_8M1T_Yak_28)
        R_98MT = (4, WeaponsColdWarAssets.R_98MT_Yak_28)
        R_98MR = (4, WeaponsColdWarAssets.R_98MR_Yak_28)

    class Pylon5:
        APU_13U_2_with_R_3S__AA_2_Atoll_B____IR_AAM = (
            5,
            Weapons.APU_13U_2_with_R_3S__AA_2_Atoll_B____IR_AAM,
        )
        R_8M1R = (5, WeaponsColdWarAssets.R_8M1R_Yak_28)
        R_8M1T = (5, WeaponsColdWarAssets.R_8M1T_Yak_28)
        R_98MT = (5, WeaponsColdWarAssets.R_98MT_Yak_28)
        R_98MR = (5, WeaponsColdWarAssets.R_98MR_Yak_28)
        ORO_57K___S_5M_x_8 = (5, Weapons.ORO_57K___S_5M_x_8)

    pylons: Set[int] = {1, 2, 3, 4, 5}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.GroundAttack,
    ]
    task_default = task.Intercept


@planemod
class Tu_126(PlaneType):
    id = "Tu_126"
    large_parking_slot = True
    height = 13.3
    width = 50.04
    length = 49.13
    fuel_max = 72000
    max_speed = 919.8
    chaff = 48
    flare = 48
    charge_total = 96
    chaff_charge_size = 1
    flare_charge_size = 1
    eplrs = True

    property_defaults: Dict[str, Any] = {}

    livery_name = "TU_126"  # from type

    pylons: Set[int] = set()

    tasks = [task.Reconnaissance, task.AWACS]
    task_default = task.AWACS


@planemod
class Tu_128M(PlaneType):
    id = "Tu_128M"
    height = 7.53
    width = 17.5
    length = 30.06
    fuel_max = 15000
    max_speed = 1908
    chaff = 30
    flare = 15
    charge_total = 60
    chaff_charge_size = 1
    flare_charge_size = 2
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    livery_name = "TU_128M"  # from type

    class Pylon1:
        R_4RM = (1, WeaponsColdWarAssets.R_4RM)
        R_4TM = (1, WeaponsColdWarAssets.R_4TM)

    class Pylon2:
        R_4RM = (2, WeaponsColdWarAssets.R_4RM)
        R_4TM = (2, WeaponsColdWarAssets.R_4TM)

    class Pylon3:
        R_4RM = (3, WeaponsColdWarAssets.R_4RM)
        R_4TM = (3, WeaponsColdWarAssets.R_4TM)

    class Pylon4:
        R_4RM = (4, WeaponsColdWarAssets.R_4RM)
        R_4TM = (4, WeaponsColdWarAssets.R_4TM)

    pylons: Set[int] = {1, 2, 3, 4}

    tasks = [
        task.GroundAttack,
        task.CAS,
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
    ]
    task_default = task.Intercept
