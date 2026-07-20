"""Custom victory conditions: alternate, legible ends to the war.

The stock win condition is total conquest -- ``Game.check_win_loss`` returns
WIN only when the enemy owns zero control points -- which forces every
campaign, including a limited war ("liberate Abkhazia", a maritime pressure
campaign), into a full ground invasion. This module adds a shallow layer over
that default:

* **Authored tier:** a campaign YAML ``victory:`` block declaring ``win_when``
  / ``lose_when`` condition lists -- victory control points, domination
  thresholds, named high-value target destruction, category decapitation,
  strength attrition vs. the campaign-start baseline, and air denial. Parsed
  by :func:`parse_victory`, re-derived from the campaign YAML by name at load
  (never pickled; the lookup degrades to "no profile" on any failure, never a
  crash, so an old save whose campaign was removed still plays with the stock
  endings).

  .. code-block:: yaml

      victory:
        description: Liberate the coast
        win_when:
          - label: Take the coast
            capture_cps: [Sukhumi-Babushara, Gudauta]
          - enemy_air_below: 0.25
            min_turn: 4
        lose_when:
          - lose_cps: [Kutaisi]

* **Generic tier:** two opt-in Settings knobs usable on ANY campaign with
  zero authoring -- ``alternate_victory_domination`` and
  ``alternate_victory_attrition`` -- synthesized into the same condition
  objects and stacked with any authored block.

Semantics: a victory entry is a *requirement*, so EVERY field set on one
entry must hold (AND within the entry), and the ``win_when`` / ``lose_when``
lists are OR (any fully-met entry ends the war). That is what makes
``min_turn`` usable as a guard ("not before turn 4") instead of nonsense
("win at turn 4").

Alternate conditions ADD to the stock endings, never replace them: capturing
everything still wins and losing everything still loses. Evaluation is ground
truth at the turn boundary only, and the AI planner never reads these
conditions -- an author who wants the AI to pursue the objectives should
shape the campaign (or the OOB) so they align with what the commander already
values.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Literal, Optional

if TYPE_CHECKING:
    from game.game import Game
    from game.settings import Settings
    from game.theater.controlpoint import ControlPoint
    from game.theater.theatergroundobject import TheaterGroundObject

#: The generic attrition knob is capped here: "enemy air below 95% of start"
#: would end the war on the first kill, which is a losses counter, not a
#: victory condition.
MAX_ATTRITION_THRESHOLD = 90


@dataclass(frozen=True)
class VictoryCondition:
    """One ``win_when`` / ``lose_when`` entry.

    EVERY set field must hold for the entry to be met (AND semantics,
    documented in the module docstring). ``label`` is an optional authored
    display prefix; the Settings knobs synthesize unlabeled entries (their
    prose already says everything).
    """

    label: Optional[str] = None
    #: Guard: the entry cannot be met before this campaign turn.
    min_turn: int = 0
    #: ALL named control points are blue-owned.
    capture_cps: tuple[str, ...] = ()
    #: ANY named control point is red-owned (the ``lose_when`` staple).
    lose_cps: tuple[str, ...] = ()
    #: BLUE owns at least this fraction of the non-neutral control points.
    territory_above: Optional[float] = None
    #: BLUE owns less than this fraction of the non-neutral control points.
    territory_below: Optional[float] = None
    #: ALL ground objects with these names are fully dead (case-insensitive;
    #: a name matching nothing can never be met -- typos are visible, not
    #: silent wins).
    destroy_targets: tuple[str, ...] = ()
    #: NO red-owned ground object of these ``category`` strings has alive
    #: units, AND the campaign-start baseline counted at least one (so an
    #: absent category can never produce a vacuous instant win).
    destroy_categories: tuple[str, ...] = ()
    #: Red owned airframes (all squadrons) below this fraction of the baseline.
    enemy_air_below: Optional[float] = None
    #: Red front-line ground inventory below this fraction of the baseline.
    enemy_ground_below: Optional[float] = None
    #: Blue owned airframes below this fraction of the baseline (``lose_when``).
    friendly_air_below: Optional[float] = None
    #: NO red control point can currently field aircraft
    #: (``runway_is_operational``: cratered airfields and sunk carriers are
    #: denied; FOB helipads count as air power; a red off-map spawn is always
    #: operational, so this condition is unreachable on those campaigns -- by
    #: construction).
    enemy_air_denied: bool = False


@dataclass(frozen=True)
class VictoryProfile:
    """A campaign's alternate endings: any met entry ends the war."""

    description: Optional[str] = None
    win_when: tuple[VictoryCondition, ...] = ()
    lose_when: tuple[VictoryCondition, ...] = ()


@dataclass
class VictoryBaseline:
    """Campaign-start strength snapshot the ratio conditions run against.

    Latched on the game the first time :func:`ensure_victory_baseline` runs
    (turn 0 for a new game; first load for a pre-feature save). Snapshotted
    unconditionally so a knob flipped on at turn 20 still measures against
    the earliest state this build saw. ``red_categories`` counts red ground
    objects per ``category`` so ``destroy_categories`` can prove the target
    class ever existed.
    """

    red_air: int
    blue_air: int
    red_ground: int
    red_categories: dict[str, int] = field(default_factory=dict)


# --- live-state counters --------------------------------------------------------------


def _air_strength(game: Game, blue: bool) -> int:
    """Owned airframes across ALL of one side's squadrons.

    The whole force, not just the air-superiority slice -- the attrition ask
    is force strength, and a bomber wing is strength.
    """
    from game.theater.player import Player

    player = Player.BLUE if blue else Player.RED
    return sum(
        squadron.owned_aircraft
        for squadron in game.air_wing_for(player).iter_squadrons()
    )


def _ground_strength(game: Game, blue: bool) -> int:
    """One side's front-line ground inventory (the force plan_groundwar fields)."""
    from game.theater.player import Player

    player = Player.BLUE if blue else Player.RED
    return sum(
        cp.base.total_armor
        for cp in game.theater.controlpoints
        if cp.captured is player
    )


def _territory(game: Game) -> tuple[int, int]:
    """(blue-owned, total non-neutral) control points."""
    from game.theater.player import Player

    blue = 0
    total = 0
    for cp in game.theater.controlpoints:
        if cp.captured is Player.NEUTRAL:
            continue
        total += 1
        if cp.captured is Player.BLUE:
            blue += 1
    return blue, total


def _red_category_counts(game: Game) -> dict[str, int]:
    """Red-owned ground objects per ``category`` string (alive or dead)."""
    from game.theater.player import Player

    counts: dict[str, int] = {}
    for tgo in game.theater.ground_objects:
        if tgo.control_point.captured is Player.RED:
            counts[tgo.category] = counts.get(tgo.category, 0) + 1
    return counts


def _red_alive_in_category(game: Game, category: str) -> int:
    """Red-owned ground objects of ``category`` that still have alive units."""
    from game.theater.player import Player

    return sum(
        1
        for tgo in game.theater.ground_objects
        if tgo.control_point.captured is Player.RED
        and tgo.category == category
        and any(unit.alive for unit in tgo.units)
    )


def _tgos_named(game: Game, name: str) -> list[TheaterGroundObject]:
    """Every ground object matching ``name`` (case-insensitive, stripped)."""
    wanted = name.strip().casefold()
    return [
        tgo
        for tgo in game.theater.ground_objects
        if tgo.name.strip().casefold() == wanted
    ]


def _cp_named(game: Game, name: str) -> Optional[ControlPoint]:
    for cp in game.theater.controlpoints:
        if cp.name == name:
            return cp
    return None


def _operational_red_airbases(game: Game) -> int:
    """Red control points that can currently field aircraft."""
    from game.theater.player import Player

    return sum(
        1
        for cp in game.theater.controlpoints
        if cp.captured is Player.RED and cp.runway_is_operational()
    )


# --- the baseline latch ---------------------------------------------------------------


def ensure_victory_baseline(game: Game) -> VictoryBaseline:
    """Latch (or return) the campaign-start strength snapshot.

    Called from ``Game.initialize_turn`` so a new game latches at turn 0; the
    verdict also calls it defensively so a pre-feature save latches on first
    read. Cheap (three sums + a category walk) and unconditional, so a
    late-enabled knob still measures honestly.
    """
    baseline = getattr(game, "victory_baseline", None)
    if baseline is None:
        baseline = VictoryBaseline(
            red_air=_air_strength(game, blue=False),
            blue_air=_air_strength(game, blue=True),
            red_ground=_ground_strength(game, blue=False),
            red_categories=_red_category_counts(game),
        )
        game.victory_baseline = baseline
    return baseline


# --- evaluation -----------------------------------------------------------------------


def _ratio_below(current: int, base: int, threshold: float) -> bool:
    """A strength ratio vs. an empty baseline is unmeasurable, never met."""
    if base <= 0:
        return False
    return current / base < threshold


def condition_met(
    game: Game, condition: VictoryCondition, baseline: VictoryBaseline
) -> bool:
    """AND semantics: every field set on the entry must hold."""
    from game.theater.player import Player

    if game.turn < condition.min_turn:
        return False
    for name in condition.capture_cps:
        cp = _cp_named(game, name)
        if cp is None or not cp.captured.is_blue:
            return False
    if condition.lose_cps:
        if not any(
            (cp := _cp_named(game, name)) is not None and cp.captured is Player.RED
            for name in condition.lose_cps
        ):
            return False
    if condition.territory_above is not None:
        blue, total = _territory(game)
        if total == 0 or blue / total < condition.territory_above:
            return False
    if condition.territory_below is not None:
        blue, total = _territory(game)
        if total == 0 or blue / total >= condition.territory_below:
            return False
    for name in condition.destroy_targets:
        targets = _tgos_named(game, name)
        if not targets:
            return False
        for tgo in targets:
            if any(unit.alive for unit in tgo.units):
                return False
    for category in condition.destroy_categories:
        if baseline.red_categories.get(category, 0) <= 0:
            return False
        if _red_alive_in_category(game, category) > 0:
            return False
    if condition.enemy_air_below is not None and not _ratio_below(
        _air_strength(game, blue=False), baseline.red_air, condition.enemy_air_below
    ):
        return False
    if condition.enemy_ground_below is not None and not _ratio_below(
        _ground_strength(game, blue=False),
        baseline.red_ground,
        condition.enemy_ground_below,
    ):
        return False
    if condition.friendly_air_below is not None and not _ratio_below(
        _air_strength(game, blue=True), baseline.blue_air, condition.friendly_air_below
    ):
        return False
    if condition.enemy_air_denied and _operational_red_airbases(game) > 0:
        return False
    return True


# --- the knobs (generic tier) ---------------------------------------------------------


def _knob_conditions(settings: Settings) -> tuple[VictoryCondition, ...]:
    """The Settings-synthesized win conditions (0 = off, the default)."""
    out = []
    domination = int(getattr(settings, "alternate_victory_domination", 0) or 0)
    if 0 < domination <= 100:
        out.append(VictoryCondition(territory_above=domination / 100))
    attrition = int(getattr(settings, "alternate_victory_attrition", 0) or 0)
    if 0 < attrition <= MAX_ATTRITION_THRESHOLD:
        out.append(VictoryCondition(enemy_air_below=attrition / 100))
    return tuple(out)


# --- parsing + the campaign lookup (rederive-never-pickle) ----------------------------

_STRING_LIST_KEYS = ("capture_cps", "lose_cps", "destroy_targets", "destroy_categories")
_FRACTION_KEYS = (
    "territory_above",
    "territory_below",
    "enemy_air_below",
    "enemy_ground_below",
    "friendly_air_below",
)
_ALLOWED_ENTRY_KEYS = (
    frozenset(_STRING_LIST_KEYS)
    | frozenset(_FRACTION_KEYS)
    | {"label", "min_turn", "enemy_air_denied"}
)


def _parse_string_list(raw: object, key: str) -> tuple[str, ...]:
    if (
        not isinstance(raw, list)
        or not raw
        or not all(isinstance(item, str) and item.strip() for item in raw)
    ):
        raise ValueError(f"victory: {key} must be a non-empty list of names: {raw!r}")
    return tuple(str(item) for item in raw)


def _parse_fraction(raw: object, key: str) -> float:
    try:
        value = float(raw)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        raise ValueError(f"victory: {key} must be a number in (0, 1): {raw!r}")
    if not 0 < value <= 1 or (key != "territory_above" and value == 1):
        # territory_above: 1.0 ("own everything") is legal, if redundant with
        # the stock ending; a *_below threshold of 1.0 is trivially near-true.
        raise ValueError(f"victory: {key} must be a fraction in (0, 1): {raw!r}")
    return value


def _parse_entry(raw: object) -> VictoryCondition:
    """One ``win_when`` / ``lose_when`` entry. Fails loudly on bad data, so a
    broken campaign dies in tests rather than silently losing its ending."""
    if not isinstance(raw, dict):
        raise ValueError(f"victory: condition entry must be a mapping: {raw!r}")
    unknown = set(raw) - _ALLOWED_ENTRY_KEYS
    if unknown:
        raise ValueError(
            f"victory: unknown condition field(s) {sorted(unknown)} in {raw!r}"
        )

    def strings(key: str) -> tuple[str, ...]:
        return _parse_string_list(raw[key], key) if key in raw else ()

    def fraction(key: str) -> Optional[float]:
        if key not in raw or raw[key] is None:
            return None
        return _parse_fraction(raw[key], key)

    denied = raw.get("enemy_air_denied", False)
    if denied not in (False, True):
        raise ValueError(
            f"victory: enemy_air_denied must be true (omit it otherwise): {raw!r}"
        )
    condition = VictoryCondition(
        label=str(raw["label"]) if raw.get("label") else None,
        min_turn=int(raw.get("min_turn", 0)),
        capture_cps=strings("capture_cps"),
        lose_cps=strings("lose_cps"),
        territory_above=fraction("territory_above"),
        territory_below=fraction("territory_below"),
        destroy_targets=strings("destroy_targets"),
        destroy_categories=strings("destroy_categories"),
        enemy_air_below=fraction("enemy_air_below"),
        enemy_ground_below=fraction("enemy_ground_below"),
        friendly_air_below=fraction("friendly_air_below"),
        enemy_air_denied=bool(denied),
    )
    has_condition = bool(
        condition.capture_cps
        or condition.lose_cps
        or condition.territory_above is not None
        or condition.territory_below is not None
        or condition.destroy_targets
        or condition.destroy_categories
        or condition.enemy_air_below is not None
        or condition.enemy_ground_below is not None
        or condition.friendly_air_below is not None
        or condition.enemy_air_denied
    )
    if not has_condition:
        raise ValueError(
            f"victory: entry has no condition (label/min_turn alone do not "
            f"end a war): {raw!r}"
        )
    return condition


def parse_victory(raw: object) -> Optional[VictoryProfile]:
    """Parse a campaign YAML ``victory:`` block, or None when absent."""
    if not raw:
        return None
    if not isinstance(raw, dict):
        raise ValueError(f"victory: must be a mapping, got {type(raw).__name__}")
    unknown = set(raw) - {"description", "win_when", "lose_when"}
    if unknown:
        raise ValueError(f"victory: unknown key(s) {sorted(unknown)}")
    win_raw = raw.get("win_when") or []
    lose_raw = raw.get("lose_when") or []
    if not isinstance(win_raw, list) or not isinstance(lose_raw, list):
        raise ValueError("victory: win_when/lose_when must be lists of conditions")
    win = tuple(_parse_entry(entry) for entry in win_raw)
    lose = tuple(_parse_entry(entry) for entry in lose_raw)
    if not win and not lose:
        raise ValueError("victory: needs at least one win_when or lose_when entry")
    description = raw.get("description")
    return VictoryProfile(
        description=str(description) if description else None,
        win_when=win,
        lose_when=lose,
    )


#: Authored-profile cache keyed by campaign name. Definitions live in the
#: campaign YAML and are re-derived per process, never pickled; tests may
#: inject here.
_PROFILE_CACHE: dict[str, Optional[VictoryProfile]] = {}


def authored_victory_for(game: Game) -> Optional[VictoryProfile]:
    """The campaign's authored ``victory:`` block, or None.

    Any lookup/parse failure degrades to None with a log, never a crash -- an
    old save whose campaign was removed (or whose block was broken by an
    edit) still plays with the stock endings.
    """
    name = getattr(game, "campaign_name", None)
    if not name:
        return None
    if name in _PROFILE_CACHE:
        return _PROFILE_CACHE[name]
    profile: Optional[VictoryProfile] = None
    try:
        import yaml

        from game.campaignloader.campaign import Campaign

        for path in Campaign.iter_campaign_defs():
            try:
                with path.open(encoding="utf-8") as campaign_file:
                    data = yaml.safe_load(campaign_file)
            except Exception:  # noqa: BLE001 -- one bad yaml must not kill the scan
                continue
            if isinstance(data, dict) and data.get("name") == name:
                profile = parse_victory(data.get("victory"))
                if profile is not None:
                    logging.info(
                        "Loaded victory conditions for %r: %d win / %d lose",
                        name,
                        len(profile.win_when),
                        len(profile.lose_when),
                    )
                break
    except Exception:  # noqa: BLE001
        logging.exception("Victory conditions: lookup failed for %r", name)
        profile = None
    _PROFILE_CACHE[name] = profile
    return profile


def active_victory_profile(game: Game) -> Optional[VictoryProfile]:
    """The authored block + the knob-synthesized conditions, or None.

    The knobs are re-read every call (settings change mid-campaign); the
    authored block comes from the process cache.
    """
    authored = authored_victory_for(game)
    extra = _knob_conditions(game.settings)
    if authored is None and not extra:
        return None
    if authored is None:
        return VictoryProfile(win_when=extra)
    if not extra:
        return authored
    return VictoryProfile(
        description=authored.description,
        win_when=authored.win_when + extra,
        lose_when=authored.lose_when,
    )


# --- the verdict (the check_win_loss branch) ------------------------------------------


def _announce(game: Game, condition: VictoryCondition, defeat: bool) -> None:
    """Name the met condition beside the generic Victory!/Defeat! dialog.

    Latched per condition text: the UI flow calls ``check_win_loss`` several
    times around a turn boundary, and the message feed should carry the
    "why" once. The latch persists (harmless -- the war is over).
    """
    text = condition.label or describe_condition(
        game, condition, ensure_victory_baseline(game), live=False
    )
    announced: set[str] = getattr(game, "victory_announced", set())
    key = ("defeat" if defeat else "victory") + ":" + text
    if key in announced:
        return
    announced.add(key)
    game.victory_announced = announced
    if defeat:
        game.message("Defeat condition met", text)
    else:
        game.message("Victory condition met", text)


def victory_verdict(game: Game) -> Optional[Literal["win", "loss"]]:
    """The alternate ending, or None while the war goes on.

    Backs the alternate-endings branch in ``Game.check_win_loss`` ahead of
    the stock territory checks. Loss precedence: a simultaneous collapse is
    never a cheap win.
    """
    profile = active_victory_profile(game)
    if profile is None:
        return None
    baseline = ensure_victory_baseline(game)
    for condition in profile.lose_when:
        if condition_met(game, condition, baseline):
            _announce(game, condition, defeat=True)
            return "loss"
    for condition in profile.win_when:
        if condition_met(game, condition, baseline):
            _announce(game, condition, defeat=False)
            return "win"
    return None


# --- display --------------------------------------------------------------------------


def describe_condition(
    game: Game,
    condition: VictoryCondition,
    baseline: VictoryBaseline,
    live: bool = True,
) -> str:
    """One entry as prose, with live progress values when ``live``.

    ``live=False`` (static prose) feeds the end-of-war banner; the live
    variant ("Capture Sukhumi, Gudauta (1/2 held)") is the building block
    for any conditions display a UI wants to add.
    """
    from game.theater.player import Player

    bits = []
    if condition.capture_cps:
        names = ", ".join(condition.capture_cps)
        now = ""
        if live:
            held = sum(
                1
                for name in condition.capture_cps
                if (cp := _cp_named(game, name)) is not None and cp.captured.is_blue
            )
            now = f" ({held}/{len(condition.capture_cps)} held)"
        bits.append(f"Capture {names}{now}")
    if condition.lose_cps:
        names = ", ".join(condition.lose_cps)
        now = ""
        if live:
            fallen = sum(
                1
                for name in condition.lose_cps
                if (cp := _cp_named(game, name)) is not None
                and cp.captured is Player.RED
            )
            now = f" ({fallen}/{len(condition.lose_cps)} fallen)"
        plural = "s" if len(condition.lose_cps) == 1 else ""
        bits.append(f"{names} fall{plural} to the enemy{now}")
    if condition.territory_above is not None:
        now = ""
        if live:
            blue, total = _territory(game)
            if total:
                now = f" (now {blue / total:.0%})"
        bits.append(f"Hold {condition.territory_above:.0%} of the bases{now}")
    if condition.territory_below is not None:
        now = ""
        if live:
            blue, total = _territory(game)
            if total:
                now = f" (now {blue / total:.0%})"
        bits.append(
            f"Friendly holdings fall below {condition.territory_below:.0%}{now}"
        )
    if condition.destroy_targets:
        names = ", ".join(condition.destroy_targets)
        now = ""
        if live:
            dead = 0
            for name in condition.destroy_targets:
                targets = _tgos_named(game, name)
                if targets and not any(
                    unit.alive for tgo in targets for unit in tgo.units
                ):
                    dead += 1
            now = f" ({dead}/{len(condition.destroy_targets)} destroyed)"
        bits.append(f"Destroy {names}{now}")
    if condition.destroy_categories:
        names = ", ".join(condition.destroy_categories)
        now = ""
        if live:
            alive = sum(
                _red_alive_in_category(game, category)
                for category in condition.destroy_categories
            )
            now = f" ({alive} still standing)"
        bits.append(f"Destroy every enemy {names} site{now}")
    if condition.enemy_air_below is not None:
        now = ""
        if live and baseline.red_air:
            ratio = _air_strength(game, blue=False) / baseline.red_air
            now = f" (now {ratio:.0%})"
        bits.append(
            f"Enemy air force below {condition.enemy_air_below:.0%} of start{now}"
        )
    if condition.enemy_ground_below is not None:
        now = ""
        if live and baseline.red_ground:
            ratio = _ground_strength(game, blue=False) / baseline.red_ground
            now = f" (now {ratio:.0%})"
        bits.append(
            f"Enemy ground force below "
            f"{condition.enemy_ground_below:.0%} of start{now}"
        )
    if condition.friendly_air_below is not None:
        now = ""
        if live and baseline.blue_air:
            ratio = _air_strength(game, blue=True) / baseline.blue_air
            now = f" (now {ratio:.0%})"
        bits.append(
            f"Friendly air force falls below "
            f"{condition.friendly_air_below:.0%} of start{now}"
        )
    if condition.enemy_air_denied:
        now = ""
        if live:
            operating = _operational_red_airbases(game)
            plural = "" if operating == 1 else "s"
            now = f" ({operating} enemy base{plural} still operating)"
        bits.append(f"Deny the enemy air operations{now}")
    text = " and ".join(bits)
    if condition.min_turn > 1:
        text += f" (not before turn {condition.min_turn})"
    if condition.label:
        return f"{condition.label} — {text}"
    return text
