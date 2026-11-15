from __future__ import annotations

from dataclasses import replace
from typing import Optional

from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QGridLayout,
    QLabel,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from game.utils import INHG_TO_HPA, inches_hg, nautical_miles
from game.weather.atmosphericconditions import AtmosphericConditions
from game.weather.dust import Dust
from game.weather.fog import Fog
from game.weather.weather import Weather

# DCS ground turbulence is in 0.1 m/s; its editor allows 0-6 m/s.
TURBULENCE_LEVELS = {"Light": 8, "Moderate": 22, "Heavy": 40}
FEET_PER_METER = 3.2808399


def turbulence_level(per_10cm: float) -> str:
    if per_10cm < 15:
        return "Light"
    if per_10cm < 30:
        return "Moderate"
    return "Heavy"


class QAtmosphereAdjustmentWidget(QWidget):
    """Temperature, QNH, turbulence, fog and dust.

    Each control starts at the turn's value and hands it back untouched unless
    it was changed, so ACCEPT never re-rolls what you did not edit.
    """

    def __init__(self, weather: Weather, auto_fog: bool) -> None:
        super().__init__()
        self.auto_fog = auto_fog
        atmospheric = weather.atmospheric
        # The edited values, kept in the turn's own units whatever unit is shown.
        self._celsius = float(atmospheric.temperature_celsius)
        self._inches_hg = atmospheric.qnh.inches_hg
        self._temperature_edited = False
        self._qnh_edited = False

        vbox = QVBoxLayout()
        label = QLabel("<h2><b>Air & Visibility:</b></h2>")
        label.setMaximumHeight(75)
        vbox.addWidget(label)
        label = QLabel("<h3><b>Air:</b></h3>")
        label.setMaximumHeight(50)
        vbox.addWidget(label)

        grid = QGridLayout()
        grid.addWidget(QLabel("Temperature"), 0, 0)
        self.temperature = QSpinBox()
        grid.addWidget(self.temperature, 0, 1)
        self.temperature_unit = QComboBox()
        self.temperature_unit.addItems(["°C", "°F"])
        grid.addWidget(self.temperature_unit, 0, 2)

        grid.addWidget(QLabel("QNH"), 1, 0)
        self.qnh = QDoubleSpinBox()
        grid.addWidget(self.qnh, 1, 1)
        self.qnh_unit = QComboBox()
        self.qnh_unit.addItems(["inHg", "hPa"])
        grid.addWidget(self.qnh_unit, 1, 2)

        grid.addWidget(QLabel("Turbulence"), 2, 0)
        self.turbulence = QComboBox()
        for name in TURBULENCE_LEVELS:
            self.turbulence.addItem(name)
        self.turbulence.setCurrentText(
            turbulence_level(atmospheric.turbulence_per_10cm)
        )
        grid.addWidget(self.turbulence, 2, 1, 1, 2)
        vbox.addLayout(grid)

        label = QLabel("<h3><b>Visibility:</b></h3>")
        label.setMaximumHeight(50)
        vbox.addWidget(label)

        grid = QGridLayout()
        self.fog_enabled = QCheckBox("Fog")
        self.fog_enabled.setChecked(weather.fog is not None)
        grid.addWidget(self.fog_enabled, 0, 0)
        grid.addWidget(QLabel("Visibility (NM)"), 1, 0)
        self.fog_visibility = self._visibility_spin(
            weather.fog.visibility.nautical_miles if weather.fog else 1.5
        )
        grid.addWidget(self.fog_visibility, 1, 1)
        grid.addWidget(QLabel("Thickness (ft)"), 2, 0)
        self.fog_thickness = QSpinBox()
        self.fog_thickness.setRange(100, 3300)
        self.fog_thickness.setSingleStep(100)
        self.fog_thickness.setValue(
            round(weather.fog.thickness * FEET_PER_METER) if weather.fog else 800
        )
        grid.addWidget(self.fog_thickness, 2, 1)

        self.dust_enabled = QCheckBox("Dust storm")
        self.dust_enabled.setChecked(weather.dust is not None)
        grid.addWidget(self.dust_enabled, 3, 0)
        grid.addWidget(QLabel("Visibility (NM)"), 4, 0)
        self.dust_visibility = self._visibility_spin(
            weather.dust.visibility.nautical_miles if weather.dust else 1.0
        )
        grid.addWidget(self.dust_visibility, 4, 1)
        vbox.addLayout(grid)

        self.fog_note = QLabel(
            'DCS sets fog itself while "Use DCS\' automatic fog setting" is on, '
            "and allows no dust storm. Turn it off in Settings to set them here."
            if auto_fog
            else "DCS allows fog or a dust storm, not both."
        )
        self.fog_note.setWordWrap(True)
        vbox.addWidget(self.fog_note)
        vbox.addStretch(1)
        self.setLayout(vbox)

        self._show_temperature()
        self._show_qnh()
        self._initial = (
            self.turbulence.currentText(),
            self.fog_visibility.value(),
            self.fog_thickness.value(),
            self.dust_visibility.value(),
        )
        self.temperature.valueChanged.connect(self._on_temperature_edited)
        self.temperature_unit.currentIndexChanged.connect(self._show_temperature)
        self.qnh.valueChanged.connect(self._on_qnh_edited)
        self.qnh_unit.currentIndexChanged.connect(self._show_qnh)
        self.fog_enabled.toggled.connect(self._on_fog_toggled)
        self.dust_enabled.toggled.connect(self._on_dust_toggled)
        self._update_enabled()

    @staticmethod
    def _visibility_spin(value_nm: float) -> QDoubleSpinBox:
        spin = QDoubleSpinBox()
        # 0.2 NM is the DCS editor's 300 m floor for dust.
        spin.setRange(0.2, 10.0)
        spin.setDecimals(1)
        spin.setSingleStep(0.1)
        spin.setValue(round(value_nm, 1))
        return spin

    @property
    def _fahrenheit(self) -> bool:
        return self.temperature_unit.currentIndex() == 1

    @property
    def _hecto_pascals(self) -> bool:
        return self.qnh_unit.currentIndex() == 1

    def _show_temperature(self) -> None:
        # Signals stay blocked so a unit change is not read as an edit.
        self.temperature.blockSignals(True)
        if self._fahrenheit:
            self.temperature.setRange(-40, 130)
            self.temperature.setValue(round(self._celsius * 9 / 5 + 32))
        else:
            self.temperature.setRange(-40, 54)
            self.temperature.setValue(round(self._celsius))
        self.temperature.blockSignals(False)

    def _show_qnh(self) -> None:
        # The DCS editor's QNH range is 720-790 mmHg.
        self.qnh.blockSignals(True)
        if self._hecto_pascals:
            self.qnh.setDecimals(0)
            self.qnh.setSingleStep(1)
            self.qnh.setRange(960, 1053)
            self.qnh.setValue(round(self._inches_hg * INHG_TO_HPA))
        else:
            self.qnh.setDecimals(2)
            self.qnh.setSingleStep(0.01)
            self.qnh.setRange(28.35, 31.10)
            self.qnh.setValue(round(self._inches_hg, 2))
        self.qnh.blockSignals(False)

    def _on_temperature_edited(self, value: int) -> None:
        self._celsius = (value - 32) * 5 / 9 if self._fahrenheit else float(value)
        self._temperature_edited = True

    def _on_qnh_edited(self, value: float) -> None:
        self._inches_hg = value / INHG_TO_HPA if self._hecto_pascals else value
        self._qnh_edited = True

    def _on_fog_toggled(self, checked: bool) -> None:
        if checked:
            self.dust_enabled.setChecked(False)
        self._update_enabled()

    def _on_dust_toggled(self, checked: bool) -> None:
        if checked:
            self.fog_enabled.setChecked(False)
        self._update_enabled()

    def _update_enabled(self) -> None:
        editable = not self.auto_fog
        self.fog_enabled.setEnabled(editable)
        self.dust_enabled.setEnabled(editable)
        self.fog_visibility.setEnabled(editable and self.fog_enabled.isChecked())
        self.fog_thickness.setEnabled(editable and self.fog_enabled.isChecked())
        self.dust_visibility.setEnabled(editable and self.dust_enabled.isChecked())

    def atmospheric(self, original: AtmosphericConditions) -> AtmosphericConditions:
        result = replace(original)
        if self._temperature_edited:
            result.temperature_celsius = round(self._celsius, 1)
        if self._qnh_edited:
            result.qnh = inches_hg(self._inches_hg)
        if self.turbulence.currentText() != self._initial[0]:
            result.turbulence_per_10cm = TURBULENCE_LEVELS[
                self.turbulence.currentText()
            ]
        return result

    def fog(self, original: Optional[Fog]) -> Optional[Fog]:
        if self.auto_fog:
            return original
        if not self.fog_enabled.isChecked():
            return None
        _, visibility, thickness, _ = self._initial
        if (
            original is not None
            and self.fog_visibility.value() == visibility
            and self.fog_thickness.value() == thickness
        ):
            return original
        return Fog(
            visibility=nautical_miles(self.fog_visibility.value()),
            thickness=round(self.fog_thickness.value() / FEET_PER_METER),
        )

    def dust(self, original: Optional[Dust]) -> Optional[Dust]:
        if self.auto_fog:
            return original
        if not self.dust_enabled.isChecked():
            return None
        if original is not None and self.dust_visibility.value() == self._initial[3]:
            return original
        return Dust(visibility=nautical_miles(self.dust_visibility.value()))
