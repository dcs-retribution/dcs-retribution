# Requires Vietnam War Vessels for DCS by TeTeT:
# https://forum.dcs.world/topic/338387-tetets-vietnam-war-vessels/
# https://github.com/tspindler-cms/tetet-vwv/releases


from typing import Set

from dcs import unittype, task
from dcs.planes import PlaneType
from dcs.helicopters import HelicopterType
from dcs.weapons_data import Weapons

from game.modsupport import shipmod, planemod, helicoptermod


## SHIPS


@shipmod
class PBR_MKII(unittype.ShipType):
    id = "PBR_MKII"
    name = "Patrol Boat, River MkII"
    detection_range = 40000
    threat_range = 5200
    air_weapon_dist = 5200


@shipmod
class USS_Sumner(unittype.ShipType):
    id = "USS Sumner"
    name = "USS Allen M. Sumner (DD-692)"
    plane_num = 0
    helicopter_num = 1
    parking = 1
    detection_range = 45000
    threat_range = 18650
    air_weapon_dist = 18650


@shipmod
class Cva_31(unittype.ShipType):
    id = "cva-31"
    name = "CVA-31 Bon Homme Richard"
    plane_num = 8
    helicopter_num = 3
    parking = 2
    detection_range = 28000
    threat_range = 15000
    air_weapon_dist = 15000


@shipmod
class USS_Fletcher(unittype.ShipType):
    id = "USS Fletcher"
    name = "USS Fletcher FRAM II Destroyer"
    plane_num = 1
    helicopter_num = 1
    parking = 1
    detection_range = 45000
    threat_range = 18650
    air_weapon_dist = 18650


@shipmod
class USS_Laffey(unittype.ShipType):
    id = "USS Laffey"
    name = "USS Laffey (DD-724)"
    plane_num = 0
    helicopter_num = 1
    parking = 1
    detection_range = 45000
    threat_range = 18650
    air_weapon_dist = 18650


@shipmod
class USS_Maddox(unittype.ShipType):
    id = "USS Maddox"
    name = "USS Maddox (DD-731)"
    detection_range = 45000
    threat_range = 18650
    air_weapon_dist = 18650


@shipmod
class USS_The_Sullivans(unittype.ShipType):
    id = "USS The Sullivans"
    name = "USS The Sullivans (DD-537)"
    detection_range = 45000
    threat_range = 18650
    air_weapon_dist = 18650


@shipmod
class P4(unittype.ShipType):
    id = "P4"
    name = "P 4 Torpedo Boat"
    detection_range = 3000
    threat_range = 1000
    air_weapon_dist = 1000


## AIRPLANES

# TODO inject weapons, see SWPack.py and a4ec.py


@planemod
class vwv_a1_skyraider(PlaneType):
    id = "vwv_a1_skyraider"
    height = 5.28
    width = 15.24
    length = 15.96
    fuel_max = 1036
    max_speed = 594
    chaff = 240
    flare = 240
    charge_total = 480
    chaff_charge_size = 1
    flare_charge_size = 1
    radio_frequency = 127.5

    livery_name = "VWV_A1_SKYRAIDER"  # from type

    class Pylon1:
        AN_M30A1___100lb_GP_Bomb_LD = (1, Weapons.AN_M30A1___100lb_GP_Bomb_LD)
        AN_M57___250lb_GP_Bomb_LD = (1, Weapons.AN_M57___250lb_GP_Bomb_LD)
        AN_M81___260lb_GP_Bomb_LD = (1, Weapons.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (1, Weapons.AN_M88___220lb_GP_Bomb_LD)
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
        AN_M81___260lb_GP_Bomb_LD = (2, Weapons.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (2, Weapons.AN_M88___220lb_GP_Bomb_LD)
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
        AN_M81___260lb_GP_Bomb_LD = (3, Weapons.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (3, Weapons.AN_M88___220lb_GP_Bomb_LD)
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
        AN_M81___260lb_GP_Bomb_LD = (4, Weapons.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (4, Weapons.AN_M88___220lb_GP_Bomb_LD)
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
        AN_M81___260lb_GP_Bomb_LD = (5, Weapons.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (5, Weapons.AN_M88___220lb_GP_Bomb_LD)
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
        AN_M81___260lb_GP_Bomb_LD = (6, Weapons.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (6, Weapons.AN_M88___220lb_GP_Bomb_LD)
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
        AN_M81___260lb_GP_Bomb_LD = (7, Weapons.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (7, Weapons.AN_M88___220lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (7, Weapons.M117___750lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            7,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        Mk_82___500lb_GP_Bomb_LD = (7, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_83___1000lb_GP_Bomb_LD = (7, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        Mk_84___2000lb_GP_Bomb_LD = (7, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        SUU_25_x_8_LUU_2___Target_Marker_Flares = (
            7,
            Weapons.SUU_25_x_8_LUU_2___Target_Marker_Flares,
        )
        AERO_1D_300_Gallons_Fuel_Tank_ = (7, Weapons.AERO_1D_300_Gallons_Fuel_Tank_)
        Fuel_Tank_150_gallons = (7, Weapons.Fuel_Tank_150_gallons)
        Fuel_Tank_150_gallons__EMPTY_ = (7, Weapons.Fuel_Tank_150_gallons__EMPTY_)
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
        Tiny_Tim = (7, Weapons.Tiny_Tim)
        LTF_5b_Aerial_Torpedo = (7, Weapons.LTF_5b_Aerial_Torpedo)
        DIS_mk46torp = (7, Weapons.DIS_mk46torp)
        toilet_bomb = (7, Weapons.toilet_bomb)

    class Pylon8:
        AN_M30A1___100lb_GP_Bomb_LD = (8, Weapons.AN_M30A1___100lb_GP_Bomb_LD)
        AN_M57___250lb_GP_Bomb_LD = (8, Weapons.AN_M57___250lb_GP_Bomb_LD)
        AN_M64___500lb_GP_Bomb_LD = (8, Weapons.AN_M64___500lb_GP_Bomb_LD)
        AN_M65___1000lb_GP_Bomb_LD = (8, Weapons.AN_M65___1000lb_GP_Bomb_LD)
        AN_M81___260lb_GP_Bomb_LD = (8, Weapons.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (8, Weapons.AN_M88___220lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (8, Weapons.M117___750lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            8,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
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
        AN_M81___260lb_GP_Bomb_LD = (9, Weapons.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (9, Weapons.AN_M88___220lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (9, Weapons.M117___750lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            9,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        Mk_82___500lb_GP_Bomb_LD = (9, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_83___1000lb_GP_Bomb_LD = (9, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        Mk_84___2000lb_GP_Bomb_LD = (9, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        SUU_25_x_8_LUU_2___Target_Marker_Flares = (
            9,
            Weapons.SUU_25_x_8_LUU_2___Target_Marker_Flares,
        )
        AERO_1D_300_Gallons_Fuel_Tank_ = (9, Weapons.AERO_1D_300_Gallons_Fuel_Tank_)
        Fuel_Tank_150_gallons = (9, Weapons.Fuel_Tank_150_gallons)
        Fuel_Tank_150_gallons__EMPTY_ = (9, Weapons.Fuel_Tank_150_gallons__EMPTY_)
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
        Tiny_Tim = (9, Weapons.Tiny_Tim)
        LTF_5b_Aerial_Torpedo = (9, Weapons.LTF_5b_Aerial_Torpedo)
        DIS_mk46torp = (9, Weapons.DIS_mk46torp)
        toilet_bomb = (9, Weapons.toilet_bomb)

    class Pylon10:
        AN_M30A1___100lb_GP_Bomb_LD = (10, Weapons.AN_M30A1___100lb_GP_Bomb_LD)
        AN_M57___250lb_GP_Bomb_LD = (10, Weapons.AN_M57___250lb_GP_Bomb_LD)
        AN_M81___260lb_GP_Bomb_LD = (10, Weapons.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (10, Weapons.AN_M88___220lb_GP_Bomb_LD)
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
        AN_M81___260lb_GP_Bomb_LD = (11, Weapons.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (11, Weapons.AN_M88___220lb_GP_Bomb_LD)
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
        AN_M81___260lb_GP_Bomb_LD = (12, Weapons.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (12, Weapons.AN_M88___220lb_GP_Bomb_LD)
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
        AN_M81___260lb_GP_Bomb_LD = (13, Weapons.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (13, Weapons.AN_M88___220lb_GP_Bomb_LD)
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
        AN_M81___260lb_GP_Bomb_LD = (14, Weapons.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (14, Weapons.AN_M88___220lb_GP_Bomb_LD)
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
        AN_M81___260lb_GP_Bomb_LD = (15, Weapons.AN_M81___260lb_GP_Bomb_LD)
        AN_M88___220lb_GP_Bomb_LD = (15, Weapons.AN_M88___220lb_GP_Bomb_LD)
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

    tasks = [task.Reconnaissance]
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
            Weapons.BRU_41A_with_4_x_Mk_82___500lb_GP_Bomb_HD_Left,
        )
        BRU_41A_with_4_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_Left = (
            1,
            Weapons.BRU_41A_with_4_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_Left,
        )
        M117___750lb_GP_Bomb_LD = (1, Weapons.M117___750lb_GP_Bomb_LD)
        Mk_84___2000lb_GP_Bomb_LD = (1, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        Fuel_Tank_300_gallons_ = (1, Weapons.Fuel_Tank_300_gallons_)
        Fuel_Tank_300_gallons__EMPTY__ = (1, Weapons.Fuel_Tank_300_gallons__EMPTY__)
        Fuel_Tank_150_gallons = (1, Weapons.Fuel_Tank_150_gallons)
        Fuel_Tank_150_gallons__EMPTY_ = (1, Weapons.Fuel_Tank_150_gallons__EMPTY_)

    # ERRR <CLEAN>

    class Pylon2:
        AIM_9B_Sidewinder_IR_AAM = (2, Weapons.AIM_9B_Sidewinder_IR_AAM)
        AIM_9C_Sidewinder_SARH_AAM = (2, Weapons.AIM_9C_Sidewinder_SARH_AAM)
        AIM_9D_Sidewinder_IR_AAM = (2, Weapons.AIM_9D_Sidewinder_IR_AAM)
        AIM_9J_Sidewinder_IR_AAM = (2, Weapons.AIM_9J_Sidewinder_IR_AAM)
        LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE = (
            2,
            Weapons.LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE,
        )

    class Pylon3:
        AIM_9B_Sidewinder_IR_AAM = (3, Weapons.AIM_9B_Sidewinder_IR_AAM)
        AIM_9C_Sidewinder_SARH_AAM = (3, Weapons.AIM_9C_Sidewinder_SARH_AAM)
        AIM_9D_Sidewinder_IR_AAM = (3, Weapons.AIM_9D_Sidewinder_IR_AAM)
        AIM_9J_Sidewinder_IR_AAM = (3, Weapons.AIM_9J_Sidewinder_IR_AAM)
        LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE = (
            3,
            Weapons.LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE,
        )

    class Pylon4:
        AIM_9B_Sidewinder_IR_AAM = (4, Weapons.AIM_9B_Sidewinder_IR_AAM)
        AIM_9C_Sidewinder_SARH_AAM = (4, Weapons.AIM_9C_Sidewinder_SARH_AAM)
        AIM_9D_Sidewinder_IR_AAM = (4, Weapons.AIM_9D_Sidewinder_IR_AAM)
        AIM_9J_Sidewinder_IR_AAM = (4, Weapons.AIM_9J_Sidewinder_IR_AAM)
        LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE = (
            4,
            Weapons.LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE,
        )

    class Pylon5:
        AIM_9B_Sidewinder_IR_AAM = (5, Weapons.AIM_9B_Sidewinder_IR_AAM)
        AIM_9C_Sidewinder_SARH_AAM = (5, Weapons.AIM_9C_Sidewinder_SARH_AAM)
        AIM_9D_Sidewinder_IR_AAM = (5, Weapons.AIM_9D_Sidewinder_IR_AAM)
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
        _2_Mk_82_Snakeye_____ = (6, Weapons._2_Mk_82_Snakeye_____)
        _2_Mk_82_____ = (6, Weapons._2_Mk_82_____)
        BRU_41A_with_4_x_Mk_82___500lb_GP_Bomb_HD_Right = (
            6,
            Weapons.BRU_41A_with_4_x_Mk_82___500lb_GP_Bomb_HD_Right,
        )
        BRU_41A_with_4_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_Right = (
            6,
            Weapons.BRU_41A_with_4_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_Right,
        )
        M117___750lb_GP_Bomb_LD = (6, Weapons.M117___750lb_GP_Bomb_LD)
        Mk_84___2000lb_GP_Bomb_LD = (6, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        Fuel_Tank_300_gallons_ = (6, Weapons.Fuel_Tank_300_gallons_)
        Fuel_Tank_300_gallons__EMPTY__ = (6, Weapons.Fuel_Tank_300_gallons__EMPTY__)
        Fuel_Tank_150_gallons = (6, Weapons.Fuel_Tank_150_gallons)
        Fuel_Tank_150_gallons__EMPTY_ = (6, Weapons.Fuel_Tank_150_gallons__EMPTY_)

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


# vwv_crusador_np not found in DCS ME


@planemod
class vwv_mig17f(PlaneType):
    id = "vwv_mig17f"
    flyable = True
    height = 3.8
    width = 9.628
    length = 11.09
    fuel_max = 1140
    max_speed = 1224
    chaff = 48
    flare = 48
    charge_total = 96
    chaff_charge_size = 1
    flare_charge_size = 1
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    livery_name = "VWV_MIG17F"  # from type

    class Pylon1:
        FAB_50 = (1, Weapons.FAB_50)
        FAB_250___250kg_GP_Bomb_LD = (1, Weapons.FAB_250___250kg_GP_Bomb_LD)
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
        FAB_250___250kg_GP_Bomb_LD = (2, Weapons.FAB_250___250kg_GP_Bomb_LD)
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
    height = 4.16
    width = 7.15
    length = 14.5
    fuel_max = 2600
    max_speed = 2448
    chaff = 0
    flare = 0
    charge_total = 0
    chaff_charge_size = 0
    flare_charge_size = 0
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    livery_name = "VWV_MIG21MF"  # from type

    class Pylon1:
        FAB_50 = (1, Weapons.FAB_50)
        FAB_250___250kg_GP_Bomb_LD = (1, Weapons.FAB_250___250kg_GP_Bomb_LD)
        B_8V20A_CM = (1, Weapons.B_8V20A_CM)
        B_8V20A_OM = (1, Weapons.B_8V20A_OM)
        B_8M1___20_S_8OFP2 = (1, Weapons.B_8M1___20_S_8OFP2)
        # ERRR B-8V20A - 20 S-8OFP2
        FAB_100M = (1, Weapons.FAB_100M)
        UPK_23_250___2_x_23mm__GSh_23L_Autocannon_Pod = (
            1,
            Weapons.UPK_23_250___2_x_23mm__GSh_23L_Autocannon_Pod,
        )
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
        FAB_250___250kg_GP_Bomb_LD = (2, Weapons.FAB_250___250kg_GP_Bomb_LD)
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
        FAB_50 = (3, Weapons.FAB_50)
        FAB_250___250kg_GP_Bomb_LD = (3, Weapons.FAB_250___250kg_GP_Bomb_LD)
        B_8V20A_CM = (3, Weapons.B_8V20A_CM)
        B_8V20A_OM = (3, Weapons.B_8V20A_OM)
        B_8M1___20_S_8OFP2 = (3, Weapons.B_8M1___20_S_8OFP2)
        # ERRR B-8V20A - 20 S-8OFP2
        FAB_100M = (3, Weapons.FAB_100M)
        UPK_23_250___2_x_23mm__GSh_23L_Autocannon_Pod = (
            3,
            Weapons.UPK_23_250___2_x_23mm__GSh_23L_Autocannon_Pod,
        )
        APU_13MT_with_R_13M__AA_2_Atoll_D____IR_AAM = (
            3,
            Weapons.APU_13MT_with_R_13M__AA_2_Atoll_D____IR_AAM,
        )
        APU_13U_2_with_R_3R__AA_2_Atoll_C____Semi_Active_AAM = (
            3,
            Weapons.APU_13U_2_with_R_3R__AA_2_Atoll_C____Semi_Active_AAM,
        )
        APU_13U_2_with_R_3S__AA_2_Atoll_B____IR_AAM = (
            3,
            Weapons.APU_13U_2_with_R_3S__AA_2_Atoll_B____IR_AAM,
        )
        RS2US___AAM__beam_rider = (3, Weapons.RS2US___AAM__beam_rider)

    class Pylon4:
        FAB_50 = (4, Weapons.FAB_50)
        FAB_250___250kg_GP_Bomb_LD = (4, Weapons.FAB_250___250kg_GP_Bomb_LD)
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

    pylons: Set[int] = {1, 2, 3, 4}

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
    height = 2.24
    width = 10.97
    length = 7.87
    fuel_max = 160
    max_speed = 648
    radio_frequency = 127.5

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

    tasks = [
        task.CAP,
        task.CAS,
        task.Escort,
        task.FighterSweep,
        task.GroundAttack,
        task.Intercept,
    ]
    task_default = task.CAS


## HELICOPTERS


@helicoptermod
class vwv_sh2f(HelicopterType):
    id = "vwv_sh2f"
    height = 4.893
    width = 16.4
    length = 18.654
    fuel_max = 1100
    max_speed = 295
    category = "Air"  # {828CEADE-3F1D-40aa-93CE-8CDB73FE2710}

    livery_name = "VWV_SH2F"  # from type

    class Pylon1:
        DIS_mk46torp = (1, Weapons.DIS_mk46torp)

    class Pylon4:
        DIS_mk46torp = (4, Weapons.DIS_mk46torp)

    # ERRR CABLE_MH6
    # ERRR suspended_soldier

    pylons: Set[int] = {1, 4, 5}

    tasks = [
        task.CAP,
        task.Escort,
        task.Intercept,
        task.FighterSweep,
        task.GroundAttack,
        task.CAS,
        task.AFAC,
        task.RunwayAttack,
        task.AntishipStrike,
    ]
    task_default = task.AntishipStrike


@helicoptermod
class vwv_hh2d(HelicopterType):
    id = "vwv_hh2d"
    height = 4.893
    width = 16.4
    length = 18.654
    fuel_max = 1100
    max_speed = 295
    category = "Air"  # {828CEADE-3F1D-40aa-93CE-8CDB73FE2710}
    radio_frequency = 251

    livery_name = "VWV_HH2D"  # from type

    class Pylon1:
        Fuel_Tank_150_gallons = (1, Weapons.Fuel_Tank_150_gallons)
        _108_US_gal__Paper_Fuel_Tank = (1, Weapons._108_US_gal__Paper_Fuel_Tank)

    class Pylon4:
        Fuel_Tank_150_gallons = (4, Weapons.Fuel_Tank_150_gallons)
        _108_US_gal__Paper_Fuel_Tank = (4, Weapons._108_US_gal__Paper_Fuel_Tank)

    class Pylon5:
        ab_212_cable = (5, Weapons.ab_212_cable)
        rescue_crew_sling = (5, Weapons.rescue_crew_sling)
        uscg_stretcher = (5, Weapons.uscg_stretcher)

    pylons: Set[int] = {1, 4, 5}

    tasks = [task.Escort, task.GroundAttack, task.CAS, task.AFAC, task.AntishipStrike]
    task_default = task.AntishipStrike


## HUTS skipped
