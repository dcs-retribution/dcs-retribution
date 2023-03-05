from __future__ import annotations

from typing import Type

from .formationattack import (
    FormationAttackBuilder,
    FormationAttackFlightPlan,
    FormationAttackLayout,
)
from .waypointbuilder import WaypointBuilder


class EscortFlightPlan(FormationAttackFlightPlan):
    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder


class Builder(FormationAttackBuilder[EscortFlightPlan, FormationAttackLayout]):
    def layout(self) -> FormationAttackLayout:
        assert self.package.waypoints is not None

        builder = WaypointBuilder(self.flight, self.coalition)
        ingress, target = builder.escort(
            self.package.waypoints.ingress, self.package.target
        )
        ingress.only_for_player = True
        target.only_for_player = True
        hold = builder.hold(self._hold_point())
        join = builder.join(self.package.waypoints.join)
        split = builder.split(self.package.waypoints.split)
        refuel = builder.refuel(self.package.waypoints.refuel)
        initial = builder.escort_hold(
            self.package.waypoints.initial, self.doctrine.ingress_altitude
        )

        return FormationAttackLayout(
            departure=builder.takeoff(self.flight.departure),
            hold=hold,
            nav_to=builder.nav_path(
                hold.position, join.position, self.doctrine.ingress_altitude
            ),
            join=join,
            ingress=ingress,
            initial=initial,
            targets=[target],
            split=split,
            refuel=refuel,
            nav_from=builder.nav_path(
                refuel.position,
                self.flight.arrival.position,
                self.doctrine.ingress_altitude,
            ),
            arrival=builder.land(self.flight.arrival),
            divert=builder.divert(self.flight.divert),
            bullseye=builder.bullseye(),
        )

    def build(self) -> EscortFlightPlan:
        return EscortFlightPlan(self.flight, self.layout())
