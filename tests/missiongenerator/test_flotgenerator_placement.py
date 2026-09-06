from unittest.mock import MagicMock

from game.dcs.groundunittype import GroundUnitType
from game.ground_forces.ai_ground_planner import CombatGroup, CombatGroupRole
from game.missiongenerator.flotgenerator import frontline_offsets


def _grp(role: CombatGroupRole) -> CombatGroup:
    return CombatGroup(role, MagicMock(spec=GroundUnitType), 1)


def test_wedges_evenly_spaced() -> None:
    w1 = _grp(CombatGroupRole.TANK)
    w2 = _grp(CombatGroupRole.TANK)
    offsets = frontline_offsets([w1, w2], 1000)
    assert offsets[id(w1)] == 250.0
    assert offsets[id(w2)] == 750.0


def test_member_shares_anchor_offset() -> None:
    wedge = _grp(CombatGroupRole.TANK)
    shorad = _grp(CombatGroupRole.SHORAD)
    shorad.anchor = wedge
    offsets = frontline_offsets([wedge, shorad], 1000)
    assert offsets[id(shorad)] == offsets[id(wedge)]


def test_unclustered_gets_an_offset() -> None:
    wedge = _grp(CombatGroupRole.TANK)
    arty = _grp(CombatGroupRole.ARTILLERY)
    offsets = frontline_offsets([wedge, arty], 1000)
    assert id(arty) in offsets
    assert 0 <= offsets[id(arty)] <= 1000
