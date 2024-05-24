from typing import Set

from dcs import task
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

from game.modsupport import planemod
from pydcs_extensions import inject_weapons


class WeaponsA7E:
    Mk_77_Mod_0 = {"clsid": "{Mk77_mod0}", "name": "Mk-77 Mod 0", "weight": 340}
    Mk_77_Mod_5 = {"clsid": "{Mk77_mod5}", "name": "Mk-77 Mod 5", "weight": 230}
    Mk_83AIR = {"clsid": "{Mk83AIR}", "name": "Mk-83AIR", "weight": 454}
    CBU_99_Mod_6 = {"clsid": "{CBU99_mod6}", "name": "CBU-99 Mod 6", "weight": 222}
    BRU_41A_with_6_x_BDU_33___25lb_Practice_Bomb_LD = {
        "clsid": "{BRU41_6X_BDU-33}",
        "name": "BRU-41A with 6 x BDU-33 - 25lb Practice Bomb LD",
        "weight": 195.713,
    }
    BRU_41A_with_6_x_Mk_82___500lb_GP_Bomb_LD = {
        "clsid": "{BRU41_6X_MK-82}",
        "name": "BRU-41A with 6 x Mk-82 - 500lb GP Bomb LD",
        "weight": 1495.913,
    }
    BRU_41A___4_x_BDU_33 = {
        "clsid": "{BRU41A_4_L*BDU33}",
        "name": "BRU-41A - 4 x BDU-33",
        "weight": 173.113,
    }
    BRU_41A___4_x_BDU_33_ = {
        "clsid": "{BRU41A_4_R*BDU33}",
        "name": "BRU-41A - 4 x BDU-33",
        "weight": 173.113,
    }
    BRU_41A___4_x_CBU_52B = {
        "clsid": "{BRU41A_4_L*CBU52B}",
        "name": "BRU-41A - 4 x CBU-52B",
        "weight": 1551.913,
    }
    BRU_41A___4_x_CBU_52B_ = {
        "clsid": "{BRU41A_4_R*CBU52B}",
        "name": "BRU-41A - 4 x CBU-52B",
        "weight": 1551.913,
    }
    BRU_41A___4_x_CBU_99 = {
        "clsid": "{BRU41A_4_L*CBU99_mod6}",
        "name": "BRU-41A - 4 x CBU-99",
        "weight": 1015.913,
    }
    BRU_41A___4_x_CBU_99_ = {
        "clsid": "{BRU41A_4_R*CBU99_mod6}",
        "name": "BRU-41A - 4 x CBU-99",
        "weight": 1015.913,
    }
    BRU_41A___4_x_Mk_20_Rockeye = {
        "clsid": "{BRU41A_4_L*MK20_ROCKEYE}",
        "name": "BRU-41A - 4 x Mk-20 Rockeye",
        "weight": 1015.913,
    }
    BRU_41A___4_x_Mk_20_Rockeye_ = {
        "clsid": "{BRU41A_4_R*MK20_ROCKEYE}",
        "name": "BRU-41A - 4 x Mk-20 Rockeye",
        "weight": 1015.913,
    }
    BRU_41A___4_x_Mk_81 = {
        "clsid": "{BRU41A_4_L*MK81}",
        "name": "BRU-41A - 4 x Mk-81",
        "weight": 599.913,
    }
    BRU_41A___4_x_Mk_81_ = {
        "clsid": "{BRU41A_4_R*MK81}",
        "name": "BRU-41A - 4 x Mk-81",
        "weight": 599.913,
    }
    BRU_41A___4_x_Mk_82 = {
        "clsid": "{BRU41A_4_L*MK82}",
        "name": "BRU-41A - 4 x Mk-82",
        "weight": 1091.913,
    }
    BRU_41A___4_x_Mk_82AIR = {
        "clsid": "{BRU41A_4_L*MK82AIR}",
        "name": "BRU-41A - 4 x Mk-82AIR",
        "weight": 1055.913,
    }
    BRU_41A___4_x_Mk_82AIR_ = {
        "clsid": "{BRU41A_4_R*MK82AIR}",
        "name": "BRU-41A - 4 x Mk-82AIR",
        "weight": 1055.913,
    }
    BRU_41A___4_x_Mk_82_ = {
        "clsid": "{BRU41A_4_R*MK82}",
        "name": "BRU-41A - 4 x Mk-82",
        "weight": 1091.913,
    }
    BRU_41A___4_x_Mk_82_Snakeye = {
        "clsid": "{BRU41A_4_L*MK82_SNAKEYE}",
        "name": "BRU-41A - 4 x Mk-82 Snakeye",
        "weight": 1055.913,
    }
    BRU_41A___4_x_Mk_82_Snakeye_ = {
        "clsid": "{BRU41A_4_R*MK82_SNAKEYE}",
        "name": "BRU-41A - 4 x Mk-82 Snakeye",
        "weight": 1055.913,
    }
    BRU_41A___6_x_BDU_33 = {
        "clsid": "{BRU41A_6*BDU33}",
        "name": "BRU-41A - 6 x BDU-33",
        "weight": 195.713,
    }
    BRU_41A___6_x_CBU_52B = {
        "clsid": "{BRU41A_6*CBU52B}",
        "name": "BRU-41A - 6 x CBU-52B",
        "weight": 2263.913,
    }
    BRU_41A___6_x_CBU_99 = {
        "clsid": "{BRU41A_6*CBU99_mod6}",
        "name": "BRU-41A - 6 x CBU-99",
        "weight": 1459.913,
    }
    BRU_41A___6_x_Mk_20_Rockeye = {
        "clsid": "{BRU41A_6*MK20_ROCKEYE}",
        "name": "BRU-41A - 6 x Mk-20 Rockeye",
        "weight": 1459.913,
    }
    BRU_41A___6_x_Mk_81 = {
        "clsid": "{BRU41A_6*MK81}",
        "name": "BRU-41A - 6 x Mk-81",
        "weight": 835.913,
    }
    BRU_41A___6_x_Mk_82 = {
        "clsid": "{BRU41A_6*MK82}",
        "name": "BRU-41A - 6 x Mk-82",
        "weight": 1573.913,
    }
    BRU_41A___6_x_Mk_82AIR = {
        "clsid": "{BRU41A_6*MK82AIR}",
        "name": "BRU-41A - 6 x Mk-82AIR",
        "weight": 1519.913,
    }
    BRU_41A___6_x_Mk_82_Snakeye = {
        "clsid": "{BRU41A_6*MK82_SNAKEYE}",
        "name": "BRU-41A - 6 x Mk-82 Snakeye",
        "weight": 1519.913,
    }
    BRU_42A___2_x_BDU_33 = {
        "clsid": "{BRU42A_2_L*BDU33}",
        "name": "BRU-42A - 2 x BDU-33",
        "weight": 82.6,
    }
    BRU_42A___2_x_BDU_33_ = {
        "clsid": "{BRU42A_2_R*BDU33}",
        "name": "BRU-42A - 2 x BDU-33",
        "weight": 82.6,
    }
    BRU_42A___2_x_CBU_52B = {
        "clsid": "{BRU42A_2_L*CBU52B}",
        "name": "BRU-42A - 2 x CBU-52B",
        "weight": 772,
    }
    BRU_42A___2_x_CBU_52B_ = {
        "clsid": "{BRU42A_2_R*CBU52B}",
        "name": "BRU-42A - 2 x CBU-52B",
        "weight": 772,
    }
    BRU_42A___2_x_CBU_87 = {
        "clsid": "{BRU42A_2_L*CBU87}",
        "name": "BRU-42A - 2 x CBU-87",
        "weight": 920,
    }
    BRU_42A___2_x_CBU_87_ = {
        "clsid": "{BRU42A_2_R*CBU87}",
        "name": "BRU-42A - 2 x CBU-87",
        "weight": 920,
    }
    BRU_42A___2_x_CBU_97 = {
        "clsid": "{BRU42A_2_L*CBU97}",
        "name": "BRU-42A - 2 x CBU-97",
        "weight": 894,
    }
    BRU_42A___2_x_CBU_97_ = {
        "clsid": "{BRU42A_2_R*CBU97}",
        "name": "BRU-42A - 2 x CBU-97",
        "weight": 894,
    }
    BRU_42A___2_x_CBU_99 = {
        "clsid": "{BRU42A_2_L*CBU99_mod6}",
        "name": "BRU-42A - 2 x CBU-99",
        "weight": 504,
    }
    BRU_42A___2_x_CBU_99_ = {
        "clsid": "{BRU42A_2_R*CBU99_mod6}",
        "name": "BRU-42A - 2 x CBU-99",
        "weight": 504,
    }
    BRU_42A___2_x_GBU_12 = {
        "clsid": "{BRU42A_2_L*GBU12}",
        "name": "BRU-42A - 2 x GBU-12",
        "weight": 610,
    }
    BRU_42A___2_x_GBU_12_ = {
        "clsid": "{BRU42A_2_R*GBU12}",
        "name": "BRU-42A - 2 x GBU-12",
        "weight": 610,
    }
    BRU_42A___2_x_LAU_10___4_ZUNI_Mk_71 = {
        "clsid": "{BRU42A_2_L*LAU10_ZUNI_MK71}",
        "name": "BRU-42A - 2 x LAU-10 - 4 ZUNI Mk 71",
        "weight": 940,
    }
    BRU_42A___2_x_LAU_10___4_ZUNI_Mk_71_ = {
        "clsid": "{BRU42A_2_R*LAU10_ZUNI_MK71}",
        "name": "BRU-42A - 2 x LAU-10 - 4 ZUNI Mk 71",
        "weight": 940,
    }
    BRU_42A___2_x_LAU_61___19_2_75__rockets_M151_HE = {
        "clsid": "{BRU42A_2_L*LAU61_HYDRA_M151HE}",
        "name": "BRU-42A - 2 x LAU-61 - 19 2.75' rockets M151 HE",
        "weight": 641.18,
    }
    BRU_42A___2_x_LAU_61___19_2_75__rockets_M151_HE_ = {
        "clsid": "{BRU42A_2_R*LAU61_HYDRA_M151HE}",
        "name": "BRU-42A - 2 x LAU-61 - 19 2.75' rockets M151 HE",
        "weight": 641.18,
    }
    BRU_42A___2_x_LAU_68___7_2_75__rockets_M151_HE = {
        "clsid": "{BRU42A_2_L*LAU68_HYDRA_M151HE}",
        "name": "BRU-42A - 2 x LAU-68 - 7 2.75' rockets M151 HE",
        "weight": 289.06,
    }
    BRU_42A___2_x_LAU_68___7_2_75__rockets_M151_HE_ = {
        "clsid": "{BRU42A_2_R*LAU68_HYDRA_M151HE}",
        "name": "BRU-42A - 2 x LAU-68 - 7 2.75' rockets M151 HE",
        "weight": 289.06,
    }
    BRU_42A___2_x_LAU_68___7_2_75__rockets_M156_WP = {
        "clsid": "{BRU42A_2_L*LAU68_HYDRA_M156WP}",
        "name": "BRU-42A - 2 x LAU-68 - 7 2.75' rockets M156 WP",
        "weight": 291.58,
    }
    BRU_42A___2_x_LAU_68___7_2_75__rockets_M156_WP_ = {
        "clsid": "{BRU42A_2_R*LAU68_HYDRA_M156WP}",
        "name": "BRU-42A - 2 x LAU-68 - 7 2.75' rockets M156 WP",
        "weight": 291.58,
    }
    BRU_42A___2_x_LAU_68___7_2_75__rockets_M257 = {
        "clsid": "{BRU42A_2_L*LAU68_HYDRA_M257}",
        "name": "BRU-42A - 2 x LAU-68 - 7 2.75' rockets M257",
        "weight": 300.26,
    }
    BRU_42A___2_x_LAU_68___7_2_75__rockets_M257_ = {
        "clsid": "{BRU42A_2_R*LAU68_HYDRA_M257}",
        "name": "BRU-42A - 2 x LAU-68 - 7 2.75' rockets M257",
        "weight": 300.26,
    }
    BRU_42A___2_x_LAU_68___7_2_75__rockets_Mk5_HEAT = {
        "clsid": "{BRU42A_2_L*LAU68_HYDRA_MK5HEAT}",
        "name": "BRU-42A - 2 x LAU-68 - 7 2.75' rockets Mk5 HEAT",
        "weight": 266.4,
    }
    BRU_42A___2_x_LAU_68___7_2_75__rockets_Mk5_HEAT_ = {
        "clsid": "{BRU42A_2_R*LAU68_HYDRA_MK5HEAT}",
        "name": "BRU-42A - 2 x LAU-68 - 7 2.75' rockets Mk5 HEAT",
        "weight": 266.4,
    }
    BRU_42A___2_x_M117 = {
        "clsid": "{BRU42A_2_L*M117}",
        "name": "BRU-42A - 2 x M117",
        "weight": 740,
    }
    BRU_42A___2_x_M117_ = {
        "clsid": "{BRU42A_2_R*M117}",
        "name": "BRU-42A - 2 x M117",
        "weight": 740,
    }
    BRU_42A___2_x_Mk_20_Rockeye = {
        "clsid": "{BRU42A_2_L*MK20_ROCKEYE}",
        "name": "BRU-42A - 2 x Mk-20 Rockeye",
        "weight": 504,
    }
    BRU_42A___2_x_Mk_20_Rockeye_ = {
        "clsid": "{BRU42A_2_R*MK20_ROCKEYE}",
        "name": "BRU-42A - 2 x Mk-20 Rockeye",
        "weight": 504,
    }
    BRU_42A___2_x_Mk_81 = {
        "clsid": "{BRU42A_2_L*MK81}",
        "name": "BRU-42A - 2 x Mk-81",
        "weight": 296,
    }
    BRU_42A___2_x_Mk_81_ = {
        "clsid": "{BRU42A_2_R*MK81}",
        "name": "BRU-42A - 2 x Mk-81",
        "weight": 296,
    }
    BRU_42A___2_x_Mk_82 = {
        "clsid": "{BRU42A_2_L*MK82}",
        "name": "BRU-42A - 2 x Mk-82",
        "weight": 542,
    }
    BRU_42A___2_x_Mk_82AIR = {
        "clsid": "{BRU42A_2_L*MK82AIR}",
        "name": "BRU-42A - 2 x Mk-82AIR",
        "weight": 524,
    }
    BRU_42A___2_x_Mk_82AIR_ = {
        "clsid": "{BRU42A_2_R*MK82AIR}",
        "name": "BRU-42A - 2 x Mk-82AIR",
        "weight": 524,
    }
    BRU_42A___2_x_Mk_82_ = {
        "clsid": "{BRU42A_2_R*MK82}",
        "name": "BRU-42A - 2 x Mk-82",
        "weight": 542,
    }
    BRU_42A___2_x_Mk_82_Snakeye = {
        "clsid": "{BRU42A_2_L*MK82_SNAKEYE}",
        "name": "BRU-42A - 2 x Mk-82 Snakeye",
        "weight": 524,
    }
    BRU_42A___2_x_Mk_82_Snakeye_ = {
        "clsid": "{BRU42A_2_R*MK82_SNAKEYE}",
        "name": "BRU-42A - 2 x Mk-82 Snakeye",
        "weight": 524,
    }
    BRU_42A___2_x_Mk_83 = {
        "clsid": "{BRU42A_2_L*MK83}",
        "name": "BRU-42A - 2 x Mk-83",
        "weight": 954,
    }
    BRU_42A___2_x_Mk_83AIR = {
        "clsid": "{BRU42A_2_L*MK83AIR}",
        "name": "BRU-42A - 2 x Mk-83AIR",
        "weight": 968,
    }
    BRU_42A___2_x_Mk_83AIR_ = {
        "clsid": "{BRU42A_2_R*MK83AIR}",
        "name": "BRU-42A - 2 x Mk-83AIR",
        "weight": 968,
    }
    BRU_42A___2_x_Mk_83_ = {
        "clsid": "{BRU42A_2_R*MK83}",
        "name": "BRU-42A - 2 x Mk-83",
        "weight": 954,
    }
    BRU_42A___3_x_BDU_33 = {
        "clsid": "{BRU42A_3*BDU33}",
        "name": "BRU-42A - 3 x BDU-33",
        "weight": 93.9,
    }
    BRU_42A___3_x_CBU_52B = {
        "clsid": "{BRU42A_3*CBU52B}",
        "name": "BRU-42A - 3 x CBU-52B",
        "weight": 1128,
    }
    BRU_42A___3_x_CBU_99 = {
        "clsid": "{BRU42A_3*CBU99_mod6}",
        "name": "BRU-42A - 3 x CBU-99",
        "weight": 726,
    }
    BRU_42A___3_x_LAU_10___4_ZUNI_Mk_71 = {
        "clsid": "{BRU42A_3*LAU10_ZUNI_MK71}",
        "name": "BRU-42A - 3 x LAU-10 - 4 ZUNI Mk 71",
        "weight": 1380,
    }
    BRU_42A___3_x_LAU_3___19_2_75__rockets_M151_HE = {
        "clsid": "{BRU42A_3*LAU3_HYDRA_MK1HE}",
        "name": "BRU-42A - 3 x LAU-3 - 19 2.75' rockets M151 HE",
        "weight": 915.9,
    }
    BRU_42A___3_x_LAU_3___19_2_75__rockets_M156_WP = {
        "clsid": "{BRU42A_3*LAU3_HYDRA_M156WP}",
        "name": "BRU-42A - 3 x LAU-3 - 19 2.75' rockets M156 WP",
        "weight": 998.7,
    }
    BRU_42A___3_x_LAU_3___19_2_75__rockets_Mk5_HEAT = {
        "clsid": "{BRU42A_3*LAU3_HYDRA_MK5HEAT}",
        "name": "BRU-42A - 3 x LAU-3 - 19 2.75' rockets Mk5 HEAT",
        "weight": 918.6,
    }
    BRU_42A___3_x_LAU_61___19_2_75__rockets_M151_HE = {
        "clsid": "{BRU42A_3*LAU61_HYDRA_M151HE}",
        "name": "BRU-42A - 3 x LAU-61 - 19 2.75' rockets M151 HE",
        "weight": 931.77,
    }
    BRU_42A___3_x_LAU_68___7_2_75__rockets_M151_HE = {
        "clsid": "{BRU42A_3*LAU68_HYDRA_M151HE}",
        "name": "BRU-42A - 3 x LAU-68 - 7 2.75' rockets M151 HE",
        "weight": 403.59,
    }
    BRU_42A___3_x_LAU_68___7_2_75__rockets_M156_WP = {
        "clsid": "{BRU42A_3*LAU68_HYDRA_M156WP}",
        "name": "BRU-42A - 3 x LAU-68 - 7 2.75' rockets M156 WP",
        "weight": 407.37,
    }
    BRU_42A___3_x_LAU_68___7_2_75__rockets_M257 = {
        "clsid": "{BRU42A_3*LAU68_HYDRA_M257}",
        "name": "BRU-42A - 3 x LAU-68 - 7 2.75' rockets M257",
        "weight": 420.39,
    }
    BRU_42A___3_x_LAU_68___7_2_75__rockets_Mk5_HEAT = {
        "clsid": "{BRU42A_3*LAU68_HYDRA_MK5HEAT}",
        "name": "BRU-42A - 3 x LAU-68 - 7 2.75' rockets Mk5 HEAT",
        "weight": 369.6,
    }
    BRU_42A___3_x_M117 = {
        "clsid": "{BRU42A_3*M117}",
        "name": "BRU-42A - 3 x M117",
        "weight": 1080,
    }
    BRU_42A___3_x_Mk_20_Rockeye = {
        "clsid": "{BRU42A_3*MK20_ROCKEYE}",
        "name": "BRU-42A - 3 x Mk-20 Rockeye",
        "weight": 726,
    }
    BRU_42A___3_x_Mk_81 = {
        "clsid": "{BRU42A_3*MK81}",
        "name": "BRU-42A - 3 x Mk-81",
        "weight": 414,
    }
    BRU_42A___3_x_Mk_82 = {
        "clsid": "{BRU42A_3*MK82}",
        "name": "BRU-42A - 3 x Mk-82",
        "weight": 783,
    }
    BRU_42A___3_x_Mk_82AIR = {
        "clsid": "{BRU42A_3*MK82AIR}",
        "name": "BRU-42A - 3 x Mk-82AIR",
        "weight": 756,
    }
    BRU_42A___3_x_Mk_82_Snakeye = {
        "clsid": "{BRU42A_3*MK82_SNAKEYE}",
        "name": "BRU-42A - 3 x Mk-82 Snakeye",
        "weight": 756,
    }
    BRU_42A___3_x_Mk_83 = {
        "clsid": "{BRU42A_3*MK83}",
        "name": "BRU-42A - 3 x Mk-83",
        "weight": 1401,
    }
    BRU_42A___3_x_Mk_83AIR = {
        "clsid": "{BRU42A_3*MK83AIR}",
        "name": "BRU-42A - 3 x Mk-83AIR",
        "weight": 1422,
    }
    AN_ALQ_81_ECM_Pod = {
        "clsid": "{ALQ_81}",
        "name": "AN/ALQ-81 ECM Pod",
        "weight": 143.789,
    }
    AERO_1D_300_Gallons_Fuel_Tank_ = {
        "clsid": "{AV8BNA_AERO1D}",
        "name": "AERO 1D 300 Gallons Fuel Tank ",
        "weight": 998.3513,
    }
    AERO_1D_300_Gallons_Fuel_Tank__ = {
        "clsid": "{A7E_AERO1D}",
        "name": "AERO 1D 300 Gallons Fuel Tank ",
        "weight": 1002.439,
    }
    AERO_1D_300_Gallons_Fuel_Tank__Empty_ = {
        "clsid": "{AV8BNA_AERO1D_EMPTY}",
        "name": "AERO 1D 300 Gallons Fuel Tank (Empty)",
        "weight": 89.8113,
    }
    AERO_1D_300_Gallons_Fuel_Tank__Empty__ = {
        "clsid": "{A7E_AERO1D_EMPTY}",
        "name": "AERO 1D 300 Gallons Fuel Tank (Empty)",
        "weight": 103.89362,
    }
    GPU_5A_Gunpod = {"clsid": "{GPU_5A}", "name": "GPU-5A Gunpod", "weight": 866.158}
    AN_AAR_45_FLIR_Pod = {
        "clsid": "{AAR_45}",
        "name": "AN/AAR-45 FLIR Pod",
        "weight": 327,
    }


inject_weapons(WeaponsA7E)


@planemod
class A_7E(PlaneType):
    id = "A-7E"
    flyable = True
    height = 4.9
    width = 11.8
    length = 14.06
    fuel_max = 4552
    max_speed = 972
    chaff = 90
    flare = 90
    charge_total = 180
    chaff_charge_size = 1
    flare_charge_size = 2
    category = "Air"  # {C168A850-3C0B-436a-95B5-C4A015552560}
    radio_frequency = 124

    livery_name = "A-7E"  # from type

    class Pylon1:
        AGM_62_Walleye_II___Guided_Weapon_Mk_5__TV_Guided_ = (
            1,
            Weapons.AGM_62_Walleye_II___Guided_Weapon_Mk_5__TV_Guided_,
        )
        LAU_118A___AGM_45B_Shrike_ARM = (
            1,
            Weapons.LAU_118A___AGM_45B_Shrike_ARM,
        )
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            1,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        Mk_77_Mod_0 = (1, WeaponsA7E.Mk_77_Mod_0)
        Mk_77_Mod_5 = (1, WeaponsA7E.Mk_77_Mod_5)
        Mk_82___500lb_GP_Bomb_LD = (1, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (1, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            1,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (1, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        Mk_83AIR = (1, WeaponsA7E.Mk_83AIR)
        Mk_84___2000lb_GP_Bomb_LD = (1, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (1, Weapons.M117___750lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            1,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        CBU_52B___220_x_HE_Frag_bomblets = (1, Weapons.CBU_52B___220_x_HE_Frag_bomblets)
        CBU_87___202_x_CEM_Cluster_Bomb = (1, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (1, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        CBU_99_Mod_6 = (1, WeaponsA7E.CBU_99_Mod_6)
        GBU_10___2000lb_Laser_Guided_Bomb = (
            1,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (1, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        BRU_42A___2_x_Mk_81 = (1, WeaponsA7E.BRU_42A___2_x_Mk_81)
        BRU_42A___2_x_Mk_82 = (1, WeaponsA7E.BRU_42A___2_x_Mk_82)
        BRU_42A___2_x_Mk_82AIR = (1, WeaponsA7E.BRU_42A___2_x_Mk_82AIR)
        BRU_42A___2_x_Mk_82_Snakeye = (1, WeaponsA7E.BRU_42A___2_x_Mk_82_Snakeye)
        BRU_42A___2_x_Mk_83 = (1, WeaponsA7E.BRU_42A___2_x_Mk_83)
        BRU_42A___2_x_M117 = (1, WeaponsA7E.BRU_42A___2_x_M117)
        BRU_42A___2_x_Mk_20_Rockeye = (1, WeaponsA7E.BRU_42A___2_x_Mk_20_Rockeye)
        BRU_42A___2_x_CBU_52B = (1, WeaponsA7E.BRU_42A___2_x_CBU_52B)
        BRU_42A___2_x_CBU_87 = (1, WeaponsA7E.BRU_42A___2_x_CBU_87)
        BRU_42A___2_x_CBU_97 = (1, WeaponsA7E.BRU_42A___2_x_CBU_97)
        BRU_42A___2_x_CBU_99 = (1, WeaponsA7E.BRU_42A___2_x_CBU_99)
        BRU_42A___3_x_Mk_81 = (1, WeaponsA7E.BRU_42A___3_x_Mk_81)
        BRU_42A___3_x_Mk_82 = (1, WeaponsA7E.BRU_42A___3_x_Mk_82)
        BRU_42A___3_x_Mk_82AIR = (1, WeaponsA7E.BRU_42A___3_x_Mk_82AIR)
        BRU_42A___3_x_Mk_82_Snakeye = (1, WeaponsA7E.BRU_42A___3_x_Mk_82_Snakeye)
        BRU_42A___3_x_Mk_83 = (1, WeaponsA7E.BRU_42A___3_x_Mk_83)
        BRU_42A___3_x_Mk_83AIR = (1, WeaponsA7E.BRU_42A___3_x_Mk_83AIR)
        BRU_42A___3_x_M117 = (1, WeaponsA7E.BRU_42A___3_x_M117)
        BRU_42A___3_x_Mk_20_Rockeye = (1, WeaponsA7E.BRU_42A___3_x_Mk_20_Rockeye)
        BRU_42A___3_x_CBU_52B = (1, WeaponsA7E.BRU_42A___3_x_CBU_52B)
        BRU_42A___3_x_CBU_99 = (1, WeaponsA7E.BRU_42A___3_x_CBU_99)
        BRU_42A___3_x_BDU_33 = (1, WeaponsA7E.BRU_42A___3_x_BDU_33)
        BRU_41A___4_x_Mk_81 = (1, WeaponsA7E.BRU_41A___4_x_Mk_81)
        BRU_41A___4_x_Mk_82 = (1, WeaponsA7E.BRU_41A___4_x_Mk_82)
        BRU_41A___4_x_Mk_82AIR = (1, WeaponsA7E.BRU_41A___4_x_Mk_82AIR)
        BRU_41A___4_x_Mk_82_Snakeye = (1, WeaponsA7E.BRU_41A___4_x_Mk_82_Snakeye)
        BRU_41A___4_x_Mk_20_Rockeye = (1, WeaponsA7E.BRU_41A___4_x_Mk_20_Rockeye)
        BRU_41A___4_x_CBU_52B = (1, WeaponsA7E.BRU_41A___4_x_CBU_52B)
        BRU_41A___4_x_CBU_99 = (1, WeaponsA7E.BRU_41A___4_x_CBU_99)
        BRU_41A___6_x_Mk_81 = (1, WeaponsA7E.BRU_41A___6_x_Mk_81)
        BRU_41A___6_x_Mk_82 = (1, WeaponsA7E.BRU_41A___6_x_Mk_82)
        BRU_41A___6_x_Mk_82AIR = (1, WeaponsA7E.BRU_41A___6_x_Mk_82AIR)
        BRU_41A___6_x_Mk_82_Snakeye = (1, WeaponsA7E.BRU_41A___6_x_Mk_82_Snakeye)
        BRU_41A___6_x_Mk_20_Rockeye = (1, WeaponsA7E.BRU_41A___6_x_Mk_20_Rockeye)
        BRU_41A___6_x_CBU_52B = (1, WeaponsA7E.BRU_41A___6_x_CBU_52B)
        BRU_41A___6_x_CBU_99 = (1, WeaponsA7E.BRU_41A___6_x_CBU_99)
        BRU_41A___6_x_BDU_33 = (1, WeaponsA7E.BRU_41A___6_x_BDU_33)
        LAU3_WP156 = (1, Weapons.LAU3_WP156)
        LAU3_HE151 = (1, Weapons.LAU3_HE151)
        LAU3_HE5 = (1, Weapons.LAU3_HE5)
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            1,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT = (
            1,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum = (
            1,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos = (
            1,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos,
        )
        LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            1,
            Weapons.LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            1,
            Weapons.LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        BRU_42A___2_x_LAU_61___19_2_75__rockets_M151_HE = (
            1,
            WeaponsA7E.BRU_42A___2_x_LAU_61___19_2_75__rockets_M151_HE,
        )
        BRU_42A___2_x_LAU_68___7_2_75__rockets_M151_HE = (
            1,
            WeaponsA7E.BRU_42A___2_x_LAU_68___7_2_75__rockets_M151_HE,
        )
        BRU_42A___2_x_LAU_68___7_2_75__rockets_Mk5_HEAT = (
            1,
            WeaponsA7E.BRU_42A___2_x_LAU_68___7_2_75__rockets_Mk5_HEAT,
        )
        BRU_42A___2_x_LAU_68___7_2_75__rockets_M257 = (
            1,
            WeaponsA7E.BRU_42A___2_x_LAU_68___7_2_75__rockets_M257,
        )
        BRU_42A___2_x_LAU_68___7_2_75__rockets_M156_WP = (
            1,
            WeaponsA7E.BRU_42A___2_x_LAU_68___7_2_75__rockets_M156_WP,
        )
        BRU_42A___2_x_LAU_10___4_ZUNI_Mk_71 = (
            1,
            WeaponsA7E.BRU_42A___2_x_LAU_10___4_ZUNI_Mk_71,
        )
        BRU_42A___3_x_LAU_3___19_2_75__rockets_M156_WP = (
            1,
            WeaponsA7E.BRU_42A___3_x_LAU_3___19_2_75__rockets_M156_WP,
        )
        BRU_42A___3_x_LAU_3___19_2_75__rockets_M151_HE = (
            1,
            WeaponsA7E.BRU_42A___3_x_LAU_3___19_2_75__rockets_M151_HE,
        )
        # ERRR {BRU42A_3*LAU3_HYDRA_MK5HEAT
        BRU_42A___3_x_LAU_61___19_2_75__rockets_M151_HE = (
            1,
            WeaponsA7E.BRU_42A___3_x_LAU_61___19_2_75__rockets_M151_HE,
        )
        BRU_42A___3_x_LAU_68___7_2_75__rockets_M151_HE = (
            1,
            WeaponsA7E.BRU_42A___3_x_LAU_68___7_2_75__rockets_M151_HE,
        )
        BRU_42A___3_x_LAU_68___7_2_75__rockets_Mk5_HEAT = (
            1,
            WeaponsA7E.BRU_42A___3_x_LAU_68___7_2_75__rockets_Mk5_HEAT,
        )
        BRU_42A___3_x_LAU_68___7_2_75__rockets_M257 = (
            1,
            WeaponsA7E.BRU_42A___3_x_LAU_68___7_2_75__rockets_M257,
        )
        BRU_42A___3_x_LAU_68___7_2_75__rockets_M156_WP = (
            1,
            WeaponsA7E.BRU_42A___3_x_LAU_68___7_2_75__rockets_M156_WP,
        )
        BRU_42A___3_x_LAU_10___4_ZUNI_Mk_71 = (
            1,
            WeaponsA7E.BRU_42A___3_x_LAU_10___4_ZUNI_Mk_71,
        )
        AN_ALQ_81_ECM_Pod = (1, WeaponsA7E.AN_ALQ_81_ECM_Pod)
        ALQ_131___ECM_Pod = (1, Weapons.ALQ_131___ECM_Pod)
        ALQ_184 = (1, Weapons.ALQ_184)
        ADM_141A_TALD = (1, Weapons.ADM_141A_TALD)
        ADM_141B_TALD = (1, Weapons.ADM_141B_TALD)
        AERO_1D_300_Gallons_Fuel_Tank__ = (
            1,
            WeaponsA7E.AERO_1D_300_Gallons_Fuel_Tank__,
        )
        AERO_1D_300_Gallons_Fuel_Tank__Empty__ = (
            1,
            WeaponsA7E.AERO_1D_300_Gallons_Fuel_Tank__Empty__,
        )

    # ERRR <CLEAN>

    class Pylon2:
        AGM_62_Walleye_II___Guided_Weapon_Mk_5__TV_Guided_ = (
            2,
            Weapons.AGM_62_Walleye_II___Guided_Weapon_Mk_5__TV_Guided_,
        )
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            2,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM_ = (
            2,
            Weapons.LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            2,
            Weapons.LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        LAU_88_with_2_x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            2,
            Weapons.LAU_88_with_2_x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        LAU_117_AGM_65F = (2, Weapons.LAU_117_AGM_65F)
        LAU_117_AGM_65G = (2, Weapons.LAU_117_AGM_65G)
        LAU_117_AGM_65H = (2, Weapons.LAU_117_AGM_65H)
        LAU_88_AGM_65H_2_L = (2, Weapons.LAU_88_AGM_65H_2_L)
        LAU_118A___AGM_45B_Shrike_ARM = (
            2,
            Weapons.LAU_118A___AGM_45B_Shrike_ARM,
        )
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            2,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        Mk_82___500lb_GP_Bomb_LD = (2, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (2, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            2,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (2, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        Mk_84___2000lb_GP_Bomb_LD = (2, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (2, Weapons.M117___750lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            2,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        CBU_52B___220_x_HE_Frag_bomblets = (2, Weapons.CBU_52B___220_x_HE_Frag_bomblets)
        CBU_87___202_x_CEM_Cluster_Bomb = (2, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (2, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        CBU_99_Mod_6 = (2, WeaponsA7E.CBU_99_Mod_6)
        GBU_10___2000lb_Laser_Guided_Bomb = (
            2,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (2, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        BRU_42A___2_x_Mk_81 = (2, WeaponsA7E.BRU_42A___2_x_Mk_81)
        BRU_42A___2_x_Mk_82 = (2, WeaponsA7E.BRU_42A___2_x_Mk_82)
        BRU_42A___2_x_Mk_82AIR = (2, WeaponsA7E.BRU_42A___2_x_Mk_82AIR)
        BRU_42A___2_x_Mk_82_Snakeye = (2, WeaponsA7E.BRU_42A___2_x_Mk_82_Snakeye)
        BRU_42A___2_x_Mk_83 = (2, WeaponsA7E.BRU_42A___2_x_Mk_83)
        BRU_42A___2_x_M117 = (2, WeaponsA7E.BRU_42A___2_x_M117)
        BRU_42A___2_x_Mk_20_Rockeye = (2, WeaponsA7E.BRU_42A___2_x_Mk_20_Rockeye)
        BRU_42A___2_x_CBU_52B = (2, WeaponsA7E.BRU_42A___2_x_CBU_52B)
        BRU_42A___2_x_CBU_87 = (2, WeaponsA7E.BRU_42A___2_x_CBU_87)
        BRU_42A___2_x_CBU_97 = (2, WeaponsA7E.BRU_42A___2_x_CBU_97)
        BRU_42A___2_x_CBU_99 = (2, WeaponsA7E.BRU_42A___2_x_CBU_99)
        BRU_42A___3_x_Mk_81 = (2, WeaponsA7E.BRU_42A___3_x_Mk_81)
        BRU_42A___3_x_Mk_82 = (2, WeaponsA7E.BRU_42A___3_x_Mk_82)
        BRU_42A___3_x_Mk_82AIR = (2, WeaponsA7E.BRU_42A___3_x_Mk_82AIR)
        BRU_42A___3_x_Mk_82_Snakeye = (2, WeaponsA7E.BRU_42A___3_x_Mk_82_Snakeye)
        BRU_42A___3_x_Mk_83 = (2, WeaponsA7E.BRU_42A___3_x_Mk_83)
        BRU_42A___3_x_M117 = (2, WeaponsA7E.BRU_42A___3_x_M117)
        BRU_42A___3_x_Mk_20_Rockeye = (2, WeaponsA7E.BRU_42A___3_x_Mk_20_Rockeye)
        BRU_42A___3_x_CBU_52B = (2, WeaponsA7E.BRU_42A___3_x_CBU_52B)
        BRU_42A___3_x_CBU_99 = (2, WeaponsA7E.BRU_42A___3_x_CBU_99)
        BRU_42A___3_x_BDU_33 = (2, WeaponsA7E.BRU_42A___3_x_BDU_33)
        BRU_41A___4_x_Mk_81 = (2, WeaponsA7E.BRU_41A___4_x_Mk_81)
        BRU_41A___4_x_Mk_82 = (2, WeaponsA7E.BRU_41A___4_x_Mk_82)
        BRU_41A___4_x_Mk_82AIR = (2, WeaponsA7E.BRU_41A___4_x_Mk_82AIR)
        BRU_41A___4_x_Mk_82_Snakeye = (2, WeaponsA7E.BRU_41A___4_x_Mk_82_Snakeye)
        BRU_41A___4_x_Mk_20_Rockeye = (2, WeaponsA7E.BRU_41A___4_x_Mk_20_Rockeye)
        BRU_41A___4_x_CBU_52B = (2, WeaponsA7E.BRU_41A___4_x_CBU_52B)
        BRU_41A___4_x_CBU_99 = (2, WeaponsA7E.BRU_41A___4_x_CBU_99)
        BRU_41A___6_x_Mk_81 = (2, WeaponsA7E.BRU_41A___6_x_Mk_81)
        BRU_41A___6_x_Mk_82 = (2, WeaponsA7E.BRU_41A___6_x_Mk_82)
        BRU_41A___6_x_Mk_82AIR = (2, WeaponsA7E.BRU_41A___6_x_Mk_82AIR)
        BRU_41A___6_x_Mk_82_Snakeye = (2, WeaponsA7E.BRU_41A___6_x_Mk_82_Snakeye)
        BRU_41A___6_x_Mk_20_Rockeye = (2, WeaponsA7E.BRU_41A___6_x_Mk_20_Rockeye)
        BRU_41A___6_x_CBU_52B = (2, WeaponsA7E.BRU_41A___6_x_CBU_52B)
        BRU_41A___6_x_CBU_99 = (2, WeaponsA7E.BRU_41A___6_x_CBU_99)
        BRU_41A___6_x_BDU_33 = (2, WeaponsA7E.BRU_41A___6_x_BDU_33)
        LAU3_WP156 = (2, Weapons.LAU3_WP156)
        LAU3_HE151 = (2, Weapons.LAU3_HE151)
        LAU3_HE5 = (2, Weapons.LAU3_HE5)
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            2,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT = (
            2,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum = (
            2,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos = (
            2,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos,
        )
        LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            2,
            Weapons.LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            2,
            Weapons.LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        BRU_42A___2_x_LAU_61___19_2_75__rockets_M151_HE = (
            2,
            WeaponsA7E.BRU_42A___2_x_LAU_61___19_2_75__rockets_M151_HE,
        )
        BRU_42A___2_x_LAU_68___7_2_75__rockets_M151_HE = (
            2,
            WeaponsA7E.BRU_42A___2_x_LAU_68___7_2_75__rockets_M151_HE,
        )
        BRU_42A___2_x_LAU_68___7_2_75__rockets_Mk5_HEAT = (
            2,
            WeaponsA7E.BRU_42A___2_x_LAU_68___7_2_75__rockets_Mk5_HEAT,
        )
        BRU_42A___2_x_LAU_68___7_2_75__rockets_M257 = (
            2,
            WeaponsA7E.BRU_42A___2_x_LAU_68___7_2_75__rockets_M257,
        )
        BRU_42A___2_x_LAU_68___7_2_75__rockets_M156_WP = (
            2,
            WeaponsA7E.BRU_42A___2_x_LAU_68___7_2_75__rockets_M156_WP,
        )
        BRU_42A___2_x_LAU_10___4_ZUNI_Mk_71 = (
            2,
            WeaponsA7E.BRU_42A___2_x_LAU_10___4_ZUNI_Mk_71,
        )
        BRU_42A___3_x_LAU_3___19_2_75__rockets_M156_WP = (
            2,
            WeaponsA7E.BRU_42A___3_x_LAU_3___19_2_75__rockets_M156_WP,
        )
        BRU_42A___3_x_LAU_3___19_2_75__rockets_M151_HE = (
            2,
            WeaponsA7E.BRU_42A___3_x_LAU_3___19_2_75__rockets_M151_HE,
        )
        # ERRR {BRU42A_3*LAU3_HYDRA_MK5HEAT
        BRU_42A___3_x_LAU_61___19_2_75__rockets_M151_HE = (
            2,
            WeaponsA7E.BRU_42A___3_x_LAU_61___19_2_75__rockets_M151_HE,
        )
        BRU_42A___3_x_LAU_68___7_2_75__rockets_M151_HE = (
            2,
            WeaponsA7E.BRU_42A___3_x_LAU_68___7_2_75__rockets_M151_HE,
        )
        BRU_42A___3_x_LAU_68___7_2_75__rockets_Mk5_HEAT = (
            2,
            WeaponsA7E.BRU_42A___3_x_LAU_68___7_2_75__rockets_Mk5_HEAT,
        )
        BRU_42A___3_x_LAU_68___7_2_75__rockets_M257 = (
            2,
            WeaponsA7E.BRU_42A___3_x_LAU_68___7_2_75__rockets_M257,
        )
        BRU_42A___3_x_LAU_68___7_2_75__rockets_M156_WP = (
            2,
            WeaponsA7E.BRU_42A___3_x_LAU_68___7_2_75__rockets_M156_WP,
        )
        BRU_42A___3_x_LAU_10___4_ZUNI_Mk_71 = (
            2,
            WeaponsA7E.BRU_42A___3_x_LAU_10___4_ZUNI_Mk_71,
        )

    # ERRR <CLEAN>

    class Pylon3:
        AGM_62_Walleye_II___Guided_Weapon_Mk_5__TV_Guided_ = (
            3,
            Weapons.AGM_62_Walleye_II___Guided_Weapon_Mk_5__TV_Guided_,
        )
        Mk_82___500lb_GP_Bomb_LD = (3, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (3, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            3,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (3, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        Mk_84___2000lb_GP_Bomb_LD = (3, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (3, Weapons.M117___750lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            3,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        CBU_52B___220_x_HE_Frag_bomblets = (3, Weapons.CBU_52B___220_x_HE_Frag_bomblets)
        CBU_87___202_x_CEM_Cluster_Bomb = (3, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (3, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        CBU_99_Mod_6 = (3, WeaponsA7E.CBU_99_Mod_6)
        GBU_10___2000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (3, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        BRU_42A___2_x_Mk_81 = (3, WeaponsA7E.BRU_42A___2_x_Mk_81)
        BRU_42A___2_x_Mk_82 = (3, WeaponsA7E.BRU_42A___2_x_Mk_82)
        BRU_42A___2_x_Mk_82AIR = (3, WeaponsA7E.BRU_42A___2_x_Mk_82AIR)
        BRU_42A___2_x_Mk_82_Snakeye = (3, WeaponsA7E.BRU_42A___2_x_Mk_82_Snakeye)
        BRU_42A___2_x_Mk_83 = (3, WeaponsA7E.BRU_42A___2_x_Mk_83)
        BRU_42A___2_x_M117 = (3, WeaponsA7E.BRU_42A___2_x_M117)
        BRU_42A___2_x_Mk_20_Rockeye = (3, WeaponsA7E.BRU_42A___2_x_Mk_20_Rockeye)
        BRU_42A___2_x_CBU_52B = (3, WeaponsA7E.BRU_42A___2_x_CBU_52B)
        BRU_42A___2_x_CBU_87 = (3, WeaponsA7E.BRU_42A___2_x_CBU_87)
        BRU_42A___2_x_CBU_97 = (3, WeaponsA7E.BRU_42A___2_x_CBU_97)
        BRU_42A___2_x_CBU_99 = (3, WeaponsA7E.BRU_42A___2_x_CBU_99)
        BRU_41A___4_x_Mk_81 = (3, WeaponsA7E.BRU_41A___4_x_Mk_81)
        BRU_41A___4_x_Mk_82 = (3, WeaponsA7E.BRU_41A___4_x_Mk_82)
        BRU_41A___4_x_Mk_82AIR = (3, WeaponsA7E.BRU_41A___4_x_Mk_82AIR)
        BRU_41A___4_x_Mk_82_Snakeye = (3, WeaponsA7E.BRU_41A___4_x_Mk_82_Snakeye)
        BRU_41A___4_x_Mk_20_Rockeye = (3, WeaponsA7E.BRU_41A___4_x_Mk_20_Rockeye)
        BRU_41A___4_x_CBU_52B = (3, WeaponsA7E.BRU_41A___4_x_CBU_52B)
        BRU_41A___4_x_CBU_99 = (3, WeaponsA7E.BRU_41A___4_x_CBU_99)
        LAU3_WP156 = (3, Weapons.LAU3_WP156)
        LAU3_HE151 = (3, Weapons.LAU3_HE151)
        LAU3_HE5 = (3, Weapons.LAU3_HE5)
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            3,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT = (
            3,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum = (
            3,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos = (
            3,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos,
        )
        LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            3,
            Weapons.LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            3,
            Weapons.LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        BRU_42A___2_x_LAU_61___19_2_75__rockets_M151_HE = (
            3,
            WeaponsA7E.BRU_42A___2_x_LAU_61___19_2_75__rockets_M151_HE,
        )
        BRU_42A___2_x_LAU_68___7_2_75__rockets_M151_HE = (
            3,
            WeaponsA7E.BRU_42A___2_x_LAU_68___7_2_75__rockets_M151_HE,
        )
        BRU_42A___2_x_LAU_68___7_2_75__rockets_Mk5_HEAT = (
            3,
            WeaponsA7E.BRU_42A___2_x_LAU_68___7_2_75__rockets_Mk5_HEAT,
        )
        BRU_42A___2_x_LAU_68___7_2_75__rockets_M257 = (
            3,
            WeaponsA7E.BRU_42A___2_x_LAU_68___7_2_75__rockets_M257,
        )
        BRU_42A___2_x_LAU_68___7_2_75__rockets_M156_WP = (
            3,
            WeaponsA7E.BRU_42A___2_x_LAU_68___7_2_75__rockets_M156_WP,
        )
        BRU_42A___2_x_LAU_10___4_ZUNI_Mk_71 = (
            3,
            WeaponsA7E.BRU_42A___2_x_LAU_10___4_ZUNI_Mk_71,
        )
        GPU_5A_Gunpod = (3, WeaponsA7E.GPU_5A_Gunpod)
        AERO_1D_300_Gallons_Fuel_Tank__ = (
            3,
            WeaponsA7E.AERO_1D_300_Gallons_Fuel_Tank__,
        )
        AERO_1D_300_Gallons_Fuel_Tank__Empty__ = (
            3,
            WeaponsA7E.AERO_1D_300_Gallons_Fuel_Tank__Empty__,
        )

    # ERRR <CLEAN>

    class Pylon4:
        AIM_9M_Sidewinder_IR_AAM = (4, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (4, Weapons.AIM_9L_Sidewinder_IR_AAM)
        CATM_9M = (4, Weapons.CATM_9M)
        AGM_122_Sidearm = (4, Weapons.AGM_122_Sidearm)
        Smokewinder___red = (4, Weapons.Smokewinder___red)
        Smokewinder___green = (4, Weapons.Smokewinder___green)
        Smokewinder___blue = (4, Weapons.Smokewinder___blue)
        Smokewinder___white = (4, Weapons.Smokewinder___white)
        Smokewinder___yellow = (4, Weapons.Smokewinder___yellow)

    class Pylon5:
        AIM_9M_Sidewinder_IR_AAM = (5, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (5, Weapons.AIM_9L_Sidewinder_IR_AAM)
        CATM_9M = (5, Weapons.CATM_9M)
        AGM_122_Sidearm = (5, Weapons.AGM_122_Sidearm)
        Smokewinder___red = (5, Weapons.Smokewinder___red)
        Smokewinder___green = (5, Weapons.Smokewinder___green)
        Smokewinder___blue = (5, Weapons.Smokewinder___blue)
        Smokewinder___white = (5, Weapons.Smokewinder___white)
        Smokewinder___yellow = (5, Weapons.Smokewinder___yellow)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (5, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

    class Pylon6:
        AGM_62_Walleye_II___Guided_Weapon_Mk_5__TV_Guided_ = (
            6,
            Weapons.AGM_62_Walleye_II___Guided_Weapon_Mk_5__TV_Guided_,
        )
        Mk_82___500lb_GP_Bomb_LD = (6, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (6, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            6,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (6, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        Mk_84___2000lb_GP_Bomb_LD = (6, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (6, Weapons.M117___750lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            6,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        CBU_52B___220_x_HE_Frag_bomblets = (6, Weapons.CBU_52B___220_x_HE_Frag_bomblets)
        CBU_87___202_x_CEM_Cluster_Bomb = (6, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (6, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        CBU_99_Mod_6 = (6, WeaponsA7E.CBU_99_Mod_6)
        GBU_10___2000lb_Laser_Guided_Bomb = (
            6,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (6, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        BRU_42A___2_x_Mk_81_ = (6, WeaponsA7E.BRU_42A___2_x_Mk_81_)
        BRU_42A___2_x_Mk_82_ = (6, WeaponsA7E.BRU_42A___2_x_Mk_82_)
        BRU_42A___2_x_Mk_82AIR_ = (6, WeaponsA7E.BRU_42A___2_x_Mk_82AIR_)
        BRU_42A___2_x_Mk_82_Snakeye_ = (6, WeaponsA7E.BRU_42A___2_x_Mk_82_Snakeye_)
        BRU_42A___2_x_Mk_83_ = (6, WeaponsA7E.BRU_42A___2_x_Mk_83_)
        BRU_42A___2_x_M117_ = (6, WeaponsA7E.BRU_42A___2_x_M117_)
        BRU_42A___2_x_Mk_20_Rockeye_ = (6, WeaponsA7E.BRU_42A___2_x_Mk_20_Rockeye_)
        BRU_42A___2_x_CBU_52B_ = (6, WeaponsA7E.BRU_42A___2_x_CBU_52B_)
        BRU_42A___2_x_CBU_87_ = (6, WeaponsA7E.BRU_42A___2_x_CBU_87_)
        BRU_42A___2_x_CBU_97_ = (6, WeaponsA7E.BRU_42A___2_x_CBU_97_)
        BRU_42A___2_x_CBU_99_ = (6, WeaponsA7E.BRU_42A___2_x_CBU_99_)
        BRU_41A___4_x_Mk_81_ = (6, WeaponsA7E.BRU_41A___4_x_Mk_81_)
        BRU_41A___4_x_Mk_82_ = (6, WeaponsA7E.BRU_41A___4_x_Mk_82_)
        BRU_41A___4_x_Mk_82AIR_ = (6, WeaponsA7E.BRU_41A___4_x_Mk_82AIR_)
        BRU_41A___4_x_Mk_82_Snakeye_ = (6, WeaponsA7E.BRU_41A___4_x_Mk_82_Snakeye_)
        BRU_41A___4_x_Mk_20_Rockeye_ = (6, WeaponsA7E.BRU_41A___4_x_Mk_20_Rockeye_)
        BRU_41A___4_x_CBU_52B_ = (6, WeaponsA7E.BRU_41A___4_x_CBU_52B_)
        BRU_41A___4_x_CBU_99_ = (6, WeaponsA7E.BRU_41A___4_x_CBU_99_)
        LAU3_WP156 = (6, Weapons.LAU3_WP156)
        LAU3_HE151 = (6, Weapons.LAU3_HE151)
        LAU3_HE5 = (6, Weapons.LAU3_HE5)
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            6,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT = (
            6,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum = (
            6,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos = (
            6,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos,
        )
        LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            6,
            Weapons.LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            6,
            Weapons.LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        BRU_42A___2_x_LAU_61___19_2_75__rockets_M151_HE_ = (
            6,
            WeaponsA7E.BRU_42A___2_x_LAU_61___19_2_75__rockets_M151_HE_,
        )
        BRU_42A___2_x_LAU_68___7_2_75__rockets_M151_HE_ = (
            6,
            WeaponsA7E.BRU_42A___2_x_LAU_68___7_2_75__rockets_M151_HE_,
        )
        BRU_42A___2_x_LAU_68___7_2_75__rockets_Mk5_HEAT_ = (
            6,
            WeaponsA7E.BRU_42A___2_x_LAU_68___7_2_75__rockets_Mk5_HEAT_,
        )
        BRU_42A___2_x_LAU_68___7_2_75__rockets_M257_ = (
            6,
            WeaponsA7E.BRU_42A___2_x_LAU_68___7_2_75__rockets_M257_,
        )
        BRU_42A___2_x_LAU_68___7_2_75__rockets_M156_WP_ = (
            6,
            WeaponsA7E.BRU_42A___2_x_LAU_68___7_2_75__rockets_M156_WP_,
        )
        BRU_42A___2_x_LAU_10___4_ZUNI_Mk_71_ = (
            6,
            WeaponsA7E.BRU_42A___2_x_LAU_10___4_ZUNI_Mk_71_,
        )
        AN_AAR_45_FLIR_Pod = (6, WeaponsA7E.AN_AAR_45_FLIR_Pod)
        GPU_5A_Gunpod = (6, WeaponsA7E.GPU_5A_Gunpod)
        AERO_1D_300_Gallons_Fuel_Tank__ = (
            6,
            WeaponsA7E.AERO_1D_300_Gallons_Fuel_Tank__,
        )
        AERO_1D_300_Gallons_Fuel_Tank__Empty__ = (
            6,
            WeaponsA7E.AERO_1D_300_Gallons_Fuel_Tank__Empty__,
        )

    # ERRR <CLEAN>

    class Pylon7:
        AGM_62_Walleye_II___Guided_Weapon_Mk_5__TV_Guided_ = (
            7,
            Weapons.AGM_62_Walleye_II___Guided_Weapon_Mk_5__TV_Guided_,
        )
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            7,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM__ = (
            7,
            Weapons.LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM__,
        )
        LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_ = (
            7,
            Weapons.LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_,
        )
        LAU_88_with_2_x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd__ = (
            7,
            Weapons.LAU_88_with_2_x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd__,
        )
        LAU_117_AGM_65F = (7, Weapons.LAU_117_AGM_65F)
        LAU_117_AGM_65G = (7, Weapons.LAU_117_AGM_65G)
        LAU_117_AGM_65H = (7, Weapons.LAU_117_AGM_65H)
        LAU_88_AGM_65H_2_R = (7, Weapons.LAU_88_AGM_65H_2_R)
        LAU_118A___AGM_45B_Shrike_ARM = (
            7,
            Weapons.LAU_118A___AGM_45B_Shrike_ARM,
        )
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            7,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        Mk_81___250lb_GP_Bomb_LD = (7, Weapons.Mk_81___250lb_GP_Bomb_LD)
        Mk_82___500lb_GP_Bomb_LD = (7, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (7, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            7,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (7, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        Mk_84___2000lb_GP_Bomb_LD = (7, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (7, Weapons.M117___750lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            7,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        CBU_52B___220_x_HE_Frag_bomblets = (7, Weapons.CBU_52B___220_x_HE_Frag_bomblets)
        CBU_87___202_x_CEM_Cluster_Bomb = (7, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (7, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        CBU_99_Mod_6 = (7, WeaponsA7E.CBU_99_Mod_6)
        GBU_10___2000lb_Laser_Guided_Bomb = (
            7,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (7, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        BRU_42A___2_x_Mk_81_ = (7, WeaponsA7E.BRU_42A___2_x_Mk_81_)
        BRU_42A___2_x_Mk_82_ = (7, WeaponsA7E.BRU_42A___2_x_Mk_82_)
        BRU_42A___2_x_Mk_82AIR_ = (7, WeaponsA7E.BRU_42A___2_x_Mk_82AIR_)
        BRU_42A___2_x_Mk_82_Snakeye_ = (7, WeaponsA7E.BRU_42A___2_x_Mk_82_Snakeye_)
        BRU_42A___2_x_Mk_83_ = (7, WeaponsA7E.BRU_42A___2_x_Mk_83_)
        BRU_42A___2_x_M117_ = (7, WeaponsA7E.BRU_42A___2_x_M117_)
        BRU_42A___2_x_Mk_20_Rockeye_ = (7, WeaponsA7E.BRU_42A___2_x_Mk_20_Rockeye_)
        BRU_42A___2_x_CBU_52B_ = (7, WeaponsA7E.BRU_42A___2_x_CBU_52B_)
        BRU_42A___2_x_CBU_87_ = (7, WeaponsA7E.BRU_42A___2_x_CBU_87_)
        BRU_42A___2_x_CBU_97_ = (7, WeaponsA7E.BRU_42A___2_x_CBU_97_)
        BRU_42A___2_x_CBU_99_ = (7, WeaponsA7E.BRU_42A___2_x_CBU_99_)
        BRU_42A___3_x_Mk_81 = (7, WeaponsA7E.BRU_42A___3_x_Mk_81)
        BRU_42A___3_x_Mk_82 = (7, WeaponsA7E.BRU_42A___3_x_Mk_82)
        BRU_42A___3_x_Mk_82AIR = (7, WeaponsA7E.BRU_42A___3_x_Mk_82AIR)
        BRU_42A___3_x_Mk_82_Snakeye = (7, WeaponsA7E.BRU_42A___3_x_Mk_82_Snakeye)
        BRU_42A___3_x_Mk_83 = (7, WeaponsA7E.BRU_42A___3_x_Mk_83)
        BRU_42A___3_x_M117 = (7, WeaponsA7E.BRU_42A___3_x_M117)
        BRU_42A___3_x_Mk_20_Rockeye = (7, WeaponsA7E.BRU_42A___3_x_Mk_20_Rockeye)
        BRU_42A___3_x_CBU_52B = (7, WeaponsA7E.BRU_42A___3_x_CBU_52B)
        BRU_42A___3_x_CBU_99 = (7, WeaponsA7E.BRU_42A___3_x_CBU_99)
        BRU_42A___3_x_BDU_33 = (7, WeaponsA7E.BRU_42A___3_x_BDU_33)
        BRU_41A___4_x_Mk_81_ = (7, WeaponsA7E.BRU_41A___4_x_Mk_81_)
        BRU_41A___4_x_Mk_82_ = (7, WeaponsA7E.BRU_41A___4_x_Mk_82_)
        BRU_41A___4_x_Mk_82AIR_ = (7, WeaponsA7E.BRU_41A___4_x_Mk_82AIR_)
        BRU_41A___4_x_Mk_82_Snakeye_ = (7, WeaponsA7E.BRU_41A___4_x_Mk_82_Snakeye_)
        BRU_41A___4_x_Mk_20_Rockeye_ = (7, WeaponsA7E.BRU_41A___4_x_Mk_20_Rockeye_)
        BRU_41A___4_x_CBU_52B_ = (7, WeaponsA7E.BRU_41A___4_x_CBU_52B_)
        BRU_41A___4_x_CBU_99_ = (7, WeaponsA7E.BRU_41A___4_x_CBU_99_)
        BRU_41A___6_x_Mk_81 = (7, WeaponsA7E.BRU_41A___6_x_Mk_81)
        BRU_41A___6_x_Mk_82 = (7, WeaponsA7E.BRU_41A___6_x_Mk_82)
        BRU_41A___6_x_Mk_82AIR = (7, WeaponsA7E.BRU_41A___6_x_Mk_82AIR)
        BRU_41A___6_x_Mk_82_Snakeye = (7, WeaponsA7E.BRU_41A___6_x_Mk_82_Snakeye)
        BRU_41A___6_x_Mk_20_Rockeye = (7, WeaponsA7E.BRU_41A___6_x_Mk_20_Rockeye)
        BRU_41A___6_x_CBU_52B = (7, WeaponsA7E.BRU_41A___6_x_CBU_52B)
        BRU_41A___6_x_CBU_99 = (7, WeaponsA7E.BRU_41A___6_x_CBU_99)
        BRU_41A___6_x_BDU_33 = (7, WeaponsA7E.BRU_41A___6_x_BDU_33)
        LAU3_WP156 = (7, Weapons.LAU3_WP156)
        LAU3_HE151 = (7, Weapons.LAU3_HE151)
        LAU3_HE5 = (7, Weapons.LAU3_HE5)
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            7,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT = (
            7,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum = (
            7,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos = (
            7,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos,
        )
        LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            7,
            Weapons.LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            7,
            Weapons.LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        BRU_42A___2_x_LAU_61___19_2_75__rockets_M151_HE_ = (
            7,
            WeaponsA7E.BRU_42A___2_x_LAU_61___19_2_75__rockets_M151_HE_,
        )
        BRU_42A___2_x_LAU_68___7_2_75__rockets_M151_HE_ = (
            7,
            WeaponsA7E.BRU_42A___2_x_LAU_68___7_2_75__rockets_M151_HE_,
        )
        BRU_42A___2_x_LAU_68___7_2_75__rockets_Mk5_HEAT_ = (
            7,
            WeaponsA7E.BRU_42A___2_x_LAU_68___7_2_75__rockets_Mk5_HEAT_,
        )
        BRU_42A___2_x_LAU_68___7_2_75__rockets_M257_ = (
            7,
            WeaponsA7E.BRU_42A___2_x_LAU_68___7_2_75__rockets_M257_,
        )
        BRU_42A___2_x_LAU_68___7_2_75__rockets_M156_WP_ = (
            7,
            WeaponsA7E.BRU_42A___2_x_LAU_68___7_2_75__rockets_M156_WP_,
        )
        BRU_42A___2_x_LAU_10___4_ZUNI_Mk_71_ = (
            7,
            WeaponsA7E.BRU_42A___2_x_LAU_10___4_ZUNI_Mk_71_,
        )
        BRU_42A___3_x_LAU_3___19_2_75__rockets_M156_WP = (
            7,
            WeaponsA7E.BRU_42A___3_x_LAU_3___19_2_75__rockets_M156_WP,
        )
        BRU_42A___3_x_LAU_3___19_2_75__rockets_M151_HE = (
            7,
            WeaponsA7E.BRU_42A___3_x_LAU_3___19_2_75__rockets_M151_HE,
        )
        # ERRR {BRU42A_3*LAU3_HYDRA_MK5HEAT
        BRU_42A___3_x_LAU_61___19_2_75__rockets_M151_HE = (
            7,
            WeaponsA7E.BRU_42A___3_x_LAU_61___19_2_75__rockets_M151_HE,
        )
        BRU_42A___3_x_LAU_68___7_2_75__rockets_M151_HE = (
            7,
            WeaponsA7E.BRU_42A___3_x_LAU_68___7_2_75__rockets_M151_HE,
        )
        BRU_42A___3_x_LAU_68___7_2_75__rockets_Mk5_HEAT = (
            7,
            WeaponsA7E.BRU_42A___3_x_LAU_68___7_2_75__rockets_Mk5_HEAT,
        )
        BRU_42A___3_x_LAU_68___7_2_75__rockets_M257 = (
            7,
            WeaponsA7E.BRU_42A___3_x_LAU_68___7_2_75__rockets_M257,
        )
        BRU_42A___3_x_LAU_68___7_2_75__rockets_M156_WP = (
            7,
            WeaponsA7E.BRU_42A___3_x_LAU_68___7_2_75__rockets_M156_WP,
        )
        BRU_42A___3_x_LAU_10___4_ZUNI_Mk_71 = (
            7,
            WeaponsA7E.BRU_42A___3_x_LAU_10___4_ZUNI_Mk_71,
        )

    # ERRR <CLEAN>

    class Pylon8:
        AGM_62_Walleye_II___Guided_Weapon_Mk_5__TV_Guided_ = (
            8,
            Weapons.AGM_62_Walleye_II___Guided_Weapon_Mk_5__TV_Guided_,
        )
        LAU_118A___AGM_45B_Shrike_ARM = (
            8,
            Weapons.LAU_118A___AGM_45B_Shrike_ARM,
        )
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            8,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        Mk_77_Mod_0 = (8, WeaponsA7E.Mk_77_Mod_0)
        Mk_77_Mod_5 = (8, WeaponsA7E.Mk_77_Mod_5)
        Mk_82___500lb_GP_Bomb_LD = (8, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (8, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            8,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        Mk_83___1000lb_GP_Bomb_LD = (8, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        Mk_83AIR = (8, WeaponsA7E.Mk_83AIR)
        Mk_84___2000lb_GP_Bomb_LD = (8, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (8, Weapons.M117___750lb_GP_Bomb_LD)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            8,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        CBU_52B___220_x_HE_Frag_bomblets = (8, Weapons.CBU_52B___220_x_HE_Frag_bomblets)
        CBU_87___202_x_CEM_Cluster_Bomb = (8, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (8, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        CBU_99_Mod_6 = (8, WeaponsA7E.CBU_99_Mod_6)
        GBU_10___2000lb_Laser_Guided_Bomb = (
            8,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (8, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        BRU_42A___2_x_Mk_81_ = (8, WeaponsA7E.BRU_42A___2_x_Mk_81_)
        BRU_42A___2_x_Mk_82_ = (8, WeaponsA7E.BRU_42A___2_x_Mk_82_)
        BRU_42A___2_x_Mk_82AIR_ = (8, WeaponsA7E.BRU_42A___2_x_Mk_82AIR_)
        BRU_42A___2_x_Mk_82_Snakeye_ = (8, WeaponsA7E.BRU_42A___2_x_Mk_82_Snakeye_)
        BRU_42A___2_x_Mk_83_ = (8, WeaponsA7E.BRU_42A___2_x_Mk_83_)
        BRU_42A___3_x_Mk_83AIR = (8, WeaponsA7E.BRU_42A___3_x_Mk_83AIR)
        BRU_42A___2_x_M117_ = (8, WeaponsA7E.BRU_42A___2_x_M117_)
        BRU_42A___2_x_Mk_20_Rockeye_ = (8, WeaponsA7E.BRU_42A___2_x_Mk_20_Rockeye_)
        BRU_42A___2_x_CBU_52B_ = (8, WeaponsA7E.BRU_42A___2_x_CBU_52B_)
        BRU_42A___2_x_CBU_87_ = (8, WeaponsA7E.BRU_42A___2_x_CBU_87_)
        BRU_42A___2_x_CBU_97_ = (8, WeaponsA7E.BRU_42A___2_x_CBU_97_)
        BRU_42A___2_x_CBU_99_ = (8, WeaponsA7E.BRU_42A___2_x_CBU_99_)
        BRU_42A___3_x_Mk_81 = (8, WeaponsA7E.BRU_42A___3_x_Mk_81)
        BRU_42A___3_x_Mk_82 = (8, WeaponsA7E.BRU_42A___3_x_Mk_82)
        BRU_42A___3_x_Mk_82AIR = (8, WeaponsA7E.BRU_42A___3_x_Mk_82AIR)
        BRU_42A___3_x_Mk_82_Snakeye = (8, WeaponsA7E.BRU_42A___3_x_Mk_82_Snakeye)
        BRU_42A___3_x_Mk_83 = (8, WeaponsA7E.BRU_42A___3_x_Mk_83)
        BRU_42A___3_x_M117 = (8, WeaponsA7E.BRU_42A___3_x_M117)
        BRU_42A___3_x_Mk_20_Rockeye = (8, WeaponsA7E.BRU_42A___3_x_Mk_20_Rockeye)
        BRU_42A___3_x_CBU_52B = (8, WeaponsA7E.BRU_42A___3_x_CBU_52B)
        BRU_42A___3_x_CBU_99 = (8, WeaponsA7E.BRU_42A___3_x_CBU_99)
        BRU_42A___3_x_BDU_33 = (8, WeaponsA7E.BRU_42A___3_x_BDU_33)
        BRU_41A___4_x_Mk_81_ = (8, WeaponsA7E.BRU_41A___4_x_Mk_81_)
        BRU_41A___4_x_Mk_82_ = (8, WeaponsA7E.BRU_41A___4_x_Mk_82_)
        BRU_41A___4_x_Mk_82AIR_ = (8, WeaponsA7E.BRU_41A___4_x_Mk_82AIR_)
        BRU_41A___4_x_Mk_82_Snakeye_ = (8, WeaponsA7E.BRU_41A___4_x_Mk_82_Snakeye_)
        BRU_41A___4_x_Mk_20_Rockeye_ = (8, WeaponsA7E.BRU_41A___4_x_Mk_20_Rockeye_)
        BRU_41A___4_x_CBU_52B_ = (8, WeaponsA7E.BRU_41A___4_x_CBU_52B_)
        BRU_41A___4_x_CBU_99_ = (8, WeaponsA7E.BRU_41A___4_x_CBU_99_)
        BRU_41A___6_x_Mk_81 = (8, WeaponsA7E.BRU_41A___6_x_Mk_81)
        BRU_41A___6_x_Mk_82 = (8, WeaponsA7E.BRU_41A___6_x_Mk_82)
        BRU_41A___6_x_Mk_82AIR = (8, WeaponsA7E.BRU_41A___6_x_Mk_82AIR)
        BRU_41A___6_x_Mk_82_Snakeye = (8, WeaponsA7E.BRU_41A___6_x_Mk_82_Snakeye)
        BRU_41A___6_x_Mk_20_Rockeye = (8, WeaponsA7E.BRU_41A___6_x_Mk_20_Rockeye)
        BRU_41A___6_x_CBU_52B = (8, WeaponsA7E.BRU_41A___6_x_CBU_52B)
        BRU_41A___6_x_CBU_99 = (8, WeaponsA7E.BRU_41A___6_x_CBU_99)
        BRU_41A___6_x_BDU_33 = (8, WeaponsA7E.BRU_41A___6_x_BDU_33)
        LAU3_WP156 = (8, Weapons.LAU3_WP156)
        LAU3_HE151 = (8, Weapons.LAU3_HE151)
        LAU3_HE5 = (8, Weapons.LAU3_HE5)
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            8,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT = (
            8,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_Mk5__HEAT,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum = (
            8,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M257__Para_Illum,
        )
        LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos = (
            8,
            Weapons.LAU_68_pod___7_x_2_75_Hydra__UnGd_Rkts_M156__Wht_Phos,
        )
        LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE = (
            8,
            Weapons.LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE,
        )
        LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            8,
            Weapons.LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        BRU_42A___2_x_LAU_61___19_2_75__rockets_M151_HE_ = (
            8,
            WeaponsA7E.BRU_42A___2_x_LAU_61___19_2_75__rockets_M151_HE_,
        )
        BRU_42A___2_x_LAU_68___7_2_75__rockets_M151_HE_ = (
            8,
            WeaponsA7E.BRU_42A___2_x_LAU_68___7_2_75__rockets_M151_HE_,
        )
        BRU_42A___2_x_LAU_68___7_2_75__rockets_Mk5_HEAT_ = (
            8,
            WeaponsA7E.BRU_42A___2_x_LAU_68___7_2_75__rockets_Mk5_HEAT_,
        )
        BRU_42A___2_x_LAU_68___7_2_75__rockets_M257_ = (
            8,
            WeaponsA7E.BRU_42A___2_x_LAU_68___7_2_75__rockets_M257_,
        )
        BRU_42A___2_x_LAU_68___7_2_75__rockets_M156_WP_ = (
            8,
            WeaponsA7E.BRU_42A___2_x_LAU_68___7_2_75__rockets_M156_WP_,
        )
        BRU_42A___2_x_LAU_10___4_ZUNI_Mk_71_ = (
            8,
            WeaponsA7E.BRU_42A___2_x_LAU_10___4_ZUNI_Mk_71_,
        )
        BRU_42A___3_x_LAU_3___19_2_75__rockets_M156_WP = (
            8,
            WeaponsA7E.BRU_42A___3_x_LAU_3___19_2_75__rockets_M156_WP,
        )
        BRU_42A___3_x_LAU_3___19_2_75__rockets_M151_HE = (
            8,
            WeaponsA7E.BRU_42A___3_x_LAU_3___19_2_75__rockets_M151_HE,
        )
        # ERRR {BRU42A_3*LAU3_HYDRA_MK5HEAT
        BRU_42A___3_x_LAU_61___19_2_75__rockets_M151_HE = (
            8,
            WeaponsA7E.BRU_42A___3_x_LAU_61___19_2_75__rockets_M151_HE,
        )
        BRU_42A___3_x_LAU_68___7_2_75__rockets_M151_HE = (
            8,
            WeaponsA7E.BRU_42A___3_x_LAU_68___7_2_75__rockets_M151_HE,
        )
        BRU_42A___3_x_LAU_68___7_2_75__rockets_Mk5_HEAT = (
            8,
            WeaponsA7E.BRU_42A___3_x_LAU_68___7_2_75__rockets_Mk5_HEAT,
        )
        BRU_42A___3_x_LAU_68___7_2_75__rockets_M257 = (
            8,
            WeaponsA7E.BRU_42A___3_x_LAU_68___7_2_75__rockets_M257,
        )
        BRU_42A___3_x_LAU_68___7_2_75__rockets_M156_WP = (
            8,
            WeaponsA7E.BRU_42A___3_x_LAU_68___7_2_75__rockets_M156_WP,
        )
        BRU_42A___3_x_LAU_10___4_ZUNI_Mk_71 = (
            8,
            WeaponsA7E.BRU_42A___3_x_LAU_10___4_ZUNI_Mk_71,
        )
        AN_ALQ_81_ECM_Pod = (8, WeaponsA7E.AN_ALQ_81_ECM_Pod)
        ALQ_131___ECM_Pod = (8, Weapons.ALQ_131___ECM_Pod)
        ALQ_184 = (8, Weapons.ALQ_184)
        ADM_141A_TALD = (8, Weapons.ADM_141A_TALD)
        ADM_141B_TALD = (8, Weapons.ADM_141B_TALD)
        AERO_1D_300_Gallons_Fuel_Tank__ = (
            8,
            WeaponsA7E.AERO_1D_300_Gallons_Fuel_Tank__,
        )
        AERO_1D_300_Gallons_Fuel_Tank__Empty__ = (
            8,
            WeaponsA7E.AERO_1D_300_Gallons_Fuel_Tank__Empty__,
        )

    # ERRR <CLEAN>

    class Pylon9:
        L_081_Fantasmagoria_ELINT_pod = (9, Weapons.L_081_Fantasmagoria_ELINT_pod)
        Mercury_LLTV_Pod = (9, Weapons.Mercury_LLTV_Pod)

    class Pylon10:
        L_081_Fantasmagoria_ELINT_pod = (10, Weapons.L_081_Fantasmagoria_ELINT_pod)
        Mercury_LLTV_Pod = (10, Weapons.Mercury_LLTV_Pod)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

    tasks = [
        task.GroundAttack,
        task.CAS,
        task.AFAC,
        task.RunwayAttack,
        task.SEAD,
        task.PinpointStrike,
        task.AntishipStrike,
        task.Reconnaissance,
    ]
    task_default = task.GroundAttack
