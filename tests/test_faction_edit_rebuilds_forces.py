"""Editing a faction mid-campaign has to rebuild the coalition's forces.

`ArmedForces` is built from the faction once, in `Coalition.__init__`, and every
`ForceGroup` freezes the unit list it could reach at that moment. So a faction edit that
does not trigger a rebuild is invisible to every buy menu until the next campaign.
"""

from __future__ import annotations

from typing import Any

import pytest

from game import persistency

from game.armedforces.armedforces import ArmedForces
from game.data.units import UnitClass
from game.dcs.groundunittype import GroundUnitType
from game.factions import FACTIONS


@pytest.fixture(autouse=True)
def _init_persistency(tmp_path_factory: pytest.TempPathFactory) -> None:
    # Layout/preset loading reads the DCS saved-game folder, only configured once the
    # app boots. An empty temp dir makes it fall back to the bundled resources.
    persistency.setup(
        str(tmp_path_factory.mktemp("saved_games")),
        prefer_liberation_payloads=False,
        port=0,
    )


def _ewr_options(faction: Any) -> set[str]:
    """What the generic Early-Warning Radar site would offer for this faction."""
    forces = ArmedForces(faction)
    offered: set[str] = set()
    for force_group in forces.forces:
        for layout in force_group.layouts:
            if layout.name != "Early-Warning Radar":
                continue
            for unit_group in layout.all_unit_groups:
                for unit_type in force_group.unit_types_for_group(unit_group):
                    offered.add(unit_type.display_name)
    return offered


def test_an_added_early_warning_radar_reaches_the_buy_menu() -> None:
    """The reported case: adding an EWR to a faction left the EWR site still offering
    the SAM search radars it had fallen back to."""
    faction = FACTIONS["Bluefor Modern"]
    before = _ewr_options(faction)
    assert before, "the EWR site should offer something"

    added = GroundUnitType.named("EWR 1L13")
    assert added.unit_class is UnitClass.EARLY_WARNING_RADAR
    if added in faction.air_defense_units:
        return  # already fielded; nothing this test can add

    faction.air_defense_units.add(added)
    faction.__dict__.pop("accessible_units", None)
    try:
        after = _ewr_options(faction)
        assert added.display_name in after, (
            "a rebuild must pick up the unit the faction gained; without one the buy "
            "menu keeps whatever the ForceGroup froze at campaign start"
        )
    finally:
        faction.air_defense_units.discard(added)
        faction.__dict__.pop("accessible_units", None)


def test_every_faction_edit_announces_itself() -> None:
    """The bug was a signal wired to preset groups alone, so adding a unit or an
    aircraft changed the faction silently and nothing rebuilt."""
    import inspect

    from qt_ui.windows.newgame.WizardPages import QFactionSelection

    source = inspect.getsource(QFactionSelection.QFactionUnits)
    for handler in ("_on_add_unit", "_on_add_ac", "_on_add_preset_group"):
        start = source.index(f"def {handler}(")
        body = source[start : source.index("\n    def ", start + 1)]
        assert "faction_changed.emit" in body, f"{handler} must announce the change"


def test_removing_a_unit_actually_removes_it() -> None:
    """The tick box promised a removal it never performed: it is only read by the New
    Game wizard's save path, so unticking one in a running campaign did nothing."""
    import inspect

    from qt_ui.windows.newgame.WizardPages import QFactionSelection

    source = inspect.getsource(QFactionSelection.QFactionUnits)
    assert "_on_remove_unit" in source, "the list needs a real remove, not a tick box"
    start = source.index("def _on_remove_unit(")
    body = source[start : source.index(chr(10) + "    def ", start + 1)]
    assert "units.remove(unit)" in body
    assert "faction_changed.emit" in body, "a removal must rebuild the forces too"


def test_a_unit_in_use_is_refused() -> None:
    """Removing a unit the map has deployed would leave the campaign holding materiel
    its own faction no longer admits."""
    import inspect

    from qt_ui.windows.newgame.WizardPages import QFactionSelection

    source = inspect.getsource(QFactionSelection.QFactionUnits)
    start = source.index("def _on_remove_unit(")
    body = source[start : source.index(chr(10) + "    def ", start + 1)]
    guard = body.index("self.in_use(unit)")
    assert guard < body.index("units.remove(unit)"), "check before removing"
    assert "return" in body[guard : body.index("units.remove(unit)")]


def test_the_dialog_rebuilds_on_that_signal() -> None:
    import inspect

    from qt_ui.windows import AirWingDialog

    source = inspect.getsource(AirWingDialog)
    assert source.count("faction_changed.connect") == 2, "both sides must be wired"
    assert "armed_forces = ArmedForces(f)" in source
