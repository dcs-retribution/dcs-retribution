# game/missiongenerator/kneeboard_recon/label_layout.py
"""Collision-avoiding label placement for recon kneeboard pages.

Each labeled marker submits a :class:`LabelRequest`. After all markers are
placed (their pixel rectangles known) but before any labels are drawn, a
single pass resolves collisions in three tiers:

1. **Close 8-offset ring** (gap 6 px, priority E, NE, N, NW, W, SW, S, SE).
   The label sits right next to the marker with no leader line.
2. **Leader-line spiral search** at distances 40, 60, 90, 140, 200 px in the
   same 8 directions. The first slot that fits without colliding with any
   previously-placed blocker wins. A thin leader line connects the
   marker-facing edge of the label back to the marker anchor.
3. **Best-effort fallback** at 40 px east with overlap accepted — only
   reached when even the far spiral can't find a clear slot, which on
   real kneeboards essentially only happens in degenerate test cases.

Tier 2 is what stops same-anchor clusters (e.g. four ground-start aircraft
spawning ~6 px apart on a 5 km airfield diagram) from collapsing all
labels onto the same pixel: each subsequent label sees prior labels as
blockers and is forced to a different leader position.

This is intentionally O(n²) — kneeboard pages have <= ~30 labels, so
n-squared is plenty fast and we avoid pulling in a third-party layout lib.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Sequence


@dataclass(frozen=True)
class Rect:
    x0: int
    y0: int
    x1: int
    y1: int

    def intersects(self, other: "Rect") -> bool:
        return not (
            self.x1 < other.x0
            or other.x1 < self.x0
            or self.y1 < other.y0
            or other.y1 < self.y0
        )

    def contained_in(self, outer: "Rect") -> bool:
        return (
            outer.x0 <= self.x0
            and outer.y0 <= self.y0
            and self.x1 <= outer.x1
            and self.y1 <= outer.y1
        )

    def contains_point(self, point: tuple[int, int]) -> bool:
        px, py = point
        return self.x0 <= px <= self.x1 and self.y0 <= py <= self.y1


@dataclass(frozen=True)
class LabelRequest:
    anchor: tuple[int, int]
    width: int
    height: int


@dataclass(frozen=True)
class Leader:
    src: tuple[int, int]  # label edge
    dest: tuple[int, int]  # marker anchor


@dataclass(frozen=True)
class PlacedLabel:
    rect: Rect
    leader: Optional[Leader]


# Priority order: E, NE, N, NW, W, SW, S, SE.
# (dx_sign, dy_sign, gap_px) for the tight no-leader ring.
_OFFSETS = [
    (+1, 0, 6),  # E
    (+1, -1, 6),  # NE
    (0, -1, 6),  # N
    (-1, -1, 6),  # NW
    (-1, 0, 6),  # W
    (-1, +1, 6),  # SW
    (0, +1, 6),  # S
    (+1, +1, 6),  # SE
]

# Directions for the leader-line spiral (same E/NE/.../SE priority, no gap).
_LEADER_DIRECTIONS = [(dx, dy) for dx, dy, _ in _OFFSETS]

# Leader-line stand-off distances tried in order. Starts close (40 px keeps
# the label visually associated with the marker) and grows to ~200 px so
# very tight clusters can fan out before the best-effort fallback kicks in.
_LEADER_DISTANCES = (40, 60, 90, 140, 200)

# Last-resort fallback distance used when even the spiral can't find a slot.
_LEADER_FALLBACK_PX = _LEADER_DISTANCES[0]


def _candidate_rect(
    anchor: tuple[int, int],
    width: int,
    height: int,
    dx_sign: int,
    dy_sign: int,
    gap: int,
) -> Rect:
    ax, ay = anchor
    if dx_sign == +1:
        x0 = ax + gap
        x1 = x0 + width
    elif dx_sign == -1:
        x1 = ax - gap
        x0 = x1 - width
    else:
        x0 = ax - width // 2
        x1 = x0 + width
    if dy_sign == -1:
        y1 = ay - gap
        y0 = y1 - height
    elif dy_sign == +1:
        y0 = ay + gap
        y1 = y0 + height
    else:
        y0 = ay - height // 2
        y1 = y0 + height
    return Rect(x0, y0, x1, y1)


def _clamp_to_page(rect: Rect, page: Rect) -> Rect:
    dx = 0
    dy = 0
    if rect.x0 < page.x0:
        dx = page.x0 - rect.x0
    elif rect.x1 > page.x1:
        dx = page.x1 - rect.x1
    if rect.y0 < page.y0:
        dy = page.y0 - rect.y0
    elif rect.y1 > page.y1:
        dy = page.y1 - rect.y1
    return Rect(rect.x0 + dx, rect.y0 + dy, rect.x1 + dx, rect.y1 + dy)


def _label_edge_toward(rect: Rect, anchor: tuple[int, int]) -> tuple[int, int]:
    """Closest point on ``rect``'s boundary to ``anchor`` — used as the
    leader-line source so the line meets the label cleanly on whichever
    side the marker is."""
    ax, ay = anchor
    if ax < rect.x0:
        x = rect.x0
    elif ax > rect.x1:
        x = rect.x1
    else:
        x = ax
    if ay < rect.y0:
        y = rect.y0
    elif ay > rect.y1:
        y = rect.y1
    else:
        y = ay
    if rect.contains_point(anchor):
        # Anchor is inside the rect (degenerate clamp). Returning it verbatim
        # would make a zero-length leader that draws nothing, so snap to the
        # nearest edge instead and keep the leader visible.
        to_left, to_right = ax - rect.x0, rect.x1 - ax
        to_top, to_bottom = ay - rect.y0, rect.y1 - ay
        nearest = min(to_left, to_right, to_top, to_bottom)
        if nearest == to_left:
            x = rect.x0
        elif nearest == to_right:
            x = rect.x1
        elif nearest == to_top:
            y = rect.y0
        else:
            y = rect.y1
    return (int(x), int(y))


def place_labels(
    requests: Sequence[LabelRequest],
    *,
    occupied: Sequence[Rect],
    page_bbox: Rect,
) -> List[PlacedLabel]:
    """Resolve label positions, returning one PlacedLabel per request."""
    placed: List[PlacedLabel] = []
    blockers: List[Rect] = list(occupied)
    for req in requests:
        chosen: Optional[PlacedLabel] = None

        # Tier 1: tight 8-offset ring, no leader line.
        for dx, dy, gap in _OFFSETS:
            candidate = _candidate_rect(req.anchor, req.width, req.height, dx, dy, gap)
            candidate = _clamp_to_page(candidate, page_bbox)
            if not candidate.contained_in(page_bbox):
                continue
            if candidate.contains_point(req.anchor):
                # Clamping (near a page edge) pulled the leaderless label
                # back over its own marker. A no-leader label must sit
                # beside the marker, not on it, so fall through to the
                # leader-line search.
                continue
            if any(candidate.intersects(b) for b in blockers):
                continue
            chosen = PlacedLabel(rect=candidate, leader=None)
            break

        # Tier 2: leader-line spiral search at increasing distances.
        # The previous version always picked the same +40 east offset, so
        # several near-coincident anchors all stacked their leader labels
        # on top of each other. By iterating distance × direction and
        # checking blockers (which include prior labels), each subsequent
        # label is forced onto a free spot.
        if chosen is None:
            for distance in _LEADER_DISTANCES:
                if chosen is not None:
                    break
                for dx, dy in _LEADER_DIRECTIONS:
                    candidate = _candidate_rect(
                        req.anchor,
                        req.width,
                        req.height,
                        dx,
                        dy,
                        distance,
                    )
                    candidate = _clamp_to_page(candidate, page_bbox)
                    if not candidate.contained_in(page_bbox):
                        continue
                    if any(candidate.intersects(b) for b in blockers):
                        continue
                    leader = Leader(
                        src=_label_edge_toward(candidate, req.anchor),
                        dest=req.anchor,
                    )
                    chosen = PlacedLabel(rect=candidate, leader=leader)
                    break

        # Tier 3: best-effort fallback — push east by 40 px and accept any
        # remaining overlap. Hit only in degenerate cases (a page so full
        # of blockers that no spiral slot at any tested distance is free).
        if chosen is None:
            candidate = _candidate_rect(
                req.anchor,
                req.width,
                req.height,
                +1,
                0,
                _LEADER_FALLBACK_PX,
            )
            candidate = _clamp_to_page(candidate, page_bbox)
            leader = Leader(
                src=_label_edge_toward(candidate, req.anchor),
                dest=req.anchor,
            )
            chosen = PlacedLabel(rect=candidate, leader=leader)

        placed.append(chosen)
        blockers.append(chosen.rect)
    return placed
