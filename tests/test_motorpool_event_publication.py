"""AC.8 acceptance tests for Task 6: one-shared-accumulator event publication.

Each inventory-mutation operation must:

1. Accept (or create and return) a single shared ``GameUpdateEvents``
   accumulator rather than publishing internally via ``EventStream``.
2. Add authored motorpool TGOs (via ``update_motorpools_at``) and supply-route
   updates to that one accumulator for deduplication.
3. Never call ``EventStream.put_nowait`` or ``EventStream.event_context``
   directly.

The mutation methods mutate state and populate the caller's accumulator; the
*outer* operation owns the single publication.  These tests drive the mutation
methods directly with a fresh accumulator and assert the resulting event set,
and that no publication reached ``EventStream``.
"""

from __future__ import annotations

from datetime import datetime
from types import SimpleNamespace
from typing import Any, Iterator, cast
from unittest.mock import MagicMock

from dcs.vehicles import Armor

from game.dcs.groundunittype import GroundUnitType
from game.sim import GameUpdateEvents
from game.theater.base import Base
from game.theater.player import Player
from game.transfers import (
    AirliftPlanner,
    PendingTransfers,
    TransferOrder,
)
from game.unitmap import FrontLineUnit
from dcs import Point
from game.theater.presetlocation import PresetLocation
from game.theater.theatergroundobject import MotorpoolGroundObject
from game.utils import Heading


class HashableCP(SimpleNamespace):
    """A hashable SimpleNamespace so it can be used as a dict key (ConvoyMap)."""

    def __hash__(self) -> int:  # type: ignore[override]
        return id(self)


def _unit_type() -> GroundUnitType:
    return next(GroundUnitType.for_dcs_type(Armor.M_1_Abrams))


def _motorpool_tgo(cp: Any, name: str = "pool") -> MotorpoolGroundObject:
    location = PresetLocation(
        name=name,
        position=Point(0, 0, None),  # type: ignore[arg-type]
        heading=Heading(0),
    )
    return MotorpoolGroundObject(name, location, cast(Any, cp), None)


def _cp(
    name: str = "alpha",
    captured: Player = Player.BLUE,
    with_motorpool: bool = True,
    with_orders: bool = False,
) -> Any:
    ground_objects: list[Any] = []
    cp = HashableCP(
        name=name,
        captured=captured,
        base=Base(),
        ground_objects=ground_objects,
        position=Point(0, 0, None),  # type: ignore[arg-type]
        coalition=SimpleNamespace(transfers=[]),
    )
    if with_motorpool:
        tgo = _motorpool_tgo(cp)
        ground_objects.append(tgo)
    if with_orders:
        from game.groundunitorders import GroundUnitOrders

        cp.ground_unit_orders = GroundUnitOrders(cast(Any, cp))
    return cp


def _make_pending(
    player: Player = Player.BLUE,
    stub_arrange: bool = True,
) -> PendingTransfers:
    network = SimpleNamespace(
        shortest_path_between=lambda _origin, destination: [destination],
    )
    game = SimpleNamespace(
        db=SimpleNamespace(flights=[]),
        transit_network_for=lambda _p: network,
        ato_for=lambda _p: SimpleNamespace(
            add_package=lambda _pkg: None,
            remove_package=lambda _pkg: None,
        ),
    )
    pending = PendingTransfers(cast(Any, game), player)
    if stub_arrange:
        cast(Any, pending).arrange_transport = lambda _t, _n, _e: None
    return pending


def _patch_event_stream(monkeypatch: pytest.MonkeyPatch) -> list[Any]:
    """Patch ``EventStream.put_nowait`` to record calls instead of queueing.

    Returns a list that will be appended to on each publication attempt.
    """
    calls: list[Any] = []

    def _put_nowait(cls: Any, events: Any) -> None:
        calls.append(events)

    monkeypatch.setattr(
        "game.server.eventstream.eventstream.EventStream.put_nowait",
        classmethod(_put_nowait),
    )
    return calls


import pytest  # noqa: E402

# ---------------------------------------------------------------------------
# Transfer create / cancel
# ---------------------------------------------------------------------------


def test_transfer_create_emits_one_final_motorpool_update(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """new_transfer populates the caller accumulator with motorpool TGOs once."""
    pubs = _patch_event_stream(monkeypatch)
    cp = _cp("alpha")
    destination = _cp("bravo")
    unit_type = _unit_type()
    transfer = TransferOrder(
        cast(Any, cp), cast(Any, destination), {unit_type: 1}, player=Player.BLUE
    )
    pending = _make_pending(Player.BLUE)
    events = GameUpdateEvents()

    pending.new_transfer(transfer, datetime.now(), events)

    # The motorpool at the origin must be in the event set exactly once.
    assert cp.ground_objects[0] in events.updated_tgos
    assert events.updated_supply_routes
    # No internal publication.
    assert pubs == []


def test_transfer_cancel_emits_one_final_motorpool_update(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """cancel_transfer populates the caller accumulator, does not publish."""
    pubs = _patch_event_stream(monkeypatch)
    cp = _cp("alpha")
    destination = _cp("bravo")
    unit_type = _unit_type()
    transfer = TransferOrder(
        cast(Any, cp), cast(Any, destination), {unit_type: 1}, player=Player.BLUE
    )
    pending = _make_pending(Player.BLUE)
    events = GameUpdateEvents()
    pending.new_transfer(transfer, datetime.now(), events)

    cancel_events = GameUpdateEvents()
    pending.cancel_transfer(transfer, cancel_events)

    assert cp.ground_objects[0] in cancel_events.updated_tgos
    assert cancel_events.updated_supply_routes
    assert pubs == []


def test_transfer_create_publishes_when_events_are_omitted(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Legacy direct new_transfer callers receive the generated event publication."""
    pubs = _patch_event_stream(monkeypatch)
    cp = _cp("alpha")
    destination = _cp("bravo")
    transfer = TransferOrder(
        cast(Any, cp), cast(Any, destination), {_unit_type(): 1}, player=Player.BLUE
    )

    _make_pending(Player.BLUE).new_transfer(transfer, datetime.now())

    assert len(pubs) == 1
    assert cp.ground_objects[0] in pubs[0].updated_tgos
    assert pubs[0].updated_supply_routes


def test_transfer_cancel_publishes_when_events_are_omitted(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Legacy direct cancel_transfer callers receive the generated event publication."""
    pubs = _patch_event_stream(monkeypatch)
    cp = _cp("alpha")
    destination = _cp("bravo")
    transfer = TransferOrder(
        cast(Any, cp), cast(Any, destination), {_unit_type(): 1}, player=Player.BLUE
    )
    pending = _make_pending(Player.BLUE)
    pending.new_transfer(transfer, datetime.now(), GameUpdateEvents())

    pending.cancel_transfer(transfer)

    assert len(pubs) == 1
    assert cp.ground_objects[0] in pubs[0].updated_tgos
    assert pubs[0].updated_supply_routes


# ---------------------------------------------------------------------------
# Transfer movement / completion / disband
# ---------------------------------------------------------------------------


def test_transfer_intermediate_move_emits_one_final_motorpool_update(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """perform_transfers snapshots origin/current/destination and publishes once."""
    pubs = _patch_event_stream(monkeypatch)
    origin = _cp("alpha")
    intermediate = _cp("bravo")
    destination = _cp("charlie")

    unit_type = _unit_type()
    transfer = TransferOrder(
        cast(Any, origin),
        cast(Any, destination),
        {unit_type: 1},
        player=Player.BLUE,
    )
    transfer.position = cast(Any, intermediate)

    # Simulate one in-transit hop without exercising transport-specific cleanup.
    def proceed() -> None:
        transfer.position = cast(Any, destination)

    transfer.proceed = proceed  # type: ignore[method-assign]
    pending = _make_pending(Player.BLUE)
    pending.pending_transfers = [transfer]
    # Stub network so is_completable does not fail during disband check.
    cast(Any, pending).network_for = lambda _cp: SimpleNamespace(
        has_path_between=lambda _a, _b: True
    )
    cast(Any, intermediate).is_friendly = lambda _p: True
    events = GameUpdateEvents()

    pending.perform_transfers(events)

    # The pre-hop and post-hop motorpool projections are refreshed. The original
    # origin is not mutated by this intermediate movement operation.
    assert events.updated_tgos == {
        intermediate.ground_objects[0],
        destination.ground_objects[0],
    }
    assert origin.ground_objects[0] not in events.updated_tgos
    assert events.updated_supply_routes
    assert pubs == []


def test_transfer_completion_emits_one_final_motorpool_update(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Completion/commissioning at the destination refreshes that motorpool once."""
    pubs = _patch_event_stream(monkeypatch)
    origin = _cp("alpha")
    destination = _cp("bravo")
    unit_type = _unit_type()
    transfer = TransferOrder(
        cast(Any, origin),
        cast(Any, destination),
        {unit_type: 1},
        player=Player.BLUE,
    )
    # Simulate arrival: position is the destination.
    transfer.position = cast(Any, destination)
    transfer.transport = None
    pending = _make_pending(Player.BLUE)
    pending.pending_transfers = [transfer]
    # Stub network so is_completable does not fail during disband check.
    cast(Any, pending).network_for = lambda _cp: SimpleNamespace(
        has_path_between=lambda _a, _b: True
    )
    cast(Any, destination).is_friendly = lambda _p: True
    events = GameUpdateEvents()

    pending.perform_transfers(events)

    assert destination.ground_objects[0] in events.updated_tgos
    assert pubs == []


def test_transfer_disband_escape_and_destruction_emit_one_final_motorpool_update(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Disband/escape/destruction refreshes the relevant motorpool, publishes once."""
    pubs = _patch_event_stream(monkeypatch)
    origin = _cp("alpha")
    destination = _cp("bravo")
    unit_type = _unit_type()
    transfer = TransferOrder(
        cast(Any, origin),
        cast(Any, destination),
        {unit_type: 1},
        player=Player.BLUE,
    )
    # Uncompletable: position captured.
    transfer.position = cast(Any, origin)
    transfer.transport = None

    pending = _make_pending(Player.BLUE)
    pending.pending_transfers = [transfer]
    # Make is_completable return False so disband fires.
    cast(Any, pending).network_for = lambda _cp: SimpleNamespace(
        has_path_between=lambda _a, _b: True
    )
    cast(Any, origin).is_friendly = lambda _p: False
    transfer.find_escape_route = lambda: None  # type: ignore[method-assign]

    events = GameUpdateEvents()
    pending.perform_transfers(events)

    assert events.updated_supply_routes
    assert pubs == []


# ---------------------------------------------------------------------------
# Ground delivery / purchase / sale
# ---------------------------------------------------------------------------


def test_ground_delivery_emits_one_final_motorpool_update(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """GroundUnitOrders.create_transfer forwards the accumulator once."""
    pubs = _patch_event_stream(monkeypatch)
    from game.groundunitorders import GroundUnitOrders

    source = _cp("factory")
    dest = _cp("front")
    unit_type = _unit_type()
    coalition = SimpleNamespace(
        player=Player.BLUE,
        transfers=_make_pending(Player.BLUE),
        adjust_budget=lambda _amt: None,
    )
    orders = GroundUnitOrders(cast(Any, dest))
    events = GameUpdateEvents()

    orders.create_transfer(
        cast(Any, coalition), cast(Any, source), {unit_type: 1}, datetime.now(), events
    )

    assert source.ground_objects[0] in events.updated_tgos
    assert pubs == []


def test_ground_purchase_emits_one_final_motorpool_update(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Ground unit purchase publishes one final motorpool update."""
    pubs = _patch_event_stream(monkeypatch)
    from game.purchaseadapter import GroundUnitPurchaseAdapter

    cp = _cp("alpha", with_orders=True)
    coalition = SimpleNamespace(
        player=Player.BLUE,
        budget=10000,
        adjust_budget=lambda _amt: None,
    )
    game = SimpleNamespace(
        settings=SimpleNamespace(enable_enemy_buy_sell=False),
    )
    cp.has_ground_unit_source = lambda _g: True
    adapter = GroundUnitPurchaseAdapter(
        cast(Any, cp), cast(Any, coalition), cast(Any, game)
    )
    unit_type = _unit_type()
    adapter.buy(unit_type, 1)

    assert len(pubs) == 1
    assert cp.ground_objects[0] in pubs[0].updated_tgos
    assert cp.ground_unit_orders.pending_orders(unit_type) == 1


def test_ground_purchase_publishes_partial_mutation_before_later_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A failed later purchase still publishes its earlier pending-order mutation."""
    pubs = _patch_event_stream(monkeypatch)
    from game.purchaseadapter import GroundUnitPurchaseAdapter, TransactionError

    cp = _cp("alpha", with_orders=True)
    budget = 10000
    coalition: Any = SimpleNamespace(
        player=Player.BLUE,
        budget=budget,
    )

    def adjust_budget(amount: int) -> None:
        coalition.budget += amount

    coalition.adjust_budget = adjust_budget
    game = SimpleNamespace(
        settings=SimpleNamespace(enable_enemy_buy_sell=False),
    )
    sources = iter((True, False))
    cp.has_ground_unit_source = lambda _g: next(sources)
    adapter = GroundUnitPurchaseAdapter(
        cast(Any, cp), cast(Any, coalition), cast(Any, game)
    )
    unit_type = _unit_type()

    with pytest.raises(TransactionError):
        adapter.buy(unit_type, 2)

    assert cp.ground_unit_orders.pending_orders(unit_type) == 1
    assert coalition.budget == budget - unit_type.price
    assert len(pubs) == 1
    assert cp.ground_objects[0] in pubs[0].updated_tgos


def test_ground_sell_publishes_partial_cancellation_before_later_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A failed later sell still publishes its earlier cancellation mutation."""
    pubs = _patch_event_stream(monkeypatch)
    from game.purchaseadapter import GroundUnitPurchaseAdapter, TransactionError

    cp = _cp("alpha", with_orders=True)
    unit_type = _unit_type()
    cp.ground_unit_orders.order({unit_type: 1})
    budget = 10000
    coalition: Any = SimpleNamespace(
        player=Player.BLUE,
        budget=budget,
    )

    def adjust_budget(amount: int) -> None:
        coalition.budget += amount

    coalition.adjust_budget = adjust_budget
    game = SimpleNamespace(
        settings=SimpleNamespace(enable_enemy_buy_sell=False),
    )
    adapter = GroundUnitPurchaseAdapter(
        cast(Any, cp), cast(Any, coalition), cast(Any, game)
    )

    with pytest.raises(TransactionError):
        adapter.sell(unit_type, 2)

    assert cp.ground_unit_orders.pending_orders(unit_type) == 0
    assert coalition.budget == budget + unit_type.price
    assert len(pubs) == 1
    assert cp.ground_objects[0] in pubs[0].updated_tgos


def test_ground_purchase_validation_failure_does_not_publish(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A purchase rejected before mutation does not publish a stale update."""
    pubs = _patch_event_stream(monkeypatch)
    from game.purchaseadapter import GroundUnitPurchaseAdapter, TransactionError

    cp = _cp("alpha", with_orders=True)
    coalition = SimpleNamespace(
        player=Player.BLUE,
        budget=0,
        adjust_budget=lambda _amount: None,
    )
    game = SimpleNamespace(
        settings=SimpleNamespace(enable_enemy_buy_sell=False),
    )
    cp.has_ground_unit_source = lambda _g: True
    adapter = GroundUnitPurchaseAdapter(
        cast(Any, cp), cast(Any, coalition), cast(Any, game)
    )
    unit_type = _unit_type()

    with pytest.raises(TransactionError):
        adapter.buy(unit_type, 1)

    assert cp.ground_unit_orders.pending_orders(unit_type) == 0
    assert pubs == []

    adapter.buy(unit_type, 0)

    assert pubs == []


# ---------------------------------------------------------------------------
# Motorpool mission loss
# ---------------------------------------------------------------------------


def test_motorpool_loss_emits_one_final_motorpool_update(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """commit_motorpool_losses adds the affected motorpool TGO to the accumulator."""
    pubs = _patch_event_stream(monkeypatch)
    from game.debriefing import Debriefing
    from game.sim.missionresultsprocessor import MissionResultsProcessor

    cp = _cp("alpha")
    unit_type = _unit_type()
    cp.base.armor = {unit_type: 3}
    loss = FrontLineUnit(unit_type=unit_type, origin=cast(Any, cp))
    debriefing = cast(Debriefing, SimpleNamespace(motorpool_losses=[loss]))
    events = GameUpdateEvents()

    MissionResultsProcessor.commit_motorpool_losses(debriefing, events)

    assert cp.ground_objects[0] in events.updated_tgos
    assert pubs == []


# ---------------------------------------------------------------------------
# Airlift planning and cancellation
# ---------------------------------------------------------------------------


def test_airlift_planning_and_cancellation_emit_one_final_update(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """arrange_transport/create_package_for_airlift and cancel_transport forward
    the accumulator and never publish independently."""
    pubs = _patch_event_stream(monkeypatch)
    origin = _cp("alpha")
    destination = _cp("bravo")
    unit_type = _unit_type()
    transfer = TransferOrder(
        cast(Any, origin),
        cast(Any, destination),
        {unit_type: 1},
        player=Player.BLUE,
        request_airflift=True,
    )
    transfer.transport = None

    # Build a planner with create_airlift_flight stubbed so no real Flight is
    # constructed, but the package publication path is exercised.
    pending = _make_pending(Player.BLUE, stub_arrange=False)
    removed_packages: list[Any] = []
    cast(Any, pending.game).ato_for = lambda _player: SimpleNamespace(
        add_package=lambda _package: None,
        remove_package=removed_packages.append,
    )

    events = GameUpdateEvents()
    forwarded: list[tuple[datetime, GameUpdateEvents]] = []

    def create_package_for_airlift(
        _planner: Any, now: datetime, planner_events: GameUpdateEvents
    ) -> None:
        forwarded.append((now, planner_events))

    monkeypatch.setattr(
        AirliftPlanner, "create_package_for_airlift", create_package_for_airlift
    )
    now = datetime.now()
    pending.arrange_transport(transfer, now, events)

    assert len(forwarded) == 1
    forwarded_now, forwarded_events = forwarded[0]
    assert forwarded_now == now
    assert forwarded_events is events

    # cancel_transport for an airlift must also forward the accumulator.
    from game.transfers import Airlift

    removed: list[Any] = []
    package = SimpleNamespace(flights=[])
    fake_flight = SimpleNamespace(id="flight-1", package=package)

    def remove_flight(flight: Any) -> None:
        removed.append(flight)
        package.flights.remove(flight)

    package.flights = [fake_flight]
    package.remove_flight = remove_flight
    airlift = Airlift(transfer, cast(Any, fake_flight), cast(Any, destination))
    transfer.transport = airlift
    cancel_events = GameUpdateEvents()
    pending.cancel_transport(airlift, transfer, cancel_events)

    assert removed == [fake_flight]
    assert removed_packages == [package]
    assert cancel_events.deleted_flights == {"flight-1"}
    assert pubs == []


# ---------------------------------------------------------------------------
# Denied / noop operations
# ---------------------------------------------------------------------------


def test_noop_transfer_processing_emits_no_update(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """perform_transfers with no pending transfers emits no motorpool update."""
    pubs = _patch_event_stream(monkeypatch)
    pending = _make_pending(Player.BLUE)
    pending.pending_transfers = []
    events = GameUpdateEvents()

    pending.perform_transfers(events)

    # No motorpool TGOs and no supply-route flag when nothing happened.
    assert events.updated_tgos == set()
    assert not events.updated_supply_routes
    assert pubs == []
