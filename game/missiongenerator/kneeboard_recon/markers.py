# game/missiongenerator/kneeboard_recon/markers.py
"""Markers for recon kneeboard pages.

Three building blocks:

* :func:`draw_sidc_enemy` — simplified red SIDC-style diamond + glyph.
* :func:`draw_aimpoint_badge` — numbered T1/T2/… badge with optional dead overlay.
* :func:`draw_friendly_cp_marker` — small blue square for friendly control points.
* :func:`draw_building_footprint` — outlined polygon of a static's footprint.

Plus :class:`Aimpoint` (the data record consumed by the detail page footer
table) and :func:`cluster_items` (first-fit clustering for CAS-style
target groups with many units).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import (
    Any,
    Callable,
    TYPE_CHECKING,
    Iterable,
    List,
    Optional,
    Sequence,
    TypeVar,
)

_T = TypeVar("_T")

from PIL import ImageDraw
from dcs.mapping import Point

from game.utils import Heading

from ._fonts import load_font

if TYPE_CHECKING:
    from dcs.mapping import Polygon

_RED = (180, 20, 20)
_BLUE = (30, 70, 170)
_BLUE_LIGHT = (220, 230, 250)
_BLACK = (0, 0, 0)
_WHITE = (255, 255, 255)
_FG = (15, 15, 15)

# Public color constants for callers that draw their own friendly-CP boxes.
FRIENDLY_OUTLINE = _BLUE
FRIENDLY_FILL = _BLUE_LIGHT


def draw_sidc_enemy(
    draw: ImageDraw.ImageDraw,
    pos: tuple[int, int],
    glyph: str,
    size: int = 26,
) -> None:
    cx, cy = pos
    half = size // 2
    pts = [(cx, cy - half), (cx + half, cy), (cx, cy + half), (cx - half, cy)]
    draw.polygon(pts, fill=_RED, outline=_BLACK)
    font = load_font(max(12, size // 2), bold=True)
    tw = draw.textlength(glyph, font=font)
    draw.text((cx - tw / 2, cy - size // 3), glyph, fill=_WHITE, font=font)


def draw_aimpoint_badge(
    draw: ImageDraw.ImageDraw,
    pos: tuple[int, int],
    label: str,
    *,
    dead: bool = False,
    size: int = 18,
) -> None:
    cx, cy = pos
    draw.rectangle(
        (cx - size, cy - size, cx + size, cy + size), fill=_RED, outline=_FG, width=2
    )
    font = load_font(max(12, size), bold=True)
    tw = draw.textlength(label, font=font)
    draw.text((cx - tw / 2, cy - size // 2 - 2), label, fill=_WHITE, font=font)
    if dead:
        draw.line((cx - size, cy - size, cx + size, cy + size), fill=_BLACK, width=4)
        draw.line((cx - size, cy + size, cx + size, cy - size), fill=_BLACK, width=4)


def draw_friendly_cp_marker(
    draw: ImageDraw.ImageDraw,
    pos: tuple[int, int],
    name: str,
    *,
    size: int = 11,
) -> None:
    cx, cy = pos
    draw.rectangle(
        (cx - size, cy - size, cx + size, cy + size),
        fill=_BLUE_LIGHT,
        outline=_BLUE,
        width=2,
    )
    font = load_font(13, bold=True)
    draw.text((cx + size + 4, cy - 8), name, fill=_BLUE, font=font)


def draw_building_footprint(
    draw: ImageDraw.ImageDraw,
    corners: Sequence[tuple[int, int]],
    *,
    fill: tuple[int, int, int] = (232, 222, 200),
    outline: tuple[int, int, int] = _FG,
) -> None:
    if len(corners) < 3:
        return
    # Fill only; the width-2 polyline below draws the border. Passing
    # ``outline`` to polygon as well would stroke a redundant 1 px edge
    # under the thicker line, thickening it asymmetrically.
    draw.polygon(list(corners), fill=fill)
    draw.line(list(corners) + [corners[0]], fill=outline, width=2)


@dataclass(frozen=True)
class Aimpoint:
    """Single aimpoint or cluster on the detail page."""

    number: int  # 1, 2, ... -> label "T1", "T2"
    description: str  # e.g. "Factory bldg A" or "SR (1234)"
    position: Point
    heading_from_center: Heading
    footprint: Optional["Polygon"]  # rectangle if known dimensions
    is_dead: bool
    cluster_size: int = 1  # > 1 means this Aimpoint represents a group
    is_trailing: bool = False  # True iff this is the cap-overflow bucket

    @property
    def label(self) -> str:
        if self.is_trailing:
            return f"T{self.number} (… remaining)"
        if self.cluster_size > 1:
            return f"T{self.number} ({self.cluster_size}×)"
        return f"T{self.number}"


def cluster_items(
    items: Iterable[_T],
    *,
    position_of: Callable[[_T], Any],
    threshold_m: float = 75.0,
    cap: int = 12,
) -> List[tuple[list[_T], bool]]:
    """First-fit single-link cluster ``items`` by their position.

    Walks items in order; each item joins the first bucket containing
    *any* existing member within ``threshold_m`` (we scan all members and
    stop at the first match), else opens a new bucket. This is the
    standard single-link agglomerative criterion — two items can wind
    up in the same bucket with mutual distance > threshold when a chain
    of intermediate members links them. Acceptable here because
    kneeboard maps cluster dense armor groups where chaining mirrors
    visual intent.

    When the bucket count exceeds ``cap``, keeps the ``cap - 1`` largest
    and dumps the rest into a trailing bucket flagged ``True``.

    Returns ``[(items_in_bucket, is_trailing_bucket), ...]``.

    Worst-case O(n³): each item scans every bucket, each bucket scans
    every member. Kneeboard pages have <= ~30 items so this is fine.
    """
    items_list = list(items)
    buckets: List[List[_T]] = []
    for it in items_list:
        p = position_of(it)
        placed = False
        for bucket in buckets:
            for member in bucket:
                if p.distance_to_point(position_of(member)) <= threshold_m:
                    bucket.append(it)
                    placed = True
                    break
            if placed:
                break
        if not placed:
            buckets.append([it])

    if len(buckets) <= cap:
        return [(b, False) for b in buckets]

    # Over the cap: keep the (cap - 1) largest buckets but emit them in the
    # original input order so cluster numbering (T1..Tn) follows the corridor
    # walk, not bucket size. The remaining buckets collapse into one trailing
    # bucket flagged True.
    n_keep = cap - 1
    largest_idx = set(
        sorted(range(len(buckets)), key=lambda i: -len(buckets[i]))[:n_keep]
    )
    kept = [buckets[i] for i in range(len(buckets)) if i in largest_idx]
    leftover = [it for i, b in enumerate(buckets) if i not in largest_idx for it in b]
    return [(b, False) for b in kept] + [(leftover, True)]
