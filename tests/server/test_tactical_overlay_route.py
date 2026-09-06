from types import SimpleNamespace

from dcs import Point
from dcs.terrain import Caucasus

from game.ato.flightplans.tacticaloverlay import (
    ReachShape,
    TacticalOverlay,
    TacticalOverlayDisplay,
    TacticalTarget,
    reach_circle,
)
from game.ato.flightplans.uizonedisplay import UiZone, UiZoneDisplay
from game.server.flights.models import TacticalOverlayJs
from game.utils import nautical_miles


class _Theater:
    terrain = Caucasus()


_GAME = SimpleNamespace(theater=_Theater())


def test_overlay_js_from_overlay() -> None:
    target = Point(1000.0, 2000.0, Caucasus())
    overlay = TacticalOverlay(
        reach=[
            ReachShape(
                geometry=reach_circle(Point(0, 0, Caucasus()), nautical_miles(5)),
                filled=True,
            )
        ],
        actual_path=[Point(0, 0, Caucasus()), Point(100, 0, Caucasus())],
        targets=[TacticalTarget(position=target)],
    )
    js = TacticalOverlayJs.from_overlay(overlay, _Theater())  # type: ignore[arg-type]
    assert js.reach[0].filled is True
    assert len(js.reach[0].polygon) >= 1
    assert js.actual_path is not None and len(js.actual_path) == 2
    assert len(js.targets) == 1


def test_overlay_js_from_ui_zone_is_outline() -> None:
    zone = UiZone([Point(0, 0, Caucasus())], nautical_miles(10))
    js = TacticalOverlayJs.from_ui_zone(zone, _Theater())  # type: ignore[arg-type]
    assert len(js.reach) == 1 and js.reach[0].filled is False
    assert js.actual_path is None and js.targets == []


def test_empty_overlay_js() -> None:
    js = TacticalOverlayJs.from_overlay(TacticalOverlay(), _Theater())  # type: ignore[arg-type]
    assert js.reach == [] and js.actual_path is None and js.targets == []


# ---- for_flight dispatch ----


class _OverlayAndBridgePlan(TacticalOverlayDisplay, UiZoneDisplay):
    """A plan that exposes both a bespoke overlay and a legacy ui_zone."""

    def tactical_overlay(self) -> TacticalOverlay:
        return TacticalOverlay(
            reach=[
                ReachShape(
                    geometry=reach_circle(Point(0, 0, Caucasus()), nautical_miles(5)),
                    filled=True,
                )
            ],
            targets=[TacticalTarget(position=Point(1000, 2000, Caucasus()))],
        )

    def ui_zone(self) -> UiZone:
        return UiZone([Point(0, 0, Caucasus())], nautical_miles(10))


class _BarePlan:
    """Neither a TacticalOverlayDisplay nor a UiZoneDisplay."""


def _flight(client_count: int, plan: object) -> SimpleNamespace:
    return SimpleNamespace(client_count=client_count, flight_plan=plan)


def test_for_flight_ai_uses_bespoke_overlay() -> None:
    js = TacticalOverlayJs.for_flight(_flight(0, _OverlayAndBridgePlan()), _GAME)  # type: ignore[arg-type]
    assert any(r.filled for r in js.reach)
    assert len(js.targets) == 1


def test_for_flight_player_falls_back_to_ui_zone() -> None:
    # client_count > 0 -> player flight keeps the legacy outline, not the overlay.
    js = TacticalOverlayJs.for_flight(_flight(1, _OverlayAndBridgePlan()), _GAME)  # type: ignore[arg-type]
    assert len(js.reach) == 1 and js.reach[0].filled is False
    assert js.targets == []


def test_for_flight_no_display_is_empty() -> None:
    js = TacticalOverlayJs.for_flight(_flight(0, _BarePlan()), _GAME)  # type: ignore[arg-type]
    assert js.reach == [] and js.actual_path is None and js.targets == []
