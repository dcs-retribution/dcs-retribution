"""Two convoys must never share a DCS group name.

Convoy names are minted by a counter that mission generation reset every turn, but a
convoy lives across turns while it travels. So a new convoy could be handed a name a
travelling one still carried, their units collided in the unit map, and Take Off died
with "Duplicate convoy unit: Convoy 002 Unit #1" — with no way out of the save.
"""

from __future__ import annotations

from game.naming import namegen


def test_reset_numbers_keeps_the_convoy_counters_running() -> None:
    """Per-mission group numbering resets; campaign-object numbering must not."""
    namegen.convoy_number = 7
    namegen.cargo_ship_number = 3
    namegen.number = 99

    namegen.reset_numbers()

    assert namegen.convoy_number == 7, "a travelling convoy still owns its name"
    assert namegen.cargo_ship_number == 3
    assert namegen.number == 0, "per-mission numbering still resets"


def test_consecutive_names_do_not_repeat_across_a_reset() -> None:
    namegen.convoy_number = 0
    first = namegen.next_convoy_name()
    namegen.reset_numbers()
    second = namegen.next_convoy_name()

    assert first != second, "mission generation minted a name already in use"


def test_a_save_that_already_has_duplicates_still_generates() -> None:
    """The counter fix stops NEW collisions; campaigns saved before it already carry
    duplicates, so the generator disambiguates rather than stranding the save.

    Drives the real generate_convoy() with its group construction stubbed out — what
    is under test is the name it asks for, not the pydcs group it builds.
    """
    from types import SimpleNamespace
    from typing import Any

    from game.missiongenerator.convoygenerator import ConvoyGenerator

    generator: Any = object.__new__(ConvoyGenerator)
    asked: list[str] = []

    def fake_group(name: str, *_args: Any, **_kwargs: Any) -> Any:
        asked.append(name)
        return SimpleNamespace(units=[], points=[SimpleNamespace(tasks=[])])

    generator._create_mixed_unit_group = fake_group
    generator.unit_map = SimpleNamespace(add_convoy_units=lambda *_a: None)

    convoy: Any = SimpleNamespace(
        name="Convoy 002",
        route_start=SimpleNamespace(x=0, y=0),
        route_end=SimpleNamespace(x=1, y=1),
        units={},
        player_owned=False,
        iter_units=lambda: iter(()),
    )

    used: set[str] = set()
    for _ in range(3):
        try:
            generator.generate_convoy(convoy, used)
        except Exception:
            pass  # the stubbed group cannot finish routing; the name is already chosen

    assert asked == ["Convoy 002", "Convoy 002 (2)", "Convoy 002 (3)"]
