from game.ato.flighttype import FlightType
from game.dcs.aircrafttype import (
    AircraftType,
    _DERIVED_TASK_SOURCES,
    derived_task_types,
)


def test_armed_recon_derived_from_cas() -> None:
    assert derived_task_types({FlightType.CAS}, False) == {FlightType.ARMED_RECON}


def test_armed_recon_derived_from_bai() -> None:
    assert derived_task_types({FlightType.BAI}, False) == {FlightType.ARMED_RECON}


def test_sead_sweep_derived_from_sead() -> None:
    assert derived_task_types({FlightType.SEAD}, False) == {FlightType.SEAD_SWEEP}


def test_sead_sweep_derived_from_sead_escort() -> None:
    assert derived_task_types({FlightType.SEAD_ESCORT}, False) == {
        FlightType.SEAD_SWEEP
    }


def test_recovery_requires_carrier() -> None:
    assert derived_task_types({FlightType.REFUELING}, True) == {FlightType.RECOVERY}
    assert derived_task_types({FlightType.REFUELING}, False) == set()


def test_unrelated_task_derives_nothing() -> None:
    assert derived_task_types({FlightType.STRIKE}, True) == set()


def test_helper_agrees_with_airframe_derivation() -> None:
    # Drift guard: the airframe's own derived capabilities must match the rules the
    # shared helper encodes, for every loaded aircraft.
    for aircraft in AircraftType.iter_all():
        caps = set(aircraft.iter_task_capabilities())
        assert derived_task_types(caps, aircraft.carrier_capable) <= caps
        if FlightType.SEAD in caps or FlightType.SEAD_ESCORT in caps:
            assert FlightType.SEAD_SWEEP in caps
        if FlightType.CAS in caps or FlightType.BAI in caps:
            assert FlightType.ARMED_RECON in caps
    assert set(_DERIVED_TASK_SOURCES) == {
        FlightType.SEAD_SWEEP,
        FlightType.ARMED_RECON,
        FlightType.RECOVERY,
    }
