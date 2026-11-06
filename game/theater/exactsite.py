"""Air-defense sites drawn unit by unit in the campaign miz (the FIXED prefix).

A FIXED group generates as drawn: every unit at its own position and heading.
Its task comes from the preset group its units match best, and the owning
faction's matching ForceGroup adds its usual optional extras (trucks, point
defense) from its stock layout. A faction that cannot field the drawn shooters
gets a stock site at the same spot instead.
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
    if task is None and any(
        unit_class_of(t) is UnitClass.EARLY_WARNING_RADAR for t in types
    ):
        # Factions field EWRs from single units, not preset groups.
        return GroupTask.EARLY_WARNING_RADAR
    return task


def faction_group_for(
    armed_forces: ArmedForces, task: GroupTask, types: list[Type[VehicleType]]
) -> Optional[ForceGroup]:
    """The faction's ForceGroup for this task closest to the drawn site."""
    candidates = list(armed_forces.groups_for_task(task))
    if not candidates:
        return None
    _, best = _best_match(candidates, _core_ids(types))
    return best if best is not None else random.choice(candidates)


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
    # Trucks are scenery to the faction check; the shooters and radars are not.
    missing = sorted(
        t.id
        for t in types
        if unit_class_of(t) is not UnitClass.LOGISTICS and t not in accessible
    )
    if missing:
        logging.warning(
            f"FIXED site {preset.original_name!r}: {generator.faction_name} cannot "
            f"field {missing}; a stock {task.description} site generates there"
        )
        _generate_stock_site(generator, preset, task)
        return

    game = generator.game
    name = namegen.random_objective_name()
    go: IadsGroundObject
    if task is GroupTask.EARLY_WARNING_RADAR:
        go = EwrGroundObject(name, preset, control_point)
    else:
        go = SamGroundObject(name, preset, control_point, task)
    force_group = faction_group_for(generator.armed_forces, task, types)

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
