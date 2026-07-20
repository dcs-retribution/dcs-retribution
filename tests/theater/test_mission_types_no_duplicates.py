from typing import Any
from unittest.mock import MagicMock

import pytest

# Importing these registers every concrete MissionTarget subclass (control
# points, theater ground objects, transfers, front lines) so the
# parametrization below discovers them all.
import game.theater.controlpoint  # noqa: F401
import game.theater.theatergroundobject  # noqa: F401
from game.theater.missiontarget import MissionTarget


def _concrete_mission_targets() -> list[type[MissionTarget]]:
    found: set[type[MissionTarget]] = set()

    def walk(cls: type[MissionTarget]) -> None:
        for sub in cls.__subclasses__():
            walk(sub)
            if not getattr(sub, "__abstractmethods__", frozenset()):
                found.add(sub)

    walk(MissionTarget)
    return sorted(found, key=lambda c: c.__name__)


@pytest.mark.parametrize("cls", _concrete_mission_targets())
@pytest.mark.parametrize("friendly", [True, False])
def test_mission_types_have_no_duplicates(
    cls: "type[MissionTarget]", friendly: bool
) -> None:
    """No mission target may offer the same FlightType twice.

    mission_types() chains a subclass's own entries with the base mission
    types; listing one the base already provides (as happened with
    SEAD_ESCORT on carriers) produces a duplicate in the "Create flight" task
    menu. Covers every concrete mission target, for either coalition.
    """
    # Built without running __init__ (it needs a full game); typed as Any so
    # the mocks can stand in for the real, strongly-typed attributes. Only
    # mission_types() and the two collaborators it consults are exercised.
    target: Any = object.__new__(cls)
    target.is_friendly = MagicMock(return_value=friendly)
    target.total_aircraft_parking = MagicMock(return_value=1)

    types = list(target.mission_types(MagicMock()))

    assert len(types) == len(set(types)), f"{cls.__name__}: duplicates in {types}"
