from typing import Any
from unittest.mock import MagicMock

from game.missiongenerator.aircraft.waypoints.strikeingress import (
    StrikeIngressBuilder,
)


def test_add_strike_tasks_handles_no_targets() -> None:
    """Regression: a Strike against an objective whose units are all destroyed
    leaves the strike waypoint with no targets. add_strike_tasks must not divide
    by zero (len(units) / len(targets)) and must add no bombing task.
    """
    # Bypass __init__ (needs a full mission/flight); only add_strike_tasks() and
    # the attributes it reads are exercised.
    builder: Any = object.__new__(StrikeIngressBuilder)
    builder.waypoint = MagicMock()
    builder.waypoint.targets = []
    builder.group = MagicMock()
    builder.group.units = [MagicMock()]  # would make the ratio 1 / 0 if reached

    waypoint = MagicMock()
    waypoint.tasks = []

    builder.add_strike_tasks(waypoint)  # must not raise ZeroDivisionError

    assert waypoint.tasks == []
