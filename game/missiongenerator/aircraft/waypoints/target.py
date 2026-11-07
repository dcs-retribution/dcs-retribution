from dcs.point import MovingPoint
from dcs.task import SetUnlimitedFuelCommand

from game.ato import FlightType
from .pydcswaypointbuilder import PydcsWaypointBuilder


class TargetBuilder(PydcsWaypointBuilder):
    """Waypoint builder for target waypoint types.

    This handles both precise target locations (TARGET_POINT) and target areas
    (TARGET_GROUP_LOC).
    """

    def dcs_name_for_waypoint(self) -> str:
        resolved = super().dcs_name_for_waypoint()  # honors custom_name override
        if self.flight.unit_type.use_f15e_waypoint_names:
            return f"#T {resolved}"
        return resolved

    def add_tasks(self, waypoint: MovingPoint) -> None:
        super().add_tasks(waypoint)
        self._restore_unlimited_fuel_for_return_leg(waypoint)

    def _restore_unlimited_fuel_for_return_leg(self, waypoint: MovingPoint) -> None:
        """Restores unlimited fuel once the air-assault objective completes.

        Air assault flight plans emit a JOIN waypoint but never a SPLIT, so
        under the phase-based AI fuel policy their flights consume real fuel
        from the objective onward and never regain unlimited fuel for the
        return leg. The assault area is the executed objective-completion
        boundary for Hercules air assaults: it is generated for every air
        assault and explicitly included in AI routes (unlike the helicopter
        assault area, which is player-only and whose flights instead restore
        fuel at their drop-off landing).
        """
        if self.flight.flight_type != FlightType.AIR_ASSAULT:
            return
        if not self.flight.squadron.coalition.game.settings.ai_unlimited_fuel:
            return
        waypoint.tasks.append(SetUnlimitedFuelCommand(True))
