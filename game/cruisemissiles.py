"""Ship-launched cruise missile strikes — planning, magazines, reconciliation.

DCS warships with land-attack cruise missiles (the Arleigh Burke's Tomahawks, the
CurrentHill asset packs' Kalibr hulls) can strike shore targets via a
``FireAtPoint`` task carrying the cruise-missile weapon flag — the mission-editor
"fire Tomahawks at a point" mechanism — but nothing in Retribution ever tasked
them. This module is the campaign side of that feature:

* **Eligibility** — :data:`LACM_SHIP_DCS_IDS`, a curated set of DCS ship types
  that actually carry land-attack cruise missiles (neither DCS nor pydcs exposes
  a per-ship weapon taxonomy to derive it from).
* **Magazines** — DCS silently rearms every mission, so without bookkeeping a
  campaign gets a free full salvo every turn. Each launching ship *group*
  carries a persisted magazine (``game.cruise_missile_magazines``, keyed by the
  group's stable ``TheaterGroup.group_name``), initialised from the hull table
  on first sight and decremented at the turn boundary from what the runtime
  plugin reports fired (:func:`reconcile_cruise_missiles`) — never at
  planning/generation time, so re-generating a mission can never double-debit.
  There is no rearm: the magazine is the campaign's missile stock.
* **Auto raids** — :func:`plan_cruise_raids` picks at most one raid per side per
  turn: the launching ship whose best reachable enemy ground object has the
  highest category priority (command/comms nodes first, then war-industry
  buildings, then anything strikeable). Pure function of game state —
  idempotent across mission regenerations.

The missiles themselves are real DCS weapons from a real, tracked ship TGO:
kills record natively at debrief (no phantom spawns), point defense gets to
intercept them, and sinking the shooter ends the raids. Symmetric — both
coalitions' capable ships participate.

Gated by ``cruise_missile_strikes`` (master: magazines + the plugin's F10
call-for-fire) and ``cruise_missile_auto_raids`` (the planner), both default
OFF.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Iterator, Optional

from game.utils import nautical_miles

if TYPE_CHECKING:
    from dcs.mapping import Point

    from game import Game
    from game.debriefing import Debriefing
    from game.theater.theatergroundobject import TheaterGroundObject
    from game.theater.theatergroup import TheaterGroup

#: DCS ship types that carry land-attack cruise missiles. Curated by hand because
#: neither DCS nor pydcs exposes a usable per-ship weapon taxonomy: the vanilla
#: Burke/Ticonderoga Tomahawk shooters plus the CurrentHill packs' explicit
#: land-attack (LACM/CMP) hull variants. The AShM-only sister hulls (CH_*_AShM)
#: are deliberately absent — anti-ship work belongs to the ANTISHIP task.
LACM_SHIP_DCS_IDS: frozenset[str] = frozenset(
    {
        "USS_Arleigh_Burke_IIa",
        "TICONDEROG",
        "CH_Arleigh_Burke_IIA",
        "CH_Arleigh_Burke_III",
        "CH_Ticonderoga",
        "CH_Ticonderoga_CMP",
        "CH_Grigorovich_LACM",
        "CH_Karakurt_LACM",
        "CH_Gremyashchiy_LACM",
    }
)

#: Campaign missile stock per hull (per *unit*, summed over a group's alive LACM
#: ships at first sight). Loosely the real land-attack fits: a Burke VLS carries
#: a deep TLAM load, the old Tico's armored box launchers eight, a Kalibr
#: corvette a single 8-cell UKSK. Balance numbers, not TO&E.
LACM_MAGAZINE_BY_TYPE: dict[str, int] = {
    "USS_Arleigh_Burke_IIa": 24,
    "TICONDEROG": 8,
    "CH_Arleigh_Burke_IIA": 24,
    "CH_Arleigh_Burke_III": 24,
    "CH_Ticonderoga": 8,
    "CH_Ticonderoga_CMP": 24,
    "CH_Grigorovich_LACM": 8,
    "CH_Karakurt_LACM": 8,
    "CH_Gremyashchiy_LACM": 8,
}
DEFAULT_MAGAZINE_PER_SHIP = 8

#: Auto-raid planning reach, ship → target. Conservative against DCS's modelled
#: Tomahawk flight (players can still call fire beyond it via the F10 menu,
#: whose range is a plugin option).
MAX_RAID_RANGE_M = nautical_miles(250).meters

#: Missiles per auto raid (capped by the ship group's remaining magazine).
RAID_SALVO = 6

#: What a cruise missile raid is *for*: fixed high-value infrastructure. Command
#: and comms nodes first, then production/storage, then any other strikeable
#: ground object. Lower sorts first.
_TARGET_CATEGORY_PRIORITY: dict[str, int] = {
    "commandcenter": 0,
    "comms": 1,
    "power": 2,
    "factory": 3,
    "oil": 4,
    "fuel": 5,
    "ware": 6,
    "ammo": 7,
}
_FALLBACK_PRIORITY = 8

#: Never raid these: ships are moving targets a FireAtPoint can't lead (and are
#: the ANTISHIP task's job).
_EXCLUDED_TARGET_CATEGORIES = frozenset({"ship"})


@dataclass(frozen=True)
class LacmShip:
    """One live launching group: a ship TGO group holding ≥1 alive LACM hull."""

    group_name: str
    coalition: str  # "blue" | "red" — the emitter/plugin side key
    position: "Point"
    remaining: int


@dataclass(frozen=True)
class CruiseRaid:
    """One planned auto raid: *missiles* cruise missiles from *group_name* onto
    the target's position. The plugin fires it after its startup delay."""

    group_name: str
    coalition: str
    target_name: str
    target_x: float
    target_y: float
    missiles: int


def magazines(game: "Game") -> dict[str, int]:
    """The persisted per-group missile stock (guarded for pre-feature saves)."""
    mags: Optional[dict[str, int]] = getattr(game, "cruise_missile_magazines", None)
    if mags is None:
        mags = {}
        game.cruise_missile_magazines = mags
    return mags


def ensure_magazines(game: "Game") -> None:
    """Lazily seed a magazine for any LACM ship group not yet tracked.

    Idempotent — an existing entry is never re-upped, so expenditure persists;
    capacity counts the group's *alive* LACM hulls at first sight.
    """
    mags = magazines(game)
    for _tgo, group in _lacm_groups(game):
        name = group.group_name
        if name in mags:
            continue
        mags[name] = _group_capacity(group)


def lacm_ships(game: "Game") -> list[LacmShip]:
    """Every live launching group with missiles left, both sides."""
    ensure_magazines(game)
    mags = magazines(game)
    ships: list[LacmShip] = []
    for tgo, group in _lacm_groups(game):
        remaining = mags.get(group.group_name, 0)
        if remaining <= 0:
            continue
        ships.append(
            LacmShip(
                group_name=group.group_name,
                coalition="blue" if tgo.control_point.captured.is_blue else "red",
                position=tgo.position,
                remaining=remaining,
            )
        )
    return ships


def plan_cruise_raids(game: "Game") -> list[CruiseRaid]:
    """At most one auto raid per side this turn (pure — safe to re-run per
    mission generation; the magazine only moves at the turn boundary)."""
    settings = game.settings
    if not getattr(settings, "cruise_missile_strikes", False):
        return []
    if not getattr(settings, "cruise_missile_auto_raids", False):
        return []
    raids = []
    for side in ("blue", "red"):
        raid = _plan_side_raid(game, side)
        if raid is not None:
            raids.append(raid)
    return raids


def reconcile_cruise_missiles(game: "Game", debriefing: "Debriefing") -> None:
    """Debit the magazines by what the plugin reported fired this mission.

    The report is the only debit site (regeneration-safe); an unreported group
    (mission never flown, plugin off) costs nothing, an unknown group name
    (stale save) is ignored.
    """
    reports = getattr(debriefing.state_data, "cruise_missiles_state", None)
    if not reports:
        return
    mags = magazines(game)
    for group_name, fired in reports:
        fired = int(fired)
        if fired <= 0:
            continue
        if group_name in mags:
            mags[group_name] = max(0, mags[group_name] - fired)


def player_briefing_info(game: "Game") -> tuple[list[LacmShip], list[CruiseRaid]]:
    """Blue-side launching ships + this turn's planned blue raid, for the
    mission briefing (like the rest of the briefing, written from the player
    coalition's perspective). Empty when the master setting is off, so the
    briefing section renders nothing. Ships list even with auto-raids off —
    the magazine matters to the F10 call-for-fire. Pure, like the planner.
    """
    if not getattr(game.settings, "cruise_missile_strikes", False):
        return [], []
    ships = [s for s in lacm_ships(game) if s.coalition == "blue"]
    if not ships:
        return [], []
    raids = [r for r in plan_cruise_raids(game) if r.coalition == "blue"]
    return ships, raids


def tgo_magazines(game: "Game", tgo: "TheaterGroundObject") -> list[tuple[str, int]]:
    """``(group_name, remaining)`` per launching group of *tgo*, for the ground
    object dialog. Empty when the setting is off or no group holds a live LACM
    hull. Seeds unseen groups first, like every other magazine read. The caller
    owns the friendly-side gate — enemy stock is not a click away by design.
    """
    if not getattr(game.settings, "cruise_missile_strikes", False):
        return []
    if getattr(tgo, "category", None) != "ship":
        return []
    ensure_magazines(game)
    mags = magazines(game)
    rows = []
    for group in getattr(tgo, "groups", []):
        name = getattr(group, "group_name", None)
        if not name:
            continue
        if any(_is_alive_lacm(u) for u in getattr(group, "units", [])):
            rows.append((name, mags.get(name, 0)))
    return rows


def debrief_expenditures(
    game: "Game", debriefing: "Debriefing"
) -> list[tuple[str, int, Optional[int]]]:
    """``(group_name, fired, remaining)`` rows for the debrief window.

    Every reported launch is listed (a launch is observable — the other side
    got a LAUNCH WARNING and met the missiles), but ``remaining`` is only
    filled in for the player's own groups; enemy residual stock stays hidden,
    like everywhere else. Runs after the turn-boundary debit, so ``remaining``
    is the post-mission magazine. A sunk blue shooter reports ``None`` too —
    its leftover stock went down with the ship.
    """
    reports = getattr(debriefing.state_data, "cruise_missiles_state", None)
    if not reports:
        return []
    blue_groups = {
        group.group_name
        for tgo, group in _lacm_groups(game)
        if tgo.control_point.captured.is_blue
    }
    mags = magazines(game)
    rows = []
    for group_name, fired in reports:
        fired = int(fired)
        if fired <= 0:
            continue
        remaining = mags.get(group_name) if group_name in blue_groups else None
        rows.append((group_name, fired, remaining))
    return rows


def _plan_side_raid(game: "Game", side: str) -> Optional[CruiseRaid]:
    ships = [s for s in lacm_ships(game) if s.coalition == side]
    if not ships:
        return None

    best: Optional[tuple[int, float, LacmShip, "TheaterGroundObject"]] = None
    for ship in ships:
        for tgo in _enemy_raid_targets(game, side):
            dist = ship.position.distance_to_point(tgo.position)
            if dist > MAX_RAID_RANGE_M:
                continue
            priority = _TARGET_CATEGORY_PRIORITY.get(
                getattr(tgo, "category", ""), _FALLBACK_PRIORITY
            )
            key = (priority, dist, ship, tgo)
            if best is None or key[:2] < best[:2]:
                best = key
    if best is None:
        return None

    _, _, ship, target = best
    return CruiseRaid(
        group_name=ship.group_name,
        coalition=side,
        target_name=target.name,
        target_x=target.position.x,
        target_y=target.position.y,
        missiles=min(RAID_SALVO, ship.remaining),
    )


def _enemy_raid_targets(game: "Game", side: str) -> Iterator["TheaterGroundObject"]:
    """Alive, raid-legal enemy ground objects for *side*'s raid this turn."""
    for cp in game.theater.controlpoints:
        owner = cp.captured
        enemy_of_side = owner.is_red if side == "blue" else owner.is_blue
        if not enemy_of_side:
            continue
        for tgo in cp.ground_objects:
            if getattr(tgo, "category", None) in _EXCLUDED_TARGET_CATEGORIES:
                continue
            if getattr(tgo, "is_control_point", False):
                continue
            if not any(unit.alive for unit in tgo.units):
                continue
            yield tgo


def _lacm_groups(
    game: "Game",
) -> Iterator[tuple["TheaterGroundObject", "TheaterGroup"]]:
    """Every ship TGO group holding at least one alive LACM hull, both sides."""
    for cp in game.theater.controlpoints:
        for tgo in cp.ground_objects:
            if getattr(tgo, "category", None) != "ship":
                continue
            for group in getattr(tgo, "groups", []):
                if not getattr(group, "group_name", None):
                    continue
                if any(_is_alive_lacm(u) for u in getattr(group, "units", [])):
                    yield tgo, group


def _group_capacity(group: "TheaterGroup") -> int:
    return sum(
        LACM_MAGAZINE_BY_TYPE.get(_dcs_id(u) or "", DEFAULT_MAGAZINE_PER_SHIP)
        for u in getattr(group, "units", [])
        if _is_alive_lacm(u)
    )


def _is_alive_lacm(unit: object) -> bool:
    return bool(getattr(unit, "alive", False)) and _dcs_id(unit) in LACM_SHIP_DCS_IDS


def _dcs_id(unit: object) -> Optional[str]:
    unit_type = getattr(unit, "type", None)
    return getattr(unit_type, "id", None)
