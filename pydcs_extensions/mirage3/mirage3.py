from enum import Enum

from dcs import task

from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

from game.modsupport import planemod
from pydcs_extensions.weapon_injector import inject_weapons


class WeaponsMirage3:
    M3_1000_Liter_MK82_4 = {
        "clsid": "{VSN_M3PTBL_MK82_4}",
        "name": "M3 1000 Liter MK82*4",
        "weight": 1004,
    }
    M3_1000_Liter_MK82_4_ = {
        "clsid": "{VSN_M3PTBR_MK82_4}",
        "name": "M3 1000 Liter MK82*4",
        "weight": 1004,
    }
    M3_Fuel_Tank_1300_Liter = {
        "clsid": "{VSN_M3C13_PTB}",
        "name": "M3 Fuel Tank 1300 Liter",
        "weight": 1172,
    }
    M3_Fuel_Tank_1700_Liter = {
        "clsid": "{VSN_M3C17_PTB}",
        "name": "M3 Fuel Tank 1700 Liter",
        "weight": 1492,
    }
    M3_Fuel_Tank_800_Liter = {
        "clsid": "{VSN_M3C80_PTB}",
        "name": "M3 Fuel Tank 800 Liter",
        "weight": 740,
    }
    M3_superSonic_Tank_1000_Liter = {
        "clsid": "{VSN_M3C10_PTB}",
        "name": "M3 superSonic Tank 1000 Liter",
        "weight": 900,
    }
    M3_Tank_1000_Liter_MK82_4 = {
        "clsid": "{VSN_M3C10L_MK82_PTB}",
        "name": "M3 Tank 1000 Liter MK82*4",
        "weight": 900,
    }
    M3_Tank_1000_Liter_MK82_4_ = {
        "clsid": "{VSN_M3C10R_MK82_PTB}",
        "name": "M3 Tank 1000 Liter MK82*4",
        "weight": 900,
    }


inject_weapons(WeaponsMirage3)


@planemod
class VSN_MirageIII(PlaneType):
    id = "VSN_MirageIII"
    flyable = True
    height = 4.5
    width = 8.22
    length = 15.03
    fuel_max = 2150
    max_speed = 2450.088
    chaff = 90
    flare = 45
    charge_total = 180
    chaff_charge_size = 1
    flare_charge_size = 2
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    livery_name = "VSN_MIRAGEIII"  # from livery_entry

    class Pylon1:
        Mk_81___250lb_GP_Bomb_LD = (1, Weapons.Mk_81___250lb_GP_Bomb_LD)
        # ERRR {MK-81SE}
        Mk_82___500lb_GP_Bomb_LD = (1, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (1, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        AIM_9M_Sidewinder_IR_AAM = (1, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (1, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (1, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        Smokewinder___red = (1, Weapons.Smokewinder___red)
        Smokewinder___green = (1, Weapons.Smokewinder___green)
        Smokewinder___blue = (1, Weapons.Smokewinder___blue)
        Smokewinder___white = (1, Weapons.Smokewinder___white)
        Smokewinder___yellow = (1, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (1, Weapons.Smokewinder___orange)
        R550_Magic_2_IR_AAM = (1, Weapons.R550_Magic_2_IR_AAM)

    # ERRR {Barax}
    # ERRR {Phimat}
    # ERRR <CLEAN>

    class Pylon2:
        Mk_81___250lb_GP_Bomb_LD = (2, Weapons.Mk_81___250lb_GP_Bomb_LD)
        # ERRR {MK-81SE}
        Mk_82___500lb_GP_Bomb_LD = (2, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (2, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_83___1000lb_GP_Bomb_LD = (2, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (2, Weapons.M117___750lb_GP_Bomb_LD)
        BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD = (
            2,
            Weapons.BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE_ = (
            2,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE_,
        )
        UB_32A___32_x_UnGd_Rkts__57_mm_S_5KO_HEAT_Frag = (
            2,
            Weapons.UB_32A___32_x_UnGd_Rkts__57_mm_S_5KO_HEAT_Frag,
        )
        LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE = (
            2,
            Weapons.LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_M156_SM = (
            2,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_M156_SM,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE = (
            2,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT = (
            2,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_M156_SM = (
            2,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_M156_SM,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE = (
            2,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT = (
            2,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE = (
            2,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT = (
            2,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT,
        )
        M3_Fuel_Tank_1300_Liter = (2, WeaponsMirage3.M3_Fuel_Tank_1300_Liter)
        M3_Fuel_Tank_1700_Liter = (2, WeaponsMirage3.M3_Fuel_Tank_1700_Liter)
        M3_superSonic_Tank_1000_Liter = (
            2,
            WeaponsMirage3.M3_superSonic_Tank_1000_Liter,
        )

    # ERRR <CLEAN>

    class Pylon3:
        Mk_81___250lb_GP_Bomb_LD = (3, Weapons.Mk_81___250lb_GP_Bomb_LD)
        # ERRR {MK-81SE}
        Mk_82___500lb_GP_Bomb_LD = (3, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (3, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        GBU_12___500lb_Laser_Guided_Bomb = (3, Weapons.GBU_12___500lb_Laser_Guided_Bomb)

    # ERRR <CLEAN>

    class Pylon4:
        Mk_81___250lb_GP_Bomb_LD = (4, Weapons.Mk_81___250lb_GP_Bomb_LD)
        # ERRR {MK-81SE}
        Mk_82___500lb_GP_Bomb_LD = (4, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (4, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)

    # ERRR <CLEAN>

    class Pylon5:
        L005_Sorbtsiya_ECM_pod__left_ = (5, Weapons.L005_Sorbtsiya_ECM_pod__left_)
        L_081_Fantasmagoria_ELINT_pod = (5, Weapons.L_081_Fantasmagoria_ELINT_pod)
        Smoke_Generator___red_ = (5, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (5, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (5, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (5, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (5, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (5, Weapons.Smoke_Generator___orange_)

    # ERRR <CLEAN>

    class Pylon6:
        Mk_81___250lb_GP_Bomb_LD = (6, Weapons.Mk_81___250lb_GP_Bomb_LD)
        # ERRR {MK-81SE}
        Mk_82___500lb_GP_Bomb_LD = (6, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (6, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_83___1000lb_GP_Bomb_LD = (6, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (6, Weapons.M117___750lb_GP_Bomb_LD)
        S530D = (6, Weapons.S530D)
        M3_Fuel_Tank_1300_Liter = (6, WeaponsMirage3.M3_Fuel_Tank_1300_Liter)
        M3_Fuel_Tank_800_Liter = (6, WeaponsMirage3.M3_Fuel_Tank_800_Liter)
        BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD = (
            6,
            Weapons.BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        BLG_66_AC_Belouga = (6, Weapons.BLG_66_AC_Belouga)

    # ERRR <CLEAN>

    class Pylon7:
        L005_Sorbtsiya_ECM_pod__left_ = (7, Weapons.L005_Sorbtsiya_ECM_pod__left_)
        L_081_Fantasmagoria_ELINT_pod = (7, Weapons.L_081_Fantasmagoria_ELINT_pod)
        Smoke_Generator___red_ = (7, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (7, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (7, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (7, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (7, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (7, Weapons.Smoke_Generator___orange_)

    # ERRR <CLEAN>

    class Pylon8:
        Mk_81___250lb_GP_Bomb_LD = (8, Weapons.Mk_81___250lb_GP_Bomb_LD)
        # ERRR {MK-81SE}
        Mk_82___500lb_GP_Bomb_LD = (8, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (8, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)

    # ERRR <CLEAN>

    class Pylon9:
        Mk_81___250lb_GP_Bomb_LD = (9, Weapons.Mk_81___250lb_GP_Bomb_LD)
        # ERRR {MK-81SE}
        Mk_82___500lb_GP_Bomb_LD = (9, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (9, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        GBU_12___500lb_Laser_Guided_Bomb = (9, Weapons.GBU_12___500lb_Laser_Guided_Bomb)

    # ERRR <CLEAN>

    class Pylon10:
        Mk_81___250lb_GP_Bomb_LD = (10, Weapons.Mk_81___250lb_GP_Bomb_LD)
        # ERRR {MK-81SE}
        Mk_82___500lb_GP_Bomb_LD = (10, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            10,
            Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (10, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (10, Weapons.M117___750lb_GP_Bomb_LD)
        BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD = (
            10,
            Weapons.BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE_ = (
            10,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE_,
        )
        UB_32A___32_x_UnGd_Rkts__57_mm_S_5KO_HEAT_Frag = (
            10,
            Weapons.UB_32A___32_x_UnGd_Rkts__57_mm_S_5KO_HEAT_Frag,
        )
        LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE = (
            10,
            Weapons.LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_M156_SM = (
            10,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_M156_SM,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE = (
            10,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT = (
            10,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_M156_SM = (
            10,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_M156_SM,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE = (
            10,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT = (
            10,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE = (
            10,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT = (
            10,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT,
        )
        M3_Fuel_Tank_1300_Liter = (10, WeaponsMirage3.M3_Fuel_Tank_1300_Liter)
        M3_Fuel_Tank_1700_Liter = (10, WeaponsMirage3.M3_Fuel_Tank_1700_Liter)
        M3_superSonic_Tank_1000_Liter = (
            10,
            WeaponsMirage3.M3_superSonic_Tank_1000_Liter,
        )

    # ERRR <CLEAN>

    class Pylon11:
        Mk_81___250lb_GP_Bomb_LD = (11, Weapons.Mk_81___250lb_GP_Bomb_LD)
        # ERRR {MK-81SE}
        Mk_82___500lb_GP_Bomb_LD = (11, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            11,
            Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        AIM_9M_Sidewinder_IR_AAM = (11, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (11, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (11, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        Smokewinder___red = (11, Weapons.Smokewinder___red)
        Smokewinder___green = (11, Weapons.Smokewinder___green)
        Smokewinder___blue = (11, Weapons.Smokewinder___blue)
        Smokewinder___white = (11, Weapons.Smokewinder___white)
        Smokewinder___yellow = (11, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (11, Weapons.Smokewinder___orange)
        R550_Magic_2_IR_AAM = (11, Weapons.R550_Magic_2_IR_AAM)

    # ERRR {Barax}
    # ERRR {Phimat}
    # ERRR <CLEAN>

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
    task_default = task.FighterSweep


@planemod
class VSN_MirageIII_AG(PlaneType):
    id = "VSN_MirageIII_AG"
    flyable = True
    height = 4.5
    width = 8.22
    length = 15.03
    fuel_max = 2150
    max_speed = 2450.088
    chaff = 90
    flare = 45
    charge_total = 180
    chaff_charge_size = 1
    flare_charge_size = 2
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    livery_name = "VSN_MIRAGEIII"  # from livery_entry

    class Pylon1:
        Mk_81___250lb_GP_Bomb_LD = (1, Weapons.Mk_81___250lb_GP_Bomb_LD)
        # ERRR {MK-81SE}
        Mk_82___500lb_GP_Bomb_LD = (1, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (1, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        AIM_9M_Sidewinder_IR_AAM = (1, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (1, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (1, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        Smokewinder___red = (1, Weapons.Smokewinder___red)
        Smokewinder___green = (1, Weapons.Smokewinder___green)
        Smokewinder___blue = (1, Weapons.Smokewinder___blue)
        Smokewinder___white = (1, Weapons.Smokewinder___white)
        Smokewinder___yellow = (1, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (1, Weapons.Smokewinder___orange)
        R550_Magic_2_IR_AAM = (1, Weapons.R550_Magic_2_IR_AAM)

    # ERRR {Barax}
    # ERRR {Phimat}
    # ERRR <CLEAN>

    class Pylon2:
        Mk_81___250lb_GP_Bomb_LD = (2, Weapons.Mk_81___250lb_GP_Bomb_LD)
        # ERRR {MK-81SE}
        Mk_82___500lb_GP_Bomb_LD = (2, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (2, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_83___1000lb_GP_Bomb_LD = (2, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (2, Weapons.M117___750lb_GP_Bomb_LD)
        BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD = (
            2,
            Weapons.BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE_ = (
            2,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE_,
        )
        UB_32A___32_x_UnGd_Rkts__57_mm_S_5KO_HEAT_Frag = (
            2,
            Weapons.UB_32A___32_x_UnGd_Rkts__57_mm_S_5KO_HEAT_Frag,
        )
        LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE = (
            2,
            Weapons.LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_M156_SM = (
            2,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_M156_SM,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE = (
            2,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT = (
            2,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_M156_SM = (
            2,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_M156_SM,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE = (
            2,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT = (
            2,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE = (
            2,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT = (
            2,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT,
        )
        M3_Fuel_Tank_1300_Liter = (2, WeaponsMirage3.M3_Fuel_Tank_1300_Liter)
        M3_Fuel_Tank_1700_Liter = (2, WeaponsMirage3.M3_Fuel_Tank_1700_Liter)
        M3_superSonic_Tank_1000_Liter = (
            2,
            WeaponsMirage3.M3_superSonic_Tank_1000_Liter,
        )
        M3_Tank_1000_Liter_MK82_4 = (2, WeaponsMirage3.M3_Tank_1000_Liter_MK82_4)

    # ERRR <CLEAN>

    class Pylon3:
        Mk_81___250lb_GP_Bomb_LD = (3, Weapons.Mk_81___250lb_GP_Bomb_LD)
        # ERRR {MK-81SE}
        Mk_82___500lb_GP_Bomb_LD = (3, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (3, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        GBU_12___500lb_Laser_Guided_Bomb = (3, Weapons.GBU_12___500lb_Laser_Guided_Bomb)

    # ERRR <CLEAN>

    class Pylon4:
        Mk_81___250lb_GP_Bomb_LD = (4, Weapons.Mk_81___250lb_GP_Bomb_LD)
        # ERRR {MK-81SE}
        Mk_82___500lb_GP_Bomb_LD = (4, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (4, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)

    # ERRR <CLEAN>

    class Pylon6:
        L005_Sorbtsiya_ECM_pod__left_ = (6, Weapons.L005_Sorbtsiya_ECM_pod__left_)
        L_081_Fantasmagoria_ELINT_pod = (6, Weapons.L_081_Fantasmagoria_ELINT_pod)
        Smoke_Generator___red_ = (6, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (6, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (6, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (6, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (6, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (6, Weapons.Smoke_Generator___orange_)

    # ERRR <CLEAN>

    class Pylon7:
        Mk_81___250lb_GP_Bomb_LD = (7, Weapons.Mk_81___250lb_GP_Bomb_LD)
        # ERRR {MK-81SE}
        Mk_82___500lb_GP_Bomb_LD = (7, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (7, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_83___1000lb_GP_Bomb_LD = (7, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (7, Weapons.M117___750lb_GP_Bomb_LD)
        S530D = (7, Weapons.S530D)
        M3_Fuel_Tank_1300_Liter = (7, WeaponsMirage3.M3_Fuel_Tank_1300_Liter)
        M3_Fuel_Tank_800_Liter = (7, WeaponsMirage3.M3_Fuel_Tank_800_Liter)
        BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            Weapons.BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        BLG_66_AC_Belouga = (7, Weapons.BLG_66_AC_Belouga)

    # ERRR <CLEAN>

    class Pylon8:
        L005_Sorbtsiya_ECM_pod__left_ = (8, Weapons.L005_Sorbtsiya_ECM_pod__left_)
        L_081_Fantasmagoria_ELINT_pod = (8, Weapons.L_081_Fantasmagoria_ELINT_pod)
        Smoke_Generator___red_ = (8, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (8, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (8, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (8, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (8, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (8, Weapons.Smoke_Generator___orange_)

    # ERRR <CLEAN>

    class Pylon10:
        Mk_81___250lb_GP_Bomb_LD = (10, Weapons.Mk_81___250lb_GP_Bomb_LD)
        # ERRR {MK-81SE}
        Mk_82___500lb_GP_Bomb_LD = (10, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            10,
            Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )

    # ERRR <CLEAN>

    class Pylon11:
        Mk_81___250lb_GP_Bomb_LD = (11, Weapons.Mk_81___250lb_GP_Bomb_LD)
        # ERRR {MK-81SE}
        Mk_82___500lb_GP_Bomb_LD = (11, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            11,
            Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (
            11,
            Weapons.GBU_12___500lb_Laser_Guided_Bomb,
        )

    # ERRR <CLEAN>

    class Pylon12:
        Mk_81___250lb_GP_Bomb_LD = (12, Weapons.Mk_81___250lb_GP_Bomb_LD)
        # ERRR {MK-81SE}
        Mk_82___500lb_GP_Bomb_LD = (12, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            12,
            Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (12, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (12, Weapons.M117___750lb_GP_Bomb_LD)
        BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD = (
            12,
            Weapons.BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE_ = (
            12,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE_,
        )
        UB_32A___32_x_UnGd_Rkts__57_mm_S_5KO_HEAT_Frag = (
            12,
            Weapons.UB_32A___32_x_UnGd_Rkts__57_mm_S_5KO_HEAT_Frag,
        )
        LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE = (
            12,
            Weapons.LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_M156_SM = (
            12,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_M156_SM,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE = (
            12,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT = (
            12,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_M156_SM = (
            12,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_M156_SM,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE = (
            12,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT = (
            12,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE = (
            12,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT = (
            12,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT,
        )
        M3_Fuel_Tank_1300_Liter = (12, WeaponsMirage3.M3_Fuel_Tank_1300_Liter)
        M3_Fuel_Tank_1700_Liter = (12, WeaponsMirage3.M3_Fuel_Tank_1700_Liter)
        M3_superSonic_Tank_1000_Liter = (
            12,
            WeaponsMirage3.M3_superSonic_Tank_1000_Liter,
        )
        M3_Tank_1000_Liter_MK82_4_ = (12, WeaponsMirage3.M3_Tank_1000_Liter_MK82_4_)

    # ERRR <CLEAN>

    class Pylon13:
        Mk_81___250lb_GP_Bomb_LD = (13, Weapons.Mk_81___250lb_GP_Bomb_LD)
        # ERRR {MK-81SE}
        Mk_82___500lb_GP_Bomb_LD = (13, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            13,
            Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        AIM_9M_Sidewinder_IR_AAM = (13, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (13, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (13, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        Smokewinder___red = (13, Weapons.Smokewinder___red)
        Smokewinder___green = (13, Weapons.Smokewinder___green)
        Smokewinder___blue = (13, Weapons.Smokewinder___blue)
        Smokewinder___white = (13, Weapons.Smokewinder___white)
        Smokewinder___yellow = (13, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (13, Weapons.Smokewinder___orange)
        R550_Magic_2_IR_AAM = (13, Weapons.R550_Magic_2_IR_AAM)

    # ERRR {Barax}
    # ERRR {Phimat}
    # ERRR <CLEAN>

    pylons = {1, 2, 3, 4, 6, 7, 8, 10, 11, 12, 13}

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


@planemod
class VSN_Kfir(PlaneType):
    id = "VSN_Kfir"
    flyable = True
    height = 4.5
    width = 8.22
    length = 15.03
    fuel_max = 2150
    max_speed = 2450.088
    chaff = 90
    flare = 45
    charge_total = 180
    chaff_charge_size = 1
    flare_charge_size = 2
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    livery_name = "VSN_KFIR"  # from livery_entry

    class Pylon1:
        Mk_81___250lb_GP_Bomb_LD = (1, Weapons.Mk_81___250lb_GP_Bomb_LD)
        # ERRR {MK-81SE}
        Mk_82___500lb_GP_Bomb_LD = (1, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (1, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        AIM_9M_Sidewinder_IR_AAM = (1, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (1, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (1, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        Smokewinder___red = (1, Weapons.Smokewinder___red)
        Smokewinder___green = (1, Weapons.Smokewinder___green)
        Smokewinder___blue = (1, Weapons.Smokewinder___blue)
        Smokewinder___white = (1, Weapons.Smokewinder___white)
        Smokewinder___yellow = (1, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (1, Weapons.Smokewinder___orange)
        R550_Magic_2_IR_AAM = (1, Weapons.R550_Magic_2_IR_AAM)

    # ERRR {Barax}
    # ERRR {Phimat}
    # ERRR <CLEAN>

    class Pylon2:
        Mk_81___250lb_GP_Bomb_LD = (2, Weapons.Mk_81___250lb_GP_Bomb_LD)
        # ERRR {MK-81SE}
        Mk_82___500lb_GP_Bomb_LD = (2, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (2, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_83___1000lb_GP_Bomb_LD = (2, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (2, Weapons.M117___750lb_GP_Bomb_LD)
        BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD = (
            2,
            Weapons.BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE_ = (
            2,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE_,
        )
        UB_32A___32_x_UnGd_Rkts__57_mm_S_5KO_HEAT_Frag = (
            2,
            Weapons.UB_32A___32_x_UnGd_Rkts__57_mm_S_5KO_HEAT_Frag,
        )
        LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE = (
            2,
            Weapons.LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_M156_SM = (
            2,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_M156_SM,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE = (
            2,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT = (
            2,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_M156_SM = (
            2,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_M156_SM,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE = (
            2,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT = (
            2,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE = (
            2,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT = (
            2,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT,
        )
        M3_Fuel_Tank_1300_Liter = (2, WeaponsMirage3.M3_Fuel_Tank_1300_Liter)
        M3_Fuel_Tank_1700_Liter = (2, WeaponsMirage3.M3_Fuel_Tank_1700_Liter)
        M3_superSonic_Tank_1000_Liter = (
            2,
            WeaponsMirage3.M3_superSonic_Tank_1000_Liter,
        )
        M3_Tank_1000_Liter_MK82_4 = (2, WeaponsMirage3.M3_Tank_1000_Liter_MK82_4)

    # ERRR <CLEAN>

    class Pylon3:
        Mk_81___250lb_GP_Bomb_LD = (3, Weapons.Mk_81___250lb_GP_Bomb_LD)
        # ERRR {MK-81SE}
        Mk_82___500lb_GP_Bomb_LD = (3, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (3, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        GBU_12___500lb_Laser_Guided_Bomb = (3, Weapons.GBU_12___500lb_Laser_Guided_Bomb)

    # ERRR <CLEAN>

    class Pylon4:
        Mk_81___250lb_GP_Bomb_LD = (4, Weapons.Mk_81___250lb_GP_Bomb_LD)
        # ERRR {MK-81SE}
        Mk_82___500lb_GP_Bomb_LD = (4, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (4, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)

    # ERRR <CLEAN>

    class Pylon6:
        L005_Sorbtsiya_ECM_pod__left_ = (6, Weapons.L005_Sorbtsiya_ECM_pod__left_)
        L_081_Fantasmagoria_ELINT_pod = (6, Weapons.L_081_Fantasmagoria_ELINT_pod)
        Smoke_Generator___red_ = (6, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (6, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (6, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (6, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (6, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (6, Weapons.Smoke_Generator___orange_)

    # ERRR <CLEAN>

    class Pylon7:
        Mk_81___250lb_GP_Bomb_LD = (7, Weapons.Mk_81___250lb_GP_Bomb_LD)
        # ERRR {MK-81SE}
        Mk_82___500lb_GP_Bomb_LD = (7, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (7, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_83___1000lb_GP_Bomb_LD = (7, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (7, Weapons.M117___750lb_GP_Bomb_LD)
        S530D = (7, Weapons.S530D)
        M3_Fuel_Tank_1300_Liter = (7, WeaponsMirage3.M3_Fuel_Tank_1300_Liter)
        M3_Fuel_Tank_800_Liter = (7, WeaponsMirage3.M3_Fuel_Tank_800_Liter)
        BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            Weapons.BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        BLG_66_AC_Belouga = (7, Weapons.BLG_66_AC_Belouga)

    # ERRR <CLEAN>

    class Pylon8:
        L005_Sorbtsiya_ECM_pod__left_ = (8, Weapons.L005_Sorbtsiya_ECM_pod__left_)
        L_081_Fantasmagoria_ELINT_pod = (8, Weapons.L_081_Fantasmagoria_ELINT_pod)
        Smoke_Generator___red_ = (8, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (8, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (8, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (8, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (8, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (8, Weapons.Smoke_Generator___orange_)

    # ERRR <CLEAN>

    class Pylon10:
        Mk_81___250lb_GP_Bomb_LD = (10, Weapons.Mk_81___250lb_GP_Bomb_LD)
        # ERRR {MK-81SE}
        Mk_82___500lb_GP_Bomb_LD = (10, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            10,
            Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )

    # ERRR <CLEAN>

    class Pylon11:
        Mk_81___250lb_GP_Bomb_LD = (11, Weapons.Mk_81___250lb_GP_Bomb_LD)
        # ERRR {MK-81SE}
        Mk_82___500lb_GP_Bomb_LD = (11, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            11,
            Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (
            11,
            Weapons.GBU_12___500lb_Laser_Guided_Bomb,
        )

    # ERRR <CLEAN>

    class Pylon12:
        Mk_81___250lb_GP_Bomb_LD = (12, Weapons.Mk_81___250lb_GP_Bomb_LD)
        # ERRR {MK-81SE}
        Mk_82___500lb_GP_Bomb_LD = (12, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            12,
            Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (12, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (12, Weapons.M117___750lb_GP_Bomb_LD)
        BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD = (
            12,
            Weapons.BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE_ = (
            12,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE_,
        )
        UB_32A___32_x_UnGd_Rkts__57_mm_S_5KO_HEAT_Frag = (
            12,
            Weapons.UB_32A___32_x_UnGd_Rkts__57_mm_S_5KO_HEAT_Frag,
        )
        LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE = (
            12,
            Weapons.LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_M156_SM = (
            12,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_M156_SM,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE = (
            12,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT = (
            12,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_M156_SM = (
            12,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_M156_SM,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE = (
            12,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT = (
            12,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE = (
            12,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT = (
            12,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT,
        )
        M3_Fuel_Tank_1300_Liter = (12, WeaponsMirage3.M3_Fuel_Tank_1300_Liter)
        M3_Fuel_Tank_1700_Liter = (12, WeaponsMirage3.M3_Fuel_Tank_1700_Liter)
        M3_superSonic_Tank_1000_Liter = (
            12,
            WeaponsMirage3.M3_superSonic_Tank_1000_Liter,
        )
        M3_Tank_1000_Liter_MK82_4_ = (12, WeaponsMirage3.M3_Tank_1000_Liter_MK82_4_)

    # ERRR <CLEAN>

    class Pylon13:
        Mk_81___250lb_GP_Bomb_LD = (13, Weapons.Mk_81___250lb_GP_Bomb_LD)
        # ERRR {MK-81SE}
        Mk_82___500lb_GP_Bomb_LD = (13, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            13,
            Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        AIM_9M_Sidewinder_IR_AAM = (13, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (13, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (13, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        Smokewinder___red = (13, Weapons.Smokewinder___red)
        Smokewinder___green = (13, Weapons.Smokewinder___green)
        Smokewinder___blue = (13, Weapons.Smokewinder___blue)
        Smokewinder___white = (13, Weapons.Smokewinder___white)
        Smokewinder___yellow = (13, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (13, Weapons.Smokewinder___orange)
        R550_Magic_2_IR_AAM = (13, Weapons.R550_Magic_2_IR_AAM)

    # ERRR {Barax}
    # ERRR {Phimat}
    # ERRR <CLEAN>

    pylons = {1, 2, 3, 4, 6, 7, 8, 10, 11, 12, 13}

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


@planemod
class VSN_Mirage5(PlaneType):
    id = "VSN_Mirage5"
    flyable = True
    height = 4.5
    width = 8.22
    length = 15.03
    fuel_max = 2150
    max_speed = 2450.088
    chaff = 90
    flare = 45
    charge_total = 180
    chaff_charge_size = 1
    flare_charge_size = 2
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    livery_name = "VSN_MIRAGE5"  # from livery_entry

    class Pylon1:
        Mk_81___250lb_GP_Bomb_LD = (1, Weapons.Mk_81___250lb_GP_Bomb_LD)
        # ERRR {MK-81SE}
        Mk_82___500lb_GP_Bomb_LD = (1, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (1, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        AIM_9M_Sidewinder_IR_AAM = (1, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (1, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (1, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        Smokewinder___red = (1, Weapons.Smokewinder___red)
        Smokewinder___green = (1, Weapons.Smokewinder___green)
        Smokewinder___blue = (1, Weapons.Smokewinder___blue)
        Smokewinder___white = (1, Weapons.Smokewinder___white)
        Smokewinder___yellow = (1, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (1, Weapons.Smokewinder___orange)
        R550_Magic_2_IR_AAM = (1, Weapons.R550_Magic_2_IR_AAM)

    # ERRR {Barax}
    # ERRR {Phimat}
    # ERRR <CLEAN>

    class Pylon2:
        Mk_81___250lb_GP_Bomb_LD = (2, Weapons.Mk_81___250lb_GP_Bomb_LD)
        # ERRR {MK-81SE}
        Mk_82___500lb_GP_Bomb_LD = (2, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (2, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_83___1000lb_GP_Bomb_LD = (2, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (2, Weapons.M117___750lb_GP_Bomb_LD)
        BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD = (
            2,
            Weapons.BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE_ = (
            2,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE_,
        )
        UB_32A___32_x_UnGd_Rkts__57_mm_S_5KO_HEAT_Frag = (
            2,
            Weapons.UB_32A___32_x_UnGd_Rkts__57_mm_S_5KO_HEAT_Frag,
        )
        LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE = (
            2,
            Weapons.LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_M156_SM = (
            2,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_M156_SM,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE = (
            2,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT = (
            2,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_M156_SM = (
            2,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_M156_SM,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE = (
            2,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT = (
            2,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE = (
            2,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT = (
            2,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT,
        )
        M3_Fuel_Tank_1300_Liter = (2, WeaponsMirage3.M3_Fuel_Tank_1300_Liter)
        M3_Fuel_Tank_1700_Liter = (2, WeaponsMirage3.M3_Fuel_Tank_1700_Liter)
        M3_superSonic_Tank_1000_Liter = (
            2,
            WeaponsMirage3.M3_superSonic_Tank_1000_Liter,
        )
        M3_Tank_1000_Liter_MK82_4 = (2, WeaponsMirage3.M3_Tank_1000_Liter_MK82_4)

    # ERRR <CLEAN>

    class Pylon3:
        Mk_81___250lb_GP_Bomb_LD = (3, Weapons.Mk_81___250lb_GP_Bomb_LD)
        # ERRR {MK-81SE}
        Mk_82___500lb_GP_Bomb_LD = (3, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (3, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        GBU_12___500lb_Laser_Guided_Bomb = (3, Weapons.GBU_12___500lb_Laser_Guided_Bomb)

    # ERRR <CLEAN>

    class Pylon4:
        Mk_81___250lb_GP_Bomb_LD = (4, Weapons.Mk_81___250lb_GP_Bomb_LD)
        # ERRR {MK-81SE}
        Mk_82___500lb_GP_Bomb_LD = (4, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (4, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)

    # ERRR <CLEAN>

    class Pylon6:
        L005_Sorbtsiya_ECM_pod__left_ = (6, Weapons.L005_Sorbtsiya_ECM_pod__left_)
        L_081_Fantasmagoria_ELINT_pod = (6, Weapons.L_081_Fantasmagoria_ELINT_pod)
        Smoke_Generator___red_ = (6, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (6, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (6, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (6, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (6, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (6, Weapons.Smoke_Generator___orange_)

    # ERRR <CLEAN>

    class Pylon7:
        Mk_81___250lb_GP_Bomb_LD = (7, Weapons.Mk_81___250lb_GP_Bomb_LD)
        # ERRR {MK-81SE}
        Mk_82___500lb_GP_Bomb_LD = (7, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (7, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_83___1000lb_GP_Bomb_LD = (7, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (7, Weapons.M117___750lb_GP_Bomb_LD)
        S530D = (7, Weapons.S530D)
        M3_Fuel_Tank_1300_Liter = (7, WeaponsMirage3.M3_Fuel_Tank_1300_Liter)
        M3_Fuel_Tank_800_Liter = (7, WeaponsMirage3.M3_Fuel_Tank_800_Liter)
        BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            Weapons.BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        BLG_66_AC_Belouga = (7, Weapons.BLG_66_AC_Belouga)

    # ERRR <CLEAN>

    class Pylon8:
        L005_Sorbtsiya_ECM_pod__left_ = (8, Weapons.L005_Sorbtsiya_ECM_pod__left_)
        L_081_Fantasmagoria_ELINT_pod = (8, Weapons.L_081_Fantasmagoria_ELINT_pod)
        Smoke_Generator___red_ = (8, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (8, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (8, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (8, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (8, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (8, Weapons.Smoke_Generator___orange_)

    # ERRR <CLEAN>

    class Pylon10:
        Mk_81___250lb_GP_Bomb_LD = (10, Weapons.Mk_81___250lb_GP_Bomb_LD)
        # ERRR {MK-81SE}
        Mk_82___500lb_GP_Bomb_LD = (10, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            10,
            Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )

    # ERRR <CLEAN>

    class Pylon11:
        Mk_81___250lb_GP_Bomb_LD = (11, Weapons.Mk_81___250lb_GP_Bomb_LD)
        # ERRR {MK-81SE}
        Mk_82___500lb_GP_Bomb_LD = (11, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            11,
            Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (
            11,
            Weapons.GBU_12___500lb_Laser_Guided_Bomb,
        )

    # ERRR <CLEAN>

    class Pylon12:
        Mk_81___250lb_GP_Bomb_LD = (12, Weapons.Mk_81___250lb_GP_Bomb_LD)
        # ERRR {MK-81SE}
        Mk_82___500lb_GP_Bomb_LD = (12, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            12,
            Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (12, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (12, Weapons.M117___750lb_GP_Bomb_LD)
        BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD = (
            12,
            Weapons.BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE_ = (
            12,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE_,
        )
        UB_32A___32_x_UnGd_Rkts__57_mm_S_5KO_HEAT_Frag = (
            12,
            Weapons.UB_32A___32_x_UnGd_Rkts__57_mm_S_5KO_HEAT_Frag,
        )
        LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE = (
            12,
            Weapons.LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_M156_SM = (
            12,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_M156_SM,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE = (
            12,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT = (
            12,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_M156_SM = (
            12,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_M156_SM,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE = (
            12,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT = (
            12,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE = (
            12,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT = (
            12,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT,
        )
        M3_Fuel_Tank_1300_Liter = (12, WeaponsMirage3.M3_Fuel_Tank_1300_Liter)
        M3_Fuel_Tank_1700_Liter = (12, WeaponsMirage3.M3_Fuel_Tank_1700_Liter)
        M3_superSonic_Tank_1000_Liter = (
            12,
            WeaponsMirage3.M3_superSonic_Tank_1000_Liter,
        )
        M3_Tank_1000_Liter_MK82_4_ = (12, WeaponsMirage3.M3_Tank_1000_Liter_MK82_4_)

    # ERRR <CLEAN>

    class Pylon13:
        Mk_81___250lb_GP_Bomb_LD = (13, Weapons.Mk_81___250lb_GP_Bomb_LD)
        # ERRR {MK-81SE}
        Mk_82___500lb_GP_Bomb_LD = (13, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            13,
            Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        AIM_9M_Sidewinder_IR_AAM = (13, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (13, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (13, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        Smokewinder___red = (13, Weapons.Smokewinder___red)
        Smokewinder___green = (13, Weapons.Smokewinder___green)
        Smokewinder___blue = (13, Weapons.Smokewinder___blue)
        Smokewinder___white = (13, Weapons.Smokewinder___white)
        Smokewinder___yellow = (13, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (13, Weapons.Smokewinder___orange)
        R550_Magic_2_IR_AAM = (13, Weapons.R550_Magic_2_IR_AAM)

    # ERRR {Barax}
    # ERRR {Phimat}
    # ERRR <CLEAN>

    pylons = {1, 2, 3, 4, 6, 7, 8, 10, 11, 12, 13}

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


@planemod
class VSN_Mirage50(PlaneType):
    id = "VSN_Mirage50"
    flyable = True
    height = 4.5
    width = 8.22
    length = 15.03
    fuel_max = 2150
    max_speed = 2450.088
    chaff = 90
    flare = 45
    charge_total = 180
    chaff_charge_size = 1
    flare_charge_size = 2
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    livery_name = "VSN_MIRAGE50"  # from livery_entry

    class Pylon1:
        Mk_81___250lb_GP_Bomb_LD = (1, Weapons.Mk_81___250lb_GP_Bomb_LD)
        # ERRR {MK-81SE}
        Mk_82___500lb_GP_Bomb_LD = (1, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (1, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        AIM_9M_Sidewinder_IR_AAM = (1, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (1, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (1, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        Smokewinder___red = (1, Weapons.Smokewinder___red)
        Smokewinder___green = (1, Weapons.Smokewinder___green)
        Smokewinder___blue = (1, Weapons.Smokewinder___blue)
        Smokewinder___white = (1, Weapons.Smokewinder___white)
        Smokewinder___yellow = (1, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (1, Weapons.Smokewinder___orange)
        R550_Magic_2_IR_AAM = (1, Weapons.R550_Magic_2_IR_AAM)

    # ERRR {Barax}
    # ERRR {Phimat}
    # ERRR <CLEAN>

    class Pylon2:
        Mk_81___250lb_GP_Bomb_LD = (2, Weapons.Mk_81___250lb_GP_Bomb_LD)
        # ERRR {MK-81SE}
        Mk_82___500lb_GP_Bomb_LD = (2, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (2, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_83___1000lb_GP_Bomb_LD = (2, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (2, Weapons.M117___750lb_GP_Bomb_LD)
        BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD = (
            2,
            Weapons.BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE_ = (
            2,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE_,
        )
        UB_32A___32_x_UnGd_Rkts__57_mm_S_5KO_HEAT_Frag = (
            2,
            Weapons.UB_32A___32_x_UnGd_Rkts__57_mm_S_5KO_HEAT_Frag,
        )
        LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE = (
            2,
            Weapons.LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_M156_SM = (
            2,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_M156_SM,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE = (
            2,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT = (
            2,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_M156_SM = (
            2,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_M156_SM,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE = (
            2,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT = (
            2,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE = (
            2,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT = (
            2,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT,
        )
        M3_Fuel_Tank_1300_Liter = (2, WeaponsMirage3.M3_Fuel_Tank_1300_Liter)
        M3_Fuel_Tank_1700_Liter = (2, WeaponsMirage3.M3_Fuel_Tank_1700_Liter)
        M3_superSonic_Tank_1000_Liter = (
            2,
            WeaponsMirage3.M3_superSonic_Tank_1000_Liter,
        )
        M3_Tank_1000_Liter_MK82_4 = (2, WeaponsMirage3.M3_Tank_1000_Liter_MK82_4)

    # ERRR <CLEAN>

    class Pylon3:
        Mk_81___250lb_GP_Bomb_LD = (3, Weapons.Mk_81___250lb_GP_Bomb_LD)
        # ERRR {MK-81SE}
        Mk_82___500lb_GP_Bomb_LD = (3, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (3, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        GBU_12___500lb_Laser_Guided_Bomb = (3, Weapons.GBU_12___500lb_Laser_Guided_Bomb)

    # ERRR <CLEAN>

    class Pylon4:
        Mk_81___250lb_GP_Bomb_LD = (4, Weapons.Mk_81___250lb_GP_Bomb_LD)
        # ERRR {MK-81SE}
        Mk_82___500lb_GP_Bomb_LD = (4, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (4, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)

    # ERRR <CLEAN>

    class Pylon6:
        L005_Sorbtsiya_ECM_pod__left_ = (6, Weapons.L005_Sorbtsiya_ECM_pod__left_)
        L_081_Fantasmagoria_ELINT_pod = (6, Weapons.L_081_Fantasmagoria_ELINT_pod)
        Smoke_Generator___red_ = (6, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (6, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (6, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (6, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (6, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (6, Weapons.Smoke_Generator___orange_)

    # ERRR <CLEAN>

    class Pylon7:
        Mk_81___250lb_GP_Bomb_LD = (7, Weapons.Mk_81___250lb_GP_Bomb_LD)
        # ERRR {MK-81SE}
        Mk_82___500lb_GP_Bomb_LD = (7, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (7, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_83___1000lb_GP_Bomb_LD = (7, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (7, Weapons.M117___750lb_GP_Bomb_LD)
        S530D = (7, Weapons.S530D)
        M3_Fuel_Tank_1300_Liter = (7, WeaponsMirage3.M3_Fuel_Tank_1300_Liter)
        M3_Fuel_Tank_800_Liter = (7, WeaponsMirage3.M3_Fuel_Tank_800_Liter)
        BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            Weapons.BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        BLG_66_AC_Belouga = (7, Weapons.BLG_66_AC_Belouga)

    # ERRR <CLEAN>

    class Pylon8:
        L005_Sorbtsiya_ECM_pod__left_ = (8, Weapons.L005_Sorbtsiya_ECM_pod__left_)
        L_081_Fantasmagoria_ELINT_pod = (8, Weapons.L_081_Fantasmagoria_ELINT_pod)
        Smoke_Generator___red_ = (8, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (8, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (8, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (8, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (8, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (8, Weapons.Smoke_Generator___orange_)

    # ERRR <CLEAN>

    class Pylon10:
        Mk_81___250lb_GP_Bomb_LD = (10, Weapons.Mk_81___250lb_GP_Bomb_LD)
        # ERRR {MK-81SE}
        Mk_82___500lb_GP_Bomb_LD = (10, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            10,
            Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )

    # ERRR <CLEAN>

    class Pylon11:
        Mk_81___250lb_GP_Bomb_LD = (11, Weapons.Mk_81___250lb_GP_Bomb_LD)
        # ERRR {MK-81SE}
        Mk_82___500lb_GP_Bomb_LD = (11, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            11,
            Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (
            11,
            Weapons.GBU_12___500lb_Laser_Guided_Bomb,
        )

    # ERRR <CLEAN>

    class Pylon12:
        Mk_81___250lb_GP_Bomb_LD = (12, Weapons.Mk_81___250lb_GP_Bomb_LD)
        # ERRR {MK-81SE}
        Mk_82___500lb_GP_Bomb_LD = (12, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            12,
            Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (12, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (12, Weapons.M117___750lb_GP_Bomb_LD)
        BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD = (
            12,
            Weapons.BRU_42___3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE_ = (
            12,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE_,
        )
        UB_32A___32_x_UnGd_Rkts__57_mm_S_5KO_HEAT_Frag = (
            12,
            Weapons.UB_32A___32_x_UnGd_Rkts__57_mm_S_5KO_HEAT_Frag,
        )
        LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE = (
            12,
            Weapons.LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_M156_SM = (
            12,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_M156_SM,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE = (
            12,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT = (
            12,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_M156_SM = (
            12,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_M156_SM,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE = (
            12,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT = (
            12,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE = (
            12,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE,
        )
        LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT = (
            12,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT,
        )
        M3_Fuel_Tank_1300_Liter = (12, WeaponsMirage3.M3_Fuel_Tank_1300_Liter)
        M3_Fuel_Tank_1700_Liter = (12, WeaponsMirage3.M3_Fuel_Tank_1700_Liter)
        M3_superSonic_Tank_1000_Liter = (
            12,
            WeaponsMirage3.M3_superSonic_Tank_1000_Liter,
        )
        M3_Tank_1000_Liter_MK82_4_ = (12, WeaponsMirage3.M3_Tank_1000_Liter_MK82_4_)

    # ERRR <CLEAN>

    class Pylon13:
        Mk_81___250lb_GP_Bomb_LD = (13, Weapons.Mk_81___250lb_GP_Bomb_LD)
        # ERRR {MK-81SE}
        Mk_82___500lb_GP_Bomb_LD = (13, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            13,
            Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        AIM_9M_Sidewinder_IR_AAM = (13, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (13, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (13, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        Smokewinder___red = (13, Weapons.Smokewinder___red)
        Smokewinder___green = (13, Weapons.Smokewinder___green)
        Smokewinder___blue = (13, Weapons.Smokewinder___blue)
        Smokewinder___white = (13, Weapons.Smokewinder___white)
        Smokewinder___yellow = (13, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (13, Weapons.Smokewinder___orange)
        R550_Magic_2_IR_AAM = (13, Weapons.R550_Magic_2_IR_AAM)

    # ERRR {Barax}
    # ERRR {Phimat}
    # ERRR <CLEAN>

    pylons = {1, 2, 3, 4, 6, 7, 8, 10, 11, 12, 13}

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
