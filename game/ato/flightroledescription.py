from __future__ import annotations

from typing import TYPE_CHECKING

from game.ato.flighttype import FlightType
from game.utils import nautical_miles

if TYPE_CHECKING:
    from game.ato.flight import Flight


def role_description(flight: "Flight") -> str:
    doctrine = flight.coalition.doctrine
    settings = flight.coalition.game.settings
    ft = flight.flight_type
    cap = doctrine.cap_engagement_range
    if ft is FlightType.BARCAP:
        return (
            f"Orbits at the far end of its racetrack, holding back from enemy SAM "
            f"threat, and engages enemy aircraft within {cap.nautical_miles:.0f}nm of its orbit."
        )
    if ft is FlightType.TARCAP:
        return (
            f"Orbits over the target area on a short racetrack and engages enemy "
            f"aircraft within {cap.nautical_miles:.0f}nm of its orbit."
        )
    if ft is FlightType.DEAD:
        return "Flies in and attacks a specific SAM/EWR site (ARM/ASM/guided bombs) to destroy it."
    if ft is FlightType.SEAD_SWEEP:
        rng = nautical_miles(settings.sead_sweep_engagement_range_distance)
        return (
            f"Loiters near the target and engages any air-defence within {rng.nautical_miles:.0f}nm of the "
            f"target — including front-line SAMs inside the bubble."
        )
    if ft is FlightType.ESCORT:
        return (
            f"Flies formation with the package and engages enemy fighters within "
            f"{doctrine.escort_engagement_range.nautical_miles:.0f}nm; reactive only, disengages at split."
        )
    if ft is FlightType.SEAD_ESCORT:
        return (
            f"Flies formation with the package and engages SAM-radar threats within "
            f"{doctrine.sead_escort_engagement_range.nautical_miles:.0f}nm; reactive only, disengages at split."
        )
    if ft is FlightType.CAS:
        rng = nautical_miles(settings.cas_engagement_range_distance)
        return f"Loiters along the front line and engages ground targets within {rng.nautical_miles:.0f}nm; no racetrack orbit."
    if ft is FlightType.SEAD:
        rng = nautical_miles(settings.sead_sweep_engagement_range_distance)
        return (
            f"Loiters at standoff near the target and reactively fires anti-radiation "
            f"missiles at air-defence radars within {rng.nautical_miles:.0f}nm as they "
            f"come up; suppresses rather than destroys."
        )
    if ft in {
        FlightType.BAI,
        FlightType.ANTISHIP,
        FlightType.STRIKE,
        FlightType.OCA_AIRCRAFT,
        FlightType.OCA_RUNWAY,
        FlightType.ARMED_RECON,
    }:
        return "Flies in and attacks the assigned target."
    # Everything else: no descriptor.
    return ""
