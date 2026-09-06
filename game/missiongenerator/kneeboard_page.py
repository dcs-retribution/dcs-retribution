"""Base class for kneeboard pages.

Kept in its own module to avoid circular imports between kneeboard.py and
kneeboard_recon/pages.py, which both need KneeboardPage.
"""

from __future__ import annotations

from pathlib import Path


class KneeboardPage:
    """Base class for all kneeboard pages."""

    def write(self, path: Path) -> None:
        """Writes the kneeboard page to the given path."""
        raise NotImplementedError
