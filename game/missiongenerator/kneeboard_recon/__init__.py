"""Target recon kneeboard pages for player flights.

See docs/superpowers/specs/2026-05-20-target-recon-kneeboard-design.md.
"""

from .pages import (
    AirbaseReconPage,
    AirfieldDeparturePage,
    DetailReconPage,
    FrontLineDetailPage,
    OverviewReconPage,
    generate_recon_pages,
)

__all__ = [
    "AirbaseReconPage",
    "AirfieldDeparturePage",
    "DetailReconPage",
    "FrontLineDetailPage",
    "OverviewReconPage",
    "generate_recon_pages",
]
