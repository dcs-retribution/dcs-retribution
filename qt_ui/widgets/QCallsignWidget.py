from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QWidget,
)

from game.radio.CallsignContainer import CallsignContainer, Callsign
from qt_ui.models import GameModel
from qt_ui.windows.QCallsignDialog import QCallsignDialog


class QCallsignWidget(QWidget):
    callsign_changed = Signal(QWidget)

    def __init__(self, container: CallsignContainer, game_model: GameModel) -> None:
        super().__init__()

        self.ct = container
        self.gm = game_model

        columns = QHBoxLayout()
        self.setLayout(columns)

        self.callsign = QLabel(self._get_label_text())
        columns.addWidget(self.callsign)
        columns.addStretch()

        self.set_callsign_btn = QPushButton("Set Callsign")
        self.set_callsign_btn.setProperty("class", "comms")
        self.set_callsign_btn.setFixedWidth(100)
        columns.addWidget(self.set_callsign_btn)
        self.set_callsign_btn.clicked.connect(self.open_callsign_dialog)

        self.reset_callsign_btn = QPushButton("Reset Callsign")
        self.reset_callsign_btn.setProperty("class", "btn-danger comms")
        self.reset_callsign_btn.setFixedWidth(100)
        columns.addWidget(self.reset_callsign_btn)
        self.reset_callsign_btn.clicked.connect(self.reset_callsign)

    def _get_label_text(self) -> str:
        cs = (
            "AUTO"
            if self.ct.callsign is None
            else f"{self.ct.callsign.name} {self.ct.callsign.nr}"
        )
        return f"<b>Callsign: {cs}</b>"

    def open_callsign_dialog(self) -> None:
        self.callsign_dialog = QCallsignDialog(self, self.ct)
        self.callsign_dialog.accepted.connect(self.assign_callsign)
        self.callsign_dialog.show()

    def assign_callsign(self) -> None:
        name = self.callsign_dialog.callsign_name_input.currentText()
        nr = self.callsign_dialog.callsign_nr_input.value()
        self.ct.callsign = Callsign(name, nr)
        self.callsign.setText(self._get_label_text())
        self.callsign_changed.emit(self)

    def reset_callsign(self) -> None:
        self.ct.callsign = None
        self.callsign.setText(self._get_label_text())
        self._reset_color_and_tooltip()
        self.callsign_changed.emit(self)

    def _reset_color_and_tooltip(self):
        self.callsign.setStyleSheet("color: white")
        self.callsign.setToolTip(None)
