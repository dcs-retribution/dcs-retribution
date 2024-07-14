from typing import Set

from dcs import task
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

from game.modsupport import planemod
from pydcs_extensions.weapon_injector import inject_weapons


class WeaponsF84G:
    Tank = {"clsid": "{PTB_F84G}", "name": "Tank", "weight": 910}


inject_weapons(WeaponsF84G)


@planemod
class VSN_F84G(PlaneType):
    id = "VSN_F84G"
    flyable = True
    height = 4.496
    width = 11.9
    length = 11.43
    fuel_max = 1282
    max_speed = 964.8
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    livery_name = "VSN_F84G"  # from type

    class Pylon2:
        Tank = (2, WeaponsF84G.Tank)

    class Pylon3:
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (3, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        AIM_9B_Sidewinder_IR_AAM = (3, Weapons.AIM_9B_Sidewinder_IR_AAM)
        Mk_83___1000lb_GP_Bomb_LD = (3, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk1__Practice = (
            3,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_1_HE,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT = (
            3,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_5_HEAT,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice = (
            3,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_61_TP,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            3,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos = (
            3,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice = (
            3,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_WTU_1_B_TP,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum = (
            3,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M257_IL,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M274__Practice_Smk = (
            3,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M274_TP_SM,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk1__Practice = (
            3,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_1_HE,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT = (
            3,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_5_HEAT,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice = (
            3,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_61_TP,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            3,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos = (
            3,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice = (
            3,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_WTU_1_B_TP,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum = (
            3,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_M257_IL,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_M274__Practice_Smk = (
            3,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_M274_TP_SM,
        )
        M117___750lb_GP_Bomb_LD = (3, Weapons.M117___750lb_GP_Bomb_LD)
        AN_M64___500lb_GP_Bomb_LD_ = (3, Weapons.AN_M64___500lb_GP_Bomb_LD_)
        _2_x_HVAR__UnGd_Rkts = (3, Weapons._2_x_HVAR__UnGd_Rkts)
        # ERRR <CLEAN>
        Smoke_Generator___red_ = (3, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (3, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (3, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (3, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (3, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (3, Weapons.Smoke_Generator___orange_)

    class Pylon6:
        Smoke_Generator___red_ = (6, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (6, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (6, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (6, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (6, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (6, Weapons.Smoke_Generator___orange_)

    class Pylon9:
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (9, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        AIM_9B_Sidewinder_IR_AAM = (9, Weapons.AIM_9B_Sidewinder_IR_AAM)
        Mk_83___1000lb_GP_Bomb_LD = (9, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk1__Practice = (
            9,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_1_HE,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT = (
            9,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_5_HEAT,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice = (
            9,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_61_TP,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            9,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos = (
            9,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice = (
            9,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_WTU_1_B_TP,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum = (
            9,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M257_IL,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M274__Practice_Smk = (
            9,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M274_TP_SM,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk1__Practice = (
            9,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_1_HE,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT = (
            9,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_5_HEAT,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice = (
            9,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_61_TP,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            9,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos = (
            9,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice = (
            9,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_WTU_1_B_TP,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum = (
            9,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_M257_IL,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_M274__Practice_Smk = (
            9,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_M274_TP_SM,
        )
        M117___750lb_GP_Bomb_LD = (9, Weapons.M117___750lb_GP_Bomb_LD)
        AN_M64___500lb_GP_Bomb_LD_ = (9, Weapons.AN_M64___500lb_GP_Bomb_LD_)
        _2_x_HVAR__UnGd_Rkts = (9, Weapons._2_x_HVAR__UnGd_Rkts)
        # ERRR <CLEAN>
        Smoke_Generator___red_ = (9, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (9, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (9, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (9, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (9, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (9, Weapons.Smoke_Generator___orange_)

    class Pylon10:
        Tank = (10, WeaponsF84G.Tank)

    pylons: Set[int] = {2, 3, 6, 9, 10}

    tasks = [
        task.CAP,
        task.CAS,
        task.Escort,
        task.FighterSweep,
        task.GroundAttack,
        task.Intercept,
        task.AntishipStrike,
    ]
    task_default = task.GroundAttack
