from typing import Dict, List, Set, Any

from dcs import task
from dcs.planes import PlaneType
from dcs.unitpropertydescription import UnitPropertyDescription
from dcs.weapons_data import Weapons

from game.modsupport import planemod
from pydcs_extensions.weapon_injector import inject_weapons


class VSNF35_Weapons:
    F35_GAU_22_gun_pod = {
        "clsid": "{VSN_F35_Gunpod}",
        "name": "F35 GAU-22 gun pod",
        "weight": 112.35,
    }
    Fuel_tank_610_gal__ = {
        "clsid": "{VSN_F35A_PTB}",
        "name": "Fuel tank 610 gal",
        "weight": 1960,
    }


inject_weapons(VSNF35_Weapons)


@planemod
class VSN_F35A(PlaneType):
    id = "VSN_F35A"
    flyable = True
    height = 4.39
    width = 10.7
    length = 15.7
    fuel_max = 8278
    max_speed = 1975.68
    chaff = 120
    flare = 120
    charge_total = 240
    chaff_charge_size = 1
    flare_charge_size = 1
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}

    livery_name = "VSN_F35A"  # from type

    class Pylon1:
        AIM_9M_Sidewinder_IR_AAM = (1, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (1, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (1, Weapons.AIM_9X_Sidewinder_IR_AAM)
        Smokewinder___red = (1, Weapons.Smokewinder___red)
        Smokewinder___green = (1, Weapons.Smokewinder___green)
        Smokewinder___blue = (1, Weapons.Smokewinder___blue)
        Smokewinder___white = (1, Weapons.Smokewinder___white)
        Smokewinder___yellow = (1, Weapons.Smokewinder___yellow)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (1, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

    class Pylon2:
        AIM_9M_Sidewinder_IR_AAM = (2, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (2, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (2, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            2,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        Mk_82___500lb_GP_Bomb_LD = (2, Weapons.Mk_82___500lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            2,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (2, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        CBU_97___10_x_SFW_Cluster_Bomb = (2, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            2,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            2,
            Weapons.LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            2,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_117_AGM_65G = (2, Weapons.LAU_117_AGM_65G)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            2,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (2, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        AGM_154C___JSOW_Unitary_BROACH = (2, Weapons.AGM_154C___JSOW_Unitary_BROACH)
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            2,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            2,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            2,
            Weapons.AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )

    class Pylon3:
        AIM_9M_Sidewinder_IR_AAM = (3, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (3, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (3, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            3,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        LAU_115_2_LAU_127_AIM_120C = (3, Weapons.LAU_115_2_LAU_127_AIM_120C)
        GBU_10___2000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_16___1000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        Mk_82___500lb_GP_Bomb_LD = (3, Weapons.Mk_82___500lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            3,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (3, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_83___1000lb_GP_Bombs_LD = (
            3,
            Weapons.MER2_with_2_x_Mk_83___1000lb_GP_Bombs_LD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (3, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        CBU_97___10_x_SFW_Cluster_Bomb = (3, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            3,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            3,
            Weapons.LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            3,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_117_AGM_65G = (3, Weapons.LAU_117_AGM_65G)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            3,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (3, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        AGM_154C___JSOW_Unitary_BROACH = (3, Weapons.AGM_154C___JSOW_Unitary_BROACH)
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            3,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            3,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        AGM_114K_Hellfire = (3, Weapons.AGM_114K_Hellfire)
        AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            3,
            Weapons.AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        Fuel_tank_610_gal__ = (3, VSNF35_Weapons.Fuel_tank_610_gal__)

    class Pylon4:
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            4,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (4, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_16___1000lb_Laser_Guided_Bomb = (
            4,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        Mk_84___2000lb_GP_Bomb_LD = (4, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        AGM_154C___JSOW_Unitary_BROACH = (4, Weapons.AGM_154C___JSOW_Unitary_BROACH)
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            4,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            4,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        CBU_97___10_x_SFW_Cluster_Bomb = (4, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)

    class Pylon5:
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            5,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )

    class Pylon6:
        Smoke_Generator___red_ = (6, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (6, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (6, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (6, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (6, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (6, Weapons.Smoke_Generator___orange_)

    class Pylon7:
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            7,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )

    class Pylon8:
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            8,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (8, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_16___1000lb_Laser_Guided_Bomb = (
            8,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        Mk_84___2000lb_GP_Bomb_LD = (8, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        AGM_154C___JSOW_Unitary_BROACH = (8, Weapons.AGM_154C___JSOW_Unitary_BROACH)
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            8,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            8,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        CBU_97___10_x_SFW_Cluster_Bomb = (8, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)

    class Pylon9:
        AIM_9M_Sidewinder_IR_AAM = (9, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (9, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (9, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            9,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        LAU_115_2_LAU_127_AIM_120C = (9, Weapons.LAU_115_2_LAU_127_AIM_120C)
        GBU_10___2000lb_Laser_Guided_Bomb = (
            9,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_16___1000lb_Laser_Guided_Bomb = (
            9,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            9,
            Weapons.GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        Mk_82___500lb_GP_Bomb_LD = (9, Weapons.Mk_82___500lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            9,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (9, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_83___1000lb_GP_Bombs_LD = (
            9,
            Weapons.MER2_with_2_x_Mk_83___1000lb_GP_Bombs_LD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (9, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        CBU_97___10_x_SFW_Cluster_Bomb = (9, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            9,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            9,
            Weapons.LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            9,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_117_AGM_65G = (9, Weapons.LAU_117_AGM_65G)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            9,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (9, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        AGM_154C___JSOW_Unitary_BROACH = (9, Weapons.AGM_154C___JSOW_Unitary_BROACH)
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            9,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            9,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        AGM_114K_Hellfire = (9, Weapons.AGM_114K_Hellfire)
        AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            9,
            Weapons.AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        Fuel_tank_610_gal__ = (9, VSNF35_Weapons.Fuel_tank_610_gal__)

    class Pylon10:
        AIM_9M_Sidewinder_IR_AAM = (10, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (10, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (10, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            10,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        Mk_82___500lb_GP_Bomb_LD = (10, Weapons.Mk_82___500lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            10,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (10, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        CBU_97___10_x_SFW_Cluster_Bomb = (10, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            10,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            10,
            Weapons.LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            10,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_117_AGM_65G = (10, Weapons.LAU_117_AGM_65G)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            10,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (
            10,
            Weapons.GBU_12___500lb_Laser_Guided_Bomb,
        )
        AGM_154C___JSOW_Unitary_BROACH = (10, Weapons.AGM_154C___JSOW_Unitary_BROACH)
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            10,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            10,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            10,
            Weapons.AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )

    class Pylon11:
        AIM_9M_Sidewinder_IR_AAM = (11, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (11, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (11, Weapons.AIM_9X_Sidewinder_IR_AAM)
        Smokewinder___red = (11, Weapons.Smokewinder___red)
        Smokewinder___green = (11, Weapons.Smokewinder___green)
        Smokewinder___blue = (11, Weapons.Smokewinder___blue)
        Smokewinder___white = (11, Weapons.Smokewinder___white)
        Smokewinder___yellow = (11, Weapons.Smokewinder___yellow)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (11, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}

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
    task_default = task.CAS


@planemod
class VSN_F35A_AG(PlaneType):
    id = "VSN_F35A_AG"
    flyable = True
    height = 4.39
    width = 10.7
    length = 15.7
    fuel_max = 8278
    max_speed = 1975.68
    chaff = 120
    flare = 120
    charge_total = 240
    chaff_charge_size = 1
    flare_charge_size = 1
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}

    livery_name = "VSN_F35A_AG"  # from type

    class Pylon1:
        AIM_9M_Sidewinder_IR_AAM = (1, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (1, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (1, Weapons.AIM_9X_Sidewinder_IR_AAM)
        Smokewinder___red = (1, Weapons.Smokewinder___red)
        Smokewinder___green = (1, Weapons.Smokewinder___green)
        Smokewinder___blue = (1, Weapons.Smokewinder___blue)
        Smokewinder___white = (1, Weapons.Smokewinder___white)
        Smokewinder___yellow = (1, Weapons.Smokewinder___yellow)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (1, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

    class Pylon2:
        AIM_9M_Sidewinder_IR_AAM = (2, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (2, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (2, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            2,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        Mk_82___500lb_GP_Bomb_LD = (2, Weapons.Mk_82___500lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            2,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (2, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        CBU_97___10_x_SFW_Cluster_Bomb = (2, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            2,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            2,
            Weapons.LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            2,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_117_AGM_65G = (2, Weapons.LAU_117_AGM_65G)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            2,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (2, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        AGM_154C___JSOW_Unitary_BROACH = (2, Weapons.AGM_154C___JSOW_Unitary_BROACH)
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            2,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            2,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            2,
            Weapons.AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )

    class Pylon3:
        AIM_9M_Sidewinder_IR_AAM = (3, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (3, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (3, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            3,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        LAU_115_2_LAU_127_AIM_120C = (3, Weapons.LAU_115_2_LAU_127_AIM_120C)
        GBU_10___2000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_16___1000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        Mk_82___500lb_GP_Bomb_LD = (3, Weapons.Mk_82___500lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            3,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (3, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_83___1000lb_GP_Bombs_LD = (
            3,
            Weapons.MER2_with_2_x_Mk_83___1000lb_GP_Bombs_LD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (3, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        CBU_97___10_x_SFW_Cluster_Bomb = (3, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            3,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            3,
            Weapons.LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            3,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_117_AGM_65G = (3, Weapons.LAU_117_AGM_65G)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            3,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (3, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        AGM_154C___JSOW_Unitary_BROACH = (3, Weapons.AGM_154C___JSOW_Unitary_BROACH)
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            3,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            3,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        AGM_114K_Hellfire = (3, Weapons.AGM_114K_Hellfire)
        AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            3,
            Weapons.AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        Fuel_tank_610_gal__ = (3, VSNF35_Weapons.Fuel_tank_610_gal__)

    class Pylon4:
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            4,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (4, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_16___1000lb_Laser_Guided_Bomb = (
            4,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        Mk_84___2000lb_GP_Bomb_LD = (4, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        AGM_154C___JSOW_Unitary_BROACH = (4, Weapons.AGM_154C___JSOW_Unitary_BROACH)
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            4,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            4,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        CBU_97___10_x_SFW_Cluster_Bomb = (4, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)

    class Pylon5:
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            5,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )

    class Pylon6:
        Smoke_Generator___red_ = (6, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (6, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (6, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (6, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (6, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (6, Weapons.Smoke_Generator___orange_)

    class Pylon7:
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            7,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )

    class Pylon8:
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            8,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (8, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_16___1000lb_Laser_Guided_Bomb = (
            8,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        Mk_84___2000lb_GP_Bomb_LD = (8, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        AGM_154C___JSOW_Unitary_BROACH = (8, Weapons.AGM_154C___JSOW_Unitary_BROACH)
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            8,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            8,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        CBU_97___10_x_SFW_Cluster_Bomb = (8, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)

    class Pylon9:
        AIM_9M_Sidewinder_IR_AAM = (9, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (9, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (9, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            9,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        LAU_115_2_LAU_127_AIM_120C = (9, Weapons.LAU_115_2_LAU_127_AIM_120C)
        GBU_10___2000lb_Laser_Guided_Bomb = (
            9,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_16___1000lb_Laser_Guided_Bomb = (
            9,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            9,
            Weapons.GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        Mk_82___500lb_GP_Bomb_LD = (9, Weapons.Mk_82___500lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            9,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (9, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_83___1000lb_GP_Bombs_LD = (
            9,
            Weapons.MER2_with_2_x_Mk_83___1000lb_GP_Bombs_LD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (9, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        CBU_97___10_x_SFW_Cluster_Bomb = (9, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            9,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            9,
            Weapons.LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            9,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_117_AGM_65G = (9, Weapons.LAU_117_AGM_65G)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            9,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (9, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        AGM_154C___JSOW_Unitary_BROACH = (9, Weapons.AGM_154C___JSOW_Unitary_BROACH)
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            9,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            9,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        AGM_114K_Hellfire = (9, Weapons.AGM_114K_Hellfire)
        AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            9,
            Weapons.AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        Fuel_tank_610_gal__ = (9, VSNF35_Weapons.Fuel_tank_610_gal__)

    class Pylon10:
        AIM_9M_Sidewinder_IR_AAM = (10, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (10, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (10, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            10,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        Mk_82___500lb_GP_Bomb_LD = (10, Weapons.Mk_82___500lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            10,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (10, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        CBU_97___10_x_SFW_Cluster_Bomb = (10, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            10,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            10,
            Weapons.LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            10,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_117_AGM_65G = (10, Weapons.LAU_117_AGM_65G)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            10,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (
            10,
            Weapons.GBU_12___500lb_Laser_Guided_Bomb,
        )
        AGM_154C___JSOW_Unitary_BROACH = (10, Weapons.AGM_154C___JSOW_Unitary_BROACH)
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            10,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            10,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            10,
            Weapons.AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )

    class Pylon11:
        AIM_9M_Sidewinder_IR_AAM = (11, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (11, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (11, Weapons.AIM_9X_Sidewinder_IR_AAM)
        Smokewinder___red = (11, Weapons.Smokewinder___red)
        Smokewinder___green = (11, Weapons.Smokewinder___green)
        Smokewinder___blue = (11, Weapons.Smokewinder___blue)
        Smokewinder___white = (11, Weapons.Smokewinder___white)
        Smokewinder___yellow = (11, Weapons.Smokewinder___yellow)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (11, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

    class Pylon12:
        L005_Sorbtsiya_ECM_pod__left_ = (12, Weapons.L005_Sorbtsiya_ECM_pod__left_)

    class Pylon13:
        L_081_Fantasmagoria_ELINT_pod = (13, Weapons.L_081_Fantasmagoria_ELINT_pod)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13}

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
    task_default = task.CAS


@planemod
class VSN_F35B(PlaneType):
    id = "VSN_F35B"
    flyable = True
    height = 4.39
    width = 10.7
    length = 15.7
    fuel_max = 8278
    max_speed = 1975.68
    chaff = 120
    flare = 120
    charge_total = 240
    chaff_charge_size = 1
    flare_charge_size = 1
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}

    livery_name = "VSN_F35B"  # from type

    class Pylon1:
        AIM_9M_Sidewinder_IR_AAM = (1, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (1, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (1, Weapons.AIM_9X_Sidewinder_IR_AAM)
        Smokewinder___red = (1, Weapons.Smokewinder___red)
        Smokewinder___green = (1, Weapons.Smokewinder___green)
        Smokewinder___blue = (1, Weapons.Smokewinder___blue)
        Smokewinder___white = (1, Weapons.Smokewinder___white)
        Smokewinder___yellow = (1, Weapons.Smokewinder___yellow)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (1, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

    class Pylon2:
        AIM_9M_Sidewinder_IR_AAM = (2, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (2, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (2, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            2,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        Mk_82___500lb_GP_Bomb_LD = (2, Weapons.Mk_82___500lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            2,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (2, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        CBU_97___10_x_SFW_Cluster_Bomb = (2, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            2,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            2,
            Weapons.LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            2,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_117_AGM_65G = (2, Weapons.LAU_117_AGM_65G)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            2,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (2, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        AGM_154C___JSOW_Unitary_BROACH = (2, Weapons.AGM_154C___JSOW_Unitary_BROACH)
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            2,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            2,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            2,
            Weapons.AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )

    class Pylon3:
        AIM_9M_Sidewinder_IR_AAM = (3, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (3, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (3, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            3,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        LAU_115_2_LAU_127_AIM_120C = (3, Weapons.LAU_115_2_LAU_127_AIM_120C)
        GBU_10___2000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_16___1000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        Mk_82___500lb_GP_Bomb_LD = (3, Weapons.Mk_82___500lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            3,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (3, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_83___1000lb_GP_Bombs_LD = (
            3,
            Weapons.MER2_with_2_x_Mk_83___1000lb_GP_Bombs_LD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (3, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        CBU_97___10_x_SFW_Cluster_Bomb = (3, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            3,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            3,
            Weapons.LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            3,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_117_AGM_65G = (3, Weapons.LAU_117_AGM_65G)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            3,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (3, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        AGM_154C___JSOW_Unitary_BROACH = (3, Weapons.AGM_154C___JSOW_Unitary_BROACH)
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            3,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            3,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        AGM_114K_Hellfire = (3, Weapons.AGM_114K_Hellfire)
        AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            3,
            Weapons.AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        Fuel_tank_610_gal__ = (3, VSNF35_Weapons.Fuel_tank_610_gal__)

    class Pylon4:
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            4,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (4, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_16___1000lb_Laser_Guided_Bomb = (
            4,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        Mk_84___2000lb_GP_Bomb_LD = (4, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        AGM_154C___JSOW_Unitary_BROACH = (4, Weapons.AGM_154C___JSOW_Unitary_BROACH)
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            4,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            4,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        CBU_97___10_x_SFW_Cluster_Bomb = (4, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)

    class Pylon5:
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            5,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )

    class Pylon6:
        Smoke_Generator___red_ = (6, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (6, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (6, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (6, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (6, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (6, Weapons.Smoke_Generator___orange_)
        F35_GAU_22_gun_pod = (6, VSNF35_Weapons.F35_GAU_22_gun_pod)

    # ERRR <CLEAN>

    class Pylon7:
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            7,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )

    class Pylon8:
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            8,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (8, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_16___1000lb_Laser_Guided_Bomb = (
            8,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        Mk_84___2000lb_GP_Bomb_LD = (8, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        AGM_154C___JSOW_Unitary_BROACH = (8, Weapons.AGM_154C___JSOW_Unitary_BROACH)
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            8,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            8,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        CBU_97___10_x_SFW_Cluster_Bomb = (8, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)

    class Pylon9:
        AIM_9M_Sidewinder_IR_AAM = (9, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (9, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (9, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            9,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        LAU_115_2_LAU_127_AIM_120C = (9, Weapons.LAU_115_2_LAU_127_AIM_120C)
        GBU_10___2000lb_Laser_Guided_Bomb = (
            9,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_16___1000lb_Laser_Guided_Bomb = (
            9,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            9,
            Weapons.GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        Mk_82___500lb_GP_Bomb_LD = (9, Weapons.Mk_82___500lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            9,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (9, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_83___1000lb_GP_Bombs_LD = (
            9,
            Weapons.MER2_with_2_x_Mk_83___1000lb_GP_Bombs_LD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (9, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        CBU_97___10_x_SFW_Cluster_Bomb = (9, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            9,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            9,
            Weapons.LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            9,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_117_AGM_65G = (9, Weapons.LAU_117_AGM_65G)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            9,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (9, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        AGM_154C___JSOW_Unitary_BROACH = (9, Weapons.AGM_154C___JSOW_Unitary_BROACH)
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            9,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            9,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        AGM_114K_Hellfire = (9, Weapons.AGM_114K_Hellfire)
        AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            9,
            Weapons.AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        Fuel_tank_610_gal__ = (9, VSNF35_Weapons.Fuel_tank_610_gal__)

    class Pylon10:
        AIM_9M_Sidewinder_IR_AAM = (10, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (10, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (10, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            10,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        Mk_82___500lb_GP_Bomb_LD = (10, Weapons.Mk_82___500lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            10,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (10, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        CBU_97___10_x_SFW_Cluster_Bomb = (10, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            10,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            10,
            Weapons.LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            10,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_117_AGM_65G = (10, Weapons.LAU_117_AGM_65G)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            10,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (
            10,
            Weapons.GBU_12___500lb_Laser_Guided_Bomb,
        )
        AGM_154C___JSOW_Unitary_BROACH = (10, Weapons.AGM_154C___JSOW_Unitary_BROACH)
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            10,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            10,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            10,
            Weapons.AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )

    class Pylon11:
        AIM_9M_Sidewinder_IR_AAM = (11, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (11, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (11, Weapons.AIM_9X_Sidewinder_IR_AAM)
        Smokewinder___red = (11, Weapons.Smokewinder___red)
        Smokewinder___green = (11, Weapons.Smokewinder___green)
        Smokewinder___blue = (11, Weapons.Smokewinder___blue)
        Smokewinder___white = (11, Weapons.Smokewinder___white)
        Smokewinder___yellow = (11, Weapons.Smokewinder___yellow)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (11, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}

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
        task.AntishipStrike,
    ]
    task_default = task.CAS


@planemod
class VSN_F35B_AG(PlaneType):
    id = "VSN_F35B_AG"
    flyable = True
    height = 4.39
    width = 10.7
    length = 15.7
    fuel_max = 8278
    max_speed = 1975.68
    chaff = 120
    flare = 120
    charge_total = 240
    chaff_charge_size = 1
    flare_charge_size = 1
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}

    livery_name = "VSN_F35B_AG"  # from type

    class Pylon1:
        AIM_9M_Sidewinder_IR_AAM = (1, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (1, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (1, Weapons.AIM_9X_Sidewinder_IR_AAM)
        Smokewinder___red = (1, Weapons.Smokewinder___red)
        Smokewinder___green = (1, Weapons.Smokewinder___green)
        Smokewinder___blue = (1, Weapons.Smokewinder___blue)
        Smokewinder___white = (1, Weapons.Smokewinder___white)
        Smokewinder___yellow = (1, Weapons.Smokewinder___yellow)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (1, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

    class Pylon2:
        AIM_9M_Sidewinder_IR_AAM = (2, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (2, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (2, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            2,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        Mk_82___500lb_GP_Bomb_LD = (2, Weapons.Mk_82___500lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            2,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (2, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        CBU_97___10_x_SFW_Cluster_Bomb = (2, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            2,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            2,
            Weapons.LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            2,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_117_AGM_65G = (2, Weapons.LAU_117_AGM_65G)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            2,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (2, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        AGM_154C___JSOW_Unitary_BROACH = (2, Weapons.AGM_154C___JSOW_Unitary_BROACH)
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            2,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            2,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            2,
            Weapons.AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )

    class Pylon3:
        AIM_9M_Sidewinder_IR_AAM = (3, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (3, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (3, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            3,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        LAU_115_2_LAU_127_AIM_120C = (3, Weapons.LAU_115_2_LAU_127_AIM_120C)
        GBU_10___2000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_16___1000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        Mk_82___500lb_GP_Bomb_LD = (3, Weapons.Mk_82___500lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            3,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (3, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_83___1000lb_GP_Bombs_LD = (
            3,
            Weapons.MER2_with_2_x_Mk_83___1000lb_GP_Bombs_LD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (3, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        CBU_97___10_x_SFW_Cluster_Bomb = (3, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            3,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            3,
            Weapons.LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            3,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_117_AGM_65G = (3, Weapons.LAU_117_AGM_65G)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            3,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (3, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        AGM_154C___JSOW_Unitary_BROACH = (3, Weapons.AGM_154C___JSOW_Unitary_BROACH)
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            3,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            3,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        AGM_114K_Hellfire = (3, Weapons.AGM_114K_Hellfire)
        AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            3,
            Weapons.AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        Fuel_tank_610_gal__ = (3, VSNF35_Weapons.Fuel_tank_610_gal__)

    class Pylon4:
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            4,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (4, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_16___1000lb_Laser_Guided_Bomb = (
            4,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        Mk_84___2000lb_GP_Bomb_LD = (4, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        AGM_154C___JSOW_Unitary_BROACH = (4, Weapons.AGM_154C___JSOW_Unitary_BROACH)
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            4,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            4,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        CBU_97___10_x_SFW_Cluster_Bomb = (4, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)

    class Pylon5:
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            5,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )

    class Pylon6:
        Smoke_Generator___red_ = (6, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (6, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (6, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (6, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (6, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (6, Weapons.Smoke_Generator___orange_)
        F35_GAU_22_gun_pod = (6, VSNF35_Weapons.F35_GAU_22_gun_pod)

    # ERRR <CLEAN>

    class Pylon7:
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            7,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )

    class Pylon8:
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            8,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (8, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_16___1000lb_Laser_Guided_Bomb = (
            8,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        Mk_84___2000lb_GP_Bomb_LD = (8, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        AGM_154C___JSOW_Unitary_BROACH = (8, Weapons.AGM_154C___JSOW_Unitary_BROACH)
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            8,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            8,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        CBU_97___10_x_SFW_Cluster_Bomb = (8, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)

    class Pylon9:
        AIM_9M_Sidewinder_IR_AAM = (9, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (9, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (9, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            9,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        LAU_115_2_LAU_127_AIM_120C = (9, Weapons.LAU_115_2_LAU_127_AIM_120C)
        GBU_10___2000lb_Laser_Guided_Bomb = (
            9,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_16___1000lb_Laser_Guided_Bomb = (
            9,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            9,
            Weapons.GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        Mk_82___500lb_GP_Bomb_LD = (9, Weapons.Mk_82___500lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            9,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (9, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_83___1000lb_GP_Bombs_LD = (
            9,
            Weapons.MER2_with_2_x_Mk_83___1000lb_GP_Bombs_LD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (9, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        CBU_97___10_x_SFW_Cluster_Bomb = (9, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            9,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            9,
            Weapons.LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            9,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_117_AGM_65G = (9, Weapons.LAU_117_AGM_65G)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            9,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (9, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        AGM_154C___JSOW_Unitary_BROACH = (9, Weapons.AGM_154C___JSOW_Unitary_BROACH)
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            9,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            9,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        AGM_114K_Hellfire = (9, Weapons.AGM_114K_Hellfire)
        AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            9,
            Weapons.AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        Fuel_tank_610_gal__ = (9, VSNF35_Weapons.Fuel_tank_610_gal__)

    class Pylon10:
        AIM_9M_Sidewinder_IR_AAM = (10, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (10, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (10, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            10,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        Mk_82___500lb_GP_Bomb_LD = (10, Weapons.Mk_82___500lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            10,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (10, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        CBU_97___10_x_SFW_Cluster_Bomb = (10, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            10,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            10,
            Weapons.LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            10,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_117_AGM_65G = (10, Weapons.LAU_117_AGM_65G)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            10,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (
            10,
            Weapons.GBU_12___500lb_Laser_Guided_Bomb,
        )
        AGM_154C___JSOW_Unitary_BROACH = (10, Weapons.AGM_154C___JSOW_Unitary_BROACH)
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            10,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            10,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            10,
            Weapons.AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )

    class Pylon11:
        AIM_9M_Sidewinder_IR_AAM = (11, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (11, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (11, Weapons.AIM_9X_Sidewinder_IR_AAM)
        Smokewinder___red = (11, Weapons.Smokewinder___red)
        Smokewinder___green = (11, Weapons.Smokewinder___green)
        Smokewinder___blue = (11, Weapons.Smokewinder___blue)
        Smokewinder___white = (11, Weapons.Smokewinder___white)
        Smokewinder___yellow = (11, Weapons.Smokewinder___yellow)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (11, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

    class Pylon12:
        L005_Sorbtsiya_ECM_pod__left_ = (12, Weapons.L005_Sorbtsiya_ECM_pod__left_)
        Smoke_Generator___red_ = (12, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (12, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (12, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (12, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (12, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (12, Weapons.Smoke_Generator___orange_)

    class Pylon13:
        L_081_Fantasmagoria_ELINT_pod = (13, Weapons.L_081_Fantasmagoria_ELINT_pod)
        Smoke_Generator___red_ = (13, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (13, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (13, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (13, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (13, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (13, Weapons.Smoke_Generator___orange_)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13}

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
        task.AntishipStrike,
    ]
    task_default = task.CAS


@planemod
class VSN_F35C(PlaneType):
    id = "VSN_F35C"
    flyable = True
    height = 4.39
    width = 10.7
    length = 15.7
    fuel_max = 8278
    max_speed = 1975.68
    chaff = 120
    flare = 120
    charge_total = 240
    chaff_charge_size = 1
    flare_charge_size = 1
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}

    livery_name = "VSN_F35C"  # from type

    class Pylon1:
        AIM_9M_Sidewinder_IR_AAM = (1, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (1, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (1, Weapons.AIM_9X_Sidewinder_IR_AAM)
        Smokewinder___red = (1, Weapons.Smokewinder___red)
        Smokewinder___green = (1, Weapons.Smokewinder___green)
        Smokewinder___blue = (1, Weapons.Smokewinder___blue)
        Smokewinder___white = (1, Weapons.Smokewinder___white)
        Smokewinder___yellow = (1, Weapons.Smokewinder___yellow)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (1, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

    class Pylon2:
        AIM_9M_Sidewinder_IR_AAM = (2, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (2, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (2, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            2,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        Mk_82___500lb_GP_Bomb_LD = (2, Weapons.Mk_82___500lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            2,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (2, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        CBU_97___10_x_SFW_Cluster_Bomb = (2, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            2,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            2,
            Weapons.LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            2,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_117_AGM_65G = (2, Weapons.LAU_117_AGM_65G)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            2,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (2, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        AGM_154C___JSOW_Unitary_BROACH = (2, Weapons.AGM_154C___JSOW_Unitary_BROACH)
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            2,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            2,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            2,
            Weapons.AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )

    class Pylon3:
        AIM_9M_Sidewinder_IR_AAM = (3, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (3, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (3, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            3,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        LAU_115_2_LAU_127_AIM_120C = (3, Weapons.LAU_115_2_LAU_127_AIM_120C)
        GBU_10___2000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_16___1000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        Mk_82___500lb_GP_Bomb_LD = (3, Weapons.Mk_82___500lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            3,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (3, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_83___1000lb_GP_Bombs_LD = (
            3,
            Weapons.MER2_with_2_x_Mk_83___1000lb_GP_Bombs_LD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (3, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        CBU_97___10_x_SFW_Cluster_Bomb = (3, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            3,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            3,
            Weapons.LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            3,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_117_AGM_65G = (3, Weapons.LAU_117_AGM_65G)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            3,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (3, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        AGM_154C___JSOW_Unitary_BROACH = (3, Weapons.AGM_154C___JSOW_Unitary_BROACH)
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            3,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            3,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        AGM_114K_Hellfire = (3, Weapons.AGM_114K_Hellfire)
        AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            3,
            Weapons.AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        Fuel_tank_610_gal__ = (3, VSNF35_Weapons.Fuel_tank_610_gal__)

    class Pylon4:
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            4,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (4, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_16___1000lb_Laser_Guided_Bomb = (
            4,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        Mk_84___2000lb_GP_Bomb_LD = (4, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        AGM_154C___JSOW_Unitary_BROACH = (4, Weapons.AGM_154C___JSOW_Unitary_BROACH)
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            4,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            4,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        CBU_97___10_x_SFW_Cluster_Bomb = (4, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)

    class Pylon5:
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            5,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )

    class Pylon6:
        Smoke_Generator___red_ = (6, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (6, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (6, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (6, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (6, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (6, Weapons.Smoke_Generator___orange_)
        F35_GAU_22_gun_pod = (6, VSNF35_Weapons.F35_GAU_22_gun_pod)

    # ERRR <CLEAN>

    class Pylon7:
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            7,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )

    class Pylon8:
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            8,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (8, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_16___1000lb_Laser_Guided_Bomb = (
            8,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        Mk_84___2000lb_GP_Bomb_LD = (8, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        AGM_154C___JSOW_Unitary_BROACH = (8, Weapons.AGM_154C___JSOW_Unitary_BROACH)
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            8,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            8,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        CBU_97___10_x_SFW_Cluster_Bomb = (8, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)

    class Pylon9:
        AIM_9M_Sidewinder_IR_AAM = (9, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (9, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (9, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            9,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        LAU_115_2_LAU_127_AIM_120C = (9, Weapons.LAU_115_2_LAU_127_AIM_120C)
        GBU_10___2000lb_Laser_Guided_Bomb = (
            9,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_16___1000lb_Laser_Guided_Bomb = (
            9,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            9,
            Weapons.GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        Mk_82___500lb_GP_Bomb_LD = (9, Weapons.Mk_82___500lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            9,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (9, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_83___1000lb_GP_Bombs_LD = (
            9,
            Weapons.MER2_with_2_x_Mk_83___1000lb_GP_Bombs_LD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (9, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        CBU_97___10_x_SFW_Cluster_Bomb = (9, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            9,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            9,
            Weapons.LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            9,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_117_AGM_65G = (9, Weapons.LAU_117_AGM_65G)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            9,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (9, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        AGM_154C___JSOW_Unitary_BROACH = (9, Weapons.AGM_154C___JSOW_Unitary_BROACH)
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            9,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            9,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        AGM_114K_Hellfire = (9, Weapons.AGM_114K_Hellfire)
        AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            9,
            Weapons.AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        Fuel_tank_610_gal__ = (9, VSNF35_Weapons.Fuel_tank_610_gal__)

    class Pylon10:
        AIM_9M_Sidewinder_IR_AAM = (10, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (10, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (10, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            10,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        Mk_82___500lb_GP_Bomb_LD = (10, Weapons.Mk_82___500lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            10,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (10, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        CBU_97___10_x_SFW_Cluster_Bomb = (10, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            10,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            10,
            Weapons.LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            10,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_117_AGM_65G = (10, Weapons.LAU_117_AGM_65G)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            10,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (
            10,
            Weapons.GBU_12___500lb_Laser_Guided_Bomb,
        )
        AGM_154C___JSOW_Unitary_BROACH = (10, Weapons.AGM_154C___JSOW_Unitary_BROACH)
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            10,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            10,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            10,
            Weapons.AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )

    class Pylon11:
        AIM_9M_Sidewinder_IR_AAM = (11, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (11, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (11, Weapons.AIM_9X_Sidewinder_IR_AAM)
        Smokewinder___red = (11, Weapons.Smokewinder___red)
        Smokewinder___green = (11, Weapons.Smokewinder___green)
        Smokewinder___blue = (11, Weapons.Smokewinder___blue)
        Smokewinder___white = (11, Weapons.Smokewinder___white)
        Smokewinder___yellow = (11, Weapons.Smokewinder___yellow)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (11, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}

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
    task_default = task.CAS


@planemod
class VSN_F35C_AG(PlaneType):
    id = "VSN_F35C_AG"
    flyable = True
    height = 4.39
    width = 10.7
    length = 15.7
    fuel_max = 8278
    max_speed = 1975.68
    chaff = 120
    flare = 120
    charge_total = 240
    chaff_charge_size = 1
    flare_charge_size = 1
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}

    livery_name = "VSN_F35C_AG"  # from type

    class Pylon1:
        AIM_9M_Sidewinder_IR_AAM = (1, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (1, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (1, Weapons.AIM_9X_Sidewinder_IR_AAM)
        Smokewinder___red = (1, Weapons.Smokewinder___red)
        Smokewinder___green = (1, Weapons.Smokewinder___green)
        Smokewinder___blue = (1, Weapons.Smokewinder___blue)
        Smokewinder___white = (1, Weapons.Smokewinder___white)
        Smokewinder___yellow = (1, Weapons.Smokewinder___yellow)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (1, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

    class Pylon2:
        AIM_9M_Sidewinder_IR_AAM = (2, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (2, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (2, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            2,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        Mk_82___500lb_GP_Bomb_LD = (2, Weapons.Mk_82___500lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            2,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (2, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        CBU_97___10_x_SFW_Cluster_Bomb = (2, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            2,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            2,
            Weapons.LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            2,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_117_AGM_65G = (2, Weapons.LAU_117_AGM_65G)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            2,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (2, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        AGM_154C___JSOW_Unitary_BROACH = (2, Weapons.AGM_154C___JSOW_Unitary_BROACH)
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            2,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            2,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            2,
            Weapons.AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )

    class Pylon3:
        AIM_9M_Sidewinder_IR_AAM = (3, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (3, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (3, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            3,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        LAU_115_2_LAU_127_AIM_120C = (3, Weapons.LAU_115_2_LAU_127_AIM_120C)
        GBU_10___2000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_16___1000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        Mk_82___500lb_GP_Bomb_LD = (3, Weapons.Mk_82___500lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            3,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (3, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_83___1000lb_GP_Bombs_LD = (
            3,
            Weapons.MER2_with_2_x_Mk_83___1000lb_GP_Bombs_LD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (3, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        CBU_97___10_x_SFW_Cluster_Bomb = (3, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            3,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            3,
            Weapons.LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            3,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_117_AGM_65G = (3, Weapons.LAU_117_AGM_65G)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            3,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (3, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        AGM_154C___JSOW_Unitary_BROACH = (3, Weapons.AGM_154C___JSOW_Unitary_BROACH)
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            3,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            3,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        AGM_114K_Hellfire = (3, Weapons.AGM_114K_Hellfire)
        AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            3,
            Weapons.AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        Fuel_tank_610_gal__ = (3, VSNF35_Weapons.Fuel_tank_610_gal__)

    class Pylon4:
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            4,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (4, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_16___1000lb_Laser_Guided_Bomb = (
            4,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        Mk_84___2000lb_GP_Bomb_LD = (4, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        AGM_154C___JSOW_Unitary_BROACH = (4, Weapons.AGM_154C___JSOW_Unitary_BROACH)
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            4,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            4,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        CBU_97___10_x_SFW_Cluster_Bomb = (4, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)

    class Pylon5:
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            5,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )

    class Pylon6:
        Smoke_Generator___red_ = (6, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (6, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (6, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (6, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (6, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (6, Weapons.Smoke_Generator___orange_)
        F35_GAU_22_gun_pod = (6, VSNF35_Weapons.F35_GAU_22_gun_pod)

    # ERRR <CLEAN>

    class Pylon7:
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            7,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )

    class Pylon8:
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            8,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (8, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_16___1000lb_Laser_Guided_Bomb = (
            8,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        Mk_84___2000lb_GP_Bomb_LD = (8, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        AGM_154C___JSOW_Unitary_BROACH = (8, Weapons.AGM_154C___JSOW_Unitary_BROACH)
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            8,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            8,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        CBU_97___10_x_SFW_Cluster_Bomb = (8, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)

    class Pylon9:
        AIM_9M_Sidewinder_IR_AAM = (9, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (9, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (9, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            9,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        LAU_115_2_LAU_127_AIM_120C = (9, Weapons.LAU_115_2_LAU_127_AIM_120C)
        GBU_10___2000lb_Laser_Guided_Bomb = (
            9,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_16___1000lb_Laser_Guided_Bomb = (
            9,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb = (
            9,
            Weapons.GBU_24A_B_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        Mk_82___500lb_GP_Bomb_LD = (9, Weapons.Mk_82___500lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            9,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (9, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_83___1000lb_GP_Bombs_LD = (
            9,
            Weapons.MER2_with_2_x_Mk_83___1000lb_GP_Bombs_LD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (9, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        CBU_97___10_x_SFW_Cluster_Bomb = (9, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            9,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            9,
            Weapons.LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            9,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_117_AGM_65G = (9, Weapons.LAU_117_AGM_65G)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            9,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (9, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        AGM_154C___JSOW_Unitary_BROACH = (9, Weapons.AGM_154C___JSOW_Unitary_BROACH)
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            9,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            9,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        AGM_114K_Hellfire = (9, Weapons.AGM_114K_Hellfire)
        AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            9,
            Weapons.AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )
        Fuel_tank_610_gal__ = (9, VSNF35_Weapons.Fuel_tank_610_gal__)

    class Pylon10:
        AIM_9M_Sidewinder_IR_AAM = (10, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (10, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (10, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            10,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        Mk_82___500lb_GP_Bomb_LD = (10, Weapons.Mk_82___500lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            10,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (10, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        CBU_97___10_x_SFW_Cluster_Bomb = (10, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            10,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            10,
            Weapons.LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            10,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_117_AGM_65G = (10, Weapons.LAU_117_AGM_65G)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            10,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (
            10,
            Weapons.GBU_12___500lb_Laser_Guided_Bomb,
        )
        AGM_154C___JSOW_Unitary_BROACH = (10, Weapons.AGM_154C___JSOW_Unitary_BROACH)
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            10,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            10,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_ = (
            10,
            Weapons.AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_,
        )

    class Pylon11:
        AIM_9M_Sidewinder_IR_AAM = (11, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (11, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (11, Weapons.AIM_9X_Sidewinder_IR_AAM)
        Smokewinder___red = (11, Weapons.Smokewinder___red)
        Smokewinder___green = (11, Weapons.Smokewinder___green)
        Smokewinder___blue = (11, Weapons.Smokewinder___blue)
        Smokewinder___white = (11, Weapons.Smokewinder___white)
        Smokewinder___yellow = (11, Weapons.Smokewinder___yellow)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (11, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

    class Pylon12:
        L005_Sorbtsiya_ECM_pod__left_ = (12, Weapons.L005_Sorbtsiya_ECM_pod__left_)
        Smoke_Generator___red_ = (12, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (12, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (12, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (12, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (12, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (12, Weapons.Smoke_Generator___orange_)

    class Pylon13:
        L_081_Fantasmagoria_ELINT_pod = (13, Weapons.L_081_Fantasmagoria_ELINT_pod)
        Smoke_Generator___red_ = (13, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (13, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (13, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (13, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (13, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (13, Weapons.Smoke_Generator___orange_)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13}

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
    task_default = task.CAS
