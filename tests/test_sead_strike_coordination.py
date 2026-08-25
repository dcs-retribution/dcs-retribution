"""Cross-package SEAD-before-strike coordination.

Locks the pure window math (delay the naked strike, keep an in-window TOT,
pull a far-late TOT back, clamp to physics, degrade to no-op) and the
scheduler wiring (threat-ring matching, the latest covering provider, player/
ASAP immunity, provider read-only, the setting gate).
"""

from __future__ import annotations

from datetime import datetime, timedelta
from types import SimpleNamespace
from typing import Any, cast
from unittest.mock import patch

from dcs.mapping import Point
from dcs.terrain import Caucasus

from game.ato.flighttype import FlightType
from game.commander.missionscheduler import (
    MissionScheduler,
    coordinated_strike_tot,
)
from game.utils import meters

T0 = datetime(2005, 4, 26, 23, 0)
LEAD = timedelta(minutes=2)
DURATION = timedelta(minutes=8)
_TERRAIN = Caucasus()


def _tot(minutes: float) -> datetime:
    return T0 + timedelta(minutes=minutes)


# --- the pure window math ---


def test_naked_strike_is_delayed_behind_its_sead() -> None:
    assert coordinated_strike_tot(
        _tot(10), _tot(5), [_tot(30)], LEAD, DURATION
    ) == _tot(32)


def test_in_window_strike_keeps_its_tot() -> None:
    assert coordinated_strike_tot(_tot(35), _tot(5), [_tot(30)], LEAD, DURATION) is None


def test_far_late_strike_is_pulled_back_into_the_window() -> None:
    assert coordinated_strike_tot(
        _tot(120), _tot(5), [_tot(30)], LEAD, DURATION
    ) == _tot(32)


def test_pull_back_is_clamped_to_the_earliest_physical_tot() -> None:
    assert coordinated_strike_tot(
        _tot(120), _tot(36), [_tot(30)], LEAD, DURATION
    ) == _tot(36)


def test_unreachable_window_keeps_a_late_tot() -> None:
    # Earliest possible arrival is past the window; the strike is already not
    # ahead of its SEAD, so the spread schedule stands.
    assert (
        coordinated_strike_tot(_tot(120), _tot(50), [_tot(30)], LEAD, DURATION) is None
    )


def test_unreachable_window_still_never_leaves_a_strike_ahead_of_sead() -> None:
    # Can't make the window either, but arriving BEFORE the SEAD is worse:
    # delayed to the earliest physical arrival.
    assert coordinated_strike_tot(
        _tot(20), _tot(50), [_tot(30)], LEAD, DURATION
    ) == _tot(50)


def test_latest_covering_provider_opens_the_window() -> None:
    assert coordinated_strike_tot(
        _tot(10), _tot(5), [_tot(30), _tot(45)], LEAD, DURATION
    ) == _tot(47)


def test_no_providers_is_a_noop() -> None:
    assert coordinated_strike_tot(_tot(10), _tot(5), [], LEAD, DURATION) is None


# --- the scheduler wiring ---

SAM_POS = Point(0, 0, _TERRAIN)
IN_RING = Point(10_000, 0, _TERRAIN)
OUT_OF_RING = Point(100_000, 0, _TERRAIN)
RING = meters(46_300)  # ~25 NM


def _sam_target() -> Any:
    return SimpleNamespace(name="SAM", position=SAM_POS, max_threat_range=lambda: RING)


def _ground_target(position: Point) -> Any:
    # A strike target has no threat ring of its own to worry about here.
    return SimpleNamespace(name="Factory", position=position)


def _package(
    task: FlightType,
    tot: datetime,
    target: Any,
    players: bool = False,
    asap: bool = False,
) -> Any:
    return SimpleNamespace(
        primary_task=task,
        time_over_target=tot,
        target=target,
        has_players=players,
        auto_asap=asap,
    )


def _coordinate(packages: list[Any], on: bool = True) -> None:
    coalition = SimpleNamespace(
        ato=SimpleNamespace(packages=packages),
        game=SimpleNamespace(settings=SimpleNamespace(sead_strike_coordination=on)),
    )
    scheduler = MissionScheduler(cast(Any, coalition), timedelta(hours=1))
    with patch("game.commander.missionscheduler.TotEstimator") as estimator:
        estimator.return_value.earliest_tot.return_value = _tot(5)
        scheduler._coordinate_sead_windows(T0)


def test_strike_in_the_sams_ring_pushes_behind_the_sead() -> None:
    sead = _package(FlightType.SEAD, _tot(30), _sam_target())
    strike = _package(FlightType.STRIKE, _tot(10), _ground_target(IN_RING))
    _coordinate([sead, strike])
    assert strike.time_over_target == _tot(32)
    assert sead.time_over_target == _tot(30)  # provider is read-only


def test_strike_outside_every_ring_keeps_the_spread_schedule() -> None:
    sead = _package(FlightType.SEAD, _tot(30), _sam_target())
    strike = _package(FlightType.STRIKE, _tot(10), _ground_target(OUT_OF_RING))
    _coordinate([sead, strike])
    assert strike.time_over_target == _tot(10)


def test_player_and_asap_strikes_are_never_rescheduled() -> None:
    sead = _package(FlightType.DEAD, _tot(30), _sam_target())
    player = _package(
        FlightType.STRIKE, _tot(10), _ground_target(IN_RING), players=True
    )
    asap = _package(FlightType.BAI, _tot(10), _ground_target(IN_RING), asap=True)
    _coordinate([sead, player, asap])
    assert player.time_over_target == _tot(10)
    assert asap.time_over_target == _tot(10)


def test_player_sead_still_opens_a_window_for_ai_strikes() -> None:
    sead = _package(FlightType.SEAD, _tot(30), _sam_target(), players=True)
    strike = _package(FlightType.OCA_RUNWAY, _tot(10), _ground_target(IN_RING))
    _coordinate([sead, strike])
    assert strike.time_over_target == _tot(32)
    assert sead.time_over_target == _tot(30)


def test_several_strikes_mass_behind_one_sead() -> None:
    sead = _package(FlightType.SEAD, _tot(30), _sam_target())
    early = _package(FlightType.STRIKE, _tot(10), _ground_target(IN_RING))
    late = _package(FlightType.BAI, _tot(110), _ground_target(IN_RING))
    _coordinate([sead, early, late])
    assert early.time_over_target == _tot(32)
    assert late.time_over_target == _tot(32)


def test_setting_off_moves_nothing() -> None:
    sead = _package(FlightType.SEAD, _tot(30), _sam_target())
    strike = _package(FlightType.STRIKE, _tot(10), _ground_target(IN_RING))
    _coordinate([sead, strike], on=False)
    assert strike.time_over_target == _tot(10)


def test_a_dead_sams_zero_ring_opens_no_window() -> None:
    dead_sam = SimpleNamespace(
        name="SAM", position=SAM_POS, max_threat_range=lambda: meters(0)
    )
    sead = _package(FlightType.DEAD, _tot(30), dead_sam)
    strike = _package(FlightType.STRIKE, _tot(10), _ground_target(IN_RING))
    _coordinate([sead, strike])
    assert strike.time_over_target == _tot(10)


# --- CAS and the front-line sandwich ---
#
# A FrontLine is a MissionTarget like any other here: a name and a position, no
# threat ring of its own, so it duck-types as _ground_target does.


def _front_line(position: Point) -> Any:
    return SimpleNamespace(name="Front line Foo/Bar", position=position)


def test_cas_under_a_live_sam_umbrella_pushes_behind_the_dead() -> None:
    dead = _package(FlightType.DEAD, _tot(30), _sam_target())
    cas = _package(FlightType.CAS, _tot(10), _front_line(IN_RING))
    _coordinate([dead, cas])
    assert cas.time_over_target == _tot(32)


def test_cas_on_an_uncovered_front_keeps_the_spread_schedule() -> None:
    dead = _package(FlightType.DEAD, _tot(30), _sam_target())
    cas = _package(FlightType.CAS, _tot(10), _front_line(OUT_OF_RING))
    _coordinate([dead, cas])
    assert cas.time_over_target == _tot(10)


def test_armed_recon_and_air_assault_stay_out_of_the_window() -> None:
    # The two deliberate exclusions, pinned at the same front line the CAS above
    # is retimed at: a loitering sweep is not a push, and an assault is timed by
    # the ground war. Sweeping them in later should fail here first.
    sead = _package(FlightType.SEAD, _tot(30), _sam_target())
    recon = _package(FlightType.ARMED_RECON, _tot(10), _front_line(IN_RING))
    assault = _package(FlightType.AIR_ASSAULT, _tot(10), _front_line(IN_RING))
    _coordinate([sead, recon, assault])
    assert recon.time_over_target == _tot(10)
    assert assault.time_over_target == _tot(10)


def test_cas_and_a_strike_mass_into_one_window() -> None:
    sead = _package(FlightType.SEAD, _tot(30), _sam_target())
    cas = _package(FlightType.CAS, _tot(10), _front_line(IN_RING))
    strike = _package(FlightType.STRIKE, _tot(75), _ground_target(IN_RING))
    _coordinate([sead, cas, strike])
    assert cas.time_over_target == _tot(32)
    assert strike.time_over_target == _tot(32)
