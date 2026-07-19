"""Recon intel-fog: enemy site composition/rings hidden until discovered.

Covers the discovery gate (``known_for``), the omniscient/setting escape hatches,
and the save-migration default. The end-to-end reveal trigger (a strike flips a
site to discovered) is asserted in ``test_bda_tarps_reveal.py`` where the
mission-results fixtures already live.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any, cast

from dcs.mapping import Point

from game.theater import Player
from game.theater.controlpoint import OffMapSpawn
from game.theater.presetlocation import PresetLocation
from game.theater.theatergroundobject import SamGroundObject
from game.utils import Heading


class _EnemySam(SamGroundObject):
    def is_friendly(self, to_player: Player) -> bool:
        return False


def _enemy_sam(*, fog: bool = True) -> SamGroundObject:
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
    tgo = _EnemySam(
        name="Enemy SAM",
        location=location,
        control_point=control_point,
        task=None,
    )
    # known_for() reaches control_point.coalition.game.settings.recon_intel_fog.
    tgo.control_point = cast(
        Any,
        SimpleNamespace(
            coalition=SimpleNamespace(
                game=SimpleNamespace(settings=SimpleNamespace(recon_intel_fog=fog))
            )
        ),
    )
    return tgo


def test_enemy_site_unknown_until_discovered() -> None:
    tgo = _enemy_sam()
    # New enemy sites start unknown to the player...
    assert tgo.discovered_by_player is False
    assert tgo.known_for(Player.BLUE) is False
    # ...but the omniscient view (AI planner / threat math) always sees truth.
    assert tgo.known_for(None) is True
    # Once discovered (attacked/scouted/destroyed), it is known and stays known.
    tgo.discovered_by_player = True
    assert tgo.known_for(Player.BLUE) is True


def test_setting_off_reveals_everything() -> None:
    tgo = _enemy_sam(fog=False)
    assert tgo.discovered_by_player is False
    # With the master toggle off, nothing is fogged even when undiscovered.
    assert tgo.known_for(Player.BLUE) is True


def test_setting_defaults_on() -> None:
    from game.settings import Settings

    assert Settings().recon_intel_fog is True


def test_old_saves_migrate_to_discovered() -> None:
    tgo = _enemy_sam()
    state = dict(tgo.__dict__)
    state.pop("discovered_by_player", None)  # simulate a pre-feature save
    state.pop("_threat_poly", None)
    tgo.__setstate__(state)
    # An in-progress campaign keeps everything visible rather than blanking.
    assert tgo.discovered_by_player is True
