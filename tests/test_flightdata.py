"""Tests for FlightData dataclass."""

import ast
from pathlib import Path

import pytest

from game.missiongenerator.aircraft.flightdata import FlightData

_GAME_ROOT = Path(__file__).resolve().parent.parent / "game"


def test_start_type_field_exists() -> None:
    """FlightData must declare a start_type field."""
    assert "start_type" in FlightData.__dataclass_fields__


def test_construction_without_start_type_raises() -> None:
    """Omitting start_type must raise TypeError."""
    with pytest.raises(TypeError):
        FlightData(  # type: ignore[call-arg]
            package=None,  # type: ignore[arg-type]
            flight_type=None,  # type: ignore[arg-type]
            aircraft_type=None,  # type: ignore[arg-type]
            units=[],
            size=0,
            friendly=True,  # type: ignore[arg-type]
            departure_delay=None,  # type: ignore[arg-type]
            arrival=None,  # type: ignore[arg-type]
            departure=None,  # type: ignore[arg-type]
            divert=None,
            waypoints=[],
            intra_flight_channel=None,  # type: ignore[arg-type]
            bingo_fuel=None,
            joker_fuel=None,
            laser_codes=[],
            custom_name=None,
            # start_type intentionally omitted
        )


def _flightdata_construction_sites() -> list[tuple[Path, int, set[str]]]:
    """Walk game/ for `FlightData(...)` call sites; return (path, line, kwarg-names)."""
    sites: list[tuple[Path, int, set[str]]] = []
    for py in _GAME_ROOT.rglob("*.py"):
        try:
            tree = ast.parse(py.read_text(encoding="utf-8"), filename=str(py))
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            if isinstance(func, ast.Name) and func.id == "FlightData":
                kwargs = {kw.arg for kw in node.keywords if kw.arg}
                sites.append((py, node.lineno, kwargs))
    return sites


def test_every_flightdata_construction_passes_start_type() -> None:
    """Every `FlightData(...)` call in game/ must pass start_type=.

    Regression guard: a new required field was once added to FlightData
    without updating PretenseFlightGroupConfigurator, which broke every
    Pretense mission gen at runtime. AST scan catches this contract drift.
    """
    sites = _flightdata_construction_sites()
    assert sites, "expected to find FlightData construction sites in game/"
    missing = [
        (str(path.relative_to(_GAME_ROOT.parent)), line)
        for path, line, kwargs in sites
        if "start_type" not in kwargs
    ]
    assert not missing, f"FlightData callers missing required start_type=: {missing}"
