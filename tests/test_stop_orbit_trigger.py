from dcs import Mission
from dcs.task import ControlledTask, OrbitAction

from game.missiongenerator.aircraft.waypoints._helper import create_stop_orbit_trigger


def _orbit() -> ControlledTask:
    return ControlledTask(OrbitAction(pattern=OrbitAction.OrbitPattern.RaceTrack))


def _flag_of(orbit: ControlledTask) -> str:
    return str(orbit.params["stopCondition"]["userFlag"])


def test_each_group_gets_its_own_stop_flag_and_trigger() -> None:
    """Two flights of one package have their own patrol times.

    Keying the flag by package meant one flag for both, and a flag fires once:
    every orbit in the package ended at whichever time was generated first, so
    an AWACS packaged with a shorter BARCAP left station hours early.
    """
    mission = Mission()
    awacs, barcap = _orbit(), _orbit()
    create_stop_orbit_trigger(awacs, 21, mission, 15780)
    create_stop_orbit_trigger(barcap, 20, mission, 8520)

    assert _flag_of(awacs) != _flag_of(barcap)
    assert len(mission.triggerrules.triggers) == 2


def test_the_same_group_is_only_given_one_trigger() -> None:
    mission = Mission()
    create_stop_orbit_trigger(_orbit(), 20, mission, 8520)
    create_stop_orbit_trigger(_orbit(), 20, mission, 8520)
    assert len(mission.triggerrules.triggers) == 1


def test_the_flag_is_stable_across_generations() -> None:
    """The flag was named after a Python id(), which is an object address.

    Two generations of the same turn produced different flag names, and an
    address is reused once its object has been collected.
    """
    first, second = _orbit(), _orbit()
    create_stop_orbit_trigger(first, 20, Mission(), 8520)
    create_stop_orbit_trigger(second, 20, Mission(), 8520)
    assert _flag_of(first) == _flag_of(second)
