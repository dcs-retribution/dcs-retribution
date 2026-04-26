import pytest

from game.data.weapons import Weapon, WeaponGroup, WeaponType


def _bare_weapon(clsid: str) -> Weapon:
    group = WeaponGroup(
        name=f"test-{clsid}",
        type=WeaponType.UNKNOWN,
        introduction_year=None,
        fallback_name=None,
    )
    return Weapon(clsid=clsid, weapon_group=group)


@pytest.mark.parametrize(
    "clsid",
    [
        "{LAU-131 - 7 AGR-20A}",
        "{LAU-131 - 7 AGR-20 M282}",
        "{BRU-32 GBU-12}",
        "DIS_GBU_12",
    ],
)
def test_accepts_laser_code_true_for_laser_guided_weapons(clsid: str) -> None:
    assert _bare_weapon(clsid).accepts_laser_code() is True


@pytest.mark.parametrize(
    "clsid",
    [
        "<CLEAN>",
        "{AUF2_MK82}",
        "definitely-not-a-real-clsid",
    ],
)
def test_accepts_laser_code_false_for_non_laser_or_unknown(clsid: str) -> None:
    assert _bare_weapon(clsid).accepts_laser_code() is False
