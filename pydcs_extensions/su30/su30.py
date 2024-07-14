from typing import Dict, Any, Set

from dcs import task
from dcs.planes import PlaneType
from dcs.unitpropertydescription import UnitPropertyDescription
from dcs.weapons_data import Weapons

from game.modsupport import planemod
from pydcs_extensions.weapon_injector import inject_weapons


class WeaponsSu30:
    ASTRA_Mk_1___Active_Rdr_AAM = {
        "clsid": "{Su30_ASTRA}",
        "name": "ASTRA Mk.1 - Active Rdr AAM",
        "weight": 154,
    }

    APK_9_POD = {"clsid": "{SU30_APK-9}", "name": "APK-9 POD", "weight": 295}

    BRAHMOS_A_Ship = {"clsid": "{BRAHMOS_S}", "name": "BRAHMOS A-Ship", "weight": 2500}
    BRAHMOS_SEAD = {"clsid": "{BRAHMOS_SEAD}", "name": "BRAHMOS SEAD", "weight": 2500}

    DAMOCLES___Targeting_Pod = {
        "clsid": "{DAMOCLES}",
        "name": "DAMOCLES - Targeting Pod",
        "weight": 208,
    }

    EL_M_2060 = {"clsid": "{SU30_ELM2060}", "name": "EL/M-2060", "weight": 295}

    GBU_38___JDAM__500lb_GPS_Guided_Bomb = {
        "clsid": "{SU30_GBU_38}",
        "name": "GBU-38 - JDAM, 500lb GPS Guided Bomb",
        "weight": 321,
    }

    I_Derby_ER___Active_Rdr_AAM = {
        "clsid": "{Su30_DERBY_ER}",
        "name": "I-Derby ER - Active Rdr AAM",
        "weight": 118,
    }

    KH_29L__AS_14_Kedge___Semi_Act_Laser = {
        "clsid": "{SU30_KH29L}",
        "name": "KH-29L (AS-14 Kedge), Semi-Act Laser",
        "weight": 657,
    }

    KH_29TE__AS_14_Kedge___TV_Guided = {
        "clsid": "{SU30_KH29TE}",
        "name": "KH-29TE (AS-14 Kedge), TV Guided",
        "weight": 1240,
    }

    Kh_31P__AS_17_Krypton____600kg = {
        "clsid": "{SU30_KH31P}",
        "name": "Kh-31P (AS-17 Krypton) - 600kg",
        "weight": 600,
    }
    Kh_36__AS_23____600kg_Grom_E1 = {
        "clsid": "{SU30_KH36}",
        "name": "Kh-36 (AS-23) - 600kg Grom-E1",
        "weight": 600,
    }
    KH_38MTE__AS_23__IR_Guided = {
        "clsid": "{SU30_KH38MTE}",
        "name": "KH-38MTE (AS-23),IR Guided",
        "weight": 505,
    }
    KH_38MLE__AS_23___Semi_Act_Laser = {
        "clsid": "{SU30_KH38MLE}",
        "name": "KH-38MLE (AS-23), Semi-Act Laser",
        "weight": 520,
    }
    Kh_38MAE__AS_23____500kg = {
        "clsid": "{SU30_KH38MAE}",
        "name": "Kh-38MAE (AS-23) - 500kg",
        "weight": 505,
    }
    Kh_59M__AS_18_Kazoo___930kg = {
        "clsid": "{SU30_KH59M}",
        "name": "Kh-59M (AS-18 Kazoo), 930kg",
        "weight": 930,
    }
    Kh_59MK__AS_18_Kazoo____930kg = {
        "clsid": "{SU30_KH59MK}",
        "name": "Kh-59MK (AS-18 Kazoo) - 930kg",
        "weight": 770,
    }
    Kh_31A__AS_17_Krypton____610kg = {
        "clsid": "{SU30_KH_31A}",
        "name": "Kh-31A (AS-17 Krypton) - 610kg",
        "weight": 600,
    }
    Kh_35__AS_20_Kayak____520kg = {
        "clsid": "{Su30_KH_35A}",
        "name": "Kh-35 (AS-20 Kayak) - 520kg",
        "weight": 711,
    }
    Kh_35UE__AS_20_Kayak____520kg = {
        "clsid": "{Su30_KH_35UE}",
        "name": "Kh-35UE (AS-20 Kayak) - 520kg",
        "weight": 711,
    }
    Kh_31AD__AS_17_Krypton____610kg = {
        "clsid": "{SU30_KH31AD}",
        "name": "Kh-31AD (AS-17 Krypton) - 610kg",
        "weight": 715,
    }
    Kh_31PD__AS_17_Krypton____600kg = {
        "clsid": "{SU30_KH31PD}",
        "name": "Kh-31PD (AS-17 Krypton) - 600kg",
        "weight": 707,
    }
    Kh_59MK2__AS_22_Kazoo____700kg = {
        "clsid": "{SU30_KH59MK2}",
        "name": "Kh-59MK2 (AS-22 Kazoo) - 700kg",
        "weight": 700,
    }
    KAB_500S___500kg__GPS_Guided = {
        "clsid": "{SU30_KAB_500S_LOADOUT}",
        "name": "KAB-500S - 500kg, GPS Guided",
        "weight": 500,
    }
    FAB_500_M54___474kg__freefall = {
        "clsid": "{Su30_FAB500M54}",
        "name": "FAB-500 M54 - 474kg, freefall",
        "weight": 474,
    }
    FAB_500_M62___474kg__freefall = {
        "clsid": "{Su30_FAB500M62}",
        "name": "FAB-500 M62 - 474kg, freefall",
        "weight": 241,
    }
    FAB_500M62_UMPK__500kg_Glide_Bomb = {
        "clsid": "{Su30_UMPKFAB500M62}",
        "name": "FAB-500M62 UMPK, 500kg Glide Bomb",
        "weight": 570,
    }
    FAB_250_M62___227kg__freefall = {
        "clsid": "{Su30_FAB250M62}",
        "name": "FAB-250 M62 - 227kg, freefall",
        "weight": 241,
    }
    FAB_500M62_NV__500kg_Parachute = {
        "clsid": "{Su30_FAB500M62NV}",
        "name": "FAB-500M62 NV, 500kg Parachute",
        "weight": 277,
    }
    RN_244___260kg__Tactic_Nuclear_bomb = {
        "clsid": "{SU30_244N}",
        "name": "RN-244 - 260kg, Tactic Nuclear bomb",
        "weight": 260,
    }

    KAB_500S___500kg = {
        "clsid": "{SU30_KAB_500S_LOADOUT}",
        "name": "KAB-500S - 500kg",
        "weight": 500,
    }

    KAB_1500Kr___1500kg = {
        "clsid": "{SU30_KAB_1500Kr_LOADOUT}",
        "name": "KAB-1500Kr - 1500kg",
        "weight": 1560,
    }

    KAB_1500LG_PR___1500kg = {
        "clsid": "{SU30_KAB_1500LG_LOADOUT}",
        "name": "KAB-1500LG PR - 1500kg",
        "weight": 1525,
    }

    LITENING___Targeting_Pod = {
        "clsid": "{LITENING_POD}",
        "name": "LITENING - Targeting Pod",
        "weight": 1.4789,
    }

    MBD3_U6_68_with_6_x_FAB_250___250kg = {
        "clsid": "{Su30_MBD3-U6-68-250}",
        "name": "MBD3-U6-68 with 6 x FAB-250 - 250kg",
        "weight": 1560,
    }

    MBD3_U6_68_with_6_x_FAB_100___100kg = {
        "clsid": "{Su30_MBD3-U6-68-100}",
        "name": "MBD3-U6-68 with 6 x FAB-100 - 100kg",
        "weight": 660,
    }

    R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = {
        "clsid": "{SU30_R27R}",
        "name": "R-27R1 (AA-10 Alamo A) - Semi-Act Rdr",
        "weight": 253,
    }

    R_27T1__AA_10_Alamo_B____Infra_Red = {
        "clsid": "{SU30_R27T}",
        "name": "R-27T1 (AA-10 Alamo B) - Infra Red",
        "weight": 245,
    }

    R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = {
        "clsid": "{SU30_R27ER}",
        "name": "R-27ER1 (AA-10 Alamo C) - Semi-Act Extended Range",
        "weight": 350,
    }

    R_27ET1__AA_10_Alamo_D____IR_Extended_Range = {
        "clsid": "{SU30_R27ET}",
        "name": "R-27ET1 (AA-10 Alamo D) - IR Extended Range",
        "weight": 343,
    }

    R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range = {
        "clsid": "{SU30_R27EA}",
        "name": "R-27EA (AA-10 Alamo) - Active Rdr Extended Range",
        "weight": 350,
    }

    R_27EP1__AA_10_Alamo_F____Passive_Rdr_Extended_Range = {
        "clsid": "{SU30_R27EP}",
        "name": "R-27EP1 (AA-10 Alamo F) - Passive Rdr Extended Range",
        "weight": 350,
    }

    R_27P1__AA_10_Alamo_E____Passive_Rdr = {
        "clsid": "{SU30_R27P}",
        "name": "R-27P1 (AA-10 Alamo E) - Passive Rdr",
        "weight": 253,
    }

    R_37M__AA_13_Axehead____Active_Rdr = {
        "clsid": "{SU30-R37M-AA}",
        "name": "R-37M (AA-13 Axehead) - Active Rdr",
        "weight": 510,
    }

    R_73L__AA_11_Archer_L____Infra_Red = {
        "clsid": "{Su30-R-73L-AA}",
        "name": "R-73L (AA-11 Archer L) - Infra Red",
        "weight": 106,
    }

    R_73M__AA_11_Archer_M____Infra_Red = {
        "clsid": "{Su30-R-73M-AA}",
        "name": "R-73M (AA-11 Archer M) - Infra Red",
        "weight": 110,
    }

    R_77__AA_12_Adder_Early____Active_Rdr = {
        "clsid": "{SU30_R77}",
        "name": "R-77 (AA-12 Adder Early) - Active Rdr",
        "weight": 175,
    }

    R_77_1__AA_12_Adder_B____Active_Rdr = {
        "clsid": "{SU30_R771}",
        "name": "R-77-1 (AA-12 Adder B) - Active Rdr",
        "weight": 190,
    }

    R_77M__AA_12_Adder_C____Active_Rdr = {
        "clsid": "{SU30_R77M}",
        "name": "R-77M (AA-12 Adder C) - Active Rdr",
        "weight": 190,
    }

    R_77PD__AA_12_Adder____Active_Rdr_Ramjet = {
        "clsid": "{SU30_R77PD}",
        "name": "R-77PD (AA-12 Adder) - Active Rdr Ramjet",
        "weight": 225,
    }

    RVV_AE__AA_12_Adder____Active_Rdr = {
        "clsid": "{SU30_RVVAE}",
        "name": "RVV-AE (AA-12 Adder) - Active Rdr",
        "weight": 175,
    }

    RVV_SD__AA_12_Adder_B____Active_Rdr = {
        "clsid": "{SU30_RVVSD}",
        "name": "RVV-SD (AA-12 Adder B) - Active Rdr",
        "weight": 190,
    }

    RVV_MD2__AA_11_Archer_M2____Infra_Red = {
        "clsid": "{Su30-RVV-MD2-AA}",
        "name": "RVV-MD2 (AA-11 Archer M2) - Infra Red",
        "weight": 117,
    }

    Rudra_M1 = {"clsid": "{SU30_RudraM1}", "name": "Rudra-M1", "weight": 690}

    RN_244___260kg__nuclear_bomb = {
        "clsid": "{SU30_244N}",
        "name": "RN-244 - 260kg, nuclear bomb",
        "weight": 260,
    }

    SAP_518_ECM_Pod__Left_ = {
        "clsid": "{SU30_SAP_518_L}",
        "name": "SAP-518 ECM Pod (Left)",
        "weight": 150,
    }

    SAP_518_ECM_Pod__Right_ = {
        "clsid": "{SU30_SAP_518_R}",
        "name": "SAP-518 ECM Pod (Right)",
        "weight": 150,
    }

    SAAW_POD = {"clsid": "{SU30_SAAW}", "name": "SAAW POD", "weight": 570}

    Smoke_Generator___Black = {
        "clsid": "{SMOKE-POD-BLACK}",
        "name": "Smoke Generator - Black",
        "weight": 220,
    }


inject_weapons(WeaponsSu30)


@planemod
class Su_30SM(PlaneType):
    id = "Su-30SM"
    flyable = True
    height = 5.932
    width = 14.7
    length = 21.935
    fuel_max = 9500
    max_speed = 2499.984
    chaff = 96
    flare = 96
    charge_total = 192
    chaff_charge_size = 1
    flare_charge_size = 1
    eplrs = True
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}

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
                1: 117,
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

    property_defaults: Dict[str, Any] = {
        "SoloFlight": False,
        "NetCrewControlPriority": 0,
        "HumanOrchestra": False,
        "HelmetMountedDevice": 1,
        "ShowLadders": True,
        "su30Chaff": 96,
        "su30Flare": 96,
    }

    class Properties:
        class SoloFlight:
            id = "SoloFlight"

        class NetCrewControlPriority:
            id = "NetCrewControlPriority"

            class Values:
                Pilot = 0
                WSO = 1
                Ask_Always = -1
                Equally_Responsible = -2

        class HumanOrchestra:
            id = "HumanOrchestra"

        class HelmetMountedDevice:
            id = "HelmetMountedDevice"

            class Values:
                Not_installed = 0
                SURA_Visor = 1
                NVG = 2

        class ShowLadders:
            id = "ShowLadders"

        class su30Chaff:
            id = "su30Chaff"

        class su30Flare:
            id = "su30Flare"

    properties = {
        "SoloFlight": UnitPropertyDescription(
            identifier="SoloFlight",
            control="checkbox",
            label="Solo Flight",
            player_only=True,
            default=False,
            weight_when_on=-80,
        ),
        "NetCrewControlPriority": UnitPropertyDescription(
            identifier="NetCrewControlPriority",
            control="comboList",
            label="Aircraft Control Priority",
            player_only=True,
            default=0,
            w_ctrl=150,
            values={
                0: "Pilot",
                1: "WSO",
                -1: "Ask Always",
                -2: "Equally Responsible",
            },
        ),
        "HumanOrchestra": UnitPropertyDescription(
            identifier="HumanOrchestra",
            control="checkbox",
            label="Disable Multicrew",
            player_only=True,
            default=False,
        ),
        "HelmetMountedDevice": UnitPropertyDescription(
            identifier="HelmetMountedDevice",
            control="comboList",
            label="Helmet Mounted Device",
            player_only=True,
            default=1,
            w_ctrl=150,
            values={
                0: "Not installed",
                1: "SURA Visor",
                2: "NVG",
            },
        ),
        "ShowLadders": UnitPropertyDescription(
            identifier="ShowLadders",
            control="checkbox",
            label="Show Ladders",
            default=True,
        ),
        "su30Chaff": UnitPropertyDescription(
            identifier="su30Chaff",
            control="spinbox",
            label="Chaff",
            player_only=True,
            minimum=0,
            maximum=192,
            default=96,
            dimension=" ",
        ),
        "su30Flare": UnitPropertyDescription(
            identifier="su30Flare",
            control="spinbox",
            label="Flare",
            player_only=True,
            minimum=0,
            maximum=192,
            default=96,
            dimension=" ",
        ),
    }

    livery_name = "SU-30SM"  # from type

    class Pylon1:
        R_73__AA_11_Archer____Infra_Red = (1, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            1,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            1,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            1,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        L005_Sorbtsiya_ECM_pod__left_ = (1, Weapons.L005_Sorbtsiya_ECM_pod__left_)
        SAP_518_ECM_Pod__Left_ = (1, WeaponsSu30.SAP_518_ECM_Pod__Left_)
        Smoke_Generator___red = (1, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (1, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (1, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (1, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (1, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (1, Weapons.Smoke_Generator___orange)
        Smoke_Generator___Black = (1, WeaponsSu30.Smoke_Generator___Black)

    class Pylon2:
        R_73__AA_11_Archer____Infra_Red = (2, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            2,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            2,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            2,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        R_77__AA_12_Adder_Early____Active_Rdr = (
            2,
            WeaponsSu30.R_77__AA_12_Adder_Early____Active_Rdr,
        )
        R_77_1__AA_12_Adder_B____Active_Rdr = (
            2,
            WeaponsSu30.R_77_1__AA_12_Adder_B____Active_Rdr,
        )
        R_77M__AA_12_Adder_C____Active_Rdr = (
            2,
            WeaponsSu30.R_77M__AA_12_Adder_C____Active_Rdr,
        )
        Smoke_Generator___red = (2, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (2, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (2, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (2, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (2, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (2, Weapons.Smoke_Generator___orange)
        Smoke_Generator___Black = (2, WeaponsSu30.Smoke_Generator___Black)

    # ERRR <CLEAN>

    class Pylon3:
        R_73__AA_11_Archer____Infra_Red = (3, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            3,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            3,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            3,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            3,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27T1__AA_10_Alamo_B____Infra_Red = (
            3,
            WeaponsSu30.R_27T1__AA_10_Alamo_B____Infra_Red,
        )
        R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range = (
            3,
            WeaponsSu30.R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            3,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_27ET1__AA_10_Alamo_D____IR_Extended_Range = (
            3,
            WeaponsSu30.R_27ET1__AA_10_Alamo_D____IR_Extended_Range,
        )
        R_27EP1__AA_10_Alamo_F____Passive_Rdr_Extended_Range = (
            3,
            WeaponsSu30.R_27EP1__AA_10_Alamo_F____Passive_Rdr_Extended_Range,
        )
        R_27P1__AA_10_Alamo_E____Passive_Rdr = (
            3,
            WeaponsSu30.R_27P1__AA_10_Alamo_E____Passive_Rdr,
        )
        R_77__AA_12_Adder_Early____Active_Rdr = (
            3,
            WeaponsSu30.R_77__AA_12_Adder_Early____Active_Rdr,
        )
        R_77_1__AA_12_Adder_B____Active_Rdr = (
            3,
            WeaponsSu30.R_77_1__AA_12_Adder_B____Active_Rdr,
        )
        R_77M__AA_12_Adder_C____Active_Rdr = (
            3,
            WeaponsSu30.R_77M__AA_12_Adder_C____Active_Rdr,
        )
        R_77PD__AA_12_Adder____Active_Rdr_Ramjet = (
            3,
            WeaponsSu30.R_77PD__AA_12_Adder____Active_Rdr_Ramjet,
        )
        R_37M__AA_13_Axehead____Active_Rdr = (
            3,
            WeaponsSu30.R_37M__AA_13_Axehead____Active_Rdr,
        )
        Kh_31P__AS_17_Krypton____600kg = (3, WeaponsSu30.Kh_31P__AS_17_Krypton____600kg)
        Kh_36__AS_23____600kg_Grom_E1 = (3, WeaponsSu30.Kh_36__AS_23____600kg_Grom_E1)
        KH_38MTE__AS_23__IR_Guided = (3, WeaponsSu30.KH_38MTE__AS_23__IR_Guided)
        KH_38MLE__AS_23___Semi_Act_Laser = (
            3,
            WeaponsSu30.KH_38MLE__AS_23___Semi_Act_Laser,
        )
        Kh_38MAE__AS_23____500kg = (3, WeaponsSu30.Kh_38MAE__AS_23____500kg)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            3,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            3,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            3,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        # ERRR {JAS39_AGM_65K}
        Kh_59M__AS_18_Kazoo___930kg = (3, WeaponsSu30.Kh_59M__AS_18_Kazoo___930kg)
        Kh_59MK__AS_18_Kazoo____930kg = (3, WeaponsSu30.Kh_59MK__AS_18_Kazoo____930kg)
        Kh_31A__AS_17_Krypton____610kg = (3, WeaponsSu30.Kh_31A__AS_17_Krypton____610kg)
        Kh_35__AS_20_Kayak____520kg = (3, WeaponsSu30.Kh_35__AS_20_Kayak____520kg)
        Kh_35UE__AS_20_Kayak____520kg = (3, WeaponsSu30.Kh_35UE__AS_20_Kayak____520kg)
        Kh_31AD__AS_17_Krypton____610kg = (
            3,
            WeaponsSu30.Kh_31AD__AS_17_Krypton____610kg,
        )
        Kh_31PD__AS_17_Krypton____600kg = (
            3,
            WeaponsSu30.Kh_31PD__AS_17_Krypton____600kg,
        )
        Kh_59MK2__AS_22_Kazoo____700kg = (3, WeaponsSu30.Kh_59MK2__AS_22_Kazoo____700kg)
        KAB_500Kr___500kg_TV_Guided_Bomb = (3, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (3, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            3,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            3,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            3,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            3,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (3, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            3,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            3,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            3,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M54___474kg__freefall = (3, WeaponsSu30.FAB_500_M54___474kg__freefall)
        FAB_500_M62___474kg__freefall = (3, WeaponsSu30.FAB_500_M62___474kg__freefall)
        FAB_500M62_UMPK__500kg_Glide_Bomb = (
            3,
            WeaponsSu30.FAB_500M62_UMPK__500kg_Glide_Bomb,
        )
        FAB_250_M62___227kg__freefall = (3, WeaponsSu30.FAB_250_M62___227kg__freefall)
        FAB_500M62_NV__500kg_Parachute = (3, WeaponsSu30.FAB_500M62_NV__500kg_Parachute)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            3,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            3,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            3,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        _2_x_B_13L_pods___10_x_S_13_OF__122mm_UnGd_Rkts__Blast_Frag = (
            3,
            Weapons._2_x_B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            3,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange = (
            3,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8OFP2_MPP = (
            3,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8OFP2_MPP,
        )
        _2_x_S_25 = (3, Weapons._2_x_S_25)

    # ERRR <CLEAN>

    class Pylon4:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            4,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range = (
            4,
            WeaponsSu30.R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            4,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_77__AA_12_Adder_Early____Active_Rdr = (
            4,
            WeaponsSu30.R_77__AA_12_Adder_Early____Active_Rdr,
        )
        R_77_1__AA_12_Adder_B____Active_Rdr = (
            4,
            WeaponsSu30.R_77_1__AA_12_Adder_B____Active_Rdr,
        )
        R_77M__AA_12_Adder_C____Active_Rdr = (
            4,
            WeaponsSu30.R_77M__AA_12_Adder_C____Active_Rdr,
        )
        R_77PD__AA_12_Adder____Active_Rdr_Ramjet = (
            4,
            WeaponsSu30.R_77PD__AA_12_Adder____Active_Rdr_Ramjet,
        )
        R_37M__AA_13_Axehead____Active_Rdr = (
            4,
            WeaponsSu30.R_37M__AA_13_Axehead____Active_Rdr,
        )
        Kh_31P__AS_17_Krypton____600kg = (4, WeaponsSu30.Kh_31P__AS_17_Krypton____600kg)
        Kh_36__AS_23____600kg_Grom_E1 = (4, WeaponsSu30.Kh_36__AS_23____600kg_Grom_E1)
        KH_38MTE__AS_23__IR_Guided = (4, WeaponsSu30.KH_38MTE__AS_23__IR_Guided)
        KH_38MLE__AS_23___Semi_Act_Laser = (
            4,
            WeaponsSu30.KH_38MLE__AS_23___Semi_Act_Laser,
        )
        Kh_38MAE__AS_23____500kg = (4, WeaponsSu30.Kh_38MAE__AS_23____500kg)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            4,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            4,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            4,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_59M__AS_18_Kazoo___930kg = (4, WeaponsSu30.Kh_59M__AS_18_Kazoo___930kg)
        Kh_59MK__AS_18_Kazoo____930kg = (4, WeaponsSu30.Kh_59MK__AS_18_Kazoo____930kg)
        Kh_31A__AS_17_Krypton____610kg = (4, WeaponsSu30.Kh_31A__AS_17_Krypton____610kg)
        Kh_35__AS_20_Kayak____520kg = (4, WeaponsSu30.Kh_35__AS_20_Kayak____520kg)
        Kh_35UE__AS_20_Kayak____520kg = (4, WeaponsSu30.Kh_35UE__AS_20_Kayak____520kg)
        Kh_31AD__AS_17_Krypton____610kg = (
            4,
            WeaponsSu30.Kh_31AD__AS_17_Krypton____610kg,
        )
        Kh_31PD__AS_17_Krypton____600kg = (
            4,
            WeaponsSu30.Kh_31PD__AS_17_Krypton____600kg,
        )
        Kh_59MK2__AS_22_Kazoo____700kg = (4, WeaponsSu30.Kh_59MK2__AS_22_Kazoo____700kg)
        KAB_500Kr___500kg_TV_Guided_Bomb = (4, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (4, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_1500Kr___1500kg = (4, WeaponsSu30.KAB_1500Kr___1500kg)
        KAB_1500LG_PR___1500kg = (4, WeaponsSu30.KAB_1500LG_PR___1500kg)
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            4,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            4,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            4,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            4,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            4,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (4, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            4,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            4,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            4,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M54___474kg__freefall = (4, WeaponsSu30.FAB_500_M54___474kg__freefall)
        FAB_500_M62___474kg__freefall = (4, WeaponsSu30.FAB_500_M62___474kg__freefall)
        FAB_500M62_UMPK__500kg_Glide_Bomb = (
            4,
            WeaponsSu30.FAB_500M62_UMPK__500kg_Glide_Bomb,
        )
        FAB_250_M62___227kg__freefall = (4, WeaponsSu30.FAB_250_M62___227kg__freefall)
        FAB_500M62_NV__500kg_Parachute = (4, WeaponsSu30.FAB_500M62_NV__500kg_Parachute)
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            4,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            4,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            4,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD = (
            4,
            Weapons.MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            4,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )

    # ERRR <CLEAN>

    class Pylon5:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            5,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range = (
            5,
            WeaponsSu30.R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            5,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_77__AA_12_Adder_Early____Active_Rdr = (
            5,
            WeaponsSu30.R_77__AA_12_Adder_Early____Active_Rdr,
        )
        R_77_1__AA_12_Adder_B____Active_Rdr = (
            5,
            WeaponsSu30.R_77_1__AA_12_Adder_B____Active_Rdr,
        )
        R_77M__AA_12_Adder_C____Active_Rdr = (
            5,
            WeaponsSu30.R_77M__AA_12_Adder_C____Active_Rdr,
        )
        R_77PD__AA_12_Adder____Active_Rdr_Ramjet = (
            5,
            WeaponsSu30.R_77PD__AA_12_Adder____Active_Rdr_Ramjet,
        )
        R_37M__AA_13_Axehead____Active_Rdr = (
            5,
            WeaponsSu30.R_37M__AA_13_Axehead____Active_Rdr,
        )
        Kh_31P__AS_17_Krypton____600kg = (5, WeaponsSu30.Kh_31P__AS_17_Krypton____600kg)
        Kh_36__AS_23____600kg_Grom_E1 = (5, WeaponsSu30.Kh_36__AS_23____600kg_Grom_E1)
        KH_38MTE__AS_23__IR_Guided = (5, WeaponsSu30.KH_38MTE__AS_23__IR_Guided)
        KH_38MLE__AS_23___Semi_Act_Laser = (
            5,
            WeaponsSu30.KH_38MLE__AS_23___Semi_Act_Laser,
        )
        Kh_38MAE__AS_23____500kg = (5, WeaponsSu30.Kh_38MAE__AS_23____500kg)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            5,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            5,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            5,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_31A__AS_17_Krypton____610kg = (5, WeaponsSu30.Kh_31A__AS_17_Krypton____610kg)
        Kh_31AD__AS_17_Krypton____610kg = (
            5,
            WeaponsSu30.Kh_31AD__AS_17_Krypton____610kg,
        )
        Kh_31PD__AS_17_Krypton____600kg = (
            5,
            WeaponsSu30.Kh_31PD__AS_17_Krypton____600kg,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (5, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (5, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            5,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            5,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        P_50T___50kg_Practice_Bomb_LD = (5, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            5,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            5,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            5,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M54___474kg__freefall = (5, WeaponsSu30.FAB_500_M54___474kg__freefall)
        FAB_500_M62___474kg__freefall = (5, WeaponsSu30.FAB_500_M62___474kg__freefall)
        FAB_500M62_UMPK__500kg_Glide_Bomb = (
            5,
            WeaponsSu30.FAB_500M62_UMPK__500kg_Glide_Bomb,
        )
        FAB_250_M62___227kg__freefall = (5, WeaponsSu30.FAB_250_M62___227kg__freefall)
        FAB_500M62_NV__500kg_Parachute = (5, WeaponsSu30.FAB_500M62_NV__500kg_Parachute)
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            5,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            5,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            5,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            5,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )
        APK_9_POD = (5, WeaponsSu30.APK_9_POD)
        L_081_Fantasmagoria_ELINT_pod = (5, Weapons.L_081_Fantasmagoria_ELINT_pod)

    # ERRR <CLEAN>

    class Pylon6:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            6,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range = (
            6,
            WeaponsSu30.R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            6,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_77__AA_12_Adder_Early____Active_Rdr = (
            6,
            WeaponsSu30.R_77__AA_12_Adder_Early____Active_Rdr,
        )
        R_77_1__AA_12_Adder_B____Active_Rdr = (
            6,
            WeaponsSu30.R_77_1__AA_12_Adder_B____Active_Rdr,
        )
        R_77M__AA_12_Adder_C____Active_Rdr = (
            6,
            WeaponsSu30.R_77M__AA_12_Adder_C____Active_Rdr,
        )
        R_77PD__AA_12_Adder____Active_Rdr_Ramjet = (
            6,
            WeaponsSu30.R_77PD__AA_12_Adder____Active_Rdr_Ramjet,
        )
        R_37M__AA_13_Axehead____Active_Rdr = (
            6,
            WeaponsSu30.R_37M__AA_13_Axehead____Active_Rdr,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (6, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (6, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_1500Kr___1500kg = (6, WeaponsSu30.KAB_1500Kr___1500kg)
        KAB_1500LG_PR___1500kg = (6, WeaponsSu30.KAB_1500LG_PR___1500kg)
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            6,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            6,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            6,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            6,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            6,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        P_50T___50kg_Practice_Bomb_LD = (6, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            6,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            6,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            6,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M54___474kg__freefall = (6, WeaponsSu30.FAB_500_M54___474kg__freefall)
        FAB_500_M62___474kg__freefall = (6, WeaponsSu30.FAB_500_M62___474kg__freefall)
        FAB_500M62_UMPK__500kg_Glide_Bomb = (
            6,
            WeaponsSu30.FAB_500M62_UMPK__500kg_Glide_Bomb,
        )
        FAB_250_M62___227kg__freefall = (6, WeaponsSu30.FAB_250_M62___227kg__freefall)
        FAB_500M62_NV__500kg_Parachute = (6, WeaponsSu30.FAB_500M62_NV__500kg_Parachute)
        RN_244___260kg__Tactic_Nuclear_bomb = (
            6,
            WeaponsSu30.RN_244___260kg__Tactic_Nuclear_bomb,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            6,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            6,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            6,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            6,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )
        RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag = (
            6,
            Weapons.RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag,
        )
        RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP = (
            6,
            Weapons.RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP,
        )

    # ERRR <CLEAN>

    class Pylon7:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            7,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range = (
            7,
            WeaponsSu30.R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            7,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_77__AA_12_Adder_Early____Active_Rdr = (
            7,
            WeaponsSu30.R_77__AA_12_Adder_Early____Active_Rdr,
        )
        R_77_1__AA_12_Adder_B____Active_Rdr = (
            7,
            WeaponsSu30.R_77_1__AA_12_Adder_B____Active_Rdr,
        )
        R_77M__AA_12_Adder_C____Active_Rdr = (
            7,
            WeaponsSu30.R_77M__AA_12_Adder_C____Active_Rdr,
        )
        R_77PD__AA_12_Adder____Active_Rdr_Ramjet = (
            7,
            WeaponsSu30.R_77PD__AA_12_Adder____Active_Rdr_Ramjet,
        )
        R_37M__AA_13_Axehead____Active_Rdr = (
            7,
            WeaponsSu30.R_37M__AA_13_Axehead____Active_Rdr,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (7, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (7, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            7,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            7,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (7, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            7,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            7,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            7,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M54___474kg__freefall = (7, WeaponsSu30.FAB_500_M54___474kg__freefall)
        FAB_500_M62___474kg__freefall = (7, WeaponsSu30.FAB_500_M62___474kg__freefall)
        FAB_500M62_UMPK__500kg_Glide_Bomb = (
            7,
            WeaponsSu30.FAB_500M62_UMPK__500kg_Glide_Bomb,
        )
        FAB_250_M62___227kg__freefall = (7, WeaponsSu30.FAB_250_M62___227kg__freefall)
        FAB_500M62_NV__500kg_Parachute = (7, WeaponsSu30.FAB_500M62_NV__500kg_Parachute)
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            7,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            7,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            7,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            7,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            7,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            7,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )
        Smoke_Generator___red = (7, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (7, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (7, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (7, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (7, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (7, Weapons.Smoke_Generator___orange)
        Smoke_Generator___Black = (7, WeaponsSu30.Smoke_Generator___Black)
        RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag = (
            7,
            Weapons.RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag,
        )
        RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP = (
            7,
            Weapons.RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP,
        )

    # ERRR <CLEAN>

    class Pylon8:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            8,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range = (
            8,
            WeaponsSu30.R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            8,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_77__AA_12_Adder_Early____Active_Rdr = (
            8,
            WeaponsSu30.R_77__AA_12_Adder_Early____Active_Rdr,
        )
        R_77_1__AA_12_Adder_B____Active_Rdr = (
            8,
            WeaponsSu30.R_77_1__AA_12_Adder_B____Active_Rdr,
        )
        R_77M__AA_12_Adder_C____Active_Rdr = (
            8,
            WeaponsSu30.R_77M__AA_12_Adder_C____Active_Rdr,
        )
        R_77PD__AA_12_Adder____Active_Rdr_Ramjet = (
            8,
            WeaponsSu30.R_77PD__AA_12_Adder____Active_Rdr_Ramjet,
        )
        R_37M__AA_13_Axehead____Active_Rdr = (
            8,
            WeaponsSu30.R_37M__AA_13_Axehead____Active_Rdr,
        )
        Kh_31P__AS_17_Krypton____600kg = (8, WeaponsSu30.Kh_31P__AS_17_Krypton____600kg)
        Kh_36__AS_23____600kg_Grom_E1 = (8, WeaponsSu30.Kh_36__AS_23____600kg_Grom_E1)
        KH_38MTE__AS_23__IR_Guided = (8, WeaponsSu30.KH_38MTE__AS_23__IR_Guided)
        KH_38MLE__AS_23___Semi_Act_Laser = (
            8,
            WeaponsSu30.KH_38MLE__AS_23___Semi_Act_Laser,
        )
        Kh_38MAE__AS_23____500kg = (8, WeaponsSu30.Kh_38MAE__AS_23____500kg)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            8,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            8,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            8,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_31A__AS_17_Krypton____610kg = (8, WeaponsSu30.Kh_31A__AS_17_Krypton____610kg)
        Kh_31AD__AS_17_Krypton____610kg = (
            8,
            WeaponsSu30.Kh_31AD__AS_17_Krypton____610kg,
        )
        Kh_31PD__AS_17_Krypton____600kg = (
            8,
            WeaponsSu30.Kh_31PD__AS_17_Krypton____600kg,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (8, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (8, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            8,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            8,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        P_50T___50kg_Practice_Bomb_LD = (8, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            8,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            8,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            8,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M54___474kg__freefall = (8, WeaponsSu30.FAB_500_M54___474kg__freefall)
        FAB_500_M62___474kg__freefall = (8, WeaponsSu30.FAB_500_M62___474kg__freefall)
        FAB_500M62_UMPK__500kg_Glide_Bomb = (
            8,
            WeaponsSu30.FAB_500M62_UMPK__500kg_Glide_Bomb,
        )
        FAB_250_M62___227kg__freefall = (8, WeaponsSu30.FAB_250_M62___227kg__freefall)
        FAB_500M62_NV__500kg_Parachute = (8, WeaponsSu30.FAB_500M62_NV__500kg_Parachute)
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            8,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            8,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            8,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            8,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )

    # ERRR <CLEAN>

    class Pylon9:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            9,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range = (
            9,
            WeaponsSu30.R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            9,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_77__AA_12_Adder_Early____Active_Rdr = (
            9,
            WeaponsSu30.R_77__AA_12_Adder_Early____Active_Rdr,
        )
        R_77_1__AA_12_Adder_B____Active_Rdr = (
            9,
            WeaponsSu30.R_77_1__AA_12_Adder_B____Active_Rdr,
        )
        R_77M__AA_12_Adder_C____Active_Rdr = (
            9,
            WeaponsSu30.R_77M__AA_12_Adder_C____Active_Rdr,
        )
        R_77PD__AA_12_Adder____Active_Rdr_Ramjet = (
            9,
            WeaponsSu30.R_77PD__AA_12_Adder____Active_Rdr_Ramjet,
        )
        R_37M__AA_13_Axehead____Active_Rdr = (
            9,
            WeaponsSu30.R_37M__AA_13_Axehead____Active_Rdr,
        )
        Kh_31P__AS_17_Krypton____600kg = (9, WeaponsSu30.Kh_31P__AS_17_Krypton____600kg)
        Kh_36__AS_23____600kg_Grom_E1 = (9, WeaponsSu30.Kh_36__AS_23____600kg_Grom_E1)
        KH_38MTE__AS_23__IR_Guided = (9, WeaponsSu30.KH_38MTE__AS_23__IR_Guided)
        KH_38MLE__AS_23___Semi_Act_Laser = (
            9,
            WeaponsSu30.KH_38MLE__AS_23___Semi_Act_Laser,
        )
        Kh_38MAE__AS_23____500kg = (9, WeaponsSu30.Kh_38MAE__AS_23____500kg)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            9,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            9,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            9,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_59M__AS_18_Kazoo___930kg = (9, WeaponsSu30.Kh_59M__AS_18_Kazoo___930kg)
        Kh_59MK__AS_18_Kazoo____930kg = (9, WeaponsSu30.Kh_59MK__AS_18_Kazoo____930kg)
        Kh_31A__AS_17_Krypton____610kg = (9, WeaponsSu30.Kh_31A__AS_17_Krypton____610kg)
        Kh_35__AS_20_Kayak____520kg = (9, WeaponsSu30.Kh_35__AS_20_Kayak____520kg)
        Kh_35UE__AS_20_Kayak____520kg = (9, WeaponsSu30.Kh_35UE__AS_20_Kayak____520kg)
        Kh_31AD__AS_17_Krypton____610kg = (
            9,
            WeaponsSu30.Kh_31AD__AS_17_Krypton____610kg,
        )
        Kh_31PD__AS_17_Krypton____600kg = (
            9,
            WeaponsSu30.Kh_31PD__AS_17_Krypton____600kg,
        )
        Kh_59MK2__AS_22_Kazoo____700kg = (9, WeaponsSu30.Kh_59MK2__AS_22_Kazoo____700kg)
        KAB_500Kr___500kg_TV_Guided_Bomb = (9, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (9, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_1500Kr___1500kg = (9, WeaponsSu30.KAB_1500Kr___1500kg)
        KAB_1500LG_PR___1500kg = (9, WeaponsSu30.KAB_1500LG_PR___1500kg)
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            9,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            9,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            9,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            9,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            9,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (9, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            9,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            9,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            9,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M54___474kg__freefall = (9, WeaponsSu30.FAB_500_M54___474kg__freefall)
        FAB_500_M62___474kg__freefall = (9, WeaponsSu30.FAB_500_M62___474kg__freefall)
        FAB_500M62_UMPK__500kg_Glide_Bomb = (
            9,
            WeaponsSu30.FAB_500M62_UMPK__500kg_Glide_Bomb,
        )
        # ERRR {DIS_UMPK_FAB_5002}
        FAB_250_M62___227kg__freefall = (9, WeaponsSu30.FAB_250_M62___227kg__freefall)
        FAB_500M62_NV__500kg_Parachute = (9, WeaponsSu30.FAB_500M62_NV__500kg_Parachute)
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            9,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            9,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            9,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD = (
            9,
            Weapons.MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            9,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )

    # ERRR <CLEAN>

    class Pylon10:
        R_73__AA_11_Archer____Infra_Red = (10, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            10,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            10,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            10,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            10,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27T1__AA_10_Alamo_B____Infra_Red = (
            10,
            WeaponsSu30.R_27T1__AA_10_Alamo_B____Infra_Red,
        )
        R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range = (
            10,
            WeaponsSu30.R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            10,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_27ET1__AA_10_Alamo_D____IR_Extended_Range = (
            10,
            WeaponsSu30.R_27ET1__AA_10_Alamo_D____IR_Extended_Range,
        )
        R_27EP1__AA_10_Alamo_F____Passive_Rdr_Extended_Range = (
            10,
            WeaponsSu30.R_27EP1__AA_10_Alamo_F____Passive_Rdr_Extended_Range,
        )
        R_27P1__AA_10_Alamo_E____Passive_Rdr = (
            10,
            WeaponsSu30.R_27P1__AA_10_Alamo_E____Passive_Rdr,
        )
        R_77__AA_12_Adder_Early____Active_Rdr = (
            10,
            WeaponsSu30.R_77__AA_12_Adder_Early____Active_Rdr,
        )
        R_77_1__AA_12_Adder_B____Active_Rdr = (
            10,
            WeaponsSu30.R_77_1__AA_12_Adder_B____Active_Rdr,
        )
        R_77M__AA_12_Adder_C____Active_Rdr = (
            10,
            WeaponsSu30.R_77M__AA_12_Adder_C____Active_Rdr,
        )
        R_77PD__AA_12_Adder____Active_Rdr_Ramjet = (
            10,
            WeaponsSu30.R_77PD__AA_12_Adder____Active_Rdr_Ramjet,
        )
        R_37M__AA_13_Axehead____Active_Rdr = (
            10,
            WeaponsSu30.R_37M__AA_13_Axehead____Active_Rdr,
        )
        Kh_31P__AS_17_Krypton____600kg = (
            10,
            WeaponsSu30.Kh_31P__AS_17_Krypton____600kg,
        )
        Kh_36__AS_23____600kg_Grom_E1 = (10, WeaponsSu30.Kh_36__AS_23____600kg_Grom_E1)
        KH_38MTE__AS_23__IR_Guided = (10, WeaponsSu30.KH_38MTE__AS_23__IR_Guided)
        KH_38MLE__AS_23___Semi_Act_Laser = (
            10,
            WeaponsSu30.KH_38MLE__AS_23___Semi_Act_Laser,
        )
        Kh_38MAE__AS_23____500kg = (10, WeaponsSu30.Kh_38MAE__AS_23____500kg)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            10,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            10,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            10,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        # ERRR {JAS39_AGM_65H}
        Kh_59M__AS_18_Kazoo___930kg = (10, WeaponsSu30.Kh_59M__AS_18_Kazoo___930kg)
        Kh_59MK__AS_18_Kazoo____930kg = (10, WeaponsSu30.Kh_59MK__AS_18_Kazoo____930kg)
        Kh_31A__AS_17_Krypton____610kg = (
            10,
            WeaponsSu30.Kh_31A__AS_17_Krypton____610kg,
        )
        Kh_35__AS_20_Kayak____520kg = (10, WeaponsSu30.Kh_35__AS_20_Kayak____520kg)
        Kh_35UE__AS_20_Kayak____520kg = (10, WeaponsSu30.Kh_35UE__AS_20_Kayak____520kg)
        Kh_31AD__AS_17_Krypton____610kg = (
            10,
            WeaponsSu30.Kh_31AD__AS_17_Krypton____610kg,
        )
        Kh_31PD__AS_17_Krypton____600kg = (
            10,
            WeaponsSu30.Kh_31PD__AS_17_Krypton____600kg,
        )
        Kh_59MK2__AS_22_Kazoo____700kg = (
            10,
            WeaponsSu30.Kh_59MK2__AS_22_Kazoo____700kg,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (
            10,
            Weapons.KAB_500Kr___500kg_TV_Guided_Bomb,
        )
        KAB_500S___500kg__GPS_Guided = (10, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            10,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            10,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            10,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            10,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (10, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            10,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            10,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            10,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M54___474kg__freefall = (10, WeaponsSu30.FAB_500_M54___474kg__freefall)
        FAB_500_M62___474kg__freefall = (10, WeaponsSu30.FAB_500_M62___474kg__freefall)
        FAB_500M62_UMPK__500kg_Glide_Bomb = (
            10,
            WeaponsSu30.FAB_500M62_UMPK__500kg_Glide_Bomb,
        )
        FAB_250_M62___227kg__freefall = (10, WeaponsSu30.FAB_250_M62___227kg__freefall)
        FAB_500M62_NV__500kg_Parachute = (
            10,
            WeaponsSu30.FAB_500M62_NV__500kg_Parachute,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            10,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            10,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            10,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD = (
            10,
            Weapons.MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            10,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )
        _2_x_B_13L_pods___10_x_S_13_OF__122mm_UnGd_Rkts__Blast_Frag = (
            10,
            Weapons._2_x_B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            10,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange = (
            10,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8OFP2_MPP = (
            10,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8OFP2_MPP,
        )
        _2_x_S_25 = (10, Weapons._2_x_S_25)

    # ERRR <CLEAN>

    class Pylon11:
        R_73__AA_11_Archer____Infra_Red = (11, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            11,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            11,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            11,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        R_77__AA_12_Adder_Early____Active_Rdr = (
            11,
            WeaponsSu30.R_77__AA_12_Adder_Early____Active_Rdr,
        )
        R_77_1__AA_12_Adder_B____Active_Rdr = (
            11,
            WeaponsSu30.R_77_1__AA_12_Adder_B____Active_Rdr,
        )
        R_77M__AA_12_Adder_C____Active_Rdr = (
            11,
            WeaponsSu30.R_77M__AA_12_Adder_C____Active_Rdr,
        )
        Smoke_Generator___red = (11, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (11, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (11, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (11, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (11, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (11, Weapons.Smoke_Generator___orange)
        Smoke_Generator___Black = (11, WeaponsSu30.Smoke_Generator___Black)

    # ERRR <CLEAN>

    class Pylon12:
        R_73__AA_11_Archer____Infra_Red = (12, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            12,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            12,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            12,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        L005_Sorbtsiya_ECM_pod__right_ = (12, Weapons.L005_Sorbtsiya_ECM_pod__right_)
        SAP_518_ECM_Pod__Right_ = (12, WeaponsSu30.SAP_518_ECM_Pod__Right_)
        Smoke_Generator___red = (12, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (12, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (12, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (12, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (12, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (12, Weapons.Smoke_Generator___orange)
        Smoke_Generator___Black = (12, WeaponsSu30.Smoke_Generator___Black)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}

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


@planemod
class Su_30MKA(PlaneType):
    id = "Su-30MKA"
    flyable = True
    height = 5.932
    width = 14.7
    length = 21.935
    fuel_max = 9500
    max_speed = 2499.984
    chaff = 96
    flare = 96
    charge_total = 192
    chaff_charge_size = 1
    flare_charge_size = 1
    eplrs = True
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}

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
                1: 117,
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

    property_defaults: Dict[str, Any] = {
        "SoloFlight": False,
        "NetCrewControlPriority": 0,
        "HumanOrchestra": False,
        "HelmetMountedDevice": 1,
        "ShowLadders": True,
        "su30Chaff": 96,
        "su30Flare": 96,
    }

    class Properties:
        class SoloFlight:
            id = "SoloFlight"

        class NetCrewControlPriority:
            id = "NetCrewControlPriority"

            class Values:
                Pilot = 0
                WSO = 1
                Ask_Always = -1
                Equally_Responsible = -2

        class HumanOrchestra:
            id = "HumanOrchestra"

        class HelmetMountedDevice:
            id = "HelmetMountedDevice"

            class Values:
                Not_installed = 0
                SURA_Visor = 1
                NVG = 2

        class ShowLadders:
            id = "ShowLadders"

        class su30Chaff:
            id = "su30Chaff"

        class su30Flare:
            id = "su30Flare"

    properties = {
        "SoloFlight": UnitPropertyDescription(
            identifier="SoloFlight",
            control="checkbox",
            label="Solo Flight",
            player_only=True,
            default=False,
            weight_when_on=-80,
        ),
        "NetCrewControlPriority": UnitPropertyDescription(
            identifier="NetCrewControlPriority",
            control="comboList",
            label="Aircraft Control Priority",
            player_only=True,
            default=0,
            w_ctrl=150,
            values={
                0: "Pilot",
                1: "WSO",
                -1: "Ask Always",
                -2: "Equally Responsible",
            },
        ),
        "HumanOrchestra": UnitPropertyDescription(
            identifier="HumanOrchestra",
            control="checkbox",
            label="Disable Multicrew",
            player_only=True,
            default=False,
        ),
        "HelmetMountedDevice": UnitPropertyDescription(
            identifier="HelmetMountedDevice",
            control="comboList",
            label="Helmet Mounted Device",
            player_only=True,
            default=1,
            w_ctrl=150,
            values={
                0: "Not installed",
                1: "SURA Visor",
                2: "NVG",
            },
        ),
        "ShowLadders": UnitPropertyDescription(
            identifier="ShowLadders",
            control="checkbox",
            label="Show Ladders",
            default=True,
        ),
        "su30Chaff": UnitPropertyDescription(
            identifier="su30Chaff",
            control="spinbox",
            label="Chaff",
            player_only=True,
            minimum=0,
            maximum=192,
            default=96,
            dimension=" ",
        ),
        "su30Flare": UnitPropertyDescription(
            identifier="su30Flare",
            control="spinbox",
            label="Flare",
            player_only=True,
            minimum=0,
            maximum=192,
            default=96,
            dimension=" ",
        ),
    }

    livery_name = "SU-30MKA"  # from type

    class Pylon1:
        R_73__AA_11_Archer____Infra_Red = (1, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            1,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            1,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            1,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        L005_Sorbtsiya_ECM_pod__left_ = (1, Weapons.L005_Sorbtsiya_ECM_pod__left_)
        SAP_518_ECM_Pod__Left_ = (1, WeaponsSu30.SAP_518_ECM_Pod__Left_)
        Smoke_Generator___red = (1, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (1, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (1, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (1, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (1, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (1, Weapons.Smoke_Generator___orange)

    class Pylon2:
        R_73__AA_11_Archer____Infra_Red = (2, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            2,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            2,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            2,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            2,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            2,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Smoke_Generator___red = (2, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (2, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (2, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (2, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (2, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (2, Weapons.Smoke_Generator___orange)

    # ERRR <CLEAN>

    class Pylon3:
        R_73__AA_11_Archer____Infra_Red = (3, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            3,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            3,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            3,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            3,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27T1__AA_10_Alamo_B____Infra_Red = (
            3,
            WeaponsSu30.R_27T1__AA_10_Alamo_B____Infra_Red,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            3,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_27ET1__AA_10_Alamo_D____IR_Extended_Range = (
            3,
            WeaponsSu30.R_27ET1__AA_10_Alamo_D____IR_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            3,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            3,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            3,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        Kh_31P__AS_17_Krypton____600kg = (3, WeaponsSu30.Kh_31P__AS_17_Krypton____600kg)
        Kh_36__AS_23____600kg_Grom_E1 = (3, WeaponsSu30.Kh_36__AS_23____600kg_Grom_E1)
        KH_38MTE__AS_23__IR_Guided = (3, WeaponsSu30.KH_38MTE__AS_23__IR_Guided)
        KH_38MLE__AS_23___Semi_Act_Laser = (
            3,
            WeaponsSu30.KH_38MLE__AS_23___Semi_Act_Laser,
        )
        Kh_38MAE__AS_23____500kg = (3, WeaponsSu30.Kh_38MAE__AS_23____500kg)
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            3,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            3,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_59M__AS_18_Kazoo___930kg = (3, WeaponsSu30.Kh_59M__AS_18_Kazoo___930kg)
        Kh_59MK__AS_18_Kazoo____930kg = (3, WeaponsSu30.Kh_59MK__AS_18_Kazoo____930kg)
        Kh_31A__AS_17_Krypton____610kg = (3, WeaponsSu30.Kh_31A__AS_17_Krypton____610kg)
        Kh_35__AS_20_Kayak____520kg = (3, WeaponsSu30.Kh_35__AS_20_Kayak____520kg)
        Kh_35UE__AS_20_Kayak____520kg = (3, WeaponsSu30.Kh_35UE__AS_20_Kayak____520kg)
        Kh_31AD__AS_17_Krypton____610kg = (
            3,
            WeaponsSu30.Kh_31AD__AS_17_Krypton____610kg,
        )
        Kh_31PD__AS_17_Krypton____600kg = (
            3,
            WeaponsSu30.Kh_31PD__AS_17_Krypton____600kg,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (3, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (3, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            3,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            3,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            3,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            3,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (3, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            3,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            3,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            3,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            3,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        FAB_500_M54___474kg__freefall = (3, WeaponsSu30.FAB_500_M54___474kg__freefall)
        FAB_500_M62___474kg__freefall = (3, WeaponsSu30.FAB_500_M62___474kg__freefall)
        FAB_250_M62___227kg__freefall = (3, WeaponsSu30.FAB_250_M62___227kg__freefall)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            3,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            3,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )
        _2_x_B_13L_pods___10_x_S_13_OF__122mm_UnGd_Rkts__Blast_Frag = (
            3,
            Weapons._2_x_B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            3,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange = (
            3,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8OFP2_MPP = (
            3,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8OFP2_MPP,
        )
        _2_x_S_25 = (3, Weapons._2_x_S_25)

    # ERRR <CLEAN>

    class Pylon4:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            4,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            4,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            4,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            4,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Kh_31P__AS_17_Krypton____600kg = (4, WeaponsSu30.Kh_31P__AS_17_Krypton____600kg)
        Kh_36__AS_23____600kg_Grom_E1 = (4, WeaponsSu30.Kh_36__AS_23____600kg_Grom_E1)
        KH_38MTE__AS_23__IR_Guided = (4, WeaponsSu30.KH_38MTE__AS_23__IR_Guided)
        KH_38MLE__AS_23___Semi_Act_Laser = (
            4,
            WeaponsSu30.KH_38MLE__AS_23___Semi_Act_Laser,
        )
        Kh_38MAE__AS_23____500kg = (4, WeaponsSu30.Kh_38MAE__AS_23____500kg)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            4,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            4,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            4,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_59M__AS_18_Kazoo___930kg = (4, WeaponsSu30.Kh_59M__AS_18_Kazoo___930kg)
        Kh_59MK__AS_18_Kazoo____930kg = (4, WeaponsSu30.Kh_59MK__AS_18_Kazoo____930kg)
        Kh_31A__AS_17_Krypton____610kg = (4, WeaponsSu30.Kh_31A__AS_17_Krypton____610kg)
        Kh_35__AS_20_Kayak____520kg = (4, WeaponsSu30.Kh_35__AS_20_Kayak____520kg)
        Kh_35UE__AS_20_Kayak____520kg = (4, WeaponsSu30.Kh_35UE__AS_20_Kayak____520kg)
        Kh_31AD__AS_17_Krypton____610kg = (
            4,
            WeaponsSu30.Kh_31AD__AS_17_Krypton____610kg,
        )
        Kh_31PD__AS_17_Krypton____600kg = (
            4,
            WeaponsSu30.Kh_31PD__AS_17_Krypton____600kg,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (4, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (4, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_1500Kr___1500kg = (4, WeaponsSu30.KAB_1500Kr___1500kg)
        KAB_1500LG_PR___1500kg = (4, WeaponsSu30.KAB_1500LG_PR___1500kg)
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            4,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            4,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            4,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            4,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            4,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (4, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            4,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            4,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            4,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            4,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        FAB_500_M54___474kg__freefall = (4, WeaponsSu30.FAB_500_M54___474kg__freefall)
        FAB_500_M62___474kg__freefall = (4, WeaponsSu30.FAB_500_M62___474kg__freefall)
        FAB_250_M62___227kg__freefall = (4, WeaponsSu30.FAB_250_M62___227kg__freefall)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            4,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            4,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )

    # ERRR <CLEAN>

    class Pylon5:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            5,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            5,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            5,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            5,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Kh_31P__AS_17_Krypton____600kg = (5, WeaponsSu30.Kh_31P__AS_17_Krypton____600kg)
        Kh_36__AS_23____600kg_Grom_E1 = (5, WeaponsSu30.Kh_36__AS_23____600kg_Grom_E1)
        KH_38MTE__AS_23__IR_Guided = (5, WeaponsSu30.KH_38MTE__AS_23__IR_Guided)
        KH_38MLE__AS_23___Semi_Act_Laser = (
            5,
            WeaponsSu30.KH_38MLE__AS_23___Semi_Act_Laser,
        )
        Kh_38MAE__AS_23____500kg = (5, WeaponsSu30.Kh_38MAE__AS_23____500kg)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            5,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            5,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            5,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_31A__AS_17_Krypton____610kg = (5, WeaponsSu30.Kh_31A__AS_17_Krypton____610kg)
        Kh_31AD__AS_17_Krypton____610kg = (
            5,
            WeaponsSu30.Kh_31AD__AS_17_Krypton____610kg,
        )
        Kh_31PD__AS_17_Krypton____600kg = (
            5,
            WeaponsSu30.Kh_31PD__AS_17_Krypton____600kg,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (5, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (5, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            5,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            5,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        P_50T___50kg_Practice_Bomb_LD = (5, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            5,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            5,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            5,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            5,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        FAB_500_M54___474kg__freefall = (5, WeaponsSu30.FAB_500_M54___474kg__freefall)
        FAB_500_M62___474kg__freefall = (5, WeaponsSu30.FAB_500_M62___474kg__freefall)
        FAB_250_M62___227kg__freefall = (5, WeaponsSu30.FAB_250_M62___227kg__freefall)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            5,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            5,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )
        APK_9_POD = (5, WeaponsSu30.APK_9_POD)
        L_081_Fantasmagoria_ELINT_pod = (5, Weapons.L_081_Fantasmagoria_ELINT_pod)

    # ERRR <CLEAN>

    class Pylon6:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            6,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            6,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            6,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            6,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (6, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (6, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_1500Kr___1500kg = (6, WeaponsSu30.KAB_1500Kr___1500kg)
        KAB_1500LG_PR___1500kg = (6, WeaponsSu30.KAB_1500LG_PR___1500kg)
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            6,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            6,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            6,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            6,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            6,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        P_50T___50kg_Practice_Bomb_LD = (6, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            6,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            6,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            6,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            6,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        FAB_500_M54___474kg__freefall = (6, WeaponsSu30.FAB_500_M54___474kg__freefall)
        FAB_500_M62___474kg__freefall = (6, WeaponsSu30.FAB_500_M62___474kg__freefall)
        FAB_250_M62___227kg__freefall = (6, WeaponsSu30.FAB_250_M62___227kg__freefall)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            6,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            6,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )
        RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag = (
            6,
            Weapons.RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag,
        )
        RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP = (
            6,
            Weapons.RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP,
        )

    # ERRR <CLEAN>

    class Pylon7:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            7,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            7,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            7,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            7,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (7, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (7, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            7,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            7,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            7,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            7,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (7, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            7,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            7,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            7,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            7,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        FAB_500_M54___474kg__freefall = (7, WeaponsSu30.FAB_500_M54___474kg__freefall)
        FAB_500_M62___474kg__freefall = (7, WeaponsSu30.FAB_500_M62___474kg__freefall)
        FAB_250_M62___227kg__freefall = (7, WeaponsSu30.FAB_250_M62___227kg__freefall)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            7,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            7,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )
        Smoke_Generator___red = (7, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (7, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (7, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (7, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (7, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (7, Weapons.Smoke_Generator___orange)
        RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag = (
            7,
            Weapons.RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag,
        )
        RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP = (
            7,
            Weapons.RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP,
        )

    # ERRR <CLEAN>

    class Pylon8:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            8,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            8,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            8,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            8,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Kh_31P__AS_17_Krypton____600kg = (8, WeaponsSu30.Kh_31P__AS_17_Krypton____600kg)
        Kh_36__AS_23____600kg_Grom_E1 = (8, WeaponsSu30.Kh_36__AS_23____600kg_Grom_E1)
        KH_38MTE__AS_23__IR_Guided = (8, WeaponsSu30.KH_38MTE__AS_23__IR_Guided)
        KH_38MLE__AS_23___Semi_Act_Laser = (
            8,
            WeaponsSu30.KH_38MLE__AS_23___Semi_Act_Laser,
        )
        Kh_38MAE__AS_23____500kg = (8, WeaponsSu30.Kh_38MAE__AS_23____500kg)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            8,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            8,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            8,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_31A__AS_17_Krypton____610kg = (8, WeaponsSu30.Kh_31A__AS_17_Krypton____610kg)
        Kh_31AD__AS_17_Krypton____610kg = (
            8,
            WeaponsSu30.Kh_31AD__AS_17_Krypton____610kg,
        )
        Kh_31PD__AS_17_Krypton____600kg = (
            8,
            WeaponsSu30.Kh_31PD__AS_17_Krypton____600kg,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (8, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (8, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            8,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            8,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        P_50T___50kg_Practice_Bomb_LD = (8, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            8,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            8,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            8,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            8,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        FAB_500_M54___474kg__freefall = (8, WeaponsSu30.FAB_500_M54___474kg__freefall)
        FAB_500_M62___474kg__freefall = (8, WeaponsSu30.FAB_500_M62___474kg__freefall)
        FAB_250_M62___227kg__freefall = (8, WeaponsSu30.FAB_250_M62___227kg__freefall)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            8,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            8,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )

    # ERRR <CLEAN>

    class Pylon9:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            9,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            9,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            9,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            9,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Kh_31P__AS_17_Krypton____600kg = (9, WeaponsSu30.Kh_31P__AS_17_Krypton____600kg)
        Kh_36__AS_23____600kg_Grom_E1 = (9, WeaponsSu30.Kh_36__AS_23____600kg_Grom_E1)
        KH_38MTE__AS_23__IR_Guided = (9, WeaponsSu30.KH_38MTE__AS_23__IR_Guided)
        KH_38MLE__AS_23___Semi_Act_Laser = (
            9,
            WeaponsSu30.KH_38MLE__AS_23___Semi_Act_Laser,
        )
        Kh_38MAE__AS_23____500kg = (9, WeaponsSu30.Kh_38MAE__AS_23____500kg)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            9,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            9,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            9,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_59M__AS_18_Kazoo___930kg = (9, WeaponsSu30.Kh_59M__AS_18_Kazoo___930kg)
        Kh_59MK__AS_18_Kazoo____930kg = (9, WeaponsSu30.Kh_59MK__AS_18_Kazoo____930kg)
        Kh_31A__AS_17_Krypton____610kg = (9, WeaponsSu30.Kh_31A__AS_17_Krypton____610kg)
        Kh_35__AS_20_Kayak____520kg = (9, WeaponsSu30.Kh_35__AS_20_Kayak____520kg)
        Kh_35UE__AS_20_Kayak____520kg = (9, WeaponsSu30.Kh_35UE__AS_20_Kayak____520kg)
        Kh_31AD__AS_17_Krypton____610kg = (
            9,
            WeaponsSu30.Kh_31AD__AS_17_Krypton____610kg,
        )
        Kh_31PD__AS_17_Krypton____600kg = (
            9,
            WeaponsSu30.Kh_31PD__AS_17_Krypton____600kg,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (9, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (9, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_1500Kr___1500kg = (9, WeaponsSu30.KAB_1500Kr___1500kg)
        KAB_1500LG_PR___1500kg = (9, WeaponsSu30.KAB_1500LG_PR___1500kg)
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            9,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            9,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            9,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            9,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            9,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (9, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            9,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            9,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            9,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            9,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        FAB_500_M54___474kg__freefall = (9, WeaponsSu30.FAB_500_M54___474kg__freefall)
        FAB_500_M62___474kg__freefall = (9, WeaponsSu30.FAB_500_M62___474kg__freefall)
        FAB_250_M62___227kg__freefall = (9, WeaponsSu30.FAB_250_M62___227kg__freefall)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            9,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            9,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )

    # ERRR <CLEAN>

    class Pylon10:
        R_73__AA_11_Archer____Infra_Red = (10, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            10,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            10,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            10,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            10,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27T1__AA_10_Alamo_B____Infra_Red = (
            10,
            WeaponsSu30.R_27T1__AA_10_Alamo_B____Infra_Red,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            10,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_27ET1__AA_10_Alamo_D____IR_Extended_Range = (
            10,
            WeaponsSu30.R_27ET1__AA_10_Alamo_D____IR_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            10,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            10,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Kh_31P__AS_17_Krypton____600kg = (
            10,
            WeaponsSu30.Kh_31P__AS_17_Krypton____600kg,
        )
        Kh_36__AS_23____600kg_Grom_E1 = (10, WeaponsSu30.Kh_36__AS_23____600kg_Grom_E1)
        KH_38MTE__AS_23__IR_Guided = (10, WeaponsSu30.KH_38MTE__AS_23__IR_Guided)
        KH_38MLE__AS_23___Semi_Act_Laser = (
            10,
            WeaponsSu30.KH_38MLE__AS_23___Semi_Act_Laser,
        )
        Kh_38MAE__AS_23____500kg = (10, WeaponsSu30.Kh_38MAE__AS_23____500kg)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            10,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            10,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            10,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_59M__AS_18_Kazoo___930kg = (10, WeaponsSu30.Kh_59M__AS_18_Kazoo___930kg)
        Kh_59MK__AS_18_Kazoo____930kg = (10, WeaponsSu30.Kh_59MK__AS_18_Kazoo____930kg)
        Kh_31A__AS_17_Krypton____610kg = (
            10,
            WeaponsSu30.Kh_31A__AS_17_Krypton____610kg,
        )
        Kh_35__AS_20_Kayak____520kg = (10, WeaponsSu30.Kh_35__AS_20_Kayak____520kg)
        Kh_35UE__AS_20_Kayak____520kg = (10, WeaponsSu30.Kh_35UE__AS_20_Kayak____520kg)
        Kh_31AD__AS_17_Krypton____610kg = (
            10,
            WeaponsSu30.Kh_31AD__AS_17_Krypton____610kg,
        )
        Kh_31PD__AS_17_Krypton____600kg = (
            10,
            WeaponsSu30.Kh_31PD__AS_17_Krypton____600kg,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (
            10,
            Weapons.KAB_500Kr___500kg_TV_Guided_Bomb,
        )
        KAB_500S___500kg__GPS_Guided = (10, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            10,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            10,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            10,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            10,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (10, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            10,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            10,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            10,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            10,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        FAB_500_M54___474kg__freefall = (10, WeaponsSu30.FAB_500_M54___474kg__freefall)
        FAB_500_M62___474kg__freefall = (10, WeaponsSu30.FAB_500_M62___474kg__freefall)
        FAB_250_M62___227kg__freefall = (10, WeaponsSu30.FAB_250_M62___227kg__freefall)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            10,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            10,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )
        _2_x_B_13L_pods___10_x_S_13_OF__122mm_UnGd_Rkts__Blast_Frag = (
            10,
            Weapons._2_x_B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            10,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange = (
            10,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8OFP2_MPP = (
            10,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8OFP2_MPP,
        )
        _2_x_S_25 = (10, Weapons._2_x_S_25)

    # ERRR <CLEAN>

    class Pylon11:
        R_73__AA_11_Archer____Infra_Red = (11, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            11,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            11,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            11,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            11,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            11,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Smoke_Generator___red = (11, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (11, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (11, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (11, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (11, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (11, Weapons.Smoke_Generator___orange)

    # ERRR <CLEAN>

    class Pylon12:
        R_73__AA_11_Archer____Infra_Red = (12, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            12,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            12,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            12,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        L005_Sorbtsiya_ECM_pod__right_ = (12, Weapons.L005_Sorbtsiya_ECM_pod__right_)
        SAP_518_ECM_Pod__Right_ = (12, WeaponsSu30.SAP_518_ECM_Pod__Right_)
        Smoke_Generator___red = (12, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (12, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (12, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (12, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (12, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (12, Weapons.Smoke_Generator___orange)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}

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


@planemod
class Su_30MKM(PlaneType):
    id = "Su-30MKM"
    flyable = True
    height = 5.932
    width = 14.7
    length = 21.935
    fuel_max = 9500
    max_speed = 2499.984
    chaff = 96
    flare = 96
    charge_total = 192
    chaff_charge_size = 1
    flare_charge_size = 1
    eplrs = True
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}

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
                1: 117,
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

    property_defaults: Dict[str, Any] = {
        "SoloFlight": False,
        "NetCrewControlPriority": 0,
        "HumanOrchestra": False,
        "HelmetMountedDevice": 1,
        "ShowLadders": True,
        "su30Chaff": 96,
        "su30Flare": 96,
    }

    class Properties:
        class SoloFlight:
            id = "SoloFlight"

        class NetCrewControlPriority:
            id = "NetCrewControlPriority"

            class Values:
                Pilot = 0
                WSO = 1
                Ask_Always = -1
                Equally_Responsible = -2

        class HumanOrchestra:
            id = "HumanOrchestra"

        class HelmetMountedDevice:
            id = "HelmetMountedDevice"

            class Values:
                Not_installed = 0
                SURA_Visor = 1
                NVG = 2

        class ShowLadders:
            id = "ShowLadders"

        class su30Chaff:
            id = "su30Chaff"

        class su30Flare:
            id = "su30Flare"

    properties = {
        "SoloFlight": UnitPropertyDescription(
            identifier="SoloFlight",
            control="checkbox",
            label="Solo Flight",
            player_only=True,
            default=False,
            weight_when_on=-80,
        ),
        "NetCrewControlPriority": UnitPropertyDescription(
            identifier="NetCrewControlPriority",
            control="comboList",
            label="Aircraft Control Priority",
            player_only=True,
            default=0,
            w_ctrl=150,
            values={
                0: "Pilot",
                1: "WSO",
                -1: "Ask Always",
                -2: "Equally Responsible",
            },
        ),
        "HumanOrchestra": UnitPropertyDescription(
            identifier="HumanOrchestra",
            control="checkbox",
            label="Disable Multicrew",
            player_only=True,
            default=False,
        ),
        "HelmetMountedDevice": UnitPropertyDescription(
            identifier="HelmetMountedDevice",
            control="comboList",
            label="Helmet Mounted Device",
            player_only=True,
            default=1,
            w_ctrl=150,
            values={
                0: "Not installed",
                1: "SURA Visor",
                2: "NVG",
            },
        ),
        "ShowLadders": UnitPropertyDescription(
            identifier="ShowLadders",
            control="checkbox",
            label="Show Ladders",
            default=True,
        ),
        "su30Chaff": UnitPropertyDescription(
            identifier="su30Chaff",
            control="spinbox",
            label="Chaff",
            player_only=True,
            minimum=0,
            maximum=192,
            default=96,
            dimension=" ",
        ),
        "su30Flare": UnitPropertyDescription(
            identifier="su30Flare",
            control="spinbox",
            label="Flare",
            player_only=True,
            minimum=0,
            maximum=192,
            default=96,
            dimension=" ",
        ),
    }

    livery_name = "SU-30MKM"  # from type

    class Pylon1:
        R_73__AA_11_Archer____Infra_Red = (1, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            1,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            1,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            1,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        L005_Sorbtsiya_ECM_pod__left_ = (1, Weapons.L005_Sorbtsiya_ECM_pod__left_)
        SAP_518_ECM_Pod__Left_ = (1, WeaponsSu30.SAP_518_ECM_Pod__Left_)
        Smoke_Generator___red = (1, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (1, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (1, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (1, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (1, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (1, Weapons.Smoke_Generator___orange)

    class Pylon2:
        R_73__AA_11_Archer____Infra_Red = (2, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            2,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            2,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            2,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            2,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            2,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Smoke_Generator___red = (2, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (2, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (2, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (2, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (2, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (2, Weapons.Smoke_Generator___orange)

    # ERRR <CLEAN>

    class Pylon3:
        R_73__AA_11_Archer____Infra_Red = (3, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            3,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            3,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            3,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            3,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27T1__AA_10_Alamo_B____Infra_Red = (
            3,
            WeaponsSu30.R_27T1__AA_10_Alamo_B____Infra_Red,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            3,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_27ET1__AA_10_Alamo_D____IR_Extended_Range = (
            3,
            WeaponsSu30.R_27ET1__AA_10_Alamo_D____IR_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            3,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            3,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Kh_31P__AS_17_Krypton____600kg = (3, WeaponsSu30.Kh_31P__AS_17_Krypton____600kg)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            3,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            3,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            3,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_59M__AS_18_Kazoo___930kg = (3, WeaponsSu30.Kh_59M__AS_18_Kazoo___930kg)
        Kh_59MK__AS_18_Kazoo____930kg = (3, WeaponsSu30.Kh_59MK__AS_18_Kazoo____930kg)
        Kh_31A__AS_17_Krypton____610kg = (3, WeaponsSu30.Kh_31A__AS_17_Krypton____610kg)
        Kh_35__AS_20_Kayak____520kg = (3, WeaponsSu30.Kh_35__AS_20_Kayak____520kg)
        KAB_500Kr___500kg_TV_Guided_Bomb = (3, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (3, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            3,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            3,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            3,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            3,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (3, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            3,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            3,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        FAB_250___250kg_GP_Bomb_LD = (3, Weapons.FAB_250___250kg_GP_Bomb_LD)
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            3,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M_62___500kg_GP_Bomb_LD = (3, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            3,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            3,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD = (
            3,
            Weapons.MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD,
        )
        _2_x_B_13L_pods___10_x_S_13_OF__122mm_UnGd_Rkts__Blast_Frag = (
            3,
            Weapons._2_x_B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            3,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange = (
            3,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8OFP2_MPP = (
            3,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8OFP2_MPP,
        )
        _2_x_S_25 = (3, Weapons._2_x_S_25)
        Mk_82___500lb_GP_Bomb_LD = (3, Weapons.Mk_82___500lb_GP_Bomb_LD)
        GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            WeaponsSu30.GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (3, Weapons.GBU_12___500lb_Laser_Guided_Bomb)

    # ERRR <CLEAN>

    class Pylon4:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            4,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            4,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            4,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            4,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Kh_31P__AS_17_Krypton____600kg = (4, WeaponsSu30.Kh_31P__AS_17_Krypton____600kg)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            4,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            4,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            4,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_59M__AS_18_Kazoo___930kg = (4, WeaponsSu30.Kh_59M__AS_18_Kazoo___930kg)
        Kh_59MK__AS_18_Kazoo____930kg = (4, WeaponsSu30.Kh_59MK__AS_18_Kazoo____930kg)
        Kh_31A__AS_17_Krypton____610kg = (4, WeaponsSu30.Kh_31A__AS_17_Krypton____610kg)
        Kh_35__AS_20_Kayak____520kg = (4, WeaponsSu30.Kh_35__AS_20_Kayak____520kg)
        KAB_500Kr___500kg_TV_Guided_Bomb = (4, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (4, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_1500Kr___1500kg = (4, WeaponsSu30.KAB_1500Kr___1500kg)
        KAB_1500LG_PR___1500kg = (4, WeaponsSu30.KAB_1500LG_PR___1500kg)
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            4,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            4,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            4,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            4,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            4,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (4, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            4,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            4,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        FAB_250___250kg_GP_Bomb_LD = (4, Weapons.FAB_250___250kg_GP_Bomb_LD)
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            4,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M_62___500kg_GP_Bomb_LD = (4, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            4,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            4,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD = (
            4,
            Weapons.MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD,
        )
        # ERRR <CLEAN>
        Mk_82___500lb_GP_Bomb_LD = (4, Weapons.Mk_82___500lb_GP_Bomb_LD)
        GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            4,
            WeaponsSu30.GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (4, Weapons.GBU_12___500lb_Laser_Guided_Bomb)

    class Pylon5:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            5,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            5,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            5,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            5,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Kh_31P__AS_17_Krypton____600kg = (5, WeaponsSu30.Kh_31P__AS_17_Krypton____600kg)
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            5,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            5,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            5,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_31A__AS_17_Krypton____610kg = (5, WeaponsSu30.Kh_31A__AS_17_Krypton____610kg)
        KAB_500Kr___500kg_TV_Guided_Bomb = (5, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (5, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            5,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            5,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        P_50T___50kg_Practice_Bomb_LD = (5, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            5,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            5,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        FAB_250___250kg_GP_Bomb_LD = (5, Weapons.FAB_250___250kg_GP_Bomb_LD)
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            5,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M_62___500kg_GP_Bomb_LD = (5, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            5,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            5,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        APK_9_POD = (5, WeaponsSu30.APK_9_POD)
        # ERRR <CLEAN>
        Mk_82___500lb_GP_Bomb_LD = (5, Weapons.Mk_82___500lb_GP_Bomb_LD)
        GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            5,
            WeaponsSu30.GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (5, Weapons.GBU_12___500lb_Laser_Guided_Bomb)

    class Pylon6:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            6,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            6,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            6,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            6,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (6, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (6, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_1500Kr___1500kg = (6, WeaponsSu30.KAB_1500Kr___1500kg)
        KAB_1500LG_PR___1500kg = (6, WeaponsSu30.KAB_1500LG_PR___1500kg)
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            6,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            6,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            6,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            6,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            6,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (6, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            6,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            6,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        FAB_250___250kg_GP_Bomb_LD = (6, Weapons.FAB_250___250kg_GP_Bomb_LD)
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            6,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M_62___500kg_GP_Bomb_LD = (6, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            6,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            6,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag = (
            6,
            Weapons.RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag,
        )
        RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP = (
            6,
            Weapons.RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP,
        )
        # ERRR <CLEAN>
        Mk_82___500lb_GP_Bomb_LD = (6, Weapons.Mk_82___500lb_GP_Bomb_LD)
        GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            6,
            WeaponsSu30.GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (6, Weapons.GBU_12___500lb_Laser_Guided_Bomb)

    class Pylon7:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            7,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            7,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            7,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            7,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (7, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (7, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            7,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            7,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            7,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            7,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (7, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            7,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            7,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        FAB_250___250kg_GP_Bomb_LD = (7, Weapons.FAB_250___250kg_GP_Bomb_LD)
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            7,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M_62___500kg_GP_Bomb_LD = (7, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            7,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            7,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag = (
            7,
            Weapons.RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag,
        )
        RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP = (
            7,
            Weapons.RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP,
        )
        # ERRR <CLEAN>
        Smoke_Generator___red = (7, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (7, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (7, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (7, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (7, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (7, Weapons.Smoke_Generator___orange)
        Mk_82___500lb_GP_Bomb_LD = (7, Weapons.Mk_82___500lb_GP_Bomb_LD)
        GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsSu30.GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (7, Weapons.GBU_12___500lb_Laser_Guided_Bomb)

    class Pylon8:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            8,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            8,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            8,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            8,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Kh_31P__AS_17_Krypton____600kg = (8, WeaponsSu30.Kh_31P__AS_17_Krypton____600kg)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            8,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            8,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            8,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_31A__AS_17_Krypton____610kg = (8, WeaponsSu30.Kh_31A__AS_17_Krypton____610kg)
        KAB_500Kr___500kg_TV_Guided_Bomb = (8, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (8, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            8,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            8,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        P_50T___50kg_Practice_Bomb_LD = (8, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            8,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            8,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        FAB_250___250kg_GP_Bomb_LD = (8, Weapons.FAB_250___250kg_GP_Bomb_LD)
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            8,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M_62___500kg_GP_Bomb_LD = (8, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            8,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            8,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        # ERRR {DAMOCLES}
        # ERRR <CLEAN>
        Mk_82___500lb_GP_Bomb_LD = (8, Weapons.Mk_82___500lb_GP_Bomb_LD)
        GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            8,
            WeaponsSu30.GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (8, Weapons.GBU_12___500lb_Laser_Guided_Bomb)

    class Pylon9:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            9,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            9,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            9,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            9,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Kh_31P__AS_17_Krypton____600kg = (9, WeaponsSu30.Kh_31P__AS_17_Krypton____600kg)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            9,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            9,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            9,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_59M__AS_18_Kazoo___930kg = (9, WeaponsSu30.Kh_59M__AS_18_Kazoo___930kg)
        Kh_59MK__AS_18_Kazoo____930kg = (9, WeaponsSu30.Kh_59MK__AS_18_Kazoo____930kg)
        Kh_31A__AS_17_Krypton____610kg = (9, WeaponsSu30.Kh_31A__AS_17_Krypton____610kg)
        Kh_35__AS_20_Kayak____520kg = (9, WeaponsSu30.Kh_35__AS_20_Kayak____520kg)
        KAB_500Kr___500kg_TV_Guided_Bomb = (9, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (9, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_1500Kr___1500kg = (9, WeaponsSu30.KAB_1500Kr___1500kg)
        KAB_1500LG_PR___1500kg = (9, WeaponsSu30.KAB_1500LG_PR___1500kg)
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            9,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            9,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            9,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            9,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            9,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (9, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            9,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            9,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        FAB_250___250kg_GP_Bomb_LD = (9, Weapons.FAB_250___250kg_GP_Bomb_LD)
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            9,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M_62___500kg_GP_Bomb_LD = (9, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            9,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            9,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD = (
            9,
            Weapons.MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD,
        )
        # ERRR <CLEAN>
        Mk_82___500lb_GP_Bomb_LD = (9, Weapons.Mk_82___500lb_GP_Bomb_LD)
        GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            9,
            WeaponsSu30.GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (9, Weapons.GBU_12___500lb_Laser_Guided_Bomb)

    class Pylon10:
        R_73__AA_11_Archer____Infra_Red = (10, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            10,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            10,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            10,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            10,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27T1__AA_10_Alamo_B____Infra_Red = (
            10,
            WeaponsSu30.R_27T1__AA_10_Alamo_B____Infra_Red,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            10,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_27ET1__AA_10_Alamo_D____IR_Extended_Range = (
            10,
            WeaponsSu30.R_27ET1__AA_10_Alamo_D____IR_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            10,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            10,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Kh_31P__AS_17_Krypton____600kg = (
            10,
            WeaponsSu30.Kh_31P__AS_17_Krypton____600kg,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            10,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            10,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            10,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_59M__AS_18_Kazoo___930kg = (10, WeaponsSu30.Kh_59M__AS_18_Kazoo___930kg)
        Kh_59MK__AS_18_Kazoo____930kg = (10, WeaponsSu30.Kh_59MK__AS_18_Kazoo____930kg)
        Kh_31A__AS_17_Krypton____610kg = (
            10,
            WeaponsSu30.Kh_31A__AS_17_Krypton____610kg,
        )
        Kh_35__AS_20_Kayak____520kg = (10, WeaponsSu30.Kh_35__AS_20_Kayak____520kg)
        KAB_500Kr___500kg_TV_Guided_Bomb = (
            10,
            Weapons.KAB_500Kr___500kg_TV_Guided_Bomb,
        )
        KAB_500S___500kg__GPS_Guided = (10, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            10,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            10,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            10,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            10,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (10, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            10,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            10,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        FAB_250___250kg_GP_Bomb_LD = (10, Weapons.FAB_250___250kg_GP_Bomb_LD)
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            10,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M_62___500kg_GP_Bomb_LD = (10, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            10,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            10,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD = (
            10,
            Weapons.MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD,
        )
        _2_x_B_13L_pods___10_x_S_13_OF__122mm_UnGd_Rkts__Blast_Frag = (
            10,
            Weapons._2_x_B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            10,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange = (
            10,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8OFP2_MPP = (
            10,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8OFP2_MPP,
        )
        _2_x_S_25 = (10, Weapons._2_x_S_25)
        # ERRR <CLEAN>
        Mk_82___500lb_GP_Bomb_LD = (10, Weapons.Mk_82___500lb_GP_Bomb_LD)
        GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            10,
            WeaponsSu30.GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (
            10,
            Weapons.GBU_12___500lb_Laser_Guided_Bomb,
        )

    class Pylon11:
        R_73__AA_11_Archer____Infra_Red = (11, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            11,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            11,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            11,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            11,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            11,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Smoke_Generator___red = (11, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (11, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (11, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (11, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (11, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (11, Weapons.Smoke_Generator___orange)

    # ERRR <CLEAN>

    class Pylon12:
        R_73__AA_11_Archer____Infra_Red = (12, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            12,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            12,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            12,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        L005_Sorbtsiya_ECM_pod__right_ = (12, Weapons.L005_Sorbtsiya_ECM_pod__right_)
        SAP_518_ECM_Pod__Right_ = (12, WeaponsSu30.SAP_518_ECM_Pod__Right_)
        Smoke_Generator___red = (12, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (12, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (12, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (12, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (12, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (12, Weapons.Smoke_Generator___orange)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}

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


@planemod
class Su_30MKM_AG(PlaneType):
    id = "Su-30MKM-AG"
    flyable = True
    height = 5.932
    width = 14.7
    length = 21.935
    fuel_max = 9500
    max_speed = 2499.984
    chaff = 96
    flare = 96
    charge_total = 192
    chaff_charge_size = 1
    flare_charge_size = 1
    eplrs = True
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}

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
                1: 117,
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

    property_defaults: Dict[str, Any] = {
        "SoloFlight": False,
        "NetCrewControlPriority": 0,
        "HumanOrchestra": False,
        "HelmetMountedDevice": 1,
        "ShowLadders": True,
        "su30Chaff": 96,
        "su30Flare": 96,
    }

    class Properties:
        class SoloFlight:
            id = "SoloFlight"

        class NetCrewControlPriority:
            id = "NetCrewControlPriority"

            class Values:
                Pilot = 0
                WSO = 1
                Ask_Always = -1
                Equally_Responsible = -2

        class HumanOrchestra:
            id = "HumanOrchestra"

        class HelmetMountedDevice:
            id = "HelmetMountedDevice"

            class Values:
                Not_installed = 0
                SURA_Visor = 1
                NVG = 2

        class ShowLadders:
            id = "ShowLadders"

        class su30Chaff:
            id = "su30Chaff"

        class su30Flare:
            id = "su30Flare"

    properties = {
        "SoloFlight": UnitPropertyDescription(
            identifier="SoloFlight",
            control="checkbox",
            label="Solo Flight",
            player_only=True,
            default=False,
            weight_when_on=-80,
        ),
        "NetCrewControlPriority": UnitPropertyDescription(
            identifier="NetCrewControlPriority",
            control="comboList",
            label="Aircraft Control Priority",
            player_only=True,
            default=0,
            w_ctrl=150,
            values={
                0: "Pilot",
                1: "WSO",
                -1: "Ask Always",
                -2: "Equally Responsible",
            },
        ),
        "HumanOrchestra": UnitPropertyDescription(
            identifier="HumanOrchestra",
            control="checkbox",
            label="Disable Multicrew",
            player_only=True,
            default=False,
        ),
        "HelmetMountedDevice": UnitPropertyDescription(
            identifier="HelmetMountedDevice",
            control="comboList",
            label="Helmet Mounted Device",
            player_only=True,
            default=1,
            w_ctrl=150,
            values={
                0: "Not installed",
                1: "SURA Visor",
                2: "NVG",
            },
        ),
        "ShowLadders": UnitPropertyDescription(
            identifier="ShowLadders",
            control="checkbox",
            label="Show Ladders",
            default=True,
        ),
        "su30Chaff": UnitPropertyDescription(
            identifier="su30Chaff",
            control="spinbox",
            label="Chaff",
            player_only=True,
            minimum=0,
            maximum=192,
            default=96,
            dimension=" ",
        ),
        "su30Flare": UnitPropertyDescription(
            identifier="su30Flare",
            control="spinbox",
            label="Flare",
            player_only=True,
            minimum=0,
            maximum=192,
            default=96,
            dimension=" ",
        ),
    }

    livery_name = "SU-30MKM-AG"  # from type

    class Pylon1:
        R_73__AA_11_Archer____Infra_Red = (1, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            1,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            1,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            1,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        L005_Sorbtsiya_ECM_pod__left_ = (1, Weapons.L005_Sorbtsiya_ECM_pod__left_)
        SAP_518_ECM_Pod__Left_ = (1, WeaponsSu30.SAP_518_ECM_Pod__Left_)
        Smoke_Generator___red = (1, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (1, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (1, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (1, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (1, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (1, Weapons.Smoke_Generator___orange)

    class Pylon2:
        R_73__AA_11_Archer____Infra_Red = (2, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            2,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            2,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            2,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            2,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            2,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Smoke_Generator___red = (2, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (2, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (2, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (2, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (2, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (2, Weapons.Smoke_Generator___orange)

    # ERRR <CLEAN>

    class Pylon3:
        R_73__AA_11_Archer____Infra_Red = (3, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            3,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            3,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            3,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            3,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27T1__AA_10_Alamo_B____Infra_Red = (
            3,
            WeaponsSu30.R_27T1__AA_10_Alamo_B____Infra_Red,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            3,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_27ET1__AA_10_Alamo_D____IR_Extended_Range = (
            3,
            WeaponsSu30.R_27ET1__AA_10_Alamo_D____IR_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            3,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            3,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Kh_31P__AS_17_Krypton____600kg = (3, WeaponsSu30.Kh_31P__AS_17_Krypton____600kg)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            3,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            3,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            3,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_59M__AS_18_Kazoo___930kg = (3, WeaponsSu30.Kh_59M__AS_18_Kazoo___930kg)
        Kh_59MK__AS_18_Kazoo____930kg = (3, WeaponsSu30.Kh_59MK__AS_18_Kazoo____930kg)
        Kh_31A__AS_17_Krypton____610kg = (3, WeaponsSu30.Kh_31A__AS_17_Krypton____610kg)
        Kh_35__AS_20_Kayak____520kg = (3, WeaponsSu30.Kh_35__AS_20_Kayak____520kg)
        KAB_500Kr___500kg_TV_Guided_Bomb = (3, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (3, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            3,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            3,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            3,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            3,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (3, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            3,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            3,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        FAB_250___250kg_GP_Bomb_LD = (3, Weapons.FAB_250___250kg_GP_Bomb_LD)
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            3,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M_62___500kg_GP_Bomb_LD = (3, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            3,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            3,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD = (
            3,
            Weapons.MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD,
        )
        _2_x_B_13L_pods___10_x_S_13_OF__122mm_UnGd_Rkts__Blast_Frag = (
            3,
            Weapons._2_x_B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            3,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange = (
            3,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8OFP2_MPP = (
            3,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8OFP2_MPP,
        )
        _2_x_S_25 = (3, Weapons._2_x_S_25)
        Mk_82___500lb_GP_Bomb_LD = (3, Weapons.Mk_82___500lb_GP_Bomb_LD)
        GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            WeaponsSu30.GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (3, Weapons.GBU_12___500lb_Laser_Guided_Bomb)

    # ERRR <CLEAN>

    class Pylon4:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            4,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            4,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            4,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            4,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Kh_31P__AS_17_Krypton____600kg = (4, WeaponsSu30.Kh_31P__AS_17_Krypton____600kg)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            4,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            4,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            4,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_59M__AS_18_Kazoo___930kg = (4, WeaponsSu30.Kh_59M__AS_18_Kazoo___930kg)
        Kh_59MK__AS_18_Kazoo____930kg = (4, WeaponsSu30.Kh_59MK__AS_18_Kazoo____930kg)
        Kh_31A__AS_17_Krypton____610kg = (4, WeaponsSu30.Kh_31A__AS_17_Krypton____610kg)
        Kh_35__AS_20_Kayak____520kg = (4, WeaponsSu30.Kh_35__AS_20_Kayak____520kg)
        KAB_500Kr___500kg_TV_Guided_Bomb = (4, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (4, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_1500Kr___1500kg = (4, WeaponsSu30.KAB_1500Kr___1500kg)
        KAB_1500LG_PR___1500kg = (4, WeaponsSu30.KAB_1500LG_PR___1500kg)
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            4,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            4,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            4,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            4,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            4,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (4, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            4,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            4,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        FAB_250___250kg_GP_Bomb_LD = (4, Weapons.FAB_250___250kg_GP_Bomb_LD)
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            4,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M_62___500kg_GP_Bomb_LD = (4, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            4,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            4,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD = (
            4,
            Weapons.MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD,
        )
        # ERRR <CLEAN>
        Mk_82___500lb_GP_Bomb_LD = (4, Weapons.Mk_82___500lb_GP_Bomb_LD)
        GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            4,
            WeaponsSu30.GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (4, Weapons.GBU_12___500lb_Laser_Guided_Bomb)

    class Pylon5:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            5,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            5,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            5,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            5,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Kh_31P__AS_17_Krypton____600kg = (5, WeaponsSu30.Kh_31P__AS_17_Krypton____600kg)
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            5,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            5,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            5,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_31A__AS_17_Krypton____610kg = (5, WeaponsSu30.Kh_31A__AS_17_Krypton____610kg)
        KAB_500Kr___500kg_TV_Guided_Bomb = (5, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (5, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            5,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            5,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        P_50T___50kg_Practice_Bomb_LD = (5, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            5,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            5,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        FAB_250___250kg_GP_Bomb_LD = (5, Weapons.FAB_250___250kg_GP_Bomb_LD)
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            5,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M_62___500kg_GP_Bomb_LD = (5, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            5,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            5,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        APK_9_POD = (5, WeaponsSu30.APK_9_POD)
        # ERRR <CLEAN>
        Mk_82___500lb_GP_Bomb_LD = (5, Weapons.Mk_82___500lb_GP_Bomb_LD)
        GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            5,
            WeaponsSu30.GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (5, Weapons.GBU_12___500lb_Laser_Guided_Bomb)

    class Pylon6:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            6,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            6,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            6,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            6,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (6, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (6, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_1500Kr___1500kg = (6, WeaponsSu30.KAB_1500Kr___1500kg)
        KAB_1500LG_PR___1500kg = (6, WeaponsSu30.KAB_1500LG_PR___1500kg)
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            6,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            6,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            6,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            6,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            6,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (6, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            6,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            6,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        FAB_250___250kg_GP_Bomb_LD = (6, Weapons.FAB_250___250kg_GP_Bomb_LD)
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            6,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M_62___500kg_GP_Bomb_LD = (6, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            6,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            6,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag = (
            6,
            Weapons.RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag,
        )
        RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP = (
            6,
            Weapons.RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP,
        )
        # ERRR <CLEAN>
        Mk_82___500lb_GP_Bomb_LD = (6, Weapons.Mk_82___500lb_GP_Bomb_LD)
        GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            6,
            WeaponsSu30.GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (6, Weapons.GBU_12___500lb_Laser_Guided_Bomb)

    class Pylon7:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            7,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            7,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            7,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            7,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (7, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (7, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            7,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            7,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            7,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            7,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (7, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            7,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            7,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        FAB_250___250kg_GP_Bomb_LD = (7, Weapons.FAB_250___250kg_GP_Bomb_LD)
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            7,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M_62___500kg_GP_Bomb_LD = (7, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            7,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            7,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag = (
            7,
            Weapons.RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag,
        )
        RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP = (
            7,
            Weapons.RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP,
        )
        # ERRR <CLEAN>
        Smoke_Generator___red = (7, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (7, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (7, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (7, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (7, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (7, Weapons.Smoke_Generator___orange)
        Mk_82___500lb_GP_Bomb_LD = (7, Weapons.Mk_82___500lb_GP_Bomb_LD)
        GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            WeaponsSu30.GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (7, Weapons.GBU_12___500lb_Laser_Guided_Bomb)

    class Pylon8:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            8,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            8,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            8,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            8,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Kh_31P__AS_17_Krypton____600kg = (8, WeaponsSu30.Kh_31P__AS_17_Krypton____600kg)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            8,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            8,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            8,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_31A__AS_17_Krypton____610kg = (8, WeaponsSu30.Kh_31A__AS_17_Krypton____610kg)
        KAB_500Kr___500kg_TV_Guided_Bomb = (8, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (8, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            8,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            8,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        P_50T___50kg_Practice_Bomb_LD = (8, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            8,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            8,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        FAB_250___250kg_GP_Bomb_LD = (8, Weapons.FAB_250___250kg_GP_Bomb_LD)
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            8,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M_62___500kg_GP_Bomb_LD = (8, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            8,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            8,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        # ERRR {DAMOCLES}
        # ERRR <CLEAN>
        Mk_82___500lb_GP_Bomb_LD = (8, Weapons.Mk_82___500lb_GP_Bomb_LD)
        GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            8,
            WeaponsSu30.GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (8, Weapons.GBU_12___500lb_Laser_Guided_Bomb)

    class Pylon9:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            9,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            9,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            9,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            9,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Kh_31P__AS_17_Krypton____600kg = (9, WeaponsSu30.Kh_31P__AS_17_Krypton____600kg)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            9,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            9,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            9,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_59M__AS_18_Kazoo___930kg = (9, WeaponsSu30.Kh_59M__AS_18_Kazoo___930kg)
        Kh_59MK__AS_18_Kazoo____930kg = (9, WeaponsSu30.Kh_59MK__AS_18_Kazoo____930kg)
        Kh_31A__AS_17_Krypton____610kg = (9, WeaponsSu30.Kh_31A__AS_17_Krypton____610kg)
        Kh_35__AS_20_Kayak____520kg = (9, WeaponsSu30.Kh_35__AS_20_Kayak____520kg)
        KAB_500Kr___500kg_TV_Guided_Bomb = (9, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (9, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_1500Kr___1500kg = (9, WeaponsSu30.KAB_1500Kr___1500kg)
        KAB_1500LG_PR___1500kg = (9, WeaponsSu30.KAB_1500LG_PR___1500kg)
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            9,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            9,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            9,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            9,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            9,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (9, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            9,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            9,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        FAB_250___250kg_GP_Bomb_LD = (9, Weapons.FAB_250___250kg_GP_Bomb_LD)
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            9,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M_62___500kg_GP_Bomb_LD = (9, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            9,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            9,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD = (
            9,
            Weapons.MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD,
        )
        # ERRR <CLEAN>
        Mk_82___500lb_GP_Bomb_LD = (9, Weapons.Mk_82___500lb_GP_Bomb_LD)
        GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            9,
            WeaponsSu30.GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (9, Weapons.GBU_12___500lb_Laser_Guided_Bomb)

    class Pylon10:
        R_73__AA_11_Archer____Infra_Red = (10, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            10,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            10,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            10,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            10,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27T1__AA_10_Alamo_B____Infra_Red = (
            10,
            WeaponsSu30.R_27T1__AA_10_Alamo_B____Infra_Red,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            10,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_27ET1__AA_10_Alamo_D____IR_Extended_Range = (
            10,
            WeaponsSu30.R_27ET1__AA_10_Alamo_D____IR_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            10,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            10,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Kh_31P__AS_17_Krypton____600kg = (
            10,
            WeaponsSu30.Kh_31P__AS_17_Krypton____600kg,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            10,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            10,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            10,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_59M__AS_18_Kazoo___930kg = (10, WeaponsSu30.Kh_59M__AS_18_Kazoo___930kg)
        Kh_59MK__AS_18_Kazoo____930kg = (10, WeaponsSu30.Kh_59MK__AS_18_Kazoo____930kg)
        Kh_31A__AS_17_Krypton____610kg = (
            10,
            WeaponsSu30.Kh_31A__AS_17_Krypton____610kg,
        )
        Kh_35__AS_20_Kayak____520kg = (10, WeaponsSu30.Kh_35__AS_20_Kayak____520kg)
        KAB_500Kr___500kg_TV_Guided_Bomb = (
            10,
            Weapons.KAB_500Kr___500kg_TV_Guided_Bomb,
        )
        KAB_500S___500kg__GPS_Guided = (10, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            10,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            10,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            10,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            10,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (10, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            10,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            10,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        FAB_250___250kg_GP_Bomb_LD = (10, Weapons.FAB_250___250kg_GP_Bomb_LD)
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            10,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M_62___500kg_GP_Bomb_LD = (10, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            10,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            10,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD = (
            10,
            Weapons.MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD,
        )
        _2_x_B_13L_pods___10_x_S_13_OF__122mm_UnGd_Rkts__Blast_Frag = (
            10,
            Weapons._2_x_B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            10,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange = (
            10,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8OFP2_MPP = (
            10,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8OFP2_MPP,
        )
        _2_x_S_25 = (10, Weapons._2_x_S_25)
        # ERRR <CLEAN>
        Mk_82___500lb_GP_Bomb_LD = (10, Weapons.Mk_82___500lb_GP_Bomb_LD)
        GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            10,
            WeaponsSu30.GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (
            10,
            Weapons.GBU_12___500lb_Laser_Guided_Bomb,
        )

    class Pylon11:
        R_73__AA_11_Archer____Infra_Red = (11, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            11,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            11,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            11,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            11,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            11,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Smoke_Generator___red = (11, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (11, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (11, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (11, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (11, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (11, Weapons.Smoke_Generator___orange)

    # ERRR <CLEAN>

    class Pylon12:
        R_73__AA_11_Archer____Infra_Red = (12, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            12,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            12,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            12,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        L005_Sorbtsiya_ECM_pod__right_ = (12, Weapons.L005_Sorbtsiya_ECM_pod__right_)
        SAP_518_ECM_Pod__Right_ = (12, WeaponsSu30.SAP_518_ECM_Pod__Right_)
        Smoke_Generator___red = (12, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (12, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (12, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (12, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (12, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (12, Weapons.Smoke_Generator___orange)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}

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


@planemod
class Su_30MKI(PlaneType):
    id = "Su-30MKI"
    flyable = True
    height = 5.932
    width = 14.7
    length = 21.935
    fuel_max = 9500
    max_speed = 2499.984
    chaff = 96
    flare = 96
    charge_total = 192
    chaff_charge_size = 1
    flare_charge_size = 1
    eplrs = True
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}

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
                1: 117,
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

    property_defaults: Dict[str, Any] = {
        "SoloFlight": False,
        "NetCrewControlPriority": 0,
        "HumanOrchestra": False,
        "HelmetMountedDevice": 1,
        "ShowLadders": True,
        "su30Chaff": 96,
        "su30Flare": 96,
    }

    class Properties:
        class SoloFlight:
            id = "SoloFlight"

        class NetCrewControlPriority:
            id = "NetCrewControlPriority"

            class Values:
                Pilot = 0
                WSO = 1
                Ask_Always = -1
                Equally_Responsible = -2

        class HumanOrchestra:
            id = "HumanOrchestra"

        class HelmetMountedDevice:
            id = "HelmetMountedDevice"

            class Values:
                Not_installed = 0
                SURA_Visor = 1
                NVG = 2

        class ShowLadders:
            id = "ShowLadders"

        class su30Chaff:
            id = "su30Chaff"

        class su30Flare:
            id = "su30Flare"

    properties = {
        "SoloFlight": UnitPropertyDescription(
            identifier="SoloFlight",
            control="checkbox",
            label="Solo Flight",
            player_only=True,
            default=False,
            weight_when_on=-80,
        ),
        "NetCrewControlPriority": UnitPropertyDescription(
            identifier="NetCrewControlPriority",
            control="comboList",
            label="Aircraft Control Priority",
            player_only=True,
            default=0,
            w_ctrl=150,
            values={
                0: "Pilot",
                1: "WSO",
                -1: "Ask Always",
                -2: "Equally Responsible",
            },
        ),
        "HumanOrchestra": UnitPropertyDescription(
            identifier="HumanOrchestra",
            control="checkbox",
            label="Disable Multicrew",
            player_only=True,
            default=False,
        ),
        "HelmetMountedDevice": UnitPropertyDescription(
            identifier="HelmetMountedDevice",
            control="comboList",
            label="Helmet Mounted Device",
            player_only=True,
            default=1,
            w_ctrl=150,
            values={
                0: "Not installed",
                1: "SURA Visor",
                2: "NVG",
            },
        ),
        "ShowLadders": UnitPropertyDescription(
            identifier="ShowLadders",
            control="checkbox",
            label="Show Ladders",
            default=True,
        ),
        "su30Chaff": UnitPropertyDescription(
            identifier="su30Chaff",
            control="spinbox",
            label="Chaff",
            player_only=True,
            minimum=0,
            maximum=192,
            default=96,
            dimension=" ",
        ),
        "su30Flare": UnitPropertyDescription(
            identifier="su30Flare",
            control="spinbox",
            label="Flare",
            player_only=True,
            minimum=0,
            maximum=192,
            default=96,
            dimension=" ",
        ),
    }

    livery_name = "SU-30MKI"  # from type

    class Pylon1:
        R_73__AA_11_Archer____Infra_Red = (1, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            1,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            1,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            1,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        L005_Sorbtsiya_ECM_pod__left_ = (1, Weapons.L005_Sorbtsiya_ECM_pod__left_)
        SAP_518_ECM_Pod__Left_ = (1, WeaponsSu30.SAP_518_ECM_Pod__Left_)
        Smoke_Generator___red = (1, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (1, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (1, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (1, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (1, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (1, Weapons.Smoke_Generator___orange)

    class Pylon2:
        R_73__AA_11_Archer____Infra_Red = (2, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            2,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            2,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            2,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        ASTRA_Mk_1___Active_Rdr_AAM = (2, WeaponsSu30.ASTRA_Mk_1___Active_Rdr_AAM)
        I_Derby_ER___Active_Rdr_AAM = (2, WeaponsSu30.I_Derby_ER___Active_Rdr_AAM)
        RVV_AE__AA_12_Adder____Active_Rdr = (
            2,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            2,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Smoke_Generator___red = (2, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (2, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (2, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (2, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (2, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (2, Weapons.Smoke_Generator___orange)

    # ERRR <CLEAN>

    class Pylon3:
        R_73__AA_11_Archer____Infra_Red = (3, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            3,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            3,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            3,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            3,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27T1__AA_10_Alamo_B____Infra_Red = (
            3,
            WeaponsSu30.R_27T1__AA_10_Alamo_B____Infra_Red,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            3,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_27ET1__AA_10_Alamo_D____IR_Extended_Range = (
            3,
            WeaponsSu30.R_27ET1__AA_10_Alamo_D____IR_Extended_Range,
        )
        ASTRA_Mk_1___Active_Rdr_AAM = (3, WeaponsSu30.ASTRA_Mk_1___Active_Rdr_AAM)
        I_Derby_ER___Active_Rdr_AAM = (3, WeaponsSu30.I_Derby_ER___Active_Rdr_AAM)
        RVV_AE__AA_12_Adder____Active_Rdr = (
            3,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            3,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            3,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            3,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            3,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_59M__AS_18_Kazoo___930kg = (3, WeaponsSu30.Kh_59M__AS_18_Kazoo___930kg)
        Kh_59MK__AS_18_Kazoo____930kg = (3, WeaponsSu30.Kh_59MK__AS_18_Kazoo____930kg)
        Kh_31A__AS_17_Krypton____610kg = (3, WeaponsSu30.Kh_31A__AS_17_Krypton____610kg)
        Kh_31P__AS_17_Krypton____600kg = (3, WeaponsSu30.Kh_31P__AS_17_Krypton____600kg)
        Kh_35__AS_20_Kayak____520kg = (3, WeaponsSu30.Kh_35__AS_20_Kayak____520kg)
        Rudra_M1 = (3, WeaponsSu30.Rudra_M1)
        SAAW_POD = (3, WeaponsSu30.SAAW_POD)
        KAB_500Kr___500kg_TV_Guided_Bomb = (3, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (3, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            3,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            3,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            3,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            3,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (3, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            3,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            3,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            3,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            3,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        FAB_500_M54___474kg__freefall = (3, WeaponsSu30.FAB_500_M54___474kg__freefall)
        FAB_500_M62___474kg__freefall = (3, WeaponsSu30.FAB_500_M62___474kg__freefall)
        FAB_250_M62___227kg__freefall = (3, WeaponsSu30.FAB_250_M62___227kg__freefall)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            3,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            3,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )
        _2_x_B_13L_pods___10_x_S_13_OF__122mm_UnGd_Rkts__Blast_Frag = (
            3,
            Weapons._2_x_B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            3,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange = (
            3,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8OFP2_MPP = (
            3,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8OFP2_MPP,
        )
        _2_x_S_25 = (3, Weapons._2_x_S_25)

    # ERRR <CLEAN>

    class Pylon4:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            4,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            4,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        I_Derby_ER___Active_Rdr_AAM = (4, WeaponsSu30.I_Derby_ER___Active_Rdr_AAM)
        RVV_AE__AA_12_Adder____Active_Rdr = (
            4,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            4,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            4,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            4,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            4,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_59M__AS_18_Kazoo___930kg = (4, WeaponsSu30.Kh_59M__AS_18_Kazoo___930kg)
        Kh_59MK__AS_18_Kazoo____930kg = (4, WeaponsSu30.Kh_59MK__AS_18_Kazoo____930kg)
        Kh_31A__AS_17_Krypton____610kg = (4, WeaponsSu30.Kh_31A__AS_17_Krypton____610kg)
        Kh_31P__AS_17_Krypton____600kg = (4, WeaponsSu30.Kh_31P__AS_17_Krypton____600kg)
        Kh_35__AS_20_Kayak____520kg = (4, WeaponsSu30.Kh_35__AS_20_Kayak____520kg)
        Rudra_M1 = (4, WeaponsSu30.Rudra_M1)
        SAAW_POD = (4, WeaponsSu30.SAAW_POD)
        KAB_500Kr___500kg_TV_Guided_Bomb = (4, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (4, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_1500Kr___1500kg = (4, WeaponsSu30.KAB_1500Kr___1500kg)
        KAB_1500LG_PR___1500kg = (4, WeaponsSu30.KAB_1500LG_PR___1500kg)
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            4,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            4,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            4,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            4,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            4,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (4, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            4,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            4,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            4,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            4,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        FAB_500_M54___474kg__freefall = (4, WeaponsSu30.FAB_500_M54___474kg__freefall)
        FAB_500_M62___474kg__freefall = (4, WeaponsSu30.FAB_500_M62___474kg__freefall)
        FAB_250_M62___227kg__freefall = (4, WeaponsSu30.FAB_250_M62___227kg__freefall)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            4,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            4,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )

    # ERRR <CLEAN>

    class Pylon5:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            5,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            5,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        I_Derby_ER___Active_Rdr_AAM = (5, WeaponsSu30.I_Derby_ER___Active_Rdr_AAM)
        RVV_AE__AA_12_Adder____Active_Rdr = (
            5,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            5,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            5,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            5,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            5,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        Kh_31A__AS_17_Krypton____610kg = (5, WeaponsSu30.Kh_31A__AS_17_Krypton____610kg)
        Kh_31P__AS_17_Krypton____600kg = (5, WeaponsSu30.Kh_31P__AS_17_Krypton____600kg)
        Rudra_M1 = (5, WeaponsSu30.Rudra_M1)
        KAB_500Kr___500kg_TV_Guided_Bomb = (5, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (5, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            5,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            5,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        P_50T___50kg_Practice_Bomb_LD = (5, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            5,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            5,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            5,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            5,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        FAB_500_M54___474kg__freefall = (5, WeaponsSu30.FAB_500_M54___474kg__freefall)
        FAB_500_M62___474kg__freefall = (5, WeaponsSu30.FAB_500_M62___474kg__freefall)
        FAB_250_M62___227kg__freefall = (5, WeaponsSu30.FAB_250_M62___227kg__freefall)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            5,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            5,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )
        APK_9_POD = (5, WeaponsSu30.APK_9_POD)
        L_081_Fantasmagoria_ELINT_pod = (5, Weapons.L_081_Fantasmagoria_ELINT_pod)

    # ERRR <CLEAN>

    class Pylon6:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            6,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            6,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            6,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            6,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        I_Derby_ER___Active_Rdr_AAM = (6, WeaponsSu30.I_Derby_ER___Active_Rdr_AAM)
        # ERRR {BRAHMOS_AG}
        BRAHMOS_A_Ship = (6, WeaponsSu30.BRAHMOS_A_Ship)
        BRAHMOS_SEAD = (6, WeaponsSu30.BRAHMOS_SEAD)
        KAB_500Kr___500kg_TV_Guided_Bomb = (6, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (6, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_1500Kr___1500kg = (6, WeaponsSu30.KAB_1500Kr___1500kg)
        KAB_1500LG_PR___1500kg = (6, WeaponsSu30.KAB_1500LG_PR___1500kg)
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            6,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            6,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            6,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            6,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            6,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (6, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            6,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            6,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            6,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            6,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        FAB_500_M54___474kg__freefall = (6, WeaponsSu30.FAB_500_M54___474kg__freefall)
        FAB_500_M62___474kg__freefall = (6, WeaponsSu30.FAB_500_M62___474kg__freefall)
        FAB_250_M62___227kg__freefall = (6, WeaponsSu30.FAB_250_M62___227kg__freefall)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            6,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            6,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )
        RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag = (
            6,
            Weapons.RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag,
        )
        RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP = (
            6,
            Weapons.RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP,
        )
        EL_M_2060 = (6, WeaponsSu30.EL_M_2060)

    # ERRR <CLEAN>

    class Pylon7:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            7,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            7,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            7,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            7,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        I_Derby_ER___Active_Rdr_AAM = (7, WeaponsSu30.I_Derby_ER___Active_Rdr_AAM)
        KAB_500Kr___500kg_TV_Guided_Bomb = (7, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (7, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            7,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            7,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            7,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            7,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (7, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            7,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            7,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            7,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            7,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        FAB_500_M54___474kg__freefall = (7, WeaponsSu30.FAB_500_M54___474kg__freefall)
        FAB_500_M62___474kg__freefall = (7, WeaponsSu30.FAB_500_M62___474kg__freefall)
        FAB_250_M62___227kg__freefall = (7, WeaponsSu30.FAB_250_M62___227kg__freefall)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            7,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            7,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )
        Smoke_Generator___red = (7, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (7, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (7, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (7, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (7, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (7, Weapons.Smoke_Generator___orange)
        # ERRR <CLEAN>
        RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag = (
            7,
            Weapons.RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag,
        )
        RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP = (
            7,
            Weapons.RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP,
        )

    class Pylon8:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            8,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            8,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            8,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            8,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        I_Derby_ER___Active_Rdr_AAM = (8, WeaponsSu30.I_Derby_ER___Active_Rdr_AAM)
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            8,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            8,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            8,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_31A__AS_17_Krypton____610kg = (8, WeaponsSu30.Kh_31A__AS_17_Krypton____610kg)
        Kh_31P__AS_17_Krypton____600kg = (8, WeaponsSu30.Kh_31P__AS_17_Krypton____600kg)
        Rudra_M1 = (8, WeaponsSu30.Rudra_M1)
        KAB_500Kr___500kg_TV_Guided_Bomb = (8, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (8, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            8,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            8,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        P_50T___50kg_Practice_Bomb_LD = (8, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            8,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            8,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            8,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            8,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        FAB_500_M54___474kg__freefall = (8, WeaponsSu30.FAB_500_M54___474kg__freefall)
        FAB_500_M62___474kg__freefall = (8, WeaponsSu30.FAB_500_M62___474kg__freefall)
        FAB_250_M62___227kg__freefall = (8, WeaponsSu30.FAB_250_M62___227kg__freefall)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            8,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            8,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )
        LITENING___Targeting_Pod = (8, WeaponsSu30.LITENING___Targeting_Pod)

    # ERRR <CLEAN>

    class Pylon9:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            9,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            9,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            9,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            9,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        I_Derby_ER___Active_Rdr_AAM = (9, WeaponsSu30.I_Derby_ER___Active_Rdr_AAM)
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            9,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            9,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            9,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_59M__AS_18_Kazoo___930kg = (9, WeaponsSu30.Kh_59M__AS_18_Kazoo___930kg)
        Kh_59MK__AS_18_Kazoo____930kg = (9, WeaponsSu30.Kh_59MK__AS_18_Kazoo____930kg)
        Kh_31A__AS_17_Krypton____610kg = (9, WeaponsSu30.Kh_31A__AS_17_Krypton____610kg)
        Kh_31P__AS_17_Krypton____600kg = (9, WeaponsSu30.Kh_31P__AS_17_Krypton____600kg)
        Kh_35__AS_20_Kayak____520kg = (9, WeaponsSu30.Kh_35__AS_20_Kayak____520kg)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            9,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            9,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        Rudra_M1 = (9, WeaponsSu30.Rudra_M1)
        SAAW_POD = (9, WeaponsSu30.SAAW_POD)
        KAB_500Kr___500kg_TV_Guided_Bomb = (9, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (9, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_1500Kr___1500kg = (9, WeaponsSu30.KAB_1500Kr___1500kg)
        KAB_1500LG_PR___1500kg = (9, WeaponsSu30.KAB_1500LG_PR___1500kg)
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            9,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            9,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            9,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (9, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            9,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            9,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            9,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            9,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        FAB_500_M54___474kg__freefall = (9, WeaponsSu30.FAB_500_M54___474kg__freefall)
        FAB_500_M62___474kg__freefall = (9, WeaponsSu30.FAB_500_M62___474kg__freefall)
        FAB_250_M62___227kg__freefall = (9, WeaponsSu30.FAB_250_M62___227kg__freefall)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            9,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            9,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )

    # ERRR <CLEAN>

    class Pylon10:
        R_73__AA_11_Archer____Infra_Red = (10, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            10,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            10,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            10,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            10,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27T1__AA_10_Alamo_B____Infra_Red = (
            10,
            WeaponsSu30.R_27T1__AA_10_Alamo_B____Infra_Red,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            10,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_27ET1__AA_10_Alamo_D____IR_Extended_Range = (
            10,
            WeaponsSu30.R_27ET1__AA_10_Alamo_D____IR_Extended_Range,
        )
        ASTRA_Mk_1___Active_Rdr_AAM = (10, WeaponsSu30.ASTRA_Mk_1___Active_Rdr_AAM)
        I_Derby_ER___Active_Rdr_AAM = (10, WeaponsSu30.I_Derby_ER___Active_Rdr_AAM)
        RVV_AE__AA_12_Adder____Active_Rdr = (
            10,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            10,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            10,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            10,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            10,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_59M__AS_18_Kazoo___930kg = (10, WeaponsSu30.Kh_59M__AS_18_Kazoo___930kg)
        Kh_59MK__AS_18_Kazoo____930kg = (10, WeaponsSu30.Kh_59MK__AS_18_Kazoo____930kg)
        Kh_31A__AS_17_Krypton____610kg = (
            10,
            WeaponsSu30.Kh_31A__AS_17_Krypton____610kg,
        )
        Kh_31P__AS_17_Krypton____600kg = (
            10,
            WeaponsSu30.Kh_31P__AS_17_Krypton____600kg,
        )
        Kh_35__AS_20_Kayak____520kg = (10, WeaponsSu30.Kh_35__AS_20_Kayak____520kg)
        Rudra_M1 = (10, WeaponsSu30.Rudra_M1)
        SAAW_POD = (10, WeaponsSu30.SAAW_POD)
        KAB_500Kr___500kg_TV_Guided_Bomb = (
            10,
            Weapons.KAB_500Kr___500kg_TV_Guided_Bomb,
        )
        KAB_500S___500kg__GPS_Guided = (10, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            10,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            10,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            10,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            10,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (10, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            10,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            10,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            10,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            10,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        FAB_500_M54___474kg__freefall = (10, WeaponsSu30.FAB_500_M54___474kg__freefall)
        FAB_500_M62___474kg__freefall = (10, WeaponsSu30.FAB_500_M62___474kg__freefall)
        FAB_250_M62___227kg__freefall = (10, WeaponsSu30.FAB_250_M62___227kg__freefall)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            10,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            10,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )
        _2_x_B_13L_pods___10_x_S_13_OF__122mm_UnGd_Rkts__Blast_Frag = (
            10,
            Weapons._2_x_B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            10,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange = (
            10,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8OFP2_MPP = (
            10,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8OFP2_MPP,
        )
        _2_x_S_25 = (10, Weapons._2_x_S_25)

    # ERRR <CLEAN>

    class Pylon11:
        R_73__AA_11_Archer____Infra_Red = (11, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            11,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            11,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            11,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        ASTRA_Mk_1___Active_Rdr_AAM = (11, WeaponsSu30.ASTRA_Mk_1___Active_Rdr_AAM)
        I_Derby_ER___Active_Rdr_AAM = (11, WeaponsSu30.I_Derby_ER___Active_Rdr_AAM)
        RVV_AE__AA_12_Adder____Active_Rdr = (
            11,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            11,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Smoke_Generator___red = (11, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (11, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (11, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (11, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (11, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (11, Weapons.Smoke_Generator___orange)

    # ERRR <CLEAN>

    class Pylon12:
        R_73__AA_11_Archer____Infra_Red = (12, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            12,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            12,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            12,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        L005_Sorbtsiya_ECM_pod__right_ = (12, Weapons.L005_Sorbtsiya_ECM_pod__right_)
        SAP_518_ECM_Pod__Right_ = (12, WeaponsSu30.SAP_518_ECM_Pod__Right_)
        Smoke_Generator___red = (12, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (12, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (12, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (12, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (12, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (12, Weapons.Smoke_Generator___orange)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}

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


@planemod
class Su_30MKA_AG(PlaneType):
    id = "Su-30MKA-AG"
    flyable = True
    height = 5.932
    width = 14.7
    length = 21.935
    fuel_max = 9500
    max_speed = 2499.984
    chaff = 96
    flare = 96
    charge_total = 192
    chaff_charge_size = 1
    flare_charge_size = 1
    eplrs = True
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}

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
                1: 117,
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

    property_defaults: Dict[str, Any] = {
        "SoloFlight": False,
        "NetCrewControlPriority": 0,
        "HumanOrchestra": False,
        "HelmetMountedDevice": 1,
        "ShowLadders": True,
        "su30Chaff": 96,
        "su30Flare": 96,
    }

    class Properties:
        class SoloFlight:
            id = "SoloFlight"

        class NetCrewControlPriority:
            id = "NetCrewControlPriority"

            class Values:
                Pilot = 0
                WSO = 1
                Ask_Always = -1
                Equally_Responsible = -2

        class HumanOrchestra:
            id = "HumanOrchestra"

        class HelmetMountedDevice:
            id = "HelmetMountedDevice"

            class Values:
                Not_installed = 0
                SURA_Visor = 1
                NVG = 2

        class ShowLadders:
            id = "ShowLadders"

        class su30Chaff:
            id = "su30Chaff"

        class su30Flare:
            id = "su30Flare"

    properties = {
        "SoloFlight": UnitPropertyDescription(
            identifier="SoloFlight",
            control="checkbox",
            label="Solo Flight",
            player_only=True,
            default=False,
            weight_when_on=-80,
        ),
        "NetCrewControlPriority": UnitPropertyDescription(
            identifier="NetCrewControlPriority",
            control="comboList",
            label="Aircraft Control Priority",
            player_only=True,
            default=0,
            w_ctrl=150,
            values={
                0: "Pilot",
                1: "WSO",
                -1: "Ask Always",
                -2: "Equally Responsible",
            },
        ),
        "HumanOrchestra": UnitPropertyDescription(
            identifier="HumanOrchestra",
            control="checkbox",
            label="Disable Multicrew",
            player_only=True,
            default=False,
        ),
        "HelmetMountedDevice": UnitPropertyDescription(
            identifier="HelmetMountedDevice",
            control="comboList",
            label="Helmet Mounted Device",
            player_only=True,
            default=1,
            w_ctrl=150,
            values={
                0: "Not installed",
                1: "SURA Visor",
                2: "NVG",
            },
        ),
        "ShowLadders": UnitPropertyDescription(
            identifier="ShowLadders",
            control="checkbox",
            label="Show Ladders",
            default=True,
        ),
        "su30Chaff": UnitPropertyDescription(
            identifier="su30Chaff",
            control="spinbox",
            label="Chaff",
            player_only=True,
            minimum=0,
            maximum=192,
            default=96,
            dimension=" ",
        ),
        "su30Flare": UnitPropertyDescription(
            identifier="su30Flare",
            control="spinbox",
            label="Flare",
            player_only=True,
            minimum=0,
            maximum=192,
            default=96,
            dimension=" ",
        ),
    }

    livery_name = "SU-30MKA-AG"  # from type

    class Pylon1:
        R_73__AA_11_Archer____Infra_Red = (1, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            1,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            1,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            1,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        L005_Sorbtsiya_ECM_pod__left_ = (1, Weapons.L005_Sorbtsiya_ECM_pod__left_)
        SAP_518_ECM_Pod__Left_ = (1, WeaponsSu30.SAP_518_ECM_Pod__Left_)
        Smoke_Generator___red = (1, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (1, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (1, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (1, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (1, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (1, Weapons.Smoke_Generator___orange)

    class Pylon2:
        R_73__AA_11_Archer____Infra_Red = (2, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            2,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            2,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            2,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            2,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            2,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Smoke_Generator___red = (2, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (2, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (2, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (2, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (2, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (2, Weapons.Smoke_Generator___orange)

    # ERRR <CLEAN>

    class Pylon3:
        R_73__AA_11_Archer____Infra_Red = (3, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            3,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            3,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            3,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            3,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27T1__AA_10_Alamo_B____Infra_Red = (
            3,
            WeaponsSu30.R_27T1__AA_10_Alamo_B____Infra_Red,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            3,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_27ET1__AA_10_Alamo_D____IR_Extended_Range = (
            3,
            WeaponsSu30.R_27ET1__AA_10_Alamo_D____IR_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            3,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            3,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            3,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        Kh_31P__AS_17_Krypton____600kg = (3, WeaponsSu30.Kh_31P__AS_17_Krypton____600kg)
        Kh_36__AS_23____600kg_Grom_E1 = (3, WeaponsSu30.Kh_36__AS_23____600kg_Grom_E1)
        KH_38MTE__AS_23__IR_Guided = (3, WeaponsSu30.KH_38MTE__AS_23__IR_Guided)
        KH_38MLE__AS_23___Semi_Act_Laser = (
            3,
            WeaponsSu30.KH_38MLE__AS_23___Semi_Act_Laser,
        )
        Kh_38MAE__AS_23____500kg = (3, WeaponsSu30.Kh_38MAE__AS_23____500kg)
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            3,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            3,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_59M__AS_18_Kazoo___930kg = (3, WeaponsSu30.Kh_59M__AS_18_Kazoo___930kg)
        Kh_59MK__AS_18_Kazoo____930kg = (3, WeaponsSu30.Kh_59MK__AS_18_Kazoo____930kg)
        Kh_31A__AS_17_Krypton____610kg = (3, WeaponsSu30.Kh_31A__AS_17_Krypton____610kg)
        Kh_35__AS_20_Kayak____520kg = (3, WeaponsSu30.Kh_35__AS_20_Kayak____520kg)
        Kh_35UE__AS_20_Kayak____520kg = (3, WeaponsSu30.Kh_35UE__AS_20_Kayak____520kg)
        Kh_31AD__AS_17_Krypton____610kg = (
            3,
            WeaponsSu30.Kh_31AD__AS_17_Krypton____610kg,
        )
        Kh_31PD__AS_17_Krypton____600kg = (
            3,
            WeaponsSu30.Kh_31PD__AS_17_Krypton____600kg,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (3, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (3, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            3,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            3,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            3,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            3,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (3, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            3,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            3,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            3,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            3,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        FAB_500_M54___474kg__freefall = (3, WeaponsSu30.FAB_500_M54___474kg__freefall)
        FAB_500_M62___474kg__freefall = (3, WeaponsSu30.FAB_500_M62___474kg__freefall)
        FAB_250_M62___227kg__freefall = (3, WeaponsSu30.FAB_250_M62___227kg__freefall)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            3,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            3,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )
        _2_x_B_13L_pods___10_x_S_13_OF__122mm_UnGd_Rkts__Blast_Frag = (
            3,
            Weapons._2_x_B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            3,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange = (
            3,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8OFP2_MPP = (
            3,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8OFP2_MPP,
        )
        _2_x_S_25 = (3, Weapons._2_x_S_25)

    # ERRR <CLEAN>

    class Pylon4:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            4,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            4,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            4,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            4,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Kh_31P__AS_17_Krypton____600kg = (4, WeaponsSu30.Kh_31P__AS_17_Krypton____600kg)
        Kh_36__AS_23____600kg_Grom_E1 = (4, WeaponsSu30.Kh_36__AS_23____600kg_Grom_E1)
        KH_38MTE__AS_23__IR_Guided = (4, WeaponsSu30.KH_38MTE__AS_23__IR_Guided)
        KH_38MLE__AS_23___Semi_Act_Laser = (
            4,
            WeaponsSu30.KH_38MLE__AS_23___Semi_Act_Laser,
        )
        Kh_38MAE__AS_23____500kg = (4, WeaponsSu30.Kh_38MAE__AS_23____500kg)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            4,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            4,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            4,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_59M__AS_18_Kazoo___930kg = (4, WeaponsSu30.Kh_59M__AS_18_Kazoo___930kg)
        Kh_59MK__AS_18_Kazoo____930kg = (4, WeaponsSu30.Kh_59MK__AS_18_Kazoo____930kg)
        Kh_31A__AS_17_Krypton____610kg = (4, WeaponsSu30.Kh_31A__AS_17_Krypton____610kg)
        Kh_35__AS_20_Kayak____520kg = (4, WeaponsSu30.Kh_35__AS_20_Kayak____520kg)
        Kh_35UE__AS_20_Kayak____520kg = (4, WeaponsSu30.Kh_35UE__AS_20_Kayak____520kg)
        Kh_31AD__AS_17_Krypton____610kg = (
            4,
            WeaponsSu30.Kh_31AD__AS_17_Krypton____610kg,
        )
        Kh_31PD__AS_17_Krypton____600kg = (
            4,
            WeaponsSu30.Kh_31PD__AS_17_Krypton____600kg,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (4, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (4, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_1500Kr___1500kg = (4, WeaponsSu30.KAB_1500Kr___1500kg)
        KAB_1500LG_PR___1500kg = (4, WeaponsSu30.KAB_1500LG_PR___1500kg)
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            4,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            4,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            4,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            4,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            4,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (4, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            4,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            4,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            4,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            4,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        FAB_500_M54___474kg__freefall = (4, WeaponsSu30.FAB_500_M54___474kg__freefall)
        FAB_500_M62___474kg__freefall = (4, WeaponsSu30.FAB_500_M62___474kg__freefall)
        FAB_250_M62___227kg__freefall = (4, WeaponsSu30.FAB_250_M62___227kg__freefall)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            4,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            4,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )

    # ERRR <CLEAN>

    class Pylon5:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            5,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            5,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            5,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            5,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Kh_31P__AS_17_Krypton____600kg = (5, WeaponsSu30.Kh_31P__AS_17_Krypton____600kg)
        Kh_36__AS_23____600kg_Grom_E1 = (5, WeaponsSu30.Kh_36__AS_23____600kg_Grom_E1)
        KH_38MTE__AS_23__IR_Guided = (5, WeaponsSu30.KH_38MTE__AS_23__IR_Guided)
        KH_38MLE__AS_23___Semi_Act_Laser = (
            5,
            WeaponsSu30.KH_38MLE__AS_23___Semi_Act_Laser,
        )
        Kh_38MAE__AS_23____500kg = (5, WeaponsSu30.Kh_38MAE__AS_23____500kg)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            5,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            5,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            5,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_31A__AS_17_Krypton____610kg = (5, WeaponsSu30.Kh_31A__AS_17_Krypton____610kg)
        Kh_31AD__AS_17_Krypton____610kg = (
            5,
            WeaponsSu30.Kh_31AD__AS_17_Krypton____610kg,
        )
        Kh_31PD__AS_17_Krypton____600kg = (
            5,
            WeaponsSu30.Kh_31PD__AS_17_Krypton____600kg,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (5, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (5, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            5,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            5,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        P_50T___50kg_Practice_Bomb_LD = (5, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            5,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            5,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            5,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            5,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        FAB_500_M54___474kg__freefall = (5, WeaponsSu30.FAB_500_M54___474kg__freefall)
        FAB_500_M62___474kg__freefall = (5, WeaponsSu30.FAB_500_M62___474kg__freefall)
        FAB_250_M62___227kg__freefall = (5, WeaponsSu30.FAB_250_M62___227kg__freefall)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            5,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            5,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )
        APK_9_POD = (5, WeaponsSu30.APK_9_POD)
        L_081_Fantasmagoria_ELINT_pod = (5, Weapons.L_081_Fantasmagoria_ELINT_pod)

    # ERRR <CLEAN>

    class Pylon6:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            6,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            6,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            6,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            6,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (6, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (6, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_1500Kr___1500kg = (6, WeaponsSu30.KAB_1500Kr___1500kg)
        KAB_1500LG_PR___1500kg = (6, WeaponsSu30.KAB_1500LG_PR___1500kg)
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            6,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            6,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            6,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            6,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            6,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        P_50T___50kg_Practice_Bomb_LD = (6, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            6,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            6,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            6,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            6,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        FAB_500_M54___474kg__freefall = (6, WeaponsSu30.FAB_500_M54___474kg__freefall)
        FAB_500_M62___474kg__freefall = (6, WeaponsSu30.FAB_500_M62___474kg__freefall)
        FAB_250_M62___227kg__freefall = (6, WeaponsSu30.FAB_250_M62___227kg__freefall)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            6,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            6,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )
        RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag = (
            6,
            Weapons.RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag,
        )
        RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP = (
            6,
            Weapons.RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP,
        )

    # ERRR <CLEAN>

    class Pylon7:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            7,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            7,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            7,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            7,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (7, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (7, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            7,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            7,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            7,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            7,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (7, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            7,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            7,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            7,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            7,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        FAB_500_M54___474kg__freefall = (7, WeaponsSu30.FAB_500_M54___474kg__freefall)
        FAB_500_M62___474kg__freefall = (7, WeaponsSu30.FAB_500_M62___474kg__freefall)
        FAB_250_M62___227kg__freefall = (7, WeaponsSu30.FAB_250_M62___227kg__freefall)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            7,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            7,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )
        Smoke_Generator___red = (7, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (7, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (7, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (7, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (7, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (7, Weapons.Smoke_Generator___orange)
        RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag = (
            7,
            Weapons.RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag,
        )
        RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP = (
            7,
            Weapons.RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP,
        )

    # ERRR <CLEAN>

    class Pylon8:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            8,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            8,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            8,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            8,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Kh_31P__AS_17_Krypton____600kg = (8, WeaponsSu30.Kh_31P__AS_17_Krypton____600kg)
        Kh_36__AS_23____600kg_Grom_E1 = (8, WeaponsSu30.Kh_36__AS_23____600kg_Grom_E1)
        KH_38MTE__AS_23__IR_Guided = (8, WeaponsSu30.KH_38MTE__AS_23__IR_Guided)
        KH_38MLE__AS_23___Semi_Act_Laser = (
            8,
            WeaponsSu30.KH_38MLE__AS_23___Semi_Act_Laser,
        )
        Kh_38MAE__AS_23____500kg = (8, WeaponsSu30.Kh_38MAE__AS_23____500kg)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            8,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            8,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            8,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_31A__AS_17_Krypton____610kg = (8, WeaponsSu30.Kh_31A__AS_17_Krypton____610kg)
        Kh_31AD__AS_17_Krypton____610kg = (
            8,
            WeaponsSu30.Kh_31AD__AS_17_Krypton____610kg,
        )
        Kh_31PD__AS_17_Krypton____600kg = (
            8,
            WeaponsSu30.Kh_31PD__AS_17_Krypton____600kg,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (8, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (8, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            8,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            8,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        P_50T___50kg_Practice_Bomb_LD = (8, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            8,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            8,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            8,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            8,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        FAB_500_M54___474kg__freefall = (8, WeaponsSu30.FAB_500_M54___474kg__freefall)
        FAB_500_M62___474kg__freefall = (8, WeaponsSu30.FAB_500_M62___474kg__freefall)
        FAB_250_M62___227kg__freefall = (8, WeaponsSu30.FAB_250_M62___227kg__freefall)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            8,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            8,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )

    # ERRR <CLEAN>

    class Pylon9:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            9,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            9,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            9,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            9,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Kh_31P__AS_17_Krypton____600kg = (9, WeaponsSu30.Kh_31P__AS_17_Krypton____600kg)
        Kh_36__AS_23____600kg_Grom_E1 = (9, WeaponsSu30.Kh_36__AS_23____600kg_Grom_E1)
        KH_38MTE__AS_23__IR_Guided = (9, WeaponsSu30.KH_38MTE__AS_23__IR_Guided)
        KH_38MLE__AS_23___Semi_Act_Laser = (
            9,
            WeaponsSu30.KH_38MLE__AS_23___Semi_Act_Laser,
        )
        Kh_38MAE__AS_23____500kg = (9, WeaponsSu30.Kh_38MAE__AS_23____500kg)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            9,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            9,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            9,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_59M__AS_18_Kazoo___930kg = (9, WeaponsSu30.Kh_59M__AS_18_Kazoo___930kg)
        Kh_59MK__AS_18_Kazoo____930kg = (9, WeaponsSu30.Kh_59MK__AS_18_Kazoo____930kg)
        Kh_31A__AS_17_Krypton____610kg = (9, WeaponsSu30.Kh_31A__AS_17_Krypton____610kg)
        Kh_35__AS_20_Kayak____520kg = (9, WeaponsSu30.Kh_35__AS_20_Kayak____520kg)
        Kh_35UE__AS_20_Kayak____520kg = (9, WeaponsSu30.Kh_35UE__AS_20_Kayak____520kg)
        Kh_31AD__AS_17_Krypton____610kg = (
            9,
            WeaponsSu30.Kh_31AD__AS_17_Krypton____610kg,
        )
        Kh_31PD__AS_17_Krypton____600kg = (
            9,
            WeaponsSu30.Kh_31PD__AS_17_Krypton____600kg,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (9, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (9, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_1500Kr___1500kg = (9, WeaponsSu30.KAB_1500Kr___1500kg)
        KAB_1500LG_PR___1500kg = (9, WeaponsSu30.KAB_1500LG_PR___1500kg)
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            9,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            9,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            9,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            9,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            9,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (9, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            9,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            9,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            9,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            9,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        FAB_500_M54___474kg__freefall = (9, WeaponsSu30.FAB_500_M54___474kg__freefall)
        FAB_500_M62___474kg__freefall = (9, WeaponsSu30.FAB_500_M62___474kg__freefall)
        FAB_250_M62___227kg__freefall = (9, WeaponsSu30.FAB_250_M62___227kg__freefall)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            9,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            9,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )

    # ERRR <CLEAN>

    class Pylon10:
        R_73__AA_11_Archer____Infra_Red = (10, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            10,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            10,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            10,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            10,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27T1__AA_10_Alamo_B____Infra_Red = (
            10,
            WeaponsSu30.R_27T1__AA_10_Alamo_B____Infra_Red,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            10,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_27ET1__AA_10_Alamo_D____IR_Extended_Range = (
            10,
            WeaponsSu30.R_27ET1__AA_10_Alamo_D____IR_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            10,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            10,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Kh_31P__AS_17_Krypton____600kg = (
            10,
            WeaponsSu30.Kh_31P__AS_17_Krypton____600kg,
        )
        Kh_36__AS_23____600kg_Grom_E1 = (10, WeaponsSu30.Kh_36__AS_23____600kg_Grom_E1)
        KH_38MTE__AS_23__IR_Guided = (10, WeaponsSu30.KH_38MTE__AS_23__IR_Guided)
        KH_38MLE__AS_23___Semi_Act_Laser = (
            10,
            WeaponsSu30.KH_38MLE__AS_23___Semi_Act_Laser,
        )
        Kh_38MAE__AS_23____500kg = (10, WeaponsSu30.Kh_38MAE__AS_23____500kg)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            10,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            10,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            10,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_59M__AS_18_Kazoo___930kg = (10, WeaponsSu30.Kh_59M__AS_18_Kazoo___930kg)
        Kh_59MK__AS_18_Kazoo____930kg = (10, WeaponsSu30.Kh_59MK__AS_18_Kazoo____930kg)
        Kh_31A__AS_17_Krypton____610kg = (
            10,
            WeaponsSu30.Kh_31A__AS_17_Krypton____610kg,
        )
        Kh_35__AS_20_Kayak____520kg = (10, WeaponsSu30.Kh_35__AS_20_Kayak____520kg)
        Kh_35UE__AS_20_Kayak____520kg = (10, WeaponsSu30.Kh_35UE__AS_20_Kayak____520kg)
        Kh_31AD__AS_17_Krypton____610kg = (
            10,
            WeaponsSu30.Kh_31AD__AS_17_Krypton____610kg,
        )
        Kh_31PD__AS_17_Krypton____600kg = (
            10,
            WeaponsSu30.Kh_31PD__AS_17_Krypton____600kg,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (
            10,
            Weapons.KAB_500Kr___500kg_TV_Guided_Bomb,
        )
        KAB_500S___500kg__GPS_Guided = (10, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            10,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            10,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            10,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            10,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (10, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            10,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            10,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            10,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            10,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        FAB_500_M54___474kg__freefall = (10, WeaponsSu30.FAB_500_M54___474kg__freefall)
        FAB_500_M62___474kg__freefall = (10, WeaponsSu30.FAB_500_M62___474kg__freefall)
        FAB_250_M62___227kg__freefall = (10, WeaponsSu30.FAB_250_M62___227kg__freefall)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            10,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            10,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )
        _2_x_B_13L_pods___10_x_S_13_OF__122mm_UnGd_Rkts__Blast_Frag = (
            10,
            Weapons._2_x_B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            10,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange = (
            10,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8OFP2_MPP = (
            10,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8OFP2_MPP,
        )
        _2_x_S_25 = (10, Weapons._2_x_S_25)

    # ERRR <CLEAN>

    class Pylon11:
        R_73__AA_11_Archer____Infra_Red = (11, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            11,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            11,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            11,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            11,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            11,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Smoke_Generator___red = (11, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (11, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (11, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (11, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (11, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (11, Weapons.Smoke_Generator___orange)

    # ERRR <CLEAN>

    class Pylon12:
        R_73__AA_11_Archer____Infra_Red = (12, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            12,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            12,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            12,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        L005_Sorbtsiya_ECM_pod__right_ = (12, Weapons.L005_Sorbtsiya_ECM_pod__right_)
        SAP_518_ECM_Pod__Right_ = (12, WeaponsSu30.SAP_518_ECM_Pod__Right_)
        Smoke_Generator___red = (12, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (12, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (12, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (12, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (12, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (12, Weapons.Smoke_Generator___orange)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}

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


@planemod
class Su_30SM_AG(PlaneType):
    id = "Su-30SM-AG"
    flyable = True
    height = 5.932
    width = 14.7
    length = 21.935
    fuel_max = 9500
    max_speed = 2499.984
    chaff = 96
    flare = 96
    charge_total = 192
    chaff_charge_size = 1
    flare_charge_size = 1
    eplrs = True
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}

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
                1: 117,
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

    property_defaults: Dict[str, Any] = {
        "SoloFlight": False,
        "NetCrewControlPriority": 0,
        "HumanOrchestra": False,
        "HelmetMountedDevice": 1,
        "ShowLadders": True,
        "su30Chaff": 96,
        "su30Flare": 96,
    }

    class Properties:
        class SoloFlight:
            id = "SoloFlight"

        class NetCrewControlPriority:
            id = "NetCrewControlPriority"

            class Values:
                Pilot = 0
                WSO = 1
                Ask_Always = -1
                Equally_Responsible = -2

        class HumanOrchestra:
            id = "HumanOrchestra"

        class HelmetMountedDevice:
            id = "HelmetMountedDevice"

            class Values:
                Not_installed = 0
                SURA_Visor = 1
                NVG = 2

        class ShowLadders:
            id = "ShowLadders"

        class su30Chaff:
            id = "su30Chaff"

        class su30Flare:
            id = "su30Flare"

    properties = {
        "SoloFlight": UnitPropertyDescription(
            identifier="SoloFlight",
            control="checkbox",
            label="Solo Flight",
            player_only=True,
            default=False,
            weight_when_on=-80,
        ),
        "NetCrewControlPriority": UnitPropertyDescription(
            identifier="NetCrewControlPriority",
            control="comboList",
            label="Aircraft Control Priority",
            player_only=True,
            default=0,
            w_ctrl=150,
            values={
                0: "Pilot",
                1: "WSO",
                -1: "Ask Always",
                -2: "Equally Responsible",
            },
        ),
        "HumanOrchestra": UnitPropertyDescription(
            identifier="HumanOrchestra",
            control="checkbox",
            label="Disable Multicrew",
            player_only=True,
            default=False,
        ),
        "HelmetMountedDevice": UnitPropertyDescription(
            identifier="HelmetMountedDevice",
            control="comboList",
            label="Helmet Mounted Device",
            player_only=True,
            default=1,
            w_ctrl=150,
            values={
                0: "Not installed",
                1: "SURA Visor",
                2: "NVG",
            },
        ),
        "ShowLadders": UnitPropertyDescription(
            identifier="ShowLadders",
            control="checkbox",
            label="Show Ladders",
            default=True,
        ),
        "su30Chaff": UnitPropertyDescription(
            identifier="su30Chaff",
            control="spinbox",
            label="Chaff",
            player_only=True,
            minimum=0,
            maximum=192,
            default=96,
            dimension=" ",
        ),
        "su30Flare": UnitPropertyDescription(
            identifier="su30Flare",
            control="spinbox",
            label="Flare",
            player_only=True,
            minimum=0,
            maximum=192,
            default=96,
            dimension=" ",
        ),
    }

    livery_name = "SU-30SM-AG"  # from type

    class Pylon1:
        R_73__AA_11_Archer____Infra_Red = (1, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            1,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            1,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            1,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        L005_Sorbtsiya_ECM_pod__left_ = (1, Weapons.L005_Sorbtsiya_ECM_pod__left_)
        SAP_518_ECM_Pod__Left_ = (1, WeaponsSu30.SAP_518_ECM_Pod__Left_)
        Smoke_Generator___red = (1, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (1, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (1, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (1, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (1, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (1, Weapons.Smoke_Generator___orange)
        Smoke_Generator___Black = (1, WeaponsSu30.Smoke_Generator___Black)

    class Pylon2:
        R_73__AA_11_Archer____Infra_Red = (2, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            2,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            2,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            2,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        R_77__AA_12_Adder_Early____Active_Rdr = (
            2,
            WeaponsSu30.R_77__AA_12_Adder_Early____Active_Rdr,
        )
        R_77_1__AA_12_Adder_B____Active_Rdr = (
            2,
            WeaponsSu30.R_77_1__AA_12_Adder_B____Active_Rdr,
        )
        R_77M__AA_12_Adder_C____Active_Rdr = (
            2,
            WeaponsSu30.R_77M__AA_12_Adder_C____Active_Rdr,
        )
        Smoke_Generator___red = (2, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (2, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (2, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (2, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (2, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (2, Weapons.Smoke_Generator___orange)
        Smoke_Generator___Black = (2, WeaponsSu30.Smoke_Generator___Black)

    # ERRR <CLEAN>

    class Pylon3:
        R_73__AA_11_Archer____Infra_Red = (3, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            3,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            3,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            3,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            3,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27T1__AA_10_Alamo_B____Infra_Red = (
            3,
            WeaponsSu30.R_27T1__AA_10_Alamo_B____Infra_Red,
        )
        R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range = (
            3,
            WeaponsSu30.R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            3,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_27ET1__AA_10_Alamo_D____IR_Extended_Range = (
            3,
            WeaponsSu30.R_27ET1__AA_10_Alamo_D____IR_Extended_Range,
        )
        R_27EP1__AA_10_Alamo_F____Passive_Rdr_Extended_Range = (
            3,
            WeaponsSu30.R_27EP1__AA_10_Alamo_F____Passive_Rdr_Extended_Range,
        )
        R_27P1__AA_10_Alamo_E____Passive_Rdr = (
            3,
            WeaponsSu30.R_27P1__AA_10_Alamo_E____Passive_Rdr,
        )
        R_77__AA_12_Adder_Early____Active_Rdr = (
            3,
            WeaponsSu30.R_77__AA_12_Adder_Early____Active_Rdr,
        )
        R_77_1__AA_12_Adder_B____Active_Rdr = (
            3,
            WeaponsSu30.R_77_1__AA_12_Adder_B____Active_Rdr,
        )
        R_77M__AA_12_Adder_C____Active_Rdr = (
            3,
            WeaponsSu30.R_77M__AA_12_Adder_C____Active_Rdr,
        )
        R_77PD__AA_12_Adder____Active_Rdr_Ramjet = (
            3,
            WeaponsSu30.R_77PD__AA_12_Adder____Active_Rdr_Ramjet,
        )
        R_37M__AA_13_Axehead____Active_Rdr = (
            3,
            WeaponsSu30.R_37M__AA_13_Axehead____Active_Rdr,
        )
        Kh_31P__AS_17_Krypton____600kg = (3, WeaponsSu30.Kh_31P__AS_17_Krypton____600kg)
        Kh_36__AS_23____600kg_Grom_E1 = (3, WeaponsSu30.Kh_36__AS_23____600kg_Grom_E1)
        KH_38MTE__AS_23__IR_Guided = (3, WeaponsSu30.KH_38MTE__AS_23__IR_Guided)
        KH_38MLE__AS_23___Semi_Act_Laser = (
            3,
            WeaponsSu30.KH_38MLE__AS_23___Semi_Act_Laser,
        )
        Kh_38MAE__AS_23____500kg = (3, WeaponsSu30.Kh_38MAE__AS_23____500kg)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            3,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            3,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            3,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        # ERRR {JAS39_AGM_65K}
        Kh_59M__AS_18_Kazoo___930kg = (3, WeaponsSu30.Kh_59M__AS_18_Kazoo___930kg)
        Kh_59MK__AS_18_Kazoo____930kg = (3, WeaponsSu30.Kh_59MK__AS_18_Kazoo____930kg)
        Kh_31A__AS_17_Krypton____610kg = (3, WeaponsSu30.Kh_31A__AS_17_Krypton____610kg)
        Kh_35__AS_20_Kayak____520kg = (3, WeaponsSu30.Kh_35__AS_20_Kayak____520kg)
        Kh_35UE__AS_20_Kayak____520kg = (3, WeaponsSu30.Kh_35UE__AS_20_Kayak____520kg)
        Kh_31AD__AS_17_Krypton____610kg = (
            3,
            WeaponsSu30.Kh_31AD__AS_17_Krypton____610kg,
        )
        Kh_31PD__AS_17_Krypton____600kg = (
            3,
            WeaponsSu30.Kh_31PD__AS_17_Krypton____600kg,
        )
        Kh_59MK2__AS_22_Kazoo____700kg = (3, WeaponsSu30.Kh_59MK2__AS_22_Kazoo____700kg)
        KAB_500Kr___500kg_TV_Guided_Bomb = (3, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (3, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            3,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            3,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            3,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            3,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (3, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            3,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            3,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            3,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M54___474kg__freefall = (3, WeaponsSu30.FAB_500_M54___474kg__freefall)
        FAB_500_M62___474kg__freefall = (3, WeaponsSu30.FAB_500_M62___474kg__freefall)
        FAB_500M62_UMPK__500kg_Glide_Bomb = (
            3,
            WeaponsSu30.FAB_500M62_UMPK__500kg_Glide_Bomb,
        )
        FAB_250_M62___227kg__freefall = (3, WeaponsSu30.FAB_250_M62___227kg__freefall)
        FAB_500M62_NV__500kg_Parachute = (3, WeaponsSu30.FAB_500M62_NV__500kg_Parachute)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            3,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            3,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            3,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        _2_x_B_13L_pods___10_x_S_13_OF__122mm_UnGd_Rkts__Blast_Frag = (
            3,
            Weapons._2_x_B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            3,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange = (
            3,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8OFP2_MPP = (
            3,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8OFP2_MPP,
        )
        _2_x_S_25 = (3, Weapons._2_x_S_25)

    # ERRR <CLEAN>

    class Pylon4:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            4,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range = (
            4,
            WeaponsSu30.R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            4,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_77__AA_12_Adder_Early____Active_Rdr = (
            4,
            WeaponsSu30.R_77__AA_12_Adder_Early____Active_Rdr,
        )
        R_77_1__AA_12_Adder_B____Active_Rdr = (
            4,
            WeaponsSu30.R_77_1__AA_12_Adder_B____Active_Rdr,
        )
        R_77M__AA_12_Adder_C____Active_Rdr = (
            4,
            WeaponsSu30.R_77M__AA_12_Adder_C____Active_Rdr,
        )
        R_77PD__AA_12_Adder____Active_Rdr_Ramjet = (
            4,
            WeaponsSu30.R_77PD__AA_12_Adder____Active_Rdr_Ramjet,
        )
        R_37M__AA_13_Axehead____Active_Rdr = (
            4,
            WeaponsSu30.R_37M__AA_13_Axehead____Active_Rdr,
        )
        Kh_31P__AS_17_Krypton____600kg = (4, WeaponsSu30.Kh_31P__AS_17_Krypton____600kg)
        Kh_36__AS_23____600kg_Grom_E1 = (4, WeaponsSu30.Kh_36__AS_23____600kg_Grom_E1)
        KH_38MTE__AS_23__IR_Guided = (4, WeaponsSu30.KH_38MTE__AS_23__IR_Guided)
        KH_38MLE__AS_23___Semi_Act_Laser = (
            4,
            WeaponsSu30.KH_38MLE__AS_23___Semi_Act_Laser,
        )
        Kh_38MAE__AS_23____500kg = (4, WeaponsSu30.Kh_38MAE__AS_23____500kg)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            4,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            4,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            4,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_59M__AS_18_Kazoo___930kg = (4, WeaponsSu30.Kh_59M__AS_18_Kazoo___930kg)
        Kh_59MK__AS_18_Kazoo____930kg = (4, WeaponsSu30.Kh_59MK__AS_18_Kazoo____930kg)
        Kh_31A__AS_17_Krypton____610kg = (4, WeaponsSu30.Kh_31A__AS_17_Krypton____610kg)
        Kh_35__AS_20_Kayak____520kg = (4, WeaponsSu30.Kh_35__AS_20_Kayak____520kg)
        Kh_35UE__AS_20_Kayak____520kg = (4, WeaponsSu30.Kh_35UE__AS_20_Kayak____520kg)
        Kh_31AD__AS_17_Krypton____610kg = (
            4,
            WeaponsSu30.Kh_31AD__AS_17_Krypton____610kg,
        )
        Kh_31PD__AS_17_Krypton____600kg = (
            4,
            WeaponsSu30.Kh_31PD__AS_17_Krypton____600kg,
        )
        Kh_59MK2__AS_22_Kazoo____700kg = (4, WeaponsSu30.Kh_59MK2__AS_22_Kazoo____700kg)
        KAB_500Kr___500kg_TV_Guided_Bomb = (4, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (4, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_1500Kr___1500kg = (4, WeaponsSu30.KAB_1500Kr___1500kg)
        KAB_1500LG_PR___1500kg = (4, WeaponsSu30.KAB_1500LG_PR___1500kg)
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            4,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            4,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            4,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            4,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            4,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (4, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            4,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            4,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            4,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M54___474kg__freefall = (4, WeaponsSu30.FAB_500_M54___474kg__freefall)
        FAB_500_M62___474kg__freefall = (4, WeaponsSu30.FAB_500_M62___474kg__freefall)
        FAB_500M62_UMPK__500kg_Glide_Bomb = (
            4,
            WeaponsSu30.FAB_500M62_UMPK__500kg_Glide_Bomb,
        )
        FAB_250_M62___227kg__freefall = (4, WeaponsSu30.FAB_250_M62___227kg__freefall)
        FAB_500M62_NV__500kg_Parachute = (4, WeaponsSu30.FAB_500M62_NV__500kg_Parachute)
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            4,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            4,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            4,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD = (
            4,
            Weapons.MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            4,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )

    # ERRR <CLEAN>

    class Pylon5:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            5,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range = (
            5,
            WeaponsSu30.R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            5,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_77__AA_12_Adder_Early____Active_Rdr = (
            5,
            WeaponsSu30.R_77__AA_12_Adder_Early____Active_Rdr,
        )
        R_77_1__AA_12_Adder_B____Active_Rdr = (
            5,
            WeaponsSu30.R_77_1__AA_12_Adder_B____Active_Rdr,
        )
        R_77M__AA_12_Adder_C____Active_Rdr = (
            5,
            WeaponsSu30.R_77M__AA_12_Adder_C____Active_Rdr,
        )
        R_77PD__AA_12_Adder____Active_Rdr_Ramjet = (
            5,
            WeaponsSu30.R_77PD__AA_12_Adder____Active_Rdr_Ramjet,
        )
        R_37M__AA_13_Axehead____Active_Rdr = (
            5,
            WeaponsSu30.R_37M__AA_13_Axehead____Active_Rdr,
        )
        Kh_31P__AS_17_Krypton____600kg = (5, WeaponsSu30.Kh_31P__AS_17_Krypton____600kg)
        Kh_36__AS_23____600kg_Grom_E1 = (5, WeaponsSu30.Kh_36__AS_23____600kg_Grom_E1)
        KH_38MTE__AS_23__IR_Guided = (5, WeaponsSu30.KH_38MTE__AS_23__IR_Guided)
        KH_38MLE__AS_23___Semi_Act_Laser = (
            5,
            WeaponsSu30.KH_38MLE__AS_23___Semi_Act_Laser,
        )
        Kh_38MAE__AS_23____500kg = (5, WeaponsSu30.Kh_38MAE__AS_23____500kg)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            5,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            5,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            5,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_31A__AS_17_Krypton____610kg = (5, WeaponsSu30.Kh_31A__AS_17_Krypton____610kg)
        Kh_31AD__AS_17_Krypton____610kg = (
            5,
            WeaponsSu30.Kh_31AD__AS_17_Krypton____610kg,
        )
        Kh_31PD__AS_17_Krypton____600kg = (
            5,
            WeaponsSu30.Kh_31PD__AS_17_Krypton____600kg,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (5, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (5, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            5,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            5,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        P_50T___50kg_Practice_Bomb_LD = (5, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            5,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            5,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            5,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M54___474kg__freefall = (5, WeaponsSu30.FAB_500_M54___474kg__freefall)
        FAB_500_M62___474kg__freefall = (5, WeaponsSu30.FAB_500_M62___474kg__freefall)
        FAB_500M62_UMPK__500kg_Glide_Bomb = (
            5,
            WeaponsSu30.FAB_500M62_UMPK__500kg_Glide_Bomb,
        )
        FAB_250_M62___227kg__freefall = (5, WeaponsSu30.FAB_250_M62___227kg__freefall)
        FAB_500M62_NV__500kg_Parachute = (5, WeaponsSu30.FAB_500M62_NV__500kg_Parachute)
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            5,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            5,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            5,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            5,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )
        APK_9_POD = (5, WeaponsSu30.APK_9_POD)
        L_081_Fantasmagoria_ELINT_pod = (5, Weapons.L_081_Fantasmagoria_ELINT_pod)

    # ERRR <CLEAN>

    class Pylon6:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            6,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range = (
            6,
            WeaponsSu30.R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            6,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_77__AA_12_Adder_Early____Active_Rdr = (
            6,
            WeaponsSu30.R_77__AA_12_Adder_Early____Active_Rdr,
        )
        R_77_1__AA_12_Adder_B____Active_Rdr = (
            6,
            WeaponsSu30.R_77_1__AA_12_Adder_B____Active_Rdr,
        )
        R_77M__AA_12_Adder_C____Active_Rdr = (
            6,
            WeaponsSu30.R_77M__AA_12_Adder_C____Active_Rdr,
        )
        R_77PD__AA_12_Adder____Active_Rdr_Ramjet = (
            6,
            WeaponsSu30.R_77PD__AA_12_Adder____Active_Rdr_Ramjet,
        )
        R_37M__AA_13_Axehead____Active_Rdr = (
            6,
            WeaponsSu30.R_37M__AA_13_Axehead____Active_Rdr,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (6, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (6, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_1500Kr___1500kg = (6, WeaponsSu30.KAB_1500Kr___1500kg)
        KAB_1500LG_PR___1500kg = (6, WeaponsSu30.KAB_1500LG_PR___1500kg)
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            6,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            6,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            6,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            6,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            6,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        P_50T___50kg_Practice_Bomb_LD = (6, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            6,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            6,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            6,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M54___474kg__freefall = (6, WeaponsSu30.FAB_500_M54___474kg__freefall)
        FAB_500_M62___474kg__freefall = (6, WeaponsSu30.FAB_500_M62___474kg__freefall)
        FAB_500M62_UMPK__500kg_Glide_Bomb = (
            6,
            WeaponsSu30.FAB_500M62_UMPK__500kg_Glide_Bomb,
        )
        FAB_250_M62___227kg__freefall = (6, WeaponsSu30.FAB_250_M62___227kg__freefall)
        FAB_500M62_NV__500kg_Parachute = (6, WeaponsSu30.FAB_500M62_NV__500kg_Parachute)
        RN_244___260kg__Tactic_Nuclear_bomb = (
            6,
            WeaponsSu30.RN_244___260kg__Tactic_Nuclear_bomb,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            6,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            6,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            6,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            6,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )
        RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag = (
            6,
            Weapons.RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag,
        )
        RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP = (
            6,
            Weapons.RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP,
        )

    # ERRR <CLEAN>

    class Pylon7:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            7,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range = (
            7,
            WeaponsSu30.R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            7,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_77__AA_12_Adder_Early____Active_Rdr = (
            7,
            WeaponsSu30.R_77__AA_12_Adder_Early____Active_Rdr,
        )
        R_77_1__AA_12_Adder_B____Active_Rdr = (
            7,
            WeaponsSu30.R_77_1__AA_12_Adder_B____Active_Rdr,
        )
        R_77M__AA_12_Adder_C____Active_Rdr = (
            7,
            WeaponsSu30.R_77M__AA_12_Adder_C____Active_Rdr,
        )
        R_77PD__AA_12_Adder____Active_Rdr_Ramjet = (
            7,
            WeaponsSu30.R_77PD__AA_12_Adder____Active_Rdr_Ramjet,
        )
        R_37M__AA_13_Axehead____Active_Rdr = (
            7,
            WeaponsSu30.R_37M__AA_13_Axehead____Active_Rdr,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (7, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (7, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            7,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            7,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (7, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            7,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            7,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            7,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M54___474kg__freefall = (7, WeaponsSu30.FAB_500_M54___474kg__freefall)
        FAB_500_M62___474kg__freefall = (7, WeaponsSu30.FAB_500_M62___474kg__freefall)
        FAB_500M62_UMPK__500kg_Glide_Bomb = (
            7,
            WeaponsSu30.FAB_500M62_UMPK__500kg_Glide_Bomb,
        )
        FAB_250_M62___227kg__freefall = (7, WeaponsSu30.FAB_250_M62___227kg__freefall)
        FAB_500M62_NV__500kg_Parachute = (7, WeaponsSu30.FAB_500M62_NV__500kg_Parachute)
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            7,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            7,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            7,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            7,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            7,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            7,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )
        Smoke_Generator___red = (7, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (7, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (7, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (7, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (7, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (7, Weapons.Smoke_Generator___orange)
        Smoke_Generator___Black = (7, WeaponsSu30.Smoke_Generator___Black)
        RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag = (
            7,
            Weapons.RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag,
        )
        RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP = (
            7,
            Weapons.RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP,
        )

    # ERRR <CLEAN>

    class Pylon8:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            8,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range = (
            8,
            WeaponsSu30.R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            8,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_77__AA_12_Adder_Early____Active_Rdr = (
            8,
            WeaponsSu30.R_77__AA_12_Adder_Early____Active_Rdr,
        )
        R_77_1__AA_12_Adder_B____Active_Rdr = (
            8,
            WeaponsSu30.R_77_1__AA_12_Adder_B____Active_Rdr,
        )
        R_77M__AA_12_Adder_C____Active_Rdr = (
            8,
            WeaponsSu30.R_77M__AA_12_Adder_C____Active_Rdr,
        )
        R_77PD__AA_12_Adder____Active_Rdr_Ramjet = (
            8,
            WeaponsSu30.R_77PD__AA_12_Adder____Active_Rdr_Ramjet,
        )
        R_37M__AA_13_Axehead____Active_Rdr = (
            8,
            WeaponsSu30.R_37M__AA_13_Axehead____Active_Rdr,
        )
        Kh_31P__AS_17_Krypton____600kg = (8, WeaponsSu30.Kh_31P__AS_17_Krypton____600kg)
        Kh_36__AS_23____600kg_Grom_E1 = (8, WeaponsSu30.Kh_36__AS_23____600kg_Grom_E1)
        KH_38MTE__AS_23__IR_Guided = (8, WeaponsSu30.KH_38MTE__AS_23__IR_Guided)
        KH_38MLE__AS_23___Semi_Act_Laser = (
            8,
            WeaponsSu30.KH_38MLE__AS_23___Semi_Act_Laser,
        )
        Kh_38MAE__AS_23____500kg = (8, WeaponsSu30.Kh_38MAE__AS_23____500kg)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            8,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            8,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            8,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_31A__AS_17_Krypton____610kg = (8, WeaponsSu30.Kh_31A__AS_17_Krypton____610kg)
        Kh_31AD__AS_17_Krypton____610kg = (
            8,
            WeaponsSu30.Kh_31AD__AS_17_Krypton____610kg,
        )
        Kh_31PD__AS_17_Krypton____600kg = (
            8,
            WeaponsSu30.Kh_31PD__AS_17_Krypton____600kg,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (8, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (8, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            8,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            8,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        P_50T___50kg_Practice_Bomb_LD = (8, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            8,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            8,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            8,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M54___474kg__freefall = (8, WeaponsSu30.FAB_500_M54___474kg__freefall)
        FAB_500_M62___474kg__freefall = (8, WeaponsSu30.FAB_500_M62___474kg__freefall)
        FAB_500M62_UMPK__500kg_Glide_Bomb = (
            8,
            WeaponsSu30.FAB_500M62_UMPK__500kg_Glide_Bomb,
        )
        FAB_250_M62___227kg__freefall = (8, WeaponsSu30.FAB_250_M62___227kg__freefall)
        FAB_500M62_NV__500kg_Parachute = (8, WeaponsSu30.FAB_500M62_NV__500kg_Parachute)
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            8,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            8,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            8,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            8,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )

    # ERRR <CLEAN>

    class Pylon9:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            9,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range = (
            9,
            WeaponsSu30.R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            9,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_77__AA_12_Adder_Early____Active_Rdr = (
            9,
            WeaponsSu30.R_77__AA_12_Adder_Early____Active_Rdr,
        )
        R_77_1__AA_12_Adder_B____Active_Rdr = (
            9,
            WeaponsSu30.R_77_1__AA_12_Adder_B____Active_Rdr,
        )
        R_77M__AA_12_Adder_C____Active_Rdr = (
            9,
            WeaponsSu30.R_77M__AA_12_Adder_C____Active_Rdr,
        )
        R_77PD__AA_12_Adder____Active_Rdr_Ramjet = (
            9,
            WeaponsSu30.R_77PD__AA_12_Adder____Active_Rdr_Ramjet,
        )
        R_37M__AA_13_Axehead____Active_Rdr = (
            9,
            WeaponsSu30.R_37M__AA_13_Axehead____Active_Rdr,
        )
        Kh_31P__AS_17_Krypton____600kg = (9, WeaponsSu30.Kh_31P__AS_17_Krypton____600kg)
        Kh_36__AS_23____600kg_Grom_E1 = (9, WeaponsSu30.Kh_36__AS_23____600kg_Grom_E1)
        KH_38MTE__AS_23__IR_Guided = (9, WeaponsSu30.KH_38MTE__AS_23__IR_Guided)
        KH_38MLE__AS_23___Semi_Act_Laser = (
            9,
            WeaponsSu30.KH_38MLE__AS_23___Semi_Act_Laser,
        )
        Kh_38MAE__AS_23____500kg = (9, WeaponsSu30.Kh_38MAE__AS_23____500kg)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            9,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            9,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            9,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_59M__AS_18_Kazoo___930kg = (9, WeaponsSu30.Kh_59M__AS_18_Kazoo___930kg)
        Kh_59MK__AS_18_Kazoo____930kg = (9, WeaponsSu30.Kh_59MK__AS_18_Kazoo____930kg)
        Kh_31A__AS_17_Krypton____610kg = (9, WeaponsSu30.Kh_31A__AS_17_Krypton____610kg)
        Kh_35__AS_20_Kayak____520kg = (9, WeaponsSu30.Kh_35__AS_20_Kayak____520kg)
        Kh_35UE__AS_20_Kayak____520kg = (9, WeaponsSu30.Kh_35UE__AS_20_Kayak____520kg)
        Kh_31AD__AS_17_Krypton____610kg = (
            9,
            WeaponsSu30.Kh_31AD__AS_17_Krypton____610kg,
        )
        Kh_31PD__AS_17_Krypton____600kg = (
            9,
            WeaponsSu30.Kh_31PD__AS_17_Krypton____600kg,
        )
        Kh_59MK2__AS_22_Kazoo____700kg = (9, WeaponsSu30.Kh_59MK2__AS_22_Kazoo____700kg)
        KAB_500Kr___500kg_TV_Guided_Bomb = (9, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (9, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_1500Kr___1500kg = (9, WeaponsSu30.KAB_1500Kr___1500kg)
        KAB_1500LG_PR___1500kg = (9, WeaponsSu30.KAB_1500LG_PR___1500kg)
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            9,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            9,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            9,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            9,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            9,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (9, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            9,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            9,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            9,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M54___474kg__freefall = (9, WeaponsSu30.FAB_500_M54___474kg__freefall)
        FAB_500_M62___474kg__freefall = (9, WeaponsSu30.FAB_500_M62___474kg__freefall)
        FAB_500M62_UMPK__500kg_Glide_Bomb = (
            9,
            WeaponsSu30.FAB_500M62_UMPK__500kg_Glide_Bomb,
        )
        # ERRR {DIS_UMPK_FAB_5002}
        FAB_250_M62___227kg__freefall = (9, WeaponsSu30.FAB_250_M62___227kg__freefall)
        FAB_500M62_NV__500kg_Parachute = (9, WeaponsSu30.FAB_500M62_NV__500kg_Parachute)
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            9,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            9,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            9,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD = (
            9,
            Weapons.MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            9,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )

    # ERRR <CLEAN>

    class Pylon10:
        R_73__AA_11_Archer____Infra_Red = (10, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            10,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            10,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            10,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            10,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27T1__AA_10_Alamo_B____Infra_Red = (
            10,
            WeaponsSu30.R_27T1__AA_10_Alamo_B____Infra_Red,
        )
        R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range = (
            10,
            WeaponsSu30.R_27EA__AA_10_Alamo____Active_Rdr_Extended_Range,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            10,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_27ET1__AA_10_Alamo_D____IR_Extended_Range = (
            10,
            WeaponsSu30.R_27ET1__AA_10_Alamo_D____IR_Extended_Range,
        )
        R_27EP1__AA_10_Alamo_F____Passive_Rdr_Extended_Range = (
            10,
            WeaponsSu30.R_27EP1__AA_10_Alamo_F____Passive_Rdr_Extended_Range,
        )
        R_27P1__AA_10_Alamo_E____Passive_Rdr = (
            10,
            WeaponsSu30.R_27P1__AA_10_Alamo_E____Passive_Rdr,
        )
        R_77__AA_12_Adder_Early____Active_Rdr = (
            10,
            WeaponsSu30.R_77__AA_12_Adder_Early____Active_Rdr,
        )
        R_77_1__AA_12_Adder_B____Active_Rdr = (
            10,
            WeaponsSu30.R_77_1__AA_12_Adder_B____Active_Rdr,
        )
        R_77M__AA_12_Adder_C____Active_Rdr = (
            10,
            WeaponsSu30.R_77M__AA_12_Adder_C____Active_Rdr,
        )
        R_77PD__AA_12_Adder____Active_Rdr_Ramjet = (
            10,
            WeaponsSu30.R_77PD__AA_12_Adder____Active_Rdr_Ramjet,
        )
        R_37M__AA_13_Axehead____Active_Rdr = (
            10,
            WeaponsSu30.R_37M__AA_13_Axehead____Active_Rdr,
        )
        Kh_31P__AS_17_Krypton____600kg = (
            10,
            WeaponsSu30.Kh_31P__AS_17_Krypton____600kg,
        )
        Kh_36__AS_23____600kg_Grom_E1 = (10, WeaponsSu30.Kh_36__AS_23____600kg_Grom_E1)
        KH_38MTE__AS_23__IR_Guided = (10, WeaponsSu30.KH_38MTE__AS_23__IR_Guided)
        KH_38MLE__AS_23___Semi_Act_Laser = (
            10,
            WeaponsSu30.KH_38MLE__AS_23___Semi_Act_Laser,
        )
        Kh_38MAE__AS_23____500kg = (10, WeaponsSu30.Kh_38MAE__AS_23____500kg)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            10,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            10,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            10,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        # ERRR {JAS39_AGM_65H}
        Kh_59M__AS_18_Kazoo___930kg = (10, WeaponsSu30.Kh_59M__AS_18_Kazoo___930kg)
        Kh_59MK__AS_18_Kazoo____930kg = (10, WeaponsSu30.Kh_59MK__AS_18_Kazoo____930kg)
        Kh_31A__AS_17_Krypton____610kg = (
            10,
            WeaponsSu30.Kh_31A__AS_17_Krypton____610kg,
        )
        Kh_35__AS_20_Kayak____520kg = (10, WeaponsSu30.Kh_35__AS_20_Kayak____520kg)
        Kh_35UE__AS_20_Kayak____520kg = (10, WeaponsSu30.Kh_35UE__AS_20_Kayak____520kg)
        Kh_31AD__AS_17_Krypton____610kg = (
            10,
            WeaponsSu30.Kh_31AD__AS_17_Krypton____610kg,
        )
        Kh_31PD__AS_17_Krypton____600kg = (
            10,
            WeaponsSu30.Kh_31PD__AS_17_Krypton____600kg,
        )
        Kh_59MK2__AS_22_Kazoo____700kg = (
            10,
            WeaponsSu30.Kh_59MK2__AS_22_Kazoo____700kg,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (
            10,
            Weapons.KAB_500Kr___500kg_TV_Guided_Bomb,
        )
        KAB_500S___500kg__GPS_Guided = (10, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            10,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            10,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            10,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            10,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (10, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            10,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            10,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            10,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M54___474kg__freefall = (10, WeaponsSu30.FAB_500_M54___474kg__freefall)
        FAB_500_M62___474kg__freefall = (10, WeaponsSu30.FAB_500_M62___474kg__freefall)
        FAB_500M62_UMPK__500kg_Glide_Bomb = (
            10,
            WeaponsSu30.FAB_500M62_UMPK__500kg_Glide_Bomb,
        )
        FAB_250_M62___227kg__freefall = (10, WeaponsSu30.FAB_250_M62___227kg__freefall)
        FAB_500M62_NV__500kg_Parachute = (
            10,
            WeaponsSu30.FAB_500M62_NV__500kg_Parachute,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            10,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            10,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            10,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD = (
            10,
            Weapons.MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            10,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )
        _2_x_B_13L_pods___10_x_S_13_OF__122mm_UnGd_Rkts__Blast_Frag = (
            10,
            Weapons._2_x_B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            10,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange = (
            10,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8OFP2_MPP = (
            10,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8OFP2_MPP,
        )
        _2_x_S_25 = (10, Weapons._2_x_S_25)

    # ERRR <CLEAN>

    class Pylon11:
        R_73__AA_11_Archer____Infra_Red = (11, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            11,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            11,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            11,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        R_77__AA_12_Adder_Early____Active_Rdr = (
            11,
            WeaponsSu30.R_77__AA_12_Adder_Early____Active_Rdr,
        )
        R_77_1__AA_12_Adder_B____Active_Rdr = (
            11,
            WeaponsSu30.R_77_1__AA_12_Adder_B____Active_Rdr,
        )
        R_77M__AA_12_Adder_C____Active_Rdr = (
            11,
            WeaponsSu30.R_77M__AA_12_Adder_C____Active_Rdr,
        )
        Smoke_Generator___red = (11, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (11, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (11, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (11, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (11, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (11, Weapons.Smoke_Generator___orange)
        Smoke_Generator___Black = (11, WeaponsSu30.Smoke_Generator___Black)

    # ERRR <CLEAN>

    class Pylon12:
        R_73__AA_11_Archer____Infra_Red = (12, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            12,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            12,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            12,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        L005_Sorbtsiya_ECM_pod__right_ = (12, Weapons.L005_Sorbtsiya_ECM_pod__right_)
        SAP_518_ECM_Pod__Right_ = (12, WeaponsSu30.SAP_518_ECM_Pod__Right_)
        Smoke_Generator___red = (12, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (12, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (12, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (12, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (12, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (12, Weapons.Smoke_Generator___orange)
        Smoke_Generator___Black = (12, WeaponsSu30.Smoke_Generator___Black)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}

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


@planemod
class Su_30MKI_AG(PlaneType):
    id = "Su-30MKI-AG"
    flyable = True
    height = 5.932
    width = 14.7
    length = 21.935
    fuel_max = 9500
    max_speed = 2499.984
    chaff = 96
    flare = 96
    charge_total = 192
    chaff_charge_size = 1
    flare_charge_size = 1
    eplrs = True
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}

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
                1: 117,
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

    property_defaults: Dict[str, Any] = {
        "SoloFlight": False,
        "NetCrewControlPriority": 0,
        "HumanOrchestra": False,
        "HelmetMountedDevice": 1,
        "ShowLadders": True,
        "su30Chaff": 96,
        "su30Flare": 96,
    }

    class Properties:
        class SoloFlight:
            id = "SoloFlight"

        class NetCrewControlPriority:
            id = "NetCrewControlPriority"

            class Values:
                Pilot = 0
                WSO = 1
                Ask_Always = -1
                Equally_Responsible = -2

        class HumanOrchestra:
            id = "HumanOrchestra"

        class HelmetMountedDevice:
            id = "HelmetMountedDevice"

            class Values:
                Not_installed = 0
                SURA_Visor = 1
                NVG = 2

        class ShowLadders:
            id = "ShowLadders"

        class su30Chaff:
            id = "su30Chaff"

        class su30Flare:
            id = "su30Flare"

    properties = {
        "SoloFlight": UnitPropertyDescription(
            identifier="SoloFlight",
            control="checkbox",
            label="Solo Flight",
            player_only=True,
            default=False,
            weight_when_on=-80,
        ),
        "NetCrewControlPriority": UnitPropertyDescription(
            identifier="NetCrewControlPriority",
            control="comboList",
            label="Aircraft Control Priority",
            player_only=True,
            default=0,
            w_ctrl=150,
            values={
                0: "Pilot",
                1: "WSO",
                -1: "Ask Always",
                -2: "Equally Responsible",
            },
        ),
        "HumanOrchestra": UnitPropertyDescription(
            identifier="HumanOrchestra",
            control="checkbox",
            label="Disable Multicrew",
            player_only=True,
            default=False,
        ),
        "HelmetMountedDevice": UnitPropertyDescription(
            identifier="HelmetMountedDevice",
            control="comboList",
            label="Helmet Mounted Device",
            player_only=True,
            default=1,
            w_ctrl=150,
            values={
                0: "Not installed",
                1: "SURA Visor",
                2: "NVG",
            },
        ),
        "ShowLadders": UnitPropertyDescription(
            identifier="ShowLadders",
            control="checkbox",
            label="Show Ladders",
            default=True,
        ),
        "su30Chaff": UnitPropertyDescription(
            identifier="su30Chaff",
            control="spinbox",
            label="Chaff",
            player_only=True,
            minimum=0,
            maximum=192,
            default=96,
            dimension=" ",
        ),
        "su30Flare": UnitPropertyDescription(
            identifier="su30Flare",
            control="spinbox",
            label="Flare",
            player_only=True,
            minimum=0,
            maximum=192,
            default=96,
            dimension=" ",
        ),
    }

    livery_name = "SU-30MKI-AG"  # from type

    class Pylon1:
        R_73__AA_11_Archer____Infra_Red = (1, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            1,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            1,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            1,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        L005_Sorbtsiya_ECM_pod__left_ = (1, Weapons.L005_Sorbtsiya_ECM_pod__left_)
        SAP_518_ECM_Pod__Left_ = (1, WeaponsSu30.SAP_518_ECM_Pod__Left_)
        Smoke_Generator___red = (1, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (1, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (1, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (1, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (1, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (1, Weapons.Smoke_Generator___orange)

    class Pylon2:
        R_73__AA_11_Archer____Infra_Red = (2, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            2,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            2,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            2,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        ASTRA_Mk_1___Active_Rdr_AAM = (2, WeaponsSu30.ASTRA_Mk_1___Active_Rdr_AAM)
        I_Derby_ER___Active_Rdr_AAM = (2, WeaponsSu30.I_Derby_ER___Active_Rdr_AAM)
        RVV_AE__AA_12_Adder____Active_Rdr = (
            2,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            2,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Smoke_Generator___red = (2, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (2, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (2, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (2, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (2, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (2, Weapons.Smoke_Generator___orange)

    # ERRR <CLEAN>

    class Pylon3:
        R_73__AA_11_Archer____Infra_Red = (3, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            3,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            3,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            3,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            3,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27T1__AA_10_Alamo_B____Infra_Red = (
            3,
            WeaponsSu30.R_27T1__AA_10_Alamo_B____Infra_Red,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            3,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_27ET1__AA_10_Alamo_D____IR_Extended_Range = (
            3,
            WeaponsSu30.R_27ET1__AA_10_Alamo_D____IR_Extended_Range,
        )
        ASTRA_Mk_1___Active_Rdr_AAM = (3, WeaponsSu30.ASTRA_Mk_1___Active_Rdr_AAM)
        I_Derby_ER___Active_Rdr_AAM = (3, WeaponsSu30.I_Derby_ER___Active_Rdr_AAM)
        RVV_AE__AA_12_Adder____Active_Rdr = (
            3,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            3,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            3,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            3,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            3,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_59M__AS_18_Kazoo___930kg = (3, WeaponsSu30.Kh_59M__AS_18_Kazoo___930kg)
        Kh_59MK__AS_18_Kazoo____930kg = (3, WeaponsSu30.Kh_59MK__AS_18_Kazoo____930kg)
        Kh_31A__AS_17_Krypton____610kg = (3, WeaponsSu30.Kh_31A__AS_17_Krypton____610kg)
        Kh_31P__AS_17_Krypton____600kg = (3, WeaponsSu30.Kh_31P__AS_17_Krypton____600kg)
        Kh_35__AS_20_Kayak____520kg = (3, WeaponsSu30.Kh_35__AS_20_Kayak____520kg)
        Rudra_M1 = (3, WeaponsSu30.Rudra_M1)
        SAAW_POD = (3, WeaponsSu30.SAAW_POD)
        KAB_500Kr___500kg_TV_Guided_Bomb = (3, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (3, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            3,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            3,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            3,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            3,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (3, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            3,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            3,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            3,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            3,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        FAB_500_M54___474kg__freefall = (3, WeaponsSu30.FAB_500_M54___474kg__freefall)
        FAB_500_M62___474kg__freefall = (3, WeaponsSu30.FAB_500_M62___474kg__freefall)
        FAB_250_M62___227kg__freefall = (3, WeaponsSu30.FAB_250_M62___227kg__freefall)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            3,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            3,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )
        _2_x_B_13L_pods___10_x_S_13_OF__122mm_UnGd_Rkts__Blast_Frag = (
            3,
            Weapons._2_x_B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            3,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange = (
            3,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8OFP2_MPP = (
            3,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8OFP2_MPP,
        )
        _2_x_S_25 = (3, Weapons._2_x_S_25)

    # ERRR <CLEAN>

    class Pylon4:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            4,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            4,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        I_Derby_ER___Active_Rdr_AAM = (4, WeaponsSu30.I_Derby_ER___Active_Rdr_AAM)
        RVV_AE__AA_12_Adder____Active_Rdr = (
            4,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            4,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            4,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            4,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            4,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_59M__AS_18_Kazoo___930kg = (4, WeaponsSu30.Kh_59M__AS_18_Kazoo___930kg)
        Kh_59MK__AS_18_Kazoo____930kg = (4, WeaponsSu30.Kh_59MK__AS_18_Kazoo____930kg)
        Kh_31A__AS_17_Krypton____610kg = (4, WeaponsSu30.Kh_31A__AS_17_Krypton____610kg)
        Kh_31P__AS_17_Krypton____600kg = (4, WeaponsSu30.Kh_31P__AS_17_Krypton____600kg)
        Kh_35__AS_20_Kayak____520kg = (4, WeaponsSu30.Kh_35__AS_20_Kayak____520kg)
        Rudra_M1 = (4, WeaponsSu30.Rudra_M1)
        SAAW_POD = (4, WeaponsSu30.SAAW_POD)
        KAB_500Kr___500kg_TV_Guided_Bomb = (4, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (4, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_1500Kr___1500kg = (4, WeaponsSu30.KAB_1500Kr___1500kg)
        KAB_1500LG_PR___1500kg = (4, WeaponsSu30.KAB_1500LG_PR___1500kg)
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            4,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            4,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            4,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            4,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            4,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (4, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            4,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            4,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            4,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            4,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        FAB_500_M54___474kg__freefall = (4, WeaponsSu30.FAB_500_M54___474kg__freefall)
        FAB_500_M62___474kg__freefall = (4, WeaponsSu30.FAB_500_M62___474kg__freefall)
        FAB_250_M62___227kg__freefall = (4, WeaponsSu30.FAB_250_M62___227kg__freefall)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            4,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            4,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )

    # ERRR <CLEAN>

    class Pylon5:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            5,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            5,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        I_Derby_ER___Active_Rdr_AAM = (5, WeaponsSu30.I_Derby_ER___Active_Rdr_AAM)
        RVV_AE__AA_12_Adder____Active_Rdr = (
            5,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            5,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            5,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            5,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            5,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        Kh_31A__AS_17_Krypton____610kg = (5, WeaponsSu30.Kh_31A__AS_17_Krypton____610kg)
        Kh_31P__AS_17_Krypton____600kg = (5, WeaponsSu30.Kh_31P__AS_17_Krypton____600kg)
        Rudra_M1 = (5, WeaponsSu30.Rudra_M1)
        KAB_500Kr___500kg_TV_Guided_Bomb = (5, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (5, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            5,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            5,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        P_50T___50kg_Practice_Bomb_LD = (5, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            5,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            5,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            5,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            5,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        FAB_500_M54___474kg__freefall = (5, WeaponsSu30.FAB_500_M54___474kg__freefall)
        FAB_500_M62___474kg__freefall = (5, WeaponsSu30.FAB_500_M62___474kg__freefall)
        FAB_250_M62___227kg__freefall = (5, WeaponsSu30.FAB_250_M62___227kg__freefall)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            5,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            5,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )
        APK_9_POD = (5, WeaponsSu30.APK_9_POD)
        L_081_Fantasmagoria_ELINT_pod = (5, Weapons.L_081_Fantasmagoria_ELINT_pod)

    # ERRR <CLEAN>

    class Pylon6:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            6,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            6,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            6,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            6,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        I_Derby_ER___Active_Rdr_AAM = (6, WeaponsSu30.I_Derby_ER___Active_Rdr_AAM)
        # ERRR {BRAHMOS_AG}
        BRAHMOS_A_Ship = (6, WeaponsSu30.BRAHMOS_A_Ship)
        BRAHMOS_SEAD = (6, WeaponsSu30.BRAHMOS_SEAD)
        KAB_500Kr___500kg_TV_Guided_Bomb = (6, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (6, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_1500Kr___1500kg = (6, WeaponsSu30.KAB_1500Kr___1500kg)
        KAB_1500LG_PR___1500kg = (6, WeaponsSu30.KAB_1500LG_PR___1500kg)
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            6,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            6,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            6,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            6,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            6,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (6, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            6,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            6,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            6,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            6,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        FAB_500_M54___474kg__freefall = (6, WeaponsSu30.FAB_500_M54___474kg__freefall)
        FAB_500_M62___474kg__freefall = (6, WeaponsSu30.FAB_500_M62___474kg__freefall)
        FAB_250_M62___227kg__freefall = (6, WeaponsSu30.FAB_250_M62___227kg__freefall)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            6,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            6,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )
        RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag = (
            6,
            Weapons.RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag,
        )
        RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP = (
            6,
            Weapons.RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP,
        )
        EL_M_2060 = (6, WeaponsSu30.EL_M_2060)

    # ERRR <CLEAN>

    class Pylon7:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            7,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            7,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            7,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            7,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        I_Derby_ER___Active_Rdr_AAM = (7, WeaponsSu30.I_Derby_ER___Active_Rdr_AAM)
        KAB_500Kr___500kg_TV_Guided_Bomb = (7, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (7, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            7,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            7,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            7,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            7,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (7, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            7,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            7,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            7,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            7,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        FAB_500_M54___474kg__freefall = (7, WeaponsSu30.FAB_500_M54___474kg__freefall)
        FAB_500_M62___474kg__freefall = (7, WeaponsSu30.FAB_500_M62___474kg__freefall)
        FAB_250_M62___227kg__freefall = (7, WeaponsSu30.FAB_250_M62___227kg__freefall)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            7,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            7,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )
        Smoke_Generator___red = (7, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (7, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (7, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (7, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (7, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (7, Weapons.Smoke_Generator___orange)
        # ERRR <CLEAN>
        RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag = (
            7,
            Weapons.RBK_500U___126_x_OAB_2_5RT__500kg_CBU_HE_Frag,
        )
        RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP = (
            7,
            Weapons.RBK_500___268_x_PTAB_1M__500kg_CBU_Light_HEAT_AP,
        )

    class Pylon8:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            8,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            8,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            8,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            8,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        I_Derby_ER___Active_Rdr_AAM = (8, WeaponsSu30.I_Derby_ER___Active_Rdr_AAM)
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            8,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            8,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            8,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_31A__AS_17_Krypton____610kg = (8, WeaponsSu30.Kh_31A__AS_17_Krypton____610kg)
        Kh_31P__AS_17_Krypton____600kg = (8, WeaponsSu30.Kh_31P__AS_17_Krypton____600kg)
        Rudra_M1 = (8, WeaponsSu30.Rudra_M1)
        KAB_500Kr___500kg_TV_Guided_Bomb = (8, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (8, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            8,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            8,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        P_50T___50kg_Practice_Bomb_LD = (8, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            8,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            8,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            8,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            8,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        FAB_500_M54___474kg__freefall = (8, WeaponsSu30.FAB_500_M54___474kg__freefall)
        FAB_500_M62___474kg__freefall = (8, WeaponsSu30.FAB_500_M62___474kg__freefall)
        FAB_250_M62___227kg__freefall = (8, WeaponsSu30.FAB_250_M62___227kg__freefall)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            8,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            8,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )
        LITENING___Targeting_Pod = (8, WeaponsSu30.LITENING___Targeting_Pod)

    # ERRR <CLEAN>

    class Pylon9:
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            9,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            9,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        RVV_AE__AA_12_Adder____Active_Rdr = (
            9,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            9,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        I_Derby_ER___Active_Rdr_AAM = (9, WeaponsSu30.I_Derby_ER___Active_Rdr_AAM)
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            9,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            9,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            9,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_59M__AS_18_Kazoo___930kg = (9, WeaponsSu30.Kh_59M__AS_18_Kazoo___930kg)
        Kh_59MK__AS_18_Kazoo____930kg = (9, WeaponsSu30.Kh_59MK__AS_18_Kazoo____930kg)
        Kh_31A__AS_17_Krypton____610kg = (9, WeaponsSu30.Kh_31A__AS_17_Krypton____610kg)
        Kh_31P__AS_17_Krypton____600kg = (9, WeaponsSu30.Kh_31P__AS_17_Krypton____600kg)
        Kh_35__AS_20_Kayak____520kg = (9, WeaponsSu30.Kh_35__AS_20_Kayak____520kg)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            9,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            9,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        Rudra_M1 = (9, WeaponsSu30.Rudra_M1)
        SAAW_POD = (9, WeaponsSu30.SAAW_POD)
        KAB_500Kr___500kg_TV_Guided_Bomb = (9, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        KAB_500S___500kg__GPS_Guided = (9, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_1500Kr___1500kg = (9, WeaponsSu30.KAB_1500Kr___1500kg)
        KAB_1500LG_PR___1500kg = (9, WeaponsSu30.KAB_1500LG_PR___1500kg)
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            9,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            9,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            9,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (9, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            9,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            9,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            9,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            9,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        FAB_500_M54___474kg__freefall = (9, WeaponsSu30.FAB_500_M54___474kg__freefall)
        FAB_500_M62___474kg__freefall = (9, WeaponsSu30.FAB_500_M62___474kg__freefall)
        FAB_250_M62___227kg__freefall = (9, WeaponsSu30.FAB_250_M62___227kg__freefall)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            9,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            9,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )

    # ERRR <CLEAN>

    class Pylon10:
        R_73__AA_11_Archer____Infra_Red = (10, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            10,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            10,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            10,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        R_27R1__AA_10_Alamo_A____Semi_Act_Rdr = (
            10,
            WeaponsSu30.R_27R1__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27T1__AA_10_Alamo_B____Infra_Red = (
            10,
            WeaponsSu30.R_27T1__AA_10_Alamo_B____Infra_Red,
        )
        R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            10,
            WeaponsSu30.R_27ER1__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_27ET1__AA_10_Alamo_D____IR_Extended_Range = (
            10,
            WeaponsSu30.R_27ET1__AA_10_Alamo_D____IR_Extended_Range,
        )
        ASTRA_Mk_1___Active_Rdr_AAM = (10, WeaponsSu30.ASTRA_Mk_1___Active_Rdr_AAM)
        I_Derby_ER___Active_Rdr_AAM = (10, WeaponsSu30.I_Derby_ER___Active_Rdr_AAM)
        RVV_AE__AA_12_Adder____Active_Rdr = (
            10,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            10,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        KH_29L__AS_14_Kedge___Semi_Act_Laser = (
            10,
            WeaponsSu30.KH_29L__AS_14_Kedge___Semi_Act_Laser,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            10,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KH_29TE__AS_14_Kedge___TV_Guided = (
            10,
            WeaponsSu30.KH_29TE__AS_14_Kedge___TV_Guided,
        )
        Kh_59M__AS_18_Kazoo___930kg = (10, WeaponsSu30.Kh_59M__AS_18_Kazoo___930kg)
        Kh_59MK__AS_18_Kazoo____930kg = (10, WeaponsSu30.Kh_59MK__AS_18_Kazoo____930kg)
        Kh_31A__AS_17_Krypton____610kg = (
            10,
            WeaponsSu30.Kh_31A__AS_17_Krypton____610kg,
        )
        Kh_31P__AS_17_Krypton____600kg = (
            10,
            WeaponsSu30.Kh_31P__AS_17_Krypton____600kg,
        )
        Kh_35__AS_20_Kayak____520kg = (10, WeaponsSu30.Kh_35__AS_20_Kayak____520kg)
        Rudra_M1 = (10, WeaponsSu30.Rudra_M1)
        SAAW_POD = (10, WeaponsSu30.SAAW_POD)
        KAB_500Kr___500kg_TV_Guided_Bomb = (
            10,
            Weapons.KAB_500Kr___500kg_TV_Guided_Bomb,
        )
        KAB_500S___500kg__GPS_Guided = (10, WeaponsSu30.KAB_500S___500kg__GPS_Guided)
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            10,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        SAB_100MN___100_kg_Illumination_Bomb = (
            10,
            Weapons.SAB_100MN___100_kg_Illumination_Bomb,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            10,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            10,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        P_50T___50kg_Practice_Bomb_LD = (10, Weapons.P_50T___50kg_Practice_Bomb_LD)
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            10,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb = (
            10,
            Weapons.BetAB_500ShP___500kg_Concrete_Piercing_HD_w_booster_Bomb,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            10,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            10,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        FAB_500_M54___474kg__freefall = (10, WeaponsSu30.FAB_500_M54___474kg__freefall)
        FAB_500_M62___474kg__freefall = (10, WeaponsSu30.FAB_500_M62___474kg__freefall)
        FAB_250_M62___227kg__freefall = (10, WeaponsSu30.FAB_250_M62___227kg__freefall)
        MBD3_U6_68_with_6_x_FAB_250___250kg = (
            10,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_250___250kg,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg = (
            10,
            WeaponsSu30.MBD3_U6_68_with_6_x_FAB_100___100kg,
        )
        _2_x_B_13L_pods___10_x_S_13_OF__122mm_UnGd_Rkts__Blast_Frag = (
            10,
            Weapons._2_x_B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            10,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange = (
            10,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange,
        )
        _2_x_B_8M1___40_x_UnGd_Rkts__80_mm_S_8OFP2_MPP = (
            10,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8OFP2_MPP,
        )
        _2_x_S_25 = (10, Weapons._2_x_S_25)

    # ERRR <CLEAN>

    class Pylon11:
        R_73__AA_11_Archer____Infra_Red = (11, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            11,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            11,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            11,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        ASTRA_Mk_1___Active_Rdr_AAM = (11, WeaponsSu30.ASTRA_Mk_1___Active_Rdr_AAM)
        I_Derby_ER___Active_Rdr_AAM = (11, WeaponsSu30.I_Derby_ER___Active_Rdr_AAM)
        RVV_AE__AA_12_Adder____Active_Rdr = (
            11,
            WeaponsSu30.RVV_AE__AA_12_Adder____Active_Rdr,
        )
        RVV_SD__AA_12_Adder_B____Active_Rdr = (
            11,
            WeaponsSu30.RVV_SD__AA_12_Adder_B____Active_Rdr,
        )
        Smoke_Generator___red = (11, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (11, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (11, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (11, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (11, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (11, Weapons.Smoke_Generator___orange)

    # ERRR <CLEAN>

    class Pylon12:
        R_73__AA_11_Archer____Infra_Red = (12, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_73L__AA_11_Archer_L____Infra_Red = (
            12,
            WeaponsSu30.R_73L__AA_11_Archer_L____Infra_Red,
        )
        R_73M__AA_11_Archer_M____Infra_Red = (
            12,
            WeaponsSu30.R_73M__AA_11_Archer_M____Infra_Red,
        )
        RVV_MD2__AA_11_Archer_M2____Infra_Red = (
            12,
            WeaponsSu30.RVV_MD2__AA_11_Archer_M2____Infra_Red,
        )
        L005_Sorbtsiya_ECM_pod__right_ = (12, Weapons.L005_Sorbtsiya_ECM_pod__right_)
        SAP_518_ECM_Pod__Right_ = (12, WeaponsSu30.SAP_518_ECM_Pod__Right_)
        Smoke_Generator___red = (12, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (12, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (12, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (12, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (12, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (12, Weapons.Smoke_Generator___orange)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}

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
