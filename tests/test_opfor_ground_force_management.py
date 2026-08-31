from __future__ import annotations

from datetime import datetime
from types import SimpleNamespace
import typing
from typing import Any, cast
from unittest.mock import MagicMock

import pytest
from dcs.mapping import Point
from PySide6.QtCore import QPoint
from PySide6.QtGui import QContextMenuEvent
from PySide6.QtWidgets import QApplication, QLabel, QMenu

from game.purchaseadapter import GroundUnitPurchaseAdapter
from game.migrator import Migrator
from game.theater.base import Base
from game.theater.player import Player
from game.transfers import (
    AirliftPlanner,
    MultiGroupTransport,
    PendingTransfers,
    TransferOrder,
)
from game.theater.transitnetwork import TransitNetwork
from qt_ui.models import TransferModel
from qt_ui.windows.PendingTransfersDialog import PendingTransfersDialog
from qt_ui.windows.basemenu.NewUnitTransferDialog import (
    ScrollingUnitTransferGrid,
    TransferDestinationComboBox,
)
from qt_ui.windows.basemenu.QBaseMenu2 import QBaseMenu2
from qt_ui.windows.settings.QSettingsWindow import CheatSettingsBox


@pytest.fixture
def app() -> QApplication:
    return cast(Any, QApplication.instance() or QApplication([]))


def test_cheat_menu_uses_explicit_opfor_transfer_label(app: QApplication) -> None:
    settings = SimpleNamespace(
        enable_frontline_cheats=False,
        enable_base_capture_cheat=False,
        enable_runway_state_cheat=False,
        enable_transfer_cheat=False,
        enable_air_wing_adjustments=False,
        enable_enemy_buy_sell=False,
    )
    box = CheatSettingsBox(
        cast(Any, SimpleNamespace(settings=settings)), cast(Any, lambda: None)
    )

    label = cast(Any, box.redfor_buysell_cheat.itemAt(0).widget())

    assert label.text() == "Enable OPFOR Buy/Sell/Transfer Cheat"


def test_red_ground_sale_is_available_only_when_cheat_is_enabled() -> None:
    unit_type = cast(Any, MagicMock())
    unit_type.price = 5
    base = Base()
    base.commission_units({unit_type: 2})
    control_point = SimpleNamespace(base=base, captured=Player.RED)
    coalition = SimpleNamespace(player=Player.RED, budget=10)
    game = SimpleNamespace(settings=SimpleNamespace(enable_enemy_buy_sell=False))

    disabled = cast(
        Any,
        GroundUnitPurchaseAdapter(
            cast(Any, control_point), cast(Any, coalition), cast(Any, game)
        ),
    )
    assert disabled.can_sell(unit_type) is False

    game.settings.enable_enemy_buy_sell = True
    enabled = cast(
        Any,
        GroundUnitPurchaseAdapter(
            cast(Any, control_point), cast(Any, coalition), cast(Any, game)
        ),
    )

    assert enabled.can_sell(unit_type) is True


def test_red_transfer_model_routes_transfer_to_red_collection_when_enabled() -> None:
    red_transfers = MagicMock(pending_transfer_count=0)
    blue_transfers = MagicMock(pending_transfer_count=0)
    game = SimpleNamespace(
        settings=SimpleNamespace(enable_enemy_buy_sell=True),
        coalition_for=lambda player: SimpleNamespace(
            transfers=red_transfers if player is Player.RED else blue_transfers
        ),
    )
    model = TransferModel(cast(Any, SimpleNamespace(game=game)))
    transfer = cast(Any, SimpleNamespace(player=Player.RED))

    now = cast(Any, SimpleNamespace())
    model.new_transfer(transfer, now)

    red_transfers.new_transfer.assert_called_once_with(transfer, now)
    blue_transfers.new_transfer.assert_not_called()


def test_transfer_owner_survives_origin_capture_and_split() -> None:
    origin = SimpleNamespace(
        name="Alpha", captured=Player.BLUE, base=Base(), position=object()
    )
    destination = SimpleNamespace(
        name="Bravo", captured=Player.BLUE, base=Base(), position=object()
    )
    unit_type = cast(Any, object())
    pending = PendingTransfers(cast(Any, SimpleNamespace()), Player.BLUE)
    transfer = TransferOrder(
        cast(Any, origin), cast(Any, destination), {unit_type: 2}, player=Player.BLUE
    )
    transport = MultiGroupTransport("Convoy", cast(Any, origin), cast(Any, destination))
    transport.add_units(transfer)

    origin.captured = Player.RED

    assert transfer.player is Player.BLUE
    assert transport.player_owned is Player.BLUE
    pending.pending_transfers.append(transfer)
    assert pending.split_transfer(transfer, 1).player is Player.BLUE


def test_transport_rejects_mixed_owner_transfer_without_mutating() -> None:
    origin = cast(Any, SimpleNamespace(position=object()))
    destination = cast(Any, SimpleNamespace(position=object()))
    blue_transfer = TransferOrder(origin, destination, {}, player=Player.BLUE)
    red_transfer = TransferOrder(origin, destination, {}, player=Player.RED)
    transport = MultiGroupTransport("Convoy", origin, destination)
    transport.add_units(blue_transfer)

    with pytest.raises(ValueError, match="ownership"):
        transport.add_units(red_transfer)

    assert transport.transfers == [blue_transfer]
    assert blue_transfer.transport is transport
    assert red_transfer.transport is None


def test_transfer_rejects_collection_owner_mismatch_without_assert() -> None:
    pending = PendingTransfers(cast(Any, SimpleNamespace()), Player.BLUE)
    transfer = cast(Any, SimpleNamespace(player=Player.RED))

    with pytest.raises(ValueError, match="ownership"):
        pending.validate_transfer(transfer)


def test_transfer_migration_backfills_missing_owner() -> None:
    transfer = SimpleNamespace()
    coalition = SimpleNamespace(player=Player.RED)

    Migrator._normalize_single_transfer_player(transfer, coalition)

    assert transfer.player is Player.RED


def test_transfer_migration_backfills_legacy_boolean_owner_from_each_coalition() -> (
    None
):
    blue_transfer = SimpleNamespace(player=False)
    red_transfer = SimpleNamespace(player=True)
    blue_pending = SimpleNamespace(pending_transfers=[blue_transfer])
    red_pending = SimpleNamespace(pending_transfers=[red_transfer])
    blue_transfers = SimpleNamespace(
        pending_transfers=blue_pending.pending_transfers,
        convoys=[],
        cargo_ships=[],
    )
    red_transfers = SimpleNamespace(
        pending_transfers=red_pending.pending_transfers,
        convoys=[],
        cargo_ships=[],
    )
    migrator = Migrator.__new__(Migrator)
    migrator.game = cast(
        Any,
        SimpleNamespace(
            coalitions=[
                SimpleNamespace(player=Player.BLUE, transfers=blue_transfers),
                SimpleNamespace(player=Player.RED, transfers=red_transfers),
            ]
        ),
    )

    migrator._update_transfers()

    assert blue_transfer.player is Player.BLUE
    assert red_transfer.player is Player.RED


def test_pending_transfers_list_context_menu_delegates_cancel_predicate(
    app: QApplication, monkeypatch: pytest.MonkeyPatch
) -> None:
    transfer = cast(
        Any, SimpleNamespace(player=Player.BLUE, description="No transports available")
    )
    blue_transfers = MagicMock(pending_transfers=[transfer], pending_transfer_count=1)
    game = SimpleNamespace(
        settings=SimpleNamespace(enable_enemy_buy_sell=False),
        coalition_for=lambda player: SimpleNamespace(transfers=blue_transfers),
    )
    game_model = cast(Any, SimpleNamespace(game=game))
    transfer_model = TransferModel(game_model)
    game_model.transfer_model = transfer_model
    dialog = PendingTransfersDialog(game_model)
    list_widget = dialog.transfer_list
    list_widget.resize(200, 100)
    list_widget.show()
    app.processEvents()
    menu_exec = MagicMock()
    monkeypatch.setattr(QMenu, "exec_", menu_exec)
    event = QContextMenuEvent(
        QContextMenuEvent.Reason.Mouse,
        list_widget.visualRect(list_widget.model().index(0, 0)).center(),
        QPoint(10, 10),
    )
    list_widget.contextMenuEvent(event)

    menu_exec.assert_called_once()


def test_transfer_model_refreshes_rows_when_red_visibility_changes(
    app: QApplication,
) -> None:
    red_transfer = cast(Any, SimpleNamespace(player=Player.RED))
    blue_transfer = cast(Any, SimpleNamespace(player=Player.BLUE))
    red_transfers = SimpleNamespace(pending_transfers=[red_transfer])
    blue_transfers = SimpleNamespace(pending_transfers=[blue_transfer])
    settings = SimpleNamespace(enable_enemy_buy_sell=False)
    game = SimpleNamespace(
        settings=settings,
        coalition_for=lambda player: SimpleNamespace(
            transfers=red_transfers if player is Player.RED else blue_transfers
        ),
    )
    game_model = cast(Any, SimpleNamespace(game=game))
    model = TransferModel(game_model)
    model_resets = []
    layouts = []
    data_changes = []
    cast(Any, model).modelAboutToBeReset.connect(lambda: model_resets.append("about"))
    cast(Any, model).modelReset.connect(lambda: model_resets.append("reset"))
    cast(Any, model).layoutAboutToBeChanged.connect(lambda: layouts.append("about"))
    cast(Any, model).layoutChanged.connect(lambda: layouts.append("changed"))
    cast(Any, model).dataChanged.connect(lambda *_args: data_changes.append(True))

    assert model.rowCount() == 1
    settings.enable_enemy_buy_sell = True
    model.sync_game_and_visibility()

    assert model.rowCount() == 2
    assert model.transfer_at_index(model.index(1, 0)) is red_transfer
    assert model.red_visible is True
    assert model_resets == ["about", "reset"]
    assert layouts == ["about", "changed"]
    assert data_changes


def test_red_transfer_model_maps_rows_and_cancels_red_transfer() -> None:
    red_transfer = cast(Any, SimpleNamespace(player=Player.RED))
    blue_transfer = cast(Any, SimpleNamespace(player=Player.BLUE))
    red_transfers = MagicMock(
        pending_transfer_count=1,
        pending_transfers=[red_transfer],
    )
    blue_transfers = MagicMock(
        pending_transfer_count=1,
        pending_transfers=[blue_transfer],
    )
    game = SimpleNamespace(
        settings=SimpleNamespace(enable_enemy_buy_sell=True),
        coalition_for=lambda player: SimpleNamespace(
            transfers=red_transfers if player is Player.RED else blue_transfers
        ),
    )
    model = TransferModel(cast(Any, SimpleNamespace(game=game)))

    assert model.rowCount() == 2
    assert model.transfer_at_index(model.index(1, 0)) is red_transfer
    model.cancel_transfer_at_index(model.index(1, 0))

    red_transfers.cancel_transfer.assert_called_once_with(red_transfer)
    blue_transfers.cancel_transfer.assert_not_called()


@typing.no_type_check
def test_legacy_boolean_transfer_owner_is_preserved_and_validated() -> None:
    transfer = SimpleNamespace(player=True)
    blue_coalition = SimpleNamespace(player=Player.BLUE)
    Migrator._normalize_single_transfer_player(transfer, blue_coalition)
    assert transfer.player is Player.BLUE

    transfer.player = False
    red_coalition = SimpleNamespace(player=Player.RED)
    Migrator._normalize_single_transfer_player(transfer, red_coalition)
    assert transfer.player is Player.RED

    with pytest.raises(RuntimeError, match="owner"):
        Migrator._normalize_single_transfer_player(transfer, blue_coalition)


@typing.no_type_check
def test_red_transfer_rejects_cross_coalition_destination() -> None:
    unit_type = cast(Any, MagicMock())
    origin = cast(
        Any,
        SimpleNamespace(name="Red origin", captured=Player.RED, base=Base()),
    )
    destination = cast(
        Any,
        SimpleNamespace(name="Blue destination", captured=Player.BLUE, base=Base()),
    )
    origin.base.commission_units({unit_type: 2})
    pending = PendingTransfers(cast(Any, SimpleNamespace()), Player.RED)
    transfer = TransferOrder(origin, destination, {unit_type: 1}, player=Player.RED)

    with pytest.raises(ValueError, match="destination"):
        pending.new_transfer(transfer, SimpleNamespace())

    assert origin.base.total_units_of_type(unit_type) == 2
    assert pending.pending_transfers == []


@typing.no_type_check
def test_red_transfer_rejects_invalid_route_before_committing_origin_losses() -> None:
    unit_type = cast(Any, MagicMock())
    origin = cast(
        Any,
        SimpleNamespace(
            name="Red origin",
            captured=Player.RED,
            base=Base(),
            position=SimpleNamespace(distance_to_point=lambda _other: 1),
        ),
    )
    destination = cast(
        Any,
        SimpleNamespace(
            name="Red destination",
            captured=Player.RED,
            base=Base(),
            position=SimpleNamespace(distance_to_point=lambda _other: 1),
        ),
    )
    origin.base.commission_units({unit_type: 2})
    pending = PendingTransfers(cast(Any, SimpleNamespace()), Player.RED)
    invalid_network = TransitNetwork()
    invalid_network.shortest_path_between = lambda _origin, _destination: (
        _ for _ in ()
    ).throw(ValueError())
    pending.network_for = lambda _cp: invalid_network
    transfer = TransferOrder(origin, destination, {unit_type: 1}, player=Player.RED)

    with pytest.raises(ValueError):
        pending.new_transfer(transfer, SimpleNamespace())

    assert origin.base.total_units_of_type(unit_type) == 2
    assert pending.pending_transfers == []


@typing.no_type_check
def test_red_transfer_destination_combo_uses_red_friendly_points(
    app: QApplication,
) -> None:
    origin = cast(Any, SimpleNamespace(name="origin"))
    red_destination = cast(
        Any,
        SimpleNamespace(
            name="red destination",
            captured=Player.RED,
            can_deploy_ground_units=True,
            is_friendly=lambda to_player: red_destination.captured == to_player,
        ),
    )
    blue_destination = cast(
        Any,
        SimpleNamespace(
            name="blue destination",
            captured=Player.BLUE,
            can_deploy_ground_units=True,
            is_friendly=lambda to_player: blue_destination.captured == to_player,
        ),
    )
    neutral_destination = cast(
        Any,
        SimpleNamespace(
            name="neutral destination",
            captured=Player.NEUTRAL,
            can_deploy_ground_units=True,
            is_friendly=lambda to_player: neutral_destination.captured == to_player,
        ),
    )
    game = cast(
        Any,
        SimpleNamespace(
            theater=SimpleNamespace(
                controlpoints=[
                    origin,
                    red_destination,
                    blue_destination,
                    neutral_destination,
                ]
            )
        ),
    )
    origin.captured = Player.RED

    combo = TransferDestinationComboBox(game, origin)

    assert [combo.itemData(i) for i in range(combo.count())] == [red_destination]


@typing.no_type_check
def test_red_transfer_grid_uses_red_faction_units(app: QApplication) -> None:
    unit_type = cast(Any, MagicMock(display_name="Red tank"))
    origin = cast(
        Any,
        SimpleNamespace(
            base=SimpleNamespace(total_units_of_type=lambda unit: 1),
            captured=Player.RED,
        ),
    )
    game_model = cast(
        Any,
        SimpleNamespace(
            game=SimpleNamespace(
                faction_for=lambda player: SimpleNamespace(
                    ground_units={unit_type} if player is Player.RED else set()
                )
            )
        ),
    )

    grid = ScrollingUnitTransferGrid(origin, game_model)

    assert grid.transfers == {}
    assert any(label.text() == "<b>Red tank</b>" for label in grid.findChildren(QLabel))


@typing.no_type_check
def test_red_base_menu_budget_uses_captured_coalition() -> None:
    menu = QBaseMenu2.__new__(QBaseMenu2)
    menu.cp = SimpleNamespace(captured=Player.RED)
    menu.budget_display = MagicMock()
    menu.update_budget(
        SimpleNamespace(
            blue=SimpleNamespace(budget=10),
            red=SimpleNamespace(budget=20),
        )
    )
    menu.budget_display.setText.assert_called_once()
    assert "20" in menu.budget_display.setText.call_args.args[0]


@typing.no_type_check
def test_capture_then_cancel_does_not_refund_units_to_enemy_owned_origin() -> None:
    unit_type = cast(Any, object())
    origin = cast(
        Any,
        SimpleNamespace(
            name="Red origin",
            captured=Player.RED,
            base=Base(),
            position=object(),
            is_friendly=lambda player: origin.captured == player,
        ),
    )
    destination = cast(
        Any,
        SimpleNamespace(
            name="Red destination", captured=Player.RED, base=Base(), position=object()
        ),
    )
    origin.base.commission_units({unit_type: 1})
    pending = PendingTransfers(cast(Any, SimpleNamespace()), Player.RED)
    transfer = TransferOrder(origin, destination, {unit_type: 1}, player=Player.RED)
    origin.base.commit_losses(transfer.units)
    pending.pending_transfers.append(transfer)
    pending._send_supply_route_event_stream_update = lambda: None

    origin.captured = Player.BLUE
    pending.cancel_transfer(transfer)

    assert origin.base.total_units_of_type(unit_type) == 0
    assert transfer.units == {}


@typing.no_type_check
def test_transfer_routing_uses_owner_after_origin_is_captured() -> None:
    origin = cast(
        Any,
        SimpleNamespace(name="Origin", captured=Player.RED, position=object()),
    )
    destination = cast(
        Any,
        SimpleNamespace(name="Destination", captured=Player.BLUE, position=object()),
    )
    blue_network = object()
    red_network = object()
    game = SimpleNamespace(
        transit_network_for=lambda player: (
            blue_network if player is Player.BLUE else red_network
        )
    )
    pending = PendingTransfers(cast(Any, game), Player.BLUE)
    transfer = TransferOrder(origin, destination, {}, player=Player.BLUE)

    assert pending.network_for(transfer.position) is blue_network


@typing.no_type_check
def test_transport_identity_uses_contained_transfer_owner_after_capture() -> None:
    blue_coalition = object()
    game = SimpleNamespace(
        coalition_for=lambda player: (
            blue_coalition if player is Player.BLUE else object()
        )
    )
    origin = cast(
        Any,
        SimpleNamespace(
            captured=Player.BLUE,
            position=object(),
            coalition=SimpleNamespace(game=game),
        ),
    )
    destination = cast(Any, SimpleNamespace(position=object()))
    transfer = TransferOrder(origin, destination, {}, player=Player.BLUE)
    convoy = MultiGroupTransport("Convoy", origin, destination)
    convoy.add_units(transfer)

    origin.captured = Player.RED

    assert convoy.is_friendly(Player.BLUE)
    assert convoy.coalition is blue_coalition


def test_airlift_rejects_helicopter_when_pickup_to_drop_off_exceeds_range() -> None:
    max_range = AirliftPlanner.HELO_MAX_RANGE.meters
    home = Point(0, 0, None)  # type: ignore[arg-type]
    pickup = Point(-0.6 * max_range, 0, None)  # type: ignore[arg-type]
    drop_off = Point(0.6 * max_range, 0, None)  # type: ignore[arg-type]
    transfer = cast(
        Any,
        SimpleNamespace(
            origin=SimpleNamespace(can_operate=lambda _unit_type: True),
            player=Player.BLUE,
            position=SimpleNamespace(position=pickup),
        ),
    )
    next_stop = cast(
        Any,
        SimpleNamespace(
            can_operate=lambda _unit_type: True,
            position=drop_off,
        ),
    )
    planner = object.__new__(AirliftPlanner)
    planner.transfer = transfer
    planner.next_stop = next_stop
    helicopter = cast(
        Any,
        SimpleNamespace(
            capable_of=lambda _task: True,
            dcs_unit_type=SimpleNamespace(helicopter=True),
        ),
    )
    airfield = cast(Any, SimpleNamespace(position=home))

    assert not planner.compatible_with_mission(helicopter, airfield)


def test_transfer_model_does_not_begin_insert_for_rejected_transfer(
    app: QApplication,
) -> None:
    unit_type = cast(Any, object())
    origin = cast(
        Any,
        SimpleNamespace(name="Red origin", captured=Player.RED, base=Base()),
    )
    destination = cast(
        Any,
        SimpleNamespace(name="Blue destination", captured=Player.BLUE, base=Base()),
    )
    red_transfers = PendingTransfers(cast(Any, SimpleNamespace()), Player.RED)
    blue_transfers = PendingTransfers(cast(Any, SimpleNamespace()), Player.BLUE)
    game = SimpleNamespace(
        settings=SimpleNamespace(enable_enemy_buy_sell=True),
        coalition_for=lambda player: SimpleNamespace(
            transfers=red_transfers if player is Player.RED else blue_transfers
        ),
    )
    model = TransferModel(cast(Any, SimpleNamespace(game=game)))
    transfer = TransferOrder(origin, destination, {unit_type: 1}, player=Player.RED)
    about_to_insert = []
    inserted = []
    cast(Any, model).rowsAboutToBeInserted.connect(lambda: about_to_insert.append(True))
    cast(Any, model).rowsInserted.connect(lambda: inserted.append(True))

    with pytest.raises(ValueError, match="destination"):
        model.new_transfer(transfer, SimpleNamespace())

    assert about_to_insert == []
    assert inserted == []
    assert red_transfers.pending_transfers == []


def test_red_transfer_model_rejects_mutation_when_cheat_is_disabled() -> None:
    game = SimpleNamespace(
        settings=SimpleNamespace(enable_enemy_buy_sell=False),
        coalition_for=lambda _player: SimpleNamespace(
            transfers=MagicMock(pending_transfer_count=0)
        ),
    )
    model = TransferModel(cast(Any, SimpleNamespace(game=game)))
    transfer = cast(Any, SimpleNamespace(player=Player.RED))

    with pytest.raises(PermissionError, match="OPFOR buy/sell/transfer is disabled"):
        model.new_transfer(transfer, SimpleNamespace())
