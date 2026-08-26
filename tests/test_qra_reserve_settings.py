from game.settings.settings import Settings


def test_ownfor_default_qra_reserve_defaults_to_zero() -> None:
    assert Settings().ownfor_default_qra_reserve == 0


def test_opfor_default_qra_reserve_defaults_to_zero() -> None:
    assert Settings().opfor_default_qra_reserve == 0


def test_qra_gci_max_radius_defaults_to_sixty() -> None:
    assert Settings().qra_gci_max_radius_nm == 60


def test_qra_engagement_range_defaults_to_thirty_eight() -> None:
    assert Settings().qra_engagement_range_nm == 38


def test_qra_comms_enabled_defaults_to_true() -> None:
    assert Settings().qra_comms_enabled is True


def test_qra_settings_are_user_visible() -> None:
    # Settings.fields() walks dataclass fields whose metadata carries the
    # option-description key; all new settings must be discoverable so the
    # settings window renders them.
    names = {
        name
        for page in Settings.pages()
        for section in Settings.sections(page)
        for name, _description in Settings.fields(page, section)
    }
    assert "ownfor_default_qra_reserve" in names
    assert "opfor_default_qra_reserve" in names
    assert "qra_gci_max_radius_nm" in names
    assert "qra_engagement_range_nm" in names
    assert "qra_comms_enabled" in names
