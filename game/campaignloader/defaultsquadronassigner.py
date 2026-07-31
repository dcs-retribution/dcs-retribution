from __future__ import annotations

import logging
import random
from typing import Optional, TYPE_CHECKING

from dcs.country import Country

from game.squadrons import Squadron
from game.squadrons.squadrondef import SquadronDef
from .campaignairwingconfig import CampaignAirWingConfig, SquadronConfig
from ..ato.flighttype import FlightType
from ..dcs.aircrafttype import AircraftType
from ..dcs.countries import country_with_name
from ..theater import ControlPoint

if TYPE_CHECKING:
    from game import Game
    from game.coalition import Coalition


def resolve_config_country(config: SquadronConfig) -> Optional[Country]:
    """The campaign-pinned DCS country for a squadron config, if any.

    An unknown ``country:`` name is a campaign authoring error: raise so New
    Game aborts loudly and points the author at the bad name, rather than
    silently flying under the wrong nation.
    """
    if config.country is None:
        return None
    try:
        return country_with_name(config.country)
    except KeyError as ex:
        raise ValueError(
            f"Squadron config country {config.country!r} is not a DCS country "
            f"name. Fix the campaign's squadron `country:` value."
        ) from ex


class DefaultSquadronAssigner:
    def __init__(
        self, config: CampaignAirWingConfig, game: Game, coalition: Coalition
    ) -> None:
        self.config = config
        self.game = game
        self.coalition = coalition
        self.air_wing = coalition.air_wing

    def assign(self) -> None:
        for control_point in self.game.theater.control_points_for(
            self.coalition.player
        ):
            for squadron_config in self.config.by_location[control_point]:
                squadron_def = self.override_squadron_defaults(
                    self.find_squadron_for(squadron_config, control_point),
                    squadron_config,
                )

                if squadron_def is None:
                    logging.info(
                        f"{self.coalition.faction.name} has no aircraft compatible "
                        f"with {squadron_config.primary} at {control_point}"
                    )
                    continue

                squadron = Squadron.create_from(
                    squadron_def,
                    squadron_config.primary,
                    squadron_config.max_size,
                    control_point,
                    self.coalition,
                    self.game,
                )
                squadron.set_auto_assignable_mission_types(
                    squadron_config.auto_assignable
                )
                self.air_wing.add_squadron(squadron)

    def find_squadron_for(
        self, config: SquadronConfig, control_point: ControlPoint
    ) -> Optional[SquadronDef]:
        # A campaign-pinned nation (#627) makes the preset pick deterministic in
        # country: only same-nation presets are eligible, and the generated
        # fallback is stamped with the pinned country by
        # override_squadron_defaults. Unpinned squadrons keep the picked def's
        # own country (the stock random behavior).
        country = resolve_config_country(config)
        for preferred_aircraft in config.aircraft:
            squadron_def = self.find_preferred_squadron(
                preferred_aircraft,
                config.aircraft_type,
                config.primary,
                control_point,
                country,
            )
            if squadron_def is not None:
                return squadron_def

        # If we didn't find any of the preferred types we should use any squadron
        # compatible with the primary task.
        squadron_def = self.find_squadron_for_task(
            config.primary, control_point, country
        )
        if squadron_def is not None:
            return squadron_def

        # If we can't find any squadron matching the requirement, we should
        # create one. A pinned country is stamped by override_squadron_defaults;
        # an unpinned squadron keeps the generated def's own country.
        return self.air_wing.squadron_def_generator.generate_for_task(
            config.primary, control_point
        )

    def find_preferred_squadron(
        self,
        preferred_aircraft: str,
        aircraft_type: Optional[str],
        task: FlightType,
        control_point: ControlPoint,
        country: Optional[Country] = None,
    ) -> Optional[SquadronDef]:
        # Attempt to find a squadron with the name in the request. An explicitly
        # named preset wins over the country preference (the author asked for
        # that unit); an authored country: still re-stamps its nation afterward
        # in override_squadron_defaults.
        squadron_def = self.find_squadron_by_name(
            preferred_aircraft, task, control_point
        )
        if squadron_def is not None:
            return squadron_def

        # If the name didn't match a squadron available to this coalition, try to find
        # an aircraft with the matching name that meets the requirements.
        try:
            aircraft = AircraftType.named(aircraft_type or preferred_aircraft)
        except KeyError:
            logging.warning(
                "%s is neither a compatible squadron or a known aircraft type, "
                "ignoring",
                preferred_aircraft,
            )
            return None

        if aircraft not in self.coalition.faction.all_aircrafts:
            return None

        # A pinned country restricts the preset pick to that nation and stamps
        # the generated fallback; an unpinned squadron keeps the preset/def's own
        # country (override_squadron_defaults handles the pinned case).
        squadron_def = self.find_squadron_for_airframe(
            aircraft, task, control_point, country
        )
        if squadron_def is not None and (
            squadron_def.livery is not None or squadron_def.livery_set is not None
        ):
            return squadron_def

        # No premade squadron available for this aircraft that meets the requirements,
        # so generate one if possible.
        return self.air_wing.squadron_def_generator.generate_for_aircraft(aircraft)

    @staticmethod
    def squadron_compatible_with(
        squadron: SquadronDef,
        task: FlightType,
        control_point: ControlPoint,
        ignore_base_preference: bool = False,
    ) -> bool:
        if ignore_base_preference:
            return control_point.can_operate(squadron.aircraft)
        return squadron.operates_from(control_point) and squadron.capable_of(task)

    def find_squadron_for_airframe(
        self,
        aircraft: AircraftType,
        task: FlightType,
        control_point: ControlPoint,
        country: Optional[Country] = None,
    ) -> Optional[SquadronDef]:
        choices = []
        for squadron in self.air_wing.squadron_defs[aircraft]:
            if not squadron.claimed and self.squadron_compatible_with(
                squadron, task, control_point
            ):
                choices.append(squadron)
        if country is not None:
            # Pinned nation: a wrong-nation preset would drag its livery and any
            # authored ace roster along even after the country override, so no
            # same-nation match falls through to the def generator instead.
            choices = [s for s in choices if s.country.id == country.id]
        if choices:
            return random.choice(choices)
        return None

    def find_squadron_by_name(
        self, name: str, task: FlightType, control_point: ControlPoint
    ) -> Optional[SquadronDef]:
        for squadrons in self.air_wing.squadron_defs.values():
            for squadron in squadrons:
                if (
                    not squadron.claimed
                    and squadron.name == name
                    and self.squadron_compatible_with(
                        squadron, task, control_point, ignore_base_preference=True
                    )
                ):
                    return squadron
        return None

    def find_squadron_for_task(
        self,
        task: FlightType,
        control_point: ControlPoint,
        country: Optional[Country] = None,
    ) -> Optional[SquadronDef]:
        for squadrons in self.air_wing.squadron_defs.values():
            for squadron in squadrons:
                if country is not None and squadron.country.id != country.id:
                    continue
                if not squadron.claimed and self.squadron_compatible_with(
                    squadron, task, control_point
                ):
                    return squadron
        return None

    @staticmethod
    def override_squadron_defaults(
        squadron_def: Optional[SquadronDef], config: SquadronConfig
    ) -> Optional[SquadronDef]:
        if squadron_def is None:
            return None

        if config.name is not None:
            squadron_def.name = config.name
        if config.nickname is not None:
            squadron_def.nickname = config.nickname
        if config.female_pilot_percentage is not None:
            squadron_def.female_pilot_percentage = config.female_pilot_percentage
        if config.country is not None:
            # Stamp the pinned nation (#627 voice/comms + pilot names). This is
            # what gives a generated def (no preset existed for the nation) its
            # country, and it also wins over a name-bound preset's own nation
            # when the author sets both.
            country = resolve_config_country(config)
            if country is not None:
                squadron_def.country = country

        return squadron_def
