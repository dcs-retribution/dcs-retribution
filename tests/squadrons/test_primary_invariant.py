import logging

import pytest

from game.ato.flighttype import FlightType
from game.campaignloader.defaultsquadronassigner import (
    warn_if_primary_not_auto_assignable,
)
from game.dcs.aircrafttype import AircraftType
from game.squadrons.squadron import Squadron


def _squadron(
    aircraft: AircraftType, auto_set: set[FlightType], name: str = "t"
) -> Squadron:
    """Minimal Squadron stub — only the attrs the guard / setter read."""
    sqn: Squadron = object.__new__(Squadron)
    sqn.aircraft = aircraft
    sqn.auto_assignable_mission_types = set(auto_set)
    sqn.name = name
    return sqn


def test_guard_warns_when_primary_missing(caplog: pytest.LogCaptureFixture) -> None:
    aircraft = AircraftType.priority_list_for_task(FlightType.CAS)[0]
    sqn = _squadron(aircraft, {FlightType.STRIKE})
    with caplog.at_level(logging.WARNING):
        warn_if_primary_not_auto_assignable(sqn, FlightType.CAS)
    assert any("auto-assignable" in record.getMessage() for record in caplog.records)


def test_guard_silent_when_primary_present(caplog: pytest.LogCaptureFixture) -> None:
    aircraft = AircraftType.priority_list_for_task(FlightType.CAS)[0]
    sqn = _squadron(aircraft, {FlightType.CAS})
    with caplog.at_level(logging.WARNING):
        warn_if_primary_not_auto_assignable(sqn, FlightType.CAS)
    assert not caplog.records


def test_replace_keeps_primary_over_def_limit() -> None:
    # A squadron limited to a set excluding SEAD, then a campaign that makes SEAD the
    # primary: replace (not intersect) must keep SEAD auto-assignable.
    aircraft = AircraftType.priority_list_for_task(FlightType.SEAD)[0]
    caps = set(aircraft.iter_task_capabilities())
    limited = caps - {
        FlightType.SEAD
    }  # SEAD-capable airframe -> non-empty, excludes SEAD
    sqn = _squadron(aircraft, limited)
    sqn.set_auto_assignable_mission_types({FlightType.SEAD})
    assert FlightType.SEAD in sqn.auto_assignable_mission_types
