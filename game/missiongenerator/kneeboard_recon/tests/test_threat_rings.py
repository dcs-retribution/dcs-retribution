# game/missiongenerator/kneeboard_recon/tests/test_threat_rings.py
"""Tests for threat-ring rendering with zero-range handling."""

from __future__ import annotations

import math

import pytest
from PIL import Image, ImageDraw

from game.missiongenerator.kneeboard_recon.threat_rings import draw_threat_rings


def _fresh_canvas() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", (400, 400), (255, 255, 255))
    return img, ImageDraw.Draw(img)


def test_draw_threat_rings_paints_both_rings() -> None:
    img, draw = _fresh_canvas()
    draw_threat_rings(draw, (200, 200), max_range_px=100, detection_range_px=140)
    # Pixel on the max-range circle (200 + 100, 200) should be red.
    px = img.getpixel((300, 200))
    assert px[0] > 150 and px[1] < 80
    # Pixel slightly past max range, on the detection ring (200 + 140, 200) — dashed,
    # but at the equator we should hit a dash with high probability.
    px2 = img.getpixel((340, 200))
    # Permit either painted or near-painted (dash may land 1 px off).
    assert px2 != (255, 255, 255) or img.getpixel((339, 200)) != (255, 255, 255)


def test_draw_threat_rings_dashed_ring_is_roughly_half_painted() -> None:
    """Detection ring is a 50%-duty dash: well above the old quarter-painted
    bug (~25%) and well below a solid ring (100%)."""
    img, draw = _fresh_canvas()
    cx, cy, r = 200, 200, 140
    draw_threat_rings(draw, (cx, cy), max_range_px=0, detection_range_px=r)
    samples = 360
    painted = 0
    for k in range(samples):
        theta = math.radians(k)
        x = int(round(cx + r * math.cos(theta)))
        y = int(round(cy - r * math.sin(theta)))
        if img.getpixel((x, y)) != (255, 255, 255):
            painted += 1
    fraction = painted / samples
    assert 0.4 <= fraction <= 0.65, f"dashed ring painted fraction {fraction:.2f}"


def test_draw_threat_rings_zero_max_range_omits_solid_ring() -> None:
    img, draw = _fresh_canvas()
    draw_threat_rings(draw, (200, 200), max_range_px=0, detection_range_px=140)
    px = img.getpixel((200 + 50, 200))
    assert px == (255, 255, 255)  # nothing painted inside detection ring


def test_draw_threat_rings_zero_detection_range_omits_dashed_ring() -> None:
    img, draw = _fresh_canvas()
    draw_threat_rings(draw, (200, 200), max_range_px=100, detection_range_px=0)
    # Past max-range circle, image should be white.
    px = img.getpixel((200 + 130, 200))
    assert px == (255, 255, 255)


def test_draw_threat_rings_both_zero_is_a_noop() -> None:
    img, draw = _fresh_canvas()
    draw_threat_rings(draw, (200, 200), max_range_px=0, detection_range_px=0)
    colors = img.getcolors()
    assert colors == [(160_000, (255, 255, 255))]
