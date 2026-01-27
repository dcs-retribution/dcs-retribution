from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
import logging
from pathlib import Path
from typing import Iterator, Any

import yaml

from dcs.unitgroup import Group
from game import persistency
from game.data.units import UnitClass
from game.ground_forces.combat_stance import CombatStance
from game.ground_forces.ai_ground_planner import CombatGroupRole
from game.profiling import logged_duration

FRONTLINE_GROUP_DIR = "resources/groups/frontline/"

LOCATIONS_TO_CHECK: list[Path] = []


@dataclass
class FrontlineUnitRequirement:
    """Represents a unit requirement within a frontline group template."""

    name: str
    min_count: int
    max_count: int
    unit_classes: list[UnitClass] = field(default_factory=list)

    @staticmethod
    def from_dict(d: dict[str, Any]) -> FrontlineUnitRequirement:
        try:
            name = d.get("name")
            min_count = d.get("min_count")
            max_count = d.get("max_count")
            unit_classes = []
            class_names = d.get("unit_classes", [])
            for class_name in class_names:
                unit_classes.append(UnitClass[class_name.upper()])
        except Exception as e:
            logging.error(
                f"Error parsing unit classes for unit '{d.get('name', 'Unknown')}': {e}"
            )
        return FrontlineUnitRequirement(
            name,
            min_count=min_count,
            max_count=max_count,
            unit_classes=unit_classes,
        )


@dataclass
class FrontlineGroupTemplate:
    """Represents a frontline combat group template loaded from YAML."""

    name: str
    role: CombatGroupRole
    formation: Group.Formation
    distance_from_frontline: tuple[int, int]
    units: dict[str, list[FrontlineUnitRequirement]] = field(default_factory=dict)
    preferred_stances: list[CombatStance] = field(default_factory=list)

    @staticmethod
    def from_dict(d: dict[str, Any], file_name: str) -> FrontlineGroupTemplate:
        units: dict[str, list[FrontlineUnitRequirement]] = defaultdict(list)
        for unit_data in d.get("units", []):
            unit_req = FrontlineUnitRequirement.from_dict(unit_data)
            units[unit_req.name].append(unit_req)
        try:
            name = d.get("name")
            role_str = d.get("role")
            role = CombatGroupRole[role_str]
            formation_str = d.get("formation")
            formation = Group.Formation[formation_str]
            distance_data = d.get("distance_from_frontline", {})
            distance_min = distance_data.get("min")
            distance_max = distance_data.get("max")
        except Exception as e:
            logging.error(
                f"Error parsing frontline group template from '{file_name}': {e}"
            )
        return FrontlineGroupTemplate(
            name=name,
            role=role,
            formation=formation,
            distance_from_frontline=(distance_min, distance_max),
            units=units,
        )


class FrontlineGroupLoader:
    """Loads frontline combat group templates from YAML files."""

    _templates: dict[str, FrontlineGroupTemplate] = {}

    def __init__(self) -> None:
        self._templates = {}

    def initialize(self) -> None:
        """Initialize and load all frontline group templates if not already loaded."""
        if not self._templates:
            self.initialize_locations_to_check()
            with logged_duration("Loading frontline group templates"):
                self.load_templates()

    @staticmethod
    def initialize_locations_to_check() -> None:
        global LOCATIONS_TO_CHECK
        if not LOCATIONS_TO_CHECK:
            LOCATIONS_TO_CHECK = [
                Path(FRONTLINE_GROUP_DIR),
                persistency.frontline_groups_dir(),
            ]

    @property
    def templates(self) -> Iterator[FrontlineGroupTemplate]:
        """Iterate over all loaded frontline group templates."""
        self.initialize()
        yield from self._templates.values()

    def load_templates(self) -> None:
        """Load all frontline group templates from YAML files."""
        for path_to_check in LOCATIONS_TO_CHECK:
            if not path_to_check.exists():
                continue

            for yaml_file in path_to_check.glob("*.yaml"):
                try:
                    self._load_template_from_file(yaml_file)
                except Exception as e:
                    logging.error(
                        f"Error loading frontline group template from {yaml_file}: {e}"
                    )
                    logging.exception(e)

        logging.info(f"Loaded {len(self._templates)} frontline group templates")

    def _load_template_from_file(self, yaml_file: Path) -> None:
        """Load a single frontline group template from a YAML file."""
        with yaml_file.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        if not data:
            logging.warning(f"Empty YAML file: {yaml_file}")
            return

        template = FrontlineGroupTemplate.from_dict(data, yaml_file.name)
        self._templates[template.name] = template
        logging.debug(f"Loaded frontline group template: {template.name}")

    def by_name(self, name: str) -> FrontlineGroupTemplate:
        """Get a frontline group template by name."""
        self.initialize()
        return self._templates[name]

    def by_role(self, role: CombatGroupRole) -> list[FrontlineGroupTemplate]:
        """Get all frontline group templates for a specific role."""
        self.initialize()
        return [t for t in self._templates.values() if t.role == role]

    def all_templates(self) -> list[FrontlineGroupTemplate]:
        """Get all loaded frontline group templates as a list."""
        self.initialize()
        return list(self._templates.values())
