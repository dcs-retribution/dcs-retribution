# This should probably be much higher, but the AI doesn't rollover their budget
# and isn't smart enough to save to repair a critical runway anyway, so it has
# to be cheap enough to repair with a single turn's income.
RUNWAY_REPAIR_COST = 100

BUILDING_REPAIR_INCOME_MULTIPLIER = 4.0
BUILDING_REPAIR_AMMO_BONUS = 10.0
BUILDING_REPAIR_FACTORY_BONUS = 12.0

REWARDS = {
    "warehouse": 2,
    "ware": 2,
    "fuel": 2,
    "ammo": 2,
    "farp": 1,
    # TODO: Should generate no cash once they generate units.
    # https://github.com/dcs-liberation/dcs_liberation/issues/1036
    "factory": 2.5,
    "oil": 10,
    "derrick": 8,
    "village": 0.25,
    "allycamp": 0.5,
}
