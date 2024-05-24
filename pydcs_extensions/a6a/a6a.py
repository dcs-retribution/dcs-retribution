from typing import Set

from dcs import task
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

from game.modsupport import planemod
from pydcs_extensions import inject_weapons, WeaponsA7E

inject_weapons(WeaponsA7E)


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

    # We have also enabled Adecarcer's modified hardpoint options for the A-6A Intruder mod.
    # This will, for instance, fix the MER bomb racks which have the "missing texture" material
    # in the stock version of the mod. It will also allow mounting some weapons which are more
    # appropriate for the A-6E variant of the aircraft. While not historically or technically
    # accurate, this will allow employing the aircraft in a role which is closer to the EA-6B
    # or A-6E, should the user wish to do so. The EA-6B mod is AI-only, so this will grant a
    # player-flyable option. The use of custom loadouts is recommended.
    # Please note that some of these weapons are part of the A-7E Corsair II mod,
    # which will need to be installed if one wants to use those weapons.

    class Pylon1:
        F_5_275Gal_Fuel_tank = (1, Weapons.F_5_275Gal_Fuel_tank)
        AIM_9M_Sidewinder_IR_AAM = (1, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (1, Weapons.AIM_9X_Sidewinder_IR_AAM)
        LAU_7_with_AIM_9B_Sidewinder_IR_AAM = (
            1,
            Weapons.LAU_7_with_AIM_9B_Sidewinder_IR_AAM,
        )
        LAU_7_with_AIM_9J_Sidewinder_IR_AAM = (
            1,
            Weapons.LAU_7_with_AIM_9J_Sidewinder_IR_AAM,
        )
        LAU_7_with_AIM_9M_Sidewinder_IR_AAM = (
            1,
            Weapons.LAU_7_with_AIM_9M_Sidewinder_IR_AAM,
        )
        LAU_7_with_AIM_9P_Sidewinder_IR_AAM = (
            1,
            Weapons.LAU_7_with_AIM_9P_Sidewinder_IR_AAM,
        )
        AGM_45A_Shrike_ARM = (1, Weapons.AGM_45A_Shrike_ARM)
        AGM_45B_Shrike_ARM = (1, Weapons.AGM_45B_Shrike_ARM)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            1,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            1,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            1,
            Weapons.LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            1,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_117_AGM_65G = (1, Weapons.LAU_117_AGM_65G)
        AGM_84D_Harpoon_AShM = (1, Weapons.AGM_84D_Harpoon_AShM)
        AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile__ = (
            1,
            Weapons.AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile__,
        )
        Mk_82___500lb_GP_Bomb_LD = (1, Weapons.Mk_82___500lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            1,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        _3_Mk_82 = (1, Weapons._3_Mk_82)
        _5_x_Mk_82___500lb_GP_Bombs_LD = (1, Weapons._5_x_Mk_82___500lb_GP_Bombs_LD)
        BRU_41A_with_6_x_Mk_82___500lb_GP_Bomb_LD = (
            1,
            Weapons.BRU_41A_with_6_x_Mk_82___500lb_GP_Bomb_LD,
        )
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (1, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        _3_Mk_82_Snakeye = (1, Weapons._3_Mk_82_Snakeye)
        _5_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            1,
            Weapons._5_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            1,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        BRU_41A___6_x_Mk_82AIR = (1, WeaponsA7E.BRU_41A___6_x_Mk_82AIR)
        Mk_83___1000lb_GP_Bomb_LD = (1, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_83___1000lb_GP_Bombs_LD = (
            1,
            Weapons.MER2_with_2_x_Mk_83___1000lb_GP_Bombs_LD,
        )
        BRU_42A___3_x_Mk_83 = (1, WeaponsA7E.BRU_42A___3_x_Mk_83)
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
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            1,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        BRU_33_with_2_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            1,
            Weapons.BRU_33_with_2_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        BRU_42A___3_x_Mk_20_Rockeye = (1, WeaponsA7E.BRU_42A___3_x_Mk_20_Rockeye)
        BRU_41A___6_x_Mk_20_Rockeye = (1, WeaponsA7E.BRU_41A___6_x_Mk_20_Rockeye)
        GBU_10___2000lb_Laser_Guided_Bomb = (
            1,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (1, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_16___1000lb_Laser_Guided_Bomb = (
            1,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        # ERRR {CBU-99}
        ADM_141A_TALD = (1, Weapons.ADM_141A_TALD)
        SUU_25_x_8_LUU_2___Target_Marker_Flares = (
            1,
            Weapons.SUU_25_x_8_LUU_2___Target_Marker_Flares,
        )
        BRU_33_with_1_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            1,
            Weapons.BRU_33_with_1_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        BRU_33_with_1_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            1,
            Weapons.BRU_33_with_1_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_33_with_1_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT = (
            1,
            Weapons.BRU_33_with_1_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT,
        )
        BRU_33_with_1_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            1,
            Weapons.BRU_33_with_1_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_33_with_2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT = (
            1,
            Weapons.BRU_33_with_2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT,
        )

    class Pylon2:
        F_5_275Gal_Fuel_tank = (2, Weapons.F_5_275Gal_Fuel_tank)
        AIM_9M_Sidewinder_IR_AAM = (2, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (2, Weapons.AIM_9X_Sidewinder_IR_AAM)
        L_081_Fantasmagoria_ELINT_pod = (2, Weapons.L_081_Fantasmagoria_ELINT_pod)
        LAU_7_with_AIM_9B_Sidewinder_IR_AAM = (
            2,
            Weapons.LAU_7_with_AIM_9B_Sidewinder_IR_AAM,
        )
        LAU_7_with_AIM_9J_Sidewinder_IR_AAM = (
            2,
            Weapons.LAU_7_with_AIM_9J_Sidewinder_IR_AAM,
        )
        LAU_7_with_AIM_9M_Sidewinder_IR_AAM = (
            2,
            Weapons.LAU_7_with_AIM_9M_Sidewinder_IR_AAM,
        )
        LAU_7_with_AIM_9P_Sidewinder_IR_AAM = (
            2,
            Weapons.LAU_7_with_AIM_9P_Sidewinder_IR_AAM,
        )
        AGM_45A_Shrike_ARM = (2, Weapons.AGM_45A_Shrike_ARM)
        AGM_45B_Shrike_ARM = (2, Weapons.AGM_45B_Shrike_ARM)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            2,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            2,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            2,
            Weapons.LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            2,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_117_AGM_65G = (2, Weapons.LAU_117_AGM_65G)
        AGM_84D_Harpoon_AShM = (2, Weapons.AGM_84D_Harpoon_AShM)
        AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile__ = (
            2,
            Weapons.AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile__,
        )
        AGM_62_Walleye_II___Guided_Weapon_Mk_5__TV_Guided_ = (
            2,
            Weapons.AGM_62_Walleye_II___Guided_Weapon_Mk_5__TV_Guided_,
        )
        Mk_82___500lb_GP_Bomb_LD = (2, Weapons.Mk_82___500lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            2,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        _3_Mk_82 = (2, Weapons._3_Mk_82)
        BRU_41A_with_6_x_Mk_82___500lb_GP_Bomb_LD = (
            2,
            Weapons.BRU_41A_with_6_x_Mk_82___500lb_GP_Bomb_LD,
        )
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (2, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        _3_Mk_82_Snakeye = (2, Weapons._3_Mk_82_Snakeye)
        BRU_41A___6_x_Mk_82_Snakeye = (2, WeaponsA7E.BRU_41A___6_x_Mk_82_Snakeye)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            2,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        BRU_41A___6_x_Mk_82AIR = (2, WeaponsA7E.BRU_41A___6_x_Mk_82AIR)
        Mk_83___1000lb_GP_Bomb_LD = (2, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_83___1000lb_GP_Bombs_LD = (
            2,
            Weapons.MER2_with_2_x_Mk_83___1000lb_GP_Bombs_LD,
        )
        BRU_42A___3_x_Mk_83 = (2, WeaponsA7E.BRU_42A___3_x_Mk_83)
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
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            2,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        BRU_42A___3_x_Mk_20_Rockeye = (2, WeaponsA7E.BRU_42A___3_x_Mk_20_Rockeye)
        BRU_41A___6_x_Mk_20_Rockeye = (2, WeaponsA7E.BRU_41A___6_x_Mk_20_Rockeye)
        GBU_10___2000lb_Laser_Guided_Bomb = (
            2,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (2, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_16___1000lb_Laser_Guided_Bomb = (
            2,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        # ERRR {CBU-99}
        ADM_141A_TALD = (2, Weapons.ADM_141A_TALD)
        SUU_25_x_8_LUU_2___Target_Marker_Flares = (
            2,
            Weapons.SUU_25_x_8_LUU_2___Target_Marker_Flares,
        )
        BRU_33_with_1_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            2,
            Weapons.BRU_33_with_1_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        BRU_33_with_1_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            2,
            Weapons.BRU_33_with_1_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_33_with_1_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT = (
            2,
            Weapons.BRU_33_with_1_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT,
        )
        BRU_33_with_1_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            2,
            Weapons.BRU_33_with_1_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_33_with_2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT = (
            2,
            Weapons.BRU_33_with_2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT,
        )

    class Pylon3:
        F_5_275Gal_Fuel_tank = (3, Weapons.F_5_275Gal_Fuel_tank)
        L_081_Fantasmagoria_ELINT_pod = (3, Weapons.L_081_Fantasmagoria_ELINT_pod)
        Mercury_LLTV_Pod = (3, Weapons.Mercury_LLTV_Pod)
        Mk_82___500lb_GP_Bomb_LD = (3, Weapons.Mk_82___500lb_GP_Bomb_LD)
        _3_Mk_82 = (3, Weapons._3_Mk_82)
        BRU_41A_with_6_x_Mk_82___500lb_GP_Bomb_LD = (
            3,
            Weapons.BRU_41A_with_6_x_Mk_82___500lb_GP_Bomb_LD,
        )
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (3, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        _3_Mk_82_Snakeye = (3, Weapons._3_Mk_82_Snakeye)
        BRU_41A___6_x_Mk_82_Snakeye = (3, WeaponsA7E.BRU_41A___6_x_Mk_82_Snakeye)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            3,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        BRU_41A___6_x_Mk_82AIR = (3, WeaponsA7E.BRU_41A___6_x_Mk_82AIR)
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
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            3,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        BRU_42A___3_x_Mk_20_Rockeye = (3, WeaponsA7E.BRU_42A___3_x_Mk_20_Rockeye)
        BRU_41A___6_x_Mk_20_Rockeye = (3, WeaponsA7E.BRU_41A___6_x_Mk_20_Rockeye)
        GBU_10___2000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (3, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_16___1000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        # ERRR {CBU-99}
        ADM_141A_TALD = (3, Weapons.ADM_141A_TALD)

    class Pylon4:
        F_5_275Gal_Fuel_tank = (4, Weapons.F_5_275Gal_Fuel_tank)
        AIM_9M_Sidewinder_IR_AAM = (4, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (4, Weapons.AIM_9X_Sidewinder_IR_AAM)
        L_081_Fantasmagoria_ELINT_pod = (4, Weapons.L_081_Fantasmagoria_ELINT_pod)
        LAU_7_with_AIM_9B_Sidewinder_IR_AAM = (
            4,
            Weapons.LAU_7_with_AIM_9B_Sidewinder_IR_AAM,
        )
        LAU_7_with_AIM_9J_Sidewinder_IR_AAM = (
            4,
            Weapons.LAU_7_with_AIM_9J_Sidewinder_IR_AAM,
        )
        LAU_7_with_AIM_9M_Sidewinder_IR_AAM = (
            4,
            Weapons.LAU_7_with_AIM_9M_Sidewinder_IR_AAM,
        )
        LAU_7_with_AIM_9P_Sidewinder_IR_AAM = (
            4,
            Weapons.LAU_7_with_AIM_9P_Sidewinder_IR_AAM,
        )
        AGM_45A_Shrike_ARM = (4, Weapons.AGM_45A_Shrike_ARM)
        AGM_45B_Shrike_ARM = (4, Weapons.AGM_45B_Shrike_ARM)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            4,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            4,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            4,
            Weapons.LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            4,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_117_AGM_65G = (4, Weapons.LAU_117_AGM_65G)
        AGM_84D_Harpoon_AShM = (4, Weapons.AGM_84D_Harpoon_AShM)
        AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile__ = (
            4,
            Weapons.AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile__,
        )
        AGM_62_Walleye_II___Guided_Weapon_Mk_5__TV_Guided_ = (
            4,
            Weapons.AGM_62_Walleye_II___Guided_Weapon_Mk_5__TV_Guided_,
        )
        Mk_82___500lb_GP_Bomb_LD = (4, Weapons.Mk_82___500lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            4,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        _3_Mk_82 = (4, Weapons._3_Mk_82)
        BRU_41A_with_6_x_Mk_82___500lb_GP_Bomb_LD = (
            4,
            Weapons.BRU_41A_with_6_x_Mk_82___500lb_GP_Bomb_LD,
        )
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (4, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        _3_Mk_82_Snakeye = (4, Weapons._3_Mk_82_Snakeye)
        BRU_41A___6_x_Mk_82_Snakeye = (4, WeaponsA7E.BRU_41A___6_x_Mk_82_Snakeye)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            4,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        BRU_41A___6_x_Mk_82AIR = (4, WeaponsA7E.BRU_41A___6_x_Mk_82AIR)
        Mk_83___1000lb_GP_Bomb_LD = (4, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_83___1000lb_GP_Bombs_LD = (
            4,
            Weapons.MER2_with_2_x_Mk_83___1000lb_GP_Bombs_LD,
        )
        BRU_42A___3_x_Mk_83 = (4, WeaponsA7E.BRU_42A___3_x_Mk_83)
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
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            4,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        BRU_42A___3_x_Mk_20_Rockeye = (4, WeaponsA7E.BRU_42A___3_x_Mk_20_Rockeye)
        BRU_41A___6_x_Mk_20_Rockeye = (4, WeaponsA7E.BRU_41A___6_x_Mk_20_Rockeye)
        GBU_10___2000lb_Laser_Guided_Bomb = (
            4,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (4, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_16___1000lb_Laser_Guided_Bomb = (
            4,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        # ERRR {CBU-99}
        ADM_141A_TALD = (4, Weapons.ADM_141A_TALD)
        SUU_25_x_8_LUU_2___Target_Marker_Flares = (
            4,
            Weapons.SUU_25_x_8_LUU_2___Target_Marker_Flares,
        )
        BRU_33_with_1_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            4,
            Weapons.BRU_33_with_1_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        BRU_33_with_1_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            4,
            Weapons.BRU_33_with_1_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_33_with_1_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT = (
            4,
            Weapons.BRU_33_with_1_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT,
        )
        BRU_33_with_1_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            4,
            Weapons.BRU_33_with_1_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_33_with_2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT = (
            4,
            Weapons.BRU_33_with_2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT,
        )

    class Pylon5:
        F_5_275Gal_Fuel_tank = (5, Weapons.F_5_275Gal_Fuel_tank)
        AIM_9M_Sidewinder_IR_AAM = (5, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (5, Weapons.AIM_9X_Sidewinder_IR_AAM)
        LAU_7_with_AIM_9B_Sidewinder_IR_AAM = (
            5,
            Weapons.LAU_7_with_AIM_9B_Sidewinder_IR_AAM,
        )
        LAU_7_with_AIM_9J_Sidewinder_IR_AAM = (
            5,
            Weapons.LAU_7_with_AIM_9J_Sidewinder_IR_AAM,
        )
        LAU_7_with_AIM_9M_Sidewinder_IR_AAM = (
            5,
            Weapons.LAU_7_with_AIM_9M_Sidewinder_IR_AAM,
        )
        LAU_7_with_AIM_9P_Sidewinder_IR_AAM = (
            5,
            Weapons.LAU_7_with_AIM_9P_Sidewinder_IR_AAM,
        )
        AGM_45A_Shrike_ARM = (5, Weapons.AGM_45A_Shrike_ARM)
        AGM_45B_Shrike_ARM = (5, Weapons.AGM_45B_Shrike_ARM)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile = (
            5,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile,
        )
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            5,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            5,
            Weapons.LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            5,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_117_AGM_65G = (5, Weapons.LAU_117_AGM_65G)
        AGM_84D_Harpoon_AShM = (5, Weapons.AGM_84D_Harpoon_AShM)
        AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile__ = (
            5,
            Weapons.AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile__,
        )
        Mk_82___500lb_GP_Bomb_LD = (5, Weapons.Mk_82___500lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            5,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        _3_Mk_82 = (5, Weapons._3_Mk_82)
        _5_x_Mk_82___500lb_GP_Bombs_LD = (5, Weapons._5_x_Mk_82___500lb_GP_Bombs_LD)
        BRU_41A_with_6_x_Mk_82___500lb_GP_Bomb_LD = (
            5,
            Weapons.BRU_41A_with_6_x_Mk_82___500lb_GP_Bomb_LD,
        )
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (5, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        _3_Mk_82_Snakeye = (5, Weapons._3_Mk_82_Snakeye)
        _5_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            5,
            Weapons._5_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            5,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        BRU_41A___6_x_Mk_82AIR = (5, WeaponsA7E.BRU_41A___6_x_Mk_82AIR)
        Mk_83___1000lb_GP_Bomb_LD = (5, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        MER2_with_2_x_Mk_83___1000lb_GP_Bombs_LD = (
            5,
            Weapons.MER2_with_2_x_Mk_83___1000lb_GP_Bombs_LD,
        )
        BRU_42A___3_x_Mk_83 = (5, WeaponsA7E.BRU_42A___3_x_Mk_83)
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
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            5,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        BRU_33_with_2_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            5,
            Weapons.BRU_33_with_2_x_Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        BRU_42A___3_x_Mk_20_Rockeye = (5, WeaponsA7E.BRU_42A___3_x_Mk_20_Rockeye)
        BRU_41A___6_x_Mk_20_Rockeye = (5, WeaponsA7E.BRU_41A___6_x_Mk_20_Rockeye)
        GBU_10___2000lb_Laser_Guided_Bomb = (
            5,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (5, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_16___1000lb_Laser_Guided_Bomb = (
            5,
            Weapons.GBU_16___1000lb_Laser_Guided_Bomb,
        )
        # ERRR {CBU-99}
        ADM_141A_TALD = (5, Weapons.ADM_141A_TALD)
        SUU_25_x_8_LUU_2___Target_Marker_Flares = (
            5,
            Weapons.SUU_25_x_8_LUU_2___Target_Marker_Flares,
        )
        BRU_33_with_1_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            5,
            Weapons.BRU_33_with_1_x_LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        BRU_33_with_1_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            5,
            Weapons.BRU_33_with_1_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_33_with_1_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT = (
            5,
            Weapons.BRU_33_with_1_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT,
        )
        BRU_33_with_1_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            5,
            Weapons.BRU_33_with_1_x_LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        BRU_33_with_2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT = (
            5,
            Weapons.BRU_33_with_2_x_LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT,
        )

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
