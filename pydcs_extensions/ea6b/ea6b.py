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
    height = 4.57
    width = 10.15
    length = 17.98
    fuel_max = 6994
    max_speed = 1047.96
    chaff = 30
    flare = 30
    charge_total = 60
    chaff_charge_size = 1
    flare_charge_size = 1
    eplrs = True
    radio_frequency = 250.5

    livery_name = "EA_6B"  # from type

    class Pylon1:
        LAU_118A___AGM_45B_Shrike_ARM = (1, Weapons.LAU_118A___AGM_45B_Shrike_ARM)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            1,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        F_5_275Gal_Fuel_tank = (1, Weapons.F_5_275Gal_Fuel_tank)
        EA6B_AN_ALQ_99 = (1, Weapons.EA6B_AN_ALQ_99)

    # ERRR <CLEAN>

    class Pylon2:
        LAU_118A___AGM_45B_Shrike_ARM = (2, Weapons.LAU_118A___AGM_45B_Shrike_ARM)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            2,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        F_5_275Gal_Fuel_tank = (2, Weapons.F_5_275Gal_Fuel_tank)
        EA6B_AN_ALQ_99 = (2, Weapons.EA6B_AN_ALQ_99)

    # ERRR <CLEAN>

    class Pylon3:
        F_5_275Gal_Fuel_tank = (3, Weapons.F_5_275Gal_Fuel_tank)
        EA6B_AN_ALQ_99_ = (3, Weapons.EA6B_AN_ALQ_99_)

    # ERRR <CLEAN>

    class Pylon4:
        LAU_118A___AGM_45B_Shrike_ARM = (4, Weapons.LAU_118A___AGM_45B_Shrike_ARM)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            4,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        F_5_275Gal_Fuel_tank = (4, Weapons.F_5_275Gal_Fuel_tank)
        EA6B_AN_ALQ_99 = (4, Weapons.EA6B_AN_ALQ_99)

    # ERRR <CLEAN>

    class Pylon5:
        LAU_118A___AGM_45B_Shrike_ARM = (5, Weapons.LAU_118A___AGM_45B_Shrike_ARM)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            5,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        F_5_275Gal_Fuel_tank = (5, Weapons.F_5_275Gal_Fuel_tank)
        EA6B_AN_ALQ_99 = (5, Weapons.EA6B_AN_ALQ_99)

    # ERRR <CLEAN>

    pylons = {1, 2, 3, 4, 5}

    tasks = [
        task.Escort,
        task.Reconnaissance,
        task.GroundAttack,
        task.CAS,
        task.AFAC,
        task.RunwayAttack,
        task.AntishipStrike,
        task.SEAD,
    ]
    task_default = task.GroundAttack
