import pytest
from types import SimpleNamespace
from datetime import date

from dcs.planes import F_16C_50

from game.ato.loadouts import Loadout
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


def test_aaq_33_has_era_data_and_degrades_on_pre_intro_f16() -> None:
    weapon = Weapon.with_clsid("{AN_AAQ_33}")

    assert weapon is not None
    assert weapon.weapon_group.name == "AN/AAQ-33 - Advanced Targeting Pod"
    assert weapon.weapon_group.introduction_year == 2005

    faction = SimpleNamespace(weapons_introduction_year_overrides={})
    assert weapon.available_on(date(2004, 1, 1), faction) is False
    assert weapon.available_on(date(2005, 1, 1), faction) is True

    loadout = Loadout("Test", {11: weapon}, date=None)
    degraded = loadout.degrade_for_date(
        SimpleNamespace(dcs_unit_type=F_16C_50), date(2004, 1, 1), faction
    )

    degraded_weapon = degraded.pylons.get(11)
    assert degraded_weapon is not None
    assert degraded_weapon.weapon_group.name == "AN/AAQ-28 LITENING"
