"""Per-squadron DCS country resolution (issue #627).

``CountryAssigner`` spawns each squadron's units under its own ``squadron.country``
so mixed-nation (CJTF) sides get nation-specific voiceovers/comms, while applying
the DCS constraint that a country may belong to only one coalition. For non-CJTF
factions (every squadron already restricted to the faction country) it must be a
no-op.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any, Iterable, cast

from dcs.countries import (
    CombinedJointTaskForcesBlue,
    CombinedJointTaskForcesRed,
    Greece,
    USA,
)

from game.game import Game
from game.missiongenerator.countryassigner import CountryAssigner
from game.theater.player import Player

USA_ID = USA.id
GREECE_ID = Greece.id
CJTF_BLUE_ID = CombinedJointTaskForcesBlue.id
CJTF_RED_ID = CombinedJointTaskForcesRed.id


def _squadron(country_id: int, player: Player) -> Any:
    return SimpleNamespace(
        country=SimpleNamespace(id=country_id),
        coalition=SimpleNamespace(player=player),
    )


def _game(
    blue_faction_id: int,
    red_faction_id: int,
    blue_squadrons: Iterable[Any],
    red_squadrons: Iterable[Any],
) -> Game:
    blue_list = list(blue_squadrons)
    red_list = list(red_squadrons)
    blue = SimpleNamespace(
        faction=SimpleNamespace(country=SimpleNamespace(id=blue_faction_id)),
        air_wing=SimpleNamespace(iter_squadrons=lambda: list(blue_list)),
    )
    red = SimpleNamespace(
        faction=SimpleNamespace(country=SimpleNamespace(id=red_faction_id)),
        air_wing=SimpleNamespace(iter_squadrons=lambda: list(red_list)),
    )
    return cast(Game, SimpleNamespace(blue=blue, red=red))


def test_single_nation_side_is_a_no_op() -> None:
    # A non-CJTF faction restricts every squadron to the faction country, so the
    # resolved country must equal the faction country and only one country is
    # registered on the coalition.
    blue_sqns = [_squadron(USA_ID, Player.BLUE), _squadron(USA_ID, Player.BLUE)]
    assigner = CountryAssigner(_game(USA_ID, CJTF_RED_ID, blue_sqns, []))

    assert [c.id for c in assigner.blue_countries] == [USA_ID]
    for sqn in blue_sqns:
        assert assigner.for_squadron(sqn).id == USA_ID


def test_mixed_nation_side_spawns_each_squadron_under_its_own_country() -> None:
    blue_us = _squadron(USA_ID, Player.BLUE)
    blue_gr = _squadron(GREECE_ID, Player.BLUE)
    assigner = CountryAssigner(_game(CJTF_BLUE_ID, CJTF_RED_ID, [blue_us, blue_gr], []))

    assert {c.id for c in assigner.blue_countries} == {
        CJTF_BLUE_ID,
        USA_ID,
        GREECE_ID,
    }
    assert assigner.for_squadron(blue_us).id == USA_ID
    assert assigner.for_squadron(blue_gr).id == GREECE_ID


def test_cross_side_country_collision_falls_back_to_faction_country() -> None:
    # Both sides field a USA squadron. A DCS country may live in only one
    # coalition, so blue keeps USA and red's USA squadron falls back to red's
    # faction country.
    blue_us = _squadron(USA_ID, Player.BLUE)
    red_us = _squadron(USA_ID, Player.RED)
    assigner = CountryAssigner(_game(CJTF_BLUE_ID, CJTF_RED_ID, [blue_us], [red_us]))

    assert USA_ID in {c.id for c in assigner.blue_countries}
    assert USA_ID not in {c.id for c in assigner.red_countries}
    assert assigner.for_squadron(blue_us).id == USA_ID
    assert assigner.for_squadron(red_us).id == CJTF_RED_ID


def test_blue_squadron_cannot_claim_reds_faction_country() -> None:
    # A blue squadron whose country equals red's faction country must NOT register
    # that nation on the blue coalition: red's faction country is red's spawn
    # fallback and a country may live in only one coalition. The blue squadron
    # falls back to blue's faction country, and the nation appears under red only
    # (no cross-coalition overlap -> no illegal .miz).
    blue_shared = _squadron(CJTF_RED_ID, Player.BLUE)
    blue_us = _squadron(USA_ID, Player.BLUE)
    assigner = CountryAssigner(
        _game(CJTF_BLUE_ID, CJTF_RED_ID, [blue_us, blue_shared], [])
    )

    blue_ids = {c.id for c in assigner.blue_countries}
    red_ids = {c.id for c in assigner.red_countries}
    assert CJTF_RED_ID not in blue_ids
    assert CJTF_RED_ID in red_ids
    assert not (blue_ids & red_ids)  # no country on both coalitions
    assert assigner.for_squadron(blue_shared).id == CJTF_BLUE_ID  # blue fallback


def test_belligerent_ids_cover_both_sides() -> None:
    blue_us = _squadron(USA_ID, Player.BLUE)
    red_us = _squadron(USA_ID, Player.RED)
    assigner = CountryAssigner(_game(CJTF_BLUE_ID, CJTF_RED_ID, [blue_us], [red_us]))
    assert assigner.belligerent_ids == {CJTF_BLUE_ID, USA_ID, CJTF_RED_ID}


def test_resolved_country_is_the_registered_instance() -> None:
    # pydcs attaches spawned groups to the Country instance and only serializes
    # countries reachable from the coalition, so the instance returned for a
    # squadron must be the very one registered on the coalition.
    blue_gr = _squadron(GREECE_ID, Player.BLUE)
    assigner = CountryAssigner(_game(CJTF_BLUE_ID, CJTF_RED_ID, [blue_gr], []))

    resolved = assigner.for_squadron(blue_gr)
    assert any(resolved is c for c in assigner.blue_countries)
