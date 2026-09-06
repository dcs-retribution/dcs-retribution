# game/missiongenerator/kneeboard_recon/tests/test_label_layout.py
"""Tests for collision-avoiding label placement."""

from __future__ import annotations

import pytest

from game.missiongenerator.kneeboard_recon.label_layout import (
    LabelRequest,
    PlacedLabel,
    Rect,
    _label_edge_toward,
    place_labels,
)


def _r(x0: int, y0: int, x1: int, y1: int) -> Rect:
    return Rect(x0, y0, x1, y1)


def test_single_label_places_east_of_anchor() -> None:
    req = LabelRequest(anchor=(100, 100), width=40, height=14)
    placed = place_labels([req], occupied=[], page_bbox=_r(0, 0, 1000, 1000))
    assert len(placed) == 1
    p = placed[0]
    # East offset: label is to the right of (100, 100).
    assert p.rect.x0 >= 100
    assert p.leader is None


def test_label_avoids_occupied_marker_by_falling_back_to_north() -> None:
    # Block the east offset.
    occupied = [_r(105, 88, 200, 112)]
    req = LabelRequest(anchor=(100, 100), width=40, height=14)
    placed = place_labels([req], occupied=occupied, page_bbox=_r(0, 0, 1000, 1000))
    assert len(placed) == 1
    # No overlap with the occupied rect.
    p = placed[0]
    assert not p.rect.intersects(occupied[0])


def test_label_avoids_other_labels() -> None:
    reqs = [
        LabelRequest(anchor=(100, 100), width=40, height=14),
        LabelRequest(anchor=(110, 100), width=40, height=14),
    ]
    placed = place_labels(reqs, occupied=[], page_bbox=_r(0, 0, 1000, 1000))
    assert len(placed) == 2
    assert not placed[0].rect.intersects(placed[1].rect)


def test_label_falls_back_to_leader_when_all_8_offsets_collide() -> None:
    # Surround the anchor with occupied rects in all 8 octants.
    req = LabelRequest(anchor=(100, 100), width=20, height=12)
    occupied = [
        _r(110, 90, 200, 110),  # E
        _r(110, 60, 200, 90),  # NE
        _r(85, 60, 115, 90),  # N
        _r(0, 60, 90, 90),  # NW
        _r(0, 90, 90, 110),  # W
        _r(0, 110, 90, 200),  # SW
        _r(85, 110, 115, 200),  # S
        _r(110, 110, 200, 200),  # SE
    ]
    placed = place_labels([req], occupied=occupied, page_bbox=_r(0, 0, 1000, 1000))
    assert len(placed) == 1
    assert placed[0].leader is not None
    # Leader connects the marker anchor to the label.
    lx, ly = placed[0].leader.dest
    assert (lx, ly) == (100, 100)


def test_leaderless_label_never_clamped_onto_its_marker() -> None:
    # Anchor hard against the right edge: the tight east offset would clamp
    # back over the marker. A no-leader label must not sit on the marker.
    req = LabelRequest(anchor=(998, 500), width=40, height=14)
    placed = place_labels([req], occupied=[], page_bbox=_r(0, 0, 1000, 1000))
    p = placed[0]
    if p.leader is None:
        assert not p.rect.contains_point(req.anchor)


def test_label_edge_toward_snaps_to_edge_when_anchor_inside() -> None:
    # Anchor inside the rect would yield a zero-length leader if returned
    # verbatim; it must snap to the nearest edge instead.
    rect = _r(0, 0, 100, 20)
    assert _label_edge_toward(rect, (50, 10)) == (50, 0)  # nearest edge: top
    assert _label_edge_toward(rect, (90, 10)) == (100, 10)  # nearest edge: right


def test_label_respects_page_bbox() -> None:
    req = LabelRequest(anchor=(995, 5), width=40, height=14)
    placed = place_labels([req], occupied=[], page_bbox=_r(0, 0, 1000, 1000))
    # All four corners of the placed rect must be inside the page bbox.
    p = placed[0].rect
    assert 0 <= p.x0 and p.x1 <= 1000
    assert 0 <= p.y0 and p.y1 <= 1000
