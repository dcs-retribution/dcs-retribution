from dcs.point import MovingPoint
from dcs.task import (
    ActivateBeaconCommand,
    RecoveryTanker,
    Tanker,
    SetUnlimitedFuelCommand,
)

from game.ato import FlightType
from game.utils import feet, knots
from .pydcswaypointbuilder import PydcsWaypointBuilder


class RecoveryTankerBuilder(PydcsWaypointBuilder):
    def add_tasks(self, waypoint: MovingPoint) -> None:

        assert self.flight.flight_type == FlightType.REFUELING

        # Unlimited fuel option : disable at racetrack start. Must be first option to work.
        if self.flight.squadron.coalition.game.settings.ai_unlimited_fuel:
            if waypoint.tasks and isinstance(
                waypoint.tasks[0], SetUnlimitedFuelCommand
            ):
                waypoint.tasks[0] = SetUnlimitedFuelCommand(False)
            else:
                waypoint.tasks.insert(0, SetUnlimitedFuelCommand(False))

        clouds = self.flight.squadron.coalition.game.conditions.weather.clouds
        waypoint.add_task(Tanker())
        group_id = self._get_carrier_group_id()
        speed = knots(250).meters_per_second
        altitude = feet(6000).meters
        if clouds is not None:
            if abs(clouds.base - altitude) < feet(1000).meters:
                altitude = clouds.base - feet(1000).meters
            if altitude < feet(2000).meters:
                altitude = clouds.base + feet(6000).meters

        # Last waypoint has index of 1.
        # Give the tanker a end condition of the last carrier waypoint.
        # If the carrier ever gets more than one waypoint this approach needs to change.
        last_waypoint = 2
        recovery_tanker = RecoveryTanker(group_id, speed, altitude, last_waypoint)

        waypoint.add_task(recovery_tanker)

        self.configure_tanker_tacan(waypoint)

    def _get_carrier_group_id(self) -> int:
        name = self.package.target.name
        carrier_position = self.package.target.position
        for carrier in self.mission_data.carriers:
            if carrier.position == carrier_position:
                return carrier.group_id
        raise RuntimeError(
            f"Could not find a carrier in the mission matching {name} at "
            f"({carrier_position.x}, {carrier_position.y})"
        )

    def configure_tanker_tacan(self, waypoint: MovingPoint) -> None:
        tanker_info = self.mission_data.tankers[-1]
        tacan = tanker_info.tacan
        if self.flight.unit_type.dcs_unit_type.tacan and tacan:
            if self.flight.tcn_name is None:
                cs = tanker_info.callsign[:-2]
                csn = tanker_info.callsign[-1]
                tacan_callsign = {
                    "Texaco": "TX",
                    "Arco": "AC",
                    "Shell": "SH",
                }.get(cs)
                if tacan_callsign:
                    tacan_callsign = tacan_callsign + csn
                else:
                    tacan_callsign = cs[0:2] + csn
            else:
                tacan_callsign = self.flight.tcn_name

            waypoint.add_task(
                ActivateBeaconCommand(
                    tacan.number,
                    tacan.band.value,
                    tacan_callsign,
                    bearing=True,
                    unit_id=self.group.units[0].id,
                    aa=True,
                )
            )
