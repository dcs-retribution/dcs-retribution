from collections.abc import Iterator
from dataclasses import Field, dataclass, field, fields
from datetime import timedelta
from enum import Enum, unique
from typing import Any, Dict, Optional

from dcs.forcedoptions import ForcedOptions

from .booleanoption import boolean_option
from .boundedfloatoption import bounded_float_option
from .boundedintoption import bounded_int_option
from .choicesoption import choices_option
from .minutesoption import minutes_option
from .optiondescription import OptionDescription, SETTING_DESCRIPTION_KEY
from .skilloption import skill_option
from ..ato.starttype import StartType

Views = ForcedOptions.Views


@unique
class AutoAtoBehavior(Enum):
    Disabled = "Disabled"
    Never = "Never assign player pilots"
    Default = "No preference"
    Prefer = "Prefer player pilots"


@unique
class NightMissions(Enum):
    DayAndNight = "nightmissions_nightandday"
    OnlyDay = "nightmissions_onlyday"
    OnlyNight = "nightmissions_onlynight"


DIFFICULTY_PAGE = "Difficulty"

AI_DIFFICULTY_SECTION = "AI Difficulty"
MISSION_DIFFICULTY_SECTION = "Mission Difficulty"
MISSION_RESTRICTIONS_SECTION = "Mission Restrictions"

CAMPAIGN_MANAGEMENT_PAGE = "Campaign Management"

GENERAL_SECTION = "General"
PILOTS_AND_SQUADRONS_SECTION = "Pilots and Squadrons"
HQ_AUTOMATION_SECTION = "HQ Automation"
FLIGHT_PLANNER_AUTOMATION = "Flight Planner Automation"

CAMPAIGN_DOCTRINE_PAGE = "Campaign Doctrine"
DOCTRINE_DISTANCES_SECTION = "Doctrine distances"

PRETENSE_PAGE = "Pretense"

MISSION_GENERATOR_PAGE = "Mission Generator"

GAMEPLAY_SECTION = "Gameplay"

# TODO: Make sections a type and add headers.
# This section had the header: "Disabling settings below may improve performance, but
# will impact the overall quality of the experience."
PERFORMANCE_SECTION = "Performance"


@dataclass
class Settings:
    version: Optional[str] = None

    # Difficulty settings
    # AI Difficulty
    player_skill: str = skill_option(
        "Player coalition skill",
        page=DIFFICULTY_PAGE,
        section=AI_DIFFICULTY_SECTION,
        default="High",
    )
    enemy_skill: str = skill_option(
        "Enemy coalition skill",
        page=DIFFICULTY_PAGE,
        section=AI_DIFFICULTY_SECTION,
        default="High",
    )
    enemy_vehicle_skill: str = skill_option(
        "Enemy AA and vehicles skill",
        page=DIFFICULTY_PAGE,
        section=AI_DIFFICULTY_SECTION,
        default="High",
    )
    player_income_multiplier: float = bounded_float_option(
        "Player income multiplier",
        page=DIFFICULTY_PAGE,
        section=AI_DIFFICULTY_SECTION,
        min=0,
        max=5,
        divisor=10,
        default=1.0,
    )
    enemy_income_multiplier: float = bounded_float_option(
        "Enemy income multiplier",
        page=DIFFICULTY_PAGE,
        section=AI_DIFFICULTY_SECTION,
        min=0,
        max=5,
        divisor=10,
        default=1.0,
    )
    invulnerable_player_pilots: bool = boolean_option(
        "Player pilots cannot be killed",
        page=DIFFICULTY_PAGE,
        section=AI_DIFFICULTY_SECTION,
        detail=(
            "Aircraft are vulnerable, but the player's pilot will be returned to the "
            "squadron at the end of the mission"
        ),
        default=True,
    )
    # Mission Difficulty
    manpads: bool = boolean_option(
        "Manpads on frontlines",
        page=DIFFICULTY_PAGE,
        section=MISSION_DIFFICULTY_SECTION,
        default=True,
    )
    night_day_missions: NightMissions = choices_option(
        "Night/day mission options",
        page=DIFFICULTY_PAGE,
        section=MISSION_DIFFICULTY_SECTION,
        choices={
            "Generate night and day missions": NightMissions.DayAndNight,
            "Only generate day missions": NightMissions.OnlyDay,
            "Only generate night missions": NightMissions.OnlyNight,
        },
        default=NightMissions.DayAndNight,
    )
    # Mission Restrictions
    labels: str = choices_option(
        "In game labels",
        page=DIFFICULTY_PAGE,
        section=MISSION_RESTRICTIONS_SECTION,
        choices=["Full", "Abbreviated", "Dot Only", "Neutral Dot", "Off"],
        default="Full",
    )
    map_coalition_visibility: Views = choices_option(
        "Map visibility options",
        page=DIFFICULTY_PAGE,
        section=MISSION_RESTRICTIONS_SECTION,
        choices={
            "All": Views.All,
            "Fog of war": Views.Allies,
            "Allies only": Views.OnlyAllies,
            "Own aircraft only": Views.MyAircraft,
            "Map only": Views.OnlyMap,
        },
        default=Views.All,
    )
    external_views_allowed: bool = boolean_option(
        "Allow external views",
        DIFFICULTY_PAGE,
        MISSION_RESTRICTIONS_SECTION,
        default=True,
    )

    easy_communication: Optional[bool] = choices_option(
        "Easy Communication",
        page=DIFFICULTY_PAGE,
        section=MISSION_RESTRICTIONS_SECTION,
        choices={"Player preference": None, "Enforced on": True, "Enforced off": False},
        default=None,
    )

    battle_damage_assessment: Optional[bool] = choices_option(
        "Battle damage assessment",
        page=DIFFICULTY_PAGE,
        section=MISSION_RESTRICTIONS_SECTION,
        choices={"Player preference": None, "Enforced on": True, "Enforced off": False},
        default=None,
    )

    # Campaign management
    # General
    squadron_random_chance: int = bounded_int_option(
        "Percentage of randomly selected aircraft types (only for generated squadrons)",
        page=CAMPAIGN_MANAGEMENT_PAGE,
        section=GENERAL_SECTION,
        default=50,
        min=0,
        max=100,
        detail=(
            "<p>Aircraft type selection is governed by the campaign and the squadron definitions available to "
            "Retribution. Squadrons are generated by Retribution if the faction does not have access to the campaign "
            "designer's squadron/aircraft definitions. Use the above to increase/decrease aircraft variety by making "
            "some selections random instead of picking aircraft types from a priority list.</p>"
        ),
    )
    restrict_weapons_by_date: bool = boolean_option(
        "Restrict weapons by date (WIP)",
        page=CAMPAIGN_MANAGEMENT_PAGE,
        section=GENERAL_SECTION,
        default=False,
        detail=(
            "Restricts weapon availability based on the campaign date. Data is "
            "extremely incomplete so does not affect all weapons."
        ),
    )
    prefer_squadrons_with_matching_primary_task: bool = boolean_option(
        "Prefer squadrons with matching primary task when planning missions",
        page=CAMPAIGN_MANAGEMENT_PAGE,
        section=GENERAL_SECTION,
        default=False,
        detail=(
            "If checked, squadrons with a primary task matching the mission will be "
            "preferred even if there is a closer squadron capable of the mission as a "
            "secondary task. Expect longer flights, but squadrons will be more often "
            "assigned to their primary task."
        ),
    )
    # CAMPAIGN DOCTRINE
    autoplan_tankers_for_strike: bool = boolean_option(
        "Auto-planner plans refueling flights for Strike packages",
        page=CAMPAIGN_DOCTRINE_PAGE,
        section=GENERAL_SECTION,
        default=True,
        invert=False,
        detail=(
            "If checked, the auto-planner will include tankers in Strike packages, "
            "provided the faction has access to them."
        ),
    )
    autoplan_tankers_for_oca: bool = boolean_option(
        "Auto-planner plans refueling flights for OCA packages",
        page=CAMPAIGN_DOCTRINE_PAGE,
        section=GENERAL_SECTION,
        default=True,
        invert=False,
        detail=(
            "If checked, the auto-planner will include tankers in OCA packages, "
            "provided the faction has access to them."
        ),
    )
    autoplan_tankers_for_dead: bool = boolean_option(
        "Auto-planner plans refueling flights for DEAD packages",
        page=CAMPAIGN_DOCTRINE_PAGE,
        section=GENERAL_SECTION,
        default=True,
        invert=False,
        detail=(
            "If checked, the auto-planner will include tankers in DEAD packages, "
            "provided the faction has access to them."
        ),
    )
    oca_target_autoplanner_min_aircraft_count: int = bounded_int_option(
        "Minimum number of aircraft (at vulnerable airfields) for auto-planner to plan OCA packages against",
        page=CAMPAIGN_DOCTRINE_PAGE,
        section=GENERAL_SECTION,
        default=20,
        min=0,
        max=100,
        detail=(
            "How many aircraft there has to be at an airfield for "
            "the auto-planner to plan an OCA strike against it."
        ),
    )
    opfor_autoplanner_aggressiveness: int = bounded_int_option(
        "OPFOR auto-planner aggressiveness (%)",
        page=CAMPAIGN_DOCTRINE_PAGE,
        section=GENERAL_SECTION,
        default=20,
        min=0,
        max=100,
        detail=(
            "Chance (larger number -> higher chance) that the OPFOR AI "
            "auto-planner will take risks and plan flights against targets "
            "within threatened airspace."
        ),
    )
    heli_combat_alt_agl: int = bounded_int_option(
        "Helicopter combat altitude (feet AGL)",
        page=CAMPAIGN_DOCTRINE_PAGE,
        section=GENERAL_SECTION,
        default=200,
        min=1,
        max=10000,
        detail=(
            "Altitude for helicopters in feet AGL while flying between combat waypoints."
            " Combat waypoints are considered INGRESS, CAS, TGT, EGRESS & SPLIT."
            " In campaigns in more mountainous areas, you might want to increase this "
            "setting to avoid the AI flying into the terrain."
        ),
    )
    heli_cruise_alt_agl: int = bounded_int_option(
        "Helicopter cruise altitude (feet AGL)",
        page=CAMPAIGN_DOCTRINE_PAGE,
        section=GENERAL_SECTION,
        default=500,
        min=1,
        max=10000,
        detail=(
            "Altitude for helicopters in feet AGL while flying between non-combat waypoints."
            " In campaigns in more mountainous areas, you might want to increase this "
            "setting to avoid the AI flying into the terrain."
        ),
    )
    atflir_autoswap: bool = boolean_option(
        "Auto-swap ATFLIR to LITENING",
        page=CAMPAIGN_DOCTRINE_PAGE,
        section=GENERAL_SECTION,
        default=True,
        detail=(
            "Automatically swaps ATFLIR to LITENING pod for newly generated land-based F/A-18 flights "
            "without having to change the payload. <u>Takes effect after current turn!</u>"
        ),
    )
    ai_jettison_empty_tanks: bool = boolean_option(
        "Enable AI empty fuel tank jettison",
        page=CAMPAIGN_DOCTRINE_PAGE,
        section=GENERAL_SECTION,
        default=False,
        detail="AI will jettison their fuel tanks as soon as they're empty.",
    )
    max_plane_altitude_offset: int = bounded_int_option(
        "Maximum randomized altitude offset (x1000 ft) for airplanes.",
        page=CAMPAIGN_DOCTRINE_PAGE,
        section=GENERAL_SECTION,
        min=0,
        max=5,
        default=2,
        detail="Creates a randomized altitude offset for airplanes.",
    )

    player_startup_time: int = bounded_int_option(
        "Player startup time",
        page=CAMPAIGN_DOCTRINE_PAGE,
        section=GENERAL_SECTION,
        default=10,
        min=0,
        max=100,
        detail=(
            "The startup time allocated to player flights (default : 10 minutes, AI is 2 minutes). "
            "Packages have to be planned again for this to take effect. "
        ),
    )

    # Doctrine Distances Section
    airbase_threat_range: int = bounded_int_option(
        "Airbase threat range (NM)",
        page=CAMPAIGN_DOCTRINE_PAGE,
        section=DOCTRINE_DISTANCES_SECTION,
        default=100,
        min=0,
        max=300,
        detail=(
            "Will impact both defensive (BARCAP) and offensive flights. Also has a performance impact, "
            "lower threat range generally means less BARCAPs are planned."
        ),
    )
    cas_engagement_range_distance: int = bounded_int_option(
        "CAS engagement range (NM)",
        page=CAMPAIGN_DOCTRINE_PAGE,
        section=DOCTRINE_DISTANCES_SECTION,
        default=10,
        min=0,
        max=100,
    )
    armed_recon_engagement_range_distance: int = bounded_int_option(
        "Armed Recon engagement range (NM)",
        page=CAMPAIGN_DOCTRINE_PAGE,
        section=DOCTRINE_DISTANCES_SECTION,
        default=5,
        min=0,
        max=25,
    )
    sead_sweep_engagement_range_distance: int = bounded_int_option(
        "SEAD Sweep engagement range (NM)",
        page=CAMPAIGN_DOCTRINE_PAGE,
        section=DOCTRINE_DISTANCES_SECTION,
        default=30,
        min=0,
        max=100,
    )
    sead_threat_buffer_min_distance: int = bounded_int_option(
        "SEAD Escort/Sweep threat buffer distance (NM)",
        page=CAMPAIGN_DOCTRINE_PAGE,
        section=DOCTRINE_DISTANCES_SECTION,
        default=5,
        min=0,
        max=100,
        detail=(
            "How close to known threats will the SEAD Escort / SEAD Sweep engagement zone extend."
        ),
    )
    tarcap_threat_buffer_min_distance: int = bounded_int_option(
        "TARCAP threat buffer distance (NM)",
        page=CAMPAIGN_DOCTRINE_PAGE,
        section=DOCTRINE_DISTANCES_SECTION,
        default=20,
        min=0,
        max=100,
        detail=("How close to known threats will the TARCAP racetrack extend."),
    )
    aewc_threat_buffer_min_distance: int = bounded_int_option(
        "AEW&C threat buffer distance (NM)",
        page=CAMPAIGN_DOCTRINE_PAGE,
        section=DOCTRINE_DISTANCES_SECTION,
        default=80,
        min=0,
        max=300,
        detail=(
            "How far, at minimum, will AEW&C racetracks be planned "
            "to known threat zones."
        ),
    )
    tanker_threat_buffer_min_distance: int = bounded_int_option(
        "Theater tanker threat buffer distance (NM)",
        page=CAMPAIGN_DOCTRINE_PAGE,
        section=DOCTRINE_DISTANCES_SECTION,
        default=70,
        min=0,
        max=300,
        detail=(
            "How far, at minimum, will theater tanker racetracks be "
            "planned to known threat zones."
        ),
    )
    max_mission_range_planes: int = bounded_int_option(
        "Auto-planner maximum mission range for airplanes (NM)",
        page=CAMPAIGN_DOCTRINE_PAGE,
        section=DOCTRINE_DISTANCES_SECTION,
        default=150,
        min=150,
        max=1000,
        detail=(
            "The maximum mission distance that's used by the auto-planner for airplanes. "
            "This setting won't take effect when a larger "
            "range is defined in the airplane's yaml specification."
        ),
    )
    max_mission_range_helicopters: int = bounded_int_option(
        "Auto-planner maximum mission range for helicopters (NM)",
        page=CAMPAIGN_DOCTRINE_PAGE,
        section=DOCTRINE_DISTANCES_SECTION,
        default=100,
        min=50,
        max=1000,
        detail=(
            "The maximum mission distance that's used by the auto-planner for helicopters. "
            "This setting won't take effect when a larger "
            "range is defined in the helicopter's yaml specification."
        ),
    )

    # Pilots and Squadrons
    ai_pilot_levelling: bool = boolean_option(
        "Allow AI pilot leveling",
        CAMPAIGN_MANAGEMENT_PAGE,
        PILOTS_AND_SQUADRONS_SECTION,
        default=True,
        detail=(
            "Set whether or not AI pilots will level up after completing a number of"
            " sorties. Since pilot level affects the AI skill, you may wish to disable"
            " this, lest you face an Ace!"
        ),
    )
    #: Feature flag for squadron limits.
    enable_squadron_pilot_limits: bool = boolean_option(
        "Enable per-squadron pilot limits",
        CAMPAIGN_MANAGEMENT_PAGE,
        PILOTS_AND_SQUADRONS_SECTION,
        default=True,
        detail=(
            "If set, squadrons will be limited to a maximum number of pilots and dead "
            "pilots will replenish at a fixed rate, each defined with the settings "
            "below. Auto-purchase may buy aircraft for which there are no pilots"
            "available, so this feature is still a work-in-progress."
        ),
    )
    #: The maximum number of pilots a squadron can have at one time. Changing this after
    #: the campaign has started will have no immediate effect; pilots already in the
    #: squadron will not be removed if the limit is lowered and pilots will not be
    #: immediately created if the limit is raised.
    squadron_pilot_limit: int = bounded_int_option(
        "Maximum number of pilots per squadron",
        CAMPAIGN_MANAGEMENT_PAGE,
        PILOTS_AND_SQUADRONS_SECTION,
        default=16,
        min=6,
        max=72,
        detail=(
            "Sets the maximum number of pilots a squadron may have active. "
            "Changing this value will not have an immediate effect, but will alter "
            "replenishment for future turns."
        ),
    )
    #: The number of pilots a squadron can replace per turn.
    squadron_replenishment_rate: int = bounded_int_option(
        "Squadron pilot replenishment rate",
        CAMPAIGN_MANAGEMENT_PAGE,
        PILOTS_AND_SQUADRONS_SECTION,
        default=4,
        min=1,
        max=20,
        detail=(
            "Sets the maximum number of pilots that will be recruited to each squadron "
            "at the end of each turn. Squadrons will not recruit new pilots beyond the "
            "pilot limit, but each squadron with room for more pilots will recruit "
            "this many pilots each turn up to the limit."
        ),
    )
    # Feature flag for squadron limits.
    enable_squadron_aircraft_limits: bool = boolean_option(
        "Enable per-squadron aircraft limits",
        CAMPAIGN_MANAGEMENT_PAGE,
        PILOTS_AND_SQUADRONS_SECTION,
        default=False,
        detail=(
            "If set, squadrons will not be able to buy more aircraft than the configured maximum."
        ),
    )

    # HQ Automation
    automate_runway_repair: bool = boolean_option(
        "Automate runway repairs",
        CAMPAIGN_MANAGEMENT_PAGE,
        HQ_AUTOMATION_SECTION,
        default=False,
    )
    automate_front_line_reinforcements: bool = boolean_option(
        "Automate front-line purchases",
        CAMPAIGN_MANAGEMENT_PAGE,
        HQ_AUTOMATION_SECTION,
        default=False,
    )
    automate_aircraft_reinforcements: bool = boolean_option(
        "Automate aircraft purchases",
        CAMPAIGN_MANAGEMENT_PAGE,
        HQ_AUTOMATION_SECTION,
        default=False,
    )
    auto_ato_behavior: AutoAtoBehavior = choices_option(
        "Automatic package planning behavior",
        CAMPAIGN_MANAGEMENT_PAGE,
        HQ_AUTOMATION_SECTION,
        default=AutoAtoBehavior.Default,
        choices={v.value: v for v in AutoAtoBehavior},
        detail=(
            "Aircraft auto-purchase is directed by the auto-planner, so disabling "
            "auto-planning disables auto-purchase."
        ),
    )
    auto_ato_behavior_awacs: bool = boolean_option(
        "Automatic AWACS package planning",
        CAMPAIGN_MANAGEMENT_PAGE,
        HQ_AUTOMATION_SECTION,
        default=True,
    )
    auto_ato_behavior_tankers: bool = boolean_option(
        "Automatic Theater tanker package planning",
        CAMPAIGN_MANAGEMENT_PAGE,
        HQ_AUTOMATION_SECTION,
        default=False,
    )
    auto_ato_player_missions_asap: bool = boolean_option(
        "Automatically generated packages with players are scheduled ASAP",
        CAMPAIGN_MANAGEMENT_PAGE,
        HQ_AUTOMATION_SECTION,
        default=True,
    )
    automate_front_line_stance: bool = boolean_option(
        "Automatically manage front line stances",
        CAMPAIGN_MANAGEMENT_PAGE,
        HQ_AUTOMATION_SECTION,
        default=True,
    )
    auto_procurement_balance: int = bounded_int_option(
        "AI ground unit procurement budget ratio (%) for OWNFOR",
        CAMPAIGN_MANAGEMENT_PAGE,
        HQ_AUTOMATION_SECTION,
        min=0,
        max=100,
        default=50,
        detail=(
            "Ratio (larger number -> more budget for ground units) "
            "that indicates how the AI procurement planner should "
            "spend its budget."
        ),
    )
    frontline_reserves_factor: int = bounded_int_option(
        "AI ground unit front-line reserves factor (%) for OWNFOR",
        CAMPAIGN_MANAGEMENT_PAGE,
        HQ_AUTOMATION_SECTION,
        min=0,
        max=1000,
        default=130,
        detail=(
            "Factor to be multiplied with the control point's unit count limit "
            "to calculate the procurement target for reserve troops at front-lines."
        ),
    )
    reserves_procurement_target: int = bounded_int_option(
        "AI ground unit reserves procurement target for OWNFOR",
        CAMPAIGN_MANAGEMENT_PAGE,
        HQ_AUTOMATION_SECTION,
        min=0,
        max=1000,
        default=10,
        detail=(
            "The number of units that will be bought as reserves for applicable control points."
        ),
    )
    auto_procurement_balance_red: int = bounded_int_option(
        "AI ground unit procurement budget ratio (%) for OPFOR",
        CAMPAIGN_MANAGEMENT_PAGE,
        HQ_AUTOMATION_SECTION,
        min=0,
        max=100,
        default=50,
        detail=(
            "Ratio (larger number -> more budget for ground units) "
            "that indicates how the AI procurement planner should "
            "spend its budget."
        ),
    )
    frontline_reserves_factor_red: int = bounded_int_option(
        "AI ground unit front-line reserves factor (%) for OPFOR",
        CAMPAIGN_MANAGEMENT_PAGE,
        HQ_AUTOMATION_SECTION,
        min=0,
        max=1000,
        default=130,
        detail=(
            "Factor to be multiplied with the control point's unit count limit "
            "to calculate the procurement target for reserve troops at front-lines."
        ),
    )
    reserves_procurement_target_red: int = bounded_int_option(
        "AI ground unit reserves procurement target for OPFOR",
        CAMPAIGN_MANAGEMENT_PAGE,
        HQ_AUTOMATION_SECTION,
        min=0,
        max=1000,
        default=10,
        detail=(
            "The number of units that will be bought as reserves for applicable control points."
        ),
    )

    # Flight Planner Automation
    #: The weight used for 2-ships.
    fpa_2ship_weight: int = bounded_int_option(
        "2-ship weight factor (WF2)",
        CAMPAIGN_MANAGEMENT_PAGE,
        FLIGHT_PLANNER_AUTOMATION,
        default=50,
        min=0,
        max=100,
        detail=(
            "Used as a distribution to randomize 2/3/4-ships for BARCAP, CAS, OCA & ANTI-SHIP flights. "
            "The weight W_i is calculated according to the following formula: &#10;&#13;"
            "W_i = WF_i / (WF2 + WF3 + WF4)"
        ),
    )
    #: The weight used for 3-ships.
    fpa_3ship_weight: int = bounded_int_option(
        "3-ship weight factor (WF3)",
        CAMPAIGN_MANAGEMENT_PAGE,
        FLIGHT_PLANNER_AUTOMATION,
        default=35,
        min=0,
        max=100,
        detail="See 2-ship weight factor (WF3)",
    )
    fpa_4ship_weight: int = bounded_int_option(
        "4-ship weight factor (WF4)",
        CAMPAIGN_MANAGEMENT_PAGE,
        FLIGHT_PLANNER_AUTOMATION,
        default=15,
        min=0,
        max=100,
        detail="See 2-ship weight factor (WF4)",
    )

    # Mission Generator
    # Gameplay
    fast_forward_to_first_contact: bool = boolean_option(
        "Fast forward mission to first contact (WIP)",
        page=MISSION_GENERATOR_PAGE,
        section=GAMEPLAY_SECTION,
        default=False,
        detail=(
            "If enabled, the mission will be generated at the point of first contact."
        ),
    )
    player_mission_interrupts_sim_at: Optional[StartType] = choices_option(
        "Player missions interrupt fast forward",
        page=MISSION_GENERATOR_PAGE,
        section=GAMEPLAY_SECTION,
        default=StartType.COLD,
        choices={
            "Never": None,
            "At startup time": StartType.COLD,
            "At taxi time": StartType.WARM,
            "At takeoff time": StartType.RUNWAY,
        },
        detail=(
            "Determines what player mission states will interrupt fast-forwarding to "
            "first contact, if enabled. If never is selected player missions will not "
            "impact simulation and player missions may be generated mid-flight. The "
            "other options will cause the mission to be generated as soon as a player "
            "mission reaches the set state or at first contact, whichever comes first."
        ),
    )
    auto_resolve_combat: bool = boolean_option(
        "Auto-resolve combat during fast-forward (WIP)",
        page=MISSION_GENERATOR_PAGE,
        section=GAMEPLAY_SECTION,
        default=False,
        detail=(
            "If enabled, aircraft entering combat during fast forward will have their "
            "combat auto-resolved after a period of time. This allows the simulation "
            "to advance further into the mission before requiring mission generation, "
            "but simulation is currently very rudimentary so may result in huge losses."
        ),
    )
    supercarrier: bool = boolean_option(
        "Use supercarrier module",
        MISSION_GENERATOR_PAGE,
        GAMEPLAY_SECTION,
        default=False,
    )
    generate_marks: bool = boolean_option(
        "Put objective markers on the map",
        MISSION_GENERATOR_PAGE,
        GAMEPLAY_SECTION,
        default=True,
    )
    generate_dark_kneeboard: bool = boolean_option(
        "Generate dark kneeboard",
        MISSION_GENERATOR_PAGE,
        GAMEPLAY_SECTION,
        default=False,
        detail=(
            "Dark kneeboard for night missions. This will likely make the kneeboard on "
            "the pilot leg unreadable."
        ),
    )
    never_delay_player_flights: bool = boolean_option(
        "Player flights ignore TOT and spawn immediately",
        MISSION_GENERATOR_PAGE,
        GAMEPLAY_SECTION,
        default=True,
        detail=(
            "Does not adjust package waypoint times. Should not be used if players "
            "have runway or in-air starts."
        ),
        tooltip=(
            "Always spawns player aircraft immediately, even if their start time is "
            "more than 10 minutes after the start of the mission. <strong>This does "
            "not alter the timing of your mission. Your TOT will not change. This "
            "option only allows the player to wait on the ground.</strong>"
        ),
    )
    untasked_opfor_client_slots: bool = boolean_option(
        "Convert untasked OPFOR aircraft into client slots",
        page=MISSION_GENERATOR_PAGE,
        section=GAMEPLAY_SECTION,
        default=False,
        detail=(
            "Warning: Enabling this will significantly reduce the number of "
            "targets available for OCA/Aircraft missions."
        ),
    )
    default_start_type: StartType = choices_option(
        "Default start type for AI aircraft",
        page=MISSION_GENERATOR_PAGE,
        section=GAMEPLAY_SECTION,
        choices={v.value: v for v in StartType},
        default=StartType.COLD,
        detail=(
            "Warning: Options other than Cold will significantly reduce the number of "
            "targets available for OCA/Aircraft missions, and OCA/Aircraft flights "
            "will not be included in automatically planned OCA packages."
        ),
    )
    default_start_type_client: StartType = choices_option(
        "Default start type for Player flights",
        page=MISSION_GENERATOR_PAGE,
        section=GAMEPLAY_SECTION,
        choices={v.value: v for v in StartType},
        default=StartType.COLD,
        detail=("Default start type for flights containing Player/Client slots."),
    )
    nevatim_parking_fix: bool = boolean_option(
        "Force air-starts for aircraft at Nevatim and Ramon Airbase inoperable parking slots",
        page=MISSION_GENERATOR_PAGE,
        section=GAMEPLAY_SECTION,
        default=False,  # TODO: set to False or remove this when DCS is fixed
        detail=(
            "Air-starts forced for all aircraft at Nevatim and Ramon Airbase except parking slots "
            "which are known to work as of DCS World 2.9.4.53990."
        ),
    )
    limit_ai_radios: bool = boolean_option(
        "Limit AI radio callouts",
        page=MISSION_GENERATOR_PAGE,
        section=GAMEPLAY_SECTION,
        default=True,
        detail="Avoids the target-detection callouts over the radio by AI. (except for AWACS flights)",
    )
    silence_ai_radios: bool = boolean_option(
        "Suppress AI radio callouts",
        page=MISSION_GENERATOR_PAGE,
        section=GAMEPLAY_SECTION,
        default=False,
        detail="Keeps the AI silent at all times for flights with human pilots. (except for AWACS flights)",
    )
    # Mission specific
    desired_player_mission_duration: timedelta = minutes_option(
        "Desired mission duration",
        page=MISSION_GENERATOR_PAGE,
        section=GAMEPLAY_SECTION,
        default=timedelta(minutes=60),
        min=30,
        max=150,
    )
    desired_tanker_on_station_time: timedelta = minutes_option(
        "Desired tanker on-station time",
        page=MISSION_GENERATOR_PAGE,
        section=GAMEPLAY_SECTION,
        default=timedelta(minutes=60),
        min=30,
        max=150,
    )
    # Mission specific
    max_frontline_width: int = bounded_int_option(
        "Maximum frontline width (km)",
        page=MISSION_GENERATOR_PAGE,
        section=GAMEPLAY_SECTION,
        default=80,
        min=1,
        max=100,
    )
    game_masters_count: int = bounded_int_option(
        "Number of game masters",
        page=MISSION_GENERATOR_PAGE,
        section=GAMEPLAY_SECTION,
        default=1,
        min=0,
        max=10,
        detail=(
            "The number of game master slots to generate for each side. "
            "Game masters can see, control & direct all units in the mission."
        ),
    )
    tactical_commander_count: int = bounded_int_option(
        "Number of tactical commands",
        page=MISSION_GENERATOR_PAGE,
        section=GAMEPLAY_SECTION,
        default=3,
        min=0,
        max=10,
        detail=(
            "The number of tactical commander slots to generate for each side. "
            "Tactical commanders can control & direct friendly units."
        ),
    )
    jtac_count: int = bounded_int_option(
        "Number of JTAC controllers",
        page=MISSION_GENERATOR_PAGE,
        section=GAMEPLAY_SECTION,
        default=3,
        min=0,
        max=10,
        detail=(
            "The number of JTAC controller slots to generate for each side. "
            "JTAC operators can only control friendly units."
        ),
    )
    observer_count: int = bounded_int_option(
        "Number of observers",
        page=MISSION_GENERATOR_PAGE,
        section=GAMEPLAY_SECTION,
        default=0,
        min=0,
        max=10,
        detail=(
            "The number of observers slots to generate for each side. "
            'Use this to allow spectators when disabling "Allow external views".'
        ),
    )
    ground_start_ai_planes: bool = boolean_option(
        "AI fixed-wing aircraft can use roadbases / bases with only ground spawns",
        MISSION_GENERATOR_PAGE,
        GAMEPLAY_SECTION,
        default=False,
        detail=(
            "If enabled, AI can use roadbases or airbases which only have ground spawns. "
            "AI will always air-start from these bases (due to DCS limitation)."
        ),
    )
    ground_start_scenery_remove_triggers: bool = boolean_option(
        "Generate SCENERY REMOVE OBJECTS ZONE triggers at roadbase first waypoints",
        MISSION_GENERATOR_PAGE,
        GAMEPLAY_SECTION,
        default=True,
        detail=(
            "Can be used to remove lightposts and other obstacles from roadbase runways. "
            "Might not work in DCS multiplayer."
        ),
    )
    ground_start_trucks: bool = boolean_option(
        "Spawn trucks at ground spawns in airbases instead of FARP statics",
        MISSION_GENERATOR_PAGE,
        GAMEPLAY_SECTION,
        default=False,
        detail=("Might have a negative performance impact."),
    )
    ground_start_trucks_roadbase: bool = boolean_option(
        "Spawn trucks at ground spawns in roadbases instead of FARP statics",
        MISSION_GENERATOR_PAGE,
        GAMEPLAY_SECTION,
        default=False,
        detail=("Might have a negative performance impact."),
    )
    ground_start_ground_power_trucks: bool = boolean_option(
        "Spawn ground power trucks at ground starts in airbases",
        MISSION_GENERATOR_PAGE,
        GAMEPLAY_SECTION,
        default=True,
        detail=(
            "Needed to cold-start some aircraft types. Might have a performance impact."
        ),
    )
    ground_start_ground_power_trucks_roadbase: bool = boolean_option(
        "Spawn ground power trucks at ground starts in roadbases",
        MISSION_GENERATOR_PAGE,
        GAMEPLAY_SECTION,
        default=True,
        detail=(
            "Needed to cold-start some aircraft types. Might have a performance impact."
        ),
    )
    ground_start_airbase_statics_farps_remove: bool = boolean_option(
        "Remove ground spawn statics, including invisible FARPs, at airbases",
        MISSION_GENERATOR_PAGE,
        GAMEPLAY_SECTION,
        default=True,
        detail=(
            "Ammo and fuel statics and invisible FARPs should be unnecessary when creating "
            "additional spawns for players at airbases. This setting will disable them and "
            "potentially grant a marginal performance benefit."
        ),
    )
    ai_unlimited_fuel: bool = boolean_option(
        "AI flights have unlimited fuel",
        MISSION_GENERATOR_PAGE,
        GAMEPLAY_SECTION,
        default=True,
        detail=(
            "AI aircraft have unlimited fuel applied at start, removed at join/racetrack start,"
            " and reapplied at split/racetrack end for applicable flights. "
        ),
    )
    dynamic_slots: bool = boolean_option(
        "Dynamic slots",
        MISSION_GENERATOR_PAGE,
        GAMEPLAY_SECTION,
        default=False,
        detail=(
            "Enables dynamic slots. Please note that losses from dynamic slots won't be registered."
        ),
    )
    dynamic_slots_hot: bool = boolean_option(
        "Allow dynamic slot hot start",
        MISSION_GENERATOR_PAGE,
        GAMEPLAY_SECTION,
        default=True,
        detail=("Enables hot start for dynamic slots."),
    )
    dynamic_cargo: bool = boolean_option(
        "Dynamic cargo",
        MISSION_GENERATOR_PAGE,
        GAMEPLAY_SECTION,
        default=True,
        detail=("Enables dynamic cargo for airfields, ships, FARPs & warehouses."),
    )
    player_flights_sixpack: bool = boolean_option(
        "Player flights can spawn on the sixpack",
        MISSION_GENERATOR_PAGE,
        GAMEPLAY_SECTION,
        default=True,
    )

    # Performance
    perf_smoke_gen: bool = boolean_option(
        "Smoke visual effect on the front line",
        page=MISSION_GENERATOR_PAGE,
        section=PERFORMANCE_SECTION,
        default=True,
    )
    perf_smoke_spacing: int = bounded_int_option(
        "Smoke generator spacing (higher means less smoke)",
        page=MISSION_GENERATOR_PAGE,
        section=PERFORMANCE_SECTION,
        default=1600,
        min=800,
        max=24000,
    )
    perf_red_alert_state: bool = boolean_option(
        "SAM starts in red alert mode",
        page=MISSION_GENERATOR_PAGE,
        section=PERFORMANCE_SECTION,
        default=True,
    )
    perf_artillery: bool = boolean_option(
        "Artillery strikes",
        page=MISSION_GENERATOR_PAGE,
        section=PERFORMANCE_SECTION,
        default=True,
    )
    generate_fire_tasks_for_missile_sites: bool = boolean_option(
        "Generate fire tasks for missile sites",
        page=MISSION_GENERATOR_PAGE,
        section=PERFORMANCE_SECTION,
        detail=(
            "If enabled, missile sites like V2s and Scuds will fire on random targets "
            "at the start of the mission."
        ),
        default=True,
    )
    perf_moving_units: bool = boolean_option(
        "Moving ground units",
        page=MISSION_GENERATOR_PAGE,
        section=PERFORMANCE_SECTION,
        default=True,
    )
    convoys_travel_full_distance: bool = boolean_option(
        "Convoys drive the full distance between control points",
        page=MISSION_GENERATOR_PAGE,
        section=PERFORMANCE_SECTION,
        default=True,
    )
    perf_disable_convoys: bool = boolean_option(
        "Disable convoys",
        page=MISSION_GENERATOR_PAGE,
        section=PERFORMANCE_SECTION,
        default=False,
    )
    perf_disable_cargo_ships: bool = boolean_option(
        "Disable shipping-convoys",
        page=MISSION_GENERATOR_PAGE,
        section=PERFORMANCE_SECTION,
        default=False,
    )
    perf_frontline_units_prefer_roads: bool = boolean_option(
        "Front line troops prefer roads",
        page=MISSION_GENERATOR_PAGE,
        section=PERFORMANCE_SECTION,
        default=False,
    )
    perf_frontline_units_max_supply: int = bounded_int_option(
        "Maximum frontline unit supply per control point",
        page=MISSION_GENERATOR_PAGE,
        section=PERFORMANCE_SECTION,
        default=60,
        min=10,
        max=300,
        causes_expensive_game_update=True,
    )
    perf_infantry: bool = boolean_option(
        "Generate infantry squads alongside vehicles",
        page=MISSION_GENERATOR_PAGE,
        section=PERFORMANCE_SECTION,
        default=True,
    )
    perf_destroyed_units: bool = boolean_option(
        "Generate carcasses for units destroyed in previous turns",
        page=MISSION_GENERATOR_PAGE,
        section=PERFORMANCE_SECTION,
        default=True,
    )
    perf_disable_untasked_blufor_aircraft: bool = boolean_option(
        "Disable untasked OWNFOR aircraft at airfields",
        page=MISSION_GENERATOR_PAGE,
        section=PERFORMANCE_SECTION,
        default=False,
    )
    perf_disable_untasked_opfor_aircraft: bool = boolean_option(
        "Disable untasked OPFOR aircraft at airfields",
        page=MISSION_GENERATOR_PAGE,
        section=PERFORMANCE_SECTION,
        default=False,
    )
    # Performance culling
    perf_culling: bool = boolean_option(
        "Culling of distant units enabled",
        page=MISSION_GENERATOR_PAGE,
        section=PERFORMANCE_SECTION,
        default=False,
    )
    perf_culling_distance: int = bounded_int_option(
        "Culling distance (km)",
        page=MISSION_GENERATOR_PAGE,
        section=PERFORMANCE_SECTION,
        default=100,
        min=10,
        max=10000,
        causes_expensive_game_update=True,
    )
    perf_do_not_cull_threatening_iads: bool = boolean_option(
        "Do not cull threatening IADS",
        page=MISSION_GENERATOR_PAGE,
        section=PERFORMANCE_SECTION,
        default=True,
    )
    perf_do_not_cull_carrier: bool = boolean_option(
        "Do not cull carrier's surroundings",
        page=MISSION_GENERATOR_PAGE,
        section=PERFORMANCE_SECTION,
        default=True,
        causes_expensive_game_update=True,
    )
    perf_ai_despawn_airstarted: bool = boolean_option(
        "De-spawn AI in the air upon RTB",
        page=MISSION_GENERATOR_PAGE,
        section=PERFORMANCE_SECTION,
        default=False,
        detail=(
            "If enabled, AI flights will de-spawn over their base "
            "if the start-up type was manually changed to 'In-Flight'."
        ),
    )
    pretense_maxdistfromfront_distance: int = bounded_int_option(
        "Max distance from front (km)",
        page=PRETENSE_PAGE,
        section=GENERAL_SECTION,
        default=130,
        min=10,
        max=10000,
        detail=(
            "Zones farther away than this from the front line are switched "
            "into low activity state, but will still be there as functional "
            "parts of the economy. Use this to adjust performance."
        ),
    )
    pretense_controllable_carrier: bool = boolean_option(
        "Controllable carrier",
        page=PRETENSE_PAGE,
        section=GENERAL_SECTION,
        default=True,
        detail=(
            "This can be used to enable or disable the native carrier support in Pretense. The Pretense carrier "
            "can be controlled through the communication menu (if the Pretense character has enough rank/CMD points) "
            "and the player can call in AI aerial and cruise missile missions using it."
            "The controllable carriers in Pretense do not build and deploy AI missions autonomously, so if you prefer "
            "to have both sides deploy carrier aviation autonomously, you might want to disable this option. "
            "When this option is disabled, moving the carrier can only be done with the Retribution interface."
        ),
    )
    pretense_carrier_steams_into_wind: bool = boolean_option(
        "Carriers steam into wind",
        page=PRETENSE_PAGE,
        section=GENERAL_SECTION,
        default=True,
        detail=(
            "This setting controls whether carriers and their escorts will steam into wind. Disable to "
            "to ensure that the carriers stay within the carrier zone in Pretense, but note that "
            "doing so might limit carrier operations, takeoff weights and landings."
        ),
    )
    pretense_carrier_zones_navmesh: str = choices_option(
        "Navmesh to use for Pretense carrier zones",
        page=PRETENSE_PAGE,
        section=GENERAL_SECTION,
        choices=["Blue navmesh", "Red navmesh"],
        default="Blue navmesh",
        detail=(
            "Use the Retribution map interface options to compare the blue navmesh and the red navmesh."
            "You can select which navmesh to use when generating the zones in which the controllable carrier(s) "
            "move and operate."
        ),
    )
    pretense_extra_zone_connections: int = bounded_int_option(
        "Extra friendly zone connections",
        page=PRETENSE_PAGE,
        section=GENERAL_SECTION,
        default=2,
        min=0,
        max=10,
        detail=(
            "Add connections from each zone to this many closest friendly zones,"
            "which don't have an existing supply route defined in the campaign."
        ),
    )
    pretense_num_of_cargo_planes: int = bounded_int_option(
        "Number of cargo planes per side",
        page=PRETENSE_PAGE,
        section=GENERAL_SECTION,
        default=2,
        min=1,
        max=100,
    )
    pretense_sead_flights_per_cp: int = bounded_int_option(
        "Number of AI SEAD flights per control point / zone",
        page=PRETENSE_PAGE,
        section=GENERAL_SECTION,
        default=1,
        min=1,
        max=10,
    )
    pretense_cas_flights_per_cp: int = bounded_int_option(
        "Number of AI CAS flights per control point / zone",
        page=PRETENSE_PAGE,
        section=GENERAL_SECTION,
        default=1,
        min=1,
        max=10,
    )
    pretense_bai_flights_per_cp: int = bounded_int_option(
        "Number of AI BAI flights per control point / zone",
        page=PRETENSE_PAGE,
        section=GENERAL_SECTION,
        default=1,
        min=1,
        max=10,
    )
    pretense_strike_flights_per_cp: int = bounded_int_option(
        "Number of AI Strike flights per control point / zone",
        page=PRETENSE_PAGE,
        section=GENERAL_SECTION,
        default=1,
        min=1,
        max=10,
    )
    pretense_barcap_flights_per_cp: int = bounded_int_option(
        "Number of AI BARCAP flights per control point / zone",
        page=PRETENSE_PAGE,
        section=GENERAL_SECTION,
        default=1,
        min=1,
        max=10,
    )
    pretense_ai_aircraft_per_flight: int = bounded_int_option(
        "Number of AI aircraft per flight",
        page=PRETENSE_PAGE,
        section=GENERAL_SECTION,
        default=2,
        min=1,
        max=4,
    )
    pretense_player_flights_per_type: int = bounded_int_option(
        "Number of player flights per aircraft type at each base",
        page=PRETENSE_PAGE,
        section=GENERAL_SECTION,
        default=1,
        min=1,
        max=10,
    )
    pretense_ai_cargo_planes_per_side: int = bounded_int_option(
        "Number of AI cargo planes per side",
        page=PRETENSE_PAGE,
        section=GENERAL_SECTION,
        default=2,
        min=1,
        max=20,
    )

    # Cheating. Not using auto settings because the same page also has buttons which do
    # not alter settings.
    enable_frontline_cheats: bool = False
    enable_base_capture_cheat: bool = False
    enable_transfer_cheat: bool = False
    enable_runway_state_cheat: bool = False
    enable_air_wing_adjustments: bool = False
    enable_enemy_buy_sell: bool = False

    # LUA Plugins system
    plugins: Dict[str, bool] = field(default_factory=dict)

    only_player_takeoff: bool = True  # Legacy parameter do not use

    @staticmethod
    def plugin_settings_key(identifier: str) -> str:
        return f"{identifier}"

    def initialize_plugin_option(self, identifier: str, default_value: Any) -> None:
        try:
            self.plugin_option(identifier)
        except KeyError:
            self.set_plugin_option(identifier, default_value)

    def plugin_option(self, identifier: str) -> Any:
        return self.plugins[self.plugin_settings_key(identifier)]

    def set_plugin_option(self, identifier: str, value: Any) -> None:
        self.plugins[self.plugin_settings_key(identifier)] = value

    def __setstate__(self, state: dict[str, Any]) -> None:
        # restore Enum & timedelta types
        for key, value in state.items():
            if isinstance(self.__dict__.get(key), timedelta) and isinstance(value, int):
                state[key] = timedelta(minutes=value)
            elif isinstance(self.__dict__.get(key), Enum) and isinstance(value, str):
                state[key] = eval(value)
            elif isinstance(value, dict):
                state[key] = self.obj_hook(value)

        # __setstate__ is called with the dict of the object being unpickled. We
        # can provide save compatibility for new settings options (which
        # normally would not be present in the unpickled object) by creating a
        # new settings object, updating it with the unpickled state, and
        # updating our dict with that.
        new_state = Settings().__dict__
        new_state.update(state)
        self.__dict__.update(new_state)
        from game.plugins import LuaPluginManager

        LuaPluginManager().load_settings(self)

    @classmethod
    def _field_description(cls, settings_field: Field[Any]) -> OptionDescription:
        return settings_field.metadata[SETTING_DESCRIPTION_KEY]

    @classmethod
    def pages(cls) -> Iterator[str]:
        seen: set[str] = set()
        for settings_field in cls._user_fields():
            description = cls._field_description(settings_field)
            if description.page not in seen:
                yield description.page
                seen.add(description.page)

    @classmethod
    def sections(cls, page: str) -> Iterator[str]:
        seen: set[str] = set()
        for settings_field in cls._user_fields():
            description = cls._field_description(settings_field)
            if description.page == page and description.section not in seen:
                yield description.section
                seen.add(description.section)

    @classmethod
    def fields(cls, page: str, section: str) -> Iterator[tuple[str, OptionDescription]]:
        for settings_field in cls._user_fields():
            description = cls._field_description(settings_field)
            if description.page == page and description.section == section:
                yield settings_field.name, description

    @classmethod
    def _user_fields(cls) -> Iterator[Field[Any]]:
        for settings_field in fields(cls):
            if SETTING_DESCRIPTION_KEY in settings_field.metadata:
                yield settings_field

    @staticmethod
    def default_json(obj: Any) -> Any:
        # Known types that don't like being serialized,
        # so we introduce our own implementation...
        if isinstance(obj, Enum):
            return {"Enum": str(obj)}
        elif isinstance(obj, timedelta):
            return {"timedelta": round(obj.seconds / 60)}
        return obj

    @staticmethod
    def obj_hook(obj: Any) -> Any:
        if (value := obj.get("Enum")) is not None:
            return eval(value)
        elif (value := obj.get("timedelta")) is not None:
            return timedelta(minutes=value)
        else:
            return obj
