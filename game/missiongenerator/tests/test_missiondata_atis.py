from __future__ import annotations

from game.missiongenerator.missiondata import AtisInfo, MissionData
from game.radio.radios import MHz


def test_mission_data_atis_frequencies_defaults_empty() -> None:
    assert MissionData().atis_frequencies == []


def test_atis_info_holds_airfield_and_frequency() -> None:
    freq = MHz(131)
    info = AtisInfo(airfield_name="Batumi", frequency=freq)
    assert info.airfield_name == "Batumi"
    assert info.frequency is freq
