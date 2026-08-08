import logging
from typing import Iterable, List, Optional

from PySide6.QtCore import Signal, Qt, QModelIndex
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
from game.ato.flightplans.waypointbuilder import AGL_TRANSITION_ALT, WaypointBuilder
from game.ato.flighttype import FlightType
from game.ato.flightwaypoint import AltitudeReference, FlightWaypoint
from game.ato.flightwaypointtype import FlightWaypointType
from game.utils import Distance, feet
from game.ato.loadouts import Loadout
from game.ato.package import Package
from game.theater import Player
from qt_ui.windows.mission.flight.waypoints.QFlightWaypointList import (
    QFlightWaypointList,
)
from qt_ui.windows.mission.flight.waypoints.QPredefinedWaypointSelectionWindow import (
    QPredefinedWaypointSelectionWindow,
)

#: Lowest altitude the bulk setter offers. Zero is a valid spin-box entry but never a
#: valid answer -- it drops the whole route to sea level -- and with the 1,000 ft step
#: every other reachable value is a round thousand anyway. Per-waypoint editing still
#: reaches any altitude, which is where a helo's sub-1,000 ft cruise gets set.
BULK_ALTITUDE_FLOOR_FT = 1000

#: Waypoint types the bulk setter must not move even though they carry a planned
#: altitude. Pickup and dropoff zones are planned at the helo's approach altitude, so
#: raising them with the rest of the route leaves the aircraft over its landing zone
#: at cruise with nothing to unload onto.
#:
#: Every *other* ground point -- takeoff, landing, cargo stop, bullseye, an on-map
#: divert field, and all three target types -- is planner-seeded at 0 ft, so
#: bulk_editable()'s deck rule already leaves it alone. A type only needs naming here
#: when its planned altitude is non-zero.
BULK_ALTITUDE_SKIP_TYPES = frozenset(
    {
        FlightWaypointType.PICKUP_ZONE,
        FlightWaypointType.DROPOFF_ZONE,
    }
)


def bulk_editable(waypoint: FlightWaypoint) -> bool:
    """Whether the bulk altitude setter should move this waypoint.

    A waypoint planned on the deck marks a place on the ground -- the field, the
    target, the bullseye -- and a cruise altitude written onto it means nothing. A
    waypoint planned at an altitude is a height to fly, so it moves with the route.

    Reading the planned altitude rather than enumerating every en-route type is also
    what makes the control work on low-level plans. The AGL exclusion this replaced
    skipped every RADIO waypoint, and the planner marks everything at or below
    AGL_TRANSITION_ALT (plus every helo leg) RADIO -- so "Apply to all" did nothing at
    all on a helo or a low-level plan, and skipped the CAS FLOT boundaries on every
    plan, since waypointbuilder.cas() hardcodes RADIO at any altitude.
    """
    if waypoint.waypoint_type in BULK_ALTITUDE_SKIP_TYPES:
        return False
    return waypoint.alt.feet > 0


def bulk_alt_type(altitude: Distance, is_helo: bool) -> AltitudeReference:
    """The altitude reference the planner would give a leg at this altitude.

    The Alt Type column is read-only, so the bulk setter has to leave a coherent
    reference behind: a flight that comes out with some legs AGL and some MSL is
    flying at two different real altitudes and the player cannot reconcile it by hand.
    Follows waypointbuilder's own rule, so a bulk-set route matches a freshly planned
    one at the same altitude.
    """
    if is_helo or altitude.feet <= AGL_TRANSITION_ALT:
        return "RADIO"
    return "BARO"


class QFlightWaypointTab(QFrame):
    loadout_changed = Signal()

    def __init__(self, game: Game, package: Package, flight: Flight):
        super(QFlightWaypointTab, self).__init__()
        self.game = game
        self.coalition = game.coalition_for(player=Player.BLUE)
        self.package = package
        self.flight = flight

        self.flight_waypoint_list: Optional[QFlightWaypointList] = None
        self.rtb_waypoint: Optional[QPushButton] = None
        self.delete_selected: Optional[QPushButton] = None
        self.add_nav_waypoint: Optional[QPushButton] = None
        self.open_fast_waypoint_button: Optional[QPushButton] = None
        self.recreate_buttons: List[QPushButton] = []
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()

        self.flight_waypoint_list = QFlightWaypointList(self.package, self.flight)
        layout.addWidget(self.flight_waypoint_list, 0, 0)

        rlayout = QVBoxLayout()
        layout.addLayout(rlayout, 0, 1)

        rlayout.addWidget(QLabel("<strong>Altitude :</strong>"))
        rlayout.addWidget(QLabel("<small>Set all en-route waypoints</small>"))
        bulk_alt_layout = QHBoxLayout()
        self.bulk_altitude = QSpinBox()
        self.bulk_altitude.setMinimum(BULK_ALTITUDE_FLOOR_FT)
        self.bulk_altitude.setMaximum(40000)
        self.bulk_altitude.setSingleStep(1000)
        self.bulk_altitude.setValue(self._default_bulk_altitude())
        self.bulk_altitude.setSuffix(" ft")
        self.bulk_altitude.setToolTip(
            "Apply this altitude to every waypoint that is flown at an altitude. "
            "Waypoints planned on the deck -- takeoff, landing, divert, target and "
            "bullseye -- and helo landing zones are left where they are. AGL or MSL "
            f"follows the planner's own rule: AGL at or below {AGL_TRANSITION_ALT:,} "
            "ft (and on helicopters), MSL above it."
        )
        bulk_alt_layout.addWidget(self.bulk_altitude)
        self.apply_bulk_altitude = QPushButton("Apply to all")
        self.apply_bulk_altitude.clicked.connect(self.on_apply_bulk_altitude)
        bulk_alt_layout.addWidget(self.apply_bulk_altitude)
        rlayout.addLayout(bulk_alt_layout)

        rlayout.addWidget(QLabel("<strong>Generator :</strong>"))
        rlayout.addWidget(QLabel("<small>AI compatible</small>"))

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

        rlayout.addWidget(QLabel("<strong>Advanced : </strong>"))
        rlayout.addWidget(QLabel("<small>Do not use for AI flights</small>"))

        self.rtb_waypoint = QPushButton("Add RTB Waypoint")
        self.rtb_waypoint.clicked.connect(self.on_rtb_waypoint)
        rlayout.addWidget(self.rtb_waypoint)

        self.delete_selected = QPushButton("Delete Selected")
        self.delete_selected.clicked.connect(self.on_delete_waypoint)
        rlayout.addWidget(self.delete_selected)

        self.open_fast_waypoint_button = QPushButton("Add Waypoint")
        self.open_fast_waypoint_button.clicked.connect(self.on_fast_waypoint)
        rlayout.addWidget(self.open_fast_waypoint_button)
        rlayout.addStretch()
        self.setLayout(layout)

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
            "Degrade flight-plan?",
            "Deleting the selected waypoint(s) will require degradation to a custom flight-plan. "
            "A custom flight-plan will no longer respect the TOTs of the package.<br><br>"
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
        if not waypoints:
            return
        self.flight.flight_plan.layout.custom_waypoints.extend(waypoints)
        self.add_rows(len(list(waypoints)))

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

    def _default_bulk_altitude(self) -> int:
        # Seed the spinner with the highest altitude already planned so the control
        # opens on a sensible value. The spin box clamps to BULK_ALTITUDE_FLOOR_FT.
        altitudes = [
            round(wpt.alt.feet)
            for wpt in self.flight.flight_plan.waypoints
            if bulk_editable(wpt)
        ]
        return max(altitudes, default=0)

    def on_apply_bulk_altitude(self) -> None:
        altitude = feet(self.bulk_altitude.value())
        alt_type = bulk_alt_type(altitude, self.flight.is_helo)
        changed = False
        for waypoint in self.flight.flight_plan.waypoints:
            if bulk_editable(waypoint):
                waypoint.alt = altitude
                waypoint.alt_type = alt_type
                changed = True
        if changed:
            self.on_change()

    def on_change(self):
        self.flight_waypoint_list.update_list()
        self.flight_waypoint_list.on_changed()
        self.update()
