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
    from game.radio.radios import RadioFrequency

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


def frequency_labels(flight: FlightData, mission_data: MissionData) -> dict[float, str]:
    """A short name, keyed by MHz, for every frequency the channel allocator may
    have preset: the one thing the Hornet's COMM section adds over the miz."""
    labels: dict[float, str] = {}

    def put(freq: Optional[RadioFrequency], label: str) -> None:
        if freq is not None:
            labels.setdefault(round(freq.mhz, 3), sanitize_short_name(label))

    put(flight.intra_flight_channel, short_callsign(flight.callsign))
    for info in [*mission_data.awacs, *mission_data.tankers]:
        put(info.freq, short_callsign(info.callsign))
    for jtac in mission_data.jtacs:
        put(jtac.freq, "JTAC")
    put(flight.package.frequency, "PKG")
    put(flight.departure.atc, "DEP")
    if flight.arrival != flight.departure:
        put(flight.arrival.atc, "ARR")
    if flight.divert is not None:
        put(flight.divert.atc, "DVT")
    return labels


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


def steerpoint_altitude(waypoint: FlightWaypoint) -> float:
    """The steerpoint's altitude in metres MSL: what the .miz route gives the jet.

    Both jets carry two altitude fields, the point's ``alt`` and the route
    leg's (``routeAltitude`` / ``NAV_ROUTE[].alt``), and the cockpit shows the
    first: a Viper flown with ``alt`` 131 ft and ``routeAltitude`` 22,000 ft
    read ELEV 131 on the DED. Without a cartridge the jet takes ELEV from the
    mission-editor waypoint altitude, so the mirror carries the same number.
    The generator has no terrain height source, so a point the .miz puts on
    the deck (a client flight's flyover waypoints) or plans AGL reads 0 here;
    the route entry keeps its AGL encoding for the DTC Manager.
    """
    if waypoint.flyover or waypoint.alt_type == "RADIO":
        return 0.0
    return waypoint.alt.meters


def leg_altitude(waypoint: FlightWaypoint) -> tuple[float, int]:
    """Altitude for the route entry, in metres + DTC altitudeType (1 MSL, 2 AGL).

    The DTC Manager resolves AGL against terrain (``tmpAlt + getAltitude(x, y)``,
    Hornet ``ROUTE_SEQ.lua``); the jet displays the point's ``alt`` instead.
    """
    if waypoint.flyover:
        return 0.0, 2
    return waypoint.alt.meters, 2 if waypoint.alt_type == "RADIO" else 1


def _altitude_msl(waypoint: FlightWaypoint) -> float:
    return waypoint.alt.meters if waypoint.alt_type == "BARO" else 0.0


@dataclass(frozen=True)
class SupportTrack:
    """One friendly racetrack: a CAP station or a tanker/AEW&C orbit."""

    callsign: str
    kind: str  # "CAP" | "TKR" | "AWACS"
    start: Point
    end: Point
    #: The orbit's planned altitude, metres MSL (0 when the plan is AGL).
    altitude_m: float = 0.0
    #: Half-width of the box drawn around the orbit; None for the default.
    half_width_m: Optional[float] = None

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
                altitude_m=_orbit_altitude(flight),
                half_width_m=support_half_width(flight),
            )
        )
    return tracks


#: Waypoint types that anchor a non-orbiting flight's own-track stand-in, in
#: preference order: the hold point is where the flight actually orbits while
#: it waits, the join point is the next best fix.
_HOLD_WAYPOINTS = (FlightWaypointType.LOITER, FlightWaypointType.JOIN)


def _orbit_altitude(flight: FlightData) -> float:
    for waypoint in flight.waypoints:
        if waypoint.waypoint_type == FlightWaypointType.PATROL_TRACK:
            return _altitude_msl(waypoint)
    return 0.0


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
        return SupportTrack(
            callsign=callsign,
            kind="CAP",
            start=start,
            end=end,
            altitude_m=_orbit_altitude(flight),
        )
    for waypoint_type in _HOLD_WAYPOINTS:
        for waypoint in flight.waypoints:
            if waypoint.waypoint_type == waypoint_type:
                position = waypoint.position
                return SupportTrack(
                    callsign=callsign,
                    kind="HOLD",
                    start=position,
                    end=position,
                    altitude_m=_altitude_msl(waypoint),
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


#: A support orbit's turn diameter, matching the Hornet SA page's own CAP
#: racetrack. The box is the racetrack's footprint: the straight legs plus the
#: room the turns need at each end.
SUPPORT_ORBIT_DIAMETER_M = 5 * 1852.0

#: The AI turns shallow at the end of a support leg and overshoots it: tankers
#: and AWACS ran 14-19 km off the leg centreline in a flown test. A 20-degree
#: turn radius at the orbit speed plus 3 NM covers that; 2 NM is the floor.
SUPPORT_ORBIT_TURN_BANK_DEG = 20.0
SUPPORT_ORBIT_TURN_PAD_M = 3 * 1852.0
SUPPORT_ORBIT_MIN_HALF_WIDTH_M = 2 * 1852.0


def support_half_width(flight: FlightData) -> Optional[float]:
    """Half-width of the box a support orbit fills, from the flight's orbit
    speed. None without one."""
    if flight.patrol_speed is None:
        return None
    speed = flight.patrol_speed.meters_per_second
    turn = speed * speed / (9.81 * math.tan(math.radians(SUPPORT_ORBIT_TURN_BANK_DEG)))
    return max(SUPPORT_ORBIT_MIN_HALF_WIDTH_M, turn + SUPPORT_ORBIT_TURN_PAD_M)


#: Corners plus the repeat that closes the figure. No display auto-closes a
#: line: the Hornet's FAOR and the Viper's GEO sets both draw segments between
#: consecutive points and stop.
SUPPORT_BOX_POINTS = 5


def _reference_point(flight: FlightData) -> Optional[Point]:
    """The flight's target, else its last waypoint: what "nearest" is measured from."""
    for waypoint in flight.waypoints:
        if is_target_waypoint(waypoint):
            return waypoint.position
    return flight.waypoints[-1].position if flight.waypoints else None


def nearest_tanker_tracks(
    flight: FlightData, mission_data: MissionData
) -> list[SupportTrack]:
    """The tanker orbits, nearest to the flight's target first.

    The Hornet's SA page draws only FAOR line 1, so line 1 is the tanker nearest
    the fight. No boom/probe filter: nothing in the game records which tanker a
    jet can take gas from. The AWACS never gets a box.
    """
    tankers = [track for track in support_tracks(mission_data) if track.kind == "TKR"]
    reference = _reference_point(flight)
    if reference is not None:
        tankers.sort(key=lambda t: math.dist(t.center, (reference.x, reference.y)))
    return tankers


def support_boxes(
    mission_data: MissionData, max_boxes: int, flight: Optional[FlightData] = None
) -> list[tuple[str, list[tuple[float, float]]]]:
    """Each tanker orbit as a closed box, (callsign, 5 points).

    The orbits already ride the jets as points, but on the Hornet's SA page only
    the SELECTED CAP point draws its racetrack, so the gas is invisible until you
    go looking for it. With ``flight`` given the boxes are
    :func:`nearest_tanker_tracks`; without it, every support orbit.
    """
    boxes: list[tuple[str, list[tuple[float, float]]]] = []
    tracks = (
        nearest_tanker_tracks(flight, mission_data)
        if flight is not None
        else support_tracks(mission_data)
    )
    for track in tracks[:max_boxes]:
        half_width = (
            track.half_width_m
            if track.half_width_m is not None
            else SUPPORT_ORBIT_DIAMETER_M / 2
        )
        half_length = track.length_m / 2 + half_width
        course = math.radians(track.course)
        # DCS x is north, y east, and `bearing_degrees` is a compass bearing.
        along = (math.cos(course), math.sin(course))
        across = (-math.sin(course), math.cos(course))
        centre_x, centre_y = track.center
        corners = [
            (
                centre_x + along[0] * length + across[0] * width,
                centre_y + along[1] * length + across[1] * width,
            )
            for length, width in (
                (half_length, half_width),
                (half_length, -half_width),
                (-half_length, -half_width),
                (-half_length, half_width),
            )
        ]
        boxes.append((track.callsign, corners + [corners[0]]))
    return boxes


def _chain_bars(bars: list[list[tuple[float, float]]]) -> list[tuple[float, float]]:
    """Order and orient the front bars into one continuous trace.

    A theater's fronts are separate bars with uncontested border between them.
    The gaps are joined straight: nothing in the campaign model says where an
    unopposed border runs, and a straight join cannot invent a salient.
    """
    if not bars:
        return []
    remaining = list(bars)
    # Start from the endpoint farthest from the set's centroid, so the chain
    # runs across the theater instead of outward from its middle.
    ends = [point for bar in remaining for point in (bar[0], bar[-1])]
    centroid = (
        sum(x for x, _ in ends) / len(ends),
        sum(y for _, y in ends) / len(ends),
    )
    first = max(
        remaining,
        key=lambda bar: max(math.dist(bar[0], centroid), math.dist(bar[-1], centroid)),
    )
    remaining.remove(first)
    if math.dist(first[-1], centroid) > math.dist(first[0], centroid):
        first = first[::-1]
    chain = list(first)
    while remaining:
        tail = chain[-1]
        best = min(
            remaining,
            key=lambda bar: min(math.dist(tail, bar[0]), math.dist(tail, bar[-1])),
        )
        remaining.remove(best)
        if math.dist(tail, best[-1]) < math.dist(tail, best[0]):
            best = best[::-1]
        chain.extend(best)
    return chain


def decimate_open(
    points: list[tuple[float, float]], max_points: int
) -> list[tuple[float, float]]:
    """Thin an open polyline to `max_points`, keeping both ends."""
    if max_points < 2 or len(points) <= max_points:
        return points
    step = (len(points) - 1) / (max_points - 1)
    kept = [points[round(index * step)] for index in range(max_points)]
    kept[-1] = points[-1]
    return kept


def red_land_boundary(
    game: Game, max_lines: int, max_points_per_line: int
) -> list[tuple[str, list[tuple[float, float]]]]:
    """The land boundary with red, as runs fitting the display's line budget.

    One continuous trace, not a front per line: the pilot reads which side of
    the line is hostile, and disconnected stubs cannot say it. Consecutive runs
    repeat the vertex they meet on, so the display draws them as one line.
    """
    bars = [points for _, points in flot_segments(game) if len(points) >= 2]
    chain = _chain_bars(bars)
    if len(chain) < 2:
        return []
    # The repeated meeting vertices come out of the budget.
    budget = max_lines * max_points_per_line - (max_lines - 1)
    chain = decimate_open(chain, budget)
    runs: list[list[tuple[float, float]]] = []
    index = 0
    while index < len(chain) - 1 and len(runs) < max_lines:
        runs.append(chain[index : index + max_points_per_line])
        index += max_points_per_line - 1
    if len(runs) == 1:
        return [("FLOT", runs[0])]
    return [(f"FLOT {n}", points) for n, points in enumerate(runs, start=1)]


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
