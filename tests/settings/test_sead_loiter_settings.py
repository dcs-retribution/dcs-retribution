from game.settings import Settings


def test_sead_loiter_standoff_factor_default() -> None:
    assert Settings().sead_loiter_standoff_factor == 0.8


def test_sead_loiter_max_window_seconds_default() -> None:
    assert Settings().sead_loiter_max_window_seconds == 1200
