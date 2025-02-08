from typing import Set

from dcs import task
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

from game.modsupport import planemod
from pydcs_extensions.weapon_injector import inject_weapons


class WeaponsF105:
    Fuel_Tank = {"clsid": "{VSN_F105G_PTB}", "name": "Fuel Tank", "weight": 3027}
    Fuel_Tank_ = {
        "clsid": "{VSN_F105G_Center_PTB}",
        "name": "Fuel Tank",
        "weight": 2062,
    }
    LAU_105_2_AIM_9L__ = {
        "clsid": "{VSN_F105_LAU105_AIM9L}",
        "name": "LAU-105 2*AIM-9L",
        "weight": 332,
    }
    LAU_105_2_AIM_9P_ = {
        "clsid": "{VSN_F105_LAU105_AIM9P}",
        "name": "LAU-105 2*AIM-9P",
        "weight": 332,
    }
    MER_6_M117_F_105 = {
        "clsid": "{SB_F105_BRU_41A_M117_6}",
        "name": "MER*6 M117 F-105",
        "weight": 2100,
    }
    MER_6_Mk_82_F_105 = {
        "clsid": "{VSN_F105_MK82_6}",
        "name": "MER*6 Mk-82 F-105",
        "weight": 1506,
    }
    TER_M117_F_105 = {
        "clsid": "{SB_F105_TER9A_M117_3}",
        "name": "TER M117 F-105",
        "weight": 1500,
    }
    vsn_f105_lau6 = {"clsid": "{F105_LAUx6}", "name": "vsn_f105_lau6", "weight": None}


inject_weapons(WeaponsF105)


@planemod
class VSN_F105G(PlaneType):
    id = "VSN_F105G"
    flyable = True
    height = 6.157
    width = 10.63
    length = 20.04
    fuel_max = 4986
    max_speed = 2240.928
    chaff = 30
    flare = 15
    charge_total = 60
    chaff_charge_size = 1
    flare_charge_size = 2
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}

    livery_name = "VSN_F105G"  # from type

    class Pylon3:
        Smoke_Generator___red_ = (3, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (3, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (3, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (3, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (3, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (3, Weapons.Smoke_Generator___orange_)

    class Pylon4:
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (4, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        LAU_105_2_AIM_9L__ = (4, WeaponsF105.LAU_105_2_AIM_9L__)
        LAU_105_2_AIM_9P_ = (4, WeaponsF105.LAU_105_2_AIM_9P_)
        AIM_9P_Sidewinder_IR_AAM = (4, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9B_Sidewinder_IR_AAM = (4, Weapons.AIM_9B_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (4, Weapons.AIM_9L_Sidewinder_IR_AAM)
        Mk_84___2000lb_GP_Bomb_LD = (4, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            4,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_82___500lb_GP_Bomb_LD = (4, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_83___1000lb_GP_Bomb_LD = (4, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (4, Weapons.M117___750lb_GP_Bomb_LD)
        AGM_45A_Shrike_ARM = (4, Weapons.AGM_45A_Shrike_ARM)
        LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_Mk1__HE = (
            4,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE,
        )
        LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_Mk5__HEAT = (
            4,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT,
        )

    # ERRR <CLEAN>

    class Pylon5:
        AGM_45A_Shrike_ARM = (5, Weapons.AGM_45A_Shrike_ARM)
        Mk_84___2000lb_GP_Bomb_LD = (5, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            5,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_82___500lb_GP_Bomb_LD = (5, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_83___1000lb_GP_Bomb_LD = (5, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        MER_6_Mk_82_F_105 = (5, WeaponsF105.MER_6_Mk_82_F_105)
        Fuel_Tank = (5, WeaponsF105.Fuel_Tank)
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            5,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        MER_6_M117_F_105 = (5, WeaponsF105.MER_6_M117_F_105)
        TER_M117_F_105 = (5, WeaponsF105.TER_M117_F_105)
        _3_Mk_83 = (5, Weapons._3_Mk_83)
        LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_Mk1__HE = (
            5,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE,
        )
        LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_Mk5__HEAT = (
            5,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT,
        )

    # ERRR {BRU33_2*LAU61_M282}
    # ERRR <CLEAN>

    class Pylon6:
        Mk_84___2000lb_GP_Bomb_LD = (6, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            6,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (6, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        MER_6_Mk_82_F_105 = (6, WeaponsF105.MER_6_Mk_82_F_105)
        MER_6_M117_F_105 = (6, WeaponsF105.MER_6_M117_F_105)
        TER_M117_F_105 = (6, WeaponsF105.TER_M117_F_105)
        _3_Mk_83 = (6, Weapons._3_Mk_83)
        Fuel_Tank_ = (6, WeaponsF105.Fuel_Tank_)

    # ERRR <CLEAN>

    class Pylon7:
        AGM_45A_Shrike_ARM = (7, Weapons.AGM_45A_Shrike_ARM)
        Mk_84___2000lb_GP_Bomb_LD = (7, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            7,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_82___500lb_GP_Bomb_LD = (7, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_83___1000lb_GP_Bomb_LD = (7, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        MER_6_Mk_82_F_105 = (7, WeaponsF105.MER_6_Mk_82_F_105)
        Fuel_Tank = (7, WeaponsF105.Fuel_Tank)
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        MER_6_M117_F_105 = (7, WeaponsF105.MER_6_M117_F_105)
        TER_M117_F_105 = (7, WeaponsF105.TER_M117_F_105)
        _3_Mk_83 = (7, Weapons._3_Mk_83)
        LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_Mk1__HE = (
            7,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE,
        )
        LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_Mk5__HEAT = (
            7,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT,
        )

    # ERRR {BRU33_2*LAU61_M282}
    # ERRR <CLEAN>

    class Pylon8:
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (8, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        LAU_105_2_AIM_9L__ = (8, WeaponsF105.LAU_105_2_AIM_9L__)
        LAU_105_2_AIM_9P_ = (8, WeaponsF105.LAU_105_2_AIM_9P_)
        AIM_9P_Sidewinder_IR_AAM = (8, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9B_Sidewinder_IR_AAM = (8, Weapons.AIM_9B_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (8, Weapons.AIM_9L_Sidewinder_IR_AAM)
        Mk_84___2000lb_GP_Bomb_LD = (8, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            8,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_82___500lb_GP_Bomb_LD = (8, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_83___1000lb_GP_Bomb_LD = (8, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (8, Weapons.M117___750lb_GP_Bomb_LD)
        AGM_45A_Shrike_ARM = (8, Weapons.AGM_45A_Shrike_ARM)
        LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_Mk1__HE = (
            8,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE,
        )
        LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_Mk5__HEAT = (
            8,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT,
        )

    # ERRR <CLEAN>

    class Pylon9:
        L_081_Fantasmagoria_ELINT_pod = (9, Weapons.L_081_Fantasmagoria_ELINT_pod)

    pylons: Set[int] = {3, 4, 5, 6, 7, 8, 9}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.Reconnaissance,
        task.GroundAttack,
        task.CAS,
        task.RunwayAttack,
        task.AntishipStrike,
    ]
    task_default = task.FighterSweep


@planemod
class VSN_F105D(PlaneType):
    id = "VSN_F105D"
    flyable = True
    height = 6.157
    width = 10.63
    length = 20.04
    fuel_max = 4986
    max_speed = 2240.928
    chaff = 30
    flare = 15
    charge_total = 60
    chaff_charge_size = 1
    flare_charge_size = 2
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}

    livery_name = "VSN_F105D"  # from type

    class Pylon3:
        Smoke_Generator___red_ = (3, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (3, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (3, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (3, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (3, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (3, Weapons.Smoke_Generator___orange_)

    class Pylon4:
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (4, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        AIM_9P_Sidewinder_IR_AAM = (4, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (4, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9B_Sidewinder_IR_AAM = (4, Weapons.AIM_9B_Sidewinder_IR_AAM)
        LAU_105_2_AIM_9L__ = (4, WeaponsF105.LAU_105_2_AIM_9L__)
        LAU_105_2_AIM_9P_ = (4, WeaponsF105.LAU_105_2_AIM_9P_)
        Mk_84___2000lb_GP_Bomb_LD = (4, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            4,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_82___500lb_GP_Bomb_LD = (4, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_83___1000lb_GP_Bomb_LD = (4, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (4, Weapons.M117___750lb_GP_Bomb_LD)
        AGM_45A_Shrike_ARM = (4, Weapons.AGM_45A_Shrike_ARM)
        LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_Mk1__HE = (
            4,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE,
        )
        LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_Mk5__HEAT = (
            4,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT,
        )

    # ERRR <CLEAN>

    class Pylon5:
        Mk_84___2000lb_GP_Bomb_LD = (5, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            5,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_82___500lb_GP_Bomb_LD = (5, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_83___1000lb_GP_Bomb_LD = (5, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        MER_6_Mk_82_F_105 = (5, WeaponsF105.MER_6_Mk_82_F_105)
        Fuel_Tank = (5, WeaponsF105.Fuel_Tank)
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            5,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        MER_6_M117_F_105 = (5, WeaponsF105.MER_6_M117_F_105)
        TER_M117_F_105 = (5, WeaponsF105.TER_M117_F_105)
        _3_Mk_83 = (5, Weapons._3_Mk_83)
        LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_Mk1__HE = (
            5,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE,
        )
        LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_Mk5__HEAT = (
            5,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT,
        )

    # ERRR {BRU33_2*LAU61_M282}
    # ERRR <CLEAN>

    class Pylon6:
        Mk_84___2000lb_GP_Bomb_LD = (6, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            6,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (6, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        MER_6_Mk_82_F_105 = (6, WeaponsF105.MER_6_Mk_82_F_105)
        MER_6_M117_F_105 = (6, WeaponsF105.MER_6_M117_F_105)
        TER_M117_F_105 = (6, WeaponsF105.TER_M117_F_105)
        _3_Mk_83 = (6, Weapons._3_Mk_83)
        Fuel_Tank_ = (6, WeaponsF105.Fuel_Tank_)

    # ERRR <CLEAN>

    class Pylon7:
        Mk_84___2000lb_GP_Bomb_LD = (7, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            7,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_82___500lb_GP_Bomb_LD = (7, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_83___1000lb_GP_Bomb_LD = (7, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        MER_6_Mk_82_F_105 = (7, WeaponsF105.MER_6_Mk_82_F_105)
        Fuel_Tank = (7, WeaponsF105.Fuel_Tank)
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        MER_6_M117_F_105 = (7, WeaponsF105.MER_6_M117_F_105)
        TER_M117_F_105 = (7, WeaponsF105.TER_M117_F_105)
        _3_Mk_83 = (7, Weapons._3_Mk_83)
        LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_Mk1__HE = (
            7,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE,
        )
        LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_Mk5__HEAT = (
            7,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT,
        )

    # ERRR {BRU33_2*LAU61_M282}
    # ERRR <CLEAN>

    class Pylon8:
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (8, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        AIM_9P_Sidewinder_IR_AAM = (8, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (8, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9B_Sidewinder_IR_AAM = (8, Weapons.AIM_9B_Sidewinder_IR_AAM)
        LAU_105_2_AIM_9L__ = (8, WeaponsF105.LAU_105_2_AIM_9L__)
        LAU_105_2_AIM_9P_ = (8, WeaponsF105.LAU_105_2_AIM_9P_)
        Mk_84___2000lb_GP_Bomb_LD = (8, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            8,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_82___500lb_GP_Bomb_LD = (8, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_83___1000lb_GP_Bomb_LD = (8, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (8, Weapons.M117___750lb_GP_Bomb_LD)
        AGM_45A_Shrike_ARM = (8, Weapons.AGM_45A_Shrike_ARM)
        LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_Mk1__HE = (
            8,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE,
        )
        LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_Mk5__HEAT = (
            8,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT,
        )

    # ERRR <CLEAN>

    class Pylon9:
        L_081_Fantasmagoria_ELINT_pod = (9, Weapons.L_081_Fantasmagoria_ELINT_pod)

    pylons: Set[int] = {3, 4, 5, 6, 7, 8, 9}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.Reconnaissance,
        task.GroundAttack,
        task.CAS,
        task.RunwayAttack,
        task.AntishipStrike,
    ]
    task_default = task.FighterSweep
