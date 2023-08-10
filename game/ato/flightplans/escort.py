from __future__ import annotations

from datetime import timedelta
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
from ..traveltime import TravelTime, GroundSpeed
from ...utils import feet


class EscortFlightPlan(FormationAttackFlightPlan):
    @property
    def push_time(self) -> timedelta:
        hold2join_time = (
            TravelTime.between_points(
                self.layout.hold.position,
                self.layout.join.position,
                GroundSpeed.for_flight(self.flight, self.layout.hold.alt),
            )
            if self.layout.hold is not None
            else timedelta(0)
        )
        return self.join_time - hold2join_time

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
        if not self.primary_flight_is_air_assault:
            hold = builder.hold(self._hold_point())
        elif self.package.primary_flight is not None:
            fp = self.package.primary_flight.flight_plan
            assert isinstance(fp.layout, AirAssaultLayout)
            assert fp.layout.pickup is not None
            hold = builder.hold(fp.layout.pickup.position)

        join = builder.join(self.package.waypoints.join)
        split = builder.split(self.package.waypoints.split)

        ingress_alt = self.doctrine.ingress_altitude
        is_helo = builder.flight.is_helo
        heli_alt = feet(self.coalition.game.settings.heli_combat_alt_agl)
        initial = builder.escort_hold(
            target.position if is_helo else self.package.waypoints.initial,
            min(heli_alt, ingress_alt) if is_helo else ingress_alt,
        )

        pf = self.package.primary_flight
        if pf and pf.flight_type in [FlightType.AIR_ASSAULT, FlightType.TRANSPORT]:
            layout = pf.flight_plan.layout
            assert isinstance(layout, AirAssaultLayout) or isinstance(
                layout, AirliftLayout
            )
            if isinstance(layout, AirliftLayout):
                join = builder.join(layout.departure.position)
            else:
                join = builder.join(layout.ingress.position)
            if layout.pickup:
                join = builder.join(layout.pickup.position)
            split = builder.split(layout.arrival.position)
            if layout.drop_off:
                initial = builder.escort_hold(
                    layout.drop_off.position,
                    min(feet(200), ingress_alt)
                    if builder.flight.is_helo
                    else ingress_alt,
                )

        refuel = self._build_refuel(builder)

        departure = builder.takeoff(self.flight.departure)
        nav_to = builder.nav_path(
            hold.position if hold else departure.position,
            join.position,
            self.doctrine.ingress_altitude,
        )

        nav_from = builder.nav_path(
            refuel.position if refuel else split.position,
            self.flight.arrival.position,
            self.doctrine.ingress_altitude,
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
        )

    def build(self, dump_debug_info: bool = False) -> EscortFlightPlan:
        return EscortFlightPlan(self.flight, self.layout())
