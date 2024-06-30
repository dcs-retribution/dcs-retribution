from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QSlider, QSpinBox, QComboBox
from dcs.weather import CloudPreset


class DcsCloudBaseSelector(QHBoxLayout):
    M2FT_FACTOR = 3.2808399

    def __init__(self, preset: Optional[CloudPreset]) -> None:
        super().__init__()
        self.preset = preset
        self.unit_changing = False

        self.label = QLabel("Cloud Base: ")
        self.addWidget(self.label)

        self.base = QSlider(Qt.Orientation.Horizontal)
        self.base.setValue(round(self.max_base - (self.max_base - self.min_base) / 2))
        self.base.valueChanged.connect(self.on_slider_change)
        self.addWidget(self.base, 1)

        self.base_spinner = QSpinBox()
        self.base_spinner.setValue(self.base.value())
        self.base_spinner.setFixedWidth(75)
        self.base_spinner.setSingleStep(100)
        self.base_spinner.valueChanged.connect(self.update_slider)
        self.addWidget(self.base_spinner, 1)

        self.unit = QComboBox()
        self.unit.insertItems(0, ["m", "ft"])
        self.unit.currentIndexChanged.connect(self.on_unit_change)
        self.unit.setCurrentIndex(1)
        self.addWidget(self.unit)

        self.update_bounds()

    @property
    def min_base(self) -> int:
        return self.preset.min_base if self.preset else 300

    @property
    def max_base(self) -> int:
        return self.preset.max_base if self.preset else 5000

    def update_bounds(self) -> None:
        self.base.setRange(self.min_base, self.max_base)
        index = self.unit.currentIndex()
        if index == 0:
            self.base_spinner.setRange(self.min_base, self.max_base)
        elif index == 1:
            self.base_spinner.setRange(
                self.m2ft(self.min_base), self.m2ft(self.max_base)
            )

    def on_slider_change(self, value: int) -> None:
        if self.unit.currentIndex() == 0:
            self.base_spinner.setValue(value)
        elif self.unit.currentIndex() == 1 and not self.unit_changing:
            self.base_spinner.setValue(self.m2ft(value))

    def update_slider(self, value: int) -> None:
        if self.unit_changing:
            return
        if self.unit.currentIndex() == 0:
            self.base.setValue(value)
        elif self.unit.currentIndex() == 1:
            self.unit_changing = True
            self.base.setValue(self.ft2m(value))
            self.unit_changing = False

    def on_unit_change(self, index: int) -> None:
        self.unit_changing = True
        if index == 0:
            self.base_spinner.setRange(self.min_base, self.max_base)
            self.base_spinner.setValue(self.base.value())
        elif index == 1:
            self.base_spinner.setRange(
                self.m2ft(self.min_base), self.m2ft(self.max_base)
            )
            self.base_spinner.setValue(self.m2ft(self.base.value()))
        self.unit_changing = False

    def m2ft(self, value: int) -> int:
        return round(value * self.M2FT_FACTOR)

    def ft2m(self, value: int) -> int:
        return round(value / self.M2FT_FACTOR)
