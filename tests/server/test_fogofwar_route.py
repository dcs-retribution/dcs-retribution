"""The /fog-of-war/reveal endpoint flips the shared, transient overview flag.

The flag is process-global, so each test restores it to off afterwards to keep
the fog assertions in the rest of the suite deterministic.
"""

from typing import Iterator

import pytest

from game.server.fogofwar.routes import get_reveal, set_reveal
from game.theater.fogofwar import fog_revealed, set_fog_revealed


@pytest.fixture(autouse=True)
def _restore_flag() -> Iterator[None]:
    yield
    set_fog_revealed(False)


def test_default_is_off() -> None:
    assert fog_revealed() is False
    assert get_reveal() is False


def test_set_reveal_flips_the_shared_flag() -> None:
    set_reveal(True)
    assert fog_revealed() is True
    assert get_reveal() is True

    set_reveal(False)
    assert fog_revealed() is False
    assert get_reveal() is False
