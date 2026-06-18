from game.ato.flight import roll_plane_altitude_offset
from game.ato.flightplans.waypointbuilder import apply_patrol_altitude_floor
from game.settings.settings import Settings
from game.utils import feet


def test_altitude_offset_defaults_preserve_legacy_band() -> None:
    # Defaults must reproduce the old symmetric +/- 2k behavior so existing saves
    # are unchanged when they auto-default the new minimum field.
    settings = Settings()
    assert settings.min_plane_altitude_offset == -2
    assert settings.max_plane_altitude_offset == 2


def test_min_patrol_altitude_defaults_off() -> None:
    # 0 means no floor: every existing and new campaign keeps each aircraft's
    # preferred patrol altitude until someone opts in.
    assert Settings().min_patrol_altitude == 0


def test_new_altitude_settings_are_user_visible() -> None:
    names = {
        name
        for page in Settings.pages()
        for section in Settings.sections(page)
        for name, _description in Settings.fields(page, section)
    }
    assert "min_plane_altitude_offset" in names
    assert "max_plane_altitude_offset" in names
    assert "min_patrol_altitude" in names


def test_equal_offset_bounds_disable_randomization() -> None:
    assert roll_plane_altitude_offset(0, 0) == 0
    assert roll_plane_altitude_offset(3, 3) == 3000


def test_offset_roll_stays_within_band() -> None:
    for _ in range(200):
        assert -2000 <= roll_plane_altitude_offset(-2, 2) <= 2000


def test_offset_roll_tolerates_swapped_bounds() -> None:
    for _ in range(200):
        assert 1000 <= roll_plane_altitude_offset(4, 1) <= 4000


def test_patrol_floor_disabled_returns_base_altitude() -> None:
    base = feet(24000)
    assert apply_patrol_altitude_floor(base, 0, feet(35000)) == base


def test_patrol_floor_raises_low_altitude() -> None:
    assert apply_patrol_altitude_floor(feet(24000), 28, feet(35000)) == feet(28000)


def test_patrol_floor_does_not_lower_higher_altitude() -> None:
    base = feet(31000)
    assert apply_patrol_altitude_floor(base, 28, feet(35000)) == base


def test_patrol_floor_capped_by_combat_ceiling() -> None:
    assert apply_patrol_altitude_floor(feet(24000), 40, feet(35000)) == feet(35000)
