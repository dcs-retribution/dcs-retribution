# game/missiongenerator/kneeboard_recon/tests/test_airfield_diagram.py
"""Tests for airfield-departure diagram primitives."""

from __future__ import annotations

import math

import pytest
from PIL import Image, ImageDraw

from game.missiongenerator.kneeboard_recon.airfield_diagram import (
    draw_spawn_marker,
    draw_wind_arrow_badge,
    draw_active_threshold_marker,
)


@pytest.fixture
def canvas() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", (400, 400), (255, 255, 255))
    return img, ImageDraw.Draw(img)


def test_draw_spawn_marker_paints_blue(
    canvas: tuple[Image.Image, ImageDraw.ImageDraw],
) -> None:
    img, draw = canvas
    draw_spawn_marker(draw, (200, 200), "ENFIELD 1-1")
    px = img.getpixel((200, 200))
    assert px[2] > px[0]  # blue channel dominates


def test_draw_active_threshold_marker_paints_green(
    canvas: tuple[Image.Image, ImageDraw.ImageDraw],
) -> None:
    img, draw = canvas
    draw_active_threshold_marker(draw, (200, 200))
    px = img.getpixel((200 + 24, 200))  # on the ring
    assert px[1] > 100 and px[0] < 100


def test_draw_active_threshold_marker_label_is_black_on_white(
    canvas: tuple[Image.Image, ImageDraw.ImageDraw],
) -> None:
    img, draw = canvas
    draw_active_threshold_marker(draw, (200, 200))
    # Label box sits to the right of the ring (radius 26). Sample just
    # inside the top-left corner of the box: the border should be black,
    # one pixel further in should be white.
    border_px = img.getpixel((200 + 26 + 6, 200 - 11))
    fill_px = img.getpixel((200 + 26 + 7, 200 - 10))
    assert border_px == (0, 0, 0)
    assert fill_px == (255, 255, 255)


def test_active_label_is_vertically_centred_on_marker(
    canvas: tuple[Image.Image, ImageDraw.ImageDraw],
) -> None:
    img, draw = canvas
    cx = cy = 200
    draw_active_threshold_marker(draw, (cx, cy))
    # Scan the box interior (right of the ring, inside the border) for the
    # label glyphs; their vertical midpoint must sit on the marker centre.
    ys = [
        y
        for x in range(cx + 35, cx + 69)
        for y in range(cy - 9, cy + 10)
        if sum(img.getpixel((x, y))) < 150
    ]
    assert ys, "no label glyphs found in box interior"
    midpoint = (min(ys) + max(ys)) / 2
    assert abs(midpoint - cy) <= 1.5, f"label midpoint {midpoint} not centred on {cy}"


def test_draw_wind_arrow_badge_includes_from_text(
    canvas: tuple[Image.Image, ImageDraw.ImageDraw],
) -> None:
    img, draw = canvas
    draw_wind_arrow_badge(draw, (200, 60), from_dir_deg=130, speed_kts=12)
    # The badge area should not be entirely white.
    region = [img.getpixel((x, y)) for x in range(150, 251) for y in range(10, 111)]
    assert any(c != (255, 255, 255) for c in region)
