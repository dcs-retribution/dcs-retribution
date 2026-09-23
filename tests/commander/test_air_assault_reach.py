from __future__ import annotations

from unittest.mock import MagicMock

from game.commander.objectivefinder import AIR_ASSAULT_MAX_REACH, ObjectiveFinder
from game.utils import nautical_miles


def _finder_with(*distances_nm: float) -> tuple[ObjectiveFinder, MagicMock]:
    """A finder with one friendly CP per distance, and a target at those ranges."""
    finder = ObjectiveFinder.__new__(ObjectiveFinder)
    friendly = [MagicMock() for _ in distances_nm]
    finder.friendly_control_points = lambda: iter(friendly)  # type: ignore[method-assign]
    lookup = {cp: nautical_miles(nm).meters for cp, nm in zip(friendly, distances_nm)}
    target = MagicMock()
    target.distance_to.side_effect = lambda other: lookup[other]
    return finder, target


def test_objective_inside_the_cap_is_kept() -> None:
    # FOB Nawa's real geometry: 68 NM from the nearest friendly base.
    finder, target = _finder_with(68, 240)

    assert finder._within_air_assault_reach(target)


def test_objective_beyond_the_cap_is_dropped() -> None:
    # Kandahar sat 177 NM behind the nearest friendly base, and C-130s were
    # fragged against it from Bagram, 269 NM away.
    finder, target = _finder_with(177, 300)

    assert not finder._within_air_assault_reach(target)


def test_reach_is_measured_to_the_nearest_base_not_the_farthest() -> None:
    finder, target = _finder_with(300, 25)

    assert finder._within_air_assault_reach(target)


def test_no_friendly_bases_means_no_air_assault() -> None:
    finder = ObjectiveFinder.__new__(ObjectiveFinder)
    finder.friendly_control_points = lambda: iter([])  # type: ignore[method-assign]

    assert not finder._within_air_assault_reach(MagicMock())


def test_cap_is_100_nm() -> None:
    assert AIR_ASSAULT_MAX_REACH.nautical_miles == 100
