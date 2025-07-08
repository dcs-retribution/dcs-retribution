from typing import Dict, List, Set, Any

from dcs import task
from dcs.planes import PlaneType
from dcs.unitpropertydescription import UnitPropertyDescription
from dcs.weapons_data import Weapons
from dcs.unitpropertydescription import UnitPropertyDescription


from game.modsupport import planemod
from pydcs_extensions.weapon_injector import inject_weapons


class WeaponsTORNADO_ADV:
    Skyflash__Semi_Active_Radar_AAM_ = {
        "clsid": "{Skflash1}",
        "name": "Skyflash (Semi-Active Radar AAM)",
        "weight": 194,
    }


inject_weapons(WeaponsTORNADO_ADV)


@planemod
class Tornado_ADV(PlaneType):
    id = "Tornado_ADV"
    flyable = True
    height = 5.7
    width = 13.9
    length = 16.7
    fuel_max = 4660
    max_speed = 2649.996
    chaff = 90
    flare = 45
    charge_total = 180
    chaff_charge_size = 1
    flare_charge_size = 2
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    livery_name = "TORNADO_ADV"  # from type

    class Pylon1:
        AIM_9P_Sidewinder_IR_AAM = (1, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9M_Sidewinder_IR_AAM = (1, Weapons.AIM_9M_Sidewinder_IR_AAM)
        # ERRR {JAS39_ASRAAM}
        AIM_9P5_Sidewinder_IR_AAM = (1, Weapons.AIM_9P5_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (1, Weapons.AIM_9L_Sidewinder_IR_AAM)

    class Pylon2:
        Fuel_Tank_800_L__21_ = (2, Weapons.Fuel_Tank_800_L__21_)

    class Pylon3:
        AIM_9P_Sidewinder_IR_AAM = (3, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9M_Sidewinder_IR_AAM = (3, Weapons.AIM_9M_Sidewinder_IR_AAM)
        # ERRR {JAS39_ASRAAM}
        AIM_9P5_Sidewinder_IR_AAM = (3, Weapons.AIM_9P5_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (3, Weapons.AIM_9L_Sidewinder_IR_AAM)

    class Pylon5:
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            5,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            5,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        Skyflash__Semi_Active_Radar_AAM_ = (
            5,
            WeaponsTORNADO_ADV.Skyflash__Semi_Active_Radar_AAM_,
        )

    class Pylon6:
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            6,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            6,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        Skyflash__Semi_Active_Radar_AAM_ = (
            6,
            WeaponsTORNADO_ADV.Skyflash__Semi_Active_Radar_AAM_,
        )

    class Pylon7:
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            7,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            7,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        Skyflash__Semi_Active_Radar_AAM_ = (
            7,
            WeaponsTORNADO_ADV.Skyflash__Semi_Active_Radar_AAM_,
        )

    class Pylon8:
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            8,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            8,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        Skyflash__Semi_Active_Radar_AAM_ = (
            8,
            WeaponsTORNADO_ADV.Skyflash__Semi_Active_Radar_AAM_,
        )

    class Pylon10:
        AIM_9P_Sidewinder_IR_AAM = (10, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9M_Sidewinder_IR_AAM = (10, Weapons.AIM_9M_Sidewinder_IR_AAM)
        # ERRR {JAS39_ASRAAM}
        AIM_9P5_Sidewinder_IR_AAM = (10, Weapons.AIM_9P5_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (10, Weapons.AIM_9L_Sidewinder_IR_AAM)

    class Pylon11:
        Fuel_Tank_800_L__21_ = (11, Weapons.Fuel_Tank_800_L__21_)

    class Pylon12:
        AIM_9P_Sidewinder_IR_AAM = (12, Weapons.AIM_9P_Sidewinder_IR_AAM)
        AIM_9M_Sidewinder_IR_AAM = (12, Weapons.AIM_9M_Sidewinder_IR_AAM)
        # ERRR {JAS39_ASRAAM}
        AIM_9P5_Sidewinder_IR_AAM = (12, Weapons.AIM_9P5_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (12, Weapons.AIM_9L_Sidewinder_IR_AAM)

    pylons: Set[int] = {1, 2, 3, 5, 6, 7, 8, 10, 11, 12}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.Reconnaissance,
    ]
    task_default = task.CAP
