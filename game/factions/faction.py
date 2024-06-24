from __future__ import annotations

import itertools
import logging
from collections import defaultdict
from dataclasses import dataclass, field
from functools import cached_property
from typing import Optional, Dict, Type, List, Any, Iterator, TYPE_CHECKING, Set

import dcs
from dcs.country import Country
from dcs.unittype import ShipType, StaticType, UnitType as DcsUnitType

from game.armedforces.forcegroup import ForceGroup
from game.data.building_data import (
    WW2_ALLIES_BUILDINGS,
    DEFAULT_AVAILABLE_BUILDINGS,
    WW2_GERMANY_BUILDINGS,
    WW2_FREE,
    REQUIRED_BUILDINGS,
    IADS_BUILDINGS,
)
from game.data.doctrine import (
    Doctrine,
    MODERN_DOCTRINE,
    COLDWAR_DOCTRINE,
    WWII_DOCTRINE,
)
from game.data.groups import GroupRole
from game.data.units import UnitClass
from game.dcs.aircrafttype import AircraftType
from game.dcs.countries import country_with_name
from game.dcs.groundunittype import GroundUnitType
from game.dcs.shipunittype import ShipUnitType
from game.dcs.unittype import UnitType
from pydcs_extensions import inject_F15I, eject_F15I
from pydcs_extensions.f16i_idf.f16i_idf import inject_F16I, eject_F16I

if TYPE_CHECKING:
    from game.theater.start_generator import ModSettings


@dataclass
class Faction:
    #: List of locales to use when generating random names. If not set, Faker will
    #: choose the default locale.
    locales: Optional[List[str]]

    # The unit type to spawn for cargo shipping.
    cargo_ship: ShipUnitType

    # Country used by this faction
    country: Country

    # Nice name of the faction
    name: str = field(default="")

    # List of faction file authors
    authors: str = field(default="")

    # A description of the faction
    description: str = field(default="")

    # Available aircraft
    aircraft: Set[AircraftType] = field(default_factory=set)

    # Available awacs aircraft
    awacs: Set[AircraftType] = field(default_factory=set)

    # Available tanker aircraft
    tankers: Set[AircraftType] = field(default_factory=set)

    # Available frontline units
    frontline_units: Set[GroundUnitType] = field(default_factory=set)

    # Available artillery units
    artillery_units: Set[GroundUnitType] = field(default_factory=set)

    # Infantry units used
    infantry_units: Set[GroundUnitType] = field(default_factory=set)

    # Logistics units used
    logistics_units: Set[GroundUnitType] = field(default_factory=set)

    # Possible Air Defence units, Like EWRs
    air_defense_units: Set[GroundUnitType] = field(default_factory=set)

    # A list of all supported sets of units
    preset_groups: list[ForceGroup] = field(default_factory=list)

    # Possible Missile site generators for this faction
    missiles: Set[GroundUnitType] = field(default_factory=set)

    # Required mods or asset packs
    requirements: Dict[str, str] = field(default_factory=dict)

    # Possible carrier units mapped to names
    carriers: Dict[ShipUnitType, Set[str]] = field(default_factory=dict)

    # Available Naval Units
    naval_units: Set[ShipUnitType] = field(default_factory=set)

    # Whether this faction has JTAC access
    has_jtac: bool = field(default=False)

    # Unit to use as JTAC for this faction
    jtac_unit: Optional[AircraftType] = field(default=None)

    # doctrine
    doctrine: Doctrine = field(default=MODERN_DOCTRINE)

    # List of available building layouts for this faction
    building_set: Set[str] = field(default_factory=set)

    # List of default livery overrides
    liveries_overrides: Dict[AircraftType, List[str]] = field(default_factory=dict)

    # List of default livery overrides for ground vehicles
    liveries_overrides_ground_forces: Dict[str, List[str]] = field(default_factory=dict)

    #: Set to True if the faction should force the "Unrestricted satnav" option
    #: for the mission. This option enables GPS for capable aircraft regardless
    #: of the time period or operator. For example, the CJTF "countries" don't
    #: appear to have GPS capability, so they need this.
    #:
    #: Note that this option cannot be set per-side. If either faction needs it,
    #: both will use it.
    unrestricted_satnav: bool = False

    # Store mod settings so mod properties can be injected again on game load,
    # in case mods like CJS F/A-18E/F/G or IDF F-16I are selected by the player
    mod_settings: Optional[ModSettings] = field(default=None)

    def has_access_to_dcs_type(self, unit_type: Type[DcsUnitType]) -> bool:
        # Vehicle and Ship Units
        if any(unit_type == u.dcs_unit_type for u in self.accessible_units):
            return True

        # Statics
        if issubclass(unit_type, StaticType):
            # TODO Improve the statics checking
            # We currently do not have any list or similar to check if a faction has
            # access to a specific static. There we accept any static here
            return True
        return False

    def has_access_to_unit_class(self, unit_class: UnitClass) -> bool:
        return any(unit.unit_class is unit_class for unit in self.accessible_units)

    @cached_property
    def accessible_units(self) -> list[UnitType[Any]]:
        all_units: Iterator[UnitType[Any]] = itertools.chain(
            self.ground_units,
            self.infantry_units,
            self.air_defense_units,
            self.naval_units,
            self.missiles,
            (
                unit
                for preset_group in self.preset_groups
                for unit in preset_group.units
            ),
        )
        return list(set(all_units))

    @property
    def air_defenses(self) -> list[str]:
        """Returns the Air Defense types"""
        # This is used for the faction overview in NewGameWizard
        air_defenses = [a.variant_id for a in self.air_defense_units]
        air_defenses.extend(
            [
                pg.name
                for pg in self.preset_groups
                if any(task.role == GroupRole.AIR_DEFENSE for task in pg.tasks)
            ]
        )
        return sorted(air_defenses)

    @cached_property
    def all_aircrafts(self) -> list[UnitType[Any]]:
        # Migrator can't cope with this, so we need to do it here...
        self.aircraft = set(self.aircraft)
        self.awacs = set(self.awacs)
        self.tankers = set(self.tankers)
        return list(self.aircraft.union(self.awacs.union(self.tankers)))

    @classmethod
    def from_dict(cls: Type[Faction], json: Dict[str, Any]) -> Faction:
        try:
            country = country_with_name(json["country"])
        except KeyError as ex:
            raise KeyError(
                f'Faction\'s country ("{json.get("country")}") is not a valid DCS '
                "country ID"
            ) from ex

        faction = Faction(
            locales=json.get("locales"),
            country=country,
            cargo_ship=ShipUnitType.named(json.get("cargo_ship", "Bulker Handy Wind")),
        )

        faction.name = json.get("name", "")
        if not faction.name:
            raise AssertionError("Faction has no valid name")

        faction.authors = json.get("authors", "")
        faction.description = json.get("description", "")

        faction.aircraft = {AircraftType.named(n) for n in json.get("aircrafts", [])}
        faction.awacs = {AircraftType.named(n) for n in json.get("awacs", [])}
        faction.tankers = {AircraftType.named(n) for n in json.get("tankers", [])}

        faction.frontline_units = {
            GroundUnitType.named(n) for n in json.get("frontline_units", [])
        }
        faction.artillery_units = {
            GroundUnitType.named(n) for n in json.get("artillery_units", [])
        }
        faction.infantry_units = {
            GroundUnitType.named(n) for n in json.get("infantry_units", [])
        }
        faction.logistics_units = {
            GroundUnitType.named(n) for n in json.get("logistics_units", [])
        }
        faction.air_defense_units = {
            GroundUnitType.named(n) for n in json.get("air_defense_units", [])
        }
        faction.missiles = {GroundUnitType.named(n) for n in json.get("missiles", [])}

        faction.naval_units = {
            ShipUnitType.named(n) for n in json.get("naval_units", [])
        }

        faction.preset_groups = [
            ForceGroup.from_preset_group(g) for g in json.get("preset_groups", [])
        ]

        faction.requirements = json.get("requirements", {})

        # First try to load the carriers in the new format which
        # specifies different names for different carrier types
        loaded_carriers = load_carriers(json)

        carriers: List[ShipUnitType] = [
            unit
            for unit in faction.naval_units
            if unit.unit_class
            in [
                UnitClass.AIRCRAFT_CARRIER,
                UnitClass.HELICOPTER_CARRIER,
            ]
        ]
        carrier_names = json.get("carrier_names", [])
        helicopter_carrier_names = json.get("helicopter_carrier_names", [])
        for c in carriers:
            if c.variant_id not in loaded_carriers:
                if c.unit_class == UnitClass.AIRCRAFT_CARRIER:
                    loaded_carriers[c] = carrier_names
                elif c.unit_class == UnitClass.HELICOPTER_CARRIER:
                    loaded_carriers[c] = helicopter_carrier_names

        faction.carriers = loaded_carriers
        faction.naval_units.union(faction.carriers.keys())

        faction.has_jtac = json.get("has_jtac", False)
        jtac_name = json.get("jtac_unit", None)
        if jtac_name is not None:
            faction.jtac_unit = AircraftType.named(jtac_name)
        else:
            faction.jtac_unit = None

        # Load doctrine
        doctrine = json.get("doctrine", "modern")
        if doctrine == "modern":
            faction.doctrine = MODERN_DOCTRINE
        elif doctrine == "coldwar":
            faction.doctrine = COLDWAR_DOCTRINE
        elif doctrine == "ww2":
            faction.doctrine = WWII_DOCTRINE
        else:
            faction.doctrine = MODERN_DOCTRINE

        # Load the building set
        faction.building_set = set()
        building_set = json.get("building_set", "default")
        if building_set == "default":
            faction.building_set.update(DEFAULT_AVAILABLE_BUILDINGS)
        elif building_set == "ww2free":
            faction.building_set.update(WW2_FREE)
        elif building_set == "ww2ally":
            faction.building_set.update(WW2_ALLIES_BUILDINGS)
        elif building_set == "ww2germany":
            faction.building_set.update(WW2_GERMANY_BUILDINGS)
        else:
            faction.building_set.update(DEFAULT_AVAILABLE_BUILDINGS)

        # Add required buildings for the game logic (e.g. ammo, factory..)
        faction.building_set.update(REQUIRED_BUILDINGS)
        faction.building_set.update(IADS_BUILDINGS)

        # Load liveries override
        faction.liveries_overrides = {}
        liveries_overrides = json.get("liveries_overrides", {})
        for name, livery in liveries_overrides.items():
            aircraft = AircraftType.named(name)
            faction.liveries_overrides[aircraft] = [s.lower() for s in livery]

        # Load liveries override for ground forces
        faction.liveries_overrides_ground_forces = {}
        liveries_overrides_ground_forces = json.get(
            "liveries_overrides_ground_forces", {}
        )
        for vehicle_type, livery in liveries_overrides_ground_forces.items():
            faction.liveries_overrides_ground_forces[vehicle_type] = [
                s.lower() for s in livery
            ]

        faction.unrestricted_satnav = json.get("unrestricted_satnav", False)

        return faction

    @property
    def ground_units(self) -> Iterator[GroundUnitType]:
        yield from self.artillery_units
        yield from self.frontline_units
        yield from self.logistics_units

    def infantry_with_class(self, unit_class: UnitClass) -> Iterator[GroundUnitType]:
        for unit in self.infantry_units:
            if unit.unit_class is unit_class:
                yield unit

    def apply_mod_settings(self, mod_settings: Optional[ModSettings] = None) -> None:
        if mod_settings is None:
            if self.mod_settings is None:
                # No mod settings were provided and none were saved for this faction
                # so stop here
                return
            elif self.mod_settings is not None:
                # Saved mod settings were found for this faction,
                # so load them for use
                mod_settings = self.mod_settings
        else:
            # Update the mod settings of this faction
            # so the settings can be applied again on load, if needed
            self.mod_settings = mod_settings

        # aircraft
        if not mod_settings.a4_skyhawk:
            self.remove_aircraft("A-4E-C")
        if not mod_settings.hercules:
            self.remove_aircraft("Hercules")
        if not mod_settings.uh_60l:
            self.remove_aircraft("UH-60L")
            self.remove_aircraft("KC130J")
        if not mod_settings.fa18ef_tanker:
            self.remove_aircraft("Superbug_AITanker")
        if not mod_settings.f4bc_phantom:
            self.remove_aircraft("VSN_F4B")
            self.remove_aircraft("VSN_F4C")
        if not mod_settings.f9f_panther:
            self.remove_aircraft("VSN_F9F")
        if not mod_settings.f15d_baz:
            self.remove_aircraft("F-15D")
        if not mod_settings.f_15_idf:
            eject_F15I()
            if AircraftType.named("F-15I Ra'am") in self.aircraft:
                self.aircraft.remove(AircraftType.named("F-15I Ra'am"))
        else:
            inject_F15I()
            if AircraftType.named("F-15E Strike Eagle (Suite 4+)") in self.aircraft:
                self.aircraft.add(AircraftType.named("F-15I Ra'am"))
        if not mod_settings.f_16_idf:
            self.remove_aircraft("F-16I")
            self.remove_aircraft("F-16D_52")
            self.remove_aircraft("F-16D_50")
            self.remove_aircraft("F-16D_50_NS")
            self.remove_aircraft("F-16D_52_NS")
            self.remove_aircraft("F-16D_Barak_30")
            self.remove_aircraft("F-16D_Barak_40")
            eject_F16I()
        else:
            inject_F16I()
        if not mod_settings.f22_raptor:
            self.remove_aircraft("F-22A")
        if not mod_settings.f84g_thunderjet:
            self.remove_aircraft("VSN_F84G")
        if not mod_settings.f100_supersabre:
            self.remove_aircraft("VSN_F100")
        if not mod_settings.f104_starfighter:
            self.remove_aircraft("VSN_F104C")
            self.remove_aircraft("VSN_F104G")
            self.remove_aircraft("VSN_F104S")
            self.remove_aircraft("VSN_F104S_AG")
        if not mod_settings.f105_thunderchief:
            self.remove_aircraft("VSN_F105D")
            self.remove_aircraft("VSN_F105G")
        if not mod_settings.f106_deltadart:
            self.remove_aircraft("VSN_F106A")
            self.remove_aircraft("VSN_F106B")
        if not mod_settings.a6a_intruder:
            self.remove_aircraft("VSN_A6A")
        if not mod_settings.ea6b_prowler:
            self.remove_aircraft("EA_6B")
        if not mod_settings.jas39_gripen:
            self.remove_aircraft("JAS39Gripen")
            self.remove_aircraft("JAS39Gripen_BVR")
            self.remove_aircraft("JAS39Gripen_AG")
        if not mod_settings.super_etendard:
            self.remove_aircraft("VSN_SEM")
        if not mod_settings.su30_flanker_h:
            self.remove_aircraft("Su-30MKA")
            self.remove_aircraft("Su-30MKI")
            self.remove_aircraft("Su-30MKM")
            self.remove_aircraft("Su-30SM")
        if not mod_settings.su57_felon:
            self.remove_aircraft("Su-57")
        if not mod_settings.ov10a_bronco:
            self.remove_aircraft("Bronco-OV-10A")
        if not mod_settings.a7e_corsair2:
            self.remove_aircraft("A-7E")
        # frenchpack
        if not mod_settings.frenchpack:
            self.remove_vehicle("AMX10RCR")
            self.remove_vehicle("SEPAR")
            self.remove_vehicle("ERC")
            self.remove_vehicle("M120")
            self.remove_vehicle("AA20")
            self.remove_vehicle("TRM2000")
            self.remove_vehicle("TRM2000_Citerne")
            self.remove_vehicle("TRM2000_AA20")
            self.remove_vehicle("TRMMISTRAL")
            self.remove_vehicle("VABH")
            self.remove_vehicle("VAB_RADIO")
            self.remove_vehicle("VAB_50")
            self.remove_vehicle("VIB_VBR")
            self.remove_vehicle("VAB_HOT")
            self.remove_vehicle("VAB_MORTIER")
            self.remove_vehicle("VBL50")
            self.remove_vehicle("VBLANF1")
            self.remove_vehicle("VBL-radio")
            self.remove_vehicle("VBAE")
            self.remove_vehicle("VBAE_MMP")
            self.remove_vehicle("AMX-30B2")
            self.remove_vehicle("Tracma")
            self.remove_vehicle("JTACFP")
            self.remove_vehicle("SHERIDAN")
            self.remove_vehicle("Leclerc_XXI")
            self.remove_vehicle("Toyota_bleu")
            self.remove_vehicle("Toyota_vert")
            self.remove_vehicle("Toyota_desert")
            self.remove_vehicle("Kamikaze")
            self.remove_vehicle("AMX1375")
            self.remove_vehicle("AMX1390")
            self.remove_vehicle("VBCI")
            self.remove_vehicle("T62")
            self.remove_vehicle("T64BV")
            self.remove_vehicle("T72M")
            self.remove_vehicle("KORNET")
        # high digit sams
        if not mod_settings.high_digit_sams:
            self.remove_preset("SA-10B/S-300PS")
            self.remove_preset("SA-12/S-300V")
            self.remove_preset("SA-20/S-300PMU-1")
            self.remove_preset("SA-20B/S-300PMU-2")
            self.remove_preset("SA-23/S-300VM")
            self.remove_preset("SA-17")
            self.remove_preset("KS-19_HDS")
            self.remove_preset("HQ-2")
            self.remove_preset("SA-2/S-75 V-759/5V23")
            self.remove_preset("SA-3/S-125 V-601P/5V27")
            self.remove_vehicle("SAM SA-14 Strela-3 manpad")
            self.remove_vehicle("SAM SA-24 Igla-S manpad")
            self.remove_vehicle("Polyana-D4M1 C2 node")
        if not mod_settings.fa_18efg:
            self.remove_aircraft("FA-18E")
            self.remove_aircraft("FA-18F")
            self.remove_aircraft("EA-18G")
        # spanish naval assets pack
        if not mod_settings.spanishnavypack:
            self.remove_ship("L61")
            self.remove_ship("F100")
            self.remove_ship("F105")
            self.remove_ship("L52")
            self.remove_ship("L02")
            self.remove_ship("DDG39")
        if not mod_settings.irondome:
            self.remove_vehicle("Iron_Dome_David_Sling_CP")
            self.remove_vehicle("IRON_DOME_LN")
            self.remove_vehicle("DAVID_SLING_LN")
            self.remove_vehicle("ELM2084_MMR_AD_RT")
            self.remove_vehicle("ELM2084_MMR_AD_SC")
            self.remove_vehicle("ELM2084_MMR_WLR")
            self.remove_preset("Iron Dome")
            self.remove_preset("Iron Dome (Semicircle)")
            self.remove_preset("David's Sling")
            self.remove_preset("David's Sling (Semicircle)")
        # swedish military assets pack
        if not mod_settings.swedishmilitaryassetspack:
            self.remove_vehicle("BV410_RBS70")
            self.remove_vehicle("BV410_RBS90")
            self.remove_vehicle("LvS_103_Lavett103_Rb103A")
            self.remove_vehicle("LvS_103_Lavett103_Rb103B")
            self.remove_vehicle("LvS_103_Lavett103_HX_Rb103A")
            self.remove_vehicle("LvS_103_Lavett103_HX_Rb103B")
            self.remove_vehicle("LvS_103_StriE103")
            self.remove_vehicle("LvS_103_PM103")
            self.remove_vehicle("LvS_103_PM103_HX")
            self.remove_vehicle("LvS_103_Elverk103")
            self.remove_vehicle("LvKv9040")
            self.remove_vehicle("RBS_70")
            self.remove_vehicle("RBS_90")
            self.remove_vehicle("RBS_98")
            self.remove_vehicle("UndE23")
            self.remove_vehicle("BV410")
            self.remove_vehicle("CV9040")
            self.remove_vehicle("Strv103")
            self.remove_vehicle("Strv121")
            self.remove_vehicle("Strv122")
            self.remove_vehicle("Strv2000")
            self.remove_vehicle("Volvo740")
            self.remove_vehicle("RBS_15KA")
            self.remove_vehicle("AG_90")
            self.remove_vehicle("SwedishinfantryAK4")
            self.remove_vehicle("SwedishinfantryAK5")
            self.remove_vehicle("SwedishinfantryAK5GT")
            self.remove_vehicle("SwedishinfantryKSP90")
            self.remove_vehicle("SwedishinfantryKSP58")
            self.remove_vehicle("SwedishinfantryPskott86")
            self.remove_vehicle("RBS_57")
            self.remove_vehicle("RBS_58")
            self.remove_vehicle("Artillerisystem08")
            self.remove_vehicle("Grkpbv90")
            self.remove_ship("HSwMS_Visby")
            self.remove_ship("Strb90")
            self.remove_aircraft("HKP15B")
            self.remove_preset("LvS-103 Rb103A")
            self.remove_preset("LvS-103 Rb103A Mobile")
            self.remove_preset("LvS-103 Rb103B")
            self.remove_preset("LvS-103 Rb103B Mobile")
        # SWPack
        if not mod_settings.SWPack:
            self.remove_aircraft("AWINGA")
            self.remove_aircraft("AWING")
            self.remove_aircraft("XWING")
            self.remove_aircraft("XWINGAI")
            self.remove_aircraft("TIE_BA")
            self.remove_aircraft("tie_bomber_2")
            self.remove_aircraft("YWINGA")
            self.remove_aircraft("YWING")
            self.remove_aircraft("CORVETTE")
            self.remove_aircraft("CORVETTEA")
            self.remove_aircraft("FAUCON")
            self.remove_aircraft("FAUCON_AI")
            self.remove_aircraft("TIE")
            self.remove_aircraft("TIE_AI")
            self.remove_aircraft("HUNTER")
            self.remove_aircraft("HUNTERA")
            self.remove_aircraft("TIE_INTER")
            self.remove_aircraft("TIE_INTERA")
            self.remove_aircraft("naboo_starfighter")
            self.remove_aircraft("naboo_starfighter_AI")
            self.remove_vehicle("MBT9_REBEL")
            self.remove_vehicle("MBT9_AAA EMPIRE")
            self.remove_vehicle("MBT9_EMPIRE")
            self.remove_vehicle("MBT9_AAA REBEL")
            self.remove_vehicle("Jugger")
            self.remove_vehicle("TB_TT")
            self.remove_vehicle("TR_TT")
            self.remove_vehicle("Gozanti")
            self.remove_ship("Destroyer_carrier")

    def remove_aircraft(self, name: str) -> None:
        for aircraft_set in [self.aircraft, self.awacs, self.tankers]:
            for i in list(aircraft_set):
                if i.dcs_unit_type.id == name:
                    aircraft_set.remove(i)

    def remove_aircraft_by_name(self, name: str) -> None:
        for aircraft_set in [self.aircraft, self.awacs, self.tankers]:
            for i in list(aircraft_set):
                if i.display_name == name:
                    aircraft_set.remove(i)

    def remove_preset(self, name: str) -> None:
        for pg in self.preset_groups:
            if pg.name == name:
                self.preset_groups.remove(pg)

    def remove_vehicle(self, name: str) -> None:
        for sequence in [
            self.frontline_units,
            self.infantry_units,
            self.air_defense_units,
            self.artillery_units,
            self.logistics_units,
        ]:
            for i in list(sequence):
                if i.dcs_unit_type.id == name:
                    sequence.remove(i)

    def remove_ship(self, name: str) -> None:
        for i in list(self.naval_units):
            if i.dcs_unit_type.id == name:
                self.naval_units.remove(i)


def load_ship(name: str) -> Optional[Type[ShipType]]:
    if (ship := getattr(dcs.ships, name, None)) is not None:
        return ship
    logging.error(f"FACTION ERROR : Unable to find {name} in dcs.ships")
    return None


def load_all_ships(data: list[str]) -> List[Type[ShipType]]:
    items = []
    for name in data:
        item = load_ship(name)
        if item is not None:
            items.append(item)
    return items


def load_carriers(json: Dict[str, Any]) -> Dict[ShipUnitType, Set[str]]:
    # Load carriers
    items: Dict[ShipUnitType, Set[str]] = defaultdict(Set[str])
    carriers = json.get("carriers", {})
    for carrier_shiptype, shipnames in carriers.items():
        shiptype = ShipUnitType.named(carrier_shiptype)
        if shiptype is not None:
            items[shiptype] = shipnames
    return items
