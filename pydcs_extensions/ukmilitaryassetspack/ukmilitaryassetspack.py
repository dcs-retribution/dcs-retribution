# Requires UK Military Assets for DCS by Currenthill:
# https://www.currenthill.com/uk
#


from dcs import unittype

from game.modsupport import shipmod, vehiclemod


@vehiclemod
class CH_Ajax(unittype.VehicleType):
    id = "CH_Ajax"
    name = "[CH] Ajax CRV"
    detection_range = 5000
    threat_range = 5000
    air_weapon_dist = 5000
    eplrs = True


@vehiclemod
class CH_AS90(unittype.VehicleType):
    id = "CH_AS90"
    name = "[CH] AS-90 SPG"
    detection_range = 0
    threat_range = 24000
    air_weapon_dist = 24000
    eplrs = True


@vehiclemod
class CH_Challenger2(unittype.VehicleType):
    id = "CH_Challenger2"
    name = "[CH] Challenger 2 MBT"
    detection_range = 5000
    threat_range = 4000
    air_weapon_dist = 4000
    eplrs = True


@vehiclemod
class CH_Challenger3(unittype.VehicleType):
    id = "CH_Challenger3"
    name = "[CH] Challenger 3 MBT"
    detection_range = 5000
    threat_range = 5000
    air_weapon_dist = 5000
    eplrs = True


@vehiclemod
class CH_LandRoverWolf(unittype.VehicleType):
    id = "CH_LandRoverWolf"
    name = "[CH] Land Rover Wolf LUV"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class CH_LandRoverWMIK_M2(unittype.VehicleType):
    id = "CH_LandRoverWMIK_M2"
    name = "[CH] Land Rover Wolf WMIK (M2)"
    detection_range = 0
    threat_range = 1800
    air_weapon_dist = 1800
    eplrs = True


@vehiclemod
class CH_LandRoverWMIK_MK19(unittype.VehicleType):
    id = "CH_LandRoverWMIK_MK19"
    name = "[CH] Land Rover Wolf WMIK (Mk19)"
    detection_range = 0
    threat_range = 2000
    air_weapon_dist = 2000
    eplrs = True


@vehiclemod
class CH_Scimitar(unittype.VehicleType):
    id = "CH_Scimitar"
    name = "[CH] Scimitar CRV"
    detection_range = 5000
    threat_range = 3000
    air_weapon_dist = 3000
    eplrs = True


@vehiclemod
class CH_Scorpion(unittype.VehicleType):
    id = "CH_Scorpion"
    name = "[CH] Scorpion LT"
    detection_range = 5000
    threat_range = 3000
    air_weapon_dist = 3000
    eplrs = True


@vehiclemod
class CH_SkySabreC2(unittype.VehicleType):
    id = "CH_SkySabreC2"
    name = "[CH] Sky Sabre C2 (HX)"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0
    eplrs = True


@vehiclemod
class CH_SkySabreGiraffe(unittype.VehicleType):
    id = "CH_SkySabreGiraffe"
    name = "[CH] Sky Sabre Giraffe AMB STR (HX)"
    detection_range = 120000
    threat_range = 0
    air_weapon_dist = 0
    eplrs = True


@vehiclemod
class CH_SkySabreLN(unittype.VehicleType):
    id = "CH_SkySabreLN"
    name = "[CH] Sky Sabre iLauncher LN (HX)"
    detection_range = 0
    threat_range = 25000
    air_weapon_dist = 25000
    eplrs = True


@vehiclemod
class CH_StormerHVM(unittype.VehicleType):
    id = "CH_StormerHVM"
    name = "[CH] Stormer HVM SHORAD"
    detection_range = 10000
    threat_range = 7000
    air_weapon_dist = 7000
    eplrs = True


@vehiclemod
class CH_Warrior(unittype.VehicleType):
    id = "CH_Warrior"
    name = "[CH] Warrior IFV"
    detection_range = 0
    threat_range = 2500
    air_weapon_dist = 2500
    eplrs = True


@shipmod
class CH_Type26(unittype.ShipType):
    id = "CH_Type26"
    name = "[CH] Type 26 Frigate"
    helicopter_num = 1
    parking = 1
    detection_range = 450000
    threat_range = 160000
    air_weapon_dist = 160000


@shipmod
class Type45(unittype.ShipType):
    id = "Type45"
    name = "[CH] Type 45 Destroyer"
    helicopter_num = 1
    parking = 1
    detection_range = 450000
    threat_range = 160000
    air_weapon_dist = 160000
