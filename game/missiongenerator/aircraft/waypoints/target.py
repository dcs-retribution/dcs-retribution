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
