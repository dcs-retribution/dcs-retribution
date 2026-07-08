"""Per-squadron DCS country resolution for mission generation.

DCS plays nation-specific voiceovers and comms based on the *country* a group
belongs to. Retribution historically collapsed every unit on a side onto a
single faction country, so a coalition (CJTF) faction flying squadrons drawn
from several nations all shared one nation's radio voice.

``CountryAssigner`` instead spawns each squadron's units under its own
``squadron.country`` -- a field presets set via YAML and auto-generated
squadrons inherit from the faction (``SquadronDefGenerator``). Because a DCS
country may belong to only one coalition in a ``.miz``, blue claims its squadron
countries first; any red squadron whose country was already claimed by blue
falls back to red's faction country. The one reservation is symmetric: each
side's *faction* country is its spawn fallback and stays exclusive to that side,
so a blue squadron that happens to share red's faction country falls back to
blue's faction country rather than registering the nation on both coalitions.

For non-CJTF factions this is a no-op: the squadron loader already restricts
squadrons to the faction country (``SquadronDefLoader.load``), so every resolved
country equals the faction country and the generated mission is unchanged.

See GitHub issue dcs-retribution/dcs-retribution#627.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from dcs.countries import country_dict
from dcs.country import Country

if TYPE_CHECKING:
    from game.game import Game
    from game.squadrons.squadron import Squadron


class CountryAssigner:
    """Resolves which DCS country each squadron's units spawn under."""

    def __init__(self, game: Game) -> None:
        # Canonical Country instances, one per id. The *same* instance must be
        # both registered on the coalition and passed when spawning groups:
        # pydcs attaches groups to the instance via ``country.add_aircraft_group``
        # and only serializes countries reachable from the coalition, so a
        # duplicate instance with the same id would drop its groups on save.
        self._instances: dict[int, Country] = {}

        blue_id = game.blue.faction.country.id
        red_id = game.red.faction.country.id
        self.primary_blue = self._instance(blue_id)
        if red_id == blue_id:
            # Mirror match: both factions share a country id. A single DCS
            # ``Country`` instance may live on only one coalition (and pydcs
            # attaches each spawned group to the exact instance it is registered
            # under), so red must get its *own* instance of the shared id rather
            # than the cached blue one -- otherwise the same object is added to
            # both coalitions, which DCS rejects as an unloadable .miz. Two
            # distinct instances of one id, one per side, is the pre-#627
            # behaviour DCS accepts.
            self.primary_red = country_dict[red_id]()
        else:
            self.primary_red = self._instance(red_id)

        # Side -> {squadron-country id: canonical Country to spawn under}.
        self._blue: dict[int, Country] = {self.primary_blue.id: self.primary_blue}
        self._red: dict[int, Country] = {self.primary_red.id: self.primary_red}

        for squadron in game.blue.air_wing.iter_squadrons():
            cid = squadron.country.id
            if cid == self.primary_red.id:
                # Red's faction country is red's spawn fallback and must stay
                # exclusively red. A blue squadron that happens to share that
                # nation falls back to blue's faction country instead of
                # registering the country on *both* coalitions -- which DCS
                # rejects as an illegal .miz. This is the mirror of the
                # red-squadron-vs-blue guard below; blue's own faction country is
                # already protected because red checks ``blue_claimed``.
                logging.debug(
                    "Country id %s is red's faction country; blue squadron units "
                    "fall back to %s",
                    cid,
                    self.primary_blue.name,
                )
                continue
            if cid in self._blue:
                continue
            if cid not in country_dict:
                # An unknown country id (a pydcs version drop or an uninstalled
                # mod) must never abort mission generation: skip it and let the
                # squadron fall back to blue's faction country in ``for_squadron``.
                logging.debug(
                    "Country id %s (blue squadron) is unknown to pydcs; units "
                    "fall back to %s",
                    cid,
                    self.primary_blue.name,
                )
                continue
            self._blue[cid] = self._instance(cid)

        blue_claimed = set(self._blue)
        for squadron in game.red.air_wing.iter_squadrons():
            cid = squadron.country.id
            if cid in self._red:
                continue
            if cid in blue_claimed:
                # A DCS country can live in only one coalition; blue already owns
                # this nation, so red spawns these units under its faction
                # country instead.
                logging.debug(
                    "Country id %s already used by blue; red squadron units fall "
                    "back to %s",
                    cid,
                    self.primary_red.name,
                )
                continue
            if cid not in country_dict:
                logging.debug(
                    "Country id %s (red squadron) is unknown to pydcs; units "
                    "fall back to %s",
                    cid,
                    self.primary_red.name,
                )
                continue
            self._red[cid] = self._instance(cid)

    def _instance(self, country_id: int) -> Country:
        inst = self._instances.get(country_id)
        if inst is None:
            inst = country_dict[country_id]()
            self._instances[country_id] = inst
        return inst

    @property
    def blue_countries(self) -> list[Country]:
        """Every canonical Country to register on the blue coalition."""
        return list(self._blue.values())

    @property
    def red_countries(self) -> list[Country]:
        """Every canonical Country to register on the red coalition."""
        return list(self._red.values())

    @property
    def belligerent_ids(self) -> set[int]:
        """Country ids belonging to either side (excluded from neutrals)."""
        return set(self._blue) | set(self._red)

    def for_squadron(self, squadron: Squadron) -> Country:
        """Canonical Country a squadron's units should spawn under."""
        cid = squadron.country.id
        if squadron.coalition.player.is_blue:
            resolved = self._blue.get(cid)
            if resolved is not None:
                return resolved
            fallback = self.primary_blue
        else:
            resolved = self._red.get(cid)
            if resolved is not None:
                return resolved
            fallback = self.primary_red
        # A squadron whose country was not registered on its side (a
        # cross-coalition collision, an unknown id, or a squadron added after
        # construction) spawns under its faction country. Log it like every
        # other skip in ``__init__`` so the fallback is never silent.
        logging.debug(
            "Squadron %s country id %s not registered on its side; units fall "
            "back to %s",
            squadron.name,
            cid,
            fallback.name,
        )
        return fallback
