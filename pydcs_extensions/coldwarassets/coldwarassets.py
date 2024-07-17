# Requires Cold War assets mod (ex Tu-16) v1.0 by tripod3:
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
    FAB_3000_M54 = {"clsid": "{FAB_3000_tu_22}", "name": "FAB-3000 M54", "weight": 9400}
    FAB_9000_M54 = {"clsid": "{FAB_9000_tu_22}", "name": "FAB-9000 M54", "weight": 9400}
    GAM_63_RASCAL = {
        "clsid": "{B_29_RASCALARM}",
        "name": "GAM-63 RASCAL",
        "weight": 2400,
    }
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
    KSR_2_086__Passive_seeker_ = {
        "clsid": "{TU_16_KSR2ARM}",
        "name": "KSR-2.086 (Passive seeker)",
        "weight": 1450,
    }
    KSR_5 = {"clsid": "{TU_16_KSR5}", "name": "KSR-5", "weight": 1450}
    KS_1 = {"clsid": "{Tu4_KS_1}", "name": "KS-1", "weight": 1160}
    KS_1_late = {"clsid": "{Tu16_KS_1}", "name": "KS-1 late", "weight": 1160}


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

    pylons: Set[int] = {1}

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
        KSR5P__Passive_seeker_ = (1, WeaponsColdWarAssets.KSR5P__Passive_seeker_)
        KSR_5 = (1, WeaponsColdWarAssets.KSR_5)

    class Pylon2:
        FAB_3000_M54 = (2, WeaponsColdWarAssets.FAB_3000_M54)
        FAB_9000_M54 = (2, WeaponsColdWarAssets.FAB_9000_M54)

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
