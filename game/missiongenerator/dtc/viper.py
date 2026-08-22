"""F-16C DTC cartridge builder.

Sections emitted (schema mined from ``CoreMods/aircraft/F-16C/DTC``):

* No ``COMM``: the Viper's channel schema has no name field, so the section
  could only mirror the ``Radio`` table upstream's channel allocator already
  writes into the unit. Dropped 2026-08-22 -- the presets come from the miz.
* ``MPD.NAV_PTS`` -- steerpoints with TOS + per-leg speed inline (the Viper
  keeps route timing on the point, unlike the Hornet's separate route table),
  labelled in ``note`` -- the DTC Manager's reference label, which the jet does
  not upload (F-16C manual, NAV RTE tab); the flight route first, then the
  flight's OWN orbit (racetrack or hold point) and the tanker / AEW&C anchors as
  extra steerpoints (the jet has no orbit element). The editor caps the list at
  25 and the jet auto-sequences only 1-20, so the route takes 1-20 and anchors
  21-25.
* ``MPD.GEO_LINES`` -- the active front lines (FLOT) as up to 4 line sets on
  the HSD, capped at the partition's 25 points.
* ``MPD.THREAT_PTS`` -- enemy SAM rings ("Custom" type, radius in meters,
  <= 15).
* ``MPD.DEST`` -- friendly recovery fields as Destination steerpoints 81-99,
  labelled with the HSD's 3-character Destination text, plus the hostile field
  the flight is working over when there is one within 10 NM of the target.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from game.missiongenerator.dtc.cartridge import DtcCartridge
from game.missiongenerator.dtc.common import (
    SupportTrack,
    leg_altitude,
    steerpoint_elevation,
    flot_segments,
    is_route_waypoint,
    is_target_waypoint,
    known_enemy_threat_sites,
    leg_speed_kmh,
    own_orbit_track,
    seconds_of_day,
    support_tracks,
    waypoint_display_name,
)

if TYPE_CHECKING:
    from game import Game
    from game.ato.flightwaypoint import FlightWaypoint
    from game.missiongenerator.aircraft.flightdata import FlightData
    from game.missiongenerator.missiondata import MissionData

VIPER_UNIT_TYPE = "F-16C_50"

MAX_STEERPOINTS = 25
#: The jet auto-sequences only from STPT 1-20 (EA guide p223), so the flown
#: route stops there and the support anchors take 21-25.
MAX_ROUTE_STEERPOINTS = 20
MAX_GEO_LINE_SETS = 4
#: GEO_LINES owns steerpoints 31-55: ``GEO_LINES.lua`` refuses a 26th point,
#: which would land in the pre-planned-threat partition at 56. The 25 are shared
#: across the four line sets with no per-set cap.
MAX_GEO_POINTS = 25
MAX_THREAT_POINTS = 15
#: DEST owns steerpoints 81-99, and the editor refuses a 20th.
MAX_DESTINATIONS = 19
#: A hostile field within this of the target is the one the flight is working
#: over, so it goes on the DEST page beside the recovery options.
TARGET_AIRFIELD_RADIUS_M = 18520.0  # 10 NM

#: The Custom threat type's stock ceiling (meters; 30,000 ft) from
#: THREAT_PTS_defs.
_CUSTOM_THREAT_ALT = 9144


def _steerpoint(
    number: int,
    name: str,
    x: float,
    y: float,
    elevation_m: float,
    route_alt_m: float,
    altitude_type: int,
    on_route: bool,
    speed_kmh: float,
    tos: int,
    tos_enabled: bool,
    point_type: str,
) -> dict[str, Any]:
    return {
        "number": number,
        "id": f"STPT{number}",
        "type": point_type,
        "note": name,
        "x": x,
        "y": y,
        # The ground under the point, not the height to fly it at. ED fills this
        # from terrain (NAV_PTS.lua) and defaults a missing one to 2000 m.
        "alt": elevation_m,
        "altitudeType": altitude_type,
        "R1": on_route,
        "R2": False,
        "R3": False,
        "speed": speed_kmh,
        "velocityType": 3,
        "TOS": tos,
        "isTOSEnabled": tos_enabled,
        "FIX_Time": tos_enabled,
        "routeAltitude": route_alt_m,
        "isOAP_1": False,
        "idOA1": f"OA1{number}",
        "idOA1_Line": f"OA1{number}Line",
        "OAP_1_X": 0,
        "OAP_1_Y": 0,
        "OAP_1_Alt": 0,
        "OAP_1_Bearing": 0,
        "OAP_1_Range": 0,
        "OAP_1_DeltaX": 0,
        "OAP_1_DeltaY": 0,
        "isOAP_2": False,
        "idOA2": f"OA2{number}",
        "idOA2_Line": f"OA2{number}Line",
        "OAP_2_X": 0,
        "OAP_2_Y": 0,
        "OAP_2_Alt": 0,
        "OAP_2_Bearing": 0,
        "OAP_2_Range": 0,
        "OAP_2_DeltaX": 0,
        "OAP_2_DeltaY": 0,
    }


def _steerpoint_type(waypoint: FlightWaypoint) -> str:
    """STPT / IP / TGT -- the three HSD symbols (circle, square, triangle)."""
    if is_target_waypoint(waypoint):
        return "TGT"
    if "INGRESS" in waypoint.waypoint_type.name:
        return "IP"
    return "STPT"


def _dest_label(name: str, taken: set[str]) -> str:
    """The HSD draws a Destination as up to 3 alphanumerics (EA guide p203)."""
    base = "".join(c for c in name.upper() if c.isalnum())[:3] or "DST"
    label, suffix = base, 2
    while label in taken and suffix < 100:
        tail = str(suffix)
        label = f"{base[: 3 - len(tail)]}{tail}"
        suffix += 1
    taken.add(label)
    return label


def _dest_reference(flight: FlightData) -> Any:
    """Sort destinations by distance from the target, else the last waypoint."""
    for waypoint in flight.waypoints:
        if is_target_waypoint(waypoint):
            return waypoint.position
    return flight.waypoints[-1].position if flight.waypoints else None


def _target_airfield(flight: FlightData, game: Game) -> Any:
    """The hostile field the flight is working over, if there is one.

    Not a recovery option -- it earns a Destination slot because the HSD is
    where the crew wants the field they are attacking or fighting above, and
    only the DEST partition draws an airfield. Keep it out of the divert slot.
    """
    reference = _dest_reference(flight)
    if reference is None:
        return None
    nearest = None
    closest = TARGET_AIRFIELD_RADIUS_M
    for cp in game.theater.controlpoints:
        if not cp.captured.is_red or cp.is_fleet:
            continue
        distance = cp.position.distance_to_point(reference)
        if distance <= closest:
            nearest, closest = cp, distance
    return nearest


def _build_dest(flight: FlightData, game: Game) -> list[dict[str, Any]]:
    """Recovery fields as Destination steerpoints, plus the target's field.

    The briefed divert leads the list, the hostile field the flight is working
    over follows it so the cap can never squeeze it out, and the rest sort by
    distance from the target so the nearest alternates fill the 19 slots.
    """
    reference = _dest_reference(flight)
    divert_name = flight.divert.airfield_name if flight.divert else None
    fields = []
    for cp in game.theater.controlpoints:
        if cp.captured.is_red or not cp.runway_is_operational():
            continue
        distance = (
            cp.position.distance_to_point(reference) if reference is not None else 0.0
        )
        fields.append((cp.name != divert_name, distance, cp))
    fields.sort(key=lambda entry: (entry[0], entry[1]))
    ordered = [cp for _, _, cp in fields]

    hostile = _target_airfield(flight, game)
    if hostile is not None:
        ordered.insert(1 if ordered else 0, hostile)

    taken: set[str] = set()
    return [
        {
            "number": index,
            "id": f"DEST{80 + index}",
            "x": cp.position.x,
            "y": cp.position.y,
            # The generator has no terrain height source; the jet reads 0.
            "alt": 0,
            "text": _dest_label(cp.name, taken),
            "note": cp.name,
        }
        for index, cp in enumerate(ordered[:MAX_DESTINATIONS], start=1)
    ]


def _anchor_name(track: SupportTrack) -> str:
    return f"{track.kind} {track.callsign}".strip()


def _build_nav_pts(
    flight: FlightData, mission_data: MissionData, game: Game
) -> list[dict[str, Any]]:
    options = flight.dtc_options
    points: list[dict[str, Any]] = []
    prev_route_wp = None
    # Match the kneeboard's numbering: its row 0 (takeoff/spawn) is not
    # emitted, so STPT n in the jet is kneeboard waypoint n (the flown
    # Hornet off-by-one applied here identically).
    waypoints = flight.waypoints[1:] if options.route else []
    for waypoint in waypoints:
        if len(points) >= MAX_ROUTE_STEERPOINTS:
            break
        number = len(points) + 1
        on_route = is_route_waypoint(waypoint)
        route_alt_m, altitude_type = leg_altitude(waypoint)
        points.append(
            _steerpoint(
                number,
                waypoint_display_name(waypoint.display_name or waypoint.name),
                waypoint.position.x,
                waypoint.position.y,
                steerpoint_elevation(waypoint),
                route_alt_m,
                altitude_type,
                on_route,
                leg_speed_kmh(prev_route_wp if on_route else None, waypoint),
                seconds_of_day(game, waypoint.tot),
                waypoint.tot is not None,
                _steerpoint_type(waypoint),
            )
        )
        if on_route:
            prev_route_wp = waypoint
    # Support anchors after the route: this flight's own orbit (racetrack, or
    # the hold point when it flies none), then the tanker/AEW&C orbits -- the
    # Viper's stand-in for the Hornet's SA racetracks. Other flights' CAP
    # stations are not this jet's business.
    if options.friendly_orbits:
        own = own_orbit_track(flight)
        anchors = ([own] if own is not None else []) + support_tracks(mission_data)
        for track in anchors:
            if len(points) >= MAX_STEERPOINTS:
                break
            number = len(points) + 1
            x, y = track.center
            points.append(
                _steerpoint(
                    number,
                    _anchor_name(track),
                    x,
                    y,
                    0.0,  # elevation: an orbit anchor has no ground of its own
                    0.0,  # route altitude: not a leg the jet is sequenced through
                    1,
                    False,
                    463.0,
                    0,
                    False,
                    "STPT",
                )
            )
    return points


def _build_geo_lines(game: Game) -> list[dict[str, Any]]:
    """FLOT boundaries across the HSD's four line sets."""
    line_sets: list[tuple[str, list[tuple[float, float]]]] = []
    line_sets.extend(flot_segments(game))
    geo_points: list[dict[str, Any]] = []
    for set_index, (name, points) in enumerate(line_sets[:MAX_GEO_LINE_SETS]):
        flags = {f"L{i}": i == set_index + 1 for i in range(1, 5)}
        for x, y in points:
            if len(geo_points) >= MAX_GEO_POINTS:
                return geo_points
            number = len(geo_points) + 1
            entry: dict[str, Any] = {
                "number": number,
                "id": f"GEO_LINES{30 + number}",
                "x": x,
                "y": y,
                "alt": 0,
                "note": name,
            }
            entry.update(flags)
            geo_points.append(entry)
    return geo_points


def _build_threat_pts(flight: FlightData, game: Game) -> list[dict[str, Any]]:
    threats: list[dict[str, Any]] = []
    for site in known_enemy_threat_sites(game)[:MAX_THREAT_POINTS]:
        number = len(threats) + 1
        threats.append(
            {
                "number": number,
                "id": f"THREAT_PTS{55 + number}",
                "x": site.x,
                "y": site.y,
                "threatName": "Custom",
                "radius": site.range_m,
                "alt": _CUSTOM_THREAT_ALT,
                "elev": 0,
                "text": site.label,
                "ring": True,
                "def_num": 1,
            }
        )
    return threats


def build_viper_cartridge(
    flight: FlightData, mission_data: MissionData, game: Game, name: str
) -> DtcCartridge:
    terrain = game.theater.terrain.name
    options = flight.dtc_options
    data: dict[str, Any] = {
        "type": VIPER_UNIT_TYPE,
        "name": name,
        "terrain": terrain,
    }
    # A section the planner turned off is omitted entirely so the jet's own
    # defaults stand.
    if (
        options.route
        or options.friendly_orbits
        or options.flot_and_zones
        or options.threat_rings
        or options.destinations
    ):
        data["MPD"] = {
            "terrain": terrain,
            "mirror_NAV_PTS": False,
            "NAV_PTS": _build_nav_pts(flight, mission_data, game),
            "mirror_GEO_LINES": False,
            "GEO_LINES": _build_geo_lines(game) if options.flot_and_zones else [],
            "mirror_THREAT_PTS": False,
            "THREAT_PTS": (
                _build_threat_pts(flight, game) if options.threat_rings else []
            ),
            "mirror_DEST": False,
            "DEST": _build_dest(flight, game) if options.destinations else [],
        }
    return DtcCartridge(
        name=name, unit_type=VIPER_UNIT_TYPE, terrain=terrain, data=data
    )
