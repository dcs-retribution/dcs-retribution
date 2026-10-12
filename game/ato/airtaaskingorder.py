from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List

from game.ato import FlightType
from game.ato.package import Package


@dataclass
class AirTaskingOrder:
    """The entire ATO for one coalition."""

    #: The set of all planned packages in the ATO.
    packages: List[Package] = field(default_factory=list)

    @property
    def has_awacs_package(self) -> bool:
        return any(
            [
                p
                for p in self.packages
                if any([f for f in p.flights if f.flight_type is FlightType.AEWC])
            ]
        )

    def add_package(self, package: Package) -> None:
        """Adds a package to the ATO."""
        self.packages.append(package)

    def remove_package(self, package: Package) -> None:
        """Removes a package from the ATO."""
        # Remove all the flights individually so the database gets updated.
        for flight in list(package.flights):
            package.remove_flight(flight)
        self.packages.remove(package)

    def clear(self) -> None:
        """Removes all packages from the ATO."""
        # Remove all packages individually so the database gets updated.
        for package in list(self.packages):
            self.remove_package(package)

    def shift_time(self, delta: timedelta) -> None:
        """Re-times every scheduled package by delta.

        Flight timing is derived from the package TOT when it is read, so this
        moves the whole ATO onto a new mission start without touching flights,
        loadouts or routes. Unscheduled packages keep the datetime.min sentinel.
        """
        for package in self.packages:
            if package.time_over_target == datetime.min:
                continue
            package.time_over_target += delta
