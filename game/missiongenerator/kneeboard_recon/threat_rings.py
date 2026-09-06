# game/missiongenerator/kneeboard_recon/threat_rings.py
"""Threat-ring rendering for recon kneeboard maps.

Each enemy threat may have:

* a max-range threat ring (solid red), drawn iff ``max_threat_range > 0``.
* a detection ring (dashed red), drawn iff ``max_detection_range > 0``.

Examples: EWRs have only a detection range; many AAA pieces have only a
threat range; SAMs typically have both.

Inputs are pre-converted to pixels by the caller via :class:`Projector`.
"""

from __future__ import annotations

from PIL import ImageDraw

_RED = (180, 20, 20)


def draw_threat_rings(
    draw: ImageDraw.ImageDraw,
    center: tuple[int, int],
    *,
    max_range_px: int,
    detection_range_px: int,
    dash_segments: int = 60,
) -> None:
    """Render max-range (solid) and detection (dashed) rings.

    Either ring is omitted when its corresponding ``*_px`` arg is zero.
    """
    cx, cy = center
    if detection_range_px > 0:
        bbox = (
            cx - detection_range_px,
            cy - detection_range_px,
            cx + detection_range_px,
            cy + detection_range_px,
        )
        # Each of the ``dash_segments`` segments draws its first half and
        # leaves the second half blank, yielding an even 50%-duty dashed
        # ring (dash and gap each span ``180 / dash_segments`` degrees).
        for i in range(dash_segments):
            a0 = i * 360 / dash_segments
            a1 = a0 + 360 / (2 * dash_segments)
            draw.arc(bbox, start=a0, end=a1, fill=_RED, width=2)
    if max_range_px > 0:
        bbox = (
            cx - max_range_px,
            cy - max_range_px,
            cx + max_range_px,
            cy + max_range_px,
        )
        draw.ellipse(bbox, outline=_RED, width=2)
