# Airport Imagery Offsets

Per-airport reference data derived from OpenStreetMap (and the
Open-Elevation DEM as a fallback elevation source), used by the recon
kneeboard renderer to overlay real-world satellite imagery on top of
DCS-modeled airport positions, place threshold markers at real runway
ends, and reduce sea-level QNH to airfield-level QFE on the ATIS block.

## Files

`<terrain>.json` — one file per shipped DCS terrain. Each file contains:

* `imagery_offset_deg` per airport — the `(dlat, dlng)` translation applied
  to the four lat/lng corners of the basemap extent so the Esri tile
  mosaic overlays where DCS thinks the airport is (DCS terrain placements
  differ from real-world placements by 0–2500 m at typical airports).
* `runways` per airport — real-world runway midpoint, endpoints, length,
  heading. Used by `_compute_thresholds` to place threshold markers at the
  actual runway ends rather than a hard-coded ±900 m from airport center.
* `elevation_m` per airport — field elevation in metres AMSL. Consumed by
  `game/missiongenerator/kneeboard_recon/atis.py::compute_qfe_inhg` to
  reduce sea-level QNH to airfield-level QFE on the ATIS block. The
  briefing page also reads this value to print a `QFE …` line below the
  weather summary. When `elevation_m` is `null`/missing, both consumers
  silently omit the QFE display rather than fabricating a value.
* `elevation_source` per airport — provenance string identifying where the
  elevation came from:
  - `"osm_aerodrome_ele"` — OSM `ele` tag on the `aeroway=aerodrome` feature.
    Generally accurate to ±1 m where mappers used a survey value; some
    contributors enter rough estimates so trust is field-dependent.
    The script handles unit suffixes (`"42 m"`, `"138 ft"`, `"138ft"`)
    and converts feet to metres.
  - `"open_elevation_dem"` — fallback DEM lookup against the
    open-elevation.com public service (backed by SRTM). Typical accuracy
    is ±5–16 m absolute vertical (SRTM3 specification, 90th percentile
    globally; the spec does not promise better accuracy near sea level).
    The service is unauthenticated and has no SLA; it has had
    multi-month outages historically. If you re-run the generator while
    Open-Elevation is down, affected airports lose their elevation entry
    and QFE silently disappears for those fields until the next
    successful regeneration. The script retries each lookup three times
    with exponential backoff and pauses between successive calls so a
    full-terrain run stays gentle on the public instance.
  - `null` — elevation is genuinely unknown for this airport.

## Regenerating

```
PYTHONPATH=. .venv/bin/python scripts/derive_airport_imagery_offsets.py \
    --terrain caucasus
```

One run takes ~30 s per theater (Overpass throttles to ~1 req/s). Re-run
when:
* Eagle Dynamics adds/moves airports in a DCS terrain update.
* OSM mappers correct an obviously-wrong runway heading or elevation.
  Compare against the rendered kneeboard before re-running for the whole
  theater; for one-off corrections, edit the JSON entry by hand instead.
* You upgrade the script (the schema or computation changes).

The cadence does not need to be tight — DCS terrains change infrequently
and OSM corrections are usually small.

## Attribution

Map data © OpenStreetMap contributors, available under the Open Database
License (ODbL): https://www.openstreetmap.org/copyright. Elevation data
for fields tagged `"elevation_source": "open_elevation_dem"` comes from
the Open-Elevation public DEM service, backed by NASA SRTM. The generated
JSON files retain this attribution in the header.
