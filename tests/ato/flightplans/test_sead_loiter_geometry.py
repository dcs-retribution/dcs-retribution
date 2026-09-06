from dcs import Point
from dcs.terrain import Caucasus

from game.ato.flightplans.waypointbuilder import WaypointBuilder


def _p(x: float, y: float) -> Point:
    return Point(x, y, Caucasus())


def test_offset_toward_moves_from_target_toward_ingress() -> None:
    # Ingress is 50 km east of the target; a 20 km offset lands 20 km east of target.
    result = WaypointBuilder._offset_toward(_p(0, 0), _p(50000, 0), 20000)
    assert round(result.x) == 20000
    assert round(result.y) == 0


def test_offset_toward_caps_at_95_percent_of_ingress_distance() -> None:
    # Requested offset (60 km) exceeds the 50 km to ingress; cap at 0.95 * 50 km.
    result = WaypointBuilder._offset_toward(_p(0, 0), _p(50000, 0), 60000)
    assert round(result.x) == 47500


def test_sead_standoff_distance_scales_threat_range_by_factor() -> None:
    # 0.8 x a 50 km threat range -> 40 km standoff.
    assert round(WaypointBuilder._sead_standoff_distance(0.8, 50000)) == 40000


def test_sead_standoff_distance_floors_factor_to_avoid_orbit_on_target() -> None:
    # A misconfigured factor of 0 must not collapse the standoff to 0 m (which would
    # park the loiter orbit directly on the SAM); the factor is floored instead.
    assert round(WaypointBuilder._sead_standoff_distance(0.0, 50000)) == 5000
