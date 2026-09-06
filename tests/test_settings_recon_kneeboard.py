"""Tests for target-recon kneeboard settings defaults."""

from __future__ import annotations

from game.settings.settings import Settings


def test_generate_target_recon_kneeboard_defaults_true() -> None:
    s = Settings()
    assert s.generate_target_recon_kneeboard is True


def test_target_recon_extra_threat_search_nmi_defaults_zero() -> None:
    s = Settings()
    assert s.target_recon_extra_threat_search_nmi == 0
