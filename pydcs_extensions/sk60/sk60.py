from typing import Any, Dict, Set

from dcs import task
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

from game.modsupport import planemod
from pydcs_extensions.weapon_injector import inject_weapons


class WeaponsSK_60:
    _1x_13_5cm_HE_rocket = {
        "clsid": "{d694b359-e7a8-4909-88d4-7100b77afd13}",
        "name": "1x 13,5cm HE rocket",
        "weight": 50,
    }
    _1x_14_5cm_HEAT_rocket = {
        "clsid": "{d694b359-e7a8-4909-88d4-7100b77afd12}",
        "name": "1x 14,5cm HEAT rocket",
        "weight": 50,
    }
    _2x_13_5cm_HE_rocket = {
        "clsid": "{d694b359-e7a8-4909-88d4-7100b77afd11}",
        "name": "2x 13,5cm HE rocket",
        "weight": 95,
    }
    AKAN_m_55_Gunpod = {
        "clsid": "{5d5aa063-a002-4de8-8a89-6eda1e80ee7b}",
        "name": "AKAN m/55 Gunpod",
        "weight": 196,
    }


inject_weapons(WeaponsSK_60)


@planemod
class SK_60(PlaneType):
    id = "SK-60"
    flyable = True
    height = 2.7
    width = 9.5
    length = 10.8
    fuel_max = 1640
    max_speed = 879.9984
    chaff = 0
    flare = 0
    charge_total = 0
    chaff_charge_size = 0
    flare_charge_size = 0
    eplrs = True
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 243

    livery_name = "SK-60"  # from type

    class Pylon1:
        _2x_13_5cm_HE_rocket = (1, Weapons._2x_13_5cm_HE_rocket)
        _1x_14_5cm_HEAT_rocket = (1, Weapons._1x_14_5cm_HEAT_rocket)
        _1x_13_5cm_HE_rocket = (1, Weapons._1x_13_5cm_HE_rocket)

    class Pylon2:
        AKAN_m_55_Gunpod = (2, Weapons.AKAN_m_55_Gunpod)
        _2x_13_5cm_HE_rocket = (2, Weapons._2x_13_5cm_HE_rocket)
        _1x_14_5cm_HEAT_rocket = (2, Weapons._1x_14_5cm_HEAT_rocket)
        _1x_13_5cm_HE_rocket = (2, Weapons._1x_13_5cm_HE_rocket)

    class Pylon3:
        _2x_13_5cm_HE_rocket = (3, Weapons._2x_13_5cm_HE_rocket)
        _1x_14_5cm_HEAT_rocket = (3, Weapons._1x_14_5cm_HEAT_rocket)
        _1x_13_5cm_HE_rocket = (3, Weapons._1x_13_5cm_HE_rocket)

    class Pylon4:
        _2x_13_5cm_HE_rocket = (4, Weapons._2x_13_5cm_HE_rocket)
        _1x_14_5cm_HEAT_rocket = (4, Weapons._1x_14_5cm_HEAT_rocket)
        _1x_13_5cm_HE_rocket = (4, Weapons._1x_13_5cm_HE_rocket)

    class Pylon5:
        AKAN_m_55_Gunpod = (5, Weapons.AKAN_m_55_Gunpod)
        _2x_13_5cm_HE_rocket = (5, Weapons._2x_13_5cm_HE_rocket)
        _1x_14_5cm_HEAT_rocket = (5, Weapons._1x_14_5cm_HEAT_rocket)
        _1x_13_5cm_HE_rocket = (5, Weapons._1x_13_5cm_HE_rocket)

    class Pylon6:
        _2x_13_5cm_HE_rocket = (6, Weapons._2x_13_5cm_HE_rocket)
        _1x_14_5cm_HEAT_rocket = (6, Weapons._1x_14_5cm_HEAT_rocket)
        _1x_13_5cm_HE_rocket = (6, Weapons._1x_13_5cm_HE_rocket)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8}

    tasks = [
        task.GroundAttack,
        task.PinpointStrike,
        task.CAS,
        task.AFAC,
        task.RunwayAttack,
        task.SEAD,
        task.Escort,
        task.Reconnaissance,
    ]
    task_default = task.GroundAttack
