from dcs.unittype import ShipType

from game.modsupport import shipmod


@shipmod
class L61(ShipType):
    id = "L61"
    name = "L61 Juan Carlos I"
    plane_num = 40
    helicopter_num = 36
    parking = 4
    detection_range = 300000
    threat_range = 150000
    air_weapon_dist = 150000


@shipmod
class F100(ShipType):
    id = "F100"
    name = "F100 Álvaro de Bazán"
    helicopter_num = 1
    parking = 1
    detection_range = 160000
    threat_range = 45000
    air_weapon_dist = 45000


@shipmod
class F105(ShipType):
    id = "F105"
    name = "F105 Cristobal Colon"
    helicopter_num = 1
    parking = 1
    detection_range = 160000
    threat_range = 45000
    air_weapon_dist = 45000


@shipmod
class L52(ShipType):
    id = "L52"
    name = "L52 Castilla"
    helicopter_num = 2
    parking = 2
    detection_range = 300000
    threat_range = 150000
    air_weapon_dist = 150000


@shipmod
class L02(ShipType):
    id = "L02"
    name = "L02 Canberra"
    plane_num = 40
    helicopter_num = 36
    parking = 4
    detection_range = 300000
    threat_range = 150000
    air_weapon_dist = 150000


@shipmod
class DDG39(ShipType):
    id = "DDG39"
    name = "HMAS HOBART DDG39"
    helicopter_num = 1
    parking = 1
    detection_range = 160000
    threat_range = 45000
    air_weapon_dist = 45000
