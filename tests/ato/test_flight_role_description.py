from types import SimpleNamespace

from game.ato import FlightType
from game.ato.flightroledescription import role_description
from game.utils import nautical_miles


def _flight(flight_type: FlightType) -> SimpleNamespace:
    doctrine = SimpleNamespace(
        cap_engagement_range=nautical_miles(35),
        escort_engagement_range=nautical_miles(20),
        sead_escort_engagement_range=nautical_miles(25),
    )
    settings = SimpleNamespace(
        sead_sweep_engagement_range_distance=30, cas_engagement_range_distance=10
    )
    return SimpleNamespace(
        flight_type=flight_type,
        coalition=SimpleNamespace(
            doctrine=doctrine, game=SimpleNamespace(settings=settings)
        ),
    )


def test_barcap_role_mentions_orbit() -> None:
    text = role_description(_flight(FlightType.BARCAP))  # type: ignore[arg-type]
    assert "orbit" in text.lower()
    assert "35" in text


def test_sead_sweep_role_mentions_hunt() -> None:
    text = role_description(_flight(FlightType.SEAD_SWEEP))  # type: ignore[arg-type]
    assert "air-defence" in text.lower() or "air defence" in text.lower()


def test_plain_sead_role_mentions_anti_radiation() -> None:
    text = role_description(_flight(FlightType.SEAD))  # type: ignore[arg-type]
    assert "anti-radiation" in text.lower()
    assert "30" in text
