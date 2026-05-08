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


def test_set_allocated_laser_code_marks_member_as_owner(
    member: FlightMember, registry: _RecordingRegistry
) -> None:
    code = LaserCode(1647, registry)
    member.set_allocated_laser_code(code)
    assert member.laser_code is code
    assert member._owns_laser_code is True


def test_set_shared_laser_code_does_not_mark_owner(
    member: FlightMember, registry: _RecordingRegistry
) -> None:
    jtac_code = LaserCode(1511, registry)
    member.set_shared_laser_code(jtac_code)
    assert member.laser_code is jtac_code
    assert member._owns_laser_code is False


def test_set_shared_laser_code_accepts_none(
    member: FlightMember, registry: _RecordingRegistry
) -> None:
    member.set_shared_laser_code(None)
    assert member.laser_code is None
    assert member._owns_laser_code is False


def test_replacing_an_owned_code_releases_it(
    member: FlightMember, registry: _RecordingRegistry
) -> None:
    first = LaserCode(1647, registry)
    second = LaserCode(1648, registry)
    member.set_allocated_laser_code(first)
    member.set_allocated_laser_code(second)
    assert registry.released == [1647]
    assert member.laser_code is second
    assert member._owns_laser_code is True


def test_replacing_an_owned_code_with_shared_releases_owned_only(
    member: FlightMember, registry: _RecordingRegistry
) -> None:
    owned = LaserCode(1647, registry)
    jtac_code = LaserCode(1511, registry)
    member.set_allocated_laser_code(owned)
    member.set_shared_laser_code(jtac_code)
    assert registry.released == [1647]
    assert member.laser_code is jtac_code
    assert member._owns_laser_code is False


def test_replacing_a_shared_code_does_not_release_it(
    member: FlightMember, registry: _RecordingRegistry
) -> None:
    jtac_code = LaserCode(1511, registry)
    other_jtac = LaserCode(1512, registry)
    member.set_shared_laser_code(jtac_code)
    member.set_shared_laser_code(other_jtac)
    assert registry.released == []
    assert member.laser_code is other_jtac
    assert member._owns_laser_code is False


def test_set_shared_laser_code_none_releases_owned(
    member: FlightMember, registry: _RecordingRegistry
) -> None:
    owned = LaserCode(1647, registry)
    member.set_allocated_laser_code(owned)
    member.set_shared_laser_code(None)
    assert registry.released == [1647]
    assert member.laser_code is None
    assert member._owns_laser_code is False
