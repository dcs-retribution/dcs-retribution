from dcs.point import MovingPoint
from dcs.task import Land, RunScript, SetUnlimitedFuelCommand

from game.ato import FlightType
from .pydcswaypointbuilder import PydcsWaypointBuilder


class LandingZoneBuilder(PydcsWaypointBuilder):
    def build(self) -> MovingPoint:
        waypoint = super().build()
        # Create a landing task, currently only for Helos!
        # Calculate a landing point with a small buffer to prevent AI from landing
        # directly at the static ammo depot and exploding
        landing_point = waypoint.position.random_point_within(30, 20)
        # Use Land Task with 30s duration for helos
        combat_land = self.flight.coalition.game.settings.use_ai_combat_landing
        waypoint.add_task(Land(landing_point, duration=30, combat_landing=combat_land))
        if waypoint.name == "DROPOFFZONE":
            script = RunScript(
                f'trigger.action.setUserFlag("split-{id(self.package)}", true)'
            )
            waypoint.tasks.append(script)
            self._restore_unlimited_fuel_for_return_leg(waypoint)
        return waypoint

    def _restore_unlimited_fuel_for_return_leg(self, waypoint: MovingPoint) -> None:
        """Restores unlimited fuel once the drop-off unloading completes.

        Air assault flight plans emit a JOIN waypoint but never a SPLIT, so
        under the phase-based AI fuel policy their flights consume real fuel
        from the objective onward and never regain unlimited fuel for the
        return leg. The drop-off landing is the executed objective-completion
        boundary for helicopter air assaults (the return navigation anchors at
        the drop-off), so the fuel command is appended after the Land task and
        the package-release script: fuel is only restored after unloading, and
        never while the objective is still active.
        """
        if self.flight.flight_type != FlightType.AIR_ASSAULT:
            return
        if not self.flight.squadron.coalition.game.settings.ai_unlimited_fuel:
            return
        waypoint.tasks.append(SetUnlimitedFuelCommand(True))
