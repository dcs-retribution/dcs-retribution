from types import SimpleNamespace

from game.ato.package import Package
from game.ato.packagewaypoints import PackageWaypoints
from game.data.doctrine import ALL_DOCTRINES
from game.utils import nautical_miles


def _fake_package(waypoints: object, standoff: object) -> Package:
    # waypoints_need_regeneration/max_standoff_range only touch these attributes, so a
    # lightweight stand-in avoids building a whole campaign just to exercise the logic.
    return SimpleNamespace(  # type: ignore[return-value]
        waypoints=waypoints,
        max_standoff_range=lambda: standoff,
    )


def test_waypoints_regenerate_when_never_built() -> None:
    package = _fake_package(waypoints=None, standoff=nautical_miles(160))
    assert Package.waypoints_need_regeneration(package) is True


def test_waypoints_kept_when_standoff_range_unchanged() -> None:
    waypoints = SimpleNamespace(standoff_range=nautical_miles(160))
    package = _fake_package(waypoints=waypoints, standoff=nautical_miles(160))
    assert Package.waypoints_need_regeneration(package) is False


def test_waypoints_regenerate_when_standoff_range_changes() -> None:
    # Payload swapped from a Kh-22 (160nm) loadout to short-range bombs.
    waypoints = SimpleNamespace(standoff_range=nautical_miles(160))
    package = _fake_package(waypoints=waypoints, standoff=None)
    assert Package.waypoints_need_regeneration(package) is True

    # And the reverse: unranged loadout swapped up to a stand-off weapon.
    waypoints = SimpleNamespace(standoff_range=None)
    package = _fake_package(waypoints=waypoints, standoff=nautical_miles(160))
    assert Package.waypoints_need_regeneration(package) is True


def test_doctrine_unchanged_when_no_standoff_weapon() -> None:
    doctrine = ALL_DOCTRINES[0]
    result = PackageWaypoints.doctrine_for_standoff_range(
        doctrine, None, nautical_miles(300)
    )
    assert result is doctrine


def test_doctrine_unchanged_when_standoff_range_within_doctrine_ingress() -> None:
    doctrine = ALL_DOCTRINES[0]
    short_range = doctrine.max_ingress_distance / 2
    result = PackageWaypoints.doctrine_for_standoff_range(
        doctrine, short_range, nautical_miles(300)
    )
    assert result is doctrine


def test_doctrine_ingress_raised_to_standoff_range() -> None:
    # Regression for issue #34: a Kh-22-class range should widen the ingress distance.
    doctrine = ALL_DOCTRINES[0]
    standoff = doctrine.max_ingress_distance + nautical_miles(50)
    result = PackageWaypoints.doctrine_for_standoff_range(
        doctrine, standoff, nautical_miles(300)
    )
    assert result.max_ingress_distance == standoff


def test_doctrine_ingress_clamped_to_departure_target_distance() -> None:
    # Regression for Druss99's PR #888 review: a stand-off range longer than the
    # route itself must not push the ingress point past the departure (off the
    # route / off the map); it should clamp to the distance actually available.
    doctrine = ALL_DOCTRINES[0]
    distance_to_target = doctrine.max_ingress_distance + nautical_miles(20)
    standoff = distance_to_target + nautical_miles(500)
    result = PackageWaypoints.doctrine_for_standoff_range(
        doctrine, standoff, distance_to_target
    )
    assert result.max_ingress_distance == distance_to_target
    assert result.max_ingress_distance < standoff
