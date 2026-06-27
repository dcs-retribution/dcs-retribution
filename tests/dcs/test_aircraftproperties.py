from datetime import date
from typing import Any

from dcs.planes import FA_18C_hornet, F_16C_50
from dcs.unitpropertydescription import UnitPropertyDescription

from game.dcs.aircraftproperties import (
    HELMET_CUEING_INTRODUCTION_YEARS,
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


def test_soviet_sura_visor_is_not_gated() -> None:
    # Su-30/Su-35 share the HelmetMountedDevice id 1 but it is the 1980s "SURA Visor",
    # not JHMCS — keying the gate on the label (not the id) must leave it available.
    prop = UnitPropertyDescription(
        identifier="HelmetMountedDevice",
        control="comboList",
        label="Helmet Mounted Device",
        default=0,
        values={0: "Not installed", 1: "SURA Visor", 2: "NVG"},
    )
    assert property_value_available_on(prop, 1, date(1995, 1, 1)) is True
    assert available_value_ids(prop, date(1995, 1, 1)) == [0, 1, 2]


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
