"""Task 5 — Qt transfer model notifications and settings-driven visibility resets.

These tests verify the model/view contracts for ``TransferModel`` and the
settings signal wiring that re-syncs transfer visibility after a game replace
or settings change.
"""

from __future__ import annotations

import json
import zipfile
from datetime import datetime
from types import SimpleNamespace
from typing import Any, cast
from unittest.mock import MagicMock

import pytest
from PySide6.QtCore import QModelIndex, QObject, Signal
from PySide6.QtWidgets import QApplication, QGridLayout, QPushButton, QWidget

from game.dcs.groundunittype import GroundUnitType
from game.purchaseadapter import GroundUnitPurchaseAdapter, TransactionError
from game.settings import Settings
from game.sim.gameupdateevents import GameUpdateEvents
from game.theater.base import Base
from game.theater.player import Player
from game.transfers import (
    PendingTransfers,
    TransferOrder,
)
from qt_ui.models import TransferModel
from qt_ui.windows.basemenu.NewUnitTransferDialog import NewUnitTransferDialog
from qt_ui.windows.basemenu.UnitTransactionFrame import UnitTransactionFrame
from qt_ui.windows.settings.QSettingsWindow import QSettingsWidget

# ---------------------------------------------------------------------------
# Qt application fixture
# ---------------------------------------------------------------------------


@pytest.fixture
def app() -> QApplication:
    return cast(QApplication, QApplication.instance() or QApplication([]))


@pytest.fixture(autouse=True)
def _seed_icons(app: QApplication) -> Any:
    """Populate uiconstants ICONS so QSettingsWidget can construct headless.

    ``QSettingsWidget.initUi`` reads several ``CONST.ICONS`` keys that are only
    populated by ``load_icons()`` (which needs the real resource files). Seed
    blank pixmaps for any missing keys so the settings widget builds under
    offscreen Qt. Depends on ``app`` so a QApplication exists first.
    """
    import qt_ui.uiconstants as CONST
    from PySide6.QtGui import QPixmap

    for key in [
        "Generator",
        "Cheat",
        "Plugins",
        "PluginsOptions",
        "Settings",
    ]:
        if key not in CONST.ICONS:
            CONST.ICONS[key] = QPixmap()
    yield


# ---------------------------------------------------------------------------
# Stub helpers (mirror the Task 4 test_transfer_ownership patterns)
# ---------------------------------------------------------------------------


class HashableCP:
    """A hashable control-point stand-in (usable as a ConvoyMap key)."""

    def __init__(self, name: str, captured: Player = Player.BLUE) -> None:
        self.name = name
        self.captured = captured
        self.base = Base()
        self.ground_objects: list[Any] = []
        self.position = object()

    def __hash__(self) -> int:
        return id(self)

    def __eq__(self, other: object) -> bool:
        return self is other


def _cp(name: str, captured: Player = Player.BLUE) -> HashableCP:
    return HashableCP(name, captured)


def _make_pending(player: Player) -> PendingTransfers:
    """A PendingTransfers with arrange_transport stubbed out."""
    game = MagicMock()
    game.transit_network_for = lambda _p: object()
    pending = PendingTransfers(cast(Any, game), player)
    cast(Any, pending).arrange_transport = lambda _transfer, _now, _events: None
    return pending


def _game_with_settings(
    blue_transfers: Any,
    red_transfers: Any,
    enemy_buy_sell: bool = False,
) -> Any:
    return MagicMock(
        settings=MagicMock(enable_enemy_buy_sell=enemy_buy_sell),
        coalition_for=lambda player: MagicMock(
            transfers=red_transfers if player is Player.RED else blue_transfers
        ),
    )


class SignalCounter(QObject):
    """Records how many times a Qt signal was emitted."""

    fired = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.count = 0
        self.fired.connect(self._inc)

    def _inc(self) -> None:
        self.count += 1


class FakeSimController(QObject):
    sim_update = Signal(GameUpdateEvents)


class FakeTransferModel(QObject):
    inventory_changed = Signal()


class FakePurchaseAdapter:
    def __init__(self, current: int) -> None:
        self.current = current
        self.coalition = SimpleNamespace(budget=100)

    def buy(self, _item: str, quantity: int) -> None:
        self.current += quantity

    def sell(self, _item: str, quantity: int) -> None:
        self.current -= quantity

    def current_quantity_of(self, _item: str) -> int:
        return self.current

    def pending_delivery_quantity(self, _item: str) -> int:
        return 0

    def expected_quantity_next_turn(self, item: str) -> int:
        return self.current_quantity_of(item)

    def name_of(self, item: str, multiline: bool = False) -> str:
        return item if not multiline else f"{item}<br />"

    def price_of(self, _item: str) -> int:
        return 1

    def can_buy(self, _item: str) -> bool:
        return True

    def can_sell_or_cancel(self, _item: str) -> bool:
        return self.current > 0

    def unit_type_of(self, _item: str) -> Any:
        return object()


def _game_model(game: Any, transfer_model: Any = None) -> Any:
    if transfer_model is None:
        transfer_model = MagicMock()
    return SimpleNamespace(game=game, transfer_model=transfer_model)


def _ground_purchase_fixture(
    transfer_model: Any,
) -> tuple[Any, GroundUnitType, Any]:
    unit_type = cast(GroundUnitType, MagicMock(price=5, display_name="Tank"))
    orders = SimpleNamespace(_pending=0)
    orders.pending_orders = lambda _unit_type: orders._pending
    orders.order = lambda _units: setattr(orders, "_pending", orders._pending + 1)
    orders.sell = lambda _units: setattr(orders, "_pending", orders._pending - 1)
    cp = SimpleNamespace(
        captured=Player.BLUE,
        ground_unit_orders=orders,
        base=SimpleNamespace(total_units_of_type=lambda _unit_type: 0),
        has_ground_unit_source=lambda _game: True,
    )
    coalition: Any = SimpleNamespace(
        budget=100,
        adjust_budget=lambda amount: setattr(
            coalition, "budget", coalition.budget + amount
        ),
    )
    game = SimpleNamespace(settings=SimpleNamespace(enable_enemy_buy_sell=False))
    adapter = GroundUnitPurchaseAdapter(
        cast(Any, cp),
        cast(Any, coalition),
        cast(Any, game),
        transfer_model.inventory_changed.emit,
    )
    return cp, unit_type, adapter


def _transfer(
    origin: HashableCP, destination: HashableCP, player: Player
) -> TransferOrder:
    return TransferOrder(cast(Any, origin), cast(Any, destination), {}, player=player)


# ---------------------------------------------------------------------------
# Inventory refresh
# ---------------------------------------------------------------------------


def test_unit_transaction_frame_refreshes_labels_after_transaction(
    app: QApplication, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Selling through the frame refreshes the visible current inventory label."""
    from qt_ui.windows.GameUpdateSignal import GameUpdateSignal

    monkeypatch.setattr(
        GameUpdateSignal,
        "get_instance",
        lambda: SimpleNamespace(updateBudget=lambda _game: None),
    )
    adapter = FakePurchaseAdapter(current=2)
    frame = UnitTransactionFrame(_game_model(SimpleNamespace()), cast(Any, adapter))
    layout = QGridLayout()
    frame.add_purchase_row("tank", layout, 0)

    assert frame.existing_units_labels["tank"].text() == "2"

    frame.sell("tank", 1)

    assert frame.existing_units_labels["tank"].text() == "1"


def test_unit_transaction_frame_refreshes_labels_after_external_inventory_change(
    app: QApplication, monkeypatch: pytest.MonkeyPatch
) -> None:
    """An external inventory signal refreshes an already-open frame label."""
    from qt_ui.windows.GameUpdateSignal import GameUpdateSignal

    monkeypatch.setattr(
        GameUpdateSignal,
        "get_instance",
        lambda: SimpleNamespace(updateBudget=lambda _game: None),
    )
    transfer_model = TransferModel(
        _game_model(
            _game_with_settings(_make_pending(Player.BLUE), _make_pending(Player.RED))
        )
    )
    adapter = FakePurchaseAdapter(current=2)
    frame = UnitTransactionFrame(
        _game_model(SimpleNamespace(), transfer_model), cast(Any, adapter)
    )
    layout = QGridLayout()
    frame.add_purchase_row("tank", layout, 0)

    adapter.current = 7
    transfer_model.inventory_changed.emit()

    assert frame.existing_units_labels["tank"].text() == "7"


def test_ground_purchase_refreshes_all_open_transaction_frames(
    app: QApplication, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Ground orders notify every open transaction frame, including pending labels."""
    from qt_ui.windows.GameUpdateSignal import GameUpdateSignal

    monkeypatch.setattr(
        GameUpdateSignal,
        "get_instance",
        lambda: SimpleNamespace(updateBudget=lambda _game: None),
    )
    transfer_model = TransferModel(
        _game_model(
            _game_with_settings(_make_pending(Player.BLUE), _make_pending(Player.RED))
        )
    )
    first_model = _game_model(SimpleNamespace(), transfer_model)
    second_model = _game_model(SimpleNamespace(), transfer_model)
    cp, unit_type, adapter = _ground_purchase_fixture(transfer_model)
    cp.ground_objects = []
    monkeypatch.setattr("game.server.EventStream.put_nowait", lambda _events: None)
    first = UnitTransactionFrame(first_model, cast(Any, adapter))
    second = UnitTransactionFrame(second_model, cast(Any, adapter))
    first_layout = QGridLayout()
    second_layout = QGridLayout()
    first.add_purchase_row(unit_type, first_layout, 0)
    second.add_purchase_row(unit_type, second_layout, 0)

    adapter.buy(unit_type, 1)

    assert cp.ground_unit_orders.pending_orders(unit_type) == 1
    assert first.purchase_groups[unit_type].amount_bought.text() == "<b>1</b>"
    assert second.purchase_groups[unit_type].amount_bought.text() == "<b>1</b>"


def test_ground_purchase_does_not_refresh_frames_when_validation_fails(
    app: QApplication, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A rejected purchase does not emit a shared inventory refresh."""
    from qt_ui.windows.GameUpdateSignal import GameUpdateSignal

    monkeypatch.setattr(
        GameUpdateSignal,
        "get_instance",
        lambda: SimpleNamespace(updateBudget=lambda _game: None),
    )
    transfer_model = TransferModel(
        _game_model(
            _game_with_settings(_make_pending(Player.BLUE), _make_pending(Player.RED))
        )
    )
    cp, unit_type, adapter = _ground_purchase_fixture(transfer_model)
    cp.ground_objects = []
    monkeypatch.setattr("game.server.EventStream.put_nowait", lambda _events: None)
    adapter.coalition.budget = 0
    first = UnitTransactionFrame(
        _game_model(SimpleNamespace(), transfer_model), cast(Any, adapter)
    )
    layout = QGridLayout()
    first.add_purchase_row(unit_type, layout, 0)
    refreshes: list[int] = []
    transfer_model.inventory_changed.connect(lambda: refreshes.append(1))

    from game.purchaseadapter import TransactionError

    with pytest.raises(TransactionError):
        adapter.buy(unit_type, 1)

    assert cp.ground_unit_orders.pending_orders(unit_type) == 0
    assert refreshes == []


@pytest.mark.parametrize(
    ("enemy_buy_sell", "expected_tabs"),
    [
        (False, ["Intel", "Departing Convoys"]),
        (True, ["Intel", "Departing Convoys", "Ground Forces HQ"]),
    ],
)
def test_red_base_menu_exposes_authorized_ground_forces_tab(
    app: QApplication,
    monkeypatch: pytest.MonkeyPatch,
    enemy_buy_sell: bool,
    expected_tabs: list[str],
) -> None:
    """RED keeps its informational tabs and gates Ground Forces HQ by setting."""
    from qt_ui.windows.basemenu import QBaseMenuTabs as tabs_module

    class StubIntel(QWidget):
        def __init__(self, _cp: Any) -> None:
            super().__init__()

    class StubConvoys(QWidget):
        def __init__(self, _cp: Any, _game_model: Any) -> None:
            super().__init__()

    class StubGroundForces(QWidget):
        def __init__(self, _cp: Any, _game_model: Any) -> None:
            super().__init__()

    monkeypatch.setattr(tabs_module, "QIntelInfo", StubIntel)
    monkeypatch.setattr(tabs_module, "DepartingConvoysMenu", StubConvoys)
    monkeypatch.setattr(tabs_module, "QGroundForcesHQ", StubGroundForces)

    cp = SimpleNamespace(captured=Player.RED)
    game_model = SimpleNamespace(
        game=SimpleNamespace(
            settings=SimpleNamespace(enable_enemy_buy_sell=enemy_buy_sell)
        )
    )

    tabs = tabs_module.QBaseMenuTabs(cast(Any, cp), cast(Any, game_model))

    assert [tabs.tabText(index) for index in range(tabs.count())] == expected_tabs


def test_neutral_base_menu_does_not_expose_ground_forces_tab(
    app: QApplication, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Neutral control points do not expose the ground-forces catalog."""
    from qt_ui.windows.basemenu import QBaseMenuTabs as tabs_module

    class StubAirfield(QWidget):
        def __init__(self, _cp: Any, _game_model: Any) -> None:
            super().__init__()

    class StubGroundForces(QWidget):
        def __init__(self, _cp: Any, _game_model: Any) -> None:
            super().__init__()

    monkeypatch.setattr(tabs_module, "QAirfieldCommand", StubAirfield)
    monkeypatch.setattr(tabs_module, "QGroundForcesHQ", StubGroundForces)

    cp = SimpleNamespace(
        captured=Player.NEUTRAL,
        can_deploy_ground_units=True,
    )
    game_model = SimpleNamespace(game=SimpleNamespace(settings=SimpleNamespace()))

    tabs = tabs_module.QBaseMenuTabs(cast(Any, cp), cast(Any, game_model))

    assert "Ground Forces HQ" not in [
        tabs.tabText(index) for index in range(tabs.count())
    ]


def test_ground_purchase_authorization_is_live_and_owner_based() -> None:
    """Ground purchases follow the current owner and RED's live setting."""
    transfer_model = FakeTransferModel()
    cp, unit_type, adapter = _ground_purchase_fixture(transfer_model)
    cp.captured = Player.RED

    assert not adapter.can_buy(unit_type)
    with pytest.raises(TransactionError):
        adapter.buy(unit_type, 1)
    assert cp.ground_unit_orders.pending_orders(unit_type) == 0

    adapter.game.settings.enable_enemy_buy_sell = True
    assert adapter.can_buy(unit_type)
    adapter.buy(unit_type, 1)
    assert cp.ground_unit_orders.pending_orders(unit_type) == 1

    adapter.game.settings.enable_enemy_buy_sell = False
    with pytest.raises(TransactionError):
        adapter.sell(unit_type, 1)
    assert cp.ground_unit_orders.pending_orders(unit_type) == 1


def test_ground_purchase_direct_neutral_calls_are_denied() -> None:
    """Neutral owners cannot buy or cancel ground-unit orders directly."""
    transfer_model = FakeTransferModel()
    cp, unit_type, adapter = _ground_purchase_fixture(transfer_model)
    cp.captured = Player.NEUTRAL
    cp.ground_unit_orders.order({unit_type: 1})

    assert not adapter.can_buy(unit_type)
    assert not adapter.can_sell(unit_type)
    assert not adapter.can_sell_or_cancel(unit_type)
    with pytest.raises(TransactionError):
        adapter.buy(unit_type, 1)
    with pytest.raises(TransactionError):
        adapter.sell(unit_type, 1)
    assert cp.ground_unit_orders.pending_orders(unit_type) == 1


def test_armor_recruitment_menu_uses_captured_faction_catalog(
    app: QApplication, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A RED menu lists RED units while enemy buy/sell authorization is enabled."""
    from qt_ui.windows.basemenu.ground_forces.QArmorRecruitmentMenu import (
        QArmorRecruitmentMenu,
    )
    from qt_ui.windows.GameUpdateSignal import GameUpdateSignal

    monkeypatch.setattr(
        GameUpdateSignal,
        "get_instance",
        lambda: SimpleNamespace(updateBudget=lambda _game: None),
    )
    blue_unit = cast(GroundUnitType, MagicMock(display_name="Blue tank", price=5))
    red_unit = cast(GroundUnitType, MagicMock(display_name="Red tank", price=5))
    blue_faction = SimpleNamespace(ground_units={blue_unit})
    red_faction = SimpleNamespace(ground_units={red_unit})
    orders = SimpleNamespace(pending_orders=lambda _unit: 0)
    game = SimpleNamespace(
        settings=SimpleNamespace(enable_enemy_buy_sell=True),
        faction_for=lambda player: (
            blue_faction if player is Player.BLUE else red_faction
        ),
        coalition_for=lambda player: SimpleNamespace(
            faction=blue_faction if player is Player.BLUE else red_faction,
            transfers=SimpleNamespace(),
            budget=100,
        ),
    )
    cp = SimpleNamespace(
        captured=Player.RED,
        ground_unit_orders=orders,
        base=SimpleNamespace(total_units_of_type=lambda _unit: 3),
        has_ground_unit_source=lambda _game: True,
    )
    game_model = SimpleNamespace(game=game, transfer_model=FakeTransferModel())

    menu = QArmorRecruitmentMenu(cast(Any, cp), cast(Any, game_model))

    assert set(menu.purchase_groups) == {red_unit}
    assert menu.purchase_groups[red_unit].sell_button.isHidden()


# ---------------------------------------------------------------------------
# Row ordering and insertion
# ---------------------------------------------------------------------------


def test_transfer_create_emits_inventory_changed(app: QApplication) -> None:
    """Creating a transfer emits the Qt inventory refresh notification."""
    blue = _make_pending(Player.BLUE)
    game = _game_with_settings(blue, _make_pending(Player.RED))
    model = TransferModel(_game_model(game))
    fired: list[int] = []
    model.inventory_changed.connect(lambda: fired.append(1))

    origin = _cp("Alpha", captured=Player.BLUE)
    destination = _cp("Bravo", captured=Player.BLUE)
    model.new_transfer(_transfer(origin, destination, Player.BLUE), datetime.now())

    assert fired == [1]


def test_transfer_cancel_emits_inventory_changed(app: QApplication) -> None:
    """Cancelling a transfer emits the Qt inventory refresh notification."""
    blue = _make_pending(Player.BLUE)
    transfer = _transfer(_cp("Alpha"), _cp("Bravo"), Player.BLUE)
    blue.new_transfer(transfer, datetime.now(), GameUpdateEvents())
    game = _game_with_settings(blue, _make_pending(Player.RED))
    model = TransferModel(_game_model(game))
    fired: list[int] = []
    model.inventory_changed.connect(lambda: fired.append(1))

    model.cancel_transfer(transfer)

    assert fired == [1]


def test_sim_update_resets_rows_when_pending_transfers_are_replaced(
    app: QApplication,
) -> None:
    """Turn processing replaces the collection, so the open view must reset."""
    blue = _make_pending(Player.BLUE)
    transfer = _transfer(_cp("Alpha"), _cp("Bravo"), Player.BLUE)
    blue.new_transfer(transfer, datetime.now(), GameUpdateEvents())
    sim_controller = FakeSimController()
    game = _game_with_settings(blue, _make_pending(Player.RED))
    game_model = _game_model(game)
    game_model.sim_controller = sim_controller
    model = TransferModel(game_model)
    resets: list[int] = []
    inventory_refreshes: list[int] = []
    cast(Any, model).modelReset.connect(lambda: resets.append(1))
    model.inventory_changed.connect(lambda: inventory_refreshes.append(1))

    blue.pending_transfers = []
    sim_controller.sim_update.emit(GameUpdateEvents())

    assert model.rowCount() == 0
    assert resets == [1]
    assert inventory_refreshes == [1]


def test_sim_update_resets_rows_when_pending_transfer_is_removed(
    app: QApplication,
) -> None:
    """Turn processing removal is visible even when the list object is retained."""
    blue = _make_pending(Player.BLUE)
    transfer = _transfer(_cp("Alpha"), _cp("Bravo"), Player.BLUE)
    blue.new_transfer(transfer, datetime.now(), GameUpdateEvents())
    sim_controller = FakeSimController()
    game = _game_with_settings(blue, _make_pending(Player.RED))
    game_model = _game_model(game)
    game_model.sim_controller = sim_controller
    model = TransferModel(game_model)
    resets: list[int] = []
    cast(Any, model).modelReset.connect(lambda: resets.append(1))

    blue.pending_transfers.remove(transfer)
    sim_controller.sim_update.emit(GameUpdateEvents())

    assert model.rowCount() == 0
    assert resets == [1]


def test_blue_insert_precedes_visible_red_rows(app: QApplication) -> None:
    """A BLUE insertion announces the pre-insert BLUE count.

    With enemy management enabled and one RED row present, inserting a BLUE
    transfer must announce row 0 (the pre-insert BLUE count), placing it before
    the visible RED row.
    """
    blue = _make_pending(Player.BLUE)
    red = _make_pending(Player.RED)
    red_origin = _cp("Red Origin", captured=Player.RED)
    red_dest = _cp("Red Dest", captured=Player.RED)
    red.new_transfer(
        _transfer(red_origin, red_dest, Player.RED), datetime.now(), GameUpdateEvents()
    )

    game = _game_with_settings(blue, red, enemy_buy_sell=True)
    model = TransferModel(_game_model(game))

    inserts: list[tuple[int, int]] = []
    cast(Any, model).rowsInserted.connect(
        lambda parent, first, last: inserts.append((first, last))
    )

    origin = _cp("Alpha", captured=Player.BLUE)
    destination = _cp("Bravo", captured=Player.BLUE)
    model.new_transfer(_transfer(origin, destination, Player.BLUE), datetime.now())

    # The BLUE row is announced at the pre-insert BLUE count (0), before RED.
    assert inserts == [(0, 0)]
    assert model.rowCount() == 2
    assert (
        model.transfer_at_index(model.index(0, 0, QModelIndex())).player is Player.BLUE
    )
    assert (
        model.transfer_at_index(model.index(1, 0, QModelIndex())).player is Player.RED
    )


def test_authorized_red_insert_uses_snapshot_visibility(
    app: QApplication,
) -> None:
    """An authorized RED transfer inserts only when RED rows are in the model."""
    blue = _make_pending(Player.BLUE)
    red = _make_pending(Player.RED)
    game = _game_with_settings(blue, red, enemy_buy_sell=False)
    model = TransferModel(_game_model(game))
    inserts: list[tuple[int, int]] = []
    cast(Any, model).rowsInserted.connect(
        lambda parent, first, last: inserts.append((first, last))
    )

    # Authorization is live, while the row list is a visibility snapshot until
    # sync_game_and_visibility is called.
    game.settings.enable_enemy_buy_sell = True
    origin = _cp("Red Origin", captured=Player.RED)
    destination = _cp("Red Dest", captured=Player.RED)
    transfer = _transfer(origin, destination, Player.RED)
    model.new_transfer(transfer, datetime.now())

    assert red.pending_transfers == [transfer]
    assert inserts == []
    assert model.rowCount() == 0


def test_red_insert_appends(app: QApplication) -> None:
    """A RED insertion (enemy management enabled) announces the aggregate tail.

    With one BLUE row present, inserting a RED transfer must announce the row
    after the BLUE count.
    """
    blue = _make_pending(Player.BLUE)
    red = _make_pending(Player.RED)
    blue_origin = _cp("Blue Origin", captured=Player.BLUE)
    blue_dest = _cp("Blue Dest", captured=Player.BLUE)
    blue.new_transfer(
        _transfer(blue_origin, blue_dest, Player.BLUE),
        datetime.now(),
        GameUpdateEvents(),
    )

    game = _game_with_settings(blue, red, enemy_buy_sell=True)
    model = TransferModel(_game_model(game))

    inserts: list[tuple[int, int]] = []
    cast(Any, model).rowsInserted.connect(
        lambda parent, first, last: inserts.append((first, last))
    )

    origin = _cp("Red Origin", captured=Player.RED)
    destination = _cp("Red Dest", captured=Player.RED)
    model.new_transfer(_transfer(origin, destination, Player.RED), datetime.now())

    # RED appends after the single BLUE row.
    assert inserts == [(1, 1)]
    assert model.rowCount() == 2


def test_hidden_red_insert_is_rejected_before_any_side_effect(
    app: QApplication, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A disabled RED transfer is a complete no-op in the UI model."""
    blue = _make_pending(Player.BLUE)
    red = _make_pending(Player.RED)
    game = _game_with_settings(blue, red, enemy_buy_sell=False)
    model = TransferModel(_game_model(game))
    inserts: list[tuple[int, int]] = []
    inventory_refreshes: list[int] = []
    published: list[GameUpdateEvents] = []
    cast(Any, model).rowsInserted.connect(
        lambda parent, first, last: inserts.append((first, last))
    )
    model.inventory_changed.connect(lambda: inventory_refreshes.append(1))
    monkeypatch.setattr("qt_ui.models.EventStream.put_nowait", published.append)

    origin = _cp("Red Origin", captured=Player.RED)
    destination = _cp("Red Dest", captured=Player.RED)
    transfer = _transfer(origin, destination, Player.RED)
    model.new_transfer(transfer, datetime.now())

    assert red.pending_transfers == []
    assert inserts == []
    assert model.rowCount() == 0
    assert published == []
    assert inventory_refreshes == []


def test_neutral_insert_is_rejected_before_any_side_effect(
    app: QApplication, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A neutral transfer is never authorized, even when RED management is enabled."""
    blue = _make_pending(Player.BLUE)
    red = _make_pending(Player.RED)
    game = _game_with_settings(blue, red, enemy_buy_sell=True)
    model = TransferModel(_game_model(game))
    inserts: list[tuple[int, int]] = []
    inventory_refreshes: list[int] = []
    published: list[GameUpdateEvents] = []
    cast(Any, model).rowsInserted.connect(
        lambda parent, first, last: inserts.append((first, last))
    )
    model.inventory_changed.connect(lambda: inventory_refreshes.append(1))
    monkeypatch.setattr("qt_ui.models.EventStream.put_nowait", published.append)

    origin = _cp("Neutral Origin", captured=Player.NEUTRAL)
    destination = _cp("Neutral Dest", captured=Player.NEUTRAL)
    transfer = _transfer(origin, destination, Player.NEUTRAL)
    model.new_transfer(transfer, datetime.now())

    assert blue.pending_transfers == []
    assert red.pending_transfers == []
    assert inserts == []
    assert model.rowCount() == 0
    assert published == []
    assert inventory_refreshes == []


# ---------------------------------------------------------------------------
# Removal
# ---------------------------------------------------------------------------


def test_hidden_red_cancel_is_rejected_before_any_side_effect(
    app: QApplication, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A disabled RED transfer cannot be cancelled through the UI model."""
    blue = _make_pending(Player.BLUE)
    red = _make_pending(Player.RED)
    origin = _cp("Red Origin", captured=Player.RED)
    destination = _cp("Red Dest", captured=Player.RED)
    transfer = _transfer(origin, destination, Player.RED)
    red.new_transfer(transfer, datetime.now(), GameUpdateEvents())
    game = _game_with_settings(blue, red, enemy_buy_sell=False)
    model = TransferModel(_game_model(game))
    removals: list[tuple[int, int]] = []
    inventory_refreshes: list[int] = []
    published: list[GameUpdateEvents] = []
    cast(Any, model).rowsRemoved.connect(
        lambda parent, first, last: removals.append((first, last))
    )
    model.inventory_changed.connect(lambda: inventory_refreshes.append(1))
    monkeypatch.setattr("qt_ui.models.EventStream.put_nowait", published.append)

    model.cancel_transfer(transfer)

    assert red.pending_transfers == [transfer]
    assert removals == []
    assert published == []
    assert inventory_refreshes == []


def test_stale_hidden_red_cancel_is_rejected_before_any_side_effect(
    app: QApplication, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A RED transfer absent from stale visible rows is rejected safely."""
    blue = _make_pending(Player.BLUE)
    red = _make_pending(Player.RED)
    origin = _cp("Red Origin", captured=Player.RED)
    destination = _cp("Red Dest", captured=Player.RED)
    transfer = _transfer(origin, destination, Player.RED)
    red.new_transfer(transfer, datetime.now(), GameUpdateEvents())
    game = _game_with_settings(blue, red, enemy_buy_sell=False)
    model = TransferModel(_game_model(game))
    removals: list[tuple[int, int]] = []
    inventory_refreshes: list[int] = []
    published: list[GameUpdateEvents] = []
    cast(Any, model).rowsRemoved.connect(
        lambda parent, first, last: removals.append((first, last))
    )
    model.inventory_changed.connect(lambda: inventory_refreshes.append(1))
    monkeypatch.setattr("qt_ui.models.EventStream.put_nowait", published.append)

    # The live setting changes, but the model's visible-row snapshot is stale.
    game.settings.enable_enemy_buy_sell = True

    model.cancel_transfer(transfer)

    assert red.pending_transfers == [transfer]
    assert model.rowCount() == 0
    assert removals == []
    assert published == []
    assert inventory_refreshes == []


def test_neutral_cancel_is_rejected_before_any_side_effect(
    app: QApplication, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A neutral transfer cannot be cancelled through the UI model."""
    blue = _make_pending(Player.BLUE)
    red = _make_pending(Player.RED)
    origin = _cp("Neutral Origin", captured=Player.NEUTRAL)
    destination = _cp("Neutral Dest", captured=Player.NEUTRAL)
    transfer = _transfer(origin, destination, Player.NEUTRAL)
    game = _game_with_settings(blue, red, enemy_buy_sell=True)
    model = TransferModel(_game_model(game))
    removals: list[tuple[int, int]] = []
    inventory_refreshes: list[int] = []
    published: list[GameUpdateEvents] = []
    cast(Any, model).rowsRemoved.connect(
        lambda parent, first, last: removals.append((first, last))
    )
    model.inventory_changed.connect(lambda: inventory_refreshes.append(1))
    monkeypatch.setattr("qt_ui.models.EventStream.put_nowait", published.append)

    model.cancel_transfer(transfer)

    assert blue.pending_transfers == []
    assert red.pending_transfers == []
    assert removals == []
    assert published == []
    assert inventory_refreshes == []


def test_remove_uses_visible_row(app: QApplication) -> None:
    """Removal authorizes first, then brackets the visible pre-mutation row.

    With one BLUE and one RED row (enemy management enabled), removing the RED
    row must announce removal of the visible row 1.
    """
    blue = _make_pending(Player.BLUE)
    red = _make_pending(Player.RED)
    blue_origin = _cp("Blue Origin", captured=Player.BLUE)
    blue_dest = _cp("Blue Dest", captured=Player.BLUE)
    blue_transfer = _transfer(blue_origin, blue_dest, Player.BLUE)
    blue.new_transfer(blue_transfer, datetime.now(), GameUpdateEvents())

    red_origin = _cp("Red Origin", captured=Player.RED)
    red_dest = _cp("Red Dest", captured=Player.RED)
    red_transfer = _transfer(red_origin, red_dest, Player.RED)
    red.new_transfer(red_transfer, datetime.now(), GameUpdateEvents())

    game = _game_with_settings(blue, red, enemy_buy_sell=True)
    model = TransferModel(_game_model(game))

    removals: list[tuple[int, int]] = []
    cast(Any, model).rowsRemoved.connect(
        lambda parent, first, last: removals.append((first, last))
    )

    model.cancel_transfer(red_transfer)

    # The visible RED row was at index 1.
    assert removals == [(1, 1)]
    assert model.rowCount() == 1
    assert model.transfer_at_index(model.index(0, 0, QModelIndex())) is blue_transfer


# ---------------------------------------------------------------------------
# Visibility sync
# ---------------------------------------------------------------------------


def test_visibility_change_resets_model(app: QApplication) -> None:
    """A visibility change resets the model strictly inside begin/endResetModel.

    With one BLUE and one RED row, toggling enemy management off via
    ``sync_game_and_visibility`` must emit exactly one modelReset and drop the
    RED row from the visible count.
    """
    blue = _make_pending(Player.BLUE)
    red = _make_pending(Player.RED)
    blue_origin = _cp("Blue Origin", captured=Player.BLUE)
    blue_dest = _cp("Blue Dest", captured=Player.BLUE)
    blue.new_transfer(
        _transfer(blue_origin, blue_dest, Player.BLUE),
        datetime.now(),
        GameUpdateEvents(),
    )
    red_origin = _cp("Red Origin", captured=Player.RED)
    red_dest = _cp("Red Dest", captured=Player.RED)
    red.new_transfer(
        _transfer(red_origin, red_dest, Player.RED), datetime.now(), GameUpdateEvents()
    )

    game = _game_with_settings(blue, red, enemy_buy_sell=True)
    model = TransferModel(_game_model(game))
    # Seed the snapshot while RED is visible.
    model.sync_game_and_visibility()
    assert model.rowCount() == 2

    resets: list[int] = []
    cast(Any, model).modelReset.connect(lambda: resets.append(1))

    # Disable enemy management — RED rows become hidden.
    game.settings.enable_enemy_buy_sell = False
    model.sync_game_and_visibility()

    assert resets == [1]
    assert model.rowCount() == 1


def test_game_replacement_syncs_transfer_visibility(app: QApplication) -> None:
    """``GameModel.set()`` calls ``sync_game_and_visibility`` after game replace."""
    from qt_ui.models import GameModel
    from qt_ui.simcontroller import SimController

    blue = _make_pending(Player.BLUE)
    red = _make_pending(Player.RED)
    red_origin = _cp("Red Origin", captured=Player.RED)
    red_dest = _cp("Red Dest", captured=Player.RED)
    red.new_transfer(
        _transfer(red_origin, red_dest, Player.RED), datetime.now(), GameUpdateEvents()
    )

    game = _game_with_settings(blue, red, enemy_buy_sell=True)
    game.blue = MagicMock(ato=MagicMock())
    game.red = MagicMock(ato=MagicMock())
    game.air_wing_for = MagicMock()
    game.theater = MagicMock(control_points_for=lambda _x: [])

    sim_controller = MagicMock(spec=SimController)
    model = GameModel(None, cast(Any, sim_controller))
    sync_calls: list[int] = []
    model.transfer_model.sync_game_and_visibility = (  # type: ignore[method-assign]
        lambda: sync_calls.append(1)
    )

    model.set(game)

    assert sync_calls == [1]


def test_game_replacement_resets_same_visibility_transfer_model(
    app: QApplication,
) -> None:
    """Replacing a same-visibility game still notifies views of new transfer rows."""
    first_blue = _make_pending(Player.BLUE)
    first_transfer = _transfer(_cp("First Origin"), _cp("First Dest"), Player.BLUE)
    first_blue.new_transfer(first_transfer, datetime.now(), GameUpdateEvents())
    first_game = _game_with_settings(
        first_blue, _make_pending(Player.RED), enemy_buy_sell=False
    )

    second_blue = _make_pending(Player.BLUE)
    second_transfer = _transfer(_cp("Second Origin"), _cp("Second Dest"), Player.BLUE)
    second_blue.new_transfer(second_transfer, datetime.now(), GameUpdateEvents())
    second_game = _game_with_settings(
        second_blue, _make_pending(Player.RED), enemy_buy_sell=False
    )

    game_model = _game_model(first_game)
    model = TransferModel(game_model)
    resets: list[int] = []
    cast(Any, model).modelReset.connect(lambda: resets.append(1))

    game_model.game = second_game
    model.sync_game_and_visibility()

    assert resets == [1]
    assert model.transfer_at_index(model.index(0, 0, QModelIndex())) is second_transfer


# ---------------------------------------------------------------------------
# Unloaded safety
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Unloaded safety
# ---------------------------------------------------------------------------


def test_unloaded_game_has_no_rows(app: QApplication) -> None:
    """An unloaded game (no game set) must produce no rows and no signals."""
    game_model = MagicMock()
    game_model.game = None
    model = TransferModel(game_model)

    inserts: list[tuple[int, int]] = []
    cast(Any, model).rowsInserted.connect(
        lambda parent, first, last: inserts.append((first, last))
    )

    assert model.rowCount() == 0
    assert inserts == []


# ---------------------------------------------------------------------------
# Settings signal wiring
# ---------------------------------------------------------------------------


def _settings_widget() -> QSettingsWidget:
    return QSettingsWidget(cast(Any, Settings()), None)


def test_settings_apply_emits_once_and_syncs_transfer_visibility(
    app: QApplication,
) -> None:
    """``applySettings`` emits the completion signal exactly once."""
    widget = _settings_widget()

    fired: list[int] = []
    widget.settings_applied.connect(lambda: fired.append(1))

    widget.applySettings()

    assert fired == [1]


def test_settings_apply_enqueues_all_motorpool_control_points(
    app: QApplication, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Settings changes publish every CP for final motorpool reconciliation."""
    widget = _settings_widget()
    first = _cp("first")
    second = _cp("second")
    published: list[GameUpdateEvents] = []
    updated_at: list[tuple[GameUpdateEvents, tuple[Any, ...]]] = []
    game = SimpleNamespace(
        theater=SimpleNamespace(controlpoints=[first, second]),
        compute_unculled_zones=lambda _events: None,
    )
    widget.game = cast(Any, game)

    def record_motorpool_update(
        events: GameUpdateEvents, *control_points: Any
    ) -> GameUpdateEvents:
        updated_at.append((events, control_points))
        return events

    monkeypatch.setattr(
        GameUpdateEvents, "update_motorpools_at", record_motorpool_update
    )
    monkeypatch.setattr(
        "qt_ui.windows.settings.QSettingsWindow.EventStream.put_nowait",
        lambda events: published.append(events),
    )
    monkeypatch.setattr(
        "qt_ui.windows.settings.QSettingsWindow.GameUpdateSignal.get_instance",
        lambda: SimpleNamespace(updateGame=lambda _game: None),
    )

    widget.applySettings()

    assert len(published) == 1
    assert updated_at == [(published[0], (first, second))]


def _write_settings_zip(path: Any, settings: Settings) -> None:
    # The inner json name must match load_settings' derivation:
    #   zipfilename.split("/")[-1].replace(".zip", ".json")
    inner = path.name.replace(".zip", ".json")
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(
            inner,
            json.dumps(settings.__dict__, indent=2, default=settings.default_json),
            zipfile.ZIP_DEFLATED,
        )


def test_settings_load_emits_once_and_syncs_transfer_visibility(
    app: QApplication, monkeypatch: pytest.MonkeyPatch, tmp_path: Any
) -> None:
    """``load_settings`` emits exactly once after an accepted, decoded archive."""
    import qt_ui.windows.settings.QSettingsWindow as qsw

    widget = _settings_widget()

    fired: list[int] = []
    widget.settings_applied.connect(lambda: fired.append(1))

    archive = tmp_path / "archive.zip"
    _write_settings_zip(archive, Settings())

    fd = MagicMock()
    fd.exec_.return_value = True
    fd.selectedFiles.return_value = [str(archive)]
    monkeypatch.setattr(qsw, "settings_dir", lambda: tmp_path)
    monkeypatch.setattr(qsw, "QFileDialog", lambda *a, **k: fd)
    widget.load_settings()

    assert fired == [1]


def test_settings_default_load_emits_once_and_syncs_transfer_visibility(
    app: QApplication, monkeypatch: pytest.MonkeyPatch, tmp_path: Any
) -> None:
    """``load_default_settings`` emits exactly once after loading defaults."""
    import qt_ui.windows.settings.QSettingsWindow as qsw

    widget = _settings_widget()

    fired: list[int] = []
    widget.settings_applied.connect(lambda: fired.append(1))

    monkeypatch.setattr(qsw, "settings_dir", lambda: tmp_path)
    widget.load_default_settings()

    assert fired == [1]


def test_default_settings_without_json_emits_no_update(
    app: QApplication, monkeypatch: pytest.MonkeyPatch, tmp_path: Any
) -> None:
    """An existing default archive without Default.json is a failed load."""
    import qt_ui.windows.settings.QSettingsWindow as qsw

    widget = _settings_widget()
    fired: list[int] = []
    published: list[GameUpdateEvents] = []
    widget.settings_applied.connect(lambda: fired.append(1))
    monkeypatch.setattr(qsw, "settings_dir", lambda: tmp_path)
    monkeypatch.setattr(qsw.EventStream, "put_nowait", published.append)
    with zipfile.ZipFile(tmp_path / "Default.zip", "w") as archive:
        archive.writestr("other.json", "{}")

    widget.load_default_settings()

    assert fired == []
    assert published == []


@pytest.mark.parametrize("loader", ["archive", "default"])
def test_settings_load_enqueues_all_motorpool_control_points(
    app: QApplication,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Any,
    loader: str,
) -> None:
    """Loaded settings publish every CP for final motorpool reconciliation."""
    import qt_ui.windows.settings.QSettingsWindow as qsw

    widget = _settings_widget()
    first = _cp("first")
    second = _cp("second")
    published: list[GameUpdateEvents] = []
    updated_at: list[tuple[GameUpdateEvents, tuple[Any, ...]]] = []
    widget.game = cast(
        Any,
        SimpleNamespace(
            theater=SimpleNamespace(controlpoints=[first, second]),
            compute_unculled_zones=lambda _events: None,
        ),
    )

    def record_motorpool_update(
        events: GameUpdateEvents, *control_points: Any
    ) -> GameUpdateEvents:
        updated_at.append((events, control_points))
        return events

    monkeypatch.setattr(
        GameUpdateEvents, "update_motorpools_at", record_motorpool_update
    )
    monkeypatch.setattr(
        qsw.EventStream, "put_nowait", lambda events: published.append(events)
    )
    monkeypatch.setattr(
        qsw.GameUpdateSignal,
        "get_instance",
        lambda: SimpleNamespace(updateGame=lambda _game: None),
    )
    monkeypatch.setattr(qsw, "settings_dir", lambda: tmp_path)

    if loader == "archive":
        archive = tmp_path / "archive.zip"
        _write_settings_zip(archive, Settings())
        fd = MagicMock()
        fd.exec_.return_value = True
        fd.selectedFiles.return_value = [str(archive)]
        monkeypatch.setattr(qsw, "QFileDialog", lambda *a, **k: fd)
        widget.load_settings()
    else:
        widget.load_default_settings()

    assert len(published) == 1
    assert updated_at == [(published[0], (first, second))]


def test_transfer_submit_requires_eligible_destination(
    app: QApplication, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Selected units cannot be submitted when no destination is available."""
    submitted: list[Any] = []
    monkeypatch.setattr(
        "qt_ui.windows.basemenu.NewUnitTransferDialog.submit_transfer",
        lambda *args, **kwargs: submitted.append((args, kwargs)),
    )
    monkeypatch.setattr(NewUnitTransferDialog, "close", lambda _self: None)
    dialog = NewUnitTransferDialog.__new__(NewUnitTransferDialog)
    cast(Any, dialog).submit_button = QPushButton()
    cast(Any, dialog).transfer_panel = SimpleNamespace(transfers={"tank": 1})
    cast(Any, dialog).dest_panel = SimpleNamespace(current=None, request_airlift=False)
    cast(Any, dialog).game_model = SimpleNamespace(
        sim_controller=SimpleNamespace(current_time_in_sim=0)
    )
    cast(Any, dialog).origin = object()

    dialog.on_transfer_quantity_changed()
    dialog.on_submit()

    assert dialog.submit_button.isEnabled() is False
    assert submitted == []


def test_cancelled_settings_load_emits_no_settings_applied(
    app: QApplication, monkeypatch: pytest.MonkeyPatch, tmp_path: Any
) -> None:
    """A cancelled load dialog emits zero completion signals."""
    import qt_ui.windows.settings.QSettingsWindow as qsw

    widget = _settings_widget()

    fired: list[int] = []
    widget.settings_applied.connect(lambda: fired.append(1))

    archive = tmp_path / "archive.zip"
    _write_settings_zip(archive, Settings())

    fd = MagicMock()
    fd.exec_.return_value = False  # cancelled
    fd.selectedFiles.return_value = [str(archive)]
    monkeypatch.setattr(qsw, "settings_dir", lambda: tmp_path)
    monkeypatch.setattr(qsw, "QFileDialog", lambda *a, **k: fd)
    widget.load_settings()

    assert fired == []
