"""DTC cartridge generation pass.

Builds one cartridge **per blue client flight** of a DTC-capable airframe
(FA-18C and F-16C) and binds it to the flight's client units with
``AutoLoad``. Per-flight rather than per-type because each flight flies its own
route -- a package's four Hornet flights get four cartridges, each loading its
own steerpoints while sharing the mission comm plan and SA picture.

Best-effort by design: a failure building one flight's cartridge skips that
flight, and a failure anywhere never blocks the mission save (the caller wraps
the pass; the miz without cartridges is exactly the miz without the feature).
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Callable, Optional

from dcs.mission import Mission

from game.missiongenerator.dtc.cartridge import DtcCartridge
from game.missiongenerator.dtc.hornet import HORNET_UNIT_TYPE, build_hornet_cartridge
from game.missiongenerator.dtc.viper import VIPER_UNIT_TYPE, build_viper_cartridge

if TYPE_CHECKING:
    from game import Game
    from game.missiongenerator.aircraft.flightdata import FlightData
    from game.missiongenerator.missiondata import MissionData

#: A builder may return ``None`` when nothing the airframe supports is switched
#: on; the generator then skips the flight rather than binding an empty
#: AutoLoading cartridge, which is worse than none.
CartridgeBuilder = Callable[..., Optional[DtcCartridge]]

#: DCS unit type id -> cartridge builder. Capability is the unit DB's ``DTC``
#: flag plus a matching ``<module>/DTC/<type>_DTC.lua`` -- the descriptor folder
#: alone is not enough (the CH-47F ships one and sets ``DTC = false``). The
#: ``F-14BU`` sets the flag too but its descriptor is a different schema and is
#: not built here. The CJS Super Hornets also qualify but are deliberately not
#: built: their descriptor has no SA table, and everything else a cartridge
#: could give them already reaches the jet through the miz.
CARTRIDGE_BUILDERS: dict[str, CartridgeBuilder] = {
    HORNET_UNIT_TYPE: build_hornet_cartridge,
    VIPER_UNIT_TYPE: build_viper_cartridge,
}


class DtcGenerator:
    """Builds + binds native DTC cartridges for blue client flights."""

    def __init__(self, mission: Mission, game: Game, mission_data: MissionData) -> None:
        self.mission = mission
        self.game = game
        self.mission_data = mission_data
        self.cartridges: list[DtcCartridge] = []

    def generate(self) -> None:
        used_names: set[str] = set()
        for flight in self.mission_data.flights:
            try:
                self._generate_for_flight(flight, used_names)
            except Exception:
                logging.exception(
                    "DTC: failed to build cartridge for %s; flight left bare",
                    flight.callsign,
                )

    def _generate_for_flight(self, flight: FlightData, used_names: set[str]) -> None:
        if not flight.friendly.is_blue:
            return
        clients = flight.client_units
        if not clients:
            return
        builder = CARTRIDGE_BUILDERS.get(flight.aircraft_type.dcs_unit_type.id)
        if builder is None:
            return
        # A per-flight choice wins over the campaign setting; an
        # all-sections-off cartridge is pointless.
        options = flight.dtc_options
        if not options.resolve_enabled(self.game.settings.dtc_data_cartridges):
            return
        if not options.any_content:
            return
        name = self._unique_name(flight, used_names)
        cartridge = builder(flight, self.mission_data, self.game, name)
        if cartridge is None:
            return
        self.mission.add_dtc_cartridge(cartridge.name, cartridge.to_json())
        for unit in clients:
            unit.add_dtc_cartridge(cartridge.name)
        self.cartridges.append(cartridge)
        used_names.add(cartridge.name)

    def _unique_name(self, flight: FlightData, used_names: set[str]) -> str:
        # The name doubles as the in-miz file name; callsigns are already
        # filesystem-safe. Keep it recognizable on the jet's DTC page.
        base = f"Retribution {flight.callsign} {flight.aircraft_type.dcs_unit_type.id}"
        name = base
        suffix = 2
        while name in used_names:
            name = f"{base} {suffix}"
            suffix += 1
        return name
