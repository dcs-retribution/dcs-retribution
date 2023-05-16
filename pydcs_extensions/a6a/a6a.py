from typing import Set

from dcs import task
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

from game.modsupport import planemod


@planemod
class VSN_A6A(PlaneType):
    id = "VSN_A6A"
    flyable = True
    height = 4.57
    width = 10.15
    length = 17.98
    fuel_max = 6994
    max_speed = 1047.96
    chaff = 30
    flare = 30
    charge_total = 60
    chaff_charge_size = 1
    flare_charge_size = 1
    eplrs = True
    radio_frequency = 250.5

    livery_name = "VSN_A6A"  # from type

    class Pylon1:
        F_5_275Gal_Fuel_tank = (1, Weapons.F_5_275Gal_Fuel_tank)
        AIM_9M_Sidewinder_IR_AAM = (1, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (1, Weapons.AIM_9X_Sidewinder_IR_AAM)
        Mk_82___500lb_GP_Bomb_LD = (1, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_83___1000lb_GP_Bomb_LD = (1, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        Mk_84___2000lb_GP_Bomb_LD = (1, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD = (
            1,
            Weapons.BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD,
        )
        BRU_42_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bombs_HD = (
            1,
            Weapons.BRU_42_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bombs_HD,
        )
        LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            1,
            Weapons.LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT = (
            1,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT,
        )
        LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            1,
            Weapons.LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_33_with_2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            1,
            Weapons.BRU_33_with_2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            1,
            Weapons.BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_33_with_2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            1,
            Weapons.BRU_33_with_2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )

    # ERRR {ac94375e-aa45-491e-858b-a8b93ee8b959}
    # ERRR <CLEAN>

    class Pylon2:
        F_5_275Gal_Fuel_tank = (2, Weapons.F_5_275Gal_Fuel_tank)
        AIM_9M_Sidewinder_IR_AAM = (2, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (2, Weapons.AIM_9X_Sidewinder_IR_AAM)
        Mk_82___500lb_GP_Bomb_LD = (2, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_83___1000lb_GP_Bomb_LD = (2, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        Mk_84___2000lb_GP_Bomb_LD = (2, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        MER6_with_6_x_Mk_82___500lb_GP_Bombs_LD = (
            2,
            Weapons.MER6_with_6_x_Mk_82___500lb_GP_Bombs_LD,
        )
        MER6_with_6_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets = (
            2,
            Weapons.MER6_with_6_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets,
        )
        BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD = (
            2,
            Weapons.BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD,
        )
        BRU_42_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bombs_HD = (
            2,
            Weapons.BRU_42_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bombs_HD,
        )
        LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            2,
            Weapons.LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT = (
            2,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT,
        )
        LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            2,
            Weapons.LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_33_with_2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            2,
            Weapons.BRU_33_with_2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            2,
            Weapons.BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_33_with_2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            2,
            Weapons.BRU_33_with_2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )

    # ERRR {ac94375e-aa45-491e-858b-a8b93ee8b959}
    # ERRR <CLEAN>

    class Pylon3:
        F_5_275Gal_Fuel_tank = (3, Weapons.F_5_275Gal_Fuel_tank)
        Mk_82___500lb_GP_Bomb_LD = (3, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_83___1000lb_GP_Bomb_LD = (3, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        Mk_84___2000lb_GP_Bomb_LD = (3, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        MER6_with_6_x_Mk_82___500lb_GP_Bombs_LD = (
            3,
            Weapons.MER6_with_6_x_Mk_82___500lb_GP_Bombs_LD,
        )
        MER6_with_6_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets = (
            3,
            Weapons.MER6_with_6_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets,
        )
        BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD = (
            3,
            Weapons.BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD,
        )
        BRU_42_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bombs_HD = (
            3,
            Weapons.BRU_42_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bombs_HD,
        )

    # ERRR {ac94375e-aa45-491e-858b-a8b93ee8b959}
    # ERRR <CLEAN>

    class Pylon4:
        F_5_275Gal_Fuel_tank = (4, Weapons.F_5_275Gal_Fuel_tank)
        AIM_9M_Sidewinder_IR_AAM = (4, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (4, Weapons.AIM_9X_Sidewinder_IR_AAM)
        Mk_82___500lb_GP_Bomb_LD = (4, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_83___1000lb_GP_Bomb_LD = (4, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        Mk_84___2000lb_GP_Bomb_LD = (4, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        MER6_with_6_x_Mk_82___500lb_GP_Bombs_LD = (
            4,
            Weapons.MER6_with_6_x_Mk_82___500lb_GP_Bombs_LD,
        )
        MER6_with_6_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets = (
            4,
            Weapons.MER6_with_6_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets,
        )
        BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD = (
            4,
            Weapons.BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD,
        )
        BRU_42_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bombs_HD = (
            4,
            Weapons.BRU_42_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bombs_HD,
        )
        LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            4,
            Weapons.LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT = (
            4,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT,
        )
        LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            4,
            Weapons.LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_33_with_2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            4,
            Weapons.BRU_33_with_2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            4,
            Weapons.BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_33_with_2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            4,
            Weapons.BRU_33_with_2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )

    # ERRR {ac94375e-aa45-491e-858b-a8b93ee8b959}
    # ERRR <CLEAN>

    class Pylon5:
        F_5_275Gal_Fuel_tank = (5, Weapons.F_5_275Gal_Fuel_tank)
        AIM_9M_Sidewinder_IR_AAM = (5, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (5, Weapons.AIM_9X_Sidewinder_IR_AAM)
        Mk_82___500lb_GP_Bomb_LD = (5, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_83___1000lb_GP_Bomb_LD = (5, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        Mk_84___2000lb_GP_Bomb_LD = (5, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD = (
            5,
            Weapons.BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD,
        )
        BRU_42_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bombs_HD = (
            5,
            Weapons.BRU_42_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bombs_HD,
        )
        LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            5,
            Weapons.LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT = (
            5,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT,
        )
        LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            5,
            Weapons.LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_33_with_2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            5,
            Weapons.BRU_33_with_2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            5,
            Weapons.BRU_33_with_2_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_33_with_2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            5,
            Weapons.BRU_33_with_2_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )

    # ERRR {ac94375e-aa45-491e-858b-a8b93ee8b959}
    # ERRR <CLEAN>

    pylons: Set[int] = {1, 2, 3, 4, 5}

    tasks = [
        task.Escort,
        task.Reconnaissance,
        task.GroundAttack,
        task.CAS,
        task.AFAC,
        task.RunwayAttack,
        task.AntishipStrike,
        task.SEAD,
    ]
    task_default = task.GroundAttack
