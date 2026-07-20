import pytest

from game import persistency
from game.armedforces.forcegroup import ForceGroup


@pytest.fixture(autouse=True)
def _init_persistency(tmp_path_factory: pytest.TempPathFactory) -> None:
    # ForceGroup/layout preset loading reads from the DCS saved-game folder,
    # which is only configured once the app boots. Point it at an empty temp
    # dir so loading falls back to the bundled resources/ presets.
    persistency.setup(
        str(tmp_path_factory.mktemp("saved_games")),
        prefer_liberation_payloads=False,
        port=0,
    )


_DOG_EAR = 'MCC-SR Sborka "Dog Ear" SR'


def _unit_names(group: ForceGroup) -> set[str]:
    return {unit.variant_id for unit in group.units}


def test_soviet_style_shorad_presets_include_dog_ear() -> None:
    assert _DOG_EAR in _unit_names(ForceGroup.from_preset_group("SA-9 SHORAD"))
    assert _DOG_EAR in _unit_names(ForceGroup.from_preset_group("SA-15 SHORAD"))
    assert _DOG_EAR in _unit_names(ForceGroup.from_preset_group("SA-19 SHORAD"))


def test_non_soviet_shorad_presets_do_not_include_dog_ear() -> None:
    assert _DOG_EAR not in _unit_names(ForceGroup.from_preset_group("Roland"))


def test_sam_sites_do_not_include_dog_ear() -> None:
    # The Sborka is a regimental SHORAD acquisition radar, not part of SA-2/3/5
    # or S-300 site TO&E (and a mid-1980s anachronism at Vietnam-era SA-2 sites),
    # so the SAM-site layouts must not grow a Dog Ear point-defense slot.
    for preset in ("SA-2/S-75", "SA-3/S-125", "SA-5/S-200", "SA-10/S-300PS"):
        assert _DOG_EAR not in _unit_names(ForceGroup.from_preset_group(preset)), preset
