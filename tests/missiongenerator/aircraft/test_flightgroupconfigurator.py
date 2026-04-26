from typing import Any, Dict, Optional

import pytest

from game.data.weapons import Weapon, WeaponGroup, WeaponType
from game.lasercodes.ilasercoderegistry import ILaserCodeRegistry
from game.lasercodes.lasercode import LaserCode
from game.missiongenerator.aircraft.flightgroupconfigurator import (
    FlightGroupConfigurator,
)


class _StubRegistry(ILaserCodeRegistry):
    def alloc_laser_code(self) -> LaserCode:
        raise NotImplementedError

    def release_code(self, code: LaserCode) -> None:
        pass


def _weapon(weapon_type: WeaponType) -> Weapon:
    group = WeaponGroup(
        name=f"test-{weapon_type.value}",
        type=weapon_type,
        introduction_year=None,
        fallback_name=None,
    )
    return Weapon(clsid=f"test-clsid-{weapon_type.value}", weapon_group=group)


@pytest.fixture(name="laser_code")
def laser_code_fixture() -> LaserCode:
    return LaserCode(1511, _StubRegistry())


def test_merge_inserts_laser_code_when_lgb_and_no_existing_settings(
    laser_code: LaserCode,
) -> None:
    result = FlightGroupConfigurator._merge_laser_code(
        None, _weapon(WeaponType.LGB), laser_code
    )
    assert result == {"laser_code": 1511}


def test_merge_preserves_other_settings_when_lgb(laser_code: LaserCode) -> None:
    base: Dict[str, Any] = {"fuze_setting": "instant"}
    result = FlightGroupConfigurator._merge_laser_code(
        base, _weapon(WeaponType.LGB), laser_code
    )
    assert result == {"fuze_setting": "instant", "laser_code": 1511}


def test_merge_overrides_existing_laser_code_when_lgb(
    laser_code: LaserCode,
) -> None:
    base: Dict[str, Any] = {"laser_code": 1688}
    result = FlightGroupConfigurator._merge_laser_code(
        base, _weapon(WeaponType.LGB), laser_code
    )
    assert result == {"laser_code": 1511}


def test_merge_returns_base_unchanged_for_non_lgb(laser_code: LaserCode) -> None:
    base: Dict[str, Any] = {"fuze_setting": "instant"}
    result = FlightGroupConfigurator._merge_laser_code(
        base, _weapon(WeaponType.ARM), laser_code
    )
    assert result is base


def test_merge_returns_base_unchanged_when_no_laser_code() -> None:
    base: Dict[str, Any] = {"fuze_setting": "instant"}
    result = FlightGroupConfigurator._merge_laser_code(
        base, _weapon(WeaponType.LGB), None
    )
    assert result is base


def test_merge_returns_none_when_no_laser_code_and_no_base() -> None:
    result = FlightGroupConfigurator._merge_laser_code(
        None, _weapon(WeaponType.LGB), None
    )
    assert result is None


def test_merge_does_not_mutate_input_base(laser_code: LaserCode) -> None:
    base: Dict[str, Any] = {"laser_code": 1688, "fuze_setting": "instant"}
    snapshot = dict(base)
    FlightGroupConfigurator._merge_laser_code(
        base, _weapon(WeaponType.LGB), laser_code
    )
    assert base == snapshot
