# Requires Iran Military Assets for DCS by CurrentHill:
# https://www.currenthill.com/iran
#

from dcs import unittype

from game.modsupport import shipmod, vehiclemod


@vehiclemod
class CH_Shahed136(unittype.VehicleType):
    id = "CH_Shahed136"
    name = "[CH] Shahed 136 LM"
    detection_range = 0
    threat_range = 360000
    air_weapon_dist = 360000
    eplrs = True


@shipmod
class IranFAC_MG(unittype.ShipType):
    id = "IranFAC_MG"
    name = "[CH] IRGCN FAC MANPADS"
    plane_num = 0
    helicopter_num = 0
    parking = 0
    detection_range = 40000
    threat_range = 5200
    air_weapon_dist = 5200


@shipmod
class IranFAC_MG_AShM(unittype.ShipType):
    id = "IranFAC_MG_AShM"
    name = "[CH] IRGCN FAC AShM"
    plane_num = 0
    helicopter_num = 0
    parking = 0
    detection_range = 40000
    threat_range = 25000
    air_weapon_dist = 25000
