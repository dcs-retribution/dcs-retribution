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
        self.laser_code: LaserCode | None = None
        self._owns_laser_code: bool = False
        self.properties: dict[str, bool | float | int | str] = {}
        self.livery: Optional[str] = None
        self.use_livery_set: bool = True

    def __setstate__(self, state: dict[str, Any]) -> None:
        new_state = FlightMember(state["pilot"], state["loadout"])
        new_state.__dict__.update(state)
        self.__dict__.update(new_state.__dict__)
        self._migrate_legacy_laser_code_fields(state)

    def _migrate_legacy_laser_code_fields(self, state: dict[str, Any]) -> None:
        """Migrate pre-collapse tgp_laser_code / weapon_laser_code into laser_code.

        Discriminator: ``state`` is the dict that came off disk. ``self.__dict__``
        is not safe to use because the constructor may have re-seeded keys.

        - If ``state`` already has the new ``laser_code`` key, the save was
          written by the new code path; trust it and just pop the legacy keys.
        - Else if ``state`` has ``weapon_laser_code``: that field is the source
          of truth for the active code. Promote with ownership iff it equals
          ``tgp_laser_code``; otherwise release the orphan tgp reservation.
        - Else if ``state`` has only ``tgp_laser_code``: pre-``weapon_laser_code``
          save; promote with ownership.
        """
        if "laser_code" in state:
            # New save format. self.laser_code / self._owns_laser_code are
            # already populated by __dict__.update(state); nothing to migrate.
            self.__dict__.pop("tgp_laser_code", None)
            self.__dict__.pop("weapon_laser_code", None)
            return

        has_weapon_key = "weapon_laser_code" in state
        has_tgp_key = "tgp_laser_code" in state
        weapon = state.get("weapon_laser_code")
        tgp = state.get("tgp_laser_code")

        if has_weapon_key:
            if weapon is not None and tgp is not None and weapon == tgp:
                self.laser_code = weapon
                self._owns_laser_code = True
            else:
                self.laser_code = weapon
                self._owns_laser_code = False
                if tgp is not None and (weapon is None or weapon != tgp):
                    tgp.release()
        elif has_tgp_key:
            if tgp is not None:
                self.laser_code = tgp
                self._owns_laser_code = True

        self.__dict__.pop("tgp_laser_code", None)
        self.__dict__.pop("weapon_laser_code", None)

    @property
    def owns_laser_code(self) -> bool:
        """True if this member's laser_code was allocated for it (and must be released on teardown)."""
        return self._owns_laser_code

    def set_allocated_laser_code(self, code: LaserCode) -> None:
        """Assign a registry-allocated code that this member now owns."""
        self._release_owned()
        self.laser_code = code
        self._owns_laser_code = True

    def set_shared_laser_code(self, code: LaserCode | None) -> None:
        """Assign a JTAC code, or None for the 1688 default. Member does not own it."""
        self._release_owned()
        self.laser_code = code
        self._owns_laser_code = False

    def _release_owned(self) -> None:
        """Release the current laser code if owned, then clear both fields.

        Always sets ``laser_code = None`` and ``_owns_laser_code = False``,
        regardless of prior ownership.
        """
        if self._owns_laser_code and self.laser_code is not None:
            self.laser_code.release()
        self.laser_code = None
        self._owns_laser_code = False

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

    AI members are untouched. Player members receive an allocated code when the
    setting is ALLOCATE_OWN, and are left at None when the setting is DEFAULT_1688.
    """
    if not member.is_player:
        return
    if settings.default_player_laser_code is DefaultPlayerLaserCode.ALLOCATE_OWN:
        member.set_allocated_laser_code(registry.alloc_laser_code())
