from types import SimpleNamespace
from typing import Any
from uuid import uuid4

import pytest
from dcs.mapping import Point
from fastapi import HTTPException

from game.server.leaflet import LeafletPoint
from game.server.tgos.models import TgoJs
from game.server.tgos.routes import (
    clear_tgo_destination,
    set_tgo_destination,
    tgo_destination_in_range,
)
from game.theater.controlpoint import OffMapSpawn, Player
from game.theater.presetlocation import PresetLocation
from game.theater.theatergroundobject import SamGroundObject, ShipGroundObject
from game.utils import Heading, nautical_miles


def _ship(blue: bool = True) -> ShipGroundObject:
    location = PresetLocation(
        name="loc", position=Point(0, 0, None), heading=Heading(0)  # type: ignore[arg-type]
    )
    player = Player.BLUE if blue else Player.RED
    cp = OffMapSpawn(
        name="cp",
        position=Point(0, 0, None),  # type: ignore[arg-type]
        theater=None,  # type: ignore[arg-type]
        starts_blue=player,
    )
    cp._coalition = SimpleNamespace(player=player)  # type: ignore[assignment]
    return ShipGroundObject(name="ship", location=location, control_point=cp)


def _game(
    tgo: Any, *, sea: bool = True, land_between: bool = False, landmap: bool = True
) -> Any:
    landmap_obj = (
        SimpleNamespace(land_inbetween=lambda a, b: land_between) if landmap else None
    )
    theater = SimpleNamespace(
        terrain=None,
        landmap=landmap_obj,
        is_in_sea=lambda p: sea,
    )
    db = SimpleNamespace(tgos=SimpleNamespace(get=lambda _id: tgo))
    return SimpleNamespace(theater=theater, db=db)


def _patch_latlng(monkeypatch: pytest.MonkeyPatch) -> None:
    # for_tgo calls tgo.position.latlng() which needs a real terrain; stub it out.
    from dcs.mapping import LatLng

    monkeypatch.setattr(
        "dcs.mapping.Point.latlng",
        lambda self: LatLng(self.x, self.y),
    )


def test_for_tgo_mobile_and_destination(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_latlng(monkeypatch)
    ship = _ship(blue=True)
    js = TgoJs.for_tgo(ship)
    assert js.mobile is True
    assert js.destination is None
    ship.target_position = Point(1000, 2000, None)  # type: ignore[arg-type]
    js2 = TgoJs.for_tgo(ship)
    assert js2.destination is not None


def test_for_tgo_red_ship_not_mobile(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_latlng(monkeypatch)
    ship = _ship(blue=False)
    ship.target_position = Point(1000, 2000, None)  # type: ignore[arg-type]
    js = TgoJs.for_tgo(ship)
    assert js.mobile is False
    # A red ship's queued destination must not leak to the client.
    assert js.destination is None


def test_for_tgo_non_ship_not_mobile(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_latlng(monkeypatch)
    location = PresetLocation(
        name="l", position=Point(0, 0, None), heading=Heading(0)  # type: ignore[arg-type]
    )
    player = Player.BLUE
    cp = OffMapSpawn(
        name="c", position=Point(0, 0, None), theater=None, starts_blue=player  # type: ignore[arg-type]
    )
    cp._coalition = SimpleNamespace(player=player)  # type: ignore[assignment]
    sam = SamGroundObject(name="sam", location=location, control_point=cp, task=None)
    assert TgoJs.for_tgo(sam).mobile is False


def _patch_point(monkeypatch: pytest.MonkeyPatch) -> None:
    # Routes build a DCS Point from lat/lng; with terrain=None, stub from_latlng
    # to return a fixed point so range/sea checks are exercised deterministically.
    monkeypatch.setattr(
        "game.server.tgos.routes.Point.from_latlng",
        staticmethod(lambda latlng, terrain: Point(latlng.lat, latlng.lng, None)),  # type: ignore[arg-type]
    )


def test_set_destination_rejects_non_ship(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_point(monkeypatch)
    location = PresetLocation(
        name="l", position=Point(0, 0, None), heading=Heading(0)  # type: ignore[arg-type]
    )
    player = Player.BLUE
    cp = OffMapSpawn(
        name="c", position=Point(0, 0, None), theater=None, starts_blue=player  # type: ignore[arg-type]
    )
    cp._coalition = SimpleNamespace(player=player)  # type: ignore[assignment]
    sam = SamGroundObject(name="sam", location=location, control_point=cp, task=None)
    with pytest.raises(HTTPException) as exc:
        set_tgo_destination(uuid4(), LeafletPoint(lat=10, lng=0), _game(sam))
    assert exc.value.status_code == 400


def test_set_destination_rejects_red(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_point(monkeypatch)
    ship = _ship(blue=False)
    with pytest.raises(HTTPException) as exc:
        set_tgo_destination(uuid4(), LeafletPoint(lat=10, lng=0), _game(ship))
    assert exc.value.status_code == 403


def test_set_destination_rejects_out_of_range(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_point(monkeypatch)
    ship = _ship(blue=True)
    far = nautical_miles(80).meters + 5000.0
    with pytest.raises(HTTPException) as exc:
        set_tgo_destination(uuid4(), LeafletPoint(lat=far, lng=0), _game(ship))
    assert exc.value.status_code == 400


def test_set_destination_rejects_land(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_point(monkeypatch)
    ship = _ship(blue=True)
    with pytest.raises(HTTPException) as exc:
        set_tgo_destination(
            uuid4(), LeafletPoint(lat=1000, lng=0), _game(ship, land_between=True)
        )
    assert exc.value.status_code == 400


def test_set_destination_accepts_open_water(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_point(monkeypatch)
    ship = _ship(blue=True)
    set_tgo_destination(uuid4(), LeafletPoint(lat=1000, lng=0), _game(ship))
    assert ship.target_position is not None
    # The stored point must match the requested destination (no lat/lng swap).
    assert ship.target_position.x == 1000
    assert ship.target_position.y == 0


def test_set_destination_rejects_not_in_sea(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_point(monkeypatch)
    ship = _ship(blue=True)
    with pytest.raises(HTTPException) as exc:
        set_tgo_destination(
            uuid4(), LeafletPoint(lat=1000, lng=0), _game(ship, sea=False)
        )
    assert exc.value.status_code == 400


def test_set_destination_allows_when_no_landmap(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Maps without a landmap can't answer is_in_sea (returns False for every
    # point); the sea/land check must be skipped so ships remain movable there,
    # matching carrier behavior.
    _patch_point(monkeypatch)
    ship = _ship(blue=True)
    set_tgo_destination(
        uuid4(), LeafletPoint(lat=1000, lng=0), _game(ship, sea=False, landmap=False)
    )
    assert ship.target_position is not None


def test_cancel_travel_rejects_red() -> None:
    ship = _ship(blue=False)
    with pytest.raises(HTTPException) as exc:
        clear_tgo_destination(uuid4(), _game(ship))
    assert exc.value.status_code == 403


def test_cancel_travel_clears_blue_ship() -> None:
    ship = _ship(blue=True)
    ship.target_position = Point(1000, 2000, None)  # type: ignore[arg-type]
    clear_tgo_destination(uuid4(), _game(ship))
    assert ship.target_position is None


def test_destination_in_range_rejects_red(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_point(monkeypatch)
    ship = _ship(blue=False)
    with pytest.raises(HTTPException) as exc:
        tgo_destination_in_range(uuid4(), 10.0, 0.0, _game(ship))
    assert exc.value.status_code == 403
