from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Dict, Iterator, List, Optional, Type

import yaml

from game import persistency
from game.factions.faction import Faction

FACTION_DIRECTORY = Path("./resources/factions/")


class FactionLoader:
    def __init__(self) -> None:
        self._factions: Optional[Dict[str, Faction]] = None

    @property
    def factions(self) -> Dict[str, Faction]:
        self.initialize()
        assert self._factions is not None
        return self._factions

    def initialize(self) -> None:
        if self._factions is None:
            self._factions = self.load_factions()

    @staticmethod
    def find_faction_files_in(path: Path) -> List[Path]:
        return (
            [f for f in path.glob("*.json") if f.is_file()]
            + [f for f in path.glob("*.yaml") if f.is_file()]
            + [f for f in path.glob("*.yml") if f.is_file()]
        )

    @classmethod
    def load_factions(cls: Type[FactionLoader]) -> Dict[str, Faction]:
        user_faction_path = persistency.base_path() / "Retribution/Factions"
        files = cls.find_faction_files_in(
            FACTION_DIRECTORY
        ) + cls.find_faction_files_in(user_faction_path)
        factions = {}

        for f in files:
            try:
                with f.open("r", encoding="utf-8") as fdata:
                    if "yml" in f.name or "yaml" in f.name:
                        data = yaml.safe_load(fdata)
                    else:
                        data = json.load(fdata)
                    factions[data["name"]] = Faction.from_dict(data)
                    logging.info("Loaded faction : " + str(f))
            except Exception:
                logging.exception(f"Unable to load faction : {f}")

        return factions

    def __getitem__(self, name: str) -> Faction:
        return self.factions[name]

    def __iter__(self) -> Iterator[str]:
        return iter(self.factions.keys())
