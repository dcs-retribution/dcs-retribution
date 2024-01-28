from dcs.unittype import VehicleType

from game.modsupport import vehiclemod


@vehiclemod
class Iron_Dome_David_Sling_CP(VehicleType):
    id = "Iron_Dome_David_Sling_CP"
    name = "[IDF Mods] Iron Dome-David Sling CP"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0
    eplrs = True


@vehiclemod
class IRON_DOME_LN(VehicleType):
    id = "IRON_DOME_LN"
    name = "[IDF Mods] Iron Dome"
    detection_range = 0
    threat_range = 20000
    air_weapon_dist = 20000


@vehiclemod
class DAVID_SLING_LN(VehicleType):
    id = "DAVID_SLING_LN"
    name = "[IDF Mods] David Sling"
    detection_range = 0
    threat_range = 250000
    air_weapon_dist = 250000


@vehiclemod
class ELM2084_MMR_AD_RT(VehicleType):
    id = "ELM2084_MMR_AD_RT"
    name = "[IDF Mods] ELM-2084MMR AD Rotating Mode"
    detection_range = 475000
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class ELM2084_MMR_AD_SC(VehicleType):
    id = "ELM2084_MMR_AD_SC"
    name = "[IDF Mods] ELM-2084MMR AD Sector Mode"
    detection_range = 650000
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class ELM2084_MMR_WLR(VehicleType):
    id = "ELM2084_MMR_WLR"
    name = "[IDF Mods] ELM-2084MMR WLR Mode"
    detection_range = 160000
    threat_range = 0
    air_weapon_dist = 0
