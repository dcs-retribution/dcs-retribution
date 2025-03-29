from typing import Set

from dcs import task
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

from game.modsupport import planemod
from pydcs_extensions.weapon_injector import inject_weapons


@planemod
class CLP_E7A(PlaneType):
    id = "CLP_E7A"
    large_parking_slot = True
    height = 12.5
    width = 34
    length = 35.5
    fuel_max = 90700
    max_speed = 1009.008
    chaff = 120
    flare = 60
    charge_total = 240
    chaff_charge_size = 1
    flare_charge_size = 2
    eplrs = True
    radio_frequency = 243

    livery_name = "CLP_E7A"  # from type

    pylons: Set[int] = set()

    tasks = [task.AWACS]
    task_default = task.AWACS
