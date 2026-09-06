"""Tests for coordinate formatting helpers."""

from __future__ import annotations

import pytest

from dcs.terrain.caucasus.caucasus import Caucasus
from dcs.mapping import LatLng, Point

from game.missiongenerator.kneeboard_recon.coords import (
    bullseye_bearing_range_nm,
    point_to_dms,
    point_to_mgrs,
)
from game.utils import Heading, nautical_miles


@pytest.fixture(scope="module")
def caucasus() -> Caucasus:
    return Caucasus()


def test_point_to_mgrs_is_38t_for_tbilisi(caucasus: Caucasus) -> None:
    # Tbilisi-Lochini is roughly (41.66 N, 44.95 E) which is MGRS zone 38T MM.
    p = Point.from_latlng(LatLng(41.6692, 44.9547), caucasus)
    result = point_to_mgrs(p)
    assert result.startswith("38T MM "), f"expected 38T MM prefix, got {result!r}"
    parts = result.split()
    assert len(parts) == 3
    assert len(parts[2]) == 10  # easting (5) + northing (5)


def test_point_to_mgrs_uses_five_digit_precision(caucasus: Caucasus) -> None:
    p = Point.from_latlng(LatLng(41.6692, 44.9547), caucasus)
    result = point_to_mgrs(p)
    parts = result.split()
    assert parts[2].isdigit()
    assert len(parts[2]) == 10


def test_point_to_dms_formats_with_decimal_seconds(caucasus: Caucasus) -> None:
    # Format is degrees-minutes-seconds with compass suffix, e.g. 41°40'9.12"N
    p = Point.from_latlng(LatLng(41.6692, 44.9547), caucasus)
    result = point_to_dms(p)
    assert "41°" in result
    assert "N" in result
    assert "44°" in result
    assert "E" in result
    # Decimal seconds are present (format: DD°MM'SS.ss"<dir>)
    assert '"' in result


def test_bullseye_bearing_range_nm_due_east(caucasus: Caucasus) -> None:
    bullseye = Point(0.0, 0.0, caucasus)
    target = Point(0.0, 1852.0, caucasus)
    bearing, range_nm = bullseye_bearing_range_nm(bullseye, target)
    assert bearing == Heading.from_degrees(90)
    assert range_nm == pytest.approx(1.0, abs=0.001)


def test_bullseye_bearing_range_nm_due_south(caucasus: Caucasus) -> None:
    bullseye = Point(0.0, 0.0, caucasus)
    target = Point(-nautical_miles(5).meters, 0.0, caucasus)
    bearing, range_nm = bullseye_bearing_range_nm(bullseye, target)
    assert bearing == Heading.from_degrees(180)
    assert range_nm == pytest.approx(5.0, abs=0.001)
