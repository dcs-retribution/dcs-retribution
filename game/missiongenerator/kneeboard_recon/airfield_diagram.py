# game/missiongenerator/kneeboard_recon/airfield_diagram.py
"""Drawing primitives specific to the airfield departure page.

Three primitives:

* :func:`draw_spawn_marker` — single-pilot parking-slot indicator.
* :func:`draw_active_threshold_marker` — green ring on the in-use runway threshold.
* :func:`draw_wind_arrow_badge` — boxed wind compass for the page corner.

These do not know about extents or projectors — the page class projects
positions first and passes pixel coords here.
"""

from __future__ import annotations

import math

from PIL import ImageDraw

from ._fonts import load_font

_BLUE = (30, 70, 170)
_GREEN = (20, 140, 50)
_FG = (15, 15, 15)
_BADGE_BG = (245, 245, 240)


SPAWN_LABEL_COLOR = _BLUE


def draw_spawn_marker(
    draw: ImageDraw.ImageDraw,
    pos: tuple[int, int],
    callsign_label: str | None = None,
    *,
    size: int = 9,
) -> None:
    """Draw the parking-slot box. Pass ``callsign_label=None`` to skip the
    inline label (use the label_layout pass for collision-avoiding placement)."""
    cx, cy = pos
    draw.rectangle(
        (cx - size, cy - size, cx + size, cy + size), fill=_BLUE, outline=_FG, width=1
    )
    if callsign_label is None:
        return
    font = load_font(11, bold=True)
    draw.text((cx + size + 4, cy - 8), callsign_label, fill=_BLUE, font=font)


def draw_active_threshold_marker(
    draw: ImageDraw.ImageDraw,
    pos: tuple[int, int],
    *,
    radius: int = 26,
) -> None:
    cx, cy = pos
    draw.ellipse(
        (cx - radius, cy - radius, cx + radius, cy + radius), outline=_GREEN, width=4
    )
    font = load_font(14, bold=True)
    label = "ACTIVE"
    pad_x, pad_y = 3, 2
    left, top, right, bottom = draw.textbbox((0, 0), label, font=font)
    text_w = right - left
    text_h = bottom - top
    # Size the box from the rendered text so a taller fallback face can't
    # clip the label, but never below the established 22 px so the layout
    # (and the area the caller reserves) is unchanged for the normal font.
    box_h = max(22, text_h + 2 * pad_y)
    box_x0 = cx + radius + 6
    box_y0 = cy - box_h // 2
    box_x1 = box_x0 + text_w + 2 * pad_x
    box_y1 = box_y0 + box_h
    draw.rectangle(
        (box_x0, box_y0, box_x1, box_y1),
        fill=(255, 255, 255),
        outline=(0, 0, 0),
        width=1,
    )
    # Vertically centre the glyphs in the box; subtract the bbox bearing so
    # the font's own top/left offsets don't shift the text off-centre.
    text_x = box_x0 + pad_x - left
    text_y = box_y0 + (box_h - text_h) // 2 - top
    draw.text((text_x, text_y), label, fill=(0, 0, 0), font=font)


def draw_wind_arrow_badge(
    draw: ImageDraw.ImageDraw,
    center: tuple[int, int],
    *,
    from_dir_deg: int,
    speed_kts: int,
    box_w: int = 110,
    box_h: int = 110,
) -> None:
    """Draw a wind compass in the upper-right corner.

    Convention: arrow points in the direction the wind is BLOWING (i.e. the
    direction OPPOSITE to ``from_dir_deg``). Label includes ``FROM DIR / SPD``
    so the pilot doesn't need to remember the convention.
    """
    cx, cy = center
    draw.rectangle(
        (cx - box_w // 2, cy - box_h // 2, cx + box_w // 2, cy + box_h // 2),
        outline=_FG,
        width=2,
        fill=_BADGE_BG,
    )
    title_font = load_font(13, bold=True)
    draw.text((cx - 40, cy - box_h // 2 + 4), "WIND", fill=_FG, font=title_font)
    # Arrow direction in pixel space: x grows right, y grows down. North = up.
    going_deg = (from_dir_deg + 180) % 360
    going_rad = math.radians(going_deg - 90)
    arm_len = 36
    tip = (cx + arm_len * math.cos(going_rad), cy + arm_len * math.sin(going_rad))
    tail = (cx - arm_len * math.cos(going_rad), cy - arm_len * math.sin(going_rad))
    draw.line(tail + tip, fill=_FG, width=3)
    # Arrowhead.
    head_angle_rad = math.radians(20)
    for sign in (-1, +1):
        a = going_rad + sign * (math.pi - head_angle_rad)
        head_end = (tip[0] + 14 * math.cos(a), tip[1] + 14 * math.sin(a))
        draw.line((tip[0], tip[1], head_end[0], head_end[1]), fill=_FG, width=3)
    label_font = load_font(12, bold=True)
    draw.text(
        (cx - 50, cy + box_h // 2 - 18),
        f"FROM {from_dir_deg:03d}° / {speed_kts} kt",
        fill=_FG,
        font=label_font,
    )
