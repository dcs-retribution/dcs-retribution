"""Tests for AirTaskingOrder.shift_time.

The Time & Weather dialog re-times the planned packages when the mission clock
changes instead of wiping and re-planning both ATOs.
"""

from datetime import datetime, timedelta

from game.ato.airtaaskingorder import AirTaskingOrder


class _FakePackage:
    def __init__(self, tot: datetime) -> None:
        self.time_over_target = tot


def test_shift_time_moves_scheduled_packages_by_delta() -> None:
    p1 = _FakePackage(datetime(2020, 1, 1, 12, 0))
    p2 = _FakePackage(datetime(2020, 1, 1, 12, 30))
    ato = AirTaskingOrder(packages=[p1, p2])  # type: ignore[list-item]

    ato.shift_time(timedelta(hours=8))

    # Relative schedule is preserved; both simply move forward by the delta.
    assert p1.time_over_target == datetime(2020, 1, 1, 20, 0)
    assert p2.time_over_target == datetime(2020, 1, 1, 20, 30)


def test_shift_time_supports_negative_delta() -> None:
    p = _FakePackage(datetime(2020, 1, 1, 12, 0))
    ato = AirTaskingOrder(packages=[p])  # type: ignore[list-item]

    ato.shift_time(timedelta(hours=-3))

    assert p.time_over_target == datetime(2020, 1, 1, 9, 0)


def test_shift_time_skips_unscheduled_sentinel() -> None:
    scheduled = _FakePackage(datetime(2020, 1, 1, 12, 0))
    unscheduled = _FakePackage(datetime.min)
    ato = AirTaskingOrder(packages=[scheduled, unscheduled])  # type: ignore[list-item]

    ato.shift_time(timedelta(hours=8))

    assert scheduled.time_over_target == datetime(2020, 1, 1, 20, 0)
    # A never-scheduled package must not be shifted off the sentinel (which would
    # also overflow for large deltas).
    assert unscheduled.time_over_target == datetime.min
