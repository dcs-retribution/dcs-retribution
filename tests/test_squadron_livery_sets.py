"""The F-14B(U) presets must carry a livery set, not one pinned livery.

The Tomcat's board number is painted into its livery -- no F-14 livery declares
a number material, so DCS never draws the mission's ``onboard_num`` on one. A
preset pinning a single ``livery:`` therefore puts the same board number on
every jet in the squadron, which is what the F-14B(U) presets used to do.
Every livery DCS ships for the type names its modex, so the fix is
a set, ordered CAG bird first.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
import yaml

PRESET_DIR = Path("resources/squadrons/F-14B(U) Tomcat")


def _presets() -> list[tuple[str, dict[str, Any]]]:
    return [
        (path.stem, yaml.safe_load(path.read_text(encoding="utf-8")))
        for path in sorted(PRESET_DIR.glob("*.yaml"))
    ]


def test_every_preset_exists() -> None:
    assert [name for name, _ in _presets()] == [
        "VF-101",
        "VF-103",
        "VF-11",
        "VF-143",
        "VF-32",
    ]


@pytest.mark.parametrize("name,preset", _presets(), ids=lambda v: str(v)[:16])
def test_preset_uses_a_livery_set_not_a_single_livery(
    name: str, preset: dict[str, Any]
) -> None:
    assert (
        "livery" not in preset
    ), f"{name} pins one livery; the whole squadron wears it"
    assert len(preset["livery_set"]) >= 2, f"{name} needs more than one board number"


@pytest.mark.parametrize("name,preset", _presets(), ids=lambda v: str(v)[:16])
def test_lowest_modex_leads_the_set(name: str, preset: dict[str, Any]) -> None:
    """The allocator hands entry 0 to the squadron's first jet -- the CAG bird."""
    modexes = [livery.split()[2] for livery in preset["livery_set"]]
    assert modexes[0] == min(modexes), f"{name} does not lead with {min(modexes)}"


@pytest.mark.parametrize("name,preset", _presets(), ids=lambda v: str(v)[:16])
def test_set_has_no_repeated_board_number(name: str, preset: dict[str, Any]) -> None:
    modexes = [livery.split()[2] for livery in preset["livery_set"]]
    assert len(set(modexes)) == len(modexes), f"{name} repeats a board number"
