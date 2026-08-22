"""The cartridge model: one JSON payload plus its identity.

DCS's native Data Transfer Cartridge is two pieces inside an ordinary miz,
both carried by pydcs: a JSON file at ``DTC/<name>.dtc`` in the zip root, and
a per-unit ``DTC`` block binding one by name with ``AutoLoad`` so the jet
ingests it at spawn. Because the file travels inside the miz it reaches
multiplayer clients with the mission download. Format confirmed against the
mission editor's own DTC manager (``MissionEditor/modules/me_managerDTC.lua``
plus the per-aircraft ``CoreMods/aircraft/<type>/DTC`` descriptors) and
against cartridges authored in the editor.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class DtcCartridge:
    """One built cartridge.

    ``name`` doubles as the file name inside the miz (``DTC/<name>.dtc``) and
    the string units reference, exactly like the editor's own manager -- keep
    it filesystem-safe (the generator builds names from callsigns, which are).
    """

    name: str
    unit_type: str
    terrain: str
    data: dict[str, Any]

    def to_json(self) -> str:
        # The editor writes {data, name, type} at the top level; the
        # descriptor's own data table carries name/type again inside (the
        # builders fill those). 4-space pretty print matches the editor's output.
        payload = {"data": self.data, "name": self.name, "type": self.unit_type}
        return json.dumps(payload, indent=4)
