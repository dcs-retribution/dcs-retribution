from typing import Set

from dcs import task
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

from game.modsupport import planemod
from pydcs_extensions.weapon_injector import inject_weapons


class WeaponsMiG31BM:

    Vympel_R_33__AA_9_Amos_ = {
        "clsid": "{R-33_mig31bm}",
        "name": "Vympel R-33 (AA-9 Amos)",
        "weight": 490,
    }
    Vympel_R_33S__AA_9_Amos_ = {
        "clsid": "{R-33S_mig31bm}",
        "name": "Vympel R-33S (AA-9 Amos)",
        "weight": 490,
    }
    Vympel_R_37M__AA_13_Axehead_ = {
        "clsid": "{R-37M_mig31bm}",
        "name": "Vympel R-37M (AA-13 Axehead)",
        "weight": 600,
    }
    Vympel_R_37__AA_13_Axehead_ = {
        "clsid": "{R-37_mig31bm}",
        "name": "Vympel R-37 (AA-13 Axehead)",
        "weight": 600,
    }
    Kh_31P__AS_17_Krypton_ = {
        "clsid": "{Kh-31_mig31bm}",
        "name": "Kh-31P (AS-17 Krypton)",
        "weight": 758,
    }


inject_weapons(WeaponsMiG31BM)


@planemod
class MiG_31BM(PlaneType):
    id = "MiG-31BM"
    flyable = True
    height = 5.15
    width = 13.64
    length = 22.69
    fuel_max = 17730
    max_speed = 3120.012
    chaff = 120
    flare = 100
    charge_total = 220
    chaff_charge_size = 1
    flare_charge_size = 1
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}

    livery_name = "MIG-31BM"  # from type

    class Pylon1:
        R_73__AA_11_Archer____Infra_Red = (1, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_77__AA_12_Adder____Active_Rdr = (1, Weapons.R_77__AA_12_Adder____Active_Rdr)

    class Pylon2:
        R_73__AA_11_Archer____Infra_Red = (2, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_77__AA_12_Adder____Active_Rdr = (2, Weapons.R_77__AA_12_Adder____Active_Rdr)
        Vympel_R_37M__AA_13_Axehead_ = (2, WeaponsMiG31BM.Vympel_R_37M__AA_13_Axehead_)
        Vympel_R_37__AA_13_Axehead_ = (2, WeaponsMiG31BM.Vympel_R_37__AA_13_Axehead_)
        Vympel_R_33S__AA_9_Amos_ = (2, WeaponsMiG31BM.Vympel_R_33S__AA_9_Amos_)
        Vympel_R_33__AA_9_Amos_ = (2, WeaponsMiG31BM.Vympel_R_33__AA_9_Amos_)
        R_40RD__AA_6_Acrid____Semi_Act_Rdr = (
            2,
            Weapons.R_40RD__AA_6_Acrid____Semi_Act_Rdr,
        )
        R_40TD__AA_6_Acrid____Infra_Red = (2, Weapons.R_40TD__AA_6_Acrid____Infra_Red)
        APU_60_2M_with_2_x_R_60M__AA_8_Aphid_B____IR_AAM__ = (
            2,
            Weapons.APU_60_2M_with_2_x_R_60M__AA_8_Aphid_B____IR_AAM__,
        )
        R_27ET__AA_10_Alamo_D____IR_Extended_Range = (
            2,
            Weapons.R_27ET__AA_10_Alamo_D____IR_Extended_Range,
        )
        R_27ER__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            2,
            Weapons.R_27ER__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        Fuel_tank_3000L = (2, Weapons.Fuel_tank_3000L)
        Fuel_tank_2000L = (2, Weapons.Fuel_tank_2000L)
        Kh_31P__AS_17_Krypton_ = (2, WeaponsMiG31BM.Kh_31P__AS_17_Krypton_)

    class Pylon3:
        Vympel_R_37M__AA_13_Axehead_ = (3, WeaponsMiG31BM.Vympel_R_37M__AA_13_Axehead_)
        Vympel_R_37__AA_13_Axehead_ = (3, WeaponsMiG31BM.Vympel_R_37__AA_13_Axehead_)
        Vympel_R_33S__AA_9_Amos_ = (3, WeaponsMiG31BM.Vympel_R_33S__AA_9_Amos_)
        Vympel_R_33__AA_9_Amos_ = (3, WeaponsMiG31BM.Vympel_R_33__AA_9_Amos_)

    class Pylon4:
        Vympel_R_37M__AA_13_Axehead_ = (4, WeaponsMiG31BM.Vympel_R_37M__AA_13_Axehead_)
        Vympel_R_37__AA_13_Axehead_ = (4, WeaponsMiG31BM.Vympel_R_37__AA_13_Axehead_)
        Vympel_R_33S__AA_9_Amos_ = (4, WeaponsMiG31BM.Vympel_R_33S__AA_9_Amos_)
        Vympel_R_33__AA_9_Amos_ = (4, WeaponsMiG31BM.Vympel_R_33__AA_9_Amos_)

    class Pylon5:
        Vympel_R_37M__AA_13_Axehead_ = (5, WeaponsMiG31BM.Vympel_R_37M__AA_13_Axehead_)
        Vympel_R_37__AA_13_Axehead_ = (5, WeaponsMiG31BM.Vympel_R_37__AA_13_Axehead_)
        Vympel_R_33S__AA_9_Amos_ = (5, WeaponsMiG31BM.Vympel_R_33S__AA_9_Amos_)
        Vympel_R_33__AA_9_Amos_ = (5, WeaponsMiG31BM.Vympel_R_33__AA_9_Amos_)

    class Pylon6:
        Vympel_R_37M__AA_13_Axehead_ = (6, WeaponsMiG31BM.Vympel_R_37M__AA_13_Axehead_)
        Vympel_R_37__AA_13_Axehead_ = (6, WeaponsMiG31BM.Vympel_R_37__AA_13_Axehead_)
        Vympel_R_33S__AA_9_Amos_ = (6, WeaponsMiG31BM.Vympel_R_33S__AA_9_Amos_)
        Vympel_R_33__AA_9_Amos_ = (6, WeaponsMiG31BM.Vympel_R_33__AA_9_Amos_)

    class Pylon7:
        R_73__AA_11_Archer____Infra_Red = (7, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_77__AA_12_Adder____Active_Rdr = (7, Weapons.R_77__AA_12_Adder____Active_Rdr)
        Vympel_R_37M__AA_13_Axehead_ = (7, WeaponsMiG31BM.Vympel_R_37M__AA_13_Axehead_)
        Vympel_R_37__AA_13_Axehead_ = (7, WeaponsMiG31BM.Vympel_R_37__AA_13_Axehead_)
        Vympel_R_33S__AA_9_Amos_ = (7, WeaponsMiG31BM.Vympel_R_33S__AA_9_Amos_)
        Vympel_R_33__AA_9_Amos_ = (7, WeaponsMiG31BM.Vympel_R_33__AA_9_Amos_)
        R_40RD__AA_6_Acrid____Semi_Act_Rdr = (
            7,
            Weapons.R_40RD__AA_6_Acrid____Semi_Act_Rdr,
        )
        R_40TD__AA_6_Acrid____Infra_Red = (7, Weapons.R_40TD__AA_6_Acrid____Infra_Red)
        APU_60_2M_with_2_x_R_60M__AA_8_Aphid_B____IR_AAM___ = (
            7,
            Weapons.APU_60_2M_with_2_x_R_60M__AA_8_Aphid_B____IR_AAM___,
        )
        R_27ET__AA_10_Alamo_D____IR_Extended_Range = (
            7,
            Weapons.R_27ET__AA_10_Alamo_D____IR_Extended_Range,
        )
        R_27ER__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            7,
            Weapons.R_27ER__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        Fuel_tank_3000L = (7, Weapons.Fuel_tank_3000L)
        Fuel_tank_2000L = (7, Weapons.Fuel_tank_2000L)
        Kh_31P__AS_17_Krypton_ = (7, WeaponsMiG31BM.Kh_31P__AS_17_Krypton_)

    class Pylon8:
        R_73__AA_11_Archer____Infra_Red = (8, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_77__AA_12_Adder____Active_Rdr = (8, Weapons.R_77__AA_12_Adder____Active_Rdr)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8}

    tasks = [
        task.CAP,
        task.Intercept,
        task.Escort,
        task.FighterSweep,
        task.Reconnaissance,
        task.GroundAttack,
        task.AntishipStrike,
        task.SEAD,
    ]
    task_default = task.CAP
