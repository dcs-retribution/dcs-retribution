import copy

from dcs import Point
from dcs.terrain import Caucasus

from game.ato.flightwaypoint import FlightWaypoint
from game.ato.flightwaypointtype import FlightWaypointType


def _wp(pretty_name: str = "[OBJ] : Scud #0") -> FlightWaypoint:
    wp = FlightWaypoint("auto-name", FlightWaypointType.CUSTOM, Point(0, 0, Caucasus()))
    wp.pretty_name = pretty_name
    return wp


def test_custom_name_defaults_to_none() -> None:
    assert _wp().custom_name is None


def test_display_name_falls_back_to_pretty_name() -> None:
    assert _wp("Pretty").display_name == "Pretty"


def test_display_name_prefers_custom_name() -> None:
    wp = _wp("Pretty")
    wp.custom_name = "SCUD1"
    assert wp.display_name == "SCUD1"


def test_apply_name_edit_sets_override_when_different() -> None:
    wp = _wp("Pretty")
    wp.apply_name_edit("SCUD1")
    assert wp.custom_name == "SCUD1"


def test_apply_name_edit_strips_padding() -> None:
    wp = _wp("Pretty")
    wp.apply_name_edit("SCUD1           ")  # cell text is "{:<16}".format(...)
    assert wp.custom_name == "SCUD1"


def test_apply_name_edit_back_to_auto_clears_override() -> None:
    wp = _wp("Pretty")
    wp.custom_name = "SCUD1"
    wp.apply_name_edit("Pretty")
    assert wp.custom_name is None


def test_apply_name_edit_blank_clears_override() -> None:
    wp = _wp("Pretty")
    wp.custom_name = "SCUD1"
    wp.apply_name_edit("   ")
    assert wp.custom_name is None


def test_apply_name_edit_no_phantom_override_when_pretty_name_padded() -> None:
    # Old saves carry pretty_name padded by the previous on_changed handler. Typing the
    # (unpadded) auto name must still read as "no override", not a phantom rename.
    wp = _wp("Hold            ")  # pre-existing padded pretty_name
    wp.apply_name_edit("Hold")
    assert wp.custom_name is None


def test_apply_name_edit_keeps_existing_override_on_padded_redraw() -> None:
    # on_changed re-applies apply_name_edit to every row whenever any cell changes,
    # feeding back the list cell's "{:<16}".format(display_name). For a row that already
    # has an override, that cell text is the padded custom_name, so re-applying it must be
    # idempotent and never clobber the override back to None.
    wp = _wp("Pretty")
    wp.custom_name = "SCUD1"
    wp.apply_name_edit("{:<16}".format(wp.display_name))
    assert wp.custom_name == "SCUD1"


def test_setstate_defaults_custom_name_for_old_saves() -> None:
    wp = _wp("Pretty")
    state = dict(wp.__dict__)
    del state["custom_name"]
    restored = FlightWaypoint.__new__(FlightWaypoint)
    restored.__setstate__(state)
    assert restored.custom_name is None


def test_deepcopy_preserves_custom_name() -> None:
    wp = _wp("Pretty")
    wp.custom_name = "SCUD1"
    assert copy.deepcopy(wp).custom_name == "SCUD1"
