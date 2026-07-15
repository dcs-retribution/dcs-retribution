from game.spatialindex import LiveUnitIndex


def test_empty_index_never_occupied() -> None:
    assert LiveUnitIndex([], 5.0).occupied(0.0, 0.0) is False


def test_occupied_within_radius() -> None:
    idx = LiveUnitIndex([(100.0, 200.0)], 5.0)
    assert idx.occupied(100.0, 200.0) is True
    assert idx.occupied(103.0, 203.0) is True  # ~4.24 m


def test_not_occupied_beyond_radius() -> None:
    idx = LiveUnitIndex([(100.0, 200.0)], 5.0)
    assert idx.occupied(110.0, 200.0) is False  # 10 m


def test_boundary_just_inside_and_outside() -> None:
    idx = LiveUnitIndex([(0.0, 0.0)], 5.0)
    assert idx.occupied(4.9, 0.0) is True
    assert idx.occupied(5.1, 0.0) is False


def test_match_found_in_neighbouring_bucket() -> None:
    # Query and point sit in different R-size buckets but within R.
    idx = LiveUnitIndex([(4.9, 0.0)], 5.0)  # bucket (0,0)
    assert idx.occupied(5.1, 0.0) is True  # bucket (1,0), dist 0.2 m


def test_non_finite_positions_skipped_at_construction() -> None:
    # A degenerate unit position (inf/nan) must not crash __init__
    # (math.floor(inf/r) -> OverflowError, math.floor(nan/r) -> ValueError);
    # such a unit isn't anywhere, so it occupies nothing. Finite points still work.
    idx = LiveUnitIndex([(float("inf"), 0.0), (0.0, float("nan")), (100.0, 200.0)], 5.0)
    assert idx.occupied(100.0, 200.0) is True
    assert idx.occupied(float("inf"), 0.0) is False
