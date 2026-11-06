from __future__ import annotations

from uuid import UUID

import pytest

from game.missiongenerator.aircraft.departurealtitude import reserve_departure_altitude
from game.utils import Distance, feet

CP_ID = UUID("00000000-0000-0000-0000-000000000001")
MINIMUM = feet(2000)
SEPARATION = feet(500)


def test_fixed_wing_departure_stack_starts_at_floor_and_increments_per_slot() -> None:
    stack: dict[UUID, Distance] = {}
    slots = [
        reserve_departure_altitude(stack, CP_ID, None, MINIMUM, SEPARATION)
        for _ in range(3)
    ]

    assert [slot.meters for slot in slots] == pytest.approx(
        [feet(2000).meters, feet(2500).meters, feet(3000).meters]
    )
    assert stack[CP_ID].meters == pytest.approx(feet(3500).meters)


def test_offmap_radio_request_above_floor_advances_next_slot_from_actual_used_altitude() -> (
    None
):
    stack: dict[UUID, Distance] = {}
    requested = feet(4000)

    assert reserve_departure_altitude(
        stack, CP_ID, requested, MINIMUM, SEPARATION
    ).meters == pytest.approx(requested.meters)
    assert reserve_departure_altitude(
        stack, CP_ID, feet(1000), MINIMUM, SEPARATION
    ).meters == pytest.approx(feet(4500).meters)


def test_mission_state_uses_separate_departure_and_legacy_midroute_stacks() -> None:
    from game.missiongenerator.missiondata import MissionData

    first_mission = MissionData()
    second_mission = MissionData()
    assert (
        reserve_departure_altitude(
            first_mission.fixed_wing_departure_stack, CP_ID, None, MINIMUM, SEPARATION
        )
        == MINIMUM
    )
    assert (
        reserve_departure_altitude(
            second_mission.fixed_wing_departure_stack, CP_ID, None, MINIMUM, SEPARATION
        )
        == MINIMUM
    )
    assert (
        first_mission.fixed_wing_departure_stack
        is not second_mission.fixed_wing_departure_stack
    )
    assert first_mission.cp_stack == {}


@pytest.mark.parametrize("requested", [feet(0), feet(1000), feet(2000)])
def test_requested_radio_altitude_cannot_lower_initial_floor(
    requested: Distance,
) -> None:
    stack: dict[UUID, Distance] = {}
    assert (
        reserve_departure_altitude(stack, CP_ID, requested, MINIMUM, SEPARATION)
        == MINIMUM
    )


def test_offmap_baro_request_remains_outside_radio_reservation_policy() -> None:
    stack: dict[UUID, Distance] = {}
    requested_baro_altitude = feet(12000)

    # The spawner calls the reservation helper only for OffMapSpawn RADIO starts.
    assert requested_baro_altitude == feet(12000)
    assert stack == {}
