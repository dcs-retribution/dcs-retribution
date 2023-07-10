from dcs.planes import F_15ESE

from pydcs_extensions.weapon_injector import inject_weapons


class WeaponsF15I:
    F_15I_Ra_am_Dome = {
        "clsid": "{IDF_MODS_PROJECT_F-15I_Raam_Dome}",
        "name": "F-15I Ra'am Dome",
        "weight": 0,
    }


inject_weapons(WeaponsF15I)


class Pylon16:
    F_15I_Ra_am_Dome = (16, WeaponsF15I.F_15I_Ra_am_Dome)


def inject_F15I() -> None:
    F_15ESE.pylons = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16}

    F_15ESE.Pylon16 = Pylon16


def eject_F15I() -> None:
    F_15ESE.pylons = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15}

    if hasattr(F_15ESE, "Pylon16"):
        delattr(F_15ESE, "Pylon16")
