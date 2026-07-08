from __future__ import annotations

from types import SimpleNamespace
from typing import cast

import pytest
from faker import Faker

from game.coalition import Coalition
from game.dcs.countries import country_with_name
from game.squadrons.pilotnames import (
    COUNTRY_FAKER_LOCALES,
    faker_for_country,
    faker_for_locale,
)
from game.squadrons.squadron import Squadron

FALLBACK = Faker("en_US")


def test_mapped_country_uses_its_own_locale() -> None:
    faker = faker_for_country(country_with_name("Greece"), FALLBACK)
    assert faker is not FALLBACK
    assert faker is faker_for_locale("el_GR")


def test_unmapped_country_falls_back() -> None:
    # The multinational CJTF "country" has no national locale of its own.
    cjtf = country_with_name("Combined Joint Task Forces Blue")
    assert faker_for_country(cjtf, FALLBACK) is FALLBACK


def test_none_country_falls_back() -> None:
    assert faker_for_country(None, FALLBACK) is FALLBACK


def test_locale_is_cached_independent_of_fallback() -> None:
    # The faker is cached by locale, so the fallback passed on a later call
    # never changes which instance a mapped country resolves to.
    a = faker_for_country(country_with_name("Iran"), FALLBACK)
    b = faker_for_country(country_with_name("Iran"), Faker("ru_RU"))
    assert a is b


@pytest.mark.parametrize("country_name,locale", sorted(COUNTRY_FAKER_LOCALES.items()))
def test_every_mapped_locale_generates_a_name(country_name: str, locale: str) -> None:
    # Guards the table: every mapped locale must build a usable, gender-aware
    # Faker (a typo'd or non-gendered locale would silently fall back, which is
    # a map mistake to fix rather than ship).
    faker = faker_for_locale(locale)
    assert faker is not None, f"{country_name}: locale {locale!r} is unusable"
    # ``name_male``/``name_female`` return a non-empty ``str``; one call each is
    # enough to prove the locale produces a gendered name.
    assert faker.name_male()
    assert faker.name_female()


def test_every_mapped_country_name_is_a_real_pydcs_country() -> None:
    # The table is keyed by ``Country.name`` while ``CountryAssigner`` keys by
    # ``Country.id`` (§627). A typo'd or renamed key (e.g. "Czeck Republic")
    # would never match a real country, so its pilots would silently fall back
    # to the faction locale with no other signal. Cross-check every key against
    # pydcs so a stale entry fails CI instead of shipping.
    from dcs.countries import country_dict

    valid_names = {country.name for country in country_dict.values()}
    unknown = sorted(name for name in COUNTRY_FAKER_LOCALES if name not in valid_names)
    assert not unknown, f"Unknown pydcs country names in the locale table: {unknown}"


def _squadron(country_name: str, fallback: Faker) -> Squadron:
    squadron = Squadron.__new__(Squadron)
    squadron.country = country_with_name(country_name)
    squadron.coalition = cast(Coalition, SimpleNamespace(faker=fallback))
    return squadron


def test_squadron_faker_resolves_to_country_locale() -> None:
    assert _squadron("Greece", FALLBACK).faker is faker_for_locale("el_GR")


def test_squadron_recruits_named_pilots_from_country_locale() -> None:
    squadron = _squadron("Greece", FALLBACK)
    squadron.female_pilot_percentage = 0  # force the name_male() path
    squadron.pilot_pool = []
    squadron.current_roster = []
    squadron.available_pilots = []
    squadron._recruit_pilots(3)
    assert len(squadron.current_roster) == 3
    assert all(pilot.name for pilot in squadron.current_roster)
