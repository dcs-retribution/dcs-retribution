"""Per-flight cartridge contents.

Every section defaults on. The campaign-wide ``dtc_data_cartridges`` setting
is the only switch surfaced today; the dataclass exists so a per-flight
control can be added without touching the builders.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class DtcOptions:
    """What (if anything) this flight's cartridge should carry.

    ``enabled`` is a tri-state: ``None`` follows the campaign-wide
    ``dtc_data_cartridges`` setting, ``True``/``False`` override it for this
    flight alone. The section flags select cartridge contents; a section that
    is off is omitted entirely, leaving the jet's own defaults untouched.
    """

    enabled: Optional[bool] = None
    #: The flight's steerpoints + route sequence (ETAs, leg speeds).
    route: bool = True
    #: Recovery aids: TACAN/ICLS/ACLS pre-tune + FPAS home waypoint (Hornet).
    nav_aids: bool = True
    #: The active front line(s) (SA FLOT lines / HSD GEO lines).
    flot_and_zones: bool = True
    #: Friendly CAP stations + tanker/AEW&C orbits (SA racetracks; Viper
    #: anchor steerpoints).
    friendly_orbits: bool = True
    #: Known enemy SAM threat rings (recon-fogged).
    threat_rings: bool = True
    #: Friendly recovery fields as Destination steerpoints (Viper only -- the
    #: Hornet descriptor has no equivalent section).
    destinations: bool = True

    def resolve_enabled(self, campaign_default: bool) -> bool:
        """The effective on/off for this flight."""
        if self.enabled is None:
            return campaign_default
        return self.enabled

    @property
    def any_content(self) -> bool:
        """Whether any section would make it into the cartridge."""
        return any(
            (
                self.route,
                self.nav_aids,
                self.flot_and_zones,
                self.friendly_orbits,
                self.threat_rings,
                self.destinations,
            )
        )
