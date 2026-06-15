from PySide6.QtWidgets import (
    QLabel,
    QHBoxLayout,
    QComboBox,
    QWidget,
    QVBoxLayout,
    QSpinBox,
    QGridLayout,
)
from dcs.cloud_presets import CLOUD_PRESETS

from game.weather.weather import ClearSkies, Cloudy, Raining, Thunderstorm
from qt_ui.widgets.conditions.DcsCloudBaseSelector import DcsCloudBaseSelector
from qt_ui.widgets.conditions.DcsCloudDensitySelector import DcsCloudDensitySelector
from qt_ui.widgets.conditions.DcsCloudThicknessSelector import DcsCloudThicknessSelector
from qt_ui.widgets.conditions.DcsPrecipitationSelector import DcsPrecipitationSelector
from qt_ui.widgets.conditions.QWeatherWidget import QWeatherWidget


class QWeatherAdjustmentWidget(QWidget):
    def __init__(self, weather: QWeatherWidget) -> None:
        super().__init__()
        self.weather = weather
        self.init_ui()

    def init_ui(self) -> None:
        weather = self.weather.conditions.weather

        vbox = QVBoxLayout()
        label = QLabel("<h2><b>Weather:</b></h2>")
        label.setMaximumHeight(75)
        vbox.addWidget(label)

        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("Type"))
        self.type_selector = QComboBox()
        for text, w_type in [
            ("Clear", ClearSkies),
            ("Clouds", Cloudy),
            ("Rain", Raining),
            ("Thunderstorm", Thunderstorm),
        ]:
            self.type_selector.addItem(text, w_type)
            if isinstance(weather, w_type):
                self.type_selector.setCurrentText(text)
        self.type_selector.currentIndexChanged.connect(self.update_ui_for_type)
        hbox.addWidget(self.type_selector)
        vbox.addLayout(hbox)

        label = QLabel("<h3><b>Clouds:</b></h3>")
        label.setMaximumHeight(50)
        vbox.addWidget(label)

        clouds = weather.clouds

        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("Preset"))
        self.preset_selector = QComboBox()
        for _, preset in CLOUD_PRESETS.items():
            self.preset_selector.addItem(preset.value.ui_name, preset.value)
        self.preset_selector.addItem("Custom", None)
        self.preset_selector.setCurrentText(
            clouds.preset.ui_name if clouds and clouds.preset else "Custom"
        )
        self.preset_selector.currentIndexChanged.connect(self.update_ui)
        hbox.addWidget(self.preset_selector)
        vbox.addLayout(hbox)

        self.cloud_base = DcsCloudBaseSelector(clouds)
        vbox.addLayout(self.cloud_base)

        self.cloud_thickness = DcsCloudThicknessSelector(clouds)
        vbox.addLayout(self.cloud_thickness)

        self.cloud_density = DcsCloudDensitySelector(clouds)
        vbox.addLayout(self.cloud_density)

        self.precipitation = DcsPrecipitationSelector(clouds)
        vbox.addLayout(self.precipitation)

        label = QLabel("<h3><b>Wind:</b></h3>")
        label.setMaximumHeight(50)
        vbox.addWidget(label)

        wind = weather.wind
        grid = QGridLayout()
        grid.addWidget(QLabel(""), 0, 0)
        grid.addWidget(QLabel("Speed (kts)"), 0, 1)
        grid.addWidget(QLabel("Dir (°)"), 0, 2)

        def _make_speed_spin(current_mps: float) -> QSpinBox:
            sb = QSpinBox()
            sb.setRange(0, 200)
            sb.setValue(round(current_mps * 1.944))  # m/s → knots
            return sb

        def _make_dir_spin(current_deg: int) -> QSpinBox:
            sb = QSpinBox()
            sb.setRange(0, 359)
            sb.setWrapping(True)
            sb.setValue(current_deg or 0)
            return sb

        grid.addWidget(QLabel("Ground"), 1, 0)
        self.wind_gl_speed = _make_speed_spin(wind.at_0m.speed or 0)
        self.wind_gl_dir = _make_dir_spin(wind.at_0m.direction or 0)
        grid.addWidget(self.wind_gl_speed, 1, 1)
        grid.addWidget(self.wind_gl_dir, 1, 2)

        grid.addWidget(QLabel("FL080 (2000m)"), 2, 0)
        self.wind_fl08_speed = _make_speed_spin(wind.at_2000m.speed or 0)
        self.wind_fl08_dir = _make_dir_spin(wind.at_2000m.direction or 0)
        grid.addWidget(self.wind_fl08_speed, 2, 1)
        grid.addWidget(self.wind_fl08_dir, 2, 2)

        grid.addWidget(QLabel("FL260 (8000m)"), 3, 0)
        self.wind_fl26_speed = _make_speed_spin(wind.at_8000m.speed or 0)
        self.wind_fl26_dir = _make_dir_spin(wind.at_8000m.direction or 0)
        grid.addWidget(self.wind_fl26_speed, 3, 1)
        grid.addWidget(self.wind_fl26_dir, 3, 2)

        vbox.addLayout(grid)

        self.setLayout(vbox)

        self.update_ui_for_type()

    def update_ui_for_type(self) -> None:
        if self.type_selector.currentData() in [ClearSkies, Thunderstorm]:
            self.preset_selector.setCurrentText("Custom")
            self.preset_selector.setDisabled(True)
        else:
            self.preset_selector.setDisabled(False)

        self.update_ui()

    def update_ui(self) -> None:
        preset = self.preset_selector.currentData()
        self.cloud_base.preset = preset
        self.cloud_base.update_bounds()
        self.cloud_thickness.update_ui(preset)
        self.cloud_density.update_ui(preset)
        self.precipitation.update_ui(preset)
