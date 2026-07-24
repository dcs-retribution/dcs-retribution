from __future__ import annotations

from typing import TYPE_CHECKING

from dcs import Mission
from dcs.vehicles import Infantry

from game.theater import Player

if TYPE_CHECKING:
    from game import Game
    from game.missiongenerator.missiondata import MissionData


class CsarGenerator:
    """Creates the late-activated infantry template groups used by Ops.CSAR.

    MOOSE ``Ops.CSAR`` clones a late-activated infantry group as the template for
    every downed pilot it spawns. We add one hidden, late-activated soldier per
    coalition that has CSAR enabled and record its group name in the mission data
    so :class:`LuaGenerator` can pass it to ``OpsCSAR.lua``.
    """

    def __init__(self, mission: Mission, game: Game, mission_data: MissionData) -> None:
        self.mission = mission
        self.game = game
        self.mission_data = mission_data

    def generate(self) -> None:
        settings = self.game.settings
        sides = []
        if settings.csar_enabled:
            sides.append((Player.BLUE, "blue"))
        if settings.csar_enabled_red:
            sides.append((Player.RED, "red"))

        for player, key in sides:
            coalition = self.game.coalition_for(player)
            country = self.mission.country(coalition.faction.country.name)
            # Park the template far off in a corner; it never activates on its own.
            position = self.game.theater.terrain.map_view_default.position
            group_name = f"CSAR_PILOT_{key.upper()}"
            group = self.mission.vehicle_group(
                country,
                group_name,
                Infantry.Soldier_M4,
                position,
            )
            group.late_activation = True
            group.hidden = True
            group.hidden_on_mfd = True
            group.hidden_on_planner = True
            self.mission_data.csar_pilot_templates[key] = group_name
