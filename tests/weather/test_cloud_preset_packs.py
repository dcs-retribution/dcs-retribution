"""Activating the selected cloud-preset pack.

The packs map the same ``PresetNN`` keys to different clouds, so exactly one may be
loaded at a time and the choice has to be applied wherever weather is built -- not
only where the setting is edited.
"""

from __future__ import annotations

import datetime
from types import SimpleNamespace
from typing import Any, Iterator, cast

import pytest
from dcs.cloud_presets import CLOUD_PRESETS

from game.settings import Settings
from game.theater import ConflictTheater
from game.settings.settings import CloudPresetPack
from game.timeofday import TimeOfDay
from game.weather.cloudpresetpacks import apply_cloud_preset_pack
from game.weather.conditions import Conditions


@pytest.fixture(autouse=True)
def restore_presets() -> Iterator[None]:
    """CLOUD_PRESETS is global to the process; leave it as it was found."""
    before = dict(CLOUD_PRESETS)
    yield
    CLOUD_PRESETS.clear()
    CLOUD_PRESETS.update(before)


def _preset35() -> str | None:
    entry = CLOUD_PRESETS.get("Preset35")
    return None if entry is None else entry.value.ui_name


def test_switching_packs_replaces_the_shared_keys() -> None:
    """The hazard the packs create: Preset35 must mean the chosen pack's cloud.

    Ejecting after injecting would delete what was just put in, since both packs
    claim the key.
    """
    settings = Settings()

    settings.cloud_preset_pack = CloudPresetPack.BANDIT
    apply_cloud_preset_pack(settings)
    bandit = _preset35()
    assert bandit is not None

    settings.cloud_preset_pack = CloudPresetPack.ATMOSX
    apply_cloud_preset_pack(settings)
    atmosx = _preset35()
    assert atmosx is not None
    assert atmosx != bandit, "a stale pack still answers to the chosen pack's key"


def test_selecting_no_pack_ejects_the_previous_one() -> None:
    settings = Settings()

    settings.cloud_preset_pack = CloudPresetPack.ATMOSX
    apply_cloud_preset_pack(settings)
    assert _preset35() is not None

    settings.cloud_preset_pack = CloudPresetPack.NONE
    apply_cloud_preset_pack(settings)
    assert _preset35() is None, "stock DCS has no Preset35"


def test_generating_conditions_applies_the_pack(monkeypatch: Any) -> None:
    """The regression: generation must not depend on the settings dialog being opened.

    A new campaign goes wizard -> generate without ever constructing a
    QSettingsWindow, so a pack activated only on that dialog's close never reached
    the generator and the mission silently used whichever presets were loaded.
    """
    # As if a previous campaign in this process had chosen Bandit.
    stale = Settings()
    stale.cloud_preset_pack = CloudPresetPack.BANDIT
    apply_cloud_preset_pack(stale)
    bandit = _preset35()

    seen: list[str | None] = []

    def snapshot(*_: Any) -> Any:
        seen.append(_preset35())
        return SimpleNamespace()

    monkeypatch.setattr(Conditions, "generate_weather", staticmethod(snapshot))

    settings = Settings()
    settings.atmosx_live_weather = False
    settings.cloud_preset_pack = CloudPresetPack.ATMOSX
    Conditions.generate(
        # Only reached by the weather generator, which is stubbed out above.
        theater=cast(ConflictTheater, SimpleNamespace(seasonal_conditions=None)),
        day=datetime.date(2026, 6, 1),
        time_of_day=TimeOfDay.Day,
        settings=settings,
        forced_time=datetime.time(12, 0),
    )

    assert seen, "the weather generator was never reached"
    assert seen[0] is not None
    assert seen[0] != bandit, "generation ran with the previously loaded pack"


@pytest.mark.parametrize(
    "ui_name, expected",
    [
        # Stock names end in a variant number...
        ("Scattered 5", "Scattered"),
        ("Light Rain 4", "Light Rain"),
        # ...and the packs add their own tag after it, which used to be chopped in
        # half: the kneeboard read "Low level stratus 3 [ATMOS-".
        ("Low level stratus 3 [ATMOS-X]", "Low level stratus"),
        ("Scattered Showers 1 [Bandit648]", "Scattered Showers"),
        ("Cirrus", "Cirrus"),
    ],
)
def test_the_kneeboard_names_the_cloud_type(ui_name: str, expected: str) -> None:
    from game.missiongenerator.kneeboard import cloud_type_name

    assert cloud_type_name(ui_name) == expected
