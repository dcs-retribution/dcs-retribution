"""Tests for the per-aircraft era gate on payload-editor properties (§24).

The gate data lives in each aircraft's own ``resources/units/aircraft/<type>.yaml``
(the ``date_gated_properties`` block) and loads into
``AircraftType.property_date_gate`` as a :class:`PropertyDateGate`. These tests pin
both halves: the gate's behavior on the real pydcs property descriptions, and the
data's continued agreement with pydcs — a pydcs value-label rename would silently
degrade a label-keyed gate to "not gated", so the label pin fails loudly instead.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest
from dcs.planes import FA_18C_hornet, F_16C_50
from dcs.unitpropertydescription import UnitPropertyDescription

from game import persistency
from game.dcs.aircraftproperties import PropertyDateGate
from game.dcs.aircrafttype import AircraftType

# Real-world JHMCS fielding; keep in lockstep with the aircraft yaml data.
JHMCS_YEAR = 2003

#: The DCS types whose data files carry a ``date_gated_properties`` block — exactly
#: the airframes pydcs confirms expose the ``HelmetMountedDevice`` property.
GATED_DCS_IDS = {"FA-18C_hornet", "F-16C_50", "A-10C_2", "MiG-29 Fulcrum"}


@pytest.fixture(autouse=True)
def _persistency(tmp_path: Path) -> None:
    # AircraftType loads the unit data files, which reach for the saved-games
    # folder; point it at a throwaway dir so the registry can populate.
    persistency.setup(str(tmp_path), prefer_liberation_payloads=False, port=16884)


def _hornet_gate() -> tuple[PropertyDateGate, UnitPropertyDescription]:
    aircraft = AircraftType.named("F/A-18C Hornet (Lot 20)")
    prop = aircraft.dcs_unit_type.properties["HelmetMountedDevice"]
    return aircraft.property_date_gate, prop


def test_registry_gates_exactly_the_helmet_airframes() -> None:
    # The full registry loads, and a (non-empty) gate lands on exactly the four
    # airframes whose yaml declares the block — nothing leaks onto other types.
    gated = {a.dcs_id for a in AircraftType.iter_all() if a.property_date_gate}
    assert gated == GATED_DCS_IDS


def test_gated_labels_still_exist_in_pydcs() -> None:
    # The gate is keyed by value *label*. If a pydcs update renames a label (e.g.
    # "JHMCS"), the gate silently degrades to "not gated" — pin every gated label
    # against the live pydcs property values so that degradation fails CI instead.
    for aircraft in AircraftType.iter_all():
        gate = aircraft.property_date_gate
        for identifier, labels in gate.introduction_years.items():
            prop = aircraft.dcs_unit_type.properties.get(identifier)
            assert prop is not None, f"{aircraft.dcs_id}: no property {identifier}"
            assert prop.values is not None
            missing = set(labels) - set(prop.values.values())
            assert not missing, (
                f"{aircraft.dcs_id}: gated labels {sorted(missing)} no longer exist "
                f"on pydcs property {identifier} (values: {prop.values})"
            )


def test_jhmcs_is_gated_before_its_introduction_year() -> None:
    gate, prop = _hornet_gate()
    assert prop.values is not None and prop.values[1] == "JHMCS"
    assert gate.value_available_on(prop, 1, date(JHMCS_YEAR - 1, 6, 1)) is False
    assert gate.value_available_on(prop, 1, date(JHMCS_YEAR, 1, 1)) is True


def test_baseline_and_nvg_options_are_always_available() -> None:
    gate, prop = _hornet_gate()
    early = date(1995, 1, 1)
    # 0 == "Not installed" (baseline), 2 == "NVG".
    assert gate.value_available_on(prop, 0, early) is True
    assert gate.value_available_on(prop, 2, early) is True


def test_available_value_ids_drops_jhmcs_pre_introduction() -> None:
    aircraft = next(a for a in AircraftType.iter_all() if a.dcs_unit_type is F_16C_50)
    gate = aircraft.property_date_gate
    prop = F_16C_50.properties["HelmetMountedDevice"]
    assert prop.values is not None
    pre = gate.available_value_ids(prop, date(2000, 1, 1))
    post = gate.available_value_ids(prop, date(JHMCS_YEAR, 1, 1))
    assert 1 not in pre
    assert 0 in pre and 2 in pre
    assert post == list(prop.values)


def test_period_correct_value_clamps_jhmcs_to_baseline() -> None:
    gate, prop = _hornet_gate()
    # Default is JHMCS (1); pre-introduction it should clamp to the baseline (0).
    assert gate.period_correct_value(prop, 1, date(2000, 1, 1)) == 0
    # Already-period-correct selections are returned unchanged.
    assert gate.period_correct_value(prop, 2, date(2000, 1, 1)) == 2
    # After introduction, JHMCS is kept.
    assert gate.period_correct_value(prop, 1, date(JHMCS_YEAR, 1, 1)) == 1


def test_ungated_airframe_has_an_empty_gate_that_gates_nothing() -> None:
    # An aircraft with no date_gated_properties block gets the falsy empty gate,
    # and every value stays available in every era.
    aircraft = AircraftType.named("F-14A Tomcat (Block 135-GR Late)")
    gate = aircraft.property_date_gate
    assert not gate
    early = date(1950, 1, 1)
    for prop in aircraft.dcs_unit_type.properties.values():
        if prop.values is None:
            continue
        assert gate.available_value_ids(prop, early) == list(prop.values)
    assert list(gate.gated_props(aircraft.dcs_unit_type.properties)) == []


def test_non_gated_property_of_a_gated_airframe_is_never_touched() -> None:
    # The gate is scoped by property identifier: a different property that merely
    # contains a value labelled "JHMCS" must not be gated.
    gate, _ = _hornet_gate()
    other = UnitPropertyDescription(
        identifier="SomeOtherProperty",
        control="comboList",
        label="Other",
        default=1,
        values={0: "Off", 1: "JHMCS"},
    )
    assert gate.value_available_on(other, 1, date(1995, 1, 1)) is True
    assert gate.available_value_ids(other, date(1995, 1, 1)) == [0, 1]


def test_gated_props_iterates_exactly_the_curated_identifiers() -> None:
    gate, prop = _hornet_gate()
    props = list(gate.gated_props(FA_18C_hornet.properties))
    assert [p.identifier for p in props] == ["HelmetMountedDevice"]


def test_soviet_hms_and_a10_hmcs_gate_by_their_own_years() -> None:
    # Per-aircraft data: the MiG-29's HMS (1983) and the A-10C II's Scorpion HMCS
    # (2012) carry their own years, independent of JHMCS.
    mig = next(a for a in AircraftType.iter_all() if a.dcs_id == "MiG-29 Fulcrum")
    mig_prop = mig.dcs_unit_type.properties["HelmetMountedDevice"]
    assert (
        mig.property_date_gate.value_available_on(mig_prop, 1, date(1982, 1, 1))
        is False
    )
    assert (
        mig.property_date_gate.value_available_on(mig_prop, 1, date(1983, 1, 1)) is True
    )

    a10 = next(a for a in AircraftType.iter_all() if a.dcs_id == "A-10C_2")
    a10_prop = a10.dcs_unit_type.properties["HelmetMountedDevice"]
    # Both the HMCS and the HMCS + NVG combination are gated to 2012.
    assert a10.property_date_gate.available_value_ids(a10_prop, date(2010, 1, 1)) == [0]
    assert (
        a10.property_date_gate.period_correct_value(a10_prop, 1, date(2010, 1, 1)) == 0
    )
    assert a10.property_date_gate.available_value_ids(a10_prop, date(2012, 1, 1)) == [
        0,
        1,
        2,
    ]


def test_from_data_tolerates_absence() -> None:
    assert not PropertyDateGate.from_data(None)
    assert not PropertyDateGate.from_data({})
    gate = PropertyDateGate.from_data({"HelmetMountedDevice": {"JHMCS": 2003}})
    assert gate
    assert gate.introduction_years == {"HelmetMountedDevice": {"JHMCS": 2003}}
