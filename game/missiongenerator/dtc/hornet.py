"""FA-18C DTC cartridge builder.

Sections emitted (schema mined from ``CoreMods/aircraft/FA-18C/DTC``):

* ``COMM`` -- COMM1/COMM2 mirroring the unit's ``Radio`` table, each channel
  named (<=5 chars) after what it tunes. The names are what the miz cannot
  carry; the frequencies are the miz's own, so the cartridge changes none.
* ``WYPT`` -- the flight's waypoints as named steerpoints + the Route 1
  sequence with per-leg altitude/speed/ETA, and ``NAV_SETTINGS`` that auto-tune
  the recovery TACAN / ICLS / ACLS from the carrier's card and the FPAS home
  waypoint.
* ``SA`` -- the front lines chained into one continuous boundary across the
  FLOT lines; the flight's OWN orbit as the
  first, pre-selected CAP_PTS racetrack (its patrol track, or a stand-in at
  the hold point) followed by the tanker/AEW&C orbits; the tanker orbits as
  FAOR boxes, nearest to the target first; the package's lane from the IP
  over the target to the split as the corridor; and enemy SAM rings as MEZ
  threats ("Custom" type; radius NM).
* ``TCN`` -- the TACAN stations: the friendly boats, the home, arrival and
  divert fields, then the map's other ground TACANs nearest the route first.

Limits honored from the ME editor: 59 waypoints, 9 CAP points, 3 FAOR + 3
FLOT lines of 7 points, one corridor of 14, 40 MEZ threats, 10 TACANs.
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING, Any, Optional

from game.dcs.beacons import Beacon, Beacons
from game.missiongenerator.dtc.cartridge import DtcCartridge
from game.missiongenerator.dtc.common import (
    SupportTrack,
    decimate_open,
    frequency_labels,
    leg_altitude,
    steerpoint_altitude,
    red_land_boundary,
    support_boxes,
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
#: The SA page draws only the SELECTED CAP point's racetrack, and only FAOR
#: line 1, so line 1 is the tanker nearest the target.
MAX_FAOR_LINES = 3
MAX_MEZ_THREATS = 40
#: The SA page draws one corridor of up to 14 points (``CORRIDORS.lua``).
MAX_CORRIDOR_POINTS = 14
#: The editor refuses an 11th TACAN station (``TCN/TACAN.lua``).
MAX_TACAN_STATIONS = 10

#: The module's stock COMM1/COMM2 channels 1-20 (MHz), for a unit with no
#: ``Radio`` table.
_DEFAULT_CHANNEL_FREQS = [
    305.0, 264.0, 265.0, 256.0, 254.0, 250.0, 270.0, 257.0, 255.0, 262.0,
    259.0, 268.0, 269.0, 260.0, 263.0, 261.0, 267.0, 251.0, 253.0, 266.0,
]  # fmt: skip
#: The ARC-210 presets 1-20; G, M, C and S are fixed selector positions.
_MAX_CHANNELS = 20

#: CAP racetrack orbit diameter (the ME default, 5 NM).
_CAP_ORBIT_DIAMETER_M = 5 * 1852.0


def _channel(frequency: float, name: str) -> dict[str, Any]:
    # Everything Retribution presets below the VHF-AM band is FM (modulation 1).
    return {
        "frequency": frequency,
        "modulation": 1 if frequency < 88.0 else 0,
        "name": name,
    }


def _build_comm(flight: FlightData, mission_data: MissionData) -> dict[str, Any]:
    labels = frequency_labels(flight, mission_data)
    presets = flight.client_units[0].radio if flight.client_units else None
    comm: dict[str, Any] = {}
    for radio_id in (1, 2):
        channels: dict[int, float] = dict(enumerate(_DEFAULT_CHANNEL_FREQS, start=1))
        if presets and radio_id in presets:
            channels.update(presets[radio_id]["channels"])
        table: dict[str, Any] = {"Guard": False}
        for number in range(1, _MAX_CHANNELS + 1):
            freq = float(channels[number])
            name = labels.get(round(freq, 3), f"CH {number}")
            table[f"Channel_{number}"] = _channel(freq, name)
        table["Channel_G"] = _channel(243.0, "GUARD")
        table["Channel_M"] = _channel(305.0, "MAN")
        table["Channel_C"] = _channel(30.0, "CUE")
        table["Channel_S"] = _channel(156.05, "MAR")
        comm[f"COMM{radio_id}"] = table
        comm[f"mirror_COMM{radio_id}"] = False
    return comm


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


#: WYPT_NAV.lua's own limits on a waypoint's elevation. The route entry's cap
#: is 80,000 ft (ROUTE_SEQ.lua), so a leg above 25,000 ft keeps its number there.
_WYPT_ALT_MIN_M = -2000 * 0.3048
_WYPT_ALT_MAX_M = 25000 * 0.3048


def _build_wypt(
    flight: FlightData, game: Game, carrier: Optional[CarrierInfo]
) -> dict[str, Any]:
    options = flight.dtc_options
    nav_pts: list[dict[str, Any]] = []
    route_one: dict[str, Any] = {}
    home_wypt = 1
    aa_wypt: Optional[int] = None
    route_order = 0
    target_flagged = False
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
            # The HSI's waypoint elevation, the number the miz route gives the
            # jet; NAV_ROUTE below carries the DTC Manager's planning copy.
            "alt": min(
                max(steerpoint_altitude(waypoint), _WYPT_ALT_MIN_M), _WYPT_ALT_MAX_M
            ),
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
                # One TGT per sequence (ROUTE_SEQ.lua): the first target.
                "TGT": is_target_waypoint(waypoint) and not target_flagged,
            }
            target_flagged = target_flagged or is_target_waypoint(waypoint)
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


def _ship_tacan(carrier: CarrierInfo) -> Optional[dict[str, Any]]:
    """A boat's station, keyed the way the editor keys a ship's ActivateBeacon
    task: the unit's id and the route point that carries it (point 1)."""
    group = carrier.ship_group
    if not group.units or not group.points:
        return None
    unit = group.units[0]
    position = group.points[0].position
    return {
        "callsign": carrier.callsign,
        "channel": carrier.tacan.number,
        "modeChannel": carrier.tacan.band.value,
        "display_name": f"{unit.name}_P1",
        "elevation": 0,
        "unitId": unit.id,
        "unitPointNum": 1,
        "x": position.x,
        "y": position.y,
    }


def _ground_tacan(beacon: Beacon) -> Optional[dict[str, Any]]:
    """A ground station, keyed by the beacon's own name as the editor keys it."""
    if not beacon.is_tacan or beacon.channel is None or beacon.x is None:
        return None
    station: dict[str, Any] = {
        "callsign": beacon.callsign,
        "channel": beacon.channel,
        "display_name": beacon.name,
        "elevation": beacon.elevation or 0,
        "x": beacon.x,
        "y": beacon.y,
    }
    if beacon.hertz is not None:
        station["frequency"] = beacon.hertz
    return station


def _field_tacans(game: Game, airfield_name: str) -> list[dict[str, Any]]:
    """The field's own ground TACANs, from the terrain's beacon data."""
    stations: list[dict[str, Any]] = []
    for airport in game.theater.terrain.airports.values():
        if airport.name != airfield_name:
            continue
        for beacon_data in airport.beacons:
            try:
                beacon = Beacons.with_id(beacon_data.id, game.theater)
            except KeyError:
                continue
            station = _ground_tacan(beacon)
            if station is not None:
                stations.append(station)
    return stations


def _build_tcn(
    flight: FlightData, mission_data: MissionData, game: Game
) -> list[dict[str, Any]]:
    """The jet's TACAN station list: our boats, the home, arrival and divert
    fields, then every other TACAN on the map nearest the route first, to the
    editor's 10. Tankers cannot be listed: the editor takes only ships and
    ground beacons."""
    stations: list[dict[str, Any]] = []

    def add(station: Optional[dict[str, Any]]) -> None:
        if station is not None and all(
            s["display_name"] != station["display_name"] for s in stations
        ):
            stations.append(station)

    for carrier in mission_data.carriers:
        if carrier.blue.is_blue == flight.friendly.is_blue:
            add(_ship_tacan(carrier))
    for runway in (flight.departure, flight.arrival, flight.divert):
        if runway is not None:
            for station in _field_tacans(game, runway.airfield_name):
                add(station)
    route = [w.position for w in flight.waypoints if is_route_waypoint(w)]
    others = [
        station
        for station in map(_ground_tacan, Beacons.iter_theater(game.theater))
        if station is not None
    ]
    if route:
        others.sort(
            key=lambda s: min(math.hypot(s["x"] - p.x, s["y"] - p.y) for p in route)
        )
    for station in others:
        add(station)
    return stations[:MAX_TACAN_STATIONS]


def _attack_lane(flight: FlightData) -> list[tuple[float, float]]:
    """The package's path from the IP over the target to the split. Empty for a
    flight with no IP, or with no split after it (CAS, Sweep): that lane would
    run on to landing and divert."""
    points: list[tuple[float, float]] = []
    for waypoint in flight.waypoints:
        name = waypoint.waypoint_type.name
        if not points and not name.startswith("INGRESS_"):
            continue
        points.append((waypoint.position.x, waypoint.position.y))
        if name == "SPLIT":
            return points
    return []


def _build_corridors(flight: FlightData) -> list[dict[str, Any]]:
    """The SA page's one corridor: the attack lane."""
    lane = decimate_open(_attack_lane(flight), MAX_CORRIDOR_POINTS)
    if not lane:
        return []
    return [
        {
            "id": "CORR_1",
            "num": 1,
            "note": "ATTACK",
            "points": [
                {"id": f"CORR_1_PT_{i}", "x": x, "y": y}
                for i, (x, y) in enumerate(lane, start=1)
            ],
        }
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
        for name, points in red_land_boundary(game, MAX_FLOT_LINES, MAX_LINE_POINTS):
            line_num = len(flot_lines) + 1
            flot_lines.append(
                {
                    "id": f"FLOT_{line_num}",
                    "num": line_num,
                    "note": name,
                    "points": _line_points("FLOT", line_num, points),
                }
            )

    faor_lines: list[dict[str, Any]] = []
    if options.friendly_orbits:
        for callsign, points in support_boxes(mission_data, MAX_FAOR_LINES, flight):
            line_num = len(faor_lines) + 1
            faor_lines.append(
                {
                    "id": f"FAOR_{line_num}",
                    "num": line_num,
                    "note": callsign,
                    "points": _line_points("FAOR", line_num, points),
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
        "CORRIDORS": _build_corridors(flight) if options.route else [],
        "FAOR_FLOT": {"FAOR": faor_lines, "FLOT": flot_lines},
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
        "TCN": _build_tcn(flight, mission_data, game) if options.nav_aids else [],
        "type": HORNET_UNIT_TYPE,
        "name": name,
        "terrain": terrain,
    }
    # A section the planner turned off is omitted entirely so the jet's own
    # defaults stand.
    if options.comms:
        data["COMM"] = _build_comm(flight, mission_data)
    if options.route or options.nav_aids:
        carrier = _find_carrier(flight, mission_data)
        data["WYPT"] = _build_wypt(flight, game, carrier)
    if options.flot_and_zones or options.friendly_orbits or options.threat_rings:
        data["SA"] = _build_sa(flight, mission_data, game)
    return DtcCartridge(
        name=name, unit_type=HORNET_UNIT_TYPE, terrain=terrain, data=data
    )
