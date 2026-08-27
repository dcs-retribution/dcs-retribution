"""High Digit SAMs 2.1.0 dropped units that DCS had meanwhile gained natively.

Leaving a dead mod class declared is not harmless: a campaign saved earlier still names
it, nothing resolves the type, and the site comes back as the wrong vehicle instead of
the SAM battery it was. Both resolution paths must therefore land on the native unit —
``GroundUnitType.named`` for the display name stored in group data, and the save
unpickler for the pickled class itself — and they must agree with each other.
"""

from __future__ import annotations

import pytest
from dcs.unittype import VehicleType
from dcs.vehicles import AirDefence

from game.dcs.groundunittype import GroundUnitType
from game.persistency import MigrationUnpickler

_HDS = "pydcs_extensions.highdigitsams.highdigitsams"

# old display name, old class name, native DCS unit
RETIRED = [
    ("AAA SON-9 Fire Can", "AAA_SON_9_Fire_Can", AirDefence.SON_9),
    ("AAA 100mm KS-19", "AAA_100mm_KS_19", AirDefence.KS_19),
    (
        "SAM SA-10B S-300PS 54K6 CP",
        "SAM_SA_10B_S_300PS_54K6_CP",
        AirDefence.S_300PS_54K6_cp,
    ),
    (
        "SAM SA-10B S-300PS 30N6 TR",
        "SAM_SA_10B_S_300PS_30N6_TR",
        AirDefence.S_300PS_5H63C_30H6_tr,
    ),
    (
        "SAM SA-10B S-300PS 40B6M TR",
        "SAM_SA_10B_S_300PS_40B6M_TR",
        AirDefence.S_300PS_40B6M_tr,
    ),
    (
        "SAM SA-10B S-300PS 40B6MD SR",
        "SAM_SA_10B_S_300PS_40B6MD_SR",
        AirDefence.S_300PS_40B6MD_sr,
    ),
    (
        "SAM SA-10B S-300PS 64H6E SR",
        "SAM_SA_10B_S_300PS_64H6E_SR",
        AirDefence.S_300PS_64H6E_sr,
    ),
    (
        "SAM SA-10B S-300PS 5P85SE LN",
        "SAM_SA_10B_S_300PS_5P85SE_LN",
        AirDefence.S_300PS_5P85C_ln,
    ),
    (
        "SAM SA-10B S-300PS 5P85SU LN",
        "SAM_SA_10B_S_300PS_5P85SU_LN",
        AirDefence.S_300PS_5P85D_ln,
    ),
    (
        "SAM SA-10 (5V55RUD) S-300PS LN 5P85CE",
        "SAM_SA_10__5V55RUD__S_300PS_LN_5P85CE",
        AirDefence.S_300PS_5P85C_ln,
    ),
    (
        "SAM SA-10 (5V55RUD) S-300PS LN 5P85DE",
        "SAM_SA_10__5V55RUD__S_300PS_LN_5P85DE",
        AirDefence.S_300PS_5P85D_ln,
    ),
]


@pytest.mark.parametrize("display_name,_class_name,native", RETIRED)
def test_old_display_name_resolves_to_the_native_unit(
    display_name: str, _class_name: str, native: type[VehicleType]
) -> None:
    assert GroundUnitType.named(display_name).dcs_unit_type.id == native.id


@pytest.mark.parametrize("_display_name,class_name,native", RETIRED)
def test_old_pickled_class_resolves_to_the_native_unit(
    _display_name: str, class_name: str, native: type[VehicleType]
) -> None:
    unpickler = MigrationUnpickler.__new__(MigrationUnpickler)
    assert unpickler._handle_high_digit_sams(_HDS, class_name) is native


def test_the_retired_classes_are_gone() -> None:
    """A class left behind is what makes a stale save resolve to the wrong vehicle."""
    from pydcs_extensions.highdigitsams import highdigitsams

    still_there = [name for _, name, _ in RETIRED if hasattr(highdigitsams, name)]
    assert not still_there
