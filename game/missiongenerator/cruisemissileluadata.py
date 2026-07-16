"""Ship cruise missile strikes -> Lua config bridge (``dcsRetribution.cruiseMissiles``).

Python owns the campaign side (eligibility, the persisted per-group magazines,
the auto-raid target pick — :mod:`game.cruisemissiles`); this lists, for the
``cruisemissiles`` plugin:

* ``ships`` — every live land-attack-capable ship group with missiles left
  (``group``/``coalition``/``remaining``), both sides. The plugin builds the F10
  call-for-fire menu from these and enforces ``remaining`` as this mission's
  hard expenditure cap per group (auto raid + player salvos share it).
* ``raids`` — this turn's planned auto raids (at most one per side), each a
  ``group``/``x``/``y``/``count``/``target``/``coalition`` record the plugin
  fires after its startup delay. ``x`` = north (``Point.x``) / ``y`` = east
  (``Point.y``) — the pydcs planning frame.

The plugin mirrors what actually fired into the ``cruise_missiles_state``
debrief channel; the turn boundary debits the magazines from that report, never
from this emit — so re-generating the mission is free.

Emits nothing unless ``cruise_missile_strikes`` is on and a live launching group
exists, so a normal mission carries no ``cruiseMissiles`` node and the plugin
no-ops.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game

    from .luagenerator import LuaData
    from .missiondata import MissionData


def populate_cruise_missiles_lua(
    root: "LuaData", game: "Game", mission_data: "MissionData"
) -> None:
    """Build the ``dcsRetribution.cruiseMissiles`` subtree (ships + auto raids)."""
    if not getattr(game.settings, "cruise_missile_strikes", False):
        return

    from game.cruisemissiles import lacm_ships, plan_cruise_raids

    ships = lacm_ships(game)
    if not ships:
        return
    raids = plan_cruise_raids(game)

    node = root.add_item("cruiseMissiles")
    ship_list = node.add_item("ships")
    for ship in ships:
        rec = ship_list.add_item()
        # The exact name Group.getByName needs (TheaterGroup.group_name, what the
        # generator stamps onto the .miz ship group).
        rec.add_key_value("group", ship.group_name)
        rec.add_key_value("coalition", ship.coalition)
        rec.add_key_value("remaining", str(ship.remaining))
    if raids:
        raid_list = node.add_item("raids")
        for raid in raids:
            rec = raid_list.add_item()
            rec.add_key_value("group", raid.group_name)
            rec.add_key_value("coalition", raid.coalition)
            rec.add_key_value("target", raid.target_name)
            rec.add_key_value("x", str(raid.target_x))
            rec.add_key_value("y", str(raid.target_y))
            rec.add_key_value("count", str(raid.missiles))
