"""Tests for ``Game.neutral_country`` (§23 / upstream #854).

The neutral coalition must never share a DCS country with a belligerent: a country
may live on only one coalition in a ``.miz``, so a collision produces an unloadable
mission (and misfiles neutral statics / breaks capture triggers keyed on neutral
membership). The in-use set spans every squadron's own country (per-squadron
countries), not just the two faction primaries — and when even the last preferred
candidate is claimed, the property must scan the full pydcs country list rather than
hand back a claimed nation.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Iterable

from dcs.countries import (
    CombinedJointTaskForcesBlue,
    Russia,
    Switzerland,
    USA,
    USAFAggressors,
    UnitedNationsPeacekeepers,
)
from dcs.country import Country

from game.game import Game


def _coalition(
    faction_country: Country, squadron_countries: Iterable[Country]
) -> SimpleNamespace:
    squadrons = [SimpleNamespace(country=country) for country in squadron_countries]
    return SimpleNamespace(
        faction=SimpleNamespace(country=faction_country),
        air_wing=SimpleNamespace(iter_squadrons=lambda: iter(squadrons)),
    )


def _neutral_country_for(
    blue_country: Country,
    red_country: Country,
    blue_squadron_countries: Iterable[Country] = (),
    red_squadron_countries: Iterable[Country] = (),
) -> Country:
    # Duck-typed fake: the property reads only the two faction countries and each
    # air wing's squadron countries, so a full Game is unnecessary.
    game = SimpleNamespace(
        blue=_coalition(blue_country, blue_squadron_countries),
        red=_coalition(red_country, red_squadron_countries),
    )
    return Game.neutral_country.fget(game)  # type: ignore[attr-defined]


def test_prefers_un_peacekeepers_when_unclaimed() -> None:
    neutral = _neutral_country_for(USA(), Russia())
    assert neutral.id == UnitedNationsPeacekeepers.id


def test_squadron_countries_exclude_preferred_candidates() -> None:
    # A blue CJTF fielding a UN squadron claims that nation for blue, so the
    # neutral coalition falls through to the next preferred candidate.
    neutral = _neutral_country_for(
        CombinedJointTaskForcesBlue(),
        Russia(),
        blue_squadron_countries=[UnitedNationsPeacekeepers()],
    )
    assert neutral.id == Switzerland.id


def test_all_preferred_candidates_claimed_scans_for_an_unclaimed_nation() -> None:
    # The Druss case: USAF Aggressors as the red faction and a blue CJTF fielding
    # UN and Swiss squadrons claims all three preferred neutrals. The old final
    # fallback returned USAFAggressors() anyway — one country on two coalitions,
    # an unloadable .miz. The scan must return a nation nobody claimed.
    claimed = {
        CombinedJointTaskForcesBlue.id,
        USAFAggressors.id,
        UnitedNationsPeacekeepers.id,
        Switzerland.id,
    }
    neutral = _neutral_country_for(
        CombinedJointTaskForcesBlue(),
        USAFAggressors(),
        blue_squadron_countries=[UnitedNationsPeacekeepers(), Switzerland()],
    )
    assert neutral.id not in claimed
