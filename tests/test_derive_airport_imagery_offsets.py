"""Tests for the merge/elevation-preservation logic in
``scripts.derive_airport_imagery_offsets``.

The derive script rebuilds airport imagery from OpenStreetMap. When a terrain
already carries authoritative ``dcs_land_getheight`` elevations (written by the
in-game probe), re-deriving must NOT overwrite them with OSM/DEM values, and
must leave airports that were not re-derived untouched.
"""

from typing import Any

from scripts.derive_airport_imagery_offsets import (
    is_never_attempted,
    merge_airports,
    preserve_protected_elevation,
)


def _record(**kw: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "name": "X",
        "dcs_position": {"lat": 0.0, "lng": 0.0},
        "imagery_offset_deg": None,
        "elevation_m": None,
        "elevation_source": None,
        "runways": [],
    }
    base.update(kw)
    return base


def test_preserve_protected_elevation_keeps_dcs_value() -> None:
    existing = _record(elevation_m=250.0, elevation_source="dcs_land_getheight")
    derived = _record(
        elevation_m=240.0,
        elevation_source="open_elevation_dem",
        imagery_offset_deg={"lat": 0.1, "lng": 0.2},
    )
    merged = preserve_protected_elevation(existing, derived)
    assert merged["elevation_m"] == 250.0
    assert merged["elevation_source"] == "dcs_land_getheight"
    # Imagery is still taken from the freshly derived record.
    assert merged["imagery_offset_deg"] == {"lat": 0.1, "lng": 0.2}


def test_preserve_protected_elevation_refreshes_unprotected() -> None:
    existing = _record(elevation_m=100.0, elevation_source="open_elevation_dem")
    derived = _record(elevation_m=110.0, elevation_source="osm_aerodrome_ele")
    merged = preserve_protected_elevation(existing, derived)
    assert merged["elevation_m"] == 110.0
    assert merged["elevation_source"] == "osm_aerodrome_ele"


def test_merge_keeps_existing_airports_not_rederived() -> None:
    existing = {
        "1": _record(
            name="A", elevation_m=250.0, elevation_source="dcs_land_getheight"
        ),
        "2": _record(
            name="B", elevation_m=300.0, elevation_source="dcs_land_getheight"
        ),
    }
    derived = {
        "1": _record(
            name="A",
            elevation_m=99.0,
            elevation_source="open_elevation_dem",
            imagery_offset_deg={"lat": 1.0, "lng": 2.0},
        )
    }
    merged = merge_airports(existing, derived)
    # id 2 was not re-derived: kept verbatim.
    assert merged["2"]["elevation_m"] == 300.0
    # id 1: imagery updated, protected elevation preserved.
    assert merged["1"]["imagery_offset_deg"] == {"lat": 1.0, "lng": 2.0}
    assert merged["1"]["elevation_m"] == 250.0
    assert merged["1"]["elevation_source"] == "dcs_land_getheight"


def test_merge_adds_brand_new_airport() -> None:
    existing = {
        "1": _record(name="A", elevation_m=250.0, elevation_source="dcs_land_getheight")
    }
    derived = {"9": _record(name="New", imagery_offset_deg={"lat": 3.0, "lng": 4.0})}
    merged = merge_airports(existing, derived)
    assert merged["9"]["imagery_offset_deg"] == {"lat": 3.0, "lng": 4.0}
    assert merged["1"]["elevation_m"] == 250.0


def test_is_never_attempted() -> None:
    assert is_never_attempted(_record()) is True
    assert is_never_attempted(_record(notes="No runway features found")) is False
    assert (
        is_never_attempted(_record(imagery_offset_deg={"lat": 1.0, "lng": 2.0}))
        is False
    )
