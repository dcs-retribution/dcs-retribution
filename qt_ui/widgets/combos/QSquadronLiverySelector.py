import logging

from PySide6.QtWidgets import QComboBox

from game.squadrons import Squadron


class SquadronLiverySelector(QComboBox):
    """
    A combo box for selecting a squadron's livery.
    The combo box will automatically be populated with all available liveries.
    """

    def __init__(self, squadron: Squadron) -> None:
        super().__init__()
        self.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)

        self.aircraft_type = squadron.aircraft
        selected_livery = squadron.livery

        liveries = set()
        cc = squadron.coalition.faction.country.shortname
        aircraft_liveries = set(self.aircraft_type.dcs_unit_type.iter_liveries())
        if len(aircraft_liveries) == 0:
            logging.info(f"Liveries for {self.aircraft_type} is empty!")
        for livery in aircraft_liveries:
            valid_livery = livery.countries is None or cc in livery.countries
            if valid_livery or cc in ["BLUE", "RED"]:
                liveries.add(livery)
        faction = squadron.coalition.faction
        overrides = [
            x
            for x in faction.liveries_overrides.get(self.aircraft_type, [])
            if x in [y.id.lower() for y in liveries]
        ]
        if selected_livery is None and squadron.livery_set:
            self.addItem("Using livery-set from squadron's yaml", userData=None)
            self.setEnabled(False)
            return
        if selected_livery is None and squadron.aircraft.default_livery:
            selected_livery = squadron.aircraft.default_livery
        if len(overrides) > 0:
            self.addItem("Use livery overrides", userData=None)
        for livery in sorted(liveries):
            self.addItem(livery.name, userData=livery.id)
            if selected_livery is not None:
                if selected_livery.lower() == livery.id:
                    self.setCurrentText(livery.name)
        if len(liveries) == 0:
            self.addItem("No available liveries (using DCS default)")
            self.setEnabled(False)
