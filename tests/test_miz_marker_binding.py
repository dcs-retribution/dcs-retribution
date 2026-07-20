"""Blue-block miz markers generate, and bind to blue control points.

The RED country block is the coalition-agnostic default marker block: blue air
defenses are conventionally authored as red-block markers near blue fields and
proximity decides the owner. But a marker authored in the BLUE block was
silently dropped for most classes (ships / SAMs / EWRs / missile / coastal /
offshore strike) -- 22 authored markers across 7 shipped campaigns never
generated -- and the classes that did walk both blocks bound coalition-blind,
so one side's marker could be handed to the other, where the objective then
silently never generates.

Contract locked here: every marker class also walks the blue block; a
blue-block MARKER binds the nearest BLUE control point when one is reasonably
close (bounded by BLUE_BLOCK_MAX_DETOUR, scoped to marker classes only so the
blue-block economy objects keep binding by proximity); red-block markers keep
the nearest-any proximity convention.
"""

from pathlib import Path

import pytest
from dcs.countries import (
    CombinedJointTaskForcesBlue,
    CombinedJointTaskForcesRed,
)
from dcs.mission import Mission
from dcs.statics import Fortification
from dcs.terrain.caucasus import Caucasus
from dcs.vehicles import AirDefence

from game import persistency
from game.campaignloader.mizcampaignloader import MizCampaignLoader
from game.theater.theaterloader import TheaterLoader


@pytest.fixture(autouse=True)
def _init_persistency(tmp_path_factory: pytest.TempPathFactory) -> None:
    persistency.setup(
        str(tmp_path_factory.mktemp("saved_games")),
        prefer_liberation_payloads=False,
        port=0,
    )


def _build_test_miz(path: Path) -> None:
    mission = Mission(terrain=Caucasus())
    blue_field = mission.terrain.airports["Kutaisi"]
    red_field = mission.terrain.airports["Senaki-Kolkhi"]
    blue_field.set_blue()
    red_field.set_red()

    blue_country = CombinedJointTaskForcesBlue()
    red_country = CombinedJointTaskForcesRed()
    mission.coalition["blue"].add_country(blue_country)
    mission.coalition["red"].add_country(red_country)

    # A BLUE-block EWR marker planted right next to the RED field: nearest-any
    # binding would hand it to red, but the blue block declares blue ownership.
    mission.vehicle_group(
        blue_country,
        "Blue EWR marker",
        AirDefence.x_1L13_EWR,
        red_field.position.point_from_heading(45, 3000),
    )

    # A RED-block SHORAD marker next to the BLUE field: the coalition-agnostic
    # proximity convention must keep binding it to the blue field (this is how
    # campaigns conventionally author blue air defenses).
    mission.vehicle_group(
        red_country,
        "Red block SHORAD marker",
        AirDefence.Strela_1_9P31,
        blue_field.position.point_from_heading(90, 3000),
    )

    mission.save(str(path))


def test_marker_coalition_binding(tmp_path: Path) -> None:
    miz = tmp_path / "marker_binding.miz"
    _build_test_miz(miz)

    theater = TheaterLoader("caucasus").load()
    MizCampaignLoader(miz, theater).populate_theater()

    kutaisi = theater.control_point_named("Kutaisi")
    senaki = theater.control_point_named("Senaki-Kolkhi")

    # The blue-block EWR generated at all (was silently dropped) and bound the
    # blue field even though the red field is 3 km away.
    assert len(kutaisi.preset_locations.ewrs) == 1
    assert not senaki.preset_locations.ewrs

    # The red-block marker still binds by proximity: blue field owns it.
    assert len(kutaisi.preset_locations.short_range_sams) == 1
    assert not senaki.preset_locations.short_range_sams


def _build_scoping_miz(path: Path) -> None:
    """Kutaisi (blue) far from two red fields, with blue-block objects on the
    red fields: an economy object (factory) and a marker (EWR) beyond the
    detour bound, plus a near-field marker that should still prefer blue."""
    mission = Mission(terrain=Caucasus())
    kutaisi = mission.terrain.airports["Kutaisi"]  # blue
    senaki = mission.terrain.airports["Senaki-Kolkhi"]  # red, ~37 km from Kutaisi
    min_vody = mission.terrain.airports["Mineralnye Vody"]  # red, ~235 km away
    kutaisi.set_blue()
    senaki.set_red()
    min_vody.set_red()

    blue_country = CombinedJointTaskForcesBlue()
    red_country = CombinedJointTaskForcesRed()
    mission.coalition["blue"].add_country(blue_country)
    mission.coalition["red"].add_country(red_country)

    # Blue-block FACTORY sitting on the distant red field. The blue block holds
    # the economy objects by convention; an all-class preference would re-own
    # them to distant blue fields. It must bind the red field it sits on.
    mission.static_group(
        blue_country,
        "Blue block factory",
        Fortification.Workshop_A,
        min_vody.position.point_from_heading(0, 3000),
    )

    # Blue-block EWR on the distant red field: nearest blue field (Kutaisi) is
    # ~235 km away, far past BLUE_BLOCK_MAX_DETOUR, so proximity decides.
    mission.vehicle_group(
        blue_country,
        "Blue EWR far",
        AirDefence.x_1L13_EWR,
        min_vody.position.point_from_heading(45, 3000),
    )

    # Blue-block EWR next to the near red field (~37 km detour, within the
    # bound): the near-field preference still binds the blue field.
    mission.vehicle_group(
        blue_country,
        "Blue EWR near",
        AirDefence.x_1L13_EWR,
        senaki.position.point_from_heading(45, 3000),
    )

    mission.save(str(path))


def test_blue_block_preference_is_scoped_and_bounded(tmp_path: Path) -> None:
    miz = tmp_path / "scoping.miz"
    _build_scoping_miz(miz)

    theater = TheaterLoader("caucasus").load()
    MizCampaignLoader(miz, theater).populate_theater()

    kutaisi = theater.control_point_named("Kutaisi")
    senaki = theater.control_point_named("Senaki-Kolkhi")
    min_vody = theater.control_point_named("Mineralnye Vody")

    # Economy object is never preferred to a distant blue field -- binds the
    # red field it sits on.
    assert len(min_vody.preset_locations.factories) == 1
    assert not kutaisi.preset_locations.factories

    # Marker beyond the detour bound binds by proximity (the red field), not
    # the 235 km-distant blue field.
    assert len(min_vody.preset_locations.ewrs) == 1

    # Marker within the detour bound still prefers the blue field.
    assert len(kutaisi.preset_locations.ewrs) == 1
    assert not senaki.preset_locations.ewrs
