"""Esri World Imagery tile fetcher with on-disk cache.

The Esri ``World_Imagery`` tile service is free for non-commercial use and
requires no API key. Attribution is rendered onto the page by the
compositor (not this module). One retry on transient network failure; no
retry on HTTP 4xx/5xx (a 403 will recur immediately).

Cache layout: ``<cache_dir>/world_imagery/<z>/<x>/<y>.png``. The cache is
unbounded on disk; users delete it manually to reclaim space or force
refresh.
"""

from __future__ import annotations

import http.client
import io
import logging
import os
import threading
import time
from pathlib import Path
from typing import Optional
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from PIL import Image, UnidentifiedImageError

from game.version import VERSION as _RETRIBUTION_VERSION

logger = logging.getLogger(__name__)

ESRI_WORLD_IMAGERY_URL = (
    "https://services.arcgisonline.com/ArcGIS/rest/services/"
    "World_Imagery/MapServer/tile/{z}/{y}/{x}"
)
# Track the live Retribution version automatically so the tile-service ToS
# identifier stays accurate across releases without manual edits here.
USER_AGENT = f"retribution-kneeboard/{_RETRIBUTION_VERSION}"
DEFAULT_TIMEOUT = 15.0

# Defensive cap on per-tile response body size. Real Esri PNG tiles are
# ~10-60 KB; a 1 MB cap is generous yet bounds memory if a misconfigured
# proxy or hostile redirect returns an unbounded body.
MAX_TILE_BYTES = 1_048_576  # 1 MiB

# Per-thread flag so the first network failure of a generation pass logs at
# WARNING and subsequent ones drop to DEBUG. Thread-local so a concurrent
# generation pass on another thread (test harness, future parallel
# mission-gen) doesn't silently suppress the other thread's first warning.
#
# ``reset_failure_log_state`` only affects the calling thread (the flag is
# thread-local). The recon kneeboard pipeline is single-threaded today,
# so calling reset from the generation entry point covers all subsequent
# tile fetches in that pass. If page rendering is ever parallelised, each
# worker thread will need its own reset call.
_log_state = threading.local()


def _is_first_failure_logged() -> bool:
    return getattr(_log_state, "first_failure_logged", False)


def reset_failure_log_state() -> None:
    """Re-enable WARNING-level logging for the next generation pass.

    Only affects the calling thread; see the comment on ``_log_state``.
    """
    _log_state.first_failure_logged = False


def fetch_tile(
    z: int,
    x: int,
    y: int,
    cache_dir: Path,
    timeout: float = DEFAULT_TIMEOUT,
) -> Optional[Image.Image]:
    """Return the Esri World Imagery tile at ``(z, x, y)`` as an RGB Image.

    Cached under ``cache_dir/world_imagery/<z>/<x>/<y>.png``. Returns
    ``None`` on any failure (network, HTTP non-200, corrupt body); the
    caller is expected to fall back to a different basemap strategy.
    """
    cache_path = cache_dir / "world_imagery" / str(z) / str(x) / f"{y}.png"
    if cache_path.exists():
        try:
            return Image.open(cache_path).convert("RGB")
        except (OSError, UnidentifiedImageError):
            # Corrupt cache entry — drop it and refetch.
            cache_path.unlink(missing_ok=True)

    body = _http_get(ESRI_WORLD_IMAGERY_URL.format(z=z, x=x, y=y), timeout)
    if body is None:
        return None

    try:
        img = Image.open(io.BytesIO(body)).convert("RGB")
    except (OSError, UnidentifiedImageError) as exc:
        _log_failure(ESRI_WORLD_IMAGERY_URL.format(z=z, x=x, y=y), exc)
        return None

    # Atomic write: PIL.Image.save streams to disk and is non-atomic, so a
    # crash mid-write — or two pages racing to fetch the same tile — would
    # leave a partial PNG. Write to a per-fetch unique sibling tempfile
    # then os.replace(). Including pid+thread id+monotonic ns in the name
    # avoids concurrent fetchers of the same tile clobbering each other's
    # in-progress writes (each gets its own tempfile; the last os.replace
    # wins atomically).
    #
    # Disk-write failures (full disk, permission denied, parent missing)
    # must NOT crash the kneeboard generation pass. The successfully-
    # decoded image is still returned — callers get a working tile, just
    # without the disk cache benefit. The tempfile is cleaned up
    # best-effort and a single WARNING surfaces the underlying cause.
    tmp_path = cache_path.with_suffix(
        f"{cache_path.suffix}.{os.getpid()}.{threading.get_ident()}."
        f"{time.monotonic_ns()}.tmp"
    )
    try:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(tmp_path, "PNG")
        os.replace(tmp_path, cache_path)
    except Exception as exc:
        try:
            tmp_path.unlink()
        except OSError:
            pass
        logger.warning(
            "kneeboard_recon: failed to write tile cache %s (%s); "
            "continuing without on-disk caching for this tile",
            cache_path,
            exc,
        )
    return img


def _http_get(url: str, timeout: float) -> Optional[bytes]:
    """Single retry on transient network/protocol errors; none on HTTP non-200.

    Transient covers timeouts, connection resets/drops (including
    ``http.client.RemoteDisconnected``, which ``urllib`` does not wrap in
    ``URLError``), SSL errors and malformed responses. ``HTTPError`` (4xx/5xx)
    is handled separately and never retried.

    Caps the response body at ``MAX_TILE_BYTES + 1`` and rejects anything
    larger so a misconfigured proxy can't make a single fetch balloon
    memory unboundedly.
    """
    for attempt in (1, 2):
        try:
            req = Request(url, headers={"User-Agent": USER_AGENT})
            with urlopen(req, timeout=timeout) as resp:
                # ``urlopen`` raises ``HTTPError`` for 4xx/5xx, caught
                # below. The ``status`` check is the defensive backup
                # for custom HTTPHandlers (and test fakes) that return
                # a non-200 response without raising.
                status = getattr(resp, "status", 200)
                if status != 200:
                    _log_failure(url, f"HTTP {status}")
                    return None
                # Read one byte past the cap so we can detect oversize bodies.
                body = resp.read(MAX_TILE_BYTES + 1)
                if len(body) > MAX_TILE_BYTES:
                    _log_failure(
                        url,
                        f"response body exceeds {MAX_TILE_BYTES} byte cap",
                    )
                    return None
                return body
        except HTTPError as exc:
            # 4xx/5xx never get retried — a 403 (Esri ToS limit) or 5xx
            # recurs immediately on the next request from the same IP.
            _log_failure(url, f"HTTP {exc.code}")
            return None
        except (OSError, http.client.HTTPException) as exc:
            # ``urllib`` raises ``URLError`` (an ``OSError``) for DNS/refused
            # and ``socket.timeout``/``TimeoutError`` (also ``OSError``) for
            # slow responses, but it does NOT wrap
            # ``http.client.RemoteDisconnected`` ("Remote end closed
            # connection without response") in ``URLError`` — it escapes
            # ``getresponse()`` unwrapped on a dropped/reset connection.
            # ``RemoteDisconnected`` is a ``ConnectionResetError`` (OSError)
            # *and* a ``BadStatusLine``/``HTTPException``. Catching the
            # ``OSError`` + ``HTTPException`` families covers timeouts,
            # connection resets/drops, SSL errors and malformed responses so
            # any transient network/protocol failure degrades to the offline
            # basemap instead of aborting mission generation. ``HTTPError``
            # (4xx/5xx) is caught above and never reaches here.
            if attempt == 2:
                _log_failure(url, exc)
                return None
            # else: fall through to retry
    return None


def _log_failure(url: str, exc: object) -> None:
    if not _is_first_failure_logged():
        logger.warning(
            "kneeboard_recon: tile fetch failed: %s (%s); "
            "subsequent failures suppressed to DEBUG",
            url,
            exc,
        )
        _log_state.first_failure_logged = True
    else:
        logger.debug("kneeboard_recon: tile fetch failed: %s (%s)", url, exc)
