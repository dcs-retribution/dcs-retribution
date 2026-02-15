# Requires Vietnam War Vessels for DCS by TeTeT:
# https://forum.dcs.world/topic/338387-tetets-vietnam-war-vessels/
# https://github.com/tspindler-cms/tetet-vwv/releases


from typing import Set, Dict, Any

from dcs import unittype, task
from dcs.planes import PlaneType
from dcs.helicopters import HelicopterType
from dcs.weapons_data import Weapons
from dcs.unitpropertydescription import UnitPropertyDescription

from game.modsupport import shipmod, planemod, helicoptermod, vehiclemod, cargomod
from pydcs_extensions.weapon_injector import inject_weapons


class WeaponsVWV:
    AN_M81___260lb_GP_Bomb_LD = {
        "clsid": "{AN-M81}",
        "name": "AN-M81 - 260lb GP Bomb LD",
        "weight": 117.93392,  # [kg]
    }
    AN_M88___220lb_GP_Bomb_LD = {
        "clsid": "{AN-M88}",
        "name": "AN-M88 - 220lb GP Bomb LD",
        "weight": 98.0665904,
    }
    Fuel_Tank_150_gallons = {
        "clsid": "{DFT-150gal}",
        "name": "Fuel Tank 150 gallons",
        "weight": 515.888512,
    }
    Fuel_Tank_150_gallons__EMPTY_ = {
        "clsid": "{DFT-150gal_EMPTY}",
        "name": "Fuel Tank 150 gallons (EMPTY)",
        "weight": 515.888512,
    }
    Fuel_Tank_300_gallons = {
        "clsid": "{DFT-300gal}",
        "name": "Fuel Tank 300 gallons",
        "weight": 991.407336,
    }
    Fuel_Tank_300_gallons_ = {
        "clsid": "{DFT-300gal_LR}",
        "name": "Fuel Tank 300 gallons",
        "weight": 998.664808,
    }
    Fuel_Tank_300_gallons__EMPTY_ = {
        "clsid": "{DFT-300gal_EMPTY}",
        "name": "Fuel Tank 300 gallons (EMPTY)",
        "weight": 991.407336,
    }
    Fuel_Tank_300_gallons__EMPTY__ = {
        "clsid": "{DFT-300gal_LR_EMPTY}",
        "name": "Fuel Tank 300 gallons (EMPTY)",
        "weight": 998.664808,
    }
    BRU_41A_with_4_x_Mk_82___500lb_GP_Bomb_HD_Left = {
        "clsid": "{Mk-82_IMER_4_L}",
        "name": "4 x Mk-82 - 500 lbs GP Bomb HD (IMER)",
        "weight": 1035.1,  # BRU-41/A (IMER) = 282 lbs
    }
    BRU_41A_with_4_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_Left = {
        "clsid": "{Mk-82_Snakeye_IMER_4_L}",
        "name": "4 x Mk-82 Snakeye - 500 lbs GP Bomb HD (IMER)",
        "weight": 1035.1,  # BRU-41/A (IMER) = 282 lbs
    }
    BRU_41A_with_4_x_Mk_82___500lb_GP_Bomb_HD_Right = {
        "clsid": "{Mk-82_IMER_4_R}",
        "name": "4 x Mk-82 - 500 lbs GP Bomb HD (IMER)",
        "weight": 1035.1,  # BRU-41/A (IMER) = 282 lbs
    }
    BRU_41A_with_4_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_Right = {
        "clsid": "{Mk-82_Snakeye_IMER_4_R}",
        "name": "4 x Mk-82 Snakeye - 500 lbs GP Bomb HD (IMER)",
        "weight": 1035.1,  # BRU-41/A (IMER) = 282 lbs
    }
    AIM_9C_Sidewinder_SARH_AAM = {
        "clsid": "{AIM-9C}",
        "name": "AIM-9C Sidewinder SARH AAM",
        "weight": 95,
    }
    AIM_9D_Sidewinder_IR_AAM = {
        "clsid": "{AIM-9D}",
        "name": "AIM-9D Sidewinder IR AAM",
        "weight": 74,
    }
    # In October 1965, to highlight the dropping of the six millionth pound of ordnance,
    # Commander Clarence J. Stoddard of VA-25, flying an A-1H, dropped a special,
    # one-time-only object in addition to his other munitions – a toilet. (Wikipedia)
    toilet_bomb = {
        "clsid": "{toilet_bomb}",
        "name": "Toilet",
        "weight": 10,
    }
    Tiny_Tim = {
        "clsid": "{Tiny_Tim}",
        "name": "Tiny Tim air-to-ground Rocket",
        "weight": 569,
    }
    ab_212_cable = {
        "clsid": "{ab_212_cable}",
        "name": "AB 212 Cable",
        "weight": 5,
    }
    rescue_crew_sling = {
        "clsid": "{rescue_crew_sling}",
        "name": "Rescue Crew Sling",
        "weight": 5,
    }
    uscg_stretcher = {
        "clsid": "{uscg_stretcher}",
        "name": "US Coast Guard Rescue Stretcher",
        "weight": 10,
    }
    dragonfly_fuel_tanks = {
        "clsid": "dragonfly_fuel_tanks",
        "name": "A-37 Fuel Tank",
        "weight": 466,
    }
    SH2F_Fuel_Tank_120_gallons_L = {
        "clsid": "{SH2F_FUEL_TANK_120L}",
        "name": "SH2F Fuel Tank 120 gallons L",
        "weight": 245.428515,
    }
    SH2F_Fuel_Tank_120_gallons_R = {
        "clsid": "{SH2F_FUEL_TANK_120R}",
        "name": "SH2F Fuel Tank 120 gallons R",
        "weight": 245.428515,
    }
    SH2F_MAD = {
        "clsid": "{SH2F_MAD}",
        "name": "SH2F_MAD",
        "weight": 0,
    }


inject_weapons(WeaponsVWV)


## AIRPLANES


@planemod
class vwv_a1_skyraider(PlaneType):
    id = "vwv_a1_skyraider"
    height = 4.77
    width = 15.24
    length = 11.84
    fuel_max = 1036
    max_speed = 522
    chaff = 0
    flare = 0
    charge_total = 0
    chaff_charge_size = 0
    flare_charge_size = 0

    livery_name = "VWV_A1_SKYRAIDER"  # from type

    class Pylon1:
        AN_M30A1___100lb_GP_Bomb_LD = (1, Weapons.AN_M30A1___100lb_GP_Bomb_LD)
        AN_M57___250lb_GP_Bomb_LD = (1, Weapons.AN_M57___250lb_GP_Bomb_LD)
        AN_M81___260lb_GP_Bomb_LD = (1, WeaponsVWV.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (1, WeaponsVWV.AN_M88___220lb_GP_Bomb_LD)
        AN_M64___500lb_GP_Bomb_LD = (1, Weapons.AN_M64___500lb_GP_Bomb_LD)
        Mk_82___500lb_GP_Bomb_LD = (1, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            1,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE = (
            1,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM = (
            1,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        _3_x_4_5_inch_M8_UnGd_Rocket = (1, Weapons._3_x_4_5_inch_M8_UnGd_Rocket)
        SUU_25_x_8_LUU_2___Target_Marker_Flares = (
            1,
            Weapons.SUU_25_x_8_LUU_2___Target_Marker_Flares,
        )
        HVAR__UnGd_Rkt = (1, Weapons.HVAR__UnGd_Rkt)

    class Pylon2:
        AN_M30A1___100lb_GP_Bomb_LD = (2, Weapons.AN_M30A1___100lb_GP_Bomb_LD)
        AN_M57___250lb_GP_Bomb_LD = (2, Weapons.AN_M57___250lb_GP_Bomb_LD)
        AN_M81___260lb_GP_Bomb_LD = (2, WeaponsVWV.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (2, WeaponsVWV.AN_M88___220lb_GP_Bomb_LD)
        AN_M64___500lb_GP_Bomb_LD = (2, Weapons.AN_M64___500lb_GP_Bomb_LD)
        Mk_82___500lb_GP_Bomb_LD = (2, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            2,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE = (
            2,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM = (
            2,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        _3_x_4_5_inch_M8_UnGd_Rocket = (2, Weapons._3_x_4_5_inch_M8_UnGd_Rocket)
        SUU_25_x_8_LUU_2___Target_Marker_Flares = (
            2,
            Weapons.SUU_25_x_8_LUU_2___Target_Marker_Flares,
        )
        HVAR__UnGd_Rkt = (2, Weapons.HVAR__UnGd_Rkt)

    class Pylon3:
        AN_M30A1___100lb_GP_Bomb_LD = (3, Weapons.AN_M30A1___100lb_GP_Bomb_LD)
        AN_M57___250lb_GP_Bomb_LD = (3, Weapons.AN_M57___250lb_GP_Bomb_LD)
        AN_M81___260lb_GP_Bomb_LD = (3, WeaponsVWV.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (3, WeaponsVWV.AN_M88___220lb_GP_Bomb_LD)
        AN_M64___500lb_GP_Bomb_LD = (3, Weapons.AN_M64___500lb_GP_Bomb_LD)
        Mk_82___500lb_GP_Bomb_LD = (3, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            3,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE = (
            3,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM = (
            3,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        _3_x_4_5_inch_M8_UnGd_Rocket = (3, Weapons._3_x_4_5_inch_M8_UnGd_Rocket)
        SUU_25_x_8_LUU_2___Target_Marker_Flares = (
            3,
            Weapons.SUU_25_x_8_LUU_2___Target_Marker_Flares,
        )
        HVAR__UnGd_Rkt = (3, Weapons.HVAR__UnGd_Rkt)

    class Pylon4:
        AN_M30A1___100lb_GP_Bomb_LD = (4, Weapons.AN_M30A1___100lb_GP_Bomb_LD)
        AN_M57___250lb_GP_Bomb_LD = (4, Weapons.AN_M57___250lb_GP_Bomb_LD)
        AN_M81___260lb_GP_Bomb_LD = (4, WeaponsVWV.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (4, WeaponsVWV.AN_M88___220lb_GP_Bomb_LD)
        AN_M64___500lb_GP_Bomb_LD = (4, Weapons.AN_M64___500lb_GP_Bomb_LD)
        Mk_82___500lb_GP_Bomb_LD = (4, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            4,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE = (
            4,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM = (
            4,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        _3_x_4_5_inch_M8_UnGd_Rocket = (4, Weapons._3_x_4_5_inch_M8_UnGd_Rocket)
        SUU_25_x_8_LUU_2___Target_Marker_Flares = (
            4,
            Weapons.SUU_25_x_8_LUU_2___Target_Marker_Flares,
        )
        HVAR__UnGd_Rkt = (4, Weapons.HVAR__UnGd_Rkt)

    class Pylon5:
        AN_M30A1___100lb_GP_Bomb_LD = (5, Weapons.AN_M30A1___100lb_GP_Bomb_LD)
        AN_M57___250lb_GP_Bomb_LD = (5, Weapons.AN_M57___250lb_GP_Bomb_LD)
        AN_M81___260lb_GP_Bomb_LD = (5, WeaponsVWV.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (5, WeaponsVWV.AN_M88___220lb_GP_Bomb_LD)
        AN_M64___500lb_GP_Bomb_LD = (5, Weapons.AN_M64___500lb_GP_Bomb_LD)
        Mk_82___500lb_GP_Bomb_LD = (5, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            5,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE = (
            5,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM = (
            5,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        _3_x_4_5_inch_M8_UnGd_Rocket = (5, Weapons._3_x_4_5_inch_M8_UnGd_Rocket)
        SUU_25_x_8_LUU_2___Target_Marker_Flares = (
            5,
            Weapons.SUU_25_x_8_LUU_2___Target_Marker_Flares,
        )
        HVAR__UnGd_Rkt = (5, Weapons.HVAR__UnGd_Rkt)

    class Pylon6:
        AN_M30A1___100lb_GP_Bomb_LD = (6, Weapons.AN_M30A1___100lb_GP_Bomb_LD)
        AN_M57___250lb_GP_Bomb_LD = (6, Weapons.AN_M57___250lb_GP_Bomb_LD)
        AN_M81___260lb_GP_Bomb_LD = (6, WeaponsVWV.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (6, WeaponsVWV.AN_M88___220lb_GP_Bomb_LD)
        AN_M64___500lb_GP_Bomb_LD = (6, Weapons.AN_M64___500lb_GP_Bomb_LD)
        Mk_82___500lb_GP_Bomb_LD = (6, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            6,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE = (
            6,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM = (
            6,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        _3_x_4_5_inch_M8_UnGd_Rocket = (6, Weapons._3_x_4_5_inch_M8_UnGd_Rocket)
        SUU_25_x_8_LUU_2___Target_Marker_Flares = (
            6,
            Weapons.SUU_25_x_8_LUU_2___Target_Marker_Flares,
        )
        HVAR__UnGd_Rkt = (6, Weapons.HVAR__UnGd_Rkt)

    class Pylon7:
        AN_M30A1___100lb_GP_Bomb_LD = (7, Weapons.AN_M30A1___100lb_GP_Bomb_LD)
        AN_M57___250lb_GP_Bomb_LD = (7, Weapons.AN_M57___250lb_GP_Bomb_LD)
        AN_M64___500lb_GP_Bomb_LD = (7, Weapons.AN_M64___500lb_GP_Bomb_LD)
        AN_M65___1000lb_GP_Bomb_LD = (7, Weapons.AN_M65___1000lb_GP_Bomb_LD)
        AN_M81___260lb_GP_Bomb_LD = (7, WeaponsVWV.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (7, WeaponsVWV.AN_M88___220lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (7, Weapons.M117___750lb_GP_Bomb_LD)
        Mk_82___500lb_GP_Bomb_LD = (7, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_83___1000lb_GP_Bomb_LD = (7, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        Mk_84___2000lb_GP_Bomb_LD = (7, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        SUU_25_x_8_LUU_2___Target_Marker_Flares = (
            7,
            Weapons.SUU_25_x_8_LUU_2___Target_Marker_Flares,
        )
        AERO_1D_300_Gallons_Fuel_Tank_ = (7, Weapons.AERO_1D_300_Gallons_Fuel_Tank_)
        Fuel_Tank_150_gallons = (7, WeaponsVWV.Fuel_Tank_150_gallons)
        Fuel_Tank_150_gallons__EMPTY_ = (7, WeaponsVWV.Fuel_Tank_150_gallons__EMPTY_)
        _3_x_4_5_inch_M8_UnGd_Rocket = (7, Weapons._3_x_4_5_inch_M8_UnGd_Rocket)
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM = (
            7,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE_ = (
            7,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE_,
        )
        LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE = (
            7,
            Weapons.LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE,
        )
        Tiny_Tim = (7, WeaponsVWV.Tiny_Tim)
        LTF_5b_Aerial_Torpedo = (7, Weapons.LTF_5b_Aerial_Torpedo)
        DIS_mk46torp = (7, Weapons.DIS_mk46torp)
        toilet_bomb = (7, WeaponsVWV.toilet_bomb)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            7,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )

    class Pylon8:
        AN_M30A1___100lb_GP_Bomb_LD = (8, Weapons.AN_M30A1___100lb_GP_Bomb_LD)
        AN_M57___250lb_GP_Bomb_LD = (8, Weapons.AN_M57___250lb_GP_Bomb_LD)
        AN_M64___500lb_GP_Bomb_LD = (8, Weapons.AN_M64___500lb_GP_Bomb_LD)
        AN_M65___1000lb_GP_Bomb_LD = (8, Weapons.AN_M65___1000lb_GP_Bomb_LD)
        AN_M81___260lb_GP_Bomb_LD = (8, WeaponsVWV.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (8, WeaponsVWV.AN_M88___220lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (8, Weapons.M117___750lb_GP_Bomb_LD)
        Mk_82___500lb_GP_Bomb_LD = (8, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_83___1000lb_GP_Bomb_LD = (8, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        Mk_84___2000lb_GP_Bomb_LD = (8, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        SUU_25_x_8_LUU_2___Target_Marker_Flares = (
            8,
            Weapons.SUU_25_x_8_LUU_2___Target_Marker_Flares,
        )
        AERO_1D_300_Gallons_Fuel_Tank_ = (8, Weapons.AERO_1D_300_Gallons_Fuel_Tank_)
        LTF_5b_Aerial_Torpedo = (8, Weapons.LTF_5b_Aerial_Torpedo)
        DIS_mk46torp = (8, Weapons.DIS_mk46torp)

    class Pylon9:
        AN_M30A1___100lb_GP_Bomb_LD = (9, Weapons.AN_M30A1___100lb_GP_Bomb_LD)
        AN_M57___250lb_GP_Bomb_LD = (9, Weapons.AN_M57___250lb_GP_Bomb_LD)
        AN_M64___500lb_GP_Bomb_LD = (9, Weapons.AN_M64___500lb_GP_Bomb_LD)
        AN_M65___1000lb_GP_Bomb_LD = (9, Weapons.AN_M65___1000lb_GP_Bomb_LD)
        AN_M81___260lb_GP_Bomb_LD = (9, WeaponsVWV.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (9, WeaponsVWV.AN_M88___220lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (9, Weapons.M117___750lb_GP_Bomb_LD)
        Mk_82___500lb_GP_Bomb_LD = (9, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_83___1000lb_GP_Bomb_LD = (9, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        Mk_84___2000lb_GP_Bomb_LD = (9, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        SUU_25_x_8_LUU_2___Target_Marker_Flares = (
            9,
            Weapons.SUU_25_x_8_LUU_2___Target_Marker_Flares,
        )
        AERO_1D_300_Gallons_Fuel_Tank_ = (9, Weapons.AERO_1D_300_Gallons_Fuel_Tank_)
        Fuel_Tank_150_gallons = (9, WeaponsVWV.Fuel_Tank_150_gallons)
        Fuel_Tank_150_gallons__EMPTY_ = (9, WeaponsVWV.Fuel_Tank_150_gallons__EMPTY_)
        _3_x_4_5_inch_M8_UnGd_Rocket = (9, Weapons._3_x_4_5_inch_M8_UnGd_Rocket)
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM = (
            9,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE_ = (
            9,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE_,
        )
        LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE = (
            9,
            Weapons.LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE,
        )
        Tiny_Tim = (9, WeaponsVWV.Tiny_Tim)
        LTF_5b_Aerial_Torpedo = (9, Weapons.LTF_5b_Aerial_Torpedo)
        DIS_mk46torp = (9, Weapons.DIS_mk46torp)
        toilet_bomb = (9, WeaponsVWV.toilet_bomb)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            9,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )

    class Pylon10:
        AN_M30A1___100lb_GP_Bomb_LD = (10, Weapons.AN_M30A1___100lb_GP_Bomb_LD)
        AN_M57___250lb_GP_Bomb_LD = (10, Weapons.AN_M57___250lb_GP_Bomb_LD)
        AN_M81___260lb_GP_Bomb_LD = (10, WeaponsVWV.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (10, WeaponsVWV.AN_M88___220lb_GP_Bomb_LD)
        AN_M64___500lb_GP_Bomb_LD = (10, Weapons.AN_M64___500lb_GP_Bomb_LD)
        Mk_82___500lb_GP_Bomb_LD = (10, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            10,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE = (
            10,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM = (
            10,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        _3_x_4_5_inch_M8_UnGd_Rocket = (10, Weapons._3_x_4_5_inch_M8_UnGd_Rocket)
        SUU_25_x_8_LUU_2___Target_Marker_Flares = (
            10,
            Weapons.SUU_25_x_8_LUU_2___Target_Marker_Flares,
        )
        HVAR__UnGd_Rkt = (10, Weapons.HVAR__UnGd_Rkt)

    class Pylon11:
        AN_M30A1___100lb_GP_Bomb_LD = (11, Weapons.AN_M30A1___100lb_GP_Bomb_LD)
        AN_M57___250lb_GP_Bomb_LD = (11, Weapons.AN_M57___250lb_GP_Bomb_LD)
        AN_M81___260lb_GP_Bomb_LD = (11, WeaponsVWV.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (11, WeaponsVWV.AN_M88___220lb_GP_Bomb_LD)
        AN_M64___500lb_GP_Bomb_LD = (11, Weapons.AN_M64___500lb_GP_Bomb_LD)
        Mk_82___500lb_GP_Bomb_LD = (11, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            11,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE = (
            11,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM = (
            11,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        _3_x_4_5_inch_M8_UnGd_Rocket = (11, Weapons._3_x_4_5_inch_M8_UnGd_Rocket)
        SUU_25_x_8_LUU_2___Target_Marker_Flares = (
            11,
            Weapons.SUU_25_x_8_LUU_2___Target_Marker_Flares,
        )
        HVAR__UnGd_Rkt = (11, Weapons.HVAR__UnGd_Rkt)

    class Pylon12:
        AN_M30A1___100lb_GP_Bomb_LD = (12, Weapons.AN_M30A1___100lb_GP_Bomb_LD)
        AN_M57___250lb_GP_Bomb_LD = (12, Weapons.AN_M57___250lb_GP_Bomb_LD)
        AN_M81___260lb_GP_Bomb_LD = (12, WeaponsVWV.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (12, WeaponsVWV.AN_M88___220lb_GP_Bomb_LD)
        AN_M64___500lb_GP_Bomb_LD = (12, Weapons.AN_M64___500lb_GP_Bomb_LD)
        Mk_82___500lb_GP_Bomb_LD = (12, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            12,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE = (
            12,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM = (
            12,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        _3_x_4_5_inch_M8_UnGd_Rocket = (12, Weapons._3_x_4_5_inch_M8_UnGd_Rocket)
        SUU_25_x_8_LUU_2___Target_Marker_Flares = (
            12,
            Weapons.SUU_25_x_8_LUU_2___Target_Marker_Flares,
        )
        HVAR__UnGd_Rkt = (12, Weapons.HVAR__UnGd_Rkt)

    class Pylon13:
        AN_M30A1___100lb_GP_Bomb_LD = (13, Weapons.AN_M30A1___100lb_GP_Bomb_LD)
        AN_M57___250lb_GP_Bomb_LD = (13, Weapons.AN_M57___250lb_GP_Bomb_LD)
        AN_M81___260lb_GP_Bomb_LD = (13, WeaponsVWV.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (13, WeaponsVWV.AN_M88___220lb_GP_Bomb_LD)
        AN_M64___500lb_GP_Bomb_LD = (13, Weapons.AN_M64___500lb_GP_Bomb_LD)
        Mk_82___500lb_GP_Bomb_LD = (13, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            13,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE = (
            13,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM = (
            13,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        _3_x_4_5_inch_M8_UnGd_Rocket = (13, Weapons._3_x_4_5_inch_M8_UnGd_Rocket)
        SUU_25_x_8_LUU_2___Target_Marker_Flares = (
            13,
            Weapons.SUU_25_x_8_LUU_2___Target_Marker_Flares,
        )
        HVAR__UnGd_Rkt = (13, Weapons.HVAR__UnGd_Rkt)

    class Pylon14:
        AN_M30A1___100lb_GP_Bomb_LD = (14, Weapons.AN_M30A1___100lb_GP_Bomb_LD)
        AN_M57___250lb_GP_Bomb_LD = (14, Weapons.AN_M57___250lb_GP_Bomb_LD)
        AN_M81___260lb_GP_Bomb_LD = (14, WeaponsVWV.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (14, WeaponsVWV.AN_M88___220lb_GP_Bomb_LD)
        AN_M64___500lb_GP_Bomb_LD = (14, Weapons.AN_M64___500lb_GP_Bomb_LD)
        Mk_82___500lb_GP_Bomb_LD = (14, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            14,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE = (
            14,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM = (
            14,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        _3_x_4_5_inch_M8_UnGd_Rocket = (14, Weapons._3_x_4_5_inch_M8_UnGd_Rocket)
        SUU_25_x_8_LUU_2___Target_Marker_Flares = (
            14,
            Weapons.SUU_25_x_8_LUU_2___Target_Marker_Flares,
        )
        HVAR__UnGd_Rkt = (14, Weapons.HVAR__UnGd_Rkt)

    class Pylon15:
        AN_M30A1___100lb_GP_Bomb_LD = (15, Weapons.AN_M30A1___100lb_GP_Bomb_LD)
        AN_M57___250lb_GP_Bomb_LD = (15, Weapons.AN_M57___250lb_GP_Bomb_LD)
        AN_M81___260lb_GP_Bomb_LD = (15, WeaponsVWV.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (15, WeaponsVWV.AN_M88___220lb_GP_Bomb_LD)
        AN_M64___500lb_GP_Bomb_LD = (15, Weapons.AN_M64___500lb_GP_Bomb_LD)
        Mk_82___500lb_GP_Bomb_LD = (15, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            15,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE = (
            15,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM = (
            15,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        _3_x_4_5_inch_M8_UnGd_Rocket = (15, Weapons._3_x_4_5_inch_M8_UnGd_Rocket)
        SUU_25_x_8_LUU_2___Target_Marker_Flares = (
            15,
            Weapons.SUU_25_x_8_LUU_2___Target_Marker_Flares,
        )
        HVAR__UnGd_Rkt = (15, Weapons.HVAR__UnGd_Rkt)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15}

    tasks = [
        task.GroundAttack,
        task.CAS,
        task.AFAC,
        task.RunwayAttack,
        task.AntishipStrike,
    ]
    task_default = task.CAS


@planemod
class vwv_ad4_skyraider(PlaneType):
    id = "vwv_ad4_skyraider"
    height = 4.77
    width = 15.24
    length = 11.84
    fuel_max = 1036
    max_speed = 522
    chaff = 0
    flare = 0
    charge_total = 0
    chaff_charge_size = 0
    flare_charge_size = 0

    livery_name = "VWV_AD4_SKYRAIDER"  # from type

    class Pylon1:
        AN_M30A1___100lb_GP_Bomb_LD = (1, Weapons.AN_M30A1___100lb_GP_Bomb_LD)
        AN_M57___250lb_GP_Bomb_LD = (1, Weapons.AN_M57___250lb_GP_Bomb_LD)
        AN_M81___260lb_GP_Bomb_LD = (1, WeaponsVWV.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (1, WeaponsVWV.AN_M88___220lb_GP_Bomb_LD)
        AN_M64___500lb_GP_Bomb_LD = (1, Weapons.AN_M64___500lb_GP_Bomb_LD)
        Mk_82___500lb_GP_Bomb_LD = (1, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            1,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE = (
            1,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM = (
            1,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        _3_x_4_5_inch_M8_UnGd_Rocket = (1, Weapons._3_x_4_5_inch_M8_UnGd_Rocket)
        SUU_25_x_8_LUU_2___Target_Marker_Flares = (
            1,
            Weapons.SUU_25_x_8_LUU_2___Target_Marker_Flares,
        )
        HVAR__UnGd_Rkt = (1, Weapons.HVAR__UnGd_Rkt)

    class Pylon2:
        AN_M30A1___100lb_GP_Bomb_LD = (2, Weapons.AN_M30A1___100lb_GP_Bomb_LD)
        AN_M57___250lb_GP_Bomb_LD = (2, Weapons.AN_M57___250lb_GP_Bomb_LD)
        AN_M81___260lb_GP_Bomb_LD = (2, WeaponsVWV.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (2, WeaponsVWV.AN_M88___220lb_GP_Bomb_LD)
        AN_M64___500lb_GP_Bomb_LD = (2, Weapons.AN_M64___500lb_GP_Bomb_LD)
        Mk_82___500lb_GP_Bomb_LD = (2, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            2,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE = (
            2,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM = (
            2,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        _3_x_4_5_inch_M8_UnGd_Rocket = (2, Weapons._3_x_4_5_inch_M8_UnGd_Rocket)
        SUU_25_x_8_LUU_2___Target_Marker_Flares = (
            2,
            Weapons.SUU_25_x_8_LUU_2___Target_Marker_Flares,
        )
        HVAR__UnGd_Rkt = (2, Weapons.HVAR__UnGd_Rkt)

    class Pylon3:
        AN_M30A1___100lb_GP_Bomb_LD = (3, Weapons.AN_M30A1___100lb_GP_Bomb_LD)
        AN_M57___250lb_GP_Bomb_LD = (3, Weapons.AN_M57___250lb_GP_Bomb_LD)
        AN_M81___260lb_GP_Bomb_LD = (3, WeaponsVWV.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (3, WeaponsVWV.AN_M88___220lb_GP_Bomb_LD)
        AN_M64___500lb_GP_Bomb_LD = (3, Weapons.AN_M64___500lb_GP_Bomb_LD)
        Mk_82___500lb_GP_Bomb_LD = (3, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            3,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE = (
            3,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM = (
            3,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        _3_x_4_5_inch_M8_UnGd_Rocket = (3, Weapons._3_x_4_5_inch_M8_UnGd_Rocket)
        SUU_25_x_8_LUU_2___Target_Marker_Flares = (
            3,
            Weapons.SUU_25_x_8_LUU_2___Target_Marker_Flares,
        )
        HVAR__UnGd_Rkt = (3, Weapons.HVAR__UnGd_Rkt)

    class Pylon4:
        AN_M30A1___100lb_GP_Bomb_LD = (4, Weapons.AN_M30A1___100lb_GP_Bomb_LD)
        AN_M57___250lb_GP_Bomb_LD = (4, Weapons.AN_M57___250lb_GP_Bomb_LD)
        AN_M81___260lb_GP_Bomb_LD = (4, WeaponsVWV.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (4, WeaponsVWV.AN_M88___220lb_GP_Bomb_LD)
        AN_M64___500lb_GP_Bomb_LD = (4, Weapons.AN_M64___500lb_GP_Bomb_LD)
        Mk_82___500lb_GP_Bomb_LD = (4, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            4,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE = (
            4,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM = (
            4,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        _3_x_4_5_inch_M8_UnGd_Rocket = (4, Weapons._3_x_4_5_inch_M8_UnGd_Rocket)
        SUU_25_x_8_LUU_2___Target_Marker_Flares = (
            4,
            Weapons.SUU_25_x_8_LUU_2___Target_Marker_Flares,
        )
        HVAR__UnGd_Rkt = (4, Weapons.HVAR__UnGd_Rkt)

    class Pylon5:
        AN_M30A1___100lb_GP_Bomb_LD = (5, Weapons.AN_M30A1___100lb_GP_Bomb_LD)
        AN_M57___250lb_GP_Bomb_LD = (5, Weapons.AN_M57___250lb_GP_Bomb_LD)
        AN_M81___260lb_GP_Bomb_LD = (5, WeaponsVWV.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (5, WeaponsVWV.AN_M88___220lb_GP_Bomb_LD)
        AN_M64___500lb_GP_Bomb_LD = (5, Weapons.AN_M64___500lb_GP_Bomb_LD)
        Mk_82___500lb_GP_Bomb_LD = (5, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            5,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE = (
            5,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM = (
            5,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        _3_x_4_5_inch_M8_UnGd_Rocket = (5, Weapons._3_x_4_5_inch_M8_UnGd_Rocket)
        SUU_25_x_8_LUU_2___Target_Marker_Flares = (
            5,
            Weapons.SUU_25_x_8_LUU_2___Target_Marker_Flares,
        )
        HVAR__UnGd_Rkt = (5, Weapons.HVAR__UnGd_Rkt)

    class Pylon6:
        AN_M30A1___100lb_GP_Bomb_LD = (6, Weapons.AN_M30A1___100lb_GP_Bomb_LD)
        AN_M57___250lb_GP_Bomb_LD = (6, Weapons.AN_M57___250lb_GP_Bomb_LD)
        AN_M81___260lb_GP_Bomb_LD = (6, WeaponsVWV.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (6, WeaponsVWV.AN_M88___220lb_GP_Bomb_LD)
        AN_M64___500lb_GP_Bomb_LD = (6, Weapons.AN_M64___500lb_GP_Bomb_LD)
        Mk_82___500lb_GP_Bomb_LD = (6, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            6,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE = (
            6,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM = (
            6,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        _3_x_4_5_inch_M8_UnGd_Rocket = (6, Weapons._3_x_4_5_inch_M8_UnGd_Rocket)
        SUU_25_x_8_LUU_2___Target_Marker_Flares = (
            6,
            Weapons.SUU_25_x_8_LUU_2___Target_Marker_Flares,
        )
        HVAR__UnGd_Rkt = (6, Weapons.HVAR__UnGd_Rkt)

    class Pylon7:
        AN_M30A1___100lb_GP_Bomb_LD = (7, Weapons.AN_M30A1___100lb_GP_Bomb_LD)
        AN_M57___250lb_GP_Bomb_LD = (7, Weapons.AN_M57___250lb_GP_Bomb_LD)
        AN_M64___500lb_GP_Bomb_LD = (7, Weapons.AN_M64___500lb_GP_Bomb_LD)
        AN_M65___1000lb_GP_Bomb_LD = (7, Weapons.AN_M65___1000lb_GP_Bomb_LD)
        AN_M81___260lb_GP_Bomb_LD = (7, WeaponsVWV.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (7, WeaponsVWV.AN_M88___220lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (7, Weapons.M117___750lb_GP_Bomb_LD)
        Mk_82___500lb_GP_Bomb_LD = (7, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_83___1000lb_GP_Bomb_LD = (7, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        Mk_84___2000lb_GP_Bomb_LD = (7, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        SUU_25_x_8_LUU_2___Target_Marker_Flares = (
            7,
            Weapons.SUU_25_x_8_LUU_2___Target_Marker_Flares,
        )
        AERO_1D_300_Gallons_Fuel_Tank_ = (7, Weapons.AERO_1D_300_Gallons_Fuel_Tank_)
        Fuel_Tank_150_gallons = (7, WeaponsVWV.Fuel_Tank_150_gallons)
        Fuel_Tank_150_gallons__EMPTY_ = (7, WeaponsVWV.Fuel_Tank_150_gallons__EMPTY_)
        _3_x_4_5_inch_M8_UnGd_Rocket = (7, Weapons._3_x_4_5_inch_M8_UnGd_Rocket)
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM = (
            7,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE_ = (
            7,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE_,
        )
        LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE = (
            7,
            Weapons.LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE,
        )
        Tiny_Tim = (7, WeaponsVWV.Tiny_Tim)
        LTF_5b_Aerial_Torpedo = (7, Weapons.LTF_5b_Aerial_Torpedo)
        DIS_mk46torp = (7, Weapons.DIS_mk46torp)
        toilet_bomb = (7, WeaponsVWV.toilet_bomb)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            7,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )

    class Pylon8:
        AN_M30A1___100lb_GP_Bomb_LD = (8, Weapons.AN_M30A1___100lb_GP_Bomb_LD)
        AN_M57___250lb_GP_Bomb_LD = (8, Weapons.AN_M57___250lb_GP_Bomb_LD)
        AN_M64___500lb_GP_Bomb_LD = (8, Weapons.AN_M64___500lb_GP_Bomb_LD)
        AN_M65___1000lb_GP_Bomb_LD = (8, Weapons.AN_M65___1000lb_GP_Bomb_LD)
        AN_M81___260lb_GP_Bomb_LD = (8, WeaponsVWV.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (8, WeaponsVWV.AN_M88___220lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (8, Weapons.M117___750lb_GP_Bomb_LD)
        Mk_82___500lb_GP_Bomb_LD = (8, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_83___1000lb_GP_Bomb_LD = (8, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        Mk_84___2000lb_GP_Bomb_LD = (8, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        SUU_25_x_8_LUU_2___Target_Marker_Flares = (
            8,
            Weapons.SUU_25_x_8_LUU_2___Target_Marker_Flares,
        )
        AERO_1D_300_Gallons_Fuel_Tank_ = (8, Weapons.AERO_1D_300_Gallons_Fuel_Tank_)
        LTF_5b_Aerial_Torpedo = (8, Weapons.LTF_5b_Aerial_Torpedo)
        DIS_mk46torp = (8, Weapons.DIS_mk46torp)

    class Pylon9:
        AN_M30A1___100lb_GP_Bomb_LD = (9, Weapons.AN_M30A1___100lb_GP_Bomb_LD)
        AN_M57___250lb_GP_Bomb_LD = (9, Weapons.AN_M57___250lb_GP_Bomb_LD)
        AN_M64___500lb_GP_Bomb_LD = (9, Weapons.AN_M64___500lb_GP_Bomb_LD)
        AN_M65___1000lb_GP_Bomb_LD = (9, Weapons.AN_M65___1000lb_GP_Bomb_LD)
        AN_M81___260lb_GP_Bomb_LD = (9, WeaponsVWV.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (9, WeaponsVWV.AN_M88___220lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (9, Weapons.M117___750lb_GP_Bomb_LD)
        Mk_82___500lb_GP_Bomb_LD = (9, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_83___1000lb_GP_Bomb_LD = (9, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        Mk_84___2000lb_GP_Bomb_LD = (9, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        SUU_25_x_8_LUU_2___Target_Marker_Flares = (
            9,
            Weapons.SUU_25_x_8_LUU_2___Target_Marker_Flares,
        )
        AERO_1D_300_Gallons_Fuel_Tank_ = (9, Weapons.AERO_1D_300_Gallons_Fuel_Tank_)
        Fuel_Tank_150_gallons = (9, WeaponsVWV.Fuel_Tank_150_gallons)
        Fuel_Tank_150_gallons__EMPTY_ = (9, WeaponsVWV.Fuel_Tank_150_gallons__EMPTY_)
        _3_x_4_5_inch_M8_UnGd_Rocket = (9, Weapons._3_x_4_5_inch_M8_UnGd_Rocket)
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM = (
            9,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE_ = (
            9,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE_,
        )
        LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE = (
            9,
            Weapons.LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE,
        )
        Tiny_Tim = (9, WeaponsVWV.Tiny_Tim)
        LTF_5b_Aerial_Torpedo = (9, Weapons.LTF_5b_Aerial_Torpedo)
        DIS_mk46torp = (9, Weapons.DIS_mk46torp)
        toilet_bomb = (9, WeaponsVWV.toilet_bomb)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            9,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )

    class Pylon10:
        AN_M30A1___100lb_GP_Bomb_LD = (10, Weapons.AN_M30A1___100lb_GP_Bomb_LD)
        AN_M57___250lb_GP_Bomb_LD = (10, Weapons.AN_M57___250lb_GP_Bomb_LD)
        AN_M81___260lb_GP_Bomb_LD = (10, WeaponsVWV.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (10, WeaponsVWV.AN_M88___220lb_GP_Bomb_LD)
        AN_M64___500lb_GP_Bomb_LD = (10, Weapons.AN_M64___500lb_GP_Bomb_LD)
        Mk_82___500lb_GP_Bomb_LD = (10, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            10,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE = (
            10,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM = (
            10,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        _3_x_4_5_inch_M8_UnGd_Rocket = (10, Weapons._3_x_4_5_inch_M8_UnGd_Rocket)
        SUU_25_x_8_LUU_2___Target_Marker_Flares = (
            10,
            Weapons.SUU_25_x_8_LUU_2___Target_Marker_Flares,
        )
        HVAR__UnGd_Rkt = (10, Weapons.HVAR__UnGd_Rkt)

    class Pylon11:
        AN_M30A1___100lb_GP_Bomb_LD = (11, Weapons.AN_M30A1___100lb_GP_Bomb_LD)
        AN_M57___250lb_GP_Bomb_LD = (11, Weapons.AN_M57___250lb_GP_Bomb_LD)
        AN_M81___260lb_GP_Bomb_LD = (11, WeaponsVWV.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (11, WeaponsVWV.AN_M88___220lb_GP_Bomb_LD)
        AN_M64___500lb_GP_Bomb_LD = (11, Weapons.AN_M64___500lb_GP_Bomb_LD)
        Mk_82___500lb_GP_Bomb_LD = (11, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            11,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE = (
            11,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM = (
            11,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        _3_x_4_5_inch_M8_UnGd_Rocket = (11, Weapons._3_x_4_5_inch_M8_UnGd_Rocket)
        SUU_25_x_8_LUU_2___Target_Marker_Flares = (
            11,
            Weapons.SUU_25_x_8_LUU_2___Target_Marker_Flares,
        )
        HVAR__UnGd_Rkt = (11, Weapons.HVAR__UnGd_Rkt)

    class Pylon12:
        AN_M30A1___100lb_GP_Bomb_LD = (12, Weapons.AN_M30A1___100lb_GP_Bomb_LD)
        AN_M57___250lb_GP_Bomb_LD = (12, Weapons.AN_M57___250lb_GP_Bomb_LD)
        AN_M81___260lb_GP_Bomb_LD = (12, WeaponsVWV.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (12, WeaponsVWV.AN_M88___220lb_GP_Bomb_LD)
        AN_M64___500lb_GP_Bomb_LD = (12, Weapons.AN_M64___500lb_GP_Bomb_LD)
        Mk_82___500lb_GP_Bomb_LD = (12, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            12,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE = (
            12,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM = (
            12,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        _3_x_4_5_inch_M8_UnGd_Rocket = (12, Weapons._3_x_4_5_inch_M8_UnGd_Rocket)
        SUU_25_x_8_LUU_2___Target_Marker_Flares = (
            12,
            Weapons.SUU_25_x_8_LUU_2___Target_Marker_Flares,
        )
        HVAR__UnGd_Rkt = (12, Weapons.HVAR__UnGd_Rkt)

    class Pylon13:
        AN_M30A1___100lb_GP_Bomb_LD = (13, Weapons.AN_M30A1___100lb_GP_Bomb_LD)
        AN_M57___250lb_GP_Bomb_LD = (13, Weapons.AN_M57___250lb_GP_Bomb_LD)
        AN_M81___260lb_GP_Bomb_LD = (13, WeaponsVWV.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (13, WeaponsVWV.AN_M88___220lb_GP_Bomb_LD)
        AN_M64___500lb_GP_Bomb_LD = (13, Weapons.AN_M64___500lb_GP_Bomb_LD)
        Mk_82___500lb_GP_Bomb_LD = (13, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            13,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE = (
            13,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM = (
            13,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        _3_x_4_5_inch_M8_UnGd_Rocket = (13, Weapons._3_x_4_5_inch_M8_UnGd_Rocket)
        SUU_25_x_8_LUU_2___Target_Marker_Flares = (
            13,
            Weapons.SUU_25_x_8_LUU_2___Target_Marker_Flares,
        )
        HVAR__UnGd_Rkt = (13, Weapons.HVAR__UnGd_Rkt)

    class Pylon14:
        AN_M30A1___100lb_GP_Bomb_LD = (14, Weapons.AN_M30A1___100lb_GP_Bomb_LD)
        AN_M57___250lb_GP_Bomb_LD = (14, Weapons.AN_M57___250lb_GP_Bomb_LD)
        AN_M81___260lb_GP_Bomb_LD = (14, WeaponsVWV.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (14, WeaponsVWV.AN_M88___220lb_GP_Bomb_LD)
        AN_M64___500lb_GP_Bomb_LD = (14, Weapons.AN_M64___500lb_GP_Bomb_LD)
        Mk_82___500lb_GP_Bomb_LD = (14, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            14,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE = (
            14,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM = (
            14,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        _3_x_4_5_inch_M8_UnGd_Rocket = (14, Weapons._3_x_4_5_inch_M8_UnGd_Rocket)
        SUU_25_x_8_LUU_2___Target_Marker_Flares = (
            14,
            Weapons.SUU_25_x_8_LUU_2___Target_Marker_Flares,
        )
        HVAR__UnGd_Rkt = (14, Weapons.HVAR__UnGd_Rkt)

    class Pylon15:
        AN_M30A1___100lb_GP_Bomb_LD = (15, Weapons.AN_M30A1___100lb_GP_Bomb_LD)
        AN_M57___250lb_GP_Bomb_LD = (15, Weapons.AN_M57___250lb_GP_Bomb_LD)
        AN_M81___260lb_GP_Bomb_LD = (15, WeaponsVWV.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (15, WeaponsVWV.AN_M88___220lb_GP_Bomb_LD)
        AN_M64___500lb_GP_Bomb_LD = (15, Weapons.AN_M64___500lb_GP_Bomb_LD)
        Mk_82___500lb_GP_Bomb_LD = (15, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            15,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE = (
            15,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM = (
            15,
            Weapons.LAU_61___19_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        _3_x_4_5_inch_M8_UnGd_Rocket = (15, Weapons._3_x_4_5_inch_M8_UnGd_Rocket)
        SUU_25_x_8_LUU_2___Target_Marker_Flares = (
            15,
            Weapons.SUU_25_x_8_LUU_2___Target_Marker_Flares,
        )
        HVAR__UnGd_Rkt = (15, Weapons.HVAR__UnGd_Rkt)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15}

    tasks = [
        task.GroundAttack,
        task.CAS,
        task.AFAC,
        task.RunwayAttack,
        task.AntishipStrike,
    ]
    task_default = task.CAS


@planemod
class vwv_ra_5(PlaneType):
    id = "vwv_ra-5"
    height = 5.91
    width = 16.16
    length = 23.32
    fuel_max = 10000
    max_speed = 2469.6

    livery_name = "VWV_RA-5"  # from type

    pylons: Set[int] = set()

    category = "Reconnaissance"

    tasks = [task.Reconnaissance, task.AFAC, task.CAS]
    task_default = task.Reconnaissance


@planemod
class vwv_crusader(PlaneType):
    id = "vwv_crusader"
    flyable = True
    height = 4.8
    width = 10.72
    length = 16.61
    fuel_max = 4096
    max_speed = 1976.4
    chaff = 120
    flare = 120
    charge_total = 240
    chaff_charge_size = 1
    flare_charge_size = 1
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    livery_name = "VWV_CRUSADER"  # from type

    class Pylon1:
        LAU3_HE151 = (1, Weapons.LAU3_HE151)
        LAU3_HE5 = (1, Weapons.LAU3_HE5)
        BRU_33_2_x_LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE = (
            1,
            Weapons.BRU_33_2_x_LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE,
        )
        BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD = (
            1,
            Weapons.BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD,
        )
        BRU_33_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            1,
            Weapons.BRU_33_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE = (
            1,
            Weapons.LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE,
        )
        _2_Mk_82_Snakeye____ = (1, Weapons._2_Mk_82_Snakeye____)
        _2_Mk_82____ = (1, Weapons._2_Mk_82____)
        BRU_41A_with_4_x_Mk_82___500lb_GP_Bomb_HD_Left = (
            1,
            WeaponsVWV.BRU_41A_with_4_x_Mk_82___500lb_GP_Bomb_HD_Left,
        )
        BRU_41A_with_4_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_Left = (
            1,
            WeaponsVWV.BRU_41A_with_4_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_Left,
        )
        M117___750lb_GP_Bomb_LD = (1, Weapons.M117___750lb_GP_Bomb_LD)
        Mk_84___2000lb_GP_Bomb_LD = (1, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        Fuel_Tank_300_gallons_ = (1, WeaponsVWV.Fuel_Tank_300_gallons_)
        Fuel_Tank_300_gallons__EMPTY__ = (1, WeaponsVWV.Fuel_Tank_300_gallons__EMPTY__)
        Fuel_Tank_150_gallons = (1, WeaponsVWV.Fuel_Tank_150_gallons)
        Fuel_Tank_150_gallons__EMPTY_ = (1, WeaponsVWV.Fuel_Tank_150_gallons__EMPTY_)

    # ERRR <CLEAN>

    class Pylon2:
        AIM_9B_Sidewinder_IR_AAM = (2, Weapons.AIM_9B_Sidewinder_IR_AAM)
        AIM_9J_Sidewinder_IR_AAM = (2, Weapons.AIM_9J_Sidewinder_IR_AAM)
        R550_Magic_1_IR_AAM = (2, Weapons.R550_Magic_1_IR_AAM)

    class Pylon3:
        AIM_9B_Sidewinder_IR_AAM = (3, Weapons.AIM_9B_Sidewinder_IR_AAM)
        AIM_9C_Sidewinder_SARH_AAM = (3, WeaponsVWV.AIM_9C_Sidewinder_SARH_AAM)
        AIM_9D_Sidewinder_IR_AAM = (3, WeaponsVWV.AIM_9D_Sidewinder_IR_AAM)
        AIM_9J_Sidewinder_IR_AAM = (3, Weapons.AIM_9J_Sidewinder_IR_AAM)
        LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE = (
            3,
            Weapons.LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE,
        )

    class Pylon4:
        AIM_9B_Sidewinder_IR_AAM = (4, Weapons.AIM_9B_Sidewinder_IR_AAM)
        AIM_9C_Sidewinder_SARH_AAM = (4, WeaponsVWV.AIM_9C_Sidewinder_SARH_AAM)
        AIM_9D_Sidewinder_IR_AAM = (4, WeaponsVWV.AIM_9D_Sidewinder_IR_AAM)
        AIM_9J_Sidewinder_IR_AAM = (4, Weapons.AIM_9J_Sidewinder_IR_AAM)
        LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE = (
            4,
            Weapons.LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE,
        )

    class Pylon5:
        AIM_9B_Sidewinder_IR_AAM = (5, Weapons.AIM_9B_Sidewinder_IR_AAM)
        AIM_9C_Sidewinder_SARH_AAM = (5, WeaponsVWV.AIM_9C_Sidewinder_SARH_AAM)
        AIM_9D_Sidewinder_IR_AAM = (5, WeaponsVWV.AIM_9D_Sidewinder_IR_AAM)
        AIM_9J_Sidewinder_IR_AAM = (5, Weapons.AIM_9J_Sidewinder_IR_AAM)
        LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE = (
            5,
            Weapons.LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE,
        )

    class Pylon6:
        LAU3_HE151 = (6, Weapons.LAU3_HE151)
        LAU3_HE5 = (6, Weapons.LAU3_HE5)
        BRU_33_2_x_LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE = (
            6,
            Weapons.BRU_33_2_x_LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE,
        )
        BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD = (
            6,
            Weapons.BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD,
        )
        BRU_33_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            6,
            Weapons.BRU_33_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE = (
            6,
            Weapons.LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE,
        )
        _2_Mk_82_Snakeye_____ = (6, Weapons._2_Mk_82_____)
        _2_Mk_82_____ = (6, Weapons._2_Mk_82_____)
        BRU_41A_with_4_x_Mk_82___500lb_GP_Bomb_HD_Right = (
            6,
            WeaponsVWV.BRU_41A_with_4_x_Mk_82___500lb_GP_Bomb_HD_Right,
        )
        BRU_41A_with_4_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_Right = (
            6,
            WeaponsVWV.BRU_41A_with_4_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_Right,
        )
        M117___750lb_GP_Bomb_LD = (6, Weapons.M117___750lb_GP_Bomb_LD)
        Mk_84___2000lb_GP_Bomb_LD = (6, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        Fuel_Tank_300_gallons_ = (6, WeaponsVWV.Fuel_Tank_300_gallons_)
        Fuel_Tank_300_gallons__EMPTY__ = (6, WeaponsVWV.Fuel_Tank_300_gallons__EMPTY__)
        Fuel_Tank_150_gallons = (6, WeaponsVWV.Fuel_Tank_150_gallons)
        Fuel_Tank_150_gallons__EMPTY_ = (6, WeaponsVWV.Fuel_Tank_150_gallons__EMPTY_)

    # ERRR <CLEAN>

    pylons: Set[int] = {1, 2, 3, 4, 5, 6}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.Reconnaissance,
        task.GroundAttack,
        task.CAS,
        task.AntishipStrike,
    ]
    task_default = task.CAP


@planemod
class vwv_mig17f(PlaneType):
    id = "vwv_mig17f"
    # flyable = True    # not available in current mod version
    height = 3.8
    width = 9.628
    length = 11.264
    fuel_max = 1170
    max_speed = 1144.8
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    livery_name = "VWV_MIG17F"  # from type

    class Pylon1:
        FAB_50 = (1, Weapons.FAB_50)
        OFAB_250_270___250_kg_GP_Bomb_LD = (1, Weapons.OFAB_250_270___250_kg_GP_Bomb_LD)
        B_8V20A_CM = (1, Weapons.B_8V20A_CM)
        B_8V20A_OM = (1, Weapons.B_8V20A_OM)
        B_8M1___20_S_8OFP2 = (1, Weapons.B_8M1___20_S_8OFP2)
        # ERRR B-8V20A - 20 S-8OFP2
        FAB_100M = (1, Weapons.FAB_100M)
        UPK_23_250___2_x_23mm__GSh_23L_Autocannon_Pod = (
            1,
            Weapons.UPK_23_250___2_x_23mm__GSh_23L_Autocannon_Pod,
        )

    class Pylon2:
        FAB_50 = (2, Weapons.FAB_50)
        OFAB_250_270___250_kg_GP_Bomb_LD = (2, Weapons.OFAB_250_270___250_kg_GP_Bomb_LD)
        B_8V20A_CM = (2, Weapons.B_8V20A_CM)
        B_8V20A_OM = (2, Weapons.B_8V20A_OM)
        B_8M1___20_S_8OFP2 = (2, Weapons.B_8M1___20_S_8OFP2)
        # ERRR B-8V20A - 20 S-8OFP2
        FAB_100M = (2, Weapons.FAB_100M)
        UPK_23_250___2_x_23mm__GSh_23L_Autocannon_Pod = (
            2,
            Weapons.UPK_23_250___2_x_23mm__GSh_23L_Autocannon_Pod,
        )

    class Pylon3:
        PTB400_MIG15 = (3, Weapons.PTB400_MIG15)

    class Pylon4:
        PTB400_MIG15 = (4, Weapons.PTB400_MIG15)

    pylons: Set[int] = {1, 2, 3, 4}

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
    task_default = task.CAP


@planemod
class vwv_mig21mf(PlaneType):
    id = "vwv_mig21mf"
    height = 4.1
    width = 7.15
    length = 14.5
    fuel_max = 2650
    max_speed = 2232
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    livery_name = "VWV_MIG21MF"  # from type

    class Pylon1:
        FAB_50 = (1, Weapons.FAB_50)
        OFAB_250_270___250_kg_GP_Bomb_LD = (1, Weapons.OFAB_250_270___250_kg_GP_Bomb_LD)
        B_8V20A_CM = (1, Weapons.B_8V20A_CM)
        B_8V20A_OM = (1, Weapons.B_8V20A_OM)
        B_8M1___20_S_8OFP2 = (1, Weapons.B_8M1___20_S_8OFP2)
        # ERRR B-8V20A - 20 S-8OFP2
        FAB_100M = (1, Weapons.FAB_100M)
        UPK_23_250___2_x_23mm__GSh_23L_Autocannon_Pod = (
            1,
            Weapons.UPK_23_250___2_x_23mm__GSh_23L_Autocannon_Pod,
        )
        Fuel_Tank_490_L_Central__21_ = (1, Weapons.Fuel_Tank_490_L_Central__21_)
        APU_13MT_with_R_13M__AA_2_Atoll_D____IR_AAM = (
            1,
            Weapons.APU_13MT_with_R_13M__AA_2_Atoll_D____IR_AAM,
        )
        APU_13U_2_with_R_3R__AA_2_Atoll_C____Semi_Active_AAM = (
            1,
            Weapons.APU_13U_2_with_R_3R__AA_2_Atoll_C____Semi_Active_AAM,
        )
        APU_13U_2_with_R_3S__AA_2_Atoll_B____IR_AAM = (
            1,
            Weapons.APU_13U_2_with_R_3S__AA_2_Atoll_B____IR_AAM,
        )
        RS2US___AAM__beam_rider = (1, Weapons.RS2US___AAM__beam_rider)

    class Pylon2:
        FAB_50 = (2, Weapons.FAB_50)
        OFAB_250_270___250_kg_GP_Bomb_LD = (2, Weapons.OFAB_250_270___250_kg_GP_Bomb_LD)
        B_8V20A_CM = (2, Weapons.B_8V20A_CM)
        B_8V20A_OM = (2, Weapons.B_8V20A_OM)
        B_8M1___20_S_8OFP2 = (2, Weapons.B_8M1___20_S_8OFP2)
        # ERRR B-8V20A - 20 S-8OFP2
        FAB_100M = (2, Weapons.FAB_100M)
        UPK_23_250___2_x_23mm__GSh_23L_Autocannon_Pod = (
            2,
            Weapons.UPK_23_250___2_x_23mm__GSh_23L_Autocannon_Pod,
        )
        APU_13MT_with_R_13M__AA_2_Atoll_D____IR_AAM = (
            2,
            Weapons.APU_13MT_with_R_13M__AA_2_Atoll_D____IR_AAM,
        )
        APU_13U_2_with_R_3R__AA_2_Atoll_C____Semi_Active_AAM = (
            2,
            Weapons.APU_13U_2_with_R_3R__AA_2_Atoll_C____Semi_Active_AAM,
        )
        APU_13U_2_with_R_3S__AA_2_Atoll_B____IR_AAM = (
            2,
            Weapons.APU_13U_2_with_R_3S__AA_2_Atoll_B____IR_AAM,
        )
        RS2US___AAM__beam_rider = (2, Weapons.RS2US___AAM__beam_rider)

    class Pylon3:
        OFAB_250_270___250_kg_GP_Bomb_LD = (3, Weapons.OFAB_250_270___250_kg_GP_Bomb_LD)
        UPK_23_250___2_x_23mm__GSh_23L_Autocannon_Pod = (
            3,
            Weapons.UPK_23_250___2_x_23mm__GSh_23L_Autocannon_Pod,
        )
        Fuel_Tank_490_L__21_ = (3, Weapons.Fuel_Tank_490_L__21_)
        Fuel_Tank_490_L_Central__21_ = (3, Weapons.Fuel_Tank_490_L_Central__21_)
        Fuel_Tank_800_L__21_ = (3, Weapons.Fuel_Tank_800_L__21_)

    class Pylon4:
        FAB_50 = (4, Weapons.FAB_50)
        OFAB_250_270___250_kg_GP_Bomb_LD = (4, Weapons.OFAB_250_270___250_kg_GP_Bomb_LD)
        B_8V20A_CM = (4, Weapons.B_8V20A_CM)
        B_8V20A_OM = (4, Weapons.B_8V20A_OM)
        B_8M1___20_S_8OFP2 = (4, Weapons.B_8M1___20_S_8OFP2)
        # ERRR B-8V20A - 20 S-8OFP2
        FAB_100M = (4, Weapons.FAB_100M)
        UPK_23_250___2_x_23mm__GSh_23L_Autocannon_Pod = (
            4,
            Weapons.UPK_23_250___2_x_23mm__GSh_23L_Autocannon_Pod,
        )
        APU_13MT_with_R_13M__AA_2_Atoll_D____IR_AAM = (
            4,
            Weapons.APU_13MT_with_R_13M__AA_2_Atoll_D____IR_AAM,
        )
        APU_13U_2_with_R_3R__AA_2_Atoll_C____Semi_Active_AAM = (
            4,
            Weapons.APU_13U_2_with_R_3R__AA_2_Atoll_C____Semi_Active_AAM,
        )
        APU_13U_2_with_R_3S__AA_2_Atoll_B____IR_AAM = (
            4,
            Weapons.APU_13U_2_with_R_3S__AA_2_Atoll_B____IR_AAM,
        )
        RS2US___AAM__beam_rider = (4, Weapons.RS2US___AAM__beam_rider)

    class Pylon5:
        FAB_50 = (5, Weapons.FAB_50)
        OFAB_250_270___250_kg_GP_Bomb_LD = (5, Weapons.OFAB_250_270___250_kg_GP_Bomb_LD)
        B_8V20A_CM = (5, Weapons.B_8V20A_CM)
        B_8V20A_OM = (5, Weapons.B_8V20A_OM)
        B_8M1___20_S_8OFP2 = (5, Weapons.B_8M1___20_S_8OFP2)
        # ERRR B-8V20A - 20 S-8OFP2
        FAB_100M = (5, Weapons.FAB_100M)
        UPK_23_250___2_x_23mm__GSh_23L_Autocannon_Pod = (
            5,
            Weapons.UPK_23_250___2_x_23mm__GSh_23L_Autocannon_Pod,
        )
        Fuel_Tank_490_L_Central__21_ = (5, Weapons.Fuel_Tank_490_L_Central__21_)
        APU_13MT_with_R_13M__AA_2_Atoll_D____IR_AAM = (
            5,
            Weapons.APU_13MT_with_R_13M__AA_2_Atoll_D____IR_AAM,
        )
        APU_13U_2_with_R_3R__AA_2_Atoll_C____Semi_Active_AAM = (
            5,
            Weapons.APU_13U_2_with_R_3R__AA_2_Atoll_C____Semi_Active_AAM,
        )
        APU_13U_2_with_R_3S__AA_2_Atoll_B____IR_AAM = (
            5,
            Weapons.APU_13U_2_with_R_3S__AA_2_Atoll_B____IR_AAM,
        )
        RS2US___AAM__beam_rider = (5, Weapons.RS2US___AAM__beam_rider)

    class Pylon6:
        SPRD_99 = (6, Weapons.SPRD_99)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.GroundAttack,
        task.CAS,
        task.AntishipStrike,
    ]
    task_default = task.CAP


@planemod
class vwv_o_1(PlaneType):
    id = "vwv_o-1"
    height = 2.22
    width = 10.97
    length = 7.85
    fuel_max = 115
    max_speed = 158.4
    radio_frequency = 225

    livery_name = "VWV_O-1"  # from type

    class Pylon1:
        _3_x_4_5_inch_M8_UnGd_Rocket = (1, Weapons._3_x_4_5_inch_M8_UnGd_Rocket)
        SUU_25_x_8_LUU_2___Target_Marker_Flares = (
            1,
            Weapons.SUU_25_x_8_LUU_2___Target_Marker_Flares,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_M156_SM = (
            1,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_M156_SM,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE = (
            1,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT = (
            1,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT,
        )
        Telson_8___8_x_UnGd_Rkts__68_mm_SNEB_Type_254_H1_SM_Red = (
            1,
            Weapons.Telson_8___8_x_UnGd_Rkts__68_mm_SNEB_Type_254_H1_SM_Red,
        )
        Telson_8___8_x_UnGd_Rkts__68_mm_SNEB_Type_254_H1_SM_Yellow = (
            1,
            Weapons.Telson_8___8_x_UnGd_Rkts__68_mm_SNEB_Type_254_H1_SM_Yellow,
        )
        Telson_8___8_x_UnGd_Rkts__68_mm_SNEB_Type_254_H1_SM_Green = (
            1,
            Weapons.Telson_8___8_x_UnGd_Rkts__68_mm_SNEB_Type_254_H1_SM_Green,
        )
        Telson_8___8_x_UnGd_Rkts__68_mm_SNEB_Type_256_H1_HE_Frag = (
            1,
            Weapons.Telson_8___8_x_UnGd_Rkts__68_mm_SNEB_Type_256_H1_HE_Frag,
        )

    class Pylon2:
        _3_x_4_5_inch_M8_UnGd_Rocket = (2, Weapons._3_x_4_5_inch_M8_UnGd_Rocket)
        SUU_25_x_8_LUU_2___Target_Marker_Flares = (
            2,
            Weapons.SUU_25_x_8_LUU_2___Target_Marker_Flares,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_M156_SM = (
            2,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_M156_SM,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE = (
            2,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT = (
            2,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT,
        )
        Telson_8___8_x_UnGd_Rkts__68_mm_SNEB_Type_254_H1_SM_Red = (
            2,
            Weapons.Telson_8___8_x_UnGd_Rkts__68_mm_SNEB_Type_254_H1_SM_Red,
        )
        Telson_8___8_x_UnGd_Rkts__68_mm_SNEB_Type_254_H1_SM_Yellow = (
            2,
            Weapons.Telson_8___8_x_UnGd_Rkts__68_mm_SNEB_Type_254_H1_SM_Yellow,
        )
        Telson_8___8_x_UnGd_Rkts__68_mm_SNEB_Type_254_H1_SM_Green = (
            2,
            Weapons.Telson_8___8_x_UnGd_Rkts__68_mm_SNEB_Type_254_H1_SM_Green,
        )
        Telson_8___8_x_UnGd_Rkts__68_mm_SNEB_Type_256_H1_HE_Frag = (
            2,
            Weapons.Telson_8___8_x_UnGd_Rkts__68_mm_SNEB_Type_256_H1_HE_Frag,
        )

    class Pylon3:
        _3_x_4_5_inch_M8_UnGd_Rocket = (3, Weapons._3_x_4_5_inch_M8_UnGd_Rocket)
        SUU_25_x_8_LUU_2___Target_Marker_Flares = (
            3,
            Weapons.SUU_25_x_8_LUU_2___Target_Marker_Flares,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_M156_SM = (
            3,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_M156_SM,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE = (
            3,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT = (
            3,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT,
        )
        Telson_8___8_x_UnGd_Rkts__68_mm_SNEB_Type_254_H1_SM_Red = (
            3,
            Weapons.Telson_8___8_x_UnGd_Rkts__68_mm_SNEB_Type_254_H1_SM_Red,
        )
        Telson_8___8_x_UnGd_Rkts__68_mm_SNEB_Type_254_H1_SM_Yellow = (
            3,
            Weapons.Telson_8___8_x_UnGd_Rkts__68_mm_SNEB_Type_254_H1_SM_Yellow,
        )
        Telson_8___8_x_UnGd_Rkts__68_mm_SNEB_Type_254_H1_SM_Green = (
            3,
            Weapons.Telson_8___8_x_UnGd_Rkts__68_mm_SNEB_Type_254_H1_SM_Green,
        )
        Telson_8___8_x_UnGd_Rkts__68_mm_SNEB_Type_256_H1_HE_Frag = (
            3,
            Weapons.Telson_8___8_x_UnGd_Rkts__68_mm_SNEB_Type_256_H1_HE_Frag,
        )

    class Pylon4:
        _3_x_4_5_inch_M8_UnGd_Rocket = (4, Weapons._3_x_4_5_inch_M8_UnGd_Rocket)
        SUU_25_x_8_LUU_2___Target_Marker_Flares = (
            4,
            Weapons.SUU_25_x_8_LUU_2___Target_Marker_Flares,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_M156_SM = (
            4,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_M156_SM,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE = (
            4,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE,
        )
        LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT = (
            4,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT,
        )
        Telson_8___8_x_UnGd_Rkts__68_mm_SNEB_Type_254_H1_SM_Red = (
            4,
            Weapons.Telson_8___8_x_UnGd_Rkts__68_mm_SNEB_Type_254_H1_SM_Red,
        )
        Telson_8___8_x_UnGd_Rkts__68_mm_SNEB_Type_254_H1_SM_Yellow = (
            4,
            Weapons.Telson_8___8_x_UnGd_Rkts__68_mm_SNEB_Type_254_H1_SM_Yellow,
        )
        Telson_8___8_x_UnGd_Rkts__68_mm_SNEB_Type_254_H1_SM_Green = (
            4,
            Weapons.Telson_8___8_x_UnGd_Rkts__68_mm_SNEB_Type_254_H1_SM_Green,
        )
        Telson_8___8_x_UnGd_Rkts__68_mm_SNEB_Type_256_H1_HE_Frag = (
            4,
            Weapons.Telson_8___8_x_UnGd_Rkts__68_mm_SNEB_Type_256_H1_HE_Frag,
        )

    pylons: Set[int] = {1, 2, 3, 4}

    tasks = [task.AFAC, task.CAS, task.Reconnaissance]
    task_default = task.AFAC


## SHIPS


@shipmod
class ATCH(unittype.ShipType):
    id = "ATCH"
    name = "[VWV] ATC(H) Tango"
    plane_num = 0
    helicopter_num = 1
    parking = 1
    detection_range = 5000
    threat_range = 3000
    air_weapon_dist = 3000


@shipmod
class ATCH_Heavy(unittype.ShipType):
    id = "ATCH_Heavy"
    name = "[VWV] ATC(H) Tango Heavy"
    plane_num = 0
    helicopter_num = 1
    parking = 1
    detection_range = 5000
    threat_range = 3000
    air_weapon_dist = 3000


@shipmod
class CCB(unittype.ShipType):
    id = "CCB"
    name = "[VWV] CCB Charlie"
    detection_range = 5000
    threat_range = 3000
    air_weapon_dist = 3000


@shipmod
class USS_New_Jersey(unittype.ShipType):
    id = "USS New Jersey"
    name = "[VWV] BB-62 USS New Jersey 1968"
    plane_num = 0
    helicopter_num = 1
    parking = 1
    detection_range = 130000
    threat_range = 14630
    air_weapon_dist = 14630


@shipmod
class USS_Oklahoma_City(unittype.ShipType):
    id = "USS Oklahoma City"
    name = "[VWV] CLG-5 USS Oklahoma City"
    plane_num = 0
    helicopter_num = 1
    parking = 1
    detection_range = 130000
    threat_range = 14630
    air_weapon_dist = 14630


@shipmod
class USS_Bon_Homme_Richard(unittype.ShipType):
    id = "USS Bon Homme Richard"
    name = "[VWV] CVA-31 Bon Homme Richard"
    plane_num = 8
    helicopter_num = 8
    parking = 2
    detection_range = 28000
    threat_range = 15000
    air_weapon_dist = 15000


@shipmod
class Essex_SCB125(unittype.ShipType):
    id = "essex_scb125"
    name = "[VWV] CV Essex Class SCB-125"
    plane_num = 40
    helicopter_num = 8
    parking = 2
    detection_range = 28000
    threat_range = 15000
    air_weapon_dist = 15000


@shipmod
class USS_Enterprise_1966(unittype.ShipType):
    id = "USS Enterprise 1966"
    name = "[VWV] CVAN-65 USS Enterprise '66"
    plane_num = 36
    helicopter_num = 12
    parking = 4
    detection_range = 50000
    threat_range = 25000
    air_weapon_dist = 25000


@shipmod
class USS_Enterprise_1969(unittype.ShipType):
    id = "USS Enterprise 1969"
    name = "[VWV] CVAN-65 USS Enterprise '69"
    plane_num = 36
    helicopter_num = 12
    parking = 4
    detection_range = 50000
    threat_range = 25000
    air_weapon_dist = 25000


@shipmod
class USS_Fletcher(unittype.ShipType):
    id = "USS Fletcher"
    name = "[VWV] DD USS Fletcher FRAM II"
    plane_num = 1
    helicopter_num = 1
    parking = 1
    detection_range = 45000
    threat_range = 18650
    air_weapon_dist = 18650


@shipmod
class USS_Mullany(unittype.ShipType):
    id = "USS Mullany"
    name = "[VWV] DD-528 USS Mullany"
    detection_range = 45000
    threat_range = 18650
    air_weapon_dist = 18650


@shipmod
class USS_The_Sullivans(unittype.ShipType):
    id = "USS The Sullivans"
    name = "[VWV] DD-537 USS The Sullivans"
    detection_range = 45000
    threat_range = 18650
    air_weapon_dist = 18650


@shipmod
class USS_Sumner(unittype.ShipType):
    id = "USS Sumner"
    name = "[VWV] DD-692 USS Allen M. Sumner"
    plane_num = 0
    helicopter_num = 1
    parking = 1
    detection_range = 45000
    threat_range = 18650
    air_weapon_dist = 18650


@shipmod
class USS_Laffey(unittype.ShipType):
    id = "USS Laffey"
    name = "[VWV] DD-724 USS Laffey"
    plane_num = 0
    helicopter_num = 1
    parking = 1
    detection_range = 45000
    threat_range = 18650
    air_weapon_dist = 18650


@shipmod
class USS_Maddox(unittype.ShipType):
    id = "USS Maddox"
    name = "[VWV] DD-731 USS Maddox"
    detection_range = 45000
    threat_range = 18650
    air_weapon_dist = 18650


@shipmod
class USS_Forrest_Sherman(unittype.ShipType):
    id = "USS Forrest Sherman"
    name = "[VWV] DD-931 USS Forrest Sherman"
    detection_range = 45000
    threat_range = 18650
    air_weapon_dist = 18650


@shipmod
class USS_Bigelow(unittype.ShipType):
    id = "USS Bigelow"
    name = "[VWV] DD-942 USS Bigelow"
    detection_range = 45000
    threat_range = 18650
    air_weapon_dist = 18650


@shipmod
class USS_Knox(unittype.ShipType):
    id = "USS Knox"
    name = "[VWV] DE-1052 USS Knox"
    plane_num = 0
    helicopter_num = 1
    parking = 1
    detection_range = 45000
    threat_range = 18650
    air_weapon_dist = 18650


@shipmod
class USS_Gray(unittype.ShipType):
    id = "USS Gray"
    name = "[VWV] DE-1054 USS Gray"
    plane_num = 0
    helicopter_num = 1
    parking = 1
    detection_range = 45000
    threat_range = 18650
    air_weapon_dist = 18650


@shipmod
class USS_Kirk(unittype.ShipType):
    id = "USS Kirk"
    name = "[VWV] DE-1087 USS Kirk"
    plane_num = 0
    helicopter_num = 1
    parking = 1
    detection_range = 45000
    threat_range = 18650
    air_weapon_dist = 18650


@shipmod
class IX514_Unarmed(unittype.ShipType):
    id = "[VWV] IX514 (unarmed)"
    name = "[VWV] IX514 (unarmed)"
    plane_num = 0
    helicopter_num = 1
    parking = 1
    detection_range = 5000
    threat_range = 3000
    air_weapon_dist = 3000


@shipmod
class IX514(unittype.ShipType):
    id = "[VWV]IX514"
    name = "[VWV] IX514"
    plane_num = 0
    helicopter_num = 1
    parking = 1
    detection_range = 5000
    threat_range = 3000
    air_weapon_dist = 3000


@shipmod
class PBR_MKII(unittype.ShipType):
    id = "PBR_MKII"
    name = "[VWV] Patrol Boat, River MkII"
    detection_range = 40000
    threat_range = 5200
    air_weapon_dist = 5200


@shipmod
class P4(unittype.ShipType):
    id = "P4"
    name = "[VWV] P 4 Torpedo Boat"
    detection_range = 3000
    threat_range = 1000
    air_weapon_dist = 1000


@shipmod
class vap_us_seafloat(unittype.ShipType):
    id = "vap_us_seafloat"
    name = "VAP US Sea Float Barge"
    helicopter_num = 4
    parking = 4
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


## HELICOPTERS


@helicoptermod
class vwv_ch46d(HelicopterType):
    id = "vwv_ch46d"
    height = 5.08
    width = 15.24
    length = 13.92
    fuel_max = 1080
    max_speed = 267
    radio_frequency = 225

    property_defaults: Dict[str, Any] = {
        "FoldRotor": False,
    }

    class Properties:

        class FoldRotor:
            id = "FoldRotor"

    properties = {
        "FoldRotor": UnitPropertyDescription(
            identifier="FoldRotor",
            control="checkbox",
            label="Fold Main Rotor",
            default=False,
            weight_when_on=0,
            w_ctrl=20,
        ),
    }

    livery_name = "VWV_CH46D"  # from type

    pylons: Set[int] = set()

    tasks = [task.Transport, task.Reconnaissance]
    task_default = task.Transport


@helicoptermod
class vwv_ch46d_late(HelicopterType):
    id = "vwv_ch46d_late"
    height = 5.08
    width = 15.24
    length = 13.92
    fuel_max = 1080
    max_speed = 267
    chaff = 0
    flare = 60
    charge_total = 60
    chaff_charge_size = 0
    flare_charge_size = 1
    radio_frequency = 225

    property_defaults: Dict[str, Any] = {
        "FoldRotor": False,
        "RemoveCMDS": False,
    }

    class Properties:

        class FoldRotor:
            id = "FoldRotor"

        class RemoveCMDS:
            id = "RemoveCMDS"

    properties = {
        "FoldRotor": UnitPropertyDescription(
            identifier="FoldRotor",
            control="checkbox",
            label="Fold Main Rotor",
            default=False,
            weight_when_on=0,
            w_ctrl=20,
        ),
        "RemoveCMDS": UnitPropertyDescription(
            identifier="RemoveCMDS",
            control="checkbox",
            label="Remove CM Dispensers",
            default=False,
            weight_when_on=-15,
            w_ctrl=20,
        ),
    }

    livery_name = "VWV_CH46D_LATE"  # from type

    pylons: Set[int] = set()

    tasks = [task.Transport, task.Reconnaissance]
    task_default = task.Transport


## FORTIFICATIONS (Buildings)
# These are static objects that don't require specific decorators like shipmod
# They are part of the static environment and are handled as static objects
class vwv_bdg_indohut1(unittype.StaticType):
    id = "vwv_bdg_indohut1"
    name = "[VWV] Indochina Hut High"
    shape_name = (
        "vwv_bdg_indohut1"  # This would need to be determined from the actual model
    )
    rate = 100


class vwv_bdg_indohut2(unittype.StaticType):
    id = "vwv_bdg_indohut2"
    name = "[VWV] Indochina Hut Low"
    shape_name = "vwv_bdg_indohut2"
    rate = 100


class vwv_bdg_guardTower(unittype.StaticType):
    id = "vwv_bdg_guardTower"
    name = "[VWV] Guard Tower"
    shape_name = "vwv_bdg_guardTower"
    rate = 100


class vwv_bdg_usWatchTower(unittype.StaticType):
    id = "vwv_bdg_usWatchTower"
    name = "[VWV] US Watch Tower"
    shape_name = "vwv_bdg_usWatchTower"
    rate = 100


class vwv_bdg_usBarrelGasoline(unittype.StaticType):
    id = "vwv_bdg_usBarrelGasoline"
    name = "[VWV] US Barrel Gasoline"
    shape_name = "vwv_bdg_usBarrelGasoline"
    rate = 100


class vwv_bdg_usBarrelGasoline2(unittype.StaticType):
    id = "vwv_bdg_usBarrelGasoline2"
    name = "[VWV] US Barrel Gasoline 2"
    shape_name = "vwv_bdg_usBarrelGasoline2"
    rate = 100


class vwv_bdg_usBarrelGasolineSpigot(unittype.StaticType):
    id = "vwv_bdg_usBarrelGasolineSpigot"
    name = "[VWV] US Barrel Gasoline Spigot"
    shape_name = "vwv_bdg_usBarrelGasolineSpigot"
    rate = 100


class vwv_bdg_usBarrelMotorfuel(unittype.StaticType):
    id = "vwv_bdg_usBarrelMotorfuel"
    name = "[VWV] US Barrel Motor Fuel"
    shape_name = "vwv_bdg_usBarrelMotorfuel"
    rate = 100


class vwv_bdg_usBarrelWastefuel(unittype.StaticType):
    id = "vwv_bdg_usBarrelWastefuel"
    name = "[VWV] US Barrel Waste Fuel"
    shape_name = "vwv_bdg_usBarrelWastefuel"
    rate = 100


class vwv_bdg_usBarrelWasteoil(unittype.StaticType):
    id = "vwv_bdg_usBarrelWasteoil"
    name = "[VWV] US Barrel Waste Oil"
    shape_name = "vwv_bdg_usBarrelWasteoil"
    rate = 100


class vwv_bdg_usBoomgate(unittype.StaticType):
    id = "vwv_bdg_usBoomgate"
    name = "[VWV] US Boomgate"
    shape_name = "vwv_bdg_usBoomgate"
    rate = 100


class vwv_bdg_usConnex(unittype.StaticType):
    id = "vwv_bdg_usConnex"
    name = "[VWV] US Connex (half)"
    shape_name = "vwv_bdg_usConnex"
    rate = 100


class vwv_bdg_usBarbedWire(unittype.StaticType):
    id = "vwv_bdg_usBarbedWire"
    name = "[VWV] US Barbed Wire (1)"
    shape_name = "vwv_bdg_usBarbedWire"
    rate = 100


class vwv_bdg_usBarbedWireOpen(unittype.StaticType):
    id = "vwv_bdg_usBarbedWireOpen"
    name = "[VWV] US Barbed Wire Open (2)"
    shape_name = "vwv_bdg_usBarbedWireOpen"
    rate = 100


class vwv_bdg_usBarbedWireOpen20(unittype.StaticType):
    id = "vwv_bdg_usBarbedWireOpen20"
    name = "[VWV] US Barbed Wire Open (20)"
    shape_name = "vwv_bdg_usBarbedWireOpen20"
    rate = 100


class vwv_bdg_usGuardHouse(unittype.StaticType):
    id = "vwv_bdg_usGuardHouse"
    name = "[VWV] US Guard House"
    shape_name = "vwv_bdg_usGuardHouse"
    rate = 100


class vwv_bdg_usMarsdenMat(unittype.StaticType):
    id = "vwv_bdg_usMarsdenMat"
    name = "[VWV] US Marsden Mat"
    shape_name = "vwv_bdg_usMarsdenMat"
    rate = 100


class vwv_bdg_usRevetment(unittype.StaticType):
    id = "vwv_bdg_usRevetment"
    name = "[VWV] US Revetment"
    shape_name = "vwv_bdg_usRevetment"
    rate = 100


class vwv_bdg_usHangar(unittype.StaticType):
    id = "vwv_bdg_usHangar"
    name = "[VWV] US Hangar"
    shape_name = "vwv_bdg_usHangar"
    rate = 100


class vwv_bdg_usBarrack(unittype.StaticType):
    id = "vwv_bdg_usBarrack"
    name = "[VWV] US Barrack"
    shape_name = "vwv_bdg_usBarrack"
    rate = 100


class VAP_FARP_1(unittype.StaticType):
    id = "VAP FARP 1"
    name = "VAP FARP 1"
    shape_name = "vap_us_farp_1"
    category = "Heliports"
    rate = 100


class VAP_FARP_2(unittype.StaticType):
    id = "VAP FARP 2"
    name = "VAP FARP 2"
    shape_name = "vap_us_farp_2"
    category = "Heliports"
    rate = 100


class VAP_FARP_3(unittype.StaticType):
    id = "VAP FARP 3"
    name = "VAP FARP 3"
    shape_name = "vap_us_farp_3"
    category = "Heliports"
    rate = 100


class VAP_FARP_4(unittype.StaticType):
    id = "VAP FARP 4"
    name = "VAP FARP 4"
    shape_name = "vap_us_farp_4"
    category = "Heliports"
    rate = 100


@planemod
class vwv_crusader_np(PlaneType):
    id = "vwv_crusader_np"
    height = 4.8
    width = 10.72
    length = 16.61
    fuel_max = 4096
    max_speed = 1976.4
    chaff = 120
    flare = 120
    charge_total = 240
    chaff_charge_size = 1
    flare_charge_size = 1
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}

    class Pylon2:
        AIM_9B_Sidewinder_IR_AAM = (2, Weapons.AIM_9B_Sidewinder_IR_AAM)
        AIM_9J_Sidewinder_IR_AAM = (2, Weapons.AIM_9J_Sidewinder_IR_AAM)
        R550_Magic_1_IR_AAM = (2, Weapons.R550_Magic_1_IR_AAM)

    class Pylon3:
        AIM_9B_Sidewinder_IR_AAM = (3, Weapons.AIM_9B_Sidewinder_IR_AAM)
        AIM_9J_Sidewinder_IR_AAM = (3, Weapons.AIM_9J_Sidewinder_IR_AAM)
        R550_Magic_1_IR_AAM = (3, Weapons.R550_Magic_1_IR_AAM)

    class Pylon4:
        AIM_9B_Sidewinder_IR_AAM = (4, Weapons.AIM_9B_Sidewinder_IR_AAM)
        AIM_9J_Sidewinder_IR_AAM = (4, Weapons.AIM_9J_Sidewinder_IR_AAM)
        R550_Magic_1_IR_AAM = (4, Weapons.R550_Magic_1_IR_AAM)

    class Pylon5:
        AIM_9B_Sidewinder_IR_AAM = (5, Weapons.AIM_9B_Sidewinder_IR_AAM)
        AIM_9J_Sidewinder_IR_AAM = (5, Weapons.AIM_9J_Sidewinder_IR_AAM)
        R550_Magic_1_IR_AAM = (5, Weapons.R550_Magic_1_IR_AAM)

    pylons: Set[int] = {2, 3, 4, 5}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.Reconnaissance,
    ]
    task_default = task.CAP


@planemod
class vwv_ec_121(PlaneType):
    id = "vwv_ec-121"
    height = 7.54
    width = 38.47
    length = 35.41
    fuel_max = 21000
    max_speed = 480.96
    category = "AWACS"  # {D2BC159C-5B7D-40cf-92CD-44DF3E99FAA9}
    radio_frequency = 127.5

    livery_name = "VWV_EC-121"  # from type

    pylons: Set[int] = set()

    tasks = [task.AWACS, task.Transport]
    task_default = task.AWACS

    tasks = [task.AWACS, task.Transport]
    task_default = task.AWACS


@planemod
class vwv_l_1049(PlaneType):
    id = "vwv_l-1049"
    height = 7.54
    width = 38.47
    length = 35.41
    fuel_max = 17850
    max_speed = 531
    radio_frequency = 127.5

    livery_name = "VWV_L-1049"  # from type

    pylons: Set[int] = set()

    tasks = [task.Transport]
    task_default = task.Transport

    tasks = [task.Transport]
    task_default = task.Transport


@planemod
class vwv_rf101b(PlaneType):
    id = "vwv_rf101b"
    height = 5.49
    width = 12.09
    length = 20.55
    fuel_max = 7770
    max_speed = 2448
    chaff = 0
    flare = 0
    charge_total = 0
    chaff_charge_size = 0
    flare_charge_size = 0
    category = "Reconnaissance"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    livery_name = "VWV_RF101B"  # from type

    pylons: Set[int] = set()

    tasks = [task.Reconnaissance, task.AFAC, task.CAS]
    task_default = task.Reconnaissance


@planemod
class vwv_a_37_dragonfly(PlaneType):
    id = "a_37_dragonfly"
    height = 2.7
    width = 10.93
    length = 8.92
    fuel_max = 1540
    max_speed = 813.6
    radio_frequency = 225

    livery_name = "A_37_DRAGONFLY"  # from type

    class Pylon1:
        Mk_82___500lb_GP_Bomb_LD = (1, Weapons.Mk_82___500lb_GP_Bomb_LD)
        # ERRR {mk77mod1}
        # ERRR {M260_HYDRA_WP}
        # ERRR {M260_HYDRA}
        LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_1_HE = (
            1,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_1_HE,
        )
        AIM_9B_Sidewinder_IR_AAM = (1, Weapons.AIM_9B_Sidewinder_IR_AAM)

    class Pylon2:
        Mk_82___500lb_GP_Bomb_LD = (2, Weapons.Mk_82___500lb_GP_Bomb_LD)
        # ERRR {mk77mod1}
        # ERRR {M260_HYDRA}
        LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_1_HE = (
            2,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_1_HE,
        )
        LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_5_HEAT = (
            2,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_5_HEAT,
        )

    class Pylon3:
        Mk_82___500lb_GP_Bomb_LD = (3, Weapons.Mk_82___500lb_GP_Bomb_LD)
        # ERRR {mk77mod1}
        # ERRR {M260_HYDRA}
        LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_1_HE = (
            3,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_1_HE,
        )
        LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_5_HEAT = (
            3,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_5_HEAT,
        )

    class Pylon4:
        Mk_82___500lb_GP_Bomb_LD = (4, Weapons.Mk_82___500lb_GP_Bomb_LD)
        # ERRR {mk77mod1}
        # ERRR {M260_HYDRA}
        LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_1_HE = (
            4,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_1_HE,
        )

    class Pylon5:
        Mk_82___500lb_GP_Bomb_LD = (5, Weapons.Mk_82___500lb_GP_Bomb_LD)
        # ERRR {mk77mod1}
        # ERRR {M260_HYDRA}
        LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_1_HE = (
            5,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_1_HE,
        )

    class Pylon6:
        Mk_82___500lb_GP_Bomb_LD = (6, Weapons.Mk_82___500lb_GP_Bomb_LD)
        # ERRR {mk77mod1}
        # ERRR {M260_HYDRA}
        LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_1_HE = (
            6,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_1_HE,
        )
        LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_5_HEAT = (
            6,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_5_HEAT,
        )

    class Pylon7:
        Mk_82___500lb_GP_Bomb_LD = (7, Weapons.Mk_82___500lb_GP_Bomb_LD)
        # ERRR {mk77mod1}
        # ERRR {M260_HYDRA}
        LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_1_HE = (
            7,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_1_HE,
        )
        LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_5_HEAT = (
            7,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_5_HEAT,
        )
        AIM_9B_Sidewinder_IR_AAM = (7, Weapons.AIM_9B_Sidewinder_IR_AAM)

    class Pylon8:
        Mk_82___500lb_GP_Bomb_LD = (8, Weapons.Mk_82___500lb_GP_Bomb_LD)
        # ERRR {mk77mod1}
        # ERRR {M260_HYDRA}
        LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_1_HE = (
            8,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_1_HE,
        )
        AIM_9B_Sidewinder_IR_AAM = (8, Weapons.AIM_9B_Sidewinder_IR_AAM)

    class Pylon9:
        dragonfly_fuel_tanks = (9, WeaponsVWV.dragonfly_fuel_tanks)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9}

    tasks = [
        task.GroundAttack,
        task.CAS,
        task.AFAC,
        task.RunwayAttack,
        task.AntishipStrike,
    ]
    task_default = task.GroundAttack


@helicoptermod
class uh2a(HelicopterType):
    id = "uh2a"
    height = 4.11
    width = 13.41
    length = 11.48
    fuel_max = 836
    max_speed = 261
    radio_frequency = 225

    property_defaults: Dict[str, Any] = {
        "FoldRotor": False,
    }

    class Properties:

        class FoldRotor:
            id = "FoldRotor"

    properties = {
        "FoldRotor": UnitPropertyDescription(
            identifier="FoldRotor",
            control="checkbox",
            label="Fold Main Rotor",
            default=False,
            weight_when_on=0,
            w_ctrl=150,
        ),
    }

    livery_name = "UH2A"  # from livery_entry

    class Pylon1:
        SH2F_Fuel_Tank_120_gallons_R = (1, Weapons.SH2F_Fuel_Tank_120_gallons_R)  # type: ignore[reportAttributeAccessIssue]

    class Pylon2:
        SH2F_Fuel_Tank_120_gallons_L = (2, Weapons.SH2F_Fuel_Tank_120_gallons_L)  # type: ignore[reportAttributeAccessIssue]

    pylons: Set[int] = {1, 2}

    tasks = [task.Transport, task.Reconnaissance]
    task_default = task.Transport


@helicoptermod
class uh2b(HelicopterType):
    id = "uh2b"
    height = 4.11
    width = 13.41
    length = 11.48
    fuel_max = 836
    max_speed = 261
    radio_frequency = 225

    property_defaults: Dict[str, Any] = {
        "FoldRotor": False,
    }

    class Properties:

        class FoldRotor:
            id = "FoldRotor"

    properties = {
        "FoldRotor": UnitPropertyDescription(
            identifier="FoldRotor",
            control="checkbox",
            label="Fold Main Rotor",
            default=False,
            weight_when_on=0,
            w_ctrl=150,
        ),
    }

    livery_name = "UH2B"  # from livery_entry

    class Pylon1:
        SH2F_Fuel_Tank_120_gallons_R = (1, Weapons.SH2F_Fuel_Tank_120_gallons_R)  # type: ignore[reportAttributeAccessIssue]

    class Pylon2:
        SH2F_Fuel_Tank_120_gallons_L = (2, Weapons.SH2F_Fuel_Tank_120_gallons_L)  # type: ignore[reportAttributeAccessIssue]

    pylons: Set[int] = {1, 2}

    tasks = [task.Transport, task.Reconnaissance]
    task_default = task.Transport


@helicoptermod
class uh2c(HelicopterType):
    id = "uh2c"
    height = 4.4
    width = 13.41
    length = 11.48
    fuel_max = 836
    max_speed = 265
    radio_frequency = 225

    property_defaults: Dict[str, Any] = {
        "FoldRotor": False,
    }

    class Properties:

        class FoldRotor:
            id = "FoldRotor"

    properties = {
        "FoldRotor": UnitPropertyDescription(
            identifier="FoldRotor",
            control="checkbox",
            label="Fold Main Rotor",
            default=False,
            weight_when_on=0,
            w_ctrl=150,
        ),
    }

    livery_name = "UH2C"  # from livery_entry

    class Pylon1:
        SH2F_Fuel_Tank_120_gallons_R = (1, Weapons.SH2F_Fuel_Tank_120_gallons_R)  # type: ignore[reportAttributeAccessIssue]

    class Pylon2:
        SH2F_Fuel_Tank_120_gallons_L = (2, Weapons.SH2F_Fuel_Tank_120_gallons_L)  # type: ignore[reportAttributeAccessIssue]

    pylons: Set[int] = {1, 2}

    tasks = [task.Transport, task.Reconnaissance]
    task_default = task.Transport


@helicoptermod
class sh2f(HelicopterType):
    id = "sh2f"
    height = 4.4
    width = 13.41
    length = 11.68
    fuel_max = 816
    max_speed = 265
    radio_frequency = 225

    property_defaults: Dict[str, Any] = {
        "FoldRotor": False,
    }

    class Properties:
        class FoldRotor:
            id = "FoldRotor"

    properties = {
        "FoldRotor": UnitPropertyDescription(
            identifier="FoldRotor",
            control="checkbox",
            label="Fold Main Rotor",
            default=False,
            weight_when_on=0,
            w_ctrl=150,
        ),
    }

    livery_name = "SH2F"  # from livery_entry

    class Pylon1:
        SH2F_MAD = (1, Weapons.SH2F_MAD)  # type: ignore[reportAttributeAccessIssue]

    class Pylon2:
        SH2F_Fuel_Tank_120_gallons_R = (2, Weapons.SH2F_Fuel_Tank_120_gallons_R)  # type: ignore[reportAttributeAccessIssue]

    class Pylon3:
        SH2F_Fuel_Tank_120_gallons_L = (3, Weapons.SH2F_Fuel_Tank_120_gallons_L)  # type: ignore[reportAttributeAccessIssue]

    class Pylon4:
        DIS_mk46torp = (4, Weapons.DIS_mk46torp)

    pylons: Set[int] = {1, 2, 3, 4}

    tasks = [task.AntishipStrike, task.Transport, task.Reconnaissance]
    task_default = task.AntishipStrike


@vehiclemod
class vwv_vn_guardTower(unittype.VehicleType):
    id = "vwv_vn_guardTower"
    name = "[VWV] VC Guard Tower (armed)"
    detection_range = 1000
    threat_range = 500
    air_weapon_dist = 500


@vehiclemod
class vap_mutt_gun(unittype.VehicleType):
    id = "vap_mutt_gun"
    name = "VAP US MUTT Gun"
    detection_range = 3500
    threat_range = 6850
    air_weapon_dist = 6850


@vehiclemod
class vap_type63_mlrs(unittype.VehicleType):
    id = "vap_type63_mlrs"
    name = "VAP VC Type63 107mm MLRS"
    detection_range = 0
    threat_range = 8500
    air_weapon_dist = 8500


@vehiclemod
class vap_vc_bicycle_mortar(unittype.VehicleType):
    id = "vap_vc_bicycle_mortar"
    name = "VAP VC Bicycle Mortar"
    detection_range = 0
    threat_range = 7000
    air_weapon_dist = 7000


@vehiclemod
class vap_m35_gun_truck(unittype.VehicleType):
    id = "vap_m35_gun_truck"
    name = "VAP US M35 Gun Truck"
    detection_range = 0
    threat_range = 4500
    air_weapon_dist = 4500


@vehiclemod
class vap_zis_150_aa(unittype.VehicleType):
    id = "vap_zis_150_aa"
    name = "VAP VC ZiS-150 AA Type 96"
    detection_range = 7000
    threat_range = 6800
    air_weapon_dist = 6800


@vehiclemod
class vap_us_hooch_LP(unittype.VehicleType):
    id = "vap_us_hooch_LP"
    name = "VAP US Hooch Low Poly"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class vap_ammo_50cal_line(unittype.VehicleType):
    id = "vap_ammo_50cal_line"
    name = "VAP US Ammo 50Cal Line"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class vap_ammo_50cal_pack(unittype.VehicleType):
    id = "vap_ammo_50cal_pack"
    name = "VAP US Ammo 50Cal Pack"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class vap_barrels_line(unittype.VehicleType):
    id = "vap_barrels_line"
    name = "VAP Barrels Line"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class vap_barrels(unittype.VehicleType):
    id = "vap_barrels"
    name = "VAP Barrels Pack"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class vap_ammo_box_pile(unittype.VehicleType):
    id = "vap_ammo_box_pile"
    name = "VAP Ammo Box Pile"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class vap_ammo_box_wood_long(unittype.VehicleType):
    id = "vap_ammo_box_wood_long"
    name = "VAP Ammo Box Long"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class vap_ammo_box_wood_small(unittype.VehicleType):
    id = "vap_ammo_box_wood_small"
    name = "VAP Ammo Box Small"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class vap_barrel_red(unittype.VehicleType):
    id = "vap_barrel_red"
    name = "VAP Barrel Red"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class vap_barrel_green(unittype.VehicleType):
    id = "vap_barrel_green"
    name = "VAP Barrel Green"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class vap_mre_boxes(unittype.VehicleType):
    id = "vap_mre_boxes"
    name = "VAP US MRE Boxes"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class vap_mixed_cargo_1(unittype.VehicleType):
    id = "vap_mixed_cargo_1"
    name = "VAP US Mixed Cargo 1"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class vap_mixed_cargo_2(unittype.VehicleType):
    id = "vap_mixed_cargo_2"
    name = "VAP US Mixed Cargo 2"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class vap_watchtower(unittype.VehicleType):
    id = "vap_watchtower"
    name = "VAP Vietcong Watchtower"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class vap_house_high(unittype.VehicleType):
    id = "vap_house_high"
    name = "VAP Bamboo House High"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class vap_house_long(unittype.VehicleType):
    id = "vap_house_long"
    name = "VAP Bamboo House Long"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class vap_house_small(unittype.VehicleType):
    id = "vap_house_small"
    name = "VAP Bamboo House Small"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class vap_house_T(unittype.VehicleType):
    id = "vap_house_T"
    name = "VAP Bamboo House T-Shape"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class vap_house_tiny(unittype.VehicleType):
    id = "vap_house_tiny"
    name = "VAP Bamboo House Tiny"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class vap_house1(unittype.VehicleType):
    id = "vap_house1"
    name = "VAP Bamboo House"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class vap_us_hooch_radio(unittype.VehicleType):
    id = "vap_us_hooch_radio"
    name = "VAP US Hooch Radio"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class vap_us_hooch_closed(unittype.VehicleType):
    id = "vap_us_hooch_closed"
    name = "VAP US Hooch Closed"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class vap_vc_bunker_single(unittype.VehicleType):
    id = "vap_vc_bunker_single"
    name = "VAP VC Bunker"
    detection_range = 1500
    threat_range = 550
    air_weapon_dist = 550


@vehiclemod
class vap_vc_mg_nest(unittype.VehicleType):
    id = "vap_vc_mg_nest"
    name = "VAP VC MG Nest"
    detection_range = 1000
    threat_range = 550
    air_weapon_dist = 550


@vehiclemod
class vap_vc_tunnel(unittype.VehicleType):
    id = "vap_vc_tunnel"
    name = "VAP VC Tunnel"
    detection_range = 500
    threat_range = 500
    air_weapon_dist = 500


@vehiclemod
class vap_mule(unittype.VehicleType):
    id = "vap_mule"
    name = "VAP US Mule"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class vap_mutt(unittype.VehicleType):
    id = "vap_mutt"
    name = "VAP US MUTT"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class vap_m35_truck(unittype.VehicleType):
    id = "vap_m35_truck"
    name = "VAP US M35 Truck"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class vap_vc_zis(unittype.VehicleType):
    id = "vap_vc_zis"
    name = "VAP VC Zis 150"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class vap_civ_zis_150(unittype.VehicleType):
    id = "vap_civ_zis_150"
    name = "VAP Civilian Zis 150"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class vap_vc_bicycle(unittype.VehicleType):
    id = "vap_vc_bicycle"
    name = "VAP VC Bicycle"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class vap_vc_bicycle_ammo(unittype.VehicleType):
    id = "vap_vc_bicycle_ammo"
    name = "VAP VC Bicycle Ammo"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class _vap_loudspeakersVietnam(unittype.VehicleType):
    id = "_vap_loudspeakersVietnam"
    name = "VAP Loudspeakers Radio Vietnam"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class vap_vc_zil(unittype.VehicleType):
    id = "vap_vc_zil"
    name = "VAP VC Zil 130 Armed"
    detection_range = 750
    threat_range = 500
    air_weapon_dist = 500


@vehiclemod
class vap_vc_bicycle_ak(unittype.VehicleType):
    id = "vap_vc_bicycle_ak"
    name = "VAP VC Bicycle AK"
    detection_range = 1500
    threat_range = 1500
    air_weapon_dist = 1500


@cargomod
class vwv_cgo_usConex(unittype.StaticType):
    id = "vwv_cgo_usConex"
    name = "[VWV] US Conex (half), Cargo"
    shape_name = "vwv_us_connex"
    category = "Cargos"
    rate = 10
    can_cargo = True


@cargomod
class vwv_cgo_usBlu82C130(unittype.StaticType):
    id = "vwv_cgo_usBlu82C130"
    name = "[VWV] US blu82 for C130, Cargo"
    shape_name = "vwv_us_blu82_c130"
    category = "Cargos"
    rate = 10
    can_cargo = True


class vwv_farp_marsdenmat(unittype.StaticType):
    id = "vwv_farp_marsdenmat"
    name = "[VWV] Marsden Mat"
    shape_name = "vwv_us_marsdenmat"
    category = "Heliports"
    rate = 100


@cargomod
class vap_oh6_cargo(unittype.StaticType):
    id = "vap_oh6_cargo"
    name = "VAP OH-6 Cargo"
    shape_name = "vap_oh6_cargo"
    category = "Cargos"
    rate = 100
    can_cargo = True
