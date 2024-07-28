from __future__ import annotations

import typing
from datetime import timedelta
from typing import TYPE_CHECKING, Any

from dcs.countries import countries_by_name

from game.ato import FlightType
from game.ato.flightplans.formation import FormationLayout
from game.ato.flightplans.waypointbuilder import WaypointBuilder
from game.ato.packagewaypoints import PackageWaypoints
from game.data.doctrine import MODERN_DOCTRINE, COLDWAR_DOCTRINE, WWII_DOCTRINE
from game.dcs.aircrafttype import AircraftType
from game.theater import ParkingType, SeasonalConditions

if TYPE_CHECKING:
    from game import Game
    from game.ato import Flight


def try_set_attr(obj: Any, attr_name: str, val: Any = None) -> None:
    if not hasattr(obj, attr_name):
        setattr(obj, attr_name, val)


class Migrator:
    def __init__(self, game: Game, is_liberation: bool):
        self.game = game
        self.is_liberation = is_liberation
        self._migrate_game()

    def _migrate_game(self) -> None:
        self._update_doctrine()
        self._update_control_points()
        self._update_packagewaypoints()
        self._update_package_attributes()
        self._update_factions()
        self._update_flights()
        self._update_squadrons()
        self._release_untasked_flights()
        self._update_weather()
        self._update_tgos()

    def _update_doctrine(self) -> None:
        doctrines = [
            MODERN_DOCTRINE,
            COLDWAR_DOCTRINE,
            WWII_DOCTRINE,
        ]
        for c in self.game.coalitions:
            if c.faction.doctrine.__dict__ in [d.__dict__ for d in doctrines]:
                continue
            found = False
            for d in doctrines:
                if c.faction.doctrine.max_patrol_altitude == d.max_patrol_altitude:
                    c.faction.doctrine = d
                    found = True
                    break
            if not found:
                c.faction.doctrine = MODERN_DOCTRINE

    def _update_packagewaypoints(self) -> None:
        for c in self.game.coalitions:
            for p in c.ato.packages:
                if p.waypoints and not hasattr(p.waypoints, "initial"):
                    p.waypoints = PackageWaypoints.create(p, c, False)

    def _update_package_attributes(self) -> None:
        for c in self.game.coalitions:
            for p in c.ato.packages:
                try_set_attr(p, "custom_name")
                try_set_attr(p, "frequency")
                if isinstance(p.time_over_target, timedelta):  # type: ignore
                    p.time_over_target = (  # type: ignore
                        p.time_over_target + self.game.conditions.start_time
                    )

    def _update_control_points(self) -> None:
        is_sinai = self.game.theater.terrain.name == "SinaiMap"
        for cp in self.game.theater.controlpoints:
            cp.release_parking_slots()
            is_carrier = cp.is_carrier
            is_lha = cp.is_lha
            is_fob = cp.category == "fob"
            radio_configurable = is_carrier or is_lha or is_fob
            if radio_configurable:
                try_set_attr(cp, "frequency")
            if is_carrier or is_lha:
                try_set_attr(cp, "tacan")
                try_set_attr(cp, "tcn_name")
                try_set_attr(cp, "icls_channel")
                try_set_attr(cp, "icls_name")
                try_set_attr(cp, "link4")
            try_set_attr(cp, "convoy_spawns", {})
            try_set_attr(cp, "ground_spawns", [])
            try_set_attr(cp, "ground_spawns_roadbase", [])
            try_set_attr(cp, "helipads_quad", [])
            try_set_attr(cp, "helipads_invisible", [])
            try_set_attr(cp, "ground_spawns_large", [])
            if (
                cp.dcs_airport and is_sinai and cp.dcs_airport.id == 20
            ):  # fix for Hatzor
                beacons = cp.dcs_airport.beacons
                faulty_beacon = [x for x in beacons if x.id == "airfield20_0"]
                if faulty_beacon:
                    beacons.remove([x for x in beacons if x.id == "airfield20_0"][0])

    def _update_flight_plan(self, f: Flight) -> None:
        layout = f.flight_plan.layout
        try_set_attr(layout, "nav_to", [])
        try_set_attr(layout, "nav_from", [])
        try_set_attr(layout, "custom_waypoints", [])
        if f.flight_type == FlightType.CAS:
            try_set_attr(layout, "ingress", None)
        if isinstance(layout, FormationLayout):
            if not layout.join and f.package.waypoints:
                builder = WaypointBuilder(f, [])
                layout.join = builder.join(f.package.waypoints.join)

    def _update_flights(self) -> None:
        to_remove = []
        for f in self.game.db.flights.objects.values():
            try_set_attr(f, "frequency")
            try_set_attr(f, "tacan")
            try_set_attr(f, "tcn_name")
            try_set_attr(f, "fuel", f.unit_type.max_fuel)
            try_set_attr(f, "plane_altitude_offset", 0)
            try_set_attr(f, "use_same_livery_for_all_members", True)
            if f.package in f.squadron.coalition.ato.packages:
                self._update_flight_plan(f)
            else:
                to_remove.append(f.id)
            for m in f.roster.members:
                try_set_attr(m, "livery", None)
        for fid in to_remove:
            self.game.db.flights.remove(fid)

    def _release_untasked_flights(self) -> None:
        for cp in self.game.theater.controlpoints:
            for s in cp.squadrons:
                count = 0
                for f in s.flight_db.objects.values():
                    if f.squadron == s:
                        count += f.count
                s.return_all_pilots_and_aircraft()
                new_claim = min(count, s.owned_aircraft)
                s.claim_inventory(new_claim)
                for i in range(new_claim):
                    s.claim_available_pilot()

    def _update_squadrons(self) -> None:
        country_dict = {
            "Netherlands": "The Netherlands",
            "CHN": "China",
        }
        # Squadrons
        for cp in self.game.theater.controlpoints:
            for s in cp.squadrons:
                preferred_task = max(
                    s.aircraft.task_priorities,
                    key=lambda x: s.aircraft.task_priorities[x],
                )
                try_set_attr(s, "primary_task", preferred_task)
                try_set_attr(s, "max_size", 12)
                try_set_attr(s, "radio_presets", {})
                try_set_attr(s, "livery_set", [])
                s.aircraft = AircraftType.named(s.aircraft.variant_id)
                if isinstance(s.country, str):
                    c = country_dict.get(s.country, s.country)
                    s.country = countries_by_name[c]()

                # code below is used to fix corruptions wrt overpopulation
                parking_type = ParkingType().from_squadron(s)
                if (
                    s.owned_aircraft < 0
                    or s.location.unclaimed_parking(parking_type) < 0
                ):
                    s.owned_aircraft = max(
                        0, s.location.unclaimed_parking(parking_type) + s.owned_aircraft
                    )

                if self.is_liberation:
                    s.set_auto_assignable_mission_types(s.auto_assignable_mission_types)
        # SquadronDefs
        for coa in self.game.coalitions:
            for ac, sdefs in coa.air_wing.squadron_defs.items():
                for sdef in sdefs:
                    try_set_attr(sdef, "radio_presets", {})

    @typing.no_type_check
    def _update_factions(self) -> None:
        for c in self.game.coalitions:
            if isinstance(c.faction.country, str):
                c.faction.country = countries_by_name[c.faction.country]()
            if isinstance(c.faction.aircraft, list):
                c.faction.aircraft = set(c.faction.aircraft)
            if isinstance(c.faction.awacs, list):
                c.faction.awacs = set(c.faction.awacs)
            if isinstance(c.faction.tankers, list):
                c.faction.tankers = set(c.faction.tankers)
            if isinstance(c.faction.frontline_units, list):
                c.faction.frontline_units = set(c.faction.frontline_units)
            if isinstance(c.faction.artillery_units, list):
                c.faction.artillery_units = set(c.faction.artillery_units)
            if isinstance(c.faction.infantry_units, list):
                c.faction.infantry_units = set(c.faction.infantry_units)
            if isinstance(c.faction.logistics_units, list):
                c.faction.logistics_units = set(c.faction.logistics_units)
            if isinstance(c.faction.air_defense_units, list):
                c.faction.air_defense_units = set(c.faction.air_defense_units)
            if isinstance(c.faction.missiles, list):
                c.faction.missiles = set(c.faction.missiles)
            if isinstance(c.faction.naval_units, list):
                c.faction.naval_units = set(c.faction.naval_units)
            if isinstance(c.faction.building_set, list):
                c.faction.building_set = set(c.faction.building_set)

    def _update_weather(self) -> None:
        a = self.game.conditions.weather.atmospheric
        try_set_attr(a, "turbulence_per_10cm", 0.1)
        sc = self.game.theater.seasonal_conditions
        if not hasattr(
            self.game.theater.seasonal_conditions, "high_avg_yearly_turbulence_per_10cm"
        ):
            self.game.theater.seasonal_conditions = SeasonalConditions(
                summer_avg_pressure=sc.summer_avg_pressure,
                winter_avg_pressure=sc.winter_avg_pressure,
                summer_avg_temperature=sc.summer_avg_temperature,
                winter_avg_temperature=sc.winter_avg_temperature,
                temperature_day_night_difference=sc.temperature_day_night_difference,
                high_avg_yearly_turbulence_per_10cm=1.2,
                low_avg_yearly_turbulence_per_10cm=0.1,
                solar_noon_turbulence_per_10cm=0.8,
                midnight_turbulence_per_10cm=0.4,
                weather_type_chances=sc.weather_type_chances,
            )

    def _update_tgos(self) -> None:
        for go in self.game.theater.ground_objects:
            try_set_attr(go, "task", None)
            try_set_attr(go, "hide_on_mfd", False)
