from __future__ import annotations

from game.ato.flightmember import FlightMember
from game.ato.flightmembers import FlightMembers
from game.ato.loadouts import Loadout
from game.lasercodes.ilasercoderegistry import ILaserCodeRegistry
from game.lasercodes.lasercode import LaserCode


class _RecordingRegistry(ILaserCodeRegistry):
    def __init__(self) -> None:
        self.released: list[int] = []

    def alloc_laser_code(self) -> LaserCode:
        raise NotImplementedError

    def release_code(self, code: LaserCode) -> None:
        self.released.append(code.code)


class _StubFlight:
    """Minimal stub matching the shape FlightMembers reads."""

    def __init__(self) -> None:
        # FlightMembers reads self.flight.squadron / self.flight.squadron.aircraft.variant_id
        # only on resize-up, which we do not exercise here.
        self.squadron = None  # never accessed in shrink/clear paths


def _make_members(
    *codes_with_ownership: tuple[LaserCode | None, bool],
) -> FlightMembers:
    flight = _StubFlight()
    members = FlightMembers.__new__(FlightMembers)
    members.flight = flight  # type: ignore[assignment]
    members.members = []
    for code, owns in codes_with_ownership:
        m = FlightMember(pilot=None, loadout=Loadout.empty_loadout())
        if code is None:
            m.set_shared_laser_code(None)
        elif owns:
            m.set_allocated_laser_code(code)
        else:
            m.set_shared_laser_code(code)
        members.members.append(m)
    return members


def test_resize_smaller_releases_owned_codes_only() -> None:
    registry = _RecordingRegistry()
    owned = LaserCode(1647, registry)
    shared = LaserCode(1511, registry)
    # member[0] stays; member[1]=owned and member[2]=shared are removed.
    # Only the owned code should be released.
    members = _make_members((None, False), (owned, True), (shared, False))
    members.resize(1)
    assert registry.released == [1647]
    assert len(members.members) == 1


def test_clear_releases_owned_codes_only() -> None:
    registry = _RecordingRegistry()
    owned = LaserCode(1647, registry)
    shared = LaserCode(1511, registry)
    members = _make_members((owned, True), (shared, False))

    # FlightMembers.clear() also returns pilots; stub squadron.return_pilots().
    class _StubSquadron:
        def return_pilots(self, pilots: list[None]) -> None:
            pass

    members.flight.squadron = _StubSquadron()  # type: ignore[assignment]
    members.clear()
    assert registry.released == [1647]
