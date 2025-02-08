from typing import Set

from dcs import task
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

from game.modsupport import planemod
from pydcs_extensions.weapon_injector import inject_weapons


class WeaponsF106:
    Fuel_Tank = {"clsid": "{VSN_F106L_PTB}", "name": "Fuel Tank", "weight": 1187}
    Fuel_Tank_ = {"clsid": "{VSN_F106R_PTB}", "name": "Fuel Tank", "weight": 1187}
    AIM_4D_Rear_aspect_advanced_heat_seeking_air_to_air_missile_ = {
        "clsid": "{Hughes AIM-4D}",
        "name": "AIM-4D Rear aspect advanced heat-seeking air-to-air missile.",
        "weight": 60.8,
    }
    AIM_4F_Semi_active_radar_homing_air_to_air_missile_ = {
        "clsid": "{Hughes AIM-4F}",
        "name": "AIM-4F Semi active radar-homing air-to-air missile.",
        "weight": 66,
    }
    AIM_4G_Rear_aspect_heat_seeking_air_to_air_missile_ = {
        "clsid": "{Hughes AIM-4G}",
        "name": "AIM-4G Rear aspect heat seeking air-to-air missile.",
        "weight": 66,
    }
    AIR_2A_Genie_Nuclear_air_to_air_unguided_rocket_ = {
        "clsid": "{AIR-2A}",
        "name": "AIR-2A Genie Nuclear air-to-air unguided rocket.",
        "weight": 66,
    }


inject_weapons(WeaponsF106)


@planemod
class VSN_F106A(PlaneType):
    id = "VSN_F106A"
    flyable = True
    height = 6.18
    width = 11.67
    length = 21.56
    fuel_max = 4464
    max_speed = 2452.032
    chaff = 90
    flare = 45
    charge_total = 180
    chaff_charge_size = 1
    flare_charge_size = 2
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    livery_name = "VSN_F106A"  # from type

    class Pylon1:
        Smokewinder___red = (1, Weapons.Smokewinder___red)
        Smokewinder___green = (1, Weapons.Smokewinder___green)
        Smokewinder___blue = (1, Weapons.Smokewinder___blue)
        Smokewinder___white = (1, Weapons.Smokewinder___white)
        Smokewinder___yellow = (1, Weapons.Smokewinder___yellow)
        Fuel_Tank = (1, WeaponsF106.Fuel_Tank)

    # ERRR <CLEAN>

    class Pylon2:
        AIM_4D_Rear_aspect_advanced_heat_seeking_air_to_air_missile_ = (
            2,
            WeaponsF106.AIM_4D_Rear_aspect_advanced_heat_seeking_air_to_air_missile_,
        )
        AIM_4F_Semi_active_radar_homing_air_to_air_missile_ = (
            2,
            WeaponsF106.AIM_4F_Semi_active_radar_homing_air_to_air_missile_,
        )
        AIM_4G_Rear_aspect_heat_seeking_air_to_air_missile_ = (
            2,
            WeaponsF106.AIM_4G_Rear_aspect_heat_seeking_air_to_air_missile_,
        )

    class Pylon3:
        AIM_4D_Rear_aspect_advanced_heat_seeking_air_to_air_missile_ = (
            3,
            WeaponsF106.AIM_4D_Rear_aspect_advanced_heat_seeking_air_to_air_missile_,
        )
        AIM_4F_Semi_active_radar_homing_air_to_air_missile_ = (
            3,
            WeaponsF106.AIM_4F_Semi_active_radar_homing_air_to_air_missile_,
        )
        AIM_4G_Rear_aspect_heat_seeking_air_to_air_missile_ = (
            3,
            WeaponsF106.AIM_4G_Rear_aspect_heat_seeking_air_to_air_missile_,
        )

    class Pylon4:
        AIR_2A_Genie_Nuclear_air_to_air_unguided_rocket_ = (
            4,
            WeaponsF106.AIR_2A_Genie_Nuclear_air_to_air_unguided_rocket_,
        )

    # ERRR <CLEAN>

    class Pylon5:
        AIM_4D_Rear_aspect_advanced_heat_seeking_air_to_air_missile_ = (
            5,
            WeaponsF106.AIM_4D_Rear_aspect_advanced_heat_seeking_air_to_air_missile_,
        )
        AIM_4F_Semi_active_radar_homing_air_to_air_missile_ = (
            5,
            WeaponsF106.AIM_4F_Semi_active_radar_homing_air_to_air_missile_,
        )
        AIM_4G_Rear_aspect_heat_seeking_air_to_air_missile_ = (
            5,
            WeaponsF106.AIM_4G_Rear_aspect_heat_seeking_air_to_air_missile_,
        )

    class Pylon6:
        AIM_4D_Rear_aspect_advanced_heat_seeking_air_to_air_missile_ = (
            6,
            WeaponsF106.AIM_4D_Rear_aspect_advanced_heat_seeking_air_to_air_missile_,
        )
        AIM_4F_Semi_active_radar_homing_air_to_air_missile_ = (
            6,
            WeaponsF106.AIM_4F_Semi_active_radar_homing_air_to_air_missile_,
        )
        AIM_4G_Rear_aspect_heat_seeking_air_to_air_missile_ = (
            6,
            WeaponsF106.AIM_4G_Rear_aspect_heat_seeking_air_to_air_missile_,
        )

    class Pylon7:
        Smokewinder___red = (7, Weapons.Smokewinder___red)
        Smokewinder___green = (7, Weapons.Smokewinder___green)
        Smokewinder___blue = (7, Weapons.Smokewinder___blue)
        Smokewinder___white = (7, Weapons.Smokewinder___white)
        Smokewinder___yellow = (7, Weapons.Smokewinder___yellow)
        Fuel_Tank_ = (7, WeaponsF106.Fuel_Tank_)

    # ERRR <CLEAN>

    class Pylon8:
        L005_Sorbtsiya_ECM_pod__left_ = (
            8,
            Weapons.L005_Sorbtsiya_ECM_pod__left_,
        )

    class Pylon9:
        Smoke_Generator___red_ = (9, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (9, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (9, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (9, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (9, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (9, Weapons.Smoke_Generator___orange_)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.Reconnaissance,
    ]
    task_default = task.FighterSweep


@planemod
class VSN_F106B(PlaneType):
    id = "VSN_F106B"
    flyable = True
    height = 6.18
    width = 11.67
    length = 21.56
    fuel_max = 4464
    max_speed = 2452.032
    chaff = 90
    flare = 45
    charge_total = 180
    chaff_charge_size = 1
    flare_charge_size = 2
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    livery_name = "VSN_F106B"  # from type

    class Pylon1:
        Smokewinder___red = (1, Weapons.Smokewinder___red)
        Smokewinder___green = (1, Weapons.Smokewinder___green)
        Smokewinder___blue = (1, Weapons.Smokewinder___blue)
        Smokewinder___white = (1, Weapons.Smokewinder___white)
        Smokewinder___yellow = (1, Weapons.Smokewinder___yellow)
        Fuel_Tank = (1, WeaponsF106.Fuel_Tank)

    # ERRR <CLEAN>

    class Pylon2:
        AIM_4D_Rear_aspect_advanced_heat_seeking_air_to_air_missile_ = (
            2,
            WeaponsF106.AIM_4D_Rear_aspect_advanced_heat_seeking_air_to_air_missile_,
        )
        AIM_4F_Semi_active_radar_homing_air_to_air_missile_ = (
            2,
            WeaponsF106.AIM_4F_Semi_active_radar_homing_air_to_air_missile_,
        )
        AIM_4G_Rear_aspect_heat_seeking_air_to_air_missile_ = (
            2,
            WeaponsF106.AIM_4G_Rear_aspect_heat_seeking_air_to_air_missile_,
        )

    class Pylon3:
        AIM_4D_Rear_aspect_advanced_heat_seeking_air_to_air_missile_ = (
            3,
            WeaponsF106.AIM_4D_Rear_aspect_advanced_heat_seeking_air_to_air_missile_,
        )
        AIM_4F_Semi_active_radar_homing_air_to_air_missile_ = (
            3,
            WeaponsF106.AIM_4F_Semi_active_radar_homing_air_to_air_missile_,
        )
        AIM_4G_Rear_aspect_heat_seeking_air_to_air_missile_ = (
            3,
            WeaponsF106.AIM_4G_Rear_aspect_heat_seeking_air_to_air_missile_,
        )

    class Pylon4:
        AIR_2A_Genie_Nuclear_air_to_air_unguided_rocket_ = (
            4,
            WeaponsF106.AIR_2A_Genie_Nuclear_air_to_air_unguided_rocket_,
        )

    # ERRR <CLEAN>

    class Pylon5:
        AIM_4D_Rear_aspect_advanced_heat_seeking_air_to_air_missile_ = (
            5,
            WeaponsF106.AIM_4D_Rear_aspect_advanced_heat_seeking_air_to_air_missile_,
        )
        AIM_4F_Semi_active_radar_homing_air_to_air_missile_ = (
            5,
            WeaponsF106.AIM_4F_Semi_active_radar_homing_air_to_air_missile_,
        )
        AIM_4G_Rear_aspect_heat_seeking_air_to_air_missile_ = (
            5,
            WeaponsF106.AIM_4G_Rear_aspect_heat_seeking_air_to_air_missile_,
        )

    class Pylon6:
        AIM_4D_Rear_aspect_advanced_heat_seeking_air_to_air_missile_ = (
            6,
            WeaponsF106.AIM_4D_Rear_aspect_advanced_heat_seeking_air_to_air_missile_,
        )
        AIM_4F_Semi_active_radar_homing_air_to_air_missile_ = (
            6,
            WeaponsF106.AIM_4F_Semi_active_radar_homing_air_to_air_missile_,
        )
        AIM_4G_Rear_aspect_heat_seeking_air_to_air_missile_ = (
            6,
            WeaponsF106.AIM_4G_Rear_aspect_heat_seeking_air_to_air_missile_,
        )

    class Pylon7:
        Smokewinder___red = (7, Weapons.Smokewinder___red)
        Smokewinder___green = (7, Weapons.Smokewinder___green)
        Smokewinder___blue = (7, Weapons.Smokewinder___blue)
        Smokewinder___white = (7, Weapons.Smokewinder___white)
        Smokewinder___yellow = (7, Weapons.Smokewinder___yellow)
        Fuel_Tank_ = (7, WeaponsF106.Fuel_Tank_)

    # ERRR <CLEAN>

    class Pylon8:
        L005_Sorbtsiya_ECM_pod__left_ = (
            8,
            Weapons.L005_Sorbtsiya_ECM_pod__left_,
        )

    class Pylon9:
        Smoke_Generator___red_ = (9, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (9, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (9, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (9, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (9, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (9, Weapons.Smoke_Generator___orange_)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.Reconnaissance,
    ]
    task_default = task.FighterSweep
