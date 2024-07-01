from enum import Enum

from dcs import task

from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

from game.modsupport import planemod
from pydcs_extensions.weapon_injector import inject_weapons


class WeaponsMirage3:
    M3_Fuel_Tank_1300_Liter = {
        "clsid": "{VSN_M3C2_PTB}",
        "name": "M3 Fuel Tank 1300 Liter",
        "weight": 1172,
    }
    M3_Fuel_Tank_1700_Liter = {
        "clsid": "{VSN_M3C3_PTB}",
        "name": "M3 Fuel Tank 1700 Liter",
        "weight": 1492,
    }
    M3_Fuel_Tank_625_Liter = {
        "clsid": "{VSN_M3C1_PTB}",
        "name": "M3 Fuel Tank 625 Liter",
        "weight": 600,
    }


inject_weapons(WeaponsMirage3)


@planemod
class VSN_MirageIIIC(PlaneType):
    id = "VSN_MirageIIIC"
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

    livery_name = "VSN_MirageIIIC"  # from type

    class Pylon1:
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (1, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        Smokewinder___red = (1, Weapons.Smokewinder___red)
        Smokewinder___green = (1, Weapons.Smokewinder___green)
        Smokewinder___blue = (1, Weapons.Smokewinder___blue)
        Smokewinder___white = (1, Weapons.Smokewinder___white)
        Smokewinder___yellow = (1, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (1, Weapons.Smokewinder___orange)
        R550_Magic_2_IR_AAM = (1, Weapons.R550_Magic_2_IR_AAM)
        Matra_Super_530D = (1, Weapons.Matra_Super_530D)

    # ERRR <CLEAN>

    class Pylon2:
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided = (
            2,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided,
        )
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            2,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            2,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (2, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        Mk_84___2000lb_GP_Bomb_LD = (2, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            2,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (2, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        BLU_107___440lb_Anti_Runway_Penetrator_Bomb = (
            2,
            Weapons.BLU_107___440lb_Anti_Runway_Penetrator_Bomb,
        )
        # ERRR {FAAFA032-8996-42BF-ADC4-8E2C86BCE536}
        Kh_59M__AS_18_Kazoo____930kg__ASM__IN = (
            2,
            Weapons.Kh_59M__AS_18_Kazoo____930kg__ASM__IN,
        )
        Kh_58U__AS_11_Kilter____640kg__ARM__IN__Pas_Rdr_ = (
            2,
            Weapons.Kh_58U__AS_11_Kilter____640kg__ARM__IN__Pas_Rdr_,
        )
        R550_Magic_2_IR_AAM = (2, Weapons.R550_Magic_2_IR_AAM)
        Matra_Super_530D = (2, Weapons.Matra_Super_530D)
        M3_Fuel_Tank_625_Liter = (2, WeaponsMirage3.M3_Fuel_Tank_625_Liter)
        M3_Fuel_Tank_1300_Liter = (2, WeaponsMirage3.M3_Fuel_Tank_1300_Liter)

    class Pylon3:
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            3,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            3,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (3, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        Mk_84___2000lb_GP_Bomb_LD = (3, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            3,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (3, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        R550_Magic_2_IR_AAM = (3, Weapons.R550_Magic_2_IR_AAM)
        Matra_Super_530D = (3, Weapons.Matra_Super_530D)

    # ERRR {Kh-58U}

    class Pylon5:
        L005_Sorbtsiya_ECM_pod__left_ = (5, Weapons.L005_Sorbtsiya_ECM_pod__left_)
        L_081_Fantasmagoria_ELINT_pod = (5, Weapons.L_081_Fantasmagoria_ELINT_pod)
        Smoke_Generator___red_ = (5, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (5, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (5, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (5, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (5, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (5, Weapons.Smoke_Generator___orange_)

    class Pylon6:
        M3_Fuel_Tank_1300_Liter = (6, WeaponsMirage3.M3_Fuel_Tank_1300_Liter)
        M3_Fuel_Tank_1700_Liter = (6, WeaponsMirage3.M3_Fuel_Tank_1700_Liter)

    class Pylon7:
        L005_Sorbtsiya_ECM_pod__left_ = (7, Weapons.L005_Sorbtsiya_ECM_pod__left_)
        L_081_Fantasmagoria_ELINT_pod = (7, Weapons.L_081_Fantasmagoria_ELINT_pod)
        Smoke_Generator___red_ = (7, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (7, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (7, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (7, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (7, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (7, Weapons.Smoke_Generator___orange_)

    class Pylon9:
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            9,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            9,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (9, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        Mk_84___2000lb_GP_Bomb_LD = (9, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            9,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (9, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        R550_Magic_2_IR_AAM = (9, Weapons.R550_Magic_2_IR_AAM)
        Matra_Super_530D = (9, Weapons.Matra_Super_530D)

    # ERRR {Kh-58U}

    class Pylon10:
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided = (
            10,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided,
        )
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            10,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            10,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (
            10,
            Weapons.KAB_500Kr___500kg_TV_Guided_Bomb,
        )
        Mk_84___2000lb_GP_Bomb_LD = (10, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            10,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (10, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        BLU_107___440lb_Anti_Runway_Penetrator_Bomb = (
            10,
            Weapons.BLU_107___440lb_Anti_Runway_Penetrator_Bomb,
        )
        # ERRR {FAAFA032-8996-42BF-ADC4-8E2C86BCE536}
        Kh_59M__AS_18_Kazoo____930kg__ASM__IN = (
            10,
            Weapons.Kh_59M__AS_18_Kazoo____930kg__ASM__IN,
        )
        Kh_58U__AS_11_Kilter____640kg__ARM__IN__Pas_Rdr_ = (
            10,
            Weapons.Kh_58U__AS_11_Kilter____640kg__ARM__IN__Pas_Rdr_,
        )
        R550_Magic_2_IR_AAM = (10, Weapons.R550_Magic_2_IR_AAM)
        Matra_Super_530D = (10, Weapons.Matra_Super_530D)
        M3_Fuel_Tank_625_Liter = (10, WeaponsMirage3.M3_Fuel_Tank_625_Liter)
        M3_Fuel_Tank_1300_Liter = (10, WeaponsMirage3.M3_Fuel_Tank_1300_Liter)

    class Pylon11:
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (11, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        Smokewinder___red = (11, Weapons.Smokewinder___red)
        Smokewinder___green = (11, Weapons.Smokewinder___green)
        Smokewinder___blue = (11, Weapons.Smokewinder___blue)
        Smokewinder___white = (11, Weapons.Smokewinder___white)
        Smokewinder___yellow = (11, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (11, Weapons.Smokewinder___orange)
        R550_Magic_2_IR_AAM = (11, Weapons.R550_Magic_2_IR_AAM)
        Matra_Super_530D = (11, Weapons.Matra_Super_530D)

    # ERRR <CLEAN>

    pylons = {1, 2, 3, 5, 6, 7, 9, 10, 11}

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
class VSN_MirageIIIC_AG(PlaneType):
    id = "VSN_MirageIIIC_AG"
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

    livery_name = "VSN_MirageIIIC_AG"  # from type

    class Pylon1:
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (1, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        Smokewinder___red = (1, Weapons.Smokewinder___red)
        Smokewinder___green = (1, Weapons.Smokewinder___green)
        Smokewinder___blue = (1, Weapons.Smokewinder___blue)
        Smokewinder___white = (1, Weapons.Smokewinder___white)
        Smokewinder___yellow = (1, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (1, Weapons.Smokewinder___orange)
        R550_Magic_2_IR_AAM = (1, Weapons.R550_Magic_2_IR_AAM)
        Matra_Super_530D = (1, Weapons.Matra_Super_530D)

    # ERRR <CLEAN>

    class Pylon2:
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided = (
            2,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided,
        )
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            2,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            2,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (2, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        Mk_84___2000lb_GP_Bomb_LD = (2, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            2,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (2, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        BLU_107___440lb_Anti_Runway_Penetrator_Bomb = (
            2,
            Weapons.BLU_107___440lb_Anti_Runway_Penetrator_Bomb,
        )
        # ERRR {FAAFA032-8996-42BF-ADC4-8E2C86BCE536}
        Kh_59M__AS_18_Kazoo____930kg__ASM__IN = (
            2,
            Weapons.Kh_59M__AS_18_Kazoo____930kg__ASM__IN,
        )
        Kh_58U__AS_11_Kilter____640kg__ARM__IN__Pas_Rdr_ = (
            2,
            Weapons.Kh_58U__AS_11_Kilter____640kg__ARM__IN__Pas_Rdr_,
        )
        R550_Magic_2_IR_AAM = (2, Weapons.R550_Magic_2_IR_AAM)
        Matra_Super_530D = (2, Weapons.Matra_Super_530D)
        M3_Fuel_Tank_625_Liter = (2, WeaponsMirage3.M3_Fuel_Tank_625_Liter)
        M3_Fuel_Tank_1300_Liter = (2, WeaponsMirage3.M3_Fuel_Tank_1300_Liter)

    class Pylon3:
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            3,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            3,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (3, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        Mk_84___2000lb_GP_Bomb_LD = (3, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            3,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (3, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        R550_Magic_2_IR_AAM = (3, Weapons.R550_Magic_2_IR_AAM)
        Matra_Super_530D = (3, Weapons.Matra_Super_530D)

    # ERRR {Kh-58U}

    class Pylon5:
        L005_Sorbtsiya_ECM_pod__left_ = (5, Weapons.L005_Sorbtsiya_ECM_pod__left_)
        L_081_Fantasmagoria_ELINT_pod = (5, Weapons.L_081_Fantasmagoria_ELINT_pod)
        Smoke_Generator___red_ = (5, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (5, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (5, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (5, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (5, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (5, Weapons.Smoke_Generator___orange_)

    class Pylon6:
        M3_Fuel_Tank_1300_Liter = (6, WeaponsMirage3.M3_Fuel_Tank_1300_Liter)
        M3_Fuel_Tank_1700_Liter = (6, WeaponsMirage3.M3_Fuel_Tank_1700_Liter)

    class Pylon7:
        L005_Sorbtsiya_ECM_pod__left_ = (7, Weapons.L005_Sorbtsiya_ECM_pod__left_)
        L_081_Fantasmagoria_ELINT_pod = (7, Weapons.L_081_Fantasmagoria_ELINT_pod)
        Smoke_Generator___red_ = (7, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (7, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (7, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (7, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (7, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (7, Weapons.Smoke_Generator___orange_)

    class Pylon9:
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            9,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            9,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (9, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        Mk_84___2000lb_GP_Bomb_LD = (9, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            9,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (9, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        R550_Magic_2_IR_AAM = (9, Weapons.R550_Magic_2_IR_AAM)
        Matra_Super_530D = (9, Weapons.Matra_Super_530D)

    # ERRR {Kh-58U}

    class Pylon10:
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided = (
            10,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided,
        )
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            10,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            10,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (
            10,
            Weapons.KAB_500Kr___500kg_TV_Guided_Bomb,
        )
        Mk_84___2000lb_GP_Bomb_LD = (10, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            10,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (10, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        BLU_107___440lb_Anti_Runway_Penetrator_Bomb = (
            10,
            Weapons.BLU_107___440lb_Anti_Runway_Penetrator_Bomb,
        )
        # ERRR {FAAFA032-8996-42BF-ADC4-8E2C86BCE536}
        Kh_59M__AS_18_Kazoo____930kg__ASM__IN = (
            10,
            Weapons.Kh_59M__AS_18_Kazoo____930kg__ASM__IN,
        )
        Kh_58U__AS_11_Kilter____640kg__ARM__IN__Pas_Rdr_ = (
            10,
            Weapons.Kh_58U__AS_11_Kilter____640kg__ARM__IN__Pas_Rdr_,
        )
        R550_Magic_2_IR_AAM = (10, Weapons.R550_Magic_2_IR_AAM)
        Matra_Super_530D = (10, Weapons.Matra_Super_530D)
        M3_Fuel_Tank_625_Liter = (10, WeaponsMirage3.M3_Fuel_Tank_625_Liter)
        M3_Fuel_Tank_1300_Liter = (10, WeaponsMirage3.M3_Fuel_Tank_1300_Liter)

    class Pylon11:
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (11, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        Smokewinder___red = (11, Weapons.Smokewinder___red)
        Smokewinder___green = (11, Weapons.Smokewinder___green)
        Smokewinder___blue = (11, Weapons.Smokewinder___blue)
        Smokewinder___white = (11, Weapons.Smokewinder___white)
        Smokewinder___yellow = (11, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (11, Weapons.Smokewinder___orange)
        R550_Magic_2_IR_AAM = (11, Weapons.R550_Magic_2_IR_AAM)
        Matra_Super_530D = (11, Weapons.Matra_Super_530D)

    # ERRR <CLEAN>

    pylons = {1, 2, 3, 5, 6, 7, 9, 10, 11}

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
class VSN_MirageIIIS(PlaneType):
    id = "VSN_MirageIIIS"
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

    livery_name = "VSN_MirageIIIS"  # from type

    class Pylon1:
        AIM_9M_Sidewinder_IR_AAM = (1, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (1, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            1,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (1, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        Smokewinder___red = (1, Weapons.Smokewinder___red)
        Smokewinder___green = (1, Weapons.Smokewinder___green)
        Smokewinder___blue = (1, Weapons.Smokewinder___blue)
        Smokewinder___white = (1, Weapons.Smokewinder___white)
        Smokewinder___yellow = (1, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (1, Weapons.Smokewinder___orange)
        R550_Magic_2_IR_AAM = (1, Weapons.R550_Magic_2_IR_AAM)
        Matra_Super_530D = (1, Weapons.Matra_Super_530D)

    # ERRR <CLEAN>

    class Pylon2:
        LAU_115_LAU_127_CATM_9M = (2, Weapons.LAU_115_LAU_127_CATM_9M)
        LAU_115_LAU_127_AIM_9L = (2, Weapons.LAU_115_LAU_127_AIM_9L)
        LAU_115_LAU_127_AIM_9M = (2, Weapons.LAU_115_LAU_127_AIM_9M)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            2,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided = (
            2,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided,
        )
        Mk_84___2000lb_GP_Bomb_LD = (2, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            2,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (2, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        BLU_107___440lb_Anti_Runway_Penetrator_Bomb = (
            2,
            Weapons.BLU_107___440lb_Anti_Runway_Penetrator_Bomb,
        )
        # ERRR {FAAFA032-8996-42BF-ADC4-8E2C86BCE536}
        Kh_59M__AS_18_Kazoo____930kg__ASM__IN = (
            2,
            Weapons.Kh_59M__AS_18_Kazoo____930kg__ASM__IN,
        )
        Kh_58U__AS_11_Kilter____640kg__ARM__IN__Pas_Rdr_ = (
            2,
            Weapons.Kh_58U__AS_11_Kilter____640kg__ARM__IN__Pas_Rdr_,
        )
        R550_Magic_2_IR_AAM = (2, Weapons.R550_Magic_2_IR_AAM)
        Matra_Super_530D = (2, Weapons.Matra_Super_530D)
        M3_Fuel_Tank_625_Liter = (2, WeaponsMirage3.M3_Fuel_Tank_625_Liter)

    class Pylon3:
        LAU_115_LAU_127_CATM_9M = (3, Weapons.LAU_115_LAU_127_CATM_9M)
        LAU_115_LAU_127_AIM_9L = (3, Weapons.LAU_115_LAU_127_AIM_9L)
        LAU_115_LAU_127_AIM_9M = (3, Weapons.LAU_115_LAU_127_AIM_9M)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            3,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        Mk_84___2000lb_GP_Bomb_LD = (3, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            3,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (3, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        R550_Magic_2_IR_AAM = (3, Weapons.R550_Magic_2_IR_AAM)
        Matra_Super_530D = (3, Weapons.Matra_Super_530D)

    # ERRR {Kh-58U}

    class Pylon5:
        L005_Sorbtsiya_ECM_pod__left_ = (5, Weapons.L005_Sorbtsiya_ECM_pod__left_)
        L_081_Fantasmagoria_ELINT_pod = (5, Weapons.L_081_Fantasmagoria_ELINT_pod)
        Smoke_Generator___red_ = (5, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (5, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (5, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (5, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (5, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (5, Weapons.Smoke_Generator___orange_)

    class Pylon6:
        M3_Fuel_Tank_1700_Liter = (6, WeaponsMirage3.M3_Fuel_Tank_1700_Liter)

    class Pylon7:
        L005_Sorbtsiya_ECM_pod__left_ = (7, Weapons.L005_Sorbtsiya_ECM_pod__left_)
        L_081_Fantasmagoria_ELINT_pod = (7, Weapons.L_081_Fantasmagoria_ELINT_pod)
        Smoke_Generator___red_ = (7, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (7, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (7, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (7, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (7, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (7, Weapons.Smoke_Generator___orange_)

    class Pylon9:
        LAU_115_LAU_127_CATM_9M = (9, Weapons.LAU_115_LAU_127_CATM_9M)
        LAU_115_LAU_127_AIM_9L = (9, Weapons.LAU_115_LAU_127_AIM_9L)
        LAU_115_LAU_127_AIM_9M = (9, Weapons.LAU_115_LAU_127_AIM_9M)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            9,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        Mk_84___2000lb_GP_Bomb_LD = (9, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            9,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (9, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        R550_Magic_2_IR_AAM = (9, Weapons.R550_Magic_2_IR_AAM)
        Matra_Super_530D = (9, Weapons.Matra_Super_530D)

    # ERRR {Kh-58U}

    class Pylon10:
        LAU_115_LAU_127_CATM_9M = (10, Weapons.LAU_115_LAU_127_CATM_9M)
        LAU_115_LAU_127_AIM_9L = (10, Weapons.LAU_115_LAU_127_AIM_9L)
        LAU_115_LAU_127_AIM_9M = (10, Weapons.LAU_115_LAU_127_AIM_9M)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            10,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided = (
            10,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided,
        )
        Mk_84___2000lb_GP_Bomb_LD = (10, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            10,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (10, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        BLU_107___440lb_Anti_Runway_Penetrator_Bomb = (
            10,
            Weapons.BLU_107___440lb_Anti_Runway_Penetrator_Bomb,
        )
        # ERRR {FAAFA032-8996-42BF-ADC4-8E2C86BCE536}
        Kh_59M__AS_18_Kazoo____930kg__ASM__IN = (
            10,
            Weapons.Kh_59M__AS_18_Kazoo____930kg__ASM__IN,
        )
        Kh_58U__AS_11_Kilter____640kg__ARM__IN__Pas_Rdr_ = (
            10,
            Weapons.Kh_58U__AS_11_Kilter____640kg__ARM__IN__Pas_Rdr_,
        )
        R550_Magic_2_IR_AAM = (10, Weapons.R550_Magic_2_IR_AAM)
        Matra_Super_530D = (10, Weapons.Matra_Super_530D)
        M3_Fuel_Tank_625_Liter = (10, WeaponsMirage3.M3_Fuel_Tank_625_Liter)

    class Pylon11:
        AIM_9M_Sidewinder_IR_AAM = (11, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (11, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            11,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (11, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        Smokewinder___red = (11, Weapons.Smokewinder___red)
        Smokewinder___green = (11, Weapons.Smokewinder___green)
        Smokewinder___blue = (11, Weapons.Smokewinder___blue)
        Smokewinder___white = (11, Weapons.Smokewinder___white)
        Smokewinder___yellow = (11, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (11, Weapons.Smokewinder___orange)
        R550_Magic_2_IR_AAM = (11, Weapons.R550_Magic_2_IR_AAM)
        Matra_Super_530D = (11, Weapons.Matra_Super_530D)

    # ERRR <CLEAN>

    pylons = {1, 2, 3, 5, 6, 7, 9, 10, 11}

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
