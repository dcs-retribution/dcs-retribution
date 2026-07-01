from __future__ import annotations

from typing import Any, Type

from dcs.task import OptAlarmState, OptROE
from dcs.unitgroup import MovingGroup, VehicleGroup
from dcs.unittype import VehicleType

from game.missiongenerator.tgogenerator import GroundObjectGenerator
from game.theater.theatergroundobject import MotorpoolGroundObject
from game.theater.theatergroup import TheaterUnit


class MotorpoolGenerator(GroundObjectGenerator):
    """Renders a MotorpoolGroundObject as parked, unmanned reserve vehicles:
    present and strikeable, but they hold fire and never move. Their deaths are
    registered as motorpool losses (a distinct loss category that decrements
    base.armor 1:1 but does not count toward front-line battle impact)."""

    def set_alarm_state(self, group: MovingGroup[Any]) -> None:
        # Always green regardless of perf_red_alert_state — parked, not alert.
        group.points[0].tasks.append(OptAlarmState(1))

    def _register_theater_unit(self, theater_unit: TheaterUnit, dcs_unit: Any) -> None:
        # Motorpool units register as motorpool losses (see generate), NOT as
        # theater objects — theater-object deaths do not touch base.armor.
        return

    def enable_eplrs(self, group: VehicleGroup, unit_type: Type[VehicleType]) -> None:
        # Unmanned parked vehicles must not broadcast datalink/targeting data to
        # coalition AI, so suppress the EPLRS task the base generator would add.
        return

    def _passivate(self, group: VehicleGroup) -> None:
        group.points[0].tasks.append(
            OptROE(OptROE.Values.WeaponHold)
        )  # won't return fire
        for unit in group.units:
            unit.player_can_drive = False  # not manned

    def generate(self) -> None:
        if self.culled:
            return
        assert isinstance(self.ground_object, MotorpoolGroundObject)
        for group in self.ground_object.groups:
            vehicle_units = [u for u in group.units if u.is_vehicle and u.alive]
            if not vehicle_units:
                continue
            dcs_group = self.create_vehicle_group(group.group_name, vehicle_units)
            self._passivate(dcs_group)
            unit_type = self.ground_object.motorpool_unit_types[group.id]
            self.unit_map.add_motorpool_units(
                dcs_group, self.ground_object.control_point, unit_type
            )
