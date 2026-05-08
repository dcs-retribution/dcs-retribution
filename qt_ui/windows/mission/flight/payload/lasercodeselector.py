from __future__ import annotations

from PySide6.QtWidgets import QComboBox, QWidget

from game import Game
from game.ato.flightmember import FlightMember
from game.lasercodes.lasercode import LaserCode
from qt_ui.blocksignals import block_signals

_DEFAULT = "default"
_ALLOCATE = "allocate"


class LaserCodeSelector(QComboBox):
    """Single combo controlling FlightMember.laser_code.

    Entries:
      - Default (1688): member.set_shared_laser_code(None)
      - Allocate own (xxxx): allocates from registry on first selection,
        member.set_allocated_laser_code(...). Re-selecting after a release
        allocates fresh.
      - JTAC <front> (yyyy): member.set_shared_laser_code(front.laser_code)
    """

    def __init__(
        self, game: Game, flight_member: FlightMember, parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        self.game = game
        self.flight_member = flight_member
        self.currentIndexChanged.connect(self.on_index_changed)
        self.rebuild()

    def set_flight_member(self, flight_member: FlightMember) -> None:
        self.flight_member = flight_member
        self.rebuild()

    def on_index_changed(self) -> None:
        data = self.currentData()
        if data == _DEFAULT:
            self.flight_member.set_shared_laser_code(None)
        elif data == _ALLOCATE:
            if not self.flight_member.owns_laser_code:
                code = self.game.laser_code_registry.alloc_laser_code()
                self.flight_member.set_allocated_laser_code(code)
            # else: already owns one; selecting the row is a no-op.
            self.rebuild()
        elif isinstance(data, LaserCode):
            # JTAC / front code.
            self.flight_member.set_shared_laser_code(data)
        # Otherwise (None data) the combo is disabled for AI; nothing to do.

    def rebuild(self) -> None:
        with block_signals(self):
            self.clear()
            if not self.flight_member.is_player:
                self.addItem("AI does not use laser codes", None)
                self.setDisabled(True)
                return

            self.setEnabled(True)
            current = self.flight_member.laser_code
            owns = self.flight_member.owns_laser_code
            selected_index: int | None = None

            self.addItem("Default (1688)", _DEFAULT)
            if current is None:
                selected_index = 0

            if owns and current is not None:
                self.addItem(f"Allocate own ({current})", _ALLOCATE)
                if selected_index is None:
                    selected_index = self.count() - 1
            else:
                self.addItem("Allocate own", _ALLOCATE)

            for front in self.game.theater.conflicts():
                self.addItem(
                    f"JTAC {front.name} ({front.laser_code})", front.laser_code
                )
                if not owns and current is not None and current == front.laser_code:
                    selected_index = self.count() - 1

            if selected_index is not None:
                self.setCurrentIndex(selected_index)
