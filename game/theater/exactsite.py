"""Air-defense sites drawn unit by unit in the campaign miz (the FIXED prefix).

A FIXED group generates as drawn: every unit at its own position and heading.
Its task comes from the preset group its units match best, and the owning
faction's matching ForceGroup adds its usual optional extras (trucks, point
defense) from its stock layout. A faction that cannot field the drawn shooters
still gets the drawn site: support units it cannot field are left out, and
when it cannot field the drawn launchers or tracking radar its own system goes
into the drawn radar and launcher spots. Only a faction with no system for the
task gets a stock site at the same spot.
"""

from __future__ import annotations

import logging
import random
from typing import Optional, TYPE_CHECKING, Type

from dcs.unittype import UnitType as DcsUnitType, VehicleType
from dcs.vehicles import vehicle_map

from game.armedforces.armedforces import ArmedForces
from game.armedforces.forcegroup import ForceGroup
from game.data.groups import GroupTask
from game.data.units import UnitClass
from game.dcs.groundunittype import GroundUnitType
from game.naming import namegen
from game.point_with_heading import PointWithHeading
from game.theater.iadsnetwork.iadsrole import IadsRole
from game.theater.presetlocation import ExactSitePreset
from game.theater.theatergroundobject import (
    EwrGroundObject,
    IadsGroundObject,
    SamGroundObject,
)
from game.theater.theatergroup import IadsGroundGroup, TheaterGroup, TheaterUnit
from game.utils import Heading, escape_string_for_lua

if TYPE_CHECKING:
    from game import Game
    from game.theater.start_generator import AirbaseGroundObjectGenerator

#: Longest reach first, so a tie between presets goes to the longer-range task.
AIR_DEFENSE_TASKS = [
    GroupTask.LORAD,
    GroupTask.MERAD,
    GroupTask.SHORAD,
    GroupTask.AAA,
    GroupTask.EARLY_WARNING_RADAR,
]

#: Drawn guns and short-range SAMs that defend a longer-range site as its own group.
POINT_DEFENSE_CLASSES = {UnitClass.SHORAD, UnitClass.AAA, UnitClass.MANPAD}

#: The only kinds of unit a stock layout's optional slots may add to a drawn site.
#: A layout's optional radar or launcher slot would change the site, not dress it.
EXTRA_CLASSES = {
    UnitClass.LOGISTICS,
    UnitClass.POWER,
    UnitClass.SHORAD,
    UnitClass.AAA,
    UnitClass.MANPAD,
}

LAUNCHER_CLASSES = {UnitClass.LAUNCHER, UnitClass.TELAR}
GUN_CLASSES = {UnitClass.SHORAD, UnitClass.AAA, UnitClass.MANPAD}
RADAR_CLASSES = {
    UnitClass.SEARCH_RADAR,
    UnitClass.TRACK_RADAR,
    UnitClass.SEARCH_TRACK_RADAR,
    UnitClass.EARLY_WARNING_RADAR,
    UnitClass.SPECIALIZED_RADAR,
}
#: Metres between units a fitted system adds where no drawn spot is left for them.
FIT_SPACING_M = 40


def unit_class_of(dcs_type: Type[DcsUnitType]) -> UnitClass:
    if not issubclass(dcs_type, VehicleType):
        return UnitClass.UNKNOWN
    unit_type = next(GroundUnitType.for_dcs_type(dcs_type), None)
    return unit_type.unit_class if unit_type is not None else UnitClass.UNKNOWN


def _core_ids(types: list[Type[VehicleType]]) -> set[str]:
    """The drawn units that say what the site is: everything but its trucks."""
    return {t.id for t in types if unit_class_of(t) is not UnitClass.LOGISTICS}


def _match_score(force_group: ForceGroup, core_ids: set[str]) -> int:
    return len(core_ids & {u.dcs_unit_type.id for u in force_group.units})


def _best_match(
    groups: list[ForceGroup], core_ids: set[str]
) -> tuple[Optional[GroupTask], Optional[ForceGroup]]:
    best_task: Optional[GroupTask] = None
    best_group: Optional[ForceGroup] = None
    best_score = 0
    for task in AIR_DEFENSE_TASKS:
        for force_group in groups:
            if task not in force_group.tasks:
                continue
            score = _match_score(force_group, core_ids)
            if score > best_score:
                best_task, best_group, best_score = task, force_group, score
    return best_task, best_group


def classify(types: list[Type[VehicleType]]) -> Optional[GroupTask]:
    """The air-defense task of the preset group the drawn units match best."""
    task, _ = _best_match(ForceGroup.preset_groups(), _core_ids(types))
    if task is not None:
        return task
    # Factions field EWRs and many SHORAD and AAA systems from single units, not
    # preset groups, so no preset names them.
    classes = {unit_class_of(t) for t in types}
    for unit_class, fallback in (
        (UnitClass.SHORAD, GroupTask.SHORAD),
        (UnitClass.AAA, GroupTask.AAA),
        (UnitClass.EARLY_WARNING_RADAR, GroupTask.EARLY_WARNING_RADAR),
    ):
        if unit_class in classes:
            return fallback
    return None


def faction_group_for(
    armed_forces: ArmedForces, task: GroupTask, types: list[Type[VehicleType]]
) -> Optional[ForceGroup]:
    """The faction's ForceGroup for this task closest to the drawn site."""
    candidates = list(armed_forces.groups_for_task(task))
    if not candidates:
        return None
    _, best = _best_match(candidates, _core_ids(types))
    return best if best is not None else random.choice(candidates)


def _shoots(unit_class: UnitClass, task: GroupTask) -> bool:
    if unit_class in LAUNCHER_CLASSES:
        return True
    return task in (GroupTask.SHORAD, GroupTask.AAA) and unit_class in GUN_CLASSES


def _is_core(unit_class: UnitClass, task: GroupTask) -> bool:
    """A unit the site cannot work without; anything else is support it can lose."""
    if _shoots(unit_class, task):
        return True
    if task is GroupTask.EARLY_WARNING_RADAR:
        return unit_class in RADAR_CLASSES
    return unit_class in (UnitClass.TRACK_RADAR, UnitClass.SEARCH_TRACK_RADAR)


def _is_spot(unit_class: UnitClass, task: GroupTask) -> bool:
    """A drawn unit whose place a fitted system takes."""
    return (
        _is_core(unit_class, task)
        or unit_class in RADAR_CLASSES
        or unit_class is UnitClass.COMMAND_POST
    )


def _spot_rank(spot_class: UnitClass, unit_class: UnitClass) -> int:
    if spot_class is unit_class:
        return 0
    tracking = {UnitClass.TRACK_RADAR, UnitClass.SEARCH_TRACK_RADAR}
    if spot_class in tracking and unit_class in tracking:
        return 1
    if spot_class in RADAR_CLASSES and unit_class in RADAR_CLASSES:
        return 2
    return 3


def _required_types(
    force_group: ForceGroup, task: GroupTask
) -> list[Type[VehicleType]]:
    """One unit type per required slot of the faction's stock layout for the task."""
    if not force_group.layouts:
        return []
    required: list[Type[VehicleType]] = []
    for tgo_group in random.choice(force_group.layouts).groups:
        for unit_group in tgo_group.unit_groups:
            if unit_group.optional or unit_group.sub_task is not None:
                continue
            types = [
                t
                for t in force_group.dcs_unit_types_for_group(unit_group)
                if issubclass(t, VehicleType)
            ]
            if not types:
                continue
            unit_class = unit_class_of(types[0])
            if unit_class in (UnitClass.LOGISTICS, UnitClass.POWER):
                continue
            if task in (GroupTask.LORAD, GroupTask.MERAD) and (
                unit_class in GUN_CLASSES
            ):
                continue
            if types[0] not in required:
                required.append(types[0])
    return required


def fit_faction_system(
    drawn: list[tuple[PointWithHeading, Type[VehicleType]]],
    task: GroupTask,
    force_group: ForceGroup,
    fieldable: set[Type[VehicleType]],
) -> Optional[list[tuple[PointWithHeading, Type[VehicleType]]]]:
    """The faction's own system in the drawn radar and launcher spots.

    Every drawn launcher spot gets one of the faction's launchers; each of its
    radars and command posts takes the closest-matching drawn radar spot, or a
    place beside the site when none is left. Spots left over stay empty. Other
    drawn units stay when the faction fields them. None when the faction's
    system has no launcher for the spots.
    """
    required = _required_types(force_group, task)
    shooters = [t for t in required if _shoots(unit_class_of(t), task)]
    others = [t for t in required if t not in shooters]
    if not shooters and task is not GroupTask.EARLY_WARNING_RADAR:
        return None
    if not shooters and not others:
        return None

    kept: list[tuple[PointWithHeading, Type[VehicleType]]] = []
    shooter_spots: list[PointWithHeading] = []
    other_spots: list[tuple[PointWithHeading, UnitClass]] = []
    for position, dcs_type in drawn:
        unit_class = unit_class_of(dcs_type)
        if not _is_spot(unit_class, task):
            if unit_class is UnitClass.LOGISTICS or dcs_type in fieldable:
                kept.append((position, dcs_type))
        elif _shoots(unit_class, task):
            shooter_spots.append(position)
        else:
            other_spots.append((position, unit_class))

    anchor = (shooter_spots or [p for p, _ in other_spots] or [drawn[0][0]])[0]
    added = 0

    def beside_site() -> PointWithHeading:
        nonlocal added
        added += 1
        return PointWithHeading.from_point(
            anchor.point_from_heading(90, FIT_SPACING_M * added),
            Heading.from_degrees(0),
        )

    fitted: list[tuple[PointWithHeading, Type[VehicleType]]] = []
    for unit_type in others:
        if other_spots:
            unit_class = unit_class_of(unit_type)
            best = min(other_spots, key=lambda s: _spot_rank(s[1], unit_class))
            other_spots.remove(best)
            fitted.append((best[0], unit_type))
        else:
            fitted.append((beside_site(), unit_type))
    if shooters:
        for index, position in enumerate(shooter_spots or [beside_site()]):
            fitted.append((position, shooters[index % len(shooters)]))
    return fitted + kept


def _add_layout_extras(
    force_group: ForceGroup, go: IadsGroundObject, name: str, game: Game
) -> None:
    if not force_group.layouts:
        return
    layout = random.choice(force_group.layouts)
    for tgo_group in layout.groups:
        for unit_group in tgo_group.unit_groups:
            if not unit_group.optional:
                continue
            try:
                unit_type = force_group.random_dcs_unit_type_for_group(unit_group)
            except IndexError:
                continue
            if unit_class_of(unit_type) not in EXTRA_CLASSES:
                continue
            force_group.create_theater_group_for_tgo(
                go, unit_group, f"{name} ({tgo_group.group_name})", game, unit_type
            )


def _generate_stock_site(
    generator: AirbaseGroundObjectGenerator,
    preset: ExactSitePreset,
    task: GroupTask,
) -> None:
    if task is GroupTask.EARLY_WARNING_RADAR:
        force_group = generator.get_unit_group_for_task(preset, task)
        if force_group is None:
            logging.error(
                f"{generator.faction_name} has no ForceGroup for EWR; "
                f"{preset.original_name!r} does not generate"
            )
            return
        generator.generate_ground_object_from_group(force_group, preset, task)
        return
    # The same step-down a marker of this class gets (long range, then shorter).
    first = AIR_DEFENSE_TASKS.index(task)
    generator.generate_aa_at(
        preset, AIR_DEFENSE_TASKS[first : AIR_DEFENSE_TASKS.index(GroupTask.AAA) + 1]
    )


def generate_exact_site(
    generator: AirbaseGroundObjectGenerator, preset: ExactSitePreset
) -> None:
    control_point = generator.control_point
    if control_point.captured.is_neutral:
        return
    drawn: list[tuple[PointWithHeading, Type[VehicleType]]] = []
    for unit in preset.units:
        dcs_type = vehicle_map.get(unit.type_id)
        if dcs_type is None:
            logging.error(
                f"FIXED site {preset.original_name!r}: unknown unit type "
                f"{unit.type_id!r} left out"
            )
            continue
        drawn.append(
            (
                PointWithHeading.from_point(
                    unit.position, Heading.from_degrees(unit.heading)
                ),
                dcs_type,
            )
        )
    types = [dcs_type for _, dcs_type in drawn]
    task = classify(types)
    if task is None:
        logging.error(
            f"FIXED site {preset.original_name!r}: no air-defense preset group "
            "matches its units, so it does not generate"
        )
        return

    accessible = {u.dcs_unit_type for u in generator.faction.accessible_units}
    fieldable = {t for t in types if t in accessible}
    # Trucks are scenery to the faction check; the shooters and radars are not.
    missing = [
        t
        for t in types
        if unit_class_of(t) is not UnitClass.LOGISTICS and t not in fieldable
    ]
    force_group = faction_group_for(generator.armed_forces, task, types)
    if any(_is_core(unit_class_of(t), task) for t in missing):
        fitted = (
            fit_faction_system(drawn, task, force_group, fieldable)
            if force_group is not None
            else None
        )
        if fitted is None:
            logging.warning(
                f"FIXED site {preset.original_name!r}: {generator.faction_name} "
                f"has no {task.description} system to fit into it; a stock site "
                "generates there"
            )
            _generate_stock_site(generator, preset, task)
            return
        assert force_group is not None
        logging.info(
            f"FIXED site {preset.original_name!r}: {generator.faction_name} cannot "
            f"field {sorted({t.id for t in missing})}; its {force_group.name} "
            "takes the drawn spots"
        )
        drawn = fitted
    elif missing:
        logging.info(
            f"FIXED site {preset.original_name!r}: {generator.faction_name} cannot "
            f"field {sorted({t.id for t in missing})}; those units are left out"
        )
        drawn = [(p, t) for p, t in drawn if t not in missing]

    game = generator.game
    name = namegen.random_objective_name()
    go: IadsGroundObject
    if task is GroupTask.EARLY_WARNING_RADAR:
        go = EwrGroundObject(name, preset, control_point)
    else:
        go = SamGroundObject(name, preset, control_point, task)
    split_point_defense = task in (GroupTask.LORAD, GroupTask.MERAD)
    main: list[TheaterUnit] = []
    point_defense: list[TheaterUnit] = []
    for position, dcs_type in drawn:
        theater_unit = TheaterUnit(
            game.next_unit_id(), "", dcs_type, position, go, True, True
        )
        theater_unit.name = escape_string_for_lua(
            theater_unit.unit_type.variant_id
            if theater_unit.unit_type
            else dcs_type.name
        )
        if split_point_defense and unit_class_of(dcs_type) in POINT_DEFENSE_CLASSES:
            point_defense.append(theater_unit)
        else:
            main.append(theater_unit)

    # Group labels match the stock layouts', so template extras join these groups.
    main_label = {GroupTask.EARLY_WARNING_RADAR: "EWR", GroupTask.AAA: "AAA"}.get(
        task, "SAM"
    )
    for label, units, role in (
        (main_label, main, IadsRole.for_task(task)),
        ("PD", point_defense, IadsRole.POINT_DEFENSE),
    ):
        if not units:
            continue
        group = IadsGroundGroup.from_group(
            TheaterGroup.from_template(
                game.next_group_id(), f"{name} ({label})", units, go
            )
        )
        group.iads_role = role
        go.groups.append(group)

    if force_group is not None:
        _add_layout_extras(force_group, go, name, game)
    control_point.connected_objectives.append(go)
