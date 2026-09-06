from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional, TYPE_CHECKING, Union

import yaml
from dcs.country import Country
from dcs.task import Modulation

from game.ato.flighttype import FlightType
from game.dcs.aircrafttype import AircraftType, derived_task_types
from game.dcs.countries import country_with_name
from game.radio.radios import RadioFrequency
from game.squadrons.operatingbases import OperatingBases
from game.squadrons.pilot import Pilot

if TYPE_CHECKING:
    from game.theater import ControlPoint


@dataclass
class SquadronDef:
    name: str
    nickname: Optional[str]
    country: Country
    role: str
    aircraft: AircraftType
    livery: Optional[str]
    livery_set: list[str]
    auto_assignable_mission_types: set[FlightType]
    radio_presets: dict[Union[str, int], list[RadioFrequency]]
    operating_bases: OperatingBases
    female_pilot_percentage: int
    pilot_pool: list[Pilot]
    claimed: bool = False

    def __str__(self) -> str:
        if self.nickname is None:
            return self.name
        return f'{self.name} "{self.nickname}"'

    def capable_of(self, task: FlightType) -> bool:
        """Returns True if the squadron is capable of performing the given task.
        A squadron may be capable of performing a task even if it will not be
        automatically assigned to it.
        """
        return self.aircraft.capable_of(task)

    def can_auto_assign(self, task: FlightType) -> bool:
        """Whether this def auto-assigns ``task``.

        Mirrors Squadron.can_auto_assign: the task must be in the def's
        auto-assignable set AND within the airframe's capabilities.
        """
        return task in self.auto_assignable_mission_types and self.aircraft.capable_of(
            task
        )

    def operates_from(self, control_point: ControlPoint) -> bool:
        if not control_point.can_operate(self.aircraft):
            return False
        if control_point.is_carrier:
            return self.operating_bases.carrier
        elif control_point.is_lha:
            return self.operating_bases.lha
        else:
            return self.operating_bases.shore

    @staticmethod
    def _auto_assignable_from_yaml(
        data: dict[str, Any], unit_type: AircraftType
    ) -> set[FlightType]:
        raw = data.get("mission_types")
        if raw is None:
            # No restriction declared: default to the full airframe capability set.
            return set(unit_type.iter_task_capabilities())
        if isinstance(raw, str) or not isinstance(raw, (list, tuple)):
            # A bare scalar (e.g. `mission_types: SEAD`) would otherwise be iterated
            # character-by-character, yielding a confusing per-character error.
            raise KeyError(
                "mission_types must be a list of flight types, got "
                f"{type(raw).__name__}: {raw!r}"
            )
        try:
            declared = {FlightType(value) for value in raw}
        except ValueError as ex:
            # FlightType(...) raises ValueError on an unknown value; surface it as a
            # KeyError with context, matching the unknown-aircraft handling above.
            raise KeyError(f"Unknown mission type in squadron definition: {ex}") from ex
        caps = set(unit_type.iter_task_capabilities())
        # Clamp to caps BEFORE deriving so a listed-but-incapable task cannot grant a
        # derived sibling (e.g. listing SEAD on an airframe that only has SEAD_ESCORT
        # must not back-door SEAD_SWEEP). mission_types can only *subtract* from the
        # cap, never add a capability. The trailing clamp keeps only capable siblings.
        declared &= caps
        declared |= derived_task_types(declared, unit_type.carrier_capable)
        return declared & caps

    @classmethod
    def from_yaml(cls, path: Path) -> SquadronDef:
        with path.open(encoding="utf8") as squadron_file:
            data = yaml.safe_load(squadron_file)

        name = data["aircraft"]
        try:
            unit_type = AircraftType.named(name)
        except KeyError as ex:
            raise KeyError(f"Could not find any aircraft named {name}") from ex

        pilots = [Pilot(n, player=False) for n in data.get("pilots", [])]
        pilots.extend([Pilot(n, player=True) for n in data.get("players", [])])
        female_pilot_percentage = data.get("female_pilot_percentage", 6)

        radio_presets = data.get("radio_presets", {})
        for radio in radio_presets:
            freq_list: list[RadioFrequency] = []
            for freq in radio_presets[radio]:
                # TODO: set up modulation for UI manipulations (issue#89)
                hz = int(freq * 1000000)
                if hz % 10:  # fix rounding errors
                    hz = hz + 10 - hz % 10
                mod = Modulation.AM
                ifr = unit_type.intra_flight_radio
                if radio == "intra_flight" and ifr:
                    for r in ifr.ranges:
                        if r.minimum.mhz <= hz / 1000000 < r.maximum.mhz:
                            mod = r.modulation
                            break
                freq_list.append(RadioFrequency(hz, modulation=mod))
            radio_presets[radio] = freq_list

        return SquadronDef(
            name=data["name"],
            nickname=data.get("nickname"),
            country=country_with_name(data["country"]),
            role=data["role"],
            aircraft=unit_type,
            livery=data.get("livery"),
            livery_set=data.get("livery_set", []),
            auto_assignable_mission_types=cls._auto_assignable_from_yaml(
                data, unit_type
            ),
            radio_presets=radio_presets,
            operating_bases=OperatingBases.from_yaml(unit_type, data.get("bases", {})),
            female_pilot_percentage=female_pilot_percentage,
            pilot_pool=pilots,
        )
