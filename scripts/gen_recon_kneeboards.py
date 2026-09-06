"""Render one PNG per recon kneeboard page type using realistic stubs.

Two uses:

1. **Manual visual review.** Run after changes to any page class / drawing
   primitive to eyeball the result without spinning up a full campaign.

2. **Golden-image regression scaffolding.** The fixture builders here are
   stable enough that the produced PNGs can be diffed byte-for-byte (or via
   PIL pixel-equality) against checked-in golden copies once we decide to
   wire that into the test suite.

Usage:

    PYTHONPATH=. .venv/bin/python scripts/gen_recon_kneeboards.py
    PYTHONPATH=. .venv/bin/python scripts/gen_recon_kneeboards.py --out /tmp/kb
    PYTHONPATH=. .venv/bin/python scripts/gen_recon_kneeboards.py --pages overview detail

Outputs:

    01-airfield-departure.png   AirfieldDeparturePage at Kobuleti, COLD start
    02-overview-recon.png       OverviewReconPage with SA-6/SA-2/EWR threats
    03-detail-recon.png         DetailReconPage with 6 aimpoints (one DESTROYED)
    04-airbase-recon.png        AirbaseReconPage against Senaki (OCA Aircraft)
    05-frontline-detail.png     FrontLineDetailPage (CAS) with armor, SHORAD,
                                and a destroyed battery around the line of contact

The stubs mirror what game/missiongenerator/kneeboard_recon/tests/test_pages.py
constructs, expanded with a realistic strike target + 3-threat IADS for the
overview, so the renders exercise more of the rendering code than the
unit-test smoke checks do.
"""

from __future__ import annotations

import argparse
import datetime
import math
from pathlib import Path
from unittest.mock import MagicMock

from PIL import Image
from dcs.mapping import Point
from dcs.terrain.caucasus.caucasus import Caucasus
from dcs.weather import Wind

from game.ato.flighttype import FlightType
from game.ato.flightwaypointtype import FlightWaypointType
from game.ato.starttype import StartType
from game.missiongenerator.kneeboard_recon.pages import (
    AirbaseReconPage,
    AirfieldDeparturePage,
    DetailReconPage,
    FrontLineDetailPage,
    OverviewReconPage,
)
from game.theater.controlpoint import ControlPoint
from game.theater.frontline import FrontLine
from game.theater.theatergroundobject import TheaterGroundObject
from game.utils import inches_hg

DEFAULT_OUT_DIR = Path("/tmp/recon-kneeboards")
ALL_PAGES = ("departure", "overview", "detail", "airbase", "frontline")
# Surface wind shared between build_weather() and the runway selector below
# so they cannot silently disagree.
WIND_FROM_DEG = 130.0
WIND_SPEED_KT = 12


def build_weather() -> MagicMock:
    m = MagicMock()
    m.atmospheric = MagicMock()
    m.atmospheric.qnh = inches_hg(29.92)
    m.atmospheric.temperature_celsius = 14
    m.wind = MagicMock()
    m.wind.at_0m = Wind(int(WIND_FROM_DEG), WIND_SPEED_KT)
    m.wind.at_2000m = Wind(145, 22)
    m.wind.at_8000m = Wind(160, 45)
    m.clouds = MagicMock()
    m.clouds.density = "bkn"
    m.clouds.base_ft = 4500
    m.fog = None
    return m


def build_flight(caucasus: Caucasus, *, callsign: str = "ENFIELD 1-1") -> MagicMock:
    """A 4-ship Strike out of Kobuleti, COLD start, RWY 13."""
    airport = next(a for a in caucasus.airport_list() if "Kobuleti" in a.name)
    f = MagicMock()
    f.callsign = callsign
    f.flight_type = MagicMock()
    f.flight_type.value = "Strike"
    f.start_type = StartType.COLD
    f.custom_name = None
    f.squadron = MagicMock()
    f.squadron.name = "VFA-86 'Sidewinders'"

    f.departure = MagicMock()
    f.departure.airfield_name = airport.name
    # Pick the runway end whose takeoff heading has the largest headwind
    # component for the surface wind in build_weather(). Real campaigns get
    # this from RunwayAssigner; here we replicate the same physics so the
    # visual review matches what a pilot would actually be assigned.
    _candidates = []
    for _rwy in airport.runways:
        for _end in (_rwy.main, _rwy.opposite):
            # Headwind = wind_speed * cos(wind_from - takeoff_heading).
            # Maximise this. Positive cos = headwind; negative = tailwind.
            _headwind_factor = math.cos(math.radians(WIND_FROM_DEG - _end.heading))
            _candidates.append((_headwind_factor, _end))
    _best = max(_candidates, key=lambda c: c[0])[1]
    f.departure.runway_name = _best.name
    f.departure.runway_heading = MagicMock()
    f.departure.runway_heading.degrees = _best.heading
    f.departure.atc = MagicMock()
    f.departure.atc.mhz = 251.000
    f.departure.tacan = "16X"
    f.departure.tacan_callsign = "KBU"
    f.departure.dcs_airport = airport

    units = []
    for i in range(4):
        u = MagicMock()
        u.position = Point(
            airport.position.x + 40 * i,
            airport.position.y + 40 * i,
            caucasus,
        )
        units.append(u)
    f.units = units
    f.aircraft_type = MagicMock()
    f.aircraft_type.utc_kneeboard = False
    return f


def build_game(caucasus: Caucasus) -> MagicMock:
    g = MagicMock()
    g.theater = MagicMock()
    g.theater.terrain = caucasus
    g.theater.timezone = datetime.timezone(datetime.timedelta(hours=3))
    g.conditions = MagicMock()
    g.conditions.start_time = datetime.datetime(2026, 5, 21, 6, 42)
    g.conditions.weather = build_weather()

    airport = next(a for a in caucasus.airport_list() if "Kobuleti" in a.name)
    # AirfieldDeparturePage resolves the departure pydcs Airport by walking
    # theater.controlpoints and matching cp.dcs_airport.name against the
    # flight's departure airfield name (see pages._dcs_airport_for_runway),
    # not by reading flight.departure.dcs_airport. Seed a Kobuleti control
    # point so the departure page resolves a runway-backed airport instead of
    # tripping its "construct via generate_recon_pages" assertion.
    # add_overview_threats() replaces this list for the overview/detail
    # renders, which is fine: the departure page renders first.
    departure_cp = MagicMock(spec=ControlPoint)
    departure_cp.dcs_airport = airport
    departure_cp.name = airport.name
    departure_cp.position = airport.position
    g.theater.controlpoints = [departure_cp]

    bullseye = MagicMock()
    bullseye.position = Point(airport.position.x, airport.position.y, caucasus)
    coalition = MagicMock()
    coalition.bullseye = bullseye
    g.coalition_for.return_value = coalition
    return g


def build_strike_target(caucasus: Caucasus, *, near: Point) -> MagicMock:
    """A strike TGO ~50 km east of `near`, with 6 building units (one dead)."""
    tgo = MagicMock(spec=TheaterGroundObject)
    tgo.obj_name = "Sukhumi Fuel Depot"
    tgo.position = Point(near.x + 35_000, near.y + 28_000, caucasus)

    units = []
    for i in range(6):
        u = MagicMock()
        u.position = Point(
            tgo.position.x + (i % 3) * 90.0,
            tgo.position.y + (i // 3) * 90.0,
            caucasus,
        )
        u.alive = i != 4  # one already destroyed exercises the strikethrough path
        u.type = MagicMock()
        u.type.length = 30
        u.type.width = 18
        u.type.name = f"Bldg-{i + 1}"
        units.append(u)
    tgo.strike_targets = units
    tgo.units = units
    tgo.is_friendly = MagicMock(return_value=False)
    tgo.max_threat_range = MagicMock(return_value=MagicMock(meters=0))
    tgo.max_detection_range = MagicMock(return_value=MagicMock(meters=0))
    return tgo


def add_overview_threats(
    game: MagicMock, target_pos: Point, caucasus: Caucasus
) -> None:
    """Attach SA-6 + SA-2 + EWR around the target so overview page is busy."""
    sa6 = MagicMock()
    sa6.obj_name = "SA-6 Kub"
    sa6.position = Point(target_pos.x - 8_000, target_pos.y + 3_000, caucasus)
    sa6.is_friendly = MagicMock(return_value=False)
    sa6.max_threat_range = MagicMock(return_value=MagicMock(meters=24_000.0))
    sa6.max_detection_range = MagicMock(return_value=MagicMock(meters=70_000.0))

    sa2 = MagicMock()
    sa2.obj_name = "SA-2 Guideline"
    sa2.position = Point(target_pos.x + 12_000, target_pos.y - 6_000, caucasus)
    sa2.is_friendly = MagicMock(return_value=False)
    sa2.max_threat_range = MagicMock(return_value=MagicMock(meters=35_000.0))
    sa2.max_detection_range = MagicMock(return_value=MagicMock(meters=60_000.0))

    ewr = MagicMock()
    ewr.obj_name = "1L13 EWR"
    ewr.position = Point(target_pos.x - 2_000, target_pos.y - 18_000, caucasus)
    ewr.is_friendly = MagicMock(return_value=False)
    ewr.max_threat_range = MagicMock(return_value=MagicMock(meters=0))
    ewr.max_detection_range = MagicMock(return_value=MagicMock(meters=120_000.0))

    cp = MagicMock()
    cp.ground_objects = [sa6, sa2, ewr]
    game.theater.controlpoints = [cp]


def wire_strike_flight(game: MagicMock, flight: MagicMock, caucasus: Caucasus) -> None:
    """Mutate `flight` and `game` so they describe a Strike on a TGO target."""
    target = build_strike_target(caucasus, near=flight.departure.dcs_airport.position)
    flight.flight_type = FlightType.STRIKE
    flight.package = MagicMock()
    flight.package.target = target

    dep = flight.departure.dcs_airport.position
    ingress = Point(
        (dep.x + target.position.x) / 2,
        (dep.y + target.position.y) / 2,
        caucasus,
    )
    flight.waypoints = [
        MagicMock(
            position=Point(dep.x + 1500, dep.y + 1500, caucasus),
            waypoint_type=FlightWaypointType.TAKEOFF,
        ),
        MagicMock(position=ingress, waypoint_type=FlightWaypointType.INGRESS_STRIKE),
        MagicMock(
            position=target.position, waypoint_type=FlightWaypointType.TARGET_POINT
        ),
    ]
    add_overview_threats(game, target.position, caucasus)


def wire_oca_flight(flight: MagicMock, caucasus: Caucasus) -> None:
    """Mutate `flight` to be OCA Aircraft against Senaki."""
    airport = next(a for a in caucasus.airport_list() if "Senaki" in a.name)
    cp = MagicMock(spec=ControlPoint)
    cp.position = airport.position
    cp.name = airport.name
    cp.dcs_airport = airport
    cp.is_friendly = MagicMock(return_value=False)
    flight.flight_type = FlightType.OCA_AIRCRAFT
    flight.package = MagicMock()
    flight.package.target = cp


def _frontline_tgo(
    *,
    pos: Point,
    obj_name: str,
    unit_name: str,
    count: int,
    alive: bool,
    threat_m: float,
    det_m: float,
) -> MagicMock:
    """A frontline TGO exposing the ``.groups[].units[]`` shape that
    ``pages._greatest_alive_threat`` walks (``alive`` flag +
    ``unit_type.display_name``), plus the threat/detection ranges the page
    reads for ring sizing. A TGO whose units are all dead resolves to None and
    renders as a black destroyed marker.
    """
    tgo = MagicMock(spec=TheaterGroundObject)
    tgo.obj_name = obj_name
    tgo.position = pos
    tgo.is_friendly = MagicMock(return_value=False)
    tgo.max_threat_range = MagicMock(return_value=MagicMock(meters=threat_m))
    tgo.max_detection_range = MagicMock(return_value=MagicMock(meters=det_m))
    unit_type = MagicMock()
    unit_type.display_name = unit_name
    group = MagicMock()
    group.units = []
    for _ in range(count):
        u = MagicMock()
        u.alive = alive
        u.unit_type = unit_type
        group.units.append(u)
    tgo.groups = [group]
    return tgo


def wire_cas_flight(game: MagicMock, flight: MagicMock, caucasus: Caucasus) -> None:
    """Mutate `flight` and `game` to describe CAS against a front line.

    Self-contained (does not depend on wire_strike_flight) so
    ``--pages frontline`` renders standalone. The synthetic FrontLine carries a
    real ``active_segment`` so pages._frontline_bounds_points can derive the
    perpendicular line-of-contact (FrontLineConflictDescription.frontline_bounds
    raises on a mock front and falls back to the segment math), and a few enemy
    TGOs sit inside the ~20 nm scope to exercise the threat-ring, dead-marker,
    and label paths.
    """
    base = flight.departure.dcs_airport.position  # Kobuleti
    center = Point(base.x + 26_000, base.y + 20_000, caucasus)

    front = MagicMock(spec=FrontLine)
    front.name = "FLOT KUTAISI/SUKHUMI"
    front.position = center
    # Real Points so heading_between_point() / point_from_heading() work in the
    # bounds-points fallback; the line runs roughly NE/SW through the center.
    seg = MagicMock()
    seg.point_a = Point(center.x - 7_000, center.y - 4_000, caucasus)
    seg.point_b = Point(center.x + 7_000, center.y + 4_000, caucasus)
    front.active_segment = seg

    # max_frontline_width drives how far the orange bounds line extends.
    game.settings = MagicMock()
    game.settings.max_frontline_width = 80

    cp = MagicMock()
    cp.ground_objects = [
        _frontline_tgo(
            pos=Point(center.x + 2_500, center.y + 1_500, caucasus),
            obj_name="Forward Armor",
            unit_name="T-72B",
            count=4,
            alive=True,
            threat_m=0.0,
            det_m=0.0,
        ),
        _frontline_tgo(
            pos=Point(center.x - 4_000, center.y + 3_000, caucasus),
            obj_name="SHORAD Section",
            unit_name="SA-13 Strela-10",
            count=2,
            alive=True,
            threat_m=5_000.0,
            det_m=10_000.0,
        ),
        _frontline_tgo(
            pos=Point(center.x + 5_000, center.y - 3_500, caucasus),
            obj_name="Destroyed Battery",
            unit_name="2S6 Tunguska",
            count=3,
            alive=False,
            threat_m=0.0,
            det_m=0.0,
        ),
    ]
    game.theater.controlpoints = [cp]

    flight.flight_type = FlightType.CAS
    flight.package = MagicMock()
    flight.package.target = front


def render(out_dir: Path, pages: tuple[str, ...], *, dark: bool = False) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    caucasus = Caucasus()
    game = build_game(caucasus)
    flight = build_flight(caucasus)
    weather = game.conditions.weather
    written: list[Path] = []

    if "departure" in pages:
        path = out_dir / "01-airfield-departure.png"
        AirfieldDeparturePage(
            flight=flight,
            game=game,
            weather=weather,
            dark=dark,
        ).write(path)
        written.append(path)

    if "overview" in pages or "detail" in pages:
        wire_strike_flight(game, flight, caucasus)

        if "overview" in pages:
            path = out_dir / "02-overview-recon.png"
            OverviewReconPage(
                flight=flight,
                game=game,
                extra_threat_search_m=0.0,
                dark=dark,
            ).write(path)
            written.append(path)

        if "detail" in pages:
            path = out_dir / "03-detail-recon.png"
            DetailReconPage(flight=flight, game=game, dark=dark).write(path)
            written.append(path)

    if "airbase" in pages:
        # Retarget the same flight as OCA so the same `game` graph works.
        wire_oca_flight(flight, caucasus)
        path = out_dir / "04-airbase-recon.png"
        AirbaseReconPage(flight=flight, game=game, dark=dark).write(path)
        written.append(path)

    if "frontline" in pages:
        # Retarget as CAS against a front line. Rendered last because
        # wire_cas_flight rewrites game.theater.controlpoints and the flight
        # target; doing it here leaves the earlier pages untouched.
        wire_cas_flight(game, flight, caucasus)
        path = out_dir / "05-frontline-detail.png"
        FrontLineDetailPage(flight=flight, game=game, dark=dark).write(path)
        written.append(path)

    return written


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_OUT_DIR,
        help=f"output directory (default: {DEFAULT_OUT_DIR})",
    )
    parser.add_argument(
        "--pages",
        nargs="+",
        choices=ALL_PAGES,
        default=list(ALL_PAGES),
        help="which page types to render (default: all)",
    )
    parser.add_argument(
        "--dark",
        action="store_true",
        help="render the dark-mode palette instead of the default light one.",
    )
    args = parser.parse_args()

    paths = render(args.out, tuple(args.pages), dark=args.dark)
    print(f"Wrote {len(paths)} page(s) to {args.out}/")
    for path in paths:
        # One unreadable PNG (truncated render, missing file) must not
        # eat the summary for every later page in the list.
        try:
            with Image.open(path) as im:
                print(f"  {path.name}  {im.size[0]}x{im.size[1]}")
        except Exception as exc:
            print(f"  {path.name}  (unreadable: {exc})")


if __name__ == "__main__":
    main()
