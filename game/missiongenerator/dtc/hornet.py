"""FA-18C DTC cartridge builder.

Sections emitted (schema mined from ``CoreMods/aircraft/FA-18C/DTC``):

* No ``COMM``: the presets already reach the jet through the ``Radio`` table
  the radio allocator writes into the unit; the cartridge adds only what the
  miz cannot carry.
* ``WYPT`` -- the flight's waypoints as named steerpoints + the Route 1
  sequence with per-leg altitude/speed/ETA, and ``NAV_SETTINGS`` that auto-tune
  the recovery TACAN / ICLS / ACLS from the carrier's card and the FPAS home
  waypoint.
* ``SA`` -- FLOT line(s) from the live front; the flight's OWN orbit as the
  first, pre-selected CAP_PTS racetrack (its patrol track, or a stand-in at
  the hold point) followed by the tanker/AEW&C orbits; and enemy SAM rings
  as MEZ threats ("Custom" type; radius NM).
* ``TCN`` -- deliberately empty in v1 (the boat's TACAN already auto-tunes via
  NAV_SETTINGS; a stations list needs channel->frequency pairing, deferred).

Limits honored from the ME editor: 59 waypoints, 9 CAP points, 3 FAOR + 3
FLOT lines of 7 points, 40 MEZ threats.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

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
    from game.missiongenerator.aircraft.flightdata import FlightData
    from game.missiongenerator.missiondata import MissionData
    from game.missiongenerator.missiondata import CarrierInfo

HORNET_UNIT_TYPE = "FA-18C_hornet"

MAX_WAYPOINTS = 59
MAX_CAP_POINTS = 9
MAX_LINE_POINTS = 7
MAX_FLOT_LINES = 3
MAX_MEZ_THREATS = 40

#: CAP racetrack orbit diameter (the ME default, 5 NM).
_CAP_ORBIT_DIAMETER_M = 5 * 1852.0


def _oa_defaults(index: int) -> dict[str, Any]:
    """The offset-aimpoint boilerplate every ME-authored waypoint carries."""
    return {
        "isOA": False,
        "idOA": f"OA{index}",
        "idOA_Line": f"OA{index}Line",
        "OA_X": 0,
        "OA_Y": 0,
        "OA_Alt": 0,
        "OA_Bearing": 0,
        "OA_Bearing_Units": 1,
        "OA_Range": 0,
        "OA_Range_Units": 1,
        "OA_DeltaX": 0,
        "OA_DeltaY": 0,
        "OA_Elevation_Units": 1,
    }


def _nav_settings_defaults(home_wypt: int) -> dict[str, Any]:
    """The module's stock (everything off) NAV settings, for a cartridge whose
    planner turned the recovery-aids section off."""
    return {
        "TACAN": {"Mode": 1, "Channel": 1, "ChannelMode": 1, "OnOff": False},
        "ICLS": {"Channel": 1, "OnOff": False},
        "ACLS": {"Frequency": 225.0, "OnOff": False},
        "AA_Waypoint": {"AA_WP_Number": 59, "AA_WP_Enabled": False},
        "Home_Waypoint": {"FPAS_HOME_WP": home_wypt},
        "Altitude_Warning": {"Warn_Alt_Rdr": 500, "Warn_Alt_Baro": 2000},
    }


def _build_wypt(
    flight: FlightData, game: Game, carrier: Optional[CarrierInfo]
) -> dict[str, Any]:
    options = flight.dtc_options
    nav_pts: list[dict[str, Any]] = []
    route_one: dict[str, Any] = {}
    home_wypt = 1
    aa_wypt: Optional[int] = None
    route_order = 0
    prev_route_wp = None
    # The kneeboard numbers the flight plan from 0 (row 0 = takeoff/spawn).
    # Skip that row so the jet's STPT n IS the kneeboard's waypoint n — the
    # flown off-by-one had every briefed number shifted (target "wp 4" was
    # STPT 5 in the jet). The dropped point is where the jet spawns anyway.
    waypoints = flight.waypoints[1 : MAX_WAYPOINTS + 1] if options.route else []
    for number, waypoint in enumerate(waypoints, start=1):
        on_route = is_route_waypoint(waypoint)
        route_alt_m, altitude_type = leg_altitude(waypoint)
        entry: dict[str, Any] = {
            "wypt_num": number,
            "id": f"STPT{number}",
            "text_note": waypoint_display_name(waypoint.display_name or waypoint.name),
            "note": "",
            "x": waypoint.position.x,
            "y": waypoint.position.y,
            # The ground under the point, not the height to fly it at. ED fills
            # this from terrain (WYPT_NAV.lua); the leg altitude rides NAV_ROUTE.
            "alt": steerpoint_elevation(waypoint),
            "altitudeType": altitude_type,
            "velocityType": 3,
            "R1": on_route,
            "R2": False,
            "R3": False,
        }
        entry.update(_oa_defaults(number))
        if on_route:
            route_order += 1
            entry["R1_order"] = route_order
            route_one[f"STPT{number}"] = {
                "route_num": 1,
                "wypt_num": number,
                "alt": route_alt_m,
                "altitudeType": entry["altitudeType"],
                "speed": leg_speed_kmh(prev_route_wp, waypoint),
                "ETA": seconds_of_day(game, waypoint.tot),
                "FIX_Time": waypoint.tot is not None,
                "TGT": is_target_waypoint(waypoint),
            }
            prev_route_wp = waypoint
        nav_pts.append(entry)
        if "LANDING" in waypoint.waypoint_type.name:
            home_wypt = number
        elif waypoint.waypoint_type.name == "BULLSEYE":
            aa_wypt = number
    if options.nav_aids:
        nav_settings = _build_nav_settings(flight, carrier, home_wypt, aa_wypt)
    else:
        nav_settings = _nav_settings_defaults(home_wypt)
    return {
        "NAV_PTS": nav_pts,
        "NAV_ROUTE": [route_one, [], []],
        "NAV_SETTINGS": nav_settings,
        "terrain": game.theater.terrain.name,
        "mirror_NAV_PTS": False,
    }


def _find_carrier(
    flight: FlightData, mission_data: MissionData
) -> Optional[CarrierInfo]:
    """The carrier this flight recovers on, if its arrival is a boat."""
    arrival_name = flight.arrival.airfield_name
    for carrier in mission_data.carriers:
        if carrier.unit_name in arrival_name or arrival_name in carrier.unit_name:
            return carrier
        if carrier.callsign and carrier.callsign in arrival_name:
            return carrier
    return None


def _build_nav_settings(
    flight: FlightData,
    carrier: Optional[CarrierInfo],
    home_wypt: int,
    aa_wypt: Optional[int] = None,
) -> dict[str, Any]:
    """Recovery aids plus the A/A (bullseye) waypoint designation.

    The A/A waypoint has to BE a waypoint in the database (EA guide p158), and
    designating it is otherwise three cockpit presses the pilot makes every
    sortie. We point it at the bullseye we already emit rather than the jet's
    stock slot 59, which our routes never reach.
    """
    # A land start tunes the departure field's TACAN when it has one; a boat
    # recovery keeps the boat's card; otherwise the arrival's.
    tacan = (
        carrier.tacan
        if carrier is not None
        else flight.departure.tacan or flight.arrival.tacan
    )
    icls = carrier.icls_channel if carrier is not None else flight.arrival.icls
    acls_freq = (
        carrier.link4_freq.mhz
        if carrier is not None and carrier.link4_freq is not None
        else None
    )
    tacan_settings: dict[str, Any] = {
        "Mode": 1,  # T/R
        "Channel": 1,
        "ChannelMode": 1,  # X
        "OnOff": False,
    }
    if tacan is not None:
        tacan_settings = {
            "Mode": 1,
            "Channel": tacan.number,
            "ChannelMode": 2 if getattr(tacan.band, "value", "X") == "Y" else 1,
            "OnOff": True,
        }
    return {
        "TACAN": tacan_settings,
        "ICLS": {
            "Channel": icls if icls is not None else 1,
            "OnOff": icls is not None,
        },
        "ACLS": {
            "Frequency": acls_freq if acls_freq is not None else 225.0,
            "OnOff": acls_freq is not None,
        },
        "AA_Waypoint": {
            "AA_WP_Number": aa_wypt if aa_wypt is not None else 59,
            "AA_WP_Enabled": aa_wypt is not None,
        },
        "Home_Waypoint": {"FPAS_HOME_WP": home_wypt},
        "Altitude_Warning": {"Warn_Alt_Rdr": 500, "Warn_Alt_Baro": 2000},
    }


def _cap_point(track: SupportTrack, number: int) -> dict[str, Any]:
    x, y = track.center
    return {
        "id": f"CAP_PTS_{number}",
        "num": number,
        "x": x,
        "y": y,
        "course": track.course,
        "length": track.length_m,
        "diameter": _CAP_ORBIT_DIAMETER_M,
        "turn_direction": "Left",
        "note": track.callsign,
    }


def _line_points(
    prefix: str, line_num: int, points: list[tuple[float, float]]
) -> list[dict[str, Any]]:
    return [
        {"id": f"{prefix}_{line_num}_PT_{i}", "x": x, "y": y}
        for i, (x, y) in enumerate(points[:MAX_LINE_POINTS], start=1)
    ]


def _build_sa(
    flight: FlightData, mission_data: MissionData, game: Game
) -> dict[str, Any]:
    options = flight.dtc_options
    caps: list[dict[str, Any]] = []
    default_cap_point = 1
    if options.friendly_orbits:
        # This flight's own orbit first -- its racetrack when it flies one, a
        # stand-in at the hold point when it does not -- then the tanker and
        # AEW&C orbits, so "where's my gas" stays answerable. Other flights'
        # CAP stations are not this jet's business and stay off the page. The
        # SA page DISPLAYS one CAP point at a time -- the selected one (flown
        # 2026-07-19) -- so entry 1 being your own orbit is what spawns up.
        own = own_orbit_track(flight)
        ordered = ([own] if own is not None else []) + support_tracks(mission_data)
        for track in ordered[:MAX_CAP_POINTS]:
            caps.append(_cap_point(track, len(caps) + 1))

    flot_lines: list[dict[str, Any]] = []
    if options.flot_and_zones:
        for name, points in flot_segments(game)[:MAX_FLOT_LINES]:
            line_num = len(flot_lines) + 1
            flot_lines.append(
                {
                    "id": f"FLOT_{line_num}",
                    "num": line_num,
                    "note": name,
                    "points": _line_points("FLOT", line_num, points),
                }
            )

    threats: list[dict[str, Any]] = []
    if options.threat_rings:
        for site in known_enemy_threat_sites(game)[:MAX_MEZ_THREATS]:
            number = len(threats) + 1
            threats.append(
                {
                    "id": f"MEZ_THRTS_{number}",
                    "num": number,
                    "x": site.x,
                    "y": site.y,
                    "text": site.label,
                    "threat_type": "Custom",
                    "threat_ring_radius": round(site.range_m / 1852.0, 1),
                    "threat_level": 1,
                }
            )

    return {
        "CAP_PTS": caps,
        "CORRIDORS": [],
        "FAOR_FLOT": {"FAOR": [], "FLOT": flot_lines},
        "MEZ_THRTS": threats,
        "SETTINGS": _sa_settings(),
        "Default_CAP_Point": default_cap_point,
        "Default_CORRIDORS_Point": 1,
        "Default_FAOR_Line": 1,
        "Default_FLOT_Line": 1,
        "Default_MEZ_THRTS_Level": 1,
        "mirror_MEZ_THRTS": False,
    }


def _sa_settings() -> dict[str, Any]:
    """The module's stock SA sensor/declutter settings (everything shown)."""
    dcltr = {
        "Bullseye_TDC_Info": True,
        "Waypoint_Info": True,
        "Compase_Rose": True,
        "Ground_Speed": True,
        "Countermeasure_Inventory": True,
        "SEQ": True,
        "CAP": True,
        "CORR": True,
        "FAOR": True,
        "FLOT": True,
        "MEZ_Names": True,
        "MEZ_Rings": True,
    }
    return {
        "SENSORS_SETTINGS": {
            "RWR_Symbols": 1,
            "FRIEND_Symbols": 3,
            "PPLI_tracks": True,
            "FF_tracks": True,
            "SURV_tracks": True,
            "UNK_tracks": True,
        },
        "DCLTR_SETTINGS": {"MREJ1": dict(dcltr), "MREJ2": dict(dcltr)},
    }


def build_hornet_cartridge(
    flight: FlightData, mission_data: MissionData, game: Game, name: str
) -> DtcCartridge:
    terrain = game.theater.terrain.name
    options = flight.dtc_options
    data: dict[str, Any] = {
        "TCN": [],
        "type": HORNET_UNIT_TYPE,
        "name": name,
        "terrain": terrain,
    }
    # A section the planner turned off is omitted entirely so the jet's own
    # defaults stand.
    if options.route or options.nav_aids:
        carrier = _find_carrier(flight, mission_data)
        data["WYPT"] = _build_wypt(flight, game, carrier)
    if options.flot_and_zones or options.friendly_orbits or options.threat_rings:
        data["SA"] = _build_sa(flight, mission_data, game)
    return DtcCartridge(
        name=name, unit_type=HORNET_UNIT_TYPE, terrain=terrain, data=data
    )
