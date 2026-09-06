"""Tests for the Esri World Imagery tile fetcher and disk cache."""

from __future__ import annotations

import http.client
import io
import socket
from collections.abc import Generator
from pathlib import Path
from typing import Any
from unittest.mock import patch, MagicMock
from urllib.error import HTTPError, URLError
from urllib.request import Request

import pytest
from PIL import Image

from game.missiongenerator.kneeboard_recon import tile_source
from game.missiongenerator.kneeboard_recon.tile_source import (
    ESRI_WORLD_IMAGERY_URL,
    fetch_tile,
    reset_failure_log_state,
)


def _png_bytes(color: tuple[int, int, int] = (10, 20, 30)) -> bytes:
    """Generate a tiny PNG byte string of the given solid colour."""
    buf = io.BytesIO()
    Image.new("RGB", (16, 16), color).save(buf, "PNG")
    return buf.getvalue()


@pytest.fixture(autouse=True)
def _reset_failure_state() -> Generator[None, None, None]:
    reset_failure_log_state()
    yield
    reset_failure_log_state()


def test_fetch_tile_returns_cached_image_without_network(tmp_path: Path) -> None:
    cache_path = tmp_path / "world_imagery" / "15" / "16383" / "16384.png"
    cache_path.parent.mkdir(parents=True)
    cache_path.write_bytes(_png_bytes(color=(40, 80, 120)))

    with patch.object(tile_source, "urlopen") as mock_url:
        img = fetch_tile(15, 16383, 16384, tmp_path)
        mock_url.assert_not_called()

    assert img is not None
    assert img.size == (16, 16)
    assert img.getpixel((0, 0)) == (40, 80, 120)


def test_fetch_tile_downloads_when_missing(tmp_path: Path) -> None:
    body = _png_bytes(color=(0, 255, 0))

    class FakeResp:
        status = 200

        def read(self, _n: int = -1) -> bytes:
            return body

        def __enter__(self) -> "FakeResp":
            return self

        def __exit__(self, *a: Any) -> None:
            pass

    seen_urls: list[str] = []

    def fake_urlopen(req: Request, timeout: float | None = None) -> FakeResp:
        seen_urls.append(req.full_url if hasattr(req, "full_url") else str(req))
        return FakeResp()

    with patch.object(tile_source, "urlopen", side_effect=fake_urlopen):
        img = fetch_tile(10, 511, 511, tmp_path)

    assert img is not None
    cache_path = tmp_path / "world_imagery" / "10" / "511" / "511.png"
    assert cache_path.exists()
    assert seen_urls == [ESRI_WORLD_IMAGERY_URL.format(z=10, x=511, y=511)]


def test_fetch_tile_returns_none_on_urlerror(tmp_path: Path) -> None:
    with patch.object(tile_source, "urlopen", side_effect=URLError("dns")):
        result = fetch_tile(8, 1, 1, tmp_path)
    assert result is None
    # cache must NOT contain a stub file on failure.
    assert not (tmp_path / "world_imagery" / "8" / "1" / "1.png").exists()


def test_fetch_tile_retries_once_on_transient_failure(tmp_path: Path) -> None:
    body = _png_bytes(color=(1, 2, 3))

    class FakeResp:
        status = 200

        def read(self, _n: int = -1) -> bytes:
            return body

        def __enter__(self) -> "FakeResp":
            return self

        def __exit__(self, *a: Any) -> None:
            pass

    call_count: dict[str, int] = {"n": 0}

    def fake_urlopen(req: Request, timeout: float | None = None) -> FakeResp:
        call_count["n"] += 1
        if call_count["n"] == 1:
            raise socket.timeout("first try slow")
        return FakeResp()

    with patch.object(tile_source, "urlopen", side_effect=fake_urlopen):
        img = fetch_tile(12, 3, 4, tmp_path)

    assert img is not None
    assert call_count["n"] == 2


def test_fetch_tile_returns_none_on_http_4xx(tmp_path: Path) -> None:
    # Real ``urllib.request.urlopen`` raises ``HTTPError`` on 4xx/5xx;
    # this is the path production actually hits. (The status-check
    # branch in ``_http_get`` is a defensive backup for custom handlers
    # that return non-200 without raising.)
    url = ESRI_WORLD_IMAGERY_URL.format(z=14, y=100, x=100)
    err = HTTPError(url, 403, "Forbidden", hdrs=http.client.HTTPMessage(), fp=None)
    with patch.object(tile_source, "urlopen", side_effect=err):
        result = fetch_tile(14, 100, 100, tmp_path)
    assert result is None
    assert not (tmp_path / "world_imagery" / "14" / "100" / "100.png").exists()


def test_fetch_tile_returns_none_on_non_raising_http_4xx(tmp_path: Path) -> None:
    # Defensive backup path: a custom HTTPHandler (or test fake) that
    # surfaces ``status=403`` without raising still gets refused.
    class FakeResp:
        status = 403

        def read(self, _n: int = -1) -> bytes:
            return b""

        def __enter__(self) -> "FakeResp":
            return self

        def __exit__(self, *a: Any) -> None:
            pass

    with patch.object(tile_source, "urlopen", return_value=FakeResp()):
        result = fetch_tile(14, 100, 100, tmp_path)
    assert result is None
    assert not (tmp_path / "world_imagery" / "14" / "100" / "100.png").exists()


def test_fetch_tile_returns_none_on_corrupt_response_body(tmp_path: Path) -> None:
    class FakeResp:
        status = 200

        def read(self, _n: int = -1) -> bytes:
            return b"not a PNG"

        def __enter__(self) -> "FakeResp":
            return self

        def __exit__(self, *a: Any) -> None:
            pass

    with patch.object(tile_source, "urlopen", return_value=FakeResp()):
        result = fetch_tile(13, 5, 6, tmp_path)
    assert result is None


def test_fetch_tile_corrupt_cache_file_is_repaired(tmp_path: Path) -> None:
    # Pre-seed an invalid cache file. fetch_tile should delete it and refetch.
    cache_path = tmp_path / "world_imagery" / "9" / "1" / "2.png"
    cache_path.parent.mkdir(parents=True)
    cache_path.write_bytes(b"garbage")

    body = _png_bytes(color=(33, 66, 99))

    class FakeResp:
        status = 200

        def read(self, _n: int = -1) -> bytes:
            return body

        def __enter__(self) -> "FakeResp":
            return self

        def __exit__(self, *a: Any) -> None:
            pass

    with patch.object(tile_source, "urlopen", return_value=FakeResp()):
        img = fetch_tile(9, 1, 2, tmp_path)

    assert img is not None
    assert img.getpixel((0, 0)) == (33, 66, 99)


def test_fetch_tile_returns_none_on_remote_disconnected(tmp_path: Path) -> None:
    # ``http.client.RemoteDisconnected`` ("Remote end closed connection
    # without response") is a ``ConnectionResetError``/``BadStatusLine`` and
    # is NOT wrapped by ``urllib`` in ``URLError`` when raised from
    # ``getresponse()``. It must still degrade to ``None`` (offline basemap
    # fallback) rather than escaping and aborting mission generation.
    disconnect = http.client.RemoteDisconnected(
        "Remote end closed connection without response"
    )
    with patch.object(tile_source, "urlopen", side_effect=disconnect):
        result = fetch_tile(8, 2, 3, tmp_path)
    assert result is None
    assert not (tmp_path / "world_imagery" / "8" / "2" / "3.png").exists()


def test_fetch_tile_recovers_from_transient_remote_disconnected(
    tmp_path: Path,
) -> None:
    # A dropped connection is transient: the single retry must succeed.
    body = _png_bytes(color=(7, 8, 9))

    class FakeResp:
        status = 200

        def read(self, _n: int = -1) -> bytes:
            return body

        def __enter__(self) -> "FakeResp":
            return self

        def __exit__(self, *a: Any) -> None:
            pass

    call_count: dict[str, int] = {"n": 0}

    def fake_urlopen(req: Request, timeout: float | None = None) -> FakeResp:
        call_count["n"] += 1
        if call_count["n"] == 1:
            raise http.client.RemoteDisconnected(
                "Remote end closed connection without response"
            )
        return FakeResp()

    with patch.object(tile_source, "urlopen", side_effect=fake_urlopen):
        img = fetch_tile(12, 3, 4, tmp_path)

    assert img is not None
    assert call_count["n"] == 2
