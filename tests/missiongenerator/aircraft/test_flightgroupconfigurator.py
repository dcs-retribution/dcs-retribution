from typing import Any, Dict, Optional

import pytest

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


class _StubSettings:
    """Stands in for pydcs' WeaponSettings, which reports the weapon's defaults."""

    def __init__(self, values: Dict[str, Any]) -> None:
        self._values = values

    def to_dict(self) -> Dict[str, Any]:
        return dict(self._values)


class _StubWeapon:
    """A weapon whose settings schema declares a tail fuze, like any real bomb."""

    def __init__(
        self, accepts: bool = True, defaults: Optional[Dict[str, Any]] = None
    ) -> None:
        self._accepts = accepts
        self._defaults = {"NFP_fuze_type_tail": "FMU139CB_LD", "laser_code": 1688}
        if defaults is not None:
            self._defaults = defaults

    def accepts_laser_code(self) -> bool:
        return self._accepts

    def create_settings(self) -> Optional[_StubSettings]:
        return _StubSettings(self._defaults) if self._defaults else None


@pytest.fixture(name="laser_code")
def laser_code_fixture() -> LaserCode:
    return LaserCode(1511, _StubRegistry())


def test_merge_keeps_the_weapon_defaults_when_the_loadout_has_no_settings(
    laser_code: LaserCode,
) -> None:
    """The regression this guards: a table holding only the laser code told DCS the
    bomb had no fuze fitted, so it fell as a dud."""
    result = FlightGroupConfigurator._merge_laser_code(
        None, _StubWeapon(), laser_code  # type: ignore[arg-type]
    )
    assert result == {"NFP_fuze_type_tail": "FMU139CB_LD", "laser_code": 1511}


def test_merge_preserves_other_settings_when_accepted(laser_code: LaserCode) -> None:
    base: Dict[str, Any] = {"fuze_setting": "instant"}
    result = FlightGroupConfigurator._merge_laser_code(
        base, _StubWeapon(defaults={}), laser_code  # type: ignore[arg-type]
    )
    assert result == {"fuze_setting": "instant", "laser_code": 1511}


def test_merge_lets_the_loadout_override_a_default(laser_code: LaserCode) -> None:
    base: Dict[str, Any] = {"NFP_fuze_type_tail": "FMU152AB_LD"}
    result = FlightGroupConfigurator._merge_laser_code(
        base, _StubWeapon(), laser_code  # type: ignore[arg-type]
    )
    assert result is not None
    assert result["NFP_fuze_type_tail"] == "FMU152AB_LD"


def test_merge_overrides_existing_laser_code_when_accepted(
    laser_code: LaserCode,
) -> None:
    base: Dict[str, Any] = {"laser_code": 1688}
    result = FlightGroupConfigurator._merge_laser_code(
        base, _StubWeapon(defaults={}), laser_code  # type: ignore[arg-type]
    )
    assert result == {"laser_code": 1511}


def test_merge_returns_base_unchanged_when_not_accepted(
    laser_code: LaserCode,
) -> None:
    base: Dict[str, Any] = {"fuze_setting": "instant"}
    result = FlightGroupConfigurator._merge_laser_code(
        base, _StubWeapon(accepts=False), laser_code  # type: ignore[arg-type]
    )
    assert result is base


def test_merge_returns_base_unchanged_when_no_laser_code() -> None:
    base: Dict[str, Any] = {"fuze_setting": "instant"}
    result = FlightGroupConfigurator._merge_laser_code(
        base, _StubWeapon(), None  # type: ignore[arg-type]
    )
    assert result is base


def test_merge_returns_none_when_no_laser_code_and_no_base() -> None:
    result = FlightGroupConfigurator._merge_laser_code(
        None, _StubWeapon(), None  # type: ignore[arg-type]
    )
    assert result is None


def test_merge_does_not_mutate_input_base(laser_code: LaserCode) -> None:
    base: Dict[str, Any] = {"laser_code": 1688, "fuze_setting": "instant"}
    snapshot = dict(base)
    FlightGroupConfigurator._merge_laser_code(
        base, _StubWeapon(), laser_code  # type: ignore[arg-type]
    )
    assert base == snapshot
