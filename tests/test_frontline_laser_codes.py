from game.lasercodes.lasercoderegistry import LaserCodeRegistry
from game.theater.frontline import FrontLine


def _bare_frontline(reg: LaserCodeRegistry) -> FrontLine:
    # Bypass FrontLine.__init__ (needs ControlPoints + convoy route); this unit
    # test exercises only the laser_codes() method, so construct a bare instance.
    front = FrontLine.__new__(FrontLine)
    front.laser_code = reg.alloc_laser_code()  # 1688
    front.extra_laser_codes = []
    return front


def test_laser_codes_allocates_then_reuses() -> None:
    reg = LaserCodeRegistry()
    front = _bare_frontline(reg)
    assert [c.code for c in front.laser_codes(3, reg)] == [1688, 1687, 1686]
    # idempotent: a second call reuses the same extras, allocates nothing new
    assert [c.code for c in front.laser_codes(3, reg)] == [1688, 1687, 1686]
    assert len(reg.available_codes) == 192 - 3


def test_laser_codes_shrinks_without_releasing() -> None:
    reg = LaserCodeRegistry()
    front = _bare_frontline(reg)
    front.laser_codes(3, reg)
    assert [c.code for c in front.laser_codes(1, reg)] == [1688]
    # extras stay allocated (released only on front-line destroy)
    assert len(reg.available_codes) == 192 - 3


def test_setstate_defaults_extra_laser_codes_for_old_saves() -> None:
    # A FrontLine pickled before multi-code support has no extra_laser_codes in
    # its state. __setstate__ must default it so laser_codes()/teardown don't
    # AttributeError on load.
    reg = LaserCodeRegistry()
    front = FrontLine.__new__(FrontLine)
    front.__setstate__({"laser_code": reg.alloc_laser_code()})  # no extra_laser_codes
    assert front.extra_laser_codes == []
    assert [c.code for c in front.laser_codes(2, reg)] == [1688, 1687]
