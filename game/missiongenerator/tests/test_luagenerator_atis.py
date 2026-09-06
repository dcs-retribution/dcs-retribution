from __future__ import annotations

from unittest.mock import MagicMock

from dcs.task import Modulation

from game.missiongenerator.luagenerator import LuaGenerator
from game.missiongenerator.missiondata import AtisInfo, MissionData
from game.radio.radios import MHz


def _lua_generator(mission_data: MissionData) -> LuaGenerator:
    gen = LuaGenerator.__new__(LuaGenerator)
    gen.game = MagicMock()
    gen.mission = MagicMock()
    gen.mission_data = mission_data
    gen.plugin_scripts = []
    return gen


def test_atis_section_serialized_for_blue_fields() -> None:
    md = MissionData(
        atis_frequencies=[
            AtisInfo("Batumi", MHz(131)),
            AtisInfo("Kobuleti", MHz(131, 500, Modulation.AM)),
        ]
    )
    lua = _lua_generator(md)._serialize_atis_lua()
    assert "Batumi" in lua and "Kobuleti" in lua
    assert "131" in lua  # MHz value emitted
    assert "modulation" in lua


def test_no_atis_section_when_empty() -> None:
    lua = _lua_generator(MissionData())._serialize_atis_lua()
    assert lua == ""
