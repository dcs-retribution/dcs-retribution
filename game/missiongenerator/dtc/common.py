"""Shared extraction helpers for the DTC cartridge builders.

Everything a cartridge wants already exists at generation time; these helpers
pull it into airframe-neutral shapes the per-jet builders (:mod:`.hornet`,
:mod:`.viper`) format.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from datetime import datetime, timezone as tz
from typing import TYPE_CHECKING, Optional

from dcs import Point

from game.ato.flighttype import FlightType
from game.ato.flightwaypointtype import FlightWaypointType

if TYPE_CHECKING:
    from game import Game
    from game.ato.flightwaypoint import FlightWaypoint
    from game.missiongenerator.aircraft.flightdata import FlightData
    from game.missiongenerator.missiondata import MissionData

#: Route-sequence default speed the ME uses when a leg speed is unknown (km/h).
DEFAULT_LEG_SPEED_KMH = 463.0

#: Sanity clamp for computed leg ground speeds (km/h).
MIN_LEG_SPEED_KMH = 150.0
MAX_LEG_SPEED_KMH = 2200.0

#: Waypoint types that are reference marks, not flown route members.
NON_ROUTE_WAYPOINTS = (
    FlightWaypointType.DIVERT,
    FlightWaypointType.BULLSEYE,
)


def waypoint_display_name(label: str, max_len: int = 24) -> str:
    """ASCII-fold a waypoint name for cockpit displays.

    Retribution waypoint names carry em-dashes and other punctuation the DDI/
    DED fonts may not render; fold dashes, drop the rest of non-ASCII, and cap
    the length.
    """
    folded = label.replace("—", "-").replace("–", "-")
    cleaned = folded.encode("ascii", "ignore").decode("ascii")
    return " ".join(cleaned.split())[:max_len]


def sanitize_short_name(label: str, max_len: int = 5) -> str:
    """Uppercase alphanumeric truncation -- the DTC channel-name filter.

    The ME import clamps channel names to 5 uppercase letters/digits
    (``custom_input_filter_*`` in the FA-18C descriptor); emitting names that
    already satisfy the filter keeps what the jet shows identical to what we
    wrote.
    """
    cleaned = re.sub(r"[^A-Z0-9]", "", label.upper())
    return cleaned[:max_len]


def short_callsign(callsign: str) -> str:
    """First word of a callsign, sanitized ("Arco 1-1" -> "ARCO")."""
    first = callsign.split()[0] if callsign.split() else callsign
    return sanitize_short_name(first)


def seconds_of_day(game: Game, when: Optional[datetime]) -> int:
    """Seconds since Zulu midnight of the mission day -- the cartridge's clock.

    DCS mission time is theater-local, but cartridge times are Zulu. The ME's
    own DTC manager bases them on ``mission.start_time - SummerTimeDelta*3600``
    (``me_managerDTC.lua``), and both jets read them against a Zulu system
    clock: the Hornet's TOT is entered in Zulu (FA-18C guide p123) and the
    Viper's CRUS TOS page sits beside a System Time that is "based on Zulu time
    (UTC)" (F-16C guide p103, p107). Emitting local put every ETA out by the
    map's UTC offset -- +4 h on Caucasus, -8 h on Nevada.

    The base stays the mission day's midnight rather than the wall clock's, so
    ETAs across a Zulu midnight keep increasing (the editor's TOS field carries
    a days component for exactly that).
    """
    if when is None:
        return 0
    start_zulu = game.conditions.start_time.replace(
        tzinfo=game.theater.timezone
    ).astimezone(tz.utc)
    midnight = start_zulu.replace(hour=0, minute=0, second=0, microsecond=0)
    when_zulu = when.replace(tzinfo=game.theater.timezone).astimezone(tz.utc)
    return max(0, int((when_zulu - midnight).total_seconds()))


def leg_speed_kmh(prev: Optional[FlightWaypoint], current: FlightWaypoint) -> float:
    """Ground speed for the leg into ``current`` in km/h (the DTC speed unit)."""
    if (
        prev is None
        or prev.tot is None
        and prev.departure_time is None
        or current.tot is None
    ):
        return DEFAULT_LEG_SPEED_KMH
    depart = prev.departure_time or prev.tot
    assert depart is not None
    elapsed = (current.tot - depart).total_seconds()
    if elapsed <= 0:
        return DEFAULT_LEG_SPEED_KMH
    meters = prev.position.distance_to_point(current.position)
    speed = meters / elapsed * 3.6
    return max(MIN_LEG_SPEED_KMH, min(MAX_LEG_SPEED_KMH, speed))


def bearing_degrees(start: Point, end: Point) -> float:
    """Map bearing from start to end (0 = north), DCS x=north / y=east."""
    return math.degrees(math.atan2(end.y - start.y, end.x - start.x)) % 360.0


def is_route_waypoint(waypoint: FlightWaypoint) -> bool:
    return waypoint.waypoint_type not in NON_ROUTE_WAYPOINTS


def is_target_waypoint(waypoint: FlightWaypoint) -> bool:
    """A point the flight attacks, by type -- never by the attached target list.

    Retribution hangs that list on the ingress point too, so the task can be
    built; reading it put the target symbol on the IP (the Viper's HSD
    triangle, the Hornet's route flag).
    """
    return "TARGET" in waypoint.waypoint_type.name


#: Waypoint types whose planned altitude may BE the ground under them. DIVERT is
#: excluded because an off-map one is an exit vector planned at cruise, and the
#: two are not separable here.
_FIELD_ELEVATION_WAYPOINTS = (
    FlightWaypointType.TAKEOFF,
    FlightWaypointType.LANDING_POINT,
)


def steerpoint_elevation(waypoint: FlightWaypoint) -> float:
    """The ground elevation under a steerpoint, in metres AMSL.

    This is NOT the altitude to fly -- that is ``leg_altitude`` below, and the two
    are separate fields in both jets. ED's own editors fill this one from the
    terrain (``alt = getAltitude(x, y)`` in the Viper's ``NAV_PTS.lua`` and the
    Hornet's ``WYPT_NAV.lua``), and the Viper's loader defaults a missing one to
    2000 m, so it has to be written and it has to be an elevation.

    Only takeoff and landing can know their ground, and only when the plan put
    the field elevation on them. Everything else returns 0, which is wrong on
    high terrain: the generator has no terrain height source.
    """
    if waypoint.waypoint_type in _FIELD_ELEVATION_WAYPOINTS:
        return waypoint.alt.meters if waypoint.alt_type == "BARO" else 0.0
    return 0.0


def leg_altitude(waypoint: FlightWaypoint) -> tuple[float, int]:
    """Altitude to fly the leg, in metres + DTC altitudeType (1 = MSL, 2 = AGL).

    Goes in the Viper's ``routeAltitude`` and the Hornet's ``NAV_ROUTE`` entry,
    never in the point's own ``alt``. AGL is resolved against terrain by the jet
    (``tmpAlt + getAltitude(x, y)``, Hornet ``ROUTE_SEQ.lua``).

    Cartridges are built only for client flights, and the generated .miz puts a
    client flight's flyover waypoints on the deck (``PydcsWaypointBuilder.build``
    sets 0 AGL so pods and weapons can be slaved to them); the cartridge must
    agree or the AutoLoad would float the steerpoint back up to the AI's track
    altitude.
    """
    if waypoint.flyover:
        return 0.0, 2
    return waypoint.alt.meters, 2 if waypoint.alt_type == "RADIO" else 1


@dataclass(frozen=True)
class SupportTrack:
    """One friendly racetrack: a CAP station or a tanker/AEW&C orbit."""

    callsign: str
    kind: str  # "CAP" | "TKR" | "AWACS"
    start: Point
    end: Point

    @property
    def center(self) -> tuple[float, float]:
        return ((self.start.x + self.end.x) / 2, (self.start.y + self.end.y) / 2)

    @property
    def course(self) -> float:
        if self.start.distance_to_point(self.end) < 1.0:
            return 0.0
        return bearing_degrees(self.start, self.end)

    @property
    def length_m(self) -> float:
        # Floor at 2 NM so a degenerate/point orbit still draws a readable
        # racetrack on the SA page.
        return max(3704.0, self.start.distance_to_point(self.end))


def racetrack_ends(
    flight: FlightData,
) -> tuple[Optional[Point], Optional[Point]]:
    """The PATROL_TRACK -> PATROL waypoint pair."""
    start: Optional[Point] = None
    end: Optional[Point] = None
    for waypoint in flight.waypoints:
        if waypoint.waypoint_type == FlightWaypointType.PATROL_TRACK:
            start = waypoint.position
        elif waypoint.waypoint_type == FlightWaypointType.PATROL:
            end = waypoint.position
    return start, end


_SUPPORT_FLIGHT_TYPES = (FlightType.REFUELING, FlightType.AEWC)


def _tracks_of_types(
    mission_data: MissionData,
    types: tuple[FlightType, ...],
    kind_by_type: dict[FlightType, str],
) -> list[SupportTrack]:
    tracks = []
    for flight in mission_data.flights:
        if flight.flight_type not in types:
            continue
        if not flight.friendly.is_blue:
            continue
        start, end = racetrack_ends(flight)
        if start is None or end is None:
            continue
        tracks.append(
            SupportTrack(
                callsign=short_callsign(flight.callsign),
                kind=kind_by_type[flight.flight_type],
                start=start,
                end=end,
            )
        )
    return tracks


#: Waypoint types that anchor a non-orbiting flight's own-track stand-in, in
#: preference order: the hold point is where the flight actually orbits while
#: it waits, the join point is the next best fix.
_HOLD_WAYPOINTS = (FlightWaypointType.LOITER, FlightWaypointType.JOIN)


def own_orbit_track(flight: FlightData) -> Optional[SupportTrack]:
    """The flight's own racetrack, or a stand-in at its hold point.

    A flight that flies a real racetrack (BARCAP, TARCAP, tanker, AEW&C) gets
    that track. Everyone else orbits somewhere too -- the hold -- so rather
    than no track at all, a degenerate one at the hold (or join) point draws as
    the minimum-length racetrack. None only when the plan has neither.
    """
    start, end = racetrack_ends(flight)
    callsign = short_callsign(flight.callsign)
    if start is not None and end is not None:
        return SupportTrack(callsign=callsign, kind="CAP", start=start, end=end)
    for waypoint_type in _HOLD_WAYPOINTS:
        for waypoint in flight.waypoints:
            if waypoint.waypoint_type == waypoint_type:
                position = waypoint.position
                return SupportTrack(
                    callsign=callsign, kind="HOLD", start=position, end=position
                )
    return None


def support_tracks(mission_data: MissionData) -> list[SupportTrack]:
    """Every blue tanker + AEW&C orbit."""
    return _tracks_of_types(
        mission_data,
        _SUPPORT_FLIGHT_TYPES,
        {FlightType.REFUELING: "TKR", FlightType.AEWC: "AWACS"},
    )


def flot_segments(game: Game) -> list[tuple[str, list[tuple[float, float]]]]:
    """Each active front line as (name, [two endpoints]) -- the same geometry
    the F10 frontline drawing uses."""
    from game.missiongenerator.frontlineconflictdescription import (
        FrontLineConflictDescription,
    )

    segments = []
    for front_line in game.theater.conflicts():
        bounds = FrontLineConflictDescription.frontline_bounds(front_line, game.theater)
        start = bounds.left_position
        end = start.point_from_heading(
            bounds.heading_from_left_to_right.degrees, bounds.length
        )
        segments.append((front_line.name, [(start.x, start.y), (end.x, end.y)]))
    return segments


@dataclass(frozen=True)
class ThreatSite:
    """One enemy air-defense site the blue player's map already shows exact."""

    label: str
    x: float
    y: float
    range_m: float


#: NATO shorthand by DCS unit-type id / display-name keywords. Ordered: the
#: specific system names first (DCS ids say "Kub"/"S-300PS", never "SA-6").
_SAM_LABEL_PATTERNS: tuple[tuple[str, str], ...] = (
    (r"S[-_ ]?400", "21"),
    (r"S[-_ ]?300|SA[-_ ]?10|SA[-_ ]?20", "10"),
    (r"S[-_ ]?200|SA[-_ ]?5", "5"),
    (r"S[-_ ]?125|SA[-_ ]?3", "3"),
    (r"S[-_ ]?75|SNR[-_ ]?75|SA[-_ ]?2\b", "2"),
    (r"BUK|SA[-_ ]?11", "11"),
    (r"SA[-_ ]?17", "17"),
    (r"TOR|SA[-_ ]?15", "15"),
    (r"KUB|SA[-_ ]?6", "6"),
    (r"OSA|SA[-_ ]?8", "8"),
    (r"STRELA[-_ ]?10|SA[-_ ]?13", "13"),
    (r"STRELA|SA[-_ ]?9", "9"),
    (r"TUNGUSKA|SA[-_ ]?19", "19"),
    (r"PANTSIR|SA[-_ ]?22", "22"),
    (r"SA[-_ ]?(\d+)", ""),  # any remaining SA-N -> the digits
    (r"PATRIOT", "P"),
    (r"HAWK", "HK"),
    (r"NASAMS", "NS"),
    (r"ROLAND", "RO"),
    (r"RAPIER", "RP"),
    (r"CHAPARRAL", "CH"),
    (r"HQ[-_ ]?7", "7"),
    (r"AVENGER", "AV"),
    (r"GEPARD|VULCAN|ZSU|SHILKA|ZU[-_ ]?23|AAA|FLAK", "A"),
)


def _threat_label(tgo_name: str, unit_names: list[str]) -> str:
    """A <=3-char SA-page label for a SAM site, derived from its unit types."""
    haystack = " ".join([tgo_name, *unit_names]).upper()
    for pattern, replacement in _SAM_LABEL_PATTERNS:
        match = re.search(pattern, haystack)
        if match:
            return replacement if replacement else match.group(1)[:3]
    return sanitize_short_name(tgo_name, 3) or "T"


def known_enemy_threat_sites(game: Game) -> list[ThreatSite]:
    """Enemy air-defense sites, longest range first -- the same set the F10
    map draws."""
    sites = []
    for cp in game.theater.controlpoints:
        if not cp.captured.is_red:
            continue
        for tgo in getattr(cp, "ground_objects", []):
            if getattr(tgo, "category", None) != "aa":
                continue
            threat_range = tgo.max_threat_range()
            if not threat_range or threat_range.meters <= 0:
                continue
            unit_names = []
            for group in getattr(tgo, "groups", []):
                for unit in getattr(group, "units", []):
                    unit_type = getattr(unit, "type", None)
                    # TheaterUnit.type is a pydcs class; its .id is the DCS
                    # type string ("Kub 1S91 str") the label patterns key on.
                    unit_names.append(
                        str(getattr(unit_type, "id", None) or unit_type or "")
                    )
            sites.append(
                ThreatSite(
                    label=_threat_label(tgo.name, unit_names),
                    x=tgo.position.x,
                    y=tgo.position.y,
                    range_m=threat_range.meters,
                )
            )
    sites.sort(key=lambda site: site.range_m, reverse=True)
    return sites
