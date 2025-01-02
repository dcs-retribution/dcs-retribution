# Requires China Military Assets for DCS by Currenthill:
# https://www.currenthill.com/china
#

from dcs import unittype

from game.modsupport import vehiclemod, shipmod, helicoptermod


# Artillery
@vehiclemod
class CH_PCL181_155(unittype.VehicleType):
    id = "CH_PCL181_155"
    name = "[CH] PCL-181 SPG 155 HE"
    detection_range = 0
    threat_range = 40000
    air_weapon_dist = 40000
    eplrs = True


@vehiclemod
class CH_PCL181_GP155(unittype.VehicleType):
    id = "CH_PCL181_GP155"
    name = "[CH] PCL-181 SPG GP155"
    detection_range = 0
    threat_range = 40000
    air_weapon_dist = 40000
    eplrs = True


@vehiclemod
class CH_PHL11_HE(unittype.VehicleType):
    id = "CH_PHL11_HE"
    name = "[CH] PHL-11 SPMRL (HE)"
    detection_range = 0
    threat_range = 30000
    air_weapon_dist = 30000
    eplrs = True


@vehiclemod
class CH_PHL11_DPICM(unittype.VehicleType):
    id = "CH_PHL11_DPICM"
    name = "[CH] PHL-11 SPMRL (DPICM)"
    detection_range = 0
    threat_range = 30000
    air_weapon_dist = 30000
    eplrs = True


@vehiclemod
class CH_PHL16_FD280(unittype.VehicleType):
    id = "CH_PHL16_FD280"
    name = "[CH] PHL-16 SPMRL (FD280)"
    detection_range = 0
    threat_range = 280000
    air_weapon_dist = 280000
    eplrs = True


@vehiclemod
class CH_PLZ07(unittype.VehicleType):
    id = "CH_PLZ07"
    name = "[CH] PLZ-07 SPG"
    detection_range = 8000
    threat_range = 22000
    air_weapon_dist = 1800
    eplrs = True


# Air Defense
@vehiclemod
class HQ17A(unittype.VehicleType):
    id = "HQ17A"
    name = "[CH] HQ-17A SHORAD"
    detection_range = 45000
    threat_range = 15000
    air_weapon_dist = 15000
    eplrs = True


@vehiclemod
class CH_HQ22_LN(unittype.VehicleType):
    id = "CH_HQ22_LN"
    name = "[CH] HQ-22 LN"
    detection_range = 0
    threat_range = 170000
    air_weapon_dist = 170000
    eplrs = True


@vehiclemod
class CH_HQ22_STR(unittype.VehicleType):
    id = "CH_HQ22_STR"
    name = "[CH] HQ-22 H-200 STR"
    detection_range = 200000
    threat_range = 0
    air_weapon_dist = 0
    eplrs = True


@vehiclemod
class CH_HQ22_SR(unittype.VehicleType):
    id = "CH_HQ22_SR"
    name = "[CH] HQ-22 JSG-100 SR"
    detection_range = 240000
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class CH_LD3000(unittype.VehicleType):
    id = "CH_LD3000"
    name = "[CH] LD-3000 C-RAM Mobile"
    detection_range = 15000
    threat_range = 3000
    air_weapon_dist = 3000
    eplrs = True


@vehiclemod
class CH_LD3000_stationary(unittype.VehicleType):
    id = "CH_LD3000_stationary"
    name = "[CH] LD-3000 C-RAM Stationary"
    detection_range = 15000
    threat_range = 3000
    air_weapon_dist = 3000
    eplrs = True


@vehiclemod
class PGL_625(unittype.VehicleType):
    id = "PGL_625"
    name = "[CH] PGL-625 SPAAGM"
    detection_range = 20000
    threat_range = 10000
    air_weapon_dist = 10000
    eplrs = True


@vehiclemod
class CH_PGZ09(unittype.VehicleType):
    id = "CH_PGZ09"
    name = "[CH] PGZ-09 SPAAG"
    detection_range = 20000
    threat_range = 4000
    air_weapon_dist = 4000
    eplrs = True


@vehiclemod
class CH_PGZ95(unittype.VehicleType):
    id = "CH_PGZ95"
    name = "[CH] PGZ-95 SPAAG"
    detection_range = 11000
    threat_range = 2500
    air_weapon_dist = 2500
    eplrs = True


# Unarmed
@vehiclemod
class CH_SX2190(unittype.VehicleType):
    id = "CH_SX2190"
    name = "[CH] SX2190 Truck"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


# Armor
@vehiclemod
class ZTZ_99A2(unittype.VehicleType):
    id = "ZTZ_99A2"
    name = "[CH] ZTZ-99A2 MBT"
    detection_range = 8000
    threat_range = 5000
    air_weapon_dist = 5000
    eplrs = True


@vehiclemod
class CH_ZBD04A_AT(unittype.VehicleType):
    id = "CH_ZBD04A-AT"
    name = "[CH] ZBD-04A AT SPATGM"
    detection_range = 20000
    threat_range = 10000
    air_weapon_dist = 10000
    eplrs = True


@vehiclemod
class CH_ZTQ_15(unittype.VehicleType):
    id = "CH_ZTQ_15"
    name = "[CH] ZTQ-15 LT"
    detection_range = 7000
    threat_range = 4000
    air_weapon_dist = 4000
    eplrs = True


@vehiclemod
class CH_ZTL11(unittype.VehicleType):
    id = "CH_ZTL11"
    name = "[CH] ZTL-11 AFV"
    detection_range = 7000
    threat_range = 4000
    air_weapon_dist = 4000
    eplrs = True


@vehiclemod
class CH_ZBL09(unittype.VehicleType):
    id = "CH_ZBL09"
    name = "[CH] ZBL-09 IFV"
    detection_range = 10000
    threat_range = 3000
    air_weapon_dist = 3000
    eplrs = True


# Missiles
@vehiclemod
class CH_CJ10(unittype.VehicleType):
    id = "CH_CJ10"
    name = "[CH] CJ-10 GLCM"
    detection_range = 2000000
    threat_range = 2000000
    air_weapon_dist = 2000000
    eplrs = True


@vehiclemod
class CH_YJ12B(unittype.VehicleType):
    id = "CH_YJ12B"
    name = "[CH] YJ-12B LBASM"
    detection_range = 0
    threat_range = 300000
    air_weapon_dist = 300000
    eplrs = True


@vehiclemod
class CH_DF21D(unittype.VehicleType):
    id = "CH_DF21D"
    name = "[CH] DF-21D LBASBM"
    detection_range = 0
    threat_range = 1000000
    air_weapon_dist = 1000000
    eplrs = True


## SHIPS


@shipmod
class CH_Type022(unittype.ShipType):
    id = "CH_Type022"
    name = "[CH] Type 022 FAC"
    plane_num = 0
    helicopter_num = 0
    parking = 0
    detection_range = 100000
    threat_range = 4000
    air_weapon_dist = 4000


@shipmod
class Type052D(unittype.ShipType):
    id = "Type052D"
    name = "[CH] Type 052D Destroyer"
    plane_num = 0
    helicopter_num = 1
    parking = 1
    detection_range = 400000
    threat_range = 250000
    air_weapon_dist = 250000


@shipmod
class Type055(unittype.ShipType):
    id = "Type055"
    name = "[CH] Type 055 Destroyer"
    plane_num = 0
    helicopter_num = 1
    parking = 1
    detection_range = 500000
    threat_range = 250000
    air_weapon_dist = 250000


@shipmod
class CH_Type056A(unittype.ShipType):
    id = "CH_Type056A"
    name = "[CH] Type 056A Corvette"
    plane_num = 0
    helicopter_num = 1
    parking = 1
    detection_range = 160000
    threat_range = 8000
    air_weapon_dist = 8000


@shipmod
class CH_Type054B(unittype.ShipType):
    id = "CH_Type054B"
    name = "[CH] Type 054B Frigate"
    plane_num = 0
    helicopter_num = 1
    parking = 1
    detection_range = 300000
    threat_range = 160000
    air_weapon_dist = 160000
