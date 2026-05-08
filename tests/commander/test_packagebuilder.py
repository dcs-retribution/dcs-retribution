from __future__ import annotations

from unittest.mock import MagicMock

from game.ato.flightmember import (
    FlightMember,
    apply_default_player_laser_code,
)
from game.ato.loadouts import Loadout
from game.lasercodes.lasercoderegistry import LaserCodeRegistry
from game.settings.settings import (
    DefaultPlayerLaserCode,
    Settings,
)


def _player_member() -> FlightMember:
    member = FlightMember(pilot=None, loadout=Loadout.empty_loadout())
    pilot = MagicMock()
    pilot.player = True
    member.pilot = pilot
    return member


def _ai_member() -> FlightMember:
    member = FlightMember(pilot=None, loadout=Loadout.empty_loadout())
    pilot = MagicMock()
    pilot.player = False
    member.pilot = pilot
    return member


def test_apply_allocate_own_assigns_an_allocated_code() -> None:
    settings = Settings()
    settings.default_player_laser_code = DefaultPlayerLaserCode.ALLOCATE_OWN
    registry = LaserCodeRegistry()
    member = _player_member()
    apply_default_player_laser_code(member, settings, registry)
    assert member.laser_code is not None
    assert member.owns_laser_code is True


def test_apply_default_1688_leaves_laser_code_none() -> None:
    settings = Settings()
    settings.default_player_laser_code = DefaultPlayerLaserCode.DEFAULT_1688
    registry = LaserCodeRegistry()
    member = _player_member()
    apply_default_player_laser_code(member, settings, registry)
    assert member.laser_code is None
    assert member.owns_laser_code is False


def test_apply_does_nothing_for_ai_members() -> None:
    settings = Settings()
    settings.default_player_laser_code = DefaultPlayerLaserCode.ALLOCATE_OWN
    registry = LaserCodeRegistry()
    member = _ai_member()
    apply_default_player_laser_code(member, settings, registry)
    assert member.laser_code is None
    assert member.owns_laser_code is False


def test_settings_default_is_allocate_own() -> None:
    settings = Settings()
    assert settings.default_player_laser_code is DefaultPlayerLaserCode.ALLOCATE_OWN
