# game/missiongenerator/kneeboard_recon/tests/test_markers.py
"""Tests for marker rendering primitives and Aimpoint clustering."""

from __future__ import annotations

import pytest
from PIL import Image, ImageDraw
from dcs.mapping import Point
from dcs.terrain.caucasus.caucasus import Caucasus

from game.missiongenerator.kneeboard_recon.markers import (
    Aimpoint,
    cluster_items,
    draw_aimpoint_badge,
    draw_building_footprint,
    draw_friendly_cp_marker,
    draw_sidc_enemy,
)
from game.utils import Heading


@pytest.fixture
def canvas() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", (200, 200), (255, 255, 255))
    return img, ImageDraw.Draw(img)


def test_draw_sidc_enemy_paints_some_red(
    canvas: tuple[Image.Image, ImageDraw.ImageDraw],
) -> None:
    img, draw = canvas
    draw_sidc_enemy(draw, (100, 100), "A", size=30)
    # The diamond center sits under the white glyph "A" — sample a few
    # points on the diamond's body away from the glyph and require at
    # least one to be red-dominant. (Spot-checking only the centroid is
    # fragile: a font upgrade that widens the glyph by a pixel flips
    # this from red to white without changing the actual rendering
    # quality.)
    samples = [
        img.getpixel((100, 108)),  # below the glyph, still inside diamond
        img.getpixel((90, 100)),  # left edge
        img.getpixel((110, 100)),  # right edge
    ]
    red_samples = [
        px for px in samples if px != (255, 255, 255) and px[0] > px[1] + px[2]
    ]
    assert red_samples, f"SIDC body must paint some red somewhere; sampled {samples!r}"


def test_draw_sidc_enemy_glyph_is_legible_against_diamond(
    canvas: tuple[Image.Image, ImageDraw.ImageDraw],
) -> None:
    """The glyph must be visibly different from the red diamond fill.

    Regression for the red-on-red bug: drawing the glyph with the same red
    fill as the polygon hid the letter entirely. Sample a small region
    around where draw_sidc_enemy paints the text — at least one pixel must
    contrast strongly with the diamond's solid red fill.
    """
    img, draw = canvas
    draw_sidc_enemy(draw, (100, 100), "A", size=30)
    # draw_sidc_enemy paints the glyph centered at (cx, cy - size//3).
    glyph_cy = 100 - 30 // 3
    sampled = [
        img.getpixel((x, y))
        for x in range(90, 111)
        for y in range(glyph_cy - 2, glyph_cy + 14)
    ]
    # The diamond fill is (180, 20, 20). A legible white-ish glyph stroke
    # will lift either the green or blue channel well above 20. Anti-
    # aliasing produces a continuum; require at least one strong pixel.
    legible = [p for p in sampled if p[1] > 100 or p[2] > 100]
    assert legible, (
        "glyph appears invisible against the red diamond fill — no "
        "sampled pixel lifts G/B channels toward white"
    )


def test_draw_aimpoint_badge_includes_label(
    canvas: tuple[Image.Image, ImageDraw.ImageDraw],
) -> None:
    img, draw = canvas
    draw_aimpoint_badge(draw, (100, 100), "T1", dead=False)
    # The badge should leave a region of saturated red.
    assert any(
        img.getpixel((x, y))[0] > 150 and img.getpixel((x, y))[1] < 80
        for x in range(85, 116)
        for y in range(85, 116)
    )


def test_draw_aimpoint_badge_dead_crosses_out(
    canvas: tuple[Image.Image, ImageDraw.ImageDraw],
) -> None:
    img, draw = canvas
    draw_aimpoint_badge(draw, (100, 100), "T4", dead=True)
    # Black diagonal lines through the badge -> at least one black pixel inside it.
    assert any(
        img.getpixel((x, y)) == (0, 0, 0)
        for x in range(85, 116)
        for y in range(85, 116)
    )


def test_draw_building_footprint_outlines_a_rectangle(
    canvas: tuple[Image.Image, ImageDraw.ImageDraw],
) -> None:
    img, draw = canvas
    rect_corners = [(50, 50), (150, 50), (150, 100), (50, 100)]
    draw_building_footprint(draw, rect_corners)
    # Edge pixels should be non-white.
    assert img.getpixel((100, 50)) != (255, 255, 255)


def test_draw_friendly_cp_marker_is_blue(
    canvas: tuple[Image.Image, ImageDraw.ImageDraw],
) -> None:
    img, draw = canvas
    draw_friendly_cp_marker(draw, (100, 100), "UGKO")
    px = img.getpixel((100, 100))
    # Blueish: blue channel dominates.
    assert px[2] >= px[0] and px[2] >= px[1]


def _caucasus() -> Caucasus:
    return Caucasus()


def test_cluster_items_merges_within_threshold() -> None:
    cau = _caucasus()
    points = [
        Point(0.0, 0.0, cau),
        Point(30.0, 0.0, cau),  # within 75 m -> merge with first
        Point(200.0, 0.0, cau),  # standalone
    ]
    buckets = cluster_items(points, position_of=lambda p: p, threshold_m=75.0, cap=12)
    assert len(buckets) == 2
    sizes = sorted(len(members) for members, _ in buckets)
    assert sizes == [1, 2]


def test_cluster_items_respects_cap_with_trailing_remaining_bucket() -> None:
    cau = _caucasus()
    points = [Point(i * 200.0, 0.0, cau) for i in range(20)]
    buckets = cluster_items(points, position_of=lambda p: p, threshold_m=75.0, cap=12)
    # 12 buckets total, last one absorbs the leftover 8 and is flagged trailing.
    assert len(buckets) == 12
    assert buckets[-1][1] is True


def test_aimpoint_label_for_single_unit_is_just_number() -> None:
    cau = _caucasus()
    ap = Aimpoint(
        number=3,
        description="Factory bldg",
        position=Point(0.0, 0.0, cau),
        heading_from_center=Heading.from_degrees(0),
        footprint=None,
        is_dead=False,
        cluster_size=1,
    )
    assert ap.label == "T3"


def test_aimpoint_label_for_cluster_includes_count() -> None:
    cau = _caucasus()
    ap = Aimpoint(
        number=4,
        description="Armor",
        position=Point(0.0, 0.0, cau),
        heading_from_center=Heading.from_degrees(0),
        footprint=None,
        is_dead=False,
        cluster_size=5,
    )
    assert ap.label == "T4 (5×)"


def test_aimpoint_label_for_trailing_cluster_uses_remaining_marker() -> None:
    """Spec: the cap-overflow bucket label reads "T<n> (… remaining)".

    Distinct from non-trailing clusters so pilots can tell the collapse-bucket
    from a real spatial cluster, regardless of how many leftover units it
    aggregates.
    """
    cau = _caucasus()
    ap = Aimpoint(
        number=12,
        description="9 units (... remaining)",
        position=Point(0.0, 0.0, cau),
        heading_from_center=Heading.from_degrees(0),
        footprint=None,
        is_dead=False,
        cluster_size=9,
        is_trailing=True,
    )
    assert ap.label == "T12 (… remaining)"


def test_cluster_items_preserves_input_order_when_over_cap() -> None:
    """When cap+trailing kicks in, the kept buckets must stay in input order.

    Regression for the pre-fix sort-by-size: a large cluster encountered late
    in the input would jump to T1, breaking the corridor-walking numbering
    that pilots rely on. With ``cap=3`` and 5 distinct-position items where
    the LARGEST cluster sits last, the kept buckets must still come out in
    input order, not bucket-size order.
    """
    cau = _caucasus()
    # Build 5 separate buckets (each at distinct positions > 75 m apart),
    # tag them A..E to track input ordering through the clustering. The
    # last bucket E has the most members (3); B, C have 1 each; A and D
    # have 2 each. With cap=3 we'd drop the smallest two (B, C) into the
    # trailing bucket.
    items = [
        ("A1", 0.0),
        ("A2", 30.0),
        ("B", 500.0),
        ("C", 1_000.0),
        ("D1", 1_500.0),
        ("D2", 1_530.0),
        ("E1", 2_000.0),
        ("E2", 2_030.0),
        ("E3", 2_060.0),
    ]
    points = [(tag, Point(x, 0.0, cau)) for tag, x in items]
    buckets = cluster_items(
        points,
        position_of=lambda t: t[1],
        threshold_m=75.0,
        cap=3,
    )
    # Expect: kept = [A-bucket, D-bucket, (trailing)] in input order
    # (A first, D second — even though E has more members than A or D).
    # Wait — with cap=3, cap-1=2 largest buckets kept. The two largest by
    # size are E (3) and tied A/D (2 each); ties break by first index.
    # So kept = [A, E] in input order; trailing absorbs B, C, D.
    assert len(buckets) == 3
    kept_tags_first = [
        members[0][0] for members, trailing in buckets[:2] if not trailing
    ]
    # The first-position tags of the kept buckets must follow input order.
    sorted_by_input = sorted(
        kept_tags_first,
        key=lambda t: [i for i, (k, _) in enumerate(items) if k == t][0],
    )
    assert kept_tags_first == sorted_by_input, (
        f"cap-overflow kept buckets must preserve input order, got "
        f"{kept_tags_first}"
    )
    assert buckets[-1][1] is True, "last bucket must be flagged trailing"
