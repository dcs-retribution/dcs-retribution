"""Fixed-wing CTLD paradrop air assault: planning gate + layout branches.

The Hercules-mod purge left Air Assault helicopter-only while the C-130J-30
yaml carried the "once we have proper support for paradrops" TODO. The Builder
now admits any troop transport (``cabin_size > 0``); a fixed-wing flight
preloads (no pickup zone), keeps no drop-off zone, and turns the CTLD
assault-area waypoint into a real AI run-in at drop height so the CTLD runtime
can release the stick over the target zone. Helicopter planning must be
byte-identical to before.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any, cast

import pytest
from dcs import Point
from dcs.terrain import Caucasus

import game.ato.flightplans.airassault as airassault
from game.ato.flightplans.airassault import Builder
from game.ato.flightplans.planningerror import PlanningError
from game.theater.controlpoint import ControlPointType
from game.theater.interfaces.CTLD import CTLD
from game.utils import Distance, feet, meters

TERRAIN = Caucasus()


def _point(x: float, y: float) -> Point:
    return Point(x, y, TERRAIN)


class _Departure(CTLD):
    """A departure control point that satisfies the CTLD pickup interface."""

    def __init__(self, cptype: ControlPointType, position: Point) -> None:
        self.cptype = cptype
        self.position = position
        self.ctld_zones = [(position, 100.0)]


class _FakeWaypointBuilder:
    """Duck-typed WaypointBuilder: returns attribute-bearing stub waypoints.

    ``assault_area`` mirrors the real ``_target_area`` defaults
    (``only_for_player=True``, altitude 0 RADIO) so the tests observe exactly
    what the fixed-wing branch changes.
    """

    def __init__(self, flight: Any) -> None:
        self.flight = flight
        self.get_cruise_altitude = feet(10000)
        self.pickup_zones_built: list[Any] = []

    @staticmethod
    def _wp(name: str, position: Point) -> SimpleNamespace:
        return SimpleNamespace(name=name, position=position)

    def takeoff(self, departure: Any) -> SimpleNamespace:
        return self._wp("TAKEOFF", departure.position)

    def pickup_zone(self, target: Any) -> SimpleNamespace:
        wp = SimpleNamespace(name="PICKUPZONE", position=target.position, alt=meters(0))
        self.pickup_zones_built.append(wp)
        return wp

    def nav_path(
        self, a: Point, b: Point, altitude: Distance, altitude_is_agl: bool
    ) -> list[SimpleNamespace]:
        return []

    def ingress(self, wp_type: Any, position: Point, target: Any) -> SimpleNamespace:
        return self._wp("INGRESS", position)

    def assault_area(self, target: Any) -> SimpleNamespace:
        return SimpleNamespace(
            name=f"ASSAULT {target.name}",
            position=target.position,
            alt=meters(0),
            only_for_player=True,
        )

    def dropoff_zone(self, target: Any) -> SimpleNamespace:
        return SimpleNamespace(
            name="DROPOFFZONE", position=target.position, alt=meters(0)
        )

    def land(self, cp: Any) -> SimpleNamespace:
        return self._wp("LAND", cp.position)

    def divert(self, divert: Any) -> None:
        return None

    def bullseye(self) -> SimpleNamespace:
        return self._wp("BULLSEYE", _point(0, 0))

    def join(self, position: Point) -> SimpleNamespace:
        return self._wp("JOIN", position)

    def split(self, position: Point) -> SimpleNamespace:
        return self._wp("SPLIT", position)


def _flight(is_helo: bool, cabin_size: int, is_hercules: bool = False) -> Any:
    departure = _Departure(ControlPointType.AIRBASE, _point(0, 0))
    target = SimpleNamespace(name="Enemy FOB", position=_point(80_000, 0))
    package = SimpleNamespace(
        target=target,
        waypoints=SimpleNamespace(
            ingress=_point(60_000, 5_000), initial=_point(50_000, 10_000)
        ),
    )
    theater = SimpleNamespace(nearest_land_pos=lambda p: p)
    settings = SimpleNamespace()
    return SimpleNamespace(
        is_helo=is_helo,
        is_hercules=is_hercules,
        unit_type=SimpleNamespace(cabin_size=cabin_size),
        departure=departure,
        arrival=SimpleNamespace(position=_point(0, 0)),
        divert=None,
        package=package,
        coalition=SimpleNamespace(
            game=SimpleNamespace(theater=theater, settings=settings)
        ),
    )


def _builder(flight: Any, monkeypatch: pytest.MonkeyPatch) -> Builder:
    monkeypatch.setattr(airassault, "WaypointBuilder", _FakeWaypointBuilder)
    return Builder(cast(Any, flight))


def test_fixed_wing_transport_flies_the_paradrop_run(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    layout = _builder(_flight(is_helo=False, cabin_size=24), monkeypatch).layout()

    # Preloaded: no pickup zone, and no helo drop-off zone either.
    assert layout.pickup is None
    assert layout.drop_off is None
    # The assault area is a real AI run-in at drop height, not the helo-case
    # player-only CTLD marker: the AI must overfly the zone for the CTLD
    # runtime to release the stick.
    assert layout.targets[0].only_for_player is False
    assert layout.targets[0].alt == feet(1000)


def test_helo_layout_is_unchanged(monkeypatch: pytest.MonkeyPatch) -> None:
    layout = _builder(_flight(is_helo=True, cabin_size=10), monkeypatch).layout()

    # Ground-start helos still load at a pickup zone and land at a drop-off
    # zone; the assault area stays the player-only CTLD implementation detail.
    assert layout.pickup is not None
    assert layout.drop_off is not None
    assert layout.targets[0].only_for_player is True
    assert layout.targets[0].alt == meters(0)


def test_fixed_wing_without_troop_cabin_is_rejected(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    builder = _builder(_flight(is_helo=False, cabin_size=0), monkeypatch)
    with pytest.raises(PlanningError):
        builder.layout()


def test_hercules_keeps_its_layout_shape(monkeypatch: pytest.MonkeyPatch) -> None:
    # The Anubis Hercules flew fixed-wing assaults before this change; its
    # layout (preloaded, initial-point ingress, AI run-in at 1,000 ft) must
    # come out of the generic fixed-wing path unchanged.
    flight = _flight(is_helo=False, cabin_size=24, is_hercules=True)
    layout = _builder(flight, monkeypatch).layout()

    assert layout.pickup is None
    assert layout.drop_off is None
    # The Hercules-specific ingress point (package.waypoints.initial).
    assert layout.ingress.position == flight.package.waypoints.initial
    assert layout.targets[0].only_for_player is False
    assert layout.targets[0].alt == feet(1000)
