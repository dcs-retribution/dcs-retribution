from typing import Dict, List, Set, Any

from dcs import task
from dcs.planes import PlaneType
from dcs.unitpropertydescription import UnitPropertyDescription
from dcs.weapons_data import Weapons

from game.modsupport import planemod
from pydcs_extensions.weapon_injector import inject_weapons


class WeaponsF111C:
    AGM_130_TV_Guided_Missile = {
        "clsid": "{F111C_AGM_130}",
        "name": "AGM-130 TV Guided Missile",
        "weight": 970,
    }
    AGM_142_Popeye = {
        "clsid": "{F111C_AGM_142_ARM}",
        "name": "AGM-142 Popeye",
        "weight": 1360,
    }
    AGM_84D_Harpoon = {
        "clsid": "{F111C_AGM_84_ARM}",
        "name": "AGM-84D Harpoon",
        "weight": 540,
    }
    AN_ASW_55 = {"clsid": "{F111C_AN_ASW_55}", "name": "AN/ASW-55", "weight": 865}
    AN_AXQ_14 = {"clsid": "{F111C_AN_AXQ_14}", "name": "AN/AXQ-14", "weight": 182}
    Elta_EL_L_8222 = {
        "clsid": "{F111C_EL_L_8222}",
        "name": "Elta EL/L 8222",
        "weight": 110,
    }
    GBU_10_2000_lb_TV_Guided_Bomb = {
        "clsid": "{F111C_GBU10}",
        "name": "GBU-10 2000 lb TV Guided Bomb",
        "weight": 934,
    }
    GBU_12_500_lb_TV_Guided_Bomb = {
        "clsid": "{F111C_GBU12}",
        "name": "GBU-12 500 lb TV Guided Bomb",
        "weight": 241,
    }
    GBU_15_2000_lb_TV_Guided_Bomb = {
        "clsid": "{F111C_GBU15_V1B}",
        "name": "GBU-15 2000 lb TV Guided Bomb",
        "weight": 1111,
    }
    GBU_16_1000_lb_TV_Guided_Bomb = {
        "clsid": "{F111C_GBU16}",
        "name": "GBU-16 1000 lb TV Guided Bomb",
        "weight": 454,
    }
    GBU_24_2000_lb_Penetrator_TV_Guided_Bomb = {
        "clsid": "{F111C_GBU24}",
        "name": "GBU-24 2000 lb Penetrator TV Guided Bomb",
        "weight": 970,
    }
    Integrated_ELINT = {
        "clsid": "{F111C_ELINT}",
        "name": "Integrated ELINT",
        "weight": 1,
    }
    Targeting_Pod_FLIR = {
        "clsid": "{F111C_FLIR}",
        "name": "Targeting Pod FLIR",
        "weight": 2,
    }


inject_weapons(WeaponsF111C)


@planemod
class F111C(PlaneType):
    id = "F111C"
    flyable = True
    height = 6.19
    width = 21.33
    length = 22.53
    fuel_max = 14860
    max_speed = 1699.2
    chaff = 100
    flare = 100
    charge_total = 200
    chaff_charge_size = 1
    flare_charge_size = 1
    eplrs = True
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    livery_name = "F111C"  # from livery_entry
    # ERRR <CLEAN>

    class Pylon2:
        Smoke_Generator___orange_ = (2, Weapons.Smoke_Generator___orange_)

    # ERRR <CLEAN>
    # ERRR <CLEAN>

    class Pylon4:
        AIM_9M_Sidewinder_IR_AAM = (4, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (4, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AGM_84D_Harpoon = (4, WeaponsF111C.AGM_84D_Harpoon)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            4,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        AGM_130_TV_Guided_Missile = (4, WeaponsF111C.AGM_130_TV_Guided_Missile)
        AGM_142_Popeye = (4, WeaponsF111C.AGM_142_Popeye)
        BRU_41A_with_6_x_BDU_33___25lb_Practice_Bomb_LD = (
            4,
            Weapons.BRU_41A_with_6_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        BDU_45___500lb_Practice_Bomb = (4, Weapons.BDU_45___500lb_Practice_Bomb)
        BDU_45B___500lb_Practice_Bomb = (4, Weapons.BDU_45B___500lb_Practice_Bomb)
        TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb = (
            4,
            Weapons.TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb,
        )
        TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb = (
            4,
            Weapons.TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb,
        )
        BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD = (
            4,
            Weapons.BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD,
        )
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            4,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        BRU_42_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bombs_HD = (
            4,
            Weapons.BRU_42_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bombs_HD,
        )
        BRU_41A_with_6_x_Mk_82___500lb_GP_Bomb_LD = (
            4,
            Weapons.BRU_41A_with_6_x_Mk_82___500lb_GP_Bomb_LD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (4, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = (
            4,
            Weapons.Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (4, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD = (
            4,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        GBU_12_500_lb_TV_Guided_Bomb = (4, WeaponsF111C.GBU_12_500_lb_TV_Guided_Bomb)
        GBU_10_2000_lb_TV_Guided_Bomb = (4, WeaponsF111C.GBU_10_2000_lb_TV_Guided_Bomb)
        GBU_15_2000_lb_TV_Guided_Bomb = (4, WeaponsF111C.GBU_15_2000_lb_TV_Guided_Bomb)
        GBU_16_1000_lb_TV_Guided_Bomb = (4, WeaponsF111C.GBU_16_1000_lb_TV_Guided_Bomb)
        GBU_24_2000_lb_Penetrator_TV_Guided_Bomb = (
            4,
            WeaponsF111C.GBU_24_2000_lb_Penetrator_TV_Guided_Bomb,
        )
        Fuel_Tank_FT600 = (4, Weapons.Fuel_Tank_FT600)

    # ERRR <CLEAN>

    class Pylon5:
        AIM_9M_Sidewinder_IR_AAM = (5, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (5, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (5, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        AGM_84D_Harpoon = (5, WeaponsF111C.AGM_84D_Harpoon)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            5,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        AGM_130_TV_Guided_Missile = (5, WeaponsF111C.AGM_130_TV_Guided_Missile)
        BRU_41A_with_6_x_BDU_33___25lb_Practice_Bomb_LD = (
            5,
            Weapons.BRU_41A_with_6_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        BDU_45___500lb_Practice_Bomb = (5, Weapons.BDU_45___500lb_Practice_Bomb)
        BDU_45B___500lb_Practice_Bomb = (5, Weapons.BDU_45B___500lb_Practice_Bomb)
        TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb = (
            5,
            Weapons.TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb,
        )
        TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb = (
            5,
            Weapons.TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb,
        )
        BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD = (
            5,
            Weapons.BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD,
        )
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            5,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        BRU_42_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bombs_HD = (
            5,
            Weapons.BRU_42_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bombs_HD,
        )
        BRU_41A_with_6_x_Mk_82___500lb_GP_Bomb_LD = (
            5,
            Weapons.BRU_41A_with_6_x_Mk_82___500lb_GP_Bomb_LD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (5, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = (
            5,
            Weapons.Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (5, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD = (
            5,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        GBU_12_500_lb_TV_Guided_Bomb = (5, WeaponsF111C.GBU_12_500_lb_TV_Guided_Bomb)
        GBU_10_2000_lb_TV_Guided_Bomb = (5, WeaponsF111C.GBU_10_2000_lb_TV_Guided_Bomb)
        GBU_15_2000_lb_TV_Guided_Bomb = (5, WeaponsF111C.GBU_15_2000_lb_TV_Guided_Bomb)
        GBU_16_1000_lb_TV_Guided_Bomb = (5, WeaponsF111C.GBU_16_1000_lb_TV_Guided_Bomb)
        GBU_24_2000_lb_Penetrator_TV_Guided_Bomb = (
            5,
            WeaponsF111C.GBU_24_2000_lb_Penetrator_TV_Guided_Bomb,
        )
        Elta_EL_L_8222 = (5, WeaponsF111C.Elta_EL_L_8222)
        Fuel_Tank_FT600 = (5, Weapons.Fuel_Tank_FT600)

    # ERRR <CLEAN>
    # ERRR <CLEAN>
    # ERRR <CLEAN>

    class Pylon8:
        AIM_9M_Sidewinder_IR_AAM = (8, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (8, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AGM_84D_Harpoon = (8, WeaponsF111C.AGM_84D_Harpoon)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            8,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        AN_AXQ_14 = (8, WeaponsF111C.AN_AXQ_14)
        AN_ASW_55 = (8, WeaponsF111C.AN_ASW_55)
        AGM_130_TV_Guided_Missile = (8, WeaponsF111C.AGM_130_TV_Guided_Missile)
        BRU_41A_with_6_x_BDU_33___25lb_Practice_Bomb_LD = (
            8,
            Weapons.BRU_41A_with_6_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        BDU_45___500lb_Practice_Bomb = (8, Weapons.BDU_45___500lb_Practice_Bomb)
        BDU_45B___500lb_Practice_Bomb = (8, Weapons.BDU_45B___500lb_Practice_Bomb)
        TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb = (
            8,
            Weapons.TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb,
        )
        TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb = (
            8,
            Weapons.TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb,
        )
        BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD = (
            8,
            Weapons.BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD,
        )
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            8,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        BRU_42_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bombs_HD = (
            8,
            Weapons.BRU_42_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bombs_HD,
        )
        BRU_41A_with_6_x_Mk_82___500lb_GP_Bomb_LD = (
            8,
            Weapons.BRU_41A_with_6_x_Mk_82___500lb_GP_Bomb_LD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (8, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = (
            8,
            Weapons.Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (8, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD = (
            8,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        GBU_12_500_lb_TV_Guided_Bomb = (8, WeaponsF111C.GBU_12_500_lb_TV_Guided_Bomb)
        GBU_10_2000_lb_TV_Guided_Bomb = (8, WeaponsF111C.GBU_10_2000_lb_TV_Guided_Bomb)
        GBU_15_2000_lb_TV_Guided_Bomb = (8, WeaponsF111C.GBU_15_2000_lb_TV_Guided_Bomb)
        GBU_16_1000_lb_TV_Guided_Bomb = (8, WeaponsF111C.GBU_16_1000_lb_TV_Guided_Bomb)
        GBU_24_2000_lb_Penetrator_TV_Guided_Bomb = (
            8,
            WeaponsF111C.GBU_24_2000_lb_Penetrator_TV_Guided_Bomb,
        )
        Fuel_Tank_FT600 = (8, Weapons.Fuel_Tank_FT600)

    # ERRR <CLEAN>

    class Pylon9:
        AIM_9M_Sidewinder_IR_AAM = (9, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (9, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AGM_84D_Harpoon = (9, WeaponsF111C.AGM_84D_Harpoon)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            9,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        AGM_130_TV_Guided_Missile = (9, WeaponsF111C.AGM_130_TV_Guided_Missile)
        AGM_142_Popeye = (9, WeaponsF111C.AGM_142_Popeye)
        BRU_41A_with_6_x_BDU_33___25lb_Practice_Bomb_LD = (
            9,
            Weapons.BRU_41A_with_6_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        BDU_45___500lb_Practice_Bomb = (9, Weapons.BDU_45___500lb_Practice_Bomb)
        BDU_45B___500lb_Practice_Bomb = (9, Weapons.BDU_45B___500lb_Practice_Bomb)
        TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb = (
            9,
            Weapons.TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb,
        )
        TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb = (
            9,
            Weapons.TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb,
        )
        BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD = (
            9,
            Weapons.BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD,
        )
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            9,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        BRU_42_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bombs_HD = (
            9,
            Weapons.BRU_42_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bombs_HD,
        )
        BRU_41A_with_6_x_Mk_82___500lb_GP_Bomb_LD = (
            9,
            Weapons.BRU_41A_with_6_x_Mk_82___500lb_GP_Bomb_LD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (9, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD = (
            9,
            Weapons.Mk_83_AIR__BSU_85____1000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (9, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD = (
            9,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        GBU_12_500_lb_TV_Guided_Bomb = (9, WeaponsF111C.GBU_12_500_lb_TV_Guided_Bomb)
        GBU_10_2000_lb_TV_Guided_Bomb = (9, WeaponsF111C.GBU_10_2000_lb_TV_Guided_Bomb)
        GBU_15_2000_lb_TV_Guided_Bomb = (9, WeaponsF111C.GBU_15_2000_lb_TV_Guided_Bomb)
        GBU_16_1000_lb_TV_Guided_Bomb = (9, WeaponsF111C.GBU_16_1000_lb_TV_Guided_Bomb)
        GBU_24_2000_lb_Penetrator_TV_Guided_Bomb = (
            9,
            WeaponsF111C.GBU_24_2000_lb_Penetrator_TV_Guided_Bomb,
        )
        Fuel_Tank_FT600 = (9, Weapons.Fuel_Tank_FT600)

    # ERRR <CLEAN>

    class Pylon10:
        Elta_EL_L_8222 = (10, WeaponsF111C.Elta_EL_L_8222)
        AN_AXQ_14 = (10, WeaponsF111C.AN_AXQ_14)

    # ERRR <CLEAN>

    class Pylon11:
        Targeting_Pod_FLIR = (11, WeaponsF111C.Targeting_Pod_FLIR)

    # ERRR <CLEAN>

    class Pylon12:
        Integrated_ELINT = (12, WeaponsF111C.Integrated_ELINT)

    # ERRR <CLEAN>

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}

    tasks = [
        task.GroundAttack,
        task.CAS,
        task.AntishipStrike,
        task.SEAD,
        task.PinpointStrike,
        task.AFAC,
        task.RunwayAttack,
    ]
    task_default = task.GroundAttack
