"""Tests for stable transfer ownership and migration."""

from __future__ import annotations

from datetime import datetime
from types import SimpleNamespace
from typing import Any, cast
from unittest.mock import MagicMock

import pytest
from game.migrator import Migrator
from game.sim import GameUpdateEvents
from game.theater.base import Base
from game.theater.player import Player
from game.transfers import (
    PendingTransfers,
    TransferOrder,
    create_transfer,
)


class HashableCP(SimpleNamespace):
    """A hashable SimpleNamespace so it can be used as a dict key (for ConvoyMap)."""

    def __hash__(self) -> int:  # type: ignore[override]
        return id(self)


def _cp(name: str, captured: Player = Player.BLUE) -> Any:
    """A minimal control-point stand-in for transfer tests."""
    return HashableCP(
        name=name,
        captured=captured,
        base=Base(),
        ground_objects=[],
        position=object(),
    )


def _make_pending(player: Player) -> PendingTransfers:
    """A PendingTransfers with arrange_transport stubbed out."""
    game = SimpleNamespace(transit_network_for=lambda _p: object())
    pending = PendingTransfers(cast(Any, game), player)
    cast(Any, pending).arrange_transport = lambda _transfer, _now, _events: None
    return pending


def _legacy_transfer(origin: Any, destination: Any, player: Any) -> Any:
    """Build a TransferOrder via __new__ (pickle path) with given player value."""
    transfer = TransferOrder.__new__(TransferOrder)
    transfer.origin = origin
    transfer.destination = destination
    transfer.units = {}
    transfer.transport = None
    transfer.position = origin
    transfer.request_airflift = False
    transfer.player = player
    return transfer


# ---------------------------------------------------------------------------
# Stable ownership
# ---------------------------------------------------------------------------


def test_transfer_string_distinguishes_red_owner() -> None:
    origin = _cp("Alpha", captured=Player.RED)
    destination = _cp("Bravo", captured=Player.RED)
    transfer = TransferOrder(origin, destination, {}, player=Player.RED)

    assert str(transfer).startswith("Enemy transfer")


def test_transfer_owner_survives_origin_capture() -> None:
    """Transfer player does not change when the origin CP is captured."""
    origin = _cp("Alpha", captured=Player.BLUE)
    destination = _cp("Bravo", captured=Player.BLUE)

    transfer = TransferOrder(origin, destination, {}, player=Player.BLUE)
    assert transfer.player is Player.BLUE

    # Enemy captures the origin.
    origin.captured = Player.RED

    # Owner must remain stable — it is not derived from origin.captured.
    assert transfer.player is Player.BLUE


def test_transfer_player_is_required_constructor_argument() -> None:
    """player must be passed explicitly; it cannot be omitted."""
    origin = _cp("Alpha")
    destination = _cp("Bravo")
    with pytest.raises(TypeError):
        TransferOrder(origin, destination, {})  # type: ignore[call-arg]


def test_new_transfer_invariant_checks_player_match() -> None:
    """PendingTransfers.new_transfer asserts transfer.player == self.player."""
    pending = _make_pending(Player.BLUE)
    origin = _cp("Alpha", captured=Player.BLUE)
    destination = _cp("Bravo", captured=Player.BLUE)
    transfer = TransferOrder(origin, destination, {}, player=Player.RED)

    with pytest.raises(AssertionError):
        pending.new_transfer(transfer, datetime.now(), GameUpdateEvents())


def test_split_transfer_preserves_owner() -> None:
    """split_transfer inherits the parent's player."""
    pending = _make_pending(Player.RED)
    origin = _cp("Alpha", captured=Player.RED)
    destination = _cp("Bravo", captured=Player.RED)
    unit = cast("Any", object())
    transfer = TransferOrder(origin, destination, {unit: 4}, player=Player.RED)
    pending.pending_transfers.append(transfer)

    child = pending.split_transfer(transfer, 1)

    assert child.player is Player.RED


def test_ground_unit_orders_create_transfer_passes_coalition_player() -> None:
    """GroundUnitOrders.create_transfer passes coalition.player to TransferOrder."""
    origin = _cp("Alpha", captured=Player.RED)
    destination = _cp("Bravo", captured=Player.RED)
    unit = cast("Any", object())

    captured_transfers: list[TransferOrder] = []
    fake_transfers = SimpleNamespace(
        new_transfer=lambda t, _now, _events: captured_transfers.append(t)
    )
    coalition = SimpleNamespace(player=Player.RED, transfers=fake_transfers)

    from game.groundunitorders import GroundUnitOrders

    orders = GroundUnitOrders(destination)
    orders.create_transfer(
        cast(Any, coalition), origin, {unit: 1}, datetime.now(), GameUpdateEvents()
    )

    assert len(captured_transfers) == 1
    assert captured_transfers[0].player is Player.RED


def test_create_transfer_passes_authorized_origin_owner() -> None:
    """UI create_transfer passes the authorized origin owner to TransferOrder."""
    origin = _cp("Alpha", captured=Player.BLUE)
    destination = _cp("Bravo", captured=Player.BLUE)
    unit = cast("Any", object())

    blue_transfers = _make_pending(Player.BLUE)
    now = datetime.now()
    game_model = SimpleNamespace(
        game=SimpleNamespace(
            coalition_for=lambda player: SimpleNamespace(transfers=blue_transfers)
        ),
        transfer_model=SimpleNamespace(
            new_transfer=lambda t, _now: blue_transfers.new_transfer(
                t, _now, GameUpdateEvents()
            )
        ),
    )

    create_transfer(game_model, origin, destination, {unit: 1}, now)
    assert blue_transfers.pending_transfers[0].player is Player.BLUE


# ---------------------------------------------------------------------------
# Migration
# ---------------------------------------------------------------------------


def test_transfer_migration_deduplicates_aliases() -> None:
    """Migration deduplicates pending list + convoy/cargo aliases by object identity
    and backfills missing/legacy-boolean owner from the containing coalition.
    """
    blue_transfers = _make_pending(Player.BLUE)
    origin = _cp("Alpha", captured=Player.BLUE)
    destination = _cp("Bravo", captured=Player.BLUE)
    # Legacy boolean player.
    transfer = _legacy_transfer(origin, destination, True)

    blue_transfers.pending_transfers.append(transfer)
    # Also reachable via a convoy alias (same object).
    fake_convoy = SimpleNamespace(transfers=[transfer])
    blue_transfers.convoys.transports = cast(Any, {origin: {destination: fake_convoy}})
    blue_transfers.cargo_ships.transports = {}

    coalition = SimpleNamespace(player=Player.BLUE, transfers=blue_transfers)

    migrator = Migrator.__new__(Migrator)
    migrator.game = SimpleNamespace(coalitions=[coalition])  # type: ignore[assignment]
    migrator._update_transfers()

    assert transfer.player is Player.BLUE


def test_transfer_migration_backfills_missing_owner() -> None:
    """Migration sets missing owner from the containing coalition."""
    red_transfers = _make_pending(Player.RED)
    origin = _cp("Alpha", captured=Player.RED)
    destination = _cp("Bravo", captured=Player.RED)
    transfer = TransferOrder.__new__(TransferOrder)
    transfer.origin = origin
    transfer.destination = destination
    transfer.units = {}
    transfer.transport = None
    transfer.position = origin
    transfer.request_airflift = False
    # No player attribute at all (very old save).

    red_transfers.pending_transfers.append(transfer)
    red_transfers.convoys.transports = {}
    red_transfers.cargo_ships.transports = {}

    coalition = SimpleNamespace(player=Player.RED, transfers=red_transfers)

    migrator = Migrator.__new__(Migrator)
    migrator.game = SimpleNamespace(coalitions=[coalition])  # type: ignore[assignment]
    migrator._update_transfers()

    assert transfer.player is Player.RED


def test_transfer_migration_rejects_conflicting_collections() -> None:
    """Same transfer reachable from both coalitions fails with diagnostic."""
    blue_transfers = _make_pending(Player.BLUE)
    red_transfers = _make_pending(Player.RED)
    origin = _cp("Alpha", captured=Player.BLUE)
    destination = _cp("Bravo", captured=Player.BLUE)
    transfer = _legacy_transfer(origin, destination, Player.BLUE)

    # The same transfer object is in both coalitions' pending lists.
    blue_transfers.pending_transfers.append(transfer)
    red_transfers.pending_transfers.append(transfer)

    blue_coalition = SimpleNamespace(player=Player.BLUE, transfers=blue_transfers)
    red_coalition = SimpleNamespace(player=Player.RED, transfers=red_transfers)

    migrator = Migrator.__new__(Migrator)
    migrator.game = SimpleNamespace(coalitions=[blue_coalition, red_coalition])  # type: ignore[assignment]

    with pytest.raises(RuntimeError):
        migrator._update_transfers()


def test_transfer_migration_rejects_conflicting_owner() -> None:
    """Enum owner conflict with sole container fails with diagnostic."""
    blue_transfers = _make_pending(Player.BLUE)
    origin = _cp("Alpha", captured=Player.BLUE)
    destination = _cp("Bravo", captured=Player.BLUE)
    # Owner is RED but in the BLUE coalition — conflict.
    transfer = _legacy_transfer(origin, destination, Player.RED)

    blue_transfers.pending_transfers.append(transfer)
    blue_transfers.convoys.transports = {}
    blue_transfers.cargo_ships.transports = {}

    coalition = SimpleNamespace(player=Player.BLUE, transfers=blue_transfers)

    migrator = Migrator.__new__(Migrator)
    migrator.game = SimpleNamespace(coalitions=[coalition])  # type: ignore[assignment]

    with pytest.raises(RuntimeError):
        migrator._update_transfers()


# ---------------------------------------------------------------------------
# AI RED logistics still functions with cheat disabled
# ---------------------------------------------------------------------------


def test_ai_red_logistics_still_functions_with_cheat_disabled() -> None:
    """Domain PendingTransfers remains usable by AI RED logistics when UI cheat is off."""
    red_transfers = _make_pending(Player.RED)
    origin = _cp("Alpha", captured=Player.RED)
    destination = _cp("Bravo", captured=Player.RED)
    unit = cast("Any", object())
    transfer = TransferOrder(origin, destination, {unit: 2}, player=Player.RED)

    # This must work even though enable_enemy_buy_sell is False for the UI.
    red_transfers.new_transfer(transfer, datetime.now(), GameUpdateEvents())
    assert red_transfers.pending_transfers[0] is transfer

    red_transfers.cancel_transfer(transfer, GameUpdateEvents())
    assert red_transfers.pending_transfers == []
