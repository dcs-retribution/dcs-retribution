"""Tests for the PortableTacanGenerator feature."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from game.missiongenerator.tgogenerator import PortableTacanGenerator
from game.radio.tacan import (
    OutOfTacanChannelsError,
    TacanBand,
    TacanChannel,
    TacanRegistry,
    TacanUsage,
)
from game.runways import RunwayData
from game.utils import Heading


def _make_runway_data(
    name: str = "TestAirfield",
    heading: int = 90,
    tacan: TacanChannel | None = None,
    tacan_callsign: str | None = None,
) -> RunwayData:
    return RunwayData(
        airfield_name=name,
        runway_heading=Heading.from_degrees(heading),
        runway_name="09",
        tacan=tacan,
        tacan_callsign=tacan_callsign,
    )


# ---------------------------------------------------------------------------
# Callsign derivation tests
# ---------------------------------------------------------------------------


class TestCallsignDerivation:
    """Test _derive_callsign logic."""

    @staticmethod
    def _make_generator(
        used: set[str] | None = None,
    ) -> PortableTacanGenerator:
        gen = PortableTacanGenerator.__new__(PortableTacanGenerator)
        gen.used_callsigns = used or set()
        return gen

    def test_normal_name(self) -> None:
        gen = self._make_generator()
        assert gen._derive_callsign("Kutaisi") == "KUT"

    def test_name_with_spaces(self) -> None:
        gen = self._make_generator()
        assert gen._derive_callsign("Al Dhafra") == "ALD"

    def test_short_name(self) -> None:
        gen = self._make_generator()
        cs = gen._derive_callsign("AB")
        assert len(cs) == 3
        assert cs == "ABX"

    def test_single_char_name(self) -> None:
        gen = self._make_generator()
        cs = gen._derive_callsign("X")
        assert cs == "XXX"

    def test_name_with_numbers(self) -> None:
        gen = self._make_generator()
        cs = gen._derive_callsign("H4")
        assert len(cs) == 3
        assert cs == "HXX"

    def test_duplicate_avoidance(self) -> None:
        gen = self._make_generator(used={"KUT"})
        cs = gen._derive_callsign("Kutaisi")
        assert cs != "KUT"
        assert len(cs) == 3
        assert cs in gen.used_callsigns

    def test_duplicate_varies_two_chars(self) -> None:
        """When base is taken, the new callsign keeps first char and varies last two."""
        gen = self._make_generator(used={"KUT"})
        cs = gen._derive_callsign("Kutaisi")
        # First collision: suffix=1 -> divmod(0,26) -> (0,0) -> K + A + A
        assert cs == "KAA"

    def test_callsign_exhaustion_raises(self) -> None:
        """RuntimeError should be raised when all 676 variants are exhausted."""
        # Fill all possible 3-letter callsigns starting with 'K'
        used: set[str] = set()
        used.add("KUT")  # the base
        for i in range(26):
            for j in range(26):
                used.add("K" + chr(ord("A") + i) + chr(ord("A") + j))
        gen = self._make_generator(used=used)
        with pytest.raises(RuntimeError, match="Exhausted TACAN callsign variants"):
            gen._derive_callsign("Kutaisi")

    def test_callsign_added_to_used(self) -> None:
        gen = self._make_generator()
        cs = gen._derive_callsign("Batumi")
        assert cs in gen.used_callsigns


# ---------------------------------------------------------------------------
# Generation skip-conditions tests (mocked)
# ---------------------------------------------------------------------------


class TestPortableTacanSkipsWhenAlreadyPresent:
    """PortableTacanGenerator.generate() should skip airfields with existing TACAN."""

    def test_skip_when_tacan_exists(self) -> None:
        """No portable TACAN should be placed if the airfield already has one."""
        existing_tacan = TacanChannel(25, TacanBand.X)
        runway_with_tacan = _make_runway_data(
            tacan=existing_tacan, tacan_callsign="BTM"
        )

        gen = PortableTacanGenerator.__new__(PortableTacanGenerator)
        gen.airfield = MagicMock()
        gen.airfield.airport.runways = [MagicMock()]  # has runways
        gen.airfield.name = "Batumi"
        gen.game = MagicMock()
        gen.tacan_registry = TacanRegistry()
        gen.runways = {}
        gen.used_callsigns = set()
        gen.mission = MagicMock()
        gen.country = MagicMock()

        with patch("game.missiongenerator.tgogenerator.RunwayAssigner") as MockAssigner:
            mock_assigner = MockAssigner.return_value
            mock_assigner.get_preferred_runway.return_value = runway_with_tacan
            gen.generate()

        # No TACAN should have been allocated, no runway stored
        assert len(gen.runways) == 0

    def test_skip_when_no_runways(self) -> None:
        """Heliports without runways should be skipped."""
        gen = PortableTacanGenerator.__new__(PortableTacanGenerator)
        gen.airfield = MagicMock()
        gen.airfield.airport.runways = []
        gen.runways = {}
        gen.generate()
        assert len(gen.runways) == 0

    def test_places_tacan_when_none_exists(self) -> None:
        """A portable TACAN should be placed at an airfield without one."""
        runway_no_tacan = _make_runway_data()
        registry = TacanRegistry()

        gen = PortableTacanGenerator.__new__(PortableTacanGenerator)
        gen.airfield = MagicMock()
        gen.airfield.airport.runways = [MagicMock()]
        gen.airfield.airport.position = MagicMock()
        gen.airfield.airport.position.point_from_heading.return_value = MagicMock()
        gen.airfield.name = "TestAirfield"
        gen.airfield.full_name = "TestAirfield"
        gen.game = MagicMock()
        gen.tacan_registry = registry
        gen.runways = {}
        gen.used_callsigns = set()
        gen.mission = MagicMock()
        gen.country = MagicMock()

        mock_group = MagicMock()
        gen.mission.vehicle_group.return_value = mock_group

        with patch("game.missiongenerator.tgogenerator.RunwayAssigner") as MockAssigner:
            mock_assigner = MockAssigner.return_value
            mock_assigner.get_preferred_runway.return_value = runway_no_tacan
            gen.generate()

        assert "TestAirfield" in gen.runways
        stored = gen.runways["TestAirfield"]
        assert stored.tacan is not None
        assert stored.tacan.band == TacanBand.X
        assert stored.tacan_callsign == "TES"

    def test_graceful_when_channels_exhausted(self) -> None:
        """Should log a warning and skip if no channels are available."""
        runway_no_tacan = _make_runway_data()
        registry = TacanRegistry()

        # Exhaust all valid X-band TransmitReceive channels
        for ch in TacanBand.X.valid_channels(TacanUsage.TransmitReceive):
            registry.mark_unavailable(ch)

        gen = PortableTacanGenerator.__new__(PortableTacanGenerator)
        gen.airfield = MagicMock()
        gen.airfield.airport.runways = [MagicMock()]
        gen.airfield.name = "ExhaustedAirfield"
        gen.game = MagicMock()
        gen.tacan_registry = registry
        gen.runways = {}
        gen.used_callsigns = set()
        gen.mission = MagicMock()
        gen.country = MagicMock()

        with patch("game.missiongenerator.tgogenerator.RunwayAssigner") as MockAssigner:
            mock_assigner = MockAssigner.return_value
            mock_assigner.get_preferred_runway.return_value = runway_no_tacan
            # Should not raise
            gen.generate()

        assert len(gen.runways) == 0
