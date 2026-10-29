"""Two unit yamls must not claim the same variant name.

Factions name units by variant, so a shared name makes one unit unreachable and the
faction can field the wrong one. CH_ZTQ_15 and PGL_625 had copied their neighbour's
variant (the ZTZ-99A2 and the LD-3000).
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

import pytest
import yaml

UNITS = Path(__file__).resolve().parents[1] / "resources" / "units"

# Shared on purpose: the mod itself gives both ids one name, or the yaml lists its
# twin's variant so either id can be picked.
KNOWN_SHARED = {
    ("ground_units", "[CH] DShK HMG"),
    ("aircraft", "SH-2F Seasprite"),
    ("aircraft", "Su-30MKA Flanker-H (A-G)"),
    ("aircraft", "Su-30MKI Flanker-H (A-G)"),
    ("aircraft", "Su-30MKM Flanker-H (A-G)"),
    ("aircraft", "Su-30SM Flanker-H (A-G)"),
}


@pytest.mark.parametrize("kind", ["aircraft", "ground_units", "ships"])
def test_no_two_unit_files_share_a_variant(kind: str) -> None:
    owners: dict[str, list[str]] = defaultdict(list)
    for path in sorted((UNITS / kind).glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        for variant in data.get("variants") or {path.stem: None}:
            owners[variant].append(path.name)
    shared = {
        variant: files
        for variant, files in owners.items()
        if len(files) > 1 and (kind, variant) not in KNOWN_SHARED
    }
    assert not shared, f"variant names claimed by more than one yaml: {shared}"
