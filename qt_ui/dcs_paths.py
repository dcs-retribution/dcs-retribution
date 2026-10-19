"""Locates DCS folders on the user's computer.

The "Saved Games" folder is the tricky one. Users frequently relocate their
Windows "Saved Games" folder (to another drive, or into OneDrive), so assuming
``~/Saved Games`` silently picks a folder DCS never uses. Many installs also still carry a stale ``DCS.openbeta`` folder from
before ED merged the stable and beta branches, which must not win over the
``DCS`` folder that is actually in use.
"""

from __future__ import annotations

import logging
import os
import re
import sys
from pathlib import Path
from typing import Iterable, Optional

# Files DCS touches whenever it runs. Their modification time tells us which
# candidate folder is the one in active use.
_ACTIVITY_MARKERS = (
    Path("Logs") / "dcs.log",
    Path("Config") / "options.lua",
)

# Subfolders DCS creates on first launch. A folder with none of these is very
# unlikely to be a DCS Saved Games folder.
_DCS_SUBFOLDERS = ("Config", "Logs", "MissionEditor", "Missions")


if sys.platform == "win32":

    def windows_saved_games_root() -> Optional[Path]:
        """Returns the user's real "Saved Games" folder, wherever it is."""
        try:
            import ctypes
            from ctypes import wintypes

            class _Guid(ctypes.Structure):
                _fields_ = [
                    ("Data1", wintypes.DWORD),
                    ("Data2", wintypes.WORD),
                    ("Data3", wintypes.WORD),
                    ("Data4", ctypes.c_ubyte * 8),
                ]

            # FOLDERID_SavedGames {4C5C32FF-BB9D-43B0-B5B4-2D72E54EAAA4}
            folder_id = _Guid(
                0x4C5C32FF,
                0xBB9D,
                0x43B0,
                (ctypes.c_ubyte * 8)(0xB5, 0xB4, 0x2D, 0x72, 0xE5, 0x4E, 0xAA, 0xA4),
            )
            path_ptr = ctypes.c_wchar_p()
            result = ctypes.windll.shell32.SHGetKnownFolderPath(
                ctypes.byref(folder_id), 0, None, ctypes.byref(path_ptr)
            )
            try:
                if result != 0 or not path_ptr.value:
                    return None
                return Path(path_ptr.value)
            finally:
                ctypes.windll.ole32.CoTaskMemFree(path_ptr)
        except Exception:
            logging.exception("Could not resolve the Windows Saved Games folder")
            return None

else:

    def windows_saved_games_root() -> Optional[Path]:
        """The Saved Games known folder only exists on Windows."""
        return None


def read_dcs_variant(install_dir: str) -> Optional[str]:
    """Returns the suffix from dcs_variant.txt (e.g. "openbeta"), if any."""
    if not install_dir:
        return None
    variant_file = Path(install_dir) / "dcs_variant.txt"
    try:
        suffix = re.sub(r"[^\w-]", "", variant_file.read_text())
    except OSError:
        return None
    return suffix or None


def _activity_time(folder: Path) -> float:
    for marker in _ACTIVITY_MARKERS:
        try:
            return (folder / marker).stat().st_mtime
        except OSError:
            continue
    return 0.0


def pick_saved_games_dir(candidates: Iterable[Path]) -> Optional[Path]:
    """Picks the existing candidate DCS has used most recently.

    Ties (including folders with no activity markers at all) are broken by the
    order of ``candidates``.
    """
    existing = [c for c in dict.fromkeys(candidates) if c.is_dir()]
    if not existing:
        return None
    return max(existing, key=_activity_time)


def candidate_saved_games_dirs(
    roots: Iterable[Path], variant: Optional[str]
) -> list[Path]:
    names = ["DCS", "DCS.openbeta"]
    if variant:
        variant_name = f"DCS.{variant}"
        if variant_name in names:
            names.remove(variant_name)
        names.insert(0, variant_name)
    return [root / name for root in dict.fromkeys(roots) for name in names]


def detect_dcs_saved_games_dir(install_dir: str = "") -> str:
    """Best guess at the DCS Saved Games directory for this computer.

    Falls back to the conventional default even if it does not exist, matching
    the previous behaviour so first-run setup still has something to show.
    """
    roots: list[Path] = []
    known_root = windows_saved_games_root()
    if known_root is not None:
        roots.append(known_root)
    roots.append(Path.home() / "Saved Games")

    candidates = candidate_saved_games_dirs(roots, read_dcs_variant(install_dir))
    picked = pick_saved_games_dir(candidates)
    if picked is not None:
        return str(picked)
    return str(candidates[0])


def looks_like_dcs_saved_games(folder: str) -> bool:
    """True if the folder contains anything DCS creates in Saved Games."""
    path = Path(folder)
    return path.is_dir() and any((path / name).is_dir() for name in _DCS_SUBFOLDERS)


def looks_like_dcs_install(folder: str) -> bool:
    """True if the folder has the MissionScripting.lua Retribution replaces."""
    return (Path(folder) / "Scripts" / "MissionScripting.lua").is_file()
