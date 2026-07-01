from __future__ import annotations

from game.theater.controlpoint import PresetLocations


def test_motorpools_defaults_to_empty_list() -> None:
    assert PresetLocations().motorpools == []


def test_motorpools_is_independent_per_instance() -> None:
    a = PresetLocations()
    b = PresetLocations()
    a.motorpools.append(object())  # type: ignore[arg-type]
    assert b.motorpools == []
