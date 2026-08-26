from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, Mapping

from game.squadrons.intercept_reserve import qra_resource_count

if TYPE_CHECKING:
    from game.squadrons.squadron import Squadron


def fielded_qra_by_squadron(
    squadrons: Iterable["Squadron"],
) -> tuple[dict[str, int], dict[str, "Squadron"]]:
    """QRA airframes actually fielded on alert, keyed by stringified squadron id.

    The "fielded" baseline is the reserve capped by owned airframes and untasked
    pilots — what the dispatcher was seeded with and what the Lua bounds survivors
    by. Squadrons with no reserve, or that can field nothing (no airframes/pilots),
    are omitted. Returns the fielded counts plus an id -> squadron lookup.

    Single source of truth so the debrief loss report (``qra_losses_by_type``) and
    the inventory debit (``commit_intercept_losses``) compute the same baseline; if
    they drifted, the reported totals and the committed losses would diverge.
    """
    fielded_by_squadron: dict[str, int] = {}
    squadrons_by_id: dict[str, "Squadron"] = {}
    for squadron in squadrons:
        if squadron.intercept_reserve <= 0:
            continue
        available_pilots = (
            squadron.number_of_available_pilots
            if squadron.pilot_limits_enabled
            else None
        )
        fielded = qra_resource_count(
            squadron.intercept_reserve, squadron.owned_aircraft, available_pilots
        )
        if fielded <= 0:
            continue
        fielded_by_squadron[str(squadron.id)] = fielded
        squadrons_by_id[str(squadron.id)] = squadron
    return fielded_by_squadron, squadrons_by_id


def reconcile_intercept_losses(
    fielded_by_squadron: Mapping[str, int],
    survivors_by_squadron: Mapping[str, int],
) -> dict[str, int]:
    """QRA losses per squadron = fielded airframes − survivors reported by Lua.

    ``fielded_by_squadron`` is the count actually put on alert (the reserve capped
    by owned airframes and untasked pilots), which is what the dispatcher was
    seeded with and what the Lua bounds survivors by. The survivor map is the
    authoritative record of which squadrons actually flew QRA: a squadron *absent*
    from the map never participated (carrier/FOB, no detection sources, plugin
    disabled, or no parking) and takes no loss. A squadron *present* with zero
    survivors is a genuine total loss. Survivor counts are clamped to the fielded
    count so a stale over-count cannot credit phantom airframes. Squadrons present
    only in the survivor map are ignored.
    """
    losses: dict[str, int] = {}
    for squadron_id, fielded in fielded_by_squadron.items():
        if squadron_id not in survivors_by_squadron:
            continue
        survivors = max(0, min(survivors_by_squadron[squadron_id], fielded))
        losses[squadron_id] = fielded - survivors
    return losses
