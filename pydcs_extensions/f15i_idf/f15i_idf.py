from dcs.planes import F_15ESE

from pydcs_extensions.pylon_injector import inject_pylon, eject_pylon
from pydcs_extensions.weapon_injector import inject_weapons


class WeaponsF15I:
    Python_4_ = {
        "clsid": "{5CE2FF2A-645A-4197-B48D-8720AC69394F}",
        "name": "Python-4 ",
        "weight": 103.6,
    }
    F_15I_Ra_am_Dome = {
        "clsid": "{IDF_MODS_PROJECT_F-15I_Raam_Dome}",
        "name": "F-15I Ra'am Dome",
        "weight": 0,
    }


inject_weapons(WeaponsF15I)


class F15IPylon1:
    Python_4_ = (1, WeaponsF15I.Python_4_)
    # ERRR {Python-4 Training}


class F15IPylon3:
    Python_4_ = (3, WeaponsF15I.Python_4_)
    # ERRR {Python-4 Training}


class F15IPylon13:
    Python_4_ = (13, WeaponsF15I.Python_4_)
    # ERRR {Python-4 Training}


class F15IPylon15:
    Python_4_ = (15, WeaponsF15I.Python_4_)
    # ERRR {Python-4 Training}


class Pylon16:
    F_15I_Ra_am_Dome = (16, WeaponsF15I.F_15I_Ra_am_Dome)


def inject_F15I() -> None:
    F_15ESE.pylons = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16}

    # Injects modified weapons from the IDF Mods Project F-16I Sufa
    # into pydcs databases via introspection.
    inject_pylon(F_15ESE.Pylon1, F15IPylon1)
    inject_pylon(F_15ESE.Pylon3, F15IPylon3)
    inject_pylon(F_15ESE.Pylon13, F15IPylon13)
    inject_pylon(F_15ESE.Pylon15, F15IPylon15)

    F_15ESE.Pylon16 = Pylon16


def eject_F15I() -> None:
    F_15ESE.pylons = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15}

    # Injects modified weapons from the IDF Mods Project F-16I Sufa
    # into pydcs databases via introspection.
    eject_pylon(F_15ESE.Pylon1, F15IPylon1)
    eject_pylon(F_15ESE.Pylon3, F15IPylon3)
    eject_pylon(F_15ESE.Pylon13, F15IPylon13)
    eject_pylon(F_15ESE.Pylon15, F15IPylon15)

    if hasattr(F_15ESE, "Pylon16"):
        delattr(F_15ESE, "Pylon16")
