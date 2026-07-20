from game.ato.flighttype import FlightType
from game.campaignloader.campaignairwingconfig import SquadronConfig


def test_empty_aircraft_key_parses_as_no_preference() -> None:
    # An authored-but-empty `aircraft:` key parses as None, and
    # DefaultSquadronAssigner iterates config.aircraft — without the guard that
    # is a TypeError at New Game. Empty means "any aircraft compatible with the
    # primary task", same as omitting the key entirely.
    config = SquadronConfig.from_data({"primary": "BARCAP", "aircraft": None})
    assert config.aircraft == []
    assert config.primary is FlightType.BARCAP


def test_aircraft_preferences_pass_through() -> None:
    config = SquadronConfig.from_data(
        {"primary": "BARCAP", "aircraft": ["F-14B Tomcat"]}
    )
    assert config.aircraft == ["F-14B Tomcat"]
