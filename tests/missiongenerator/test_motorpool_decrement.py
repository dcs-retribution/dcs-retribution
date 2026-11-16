from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock

from dcs.vehicles import Armor

from game.dcs.groundunittype import GroundUnitType
from game.sim.missionresultsprocessor import MissionResultsProcessor
from game.unitmap import UnitMap


def _gut() -> GroundUnitType:
    return next(GroundUnitType.for_dcs_type(Armor.M_1_Abrams))


def test_killed_motorpool_unit_decrements_base_armor_by_one() -> None:
    gut = _gut()
    # A CP whose base holds the reserve pool.
    base = SimpleNamespace(
        armor={gut: 5},
        total_units_of_type=lambda t: 5 if t is gut else 0,
    )
    cp = MagicMock()
    cp.base = base

    # Register one motorpool vehicle exactly as MotorpoolGenerator does.
    unit_map = UnitMap()
    group = SimpleNamespace(units=[SimpleNamespace(name="0001 | Reserve Abrams")])
    unit_map.add_motorpool_units(group, cp, gut)  # type: ignore[arg-type]

    # Prove exclusion: motorpool_unit finds it, front_line_unit does not.
    assert unit_map.motorpool_unit("0001 | Reserve Abrams") is not None
    assert unit_map.front_line_unit("0001 | Reserve Abrams") is None

    # Simulate a debrief that killed that unit.
    debriefing = MagicMock()
    motorpool_loss = unit_map.motorpool_unit("0001 | Reserve Abrams")
    assert motorpool_loss is not None
    debriefing.motorpool_losses = [motorpool_loss]

    MissionResultsProcessor.commit_motorpool_losses(debriefing)

    assert base.armor[gut] == 4
