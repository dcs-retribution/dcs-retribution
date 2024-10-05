import logging

from PySide6.QtWidgets import QComboBox

from game.squadrons import Squadron

LIVERY_SET_TEXT = "Use livery-set from squadron's yaml"


class SquadronLiverySelector(QComboBox):
    """
    A combo box for selecting a squadron's livery.
    The combo box will automatically be populated with all available liveries.
    """

    def __init__(self, squadron: Squadron, update_squadron: bool = True) -> None:
        super().__init__()
        self.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)

        self.squadron = squadron
        self.aircraft_type = squadron.aircraft
        selected_livery = squadron.livery

        if update_squadron:
            self.currentTextChanged.connect(self.on_change)

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
        if selected_livery and selected_livery.lower() not in [
            livery.id.lower() for livery in liveries
        ]:
            # squadron livery not found, or incompatible with faction
            # => attempt to use the unit's default-livery as a fallback
            selected_livery = None
        if squadron.livery_set:
            self.addItem(LIVERY_SET_TEXT, userData=None)
        if len(overrides) > 0:
            self.addItem("Use livery overrides", userData=None)
        if (
            selected_livery is None
            and not squadron.livery_set
            and squadron.aircraft.default_livery
        ):
            selected_livery = squadron.aircraft.default_livery
        for livery in sorted(liveries):
            self.addItem(livery.name, userData=livery.id)
            if selected_livery is not None and not squadron.livery_set:
                if selected_livery.lower() == livery.id:
                    self.setCurrentText(livery.name)
        if len(liveries) == 0:
            self.addItem("No available liveries (using DCS default)")
            self.setEnabled(False)

    @property
    def using_livery_set(self) -> bool:
        return self.currentText() == LIVERY_SET_TEXT

    def on_change(self, text: str) -> None:
        self.squadron.livery = self.currentData()
        if text == LIVERY_SET_TEXT:
            self.squadron.use_livery_set = True
        else:
            self.squadron.use_livery_set = False
