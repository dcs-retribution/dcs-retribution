# scripts/

Developer/data-generation utilities. Run them from the repo root with the venv
and `PYTHONPATH=.` (they import the `game` package):

```bash
PYTHONPATH=. .venv/bin/python scripts/<script>.py ...
```

## Airfield elevations for kneeboard QFE — `dcs_airfield_elevations.py`

The kneeboard QFE is reduced from QNH using each field's elevation. Those
elevations live in `resources/airport_imagery/<terrain>.json`. They were
originally SRTM/OSM estimates (see `derive_airport_imagery_offsets.py`), which can
be off by tens of metres versus DCS's own terrain mesh — enough to leave the
altimeter 50–75 ft off when you dial QFE. This tool replaces them with DCS's exact
`land.getHeight`, so kneeboard QFE matches the in-sim ATIS.

It's a per-terrain workflow you run for maps you own:

```bash
# 1. build a probe mission for the terrain (valid names below)
PYTHONPATH=. .venv/bin/python scripts/dcs_airfield_elevations.py generate --terrain Syria
#    -> writes atmos_probe_syria.miz

# 2. load atmos_probe_syria.miz in DCS, let it sit a few seconds, quit.
#    The probe logs each airfield's land.getHeight to dcs.log (Saved Games/DCS/Logs/dcs.log)
#    and, if io is available, writes atmos_probe.json (path printed in the [ATMOS] log line).

# 3. preview the change table, then apply it in place (terrain auto-detected from the dump)
PYTHONPATH=. .venv/bin/python scripts/dcs_airfield_elevations.py apply --log <dcs.log> --dry-run
PYTHONPATH=. .venv/bin/python scripts/dcs_airfield_elevations.py apply --log <dcs.log>
```

`apply` reads from `--log <dcs.log>` (reassembles the dump the probe streamed to
the log — works even when DCS sanitizes `io`) or `--dump atmos_probe.json` (the
file the probe writes when `MissionScripting.lua` is de-sanitized). It updates only
`elevation_m` + `elevation_source` per airfield, preserving runway/imagery fields,
and adds an elevation-only stub for any airfield missing from the JSON.

**Valid `--terrain` names:** Afghanistan, Caucasus, Falklands, GermanyColdWar,
Iraq, Kola, MarianaIslands, Nevada, Normandy, PersianGulf, Sinai, Syria, TheChannel.

Implementation: the probe Lua is `resources/plugins/base/dcs_atmos_probe.lua`; the
dump parser is `game/atmosprobe/model.py`; tests live under `tests/atmosprobe/`.

> Note: a de-sanitized `MissionScripting.lua` (the copy Retribution ships at
> `resources/scripts/MissionScripting.lua`) is what lets `io` write a file; without
> it the probe falls back to the dcs.log stream, which `apply --log` consumes.

## Other scripts

- **`derive_airport_imagery_offsets.py`** — generates the
  `resources/airport_imagery/<terrain>.json` files from OpenStreetMap (runway
  geometry + the imagery offset) and Open-Elevation/SRTM (the initial elevations
  that `dcs_airfield_elevations.py` then upgrades). Part of the kneeboard recon
  feature.
- **`gen_recon_kneeboards.py`** — renders the recon kneeboard pages (basemap tiles
  + overlays). Part of the kneeboard recon feature.
