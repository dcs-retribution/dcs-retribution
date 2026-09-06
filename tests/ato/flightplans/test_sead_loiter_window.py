from datetime import datetime

from game.ato.flightplans.sead import _loiter_end_time


def test_loiter_end_time_returns_latest_mate_departure() -> None:
    tot = datetime(2020, 1, 1, 0, 10, 0)
    mates = [
        datetime(2020, 1, 1, 0, 15, 0),
        datetime(2020, 1, 1, 0, 22, 0),  # latest
        datetime(2020, 1, 1, 0, 18, 0),
    ]
    assert _loiter_end_time(tot, mates, 1200) == datetime(2020, 1, 1, 0, 22, 0)


def test_loiter_end_time_falls_back_to_window_when_no_mates() -> None:
    tot = datetime(2020, 1, 1, 0, 10, 0)
    # No gating mates -> tot + 1200 s fallback window.
    assert _loiter_end_time(tot, [], 1200) == datetime(2020, 1, 1, 0, 30, 0)


def test_loiter_end_time_floors_at_tot_when_all_mates_depart_earlier() -> None:
    tot = datetime(2020, 1, 1, 0, 10, 0)
    mates = [
        datetime(2020, 1, 1, 0, 5, 0),
        datetime(2020, 1, 1, 0, 8, 0),
    ]
    # All mates leave before the SEAD even arrives; never return a time before TOT.
    assert _loiter_end_time(tot, mates, 1200) == tot
