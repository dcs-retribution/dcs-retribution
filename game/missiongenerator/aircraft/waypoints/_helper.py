from dcs import Mission
from dcs.action import DoScript
from dcs.condition import TimeAfter
from dcs.task import ControlledTask
from dcs.translation import String
from dcs.triggers import TriggerOnce, Event


def create_stop_orbit_trigger(
    orbit: ControlledTask, group_id: int, mission: Mission, elapsed: int
) -> None:
    """End an orbit at `elapsed`, working around the broken "stop after time".

    Keyed by the group rather than by its package. Every flight has its own
    patrol or push time, but a flag can only fire once, so a package-wide flag
    ended every orbit in the package at whichever time the first flight to be
    generated happened to need: an AWACS packaged with a shorter-lived BARCAP
    was pulled off station two hours early, and a tanker half an hour early.

    The flag is named after the group id rather than a Python ``id()``, which is
    an object address: it changes between two generations of the same turn, and
    is reused once the object it belonged to has been collected.
    """
    flag = f"stop-orbit-{group_id}"
    orbit.stop_if_user_flag(flag, True)
    comment = f"StopOrbit{group_id}"
    if any(t.comment == comment for t in mission.triggerrules.triggers):
        return
    stop_trigger = TriggerOnce(Event.NoEvent, comment)
    stop_trigger.add_condition(TimeAfter(elapsed))
    # setUserFlag rather than SetFlag: the stop condition names the flag as a
    # string, and a string flag cannot collide with the numbered ones the
    # trigger generator hands out for capture zones.
    stop_trigger.add_action(
        DoScript(String(f'trigger.action.setUserFlag("{flag}", true)'))
    )
    mission.triggerrules.triggers.append(stop_trigger)
