from __future__ import annotations

import logging
import random
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Iterator, TYPE_CHECKING

from game.ato.flighttype import FlightType
from game.ato.traveltime import TotEstimator
from game.theater import MissionTarget, NavalControlPoint

if TYPE_CHECKING:
    from game.coalition import Coalition
    from game.ato import Package

logger = logging.getLogger(__name__)


class MissionScheduler:
    def __init__(self, coalition: Coalition, desired_mission_length: timedelta) -> None:
        self.coalition = coalition
        self.desired_mission_length = desired_mission_length

    def _cluster_packages_by_location(
        self, packages: list[Package]
    ) -> list[list[Package]]:
        """Group packages by geographic proximity to optimize TOT scheduling.
        
        Packages attacking targets in the same area should have similar TOTs
        to reduce overall mission time and allow better coordination.
        """
        if not packages:
            return []
        
        # Distance threshold for clustering (in meters) - targets within 150km are considered "nearby"
        CLUSTER_DISTANCE_THRESHOLD = 150000.0
        
        clusters: list[list[Package]] = []
        remaining = packages.copy()
        
        while remaining:
            # Start new cluster with first remaining package
            seed = remaining.pop(0)
            cluster = [seed]
            
            # Find all packages with targets close to this one
            i = 0
            while i < len(remaining):
                pkg = remaining[i]
                # Check distance to any package already in cluster
                is_nearby = any(
                    pkg.target.distance_to(c.target) < CLUSTER_DISTANCE_THRESHOLD
                    for c in cluster
                )
                if is_nearby:
                    cluster.append(remaining.pop(i))
                else:
                    i += 1
            
            clusters.append(cluster)
        
        # Logging moved to cluster processing loop below
        return clusters

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

        # Group packages by geographic proximity
        package_clusters = self._cluster_packages_by_location(non_dca_packages)
        
        # Pre-calculate earliest TOT for each package to understand travel times
        package_earliest_tots = {}
        for pkg in non_dca_packages:
            earliest = TotEstimator(pkg).earliest_tot(now)
            package_earliest_tots[pkg] = earliest
        
        # Calculate time windows for each cluster based on TOT (not departure time)
        # Ensure all TOTs fit within mission duration
        cluster_tot_map = {}
        if package_clusters:
            logger.info(f"[Scheduler] Grouped {len(non_dca_packages)} packages into "
                       f"{len(package_clusters)} geographic clusters")
            
            mission_end = now + self.desired_mission_length
            
            # Find the latest TOT we can accommodate (mission end minus some buffer)
            latest_acceptable_tot = mission_end - timedelta(minutes=5)
            
            cluster_interval = max(
                60,  # Minimum 1 minute between cluster TOT windows
                int(self.desired_mission_length.total_seconds() - 10 * 60) // len(package_clusters)
            )
            
            for i, cluster in enumerate(package_clusters):
                # Log cluster details
                target_names = ", ".join(p.target.name for p in cluster[:3])
                if len(cluster) > 3:
                    target_names += f" (+{len(cluster)-3} more)"
                logger.info(f"[Scheduler]   Cluster {i+1}: {len(cluster)} packages near {target_names}")
                
                # Calculate TOT window for this cluster (these are absolute datetimes)
                cluster_tot_start = now + timedelta(seconds=5 * 60 + i * cluster_interval)
                cluster_tot_end = min(
                    cluster_tot_start + timedelta(minutes=10),  # 10 minute TOT window per cluster
                    latest_acceptable_tot
                )
                
                # Convert to seconds for the generator
                tot_start_sec = (cluster_tot_start - now).total_seconds()
                tot_end_sec = (cluster_tot_end - now).total_seconds()
                
                logger.info(f"[Scheduler]   Cluster {i+1} TOT window: "
                           f"{tot_start_sec//60:.0f}-{tot_end_sec//60:.0f} min")
                
                # Within each cluster, spread TOTs with small random variation
                margin = min(2 * 60, (tot_end_sec - tot_start_sec) // 4)  # 2 min max variation
                gen = start_time_generator(
                    count=len(cluster),
                    earliest=int(tot_start_sec),
                    latest=int(tot_end_sec),
                    margin=int(margin)
                )
                
                for pkg in cluster:
                    desired_tot_offset = next(gen)
                    desired_tot = now + desired_tot_offset
                    earliest_tot = package_earliest_tots.get(pkg, desired_tot)
                    
                    # Can't arrive before we can physically get there
                    actual_tot = max(desired_tot, earliest_tot)
                    
                    # Warn if package TOT exceeds mission duration
                    if actual_tot > mission_end:
                        travel_time_min = (earliest_tot - now).total_seconds() / 60
                        logger.warning(f"[Scheduler] Package to {pkg.target.name} TOT exceeds "
                                     f"mission duration (travel time: {travel_time_min:.0f}min, "
                                     f"TOT: {(actual_tot - now).total_seconds()/60:.0f}min)")
                    
                    cluster_tot_map[pkg] = actual_tot
        
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
                # Use clustered TOT if available, ensuring it's within mission duration
                if package in cluster_tot_map:
                    package.time_over_target = cluster_tot_map[package]
                else:
                    # Fallback for packages not in clusters (shouldn't happen)
                    package.time_over_target = tot
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

    @staticmethod
    def _get_departure_time(package: Package) -> datetime | None:
        departure_time = package.mission_departure_time
        # Should be impossible for CAP/AEWC
        if departure_time is None:
            logging.error(f"Could not determine mission end time for {package}")
        return departure_time
