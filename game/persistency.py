from __future__ import annotations

import logging
import pickle
import shutil
from pathlib import Path
from typing import Optional, TYPE_CHECKING

from game.profiling import logged_duration

if TYPE_CHECKING:
    from game import Game

_dcs_saved_game_folder: Optional[str] = None


# fmt: off
class MigrationUnpickler(pickle.Unpickler):
    """Custom unpickler to migrate campaign save-files for when components have been moved"""
    def find_class(self, module, name):
        if name == "NightMissions":
            from game.weather.conditions import NightMissions
            return NightMissions
        if name == "Conditions":
            from game.weather.conditions import Conditions
            return Conditions
        if name == "ClearSkies":
            from game.weather.conditions import ClearSkies
            return ClearSkies
        if name == "AtmosphericConditions":
            from game.weather.atmosphericconditions import AtmosphericConditions
            return AtmosphericConditions
        if name == "WindConditions":
            from game.weather.wind import WindConditions
            return WindConditions
        return super().find_class(module, name)
# fmt: on


def setup(user_folder: str) -> None:
    global _dcs_saved_game_folder
    _dcs_saved_game_folder = user_folder
    if not save_dir().exists():
        save_dir().mkdir(parents=True)


def base_path() -> Path:
    global _dcs_saved_game_folder
    assert _dcs_saved_game_folder
    return Path(_dcs_saved_game_folder)


def settings_dir() -> Path:
    return base_path() / "Retribution" / "Settings"


def save_dir() -> Path:
    return base_path() / "Retribution" / "Saves"


def _temporary_save_file() -> str:
    return str(save_dir() / "tmpsave.retribution")


def _autosave_path() -> str:
    return str(save_dir() / "autosave.retribution")


def mission_path_for(name: str) -> Path:
    return base_path() / "Missions" / name


def load_game(path: str) -> Optional[Game]:
    with open(path, "rb") as f:
        try:
            save = MigrationUnpickler(f).load()
            save.savepath = path
            return save
        except Exception:
            logging.exception("Invalid Save game")
            return None


def save_game(game: Game) -> bool:
    with logged_duration("Saving game"):
        try:
            with open(_temporary_save_file(), "wb") as f:
                pickle.dump(game, f)
            shutil.copy(_temporary_save_file(), game.savepath)
            return True
        except Exception:
            logging.exception("Could not save game")
            return False


def autosave(game: Game) -> bool:
    """
    Autosave to the autosave location
    :param game: Game to save
    :return: True if saved successfully
    """
    try:
        with open(_autosave_path(), "wb") as f:
            pickle.dump(game, f)
        return True
    except Exception:
        logging.exception("Could not save game")
        return False
