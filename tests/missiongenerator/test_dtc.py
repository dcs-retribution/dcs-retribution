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
    SUPPORT_BOX_POINTS,
    SUPPORT_ORBIT_DIAMETER_M,
    SupportTrack,
    known_enemy_threat_sites,
    red_land_boundary,
    sanitize_short_name,
    seconds_of_day,
    support_boxes,
    support_half_width,
    support_tracks,
)
from game.missiongenerator.dtc.generator import CARTRIDGE_BUILDERS
from game.missiongenerator.dtc.options import DtcOptions
from game.missiongenerator.dtc.hornet import build_hornet_cartridge
from game.missiongenerator.dtc.viper import build_viper_cartridge
from game.settings.settings import DtcCartridgeLoading
from game.utils import Speed, knots


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
        self.radio: Optional[dict[int, dict[str, dict[int, float]]]] = None

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
    patrol_speed: Optional[Speed] = None,
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
        patrol_speed=patrol_speed,
        work_zone=None,
    )


def _support_flight(
    flight_type: FlightType,
    callsign: str,
    start: Pt,
    end: Pt,
    patrol_speed: Optional[Speed] = None,
) -> Any:
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
        patrol_speed=patrol_speed,
    )


def _mission_data(flights: list[Any], carriers: Optional[list[Any]] = None) -> Any:
    return SimpleNamespace(
        flights=flights,
        awacs=[],
        tankers=[],
        jtacs=[],
        carriers=carriers or [],
    )


def _game(
    *,
    loading: DtcCartridgeLoading = DtcCartridgeLoading.PILOT,
    controlpoints: Optional[list[Any]] = None,
) -> Any:
    return SimpleNamespace(
        settings=SimpleNamespace(dtc_cartridge_loading=loading),
        conditions=SimpleNamespace(start_time=datetime(1988, 7, 15, 7, 0)),
        theater=SimpleNamespace(
            terrain=SimpleNamespace(name="Caucasus", airports={}),
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
        blue=SimpleNamespace(is_blue=True),
        ship_group=SimpleNamespace(
            units=[SimpleNamespace(name="CVN-71 Theodore Roosevelt", id=17)],
            points=[SimpleNamespace(position=Pt(-90000, 40000))],
        ),
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
    flight.client_units[0].radio = {
        1: {"channels": {1: 258.5, 2: 251.0, 3: 304.25}},
        2: {"channels": {}},
    }
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

    # COMM mirrors the unit's presets and names each channel after what it
    # tunes; a channel the allocator did not set keeps the stock default.
    comm1 = data["COMM"]["COMM1"]
    assert comm1["Channel_1"] == {"frequency": 258.5, "modulation": 0, "name": "WIZAR"}
    assert comm1["Channel_2"]["name"] == "OVERL"
    assert comm1["Channel_3"]["name"] == "ARR"
    assert comm1["Channel_4"] == {"frequency": 256.0, "modulation": 0, "name": "CH 4"}
    assert data["COMM"]["COMM2"]["Channel_1"]["frequency"] == 305.0
    assert data["COMM"]["mirror_COMM1"] is False

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
    """GEO_LINES owns steerpoints 31-55 and the editor refuses a 26th point, so
    more front than the partition holds is thinned rather than run on into the
    pre-planned-threat partition at 56."""
    flight, mission_data, game = _hornet_fixture()
    flight.aircraft_type = SimpleNamespace(dcs_unit_type=SimpleNamespace(id="F-16C_50"))
    segments = [
        (f"Front {n}", [(float(n * 1000 + i), float(i)) for i in range(8)])
        for n in range(4)
    ]
    monkeypatch.setattr(
        "game.missiongenerator.dtc.common.flot_segments", lambda g: segments
    )
    data = json.loads(build_viper_cartridge(flight, mission_data, game, "V").to_json())[
        "data"
    ]
    geo = data["MPD"]["GEO_LINES"]
    assert len(geo) == 25
    assert geo[-1]["id"] == "GEO_LINES55"
    # The boundary is L1 only; the fixture's tanker box takes L2.
    assert all(point["L1"] for point in geo if point["note"] == "FLOT")


def test_viper_never_writes_the_bullseye_steerpoint(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """STPT 25 is the jet's bullseye, configured from the miz on load (EA guide
    p325). A support anchor written there replaced it, so every bullseye
    readout pointed at the orbit; the anchors stop at 24."""
    from dcs.mapping import Point

    flight, mission_data, game = _hornet_fixture()
    flight.aircraft_type = SimpleNamespace(dcs_unit_type=SimpleNamespace(id="F-16C_50"))
    flight.waypoints = [
        _waypoint("TAKEOFF", FlightWaypointType.TAKEOFF, 0, 0, 0, None)
    ] + [
        _waypoint(f"NAV{i}", FlightWaypointType.NAV, i * 100, i * 100, 3000, None)
        for i in range(1, 25)
    ]
    terrain = game.theater.terrain
    monkeypatch.setattr(
        "game.missiongenerator.dtc.viper.support_tracks",
        lambda _md: [
            SupportTrack(
                callsign=f"TKR{n}",
                kind="TKR",
                start=Point(float(n * 1000), 0.0, terrain),
                end=Point(float(n * 1000), 5000.0, terrain),
                altitude_m=6000.0,
            )
            for n in range(10)
        ],
    )
    data = json.loads(build_viper_cartridge(flight, mission_data, game, "V").to_json())[
        "data"
    ]
    numbers = [p["number"] for p in data["MPD"]["NAV_PTS"]]
    assert numbers == list(range(1, 25))


def test_hornet_flags_one_target_per_sequence() -> None:
    """ROUTE_SEQ.lua refuses a second TGT in a sequence."""
    flight, mission_data, game = _hornet_fixture()
    second = _waypoint(
        "TARGET 2",
        FlightWaypointType.TARGET_POINT,
        61000,
        81000,
        7620,
        datetime(1988, 7, 15, 7, 31),
        targets=[object()],
    )
    flight.waypoints = flight.waypoints[:2] + [second] + flight.waypoints[2:]
    route = json.loads(
        build_hornet_cartridge(flight, mission_data, game, "H").to_json()
    )["data"]["WYPT"]["NAV_ROUTE"][0]
    assert "STPT2" in route  # the second target is on the sequence
    flagged = [name for name, leg in route.items() if leg["TGT"]]
    assert flagged == ["STPT1"]


def test_red_land_boundary_chains_the_fronts(monkeypatch: pytest.MonkeyPatch) -> None:
    """One continuous trace, ordered across the theater and oriented so each bar
    starts at the end nearest the last."""
    segments = [
        # Deliberately out of order, and the middle bar runs the wrong way.
        ("B", [(2000.0, 0.0), (3000.0, 0.0)]),
        ("C", [(4000.0, 0.0), (5000.0, 0.0)]),
        ("A", [(0.0, 0.0), (1000.0, 0.0)]),
    ]
    monkeypatch.setattr(
        "game.missiongenerator.dtc.common.flot_segments", lambda g: segments
    )
    runs = red_land_boundary(None, 1, 25)  # type: ignore[arg-type]
    assert len(runs) == 1
    name, points = runs[0]
    assert name == "FLOT"
    xs = [x for x, _ in points]
    assert sorted(xs) == [0.0, 1000.0, 2000.0, 3000.0, 4000.0, 5000.0]
    assert xs == sorted(xs) or xs == sorted(xs, reverse=True)


def test_red_land_boundary_splits_across_the_lines_sharing_a_vertex(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A display with several short lines draws one boundary only if consecutive
    lines meet on a shared vertex."""
    segments = [("F", [(float(i * 100), 0.0) for i in range(9)])]
    monkeypatch.setattr(
        "game.missiongenerator.dtc.common.flot_segments", lambda g: segments
    )
    runs = red_land_boundary(None, 3, 5)  # type: ignore[arg-type]
    assert [name for name, _ in runs] == ["FLOT 1", "FLOT 2"]
    assert runs[0][1][-1] == runs[1][1][0]


def test_red_land_boundary_thins_to_the_budget(monkeypatch: pytest.MonkeyPatch) -> None:
    segments = [("F", [(float(i), 0.0) for i in range(40)])]
    monkeypatch.setattr(
        "game.missiongenerator.dtc.common.flot_segments", lambda g: segments
    )
    _, points = red_land_boundary(None, 1, 25)[0]  # type: ignore[arg-type]
    assert len(points) == 25
    assert points[0] == (0.0, 0.0)
    assert points[-1] == (39.0, 0.0)


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


def test_a_steerpoints_alt_is_the_altitude_the_miz_gives_the_jet() -> None:
    """The point's ``alt`` is what the cockpit shows (a Viper flown with ``alt``
    131 ft / ``routeAltitude`` 22,000 ft read ELEV 131 on the DED), and without a
    cartridge the jet takes it from the mission-editor waypoint altitude. So an
    en-route point carries its planned altitude. A point the miz puts on the deck
    reads 0: the generator has no terrain height source. The route entry keeps
    the AGL encoding the DTC Manager resolves (``tmpAlt + getAltitude(x, y)``,
    Hornet ``ROUTE_SEQ.lua``).
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
    # Nav point: the 6705 m it is flown at, in both fields.
    assert nav_pts[0]["alt"] == 6705
    assert route["STPT1"]["alt"] == 6705 and route["STPT1"]["altitudeType"] == 1
    # Target: on the deck in the miz (0 AGL), ground unknown here: 0.
    assert nav_pts[1]["alt"] == 0
    assert route["STPT2"]["alt"] == 0 and route["STPT2"]["altitudeType"] == 2
    # Landing: the field's own elevation.
    assert nav_pts[2]["alt"] == 58

    flight.aircraft_type = SimpleNamespace(dcs_unit_type=SimpleNamespace(id="F-16C_50"))
    viper = json.loads(
        build_viper_cartridge(flight, mission_data, game, "Test F-16C").to_json()
    )["data"]
    steerpoints = viper["MPD"]["NAV_PTS"]
    assert steerpoints[0]["alt"] == 6705 and steerpoints[0]["routeAltitude"] == 6705
    assert steerpoints[1]["alt"] == 0 and steerpoints[1]["routeAltitude"] == 0
    assert steerpoints[1]["altitudeType"] == 2
    assert steerpoints[2]["alt"] == 58


def test_the_hornets_waypoint_elevation_stays_inside_the_editors_range() -> None:
    """WYPT_NAV.lua clamps a waypoint elevation to -2000..25000 ft; the route
    entry (ROUTE_SEQ.lua) allows 80,000 ft, so a high leg keeps its number
    there."""
    takeoff = _waypoint("TAKEOFF", FlightWaypointType.TAKEOFF, 0, 0, 0, None)
    high = _waypoint("NAV", FlightWaypointType.NAV, 10000, 0, 9144, None)
    land = _waypoint("LANDING", FlightWaypointType.LANDING_POINT, 0, 0, 0, None)
    flight = _flight(waypoints=[takeoff, high, land])
    hornet = json.loads(
        build_hornet_cartridge(
            flight, _mission_data([flight]), _game(), "Cap"
        ).to_json()
    )["data"]["WYPT"]
    assert hornet["NAV_PTS"][0]["alt"] == pytest.approx(25000 * 0.3048)
    assert hornet["NAV_ROUTE"][0]["STPT1"]["alt"] == 9144


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
    # The pilot loads it by default.
    assert flights[0].client_units[0].dtc_autoload is False
    assert flights[0].client_units[0].dtc_cartridges[0]["name"] == built[0]
    assert set(generator.mission.dtc_cartridges) == set(built)


def test_generator_respects_the_setting(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setitem(
        CARTRIDGE_BUILDERS,
        "FA-18C_hornet",
        lambda *args: pytest.fail("builder must not run when the setting is off"),
    )
    generator = _generator(_game(loading=DtcCartridgeLoading.OFF), [_flight()])
    generator.generate()
    assert generator.cartridges == []


def test_generator_loads_at_spawn_when_set(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_builder(f: Any, md: Any, g: Any, name: str) -> DtcCartridge:
        return DtcCartridge(name, "FA-18C_hornet", "Caucasus", {})

    monkeypatch.setitem(CARTRIDGE_BUILDERS, "FA-18C_hornet", fake_builder)
    flights = [_flight(), _flight(dtc_options=DtcOptions(auto_load=False))]
    _generator(_game(loading=DtcCartridgeLoading.SPAWN), flights).generate()
    assert flights[0].client_units[0].dtc_autoload is True
    # A per-flight choice wins over the campaign setting.
    assert flights[1].client_units[0].dtc_autoload is False


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
        _game(loading=DtcCartridgeLoading.OFF),
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
        comms=False, route=False, friendly_orbits=False, threat_rings=False
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
    and GEO_LINES (Viper) was never exercised. flot_segments mirrors the F10
    frontline drawing; this locks the builders consuming its chained boundary."""
    flight, mission_data, game = _hornet_fixture()
    segments = [
        ("Front A", [(1000.0, 2000.0), (3000.0, 4000.0)]),
        ("Front B", [(5000.0, 6000.0), (7000.0, 8000.0)]),
    ]
    monkeypatch.setattr(
        "game.missiongenerator.dtc.common.flot_segments", lambda g: segments
    )

    hornet = json.loads(
        build_hornet_cartridge(flight, mission_data, game, "H").to_json()
    )["data"]
    flot = hornet["SA"]["FAOR_FLOT"]["FLOT"]
    # The two fronts chain into one boundary line.
    assert [line["note"] for line in flot] == ["FLOT"]
    assert flot[0]["id"] == "FLOT_1"
    assert flot[0]["num"] == 1
    assert [(p["x"], p["y"]) for p in flot[0]["points"]] == [
        (1000.0, 2000.0),
        (3000.0, 4000.0),
        (5000.0, 6000.0),
        (7000.0, 8000.0),
    ]

    flight.aircraft_type = SimpleNamespace(dcs_unit_type=SimpleNamespace(id="F-16C_50"))
    viper = json.loads(
        build_viper_cartridge(flight, mission_data, game, "V").to_json()
    )["data"]
    geo = viper["MPD"]["GEO_LINES"]
    # Two 2-point fronts = one 4-point boundary, all on line set L1.
    boundary = [point for point in geo if point["L1"]]
    assert len(boundary) == 4
    assert all(point["note"] == "FLOT" for point in boundary)


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


def _orbit_track(callsign: str, kind: str, length_m: float) -> Any:
    """A due-north racetrack of `length_m`, centred on the origin."""
    from dcs.mapping import Point

    terrain = Caucasus()
    return SupportTrack(
        callsign=callsign,
        kind=kind,
        start=Point(-length_m / 2, 0.0, terrain),
        end=Point(length_m / 2, 0.0, terrain),
    )


def test_support_box_is_the_racetrack_footprint(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The box encloses the straight legs AND the room the turns need, so a
    tanker at the edge of the drawn box is still inside its own orbit."""
    track = _orbit_track("ARCO", "TKR", 20000.0)
    monkeypatch.setattr(
        "game.missiongenerator.dtc.common.support_tracks", lambda data: [track]
    )
    ((callsign, points),) = support_boxes(None, 3)  # type: ignore[arg-type]
    assert callsign == "ARCO"
    assert len(points) == SUPPORT_BOX_POINTS
    # Closed: nothing auto-closes a line set, so the first corner repeats.
    assert points[0] == points[-1]
    half_width = SUPPORT_ORBIT_DIAMETER_M / 2
    xs = sorted({round(x, 3) for x, _ in points})
    ys = sorted({round(y, 3) for _, y in points})
    assert xs == [-(10000.0 + half_width), 10000.0 + half_width]
    assert ys == [-half_width, half_width]


def test_support_box_follows_the_orbit_course(monkeypatch: pytest.MonkeyPatch) -> None:
    """An east-west orbit boxes east-west; the box is not axis-aligned by
    accident."""
    from dcs.mapping import Point

    terrain = Caucasus()
    track = SupportTrack(
        callsign="MAGIC",
        kind="AWACS",
        start=Point(0.0, -10000.0, terrain),
        end=Point(0.0, 10000.0, terrain),
    )
    monkeypatch.setattr(
        "game.missiongenerator.dtc.common.support_tracks", lambda data: [track]
    )
    ((_, points),) = support_boxes(None, 3)  # type: ignore[arg-type]
    half_width = SUPPORT_ORBIT_DIAMETER_M / 2
    xs = sorted({round(x, 3) for x, _ in points})
    ys = sorted({round(y, 3) for _, y in points})
    assert xs == [-half_width, half_width]
    assert ys == [-(10000.0 + half_width), 10000.0 + half_width]


def test_support_box_width_follows_the_orbit_speed() -> None:
    """A tanker's box is as wide as the orbit it flies: a 20-degree turn at its
    orbit speed plus 3 NM each side, never under 2 NM."""
    fast = _support_flight(
        FlightType.REFUELING,
        "Texaco 1",
        Pt(0, 0),
        Pt(20000, 0),
        patrol_speed=knots(430),
    )
    tracks = support_tracks(_mission_data([fast]))
    speed = knots(430).meters_per_second
    turn = speed * speed / (9.81 * math.tan(math.radians(20.0)))
    assert tracks[0].half_width_m == pytest.approx(turn + 3 * 1852.0)
    ((_, points),) = support_boxes(_mission_data([fast]), 3)
    ys = sorted({round(y, 3) for _, y in points})
    assert ys == [round(-(turn + 3 * 1852.0), 3), round(turn + 3 * 1852.0, 3)]

    slow = _support_flight(
        FlightType.REFUELING, "Arco 1", Pt(0, 0), Pt(20000, 0), patrol_speed=knots(1)
    )
    assert support_half_width(slow) == pytest.approx(3 * 1852.0, rel=1e-3)
    # No orbit speed: the fixed default box.
    assert support_half_width(_flight()) is None


def test_viper_draws_the_tanker_boxes_on_the_later_line_sets(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """L1 is the boundary; a tanker's box takes L2-L4. The AWACS gets none."""
    flight, mission_data, game = _hornet_fixture()
    flight.aircraft_type = SimpleNamespace(dcs_unit_type=SimpleNamespace(id="F-16C_50"))
    monkeypatch.setattr(
        "game.missiongenerator.dtc.common.flot_segments",
        lambda g: [("Front", [(0.0, 0.0), (10000.0, 0.0)])],
    )
    monkeypatch.setattr(
        "game.missiongenerator.dtc.common.support_tracks",
        lambda data: [
            _orbit_track("ARCO", "TKR", 20000.0),
            _orbit_track("MAGIC", "AWACS", 30000.0),
        ],
    )
    data = json.loads(build_viper_cartridge(flight, mission_data, game, "V").to_json())[
        "data"
    ]
    geo = data["MPD"]["GEO_LINES"]
    assert [point["note"] for point in geo if point["L1"]] == ["FLOT", "FLOT"]
    arco = [point for point in geo if point["L2"]]
    assert [point["note"] for point in arco] == ["ARCO"] * SUPPORT_BOX_POINTS
    assert not [point for point in geo if point["L3"]]
    assert (arco[0]["x"], arco[0]["y"]) == (arco[-1]["x"], arco[-1]["y"])
    assert [point["id"] for point in geo][:3] == [
        "GEO_LINES31",
        "GEO_LINES32",
        "GEO_LINES33",
    ]


def test_viper_boxes_take_their_points_from_the_boundary(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Three boxes cost 15 of the 25, so the boundary is thinned to 10 rather
    than a box losing a corner."""
    flight, mission_data, game = _hornet_fixture()
    flight.aircraft_type = SimpleNamespace(dcs_unit_type=SimpleNamespace(id="F-16C_50"))
    monkeypatch.setattr(
        "game.missiongenerator.dtc.common.flot_segments",
        lambda g: [("Front", [(float(i * 1000), 0.0) for i in range(30)])],
    )
    monkeypatch.setattr(
        "game.missiongenerator.dtc.common.support_tracks",
        lambda data: [
            _orbit_track(name, "TKR", 20000.0) for name in ("A", "B", "C", "D")
        ],
    )
    data = json.loads(build_viper_cartridge(flight, mission_data, game, "V").to_json())[
        "data"
    ]
    geo = data["MPD"]["GEO_LINES"]
    assert len(geo) == 25
    # Boxes on L2, L3, L4, and the fourth orbit does not fit.
    assert len([point for point in geo if point["L1"]]) == 10
    for line in ("L2", "L3", "L4"):
        assert len([point for point in geo if point[line]]) == SUPPORT_BOX_POINTS


def test_hornet_tanker_boxes_ride_the_faor_lines(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The SA page draws only the selected CAP point's racetrack, so the gas
    had no always-visible shape until it rode FAOR."""
    flight, mission_data, game = _hornet_fixture()
    monkeypatch.setattr(
        "game.missiongenerator.dtc.common.support_tracks",
        lambda data: [_orbit_track("ARCO", "TKR", 20000.0)],
    )
    data = json.loads(
        build_hornet_cartridge(flight, mission_data, game, "H").to_json()
    )["data"]
    (faor,) = data["SA"]["FAOR_FLOT"]["FAOR"]
    assert faor["id"] == "FAOR_1"
    assert faor["num"] == 1
    assert faor["note"] == "ARCO"
    assert [point["id"] for point in faor["points"]] == [
        f"FAOR_1_PT_{i}" for i in range(1, SUPPORT_BOX_POINTS + 1)
    ]
    assert faor["points"][0]["x"] == faor["points"][-1]["x"]


def test_faor_line_one_is_the_tanker_nearest_the_target() -> None:
    """The SA page draws only FAOR line 1, and with the AWACS first that line
    was the AWACS. The boxes are the tankers, nearest to the target first."""
    flight, mission_data, game = _hornet_fixture()
    # The target sits at (60000, 80000).
    far = _support_flight(FlightType.REFUELING, "Arco 1", Pt(-100000, 0), Pt(-80000, 0))
    near = _support_flight(
        FlightType.REFUELING, "Shell 1", Pt(40000, 60000), Pt(60000, 60000)
    )
    awacs = _support_flight(
        FlightType.AEWC, "Magic 1", Pt(55000, 75000), Pt(75000, 75000)
    )
    mission_data.flights = [flight, far, awacs, near]

    faor = json.loads(
        build_hornet_cartridge(flight, mission_data, game, "Gas").to_json()
    )["data"]["SA"]["FAOR_FLOT"]["FAOR"]
    assert [line["note"] for line in faor] == ["SHELL", "ARCO"]


def test_tanker_boxes_are_omitted_when_orbits_are_off(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    flight, mission_data, game = _hornet_fixture()
    flight.aircraft_type = SimpleNamespace(dcs_unit_type=SimpleNamespace(id="F-16C_50"))
    flight.dtc_options = DtcOptions(friendly_orbits=False)
    monkeypatch.setattr(
        "game.missiongenerator.dtc.common.flot_segments",
        lambda g: [("Front", [(0.0, 0.0), (10000.0, 0.0)])],
    )
    monkeypatch.setattr(
        "game.missiongenerator.dtc.common.support_tracks",
        lambda data: [_orbit_track("ARCO", "TKR", 20000.0)],
    )
    data = json.loads(build_viper_cartridge(flight, mission_data, game, "V").to_json())[
        "data"
    ]
    assert all(point["L1"] for point in data["MPD"]["GEO_LINES"])


def _hornet_sa(flight: Any, mission_data: Any, game: Any) -> Any:
    return json.loads(
        build_hornet_cartridge(flight, mission_data, game, "H").to_json()
    )["data"]["SA"]


def test_hornet_lane_runs_from_the_ip_over_the_target_to_the_split() -> None:
    flight, mission_data, game = _hornet_fixture()
    assert _hornet_sa(flight, mission_data, game)["CORRIDORS"] == []  # no IP

    flight.waypoints = [
        _waypoint("TAKEOFF", FlightWaypointType.TAKEOFF, 0, 0, 0, None),
        _waypoint("JOIN", FlightWaypointType.JOIN, 10000, 10000, 7000, None),
        _waypoint("IP", FlightWaypointType.INGRESS_STRIKE, 40000, 50000, 7000, None),
        _waypoint("TGT", FlightWaypointType.TARGET_POINT, 60000, 80000, 0, None),
        _waypoint("SPLIT", FlightWaypointType.SPLIT, 40000, 90000, 7000, None),
        _waypoint("LANDING", FlightWaypointType.LANDING_POINT, 0, 0, 0, None),
    ]
    (lane,) = _hornet_sa(flight, mission_data, game)["CORRIDORS"]
    assert lane["id"] == "CORR_1"
    assert [(p["x"], p["y"]) for p in lane["points"]] == [
        (40000, 50000),
        (60000, 80000),
        (40000, 90000),
    ]
    assert [p["id"] for p in lane["points"]] == [
        "CORR_1_PT_1",
        "CORR_1_PT_2",
        "CORR_1_PT_3",
    ]

    flight.dtc_options = DtcOptions(route=False)
    assert _hornet_sa(flight, mission_data, game)["CORRIDORS"] == []


@pytest.mark.parametrize(
    "ingress", [FlightWaypointType.INGRESS_CAS, FlightWaypointType.INGRESS_SWEEP]
)
def test_hornet_draws_no_lane_when_no_split_follows_the_ip(
    ingress: FlightWaypointType,
) -> None:
    """CAS and Sweep have no split, so the lane ran on to landing and divert."""
    flight, mission_data, game = _hornet_fixture()
    flight.waypoints = [
        _waypoint("TAKEOFF", FlightWaypointType.TAKEOFF, 0, 0, 0, None),
        _waypoint("IP", ingress, 40000, 50000, 7000, None),
        _waypoint("TGT", FlightWaypointType.TARGET_POINT, 60000, 80000, 0, None),
        _waypoint("EGRESS", FlightWaypointType.EGRESS, 40000, 90000, 7000, None),
        _waypoint("LANDING", FlightWaypointType.LANDING_POINT, 0, 0, 0, None),
        _waypoint("DIVERT", FlightWaypointType.DIVERT, 5000, 5000, 0, None),
    ]
    assert _hornet_sa(flight, mission_data, game)["CORRIDORS"] == []


def test_hornet_tacan_list_carries_the_boat_then_the_fields() -> None:
    """Ships are keyed by unit id and route point, as the editor keys an
    ActivateBeacon task; fields come from the terrain's beacon data, the
    flight's own first, then the rest of the map's."""
    flight, mission_data, game = _hornet_fixture()
    game.theater.terrain.airports = {
        25: SimpleNamespace(
            name="Kutaisi",
            beacons=[SimpleNamespace(id="airfield25_3")],
        )
    }
    tcn = json.loads(build_hornet_cartridge(flight, mission_data, game, "H").to_json())[
        "data"
    ]["TCN"]
    assert tcn[0] == {
        "callsign": "Mother",
        "channel": 71,
        "modeChannel": "X",
        "display_name": "CVN-71 Theodore Roosevelt_P1",
        "elevation": 0,
        "unitId": 17,
        "unitPointNum": 1,
        "x": -90000,
        "y": 40000,
    }
    assert (tcn[1]["display_name"], tcn[1]["callsign"], tcn[1]["channel"]) == (
        "Kutaisi",
        "KTS",
        44,
    )
    assert tcn[1]["x"] != 0 and tcn[1]["y"] != 0
    # Then every other TACAN on the map (Caucasus has six), nearest the route
    # first, with no repeats.
    names = [t["display_name"] for t in tcn]
    assert len(names) == len(set(names)) == 7
    route = [(w.position.x, w.position.y) for w in flight.waypoints]
    distances = [
        min(math.hypot(t["x"] - x, t["y"] - y) for x, y in route) for t in tcn[2:]
    ]
    assert distances == sorted(distances)

    flight.dtc_options = DtcOptions(nav_aids=False)
    data = json.loads(
        build_hornet_cartridge(flight, mission_data, game, "H").to_json()
    )["data"]
    assert data["TCN"] == []


def _zone(points: list[tuple[float, float]], radius_nm: float) -> Any:
    return SimpleNamespace(
        points=[Pt(x, y) for x, y in points],
        radius=SimpleNamespace(meters=radius_nm * 1852.0),
    )


def _viper_geo(flight: Any, mission_data: Any, game: Any) -> Any:
    flight.aircraft_type = SimpleNamespace(dcs_unit_type=SimpleNamespace(id="F-16C_50"))
    return json.loads(build_viper_cartridge(flight, mission_data, game, "V").to_json())[
        "data"
    ]["MPD"]["GEO_LINES"]


def test_viper_boxes_a_cas_working_area_after_the_front(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A CAS flight gets a closed box on its working area: the engagement range
    either side of the track and past each end, on the set after the front."""
    flight, mission_data, game = _hornet_fixture()
    flight.flight_type = FlightType.CAS
    flight.work_zone = _zone([(60000.0, 70000.0), (60000.0, 90000.0)], 10)
    monkeypatch.setattr(
        "game.missiongenerator.dtc.common.flot_segments",
        lambda g: [("Front", [(0.0, 0.0), (10000.0, 0.0)])],
    )
    geo = _viper_geo(flight, mission_data, game)
    assert [p["note"] for p in geo if p["L1"]] == ["FLOT", "FLOT"]
    box = [p for p in geo if p["L2"]]
    assert [p["note"] for p in box] == ["CAS"] * SUPPORT_BOX_POINTS
    r = 10 * 1852.0
    assert [(p["x"], p["y"]) for p in box] == [
        (60000.0 + r, 70000.0 - r),
        (60000.0 + r, 90000.0 + r),
        (60000.0 - r, 90000.0 + r),
        (60000.0 - r, 70000.0 - r),
        (60000.0 + r, 70000.0 - r),
    ]
    # The fixture's tanker box moves down a set.
    assert {p["note"] for p in geo if p["L3"]} == {"ARCO"}

    flight.dtc_options = DtcOptions(flot_and_zones=False)
    assert not [p for p in _viper_geo(flight, mission_data, game) if p["note"] == "CAS"]


def test_viper_boxes_a_sead_point_and_skips_a_strike() -> None:
    flight, mission_data, game = _hornet_fixture()
    flight.flight_type = FlightType.SEAD
    flight.work_zone = _zone([(60000.0, 80000.0)], 20)
    box = [p for p in _viper_geo(flight, mission_data, game) if p["note"] == "SEAD"]
    r = 20 * 1852.0
    xs = sorted({p["x"] for p in box})
    ys = sorted({p["y"] for p in box})
    assert len(box) == SUPPORT_BOX_POINTS
    assert (xs, ys) == ([60000.0 - r, 60000.0 + r], [80000.0 - r, 80000.0 + r])

    flight.flight_type = FlightType.STRIKE
    notes = {p["note"] for p in _viper_geo(flight, mission_data, game)}
    assert "SEAD" not in notes and "CAS" not in notes
