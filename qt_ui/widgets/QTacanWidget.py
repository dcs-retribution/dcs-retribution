from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QWidget,
)

from game.radio.TacanContainer import TacanContainer
from game.radio.tacan import TacanChannel, TacanBand
from qt_ui.models import GameModel
from qt_ui.windows.QTacanDialog import QTacanDialog


class QTacanWidget(QWidget):
    def __init__(self, container: TacanContainer, game_model: GameModel) -> None:
        super().__init__()

        self.ct = container
        self.gm = game_model

        columns = QHBoxLayout()
        self.setLayout(columns)

        self.channel = QLabel(self._get_label_text())
        self.check_channel()
        columns.addWidget(self.channel)
        columns.addStretch()

        self.set_tacan_btn = QPushButton("Set TACAN")
        self.set_tacan_btn.setProperty("class", "comms")
        self.set_tacan_btn.setFixedWidth(100)
        columns.addWidget(self.set_tacan_btn)
        self.set_tacan_btn.clicked.connect(self.open_tacan_dialog)

        self.reset_tacan_btn = QPushButton("Reset TACAN")
        self.reset_tacan_btn.setProperty("class", "btn-danger comms")
        self.reset_tacan_btn.setFixedWidth(100)
        columns.addWidget(self.reset_tacan_btn)
        self.reset_tacan_btn.clicked.connect(self.reset_tacan)

    def _get_label_text(self) -> str:
        c = "AUTO" if self.ct.tacan is None else self.ct.tacan
        cs = self.ct.tcn_name
        cs = "" if cs is None else f" ({cs})"
        return f"<b>TACAN: {c}{cs}</b>"

    def open_tacan_dialog(self) -> None:
        self.tacan_dialog = QTacanDialog(self, self.ct)
        self.tacan_dialog.accepted.connect(self.assign_tacan)
        self.tacan_dialog.show()

    def assign_tacan(self) -> None:
        channel = self.tacan_dialog.tacan_input.value()
        band = self.tacan_dialog.band_input.currentText()
        band = TacanBand.X if band == "X" else TacanBand.Y
        self._try_remove()
        self.ct.tacan = TacanChannel(number=channel, band=band)
        self.gm.allocated_tacan.append(self.ct.tacan)
        if cs := self.tacan_dialog.callsign_input.text():
            self.ct.tcn_name = cs.upper()
        self.channel.setText(self._get_label_text())
        self.check_channel()

    def reset_tacan(self) -> None:
        self._try_remove()
        self.ct.tacan = None
        self.ct.tcn_name = None
        self.channel.setText(self._get_label_text())
        self._reset_color_and_tooltip()

    def check_channel(self) -> None:
        if self.ct.tacan is None:
            return
        if self.gm.allocated_tacan.count(self.ct.tacan) > 1:
            self.channel.setStyleSheet("color: orange")
            self.channel.setToolTip(
                "Double booked TACAN channel, verify that this was your intention."
            )
        elif self.gm.allocated_tacan.count(self.ct.tacan) == 1:
            self._reset_color_and_tooltip()

    def _reset_color_and_tooltip(self):
        self.channel.setStyleSheet("color: white")
        self.channel.setToolTip(None)

    def _try_remove(self) -> None:
        try:
            self.gm.allocated_tacan.remove(self.ct.tacan)
        except ValueError:
            pass
