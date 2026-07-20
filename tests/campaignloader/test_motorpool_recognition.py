from __future__ import annotations

from types import SimpleNamespace
from typing import Iterator

from dcs.statics import Fortification

from game.campaignloader.mizcampaignloader import MizCampaignLoader


def _static(type_id: str) -> SimpleNamespace:
    return SimpleNamespace(units=[SimpleNamespace(type=type_id)])


def test_motorpool_sentinel_is_garage_a() -> None:
    assert MizCampaignLoader.MOTORPOOL_UNIT_TYPE == Fortification.Garage_A.id


def test_motorpools_property_filters_by_sentinel() -> None:
    garage = _static(Fortification.Garage_A.id)
    other = _static(Fortification.Workshop_A.id)
    fake_self = SimpleNamespace(
        MOTORPOOL_UNIT_TYPE=MizCampaignLoader.MOTORPOOL_UNIT_TYPE,
        blue=SimpleNamespace(static_group=[garage, other]),
        red=SimpleNamespace(static_group=[other]),
    )
    # Call the property's underlying function with our fake self.
    result: Iterator[object] = MizCampaignLoader.motorpools.fget(fake_self)  # type: ignore[attr-defined]
    assert list(result) == [garage]
