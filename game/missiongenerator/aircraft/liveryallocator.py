"""Board-number-driven livery choice for squadrons with a livery set.

No F-14 livery declares a board-number material, so DCS never paints the
mission's ``onboard_num`` on a Tomcat -- the visible modex is whatever the
livery texture carries. (Every airframe that does show one -- Su-27, MiG-29A,
F-15C, Su-25, FA-18C -- names the material in its livery description.lua; no
stock F-14 livery does, and Heatblur ships four VF-32 skins differing only in
the painted number.) On the Tomcat the livery IS the
board number, which makes the ORDER liveries are handed out the modex order.

:class:`LiveryAllocator` picks each jet's livery from its board number: a
livery painted with that number if the set has one, the squadron's CAG / hi-vis
livery for the X00 jet, and otherwise the line liveries in turn. A CAG / hi-vis
livery (an X00 number, or "CAG" / "Hi Vis" in the name) is never worn by any
jet but the X00. Without a meaningful number (a random
pydcs one) the squadron's first jet of the mission stands in for X00.

Replaces ``Squadron.random_round_robin_livery_from_set`` for mission
generation, which picked at random and so could put two CAG birds in one
squadron.
"""

from __future__ import annotations

import re
from typing import Optional, TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    from game.squadrons import Squadron

#: A three-digit modex inside a livery name: "AA100", "Swordsmen 101". Four-digit
#: years, six-digit BuNos and the squadron designator ("VF-103") do not match.
_MODEX_IN_NAME = re.compile(r"(?<![\d-])(\d{3})(?!\d)")
_HIGH_VIS_NAME = re.compile(r"\bcag\b|\bhi(gh)?[- ]?vis", re.IGNORECASE)


def livery_modex(livery: str) -> Optional[int]:
    """The board number painted on a livery, when its name carries one."""
    match = _MODEX_IN_NAME.search(livery)
    return int(match.group(1)) if match else None


def is_cag_livery(livery: str) -> bool:
    """A CAG / hi-vis livery, which only the X00 jet may wear."""
    number = livery_modex(livery)
    if number is not None and number % 100 == 0:
        return True
    return _HIGH_VIS_NAME.search(livery) is not None


class LiveryAllocator:
    """Board-number-driven livery choice, per squadron, per mission."""

    def __init__(self) -> None:
        self._next_line: dict[UUID, int] = {}
        self._seen: set[UUID] = set()

    def next_livery(
        self, squadron: Squadron, board_number: Optional[int] = None
    ) -> Optional[str]:
        """The livery for the squadron's next jet, or None to fall back.

        ``board_number`` is the jet's modex when it is meaningful (sequenced or
        pinned); None for a random pydcs number.
        """
        liveries = squadron.ordered_livery_set
        if not liveries:
            return None
        first_jet = squadron.id not in self._seen
        self._seen.add(squadron.id)
        if board_number is not None:
            for livery in liveries:
                if livery_modex(livery) == board_number:
                    return livery
        cag = [livery for livery in liveries if is_cag_livery(livery)]
        is_x00 = board_number % 100 == 0 if board_number is not None else first_jet
        if is_x00 and cag:
            return cag[0]
        line = [livery for livery in liveries if not is_cag_livery(livery)]
        if not line:
            # Only CAG liveries in the set: a line jet takes the squadron's
            # plain livery instead.
            return None
        index = self._next_line.get(squadron.id, 0)
        self._next_line[squadron.id] = index + 1
        return line[index % len(line)]
