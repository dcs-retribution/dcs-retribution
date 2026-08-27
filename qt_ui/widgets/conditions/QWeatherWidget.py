from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QToolButton,
    QVBoxLayout,
)
from dcs.weather import CloudPreset, Weather as PydcsWeather

from game.timeofday import TimeOfDay
from game.utils import meters, mps
from game.weather.atmosxliveweather import LiveWeather
from game.weather.conditions import Conditions
from qt_ui import uiconstants as CONST


class QWeatherWidget(QGroupBox):
    """
    UI Component to display current weather forecast
    """

    #: The player asked for a fresh observation. Whoever owns the game does the work.
    refresh_requested = Signal()

    turn = None
    conditions = None

    def __init__(self):
        super(QWeatherWidget, self).__init__("")
        self.setProperty("style", "QWeatherWidget")

        self.icons = {
            TimeOfDay.Dawn: CONST.ICONS["Dawn"],
            TimeOfDay.Day: CONST.ICONS["Day"],
            TimeOfDay.Dusk: CONST.ICONS["Dusk"],
            TimeOfDay.Night: CONST.ICONS["Night"],
        }

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.makeWeatherIcon()
        self.makeCloudRainFogWidget()
        self.makeWindsWidget()
        self.makeRefreshButton()

    def makeWeatherIcon(self):
        """Makes the Weather Icon Widget"""
        self.weather_icon = QLabel()
        self.weather_icon.setPixmap(self.icons[TimeOfDay.Dawn])
        self.layout.addWidget(self.weather_icon)

    def makeCloudRainFogWidget(self):
        """Makes the Cloud, Rain, Fog Widget"""
        self.textLayout = QVBoxLayout()
        self.layout.addLayout(self.textLayout)

        self.forecastClouds = self.makeLabel()
        self.textLayout.addWidget(self.forecastClouds)

        self.forecastRain = self.makeLabel()
        self.textLayout.addWidget(self.forecastRain)

        self.forecastFog = self.makeLabel()
        self.textLayout.addWidget(self.forecastFog)

    def makeWindsWidget(self):
        """Factory for the winds widget."""
        windsLayout = QGridLayout()
        self.layout.addLayout(windsLayout)

        windsLayout.addWidget(self.makeIcon(CONST.ICONS["Weather_winds"]), 0, 0, 3, 1)

        windsLayout.addWidget(self.makeLabel("At GL"), 0, 1)
        windsLayout.addWidget(self.makeLabel("At FL08"), 1, 1)
        windsLayout.addWidget(self.makeLabel("At FL26"), 2, 1)

        self.windGLSpeedLabel = self.makeLabel("0kts")
        self.windGLDirLabel = self.makeLabel("0º")
        windsLayout.addWidget(self.windGLSpeedLabel, 0, 2)
        windsLayout.addWidget(self.windGLDirLabel, 0, 3)

        self.windFL08SpeedLabel = self.makeLabel("0kts")
        self.windFL08DirLabel = self.makeLabel("0º")
        windsLayout.addWidget(self.windFL08SpeedLabel, 1, 2)
        windsLayout.addWidget(self.windFL08DirLabel, 1, 3)

        self.windFL26SpeedLabel = self.makeLabel("0kts")
        self.windFL26DirLabel = self.makeLabel("0º")
        windsLayout.addWidget(self.windFL26SpeedLabel, 2, 2)
        windsLayout.addWidget(self.windFL26DirLabel, 2, 3)

    def makeRefreshButton(self) -> None:
        """A button to fetch the observation again, hidden unless that means anything."""
        self.refresh_button = QToolButton()
        self.refresh_button.setText("⟳")
        self.refresh_button.setToolTip(
            "Fetch the current METAR again and use it for this turn."
        )
        self.refresh_button.setAutoRaise(True)
        # The glyph renders at the panel's small label size otherwise, which is far
        # too fiddly a target for a button you press between planning and take-off.
        font = self.refresh_button.font()
        font.setPointSize(20)
        self.refresh_button.setFont(font)
        self.refresh_button.setFixedSize(QSize(40, 40))
        self.refresh_button.clicked.connect(self.refresh_requested.emit)
        self.refresh_button.hide()
        self.layout.addWidget(
            self.refresh_button, alignment=Qt.AlignmentFlag.AlignVCenter
        )

    def makeLabel(self, text: str = "") -> QLabel:
        """Shorthand to generate a QLabel with widget standard style

        :arg pixmap QPixmap for the icon.
        """
        label = QLabel(text)
        label.setProperty("style", "text-sm")

        return label

    def makeIcon(self, pixmap: QPixmap) -> QLabel:
        """Shorthand to generate a QIcon with pixmap.

        :arg pixmap QPixmap for the icon.
        """
        icon = QLabel()
        icon.setPixmap(pixmap)

        return icon

    def setCurrentTurn(
        self, turn: int, conditions: Conditions, can_refresh: bool = False
    ) -> None:
        """Sets the turn information display.

        :arg turn Current turn number.
        :arg conditions Current time and weather conditions.
        :arg can_refresh Whether live weather is on, so a refresh is worth offering.
        """
        self.turn = turn
        self.conditions = conditions

        self.update_forecast()
        self.updateWinds()
        self.refresh_button.setVisible(can_refresh)
        self.setToolTip(self.weather_details())

    def weather_details(self) -> str:
        """Everything the widget has room to show only three words of."""
        weather = self.conditions.weather
        rows: list[tuple[str, str]] = []

        if isinstance(weather, LiveWeather):
            rows.append(("Source", f"Live METAR &mdash; {weather.station}"))
        else:
            rows.append(("Source", "Generated forecast"))

        atmospheric = weather.atmospheric
        rows.append(("Temperature", f"{atmospheric.temperature_celsius:.0f} &deg;C"))
        rows.append(
            (
                "QNH",
                f"{atmospheric.qnh.inches_hg:.2f} inHg / "
                f"{atmospheric.qnh.mm_hg:.0f} mmHg / "
                f"{atmospheric.qnh.hecto_pascals:.0f} hPa",
            )
        )
        rows.append(("Turbulence", f"{atmospheric.turbulence_per_10cm:.1f} per 10cm"))

        clouds = weather.clouds
        if clouds is None:
            rows.append(("Clouds", "Clear"))
        else:
            if clouds.preset is not None:
                # A preset's description is two lines: a name after "##", then the
                # METAR-style layer breakdown. The widget shows the first; the second
                # never fitted anywhere until there was a tooltip to put it in.
                lines = clouds.preset.description.splitlines()
                rows.append(("Cloud preset", lines[0].split("##")[-1].strip()))
                for line in lines[1:]:
                    if line.strip():
                        rows.append(("Layers", line.strip()))
            rows.append(("Cloud base", self.height(clouds.base)))
            if clouds.thickness:
                rows.append(("Cloud thickness", self.height(clouds.thickness)))
            if clouds.density:
                rows.append(("Cloud density", f"{clouds.density} of 10"))
            if clouds.precipitation is not PydcsWeather.Preceptions.None_:
                rows.append(("Precipitation", clouds.precipitation.name))

        if weather.fog is None:
            rows.append(("Fog", "None"))
        else:
            rows.append(
                (
                    "Fog",
                    f"{weather.fog.visibility.nautical_miles:.1f}nm visibility, "
                    f"{self.height(weather.fog.thickness)} thick",
                )
            )

        if isinstance(weather, LiveWeather):
            visibility = weather.vdata.get("visibility")
            if isinstance(visibility, dict) and "distance" in visibility:
                distance = meters(float(visibility["distance"]))
                rows.append(("Visibility", f"{distance.nautical_miles:.0f}nm"))

        for label, wind in (
            ("Wind GL", weather.wind.at_0m),
            ("Wind FL08", weather.wind.at_2000m),
            ("Wind FL26", weather.wind.at_8000m),
        ):
            speed = mps(wind.speed or 0)
            rows.append(
                (
                    label,
                    f"{str(wind.direction or 0).rjust(3, '0')}&deg; at "
                    f"{speed.knots:.0f}kts",
                )
            )

        cells = "".join(
            f"<tr><td><b>{label}</b>&nbsp;&nbsp;</td><td>{value}</td></tr>"
            for label, value in rows
        )
        return f"<table>{cells}</table>"

    @staticmethod
    def height(value: int) -> str:
        return f"{value}m / {int(meters(value).feet)}ft"

    def updateWinds(self):
        """Updates the UI with the current conditions wind info."""
        windGlSpeed = mps(self.conditions.weather.wind.at_0m.speed or 0)
        windGlDir = str(self.conditions.weather.wind.at_0m.direction or 0).rjust(3, "0")
        self.windGLSpeedLabel.setText(f"{int(windGlSpeed.knots)}kts")
        self.windGLDirLabel.setText(f"{windGlDir}º")

        windFL08Speed = mps(self.conditions.weather.wind.at_2000m.speed or 0)
        windFL08Dir = str(self.conditions.weather.wind.at_2000m.direction or 0).rjust(
            3, "0"
        )
        self.windFL08SpeedLabel.setText(f"{int(windFL08Speed.knots)}kts")
        self.windFL08DirLabel.setText(f"{windFL08Dir}º")

        windFL26Speed = mps(self.conditions.weather.wind.at_8000m.speed or 0)
        windFL26Dir = str(self.conditions.weather.wind.at_8000m.direction or 0).rjust(
            3, "0"
        )
        self.windFL26SpeedLabel.setText(f"{int(windFL26Speed.knots)}kts")
        self.windFL26DirLabel.setText(f"{windFL26Dir}º")

    def update_forecast_from_preset(self, preset: CloudPreset) -> None:
        self.forecastFog.setText("No fog")
        if "Rain" in preset.name:
            self.forecastRain.setText("Rain")
            self.update_forecast_icons("rain")
        else:
            self.forecastRain.setText("No rain")
            self.update_forecast_icons("partly-cloudy")

        # We get a description like the following for the cloud preset.
        #
        # 09 ##Two Layer Broken/Scattered \nMETAR:BKN 7.5/10 SCT 20/22 FEW41
        #
        # The second line is probably interesting but doesn't fit into the widget
        # currently, so for now just extract the first line.
        self.forecastClouds.setText(preset.description.splitlines()[0].split("##")[1])

    def update_forecast(self):
        """Updates the Forecast Text and icon with the current conditions wind info."""
        if (
            self.conditions.weather.clouds
            and self.conditions.weather.clouds.preset is not None
        ):
            self.update_forecast_from_preset(self.conditions.weather.clouds.preset)
            return

        if self.conditions.weather.clouds is None:
            cloud_density = 0
            precipitation = None
        else:
            cloud_density = self.conditions.weather.clouds.density
            precipitation = self.conditions.weather.clouds.precipitation

        if not cloud_density:
            self.forecastClouds.setText("Clear")
            weather_type = "clear"
        elif cloud_density < 3:
            self.forecastClouds.setText("Partly Cloudy")
            weather_type = "partly-cloudy"
        elif cloud_density < 5:
            self.forecastClouds.setText("Mostly Cloudy")
            weather_type = "partly-cloudy"
        else:
            self.forecastClouds.setText("Totally Cloudy")
            weather_type = "partly-cloudy"

        if precipitation == PydcsWeather.Preceptions.Rain:
            self.forecastRain.setText("Rain")
            weather_type = "rain"
        elif precipitation == PydcsWeather.Preceptions.Thunderstorm:
            self.forecastRain.setText("Thunderstorm")
            weather_type = "thunderstorm"
        else:
            self.forecastRain.setText("No rain")

        if not self.conditions.weather.fog is not None:
            self.forecastFog.setText("No fog")
        else:
            visibility = round(self.conditions.weather.fog.visibility.nautical_miles, 1)
            self.forecastFog.setText(f"Fog vis: {visibility}nm")
            if cloud_density > 1:
                weather_type = "cloudy-fog"
            else:
                weather_type = "fog"

        self.update_forecast_icons(weather_type)

    def update_forecast_icons(self, weather_type: str) -> None:
        time = "night" if self.conditions.time_of_day == TimeOfDay.Night else "day"
        icon_key = f"Weather_{time}-{weather_type}"
        icon = CONST.ICONS.get(icon_key) or CONST.ICONS["Weather_night-partly-cloudy"]
        self.weather_icon.setPixmap(icon)
