from dcs import task
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

from game.modsupport import planemod
from pydcs_extensions.weapon_injector import inject_weapons


class WeaponsSEM:
    Fuel_Tank_1100_Liter = {
        "clsid": "{SEM1100_PTB}",
        "name": "Fuel Tank 1100 Liter",
        "weight": 1150,
    }
    Fuel_Tank_625_Liter = {
        "clsid": "{SEM625_PTB}",
        "name": "Fuel Tank 625 Liter",
        "weight": 1150,
    }


inject_weapons(WeaponsSEM)


@planemod
class VSN_SEM(PlaneType):
    id = "VSN_SEM"
    flyable = True
    height = 4
    width = 13.05
    length = 18
    fuel_max = 6103
    max_speed = 2649.996
    chaff = 90
    flare = 45
    charge_total = 180
    chaff_charge_size = 1
    flare_charge_size = 2
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    livery_name = "VSN_SEM"  # from type

    class Pylon1:
        Smokewinder___red = (1, Weapons.Smokewinder___red)
        Smokewinder___green = (1, Weapons.Smokewinder___green)
        Smokewinder___blue = (1, Weapons.Smokewinder___blue)
        Smokewinder___white = (1, Weapons.Smokewinder___white)
        Smokewinder___yellow = (1, Weapons.Smokewinder___yellow)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (1, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        Mk_81___250lb_GP_Bomb_LD = (1, Weapons.Mk_81___250lb_GP_Bomb_LD)
        Mk_82___500lb_GP_Bomb_LD = (1, Weapons.Mk_82___500lb_GP_Bomb_LD)
        R550_Magic_2_IR_AAM = (1, Weapons.R550_Magic_2_IR_AAM)
        LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            1,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE_,
        )
        ALQ_131___ECM_Pod = (1, Weapons.ALQ_131___ECM_Pod)
        AIM_9M_Sidewinder_IR_AAM = (1, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (1, Weapons.AIM_9P_Sidewinder_IR_AAM)

    class Pylon2:
        AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            2,
            Weapons.AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (2, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            2,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE_,
        )
        Mk_81___250lb_GP_Bomb_LD = (2, Weapons.Mk_81___250lb_GP_Bomb_LD)
        Mk_82___500lb_GP_Bomb_LD = (2, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Fuel_Tank_1100_Liter = (2, WeaponsSEM.Fuel_Tank_1100_Liter)
        Fuel_Tank_625_Liter = (2, WeaponsSEM.Fuel_Tank_625_Liter)

    # ERRR <CLEAN>

    class Pylon5:
        L_081_Fantasmagoria_ELINT_pod = (5, Weapons.L_081_Fantasmagoria_ELINT_pod)

    class Pylon6:
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            6,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            6,
            Weapons.AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )

    # ERRR <CLEAN>

    class Pylon10:
        AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            10,
            Weapons.AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (
            10,
            Weapons.GBU_12___500lb_Laser_Guided_Bomb,
        )
        LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            10,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE_,
        )
        Mk_81___250lb_GP_Bomb_LD = (10, Weapons.Mk_81___250lb_GP_Bomb_LD)
        Mk_82___500lb_GP_Bomb_LD = (10, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Fuel_Tank_1100_Liter = (10, WeaponsSEM.Fuel_Tank_1100_Liter)
        Fuel_Tank_625_Liter = (10, WeaponsSEM.Fuel_Tank_625_Liter)

    class Pylon11:
        Smokewinder___red = (11, Weapons.Smokewinder___red)
        Smokewinder___green = (11, Weapons.Smokewinder___green)
        Smokewinder___blue = (11, Weapons.Smokewinder___blue)
        Smokewinder___white = (11, Weapons.Smokewinder___white)
        Smokewinder___yellow = (11, Weapons.Smokewinder___yellow)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (11, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        Mk_81___250lb_GP_Bomb_LD = (11, Weapons.Mk_81___250lb_GP_Bomb_LD)
        Mk_82___500lb_GP_Bomb_LD = (11, Weapons.Mk_82___500lb_GP_Bomb_LD)
        R550_Magic_2_IR_AAM = (11, Weapons.R550_Magic_2_IR_AAM)
        LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            11,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE_,
        )
        ALQ_131___ECM_Pod = (11, Weapons.ALQ_131___ECM_Pod)
        AIM_9M_Sidewinder_IR_AAM = (11, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (11, Weapons.AIM_9P_Sidewinder_IR_AAM)

    pylons = {1, 2, 3, 5, 6, 9, 10, 11}

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
    task_default = task.FighterSweep
