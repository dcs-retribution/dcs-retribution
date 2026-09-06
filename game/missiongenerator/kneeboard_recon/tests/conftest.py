"""Shared fixtures for kneeboard_recon page tests.

Centralising these here lets both ``test_pages.py`` (smoke tests) and
``test_pages_golden.py`` (visual regression) drive identical stub data.
"""

from __future__ import annotations

import datetime
from collections.abc import Iterator
from unittest.mock import MagicMock

import pytest
from dcs.mapping import Point
from dcs.terrain.caucasus.caucasus import Caucasus
from dcs.weather import Wind

from game.ato.flighttype import FlightType
from game.ato.flightwaypointtype import FlightWaypointType
from game.ato.starttype import StartType
from game.theater.controlpoint import ControlPoint
from game.theater.theatergroundobject import TheaterGroundObject
from game.utils import inches_hg


@pytest.fixture(scope="module")
def caucasus() -> Caucasus:
    return Caucasus()


@pytest.fixture(autouse=True)
def _offline_basemap(
    monkeypatch: pytest.MonkeyPatch, tmp_path_factory: pytest.TempPathFactory
) -> Iterator[None]:
    """Force the tile pipeline to bypass network in tests, and supply a
    tmp_path for ``tile_cache_dir`` so ``base_path()`` is not required.

    Patches the cache-dir helper imported into ``pages``, the
    ``render_tiles`` function imported into ``basemap``, and the OSM
    airport-imagery loader so every test exercises the legacy fallback
    path (which the recon page assertions were originally written
    against). Tests targeting OSM-derived behavior should patch
    ``_airport_imagery.load`` themselves to return a real record.
    """
    from game.missiongenerator.kneeboard_recon import basemap as _basemap
    from game.missiongenerator.kneeboard_recon import pages as _pages

    cache = tmp_path_factory.mktemp("tilecache")
    monkeypatch.setattr(_pages, "tile_cache_dir", lambda: cache)
    monkeypatch.setattr(_basemap, "render_tiles", lambda *a, **kw: None)
    monkeypatch.setattr(_pages._airport_imagery, "load", lambda terrain_name: None)
    yield


@pytest.fixture
def stub_weather() -> MagicMock:
    m = MagicMock()
    m.atmospheric = MagicMock()
    m.atmospheric.qnh = inches_hg(29.92)
    m.atmospheric.temperature_celsius = 14
    m.wind = MagicMock()
    m.wind.at_0m = Wind(130, 12)
    m.wind.at_2000m = Wind(145, 22)
    m.wind.at_8000m = Wind(160, 45)
    m.clouds = None
    m.fog = None
    return m


@pytest.fixture
def stub_flight(caucasus: Caucasus) -> MagicMock:
    """Minimal FlightData-shaped stub for a 4-ship at Kobuleti."""
    f = MagicMock()
    f.callsign = "ENFIELD 1-1"
    f.flight_type = MagicMock()
    f.flight_type.value = "Strike"
    f.start_type = StartType.COLD
    f.custom_name = None
    # Departure airport (use Kobuleti from pydcs)
    airport = next(a for a in caucasus.airport_list() if "Kobuleti" in a.name)
    f.departure = MagicMock()
    f.departure.airfield_name = airport.name
    f.departure.runway_name = "13"
    f.departure.runway_heading = MagicMock()
    f.departure.runway_heading.degrees = 132
    f.departure.atc = None
    f.departure.tacan = None
    f.departure.tacan_callsign = None
    f.departure.dcs_airport = airport
    # 4 spawn units around the airport
    units = []
    for i in range(4):
        u = MagicMock()
        u.position = Point(
            airport.position.x + 30 * i, airport.position.y + 30 * i, caucasus
        )
        units.append(u)
    f.units = units
    f.aircraft_type = MagicMock()
    f.aircraft_type.utc_kneeboard = False
    return f


@pytest.fixture
def stub_game(caucasus: Caucasus) -> MagicMock:
    g = MagicMock()
    g.theater = MagicMock()
    g.theater.terrain = caucasus
    g.theater.timezone = datetime.timezone(datetime.timedelta(hours=3))  # Caucasus
    # _should_emit_departure and _dcs_airport_for_runway look up the pydcs
    # Airport via theater.controlpoints; provide a stand-in CP for Kobuleti
    # (the airport used by stub_flight) so departure dispatch works.
    kobuleti_ap = next(a for a in caucasus.airport_list() if "Kobuleti" in a.name)
    kobuleti_cp = MagicMock(spec=ControlPoint)
    kobuleti_cp.dcs_airport = kobuleti_ap
    kobuleti_cp.full_name = kobuleti_ap.name
    g.theater.controlpoints = [kobuleti_cp]
    g.conditions = MagicMock()
    g.conditions.start_time = datetime.datetime(2026, 5, 21, 6, 42)
    # Provide a real Point for bullseye so bearing/range formatting works
    airport = next(a for a in caucasus.airport_list() if "Kobuleti" in a.name)
    bullseye = MagicMock()
    bullseye.position = Point(airport.position.x, airport.position.y, caucasus)
    coalition = MagicMock()
    coalition.bullseye = bullseye
    g.coalition_for.return_value = coalition
    return g


@pytest.fixture
def stub_strike_flight(stub_flight: MagicMock, caucasus: Caucasus) -> MagicMock:
    """Extend stub_flight with a strike-type TGO target so OverviewReconPage can render.

    Anchored to Anapa-Vityazevo by name rather than ``next(airport_list())``
    so MGRS-zone assertions stay stable across pydcs reorderings of the
    airport list. The TGO sits ~30 km NE of Anapa, which keeps it inside
    MGRS GZD 37T.
    """
    stub_flight.flight_type = FlightType.STRIKE
    tgo = MagicMock(spec=TheaterGroundObject)
    anchor_airport = next(a for a in caucasus.airport_list() if "Anapa" in a.name)
    tgo.position = Point(
        anchor_airport.position.x + 30_000,
        anchor_airport.position.y + 5_000,
        caucasus,
    )
    unit_a = MagicMock()
    unit_a.position = Point(tgo.position.x + 20, tgo.position.y + 20, caucasus)
    unit_a.alive = True
    unit_a.type = MagicMock()
    unit_a.type.length = 30
    unit_a.type.width = 15
    tgo.strike_targets = [unit_a]
    tgo.max_threat_range = MagicMock(return_value=MagicMock(meters=0))
    tgo.max_detection_range = MagicMock(return_value=MagicMock(meters=0))
    stub_flight.package = MagicMock()
    stub_flight.package.target = tgo
    stub_flight.waypoints = [
        MagicMock(
            position=Point(
                stub_flight.units[0].position.x + 1000,
                stub_flight.units[0].position.y,
                caucasus,
            ),
            waypoint_type=FlightWaypointType.INGRESS_STRIKE,
        ),
        MagicMock(
            position=tgo.position,
            waypoint_type=FlightWaypointType.TARGET_POINT,
        ),
    ]
    return stub_flight


@pytest.fixture
def stub_oca_flight(stub_flight: MagicMock, caucasus: Caucasus) -> MagicMock:
    # Target is a ControlPoint (here we just put a MagicMock with the
    # attributes the page consumes — full ControlPoint construction is
    # expensive and not under test).
    airport = next(a for a in caucasus.airport_list() if "Senaki" in a.name)
    cp = MagicMock(spec=ControlPoint)
    cp.position = airport.position
    cp.name = airport.name
    cp.dcs_airport = airport
    cp.is_friendly = MagicMock(return_value=False)
    stub_flight.package = MagicMock()
    stub_flight.package.target = cp
    stub_flight.flight_type = FlightType.OCA_AIRCRAFT
    return stub_flight
