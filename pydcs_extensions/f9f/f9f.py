from typing import Set

from dcs import task
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

from game.modsupport import planemod


@planemod
class VSN_F9F(PlaneType):
    id = "VSN_F9F"
    flyable = True
    height = 3.73
    width = 11.58
    length = 11.84
    fuel_max = 2310
    max_speed = 961.2
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    livery_name = "VSN_F9F"  # from type

    class Pylon1:
        Smoke_Generator___red_ = (1, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (1, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (1, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (1, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (1, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (1, Weapons.Smoke_Generator___orange_)

    class Pylon2:
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk1__Practice = (
            2,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_1_HE,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT = (
            2,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_5_HEAT,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice = (
            2,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_61_TP,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            2,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos = (
            2,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice = (
            2,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_WTU_1_B_TP,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum = (
            2,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M257_IL,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M274__Practice_Smk = (
            2,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M274_TP_SM,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk1__Practice = (
            2,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_1_HE,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT = (
            2,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_5_HEAT,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice = (
            2,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_61_TP,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            2,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos = (
            2,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice = (
            2,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_WTU_1_B_TP,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum = (
            2,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_M257_IL,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_M274__Practice_Smk = (
            2,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_M274_TP_SM,
        )
        AN_M64___500lb_GP_Bomb_LD_ = (2, Weapons.AN_M64___500lb_GP_Bomb_LD_)
        Mk_82___500lb_GP_Bomb_LD = (2, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_81___250lb_GP_Bomb_LD = (2, Weapons.Mk_81___250lb_GP_Bomb_LD)
        HVAR__UnGd_Rkt = (2, Weapons.HVAR__UnGd_Rkt)
        LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_Mk1__HE = (
            2,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE,
        )
        LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_Mk5__HEAT = (
            2,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT,
        )

    # ERRR <CLEAN>

    class Pylon3:
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
        AN_M64___500lb_GP_Bomb_LD_ = (3, Weapons.AN_M64___500lb_GP_Bomb_LD_)
        Mk_82___500lb_GP_Bomb_LD = (3, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_81___250lb_GP_Bomb_LD = (3, Weapons.Mk_81___250lb_GP_Bomb_LD)
        HVAR__UnGd_Rkt = (3, Weapons.HVAR__UnGd_Rkt)
        LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_Mk1__HE = (
            3,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE,
        )
        LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_Mk5__HEAT = (
            3,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT,
        )

    # ERRR <CLEAN>

    class Pylon4:
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk1__Practice = (
            4,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_1_HE,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT = (
            4,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_5_HEAT,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice = (
            4,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_61_TP,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            4,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos = (
            4,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice = (
            4,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_WTU_1_B_TP,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum = (
            4,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M257_IL,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M274__Practice_Smk = (
            4,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M274_TP_SM,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk1__Practice = (
            4,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_1_HE,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT = (
            4,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_5_HEAT,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice = (
            4,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_61_TP,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            4,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos = (
            4,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice = (
            4,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_WTU_1_B_TP,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum = (
            4,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_M257_IL,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_M274__Practice_Smk = (
            4,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_M274_TP_SM,
        )
        AN_M64___500lb_GP_Bomb_LD_ = (4, Weapons.AN_M64___500lb_GP_Bomb_LD_)
        Mk_82___500lb_GP_Bomb_LD = (4, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_81___250lb_GP_Bomb_LD = (4, Weapons.Mk_81___250lb_GP_Bomb_LD)
        HVAR__UnGd_Rkt = (4, Weapons.HVAR__UnGd_Rkt)
        LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_Mk1__HE = (
            4,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE,
        )
        LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_Mk5__HEAT = (
            4,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT,
        )

    # ERRR <CLEAN>

    class Pylon5:
        AIM_9B_Sidewinder_IR_AAM = (5, Weapons.AIM_9B_Sidewinder_IR_AAM)
        Mk_83___1000lb_GP_Bomb_LD = (5, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk1__Practice = (
            5,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_1_HE,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT = (
            5,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_5_HEAT,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice = (
            5,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_61_TP,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            5,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos = (
            5,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice = (
            5,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_WTU_1_B_TP,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum = (
            5,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M257_IL,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M274__Practice_Smk = (
            5,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M274_TP_SM,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk1__Practice = (
            5,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_1_HE,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT = (
            5,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_5_HEAT,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice = (
            5,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_61_TP,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            5,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos = (
            5,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice = (
            5,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_WTU_1_B_TP,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum = (
            5,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_M257_IL,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_M274__Practice_Smk = (
            5,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_M274_TP_SM,
        )
        M117___750lb_GP_Bomb_LD = (5, Weapons.M117___750lb_GP_Bomb_LD)
        AN_M64___500lb_GP_Bomb_LD_ = (5, Weapons.AN_M64___500lb_GP_Bomb_LD_)
        Mk_82___500lb_GP_Bomb_LD = (5, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_81___250lb_GP_Bomb_LD = (5, Weapons.Mk_81___250lb_GP_Bomb_LD)
        HVAR__UnGd_Rkt = (5, Weapons.HVAR__UnGd_Rkt)
        # ERRR <CLEAN>
        Smoke_Generator___red_ = (5, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (5, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (5, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (5, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (5, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (5, Weapons.Smoke_Generator___orange_)

    class Pylon6:
        Smoke_Generator___red_ = (6, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (6, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (6, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (6, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (6, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (6, Weapons.Smoke_Generator___orange_)

    class Pylon7:
        AIM_9B_Sidewinder_IR_AAM = (7, Weapons.AIM_9B_Sidewinder_IR_AAM)
        Mk_83___1000lb_GP_Bomb_LD = (7, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk1__Practice = (
            7,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_1_HE,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT = (
            7,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_5_HEAT,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice = (
            7,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_61_TP,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            7,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos = (
            7,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice = (
            7,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_WTU_1_B_TP,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum = (
            7,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M257_IL,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M274__Practice_Smk = (
            7,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M274_TP_SM,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk1__Practice = (
            7,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_1_HE,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT = (
            7,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_5_HEAT,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice = (
            7,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_61_TP,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            7,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos = (
            7,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice = (
            7,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_WTU_1_B_TP,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum = (
            7,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_M257_IL,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_M274__Practice_Smk = (
            7,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_M274_TP_SM,
        )
        M117___750lb_GP_Bomb_LD = (7, Weapons.M117___750lb_GP_Bomb_LD)
        AN_M64___500lb_GP_Bomb_LD_ = (7, Weapons.AN_M64___500lb_GP_Bomb_LD_)
        Mk_82___500lb_GP_Bomb_LD = (7, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_81___250lb_GP_Bomb_LD = (7, Weapons.Mk_81___250lb_GP_Bomb_LD)
        HVAR__UnGd_Rkt = (7, Weapons.HVAR__UnGd_Rkt)
        # ERRR <CLEAN>
        Smoke_Generator___red_ = (7, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (7, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (7, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (7, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (7, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (7, Weapons.Smoke_Generator___orange_)

    class Pylon8:
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk1__Practice = (
            8,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_1_HE,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT = (
            8,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_5_HEAT,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice = (
            8,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_61_TP,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            8,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos = (
            8,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice = (
            8,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_WTU_1_B_TP,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum = (
            8,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M257_IL,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M274__Practice_Smk = (
            8,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M274_TP_SM,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk1__Practice = (
            8,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_1_HE,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT = (
            8,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_5_HEAT,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice = (
            8,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_61_TP,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            8,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos = (
            8,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice = (
            8,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_WTU_1_B_TP,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum = (
            8,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_M257_IL,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_M274__Practice_Smk = (
            8,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_M274_TP_SM,
        )
        AN_M64___500lb_GP_Bomb_LD_ = (8, Weapons.AN_M64___500lb_GP_Bomb_LD_)
        Mk_82___500lb_GP_Bomb_LD = (8, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_81___250lb_GP_Bomb_LD = (8, Weapons.Mk_81___250lb_GP_Bomb_LD)
        HVAR__UnGd_Rkt = (8, Weapons.HVAR__UnGd_Rkt)
        LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_Mk1__HE = (
            8,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE,
        )
        LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_Mk5__HEAT = (
            8,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT,
        )

    # ERRR <CLEAN>

    class Pylon9:
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
        AN_M64___500lb_GP_Bomb_LD_ = (9, Weapons.AN_M64___500lb_GP_Bomb_LD_)
        Mk_82___500lb_GP_Bomb_LD = (9, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_81___250lb_GP_Bomb_LD = (9, Weapons.Mk_81___250lb_GP_Bomb_LD)
        HVAR__UnGd_Rkt = (9, Weapons.HVAR__UnGd_Rkt)
        LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_Mk1__HE = (
            9,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE,
        )
        LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_Mk5__HEAT = (
            9,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT,
        )

    # ERRR <CLEAN>

    class Pylon10:
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk1__Practice = (
            10,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_1_HE,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT = (
            10,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_5_HEAT,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice = (
            10,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_61_TP,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            10,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos = (
            10,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice = (
            10,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_WTU_1_B_TP,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum = (
            10,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M257_IL,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M274__Practice_Smk = (
            10,
            Weapons.LAU_68___7_x_UnGd_Rkts__70_mm_Hydra_70_M274_TP_SM,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk1__Practice = (
            10,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_1_HE,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT = (
            10,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_5_HEAT,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk61__Practice = (
            10,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_Mk_61_TP,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            10,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos = (
            10,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_WTU_1_B__Practice = (
            10,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_WTU_1_B_TP,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum = (
            10,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_M257_IL,
        )
        LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_M274__Practice_Smk = (
            10,
            Weapons.LAU_131___7_x_UnGd_Rkts__70_mm_Hydra_70_M274_TP_SM,
        )
        AN_M64___500lb_GP_Bomb_LD_ = (10, Weapons.AN_M64___500lb_GP_Bomb_LD_)
        Mk_82___500lb_GP_Bomb_LD = (10, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_81___250lb_GP_Bomb_LD = (10, Weapons.Mk_81___250lb_GP_Bomb_LD)
        HVAR__UnGd_Rkt = (10, Weapons.HVAR__UnGd_Rkt)
        LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_Mk1__HE = (
            10,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_1_HE,
        )
        LAU_3_pod___19_x_2_75_FFAR__UnGd_Rkts_Mk5__HEAT = (
            10,
            Weapons.LAU_3___19_x_UnGd_Rkts__70_mm_Mk_4_FFAR_Mk_5_HEAT,
        )

    # ERRR <CLEAN>

    class Pylon11:
        Smoke_Generator___red_ = (11, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (11, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (11, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (11, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (11, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (11, Weapons.Smoke_Generator___orange_)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}

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
