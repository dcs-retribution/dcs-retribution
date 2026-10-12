"""Fog and dust reach the mission in the form DCS keeps (me_weather.lua fixFog)."""

from __future__ import annotations

import datetime
from types import SimpleNamespace
from typing import Any, Optional

from dcs.mission import Mission
from dcs.terrain.caucasus.caucasus import Caucasus
from dcs.weather import Wind

from game.missiongenerator.environmentgenerator import EnvironmentGenerator
from game.utils import inches_hg, nautical_miles
from game.weather.atmosphericconditions import AtmosphericConditions
from game.weather.dust import Dust
from game.weather.fog import Fog
from game.weather.wind import WindConditions


def _generate(fog: Optional[Fog], dust: Optional[Dust], auto_fog: bool) -> Mission:
    weather = SimpleNamespace(
        atmospheric=AtmosphericConditions(
            qnh=inches_hg(29.92), temperature_celsius=15, turbulence_per_10cm=5
        ),
        clouds=None,
        fog=fog,
        dust=dust,
        wind=WindConditions(at_0m=Wind(), at_2000m=Wind(), at_8000m=Wind()),
    )
    mission = Mission(Caucasus())
    conditions: Any = SimpleNamespace(weather=weather)
    EnvironmentGenerator(
        mission, conditions, datetime.datetime(2026, 6, 9, 18), auto_fog
    ).generate()
    return mission


FOG = Fog(visibility=nautical_miles(1.5), thickness=250)
DUST = Dust(visibility=nautical_miles(1.0))


def test_manual_fog_is_switched_on() -> None:
    d = _generate(FOG, None, auto_fog=False).weather.dict()
    assert d["enable_fog"] is True
    assert d["fog"] == {"thickness": 250, "visibility": 2778}
    assert "fog2" not in d


def test_auto_fog_leaves_the_fog_block_off() -> None:
    d = _generate(FOG, None, auto_fog=True).weather.dict()
    assert d["enable_fog"] is False
    assert d["fog2"] == {"mode": 2}


def test_dust_is_written_with_no_fog() -> None:
    d = _generate(None, DUST, auto_fog=False).weather.dict()
    assert d["enable_dust"] is True and d["dust_density"] == 1852


def test_dust_is_dropped_beside_any_fog() -> None:
    for fog, auto_fog in ((FOG, False), (None, True)):
        d = _generate(fog, DUST, auto_fog=auto_fog).weather.dict()
        assert d["enable_dust"] is False
