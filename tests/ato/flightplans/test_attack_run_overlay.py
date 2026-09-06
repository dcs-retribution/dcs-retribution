from dcs import Point
from dcs.terrain import Caucasus

from game.ato.flightplans.tacticaloverlay import attack_run_overlay


def _p(x: float, y: float) -> Point:
    return Point(x, y, Caucasus())


def test_attack_run_reveals_target_and_detour() -> None:
    ingress = _p(0, 0)
    target = _p(10000, 5000)
    split = _p(20000, 0)
    overlay = attack_run_overlay(ingress, target, split)
    assert overlay.reach == []
    assert overlay.targets[0].position == target
    assert overlay.actual_path == [ingress, target, split]
