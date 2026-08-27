from __future__ import annotations

from typing import Callable, NamedTuple

from game.settings import Settings
from game.settings.settings import CloudPresetPack
from pydcs_extensions import AtmosXClouds, BanditClouds, Weather2Clouds


class _Pack(NamedTuple):
    """The pair of calls that swaps one pack's presets into ``CLOUD_PRESETS``."""

    inject: Callable[[], None]
    eject: Callable[[], None]


_PACKS = {
    CloudPresetPack.BANDIT: _Pack(BanditClouds.activate, BanditClouds.deactivate),
    CloudPresetPack.WEATHER2: _Pack(Weather2Clouds.activate, Weather2Clouds.deactivate),
    CloudPresetPack.ATMOSX: _Pack(AtmosXClouds.activate, AtmosXClouds.deactivate),
}


def apply_cloud_preset_pack(settings: Settings) -> None:
    """Make ``settings.cloud_preset_pack`` the pack that ``CLOUD_PRESETS`` holds.

    Only one pack may be injected at a time. They reuse the same ``PresetNN`` keys
    for different clouds, so a stale pack does not merely leave unused entries
    behind: it answers to the chosen pack's own keys with the wrong cloud.

    Idempotent, and cheap enough to call on every weather generation -- which is
    deliberate. The setting is reachable from the new-campaign wizard, from the
    in-game settings dialog and from a loaded save, so making correctness depend on
    which of those the user happened to pass through is what silently stopped the
    packs from applying at all.
    """
    chosen = settings.cloud_preset_pack
    # Eject the others first, then inject: because the keys are shared, ejecting
    # after injecting would undo the chosen pack's own presets.
    for pack, calls in _PACKS.items():
        if pack is not chosen:
            calls.eject()
    if chosen in _PACKS:
        _PACKS[chosen].inject()
