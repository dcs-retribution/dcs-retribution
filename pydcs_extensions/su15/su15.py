from typing import Any, Dict, Set

from dcs import task
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

from game.modsupport import planemod
from pydcs_extensions.weapon_injector import inject_weapons


class WeaponsSu15:
    PTB_600 = {"clsid": "{Su_15_PTB-600}", "name": "PTB-600", "weight": 535}
    R_8M1R = {"clsid": "{R-8M1R}", "name": "R-8M1R", "weight": 285}
    R_8M1T = {"clsid": "{R-8M1T}", "name": "R-8M1T", "weight": 265}
    R_8R_Inert = {"clsid": "{R-8RInert}", "name": "R-8R Inert", "weight": 285}
    R_8T_Inert = {"clsid": "{R-8TInert}", "name": "R-8T Inert", "weight": 265}
    R_98MR = {"clsid": "{R-98MR}", "name": "R-98MR", "weight": 292}
    R_98MT = {"clsid": "{R-98MT}", "name": "R-98MT", "weight": 272}


inject_weapons(WeaponsSu15)


@planemod
class Su_15TM(PlaneType):
    id = "Su_15TM"
    height = 5
    width = 9.34
    length = 21.41
    fuel_max = 5550
    max_speed = 2229.984
    chaff = 30
    flare = 15
    charge_total = 60
    chaff_charge_size = 1
    flare_charge_size = 2
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    livery_name = "SU_15TM"  # from type

    class Pylon1:
        R_98MR = (1, WeaponsSu15.R_98MR)
        R_98MT = (1, WeaponsSu15.R_98MT)
        R_8M1R = (1, WeaponsSu15.R_8M1R)
        R_8M1T = (1, WeaponsSu15.R_8M1T)
        UB_32A_pod___32_x_S_5KO__57mm_UnGd_Rkts__HEAT_Frag = (
            1,
            Weapons.UB_32A_pod___32_x_S_5KO__57mm_UnGd_Rkts__HEAT_Frag,
        )
        UB_16UM_pod___16_x_S_5KO__57mm_UnGd_Rkts__HEAT_Frag = (
            1,
            Weapons.UB_16UM_pod___16_x_S_5KO__57mm_UnGd_Rkts__HEAT_Frag,
        )
        S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk_ = (
            1,
            Weapons.S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk_,
        )
        FAB_100___100kg_GP_Bomb_LD = (1, Weapons.FAB_100___100kg_GP_Bomb_LD)
        FAB_250___250kg_GP_Bomb_LD = (1, Weapons.FAB_250___250kg_GP_Bomb_LD)
        FAB_500_M_62___500kg_GP_Bomb_LD = (1, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)

    class Pylon2:
        APU_60_1M_with_R_60__AA_8_Aphid____IR_AAM = (
            2,
            Weapons.APU_60_1M_with_R_60__AA_8_Aphid____IR_AAM,
        )
        APU_60_1M_with_R_60M__AA_8_Aphid_B____IR_AAM = (
            2,
            Weapons.APU_60_1M_with_R_60M__AA_8_Aphid_B____IR_AAM,
        )

    class Pylon3:
        SPPU_22_1___2_x_23mm__GSh_23L_Autocannon_Pod = (
            3,
            Weapons.SPPU_22_1___2_x_23mm__GSh_23L_Autocannon_Pod,
        )
        PTB_600 = (3, WeaponsSu15.PTB_600)
        UB_32A_pod___32_x_S_5KO__57mm_UnGd_Rkts__HEAT_Frag = (
            3,
            Weapons.UB_32A_pod___32_x_S_5KO__57mm_UnGd_Rkts__HEAT_Frag,
        )
        UB_16UM_pod___16_x_S_5KO__57mm_UnGd_Rkts__HEAT_Frag = (
            3,
            Weapons.UB_16UM_pod___16_x_S_5KO__57mm_UnGd_Rkts__HEAT_Frag,
        )
        S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk_ = (
            3,
            Weapons.S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk_,
        )
        FAB_100___100kg_GP_Bomb_LD = (3, Weapons.FAB_100___100kg_GP_Bomb_LD)
        FAB_250___250kg_GP_Bomb_LD = (3, Weapons.FAB_250___250kg_GP_Bomb_LD)
        FAB_500_M_62___500kg_GP_Bomb_LD = (3, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)

    class Pylon4:
        SPPU_22_1___2_x_23mm__GSh_23L_Autocannon_Pod = (
            4,
            Weapons.SPPU_22_1___2_x_23mm__GSh_23L_Autocannon_Pod,
        )
        PTB_600 = (4, WeaponsSu15.PTB_600)
        UB_32A_pod___32_x_S_5KO__57mm_UnGd_Rkts__HEAT_Frag = (
            4,
            Weapons.UB_32A_pod___32_x_S_5KO__57mm_UnGd_Rkts__HEAT_Frag,
        )
        UB_16UM_pod___16_x_S_5KO__57mm_UnGd_Rkts__HEAT_Frag = (
            4,
            Weapons.UB_16UM_pod___16_x_S_5KO__57mm_UnGd_Rkts__HEAT_Frag,
        )
        S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk_ = (
            4,
            Weapons.S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk_,
        )
        FAB_100___100kg_GP_Bomb_LD = (4, Weapons.FAB_100___100kg_GP_Bomb_LD)
        FAB_250___250kg_GP_Bomb_LD = (4, Weapons.FAB_250___250kg_GP_Bomb_LD)
        FAB_500_M_62___500kg_GP_Bomb_LD = (4, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)

    class Pylon5:
        APU_60_1M_with_R_60__AA_8_Aphid____IR_AAM = (
            5,
            Weapons.APU_60_1M_with_R_60__AA_8_Aphid____IR_AAM,
        )
        APU_60_1M_with_R_60M__AA_8_Aphid_B____IR_AAM = (
            5,
            Weapons.APU_60_1M_with_R_60M__AA_8_Aphid_B____IR_AAM,
        )

    class Pylon6:
        R_98MR = (6, WeaponsSu15.R_98MR)
        R_98MT = (6, WeaponsSu15.R_98MT)
        R_8M1R = (6, WeaponsSu15.R_8M1R)
        R_8M1T = (6, WeaponsSu15.R_8M1T)
        UB_32A_pod___32_x_S_5KO__57mm_UnGd_Rkts__HEAT_Frag = (
            6,
            Weapons.UB_32A_pod___32_x_S_5KO__57mm_UnGd_Rkts__HEAT_Frag,
        )
        UB_16UM_pod___16_x_S_5KO__57mm_UnGd_Rkts__HEAT_Frag = (
            6,
            Weapons.UB_16UM_pod___16_x_S_5KO__57mm_UnGd_Rkts__HEAT_Frag,
        )
        S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk_ = (
            6,
            Weapons.S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk_,
        )
        FAB_100___100kg_GP_Bomb_LD = (6, Weapons.FAB_100___100kg_GP_Bomb_LD)
        FAB_250___250kg_GP_Bomb_LD = (6, Weapons.FAB_250___250kg_GP_Bomb_LD)
        FAB_500_M_62___500kg_GP_Bomb_LD = (6, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6}

    tasks = [
        task.GroundAttack,
        task.CAS,
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
    ]
    task_default = task.Intercept


@planemod
class Su_15(PlaneType):
    id = "Su_15"
    height = 5
    width = 9.34
    length = 21.41
    fuel_max = 5600
    max_speed = 2229.984
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    livery_name = "SU_15"  # from type

    class Pylon1:
        R_8M1R = (1, WeaponsSu15.R_8M1R)
        R_8R_Inert = (1, WeaponsSu15.R_8R_Inert)
        R_8M1T = (1, WeaponsSu15.R_8M1T)
        R_8T_Inert = (1, WeaponsSu15.R_8T_Inert)

    class Pylon2:
        SPPU_22_1___2_x_23mm__GSh_23L_Autocannon_Pod = (
            2,
            Weapons.SPPU_22_1___2_x_23mm__GSh_23L_Autocannon_Pod,
        )
        PTB_600 = (2, WeaponsSu15.PTB_600)

    class Pylon3:
        SPPU_22_1___2_x_23mm__GSh_23L_Autocannon_Pod = (
            3,
            Weapons.SPPU_22_1___2_x_23mm__GSh_23L_Autocannon_Pod,
        )
        PTB_600 = (3, WeaponsSu15.PTB_600)

    class Pylon4:
        R_8M1R = (4, WeaponsSu15.R_8M1R)
        R_8R_Inert = (4, WeaponsSu15.R_8R_Inert)
        R_8M1T = (4, WeaponsSu15.R_8M1T)
        R_8T_Inert = (4, WeaponsSu15.R_8T_Inert)

    pylons: Set[int] = {1, 2, 3, 4}

    tasks = [task.CAP, task.Escort, task.FighterSweep, task.Intercept]
    task_default = task.Intercept
