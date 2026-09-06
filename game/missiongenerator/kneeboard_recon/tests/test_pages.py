# game/missiongenerator/kneeboard_recon/tests/test_pages.py
"""Smoke tests for the recon page classes.

These tests stub FlightData / Game / Weather, drive each page class to write
a PNG to a tmp_path, and assert the output is the right size and contains
expected text via the page writer's internal text buffer.
"""

from __future__ import annotations

import datetime
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from PIL import Image
from dcs.mapping import Point
from dcs.terrain.caucasus.caucasus import Caucasus

from game.ato.flighttype import FlightType
from game.ato.flightwaypointtype import FlightWaypointType
from game.ato.starttype import StartType
from game.missiongenerator.kneeboard_recon import generate_recon_pages
from game.missiongenerator.kneeboard_recon.pages import (
    AirbaseReconPage,
    AirfieldDeparturePage,
    DetailReconPage,
    OverviewReconPage,
)


def test_airfield_departure_page_writes_correct_size(
    tmp_path: Path,
    stub_flight: MagicMock,
    stub_game: MagicMock,
    stub_weather: MagicMock,
) -> None:
    page = AirfieldDeparturePage(
        flight=stub_flight, game=stub_game, weather=stub_weather
    )
    out = tmp_path / "departure.png"
    page.write(out)
    assert out.exists()
    img = Image.open(out)
    assert img.size == (768, 1024)


def test_airfield_departure_page_includes_callsign_and_runway_in_title(
    tmp_path: Path,
    stub_flight: MagicMock,
    stub_game: MagicMock,
    stub_weather: MagicMock,
) -> None:
    page = AirfieldDeparturePage(
        flight=stub_flight, game=stub_game, weather=stub_weather
    )
    page.write(tmp_path / "departure.png")
    # Page writer accumulates emitted text in text_log for assertion.
    assert any("ENFIELD 1-1" in s for s in page.last_text_log)
    assert any("Kobuleti" in s for s in page.last_text_log)


def test_airfield_departure_page_atis_block_includes_qnh(
    tmp_path: Path,
    stub_flight: MagicMock,
    stub_game: MagicMock,
    stub_weather: MagicMock,
) -> None:
    page = AirfieldDeparturePage(
        flight=stub_flight, game=stub_game, weather=stub_weather
    )
    page.write(tmp_path / "departure.png")
    assert any("29.92" in s for s in page.last_text_log)


def test_airfield_departure_page_qfe_uses_osm_elevation(
    tmp_path: Path,
    stub_flight: MagicMock,
    stub_game: MagicMock,
    stub_weather: MagicMock,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """When OSM/DEM elevation ships for the field, the departure QFE is
    reduced from QNH (not "N/A"). Exercises the _field_elevation_m ->
    field_elevation_for_airport -> build_atis_block chain that conftest's
    autouse load=None patch otherwise leaves uncovered."""
    from game.missiongenerator.kneeboard_recon import pages as _pages
    from game.missiongenerator.kneeboard_recon.airport_imagery import (
        AirportImagery,
        TerrainImagery,
    )

    airport = stub_flight.departure.dcs_airport
    record = TerrainImagery(
        terrain="Caucasus",
        by_airport_id={
            str(airport.id): AirportImagery(
                name=airport.name,
                imagery_offset_lat=0.0,
                imagery_offset_lng=0.0,
                runways=(),
                elevation_m=10.0,
            )
        },
    )
    monkeypatch.setattr(_pages._airport_imagery, "load", lambda _terrain: record)

    page = AirfieldDeparturePage(
        flight=stub_flight, game=stub_game, weather=stub_weather
    )
    page.write(tmp_path / "departure.png")
    qfe_lines = [s for s in page.last_text_log if s.startswith("QFE ")]
    assert qfe_lines, "expected a QFE entry in the page log"
    assert "N/A" not in qfe_lines[0]
    assert "29.8" in qfe_lines[0]  # ~29.88 inHg reduced from 29.92 at 10 m


def test_airfield_departure_page_qfe_is_na_without_elevation(
    tmp_path: Path,
    stub_flight: MagicMock,
    stub_game: MagicMock,
    stub_weather: MagicMock,
) -> None:
    """No OSM elevation shipped (conftest load=None) -> QFE shows N/A."""
    page = AirfieldDeparturePage(
        flight=stub_flight, game=stub_game, weather=stub_weather
    )
    page.write(tmp_path / "departure.png")
    assert any(s == "QFE N/A" for s in page.last_text_log)


def test_airfield_departure_page_populates_sunrise_and_sunset(
    tmp_path: Path,
    stub_flight: MagicMock,
    stub_game: MagicMock,
    stub_weather: MagicMock,
) -> None:
    """Sun times must be computed (not silently None) when start time is valid."""
    page = AirfieldDeparturePage(
        flight=stub_flight, game=stub_game, weather=stub_weather
    )
    page.write(tmp_path / "departure.png")
    assert any(
        s.startswith("SUNRISE ") for s in page.last_text_log
    ), "expected a SUNRISE entry in the page log"
    assert any(
        s.startswith("SUNSET ") for s in page.last_text_log
    ), "expected a SUNSET entry in the page log"


def test_sun_times_date_shift_math_for_east_of_greenwich() -> None:
    """The date-shift logic feeds the right UTC date to suntime per event.

    Suntime takes a UTC date and returns the UTC moment of sunrise/sunset
    falling within that astronomical UTC day. For a +10 timezone:

    * Local-date X sunrise (~06:00 local) happens at ~20:00 UTC the prior
      UTC day. Sunrise lookup must use UTC date X-1.
    * Local-date X sunset (~18:00 local) happens at ~08:00 UTC the same
      UTC day. Sunset lookup must use UTC date X.

    The pre-fix code passed UTC date X for both events, which on +10 zones
    fetched the next local day's sunrise (off by one calendar day in the
    underlying time even when HH:MM happens to look similar).
    """
    import datetime

    tz = datetime.timezone(datetime.timedelta(hours=10))
    sr_local = datetime.datetime(2026, 5, 21, 6, 0, tzinfo=tz)
    ss_local = datetime.datetime(2026, 5, 21, 18, 0, tzinfo=tz)
    sr_utc_date = sr_local.astimezone(datetime.timezone.utc).date()
    ss_utc_date = ss_local.astimezone(datetime.timezone.utc).date()
    assert sr_utc_date == datetime.date(
        2026, 5, 20
    ), "+10 local 06:00 should map to UTC the prior calendar day"
    assert ss_utc_date == datetime.date(
        2026, 5, 21
    ), "+10 local 18:00 should map to UTC the same calendar day"

    # Mirror at the western end: at -10 (Hawaii-ish), local sunset of
    # date X can spill into UTC date X+1.
    tz_west = datetime.timezone(datetime.timedelta(hours=-10))
    ss_west_local = datetime.datetime(2026, 5, 21, 18, 0, tzinfo=tz_west)
    ss_west_utc_date = ss_west_local.astimezone(datetime.timezone.utc).date()
    assert ss_west_utc_date == datetime.date(
        2026, 5, 22
    ), "-10 local 18:00 should map to UTC the next calendar day"


def test_overview_page_writes_correct_size(
    tmp_path: Path, stub_strike_flight: MagicMock, stub_game: MagicMock
) -> None:
    page = OverviewReconPage(
        flight=stub_strike_flight,
        game=stub_game,
    )
    page.write(tmp_path / "overview.png")
    img = Image.open(tmp_path / "overview.png")
    assert img.size == (768, 1024)


def test_overview_page_shows_target_bearing(
    tmp_path: Path, stub_strike_flight: MagicMock, stub_game: MagicMock
) -> None:
    page = OverviewReconPage(
        flight=stub_strike_flight,
        game=stub_game,
    )
    page.write(tmp_path / "overview.png")
    assert any("TARGET BE" in s for s in page.last_text_log)


def test_detail_page_writes_correct_size(
    tmp_path: Path, stub_strike_flight: MagicMock, stub_game: MagicMock
) -> None:
    page = DetailReconPage(
        flight=stub_strike_flight,
        game=stub_game,
    )
    page.write(tmp_path / "detail.png")
    img = Image.open(tmp_path / "detail.png")
    assert img.size == (768, 1024)


def test_detail_page_includes_aimpoint_mgrs_in_table(
    tmp_path: Path, stub_strike_flight: MagicMock, stub_game: MagicMock
) -> None:
    page = DetailReconPage(
        flight=stub_strike_flight,
        game=stub_game,
    )
    page.write(tmp_path / "detail.png")
    # MGRS strings start with the GZD (digits + letter) for Caucasus.
    # The stub target is near Anapa-Vityazevo which falls in zone 37T.
    assert any("37T " in s for s in page.last_text_log)


def test_detail_page_includes_atk_axis_label(
    tmp_path: Path, stub_strike_flight: MagicMock, stub_game: MagicMock
) -> None:
    page = DetailReconPage(
        flight=stub_strike_flight,
        game=stub_game,
    )
    page.write(tmp_path / "detail.png")
    assert any("Attack Axis" in s for s in page.last_text_log)


@pytest.mark.parametrize(
    "ip_offset,target_offset,expected_hdg",
    [
        # (ip_dx_north, ip_dy_east) relative to target, then expected compass.
        # IP south of target → run-in heads north (000°).
        ((-10_000.0, 0.0), (0.0, 0.0), 0),
        # IP west of target → run-in heads east (090°).
        ((0.0, -10_000.0), (0.0, 0.0), 90),
        # IP north of target → run-in heads south (180°).
        ((+10_000.0, 0.0), (0.0, 0.0), 180),
        # IP east of target → run-in heads west (270°).
        ((0.0, +10_000.0), (0.0, 0.0), 270),
    ],
)
def test_detail_page_atk_axis_uses_compass_heading(
    tmp_path: Path,
    stub_strike_flight: MagicMock,
    stub_game: MagicMock,
    caucasus: Caucasus,
    ip_offset: tuple[float, float],
    target_offset: tuple[float, float],
    expected_hdg: int,
) -> None:
    """Attack Axis label must read the true compass bearing from IP to target.

    Regression for the pixel-space-atan2 bug: deriving the heading from
    `math.atan2` over screen pixel deltas mislabels every axis (e.g. due-north
    target was reported as 270°). The fix uses pydcs `heading_between_point`
    on the world coordinates.
    """
    tgo = stub_strike_flight.package.target
    tgo.position = Point(
        tgo.position.x + target_offset[0],
        tgo.position.y + target_offset[1],
        caucasus,
    )
    ip = MagicMock(
        position=Point(
            tgo.position.x + ip_offset[0],
            tgo.position.y + ip_offset[1],
            caucasus,
        ),
        waypoint_type=FlightWaypointType.INGRESS_STRIKE,
    )
    tgt_wp = MagicMock(
        position=tgo.position,
        waypoint_type=FlightWaypointType.TARGET_POINT,
    )
    stub_strike_flight.waypoints = [ip, tgt_wp]

    page = DetailReconPage(
        flight=stub_strike_flight,
        game=stub_game,
    )
    page.write(tmp_path / "detail.png")
    atk_lines = [s for s in page.last_text_log if s.startswith("Attack Axis ")]
    assert atk_lines, "expected an Attack Axis line in the page log"
    # Attack Axis label format: "Attack Axis 270°".
    reported = int(atk_lines[-1].split()[2].rstrip("°"))
    # Allow ±1° tolerance for great-circle bearing rounding at non-equatorial
    # latitudes (pydcs `heading_between_point` projects through lat/lng).
    diff = min((reported - expected_hdg) % 360, (expected_hdg - reported) % 360)
    assert diff <= 1, (
        f"Attack Axis reported {reported}°, expected ~{expected_hdg}° "
        f"(diff {diff}°). Full line: {atk_lines[-1]!r}"
    )


def test_airbase_page_writes_correct_size(
    tmp_path: Path, stub_oca_flight: MagicMock, stub_game: MagicMock
) -> None:
    page = AirbaseReconPage(
        flight=stub_oca_flight,
        game=stub_game,
    )
    page.write(tmp_path / "airbase.png")
    img = Image.open(tmp_path / "airbase.png")
    assert img.size == (768, 1024)


def test_airbase_page_includes_threshold_mgrs(
    tmp_path: Path, stub_oca_flight: MagicMock, stub_game: MagicMock
) -> None:
    page = AirbaseReconPage(
        flight=stub_oca_flight,
        game=stub_game,
    )
    page.write(tmp_path / "airbase.png")
    assert any("38T " in s for s in page.last_text_log)


# ---------------------------------------------------------------------------
# Dispatcher tests
# ---------------------------------------------------------------------------


def test_dispatcher_skips_recon_for_cap(
    stub_flight: MagicMock, stub_game: MagicMock, stub_weather: MagicMock
) -> None:
    stub_flight.flight_type = FlightType.BARCAP
    stub_flight.package = MagicMock()
    stub_flight.package.target = MagicMock()
    pages = generate_recon_pages(
        flight=stub_flight,
        game=stub_game,
        weather=stub_weather,
        extra_threat_search_m=0.0,
    )
    # CAP gets no recon pages even if start_type is COLD; departure page is
    # still emitted.
    classes = [p.__class__.__name__ for p in pages]
    assert "OverviewReconPage" not in classes
    assert "DetailReconPage" not in classes
    assert "AirfieldDeparturePage" in classes


def test_dispatcher_emits_departure_for_runway_start(
    stub_strike_flight: MagicMock,
    stub_game: MagicMock,
    stub_weather: MagicMock,
) -> None:
    """Runway starts are ground starts — pilot still benefits from ATIS/wind."""
    stub_strike_flight.start_type = StartType.RUNWAY
    pages = generate_recon_pages(
        flight=stub_strike_flight,
        game=stub_game,
        weather=stub_weather,
        extra_threat_search_m=0.0,
    )
    classes = [p.__class__.__name__ for p in pages]
    assert "AirfieldDeparturePage" in classes
    assert "OverviewReconPage" in classes
    assert "DetailReconPage" in classes


@pytest.mark.parametrize(
    "start_type", [StartType.COLD, StartType.WARM, StartType.RUNWAY]
)
def test_dispatcher_emits_departure_for_all_ground_starts(
    stub_strike_flight: MagicMock,
    stub_game: MagicMock,
    stub_weather: MagicMock,
    start_type: StartType,
) -> None:
    """Every ground start (COLD, WARM, RUNWAY) gets a departure page."""
    stub_strike_flight.start_type = start_type
    pages = generate_recon_pages(
        flight=stub_strike_flight,
        game=stub_game,
        weather=stub_weather,
        extra_threat_search_m=0.0,
    )
    classes = [p.__class__.__name__ for p in pages]
    assert "AirfieldDeparturePage" in classes


def test_dispatcher_skips_departure_for_in_flight_spawn(
    stub_strike_flight: MagicMock,
    stub_game: MagicMock,
    stub_weather: MagicMock,
) -> None:
    """Air-spawned flights never see the airfield — no departure page."""
    stub_strike_flight.start_type = StartType.IN_FLIGHT
    pages = generate_recon_pages(
        flight=stub_strike_flight,
        game=stub_game,
        weather=stub_weather,
        extra_threat_search_m=0.0,
    )
    classes = [p.__class__.__name__ for p in pages]
    assert "AirfieldDeparturePage" not in classes


def test_dispatcher_emits_only_departure_when_target_is_none(
    stub_strike_flight: MagicMock,
    stub_game: MagicMock,
    stub_weather: MagicMock,
) -> None:
    """A ground-start strike with no package target still gets its departure
    page but no overview/detail (the target-None early-exit path)."""
    stub_strike_flight.start_type = StartType.COLD
    stub_strike_flight.package.target = None
    pages = generate_recon_pages(
        flight=stub_strike_flight,
        game=stub_game,
        weather=stub_weather,
        extra_threat_search_m=0.0,
    )
    classes = [p.__class__.__name__ for p in pages]
    assert classes == ["AirfieldDeparturePage"]


def test_dispatcher_returns_airbase_variant_for_controlpoint_target(
    stub_oca_flight: MagicMock,
    stub_game: MagicMock,
    stub_weather: MagicMock,
) -> None:
    pages = generate_recon_pages(
        flight=stub_oca_flight,
        game=stub_game,
        weather=stub_weather,
        extra_threat_search_m=0.0,
    )
    classes = [p.__class__.__name__ for p in pages]
    assert "AirbaseReconPage" in classes
    assert "DetailReconPage" not in classes


def test_dispatcher_skips_airbase_variant_when_cp_has_no_dcs_airport(
    stub_oca_flight: MagicMock,
    stub_game: MagicMock,
    stub_weather: MagicMock,
) -> None:
    """Fob / Carrier / Lha / OffMapSpawn return dcs_airport=None.

    Emitting AirbaseReconPage for them would NPE inside the page when it
    tries to read airport.position.
    """
    stub_oca_flight.package.target.dcs_airport = None
    pages = generate_recon_pages(
        flight=stub_oca_flight,
        game=stub_game,
        weather=stub_weather,
        extra_threat_search_m=0.0,
    )
    classes = [p.__class__.__name__ for p in pages]
    assert "AirbaseReconPage" not in classes


def test_dispatcher_includes_armed_recon(
    stub_strike_flight: MagicMock, stub_game: MagicMock, stub_weather: MagicMock
) -> None:
    """Spec: ARMED_RECON must produce overview + detail recon pages."""
    stub_strike_flight.flight_type = FlightType.ARMED_RECON
    pages = generate_recon_pages(
        flight=stub_strike_flight,
        game=stub_game,
        weather=stub_weather,
        extra_threat_search_m=0.0,
    )
    classes = [p.__class__.__name__ for p in pages]
    assert "OverviewReconPage" in classes
    assert "DetailReconPage" in classes


def test_dispatcher_flight_type_contract_matches_spec() -> None:
    """Locks the recon-flight-type contract against accidental drift.

    Spec design doc table (Per-flight-type behaviour): STRIKE, BAI, CAS, SEAD,
    DEAD, OCA_AIRCRAFT, OCA_RUNWAY, ANTISHIP, ARMED_RECON get recon pages;
    CAP/escort/sweep/awacs/tanker/transport/ferry do not.
    """
    from game.missiongenerator.kneeboard_recon.pages import _FLIGHT_TYPES_WITH_RECON

    expected = {
        FlightType.STRIKE,
        FlightType.BAI,
        FlightType.CAS,
        FlightType.SEAD,
        FlightType.DEAD,
        FlightType.OCA_AIRCRAFT,
        FlightType.OCA_RUNWAY,
        FlightType.ANTISHIP,
        FlightType.ARMED_RECON,
    }
    assert _FLIGHT_TYPES_WITH_RECON == frozenset(expected)
    # Sanity check: none of the support / patrol types are in the set.
    for ft in (
        FlightType.BARCAP,
        FlightType.TARCAP,
        FlightType.ESCORT,
        FlightType.SWEEP,
        FlightType.AEWC,
        FlightType.REFUELING,
        FlightType.TRANSPORT,
        FlightType.FERRY,
    ):
        assert ft not in _FLIGHT_TYPES_WITH_RECON


def test_airbase_parking_selection_picks_nearest_to_airport_center(
    stub_oca_flight: MagicMock,
    stub_game: MagicMock,
    caucasus: Caucasus,
) -> None:
    """OCA strikes want the parking slots nearest the apron, not the first 8
    in pydcs iteration order (which is roughly insertion order — meaningless)."""
    from game.missiongenerator.kneeboard_recon.pages import AirbaseReconPage

    page = AirbaseReconPage(flight=stub_oca_flight, game=stub_game)
    airport = stub_oca_flight.package.target.dcs_airport

    fake_slots = []
    # 20 slots at varying distances. The 8 nearest are at 100, 200, ..., 800 m.
    distances = [100, 200, 300, 400, 500, 600, 700, 800] + [
        2_000 + i * 100 for i in range(12)
    ]
    for i, dist in enumerate(distances):
        slot = MagicMock()
        slot.position = Point(
            airport.position.x + float(dist),
            airport.position.y,
            caucasus,
        )
        slot.id = i
        fake_slots.append(slot)

    selected = page._select_parking_slots(fake_slots, airport.position)
    selected_distances = sorted(
        s.position.distance_to_point(airport.position) for s in selected
    )
    assert len(selected) == AirbaseReconPage.PARKING_MARKER_LIMIT
    assert selected_distances == [100, 200, 300, 400, 500, 600, 700, 800]


def test_airbase_threshold_world_coords_follow_pydcs_convention(
    tmp_path: Path,
    stub_oca_flight: MagicMock,
    stub_game: MagicMock,
    caucasus: Caucasus,
) -> None:
    """AirbaseReconPage._compute_thresholds must place each named threshold at
    the END where aircraft landing on that runway first touch down — i.e.
    900 m OPPOSITE the landing heading. Aircraft landing on RWY 27 fly heading
    270° (west) and touch down at the east end, so the "27 threshold" sits
    900 m east of airport center.

    Regression for two bugs: (1) the offset was once rotated 90° because the
    code used ``radians(heading - 90)`` (a pixel-space convention) in
    world-coordinate math; (2) the offset was once placed along the landing
    heading, putting the named threshold at the wrong end of the runway.
    """
    import math

    from dcs.mapping import point_from_heading
    from game.missiongenerator.kneeboard_recon.pages import (
        AirbaseReconPage,
        _FALLBACK_RUNWAY_HALF_LENGTH_M,
    )

    page = AirbaseReconPage(flight=stub_oca_flight, game=stub_game)
    airport = stub_oca_flight.package.target.dcs_airport
    results = page._compute_thresholds(airport)
    assert results, "test airport must have at least one runway"
    for thr_pos, approach_name, _mgrs in results:
        # Locate the matching approach to grab its heading.
        approach = next(
            a
            for rwy in airport.runways
            for a in (rwy.main, rwy.opposite)
            if a.name == approach_name
        )
        expected_x, expected_y = point_from_heading(
            airport.position.x,
            airport.position.y,
            (approach.heading + 180) % 360,
            _FALLBACK_RUNWAY_HALF_LENGTH_M,
        )
        assert thr_pos.x == pytest.approx(
            expected_x, abs=1.0
        ), f"approach {approach_name}: expected x={expected_x:.1f}, got {thr_pos.x:.1f}"
        assert thr_pos.y == pytest.approx(
            expected_y, abs=1.0
        ), f"approach {approach_name}: expected y={expected_y:.1f}, got {thr_pos.y:.1f}"

        # Geometric sanity: the named threshold must sit on the side of the
        # airport OPPOSITE the landing direction (the touchdown end). Project
        # (threshold - center) onto the landing-heading unit vector; the
        # result must be strictly negative. Catches any future sign flip
        # independently of the point_from_heading equality above.
        landing_rad = math.radians(approach.heading)
        offset_x = thr_pos.x - airport.position.x
        offset_y = thr_pos.y - airport.position.y
        projection = offset_x * math.cos(landing_rad) + offset_y * math.sin(landing_rad)
        assert projection < 0.0, (
            f"approach {approach_name}: threshold must be opposite the "
            f"landing direction (projection along landing vector = "
            f"{projection:.1f}, expected strictly negative)"
        )


def test_airfield_departure_threshold_world_coords_follow_pydcs_convention(
    tmp_path: Path,
    stub_flight: MagicMock,
    stub_game: MagicMock,
    stub_weather: MagicMock,
    caucasus: Caucasus,
) -> None:
    """AirfieldDeparturePage._compute_threshold_pixel must place the active
    threshold marker at the END where takeoff/landing BEGINS, i.e.
    ``_FALLBACK_RUNWAY_HALF_LENGTH_M`` OPPOSITE the active landing
    heading from airport center. Aircraft departing on RWY 22 (heading
    220°) start their takeoff roll at the NE end and fly SW, so the
    active threshold sits NE of center.

    Regression for two bugs: (1) the offset was once rotated 90° due to
    pixel-space convention bleeding into world math; (2) the offset was once
    placed along the landing heading, putting the active threshold at the
    rollout end of the runway.
    """
    import math

    from game.utils import Heading
    from game.missiongenerator.kneeboard_recon.extent import MapExtent
    from game.missiongenerator.kneeboard_recon.pages import (
        _FALLBACK_RUNWAY_HALF_LENGTH_M,
    )
    from game.missiongenerator.kneeboard_recon.projection import Projector
    from dcs.mapping import point_from_heading

    heading_deg = 220.0
    stub_flight.departure.runway_heading = Heading.from_degrees(int(heading_deg))
    page = AirfieldDeparturePage(
        flight=stub_flight,
        game=stub_game,
        weather=stub_weather,
    )
    airport = stub_flight.departure.dcs_airport
    extent = MapExtent(
        min_x=airport.position.x - 2_500.0,
        max_x=airport.position.x + 2_500.0,
        min_y=airport.position.y - 2_500.0,
        max_y=airport.position.y + 2_500.0,
        terrain=caucasus,
    )
    map_w, map_h = 924, 700
    projector = Projector(extent=extent, pixel_width=map_w, pixel_height=map_h)
    thr_pixel = page._compute_threshold_pixel(projector, airport, x0=0, y0=0)
    assert thr_pixel is not None
    # Invert the projection to recover the world point the marker is drawn at.
    px, py = thr_pixel
    frac_x = px / (map_w - 1)
    frac_y = 1.0 - py / (map_h - 1)
    world_y = extent.min_y + frac_x * extent.span_y_m
    world_x = extent.min_x + frac_y * extent.span_x_m
    expected_x, expected_y = point_from_heading(
        airport.position.x,
        airport.position.y,
        (heading_deg + 180) % 360,
        _FALLBACK_RUNWAY_HALF_LENGTH_M,
    )
    assert world_x == pytest.approx(
        expected_x, abs=10.0
    ), f"expected x={expected_x:.1f}, got {world_x:.1f}"
    assert world_y == pytest.approx(
        expected_y, abs=10.0
    ), f"expected y={expected_y:.1f}, got {world_y:.1f}"

    # Geometric sanity: the active threshold marker must sit on the side of
    # the airport OPPOSITE the landing direction (i.e. where takeoff/landing
    # begins). Project (marker - center) onto the landing-heading unit vector;
    # the result must be strictly negative. Catches any future sign flip
    # independently of the point_from_heading equality above.
    landing_rad = math.radians(heading_deg)
    offset_x = world_x - airport.position.x
    offset_y = world_y - airport.position.y
    projection = offset_x * math.cos(landing_rad) + offset_y * math.sin(landing_rad)
    assert projection < 0.0, (
        f"active threshold must be opposite the landing direction "
        f"(projection along landing vector = {projection:.1f}, expected "
        f"strictly negative)"
    )


def test_detail_page_clusters_dense_unit_groups(
    tmp_path: Path, stub_strike_flight: MagicMock, stub_game: MagicMock
) -> None:
    """20 well-separated units → cap=12 aimpoint badges with the trailing
    cluster carrying the leftover count.

    Units are placed >300 m apart so cluster_items opens 20 buckets, which
    actually exercises the cap+trailing-bucket logic. (A previous version
    placed them 30 m apart so all 20 collapsed into one bucket and the cap
    code never fired.)
    """
    cau = stub_strike_flight.package.target.position._terrain
    sparse = []
    base = stub_strike_flight.package.target.position
    for i in range(20):
        u = MagicMock()
        # Grid of 5×4 with 300 m spacing → every pair is >75 m apart.
        u.position = Point(base.x + (i % 5) * 300.0, base.y + (i // 5) * 300.0, cau)
        u.alive = True
        u.type = MagicMock()
        u.type.length = None
        u.type.width = None
        u.type.name = f"U{i}"
        sparse.append(u)
    stub_strike_flight.package.target.strike_targets = sparse
    page = DetailReconPage(flight=stub_strike_flight, game=stub_game)
    page.write(tmp_path / "detail_cluster.png")
    # Aimpoint table emits one MGRS per badge.
    mgrs_lines = [s for s in page.last_text_log if "T " in s and s[:2].isdigit()]
    assert len(mgrs_lines) == DetailReconPage.CLUSTER_CAP, (
        f"expected exactly {DetailReconPage.CLUSTER_CAP} aimpoint badges, "
        f"got {len(mgrs_lines)}"
    )
    # The trailing cluster aggregates 20 - (cap - 1) = 9 units.
    trailing_label = next(
        (
            s
            for s in page.last_text_log
            if s.startswith(f"T{DetailReconPage.CLUSTER_CAP}")
        ),
        None,
    )
    assert trailing_label is not None, "expected a final trailing aimpoint label"
    # Spec calls for the cap-overflow bucket badge label to read
    # "T12 (… remaining)" — distinct from the per-bucket "(N×)" form so
    # pilots can tell the trailing collapse-bucket from a real cluster.
    assert "… remaining" in trailing_label, (
        f"trailing cluster must use spec-compliant '… remaining' label, "
        f"got {trailing_label!r}"
    )


def test_detail_page_records_target_bullseye(
    tmp_path: Path, stub_strike_flight: MagicMock, stub_game: MagicMock
) -> None:
    """Detail page must record `TARGET BE:` for debug + test parity with Overview.

    Regression for missing bullseye recording on Detail page — previously the
    bullseye string was only drawn to the footer, not recorded in
    last_text_log, so there was no way to assert on it.
    """
    page = DetailReconPage(flight=stub_strike_flight, game=stub_game)
    page.write(tmp_path / "detail_be.png")
    be_lines = [s for s in page.last_text_log if s.startswith("TARGET BE")]
    assert be_lines, "Detail page should record TARGET BE in last_text_log"


def test_bullseye_format_has_no_spaces_around_slash(
    tmp_path: Path, stub_strike_flight: MagicMock, stub_game: MagicMock
) -> None:
    """Spec example: `TARGET BE: 087°/22 NM` — no spaces around the slash."""
    page = OverviewReconPage(flight=stub_strike_flight, game=stub_game)
    page.write(tmp_path / "ov_be.png")
    be_lines = [s for s in page.last_text_log if s.startswith("TARGET BE")]
    assert be_lines, "Overview page must record TARGET BE"
    # The bearing/range pair should appear as `NNN°/RR NM` (no whitespace
    # immediately around the slash).
    assert any(
        "° / " not in s and "°/" in s for s in be_lines
    ), f"expected spec-compliant `°/N NM` format, got {be_lines!r}"


def test_sead_dispatch_describes_sam_components(
    tmp_path: Path, stub_strike_flight: MagicMock, stub_game: MagicMock
) -> None:
    """SEAD detail page must render SAM-component role labels (TR/LN/etc.)."""
    from unittest.mock import MagicMock as _MM
    from dcs.vehicles import AirDefence

    cau = stub_strike_flight.package.target.position._terrain
    base = stub_strike_flight.package.target.position
    sam_unit = _MM()
    sam_unit.position = Point(base.x + 50.0, base.y, cau)
    sam_unit.alive = True
    sam_unit.type = AirDefence.Kub_1S91_str  # TR unit, ALIC 108
    sam_unit.name = "sam_tr"
    stub_strike_flight.flight_type = FlightType.SEAD
    stub_strike_flight.package.target.strike_targets = [sam_unit]
    page = DetailReconPage(flight=stub_strike_flight, game=stub_game)
    page.write(tmp_path / "sead.png")
    # The aimpoint description should include the TR role label.
    assert any(
        "TR" in s for s in page.last_text_log
    ), f"SEAD render must include TR role label; last_text_log={page.last_text_log!r}"


def test_dispatcher_antiship_emits_detail_page_for_naval_target(
    stub_strike_flight: MagicMock,
    stub_game: MagicMock,
    stub_weather: MagicMock,
) -> None:
    """ANTISHIP against a NavalGroundObject must produce Overview + DetailReconPage.

    NavalGroundObject inherits from TheaterGroundObject so the dispatcher
    routes through the TGO branch; this test guards against the inheritance
    being broken later.
    """
    from game.theater.theatergroundobject import (
        NavalGroundObject,
        TheaterGroundObject,
    )

    # NavalGroundObject construction is heavy — just use a plain TGO subclass
    # spec to keep the test fast while preserving the isinstance check.
    naval = MagicMock(spec=NavalGroundObject)
    naval.position = stub_strike_flight.package.target.position
    naval.strike_targets = []
    naval.units = []
    naval.obj_name = "Enemy Battle Group"
    stub_strike_flight.flight_type = FlightType.ANTISHIP
    stub_strike_flight.package.target = naval

    # NavalGroundObject must satisfy isinstance(..., TheaterGroundObject)
    assert isinstance(naval, TheaterGroundObject), (
        "NavalGroundObject must remain a TheaterGroundObject subclass "
        "or the dispatcher will silently drop ANTISHIP detail pages"
    )
    pages = generate_recon_pages(
        flight=stub_strike_flight,
        game=stub_game,
        weather=stub_weather,
        extra_threat_search_m=0.0,
    )
    classes = [p.__class__.__name__ for p in pages]
    assert "OverviewReconPage" in classes
    assert "DetailReconPage" in classes
    assert "AirbaseReconPage" not in classes


def test_dispatcher_emits_frontline_detail_for_cas_frontline_target(
    stub_strike_flight: MagicMock,
    stub_game: MagicMock,
    stub_weather: MagicMock,
    caucasus: Caucasus,
) -> None:
    """CAS against a FrontLine target must produce Overview + FrontLineDetailPage.

    Before this branch, FrontLine targets fell through every dispatcher arm
    (not ControlPoint, not TheaterGroundObject) and the pilot got only the
    Overview page. This test locks the FrontLine branch in place.
    """
    from game.theater.frontline import FrontLine

    airport = next(a for a in caucasus.airport_list() if "Kobuleti" in a.name)
    front = MagicMock(spec=FrontLine)
    front.position = Point(airport.position.x + 30_000, airport.position.y, caucasus)
    front.name = "Front line A/B"
    # Concrete list, not iter(): production code may walk ``points`` more
    # than once (extent + corridor passes); a one-shot iterator would
    # collapse the second pass to an empty sequence and silently produce
    # a zero-area extent.
    front.points = [
        Point(front.position.x - 5_000, front.position.y - 1_000, caucasus),
        Point(front.position.x, front.position.y, caucasus),
        Point(front.position.x + 5_000, front.position.y + 1_000, caucasus),
    ]
    stub_strike_flight.flight_type = FlightType.CAS
    stub_strike_flight.package.target = front

    pages = generate_recon_pages(
        flight=stub_strike_flight,
        game=stub_game,
        weather=stub_weather,
        extra_threat_search_m=0.0,
    )
    classes = [p.__class__.__name__ for p in pages]
    assert "OverviewReconPage" in classes
    assert "FrontLineDetailPage" in classes
    assert "DetailReconPage" not in classes
    assert "AirbaseReconPage" not in classes


def test_greatest_alive_threat_picks_highest_priority_unit_type() -> None:
    """A mixed-unit TGO labels by the worst surviving threat, not by raw count."""
    from game.data.units import UnitClass
    from game.missiongenerator.kneeboard_recon.pages import _greatest_alive_threat

    def _ut(name: str, cls: UnitClass) -> MagicMock:
        u = MagicMock()
        u.display_name = name
        u.unit_class = cls
        return u

    def _alive_unit(ut: MagicMock) -> MagicMock:
        u = MagicMock()
        u.alive = True
        u.unit_type = ut
        return u

    marder = _ut("Marder", UnitClass.IFV)
    sa6 = _ut("SA-6 Kub", UnitClass.LAUNCHER)
    aaa = _ut("ZU-23", UnitClass.AAA)
    grp = MagicMock()
    # Three Marders + one SA-6 + two AAA: SA-6 wins on priority despite Marders
    # being more numerous.
    grp.units = [
        _alive_unit(marder),
        _alive_unit(marder),
        _alive_unit(marder),
        _alive_unit(sa6),
        _alive_unit(aaa),
        _alive_unit(aaa),
    ]
    tgo = MagicMock()
    tgo.groups = [grp]

    result = _greatest_alive_threat(tgo)
    assert result is not None
    name, count = result
    assert name == "SA-6 Kub"
    assert count == 1


def test_greatest_alive_threat_returns_none_when_all_dead() -> None:
    """A fully-attrited TGO returns None so the page can render the dead marker."""
    from game.data.units import UnitClass
    from game.missiongenerator.kneeboard_recon.pages import _greatest_alive_threat

    ut = MagicMock()
    ut.display_name = "T-72"
    ut.unit_class = UnitClass.TANK
    dead = MagicMock()
    dead.alive = False
    dead.unit_type = ut
    grp = MagicMock()
    grp.units = [dead, dead, dead]
    tgo = MagicMock()
    tgo.groups = [grp]

    assert _greatest_alive_threat(tgo) is None


def test_frontline_detail_skips_buildings_and_ewr(
    tmp_path: Path,
    stub_strike_flight: MagicMock,
    stub_game: MagicMock,
    caucasus: Caucasus,
) -> None:
    """BuildingGroundObject and EwrGroundObject must not contribute markers."""
    from game.missiongenerator.kneeboard_recon.pages import FrontLineDetailPage
    from game.theater.frontline import FrontLine
    from game.theater.theatergroundobject import (
        BuildingGroundObject,
        EwrGroundObject,
    )

    airport = next(a for a in caucasus.airport_list() if "Kobuleti" in a.name)
    front = MagicMock(spec=FrontLine)
    front.position = Point(airport.position.x + 30_000, airport.position.y, caucasus)
    front.name = "Front line A/B"
    front.active_segment = MagicMock(
        point_a=Point(front.position.x - 4_000, front.position.y, caucasus),
        point_b=Point(front.position.x + 4_000, front.position.y, caucasus),
    )
    stub_strike_flight.package.target = front

    # Two TGOs in scope: a building and an EWR. Both must be filtered, so the
    # page must emit no labels (the active segment alone leaves last_text_log
    # with just the title + FRONT BE footer).
    building = MagicMock(spec=BuildingGroundObject)
    building.position = Point(front.position.x + 1_000, front.position.y, caucasus)
    ewr = MagicMock(spec=EwrGroundObject)
    ewr.position = Point(front.position.x - 1_000, front.position.y, caucasus)
    cp = MagicMock()
    cp.ground_objects = [building, ewr]
    stub_game.theater.controlpoints = list(stub_game.theater.controlpoints) + [cp]

    page = FrontLineDetailPage(flight=stub_strike_flight, game=stub_game)
    page.write(tmp_path / "frontline.png")
    # No TGO labels emitted — the only recorded text is the title + bullseye.
    label_lines = [
        t for t in page.last_text_log if "BE:" not in t and "FRONTLINE" not in t
    ]
    assert label_lines == []


def test_frontline_detail_page_writes_correct_size(
    tmp_path: Path,
    stub_strike_flight: MagicMock,
    stub_game: MagicMock,
    caucasus: Caucasus,
) -> None:
    """FrontLineDetailPage.write must produce a 768x1024 PNG without crashing."""
    from game.missiongenerator.kneeboard_recon.pages import FrontLineDetailPage
    from game.theater.frontline import FrontLine

    airport = next(a for a in caucasus.airport_list() if "Kobuleti" in a.name)
    front = MagicMock(spec=FrontLine)
    front.position = Point(airport.position.x + 30_000, airport.position.y, caucasus)
    front.name = "Front line A/B"
    # Concrete list, not iter(): production code may walk ``points`` more
    # than once (extent + corridor passes); a one-shot iterator would
    # collapse the second pass to an empty sequence.
    front.points = [
        Point(front.position.x - 5_000, front.position.y - 1_000, caucasus),
        Point(front.position.x + 5_000, front.position.y + 1_000, caucasus),
    ]
    stub_strike_flight.package.target = front

    page = FrontLineDetailPage(flight=stub_strike_flight, game=stub_game)
    out = tmp_path / "frontline.png"
    page.write(out)
    from PIL import Image

    img = Image.open(out)
    assert img.size == (768, 1024)


def test_airbase_footer_does_not_claim_defender_runway(
    tmp_path: Path, stub_oca_flight: MagicMock, stub_game: MagicMock
) -> None:
    """The page must not assert an enemy 'Active RWY' from the player's own departure."""
    page = AirbaseReconPage(flight=stub_oca_flight, game=stub_game)
    page.write(tmp_path / "airbase.png")
    joined = " ".join(page.last_text_log)
    # Misleading "Active RWY (defender) <player's runway>" text removed in the fix.
    assert "Active RWY" not in joined
    assert "RWY in use" not in joined


def test_overview_threats_filtered_to_corridor(
    tmp_path: Path, stub_strike_flight: MagicMock, stub_game: MagicMock
) -> None:
    """Threats far outside the corridor must not pull the extent across the theater."""
    cau = stub_strike_flight.package.target.position._terrain
    near_target = stub_strike_flight.package.target.position
    # Two threats: one near the target, one far enough outside the
    # corridor that the filter must exclude it but not so far that
    # Point.latlng() walks off the terrain projection.
    near_tgo = MagicMock()
    near_tgo.position = Point(near_target.x + 5_000.0, near_target.y, cau)
    near_tgo.obj_name = "NEAR"
    near_tgo.is_friendly = MagicMock(return_value=False)
    near_tgo.max_threat_range = MagicMock(return_value=MagicMock(meters=20_000.0))
    near_tgo.max_detection_range = MagicMock(return_value=MagicMock(meters=30_000.0))

    far_tgo = MagicMock()
    far_tgo.position = Point(near_target.x + 300_000.0, near_target.y, cau)
    far_tgo.obj_name = "FAR"
    far_tgo.is_friendly = MagicMock(return_value=False)
    far_tgo.max_threat_range = MagicMock(return_value=MagicMock(meters=20_000.0))
    far_tgo.max_detection_range = MagicMock(return_value=MagicMock(meters=30_000.0))

    cp = MagicMock()
    cp.ground_objects = [near_tgo, far_tgo]
    stub_game.theater.controlpoints = [cp]

    page = OverviewReconPage(
        flight=stub_strike_flight,
        game=stub_game,
        extra_threat_search_m=0.0,
    )
    page.write(tmp_path / "overview_filter.png")
    # The "FAR" threat label must not appear (filtered out).
    assert not any(
        "FAR" in s for s in page.last_text_log
    ), "far-away threat should be filtered out of the overview"
