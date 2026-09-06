"""Derive per-airport imagery offsets and runway geometry from OpenStreetMap.

For a given DCS theater, queries the Overpass API for each airport's real-
world runway data, computes:

* the offset between ``airport.position.latlng()`` (DCS) and the OSM runway
  midpoint (real world), so the satellite basemap can be translated to
  overlay the real airfield where DCS draws its markers,
* the real runway length and per-end threshold lat/lng, so the recon page
  threshold markers can be placed at the actual runway ends instead of the
  hard-coded 900m / 800m offsets currently in ``pages.py``.

Output:
    resources/airport_imagery/<terrain>.json

Usage:
    PYTHONPATH=. .venv/bin/python scripts/derive_airport_imagery_offsets.py \
        --terrain caucasus

    PYTHONPATH=. .venv/bin/python scripts/derive_airport_imagery_offsets.py \
        --terrain caucasus --only-airport Senaki

OpenStreetMap data is licensed under the ODbL. The generated JSON should
include attribution; consumers must propagate that attribution wherever
the derived data is displayed.
"""

from __future__ import annotations

import argparse
import datetime
import json
import math
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Optional

from dcs.terrain.terrain import Terrain

_FEET_TO_METRES = 0.3048
# OSM occasionally exports single-node "ways" (length 0) when a runway has
# been split mid-edit. Drop them before sorting by length — otherwise a
# degenerate way can become the primary runway and zero out heading/midpoint.
_MIN_RUNWAY_LENGTH_M = 10.0


def _parse_osm_ele_metres(raw) -> Optional[float]:
    """Parse the OSM ``ele`` tag, converting imperial units to metres.

    OSM defaults to metres but contributors occasionally write values like
    ``"138 ft"`` or ``"138ft"`` (notably in US-mapped areas). Treating those
    as metres silently 3.28×'s the elevation, which would give a 1000 ft
    QFE error for any field whose OSM elevation was tagged in feet.
    Returns ``None`` for unparseable values.
    """
    if raw is None:
        return None
    s = str(raw).strip()
    if not s:
        return None
    m = re.match(r"^([+-]?\d+(?:\.\d+)?)\s*([A-Za-z']*)\s*", s)
    if not m:
        return None
    try:
        value = float(m.group(1))
    except ValueError:
        return None
    unit = m.group(2).lower()
    if unit in ("ft", "feet", "'"):
        return value * _FEET_TO_METRES
    # OSM default unit is metres (no unit suffix), and "m" is the explicit
    # metric tag. Anything else (rare, e.g. "amsl" suffix) we treat as
    # metres rather than silently failing.
    return value


OVERPASS_URL = "https://overpass-api.de/api/interpreter"
OPEN_ELEVATION_URL = "https://api.open-elevation.com/api/v1/lookup"
USER_AGENT = "retribution-kneeboard-osm-import/1.0"
OVERPASS_TIMEOUT = 60.0
OPEN_ELEVATION_TIMEOUT = 30.0
QUERY_RADIUS_M = 5_000.0
INTER_QUERY_DELAY_S = 1.5  # Overpass fair-use throttling.
OPEN_ELEVATION_DELAY_S = 1.0  # Open-Elevation public-instance throttling.
OVERPASS_RETRY_ATTEMPTS = 3
OVERPASS_RETRY_BACKOFF_S = 5.0  # First retry waits this long; doubles per attempt.
OPEN_ELEVATION_RETRY_ATTEMPTS = 3
OPEN_ELEVATION_RETRY_BACKOFF_S = 5.0


# ----------------------------------------------------------------------------
# Terrain loading
# ----------------------------------------------------------------------------


_TERRAIN_LOADERS = {
    "caucasus": ("dcs.terrain.caucasus.caucasus", "Caucasus"),
    "syria": ("dcs.terrain.syria.syria", "Syria"),
    "persiangulf": ("dcs.terrain.persiangulf.persiangulf", "PersianGulf"),
    "sinai": ("dcs.terrain.sinai.sinai", "Sinai"),
    "nevada": ("dcs.terrain.nevada.nevada", "Nevada"),
    "normandy": ("dcs.terrain.normandy.normandy", "Normandy"),
    "thechannel": ("dcs.terrain.thechannel.thechannel", "TheChannel"),
    "marianaislands": (
        "dcs.terrain.marianaislands.marianaislands",
        "MarianaIslands",
    ),
    "falklands": ("dcs.terrain.falklands.falklands", "Falklands"),
    "kola": ("dcs.terrain.kola.kola", "Kola"),
    "afghanistan": ("dcs.terrain.afghanistan.afghanistan", "Afghanistan"),
    "iraq": ("dcs.terrain.iraq.iraq", "Iraq"),
    "germanycw": ("dcs.terrain.germanycoldwar.germanycoldwar", "GermanyColdWar"),
}


def load_terrain(slug: str) -> Terrain:
    if slug not in _TERRAIN_LOADERS:
        raise SystemExit(
            f"Unknown terrain '{slug}'. Known: {', '.join(_TERRAIN_LOADERS)}"
        )
    module_name, class_name = _TERRAIN_LOADERS[slug]
    module = __import__(module_name, fromlist=[class_name])
    cls = getattr(module, class_name)
    return cls()


# ----------------------------------------------------------------------------
# Overpass query
# ----------------------------------------------------------------------------


def query_overpass(query: str) -> dict:
    """POST a query to Overpass and return parsed JSON.

    Retries on transient failures (HTTP 429/5xx, URLError/timeout) with
    exponential backoff. A single failing airport's traceback used to
    abort the entire terrain run mid-list; the retry loop turns
    Overpass's regular rate-limit responses into pauses instead.
    """
    data = urllib.parse.urlencode({"data": query}).encode()
    last_exc: Optional[BaseException] = None
    for attempt in range(1, OVERPASS_RETRY_ATTEMPTS + 1):
        req = urllib.request.Request(
            OVERPASS_URL,
            data=data,
            headers={"User-Agent": USER_AGENT},
        )
        try:
            with urllib.request.urlopen(req, timeout=OVERPASS_TIMEOUT) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as exc:
            last_exc = exc
            transient = exc.code == 429 or 500 <= exc.code < 600
            if not transient or attempt == OVERPASS_RETRY_ATTEMPTS:
                raise
            wait = OVERPASS_RETRY_BACKOFF_S * (2 ** (attempt - 1))
            print(
                f"    overpass HTTP {exc.code} (attempt {attempt}/"
                f"{OVERPASS_RETRY_ATTEMPTS}); retrying in {wait:.0f}s"
            )
            time.sleep(wait)
        except urllib.error.URLError as exc:
            last_exc = exc
            if attempt == OVERPASS_RETRY_ATTEMPTS:
                raise
            wait = OVERPASS_RETRY_BACKOFF_S * (2 ** (attempt - 1))
            print(
                f"    overpass network error {exc.reason!r} (attempt "
                f"{attempt}/{OVERPASS_RETRY_ATTEMPTS}); retrying in "
                f"{wait:.0f}s"
            )
            time.sleep(wait)
    # Loop only exits via `return` or `raise`. This is unreachable, but
    # keeps the type checker happy.
    assert last_exc is not None  # pragma: no cover
    raise last_exc


def fetch_runways_and_aerodrome(
    lat: float, lng: float
) -> tuple[list[dict], Optional[float]]:
    """Return parsed runway data and any OSM-tagged aerodrome elevation.

    Runway entry: ``{ref, surface, osm_way_id, length_m, heading_deg,
                     midpoint, endpoint_a, endpoint_b}``

    Aerodrome elevation (metres AMSL) is parsed from ``aeroway=aerodrome``
    features within the same query radius — usually present on major
    commercial fields, absent on smaller military strips. Callers should
    fall back to a DEM lookup when this returns ``None``.
    """
    # OSM uses two conventions for closed runways:
    #   1. plain ``aeroway=runway`` with a sibling ``abandoned=yes`` /
    #      ``disused=yes`` flag (favoured by mappers who want the feature
    #      to render as a runway in standard styles), and
    #   2. the lifecycle-prefix form ``abandoned:aeroway=runway`` /
    #      ``disused:aeroway=runway`` / ``former:aeroway=runway`` (more
    #      strictly OSM-canonical; the feature renders as whatever the
    #      ``highway=service`` / etc. tag says).
    # Both forms describe physically existing runway pavement and matter
    # for DCS Cold-War era airfields (Tegel, Brand, Damgarten...), so we
    # query for both. Status is normalised below.
    query = f"""
        [out:json][timeout:{int(OVERPASS_TIMEOUT)}];
        (
          way["aeroway"="runway"](around:{QUERY_RADIUS_M:.0f},{lat},{lng});
          way["abandoned:aeroway"="runway"](around:{QUERY_RADIUS_M:.0f},{lat},{lng});
          way["disused:aeroway"="runway"](around:{QUERY_RADIUS_M:.0f},{lat},{lng});
          way["former:aeroway"="runway"](around:{QUERY_RADIUS_M:.0f},{lat},{lng});
          node["aeroway"="aerodrome"](around:{QUERY_RADIUS_M:.0f},{lat},{lng});
          way["aeroway"="aerodrome"](around:{QUERY_RADIUS_M:.0f},{lat},{lng});
        );
        out body;
        >;
        out skel qt;
    """.strip()

    result = query_overpass(query)
    elements = result.get("elements", [])
    nodes = {e["id"]: e for e in elements if e["type"] == "node"}
    ways = [e for e in elements if e["type"] == "way"]

    # Aerodrome elevation — first feature with a parseable `ele` tag wins.
    aerodrome_ele_m: Optional[float] = None
    for el in elements:
        tags = el.get("tags", {})
        if tags.get("aeroway") != "aerodrome":
            continue
        parsed = _parse_osm_ele_metres(tags.get("ele"))
        if parsed is not None:
            aerodrome_ele_m = parsed
            break

    runways = []
    for way in ways:
        tags = way.get("tags", {})
        is_active = tags.get("aeroway") == "runway"
        is_abandoned_pfx = tags.get("abandoned:aeroway") == "runway"
        is_disused_pfx = tags.get("disused:aeroway") == "runway"
        is_former_pfx = tags.get("former:aeroway") == "runway"
        if not (is_active or is_abandoned_pfx or is_disused_pfx or is_former_pfx):
            continue  # aerodrome polygons handled above
        # Note: we DO include runways tagged `abandoned=yes` or `disused=yes`
        # — these are still physically present and visible in satellite
        # imagery (e.g. Kobuleti's WW2-era unpaved strip is OSM-abandoned but
        # is exactly the runway DCS models). The `status` field below lets
        # downstream consumers distinguish if they care.
        status = "active"
        if is_abandoned_pfx:
            status = "abandoned"
        elif is_disused_pfx:
            status = "disused"
        elif is_former_pfx:
            status = "former"
        elif tags.get("abandoned") == "yes":
            status = "abandoned"
        elif tags.get("disused") == "yes":
            status = "disused"
        coords = [
            (nodes[nid]["lat"], nodes[nid]["lon"])
            for nid in way["nodes"]
            if nid in nodes
        ]
        if len(coords) < 2:
            continue

        # Two endpoints (start, end). For multi-node ways take first/last.
        a_lat, a_lng = coords[0]
        b_lat, b_lng = coords[-1]
        length_m, heading_deg = _length_and_heading(a_lat, a_lng, b_lat, b_lng)
        mid_lat = (a_lat + b_lat) / 2
        mid_lng = (a_lng + b_lng) / 2

        runways.append(
            {
                "ref": tags.get("ref"),
                "surface": tags.get("surface"),
                "status": status,
                "osm_way_id": way["id"],
                "length_m": round(length_m, 1),
                "heading_deg": round(heading_deg, 1),
                "midpoint": {"lat": mid_lat, "lng": mid_lng},
                "endpoint_a": {"lat": a_lat, "lng": a_lng},
                "endpoint_b": {"lat": b_lat, "lng": b_lng},
            }
        )

    # Drop degenerate ways (single-node "runway" features yielded by OSM
    # mid-edit) before the sort — otherwise a length-0 way can become
    # ``primary`` and zero out heading/midpoint downstream.
    runways = [r for r in runways if r["length_m"] >= _MIN_RUNWAY_LENGTH_M]
    runways.sort(key=lambda r: r["length_m"], reverse=True)
    return runways, aerodrome_ele_m


def fetch_elevation_open_elevation(lat: float, lng: float) -> Optional[float]:
    """Query Open-Elevation DEM for a single point. Returns metres AMSL or None.

    Used as fallback when OSM has no ``aeroway=aerodrome`` ``ele`` tag.
    Free service, no auth; backed by SRTM. Returns ``None`` after the
    retry budget is exhausted rather than raising, so a single outage
    only strips elevation from one airfield instead of aborting the
    entire terrain run.
    """
    payload = json.dumps({"locations": [{"latitude": lat, "longitude": lng}]}).encode()
    for attempt in range(1, OPEN_ELEVATION_RETRY_ATTEMPTS + 1):
        req = urllib.request.Request(
            OPEN_ELEVATION_URL,
            data=payload,
            headers={
                "User-Agent": USER_AGENT,
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=OPEN_ELEVATION_TIMEOUT) as resp:
                body = json.load(resp)
            results = body.get("results") or []
            if not results:
                return None
            ele = results[0].get("elevation")
            if ele is None:
                return None
            try:
                return float(ele)
            except (TypeError, ValueError):
                return None
        except urllib.error.HTTPError as exc:
            transient = exc.code == 429 or 500 <= exc.code < 600
            if not transient or attempt == OPEN_ELEVATION_RETRY_ATTEMPTS:
                print(f"    open-elevation HTTP {exc.code}: {exc}")
                return None
            wait = OPEN_ELEVATION_RETRY_BACKOFF_S * (2 ** (attempt - 1))
            print(
                f"    open-elevation HTTP {exc.code} (attempt {attempt}/"
                f"{OPEN_ELEVATION_RETRY_ATTEMPTS}); retrying in {wait:.0f}s"
            )
            time.sleep(wait)
        except Exception as exc:
            if attempt == OPEN_ELEVATION_RETRY_ATTEMPTS:
                print(f"    open-elevation failed: {exc}")
                return None
            wait = OPEN_ELEVATION_RETRY_BACKOFF_S * (2 ** (attempt - 1))
            print(
                f"    open-elevation error {exc!r} (attempt {attempt}/"
                f"{OPEN_ELEVATION_RETRY_ATTEMPTS}); retrying in {wait:.0f}s"
            )
            time.sleep(wait)
    return None


def _length_and_heading(
    lat1: float, lng1: float, lat2: float, lng2: float
) -> tuple[float, float]:
    """Approximate great-circle length (m) and heading (deg) from A to B."""
    lat_mid_rad = math.radians((lat1 + lat2) / 2)
    m_per_deg_lat = 111_133.0
    m_per_deg_lng = 111_320.0 * math.cos(lat_mid_rad)
    dy_m = (lat2 - lat1) * m_per_deg_lat
    dx_m = (lng2 - lng1) * m_per_deg_lng
    length = math.hypot(dx_m, dy_m)
    # Heading: 0 = north, 90 = east; atan2(east, north).
    heading = (math.degrees(math.atan2(dx_m, dy_m)) + 360.0) % 360.0
    return length, heading


# ----------------------------------------------------------------------------
# Per-airport derivation
# ----------------------------------------------------------------------------


def derive_airport(airport) -> Optional[dict]:
    """Return the data record for one DCS airport.

    Filtering by ``--only-airport`` happens in ``main`` before this
    function is called, so the per-call name check (and matching
    ``skipped_filtered`` counter) is unnecessary here.
    """
    dcs_ll = airport.position.latlng()
    try:
        runways, aerodrome_ele_m = fetch_runways_and_aerodrome(dcs_ll.lat, dcs_ll.lng)
    except Exception as exc:
        print(f"  ! Overpass failed for {airport.name}: {exc}")
        return {
            "name": airport.name,
            "dcs_position": {"lat": dcs_ll.lat, "lng": dcs_ll.lng},
            "imagery_offset_deg": None,
            "elevation_m": None,
            "elevation_source": None,
            "runways": [],
            "notes": f"Overpass query failed: {exc!r}",
        }

    if not runways:
        return {
            "name": airport.name,
            "dcs_position": {"lat": dcs_ll.lat, "lng": dcs_ll.lng},
            "imagery_offset_deg": None,
            "elevation_m": None,
            "elevation_source": None,
            "runways": [],
            "notes": "No runway features found in OSM within "
            f"{QUERY_RADIUS_M:.0f}m of DCS airport position.",
        }

    # Imagery offset: align DCS airport.position with the longest runway's
    # midpoint. Markers that DCS computes from airport.position will then
    # overlay the actual runway when the basemap is translated by this
    # offset.
    primary = runways[0]
    offset_lat = primary["midpoint"]["lat"] - dcs_ll.lat
    offset_lng = primary["midpoint"]["lng"] - dcs_ll.lng

    # Elevation: prefer OSM `aeroway=aerodrome` `ele` (surveyed), else fall
    # back to Open-Elevation DEM at the primary-runway midpoint (universal
    # coverage, ±5m SRTM accuracy is plenty for QFE / pattern altitudes).
    elevation_m: Optional[float] = None
    elevation_source: Optional[str] = None
    if aerodrome_ele_m is not None:
        elevation_m = round(aerodrome_ele_m, 1)
        elevation_source = "osm_aerodrome_ele"
    else:
        dem = fetch_elevation_open_elevation(
            primary["midpoint"]["lat"], primary["midpoint"]["lng"]
        )
        # Sleep between successive Open-Elevation calls. The public
        # instance is a volunteer service with no published rate limit;
        # unthrottled bulk POSTs have caused 503s for other users.
        time.sleep(OPEN_ELEVATION_DELAY_S)
        if dem is not None:
            elevation_m = round(dem, 1)
            elevation_source = "open_elevation_dem"

    return {
        "name": airport.name,
        "dcs_position": {"lat": dcs_ll.lat, "lng": dcs_ll.lng},
        "imagery_offset_deg": {"lat": offset_lat, "lng": offset_lng},
        "elevation_m": elevation_m,
        "elevation_source": elevation_source,
        "runways": runways,
    }


def _offset_meters(lat: float, dlat: float, dlng: float) -> dict:
    m_per_deg_lat = 111_133.0
    m_per_deg_lng = 111_320.0 * math.cos(math.radians(lat))
    north_m = dlat * m_per_deg_lat
    east_m = dlng * m_per_deg_lng
    return {
        "north": round(north_m, 1),
        "east": round(east_m, 1),
        "total": round(math.hypot(north_m, east_m), 1),
    }


# ----------------------------------------------------------------------------
# Merge / elevation preservation
# ----------------------------------------------------------------------------


Record = dict[str, Any]

# Elevation sources that are authoritative and must NEVER be overwritten by a
# re-derive. ``dcs_land_getheight`` comes from the in-game atmosphere probe and
# is the QFE ground truth; OSM/DEM values are only a fallback for fields the
# probe never visited. A full re-derive against OSM would otherwise silently
# reset every probed elevation back to a ~5m-accurate SRTM value.
PROTECTED_ELEVATION_SOURCES = frozenset({"dcs_land_getheight"})


def is_never_attempted(record: Record) -> bool:
    """True if a record has neither an imagery offset nor a prior derive note.

    A ``notes`` field means an earlier run already tried this airport and
    found no OSM runway, so ``--fill-missing`` skips it; only airports that
    have never been derived at all are re-attempted.
    """
    return not record.get("imagery_offset_deg") and record.get("notes") is None


def preserve_protected_elevation(existing: Record, derived: Record) -> Record:
    """Return ``derived`` with elevation copied from ``existing`` when the
    existing elevation comes from a protected (authoritative) source.

    Imagery fields always come from ``derived``; only the elevation pair is
    protected.
    """
    if existing.get("elevation_source") in PROTECTED_ELEVATION_SOURCES:
        derived = dict(derived)
        derived["elevation_m"] = existing.get("elevation_m")
        derived["elevation_source"] = existing.get("elevation_source")
    return derived


def merge_airports(
    existing: dict[str, Record], derived: dict[str, Record]
) -> dict[str, Record]:
    """Merge freshly derived airport records over an existing dataset.

    Airports absent from ``derived`` are kept verbatim (so a partial re-derive
    never drops them); re-derived airports take their imagery from ``derived``
    but keep any protected elevation from ``existing``.
    """
    merged: dict[str, Record] = dict(existing)
    for aid, rec in derived.items():
        existing_rec = existing.get(aid)
        merged[aid] = (
            preserve_protected_elevation(existing_rec, rec)
            if existing_rec is not None
            else rec
        )
    return merged


# ----------------------------------------------------------------------------
# Driver
# ----------------------------------------------------------------------------


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--terrain", required=True)
    parser.add_argument(
        "--only-airport",
        default=None,
        help="Restrict to airports whose name contains this substring.",
    )
    parser.add_argument(
        "--out-dir",
        default="resources/airport_imagery",
        help="Output directory for the JSON file.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the result to stdout instead of writing a JSON file.",
    )
    parser.add_argument(
        "--fill-missing",
        action="store_true",
        help="Only derive airports the existing file has never attempted "
        "(no imagery offset and no prior 'no runway' note). Useful after a "
        "terrain update adds new airfields, without re-deriving (and risking "
        "OSM churn on) airfields already imaged.",
    )
    args = parser.parse_args(argv)

    terrain = load_terrain(args.terrain.lower())
    print(f"Loaded terrain: {terrain.name}")

    out_dir = Path(args.out_dir)
    # Filename must match what airport_imagery.load() looks up: terrain.name
    # lowercased with spaces stripped (e.g. "SinaiMap" -> "sinaimap.json").
    out_path = out_dir / f"{terrain.name.lower().replace(' ', '')}.json"

    # Load the existing dataset so a re-derive MERGES into it — preserving
    # protected elevations and any airports not re-derived — instead of
    # rebuilding the file from scratch and clobbering probe elevations.
    existing_airports: dict[str, Record] = {}
    if out_path.exists():
        existing_doc = json.loads(out_path.read_text(encoding="utf-8"))
        existing_airports = existing_doc.get("airports", {})

    airports = list(terrain.airport_list())
    if args.only_airport is not None:
        airports = [a for a in airports if args.only_airport.lower() in a.name.lower()]
    if args.fill_missing:
        airports = [
            a
            for a in airports
            if is_never_attempted(existing_airports.get(str(a.id), {}))
        ]
    if not airports:
        print("No airports matched.")
        return 1

    out = {
        "terrain": terrain.name,
        "source": "OpenStreetMap (ODbL)",
        "attribution": "Map data (c) OpenStreetMap contributors, "
        "ODbL (https://www.openstreetmap.org/copyright)",
        "airports": {},
    }
    derived: dict[str, Record] = {}

    # Sort airports up front so the [i/N] progress order, the iteration
    # order, and the resulting JSON's `airports` dict order are all
    # deterministic across runs and pydcs versions.
    airports.sort(key=lambda a: (a.name, str(a.id)))

    succeeded = 0
    skipped_no_runways = 0
    skipped_no_elevation = 0
    failed = 0
    for i, ap in enumerate(airports, start=1):
        print(f"[{i}/{len(airports)}] {ap.name}")
        record = derive_airport(ap)
        if record is None:
            # ``derive_airport`` no longer self-filters — guard for future
            # callers that re-introduce a None return.
            continue
        derived[str(ap.id)] = record
        offset = record.get("imagery_offset_deg")
        if offset:
            # Compute meters-from-degrees just for the log line; the JSON
            # itself only stores the degree-domain offset (consumers do
            # not need the meters form).
            m = _offset_meters(
                record["dcs_position"]["lat"],
                offset["lat"],
                offset["lng"],
            )
            ele = record.get("elevation_m")
            src = record.get("elevation_source") or "none"
            ele_str = f"{ele}m ({src})" if ele is not None else "no elevation"
            print(
                f"    -> offset {m['total']}m "
                f"(north={m['north']}, east={m['east']}); "
                f"{len(record['runways'])} runway(s); elev {ele_str}"
            )
            succeeded += 1
            if ele is None:
                skipped_no_elevation += 1
        else:
            print(f"    -> {record.get('notes', 'no offset')}")
            if "Overpass query failed" in (record.get("notes") or ""):
                failed += 1
            else:
                skipped_no_runways += 1
        if i < len(airports):
            time.sleep(INTER_QUERY_DELAY_S)

    out["airports"] = merge_airports(existing_airports, derived)
    out["generated_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()

    summary = (
        f"\nSummary: {succeeded} succeeded, {skipped_no_runways} no-runway, "
        f"{failed} overpass-failed, {skipped_no_elevation} missing-elevation "
        f"(total {len(airports)})."
    )

    if args.dry_run:
        # `sort_keys=True` so two runs against the same OSM snapshot
        # produce byte-identical JSON. Combined with the airport-list
        # sort above, this makes the resource files diff-clean.
        json.dump(out, sys.stdout, indent=2, sort_keys=True)
        sys.stdout.write("\n")
        print(summary)
        return 0

    out_dir.mkdir(parents=True, exist_ok=True)
    # Atomic write: write to a per-run unique tempfile in the same
    # directory, then `Path.replace` it onto the final path. Without this
    # a Ctrl-C (or any exception during `json.dump`) used to leave a
    # truncated JSON indistinguishable from a valid one on the next run.
    tmp_path = out_path.with_suffix(
        f"{out_path.suffix}.{os.getpid()}.{time.monotonic_ns()}.tmp"
    )
    try:
        with tmp_path.open("w", encoding="utf-8") as f:
            json.dump(out, f, indent=2, sort_keys=True)
            f.write("\n")
        tmp_path.replace(out_path)
    except BaseException:
        try:
            tmp_path.unlink()
        except OSError:
            pass
        raise
    print(f"\nWrote {out_path}")
    print(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
