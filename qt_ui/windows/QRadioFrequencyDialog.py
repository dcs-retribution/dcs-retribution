from typing import Optional, Iterable

from PySide6.QtCore import Qt, QLocale
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QDialog,
    QPushButton,
    QLabel,
    QHBoxLayout,
    QDoubleSpinBox,
    QComboBox,
)

from game.radio.Link4Container import Link4Container
from game.radio.RadioFrequencyContainer import RadioFrequencyContainer
from game.radio.radios import RadioRange, kHz, MHz
from qt_ui.uiconstants import EVENT_ICONS


class QFrequencySpinbox(QDoubleSpinBox):
    def __init__(self, ranges: Iterable[RadioRange]) -> None:
        super().__init__()
        self.setLocale(QLocale(QLocale.Language.English))
        self.setDecimals(3)
        self.ranges = list(ranges)
        first = True
        for r in ranges:
            if r.minimum.mhz < self.minimum():
                self.setMinimum(r.minimum.mhz)
            if self.maximum() < r.maximum.mhz:
                self.setMaximum(r.maximum.mhz)
            if first:
                self.setSingleStep(r.step.mhz)
                self.setValue(r.minimum.mhz)
                first = False

    def correct_value(self, value: float) -> None:
        for r in self.ranges:
            if r.maximum.mhz == value:
                self.setValue(value - r.step.mhz)
                return

    def stepBy(self, steps: int) -> None:
        new_value = self.check_value(self.value() + (steps * self.singleStep()))
        self.setValue(new_value)

    def check_value(self, value: float) -> float:
        for r in self.ranges:
            if r.minimum.mhz <= value < r.maximum.mhz:
                self.setSingleStep(r.step.mhz)
                return value
        minimums = [m for m in set(r.minimum.mhz for r in self.ranges) if m > value]
        maximums = [m for m in set(r.maximum.mhz for r in self.ranges) if m <= value]
        if not minimums or not maximums:
            return self.value()
        smallest_min = min(minimums)
        largest_max = max(maximums)
        if largest_max <= value < smallest_min:
            if value < self.value():
                rs = [r for r in self.ranges if r.maximum.mhz == largest_max]
                value = largest_max - rs[0].step.mhz
            else:
                rs = [r for r in self.ranges if r.minimum.mhz == smallest_min]
                value = smallest_min
            r = rs[0]
            self.setSingleStep(r.step.mhz)
            return value
        raise RuntimeError()


class QFrequencyModulationBox(QComboBox):
    def __init__(self, ranges: Iterable[RadioRange], freq: float) -> None:
        super().__init__()
        self.setMaximumWidth(60)
        self.ranges = list(ranges)
        self.update_modulations(freq)

    def update_modulations(self, freq: float) -> None:
        self.modulations = set(
            r.modulation for r in self.ranges if r.minimum.mhz <= freq < r.maximum.mhz
        )
        self.setEnabled(len(self.modulations) > 1)
        self.clear()
        for i, m in enumerate(sorted(self.modulations, key=lambda x: x.name)):
            self.addItem(QIcon(), m.name, m)


class QRadioFrequencyDialog(QDialog):
    def __init__(
        self,
        parent=None,
        container: Optional[RadioFrequencyContainer] = None,
        ranges: Iterable[RadioRange] = tuple([RadioRange(MHz(225), MHz(400), kHz(25))]),
        link4: bool = False,
    ) -> None:
        super().__init__(parent=parent)
        self.container = container
        self.setMinimumWidth(400)

        # Make dialog modal to prevent background windows to close unexpectedly.
        self.setModal(True)

        self.setWindowTitle("Assign frequency")
        self.setWindowIcon(EVENT_ICONS["strike"])

        layout = QHBoxLayout()

        self.frequency_label = QLabel("FREQ (MHz):")
        self.frequency_input = QFrequencySpinbox(ranges)
        self.frequency_modulation = QFrequencyModulationBox(
            ranges, self.frequency_input.value()
        )
        self.frequency_input.valueChanged.connect(
            self.frequency_modulation.update_modulations
        )
        self.frequency_input.valueChanged.connect(self.frequency_input.correct_value)

        layout.addWidget(self.frequency_label)
        layout.addWidget(self.frequency_input)
        layout.addWidget(self.frequency_modulation)

        self.create_button = QPushButton("Save")
        self.create_button.clicked.connect(self.accept)
        layout.addWidget(self.create_button, alignment=Qt.AlignRight)

        self.setLayout(layout)

        if link4 and isinstance(container, Link4Container):
            if container.link4:
                self.frequency_input.setValue(container.link4.mhz)
        elif container.frequency:
            self.frequency_input.setValue(container.frequency.mhz)
