from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from game.ato.loadouts import Loadout
from game.lasercodes import LaserCode
from game.lasercodes.lasercoderegistry import LaserCodeRegistry
from game.settings.settings import DefaultPlayerLaserCode, Settings

if TYPE_CHECKING:
    from game.squadrons import Pilot


class FlightMember:
    def __init__(self, pilot: Pilot | None, loadout: Loadout) -> None:
        self.pilot = pilot
        self.loadout = loadout
        self.use_custom_loadout = False
        self.tgp_laser_code: LaserCode | None = None
        self.weapon_laser_code: LaserCode | None = None
        self.properties: dict[str, bool | float | int | str] = {}
        self.livery: Optional[str] = None
        self.use_livery_set: bool = True

    def __setstate__(self, state: dict[str, Any]) -> None:
        new_state = FlightMember(state["pilot"], state["loadout"])
        new_state.__dict__.update(state)
        self.__dict__.update(new_state.__dict__)

    def assign_tgp_laser_code(self, code: LaserCode) -> None:
        if self.tgp_laser_code is not None:
            raise RuntimeError(
                f"{self.pilot} already has already been assigned laser code "
                f"{self.tgp_laser_code}"
            )
        self.tgp_laser_code = code

    def release_tgp_laser_code(self) -> None:
        if self.tgp_laser_code is None:
            raise RuntimeError(f"{self.pilot} has no assigned laser code")

        if self.weapon_laser_code == self.tgp_laser_code:
            self.weapon_laser_code = None
        self.tgp_laser_code.release()
        self.tgp_laser_code = None

    @property
    def is_player(self) -> bool:
        if self.pilot is None:
            return False
        return self.pilot.player


def apply_default_player_laser_code(
    member: FlightMember,
    settings: Settings,
    registry: LaserCodeRegistry,
) -> None:
    """Apply the campaign-level default laser code to a newly-created flight member.

    AI members are untouched. For player members when the setting is
    ALLOCATE_OWN, a unique code is allocated and assigned to both the TGP
    (kneeboard) code and the weapon code, so the player's LGBs home on their own
    code by default while remaining independently overridable in the payload tab.
    When the setting is DEFAULT_1688 both are left unset, falling back to 1688.
    """
    if not member.is_player:
        return
    if settings.default_player_laser_code is DefaultPlayerLaserCode.ALLOCATE_OWN:
        code = registry.alloc_laser_code()
        member.assign_tgp_laser_code(code)
        member.weapon_laser_code = code
