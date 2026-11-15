from datetime import datetime
from typing import Optional, cast

from PySide6.QtCore import QDateTime
from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel, QHBoxLayout, QDateTimeEdit

from game.weather.daylight import daylight_lines, moon_line, sun_times, theater_middle
from qt_ui.widgets.conditions.QTimeTurnWidget import QTimeTurnWidget


class QTimeAdjustmentWidget(QWidget):
    def __init__(
        self, time_turn: QTimeTurnWidget, parent: Optional[QWidget] = None
    ) -> None:
        super().__init__(parent)
        self.current_datetime = time_turn.sim_controller.current_time_in_sim
        game_loop = time_turn.sim_controller.game_loop
        assert game_loop is not None
        theater = game_loop.game.theater
        self.timezone = theater.timezone
        self.sun_position = theater_middle(theater)
        self.init_ui()

    def init_ui(self) -> None:
        vbox = QVBoxLayout()

        vbox.addWidget(QLabel("<h2><b>Time & Date:</b></h2>"))
        vbox.addWidget(
            QLabel(
                "<h4><b>ACCEPT keeps your flight plans and re-times them to the "
                "new mission start.</b></h4>"
            )
        )

        hbox = QHBoxLayout()

        t = self.current_datetime.time()
        d = self.current_datetime.date()
        self.datetime_edit = QDateTimeEdit(
            QDateTime(d.year, d.month, d.day, t.hour, t.minute, t.second)
        )
        hbox.addWidget(self.datetime_edit)

        vbox.addLayout(hbox)

        self.sun_times_label = QLabel()
        self.sun_times_label.setToolTip("Measured at the middle of the map.")
        vbox.addWidget(self.sun_times_label)
        self.light_label = QLabel()
        vbox.addWidget(self.light_label)
        self.moon_label = QLabel()
        vbox.addWidget(self.moon_label)
        self.datetime_edit.dateTimeChanged.connect(self.update_daylight)
        self.update_daylight()

        self.setLayout(vbox)

    def update_daylight(self) -> None:
        start = cast(datetime, self.datetime_edit.dateTime().toPython())
        sunrise, sunset = sun_times(self.sun_position, start.date(), self.timezone)
        times, light = daylight_lines(start, sunrise, sunset)
        self.sun_times_label.setText(times)
        self.light_label.setText(light)
        self.moon_label.setText(moon_line(start, self.timezone))
