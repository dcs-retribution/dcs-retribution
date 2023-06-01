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
            "preferred even if there is a closer squadron capable of the mission as a"
            "secondary task. Expect longer flights, but squadrons will be more often "
            "assigned to their primary task."
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
            "pilots will replenish at a fixed rate, each defined with the settings"
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
        default=12,
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
            "If set, squadrons will not be able to exceed a maximum number of aircraft "
            "(configurable), and the campaign will begin with all squadrons at full strength "
            "given enough room at the base."
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
        "AI ground unit procurement budget ratio (%)",
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
        "AI ground unit front-line reserves factor (%)",
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
        "AI ground unit reserves procurement target",
        CAMPAIGN_MANAGEMENT_PAGE,
        HQ_AUTOMATION_SECTION,
        min=0,
        max=1000,
        default=10,
        detail=(
            "The number of units that will be bought as reserves for applicable control points"
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
        detail="See 2-ship weight factor (WF2)",
    )
    fpa_4ship_weight: int = bounded_int_option(
        "4-ship weight factor (WF4)",
        CAMPAIGN_MANAGEMENT_PAGE,
        FLIGHT_PLANNER_AUTOMATION,
        default=15,
        min=0,
        max=100,
        detail="See 2-ship weight factor (WF2)",
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
        default=None,
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
    atflir_autoswap: bool = boolean_option(
        "Auto-swap ATFLIR to LITENING",
        MISSION_GENERATOR_PAGE,
        GAMEPLAY_SECTION,
        default=True,
        detail=(
            "Automatically swaps ATFLIR to LITENING pod for newly generated land-based F-18 flights "
            "without having to change the payload. <u>Takes effect after current turn!</u>"
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
    max_frontline_length: int = bounded_int_option(
        "Maximum frontline length (km)",
        page=MISSION_GENERATOR_PAGE,
        section=GAMEPLAY_SECTION,
        default=80,
        min=1,
        max=100,
    )
    opfor_autoplanner_aggressiveness: int = bounded_int_option(
        "OPFOR autoplanner aggressiveness (%)",
        page=MISSION_GENERATOR_PAGE,
        section=GAMEPLAY_SECTION,
        default=20,
        min=0,
        max=100,
        detail=(
            "Chance (larger number -> higher chance) that the OPFOR AI "
            "autoplanner will take risks and plan flights against targets "
            "within threatened airspace."
        ),
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
    perf_disable_idle_aircraft: bool = boolean_option(
        "Disable idle aircraft at airfields",
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

    # Cheating. Not using auto settings because the same page also has buttons which do
    # not alter settings.
    show_red_ato: bool = False
    enable_frontline_cheats: bool = False
    enable_base_capture_cheat: bool = False
    enable_transfer_cheat: bool = False

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
