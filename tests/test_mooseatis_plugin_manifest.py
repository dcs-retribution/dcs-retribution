from __future__ import annotations

import json
from pathlib import Path

PLUGINS = Path("resources/plugins")


def test_mooseatis_registered_in_plugins_json() -> None:
    registry = json.loads((PLUGINS / "plugins.json").read_text(encoding="utf-8"))
    assert "MooseAtis" in registry
    # Must load after "base" (which loads MOOSE).
    assert registry.index("MooseAtis") > registry.index("base")


def test_mooseatis_manifest_is_valid_and_default_off() -> None:
    manifest = json.loads(
        (PLUGINS / "MooseAtis" / "plugin.json").read_text(encoding="utf-8")
    )
    assert manifest["nameInUI"] == "Moose ATIS"
    assert manifest["defaultValue"] is False  # opt-in
    assert manifest["configurationWorkOrders"][0]["file"] == "Plugin_Atis.lua"


def test_mooseatis_other_resource_files_exist() -> None:
    base = PLUGINS / "MooseAtis"
    manifest = json.loads((base / "plugin.json").read_text(encoding="utf-8"))
    assert manifest["otherResourceFiles"], "expected vendored soundfiles listed"
    for rel in manifest["otherResourceFiles"]:
        assert (base / rel).exists(), f"missing bundled resource: {rel}"


def test_loader_script_exists() -> None:
    assert (PLUGINS / "MooseAtis" / "Plugin_Atis.lua").exists()
