"""The Early Tomcat's payload file must bind to its own unit type.

pydcs keys payload files by the file's unitType FIELD, not by the filename.
F-14A-135-GR-Early.lua declared unitType "F-14A-135-GR" (missing -Early), which
silently unbound the entire file: the Early variant resolved no presets for any
task and auto-planned with an empty loadout, flying every tasking unarmed.
"""

import re
from pathlib import Path

import pytest
from dcs.payloads import PayloadDirectories
from dcs.planes import F_14A_135_GR_Early
from dcs.unittype import FlyingType

from game.ato.flighttype import FlightType
from game.ato.loadouts import Loadout

PAYLOADS_DIR = Path(__file__).parent.parent / "resources" / "customized_payloads"


@pytest.fixture(autouse=True)
def payload_dirs() -> None:
    # Force a rescan against the repo's payload dir regardless of what earlier
    # tests (or a developer's Saved Games) left in the class-level cache.
    PayloadDirectories.set_fallback(PAYLOADS_DIR)
    FlyingType._payload_cache = None  # type: ignore[assignment]


def test_early_tomcat_payload_file_binds_to_its_own_type() -> None:
    text = (PAYLOADS_DIR / "F-14A-135-GR-Early.lua").read_text()
    match = re.search(r'\["unitType"\]\s*=\s*"([^"]*)"', text)
    assert match is not None
    assert match.group(1) == "F-14A-135-GR-Early"


def test_early_tomcat_resolves_an_armed_barcap_loadout() -> None:
    loadout = Loadout.default_for_task_and_aircraft(
        FlightType.BARCAP, F_14A_135_GR_Early
    )
    assert loadout.pylons, "the Early Tomcat resolved an empty BARCAP loadout"
    a2a = [
        w
        for w in loadout.pylons.values()
        if w is not None and re.search(r"AIM-\d|AIM_\d", w.name)
    ]
    assert a2a, f"loadout {loadout.name} has no A2A missile"
