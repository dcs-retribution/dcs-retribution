from PySide6 import QtCore, QtGui
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
)

from game.weather.conditions import Conditions
from qt_ui.simcontroller import SimController
from qt_ui.widgets.QConditionsDialog import QConditionsDialog
from qt_ui.widgets.conditions.QTimeTurnWidget import QTimeTurnWidget
from qt_ui.widgets.conditions.QWeatherWidget import QWeatherWidget


class QConditionsWidget(QFrame):
    """
    UI Component to display Turn Number, Day Time & Hour and weather combined.
    """

    def __init__(self, sim_controller: SimController) -> None:
        super(QConditionsWidget, self).__init__()
        self.setProperty("style", "QConditionsWidget")
        self.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setHorizontalSpacing(0)
        self.layout.setVerticalSpacing(0)
        self.setLayout(self.layout)

        self.time_turn_widget = QTimeTurnWidget(sim_controller)
        self.time_turn_widget.setStyleSheet("QGroupBox { margin-right: 0px; }")
        self.layout.addWidget(self.time_turn_widget, 0, 0)

        self.weather_widget = QWeatherWidget()
        self.weather_widget.setStyleSheet(
            "QGroupBox { margin-top: 5px; margin-left: 0px; border-left: 0px; }"
        )
        self.weather_widget.hide()
        self.layout.addWidget(self.weather_widget, 0, 1)

    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent) -> None:
        QConditionsDialog(self.time_turn_widget, self.weather_widget).exec()

    def setCurrentTurn(self, turn: int, conditions: Conditions) -> None:
        """Sets the turn information display.

        :arg turn Current turn number.
        :arg conditions Current time and weather conditions.
        """
        self.time_turn_widget.set_current_turn(turn, conditions)
        self.weather_widget.setCurrentTurn(turn, conditions)
        self.weather_widget.show()
