"""Generates kneeboard pages relevant to the player's mission.

The player kneeboard includes the following information:

* Airfield (departure, arrival, divert) info.
* Flight plan (waypoint numbers, names, altitudes).
* Comm channels.
* AWACS info.
* Tanker info.
* JTAC info.

Things we should add:

* Flight plan ToT and fuel ladder (current have neither available).
* Support for planning an arrival/divert airfield separate from departure.
* Mission package infrastructure to include information about the larger
  mission, i.e. information about the escort flight for a strike package.
* Target information. Steerpoints, preplanned objectives, ToT, etc.

For multiplayer missions, a kneeboard will be generated per flight.
https://forums.eagle.ru/showthread.php?t=206360 claims that kneeboard pages can
only be added per airframe, so PvP missions where each side have the same
aircraft will be able to see the enemy's kneeboard for the same airframe.
"""
import datetime
import math
import textwrap
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterator, List, Optional, TYPE_CHECKING, Tuple

from PIL import Image, ImageDraw, ImageFont
from dcs.mission import Mission
from dcs.planes import F_15ESE
from suntime import Sun, SunTimeException  # type: ignore
from tabulate import tabulate

from game.ato.flighttype import FlightType
from game.ato.flightwaypoint import FlightWaypoint
from game.ato.flightwaypointtype import FlightWaypointType
from game.data.alic import AlicCodes
from game.dcs.aircrafttype import AircraftType
from game.radio.radios import RadioFrequency
from game.runways import RunwayData
from game.theater import TheaterGroundObject, TheaterUnit
from game.theater.bullseye import Bullseye
from game.utils import Distance, UnitSystem, meters, mps, pounds
from game.weather.weather import Weather
from .aircraft.flightdata import FlightData
from .briefinggenerator import CommInfo, JtacInfo, MissionInfoGenerator
from .missiondata import AwacsInfo, TankerInfo
from ..persistency import kneeboards_dir

if TYPE_CHECKING:
    from game import Game


class KneeboardPageWriter:
    """Creates kneeboard images."""

    def __init__(
        self, page_margin: int = 24, line_spacing: int = 12, dark_theme: bool = False
    ) -> None:
        if dark_theme:
            self.foreground_fill = (215, 200, 200)
            self.background_fill = (10, 5, 5)
        else:
            self.foreground_fill = (15, 15, 15)
            self.background_fill = (255, 252, 252)
        self.image_size = (960, 1080)
        self.image = Image.new("RGB", self.image_size, self.background_fill)
        # These font sizes create a relatively full page for current sorties. If
        # we start generating more complicated flight plans, or start including
        # more information in the comm ladder (the latter of which we should
        # probably do), we'll need to split some of this information off into a
        # second page.
        self.title_font = ImageFont.truetype(
            "courbd.ttf", 32, layout_engine=ImageFont.Layout.BASIC
        )
        self.heading_font = ImageFont.truetype(
            "courbd.ttf", 24, layout_engine=ImageFont.Layout.BASIC
        )
        self.content_font = ImageFont.truetype(
            "courbd.ttf", 16, layout_engine=ImageFont.Layout.BASIC
        )
        self.table_font = ImageFont.truetype(
            "courbd.ttf", 20, layout_engine=ImageFont.Layout.BASIC
        )
        self.draw = ImageDraw.Draw(self.image)
        self.page_margin = page_margin
        self.x = page_margin
        self.y = page_margin
        self.line_spacing = line_spacing
        self.text_buffer: List[str] = []

    @property
    def position(self) -> Tuple[int, int]:
        return self.x, self.y

    def text(
        self,
        text: str,
        font: Optional[ImageFont.FreeTypeFont] = None,
        fill: Optional[Tuple[int, int, int]] = None,
        wrap: bool = False,
    ) -> None:
        if font is None:
            font = self.content_font
        if fill is None:
            fill = self.foreground_fill

        if wrap:
            text = "\n".join(
                self.wrap_line_with_font(
                    line, self.image_size[0] - self.page_margin - self.x, font
                )
                for line in text.splitlines()
            )

        self.draw.text(self.position, text, font=font, fill=fill)
        box = self.draw.textbbox(self.position, text, font=font)
        height = abs(box[1] - box[3])  # abs(top - bottom) => offset
        self.y += height + self.line_spacing
        self.text_buffer.append(text)

    def flush_text_buffer(self) -> None:
        self.text_buffer = []

    def get_text_string(self) -> str:
        return "\n".join(x for x in self.text_buffer)

    def title(self, title: str) -> None:
        self.text(title, font=self.title_font, fill=self.foreground_fill)

    def heading(self, text: str) -> None:
        self.text(text, font=self.heading_font, fill=self.foreground_fill)

    def table(
        self,
        cells: List[List[str]],
        headers: Optional[List[str]] = None,
        font: Optional[ImageFont.FreeTypeFont] = None,
    ) -> None:
        if headers is None:
            headers = []
        if font is None:
            font = self.table_font
        table = tabulate(cells, headers=headers, numalign="right")
        self.text(table, font, fill=self.foreground_fill)

    def write(self, path: Path) -> None:
        self.image.save(path)
        path.with_suffix(".txt").write_text(self.get_text_string())

    @staticmethod
    def wrap_line(inputstr: str, max_length: int) -> str:
        if len(inputstr) <= max_length:
            return inputstr
        tokens = inputstr.split(" ")
        output = ""
        segments = []
        for token in tokens:
            combo = output + " " + token
            if len(combo) > max_length:
                combo = output + "\n" + token
                segments.append(combo)
                output = ""
            else:
                output = combo
        return "".join(segments + [output]).strip()

    @staticmethod
    def wrap_line_with_font(
        inputstr: str, max_width: int, font: ImageFont.FreeTypeFont
    ) -> str:
        if font.getlength(inputstr) <= max_width:
            return inputstr
        tokens = inputstr.split(" ")
        output = ""
        segments = []
        for token in tokens:
            combo = output + " " + token
            if font.getlength(combo) > max_width:
                segments.append(output + "\n")
                output = token
            else:
                output = combo
        return "".join(segments + [output]).strip()


class KneeboardPage:
    """Base class for all kneeboard pages."""

    def write(self, path: Path) -> None:
        """Writes the kneeboard page to the given path."""
        raise NotImplementedError


@dataclass(frozen=True)
class NumberedWaypoint:
    number: int
    waypoint: FlightWaypoint


class FlightPlanBuilder:
    WAYPOINT_DESC_MAX_LEN = 25

    def __init__(self, start_time: datetime.datetime, units: UnitSystem) -> None:
        self.start_time = start_time
        self.rows: List[List[str]] = []
        self.target_points: List[NumberedWaypoint] = []
        self.last_waypoint: Optional[FlightWaypoint] = None
        self.units = units

    def add_waypoint(self, waypoint_num: int, waypoint: FlightWaypoint) -> None:
        if waypoint.waypoint_type == FlightWaypointType.TARGET_POINT:
            self.target_points.append(NumberedWaypoint(waypoint_num, waypoint))
            return

        if self.target_points:
            self.coalesce_target_points()
            self.target_points = []

        self.add_waypoint_row(NumberedWaypoint(waypoint_num, waypoint))
        self.last_waypoint = waypoint

    def coalesce_target_points(self) -> None:
        if len(self.target_points) <= 4:
            for steerpoint in self.target_points:
                self.add_waypoint_row(steerpoint)
            return

        first_waypoint_num = self.target_points[0].number
        last_waypoint_num = self.target_points[-1].number

        self.rows.append(
            [
                f"{first_waypoint_num}-{last_waypoint_num}",
                "Target points",
                "0",
                self._waypoint_distance(self.target_points[0].waypoint),
                self._ground_speed(self.target_points[0].waypoint),
                self._format_time(self.target_points[0].waypoint.tot),
                self._format_time(self.target_points[0].waypoint.departure_time),
                self._format_min_fuel(self.target_points[0].waypoint.min_fuel),
            ]
        )
        self.last_waypoint = self.target_points[-1].waypoint

    def add_waypoint_row(self, waypoint: NumberedWaypoint) -> None:
        self.rows.append(
            [
                str(waypoint.number),
                KneeboardPageWriter.wrap_line(
                    waypoint.waypoint.pretty_name,
                    FlightPlanBuilder.WAYPOINT_DESC_MAX_LEN,
                ),
                self._format_alt(waypoint.waypoint.alt),
                self._waypoint_distance(waypoint.waypoint),
                self._waypoint_bearing(waypoint.waypoint),
                self._ground_speed(waypoint.waypoint),
                self._format_time(waypoint.waypoint.tot),
                self._format_time(waypoint.waypoint.departure_time),
                self._format_min_fuel(waypoint.waypoint.min_fuel),
            ]
        )

    @staticmethod
    def _format_time(time: datetime.datetime | None) -> str:
        if time is None:
            return ""
        return f"{time.strftime('%H:%M:%S')}{'Z' if time.tzinfo is not None else ''}"

    def _format_alt(self, alt: Distance) -> str:
        return f"{self.units.distance_short(alt):.0f}"

    def _waypoint_distance(self, waypoint: FlightWaypoint) -> str:
        if self.last_waypoint is None:
            return "-"

        distance = meters(
            self.last_waypoint.position.distance_to_point(waypoint.position)
        )

        return f"{self.units.distance_long(distance):.1f}"

    def _waypoint_bearing(self, waypoint: FlightWaypoint) -> str:
        if self.last_waypoint is None:
            return "-"
        bearing = self.last_waypoint.position.heading_between_point(waypoint.position)

        return f"{(bearing):.0f}"

    def _ground_speed(self, waypoint: FlightWaypoint) -> str:
        if self.last_waypoint is None:
            return "-"

        if waypoint.tot is None:
            return "-"

        if self.last_waypoint.departure_time is not None:
            last_time = self.last_waypoint.departure_time
        elif self.last_waypoint.tot is not None:
            last_time = self.last_waypoint.tot
        else:
            return "-"

        if (waypoint.tot - last_time).total_seconds() == 0.0:
            return "-"

        speed = mps(
            self.last_waypoint.position.distance_to_point(waypoint.position)
            / (waypoint.tot - last_time).total_seconds()
        )

        return f"{self.units.speed(speed):.0f}"

    def _format_min_fuel(self, min_fuel: Optional[float]) -> str:
        if min_fuel is None:
            return ""

        mass = pounds(min_fuel)
        return f"{math.ceil(self.units.mass(mass) / 100) * 100:.0f}"

    def build(self) -> List[List[str]]:
        return self.rows


class BriefingPage(KneeboardPage):
    """A kneeboard page containing briefing information."""

    def __init__(
        self,
        flight: FlightData,
        bullseye: Bullseye,
        weather: Weather,
        start_time: datetime.datetime,
        dark_kneeboard: bool,
    ) -> None:
        self.flight = flight
        self.bullseye = bullseye
        self.weather = weather
        self.start_time = start_time
        self.dark_kneeboard = dark_kneeboard
        self.flight_plan_font = ImageFont.truetype(
            "courbd.ttf",
            16,
            layout_engine=ImageFont.Layout.BASIC,
        )

    def write(self, path: Path) -> None:
        writer = KneeboardPageWriter(dark_theme=self.dark_kneeboard)
        if self.flight.custom_name:
            custom_name_title = ' ("{}")'.format(self.flight.custom_name)
        else:
            custom_name_title = ""
        writer.title(f"{self.flight.callsign} Mission Info{custom_name_title}")

        # TODO: Handle carriers.
        writer.heading("Airfield Info")
        writer.table(
            [
                self.airfield_info_row("Departure", self.flight.departure),
                self.airfield_info_row("Arrival", self.flight.arrival),
                self.airfield_info_row("Divert", self.flight.divert),
            ],
            headers=["", "Airbase", "ATC", "TCN", "I(C)LS", "RWY"],
        )

        writer.heading(
            f"Flight Plan ({self.flight.squadron.aircraft.variant_id} - "
            f"{self.flight.flight_type.value})"
        )

        units = self.flight.aircraft_type.kneeboard_units

        flight_plan_builder = FlightPlanBuilder(self.start_time, units)
        for num, waypoint in enumerate(self.flight.waypoints):
            flight_plan_builder.add_waypoint(num, waypoint)

        uom_row = [
            [
                "",
                "",
                units.distance_short_uom,
                units.distance_long_uom,
                "T",
                units.speed_uom,
                "",
                "",
                units.mass_uom,
            ]
        ]

        writer.table(
            flight_plan_builder.build() + uom_row,
            headers=[
                "#",
                "Action",
                "Alt",
                "Dist",
                "Brg",
                "GSPD",
                "Time",
                "Departure",
                "Min fuel",
            ],
            font=self.flight_plan_font,
        )

        writer.text(f"Bullseye: {self.bullseye.position.latlng().format_dms()}")

        qnh_in_hg = f"{self.weather.atmospheric.qnh.inches_hg:.2f}"
        qnh_mm_hg = f"{self.weather.atmospheric.qnh.mm_hg:.1f}"
        qnh_hpa = f"{self.weather.atmospheric.qnh.hecto_pascals:.1f}"
        writer.text(
            f"Temperature: {round(self.weather.atmospheric.temperature_celsius)} °C at sea level"
        )
        writer.text(f"QNH: {qnh_in_hg} inHg / {qnh_mm_hg} mmHg / {qnh_hpa} hPa")
        writer.text(
            f"Turbulence: {round(self.weather.atmospheric.turbulence_per_10cm)} per 10cm at ground level."
        )
        writer.text(
            f"Wind: {self.weather.wind.at_0m.direction}°"
            f" / {round(mps(self.weather.wind.at_0m.speed).knots)}kts (0ft)"
            f" ; {self.weather.wind.at_2000m.direction}°"
            f" / {round(mps(self.weather.wind.at_2000m.speed).knots)}kts (~6500ft)"
            f" ; {self.weather.wind.at_8000m.direction}°"
            f" / {round(mps(self.weather.wind.at_8000m.speed).knots)}kts (~26000ft)"
        )
        c = self.weather.clouds
        writer.text(
            f'Cloud base: {f"{int(round(meters(c.base).feet, -2))}ft" if c else "CAVOK"}'
            f'{f", {c.preset.ui_name[:-2]}" if c and c.preset else ""}'
        )

        fl = self.flight

        start_pos = fl.waypoints[0].position.latlng()
        sun = Sun(start_pos.lat, start_pos.lng)

        date = fl.squadron.coalition.game.date
        dt = datetime.datetime(date.year, date.month, date.day)
        tz = fl.squadron.coalition.game.theater.timezone

        # Get today's sunrise and sunset in UTC
        try:
            rise_utc = sun.get_sunrise_time(dt)
            rise = rise_utc + tz.utcoffset(sun.get_sunrise_time(dt))
        except SunTimeException:
            rise_utc = None
            rise = None

        try:
            set_utc = sun.get_sunset_time(dt)
            sunset = set_utc + tz.utcoffset(sun.get_sunset_time(dt))
        except SunTimeException:
            set_utc = None
            sunset = None

        writer.text(
            f"Sunrise - Sunset: {rise.strftime('%H:%M') if rise else 'N/A'} - {sunset.strftime('%H:%M') if sunset else 'N/A'}"
            f" ({rise_utc.strftime('%H:%M') if rise_utc else 'N/A'} - {set_utc.strftime('%H:%M') if set_utc else 'N/A'} UTC)"
        )

        if fl.bingo_fuel and fl.joker_fuel:
            writer.table(
                [
                    [
                        f"{units.mass(pounds(fl.bingo_fuel)):.0f} {units.mass_uom}",
                        f"{units.mass(pounds(fl.joker_fuel)):.0f} {units.mass_uom}",
                    ]
                ],
                ["Bingo", "Joker"],
            )

        if any(self.flight.laser_codes):
            codes: list[list[str]] = []
            for idx, code in enumerate(self.flight.laser_codes, start=1):
                codes.append([str(idx), "" if code is None else str(code)])
            writer.table(codes, ["#", "Laser Code"])

        writer.write(path)

    def airfield_info_row(
        self, row_title: str, runway: Optional[RunwayData]
    ) -> List[str]:
        """Creates a table row for a given airfield.

        Args:
            row_title: Purpose of the airfield. e.g. "Departure", "Arrival" or
                "Divert".
            runway: The runway described by this row.

        Returns:
            A list of strings to be used as a row of the airfield table.
        """
        if runway is None:
            return [row_title, "", "", "", "", ""]

        atc = ""
        if runway.atc is not None:
            atc = self.format_frequency(runway.atc)
        if runway.tacan is None:
            tacan = ""
        else:
            tacan = str(runway.tacan)
        if runway.ils is not None:
            ils = str(runway.ils)
        elif runway.icls is not None:
            ils = str(runway.icls)
        else:
            ils = ""
        return [
            row_title,
            "\n".join(textwrap.wrap(runway.airfield_name, width=17)),
            atc,
            tacan,
            ils,
            runway.runway_name,
        ]

    def format_frequency(self, frequency: RadioFrequency) -> str:
        channel = self.flight.channel_for(frequency)
        if channel is None:
            return str(frequency)

        channel_name = self.flight.aircraft_type.channel_name(
            channel.radio_id, channel.channel
        )
        return f"{channel_name}\n{frequency}"


class SupportPage(KneeboardPage):
    """A kneeboard page containing information about support units."""

    JTAC_REGION_MAX_LEN = 25

    def __init__(
        self,
        flight: FlightData,
        package_flights: List[FlightData],
        comms: List[CommInfo],
        awacs: List[AwacsInfo],
        tankers: List[TankerInfo],
        jtacs: List[JtacInfo],
        start_time: datetime.datetime,
        dark_kneeboard: bool,
    ) -> None:
        self.flight = flight
        self.package_flights = package_flights
        self.comms = list(comms)
        self.awacs = awacs
        self.tankers = tankers
        self.jtacs = jtacs
        self.start_time = start_time
        self.dark_kneeboard = dark_kneeboard
        flight_name = self.flight.custom_name if self.flight.custom_name else "Flight"
        self.comms.append(CommInfo(flight_name, self.flight.intra_flight_channel))

    def write(self, path: Path) -> None:
        writer = KneeboardPageWriter(dark_theme=self.dark_kneeboard)
        if self.flight.custom_name:
            custom_name_title = ' ("{}")'.format(self.flight.custom_name)
        else:
            custom_name_title = ""
        writer.title(f"{self.flight.callsign} Support Info{custom_name_title}")

        # Package Section
        package = self.flight.package
        custom = f' "{package.custom_name}"' if package.custom_name else ""
        writer.heading(f"{package.package_description} Package{custom}")
        freq = self.format_frequency(package.frequency).replace("\n", " - ")
        writer.text(f"  FREQ: {freq}", font=writer.table_font)
        tot = self._format_time(package.time_over_target)
        writer.text(f"  TOT: {tot}", font=writer.table_font)
        comm_ladder = []
        for comm in self.comms:
            comm_ladder.append(
                [
                    comm.name,
                    str(self.flight.flight_type),
                    KneeboardPageWriter.wrap_line(str(self.flight.aircraft_type), 23),
                    str(len(self.flight.units)),
                    self.format_frequency(comm.freq),
                ]
            )
        for f in self.package_flights:
            callsign = f.callsign
            if f.custom_name:
                callsign = f"{callsign}\n({f.custom_name})"
            comm_ladder.append(
                [
                    callsign,
                    str(f.flight_type),
                    KneeboardPageWriter.wrap_line(str(f.aircraft_type), 23),
                    str(len(f.units)),
                    self.format_frequency(f.intra_flight_channel),
                ]
            )

        writer.table(comm_ladder, headers=["Callsign", "Task", "Type", "#A/C", "FREQ"])

        # AEW&C
        writer.heading("AEW&C")
        aewc_ladder = []

        for single_aewc in self.awacs:
            if single_aewc.depature_location is None:
                tot = "-"
                tos = "-"
            else:
                tot = self._format_time(single_aewc.start_time)
                tos = self._format_duration(
                    single_aewc.end_time - single_aewc.start_time
                )

            aewc_ladder.append(
                [
                    str(single_aewc.callsign),
                    self.format_frequency(single_aewc.freq),
                    str(single_aewc.depature_location),
                    "TOT: " + tot + "\n" + "TOS: " + tos,
                ]
            )

        writer.table(
            aewc_ladder,
            headers=["Callsign", "FREQ", "Departure", "TOT / TOS"],
        )

        comm_ladder = []
        writer.heading("Tankers")
        for tanker in self.tankers:
            tot = self._format_time(tanker.start_time)
            tos = self._format_duration(tanker.end_time - tanker.start_time)
            comm_ladder.append(
                [
                    tanker.callsign,
                    "Tanker",
                    KneeboardPageWriter.wrap_line(tanker.variant, 21),
                    str(tanker.tacan) if tanker.tacan else "N/A",
                    self.format_frequency(tanker.freq),
                    "TOT: " + tot + "\n" + "TOS: " + tos,
                ]
            )

        writer.table(
            comm_ladder,
            headers=["Callsign", "Task", "Type", "TACAN", "FREQ", "TOT / TOS"],
        )

        writer.heading("JTAC")
        jtacs = []
        for jtac in self.jtacs:
            jtacs.append(
                [
                    jtac.callsign,
                    KneeboardPageWriter.wrap_line(
                        jtac.region,
                        self.JTAC_REGION_MAX_LEN,
                    ),
                    jtac.code,
                    self.format_frequency(jtac.freq),
                ]
            )
        writer.table(jtacs, headers=["Callsign", "Region", "Laser Code", "FREQ"])

        writer.write(path)

    def format_frequency(self, frequency: Optional[RadioFrequency]) -> str:
        if frequency is None:
            return ""
        channel = self.flight.channel_for(frequency)
        if channel is None:
            return str(frequency)

        channel_name = self.flight.aircraft_type.channel_name(
            channel.radio_id, channel.channel
        )
        return f"{channel_name}\n{frequency}"

    @staticmethod
    def _format_time(time: datetime.datetime | None) -> str:
        if time is None:
            return ""
        return f"{time.strftime('%H:%M:%S')}{'Z' if time.tzinfo is not None else ''}"

    @staticmethod
    def _format_duration(time: Optional[datetime.timedelta]) -> str:
        if time is None:
            return ""
        time -= datetime.timedelta(microseconds=time.microseconds)
        return f"{time}"


class SeadTaskPage(KneeboardPage):
    """A kneeboard page containing SEAD/DEAD target information."""

    def __init__(self, flight: FlightData, dark_kneeboard: bool) -> None:
        self.flight = flight
        self.dark_kneeboard = dark_kneeboard

    @property
    def target_units(self) -> Iterator[TheaterUnit]:
        if isinstance(self.flight.package.target, TheaterGroundObject):
            yield from self.flight.package.target.strike_targets

    @staticmethod
    def alic_for(unit: TheaterUnit) -> str:
        try:
            return str(AlicCodes.code_for(unit))
        except KeyError:
            return ""

    def write(self, path: Path) -> None:
        writer = KneeboardPageWriter(dark_theme=self.dark_kneeboard)
        if self.flight.custom_name:
            custom_name_title = ' ("{}")'.format(self.flight.custom_name)
        else:
            custom_name_title = ""
        task = "DEAD" if self.flight.flight_type == FlightType.DEAD else "SEAD"
        writer.title(f"{self.flight.callsign} {task} Target Info{custom_name_title}")

        writer.table(
            [self.target_info_row(t) for t in self.target_units],
            headers=["Description", "ALIC", "Location"],
        )

        writer.write(path)

    def target_info_row(self, unit: TheaterUnit) -> List[str]:
        ll = unit.position.latlng()
        unit_type = unit.type
        name = unit.name if unit_type is None else unit_type.name
        return [
            name,
            self.alic_for(unit),
            ll.format_dms(include_decimal_seconds=True),
        ]


class StrikeTaskPage(KneeboardPage):
    """A kneeboard page containing strike target information."""

    WAYPOINT_DESC_MAX_LEN = 35

    def __init__(self, flight: FlightData, dark_kneeboard: bool) -> None:
        self.flight = flight
        self.dark_kneeboard = dark_kneeboard

    @property
    def targets(self) -> Iterator[NumberedWaypoint]:
        for idx, waypoint in enumerate(self.flight.waypoints):
            if waypoint.waypoint_type == FlightWaypointType.TARGET_POINT:
                yield NumberedWaypoint(idx, waypoint)

    def write(self, path: Path) -> None:
        writer = KneeboardPageWriter(dark_theme=self.dark_kneeboard)
        if self.flight.custom_name:
            custom_name_title = ' ("{}")'.format(self.flight.custom_name)
        else:
            custom_name_title = ""
        writer.title(f"{self.flight.callsign} Strike Task Info{custom_name_title}")

        if self.flight.units[0].unit_type == F_15ESE:
            i: int = 0
            for target in self.targets:
                if not target.waypoint.pretty_name.__contains__("DTC"):
                    target.waypoint.pretty_name = (
                        f"{target.waypoint.pretty_name} (DTC M{(i//8)+1}.{i%9+1})"
                    )
                    i = i + 1

        writer.table(
            [self.target_info_row(t, writer) for t in self.targets],
            headers=["STPT", "Description", "Location"],
        )

        writer.write(path)

    @staticmethod
    def target_info_row(
        target: NumberedWaypoint, writer: KneeboardPageWriter
    ) -> list[str]:
        return [
            str(target.number),
            writer.wrap_line(
                target.waypoint.pretty_name, StrikeTaskPage.WAYPOINT_DESC_MAX_LEN
            ),
            target.waypoint.position.latlng().format_dms(include_decimal_seconds=True),
        ]


class NotesPage(KneeboardPage):
    """A kneeboard page containing the campaign owner's notes."""

    def __init__(
        self,
        notes: str,
        dark_kneeboard: bool,
    ) -> None:
        self.notes = notes
        self.dark_kneeboard = dark_kneeboard

    def write(self, path: Path) -> None:
        writer = KneeboardPageWriter(dark_theme=self.dark_kneeboard)
        writer.title(f"Notes")
        writer.text(self.notes, wrap=True)
        writer.write(path)


class KneeboardGenerator(MissionInfoGenerator):
    """Creates kneeboard pages for each client flight in the mission."""

    def __init__(self, mission: Mission, game: "Game") -> None:
        super().__init__(mission, game)
        self.dark_kneeboard = self.game.settings.generate_dark_kneeboard and (
            self.mission.start_time.hour > 19 or self.mission.start_time.hour < 7
        )

    def generate(self) -> None:
        """Generates a kneeboard per client flight."""
        temp_dir = Path("kneeboards")
        temp_dir.mkdir(exist_ok=True)
        for aircraft, pages in self.pages_by_airframe().items():
            aircraft_dir = temp_dir / aircraft.dcs_unit_type.id
            aircraft_dir.mkdir(exist_ok=True)
            for idx, page in enumerate(pages):
                page_path = aircraft_dir / f"page{idx:02}.png"
                page.write(page_path)
                self.mission.add_aircraft_kneeboard(aircraft.dcs_unit_type, page_path)
        if not kneeboards_dir().exists():
            return
        for type in kneeboards_dir().iterdir():
            if type.is_dir():
                for kneeboard in type.iterdir():
                    self.mission.custom_kneeboards[type.name].append(kneeboard)
            else:
                self.mission.custom_kneeboards[""].append(type)

    def pages_by_airframe(self) -> Dict[AircraftType, List[KneeboardPage]]:
        """Returns a list of kneeboard pages per airframe in the mission.

        Only client flights will be included, but because DCS does not support
        group-specific kneeboard pages, flights (possibly from opposing sides)
        will be able to see the kneeboards of all aircraft of the same type.

        Returns:
            A dict mapping aircraft types to the list of kneeboard pages for
            that aircraft.
        """
        all_flights: Dict[AircraftType, List[KneeboardPage]] = defaultdict(list)
        for flight in self.flights:
            if not flight.client_units:
                continue
            package_flights = [
                f
                for f in self.flights
                if f.package is flight.package and f is not flight
            ]
            all_flights[flight.aircraft_type].extend(
                self.generate_flight_kneeboard(flight, package_flights)
            )
        return all_flights

    def generate_task_page(self, flight: FlightData) -> Optional[KneeboardPage]:
        if flight.flight_type in (FlightType.DEAD, FlightType.SEAD):
            return SeadTaskPage(flight, self.dark_kneeboard)
        elif flight.flight_type is FlightType.STRIKE:
            return StrikeTaskPage(flight, self.dark_kneeboard)
        return None

    def generate_flight_kneeboard(
        self, flight: FlightData, package_flights: List[FlightData]
    ) -> List[KneeboardPage]:
        """Returns a list of kneeboard pages for the given flight."""

        if flight.aircraft_type.utc_kneeboard:
            zoned_time = self.game.conditions.start_time.replace(
                tzinfo=self.game.theater.timezone
            ).astimezone(datetime.timezone.utc)
        else:
            zoned_time = self.game.conditions.start_time

        pages: List[KneeboardPage] = [
            BriefingPage(
                flight,
                self.game.coalition_for(flight.friendly).bullseye,
                self.game.conditions.weather,
                zoned_time,
                self.dark_kneeboard,
            ),
            SupportPage(
                flight,
                package_flights,
                self.comms,
                self.awacs,
                self.tankers,
                self.jtacs,
                zoned_time,
                self.dark_kneeboard,
            ),
        ]

        # Only create the notes page if there are notes to show.
        if notes := self.game.notes:
            pages.append(NotesPage(notes, self.dark_kneeboard))

        if (target_page := self.generate_task_page(flight)) is not None:
            pages.append(target_page)

        return pages
