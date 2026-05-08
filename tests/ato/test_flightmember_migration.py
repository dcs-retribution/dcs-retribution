from __future__ import annotations

import pickle
from typing import Any

import pytest

from game.ato.flightmember import FlightMember
from game.ato.loadouts import Loadout
from game.lasercodes.ilasercoderegistry import ILaserCodeRegistry
from game.lasercodes.lasercode import LaserCode


class _TrackingRegistry(ILaserCodeRegistry):
    """Test registry: alloc_laser_code is unused, release_code records calls."""

    def __init__(self) -> None:
        self.allocated: set[int] = set()
        self.released: list[int] = []

    def alloc_laser_code(self) -> LaserCode:
        raise NotImplementedError

    def release_code(self, code: LaserCode) -> None:
        self.allocated.discard(code.code)
        self.released.append(code.code)

    def reserve(self, value: int) -> LaserCode:
        """Test helper: produce a LaserCode bound to this registry."""
        self.allocated.add(value)
        return LaserCode(value, self)


def _legacy_state(
    *,
    tgp: LaserCode | None,
    weapon: LaserCode | None,
    include_weapon_key: bool = True,
    include_tgp_key: bool = True,
) -> dict[str, Any]:
    """Build a state dict that matches a legacy save shape (pre-collapse fields)."""
    member = FlightMember(pilot=None, loadout=Loadout.empty_loadout())
    state = member.__dict__.copy()
    # Drop the new fields so the state looks pre-collapse.
    state.pop("laser_code", None)
    state.pop("_owns_laser_code", None)
    if include_tgp_key:
        state["tgp_laser_code"] = tgp
    else:
        state.pop("tgp_laser_code", None)
    if include_weapon_key:
        state["weapon_laser_code"] = weapon
    else:
        state.pop("weapon_laser_code", None)
    return state


def _legacy_member(
    *,
    tgp: LaserCode | None,
    weapon: LaserCode | None,
    include_weapon_key: bool = True,
    include_tgp_key: bool = True,
) -> bytes:
    """Build a pickled FlightMember whose state dict matches a legacy save shape."""
    state = _legacy_state(
        tgp=tgp,
        weapon=weapon,
        include_weapon_key=include_weapon_key,
        include_tgp_key=include_tgp_key,
    )
    return pickle.dumps((FlightMember, state))


def _load_legacy(payload: bytes) -> FlightMember:
    cls, state = pickle.loads(payload)
    member = cls.__new__(cls)
    member.__setstate__(state)
    return member


def _load_legacy_state(state: dict[str, Any]) -> FlightMember:
    """Load a FlightMember from a raw state dict without pickle round-trip.

    This preserves Python object identity (e.g. registry references) for
    tests that need to inspect side-effects on the original registry.
    """
    member = FlightMember.__new__(FlightMember)
    member.__setstate__(state)
    return member


def test_new_format_save_clears_legacy_none_fields() -> None:
    """A save written by Tasks 1-7 code carries tgp_laser_code and
    weapon_laser_code = None alongside the new laser_code key.  The migration
    must recognise the state as new-format (via the laser_code key) and pop
    the legacy None-valued keys without touching the new fields.

    Task 8 removed the legacy fields from the constructor, so we inject them
    into the state dict manually to simulate a Tasks-1-7 intermediate save.
    """
    member = FlightMember(pilot=None, loadout=Loadout.empty_loadout())
    state = member.__dict__.copy()
    # Simulate a Tasks-1-7 save that has both legacy keys set to None
    # alongside the new laser_code key.
    state["tgp_laser_code"] = None
    state["weapon_laser_code"] = None
    reborn = FlightMember.__new__(FlightMember)
    reborn.__setstate__(state)
    assert reborn.laser_code is None
    assert reborn._owns_laser_code is False
    assert "tgp_laser_code" not in reborn.__dict__
    assert "weapon_laser_code" not in reborn.__dict__


def test_legacy_save_with_only_tgp_set_promotes_to_owned() -> None:
    registry = _TrackingRegistry()
    tgp = registry.reserve(1647)
    state = _legacy_state(tgp=tgp, weapon=None, include_weapon_key=False)
    reborn = _load_legacy_state(state)
    assert reborn.laser_code is not None
    assert reborn.laser_code.code == 1647
    assert reborn._owns_laser_code is True
    # tgp must NOT have been released; the new owner is the migrated member.
    assert registry.released == []
    assert "tgp_laser_code" not in reborn.__dict__


def test_legacy_save_with_neither_field_present_is_default() -> None:
    payload = _legacy_member(
        tgp=None, weapon=None, include_tgp_key=False, include_weapon_key=False
    )
    reborn = _load_legacy(payload)
    assert reborn.laser_code is None
    assert reborn._owns_laser_code is False


def test_legacy_use_own_code_keeps_ownership_no_release() -> None:
    registry = _TrackingRegistry()
    code = registry.reserve(1647)
    # Same LaserCode value in both fields means the user picked "Use own code".
    state = _legacy_state(tgp=code, weapon=code)
    reborn = _load_legacy_state(state)
    assert reborn.laser_code is not None
    assert reborn.laser_code.code == 1647
    assert reborn._owns_laser_code is True
    assert registry.released == []


def test_legacy_jtac_weapon_releases_orphan_tgp() -> None:
    registry = _TrackingRegistry()
    tgp = registry.reserve(1647)
    jtac = registry.reserve(1511)
    state = _legacy_state(tgp=tgp, weapon=jtac)
    reborn = _load_legacy_state(state)
    assert reborn.laser_code is not None
    assert reborn.laser_code.code == 1511
    assert reborn._owns_laser_code is False
    # The orphan TGP reservation goes back to the pool; the JTAC code stays.
    assert registry.released == [1647]
    assert 1511 in registry.allocated


def test_legacy_default_weapon_releases_orphan_tgp() -> None:
    registry = _TrackingRegistry()
    tgp = registry.reserve(1647)
    state = _legacy_state(tgp=tgp, weapon=None)
    reborn = _load_legacy_state(state)
    assert reborn.laser_code is None
    assert reborn._owns_laser_code is False
    assert registry.released == [1647]


def test_migrated_state_round_trips_without_legacy_keys() -> None:
    registry = _TrackingRegistry()
    code = registry.reserve(1647)
    once = _load_legacy(_legacy_member(tgp=code, weapon=code))
    redumped = pickle.dumps(once)
    twice = pickle.loads(redumped)
    assert twice.laser_code is not None
    assert twice.laser_code.code == 1647
    assert twice._owns_laser_code is True
    assert "tgp_laser_code" not in twice.__dict__
    assert "weapon_laser_code" not in twice.__dict__
    # No spurious release on the second load.
    assert registry.released == []


def test_setstate_is_idempotent_on_already_migrated_state() -> None:
    registry = _TrackingRegistry()
    code = registry.reserve(1647)
    # Use _load_legacy_state (not _load_legacy) so the LaserCode inside `once`
    # still references this registry — not a pickle-cloned copy of it.
    once = _load_legacy_state(_legacy_state(tgp=code, weapon=code))
    state = once.__dict__.copy()
    twice = FlightMember.__new__(FlightMember)
    twice.__setstate__(state)
    assert twice.laser_code is not None
    assert twice.laser_code.code == 1647
    assert twice._owns_laser_code is True
    assert registry.released == []
