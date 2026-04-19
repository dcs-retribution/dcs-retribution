from __future__ import annotations

import itertools
import hashlib
import logging
import pickle
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from pathlib import Path
from typing import Iterator

import dcs
import yaml
from dcs import Point
from dcs.unitgroup import StaticGroup

from game import persistency
from game.data.groups import GroupRole
from game.layout.layout import (
    TgoLayout,
    TgoLayoutGroup,
    TgoLayoutUnitGroup,
    LayoutUnit,
    AntiAirLayout,
    BuildingLayout,
    NavalLayout,
    GroundForceLayout,
    DefensesLayout,
)
from game.layout.layoutmapping import LayoutMapping
from game.profiling import logged_duration
from game.version import VERSION

LAYOUT_DIR = "resources/layouts/"
LAYOUT_DUMP = "Retribution/layouts.p"

LAYOUT_TYPES = {
    GroupRole.AIR_DEFENSE: AntiAirLayout,
    GroupRole.BUILDING: BuildingLayout,
    GroupRole.NAVAL: NavalLayout,
    GroupRole.GROUND_FORCE: GroundForceLayout,
    GroupRole.DEFENSES: DefensesLayout,
}

LOCATIONS_TO_CHECK: list[Path] = []


class LayoutLoader:
    # Map of all available layouts indexed by name
    _layouts: dict[str, TgoLayout] = {}

    def __init__(self) -> None:
        self._layouts = {}

    def initialize(self) -> None:
        if not self._layouts:
            self.initialize_locations_to_check()
            with logged_duration("Loading layouts"):
                self.load_templates()

    @staticmethod
    def initialize_locations_to_check() -> None:
        global LOCATIONS_TO_CHECK
        if not LOCATIONS_TO_CHECK:
            LOCATIONS_TO_CHECK = [
                Path(LAYOUT_DIR),
                persistency.layouts_dir(),
            ]

    @property
    def layouts(self) -> Iterator[TgoLayout]:
        self.initialize()
        yield from self._layouts.values()

    def load_templates(self) -> None:
        """This will load all pre-loaded layouts from a pickle file.
        If pickle can not be loaded it will import and dump the layouts"""
        # We use a pickle for performance reasons. Importing takes many seconds
        source_signature = self._layout_source_signature()
        file = persistency.base_path() / LAYOUT_DUMP
        if file.is_file():
            # Load from pickle if existing
            with file.open("rb") as f:
                try:
                    dump = pickle.load(f)
                    if isinstance(dump, tuple) and len(dump) == 3:
                        version, dump_signature, self._layouts = dump
                    else:
                        # Backward compatibility for older dumps:
                        # (version, layouts)
                        version, self._layouts = dump
                        dump_signature = None
                    # Check if the game version of the dump is identical to the current
                    if version == VERSION and dump_signature == source_signature:
                        return
                except Exception as e:
                    logging.exception(f"Error {e} reading layouts dump. Recreating.")
        # If no dump is available or game version is different create a new dump
        self.import_templates(source_signature)

    def import_templates(self, source_signature: str | None = None) -> None:
        """This will import all layouts from the template folder
        and dumps them to a pickle"""
        self._layouts = {}
        mappings: dict[str, list[LayoutMapping]] = defaultdict(list)
        with logged_duration("Parsing mapping yamls"):
            for path_to_check in LOCATIONS_TO_CHECK:
                for file in path_to_check.rglob("*.yaml"):
                    self._process_yaml(file, mappings)

        with logged_duration(f"Parsing all layout miz multithreaded"):
            with ThreadPoolExecutor() as exe:
                exe.map(self._load_from_miz, mappings.keys(), mappings.values())

        # Sort al the LayoutGroups with the correct index
        for layout in self._layouts.values():
            layout.groups.sort(key=lambda g: g.group_index)
            for group in layout.groups:
                group.unit_groups.sort(key=lambda ug: ug.unit_index)

        logging.info(f"Imported {len(self._layouts)} layouts")
        self._dump_templates(source_signature or self._layout_source_signature())

    @staticmethod
    def _process_yaml(file: Path, mappings: dict[str, list[LayoutMapping]]) -> None:
        if not file.is_file():
            raise RuntimeError(f"{file.name} is not a file")
        with file.open("r", encoding="utf-8") as f:
            mapping_dict = yaml.safe_load(f)
        template_map = LayoutMapping.from_dict(mapping_dict, f.name)
        mappings[template_map.layout_file].append(template_map)

    def _dump_templates(self, source_signature: str) -> None:
        file = persistency.base_path() / LAYOUT_DUMP
        dump = (VERSION, source_signature, self._layouts)
        with file.open("wb") as fdata:
            pickle.dump(dump, fdata)

    @staticmethod
    def _layout_source_signature() -> str:
        """
        Compute a stable signature for all layout source files so cache invalidates
        whenever any layout YAML or MIZ changes.
        """
        hasher = hashlib.sha256()
        files: list[Path] = []
        for root in LOCATIONS_TO_CHECK:
            if not root.exists():
                continue
            files.extend(root.rglob("*.yaml"))
            files.extend(root.rglob("*.miz"))

        for file in sorted((f for f in files if f.is_file()), key=lambda p: str(p)):
            stat = file.stat()
            hasher.update(str(file).encode("utf-8"))
            hasher.update(str(stat.st_mtime_ns).encode("ascii"))
            hasher.update(str(stat.st_size).encode("ascii"))

        return hasher.hexdigest()

    def _load_from_miz(self, miz: str, mappings: list[LayoutMapping]) -> None:
        path = Path(miz)
        locations_to_check = deepcopy(LOCATIONS_TO_CHECK)
        while not path.exists() and locations_to_check:
            path = locations_to_check.pop() / miz
            miz = path.absolute().as_posix()
        if not path.exists():
            logging.warning(f"Layout miz file not found: '{miz}'")
            return
        template_position: dict[str, Point] = {}
        temp_mis = dcs.Mission()
        with logged_duration(f"Parsing {miz}"):
            # The load_file takes a lot of time to compute. That's why the layouts
            # are written to a pickle and can be reloaded from the ui
            # Example the whole routine: 0:00:00.934417,
            # the .load_file() method: 0:00:00.920409
            temp_mis.load_file(miz)

        for mapping in mappings:
            groups_found = False
            layout_group_names = [
                gm.name for _, gms in mapping.groups.items() for gm in gms
            ]
            miz_groups = []

            # Find the group from the mapping in any coalition
            for country in itertools.chain(
                temp_mis.coalition["red"].countries.values(),
                temp_mis.coalition["blue"].countries.values(),
            ):
                for dcs_group in itertools.chain(
                    temp_mis.country(country.name).vehicle_group,
                    temp_mis.country(country.name).ship_group,
                    temp_mis.country(country.name).static_group,
                ):
                    miz_groups.append(dcs_group.name)
                    try:
                        g_id, u_id, group_name, group_mapping = mapping.group_for_name(
                            dcs_group.name
                        )
                        groups_found = True
                    except KeyError:
                        continue

                    if not isinstance(dcs_group, StaticGroup) and max(
                        group_mapping.unit_count
                    ) > len(dcs_group.units):
                        logging.error(
                            f"Incorrect unit_count found in Layout {mapping.name}-{group_mapping.name}"
                        )

                    layout = self._layouts.get(mapping.name, None)
                    if layout is None:
                        # Create a new template
                        layout = LAYOUT_TYPES[mapping.primary_role](
                            mapping.name, mapping.description
                        )
                        layout.generic = mapping.generic
                        layout.tasks = mapping.tasks
                        self._layouts[layout.name] = layout
                    for i, unit in enumerate(dcs_group.units):
                        unit_group = None
                        for _unit_group in layout.all_unit_groups:
                            if _unit_group.name == group_mapping.name:
                                # We already have a layoutgroup for this dcs_group
                                unit_group = _unit_group
                        if not unit_group:
                            unit_group = TgoLayoutUnitGroup(
                                group_mapping.name,
                                [],
                                group_mapping.unit_count,
                                group_mapping.unit_types,
                                group_mapping.unit_classes,
                                group_mapping.fallback_classes,
                                u_id,
                            )
                            unit_group.optional = group_mapping.optional
                            unit_group.fill = group_mapping.fill
                            unit_group.sub_task = group_mapping.sub_task
                            tgo_group = None
                            for _tgo_group in layout.groups:
                                if _tgo_group.group_name == group_name:
                                    tgo_group = _tgo_group
                            if tgo_group is None:
                                tgo_group = TgoLayoutGroup(group_name, g_id)
                                layout.groups.append(tgo_group)
                            tgo_group.unit_groups.append(unit_group)
                        layout_unit = LayoutUnit.from_unit(unit)
                        if i == 0 and layout.name not in template_position:
                            template_position[layout.name] = unit.position
                        layout_unit.position = (
                            layout_unit.position - template_position[layout.name]
                        )
                        unit_group.layout_units.append(layout_unit)

            if not groups_found:
                logging.error(
                    f"Layout '{mapping.name}' could not be loaded from '{miz}'. "
                    f"No groups in the mission file match the expected names. "
                    f"Expected group names: {layout_group_names}. "
                    f"Actual group names in mission: {miz_groups}. "
                    f"Fix the mission file by creating groups with the expected names."
                )

    def by_name(self, name: str) -> TgoLayout:
        self.initialize()
        return self._layouts[name]
