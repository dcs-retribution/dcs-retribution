"""Tests for the curated carrier comms plans."""

from __future__ import annotations

from unittest.mock import MagicMock

from dcs.ships import CVN_71, KUZNECOW, LHA_Tarawa, Stennis

from game.data.carrier_comms import CARRIER_COMMS_PLANS
from game.missiongenerator.tgogenerator import (
    CarrierGenerator,
    GenericCarrierGenerator,
    IclsAllocator,
    LINK4_CARRIERS,
)
from game.radio.radios import MHz, RadioRegistry
from game.radio.tacan import (
    UNAVAILABLE,
    TacanBand,
    TacanChannel,
    TacanRegistry,
    TacanUsage,
)
from game.unitmap import UnitMap

# ---------------------------------------------------------------------------
# Table invariants
# ---------------------------------------------------------------------------


class TestCommsPlanTable:
    def test_tacan_channels_unique(self) -> None:
        channels = [plan.tacan for plan in CARRIER_COMMS_PLANS.values()]
        assert len(channels) == len(set(channels))

    def test_tacan_channels_valid_for_ship_beacons(self) -> None:
        """Curated channels must be legal for a transmit/receive beacon."""
        excluded = UNAVAILABLE[TacanUsage.TransmitReceive][TacanBand.X]
        for plan in CARRIER_COMMS_PLANS.values():
            assert plan.tacan.band is TacanBand.X
            assert 1 <= plan.tacan.number <= 126
            assert plan.tacan.number not in excluded

    def test_atc_frequencies_unique(self) -> None:
        freqs = [plan.atc for plan in CARRIER_COMMS_PLANS.values()]
        assert len(freqs) == len(set(freqs))

    def test_icls_channels_unique_and_valid(self) -> None:
        channels = [
            plan.icls for plan in CARRIER_COMMS_PLANS.values() if plan.icls is not None
        ]
        assert len(channels) == len(set(channels))
        assert all(1 <= ch <= 20 for ch in channels)

    def test_link4_in_acls_band(self) -> None:
        freqs = [
            plan.link4
            for plan in CARRIER_COMMS_PLANS.values()
            if plan.link4 is not None
        ]
        assert len(freqs) == len(set(freqs))
        assert all(MHz(336).hertz <= f.hertz <= MHz(337).hertz for f in freqs)

    def test_idents_are_short_uppercase(self) -> None:
        for plan in CARRIER_COMMS_PLANS.values():
            assert plan.tacan_ident.isalpha()
            assert plan.tacan_ident == plan.tacan_ident.upper()
            assert len(plan.tacan_ident) == 3

    def test_link4_capable_hulls_carry_full_deck_data(self) -> None:
        """Every ACLS-capable hull in the table must have ICLS and Link 4."""
        for carrier_type in LINK4_CARRIERS:
            plan = CARRIER_COMMS_PLANS[carrier_type.id]
            assert plan.icls is not None
            assert plan.link4 is not None

    def test_lha_and_kuznetsov_scope(self) -> None:
        assert CARRIER_COMMS_PLANS[LHA_Tarawa.id].icls is not None
        assert CARRIER_COMMS_PLANS[LHA_Tarawa.id].link4 is None
        assert CARRIER_COMMS_PLANS[KUZNECOW.id].icls is None
        assert CARRIER_COMMS_PLANS[KUZNECOW.id].link4 is None


# ---------------------------------------------------------------------------
# ICLS allocator
# ---------------------------------------------------------------------------


class TestIclsAllocator:
    def test_claim_free_channel(self) -> None:
        alloc = IclsAllocator()
        assert alloc.claim(11) == 11
        assert alloc.claim(11) is None

    def test_alloc_skips_claimed(self) -> None:
        alloc = IclsAllocator()
        alloc.claim(1)
        alloc.reserve(2)
        assert alloc.alloc() == 3

    def test_alloc_exhaustion(self) -> None:
        alloc = IclsAllocator()
        for _ in range(20):
            alloc.alloc()
        try:
            alloc.alloc()
        except RuntimeError:
            return
        raise AssertionError("expected RuntimeError when ICLS channels exhausted")


# ---------------------------------------------------------------------------
# Comms resolution (curated -> fallback -> stored precedence)
# ---------------------------------------------------------------------------


def _make_generator() -> GenericCarrierGenerator:
    gen = CarrierGenerator.__new__(CarrierGenerator)
    gen.control_point = MagicMock()
    gen.control_point.frequency = None
    gen.control_point.tacan = None
    gen.control_point.tcn_name = None
    gen.control_point.link4 = None
    gen.control_point.icls_channel = None
    gen.radio_registry = RadioRegistry()
    gen.tacan_registry = TacanRegistry()
    gen.icls_alloc = IclsAllocator()
    gen.unit_map = UnitMap()
    return gen


class TestCommsResolution:
    def test_curated_tacan(self) -> None:
        gen = _make_generator()
        plan = CARRIER_COMMS_PLANS[CVN_71.id]
        tacan, ident = gen._resolve_tacan(plan)
        assert tacan == TacanChannel(71, TacanBand.X)
        assert ident == "TRO"
        # Persisted for later turns and reserved against reuse.
        assert gen.control_point.tacan == tacan
        assert gen.control_point.tcn_name == "TRO"
        assert tacan in gen.tacan_registry.allocated_channels

    def test_curated_tacan_taken_falls_back_to_neighbor(self) -> None:
        """A map-owned hull channel degrades to the nearest free channel
        (Bagram owns 74X on Afghanistan), not to the bottom of the band."""
        gen = _make_generator()
        plan = CARRIER_COMMS_PLANS[CVN_71.id]
        gen.tacan_registry.mark_unavailable(plan.tacan)
        tacan, ident = gen._resolve_tacan(plan)
        assert tacan in (
            TacanChannel(70, TacanBand.X),
            TacanChannel(72, TacanBand.X),
        )
        assert ident == "TRO"

    def test_stored_tacan_wins(self) -> None:
        gen = _make_generator()
        stored = TacanChannel(42, TacanBand.X)
        gen.control_point.tacan = stored
        gen.control_point.tcn_name = "OLD"
        tacan, ident = gen._resolve_tacan(CARRIER_COMMS_PLANS[CVN_71.id])
        assert tacan == stored
        assert ident == "OLD"

    def test_no_plan_uses_legacy_allocator(self) -> None:
        gen = _make_generator()
        tacan, ident = gen._resolve_tacan(None)
        assert tacan is not None
        assert len(ident) == 3

    def test_curated_atc_reserved_and_persisted(self) -> None:
        gen = _make_generator()
        plan = CARRIER_COMMS_PLANS[CVN_71.id]
        atc = gen._resolve_atc(plan)
        assert atc == MHz(305)
        assert atc in gen.radio_registry.allocated_channels
        assert gen.control_point.frequency == atc

    def test_curated_atc_taken_falls_back(self) -> None:
        gen = _make_generator()
        plan = CARRIER_COMMS_PLANS[CVN_71.id]
        gen.radio_registry.reserve(plan.atc)
        atc = gen._resolve_atc(plan)
        assert atc != plan.atc
        assert gen.control_point.frequency == atc

    def test_stored_atc_wins(self) -> None:
        gen = _make_generator()
        gen.control_point.frequency = MHz(271)
        atc = gen._resolve_atc(CARRIER_COMMS_PLANS[CVN_71.id])
        assert atc == MHz(271)

    def test_curated_link4(self) -> None:
        gen = _make_generator()
        plan = CARRIER_COMMS_PLANS[CVN_71.id]
        link4 = gen._resolve_link4(plan, CVN_71)
        assert link4 == plan.link4
        assert link4 in gen.radio_registry.allocated_channels
        assert gen.control_point.link4 == link4

    def test_link4_none_for_non_acls_hull(self) -> None:
        gen = _make_generator()
        assert gen._resolve_link4(CARRIER_COMMS_PLANS[KUZNECOW.id], KUZNECOW) is None
        assert (
            gen._resolve_link4(CARRIER_COMMS_PLANS[LHA_Tarawa.id], LHA_Tarawa) is None
        )

    def test_curated_icls_and_second_boat_fallback(self) -> None:
        gen = _make_generator()
        plan = CARRIER_COMMS_PLANS[Stennis.id]
        assert gen._resolve_icls(plan, Stennis) == plan.icls
        # A second boat of the same hull cannot reuse the channel.
        second = _make_generator()
        second.icls_alloc = gen.icls_alloc
        assert second._resolve_icls(plan, Stennis) == 1

    def test_stored_icls_reserved(self) -> None:
        gen = _make_generator()
        gen.control_point.icls_channel = 1
        assert gen._resolve_icls(CARRIER_COMMS_PLANS[CVN_71.id], CVN_71) == 1
        assert gen.icls_alloc.alloc() == 2

    def test_icls_none_for_kuznetsov(self) -> None:
        gen = _make_generator()
        assert gen._resolve_icls(CARRIER_COMMS_PLANS[KUZNECOW.id], KUZNECOW) is None


# ---------------------------------------------------------------------------
# Flagship naming
# ---------------------------------------------------------------------------


class TestFlagshipName:
    def test_clean_hull_name(self) -> None:
        gen = _make_generator()
        assert gen._flagship_name(CVN_71) == "CVN-71 Theodore Roosevelt"

    def test_duplicate_falls_back_to_unique_name(self) -> None:
        gen = _make_generator()
        dcs_unit = MagicMock()
        dcs_unit.name = "CVN-71 Theodore Roosevelt"
        gen.unit_map.add_theater_unit_mapping(MagicMock(), dcs_unit)
        assert gen._flagship_name(CVN_71) is None
