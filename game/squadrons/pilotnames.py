from __future__ import annotations

from functools import lru_cache
from typing import Optional, Sequence

from dcs.country import Country
from faker import Faker

# Map a DCS country (by its pydcs ``Country.name``) to a Faker locale so a
# squadron's pilots are named in their own nation's convention rather than the
# single shared faction locale. This completes the per-squadron DCS country
# feature (issue #627): the squadron's country is already correct on the
# generated ``.miz`` group (and drives the per-nation voiceovers), so the roster
# should match — a Greek squadron under the Greek flag should not be full of
# "John Smith"s.
#
# Only locales shipped with Faker are listed. Any unmapped country — including
# the multinational / irregular "countries" (the CJTFs, Insurgents, UN
# Peacekeepers) — falls back to the coalition's faction-locale Faker, so this can
# only ever *improve* a name, never break generation. Keyed by the exact pydcs
# name (see ``dcs.countries.country_dict``). Several nations share a locale where
# Faker has no closer match (e.g. Belarus/Kazakhstan -> ru_RU, the smaller Arab
# states -> the generic ``ar_AA``); that is deliberate and still better than the
# faction default.
COUNTRY_FAKER_LOCALES: dict[str, str] = {
    # --- Anglosphere -------------------------------------------------------
    "USA": "en_US",
    "USAF Aggressors": "en_US",
    "UK": "en_GB",
    "Canada": "en_CA",
    "Australia": "en_AU",
    "New Zealand": "en_NZ",
    # --- Western & Central Europe -----------------------------------------
    "France": "fr_FR",
    "Belgium": "nl_BE",
    "The Netherlands": "nl_NL",
    "Germany": "de_DE",
    "GDR": "de_DE",
    "Third Reich": "de_DE",
    "Austria": "de_AT",
    "Switzerland": "de_CH",
    "Italy": "it_IT",
    "Italian Social Republic": "it_IT",
    "Spain": "es_ES",
    "Portugal": "pt_PT",
    "Greece": "el_GR",
    "Cyprus": "el_CY",
    # --- Nordics -----------------------------------------------------------
    "Sweden": "sv_SE",
    "Norway": "no_NO",
    "Denmark": "da_DK",
    "Finland": "fi_FI",
    # --- Eastern Europe / former USSR -------------------------------------
    "Poland": "pl_PL",
    "Czech Republic": "cs_CZ",
    "Slovakia": "sk_SK",
    "Slovenia": "sl_SI",
    "Croatia": "hr_HR",
    "Bulgaria": "bg_BG",
    "Romania": "ro_RO",
    "Hungary": "hu_HU",
    "Russia": "ru_RU",
    "USSR": "ru_RU",
    "Belarus": "ru_RU",
    "Kazakhstan": "ru_RU",
    "Ukraine": "uk_UA",
    "Georgia": "ka_GE",
    "Abkhazia": "ru_RU",
    "South Ossetia": "ru_RU",
    # --- Middle East / North Africa (Arabic) ------------------------------
    "Iraq": "ar_AA",
    "Syria": "ar_AA",
    "Saudi Arabia": "ar_SA",
    "Egypt": "ar_EG",
    "Jordan": "ar_JO",
    "Bahrain": "ar_BH",
    "United Arab Emirates": "ar_AE",
    "Kuwait": "ar_AA",
    "Qatar": "ar_AA",
    "Oman": "ar_AA",
    "Lebanon": "ar_AA",
    "Libya": "ar_AA",
    "Algeria": "ar_AA",
    "Morocco": "ar_AA",
    "Tunisia": "ar_AA",
    "Sudan": "ar_AA",
    # --- Non-Arabic Middle East / Central & South Asia --------------------
    "Iran": "fa_IR",
    "Afghanistan": "fa_IR",
    "Israel": "he_IL",
    "Turkey": "tr_TR",
    "Pakistan": "en_PK",
    "India": "en_IN",
    # --- East & Southeast Asia --------------------------------------------
    "China": "zh_CN",
    "Japan": "ja_JP",
    "South Korea": "ko_KR",
    "North Korea": "ko_KR",
    "Indonesia": "id_ID",
    "Malaysia": "id_ID",
    "Philippines": "fil_PH",
    "Thailand": "th_TH",
    "Vietnam": "vi_VN",
    # --- Latin America (Spanish / Portuguese) -----------------------------
    "Mexico": "es_MX",
    # es_AR ships without a male/female name provider, so Argentina uses the
    # generic Latin-American Spanish locale instead (which does).
    "Argentina": "es_MX",
    "Chile": "es_CL",
    "Brazil": "pt_BR",
    "Cuba": "es_MX",
    "Venezuela": "es_MX",
    "Peru": "es_MX",
    "Bolivia": "es_MX",
    "Ecuador": "es_MX",
    "Honduras": "es_MX",
    # --- Sub-Saharan Africa -----------------------------------------------
    "Nigeria": "yo_NG",
    "Ghana": "tw_GH",
}


@lru_cache(maxsize=None)
def faker_for_locale(locale: str) -> Optional[Faker]:
    # One shared instance per locale is fine — name generation only draws the
    # RNG — and caching avoids rebuilding a provider set for every pilot. Only
    # accept the locale if it can produce the gendered names the pilot
    # generator needs; some shipped locales (e.g. es_AR) have no male/female
    # name provider. Returns None when unusable so the caller falls back.
    try:
        faker = Faker(locale)
        faker.name_male()
        faker.name_female()
    except Exception:  # noqa: BLE001 — any locale defect must just fall back
        return None
    return faker


@lru_cache(maxsize=None)
def faker_for_locales(locales: Optional[tuple[str, ...]]) -> Faker:
    """One shared Faker over a faction's locale list (the squadron fallback).

    Cached by the locale tuple so every squadron of a faction shares one
    instance; ``None`` / an empty tuple (a faction with no ``locales``) builds
    Faker's default. This is the one construction path for faction-locale
    fakers — the old per-``Coalition`` instance is gone.
    """
    return Faker(list(locales) if locales else None)


def faker_for_country(
    country: Optional[Country], fallback_locales: Optional[Sequence[str]]
) -> Faker:
    """Return a Faker whose locale matches ``country``.

    Unmapped countries, the multinational / irregular factions, and any locale
    not shipped (or not gender-aware) in the installed Faker all resolve to a
    faker built from ``fallback_locales`` (the faction's locale list), so a
    roster is always generated.
    """
    if country is not None:
        locale = COUNTRY_FAKER_LOCALES.get(country.name)
        if locale is not None:
            faker = faker_for_locale(locale)
            if faker is not None:
                return faker
    return faker_for_locales(
        tuple(fallback_locales) if fallback_locales is not None else None
    )
