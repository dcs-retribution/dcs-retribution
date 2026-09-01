from datetime import datetime
from types import SimpleNamespace
from typing import Any, cast
from uuid import uuid4

import pytest
from dcs.mapping import Point
from fastapi import HTTPException

from game.missiongenerator.motorpoolpopulator import MotorpoolPopulator, select_capped
from game.server.leaflet import LeafletPoint
from game.server.tgos.models import TgoJs
from game.server.tgos.routes import (
    clear_tgo_destination,
    set_tgo_destination,
    tgo_destination_in_range,
)
from game.sim import GameUpdateEvents
from game.theater.base import Base
from game.theater.controlpoint import ControlPoint, OffMapSpawn, Player
from game.theater.presetlocation import PresetLocation
from game.transfers import PendingTransfers, TransferOrder
from game.theater.theatergroundobject import (
    MotorpoolGroundObject,
    SamGroundObject,
    ShipGroundObject,
)
from game.dcs.groundunittype import GroundUnitType
from game.utils import Heading, nautical_miles
from dcs.vehicles import Armor


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


def _populated_motorpools(
    reserve: dict[GroundUnitType, int], cap: int, count: int = 1
) -> tuple[list[MotorpoolGroundObject], Any]:
    coalition = SimpleNamespace(transfers=[])
    armor = dict(reserve)
    cp = SimpleNamespace(
        name="factory",
        captured=Player.BLUE,
        connected_points=[],
        base=SimpleNamespace(
            armor=armor,
            total_armor=sum(armor.values()),
            total_units_of_type=lambda unit_type: armor.get(unit_type, 0),
        ),
        ground_unit_orders=SimpleNamespace(
            units={}, pending_orders=lambda _unit_type: 0
        ),
        coalition=coalition,
    )
    motorpools = [
        MotorpoolGroundObject(
            f"pool-{index}",
            PresetLocation(
                name=f"motorpool-{index}",
                position=Point(index * 100, 0, None),  # type: ignore[arg-type]
                heading=Heading(0),
            ),
            cp,  # type: ignore[arg-type]
            None,
        )
        for index in range(count)
    ]
    cp.ground_objects = motorpools
    cp.connected_objectives = motorpools
    next_ids = {"unit": 2227, "group": 0}

    def next_unit_id() -> int:
        next_ids["unit"] += 1
        return next_ids["unit"]

    def next_group_id() -> int:
        next_ids["group"] += 1
        return next_ids["group"]

    game = SimpleNamespace(
        theater=SimpleNamespace(controlpoints=[cp]),
        settings=SimpleNamespace(motorpool_enabled=True, motorpool_spawn_cap=cap),
        next_unit_id=next_unit_id,
        next_group_id=next_group_id,
        coalitions=[coalition],
    )
    coalition.game = game
    MotorpoolPopulator(cast(Any, game)).populate()
    return motorpools, cp


def test_motorpool_tgo_reserve_units_match_popup_display_names(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _patch_latlng(monkeypatch)
    abrams = next(GroundUnitType.for_dcs_type(Armor.M_1_Abrams))
    motorpools, _ = _populated_motorpools({abrams: 3}, cap=3)
    tgo = motorpools[0]

    assert TgoJs.for_tgo(tgo).reserve_units == [unit.display_name for unit in tgo.units]
    assert TgoJs.for_tgo(tgo).reserve_units[0].startswith("2228 |")


def test_initial_tgo_serialization_reconciles_new_motorpool_reserve(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Initial /game and /tgos payloads populate caches before reading them."""
    _patch_latlng(monkeypatch)
    abrams = next(GroundUnitType.for_dcs_type(Armor.M_1_Abrams))
    motorpools, cp = _populated_motorpools({abrams: 3}, cap=3)
    for tgo in motorpools:
        tgo.groups = []
        tgo.motorpool_unit_types = {}
        tgo.motorpool_projection_keys = {}

    payloads = TgoJs.all_in_game(cp.coalition.game)

    assert [len(payload.reserve_units) for payload in payloads] == [3]
    assert [unit.display_name for unit in motorpools[0].units] == payloads[
        0
    ].reserve_units


def test_motorpool_tgo_expected_inventory_includes_pending_orders(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _patch_latlng(monkeypatch)
    abrams = next(GroundUnitType.for_dcs_type(Armor.M_1_Abrams))
    bradley = next(GroundUnitType.for_dcs_type(Armor.M_2_Bradley))
    motorpools, cp = _populated_motorpools({abrams: 3, bradley: 1}, cap=3)
    cp.ground_unit_orders = SimpleNamespace(
        units={abrams: 2, bradley: -1},
        pending_orders=lambda unit_type: 2 if unit_type == abrams else -1,
    )

    expected = TgoJs.for_tgo(motorpools[0]).expected_inventory

    assert [entry.dict() for entry in expected] == [
        {
            "unit_type": abrams.variant_id,
            "display_name": abrams.display_name,
            "count": 5,
        },
    ]


def test_event_serialization_reconciles_motorpool_payload(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from game.server.eventstream.models import GameUpdateEventsJs

    _patch_latlng(monkeypatch)
    abrams = next(GroundUnitType.for_dcs_type(Armor.M_1_Abrams))
    motorpools, cp = _populated_motorpools({abrams: 2}, cap=3)
    tgo = motorpools[0]
    game = cp.coalition.game
    original_ids = [unit.id for unit in tgo.units]
    cp.base.armor[abrams] = 3
    cp.base.total_armor = 3
    events = GameUpdateEvents().update_motorpools_at(cp)
    monkeypatch.setattr(
        "game.server.eventstream.models.UnculledZoneJs.from_game", lambda _game: []
    )

    payload = GameUpdateEventsJs.from_events(events, game)

    assert len(payload.updated_tgos) == 1
    assert len(payload.updated_tgos[0].reserve_units) == 3
    assert [unit.id for unit in list(tgo.units)[:2]] == original_ids


def test_event_serialization_sorts_updated_tgos_by_stable_id(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Updated TGO payload order is deterministic despite set iteration order."""
    from game.server.eventstream.models import GameUpdateEventsJs

    class StubTgo:
        def __init__(self, name: str) -> None:
            self.id = uuid4()
            self.name = name

        __hash__ = object.__hash__

    first = StubTgo("first")
    second = StubTgo("second")
    tgos = {first, second}
    expected = sorted(tgos, key=lambda tgo: tgo.id)

    def serialize(tgo: StubTgo) -> TgoJs:
        return TgoJs(
            id=tgo.id,
            name=tgo.name,
            control_point_name="cp",
            category="category",
            blue=True,
            position=LeafletPoint(lat=0, lng=0),
            units=[],
            reserve_units=[],
            expected_inventory=[],
            unrendered_reserve=[],
            in_transit_units=[],
            threat_ranges=[],
            detection_ranges=[],
            dead=False,
            sidc="",
            task=None,
            mobile=False,
            destination=None,
        )

    monkeypatch.setattr("game.server.eventstream.models.TgoJs.for_tgo", serialize)
    monkeypatch.setattr(
        "game.server.eventstream.models.UnculledZoneJs.from_game", lambda _game: []
    )

    payload = GameUpdateEventsJs.from_events(
        GameUpdateEvents(updated_tgos=cast(Any, tgos)), cast(Any, SimpleNamespace())
    )

    assert [tgo.name for tgo in payload.updated_tgos] == [tgo.name for tgo in expected]


def test_same_cp_motorpool_payloads_are_disjoint(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _patch_latlng(monkeypatch)
    abrams = next(GroundUnitType.for_dcs_type(Armor.M_1_Abrams))
    motorpools, _ = _populated_motorpools({abrams: 6}, cap=6, count=2)

    payloads = [TgoJs.for_tgo(tgo).reserve_units for tgo in motorpools]

    assert payloads == [[unit.display_name for unit in tgo.units] for tgo in motorpools]
    assert set(payloads[0]).isdisjoint(payloads[1])


def test_motorpool_aggregate_inventory_uses_primary_marker_once(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _patch_latlng(monkeypatch)
    abrams = next(GroundUnitType.for_dcs_type(Armor.M_1_Abrams))
    bradley = next(GroundUnitType.for_dcs_type(Armor.M_2_Bradley))
    reserve = {bradley: 4, abrams: 5}
    cap = 4
    motorpools, cp = _populated_motorpools(reserve, cap=cap, count=2)
    destination = SimpleNamespace(name="destination")
    original_origin = SimpleNamespace(name="original-origin")
    cp.coalition.transfers = [
        SimpleNamespace(
            origin=cp,
            position=destination,
            destination=destination,
            units={bradley: 2, abrams: 1},
        ),
        SimpleNamespace(
            origin=cp,
            position=destination,
            destination=destination,
            units={abrams: 2},
        ),
        SimpleNamespace(
            origin=original_origin,
            position=cp,
            destination=destination,
            units={bradley: 7},
        ),
    ]
    selected = select_capped(reserve, cap)
    expected_unrendered = [
        {
            "unit_type": unit_type.variant_id,
            "display_name": unit_type.display_name,
            "count": count - selected.get(unit_type, 0),
        }
        for unit_type, count in sorted(
            reserve.items(), key=lambda item: item[0].variant_id
        )
        if count - selected.get(unit_type, 0) > 0
    ]
    expected_transit = [
        {
            "unit_type": unit_type.variant_id,
            "display_name": unit_type.display_name,
            "count": count,
        }
        for unit_type, count in sorted(
            ((abrams, 3), (bradley, 2)), key=lambda item: item[0].variant_id
        )
    ]

    first, second = (TgoJs.for_tgo(tgo) for tgo in motorpools)

    assert [entry.dict() for entry in first.unrendered_reserve] == expected_unrendered
    assert [entry.dict() for entry in first.in_transit_units] == expected_transit
    assert second.unrendered_reserve == []
    assert second.in_transit_units == []


def test_motorpool_in_transit_units_survive_origin_capture(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Queued transfers remain visible after their origin changes coalition."""
    _patch_latlng(monkeypatch)
    abrams = next(GroundUnitType.for_dcs_type(Armor.M_1_Abrams))
    motorpools, origin = _populated_motorpools({abrams: 2}, cap=2)
    game = origin.coalition.game

    blue_transfers = PendingTransfers.__new__(PendingTransfers)
    blue_transfers.game = game
    blue_transfers.player = Player.BLUE
    blue_transfers.pending_transfers = []
    cast(Any, blue_transfers).arrange_transport = lambda _transfer, _now, _events: None
    red_transfers = PendingTransfers.__new__(PendingTransfers)
    red_transfers.game = game
    red_transfers.player = Player.RED
    red_transfers.pending_transfers = []
    cast(Any, red_transfers).arrange_transport = lambda _transfer, _now, _events: None
    blue_coalition = SimpleNamespace(
        game=game, player=Player.BLUE, transfers=blue_transfers
    )
    red_coalition = SimpleNamespace(
        game=game, player=Player.RED, transfers=red_transfers
    )
    game.coalitions = [blue_coalition, red_coalition]
    origin.coalition = blue_coalition
    destination = SimpleNamespace(name="destination")
    transfer = TransferOrder(
        origin, cast(Any, destination), {abrams: 1}, player=Player.BLUE
    )
    origin.base.commit_losses = lambda _units: None
    blue_transfers.new_transfer(transfer, datetime.now())

    origin.captured = Player.RED
    origin.coalition = red_coalition

    transit = TgoJs.for_tgo(motorpools[0]).in_transit_units
    assert [(entry.unit_type, entry.count) for entry in transit] == [
        (abrams.variant_id, 1)
    ]


def test_new_transfer_emits_motorpool_tgo_update(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from datetime import datetime

    from game.transfers import PendingTransfers, TransferOrder

    unit_type = next(GroundUnitType.for_dcs_type(Armor.M_1_Abrams))
    cp = SimpleNamespace(
        captured=Player.BLUE,
        base=Base(),
        ground_objects=[],
        coalition=SimpleNamespace(transfers=[]),
    )
    location = PresetLocation(
        name="motorpool",
        position=Point(0, 0, None),  # type: ignore[arg-type]
        heading=Heading(0),
    )
    tgo = MotorpoolGroundObject("pool", location, cp, None)  # type: ignore[arg-type]
    cp.ground_objects = [tgo]
    destination = SimpleNamespace()
    transfer = TransferOrder(
        cast("ControlPoint", cp),
        cast("ControlPoint", destination),
        {unit_type: 1},
        player=Player.BLUE,
    )
    pending = PendingTransfers.__new__(PendingTransfers)
    pending.pending_transfers = []
    pending.player = Player.BLUE
    cast(Any, pending).arrange_transport = lambda _transfer, _now, _events: None
    events = GameUpdateEvents()

    pending.new_transfer(transfer, datetime.now(), events)

    assert events.updated_tgos == {tgo}


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
