"""Per-flight cartridge contents.

Every section defaults on. The campaign-wide ``dtc_cartridge_loading`` setting
is the only switch surfaced today; the dataclass exists so a per-flight
control can be added without touching the builders.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from game.settings.settings import DtcCartridgeLoading


@dataclass
class DtcOptions:
    """What (if anything) this flight's cartridge should carry.

    ``enabled`` and ``auto_load`` are tri-states: ``None`` follows the
    campaign-wide ``dtc_cartridge_loading`` setting, ``True``/``False``
    override it for this flight alone. The section flags select cartridge contents; a section that
    is off is omitted entirely, leaving the jet's own defaults untouched.
    """

    enabled: Optional[bool] = None
    #: Load the cartridge at spawn; off, it waits on the jet's DTC page.
    auto_load: Optional[bool] = None
    #: Radio presets with channel names (Hornet only -- the Viper's channel
    #: schema has no name field).
    comms: bool = True
    #: The flight's steerpoints + route sequence (ETAs, leg speeds), and the
    #: Hornet's attack lane (SA corridor).
    route: bool = True
    #: Recovery aids: TACAN/ICLS/ACLS pre-tune, FPAS home waypoint and the
    #: TACAN station list (Hornet).
    nav_aids: bool = True
    #: The active front line(s) (SA FLOT lines / HSD GEO lines), and the
    #: Viper's box on a CAS or SEAD flight's working area.
    flot_and_zones: bool = True
    #: Friendly CAP stations + tanker/AEW&C orbits (SA racetracks; Viper
    #: anchor steerpoints).
    friendly_orbits: bool = True
    #: Known enemy SAM threat rings (recon-fogged).
    threat_rings: bool = True
    #: Friendly recovery fields as Destination steerpoints (Viper only -- the
    #: Hornet descriptor has no equivalent section).
    destinations: bool = True

    def resolve_enabled(self, campaign_default: DtcCartridgeLoading) -> bool:
        """The effective on/off for this flight."""
        from game.settings.settings import DtcCartridgeLoading

        if self.enabled is None:
            return campaign_default is not DtcCartridgeLoading.OFF
        return self.enabled

    def resolve_auto_load(self, campaign_default: DtcCartridgeLoading) -> bool:
        """Whether the jet loads the cartridge at spawn."""
        from game.settings.settings import DtcCartridgeLoading

        if self.auto_load is None:
            return campaign_default is DtcCartridgeLoading.SPAWN
        return self.auto_load

    @property
    def any_content(self) -> bool:
        """Whether any section would make it into the cartridge."""
        return any(
            (
                self.comms,
                self.route,
                self.nav_aids,
                self.flot_and_zones,
                self.friendly_orbits,
                self.threat_rings,
                self.destinations,
            )
        )
