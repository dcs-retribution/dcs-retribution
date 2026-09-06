from game.ato.flightplans.sead import SEAD_ENGAGEMENT_RANGE, SeadFlightPlan
from game.ato.flightplans.uizonedisplay import UiZoneDisplay
from game.utils import nautical_miles


def test_sead_engagement_range_is_fixed_at_20nm() -> None:
    # Hard-coded HARM reach for the planner overlay, independent of the user-tunable
    # SEAD-sweep engagement range setting.
    assert SEAD_ENGAGEMENT_RANGE == nautical_miles(20)


def test_sead_flight_plan_displays_a_ui_zone() -> None:
    assert issubclass(SeadFlightPlan, UiZoneDisplay)
