"""A FIXED-prefixed campaign group generates exactly as drawn.

Builds a real New Game from a copy of Black Sea with drawn sites added
next to one of its red SAM markers.
"""

from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

import dcs
import pytest
from dcs.mapping import Point
from dcs.vehicles import AirDefence, Unarmed

from game import persistency
from game.campaignloader.campaign import Campaign
from game.campaignloader.mizcampaignloader import MizCampaignLoader
from game.data.groups import GroupTask
from game.factions import FACTIONS
from game.settings import Settings
from game.theater.iadsnetwork.iadsrole import IadsRole
from game.theater.start_generator import GameGenerator, GeneratorSettings, ModSettings
from game.theater.theatergroundobject import TheaterGroundObject
from game.theater.theatergroup import IadsGroundGroup

CAMPAIGN = Path("resources/campaigns/black_sea.yaml")

#: (type, east offset m, north offset m, heading deg) from the site's anchor.
SA11 = [
    (AirDefence.SA_11_Buk_SR_9S18M1, 0, 0, 10),
    (AirDefence.SA_11_Buk_CC_9S470M1, 40, 15, 200),
    (AirDefence.SA_11_Buk_LN_9A310M1, 150, 90, 45),
    (AirDefence.SA_11_Buk_LN_9A310M1, -140, 110, 315),
    (AirDefence.ZSU_23_4_Shilka, 0, -250, 180),
    (Unarmed.Ural_375, -60, -40, 90),
]
#: A Patriot radar and launcher: nothing the red Russian faction can field.
PATRIOT = [
    (AirDefence.Patriot_str, 0, 0, 0),
    (AirDefence.Patriot_ln, 120, 40, 0),
]


def _add_site(mission: dcs.Mission, name: str, anchor: Point, units: list[Any]) -> None:
    country = mission.country(MizCampaignLoader.RED_COUNTRY.name)
    assert country is not None
    first_type, east, north, heading = units[0]
    group = mission.vehicle_group(
        country,
        name,
        first_type,
        Point(anchor.x + north, anchor.y + east, mission.terrain),
        heading=heading,
        group_size=1,
    )
    for unit_type, east, north, heading in units[1:]:
        unit = mission.vehicle(f"{name} {len(group.units)}", unit_type)
        unit.position = Point(anchor.x + north, anchor.y + east, mission.terrain)
        unit.heading = heading
        group.add_unit(unit)


@pytest.fixture(scope="module")
def game(tmp_path_factory: pytest.TempPathFactory) -> Any:
    folder = tmp_path_factory.mktemp("campaign")
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(persistency, "_dcs_saved_game_folder", str(folder))
        yield _generate(folder)


def _generate(folder: Path) -> Any:
    shutil.copy(CAMPAIGN, folder / CAMPAIGN.name)
    mission = dcs.Mission()
    mission.load_file(str(CAMPAIGN.with_suffix(".miz")))
    red = mission.country(MizCampaignLoader.RED_COUNTRY.name)
    assert red is not None
    marker = next(
        g
        for g in red.vehicle_group
        if g.units[0].type in MizCampaignLoader.MEDIUM_RANGE_SAM_UNIT_TYPES
    )
    anchor = marker.position
    _add_site(
        mission,
        "FIXED SA-11 test",
        Point(anchor.x + 3000, anchor.y, mission.terrain),
        SA11,
    )
    _add_site(
        mission,
        "fixed-patriot test",
        Point(anchor.x - 3000, anchor.y, mission.terrain),
        PATRIOT,
    )
    mission.save(str(folder / CAMPAIGN.with_suffix(".miz").name))

    campaign = Campaign.from_file(folder / CAMPAIGN.name)
    theater = campaign.load_theater(campaign.advanced_iads)
    settings = Settings()
    if campaign.settings:
        settings.__dict__.update(Settings.deserialize_state_dict(campaign.settings))
    return GameGenerator(
        player=FACTIONS[campaign.recommended_player_faction],
        enemy=FACTIONS[campaign.recommended_enemy_faction],
        theater=theater,
        air_wing_config=campaign.load_air_wing_config(theater),
        settings=settings,
        generator_settings=GeneratorSettings(
            start_date=datetime(2000, 1, 1),
            start_time=campaign.recommended_start_time,
            player_budget=campaign.recommended_player_money,
            enemy_budget=campaign.recommended_enemy_money,
            inverted=False,
            advanced_iads=campaign.advanced_iads,
            no_carrier=False,
            no_lha=False,
            no_player_navy=False,
            no_enemy_navy=False,
            tgo_config=campaign.load_ground_forces_config(),
            carrier_config=campaign.load_carrier_config(),
            squadrons_start_full=True,
        ),
        mod_settings=ModSettings(),
        campaign_name=campaign.name,
    ).generate()


def _tgo(game: Any, name: str) -> TheaterGroundObject:
    return next(
        tgo
        for cp in game.theater.controlpoints
        for tgo in cp.connected_objectives
        if tgo.original_name == name
    )


def test_prefix_needs_a_word_break() -> None:
    def named(name: str) -> Any:
        return type("G", (), {"name": name})()

    assert MizCampaignLoader.is_exact_site(named("FIXED SA-6"))
    assert MizCampaignLoader.is_exact_site(named("fixed-2"))
    assert not MizCampaignLoader.is_exact_site(named("FIXEDWING"))
    assert not MizCampaignLoader.is_exact_site(named("SA-6 FIXED"))


def test_drawn_site_keeps_every_unit_where_it_was_drawn(game: Any) -> None:
    tgo = _tgo(game, "FIXED SA-11 test")
    assert tgo.control_point.captured.is_red
    assert tgo.task is GroupTask.MERAD
    drawn = {
        (
            unit.type_id,
            round(unit.position.x),
            round(unit.position.y),
            round(unit.heading),
        )
        for preset in tgo.control_point.preset_locations.exact_air_defenses
        if preset.original_name == tgo.original_name
        for unit in preset.units
    }
    placed = {
        (
            u.type.id,
            round(u.position.x),
            round(u.position.y),
            round(u.position.heading.degrees),
        )
        for u in tgo.units
    }
    assert len(drawn) == len(SA11)
    # Every drawn unit is there as drawn; anything else is a template extra.
    assert drawn <= placed
    extras = {
        u.unit_type.unit_class.value
        for u in tgo.units
        if u.unit_type
        and (
            u.type.id,
            round(u.position.x),
            round(u.position.y),
            round(u.position.heading.degrees),
        )
        not in drawn
    }
    assert extras <= {"Logistics", "Power", "SHORAD", "AAA", "Manpad"}


def test_drawn_guns_are_the_sites_point_defense(game: Any) -> None:
    tgo = _tgo(game, "FIXED SA-11 test")
    roles = {
        u.type.id: group.iads_role
        for group in tgo.groups
        if isinstance(group, IadsGroundGroup)
        for u in group.units
    }
    assert roles[AirDefence.ZSU_23_4_Shilka.id] is IadsRole.POINT_DEFENSE
    assert roles[AirDefence.SA_11_Buk_LN_9A310M1.id] is IadsRole.SAM
    assert roles[AirDefence.SA_11_Buk_SR_9S18M1.id] is IadsRole.SAM


def test_a_site_the_faction_cannot_field_falls_back_to_stock(game: Any) -> None:
    tgo = _tgo(game, "fixed-patriot test")
    assert tgo.control_point.captured.is_red
    types = {u.type.id for u in tgo.units}
    assert tgo.units
    assert AirDefence.Patriot_str.id not in types
    assert AirDefence.Patriot_ln.id not in types
