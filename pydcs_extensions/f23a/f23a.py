from typing import Set

from dcs import task
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

from game.modsupport import planemod


@planemod
class F_23A(PlaneType):
    id = "F-23A"
    flyable = True
    height = 4.47
    width = 13.28
    length = 20.99
    fuel_max = 8870
    max_speed = 2520
    chaff = 120
    flare = 120
    charge_total = 240
    chaff_charge_size = 1
    flare_charge_size = 2
    eplrs = True
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 124

    livery_name = "F-23A"  # from type

    class Pylon1:
        AIM_9X_Sidewinder_IR_AAM = (1, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_9M_Sidewinder_IR_AAM = (1, Weapons.AIM_9M_Sidewinder_IR_AAM)

    class Pylon3:
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            3,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )

    class Pylon4:
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            4,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )

    class Pylon5:
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            5,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )

    class Pylon6:
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            6,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )

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

    class Pylon10:
        AIM_9M_Sidewinder_IR_AAM = (10, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (10, Weapons.AIM_9X_Sidewinder_IR_AAM)

    pylons: Set[int] = {1, 3, 4, 5, 6, 7, 8, 10}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.Reconnaissance,
    ]
    task_default = task.CAP
