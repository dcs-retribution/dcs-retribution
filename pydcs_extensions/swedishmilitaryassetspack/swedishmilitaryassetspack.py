# Requires Swedish Military Assets for DCS by Currenthill:
# https://forum.dcs.world/topic/295202-swedish-military-assets-for-dcs-by-currenthill/
#

from typing import Set

from dcs import unittype, task
from dcs.helicopters import HelicopterType
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

from game.modsupport import (
    helicoptermod,
    planemod,
    shipmod,
    vehiclemod,
)
from pydcs_extensions.weapon_injector import inject_weapons


class WeaponsSW:

    IRIS_T_IR_AAM = {"clsid": "{CH_IRIS-T}", "name": "IRIS-T IR AAM", "weight": 88.4}

    Meteor_AMRAAM___Active_Radar_AAM = {
        "clsid": "{CH_Meteor}",
        "name": "Meteor AMRAAM - Active Radar AAM",
        "weight": 190,
    }

    Meteor_AMRAAM___Active_Radar_AAM_x_2 = {
        "clsid": "{CH_Meteor_DUAL}",
        "name": "Meteor AMRAAM - Active Radar AAM x 2",
        "weight": 380,
    }

    AIM_120C_8_AMRAAM___Active_Radar_AAM = {
        "clsid": "{CH_AIM-120C8}",
        "name": "AIM-120C-8 AMRAAM - Active Radar AAM",
        "weight": 161,
    }

    AIM_120C_8_AMRAAM___Active_Radar_AAM_x_2 = {
        "clsid": "{CH_AIM-120C8_DUAL}",
        "name": "AIM-120C-8 AMRAAM - Active Radar AAM x 2",
        "weight": 322,
    }

    GBU_49___500lb_Laser__GPS_Guided_Bomb_LD = {
        "clsid": "{CH_GBU49}",
        "name": "GBU-49 - 500lb Laser & GPS Guided Bomb LD",
        "weight": 253,
    }

    GBU_39_SDB_285_lb_Guided_Glide_Bomb = {
        "clsid": "{CH_GBU39}",
        "name": "GBU-39 SDB 285 lb Guided Glide-Bomb",
        "weight": 129,
    }

    Taurus_KEPD_350_ALCM = {
        "clsid": "{CH_KEPD350}",
        "name": "Taurus KEPD-350 ALCM",
        "weight": 1400,
    }

    Drop_tank_1100_litres = {
        "clsid": "{CH_JAS39C_Tank1100}",
        "name": "Drop tank 1100 litres",
        "weight": 946.06,
    }

    RBS_15_Mk4 = {"clsid": "{CH_RBS15MK4}", "name": "RBS-15 Mk4", "weight": 650}


inject_weapons(WeaponsSW)


## ARTILLERY
@vehiclemod
class Grkpbv90(unittype.VehicleType):
    id = "Grkpbv90"
    name = "[CH] Grkpbv 90 SPM"
    detection_range = 0
    threat_range = 7500
    air_weapon_dist = 7500
    eplrs = True


@vehiclemod
class Artillerisystem08_SGR77B(unittype.VehicleType):
    id = "Artillerisystem08_SGR77B"
    name = "[CH] Archer SPG SGR77B"
    detection_range = 10000
    threat_range = 40000
    air_weapon_dist = 40000
    eplrs = True


@vehiclemod
class Artillerisystem08_M982(unittype.VehicleType):
    id = "Artillerisystem08_M982"
    name = "[CH] Archer SPG M982 Excalibur"
    detection_range = 0
    threat_range = 50000
    air_weapon_dist = 50000
    eplrs = True


# Air Defense
@vehiclemod
class LvKv9040(unittype.VehicleType):
    id = "LvKv9040"
    name = "[CH] Lvkv 9040B SPAAG"
    detection_range = 15000
    threat_range = 4000
    air_weapon_dist = 4000
    eplrs = True


@vehiclemod
class LvS_103_Lavett103_Rb103A(unittype.VehicleType):
    id = "LvS-103_Lavett103_Rb103A"
    name = "[CH] LvS-103 Lavett 103 Rb103A LN"
    detection_range = 0
    threat_range = 160000
    air_weapon_dist = 160000
    eplrs = True


@vehiclemod
class LvS_103_Lavett103_Rb103B(unittype.VehicleType):
    id = "LvS-103_Lavett103_Rb103B"
    name = "[CH] LvS-103 Lavett 103 Rb103B LN"
    detection_range = 0
    threat_range = 120000
    air_weapon_dist = 120000
    eplrs = True


@vehiclemod
class LvS_103_Lavett103_HX_Rb103A(unittype.VehicleType):
    id = "LvS-103_Lavett103_HX_Rb103A"
    name = "[CH] LvS-103 Lavett 103 Rb103A LN (HX)"
    detection_range = 0
    threat_range = 160000
    air_weapon_dist = 160000
    eplrs = True


@vehiclemod
class LvS_103_Lavett103_HX_Rb103B(unittype.VehicleType):
    id = "LvS-103_Lavett103_HX_Rb103B"
    name = "[CH] LvS-103 Lavett 103 Rb103B LN (HX)"
    detection_range = 0
    threat_range = 120000
    air_weapon_dist = 120000
    eplrs = True


@vehiclemod
class LvS_103_StriE103(unittype.VehicleType):
    id = "LvS-103_StriE103"
    name = "[CH] LvS-103 StriE 103 ECS (HX)"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0
    eplrs = True


@vehiclemod
class LvS_103_PM103(unittype.VehicleType):
    id = "LvS-103_PM103"
    name = "[CH] LvS-103 PM 103 STR"
    detection_range = 200000
    threat_range = 0
    air_weapon_dist = 0
    eplrs = True


@vehiclemod
class LvS_103_PM103_HX(unittype.VehicleType):
    id = "LvS-103_PM103_HX"
    name = "[CH] LvS-103 PM 103 STR (HX)"
    detection_range = 200000
    threat_range = 0
    air_weapon_dist = 0
    eplrs = True


@vehiclemod
class LvS_103_Elverk103(unittype.VehicleType):
    id = "LvS-103_Elverk103"
    name = "[CH] LvS-103 Elverk 103 EPP (HX)"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0
    eplrs = True


@vehiclemod
class RBS_70(unittype.VehicleType):
    id = "RBS-70"
    name = "[CH] RBS 70 VSHORAD LN"
    detection_range = 0
    threat_range = 8000
    air_weapon_dist = 8000
    eplrs = True


@vehiclemod
class RBS_90(unittype.VehicleType):
    id = "RBS-90"
    name = "[CH] RBS 90 VSHORAD LN"
    detection_range = 20000
    threat_range = 8000
    air_weapon_dist = 8000
    eplrs = True


@vehiclemod
class RBS_98(unittype.VehicleType):
    id = "RBS-98"
    name = "[CH] RBS 98 SAM LN (BvS 10)"
    detection_range = 0
    threat_range = 20000
    air_weapon_dist = 20000
    eplrs = True


@vehiclemod
class UndE23(unittype.VehicleType):
    id = "UndE23"
    name = "[CH] UndE 23 (RBS 70/90/98) STR"
    detection_range = 300000
    threat_range = 0
    air_weapon_dist = 0
    eplrs = True


## INFANTRY
@vehiclemod
class SwedishinfantryAK4(unittype.VehicleType):
    id = "SwedishinfantryAK4"
    name = "[CH] Ak 4 Soldier"
    detection_range = 0
    threat_range = 600
    air_weapon_dist = 600
    eplrs = True


@vehiclemod
class SwedishinfantryAK5(unittype.VehicleType):
    id = "SwedishinfantryAK5"
    name = "[CH] Ak 5 Soldier"
    detection_range = 0
    threat_range = 500
    air_weapon_dist = 500
    eplrs = True


@vehiclemod
class SwedishinfantryAK5GT(unittype.VehicleType):
    id = "SwedishinfantryAK5GT"
    name = "[CH] Ak 5 Granattillsats Soldier"
    detection_range = 0
    threat_range = 500
    air_weapon_dist = 500
    eplrs = True


@vehiclemod
class SwedishinfantryKSP90(unittype.VehicleType):
    id = "SwedishinfantryKSP90"
    name = "[CH] Ksp 90 Soldier"
    detection_range = 0
    threat_range = 700
    air_weapon_dist = 700
    eplrs = True


@vehiclemod
class SwedishinfantryKSP58(unittype.VehicleType):
    id = "SwedishinfantryKSP58"
    name = "[CH] Ksp 58 Soldier"
    detection_range = 0
    threat_range = 1200
    air_weapon_dist = 1200
    eplrs = True


@vehiclemod
class SwedishinfantryPskott86(unittype.VehicleType):
    id = "SwedishinfantryPskott86"
    name = "[CH] Pskott 86 Soldier"
    detection_range = 0
    threat_range = 400
    air_weapon_dist = 400
    eplrs = True


@vehiclemod
class RBS_57(unittype.VehicleType):
    id = "RBS-57"
    name = "[CH] RBS 57 ATGM Soldier"
    detection_range = 0
    threat_range = 1000
    air_weapon_dist = 1000
    eplrs = True


@vehiclemod
class RBS_58(unittype.VehicleType):
    id = "RBS-58"
    name = "[CH] RBS 58 ATGM"
    detection_range = 5000
    threat_range = 5000
    air_weapon_dist = 5000
    eplrs = True


@vehiclemod
class AG_90(unittype.VehicleType):
    id = "AG-90"
    name = "[CH] Ag 90 Sniper AMR"
    detection_range = 5000
    threat_range = 1800
    air_weapon_dist = 1800
    eplrs = True


##Armor
@vehiclemod
class CV9040(unittype.VehicleType):
    id = "CV9040"
    name = "[CH] Strf 9040B IFV"
    detection_range = 0
    threat_range = 4000
    air_weapon_dist = 4000
    eplrs = True


@vehiclemod
class CH_Strf9040C(unittype.VehicleType):
    id = "CH_Strf9040C"
    name = "[CH] Strf 9040C IFV"
    detection_range = 3500
    threat_range = 3500
    air_weapon_dist = 3500
    eplrs = True


@vehiclemod
class Strv103(unittype.VehicleType):
    id = "Strv103"
    name = "[CH] Strv 103 MBT"
    detection_range = 6000
    threat_range = 6000
    air_weapon_dist = 6000
    eplrs = True


@vehiclemod
class Strv2000(unittype.VehicleType):
    id = "Strv2000"
    name = "[CH] Strv 2000 T140/40 MBT"
    detection_range = 8000
    threat_range = 8000
    air_weapon_dist = 4000
    eplrs = True


@vehiclemod
class Volvo740(unittype.VehicleType):
    id = "Volvo740"
    name = "[CH] Volvo 740 Improvised fighting vehicle"
    detection_range = 0
    threat_range = 1200
    air_weapon_dist = 1200
    eplrs = True


@vehiclemod
class CH_BVS10(unittype.VehicleType):
    id = "CH_BVS10"
    name = "[CH] BvS 10 ATV"
    detection_range = 0
    threat_range = 1800
    air_weapon_dist = 1800
    eplrs = True


@vehiclemod
class CH_CV9050(unittype.VehicleType):
    id = "CH_CV9050"
    name = "[CH] CV 9050 IFV"
    detection_range = 6000
    threat_range = 5500
    air_weapon_dist = 5500
    eplrs = True


@vehiclemod
class CH_Ikv91(unittype.VehicleType):
    id = "CH_Ikv91"
    name = "[CH] Ikv 91 LT"
    detection_range = 3500
    threat_range = 3500
    air_weapon_dist = 1200
    eplrs = True


@vehiclemod
class CH_Strv123(unittype.VehicleType):
    id = "CH_Strv123"
    name = "[CH] Strv 123 MBT"
    detection_range = 0
    threat_range = 8000
    air_weapon_dist = 1200
    eplrs = True


@vehiclemod
class CH_Strv122(unittype.VehicleType):
    id = "CH_Strv122"
    name = "[CH] Strv 122 MBT"
    detection_range = 0
    threat_range = 8000
    air_weapon_dist = 1200
    eplrs = True


@vehiclemod
class CH_SisuGTP(unittype.VehicleType):
    id = "CH_SisuGTP"
    name = "[CH] Sisu GTP APC"
    detection_range = 0
    threat_range = 1800
    air_weapon_dist = 1800
    eplrs = True


## Missiles
@vehiclemod
class RBS_15KA(unittype.VehicleType):
    id = "RBS-15KA"
    name = "[CH] RBS 15KA LBASM"
    detection_range = 300000
    threat_range = 300000
    air_weapon_dist = 300000
    eplrs = True


## SHIPS
@shipmod
class Strb90(unittype.ShipType):
    id = "Strb90"
    name = "[CH] Strb 90 FAC"
    plane_num = 0
    helicopter_num = 0
    parking = 0
    detection_range = 46300
    threat_range = 10000
    air_weapon_dist = 10000


@shipmod
class HSwMS_Visby(unittype.ShipType):
    id = "HSwMS_Visby"
    name = "[CH] Visby Class Corvette"
    plane_num = 0
    helicopter_num = 1
    parking = 1
    detection_range = 180000
    threat_range = 30000
    air_weapon_dist = 30000


## HELICOPTERS
@helicoptermod
class HKP15B(HelicopterType):
    id = "HKP15B"
    height = 3.4
    width = 10.83
    length = 11.45
    fuel_max = 686
    max_speed = 311
    chaff = 0
    flare = 0
    charge_total = 0
    chaff_charge_size = 0
    flare_charge_size = 0
    eplrs = True
    radio_frequency = 124

    panel_radio = {
        1: {
            "channels": {6: 41, 2: 31, 8: 50, 3: 32, 1: 30, 4: 33, 5: 40, 7: 42},
        },
    }

    livery_name = "HKP15B"  # from type

    pylons: Set[int] = set()

    tasks = [task.Reconnaissance, task.Transport]
    task_default = task.Reconnaissance


## Planes
@planemod
class CH_JAS39C(PlaneType):
    id = "CH_JAS39C"
    height = 4.5
    width = 8.4
    length = 14.1
    fuel_max = 2550
    max_speed = 2649.996
    chaff = 80
    flare = 40
    charge_total = 120
    chaff_charge_size = 1
    flare_charge_size = 1
    eplrs = True
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}

    livery_name = "CH_JAS39C"  # from type

    class Pylon1:
        IRIS_T_IR_AAM = (1, Weapons.IRIS_T_IR_AAM)

    class Pylon2:
        IRIS_T_IR_AAM = (2, Weapons.IRIS_T_IR_AAM)
        Meteor_AMRAAM___Active_Radar_AAM = (2, Weapons.Meteor_AMRAAM___Active_Radar_AAM)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            2,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_8_AMRAAM___Active_Radar_AAM = (
            2,
            Weapons.AIM_120C_8_AMRAAM___Active_Radar_AAM,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (2, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_49___500lb_Laser__GPS_Guided_Bomb_LD = (
            2,
            Weapons.GBU_49___500lb_Laser__GPS_Guided_Bomb_LD,
        )
        GBU_39_SDB_285_lb_Guided_Glide_Bomb = (
            2,
            Weapons.GBU_39_SDB_285_lb_Guided_Glide_Bomb,
        )
        Rb_75A__AGM_65A_Maverick___TV_ASM_ = (
            2,
            Weapons.Rb_75A__AGM_65A_Maverick___TV_ASM_,
        )
        Rb_75B__AGM_65B_Maverick___TV_ASM_ = (
            2,
            Weapons.Rb_75B__AGM_65B_Maverick___TV_ASM_,
        )
        Rb_75T__AGM_65A_Maverick___TV_ASM_Lg_HE_Whd_ = (
            2,
            Weapons.Rb_75T__AGM_65A_Maverick___TV_ASM_Lg_HE_Whd_,
        )
        _4x_SB_M_71_120kg_GP_Bomb_Low_drag = (
            2,
            Weapons._4x_SB_M_71_120kg_GP_Bomb_Low_drag,
        )
        _4x_SB_M_71_120kg_GP_Bomb_High_drag = (
            2,
            Weapons._4x_SB_M_71_120kg_GP_Bomb_High_drag,
        )
        ARAK_M_70B_HE_6x_135mm_UnGd_Rkts__Shu70_HE_FRAG = (
            2,
            Weapons.ARAK_M_70B_HE_6x_135mm_UnGd_Rkts__Shu70_HE_FRAG,
        )
        ARAK_M_70B_AP_6x_135mm_UnGd_Rkts__Pshu70_HEAT = (
            2,
            Weapons.ARAK_M_70B_AP_6x_135mm_UnGd_Rkts__Pshu70_HEAT,
        )

    # ERRR <CLEAN>

    class Pylon3:
        IRIS_T_IR_AAM = (3, Weapons.IRIS_T_IR_AAM)
        Meteor_AMRAAM___Active_Radar_AAM = (3, Weapons.Meteor_AMRAAM___Active_Radar_AAM)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            3,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_8_AMRAAM___Active_Radar_AAM = (
            3,
            Weapons.AIM_120C_8_AMRAAM___Active_Radar_AAM,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (3, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_49___500lb_Laser__GPS_Guided_Bomb_LD = (
            3,
            Weapons.GBU_49___500lb_Laser__GPS_Guided_Bomb_LD,
        )
        GBU_39_SDB_285_lb_Guided_Glide_Bomb = (
            3,
            Weapons.GBU_39_SDB_285_lb_Guided_Glide_Bomb,
        )
        BK_90_MJ12__12x_MJ2_HEAT___36x_MJ1_HE_FRAG_Bomblets_ = (
            3,
            Weapons.BK_90_MJ12__12x_MJ2_HEAT___36x_MJ1_HE_FRAG_Bomblets_,
        )
        BK_90_MJ1__72_x_MJ1_HE_FRAG_Bomblets_ = (
            3,
            Weapons.BK_90_MJ1__72_x_MJ1_HE_FRAG_Bomblets_,
        )
        BK_90_MJ2__24_x_MJ2_HEAT_Bomblets_ = (
            3,
            Weapons.BK_90_MJ2__24_x_MJ2_HEAT_Bomblets_,
        )
        Rb_75A__AGM_65A_Maverick___TV_ASM_ = (
            3,
            Weapons.Rb_75A__AGM_65A_Maverick___TV_ASM_,
        )
        Rb_75B__AGM_65B_Maverick___TV_ASM_ = (
            3,
            Weapons.Rb_75B__AGM_65B_Maverick___TV_ASM_,
        )
        Rb_75T__AGM_65A_Maverick___TV_ASM_Lg_HE_Whd_ = (
            3,
            Weapons.Rb_75T__AGM_65A_Maverick___TV_ASM_Lg_HE_Whd_,
        )
        Taurus_KEPD_350_ALCM = (3, Weapons.Taurus_KEPD_350_ALCM)
        _4x_SB_M_71_120kg_GP_Bomb_Low_drag = (
            3,
            Weapons._4x_SB_M_71_120kg_GP_Bomb_Low_drag,
        )
        _4x_SB_M_71_120kg_GP_Bomb_High_drag = (
            3,
            Weapons._4x_SB_M_71_120kg_GP_Bomb_High_drag,
        )
        ARAK_M_70B_HE_6x_135mm_UnGd_Rkts__Shu70_HE_FRAG = (
            3,
            Weapons.ARAK_M_70B_HE_6x_135mm_UnGd_Rkts__Shu70_HE_FRAG,
        )
        ARAK_M_70B_AP_6x_135mm_UnGd_Rkts__Pshu70_HEAT = (
            3,
            Weapons.ARAK_M_70B_AP_6x_135mm_UnGd_Rkts__Pshu70_HEAT,
        )
        RBS_15_Mk4 = (3, Weapons.RBS_15_Mk4)
        Drop_tank_1100_litres = (3, Weapons.Drop_tank_1100_litres)

    # ERRR <CLEAN>

    class Pylon4:
        GBU_12___500lb_Laser_Guided_Bomb = (4, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_49___500lb_Laser__GPS_Guided_Bomb_LD = (
            4,
            Weapons.GBU_49___500lb_Laser__GPS_Guided_Bomb_LD,
        )
        _4x_SB_M_71_120kg_GP_Bomb_Low_drag = (
            4,
            Weapons._4x_SB_M_71_120kg_GP_Bomb_Low_drag,
        )
        _4x_SB_M_71_120kg_GP_Bomb_High_drag = (
            4,
            Weapons._4x_SB_M_71_120kg_GP_Bomb_High_drag,
        )
        Drop_tank_1100_litres = (4, Weapons.Drop_tank_1100_litres)
        AN_AAQ_28_LITENING___Targeting_Pod_ = (
            4,
            Weapons.AN_AAQ_28_LITENING___Targeting_Pod_,
        )

    # ERRR <CLEAN>

    class Pylon5:
        AN_AAQ_28_LITENING___Targeting_Pod_ = (
            5,
            Weapons.AN_AAQ_28_LITENING___Targeting_Pod_,
        )

    # ERRR <CLEAN>

    class Pylon6:
        IRIS_T_IR_AAM = (6, Weapons.IRIS_T_IR_AAM)
        Meteor_AMRAAM___Active_Radar_AAM = (6, Weapons.Meteor_AMRAAM___Active_Radar_AAM)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            6,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_8_AMRAAM___Active_Radar_AAM = (
            6,
            Weapons.AIM_120C_8_AMRAAM___Active_Radar_AAM,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (6, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_49___500lb_Laser__GPS_Guided_Bomb_LD = (
            6,
            Weapons.GBU_49___500lb_Laser__GPS_Guided_Bomb_LD,
        )
        GBU_39_SDB_285_lb_Guided_Glide_Bomb = (
            6,
            Weapons.GBU_39_SDB_285_lb_Guided_Glide_Bomb,
        )
        BK_90_MJ12__12x_MJ2_HEAT___36x_MJ1_HE_FRAG_Bomblets_ = (
            6,
            Weapons.BK_90_MJ12__12x_MJ2_HEAT___36x_MJ1_HE_FRAG_Bomblets_,
        )
        BK_90_MJ1__72_x_MJ1_HE_FRAG_Bomblets_ = (
            6,
            Weapons.BK_90_MJ1__72_x_MJ1_HE_FRAG_Bomblets_,
        )
        BK_90_MJ2__24_x_MJ2_HEAT_Bomblets_ = (
            6,
            Weapons.BK_90_MJ2__24_x_MJ2_HEAT_Bomblets_,
        )
        Rb_75A__AGM_65A_Maverick___TV_ASM_ = (
            6,
            Weapons.Rb_75A__AGM_65A_Maverick___TV_ASM_,
        )
        Rb_75B__AGM_65B_Maverick___TV_ASM_ = (
            6,
            Weapons.Rb_75B__AGM_65B_Maverick___TV_ASM_,
        )
        Rb_75T__AGM_65A_Maverick___TV_ASM_Lg_HE_Whd_ = (
            6,
            Weapons.Rb_75T__AGM_65A_Maverick___TV_ASM_Lg_HE_Whd_,
        )
        Taurus_KEPD_350_ALCM = (6, Weapons.Taurus_KEPD_350_ALCM)
        _4x_SB_M_71_120kg_GP_Bomb_Low_drag = (
            6,
            Weapons._4x_SB_M_71_120kg_GP_Bomb_Low_drag,
        )
        _4x_SB_M_71_120kg_GP_Bomb_High_drag = (
            6,
            Weapons._4x_SB_M_71_120kg_GP_Bomb_High_drag,
        )
        ARAK_M_70B_HE_6x_135mm_UnGd_Rkts__Shu70_HE_FRAG = (
            6,
            Weapons.ARAK_M_70B_HE_6x_135mm_UnGd_Rkts__Shu70_HE_FRAG,
        )
        ARAK_M_70B_AP_6x_135mm_UnGd_Rkts__Pshu70_HEAT = (
            6,
            Weapons.ARAK_M_70B_AP_6x_135mm_UnGd_Rkts__Pshu70_HEAT,
        )
        RBS_15_Mk4 = (6, Weapons.RBS_15_Mk4)
        Drop_tank_1100_litres = (6, Weapons.Drop_tank_1100_litres)

    # ERRR <CLEAN>

    class Pylon7:
        IRIS_T_IR_AAM = (7, Weapons.IRIS_T_IR_AAM)
        Meteor_AMRAAM___Active_Radar_AAM = (7, Weapons.Meteor_AMRAAM___Active_Radar_AAM)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            7,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_8_AMRAAM___Active_Radar_AAM = (
            7,
            Weapons.AIM_120C_8_AMRAAM___Active_Radar_AAM,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (7, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_49___500lb_Laser__GPS_Guided_Bomb_LD = (
            7,
            Weapons.GBU_49___500lb_Laser__GPS_Guided_Bomb_LD,
        )
        GBU_39_SDB_285_lb_Guided_Glide_Bomb = (
            7,
            Weapons.GBU_39_SDB_285_lb_Guided_Glide_Bomb,
        )
        Rb_75A__AGM_65A_Maverick___TV_ASM_ = (
            7,
            Weapons.Rb_75A__AGM_65A_Maverick___TV_ASM_,
        )
        Rb_75B__AGM_65B_Maverick___TV_ASM_ = (
            7,
            Weapons.Rb_75B__AGM_65B_Maverick___TV_ASM_,
        )
        Rb_75T__AGM_65A_Maverick___TV_ASM_Lg_HE_Whd_ = (
            7,
            Weapons.Rb_75T__AGM_65A_Maverick___TV_ASM_Lg_HE_Whd_,
        )
        _4x_SB_M_71_120kg_GP_Bomb_Low_drag = (
            7,
            Weapons._4x_SB_M_71_120kg_GP_Bomb_Low_drag,
        )
        _4x_SB_M_71_120kg_GP_Bomb_High_drag = (
            7,
            Weapons._4x_SB_M_71_120kg_GP_Bomb_High_drag,
        )
        ARAK_M_70B_HE_6x_135mm_UnGd_Rkts__Shu70_HE_FRAG = (
            7,
            Weapons.ARAK_M_70B_HE_6x_135mm_UnGd_Rkts__Shu70_HE_FRAG,
        )
        ARAK_M_70B_AP_6x_135mm_UnGd_Rkts__Pshu70_HEAT = (
            7,
            Weapons.ARAK_M_70B_AP_6x_135mm_UnGd_Rkts__Pshu70_HEAT,
        )

    # ERRR <CLEAN>

    class Pylon8:
        IRIS_T_IR_AAM = (8, Weapons.IRIS_T_IR_AAM)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.AFAC,
        task.SEAD,
        task.AntishipStrike,
        task.CAS,
        task.PinpointStrike,
        task.GroundAttack,
        task.RunwayAttack,
    ]
    task_default = task.CAP
