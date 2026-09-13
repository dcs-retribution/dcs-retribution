"""Native DTC cartridge pre-population.

Locks the cartridge JSON shapes against the format mined from the DCS ME's own
DTC editor (``CoreMods/aircraft/<type>/DTC``) + a working MP mission: the
``DTC/<name>.dtc`` files, the per-unit ``DTC.Cartridges``/``AutoLoad`` block,
ETA/TOS as seconds since midnight, and the SA/HSD elements.
"""

from __future__ import annotations

import dataclasses
import json
import math
import zipfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Optional

import pytest
from dcs.mission import Mission
from dcs.planes import FA_18C_hornet
from dcs.terrain import Caucasus

from game.ato.flighttype import FlightType
from game.ato.flightwaypointtype import FlightWaypointType
from game.missiongenerator.dtc import DtcGenerator
from game.missiongenerator.dtc.cartridge import DtcCartridge
from game.missiongenerator.dtc.common import (
    known_enemy_threat_sites,
    sanitize_short_name,
    seconds_of_day,
)
from game.missiongenerator.dtc.generator import CARTRIDGE_BUILDERS
from game.missiongenerator.dtc.options import DtcOptions
from game.missiongenerator.dtc.hornet import build_hornet_cartridge
from game.missiongenerator.dtc.viper import build_viper_cartridge


class Pt:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def distance_to_point(self, other: "Pt") -> float:
        return math.hypot(self.x - other.x, self.y - other.y)


#: The waypoint types the flight plans mark as flyovers, which the miz then
#: puts on the deck for a client flight.
_FLYOVER_TYPES = (
    FlightWaypointType.CAS,
    FlightWaypointType.TARGET_GROUP_LOC,
    FlightWaypointType.TARGET_POINT,
    FlightWaypointType.TARGET_SHIP,
)


class _FakeUnit:
    """A client unit: records the pydcs DTC binding calls."""

    def __init__(self) -> None:
        self.dtc_cartridges: list[dict[str, Any]] = []
        self.dtc_autoload = False

    def add_dtc_cartridge(
        self, name: str, default: bool = True, autoload: bool = True
    ) -> None:
        self.dtc_cartridges.append({"name": name, "default": default})
        self.dtc_autoload = autoload


class _FakeMission:
    """The mission seam the generator writes cartridges into."""

    def __init__(self) -> None:
        self.dtc_cartridges: dict[str, str] = {}

    def add_dtc_cartridge(self, name: str, content: str) -> None:
        self.dtc_cartridges[name] = content


def _waypoint(
    name: str,
    waypoint_type: FlightWaypointType,
    x: float,
    y: float,
    alt_m: float,
    tot: Optional[datetime],
    *,
    alt_type: str = "BARO",
    targets: Optional[list[Any]] = None,
) -> Any:
    return SimpleNamespace(
        name=name,
        display_name=name,
        waypoint_type=waypoint_type,
        position=Pt(x, y),
        alt=SimpleNamespace(meters=alt_m),
        alt_type=alt_type,
        tot=tot,
        departure_time=None,
        targets=targets or [],
        # The flight-plan builders set flyover on the points a client flight
        # gets on the deck; these fakes mirror that by type.
        flyover=waypoint_type in _FLYOVER_TYPES,
    )


class _Freq:
    """Hashable RadioFrequency stand-in (SimpleNamespace defines __eq__ and
    loses hashability, but frequencies key the channel map)."""

    def __init__(self, mhz: float) -> None:
        self.mhz = mhz


def _freq(mhz: float) -> Any:
    return _Freq(mhz)


def _runway(name: str, atc_mhz: Optional[float] = None) -> Any:
    return SimpleNamespace(
        airfield_name=name,
        atc=_freq(atc_mhz) if atc_mhz is not None else None,
        tacan=None,
        tacan_callsign=None,
        icls=None,
    )


def _flight(
    *,
    dcs_id: str = "FA-18C_hornet",
    callsign: str = "Wizard 1",
    blue: bool = True,
    clients: int = 1,
    flight_type: FlightType = FlightType.STRIKE,
    waypoints: Optional[list[Any]] = None,
    channel_map: Optional[dict[Any, Any]] = None,
    arrival: Optional[Any] = None,
    dtc_options: Optional[DtcOptions] = None,
) -> Any:
    intra = _freq(258.5)
    return SimpleNamespace(
        callsign=callsign,
        friendly=SimpleNamespace(is_blue=blue),
        client_units=[_FakeUnit() for _ in range(clients)],
        aircraft_type=SimpleNamespace(dcs_unit_type=SimpleNamespace(id=dcs_id)),
        flight_type=flight_type,
        waypoints=waypoints or [],
        intra_flight_channel=intra,
        frequency_to_channel_map=channel_map or {},
        package=SimpleNamespace(frequency=None),
        departure=_runway("Kutaisi", 259.0),
        arrival=arrival if arrival is not None else _runway("Kutaisi", 259.0),
        divert=None,
        dtc_options=dtc_options if dtc_options is not None else DtcOptions(),
    )


def _support_flight(flight_type: FlightType, callsign: str, start: Pt, end: Pt) -> Any:
    waypoints = [
        _waypoint(
            "RACETRACK START",
            FlightWaypointType.PATROL_TRACK,
            start.x,
            start.y,
            6000,
            None,
        ),
        _waypoint("RACETRACK END", FlightWaypointType.PATROL, end.x, end.y, 6000, None),
    ]
    return _flight(
        callsign=callsign,
        flight_type=flight_type,
        clients=0,
        waypoints=waypoints,
    )


def _mission_data(flights: list[Any], carriers: Optional[list[Any]] = None) -> Any:
    return SimpleNamespace(
        flights=flights,
        awacs=[],
        tankers=[],
        jtacs=[],
        carriers=carriers or [],
    )


def _game(*, dtc_on: bool = True, controlpoints: Optional[list[Any]] = None) -> Any:
    return SimpleNamespace(
        settings=SimpleNamespace(dtc_data_cartridges=dtc_on),
        conditions=SimpleNamespace(start_time=datetime(1988, 7, 15, 7, 0)),
        theater=SimpleNamespace(
            terrain=SimpleNamespace(name="Caucasus"),
            timezone=timezone(timedelta(hours=4)),
            conflicts=lambda: [],
            controlpoints=controlpoints or [],
        ),
    )


def _sam_cp() -> Any:
    tgo = SimpleNamespace(
        name="SAM SA-2 Site",
        category="aa",
        max_threat_range=lambda: SimpleNamespace(meters=43000.0),
        position=Pt(120000, -30000),
        groups=[SimpleNamespace(units=[SimpleNamespace(type="SA-2 launcher")])],
    )
    return SimpleNamespace(
        name="SAM SA-2 Site",
        position=Pt(120000, -30000),
        is_fleet=False,
        captured=SimpleNamespace(is_red=True),
        ground_objects=[tgo],
        runway_is_operational=lambda: True,
    )


def _airbase_cp(
    name: str,
    x: float,
    y: float,
    *,
    red: bool = False,
    operational: bool = True,
) -> Any:
    return SimpleNamespace(
        name=name,
        position=Pt(x, y),
        captured=SimpleNamespace(is_red=red),
        is_fleet=False,
        runway_is_operational=lambda: operational,
        ground_objects=[],
    )


def test_channel_names_pass_the_dtc_filter() -> None:
    assert sanitize_short_name("CVN-71") == "CVN71"
    assert sanitize_short_name("Overlord 1-1") == "OVERL"
    assert sanitize_short_name("Arco") == "ARCO"


def test_eta_is_seconds_since_zulu_midnight() -> None:
    """Cartridge times are Zulu, not the local mission clock: the ME's own DTC
    manager subtracts the terrain's SummerTimeDelta, and both jets read TOT/TOS
    against a Zulu system clock. Caucasus is UTC+4, so 07:19:13 local is
    03:19:13Z."""
    game = _game()
    assert (
        seconds_of_day(game, datetime(1988, 7, 15, 7, 19, 13))
        == 3 * 3600 + 19 * 60 + 13
    )
    assert seconds_of_day(game, None) == 0


def test_eta_keeps_climbing_across_zulu_midnight() -> None:
    """The base is the mission day's Zulu midnight, not the wall clock's, so a
    sortie that crosses 00:00Z still hands the jet increasing times."""
    game = _game()
    game.conditions.start_time = datetime(1988, 7, 15, 22, 0)  # 18:00Z
    before = seconds_of_day(game, datetime(1988, 7, 15, 23, 30))  # 19:30Z
    after = seconds_of_day(game, datetime(1988, 7, 16, 5, 30))  # 01:30Z next day
    assert before == 19 * 3600 + 30 * 60
    assert after == 25 * 3600 + 30 * 60
    assert after > before


def test_threat_sites_list_every_red_sam() -> None:
    game = _game(controlpoints=[_sam_cp()])
    sites = known_enemy_threat_sites(game)
    assert len(sites) == 1
    assert sites[0].label == "2"
    assert sites[0].range_m == 43000.0


def _hornet_fixture() -> tuple[Any, Any, Any]:
    takeoff = _waypoint(
        "TAKEOFF", FlightWaypointType.TAKEOFF, 0, 0, 0, datetime(1988, 7, 15, 7, 5)
    )
    target = _waypoint(
        "TARGET",
        FlightWaypointType.TARGET_POINT,
        60000,
        80000,
        7620,
        datetime(1988, 7, 15, 7, 30),
        targets=[object()],
    )
    landing = _waypoint(
        "LANDING",
        FlightWaypointType.LANDING_POINT,
        0,
        0,
        0,
        datetime(1988, 7, 15, 8, 10),
    )
    awacs_freq = _freq(251.0)
    carrier = SimpleNamespace(
        unit_name="CVN-71 Theodore Roosevelt",
        callsign="Mother",
        tacan=SimpleNamespace(number=71, band=SimpleNamespace(value="X")),
        icls_channel=11,
        link4_freq=_freq(336.4),
    )
    flight = _flight(
        waypoints=[takeoff, target, landing],
        arrival=SimpleNamespace(
            airfield_name="CVN-71 Theodore Roosevelt",
            atc=_freq(304.25),
            tacan=None,
            tacan_callsign=None,
            icls=None,
        ),
    )
    mission_data = _mission_data(
        [
            flight,
            _support_flight(
                FlightType.REFUELING, "Arco 1", Pt(10000, 10000), Pt(30000, 10000)
            ),
            _support_flight(
                FlightType.BARCAP, "Colt 1", Pt(-20000, 5000), Pt(-20000, 25000)
            ),
        ],
        carriers=[carrier],
    )
    mission_data.awacs = [
        SimpleNamespace(callsign="Overlord 1-1", freq=awacs_freq, group_name="ovl")
    ]
    game = _game(controlpoints=[_sam_cp()])
    return flight, mission_data, game


def test_hornet_cartridge_shape() -> None:
    flight, mission_data, game = _hornet_fixture()
    cartridge = build_hornet_cartridge(flight, mission_data, game, "Test FA-18C")

    payload = json.loads(cartridge.to_json())
    assert set(payload) == {"data", "name", "type"}
    assert payload["type"] == "FA-18C_hornet"
    data = payload["data"]
    assert data["terrain"] == "Caucasus"

    # Waypoints: numbered to MATCH THE KNEEBOARD -- its row 0 (takeoff) is not
    # emitted, so STPT n is kneeboard waypoint n.
    nav_pts = data["WYPT"]["NAV_PTS"]
    assert [w["wypt_num"] for w in nav_pts] == [1, 2]
    assert [w["text_note"] for w in nav_pts] == ["TARGET", "LANDING"]
    assert all(w["R1"] for w in nav_pts)
    assert [w["R1_order"] for w in nav_pts] == [1, 2]

    # Route sequence: ETA absolute seconds, target flagged, routes 2/3 empty.
    route = data["WYPT"]["NAV_ROUTE"]
    assert route[1] == [] and route[2] == []
    assert route[0]["STPT1"]["ETA"] == 3 * 3600 + 30 * 60  # 07:30 local, UTC+4
    assert route[0]["STPT1"]["TGT"] is True
    assert route[0]["STPT2"]["TGT"] is False

    # NAV settings: the boat card pre-tuned.
    nav_settings = data["WYPT"]["NAV_SETTINGS"]
    assert nav_settings["TACAN"] == {
        "Mode": 1,
        "Channel": 71,
        "ChannelMode": 1,
        "OnOff": True,
    }
    assert nav_settings["ICLS"] == {"Channel": 11, "OnOff": True}
    assert nav_settings["ACLS"] == {"Frequency": 336.4, "OnOff": True}
    assert nav_settings["Home_Waypoint"] == {"FPAS_HOME_WP": 2}

    # No COMM section: the presets reach the jet through the miz.
    assert "COMM" not in data

    # SA: the tanker racetrack, the SAM ring, styles visible. The COLT CAP
    # station is another flight's and stays off the page; this strike plan
    # has no hold point, so there is no own-orbit entry either.
    caps = data["SA"]["CAP_PTS"]
    assert [c["note"] for c in caps] == ["ARCO"]
    assert caps[0]["id"] == "CAP_PTS_1"
    assert caps[0]["course"] == pytest.approx(0.0)  # along +x = north
    assert caps[0]["length"] == pytest.approx(20000.0)
    mez = data["SA"]["MEZ_THRTS"]
    assert len(mez) == 1
    assert mez[0]["threat_type"] == "Custom"
    assert mez[0]["text"] == "2"
    assert mez[0]["threat_ring_radius"] == pytest.approx(23.2)
    assert data["SA"]["Default_FLOT_Line"] == 1


def test_hornet_designates_the_bullseye_as_the_aa_waypoint() -> None:
    """The A/A waypoint has to BE a waypoint in the database (EA guide p158),
    and the jet's stock slot 59 is past anything our routes emit."""
    flight, mission_data, game = _hornet_fixture()
    flight.waypoints = list(flight.waypoints) + [
        _waypoint("BULLSEYE", FlightWaypointType.BULLSEYE, 5000, 5000, 0, None)
    ]
    data = json.loads(
        build_hornet_cartridge(flight, mission_data, game, "H").to_json()
    )["data"]
    nav_pts = data["WYPT"]["NAV_PTS"]
    assert nav_pts[-1]["text_note"] == "BULLSEYE"
    bulls = nav_pts[-1]["wypt_num"]
    assert data["WYPT"]["NAV_SETTINGS"]["AA_Waypoint"] == {
        "AA_WP_Number": bulls,
        "AA_WP_Enabled": True,
    }
    # A reference point, never a flown leg.
    assert nav_pts[-1]["R1"] is False
    assert f"STPT{bulls}" not in data["WYPT"]["NAV_ROUTE"][0]


def test_hornet_land_start_tunes_the_departure_fields_tacan() -> None:
    """A Hornet leaving an airbase gets that field's TACAN; the arrival's only
    when the departure has none. A boat recovery keeps the boat's card."""
    flight, mission_data, game = _hornet_fixture()
    mission_data.carriers = []
    flight.departure = _runway("Kutaisi", 259.0)
    flight.departure.tacan = SimpleNamespace(number=44, band=SimpleNamespace(value="X"))
    flight.arrival = _runway("Senaki", 259.0)
    flight.arrival.tacan = SimpleNamespace(number=31, band=SimpleNamespace(value="X"))
    data = json.loads(
        build_hornet_cartridge(flight, mission_data, game, "Land").to_json()
    )["data"]
    assert data["WYPT"]["NAV_SETTINGS"]["TACAN"]["Channel"] == 44
    assert data["WYPT"]["NAV_SETTINGS"]["TACAN"]["OnOff"] is True

    flight.departure.tacan = None
    data = json.loads(
        build_hornet_cartridge(flight, mission_data, game, "Land").to_json()
    )["data"]
    assert data["WYPT"]["NAV_SETTINGS"]["TACAN"]["Channel"] == 31


def test_hornet_aa_waypoint_stays_off_without_a_bullseye() -> None:
    """No bullseye in the plan means nothing to designate; leave the jet's own
    slot 59 selected and switched off rather than pointing at empty space."""
    flight, mission_data, game = _hornet_fixture()
    data = json.loads(
        build_hornet_cartridge(flight, mission_data, game, "H").to_json()
    )["data"]
    assert data["WYPT"]["NAV_SETTINGS"]["AA_Waypoint"] == {
        "AA_WP_Number": 59,
        "AA_WP_Enabled": False,
    }


def test_viper_cartridge_shape() -> None:
    flight, mission_data, game = _hornet_fixture()
    flight.aircraft_type = SimpleNamespace(dcs_unit_type=SimpleNamespace(id="F-16C_50"))
    cartridge = build_viper_cartridge(flight, mission_data, game, "Test F-16C")
    data = json.loads(cartridge.to_json())["data"]

    nav_pts = data["MPD"]["NAV_PTS"]
    # Route first (kneeboard row 0 / takeoff not emitted, so STPT n matches
    # the kneeboard), then the tanker + CAP anchors as extra steerpoints.
    assert [p["note"] for p in nav_pts] == [
        "TARGET",
        "LANDING",
        "TKR ARCO",
    ]
    assert nav_pts[0]["TOS"] == 3 * 3600 + 30 * 60  # 07:30 local, UTC+4
    assert nav_pts[0]["isTOSEnabled"] is True
    assert nav_pts[2]["R1"] is False
    assert [p["type"] for p in nav_pts] == ["TGT", "STPT", "STPT"]

    threat = data["MPD"]["THREAT_PTS"]
    assert len(threat) == 1
    assert threat[0]["threatName"] == "Custom"
    assert threat[0]["radius"] == pytest.approx(43000.0)
    assert threat[0]["id"] == "THREAT_PTS56"

    # No COMM section: the Viper's schema has no channel names, so it could
    # only mirror the Radio table the miz already carries.
    assert "COMM" not in data


def test_viper_marks_the_target_and_the_run_in() -> None:
    """The HSD draws STPT as a circle, IP as a square and TGT as a triangle
    (EA guide p202), so the ingress and the target read at a glance."""
    flight, mission_data, game = _hornet_fixture()
    flight.aircraft_type = SimpleNamespace(dcs_unit_type=SimpleNamespace(id="F-16C_50"))
    flight.waypoints = [
        _waypoint("TAKEOFF", FlightWaypointType.TAKEOFF, 0, 0, 0, None),
        _waypoint("IP", FlightWaypointType.INGRESS_STRIKE, 100, 100, 3000, None),
        _waypoint(
            "TARGET",
            FlightWaypointType.TARGET_POINT,
            200,
            200,
            0,
            None,
            targets=[object()],
        ),
        _waypoint("EGRESS", FlightWaypointType.NAV, 300, 300, 3000, None),
        _waypoint("LANDING", FlightWaypointType.LANDING_POINT, 0, 0, 0, None),
    ]
    data = json.loads(build_viper_cartridge(flight, mission_data, game, "V").to_json())[
        "data"
    ]
    route = data["MPD"]["NAV_PTS"][:4]
    assert [p["type"] for p in route] == ["IP", "TGT", "STPT", "STPT"]
    # The id prefix stays STPT whatever the sub-type is (the editor's own rule).
    assert [p["id"] for p in route] == ["STPT1", "STPT2", "STPT3", "STPT4"]


def test_viper_route_stops_at_the_auto_sequencing_limit() -> None:
    """The jet auto-sequences only from STPT 1-20 (EA guide p223); a longer
    route would silently stop advancing itself past 20, and the support anchors
    must still land in the 21-25 tail rather than being dropped."""
    flight, mission_data, game = _hornet_fixture()
    flight.aircraft_type = SimpleNamespace(dcs_unit_type=SimpleNamespace(id="F-16C_50"))
    flight.waypoints = [
        _waypoint("TAKEOFF", FlightWaypointType.TAKEOFF, 0, 0, 0, None)
    ] + [
        _waypoint(f"NAV{i}", FlightWaypointType.NAV, i * 100, i * 100, 3000, None)
        for i in range(1, 25)
    ]
    data = json.loads(build_viper_cartridge(flight, mission_data, game, "V").to_json())[
        "data"
    ]
    nav_pts = data["MPD"]["NAV_PTS"]
    assert [p["note"] for p in nav_pts[:20]] == [f"NAV{i}" for i in range(1, 21)]
    assert [p["note"] for p in nav_pts[20:]] == ["TKR ARCO"]
    assert nav_pts[-1]["number"] == 21


def test_viper_geo_lines_stay_inside_their_partition(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """GEO_LINES owns steerpoints 31-55 and the editor refuses a 26th point; a
    fuller line source than today's 2-point fronts would otherwise run ids into
    the pre-planned-threat partition at 56."""
    flight, mission_data, game = _hornet_fixture()
    flight.aircraft_type = SimpleNamespace(dcs_unit_type=SimpleNamespace(id="F-16C_50"))
    segments = [
        (f"Front {n}", [(float(n * 1000 + i), float(i)) for i in range(8)])
        for n in range(4)
    ]
    monkeypatch.setattr(
        "game.missiongenerator.dtc.viper.flot_segments", lambda g: segments
    )
    data = json.loads(build_viper_cartridge(flight, mission_data, game, "V").to_json())[
        "data"
    ]
    geo = data["MPD"]["GEO_LINES"]
    assert len(geo) == 25
    assert geo[-1]["id"] == "GEO_LINES55"


def _viper_with_fields(fields: list[Any], divert: Optional[str] = None) -> Any:
    flight, mission_data, game = _hornet_fixture()
    flight.aircraft_type = SimpleNamespace(dcs_unit_type=SimpleNamespace(id="F-16C_50"))
    game.theater.controlpoints = fields
    if divert is not None:
        flight.divert = _runway(divert)
    return flight, mission_data, game


def test_viper_destinations_lead_with_the_divert() -> None:
    """DEST owns steerpoints 81-99 (EA guide p203). The briefed divert leads;
    the rest sort by distance from the target so the nearest alternates are the
    ones that fit."""
    flight, mission_data, game = _viper_with_fields(
        [
            _airbase_cp("Vaziani", 200000, 200000),
            _airbase_cp("Kobuleti", 61000, 81000),
            _airbase_cp("Krasnodar", 400000, 400000, red=True),
            _airbase_cp("Senaki", 65000, 85000, operational=False),
            _airbase_cp("Batumi", 70000, 90000),
        ],
        divert="Vaziani",
    )
    data = json.loads(build_viper_cartridge(flight, mission_data, game, "V").to_json())[
        "data"
    ]
    dest = data["MPD"]["DEST"]
    # Red-held and unusable fields drop out; the divert leads, then by range
    # from the target at (60000, 80000).
    assert [d["note"] for d in dest] == ["Vaziani", "Kobuleti", "Batumi"]
    assert [d["id"] for d in dest] == ["DEST81", "DEST82", "DEST83"]
    assert [d["text"] for d in dest] == ["VAZ", "KOB", "BAT"]
    # The generator has no terrain height source; destinations read 0.
    assert dest[1]["alt"] == 0
    assert dest[0]["number"] == 1


def test_viper_destination_labels_stay_three_characters() -> None:
    """The HSD shows three alphanumerics, so a collision has to fit in three."""
    flight, mission_data, game = _viper_with_fields(
        [
            _airbase_cp("Kutaisi", 61000, 81000),
            _airbase_cp("Kut-Al Field", 62000, 82000),
            _airbase_cp("CVN-71 Theodore Roosevelt", 63000, 83000),
        ]
    )
    data = json.loads(build_viper_cartridge(flight, mission_data, game, "V").to_json())[
        "data"
    ]
    labels = [d["text"] for d in data["MPD"]["DEST"]]
    assert labels == ["KUT", "KU2", "CVN"]
    assert all(len(label) <= 3 for label in labels)


def test_viper_destinations_stop_at_the_partition_end() -> None:
    """Steerpoints 81-99 is 19 slots, and the editor refuses a 20th."""
    flight, mission_data, game = _viper_with_fields(
        [_airbase_cp(f"Field{n:02d}", 60000 + n * 1000, 80000) for n in range(25)]
    )
    data = json.loads(build_viper_cartridge(flight, mission_data, game, "V").to_json())[
        "data"
    ]
    dest = data["MPD"]["DEST"]
    assert len(dest) == 19
    assert dest[-1]["id"] == "DEST99"


def test_a_steerpoints_alt_is_its_ground_not_its_leg_altitude() -> None:
    """``alt`` on a point is the ground under it; the leg altitude is a separate
    field. ED's own editors fill the first from terrain -- ``alt = getAltitude(x, y)``
    in the Viper's ``NAV_PTS.lua`` and the Hornet's ``WYPT_NAV.lua`` -- and resolve
    the second against terrain when it is AGL (``tmpAlt + getAltitude(x, y)``,
    Hornet ``ROUTE_SEQ.lua``). Writing one number into both told the jet the
    ground under an 18,000 ft nav point was at 18,000 ft, and that a target sat
    at sea level.
    """
    takeoff = _waypoint("TAKEOFF", FlightWaypointType.TAKEOFF, 0, 0, 0, None)
    nav = _waypoint("NAV", FlightWaypointType.NAV, 10000, 0, 6705, None)
    target = _waypoint(
        "TARGET", FlightWaypointType.TARGET_GROUP_LOC, 60000, 80000, 6705, None
    )
    land = _waypoint("LANDING", FlightWaypointType.LANDING_POINT, 0, 0, 58, None)
    # Kneeboard row 0 (takeoff) is not emitted; the rest land on STPT 1/2/3.
    flight = _flight(waypoints=[takeoff, nav, target, land])
    mission_data = _mission_data([flight])
    game = _game()

    hornet = json.loads(
        build_hornet_cartridge(flight, mission_data, game, "Test FA-18C").to_json()
    )["data"]
    nav_pts = hornet["WYPT"]["NAV_PTS"]
    route = hornet["WYPT"]["NAV_ROUTE"][0]
    # Nav point: ground unknown, so 0 -- never the 6705 m it is flown at.
    assert nav_pts[0]["alt"] == 0
    assert route["STPT1"]["alt"] == 6705 and route["STPT1"]["altitudeType"] == 1
    # Target: still 0, and the leg is the .miz's 0 AGL.
    assert nav_pts[1]["alt"] == 0
    assert route["STPT2"]["alt"] == 0 and route["STPT2"]["altitudeType"] == 2
    # Landing: the one point whose planned altitude IS its ground.
    assert nav_pts[2]["alt"] == 58

    flight.aircraft_type = SimpleNamespace(dcs_unit_type=SimpleNamespace(id="F-16C_50"))
    viper = json.loads(
        build_viper_cartridge(flight, mission_data, game, "Test F-16C").to_json()
    )["data"]
    steerpoints = viper["MPD"]["NAV_PTS"]
    assert steerpoints[0]["alt"] == 0 and steerpoints[0]["routeAltitude"] == 6705
    assert steerpoints[1]["alt"] == 0 and steerpoints[1]["routeAltitude"] == 0
    assert steerpoints[1]["altitudeType"] == 2
    assert steerpoints[2]["alt"] == 58


def test_unit_dict_and_miz_round_trip(tmp_path: Path) -> None:
    mission = Mission(Caucasus())
    usa = mission.country("USA")
    group = mission.flight_group_inflight(
        usa,
        "DTC Test",
        FA_18C_hornet,
        mission.terrain.airports["Kutaisi"].position,
        altitude=6000,
        group_size=2,
    )
    cartridge = DtcCartridge(
        name="Test FA-18C",
        unit_type="FA-18C_hornet",
        terrain="Caucasus",
        data={"COMM": {}, "type": "FA-18C_hornet"},
    )
    mission.add_dtc_cartridge(cartridge.name, cartridge.to_json())
    group.units[0].add_dtc_cartridge(cartridge.name)

    lead = group.units[0].dict()
    wing = group.units[1].dict()
    assert lead["DTC"] == {
        "Cartridges": {1: {"default": True, "name": "Test FA-18C"}},
        "AutoLoad": True,
    }
    assert "DTC" not in wing

    miz = tmp_path / "dtc_test.miz"
    mission.save(str(miz))
    with zipfile.ZipFile(miz) as zf:
        payload = json.loads(zf.read("DTC/Test FA-18C.dtc"))
        assert payload["name"] == "Test FA-18C"
        mission_lua = zf.read("mission").decode("utf-8")
        assert '"AutoLoad"' in mission_lua
        assert "Test FA-18C" in mission_lua

    # The binding and the file both survive a load.
    reloaded = Mission(Caucasus())
    reloaded.load_file(str(miz))
    assert "Test FA-18C" in reloaded.dtc_cartridges
    unit = reloaded.country("USA").plane_group[0].units[0]
    assert unit.dtc_cartridges == [{"name": "Test FA-18C", "default": True}]
    assert unit.dtc_autoload


def _generator(game: Any, flights: list[Any]) -> DtcGenerator:
    return DtcGenerator(
        _FakeMission(),  # type: ignore[arg-type]
        game,
        _mission_data(flights),
    )


def test_generator_builds_only_blue_client_supported_flights(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    built = []

    def fake_builder(flight: Any, md: Any, game: Any, name: str) -> DtcCartridge:
        built.append(name)
        return DtcCartridge(name, "FA-18C_hornet", "Caucasus", {})

    monkeypatch.setitem(CARTRIDGE_BUILDERS, "FA-18C_hornet", fake_builder)

    flights = [
        _flight(callsign="Wizard 1"),
        _flight(callsign="Wizard 1"),  # same callsign: name must dedupe
        _flight(callsign="Dodge 1", blue=False),
        _flight(callsign="Uzi 1", clients=0),
        _flight(callsign="Chevy 1", dcs_id="F-14B"),
    ]
    generator = _generator(_game(), flights)
    generator.generate()
    assert built == [
        "Retribution Wizard 1 FA-18C_hornet",
        "Retribution Wizard 1 FA-18C_hornet 2",
    ]
    assert len(generator.cartridges) == 2
    # Bound to the clients and written into the mission under the same name.
    assert flights[0].client_units[0].dtc_autoload is True
    assert flights[0].client_units[0].dtc_cartridges[0]["name"] == built[0]
    assert set(generator.mission.dtc_cartridges) == set(built)


def test_generator_respects_the_setting(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setitem(
        CARTRIDGE_BUILDERS,
        "FA-18C_hornet",
        lambda *args: pytest.fail("builder must not run when the setting is off"),
    )
    generator = _generator(_game(dtc_on=False), [_flight()])
    generator.generate()
    assert generator.cartridges == []


def test_generator_survives_a_builder_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def broken(*args: Any) -> DtcCartridge:
        raise RuntimeError("boom")

    monkeypatch.setitem(CARTRIDGE_BUILDERS, "FA-18C_hornet", broken)
    generator = _generator(_game(), [_flight()])
    generator.generate()
    assert generator.cartridges == []


def test_per_flight_override_beats_the_campaign_setting(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_builder(f: Any, md: Any, g: Any, name: str) -> DtcCartridge:
        return DtcCartridge(name, "FA-18C_hornet", "Caucasus", {})

    monkeypatch.setitem(CARTRIDGE_BUILDERS, "FA-18C_hornet", fake_builder)
    # Campaign OFF, flight forced ON -> builds.
    generator = _generator(
        _game(dtc_on=False),
        [_flight(callsign="Force On", dtc_options=DtcOptions(enabled=True))],
    )
    generator.generate()
    assert len(generator.cartridges) == 1
    # Campaign ON, flight forced OFF -> skipped.
    generator = _generator(
        _game(),
        [_flight(callsign="Force Off", dtc_options=DtcOptions(enabled=False))],
    )
    generator.generate()
    assert generator.cartridges == []


def test_all_sections_off_builds_no_cartridge(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setitem(
        CARTRIDGE_BUILDERS,
        "FA-18C_hornet",
        lambda *args: pytest.fail("an empty cartridge must not be built"),
    )
    # Every section flag off, whatever flags exist: a section added later must
    # not quietly revive this cartridge.
    bare = DtcOptions(
        **{f.name: False for f in dataclasses.fields(DtcOptions) if f.type == "bool"}
    )
    generator = _generator(_game(), [_flight(dtc_options=bare)])
    generator.generate()
    assert generator.cartridges == []


def test_hornet_sections_are_omitted_when_off() -> None:
    flight, mission_data, game = _hornet_fixture()
    flight.dtc_options = DtcOptions(
        route=False, friendly_orbits=False, threat_rings=False
    )
    cartridge = build_hornet_cartridge(flight, mission_data, game, "Trimmed")
    data = json.loads(cartridge.to_json())["data"]
    assert "COMM" not in data
    # nav_aids stays on: WYPT present with the boat tuned but no steerpoints.
    assert data["WYPT"]["NAV_PTS"] == []
    assert data["WYPT"]["NAV_SETTINGS"]["TACAN"]["OnOff"] is True
    # flot_and_zones stays on: SA present, but no CAP orbits and no MEZ rings.
    assert data["SA"]["CAP_PTS"] == []
    assert data["SA"]["MEZ_THRTS"] == []
    assert len(data["SA"]["FAOR_FLOT"]["FLOT"]) == 0  # fake game has no fronts

    flight.dtc_options = DtcOptions(
        nav_aids=False, flot_and_zones=False, friendly_orbits=False, threat_rings=False
    )
    cartridge = build_hornet_cartridge(flight, mission_data, game, "Route Only")
    data = json.loads(cartridge.to_json())["data"]
    assert "SA" not in data
    assert len(data["WYPT"]["NAV_PTS"]) == 2  # kneeboard rows 1..N
    assert data["WYPT"]["NAV_SETTINGS"]["TACAN"]["OnOff"] is False


def test_viper_sections_are_omitted_when_off() -> None:
    flight, mission_data, game = _hornet_fixture()
    flight.aircraft_type = SimpleNamespace(dcs_unit_type=SimpleNamespace(id="F-16C_50"))
    flight.dtc_options = DtcOptions(route=False, destinations=False)
    cartridge = build_viper_cartridge(flight, mission_data, game, "Anchors Only")
    data = json.loads(cartridge.to_json())["data"]
    assert "COMM" not in data
    # Route off, friendly orbits on: only the support anchors load.
    assert [p["note"] for p in data["MPD"]["NAV_PTS"]] == ["TKR ARCO"]

    flight.dtc_options = DtcOptions(
        route=False,
        nav_aids=False,
        flot_and_zones=False,
        friendly_orbits=False,
        threat_rings=True,
        destinations=False,
    )
    cartridge = build_viper_cartridge(flight, mission_data, game, "Threats Only")
    data = json.loads(cartridge.to_json())["data"]
    assert data["MPD"]["NAV_PTS"] == []
    assert data["MPD"]["GEO_LINES"] == []
    assert len(data["MPD"]["THREAT_PTS"]) == 1


def test_flot_populates_when_a_front_exists(monkeypatch: pytest.MonkeyPatch) -> None:
    """The FLOT half of option 4 -- every other test runs a game with no fronts
    (conflicts() == []), so the front-line geometry reaching FAOR_FLOT (Hornet)
    and GEO_LINES (Viper) was never exercised. flot_segments itself mirrors the
    trusted F10 frontline drawing; this locks the builders consuming it."""
    flight, mission_data, game = _hornet_fixture()
    segments = [
        ("Front A", [(1000.0, 2000.0), (3000.0, 4000.0)]),
        ("Front B", [(5000.0, 6000.0), (7000.0, 8000.0)]),
    ]
    monkeypatch.setattr(
        "game.missiongenerator.dtc.hornet.flot_segments", lambda g: segments
    )
    monkeypatch.setattr(
        "game.missiongenerator.dtc.viper.flot_segments", lambda g: segments
    )

    hornet = json.loads(
        build_hornet_cartridge(flight, mission_data, game, "H").to_json()
    )["data"]
    flot = hornet["SA"]["FAOR_FLOT"]["FLOT"]
    assert [line["note"] for line in flot] == ["Front A", "Front B"]
    assert flot[0]["id"] == "FLOT_1"
    assert flot[0]["num"] == 1
    assert [(p["x"], p["y"]) for p in flot[0]["points"]] == [
        (1000.0, 2000.0),
        (3000.0, 4000.0),
    ]

    flight.aircraft_type = SimpleNamespace(dcs_unit_type=SimpleNamespace(id="F-16C_50"))
    viper = json.loads(
        build_viper_cartridge(flight, mission_data, game, "V").to_json()
    )["data"]
    geo = viper["MPD"]["GEO_LINES"]
    # Two 2-point fronts = 4 points, tagged to consecutive HSD line sets.
    assert len(geo) == 4
    assert geo[0]["note"] == "Front A"
    assert geo[0]["L1"] is True and geo[0]["L2"] is False
    assert geo[2]["note"] == "Front B"
    assert geo[2]["L2"] is True and geo[2]["L1"] is False


def test_other_flights_cap_stations_never_appear() -> None:
    """However many CAP stations the ATO flies, none of them is this jet's
    business: the page carries its own orbit and the support orbits only."""
    flight, mission_data, game = _hornet_fixture()
    for callsign, x in (("Colt 2", -17000), ("Ford 1", 30000), ("Uzi 1", 50000)):
        mission_data.flights.append(
            _support_flight(FlightType.BARCAP, callsign, Pt(x, 6500), Pt(x, 26500))
        )
    cartridge = build_hornet_cartridge(flight, mission_data, game, "Crowded")
    caps = json.loads(cartridge.to_json())["data"]["SA"]["CAP_PTS"]
    assert [c["note"] for c in caps] == ["ARCO"]


def test_own_racetrack_leads_and_is_preselected() -> None:
    """A flight that flies a racetrack gets it as CAP point 1, selected at
    spawn; the tanker follows; the other flight's COLT station never appears."""
    flight, mission_data, game = _hornet_fixture()
    flight.flight_type = FlightType.BARCAP
    flight.waypoints = list(flight.waypoints) + [
        _waypoint(
            "RACETRACK START", FlightWaypointType.PATROL_TRACK, -40000, 5000, 6000, None
        ),
        _waypoint(
            "RACETRACK END", FlightWaypointType.PATROL, -40000, 25000, 6000, None
        ),
    ]
    cartridge = build_hornet_cartridge(flight, mission_data, game, "Own CAP")
    data = json.loads(cartridge.to_json())["data"]["SA"]
    assert [c["note"] for c in data["CAP_PTS"]] == ["WIZAR", "ARCO"]
    assert data["CAP_PTS"][0]["course"] == pytest.approx(90.0)
    assert data["Default_CAP_Point"] == 1


def _with_hold(flight: Any) -> None:
    flight.waypoints = (
        [flight.waypoints[0]]
        + [_waypoint("HOLD", FlightWaypointType.LOITER, 15000, 15000, 6000, None)]
        + list(flight.waypoints[1:])
    )


def test_a_flight_without_an_orbit_gets_a_track_at_its_hold() -> None:
    """Not a true orbiting plan, so instead of no track at all the page gets
    one at the hold point -- the minimum-length racetrack, selected at spawn."""
    flight, mission_data, game = _hornet_fixture()
    _with_hold(flight)
    cartridge = build_hornet_cartridge(flight, mission_data, game, "Hold")
    data = json.loads(cartridge.to_json())["data"]["SA"]
    caps = data["CAP_PTS"]
    assert [c["note"] for c in caps] == ["WIZAR", "ARCO"]
    assert (caps[0]["x"], caps[0]["y"]) == (15000, 15000)
    assert caps[0]["length"] == pytest.approx(3704.0)
    assert data["Default_CAP_Point"] == 1


def test_the_hold_stand_in_reaches_the_viper_too() -> None:
    flight, mission_data, game = _hornet_fixture()
    _with_hold(flight)
    flight.aircraft_type = SimpleNamespace(dcs_unit_type=SimpleNamespace(id="F-16C_50"))
    nav_pts = json.loads(
        build_viper_cartridge(flight, mission_data, game, "Hold").to_json()
    )["data"]["MPD"]["NAV_PTS"]
    # The route takes 1-3 (hold, target, landing); the anchors follow.
    assert [p["note"] for p in nav_pts[3:]] == ["HOLD WIZAR", "TKR ARCO"]


def test_viper_dest_paints_the_enemy_field_being_worked_over() -> None:
    """An OCA Viper wants the target field on the HSD, and only the DEST
    partition draws an airfield: it lands right after the briefed divert."""
    flight, mission_data, game = _hornet_fixture()
    flight.aircraft_type = SimpleNamespace(dcs_unit_type=SimpleNamespace(id="F-16C_50"))
    flight.divert = _runway("Batumi")
    # The target is at (60000, 80000); the red field sits 5 km from it.
    game.theater.controlpoints = [
        _airbase_cp("Batumi", -9000, 3000),
        _airbase_cp("Kutaisi", 0, 0),
        _airbase_cp("Senaki", 62000, 84000, red=True),
        _airbase_cp("Sukhumi", 200000, 200000, red=True),
    ]
    dest = json.loads(
        build_viper_cartridge(flight, mission_data, game, "OCA").to_json()
    )["data"]["MPD"]["DEST"]
    assert [d["note"] for d in dest] == ["Batumi", "Senaki", "Kutaisi"]
    assert dest[1]["id"] == "DEST82"


def test_generator_skips_a_builder_that_returns_none(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setitem(CARTRIDGE_BUILDERS, "FAKE-JET", lambda *args: None)
    flight = _flight(dcs_id="FAKE-JET", callsign="Rhino 1")
    generator = _generator(_game(), [flight])
    generator.generate()
    assert generator.cartridges == []
    assert flight.client_units[0].dtc_cartridges == []


def test_only_the_stock_hornet_and_viper_take_a_cartridge() -> None:
    """The F-14B(U) sets the DTC flag too but its descriptor is a different
    schema; the plain F-14B and the CJS Super Hornets take none."""
    assert set(CARTRIDGE_BUILDERS) == {"FA-18C_hornet", "F-16C_50"}


def test_an_ingress_carrying_the_target_list_is_still_an_ip() -> None:
    """Retribution attaches the target list to the ingress point so the task
    can be built. That must not make it the target on the HSD or the route."""
    flight, mission_data, game = _hornet_fixture()
    flight.waypoints = [
        _waypoint("TAKEOFF", FlightWaypointType.TAKEOFF, 0, 0, 0, None),
        _waypoint(
            "IP", FlightWaypointType.INGRESS_STRIKE, 100, 100, 3000, None, targets=[1]
        ),
        _waypoint(
            "TARGET", FlightWaypointType.TARGET_POINT, 200, 200, 0, None, targets=[1]
        ),
        _waypoint("LANDING", FlightWaypointType.LANDING_POINT, 0, 0, 0, None),
    ]
    route = json.loads(
        build_hornet_cartridge(flight, mission_data, game, "IP").to_json()
    )["data"]["WYPT"]["NAV_ROUTE"][0]
    assert route["STPT1"]["TGT"] is False
    assert route["STPT2"]["TGT"] is True

    flight.aircraft_type = SimpleNamespace(dcs_unit_type=SimpleNamespace(id="F-16C_50"))
    nav_pts = json.loads(
        build_viper_cartridge(flight, mission_data, game, "IP").to_json()
    )["data"]["MPD"]["NAV_PTS"]
    assert [p["type"] for p in nav_pts[:3]] == ["IP", "TGT", "STPT"]
