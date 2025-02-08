# Requires Russian Military Assets for DCS by Currenthill:
# https://www.currenthill.com/russia
#


from typing import Set, Dict, Any

from dcs import unittype, task
from dcs.helicopters import HelicopterType
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

from game.modsupport import (
    fortificationmod,
    helicoptermod,
    planemod,
    shipmod,
    cargomod,
    vehiclemod,
)
from pydcs_extensions.weapon_injector import inject_weapons


# Weapons
class WeaponsRU:

    Kh_555_ALCM = {"clsid": "{CH_Kh555}", "name": "Kh-555 ALCM", "weight": 1280}

    _6_x_Kh_555_ALCM = {
        "clsid": "{CH_Kh555x6}",
        "name": "6 x Kh-555 ALCM",
        "weight": 7680,
    }

    _6_x_9M120_Ataka__AT_9_Spiral_2____ATGM__SACLOS__Tandem_HEAT = {
        "clsid": "{Ka52_9M120_6}",
        "name": "6 x 9M120 Ataka (AT-9 Spiral-2) - ATGM, SACLOS, Tandem HEAT",
        "weight": 118,
    }

    _6_x_9M120F_Ataka__AT_9_Spiral_2____AGM__SACLOS__HE = {
        "clsid": "{Ka52_9M120F_6}",
        "name": "6 x 9M120F Ataka (AT-9 Spiral-2) - AGM, SACLOS, HE",
        "weight": 118,
    }

    Kh_101_ALCM = {"clsid": "{Tu95MSM_Kh101}", "name": "Kh-101 ALCM", "weight": 2400}

    Kh_101_ALCM_ = {"clsid": "{Tu160M2_Kh101}", "name": "Kh-101 ALCM", "weight": 2400}

    _6_x_Kh_101_ALCM = {
        "clsid": "{Tu160M2_Kh101x6}",
        "name": "6 x Kh-101 ALCM",
        "weight": 14400,
    }

    _6_x_Kh_555_ALCM = {
        "clsid": "{CH_Kh555x6}",
        "name": "6 x Kh-555 ALCM",
        "weight": 7680,
    }

    Kh_31A = {"clsid": "{Ka52_Kh31A}", "name": "Kh-31A", "weight": 610}

    Kh_35U = {"clsid": "{Ka52_Kh35U}", "name": "Kh-35U", "weight": 550}

    Kh_38MA = {"clsid": "{Ka52_Kh38MA}", "name": "Kh-38MA", "weight": 50}

    _9M120 = {"clsid": "{Ka52_9M120}", "name": "9M120", "weight": None}

    _9M120F = {"clsid": "{Ka52_9M120F}", "name": "9M120F", "weight": None}


inject_weapons(WeaponsRU)


# Artillery
@vehiclemod
class CH_2S35(unittype.VehicleType):
    id = "CH_2S35"
    name = "[CH] 2S35 SPG"
    detection_range = 5000
    threat_range = 40000
    air_weapon_dist = 1800
    eplrs = True


@vehiclemod
class CH_TOS1A(unittype.VehicleType):
    id = "CH_TOS1A"
    name = "[CH] TOS-1A MRL"
    detection_range = 0
    threat_range = 6000
    air_weapon_dist = 6000
    eplrs = True


# Infantry
@vehiclemod
class CH_DSHK_HMG_RUS(unittype.VehicleType):
    id = "CH_DSHK_HMG_RUS"
    name = "[CH] DShK HMG"
    detection_range = 5000
    threat_range = 1800
    air_weapon_dist = 1800
    eplrs = True


@vehiclemod
class CH_DSHK_HMG_UKR(unittype.VehicleType):
    id = "CH_DSHK_HMG_UKR"
    name = "[CH] DShK HMG"
    detection_range = 5000
    threat_range = 1800
    air_weapon_dist = 1800
    eplrs = True


@vehiclemod
class CH_9M133(unittype.VehicleType):
    id = "CH_9M133"
    name = "[CH] 9M133 ATGM Soldier"
    detection_range = 5500
    threat_range = 5500
    air_weapon_dist = 5500
    eplrs = True


@vehiclemod
class CH_RussianInfantry_Kord(unittype.VehicleType):
    id = "CH_RussianInfantry_Kord"
    name = "[CH] Kord HMG Soldier"
    detection_range = 0
    threat_range = 1800
    air_weapon_dist = 1800
    eplrs = True


# Air Defense
@vehiclemod
class CH_2S38_LG(unittype.VehicleType):
    id = "CH_2S38_LG"
    name = "[CH] 2S38 SPAAG (LG-HE)"
    detection_range = 12000
    threat_range = 8000
    air_weapon_dist = 8000
    eplrs = True


@vehiclemod
class CH_2S38(unittype.VehicleType):
    id = "CH_2S38"
    name = "[CH] 2S38 SPAAG"
    detection_range = 12000
    threat_range = 5000
    air_weapon_dist = 5000
    eplrs = True


@vehiclemod
class PantsirS1(unittype.VehicleType):
    id = "PantsirS1"
    name = "[CH] Pantsir-S1 SPAAGM"
    detection_range = 36000
    threat_range = 20000
    air_weapon_dist = 20000
    eplrs = True


@vehiclemod
class PantsirS2(unittype.VehicleType):
    id = "PantsirS2"
    name = "[CH] Pantsir-S2 SPAAGM"
    detection_range = 40000
    threat_range = 30000
    air_weapon_dist = 30000
    eplrs = True


@vehiclemod
class CH_S350_50P6_9M96D(unittype.VehicleType):
    id = "CH_S350_50P6_9M96D"
    name = "[CH] S-350 50P6 9M96D LN"
    detection_range = 0
    threat_range = 150000
    air_weapon_dist = 150000
    eplrs = True


@vehiclemod
class CH_S350_50P6_9M100(unittype.VehicleType):
    id = "CH_S350_50P6_9M100"
    name = "[CH] S-350 50P6 9M100 LN"
    detection_range = 0
    threat_range = 15000
    air_weapon_dist = 15000
    eplrs = True


@vehiclemod
class CH_S350_50N6(unittype.VehicleType):
    id = "CH_S350_50N6"
    name = "[CH] S-350 50N6 STR"
    detection_range = 200000
    threat_range = 0
    air_weapon_dist = 0
    eplrs = True


@vehiclemod
class CH_S350_50K6(unittype.VehicleType):
    id = "CH_S350_50K6"
    name = "[CH] S-350 50K6 CP"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0
    eplrs = True


@vehiclemod
class CH_S350_96L6(unittype.VehicleType):
    id = "CH_S350_96L6"
    name = "[CH] S-350 96L6 SR"
    detection_range = 300000
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class TorM2K(unittype.VehicleType):
    id = "TorM2K"
    name = "[CH] Tor M2K SHORAD"
    detection_range = 25000
    threat_range = 12000
    air_weapon_dist = 12000
    eplrs = True


@vehiclemod
class TorM2(unittype.VehicleType):
    id = "TorM2"
    name = "[CH] Tor M2 SHORAD"
    detection_range = 25000
    threat_range = 12000
    air_weapon_dist = 12000
    eplrs = True


@vehiclemod
class TorM2M(unittype.VehicleType):
    id = "TorM2M"
    name = "[CH] Tor M2M SHORAD"
    detection_range = 25000
    threat_range = 16000
    air_weapon_dist = 16000
    eplrs = True


@vehiclemod
class CH_BukM3_9A317M(unittype.VehicleType):
    id = "CH_BukM3_9A317M"
    name = "[CH] Buk M3 9A317M TELAR"
    detection_range = 120000
    threat_range = 70000
    air_weapon_dist = 70000


@vehiclemod
class CH_BukM3_9A317MA(unittype.VehicleType):
    id = "CH_BukM3_9A317MA"
    name = "[CH] Buk M3 9A317MA TELAR"
    detection_range = 120000
    threat_range = 70000
    air_weapon_dist = 70000


@vehiclemod
class CH_BukM3_9S36M(unittype.VehicleType):
    id = "CH_BukM3_9S36M"
    name = "[CH] Buk M3 9S36M TR"
    detection_range = 120000
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class CH_BukM3_9S510M(unittype.VehicleType):
    id = "CH_BukM3_9S510M"
    name = "[CH] Buk M3 9S510M CP"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0
    eplrs = True


@vehiclemod
class CH_BukM3_9S18M13(unittype.VehicleType):
    id = "CH_BukM3_9S18M13"
    name = "[CH] Buk M3 9S18M1-3 SR"
    detection_range = 150000
    threat_range = 0
    air_weapon_dist = 0


# Fortification
@fortificationmod
class CH_TM62_AT_Mine(unittype.VehicleType):
    id = "CH_TM62_AT_Mine"
    name = "[CH] TM-62M AT mine"
    detection_range = 0
    threat_range = 50
    air_weapon_dist = 50


# Armor
@vehiclemod
class CH_T14(unittype.VehicleType):
    id = "CH_T14"
    name = "[CH] T-14 MBT"
    detection_range = 8000
    threat_range = 5000
    air_weapon_dist = 5000
    eplrs = True


@vehiclemod
class CH_T90M(unittype.VehicleType):
    id = "CH_T90M"
    name = "[CH] T-90M MBT"
    detection_range = 8000
    threat_range = 5000
    air_weapon_dist = 5000
    eplrs = True


@vehiclemod
class CH_TigrM(unittype.VehicleType):
    id = "CH_TigrM"
    name = "[CH] Tigr-M"
    detection_range = 0
    threat_range = 1200
    air_weapon_dist = 1200
    eplrs = True


@vehiclemod
class CH_T90A(unittype.VehicleType):
    id = "CH_T90A"
    name = "[CH] T-90A MBT"
    detection_range = 0
    threat_range = 8000
    air_weapon_dist = 1800
    eplrs = True


@vehiclemod
class CH_T80BVM(unittype.VehicleType):
    id = "CH_T80BVM"
    name = "[CH] T-80BVM MBT"
    detection_range = 0
    threat_range = 8000
    air_weapon_dist = 1800
    eplrs = True


@vehiclemod
class CH_BMD4(unittype.VehicleType):
    id = "CH_BMD4"
    name = "[CH] BMD-4 IFV"
    detection_range = 6000
    threat_range = 4000
    air_weapon_dist = 4000
    eplrs = True


# Missiles
@vehiclemod
class CH_3K60_BAL(unittype.VehicleType):
    id = "CH_3K60_BAL"
    name = "[CH] Bal LBASM TEL"
    detection_range = 260000
    threat_range = 260000
    air_weapon_dist = 260000
    eplrs = True


@vehiclemod
class K300P(unittype.VehicleType):
    id = "K300P"
    name = "[CH] Bastion-P LBASM TEL"
    detection_range = 400000
    threat_range = 400000
    air_weapon_dist = 400000
    eplrs = True


@vehiclemod
class MonolitB(unittype.VehicleType):
    id = "MonolitB"
    name = "[CH] Monolit-B LBASM STR"
    detection_range = 800000
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class CH_IskanderM(unittype.VehicleType):
    id = "CH_IskanderM"
    name = "[CH] Iskander-M SRBM"
    detection_range = 0
    threat_range = 500000
    air_weapon_dist = 500000
    eplrs = True


@vehiclemod
class CH_IskanderK(unittype.VehicleType):
    id = "CH_IskanderK"
    name = "[CH] Iskander-K GLCM"
    detection_range = 1500000
    threat_range = 1500000
    air_weapon_dist = 1500000
    eplrs = True


## SHIPS


@shipmod
class CH_Project22160(unittype.ShipType):
    id = "CH_Project22160"
    name = "[CH] Project 22160 Patrol Ship"
    plane_num = 0
    helicopter_num = 1
    parking = 1
    detection_range = 80000
    threat_range = 8000
    air_weapon_dist = 8000


@shipmod
class Admiral_Gorshkov(unittype.ShipType):
    id = "Admiral_Gorshkov"
    name = "[CH] Project 22350 Admiral Gorshkov Frigate"
    plane_num = 0
    helicopter_num = 1
    parking = 1
    detection_range = 150000
    threat_range = 150000
    air_weapon_dist = 150000


@shipmod
class CH_Grigorovich_AShM(unittype.ShipType):
    id = "CH_Grigorovich_AShM"
    name = "[CH] Project 11356R Admiral Grigorovich Frigate (AShM)"
    plane_num = 0
    helicopter_num = 1
    parking = 1
    detection_range = 300000
    threat_range = 70000
    air_weapon_dist = 70000


@shipmod
class CH_Grigorovich_LACM(unittype.ShipType):
    id = "CH_Grigorovich_LACM"
    name = "[CH] Project 11356R Admiral Grigorovich Frigate (LACM)"
    plane_num = 0
    helicopter_num = 1
    parking = 1
    detection_range = 300000
    threat_range = 70000
    air_weapon_dist = 70000


@shipmod
class Karakurt_AShM(unittype.ShipType):
    id = "Karakurt_AShM"
    name = "[CH] Project 22800 Karakurt Corvette AShM"
    plane_num = 0
    helicopter_num = 0
    parking = 0
    detection_range = 150000
    threat_range = 25000
    air_weapon_dist = 25000


@shipmod
class Karakurt_LACM(unittype.ShipType):
    id = "Karakurt_LACM"
    name = "[CH] Project 22800 Karakurt Corvette LACM"
    plane_num = 0
    helicopter_num = 0
    parking = 0
    detection_range = 150000
    threat_range = 25000
    air_weapon_dist = 25000


@shipmod
class CH_Steregushchiy(unittype.ShipType):
    id = "CH_Steregushchiy"
    name = "[CH] Project 20381 Steregushchiy Corvette"
    plane_num = 0
    helicopter_num = 1
    parking = 1
    detection_range = 150000
    threat_range = 150000
    air_weapon_dist = 150000


@shipmod
class CH_Gremyashchiy_AShM(unittype.ShipType):
    id = "CH_Gremyashchiy_AShM"
    name = "[CH] Project 20385 Gremyashchiy Corvette (AShM)"
    plane_num = 0
    helicopter_num = 1
    parking = 1
    detection_range = 300000
    threat_range = 150000
    air_weapon_dist = 150000


@shipmod
class CH_Gremyashchiy_LACM(unittype.ShipType):
    id = "CH_Gremyashchiy_LACM"
    name = "[CH] Project 20385 Gremyashchiy Corvette (LACM)"
    plane_num = 0
    helicopter_num = 1
    parking = 1
    detection_range = 300000
    threat_range = 150000
    air_weapon_dist = 150000


# Helicopters
@helicoptermod
class CH_Ka52K(HelicopterType):
    id = "CH_Ka52K"
    height = 5.6
    width = 14.4
    length = 15.84
    fuel_max = 1450
    max_speed = 350
    chaff = 32
    flare = 96
    charge_total = 128
    chaff_charge_size = 1
    flare_charge_size = 1
    radio_frequency = 124

    livery_name = "CH_KA52K"  # from type

    class Pylon1:
        B_8V20A_CM = (1, Weapons.B_8V20A_CM)
        B_8V20A_OFP2 = (1, Weapons.B_8V20A_OFP2)
        B_8V20A_OM = (1, Weapons.B_8V20A_OM)
        Kh_25ML__AS_10_Karen____300kg__ASM__Semi_Act_Laser_ = (
            1,
            Weapons.Kh_25ML__AS_10_Karen____300kg__ASM__Semi_Act_Laser_,
        )
        B_8V20A___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            1,
            Weapons.B_8V20A___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation = (
            1,
            Weapons.B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation,
        )
        UPK_23_250___2_x_23mm__GSh_23L_Autocannon_Pod = (
            1,
            Weapons.UPK_23_250___2_x_23mm__GSh_23L_Autocannon_Pod,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            1,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            1,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        FAB_250___250kg_GP_Bomb_LD = (1, Weapons.FAB_250___250kg_GP_Bomb_LD)
        FAB_250_M62___250_kg_GP_Bomb_LD = (1, Weapons.FAB_250_M62___250_kg_GP_Bomb_LD)
        FAB_500_M_62___500kg_GP_Bomb_LD = (1, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        Fuel_tank_PTB_450 = (1, Weapons.Fuel_tank_PTB_450)
        APU_6___6_x_9M127_Vikhr___ATGM__LOSBR__Tandem_HEAT_Frag = (
            1,
            Weapons.APU_6___6_x_9M127_Vikhr___ATGM__LOSBR__Tandem_HEAT_Frag,
        )
        _6_x_9M120_Ataka__AT_9_Spiral_2____ATGM__SACLOS__Tandem_HEAT = (
            1,
            Weapons._6_x_9M120_Ataka__AT_9_Spiral_2____ATGM__SACLOS__Tandem_HEAT,
        )
        _6_x_9M120F_Ataka__AT_9_Spiral_2____AGM__SACLOS__HE = (
            1,
            Weapons._6_x_9M120F_Ataka__AT_9_Spiral_2____AGM__SACLOS__HE,
        )

    class Pylon2:
        B_8V20A_CM = (2, Weapons.B_8V20A_CM)
        B_8V20A_OFP2 = (2, Weapons.B_8V20A_OFP2)
        B_8V20A_OM = (2, Weapons.B_8V20A_OM)
        Kh_25ML__AS_10_Karen____300kg__ASM__Semi_Act_Laser_ = (
            2,
            Weapons.Kh_25ML__AS_10_Karen____300kg__ASM__Semi_Act_Laser_,
        )
        B_8V20A___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            2,
            Weapons.B_8V20A___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation = (
            2,
            Weapons.B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation,
        )
        UPK_23_250___2_x_23mm__GSh_23L_Autocannon_Pod = (
            2,
            Weapons.UPK_23_250___2_x_23mm__GSh_23L_Autocannon_Pod,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            2,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            2,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        FAB_250___250kg_GP_Bomb_LD = (2, Weapons.FAB_250___250kg_GP_Bomb_LD)
        FAB_250_M62___250_kg_GP_Bomb_LD = (2, Weapons.FAB_250_M62___250_kg_GP_Bomb_LD)
        FAB_500_M_62___500kg_GP_Bomb_LD = (2, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        Fuel_tank_PTB_450 = (2, Weapons.Fuel_tank_PTB_450)
        APU_6___6_x_9M127_Vikhr___ATGM__LOSBR__Tandem_HEAT_Frag = (
            2,
            Weapons.APU_6___6_x_9M127_Vikhr___ATGM__LOSBR__Tandem_HEAT_Frag,
        )
        _6_x_9M120_Ataka__AT_9_Spiral_2____ATGM__SACLOS__Tandem_HEAT = (
            2,
            Weapons._6_x_9M120_Ataka__AT_9_Spiral_2____ATGM__SACLOS__Tandem_HEAT,
        )
        _6_x_9M120F_Ataka__AT_9_Spiral_2____AGM__SACLOS__HE = (
            2,
            Weapons._6_x_9M120F_Ataka__AT_9_Spiral_2____AGM__SACLOS__HE,
        )
        Kh_35U = (2, Weapons.Kh_35U)
        Kh_38MA = (2, Weapons.Kh_38MA)
        Kh_31A = (2, Weapons.Kh_31A)

    class Pylon3:
        B_8V20A_CM = (3, Weapons.B_8V20A_CM)
        B_8V20A_OFP2 = (3, Weapons.B_8V20A_OFP2)
        B_8V20A_OM = (3, Weapons.B_8V20A_OM)
        Kh_25ML__AS_10_Karen____300kg__ASM__Semi_Act_Laser_ = (
            3,
            Weapons.Kh_25ML__AS_10_Karen____300kg__ASM__Semi_Act_Laser_,
        )
        B_8V20A___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            3,
            Weapons.B_8V20A___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation = (
            3,
            Weapons.B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation,
        )
        UPK_23_250___2_x_23mm__GSh_23L_Autocannon_Pod = (
            3,
            Weapons.UPK_23_250___2_x_23mm__GSh_23L_Autocannon_Pod,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            3,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            3,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        FAB_250___250kg_GP_Bomb_LD = (3, Weapons.FAB_250___250kg_GP_Bomb_LD)
        FAB_250_M62___250_kg_GP_Bomb_LD = (3, Weapons.FAB_250_M62___250_kg_GP_Bomb_LD)
        FAB_500_M_62___500kg_GP_Bomb_LD = (3, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        Fuel_tank_PTB_450 = (3, Weapons.Fuel_tank_PTB_450)
        APU_6___6_x_9M127_Vikhr___ATGM__LOSBR__Tandem_HEAT_Frag = (
            3,
            Weapons.APU_6___6_x_9M127_Vikhr___ATGM__LOSBR__Tandem_HEAT_Frag,
        )
        _6_x_9M120_Ataka__AT_9_Spiral_2____ATGM__SACLOS__Tandem_HEAT = (
            3,
            Weapons._6_x_9M120_Ataka__AT_9_Spiral_2____ATGM__SACLOS__Tandem_HEAT,
        )
        _6_x_9M120F_Ataka__AT_9_Spiral_2____AGM__SACLOS__HE = (
            3,
            Weapons._6_x_9M120F_Ataka__AT_9_Spiral_2____AGM__SACLOS__HE,
        )
        Kh_35U = (3, Weapons.Kh_35U)
        Kh_38MA = (3, Weapons.Kh_38MA)
        Kh_31A = (3, Weapons.Kh_31A)

    class Pylon4:
        B_8V20A_CM = (4, Weapons.B_8V20A_CM)
        B_8V20A_OFP2 = (4, Weapons.B_8V20A_OFP2)
        B_8V20A_OM = (4, Weapons.B_8V20A_OM)
        Kh_25ML__AS_10_Karen____300kg__ASM__Semi_Act_Laser_ = (
            4,
            Weapons.Kh_25ML__AS_10_Karen____300kg__ASM__Semi_Act_Laser_,
        )
        B_8V20A___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            4,
            Weapons.B_8V20A___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation = (
            4,
            Weapons.B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation,
        )
        UPK_23_250___2_x_23mm__GSh_23L_Autocannon_Pod = (
            4,
            Weapons.UPK_23_250___2_x_23mm__GSh_23L_Autocannon_Pod,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            4,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            4,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        FAB_250___250kg_GP_Bomb_LD = (4, Weapons.FAB_250___250kg_GP_Bomb_LD)
        FAB_250_M62___250_kg_GP_Bomb_LD = (4, Weapons.FAB_250_M62___250_kg_GP_Bomb_LD)
        FAB_500_M_62___500kg_GP_Bomb_LD = (4, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        Fuel_tank_PTB_450 = (4, Weapons.Fuel_tank_PTB_450)
        APU_6___6_x_9M127_Vikhr___ATGM__LOSBR__Tandem_HEAT_Frag = (
            4,
            Weapons.APU_6___6_x_9M127_Vikhr___ATGM__LOSBR__Tandem_HEAT_Frag,
        )
        _6_x_9M120_Ataka__AT_9_Spiral_2____ATGM__SACLOS__Tandem_HEAT = (
            4,
            Weapons._6_x_9M120_Ataka__AT_9_Spiral_2____ATGM__SACLOS__Tandem_HEAT,
        )
        _6_x_9M120F_Ataka__AT_9_Spiral_2____AGM__SACLOS__HE = (
            4,
            Weapons._6_x_9M120F_Ataka__AT_9_Spiral_2____AGM__SACLOS__HE,
        )

    pylons: Set[int] = {1, 2, 3, 4}

    tasks = [
        task.CAS,
        task.GroundAttack,
        task.Escort,
        task.AFAC,
        task.AntishipStrike,
        task.Transport,
        task.Reconnaissance,
    ]
    task_default = task.AntishipStrike


@helicoptermod
class CH_Ka52(HelicopterType):
    id = "CH_Ka52"
    height = 5.6
    width = 14.4
    length = 15.84
    fuel_max = 1450
    max_speed = 350
    chaff = 32
    flare = 96
    charge_total = 128
    chaff_charge_size = 1
    flare_charge_size = 1
    radio_frequency = 124

    livery_name = "CH_KA52"  # from type

    class Pylon1:
        B_8V20A_CM = (1, Weapons.B_8V20A_CM)
        B_8V20A_OFP2 = (1, Weapons.B_8V20A_OFP2)
        B_8V20A_OM = (1, Weapons.B_8V20A_OM)
        Kh_25ML__AS_10_Karen____300kg__ASM__Semi_Act_Laser_ = (
            1,
            Weapons.Kh_25ML__AS_10_Karen____300kg__ASM__Semi_Act_Laser_,
        )
        B_8V20A___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            1,
            Weapons.B_8V20A___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation = (
            1,
            Weapons.B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation,
        )
        UPK_23_250___2_x_23mm__GSh_23L_Autocannon_Pod = (
            1,
            Weapons.UPK_23_250___2_x_23mm__GSh_23L_Autocannon_Pod,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            1,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            1,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        FAB_250___250kg_GP_Bomb_LD = (1, Weapons.FAB_250___250kg_GP_Bomb_LD)
        FAB_250_M62___250_kg_GP_Bomb_LD = (1, Weapons.FAB_250_M62___250_kg_GP_Bomb_LD)
        FAB_500_M_62___500kg_GP_Bomb_LD = (1, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        Fuel_tank_PTB_450 = (1, Weapons.Fuel_tank_PTB_450)
        APU_6___6_x_9M127_Vikhr___ATGM__LOSBR__Tandem_HEAT_Frag = (
            1,
            Weapons.APU_6___6_x_9M127_Vikhr___ATGM__LOSBR__Tandem_HEAT_Frag,
        )
        _6_x_9M120_Ataka__AT_9_Spiral_2____ATGM__SACLOS__Tandem_HEAT = (
            1,
            Weapons._6_x_9M120_Ataka__AT_9_Spiral_2____ATGM__SACLOS__Tandem_HEAT,
        )
        _6_x_9M120F_Ataka__AT_9_Spiral_2____AGM__SACLOS__HE = (
            1,
            Weapons._6_x_9M120F_Ataka__AT_9_Spiral_2____AGM__SACLOS__HE,
        )

    class Pylon2:
        B_8V20A_CM = (2, Weapons.B_8V20A_CM)
        B_8V20A_OFP2 = (2, Weapons.B_8V20A_OFP2)
        B_8V20A_OM = (2, Weapons.B_8V20A_OM)
        B_8V20A___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            2,
            Weapons.B_8V20A___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation = (
            2,
            Weapons.B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation,
        )
        UPK_23_250___2_x_23mm__GSh_23L_Autocannon_Pod = (
            2,
            Weapons.UPK_23_250___2_x_23mm__GSh_23L_Autocannon_Pod,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            2,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            2,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        FAB_250___250kg_GP_Bomb_LD = (2, Weapons.FAB_250___250kg_GP_Bomb_LD)
        FAB_250_M62___250_kg_GP_Bomb_LD = (2, Weapons.FAB_250_M62___250_kg_GP_Bomb_LD)
        FAB_500_M_62___500kg_GP_Bomb_LD = (2, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        Fuel_tank_PTB_450 = (2, Weapons.Fuel_tank_PTB_450)

    class Pylon3:
        B_8V20A_CM = (3, Weapons.B_8V20A_CM)
        B_8V20A_OFP2 = (3, Weapons.B_8V20A_OFP2)
        B_8V20A_OM = (3, Weapons.B_8V20A_OM)
        B_8V20A___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            3,
            Weapons.B_8V20A___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation = (
            3,
            Weapons.B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation,
        )
        UPK_23_250___2_x_23mm__GSh_23L_Autocannon_Pod = (
            3,
            Weapons.UPK_23_250___2_x_23mm__GSh_23L_Autocannon_Pod,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            3,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            3,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        FAB_250___250kg_GP_Bomb_LD = (3, Weapons.FAB_250___250kg_GP_Bomb_LD)
        FAB_250_M62___250_kg_GP_Bomb_LD = (3, Weapons.FAB_250_M62___250_kg_GP_Bomb_LD)
        FAB_500_M_62___500kg_GP_Bomb_LD = (3, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        Fuel_tank_PTB_450 = (3, Weapons.Fuel_tank_PTB_450)

    class Pylon4:
        B_8V20A_CM = (4, Weapons.B_8V20A_CM)
        B_8V20A_OFP2 = (4, Weapons.B_8V20A_OFP2)
        B_8V20A_OM = (4, Weapons.B_8V20A_OM)
        Kh_25ML__AS_10_Karen____300kg__ASM__Semi_Act_Laser_ = (
            4,
            Weapons.Kh_25ML__AS_10_Karen____300kg__ASM__Semi_Act_Laser_,
        )
        B_8V20A___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            4,
            Weapons.B_8V20A___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation = (
            4,
            Weapons.B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation,
        )
        UPK_23_250___2_x_23mm__GSh_23L_Autocannon_Pod = (
            4,
            Weapons.UPK_23_250___2_x_23mm__GSh_23L_Autocannon_Pod,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            4,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            4,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        FAB_250___250kg_GP_Bomb_LD = (4, Weapons.FAB_250___250kg_GP_Bomb_LD)
        FAB_250_M62___250_kg_GP_Bomb_LD = (4, Weapons.FAB_250_M62___250_kg_GP_Bomb_LD)
        FAB_500_M_62___500kg_GP_Bomb_LD = (4, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        Fuel_tank_PTB_450 = (4, Weapons.Fuel_tank_PTB_450)
        APU_6___6_x_9M127_Vikhr___ATGM__LOSBR__Tandem_HEAT_Frag = (
            4,
            Weapons.APU_6___6_x_9M127_Vikhr___ATGM__LOSBR__Tandem_HEAT_Frag,
        )
        _6_x_9M120_Ataka__AT_9_Spiral_2____ATGM__SACLOS__Tandem_HEAT = (
            4,
            Weapons._6_x_9M120_Ataka__AT_9_Spiral_2____ATGM__SACLOS__Tandem_HEAT,
        )
        _6_x_9M120F_Ataka__AT_9_Spiral_2____AGM__SACLOS__HE = (
            4,
            Weapons._6_x_9M120F_Ataka__AT_9_Spiral_2____AGM__SACLOS__HE,
        )

    class Pylon5:
        _9S846_Strelets___2_x_9M39_Igla = (5, Weapons._9S846_Strelets___2_x_9M39_Igla)

    # ERRR <CLEAN>

    class Pylon6:
        _9S846_Strelets___2_x_9M39_Igla = (6, Weapons._9S846_Strelets___2_x_9M39_Igla)

    # ERRR <CLEAN>

    pylons: Set[int] = {1, 2, 3, 4, 5, 6}

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
class CH_Mi28N(HelicopterType):
    id = "CH_Mi28N"
    height = 5.087
    width = 17.2
    length = 17.87
    fuel_max = 1500
    max_speed = 365
    chaff = 0
    flare = 128
    charge_total = 128
    chaff_charge_size = 0
    flare_charge_size = 1
    eplrs = True
    radio_frequency = 124

    livery_name = "CH_MI28N"  # from type

    class Pylon1:
        B_8V20A_CM = (1, Weapons.B_8V20A_CM)
        B_8V20A_OFP2 = (1, Weapons.B_8V20A_OFP2)
        B_8V20A_OM = (1, Weapons.B_8V20A_OM)
        B_8V20A___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            1,
            Weapons.B_8V20A___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation = (
            1,
            Weapons.B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            1,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            1,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        FAB_250___250kg_GP_Bomb_LD = (1, Weapons.FAB_250___250kg_GP_Bomb_LD)
        FAB_250_M62___250_kg_GP_Bomb_LD = (1, Weapons.FAB_250_M62___250_kg_GP_Bomb_LD)
        FAB_500_M_62___500kg_GP_Bomb_LD = (1, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        Fuel_tank_PTB_450 = (1, Weapons.Fuel_tank_PTB_450)
        _6_x_9M120_Ataka__AT_9_Spiral_2____ATGM__SACLOS__Tandem_HEAT = (
            1,
            Weapons._6_x_9M120_Ataka__AT_9_Spiral_2____ATGM__SACLOS__Tandem_HEAT,
        )
        _6_x_9M120F_Ataka__AT_9_Spiral_2____AGM__SACLOS__HE = (
            1,
            Weapons._6_x_9M120F_Ataka__AT_9_Spiral_2____AGM__SACLOS__HE,
        )
        _9S846_Strelets___2_x_9M39_Igla = (1, Weapons._9S846_Strelets___2_x_9M39_Igla)

    class Pylon2:
        B_8V20A_CM = (2, Weapons.B_8V20A_CM)
        B_8V20A_OFP2 = (2, Weapons.B_8V20A_OFP2)
        B_8V20A_OM = (2, Weapons.B_8V20A_OM)
        B_8V20A___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            2,
            Weapons.B_8V20A___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation = (
            2,
            Weapons.B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation,
        )
        UPK_23_250___2_x_23mm__GSh_23L_Autocannon_Pod = (
            2,
            Weapons.UPK_23_250___2_x_23mm__GSh_23L_Autocannon_Pod,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            2,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            2,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        FAB_250___250kg_GP_Bomb_LD = (2, Weapons.FAB_250___250kg_GP_Bomb_LD)
        FAB_250_M62___250_kg_GP_Bomb_LD = (2, Weapons.FAB_250_M62___250_kg_GP_Bomb_LD)
        FAB_500_M_62___500kg_GP_Bomb_LD = (2, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        Fuel_tank_PTB_450 = (2, Weapons.Fuel_tank_PTB_450)
        _6_x_9M120_Ataka__AT_9_Spiral_2____ATGM__SACLOS__Tandem_HEAT = (
            2,
            Weapons._6_x_9M120_Ataka__AT_9_Spiral_2____ATGM__SACLOS__Tandem_HEAT,
        )
        _6_x_9M120F_Ataka__AT_9_Spiral_2____AGM__SACLOS__HE = (
            2,
            Weapons._6_x_9M120F_Ataka__AT_9_Spiral_2____AGM__SACLOS__HE,
        )
        _9S846_Strelets___2_x_9M39_Igla = (2, Weapons._9S846_Strelets___2_x_9M39_Igla)

    class Pylon3:
        B_8V20A_CM = (3, Weapons.B_8V20A_CM)
        B_8V20A_OFP2 = (3, Weapons.B_8V20A_OFP2)
        B_8V20A_OM = (3, Weapons.B_8V20A_OM)
        B_8V20A___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            3,
            Weapons.B_8V20A___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation = (
            3,
            Weapons.B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation,
        )
        UPK_23_250___2_x_23mm__GSh_23L_Autocannon_Pod = (
            3,
            Weapons.UPK_23_250___2_x_23mm__GSh_23L_Autocannon_Pod,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            3,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            3,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        FAB_250___250kg_GP_Bomb_LD = (3, Weapons.FAB_250___250kg_GP_Bomb_LD)
        FAB_250_M62___250_kg_GP_Bomb_LD = (3, Weapons.FAB_250_M62___250_kg_GP_Bomb_LD)
        FAB_500_M_62___500kg_GP_Bomb_LD = (3, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        Fuel_tank_PTB_450 = (3, Weapons.Fuel_tank_PTB_450)
        _6_x_9M120_Ataka__AT_9_Spiral_2____ATGM__SACLOS__Tandem_HEAT = (
            3,
            Weapons._6_x_9M120_Ataka__AT_9_Spiral_2____ATGM__SACLOS__Tandem_HEAT,
        )
        _6_x_9M120F_Ataka__AT_9_Spiral_2____AGM__SACLOS__HE = (
            3,
            Weapons._6_x_9M120F_Ataka__AT_9_Spiral_2____AGM__SACLOS__HE,
        )
        _9S846_Strelets___2_x_9M39_Igla = (3, Weapons._9S846_Strelets___2_x_9M39_Igla)

    class Pylon4:
        B_8V20A_CM = (4, Weapons.B_8V20A_CM)
        B_8V20A_OFP2 = (4, Weapons.B_8V20A_OFP2)
        B_8V20A_OM = (4, Weapons.B_8V20A_OM)
        B_8V20A___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            4,
            Weapons.B_8V20A___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation = (
            4,
            Weapons.B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            4,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            4,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        FAB_250___250kg_GP_Bomb_LD = (4, Weapons.FAB_250___250kg_GP_Bomb_LD)
        FAB_250_M62___250_kg_GP_Bomb_LD = (4, Weapons.FAB_250_M62___250_kg_GP_Bomb_LD)
        FAB_500_M_62___500kg_GP_Bomb_LD = (4, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        Fuel_tank_PTB_450 = (4, Weapons.Fuel_tank_PTB_450)
        _6_x_9M120_Ataka__AT_9_Spiral_2____ATGM__SACLOS__Tandem_HEAT = (
            4,
            Weapons._6_x_9M120_Ataka__AT_9_Spiral_2____ATGM__SACLOS__Tandem_HEAT,
        )
        _6_x_9M120F_Ataka__AT_9_Spiral_2____AGM__SACLOS__HE = (
            4,
            Weapons._6_x_9M120F_Ataka__AT_9_Spiral_2____AGM__SACLOS__HE,
        )
        _9S846_Strelets___2_x_9M39_Igla = (4, Weapons._9S846_Strelets___2_x_9M39_Igla)

    pylons: Set[int] = {1, 2, 3, 4}

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


# Planes
@planemod
class CH_Tu_95MSM(PlaneType):
    id = "CH_Tu-95MSM"
    large_parking_slot = True
    height = 13.3
    width = 50.04
    length = 49.13
    fuel_max = 87000
    max_speed = 919.8
    chaff = 48
    flare = 48
    charge_total = 96
    chaff_charge_size = 1
    flare_charge_size = 1
    eplrs = True

    property_defaults: Dict[str, Any] = {}

    livery_name = "CH_TU-95MSM"  # from type

    class Pylon1:
        Kh_101_ALCM = (1, Weapons.Kh_101_ALCM)
        Kh_555_ALCM = (1, Weapons.Kh_555_ALCM)

    # ERRR <CLEAN>

    class Pylon2:
        Kh_101_ALCM = (2, Weapons.Kh_101_ALCM)
        Kh_555_ALCM = (2, Weapons.Kh_555_ALCM)

    class Pylon3:
        Kh_101_ALCM = (3, Weapons.Kh_101_ALCM)
        Kh_555_ALCM = (3, Weapons.Kh_555_ALCM)

    # ERRR <CLEAN>

    class Pylon4:
        Kh_101_ALCM = (4, Weapons.Kh_101_ALCM)
        Kh_555_ALCM = (4, Weapons.Kh_555_ALCM)

    class Pylon5:
        Kh_101_ALCM = (5, Weapons.Kh_101_ALCM)
        Kh_555_ALCM = (5, Weapons.Kh_555_ALCM)

    # ERRR <CLEAN>

    class Pylon6:
        Kh_101_ALCM = (6, Weapons.Kh_101_ALCM)
        Kh_555_ALCM = (6, Weapons.Kh_555_ALCM)

    class Pylon7:
        Kh_101_ALCM = (7, Weapons.Kh_101_ALCM)
        Kh_555_ALCM = (7, Weapons.Kh_555_ALCM)

    # ERRR <CLEAN>

    class Pylon8:
        Kh_101_ALCM = (8, Weapons.Kh_101_ALCM)
        Kh_555_ALCM = (8, Weapons.Kh_555_ALCM)

    class Pylon9:
        _6_x_Kh_555_ALCM = (9, Weapons._6_x_Kh_555_ALCM)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9}

    tasks = [
        task.Reconnaissance,
        task.GroundAttack,
        task.CAS,
        task.AFAC,
        task.RunwayAttack,
        task.AntishipStrike,
        task.PinpointStrike,
        task.SEAD,
    ]
    task_default = task.GroundAttack


@planemod
class CH_Tu_160M2(PlaneType):
    id = "CH_Tu-160M2"
    large_parking_slot = True
    height = 13.25
    width = 55.7
    length = 54.1
    fuel_max = 148000
    max_speed = 2199.6
    chaff = 72
    flare = 72
    charge_total = 144
    chaff_charge_size = 1
    flare_charge_size = 1
    eplrs = True

    property_defaults: Dict[str, Any] = {}

    livery_name = "CH_TU-160M2"  # from type

    class Pylon1:
        _6_x_Kh_101_ALCM = (1, Weapons._6_x_Kh_101_ALCM)
        _6_x_Kh_555_ALCM = (1, Weapons._6_x_Kh_555_ALCM)

    class Pylon2:
        _6_x_Kh_101_ALCM = (2, Weapons._6_x_Kh_101_ALCM)
        _6_x_Kh_555_ALCM = (2, Weapons._6_x_Kh_555_ALCM)

    pylons: Set[int] = {1, 2}

    tasks = [
        task.Reconnaissance,
        task.GroundAttack,
        task.CAS,
        task.AFAC,
        task.RunwayAttack,
        task.AntishipStrike,
        task.PinpointStrike,
        task.SEAD,
    ]
    task_default = task.GroundAttack


# Cargo
@cargomod
class BMD4_cargo(unittype.StaticType):
    id = "BMD4_cargo"
    name = "[CH] BMD-4 IFV"
    shape_name = "CH_BMD-4"
    category = "Cargos"
    rate = 100
    can_cargo = True
