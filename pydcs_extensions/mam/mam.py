from typing import Any, Dict, Set

from dcs import task
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

from game.modsupport import planemod
from pydcs_extensions.weapon_injector import inject_weapons


class WeaponsB2:

    B2_AGM_154C_8 = {
        "clsid": "{B2_AGM-154C*8}",
        "name": "B2 AGM-154C*8",
        "weight": 3872,
    }
    B2_CBU87_18 = {"clsid": "{B2_CBU87*18}", "name": "B2 CBU87*18", "weight": 7740}
    B2_CBU_97_18 = {"clsid": "{B2_CBU97*18}", "name": "B2 CBU-97*18", "weight": 7506}
    B2_GBU_27_4 = {"clsid": "{B2_GBU-27*4}", "name": "B2 GBU-27*4", "weight": 4800}
    B2_GBU_28_4 = {"clsid": "{B2_GBU-28*4}", "name": "B2 GBU-28*4", "weight": 8520}
    B2_GBU_38_40 = {"clsid": "{B2_GBU-38*40}", "name": "B2 GBU-38*40", "weight": 9640}
    B2_Mk_82_40 = {"clsid": "{B2_Mk82*40}", "name": "B2 Mk-82*40", "weight": 9640}


inject_weapons(WeaponsB2)


@planemod
class A400M_Atlas(PlaneType):
    id = "A400M_Atlas"
    height = 11.66
    width = 40.4
    length = 29.79
    fuel_max = 20830
    max_speed = 621
    chaff = 120
    flare = 60
    charge_total = 240
    chaff_charge_size = 1
    flare_charge_size = 2
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    livery_name = "A400M_ATLAS"  # from type

    pylons: Set[int] = set()

    tasks = [task.Transport]
    task_default = task.Transport


@planemod
class B2_Spirit(PlaneType):
    id = "B2_Spirit"
    group_size_max = 1
    height = 10.36
    width = 41.67
    length = 44.81
    fuel_max = 88450
    max_speed = 1329.84
    chaff = 60
    flare = 30
    charge_total = 120
    chaff_charge_size = 1
    flare_charge_size = 2
    eplrs = True
    radio_frequency = 127.5

    livery_name = "B2_SPIRIT"  # from type

    class Pylon1:
        B2_Mk_82_40 = (1, WeaponsB2.B2_Mk_82_40)
        B2_CBU87_18 = (1, WeaponsB2.B2_CBU87_18)
        B2_CBU_97_18 = (1, WeaponsB2.B2_CBU_97_18)
        B2_GBU_38_40 = (1, WeaponsB2.B2_GBU_38_40)
        B2_GBU_28_4 = (1, WeaponsB2.B2_GBU_28_4)
        B2_GBU_27_4 = (1, WeaponsB2.B2_GBU_27_4)
        B2_AGM_154C_8 = (1, WeaponsB2.B2_AGM_154C_8)
        B_1B_Mk_84_8 = (1, Weapons.B_1B_Mk_84_8)

    class Pylon2:
        B2_Mk_82_40 = (2, WeaponsB2.B2_Mk_82_40)
        B2_CBU87_18 = (2, WeaponsB2.B2_CBU87_18)
        B2_CBU_97_18 = (2, WeaponsB2.B2_CBU_97_18)
        B2_GBU_38_40 = (2, WeaponsB2.B2_GBU_38_40)
        B2_GBU_28_4 = (2, WeaponsB2.B2_GBU_28_4)
        B2_GBU_27_4 = (2, WeaponsB2.B2_GBU_27_4)
        B2_AGM_154C_8 = (2, WeaponsB2.B2_AGM_154C_8)
        B_1B_Mk_84_8 = (2, Weapons.B_1B_Mk_84_8)

    pylons: Set[int] = {1, 2}

    tasks = [task.GroundAttack, task.RunwayAttack, task.PinpointStrike, task.CAS]
    task_default = task.GroundAttack


@planemod
class C2A_Greyhound(PlaneType):
    id = "C2A_Greyhound"
    group_size_max = 1
    height = 4.85
    width = 24.6
    length = 17.3
    fuel_max = 5624
    max_speed = 625.68
    chaff = 120
    flare = 60
    charge_total = 240
    chaff_charge_size = 1
    flare_charge_size = 2
    eplrs = True
    radio_frequency = 127.5

    livery_name = "C2A_GREYHOUND"  # from type

    pylons: Set[int] = set()

    tasks = [task.Transport]
    task_default = task.Transport


@planemod
class C5_Galaxy(PlaneType):
    id = "C5_Galaxy"
    group_size_max = 1
    height = 16.79
    width = 60.89
    length = 53.04
    fuel_max = 157768
    max_speed = 856.008
    chaff = 120
    flare = 60
    charge_total = 240
    chaff_charge_size = 1
    flare_charge_size = 2
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    livery_name = "C5_GALAXY"  # from type

    pylons: Set[int] = set()

    tasks = [task.Transport]
    task_default = task.Transport


@planemod
class KC_10_Extender(PlaneType):
    id = "KC_10_Extender"
    group_size_max = 1
    height = 17.7
    width = 50.41
    length = 55.35
    fuel_max = 160200
    max_speed = 996.012
    chaff = 120
    flare = 60
    charge_total = 240
    chaff_charge_size = 1
    flare_charge_size = 2
    tacan = True
    category = "Tankers"  # {8A302789-A55D-4897-B647-66493FA6826F}

    livery_name = "KC_10_EXTENDER"  # from type

    pylons: Set[int] = set()

    tasks = [task.Transport, task.Refueling]
    task_default = task.Refueling


@planemod
class KC_10_Extender_D(PlaneType):
    id = "KC_10_Extender_D"
    group_size_max = 1
    height = 17.7
    width = 50.41
    length = 55.35
    fuel_max = 154000
    max_speed = 804.996
    chaff = 120
    flare = 60
    charge_total = 240
    chaff_charge_size = 1
    flare_charge_size = 2
    tacan = True
    category = "Tankers"  # {8A302789-A55D-4897-B647-66493FA6826F}

    livery_name = "KC_10_EXTENDER_D"  # from type

    pylons: Set[int] = set()

    tasks = [task.Transport, task.Refueling]
    task_default = task.Refueling


@planemod
class P3C_Orion(PlaneType):
    id = "P3C_Orion"
    group_size_max = 1
    height = 10.27
    width = 30.37
    length = 35.61
    fuel_max = 28350
    max_speed = 1479.6
    chaff = 120
    flare = 60
    charge_total = 240
    chaff_charge_size = 1
    flare_charge_size = 2
    eplrs = True
    radio_frequency = 127.5

    livery_name = "P3C_ORION"  # from type

    class Pylon1:
        Smokewinder___red = (1, Weapons.Smokewinder___red)
        Smokewinder___green = (1, Weapons.Smokewinder___green)
        Smokewinder___blue = (1, Weapons.Smokewinder___blue)
        Smokewinder___white = (1, Weapons.Smokewinder___white)
        Smokewinder___yellow = (1, Weapons.Smokewinder___yellow)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (1, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        LAU_115_LAU_127_AIM_9L = (1, Weapons.LAU_115_LAU_127_AIM_9L)
        Mk_82___500lb_GP_Bomb_LD = (1, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            1,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        AGM_84D_Harpoon_AShM = (1, Weapons.AGM_84D_Harpoon_AShM)
        LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE = (
            1,
            Weapons.LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE,
        )

    class Pylon2:
        LAU_115_LAU_127_AIM_9L = (2, Weapons.LAU_115_LAU_127_AIM_9L)
        Mk_82___500lb_GP_Bomb_LD = (2, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            2,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        MER2_with_2_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets = (
            2,
            Weapons.MER2_with_2_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets,
        )
        AGM_84D_Harpoon_AShM = (2, Weapons.AGM_84D_Harpoon_AShM)
        AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            2,
            Weapons.AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            2,
            Weapons.LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        LAU_117_AGM_65F = (2, Weapons.LAU_117_AGM_65F)
        LAU_117_AGM_65G = (2, Weapons.LAU_117_AGM_65G)
        LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE = (
            2,
            Weapons.LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE,
        )
        LTF_5b_Aerial_Torpedo = (2, Weapons.LTF_5b_Aerial_Torpedo)

    class Pylon3:
        Mk_82___500lb_GP_Bomb_LD = (3, Weapons.Mk_82___500lb_GP_Bomb_LD)
        BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD = (
            3,
            Weapons.BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            3,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        MER2_with_2_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets = (
            3,
            Weapons.MER2_with_2_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets,
        )
        AGM_84D_Harpoon_AShM = (3, Weapons.AGM_84D_Harpoon_AShM)
        AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            3,
            Weapons.AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            3,
            Weapons.LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        LAU_117_AGM_65F = (3, Weapons.LAU_117_AGM_65F)
        LAU_117_AGM_65G = (3, Weapons.LAU_117_AGM_65G)
        LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE = (
            3,
            Weapons.LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE,
        )
        LTF_5b_Aerial_Torpedo = (3, Weapons.LTF_5b_Aerial_Torpedo)

    class Pylon4:
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            4,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        Mk_82___500lb_GP_Bomb_LD = (4, Weapons.Mk_82___500lb_GP_Bomb_LD)

    class Pylon5:
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            5,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        Mk_82___500lb_GP_Bomb_LD = (5, Weapons.Mk_82___500lb_GP_Bomb_LD)
        LTF_5b_Aerial_Torpedo = (5, Weapons.LTF_5b_Aerial_Torpedo)

    class Pylon6:
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            6,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        Mk_82___500lb_GP_Bomb_LD = (6, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_83___1000lb_GP_Bomb_LD = (6, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        LTF_5b_Aerial_Torpedo = (6, Weapons.LTF_5b_Aerial_Torpedo)

    class Pylon7:
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            7,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        Mk_82___500lb_GP_Bomb_LD = (7, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_83___1000lb_GP_Bomb_LD = (7, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        LTF_5b_Aerial_Torpedo = (7, Weapons.LTF_5b_Aerial_Torpedo)

    class Pylon8:
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            8,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        Mk_82___500lb_GP_Bomb_LD = (8, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_83___1000lb_GP_Bomb_LD = (8, Weapons.Mk_83___1000lb_GP_Bomb_LD)

    class Pylon9:
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            9,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        Mk_82___500lb_GP_Bomb_LD = (9, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_83___1000lb_GP_Bomb_LD = (9, Weapons.Mk_83___1000lb_GP_Bomb_LD)

    class Pylon10:
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            10,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        Mk_82___500lb_GP_Bomb_LD = (10, Weapons.Mk_82___500lb_GP_Bomb_LD)

    class Pylon11:
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            11,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        Mk_82___500lb_GP_Bomb_LD = (11, Weapons.Mk_82___500lb_GP_Bomb_LD)

    class Pylon12:
        Mk_82___500lb_GP_Bomb_LD = (12, Weapons.Mk_82___500lb_GP_Bomb_LD)
        BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD = (
            12,
            Weapons.BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            12,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        MER2_with_2_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets = (
            12,
            Weapons.MER2_with_2_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets,
        )
        AGM_84D_Harpoon_AShM = (12, Weapons.AGM_84D_Harpoon_AShM)
        AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            12,
            Weapons.AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            12,
            Weapons.LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        LAU_117_AGM_65F = (12, Weapons.LAU_117_AGM_65F)
        LAU_117_AGM_65G = (12, Weapons.LAU_117_AGM_65G)
        LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE = (
            12,
            Weapons.LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE,
        )
        LTF_5b_Aerial_Torpedo = (12, Weapons.LTF_5b_Aerial_Torpedo)

    class Pylon13:
        LAU_115_LAU_127_AIM_9L = (13, Weapons.LAU_115_LAU_127_AIM_9L)
        Mk_82___500lb_GP_Bomb_LD = (13, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            13,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        MER2_with_2_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets = (
            13,
            Weapons.MER2_with_2_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets,
        )
        AGM_84D_Harpoon_AShM = (13, Weapons.AGM_84D_Harpoon_AShM)
        AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            13,
            Weapons.AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            13,
            Weapons.LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        LAU_117_AGM_65F = (13, Weapons.LAU_117_AGM_65F)
        LAU_117_AGM_65G = (13, Weapons.LAU_117_AGM_65G)
        LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE = (
            13,
            Weapons.LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE,
        )

    class Pylon14:
        Smokewinder___red = (14, Weapons.Smokewinder___red)
        Smokewinder___green = (14, Weapons.Smokewinder___green)
        Smokewinder___blue = (14, Weapons.Smokewinder___blue)
        Smokewinder___white = (14, Weapons.Smokewinder___white)
        Smokewinder___yellow = (14, Weapons.Smokewinder___yellow)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (14, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        LAU_115_LAU_127_AIM_9L = (14, Weapons.LAU_115_LAU_127_AIM_9L)
        Mk_82___500lb_GP_Bomb_LD = (14, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            14,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        AGM_84D_Harpoon_AShM = (14, Weapons.AGM_84D_Harpoon_AShM)
        LTF_5b_Aerial_Torpedo = (14, Weapons.LTF_5b_Aerial_Torpedo)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14}

    tasks = [
        task.Transport,
        task.Reconnaissance,
        task.GroundAttack,
        task.CAS,
        task.AFAC,
        task.RunwayAttack,
        task.AntishipStrike,
    ]
    task_default = task.AntishipStrike


@planemod
class V22_Osprey(PlaneType):
    id = "V22_Osprey"
    group_size_max = 1
    height = 6.63
    width = 25.78
    length = 17.48
    fuel_max = 3519.423
    max_speed = 990
    chaff = 120
    flare = 60
    charge_total = 240
    chaff_charge_size = 1
    flare_charge_size = 2
    eplrs = True
    category = "Air"  # {C168A850-3C0B-436a-95B5-C4A015552560}

    livery_name = "V22_OSPREY"  # from type

    pylons: Set[int] = set()

    tasks = [task.Transport]
    task_default = task.Transport
