# Requires Swedish Military Assets for DCS by Currenthill:
# https://forum.dcs.world/topic/295202-swedish-military-assets-for-dcs-by-currenthill/
#

from typing import Set

from dcs import unittype, task
from dcs.helicopters import HelicopterType
from dcs.liveries_scanner import Liveries

from game.modsupport import vehiclemod, shipmod, helicoptermod


@vehiclemod
class BV410_RBS70(unittype.VehicleType):
    id = "BV410_RBS70"
    name = "[SMA] RBS 70 EldE 70 Mobile SAM LN"
    detection_range = 0
    threat_range = 8000
    air_weapon_dist = 8000
    eplrs = True


@vehiclemod
class BV410_RBS90(unittype.VehicleType):
    id = "BV410_RBS90"
    name = "[SMA] RBS 90 EldE 90 Mobile SAM LN"
    detection_range = 20000
    threat_range = 8000
    air_weapon_dist = 8000
    eplrs = True


@vehiclemod
class LvS_103_Lavett103_Rb103A(unittype.VehicleType):
    id = "LvS-103_Lavett103_Rb103A"
    name = "[SMA] LvS-103 Lavett 103 Rb103A Stationary SAM LN"
    detection_range = 0
    threat_range = 150000
    air_weapon_dist = 150000
    eplrs = True


@vehiclemod
class LvS_103_Lavett103_Rb103B(unittype.VehicleType):
    id = "LvS-103_Lavett103_Rb103B"
    name = "[SMA] LvS-103 Lavett 103 Rb103B Stationary SAM LN"
    detection_range = 0
    threat_range = 35000
    air_weapon_dist = 35000
    eplrs = True


@vehiclemod
class LvS_103_Lavett103_HX_Rb103A(unittype.VehicleType):
    id = "LvS-103_Lavett103_HX_Rb103A"
    name = "[SMA] LvS-103 Lavett 103 Rb103A Mobile SAM LN"
    detection_range = 0
    threat_range = 150000
    air_weapon_dist = 150000
    eplrs = True


@vehiclemod
class LvS_103_Lavett103_HX_Rb103B(unittype.VehicleType):
    id = "LvS-103_Lavett103_HX_Rb103B"
    name = "[SMA] LvS-103 Lavett 103 Rb103B Mobile SAM LN"
    detection_range = 0
    threat_range = 150000
    air_weapon_dist = 150000
    eplrs = True


@vehiclemod
class LvS_103_StriE103(unittype.VehicleType):
    id = "LvS-103_StriE103"
    name = "[SMA] LvS-103 StriE 103 Mobile SAM ECS"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0
    eplrs = True


@vehiclemod
class LvS_103_PM103(unittype.VehicleType):
    id = "LvS-103_PM103"
    name = "[SMA] LvS-103 PM 103 Stationary SAM STR"
    detection_range = 160000
    threat_range = 0
    air_weapon_dist = 0
    eplrs = True


@vehiclemod
class LvS_103_PM103_HX(unittype.VehicleType):
    id = "LvS-103_PM103_HX"
    name = "[SMA] LvS-103 PM 103 Mobile SAM STR"
    detection_range = 160000
    threat_range = 0
    air_weapon_dist = 0
    eplrs = True


@vehiclemod
class LvS_103_Elverk103(unittype.VehicleType):
    id = "LvS-103_Elverk103"
    name = "[SMA] LvS-103 Elverk 103 Mobile SAM EPP"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0
    eplrs = True


@vehiclemod
class LvKv9040(unittype.VehicleType):
    id = "LvKv9040"
    name = "[SMA] Lvkv 9040 SPAAG"
    detection_range = 15000
    threat_range = 4000
    air_weapon_dist = 4000
    eplrs = True


@vehiclemod
class RBS_70(unittype.VehicleType):
    id = "RBS-70"
    name = "[SMA] RBS 70 EldE 70 Stationary SAM LN"
    detection_range = 0
    threat_range = 8000
    air_weapon_dist = 8000
    eplrs = True


@vehiclemod
class RBS_90(unittype.VehicleType):
    id = "RBS-90"
    name = "[SMA] RBS 90 EldE 90 Stationary SAM LN"
    detection_range = 20000
    threat_range = 8000
    air_weapon_dist = 8000
    eplrs = True


@vehiclemod
class RBS_98(unittype.VehicleType):
    id = "RBS-98"
    name = "[SMA] RBS 98 EldE 98 Mobile SAM LN"
    detection_range = 0
    threat_range = 20000
    air_weapon_dist = 20000
    eplrs = True


@vehiclemod
class UndE23(unittype.VehicleType):
    id = "UndE23"
    name = "[SMA] UndE 23 (RBS 70/90/98) SAM STR"
    detection_range = 100000
    threat_range = 0
    air_weapon_dist = 0
    eplrs = True


@vehiclemod
class BV410(unittype.VehicleType):
    id = "BV410"
    name = "[SMA] Bv 410 ATV"
    detection_range = 0
    threat_range = 1800
    air_weapon_dist = 1800
    eplrs = True


@vehiclemod
class CV9040(unittype.VehicleType):
    id = "CV9040"
    name = "[SMA] Strf 9040 IFV"
    detection_range = 0
    threat_range = 4000
    air_weapon_dist = 4000
    eplrs = True


@vehiclemod
class Strv103(unittype.VehicleType):
    id = "Strv103"
    name = "[SMA] Strv 103 MBT"
    detection_range = 6000
    threat_range = 6000
    air_weapon_dist = 6000
    eplrs = True


@vehiclemod
class Strv121(unittype.VehicleType):
    id = "Strv121"
    name = "[SMA] Strv 121 MBT"
    detection_range = 0
    threat_range = 8000
    air_weapon_dist = 1200
    eplrs = True


@vehiclemod
class Strv122(unittype.VehicleType):
    id = "Strv122"
    name = "[SMA] Strv 122 MBT"
    detection_range = 0
    threat_range = 8000
    air_weapon_dist = 1200
    eplrs = True


@vehiclemod
class Strv2000(unittype.VehicleType):
    id = "Strv2000"
    name = "[SMA] Strv 2000 T140/40 MBT"
    detection_range = 8000
    threat_range = 8000
    air_weapon_dist = 4000
    eplrs = True


@vehiclemod
class Volvo740(unittype.VehicleType):
    id = "Volvo740"
    name = "[SMA] Volvo 740 Improvised fighting vehicle"
    detection_range = 0
    threat_range = 1200
    air_weapon_dist = 1200
    eplrs = True


@vehiclemod
class RBS_15KA(unittype.VehicleType):
    id = "RBS-15KA"
    name = "[SMA] RBS 15KA LBASM"
    detection_range = 300000
    threat_range = 300000
    air_weapon_dist = 300000
    eplrs = True


## INFANTRY


@vehiclemod
class AG_90(unittype.VehicleType):
    id = "AG-90"
    name = "[SMA] Ag 90 Sniper team"
    detection_range = 5000
    threat_range = 1800
    air_weapon_dist = 1800
    eplrs = True


@vehiclemod
class SwedishinfantryAK4(unittype.VehicleType):
    id = "SwedishinfantryAK4"
    name = "[SMA] Ak 4 Soldier"
    detection_range = 1500
    threat_range = 600
    air_weapon_dist = 600
    eplrs = True


@vehiclemod
class SwedishinfantryAK5(unittype.VehicleType):
    id = "SwedishinfantryAK5"
    name = "[SMA] Ak 5 Soldier"
    detection_range = 1500
    threat_range = 500
    air_weapon_dist = 500
    eplrs = True


@vehiclemod
class SwedishinfantryAK5GT(unittype.VehicleType):
    id = "SwedishinfantryAK5GT"
    name = "[SMA] Ak 5 Granattillsats Soldier"
    detection_range = 1000
    threat_range = 500
    air_weapon_dist = 500
    eplrs = True


@vehiclemod
class SwedishinfantryKSP90(unittype.VehicleType):
    id = "SwedishinfantryKSP90"
    name = "[SMA] Ksp 90 Soldier"
    detection_range = 700
    threat_range = 700
    air_weapon_dist = 700
    eplrs = True


@vehiclemod
class SwedishinfantryKSP58(unittype.VehicleType):
    id = "SwedishinfantryKSP58"
    name = "[SMA] Ksp 58 Soldier"
    detection_range = 1200
    threat_range = 1200
    air_weapon_dist = 1200
    eplrs = True


@vehiclemod
class SwedishinfantryPskott86(unittype.VehicleType):
    id = "SwedishinfantryPskott86"
    name = "[SMA] Pskott 86 Soldier"
    detection_range = 1500
    threat_range = 400
    air_weapon_dist = 400
    eplrs = True


@vehiclemod
class RBS_57(unittype.VehicleType):
    id = "RBS-57"
    name = "[SMA] RBS 57 ATGM"
    detection_range = 5000
    threat_range = 1000
    air_weapon_dist = 1000
    eplrs = True


@vehiclemod
class RBS_58(unittype.VehicleType):
    id = "RBS-58"
    name = "[SMA] RBS 58 ATGM"
    detection_range = 5000
    threat_range = 5000
    air_weapon_dist = 5000
    eplrs = True


## ARTILLERY


@vehiclemod
class Artillerisystem08(unittype.VehicleType):
    id = "Artillerisystem08"
    name = "[SMA] Artillerisystem 08 SPG"
    detection_range = 10000
    threat_range = 25000
    air_weapon_dist = 25000
    eplrs = True


@vehiclemod
class Grkpbv90(unittype.VehicleType):
    id = "Grkpbv90"
    name = "[SMA] Grkpbv 90 SPM"
    detection_range = 0
    threat_range = 7500
    air_weapon_dist = 7500
    eplrs = True


## SHIPS


@shipmod
class HSwMS_Visby(unittype.ShipType):
    id = "HSwMS_Visby"
    name = "[SMA] HSwMS Visby Corvette"
    plane_num = 0
    helicopter_num = 1
    parking = 1
    detection_range = 180000
    threat_range = 30000
    air_weapon_dist = 30000


@shipmod
class Strb90(unittype.ShipType):
    id = "Strb90"
    name = "[SMA] Strb 90 FAC"
    plane_num = 0
    helicopter_num = 0
    parking = 0
    detection_range = 46300
    threat_range = 10000
    air_weapon_dist = 10000


## HELICOPTERS


@helicoptermod
class HKP15B(HelicopterType):
    id = "HKP15B"
    height = 3.4
    width = 10.83
    length = 11.45
    fuel_max = 686
    max_speed = 311
    chaff = 0
    flare = 0
    charge_total = 0
    chaff_charge_size = 0
    flare_charge_size = 0
    eplrs = True
    radio_frequency = 124

    panel_radio = {
        1: {
            "channels": {6: 41, 2: 31, 8: 50, 3: 32, 1: 30, 4: 33, 5: 40, 7: 42},
        },
    }

    livery_name = "HKP15B"  # from type
    Liveries = Liveries()[livery_name]

    pylons: Set[int] = set()

    tasks = [task.Reconnaissance, task.Transport]
    task_default = task.Reconnaissance
