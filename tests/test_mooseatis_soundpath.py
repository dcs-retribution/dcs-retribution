from pathlib import Path

PLUGIN_ATIS_LUA = Path("resources/plugins/MooseAtis/Plugin_Atis.lua")


def test_atis_soundfiles_path_points_at_l10n_default() -> None:
    # pydcs flattens every bundled resource to l10n/DEFAULT/<basename>, so MOOSE
    # ATIS must look for its .ogg files there. An empty soundfiles path makes
    # DCS play bare basenames it cannot resolve -> silent ATIS on every field.
    lua = PLUGIN_ATIS_LUA.read_text(encoding="utf-8")
    assert 'local soundPath = "l10n/DEFAULT/"' in lua
    assert "SetSoundfilesPath(soundPath, soundPath, soundPath)" in lua
    assert 'SetSoundfilesPath("", "", "")' not in lua
