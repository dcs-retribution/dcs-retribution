from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal, TYPE_CHECKING, Any, Dict, Optional

from dcs import Point

from game.ato.flightwaypointtype import FlightWaypointType
from game.theater.theatergroup import TheaterUnit
from game.utils import Distance, meters

if TYPE_CHECKING:
    from game.theater import ControlPoint

AltitudeReference = Literal["BARO", "RADIO"]


@dataclass
class FlightWaypoint:
    name: str
    waypoint_type: FlightWaypointType
    position: Point
    alt: Distance = meters(0)
    alt_type: AltitudeReference = "BARO"
    control_point: ControlPoint | None = None

    # TODO: Merge with pretty_name.
    # Only used in the waypoint list in the flight edit page. No sense
    # having three names. A short and long form is enough.
    description: str = ""

    targets: list[TheaterUnit] = field(default_factory=list)
    obj_name: str = ""
    pretty_name: str = ""
    # User override; None = follow the auto names. Invariant: never "" — apply_name_edit
    # stores None instead of an empty string, so `custom_name or pretty_name` is safe.
    custom_name: str | None = None
    only_for_player: bool = False
    flyover: bool = False

    # The minimum amount of fuel remaining at this waypoint in pounds.
    min_fuel: float | None = None

    # These are set very late by the air conflict generator (part of mission
    # generation). We do it late so that we don't need to propagate changes
    # to waypoint times whenever the player alters the package TOT or the
    # flight's offset in the UI.
    tot: datetime | None = None
    departure_time: datetime | None = None

    @property
    def x(self) -> float:
        return self.position.x

    @property
    def y(self) -> float:
        return self.position.y

    @property
    def display_name(self) -> str:
        """User-facing name for Retribution displays: the override if the player set
        one, otherwise the auto pretty_name."""
        return self.custom_name or self.pretty_name

    def apply_name_edit(self, raw: str) -> None:
        """Record (or clear) a user rename from the flight-plan list cell.

        The cell text is "{:<16}".format(display_name), so it arrives padded; strip it.
        Only a value that differs from the auto pretty_name is a real override — a blank
        or back-to-auto entry reverts so the waypoint resumes following its auto name.
        pretty_name is stripped on the other side of the comparison too: saves made before
        this change carry pretty_name padded by the old on_changed handler, and we must not
        read that padding as a difference (it would set a phantom override).
        """
        stripped = raw.strip()
        self.custom_name = (
            stripped if stripped and stripped != self.pretty_name.strip() else None
        )

    def __hash__(self) -> int:
        return hash(id(self))

    def __setstate__(self, state: Dict[str, Any]) -> None:
        # Saves made before custom_name existed won't carry the key; default it so
        # attribute access on a reloaded waypoint is safe.
        state.setdefault("custom_name", None)
        self.__dict__.update(state)

    def __deepcopy__(self, memo: Optional[Dict[int, Any]] = None) -> FlightWaypoint:
        obj = FlightWaypoint(self.name, self.waypoint_type, self.position)
        for attr in dir(self):
            if attr == "control_point":
                obj.control_point = self.control_point
            elif attr == "targets":
                obj.targets = self.targets
            elif "__" in attr or attr not in obj.__dataclass_fields__:
                continue
            else:
                attr_copy = deepcopy(getattr(self, attr))
                setattr(obj, attr, attr_copy)
        return obj
