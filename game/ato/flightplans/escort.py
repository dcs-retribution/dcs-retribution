from __future__ import annotations

from typing import Type

from .airassault import AirAssaultLayout
from .airlift import AirliftLayout
from .formationattack import (
    FormationAttackBuilder,
    FormationAttackFlightPlan,
    FormationAttackLayout,
)
from .waypointbuilder import WaypointBuilder
from .. import FlightType


class EscortFlightPlan(FormationAttackFlightPlan):
    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder


class Builder(FormationAttackBuilder[EscortFlightPlan, FormationAttackLayout]):
    def layout(self) -> FormationAttackLayout:
        assert self.package.waypoints is not None

        builder = WaypointBuilder(self.flight)
        ingress, target = builder.escort(
            self.package.waypoints.ingress, self.package.target
        )
        ingress.only_for_player = True
        target.only_for_player = True
        hold = None
        if not self.flight.is_helo:
            hold = builder.hold(self._hold_point())

        join_pos = (
            self.package.waypoints.ingress
            if self.flight.is_helo
            else self.package.waypoints.join
        )
        join = builder.join(join_pos)

        split = builder.split(self._get_split())

        is_helo = builder.flight.is_helo
        initial = builder.escort_hold(
            target.position if is_helo else self.package.waypoints.initial,
        )

        pf = self.package.primary_flight
        if pf and pf.flight_type in [FlightType.AIR_ASSAULT, FlightType.TRANSPORT]:
            layout = pf.flight_plan.layout
            assert isinstance(layout, AirAssaultLayout) or isinstance(
                layout, AirliftLayout
            )
            if isinstance(layout, AirliftLayout):
                ascent = layout.pickup_ascent or layout.drop_off_ascent
                assert ascent is not None
                join = builder.join(ascent.position)
                if layout.pickup and layout.drop_off_ascent:
                    join = builder.join(layout.drop_off_ascent.position)
            split = builder.split(layout.arrival.position)
            if layout.drop_off:
                initial = builder.escort_hold(
                    layout.drop_off.position,
                )

        refuel = self._build_refuel(builder)

        departure = builder.takeoff(self.flight.departure)
        nav_to = builder.nav_path(
            hold.position if hold else departure.position,
            join.position,
            builder.get_cruise_altitude,
        )

        nav_from = builder.nav_path(
            refuel.position if refuel else split.position,
            self.flight.arrival.position,
            builder.get_cruise_altitude,
        )

        return FormationAttackLayout(
            departure=departure,
            hold=hold,
            nav_to=nav_to,
            join=join,
            ingress=ingress,
            initial=initial,
            targets=[target],
            split=split,
            refuel=refuel,
            nav_from=nav_from,
            arrival=builder.land(self.flight.arrival),
            divert=builder.divert(self.flight.divert),
            bullseye=builder.bullseye(),
            custom_waypoints=list(),
        )

    def build(self, dump_debug_info: bool = False) -> EscortFlightPlan:
        return EscortFlightPlan(self.flight, self.layout())
