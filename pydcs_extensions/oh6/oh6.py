from typing import Dict, List, Set, Any

from dcs import task
from dcs.helicopters import HelicopterType
from dcs.unitpropertydescription import UnitPropertyDescription

from game.modsupport import helicoptermod
from pydcs_extensions.weapon_injector import inject_weapons


class WeaponsOH6:
    Cameraman = {"clsid": "{OH-6_CAMMAN}", "name": "Cameraman", "weight": 70}
    Camrig = {"clsid": "{OH-6_CAMRIG}", "name": "Camrig", "weight": 70}
    Floaters = {"clsid": "{OH-6_FLOATERS}", "name": "Floaters", "weight": 50}
    Frag_Grenade = {"clsid": "{OH6_FRAG}", "name": "Frag Grenade", "weight": 0}
    M134_Door_Minigun = {
        "clsid": "{OH-6_M134_Door}",
        "name": "M134 Door Minigun",
        "weight": 110,
    }
    M134_Minigun = {
        "clsid": "{OH-6_M134_Minigun}",
        "name": "M134 Minigun",
        "weight": 39,
    }
    M60_Doorgun = {"clsid": "{OH-6_M60_Door}", "name": "M60 Doorgun", "weight": 110}
    Searchlight = {"clsid": "{OH-6_Searchlight}", "name": "Searchlight", "weight": 70}
    SMOKE_Grenade_Blue = {
        "clsid": "{OH6_SMOKE_BLUE}",
        "name": "SMOKE Grenade Blue",
        "weight": 0,
    }
    SMOKE_Grenade_Green = {
        "clsid": "{OH6_SMOKE_GREEN}",
        "name": "SMOKE Grenade Green",
        "weight": 0,
    }
    SMOKE_Grenade_RED = {
        "clsid": "{OH6_SMOKE_RED}",
        "name": "SMOKE Grenade RED",
        "weight": 0,
    }
    SMOKE_Grenade_yellow = {
        "clsid": "{OH6_SMOKE_YELLOW}",
        "name": "SMOKE Grenade yellow",
        "weight": 0,
    }
    XM158_Weapon_System__4_ = {
        "clsid": "{OH6_XM158_4}",
        "name": "XM158 Weapon System (4)",
        "weight": 76.8,
    }
    XM158_Weapon_System__7_ = {
        "clsid": "{OH6_XM158}",
        "name": "XM158 Weapon System (7)",
        "weight": 99.9,
    }


inject_weapons(WeaponsOH6)


@helicoptermod
class OH_6A(HelicopterType):
    id = "OH-6A"
    flyable = True
    height = 3
    width = 8.33
    length = 10
    fuel_max = 181
    max_speed = 217
    chaff = 0
    flare = 30
    charge_total = 30
    chaff_charge_size = 1
    flare_charge_size = 1
    category = "Air"  # Helicopter
    radio_frequency = 262

    panel_radio = {
        1: {
            "channels": {
                1: 264,
                2: 265,
                4: 254,
                8: 258,
                16: 267,
                17: 251,
                9: 262,
                18: 253,
                5: 250,
                10: 259,
                20: 252,
                11: 268,
                3: 256,
                6: 270,
                12: 269,
                13: 260,
                7: 257,
                14: 263,
                19: 266,
                15: 261,
            },
        },
    }

    callnames: Dict[str, List[str]] = {
        "Assault",
        "Banshee",
        "Condor",
        "Gunner",
        "Eagle",
        "Griffin",
        "Little Griffin",
        "Deadbone",
        "Brandy",
        "Thunder",
        "Roadrunner",
        "Woodstock",
        "Scalphunter",
        "Darkhorse",
        "War Wagon",
    }

    property_defaults: Dict[str, Any] = {
        "CableCutterEnables": False,
        "FlaresEquipped": False,
        "RWREquipped": False,
    }

    class Properties:

        class CableCutterEnables:
            id = "CableCutterEnables"

        class FlaresEquipped:
            id = "FlaresEquipped"

        class RWREquipped:
            id = "RWREquipped"

    properties = {
        "CableCutterEnables": UnitPropertyDescription(
            identifier="CableCutterEnables",
            control="checkbox",
            label="Cable Cutter",
            default=False,
            weight_when_on=0,
        ),
        "FlaresEquipped": UnitPropertyDescription(
            identifier="FlaresEquipped",
            control="checkbox",
            label="Equip Flares",
            default=False,
            weight_when_on=10,
        ),
        "RWREquipped": UnitPropertyDescription(
            identifier="RWREquipped",
            control="checkbox",
            label="Equip RWR",
            default=False,
            weight_when_on=10,
        ),
    }

    livery_name = "OH-6A"  # from type

    class Pylon1:
        SMOKE_Grenade_RED = (1, WeaponsOH6.SMOKE_Grenade_RED)
        SMOKE_Grenade_Green = (1, WeaponsOH6.SMOKE_Grenade_Green)
        SMOKE_Grenade_Blue = (1, WeaponsOH6.SMOKE_Grenade_Blue)
        SMOKE_Grenade_yellow = (1, WeaponsOH6.SMOKE_Grenade_yellow)

    class Pylon2:
        SMOKE_Grenade_RED = (2, WeaponsOH6.SMOKE_Grenade_RED)
        SMOKE_Grenade_Green = (2, WeaponsOH6.SMOKE_Grenade_Green)
        SMOKE_Grenade_Blue = (2, WeaponsOH6.SMOKE_Grenade_Blue)
        SMOKE_Grenade_yellow = (2, WeaponsOH6.SMOKE_Grenade_yellow)

    class Pylon3:
        SMOKE_Grenade_RED = (3, WeaponsOH6.SMOKE_Grenade_RED)
        SMOKE_Grenade_Green = (3, WeaponsOH6.SMOKE_Grenade_Green)
        SMOKE_Grenade_Blue = (3, WeaponsOH6.SMOKE_Grenade_Blue)
        SMOKE_Grenade_yellow = (3, WeaponsOH6.SMOKE_Grenade_yellow)

    class Pylon4:
        SMOKE_Grenade_RED = (4, WeaponsOH6.SMOKE_Grenade_RED)
        SMOKE_Grenade_Green = (4, WeaponsOH6.SMOKE_Grenade_Green)
        SMOKE_Grenade_Blue = (4, WeaponsOH6.SMOKE_Grenade_Blue)
        SMOKE_Grenade_yellow = (4, WeaponsOH6.SMOKE_Grenade_yellow)

    class Pylon5:
        Frag_Grenade = (5, WeaponsOH6.Frag_Grenade)

    # ERRR <CLEAN>
    # ERRR <CLEAN>

    class Pylon8:
        M134_Minigun = (8, WeaponsOH6.M134_Minigun)

    class Pylon9:
        XM158_Weapon_System__7_ = (9, WeaponsOH6.XM158_Weapon_System__7_)
        XM158_Weapon_System__4_ = (9, WeaponsOH6.XM158_Weapon_System__4_)

    class Pylon10:
        XM158_Weapon_System__7_ = (10, WeaponsOH6.XM158_Weapon_System__7_)
        XM158_Weapon_System__4_ = (10, WeaponsOH6.XM158_Weapon_System__4_)

    class Pylon11:
        M60_Doorgun = (11, WeaponsOH6.M60_Doorgun)
        M134_Door_Minigun = (11, WeaponsOH6.M134_Door_Minigun)

    class Pylon12:
        Camrig = (12, WeaponsOH6.Camrig)
        Cameraman = (12, WeaponsOH6.Cameraman)
        Searchlight = (12, WeaponsOH6.Searchlight)
        Floaters = (12, WeaponsOH6.Floaters)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}

    tasks = [task.Transport, task.Reconnaissance]
    task_default = task.Reconnaissance
