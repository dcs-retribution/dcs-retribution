from game.ground_forces.frontline_clustering import (
    allocate_largest_remainder,
    even_slot_centers,
)


def test_allocate_proportional_even_split() -> None:
    # 10 Abrams + 10 Linebackers, deployable target 15 -> ~even, not 10/5.
    result = allocate_largest_remainder({"abrams": 7.5, "linebacker": 7.5}, 15)
    assert sum(result.values()) == 15
    assert abs(result["abrams"] - result["linebacker"]) <= 1


def test_allocate_caps_total() -> None:
    result = allocate_largest_remainder({"a": 100.0, "b": 100.0}, 15)
    assert sum(result.values()) == 15


def test_allocate_under_target_deploys_all() -> None:
    # sum(weights) rounds to 8 < cap 15 -> deploy 8.
    result = allocate_largest_remainder({"a": 4.0, "b": 4.0}, 15)
    assert sum(result.values()) == 8


def test_allocate_largest_remainder_distribution() -> None:
    # 3 units across weights 1:1:1 -> 1 each.
    result = allocate_largest_remainder({"a": 1.0, "b": 1.0, "c": 1.0}, 3)
    assert result == {"a": 1, "b": 1, "c": 1}


def test_allocate_empty() -> None:
    assert allocate_largest_remainder({}, 10) == {}


def test_even_slot_centers_basic() -> None:
    assert even_slot_centers(2, 1000) == [250.0, 750.0]


def test_even_slot_centers_single() -> None:
    assert even_slot_centers(1, 1000) == [500.0]


def test_even_slot_centers_zero() -> None:
    assert even_slot_centers(0, 1000) == []
