from game.ato.flighttype import FlightType


def test_provides_escort_coverage_includes_escort_like_types() -> None:
    assert FlightType.ESCORT.provides_escort_coverage
    assert FlightType.SEAD_ESCORT.provides_escort_coverage
    assert FlightType.TARCAP.provides_escort_coverage


def test_provides_escort_coverage_excludes_others() -> None:
    assert not FlightType.STRIKE.provides_escort_coverage
    assert not FlightType.BARCAP.provides_escort_coverage
    assert not FlightType.CAS.provides_escort_coverage
