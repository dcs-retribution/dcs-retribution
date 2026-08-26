from types import SimpleNamespace
from typing import Any, cast
from unittest.mock import MagicMock

from game.debriefing import (
    AirLosses,
    BaseCaptureEvent,
    Debriefing,
    GroundLosses,
    SideLossCounts,
    StateData,
)
from game.theater import ControlPoint, Player


def _items(n: int) -> list[Any]:
    """n placeholder loss objects. loss_counts only needs list length."""
    return [MagicMock() for _ in range(n)]


def _airlift(cargo_size: int) -> Any:
    """An airlift loss whose .cargo has the given length."""
    return SimpleNamespace(cargo=list(range(cargo_size)))


def _capture(captured_by: Player) -> BaseCaptureEvent:
    return BaseCaptureEvent(cast(ControlPoint, MagicMock()), captured_by)


def _sample_debriefing() -> Debriefing:
    """A Debriefing with known per-side losses, built without the heavy
    __init__ (which needs a Game and UnitMap). loss_counts and the loss
    properties only read air_losses, ground_losses, and base_captures."""
    air = AirLosses(player=_items(1), enemy=_items(2))
    ground = GroundLosses(
        player_front_line=_items(3),
        enemy_front_line=_items(1),
        player_motorpool=_items(2),
        enemy_motorpool=_items(3),
        player_convoy=_items(2),
        enemy_convoy=_items(0),
        player_cargo_ships=_items(1),
        enemy_cargo_ships=_items(4),
        player_airlifts=[_airlift(2)],
        enemy_airlifts=[_airlift(1), _airlift(3)],
        player_ground_objects=_items(5),
        enemy_ground_objects=_items(2),
        player_scenery=_items(0),
        enemy_scenery=_items(1),
        player_airfields=_items(1),
        enemy_airfields=_items(2),
    )
    captures = [
        _capture(Player.BLUE),
        _capture(Player.BLUE),
        _capture(Player.RED),
    ]
    debriefing = Debriefing.__new__(Debriefing)
    debriefing.air_losses = air
    debriefing.ground_losses = ground
    debriefing.base_captures = captures
    # loss_counts now also folds in survivor-based QRA losses; default to none.
    debriefing.state_data = cast(StateData, SimpleNamespace(intercept_survivors={}))
    debriefing.game = MagicMock()
    debriefing.game.blue.air_wing.iter_squadrons.return_value = []
    debriefing.game.red.air_wing.iter_squadrons.return_value = []
    return debriefing


def _qra_squadron(
    squadron_id: str, reserve: int, owned: int, aircraft: Any
) -> MagicMock:
    squadron = MagicMock()
    squadron.id = squadron_id
    squadron.intercept_reserve = reserve
    squadron.owned_aircraft = owned
    squadron.pilot_limits_enabled = False
    squadron.aircraft = aircraft
    return squadron


def test_qra_losses_folded_into_aircraft_counts() -> None:
    """QRA interceptors are Moose-spawned (not ATO flights), so their losses come
    from survivor counts, not air_losses. They must still show in the debrief."""
    debriefing = _sample_debriefing()  # ATO air losses: blue 1, red 2
    mig19 = MagicMock(name="MiG-19P")
    # Blue QRA squadron fielded 2, 0 survivors -> 2 lost. Red enrolled but all
    # survived -> 0 lost.
    blue_sq = _qra_squadron("blue-qra", reserve=2, owned=4, aircraft=mig19)
    red_sq = _qra_squadron("red-qra", reserve=2, owned=4, aircraft=MagicMock())
    debriefing.state_data = cast(
        StateData,
        SimpleNamespace(intercept_survivors={"blue-qra": 0, "red-qra": 2}),
    )
    game: Any = debriefing.game
    game.blue.air_wing.iter_squadrons.return_value = [blue_sq]
    game.red.air_wing.iter_squadrons.return_value = [red_sq]

    assert debriefing.qra_losses_by_type(Player.BLUE) == {mig19: 2}
    assert debriefing.qra_losses_by_type(Player.RED) == {}
    # ATO (1) + QRA (2) for blue; red unchanged (ATO 2 + QRA 0).
    assert debriefing.loss_counts(Player.BLUE).aircraft == 3
    assert debriefing.loss_counts(Player.RED).aircraft == 2
    assert debriefing.aircraft_losses_by_type(Player.BLUE)[mig19] == 2


def test_loss_counts_blue_side() -> None:
    blue = _sample_debriefing().loss_counts(Player.BLUE)
    assert blue == SideLossCounts(
        aircraft=1,
        front_line=3,
        motorpool=2,
        convoy=2,
        cargo_ships=1,
        airlift_cargo=2,
        ground_objects=5,
        scenery=0,
        bases_lost=1,  # one base captured by RED == one base Blue lost
        runways_destroyed=1,
    )


def test_loss_counts_red_side() -> None:
    red = _sample_debriefing().loss_counts(Player.RED)
    assert red == SideLossCounts(
        aircraft=2,
        front_line=1,
        motorpool=3,
        convoy=0,
        cargo_ships=4,
        airlift_cargo=4,  # 1 + 3
        ground_objects=2,
        scenery=1,
        bases_lost=2,  # two bases captured by BLUE == two bases Red lost
        runways_destroyed=2,
    )


def test_loss_counts_partition_matches_combined_totals() -> None:
    """Blue + Red for each category must equal the combined total the UI
    shows today (the existing Debriefing properties). Pins that loss_counts
    reads the same lists and never alters totals."""
    debriefing = _sample_debriefing()
    blue = debriefing.loss_counts(Player.BLUE)
    red = debriefing.loss_counts(Player.RED)

    assert blue.aircraft + red.aircraft == len(list(debriefing.air_losses.losses))
    assert blue.front_line + red.front_line == len(list(debriefing.front_line_losses))
    assert blue.motorpool + red.motorpool == len(list(debriefing.motorpool_losses))
    assert blue.convoy + red.convoy == len(list(debriefing.convoy_losses))
    assert blue.cargo_ships + red.cargo_ships == len(list(debriefing.cargo_ship_losses))
    assert blue.airlift_cargo + red.airlift_cargo == sum(
        len(loss.cargo) for loss in debriefing.airlift_losses
    )
    assert blue.ground_objects + red.ground_objects == len(
        list(debriefing.ground_object_losses)
    )
    assert blue.scenery + red.scenery == len(list(debriefing.scenery_object_losses))
    assert blue.bases_lost + red.bases_lost == len(debriefing.base_captures)
    assert blue.runways_destroyed + red.runways_destroyed == len(
        list(debriefing.damaged_runways)
    )


def test_motorpool_losses_by_type_counts_per_side() -> None:
    """motorpool_losses_by_type buckets a side's motorpool kills by unit type,
    mirroring front_line_losses_by_type. Feeds the debrief casualty screen."""
    t90 = MagicMock(name="T-90A")
    bmp = MagicMock(name="BMP-3")
    debriefing = _sample_debriefing()
    debriefing.ground_losses = GroundLosses(
        player_motorpool=[
            MagicMock(unit_type=t90),
            MagicMock(unit_type=t90),
            MagicMock(unit_type=bmp),
        ],
        enemy_motorpool=[MagicMock(unit_type=bmp)],
    )

    assert debriefing.motorpool_losses_by_type(Player.BLUE) == {t90: 2, bmp: 1}
    assert debriefing.motorpool_losses_by_type(Player.RED) == {bmp: 1}


def _minimal_unit_map() -> MagicMock:
    """A UnitMap mock where every unit lookup returns None (no aircraft/ground units)."""
    unit_map = MagicMock()
    unit_map.flight.return_value = None
    return unit_map


def test_state_data_parses_intercept_survivors() -> None:
    """StateData.from_json reads intercept_survivors from the JSON payload."""
    data = {
        "intercept_survivors": {
            "aaaaaaaa-0000-0000-0000-000000000001": 2,
            "aaaaaaaa-0000-0000-0000-000000000002": 0,
        }
    }
    state = StateData.from_json(data, _minimal_unit_map())
    assert state.intercept_survivors == {
        "aaaaaaaa-0000-0000-0000-000000000001": 2,
        "aaaaaaaa-0000-0000-0000-000000000002": 0,
    }


def test_state_data_intercept_survivors_defaults_to_empty() -> None:
    """StateData.from_json defaults intercept_survivors to {} when key absent."""
    state = StateData.from_json({}, _minimal_unit_map())
    assert state.intercept_survivors == {}


def test_state_data_intercept_survivors_tolerates_empty_lua_array() -> None:
    """An empty Lua table serializes to [] in JSON; from_json must not crash."""
    state = StateData.from_json({"intercept_survivors": []}, _minimal_unit_map())
    assert state.intercept_survivors == {}
