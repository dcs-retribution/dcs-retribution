from datetime import date
from typing import Any

from dcs.planes import FA_18C_hornet, F_16C_50
from dcs.unitpropertydescription import UnitPropertyDescription

from game.dcs.aircraftproperties import (
    HELMET_CUEING_INTRODUCTION_YEARS,
    HELMET_DEVICE_PROPERTY_IDS,
    available_value_ids,
    period_correct_value,
    property_value_available_on,
)


def _helmet_prop(unit_type: Any) -> UnitPropertyDescription:
    prop: UnitPropertyDescription = unit_type.properties["HelmetMountedDevice"]
    # Guard the fixtures: the gate is keyed by these labels/ids.
    assert prop.values is not None
    assert prop.values[1] == "JHMCS"
    return prop


# Real-world JHMCS fielding; bump this constant if the curated year changes.
JHMCS_YEAR = HELMET_CUEING_INTRODUCTION_YEARS["JHMCS"]


def test_helmet_cueing_data_is_loaded_from_yaml() -> None:
    # The gate data lives in resources/aircraftproperties/helmets/*.yaml (mirroring the
    # weapons era data), loaded at import. Guard that every curated entry and the property
    # scope survive the load so a lost/renamed YAML file fails here, not silently.
    assert HELMET_CUEING_INTRODUCTION_YEARS["JHMCS"] == 2003
    assert HELMET_CUEING_INTRODUCTION_YEARS["HMS"] == 1985
    assert HELMET_CUEING_INTRODUCTION_YEARS["SURA Visor"] == 1996
    assert HELMET_CUEING_INTRODUCTION_YEARS["HMCS"] == 2012
    assert HELMET_CUEING_INTRODUCTION_YEARS["HMCS + NVG"] == 2012
    assert "HelmetMountedDevice" in HELMET_DEVICE_PROPERTY_IDS
    assert "HelmetMountedDeviceWSO" in HELMET_DEVICE_PROPERTY_IDS


def test_jhmcs_is_gated_before_its_introduction_year() -> None:
    prop = _helmet_prop(FA_18C_hornet)
    assert property_value_available_on(prop, 1, date(JHMCS_YEAR - 1, 6, 1)) is False
    assert property_value_available_on(prop, 1, date(JHMCS_YEAR, 1, 1)) is True


def test_baseline_and_nvg_options_are_always_available() -> None:
    prop = _helmet_prop(FA_18C_hornet)
    early = date(1995, 1, 1)
    # 0 == "Not installed" (baseline), 2 == "NVG".
    assert property_value_available_on(prop, 0, early) is True
    assert property_value_available_on(prop, 2, early) is True


def test_available_value_ids_drops_jhmcs_pre_introduction() -> None:
    prop = _helmet_prop(F_16C_50)
    assert prop.values is not None
    pre = available_value_ids(prop, date(2000, 1, 1))
    post = available_value_ids(prop, date(JHMCS_YEAR, 1, 1))
    assert 1 not in pre
    assert 0 in pre and 2 in pre
    assert post == list(prop.values)


def test_period_correct_value_clamps_jhmcs_to_baseline() -> None:
    prop = _helmet_prop(FA_18C_hornet)
    # Default is JHMCS (1); pre-introduction it should clamp to the baseline (0).
    assert period_correct_value(prop, 1, date(2000, 1, 1)) == 0
    # Already-period-correct selections are returned unchanged.
    assert period_correct_value(prop, 2, date(2000, 1, 1)) == 2
    # After introduction, JHMCS is kept.
    assert period_correct_value(prop, 1, date(JHMCS_YEAR, 1, 1)) == 1


def test_soviet_hms_is_gated_at_its_own_year() -> None:
    # The MiG-29 shares HelmetMountedDevice id 1 with JHMCS, but its label is "HMS" (the
    # Soviet Shchel-3UM sight, ~1985) — the label key gives it its own earlier year.
    prop = UnitPropertyDescription(
        identifier="HelmetMountedDevice",
        control="comboList",
        label="Helmet Mounted Device",
        default=1,
        values={0: "Not installed", 1: "HMS"},
    )
    assert property_value_available_on(prop, 1, date(1984, 6, 1)) is False
    assert property_value_available_on(prop, 1, date(1985, 1, 1)) is True
    # Pre-1985 it clamps to the baseline, well before JHMCS would even apply.
    assert period_correct_value(prop, 1, date(1980, 1, 1)) == 0


def test_soviet_sura_visor_is_gated_at_its_own_year() -> None:
    # The Su-30 mod shares id 1 but labels it "SURA Visor" (SURA-M, ~1996). It is gated
    # at its own year, not JHMCS's — and not left perpetually available.
    prop = UnitPropertyDescription(
        identifier="HelmetMountedDevice",
        control="comboList",
        label="Helmet Mounted Device",
        default=1,
        values={0: "Not installed", 1: "SURA Visor", 2: "NVG"},
    )
    assert property_value_available_on(prop, 1, date(1995, 1, 1)) is False
    assert property_value_available_on(prop, 1, date(1996, 1, 1)) is True
    # NVG (id 2) is never gated; pre-1996 only SURA drops.
    assert available_value_ids(prop, date(1995, 1, 1)) == [0, 2]
    assert available_value_ids(prop, date(1996, 1, 1)) == [0, 1, 2]


def test_a10c_hmcs_options_are_gated() -> None:
    # The A-10C II shares id 1 ("HMCS") and adds id 2 ("HMCS + NVG"); both carry the
    # Scorpion HMCS (~2012) and are gated, while plain NVG/baseline are not.
    prop = UnitPropertyDescription(
        identifier="HelmetMountedDevice",
        control="comboList",
        label="Helmet Mounted Device",
        default=1,
        values={0: "Not installed", 1: "HMCS", 2: "HMCS + NVG"},
    )
    assert available_value_ids(prop, date(2011, 1, 1)) == [0]
    assert available_value_ids(prop, date(2012, 1, 1)) == [0, 1, 2]


def test_non_helmet_property_is_never_gated() -> None:
    # A property that merely contains a value labelled "JHMCS" but is not a helmet
    # device must not be touched (the gate is scoped to the helmet identifiers).
    prop = UnitPropertyDescription(
        identifier="SomeOtherProperty",
        control="comboList",
        label="Other",
        default=1,
        values={0: "Off", 1: "JHMCS"},
    )
    assert property_value_available_on(prop, 1, date(1995, 1, 1)) is True
