from __future__ import annotations

import logging
from unittest.mock import MagicMock

import pytest

from dcs.task import Modulation

from game.missiongenerator.atisgenerator import AtisGenerator
from game.radio.radios import MHz, RadioRegistry
from game.theater.controlpoint import Airfield


def _airfield(name: str, friendly: bool = True) -> MagicMock:
    cp = MagicMock(spec=Airfield)
    cp.full_name = name
    cp.is_friendly.return_value = friendly
    return cp


def _flight(
    *,
    departure: object = None,
    arrival: object = None,
    divert: object = None,
    client_count: int = 1,
) -> MagicMock:
    flight = MagicMock()
    flight.departure = departure
    flight.arrival = arrival
    flight.divert = divert
    flight.client_count = client_count
    return flight


def _ato(*flights: MagicMock) -> MagicMock:
    package = MagicMock()
    package.flights = list(flights)
    ato = MagicMock()
    ato.packages = [package]
    return ato


def test_allocates_unique_vhf_am_per_player_airfield() -> None:
    registry = RadioRegistry()
    flight = _flight(departure=_airfield("Batumi"), arrival=_airfield("Kobuleti"))
    gen = AtisGenerator(_ato(flight), registry, friendly=MagicMock())
    result = gen.generate()
    assert len(result) == 2
    freqs = {info.frequency.hertz for info in result}
    assert len(freqs) == 2  # unique
    for info in result:
        assert info.frequency.modulation == Modulation.AM
        assert 130_000_000 <= info.frequency.hertz < 140_000_000


def test_deterministic_order_by_airfield_name() -> None:
    flight = _flight(departure=_airfield("Zugdidi"), arrival=_airfield("Anapa"))
    gen = AtisGenerator(_ato(flight), RadioRegistry(), friendly=MagicMock())
    names = [info.airfield_name for info in gen.generate()]
    assert names == ["Anapa", "Zugdidi"]


def test_includes_divert_airfield_and_dedupes_departure_arrival() -> None:
    # Same field for takeoff and landing collapses to one station; the divert
    # adds a second.
    flight = _flight(
        departure=_airfield("Batumi"),
        arrival=_airfield("Batumi"),
        divert=_airfield("Kutaisi"),
    )
    gen = AtisGenerator(_ato(flight), RadioRegistry(), friendly=MagicMock())
    names = sorted(info.airfield_name for info in gen.generate())
    assert names == ["Batumi", "Kutaisi"]


def test_excludes_ai_only_flight_airfields() -> None:
    player = _flight(departure=_airfield("Batumi"), arrival=_airfield("Batumi"))
    ai = _flight(
        departure=_airfield("Senaki"), arrival=_airfield("Senaki"), client_count=0
    )
    gen = AtisGenerator(_ato(player, ai), RadioRegistry(), friendly=MagicMock())
    names = [info.airfield_name for info in gen.generate()]
    assert names == ["Batumi"]


def test_no_player_flights_yields_no_atis() -> None:
    ai = _flight(
        departure=_airfield("Senaki"), arrival=_airfield("Senaki"), client_count=0
    )
    gen = AtisGenerator(_ato(ai), RadioRegistry(), friendly=MagicMock())
    assert gen.generate() == []


def test_skips_frequency_already_reserved() -> None:
    registry = RadioRegistry()
    registry.reserve(MHz(131))  # base slot taken by something else
    flight = _flight(departure=_airfield("Batumi"), arrival=_airfield("Batumi"))
    gen = AtisGenerator(_ato(flight), registry, friendly=MagicMock())
    info = gen.generate()[0]
    assert info.frequency.hertz != MHz(131).hertz  # skipped to next slot


def test_band_exhaustion_logs_and_skips_without_raising(
    caplog: pytest.LogCaptureFixture,
) -> None:
    # 2 slots wide -> 3 player airfields can't all fit; the 3rd is skipped.
    flight = _flight(
        departure=_airfield("A"), arrival=_airfield("B"), divert=_airfield("C")
    )
    gen = AtisGenerator(
        _ato(flight),
        RadioRegistry(),
        friendly=MagicMock(),
        base_mhz=131.0,
        spacing_khz=500,
        window_max_mhz=132.0,  # slots: 131.0, 131.5 -> only 2
    )
    with caplog.at_level(logging.WARNING):
        result = gen.generate()
    assert len(result) == 2
    assert any("exhaust" in r.message.lower() for r in caplog.records)


def test_ignores_non_airfield_and_enemy_control_points() -> None:
    carrier = MagicMock()  # not an Airfield instance
    enemy = _airfield("Mozdok", friendly=False)
    flight = _flight(departure=_airfield("Batumi"), arrival=carrier, divert=enemy)
    gen = AtisGenerator(_ato(flight), RadioRegistry(), friendly=MagicMock())
    result = gen.generate()
    assert [info.airfield_name for info in result] == ["Batumi"]
