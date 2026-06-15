from __future__ import annotations

from enum import unique, Enum


@unique
class UnitClass(Enum):
    UNKNOWN = "Unknown"
    AAA = "AAA"
    AIRCRAFT_CARRIER = "AircraftCarrier"
    APC = "APC"
    ARTILLERY = "Artillery"
    ATGM = "ATGM"
    BOAT = "Boat"
    COMMAND_POST = "CommandPost"
    CRUISER = "Cruiser"
    DESTROYER = "Destroyer"
    EARLY_WARNING_RADAR = "EarlyWarningRadar"
    FORTIFICATION = "Fortification"
    FRIGATE = "Frigate"
    HELICOPTER = "Helicopter"
    HELICOPTER_CARRIER = "HelicopterCarrier"
    IFV = "IFV"
    INFANTRY = "Infantry"
    LANDING_SHIP = "LandingShip"
    LAUNCHER = "Launcher"
    LOGISTICS = "Logistics"
    MANPAD = "Manpad"
    MISSILE = "Missile"
    ANTISHIP_MISSILE = "AntiShipMissile"
    OPTICAL_TRACKER = "OpticalTracker"
    PLANE = "Plane"
    POWER = "Power"
    RECON = "Recon"
    SEARCH_LIGHT = "SearchLight"
    SEARCH_RADAR = "SearchRadar"
    SEARCH_TRACK_RADAR = "SearchTrackRadar"
    SHORAD = "SHORAD"
    SPECIALIZED_RADAR = "SpecializedRadar"
    SUBMARINE = "Submarine"
    TANK = "Tank"
    TELAR = "TELAR"
    TRACK_RADAR = "TrackRadar"


# All UnitClasses which can have AntiAir capabilities
ANTI_AIR_UNIT_CLASSES = [
    UnitClass.AAA,
    UnitClass.AIRCRAFT_CARRIER,
    UnitClass.CRUISER,
    UnitClass.DESTROYER,
    UnitClass.EARLY_WARNING_RADAR,
    UnitClass.FRIGATE,
    UnitClass.HELICOPTER_CARRIER,
    UnitClass.LAUNCHER,
    UnitClass.MANPAD,
    UnitClass.SEARCH_RADAR,
    UnitClass.SEARCH_TRACK_RADAR,
    UnitClass.SPECIALIZED_RADAR,
    UnitClass.SHORAD,
    UnitClass.SUBMARINE,
    UnitClass.TELAR,
    UnitClass.TRACK_RADAR,
]

# Mobile, self-contained point air-defense unit classes. A generated DCS group
# that contains any of these should be hidden on the MFD/datalink even when the
# group's own hide_on_mfd flag is not set -- e.g. a SHORAD/AAA/MANPAD escort
# placed inside an armor or missile group, which would otherwise inherit the
# parent group's visible flag and betray its position on the datalink.
#
# Deliberately excludes TELAR and the radar/launcher classes so standalone
# MERAD/LORAD SAM sites (SA-6/11, SA-2/3/5/10, etc.) stay visible/targetable for
# SEAD.
MOBILE_AIR_DEFENSE_UNIT_CLASSES = frozenset(
    {
        UnitClass.AAA,
        UnitClass.SHORAD,
        UnitClass.MANPAD,
    }
)
