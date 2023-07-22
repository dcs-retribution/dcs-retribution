from __future__ import annotations

import logging
import pickle
import shutil
from pathlib import Path
from typing import Optional, TYPE_CHECKING, Any

import dcs.terrain.falklands.airports

from game.profiling import logged_duration

if TYPE_CHECKING:
    from game import Game

_dcs_saved_game_folder: Optional[str] = None


# fmt: off
class DummyObject:
    def __setstate__(self, state: dict[str, Any]) -> None:
        self.__dict__.update(state)


class MigrationUnpickler(pickle.Unpickler):
    """Custom unpickler to migrate campaign save-files for when components have been moved"""
    def find_class(self, module: Any, name: str) -> Any:
        if name == "NightMissions":
            from game.settings import NightMissions
            return NightMissions
        if name == "Conditions":
            from game.weather.conditions import Conditions
            return Conditions
        if name == "AtmosphericConditions":
            from game.weather.atmosphericconditions import AtmosphericConditions
            return AtmosphericConditions
        if name == "WindConditions":
            from game.weather.wind import WindConditions
            return WindConditions
        if name == "Clouds":
            from game.weather.clouds import Clouds
            return Clouds
        if name == "Fog":
            from game.weather.fog import Fog
            return Fog
        if name == "ClearSkies":
            from game.weather.weather import ClearSkies
            return ClearSkies
        if name == "Cloudy":
            from game.weather.weather import Cloudy
            return Cloudy
        if name == "Raining":
            from game.weather.weather import Raining
            return Raining
        if name == "Thunderstorm":
            from game.weather.weather import Thunderstorm
            return Thunderstorm
        if name == "Hipico":
            return dcs.terrain.falklands.airports.Hipico_Flying_Club
        if name in ["SaveManager", "SaveGameBundle"]:
            return DummyObject
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


def payloads_dir(backup: bool = False) -> Path:
    payloads = base_path() / "MissionEditor" / "UnitPayloads"
    if backup:
        return payloads / "_retribution_backups"
    return payloads


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
