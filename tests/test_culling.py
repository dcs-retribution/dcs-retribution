"""Culling must not erase scenery-objective kill tracking.

A scenery objective's map buildings exist whether or not the campaign spawns
anything, so a culled trigger zone leaves a bombable, visibly-collapsing
target whose death is never recorded — the kill silently vanishes at debrief.
The apparatus (trigger zone, MapObjectIsDead rule, IADS command stand-in)
costs nothing, so it generates regardless of culling; culling keeps its
performance win for real spawnable content.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from game.missiongenerator.tgogenerator import GroundObjectGenerator
from game.theater.theatergroup import SceneryUnit


def _culled_generator(unit: MagicMock) -> GroundObjectGenerator:
    group = MagicMock()
    group.units = [unit]
    ground_object = MagicMock()
    ground_object.groups = [group]
    game = MagicMock()
    game.iads_considerate_culling.return_value = True  # this TGO is culled
    game.settings.plugin_option.return_value = False
    return GroundObjectGenerator(
        ground_object, MagicMock(), game, MagicMock(), MagicMock()
    )


def test_culled_scenery_objective_keeps_kill_tracking() -> None:
    scenery = MagicMock(spec=SceneryUnit)
    scenery.is_static = True
    generator = _culled_generator(scenery)

    with patch.object(
        GroundObjectGenerator, "add_trigger_zone_for_scenery"
    ) as add_zone, patch.object(
        GroundObjectGenerator, "create_static_group"
    ) as create_static:
        generator.generate()

    add_zone.assert_called_once_with(scenery)
    create_static.assert_not_called()


def test_culled_tgo_still_skips_spawnable_content() -> None:
    # The other half of the contract: culling still buys its performance —
    # a culled TGO's real statics never spawn.
    static = MagicMock()
    static.is_static = True
    generator = _culled_generator(static)

    with patch.object(GroundObjectGenerator, "create_static_group") as create_static:
        generator.generate()

    create_static.assert_not_called()
