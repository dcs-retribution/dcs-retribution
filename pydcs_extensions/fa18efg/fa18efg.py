from dcs.planes import FA_18C_hornet

from pydcs_extensions.pylon_injector import inject_pylons
from pydcs_extensions.weapon_injector import inject_weapons
from qt_ui.uiconstants import AIRCRAFT_ICONS, AIRCRAFT_BANNERS


class WeaponsFA18EFG:
    AA42R_Buddy_Pod = {"clsid": "{AA42R}", "name": "AA42R Buddy Pod", "weight": 1520}
    ALQ_99Center = {"clsid": "{ALQ-99Center}", "name": "ALQ-99Center", "weight": 0}
    ALQ_99Wing = {"clsid": "{ALQ-99Wing}", "name": "ALQ-99Wing", "weight": 0}
    FPU_12_Fuel_Tank_480_gallons = {
        "clsid": "{FPU_12_FUEL_TANK}",
        "name": "FPU-12 Fuel Tank 480 gallons",
        "weight": 1550,
    }
    FPU_12_Fuel_Tank_480_gallons_High_Vis = {
        "clsid": "{FPU_12_FUEL_TANKHighVis}",
        "name": "FPU-12 Fuel Tank 480 gallons High Vis",
        "weight": 1550,
    }
    LAU_127L = {"clsid": "{LAU-127L}", "name": "LAU-127L", "weight": 30}
    LAU_127R = {"clsid": "{LAU-127R}", "name": "LAU-127R", "weight": 30}
    USAFlag = {"clsid": "{USAFlag}", "name": "USAFlag", "weight": 0}


class FA18EFGPylon2:
    FPU_12_Fuel_Tank_480_gallons = (2, WeaponsFA18EFG.FPU_12_Fuel_Tank_480_gallons)
    FPU_12_Fuel_Tank_480_gallons_High_Vis = (
        2,
        WeaponsFA18EFG.FPU_12_Fuel_Tank_480_gallons_High_Vis,
    )


class FA18EFGPylon3:
    FPU_12_Fuel_Tank_480_gallons = (3, WeaponsFA18EFG.FPU_12_Fuel_Tank_480_gallons)
    FPU_12_Fuel_Tank_480_gallons_High_Vis = (
        3,
        WeaponsFA18EFG.FPU_12_Fuel_Tank_480_gallons_High_Vis,
    )


class FA18EFGPylon5:
    FPU_12_Fuel_Tank_480_gallons = (5, WeaponsFA18EFG.FPU_12_Fuel_Tank_480_gallons)
    FPU_12_Fuel_Tank_480_gallons_High_Vis = (
        5,
        WeaponsFA18EFG.FPU_12_Fuel_Tank_480_gallons_High_Vis,
    )
    AA42R_Buddy_Pod = (5, WeaponsFA18EFG.AA42R_Buddy_Pod)
    ALQ_99Center = (5, WeaponsFA18EFG.ALQ_99Center)


class FA18EFGPylon7:
    FPU_12_Fuel_Tank_480_gallons = (7, WeaponsFA18EFG.FPU_12_Fuel_Tank_480_gallons)
    FPU_12_Fuel_Tank_480_gallons_High_Vis = (
        7,
        WeaponsFA18EFG.FPU_12_Fuel_Tank_480_gallons_High_Vis,
    )


class FA18EFGPylon8:
    FPU_12_Fuel_Tank_480_gallons = (8, WeaponsFA18EFG.FPU_12_Fuel_Tank_480_gallons)
    FPU_12_Fuel_Tank_480_gallons_High_Vis = (
        8,
        WeaponsFA18EFG.FPU_12_Fuel_Tank_480_gallons_High_Vis,
    )


class FA18EFGPylon10:
    USAFlag = (10, WeaponsFA18EFG.USAFlag)
    LAU_127R = (10, WeaponsFA18EFG.LAU_127R)
    LAU_127L = (10, WeaponsFA18EFG.LAU_127L)
    ALQ_99Wing = (10, WeaponsFA18EFG.ALQ_99Wing)


inject_weapons(WeaponsFA18EFG)


def inject_FA18EFG() -> None:
    # Injects modified wingspan and custom weapons from the CJS SuperBug mod
    # into pydcs databases via introspection.
    AIRCRAFT_ICONS["FA-18C_hornet"] = AIRCRAFT_ICONS["FA-18EFG"]
    AIRCRAFT_BANNERS["FA-18C_hornet"] = AIRCRAFT_BANNERS["FA-18EFG"]
    setattr(FA_18C_hornet, "width", 13.62456)
    inject_pylons(FA_18C_hornet.Pylon2, FA18EFGPylon2)
    inject_pylons(FA_18C_hornet.Pylon3, FA18EFGPylon3)
    inject_pylons(FA_18C_hornet.Pylon5, FA18EFGPylon5)
    inject_pylons(FA_18C_hornet.Pylon7, FA18EFGPylon7)
    inject_pylons(FA_18C_hornet.Pylon8, FA18EFGPylon8)
    inject_pylons(FA_18C_hornet.Pylon10, FA18EFGPylon10)
