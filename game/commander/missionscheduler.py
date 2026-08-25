from __future__ import annotations

import logging
import random
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Iterator, Optional, TYPE_CHECKING

from game.ato.flighttype import FlightType
from game.ato.traveltime import TotEstimator
from game.theater import MissionTarget, NavalControlPoint

if TYPE_CHECKING:
    from game.coalition import Coalition
    from game.ato import Package


def coordinated_strike_tot(
    strike_tot: datetime,
    earliest_tot: datetime,
    provider_tots: list[datetime],
    lead: timedelta,
    duration: timedelta,
) -> Optional[datetime]:
    """The TOT placing a strike inside its SEAD window, or None to keep it.

    The window opens ``lead`` after the LATEST covering SEAD/DEAD package's TOT
    (every suppressor on station first) and lasts ``duration`` (push while the
    suppression holds). A strike already inside the window keeps its TOT; one
    outside is moved to the window opening -- delayed if it would have arrived
    before its SEAD (the naked-strike case), pulled forward if the random
    spread had left it long after the window closed. Never earlier than the
    package can physically fly (``earliest_tot``); if even that is past the
    window the TOT is kept unless keeping it would still put the strike ahead
    of its SEAD.
    """
    if not provider_tots:
        return None
    window_start = max(provider_tots) + lead
    window_end = window_start + duration
    if window_start <= strike_tot <= window_end:
        return None
    desired = max(window_start, earliest_tot)
    if desired > window_end and strike_tot >= window_start:
        # Can't make the window, but at least the strike isn't ahead of its
        # SEAD. Leave the spread schedule alone.
        return None
    if desired == strike_tot:
        return None
    return desired


class MissionScheduler:
    #: How long after the covering SEAD/DEAD package's TOT the strike window
    #: opens (suppressors on station first) ...
    SEAD_WINDOW_LEAD = timedelta(minutes=2)
    #: ... and how long it stays open (push while the suppression holds; a
    #: strike randomly spread far beyond this is pulled back into the window).
    SEAD_WINDOW_DURATION = timedelta(minutes=8)

    #: The package types timed into a SEAD window: every FormationAttack
    #: tasking that makes one timed arrival on a point inside a threat ring,
    #: plus CAS.
    #:
    #: CAS is the only PatrollingFlightPlan here. It is included because the
    #: front it patrols sits under the ring, and it climbs into that ring to
    #: escape MANPADS low. Its organic SEAD_SWEEP escort flies the package's
    #: own TOT, so it accompanies rather than pre-suppresses.
    #:
    #: AIR_ASSAULT is the one FormationAttack tasking left out, and not for
    #: want of a covering ring: it is ROTARY_WING, so massing a slow helo into
    #: an eight-minute window with fast movers converging on the same point
    #: trades a suppression gain for a deconfliction risk.
    COORDINATED_STRIKE_TYPES = frozenset(
        {
            FlightType.STRIKE,
            FlightType.BAI,
            FlightType.OCA_RUNWAY,
            FlightType.OCA_AIRCRAFT,
            FlightType.ARMED_RECON,
            FlightType.CAS,
        }
    )

    def __init__(self, coalition: Coalition, desired_mission_length: timedelta) -> None:
        self.coalition = coalition
        self.desired_mission_length = desired_mission_length

    def schedule_missions(self, now: datetime) -> None:
        """Identifies and plans mission for the turn."""

        def start_time_generator(
            count: int, earliest: int, latest: int, margin: int
        ) -> Iterator[timedelta]:
            interval = (latest - earliest) // count
            for time in range(earliest, latest, interval):
                error = random.randint(-margin, margin)
                yield timedelta(seconds=max(0, time + error))

        dca_types = {
            FlightType.BARCAP,
            FlightType.TARCAP,
        }

        previous_cap_end_time: dict[MissionTarget, datetime] = defaultdict(now.replace)
        non_dca_packages = [
            p for p in self.coalition.ato.packages if p.primary_task not in dca_types
        ]

        previous_aewc_end_time: dict[MissionTarget, datetime] = defaultdict(now.replace)

        max_simultaneous_recovery_tankers = 2  # TODO: make configurable
        carrier_etas: dict[MissionTarget, list[datetime]] = defaultdict(list)
        max_carrier_simultaneous_barcaps = 2  # TODO: make configurable
        carrier_barcaps: dict[MissionTarget, int] = defaultdict(int)

        start_time = start_time_generator(
            count=len(non_dca_packages),
            earliest=5 * 60,
            latest=int(self.desired_mission_length.total_seconds()),
            margin=5 * 60,
        )
        for package in self.coalition.ato.packages:
            if package.primary_task is FlightType.RECOVERY:
                continue
            tot = TotEstimator(package).earliest_tot(now)
            if package.primary_task in dca_types:
                previous_end_time = previous_cap_end_time[package.target]
                if tot > previous_end_time:
                    # Can't get there exactly on time, so get there ASAP. This
                    # will typically only happen for the first CAP at each
                    # target.
                    package.time_over_target = tot
                else:
                    package.time_over_target = previous_end_time

                departure_time = self._get_departure_time(package)
                if departure_time is None:
                    continue
                is_naval_cp = isinstance(package.target, NavalControlPoint)
                count = carrier_barcaps[package.target]
                if count >= max_carrier_simultaneous_barcaps - 1 and is_naval_cp:
                    previous_cap_end_time[package.target] = departure_time
                    carrier_barcaps[package.target] = 0
                elif is_naval_cp:
                    carrier_barcaps[package.target] += 1
                elif not is_naval_cp:
                    previous_cap_end_time[package.target] = departure_time
            elif package.auto_asap:
                package.set_tot_asap(now)
            elif package.primary_task is FlightType.AEWC:
                last = previous_aewc_end_time[package.target]
                package.time_over_target = tot if tot > last else last
                departure_time = self._get_departure_time(package)
                if departure_time is None:
                    continue
                previous_aewc_end_time[package.target] = departure_time
            else:
                # But other packages should be spread out a bit. Note that take
                # times are delayed, but all aircraft will become active at
                # mission start. This makes it more worthwhile to attack enemy
                # airfields to hit grounded aircraft, since they're more likely
                # to be present. Runway and air started aircraft will be
                # delayed until their takeoff time by AirConflictGenerator.
                package.time_over_target = next(start_time) + tot

        # Time strikes into their SEAD windows BEFORE collecting the recovery
        # ETAs below: landing_time is derived from the package TOT, so a
        # retimed package collected earlier would book its tanker against a
        # landing it no longer flies.
        self._coordinate_sead_windows(now)

        for package in self.coalition.ato.packages:
            if package.primary_task is FlightType.RECOVERY:
                continue
            for f in package.flights:
                if f.departure.is_fleet and not f.is_helo:
                    carrier_etas[f.departure].append(
                        f.flight_plan.landing_time - timedelta(minutes=10)
                    )

        # division by 2 is meant to provide some leeway to avoid filtering out too many ETAs
        duration = self.coalition.game.settings.desired_tanker_on_station_time / 2

        for cp in carrier_etas:
            filtered: list[datetime] = []
            for eta in sorted(carrier_etas[cp]):
                count = len([t for t in filtered if eta < t + duration])
                if count < max_simultaneous_recovery_tankers:
                    filtered.append(eta)
            carrier_etas[cp] = filtered
        for package in [
            p
            for p in self.coalition.ato.packages
            if p.primary_task is FlightType.RECOVERY
        ]:
            if carrier_etas[package.target]:
                package.time_over_target = carrier_etas[package.target].pop(0)

    def _coordinate_sead_windows(self, now: datetime) -> None:
        """Cross-package SEAD-before-strike sequencing.

        Packages are timed independently, so nothing stops the random spread
        from sending a strike into a defended target half an hour BEFORE the
        SEAD package tasked against the SAM covering it. This pass finds, for
        every movable strike-class package, the SEAD/DEAD packages whose target
        ground object's threat ring covers the strike's target, and retimes the
        strike into the window just behind the latest of them. Several strikes
        behind one SEAD mass into the same window, which is the point -- it
        reads as a push.

        Only AI, non-ASAP packages move: a package with a player flight is
        never rescheduled, but a player-flown SEAD still opens a window the AI
        strikes push behind, because providers are only read.
        """
        if not self.coalition.game.settings.sead_strike_coordination:
            return
        providers: list[tuple[Package, float]] = []
        for package in self.coalition.ato.packages:
            if package.primary_task not in (FlightType.SEAD, FlightType.DEAD):
                continue
            # SEAD/DEAD is planned against a SAM ground object; duck-typed so
            # any non-TGO tasking degrades to "no window" rather than crashing.
            threat_range = getattr(package.target, "max_threat_range", None)
            if threat_range is None:
                continue
            ring_meters = threat_range().meters
            if ring_meters <= 0:
                continue
            providers.append((package, ring_meters))
        if not providers:
            return
        for package in self.coalition.ato.packages:
            if package.primary_task not in self.COORDINATED_STRIKE_TYPES:
                continue
            if package.auto_asap or package.has_players:
                continue
            provider_tots = [
                p.time_over_target
                for p, ring in providers
                if p.target.position.distance_to_point(package.target.position) <= ring
            ]
            if not provider_tots:
                continue
            new_tot = coordinated_strike_tot(
                package.time_over_target,
                TotEstimator(package).earliest_tot(now),
                provider_tots,
                self.SEAD_WINDOW_LEAD,
                self.SEAD_WINDOW_DURATION,
            )
            if new_tot is not None:
                logging.debug(
                    "SEAD window: retimed %s vs %s from %s to %s",
                    package.primary_task,
                    getattr(package.target, "name", "target"),
                    package.time_over_target,
                    new_tot,
                )
                package.time_over_target = new_tot

    @staticmethod
    def _get_departure_time(package: Package) -> datetime | None:
        departure_time = package.mission_departure_time
        # Should be impossible for CAP/AEWC
        if departure_time is None:
            logging.error(f"Could not determine mission end time for {package}")
        return departure_time
