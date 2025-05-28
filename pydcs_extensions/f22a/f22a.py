from typing import Any, Dict, Set

from dcs import task
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

from game.modsupport import planemod
from pydcs_extensions.weapon_injector import inject_weapons


class F22AWeapons:
    AIM_9XX = {"clsid": "{AIM-9XX}", "name": "AIM-9XX", "weight": 85}
    AIM_120D = {"clsid": "{AIM-120D}", "name": "AIM-120D", "weight": 152}
    AIM9X_BLKII_Sidewinder_IR_AAM = {
        "clsid": "{AIM9X-BLKII}",
        "name": "AIM9X-BLKII Sidewinder IR AAM",
        "weight": 85.5,
    }
    LDTP_Fuel_tank_600_gal = {
        "clsid": "{LDTP_FUEL_Tank}",
        "name": "LDTP Fuel tank 600 gal",
        "weight": 2045.8766885,
    }
    AIM_120C7___Active_Radar_AAM = {
        "clsid": "{AIM-120C-7}",
        "name": "AIM-120C7 - Active Radar AAM",
        "weight": 161.48,
    }
    AIM_120C7___Active_Radar_AAM__IRST_POD = {
        "clsid": "{AIM_120C-7_IRST_LEFT}",
        "name": "AIM-120C7 - Active Radar AAM + IRST POD",
        "weight": 266.48,
    }
    AIM_120C7___Active_Radar_AAM__IRST_POD_ = {
        "clsid": "{AIM_120C-7_IRST_RIGHT}",
        "name": "AIM-120C7 - Active Radar AAM + IRST POD",
        "weight": 266.48,
    }
    AIM_120C8___Active_Radar_AAM = {
        "clsid": "{AIM-120C-8}",
        "name": "AIM-120C8 - Active Radar AAM",
        "weight": 161.48,
    }
    AIM_120C8___Active_Radar_AAM__IRST_POD = {
        "clsid": "{AIM_120C-8_IRST_LEFT}",
        "name": "AIM-120C8 - Active Radar AAM + IRST POD",
        "weight": 266.48,
    }
    AIM_120C8___Active_Radar_AAM__IRST_POD_ = {
        "clsid": "{AIM_120C-8_IRST_RIGHT}",
        "name": "AIM-120C8 - Active Radar AAM + IRST POD",
        "weight": 266.48,
    }
    AIM_120D3___Active_Radar_AAM = {
        "clsid": "{AIM-120D-3}",
        "name": "AIM-120D3 - Active Radar AAM",
        "weight": 165,
    }
    AIM_120D3___Active_Radar_AAM__IRST_POD = {
        "clsid": "{AIM_120D-3_IRST_LEFT}",
        "name": "AIM-120D3 - Active Radar AAM + IRST POD",
        "weight": 270,
    }
    AIM_120D3___Active_Radar_AAM__IRST_POD_ = {
        "clsid": "{AIM_120D-3_IRST_RIGHT}",
        "name": "AIM-120D3 - Active Radar AAM + IRST POD",
        "weight": 270,
    }
    AIM_260A___Active_Radar_AAM = {
        "clsid": "{AIM-260A}",
        "name": "AIM-260A - Active Radar AAM",
        "weight": 160,
    }
    AIM_260A___Active_Radar_AAM__IRST_POD = {
        "clsid": "{AIM_260A_IRST_LEFT}",
        "name": "AIM-260A - Active Radar AAM + IRST POD",
        "weight": 265,
    }
    AIM_260A___Active_Radar_AAM__IRST_POD_ = {
        "clsid": "{AIM_260A_IRST_RIGHT}",
        "name": "AIM-260A - Active Radar AAM + IRST POD",
        "weight": 265,
    }
    _2x_AIM9X_BLKII_Sidewinder_IR_AAM = {
        "clsid": "{LAU_115_2xAIM9X-II}",
        "name": "2x AIM9X-BLKII Sidewinder IR AAM",
        "weight": 221,
    }
    _2x_AIM_120C7___Active_Radar_AAM = {
        "clsid": "{LAU_115_2xAIM-120C-7}",
        "name": "2x AIM-120C7 - Active Radar AAM",
        "weight": 372.96,
    }
    _2x_AIM_120C8___Active_Radar_AAM = {
        "clsid": "{LAU_115_2xAIM-120C-8}",
        "name": "2x AIM-120C8 - Active Radar AAM",
        "weight": 372.96,
    }
    _2x_AIM_120D3___Active_Radar_AAM = {
        "clsid": "{LAU_115_2xAIM-120D-3}",
        "name": "2x AIM-120D3 - Active Radar AAM",
        "weight": 380,
    }
    _2x_AIM_260A___Active_Radar_AAM = {
        "clsid": "{LAU_115_2xAIM-260A}",
        "name": "2x AIM-260A - Active Radar AAM",
        "weight": 370,
    }
    IRST_Sensor_Pod = {
        "clsid": "{IRST_SENSOR_Pod}",
        "name": "IRST Sensor Pod",
        "weight": 105,
    }
    Mako_Multi_Mission_Hypersonic_Missile___Active_Radar_AAM = {
        "clsid": "{MAKO_A2A_C}",
        "name": "Mako Multi-Mission Hypersonic Missile - Active Radar AAM",
        "weight": 160,
    }


inject_weapons(F22AWeapons)


@planemod
class F_22A(PlaneType):
    id = "F-22A"
    flyable = True
    height = 4.88
    width = 13.05
    length = 19.1
    fuel_max = 8200
    max_speed = 2649.996
    chaff = 120
    flare = 120
    charge_total = 240
    chaff_charge_size = 1
    flare_charge_size = 2
    eplrs = True
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    property_defaults: Dict[str, Any] = {
        "BAY_DOOR_OPTION": False,
    }

    class Properties:
        class BAY_DOOR_OPTION:
            id = "BAY_DOOR_OPTION"

    livery_name = "F-22A"  # from type

    class Pylon1:
        AIM_9X_Sidewinder_IR_AAM = (1, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_9M_Sidewinder_IR_AAM = (1, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM9X_BLKII_Sidewinder_IR_AAM = (1, F22AWeapons.AIM9X_BLKII_Sidewinder_IR_AAM)

    class Pylon2:
        Fuel_tank_610_gal = (2, Weapons.Fuel_tank_610_gal)
        LDTP_Fuel_tank_600_gal = (2, F22AWeapons.LDTP_Fuel_tank_600_gal)
        AIM_9X_Sidewinder_IR_AAM = (2, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_9M_Sidewinder_IR_AAM = (2, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            2,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            2,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C7___Active_Radar_AAM = (2, F22AWeapons.AIM_120C7___Active_Radar_AAM)
        AIM_120C8___Active_Radar_AAM = (2, F22AWeapons.AIM_120C8___Active_Radar_AAM)
        AIM_120D3___Active_Radar_AAM = (2, F22AWeapons.AIM_120D3___Active_Radar_AAM)
        # ERRR {LAU_115_2xAIM9X-II}}
        _2x_AIM_120C7___Active_Radar_AAM = (
            2,
            F22AWeapons._2x_AIM_120C7___Active_Radar_AAM,
        )
        _2x_AIM_120C8___Active_Radar_AAM = (
            2,
            F22AWeapons._2x_AIM_120C8___Active_Radar_AAM,
        )
        _2x_AIM_120D3___Active_Radar_AAM = (
            2,
            F22AWeapons._2x_AIM_120D3___Active_Radar_AAM,
        )
        _2x_AIM_260A___Active_Radar_AAM = (
            2,
            F22AWeapons._2x_AIM_260A___Active_Radar_AAM,
        )

    class Pylon3:
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            3,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            3,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C7___Active_Radar_AAM = (3, F22AWeapons.AIM_120C7___Active_Radar_AAM)
        AIM_120C8___Active_Radar_AAM = (3, F22AWeapons.AIM_120C8___Active_Radar_AAM)
        AIM_120D3___Active_Radar_AAM = (3, F22AWeapons.AIM_120D3___Active_Radar_AAM)
        AIM_260A___Active_Radar_AAM = (3, F22AWeapons.AIM_260A___Active_Radar_AAM)

    class Pylon4:
        IRST_Sensor_Pod = (4, F22AWeapons.IRST_Sensor_Pod)
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            4,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            4,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C7___Active_Radar_AAM = (4, F22AWeapons.AIM_120C7___Active_Radar_AAM)
        AIM_120C8___Active_Radar_AAM = (4, F22AWeapons.AIM_120C8___Active_Radar_AAM)
        AIM_120D3___Active_Radar_AAM = (4, F22AWeapons.AIM_120D3___Active_Radar_AAM)
        AIM_260A___Active_Radar_AAM = (4, F22AWeapons.AIM_260A___Active_Radar_AAM)
        Mako_Multi_Mission_Hypersonic_Missile___Active_Radar_AAM = (
            4,
            F22AWeapons.Mako_Multi_Mission_Hypersonic_Missile___Active_Radar_AAM,
        )
        AIM_120C7___Active_Radar_AAM__IRST_POD = (
            4,
            F22AWeapons.AIM_120C7___Active_Radar_AAM__IRST_POD,
        )
        AIM_120C8___Active_Radar_AAM__IRST_POD = (
            4,
            F22AWeapons.AIM_120C8___Active_Radar_AAM__IRST_POD,
        )
        AIM_120D3___Active_Radar_AAM__IRST_POD = (
            4,
            F22AWeapons.AIM_120D3___Active_Radar_AAM__IRST_POD,
        )
        AIM_260A___Active_Radar_AAM__IRST_POD = (
            4,
            F22AWeapons.AIM_260A___Active_Radar_AAM__IRST_POD,
        )

    class Pylon5:
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            5,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            5,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C7___Active_Radar_AAM = (5, F22AWeapons.AIM_120C7___Active_Radar_AAM)
        AIM_120C8___Active_Radar_AAM = (5, F22AWeapons.AIM_120C8___Active_Radar_AAM)
        AIM_120D3___Active_Radar_AAM = (5, F22AWeapons.AIM_120D3___Active_Radar_AAM)
        AIM_260A___Active_Radar_AAM = (5, F22AWeapons.AIM_260A___Active_Radar_AAM)
        Mako_Multi_Mission_Hypersonic_Missile___Active_Radar_AAM = (
            5,
            F22AWeapons.Mako_Multi_Mission_Hypersonic_Missile___Active_Radar_AAM,
        )

    class Pylon6:
        Smokewinder___red = (6, Weapons.Smokewinder___red)
        Smokewinder___green = (6, Weapons.Smokewinder___green)
        Smokewinder___blue = (6, Weapons.Smokewinder___blue)
        Smokewinder___white = (6, Weapons.Smokewinder___white)
        Smokewinder___yellow = (6, Weapons.Smokewinder___yellow)

    class Pylon7:
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            7,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            7,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C7___Active_Radar_AAM = (7, Weapons.AIM_120C7___Active_Radar_AAM)
        AIM_120C8___Active_Radar_AAM = (7, Weapons.AIM_120C8___Active_Radar_AAM)
        AIM_120D3___Active_Radar_AAM = (7, Weapons.AIM_120D3___Active_Radar_AAM)
        AIM_260A___Active_Radar_AAM = (7, Weapons.AIM_260A___Active_Radar_AAM)
        Mako_Multi_Mission_Hypersonic_Missile___Active_Radar_AAM = (
            7,
            Weapons.Mako_Multi_Mission_Hypersonic_Missile___Active_Radar_AAM,
        )

    class Pylon8:
        IRST_Sensor_Pod = (8, F22AWeapons.IRST_Sensor_Pod)
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            8,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            8,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C7___Active_Radar_AAM = (8, Weapons.AIM_120C7___Active_Radar_AAM)
        AIM_120C8___Active_Radar_AAM = (8, Weapons.AIM_120C8___Active_Radar_AAM)
        AIM_120D3___Active_Radar_AAM = (8, Weapons.AIM_120D3___Active_Radar_AAM)
        AIM_260A___Active_Radar_AAM = (8, Weapons.AIM_260A___Active_Radar_AAM)
        Mako_Multi_Mission_Hypersonic_Missile___Active_Radar_AAM = (
            8,
            Weapons.Mako_Multi_Mission_Hypersonic_Missile___Active_Radar_AAM,
        )
        AIM_120C7___Active_Radar_AAM__IRST_POD_ = (
            8,
            Weapons.AIM_120C7___Active_Radar_AAM__IRST_POD_,
        )
        AIM_120C8___Active_Radar_AAM__IRST_POD_ = (
            8,
            Weapons.AIM_120C8___Active_Radar_AAM__IRST_POD_,
        )
        AIM_120D3___Active_Radar_AAM__IRST_POD_ = (
            8,
            Weapons.AIM_120D3___Active_Radar_AAM__IRST_POD_,
        )
        AIM_260A___Active_Radar_AAM__IRST_POD_ = (
            8,
            Weapons.AIM_260A___Active_Radar_AAM__IRST_POD_,
        )

    class Pylon9:
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            9,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            9,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C7___Active_Radar_AAM = (9, Weapons.AIM_120C7___Active_Radar_AAM)
        AIM_120C8___Active_Radar_AAM = (9, Weapons.AIM_120C8___Active_Radar_AAM)
        AIM_120D3___Active_Radar_AAM = (9, Weapons.AIM_120D3___Active_Radar_AAM)
        AIM_260A___Active_Radar_AAM = (9, Weapons.AIM_260A___Active_Radar_AAM)

    class Pylon10:
        Fuel_tank_610_gal = (10, Weapons.Fuel_tank_610_gal)
        LDTP_Fuel_tank_600_gal = (10, F22AWeapons.LDTP_Fuel_tank_600_gal)
        AIM_9X_Sidewinder_IR_AAM = (10, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_9M_Sidewinder_IR_AAM = (10, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            10,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            10,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C7___Active_Radar_AAM = (10, Weapons.AIM_120C7___Active_Radar_AAM)
        AIM_120C8___Active_Radar_AAM = (10, Weapons.AIM_120C8___Active_Radar_AAM)
        AIM_120D3___Active_Radar_AAM = (10, Weapons.AIM_120D3___Active_Radar_AAM)
        _2x_AIM9X_BLKII_Sidewinder_IR_AAM = (
            10,
            F22AWeapons._2x_AIM9X_BLKII_Sidewinder_IR_AAM,
        )
        _2x_AIM_120C7___Active_Radar_AAM = (
            10,
            F22AWeapons._2x_AIM_120C7___Active_Radar_AAM,
        )
        _2x_AIM_120C8___Active_Radar_AAM = (
            10,
            F22AWeapons._2x_AIM_120C8___Active_Radar_AAM,
        )
        _2x_AIM_120D3___Active_Radar_AAM = (
            10,
            F22AWeapons._2x_AIM_120D3___Active_Radar_AAM,
        )
        _2x_AIM_260A___Active_Radar_AAM = (
            10,
            F22AWeapons._2x_AIM_260A___Active_Radar_AAM,
        )

    class Pylon11:
        AIM_9X_Sidewinder_IR_AAM = (11, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_9M_Sidewinder_IR_AAM = (11, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM9X_BLKII_Sidewinder_IR_AAM = (11, F22AWeapons.AIM9X_BLKII_Sidewinder_IR_AAM)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.Reconnaissance,
    ]
    task_default = task.CAP
