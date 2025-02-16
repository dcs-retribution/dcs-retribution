# Requires Ukraine Military Assets for DCS by Currenthill:
# https://www.currenthill.com/ukraine
#


from typing import Set, Dict, Any

from dcs import unittype, task
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

from game.modsupport import (
    planemod,
    vehiclemod,
)
from pydcs_extensions.weapon_injector import inject_weapons


# Weapons
class WeaponsUKR:
    CH_AASM_250_PGM = {
        "clsid": "{CH_AASM250}",
        "name": "[CH] AASM 250 PGM",
        "weight": 340,
    }
    CH_Storm_Shadow_ALCM = {
        "clsid": "{SU24MU_STORMSHADOW}",
        "name": "[CH] Storm Shadow ALCM",
        "weight": 1300,
    }
    CH_Taurus_KEPD_350_ALCM = {
        "clsid": "{SU24MU_KEPD350}",
        "name": "[CH] Taurus KEPD-350 ALCM",
        "weight": 1400,
    }
    ADM_160B_MALD_x_3___Miniature_Air_Launched_Decoy = {
        "clsid": "{MIG29MU2_BRU_42A_x3_ADM_160B}",
        "name": "ADM-160B MALD x 3 - Miniature Air-Launched Decoy",
        "weight": 500.8,
    }
    ADM_160B_MALD___Miniature_Air_Launched_Decoy = {
        "clsid": "{MiG-29MU2_ADM-160B}",
        "name": "ADM-160B MALD - Miniature Air-Launched Decoy",
        "weight": 150,
    }
    ADM_160B_MALD___Miniature_Air_Launched_Decoy_ = {
        "clsid": "{MiG-29MU2_ADM-160B_LAU118}",
        "name": "ADM-160B MALD - Miniature Air-Launched Decoy",
        "weight": 150,
    }
    JDAM_ER___450_kg_GPS_Guided_Mk_83_GP_bomb = {
        "clsid": "{MIG29MU2_JDAM-ER}",
        "name": "JDAM-ER - 450 kg GPS Guided Mk-83 GP bomb",
        "weight": 934,
    }


inject_weapons(WeaponsUKR)


# Armor
@vehiclemod
class T84_OplotM(unittype.VehicleType):
    id = "T84_OplotM"
    name = "[CH] T-84 Oplot-M MBT"
    detection_range = 8000
    threat_range = 5000
    air_weapon_dist = 5000
    eplrs = True


@vehiclemod
class BTR_4(unittype.VehicleType):
    id = "BTR-4"
    name = "[CH] BTR-4 IFV"
    detection_range = 0
    threat_range = 5000
    air_weapon_dist = 5000
    eplrs = True


@vehiclemod
class CH_T64BV(unittype.VehicleType):
    id = "CH_T64BV"
    name = "[CH] T-64BV MBT"
    detection_range = 5000
    threat_range = 4000
    air_weapon_dist = 4000
    eplrs = True


@vehiclemod
class CH_Kozak5(unittype.VehicleType):
    id = "CH_Kozak5"
    name = "[CH] Kozak-5 APC"
    detection_range = 0
    threat_range = 1800
    air_weapon_dist = 1800
    eplrs = True


@vehiclemod
class CH_KrAZSpartan(unittype.VehicleType):
    id = "CH_KrAZSpartan"
    name = "[CH] KrAZ Spartan APC"
    detection_range = 0
    threat_range = 1800
    air_weapon_dist = 1800
    eplrs = True


@vehiclemod
class CH_BRDM2L1(unittype.VehicleType):
    id = "CH_BRDM2L1"
    name = "[CH] BRDM-2L1 ARV"
    detection_range = 0
    threat_range = 2000
    air_weapon_dist = 2000
    eplrs = True


# Infantry
@vehiclemod
class CH_Alligator_Sniper(unittype.VehicleType):
    id = "CH_Alligator_Sniper"
    name = "[CH] Alligator Sniper AMR"
    detection_range = 5000
    threat_range = 3000
    air_weapon_dist = 3000
    eplrs = True


@vehiclemod
class CH_Stugna_P(unittype.VehicleType):
    id = "CH_Stugna_P"
    name = "[CH] Stugna-P ATGM"
    detection_range = 5500
    threat_range = 5500
    air_weapon_dist = 5500
    eplrs = True


# Logistics
@vehiclemod
class CH_KrAZ6322(unittype.VehicleType):
    id = "CH_KrAZ6322"
    name = "[CH] KrAZ-6322 Truck"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


# Planes
@planemod
class Su_24MU(PlaneType):
    id = "Su-24MU"
    height = 4.97
    width = 17.64
    length = 24.53
    fuel_max = 11700
    max_speed = 1699.2
    chaff = 96
    flare = 96
    charge_total = 192
    chaff_charge_size = 1
    flare_charge_size = 1

    livery_name = "SU-24MU"  # from type

    class Pylon1:
        R_60M__AA_8_Aphid_B____IR_AAM = (1, Weapons.R_60M__AA_8_Aphid_B____IR_AAM)
        R_73__AA_11_Archer____Infra_Red = (1, Weapons.R_73__AA_11_Archer____Infra_Red)
        MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD = (
            1,
            Weapons.MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD,
        )
        UB_32A___32_x_UnGd_Rkts__57_mm_S_5KO_HEAT_Frag = (
            1,
            Weapons.UB_32A___32_x_UnGd_Rkts__57_mm_S_5KO_HEAT_Frag,
        )
        B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            1,
            Weapons.B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        FAB_250___250kg_GP_Bomb_LD = (1, Weapons.FAB_250___250kg_GP_Bomb_LD)
        B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation = (
            1,
            Weapons.B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation,
        )
        APU_68___S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk_ = (
            1,
            Weapons.APU_68___S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk_,
        )
        O_25___1_x_UnGd_Rkts__340_mm_S_25_OFM_Hardened_Target_Penetrator = (
            1,
            Weapons.O_25___1_x_UnGd_Rkts__340_mm_S_25_OFM_Hardened_Target_Penetrator,
        )
        Kh_25ML__AS_10_Karen____300kg__ASM__Semi_Act_Laser_ = (
            1,
            Weapons.Kh_25ML__AS_10_Karen____300kg__ASM__Semi_Act_Laser_,
        )
        CH_AASM_250_PGM = (1, Weapons.CH_AASM_250_PGM)

    class Pylon2:
        MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD = (
            2,
            Weapons.MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_ = (
            2,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_,
        )
        Kh_25ML__AS_10_Karen____300kg__ASM__Semi_Act_Laser_ = (
            2,
            Weapons.Kh_25ML__AS_10_Karen____300kg__ASM__Semi_Act_Laser_,
        )
        FAB_250___250kg_GP_Bomb_LD = (2, Weapons.FAB_250___250kg_GP_Bomb_LD)
        FAB_500_M_62___500kg_GP_Bomb_LD = (2, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        KAB_500Kr___500kg_TV_Guided_Bomb = (2, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        UB_32A___32_x_UnGd_Rkts__57_mm_S_5KO_HEAT_Frag = (
            2,
            Weapons.UB_32A___32_x_UnGd_Rkts__57_mm_S_5KO_HEAT_Frag,
        )
        B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            2,
            Weapons.B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation = (
            2,
            Weapons.B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation,
        )
        APU_68___S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk_ = (
            2,
            Weapons.APU_68___S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk_,
        )
        O_25___1_x_UnGd_Rkts__340_mm_S_25_OFM_Hardened_Target_Penetrator = (
            2,
            Weapons.O_25___1_x_UnGd_Rkts__340_mm_S_25_OFM_Hardened_Target_Penetrator,
        )
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            2,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        Fuel_tank_3000L = (2, Weapons.Fuel_tank_3000L)
        CH_Storm_Shadow_ALCM = (2, Weapons.CH_Storm_Shadow_ALCM)
        CH_Taurus_KEPD_350_ALCM = (2, Weapons.CH_Taurus_KEPD_350_ALCM)
        CH_AASM_250_PGM = (2, Weapons.CH_AASM_250_PGM)

    class Pylon3:
        MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD = (
            3,
            Weapons.MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD,
        )
        FAB_250___250kg_GP_Bomb_LD = (3, Weapons.FAB_250___250kg_GP_Bomb_LD)
        FAB_500_M_62___500kg_GP_Bomb_LD = (3, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        KAB_500Kr___500kg_TV_Guided_Bomb = (3, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        UB_32A___32_x_UnGd_Rkts__57_mm_S_5KO_HEAT_Frag = (
            3,
            Weapons.UB_32A___32_x_UnGd_Rkts__57_mm_S_5KO_HEAT_Frag,
        )
        B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            3,
            Weapons.B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        APU_68___S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk_ = (
            3,
            Weapons.APU_68___S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk_,
        )
        CH_AASM_250_PGM = (3, Weapons.CH_AASM_250_PGM)

    class Pylon4:
        MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD = (
            4,
            Weapons.MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD,
        )
        FAB_250___250kg_GP_Bomb_LD = (4, Weapons.FAB_250___250kg_GP_Bomb_LD)
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            4,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        CH_AASM_250_PGM = (4, Weapons.CH_AASM_250_PGM)

    class Pylon5:
        Fuel_tank_2000L = (5, Weapons.Fuel_tank_2000L)
        L_081_Fantasmagoria_ELINT_pod = (5, Weapons.L_081_Fantasmagoria_ELINT_pod)
        FAB_250___250kg_GP_Bomb_LD = (5, Weapons.FAB_250___250kg_GP_Bomb_LD)

    class Pylon6:
        MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD = (
            6,
            Weapons.MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD,
        )
        FAB_250___250kg_GP_Bomb_LD = (6, Weapons.FAB_250___250kg_GP_Bomb_LD)
        FAB_500_M_62___500kg_GP_Bomb_LD = (6, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        KAB_500Kr___500kg_TV_Guided_Bomb = (6, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        UB_32A___32_x_UnGd_Rkts__57_mm_S_5KO_HEAT_Frag = (
            6,
            Weapons.UB_32A___32_x_UnGd_Rkts__57_mm_S_5KO_HEAT_Frag,
        )
        B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            6,
            Weapons.B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        APU_68___S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk_ = (
            6,
            Weapons.APU_68___S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk_,
        )
        CH_AASM_250_PGM = (6, Weapons.CH_AASM_250_PGM)

    class Pylon7:
        MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD = (
            7,
            Weapons.MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_ = (
            7,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_,
        )
        Kh_25ML__AS_10_Karen____300kg__ASM__Semi_Act_Laser_ = (
            7,
            Weapons.Kh_25ML__AS_10_Karen____300kg__ASM__Semi_Act_Laser_,
        )
        FAB_250___250kg_GP_Bomb_LD = (7, Weapons.FAB_250___250kg_GP_Bomb_LD)
        FAB_500_M_62___500kg_GP_Bomb_LD = (7, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        KAB_500Kr___500kg_TV_Guided_Bomb = (7, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        UB_32A___32_x_UnGd_Rkts__57_mm_S_5KO_HEAT_Frag = (
            7,
            Weapons.UB_32A___32_x_UnGd_Rkts__57_mm_S_5KO_HEAT_Frag,
        )
        B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            7,
            Weapons.B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation = (
            7,
            Weapons.B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation,
        )
        APU_68___S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk_ = (
            7,
            Weapons.APU_68___S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk_,
        )
        O_25___1_x_UnGd_Rkts__340_mm_S_25_OFM_Hardened_Target_Penetrator = (
            7,
            Weapons.O_25___1_x_UnGd_Rkts__340_mm_S_25_OFM_Hardened_Target_Penetrator,
        )
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            7,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        Fuel_tank_3000L = (7, Weapons.Fuel_tank_3000L)
        CH_Storm_Shadow_ALCM = (7, Weapons.CH_Storm_Shadow_ALCM)
        CH_Taurus_KEPD_350_ALCM = (7, Weapons.CH_Taurus_KEPD_350_ALCM)
        CH_AASM_250_PGM = (7, Weapons.CH_AASM_250_PGM)

    class Pylon8:
        R_60M__AA_8_Aphid_B____IR_AAM = (8, Weapons.R_60M__AA_8_Aphid_B____IR_AAM)
        R_73__AA_11_Archer____Infra_Red = (8, Weapons.R_73__AA_11_Archer____Infra_Red)
        MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD = (
            8,
            Weapons.MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD,
        )
        UB_32A___32_x_UnGd_Rkts__57_mm_S_5KO_HEAT_Frag = (
            8,
            Weapons.UB_32A___32_x_UnGd_Rkts__57_mm_S_5KO_HEAT_Frag,
        )
        B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            8,
            Weapons.B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        FAB_250___250kg_GP_Bomb_LD = (8, Weapons.FAB_250___250kg_GP_Bomb_LD)
        B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation = (
            8,
            Weapons.B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation,
        )
        APU_68___S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk_ = (
            8,
            Weapons.APU_68___S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk_,
        )
        O_25___1_x_UnGd_Rkts__340_mm_S_25_OFM_Hardened_Target_Penetrator = (
            8,
            Weapons.O_25___1_x_UnGd_Rkts__340_mm_S_25_OFM_Hardened_Target_Penetrator,
        )
        Kh_25ML__AS_10_Karen____300kg__ASM__Semi_Act_Laser_ = (
            8,
            Weapons.Kh_25ML__AS_10_Karen____300kg__ASM__Semi_Act_Laser_,
        )
        CH_AASM_250_PGM = (8, Weapons.CH_AASM_250_PGM)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8}

    tasks = [
        task.Reconnaissance,
        task.GroundAttack,
        task.CAS,
        task.AFAC,
        task.RunwayAttack,
        task.AntishipStrike,
        task.SEAD,
        task.PinpointStrike,
    ]
    task_default = task.GroundAttack


@planemod
class MiG_29MU2(PlaneType):
    id = "MiG-29MU2"
    height = 4.73
    width = 11.36
    length = 20.32
    fuel_max = 3493
    max_speed = 2450.16
    chaff = 30
    flare = 30
    charge_total = 60
    chaff_charge_size = 1
    flare_charge_size = 1
    eplrs = True
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}

    livery_name = "MIG-29MU2"  # from type

    class Pylon1:
        R_73__AA_11_Archer____Infra_Red = (1, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_60M__AA_8_Aphid_B____IR_AAM = (1, Weapons.R_60M__AA_8_Aphid_B____IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (1, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9M_Sidewinder_IR_AAM = (1, Weapons.AIM_9M_Sidewinder_IR_AAM)
        R_27ER__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            1,
            Weapons.R_27ER__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_27ET__AA_10_Alamo_D____IR_Extended_Range = (
            1,
            Weapons.R_27ET__AA_10_Alamo_D____IR_Extended_Range,
        )
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            1,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            1,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )

    # ERRR <CLEAN>

    class Pylon2:
        R_73__AA_11_Archer____Infra_Red = (2, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_60M__AA_8_Aphid_B____IR_AAM = (2, Weapons.R_60M__AA_8_Aphid_B____IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (2, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9M_Sidewinder_IR_AAM = (2, Weapons.AIM_9M_Sidewinder_IR_AAM)
        R_27ER__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            2,
            Weapons.R_27ER__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_27ET__AA_10_Alamo_D____IR_Extended_Range = (
            2,
            Weapons.R_27ET__AA_10_Alamo_D____IR_Extended_Range,
        )
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            2,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            2,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            2,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (2, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        ADM_160B_MALD___Miniature_Air_Launched_Decoy_ = (
            2,
            Weapons.ADM_160B_MALD___Miniature_Air_Launched_Decoy_,
        )
        JDAM_ER___450_kg_GPS_Guided_Mk_83_GP_bomb = (
            2,
            Weapons.JDAM_ER___450_kg_GPS_Guided_Mk_83_GP_bomb,
        )
        UB_32A___32_x_UnGd_Rkts__57_mm_S_5KO_HEAT_Frag = (
            2,
            Weapons.UB_32A___32_x_UnGd_Rkts__57_mm_S_5KO_HEAT_Frag,
        )
        B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            2,
            Weapons.B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation = (
            2,
            Weapons.B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation,
        )
        O_25___1_x_UnGd_Rkts__340_mm_S_25_OFM_Hardened_Target_Penetrator = (
            2,
            Weapons.O_25___1_x_UnGd_Rkts__340_mm_S_25_OFM_Hardened_Target_Penetrator,
        )
        B_8M1___20_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange = (
            2,
            Weapons.B_8M1___20_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange,
        )
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            2,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        Kh_25ML__AS_10_Karen____300kg__ASM__Semi_Act_Laser__ = (
            2,
            Weapons.Kh_25ML__AS_10_Karen____300kg__ASM__Semi_Act_Laser__,
        )
        FAB_500_M_62___500kg_GP_Bomb_LD = (2, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        FAB_250___250kg_GP_Bomb_LD = (2, Weapons.FAB_250___250kg_GP_Bomb_LD)
        APU_68___S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk_ = (
            2,
            Weapons.APU_68___S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk_,
        )
        LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE = (
            2,
            Weapons.LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE,
        )
        # ERRR <CLEAN>
        CH_AASM_250_PGM = (2, Weapons.CH_AASM_250_PGM)

    class Pylon3:
        Fuel_tank_1150L_MiG_29 = (3, Weapons.Fuel_tank_1150L_MiG_29)
        R_73__AA_11_Archer____Infra_Red = (3, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_60M__AA_8_Aphid_B____IR_AAM = (3, Weapons.R_60M__AA_8_Aphid_B____IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (3, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9M_Sidewinder_IR_AAM = (3, Weapons.AIM_9M_Sidewinder_IR_AAM)
        R_27ER__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            3,
            Weapons.R_27ER__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_27ET__AA_10_Alamo_D____IR_Extended_Range = (
            3,
            Weapons.R_27ET__AA_10_Alamo_D____IR_Extended_Range,
        )
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            3,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            3,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            3,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (3, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        ADM_160B_MALD___Miniature_Air_Launched_Decoy_ = (
            3,
            Weapons.ADM_160B_MALD___Miniature_Air_Launched_Decoy_,
        )
        JDAM_ER___450_kg_GPS_Guided_Mk_83_GP_bomb = (
            3,
            Weapons.JDAM_ER___450_kg_GPS_Guided_Mk_83_GP_bomb,
        )
        UB_32A___32_x_UnGd_Rkts__57_mm_S_5KO_HEAT_Frag = (
            3,
            Weapons.UB_32A___32_x_UnGd_Rkts__57_mm_S_5KO_HEAT_Frag,
        )
        B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            3,
            Weapons.B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        O_25___1_x_UnGd_Rkts__340_mm_S_25_OFM_Hardened_Target_Penetrator = (
            3,
            Weapons.O_25___1_x_UnGd_Rkts__340_mm_S_25_OFM_Hardened_Target_Penetrator,
        )
        B_8M1___20_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange = (
            3,
            Weapons.B_8M1___20_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange,
        )
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            3,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        Kh_25ML__AS_10_Karen____300kg__ASM__Semi_Act_Laser__ = (
            3,
            Weapons.Kh_25ML__AS_10_Karen____300kg__ASM__Semi_Act_Laser__,
        )
        FAB_500_M_62___500kg_GP_Bomb_LD = (3, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        FAB_250___250kg_GP_Bomb_LD = (3, Weapons.FAB_250___250kg_GP_Bomb_LD)
        APU_68___S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk_ = (
            3,
            Weapons.APU_68___S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk_,
        )
        LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE = (
            3,
            Weapons.LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE,
        )
        ADM_160B_MALD_x_3___Miniature_Air_Launched_Decoy = (
            3,
            Weapons.ADM_160B_MALD_x_3___Miniature_Air_Launched_Decoy,
        )
        # ERRR <CLEAN>
        CH_AASM_250_PGM = (3, Weapons.CH_AASM_250_PGM)

    class Pylon4:
        Fuel_tank_1400L = (4, Weapons.Fuel_tank_1400L)

    class Pylon5:
        Fuel_tank_1150L_MiG_29 = (5, Weapons.Fuel_tank_1150L_MiG_29)
        R_73__AA_11_Archer____Infra_Red = (5, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_60M__AA_8_Aphid_B____IR_AAM = (5, Weapons.R_60M__AA_8_Aphid_B____IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (5, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9M_Sidewinder_IR_AAM = (5, Weapons.AIM_9M_Sidewinder_IR_AAM)
        R_27ER__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            5,
            Weapons.R_27ER__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_27ET__AA_10_Alamo_D____IR_Extended_Range = (
            5,
            Weapons.R_27ET__AA_10_Alamo_D____IR_Extended_Range,
        )
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            5,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            5,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            5,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (5, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        ADM_160B_MALD___Miniature_Air_Launched_Decoy_ = (
            5,
            Weapons.ADM_160B_MALD___Miniature_Air_Launched_Decoy_,
        )
        JDAM_ER___450_kg_GPS_Guided_Mk_83_GP_bomb = (
            5,
            Weapons.JDAM_ER___450_kg_GPS_Guided_Mk_83_GP_bomb,
        )
        UB_32A___32_x_UnGd_Rkts__57_mm_S_5KO_HEAT_Frag = (
            5,
            Weapons.UB_32A___32_x_UnGd_Rkts__57_mm_S_5KO_HEAT_Frag,
        )
        B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            5,
            Weapons.B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        O_25___1_x_UnGd_Rkts__340_mm_S_25_OFM_Hardened_Target_Penetrator = (
            5,
            Weapons.O_25___1_x_UnGd_Rkts__340_mm_S_25_OFM_Hardened_Target_Penetrator,
        )
        B_8M1___20_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange = (
            5,
            Weapons.B_8M1___20_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange,
        )
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            5,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        Kh_25ML__AS_10_Karen____300kg__ASM__Semi_Act_Laser__ = (
            5,
            Weapons.Kh_25ML__AS_10_Karen____300kg__ASM__Semi_Act_Laser__,
        )
        FAB_500_M_62___500kg_GP_Bomb_LD = (5, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        FAB_250___250kg_GP_Bomb_LD = (5, Weapons.FAB_250___250kg_GP_Bomb_LD)
        APU_68___S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk_ = (
            5,
            Weapons.APU_68___S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk_,
        )
        LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE = (
            5,
            Weapons.LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE,
        )
        ADM_160B_MALD_x_3___Miniature_Air_Launched_Decoy = (
            5,
            Weapons.ADM_160B_MALD_x_3___Miniature_Air_Launched_Decoy,
        )
        # ERRR <CLEAN>
        CH_AASM_250_PGM = (5, Weapons.CH_AASM_250_PGM)

    class Pylon6:
        R_73__AA_11_Archer____Infra_Red = (6, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_60M__AA_8_Aphid_B____IR_AAM = (6, Weapons.R_60M__AA_8_Aphid_B____IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (6, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9M_Sidewinder_IR_AAM = (6, Weapons.AIM_9M_Sidewinder_IR_AAM)
        R_27ER__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            6,
            Weapons.R_27ER__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_27ET__AA_10_Alamo_D____IR_Extended_Range = (
            6,
            Weapons.R_27ET__AA_10_Alamo_D____IR_Extended_Range,
        )
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            6,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            6,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            6,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (6, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        ADM_160B_MALD___Miniature_Air_Launched_Decoy_ = (
            6,
            Weapons.ADM_160B_MALD___Miniature_Air_Launched_Decoy_,
        )
        JDAM_ER___450_kg_GPS_Guided_Mk_83_GP_bomb = (
            6,
            Weapons.JDAM_ER___450_kg_GPS_Guided_Mk_83_GP_bomb,
        )
        UB_32A___32_x_UnGd_Rkts__57_mm_S_5KO_HEAT_Frag = (
            6,
            Weapons.UB_32A___32_x_UnGd_Rkts__57_mm_S_5KO_HEAT_Frag,
        )
        B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            6,
            Weapons.B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation = (
            6,
            Weapons.B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation,
        )
        O_25___1_x_UnGd_Rkts__340_mm_S_25_OFM_Hardened_Target_Penetrator = (
            6,
            Weapons.O_25___1_x_UnGd_Rkts__340_mm_S_25_OFM_Hardened_Target_Penetrator,
        )
        B_8M1___20_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange = (
            6,
            Weapons.B_8M1___20_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange,
        )
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            6,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        Kh_25ML__AS_10_Karen____300kg__ASM__Semi_Act_Laser__ = (
            6,
            Weapons.Kh_25ML__AS_10_Karen____300kg__ASM__Semi_Act_Laser__,
        )
        FAB_500_M_62___500kg_GP_Bomb_LD = (6, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        FAB_250___250kg_GP_Bomb_LD = (6, Weapons.FAB_250___250kg_GP_Bomb_LD)
        APU_68___S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk_ = (
            6,
            Weapons.APU_68___S_24B___240mm_UnGd_Rkt__235kg__HE_Frag___Low_Smk_,
        )
        LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE = (
            6,
            Weapons.LAU_10___4_x_UnGd_Rkts__127_mm_Zuni_Mk__24_Mod__1_HE,
        )
        # ERRR <CLEAN>
        CH_AASM_250_PGM = (6, Weapons.CH_AASM_250_PGM)

    class Pylon7:
        R_73__AA_11_Archer____Infra_Red = (7, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_60M__AA_8_Aphid_B____IR_AAM = (7, Weapons.R_60M__AA_8_Aphid_B____IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (7, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9M_Sidewinder_IR_AAM = (7, Weapons.AIM_9M_Sidewinder_IR_AAM)
        R_27ER__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            7,
            Weapons.R_27ER__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_27ET__AA_10_Alamo_D____IR_Extended_Range = (
            7,
            Weapons.R_27ET__AA_10_Alamo_D____IR_Extended_Range,
        )
        AIM_120B_AMRAAM___Active_Radar_AAM = (
            7,
            Weapons.AIM_120B_AMRAAM___Active_Radar_AAM,
        )
        AIM_120C_AMRAAM___Active_Radar_AAM = (
            7,
            Weapons.AIM_120C_AMRAAM___Active_Radar_AAM,
        )

    # ERRR <CLEAN>

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7}

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
class CH_Su_27P1M(PlaneType):
    id = "CH_Su-27P1M"
    height = 5.932
    width = 14.7
    length = 21.935
    fuel_max = 9400
    max_speed = 2499.984
    chaff = 96
    flare = 96
    charge_total = 192
    chaff_charge_size = 1
    flare_charge_size = 1
    eplrs = True

    property_defaults: Dict[str, Any] = {}

    livery_name = "CH_SU-27P1M"  # from type

    class Pylon1:
        R_73__AA_11_Archer____Infra_Red = (1, Weapons.R_73__AA_11_Archer____Infra_Red)

    class Pylon2:
        R_73__AA_11_Archer____Infra_Red = (2, Weapons.R_73__AA_11_Archer____Infra_Red)

    # ERRR <CLEAN>

    class Pylon3:
        R_73__AA_11_Archer____Infra_Red = (3, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_27ER__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            3,
            Weapons.R_27ER__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_27ET__AA_10_Alamo_D____IR_Extended_Range = (
            3,
            Weapons.R_27ET__AA_10_Alamo_D____IR_Extended_Range,
        )
        B_8M1___20_S_8OFP2 = (3, Weapons.B_8M1___20_S_8OFP2)
        FAB_250___250kg_GP_Bomb_LD = (3, Weapons.FAB_250___250kg_GP_Bomb_LD)
        FAB_500_M_62___500kg_GP_Bomb_LD = (3, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            3,
            Weapons.B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation = (
            3,
            Weapons.B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation,
        )
        B_8M1___20_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange = (
            3,
            Weapons.B_8M1___20_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD = (
            3,
            Weapons.MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            3,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        _2_x_B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation = (
            3,
            Weapons._2_x_B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation,
        )
        _2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            3,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        _2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange = (
            3,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange,
        )
        _2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8OFP2_MPP = (
            3,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8OFP2_MPP,
        )
        ADM_160B_MALD___Miniature_Air_Launched_Decoy_ = (
            3,
            Weapons.ADM_160B_MALD___Miniature_Air_Launched_Decoy_,
        )
        ADM_160B_MALD_x_3___Miniature_Air_Launched_Decoy = (
            3,
            Weapons.ADM_160B_MALD_x_3___Miniature_Air_Launched_Decoy,
        )
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            3,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        JDAM_ER___450_kg_GPS_Guided_Mk_83_GP_bomb = (
            3,
            Weapons.JDAM_ER___450_kg_GPS_Guided_Mk_83_GP_bomb,
        )
        # ERRR <CLEAN>
        CH_AASM_250_PGM = (3, Weapons.CH_AASM_250_PGM)

    class Pylon4:
        R_27ER__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            4,
            Weapons.R_27ER__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        FAB_250___250kg_GP_Bomb_LD = (4, Weapons.FAB_250___250kg_GP_Bomb_LD)
        FAB_500_M_62___500kg_GP_Bomb_LD = (4, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD = (
            4,
            Weapons.MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_5_x_FAB_250___250kg_GP_Bombs_LD = (
            4,
            Weapons.MBD3_U6_68_with_5_x_FAB_250___250kg_GP_Bombs_LD,
        )
        ADM_160B_MALD___Miniature_Air_Launched_Decoy_ = (
            4,
            Weapons.ADM_160B_MALD___Miniature_Air_Launched_Decoy_,
        )
        ADM_160B_MALD_x_3___Miniature_Air_Launched_Decoy = (
            4,
            Weapons.ADM_160B_MALD_x_3___Miniature_Air_Launched_Decoy,
        )
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            4,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        JDAM_ER___450_kg_GPS_Guided_Mk_83_GP_bomb = (
            4,
            Weapons.JDAM_ER___450_kg_GPS_Guided_Mk_83_GP_bomb,
        )
        # ERRR <CLEAN>
        CH_AASM_250_PGM = (4, Weapons.CH_AASM_250_PGM)

    class Pylon5:
        R_27ER__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            5,
            Weapons.R_27ER__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        FAB_250___250kg_GP_Bomb_LD = (5, Weapons.FAB_250___250kg_GP_Bomb_LD)
        FAB_500_M_62___500kg_GP_Bomb_LD = (5, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD = (
            5,
            Weapons.MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_3_x_FAB_250___250kg_GP_Bombs_LD = (
            5,
            Weapons.MBD3_U6_68_with_3_x_FAB_250___250kg_GP_Bombs_LD,
        )
        ADM_160B_MALD___Miniature_Air_Launched_Decoy_ = (
            5,
            Weapons.ADM_160B_MALD___Miniature_Air_Launched_Decoy_,
        )
        ADM_160B_MALD_x_3___Miniature_Air_Launched_Decoy = (
            5,
            Weapons.ADM_160B_MALD_x_3___Miniature_Air_Launched_Decoy,
        )
        JDAM_ER___450_kg_GPS_Guided_Mk_83_GP_bomb = (
            5,
            Weapons.JDAM_ER___450_kg_GPS_Guided_Mk_83_GP_bomb,
        )
        # ERRR <CLEAN>
        CH_AASM_250_PGM = (5, Weapons.CH_AASM_250_PGM)

    class Pylon6:
        R_27ER__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            6,
            Weapons.R_27ER__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        FAB_250___250kg_GP_Bomb_LD = (6, Weapons.FAB_250___250kg_GP_Bomb_LD)
        FAB_500_M_62___500kg_GP_Bomb_LD = (6, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD = (
            6,
            Weapons.MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            6,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        ADM_160B_MALD___Miniature_Air_Launched_Decoy_ = (
            6,
            Weapons.ADM_160B_MALD___Miniature_Air_Launched_Decoy_,
        )
        ADM_160B_MALD_x_3___Miniature_Air_Launched_Decoy = (
            6,
            Weapons.ADM_160B_MALD_x_3___Miniature_Air_Launched_Decoy,
        )
        JDAM_ER___450_kg_GPS_Guided_Mk_83_GP_bomb = (
            6,
            Weapons.JDAM_ER___450_kg_GPS_Guided_Mk_83_GP_bomb,
        )
        # ERRR <CLEAN>
        CH_AASM_250_PGM = (6, Weapons.CH_AASM_250_PGM)

    class Pylon7:
        R_27ER__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            7,
            Weapons.R_27ER__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        FAB_250___250kg_GP_Bomb_LD = (7, Weapons.FAB_250___250kg_GP_Bomb_LD)
        FAB_500_M_62___500kg_GP_Bomb_LD = (7, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD = (
            7,
            Weapons.MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_5_x_FAB_250___250kg_GP_Bombs_LD = (
            7,
            Weapons.MBD3_U6_68_with_5_x_FAB_250___250kg_GP_Bombs_LD,
        )
        ADM_160B_MALD___Miniature_Air_Launched_Decoy_ = (
            7,
            Weapons.ADM_160B_MALD___Miniature_Air_Launched_Decoy_,
        )
        ADM_160B_MALD_x_3___Miniature_Air_Launched_Decoy = (
            7,
            Weapons.ADM_160B_MALD_x_3___Miniature_Air_Launched_Decoy,
        )
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            7,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        JDAM_ER___450_kg_GPS_Guided_Mk_83_GP_bomb = (
            7,
            Weapons.JDAM_ER___450_kg_GPS_Guided_Mk_83_GP_bomb,
        )
        # ERRR <CLEAN>
        CH_AASM_250_PGM = (7, Weapons.CH_AASM_250_PGM)

    class Pylon8:
        R_73__AA_11_Archer____Infra_Red = (8, Weapons.R_73__AA_11_Archer____Infra_Red)
        R_27ER__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            8,
            Weapons.R_27ER__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_27ET__AA_10_Alamo_D____IR_Extended_Range = (
            8,
            Weapons.R_27ET__AA_10_Alamo_D____IR_Extended_Range,
        )
        B_8M1___20_S_8OFP2 = (8, Weapons.B_8M1___20_S_8OFP2)
        FAB_250___250kg_GP_Bomb_LD = (8, Weapons.FAB_250___250kg_GP_Bomb_LD)
        FAB_500_M_62___500kg_GP_Bomb_LD = (8, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            8,
            Weapons.B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation = (
            8,
            Weapons.B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation,
        )
        B_8M1___20_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange = (
            8,
            Weapons.B_8M1___20_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD = (
            8,
            Weapons.MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            8,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        _2_x_B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation = (
            8,
            Weapons._2_x_B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation,
        )
        _2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            8,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        _2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange = (
            8,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8TsM_SM_Orange,
        )
        _2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8OFP2_MPP = (
            8,
            Weapons._2_x_B_8M1___20_x_UnGd_Rkts__80_mm_S_8OFP2_MPP,
        )
        ADM_160B_MALD___Miniature_Air_Launched_Decoy_ = (
            8,
            Weapons.ADM_160B_MALD___Miniature_Air_Launched_Decoy_,
        )
        ADM_160B_MALD_x_3___Miniature_Air_Launched_Decoy = (
            8,
            Weapons.ADM_160B_MALD_x_3___Miniature_Air_Launched_Decoy,
        )
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            8,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        JDAM_ER___450_kg_GPS_Guided_Mk_83_GP_bomb = (
            8,
            Weapons.JDAM_ER___450_kg_GPS_Guided_Mk_83_GP_bomb,
        )
        # ERRR <CLEAN>
        CH_AASM_250_PGM = (8, Weapons.CH_AASM_250_PGM)

    class Pylon9:
        R_73__AA_11_Archer____Infra_Red = (9, Weapons.R_73__AA_11_Archer____Infra_Red)

    # ERRR <CLEAN>

    class Pylon10:
        R_73__AA_11_Archer____Infra_Red = (10, Weapons.R_73__AA_11_Archer____Infra_Red)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

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
