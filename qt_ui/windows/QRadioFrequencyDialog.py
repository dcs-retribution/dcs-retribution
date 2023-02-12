from typing import Optional

from PySide2.QtCore import Qt, QLocale
from PySide2.QtWidgets import (
    QDialog,
    QPushButton,
    QLabel,
    QHBoxLayout,
    QDoubleSpinBox,
)

from game.radio.Link4Container import Link4Container
from game.radio.RadioFrequencyContainer import RadioFrequencyContainer
from game.radio.radios import RadioRange, kHz, MHz
from qt_ui.uiconstants import EVENT_ICONS


class QRadioFrequencyDialog(QDialog):
    def __init__(
        self,
        parent=None,
        container: Optional[RadioFrequencyContainer] = None,
        range: RadioRange = RadioRange(MHz(225), MHz(400), kHz(25)),
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
        self.frequency_input = QDoubleSpinBox()
        self.frequency_input.setRange(
            range.minimum.mhz, range.maximum.mhz - range.step.mhz
        )
        self.frequency_input.setSingleStep(range.step.mhz)
        self.frequency_input.setDecimals(3)
        self.frequency_input.setLocale(QLocale(QLocale.Language.English))
        if range.minimum.mhz <= 225.0 < range.maximum.mhz:
            self.frequency_input.setValue(225.0)
        else:
            mid = range.minimum.mhz + (range.maximum.mhz - range.minimum.mhz) / 2
            self.frequency_input.setValue(mid)
        layout.addWidget(self.frequency_label)
        layout.addWidget(self.frequency_input)

        self.create_button = QPushButton("Save")
        self.create_button.clicked.connect(self.accept)
        layout.addWidget(self.create_button, alignment=Qt.AlignRight)

        self.setLayout(layout)

        if link4 and isinstance(container, Link4Container):
            if container.link4:
                self.frequency_input.setValue(container.link4.mhz)
        elif container.frequency:
            self.frequency_input.setValue(container.frequency.mhz)
