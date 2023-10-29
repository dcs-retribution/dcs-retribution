from typing import Dict, List, Set, Any

from dcs import task
from dcs.planes import F_16C_50, PlaneType
from dcs.weapons_data import Weapons

from game.modsupport import planemod
from pydcs_extensions.pylon_injector import inject_pylon, eject_pylon
from pydcs_extensions.weapon_injector import inject_weapons


class WeaponsF16I:
    ANAXQ_14 = {"clsid": "{ANAXQ-14}", "name": "ANAXQ-14", "weight": 0}
    AN_AAQ_13 = {"clsid": "{ANAAQ-13}", "name": "AN/AAQ-13", "weight": 211}
    Barak_lights = {"clsid": "{Barak lights}", "name": "Barak lights", "weight": 2}
    Barak_tail_1 = {"clsid": "{Barak tail 1}", "name": "Barak tail 1", "weight": 208}
    Barak_tail_2 = {"clsid": "{Barak tail 2}", "name": "Barak tail 2", "weight": 208}
    CREW = {"clsid": "{CREW}", "name": "CREW", "weight": 0}
    Crew_Ladder_For_CFT = {
        "clsid": "{IDF Mods Project LDR CFT}",
        "name": "Crew Ladder For CFT",
        "weight": 0,
    }
    Crew_Ladder_No_CFT = {
        "clsid": "{IDF Mods Project LDR No CFT}",
        "name": "Crew Ladder No CFT",
        "weight": 0,
    }
    Delilah_cover_Pylon_3 = {
        "clsid": "{Delilah cover S 3}",
        "name": "Delilah cover Pylon 3",
        "weight": 0,
    }
    Delilah_cover_Pylon_3_7 = {
        "clsid": "{Delilah cover S 3-7}",
        "name": "Delilah cover Pylon 3-7",
        "weight": 0,
    }
    Delilah_cover_Pylon_7 = {
        "clsid": "{Delilah cover S 7}",
        "name": "Delilah cover Pylon 7",
        "weight": 0,
    }
    ECM_lights = {"clsid": "{Lights}", "name": "ECM lights", "weight": 30}
    Fuel_tank_300_gal__ = {
        "clsid": "{IDF Mods Project 300gal}",
        "name": "Fuel tank 300 gal",
        "weight": 1197.4895155,
    }
    Fuel_tank_600_gal = {
        "clsid": "{600gal}",
        "name": "Fuel tank 600 gal",
        "weight": 2107.806774925,
    }
    Fuel_tank_600_gal__EMPTY_ = {
        "clsid": "{600gal_Empty}",
        "name": "Fuel tank 600 gal *EMPTY*",
        "weight": 172,
    }
    IDF_Mods_Project_Fuel_Tank_370_EMPTY = {
        "clsid": "{IDF Mods Project Fuel Tank 370 EMPTY}",
        "name": "IDF Mods Project Fuel Tank 370 EMPTY",
        "weight": 250,
    }
    IDF_Mods_Project_F_16C_CFT = {
        "clsid": "{IDF Mods Project F-16C CFT}",
        "name": "IDF Mods Project F-16C CFT",
        "weight": 408,
    }
    IDF_Mods_Project_F_16C_CFT_Fuel_Left_1500lb = {
        "clsid": "{IDF Mods Project F-16C CFT Fuel Left}",
        "name": "IDF Mods Project F-16C CFT Fuel Left 1500lb",
        "weight": 680.0827540681,
    }
    IDF_Mods_Project_F_16C_CFT_Fuel_Right_1500lb = {
        "clsid": "{IDF Mods Project F-16C CFT Fuel Right}",
        "name": "IDF Mods Project F-16C CFT Fuel Right 1500lb",
        "weight": 680.0827540681,
    }
    IDF_Mods_Project_F_16I_CFT = {
        "clsid": "{IDF Mods Project F-16I CFT}",
        "name": "IDF Mods Project F-16I CFT",
        "weight": 408,
    }
    IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb = {
        "clsid": "{IDF Mods Project F-16I CFT Fuel Left}",
        "name": "IDF Mods Project F-16I CFT Fuel Left 1500lb",
        "weight": 680.0827540681,
    }
    IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb__370Gal = {
        "clsid": "{IDF Mods Project F-16I CFT Fuel Left + Fuel Tank 370}",
        "name": "IDF Mods Project F-16I CFT Fuel Left 1500lb + 370Gal",
        "weight": 2063.8845750252,
    }
    IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb__600Gal = {
        "clsid": "{600gal+CFT Fuel Left 1500lb}",
        "name": "IDF Mods Project F-16I CFT Fuel Left 1500lb + 600Gal",
        "weight": 2991.8895289931,
    }
    IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb = {
        "clsid": "{IDF Mods Project F-16I CFT Fuel Right}",
        "name": "IDF Mods Project F-16I CFT Fuel Right 1500lb",
        "weight": 680.0827540681,
    }
    IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb__370Gal = {
        "clsid": "{IDF Mods Project F-16I CFT Fuel Right + Fuel Tank 370}",
        "name": "IDF Mods Project F-16I CFT Fuel Right 1500lb + 370Gal",
        "weight": 2063.8845750252,
    }
    IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb__600Gal = {
        "clsid": "{600gal+CFT Fuel Right 1500lb}",
        "name": "IDF Mods Project F-16I CFT Fuel Right 1500lb + 600Gal",
        "weight": 2991.8895289931,
    }
    Ladder_F_16C = {"clsid": "{Ladder F-16C}", "name": "Ladder F-16C", "weight": 0}
    Python_5_Cover_Pylon_2 = {
        "clsid": "{Python 5 cover S 2}",
        "name": "Python 5 Cover Pylon 2",
        "weight": 0,
    }
    Python_5_Cover_Pylon_2_8 = {
        "clsid": "{Python 5 cover S 2-8}",
        "name": "Python 5 Cover Pylon 2-8",
        "weight": 0,
    }
    Python_5_Cover_Pylon_8 = {
        "clsid": "{Python 5 cover S 8}",
        "name": "Python 5 Cover Pylon 8",
        "weight": 0,
    }
    Remove_Before_Flight = {
        "clsid": "{IDF Mods Project RBF}",
        "name": "Remove Before Flight",
        "weight": 0,
    }
    Remove_Before_Flight_And_Ladder_F_16C = {
        "clsid": "{Remove Before Flight And Ladder F-16C}",
        "name": "Remove Before Flight And Ladder F-16C",
        "weight": 0,
    }
    Remove_Before_Flight_F_16C = {
        "clsid": "{Remove Before Flight F-16C}",
        "name": "Remove Before Flight F-16C",
        "weight": 0,
    }
    Remove_Before_Flight_With_TGP = {
        "clsid": "{Remove Before Flight With TGP F-16C}",
        "name": "Remove Before Flight With TGP",
        "weight": 0,
    }
    Remove_Before_Flight_With_TGP_And_Ladder_F_16C = {
        "clsid": "{Remove Before Flight With TGP And Ladder F-16C}",
        "name": "Remove Before Flight With TGP And Ladder F-16C",
        "weight": 0,
    }
    Remove_Before_Flight_without_Lantirn = {
        "clsid": "{IDF Mods Project Remove Before Flight without Lantirn}",
        "name": "Remove Before Flight without Lantirn",
        "weight": 0,
    }
    Remove_Before_Flight_without_TGP_ = {
        "clsid": "{IDF Mods Project Remove Before Flight without TGP}",
        "name": "Remove Before Flight without TGP ",
        "weight": 0,
    }
    Remove_Before_Flight_without_TGP_And_Lantirn = {
        "clsid": "{Remove Before Flight without TGP And Lantirn}",
        "name": "Remove Before Flight without TGP And Lantirn",
        "weight": 0,
    }
    Spice_2000_Cover_Pylon_3 = {
        "clsid": "{Spice 2000 cov S 4}",
        "name": "Spice 2000 Cover Pylon 3",
        "weight": 0,
    }
    Spice_2000_Cover_Pylon_3_7 = {
        "clsid": "{Spice 2000 cov S 4-6}",
        "name": "Spice 2000 Cover Pylon 3-7",
        "weight": 0,
    }
    Spice_2000_Cover_Pylon_7 = {
        "clsid": "{Spice 2000 cov S 6}",
        "name": "Spice 2000 Cover Pylon 7",
        "weight": 0,
    }
    _1ECM_Tail = {"clsid": "{1ECM_Tail}", "name": "1ECM Tail", "weight": 50}
    _2ECM_Tail = {"clsid": "{2ECM_Tail}", "name": "2ECM Tail", "weight": 50}
    Python_5_Training = {
        "clsid": "{Python-5 Training}",
        "name": "Python-5 Training",
        "weight": 105,
    }
    Pylon_3_4_GBU_10___2000lb_Laser_Guided_Bomb = {
        "clsid": "{BRUL657_2*GBU-10}",
        "name": "Pylon 3,4 GBU-10 - 2000lb Laser Guided Bomb",
        "weight": 1868,
    }
    Pylon_3_4_GBU_12___500lb_Laser_Guided_Bomb = {
        "clsid": "{BRUL657_2*GBU-12}",
        "name": "Pylon 3,4 GBU-12 - 500lb Laser Guided Bomb",
        "weight": 554,
    }
    Pylon_3_4_GBU_31 = {
        "clsid": "{BRUL657_2*GBU-31}",
        "name": "Pylon 3,4 GBU-31",
        "weight": 1868,
    }
    Pylon_3_4_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{BRUL657_2*GBU-31V}",
        "name": "Pylon 3,4 GBU-31(V)3/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 1962,
    }
    Pylon_3_4_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = {
        "clsid": "{BRUL557_2*GBU-38}",
        "name": "Pylon 3,4 GBU-38 - JDAM, 500lb GPS Guided Bomb",
        "weight": 482,
    }
    Pylon_3_4_Mk_82___500lb_GP_Bomb_LD = {
        "clsid": "{BRUL657_2*MK-82}",
        "name": "Pylon 3,4 Mk-82 - 500lb GP Bomb LD",
        "weight": 456,
    }
    Pylon_3_4_Mk_84___2000lb_GP_Bomb_LD = {
        "clsid": "{BRUL657_2*MK-84}",
        "name": "Pylon 3,4 Mk-84 - 2000lb GP Bomb LD",
        "weight": 1962,
    }
    Pylon_4_GBU_31 = {
        "clsid": "{BRUL657_1*GBU-31}",
        "name": "Pylon 4 GBU-31",
        "weight": 934,
    }
    Pylon_4_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{BRUL657_1*GBU-31V}",
        "name": "Pylon 4 GBU-31(V)3/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 981,
    }
    Pylon_4_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = {
        "clsid": "{BRUL657_1*GBU-38}",
        "name": "Pylon 4 GBU-38 - JDAM, 500lb GPS Guided Bomb",
        "weight": 241,
    }
    Pylon_6_7_GBU_10___2000lb_Laser_Guided_Bomb = {
        "clsid": "{BRUR657_2*GBU-10}",
        "name": "Pylon 6,7 GBU-10 - 2000lb Laser Guided Bomb",
        "weight": 1868,
    }
    Pylon_6_7_GBU_12___500lb_Laser_Guided_Bomb = {
        "clsid": "{BRUR657_2*GBU-12}",
        "name": "Pylon 6,7 GBU-12 - 500lb Laser Guided Bomb",
        "weight": 554,
    }
    Pylon_6_7_GBU_31 = {
        "clsid": "{BRUR657_2*GBU-31}",
        "name": "Pylon 6,7 GBU-31",
        "weight": 1868,
    }
    Pylon_6_7_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{BRUR657_2*GBU-31V}",
        "name": "Pylon 6,7 GBU-31(V)3/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 1962,
    }
    Pylon_6_7_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = {
        "clsid": "{BRUR557_2*GBU-38}",
        "name": "Pylon 6,7 GBU-38 - JDAM, 500lb GPS Guided Bomb",
        "weight": 482,
    }
    Pylon_6_7_Mk_82___500lb_GP_Bomb_LD = {
        "clsid": "{BRUR657_2*MK-82}",
        "name": "Pylon 6,7 Mk-82 - 500lb GP Bomb LD",
        "weight": 456,
    }
    Pylon_6_7_Mk_84___2000lb_GP_Bomb_LD = {
        "clsid": "{BRUR657_2*MK-84}",
        "name": "Pylon 6,7 Mk-84 - 2000lb GP Bomb LD",
        "weight": 1962,
    }
    Pylon_6_GBU_31 = {
        "clsid": "{BRUR657_1*GBU-31}",
        "name": "Pylon 6 GBU-31",
        "weight": 934,
    }
    Pylon_6_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = {
        "clsid": "{BRUR657_1*GBU-31V}",
        "name": "Pylon 6 GBU-31(V)3/B - JDAM, 2000lb GPS Guided Bomb",
        "weight": 981,
    }
    Pylon_6_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = {
        "clsid": "{BRUR657_1*GBU-38}",
        "name": "Pylon 6 GBU-38 - JDAM, 500lb GPS Guided Bomb",
        "weight": 241,
    }
    Fuel_tank_300_gal_Empty = {
        "clsid": "{IDF Mods Project 300gal Empty}",
        "name": "Fuel tank 300 gal Empty",
        "weight": 226,
    }


class F16IDFPylon4:
    Fuel_tank_600_gal = (4, WeaponsF16I.Fuel_tank_600_gal)
    Fuel_tank_600_gal__EMPTY_ = (4, WeaponsF16I.Fuel_tank_600_gal__EMPTY_)
    IDF_Mods_Project_Fuel_Tank_370_EMPTY = (
        4,
        WeaponsF16I.IDF_Mods_Project_Fuel_Tank_370_EMPTY,
    )
    IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb = (
        4,
        WeaponsF16I.IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb,
    )
    IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb__600Gal = (
        4,
        WeaponsF16I.IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb__600Gal,
    )
    IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb__370Gal = (
        4,
        WeaponsF16I.IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb__370Gal,
    )


class F16IDFPylon6:
    Fuel_tank_600_gal = (6, WeaponsF16I.Fuel_tank_600_gal)
    Fuel_tank_600_gal__EMPTY_ = (6, WeaponsF16I.Fuel_tank_600_gal__EMPTY_)
    IDF_Mods_Project_Fuel_Tank_370_EMPTY = (
        6,
        WeaponsF16I.IDF_Mods_Project_Fuel_Tank_370_EMPTY,
    )
    IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb = (
        6,
        WeaponsF16I.IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb,
    )
    IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb__370Gal = (
        6,
        WeaponsF16I.IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb__370Gal,
    )
    IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb__600Gal = (
        6,
        WeaponsF16I.IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb__600Gal,
    )


class Pylon13:
    ALQ_184 = (13, Weapons.ALQ_184)


class Pylon14:
    _2ECM_Tail = (14, WeaponsF16I._2ECM_Tail)
    _1ECM_Tail = (14, WeaponsF16I._1ECM_Tail)
    Barak_tail_2 = (14, WeaponsF16I.Barak_tail_2)
    Barak_tail_1 = (14, WeaponsF16I.Barak_tail_1)


class Pylon15:
    IDF_Mods_Project_F_16C_CFT = (15, WeaponsF16I.IDF_Mods_Project_F_16C_CFT)


class Pylon16:
    ECM_lights = (16, WeaponsF16I.ECM_lights)
    Barak_lights = (16, WeaponsF16I.Barak_lights)


class Pylon17:
    Remove_Before_Flight_With_TGP = (17, WeaponsF16I.Remove_Before_Flight_With_TGP)
    Ladder_F_16C = (17, WeaponsF16I.Ladder_F_16C)
    Remove_Before_Flight_F_16C = (17, WeaponsF16I.Remove_Before_Flight_F_16C)
    Remove_Before_Flight_And_Ladder_F_16C = (
        17,
        WeaponsF16I.Remove_Before_Flight_And_Ladder_F_16C,
    )
    Remove_Before_Flight_With_TGP_And_Ladder_F_16C = (
        17,
        WeaponsF16I.Remove_Before_Flight_With_TGP_And_Ladder_F_16C,
    )


inject_weapons(WeaponsF16I)


def inject_F16I() -> None:
    F_16C_50.pylons = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17}

    # Injects modified weapons from the IDF Mods Project F-16I Sufa
    # into pydcs databases via introspection.
    inject_pylon(F_16C_50.Pylon4, F16IDFPylon4)
    inject_pylon(F_16C_50.Pylon6, F16IDFPylon6)

    F_16C_50.Pylon13 = Pylon13
    F_16C_50.Pylon14 = Pylon14
    F_16C_50.Pylon15 = Pylon15
    F_16C_50.Pylon16 = Pylon16
    F_16C_50.Pylon17 = Pylon17


def eject_F16I() -> None:
    F_16C_50.pylons = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}

    # Injects modified weapons from the IDF Mods Project F-16I Sufa
    # into pydcs databases via introspection.
    eject_pylon(F_16C_50.Pylon4, F16IDFPylon4)
    eject_pylon(F_16C_50.Pylon6, F16IDFPylon6)

    for p in [13, 14, 15, 16, 17]:
        if hasattr(F_16C_50, f"Pylon{p}"):
            delattr(F_16C_50, f"Pylon{p}")


@planemod
class F_16D_52(PlaneType):
    id = "F-16D_52"
    flyable = True
    height = 5.02
    width = 9.45
    length = 14.52
    fuel_max = 2585.48
    max_speed = 2120.04
    chaff = 60
    flare = 60
    charge_total = 120
    chaff_charge_size = 1
    flare_charge_size = 1
    eplrs = True
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 305

    panel_radio = {
        1: {
            "channels": {
                1: 305,
                2: 264,
                4: 256,
                8: 257,
                16: 261,
                17: 267,
                9: 255,
                18: 251,
                5: 254,
                10: 262,
                20: 266,
                11: 259,
                3: 265,
                6: 250,
                12: 268,
                13: 269,
                7: 270,
                14: 260,
                19: 253,
                15: 263,
            },
        },
        2: {
            "channels": {
                1: 127,
                2: 135,
                4: 127,
                8: 128,
                16: 132,
                17: 138,
                9: 126,
                18: 122,
                5: 125,
                10: 133,
                20: 137,
                11: 130,
                3: 136,
                6: 121,
                12: 139,
                13: 140,
                7: 141,
                14: 131,
                19: 124,
                15: 134,
            },
        },
    }

    callnames: Dict[str, List[str]] = {
        "USA": [
            "Viper",
            "Venom",
            "Lobo",
            "Cowboy",
            "Python",
            "Rattler",
            "Panther",
            "Wolf",
            "Weasel",
            "Wild",
            "Ninja",
            "Jedi",
        ]
    }

    property_defaults: Dict[str, Any] = {
        "LAU3ROF": 0,
        "LaserCode100": 6,
        "LaserCode10": 8,
        "LaserCode1": 8,
        "HelmetMountedDevice": 1,
    }

    class Properties:
        class LAU3ROF:
            id = "LAU3ROF"

            class Values:
                Single = 0
                Ripple = 1

        class LaserCode100:
            id = "LaserCode100"

        class LaserCode10:
            id = "LaserCode10"

        class LaserCode1:
            id = "LaserCode1"

        class HelmetMountedDevice:
            id = "HelmetMountedDevice"

            class Values:
                Not_installed = 0
                JHMCS = 1
                NVG = 2

    livery_name = "F-16D_52"  # from type

    class Pylon1:
        AIM_9M_Sidewinder_IR_AAM = (1, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (1, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (1, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            1,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            1,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        CATM_9M = (1, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (1, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

        Python_5_Training = (1, WeaponsF16I.Python_5_Training)

    class Pylon2:
        AIM_9M_Sidewinder_IR_AAM = (2, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (2, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (2, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            2,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            2,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        CATM_9M = (2, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (2, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

        Python_5_Training = (1, WeaponsF16I.Python_5_Training)

    # ERRR <CLEAN>

    class Pylon3:
        AIM_9M_Sidewinder_IR_AAM = (3, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (3, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (3, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            3,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            3,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        CATM_9M = (3, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (3, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        LAU3_WP156 = (3, Weapons.LAU3_WP156)
        LAU3_WP1B = (3, Weapons.LAU3_WP1B)
        LAU3_WP61 = (3, Weapons.LAU3_WP61)
        LAU3_HE5 = (3, Weapons.LAU3_HE5)
        LAU3_HE151 = (3, Weapons.LAU3_HE151)
        BDU_50LD___500lb_Inert_Practice_Bomb_LD = (
            3,
            Weapons.BDU_50LD___500lb_Inert_Practice_Bomb_LD,
        )
        BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD = (
            3,
            Weapons.BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD,
        )
        BDU_50HD___500lb_Inert_Practice_Bomb_HD = (
            3,
            Weapons.BDU_50HD___500lb_Inert_Practice_Bomb_HD,
        )
        Mk_82___500lb_GP_Bomb_LD = (3, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (3, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            3,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (3, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD = (
            3,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD = (
            3,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD,
        )
        GBU_10___2000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (3, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        CBU_87___202_x_CEM_Cluster_Bomb = (3, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (3, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            3,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        BRU_57_with_2_x_CBU_105___10_x_SFW__CBU_with_WCMD = (
            3,
            Weapons.BRU_57_with_2_x_CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            3,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        BRU_57_with_2_x_CBU_103___202_x_CEM__CBU_with_WCMD = (
            3,
            Weapons.BRU_57_with_2_x_CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            3,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            3,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            3,
            Weapons.TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD = (
            3,
            Weapons.TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            3,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_117_AGM_65G = (3, Weapons.LAU_117_AGM_65G)
        LAU_117_AGM_65H = (3, Weapons.LAU_117_AGM_65H)
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            3,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_88_AGM_65D_ONE = (3, Weapons.LAU_88_AGM_65D_ONE)
        LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_ = (
            3,
            Weapons.LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_88_AGM_65H = (3, Weapons.LAU_88_AGM_65H)
        LAU_88_AGM_65H_3 = (3, Weapons.LAU_88_AGM_65H_3)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            3,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            Weapons.GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            3,
            Weapons.GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            Weapons.GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )
        BRU_57_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            Weapons.BRU_57_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        AGM_154A___JSOW_CEB__CBU_type_ = (3, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        MXU_648_TP = (3, Weapons.MXU_648_TP)
        ALQ_184 = (3, Weapons.ALQ_184)
        ALQ_184_Long = (3, Weapons.ALQ_184_Long)
        ALQ_131___ECM_Pod = (3, Weapons.ALQ_131___ECM_Pod)
        # ERRR <CLEAN>
        TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD = (
            3,
            Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            3,
            Weapons.TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            3,
            Weapons.TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_2_x_GBU_12___500lb_Laser_Guided_Bomb = (
            3,
            Weapons.TER_9A_with_2_x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb = (
            3,
            Weapons.TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb,
        )
        TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb = (
            3,
            Weapons.TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb,
        )
        LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM_ = (
            3,
            Weapons.LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_88_AGM_65H_2_L = (3, Weapons.LAU_88_AGM_65H_2_L)
        Pylon_3_4_Mk_82___500lb_GP_Bomb_LD = (
            3,
            WeaponsF16I.Pylon_3_4_Mk_82___500lb_GP_Bomb_LD,
        )
        Pylon_3_4_Mk_84___2000lb_GP_Bomb_LD = (
            3,
            WeaponsF16I.Pylon_3_4_Mk_84___2000lb_GP_Bomb_LD,
        )
        Pylon_3_4_GBU_31 = (3, WeaponsF16I.Pylon_3_4_GBU_31)
        Pylon_3_4_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            WeaponsF16I.Pylon_3_4_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )
        Pylon_3_4_GBU_12___500lb_Laser_Guided_Bomb = (
            3,
            WeaponsF16I.Pylon_3_4_GBU_12___500lb_Laser_Guided_Bomb,
        )
        Pylon_3_4_GBU_10___2000lb_Laser_Guided_Bomb = (
            3,
            WeaponsF16I.Pylon_3_4_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        Pylon_3_4_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            WeaponsF16I.Pylon_3_4_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        Pylon_4_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            WeaponsF16I.Pylon_4_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        Pylon_4_GBU_31 = (3, WeaponsF16I.Pylon_4_GBU_31)
        Pylon_4_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            WeaponsF16I.Pylon_4_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )

    class Pylon4:
        LAU3_WP156 = (4, Weapons.LAU3_WP156)
        LAU3_WP1B = (4, Weapons.LAU3_WP1B)
        LAU3_WP61 = (4, Weapons.LAU3_WP61)
        LAU3_HE5 = (4, Weapons.LAU3_HE5)
        LAU3_HE151 = (4, Weapons.LAU3_HE151)
        BDU_50LD___500lb_Inert_Practice_Bomb_LD = (
            4,
            Weapons.BDU_50LD___500lb_Inert_Practice_Bomb_LD,
        )
        BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD = (
            4,
            Weapons.BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD,
        )
        BDU_50HD___500lb_Inert_Practice_Bomb_HD = (
            4,
            Weapons.BDU_50HD___500lb_Inert_Practice_Bomb_HD,
        )
        Mk_82___500lb_GP_Bomb_LD = (4, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (4, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            4,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (4, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD = (
            4,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD = (
            4,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD,
        )
        GBU_10___2000lb_Laser_Guided_Bomb = (
            4,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (4, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb = (
            4,
            Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        CBU_87___202_x_CEM_Cluster_Bomb = (4, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (4, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            4,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            4,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            4,
            Weapons.TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD = (
            4,
            Weapons.TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb = (
            4,
            Weapons.TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb,
        )
        TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb = (
            4,
            Weapons.TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb,
        )
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            4,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        Fuel_tank_370_gal = (4, Weapons.Fuel_tank_370_gal)
        MXU_648_TP = (4, Weapons.MXU_648_TP)
        Fuel_tank_600_gal = (4, WeaponsF16I.Fuel_tank_600_gal)
        Fuel_tank_600_gal__EMPTY_ = (4, WeaponsF16I.Fuel_tank_600_gal__EMPTY_)
        IDF_Mods_Project_Fuel_Tank_370_EMPTY = (
            4,
            WeaponsF16I.IDF_Mods_Project_Fuel_Tank_370_EMPTY,
        )
        # ERRR <CLEAN>
        TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD = (
            4,
            Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            4,
            Weapons.TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            4,
            Weapons.TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb = (
            4,
            Weapons.TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb,
        )
        TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb = (
            4,
            Weapons.TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb,
        )
        IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb = (
            4,
            WeaponsF16I.IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb,
        )
        IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb__600Gal = (
            4,
            WeaponsF16I.IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb__600Gal,
        )
        IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb__370Gal = (
            4,
            WeaponsF16I.IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb__370Gal,
        )

    class Pylon5:
        Fuel_tank_300_gal = (5, Weapons.Fuel_tank_300_gal)
        Fuel_tank_300_gal_Empty = (5, WeaponsF16I.Fuel_tank_300_gal_Empty)
        MXU_648_TP = (5, Weapons.MXU_648_TP)
        ALQ_184 = (5, Weapons.ALQ_184)
        ALQ_184_Long = (5, Weapons.ALQ_184_Long)
        ALQ_131___ECM_Pod = (5, Weapons.ALQ_131___ECM_Pod)

    # ERRR <CLEAN>

    class Pylon6:
        LAU3_WP156 = (6, Weapons.LAU3_WP156)
        LAU3_WP1B = (6, Weapons.LAU3_WP1B)
        LAU3_WP61 = (6, Weapons.LAU3_WP61)
        LAU3_HE5 = (6, Weapons.LAU3_HE5)
        LAU3_HE151 = (6, Weapons.LAU3_HE151)
        BDU_50LD___500lb_Inert_Practice_Bomb_LD = (
            6,
            Weapons.BDU_50LD___500lb_Inert_Practice_Bomb_LD,
        )
        BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD = (
            6,
            Weapons.BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD,
        )
        BDU_50HD___500lb_Inert_Practice_Bomb_HD = (
            6,
            Weapons.BDU_50HD___500lb_Inert_Practice_Bomb_HD,
        )
        Mk_82___500lb_GP_Bomb_LD = (6, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (6, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            6,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (6, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD = (
            6,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD = (
            6,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD,
        )
        GBU_10___2000lb_Laser_Guided_Bomb = (
            6,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (6, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb = (
            6,
            Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        CBU_87___202_x_CEM_Cluster_Bomb = (6, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (6, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            6,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            6,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            6,
            Weapons.TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD = (
            6,
            Weapons.TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb = (
            6,
            Weapons.TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb,
        )
        TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb = (
            6,
            Weapons.TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb,
        )
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            6,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        Fuel_tank_370_gal = (6, Weapons.Fuel_tank_370_gal)
        MXU_648_TP = (6, Weapons.MXU_648_TP)
        Fuel_tank_600_gal = (6, WeaponsF16I.Fuel_tank_600_gal)
        Fuel_tank_600_gal__EMPTY_ = (6, WeaponsF16I.Fuel_tank_600_gal__EMPTY_)
        IDF_Mods_Project_Fuel_Tank_370_EMPTY = (
            6,
            WeaponsF16I.IDF_Mods_Project_Fuel_Tank_370_EMPTY,
        )
        # ERRR <CLEAN>
        TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD_ = (
            6,
            Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD_,
        )
        TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_ = (
            6,
            Weapons.TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_,
        )
        TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD_ = (
            6,
            Weapons.TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD_,
        )
        TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb_ = (
            6,
            Weapons.TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb_,
        )
        TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb_ = (
            6,
            Weapons.TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb_,
        )
        IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb = (
            6,
            WeaponsF16I.IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb,
        )
        IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb__370Gal = (
            6,
            WeaponsF16I.IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb__370Gal,
        )
        IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb__600Gal = (
            6,
            WeaponsF16I.IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb__600Gal,
        )

    class Pylon7:
        AIM_9M_Sidewinder_IR_AAM = (7, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (7, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (7, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            7,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            7,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        CATM_9M = (7, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (7, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        LAU3_WP156 = (7, Weapons.LAU3_WP156)
        LAU3_WP1B = (7, Weapons.LAU3_WP1B)
        LAU3_WP61 = (7, Weapons.LAU3_WP61)
        LAU3_HE5 = (7, Weapons.LAU3_HE5)
        LAU3_HE151 = (7, Weapons.LAU3_HE151)
        BDU_50LD___500lb_Inert_Practice_Bomb_LD = (
            7,
            Weapons.BDU_50LD___500lb_Inert_Practice_Bomb_LD,
        )
        BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD = (
            7,
            Weapons.BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD,
        )
        BDU_50HD___500lb_Inert_Practice_Bomb_HD = (
            7,
            Weapons.BDU_50HD___500lb_Inert_Practice_Bomb_HD,
        )
        Mk_82___500lb_GP_Bomb_LD = (7, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (7, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            7,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (7, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD = (
            7,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD = (
            7,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD,
        )
        GBU_10___2000lb_Laser_Guided_Bomb = (
            7,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (7, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb = (
            7,
            Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        CBU_87___202_x_CEM_Cluster_Bomb = (7, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (7, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            7,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        BRU_57_with_2_x_CBU_105___10_x_SFW__CBU_with_WCMD = (
            7,
            Weapons.BRU_57_with_2_x_CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            7,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        BRU_57_with_2_x_CBU_103___202_x_CEM__CBU_with_WCMD = (
            7,
            Weapons.BRU_57_with_2_x_CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            7,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            7,
            Weapons.TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD = (
            7,
            Weapons.TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            7,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_117_AGM_65G = (7, Weapons.LAU_117_AGM_65G)
        LAU_117_AGM_65H = (7, Weapons.LAU_117_AGM_65H)
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            7,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_88_AGM_65D_ONE = (7, Weapons.LAU_88_AGM_65D_ONE)
        LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_ = (
            7,
            Weapons.LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_88_AGM_65H = (7, Weapons.LAU_88_AGM_65H)
        LAU_88_AGM_65H_3 = (7, Weapons.LAU_88_AGM_65H_3)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            7,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            Weapons.GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            7,
            Weapons.GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            Weapons.GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )
        BRU_57_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            Weapons.BRU_57_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        AGM_154A___JSOW_CEB__CBU_type_ = (7, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        MXU_648_TP = (7, Weapons.MXU_648_TP)
        ALQ_184 = (7, Weapons.ALQ_184)
        ALQ_184_Long = (7, Weapons.ALQ_184_Long)
        ALQ_131___ECM_Pod = (7, Weapons.ALQ_131___ECM_Pod)
        # ERRR <CLEAN>
        TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD_ = (
            7,
            Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD_,
        )
        TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_ = (
            7,
            Weapons.TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_,
        )
        TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD_ = (
            7,
            Weapons.TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD_,
        )
        TER_9A_with_2_x_GBU_12___500lb_Laser_Guided_Bomb_ = (
            7,
            Weapons.TER_9A_with_2_x_GBU_12___500lb_Laser_Guided_Bomb_,
        )
        TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb_ = (
            7,
            Weapons.TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb_,
        )
        TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb_ = (
            7,
            Weapons.TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb_,
        )
        LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM__ = (
            7,
            Weapons.LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM__,
        )
        LAU_88_AGM_65H_2_R = (7, Weapons.LAU_88_AGM_65H_2_R)
        Pylon_6_7_Mk_82___500lb_GP_Bomb_LD = (
            7,
            WeaponsF16I.Pylon_6_7_Mk_82___500lb_GP_Bomb_LD,
        )
        Pylon_6_7_Mk_84___2000lb_GP_Bomb_LD = (
            7,
            WeaponsF16I.Pylon_6_7_Mk_84___2000lb_GP_Bomb_LD,
        )
        Pylon_6_7_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsF16I.Pylon_6_7_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )
        Pylon_6_7_GBU_31 = (7, WeaponsF16I.Pylon_6_7_GBU_31)
        Pylon_6_7_GBU_12___500lb_Laser_Guided_Bomb = (
            7,
            WeaponsF16I.Pylon_6_7_GBU_12___500lb_Laser_Guided_Bomb,
        )
        Pylon_6_7_GBU_10___2000lb_Laser_Guided_Bomb = (
            7,
            WeaponsF16I.Pylon_6_7_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        Pylon_6_7_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            WeaponsF16I.Pylon_6_7_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        Pylon_6_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            WeaponsF16I.Pylon_6_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        Pylon_6_GBU_31 = (7, WeaponsF16I.Pylon_6_GBU_31)
        Pylon_6_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsF16I.Pylon_6_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )

    class Pylon8:
        AIM_9M_Sidewinder_IR_AAM = (8, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (8, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (8, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            8,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            8,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        CATM_9M = (8, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (8, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

        Python_5_Training = (1, WeaponsF16I.Python_5_Training)

    # ERRR <CLEAN>

    class Pylon9:
        AIM_9M_Sidewinder_IR_AAM = (9, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (9, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (9, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            9,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            9,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        CATM_9M = (9, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (9, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

        Python_5_Training = (1, WeaponsF16I.Python_5_Training)

    class Pylon10:
        AN_ASQ_213_HTS___HARM_Targeting_System = (
            10,
            Weapons.AN_ASQ_213_HTS___HARM_Targeting_System,
        )

    class Pylon11:
        AN_AAQ_28_LITENING___Targeting_Pod = (
            11,
            Weapons.AN_AAQ_28_LITENING___Targeting_Pod,
        )

    class Pylon12:
        Smoke_Generator___red_ = (12, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (12, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (12, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (12, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (12, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (12, Weapons.Smoke_Generator___orange_)

    class Pylon13:
        ALQ_184_Long = (13, Weapons.ALQ_184_Long)

    class Pylon14:
        Crew_Ladder_For_CFT = (14, WeaponsF16I.Crew_Ladder_For_CFT)
        Crew_Ladder_No_CFT = (14, WeaponsF16I.Crew_Ladder_No_CFT)

    class Pylon15:
        Remove_Before_Flight = (15, WeaponsF16I.Remove_Before_Flight)
        Remove_Before_Flight_without_Lantirn = (
            15,
            WeaponsF16I.Remove_Before_Flight_without_Lantirn,
        )
        Remove_Before_Flight_without_TGP_ = (
            15,
            WeaponsF16I.Remove_Before_Flight_without_TGP_,
        )
        Remove_Before_Flight_without_TGP_And_Lantirn = (
            15,
            WeaponsF16I.Remove_Before_Flight_without_TGP_And_Lantirn,
        )

    class Pylon16:
        IDF_Mods_Project_F_16I_CFT = (16, WeaponsF16I.IDF_Mods_Project_F_16I_CFT)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.PinpointStrike,
        task.CAS,
        task.GroundAttack,
        task.RunwayAttack,
        task.SEAD,
        task.AFAC,
        task.AntishipStrike,
        task.Reconnaissance,
    ]
    task_default = task.CAP


@planemod
class F_16D_50(PlaneType):
    id = "F-16D_50"
    flyable = True
    height = 5.02
    width = 9.45
    length = 14.52
    fuel_max = 2585.48
    max_speed = 2120.04
    chaff = 60
    flare = 60
    charge_total = 120
    chaff_charge_size = 1
    flare_charge_size = 1
    eplrs = True
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 305

    panel_radio = {
        1: {
            "channels": {
                1: 305,
                2: 264,
                4: 256,
                8: 257,
                16: 261,
                17: 267,
                9: 255,
                18: 251,
                5: 254,
                10: 262,
                20: 266,
                11: 259,
                3: 265,
                6: 250,
                12: 268,
                13: 269,
                7: 270,
                14: 260,
                19: 253,
                15: 263,
            },
        },
        2: {
            "channels": {
                1: 127,
                2: 135,
                4: 127,
                8: 128,
                16: 132,
                17: 138,
                9: 126,
                18: 122,
                5: 125,
                10: 133,
                20: 137,
                11: 130,
                3: 136,
                6: 121,
                12: 139,
                13: 140,
                7: 141,
                14: 131,
                19: 124,
                15: 134,
            },
        },
    }

    callnames: Dict[str, List[str]] = {
        "USA": [
            "Viper",
            "Venom",
            "Lobo",
            "Cowboy",
            "Python",
            "Rattler",
            "Panther",
            "Wolf",
            "Weasel",
            "Wild",
            "Ninja",
            "Jedi",
        ]
    }

    property_defaults: Dict[str, Any] = {
        "LAU3ROF": 0,
        "LaserCode100": 6,
        "LaserCode10": 8,
        "LaserCode1": 8,
        "HelmetMountedDevice": 1,
    }

    class Properties:
        class LAU3ROF:
            id = "LAU3ROF"

            class Values:
                Single = 0
                Ripple = 1

        class LaserCode100:
            id = "LaserCode100"

        class LaserCode10:
            id = "LaserCode10"

        class LaserCode1:
            id = "LaserCode1"

        class HelmetMountedDevice:
            id = "HelmetMountedDevice"

            class Values:
                Not_installed = 0
                JHMCS = 1
                NVG = 2

    livery_name = "F-16D_50"  # from type

    class Pylon1:
        AIM_9M_Sidewinder_IR_AAM = (1, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (1, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (1, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            1,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            1,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        CATM_9M = (1, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (1, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

        Python_5_Training = (1, WeaponsF16I.Python_5_Training)

    class Pylon2:
        AIM_9M_Sidewinder_IR_AAM = (2, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (2, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (2, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            2,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            2,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        CATM_9M = (2, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (2, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

        Python_5_Training = (1, WeaponsF16I.Python_5_Training)

    # ERRR <CLEAN>

    class Pylon3:
        AIM_9M_Sidewinder_IR_AAM = (3, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (3, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (3, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            3,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            3,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        CATM_9M = (3, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (3, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        LAU3_WP156 = (3, Weapons.LAU3_WP156)
        LAU3_WP1B = (3, Weapons.LAU3_WP1B)
        LAU3_WP61 = (3, Weapons.LAU3_WP61)
        LAU3_HE5 = (3, Weapons.LAU3_HE5)
        LAU3_HE151 = (3, Weapons.LAU3_HE151)
        BDU_50LD___500lb_Inert_Practice_Bomb_LD = (
            3,
            Weapons.BDU_50LD___500lb_Inert_Practice_Bomb_LD,
        )
        BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD = (
            3,
            Weapons.BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD,
        )
        BDU_50HD___500lb_Inert_Practice_Bomb_HD = (
            3,
            Weapons.BDU_50HD___500lb_Inert_Practice_Bomb_HD,
        )
        Mk_82___500lb_GP_Bomb_LD = (3, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (3, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            3,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (3, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD = (
            3,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD = (
            3,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD,
        )
        GBU_10___2000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (3, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        CBU_87___202_x_CEM_Cluster_Bomb = (3, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (3, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            3,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        BRU_57_with_2_x_CBU_105___10_x_SFW__CBU_with_WCMD = (
            3,
            Weapons.BRU_57_with_2_x_CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            3,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        BRU_57_with_2_x_CBU_103___202_x_CEM__CBU_with_WCMD = (
            3,
            Weapons.BRU_57_with_2_x_CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            3,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            3,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            3,
            Weapons.TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD = (
            3,
            Weapons.TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            3,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_117_AGM_65G = (3, Weapons.LAU_117_AGM_65G)
        LAU_117_AGM_65H = (3, Weapons.LAU_117_AGM_65H)
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            3,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_88_AGM_65D_ONE = (3, Weapons.LAU_88_AGM_65D_ONE)
        LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_ = (
            3,
            Weapons.LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_88_AGM_65H = (3, Weapons.LAU_88_AGM_65H)
        LAU_88_AGM_65H_3 = (3, Weapons.LAU_88_AGM_65H_3)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            3,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            Weapons.GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            3,
            Weapons.GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            Weapons.GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )
        BRU_57_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            Weapons.BRU_57_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        AGM_154A___JSOW_CEB__CBU_type_ = (3, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        MXU_648_TP = (3, Weapons.MXU_648_TP)
        ALQ_184 = (3, Weapons.ALQ_184)
        ALQ_184_Long = (3, Weapons.ALQ_184_Long)
        ALQ_131___ECM_Pod = (3, Weapons.ALQ_131___ECM_Pod)
        # ERRR <CLEAN>
        TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD = (
            3,
            Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            3,
            Weapons.TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            3,
            Weapons.TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_2_x_GBU_12___500lb_Laser_Guided_Bomb = (
            3,
            Weapons.TER_9A_with_2_x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb = (
            3,
            Weapons.TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb,
        )
        TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb = (
            3,
            Weapons.TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb,
        )
        LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM_ = (
            3,
            Weapons.LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_88_AGM_65H_2_L = (3, Weapons.LAU_88_AGM_65H_2_L)
        Pylon_3_4_Mk_82___500lb_GP_Bomb_LD = (
            3,
            WeaponsF16I.Pylon_3_4_Mk_82___500lb_GP_Bomb_LD,
        )
        Pylon_3_4_Mk_84___2000lb_GP_Bomb_LD = (
            3,
            WeaponsF16I.Pylon_3_4_Mk_84___2000lb_GP_Bomb_LD,
        )
        Pylon_3_4_GBU_31 = (3, WeaponsF16I.Pylon_3_4_GBU_31)
        Pylon_3_4_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            WeaponsF16I.Pylon_3_4_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )
        Pylon_3_4_GBU_12___500lb_Laser_Guided_Bomb = (
            3,
            WeaponsF16I.Pylon_3_4_GBU_12___500lb_Laser_Guided_Bomb,
        )
        Pylon_3_4_GBU_10___2000lb_Laser_Guided_Bomb = (
            3,
            WeaponsF16I.Pylon_3_4_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        Pylon_3_4_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            WeaponsF16I.Pylon_3_4_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        Pylon_4_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            WeaponsF16I.Pylon_4_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        Pylon_4_GBU_31 = (3, WeaponsF16I.Pylon_4_GBU_31)
        Pylon_4_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            WeaponsF16I.Pylon_4_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )

    class Pylon4:
        LAU3_WP156 = (4, Weapons.LAU3_WP156)
        LAU3_WP1B = (4, Weapons.LAU3_WP1B)
        LAU3_WP61 = (4, Weapons.LAU3_WP61)
        LAU3_HE5 = (4, Weapons.LAU3_HE5)
        LAU3_HE151 = (4, Weapons.LAU3_HE151)
        BDU_50LD___500lb_Inert_Practice_Bomb_LD = (
            4,
            Weapons.BDU_50LD___500lb_Inert_Practice_Bomb_LD,
        )
        BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD = (
            4,
            Weapons.BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD,
        )
        BDU_50HD___500lb_Inert_Practice_Bomb_HD = (
            4,
            Weapons.BDU_50HD___500lb_Inert_Practice_Bomb_HD,
        )
        Mk_82___500lb_GP_Bomb_LD = (4, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (4, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            4,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (4, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD = (
            4,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD = (
            4,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD,
        )
        GBU_10___2000lb_Laser_Guided_Bomb = (
            4,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (4, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb = (
            4,
            Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        CBU_87___202_x_CEM_Cluster_Bomb = (4, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (4, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            4,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            4,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            4,
            Weapons.TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD = (
            4,
            Weapons.TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb = (
            4,
            Weapons.TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb,
        )
        TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb = (
            4,
            Weapons.TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb,
        )
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            4,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        Fuel_tank_370_gal = (4, Weapons.Fuel_tank_370_gal)
        MXU_648_TP = (4, Weapons.MXU_648_TP)
        Fuel_tank_600_gal = (4, WeaponsF16I.Fuel_tank_600_gal)
        Fuel_tank_600_gal__EMPTY_ = (4, WeaponsF16I.Fuel_tank_600_gal__EMPTY_)
        IDF_Mods_Project_Fuel_Tank_370_EMPTY = (
            4,
            WeaponsF16I.IDF_Mods_Project_Fuel_Tank_370_EMPTY,
        )
        # ERRR <CLEAN>
        TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD = (
            4,
            Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            4,
            Weapons.TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            4,
            Weapons.TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb = (
            4,
            Weapons.TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb,
        )
        TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb = (
            4,
            Weapons.TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb,
        )
        IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb = (
            4,
            WeaponsF16I.IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb,
        )
        IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb__600Gal = (
            4,
            WeaponsF16I.IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb__600Gal,
        )
        IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb__370Gal = (
            4,
            WeaponsF16I.IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb__370Gal,
        )

    class Pylon5:
        Fuel_tank_300_gal = (5, Weapons.Fuel_tank_300_gal)
        Fuel_tank_300_gal_Empty = (5, WeaponsF16I.Fuel_tank_300_gal_Empty)
        MXU_648_TP = (5, Weapons.MXU_648_TP)
        ALQ_184 = (5, Weapons.ALQ_184)
        ALQ_184_Long = (5, Weapons.ALQ_184_Long)
        ALQ_131___ECM_Pod = (5, Weapons.ALQ_131___ECM_Pod)

    # ERRR <CLEAN>

    class Pylon6:
        LAU3_WP156 = (6, Weapons.LAU3_WP156)
        LAU3_WP1B = (6, Weapons.LAU3_WP1B)
        LAU3_WP61 = (6, Weapons.LAU3_WP61)
        LAU3_HE5 = (6, Weapons.LAU3_HE5)
        LAU3_HE151 = (6, Weapons.LAU3_HE151)
        BDU_50LD___500lb_Inert_Practice_Bomb_LD = (
            6,
            Weapons.BDU_50LD___500lb_Inert_Practice_Bomb_LD,
        )
        BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD = (
            6,
            Weapons.BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD,
        )
        BDU_50HD___500lb_Inert_Practice_Bomb_HD = (
            6,
            Weapons.BDU_50HD___500lb_Inert_Practice_Bomb_HD,
        )
        Mk_82___500lb_GP_Bomb_LD = (6, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (6, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            6,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (6, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD = (
            6,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD = (
            6,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD,
        )
        GBU_10___2000lb_Laser_Guided_Bomb = (
            6,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (6, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb = (
            6,
            Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        CBU_87___202_x_CEM_Cluster_Bomb = (6, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (6, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            6,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            6,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            6,
            Weapons.TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD = (
            6,
            Weapons.TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb = (
            6,
            Weapons.TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb,
        )
        TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb = (
            6,
            Weapons.TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb,
        )
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            6,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        Fuel_tank_370_gal = (6, Weapons.Fuel_tank_370_gal)
        MXU_648_TP = (6, Weapons.MXU_648_TP)
        Fuel_tank_600_gal = (6, WeaponsF16I.Fuel_tank_600_gal)
        Fuel_tank_600_gal__EMPTY_ = (6, WeaponsF16I.Fuel_tank_600_gal__EMPTY_)
        IDF_Mods_Project_Fuel_Tank_370_EMPTY = (
            6,
            WeaponsF16I.IDF_Mods_Project_Fuel_Tank_370_EMPTY,
        )
        # ERRR <CLEAN>
        TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD_ = (
            6,
            Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD_,
        )
        TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_ = (
            6,
            Weapons.TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_,
        )
        TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD_ = (
            6,
            Weapons.TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD_,
        )
        TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb_ = (
            6,
            Weapons.TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb_,
        )
        TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb_ = (
            6,
            Weapons.TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb_,
        )
        IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb = (
            6,
            WeaponsF16I.IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb,
        )
        IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb__370Gal = (
            6,
            WeaponsF16I.IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb__370Gal,
        )
        IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb__600Gal = (
            6,
            WeaponsF16I.IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb__600Gal,
        )

    class Pylon7:
        AIM_9M_Sidewinder_IR_AAM = (7, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (7, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (7, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            7,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            7,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        CATM_9M = (7, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (7, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        LAU3_WP156 = (7, Weapons.LAU3_WP156)
        LAU3_WP1B = (7, Weapons.LAU3_WP1B)
        LAU3_WP61 = (7, Weapons.LAU3_WP61)
        LAU3_HE5 = (7, Weapons.LAU3_HE5)
        LAU3_HE151 = (7, Weapons.LAU3_HE151)
        BDU_50LD___500lb_Inert_Practice_Bomb_LD = (
            7,
            Weapons.BDU_50LD___500lb_Inert_Practice_Bomb_LD,
        )
        BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD = (
            7,
            Weapons.BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD,
        )
        BDU_50HD___500lb_Inert_Practice_Bomb_HD = (
            7,
            Weapons.BDU_50HD___500lb_Inert_Practice_Bomb_HD,
        )
        Mk_82___500lb_GP_Bomb_LD = (7, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (7, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            7,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (7, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD = (
            7,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD = (
            7,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD,
        )
        GBU_10___2000lb_Laser_Guided_Bomb = (
            7,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (7, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb = (
            7,
            Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        CBU_87___202_x_CEM_Cluster_Bomb = (7, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (7, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            7,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        BRU_57_with_2_x_CBU_105___10_x_SFW__CBU_with_WCMD = (
            7,
            Weapons.BRU_57_with_2_x_CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            7,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        BRU_57_with_2_x_CBU_103___202_x_CEM__CBU_with_WCMD = (
            7,
            Weapons.BRU_57_with_2_x_CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            7,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            7,
            Weapons.TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD = (
            7,
            Weapons.TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            7,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_117_AGM_65G = (7, Weapons.LAU_117_AGM_65G)
        LAU_117_AGM_65H = (7, Weapons.LAU_117_AGM_65H)
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            7,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_88_AGM_65D_ONE = (7, Weapons.LAU_88_AGM_65D_ONE)
        LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_ = (
            7,
            Weapons.LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_88_AGM_65H = (7, Weapons.LAU_88_AGM_65H)
        LAU_88_AGM_65H_3 = (7, Weapons.LAU_88_AGM_65H_3)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            7,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            Weapons.GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            7,
            Weapons.GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            Weapons.GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )
        BRU_57_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            Weapons.BRU_57_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        AGM_154A___JSOW_CEB__CBU_type_ = (7, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        MXU_648_TP = (7, Weapons.MXU_648_TP)
        ALQ_184 = (7, Weapons.ALQ_184)
        ALQ_184_Long = (7, Weapons.ALQ_184_Long)
        ALQ_131___ECM_Pod = (7, Weapons.ALQ_131___ECM_Pod)
        # ERRR <CLEAN>
        TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD_ = (
            7,
            Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD_,
        )
        TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_ = (
            7,
            Weapons.TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_,
        )
        TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD_ = (
            7,
            Weapons.TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD_,
        )
        TER_9A_with_2_x_GBU_12___500lb_Laser_Guided_Bomb_ = (
            7,
            Weapons.TER_9A_with_2_x_GBU_12___500lb_Laser_Guided_Bomb_,
        )
        TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb_ = (
            7,
            Weapons.TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb_,
        )
        TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb_ = (
            7,
            Weapons.TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb_,
        )
        LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM__ = (
            7,
            Weapons.LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM__,
        )
        LAU_88_AGM_65H_2_R = (7, Weapons.LAU_88_AGM_65H_2_R)
        Pylon_6_7_Mk_82___500lb_GP_Bomb_LD = (
            7,
            WeaponsF16I.Pylon_6_7_Mk_82___500lb_GP_Bomb_LD,
        )
        Pylon_6_7_Mk_84___2000lb_GP_Bomb_LD = (
            7,
            WeaponsF16I.Pylon_6_7_Mk_84___2000lb_GP_Bomb_LD,
        )
        Pylon_6_7_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsF16I.Pylon_6_7_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )
        Pylon_6_7_GBU_31 = (7, WeaponsF16I.Pylon_6_7_GBU_31)
        Pylon_6_7_GBU_12___500lb_Laser_Guided_Bomb = (
            7,
            WeaponsF16I.Pylon_6_7_GBU_12___500lb_Laser_Guided_Bomb,
        )
        Pylon_6_7_GBU_10___2000lb_Laser_Guided_Bomb = (
            7,
            WeaponsF16I.Pylon_6_7_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        Pylon_6_7_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            WeaponsF16I.Pylon_6_7_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        Pylon_6_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            WeaponsF16I.Pylon_6_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        Pylon_6_GBU_31 = (7, WeaponsF16I.Pylon_6_GBU_31)
        Pylon_6_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsF16I.Pylon_6_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )

    class Pylon8:
        AIM_9M_Sidewinder_IR_AAM = (8, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (8, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (8, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            8,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            8,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        CATM_9M = (8, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (8, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

        Python_5_Training = (1, WeaponsF16I.Python_5_Training)

    # ERRR <CLEAN>

    class Pylon9:
        AIM_9M_Sidewinder_IR_AAM = (9, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (9, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (9, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            9,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            9,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        CATM_9M = (9, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (9, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

        Python_5_Training = (1, WeaponsF16I.Python_5_Training)

    class Pylon10:
        AN_ASQ_213_HTS___HARM_Targeting_System = (
            10,
            Weapons.AN_ASQ_213_HTS___HARM_Targeting_System,
        )

    class Pylon11:
        AN_AAQ_28_LITENING___Targeting_Pod = (
            11,
            Weapons.AN_AAQ_28_LITENING___Targeting_Pod,
        )

    class Pylon12:
        Smoke_Generator___red_ = (12, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (12, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (12, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (12, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (12, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (12, Weapons.Smoke_Generator___orange_)

    class Pylon13:
        ALQ_184_Long = (13, Weapons.ALQ_184_Long)

    class Pylon14:
        Crew_Ladder_For_CFT = (14, WeaponsF16I.Crew_Ladder_For_CFT)
        Crew_Ladder_No_CFT = (14, WeaponsF16I.Crew_Ladder_No_CFT)

    class Pylon15:
        Remove_Before_Flight = (15, WeaponsF16I.Remove_Before_Flight)
        Remove_Before_Flight_without_Lantirn = (
            15,
            WeaponsF16I.Remove_Before_Flight_without_Lantirn,
        )
        Remove_Before_Flight_without_TGP_ = (
            15,
            WeaponsF16I.Remove_Before_Flight_without_TGP_,
        )
        Remove_Before_Flight_without_TGP_And_Lantirn = (
            15,
            WeaponsF16I.Remove_Before_Flight_without_TGP_And_Lantirn,
        )

    class Pylon16:
        IDF_Mods_Project_F_16I_CFT = (16, WeaponsF16I.IDF_Mods_Project_F_16I_CFT)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.PinpointStrike,
        task.CAS,
        task.GroundAttack,
        task.RunwayAttack,
        task.SEAD,
        task.AFAC,
        task.AntishipStrike,
        task.Reconnaissance,
    ]
    task_default = task.CAP


@planemod
class F_16D_52_NS(PlaneType):
    id = "F-16D_52_NS"
    flyable = True
    height = 5.02
    width = 9.45
    length = 14.52
    fuel_max = 2585.48
    max_speed = 2120.04
    chaff = 60
    flare = 60
    charge_total = 120
    chaff_charge_size = 1
    flare_charge_size = 1
    eplrs = True
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 305

    panel_radio = {
        1: {
            "channels": {
                1: 305,
                2: 264,
                4: 256,
                8: 257,
                16: 261,
                17: 267,
                9: 255,
                18: 251,
                5: 254,
                10: 262,
                20: 266,
                11: 259,
                3: 265,
                6: 250,
                12: 268,
                13: 269,
                7: 270,
                14: 260,
                19: 253,
                15: 263,
            },
        },
        2: {
            "channels": {
                1: 127,
                2: 135,
                4: 127,
                8: 128,
                16: 132,
                17: 138,
                9: 126,
                18: 122,
                5: 125,
                10: 133,
                20: 137,
                11: 130,
                3: 136,
                6: 121,
                12: 139,
                13: 140,
                7: 141,
                14: 131,
                19: 124,
                15: 134,
            },
        },
    }

    callnames: Dict[str, List[str]] = {
        "USA": [
            "Viper",
            "Venom",
            "Lobo",
            "Cowboy",
            "Python",
            "Rattler",
            "Panther",
            "Wolf",
            "Weasel",
            "Wild",
            "Ninja",
            "Jedi",
        ]
    }

    property_defaults: Dict[str, Any] = {
        "LAU3ROF": 0,
        "LaserCode100": 6,
        "LaserCode10": 8,
        "LaserCode1": 8,
        "HelmetMountedDevice": 1,
    }

    class Properties:
        class LAU3ROF:
            id = "LAU3ROF"

            class Values:
                Single = 0
                Ripple = 1

        class LaserCode100:
            id = "LaserCode100"

        class LaserCode10:
            id = "LaserCode10"

        class LaserCode1:
            id = "LaserCode1"

        class HelmetMountedDevice:
            id = "HelmetMountedDevice"

            class Values:
                Not_installed = 0
                JHMCS = 1
                NVG = 2

    livery_name = "F-16D_52_NS"  # from type

    class Pylon1:
        AIM_9M_Sidewinder_IR_AAM = (1, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (1, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (1, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            1,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            1,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        CATM_9M = (1, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (1, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

        Python_5_Training = (1, WeaponsF16I.Python_5_Training)

    class Pylon2:
        AIM_9M_Sidewinder_IR_AAM = (2, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (2, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (2, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            2,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            2,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        CATM_9M = (2, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (2, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

        Python_5_Training = (1, WeaponsF16I.Python_5_Training)

    # ERRR <CLEAN>

    class Pylon3:
        AIM_9M_Sidewinder_IR_AAM = (3, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (3, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (3, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            3,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            3,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        CATM_9M = (3, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (3, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        LAU3_WP156 = (3, Weapons.LAU3_WP156)
        LAU3_WP1B = (3, Weapons.LAU3_WP1B)
        LAU3_WP61 = (3, Weapons.LAU3_WP61)
        LAU3_HE5 = (3, Weapons.LAU3_HE5)
        LAU3_HE151 = (3, Weapons.LAU3_HE151)
        BDU_50LD___500lb_Inert_Practice_Bomb_LD = (
            3,
            Weapons.BDU_50LD___500lb_Inert_Practice_Bomb_LD,
        )
        BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD = (
            3,
            Weapons.BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD,
        )
        BDU_50HD___500lb_Inert_Practice_Bomb_HD = (
            3,
            Weapons.BDU_50HD___500lb_Inert_Practice_Bomb_HD,
        )
        Mk_82___500lb_GP_Bomb_LD = (3, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (3, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            3,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (3, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD = (
            3,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD = (
            3,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD,
        )
        GBU_10___2000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (3, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        CBU_87___202_x_CEM_Cluster_Bomb = (3, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (3, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            3,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        BRU_57_with_2_x_CBU_105___10_x_SFW__CBU_with_WCMD = (
            3,
            Weapons.BRU_57_with_2_x_CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            3,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        BRU_57_with_2_x_CBU_103___202_x_CEM__CBU_with_WCMD = (
            3,
            Weapons.BRU_57_with_2_x_CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            3,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            3,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            3,
            Weapons.TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD = (
            3,
            Weapons.TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            3,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_117_AGM_65G = (3, Weapons.LAU_117_AGM_65G)
        LAU_117_AGM_65H = (3, Weapons.LAU_117_AGM_65H)
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            3,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_88_AGM_65D_ONE = (3, Weapons.LAU_88_AGM_65D_ONE)
        LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_ = (
            3,
            Weapons.LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_88_AGM_65H = (3, Weapons.LAU_88_AGM_65H)
        LAU_88_AGM_65H_3 = (3, Weapons.LAU_88_AGM_65H_3)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            3,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            Weapons.GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            3,
            Weapons.GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            Weapons.GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )
        BRU_57_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            Weapons.BRU_57_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        AGM_154A___JSOW_CEB__CBU_type_ = (3, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        MXU_648_TP = (3, Weapons.MXU_648_TP)
        ALQ_184 = (3, Weapons.ALQ_184)
        ALQ_184_Long = (3, Weapons.ALQ_184_Long)
        ALQ_131___ECM_Pod = (3, Weapons.ALQ_131___ECM_Pod)
        # ERRR <CLEAN>
        TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD = (
            3,
            Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            3,
            Weapons.TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            3,
            Weapons.TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_2_x_GBU_12___500lb_Laser_Guided_Bomb = (
            3,
            Weapons.TER_9A_with_2_x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb = (
            3,
            Weapons.TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb,
        )
        TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb = (
            3,
            Weapons.TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb,
        )
        LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM_ = (
            3,
            Weapons.LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_88_AGM_65H_2_L = (3, Weapons.LAU_88_AGM_65H_2_L)
        Pylon_3_4_Mk_82___500lb_GP_Bomb_LD = (
            3,
            WeaponsF16I.Pylon_3_4_Mk_82___500lb_GP_Bomb_LD,
        )
        Pylon_3_4_Mk_84___2000lb_GP_Bomb_LD = (
            3,
            WeaponsF16I.Pylon_3_4_Mk_84___2000lb_GP_Bomb_LD,
        )
        Pylon_3_4_GBU_31 = (3, WeaponsF16I.Pylon_3_4_GBU_31)
        Pylon_3_4_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            WeaponsF16I.Pylon_3_4_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )
        Pylon_3_4_GBU_12___500lb_Laser_Guided_Bomb = (
            3,
            WeaponsF16I.Pylon_3_4_GBU_12___500lb_Laser_Guided_Bomb,
        )
        Pylon_3_4_GBU_10___2000lb_Laser_Guided_Bomb = (
            3,
            WeaponsF16I.Pylon_3_4_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        Pylon_3_4_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            WeaponsF16I.Pylon_3_4_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        Pylon_4_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            WeaponsF16I.Pylon_4_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        Pylon_4_GBU_31 = (3, WeaponsF16I.Pylon_4_GBU_31)
        Pylon_4_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            WeaponsF16I.Pylon_4_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )

    class Pylon4:
        LAU3_WP156 = (4, Weapons.LAU3_WP156)
        LAU3_WP1B = (4, Weapons.LAU3_WP1B)
        LAU3_WP61 = (4, Weapons.LAU3_WP61)
        LAU3_HE5 = (4, Weapons.LAU3_HE5)
        LAU3_HE151 = (4, Weapons.LAU3_HE151)
        BDU_50LD___500lb_Inert_Practice_Bomb_LD = (
            4,
            Weapons.BDU_50LD___500lb_Inert_Practice_Bomb_LD,
        )
        BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD = (
            4,
            Weapons.BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD,
        )
        BDU_50HD___500lb_Inert_Practice_Bomb_HD = (
            4,
            Weapons.BDU_50HD___500lb_Inert_Practice_Bomb_HD,
        )
        Mk_82___500lb_GP_Bomb_LD = (4, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (4, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            4,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (4, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD = (
            4,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD = (
            4,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD,
        )
        GBU_10___2000lb_Laser_Guided_Bomb = (
            4,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (4, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb = (
            4,
            Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        CBU_87___202_x_CEM_Cluster_Bomb = (4, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (4, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            4,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            4,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            4,
            Weapons.TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD = (
            4,
            Weapons.TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb = (
            4,
            Weapons.TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb,
        )
        TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb = (
            4,
            Weapons.TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb,
        )
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            4,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        Fuel_tank_370_gal = (4, Weapons.Fuel_tank_370_gal)
        MXU_648_TP = (4, Weapons.MXU_648_TP)
        Fuel_tank_600_gal = (4, WeaponsF16I.Fuel_tank_600_gal)
        Fuel_tank_600_gal__EMPTY_ = (4, WeaponsF16I.Fuel_tank_600_gal__EMPTY_)
        IDF_Mods_Project_Fuel_Tank_370_EMPTY = (
            4,
            WeaponsF16I.IDF_Mods_Project_Fuel_Tank_370_EMPTY,
        )
        # ERRR <CLEAN>
        TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD = (
            4,
            Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            4,
            Weapons.TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            4,
            Weapons.TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb = (
            4,
            Weapons.TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb,
        )
        TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb = (
            4,
            Weapons.TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb,
        )
        IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb = (
            4,
            WeaponsF16I.IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb,
        )
        IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb__600Gal = (
            4,
            WeaponsF16I.IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb__600Gal,
        )
        IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb__370Gal = (
            4,
            WeaponsF16I.IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb__370Gal,
        )

    class Pylon5:
        Fuel_tank_300_gal = (5, Weapons.Fuel_tank_300_gal)
        Fuel_tank_300_gal_Empty = (5, WeaponsF16I.Fuel_tank_300_gal_Empty)
        MXU_648_TP = (5, Weapons.MXU_648_TP)
        ALQ_184 = (5, Weapons.ALQ_184)
        ALQ_184_Long = (5, Weapons.ALQ_184_Long)
        ALQ_131___ECM_Pod = (5, Weapons.ALQ_131___ECM_Pod)

    # ERRR <CLEAN>

    class Pylon6:
        LAU3_WP156 = (6, Weapons.LAU3_WP156)
        LAU3_WP1B = (6, Weapons.LAU3_WP1B)
        LAU3_WP61 = (6, Weapons.LAU3_WP61)
        LAU3_HE5 = (6, Weapons.LAU3_HE5)
        LAU3_HE151 = (6, Weapons.LAU3_HE151)
        BDU_50LD___500lb_Inert_Practice_Bomb_LD = (
            6,
            Weapons.BDU_50LD___500lb_Inert_Practice_Bomb_LD,
        )
        BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD = (
            6,
            Weapons.BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD,
        )
        BDU_50HD___500lb_Inert_Practice_Bomb_HD = (
            6,
            Weapons.BDU_50HD___500lb_Inert_Practice_Bomb_HD,
        )
        Mk_82___500lb_GP_Bomb_LD = (6, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (6, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            6,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (6, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD = (
            6,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD = (
            6,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD,
        )
        GBU_10___2000lb_Laser_Guided_Bomb = (
            6,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (6, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb = (
            6,
            Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        CBU_87___202_x_CEM_Cluster_Bomb = (6, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (6, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            6,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            6,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            6,
            Weapons.TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD = (
            6,
            Weapons.TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb = (
            6,
            Weapons.TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb,
        )
        TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb = (
            6,
            Weapons.TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb,
        )
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            6,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        Fuel_tank_370_gal = (6, Weapons.Fuel_tank_370_gal)
        MXU_648_TP = (6, Weapons.MXU_648_TP)
        Fuel_tank_600_gal = (6, WeaponsF16I.Fuel_tank_600_gal)
        Fuel_tank_600_gal__EMPTY_ = (6, WeaponsF16I.Fuel_tank_600_gal__EMPTY_)
        IDF_Mods_Project_Fuel_Tank_370_EMPTY = (
            6,
            WeaponsF16I.IDF_Mods_Project_Fuel_Tank_370_EMPTY,
        )
        # ERRR <CLEAN>
        TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD_ = (
            6,
            Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD_,
        )
        TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_ = (
            6,
            Weapons.TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_,
        )
        TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD_ = (
            6,
            Weapons.TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD_,
        )
        TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb_ = (
            6,
            Weapons.TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb_,
        )
        TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb_ = (
            6,
            Weapons.TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb_,
        )
        IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb = (
            6,
            WeaponsF16I.IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb,
        )
        IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb__370Gal = (
            6,
            WeaponsF16I.IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb__370Gal,
        )
        IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb__600Gal = (
            6,
            WeaponsF16I.IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb__600Gal,
        )

    class Pylon7:
        AIM_9M_Sidewinder_IR_AAM = (7, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (7, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (7, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            7,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            7,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        CATM_9M = (7, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (7, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        LAU3_WP156 = (7, Weapons.LAU3_WP156)
        LAU3_WP1B = (7, Weapons.LAU3_WP1B)
        LAU3_WP61 = (7, Weapons.LAU3_WP61)
        LAU3_HE5 = (7, Weapons.LAU3_HE5)
        LAU3_HE151 = (7, Weapons.LAU3_HE151)
        BDU_50LD___500lb_Inert_Practice_Bomb_LD = (
            7,
            Weapons.BDU_50LD___500lb_Inert_Practice_Bomb_LD,
        )
        BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD = (
            7,
            Weapons.BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD,
        )
        BDU_50HD___500lb_Inert_Practice_Bomb_HD = (
            7,
            Weapons.BDU_50HD___500lb_Inert_Practice_Bomb_HD,
        )
        Mk_82___500lb_GP_Bomb_LD = (7, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (7, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            7,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (7, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD = (
            7,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD = (
            7,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD,
        )
        GBU_10___2000lb_Laser_Guided_Bomb = (
            7,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (7, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb = (
            7,
            Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        CBU_87___202_x_CEM_Cluster_Bomb = (7, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (7, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            7,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        BRU_57_with_2_x_CBU_105___10_x_SFW__CBU_with_WCMD = (
            7,
            Weapons.BRU_57_with_2_x_CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            7,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        BRU_57_with_2_x_CBU_103___202_x_CEM__CBU_with_WCMD = (
            7,
            Weapons.BRU_57_with_2_x_CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            7,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            7,
            Weapons.TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD = (
            7,
            Weapons.TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            7,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_117_AGM_65G = (7, Weapons.LAU_117_AGM_65G)
        LAU_117_AGM_65H = (7, Weapons.LAU_117_AGM_65H)
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            7,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_88_AGM_65D_ONE = (7, Weapons.LAU_88_AGM_65D_ONE)
        LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_ = (
            7,
            Weapons.LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_88_AGM_65H = (7, Weapons.LAU_88_AGM_65H)
        LAU_88_AGM_65H_3 = (7, Weapons.LAU_88_AGM_65H_3)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            7,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            Weapons.GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            7,
            Weapons.GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            Weapons.GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )
        BRU_57_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            Weapons.BRU_57_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        AGM_154A___JSOW_CEB__CBU_type_ = (7, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        MXU_648_TP = (7, Weapons.MXU_648_TP)
        ALQ_184 = (7, Weapons.ALQ_184)
        ALQ_184_Long = (7, Weapons.ALQ_184_Long)
        ALQ_131___ECM_Pod = (7, Weapons.ALQ_131___ECM_Pod)
        # ERRR <CLEAN>
        TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD_ = (
            7,
            Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD_,
        )
        TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_ = (
            7,
            Weapons.TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_,
        )
        TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD_ = (
            7,
            Weapons.TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD_,
        )
        TER_9A_with_2_x_GBU_12___500lb_Laser_Guided_Bomb_ = (
            7,
            Weapons.TER_9A_with_2_x_GBU_12___500lb_Laser_Guided_Bomb_,
        )
        TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb_ = (
            7,
            Weapons.TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb_,
        )
        TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb_ = (
            7,
            Weapons.TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb_,
        )
        LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM__ = (
            7,
            Weapons.LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM__,
        )
        LAU_88_AGM_65H_2_R = (7, Weapons.LAU_88_AGM_65H_2_R)
        Pylon_6_7_Mk_82___500lb_GP_Bomb_LD = (
            7,
            WeaponsF16I.Pylon_6_7_Mk_82___500lb_GP_Bomb_LD,
        )
        Pylon_6_7_Mk_84___2000lb_GP_Bomb_LD = (
            7,
            WeaponsF16I.Pylon_6_7_Mk_84___2000lb_GP_Bomb_LD,
        )
        Pylon_6_7_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsF16I.Pylon_6_7_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )
        Pylon_6_7_GBU_31 = (7, WeaponsF16I.Pylon_6_7_GBU_31)
        Pylon_6_7_GBU_12___500lb_Laser_Guided_Bomb = (
            7,
            WeaponsF16I.Pylon_6_7_GBU_12___500lb_Laser_Guided_Bomb,
        )
        Pylon_6_7_GBU_10___2000lb_Laser_Guided_Bomb = (
            7,
            WeaponsF16I.Pylon_6_7_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        Pylon_6_7_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            WeaponsF16I.Pylon_6_7_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        Pylon_6_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            WeaponsF16I.Pylon_6_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        Pylon_6_GBU_31 = (7, WeaponsF16I.Pylon_6_GBU_31)
        Pylon_6_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsF16I.Pylon_6_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )

    class Pylon8:
        AIM_9M_Sidewinder_IR_AAM = (8, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (8, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (8, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            8,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            8,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        CATM_9M = (8, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (8, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

        Python_5_Training = (1, WeaponsF16I.Python_5_Training)

    # ERRR <CLEAN>

    class Pylon9:
        AIM_9M_Sidewinder_IR_AAM = (9, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (9, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (9, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            9,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            9,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        CATM_9M = (9, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (9, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

        Python_5_Training = (1, WeaponsF16I.Python_5_Training)

    class Pylon10:
        AN_ASQ_213_HTS___HARM_Targeting_System = (
            10,
            Weapons.AN_ASQ_213_HTS___HARM_Targeting_System,
        )

    class Pylon11:
        AN_AAQ_28_LITENING___Targeting_Pod = (
            11,
            Weapons.AN_AAQ_28_LITENING___Targeting_Pod,
        )

    class Pylon12:
        Smoke_Generator___red_ = (12, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (12, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (12, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (12, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (12, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (12, Weapons.Smoke_Generator___orange_)

    class Pylon13:
        ALQ_184 = (13, Weapons.ALQ_184)

    class Pylon14:
        Crew_Ladder_No_CFT = (14, WeaponsF16I.Crew_Ladder_No_CFT)

    class Pylon15:
        Remove_Before_Flight = (15, WeaponsF16I.Remove_Before_Flight)
        Remove_Before_Flight_without_Lantirn = (
            15,
            WeaponsF16I.Remove_Before_Flight_without_Lantirn,
        )
        Remove_Before_Flight_without_TGP_ = (
            15,
            WeaponsF16I.Remove_Before_Flight_without_TGP_,
        )
        Remove_Before_Flight_without_TGP_And_Lantirn = (
            15,
            WeaponsF16I.Remove_Before_Flight_without_TGP_And_Lantirn,
        )

    class Pylon16:
        IDF_Mods_Project_F_16I_CFT = (16, WeaponsF16I.IDF_Mods_Project_F_16I_CFT)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.PinpointStrike,
        task.CAS,
        task.GroundAttack,
        task.RunwayAttack,
        task.SEAD,
        task.AFAC,
        task.AntishipStrike,
        task.Reconnaissance,
    ]
    task_default = task.CAP


@planemod
class F_16D_50_NS(PlaneType):
    id = "F-16D_50_NS"
    flyable = True
    height = 5.02
    width = 9.45
    length = 14.52
    fuel_max = 2585.48
    max_speed = 2120.04
    chaff = 60
    flare = 60
    charge_total = 120
    chaff_charge_size = 1
    flare_charge_size = 1
    eplrs = True
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 305

    panel_radio = {
        1: {
            "channels": {
                1: 305,
                2: 264,
                4: 256,
                8: 257,
                16: 261,
                17: 267,
                9: 255,
                18: 251,
                5: 254,
                10: 262,
                20: 266,
                11: 259,
                3: 265,
                6: 250,
                12: 268,
                13: 269,
                7: 270,
                14: 260,
                19: 253,
                15: 263,
            },
        },
        2: {
            "channels": {
                1: 127,
                2: 135,
                4: 127,
                8: 128,
                16: 132,
                17: 138,
                9: 126,
                18: 122,
                5: 125,
                10: 133,
                20: 137,
                11: 130,
                3: 136,
                6: 121,
                12: 139,
                13: 140,
                7: 141,
                14: 131,
                19: 124,
                15: 134,
            },
        },
    }

    callnames: Dict[str, List[str]] = {
        "USA": [
            "Viper",
            "Venom",
            "Lobo",
            "Cowboy",
            "Python",
            "Rattler",
            "Panther",
            "Wolf",
            "Weasel",
            "Wild",
            "Ninja",
            "Jedi",
        ]
    }

    property_defaults: Dict[str, Any] = {
        "LAU3ROF": 0,
        "LaserCode100": 6,
        "LaserCode10": 8,
        "LaserCode1": 8,
        "HelmetMountedDevice": 1,
    }

    class Properties:
        class LAU3ROF:
            id = "LAU3ROF"

            class Values:
                Single = 0
                Ripple = 1

        class LaserCode100:
            id = "LaserCode100"

        class LaserCode10:
            id = "LaserCode10"

        class LaserCode1:
            id = "LaserCode1"

        class HelmetMountedDevice:
            id = "HelmetMountedDevice"

            class Values:
                Not_installed = 0
                JHMCS = 1
                NVG = 2

    livery_name = "F-16D_50_NS"  # from type

    class Pylon1:
        AIM_9M_Sidewinder_IR_AAM = (1, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (1, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (1, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            1,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            1,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        CATM_9M = (1, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (1, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

        Python_5_Training = (1, WeaponsF16I.Python_5_Training)

    class Pylon2:
        AIM_9M_Sidewinder_IR_AAM = (2, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (2, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (2, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            2,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            2,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        CATM_9M = (2, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (2, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

        Python_5_Training = (1, WeaponsF16I.Python_5_Training)

    # ERRR <CLEAN>

    class Pylon3:
        AIM_9M_Sidewinder_IR_AAM = (3, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (3, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (3, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            3,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            3,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        CATM_9M = (3, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (3, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        LAU3_WP156 = (3, Weapons.LAU3_WP156)
        LAU3_WP1B = (3, Weapons.LAU3_WP1B)
        LAU3_WP61 = (3, Weapons.LAU3_WP61)
        LAU3_HE5 = (3, Weapons.LAU3_HE5)
        LAU3_HE151 = (3, Weapons.LAU3_HE151)
        BDU_50LD___500lb_Inert_Practice_Bomb_LD = (
            3,
            Weapons.BDU_50LD___500lb_Inert_Practice_Bomb_LD,
        )
        BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD = (
            3,
            Weapons.BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD,
        )
        BDU_50HD___500lb_Inert_Practice_Bomb_HD = (
            3,
            Weapons.BDU_50HD___500lb_Inert_Practice_Bomb_HD,
        )
        Mk_82___500lb_GP_Bomb_LD = (3, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (3, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            3,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (3, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD = (
            3,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD = (
            3,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD,
        )
        GBU_10___2000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (3, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        CBU_87___202_x_CEM_Cluster_Bomb = (3, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (3, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            3,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        BRU_57_with_2_x_CBU_105___10_x_SFW__CBU_with_WCMD = (
            3,
            Weapons.BRU_57_with_2_x_CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            3,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        BRU_57_with_2_x_CBU_103___202_x_CEM__CBU_with_WCMD = (
            3,
            Weapons.BRU_57_with_2_x_CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            3,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            3,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            3,
            Weapons.TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD = (
            3,
            Weapons.TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            3,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_117_AGM_65G = (3, Weapons.LAU_117_AGM_65G)
        LAU_117_AGM_65H = (3, Weapons.LAU_117_AGM_65H)
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            3,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_88_AGM_65D_ONE = (3, Weapons.LAU_88_AGM_65D_ONE)
        LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_ = (
            3,
            Weapons.LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_88_AGM_65H = (3, Weapons.LAU_88_AGM_65H)
        LAU_88_AGM_65H_3 = (3, Weapons.LAU_88_AGM_65H_3)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            3,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            Weapons.GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            3,
            Weapons.GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            Weapons.GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )
        BRU_57_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            Weapons.BRU_57_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        AGM_154A___JSOW_CEB__CBU_type_ = (3, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        MXU_648_TP = (3, Weapons.MXU_648_TP)
        ALQ_184 = (3, Weapons.ALQ_184)
        ALQ_184_Long = (3, Weapons.ALQ_184_Long)
        ALQ_131___ECM_Pod = (3, Weapons.ALQ_131___ECM_Pod)
        # ERRR <CLEAN>
        TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD = (
            3,
            Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            3,
            Weapons.TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            3,
            Weapons.TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_2_x_GBU_12___500lb_Laser_Guided_Bomb = (
            3,
            Weapons.TER_9A_with_2_x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb = (
            3,
            Weapons.TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb,
        )
        TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb = (
            3,
            Weapons.TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb,
        )
        LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM_ = (
            3,
            Weapons.LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_88_AGM_65H_2_L = (3, Weapons.LAU_88_AGM_65H_2_L)
        Pylon_3_4_Mk_82___500lb_GP_Bomb_LD = (
            3,
            WeaponsF16I.Pylon_3_4_Mk_82___500lb_GP_Bomb_LD,
        )
        Pylon_3_4_Mk_84___2000lb_GP_Bomb_LD = (
            3,
            WeaponsF16I.Pylon_3_4_Mk_84___2000lb_GP_Bomb_LD,
        )
        Pylon_3_4_GBU_31 = (3, WeaponsF16I.Pylon_3_4_GBU_31)
        Pylon_3_4_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            WeaponsF16I.Pylon_3_4_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )
        Pylon_3_4_GBU_12___500lb_Laser_Guided_Bomb = (
            3,
            WeaponsF16I.Pylon_3_4_GBU_12___500lb_Laser_Guided_Bomb,
        )
        Pylon_3_4_GBU_10___2000lb_Laser_Guided_Bomb = (
            3,
            WeaponsF16I.Pylon_3_4_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        Pylon_3_4_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            WeaponsF16I.Pylon_3_4_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        Pylon_4_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            WeaponsF16I.Pylon_4_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        Pylon_4_GBU_31 = (3, WeaponsF16I.Pylon_4_GBU_31)
        Pylon_4_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            WeaponsF16I.Pylon_4_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )

    class Pylon4:
        LAU3_WP156 = (4, Weapons.LAU3_WP156)
        LAU3_WP1B = (4, Weapons.LAU3_WP1B)
        LAU3_WP61 = (4, Weapons.LAU3_WP61)
        LAU3_HE5 = (4, Weapons.LAU3_HE5)
        LAU3_HE151 = (4, Weapons.LAU3_HE151)
        BDU_50LD___500lb_Inert_Practice_Bomb_LD = (
            4,
            Weapons.BDU_50LD___500lb_Inert_Practice_Bomb_LD,
        )
        BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD = (
            4,
            Weapons.BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD,
        )
        BDU_50HD___500lb_Inert_Practice_Bomb_HD = (
            4,
            Weapons.BDU_50HD___500lb_Inert_Practice_Bomb_HD,
        )
        Mk_82___500lb_GP_Bomb_LD = (4, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (4, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            4,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (4, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD = (
            4,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD = (
            4,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD,
        )
        GBU_10___2000lb_Laser_Guided_Bomb = (
            4,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (4, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb = (
            4,
            Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        CBU_87___202_x_CEM_Cluster_Bomb = (4, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (4, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            4,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            4,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            4,
            Weapons.TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD = (
            4,
            Weapons.TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb = (
            4,
            Weapons.TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb,
        )
        TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb = (
            4,
            Weapons.TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb,
        )
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            4,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        Fuel_tank_370_gal = (4, Weapons.Fuel_tank_370_gal)
        MXU_648_TP = (4, Weapons.MXU_648_TP)
        Fuel_tank_600_gal = (4, WeaponsF16I.Fuel_tank_600_gal)
        Fuel_tank_600_gal__EMPTY_ = (4, WeaponsF16I.Fuel_tank_600_gal__EMPTY_)
        IDF_Mods_Project_Fuel_Tank_370_EMPTY = (
            4,
            WeaponsF16I.IDF_Mods_Project_Fuel_Tank_370_EMPTY,
        )
        # ERRR <CLEAN>
        TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD = (
            4,
            Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            4,
            Weapons.TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            4,
            Weapons.TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb = (
            4,
            Weapons.TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb,
        )
        TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb = (
            4,
            Weapons.TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb,
        )
        IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb = (
            4,
            WeaponsF16I.IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb,
        )
        IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb__600Gal = (
            4,
            WeaponsF16I.IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb__600Gal,
        )
        IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb__370Gal = (
            4,
            WeaponsF16I.IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb__370Gal,
        )

    class Pylon5:
        Fuel_tank_300_gal = (5, Weapons.Fuel_tank_300_gal)
        Fuel_tank_300_gal_Empty = (5, WeaponsF16I.Fuel_tank_300_gal_Empty)
        MXU_648_TP = (5, Weapons.MXU_648_TP)
        ALQ_184 = (5, Weapons.ALQ_184)
        ALQ_184_Long = (5, Weapons.ALQ_184_Long)
        ALQ_131___ECM_Pod = (5, Weapons.ALQ_131___ECM_Pod)

    # ERRR <CLEAN>

    class Pylon6:
        LAU3_WP156 = (6, Weapons.LAU3_WP156)
        LAU3_WP1B = (6, Weapons.LAU3_WP1B)
        LAU3_WP61 = (6, Weapons.LAU3_WP61)
        LAU3_HE5 = (6, Weapons.LAU3_HE5)
        LAU3_HE151 = (6, Weapons.LAU3_HE151)
        BDU_50LD___500lb_Inert_Practice_Bomb_LD = (
            6,
            Weapons.BDU_50LD___500lb_Inert_Practice_Bomb_LD,
        )
        BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD = (
            6,
            Weapons.BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD,
        )
        BDU_50HD___500lb_Inert_Practice_Bomb_HD = (
            6,
            Weapons.BDU_50HD___500lb_Inert_Practice_Bomb_HD,
        )
        Mk_82___500lb_GP_Bomb_LD = (6, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (6, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            6,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (6, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD = (
            6,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD = (
            6,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD,
        )
        GBU_10___2000lb_Laser_Guided_Bomb = (
            6,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (6, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb = (
            6,
            Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        CBU_87___202_x_CEM_Cluster_Bomb = (6, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (6, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            6,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            6,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            6,
            Weapons.TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD = (
            6,
            Weapons.TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb = (
            6,
            Weapons.TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb,
        )
        TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb = (
            6,
            Weapons.TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb,
        )
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            6,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        Fuel_tank_370_gal = (6, Weapons.Fuel_tank_370_gal)
        MXU_648_TP = (6, Weapons.MXU_648_TP)
        Fuel_tank_600_gal = (6, WeaponsF16I.Fuel_tank_600_gal)
        Fuel_tank_600_gal__EMPTY_ = (6, WeaponsF16I.Fuel_tank_600_gal__EMPTY_)
        IDF_Mods_Project_Fuel_Tank_370_EMPTY = (
            6,
            WeaponsF16I.IDF_Mods_Project_Fuel_Tank_370_EMPTY,
        )
        # ERRR <CLEAN>
        TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD_ = (
            6,
            Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD_,
        )
        TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_ = (
            6,
            Weapons.TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_,
        )
        TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD_ = (
            6,
            Weapons.TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD_,
        )
        TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb_ = (
            6,
            Weapons.TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb_,
        )
        TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb_ = (
            6,
            Weapons.TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb_,
        )
        IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb = (
            6,
            WeaponsF16I.IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb,
        )
        IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb__370Gal = (
            6,
            WeaponsF16I.IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb__370Gal,
        )
        IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb__600Gal = (
            6,
            WeaponsF16I.IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb__600Gal,
        )

    class Pylon7:
        AIM_9M_Sidewinder_IR_AAM = (7, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (7, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (7, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            7,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            7,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        CATM_9M = (7, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (7, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        LAU3_WP156 = (7, Weapons.LAU3_WP156)
        LAU3_WP1B = (7, Weapons.LAU3_WP1B)
        LAU3_WP61 = (7, Weapons.LAU3_WP61)
        LAU3_HE5 = (7, Weapons.LAU3_HE5)
        LAU3_HE151 = (7, Weapons.LAU3_HE151)
        BDU_50LD___500lb_Inert_Practice_Bomb_LD = (
            7,
            Weapons.BDU_50LD___500lb_Inert_Practice_Bomb_LD,
        )
        BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD = (
            7,
            Weapons.BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD,
        )
        BDU_50HD___500lb_Inert_Practice_Bomb_HD = (
            7,
            Weapons.BDU_50HD___500lb_Inert_Practice_Bomb_HD,
        )
        Mk_82___500lb_GP_Bomb_LD = (7, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (7, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            7,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (7, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD = (
            7,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD = (
            7,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD,
        )
        GBU_10___2000lb_Laser_Guided_Bomb = (
            7,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (7, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb = (
            7,
            Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        CBU_87___202_x_CEM_Cluster_Bomb = (7, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (7, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            7,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        BRU_57_with_2_x_CBU_105___10_x_SFW__CBU_with_WCMD = (
            7,
            Weapons.BRU_57_with_2_x_CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            7,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        BRU_57_with_2_x_CBU_103___202_x_CEM__CBU_with_WCMD = (
            7,
            Weapons.BRU_57_with_2_x_CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            7,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            7,
            Weapons.TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD = (
            7,
            Weapons.TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            7,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_117_AGM_65G = (7, Weapons.LAU_117_AGM_65G)
        LAU_117_AGM_65H = (7, Weapons.LAU_117_AGM_65H)
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            7,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_88_AGM_65D_ONE = (7, Weapons.LAU_88_AGM_65D_ONE)
        LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_ = (
            7,
            Weapons.LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_88_AGM_65H = (7, Weapons.LAU_88_AGM_65H)
        LAU_88_AGM_65H_3 = (7, Weapons.LAU_88_AGM_65H_3)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            7,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            Weapons.GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            7,
            Weapons.GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            Weapons.GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )
        BRU_57_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            Weapons.BRU_57_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        AGM_154A___JSOW_CEB__CBU_type_ = (7, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        MXU_648_TP = (7, Weapons.MXU_648_TP)
        ALQ_184 = (7, Weapons.ALQ_184)
        ALQ_184_Long = (7, Weapons.ALQ_184_Long)
        ALQ_131___ECM_Pod = (7, Weapons.ALQ_131___ECM_Pod)
        # ERRR <CLEAN>
        TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD_ = (
            7,
            Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD_,
        )
        TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_ = (
            7,
            Weapons.TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_,
        )
        TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD_ = (
            7,
            Weapons.TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD_,
        )
        TER_9A_with_2_x_GBU_12___500lb_Laser_Guided_Bomb_ = (
            7,
            Weapons.TER_9A_with_2_x_GBU_12___500lb_Laser_Guided_Bomb_,
        )
        TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb_ = (
            7,
            Weapons.TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb_,
        )
        TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb_ = (
            7,
            Weapons.TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb_,
        )
        LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM__ = (
            7,
            Weapons.LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM__,
        )
        LAU_88_AGM_65H_2_R = (7, Weapons.LAU_88_AGM_65H_2_R)
        Pylon_6_7_Mk_82___500lb_GP_Bomb_LD = (
            7,
            WeaponsF16I.Pylon_6_7_Mk_82___500lb_GP_Bomb_LD,
        )
        Pylon_6_7_Mk_84___2000lb_GP_Bomb_LD = (
            7,
            WeaponsF16I.Pylon_6_7_Mk_84___2000lb_GP_Bomb_LD,
        )
        Pylon_6_7_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsF16I.Pylon_6_7_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )
        Pylon_6_7_GBU_31 = (7, WeaponsF16I.Pylon_6_7_GBU_31)
        Pylon_6_7_GBU_12___500lb_Laser_Guided_Bomb = (
            7,
            WeaponsF16I.Pylon_6_7_GBU_12___500lb_Laser_Guided_Bomb,
        )
        Pylon_6_7_GBU_10___2000lb_Laser_Guided_Bomb = (
            7,
            WeaponsF16I.Pylon_6_7_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        Pylon_6_7_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            WeaponsF16I.Pylon_6_7_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        Pylon_6_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            WeaponsF16I.Pylon_6_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        Pylon_6_GBU_31 = (7, WeaponsF16I.Pylon_6_GBU_31)
        Pylon_6_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsF16I.Pylon_6_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )

    class Pylon8:
        AIM_9M_Sidewinder_IR_AAM = (8, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (8, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (8, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            8,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            8,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        CATM_9M = (8, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (8, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

        Python_5_Training = (1, WeaponsF16I.Python_5_Training)

    # ERRR <CLEAN>

    class Pylon9:
        AIM_9M_Sidewinder_IR_AAM = (9, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (9, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (9, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            9,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            9,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        CATM_9M = (9, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (9, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

        Python_5_Training = (1, WeaponsF16I.Python_5_Training)

    class Pylon10:
        AN_ASQ_213_HTS___HARM_Targeting_System = (
            10,
            Weapons.AN_ASQ_213_HTS___HARM_Targeting_System,
        )

    class Pylon11:
        AN_AAQ_28_LITENING___Targeting_Pod = (
            11,
            Weapons.AN_AAQ_28_LITENING___Targeting_Pod,
        )

    class Pylon12:
        Smoke_Generator___red_ = (12, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (12, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (12, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (12, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (12, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (12, Weapons.Smoke_Generator___orange_)

    class Pylon13:
        ALQ_184 = (13, Weapons.ALQ_184)

    class Pylon14:
        Crew_Ladder_No_CFT = (14, WeaponsF16I.Crew_Ladder_No_CFT)

    class Pylon15:
        Remove_Before_Flight = (15, WeaponsF16I.Remove_Before_Flight)
        Remove_Before_Flight_without_Lantirn = (
            15,
            WeaponsF16I.Remove_Before_Flight_without_Lantirn,
        )
        Remove_Before_Flight_without_TGP_ = (
            15,
            WeaponsF16I.Remove_Before_Flight_without_TGP_,
        )
        Remove_Before_Flight_without_TGP_And_Lantirn = (
            15,
            WeaponsF16I.Remove_Before_Flight_without_TGP_And_Lantirn,
        )

    class Pylon16:
        IDF_Mods_Project_F_16I_CFT = (16, WeaponsF16I.IDF_Mods_Project_F_16I_CFT)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.PinpointStrike,
        task.CAS,
        task.GroundAttack,
        task.RunwayAttack,
        task.SEAD,
        task.AFAC,
        task.AntishipStrike,
        task.Reconnaissance,
    ]
    task_default = task.CAP


@planemod
class F_16D_Barak_40(PlaneType):
    id = "F-16D_Barak_40"
    flyable = True
    height = 5.02
    width = 9.45
    length = 14.52
    fuel_max = 2585.48
    max_speed = 2120.04
    chaff = 60
    flare = 60
    charge_total = 120
    chaff_charge_size = 1
    flare_charge_size = 1
    eplrs = True
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 305

    panel_radio = {
        1: {
            "channels": {
                1: 305,
                2: 264,
                4: 256,
                8: 257,
                16: 261,
                17: 267,
                9: 255,
                18: 251,
                5: 254,
                10: 262,
                20: 266,
                11: 259,
                3: 265,
                6: 250,
                12: 268,
                13: 269,
                7: 270,
                14: 260,
                19: 253,
                15: 263,
            },
        },
        2: {
            "channels": {
                1: 127,
                2: 135,
                4: 127,
                8: 128,
                16: 132,
                17: 138,
                9: 126,
                18: 122,
                5: 125,
                10: 133,
                20: 137,
                11: 130,
                3: 136,
                6: 121,
                12: 139,
                13: 140,
                7: 141,
                14: 131,
                19: 124,
                15: 134,
            },
        },
    }

    callnames: Dict[str, List[str]] = {
        "USA": [
            "Viper",
            "Venom",
            "Lobo",
            "Cowboy",
            "Python",
            "Rattler",
            "Panther",
            "Wolf",
            "Weasel",
            "Wild",
            "Ninja",
            "Jedi",
        ]
    }

    property_defaults: Dict[str, Any] = {
        "LAU3ROF": 0,
        "LaserCode100": 6,
        "LaserCode10": 8,
        "LaserCode1": 8,
        "HelmetMountedDevice": 1,
    }

    class Properties:
        class LAU3ROF:
            id = "LAU3ROF"

            class Values:
                Single = 0
                Ripple = 1

        class LaserCode100:
            id = "LaserCode100"

        class LaserCode10:
            id = "LaserCode10"

        class LaserCode1:
            id = "LaserCode1"

        class HelmetMountedDevice:
            id = "HelmetMountedDevice"

            class Values:
                Not_installed = 0
                JHMCS = 1
                NVG = 2

    livery_name = "F-16D_BARAK_40"  # from type

    class Pylon1:
        AIM_9M_Sidewinder_IR_AAM = (1, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (1, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (1, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            1,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            1,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        CATM_9M = (1, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (1, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

        Python_5_Training = (1, WeaponsF16I.Python_5_Training)

    class Pylon2:
        AIM_9M_Sidewinder_IR_AAM = (2, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (2, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (2, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            2,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            2,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        CATM_9M = (2, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (2, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

        Python_5_Training = (1, WeaponsF16I.Python_5_Training)

    # ERRR <CLEAN>

    class Pylon3:
        AIM_9M_Sidewinder_IR_AAM = (3, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (3, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (3, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            3,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            3,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        CATM_9M = (3, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (3, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        Python_5_Training = (1, WeaponsF16I.Python_5_Training)
        LAU3_WP156 = (3, Weapons.LAU3_WP156)
        LAU3_WP1B = (3, Weapons.LAU3_WP1B)
        LAU3_WP61 = (3, Weapons.LAU3_WP61)
        LAU3_HE5 = (3, Weapons.LAU3_HE5)
        LAU3_HE151 = (3, Weapons.LAU3_HE151)
        BDU_50LD___500lb_Inert_Practice_Bomb_LD = (
            3,
            Weapons.BDU_50LD___500lb_Inert_Practice_Bomb_LD,
        )
        BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD = (
            3,
            Weapons.BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD,
        )
        BDU_50HD___500lb_Inert_Practice_Bomb_HD = (
            3,
            Weapons.BDU_50HD___500lb_Inert_Practice_Bomb_HD,
        )
        Mk_82___500lb_GP_Bomb_LD = (3, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (3, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            3,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (3, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD = (
            3,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD = (
            3,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD,
        )
        GBU_10___2000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (3, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        CBU_87___202_x_CEM_Cluster_Bomb = (3, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (3, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            3,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        BRU_57_with_2_x_CBU_105___10_x_SFW__CBU_with_WCMD = (
            3,
            Weapons.BRU_57_with_2_x_CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            3,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        BRU_57_with_2_x_CBU_103___202_x_CEM__CBU_with_WCMD = (
            3,
            Weapons.BRU_57_with_2_x_CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            3,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            3,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            3,
            Weapons.TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD = (
            3,
            Weapons.TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            3,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_117_AGM_65G = (3, Weapons.LAU_117_AGM_65G)
        LAU_117_AGM_65H = (3, Weapons.LAU_117_AGM_65H)
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            3,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_88_AGM_65D_ONE = (3, Weapons.LAU_88_AGM_65D_ONE)
        LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_ = (
            3,
            Weapons.LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_88_AGM_65H = (3, Weapons.LAU_88_AGM_65H)
        LAU_88_AGM_65H_3 = (3, Weapons.LAU_88_AGM_65H_3)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            3,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            Weapons.GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            3,
            Weapons.GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            Weapons.GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )
        BRU_57_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            Weapons.BRU_57_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        AGM_154A___JSOW_CEB__CBU_type_ = (3, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        MXU_648_TP = (3, Weapons.MXU_648_TP)
        ALQ_184 = (3, Weapons.ALQ_184)
        ALQ_184_Long = (3, Weapons.ALQ_184_Long)
        ALQ_131___ECM_Pod = (3, Weapons.ALQ_131___ECM_Pod)
        # ERRR <CLEAN>
        TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD = (
            3,
            Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            3,
            Weapons.TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            3,
            Weapons.TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_2_x_GBU_12___500lb_Laser_Guided_Bomb = (
            3,
            Weapons.TER_9A_with_2_x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb = (
            3,
            Weapons.TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb,
        )
        TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb = (
            3,
            Weapons.TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb,
        )
        LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM_ = (
            3,
            Weapons.LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_88_AGM_65H_2_L = (3, Weapons.LAU_88_AGM_65H_2_L)
        Pylon_3_4_Mk_82___500lb_GP_Bomb_LD = (
            3,
            WeaponsF16I.Pylon_3_4_Mk_82___500lb_GP_Bomb_LD,
        )
        Pylon_3_4_Mk_84___2000lb_GP_Bomb_LD = (
            3,
            WeaponsF16I.Pylon_3_4_Mk_84___2000lb_GP_Bomb_LD,
        )
        Pylon_3_4_GBU_31 = (3, WeaponsF16I.Pylon_3_4_GBU_31)
        Pylon_3_4_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            WeaponsF16I.Pylon_3_4_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )
        Pylon_3_4_GBU_12___500lb_Laser_Guided_Bomb = (
            3,
            WeaponsF16I.Pylon_3_4_GBU_12___500lb_Laser_Guided_Bomb,
        )
        Pylon_3_4_GBU_10___2000lb_Laser_Guided_Bomb = (
            3,
            WeaponsF16I.Pylon_3_4_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        Pylon_3_4_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            WeaponsF16I.Pylon_3_4_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        Pylon_4_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            WeaponsF16I.Pylon_4_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        Pylon_4_GBU_31 = (3, WeaponsF16I.Pylon_4_GBU_31)
        Pylon_4_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            WeaponsF16I.Pylon_4_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )

    class Pylon4:
        LAU3_WP156 = (4, Weapons.LAU3_WP156)
        LAU3_WP1B = (4, Weapons.LAU3_WP1B)
        LAU3_WP61 = (4, Weapons.LAU3_WP61)
        LAU3_HE5 = (4, Weapons.LAU3_HE5)
        LAU3_HE151 = (4, Weapons.LAU3_HE151)
        BDU_50LD___500lb_Inert_Practice_Bomb_LD = (
            4,
            Weapons.BDU_50LD___500lb_Inert_Practice_Bomb_LD,
        )
        BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD = (
            4,
            Weapons.BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD,
        )
        BDU_50HD___500lb_Inert_Practice_Bomb_HD = (
            4,
            Weapons.BDU_50HD___500lb_Inert_Practice_Bomb_HD,
        )
        Mk_82___500lb_GP_Bomb_LD = (4, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (4, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            4,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (4, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD = (
            4,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD = (
            4,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD,
        )
        GBU_10___2000lb_Laser_Guided_Bomb = (
            4,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (4, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb = (
            4,
            Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        CBU_87___202_x_CEM_Cluster_Bomb = (4, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (4, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            4,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            4,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            4,
            Weapons.TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD = (
            4,
            Weapons.TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb = (
            4,
            Weapons.TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb,
        )
        TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb = (
            4,
            Weapons.TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb,
        )
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            4,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        Fuel_tank_370_gal = (4, Weapons.Fuel_tank_370_gal)
        MXU_648_TP = (4, Weapons.MXU_648_TP)
        # ERRR <CLEAN>
        Fuel_tank_600_gal = (4, WeaponsF16I.Fuel_tank_600_gal)
        Fuel_tank_600_gal__EMPTY_ = (4, WeaponsF16I.Fuel_tank_600_gal__EMPTY_)
        IDF_Mods_Project_Fuel_Tank_370_EMPTY = (
            4,
            WeaponsF16I.IDF_Mods_Project_Fuel_Tank_370_EMPTY,
        )
        TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD = (
            4,
            Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            4,
            Weapons.TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            4,
            Weapons.TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb = (
            4,
            Weapons.TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb,
        )
        TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb = (
            4,
            Weapons.TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb,
        )

    class Pylon5:
        Fuel_tank_300_gal = (5, Weapons.Fuel_tank_300_gal)
        Fuel_tank_300_gal_Empty = (5, WeaponsF16I.Fuel_tank_300_gal_Empty)
        MXU_648_TP = (5, Weapons.MXU_648_TP)
        ALQ_184 = (5, Weapons.ALQ_184)
        ALQ_184_Long = (5, Weapons.ALQ_184_Long)
        ALQ_131___ECM_Pod = (5, Weapons.ALQ_131___ECM_Pod)

    # ERRR <CLEAN>

    class Pylon6:
        LAU3_WP156 = (6, Weapons.LAU3_WP156)
        LAU3_WP1B = (6, Weapons.LAU3_WP1B)
        LAU3_WP61 = (6, Weapons.LAU3_WP61)
        LAU3_HE5 = (6, Weapons.LAU3_HE5)
        LAU3_HE151 = (6, Weapons.LAU3_HE151)
        BDU_50LD___500lb_Inert_Practice_Bomb_LD = (
            6,
            Weapons.BDU_50LD___500lb_Inert_Practice_Bomb_LD,
        )
        BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD = (
            6,
            Weapons.BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD,
        )
        BDU_50HD___500lb_Inert_Practice_Bomb_HD = (
            6,
            Weapons.BDU_50HD___500lb_Inert_Practice_Bomb_HD,
        )
        Mk_82___500lb_GP_Bomb_LD = (6, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (6, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            6,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (6, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD = (
            6,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD = (
            6,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD,
        )
        GBU_10___2000lb_Laser_Guided_Bomb = (
            6,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (6, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb = (
            6,
            Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        CBU_87___202_x_CEM_Cluster_Bomb = (6, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (6, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            6,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            6,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            6,
            Weapons.TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD = (
            6,
            Weapons.TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb = (
            6,
            Weapons.TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb,
        )
        TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb = (
            6,
            Weapons.TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb,
        )
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            6,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        Fuel_tank_370_gal = (6, Weapons.Fuel_tank_370_gal)
        MXU_648_TP = (6, Weapons.MXU_648_TP)
        # ERRR <CLEAN>
        Fuel_tank_600_gal = (6, WeaponsF16I.Fuel_tank_600_gal)
        Fuel_tank_600_gal__EMPTY_ = (6, WeaponsF16I.Fuel_tank_600_gal__EMPTY_)
        IDF_Mods_Project_Fuel_Tank_370_EMPTY = (
            6,
            WeaponsF16I.IDF_Mods_Project_Fuel_Tank_370_EMPTY,
        )
        TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD_ = (
            6,
            Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD_,
        )
        TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_ = (
            6,
            Weapons.TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_,
        )
        TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD_ = (
            6,
            Weapons.TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD_,
        )
        TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb_ = (
            6,
            Weapons.TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb_,
        )
        TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb_ = (
            6,
            Weapons.TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb_,
        )

    class Pylon7:
        AIM_9M_Sidewinder_IR_AAM = (7, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (7, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (7, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            7,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            7,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        CATM_9M = (7, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (7, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        # ERRR {Python-5 Training}
        LAU3_WP156 = (7, Weapons.LAU3_WP156)
        LAU3_WP1B = (7, Weapons.LAU3_WP1B)
        LAU3_WP61 = (7, Weapons.LAU3_WP61)
        LAU3_HE5 = (7, Weapons.LAU3_HE5)
        LAU3_HE151 = (7, Weapons.LAU3_HE151)
        BDU_50LD___500lb_Inert_Practice_Bomb_LD = (
            7,
            Weapons.BDU_50LD___500lb_Inert_Practice_Bomb_LD,
        )
        BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD = (
            7,
            Weapons.BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD,
        )
        BDU_50HD___500lb_Inert_Practice_Bomb_HD = (
            7,
            Weapons.BDU_50HD___500lb_Inert_Practice_Bomb_HD,
        )
        Mk_82___500lb_GP_Bomb_LD = (7, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (7, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            7,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (7, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD = (
            7,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD = (
            7,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD,
        )
        GBU_10___2000lb_Laser_Guided_Bomb = (
            7,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (7, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb = (
            7,
            Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        CBU_87___202_x_CEM_Cluster_Bomb = (7, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (7, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            7,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        BRU_57_with_2_x_CBU_105___10_x_SFW__CBU_with_WCMD = (
            7,
            Weapons.BRU_57_with_2_x_CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            7,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        BRU_57_with_2_x_CBU_103___202_x_CEM__CBU_with_WCMD = (
            7,
            Weapons.BRU_57_with_2_x_CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            7,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            7,
            Weapons.TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD = (
            7,
            Weapons.TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            7,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_117_AGM_65G = (7, Weapons.LAU_117_AGM_65G)
        LAU_117_AGM_65H = (7, Weapons.LAU_117_AGM_65H)
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            7,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_88_AGM_65D_ONE = (7, Weapons.LAU_88_AGM_65D_ONE)
        LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_ = (
            7,
            Weapons.LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_88_AGM_65H = (7, Weapons.LAU_88_AGM_65H)
        LAU_88_AGM_65H_3 = (7, Weapons.LAU_88_AGM_65H_3)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            7,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            Weapons.GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            7,
            Weapons.GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            Weapons.GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )
        BRU_57_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            Weapons.BRU_57_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        AGM_154A___JSOW_CEB__CBU_type_ = (7, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        MXU_648_TP = (7, Weapons.MXU_648_TP)
        ALQ_184 = (7, Weapons.ALQ_184)
        ALQ_184_Long = (7, Weapons.ALQ_184_Long)
        ALQ_131___ECM_Pod = (7, Weapons.ALQ_131___ECM_Pod)
        # ERRR <CLEAN>
        TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD_ = (
            7,
            Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD_,
        )
        TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_ = (
            7,
            Weapons.TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_,
        )
        TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD_ = (
            7,
            Weapons.TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD_,
        )
        TER_9A_with_2_x_GBU_12___500lb_Laser_Guided_Bomb_ = (
            7,
            Weapons.TER_9A_with_2_x_GBU_12___500lb_Laser_Guided_Bomb_,
        )
        TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb_ = (
            7,
            Weapons.TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb_,
        )
        TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb_ = (
            7,
            Weapons.TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb_,
        )
        LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM__ = (
            7,
            Weapons.LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM__,
        )
        LAU_88_AGM_65H_2_R = (7, Weapons.LAU_88_AGM_65H_2_R)
        Pylon_6_7_Mk_82___500lb_GP_Bomb_LD = (
            7,
            WeaponsF16I.Pylon_6_7_Mk_82___500lb_GP_Bomb_LD,
        )
        Pylon_6_7_Mk_84___2000lb_GP_Bomb_LD = (
            7,
            WeaponsF16I.Pylon_6_7_Mk_84___2000lb_GP_Bomb_LD,
        )
        Pylon_6_7_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsF16I.Pylon_6_7_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )
        Pylon_6_7_GBU_31 = (7, WeaponsF16I.Pylon_6_7_GBU_31)
        Pylon_6_7_GBU_12___500lb_Laser_Guided_Bomb = (
            7,
            WeaponsF16I.Pylon_6_7_GBU_12___500lb_Laser_Guided_Bomb,
        )
        Pylon_6_7_GBU_10___2000lb_Laser_Guided_Bomb = (
            7,
            WeaponsF16I.Pylon_6_7_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        Pylon_6_7_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            WeaponsF16I.Pylon_6_7_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        Pylon_6_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            WeaponsF16I.Pylon_6_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        Pylon_6_GBU_31 = (7, WeaponsF16I.Pylon_6_GBU_31)
        Pylon_6_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsF16I.Pylon_6_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )

    class Pylon8:
        AIM_9M_Sidewinder_IR_AAM = (8, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (8, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (8, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            8,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            8,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        CATM_9M = (8, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (8, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

        Python_5_Training = (1, WeaponsF16I.Python_5_Training)

    # ERRR <CLEAN>

    class Pylon9:
        AIM_9M_Sidewinder_IR_AAM = (9, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (9, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (9, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            9,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            9,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        CATM_9M = (9, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (9, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

        Python_5_Training = (1, WeaponsF16I.Python_5_Training)

    class Pylon10:
        AN_ASQ_213_HTS___HARM_Targeting_System = (
            10,
            Weapons.AN_ASQ_213_HTS___HARM_Targeting_System,
        )

    class Pylon11:
        AN_AAQ_28_LITENING___Targeting_Pod = (
            11,
            Weapons.AN_AAQ_28_LITENING___Targeting_Pod,
        )

    class Pylon12:
        Smoke_Generator___red_ = (12, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (12, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (12, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (12, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (12, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (12, Weapons.Smoke_Generator___orange_)

    class Pylon13:
        ALQ_184_Long = (13, Weapons.ALQ_184_Long)

    class Pylon14:
        Crew_Ladder_No_CFT = (14, WeaponsF16I.Crew_Ladder_No_CFT)

    class Pylon15:
        Remove_Before_Flight = (15, WeaponsF16I.Remove_Before_Flight)
        Remove_Before_Flight_without_Lantirn = (
            15,
            WeaponsF16I.Remove_Before_Flight_without_Lantirn,
        )
        Remove_Before_Flight_without_TGP_ = (
            15,
            WeaponsF16I.Remove_Before_Flight_without_TGP_,
        )
        Remove_Before_Flight_without_TGP_And_Lantirn = (
            15,
            WeaponsF16I.Remove_Before_Flight_without_TGP_And_Lantirn,
        )

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.PinpointStrike,
        task.CAS,
        task.GroundAttack,
        task.RunwayAttack,
        task.SEAD,
        task.AFAC,
        task.AntishipStrike,
        task.Reconnaissance,
    ]
    task_default = task.CAP


@planemod
class F_16D_Barak_30(PlaneType):
    id = "F-16D_Barak_30"
    flyable = True
    height = 5.02
    width = 9.45
    length = 14.52
    fuel_max = 2585.48
    max_speed = 2120.04
    chaff = 60
    flare = 60
    charge_total = 120
    chaff_charge_size = 1
    flare_charge_size = 1
    eplrs = True
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 305

    panel_radio = {
        1: {
            "channels": {
                1: 305,
                2: 264,
                4: 256,
                8: 257,
                16: 261,
                17: 267,
                9: 255,
                18: 251,
                5: 254,
                10: 262,
                20: 266,
                11: 259,
                3: 265,
                6: 250,
                12: 268,
                13: 269,
                7: 270,
                14: 260,
                19: 253,
                15: 263,
            },
        },
        2: {
            "channels": {
                1: 127,
                2: 135,
                4: 127,
                8: 128,
                16: 132,
                17: 138,
                9: 126,
                18: 122,
                5: 125,
                10: 133,
                20: 137,
                11: 130,
                3: 136,
                6: 121,
                12: 139,
                13: 140,
                7: 141,
                14: 131,
                19: 124,
                15: 134,
            },
        },
    }

    callnames: Dict[str, List[str]] = {
        "USA": [
            "Viper",
            "Venom",
            "Lobo",
            "Cowboy",
            "Python",
            "Rattler",
            "Panther",
            "Wolf",
            "Weasel",
            "Wild",
            "Ninja",
            "Jedi",
        ]
    }

    property_defaults: Dict[str, Any] = {
        "LAU3ROF": 0,
        "LaserCode100": 6,
        "LaserCode10": 8,
        "LaserCode1": 8,
        "HelmetMountedDevice": 1,
    }

    class Properties:
        class LAU3ROF:
            id = "LAU3ROF"

            class Values:
                Single = 0
                Ripple = 1

        class LaserCode100:
            id = "LaserCode100"

        class LaserCode10:
            id = "LaserCode10"

        class LaserCode1:
            id = "LaserCode1"

        class HelmetMountedDevice:
            id = "HelmetMountedDevice"

            class Values:
                Not_installed = 0
                JHMCS = 1
                NVG = 2

    livery_name = "F-16D_BARAK_30"  # from type

    class Pylon1:
        AIM_9M_Sidewinder_IR_AAM = (1, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (1, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (1, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            1,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            1,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        CATM_9M = (1, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (1, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

        Python_5_Training = (1, WeaponsF16I.Python_5_Training)

    class Pylon2:
        AIM_9M_Sidewinder_IR_AAM = (2, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (2, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (2, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            2,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            2,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        CATM_9M = (2, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (2, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

        Python_5_Training = (1, WeaponsF16I.Python_5_Training)

    # ERRR <CLEAN>

    class Pylon3:
        AIM_9M_Sidewinder_IR_AAM = (3, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (3, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (3, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            3,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            3,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        CATM_9M = (3, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (3, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        Python_5_Training = (1, WeaponsF16I.Python_5_Training)
        LAU3_WP156 = (3, Weapons.LAU3_WP156)
        LAU3_WP1B = (3, Weapons.LAU3_WP1B)
        LAU3_WP61 = (3, Weapons.LAU3_WP61)
        LAU3_HE5 = (3, Weapons.LAU3_HE5)
        LAU3_HE151 = (3, Weapons.LAU3_HE151)
        BDU_50LD___500lb_Inert_Practice_Bomb_LD = (
            3,
            Weapons.BDU_50LD___500lb_Inert_Practice_Bomb_LD,
        )
        BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD = (
            3,
            Weapons.BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD,
        )
        BDU_50HD___500lb_Inert_Practice_Bomb_HD = (
            3,
            Weapons.BDU_50HD___500lb_Inert_Practice_Bomb_HD,
        )
        Mk_82___500lb_GP_Bomb_LD = (3, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (3, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            3,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (3, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD = (
            3,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD = (
            3,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD,
        )
        GBU_10___2000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (3, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        CBU_87___202_x_CEM_Cluster_Bomb = (3, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (3, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            3,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        BRU_57_with_2_x_CBU_105___10_x_SFW__CBU_with_WCMD = (
            3,
            Weapons.BRU_57_with_2_x_CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            3,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        BRU_57_with_2_x_CBU_103___202_x_CEM__CBU_with_WCMD = (
            3,
            Weapons.BRU_57_with_2_x_CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            3,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            3,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            3,
            Weapons.TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD = (
            3,
            Weapons.TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            3,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_117_AGM_65G = (3, Weapons.LAU_117_AGM_65G)
        LAU_117_AGM_65H = (3, Weapons.LAU_117_AGM_65H)
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            3,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_88_AGM_65D_ONE = (3, Weapons.LAU_88_AGM_65D_ONE)
        LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_ = (
            3,
            Weapons.LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_88_AGM_65H = (3, Weapons.LAU_88_AGM_65H)
        LAU_88_AGM_65H_3 = (3, Weapons.LAU_88_AGM_65H_3)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            3,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            Weapons.GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            3,
            Weapons.GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            Weapons.GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )
        BRU_57_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            Weapons.BRU_57_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        AGM_154A___JSOW_CEB__CBU_type_ = (3, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        MXU_648_TP = (3, Weapons.MXU_648_TP)
        ALQ_184 = (3, Weapons.ALQ_184)
        ALQ_184_Long = (3, Weapons.ALQ_184_Long)
        ALQ_131___ECM_Pod = (3, Weapons.ALQ_131___ECM_Pod)
        # ERRR <CLEAN>
        TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD = (
            3,
            Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            3,
            Weapons.TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            3,
            Weapons.TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_2_x_GBU_12___500lb_Laser_Guided_Bomb = (
            3,
            Weapons.TER_9A_with_2_x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb = (
            3,
            Weapons.TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb,
        )
        TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb = (
            3,
            Weapons.TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb,
        )
        LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM_ = (
            3,
            Weapons.LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_88_AGM_65H_2_L = (3, Weapons.LAU_88_AGM_65H_2_L)
        Pylon_3_4_Mk_82___500lb_GP_Bomb_LD = (
            3,
            WeaponsF16I.Pylon_3_4_Mk_82___500lb_GP_Bomb_LD,
        )
        Pylon_3_4_Mk_84___2000lb_GP_Bomb_LD = (
            3,
            WeaponsF16I.Pylon_3_4_Mk_84___2000lb_GP_Bomb_LD,
        )
        Pylon_3_4_GBU_31 = (3, WeaponsF16I.Pylon_3_4_GBU_31)
        Pylon_3_4_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            WeaponsF16I.Pylon_3_4_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )
        Pylon_3_4_GBU_12___500lb_Laser_Guided_Bomb = (
            3,
            WeaponsF16I.Pylon_3_4_GBU_12___500lb_Laser_Guided_Bomb,
        )
        Pylon_3_4_GBU_10___2000lb_Laser_Guided_Bomb = (
            3,
            WeaponsF16I.Pylon_3_4_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        Pylon_3_4_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            WeaponsF16I.Pylon_3_4_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        Pylon_4_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            WeaponsF16I.Pylon_4_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        Pylon_4_GBU_31 = (3, WeaponsF16I.Pylon_4_GBU_31)
        Pylon_4_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            WeaponsF16I.Pylon_4_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )

    class Pylon4:
        LAU3_WP156 = (4, Weapons.LAU3_WP156)
        LAU3_WP1B = (4, Weapons.LAU3_WP1B)
        LAU3_WP61 = (4, Weapons.LAU3_WP61)
        LAU3_HE5 = (4, Weapons.LAU3_HE5)
        LAU3_HE151 = (4, Weapons.LAU3_HE151)
        BDU_50LD___500lb_Inert_Practice_Bomb_LD = (
            4,
            Weapons.BDU_50LD___500lb_Inert_Practice_Bomb_LD,
        )
        BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD = (
            4,
            Weapons.BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD,
        )
        BDU_50HD___500lb_Inert_Practice_Bomb_HD = (
            4,
            Weapons.BDU_50HD___500lb_Inert_Practice_Bomb_HD,
        )
        Mk_82___500lb_GP_Bomb_LD = (4, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (4, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            4,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (4, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD = (
            4,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD = (
            4,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD,
        )
        GBU_10___2000lb_Laser_Guided_Bomb = (
            4,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (4, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb = (
            4,
            Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        CBU_87___202_x_CEM_Cluster_Bomb = (4, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (4, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            4,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            4,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            4,
            Weapons.TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD = (
            4,
            Weapons.TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb = (
            4,
            Weapons.TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb,
        )
        TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb = (
            4,
            Weapons.TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb,
        )
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            4,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        Fuel_tank_370_gal = (4, Weapons.Fuel_tank_370_gal)
        MXU_648_TP = (4, Weapons.MXU_648_TP)
        # ERRR <CLEAN>
        Fuel_tank_600_gal = (4, WeaponsF16I.Fuel_tank_600_gal)
        Fuel_tank_600_gal__EMPTY_ = (4, WeaponsF16I.Fuel_tank_600_gal__EMPTY_)
        IDF_Mods_Project_Fuel_Tank_370_EMPTY = (
            4,
            WeaponsF16I.IDF_Mods_Project_Fuel_Tank_370_EMPTY,
        )
        TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD = (
            4,
            Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            4,
            Weapons.TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            4,
            Weapons.TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb = (
            4,
            Weapons.TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb,
        )
        TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb = (
            4,
            Weapons.TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb,
        )

    class Pylon5:
        Fuel_tank_300_gal = (5, Weapons.Fuel_tank_300_gal)
        Fuel_tank_300_gal_Empty = (5, WeaponsF16I.Fuel_tank_300_gal_Empty)
        MXU_648_TP = (5, Weapons.MXU_648_TP)
        ALQ_184 = (5, Weapons.ALQ_184)
        ALQ_184_Long = (5, Weapons.ALQ_184_Long)
        ALQ_131___ECM_Pod = (5, Weapons.ALQ_131___ECM_Pod)

    # ERRR <CLEAN>

    class Pylon6:
        LAU3_WP156 = (6, Weapons.LAU3_WP156)
        LAU3_WP1B = (6, Weapons.LAU3_WP1B)
        LAU3_WP61 = (6, Weapons.LAU3_WP61)
        LAU3_HE5 = (6, Weapons.LAU3_HE5)
        LAU3_HE151 = (6, Weapons.LAU3_HE151)
        BDU_50LD___500lb_Inert_Practice_Bomb_LD = (
            6,
            Weapons.BDU_50LD___500lb_Inert_Practice_Bomb_LD,
        )
        BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD = (
            6,
            Weapons.BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD,
        )
        BDU_50HD___500lb_Inert_Practice_Bomb_HD = (
            6,
            Weapons.BDU_50HD___500lb_Inert_Practice_Bomb_HD,
        )
        Mk_82___500lb_GP_Bomb_LD = (6, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (6, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            6,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (6, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD = (
            6,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD = (
            6,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD,
        )
        GBU_10___2000lb_Laser_Guided_Bomb = (
            6,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (6, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb = (
            6,
            Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        CBU_87___202_x_CEM_Cluster_Bomb = (6, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (6, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            6,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            6,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            6,
            Weapons.TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD = (
            6,
            Weapons.TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb = (
            6,
            Weapons.TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb,
        )
        TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb = (
            6,
            Weapons.TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb,
        )
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            6,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        Fuel_tank_370_gal = (6, Weapons.Fuel_tank_370_gal)
        MXU_648_TP = (6, Weapons.MXU_648_TP)
        # ERRR <CLEAN>
        Fuel_tank_600_gal = (6, WeaponsF16I.Fuel_tank_600_gal)
        Fuel_tank_600_gal__EMPTY_ = (6, WeaponsF16I.Fuel_tank_600_gal__EMPTY_)
        IDF_Mods_Project_Fuel_Tank_370_EMPTY = (
            6,
            WeaponsF16I.IDF_Mods_Project_Fuel_Tank_370_EMPTY,
        )
        TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD_ = (
            6,
            Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD_,
        )
        TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_ = (
            6,
            Weapons.TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_,
        )
        TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD_ = (
            6,
            Weapons.TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD_,
        )
        TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb_ = (
            6,
            Weapons.TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb_,
        )
        TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb_ = (
            6,
            Weapons.TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb_,
        )

    class Pylon7:
        AIM_9M_Sidewinder_IR_AAM = (7, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (7, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (7, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            7,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            7,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        CATM_9M = (7, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (7, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        Python_5_Training = (1, WeaponsF16I.Python_5_Training)
        LAU3_WP156 = (7, Weapons.LAU3_WP156)
        LAU3_WP1B = (7, Weapons.LAU3_WP1B)
        LAU3_WP61 = (7, Weapons.LAU3_WP61)
        LAU3_HE5 = (7, Weapons.LAU3_HE5)
        LAU3_HE151 = (7, Weapons.LAU3_HE151)
        BDU_50LD___500lb_Inert_Practice_Bomb_LD = (
            7,
            Weapons.BDU_50LD___500lb_Inert_Practice_Bomb_LD,
        )
        BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD = (
            7,
            Weapons.BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD,
        )
        BDU_50HD___500lb_Inert_Practice_Bomb_HD = (
            7,
            Weapons.BDU_50HD___500lb_Inert_Practice_Bomb_HD,
        )
        Mk_82___500lb_GP_Bomb_LD = (7, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (7, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            7,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (7, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD = (
            7,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD = (
            7,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD,
        )
        GBU_10___2000lb_Laser_Guided_Bomb = (
            7,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (7, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb = (
            7,
            Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        CBU_87___202_x_CEM_Cluster_Bomb = (7, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (7, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            7,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        BRU_57_with_2_x_CBU_105___10_x_SFW__CBU_with_WCMD = (
            7,
            Weapons.BRU_57_with_2_x_CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            7,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        BRU_57_with_2_x_CBU_103___202_x_CEM__CBU_with_WCMD = (
            7,
            Weapons.BRU_57_with_2_x_CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            7,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            7,
            Weapons.TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD = (
            7,
            Weapons.TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            7,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_117_AGM_65G = (7, Weapons.LAU_117_AGM_65G)
        LAU_117_AGM_65H = (7, Weapons.LAU_117_AGM_65H)
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            7,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_88_AGM_65D_ONE = (7, Weapons.LAU_88_AGM_65D_ONE)
        LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_ = (
            7,
            Weapons.LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_88_AGM_65H = (7, Weapons.LAU_88_AGM_65H)
        LAU_88_AGM_65H_3 = (7, Weapons.LAU_88_AGM_65H_3)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            7,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            Weapons.GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            7,
            Weapons.GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            Weapons.GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )
        BRU_57_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            Weapons.BRU_57_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        AGM_154A___JSOW_CEB__CBU_type_ = (7, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        MXU_648_TP = (7, Weapons.MXU_648_TP)
        ALQ_184 = (7, Weapons.ALQ_184)
        ALQ_184_Long = (7, Weapons.ALQ_184_Long)
        ALQ_131___ECM_Pod = (7, Weapons.ALQ_131___ECM_Pod)
        # ERRR <CLEAN>
        TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD_ = (
            7,
            Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD_,
        )
        TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_ = (
            7,
            Weapons.TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_,
        )
        TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD_ = (
            7,
            Weapons.TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD_,
        )
        TER_9A_with_2_x_GBU_12___500lb_Laser_Guided_Bomb_ = (
            7,
            Weapons.TER_9A_with_2_x_GBU_12___500lb_Laser_Guided_Bomb_,
        )
        TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb_ = (
            7,
            Weapons.TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb_,
        )
        TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb_ = (
            7,
            Weapons.TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb_,
        )
        LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM__ = (
            7,
            Weapons.LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM__,
        )
        LAU_88_AGM_65H_2_R = (7, Weapons.LAU_88_AGM_65H_2_R)
        Pylon_6_7_Mk_82___500lb_GP_Bomb_LD = (
            7,
            WeaponsF16I.Pylon_6_7_Mk_82___500lb_GP_Bomb_LD,
        )
        Pylon_6_7_Mk_84___2000lb_GP_Bomb_LD = (
            7,
            WeaponsF16I.Pylon_6_7_Mk_84___2000lb_GP_Bomb_LD,
        )
        Pylon_6_7_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsF16I.Pylon_6_7_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )
        Pylon_6_7_GBU_31 = (7, WeaponsF16I.Pylon_6_7_GBU_31)
        Pylon_6_7_GBU_12___500lb_Laser_Guided_Bomb = (
            7,
            WeaponsF16I.Pylon_6_7_GBU_12___500lb_Laser_Guided_Bomb,
        )
        Pylon_6_7_GBU_10___2000lb_Laser_Guided_Bomb = (
            7,
            WeaponsF16I.Pylon_6_7_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        Pylon_6_7_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            WeaponsF16I.Pylon_6_7_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        Pylon_6_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            WeaponsF16I.Pylon_6_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        Pylon_6_GBU_31 = (7, WeaponsF16I.Pylon_6_GBU_31)
        Pylon_6_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsF16I.Pylon_6_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )

    class Pylon8:
        AIM_9M_Sidewinder_IR_AAM = (8, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (8, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (8, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            8,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            8,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        CATM_9M = (8, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (8, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

        Python_5_Training = (1, WeaponsF16I.Python_5_Training)

    # ERRR <CLEAN>

    class Pylon9:
        AIM_9M_Sidewinder_IR_AAM = (9, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (9, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (9, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            9,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            9,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        CATM_9M = (9, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (9, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

        Python_5_Training = (1, WeaponsF16I.Python_5_Training)

    class Pylon10:
        AN_ASQ_213_HTS___HARM_Targeting_System = (
            10,
            Weapons.AN_ASQ_213_HTS___HARM_Targeting_System,
        )

    class Pylon11:
        AN_AAQ_28_LITENING___Targeting_Pod = (
            11,
            Weapons.AN_AAQ_28_LITENING___Targeting_Pod,
        )

    class Pylon12:
        Smoke_Generator___red_ = (12, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (12, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (12, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (12, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (12, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (12, Weapons.Smoke_Generator___orange_)

    class Pylon13:
        ALQ_184_Long = (13, Weapons.ALQ_184_Long)

    class Pylon14:
        Crew_Ladder_No_CFT = (14, WeaponsF16I.Crew_Ladder_No_CFT)

    class Pylon15:
        Remove_Before_Flight = (15, WeaponsF16I.Remove_Before_Flight)
        Remove_Before_Flight_without_Lantirn = (
            15,
            WeaponsF16I.Remove_Before_Flight_without_Lantirn,
        )
        Remove_Before_Flight_without_TGP_ = (
            15,
            WeaponsF16I.Remove_Before_Flight_without_TGP_,
        )
        Remove_Before_Flight_without_TGP_And_Lantirn = (
            15,
            WeaponsF16I.Remove_Before_Flight_without_TGP_And_Lantirn,
        )

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.PinpointStrike,
        task.CAS,
        task.GroundAttack,
        task.RunwayAttack,
        task.SEAD,
        task.AFAC,
        task.AntishipStrike,
        task.Reconnaissance,
    ]
    task_default = task.CAP


@planemod
class F_16I(PlaneType):
    id = "F-16I"
    flyable = True
    height = 5.02
    width = 9.45
    length = 14.52
    fuel_max = 2585.48
    max_speed = 2120.04
    chaff = 60
    flare = 60
    charge_total = 120
    chaff_charge_size = 1
    flare_charge_size = 1
    eplrs = True
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 305

    panel_radio = {
        1: {
            "channels": {
                1: 305,
                2: 264,
                4: 256,
                8: 257,
                16: 261,
                17: 267,
                9: 255,
                18: 251,
                5: 254,
                10: 262,
                20: 266,
                11: 259,
                3: 265,
                6: 250,
                12: 268,
                13: 269,
                7: 270,
                14: 260,
                19: 253,
                15: 263,
            },
        },
        2: {
            "channels": {
                1: 127,
                2: 135,
                4: 127,
                8: 128,
                16: 132,
                17: 138,
                9: 126,
                18: 122,
                5: 125,
                10: 133,
                20: 137,
                11: 130,
                3: 136,
                6: 121,
                12: 139,
                13: 140,
                7: 141,
                14: 131,
                19: 124,
                15: 134,
            },
        },
    }

    callnames: Dict[str, List[str]] = {
        "USA": [
            "Viper",
            "Venom",
            "Lobo",
            "Cowboy",
            "Python",
            "Rattler",
            "Panther",
            "Wolf",
            "Weasel",
            "Wild",
            "Ninja",
            "Jedi",
        ]
    }

    property_defaults: Dict[str, Any] = {
        "LAU3ROF": 0,
        "LaserCode100": 6,
        "LaserCode10": 8,
        "LaserCode1": 8,
        "HelmetMountedDevice": 1,
    }

    class Properties:
        class LAU3ROF:
            id = "LAU3ROF"

            class Values:
                Single = 0
                Ripple = 1

        class LaserCode100:
            id = "LaserCode100"

        class LaserCode10:
            id = "LaserCode10"

        class LaserCode1:
            id = "LaserCode1"

        class HelmetMountedDevice:
            id = "HelmetMountedDevice"

            class Values:
                Not_installed = 0
                JHMCS = 1
                NVG = 2

    livery_name = "F-16I"  # from type

    class Pylon1:
        AIM_9M_Sidewinder_IR_AAM = (1, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (1, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (1, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            1,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            1,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        CATM_9M = (1, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (1, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

        Python_5_Training = (1, WeaponsF16I.Python_5_Training)

    class Pylon2:
        AIM_9M_Sidewinder_IR_AAM = (2, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (2, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (2, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            2,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            2,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        CATM_9M = (2, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (2, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

        Python_5_Training = (1, WeaponsF16I.Python_5_Training)

    # ERRR <CLEAN>

    class Pylon3:
        AIM_9M_Sidewinder_IR_AAM = (3, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (3, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (3, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            3,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            3,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        CATM_9M = (3, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (3, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        LAU3_WP156 = (3, Weapons.LAU3_WP156)
        LAU3_WP1B = (3, Weapons.LAU3_WP1B)
        LAU3_WP61 = (3, Weapons.LAU3_WP61)
        LAU3_HE5 = (3, Weapons.LAU3_HE5)
        LAU3_HE151 = (3, Weapons.LAU3_HE151)
        BDU_50LD___500lb_Inert_Practice_Bomb_LD = (
            3,
            Weapons.BDU_50LD___500lb_Inert_Practice_Bomb_LD,
        )
        BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD = (
            3,
            Weapons.BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD,
        )
        BDU_50HD___500lb_Inert_Practice_Bomb_HD = (
            3,
            Weapons.BDU_50HD___500lb_Inert_Practice_Bomb_HD,
        )
        Mk_82___500lb_GP_Bomb_LD = (3, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (3, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            3,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (3, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD = (
            3,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD = (
            3,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD,
        )
        GBU_10___2000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (3, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        CBU_87___202_x_CEM_Cluster_Bomb = (3, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (3, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            3,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        BRU_57_with_2_x_CBU_105___10_x_SFW__CBU_with_WCMD = (
            3,
            Weapons.BRU_57_with_2_x_CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            3,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        BRU_57_with_2_x_CBU_103___202_x_CEM__CBU_with_WCMD = (
            3,
            Weapons.BRU_57_with_2_x_CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            3,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            3,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            3,
            Weapons.TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD = (
            3,
            Weapons.TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            3,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_117_AGM_65G = (3, Weapons.LAU_117_AGM_65G)
        LAU_117_AGM_65H = (3, Weapons.LAU_117_AGM_65H)
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            3,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_88_AGM_65D_ONE = (3, Weapons.LAU_88_AGM_65D_ONE)
        LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_ = (
            3,
            Weapons.LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_88_AGM_65H = (3, Weapons.LAU_88_AGM_65H)
        LAU_88_AGM_65H_3 = (3, Weapons.LAU_88_AGM_65H_3)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            3,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            Weapons.GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            3,
            Weapons.GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            Weapons.GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )
        BRU_57_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            Weapons.BRU_57_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        AGM_154A___JSOW_CEB__CBU_type_ = (3, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        MXU_648_TP = (3, Weapons.MXU_648_TP)
        ALQ_184 = (3, Weapons.ALQ_184)
        ALQ_184_Long = (3, Weapons.ALQ_184_Long)
        ALQ_131___ECM_Pod = (3, Weapons.ALQ_131___ECM_Pod)
        # ERRR <CLEAN>
        TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD = (
            3,
            Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            3,
            Weapons.TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            3,
            Weapons.TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_2_x_GBU_12___500lb_Laser_Guided_Bomb = (
            3,
            Weapons.TER_9A_with_2_x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb = (
            3,
            Weapons.TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb,
        )
        TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb = (
            3,
            Weapons.TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb,
        )
        LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM_ = (
            3,
            Weapons.LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM_,
        )
        Pylon_3_4_Mk_82___500lb_GP_Bomb_LD = (
            3,
            WeaponsF16I.Pylon_3_4_Mk_82___500lb_GP_Bomb_LD,
        )
        Pylon_3_4_Mk_84___2000lb_GP_Bomb_LD = (
            3,
            WeaponsF16I.Pylon_3_4_Mk_84___2000lb_GP_Bomb_LD,
        )
        Pylon_3_4_GBU_31 = (3, WeaponsF16I.Pylon_3_4_GBU_31)
        Pylon_3_4_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            WeaponsF16I.Pylon_3_4_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )
        Pylon_3_4_GBU_12___500lb_Laser_Guided_Bomb = (
            3,
            WeaponsF16I.Pylon_3_4_GBU_12___500lb_Laser_Guided_Bomb,
        )
        Pylon_3_4_GBU_10___2000lb_Laser_Guided_Bomb = (
            3,
            WeaponsF16I.Pylon_3_4_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        Pylon_3_4_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            WeaponsF16I.Pylon_3_4_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        Pylon_4_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            WeaponsF16I.Pylon_4_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        Pylon_4_GBU_31 = (3, WeaponsF16I.Pylon_4_GBU_31)
        Pylon_4_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            WeaponsF16I.Pylon_4_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )
        LAU_88_AGM_65H_2_L = (3, Weapons.LAU_88_AGM_65H_2_L)

    class Pylon4:
        LAU3_WP156 = (4, Weapons.LAU3_WP156)
        LAU3_WP1B = (4, Weapons.LAU3_WP1B)
        LAU3_WP61 = (4, Weapons.LAU3_WP61)
        LAU3_HE5 = (4, Weapons.LAU3_HE5)
        LAU3_HE151 = (4, Weapons.LAU3_HE151)
        BDU_50LD___500lb_Inert_Practice_Bomb_LD = (
            4,
            Weapons.BDU_50LD___500lb_Inert_Practice_Bomb_LD,
        )
        BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD = (
            4,
            Weapons.BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD,
        )
        BDU_50HD___500lb_Inert_Practice_Bomb_HD = (
            4,
            Weapons.BDU_50HD___500lb_Inert_Practice_Bomb_HD,
        )
        Mk_82___500lb_GP_Bomb_LD = (4, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (4, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            4,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (4, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD = (
            4,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD = (
            4,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD,
        )
        GBU_10___2000lb_Laser_Guided_Bomb = (
            4,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (4, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb = (
            4,
            Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        CBU_87___202_x_CEM_Cluster_Bomb = (4, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (4, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            4,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            4,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            4,
            Weapons.TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD = (
            4,
            Weapons.TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb = (
            4,
            Weapons.TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb,
        )
        TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb = (
            4,
            Weapons.TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb,
        )
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            4,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        Fuel_tank_370_gal = (4, Weapons.Fuel_tank_370_gal)
        MXU_648_TP = (4, Weapons.MXU_648_TP)
        Fuel_tank_600_gal = (4, WeaponsF16I.Fuel_tank_600_gal)
        Fuel_tank_600_gal__EMPTY_ = (4, WeaponsF16I.Fuel_tank_600_gal__EMPTY_)
        IDF_Mods_Project_Fuel_Tank_370_EMPTY = (
            4,
            WeaponsF16I.IDF_Mods_Project_Fuel_Tank_370_EMPTY,
        )
        # ERRR <CLEAN>
        TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD = (
            4,
            Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            4,
            Weapons.TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            4,
            Weapons.TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb = (
            4,
            Weapons.TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb,
        )
        TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb = (
            4,
            Weapons.TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb,
        )
        IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb = (
            4,
            WeaponsF16I.IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb,
        )
        IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb__600Gal = (
            4,
            WeaponsF16I.IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb__600Gal,
        )
        IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb__370Gal = (
            4,
            WeaponsF16I.IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb__370Gal,
        )

    class Pylon5:
        Fuel_tank_300_gal = (5, Weapons.Fuel_tank_300_gal)
        Fuel_tank_300_gal_Empty = (5, WeaponsF16I.Fuel_tank_300_gal_Empty)
        MXU_648_TP = (5, Weapons.MXU_648_TP)
        ALQ_184 = (5, Weapons.ALQ_184)
        ALQ_184_Long = (5, Weapons.ALQ_184_Long)
        ALQ_131___ECM_Pod = (5, Weapons.ALQ_131___ECM_Pod)

    # ERRR <CLEAN>

    class Pylon6:
        LAU3_WP156 = (6, Weapons.LAU3_WP156)
        LAU3_WP1B = (6, Weapons.LAU3_WP1B)
        LAU3_WP61 = (6, Weapons.LAU3_WP61)
        LAU3_HE5 = (6, Weapons.LAU3_HE5)
        LAU3_HE151 = (6, Weapons.LAU3_HE151)
        BDU_50LD___500lb_Inert_Practice_Bomb_LD = (
            6,
            Weapons.BDU_50LD___500lb_Inert_Practice_Bomb_LD,
        )
        BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD = (
            6,
            Weapons.BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD,
        )
        BDU_50HD___500lb_Inert_Practice_Bomb_HD = (
            6,
            Weapons.BDU_50HD___500lb_Inert_Practice_Bomb_HD,
        )
        Mk_82___500lb_GP_Bomb_LD = (6, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (6, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            6,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (6, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD = (
            6,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD = (
            6,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD,
        )
        GBU_10___2000lb_Laser_Guided_Bomb = (
            6,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (6, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb = (
            6,
            Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        CBU_87___202_x_CEM_Cluster_Bomb = (6, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (6, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            6,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            6,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            6,
            Weapons.TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD = (
            6,
            Weapons.TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb = (
            6,
            Weapons.TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb,
        )
        TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb = (
            6,
            Weapons.TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb,
        )
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            6,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        Fuel_tank_370_gal = (6, Weapons.Fuel_tank_370_gal)
        MXU_648_TP = (6, Weapons.MXU_648_TP)
        Fuel_tank_600_gal = (6, WeaponsF16I.Fuel_tank_600_gal)
        Fuel_tank_600_gal__EMPTY_ = (6, WeaponsF16I.Fuel_tank_600_gal__EMPTY_)
        IDF_Mods_Project_Fuel_Tank_370_EMPTY = (
            6,
            WeaponsF16I.IDF_Mods_Project_Fuel_Tank_370_EMPTY,
        )
        # ERRR <CLEAN>
        TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD_ = (
            6,
            Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD_,
        )
        TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_ = (
            6,
            Weapons.TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_,
        )
        TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD_ = (
            6,
            Weapons.TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD_,
        )
        TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb_ = (
            6,
            Weapons.TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb_,
        )
        TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb_ = (
            6,
            Weapons.TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb_,
        )
        IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb = (
            6,
            WeaponsF16I.IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb,
        )
        IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb__370Gal = (
            6,
            WeaponsF16I.IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb__370Gal,
        )
        IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb__600Gal = (
            6,
            WeaponsF16I.IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb__600Gal,
        )

    class Pylon7:
        AIM_9M_Sidewinder_IR_AAM = (7, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (7, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (7, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            7,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            7,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        CATM_9M = (7, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (7, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        LAU3_WP156 = (7, Weapons.LAU3_WP156)
        LAU3_WP1B = (7, Weapons.LAU3_WP1B)
        LAU3_WP61 = (7, Weapons.LAU3_WP61)
        LAU3_HE5 = (7, Weapons.LAU3_HE5)
        LAU3_HE151 = (7, Weapons.LAU3_HE151)
        BDU_50LD___500lb_Inert_Practice_Bomb_LD = (
            7,
            Weapons.BDU_50LD___500lb_Inert_Practice_Bomb_LD,
        )
        BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD = (
            7,
            Weapons.BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD,
        )
        BDU_50HD___500lb_Inert_Practice_Bomb_HD = (
            7,
            Weapons.BDU_50HD___500lb_Inert_Practice_Bomb_HD,
        )
        Mk_82___500lb_GP_Bomb_LD = (7, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (7, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            7,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (7, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD = (
            7,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_GP_Chute_Retarded_Bomb_HD,
        )
        Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD = (
            7,
            Weapons.Mk_84_AIR__BSU_50____2000_lb_TP_Chute_Retarded_Bomb_HD,
        )
        GBU_10___2000lb_Laser_Guided_Bomb = (
            7,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (7, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb = (
            7,
            Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb,
        )
        CBU_87___202_x_CEM_Cluster_Bomb = (7, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (7, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            7,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        BRU_57_with_2_x_CBU_105___10_x_SFW__CBU_with_WCMD = (
            7,
            Weapons.BRU_57_with_2_x_CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            7,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        BRU_57_with_2_x_CBU_103___202_x_CEM__CBU_with_WCMD = (
            7,
            Weapons.BRU_57_with_2_x_CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            7,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            7,
            Weapons.TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD = (
            7,
            Weapons.TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            7,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_117_AGM_65G = (7, Weapons.LAU_117_AGM_65G)
        LAU_117_AGM_65H = (7, Weapons.LAU_117_AGM_65H)
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            7,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_88_AGM_65D_ONE = (7, Weapons.LAU_88_AGM_65D_ONE)
        LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_ = (
            7,
            Weapons.LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_88_AGM_65H = (7, Weapons.LAU_88_AGM_65H)
        LAU_88_AGM_65H_3 = (7, Weapons.LAU_88_AGM_65H_3)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            7,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            Weapons.GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            7,
            Weapons.GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            Weapons.GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )
        BRU_57_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            Weapons.BRU_57_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        AGM_154A___JSOW_CEB__CBU_type_ = (7, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        MXU_648_TP = (7, Weapons.MXU_648_TP)
        ALQ_184 = (7, Weapons.ALQ_184)
        ALQ_184_Long = (7, Weapons.ALQ_184_Long)
        ALQ_131___ECM_Pod = (7, Weapons.ALQ_131___ECM_Pod)
        # ERRR <CLEAN>
        TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD_ = (
            7,
            Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD_,
        )
        TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_ = (
            7,
            Weapons.TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_,
        )
        TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD_ = (
            7,
            Weapons.TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD_,
        )
        TER_9A_with_2_x_GBU_12___500lb_Laser_Guided_Bomb_ = (
            7,
            Weapons.TER_9A_with_2_x_GBU_12___500lb_Laser_Guided_Bomb_,
        )
        TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb_ = (
            7,
            Weapons.TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb_,
        )
        TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb_ = (
            7,
            Weapons.TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb_,
        )
        LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM__ = (
            7,
            Weapons.LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM__,
        )
        Pylon_6_7_Mk_82___500lb_GP_Bomb_LD = (
            7,
            WeaponsF16I.Pylon_6_7_Mk_82___500lb_GP_Bomb_LD,
        )
        Pylon_6_7_Mk_84___2000lb_GP_Bomb_LD = (
            7,
            WeaponsF16I.Pylon_6_7_Mk_84___2000lb_GP_Bomb_LD,
        )
        Pylon_6_7_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsF16I.Pylon_6_7_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )
        Pylon_6_7_GBU_31 = (7, WeaponsF16I.Pylon_6_7_GBU_31)
        Pylon_6_7_GBU_12___500lb_Laser_Guided_Bomb = (
            7,
            WeaponsF16I.Pylon_6_7_GBU_12___500lb_Laser_Guided_Bomb,
        )
        Pylon_6_7_GBU_10___2000lb_Laser_Guided_Bomb = (
            7,
            WeaponsF16I.Pylon_6_7_GBU_10___2000lb_Laser_Guided_Bomb,
        )
        Pylon_6_7_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            WeaponsF16I.Pylon_6_7_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        Pylon_6_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            WeaponsF16I.Pylon_6_GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        Pylon_6_GBU_31 = (7, WeaponsF16I.Pylon_6_GBU_31)
        Pylon_6_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsF16I.Pylon_6_GBU_38_V_1_B___JDAM__500lb_GPS_Guided_Bomb,
        )
        LAU_88_AGM_65H_2_R = (7, Weapons.LAU_88_AGM_65H_2_R)

    class Pylon8:
        AIM_9M_Sidewinder_IR_AAM = (8, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (8, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (8, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            8,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            8,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        CATM_9M = (8, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (8, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

        Python_5_Training = (1, WeaponsF16I.Python_5_Training)

    # ERRR <CLEAN>

    class Pylon9:
        AIM_9M_Sidewinder_IR_AAM = (9, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (9, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (9, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            9,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            9,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        CATM_9M = (9, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (9, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

        Python_5_Training = (1, WeaponsF16I.Python_5_Training)

    class Pylon10:
        AN_ASQ_213_HTS___HARM_Targeting_System = (
            10,
            Weapons.AN_ASQ_213_HTS___HARM_Targeting_System,
        )
        AN_AAQ_13 = (10, WeaponsF16I.AN_AAQ_13)

    class Pylon11:
        AN_AAQ_28_LITENING___Targeting_Pod = (
            11,
            Weapons.AN_AAQ_28_LITENING___Targeting_Pod,
        )

    class Pylon12:
        Smoke_Generator___red_ = (12, Weapons.Smoke_Generator___red_)
        Smoke_Generator___green_ = (12, Weapons.Smoke_Generator___green_)
        Smoke_Generator___blue_ = (12, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (12, Weapons.Smoke_Generator___white_)
        Smoke_Generator___yellow_ = (12, Weapons.Smoke_Generator___yellow_)
        Smoke_Generator___orange_ = (12, Weapons.Smoke_Generator___orange_)

    class Pylon13:
        ALQ_184_Long = (13, Weapons.ALQ_184_Long)

    class Pylon14:
        Crew_Ladder_For_CFT = (14, WeaponsF16I.Crew_Ladder_For_CFT)
        Crew_Ladder_No_CFT = (14, WeaponsF16I.Crew_Ladder_No_CFT)

    class Pylon15:
        Remove_Before_Flight = (15, WeaponsF16I.Remove_Before_Flight)
        Remove_Before_Flight_without_Lantirn = (
            15,
            WeaponsF16I.Remove_Before_Flight_without_Lantirn,
        )
        Remove_Before_Flight_without_TGP_ = (
            15,
            WeaponsF16I.Remove_Before_Flight_without_TGP_,
        )
        Remove_Before_Flight_without_TGP_And_Lantirn = (
            15,
            WeaponsF16I.Remove_Before_Flight_without_TGP_And_Lantirn,
        )

    class Pylon16:
        IDF_Mods_Project_F_16I_CFT = (16, WeaponsF16I.IDF_Mods_Project_F_16I_CFT)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.PinpointStrike,
        task.CAS,
        task.GroundAttack,
        task.RunwayAttack,
        task.SEAD,
        task.AFAC,
        task.AntishipStrike,
        task.Reconnaissance,
    ]
    task_default = task.CAP
