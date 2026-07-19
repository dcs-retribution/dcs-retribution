"""Transient "overview" reveal toggle for the recon fog-of-war.

The 414th recon fog hides enemy composition, threat/detection rings, and SCAR
command posts from the human side until they are scouted (see the viewer-aware
visibility layer in ``theatergroup``/``theatergroundobject``). This module adds a
single runtime switch that, while enabled, forces every player-facing fog
accessor to resolve to ground truth — the "show the real picture" overview.

It is deliberately a process-global runtime flag, **never persisted**: loading a
save always starts with the fog intact, so a god-view can't be baked into a
campaign or shared by accident. The flag is flipped from the main window's
"Reveal fog of war" view action; the three fog chokepoints (``alive_for``,
``known_for``, ``hidden_on_player_map``) consult ``fog_revealed()`` and short to
truth when it is on. AI/planner/threat math already pass ``viewer=None`` and are
therefore unaffected either way.

This module intentionally has no imports so it can be pulled in from anywhere in
the theater layer without risk of an import cycle.
"""

from __future__ import annotations

_revealed: bool = False


def fog_revealed() -> bool:
    """Whether the overview is on (player-facing fog forced to ground truth)."""
    return _revealed


def set_fog_revealed(value: bool) -> None:
    """Enable/disable the overview. Runtime-only; never written to a save."""
    global _revealed
    _revealed = bool(value)
