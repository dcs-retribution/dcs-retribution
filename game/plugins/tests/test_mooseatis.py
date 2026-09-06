from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from game.plugins.mooseatis import MooseAtisPlugin


def _plugin() -> MooseAtisPlugin:
    plugin = MooseAtisPlugin.__new__(MooseAtisPlugin)
    plugin.identifier = "MooseAtis"
    plugin.other_resource_files = ["SoundFiles/Wind.ogg", "SoundFiles/QNH.ogg"]
    return plugin


def _lua_generator(terrain_name: str) -> MagicMock:
    gen = MagicMock()
    gen.game.theater.terrain.name = terrain_name
    return gen


def test_injects_static_common_files() -> None:
    gen = _lua_generator("Caucasus")
    _plugin().inject_other_resource_files(gen)
    injected = [c.args[1] for c in gen.inject_other_plugin_resources.call_args_list]
    assert "SoundFiles/Wind.ogg" in injected
    assert "SoundFiles/QNH.ogg" in injected


def test_injects_present_terrain_name_files(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    names_dir = tmp_path / "MooseAtis" / "SoundFiles" / "Caucasus"
    names_dir.mkdir(parents=True)
    (names_dir / "Batumi.ogg").write_bytes(b"")
    monkeypatch.setattr("game.plugins.mooseatis.PLUGIN_RESOURCE_ROOT", tmp_path)
    gen = _lua_generator("Caucasus")
    _plugin().inject_other_resource_files(gen)
    injected = [c.args[1] for c in gen.inject_other_plugin_resources.call_args_list]
    assert "SoundFiles/Caucasus/Batumi.ogg" in injected


def test_no_terrain_files_is_noop(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr("game.plugins.mooseatis.PLUGIN_RESOURCE_ROOT", tmp_path)
    gen = _lua_generator("Nevada")
    _plugin().inject_other_resource_files(gen)
    injected = [c.args[1] for c in gen.inject_other_plugin_resources.call_args_list]
    assert injected == ["SoundFiles/Wind.ogg", "SoundFiles/QNH.ogg"]
