from typing import Dict

from dcs.cloud_presets import CLOUD_PRESETS, Clouds


def inject_cloud_presets(presets: Dict[str, Clouds]) -> None:
    """
    Inject custom cloud presets from mods into pydcs' cloud presets databases via introspection
    :param presets: The custom presets to be injected into pydcs' cloud presets database
    :return: None
    """
    CLOUD_PRESETS.update(presets)


def eject_cloud_presets(presets: Dict[str, Clouds]) -> None:
    for preset in presets:
        if preset in CLOUD_PRESETS:
            del CLOUD_PRESETS[preset]
