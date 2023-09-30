from PySide2.QtCore import Signal
from PySide2.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QWidget,
)

from game.radio.radios import RadioFrequency, RadioRange, MHz, kHz
from game.theater import NavalControlPoint
from qt_ui.models import GameModel
from qt_ui.windows.QRadioFrequencyDialog import QRadioFrequencyDialog


class QLink4Widget(QWidget):
    freq_changed = Signal(QWidget)

    def __init__(self, cp: NavalControlPoint, game_model: GameModel) -> None:
        super().__init__()

        self.cp = cp
        self.gm = game_model

        columns = QHBoxLayout()
        self.setLayout(columns)

        self.freq = QLabel(self._get_label_text())
        self.check_freq()
        columns.addWidget(self.freq)
        columns.addStretch()

        self.set_freq_btn = QPushButton("Set LINK4")
        self.set_freq_btn.setProperty("class", "comms")
        self.set_freq_btn.setFixedWidth(100)
        columns.addWidget(self.set_freq_btn)
        self.set_freq_btn.clicked.connect(self.open_freq_dialog)

        self.reset_freq_btn = QPushButton("Reset LINK4")
        self.reset_freq_btn.setProperty("class", "btn-danger comms")
        self.reset_freq_btn.setFixedWidth(100)
        columns.addWidget(self.reset_freq_btn)
        self.reset_freq_btn.clicked.connect(self.reset_freq)

    def _get_label_text(self) -> str:
        freq = "AUTO" if self.cp.link4 is None else self.cp.link4
        return f"<b>LINK4: {freq}</b>"

    def open_freq_dialog(self) -> None:
        ranges = [RadioRange(MHz(225), MHz(400), kHz(25))]
        self.frequency_dialog = QRadioFrequencyDialog(self, self.cp, ranges, link4=True)
        self.frequency_dialog.accepted.connect(self.assign_frequency)
        self.frequency_dialog.show()

    def assign_frequency(self) -> None:
        hz = round(self.frequency_dialog.frequency_input.value() * 10**6)
        self._try_remove()
        self.cp.link4 = RadioFrequency(hertz=hz)
        self.gm.allocated_freqs.append(self.cp.link4)
        self.freq.setText(self._get_label_text())
        self.check_freq()
        self.freq_changed.emit(self)

    def reset_freq(self):
        self._try_remove()
        self.cp.link4 = None
        self.freq.setText(self._get_label_text())
        self._reset_color_and_tooltip()
        self.freq_changed.emit(self)

    def check_freq(self):
        if self.cp.link4 is None:
            return
        if self.gm.allocated_freqs.count(self.cp.link4) > 1:
            self.freq.setStyleSheet("color: orange")
            self.freq.setToolTip(
                "Double booked frequency, verify that this was your intention."
            )
        elif self.gm.allocated_freqs.count(self.cp.link4) == 1:
            self._reset_color_and_tooltip()
        if self.cp.link4 == MHz(243) or self.cp.link4 == MHz(121, 500):
            self.freq.setStyleSheet("color: red")
            self.freq.setToolTip(
                "GUARD Freq. was assigned, verify that this was your intention."
            )

    def _reset_color_and_tooltip(self):
        self.freq.setStyleSheet("color: white")
        self.freq.setToolTip(None)

    def _try_remove(self):
        try:
            self.gm.allocated_freqs.remove(self.cp.link4)
        except ValueError:
            pass
