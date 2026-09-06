"""Shared font loader for recon kneeboard rendering.

Tries courbd.ttf / cour.ttf first (matches the existing kneeboard look),
falls back to DejaVuSansMono for systems without the Courier shipped fonts,
and finally to PIL's bitmap default if neither is available.
"""

from __future__ import annotations

from functools import lru_cache

from typing import Union

from PIL import ImageFont

# Canonical font type used throughout the recon kneeboard.  PIL's two font
# classes — FreeTypeFont (returned by truetype()) and ImageFont (returned by
# load_default()) — are siblings, not parent/child, so both must appear in
# the Union.  All PIL drawing surfaces accept either.
PilFont = Union[ImageFont.FreeTypeFont, ImageFont.ImageFont]


# A single page render calls this 10-20 times across markers, badges, labels,
# scale bars, ATIS panels. ``ImageFont.truetype`` parses the font file on
# every call — caching gives the same FreeType handle back so a 20-flight
# mission generation avoids ~360 redundant font-file reads.
@lru_cache(maxsize=64)
def load_font(size: int, *, bold: bool = False) -> PilFont:
    for b, r in (
        ("courbd.ttf", "cour.ttf"),
        ("DejaVuSansMono-Bold.ttf", "DejaVuSansMono.ttf"),
    ):
        try:
            return ImageFont.truetype(
                b if bold else r, size, layout_engine=ImageFont.Layout.BASIC
            )
        except OSError:
            continue
    return ImageFont.load_default()
