from typing import Set

from dcs import task
from dcs.helicopters import HelicopterType

from game.modsupport import helicoptermod


@helicoptermod
class seaking_sikorsky_sh_3h(HelicopterType):
    id = "seaking_sikorsky_sh_3h"
    height = 5.13
    width = 18.91
    length = 16.495
    fuel_max = 2296
    max_speed = 250
    category = "Air"  # {828CEADE-3F1D-40aa-93CE-8CDB73FE2710}
    radio_frequency = 124

    livery_name = "SEAKING_SIKORSKY_SH_3H"  # from type

    pylons: Set[int] = set()

    tasks = [
        task.CAS,
        task.GroundAttack,
        task.Escort,
        task.AFAC,
        task.AntishipStrike,
        task.Transport,
        task.Reconnaissance,
    ]
    task_default = task.CAS


@helicoptermod
class seaking_westland_mk48(HelicopterType):
    id = "seaking_westland_mk48"
    height = 5.13
    width = 18.91
    length = 16.495
    fuel_max = 2296
    max_speed = 250
    category = "Air"  # {828CEADE-3F1D-40aa-93CE-8CDB73FE2710}
    radio_frequency = 124

    livery_name = "SEAKING_WESTLAND_MK48"  # from type

    pylons: Set[int] = set()

    tasks = [
        task.CAS,
        task.GroundAttack,
        task.Escort,
        task.AFAC,
        task.AntishipStrike,
        task.Transport,
        task.Reconnaissance,
    ]
    task_default = task.CAS


@helicoptermod
class sikorsky_seaking_static(HelicopterType):
    id = "sikorsky_seaking_static"
    height = 5.13
    width = 18.91
    length = 16.495
    fuel_max = 2296
    max_speed = 250
    category = "Air"  # {828CEADE-3F1D-40aa-93CE-8CDB73FE2710}
    radio_frequency = 124

    livery_name = "SIKORSKY_SEAKING_STATIC"  # from type

    pylons: Set[int] = set()

    tasks = [
        task.CAS,
        task.GroundAttack,
        task.Escort,
        task.AFAC,
        task.AntishipStrike,
        task.Transport,
        task.Reconnaissance,
    ]
    task_default = task.CAS


@helicoptermod
class westland_seaking_static(HelicopterType):
    id = "westland_seaking_static"
    height = 5.13
    width = 18.91
    length = 16.495
    fuel_max = 2296
    max_speed = 250
    category = "Air"  # {828CEADE-3F1D-40aa-93CE-8CDB73FE2710}
    radio_frequency = 124

    livery_name = "WESTLAND_SEAKING_STATIC"  # from type

    pylons: Set[int] = set()

    tasks = [
        task.CAS,
        task.GroundAttack,
        task.Escort,
        task.AFAC,
        task.AntishipStrike,
        task.Transport,
        task.Reconnaissance,
    ]
    task_default = task.CAS
