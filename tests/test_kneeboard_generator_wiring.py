# tests/test_kneeboard_generator_wiring.py
"""Integration: KneeboardGenerator calls generate_recon_pages for each flight."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch

import pytest


def test_generate_flight_kneeboard_calls_generate_recon_pages() -> None:
    from game.missiongenerator.kneeboard import KneeboardGenerator

    flight = MagicMock()
    flight.client_units = [MagicMock()]
    flight.aircraft_type = MagicMock()
    flight.aircraft_type.utc_kneeboard = False
    flight.package = MagicMock()
    flight.package.target = MagicMock()
    flight.friendly = MagicMock()
    flight.waypoints = []
    package_flights: list[Any] = []

    game = MagicMock()
    game.coalition_for.return_value.bullseye.position = MagicMock()
    game.conditions.weather = MagicMock()
    game.conditions.start_time = MagicMock()
    game.settings = MagicMock()
    game.settings.generate_target_recon_kneeboard = True
    game.settings.target_recon_extra_threat_search_nmi = 0
    game.notes = ""

    with patch(
        "game.missiongenerator.kneeboard.generate_recon_pages",
        return_value=[],
    ) as mocked, patch(
        "game.missiongenerator.kneeboard.BriefingPage",
        return_value=MagicMock(),
    ), patch(
        "game.missiongenerator.kneeboard.SupportPage",
        return_value=MagicMock(),
    ):
        gen = KneeboardGenerator.__new__(KneeboardGenerator)
        gen.mission = MagicMock()
        gen.game = game
        gen.dark_kneeboard = False
        gen.comms = []
        gen.awacs = []
        gen.tankers = []
        gen.jtacs = []
        gen.flights = []
        gen.generate_flight_kneeboard(flight, package_flights)
        mocked.assert_called_once()
        # Regression: dark_kneeboard must propagate so the recon-page
        # palette tracks the user's setting. The flag was silently dropped
        # in earlier revisions, leaving recon pages always in light mode.
        _, kwargs = mocked.call_args
        assert kwargs.get("dark") is False


def test_generate_flight_kneeboard_passes_dark_mode_when_enabled() -> None:
    """When dark_kneeboard is True, the flag must reach generate_recon_pages."""
    from game.missiongenerator.kneeboard import KneeboardGenerator

    flight = MagicMock()
    flight.client_units = [MagicMock()]
    flight.aircraft_type = MagicMock()
    flight.aircraft_type.utc_kneeboard = False
    flight.package = MagicMock()
    flight.package.target = MagicMock()
    flight.friendly = MagicMock()
    flight.waypoints = []
    package_flights: list[Any] = []

    game = MagicMock()
    game.coalition_for.return_value.bullseye.position = MagicMock()
    game.conditions.weather = MagicMock()
    game.conditions.start_time = MagicMock()
    game.settings = MagicMock()
    game.settings.generate_target_recon_kneeboard = True
    game.settings.target_recon_extra_threat_search_nmi = 0
    game.notes = ""

    with patch(
        "game.missiongenerator.kneeboard.generate_recon_pages",
        return_value=[],
    ) as mocked, patch(
        "game.missiongenerator.kneeboard.BriefingPage",
        return_value=MagicMock(),
    ), patch(
        "game.missiongenerator.kneeboard.SupportPage",
        return_value=MagicMock(),
    ):
        gen = KneeboardGenerator.__new__(KneeboardGenerator)
        gen.mission = MagicMock()
        gen.game = game
        gen.dark_kneeboard = True
        gen.comms = []
        gen.awacs = []
        gen.tankers = []
        gen.jtacs = []
        gen.flights = []
        gen.generate_flight_kneeboard(flight, package_flights)
        _, kwargs = mocked.call_args
        assert kwargs.get("dark") is True


def test_generate_flight_kneeboard_skips_recon_when_setting_off() -> None:
    from game.missiongenerator.kneeboard import KneeboardGenerator

    flight = MagicMock()
    flight.client_units = [MagicMock()]
    flight.aircraft_type = MagicMock()
    flight.aircraft_type.utc_kneeboard = False
    flight.package = MagicMock()
    flight.package.target = MagicMock()
    flight.friendly = MagicMock()
    flight.waypoints = []
    package_flights: list[Any] = []

    game = MagicMock()
    game.coalition_for.return_value.bullseye.position = MagicMock()
    game.conditions.weather = MagicMock()
    game.conditions.start_time = MagicMock()
    game.settings = MagicMock()
    game.settings.generate_target_recon_kneeboard = False
    game.settings.target_recon_extra_threat_search_nmi = 0
    game.notes = ""

    with patch(
        "game.missiongenerator.kneeboard.generate_recon_pages",
        return_value=[],
    ) as mocked, patch(
        "game.missiongenerator.kneeboard.BriefingPage",
        return_value=MagicMock(),
    ), patch(
        "game.missiongenerator.kneeboard.SupportPage",
        return_value=MagicMock(),
    ):
        gen = KneeboardGenerator.__new__(KneeboardGenerator)
        gen.mission = MagicMock()
        gen.game = game
        gen.dark_kneeboard = False
        gen.comms = []
        gen.awacs = []
        gen.tankers = []
        gen.jtacs = []
        gen.flights = []
        gen.generate_flight_kneeboard(flight, package_flights)
        mocked.assert_not_called()
