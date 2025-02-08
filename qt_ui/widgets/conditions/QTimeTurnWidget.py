from datetime import datetime

from PySide6.QtWidgets import QGroupBox, QHBoxLayout, QLabel, QVBoxLayout

from game.sim import GameUpdateEvents
from game.timeofday import TimeOfDay
from game.weather.conditions import Conditions
from qt_ui import uiconstants as CONST
from qt_ui.simcontroller import SimController


class QTimeTurnWidget(QGroupBox):
    """
    UI Component to display current turn and time info
    """

    def __init__(self, sim_controller: SimController) -> None:
        super(QTimeTurnWidget, self).__init__("Turn")
        self.sim_controller = sim_controller
        self.setStyleSheet(
            "padding: 0px; margin-left: 5px; margin-right: 0px; margin-top: 1ex; margin-bottom: 5px; border-right: 0px"
        )

        self.icons = {
            TimeOfDay.Dawn: CONST.ICONS["Dawn"],
            TimeOfDay.Day: CONST.ICONS["Day"],
            TimeOfDay.Dusk: CONST.ICONS["Dusk"],
            TimeOfDay.Night: CONST.ICONS["Night"],
        }

        # self.setProperty('style', 'conditions__widget--turn')
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.daytime_icon = QLabel()
        self.daytime_icon.setPixmap(self.icons[TimeOfDay.Dawn])
        self.layout.addWidget(self.daytime_icon)

        self.time_column = QVBoxLayout()
        self.layout.addLayout(self.time_column)

        self.date_display = QLabel()
        self.time_column.addWidget(self.date_display)

        self.time_display = QLabel()
        self.time_column.addWidget(self.time_display)

        sim_controller.sim_update.connect(self.on_sim_update)

    def on_sim_update(self, _events: GameUpdateEvents) -> None:
        time = self.sim_controller.current_time_in_sim_if_game_loaded
        if time is None:
            self.date_display.setText("")
            self.time_display.setText("")
        else:
            self.set_date_and_time(time)

    def set_current_turn(self, turn: int, conditions: Conditions) -> None:
        """Sets the turn information display.

        :arg turn Current turn number.
        :arg conditions Current time and weather conditions.
        """
        self.daytime_icon.setPixmap(self.icons[conditions.time_of_day])
        self.set_date_and_time(conditions.start_time)
        self.setTitle(f"Turn {turn}")

    def set_date_and_time(self, time: datetime) -> None:
        self.date_display.setText(time.strftime("%d %b %Y"))
        self.time_display.setText(time.strftime("%H:%M:%S Local"))
