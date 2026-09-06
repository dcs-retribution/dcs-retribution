from datetime import datetime

from game.missiongenerator.aircraft.waypoints.seadloiter import _loiter_stop_seconds


def test_loiter_stop_seconds_is_delta_from_now_to_loiter_end() -> None:
    now = datetime(2020, 1, 1, 0, 0, 0)
    loiter_end = datetime(2020, 1, 1, 0, 30, 0)  # 1800 s after now
    assert _loiter_stop_seconds(loiter_end, now) == 1800


def test_loiter_stop_seconds_floors_at_one_when_end_not_after_now() -> None:
    # A loiter-end at or before `now` would yield <= 0 s, which DCS treats as "fire
    # immediately" and kills the orbit at mission start; it must floor to 1.
    now = datetime(2020, 1, 1, 0, 10, 0)
    assert _loiter_stop_seconds(datetime(2020, 1, 1, 0, 10, 0), now) == 1
    assert _loiter_stop_seconds(datetime(2020, 1, 1, 0, 0, 0), now) == 1
