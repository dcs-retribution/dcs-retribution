# Requires Swedish Military Assets for DCS by Currenthill:
# https://forum.dcs.world/topic/295202-swedish-military-assets-for-dcs-by-currenthill/
#

from typing import Set

from dcs import unittype, task
from dcs.helicopters import HelicopterType

from game.modsupport import vehiclemod, shipmod, helicoptermod


@vehiclemod
class Vap_mutt_gun(unittype.VehicleType):
    id = "vap_mutt_gun"
    name = "VAP US MUTT Gun"
    detection_range = 0
    threat_range = 5000
    air_weapon_dist = 5000


@vehiclemod
class Vap_type63_mlrs(unittype.VehicleType):
    id = "vap_type63_mlrs"
    name = "VAP VC Type63 107mm MLRS"
    detection_range = 5000
    threat_range = 5000
    air_weapon_dist = 5000


@vehiclemod
class Vap_vc_bicycle_mortar(unittype.VehicleType):
    id = "vap_vc_bicycle_mortar"
    name = "VAP VC Bicycle Mortar"
    detection_range = 0
    threat_range = 7000
    air_weapon_dist = 7000


@vehiclemod
class Vap_zis_150_aa(unittype.VehicleType):
    id = "vap_zis_150_aa"
    name = "VAP VC Zis 150 AAA"
    detection_range = 5000
    threat_range = 7000
    air_weapon_dist = 7000


@vehiclemod
class Vap_us_hooch_LP(unittype.VehicleType):
    id = "vap_us_hooch_LP"
    name = "VAP US Hooch Low Poly"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class Vap_ammo_50cal_line(unittype.VehicleType):
    id = "vap_ammo_50cal_line"
    name = "VAP US Ammo 50Cal Line"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class Vap_ammo_50cal_pack(unittype.VehicleType):
    id = "vap_ammo_50cal_pack"
    name = "VAP US Ammo 50Cal Pack"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class Vap_barrels_line(unittype.VehicleType):
    id = "vap_barrels_line"
    name = "VAP Barrels Line"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class Vap_barrels(unittype.VehicleType):
    id = "vap_barrels"
    name = "VAP Barrels Pack"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class Vap_ammo_box_pile(unittype.VehicleType):
    id = "vap_ammo_box_pile"
    name = "VAP Ammo Box Pile"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class Vap_ammo_box_wood_long(unittype.VehicleType):
    id = "vap_ammo_box_wood_long"
    name = "VAP Ammo Box Long"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class Vap_ammo_box_wood_small(unittype.VehicleType):
    id = "vap_ammo_box_wood_small"
    name = "VAP Ammo Box Small"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class Vap_barrel_red(unittype.VehicleType):
    id = "vap_barrel_red"
    name = "VAP Barrel Red"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class Vap_barrel_green(unittype.VehicleType):
    id = "vap_barrel_green"
    name = "VAP Barrel Green"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class Vap_mre_boxes(unittype.VehicleType):
    id = "vap_mre_boxes"
    name = "VAP US MRE Boxes"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class Vap_mixed_cargo_1(unittype.VehicleType):
    id = "vap_mixed_cargo_1"
    name = "VAP US Mixed Cargo 1"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class Vap_mixed_cargo_2(unittype.VehicleType):
    id = "vap_mixed_cargo_2"
    name = "VAP US Mixed Cargo 2"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class Vap_watchtower(unittype.VehicleType):
    id = "vap_watchtower"
    name = "VAP Vietcong Watchtower"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class Vap_house_high(unittype.VehicleType):
    id = "vap_house_high"
    name = "VAP Bamboo House High"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class Vap_house_long(unittype.VehicleType):
    id = "vap_house_long"
    name = "VAP Bamboo House Long"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class Vap_house_small(unittype.VehicleType):
    id = "vap_house_small"
    name = "VAP Bamboo House Small"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class Vap_house_T(unittype.VehicleType):
    id = "vap_house_T"
    name = "VAP Bamboo House T-Shape"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class Vap_house_tiny(unittype.VehicleType):
    id = "vap_house_tiny"
    name = "VAP Bamboo House Tiny"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class Vap_house1(unittype.VehicleType):
    id = "vap_house1"
    name = "VAP Bamboo House"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class Vap_us_hooch_radio(unittype.VehicleType):
    id = "vap_us_hooch_radio"
    name = "VAP US Hooch Radio"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class Vap_us_hooch_closed(unittype.VehicleType):
    id = "vap_us_hooch_closed"
    name = "VAP US Hooch"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class Vap_vc_bunker_single(unittype.VehicleType):
    id = "vap_vc_bunker_single"
    name = "VAP VC Bunker"
    detection_range = 0
    threat_range = 800
    air_weapon_dist = 800


@vehiclemod
class Vap_vc_mg_nest(unittype.VehicleType):
    id = "vap_vc_mg_nest"
    name = "VAP VC MG Nest"
    detection_range = 1000
    threat_range = 500
    air_weapon_dist = 500


@vehiclemod
class Vap_mule(unittype.VehicleType):
    id = "vap_mule"
    name = "VAP US Mule"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class Vap_mutt(unittype.VehicleType):
    id = "vap_mutt"
    name = "VAP US MUTT"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class Vap_m35_truck(unittype.VehicleType):
    id = "vap_m35_truck"
    name = "VAP US M35 Truck"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class Vap_vc_zis(unittype.VehicleType):
    id = "vap_vc_zis"
    name = "VAP VC Zis 150"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class Vap_vc_bicycle(unittype.VehicleType):
    id = "vap_vc_bicycle"
    name = "VAP VC Bicycle"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class Vap_vc_zil(unittype.VehicleType):
    id = "vap_vc_zil"
    name = "VAP VC Zil 130"
    detection_range = 5000
    threat_range = 500
    air_weapon_dist = 500


@vehiclemod
class Vap_vc_bicycle_ak(unittype.VehicleType):
    id = "vap_vc_bicycle_ak"
    name = "VAP VC Bicycle AK"
    detection_range = 5000
    threat_range = 500
    air_weapon_dist = 500


@shipmod
class Vap_us_seafloat(unittype.ShipType):
    id = "vap_us_seafloat"
    name = "VAP - US Sea Float Barge"
    helicopter_num = 4
    parking = 4
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0
