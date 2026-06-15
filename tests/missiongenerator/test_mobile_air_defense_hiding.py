"""Mobile point air-defense units are hidden on the MFD even when they ride
inside a non-air-defense group.

``hidden_on_mfd`` is a group-level DCS property, so a SHORAD/AAA/MANPAD escort
generated inside an armor or missile group (whose own hide_on_mfd flag is not
set) used to inherit the parent's visible flag and betray itself on the
datalink. The group generators now also hide a group when it *contains* a
mobile air-defense unit.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any, Optional, cast

from game.data.units import UnitClass
from game.missiongenerator.tgogenerator import GroundObjectGenerator
from game.theater.theatergroup import TheaterUnit


def _unit(unit_class: Optional[UnitClass]) -> TheaterUnit:
    """A fake TheaterUnit whose ``unit_type`` exposes ``unit_class`` (or None for
    a unit with no resolvable type, e.g. a static)."""
    unit_type = None if unit_class is None else SimpleNamespace(unit_class=unit_class)
    return cast(TheaterUnit, SimpleNamespace(unit_type=unit_type))


def _contains(*classes: Optional[UnitClass]) -> bool:
    return GroundObjectGenerator._contains_mobile_air_defense(
        [_unit(c) for c in classes]
    )


def test_shorad_escort_inside_armor_is_detected() -> None:
    assert _contains(UnitClass.TANK, UnitClass.IFV, UnitClass.SHORAD)


def test_aaa_and_manpad_are_detected() -> None:
    assert _contains(UnitClass.AAA)
    assert _contains(UnitClass.MANPAD)


def test_pure_armor_group_is_not_hidden() -> None:
    assert not _contains(UnitClass.TANK, UnitClass.IFV, UnitClass.APC)


def test_standalone_merad_telar_site_stays_visible() -> None:
    # SA-6/11 style mobile SAM sites are TELAR-class and deliberately left
    # targetable for SEAD.
    assert not _contains(UnitClass.TELAR, UnitClass.TRACK_RADAR)


def test_units_without_a_resolvable_type_are_ignored() -> None:
    assert not _contains(None)
    assert _contains(None, UnitClass.SHORAD)


def test_empty_group_is_not_hidden() -> None:
    assert not GroundObjectGenerator._contains_mobile_air_defense([])
