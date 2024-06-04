from dcs import task
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

from game.modsupport import planemod
from pydcs_extensions.weapon_injector import inject_weapons


class WeaponsEA6B:
    EA6B_AN_ALQ_99 = {
        "clsid": "{EA6B_ANALQ991}",
        "name": "EA6B AN-ALQ-99",
        "weight": 435,
    }
    EA6B_AN_ALQ_99_ = {
        "clsid": "{EA6B_ANALQ992}",
        "name": "EA6B AN-ALQ-99",
        "weight": 435,
    }


inject_weapons(WeaponsEA6B)


@planemod
class EA_6B(PlaneType):
    id = "EA_6B"
    group_size_max = 1
    height = 6.93
    width = 20.93
    length = 16.26
    fuel_max = 5500
    max_speed = 834.12
    chaff = 30
    flare = 30
    charge_total = 60
    chaff_charge_size = 1
    flare_charge_size = 1
    eplrs = True
    radio_frequency = 127.5

    livery_name = "EA_6B"  # from type

    class Pylon1:
        LAU_118a_with_AGM_45B_Shrike_ARM__Imp_ = (
            1,
            Weapons.LAU_118a_with_AGM_45B_Shrike_ARM__Imp_,
        )
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            1,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        Fuel_tank_S_3 = (1, Weapons.Fuel_tank_S_3)
        EA6B_AN_ALQ_99 = (1, WeaponsEA6B.EA6B_AN_ALQ_99)

    # ERRR <CLEAN>

    class Pylon2:
        LAU_118a_with_AGM_45B_Shrike_ARM__Imp_ = (
            2,
            Weapons.LAU_118a_with_AGM_45B_Shrike_ARM__Imp_,
        )
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            2,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        Fuel_tank_S_3 = (2, Weapons.Fuel_tank_S_3)
        EA6B_AN_ALQ_99 = (2, WeaponsEA6B.EA6B_AN_ALQ_99)

    # ERRR <CLEAN>

    class Pylon3:
        Fuel_tank_S_3 = (3, Weapons.Fuel_tank_S_3)
        EA6B_AN_ALQ_99_ = (3, WeaponsEA6B.EA6B_AN_ALQ_99_)

    # ERRR <CLEAN>

    class Pylon4:
        LAU_118a_with_AGM_45B_Shrike_ARM__Imp_ = (
            4,
            Weapons.LAU_118a_with_AGM_45B_Shrike_ARM__Imp_,
        )
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            4,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        Fuel_tank_S_3 = (4, Weapons.Fuel_tank_S_3)
        EA6B_AN_ALQ_99 = (4, WeaponsEA6B.EA6B_AN_ALQ_99)

    # ERRR <CLEAN>

    class Pylon5:
        LAU_118a_with_AGM_45B_Shrike_ARM__Imp_ = (
            5,
            Weapons.LAU_118a_with_AGM_45B_Shrike_ARM__Imp_,
        )
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            5,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        Fuel_tank_S_3 = (5, Weapons.Fuel_tank_S_3)
        EA6B_AN_ALQ_99 = (5, WeaponsEA6B.EA6B_AN_ALQ_99)

    # ERRR <CLEAN>

    pylons = {1, 2, 3, 4, 5}

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
    task_default = task.GroundAttack
