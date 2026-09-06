from __future__ import annotations

from unittest.mock import MagicMock, patch

from game.missiongenerator.missiongenerator import MissionGenerator
from game.missiongenerator.missiondata import AtisInfo, MissionData
from game.radio.radios import MHz, RadioRegistry


def _generator(plugin_enabled: bool) -> MissionGenerator:
    gen = MissionGenerator.__new__(MissionGenerator)
    gen.game = MagicMock()
    gen.game.settings.plugins.get.return_value = plugin_enabled
    gen.mission_data = MissionData()
    gen.radio_registry = RadioRegistry()
    return gen


def test_populates_atis_frequencies_when_enabled() -> None:
    gen = _generator(plugin_enabled=True)
    with patch("game.missiongenerator.missiongenerator.AtisGenerator") as atis_cls:
        atis_cls.return_value.generate.return_value = [AtisInfo("Batumi", MHz(131))]
        gen.generate_atis()
    assert [a.airfield_name for a in gen.mission_data.atis_frequencies] == ["Batumi"]


def test_skips_when_plugin_disabled() -> None:
    gen = _generator(plugin_enabled=False)
    with patch("game.missiongenerator.missiongenerator.AtisGenerator") as atis_cls:
        gen.generate_atis()
    atis_cls.assert_not_called()
    assert gen.mission_data.atis_frequencies == []
