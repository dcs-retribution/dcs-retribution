import logging
from typing import Iterable, List, Optional

from PySide6.QtCore import Signal, Qt, QModelIndex, QItemSelectionModel
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from game import Game
from game.ato.flight import Flight
from game.ato.flightplans.custom import CustomFlightPlan
from game.ato.flightplans.formationattack import FormationAttackFlightPlan
from game.ato.flightplans.planningerror import PlanningError
from game.ato.flightplans.waypointbuilder import WaypointBuilder
from game.ato.flighttype import FlightType
from game.ato.flightwaypoint import FlightWaypoint
from game.ato.flightwaypointtype import FlightWaypointType
from game.utils import feet
from game.ato.loadouts import Loadout
from game.ato.package import Package
from game.theater import Player
from qt_ui.windows.mission.flight.waypoints.QFlightWaypointList import (
    QFlightWaypointList,
)
from qt_ui.windows.mission.flight.waypoints.QPredefinedWaypointSelectionWindow import (
    QPredefinedWaypointSelectionWindow,
)


class QFlightWaypointTab(QFrame):
    loadout_changed = Signal()

    # Waypoint types whose altitude the bulk setter must not touch. Their altitude is
    # tied to something other than the en-route cruise band, so overwriting it with a
    # cruise MSL would break the flight plan:
    #   * Takeoff / pattern / landing points are tied to the airfield.
    #   * Divert and cargo-stop points are alternate landing fields.
    #   * Target points carry the target's own elevation (used for attack geometry).
    #   * Pickup / dropoff zones are ground-level helo landing zones.
    #   * Refuel / recovery-tanker points are tied to the tanker's orbit altitude.
    #   * Bullseye is a fixed map reference, not a flown waypoint.
    BULK_ALTITUDE_SKIP_TYPES = frozenset(
        {
            FlightWaypointType.TAKEOFF,
            FlightWaypointType.DESCENT_POINT,
            FlightWaypointType.LANDING_POINT,
            FlightWaypointType.DIVERT,
            FlightWaypointType.CARGO_STOP,
            FlightWaypointType.TARGET_POINT,
            FlightWaypointType.TARGET_GROUP_LOC,
            FlightWaypointType.TARGET_SHIP,
            FlightWaypointType.PICKUP_ZONE,
            FlightWaypointType.DROPOFF_ZONE,
            FlightWaypointType.REFUEL,
            FlightWaypointType.RECOVERY_TANKER,
            FlightWaypointType.BULLSEYE,
        }
    )

    def __init__(self, game: Game, package: Package, flight: Flight):
        super(QFlightWaypointTab, self).__init__()
        self.game = game
        self.coalition = game.coalition_for(player=Player.BLUE)
        self.package = package
        self.flight = flight
        # Show the escort-drift warning at most once per manual-timing session.
        self._escort_warning_shown = False

        self.flight_waypoint_list: Optional[QFlightWaypointList] = None
        self.rtb_waypoint: Optional[QPushButton] = None
        self.delete_selected: Optional[QPushButton] = None
        self.add_nav_waypoint: Optional[QPushButton] = None
        self.open_fast_waypoint_button: Optional[QPushButton] = None
        self.move_up_button: Optional[QPushButton] = None
        self.move_down_button: Optional[QPushButton] = None
        self.manual_tot_label: Optional[QLabel] = None
        self.reset_tot_button: Optional[QPushButton] = None
        self.plan_type_label: Optional[QLabel] = None
        self.convert_button: Optional[QPushButton] = None
        self.recreate_buttons: List[QPushButton] = []
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()

        self.flight_waypoint_list = QFlightWaypointList(self.package, self.flight)
        self.flight_waypoint_list.tot_changed.connect(self.on_tot_changed)
        layout.addWidget(self.flight_waypoint_list, 0, 0)

        rlayout = QVBoxLayout()
        layout.addLayout(rlayout, 0, 1)

        rlayout.addWidget(QLabel("<strong>Altitude :</strong>"))
        rlayout.addWidget(QLabel("<small>Set all en-route waypoints</small>"))
        bulk_alt_layout = QHBoxLayout()
        self.bulk_altitude = QSpinBox()
        self.bulk_altitude.setMinimum(0)
        self.bulk_altitude.setMaximum(40000)
        self.bulk_altitude.setSingleStep(1000)
        self.bulk_altitude.setValue(self._default_bulk_altitude())
        self.bulk_altitude.setSuffix(" ft")
        self.bulk_altitude.setToolTip(
            "Apply this MSL altitude to every en-route waypoint. Takeoff, landing, "
            "divert, target, landing-zone, tanker, and ground (AGL) waypoints are "
            "left unchanged."
        )
        bulk_alt_layout.addWidget(self.bulk_altitude)
        self.apply_bulk_altitude = QPushButton("Apply to all")
        self.apply_bulk_altitude.clicked.connect(self.on_apply_bulk_altitude)
        bulk_alt_layout.addWidget(self.apply_bulk_altitude)
        rlayout.addLayout(bulk_alt_layout)

        rlayout.addWidget(QLabel("<strong>Generator :</strong>"))
        rlayout.addWidget(QLabel("<small>AI compatible</small>"))
        self.plan_type_label = QLabel()
        rlayout.addWidget(self.plan_type_label)

        self.recreate_buttons.clear()
        for task in self.package.target.mission_types(for_player=Player.BLUE):
            if task == FlightType.AIR_ASSAULT and not self.game.settings.plugin_option(
                "ctld"
            ):
                # Only add Air Assault if ctld plugin is enabled
                continue

            def make_closure(arg):
                def closure():
                    return self.confirm_recreate(arg)

                return closure

            button = QPushButton(f"Recreate as {task}")
            button.clicked.connect(make_closure(task))
            rlayout.addWidget(button)
            self.recreate_buttons.append(button)

        self.add_nav_waypoint = QPushButton("Insert NAV point")
        self.add_nav_waypoint.clicked.connect(self.on_add_nav)
        rlayout.addWidget(self.add_nav_waypoint)

        self.move_up_button = QPushButton("Move Up")
        self.move_up_button.clicked.connect(lambda: self.on_move_waypoint(-1))
        rlayout.addWidget(self.move_up_button)

        self.move_down_button = QPushButton("Move Down")
        self.move_down_button.clicked.connect(lambda: self.on_move_waypoint(1))
        rlayout.addWidget(self.move_down_button)

        self.manual_tot_label = QLabel(
            "<small><b>Manually timed</b> — decoupled from package TOT</small>"
        )
        rlayout.addWidget(self.manual_tot_label)

        self.reset_tot_button = QPushButton("Reset ToT to auto")
        self.reset_tot_button.clicked.connect(self.on_reset_tot)
        rlayout.addWidget(self.reset_tot_button)

        rlayout.addWidget(QLabel("<strong>Advanced : </strong>"))
        rlayout.addWidget(QLabel("<small>Do not use for AI flights</small>"))

        self.rtb_waypoint = QPushButton("Add RTB Waypoint")
        self.rtb_waypoint.clicked.connect(self.on_rtb_waypoint)
        rlayout.addWidget(self.rtb_waypoint)

        self.convert_button = QPushButton("Convert to custom plan")
        self.convert_button.clicked.connect(self.on_convert_to_custom)
        rlayout.addWidget(self.convert_button)

        self.delete_selected = QPushButton("Delete Selected")
        self.delete_selected.clicked.connect(self.on_delete_waypoint)
        rlayout.addWidget(self.delete_selected)

        self.open_fast_waypoint_button = QPushButton("Add Waypoint")
        self.open_fast_waypoint_button.clicked.connect(self.on_fast_waypoint)
        rlayout.addWidget(self.open_fast_waypoint_button)
        rlayout.addStretch()
        self.setLayout(layout)
        self.refresh_manual_tot_widgets()
        self.refresh_plan_type()

    def on_add_nav(self):
        selected = self.flight_waypoint_list.selectedIndexes()
        if not selected:
            return
        index: QModelIndex = selected[0]
        self.flight_waypoint_list.setCurrentIndex(index)
        wpt: FlightWaypoint = self.flight_waypoint_list.model.data(
            index, Qt.ItemDataRole.UserRole
        )
        next_wpt: Optional[FlightWaypoint] = None
        if index.row() + 1 < self.flight_waypoint_list.model.rowCount():
            next_wpt = self.flight_waypoint_list.model.data(
                index.siblingAtRow(index.row() + 1), Qt.ItemDataRole.UserRole
            )
        if not self.flight.flight_plan.layout.add_waypoint(wpt, next_wpt):
            QMessageBox.critical(
                QWidget(),
                "Failed to add NAV waypoint",
                "Could not insert a new waypoint given the currently selected waypoint.\n"
                "Please select a different waypoint to insert the new NAV waypoint.",
            )
        else:
            self.flight_waypoint_list.model.insertRow(
                self.flight_waypoint_list.model.rowCount()
            )
            self.on_change()

    def on_delete_waypoint(self):
        waypoints = []
        selection = self.flight_waypoint_list.selectionModel()
        for selected_row in selection.selectedIndexes():
            if selected_row.row() > 0:
                waypoints.append(self.flight.flight_plan.waypoints[selected_row.row()])
        for waypoint in waypoints:
            self.delete_waypoint(waypoint)
        self.on_change()

    def delete_waypoint(self, waypoint: FlightWaypoint) -> None:
        # Need to degrade to a custom flight plan and remove the waypoint.
        # If the waypoint is a target waypoint and is not the last target
        # waypoint, we don't need to degrade.
        fp = self.flight.flight_plan
        if isinstance(fp, FormationAttackFlightPlan):
            is_target = waypoint in fp.target_area_waypoint.targets
            count = len(fp.target_area_waypoint.targets)
            if is_target and count > 1:
                fp.target_area_waypoint.targets.remove(waypoint)
                return
        model = self.flight_waypoint_list.model
        if fp.layout.delete_waypoint(waypoint):
            model.removeRow(model.rowCount() - 1)
            return

        if not self.flight.flight_plan.is_custom:
            confirmed = self.confirm_degrade()
            if not confirmed:
                return
        model.removeRow(model.rowCount() - 1)
        self.degrade_to_custom_flight_plan()
        assert isinstance(self.flight.flight_plan, CustomFlightPlan)
        self.flight.flight_plan.layout.custom_waypoints.remove(waypoint)

    def confirm_degrade(self, parent: Optional[QWidget] = None) -> bool:
        result = QMessageBox.warning(
            parent if parent else self,
            "Convert flight plan?",
            "Deleting the selected waypoint(s) requires converting this flight to a "
            "custom flight plan. A custom flight plan is no longer automatically timed "
            "to the package TOT; its waypoint times become independent and manually "
            "adjustable.<br><br>"
            "<b>Are you sure you wish to continue?</b>",
            QMessageBox.StandardButton.Yes,
            QMessageBox.StandardButton.No,
        )
        return result == QMessageBox.StandardButton.Yes

    def on_fast_waypoint(self):
        self.subwindow = QPredefinedWaypointSelectionWindow(
            self.game, self.flight, self.flight_waypoint_list
        )
        self.subwindow.waypoints_added.connect(self.on_waypoints_added)
        self.subwindow.show()

    def on_waypoints_added(self, waypoints: Iterable[FlightWaypoint]) -> None:
        waypoints = list(waypoints)
        if not waypoints:
            return
        customs = self.flight.flight_plan.layout.custom_waypoints
        insert_at = self._custom_insert_index()
        if insert_at is None:
            customs.extend(waypoints)
        else:
            customs[insert_at:insert_at] = waypoints
        self.add_rows(len(waypoints))

    def _custom_insert_index(self) -> Optional[int]:
        selected = self.flight_waypoint_list.selectedIndexes()
        if not selected:
            return None
        row = selected[0].row()
        waypoints = self.flight.flight_plan.waypoints
        customs = self.flight.flight_plan.layout.custom_waypoints
        selected_wp = waypoints[row]
        if selected_wp in customs:
            # Insert immediately after the selected custom waypoint.
            return customs.index(selected_wp) + 1
        # Selected waypoint is structural: append to the front of custom_waypoints so the
        # new waypoint still renders after the structural section it follows.
        return 0 if customs else None

    def add_rows(self, count: int) -> None:
        rc = self.flight_waypoint_list.model.rowCount()
        self.flight_waypoint_list.model.insertRows(rc, count)
        self.on_change()

    def on_rtb_waypoint(self):
        rtb = WaypointBuilder(self.flight).land(self.flight.arrival)
        self.degrade_to_custom_flight_plan()
        assert isinstance(self.flight.flight_plan, CustomFlightPlan)
        self.flight.flight_plan.layout.custom_waypoints.append(rtb)
        self.add_rows(1)

    def degrade_to_custom_flight_plan(self) -> None:
        if not isinstance(self.flight.flight_plan, CustomFlightPlan):
            self.flight.degrade_to_custom_flight_plan()

    def on_convert_to_custom(self) -> None:
        if self.flight.flight_plan.is_custom:
            return
        result = QMessageBox.question(
            self,
            "Convert flight plan?",
            "Convert this flight to a custom flight plan? A custom flight plan is no "
            "longer automatically timed to the package TOT; its waypoint times become "
            "independent and manually adjustable.",
            QMessageBox.StandardButton.Yes,
            QMessageBox.StandardButton.No,
        )
        if result != QMessageBox.StandardButton.Yes:
            return
        self.degrade_to_custom_flight_plan()
        self.on_change()

    def refresh_plan_type(self) -> None:
        if self.plan_type_label is None or self.convert_button is None:
            return
        is_custom = self.flight.flight_plan.is_custom
        if is_custom:
            self.plan_type_label.setText("<small><b>Plan:</b> Custom</small>")
        else:
            self.plan_type_label.setText(
                f"<small><b>Plan:</b> Standard ({self.flight.flight_type})</small>"
            )
        self.convert_button.setEnabled(not is_custom)

    def confirm_recreate(self, task: FlightType) -> None:
        result = QMessageBox.question(
            self,
            "Regenerate flight?",
            (
                "Changing the flight type will reset its flight plan. Do you want "
                "to continue?"
            ),
            QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes,
        )
        original_task = self.flight.flight_type
        if result == QMessageBox.StandardButton.Yes:
            self.flight.set_flight_type(task)
            try:
                self.flight.recreate_flight_plan(dump_debug_info=True)
            except PlanningError as ex:
                self.flight.set_flight_type(original_task)
                logging.exception("Could not recreate flight")
                QMessageBox.critical(
                    self,
                    "Could not recreate flight",
                    str(ex),
                    QMessageBox.StandardButton.Ok,
                )
            for member in self.flight.iter_members():
                if not member.loadout.is_custom:
                    member.loadout = Loadout.default_for(self.flight)
                    self.loadout_changed.emit()
            self.flight_waypoint_list.update_list()
            self.on_change()

    def _is_bulk_editable(self, waypoint: FlightWaypoint) -> bool:
        # Skip pattern waypoints and any AGL/ground-referenced point (takeoff and
        # landing are RADIO, alt 0) so the bulk set only moves the en-route legs.
        if waypoint.waypoint_type in self.BULK_ALTITUDE_SKIP_TYPES:
            return False
        return waypoint.alt_type != "RADIO"

    def _default_bulk_altitude(self) -> int:
        # Seed the spinner with the highest en-route altitude already planned so the
        # control opens on a sensible value rather than zero.
        altitudes = [
            round(wpt.alt.feet)
            for wpt in self.flight.flight_plan.waypoints
            if self._is_bulk_editable(wpt)
        ]
        return max(altitudes, default=0)

    def on_apply_bulk_altitude(self) -> None:
        altitude = feet(self.bulk_altitude.value())
        changed = False
        for waypoint in self.flight.flight_plan.waypoints:
            if self._is_bulk_editable(waypoint):
                waypoint.alt = altitude
                changed = True
        if changed:
            self.on_change()

    def on_move_waypoint(self, direction: int) -> None:
        selected = self.flight_waypoint_list.selectedIndexes()
        if not selected:
            return
        row = selected[0].row()
        if row == 0:
            # The departure/takeoff waypoint is fixed.
            return
        waypoint = self.flight.flight_plan.waypoints[row]
        if not self.flight.flight_plan.move_waypoint(waypoint, direction):
            QMessageBox.information(
                self,
                "Cannot move waypoint",
                "This waypoint can't move past a fixed point in a standard flight "
                "plan. To reorder freely, convert this flight to a custom plan using "
                "Convert to custom plan in the Advanced section.",
            )
            return
        new_row = row + direction
        self.on_change()
        self.flight_waypoint_list.selectionModel().setCurrentIndex(
            self.flight_waypoint_list.model.index(new_row, 0),
            QItemSelectionModel.SelectionFlag.ClearAndSelect,
        )

    def on_reset_tot(self) -> None:
        self.flight.flight_plan.clear_manual_timing()
        self.on_change()

    def on_tot_changed(self) -> None:
        self.on_change()
        self.maybe_warn_escort_drift()

    def maybe_warn_escort_drift(self) -> None:
        """Remind the player that manual timing won't move the package's escorts.

        Escort start/end times are derived from the package's automatic ToTs, so a flight
        with manual waypoint times can arrive out of sync with its escort. Warn once per
        manual-timing session when the package actually contains an escort.
        """
        if self._escort_warning_shown or not self.flight.manually_timed:
            return
        if not any(
            f.flight_type.provides_escort_coverage for f in self.package.flights
        ):
            return
        self._escort_warning_shown = True
        QMessageBox.warning(
            self,
            "Escort timing may drift",
            "This flight now has manually-timed waypoints that are decoupled from the "
            "package TOT. Escort coordination still uses the package's automatic timing, "
            "so the escort may arrive at the wrong time. Adjust the escort flight's "
            "timing to match, or reset this flight's ToT to auto.",
        )

    def refresh_manual_tot_widgets(self) -> None:
        manual = self.flight.manually_timed
        self.manual_tot_label.setVisible(manual)
        self.reset_tot_button.setVisible(manual)
        if not manual:
            # Timing reverted to auto (reset button or a reorder); re-arm the warning so
            # the next manual-timing session prompts again.
            self._escort_warning_shown = False

    def on_change(self):
        self.flight_waypoint_list.update_list()
        self.flight_waypoint_list.on_changed()
        self.update()
        self.refresh_manual_tot_widgets()
        self.refresh_plan_type()
