from typing import Set

from dcs import task
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons
from dcs import unittype

from game.modsupport import vehiclemod, shipmod, planemod
from pydcs_extensions.weapon_injector import inject_weapons


class SWWeapons:
    PROTONB = {
        "clsid": "{PROTONB}",
        "name": "PROTONB",
        "weight": 50,
    }
    PROTONBGG = {
        "clsid": "{PROTONBGG}",
        "name": "PROTONBGG",
        "weight": 1000,
    }
    PROTONF = {
        "clsid": "{PROTONF}",
        "name": "PROTONF",
        "weight": 50,
    }
    PROTONM = {
        "clsid": "{PROTONM}",
        "name": "PROTONM",
        "weight": 50,
    }
    PROTONM1 = {
        "clsid": "{PROTONM1}",
        "name": "PROTONM1",
        "weight": 50,
    }
    PROTONM2 = {
        "clsid": "{PROTONM2}",
        "name": "PROTONM2",
        "weight": 50,
    }
    PROTONM3 = {
        "clsid": "{PROTONM3}",
        "name": "PROTONM3",
        "weight": 0.1,
    }
    PROTONMissile = {
        "clsid": "{PROTONMissile}",
        "name": "PROTONMissile",
        "weight": 50,
    }
    ENERGY_CELL = {
        "clsid": "{AFUEL}",
        "name": "ENERGY CELL",
        "weight": 1005,
    }
    ENERGY_CELL_ = {
        "clsid": "{TIEFUEL}",
        "name": "ENERGY CELL",
        "weight": 1005,
    }
    ENERGY_CELL__ = {
        "clsid": "{HUNTFUEL}",
        "name": "ENERGY CELL",
        "weight": 1005,
    }
    ENERGY_CELL___ = {
        "clsid": "{TIRFUEL}",
        "name": "ENERGY CELL",
        "weight": 1005,
    }
    ENERGY_CELL____ = {
        "clsid": "{XFUELTANK}",
        "name": "ENERGY CELL",
        "weight": 2005,
    }
    Lite_Jump_Core_Battery = {
        "clsid": "{FHYPERCORE}",
        "name": "Lite Jump Core Battery",
        "weight": 50000,
    }


inject_weapons(SWWeapons)


@planemod
class XWING(PlaneType):
    id = "XWING"
    flyable = True
    height = 5.63
    width = 6
    length = 19.43
    fuel_max = 5000
    max_speed = 1152.396
    chaff = 5000
    flare = 5000
    charge_total = 10000
    chaff_charge_size = 1
    flare_charge_size = 1
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    livery_name = "XWING"  # from type

    class Pylon1:
        PROTONM = (1, SWWeapons.PROTONM)

    class Pylon2:
        PROTONM = (2, SWWeapons.PROTONM)
        ENERGY_CELL____ = (2, SWWeapons.ENERGY_CELL____)

    class Pylon3:
        PROTONM = (3, SWWeapons.PROTONM)

    class Pylon4:
        PROTONM = (4, SWWeapons.PROTONM)

    class Pylon5:
        PROTONM = (5, SWWeapons.PROTONM)

    class Pylon6:
        PROTONM = (6, SWWeapons.PROTONM)

    class Pylon10:
        ENERGY_CELL____ = (10, SWWeapons.ENERGY_CELL____)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 10}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.Reconnaissance,
    ]
    task_default = task.CAP


@planemod
class YWING(PlaneType):
    id = "YWING"
    flyable = True
    height = 5.63
    width = 10
    length = 19.43
    fuel_max = 7000
    max_speed = 2649.996
    chaff = 5000
    flare = 5000
    charge_total = 10000
    chaff_charge_size = 1
    flare_charge_size = 1
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    livery_name = "YWING"  # from type

    class Pylon1:
        PROTONB = (1, SWWeapons.PROTONB)
        Mk_84___2000lb_GP_Bomb_LD = (1, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            1,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        Kh_58U__AS_11_Kilter____640kg__ARM__IN__Pas_Rdr = (
            1,
            Weapons.Kh_58U__AS_11_Kilter____640kg__ARM__IN__Pas_Rdr,
        )

    class Pylon2:
        PROTONB = (2, SWWeapons.PROTONB)
        Mk_84___2000lb_GP_Bomb_LD = (2, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        Kh_58U__AS_11_Kilter____640kg__ARM__IN__Pas_Rdr = (
            2,
            Weapons.Kh_58U__AS_11_Kilter____640kg__ARM__IN__Pas_Rdr,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            2,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )

    class Pylon3:
        PROTONB = (3, SWWeapons.PROTONB)
        Kh_58U__AS_11_Kilter____640kg__ARM__IN__Pas_Rdr = (
            3,
            Weapons.Kh_58U__AS_11_Kilter____640kg__ARM__IN__Pas_Rdr,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            3,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        Mk_84___2000lb_GP_Bomb_LD = (3, Weapons.Mk_84___2000lb_GP_Bomb_LD)

    class Pylon4:
        PROTONB = (4, SWWeapons.PROTONB)
        Kh_58U__AS_11_Kilter____640kg__ARM__IN__Pas_Rdr = (
            4,
            Weapons.Kh_58U__AS_11_Kilter____640kg__ARM__IN__Pas_Rdr,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            4,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        Mk_84___2000lb_GP_Bomb_LD = (4, Weapons.Mk_84___2000lb_GP_Bomb_LD)

    class Pylon5:
        Kh_58U__AS_11_Kilter____640kg__ARM__IN__Pas_Rdr = (
            5,
            Weapons.Kh_58U__AS_11_Kilter____640kg__ARM__IN__Pas_Rdr,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            5,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        Mk_84___2000lb_GP_Bomb_LD = (5, Weapons.Mk_84___2000lb_GP_Bomb_LD)

    class Pylon6:
        Mk_84___2000lb_GP_Bomb_LD = (6, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        L_081_Fantasmagoria_ELINT_pod = (6, Weapons.L_081_Fantasmagoria_ELINT_pod)

    class Pylon7:
        ENERGY_CELL___ = (7, SWWeapons.ENERGY_CELL___)

    class Pylon8:
        ENERGY_CELL___ = (8, SWWeapons.ENERGY_CELL___)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.Reconnaissance,
        task.GroundAttack,
        task.CAS,
        task.AFAC,
        task.RunwayAttack,
        task.AntishipStrike,
    ]
    task_default = task.CAS


@planemod
class CORVETTE(PlaneType):
    id = "CORVETTE"
    flyable = True
    height = 20.63
    width = 30
    length = 30.43
    fuel_max = 11000
    max_speed = 792.396
    chaff = 5000
    flare = 5000
    charge_total = 10000
    chaff_charge_size = 1
    flare_charge_size = 1
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    livery_name = "CORVETTE"  # from type

    class Pylon3:
        PROTONM3 = (3, SWWeapons.PROTONM3)

    class Pylon4:
        PROTONM3 = (4, SWWeapons.PROTONM3)

    class Pylon5:
        PROTONM3 = (5, SWWeapons.PROTONM3)

    class Pylon7:
        PROTONM3 = (7, SWWeapons.PROTONM3)

    class Pylon8:
        PROTONM3 = (8, SWWeapons.PROTONM3)

    class Pylon9:
        PROTONM3 = (9, SWWeapons.PROTONM3)

    pylons: Set[int] = {3, 4, 5, 7, 8, 9}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.Reconnaissance,
    ]
    task_default = task.FighterSweep


@planemod
class AWING(PlaneType):
    id = "AWING"
    flyable = True
    height = 5.63
    width = 10
    length = 19.43
    fuel_max = 5000
    max_speed = 1440.396
    chaff = 5000
    flare = 5000
    charge_total = 10000
    chaff_charge_size = 1
    flare_charge_size = 1
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    livery_name = "AWING"  # from type

    class Pylon1:
        PROTONM1 = (1, SWWeapons.PROTONM1)

    class Pylon2:
        ENERGY_CELL = (2, SWWeapons.ENERGY_CELL)

    class Pylon3:
        PROTONM1 = (3, SWWeapons.PROTONM1)

    class Pylon10:
        ENERGY_CELL = (10, SWWeapons.ENERGY_CELL)

    pylons: Set[int] = {1, 2, 3, 10}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.Reconnaissance,
    ]
    task_default = task.CAP


@planemod
class FAUCON(PlaneType):
    id = "FAUCON"
    flyable = True
    height = 5.63
    width = 10
    length = 19.43
    fuel_max = 15000
    max_speed = 2304.396
    chaff = 5000
    flare = 5000
    charge_total = 10000
    chaff_charge_size = 1
    flare_charge_size = 1
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    livery_name = "FAUCON"  # from type

    class Pylon1:
        PROTONF = (1, SWWeapons.PROTONF)

    class Pylon2:
        Lite_Jump_Core_Battery = (2, SWWeapons.Lite_Jump_Core_Battery)

    pylons: Set[int] = {1, 2}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.Reconnaissance,
    ]
    task_default = task.FighterSweep


@planemod
class TIE(PlaneType):
    id = "TIE"
    flyable = True
    height = 5.63
    width = 10
    length = 19.43
    fuel_max = 8000
    max_speed = 2649.996
    chaff = 5000
    flare = 5000
    charge_total = 10000
    chaff_charge_size = 1
    flare_charge_size = 1
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    livery_name = "TIE"  # from type

    class Pylon2:
        ENERGY_CELL_ = (2, SWWeapons.ENERGY_CELL_)

    class Pylon10:
        ENERGY_CELL_ = (10, SWWeapons.ENERGY_CELL_)

    pylons: Set[int] = {2, 10}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.Reconnaissance,
    ]
    task_default = task.FighterSweep


@planemod
class HUNTER(PlaneType):
    id = "HUNTER"
    flyable = True
    height = 5.63
    width = 6
    length = 19.43
    fuel_max = 10000
    max_speed = 2649.996
    chaff = 5000
    flare = 5000
    charge_total = 10000
    chaff_charge_size = 1
    flare_charge_size = 1
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    livery_name = "HUNTER"  # from type

    class Pylon1:
        PROTONM2 = (1, SWWeapons.PROTONM2)

    class Pylon2:
        ENERGY_CELL__ = (2, SWWeapons.ENERGY_CELL__)

    class Pylon3:
        PROTONM2 = (3, SWWeapons.PROTONM2)

    class Pylon10:
        ENERGY_CELL__ = (10, SWWeapons.ENERGY_CELL__)

    pylons: Set[int] = {1, 2, 3, 10}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.Reconnaissance,
    ]
    task_default = task.CAP


@planemod
class TIE_INTER(PlaneType):
    id = "TIE_INTER"
    flyable = True
    height = 5.63
    width = 6
    length = 19.43
    fuel_max = 5000
    max_speed = 1440.396
    chaff = 5000
    flare = 5000
    charge_total = 10000
    chaff_charge_size = 1
    flare_charge_size = 1
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    livery_name = "TIE_INTER"  # from type

    class Pylon1:
        PROTONM1 = (1, SWWeapons.PROTONM1)

    class Pylon2:
        ENERGY_CELL___ = (2, SWWeapons.ENERGY_CELL___)

    class Pylon3:
        PROTONM1 = (3, SWWeapons.PROTONM1)

    class Pylon10:
        ENERGY_CELL___ = (10, SWWeapons.ENERGY_CELL___)

    pylons: Set[int] = {1, 2, 3, 10}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.Reconnaissance,
    ]
    task_default = task.CAP


@planemod
class naboo_starfighter(PlaneType):
    id = "naboo_starfighter"
    flyable = True
    height = 5.63
    width = 5
    length = 10.43
    fuel_max = 9249
    max_speed = 1152.396
    chaff = 0
    flare = 500
    charge_total = 500
    chaff_charge_size = 1
    flare_charge_size = 1
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    livery_name = "NABOO_STARFIGHTER"  # from type

    class Pylon1:
        PROTONM = (1, SWWeapons.PROTONM)

    class Pylon2:
        PROTONM = (2, SWWeapons.PROTONM)
        ENERGY_CELL____ = (2, SWWeapons.ENERGY_CELL____)

    class Pylon3:
        PROTONM = (3, SWWeapons.PROTONM)

    class Pylon4:
        PROTONM = (4, SWWeapons.PROTONM)

    class Pylon5:
        PROTONM = (5, SWWeapons.PROTONM)

    class Pylon6:
        PROTONM = (6, SWWeapons.PROTONM)

    class Pylon10:
        ENERGY_CELL____ = (10, SWWeapons.ENERGY_CELL____)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 10}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.Reconnaissance,
        task.GroundAttack,
        task.CAS,
        task.AFAC,
        task.RunwayAttack,
    ]
    task_default = task.FighterSweep


@planemod
class tie_bomber_2(PlaneType):
    id = "tie_bomber_2"
    flyable = True
    height = 5.63
    width = 10
    length = 19.43
    fuel_max = 6000
    max_speed = 2649.996
    chaff = 5000
    flare = 5000
    charge_total = 10000
    chaff_charge_size = 1
    flare_charge_size = 1
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    livery_name = "TIE_BOMBER_2"  # from type

    class Pylon1:
        PROTONM1 = (1, SWWeapons.PROTONM1)
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            1,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (1, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            1,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        Kh_58U__AS_11_Kilter____640kg__ARM__IN__Pas_Rdr = (
            1,
            Weapons.Kh_58U__AS_11_Kilter____640kg__ARM__IN__Pas_Rdr,
        )

    class Pylon2:
        ENERGY_CELL___ = (2, SWWeapons.ENERGY_CELL___)

    class Pylon3:
        PROTONM1 = (3, SWWeapons.PROTONM1)
        Mk_84___2000lb_GP_Bomb_LD = (3, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            3,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            3,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        Kh_58U__AS_11_Kilter____640kg__ARM__IN__Pas_Rdr = (
            3,
            Weapons.Kh_58U__AS_11_Kilter____640kg__ARM__IN__Pas_Rdr,
        )

    class Pylon4:
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            4,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        PROTONM2 = (4, SWWeapons.PROTONM2)
        Mk_84___2000lb_GP_Bomb_LD = (4, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            4,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        Kh_58U__AS_11_Kilter____640kg__ARM__IN__Pas_Rdr = (
            4,
            Weapons.Kh_58U__AS_11_Kilter____640kg__ARM__IN__Pas_Rdr,
        )

    class Pylon5:
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            5,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        PROTONM2 = (5, SWWeapons.PROTONM2)
        Mk_84___2000lb_GP_Bomb_LD = (5, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            5,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        Kh_58U__AS_11_Kilter____640kg__ARM__IN__Pas_Rdr = (
            5,
            Weapons.Kh_58U__AS_11_Kilter____640kg__ARM__IN__Pas_Rdr,
        )

    class Pylon6:
        L_081_Fantasmagoria_ELINT_pod = (6, Weapons.L_081_Fantasmagoria_ELINT_pod)

    class Pylon7:
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (7, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            7,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        Kh_58U__AS_11_Kilter____640kg__ARM__IN__Pas_Rdr = (
            7,
            Weapons.Kh_58U__AS_11_Kilter____640kg__ARM__IN__Pas_Rdr,
        )

    class Pylon8:
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            8,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        PROTONM2 = (8, SWWeapons.PROTONM2)
        Mk_84___2000lb_GP_Bomb_LD = (8, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            8,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        Kh_58U__AS_11_Kilter____640kg__ARM__IN__Pas_Rdr = (
            8,
            Weapons.Kh_58U__AS_11_Kilter____640kg__ARM__IN__Pas_Rdr,
        )

    class Pylon9:
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            9,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (9, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__ = (
            9,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__,
        )
        Kh_58U__AS_11_Kilter____640kg__ARM__IN__Pas_Rdr = (
            9,
            Weapons.Kh_58U__AS_11_Kilter____640kg__ARM__IN__Pas_Rdr,
        )

    class Pylon10:
        ENERGY_CELL___ = (10, SWWeapons.ENERGY_CELL___)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.Reconnaissance,
        task.GroundAttack,
        task.CAS,
        task.RunwayAttack,
    ]
    task_default = task.GroundAttack


@vehiclemod
class MBT9_EMPIRE(unittype.VehicleType):
    id = "MBT9_EMPIRE"
    name = "SW - MBT-9 IMPERIAL"
    detection_range = 0
    threat_range = 5000
    air_weapon_dist = 5000


@vehiclemod
class MBT9_REBEL(unittype.VehicleType):
    id = "MBT9_REBEL"
    name = "SW - MBT-9 REBEL"
    detection_range = 0
    threat_range = 5000
    air_weapon_dist = 5000


@vehiclemod
class MBT9_AAA_EMPIRE(unittype.VehicleType):
    id = "MBT9_AAA EMPIRE"
    name = "SW - MBT-9AV IMPERIAL"
    detection_range = 0
    threat_range = 12000
    air_weapon_dist = 12000


@vehiclemod
class MBT9_AAA_REBEL(unittype.VehicleType):
    id = "MBT9_AAA REBEL"
    name = "SW - MBT-9AV REBEL"
    detection_range = 0
    threat_range = 12000
    air_weapon_dist = 12000


@vehiclemod
class Jugger(unittype.VehicleType):
    id = "Jugger"
    name = "SW - Juggernaut"
    detection_range = 25000
    threat_range = 30
    air_weapon_dist = 30
    eplrs = True


@vehiclemod
class TB_TT(unittype.VehicleType):
    id = "TB_TT"
    name = "SW - AT-AT"
    detection_range = 5000
    threat_range = 20000
    air_weapon_dist = 20000


@vehiclemod
class SW___TR_TT(unittype.VehicleType):
    id = "SW - TR_TT"
    name = "SW - AT-ST"
    detection_range = 5000
    threat_range = 5000
    air_weapon_dist = 5000


@vehiclemod
class Gozanti(unittype.VehicleType):
    id = "Gozanti"
    name = "SW - Gozanti"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0
    eplrs = True


@shipmod
class Destroyer_carrier(unittype.ShipType):
    id = "Destroyer_carrier"
    name = "SW - ISD carrier"
    plane_num = 72
    helicopter_num = 6
    parking = 11
    detection_range = 25000
    threat_range = 0
    air_weapon_dist = 15000
