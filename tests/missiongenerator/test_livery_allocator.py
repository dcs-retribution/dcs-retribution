"""Board-number-driven livery choice (see liveryallocator.py).

The Tomcat's visible board number is its livery. A jet wears the livery painted
with its own number when the set has one; the CAG / hi-vis livery goes to the
X00 jet and to no other; every other jet cycles the line liveries.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any
from uuid import uuid4

import pytest

from game.missiongenerator.aircraft.liveryallocator import (
    LiveryAllocator,
    is_cag_livery,
    livery_modex,
)
from game.squadrons.squadron import Squadron

VF103 = [
    "VF-103 2004 AA100 BuNo 162918",
    "VF-103 2004 AA101 BuNo 162705",
    "VF-103 2004 AA103 BuNo 163217",
    "VF-103 2004 AA105 BuNo 163229",
]
VF143 = ["VF-143 2004 AG100 BuNo 163220", "VF-143 2004 AG106 BuNo 161434"]


def _squadron(*liveries: str, pool: list[str] | None = None) -> Any:
    squadron = SimpleNamespace(
        id=uuid4(),
        livery_set=list(liveries),
        _livery_pool=list(pool or []),
    )
    squadron.ordered_livery_set = list(squadron.livery_set) + list(
        squadron._livery_pool
    )
    return squadron


def _for_numbers(squadron: Any, numbers: list[int | None]) -> list[str | None]:
    allocator = LiveryAllocator()
    return [allocator.next_livery(squadron, number) for number in numbers]


def _modexes(liveries: list[str | None]) -> list[int | None]:
    return [None if l is None else livery_modex(l) for l in liveries]


@pytest.mark.parametrize(
    "livery,number,cag",
    [
        ("VF-103 2004 AA100 BuNo 162918", 100, True),
        ("VF-11 2004 AG201 BuNo 162912", 201, False),
        ("VF-32 Fighting Swordsmen 100 (2000)", 100, True),
        ("VF-143 Pukin Dogs CAG", None, True),
        ("VFA-83 High Vis", None, True),
        ("VFA-83 Low Vis", None, False),
    ],
)
def test_livery_reading(livery: str, number: int | None, cag: bool) -> None:
    assert livery_modex(livery) == number
    assert is_cag_livery(livery) is cag


def test_a_jet_wears_the_livery_painted_with_its_number() -> None:
    worn = _for_numbers(_squadron(*VF103), [100, 101, 102, 103, 104, 105])

    # 102 and 104 have no livery of their own: they take line jets in turn.
    assert _modexes(worn) == [100, 101, 101, 103, 103, 105]


def test_the_cag_bird_never_flies_on_a_line_jet() -> None:
    """VF-143 ships one CAG bird and one line jet: the line jets share AG106."""
    worn = _for_numbers(_squadron(*VF143), [100, 101, 102, 103, 104])

    assert _modexes(worn) == [100, 106, 106, 106, 106]


def test_the_x00_jet_takes_a_cag_livery_with_no_number() -> None:
    squadron = _squadron("VF-143 Pukin Dogs CAG", "VF-143 Pukin Dogs Line")

    assert _for_numbers(squadron, [200, 201]) == [
        "VF-143 Pukin Dogs CAG",
        "VF-143 Pukin Dogs Line",
    ]


def test_a_pinned_run_wears_its_own_numbers() -> None:
    worn = _for_numbers(_squadron(*VF103), [103, 104, 105])

    assert _modexes(worn) == [103, 101, 105]


def test_without_a_number_the_first_jet_stands_in_for_x00() -> None:
    worn = _for_numbers(_squadron(*VF103), [None, None, None, None, None])

    assert _modexes(worn) == [100, 101, 103, 105, 101]


def test_a_set_of_only_cag_liveries_leaves_line_jets_to_the_fallback() -> None:
    squadron = _squadron("VF-143 2004 AG100 BuNo 163220")

    assert _for_numbers(squadron, [100, 101]) == [
        "VF-143 2004 AG100 BuNo 163220",
        None,
    ]


def test_a_set_with_no_cag_livery_cycles_it_whole() -> None:
    squadron = _squadron(
        "VF-101 2004 AD101 BuNo 162920", "VF-101 2004 AD107 BuNo 162910"
    )

    assert _modexes(_for_numbers(squadron, [100, 102, 103])) == [101, 107, 101]


def test_sequence_is_per_squadron() -> None:
    allocator = LiveryAllocator()
    first = _squadron("A Line 1", "A Line 2")
    second = _squadron("B Line 1", "B Line 2")

    assert allocator.next_livery(first) == "A Line 1"
    assert allocator.next_livery(second) == "B Line 1"
    assert allocator.next_livery(first) == "A Line 2"


def test_squadron_without_a_livery_set_is_left_alone() -> None:
    assert LiveryAllocator().next_livery(_squadron()) is None


def test_ordered_livery_set_rejoins_a_drained_pool() -> None:
    """The property the allocator reads, exercised on the real Squadron."""
    squadron = SimpleNamespace(livery_set=["AA105"], _livery_pool=["AA100", "AA101"])

    assert Squadron.ordered_livery_set.fget(squadron) == [  # type: ignore[attr-defined]
        "AA105",
        "AA100",
        "AA101",
    ]


@pytest.mark.parametrize(
    "dcs_id,uses_allocator", [("F-14BU", True), ("F-15ESE", False)]
)
def test_only_navy_squadrons_use_the_allocator(
    dcs_id: str, uses_allocator: bool
) -> None:
    """Every other squadron keeps the random round-robin."""
    from game.missiongenerator.aircraft.aircraftpainter import AircraftPainter

    squadron = _squadron(*VF143)
    squadron.use_livery_set = True
    squadron.random_round_robin_livery_from_set = lambda: "round-robin"
    flight = SimpleNamespace(
        squadron=squadron,
        unit_type=SimpleNamespace(dcs_unit_type=SimpleNamespace(id=dcs_id)),
    )
    painter = AircraftPainter(flight, SimpleNamespace(units=[]), LiveryAllocator())  # type: ignore[arg-type]

    livery = painter.livery_from_squadron_set(True, 100)

    assert (livery != "round-robin") is uses_allocator
