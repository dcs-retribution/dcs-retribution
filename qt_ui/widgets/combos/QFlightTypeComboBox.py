"""Combo box for selecting a flight's task type."""

from PySide6.QtWidgets import QComboBox

from game.ato.flighttype import FlightType
from game.settings.settings import Settings
from game.theater import ConflictTheater, MissionTarget


class QFlightTypeComboBox(QComboBox):
    """Combo box for selecting a flight task type."""

    def __init__(
        self,
        theater: ConflictTheater,
        target: MissionTarget,
        settings: Settings,
        is_ownfor: bool,
    ) -> None:
        super().__init__()
        self.theater = theater
        self.target = target
        for mission_type in self.target.mission_types(for_player=is_ownfor):
            if mission_type == FlightType.AIR_ASSAULT and not settings.plugin_option(
                "ctld"
            ):
                # Only add Air Assault if ctld plugin is enabled
                continue
            self.addItem(str(mission_type), userData=mission_type)
