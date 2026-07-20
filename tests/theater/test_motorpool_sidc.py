from __future__ import annotations

from game.sidc import Status
from game.theater.theatergroundobject import MotorpoolGroundObject


def test_motorpool_sidc_status_is_always_present() -> None:
    # Empty-on-map is a motorpool's normal resting state (vehicles are populated
    # ephemerally at mission-gen), so the override must never fall through to the
    # base PRESENT_DESTROYED / PRESENT_DAMAGED status. __new__ skips __init__: the
    # override reads no instance state, which is exactly the property we assert.
    mp = MotorpoolGroundObject.__new__(MotorpoolGroundObject)
    assert mp.sidc_status is Status.PRESENT
