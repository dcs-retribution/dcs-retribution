from __future__ import annotations

from dcs.mapping import Point

from game.lasercodes.lasercoderegistry import LaserCodeRegistry
from game.missiongenerator.flotgenerator import (
    frontline_segment_from_bounds,
    jtac_count_and_codes,
    jtacs_per_frontline,
)
from game.missiongenerator.missiondata import JtacInfo
from game.radio.radios import MHz
from game.theater.frontline import FrontLine
from game.theater.player import Player


def test_jtacinfo_carries_optional_frontline_segment() -> None:
    point_a = Point(10.0, 20.0, None)  # type: ignore[arg-type]
    point_b = Point(30.0, 40.0, None)  # type: ignore[arg-type]
    info = JtacInfo(
        group_name="JTAC GROUP",
        unit_name="JTAC UNIT",
        callsign="Axeman 1",
        region="Frontline Alpha/Bravo",
        code="1688",
        blue=Player.BLUE,
        freq=MHz(30),
        frontline_segment=(point_a, point_b),
    )
    assert info.frontline_segment == (point_a, point_b)


def test_frontline_segment_from_bounds_returns_left_right() -> None:
    class FakeBounds:
        left_position = Point(1.0, 2.0, None)  # type: ignore[arg-type]
        right_position = Point(3.0, 4.0, None)  # type: ignore[arg-type]

    seg = frontline_segment_from_bounds(FakeBounds())  # type: ignore[arg-type]
    assert seg == (FakeBounds.left_position, FakeBounds.right_position)


def test_jtacinfo_frontline_segment_defaults_none() -> None:
    info = JtacInfo(
        group_name="JTAC GROUP",
        unit_name="JTAC UNIT",
        callsign="Axeman 1",
        region="Frontline Alpha/Bravo",
        code="1688",
        blue=Player.BLUE,
        freq=MHz(30),
    )
    assert info.frontline_segment is None


def test_jtacinfo_carries_vhf_frequency() -> None:
    jtac = JtacInfo(
        group_name="JTAC Alpha",
        unit_name="JTAC Alpha Unit",
        callsign="Overlord 1",
        region="Frontline A/B",
        code="1688",
        blue=Player.BLUE,
        freq=MHz(251),
        freq_vhf=MHz(124),
    )
    assert jtac.freq_vhf == MHz(124)


# ---------------------------------------------------------------------------
# jtacs_per_frontline clamp tests
# ---------------------------------------------------------------------------


def _bare_frontline(reg: LaserCodeRegistry) -> FrontLine:
    """Bypass FrontLine.__init__ (needs ControlPoints); unit-test only."""
    front = FrontLine.__new__(FrontLine)
    front.laser_code = reg.alloc_laser_code()
    front.extra_laser_codes = []
    return front


def test_jtacs_per_frontline_clamps_zero_to_one() -> None:
    assert jtacs_per_frontline(0) == 1


def test_jtacs_per_frontline_clamps_five_to_four() -> None:
    assert jtacs_per_frontline(5) == 4


def test_jtacs_per_frontline_accepts_float_option() -> None:
    # The option may arrive widened to a float; must not ValueError.
    assert jtacs_per_frontline(2.0) == 2
    assert jtacs_per_frontline("3") == 3


def test_jtacs_per_frontline_passes_two_through() -> None:
    assert jtacs_per_frontline(2) == 2


def test_jtacs_per_frontline_none_defaults_to_one() -> None:
    assert jtacs_per_frontline(None) == 1


# ---------------------------------------------------------------------------
# jtac_count_and_codes tests
# ---------------------------------------------------------------------------


def test_jtac_count_and_codes_non_fc3_n2_returns_distinct_codes() -> None:
    reg = LaserCodeRegistry()
    front = _bare_frontline(reg)
    n, codes = jtac_count_and_codes(
        fc3=False, n_requested=2, front_line=front, registry=reg
    )
    assert n == 2
    assert len(codes) == 2
    assert len({c.code for c in codes}) == 2  # distinct


def test_jtac_count_and_codes_fc3_forces_single_jtac_with_1113() -> None:
    reg = LaserCodeRegistry()
    front = _bare_frontline(reg)
    n, codes = jtac_count_and_codes(
        fc3=True, n_requested=2, front_line=front, registry=reg
    )
    assert n == 1
    assert len(codes) == 1
    assert codes[0].code == 1113
