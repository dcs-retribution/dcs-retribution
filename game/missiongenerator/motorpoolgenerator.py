from __future__ import annotations

from typing import Any, Type

from dcs.statics import Fortification
from dcs.task import OptAlarmState, OptROE
from dcs.unitgroup import MovingGroup, VehicleGroup
from dcs.unittype import VehicleType

from game.missiongenerator.tgogenerator import GroundObjectGenerator
from game.point_with_heading import PointWithHeading
from game.theater.theatergroundobject import MotorpoolGroundObject
from game.theater.theatergroup import TheaterUnit

# The reserve vehicles are laid in a grid that grows in the garage's local +x/+y
# from the TGO position (motorpoolpopulator._make_unit: slot 0 sits exactly on
# tgo.position, then the grid is rotated to the garage heading). Offsetting the
# depot in the opposite (-x/-y) local corner — and rotating it by the same heading —
# guarantees it never shares a spawn point with a vehicle whatever the orientation
# (DCS silently drops overlapping spawns). The magnitude just adds clearance for the
# building + vehicle footprints; it does not need to exceed the grid's reach (the
# direction does the work).
_DEPOT_OFFSET_M = 50.0


class MotorpoolGenerator(GroundObjectGenerator):
    """Renders a MotorpoolGroundObject as parked, unmanned reserve vehicles:
    present and strikeable, but they hold fire and never move. Their deaths are
    registered as motorpool losses (a distinct loss category that decrements
    base.armor 1:1 but does not count toward front-line battle impact)."""

    def set_alarm_state(self, group: MovingGroup[Any], force_red: bool = False) -> None:
        # Always green regardless of perf_red_alert_state or force_red — parked, not alert.
        group.points[0].tasks.append(OptAlarmState(1))

    def _register_theater_unit(self, theater_unit: TheaterUnit, dcs_unit: Any) -> None:
        # Motorpool units register as motorpool losses (see generate), NOT as
        # theater objects — theater-object deaths do not touch base.armor.
        return

    def enable_eplrs(self, group: VehicleGroup, unit_type: Type[VehicleType]) -> None:
        # Unmanned parked vehicles must not broadcast datalink/targeting data to
        # coalition AI, so suppress the EPLRS task the base generator would add.
        return

    def _set_passive(self, group: VehicleGroup) -> None:
        group.points[0].tasks.append(
            OptROE(OptROE.Values.WeaponHold)
        )  # won't return fire
        for unit in group.units:
            unit.player_can_drive = False  # not manned

    def _spawn_depot(self) -> None:
        # Depot structure: present whenever the motorpool renders (even at zero
        # reserve); skipped only when the whole TGO is culled, since generate()
        # returns before calling this. Unregistered on purpose — it is inert scenery,
        # so bombing it produces no debrief loss and never touches base.armor. It
        # respawns every mission (population is ephemeral). Placed clear of the
        # vehicle grid (see _DEPOT_OFFSET_M) so it never collides with a parked unit.
        origin = self.ground_object.position
        heading = self.ground_object.heading
        depot_pos = PointWithHeading.from_point(
            origin.new_in_same_map(
                origin.x - _DEPOT_OFFSET_M, origin.y - _DEPOT_OFFSET_M
            ),
            heading,
        )
        # Rotate the depot corner about the origin by the garage heading so it stays
        # opposite the (also-rotated) vehicle grid at any orientation.
        depot_pos.rotate(origin, heading)
        self.m.static_group(
            country=self.country,
            name=f"{self.ground_object.name} Depot",
            _type=Fortification.Garage_A,
            position=depot_pos,
            heading=heading.degrees,
        )

    def generate(self) -> None:
        if self.culled:
            return
        assert isinstance(self.ground_object, MotorpoolGroundObject)
        self._spawn_depot()
        for group in self.ground_object.groups:
            vehicle_units = [u for u in group.units if u.is_vehicle and u.alive]
            if not vehicle_units:
                continue
            dcs_group = self.create_vehicle_group(group.group_name, vehicle_units)
            self._set_passive(dcs_group)
            unit_type = self.ground_object.motorpool_unit_types[group.id]
            self.unit_map.add_motorpool_units(
                dcs_group, self.ground_object.control_point, unit_type
            )
