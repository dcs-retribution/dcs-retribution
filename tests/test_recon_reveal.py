"""Recon intel-fog reveal-on-engage: a struck or overflown enemy site becomes
known (composition revealed, permanently). Friendly sites are never gated.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any, cast

from dcs.mapping import Point

from game.ato.flighttype import FlightType
from game.sim.gameupdateevents import GameUpdateEvents
from game.sim.missionresultsprocessor import MissionResultsProcessor
from game.theater import Player
from game.theater.controlpoint import OffMapSpawn
from game.theater.presetlocation import PresetLocation
from game.theater.theatergroundobject import SamGroundObject
from game.utils import Heading


class _EnemySam(SamGroundObject):
    def is_friendly(self, to_player: Player) -> bool:
        return False


def _enemy_sam() -> SamGroundObject:
    location = PresetLocation(
        name="target",
        position=Point(0, 0, None),  # type: ignore[arg-type]
        heading=Heading(0),
    )
    control_point = OffMapSpawn(
        name="enemy-cp",
        position=Point(0, 0, None),  # type: ignore[arg-type]
        theater=None,  # type: ignore[arg-type]
        starts_blue=Player.RED,
    )
    return _EnemySam(
        name="Enemy SAM",
        location=location,
        control_point=control_point,
        task=None,
    )


def _processor(*packages: Any) -> MissionResultsProcessor:
    game = SimpleNamespace(
        blue=SimpleNamespace(ato=SimpleNamespace(packages=list(packages))),
        red=SimpleNamespace(ato=SimpleNamespace(packages=[])),
    )
    return MissionResultsProcessor(game)  # type: ignore[arg-type]


def _debrief(surviving: int) -> Any:
    return SimpleNamespace(
        air_losses=SimpleNamespace(surviving_flight_members=lambda flight: surviving)
    )


def test_struck_enemy_site_is_revealed() -> None:
    tgo = _enemy_sam()
    assert tgo.discovered_by_player is False
    processor = _processor()
    processor.reveal_discovered_sites({tgo}, _debrief(0), GameUpdateEvents())
    assert tgo.discovered_by_player is True


def test_surviving_offensive_overflight_reveals_target() -> None:
    tgo = _enemy_sam()
    flight = SimpleNamespace(flight_type=FlightType.STRIKE)
    package = SimpleNamespace(target=tgo, flights=[flight])
    processor = _processor(package)
    # No units struck, but a surviving striker overflew the target.
    processor.reveal_discovered_sites(set(), _debrief(1), GameUpdateEvents())
    assert tgo.discovered_by_player is True


def test_dead_flight_with_no_survivors_does_not_reveal() -> None:
    tgo = _enemy_sam()
    flight = SimpleNamespace(flight_type=FlightType.DEAD)
    package = SimpleNamespace(target=tgo, flights=[flight])
    processor = _processor(package)
    processor.reveal_discovered_sites(set(), _debrief(0), GameUpdateEvents())
    assert tgo.discovered_by_player is False
