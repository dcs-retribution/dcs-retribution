from __future__ import annotations

from typing import cast

from game.ato.flighttype import FlightType
from game.dcs.aircrafttype import AircraftType
from game.squadrons.airwing import AirWing
from game.squadrons.squadron import Squadron


class _FakeSquadron:
    def __init__(self, reserve: int, max_size: int, barcap: bool) -> None:
        self.intercept_reserve = reserve
        self.max_size = max_size
        self._barcap = barcap
        # Attributes read by the real Squadron.set_intercept_reserve, which
        # repropagate_qra_reserve now routes through.
        self.owned_aircraft = max_size
        self.untasked_aircraft = max(0, max_size - reserve)

    def capable_of(self, task: FlightType) -> bool:
        return self._barcap

    def set_intercept_reserve(self, value: int) -> None:
        # Exercise the real model logic (delta-adjust untasked + set reserve).
        Squadron.set_intercept_reserve(cast(Squadron, self), value)


def _airwing(squadrons: list[_FakeSquadron]) -> AirWing:
    wing = AirWing.__new__(AirWing)
    wing.squadrons = cast("dict[AircraftType, list[Squadron]]", {0: list(squadrons)})
    return wing


def test_repropagate_bumps_only_tracking_barcap_squadrons() -> None:
    tracking = _FakeSquadron(reserve=0, max_size=12, barcap=True)
    user_set = _FakeSquadron(reserve=2, max_size=12, barcap=True)
    non_barcap = _FakeSquadron(reserve=0, max_size=12, barcap=False)
    wing = _airwing([tracking, user_set, non_barcap])

    wing.repropagate_qra_reserve(0, 4)

    assert tracking.intercept_reserve == 4
    assert user_set.intercept_reserve == 2
    assert non_barcap.intercept_reserve == 0


def test_repropagate_is_a_no_op_when_default_unchanged() -> None:
    squadron = _FakeSquadron(reserve=0, max_size=12, barcap=True)
    wing = _airwing([squadron])

    wing.repropagate_qra_reserve(0, 0)

    assert squadron.intercept_reserve == 0
