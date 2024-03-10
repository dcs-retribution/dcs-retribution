from dataclasses import dataclass
from datetime import timedelta

from game.data.units import UnitClass
from game.utils import Distance, feet, nautical_miles, Speed, knots


@dataclass
class GroundUnitProcurementRatios:
    ratios: dict[UnitClass, float]

    def for_unit_class(self, unit_class: UnitClass) -> float:
        try:
            return self.ratios[unit_class] / sum(self.ratios.values())
        except KeyError:
            return 0.0


@dataclass(frozen=True)
class Doctrine:
    name: str

    cas: bool
    cap: bool
    sead: bool
    strike: bool
    antiship: bool

    #: The minimum distance between the departure airfield and the hold point.
    hold_distance: Distance

    #: The minimum distance between the hold point and the join point.
    push_distance: Distance

    #: The distance between the join point and the ingress point. Only used for the
    #: fallback flight plan layout (when the departure airfield is near a threat zone).
    join_distance: Distance

    #: The maximum distance between the ingress point (beginning of the attack) and
    #: target.
    max_ingress_distance: Distance

    #: The minimum distance between the ingress point (beginning of the attack) and
    #: target.
    min_ingress_distance: Distance

    min_patrol_altitude: Distance
    max_patrol_altitude: Distance

    min_cruise_altitude: Distance
    max_cruise_altitude: Distance

    min_combat_altitude: Distance
    max_combat_altitude: Distance

    #: The duration that CAP flights will remain on-station.
    cap_duration: timedelta

    #: The minimum length of the CAP race track.
    cap_min_track_length: Distance

    #: The maximum length of the CAP race track.
    cap_max_track_length: Distance

    #: The minimum distance between the defended position and the *end* of the
    #: CAP race track.
    cap_min_distance_from_cp: Distance

    #: The maximum distance between the defended position and the *end* of the
    #: CAP race track.
    cap_max_distance_from_cp: Distance

    #: The engagement range of CAP flights. Any enemy aircraft within this range
    #: of the CAP's current position will be engaged by the CAP.
    cap_engagement_range: Distance

    cas_duration: timedelta

    sweep_distance: Distance

    ground_unit_procurement_ratios: GroundUnitProcurementRatios

    rtb_speed: Speed

    sead_escort_spacing: Distance

    escort_spacing: Distance

    sead_escort_engagement_range: Distance

    escort_engagement_range: Distance


MODERN_DOCTRINE = Doctrine(
    "modern",
    cap=True,
    cas=True,
    sead=True,
    strike=True,
    antiship=True,
    hold_distance=nautical_miles(25),
    push_distance=nautical_miles(20),
    join_distance=nautical_miles(20),
    max_ingress_distance=nautical_miles(45),
    min_ingress_distance=nautical_miles(10),
    min_patrol_altitude=feet(15000),
    max_patrol_altitude=feet(33000),
    min_cruise_altitude=feet(10000),
    max_cruise_altitude=feet(40000),
    min_combat_altitude=feet(1000),
    max_combat_altitude=feet(35000),
    cap_duration=timedelta(minutes=30),
    cap_min_track_length=nautical_miles(15),
    cap_max_track_length=nautical_miles(40),
    cap_min_distance_from_cp=nautical_miles(10),
    cap_max_distance_from_cp=nautical_miles(40),
    cap_engagement_range=nautical_miles(50),
    cas_duration=timedelta(minutes=30),
    sweep_distance=nautical_miles(60),
    ground_unit_procurement_ratios=GroundUnitProcurementRatios(
        {
            UnitClass.TANK: 3,
            UnitClass.ATGM: 2,
            UnitClass.APC: 2,
            UnitClass.IFV: 3,
            UnitClass.ARTILLERY: 1,
            UnitClass.SHORAD: 2,
            UnitClass.RECON: 1,
        }
    ),
    rtb_speed=knots(500),
    sead_escort_spacing=feet(1000),
    escort_spacing=feet(2000),
    sead_escort_engagement_range=nautical_miles(40),
    escort_engagement_range=nautical_miles(30),
)

COLDWAR_DOCTRINE = Doctrine(
    name="coldwar",
    cap=True,
    cas=True,
    sead=True,
    strike=True,
    antiship=True,
    hold_distance=nautical_miles(15),
    push_distance=nautical_miles(10),
    join_distance=nautical_miles(10),
    max_ingress_distance=nautical_miles(30),
    min_ingress_distance=nautical_miles(10),
    min_patrol_altitude=feet(10000),
    max_patrol_altitude=feet(24000),
    min_cruise_altitude=feet(10000),
    max_cruise_altitude=feet(30000),
    min_combat_altitude=feet(1000),
    max_combat_altitude=feet(25000),
    cap_duration=timedelta(minutes=30),
    cap_min_track_length=nautical_miles(12),
    cap_max_track_length=nautical_miles(24),
    cap_min_distance_from_cp=nautical_miles(8),
    cap_max_distance_from_cp=nautical_miles(25),
    cap_engagement_range=nautical_miles(35),
    cas_duration=timedelta(minutes=30),
    sweep_distance=nautical_miles(40),
    ground_unit_procurement_ratios=GroundUnitProcurementRatios(
        {
            UnitClass.TANK: 4,
            UnitClass.ATGM: 2,
            UnitClass.APC: 3,
            UnitClass.IFV: 2,
            UnitClass.ARTILLERY: 1,
            UnitClass.SHORAD: 2,
            UnitClass.RECON: 1,
        }
    ),
    rtb_speed=knots(450),
    sead_escort_spacing=feet(500),
    escort_spacing=feet(1000),
    sead_escort_engagement_range=nautical_miles(25),
    escort_engagement_range=nautical_miles(20),
)

WWII_DOCTRINE = Doctrine(
    name="ww2",
    cap=True,
    cas=True,
    sead=False,
    strike=True,
    antiship=True,
    hold_distance=nautical_miles(10),
    push_distance=nautical_miles(5),
    join_distance=nautical_miles(5),
    max_ingress_distance=nautical_miles(7),
    min_ingress_distance=nautical_miles(5),
    min_patrol_altitude=feet(4000),
    max_patrol_altitude=feet(15000),
    min_cruise_altitude=feet(5000),
    max_cruise_altitude=feet(30000),
    min_combat_altitude=feet(1000),
    max_combat_altitude=feet(10000),
    cap_duration=timedelta(minutes=30),
    cap_min_track_length=nautical_miles(8),
    cap_max_track_length=nautical_miles(18),
    cap_min_distance_from_cp=nautical_miles(0),
    cap_max_distance_from_cp=nautical_miles(5),
    cap_engagement_range=nautical_miles(20),
    cas_duration=timedelta(minutes=30),
    sweep_distance=nautical_miles(10),
    ground_unit_procurement_ratios=GroundUnitProcurementRatios(
        {
            UnitClass.TANK: 3,
            UnitClass.ATGM: 3,
            UnitClass.APC: 3,
            UnitClass.ARTILLERY: 1,
            UnitClass.SHORAD: 3,
            UnitClass.RECON: 1,
        }
    ),
    rtb_speed=knots(300),
    sead_escort_spacing=feet(100),
    escort_spacing=feet(200),
    sead_escort_engagement_range=nautical_miles(10),
    escort_engagement_range=nautical_miles(5),
)

ALL_DOCTRINES = [
    COLDWAR_DOCTRINE,
    MODERN_DOCTRINE,
    WWII_DOCTRINE,
]
