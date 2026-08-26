from game.missiongenerator.interceptattrition import reconcile_intercept_losses


def test_no_losses_when_all_survive() -> None:
    losses = reconcile_intercept_losses({"a": 4}, {"a": 4})
    assert losses == {"a": 0}


def test_losses_are_reserve_minus_survivors() -> None:
    losses = reconcile_intercept_losses({"a": 4}, {"a": 1})
    assert losses == {"a": 3}


def test_missing_squadron_takes_no_loss() -> None:
    # Absent from the survivor map means the squadron never flew QRA this mission
    # (carrier/no-EWR/plugin-disabled/no-parking) -> no loss, not a total loss.
    losses = reconcile_intercept_losses({"a": 4}, {})
    assert losses == {}


def test_zero_survivors_is_a_real_total_loss() -> None:
    # Present with zero survivors means the dispatcher reported everyone dead.
    losses = reconcile_intercept_losses({"a": 4}, {"a": 0})
    assert losses == {"a": 4}


def test_survivors_never_produce_negative_losses() -> None:
    # Defensive: a stale/over-count must not credit phantom airframes.
    losses = reconcile_intercept_losses({"a": 2}, {"a": 5})
    assert losses == {"a": 0}


def test_unknown_squadron_in_state_is_ignored() -> None:
    losses = reconcile_intercept_losses({"a": 2}, {"a": 2, "ghost": 9})
    assert losses == {"a": 0}
