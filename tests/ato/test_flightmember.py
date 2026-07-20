from __future__ import annotations

import pytest

from game.ato.flightmember import FlightMember
from game.ato.loadouts import Loadout
from game.lasercodes.ilasercoderegistry import ILaserCodeRegistry
from game.lasercodes.lasercode import LaserCode


class _RecordingRegistry(ILaserCodeRegistry):
    """Test registry that records release() calls but does not allocate."""

    def __init__(self) -> None:
        self.released: list[int] = []

    def alloc_laser_code(self) -> LaserCode:
        raise NotImplementedError

    def release_code(self, code: LaserCode) -> None:
        self.released.append(code.code)


@pytest.fixture(name="registry")
def registry_fixture() -> _RecordingRegistry:
    return _RecordingRegistry()


@pytest.fixture(name="member")
def member_fixture() -> FlightMember:
    # Loadout.empty_loadout() does not require an aircraft; safe for unit tests.
    return FlightMember(pilot=None, loadout=Loadout.empty_loadout())


def test_assign_tgp_laser_code_sets_field(
    member: FlightMember, registry: _RecordingRegistry
) -> None:
    code = LaserCode(1647, registry)
    member.assign_tgp_laser_code(code)
    assert member.tgp_laser_code is code


def test_assign_tgp_laser_code_raises_when_already_assigned(
    member: FlightMember, registry: _RecordingRegistry
) -> None:
    member.assign_tgp_laser_code(LaserCode(1647, registry))
    with pytest.raises(RuntimeError):
        member.assign_tgp_laser_code(LaserCode(1648, registry))


def test_release_tgp_laser_code_releases_and_clears(
    member: FlightMember, registry: _RecordingRegistry
) -> None:
    code = LaserCode(1647, registry)
    member.assign_tgp_laser_code(code)
    member.release_tgp_laser_code()
    assert registry.released == [1647]
    assert member.tgp_laser_code is None


def test_release_tgp_laser_code_raises_when_unassigned(
    member: FlightMember, registry: _RecordingRegistry
) -> None:
    with pytest.raises(RuntimeError):
        member.release_tgp_laser_code()


def test_release_tgp_laser_code_clears_weapon_code_when_shared(
    member: FlightMember, registry: _RecordingRegistry
) -> None:
    # Mirrors the apply_default_player_laser_code path where both fields point at
    # the same allocated code: releasing the TGP code must also drop the weapon
    # reference so the released code is not left dangling on the weapon field.
    code = LaserCode(1647, registry)
    member.assign_tgp_laser_code(code)
    member.weapon_laser_code = code
    member.release_tgp_laser_code()
    assert registry.released == [1647]
    assert member.tgp_laser_code is None
    assert member.weapon_laser_code is None


def test_release_tgp_laser_code_keeps_independent_weapon_code(
    member: FlightMember, registry: _RecordingRegistry
) -> None:
    # A buddy-lase plan: the weapon code is a different (e.g. JTAC) code than the
    # member's own TGP code. Releasing the TGP code must leave the weapon code.
    own = LaserCode(1647, registry)
    weapon = LaserCode(1511, registry)
    member.assign_tgp_laser_code(own)
    member.weapon_laser_code = weapon
    member.release_tgp_laser_code()
    assert registry.released == [1647]
    assert member.tgp_laser_code is None
    assert member.weapon_laser_code is weapon
