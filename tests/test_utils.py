from game.utils import max_optional_distance, nautical_miles


def test_max_optional_distance_picks_largest() -> None:
    distances = [nautical_miles(10), nautical_miles(160), nautical_miles(40)]
    result = max_optional_distance(distances)
    assert result is not None
    assert result.nautical_miles == 160


def test_max_optional_distance_ignores_none() -> None:
    distances = [None, nautical_miles(10), None, nautical_miles(40)]
    result = max_optional_distance(distances)
    assert result is not None
    assert result.nautical_miles == 40


def test_max_optional_distance_all_none_returns_none() -> None:
    assert max_optional_distance([None, None]) is None


def test_max_optional_distance_empty_returns_none() -> None:
    assert max_optional_distance([]) is None
