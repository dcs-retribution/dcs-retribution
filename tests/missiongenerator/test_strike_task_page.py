from game.missiongenerator.kneeboard import StrikeTaskPage


def test_target_description_non_f15e_returns_display_name() -> None:
    assert StrikeTaskPage._target_description("SCUD1", 0, False) == "SCUD1"


def test_target_description_f15e_appends_dtc_slot() -> None:
    assert StrikeTaskPage._target_description("SCUD1", 0, True) == "SCUD1 (DTC M1.1)"


def test_target_description_f15e_reflects_rename() -> None:
    # The DTC reference is built from display_name, so a renamed target reads "SCUD1",
    # not the long auto pretty_name.
    assert StrikeTaskPage._target_description("SCUD1", 1, True) == "SCUD1 (DTC M1.2)"


def test_target_description_f15e_slot_matches_cdu_formula() -> None:
    # Slot math mirrors the CDU programming (M{i//8+1}.{i%8+1}): 8 minor slots per major
    # group, so index 8 is the first slot of group 2 -> M2.1 (NOT M2.9).
    assert StrikeTaskPage._target_description("Tgt", 8, True) == "Tgt (DTC M2.1)"


def test_target_description_f15e_minor_slot_advances_within_group() -> None:
    # Index 9 is the second slot of group 2 -> M2.2, matching the CDU.
    assert StrikeTaskPage._target_description("Tgt", 9, True) == "Tgt (DTC M2.2)"
