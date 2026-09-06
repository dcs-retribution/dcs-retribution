# tests/atmosprobe/test_model.py
from pathlib import Path

from game.atmosprobe.model import AtmoDump, load_dump

FIXTURE = Path(__file__).parent / "fixtures" / "sample_dump.json"


def test_load_dump_parses_schema() -> None:
    dump: AtmoDump = load_dump(FIXTURE)
    assert dump.schema_version == 1
    assert dump.terrain == "Caucasus"
    assert dump.configured.qnh_mmhg == 750.1
    assert dump.configured.wind.at_8000m.speed_mps == 30.0
    assert len(dump.airbases) == 1
    assert dump.airbases[0].id == "12"
    assert dump.airbases[0].land_height_m == 42.0
    assert dump.airbases[0].surface.pressure_hpa == 994.2
    assert len(dump.columns) == 2
    assert dump.columns[0].label == "airbase:Anapa-Vityazevo"
    assert len(dump.columns[0].rungs) == 3
    assert dump.columns[0].rungs[1].wind.dir_from_deg == 300.0


def test_load_dump_rejects_wrong_schema_version(tmp_path: Path) -> None:
    import json

    import pytest

    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    data["schema_version"] = 999
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError, match="schema_version 999"):
        load_dump(bad)


def test_load_dump_rejects_missing_schema_version(tmp_path: Path) -> None:
    import json

    import pytest

    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    del data["schema_version"]
    bad = tmp_path / "noversion.json"
    bad.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError, match="no schema_version"):
        load_dump(bad)


def test_load_dump_from_log_reassembles_chunks(tmp_path: Path) -> None:
    import json

    from game.atmosprobe.model import load_dump_from_log

    payload = json.dumps(json.loads(FIXTURE.read_text(encoding="utf-8")))
    chunk = 40
    n = (len(payload) + chunk - 1) // chunk
    lines = [f"... INFO SCRIPTING: [ATMOS] JSON-BEGIN bytes={len(payload)} chunks={n}"]
    for i in range(1, n + 1):
        piece = payload[(i - 1) * chunk : i * chunk]
        lines.append(f"... INFO SCRIPTING: [ATMOS] JSON {i}/{n} {piece}")
    lines.append("... INFO SCRIPTING: [ATMOS] JSON-END")
    log = tmp_path / "dcs.log"
    log.write_text("\n".join(lines) + "\n", encoding="utf-8")

    dump = load_dump_from_log(log)
    assert dump.terrain == "Caucasus"
    assert dump.airbases[0].id == "12"
    assert len(dump.columns[0].rungs) == 3


def test_load_dump_from_log_missing_chunk_raises(tmp_path: Path) -> None:
    import pytest

    from game.atmosprobe.model import load_dump_from_log

    log = tmp_path / "dcs.log"
    log.write_text("x [ATMOS] JSON 1/3 {}\nx [ATMOS] JSON 3/3 {}\n", encoding="utf-8")
    with pytest.raises(ValueError, match="missing chunks"):
        load_dump_from_log(log)
