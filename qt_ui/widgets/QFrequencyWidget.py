from PySide2.QtCore import Signal
from PySide2.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QWidget,
)

from game.ato import Flight
from game.radio.RadioFrequencyContainer import RadioFrequencyContainer
from game.radio.radios import RadioFrequency, RadioRange, MHz, kHz
from qt_ui.models import GameModel
from qt_ui.windows.QRadioFrequencyDialog import QRadioFrequencyDialog


class QFrequencyWidget(QWidget):
    freq_changed = Signal(QWidget)

    def __init__(
        self, container: RadioFrequencyContainer, game_model: GameModel
    ) -> None:
        super().__init__()

        self.ct = container
        self.gm = game_model

        columns = QHBoxLayout()
        self.setLayout(columns)

        self.freq = QLabel(self._get_label_text())
        self.check_freq()
        columns.addWidget(self.freq)
        columns.addStretch()

        self.set_freq_btn = QPushButton("Set FREQ")
        self.set_freq_btn.setProperty("class", "comms")
        self.set_freq_btn.setFixedWidth(100)
        columns.addWidget(self.set_freq_btn)
        self.set_freq_btn.clicked.connect(self.open_freq_dialog)

        self.reset_freq_btn = QPushButton("Reset FREQ")
        self.reset_freq_btn.setProperty("class", "btn-danger comms")
        self.reset_freq_btn.setFixedWidth(100)
        columns.addWidget(self.reset_freq_btn)
        self.reset_freq_btn.clicked.connect(self.reset_freq)

    def _get_label_text(self) -> str:
        freq = "AUTO" if self.ct.frequency is None else self.ct.frequency
        return f"<b>FREQ: {freq}</b>"

    def open_freq_dialog(self) -> None:
        ranges = [RadioRange(MHz(30), MHz(400), kHz(25))]
        if isinstance(self.ct, Flight):
            if self.ct.unit_type.intra_flight_radio is not None:
                ranges = self.ct.unit_type.intra_flight_radio.ranges
        self.frequency_dialog = QRadioFrequencyDialog(self, self.ct, ranges)
        self.frequency_dialog.accepted.connect(self.assign_frequency)
        self.frequency_dialog.show()

    def assign_frequency(self) -> None:
        hz = round(self.frequency_dialog.frequency_input.value() * 10**6)
        self._try_remove()
        mod = self.frequency_dialog.frequency_modulation.currentData()
        self.ct.frequency = RadioFrequency(hertz=hz, modulation=mod)
        self.gm.allocated_freqs.append(self.ct.frequency)
        self.freq.setText(self._get_label_text())
        self.check_freq()
        self.freq_changed.emit(self)

    def reset_freq(self) -> None:
        self._try_remove()
        self.ct.frequency = None
        self.freq.setText(self._get_label_text())
        self._reset_color_and_tooltip()
        self.freq_changed.emit(self)

    def check_freq(self) -> None:
        if self.ct.frequency is None:
            return
        if self.gm.allocated_freqs.count(self.ct.frequency) > 1:
            self.freq.setStyleSheet("color: orange")
            self.freq.setToolTip(
                "Double booked frequency, verify that this was your intention."
            )
        elif self.gm.allocated_freqs.count(self.ct.frequency) == 1:
            self._reset_color_and_tooltip()
        if self.ct.frequency == MHz(243) or self.ct.frequency == MHz(121, 500):
            self.freq.setStyleSheet("color: red")
            self.freq.setToolTip(
                "GUARD Freq. was assigned, verify that this was your intention."
            )

    def _reset_color_and_tooltip(self):
        self.freq.setStyleSheet("color: white")
        self.freq.setToolTip(None)

    def _try_remove(self) -> None:
        try:
            self.gm.allocated_freqs.remove(self.ct.frequency)
        except ValueError:
            pass
