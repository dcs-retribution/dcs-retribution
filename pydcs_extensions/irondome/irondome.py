from dcs.unittype import VehicleType

from game.modsupport import vehiclemod


@vehiclemod
class I9K51_GRAD(VehicleType):
    id = "I9K51_GRAD"
    name = "(IDF Mods Project) BM-21 Grad 122mm"
    detection_range = 0
    threat_range = 19000
    air_weapon_dist = 19000
    eplrs = True


@vehiclemod
class I9K57_URAGAN(VehicleType):
    id = "I9K57_URAGAN"
    name = "(IDF Mods Project) Urgan BM-27 220mm"
    detection_range = 0
    threat_range = 35800
    air_weapon_dist = 35800
    eplrs = True


@vehiclemod
class I9K58_SMERCH(VehicleType):
    id = "I9K58_SMERCH"
    name = "(IDF Mods Project) 9A52 Smerch CM 300mm"
    detection_range = 0
    threat_range = 70000
    air_weapon_dist = 70000
    eplrs = True


@vehiclemod
class IRON_DOME_CP(VehicleType):
    id = "IRON_DOME_CP"
    name = "Iron Dome CP"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0
    eplrs = True


@vehiclemod
class IRON_DOME_LN(VehicleType):
    id = "IRON_DOME_LN"
    name = "Iron Dome LN"
    detection_range = 0
    threat_range = 25000
    air_weapon_dist = 25000


@vehiclemod
class ELM2048_MMR(VehicleType):
    id = "ELM2048_MMR"
    name = "Iron Dome ELM-2048 MMR"
    detection_range = 412000
    threat_range = 0
    air_weapon_dist = 0
