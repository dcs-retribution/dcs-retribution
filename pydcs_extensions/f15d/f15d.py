from typing import Set

from dcs import task
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

from game.modsupport import planemod
from pydcs_extensions.weapon_injector import inject_weapons


class WeaponsF15D:
    Python_5 = {"clsid": "{Python 5}", "name": "Python 5", "weight": 103}
    CFT_Fuel_left_750gal = {
        "clsid": "{F-15D_cft_750gal_left}",
        "name": "CFT Fuel left 750gal",
        "weight": 2737.33,
    }
    CFT_Fuel_left_750gal_And_Tank = {
        "clsid": "{F-15D_cft_750gal_left_And_Tank}",
        "name": "CFT Fuel left 750gal And Tank",
        "weight": 4963.69,
    }
    CFT_Fuel_Right_750gal = {
        "clsid": "{F-15D_cft_750gal_Right}",
        "name": "CFT Fuel Right 750gal",
        "weight": 2737.33,
    }
    CFT_Fuel_Right_750gal_And_Tank = {
        "clsid": "{F-15D_cft_750gal_Right_And_Tank}",
        "name": "CFT Fuel Right 750gal And Tank",
        "weight": 4963.69,
    }
    I_Derby_ER = {"clsid": "{I-Derby ER}", "name": "I-Derby ER", "weight": 118}
    ELL___8222SB = {"clsid": "{ELL - 8222SB}", "name": "ELL - 8222SB", "weight": 100}


inject_weapons(WeaponsF15D)


@planemod
class F_15D(PlaneType):
    id = "F-15D"
    flyable = True
    height = 5.63
    width = 13.05
    length = 19.43
    fuel_max = 6103
    max_speed = 2649.996
    chaff = 120
    flare = 120
    charge_total = 240
    chaff_charge_size = 1
    flare_charge_size = 1
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    livery_name = "F-15D"  # from type

    class Pylon1:
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            1,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            1,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        Smokewinder___red = (1, Weapons.Smokewinder___red)
        Smokewinder___green = (1, Weapons.Smokewinder___green)
        Smokewinder___blue = (1, Weapons.Smokewinder___blue)
        Smokewinder___white = (1, Weapons.Smokewinder___white)
        Smokewinder___yellow = (1, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (1, Weapons.Smokewinder___orange)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (1, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        Python_5 = (1, WeaponsF15D.Python_5)
        AIM_9X_Sidewinder_IR_AAM = (1, Weapons.AIM_9X_Sidewinder_IR_AAM)

    class Pylon2:
        Fuel_tank_610_gal = (2, Weapons.Fuel_tank_610_gal)
        Mk_84___2000lb_GP_Bomb_LD = (2, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            2,
            Weapons.GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        CFT_Fuel_Right_750gal_And_Tank = (2, WeaponsF15D.CFT_Fuel_Right_750gal_And_Tank)
        CFT_Fuel_Right_750gal = (2, WeaponsF15D.CFT_Fuel_Right_750gal)

    class Pylon3:
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            3,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            3,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        Python_5 = (3, WeaponsF15D.Python_5)
        I_Derby_ER = (3, WeaponsF15D.I_Derby_ER)
        AIM_9X_Sidewinder_IR_AAM = (3, Weapons.AIM_9X_Sidewinder_IR_AAM)

    class Pylon4:
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            4,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            4,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        AIM_7M_Sparrow_Semi_Active_Radar = (4, Weapons.AIM_7M_Sparrow_Semi_Active_Radar)
        AIM_7F_Sparrow_Semi_Active_Radar = (4, Weapons.AIM_7F_Sparrow_Semi_Active_Radar)
        AIM_7MH_Sparrow_Semi_Active_Radar = (
            4,
            Weapons.AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        AIM_7E_2_Sparrow_Semi_Active_Radar = (
            4,
            Weapons.AIM_7E_2_Sparrow_Semi_Active_Radar,
        )
        I_Derby_ER = (4, WeaponsF15D.I_Derby_ER)

    class Pylon5:
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            5,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            5,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        AIM_7M_Sparrow_Semi_Active_Radar = (5, Weapons.AIM_7M_Sparrow_Semi_Active_Radar)
        AIM_7F_Sparrow_Semi_Active_Radar = (5, Weapons.AIM_7F_Sparrow_Semi_Active_Radar)
        AIM_7MH_Sparrow_Semi_Active_Radar = (
            5,
            Weapons.AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        AIM_7E_2_Sparrow_Semi_Active_Radar = (
            5,
            Weapons.AIM_7E_2_Sparrow_Semi_Active_Radar,
        )
        I_Derby_ER = (5, WeaponsF15D.I_Derby_ER)
        ELL___8222SB = (5, WeaponsF15D.ELL___8222SB)

    class Pylon6:
        Fuel_tank_610_gal = (6, Weapons.Fuel_tank_610_gal)
        Mk_84___2000lb_GP_Bomb_LD = (6, Weapons.Mk_84___2000lb_GP_Bomb_LD)

    class Pylon7:
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            7,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            7,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        AIM_7M_Sparrow_Semi_Active_Radar = (7, Weapons.AIM_7M_Sparrow_Semi_Active_Radar)
        AIM_7F_Sparrow_Semi_Active_Radar = (7, Weapons.AIM_7F_Sparrow_Semi_Active_Radar)
        AIM_7MH_Sparrow_Semi_Active_Radar = (
            7,
            Weapons.AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        AIM_7E_2_Sparrow_Semi_Active_Radar = (
            7,
            Weapons.AIM_7E_2_Sparrow_Semi_Active_Radar,
        )
        I_Derby_ER = (7, WeaponsF15D.I_Derby_ER)

    class Pylon8:
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            8,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            8,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        AIM_7M_Sparrow_Semi_Active_Radar = (8, Weapons.AIM_7M_Sparrow_Semi_Active_Radar)
        AIM_7F_Sparrow_Semi_Active_Radar = (8, Weapons.AIM_7F_Sparrow_Semi_Active_Radar)
        AIM_7MH_Sparrow_Semi_Active_Radar = (
            8,
            Weapons.AIM_7MH_Sparrow_Semi_Active_Radar,
        )
        AIM_7E_2_Sparrow_Semi_Active_Radar = (
            8,
            Weapons.AIM_7E_2_Sparrow_Semi_Active_Radar,
        )
        I_Derby_ER = (8, WeaponsF15D.I_Derby_ER)

    class Pylon9:
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            9,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            9,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        Python_5 = (9, WeaponsF15D.Python_5)
        I_Derby_ER = (9, WeaponsF15D.I_Derby_ER)
        AIM_9X_Sidewinder_IR_AAM = (9, Weapons.AIM_9X_Sidewinder_IR_AAM)

    class Pylon10:
        Fuel_tank_610_gal = (10, Weapons.Fuel_tank_610_gal)
        Mk_84___2000lb_GP_Bomb_LD = (10, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            10,
            Weapons.GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        CFT_Fuel_left_750gal_And_Tank = (10, WeaponsF15D.CFT_Fuel_left_750gal_And_Tank)
        CFT_Fuel_left_750gal = (10, WeaponsF15D.CFT_Fuel_left_750gal)

    class Pylon11:
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            11,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            11,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        Smokewinder___red = (11, Weapons.Smokewinder___red)
        Smokewinder___green = (11, Weapons.Smokewinder___green)
        Smokewinder___blue = (11, Weapons.Smokewinder___blue)
        Smokewinder___white = (11, Weapons.Smokewinder___white)
        Smokewinder___yellow = (11, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (11, Weapons.Smokewinder___orange)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (11, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        Python_5 = (11, WeaponsF15D.Python_5)
        AIM_9X_Sidewinder_IR_AAM = (11, Weapons.AIM_9X_Sidewinder_IR_AAM)

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
