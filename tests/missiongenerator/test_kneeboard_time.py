"""Kneeboard time rendering, local and Zulu."""

import datetime

from game.missiongenerator.kneeboard import format_kneeboard_time

CAUCASUS = datetime.timezone(datetime.timedelta(hours=4))
LOCAL = datetime.datetime(1988, 7, 15, 7, 19, 13)


def test_local_time_renders_bare() -> None:
    assert format_kneeboard_time(LOCAL) == "07:19:13"


def test_utc_time_carries_the_z_suffix() -> None:
    utc = LOCAL.replace(tzinfo=datetime.timezone.utc)
    assert format_kneeboard_time(utc) == "07:19:13Z"


def test_annotation_puts_zulu_on_a_second_line() -> None:
    """Underneath rather than beside, so the table column does not widen."""
    assert format_kneeboard_time(LOCAL, CAUCASUS) == "07:19:13\n03:19:13Z"


def test_annotation_is_skipped_when_the_time_is_already_zulu() -> None:
    """An airframe on the UTC convention must not get the same time twice."""
    utc = LOCAL.replace(tzinfo=datetime.timezone.utc)
    assert format_kneeboard_time(utc, CAUCASUS) == "07:19:13Z"


def test_missing_time_renders_empty() -> None:
    assert format_kneeboard_time(None, CAUCASUS) == ""
