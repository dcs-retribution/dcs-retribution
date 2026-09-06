from pathlib import Path
from typing import Any, Optional

from game.plugins.mooseautolase import (
    MooseAutolasePlugin,
    build_unit_class_table,
    corridor_depths_m,
    _lua_frontlines,
    _lua_jtacs,
)
from game.radio.radios import MHz, RadioFrequency


def test_build_unit_class_table_maps_known_units() -> None:
    table = build_unit_class_table()
    assert table["ZSU-23-4 Shilka"] == "AAA"
    assert table["M-1 Abrams"] == "Tank"
    assert all(isinstance(v, str) and v for v in table.values())


def test_corridor_depths_match_deployment_table() -> None:
    default_m, artillery_m = corridor_depths_m()
    assert default_m == 8000
    assert artillery_m == 18000


class _FakeJtac:
    def __init__(
        self,
        name: str = "",
        seg: Any = None,
        group_name: Optional[str] = None,
        callsign: str = "Default 1",
        code: str = "1688",
        uhf_mhz: int = 251,
        vhf_mhz: int = 124,
        region: str = "Frontline Default",
    ) -> None:
        # Support both positional (name, seg) and keyword-only construction.
        self.group_name = group_name if group_name is not None else name
        self.frontline_segment = seg
        self.callsign = callsign
        self.code = code
        self.freq: RadioFrequency = MHz(uhf_mhz)
        self.freq_vhf: RadioFrequency = MHz(vhf_mhz)
        self.region = region


class _FakeMissionData:
    def __init__(self, jtacs: list[Any]) -> None:
        self.jtacs = jtacs


class _RecordingLuaGenerator:
    def __init__(self, jtacs: list[Any]) -> None:
        self.mission_data = _FakeMissionData(jtacs)
        self.triggers: list[str] = []

    def inject_lua_trigger(self, lua: str, comment: str) -> None:
        self.triggers.append(lua)

    def injected_lua(self) -> str:
        return "\n".join(self.triggers)


def _make_plugin() -> MooseAutolasePlugin:
    plugin = MooseAutolasePlugin.from_json(
        "MooseAutolase", Path("resources/plugins/MooseAutolase/plugin.json")
    )
    assert isinstance(plugin, MooseAutolasePlugin)
    return plugin


def test_subclass_injects_computed_tables_before_work_orders() -> None:
    from dcs.mapping import Point

    plugin = _make_plugin()
    seg = (Point(1.0, 2.0, None), Point(3.0, 4.0, None))  # type: ignore[arg-type]
    gen = _RecordingLuaGenerator([_FakeJtac("JTAC Alpha", seg)])

    plugin._inject_option_table(gen)  # type: ignore[arg-type]
    plugin._inject_computed_config(gen)  # type: ignore[arg-type]

    combined = gen.injected_lua()
    assert "dcsRetribution.plugins.MooseAutolase.UnitClasses" in combined
    assert "dcsRetribution.plugins.MooseAutolase.Frontlines" in combined
    # Frontlines table is keyed by region, not group_name
    assert '["Frontline Default"]' in combined
    assert '["JTAC Alpha"]' not in combined.split("Frontlines")[1].split("JTACs")[0]
    assert "DefaultCorridorM = 8000" in combined
    assert "ArtilleryCorridorM = 18000" in combined


def test_inject_jtacs_table_one_entry_per_drone_with_codes_and_bands() -> None:
    # Two JTACs in the same region → two flat entries, each its own callsign,
    # code, bands, and staggered orbitAlt. maxLasing = 1 each. No frontlineIndex.
    gen = _RecordingLuaGenerator(
        jtacs=[
            _FakeJtac(
                group_name="JTAC Alpha",
                callsign="O'Hare 1",
                code="1688",
                uhf_mhz=251,
                vhf_mhz=124,
                region="Frontline A/B",
            ),
            _FakeJtac(
                group_name="JTAC Bravo",
                callsign="Overlord 2",
                code="1687",
                uhf_mhz=252,
                vhf_mhz=125,
                region="Frontline A/B",
            ),
        ]
    )
    plugin = _make_plugin()
    plugin._inject_computed_config(gen)  # type: ignore[arg-type]
    lua = gen.injected_lua()
    assert "MooseAutolase.JTACs" in lua
    # one flat entry per drone — no nested drones table
    assert "drones =" not in lua
    assert lua.count("groupName =") == 2
    assert lua.count("maxLasing = 1") == 2
    # both drones' own callsigns appear (not just the first); apostrophe survives
    assert "O'Hare 1" in lua
    assert "Overlord 2" in lua
    # distinct codes + bands
    assert "laserCode = 1688" in lua
    assert "laserCode = 1687" in lua
    assert "uhf = 251" in lua
    assert "uhf = 252" in lua
    assert "vhf = 124" in lua
    assert "vhf = 125" in lua
    # staggered orbit alts by per-front index (drone 0 → 15000, drone 1 → 17000)
    assert "orbitAlt = 15000" in lua
    assert "orbitAlt = 17000" in lua
    # frontlineIndex is no longer emitted (deconfliction is claim-based)
    assert "frontlineIndex" not in lua


def test_inject_jtacs_empty() -> None:
    gen = _RecordingLuaGenerator(jtacs=[])
    plugin = _make_plugin()
    plugin._inject_computed_config(gen)  # type: ignore[arg-type]
    lua = gen.injected_lua()
    # Table is present but empty
    assert "MooseAutolase.JTACs" in lua


def test_inject_jtacs_one() -> None:
    # One JTAC → one flat entry, maxLasing 1.
    gen = _RecordingLuaGenerator(
        jtacs=[
            _FakeJtac(
                group_name="Solo",
                callsign="Eagle 1",
                code="1111",
                uhf_mhz=300,
                vhf_mhz=150,
            ),
        ]
    )
    plugin = _make_plugin()
    plugin._inject_computed_config(gen)  # type: ignore[arg-type]
    lua = gen.injected_lua()
    assert "orbitAlt = 15000" in lua
    assert "maxLasing = 1" in lua
    assert 'callsign = "Eagle 1"' in lua


def test_inject_jtacs_orbit_alt_stagger_and_cap() -> None:
    """5 JTACs in the same region: orbit alts stagger by 2000 ft per drone index,
    capped at 28000.  All five share a region so the index resets from 0."""
    jtacs = [
        _FakeJtac(
            group_name=f"JTAC {i}",
            callsign=f"X {i}",
            code="1688",
            uhf_mhz=251,
            vhf_mhz=124,
            region="Frontline X/Y",
        )
        for i in range(5)
    ]
    gen = _RecordingLuaGenerator(jtacs=jtacs)
    plugin = _make_plugin()
    plugin._inject_computed_config(gen)  # type: ignore[arg-type]
    lua = gen.injected_lua()
    # Indices 0–4 → 15000, 17000, 19000, 21000, 23000 (all below cap 28000)
    assert "orbitAlt = 15000" in lua
    assert "orbitAlt = 17000" in lua
    assert "orbitAlt = 19000" in lua
    assert "orbitAlt = 21000" in lua
    assert "orbitAlt = 23000" in lua


def test_inject_jtacs_no_vhf_falls_back_to_uhf() -> None:
    """A JTAC with freq_vhf=None must not crash; vhf field should equal the UHF value."""

    class _FakeJtacNoVhf:
        """Minimal JTAC stub with freq_vhf explicitly None (Pretense-style before fix)."""

        def __init__(self, uhf_mhz: int) -> None:
            self.group_name = "Pretense JTAC"
            self.callsign = "Axeman 1"
            self.code = "1688"
            self.freq: RadioFrequency = MHz(uhf_mhz)
            self.freq_vhf: Optional[RadioFrequency] = None
            self.frontline_segment = None
            self.region = "Frontline Default"

    gen = _RecordingLuaGenerator(jtacs=[_FakeJtacNoVhf(uhf_mhz=305)])
    plugin = _make_plugin()
    # Must not raise AttributeError
    plugin._inject_computed_config(gen)  # type: ignore[arg-type]
    lua = gen.injected_lua()
    # Row is present
    assert "MooseAutolase.JTACs" in lua
    assert 'groupName = "Pretense JTAC"' in lua
    # vhf falls back to the UHF value (305)
    assert "vhf = 305" in lua
    assert "uhf = 305" in lua


def test_lua_jtacs_one_entry_per_drone() -> None:
    jtacs = [
        _FakeJtac(
            group_name="JTAC 1",
            callsign="A 1",
            region="Frontline A/B",
            code="1688",
            uhf_mhz=251,
            vhf_mhz=30,
        ),
        _FakeJtac(
            group_name="JTAC 2",
            callsign="A 2",
            region="Frontline A/B",
            code="1687",
            uhf_mhz=252,
            vhf_mhz=31,
        ),
        _FakeJtac(
            group_name="JTAC 3",
            callsign="C 1",
            region="Frontline C/D",
            code="1686",
            uhf_mhz=253,
            vhf_mhz=32,
        ),
    ]
    lua = _lua_jtacs(_FakeMissionData(jtacs))
    # one flat entry per drone (three drones → three entries)
    assert lua.count("groupName =") == 3
    assert lua.count("frontline =") == 3
    assert lua.count("maxLasing = 1") == 3
    assert "drones =" not in lua
    assert "frontlineIndex" not in lua
    assert "laserCode = 1688" in lua
    assert "laserCode = 1687" in lua
    # each drone's own callsign present
    assert 'callsign = "A 1"' in lua
    assert 'callsign = "A 2"' in lua
    assert 'callsign = "C 1"' in lua


def test_lua_frontlines_keyed_by_region_deduped() -> None:
    """_lua_frontlines keys entries by region and deduplicates shared regions."""
    from dcs.mapping import Point

    seg_ab = (Point(1.0, 2.0, None), Point(3.0, 4.0, None))  # type: ignore[arg-type]
    seg_cd = (Point(5.0, 6.0, None), Point(7.0, 8.0, None))  # type: ignore[arg-type]
    jtacs = [
        _FakeJtac(group_name="JTAC 1", region="Frontline A/B", seg=seg_ab),
        # Second JTAC shares region A/B — must produce only one entry
        _FakeJtac(group_name="JTAC 2", region="Frontline A/B", seg=seg_ab),
        _FakeJtac(group_name="JTAC 3", region="Frontline C/D", seg=seg_cd),
    ]
    lua = _lua_frontlines(_FakeMissionData(jtacs))

    # Keys are region strings, not group names
    assert '["Frontline A/B"]' in lua
    assert '["Frontline C/D"]' in lua
    assert '"JTAC 1"' not in lua
    assert '"JTAC 2"' not in lua
    assert '"JTAC 3"' not in lua

    # Dedup: A/B appears only once despite two JTACs sharing it
    assert lua.count('["Frontline A/B"]') == 1

    # Both regions present → two entries total
    assert lua.count("a = {") == 2


def test_inject_hides_ctld_jtac_status_when_ctld_autolase_off() -> None:
    # MooseAutolase's computed config must emit a guarded override that turns off
    # ctld's JTAC Status F10 menu, gated on ctld.autolase being falsy.
    gen = _RecordingLuaGenerator(
        jtacs=[_FakeJtac(group_name="Solo", callsign="Eagle 1")]
    )
    plugin = _make_plugin()
    plugin._inject_computed_config(gen)  # type: ignore[arg-type]
    lua = gen.injected_lua()
    assert "ctld.JTAC_jtacStatusF10 = false" in lua
    # guarded so it is inert when ctld is absent or ctld's own autolase is on
    assert "dcsRetribution.plugins.ctld.autolase" in lua


from game.plugins.manager import LuaPluginManager
from game.plugins.mooseautolase import MooseAutolasePlugin as _MAP


def test_manager_loads_mooseautolase_as_subclass() -> None:
    plugin = {p.identifier: p for p in LuaPluginManager.plugins()}.get("MooseAutolase")
    assert plugin is not None
    assert isinstance(plugin, _MAP)
