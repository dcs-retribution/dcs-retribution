from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QWidget,
)

from game.radio.ICLSContainer import ICLSContainer
from qt_ui.models import GameModel
from qt_ui.windows.QICLSDialog import QICLSDialog


class QICLSWidget(QWidget):
    def __init__(self, container: ICLSContainer, game_model: GameModel) -> None:
        super().__init__()

        self.ct = container
        self.gm = game_model

        columns = QHBoxLayout()
        self.setLayout(columns)

        self.channel = QLabel(self._get_label_text())
        self.check_channel()
        columns.addWidget(self.channel)
        columns.addStretch()

        self.set_icls_btn = QPushButton("Set ICLS")
        self.set_icls_btn.setProperty("class", "comms")
        self.set_icls_btn.setFixedWidth(100)
        columns.addWidget(self.set_icls_btn)
        self.set_icls_btn.clicked.connect(self.open_icls_dialog)

        self.reset_icls_btn = QPushButton("Reset ICLS")
        self.reset_icls_btn.setProperty("class", "btn-danger comms")
        self.reset_icls_btn.setFixedWidth(100)
        columns.addWidget(self.reset_icls_btn)
        self.reset_icls_btn.clicked.connect(self.reset_icls)

    def _get_label_text(self) -> str:
        c = "AUTO" if self.ct.icls_channel is None else self.ct.icls_channel
        cs = self.ct.icls_name
        cs = "" if cs is None else f" ({cs})"
        return f"<b>ICLS: {c}{cs}</b>"

    def open_icls_dialog(self) -> None:
        self.icls_dialog = QICLSDialog(self, self.ct)
        self.icls_dialog.accepted.connect(self.assign_icls)
        self.icls_dialog.show()

    def assign_icls(self) -> None:
        self._try_remove()
        self.ct.icls_channel = self.icls_dialog.icls_input.value()
        self.gm.allocated_icls.append(self.ct.icls_channel)
        if cs := self.icls_dialog.callsign_input.text():
            self.ct.icls_name = cs.upper()
        self.channel.setText(self._get_label_text())
        self.check_channel()

    def reset_icls(self) -> None:
        self._try_remove()
        self.ct.icls_channel = None
        self.ct.icls_name = None
        self.channel.setText(self._get_label_text())
        self._reset_color_and_tooltip()

    def check_channel(self) -> None:
        if self.ct.icls_channel is None:
            return
        if self.gm.allocated_icls.count(self.ct.icls_channel) > 1:
            self.channel.setStyleSheet("color: orange")
            self.channel.setToolTip(
                "Double booked ICLS channel, verify that this was your intention."
            )
        elif self.gm.allocated_icls.count(self.ct.icls_channel) == 1:
            self._reset_color_and_tooltip()

    def _reset_color_and_tooltip(self):
        self.channel.setStyleSheet("color: white")
        self.channel.setToolTip(None)

    def _try_remove(self) -> None:
        try:
            self.gm.allocated_icls.remove(self.ct.icls_channel)
        except ValueError:
            pass
