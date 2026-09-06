from __future__ import annotations

from unittest.mock import MagicMock

from game.missiongenerator.briefinggenerator import MissionInfoGenerator
from game.missiongenerator.missiondata import AtisInfo
from game.radio.radios import MHz


def test_add_atis_collects_by_name() -> None:
    gen = MissionInfoGenerator(MagicMock(), MagicMock())
    gen.add_atis(AtisInfo("Batumi", MHz(131)))
    gen.add_atis(AtisInfo("Kobuleti", MHz(131, 500)))
    assert gen.atis_by_name["Batumi"].hertz == MHz(131).hertz
    assert "Kobuleti" in gen.atis_by_name
