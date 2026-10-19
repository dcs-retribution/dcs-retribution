import os
from pathlib import Path

import pytest

from qt_ui import dcs_paths
from qt_ui.dcs_paths import (
    candidate_saved_games_dirs,
    detect_dcs_saved_games_dir,
    looks_like_dcs_install,
    looks_like_dcs_saved_games,
    pick_saved_games_dir,
    read_dcs_variant,
)


def _make_dcs_folder(path: Path, log_mtime: float | None = None) -> Path:
    (path / "Config").mkdir(parents=True)
    if log_mtime is not None:
        log = path / "Logs" / "dcs.log"
        log.parent.mkdir()
        log.write_text("log")
        os.utime(log, (log_mtime, log_mtime))
    return path


def test_pick_prefers_most_recently_used_folder(tmp_path: Path) -> None:
    stale_beta = _make_dcs_folder(tmp_path / "DCS.openbeta", log_mtime=1_000)
    active = _make_dcs_folder(tmp_path / "DCS", log_mtime=2_000)

    # Even when the stale folder is listed first, the active one wins.
    assert pick_saved_games_dir([stale_beta, active]) == active


def test_pick_falls_back_to_candidate_order(tmp_path: Path) -> None:
    first = _make_dcs_folder(tmp_path / "DCS")
    second = _make_dcs_folder(tmp_path / "DCS.openbeta")

    assert pick_saved_games_dir([first, second]) == first


def test_pick_ignores_missing_folders(tmp_path: Path) -> None:
    present = _make_dcs_folder(tmp_path / "DCS.openbeta")

    assert pick_saved_games_dir([tmp_path / "DCS", present]) == present
    assert pick_saved_games_dir([tmp_path / "nope"]) is None


def test_candidates_put_variant_first_and_dedupe_roots(tmp_path: Path) -> None:
    root = tmp_path / "Saved Games"

    assert candidate_saved_games_dirs([root, root], "openbeta") == [
        root / "DCS.openbeta",
        root / "DCS",
    ]
    assert candidate_saved_games_dirs([root], None) == [
        root / "DCS",
        root / "DCS.openbeta",
    ]


def test_read_dcs_variant(tmp_path: Path) -> None:
    assert read_dcs_variant("") is None
    assert read_dcs_variant(str(tmp_path)) is None

    (tmp_path / "dcs_variant.txt").write_text("openbeta\r\n")
    assert read_dcs_variant(str(tmp_path)) == "openbeta"


def test_detect_uses_relocated_saved_games_folder(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    home = tmp_path / "home"
    relocated = tmp_path / "D_drive" / "Saved Games"
    _make_dcs_folder(relocated / "DCS", log_mtime=2_000)
    # A leftover default-location folder that DCS no longer writes to.
    _make_dcs_folder(home / "Saved Games" / "DCS", log_mtime=1_000)

    monkeypatch.setattr(Path, "home", classmethod(lambda cls: home))
    monkeypatch.setattr(dcs_paths, "windows_saved_games_root", lambda: relocated)

    assert detect_dcs_saved_games_dir() == str(relocated / "DCS")


def test_detect_falls_back_to_default_when_nothing_exists(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
    monkeypatch.setattr(dcs_paths, "windows_saved_games_root", lambda: None)

    assert detect_dcs_saved_games_dir() == str(tmp_path / "Saved Games" / "DCS")


def test_looks_like_dcs_saved_games(tmp_path: Path) -> None:
    assert not looks_like_dcs_saved_games(str(tmp_path / "missing"))
    assert not looks_like_dcs_saved_games(str(tmp_path))

    (tmp_path / "Missions").mkdir()
    assert looks_like_dcs_saved_games(str(tmp_path))


def test_looks_like_dcs_install(tmp_path: Path) -> None:
    assert not looks_like_dcs_install(str(tmp_path))

    scripts = tmp_path / "Scripts"
    scripts.mkdir()
    (scripts / "MissionScripting.lua").write_text("-- lua")
    assert looks_like_dcs_install(str(tmp_path))
