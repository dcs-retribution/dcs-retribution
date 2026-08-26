from __future__ import annotations

from game.squadrons.squadron import Squadron


def test_setstate_defaults_intercept_reserve_for_old_saves() -> None:
    # Old saves pickled before this field existed must load with the default.
    squadron = Squadron.__new__(Squadron)
    squadron.__setstate__({"name": "Test", "livery_set": []})
    assert squadron.intercept_reserve == 0


def test_setstate_preserves_saved_intercept_reserve() -> None:
    squadron = Squadron.__new__(Squadron)
    squadron.__setstate__({"name": "Test", "livery_set": [], "intercept_reserve": 3})
    assert squadron.intercept_reserve == 3
