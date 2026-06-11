import pytest
import re
from types import SimpleNamespace
from datetime import date
from pathlib import Path

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


@pytest.mark.parametrize(
    ("clsid", "group_name", "introduction_year"),
    [
        ("{F-15E_AAQ-33_XR_ATP-SE}", "AN/AAQ-33 - Advanced Targeting Pod", 2005),
        ("{F-15E_AAQ-28_LITENING}", "AN/AAQ-28 LITENING", 1999),
        ("{SUPERHORNET_PYLON_05_TP_ASQ228}", "AN/ASQ-228 ATFLIR", 2003),
        ("{SUPERHORNET_PYLON_06_CN_TP_AAQ28}", "AN/AAQ-28 LITENING", 1999),
        ("_NiteHawk_FLIR", "AN/AAS-38 Nite Hawk", 1984),
        ("{HB_PAVE_SPIKE_FAST_TRACK}", "AN/AVQ-23 Pave Spike", 1974),
        ("{HB_PAVE_SPIKE_FAST_ON_ADAPTER_IN_AERO7}", "AN/AVQ-23 Pave Spike", 1974),
        ("{JAS39_Litening}", "AN/AAQ-28 LITENING", 1999),
        ("{JAS39_FLIR}", "AN/AAQ-28 LITENING", 1999),
        ("{LITENING_POD}", "AN/AAQ-28 LITENING", 1999),
        ("{DAMOCLES}", "DAMOCLES", 2009),
        ("{F111C_FLIR}", "AN/AVQ-26 Pave Tack", 1982),
        ("DIS_WMD7", "AVIC WMD-7", 2007),
    ],
)
def test_targeting_pod_variants_have_era_data(
    clsid: str, group_name: str, introduction_year: int
) -> None:
    weapon = Weapon.with_clsid(clsid)

    assert weapon is not None
    assert weapon.weapon_group.type is WeaponType.TGP
    assert weapon.weapon_group.name == group_name
    assert weapon.weapon_group.introduction_year == introduction_year


def test_custom_payload_targeting_pods_do_not_fall_back_to_unknown() -> None:
    payload_clsids: set[str] = set()
    for path in Path("resources/customized_payloads").glob("*.lua"):
        text = path.read_text(encoding="utf-8", errors="ignore")
        payload_clsids.update(re.findall(r'\["CLSID"\]\s*=\s*"([^"]+)"', text))

    def is_targeting_pod(weapon: Weapon) -> bool:
        name = weapon.name.upper()
        return (
            "NAV POD" not in name
            and any(
                token in name
                for token in [
                    "TARGETING POD",
                    "ATFLIR",
                    "LITENING",
                    "LANTIRN",
                    "SNIPER",
                    "DAMOCLES",
                    "WMD7",
                    "FLIR/LDT POD",
                    "TARGETING POD FLIR",
                ]
            )
        )

    targeting_pods = [
        Weapon.with_clsid(clsid)
        for clsid in sorted(payload_clsids)
        if Weapon.with_clsid(clsid) is not None
        and is_targeting_pod(Weapon.with_clsid(clsid))
    ]

    assert targeting_pods
    assert all(weapon.weapon_group.type is WeaponType.TGP for weapon in targeting_pods)
    assert all(
        weapon.weapon_group.introduction_year is not None for weapon in targeting_pods
    )
