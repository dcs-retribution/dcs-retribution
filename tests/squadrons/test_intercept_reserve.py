from __future__ import annotations

from game.squadrons.intercept_reserve import (
    clamp_intercept_reserve,
    max_intercept_reserve,
    qra_resource_count,
    repropagated_intercept_reserve,
    seeded_intercept_reserve,
    untasked_after_reserve_change,
)


def test_non_barcap_squadron_is_unchanged() -> None:
    assert seeded_intercept_reserve(False, 0, 4, 12) == 0


def test_explicit_non_zero_reserve_is_preserved() -> None:
    assert seeded_intercept_reserve(True, 3, 4, 12) == 3


def test_barcap_squadron_seeded_from_default() -> None:
    assert seeded_intercept_reserve(True, 0, 4, 12) == 4


def test_seed_is_clamped_to_max_size() -> None:
    assert seeded_intercept_reserve(True, 0, 10, 4) == 4


def test_zero_default_leaves_reserve_at_zero() -> None:
    assert seeded_intercept_reserve(True, 0, 0, 12) == 0


def test_clamp_within_bounds_is_unchanged() -> None:
    assert clamp_intercept_reserve(3, 12) == 3


def test_clamp_caps_at_max_size() -> None:
    assert clamp_intercept_reserve(99, 12) == 12


def test_clamp_floors_at_zero() -> None:
    assert clamp_intercept_reserve(-5, 12) == 0


def test_clamp_with_zero_max_size_returns_zero() -> None:
    # An empty squadron (max_size 0) can hold no reserve, even from a YAML default.
    assert clamp_intercept_reserve(5, 0) == 0


def test_resource_count_is_reserve_when_owned_is_sufficient() -> None:
    assert qra_resource_count(4, 10) == 4


def test_resource_count_capped_at_owned_after_attrition() -> None:
    # Squadron attrited below its reserve must not field more jets than it owns.
    assert qra_resource_count(5, 3) == 3


def test_resource_count_is_zero_when_nothing_owned() -> None:
    assert qra_resource_count(4, 0) == 0


def test_resource_count_capped_by_available_pilots() -> None:
    assert qra_resource_count(4, 10, available_pilots=2) == 2


def test_resource_count_airframes_win_when_fewer_than_pilots() -> None:
    assert qra_resource_count(4, 1, available_pilots=10) == 1


def test_resource_count_no_pilot_cap_when_pilots_none() -> None:
    assert qra_resource_count(4, 10, available_pilots=None) == 4


def test_resource_count_zero_with_no_available_pilots() -> None:
    assert qra_resource_count(4, 10, available_pilots=0) == 0


def test_repropagate_non_barcap_squadron_is_unchanged() -> None:
    # A non-BARCAP squadron never carries QRA, even if its value equals the default.
    assert repropagated_intercept_reserve(False, 0, 0, 4, 12) == 0


def test_repropagate_tracking_squadron_moves_to_new_default() -> None:
    # Opt-in on an existing campaign: 0 -> 4 bumps a squadron still at the old default.
    assert repropagated_intercept_reserve(True, 0, 0, 4, 12) == 4


def test_repropagate_user_set_value_is_left_alone() -> None:
    # Reserve 3 != clamped old default 0, so the user's choice is preserved.
    assert repropagated_intercept_reserve(True, 3, 0, 4, 12) == 3


def test_repropagate_matches_clamped_old_default() -> None:
    # max_size 4 clamped the old default 6 down to 4 at seed time; that squadron
    # still tracks the default and follows it down to the new (clamped) value.
    assert repropagated_intercept_reserve(True, 4, 6, 2, 4) == 2


def test_repropagate_new_value_is_clamped_to_max_size() -> None:
    assert repropagated_intercept_reserve(True, 0, 0, 10, 4) == 4


def test_repropagate_no_op_when_old_equals_new() -> None:
    assert repropagated_intercept_reserve(True, 2, 2, 2, 12) == 2


def test_untasked_grows_when_reserve_freed() -> None:
    # Reserve 4 -> 0 mid-turn releases the 4 benched jets into the plannable pool.
    # owned 10: 6 untasked + 4 reserve.
    assert untasked_after_reserve_change(4, 0, 6, 10) == 10


def test_untasked_shrinks_when_reserve_raised() -> None:
    # Reserve 0 -> 4 benches 4 jets that were plannable. owned 10.
    assert untasked_after_reserve_change(0, 4, 10, 10) == 6


def test_untasked_unchanged_when_reserve_unchanged() -> None:
    assert untasked_after_reserve_change(3, 3, 5, 8) == 5


def test_untasked_floors_at_zero_when_reserve_exceeds_pool() -> None:
    # Only still-untasked jets can be benched; already-tasked flights are never
    # retroactively un-planned, so the pool floors at 0. owned 10, 8 tasked.
    assert untasked_after_reserve_change(0, 5, 2, 10) == 0


def test_untasked_capped_at_owned_after_attrition() -> None:
    # Attrition left owned 2 below reserve 4; return_all floored untasked to 0.
    # Lowering reserve to 1 must free only the 1 jet that exists beyond the new
    # reserve (max 2-1), NOT the delta of 3.
    assert untasked_after_reserve_change(4, 1, 0, 2) == 1


def test_max_reserve_capped_by_unplanned_airframes() -> None:
    # 12/14 tasked -> untasked 2, reserve 0: QRA can rise to 2 (the unplanned jets).
    assert (
        max_intercept_reserve(untasked_aircraft=2, intercept_reserve=0, max_size=14)
        == 2
    )


def test_max_reserve_is_zero_when_everything_tasked() -> None:
    # 14/14 tasked -> untasked 0, reserve 0: no jets free for QRA.
    assert (
        max_intercept_reserve(untasked_aircraft=0, intercept_reserve=0, max_size=14)
        == 0
    )


def test_max_reserve_includes_already_reserved_jets() -> None:
    # untasked+reserve = owned - tasked is the invariant ceiling; already-reserved
    # jets stay reservable.
    assert (
        max_intercept_reserve(untasked_aircraft=1, intercept_reserve=3, max_size=14)
        == 4
    )


def test_max_reserve_bounded_by_max_size() -> None:
    assert (
        max_intercept_reserve(untasked_aircraft=20, intercept_reserve=0, max_size=12)
        == 12
    )
