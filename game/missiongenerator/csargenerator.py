from __future__ import annotations

from typing import TYPE_CHECKING

from dcs import Mission
from dcs.mapping import Vector2
from dcs.task import EmbarkToTransport
from dcs.vehicles import Infantry

from game.theater import Player
from game.utils import Distance, meters

if TYPE_CHECKING:
    from game import Game
    from game.coalition import Coalition
    from game.missiongenerator.missiondata import MissionData
    from game.squadrons.downedpilot import DownedPilot

#: Radius the pilot will walk within to board a helicopter that is embarking.
#:
#: Must exceed LANDING_ZONE_OFFSET (game/ato/flightplans/csar.py): the touchdown
#: point is deliberately held away from the survivor so the helicopter can't land
#: on them, and the AI adds its own dispersion on top of that. A helicopter that
#: comes down outside this radius is never reached and the rescue silently fails.
EMBARK_ZONE_RADIUS = meters(300)


class CsarGenerator:
    """Places downed pilots and the Ops.CSAR templates into the mission.

    Each downed pilot is generated as a real ground group carrying DCS's native
    ``EmbarkToTransport`` task. That is what makes an AI rescue work: the stock
    DCS transport logic walks the pilot to any helicopter running an ``Embarking``
    task in the same zone and loads them aboard. MOOSE Ops.CSAR cannot do this for
    AI helicopters at all -- its boarding loop only ever considers player units --
    so the AI side is handled entirely by DCS, while OpsCSAR.lua additionally hands
    these same groups to Ops.CSAR so a player in any CSAR-capable helicopter can
    still fly out and pick them up.
    """

    def __init__(self, mission: Mission, game: Game, mission_data: MissionData) -> None:
        self.mission = mission
        self.game = game
        self.mission_data = mission_data

    def generate(self) -> None:
        settings = self.game.settings
        for player, key in ((Player.BLUE, "blue"), (Player.RED, "red")):
            enabled = (
                settings.csar_enabled if player.is_blue else settings.csar_enabled_red
            )
            if not enabled:
                continue
            coalition = self.game.coalition_for(player)
            self._generate_template(coalition, key)
            for downed in coalition.downed_pilots:
                self._generate_downed_pilot(coalition, downed)

    def _generate_template(self, coalition: Coalition, key: str) -> None:
        """Creates the late-activated group Ops.CSAR is constructed against.

        Ops.CSAR requires a template group to exist even though we hand it
        pre-placed pilots rather than letting it spawn its own.
        """
        country = self.mission.country(coalition.faction.country.name)
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

    def _embark_radius_for(self, downed: DownedPilot) -> Distance:
        """How far this survivor will walk to board.

        Normally the standard embark zone around themselves. When they are part of
        a cluster the rescue flight may land for any member of it, so the zone has
        to stretch to whichever of them is furthest away -- otherwise the flight
        sets down for one pilot and the rest never walk out.
        """
        cluster = downed.cluster(meters(self.game.settings.csar_cluster_radius))
        if len(cluster) < 2:
            return EMBARK_ZONE_RADIUS
        furthest = max(
            other.position.distance_to_point(downed.position) for other in cluster
        )
        return EMBARK_ZONE_RADIUS + meters(furthest)

    def _generate_downed_pilot(self, coalition: Coalition, downed: DownedPilot) -> None:
        from game.missiongenerator.missiondata import CsarPilotGroupInfo

        country = self.mission.country(coalition.faction.country.name)
        # Ops.CSAR announces the survivor by group name in its MAYDAY call, so
        # keep it readable. The id fragment only guards against two pilots in the
        # same mission sharing a generated name.
        group_name = f"CSAR {downed.pilot.name} {str(downed.id)[:8]}"
        group = self.mission.vehicle_group(
            country,
            group_name,
            Infantry.Soldier_M4,
            downed.position,
        )
        # Keep the survivor out of the mission planner's clutter, but leave them
        # visible in-game so a player can spot them.
        group.hidden_on_planner = True

        # The pilot's half of DCS's native troop transport. Only useful when the
        # rescue helicopter is going to land, since the embark won't fire until it
        # has weight off wheels -- under hover extraction (including any survivor
        # in the water) OpsCSAR.lua does the pickup by script instead.
        if not downed.needs_hover_extraction(self.game.settings):
            group.points[0].tasks.append(
                EmbarkToTransport(
                    position=Vector2(downed.position.x, downed.position.y),
                    zone_radius=round(self._embark_radius_for(downed).meters),
                )
            )

        self.mission_data.csar_pilot_groups[str(downed.id)] = CsarPilotGroupInfo(
            group_name=group_name,
            unit_name=group.units[0].name,
            group_id=group.id,
            blue=coalition.player.is_blue,
        )
