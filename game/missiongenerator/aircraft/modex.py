"""Squadron-sequenced board numbers (modex) for Hornets and Tomcats.

pydcs assigns every aircraft's ``onboard_num`` by popping from an *unordered*
set (``Country.next_onboard_num`` -> ``set.pop()``), so board numbers come out
as random three-digit values. Navy jets don't wear random numbers: the air
wing gives each squadron a modex block (100, 200, 300, ...) and numbers the
squadron's jets sequentially inside it -- the first jet X00, the second X01,
the third X02.

:class:`ModexAllocator` pre-assigns one block per Hornet/Tomcat squadron at
construction (per coalition, in air-wing order, Tomcats ahead of Hornets --
the traditional CVW fighter blocks) and re-stamps every generated unit of
those squadrons with the next number in its squadron's sequence, in
generation order: tasked flights first, then the untasked ramp aircraft. The
campaign does not model individual airframes, so numbering is per-mission
(deterministic within a mission, not sticky to a pilot across turns). Every other airframe keeps the stock pydcs number.

A player may pin a Hornet or Tomcat flight's board number on the payload tab
(``Flight.board_number``, the lead's number; wingmen follow in order). Taking
a number another flight has pinned moves that flight to the next free run
(:func:`take_board_number`). Pinned
numbers are claimed per coalition before anything is stamped: the flight wears
them, the squadron sequences skip them, and a random pydcs
number that lands on one is re-rolled, so no other package wears it.
"""

from __future__ import annotations

from typing import Any, Iterable, Optional, TYPE_CHECKING
from uuid import UUID

from dcs.country import Country
from dcs.unitgroup import FlyingGroup

if TYPE_CHECKING:
    from game import Game
    from game.ato import Flight
    from game.squadrons import Squadron

#: DCS unit type ids that wear squadron-sequenced modex numbers.
MODEX_AIRCRAFT_IDS: frozenset[str] = frozenset(
    {
        # Hornets (player module + AI variants).
        "FA-18C_hornet",
        "F/A-18A",
        "F/A-18C",
        # Tomcats (Heatblur player variants + the AI F-14A). No F-14 livery
        # declares a board-number material, so DCS never paints these on the
        # airframe -- the Tomcat's visible modex is its livery, sequenced by
        # liveryallocator.py instead.
        "F-14A",
        "F-14A-135-GR",
        "F-14A-135-GR-Early",
        "F-14A-95-GR",
        "F-14B",
        "F-14BU",
    }
)

#: Blocks run 100, 200, ... 900 and wrap after nine squadrons -- a coalition
#: fielding a tenth Hornet/Tomcat squadron reuses blocks rather than growing a
#: fourth digit (DCS board numbers are three digits).
_FIRST_BLOCK = 100
_MAX_BLOCKS = 9
#: One squadron's numbers span X00-X99.
_BLOCK_SIZE = 100
#: DCS board numbers are three digits.
MIN_BOARD_NUMBER = 1
MAX_BOARD_NUMBER = 999


def is_modex_flight(flight: Flight) -> bool:
    """Navy only: the Hornet and Tomcat flights that wear sequenced modexes."""
    return flight.squadron.aircraft.dcs_unit_type.id in MODEX_AIRCRAFT_IDS


def pinned_board_numbers(flight: Flight) -> list[int]:
    """The numbers a flight's pinned board number covers, lead first."""
    lead = getattr(flight, "board_number", None)
    if lead is None or not is_modex_flight(flight):
        return []
    return [lead + offset for offset in range(flight.count)]


def max_board_number_lead(count: int) -> int:
    """The highest lead number whose run of ``count`` still fits in three digits."""
    return MAX_BOARD_NUMBER - max(count, 1) + 1


def _next_free_lead(count: int, near: int, taken: set[int]) -> Optional[int]:
    """The first free run of ``count`` at or above ``near``, else the nearest below.

    Upward first keeps a moved flight inside its own hundred block.
    """
    top = max_board_number_lead(count)
    upward = range(max(near, MIN_BOARD_NUMBER), top + 1)
    downward = range(min(near, top + 1) - 1, MIN_BOARD_NUMBER - 1, -1)
    for lead in (*upward, *downward):
        if taken.isdisjoint(range(lead, lead + count)):
            return lead
    return None


def take_board_number(
    flight: Flight, lead: int, others: Iterable[Flight]
) -> list[tuple[Flight, int, Optional[int]]]:
    """Pin ``lead`` on ``flight``; any pinned flight it overlaps moves aside.

    A displaced flight keeps a pin, moved to the next free run above its old
    one, so no third flight is disturbed. ``others`` is the coalition's ATO. Returns
    each move as (flight, old lead, new lead); None means no run was free.
    """
    lead = max(MIN_BOARD_NUMBER, min(lead, max_board_number_lead(flight.count)))
    flight.board_number = lead
    others = [other for other in others if other is not flight]
    run = set(range(lead, lead + flight.count))
    displaced = [o for o in others if run.intersection(pinned_board_numbers(o))]
    moving = {id(o) for o in displaced}
    taken = run.union(*(pinned_board_numbers(o) for o in others if id(o) not in moving))
    moves: list[tuple[Flight, int, Optional[int]]] = []
    for other in displaced:
        old = other.board_number
        assert old is not None
        new = _next_free_lead(other.count, old, taken)
        other.board_number = new
        taken.update(pinned_board_numbers(other))
        moves.append((other, old, new))
    return moves


def _tomcats_first(squadron: Squadron) -> int:
    """Sort key: F-14 squadrons take the 100/200 fighter blocks like a real CVW."""
    return 0 if squadron.aircraft.dcs_unit_type.id.startswith("F-14") else 1


class ModexAllocator:
    """Deterministic per-squadron modex blocks + a per-squadron jet sequence."""

    def __init__(self, game: Game) -> None:
        self._blocks: dict[UUID, int] = {}
        self._next_index: dict[UUID, int] = {}
        self._reserved: set[UUID] = set()
        #: Pinned numbers per coalition, and each pinned flight's numbers by
        #: member (None where the member lost a clash and falls back to auto).
        self._claims: dict[int, set[int]] = {}
        self._pinned: dict[int, list[Optional[int]]] = {}
        self._squadron_coalition: dict[UUID, int] = {}
        self._claims_reserved: set[int] = set()
        for coalition in game.coalitions:
            self._claim_pinned_numbers(coalition)
            squadrons = []
            for squadron in coalition.air_wing.iter_squadrons():
                self._squadron_coalition[squadron.id] = id(coalition)
                if squadron.aircraft.dcs_unit_type.id in MODEX_AIRCRAFT_IDS:
                    squadrons.append(squadron)
            # Stable sort: Tomcats first, air-wing order preserved within a
            # type -- so a squadron keeps the same block mission after mission.
            squadrons.sort(key=_tomcats_first)
            for index, squadron in enumerate(squadrons):
                self._blocks[squadron.id] = (
                    _FIRST_BLOCK + (index % _MAX_BLOCKS) * _BLOCK_SIZE
                )

    def _claim_pinned_numbers(self, coalition: Any) -> None:
        claims = self._claims.setdefault(id(coalition), set())
        ato = getattr(coalition, "ato", None)
        for package in getattr(ato, "packages", []):
            for flight in package.flights:
                numbers: list[Optional[int]] = []
                for number in pinned_board_numbers(flight):
                    # The payload tab moves clashing pins aside; a flight resized
                    # after pinning can still overlap, and the first claim wins.
                    if number > MAX_BOARD_NUMBER or number in claims:
                        numbers.append(None)
                    else:
                        claims.add(number)
                        numbers.append(number)
                if numbers:
                    self._pinned[id(flight)] = numbers

    def assign(
        self,
        squadron: Squadron,
        group: FlyingGroup[Any],
        country: Country,
        flight: Optional[Flight] = None,
    ) -> None:
        """Stamp the group's units with their board numbers.

        A pinned flight wears its own numbers. Otherwise a Hornet/Tomcat
        squadron takes its next modex numbers, skipping pinned ones, and any
        other airframe keeps its pydcs number unless that number is pinned by
        another flight. The squadron's whole block is reserved with the country
        on first use so pydcs's random allocator can't hand a later
        same-country aircraft a number inside it.
        """
        claims = self._claims.get(self._squadron_coalition.get(squadron.id, -1), set())
        if claims and id(country) not in self._claims_reserved:
            self._claims_reserved.add(id(country))
            for number in claims:
                country.reserve_onboard_num(f"{number:03}")
        pinned = self._pinned.get(id(flight), []) if flight is not None else []
        block = self._blocks.get(squadron.id)
        if block is not None and squadron.id not in self._reserved:
            self._reserved.add(squadron.id)
            for number in range(block, block + _BLOCK_SIZE):
                country.reserve_onboard_num(f"{number:03}")
        for position, unit in enumerate(group.units):
            own = pinned[position] if position < len(pinned) else None
            if own is not None:
                unit.onboard_num = f"{own:03}"
            elif block is not None:
                unit.onboard_num = self._next_in_block(squadron.id, block, claims)
            elif _as_number(unit.onboard_num) in claims:
                unit.onboard_num = country.next_onboard_num()

    def _next_in_block(self, squadron_id: UUID, block: int, claims: set[int]) -> str:
        # More than 100 airframes of one squadron in one mission cannot happen
        # with real squadron sizes; wrap within the block rather than bleed into
        # the next squadron's. A block pinned solid falls back to its own base.
        for _ in range(_BLOCK_SIZE):
            index = self._next_index.get(squadron_id, 0)
            self._next_index[squadron_id] = index + 1
            number = block + index % _BLOCK_SIZE
            if number not in claims:
                return f"{number:03}"
        return f"{block:03}"


def _as_number(onboard_num: str) -> Optional[int]:
    try:
        return int(onboard_num)
    except (TypeError, ValueError):
        return None
