"""Every shipped preset must name units and layouts that actually exist.

ForceGroup._process_path only *logs* an unknown unit or layout and carries on, so a
preset that names something Retribution does not know loses it in silence: the site
generates short, or not at all, and nothing tells you. That is the same shape as the
bug where a mod dropped a unit family the presets still asked for — DCS discarded the
units, Retribution kept believing the site was alive, and DEAD packages against it could
never finish. This test refuses to let a preset ship in that state.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from game import persistency
from game.dcs.groundunittype import GroundUnitType
from game.dcs.shipunittype import ShipUnitType
from game.layout import LAYOUTS

PRESETS = sorted(Path("resources/groups").glob("*.yaml"))


@pytest.fixture(autouse=True)
def _init_persistency(tmp_path_factory: pytest.TempPathFactory) -> None:
    # Preset and layout loading read the DCS saved-game folder, which only exists once
    # the app boots. Point it at an empty temp dir so we load the bundled resources.
    persistency.setup(
        str(tmp_path_factory.mktemp("saved_games")),
        prefer_liberation_payloads=False,
        port=0,
    )


def test_there_are_presets_to_check() -> None:
    """Guard the guard: a bad glob would make every test below vacuously pass."""
    assert len(PRESETS) > 50


@pytest.mark.parametrize("preset", PRESETS, ids=lambda p: p.stem)
def test_preset_units_and_layouts_exist(preset: Path) -> None:
    data = yaml.safe_load(preset.read_text(encoding="utf-8"))

    unknown = [
        unit
        for unit in data.get("units") or []
        if not GroundUnitType.exists(unit) and not ShipUnitType.exists(unit)
    ]
    assert not unknown, f"{preset.name} names units that do not exist: {unknown}"

    for layout in data.get("layouts") or []:
        try:
            LAYOUTS.by_name(layout)
        except KeyError:
            pytest.fail(f"{preset.name} references unknown layout {layout!r}")
